+++
title = "헥사고날 아키텍처"
description = "헥사고날 아키텍처(Ports and Adapters)의 개념과 클린 아키텍처와의 관계"
date = 2024-01-23
weight = 610

[taxonomies]
subjects = ["software-engineering"]
authors = ["brainscience"]
+++

# 헥사고날 아키텍처 (Hexagonal Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 헥사고날 아키텍처는 2005년 Alistair Cockburn이 제안한 설계 패턴으로, 업무 핵심 로직(Business Logic)을 중앙에 두고, 포트(Port)와 어댑터(Adapter)를 통해 외부와 연결하는 구조다.
> 2. **가치**: 외부 기술(데이터베이스, UI, 외부 API)이 변경되어도 업무 핵심 로직을 수정할 필요 없이 어댑터만 교체하면 되므로, 시스템의 진화성과 테스트 용이성이 크게 향상된다.
> 3. **융합**: 클린 아키텍처와思想적으로同一이며, DDD의 Repository 패턴, 포트-어댑터 패턴과 직접적으로 연결된다. MSA에서 서비스 내부 구조 설계의 기본 프레임워크로 활용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: 헥사고날 아키텍처는 "포함-역전(Inversion of Control)"의 원리를 구조적으로 표현한 설계 패턴이다. Alistair Cockburn은 2005년 자신의 블로그에서 "이 패턴의 핵심은、外部와 Business logic 사이의 연결고리를 명명된 포트(Named Port)와 어댑터(Adapter)로 분리하는 것"이라고 정의했다. 六角形(Hexagon)은 문서에서 도형을 그린 데서 유래했으며, 실제로는 형태가 아니라 연결 구조가 중요하다. 내부에는 업무 핵심 로직이, 각 변(Edge)에는 포트가, 외부에는 어댑터가 위치한다.

- **필요성**: 전통적Architecture에서 Business Logic이 직접 데이터베이스, UI 프레임워크, 외부 API에 의존하게 되면, 기술 변경 시 Business Logic까지 수정이 필요해진다. 예를 들어, MySQL에서 MongoDB로 전환하려면 Business Logic이 SQL에 묶여 있다면 상당 부분 재작성해야 한다. 헥사고날 아키텍처는 Business Logic이 외부 기술의-details를 모르onos, 포트라는 추상 인터페이스를 통해 외부와通信하게 함으로써, 이러한 강결합을 해소한다.

- **💡 비유**: 헥사고날 아키텍처는 **호텔 전산 시스템**과 같다. 호텔管理软件(핵심 로직)는客房预约、결제, 손님 관리 등의 업무를 처리하는데, 실제 결제는 신한카드, 삼성카드 등 다양한 카드사(어댑터) 중 어느 것으로 하든 상관없다.软件的.paymentProcessor接口只要接受信用卡信息即可，具体由哪个卡公司处理是通过适配器连接的。

- **등장 배경 및 발전 과정**:
  1. **2005년 헥사고날 아키텍처 탄생**: Alistair Cockburn이 "Ports and Adapters Architecture"라는 이름으로 처음 소개했다.

  헥사고날 아키텍처의 기본 구조를 시각화하면 다음과 같다.

  ```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                 헥사고날 아키텍처 기본 구조                           │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │                         ┌─────────────┐                            │
  │                    ╱                         ╲                        │
  │                   ╱    Business Logic       ╲                       │
  │                  ╱      (Hexagon Core)       ╲                      │
  │                  │                            │                      │
  │                  │  - Domain Services        │                      │
  │                  │  - Domain Objects         │                      │
  │                  │  - Business Rules         │                      │
  │                  │  - Value Objects          │                      │
  │                  ╲                            ╱                      │
  │                   ╲                          ╱                       │
  │                    ╲                        ╱                        │
  │                     ┌──────────────────────┐                      │
  │                     │     _ports_          │                      │
  │                     │  (기술로부터 분리된    │                      │
  │                     │   接口 정의)           │                      │
  │                     └──────────────────────┘                      │
  │                                                                     │
  │    ┃ Persistence ┃    ┃     UI      ┃    ┃  External  ┃           │
  │    ┃   Port      ┃    ┃    Port      ┃    ┃   API     ┃           │
  │    ┃  (저장)    ┃    ┃   (표시)     ┃    ┃  Port     ┃           │
  │         ┃              ┃               ┃         ┃                ┃
  │         ▼              ▼               ▼         ▼                ┃
  │    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐           ┃
  │    │ JPA    │    │  REST  │    │Payment │    │  SMS   │           ┃
  │    │Adapter │    │Adapter │    │Adapter │    │Adapter │           ┃
  │    │ (MySQL)│    │(Spring)│    │(Stripe)│    │(Twilio)│           ┃
  │    └────────┘    └────────┘    └────────┘    └────────┘           ┃
  │                                                                     │
  │  핵심 규칙:                                                        │
  │  • Business Logic은 포트만 호출 (외부 기술 모름)                     │
  │  • 어댑터는 특정 포트를 구현 (기술 연결)                             │
  │  • 외부 기술 변경 시 해당 어댑터만 교체 → Business Logic 무관       │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
  ```

  **[다이어그램 해설]** 헥사고날 아키텍처에서 六角形(Hexagon)은 Business Logic의 경계를 나타내며, 내부에는 도메인 객체, 도메인 서비스, 비즈니스 규칙이 위치한다. 六角形의 각 변(Edge)에는 포트가 정의되어 있으며, 포트는 "무역항"처럼 Business Logic과 외부 세계가 만나는 接口를 의미한다.Persistence Port는 데이터 저장소의 추상接口이고, UI Port는 사용자 인터페이스의 추상接口이며, External API Port는 외부 서비스의 추상Interface이다. 각 포트의 외부에는 해당 포트를 구현하는 어댑터가 위치한다. JPA Adapter는 Persistence Port를 구현하여 MySQL과 연결하고, REST Adapter는 UI Port를 구현하여 HTTP 요청을 처리하며, Stripe Adapter는 Payment Port를 구현하여 외부 결제 서비스와 연결한다. 핵심 규칙은 Business Logic이 포트만 호출하고 구체적 어댑터를 모르onos다는 것이다. 이 구조에서 외부 기술 변경(예: MySQL → PostgreSQL)은 해당 어댑터 교체만으로 해결된다.

  2. **2012년 클린 아키텍처와의 통합**: 로버트 C. 마틴의 클린 아키텍처가 헥사고날 아키텍처와同一의 설계 철학을 공유하며 상호 보완적 관계가 되었다.

  3. **DDD와의 결합**: DDD의 Repository 패턴, Application Service 패턴이 헥사고날의 포트-어댑터 패턴과 직접 매핑되며, DDD의战略적 설계가 헥사고날의 외부 경계 설계에 적용된다.

- **📢 섹션 요약 비유**: 헥사고날 아키텍처는 **범용 건전지 커넥터**와 같습니다. 건전지(업무 로직)는 단일 규격의 커넥터(포트)를持ち, 다양한 기기(어댑터)가 그 커넥터에 연결됩니다. 기기가壊れても新しい 기기를 연결하면 되며, 건전지 자체는更换할 필요가 없습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Business Logic (Hexagon Core)** | 업무 규칙 및 결정 로직 | 도메인 객체 조작,业务流程 실행, 규칙 적용 | Domain Service, Entity, Rule Engine | 전기 모터 |
| **Port (입구)** | 외부에서 내부로 들어오는 接口 | 입력 검증, 요청 포맷 정의, 인터페이스 선언 | Driving Port, Input Port | 모터의 입력 단자 |
| **Port (출구)** | 내부에서 외부로 나가는 接口 | 데이터 조회, 외부 서비스 호출, 기술 추상화 | Driven Port, Output Port | 모터의 출력 단자 |
| **Driving Adapter** | 포트를 호출하는 어댑터 | 사용자 요청을 포트로 전달 | REST Controller, CLI, UI Event Handler | 전원 스위치 |
| **Driven Adapter** | 포트를 구현하는 어댑터 | 포트 Interface를 구현하여 외부 기술 연결 | JPA Repository, REST Client, Message Producer | 발전기 |

---

### Driving Port vs Driven Port (입구 포트 vs 출구 포트)

헥사고날 아키텍처에서 포트는 방향에 따라 두 가지로 나뉜다. Driving Port(입구 포트)는 외부에서 내부 Business Logic을 호출하는 接口이고, Driven Port(출구 포트)는 Business Logic이 외부를 호출하기 위해 사용하는 接口다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                  Driving Port vs Driven Port                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [Driving Port (입구 포트)]                                         │
│                                                                     │
│  • 외부에서_application의 기능을 호출하는 接口                         │
│  • Application Service가implemented하는 인터페이스                    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  // Hexagon Core                                            │   │
│  │                                                             │   │
│  │  // Driving Port (입구 포트) - Application Service Interface │   │
│  │  public interface OrderServicePort {                        │   │
│  │      OrderResponse createOrder(OrderRequest request);       │   │
│  │      OrderResponse cancelOrder(OrderId orderId);           │   │
│  │  }                                                          │   │
│  │                                                             │   │
│  │  // Business Logic Implementation                            │   │
│  │  public class OrderService implements OrderServicePort {    │   │
│  │      private final PaymentGatewayPort paymentGateway;       │   │
│  │      private final InventoryPort inventory;                 │   │
│  │                                                             │   │
│  │      @Override                                              │   │
│  │      public OrderResponse createOrder(OrderRequest req) {   │   │
│  │          // Business Logic: 도메인 규칙 적용                  │   │
│  │          Order order = new Order(...);                      │   │
│  │          inventory.reserve(order.getItems());              │   │
│  │          paymentGateway.charge(order.getTotal());           │   │
│  │          return OrderResponse.from(order);                  │   │
│  │      }                                                      │   │
│  │  }                                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              │ OrderServicePort 구현                 │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  // Driving Adapter (입구 어댑터) - REST Controller           │   │
│  │  @RestController                                           │   │
│  │  public class OrderController implements OrderServicePort {  │   │
│  │      private final OrderServicePort orderService;           │   │
│  │                                                             │   │
│  │      @PostMapping("/orders")                                │   │
│  │      public OrderResponse createOrder(@RequestBody ...) {   │   │
│  │          return orderService.createOrder(request);         │   │
│  │      }                                                      │   │
│  │  }                                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  [Driven Port (출구 포트)]                                           │
│                                                                     │
│  • Business Logic이 외부 무언가를 호출하기 위해 사용하는 接口         │
│  • 구체적 구현은 외부 어댑터에서 이루어짐                             │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  // Hexagon Core                                            │   │
│  │                                                             │   │
│  │  // Driven Port (출구 포트) -PaymentGateway 추상 Interface   │   │
│  │  public interface PaymentGatewayPort {                     │   │
│  │      void charge(Money amount, PaymentMethod method);       │   │
│  │  }                                                          │   │
│  │                                                             │   │
│  │  // Business Logic Implementation (출구 포트 사용)            │   │
│  │  public class OrderService implements OrderServicePort {    │   │
│  │      private final PaymentGatewayPort paymentGateway;        │   │
│  │      // 구체적 구현을 모르onos, 오직 Port만 알ants            │   │
│  │  }                                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▲                                       │
│                              │ PaymentGatewayPort 구현               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  // Driven Adapter (출구 어댑터) - Stripe 구현체               │   │
│  │  @Component                                                  │   │
│  │  public class StripePaymentAdapter implements PaymentGateway │   │
│  │      @Override                                               │   │
│  │      public void charge(Money amount, PaymentMethod method) {│   │
│  │          // Stripe API 호출 구현                             │   │
│  │          Stripe.charges.create(...);                        │   │
│  │      }                                                      │   │
│  │  }                                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Driving Port와 Driven Port의 차이는 방향과 Ownership에 있다. Driving Port는 외부(UI, API Gateway 등)가application의 기능을 호출하는 接口이며, OrderServicePort가 그 예다. REST Controller(Driving Adapter)가 이 포트를 구현하고, 내부의 OrderService(Implementation)가 호출한다. 이는 "외부에서 내부로"의 흐름이다. Driven Port는application의 Business Logic이 외부 인프라(데이터베이스, 결제 게이트웨이, 메시지 시스템 등)를 호출하기 위해 정의하는 接口이며, PaymentGatewayPort가 그 예다. OrderService는 구체적 구현(Stripe, PayPal 등)을 모르anos, 오직 PaymentGatewayPort 인터페이스만 호출한다. 구체적 구현은 StripePaymentAdapter, PayPalPaymentAdapter 같은 Driven Adapter가 담당한다. 이는 "내부에서 외부로"의 흐름이다. 이 구조의 핵심 가치는, 결제 게이트웨이를 Stripe에서 PayPal로 교체하더라도 Business Logic(OrderService)은 전혀 변경되지 않는다는 점이다.

---

### 헥사고날 아키텍처 vs 클린 아키텍처 vs DDD 비교

세アーキテク처 모두 "업무 로직과 인프라의 분리"라는 동일한 목표를 공유하지만, 접근 방식과 용어에서 차이를 보인다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│           헥사고날 vs 클린 아키텍처 vs DDD 용어 매핑                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │
│  │  헥사고날       │  │  클린 아키텍처   │  │      DDD       │       │
│  │  (Cockburn)    │  │  (Uncle Bob)   │  │   (Evans)      │       │
│  ├────────────────┼────────────────┼────────────────┤       │
│  │ Hexagon Core   │  │ Entities       │  │ Domain         │       │
│  │ (업무 핵심)     │  │ + Use Cases    │  │ + Application  │       │
│  │                │  │ (업무 규칙)     │  │ Service        │       │
│  ├────────────────┼────────────────┼────────────────┤       │
│  │ Driving Port   │  │ -             │  │ Application    │       │
│  │ (입구 포트)     │  │ (Interface    │  │ Service        │       │
│  │                │  │  Adapter)     │  │ (입구)         │       │
│  ├────────────────┼────────────────┼────────────────┤       │
│  │ Driven Port    │  │ Ports         │  │ Repository     │       │
│  │ (출구 포트)     │  │ (추상 인터페이스)│  │ Interface     │       │
│  │                │  │               │  │ (출구)         │       │
│  ├────────────────┼────────────────┼────────────────┤       │
│  │ Driving Adapter│  │ Controllers,  │  │ Controller,   │       │
│  │ (입구 어댑터)   │  │ Presenters    │  │ Command Handler│       │
│  ├────────────────┼────────────────┼────────────────┤       │
│  │ Driven Adapter │  │ Frameworks &  │  │ Repository    │       │
│  │ (출구 어댑터)   │  │ Drivers       │  │ Implementations│      │
│  └────────────────┴────────────────┴────────────────┘       │
│                                                                     │
│  공통점:                                                            │
│  1. 업무 핵심 로직을 외부 기술로부터 분리                             │
│  2. 추상 인터페이스(Port)를 통해 외부 접근                           │
│  3. 외부 기술 변경 시 업무 로직 무관                                 │
│  4. 테스트 용이성 향상                                               │
│                                                                     │
│  차이점:                                                            │
│  • 헥사고날: 포트-어댑터 개념에 집중 (形状自由)                        │
│  • 클린 아키텍처:同心圆柱体 구조와 의존성 규칙 명시                      │
│  • DDD: 도메인 모델링 방법론과 전략적/전술적 설계 구분                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 세アーキテク처 모두 "관심사 분리"와 "결합도 감소"라는 동일한 목표를 공유하며, 용어만 다를 뿐本质적으로 동일한 구조를 나타낸다. 헥사고날 아키텍처는 Port와 Adapter라는 개념에 초점을 맞추어 상대적으로 간단하고 실무적이며, 형태의 제약이 없다(六角形은 단순히 다이어그램에서 도형을 그린 것에 불과). 클린 아키텍처는同心圆柱体(Layer) 구조와 함께 "의존성 규칙"을 명시적으로 강조한다. DDD는 도메인 모델링 방법론으로, Strategic Design(Bounded Context, Ubiquitous Language)과 Tactical Design(Aggregate, Entity, Repository)을 함께 다루며, 도메인 전문가와의 협업 과정까지 포함한다. 실무에서는 세アーキテク처의 장점을 모두 취하여, DDD로 도메인을 모델링하고, 헥사고날/클린 아키텍처로 코드를 구조화하는 것이 일반적이다.

- **📢 섹션 요약 비유**: 헥사고날 아키텍처는 **오디세이 카세트플레이어**와 같습니다. 카세트(업무 로직)의 구멍(Port)은 표준 규격이어서, 어떤 회사 제품(어댑터)이든 사용할 수 있어요. 다만 카세트 플레이어가 고장나면 카세트(업무 로직)를 바꿀 필요 없이 플레이어(어댑터)만 바꾸면 됩니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: 헥사고날 vs 전통적 3계층 vs 클린 아키텍처

| 비교 항목 | 전통적 3계층 | 헥사고날 | 클린 아키텍처 |
|:---|:---|:---|:---|
| **접근** | 기술 관점 분리 | 포트-어댑터 분리 |同心圆柱 분리 |
| **의존성 방향** | 위→아래 강제 | 포트 통해 역전 | 안쪽→바깥쪽 |
| **변경 관리** | 상위 계층 변경→하위 영향 | 외부 기술 변경→어댑터만 | 외부 변경→내부 무관 |
| **테스트** | 전체 계층 테스트 필요 | 포트만 Mock 가능 | 내부 무관 테스트 |

- **📢 섹션 요약 비유**: 전통적 3계층은 **계단식 물 흘러내리듯** 위에서 아래로만 흐르지만, 헥사고날은 **환형 순환系统**처럼 어떤 방향에서든 필요한 곳으로 흘러가게 합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 외부 API 변경 대응**: 외부 배송 서비스 API가 v1에서 v2로 변경될 때, Driven Adapter(ShippingAdapterV1)를 ShippingAdapterV2로 교체하면 Business Logic은 전혀 변경 없이 계속 동작한다.

### 도입 체크리스트
- **기술적**: 포트가 명확히 정의되어 있는가?Driving/Driven 포트가 구분되어 있는가?
- **운영·보안적**: 테스트에서 실제 인프라 대신 Mock 포트를 사용할 수 있는가?

### 안티패턴
- **로우-port 어댑터**: 포트 없이 Business Logic이 직접 외부 기술을 호출하는 안티패턴.

- **📢 섹션 요약 비유**: 헥사고날에서 포트 없이 직접 외부를 호출하면 **전파선 없이 발전기에 직접 코드를 연결**하는 것처럼, 위험하고 관리가 불가능해집니다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망
- **헥사고날 + Serverless**: Serverless 함수(FaaS)에서도 헥사고날 포트-어댑터 패턴을 적용하여, 비즈니스 로직은 동일한 함수를 유지하면서Trigger(어댑터)만 교체하는 접근이 가능해질 전망이다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **의존성 역전 원칙 (DIP)** | 고수준 모듈이 저수준 모듈의 추상에 의존하게 하여 결합도를 낮추는 원칙으로, 헥사고날 포트의 기반이 된다. |
| **포함-역전 (IoC)** | 객체의 생성/연결을 외부(프레임워크/컨테이너)에 위임하는 설계 원칙으로, 헥사고날의 핵심 메커니즘이다. |
| **클린 아키텍처** | 헥사고날과 동일한 설계 철학을 공유하며,同心圆柱構造と依存性規則を強調する。 |
| **DDD의 Repository 패턴** | Driven Port의 대표적인 예로,데이터 액세스를 추상화하여 인프라와 분리한다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. 헥사고날 아키텍처는 **万能 슬롯三口**과 같습니다. 어떤 기기(어댑터)이든 슬롯(포트)에 맞으면 연결할 수 있어서, 기기가 고장 나면 그 기기만 바꾸면 됩니다.
2. 컴퓨터에서 마이크를 사용할 때, 마이크(업무 로직)는 음성 신호를 세 данным образом 처리하는 것에만 집중하고, 컴퓨터에 연결되는 방법(USB, 블루투스 등)은 어댑터가 처리합니다.
3. 그래서 블루투스 마이크를USB 마이크로 바꿔도(어댑터 변경) 마이크의 소리 품질(업무 로직)이 변하지 않습니다!
