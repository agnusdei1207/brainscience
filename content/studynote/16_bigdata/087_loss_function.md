+++
weight = 87
title = "87. 손실 함수 (Loss Function)"
description = "손실 함수의 정의와 역할, 분류/회귀별 주요 손실 함수, 커스텀 손실 함수 설계 원칙"
date = "2026-04-05"
[taxonomies]
tags = ["손실함수", "LossFunction", "손실", "비용함수", "Objective", "CrossEntropy", "MSE"]
categories = ["studynote-bigdata"]
+++

# 손실 함수 (Loss Function)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 손실 함수(Loss Function)는 모델의 예측값과 실제값 사이의 오차를定量적으로 측정하는 함수로, 모델의 학습 방향을 결정하는 핵심 신호이다.
> 2. **가치**: 어떤 손실 함수를 사용하느냐에 따라 모델이 학습하는 방향과 최종 성능이 크게 달라지므로, 문제 상황에 맞는 적절한 손실 함수의 선택이 필수적이다.
> 3. **융합**: 회귀에는 MSE, MAE 등이, 분류에는 Cross-Entropy, Hinge Loss 등이 사용되며, 특정 도메인에서는 커스텀 손실 함수를 설계하여 원하는 행동을 유도할 수 있다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

손실 함수(Loss Function), 또는 비용 함수(Cost Function)는 模型의性能を数量적으로評価하는尺度이다. 머신러닝의 목표는 훈련 데이터에서 손실 함수의 값을 최소화하는 파라미터를 찾는 것이다. 이는 곧"예측과 실제 사이의 오차를 최소화"하는 것과 동일하다.

손실 함수의 선택이 왜 중요한가? 그것은 模型이"무엇을" 그리고"어떻게" 학습하느냐에 直接적 영향을 미치기 때문이다. 예를 들어, 레스토랑 리뷰의 감성 분석에서"이 음식은 괜찮았어요"를 예측할 때, 단순 정확도(Accuracy)와 실제 비즈니스 가치(손실의 방향)가 다를 수 있다.

```text
[손실 함수의 역할]

예측: "이 영화 좋을까?"  →  모델 예측: 0.73 (긍정 확률 73%)
실제: "이 영화 정말 훌륭하다"  →  실제: 긍정 (1)

손실 함수 = measure(prediction, actual)
         = measure(0.73, 1)
         = ???

손실이 크면 → 모델이 많이 잘못 예측 → 더 많이 학습
손실이 작으면 → 모델이 잘 예측 → 적게 학습

목표: Σ 손실 함수를 최소화하는 파라미터 θ* 찾기
θ* = argmin_θ Σ L(yᵢ, f(xᵢ; θ))
```

손실 함수의 선택이 예측 결과에 미치는 영향을 시각화해보자.

```text
[손실 함수에 따른 모델 행동 차이]

동일한 데이터에 서로 다른 손실 함수 적용:

┌─────────────────────────────────────────────────────┐
│                                                     │
│  원래 데이터:                                      │
│        y                                            │
│        │                                    ● outliers
│        │                              ●            │
│        │                   ●                       │
│        │            ●                              │
│        │       ●                                   │
│        │  ●                                         │
│        └────────────────────────────────→ x        │
│                                                     │
└─────────────────────────────────────────────────────┘

[MSE (L2) 손실 사용 시]
→ outliers에 과도하게 민감 (오차를 제곱하므로)
→ outliers까지 맞추려다主线에서 크게 벗어남

[MAE (L1) 손실 사용 시]
→ outliers에 덜 민감
→主线 패턴에 더 집중
→より robust한 모델
```

> 📢 **섹션 요약 비유**: 손실 함수는犹如裁判での評価基準と類似している.裁判官(모델)이 사건(데이터)을审判할 때 어떤 기준으로 判断하느냐에 따라 판결(예측)이 달라진다.杀人罪(异常값)에 대해杀人罪로 판단하면(MSE) 형량이 크게 달라지고,軽犯罪(평균적 패턴)로 판단하면(MAE) 형량이 작아진다.評価基準(손실 함수)을 어떻게 설정하느냐가 결론을 결정한다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 2.1 회귀 문제용 손실 함수

**MSE (Mean Squared Error)**
$$MSE = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

```python
import numpy as np

def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# 예시
y_true = np.array([1.0, 2.0, 3.0, 4.0])
y_pred = np.array([1.1, 1.9, 3.2, 3.8])
mse(y_true, y_pred)  # = 0.025
```

특징: 오차를 제곱하므로 큰 오차에 대해 강한 페널티 부여. outlier에 민감.

**MAE (Mean Absolute Error)**
$$MAE = \frac{1}{n} \sum_{i=1}^{n}|y_i - \hat{y}_i|$$

특징: 오차의 절대값. outlier에 덜 민감하지만 미분 불가능한 점이 존재.

**Huber Loss**
$$L_\delta(y, \hat{y}) = \begin{cases} \frac{1}{2}(y-\hat{y})^2 & \text{if } |y-\hat{y}| \leq \delta \\ \delta|y-\hat{y}| - \frac{1}{2}\delta^2 & \text{otherwise} \end{cases}$$

특징: MSE와 MAE의折衷. 작은 오차에는 MSE로, 큰 오차에는 MAE로 행동.

```text
[회귀용 손실 함수 비교]

손실 값
   │
   │         ┌─ MSE (L2): 오차 증가 시 손실이 급격히 증가
   │        ╱
   │       ╱  ── Huber (δ=1.0)
   │      ╱  /
   │     ╱  /
   │    ╱  /
   │   ╱  ── MAE (L1)
   │  ╱
   │ ╱
   └────────────────────→ |오차|
        0    1    2    3

적용 가이드라인:
  - outliers가 거의 없음: MSE
  - outliers가 존재: MAE 또는 Huber
  - 미분 가능성 필요: MSE 또는 Huber
```

### 2.2 분류 문제용 손실 함수

**Binary Cross-Entropy (Log Loss)**
$$L = -\frac{1}{n} \sum_{i=1}^{n}[y_i \log(\hat{y}_i) + (1-y_i) \log(1-\hat{y}_i)]$$

```python
from sklearn.metrics import log_loss

y_true = [0, 0, 1, 1]
y_pred = [0.1, 0.2, 0.8, 0.9]
log_loss(y_true, y_pred)  # ≈ 0.164
```

특징: 확률 예측에 적합. 작은 확률에서 log는 큰 손실값을 produce.

**Categorical Cross-Entropy**
$$L = -\sum_{c=1}^{C} y_c \log(\hat{y}_c)$$

다중 클래스 분류에 사용. 출력층에 softmax와 함께 사용.

**Hinge Loss (SVM)**
$$L = \max(0, 1 - y \cdot \hat{y})$$

특징: Support Vector Machine에서 사용. 결정 경계에서 올바르게 분류되면 손실 0.

```text
[분류용 손실 함수 비교]

Binary Classification (y ∈ {0, 1}):

Cross-Entropy:
  - 예측: 0.9, 실제: 1 → 손실 = -log(0.9) ≈ 0.105
  - 예측: 0.1, 실제: 1 → 손실 = -log(0.1) ≈ 2.302 (큰 페널티)
  → 확률적 예측에 적합

Hinge Loss:
  - 예측: 0.9, 실제: 1 → 손실 = max(0, 1 - 1×0.9) = 0.1
  - 예측: 0.1, 실제: 1 → 손실 = max(0, 1 - 1×0.1) = 0.9
  → 결정 경계와의 거리에 페널티
```

### 2.3 손실 함수의 수학적 성질

손실 함수의 선택은 최적화 알고리즘과 긴밀하게 연결되어 있다.

| 손실 함수 | 미분 가능 | 볼록 |鲁棒성 | 파생 gradient |
|:---|:---|:---|:---|:---|
| **MSE** | Yes | Yes | 낮음 (outlier 민감) | y - ŷ |
| **MAE** | No (at 0) | Yes | 높음 | sign(y - ŷ) |
| **Cross-Entropy** | Yes | Yes | 보통 | ŷ - y |
| **Hinge** | Yes (except boundary) | No | 높음 | 복잡함 |

> 📢 **섹션 요약 비유**: 손실 함수는犹如물체의 중력장과 같다. 중력이 있으면 물체는중력이最小的 방향으로 이동한다(최적화). 물체의 위치(파라미터)가 같은 장소에 있어도중력의 세기(미분值)가 다르면 이동하는 방향과 속도가 달라진다. 적절한 중력장(손실 함수)을 설정해야 원하는 곳에 도달할 수 있다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

손실 함수의 선택과其他 요소들의 관계를 살펴보자.

```text
[손실 함수 ↔ 모델 ↔ 최적화 관계]

                    손실 함수
                        │
         ┌──────────────┼──────────────┐
         │              │              │
    회귀 문제       이진 분류       다중 클래스
         │              │              │
        MSE           BCE          Cross-Entropy
        MAE         Hinge            Softmax
       Huber          Focal            + CE
         │              │              │
         └──────────────┼──────────────┘
                        │
                   최적화 알고리즘
                   (Gradient Descent)
                        │
            ┌───────────┼───────────┐
            │           │           │
        SGD          Adam          Newton
```

**Focal Loss (RetinaNet에서 제안)**
$$FL(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)$$

클래스 불균형 문제에 특화. 易分类样本의 기여을 줄이고, 难分类样本에 집중.

```python
import torch
import torch.nn.functional as F

def focal_loss(pred, target, alpha=0.25, gamma=2.0):
    ce_loss = F.cross_entropy(pred, target, reduction='none')
    pt = torch.exp(-ce_loss)
    focal_loss = alpha * (1 - pt) ** gamma * ce_loss
    return focal_loss.mean()
```

**커스텀 손실 함수의 필요성**
비즈니스에서 특정 형태의 오류에 더 큰 페널티를 부여해야 하는 경우가 있다.

```python
# 예: 시간 예측에서 늦게 예측하는 것이 빨리 예측하는 것보다 더 나쁜 경우
def asymmetric_mse(y_true, y_pred, late_penalty=2.0):
    error = y_pred - y_true
    # 늦게 예측 (error > 0): late_penalty 배로 페널티
    # 일찍 예측 (error < 0): 通常 페널티
    weights = np.where(error > 0, late_penalty, 1.0)
    return np.mean(weights * error ** 2)
```

> 📢 **섹션 요약 비유**: 손실 함수의 선택은犹如자동차の行驶模式選択と類似している. 스포츠 모드(MSE)에서는加速が速하지만 연비가 나쁘고, اقتصاد 모드(MAE)에서는 연비가 좋지만 반응이 느리다. 또한 커스텀 손실 함수(에코노미 + 안전)는普通의 경제 모드와는 다른 독특한 특성을 보인다. 같은 자동차(모델)라도 어떤 모드(손실 함수)를 설정하느냐에 따라 성능 특성 이 달라진다.

---

### Ⅳ. 실무 적용 및 한계 (Application & Limitation)

**실무 적용:**

1. **검색 엔진 (Learning to Rank)**
   - pairwise 손실 함수: 두 문서의 상대적 순서가 올바른지 평가
   - LambdaMART: Ranking에 특화된 손실

2. **객체 탐지 (Object Detection)**
   - Classification loss + Localization loss의 결합
   - Focal Loss: 클래스 불균형 처리

3. **생성 모델 (GAN)**
   - Generator Loss + Discriminator Loss의对抗적 학습
   - Wasserstein Loss:.Mode Collapse 완화

4. **의료 진단**
   - Recall을 강조하는 커스텀 손실 (FN은 FP보다 치명적일 수 있음)

```python
# scikit-learn에서의 다양한 손실 함수

from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC

# SGDClassifier: 손실 함수 선택 가능
clf = SGDClassifier(loss='hinge')      # SVM (Hinge Loss)
clf = SGDClassifier(loss='log_loss')   # 로지스틱 회귀 (Log Loss)
clf = SGDClassifier(loss='modified_huber')  # Hinge Loss의 smooth 버전

# 회귀
from sklearn.ensemble import GradientBoostingRegressor
reg = GradientBoostingRegressor(loss='squared_error')  # MSE
reg = GradientBoostingRegressor(loss='absolute_error')  # MAE
```

**한계점:**

1. **도메인 특수성**: 표준 손실 함수가 비즈니스 요구를 정확히 반영하지 못할 수 있다.

2. **클래스 불균형**: 표준 Cross-Entropy는 불균형 데이터에서 다수 클래스에 치우칠 수 있다.

3. **조합의 복잡성**: 여러 손실 함수를 결합할 때 가중치 조정이 필요하다.

4. **미분 가능성**: 일부 손실 함수(예: MAE)는 모든 곳에서 미분 불가능하여 최적화가 어려울 수 있다.

> 📢 **섹션 요약 비유**: 손실 함수의 설계는犹如楽器の调律과 유사하다. 오케스트라(머신러닝 시스템)에서 각 악기(모델)가 제각각의 음(예측)을 내는데, 이를統合하여 조화로운 음악(전반적 성능)을 만들어 내야 한다.调教師(데이터 과학자)가全体の音を聞いて微調整(손실 함수 설계)해야 한다. 때로는 특정 악기(특정クラス)에 더 많은 비중을 두어야 조화가 될 때가 있다.

---

### Ⅴ. 요약 및 전망 (Summary & Outlook)

손실 함수는 模型의 학습 방향을 결정하는 핵심 요소이다. 문제 유형(회귀, 분류, 순위 등)과 데이터 특성(	outliers, 클래스 불균형 등)에 따라 적절한 손실 함수를 선택해야 한다.

앞으로의 전망으로는, 더 복잡한 실제 환경에서의 커스텀 손실 함수 개발, 다목적 손실 함수(Multi-Task Learning에서의 손실 조합), 그리고 AutoML을 통한 손실 함수 자동 선택 등의 研究가 진행될 것이다. 또한 설명 가능한 AI와 결합하여"公平성"이나"隐私保护"를 반영하는 새로운 손실 함수에 대한 연구도 활발히 진행되고 있다.

결론적으로, 손실 함수의 선택은 단순히 주어진 함수를 사용하는 것을 넘어, 해결하려는 문제의 본질적 목표를 어떻게 수학적으로 formulate할 것인가의 문제이다.

---

**References**
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press.
- Lin, T.-Y., et al. (2017). Focal Loss for Dense Object Detection. ICCV.
- Murphy, K. P. (2012). Machine Learning: A Probabilistic Perspective. MIT Press.
