+++
weight = 10
title = "계획 및 추론"
description = "인공지능에서 계획(Planning)과 추론(Reasoning)의 정의, 계획 알고리즘, STRIPS와 PDDL"
category = "10_ai"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 계획 (Planning)은 목표 상태(Goal State)에 도달하기 위한 행동 시퀀스(Action Sequence)를 수립하는 작업이며, 추론 (Reasoning)은 이미 알려진 사실로부터 새로운 사실을 논리적으로導出하는 과정이다.
> 2. **가치**: 자율주행, 로보틱스, 게임 AI, 자동화된 기업 프로세스 등"목표 달성을 위해 행동을 순서대로 구성"해야 하는 모든 영역에 필수적이다.
> 3. **융합**: Classical Planning에서 현대적 Neural Planning, Hierarchical Task Network (HTN), AND-OR Graph 등 다양한 접근법이 발전했으며, LLM과 결합한" Language-based Planning"이 새로운 연구방향으로 부상하고 있다.

---

## Ⅰ. 개요 및 필요성

### 개념 정의

**계획 (Planning)**은 Russell & Norvig의 정의에 따르면,"목표 상태에 대한 기술로부터 행동을 선택하여 그 목표를 달성하는 것"이다.Planning은"현재 상태 S에서 목표 상태 G에 도달하기 위해 어떤 행동을 언제 실행할 것인가?"라는 질문에 답하는 것이다. 예를 들어,"현재 서울에 있고,goal이 도쿄에 도착"이라면,"서울→김포机场→비행기→도쿄机场"와 같은 행동 시퀀스를 수립하는 것이 Planning이다.

**추론 (Reasoning)**은 이미 알려진 사실(전제, Premise)으로부터 논리적 절차에 따라 새로운 사실(결론, Conclusion)을 도출하는 과정이다. 여기에는 연역 추론(Deductive: 일반에서 특수로), 귀납 추론(Inductive: 특수에서 일반으로), 연관 추론(Abductive: 관찰에서 설명으로) 등 다양한 형태가 포함된다.

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Planning vs Reasoning 비교                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Planning (계획)                Reasoning (추론)                     │
│  ─────────────────              ──────────────────                    │
│  질문: "어떻게Goal에 도달?"     질문: "무엇으로부터導出?"            │
│  │                            │                                     │
│  ├─ 현재 상태에서 목표 상태로   ├─ 전제로부터 결론을                 │
│  │  의 이동 경로 탐색          │  논리적으로 도출                   │
│  │                            │                                     │
│  ├─ 행동 시퀀스 생성           ├─ 새로운 정보 생성                  │
│  │                            │                                     │
│  └─ Plan: 행동 A → B → C       └─ Inference: A ∧ B → C              │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │ 관계: Planning은 Reasoning을 利用할 수 있다                      │   │
│  │ 예: "행동 X의效果가 상태 Y를 만들어낸다"는 추론을 통해          │   │
│  │     Planning에서 행동 선택의 근거로 삼는다                      │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Planning과 Reasoning은 밀접하게 관련되면서도 다른 작업이다. Planning은 목표 지향적 행동 시퀀스를"생성"하는 것이고, Reasoning은 논리적 관계를 통해 정보를"도출"하는 것이다. 그러나 실제로는Planning에서 Reasoning을 활용: 각 행동의 선행 조건과 효과를 추론하여 어떤 행동을 선택할지 결정한다.

### 비유

Planning은"여행 일정 짜기"와 같다. 현재 위치(현재 상태)에서 목적지(목표 상태)까지 다양한 이동 수단(행동)을 순서대로 조합하여 일정을組む 것이다. Reasoning은"지도를 보며 경로를 分析하는 것"으로, 지도의 정보(전제)로부터"이 경로가 더 빠르다"는結論을 도출한다.

### 섹션 요약 비유

Planning과 Reasoning은"길 찾기"에서의 관계와 같다. Reasoning은"이 길은 산을 넘어야 하고 저 길은 강을 건너야 한다"는 개별 정보의 분석이고, Planning은 그러한 분석을 종합하여"최적의 경로로 여행 일정을組む" 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Planning 문제의 formal 정의

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Planning 문제의Formal 정의                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Planning Problem = (S, A, E, s₀, G)                                │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │  S: 상태 공간 (State Space)                                  │     │
│  │     - 가능한 모든 세계 상태의集合                            │     │
│  │     - 예: {at(서울), at(김포), ¬at(도쿄)}                   │     │
│  │       (¬는 NOT, "도okol에 없다")                             │     │
│  │                                                             │     │
│  │  A: 행동 공간 (Action Space)                                 │     │
│  │     - 각 행동의 선행 조건(precondition)와                   │     │
│  │       효과(effect)로 정의                                    │     │
│  │     - 예: fly(서울, 도쿄)                                    │     │
│  │       Precond: at(서울), plane_available(서울)               │     │
│  │       Effect: ¬at(서울), at(도쿄)                            │     │
│  │                                                             │     │
│  │  E: 효과 함수 (Transition Function)                          │     │
│  │     - S × A → S: 상태에 행동을 적용하면                      │     │
│  │       새로운 상태로 전이                                      │     │
│  │                                                             │     │
│  │  s₀: 초기 상태 (Initial State)                               │     │
│  │       - 예: at(서울) ∧ plane_available(서울)                │     │
│  │                                                             │     │
│  │  G: 목표 상태 (Goal State)                                   │     │
│  │       - 예: at(도쿄)                                        │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  【Plan求解 과정】                                                    │
│                                                                      │
│  s₀ ──▶ [A₁ 적용] ──▶ s₁ ──▶ [A₂ 적용] ──▶ s₂ ──▶ ... ──▶ G ✓  │
│         행동 1            행동 2                                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Planning 문제의 formal 정의는State Space(상태 공간), Action Space(행동 공간), Transition Function(효율 함수), Initial State(초기 상태), Goal State(목표 상태)의 5-tuple로 표현된다. 상태는世界中 존재할 수 있는 모든 조건들의 조합으로, 행동은 선행 조건(Precondition)이 충족되어야 실행 가능하고,效果(Effect)가 적용되어世界を新しい状態へと变迁させる. Planning은初期状態에서 목표 상태로 가는最短 또는 최적의 행동 시퀀스를 찾는 검색 문제로 定式化된다.

### STRIPS와 PDDL

```
┌──────────────────────────────────────────────────────────────────────┐
│                    STRIPS / PDDL 표기법                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  【STRIPS 표기법 (1971)】                                            │
│                                                                      │
│  OPERATION: fly(p, from, to)                                        │
│  PRECONDITION: at(p, from) ∧ plane_available(from)                  │
│  EFFECT: at(p, to) ∧ ¬at(p, from) ∧ ¬plane_available(from)         │
│                                                                      │
│  예:                                                                 │
│  OPERATION: drive(car, origin, destination)                        │
│  PRECONDITION: at(car, origin)                                      │
│  EFFECT: at(car, destination) ∧ ¬at(car, origin)                   │
│                                                                      │
│  【PDDL 표기법 (1998) — STRIPS의 발전형】                            │
│                                                                      │
│  (define (problem problem-name)                                      │
│    (:domain transportation)                                          │
│    (:objects city1 city2 - location                                 │
│              plane1 - airplane                                       │
│              truck1 - truck)                                        │
│    (:init (at plane1 city1)                                         │
│            (at truck1 city1))                                        │
│    (:goal (and (at plane1 city2)                                    │
│                (at truck1 city2))))                                 │
│                                                                      │
│  핵심 구성:                                                          │
│  - :domain — 문제 영역 정의                                           │
│  - :objects — 변수 및 객체 선언                                       │
│  - :init — 초기 상태 기술                                            │
│  - :goal — 목표 상태 기술                                            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** STRIPS(Stanford Research Institute Problem Solver)는 1971년 제안된 classical planning 언어다. 각 행동을 PRECONDITION(선행 조건)과 EFFECT(효과)로 정의하며, 이것을 조합하여 목표에 도달하는 행동 시퀀스를 탐색한다. PDDL(Planning Domain Definition Language)은 STRIPS를 기반으로 1998년标准化된 국제적 planning 문제 기술 언어로, :domain, :objects, :init, :goal의 구조를 가진다. 현재는 International Planning Competition(IPC)에서 사용되는 표준 언어다.

### Planning 알고리즘 분류

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Planning 알고리즘 분류                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  【 Classical Planning (도메인 독립적) 】                              │
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐                            │
│  │ Forward Search  │  │ Backward Search │                            │
│  │ (전방 탐색)     │  │ (후방 탐색)      │                            │
│  ├─────────────────┤  ├─────────────────┤                            │
│  │ s₀에서 시작해   │  │ G에서 시작해     │                            │
│  │ G로 다가감      │  │ s₀로 역추적     │                            │
│  │ (데이터 주도)   │  │ (목표 주도)     │                            │
│  │ 비효율적 수 있다 │  │ Goal에 가까운    │                            │
│  │                │  │ 상태先行探索    │                            │
│  └─────────────────┘  └─────────────────┘                            │
│                                                                      │
│  【Search 기반 알고리즘】                                             │
│  - BFS, DFS, IDS (단순 탐색)                                         │
│  - A* Search (휴리스틱 활용)                                         │
│  - Greedy Best-First Search                                          │
│  - Hierarchical Task Network (HTN)                                   │
│                                                                      │
│  【Planning as SAT/SMT】                                             │
│  - Planning 문제를 Boolean Satisfiability로 변환                      │
│  -高效的求解 가능 (특히 제약이 많은 경우)                              │
│                                                                      │
│  【Graphplan】                                                       │
│  - Planning 그래프_construction → solution 추출                       │
│  - mutually exclusive 행동 고려                                       │
│                                                                      │
│  【Modern: Neural Planning / LLM-based Planning】                     │
│  - 데이터 기반 planning 학습                                          │
│  - LLM이 자연어로 기술된 목표에서 Plan 생성                          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Classical Planning 알고리즘은 크게 Forward Search(초기에서 목표 방향)와 Backward Search(목표에서 초기 방향)로 나뉜다. Forward는 간단하지만 상태 공간이 크면 비효율적이고, Backward는 목표에 가까운 상태先行探索하므로 효율적인 경우 많다. A* 알고리즘은 휴리스틱(heuristic)을 활용하여 최적의 경로를 찾는 것으로, planning에서도 널리 활용된다. 최근에는 Neural Network로 planning을 학습하는 Neural Planning과, LLM의 언어 이해 능력을 利用한 Language-based Planning이 새로운研究方向으로 부상하고 있다.

### 섹션 요약 비유

Planning 알고리즘은"길 찾기 방법론"과 같다. Forward Search는"현재 위치에서 출발하여 모든 가능성을探索하며goal에 가까운 길을 찾기"이고, Backward Search는"goal에서 역으로"어디서부터 출발해야 하는지"를 찾는 것이며, A*은"직선 거리(휴리스틱)를 참고하여 가장 빠른길을 찾기"이다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: Classical Planning vs Modern Planning

| 구분 | Classical Planning | Modern Planning (Neural/LLM) |
|:---|:---|:---|
| **지식 표현** | 명시적 규칙 (STRIPS/PDDL) | 암묵적 (신경망 가중치) |
| **검증 가능성** | 명시적 추적, 완전 검증 가능 | 부분적 (블랙박스) |
| **적응성** | 새 도메인에 수동 변환 필요 | 데이터로 자동 학습 |
| **불확실성** | 가정 (noiseless) 환경에만適用 | 확률적/부분 관찰 환경対応 |
| **규모** | 소~중규모 문제에 효과적 | 대규모 문제에 잠재력 |

### 섹션 요약 비유

Classical Planning은"항상 정해진 규칙의 게임"에서 미리Strategizing하는 것과 같고, Modern Neural Planning은"大量의 경기 데이터"를 분석하여 자연스럽게 winning strategies를 습득하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 — 로봇의 물체 파악 및 회수**: Kitchenery에서 특정 물체(예: 빨간 컵)를 찾아 회수하는 로봇의 planning을 생각해보자. Initial state: "컵이 찬장 안에 있다", Goal: "컵이 손에 있다". Planning 과정: (1) 개방 행동을 통해 문 열기, (2) 이동 행동으로 찬장 앞까지 가기, (3) 회수 행동으로 컵 잡기. 각 행동의 선행 조건과 효과를 PDDL로 정의하면 자동 계획 시스템을構築할 수 있다.

**시나리오 — LLM-based Agent Planning**: ChatGPT 같은 LLM에"30분 안에 간단한 간식을 가져다줘"라고 요청하면, LLM은 자연어로 기술된 목표에서 단계별 계획을自動 생성한다: (1) 냉장고 확인, (2) 과일/빵 선택, (3) 트레이에 담기, (4) 테이블에 두기. 이러한 Language-based Planning은 현대 AI Agent의 핵심 component로 활용되고 있다.

### 섹션 요약 비유

Planning은"요리 레시피 짜기"와 같다. 재료를 확인하고(현재 상태), 목표 요리를 정하고(목표 상태), 적절한 조리 순서를決定하는 것이 Planning이다. 조리 과정에서 재료가 다 떨어지면(실행 중 변화) 다시Planning을 수정해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

- **LLM-based Agentic AI**: LLM이 일상 언어의 목표에서 구체적 실행 계획을 세우고, 도구를 사용하며, 피드백을 받아 Plan을 수정하는 Agentic AI가 2024년 이후加速发展
- **Foundation Model for Planning**: 대규모 사전 학습된 모델이 다양한 planning 도메인에 범용으로 적용 가능
- **Neuro-Symbolic Planning**: Symbolic planning의 검증 가능성과 Neural planning의 학습 가능성을 결합

### 섹션 요약 비유

Planning과 Reasoning의 발전은"AI가 단순히 따라하는 것을 넘어 스스로 계획하고 추론하는 단계로 나아가는 것"을 의미한다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **상태 공간 (State Space)** | Planning 문제에서 가능한 모든 상태들의集合, 탐색의 기본 공간 |
| **행동 (Action)** | Planning의 기본 단위로, 선행 조건(precondition)과 효과(effect)로 정의 |
| **STRIPS / PDDL** | Classical Planning의 표준 기술 언어 |
| **A* Search** | 휴리스틱을利用한 최적 경로 탐색 알고리즘, Planning에서 널리 활용 |
| **Hierarchical Task Network (HTN)** | 작업을 하위 작업으로 분해하는 계층적 planning 접근법 |
| **추론 (Reasoning)** | 전제로부터 결론을 논리적으로 도출하는 과정, Planning의 기반이 됨 |
| **LLM-based Agent** | LLM을 활용하여 자연어로 기술된 목표에서 Plan을 자동 생성하는 Agent |

---

## 👶 어린이를 위한 3줄 비유 설명

1. Planning은"좋은 결과를 위해 무엇을 먼저, 무엇을 나중에 할지 순서를 정하는 것"이에요. 예를 들어"엄마 커피를 가져다 드리겠다"고 했을 때,"먼저 컵을 가져오고, 그次に 커피를 따르고, 마지막으로 엄마한테 건네야겠다"는 순서를 세우는 거예요.
2. Reasoning은"이미 알고 있는 사실로부터 새로운 사실을 알아내는 것"이에요."비 온 뒤에 땅이 젖어 있으면" (전제), "이 땅에서 놀면 옷이 더러워질 것이다" (결론)와 같이 맺고 따르는 거예요.
3. AI에서도 이 두 가지를 함께 써요. 먼저 추론으로 정보를 분석하고, 그分析을 바탕으로 계획해서 행동을順序대로 실행하는 거예요!
