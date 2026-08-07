"""
실험 공용 모듈 - 데이터 로드, Pipeline 팩토리, 평가, 통계 비교(McNemar), 결과 로깅

가설(실험)마다 달라지는 부분(피처 구성, 결측치 전략, 모델 종류 등)은 이 모듈을 쓰는
쪽(experiments/*.ipynb)에서 결정하고, 여기는 모든 실험이 공통으로 재사용하는 뼈대만 둔다.
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"

COLUMN_NAMES = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country", "income",
]

ALL_NUMERIC_COLS = ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
ALL_CATEGORICAL_COLS = ["workclass", "education", "marital-status", "occupation", "relationship", "race", "sex", "native-country"]
TARGET_COL = "income"

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
RESULTS_LOG_PATH = os.path.join(RESULTS_DIR, "experiment_log.csv")


def load_raw(url: str = DATA_URL) -> pd.DataFrame:
    """Adult 데이터를 로드하고, 문자열 공백 제거 + '?' -> NaN 변환만 수행한다.

    결측치를 어떻게 처리할지(제거/대치)는 여기서 정하지 않는다 - 그게 실험 대상이다.
    """
    df = pd.read_csv(url, header=None, names=COLUMN_NAMES, skipinitialspace=True)

    obj_cols = df.select_dtypes(include="object").columns
    df[obj_cols] = df[obj_cols].apply(lambda s: s.str.strip())
    df[obj_cols] = df[obj_cols].replace("?", np.nan)

    df[TARGET_COL] = df[TARGET_COL].str.rstrip(".")
    return df


def make_xy(df: pd.DataFrame, feature_cols: list[str]):
    """feature_cols만 골라 X, y(0/1)를 반환한다."""
    X = df[feature_cols].copy()
    y = (df[TARGET_COL] == ">50K").astype(int)
    return X, y


def make_pipeline(
    numeric_cols: list[str],
    categorical_cols: list[str],
    model,
    numeric_impute_strategy: str = "median",
    categorical_impute_strategy: str = "most_frequent",
    categorical_fill_value: str | None = None,
    add_missing_indicator: bool = False,
) -> Pipeline:
    """전처리(ColumnTransformer) + 모델을 하나로 묶은 Pipeline을 만든다.

    numeric_cols/categorical_cols/impute 전략/모델을 실험마다 바꿔가며 호출하면 된다.
    categorical_impute_strategy="constant"로 두고 categorical_fill_value(예: "Missing")를
    지정하면, 결측을 최빈값으로 덮지 않고 별도 범주로 남겨서 원-핫 인코딩에 포함시킨다.
    add_missing_indicator=True면 결측 여부를 나타내는 이진 컬럼이 추가된다.
    """
    numeric_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy=numeric_impute_strategy, add_indicator=add_missing_indicator)),
        ("scale", StandardScaler()),
    ])
    categorical_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy=categorical_impute_strategy, fill_value=categorical_fill_value,
                                  add_indicator=add_missing_indicator)),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_cols),
        ("cat", categorical_pipeline, categorical_cols),
    ])

    return Pipeline([
        ("preprocess", preprocessor),
        ("model", model),
    ])


def evaluate(pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """학습된 pipeline을 평가하고 지표 + 예측값을 dict로 반환한다."""
    y_pred = pipeline.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
    }

    if hasattr(pipeline, "predict_proba"):
        y_proba = pipeline.predict_proba(X_test)[:, 1]
        metrics["roc_auc"] = roc_auc_score(y_test, y_proba)
    else:
        y_proba = None

    return {"metrics": metrics, "y_pred": y_pred, "y_proba": y_proba}


def compare_models(y_true, pred_a, pred_b, name_a: str = "A", name_b: str = "B", alpha: float = 0.05) -> dict:
    """같은 테스트셋에 대한 두 모델의 예측을 McNemar's test로 비교한다.

    귀무가설(H0): 두 모델의 오류 패턴에 차이가 없다 (한쪽만 맞히는 비율이 같다).
    """
    y_true = np.asarray(y_true)
    pred_a = np.asarray(pred_a)
    pred_b = np.asarray(pred_b)

    correct_a = (pred_a == y_true)
    correct_b = (pred_b == y_true)

    both_correct = int(np.sum(correct_a & correct_b))
    only_a_correct = int(np.sum(correct_a & ~correct_b))
    only_b_correct = int(np.sum(~correct_a & correct_b))
    both_wrong = int(np.sum(~correct_a & ~correct_b))

    table = [[both_correct, only_a_correct], [only_b_correct, both_wrong]]

    discordant = only_a_correct + only_b_correct
    exact = discordant < 25
    result = mcnemar(table, exact=exact, correction=not exact)

    p_value = result.pvalue
    significant = p_value < alpha

    if not significant:
        interpretation = f"p={p_value:.4g} >= {alpha}: '{name_a}'와 '{name_b}'의 오류 패턴 차이가 통계적으로 유의하지 않음 (우연일 수 있음)"
    elif only_a_correct > only_b_correct:
        interpretation = f"p={p_value:.4g} < {alpha}: '{name_a}'가 '{name_b}'보다 통계적으로 유의하게 더 나음"
    else:
        interpretation = f"p={p_value:.4g} < {alpha}: '{name_b}'가 '{name_a}'보다 통계적으로 유의하게 더 나음"

    return {
        "table": {"both_correct": both_correct, f"only_{name_a}_correct": only_a_correct,
                  f"only_{name_b}_correct": only_b_correct, "both_wrong": both_wrong},
        "statistic": result.statistic,
        "p_value": p_value,
        "significant": significant,
        "interpretation": interpretation,
    }


def log_result(run_name: str, experiment_group: str, description: str, metrics: dict,
               compared_to: str | None = None, mcnemar_result: dict | None = None,
               log_path: str = RESULTS_LOG_PATH) -> None:
    """실험 1회 결과를 log_path(csv)에 한 줄 추가한다. 파일 없으면 헤더와 함께 생성."""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "experiment_group": experiment_group,
        "run_name": run_name,
        "description": description,
        **metrics,
        "compared_to": compared_to or "",
        "mcnemar_p_value": mcnemar_result["p_value"] if mcnemar_result else "",
        "mcnemar_significant": mcnemar_result["significant"] if mcnemar_result else "",
        "mcnemar_interpretation": mcnemar_result["interpretation"] if mcnemar_result else "",
    }

    df_row = pd.DataFrame([row])
    header = not os.path.exists(log_path)
    df_row.to_csv(log_path, mode="a", header=header, index=False)
    print(f"[logged] {run_name} -> {log_path}")


def show_log(experiment_group: str | None = None, log_path: str = RESULTS_LOG_PATH) -> pd.DataFrame:
    """지금까지 쌓인 실험 로그를 읽어서 보여준다. experiment_group으로 필터링 가능."""
    if not os.path.exists(log_path):
        print("아직 기록된 실험이 없습니다.")
        return pd.DataFrame()

    df = pd.read_csv(log_path)
    if experiment_group is not None:
        df = df[df["experiment_group"] == experiment_group]
    return df.sort_values("f1", ascending=False)
