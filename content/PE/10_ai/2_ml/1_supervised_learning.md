+++
title = "지도 학습 (Supervised Learning)"
date = "2026-03-05"
[extra]
categories = "studynotes-ai"
+++

# 지도 학습 (Supervised Learning)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지도 학습은 입력(X)과 정답(y) 쌍으로 구성된 레이블된 데이터를 사용하여 입력을 출력으로 매핑하는 함수 f: X → Y를 학습하는 머신러닝 패러다임으로, 회귀(Regression)와 분류(Classification)가 핵심 문제 유형이다.
> 2. **가치**: 스팸 필터링, 이미지 분류, 질병 진단, 주가 예측, 음성 인식 등 광범위한 실무 문제에 적용 가능하며, 명확한 평가 지표(정확도, MSE 등)로 성능 측정이 용이하다.
> 3. **융합**: 신경망, 앙상블, SVM, 결정 트리 등 다양한 알고리즘이 포함되며, 전이 학습, 준지도 학습, 자가 지도 학습으로 확장되어 현대 AI의 주류 방식이다.

---

## I. 개요 (Context & Background)

### 개념 정의

지도 학습(Supervised Learning)은 **입력 데이터(특성, Feature)와 이에 대응하는 정답(레이블, Label/Target) 쌍으로 구성된 훈련 데이터를 사용하여, 새로운 입력에 대해 정확한 출력을 예측할 수 있는 모델을 학습하는 머신러닝 접근법**이다.

**핵심 요소**:
- **훈련 데이터**: D = {(x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)}
- **입력 공간**: X (특성 벡터)
- **출력 공간**: Y (연속값 또는 이산값)
- **가설 공간**: H (가능한 모델 함수 집합)
- **학습 목표**: h ∈ H를 찾아 h(x) ≈ y

### 💡 비유: "선생님이 정답을 알려주며 가르치는 학습"

지도 학습을 **"선생님이 문제와 정답을 함께 보여주는 수업"**에 비유할 수 있다.

**상황**: 수학 문제집을 풀 때

**지도 학습**:
```
문제 1: 2 + 3 = ?    정답: 5
문제 2: 4 + 1 = ?    정답: 5
문제 3: 7 + 2 = ?    정답: 9
...
학생: "아, 두 수를 더하는 거구나!"

시험: 5 + 6 = ?    예측: 11 ✓
```

**비지도 학습 (비교)**:
```
문제 1: 2, 3, 5
문제 2: 4, 1, 5
문제 3: 7, 2, 9
...
학생: "음, 어떤 규칙이 있는 것 같은데... 숫자들을 그룹으로 나눠볼까?"
```

### 등장 배경 및 발전 과정

#### 1. 문제 유형

| 유형 | 출력 Y | 예시 | 알고리즘 |
|------|--------|------|----------|
| **이진 분류** | {0, 1} | 스팸 여부 | 로지스틱 회귀, SVM |
| **다중 분류** | {1, 2, ..., K} | 숫자 인식 | Softmax, NN |
| **회귀** | ℝ (연속) | 집값 예측 | 선형 회귀, RF |
| **다중 레이블** | {0,1}^K | 태그 분류 | Binary Relevance |
| **서열 예측** | 시퀀스 | 번역 | RNN, Transformer |

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 구성 요소 | 역할 | 상세 |
|-----------|------|------|
| **특성(Feature)** | 입력 변수 | x = (x₁, x₂, ..., xₙ) |
| **레이블(Label)** | 정답 | y (분류: 범주, 회귀: 실수) |
| **모델(Model)** | 매핑 함수 | ŷ = f(x; θ) |
| **손실 함수(Loss)** | 오차 측정 | L(y, ŷ) |
| **옵티마이저** | 파라미터 갱신 | θ ← θ - η∇L |

### 회귀 vs 분류

```
회귀 (Regression):
┌────────────────────────────────────────────────────────────────────┐
│  목표: 연속형 출력 예측                                              │
│  손실: MSE = (1/n) Σ(yᵢ - ŷᵢ)²                                    │
│  예시: 주가 예측, 온도 예측, 매출 예측                               │
│                                                                    │
│  y                                                                │
│  ↑     *                                                          │
│  │   *    *    *                                                  │
│  │ *         *   *   ← 회귀선                                     │
│  │       *       *                                                │
│  │   *          *                                                 │
│  └──────────────────────→ x                                       │
└────────────────────────────────────────────────────────────────────┘

분류 (Classification):
┌────────────────────────────────────────────────────────────────────┐
│  목표: 이산형 클래스 예측                                           │
│  손실: Cross-Entropy = -Σ yᵢ log(ŷᵢ)                              │
│  예시: 스팸 탐지, 질병 진단, 필기체 인식                            │
│                                                                    │
│       │  ○ ○ ○                                                    │
│       │ ○ ○ ○○ ← 클래스 1                                          │
│  x₂   │ ──────────── ← 결정 경계                                  │
│       │ ● ● ● ● ← 클래스 2                                         │
│       │  ●  ● ●                                                    │
│       └─────────────────→ x₁                                       │
└────────────────────────────────────────────────────────────────────┘
```

### 핵심 알고리즘 코드

```python
import numpy as np
from typing import List, Tuple, Optional

class LogisticRegression:
    """로지스틱 회귀 (이진 분류)"""

    def __init__(self, learning_rate: float = 0.01, n_iterations: int = 1000):
        self.lr = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None

    def sigmoid(self, z: np.ndarray) -> np.ndarray:
        """시그모이드 활성화 함수"""
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def fit(self, X: np.ndarray, y: np.ndarray):
        """모델 학습"""
        n_samples, n_features = X.shape

        # 파라미터 초기화
        self.weights = np.zeros(n_features)
        self.bias = 0

        # 경사 하강법
        for i in range(self.n_iterations):
            # 순전파
            linear_pred = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(linear_pred)

            # 역전파 (기울기 계산)
            dw = (1 / n_samples) * np.dot(X.T, (predictions - y))
            db = (1 / n_samples) * np.sum(predictions - y)

            # 파라미터 갱신
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """확률 예측"""
        linear_pred = np.dot(X, self.weights) + self.bias
        return self.sigmoid(linear_pred)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """클래스 예측"""
        return (self.predict_proba(X) >= 0.5).astype(int)


class LinearRegression:
    """선형 회귀 (연속값 예측)"""

    def __init__(self, learning_rate: float = 0.01, n_iterations: int = 1000):
        self.lr = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        """모델 학습"""
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iterations):
            y_pred = np.dot(X, self.weights) + self.bias

            # MSE 기울기
            dw = (2 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (2 / n_samples) * np.sum(y_pred - y)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X: np.ndarray) -> np.ndarray:
        """예측"""
        return np.dot(X, self.weights) + self.bias

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """R² 점수"""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot)
```

---

## III. 융합 비교 및 다각도 분석

### 분류 알고리즘 비교

| 알고리즘 | 장점 | 단점 | 용도 |
|---------|------|------|------|
| **로지스틱 회귀** | 빠름, 해석 가능 | 선형만 | 기준 모델 |
| **SVM** | 고차원 우수 | 스케일링 필요 | 텍스트 |
| **결정 트리** | 해석 용이 | 과적합 | 규칙 추출 |
| **Random Forest** | 강건함 | 느림 | 범용 |
| **XGBoost** | 성능 최상 | 튜닝 복잡 | 대회 |

### 회귀 알고리즘 비교

| 알고리즘 | 특징 | 용도 |
|---------|------|------|
| **선형 회귀** | 기본 | 기준 |
| **Ridge/Lasso** | 정규화 | 과적합 방지 |
| **Polynomial** | 비선형 | 곡선 |
| **Random Forest** | 비선형, 앙상블 | 범용 |
| **Gradient Boosting** | 최고 성능 | 정밀 예측 |

---

## IV. 실무 적용 및 기술사적 판단

### 실무 시나리오

#### 시나리오 1: 이탈 고객 예측 (분류)

**문제**: 이탈할 고객 예측

**전략**:
1. **특성**: 이용 패턴, 빈도, 금액
2. **모델**: XGBoost + SMOTE
3. **평가**: 재현율 중심

#### 시나리오 2: 수요 예측 (회귀)

**문제**: 일일 판매량 예측

**전략**:
1. **특성**: 날짜, 요일, 프로모션
2. **모델**: Prophet 또는 LSTM
3. **평가**: MAPE

### 안티패턴

1. **데이터 누수**: 타겟 정보 포함
2. **과적합**: 훈련 데이터 암기
3. **불균형 무시**: 클래스 비율 차이

---

## V. 기대효과 및 결론

### 평가 지표

| 유형 | 지표 | 수식 |
|------|------|------|
| 분류 | 정확도 | (TP+TN)/(TP+FP+FN+TN) |
| 분류 | F1 | 2×P×R/(P+R) |
| 회귀 | MSE | Σ(y-ŷ)²/n |
| 회귀 | MAE | Σ|y-ŷ|/n |

---

## 👶 어린이를 위한 3줄 비유

**1. 지도 학습은 선생님이 정답을 알려주는 수업이에요.** "이 사진은 고양이야", "이 사진은 강아지야"라고 계속 보여주면, 컴퓨터도 "아, 뾰족한 귀는 고양이구나!" 하고 배워요.

**2. 두 가지 문제를 풀 수 있어요.** "이건 뭐야?" 하고 카테고리를 맞추는 것(분류)과 "이거 얼마야?" 하고 숫자를 예측하는 것(회귀)이에요.

**3. 정답이 있으니 얼마나 잘했는지 바로 알 수 있어요.** "정답은 고양이인데 넌 강아지라고 했어? 틀렸어!" 하고 바로 교정받을 수 있거든요.
