+++
title = "193. 전략 패턴 (Strategy Pattern)"
weight = 193
date = "2026-03-04"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- 동일 계열의 알고리즘들을 캡슐화하고 인터페이스화하여 런타임에 동적으로 교체 가능하게 함.
- OCP(개방-폐쇄 원칙)를 준수하며, 상속(Inheritance)의 경직성을 합성(Composition)으로 해결.
- 조건문(if-else, switch)의 나열을 다형성으로 제거하여 코드의 가독성과 확장성을 극대화.

### Ⅰ. 개요 (Context & Background)
소프트웨어 요구사항이 진화함에 따라 동일한 목적(예: 결제, 정렬, 압축)을 수행하는 여러 알고리즘이 발생한다. 이를 하나의 클래스 내부에 조건문으로 구현하면 클래스가 비대해지고 수정 시 기존 코드에 영향을 주는 문제가 발생한다. **전략 패턴(Strategy Pattern)**은 이러한 알고리즘들을 각각의 클래스로 분리하고 공통 인터페이스를 통해 클라이언트가 필요에 따라 선택적으로 사용할 수 있게 하는 행위 패턴이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
전략 패턴은 **Context(컨텍스트)**, **Strategy(전략 인터페이스)**, **ConcreteStrategy(구체적 전략)**의 세 가지 핵심 요소로 구성된다.

```text
[ Client ]
    |
    v
[ Context ] ---------------------> [ <<Interface>> Strategy ]
| - strategy: Strategy           | + executeAlgorithm()      |
| + setStrategy(Strategy)        |                           |
| + performAction()              +---------------------------+
         |                                ^          ^
         | (Delegation)                   |          |
         v                                |          |
+-----------------------+        +---------------------------+
| ConcreteStrategyA     |        | ConcreteStrategyB         |
| + executeAlgorithm()  |        | + executeAlgorithm()      |
+-----------------------+        +---------------------------+
```

1. **Context**: 전략 인터페이스에 대한 참조를 유지하며, 실제 실행 시 해당 전략 객체에 행위를 위임(Delegation)한다.
2. **Strategy**: 모든 지원 알고리즘에 대한 공통 인터페이스를 정의한다.
3. **ConcreteStrategy**: Strategy 인터페이스를 구현하여 실제 알고리즘을 제공한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전략 패턴 (Strategy) | 상태 패턴 (State) | 템플릿 메서드 (Template Method) |
| :--- | :--- | :--- | :--- |
| **핵심 목적** | 알고리즘의 교체 및 확장 | 상태 변화에 따른 행위 변화 | 알고리즘 골격 유지 및 세부 구현 지연 |
| **변경 주체** | 클라이언트가 능동적으로 설정 | 객체 내부 로직에 의해 자동 전이 | 상속을 통한 하위 클래스에서 결정 |
| **구조적 특징** | 합성(Composition) 기반 | 합성(Composition) 기반 | 상속(Inheritance) 기반 |
| **결합도** | 매우 낮음 (인터페이스 의존) | 중간 (상태 객체 간 참조 가능) | 높음 (부모-자식 강결합) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 시점**: 한 클래스 내에 유사한 행위를 수행하는 다수의 조건문이 보일 때, 또는 런타임에 다른 알고리즘을 선택해야 할 때 적용한다.
- **기술사적 판단**: 전략 패턴은 **"상속보다는 합성을 사용하라(Favor Composition over Inheritance)"**는 객체지향 설계의 대원칙을 가장 잘 보여주는 패턴이다. 특히 Spring Framework의 `Resource` 로딩 전략이나 `AuthenticationStrategy` 등에서 광범위하게 활용된다. 다만, 전략의 수가 적거나 변동 가능성이 거의 없다면 단순 구현이 더 효율적일 수 있다(Over-engineering 방지).

### Ⅴ. 기대효과 및 결론 (Future & Standard)
전략 패턴을 적용함으로써 시스템은 새로운 알고리즘 추가 시 기존 코드를 건드리지 않는 높은 확장성을 확보하게 된다. 이는 유지보수 비용을 낮추고 테스트 용이성을 높이는 결과로 이어진다. 향후 AI 기반 추천 엔진이나 동적 정책 결정 시스템(Policy Engine)에서 가중치 알고리즘을 실시간으로 교체하는 핵심 구조로 지속 활용될 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **OCP (Open-Closed Principle)**: 전략 패턴의 철학적 근간.
- **Dependency Injection (DI)**: 전략 객체를 외부에서 주입하는 기법.
- **Factory Pattern**: 적절한 전략 객체를 생성하여 반환할 때 함께 사용.

### 👶 어린이를 위한 3줄 비유 설명
- 축구 선수가 '신발'을 갈아 신는 것과 같아요.
- 비가 오면 수중전을 위한 축구화를 신고, 맑은 날에는 일반 축구화를 신는 것처럼 상황에 맞춰 장비를 바꾸는 거예요.
- 선수는 그대로인데 발에 신는 '전략(신발)'만 바꿔서 능력을 다르게 발휘하는 방법이랍니다.
