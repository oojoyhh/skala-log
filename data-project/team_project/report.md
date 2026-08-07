# Adult Income 데이터 분석 보고서

- 원본 데이터: 32,561행
- 중복 행 제거: 24건
- 결측치 행 제거 후 최종 분석 데이터: 30,139행

## 결측치 현황

| index | missing_count | missing_pct |
|---|---|---|
| age | 0 | 0.0 |
| workclass | 1836 | 5.64 |
| fnlwgt | 0 | 0.0 |
| education | 0 | 0.0 |
| education-num | 0 | 0.0 |
| marital-status | 0 | 0.0 |
| occupation | 1843 | 5.66 |
| relationship | 0 | 0.0 |
| race | 0 | 0.0 |
| sex | 0 | 0.0 |
| capital-gain | 0 | 0.0 |
| capital-loss | 0 | 0.0 |
| hours-per-week | 0 | 0.0 |
| native-country | 582 | 1.79 |
| income | 0 | 0.0 |

## 이상치(IQR) 요약

| column | Q1 | Q3 | IQR | lower_bound | upper_bound | outlier_count | outlier_pct |
|---|---|---|---|---|---|---|---|
| age | 28.0 | 47.0 | 19.0 | -0.5 | 75.5 | 168 | 0.56 |
| fnlwgt | 117627.5 | 237604.5 | 119977.0 | -62338.0 | 417570.0 | 904 | 3.0 |
| education-num | 9.0 | 13.0 | 4.0 | 3.0 | 19.0 | 193 | 0.64 |
| capital-gain | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2538 | 8.42 |
| capital-loss | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1427 | 4.73 |
| hours-per-week | 40.0 | 45.0 | 5.0 | 32.5 | 52.5 | 7947 | 26.37 |

## 상관계수 행렬

| index | age | fnlwgt | education-num | capital-gain | capital-loss | hours-per-week |
|---|---|---|---|---|---|---|
| age | 1.0 | -0.076 | 0.043 | 0.08 | 0.06 | 0.101 |
| fnlwgt | -0.076 | 1.0 | -0.045 | 0.0 | -0.01 | -0.023 |
| education-num | 0.043 | -0.045 | 1.0 | 0.124 | 0.08 | 0.153 |
| capital-gain | 0.08 | 0.0 | 0.124 | 1.0 | -0.032 | 0.08 |
| capital-loss | 0.06 | -0.01 | 0.08 | -0.032 | 1.0 | 0.052 |
| hours-per-week | 0.101 | -0.023 | 0.153 | 0.08 | 0.052 | 1.0 |

## t-test 결과 (age, income 그룹 비교)

- `<=50K` 평균 age: 36.61 (n=22,633)
- `>50K` 평균 age: 43.96 (n=7,506)
- t-statistic: -49.4772
- p-value: < 1e-300 (부동소수점 표현 한계로 0에 수렴)
- Cohen's d: 0.577 (중간)
- 해석: p-value < 0.05 → 두 소득 그룹의 평균 나이 차이는 통계적으로 유의합니다. 다만 표본이 30,139건으로 매우 커서 작은 차이도 유의하게 나올 수 있으므로, 효과크기(Cohen's d=0.577, 중간 수준)와 실제 평균 차이(7.35세)를 함께 고려해야 합니다.

## ML Pipeline 평가 결과

- Accuracy: 0.8451
- F1-score (>50K): 0.6589

```
              precision    recall  f1-score   support

       <=50K       0.87      0.93      0.90      4527
        >50K       0.73      0.60      0.66      1501

    accuracy                           0.85      6028
   macro avg       0.80      0.76      0.78      6028
weighted avg       0.84      0.85      0.84      6028

```

- 저장된 모델 파일: `income_pipeline.joblib`
