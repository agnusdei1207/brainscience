+++
weight = 91
title = "91. Transformer/BERT (트랜스포머/양방향 인코더 표현)"
description = "Transformer의 Self-Attention 메커니즘, BERT의 사전 학습 및 파인튜닝, 자연어 처리에서의 혁신"
date = "2026-04-05"
[taxonomies]
tags = ["Transformer", "BERT", "Self-Attention", "어텐션", "사전학습", "트랜스포머", "자연어처리"]
categories = ["studynote-bigdata"]
+++

# Transformer/BERT (트랜스포머/양방향 인코더 표현)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: Transformer는 2017년 Vaswani et al.이 제안한 모델로, Self-Attention 메커니즘을 통해 시퀀스의 모든 위치 간 의존성을 병렬적으로 계산할 수 있어, RNN의 순차적 처리 한계를 극복한 것이다.
> 2. **가치**: BERT는 Transformer의 인코더 부분을 활용하여 양방향(Bidirectional) 문맥을 동시에 고려하는 사전 학습 모델로, 다양한NLPタスクで最高 성능을 달성하고 있다.
> 3. **융합**: BERT 이후RoBERTa, ALBERT, ELECTRA 등 다수의 BERT 변형 모델이 등장했으며, GPT 계열과 함께 현대 NLP의 사실상의 표준 기반 역할을 하고 있다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

Transformer는 2017년 Google's论文"Attention Is All You Need"에서 소개되었으며, NLP 분야에Revolution을 가져왔다. 그전까지 RNN(특히 LSTM/GRU)이 순서 데이터 처리의 표준이었지만, Transformer는 Attention 메커니즘만으로 구성되어 RNN을 完全하게替代했다.

왜 Transformer가 중요한가? RNN의 가장 큰 문제점은 시퀀스가 길어질수록 먼 위치의 정보를 전달하기 어려워지는"장기 의존성(Long-term Dependency)"문제와"순차적 처리"로 인한 병렬화 한계였다. Transformer는 이러한 제약을 Self-Attention으로 완전히 해결했다.

```text
[RNN vs Transformer: 처리 방식 비교]

[RNN (순차적 처리)]
  시간 t=1: x₁ 처리 → h₁
                    ↓
  시간 t=2: x₂ + h₁ 처리 → h₂
                    ↓
  시간 t=3: x₃ + h₂ 처리 → h₃
                    ↓
  ...

  문제: t=1의 정보가 h₃에 전달되려면 2단계 거치는 동안 손실 가능
       병렬 처리 불가능 (순서 의존)

[Transformer (병렬 처리)]
  모든 시간 단계 x₁, x₂, x₃, ... xₙ을 동시에 처리
       │
  ┌────┴────┐
  │         │
  ▼         ▼
  Self-Attention: 모든 위치 간 관계를 동시에 계산

  병렬 처리 가능 → RNN보다 수십~수백 배 빠른 훈련
  모든 위치 간 직접 연결 → 장기 의존성 문제 해결
```

> 📢 **섹션 요약 비유**: Transformer는犹如효율적인회의진행방식과 유사하다. RNN이 한 사람씩轮流발언하면서 의견을 전달한다면(순차적), Transformer는 모든参会자가 동시에 discussion하고(병렬 처리),누가무엇을 말했는지 모두가即时 확인하는(모든 위치 간 직접 attention) 것과 같다. 훨씬 효율적이고 빠르며,情報の損失도 없다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 2.1 Self-Attention 메커니즘

Self-Attention은 입력 시퀀스 내의 모든 위치들이 서로 어떻게 관련되어 있는지를 계산하는 메커니즘이다.

```text
[Self-Attention 계산 과정]

입력 시퀀스: "The cat sat on the mat"

각 단어에 대해 Query(Q), Key(K), Value(V) 벡터를 생성:

  Q = 입력 × W_Q
  K = 입력 × W_K
  V = 입력 × W_V

Attention Score 계산:
  Attention(Q, K, V) = softmax(QKᵀ / √d_k) × V

  여기서:
  - QKᵀ: Query와 Key의 유사도 (dot product)
  - √d_k: 스케일링 (벡터 차원 정규화)
  - softmax: 확률적으로 변환
  - V: 실제注意力가 적용될 값

[Multi-Head Attention]

여러 개의 Attention을 병렬로 수행:

  MultiHead = Concat(head₁, head₂, ..., headₕ) × W_O

  각 head_i = Attention(QW_Qᵢ, KW_Kᵢ, VW_Vᵢ)

  이점:
  - 다양한 종류의 관계를 동시에 포착
  - 예: head₁은 문법 관계, head₂는 의미 관계 등
```

### 2.2 Transformer 구조

Transformer는 인코더(Encoder)와 디코더(Decoder)로 구성된다.

```text
[Transformer 아키텍처]

인코더 (N=6 레이어):
  입력 임베딩 + 위치 인코딩
       │
  ┌────┴────┐
  │ Encoder │
  │  Layer  │ × N
  │ Multi-Head │
  │ Attention │
  │   +   FFN  │
  └────┬────┘
       │
  디코더 입력 (Shifted Right)
       │
  ┌────┴────┐
  │ Decoder │
  │  Layer  │ × N
  │ Masked  │
  │ Multi-Head │
  │ Attention │
  │   +  Encoder-  │
  │   Decoder      │
  │ Attention + FFN│
  └────┬────┘
       │
  선형 계층 + Softmax
       │
     출력
```

**위치 인코딩 (Positional Encoding)**
Transformer는 순환 구조가 없으므로, 단어의 위치 정보를 추가해야 한다. Sinusoidal 함수를 사용하여 각 위치에 고유한 인코딩을 생성한다.

### 2.3 BERT: Bidirectional Encoder Representations from Transformers

BERT는 Transformer의 인코더만을 사용하며, 양방향(Bidirectional) 문맥을 학습하는 것이 핵심이다.

```text
[BERT vs 기존 접근법]

기존 언어 모델 (单向):
  - Left-to-Right: "I love you" 모델이 좌→우만 예측
  - GPT: 이전 단어들만 고려하여 다음 단어 예측
  이 경우 오른쪽 문맥이 누락됨

BERT (双向):
  - 양방향 문맥을 동시에 고려
  - "The cat sat on the [MASK]" → [MASK]를 양방향에서 추론
  → 더 풍부한 표현 학습 가능

[BERT의 사전 학습]

1. Masked Language Model (MLM):
  - 입력의 15% 토큰을 [MASK]로 치환
  - 주변 문맥(양방향)에서 [MASK] 토큰 예측
  예: "The cat [MASK] on the mat" → "sat"

2. Next Sentence Prediction (NSP):
  - 두 문장이 주어졌을 때 연속적인지 판단
  예: "The cat sat on the mat." + "It was fluffy."
  → IsNext (연속) 또는 NotNext (비연속)
```

### 2.4 BERT의 파인튜닝 (Fine-tuning)

사전 학습된 BERT를 특정タスクに適用するには、이른 파인튜닝 과정을 거친다.

```python
# Hugging Face Transformers를 활용한 BERT 파인튜닝
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 사전 학습된 BERT 로드
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# 텍스트 전처리
inputs = tokenizer("This is great!", return_tensors="pt")

# 파인튜닝
outputs = model(**inputs)
logits = outputs.logits
```

> 📢 **섹션 요약 비유**: BERT의 사전 학습과 파인튜닝은犹如대학 교육과 전문 과정의 관계와 유사하다. 대학에서 다양한 과목을 학습하면(사전 학습) 기본적인知的能力과 지식이 쌓인다. 이후 전문 과정(의료, 법률 등)에서 파인튜닝하면 그 분야에 즉시 적용 가능한 전문가가 된다. BERT도 다양한 тек스트에서 기본 언어 이해 능력을 학습한 후, 특정タスクに맞게微調整하여 적용하는 것이다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

BERT 이후 등장한 주요 변형 모델들을 비교해보자.

| 모델 | 개발사 | 주요创新 | 크기 |
|:---|:---|:---|:---|
| **BERT** | Google | 양방향, MLM + NSP | Base: 110M, Large: 340M |
| **RoBERTa** | Facebook | NSP 제거, 더 많은 데이터, 긴 훈련 | Base: 125M, Large: 355M |
| **ALBERT** | Google | 파라미터 공유,Embedding分解 | Base: 12M, Large: 235M |
| **ELECTRA** | Google | Replaced Token Detection (RTD) | Base: 14M, Large: 335M |
| **DistilBERT** | HuggingFace | 지식 증류, 60% 빠른推断 | 66M |
| **TinyBERT** | Huawei |BERT의 7.5배 작은 버전 | 14M |

```text
[BERT vs GPT 차이]

BERT (인코더 Only):
  - 양방향 문맥 이해 (MLM)
  - 주로 분류, QA, NER 등에 강점
  - 입력 시퀀스 전체를 양방향으로Attention

GPT (디코더 Only):
  - 단방향 (이전 토큰들만 고려)
  - 주로 텍스트 생성에 강점
  - autoregressive 생성

T5 (인코더-디코더):
  - 모든 작업을 텍스트-투-텍스트로 변환
  - 범용적但是 복잡한部

[Transformer vs RNN/LSTM]

장점:
  ✓ 병렬 처리로 훈련 속도大幅 향상
  ✓ 장기 의존성 문제 해결
  ✓ 더 나은 성능 (대부분의 NLPタスクで)

단점:
  ✗ 시퀀스 길이에 비례하는 메모리 사용 (O(N²))
  ✗ 위치 정보를 명시적으로注入해야 함
  ✗ RNN보다 많은 데이터 필요
```

> 📢 **섹션 요약 비유**: BERT와 GPT의 관계는犹如비밀번호破解의두 가지 전략과 유사하다. BERT는 전체 비밀번호를 양방향에서 동시에推测하려는 것이고, GPT는 첫 글자부터順次に猜测해 가는 것이다. 전자가 대부분의 경우 더 빠르지만,后者는 문장을生成할 때(텍스트 생성) 더 자연스럽다.

---

### Ⅳ. 실무 적용 및 한계 (Application & Limitation)

**주요 적용 분야:**

1. **텍스트 분류 (Text Classification)**
   - 감성 분석, 스팸 탐지, 토픽 분류
   - BERT 파인튜닝으로 SOTA 성능 달성

2. **질문 답변 (Question Answering)**
   - SQuAD, Natural Questions 등 데이터셋에서 인간 수준 초과

3. **명명된 개체 인식 (NER)**
   - 사람, 장소, 조직 등의 개체 추출

4. **텍스트 생성 ( GPT와 결합)**
   - 대화 시스템, 요약, 번역 등

**한계점:**

1. **계산 비용**: 매우 큰 모델(수십억 파라미터)로 훈련/동작에 상당한 GPU 메모리와 연산 필요

2. **긴 시퀀스 처리 한계**: Self-Attention의 이차 복잡도로 인해 긴 시퀀스 처리가 어려움 (단축을工夫로 해결하려는 연구 활발)

3. **프라이버시 문제**: 대규모 텍스트 데이터로 사전 학습 시 데이터 내 개인 정보 포함 가능성

4. **역幻觉 (Hallucination)**: 생성 모델에서 사실과 다른 내용을 생성하는 경향

```python
# Hugging Face로 BERT 기반 감성 분석 파이프라인
from transformers import pipeline

# 사전 훈련된 감성 분석 모델
classifier = pipeline("sentiment-analysis")

# 텍스트 분류
result = classifier("I love using BERT for NLP tasks!")
# [{'label': 'POSITIVE', 'score': 0.99}]
```

> 📢 **섹션 요약 비유**: Transformer/BERT는犹如万能調理器와 같다. 기본 원리는 간단하지만(Attention),それを大規模な데이터로 훈련하면(사전 학습) 다양한 요리에 활용할 수 있다(다양한NLPタスク). 그러나万能調理기도 크기가 크면(큰 모델) 설치 비용이 많이 들고(계산 비용), 처음 사용시 조리법을 찾는 데 시간이 걸린다(파인튜닝 필요).

---

### Ⅴ. 요약 및 전망 (Summary & Outlook)

Transformer는 현대 NLP의基石로서, 2017년 등장 이후 불과 数년 만에 거의 모든NLPタスク를Revolutionized했다. BERT는 사전 학습+파인튜닝이라는Paradigm을 정립하여, 레이블된 데이터가 부족한 상황에서도 전이 학습이 가능하게 했다.

앞으로의 전망으로는, 더 효율적인Transformervariant 개발 (Longformer, BigBird, Reformer 등), 효율적인 모델 크기 축소 (知識 증류, 양자화), Multimodal 학습 (텍스트+이미지+오디오), 그리고 Foundation Models로서의 발전 등이 기대된다.

결론적으로, Transformer/BERT는 NLP의Past, Present를代表了가며, Near Future에도 その 영향は続くものと考えられる.

---

**References**
- Vaswani, A., et al. (2017). Attention Is All You Need. NIPS.
- Devlin, J., et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. NAACL.
- Rogers, A., et al. (2020). A Primer in BERTology: What we know about how BERT works. Transactions of the Association for Computational Linguistics.
