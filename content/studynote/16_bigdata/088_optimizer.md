+++
weight = 88
title = "88. 옵티마이저 (Optimizer)"
description = "옵티마이저의 개념, 다양한 최적화 알고리즘의 분류와 특성, Adaptive Learning Rate 방법론"
date = "2026-04-05"
[taxonomies]
tags = ["옵티마이저", "Optimizer", "최적화", "Adam", "SGD", "AdamW", "모멘텀"]
categories = ["studynote-bigdata"]
+++

# 옵티마이저 (Optimizer)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 옵티마이저(Optimizer)는 손실 함수의 값을 최소화하는 방향으로 모델 파라미터를 업데이트하는 알고리즘이다. 학습률, 모멘텀, 적응적 학습률 등의 메커니즘을 통해 효율적인 최적화를 도모한다.
> 2. **가치**: 적절한 옵티마이저 선택과 하이퍼파라미터 튜닝은 모델 수렴 속도와 최종 성능에 直接적 영향을 미친다.
> 3. **융합**: SGD, Adam, AdamW, RMSProp, AdaGrad 등 다양한 옵티마이저가 있으며, 각각 고유한 장단점이 있어 문제 상황에 맞게 선택해야 한다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

옵티마이저(Optimizer)는 머신러닝과딥러닝에서 模型의 파라미터를更新하여 손실 함수를 최소화하는 핵심 알고리즘이다. 손실 함수가山脈의 높이 차이를 나타낸다면, 옵티마이저는 그山脈을 가장 효율적인 경로로 내려오는探险가이다.

深度學習에서는 수백만~수십억 개의 파라미터를 포함하는 매우複雑な 非凸最適化 문제를 풀어야 한다. 따라서 옵티마이저의 선택은 模型의 훈련 효율과 最终性能에 Crucial한 영향을 미친다.

옵티마이저의 발전 과정을 시각화해보면 다음과 같다.

```text
[옵티마이저의 발전 역사]

1952: Gradient Descent (Cauchy)
    │
    │  문제: 전체 데이터의 gradient 계산 필요, 느림
    ▼
1986: Stochastic Gradient Descent (SGD)
    │  Batch GD보다 빠르지만 노이즈 심함
    │  문제: 모든 파라미터에 동일한 학습률 적용
    ▼
1983: Momentum (Polyak)
    │  이전 gradient 방향에 관성 부여
    │  문제: 여전히 고정 학습률
    ▼
2011: AdaGrad
    │  적응적 학습률 (파라미터별)
    │  문제: 학습률이 계속 감소하는 문제
    ▼
2012: RMSProp
    │  AdaGrad의 문제 해결 (지수 이동 평균)
    ▼
2014: Adam (Adaptive Moment Estimation)
    │  모멘텀 + RMSProp 결합
    │  현재 딥러닝의 사실상의 표준
    ▼
2017: AdamW (Decoupled Weight Decay)
    │  Adam + L2 Regularization의 올바른 분리
    ▼
~2018 이후: LAMB, NovoGrad, Ranger, ...
    │  대규모 분산 훈련을 위한 최적화
    ▼
```

> 📢 **섹션 요약 비유**: 옵티마이저의 발전 역사는犹如교통手段의进化と類似している. 처음에는 다리를 사용해 직접 걸어갔다면(Gradient Descent),、自行车(SGD)를 타고 이동하는 것이 더 빨라졌다. 그리고堵著에는，自行车の速度를 상황에 맞게 조절하는 능력이 필요해졌다(Momentum). Cars、오토바이等의 다양한交通工具(다양한 옵티마이저)가 개발된 것처럼,、深層学習에서도 다양한 최적화 알고리즘이 등장했다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 2.1 옵티마이저의 구성 요소

대부분의 옵티마이저는 다음 요소들의 조합으로 구성된다.

```text
[옵티마이저의 핵심 요소]

파라미터 업데이트 규칙:
  θ_{t+1} = θ_t - α × update(gradient, history)

주요 요소:
  1. 학습률 (α): 업데이트의 스케일
  2. 모멘텀: 이전 업데이트 방향의 관성
  3. 적응적 학습률: 파라미터별 학습률 조정
  4. Regularization: 과적합防止
```

### 2.2 주요 옵티마이저 심층 분석

**SGD (Stochastic Gradient Descent)**

```python
# SGD 옵티마이저
# θ_{t+1} = θ_t - α ∇L(θ_t)

class SGD:
    def __init__(self, lr=0.01, momentum=0.0):
        self.lr = lr
        self.momentum = momentum
        self.v = None

    def step(self, params, grads):
        if self.v is None:
            self.v = [np.zeros_like(p) for p in params]

        for i, (p, g) in enumerate(zip(params, grads)):
            if self.momentum > 0:
                self.v[i] = self.momentum * self.v[i] - self.lr * g
            else:
                self.v[i] = -self.lr * g
            p += self.v[i]
```

**Adam (Adaptive Moment Estimation)**

Adam은 각 파라미터에 대해 적응적 학습률을計算한다.

```python
# Adam 옵티마이저 상세
# m_t = β₁ · m_{t-1} + (1-β₁) · g_t     (모멘텀, 1차 모멘트)
# v_t = β₂ · v_{t-1} + (1-β₂) · g_t²    (적응 학습률, 2차 모멘트)
# m_hat = m_t / (1 - β₁^t)                (바이어스補正)
# v_hat = v_t / (1 - β₂^t)
# θ_{t+1} = θ_t - α · m_hat / (√v_hat + ε)

class Adam:
    def __init__(self, lr=0.001, β₁=0.9, β₂=0.999, ε=1e-8):
        self.lr = lr
        self.β₁ = β₁
        self.β₂ = β₂
        self.ε = ε
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        self.t += 1
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]

        for i, (p, g) in enumerate(zip(params, grads)):
            # 1차 모멘트 (모멘텀)
            self.m[i] = self.β₁ * self.m[i] + (1 - self.β₁) * g
            # 2차 모멘트 (적응 학습률)
            self.v[i] = self.β₂ * self.v[i] + (1 - self.β₂) * (g ** 2)

            # 바이어스 보정
            m_hat = self.m[i] / (1 - self.β₁ ** self.t)
            v_hat = self.v[i] / (1 - self.β₂ ** self.t)

            # 업데이트
            p -= self.lr * m_hat / (np.sqrt(v_hat) + self.ε)
```

```text
[Adam의物적意味]

m_t (모멘텀): gradient의 지수加权移動平均
  →過去のgradient 방향을 기억하여 진동 감소

v_t (적응 학습률): gradient 제곱의 지수加权移動平均
  →陡한 방향(큰 gradient)에서는 학습률을 줄이고
    平坦한 방향(작은 gradient)에서는 학습률을 유지

예시:
  파라미터 θ₁ (거친 gradient): v_hat 큼 → 학습률 ↓
  파라미터 θ₂ (미세한 gradient): v_hat 작음 → 학습률 유지
```

### 2.3 AdamW (Weight Decay의 올바른 분리)

AdamW는 Adam의 L2 Regularization 문제를 해결한다.

```python
# Adam vs AdamW의 차이

# Adam (잘못된 L2 regularization)
loss = compute_loss(params) + λ * Σ||params||²  # 손실에 L2 추가
# 문제: 옵티마이저가 gradient를計算할 때 이미 L2 영향이 포함됨
# 但し learning rate 조정을 통해 적용되어 문제가 있음

# AdamW (올바른 분리)
loss = compute_loss(params)  # 손실에 L2 추가 안 함
optimizer.step()
# 옵티마이저 내부에서 직접 weight decay 적용
params -= (self.lr * m_hat / (np.sqrt(v_hat) + ε) + self.lr * λ * params)
```

### 2.4 Learning Rate Scheduling

옵티마이저와 함께 학습률을 동적으로 조절한다.

```text
[주요 Learning Rate Schedule]

1. Step Decay:
   epoch 1-30:  lr=0.1
   epoch 31-60: lr=0.01
   epoch 61-90: lr=0.001

2. Cosine Annealing:
   lr(t) = lr_max × (1 + cos(πt/T)) / 2
   (0에서 시작해 가장高点 дости後 다시 감소)

3. Warmup + Decay:
   - 처음 few epochs: lr 점진적 증가
   - 이후: Cosine或其他 schedule로 감소

4. Reduce on Plateau:
   - 검증 성능이 개선되지 않으면 lr 감소
```

> 📢 **섹션 요약 비유**: 옵티마이저는犹如万能钥匙と類似している. 모든 문(문제)에 동일한 열쇠(기본 옵티마이저)를 쓸 수 있지만, 열쇠의デザイン(파라미터 설정)를 상황에 맞게 조정해야 가장 잘 열린다. 때로는 열쇠를 삐딱하게 돌리거나(모멘텀), 힘을 가감해야(학습률) 문이 쉽게 열린다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

주요 옵티마이저를 비교해보자.

| 옵티마이저 | 장점 | 단점 | 권장 사용 상황 |
|:---|:---|:---|:---|
| **SGD + Momentum** | 일반화 양호, 튜닝 쉬움 | 수렴 느림 | 컴퓨터 비전, 전통적 ML |
| **Adam** | 빠른 초기 수렴, 대부분의 경우 good | 종종 SGD보다 일반화 낮음 | 자연어 처리,빠른 prototyping |
| **AdamW** | Adam + 올바른 정규화 | 하이퍼파라미터 민감 | Transformer,大型モデル |
| **LAMB** | 대규모 분산 훈련에 효과적 | 구현 복잡 | BERT规模的训练 |
| **AdaGrad** | 희소 데이터에 효과적 | 학습률 감소 문제 | 추천 시스템, RNN |

```text
[SGD vs Adam: 공통된 인식]

일반적인 인식:
  • Adam: 빠른 수렴, 낮은 훈련 손실
  • SGD: 더 나은 일반화, 더 높은 훈련 손실

실제 연구 결과 (Reddi et al., 2018):
  • Adam의 수렴 문제가 있을 수 있음 (arnesiate 문제)
  • 적절한 하이퍼파라미터로 Adam도 SGD에 필적하는 성능

결론:
  ✓ Rapid Prototyping: Adam (빠른 iteration)
  ✓ Production/Competition: SGD + Momentum (より良い一般化)
  ✓大型モデル: AdamW 또는 LAMB
```

> 📢 **섹션 요약 비유**: 옵티마이저 선택은犹如料理での火加減と類似している. 강불(높은 학습률)로 빨리 끓일 수 있지만 넘칠 위험이 있고, 약불(낮은 학습률)은 안전하지만 시간이 오래 걸린다. 가스레인지의 자동 제어 기능(Adam)은 편리하지만,_manual火加減(SGD+Momentum)에 비해 맛이 조금 다를 수 있다. 상황과 목적에 맞는火加減(옵티마이저) 선택이 필요하다.

---

### Ⅳ. 실무 적용 및 한계 (Application & Limitation)

**실무 적용:**

1. **컴퓨터 비전 (CNN)**
   - SGD + Momentum (lr=0.01, momentum=0.9)
   - Weight Decay 적용
   - Step Decay 또는 Cosine Annealing

2. **자연어 처리 (Transformer)**
   - AdamW (lr=1e-4 ~ 3e-4, weight_decay=0.01)
   - Warmup + Cosine Annealing
   - Gradient Clipping (max_norm=1.0)

3. **Recommender Systems**
   - AdaGrad 또는 Adam
   - 학습률 lr=0.01 ~ 0.1

```python
# PyTorch에서의 옵티마이저 설정 예시
import torch.optim as optim

# SGD with Momentum
optimizer = optim.SGD(
    model.parameters(),
    lr=0.01,
    momentum=0.9,
    weight_decay=1e-4
)

# AdamW (권장 for Transformers)
optimizer = optim.AdamW(
    model.parameters(),
    lr=3e-4,
    betas=(0.9, 0.999),
    weight_decay=0.01
)

# Learning Rate Scheduler와 결합
scheduler = optim.lr_scheduler.OneCycleLR(
    optimizer,
    max_lr=3e-4,
    epochs=num_epochs,
    steps_per_epoch=len(train_loader)
)
```

**한계점:**

1. **수렴 보장 없음**: 비볼록(non-convex) 함수에서全局 최적 보장 없음

2. **지역 최솟값/鞍点 문제**: 특히 고차원에서는鞍점(saddle point)이 지역 최솟값보다 문제

3. **하이퍼파라미터 민감도**: Adam도 학습률, β₁, β₂ 등의 조정이 필요

4. **대规模 모델에서의 메모리**: 2차 모멘트(v_t) 추가로 메모리 사용량 증가

> 📢 **섹션 요약 비유**: 옵티마이저는犹如探索ロボットと類似している.複雑な 미로(손실 함수 landscape)에서 最速経路으로出口(최적해)를 찾아야 한다. 로봇은壁(gradient)를 감지하여 방향을 결정하는데, 너무 빨리 움직이면 벽에 충돌하고(발산), 너무 느리면 시간 내에 탈출하지 못한다(느린 수렴). 때로는 후진해서 우회하는 것이(모멘텀) 더 빠른 경우도 있다.

---

### Ⅴ. 요약 및 전망 (Summary & Outlook)

옵티마이저는深度학습 훈련의核心要素이다. Adam이 대부분의 상황에서 좋은 기본값을 제공하지만, SGD + Momentum이、より良い一般化性能を達成する場合도 많다.

앞으로의 전망으로는, 더 대규모 분산 훈련을 위한 최적화 알고리즘,Learning Rate 자동 조정 기능의 통합, 그리고 二階堂最適化 방법론의 효율적 구현 등의 研究가 진행되고 있다. 또한 Neuroscience의 发现를 활용한biol-inspired 최적화 알고리즘도 기대된다.

결론적으로, 옵티마이저 선택은 경험, 실험, 그리고 문제 상황에 대한 이해를 통해 이루어져야 하며, 어떤 경우에도万能적인最优解는 없다.

---

**References**
- Ruder, S. (2016). An overview of gradient descent optimization algorithms. arXiv:1609.04747.
- Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. ICLR.
- Loshchilov, I., & Hutter, F. (2017). Decoupled Weight Decay Regularization. ICLR.
- Reddi, S. J., et al. (2018). On the Convergence of Adam and Beyond. ICLR.
