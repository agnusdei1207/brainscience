+++
weight = 198
title = "198. 지식 증류 (Knowledge Distillation) 소프트 타겟 확률 분포 모방"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: 지식 증류(Knowledge Distillation)는 대형 교사 모델(Teacher Model)의 확률 분포(소프트 타겟)를 소형 학생 모델(Student Model)이 모방하여, 크기를 줄이면서도 성능을 최대한 유지하는 경량화 기법이다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

대형 언어 모델(LLM)과 대형 비전 모델은 추론 비용이 막대하여 엣지 디바이스나 실시간 서비스에 배포하기 어렵다.

| 모델 | 파라미터 수 | 추론 메모리 | 추론 속도 |
|:---|:---|:---|:---|
| GPT-3 | 175B | 350GB | 수초/요청 |
| GPT-4 (추정) | 1T+ | 2TB+ | 수초/요청 |
| BERT-base | 110M | 440MB | 100ms |
| DistilBERT | 66M (-40%) | 264MB | 60ms (-40%) |
| MobileNet V3 | 5.4M | 22MB | 10ms |

---

## 2. 구성요소

| 기법 | 방법 | 특징 |
|:---|:---|:---|
| 지식 증류 | 교사→학생 지식 전이 | 작은 모델로 높은 성능 |
| 양자화(Quantization) | 정밀도 감소 (FP32→INT8) | 구현 쉬움, 정확도 일부 손실 |
| 가지치기(Pruning) | 불필요 파라미터 제거 | 구조적/비구조적 선택 |
| NAS (Neural Architecture Search) | 최적 아키텍처 탐색 | 높은 계산 비용 |

---

## 3. 구조 및 원리

**핵심 조건**: 지식 증류 (Knowledge Distillation) 소프트 타겟 확률 분포 모방은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 사례 | 교사 | 학생 | 감소율 | 성능 유지 |
|:---|:---|:---|:---|:---|
| DistilBERT | BERT-base | DistilBERT | 40% 파라미터 | 97% GLUE |
| TinyBERT | BERT-base | TinyBERT | 87% 파라미터 | 96% GLUE |
| DistilGPT-2 | GPT-2 | DistilGPT-2 | 33% 파라미터 | 유사 생성 품질 |
| MobileNet → ??? | EfficientNet | MobileNet | 96% 파라미터 | 90% Top-1 |
| ResNet → 경량화 | ResNet-50 | ResNet-18 + KD | 75% 파라미터 | 98% 성능 |

```
교사와 학생이 동일 아키텍처인 경우

Self-KD (Self-Knowledge Distillation):
  에포크 초기 모델 → 교사 역할
  현재 학습 중 모델 → 학생 역할

Born Again Networks (BAN):
  학습 완료 모델 → 교사
  동일 크기 새 모델 → 학생
  → 앙상블 없이 앙상블 효과
```

| 항목 | 지식 증류 | 전이 학습 (Fine-tuning) |
|:---|:---|:---|
| 목표 | 모델 경량화 | 새 태스크 적응 |
| 교사 역할 | 소프트 레이블 제공 | 초기 가중치 제공 |
| 학생 크기 | 교사보다 작음 | 교사와 동일 또는 더 작음 |
| 학습 데이터 | 동일 태스크 데이터 | 새 태스크 데이터 |
| 출력 | 경량 추론 모델 | 새 태스크 특화 모델 |

---

## 4. 비교 및 연결

| 전략 | 파라미터 감소 | 정확도 손실 | 구현 난이도 | 적합 시나리오 |
|:---|:---|:---|:---|:---|
| 지식 증류 | 40~90% | 낮음 (1~5%) | 중간 | 구조 변경 가능 시 |
| PTQ 양자화 | 0% (메모리만) | 낮음 (1~3%) | 쉬움 | 빠른 배포 필요 |
| QAT 양자화 | 0% (메모리만) | 최소 | 어려움 | 최고 품질 필요 |
| 구조적 가지치기 | 10~50% | 중간 | 어려움 | FLOP 감소 필요 |
| NAS | 60~95% | 최소 | 매우 어려움 | 장기 프로젝트 |

```python
import torch
import torch.nn.functional as F

def distillation_loss(student_logits, teacher_logits,
                      labels, T=4.0, alpha=0.7):
    """
    지식 증류 손실 함수
    Args:
        student_logits: 학생 모델 출력 (배치, 클래스)
        teacher_logits: 교사 모델 출력 (배치, 클래스)
        labels: 실제 정답 레이블
        T: 온도 매개변수
        alpha: 증류 손실 가중치
    """
    # 소프트 타겟 생성 (온도 T 적용)
    soft_teacher = F.softmax(teacher_logits / T, dim=-1)
    soft_student = F.log_softmax(student_logits / T, dim=-1)

    # 증류 손실 (KL Divergence) - T^2로 스케일링
    distill_loss = F.kl_div(soft_student, soft_teacher,
                            reduction='batchmean') * (T ** 2)

    # 하드 레이블 손실 (Cross Entropy)
    hard_loss = F.cross_entropy(student_logits, labels)

    # 최종 손실 조합
    return alpha * distill_loss + (1 - alpha) * hard_loss

# 학습 루프
teacher_model.eval()  # 교사는 고정 (그래디언트 없음)
for inputs, labels in dataloader:
    with torch.no_grad():
        teacher_logits = teacher_model(inputs)

    student_logits = student_model(inputs)
    loss = distillation_loss(student_logits, teacher_logits,
                             labels, T=4.0, alpha=0.7)
    loss.backward()
    optimizer.step()
```

| 판단 항목 | 지식 증류 선택 기준 |
|:---|:---|
| 엣지 디바이스 배포 | 구조 변경 가능하고 재학습 리소스 있을 때 |
| 빠른 경량화 필요 | PTQ 양자화 먼저 고려 (구현 쉬움) |
| 최고 성능 유지 | 피처 기반 증류 + QAT 양자화 조합 |
| 언어 모델 경량화 | DistilBERT/TinyBERT 사전학습 모델 활용 |

---

## 5. 실무 적용 및 판단

| 효과 | 수치 |
|:---|:---|
| 모델 크기 감소 | 40~90% |
| 추론 속도 향상 | 2~5배 |
| 메모리 사용 감소 | 40~90% |
| 성능 유지율 | 95~99% (태스크에 따라) |
| 배포 비용 감소 | 클라우드 추론 비용 50~80% 감소 |

```
지식 증류 발전 방향

1. LLM 증류 (Large Language Model Distillation)
   ├─ GPT-4 → GPT-3.5급 성능으로 증류
   └─ Alpaca: GPT-4 52K 샘플로 LLaMA 7B 파인튜닝

2. 멀티모달 증류 (Multimodal Distillation)
   └─ 텍스트+이미지 교사 → 경량 단일 모달 학생

3. Online Distillation
   └─ 교사 학습과 학생 학습 동시 진행 (코-학습)

4. Task-Agnostic Distillation
   └─ 태스크 무관하게 일반 표현 증류
      (DistilBERT, TinyBERT 방식)
```

지식 증류는 AI 모델의 엣지 배포와 실시간 서빙을 가능하게 하는 핵심 경량화 기법이다. 소프트 타겟이 하드 레이블 대비 더 풍부한 학습 신호를 제공하는 원리를 이해하고, 기술사 관점에서는 **3가지 증류 방식의 차이, 온도 매개변수의 역할, BERT → DistilBERT 같은 실제 적용 사례**를 명확히 설명할 수 있어야 한다.

```
Hard Label (전통 학습) vs Soft Target (지식 증류)

[분류 문제: 개, 고양이, 자동차]

Hard Label (원핫 인코딩):
  실제 정답: 개 → [1, 0, 0]
  → 클래스 간 관계 정보 없음
  → "개와 고양이가 자동차보다 유사하다"는 정보 손실

Soft Target (교사 모델 출력):
  교사 모델 확률: 개 → [0.7, 0.25, 0.05]
  → "개랑 고양이가 비슷함" 정보 포함!
  → 학생 모델이 더 풍부한 정보로 학습
```

```
지식 증류 학습 구조

교사 모델 (Teacher, 고정)
  입력 x → 소프트맥스(logits/T) → 소프트 타겟 q_T
                                      │
학생 모델 (Student, 학습 중)           │
  입력 x → 소프트맥스(logits/T) → q_S ↓
                                  KL Divergence 손실
                                  L_distill = KL(q_T || q_S)
  입력 x → 소프트맥스(logits/1) → 하드 예측
                                  L_ce = CrossEntropy(y, q_S)

최종 손실 함수:
  L_total = α × T² × L_distill + (1-α) × L_ce

  α: 증류 손실 가중치 (보통 0.5~0.9)
  T: 온도 매개변수 (보통 2~20)
  T²: 온도 스케일링 보정 (그래디언트 크기 정규화)
```

```
온도(T)에 따른 확률 분포 변화

원본 logits: [3.0, 0.5, -1.5]

T=1 (Hard, 기본):
  소프트맥스: [0.87, 0.12, 0.01]
  → 개 압도적 우세, 고양이/자동차 구분 어려움

T=5 (Soft):
  소프트맥스: [0.55, 0.35, 0.10]
  → 고양이와의 유사성 정보 드러남

T=10 (Very Soft):
  소프트맥스: [0.40, 0.38, 0.22]
  → 모든 클래스 관계 정보 최대 활용

T→∞:
  소프트맥스: [0.33, 0.33, 0.33]
  → 균등 분포 (정보 없음)

최적 T: 태스크와 교사 모델에 따라 실험적으로 결정
```

```
┌───────────────────────────────────────────────────────────┐
│              지식 증류 3가지 방식                           │
│                                                           │
│  ① 응답 기반 (Response-based Distillation)                │
│     교사 모델의 최종 출력 확률 분포만 모방                  │
│                                                           │
│     Teacher: [레이어1] → [레이어N] → 소프트맥스 출력       │
│                                              ↓ 전이         │
│     Student: [레이어1] → [레이어M] → 소프트맥스 모방       │
│                                                           │
│  ② 피처 기반 (Feature-based Distillation)                 │
│     중간 피처 표현(Feature Map)도 함께 모방                 │
│                                                           │
│     Teacher: [레이어1] → [레이어k] → [레이어N]             │
│                              ↓ 중간 피처 전이              │
│     Student: [레이어1] → [레이어j] → [레이어M]             │
│                                                           │
│  ③ 관계 기반 (Relation-based Distillation)                │
│     샘플 간 관계(거리, 각도)를 모방                        │
│                                                           │
│     데이터 포인트 A, B, C 간의 거리 관계:                  │
│     Teacher: dist(A,B) < dist(A,C)                       │
│     Student: 동일한 거리 관계 유지하도록 학습              │
└───────────────────────────────────────────────────────────┘
```

| 방식 | 전이 정보 | 구현 난이도 | 효과 |
|:---|:---|:---|:---|
| 응답 기반 | 최종 확률 분포 | 쉬움 | 기본 경량화 |
| 피처 기반 | 중간 레이어 표현 | 중간 | 높은 성능 유지 |
| 관계 기반 | 샘플 간 관계 | 어려움 | 일반화 향상 |

```
DistilBERT 증류 과정

교사: BERT-base (12 레이어, 110M 파라미터)
학생: DistilBERT (6 레이어, 66M 파라미터)

손실 함수 조합:
  L = 5.0 × L_ce           # 하드 레이블 손실
    + 2.0 × L_mlm           # 언어 모델 손실 (MLM)
    + 1.0 × L_cos           # 중간 레이어 코사인 유사도

결과:
  파라미터: 40% 감소 (110M → 66M)
  추론 속도: 60% 향상
  성능 유지: GLUE 벤치마크 97% 유지
  메모리: 40% 감소
```

---

## 6. 기대효과 및 결론

지식 증류는 AI 모델의 엣지 배포와 실시간 서빙을 가능하게 하는 핵심 경량화 기법이다.

지식 증류 (Knowledge Distillation) 소프트 타겟 확률 분포 모방의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
대형 Teacher 모델 (높은 정확도 · 느린 추론)
    │
    ▼
지식 증류 (Knowledge Distillation)
    ├─► 소프트 타겟: Teacher의 확률 분포 전달
    ├─► Temperature Scaling: 분포 평탄화 (T>1)
    └─► KL Divergence 손실: Student ↔ Teacher 분포 매칭
    │
    ▼
경량 Student 모델 (엣지 배포 가능)
    │
    ▼
결합 기법
    ├─► 양자화 + 증류: INT8 Student
    ├─► 프루닝 + 증류: 희소 Student
    └─► Self-Distillation: 같은 모델 내 증류
```
2. 온도 매개변수는 아이스크림 온도예요. 너무 딱딱하면(낮은 온도) 한 맛만 강하게 느껴지고, 살짝 녹으면(높은 온도) 여러 맛이 고루 느껴지죠.
3. DistilBERT는 두꺼운 사전을 얇은 포켓 사전으로 만든 거예요. 40%는 줄었지만 97%의 내용은 그대로 담겨 있어요.

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 기법 | Knowledge Distillation (지식 증류) | 교사→학생 모델 지식 전이 |
| 입력 신호 | Soft Target (소프트 타겟) | 교사 모델 확률 분포 출력 |
| 하이퍼파라미터 | Temperature (온도) | 확률 분포 부드러움 조절 |
| 증류 방식 | Response-based | 최종 출력 모방 |
| 증류 방식 | Feature-based | 중간 레이어 표현 모방 |
| 증류 방식 | Relation-based | 샘플 간 관계 모방 |
| 실사례 | DistilBERT | BERT 40% 경량화 |
| 비교 기법 | Quantization (양자화) | FP32→INT8 정밀도 감소 |
| 비교 기법 | Pruning (가지치기) | 불필요 파라미터 제거 |
