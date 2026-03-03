+++
title = "회귀 분석 (Regression Analysis)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 회귀 분석 (Regression Analysis)

## 핵심 인사이트 (3줄 요약)
> **변수 간 관계를 수학적 모델로 표현하고 예측**. 독립변수로 종속변수 추정. 최소제곱법(OLS)이 핵심.

---

### Ⅰ. 개요

**개념**: 회귀 분석(Regression Analysis)은 **하나 이상의 독립변수(X)와 종속변수(Y) 사이의 관계를 수학적 모델로 표현하고, 이를 통해 Y값을 예측하는 통계 기법**이다.

> 💡 **비유**: "키로 몸무게 추측하기" - 키가 크면 보통 몸무게도 많이 나가요. 이런 관계를 수학 공식으로 만들면, 키만 알고도 몸무게를 예측할 수 있어요.

**등장 배경** (3가지 이상 기술):

1. **기존 문제점**: 변수 간의 복잡한 관계를 인간의 직관만으로 파악하기 어려움. 여러 요인이 동시에 결과에 영향을 미치는 경우 분석 불가
2. **기술적 필요성**: 데이터에서 패턴을 추출하여 미래를 예측하고, 인과관계를 통계적으로 검증하는 도구 필요
3. **산업적 요구**: 매출 예측, 주가 분석, 의료 진단, 날씨 예보 등 다양한 분야에서 정량적 예측 모델 필요

**핵심 목적**: 변수 간의 관계를 모델링하여 설명하고, 새로운 입력에 대한 출력을 예측하는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (4개 이상):

| 구성 요소 | 영어 | 역할/기능 | 비유 |
|----------|------|----------|------|
| 종속변수 Y | Dependent Variable | 예측하려는 결과 | 몸무게 |
| 독립변수 X | Independent Variable | 예측에 사용되는 입력 | 키, 나이, 성별 |
| 회귀계수 β | Coefficient | X가 Y에 미치는 영향력 | 키 1cm당 몸무게 증가량 |
| 오차항 ε | Error Term | 모델이 설명 못 하는 변동 | 개인차 |
| 결정계수 R² | R-squared | 모델의 설명력 | 예측 정확도 지표 |

**회귀 분석 분류 구조**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    회귀 분석 분류                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 단순 회귀 (Simple Linear Regression):                       │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Y = β₀ + β₁X + ε                                      │    │
│  │  • 독립변수 1개                                         │    │
│  │  • 직선 관계 모델링                                     │    │
│  │  예: 광고비 → 매출                                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  📈 다중 회귀 (Multiple Linear Regression):                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Y = β₀ + β₁X₁ + β₂X₂ + ... + βₖXₖ + ε                │    │
│  │  • 독립변수 여러 개                                     │    │
│  │  • 여러 요인의 영향 동시 분석                            │    │
│  │  예: 면적, 방수, 위치 → 집값                            │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  🔀 다항 회귀 (Polynomial Regression):                          │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Y = β₀ + β₁X + β₂X² + β₃X³ + ... + ε                 │    │
│  │  • 곡선 관계 모델링                                     │    │
│  │  • 비선형 패턴 포착                                     │    │
│  │  예: 온도 → 작물 수확량 (최적점 존재)                   │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  📋 로지스틱 회귀 (Logistic Regression):                        │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  P(Y=1) = 1 / (1 + e^-(β₀+β₁X₁+...+βₖXₖ))             │    │
│  │  • 종속변수가 범주형 (0/1)                              │    │
│  │  • 확률 예측 → 분류                                     │    │
│  │  예: 소득, 나이 → 대출 연체 확률                        │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**최소제곱법(OLS) 원리**:

```
┌─────────────────────────────────────────────────────────────────┐
│              최소제곱법 (Ordinary Least Squares)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   목표: 잔차 제곱합(SSE) 최소화                                  │
│                                                                 │
│   min Σ(yᵢ - ŷᵢ)² = min Σ(yᵢ - (β₀ + β₁xᵢ))²                  │
│                                                                 │
│   ┌─────────────────────────────────────────────────────┐      │
│   │         Y                                           │      │
│   │         ↑                                           │      │
│   │    ●    │     ↘ 회귀선                               │      │
│   │  ●  ●   │      \                                     │      │
│   │    ●    │       \  잔차(residual) = |yᵢ - ŷᵢ|        │      │
│   │  ●   ●  │    ●  │ ↗                                   │      │
│   │ ●    ●  │  ●    │                                     │      │
│   │─────────┼──────────────────→ X                       │      │
│   └─────────────────────────────────────────────────────┘      │
│                                                                 │
│   정규방정식 해:                                                │
│   β₁ = Σ(xᵢ-x̄)(yᵢ-ȳ) / Σ(xᵢ-x̄)²                              │
│   β₀ = ȳ - β₁x̄                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**회귀 진단 지표**:

| 지표 | 공식/의미 | 좋은 값 | 해석 |
|-----|----------|---------|------|
| R² (결정계수) | 1 - SS_res/SS_tot | 1에 가까울수록 | 모델이 설명하는 변동 비율 |
| 조정 R² | 1 - (1-R²)(n-1)/(n-k-1) | 높을수록 | 변수 수 보정한 R² |
| RMSE | √(Σ(y-ŷ)²/n) | 0에 가까울수록 | 예측 오차의 표준편차 |
| MAE | Σ\|y-ŷ\|/n | 0에 가까울수록 | 평균 절대 오차 |
| F-통계량 | (SS_reg/k)/(SS_res/(n-k-1)) | p < 0.05 | 모형 전체 유의성 |
| t-통계량 | βᵢ/SE(βᵢ) | p < 0.05 | 개별 계수 유의성 |

**회귀 분석 가정 (LINE)**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    회귀 분석 4가지 가정                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  L - Linearity (선형성):                                        │
│      X와 Y 사이의 관계가 선형이어야 함                           │
│      검증: 산점도, 잔차 vs 적합값 도표                           │
│                                                                 │
│  I - Independence (독립성):                                     │
│      오차들이 서로 독립이어야 함                                 │
│      검증: Durbin-Watson 검정 (1.5~2.5 양호)                    │
│                                                                 │
│  N - Normality (정규성):                                        │
│      오차가 정규분포를 따라야 함                                 │
│      검증: Q-Q plot, Shapiro-Wilk 검정                          │
│                                                                 │
│  E - Equal Variance (등분산성):                                 │
│      모든 X 수준에서 오차 분산이 일정해야 함                     │
│      검증: Breusch-Pagan 검정, White 검정                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**동작 원리** (단계별 상세 설명):

```
① 데이터수집 → ② 모형설정 → ③ 모수추정 → ④ 모형진단 → ⑤ 예측/해석
```

- **1단계**: 종속변수와 잠재적 독립변수들의 데이터를 수집. 이상치, 결측치 처리
- **2단계**: 이론적 근거로 변수 선택. 단순/다중/다항/로지스틱 등 모형 결정
- **3단계**: 최소제곱법으로 회귀계수(β) 추정. 신뢰구간, p-value 계산
- **4단계**: R², 잔차분석, 다중공선성(VIF) 등으로 모형 적절성 평가
- **5단계**: 새로운 X값에 대한 Y 예측. 계수 해석으로 인사이트 도출

**코드 예시** (Python):

```python
from typing import List, Tuple, Optional
import math

class LinearRegression:
    """단순 및 다중 선형 회귀 분석"""

    def __init__(self):
        self.coefficients: List[float] = []
        self.intercept: float = 0.0
        self.r_squared: float = 0.0
        self.adj_r_squared: float = 0.0
        self.rmse: float = 0.0
        self.n: int = 0
        self.k: int = 0

    def fit(self, X: List[List[float]], y: List[float]) -> 'LinearRegression':
        """
        최소제곱법으로 회귀계수 추정
        X: 독립변수 행렬 (n x k)
        y: 종속변수 벡터 (n x 1)
        """
        self.n = len(y)
        self.k = len(X[0]) if X else 0

        # 절편을 위해 X에 1 추가
        X_with_intercept = [[1] + row for row in X]

        # 정규방정식: β = (X'X)^(-1) X'y
        # 행렬 연산 구현
        Xt = self._transpose(X_with_intercept)
        XtX = self._matrix_multiply(Xt, X_with_intercept)
        XtX_inv = self._matrix_inverse(XtX)
        Xty = self._matrix_vector_multiply(Xt, y)

        beta = self._matrix_vector_multiply(XtX_inv, Xty)

        self.intercept = beta[0]
        self.coefficients = beta[1:]

        # 성능 지표 계산
        self._calculate_metrics(X, y)

        return self

    def predict(self, X: List[List[float]]) -> List[float]:
        """예측값 계산"""
        predictions = []
        for row in X:
            pred = self.intercept
            for i, coef in enumerate(self.coefficients):
                pred += coef * row[i]
            predictions.append(pred)
        return predictions

    def _calculate_metrics(self, X: List[List[float]], y: List[float]) -> None:
        """R², RMSE 등 성능 지표 계산"""
        y_pred = self.predict(X)
        y_mean = sum(y) / len(y)

        # SST (Total Sum of Squares)
        sst = sum((yi - y_mean) ** 2 for yi in y)

        # SSE (Sum of Squared Errors / Residual Sum of Squares)
        sse = sum((yi - y_pred_i) ** 2 for yi, y_pred_i in zip(y, y_pred))

        # R²
        self.r_squared = 1 - (sse / sst) if sst != 0 else 0

        # Adjusted R²
        n, k = self.n, self.k
        self.adj_r_squared = 1 - (1 - self.r_squared) * (n - 1) / (n - k - 1) if n > k + 1 else 0

        # RMSE
        self.rmse = math.sqrt(sse / n)

    def summary(self) -> str:
        """모델 요약 정보"""
        return (f"Linear Regression Summary\n"
                f"{'='*40}\n"
                f"Intercept (β₀): {self.intercept:.4f}\n"
                f"Coefficients: {[round(c, 4) for c in self.coefficients]}\n"
                f"R-squared: {self.r_squared:.4f}\n"
                f"Adjusted R-squared: {self.adj_r_squared:.4f}\n"
                f"RMSE: {self.rmse:.4f}\n"
                f"Observations: {self.n}")


class LogisticRegression:
    """로지스틱 회귀 (이진 분류)"""

    def __init__(self, learning_rate: float = 0.01, max_iter: int = 1000):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.coefficients: List[float] = []
        self.intercept: float = 0.0

    @staticmethod
    def _sigmoid(z: float) -> float:
        """시그모이드 함수: 0~1 사이 확률로 변환"""
        if z >= 0:
            return 1 / (1 + math.exp(-z))
        else:
            exp_z = math.exp(z)
            return exp_z / (1 + exp_z)

    def fit(self, X: List[List[float]], y: List[int]) -> 'LogisticRegression':
        """경사하강법으로 계수 추정"""
        n = len(y)
        k = len(X[0]) if X else 0

        # 계수 초기화
        self.coefficients = [0.0] * k
        self.intercept = 0.0

        for _ in range(self.max_iter):
            # 예측값 계산
            y_pred = []
            for row in X:
                z = self.intercept + sum(c * x for c, x in zip(self.coefficients, row))
                y_pred.append(self._sigmoid(z))

            # 그래디언트 계산
            d_intercept = sum(pred - actual for pred, actual in zip(y_pred, y)) / n
            d_coefficients = []
            for j in range(k):
                d_j = sum((pred - actual) * row[j]
                         for pred, actual, row in zip(y_pred, y, X)) / n
                d_coefficients.append(d_j)

            # 계수 업데이트
            self.intercept -= self.learning_rate * d_intercept
            for j in range(k):
                self.coefficients[j] -= self.learning_rate * d_coefficients[j]

        return self

    def predict_proba(self, X: List[List[float]]) -> List[float]:
        """양성 클래스 확률 예측"""
        probabilities = []
        for row in X:
            z = self.intercept + sum(c * x for c, x in zip(self.coefficients, row))
            probabilities.append(self._sigmoid(z))
        return probabilities

    def predict(self, X: List[List[float]], threshold: float = 0.5) -> List[int]:
        """클래스 예측 (0 또는 1)"""
        return [1 if p >= threshold else 0 for p in self.predict_proba(X)]


class PolynomialRegression:
    """다항 회귀"""

    def __init__(self, degree: int = 2):
        self.degree = degree
        self.linear_model = LinearRegression()

    def _transform(self, X: List[List[float]]) -> List[List[float]]:
        """다항 특성 생성"""
        if not X or not X[0]:
            return X

        transformed = []
        for row in X:
            new_row = list(row)  # 원본 특성
            # 다항식 특성 추가 (x², x³, ...)
            for val in row:
                for d in range(2, self.degree + 1):
                    new_row.append(val ** d)
            transformed.append(new_row)
        return transformed

    def fit(self, X: List[List[float]], y: List[float]) -> 'PolynomialRegression':
        X_poly = self._transform(X)
        self.linear_model.fit(X_poly, y)
        return self

    def predict(self, X: List[List[float]]) -> List[float]:
        X_poly = self._transform(X)
        return self.linear_model.predict(X_poly)

    @property
    def r_squared(self) -> float:
        return self.linear_model.r_squared


def calculate_vif(X: List[List[float]]) -> List[float]:
    """
    분산팽창요인(VIF) 계산
    다중공선성 진단: VIF > 10이면 심각한 다중공선성
    """
    k = len(X[0]) if X else 0
    vif_values = []

    for j in range(k):
        # j번째 변수를 종속변수로, 나머지를 독립변수로 회귀
        X_j = [[row[i] for i in range(k) if i != j] for row in X]
        y_j = [row[j] for row in X]

        model = LinearRegression()
        model.fit(X_j, y_j)

        # VIF = 1 / (1 - R²)
        r2 = model.r_squared
        vif = 1 / (1 - r2) if r2 < 1 else float('inf')
        vif_values.append(vif)

    return vif_values


def stepwise_selection(X: List[List[float]], y: List[float],
                       threshold_in: float = 0.05,
                       threshold_out: float = 0.10) -> List[int]:
    """
    단계적 변수 선택 (전진 + 후진)
    """
    n_features = len(X[0]) if X else 0
    selected = []

    while True:
        changed = False

        # 전진 선택
        remaining = [i for i in range(n_features) if i not in selected]
        if remaining:
            best_pval = 1
            best_feature = None

            for feature in remaining:
                current_features = selected + [feature]
                X_subset = [[row[i] for i in current_features] for row in X]
                model = LinearRegression().fit(X_subset, y)

                # 간단한 p-value 근사 (t-검정)
                if model.r_squared > 0:
                    pval = 1 - model.r_squared  # 근사
                    if pval < best_pval and pval < threshold_in:
                        best_pval = pval
                        best_feature = feature

            if best_feature is not None:
                selected.append(best_feature)
                changed = True

        # 후진 제거
        if len(selected) > 1:
            worst_pval = 0
            worst_feature = None

            for feature in selected:
                current_features = [f for f in selected if f != feature]
                X_subset = [[row[i] for i in current_features] for row in X]
                model = LinearRegression().fit(X_subset, y)

                pval = 1 - model.r_squared
                if pval > worst_pval and pval > threshold_out:
                    worst_pval = pval
                    worst_feature = feature

            if worst_feature is not None:
                selected.remove(worst_feature)
                changed = True

        if not changed:
            break

    return selected


# === 행렬 연산 헬퍼 함수들 ===

def _transpose(matrix: List[List[float]]) -> List[List[float]]:
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

def _matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    n, m, p = len(A), len(B), len(B[0])
    result = [[0.0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            for k in range(m):
                result[i][j] += A[i][k] * B[k][j]
    return result

def _matrix_vector_multiply(A: List[List[float]], v: List[float]) -> List[float]:
    return [sum(a[i] * v[i] for i in range(len(v))) for a in A]

def _matrix_inverse(A: List[List[float]]) -> List[List[float]]:
    """가우스-조던 소거법으로 역행렬 계산"""
    n = len(A)
    # [A | I] 확장 행렬 생성
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]

    # 전진 소거
    for i in range(n):
        # 피벗 선택
        max_row = max(range(i, n), key=lambda r: abs(aug[r][i]))
        aug[i], aug[max_row] = aug[max_row], aug[i]

        if abs(aug[i][i]) < 1e-10:
            raise ValueError("행렬이 특이(singular)합니다")

        pivot = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = aug[k][i]
                for j in range(2 * n):
                    aug[k][j] -= factor * aug[i][j]

    # 역행렬 부분 추출
    return [row[n:] for row in aug]


# LinearRegression 클래스에 메서드로 추가
LinearRegression._transpose = staticmethod(_transpose)
LinearRegression._matrix_multiply = staticmethod(_matrix_multiply)
LinearRegression._matrix_vector_multiply = staticmethod(_matrix_vector_multiply)
LinearRegression._matrix_inverse = staticmethod(_matrix_inverse)


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("회귀 분석 예시")
    print("=" * 60)

    # 1. 단순 선형 회귀
    print("\n1. 단순 선형 회귀")
    print("문제: 광고비에 따른 매출 예측")
    X_simple = [[100], [150], [200], [250], [300], [350], [400], [450], [500]]
    y_sales = [120, 180, 230, 300, 350, 420, 490, 540, 620]

    model_simple = LinearRegression()
    model_simple.fit(X_simple, y_sales)
    print(model_simple.summary())

    # 예측
    new_ad = [[275], [600]]
    predictions = model_simple.predict(new_ad)
    print(f"\n광고비 275만 원 → 예상 매출: {predictions[0]:.1f}억 원")
    print(f"광고비 600만 원 → 예상 매출: {predictions[1]:.1f}억 원")

    # 2. 다중 선형 회귀
    print("\n2. 다중 선형 회귀")
    print("문제: 면적, 방 수로 집값 예측")
    X_multi = [
        [50, 2], [60, 2], [70, 3], [80, 3], [90, 4],
        [100, 4], [110, 5], [120, 5], [130, 6], [140, 6]
    ]
    y_price = [3.5, 4.2, 5.5, 6.3, 7.8, 8.5, 10.2, 11.0, 12.5, 13.8]

    model_multi = LinearRegression()
    model_multi.fit(X_multi, y_price)
    print(model_multi.summary())

    # VIF 확인
    vif = calculate_vif(X_multi)
    print(f"VIF: {[round(v, 2) for v in vif]}")

    # 3. 다항 회귀
    print("\n3. 다항 회귀")
    print("문제: 온도에 따른 아이스크림 판매량 (곡선 관계)")
    X_temp = [[10], [15], [20], [25], [30], [35], [40]]
    y_sales_ice = [50, 120, 200, 350, 500, 450, 300]  # 30도에서 최대

    model_poly = PolynomialRegression(degree=2)
    model_poly.fit(X_temp, y_sales_ice)
    print(f"R-squared: {model_poly.r_squared:.4f}")

    for temp, actual in zip(X_temp, y_sales_ice):
        pred = model_poly.predict([temp])[0]
        print(f"온도 {temp[0]}°C: 실제 {actual} → 예측 {pred:.0f}")

    # 4. 로지스틱 회귀
    print("\n4. 로지스틱 회귀")
    print("문제: 소득, 나이로 대출 연체 예측")
    X_loan = [
        [3000, 25], [4000, 30], [5000, 35], [6000, 40],
        [7000, 45], [2000, 22], [2500, 28], [8000, 50]
    ]
    y_default = [1, 0, 0, 0, 0, 1, 1, 0]  # 1=연체

    model_logistic = LogisticRegression(learning_rate=0.001, max_iter=5000)
    model_logistic.fit(X_loan, y_default)

    test_applicants = [[2500, 25], [7000, 40]]
    for income, age in test_applicants:
        prob = model_logistic.predict_proba([[income, age]])[0]
        pred = model_logistic.predict([[income, age]])[0]
        result = "연체 위험" if pred == 1 else "정상"
        print(f"소득 {income}만 원, 나이 {age}세 → 연체 확률: {prob:.1%} ({result})")
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석**:

| 장점 | 단점 |
|-----|------|
| 관계를 정량화하여 해석 용이 | 선형성 가정이 비현실적일 수 있음 |
| 예측과 설명 동시 가능 | 이상치(outlier)에 민감 |
| 계산 효율적, 확장성 좋음 | 다중공선성 문제 |
| 통계적 유의성 검증 가능 | 과적합(overfitting) 위험 |
| 다양한 변형 모델 존재 | 외삽(extrapolation) 신뢰도 낮음 |

**회귀 분석 기법 비교**:

| 비교 항목 | 선형 회귀 | 로지스틱 회귀 | 릿지/라쏘 | 다항 회귀 |
|---------|----------|-------------|----------|----------|
| 종속변수 | 연속형 | 이진 범주형 | 연속형 | 연속형 |
| 핵심 특성 | ★ 직선 관계 | S자 곡선 확률 | 정규화로 과적합 방지 | 곡선 관계 |
| 복잡도 | 낮음 | 낮음 | 중간 | 중간 |
| 해석력 | ★ 높음 | 높음 | 중간 | 중간 |
| 적합 분야 | 수치 예측 | 분류 문제 | 고차원 데이터 | 비선형 관계 |

> **★ 선택 기준**:
> - 종속변수가 연속형이고 선형 관계 → **선형 회귀**
> - 종속변수가 이진 분류 → **로지스틱 회귀**
> - 변수가 많고 과적합 우려 → **릿지/라쏘 회귀**
> - 비선형 관계 → **다항 회귀** 또는 비선형 모델

**정규화 기법 비교**:

| 기법 | 규제 방식 | 특징 | 적합 상황 |
|-----|----------|------|----------|
| 릿지(Ridge) | L2 (β²) | 변수 선택 안 함, 계수 축소 | 다중공선성 |
| 라쏘(Lasso) | L1 (\|β\|) | ★ 변수 선택 가능 | 희소 모델 필요 시 |
| 엘라스틱넷 | L1 + L2 | 두 장점 결합 | 변수 많고 상관관계 높음 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단** (3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| 매출 예측 | 과거 매출, 계절성, 마케팅 비용으로 다중 회귀 | 예측 정확도 85%+, 재고 비용 20% 감소 |
| 신용평가 | 소득, 부채, 연체이력으로 로지스틱 회귀 | 부실 채권 30% 감소, 심사 시간 90% 단축 |
| 의료 진단 | 증상, 검사값으로 질병 확률 예측 | 조기 진단율 40% 향상 |
| 부동산 가격 | 면적, 위치, 연식 등으로 가격 모델 | 시장가 대비 ±5% 이내 예측 |

**실제 도입 사례**:

- **사례 1: Zillow 집값 예측 (Zestimate)** - 다중 회귀 + 머신러닝으로 1억 호 이상 부동산 가치 추정. 2% 이내 오차율 달성. 하지만 시장 변동성으로 2021년 iBuying 사업 중단 (회귀 모델의 한계)
- **사례 2: 신용평가사 (FICO, KCB)** - 로지스틱 회귀 기반 신용점수 모델. 20+ 변수로 연체 확률 계산. 금융권 표준 모델로 자리잡음
- **사례 3: Google 광고 입찰** - 클릭 확률(CTR) 예측에 로지스틱 회귀 활용. 수십억 건 실시간 예측으로 매출 수십억 달러

**도입 시 고려사항** (4가지 관점):

1. **기술적**:
   - 선형성 가정 검증 (잔차 도표)
   - 다중공선성 확인 (VIF < 10)
   - 교차검증으로 일반화 성능 확인

2. **운영적**:
   - 모델 재학습 주기 (데이터 드리프트)
   - 실시간 vs 배치 예측
   - 변수 모니터링 (값 범위 변화)

3. **보안적**:
   - 학습 데이터 프라이버시
   - 모델 역추론 공격 방지
   - 변수 선택 시 차별적 요소 배제

4. **경제적**:
   - 단순 모델 vs 복잡 모델 트레이드오프
   - 해석 가능성 비용
   - 외부 데이터 구매 비용 vs 예측 가치

**주의사항 / 흔한 실수**:

- ❌ **상관관계 ≠ 인과관계**: 회귀는 관계를 보여줄 뿐, 인과를 증명하지 않음
- ❌ **외삽 위험**: 학습 데이터 범위 밖 예측은 신뢰도 낮음
- ❌ **다중공선성 무시**: 독립변수 간 높은 상관관계 시 계수 해석 왜곡
- ❌ **자동회귀 오류**: 시계열 데이터에서 시계열 특성 무시

**관련 개념 / 확장 학습**:

```
📌 회귀 분석 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│                   회귀 분석 연관 개념                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [상관분석] ←──→ [회귀분석] ←──→ [분산분석]                   │
│        ↓                ↓                ↓                       │
│   [공분산]        [잔차분석]      [가설검정]                     │
│        ↓                ↓                ↓                       │
│   [피어슨상관]  [정규성검정]    [신뢰구간]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 상관분석 | 선행 개념 | 두 변수 간 선형 관계의 강도 | `[상관분석](./correlation.md)` |
| 분산분석(ANOVA) | 확장 개념 | 집단 간 평균 차이 검정 | `[ANOVA](./anova.md)` |
| 정규화(Ridge/Lasso) | 확장 기법 | 과적합 방지를 위한 규제 | `[정규화](./regularization.md)` |
| 시계열 분석 | 특수 유형 | 시간 순서 데이터 회귀 | `[시계열](./time_series.md)` |
| 가설 검정 | 검증 도구 | 회귀계수 유의성 검증 | `[가설검정](./hypothesis_testing.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과**:

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 예측 정확도 | 수치형 결과값 예측 | R² > 0.8, RMSE 최소화 |
| 의사결정 속도 | 자동화된 예측 | 분석 시간 80% 단축 |
| 비용 절감 | 데이터 기반 계획 | 재고/마케팅 비용 20% 감소 |
| 리스크 관리 | 확률 기반 의사결정 | 의사결정 오류 40% 감소 |

**미래 전망** (3가지 관점):

1. **기술 발전 방향**: 정규화 기법 발전으로 고차원 데이터 처리. 베이지안 회귀로 불확실성 정량화. 딥러닝과 결합한 신경망 회귀
2. **시장 트렌드**: XAI(설명 가능한 AI) 요구로 해석 가능한 회귀 모델 재조명. AutoML로 자동 변수 선택, 하이퍼파라미터 튜닝
3. **후속 기술**: 일반화 가법 모델(GAM), 가우스 프로세스 회귀, 분위 회귀(Quantile Regression)

> **결론**: 회귀 분석은 예측 모델링의 기초이자 핵심 기법으로, 딥러닝 시대에도 해석 가능성과 효율성 때문에 여전히 중요하다. 특히 규제 산업(금융, 의료)에서는 복잡한 블랙박스 모델보다 회귀 모델이 선호된다. 정규화 기법과 결합하여 고차원 데이터에서도 강력한 성능을 발휘한다.

> **※ 참고 표준**: ISO 3534 (Statistics), NIST/SEMATECH e-Handbook of Statistical Methods, Elements of Statistical Learning (ESL)

---

## 어린이를 위한 종합 설명

**회귀 분석**은 마치 **키로 몸무게를 추측하는 게임**과 같아요.

첫 번째 문단: 친구들의 키와 몸무게를 적어봐요. 키가 150cm인 친구는 45kg, 160cm인 친구는 55kg, 170cm인 친구는 65kg... 이렇게 데이터를 모으면 어떤 규칙이 보여요! "키가 10cm 크면 몸무게는 10kg 정도 늘어나는 것 같아!" 이 규칙을 수학 공식으로 만들면 `몸무게 = 키 × 1 - 105` 같은 식이 돼요.

두 번째 문단: 이렇게 만든 공식으로 새로운 친구의 몸무게를 예측할 수 있어요. 키가 165cm인 친구가 왔어요. 공식에 대입하면 `165 × 1 - 105 = 60kg`! 실제로 물어보니 58kg라고 해요. 꽤 비슷하죠? 하지만 완전히 똑같지는 않아요. 운동을 많이 한 친구는 더 무겁고, 다이어트 중인 친구는 더 가벼우니까요. 이 차이가 "오차"예요.

세 번째 문단: 회귀 분석은 이 오차를 최소화하는 최고의 공식을 찾는 거예요. 여러 변수를 동시에 볼 수도 있어요. "키도 크고, 운동도 많이 하면?" 키, 운동량 두 가지를 함께 계산하면 훨씬 더 정확해져요! 이게 "다중 회귀"예요. 회귀 분석은 날씨 예보, 주가 예측, 매출 예측 등 우리 삶 곳곳에서 사용돼요!

---

## ✅ 작성 완료 체크리스트

- [x] 핵심 인사이트 3줄 요약
- [x] Ⅰ. 개요: 개념 + 비유 + 등장배경(3가지)
- [x] Ⅱ. 구성요소: 표(5개) + 다이어그램 + 단계별 동작 + Python 코드
- [x] Ⅲ. 비교: 장단점 표 + 대안 비교표 + 선택 기준
- [x] Ⅳ. 실무: 적용 시나리오(4개) + 실제 사례(3개) + 고려사항(4가지) + 주의사항(4개)
- [x] Ⅴ. 결론: 정량 효과 표 + 미래 전망(3가지) + 참고 표준
- [x] 관련 개념: 5개 나열 + 개념 맵 + 링크
- [x] 어린이를 위한 종합 설명 (3문단)
