+++
weight = 86
title = "86. 학습률/경사하강법 (Learning Rate/Gradient Descent)"
description = "학습률과 경사하강법의 기본 원리, 다양한 확률적 경사하강법 변형, 학습률 스케줄링 기법"
date = "2026-04-05"
[taxonomies]
tags = ["학습률", "LearningRate", "경사하강법", "GradientDescent", "SGD", "Adam", "모멘텀"]
categories = ["studynote-bigdata"]
+++

# 학습률/경사하강법 (Learning Rate/Gradient Descent)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 경사하강법(Gradient Descent)은 손실 함수의 gradient의 반대 방향으로 파라미터를 반복적으로 업데이트하여 손실을 최소화하는 최적화 알고리즘이며, 학습률(Learning Rate)은 각 업데이트에서 얼마만큼 이동할지를 결정하는 스케일 factor이다.
> 2. **가치**: 적절한 학습률 선택이 모델 수렴 속도와 최종 성능을 결정하며, 너무 크면 발산하고 너무 작으면 느리게 수렴하거나 지역 최솟값에 갇힐 수 있다.
> 3. **융합**: SGD, Momentum, AdaGrad, RMSProp, Adam 등 다양한 확률적 경사하강법 변형이 있으며, 학습률 스케줄링(Learning Rate Scheduling)과 결합하여 더 효율적인 학습이 가능하다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

경사하강법(Gradient Descent)은 머신러닝과 딥러닝에서 가장 fundamental한 최적화 알고리즘이다. 그 핵심 아이디어는"손실 함수의 기울기(gradient)의 반대 방향으로 조금씩 이동하면 손실을 줄일 수 있다"는 것이다. 이는 산을 내려갈 때 가장 가파른 경로를 따라 한 발짝씩 내려가는 것과 similar하다.

학습률(Learning Rate)은 이 산을 내려가는 각 단계의 크기를 결정한다. 만약 학습률이 너무 크면对面的山坡를 건너뛰어 오히려 손실이 증가할 수 있고, 너무 작으면下山하는데 너무 오래 걸리거나 지역적인 골짜기(지역 최솟값)에 갇힐 수 있다.

```text
[학습률의影響]

손실 함수 L(w)를 최소화하는 파라미터 w를 찾는 문제

        L(w)
          │峰值 (높은 손실)
          │    ╱
          │   ╱  ← gradient 방향
          │  ╱
          │ ╱
          │╱
          ●━━━━━━━━━━━━→ w (파라미터)
         /│
        / │ 학습률太小: 거의 진동 없음, 느린 수렴
       /  │ 학습률 적절: 빠른 수렴
      /   │ 학습률太大: 발산 또는振动
     /    │

[학습률별 수렴 패턴]

학습률 α = 0.001 (너무 작음):
  손실 ↓↓↓↓↓↓↓↓↓↓ (очень медленно)
  → 10000 에포크 필요

학습률 α = 0.1 (적절):
  손실 ↓↓↓↓↓ (빠르게 수렴)
  → 100 에포크 필요

학습률 α = 10.0 (너무 큼):
  손실 ↑↓↓↑↓↓↑↓↓ (발산 또는振动)
  → 수렴하지 않음
```

> 📢 **섹션 요약 비유**: 경사하강법의 학습률 선택은犹如자동차의 가속 페달と類似している. 너무 가볍게 밟으면(낮은 학습률)交叉点に到達하기 전에信号이 바뀌고, 너무 세게 밟으면(높은 학습률)車輛が飛び出하거나摇晃하게 된다. 적절한 힘으로 밟아야 안전하고 빠르게 목적지에 도착할 수 있다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 2.1 기본 경사하강법 (Batch Gradient Descent)

전체 훈련 데이터에 대한 gradient를 계산하여 한 번에 파라미터를 업데이트한다.

```python
# Pseudocode for Batch Gradient Descent
w = w_initial  # 초기 파라미터

for epoch in range(num_epochs):
    gradient = compute_gradient(loss_function, X, y, w)  # 전체 데이터에 대해 gradient 계산
    w = w - learning_rate * gradient  # 업데이트
```

$$w_{t+1} = w_t - \alpha \cdot \nabla L(w_t)$$

```text
[Batch Gradient Descent 동작]

전체 데이터: ●●●●●●●●●●●●●●●● (N=1000개)

각 에포크에서:
  1. 전체 1000개 데이터의 平均 gradient 계산
  2. 한 번의 큰 업데이트

  에포크 1: w → w₁ (1000개 gradient 계산)
  에포크 2: w₁ → w₂ (1000개 gradient 계산)
  ...
  에포크 t: w_{t-1} → w_t

장점: 정확한 gradient 방향
단점: N이 크면 계산 비용이 매우 높음
      메모리에 전체 데이터 필요
```

### 2.2 확률적 경사하강법 (Stochastic Gradient Descent, SGD)

각 샘플 또는 작은 배치에 대해 gradient를 계산하고 즉시 업데이트한다.

```python
# Pseudocode for SGD
w = w_initial

for epoch in range(num_epochs):
    for i in range(N):  # 각 샘플마다
        xi, yi = X[i], y[i]
        gradient = compute_gradient_single(loss_function, xi, yi, w)
        w = w - learning_rate * gradient
```

```text
[SGD vs Batch GD]

Batch GD (N=1000):
  에포크당 gradient 계산: 1회 (전체 데이터)
  업데이트 횟수: 1회

SGD:
  에포크당 gradient 계산: 1000회 (샘플마다)
  업데이트 횟수: 1000회

  에포크 1: w → w₁ → w₂ → ... → w₁₀₀₀
  에포크 2: w₁₀₀₀ → w₁₀₀₁ → ... → w₂₀₀₀

"확률적"인 이유:
  - 전체 데이터의 gradient가 아닌,
    개별 샘플의 gradient로 gradient를 추정
  - 노이즈가 있지만 이것이 지역 최솟값 탈출에 도움될 수 있음
```

### 2.3 미니배치 확률적 경사하강법 (Mini-batch SGD)

배치 크기(Batch Size)만큼의 샘플을 모아 gradient를 계산한다.Batch GD와 SGD의折衷이다.

```python
# Pseudocode for Mini-batch SGD
w = w_initial
batch_size = 32

for epoch in range(num_epochs):
    # 데이터를 배치로 분할
    for batch in DataLoader(X, y, batch_size=32):
        gradient = compute_gradient(loss_function, batch, w)
        w = w - learning_rate * gradient
```

```text
[Mini-batch SGD의장점]

배치 크기 선택:
  Batch Size = N (전체 데이터) → Batch GD (정확하지만 느림)
  Batch Size = 1 → SGD (빠르지만 노이즈 심함)
  Batch Size = 32~256 → Mini-batch SGD (折衷)

  ┌──────────────────────────────────────────────────┐
  │                                                  │
  │   배치 크기별 특성:                              │
  │   • 작을수록: 더 나은 일반화 (노이즈가 도움)     │
  │   • 클수록: 더 빠른 수렴 (GPU 병렬화 효과)        │
  │                                                  │
  │   일반적 권장: 32, 64, 128, 256                │
  │   (2의 거듭제곱이 GPU 메모리에 맞기 쉬움)        │
  │                                                  │
  └──────────────────────────────────────────────────┘
```

### 2.4 모멘텀 (Momentum)

이전 업데이트 방향을 고려하여 관성을준다.

```python
# 모멘텀의 동작
v = 0  # 속도

for epoch in range(num_epochs):
    for batch in dataloader:
        gradient = compute_gradient(loss, batch, w)

        v = momentum * v - learning_rate * gradient  # 모멘텀 적용
        w = w + v
```

```text
[모멘텀 효과]

Without Momentum (SGD):
  ●→→→→→↓
  │  ↘        ← 골짜기에서 진동
  │    ↘

With Momentum (β=0.9):
  ●→→→→→↓
       ╲      ← 모멘텀이 수렴 가속화
        ╲→→→↓
            ↓

物리적 비유:
  - 모멘텀 없는場合: 공이 울퉁불퉁한 표면을 천천히 구름
  - 모멘텀 있는 경우: 속도를 모아 빠르게 구름
  - 특히 평평한 부분에서 도움됨
```

### 2.5 Adam (Adaptive Moment Estimation)

Adam은 모멘텀과 RMSProp을 결합한 것으로,각 파라미터에 적응적 학습률을 적용한다.

```python
# Adam 알고리즘
m = 0  # 첫 번째 모멘트 (평균)
v = 0  # 두 번째 모멘트 (분산)

for epoch in range(num_epochs):
    for batch in dataloader:
        g = compute_gradient(loss, batch, w)

        m = beta1 * m + (1 - beta1) * g        # 모멘텀 업데이트
        v = beta2 * v + (1 - beta2) * g**2      # RMSProp 업데이트

        m_hat = m / (1 - beta1**t)              #バイアス補正
        v_hat = v / (1 - beta2**t)

        w = w - learning_rate * m_hat / (sqrt(v_hat) + epsilon)
```

> 📢 **섹션 요약 비유**: Adam은犹如経験豊富な万能ランナー と類似している. 일반 랜너(일반 SGD)가只知道현재 발밑의 경사만 보고 뛰지만, Adam은過去の 뛰어난 경향을 기억(모멘텀)하면서도 최근 훈련 상태를 파악(적응적 학습률)하여 더 효율적으로 � 수 있다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

주요 최적화 알고리즘들을 비교해보자.

| 알고리즘 | 업데이트 방식 | 학습률 | 모멘텀 | 특성 |
|:---|:---|:---|:---|:---|
| **GD** | 전체 gradient | 고정 | 없음 | 정확한 gradient, 느림 |
| **SGD** | 개별 샘플 gradient | 고정 | 없음 | 빠름, 노이즈 많음 |
| **Momentum** | 배치 gradient | 고정 | 있음 | 진동 감소 |
| **Nesterov** | 배치 gradient | 고정 | 있음 | Look-ahead gradient |
| **AdaGrad** | 배치 gradient | 적응적 | 없음 | 희소 데이터에 좋음 |
| **RMSProp** | 배치 gradient | 적응적 | 없음 | 비안정적gradient에 좋음 |
| **Adam** | 배치 gradient | 적응적 | 있음 | 대부분의 경우 좋은 기본값 |

```text
[학습률 스케줄링]

학습률을 에포크마다 또는 일정한 간격으로 조정한다.

1. Step Decay:
  - 특정 에포크마다 학습률 감소
  예: 0.1 → 0.01 → 0.001 (각 30, 60 에포크마다)

2. Exponential Decay:
  - 학습률이指數적으로 감소
  α_t = α₀ × γ^t (γ ≈ 0.95)

3. Cosine Annealing:
  - Cosine 함수 형태로 학습률이 증감
  - Warm-up + Cool-down 가능

4. Reduce on Plateau:
  - 검증 성능이 개선되지 않으면 학습률 감소
  patience = 5, factor = 0.5

5. Warm-up:
  - 처음 몇 에포크 동안 학습률을 점진적으로 증가
  - 대규모 모델/데이터에서 안정적 수렴에 도움
```

> 📢 **섹션 요약 비유**: 학습률 스케줄링은犹如登山家の戦略と類似している. 산의 가파른 부분에서는 빠르게 내려올 수 있지만(높은 학습률), 협곡에 가까워지면 속도를 줄여야 한다(학습률 감소). 때로는 옆으로 돌아가며 길을 찾는 것도 필요하다(모멘텀).

---

### Ⅳ. 실무 적용 및 한계 (Application & Limitation)

**실무 적용:**

1. **图像 분류 (CNN)**: Adam (lr=0.001)이 기본값으로 널리 사용됨

2. **Transformer**: AdamW (Adam + Weight Decay)와 함께 Cosine Annealing Scheduler 활용

3. **.Object Detection**: SGD with Momentum (lr=0.01~0.001)이 여전히 선호됨

```python
# PyTorch에서의 학습률 설정 예시
import torch.optim as optim

# SGD with Momentum
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=1e-4)

# Adam
optimizer = optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))

# AdamW (권장)
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# 학습률 스케줄러
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
```

**한계점:**

1. **지역 최솟값 문제**: 고차원 공간에서는 지역 최솟값보다鞍点(Saddle Point)가 더 큰 문제이다.

2. **학습률 민감도**: Adam도 학습률 초기값에敏感하다.

3. **수렴 보장이 없음**: 비볼록(non-convex) 함수에서는全局 최적점에 도달한다는 보장이 없다.

> 📢 **섹션 요약 비유**: 경사하강법과 학습률은犹如解 Puzzle Toysと類似している. 조각(파라미터)을 올바른 위치(최적해)에 놓기 위해 약간씩 움직이는데(gradient), 너무 많이 움직이면 위치를 지나치고(발산), 너무 적게 움직이면 찾는 데 시간이 오래 걸린다(느린 수렴). 올바른 정도의 힘(학습률)을 순간순간 판단해 가며 움직여야 한다.

---

### Ⅴ. 요약 및 전망 (Summary & Outlook)

학습률과 경사하강법은딥러닝 최적화의 핵심 요소이다. Adam이 대부분의 상황에서 좋은 기본값을 제공하지만, SGD with Momentum이某些タスクでより 좋은 성능을 보이기도 한다.

앞으로는 더 효율적인 최적화 알고리즘 개발,Learning Rate의自動 조정, 그리고 Hessian 기반의 2차 최적화 방법론 등의 研究가 진행되고 있다.

결론적으로, 학습률 선택은 경험과 실험을 통해 이루어지며, 적절한learning rate schedule과 결합할 때より良い 수렴을 달성할 수 있다.

---

**References**
- Ruder, S. (2016). An overview of gradient descent optimization algorithms. arXiv:1609.04747.
- Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. ICLR.
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press.
