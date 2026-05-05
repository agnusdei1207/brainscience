+++
weight = 160
title = "160. 디자인 패턴과 설계 원칙 (OCP·DIP와 디자인 패턴)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 디자인 패턴은 SOLID (Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion) 원칙의 구체적 구현 수단이며, 특히 OCP (Open-Closed Principle, 개방-폐쇄 원칙)와 DIP (Dependency Inversion Principle, 의존성 역전 원칙)를 구현하는 핵심 도구다.
> 2. **가치**: 패턴을 원칙과 연결해 이해하면 "왜 이 패턴을 쓰는가"에 답할 수 있어, 패턴 암기가 아닌 설계 판단력을 갖추게 된다.
> 3. **판단 포인트**: 새 기능 추가 시 기존 코드를 수정해야 한다면 OCP 위반이고, 고수준 모듈이 구체 클래스에 직접 의존한다면 DIP 위반이다 — 두 원칙을 지키는 패턴을 선택해야 한다.

> 📝 모범 답안

## 1. 개요 및 필요성

좋은 소프트웨어 설계의 핵심은 변경(Change)에 유연하게 대응하는 것이다. 로버트 마틴(Robert Martin)이 체계화한 SOLID 원칙은 객체지향 설계의 5가지 핵심 지침으로, 이 중 OCP와 DIP는 디자인 패턴과 가장 긴밀하게 연결된다.

**OCP (Open-Closed Principle, 개방-폐쇄 원칙)**: 소프트웨어 엔티티는 확장에는 열려 있어야 하고(Open for Extension), 수정에는 닫혀 있어야 한다(Closed for Modification). 즉, 기존 코드를 변경하지 않고 새 기능을 추가할 수 있어야 한다.

**DIP (Dependency Inversion Principle, 의존성 역전 원칙)**: 고수준 모듈(High-Level Module)은 저수준 모듈(Low-Level Module)에 직접 의존해서는 안 된다. 둘 다 추상화(Abstraction, 인터페이스나 추상 클래스)에 의존해야 하며, 추상화는 세부 구현(Detail)에 의존하면 안 된다.

이 두 원칙이 실제 코드에서 구현되는 방식이 바로 디자인 패턴이다.

📢 **섹션 요약 비유**: OCP는 "콘센트 규격처럼 확장구는 꽂아도 되지만 벽 배선은 건드리지 말라"는 규칙이고, DIP는 "전자기기가 특정 브랜드 콘센트가 아닌 표준 220V 규격에 의존해야 한다"는 원칙이다.

## 2. 구성요소

### OCP 위반과 준수 비교

OCP를 위반하면 새 도형 추가 시마다 `ShapeDrawer` 클래스를 수정해야 한다. OCP를 준수하면 `Shape` 인터페이스를 구현한 새 클래스를 추가만 하면 된다.

```
  OCP 위반 (수정이 필요한 구조):
  ┌─────────────────────────────────────┐
  │           ShapeDrawer               │
  │  + draw(shape):                     │
  │    if shape == CIRCLE: ...          │
  │    if shape == SQUARE: ...          │
  │    // 새 도형 추가 시 이 블록 수정  │
  └─────────────────────────────────────┘

  OCP 준수 (확장만으로 기능 추가):
  ┌──────────────┐         ┌──────────────────┐
  │ ShapeDrawer  │────────>│ <<interface>>    │
  └──────────────┘         │     Shape        │
                           └────────┬─────────┘
                                    │
                       ┌────────────┼────────────┐
                       │            │            │
               ┌───────┴───┐ ┌──────┴───┐ ┌─────┴───────┐
               │  Circle   │ │  Square  │ │  Triangle   │
               └───────────┘ └──────────┘ └─────────────┘
```

### DIP 위반과 준수 비교

```
  DIP 위반 (구체 클래스 직접 의존):
  ┌──────────────────┐         ┌──────────────────┐
  │  OrderService    │────────>│  MySQLRepository │
  │  (고수준 모듈)    │         │  (저수준 구체)   │
  └──────────────────┘         └──────────────────┘

  DIP 준수 (추상화를 경유한 의존):
  ┌──────────────────┐         ┌──────────────────┐
  │  OrderService    │────────>│  <<interface>>   │
  │  (고수준 모듈)    │         │ OrderRepository  │
  └──────────────────┘         └────────┬─────────┘
                                        │ implements
                               ┌────────┴─────────┐
                               │  MySQLRepository │
                               │  (저수준 구체)   │
                               └──────────────────┘
```

| SOLID 원칙 | 핵심 내용 | 구현 패턴 | 위반 증상 |
|:---|:---|:---|:---|
| SRP (Single Responsibility Principle, 단일 책임 원칙) | 클래스는 단 하나의 변경 이유만 가져야 함 | 파사드(Facade), Command | 갓 클래스(God Class) |
| OCP (Open-Closed Principle) | 확장 열림, 수정 닫힘 | Strategy, Decorator, Factory Method | if-else 체인 증식 |
| LSP (Liskov Substitution Principle, 리스코프 치환 원칙) | 하위 타입은 상위 타입으로 대체 가능 | Template Method | 상속 후 예외 던지기 |
| ISP (Interface Segregation Principle, 인터페이스 분리 원칙) | 클라이언트가 사용하지 않는 메서드에 의존 강요 금지 | Adapter, Facade | 뚱뚱한 인터페이스 |
| DIP (Dependency Inversion Principle) | 고수준·저수준 모두 추상화에 의존 | Abstract Factory, Bridge | new 구체클래스() 직접 생성 |

📢 **섹션 요약 비유**: SOLID 원칙은 건축물의 설계 기준이고, 디자인 패턴은 그 기준을 만족하는 검증된 건축 공법이다.

## 3. 구조 및 동작 원리

각 디자인 패턴이 어떤 SOLID 원칙을 주로 구현하는지 매핑한 표다.

| 패턴 | 분류 | 주요 SOLID 원칙 | 핵심 메커니즘 |
|:---|:---|:---|:---|
| Strategy (전략) | 행위 | OCP, DIP | 알고리즘을 인터페이스로 캡슐화, 런타임 교체 |
| Decorator (데코레이터) | 구조 | OCP, SRP | 기능 추가를 새 클래스로 분리, 중첩 가능 |
| Factory Method (팩토리 메서드) | 생성 | OCP, DIP | 생성 책임을 서브클래스로 위임 |
| Abstract Factory (추상 팩토리) | 생성 | OCP, DIP | 제품군 생성을 추상화 인터페이스로 분리 |
| Bridge (브리지) | 구조 | OCP, DIP | 추상과 구현을 독립된 계층으로 분리 |
| Observer (관찰자) | 행위 | OCP, DIP | 이벤트 발행을 인터페이스로 추상화 |
| Command (커맨드) | 행위 | OCP, SRP | 요청을 객체로 캡슐화, 실행 책임 분리 |
| Adapter (어댑터) | 구조 | ISP | 인터페이스 불일치를 래퍼(Wrapper)로 해소 |

📢 **섹션 요약 비유**: SOLID 원칙이 "집 짓기 규칙"이라면, 패턴은 그 규칙을 만족하면서 벽·지붕·창문을 다는 "표준 시공 방법서"다.

## 4. 비교 및 트레이드오프

**전략 패턴과 OCP (Strategy + OCP)**

결제 시스템에서 결제 수단(카드, 계좌이체, 간편결제)을 추가할 때마다 `PaymentService` 클래스를 수정하는 설계는 OCP를 위반한다. `PaymentStrategy` 인터페이스를 도입하고 각 결제 수단을 별도 클래스로 구현하면, 새 결제 수단 추가는 새 클래스 작성만으로 완료된다. 기존 `PaymentService`는 단 한 줄도 수정하지 않는다.

**추상 팩토리 패턴과 DIP (Abstract Factory + DIP)**

데이터 접근 계층에서 `OrderService`가 `new MySQLOrderRepository()`를 직접 생성하면 DIP를 위반한다. `OrderRepository` 인터페이스를 정의하고 DI (Dependency Injection, 의존성 주입) 프레임워크로 구현체를 주입하면, `OrderService`는 추상화에만 의존하게 된다. 이후 Oracle·NoSQL로의 전환이 서비스 코드 변경 없이 구현체 교체만으로 가능해진다.

**코드 리뷰에서의 OCP/DIP 체크 포인트**
- `instanceof` 또는 `if-else if-else` 타입 분기: OCP 위반 신호
- `new ConcreteClass()` 직접 생성: DIP 위반 신호
- 인터페이스 없이 구체 클래스 매개변수로 받는 메서드: DIP 위반 신호

📢 **섹션 요약 비유**: OCP를 지키는 코드는 새 기능을 추가할 때 기존 코드를 읽지 않아도 되는 코드고, DIP를 지키는 코드는 구현체를 교체해도 다른 코드가 컴파일 오류를 내지 않는 코드다.

## 5. 실무 적용 및 최적화 기법

OCP와 DIP를 디자인 패턴과 연결해 이해하면 얻는 효과:

- **변경 비용 최소화**: OCP 준수로 기능 확장 시 기존 코드 수정·재테스트 범위가 최소화된다.
- **교체 용이성**: DIP 준수로 구현체(DB, 외부 API, 라이브러리) 교체 시 영향 범위가 추상화 경계 내로 제한된다.
- **테스트 용이성**: DIP는 테스트 더블(Test Double) 주입을 가능하게 하여 단위 테스트를 쉽게 만든다.
- **설계 회화력**: 패턴을 원칙과 연결해 설명하면 기술사 논문·구술에서 설득력이 높아진다.

기술사 출제 포인트: "전략 패턴이 OCP를 어떻게 구현하는가", "DIP를 위반하는 코드를 개선하는 방법" 등이 자주 출제된다. 패턴 이름만 암기하지 말고 "어떤 원칙을 왜 만족하는가"를 설명할 수 있어야 한다.

📢 **섹션 요약 비유**: 패턴은 원칙을 지키는 검증된 레시피다 — 요리(원칙)를 맛있게 만드는 방법(패턴)을 알면, 새 재료(요구사항)가 들어와도 요리를 망치지 않는다.

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | SOLID 원칙 | 객체지향 설계의 5가지 핵심 지침 |
| 핵심 원칙 | OCP (Open-Closed Principle) | 확장 열림·수정 닫힘의 설계 원칙 |
| 핵심 원칙 | DIP (Dependency Inversion Principle) | 추상화를 통한 의존 방향 역전 원칙 |
| 구현 패턴 | Strategy (전략 패턴) | OCP를 알고리즘 교체로 구현 |
| 구현 패턴 | Abstract Factory (추상 팩토리) | DIP를 제품 생성 추상화로 구현 |
| 연관 개념 | DI (Dependency Injection) | DIP 구현의 실질적 메커니즘 |
| 연관 개념 | IoC (Inversion of Control) | DIP의 실행 제어 역전 개념 |

### 👶 어린이를 위한 3줄 비유 설명

- OCP는 레고처럼 새 블록을 추가할 수 있지만, 이미 만든 성의 기초는 건드리지 않는 규칙이에요.
- DIP는 스마트폰 충전기가 특정 폰 모양이 아닌 표준 USB 규격으로 만들어져야 하는 것처럼, 코드도 표준 인터페이스에만 의존해야 해요.
- 디자인 패턴은 이 두 규칙을 지키면서 프로그램을 만드는 "선배 개발자들이 검증한 레시피"예요.
