+++
weight = 148
title = "148. RLHF (Reinforcement Learning from Human Feedback) 인간 피드백 정렬"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RLHF (Reinforcement Learning from Human Feedback)는 인간 평가자의 선호 피드백으로 보상 모델(Reward Model)을 학습하고, 이를 PPO (Proximal Policy Optimization)로 LLM을 최적화해 인간 가치에 정렬(Alignment)한다.
> 2. **가치**: 단순 언어 모델링 목표(다음 토큰 예측)가 포착하지 못하는 "유용하고, 안전하고, 정직한" 응답을 생성하도록 만든다.
> 3. **판단 포인트**: RLHF의 핵심 병목은 고비용 인간 레이블링이며, DPO (Direct Preference Optimization)는 보상 모델 없이 선호 쌍으로 직접 최적화해 이를 해결한다.

## Ⅰ. 개요 및 필요성

순수 언어 모델은 유해하거나 거짓된 내용을 생성할 수 있다. ChatGPT가 단순한 GPT보다 훨씬 안전하고 유용한 이유는 RLHF로 인간의 가치관을 주입했기 때문이다.

OpenAI의 InstructGPT(2022) 논문이 RLHF의 효과를 체계적으로 증명했다: 1.3B RLHF 모델이 175B 베이스 GPT-3보다 인간 평가에서 더 좋은 평가를 받았다.

**정렬(Alignment) 3원칙 (OpenAI 3H)**
- Helpful (유용함): 사용자 요청 충족
- Harmless (무해함): 위험한 내용 생성 거부
- Honest (정직함): 모르면 모른다고 응답

📢 **섹션 요약 비유**: RLHF는 AI에게 "이 답변이 사람에게 더 도움이 되는지, 해로운지"를 가르쳐 사람처럼 판단하게 만드는 훈련이다.

## Ⅱ. 아키텍처 및 핵심 원리

| 단계 | 방법 | 설명 |
|:---|:---|:---|
| Step 1: SFT | 인스트럭션 파인튜닝 | 지시 따르기 능력 기반 구축 |
| Step 2: RM 학습 | 보상 모델 훈련 | 응답 품질 점수화 학습 |
| Step 3: PPO | 강화학습으로 최적화 | RM 보상 최대화 |

```
[RLHF 3단계 파이프라인]

Step 1: SFT (Supervised Fine-Tuning)
  베이스 모델 ─▶ 인스트럭션 데이터 학습 ─▶ SFT 모델

Step 2: Reward Model 학습
  SFT 모델로 동일 프롬프트에 여러 응답 생성
  인간 평가자가 응답 쌍 비교 → 선호 선택
  (응답A ≻ 응답B, 응답C ≻ 응답A, ...)
  ─▶ 보상 모델(RM) 학습 (Bradley-Terry 모델)
     RM(x, y) = 선호 응답 y의 점수

Step 3: PPO (Proximal Policy Optimization)
  프롬프트 ─▶ SFT 모델 (정책 π) ─▶ 응답 생성
                        │
                   RM이 보상 r(x,y) 계산
                        │
              ┌──────────▼──────────────────┐
              │  PPO 손실 최적화              │
              │  L = E[r(x,y)] - β·KL(π||π₀)│
              │  KL 패널티: 원래 모델에서    │
              │  너무 멀리 벗어나지 않도록   │
              └─────────────────────────────┘
                        │
                  정렬된 LLM 생성

[DPO 비교]
RLHF: SFT → RM 학습 → PPO (3단계, 복잡)
DPO:  SFT → 선호 쌍으로 직접 최적화 (2단계, 간단)
```

**보상 모델(Reward Model) 구조**
- 기반: LLM (SFT 모델과 같은 아키텍처)
- 출력: 스칼라 점수 (응답의 선호도)
- 학습: 선호 쌍 비교 손실: log σ(r(y_w) - r(y_l))

📢 **섹션 요약 비유**: RLHF는 AI에게 영어 선생님 역할을 하는 인간 심판이 점수를 매기면, AI가 더 높은 점수를 받으려 노력하는 훈련이다.

## Ⅲ. 비교 및 연결

| 항목 | SFT만 | RLHF | DPO |
|:---|:---|:---|:---|
| 정렬 품질 | 보통 | 높음 | 높음 |
| 구현 복잡도 | 낮음 | 매우 높음 | 중간 |
| 인간 레이블 필요 | 많음 | 매우 많음 | 적음 |
| 학습 안정성 | 높음 | 낮음 (PPO 불안정) | 높음 |
| 메모리 요구 | 보통 | 매우 높음 (4개 모델) | 중간 |

**RLAIF (Reinforcement Learning from AI Feedback)**
- 인간 대신 강력한 AI (Claude, GPT-4)가 선호 피드백 제공
- Constitutional AI (Anthropic): AI가 자체 규범으로 응답 평가

**KL (Kullback-Leibler) 발산 패널티**
- PPO 학습 중 SFT 원본 모델에서 너무 벗어나면 언어 능력 저하
- β·KL(π||π_ref): 정렬 강도와 원본 능력 사이 균형 조절

📢 **섹션 요약 비유**: KL 패널티는 새 언어를 배울 때 모국어 실력을 잃지 않게 조절하는 것이다.

## Ⅳ. 실무 적용 및 기술사 판단

**RLHF 구현 비용**
- 인간 평가자: 수백~수천 명의 선호 비교 레이블링
- GPU: PPO 학습 시 SFT 모델 4개 복사본 필요 (Actor, Critic, Reference, RM)
- 대안: DPO, IPO, KTO 등 RLHF 대안 알고리즘

**DPO (Direct Preference Optimization)**
```
손실 함수:
L_DPO = -E[log σ(β·log π_θ(y_w|x)/π_ref(y_w|x) 
                  - β·log π_θ(y_l|x)/π_ref(y_l|x))]
y_w = 선호 응답, y_l = 비선호 응답
```
- 보상 모델 불필요, 직접 LLM 최적화
- 2023년 이후 사실상 RLHF 대체 트렌드

**기술사 출제 포인트**
- "RLHF의 3단계 구조와 각 단계의 역할을 설명하시오"
- "DPO가 RLHF의 한계를 해결하는 방식을 설명하시오"

📢 **섹션 요약 비유**: RLHF는 AI를 시험하는 인간 심판이 있는 복잡한 훈련 방식이고, DPO는 그 심판 없이 학생 스스로 좋고 나쁜 답을 비교하며 배우는 방식이다.

## Ⅴ. 기대효과 및 결론

RLHF는 ChatGPT, Claude, Gemini 같은 상업 AI 어시스턴트의 핵심 기술이다. 단순한 언어 모델을 인간 가치관에 정렬된 안전한 AI로 만드는 것이 AI 안전(AI Safety) 연구의 핵심 주제이기도 하다. DPO, KTO 등 더 효율적인 방법이 등장하고 있지만 "인간 선호 정렬" 개념 자체는 앞으로도 LLM 개발의 표준이 될 것이다.

📢 **섹션 요약 비유**: RLHF는 AI에게 "인간 사회에서 어떻게 행동해야 하는가"를 가르치는 사회화 과정이다. 이 없이는 강력하지만 위험한 AI가 된다.

### 📌 관련 개념 맵
| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 전체 | RLHF | 인간 피드백 강화학습 |
| 구성 | SFT | 지도 파인튜닝 1단계 |
| 구성 | 보상 모델 (Reward Model) | 선호 점수화 |
| 구성 | PPO | 정책 최적화 알고리즘 |
| 대안 | DPO (Direct Preference Optimization) | 보상 모델 없는 정렬 |
| 개념 | 정렬 (Alignment) | 인간 가치 반영 |
| 확장 | RLAIF | AI 피드백으로 대체 |

### 👶 어린이를 위한 3줄 비유 설명
1. RLHF는 AI가 대답을 하면, 사람이 "이 대답이 더 좋아" 또는 "저 대답이 더 나빠"라고 알려주는 훈련이에요.
2. AI는 더 좋은 점수를 받으려고 계속 대답을 개선해서, 점점 유용하고 안전한 AI가 돼요.
3. ChatGPT가 위험한 내용을 거절하는 것도 이 훈련 덕분이에요.

### 📈 관련 키워드 및 발전 흐름도

```text
사전 학습 LLM (GPT, LLaMA 등)
    │
    ▼
SFT (Supervised Fine-Tuning) — 인스트럭션 따르기 학습
    │
    ▼
RLHF 3단계
    ├─► Step 1: SFT 모델 기반
    ├─► Step 2: 보상 모델 (RM) 학습 — 인간 선호 쌍
    └─► Step 3: PPO 강화학습 — RM 보상 최대화 + KL 제약
    │
    ▼
RLHF 대안 기법
    ├─► DPO: 보상 모델 불필요, 직접 선호 최적화
    ├─► KTO: 바이너리 피드백만으로 정렬
    └─► RLAIF: AI가 인간 대신 피드백 제공
    │
    ▼
HHH 정렬 AI (Helpful · Harmless · Honest)
```

