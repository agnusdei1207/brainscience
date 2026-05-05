+++
weight = 103
title = "회귀 분석 (Regression Analysis)"
date = "2024-03-20"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 회귀 분석 (Regression Analysis)은(는) 대규모 데이터에서 패턴·예측·의사결정 근거를 추출하기 위한 분석 기법 또는 모델이다.
> **비유**: 광산에서 캐낸 원석을 분류·정제해 의미 있는 보석으로 가공하는 과정과 같다.

📝 모범 답안

## 1. 개요 및 필요성

- **통계학의 근간:** '평균으로의 회귀(Regression to the Mean)' 현상에서 유래하였으며, 오늘날 머신러닝의 지도 학습 중 '수치 예측' 영역의 핵심 기술임.
- **비즈니스 가치:** 매출액 예측, 부동산 가격 산정, 고객 평생 가치(LTV) 추정 등 연속형 데이터를 다루는 모든 의사결정 모델링에 필수적임.

---

## 2. 구성요소

- **수학적 기본 모델:** $Y = \beta_0 + \beta_1 X_1 + \dots + \beta_n X_n + \epsilon$
- **Bilingual ASCII Diagram:**
```text
[Linear Regression Concepts / 선형 회귀 핵심 개념]

    Dependent (Y)
      ^
      |           *  Actual Data Point (y)
      |          /
      |         |  Residual/Error (e = y - y_hat)
      |         v
      |       /------* Regression Line (y_hat = b0 + b1x)
      |     /   *
      |   /  *
      | /_________________ Independent (X)

[Key Assumptions / 핵심 가정]
1. Linearity (선형성): X와 Y는 직선 관계
2. Independence (독립성): 잔차 간의 상관관계 없음
3. Homoscedasticity (등분산성): 잔차의 분산이 일정
4. Normality (정규성): 잔차 항은 정규 분포를 따름
```
- **주요 유형:** 
  - **단순 회귀:** 독립변수 1개.
  - **다중 회귀:** 독립변수 2개 이상 (다중 공선성 주의).
  - **다항 회귀:** 변수 간 관계가 곡선일 때 차수를 높임.

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 전처리, 모델 가정, 평가 지표, 해석 가능성을 함께 검토해야 한다.

동작 순서:
| 비교 항목 (Criteria) | 선형 회귀 (Linear) | 라쏘 (Lasso / L1) | 릿지 (Ridge / L2) |
| :--- | :--- | :--- | :--- |
| **목적 (Goal)** | 오차 최소화 | 변수 선택 + 과적합 방지 | 과적합 방지 (계수 축소) |
| **페널티 (Penalty)** | 없음 | 계수의 절대값 합 추가 | 계수의 제곱합 추가 |
| **특징 (Feature)** | 해석이 쉬움 | 중요하지 않은 변수 계수 0화 | 모든 변수를 유지하며 가중치 감소 |
| **모델 복잡도** | 높음 | 낮음 (Sparse) | 중간 |
| **비유 (Analogy)** | 있는 그대로의 직선 | 깐깐한 거름망 | 부드러운 압축 |

---

## 4. 비교 및 연결

- **전략적 전처리:** 회귀 분석 전 **다중 공선성(Multicollinearity)** 확인이 필수적임. VIF 지수가 10 이상인 변수는 제거하거나 PCA로 차원을 축소해야 모델의 신뢰성을 확보함.
- **성능 지표:** 단순 정확도보다는 **결정 계수($R^2$)**를 통해 모델의 설명력을 확인하고, MSE/RMSE를 통해 오차의 크기를 평가함.
- **데이터 엔지니어링 연계:** 대규모 빅데이터 환경에서는 Spark의 MLlib LinearRegression을 사용하여 분산 환경에서의 연산 가속을 꾀함.

---

## 5. 실무 적용 및 판단

- **예측 가능성 증대:** 불확실한 미래 수치를 정교한 수식 기반으로 예측하여 비즈니스 리스크를 낮춤.
- **AI의 기초:** 복잡한 신경망(Deep Learning)도 결국 수많은 로지스틱 회귀와 선형 회귀 층의 결합체이므로, 회귀 분석에 대한 깊은 이해는 AI 전문가의 기본 소양임.
- **표준 확립:** 설명 가능한 AI(XAI) 트렌드에서 회귀 계수는 모델의 판단 근거를 제시하는 강력한 표준 지표로 활용됨.

---

## 6. 기대효과 및 결론

회귀 분석 (Regression Analysis)은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 분석 기법의 실무 가치는 모델의 화려함보다 데이터 가정과 해석 책임을 얼마나 지키느냐에서 나온다.

---

## 7. 발전 흐름도

```text
[상위 개념: Predictive Analytics, Supervised Learning]
    │
    ▼
[하위 개념: OLS, Regularization (L1, L2), Logistic Regression]
    │
    ▼
[연관 기술: Pearson Correlation, VIF, R-Squared, Gradient Descent]
```

이 흐름도는 상위 개념: Predictive Analytics, Supervised Learning에서 출발해 연관 기술: Pearson Correlation, VIF, R-Squared, Gradient Descent까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

- **상위 개념:** Predictive Analytics, Supervised Learning
- **하위 개념:** OLS, Regularization (L1, L2), Logistic Regression
- **연관 기술:** Pearson Correlation, VIF, R-Squared, Gradient Descent
