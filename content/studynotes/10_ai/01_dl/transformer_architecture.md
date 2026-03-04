+++
title = "트랜스포머 아키텍처 (Transformer Architecture)"
date = "2026-03-04"
[extra]
categories = "studynotes-ai"
+++

# 트랜스포머 아키텍처 (Transformer Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 순환(Recurrence) 구조를 완전히 배제하고 셀프 어텐션(Self-Attention) 메커니즘만을 활용하여 시퀀스 내 모든 요소 간의 전역적 관계를 병렬로 학습하는 혁신적인 신경망 아키텍처입니다.
> 2. **가치**: RNN의 고질적인 문제인 장기 의존성(Long-term Dependency)을 해결하고 대규모 병렬 연산을 가능하게 함으로써, GPT, BERT와 같은 거대 언어 모델(LLM)의 기술적 토대를 마련했습니다.
> 3. **융합**: 자연어 처리를 넘어 컴퓨터 비전(ViT), 음성 인식, 단백질 구조 예측(AlphaFold) 등 AI 전 분야의 파운데이션 모델(Foundation Model)로 진화하며 범용 인공지능(AGI) 시대를 견인하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**트랜스포머(Transformer)**는 2017년 Google Brain 팀의 논문 "Attention Is All You Need"를 통해 발표된 딥러닝 아키텍처입니다. 기존의 자연어 처리 모델들이 데이터를 순차적으로 처리하는 RNN(Recurrent Neural Network)이나 LSTM 구조에 기반했던 것과 달리, 트랜스포머는 전체 문장의 모든 단어를 동시에 입력받아 단어 간의 상관관계를 직접 계산합니다. 이는 행렬 연산을 통한 대규모 병렬화를 가능하게 하여 학습 속도를 비약적으로 향상시켰습니다.

#### 2. 💡 비유를 통한 이해
트랜스포머는 **'파티장의 웅성거림 속에서 대화하기'**에 비유할 수 있습니다.
- **RNN 방식**: 파티장에 들어온 순서대로 사람들의 말을 한 명씩 기억하며 전달받는 것입니다. 마지막 사람의 말을 들을 때쯤이면 첫 번째 사람이 한 말을 잊어버리기 쉽습니다.
- **트랜스포머 방식**: 파티장 중앙에 서서 모든 사람의 목소리를 동시에 듣는 것입니다. 내가 관심 있는 사람(Query)이 누구인지에 따라, 그와 관련된 말을 하는 사람(Key)의 목소리에만 집중(Attention)하여 정보를 추출(Value)합니다. 거리와 상관없이 나에게 중요한 정보라면 즉시 파악할 수 있는 능력을 갖춘 것입니다.

#### 3. 등장 배경 및 발전 과정
1.  **기존 기술의 치명적 한계점**: RNN은 시퀀스가 길어질수록 앞부분의 정보가 소실되는 '기울기 소실(Vanishing Gradient)' 문제와, 이전 단계의 계산이 끝나야 다음 단계를 진행할 수 있는 '순차적 연산 구조'로 인해 GPU의 병렬 연산 능력을 제대로 활용하지 못했습니다.
2.  **혁신적 패러다임의 변화**: 트랜스포머는 '순차성'을 버리는 대신 **'위치 인코딩(Positional Encoding)'**을 통해 순서 정보를 보강하고, 모든 연산을 행렬 곱으로 처리하여 하드웨어 가속 효율을 극대화했습니다.
3.  **비즈니스적 요구사항**: 인터넷상의 방대한 텍스트 데이터를 효율적으로 학습시켜야 하는 거대 IT 기업들에게 트랜스포머의 병렬성은 '확장 가능성(Scalability)'이라는 최고의 선물을 안겨주었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 트랜스포머 구성 요소 및 내부 메커니즘 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Self-Attention** | 문맥 내 단어 간 관계 파악 | Q, K, V 벡터의 내적을 통한 가중치 산출 | Scaled Dot-Product | 중요한 사람에게 집중하기 |
| **Multi-Head Attention** | 다양한 관점의 의미 학습 | Attention 연산을 병렬로 여러 번 수행 | Linear Projection | 여러 명의 눈으로 관찰하기 |
| **Positional Encoding** | 단어의 위치 정보 주입 | Sine/Cosine 함수 기반 주기적 신호 합성 | Absolute/Relative PE | 줄 서있는 번호표 달기 |
| **Feed Forward (FFN)** | 비선형 특징 추출 및 변환 | ReLU/GELU 활성화 함수 기반 2층 신경망 | Position-wise MLP | 개인별 심층 사고 과정 |
| **Add & Norm** | 학습 안정성 및 성능 유지 | 잔차 연결(Residual) 및 계층 정규화(Layer Norm) | Skip Connection | 기초 체력 유지 및 균형 |

#### 2. 트랜스포머 전체 구조 및 데이터 흐름 다이어그램

```text
<<< Transformer Encoder-Decoder Full Architecture >>>

      [ Output Probabilities ]
                 ^
                 | (Softmax & Linear)
   +-----------------------------+
   |        Decoder Stack        | (N Layers)
   |  +-----------------------+  |
   |  | Position-wise FFNN    |  |
   |  +-----------^-----------+  |
   |              |              |
   |  +-----------+-----------+  | <--- (From Encoder)
   |  | Encoder-Decoder Attn  |  |      K, V Vectors
   |  +-----------^-----------+  |
   |              |              |
   |  +-----------+-----------+  |
   |  | Masked Self-Attention |  | (Causal Masking)
   |  +-----------^-----------+  |
   +--------------+--------------+
                 ^
                 | (Target Embed + Positional)

------------------ ( Bottleneck / Context Vector ) ------------------

   +-----------------------------+
   |        Encoder Stack        | (N Layers)
   |  +-----------------------+  |
   |  | Position-wise FFNN    |  |
   |  +-----------^-----------+  |
   |              |              |
   |  +-----------+-----------+  |
   |  | Multi-Head Attention  |  | (Bidirectional)
   |  +-----------^-----------+  |
   +--------------+--------------+
                 ^
                 |
      [ Input Embed + Positional ]

<<< Detailed Multi-Head Attention Mechanism >>>

[Input X] --> [Wq, Wk, Wv] --> [Q, K, V split into H heads]
     --> [Dot-product Attention for each head]
     --> [Concat results] --> [Wo Linear] --> [Output]
```

#### 3. 심층 동작 원리: Scaled Dot-Product Attention
트랜스포머의 심장인 셀프 어텐션은 다음의 수식으로 정의됩니다:
$$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $$
1.  **Dot Product ($QK^T$)**: Query와 Key의 유사도를 구합니다.
2.  **Scaling ($\sqrt{d_k}$)**: 차원이 커질수록 내적 값이 커져 Softmax의 기울기가 소실되는 것을 방지하기 위해 정규화합니다.
3.  **Softmax**: 가중치의 합이 1이 되도록 확률 분포를 생성합니다.
4.  **Value Weighted Sum**: 계산된 가중치를 Value에 곱해 최종 문맥 벡터를 생성합니다.

#### 4. 실무 수준의 PyTorch 구현 코드 (Production Grade)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    """
    고성능 연산을 위해 최적화된 Multi-Head Attention 모듈
    """
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads

        # Q, K, V 선형 변환을 하나의 행렬로 결합하여 연산 효율 극대화
        self.qkv_linear = nn.Linear(d_model, d_model * 3)
        self.output_linear = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.shape
        
        # 1. Linear Projection (batch, seq, 3 * d_model)
        qkv = self.qkv_linear(x)
        
        # 2. Reshape and Split Heads (batch, n_heads, seq, d_k)
        qkv = qkv.reshape(batch_size, seq_len, 3, self.n_heads, self.d_k)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]

        # 3. Scaled Dot-Product Attention
        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.d_k ** 0.5)
        
        if mask is not None:
            # Masking (Future Look-ahead 방지 또는 Padding 처리)
            scores = scores.masked_fill(mask == 0, -1e9)
        
        attn_weights = F.softmax(scores, dim=-1)
        
        # 4. Context Vector Calculation
        context = torch.matmul(attn_weights, v) # (batch, n_heads, seq, d_k)
        
        # 5. Concat and Final Projection
        context = context.permute(0, 2, 1, 3).reshape(batch_size, seq_len, self.d_model)
        return self.output_linear(context)

class PositionalEncoding(nn.Module):
    """
    Sine/Cosine 함수 기반의 절대 위치 정보를 주입
    """
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-torch.log(torch.tensor(10000.0)) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, :x.size(1)]
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. RNN vs CNN vs Transformer 비교 분석

| 비교 항목 | RNN (Recurrent) | CNN (Convolutional) | Transformer (Attention) |
| :--- | :--- | :--- | :--- |
| **순차 연산 복잡도** | $O(N)$ (병렬화 불가) | $O(1)$ | $O(1)$ |
| **최대 경로 길이** | $O(N)$ (기울기 소실) | $O(\log_k N)$ | $O(1)$ (상시 전역 연결) |
| **파라미터 효율성** | 높음 (가중치 공유) | 높음 (로컬 윈도우) | 보통 (Attention Map 생성) |
| **긴 문장 처리** | 취약 | 보통 | **매우 우수** |
| **주요 한계점** | 장기 의존성 문제 | 고정된 수용 영역(Receptive Field) | $O(N^2)$ 메모리 복잡도 |

#### 2. 과목 융합 관점 분석: 시스템 아키텍처 및 H/W
- **H/W 가속 (NVIDIA Tensor Core)**: 트랜스포머의 핵심 연산은 대형 행렬 곱셈(GEMM)입니다. 이는 NVIDIA GPU의 Tensor Core 유닛에 최적화되어 있어, 부동 소수점 연산 효율이 극대화됩니다.
- **분산 학습 전략 (Data/Model Parallelism)**: 트랜스포머는 그 거대한 크기 때문에 단일 기기 학습이 불가능합니다. OS와 네트워크 레벨에서 **ZeRO(Zero Redundancy Optimizer)** 기술을 활용하여 파라미터, 기울기, 옵티마이저 상태를 노드 간에 효율적으로 분산하는 전략이 필수적입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)
- **시나리오 1: 제한된 자원의 모바일 기기 내 언어 모델 배포**
  - 상황: VRAM이 4GB 미만인 환경에서 7B 모델 구동 요청.
  - 판단: 트랜스포머의 $O(N^2)$ 어텐션 맵은 메모리 부족을 유발합니다. 기술사는 **Grouped-Query Attention(GQA)** 또는 **Flash Attention**을 적용하여 메모리 오버헤드를 줄이고, 4-bit 양자화(Quantization)를 통해 가중치 크기를 최소화하는 전략을 수립해야 합니다.
- **시나리오 2: 초장문(100k+ 토큰) 문서 요약 시스템 구축**
  - 상황: 법률 문서 수천 페이지를 한 번에 처리해야 함.
  - 판단: 표준 트랜스포머는 불가능합니다. 기술사는 전역 어텐션 대신 **Sliding Window Attention** 또는 **Sparse Attention** 기반의 모델(예: Longformer, BigBird)을 도입하여 연산 복잡도를 선형($O(N)$)으로 낮추어야 합니다.

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] **데이터 품질**: 트랜스포머는 '데이터 아사(Data Hungry)' 성향이 강하므로 충분한 말뭉치가 확보되었는가?
- [ ] **학습 안정성**: Warm-up 단계와 Weight Decay 전략이 하이퍼파라미터에 포함되었는가?
- [ ] **서빙 오버헤드**: 자동 회귀적(Autoregressive) 생성 방식의 지연 시간(Latency)을 해결하기 위한 KV 캐싱이 구현되었는가?

#### 3. 안티패턴 (Anti-patterns)
- **무분별한 모델 확장**: 비즈니스 요구사항에 비해 지나치게 큰 파라미터 모델을 선택하여 운영 비용(OpEx)을 폭증시키는 사례.
- **Fine-tuning 데이터 편향**: 사전 학습된 거대 지식을 무시하고 좁은 범위의 데이터로만 미세 조정하여 모델의 일반화 능력을 파괴하는 행위.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- **정량적**: RNN 대비 학습 시간 10배 이상 단축, 번역 품질(BLEU Score) 20% 이상 향상.
- **정성적**: 단일 아키텍처로 멀티모달(텍스트, 이미지, 비디오) 통합 학습 기반 마련, AI 개발 생산성 혁명.

#### 2. 미래 전망
향후 트랜스포머는 연산 효율을 개선한 **Linear Attention** 구조와, 외부 메모리를 동적으로 활용하는 **RAG(Retrieval-Augmented Generation)** 기술과 결합하여 더욱 거대해질 것입니다. 또한, 인간의 뇌 구조를 더 모사한 **Spiking Transformer**나 효율성을 극대화한 **Mamba(State Space Model)**와 같은 새로운 패러다임과 경쟁 및 융합하며 진화할 것입니다.

#### 3. 참고 표준
- **W3C AI 관련 표준화**: LLM 응답의 투명성 및 상호운용성 가이드.
- **NIST AI RMF**: 인공지능 위험 관리 프레임워크 준수 필요.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[Self-Attention](@/studynotes/10_ai/01_dl/transformer_architecture.md)**: 문장 내 단어 간의 전역적 상관관계를 계산하는 핵심 알고리즘.
- **[LLM (Large Language Model)](@/studynotes/10_ai/01_dl/rag.md)**: 트랜스포머를 기반으로 구축된 거대 지능 모델군.
- **[ViT (Vision Transformer)](@/studynotes/10_ai/01_dl/transformer_architecture.md)**: 이미지를 패치 단위로 쪼개어 트랜스포머로 처리하는 컴퓨터 비전 기술.
- **[Flash Attention](@/studynotes/10_ai/01_dl/transformer_architecture.md)**: 메모리 계층 구조를 활용하여 어텐션 연산을 가속화하는 최신 기법.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **눈이 여러 개인 선생님**: 트랜스포머는 책을 읽을 때 문장 앞뒤를 한꺼번에 다 볼 수 있는 아주 많은 눈을 가진 똑똑한 선생님과 같아요.
2. **중요한 것 골라내기**: 수많은 글자 중에서 정답을 찾는 데 꼭 필요한 단어가 무엇인지 '반짝!' 하고 찾아내는 능력이 아주 뛰어나답니다.
3. **엄청나게 빠른 공부**: 한 글자씩 읽지 않고 전체 페이지를 사진 찍듯 한꺼번에 공부해서, 세상의 모든 지식을 아주 빠르게 배울 수 있어요.
