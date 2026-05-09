+++
weight = 191
title = "행위 패턴 개요 (Behavioral Patterns Overview)"
date = "2026-03-04"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- **메시지 통신의 설계:** 객체나 클래스 간의 알고리즘 분배와 책임, 그리고 통신 방식을 정의하여 결합도를 낮추는 패턴군이다.
- **제어 흐름의 캡슐화:** 복잡한 실행 흐름을 객체 내부에 숨겨 코드의 가독성과 유지보수성을 극대화한다.
- **유연한 상호작용:** 객체들이 서로 어떻게 협력하는지에 집중하여 런타임에 동적으로 행동을 변경할 수 있는 구조를 제공한다.

### Ⅰ. 개요 (Context & Background)
- 소프트웨어 시스템이 커질수록 객체 간의 상호작용은 기하급수적으로 복잡해진다. 행위 패턴은 이러한 '객체 간의 관계'와 '책임의 분배'를 표준화하여 스파게티 코드를 방지하고, 변화에 유연한 설계(OCP)를 가능하게 한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ Client ] ----> [ Behavioral Pattern Strategy/Subject/Command ]
     |                       |
     |              +-------------------+
     |              |   Algorithm /     |
     +------------> |   Responsibility  |
                    |    Encapsulation  |
                    +-------------------+
                             |
                    [ Concrete Handlers ]
                    (Strategy A, Observer B, State C)

<Bilingual ASCII Diagram: 행위 패턴 통제 구조 / Behavioral Pattern Control Structure>
```

- **핵심 메커니즘:**
  1. **상속 기반(Class):** 템플릿 메서드와 같이 상속을 통해 알고리즘의 뼈대를 고정하고 세부를 하위 클래스에서 정의한다.
  2. **합성 기반(Object):** 전략, 상태 패턴과 같이 객체 합성을 통해 런타임에 행동을 위임(Delegation)한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | 생성 패턴 (Creational) | 구조 패턴 (Structural) | 행위 패턴 (Behavioral) |
| :--- | :--- | :--- | :--- |
| **주요 관심사** | 객체의 생성과 초기화 | 클래스/객체의 조합 및 구성 | 객체 간의 알고리즘 및 통신 |
| **핵심 목적** | 결합도 낮은 인스턴스화 | 큰 구조의 설계와 인터페이스 | 책임 분산 및 협력 방식 최적화 |
| **대표 사례** | Singleton, Factory | Adapter, Facade | Strategy, Observer, Command |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **판단 기준:** 시스템의 변경이 '데이터 구조'에 있는지, '기능적 절차'에 있는지 파악해야 한다. 기능적 절차가 빈번히 바뀐다면 행위 패턴 적용이 필수적이다.
- **주의 사항:** 너무 많은 행위 패턴을 남용하면 객체 간의 메시지 추적이 어려워져 오히려 디버깅 비용이 상승할 수 있다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 행위 패턴은 MSA 환경에서의 서비스 간 통신(Saga, Event-driven)의 논리적 모태가 된다. 객체지향의 본질인 '메시지 전달'을 가장 잘 구현한 도구이며, 클린 코드 달성의 핵심 지표이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- GoF 디자인 패턴 -> 행위 패턴 -> (Strategy, Observer, State, Command, Template Method) -> SOLID 원칙 (LSP, OCP)

### 👶 어린이를 위한 3줄 비유 설명
- **생성 패턴**은 "장난감을 어떻게 만드느냐"이고, **구조 패턴**은 "장난감을 어떻게 조립하느냐"예요.
- **행위 패턴**은 "장난감 친구들이 서로 어떻게 대화하고 놀이를 정하느냐"를 정하는 규칙이랍니다.
- 이 규칙이 잘 짜여 있으면 새로운 친구가 와도 금방 같이 재미있게 놀 수 있어요!
