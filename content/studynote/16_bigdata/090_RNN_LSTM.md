+++
weight = 90
title = "90. RNN/LSTM (순환 신경망/장단기 기억 네트워크)"
description = "RNN의 기본 구조와 한계, LSTM의 게이트 메커니즘, 시계열/NLP에서의 활용"
date = "2026-04-05"
[taxonomies]
tags = ["RNN", "LSTM", "순환신경망", "장단기기억", "시계열", "순환연결", "게이트"]
categories = ["studynote-bigdata"]
+++

# RNN/LSTM (순환 신경망/장단기 기억 네트워크)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: RNN(Recurrent Neural Network)은 시계열이나 순서 데이터처럼 시간적 의존성을 가지는 데이터를 처리하기 위해 설계된 신경망으로, 은닉 상태(Hidden State)를 통해 이전 시간 단계의 정보를 현재로 전달하는 순환 구조를 가진다.
> 2. **가치**: 기본 RNN의 장기 의존성 학습 한계(Gradient Vanishing/Exploding)를克服하기 위해 LSTM(Long Short-Term Memory)은 입력, 출력,遗忘을 제어하는 게이트 메커니즘을 도입하여 긴 시간 스텝의 의존성도 효과적으로 학습할 수 있게 했다.
> 3. **융합**: 시계열 예측, 자연어 처리(번역, 요약, 감성 분석), 음성 인식, 음악 생성 등 순서 데이터가 중요한 다양한 도메인에서 활용된다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

RNN(Recurrent Neural Network, 순환 신경망)은"순환"구조를 통해 시간적으로 연속적인 데이터를 처리할 수 있는 신경망이다. 전통적인 피드포워드(Feedforward) 신경망이 입력을 독립적으로 처리하는 것과 달리, RNN은 이전 입력의 정보를"기억"하여 현재 입력의 처리에도 활용한다.

우리가 문장을 이해할 때 이전 단어들을 기억하면서 다음 단어를 이해하는 것과 similar하게, RNN은 이전 시간 단계의 정보를 현재 상태에 전달하여 순서 데이터의 문맥을捕捉한다.

```text
[RNN의 순환 구조]

피드포워드 신경망:
  입력 → 은닉층 → 출력
  (각 입력은 독립적으로 처리)

RNN (시간에 펼침):
  시간 t=1: x₁ → [RNN셀] → h₁ → 출력 o₁
                    ↓
  시간 t=2: x₂ → [RNN셀] → h₂ → 출력 o₂
                    ↓
  시간 t=3: x₃ → [RNN셀] → h₃ → 출력 o₃
                    ↓
                  ...

  각 시간 단계에서 동일한 RNN 셀 재사용
  h_t = f(W·x_t + U·h_{t-1} + b)

[언어 모델링 예시]

"The cat sat on the ___"
  t=1: "The" → h₁ (문장의 시작)
  t=2: "cat" → h₂ (h₁ + "cat")
  t=3: "sat" → h₃ (h₂ + "sat")
  t=4: "on" → h₄ (h₃ + "on")
  t=5: "the" → h₅ (h₄ + "the")
  t=6: "mat" → h₆ = "문맥을 반영한 현재 상태"
               → "mat" 다음에 올 단어 예측: " sat"
```

RNN이 필요한 이유는 순서 데이터에서 시간적 의존성(Temporal Dependency)을 모델링해야 하기 때문이다. 예컨대"나는 학교에갔다. 학교에서 친구들과 ___."라고 할 때, 빈칸에는"수업했다"나"놀다"처럼 학교와 관련된 단어가 와야 하는데, 이는 이전 문맥을把握해야만 예측 가능하다.

> 📢 **섹션 요약 비유**: RNN은犹如기억력이 있는eton이다. 각 계산单元(셀)이 과거의 정보를 요약하여"기억 노트"(은닉 상태)에 기록하고, 이 노트를 다음思考에 활용한다. 따라서 일관된 이야기(순서 데이터)를 이어갈 수 있다. 그러나 너무 오래 전의 정보는 기억이 희미해지는 문제가 있다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 2.1 기본 RNN의 구조

RNN의 핵심은 은닉 상태 h_t가 현재 입력 x_t와 이전 은닉 상태 h_{t-1} 모두에 의해 결정되는 것이다.

```text
[RNN 셀의 내부 구조]

      x_t
       │
       ▼
  ┌──────────────────────────────────┐
  │   h_{t-1}                        │
  │       │                           │
  │       ▼                           │
  │  ┌────────┐                       │
  │  │        │                       │
  │  │  RNN   │ ← W_xh·x_t + W_hh·h_{t-1} + b
  │  │  셀    │                       │
  │  │        │                       │
  │  └────────┘                       │
  │       │                           │
  │       ▼ h_t = tanh( activations )│
  │       │                           │
  └───────┼───────────────────────────┘
          │
          ├──→ 출력 o_t = W_hy·h_t
          │
          └──→ 다음 스텝으로 전달 (순환)
```

### 2.2 RNN의 한계: Gradient Vanishing/Exploding

RNN의 가장 큰 문제점은 긴 시퀀스를 학습할 때 발생하는 Gradient Vanishing(또는 Exploding)이다.

```text
[Gradient Vanishing 문제]

손실 함수의 gradient가 시간에 역전파될 때:

  ∂L/∂W ∝ ∂L/∂h_T × ∂h_T/∂h_{T-1} × ... × ∂h_2/∂h_1 × ∂h_1/∂W

  각 단계의 Jacobian:
    ∂h_{t}/∂h_{t-1} = W_hhᵀ × diag(tanh'())

  만약 |λ_max(W_hh)| < 1:
    → gradient가 지수적으로 감소 (Vanishing)
    → 너무 오래 전 정보는 학습에 거의 기여X

  만약 |λ_max(W_hh)| > 1:
    → gradient가 지수적으로 증가 (Exploding)
    → 훈련 불안정

예시:
  "The movie was fantastic and I loved it."
  vs
  "I heard about the movie that was... really... loved it... everyone..."

  ← "loved"와 연결되어야 하지만 너무 멀리 떨어짐
```

### 2.3 LSTM (Long Short-Term Memory)

LSTM은 1997년 Hochreiter와 Schmidhuber가 제안한 구조로, 게이트(Gate) 메커니즘을 통해 장기 의존성 문제를 해결했다.

```text
[LSTM 셀의 구조]

               x_t
                │
        ┌───────┴───────┐
        │               │
        ▼               ▼
  ┌─────────────────────────────┐
  │                              │
  │   ┌─────────┐    ┌───────┐ │
  │   │ Forget  │    │ Input │ │
  │   │ Gate    │    │ Gate  │ │
  │   │ f_t     │    │ i_t   │ │
  │   └────┬────┘    └────┬──┘ │
  │        │               │    │
  │        ▼               ▼    │
  │      ┌───────────────┐     │
  │      │               │     │
  │      │  Cell State   │     │
  │      │    C_t        │←┘   │
  │      │               │     │
  │      └───────┬───────┘     │
  │              │             │
  │              ▼             │
  │      ┌───────────────┐     │
  │      │    Output     │     │
  │      │    Gate o_t   │     │
  │      └───────────────┘     │
  │              │             │
  └──────────────┼─────────────┘
                 │
                 ▼
               h_t
```

LSTM의 핵심은 Cell State C_t라는 별도의 기억 통로이다. 이 기억을 게이트를 통해 선택적으로 추가하거나 삭제할 수 있다.

**세 개의 게이트:**
1. **Forget Gate (f_t)**: 이전 기억 중 무엇을 잊을지 결정
2. **Input Gate (i_t)**: 새로운 정보를 무엇을 기억할지 결정
3. **Output Gate (o_t)**: 최종 기억 중 무엇을 출력할지 결정

```python
# LSTM의 수식

f_t = σ(W_f · [h_{t-1}, x_t] + b_f)  # Forget Gate
i_t = σ(W_i · [h_{t-1}, x_t] + b_i)  # Input Gate
C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C)  # 새 정보 후보

C_t = f_t * C_{t-1} + i_t * C̃_t  # Cell State 업데이트

o_t = σ(W_o · [h_{t-1}, x_t] + b_o)  # Output Gate
h_t = o_t * tanh(C_t)  # 은닉 상태 = Output Gate * Cell State
```

### 2.4 GRU (Gated Recurrent Unit)

GRU는 LSTM의 간소화된 버전으로, Reset Gate와 Update Gate 두 개만 사용한다.

```python
# GRU의 수식 (LSTM보다 단순)

z_t = σ(W_z · [h_{t-1}, x_t])  # Update Gate
r_t = σ(W_r · [h_{t-1}, x_t])  # Reset Gate

h̃_t = tanh(W · [r_t * h_{t-1}, x_t])

h_t = (1 - z_t) * h_{t-1} + z_t * h̃_t
# Update Gate가 기존 기억과 새 기억의 비율을 조절
```

> 📢 **섹션 요약 비유**: LSTM은犹如상호명한이 있는은행원과 같다. Forget Gate는"더 이상 필요 없는 계좌는 닫아라"(기억 삭제), Input Gate는"새로운 고객을 등록하라"(새로운 정보 기억), Output Gate는"오늘 처리할 고객은 누구인가"(정보 선택적 출력)를 담당한다. 이를 통해短期记忆力(기본 RNN)보다 훨씬长期의客户관계(장기 의존성)를 효과적으로 관리할 수 있다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

RNN계열 모델들을 비교하고 다른 모델과 대비해보자.

| 모델 | 게이트 수 | 파라미터 수 | 장기 의존성 | 계산 비용 |
|:---|:---|:---|:---|:---|
| **Vanilla RNN** | 0 | 적음 | 힘、政策 | 낮음 |
| **LSTM** | 3 | 중간 | 우수 | 중간 |
| **GRU** | 2 | LSTM보다 적음 | LSTM보다 약간 낮음 | 낮음 |

```text
[RNN vs CNN]

RNN: 시간적 의존성 (Sequential dependency)
     "이 단어 다음에 무엇이 올 것인가?"

CNN: 공간적 의존성 (Spatial dependency)
     "이 픽셀과 이웃 픽셀들의 관계"

[RNN vs Transformer]

RNN:
  - 순차적 처리 (시퀀스 길이에 비례하는 계산)
  - 선형 복잡도 O(N)
  - 상태를 압축하여 전달 (정보 병목)

Transformer:
  - 병렬 처리 가능
  - Self-Attention으로 모든 위치 직접 연결
  - 이차 복잡도 O(N²) but 더 강력한 표현력

현재 트렌드:
  •NLP: Transformer가 RNN을 대체 (BERT, GPT 등)
  •그러나 RNN/LSTM은 여전히 임베디드 시스템 등 자원 제약 환경에서 활용
```

> 📢 **섹션 요약 비유**: RNN과 Transformer의 차이는犹如手紙の과 이메일의 차이와 유사하다. RNN은 편지를 순서대로 읽어가며 그 순간의 감정(은닉 상태)을 기억하면서 내용을 이해하는 것이고, Transformer는 전체 편지를 한 번에 펼쳐 모든 문장의 관련성을 동시에 확인하는 것이다. 이메일(Transformer)이 더 효율적이지만, 手紙(RNN)도 비용과简便성에서 여전히価値がある.

---

### Ⅳ. 실무 적용 및 한계 (Application & Limitation)

**주요 적용 분야:**

1. **기계 번역 (Machine Translation)**
   - Seq2Seq 모델: Encoder-Decoder 구조
   - "I love you" → [Encoder RNN] → [Decoder RNN] → "사랑해요"

2. **시계열 예측 (Time Series Forecasting)**
   - 주가 예측, 기상 예측, 에너지 소비 예측
   - LSTM이 특히 효과적

3. **음성 인식 (Speech Recognition)**
   - 오디오 시퀀스를 텍스트 시퀀스로 변환
   - CTC (Connectionist Temporal Classification) 손실과 결합

4. **자연어 생성 (Text Generation)**
   - 캐릭터 단위 또는 단어 단위 언어 모델

**한계점:**

1. **순차적 처리**: RNN은 시간 스텝을 순서대로 처리해야 하므로 병렬화에 한계

2. **장기 의존성 문제**: 기본 RNN에서는 여전히 gradient vanishing 문제

3. **긴 시퀀스에서의 효율성**: LSTM/GRU도 계산 비용이 시퀀스 길이에 비례

4. **메모리 제약**: 긴 시퀀스는.hidden state에 압축되어 정보 손실 발생

```python
# PyTorch에서의 LSTM 구현 예시
import torch.nn as nn

class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(
            embed_dim,
            hidden_dim,
            num_layers=2,
            batch_first=True,
            bidirectional=True  # 양방향 LSTM
        )
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        # x: (batch_size, sequence_length)
        embedded = self.embedding(x)  # (batch_size, seq_len, embed_dim)

        # LSTM forward
        lstm_out, (h_n, c_n) = self.lstm(embedded)
        # lstm_out: (batch_size, seq_len, hidden_dim * 2)
        # h_n: (num_layers * 2, batch_size, hidden_dim)

        # 양방향의 마지막 은닉 상태 결합
        hidden = torch.cat((h_n[-2], h_n[-1]), dim=1)  # (batch_size, hidden_dim * 2)

        return self.fc(hidden)
```

> 📢 **섹션 요약 비유**: LSTM은犹如기어가 많은 Insectと類似한면이 있다. 각 다리(게이트)가 독립적으로 움직이면서(입력, 출력,遗忘 제어) всего몸의 움직임(시퀀스 처리)을協調한다. 다리가 많으면 복잡한 terrain(장기 의존성)도克服할 수 있지만, 그만큼 제어해야 할 것이 늘어나고(파라미터 증가), 에너지원도 더 많이消費한다.

---

### Ⅴ. 요약 및 전망 (Summary & Outlook)

RNN과 LSTM은 순서 데이터 처리의 기초적인 모델로서贡献해왔다. 그러나 최근에는 Transformer 아키텍처의崛起로 인해NLP 등 많은 영역에서替代되고 있는 추세이다.

그러나 RNN/LSTM의 장점인 선형 복잡도 O(N)와 순차적 처리能力은 여전히 자원 제약 환경이나 streaming 데이터 처리에서 가치를 가지고 있다. 또한 최근에는 RNN과 Transformer를 결합한 Hybrid 모델이나, RNN의 효율성과 Transformer의 표현력을综合利用하는 연구도 진행되고 있다.

앞으로의 전망으로는, 더 효율적인 순환 구조 개발, 장기 의존성을 더 잘 포착하는 메커니즘, 그리고신경망과 명시적 메모리의 결합 등의研究方向가 유망하다.

---

**References**
- Hochreiter, S., & Schmidhuber, J. (1997). Long Short-Term Memory. Neural Computation, 9(8), 1735-1780.
- Cho, K., et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation. EMNLP.
- Chung, J., et al. (2014). Empirical Evaluation of Gated Recurrent Neural Networks on Sequence Modeling. arXiv.
