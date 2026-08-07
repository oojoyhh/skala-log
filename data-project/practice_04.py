"""
sales_100k.csv EDA 시각화 · 통계 검정 · sklearn Pipeline · Plotly 인터랙티브 차트

작성자: 김효주

[전체 설명]
  1) 실습3에서 IQR로 이상치 제거한 df_clean을 입력으로 사용해
     히스토그램+KDE / 박스플롯 / 월별 라인 / 상관 히트맵 4종을 2x2 서브플롯에 그린다.
  2) 서울 vs 부산 평균 매출 차이를 t-test로, region x category 독립성을
     카이제곱 검정으로 확인하고 각각 귀무가설/대립가설과 p-value 해석을 출력한다.
  3) ColumnTransformer + Pipeline으로 전처리와 회귀 모델을 하나로 묶어
     학습 -> 예측 -> 평가 -> 저장 -> 재로딩까지 수행한다.
  4) 지역·카테고리별 총매출을 Plotly 막대 차트로 만들어 HTML로 저장한다.

[연계]
  - IQR 이상치 제거된 df_clean을 시각화/통계 검정/파이프라인 입력 데이터로 공통 사용
  - region x category groupby 결과를 카이제곱 분할표 및 Plotly 차트의 기반으로 공통 활용

[변경내역]
  v1.0 : 2x2 서브플롯(히스토그램+KDE, 박스플롯, 월별 라인, 상관 히트맵) 작성
  v1.1 : t-test(서울 vs 부산), 카이제곱(category x payment_method) 검정 + 귀무/대립가설 추가
  v1.2 : sklearn Pipeline 구성, 학습/평가/저장/재로딩 추가
  v1.3 : Plotly 인터랙티브 차트 작성 및 html 저장 추가
  v1.4 : Pipeline에 predict() 명시적 호출 추가
  v1.5 : 카이제곱 검정을 category x payment_method -> region x category로 변경 (연계 취지에 맞춤)
         한글 폰트 자동 탐색 함수 추가
  v1.6 : t-test/카이제곱 함수를 특정 값(서울/부산 등) 하드코딩 대신 인자로 받도록 일반화
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
import joblib
import plotly.express as px

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "data", "sales_100k.csv")
EDA_IMG_PATH = os.path.join(SCRIPT_DIR, "eda_4plots.png")
MODEL_PATH = os.path.join(SCRIPT_DIR, "sales_pipeline.joblib")
CHART_HTML_PATH = os.path.join(SCRIPT_DIR, "region_category_sales.html")


def set_korean_font() -> str:
    # 폰트 설정
    installed = {f.name for f in font_manager.fontManager.ttflist}
    candidates = ["AppleGothic", "Malgun Gothic", "NanumGothic", "Noto Sans CJK KR", "Noto Sans KR"]
    font_name = next((f for f in candidates if f in installed), "DejaVu Sans")

    plt.rcParams["font.family"] = font_name
    plt.rcParams["axes.unicode_minus"] = False  # 한글 폰트 적용 시 마이너스(-) 기호가 깨지는 것 방지

    if font_name == "DejaVu Sans":
        print("한글 폰트를 찾지 못해 그래프 제목이 깨질 수 있습니다.")
    return font_name


def load_clean_data(path: str = DATA_PATH, target_col: str = "amount") -> pd.DataFrame:
    """CSV를 불러오고, target_col 기준 IQR 이상치를 제거해서 돌려준다."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

    try:
        raw = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV 파일이 비어 있습니다: {path}")

    if target_col not in raw.columns:
        raise KeyError(f"'{target_col}' 컬럼이 존재하지 않습니다.")

    # 사분위수 기준 정상 범위를 벗어나는 값을 이상치로 간주
    q1 = raw[target_col].quantile(0.25)
    q3 = raw[target_col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # between()은 NaN을 자동으로 False 처리하므로, target_col 결측치도 이 과정에서 함께 걸러진다
    clean = raw[raw[target_col].between(lower_bound, upper_bound)].copy()
    print(f"제거 전: {len(raw):,}행 -> 제거 후: {len(clean):,}행")
    return clean


def plot_eda(df: pd.DataFrame, save_path: str = EDA_IMG_PATH) -> None:
    """매출 데이터 EDA용 2x2 차트(분포/지역별비교/월별추이/상관관계)를 그려서 저장."""
    set_korean_font()

    data = df.copy()
    # 일 단위 날짜를 월 단위로 뭉개서 월별 추이를 볼 수 있게 가공
    data["order_date"] = pd.to_datetime(data["order_date"])
    data["year_month"] = data["order_date"].dt.to_period("M").astype(str)
    monthly_total = data.groupby("year_month")["amount"].sum().reset_index()

    numeric_cols = ["quantity", "unit_price", "customer_age", "amount"]
    corr_matrix = data[numeric_cols].corr()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 매출액이 특정 구간에 몰려있는지, 꼬리가 긴 분포인지 파악
    sns.histplot(data=data, x="amount", kde=True, ax=axes[0, 0])
    axes[0, 0].set_title("Amount 분포 (히스토그램+KDE)")

    # 지역별로 매출 규모나 변동폭에 눈에 띄는 차이가 있는지 확인
    sns.boxplot(data=data, x="region", y="amount", ax=axes[0, 1])
    axes[0, 1].set_title("지역별 Amount 분포")
    axes[0, 1].tick_params(axis="x", rotation=45)  # 지역명이 겹치지 않도록 라벨 회전

    # 계절성이나 추세가 있는지 시간 흐름에 따라 확인
    axes[1, 0].plot(monthly_total["year_month"], monthly_total["amount"])
    axes[1, 0].set_title("월별 총매출 추이")
    axes[1, 0].tick_params(axis="x", rotation=45)

    # amount와 다른 숫자형 컬럼들 간 선형 관계 파악 (quantity/unit_price가 높게 나올 것으로 예상)
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=axes[1, 1])
    axes[1, 1].set_title("숫자형 컬럼 상관 히트맵")

    plt.tight_layout()

    try:
        plt.savefig(save_path, dpi=100)
    except OSError as e:
        raise RuntimeError(f"이미지 저장 실패: {e}")
    finally:
        plt.close(fig)  # 메모리에 figure가 계속 쌓이지 않도록 명시적으로 닫기

    print(f"[시각화] 4종 차트 저장 완료: {save_path}")


def compare_group_means(df: pd.DataFrame, group_col: str, group_a: str, group_b: str, value_col: str = "amount") -> None:
    """
    두 그룹의 평균(value_col)이 통계적으로 다른지 독립표본 t-test로 확인.
    귀무가설(H0): group_a와 group_b의 평균 {value_col}은 차이가 없다
    대립가설(H1): group_a와 group_b의 평균 {value_col}은 차이가 있다
    """
    sample_a = df.loc[df[group_col] == group_a, value_col]
    sample_b = df.loc[df[group_col] == group_b, value_col]

    if sample_a.empty or sample_b.empty:
        raise ValueError(f"{group_a} 또는 {group_b} 데이터가 없어 t-test를 수행할 수 없습니다.")

    # 두 그룹의 분산이 같다고 가정하지 않는 Welch's t-test
    t_stat, p_value = stats.ttest_ind(sample_a, sample_b, equal_var=False)
    print(f"[t-test] {group_a} vs {group_b} - t={t_stat:.4f}, p={p_value:.4f}")

    if p_value < 0.05:
        print(f"=> p={p_value:.4f} < 0.05 이므로 귀무가설을 기각한다. "
              f"{group_a}과 {group_b}의 평균 {value_col}은 통계적으로 유의미한 차이가 있다.")
    else:
        print(f"=> p={p_value:.4f} >= 0.05 이므로 귀무가설을 기각하지 못한다. "
              f"{group_a}과 {group_b}의 평균 {value_col} 차이는 통계적으로 유의미하지 않다.")


def test_independence(df: pd.DataFrame, col_a: str, col_b: str) -> None:
    """
    두 범주형 컬럼(col_a, col_b)이 서로 독립인지 카이제곱 검정으로 확인.
    귀무가설(H0): col_a와 col_b는 서로 독립이다 (관련 없다)
    대립가설(H1): col_a와 col_b는 서로 독립이 아니다 (관련 있다)
    """
    # 두 범주형 변수의 조합별 빈도를 세어 분할표로 만듦
    contingency = pd.crosstab(df[col_a], df[col_b])
    chi2, p_value, dof, _ = stats.chi2_contingency(contingency)
    print(f"[카이제곱] {col_a} x {col_b} - chi2={chi2:.4f}, p={p_value:.4f}, dof={dof}")

    if p_value < 0.05:
        print(f"=> p={p_value:.4f} < 0.05 이므로 귀무가설을 기각한다. "
              f"{col_a}와 {col_b}는 서로 독립이 아니다 (연관성 있음).")
    else:
        print(f"=> p={p_value:.4f} >= 0.05 이므로 귀무가설을 기각하지 못한다. "
              f"{col_a}와 {col_b}는 통계적으로 독립이다 (연관성 없음).")


def train_pipeline(df: pd.DataFrame, model_path: str = MODEL_PATH) -> Pipeline:
    """전처리 + 회귀모델을 Pipeline으로 묶어 학습하고, 평가 후 파일로 저장/재로딩 검증."""
    data = df.dropna(subset=["region", "category"]).copy()

    numeric_cols = ["quantity", "unit_price", "customer_age"]
    category_cols = ["region", "category", "payment_method", "customer_gender"]

    X = data[numeric_cols + category_cols]
    y = data["amount"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer(transformers=[
        ("scale", StandardScaler(), numeric_cols),
        # handle_unknown="ignore": 학습 때 없던 새 카테고리 값이 들어와도 에러 대신 무시하고 진행
        ("encode", OneHotEncoder(handle_unknown="ignore"), category_cols),
    ])

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression()),
    ])

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(f"[Pipeline] 예측값 샘플 (상위 5개): {preds[:5]}")

    r2 = model.score(X_test, y_test)
    print(f"[Pipeline] R^2 score: {r2:.4f}")

    try:
        joblib.dump(model, model_path)
    except OSError as e:
        raise RuntimeError(f"모델 저장 실패: {e}")
    print("모델 저장 완료")

    # 저장 -> 로딩 과정에서 모델이 손상되지 않았는지, 저장이 제대로 됐는지 확인
    try:
        reloaded = joblib.load(model_path)
    except (OSError, EOFError) as e:
        raise RuntimeError(f"모델 재로딩 실패: {e}")

    reloaded_r2 = reloaded.score(X_test, y_test)
    print(f"재로딩 후 score: {reloaded_r2:.4f} (원래 score와 일치: {reloaded_r2 == r2})")

    return model


def plot_sales_bar(df: pd.DataFrame, save_path: str = CHART_HTML_PATH) -> None:
    """지역·카테고리별 총매출을 인터랙티브 막대 차트로 만들어 HTML로 저장."""
    sales_by_group = df.groupby(["region", "category"], as_index=False)["amount"].sum()
    sales_by_group.columns = ["region", "category", "total"]

    fig = px.bar(
        sales_by_group, x="region", y="total", color="category",
        barmode="group",  # 카테고리별 막대를 겹치지 않고 나란히 배치
        title="지역·카테고리별 총매출",
    )

    try:
        fig.write_html(save_path)
    except OSError as e:
        raise RuntimeError(f"차트 저장 실패: {e}")

    print(f"[Plotly] 인터랙티브 차트 저장 완료: {save_path}")


if __name__ == "__main__":
    df_clean = load_clean_data()

    plot_eda(df_clean)

    compare_group_means(df_clean, group_col="region", group_a="서울", group_b="부산")
    test_independence(df_clean, col_a="region", col_b="category")

    train_pipeline(df_clean)
    plot_sales_bar(df_clean)