+++
weight = 198
title = "198. 상태 패턴 vs 전략 패턴 (State vs Strategy Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Strategy (전략 패턴)는 **알고리즘 교체**, State (상태 패턴)는 **내부 상태 전이**를 캡슐화한다. 구조는 거의 동일하지만 "누가 교체하는가"에서 갈린다.
> 2. **가치**: 방대한 `if-else` / `switch-case` 분기를 객체 다형성으로 대체하여 OCP (Open-Closed Principle)를 달성한다.
> 3. **판단 포인트**: 클라이언트가 능동적으로 행동을 선택하면 Strategy, 객체 스스로 조건에 따라 자신의 상태를 바꾸면 State.

---

## Ⅰ. 개요 및 필요성

### 1-1. 공통 배경

GoF (Gang of Four) 패턴 중 **행동(Behavioral)** 카테고리에 속하는 두 패턴은 겉으로 보기에 구조(UML)가 거의 동일하다.

- `Context` 클래스가 `Strategy` 또는 `State` 인터페이스를 참조한다.
- 런타임(Runtime)에 해당 인터페이스의 구현체를 교체할 수 있다.
- 분기 로직 없이 행동을 다형성(Polymorphism)으로 처리한다.

### 1-2. 두 패턴의 존재 이유

전통적인 코드는 아래처럼 상태·전략을 `if-else`로 처리한다:

```
if (state == "IDLE") { ... }
else if (state == "PROCESSING") { ... }
else if (state == "DONE") { ... }
```

상태/전략이 늘어날수록 분기가 폭발한다. 두 패턴은 각 분기를 **클래스**로 분리하여 새로운 분기 추가 시 기존 코드를 건드리지 않도록 한다.

### 1-3. FSM (Finite State Machine)과 State 패턴

State 패턴의 핵심 개념은 FSM (Finite State Machine, 유한 상태 머신)이다. FSM은 다음 세 가지로 정의된다:

| 요소 | 설명 |
|:---|:---|
| 상태 집합 (States) | 유한하게 정의된 상태들 |
| 이벤트 (Events) | 상태를 전이시키는 트리거 |
| 전이 함수 (Transition) | 현재 상태 + 이벤트 → 다음 상태 |

📢 **섹션 요약 비유**: Strategy는 "운전자가 직접 기어를 바꾸는 수동 변속기", State는 "속도와 엔진 상태를 보고 자동으로 변속하는 자동 변속기".

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 구조 비교 (UML 요약)

```
[ Strategy Pattern ]                    [ State Pattern ]
                                                         
  Client                                  Context
    │                                       │
    ▼  setStrategy()                        │ (state transitions internally)
  Context ──────► «interface»            ◄─┤ state.handle()
    │             Strategy               │ │
    │                │                   │ ▼
    │         ┌──────┴──────┐      ┌────────────────────┐
    │         ▼             ▼      ▼                    ▼
    │    ConcreteA     ConcreteB  StateA  ──event──► StateB
    │                              (transitions managed inside)
    └─ Algorithm varies            └─ Behavior changes with state
```

### 2-2. 자판기 (Vending Machine) 예시로 보는 State 패턴

자판기는 대표적인 FSM (Finite State Machine):

```
┌─────────────────────────────────────────────────────┐
│                  VendingMachine (Context)            │
│                                                     │
│  currentState: VendingState                         │
│                                                     │
│  insertCoin() ─► currentState.insertCoin(this)      │
│  selectItem()─► currentState.selectItem(this)       │
│  dispense()  ─► currentState.dispense(this)         │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
  ┌─────────────┐ ┌──────────┐ ┌──────────────┐
  │  IdleState  │ │ HasCoin  │ │ SoldOutState │
  │  (대기 중)  │ │ State    │ │  (품절)      │
  │             │ │ (동전    │ │              │
  │insertCoin() │ │  투입됨) │ │              │
  │→ HasCoin    │ │select()  │ │              │
  └─────────────┘ │→ dispense│ └──────────────┘
                  └──────────┘
```

각 상태 클래스는 **동전 투입, 상품 선택, 배출** 이벤트에 대해 서로 다른 행동을 구현한다. 상태 전이는 `context.setState(new HasCoinState())` 처럼 **ConcreteState 내부**에서 일어난다.

### 2-3. 전략 패턴 정렬 예시

```
  Client
    │
    ├─ setSortStrategy(new QuickSort())   ← 클라이언트가 능동적으로 교체
    │
    ▼
  Sorter (Context)
    │
    └─ strategy.sort(data) ────►  «interface» SortStrategy
                                        │
                             ┌──────────┼──────────┐
                             ▼          ▼           ▼
                         QuickSort  MergeSort  BubbleSort
```

📢 **섹션 요약 비유**: State는 "신호등이 스스로 초록→노랑→빨강으로 바뀌는 것", Strategy는 "운전자가 내비게이션 경로를 직접 고르는 것".

---

## Ⅲ. 비교 및 연결

### 3-1. State vs Strategy 핵심 비교표

| 비교 항목 | Strategy 패턴 | State 패턴 |
|:---|:---|:---|
| **목적** | 알고리즘(행동)의 교체 | 상태에 따른 행동 변화 |
| **교체 주체** | 외부 클라이언트(Client) | 내부 상태 객체 자신 |
| **상태 인식** | Context가 전략에 무관심 | Context가 현재 상태를 알고 있음 |
| **전이 로직** | 없음 | ConcreteState 내부에 있음 |
| **참조 방향** | Context → Strategy | Context ↔ State (양방향 가능) |
| **대표 사례** | 정렬 알고리즘, 인증 방식 | 자판기, 주문 처리 흐름, TCP 연결 |
| **FSM 연관성** | 없음 | FSM의 객체지향 구현체 |
| **OCP 달성** | ✅ | ✅ |

### 3-2. 관련 패턴 연결

| 패턴 | State/Strategy와의 관계 |
|:---|:---|
| Template Method (템플릿 메서드) | Strategy와 유사하나 상속 기반 |
| Command (커맨드) | 명령 객체로 Strategy를 감쌀 수 있음 |
| Flyweight (플라이웨이트) | 상태 객체를 공유 인스턴스로 최적화 |
| Singleton (싱글톤) | 무상태 State/Strategy 객체에 적용 가능 |

📢 **섹션 요약 비유**: Strategy는 "메뉴판에서 손님이 고르는 것", State는 "요리사가 조리 단계에 따라 다음 동작을 알아서 결정하는 것".

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 코드 시그니처 비교

**Strategy (전략 패턴)**:
```java
// 클라이언트가 명시적으로 전략 주입
context.setStrategy(new AESEncryption());
context.execute();

// 또는 생성자 DI (Dependency Injection)
PaymentService svc = new PaymentService(new KakaoPay());
```

**State (상태 패턴)**:
```java
// 상태는 내부에서 전이됨 - 클라이언트는 이벤트만 발생
order.pay();          // → PAID 상태로 전이
order.ship();         // → SHIPPED 상태로 전이
order.deliver();      // → DELIVERED 상태로 전이
// 잘못된 순서의 이벤트는 IllegalStateException 발생
```

### 4-2. TCP 연결 State 패턴 적용 사례

```
  TCPConnection
       │
       ├─ CLOSED ──SYN_SENT──► ESTABLISHED ──FIN_WAIT──► TIME_WAIT ──► CLOSED
       │                              │
       │                         DATA 전송 가능
       │
  각 상태 클래스: open(), close(), acknowledge() 메서드를 다르게 구현
```

### 4-3. 기술사 서술 포인트

- Strategy: **DI (Dependency Injection)**와 자연스럽게 연결 → Spring Bean 주입 패턴
- State: **도메인 주도 설계(DDD, Domain-Driven Design)** 의 Aggregate 상태 관리에 적합
- 두 패턴 모두 **SRP (Single Responsibility Principle) + OCP** 동시 달성

📢 **섹션 요약 비유**: Strategy는 "회사가 외주 업체를 바꾸는 것(외부 결정)", State는 "부서가 프로젝트 단계에 따라 업무 방식을 자동으로 바꾸는 것(내부 결정)".

---

## Ⅴ. 기대효과 및 결론

### 5-1. 공통 효과

- 거대한 `switch/if-else` 분기 제거 → 코드 가독성·유지보수성 향상
- OCP (Open-Closed Principle): 새로운 전략/상태 추가 시 기존 클래스 무수정
- 단위 테스트(Unit Test) 용이: 각 전략/상태 독립 테스트 가능

### 5-2. State 패턴만의 효과

- FSM (Finite State Machine) 의 명시적 코드화 → 불법 상태 전이 방지
- 상태 전이 이력 추적 및 Audit Log 구현 용이
- 비즈니스 흐름(워크플로우)을 코드로 명확하게 문서화

### 5-3. 결론: 선택 기준

```
클라이언트가 의도적으로 행동 방식을 선택하는가?
        YES → Strategy Pattern
        NO  → 내부 조건/이벤트로 행동이 자동으로 바뀌는가?
                YES → State Pattern
```

📢 **섹션 요약 비유**: Strategy는 "내가 직접 고른 음악 플레이리스트", State는 "기분·시간대에 따라 AI가 자동으로 틀어주는 플레이리스트".

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF Behavioral Pattern | 행동 패턴 그룹 |
| 상위 개념 | FSM (Finite State Machine) | State 패턴의 이론적 기반 |
| 하위 개념 | ConcreteState / ConcreteStrategy | 실제 행동 구현체 |
| 연관 개념 | OCP (Open-Closed Principle) | 두 패턴이 달성하는 설계 원칙 |
| 연관 개념 | DI (Dependency Injection) | Strategy 패턴의 스프링 적용 방식 |
| 연관 개념 | Command Pattern | Strategy와 함께 사용 가능 |

### 👶 어린이를 위한 3줄 비유 설명

- Strategy는 아이가 "오늘은 자전거 타고 학교 갈래요" 하고 **스스로 방법을 고르는 것**이에요.
- State는 신호등처럼 **조건(시간)이 되면 스스로 색이 바뀌는 것**이에요.
- 둘 다 '행동을 바꾼다'는 점은 같지만, 누가 바꾸느냐가 달라요!
