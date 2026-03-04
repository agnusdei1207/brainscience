+++
title = "트랜스포머 아키텍처 (Transformer Architecture)"
date = 2024-05-18
description = "현대 자연어 처리 및 거대 언어 모델(LLM)의 핵심인 트랜스포머의 Self-Attention 메커니즘, 아키텍처 구조 및 PyTorch 구현 상세 분석"
weight = 10
+++

# 트랜스포머 아키텍처 심층 분석 (Transformer Architecture)

## 1. 패러다임의 전환: Attention Is All You Need
2017년 Google Brain 팀에서 발표한 트랜스포머(Transformer) 모델은 기존 순차적 데이터 처리를 지배하던 RNN(Recurrent Neural Network), LSTM의 한계를 근본적으로 돌파한 혁명적인 아키텍처입니다. RNN은 시퀀스를 순차적으로 처리해야 하므로 병렬 처리가 불가능하고, 긴 문장에서는 정보가 유실되는 장기 의존성(Long-term Dependency) 문제가 있었습니다.

트랜스포머는 순환(Recurrence) 구조를 완전히 배제하고, 오직 **어텐션(Attention) 메커니즘**만을 사용하여 문장 내의 모든 단어 간의 관계를 한 번에(병렬로) 파악합니다. 이를 통해 학습 속도를 비약적으로 향상시켰으며, GPT, BERT와 같은 거대 언어 모델(LLM)의 기초를 마련했습니다.

## 2. 트랜스포머의 전체 아키텍처 및 내부 구조
트랜스포머는 크게 **인코더(Encoder)**와 **디코더(Decoder)** 스택으로 구성됩니다. 각 블록은 여러 개의 동일한 레이어로 쌓여 있습니다. (예: 논문에서는 N=6 사용)

```ascii
[ Transformer Encoder-Decoder Architecture ]

      [출력 단어 확률 분포 (Probabilities)]
                 ^
                 |  (Softmax & Linear)
   +---------------------------+
   |        디코더 (Decoder)     |
   |  +---------------------+  |
   |  | Feed Forward Neural |  |
   |  | Network (FFNN)      |  |
   |  +---------------------+  |
   |            ^              |
   |  +---------------------+  |<--- (Encoder의 출력 K, V 전달)
   |  | Encoder-Decoder     |  |
   |  | Multi-Head Attention|  |
   |  +---------------------+  |
   |            ^              |
   |  +---------------------+  |
   |  | Masked Multi-Head   |  |
   |  | Self-Attention      |  |
   |  +---------------------+  |
   +---------------------------+
                 ^
                 | (Target Sequence)

---------------------------------------------

   +---------------------------+
   |        인코더 (Encoder)     | (N개 스택)
   |  +---------------------+  |
   |  | Feed Forward Neural |  |
   |  | Network (FFNN)      |  |
   |  +---------------------+  |
   |            ^              |
   |  +---------------------+  |
   |  | Multi-Head          |  |
   |  | Self-Attention      |  |
   |  +---------------------+  |
   +---------------------------+
                 ^
                 |
      [입력 임베딩 + Positional Encoding]
```
*(주의: 각 Sub-layer마다 Add & Norm(Residual Connection 및 Layer Normalization)이 포함되어 학습 안정성을 보장합니다.)*

## 3. 핵심 메커니즘: 셀프 어텐션 (Self-Attention)
셀프 어텐션은 "현재 단어가 문장 내의 다른 모든 단어들과 얼마나 연관되어 있는가?"를 계산하는 메커니즘입니다.

1. **Q, K, V의 생성**: 입력 벡터로부터 세 개의 벡터, 즉 **Query(질의)**, **Key(키)**, **Value(값)**를 행렬 곱 연산을 통해 생성합니다.
2. **어텐션 스코어 계산**: 특정 단어의 Query와 다른 모든 단어의 Key를 내적(Dot Product)하여 연관성을 계산합니다. 이 값이 클수록 두 단어의 연관성이 높습니다.
3. **스케일링 및 소프트맥스**: 내적 값을 Key 차원 수의 제곱근($\sqrt{d_k}$)으로 나누어 스케일링(Scaled Dot-Product)한 후, Softmax 함수를 취해 확률값(0~1)으로 변환합니다.
4. **가중합 (Weighted Sum)**: 계산된 Softmax 가중치를 Value 벡터에 곱한 후 모두 더하여 최종 출력 벡터를 만듭니다.

수식: $ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $

### 멀티 헤드 어텐션 (Multi-Head Attention)
단일 어텐션 대신 Q, K, V를 여러 개(Head)로 나누어 병렬로 어텐션을 수행합니다. 이를 통해 모델은 문장의 의미적, 문법적, 문맥적 관계 등 다양한 관점에서의 표현(Representation)을 동시에 학습할 수 있습니다.

## 4. 위치 인코딩 (Positional Encoding)
트랜스포머는 RNN과 달리 단어를 순차적으로 받지 않으므로 단어의 위치(순서) 정보를 알 수 없습니다. 이를 보완하기 위해 임베딩 벡터에 사인(Sine) 및 코사인(Cosine) 함수 기반의 주기적인 값(Positional Encoding)을 더해주어, 모델이 단어의 절대적 및 상대적 위치를 인식할 수 있게 합니다.

## 5. PyTorch를 이용한 Self-Attention 구현 (Production-Level)
딥러닝 실무에서 사용되는 형태의 Scaled Dot-Product Attention 및 Multi-Head Attention의 축약된 PyTorch 코드입니다.

```python
import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Q, K, V를 위한 선형 변환 행렬
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        
        # 최종 출력을 위한 선형 변환
        self.W_o = nn.Linear(d_model, d_model)
        
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        # 1. Q * K^T 연산
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        # 2. Masking (옵션, 디코더나 패딩 처리에 사용)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
            
        # 3. Softmax
        attention_weights = torch.softmax(scores, dim=-1)
        
        # 4. Attention Weights * V 연산
        output = torch.matmul(attention_weights, V)
        return output, attention_weights

    def forward(self, q, k, v, mask=None):
        batch_size = q.size(0)
        
        # 선형 변환 후 헤드 수만큼 분할 (batch_size, num_heads, seq_len, d_k)
        Q = self.W_q(q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(k).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(v).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # 어텐션 수행
        attn_output, _ = self.scaled_dot_product_attention(Q, K, V, mask)
        
        # 분할된 헤드를 다시 결합 (Concat)
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        
        # 최종 선형 레이어 통과
        return self.W_o(attn_output)

# 테스트 코드
# d_model: 임베딩 차원수=512, num_heads: 8
mha = MultiHeadAttention(d_model=512, num_heads=8)
# batch=32, seq_len=10, d_model=512 크기의 더미 입력
dummy_input = torch.randn(32, 10, 512) 
output = mha(dummy_input, dummy_input, dummy_input) # Self-Attention (Q=K=V)
print(f"출력 텐서 형태: {output.shape}") # torch.Size([32, 10, 512])
```

## 6. 결론
트랜스포머는 NLP 분야를 넘어 컴퓨터 비전(Vision Transformer, ViT), 음성 인식, 그리고 단백질 구조 예측(AlphaFold) 등 AI의 모든 분야로 확장되는 파운데이션 모델(Foundation Model)의 코어 엔진이 되었습니다. 개발자 및 AI 엔지니어는 트랜스포머의 병렬 처리 특성과 VRAM 최적화(KV Cache, Flash Attention 등)를 깊이 이해해야만 최신 모델을 실무 환경에 효과적으로 서빙하고 파인튜닝할 수 있습니다.
