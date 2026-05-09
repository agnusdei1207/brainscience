+++
weight = 434
title = "434. 딥러닝 트랜스포머 LLM 자기회귀 어텐션 메커니즘 (LLM / Transformer)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 트랜스포머(Transformer) 아키텍처는 셀프 어텐션(Self-Attention) 메커니즘으로 시퀀스의 모든 위치 간 의존 관계를 병렬 계산하여 RNN의 순차 처리 한계를 극복하고, LLM(Large Language Model)은 트랜스포머 기반 자기회귀(Autoregressive) 사전 훈련으로 범용 언어 이해·생성 능력을 획득한다.
> 2. **가치**: Attention Is All You Need(Vaswani et al., 2017)로 시작된 트랜스포머 혁명은 GPT·BERT·LLaMA·Claude 등 수십억~수조 파라미터 모델로 진화하여 NLP 전 영역에서 인간 수준에 도달했다.
> 3. **판단 포인트**: 셀프 어텐션의 O(n²) 계산 복잡도가 긴 문맥(Long Context) 처리의 병목이며, Sparse Attention·Flash Attention·MQA(Multi-Query Attention)가 핵심 효율화 기술이다.

## Ⅰ. 개요 및 필요성

순환 신경망(RNN/LSTM)은 순차적 처리로 긴 시퀀스의 장기 의존성(Long-term Dependency) 포착이 어렵고, 병렬화가 불가능했다. 트랜스포머는 어텐션 메커니즘으로 시퀀스의 모든 위치를 동시에 비교하여 병렬 처리가 가능하고 장기 의존성을 효과적으로 포착한다. GPT-4는 1조+ 파라미터 추정으로 범용 AI 능력의 새 기준을 제시했다.

📢 **섹션 요약 비유**: 셀프 어텐션은 문장 전체를 동시에 읽는 능력 — "그(he)"가 누구를 가리키는지 문장 전체를 한눈에 보고 결정한다.

## Ⅱ. 아키텍처 및 핵심 원리

```
트랜스포머 아키텍처 (Attention Is All You Need):
  Input Embedding + Positional Encoding
          ↓
  Multi-Head Self-Attention
  (Q: Query, K: Key, V: Value)
  Attention(Q,K,V) = softmax(QK^T / √d_k) · V
          ↓
  Feed-Forward Network (per position)
          ↓
  Layer Normalization + Residual Connection
          ↓ (N번 반복)
  Output

자기회귀 LLM (GPT 계열):
  입력: "안녕" → 다음 토큰 예측: "하세요" → "저는" → "AI" → ...
  훈련: 다음 토큰 예측 손실 최소화 (Causal Language Modeling)
```

| 모델 | 구조 | 파라미터 | 주요 용도 |
|:---|:---|:---|:---|
| BERT | Encoder-only | 340M | 이해·분류·NER |
| GPT-4 | Decoder-only | ~1T(추정) | 생성·대화·코드 |
| T5 | Encoder-Decoder | 11B | 번역·요약 |
| LLaMA 3 | Decoder-only | 8B~70B | 오픈소스 경쟁력 |

📢 **섹션 요약 비유**: Multi-Head Attention은 여러 관점에서 문장 읽기 — 한 head는 문법, 다른 head는 의미, 또 다른 head는 감정 관계를 동시에 본다.

## Ⅲ. 비교 및 연결

Flash Attention: 어텐션 계산을 GPU HBM-SRAM 간 I/O 최소화로 최적화 — 기존 대비 4~20배 속도 향상, 메모리 O(n²)→O(n) 감소. KV Cache: 디코딩 시 이전 토큰의 Key-Value를 캐싱하여 재계산 방지 → 추론 가속.

📢 **섹션 요약 비유**: KV Cache는 이미 계산한 답을 칠판에 써두기 — 매번 처음부터 계산하는 대신, 이전 결과를 재활용하여 빠르게 다음 단어를 예측한다.

## Ⅳ. 실무 적용 및 기술사 판단

**의사결정 포인트**:
- LLM 서빙 지연: KV Cache + Flash Attention + vLLM(PagedAttention)
- 파인튜닝 효율: LoRA/QLoRA(저차원 가중치 업데이트로 VRAM 90% 절감)
- 프라이버시 요건: 온프레미스 LLaMA 3 배포 vs 클라우드 API
- 컨텍스트 길이: GPT-4 Turbo 128K, Gemini 1M 토큰 → 장문서 분석 가능

📢 **섹션 요약 비유**: vLLM PagedAttention은 가상 메모리 관리 — KV Cache를 페이지(조각)으로 나눠 GPU 메모리를 훨씬 효율적으로 사용한다.

## Ⅴ. 기대효과 및 결론

트랜스포머/LLM은 NLP를 넘어 코드 생성·과학적 발견·멀티모달 이해로 확장하며 AI의 새 시대를 열었다. 연산 비용·환경 부담·할루시네이션(Hallucination)·편향이 현실적 한계이며, RAG·파인튜닝·RLHF·Constitutional AI가 품질 향상의 핵심 기법이다. 효율화(LoRA, FlashAttention, MoE)와 신뢰성(RAG, 그라운딩)이 LLM 실용화의 두 축이다.

📢 **섹션 요약 비유**: LLM은 인류의 모든 글을 읽고 자란 아이 — 엄청난 지식을 가졌지만, 실제로 경험하지 않은 것은 가끔 틀리게 말한다(할루시네이션).

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Self-Attention | 핵심 메커니즘 | 시퀀스 전 위치 간 의존 병렬 계산 |
| Flash Attention | 최적화 기술 | GPU I/O 효율화로 어텐션 가속 |
| KV Cache | 추론 최적화 | 이전 토큰 Key-Value 재사용 |
| LoRA | 파인튜닝 효율화 | 저차원 가중치 업데이트 |
| Hallucination | 핵심 문제 | LLM 부정확한 자신감 있는 생성 |

### 👶 어린이를 위한 3줄 비유 설명

1. 트랜스포머의 어텐션은 문장 전체 눈 — 어떤 단어가 어떤 단어와 관련 있는지 한 번에 모두 확인해.
2. LLM은 책을 수조 권 읽은 독서왕 — 엄청나게 많이 읽었으니 질문에 잘 답하지만, 가끔 틀리게 기억하기도 해(할루시네이션).
3. LoRA는 LLM의 스티커 학습 — 전체를 다시 배우는 대신, 필요한 부분에만 스티커(저차원 가중치)를 붙여서 새 기술을 빠르게 익혀.
