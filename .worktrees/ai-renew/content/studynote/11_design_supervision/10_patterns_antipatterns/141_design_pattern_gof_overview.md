+++
title = "141. 디자인 패턴 개요 (Design Pattern Overview)"
weight = 141
date = "2026-03-04"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- **설계의 재사용성:** 소프트웨어 설계 시 발생하는 반복적인 문제에 대한 검증된 해결책(Template)으로, 개발자 간 의사소통 효율을 극대화한다.
- **객체지향 원칙의 집대성:** SOLID 원칙을 실제 구현 수준으로 구체화하여 소프트웨어의 유연성, 확장성, 유지보수성을 확보하는 도구이다.
- **GoF 23 패턴:** 생성(Creational), 구조(Structural), 행위(Behavioral)의 3가지 범주로 분류되어 현대 소프트웨어 아키텍처의 근간을 형성한다.

### Ⅰ. 개요 (Context & Background)
- **정의:** 디자인 패턴이란 소프트웨어 설계에서 반복적으로 발생하는 문제에 대해 전문가들이 정립한 최적의 해결 방법(Best Practice)이다.
- **배경:** 1994년 에리히 감마(Erich Gamma) 등 4인(Gang of Four, GoF)이 23개의 패턴을 정리하며 대중화되었으며, 단순한 코드 복사가 아닌 '설계의 의도'를 공유하는 것이 목적이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **GoF 디자인 패턴 분류 체계**
```text
+-----------------------------------------------------------------------+
|                       GoF Design Patterns (23)                        |
+-----------------------------------------------------------------------+
| [Creational 생성]      | [Structural 구조]       | [Behavioral 행위]      |
| (How to create?)       | (How to assemble?)      | (How to communicate?)  |
|------------------------|-------------------------|------------------------|
| Singleton, Builder,    | Adapter, Bridge,        | Strategy, Observer,    |
| Factory Method,        | Composite, Decorator,   | Template Method,       |
| Abstract Factory,      | Facade, Flyweight,      | Command, State, etc.   |
| Prototype              | Proxy                   | (11 Patterns)          |
+-----------------------------------------------------------------------+
```
- **핵심 구성요소:**
  1. **Pattern Name:** 설계의 어휘(Vocabulary) 역할
  2. **Problem:** 패턴이 적용되는 상황과 맥락
  3. **Solution:** 요소들 간의 관계 및 책임 분배
  4. **Consequences:** 패턴 적용에 따른 장단점 및 상충 관계(Trade-off)

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 분류 | 생성(Creational) | 구조(Structural) | 행위(Behavioral) |
| :--- | :--- | :--- | :--- |
| **관점** | 객체 생성 프로세스 캡슐화 | 클래스/객체 조합 구조 | 객체 간 상호작용 및 책임 |
| **목적** | 생성 로직과 클라이언트 분리 | 더 큰 구조 형성 및 확장 | 결합도 최소화 및 유연성 |
| **대표 패턴** | Singleton, Factory Method | Adapter, Decorator | Strategy, Observer |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **감리 주안점:** 디자인 패턴의 오용(Over-engineering) 여부를 점검해야 한다. 단순한 기능을 위해 복잡한 패턴을 도입하여 '설계 부채'를 유발하는지 확인한다.
- **기술사적 판단:** 패턴은 '도구'이지 '목적'이 아니다. 비즈니스 요구사항의 변경 가능성(Volatility)에 따라 적절한 패턴을 선택해야 하며, 인터페이스 기반 설계를 통해 결합도를 낮추는 것이 핵심이다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과:** 코드 품질 향상, 검증된 아키텍처 확보, 개발 기간 단축 및 팀 간 명확한 의사소통 지원.
- **결론:** 클라우드 네이티브 및 MSA 환경에서도 서킷 브레이커, 사이드카 등 아키텍처 패턴으로 확장되어 활용되고 있으며, 객체지향 설계의 필수 소양으로 자리 잡고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** S/W 아키텍처, 객체지향 설계(OOD)
- **하위 개념:** 생성 패턴, 구조 패턴, 행위 패턴, 안티 패턴(Anti-Pattern)
- **연관 개념:** SOLID 5원칙, 리팩토링, 클린 코드

### 👶 어린이를 위한 3줄 비유 설명
- 레고 블록을 조립할 때, 성을 만드는 방법이나 자동차를 만드는 방법이 이미 설명서에 적혀 있는 것과 같아요.
- 매번 처음부터 고민하지 않고, 똑똑한 사람들이 미리 만들어둔 '조립 비법'을 따라 하는 거예요.
- 그러면 더 튼튼하고 멋진 장난감을 훨씬 빠르게 만들 수 있답니다!
