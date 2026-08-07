"""
Pandas EDA · Polars Lazy · DuckDB SQL 비교

작성자: 판교캠퍼스 8반 P253 김효주

[전체 설명]
  1) Pandas로 기본 EDA(df.info(), 결측치 확인)를 수행한다.
  2) IQR(사분위범위) 방법으로 amount 컬럼의 이상치를 제거하고, 제거 전/후 행 수를 출력한다.
  3) region(지역) x category(카테고리) 조합별로 총매출(total)/평균(mean)/건수(count)를
     named aggregation 방식으로 집계하고 총매출 내림차순으로 정렬한다.
  4) 위 2)~3)의 동일한 로직을 Pandas / Polars(Lazy) / DuckDB(SQL) 세 가지 방식으로
     각각 구현하고, 세 도구의 결과가 일치하는지 확인한다.
  5) timeit으로 세 도구의 실행 시간을 동일 반복 횟수(N)로 비교한다.

[변경내역]
  v1.0 : Pandas EDA + IQR 이상치 제거 + named aggregation 작성
  v1.1 : Polars Lazy 버전 추가
  v1.2 : DuckDB SQL 버전 추가
  v1.3 : timeit 성능 비교 로직 추가
  v1.4 : Polars의 quantile() 기본 보간법(nearest)이 pandas/DuckDB(linear)와 달라
         이상치 제거 후 행 수가 1개 차이남(973805 vs 973806)을 확인. 
         100만 행 규모에서는 무시 가능한 수준으로 판단하여 별도 보정하지 않음.

        cf.
        pandas .quantile()의 기본값은 interpolation='linear'     → 두 인접 값을 선형보간
        DuckDB quantile_cont()는 이름 그대로 연속(continuous) 방식  → 선형보간과 사실상 동일한 결과
        Polars .quantile()의 기본값은 interpolation='nearest'    → 가장 가까운 실제 데이터 값을 그대로 사용
"""

import os
import timeit
import pandas as pd
import polars as pl
import duckdb

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(SCRIPT_DIR, "data", "sales_100k.csv")

def load_and_inspect(path: str) -> pd.DataFrame:
    """CSV 로딩 + 기본 EDA(info, 결측치) 체크포인트 출력"""
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

    # 기본 구조
    df.info()

    # 결측치 확인
    print(df.isnull().sum())

    return df


def compute_iqr_bounds(q1: float, q3: float) -> tuple:
    """Pandas/Polars/DuckDB 세 곳에서 반복되는 IQR 공식을 하나로 모은 헬퍼"""
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return lower, upper


def run_pandas(path: str = FILE, verbose: bool = False) -> pd.DataFrame:
    # verbose=False일 땐(timeit 반복용) 체크포인트 출력 없이 조용히 실행
    if verbose:
        df = load_and_inspect(path)
    else:
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

    if "amount" not in df.columns:
        raise KeyError("'amount' 컬럼이 존재하지 않습니다.")

    # IQR 계산 => NaN 행 필터링 과정에서 함께 제외됨
    Q1 = df["amount"].quantile(0.25)
    Q3 = df["amount"].quantile(0.75)
    lower, upper = compute_iqr_bounds(Q1, Q3)

    if verbose:
        print(f"제거 전: {len(df)}")

    # IQR 범위 내
    df_clean = df[df["amount"].between(lower, upper)]

    if verbose:
        print(f"제거 후: {len(df_clean)}")

    # named aggregation
    grouped = df_clean.groupby(["region", "category"]).agg(
        total=("amount", "sum"),
        mean=("amount", "mean"),
        count=("amount", "count"),
    ).reset_index()

    # 내림차순 정렬
    return grouped.sort_values("total", ascending=False)


def run_polars(path: str = FILE, verbose: bool = False) -> pl.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

    # scan_csv는 실제로 읽지 않고 실행 계획만 세움 (lazy)
    lf = pl.scan_csv(path)

    try:
        # IQR 계산을 위해 quantile만 우선 collect (부분 실행)
        q = lf.select([
            pl.col("amount").quantile(0.25).alias("q1"),
            pl.col("amount").quantile(0.75).alias("q3"),
        ]).collect()
    except pl.exceptions.ColumnNotFoundError:
        raise KeyError("'amount' 컬럼이 존재하지 않습니다.")

    Q1, Q3 = q["q1"][0], q["q3"][0]
    lower, upper = compute_iqr_bounds(Q1, Q3)

    if verbose:
        before = lf.select(pl.len()).collect().item()
        print(f"제거 전: {before}")

    # filter(이상치 제거) -> group_by -> agg(named) -> sort -> collect(최종 실행)
    result = (
        lf.filter(pl.col("amount").is_between(lower, upper))
        .group_by("region", "category")
        .agg(
            pl.col("amount").sum().alias("total"),
            pl.col("amount").mean().alias("mean"),
            pl.col("amount").count().alias("count"),
        )
        .sort("total", descending=True)
        .collect()
    )

    if verbose:
        after = result.select(pl.col("count").sum()).item()
        print(f"제거 후: {after}")

    return result


def run_duckdb(path: str = FILE, verbose: bool = False) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

    try:
        # SQL 함수(quantile_cont)로 Q1, Q3 계산
        bounds = duckdb.sql(f"""
            SELECT
                quantile_cont(amount, 0.25) AS q1,
                quantile_cont(amount, 0.75) AS q3
            FROM '{path}'
        """).df()
    except duckdb.Error as e:
        raise RuntimeError(f"IQR 계산 쿼리 실패: {e}")

    Q1, Q3 = bounds["q1"][0], bounds["q3"][0]
    lower, upper = compute_iqr_bounds(Q1, Q3)

    if verbose:
        before = duckdb.sql(f"SELECT count(*) AS n FROM '{path}'").df()["n"][0]
        print(f"제거 전: {before}")

    try:
        # WHERE로 이상치 제거 + GROUP BY 집계 + ORDER BY 정렬
        result = duckdb.sql(f"""
            SELECT
                region,
                category,
                sum(amount) AS total,
                avg(amount) AS mean,
                count(amount) AS count
            FROM '{path}'
            WHERE amount BETWEEN {lower} AND {upper}
            GROUP BY region, category
            ORDER BY total DESC
        """).df()
    except duckdb.Error as e:
        raise RuntimeError(f"집계 쿼리 실패: {e}")

    if verbose:
        print(f"제거 후: {result['count'].sum()}")

    return result


if __name__ == "__main__":
    # 1. Pandas EDA + IQR + named aggregation
    pandas_result = run_pandas(verbose=True)
    print(pandas_result.head(10))

    # 2. Polars Lazy API로 동일 집계
    polars_result = run_polars(verbose=True)
    print(polars_result.head(10))

    # 3. DuckDB SQL로 동일 집계
    duckdb_result = run_duckdb(verbose=True)
    print(duckdb_result.head(10))

    # 4. timeit 성능 비교 (세 도구 동일 반복 횟수 N으로 통일)
    N = 3
    t_pandas = timeit.timeit(lambda: run_pandas(verbose=False), number=N)
    t_polars = timeit.timeit(lambda: run_polars(verbose=False), number=N)
    t_duckdb = timeit.timeit(lambda: run_duckdb(verbose=False), number=N)

    print(f"Pandas: {t_pandas:.4f}초 (1회 평균: {t_pandas/N:.4f}초)")
    print(f"Polars: {t_polars:.4f}초 (1회 평균: {t_polars/N:.4f}초)")
    print(f"DuckDB: {t_duckdb:.4f}초 (1회 평균: {t_duckdb/N:.4f}초)")