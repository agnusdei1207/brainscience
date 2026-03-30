+++
weight = 609
title = "클린 아키텍처"
description = "클린 아키텍처의 개념, 의존성 규칙,同心円 구조"
date = 2024-01-22

[extra]
categories = ["studynote-software-engineering"]
+++

# 클린 아키텍처 (Clean Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 클린 아키텍처는 로버트 C. 마틴(Uncle Bob)이 2012년 제안한 소프트웨어 설계 방법론으로, 시스템을同心円(Layered Circles) 구조로 구성하여 핵심 업무 로직(Enterprise Business Rules)이 외부 infrastructure에 의존하지 않도록 한다.
> 2. **가치**: 의존성 역전 원칙(Dependency Inversion Principle)을 적용하여 프레임워크, 데이터베이스, UI 등의 외부 요소가 변해도 핵심业务逻辑は影響を受けない强壮한 구조를 만든다.
> 3. **융합**: 클린 아키텍처의 원리는 DDD의 Onion Architecture, Hexagonal Architecture와 상호 보완적이며, MSA에서 서비스 내부 구조를 설계하는 기본 프레임워크로 적용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: 클린 아키텍처는 소프트웨어 시스템을同心円の層(Circle)으로 구성하고, 가장 중심에 **엔티티(Entities,Enterprise Business Rules)**를 배치하며, 외부로 갈수록 **메커니즘(Mechanisms)** 즉 구체적인 구현-details가 위치하는 구조다. 핵심 원칙은 **의존성 규칙(Dependency Rule)**으로, "외부 원은 내부 원에 의존할 수 있지만, 내부 원은 외부 원을 알지 못한다"는 것이다. 이를 통해 프레임워크, 데이터베이스, UI 등 자주 변하는 외부 요소가 핵심业务逻辑에 영향을 미치지 않도록 한다.

- **필요성**: 전통적 계층화 아키텍처에서 프레젠테이션 계층(예: Spring MVC)이 비즈니스 로직 계층에 의존하는 것은 자연스럽지만, 비즈니스 로직이 프레젠테이션이나 인프라에 직접 의존하게 되면(예: DAO를 service에서 new 키워드로 직접 생성), 프레젠테이션 기술 변경이나 데이터베이스 전환 시 비즈니스 로직까지 수정해야 하는 상황이 발생한다. 클린 아키텍처는 이러한 의존성 방향을 역전시켜, 비즈니스 로직이 외부 details를 모르면서도 외부를 사용할 수 있게 한다.

- **💡 비유**: 클린 아키텍처는 **러시아 인형(마트료시카)**과 같습니다. 가장 작은 인형(핵심業務邏輯)이 맨 중심에 있고, 점점 큰 인형(프레임워크, UI, DB)이 바깥을 감싸고 있습니다. 바깥의 큰 인형을 바꿔도(UI 변경) 안의 작은 인형(핵심 로직)은 전혀影響받지 않습니다.

- **등장 배경 및 발전 과정**:
  1. **2012년 클린 아키텍처의 제안**: 로버트 C. 마틴이 "Clean Architecture"라는 제목으로 자신의 블로그에同心円 구조를 게시했다.

  클린 아키텍처의同心|timezone 구조를 시각화하면 다음과 같다.

  ```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    클린 아키텍처 同心|timezone 구조                     │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │                        ┌───────────────────────┐                   │
  │                    ┌───┤   Entities           ├───┐               │
  │                    │   │ (Enterprise         │   │               │
  │                    │   │  Business Rules)     │   │               │
  │                    │   └───────────────────────┘   │               │
  │                    │                               │               │
  │                ┌───┴───────────────────────────┴───┐               │
  │            ┌───┤      Use Cases                  ├───┐           │
  │            │   │   (Application                   │   │           │
  │            │   │    Business Rules)                │   │           │
  │            │   └───────────────────────────┴───┘   │               │
  │            │                                       │               │
  │        ┌───┴───────────────────────────────┴───┐   │               │
  │    ┌───┤      Interface Adapters              ├───┐   │           │
  │    │   │  ┌────────┐  ┌────────┐  ┌────────┐ │   │   │           │
  │    │   │  │ MVC    │  │ Present│  │ Gateway│ │   │   │           │
  │    │   │  │ Views  │  │ ers    │  │ Tests  │ │   │   │           │
  │    │   │  └────────┘  └────────┘  └────────┘ │   │   │           │
  │    │   └───────────────────────────────┴───┘   │               │
  │    │                                               │               │
  │┌───┴───────────────────────────────────────────┴───┐   │           │
  ││          Frameworks & Drivers                    ├───┐   │       │
  ││  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐│   │   │       │
  ││  │Web      │  │ DB      │  │ External│  │ Logger  ││   │   │       │
  ││  │Server   │  │ (MySQL, │  │ APIs    │  │ (Log4j) ││   │   │       │
  ││  │(Tomcat) │  │ Oracle) │  │         │  │         ││   │   │       │
  ││  └─────────┘  └─────────┘  └─────────┘  └─────────┘│   │   │       │
  │└───────────────────────────────────────────────────┴───┘           │
  │                                                                     │
  │                                                                     │
  │  의존성 방향:                                                       │
  │                                                                     │
  │  외부 원 ──의존──▶ 내부 원 (에외: 의존성 역전으로 포트 인터페이스)     │
  │                                                                     │
  │  ┌─────────────────────────────────────────────────────────────┐   │
  │  │ 핵심 규칙: 외부 것은 내부 것을 모르지만,                          │   │
  │  │           내부 것은 외부 것을알 수 있다 (의존성 역전 사용 시)        │   │
  │  └─────────────────────────────────────────────────────────────┘   │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
  ```

  **[다이어그램 해설]** 클린 아키텍처의同心|timezone은 4개의 주요 원으로 구성된다. 가장 중심에는 Entities(기업 비즈니스 규칙)이 있으며, 이는 애플리케이션에 독립적으로 존재하는 핵심 업무 규칙이다. 두 번째 원에는 Use Cases(애플리케이션 비즈니스 규칙)가 있으며, 시스템의 유스케이스를 표현한다. 세 번째 원에는 Interface Adapters(MVC의 Controller/Presenter, Gateway 등)가 있으며, 데이터 형식을 변환하고 외부와 내부 사이의 어댑터 역할을 한다. 가장 바깥쪽에는 Frameworks & Drivers(DB, Web Server, External API 등)가 있으며, 구체적인 구현-details가 위치한다. 핵심 의존성 규칙은 "외부 원은 내부 원에 의존하지만, 내부 원은 외부 원을 모르onos"이다. 이를 실현하기 위해 외부 infrastructure을 접근하는 Interface(Port)를 내부 원에 정의하고, 외부 원에서 그 Interface를 구현하는方式来耦合を反転시킨다. 예를 들어, Use Cases가 데이터베이스를 직접 모르더라도, Repository 인터페이스(포트)를 통해 데이터에 접근할 수 있다.

  2. **Hexagonal Architecture와의 관계**: 2005년 Alistair Cockburn이 제안한 Hexagonal Architecture(Ports and Adapters)와 클린 아키텍처는思想적으로相互 보완적이다. Cockburn은 "어떤 기술이든 상관없이Business logic을 중앙에 두고, 어댑터를 통해 외부와 연결한다"는 동일한 원칙을 제시했다.

  3. **DDD와의 융합**: DDD의 Application Service, Domain Service, Repository 패턴이 클린 아키텍처의 Use Cases, Entities, Interface Adapter에 대응된다.

- **📢 섹션 요약 비유**: 클린 아키텍처는 **핵발전소**와 같습니다. 원자炉(핵심業務邏輯)는 가장 중심에 있고, 그周りに多重 防護壁(각 Layer)이 있어 밖에서 무슨 일이 있어炉は影響を受けません.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Entities** | 기업 전체 적용 규칙 | 도메인 객체, 비즈니스 규칙 | Domain Class, Business Rule | 설계도 |
| **Use Cases** | 애플리케이션 고유 규칙 | 유스케이스 구현,业务流程 관리 | Application Service, Command Handler | 레시피 |
| **Interface Adapters** | 데이터 변환 | 포트-어댑터 패턴, MVC 구현 | Controller, Presenter, Gateway | 조리 도구 |
| **Frameworks & Drivers** | 외부 도구 연결 | DB, Web, External API 연동 | Spring, Hibernate, Express.js | 재료와 조리 기기 |
| **Ports** | 내부-외부 연결 Interface | 추상 인터페이스 정의 | Repository Interface, Service Interface |厨房入口 |
| **Adapters** | 포트 구현체 | 구체적 기술로 포트 구현 | JPA Repository, REST Client |調理士 |

---

### 의존성 역전 원칙 적용: Repository 패턴

클린 아키텍처에서 핵심적인 의존성 역전의 예가 Repository 패턴이다. Use Cases(내부 원)는 데이터베이스(외부 원)의 구체적 구현을 모르onos, Repository Port(추상 인터페이스)만 의존한다. 실제 DB 연동은 Infrastructure Layer(외부 원)에서 구현한다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│              클린 아키텍처 의존성 역전: Repository 패턴                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [내부 원 (Entities, Use Cases)]                                     │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  // Domain/Entity ( Entities 원)                             │   │
│  │  public class Order {                                       │   │
│  │      private OrderId id;                                    │   │
│  │      private Money total;                                    │   │
│  │  }                                                          │   │
│  │                                                             │   │
│  │  // Domain/Port ( Repository용 추상 Interface)               │   │
│  │  // 핵심: 이 인터페이스가 내부 원에 존재함                    │   │
│  │  public interface OrderRepository {                         │   │
│  │      Order findById(OrderId id);                            │   │
│  │      void save(Order order);                               │   │
│  │      List<Order> findByCustomer(CustomerId customerId);     │   │
│  │  }                                                          │   │
│  │                                                             │   │
│  │  // Application/UseCase ( Use Cases 원)                     │   │
│  │  public class CreateOrderUseCase {                         │   │
│  │      private final OrderRepository repository;  // 추상에만 의존│   │
│  │                                                             │   │
│  │      public CreateOrderUseCase(OrderRepository repository) │   │
│  │          this.repository = repository;                      │   │
│  │      }                                                      │   │
│  │                                                             │   │
│  │      public void execute(CreateOrderCommand cmd) {         │   │
│  │          Order order = new Order(...);                     │   │
│  │          repository.save(order);  // 구체 구현을 모름          │   │
│  │      }                                                      │   │
│  │  }                                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │ (의존)                                 │
│                              ▼ (역전: 구현체은 Infrastructure에)       │
│  [외부 원 (Infrastructure, Frameworks)]                              │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  // Infrastructure/Persistence/Adapter ( Adapter)           │   │
│  │                                                             │   │
│  │  // JPA 구현: ORM을 사용하는 구체적 어댑터                    │   │
│  │  public class JpaOrderRepository implements OrderRepository {│   │
│  │      @PersistenceContext                                    │   │
│  │      private EntityManager em;                              │   │
│  │                                                             │   │
│  │      @Override                                              │   │
│  │      public Order findById(OrderId id) {                  │   │
│  │          return em.find(OrderEntity.class, id.value());    │   │
│  │      }                                                      │   │
│  │  }                                                          │   │
│  │                                                             │   │
│  │  // Mock 구현: 테스트용 어댑터                                 │   │
│  │  public class InMemoryOrderRepository implements OrderRepo..│   │
│  │      private Map<OrderId, Order> store = new HashMap<>(); │   │
│  │      // ...                                                │   │
│  │  }                                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  [의존성 방향]                                                       │
│                                                                     │
│  UseCase ──의존──▶ OrderRepository ( Port)                          │
│       │                                                              │
│       │               (의존성 역전)                                  │
│       ▼                                                              │
│  JpaOrderRepository ( Adapter)가 Port를 구현                         │
│                                                                     │
│  ✅ 중요: UseCase는 더미 구현체로 테스트 가능                         │
│  ✅ 중요: JPA → MongoDB 전환 시 UseCase 수정 불필요                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 클린 아키텍처에서 Repository 패턴의 핵심은 "추상화는 내부 원에, 구현은 외부 원에" 위치한다는 것이다. OrderRepository 인터페이스(포트)는 Domain/Entity Layer(내부 원)에 정의되어 있어 프레임워크나 데이터베이스 기술이 변경되어도影響받지 않는다. UseCase(CreateOrderUseCase)는 이 추상에만 의존하며, 구체적 구현(JpaOrderRepository, InMemoryOrderRepository)을 모르anos. JpaOrderRepository는 Infrastructure/Persistence Layer(외부 원)에 존재하며, OrderRepository Port를 구현한다. 이 구조의最大的 장점은 테스트 용이성이다. CreateOrderUseCase를 테스트할 때 실제 DB 대신 InMemoryOrderRepository를 주입하면 단위 테스트가 가능하다. 또한 JPA에서 MongoDB로 데이터베이스를 변경하더라도 UseCase의 코드는 전혀 수정할 필요 없이 Adapter만 교체하면 된다.

---

### 각 Layer 간 데이터 흐름

클린 아키텍처에서 요청이 처리되는 전체 흐름을 시각화하면 다음과 같다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                 클린 아키텍처 데이터 흐름 전체 과정                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. [HTTP 요청] ──▶ [Frameworks & Drivers]                          │
│                          │ (톰캣/스프링이 HTTP 수용)                   │
│                          ▼                                           │
│  2. [Interface Adapters: Controller]                                 │
│                          │ (요청을 UseCase가 이해하는 포맷으로 변환)    │
│                          ▼                                           │
│  3. [Use Cases: Application Service]                                 │
│                          │ (업무 규칙 적용, 엔티티 조작)               │
│                          │ (필요 시 도메인 서비스 호출)                 │
│                          ▼                                           │
│  4. [Entities: Domain Object]                                        │
│                          │ (핵심 비즈니스 규칙 실행)                    │
│                          ▼                                           │
│  5. [Ports: Repository Interface]                                   │
│                          │ (추상 인터페이스 호출만)                     │
│                          ▼                                           │
│  6. [Interface Adapters: Gateway]                                   │
│                          │ (Port 구현체 선택, 데이터 변환)             │
│                          ▼                                           │
│  7. [Frameworks & Drivers: DB]                                       │
│                          │ (실제 DB에 SQL 실행)                       │
│                          ▼                                           │
│  8. [응답 복귀]: DB → Gateway → UseCase → Controller → HTTP 응답    │
│                                                                     │
│  예시: 주문 생성 요청                                                │
│                                                                     │
│  POST /orders { "customerId": "C001", "items": [...] }              │
│       │                                                             │
│       ▼                                                             │
│  OrderController.createOrder(OrderRequest)                           │
│       │                                                             │
│       ▼                                                             │
│  CreateOrderUseCase.execute(CreateOrderCommand)                     │
│       │                                                             │
│       ├──▶ OrderRepository.save(order)  (Port)                     │
│       │                                                             │
│       └──▶ JpaOrderRepository.save(order)   (Adapter)              │
│                    │                                                │
│                    ▼                                                │
│               MySQL DB에 INSERT                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 전체 데이터 흐름은 외부(Frameworks)로부터 시작하여 내부를 향해 진행하다가, 다시 외부를 향해 복귀하는 折り返し構造를 취한다. HTTP 요청이 들어오면 Frameworks & Drivers Layer의 Web Server(Spring MVC)가 이를 수용하고, Controller(Interface Adapter)가 요청을 분석하여 UseCase가 이해하는 포맷의 Command 객체로 변환한다. UseCase는 엔티티를 생성하고, Repository Port를 호출하여 데이터를 저장하도록 지시한다. Repository Port는 Infrastructure Layer의 구체적 Adapter(JPA, MongoDB, InMemory 등) 중 어느 것을 사용할지 Interface만 정의하며, 실제 실행은 Adapter에서 이루어진다. 응답 시에는 이 과정을 역순으로 진행하여 최종적으로 HTTP 응답이 반환된다. 이러한 흐름에서 핵심은 각 Layer가 "자기보다 안쪽의 것"만 알ant라는 의존성 규칙이다.

- **📢 섹션 요약 비유**: 클린 아키텍처는 **호텔의 객실 탐방**과 같습니다. 손님(사용자)이前台(Frameworks)에 탐방을 요청하면,礼宾宾客が客室の案内步骤(Use Cases)을 수행하고, 각 객실(Entities)의 규칙에 따라 작동하며,戻る際に同じ路径を辿ります.フロント的工作人员(Adapter)는手順の詳細を知っているだけで，部屋のlocksmith(Entities)를直接操作する必要はありません。

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: 클린 아키텍처 vs 계층화 vs DDD

| 비교 항목 | 클린 아키텍처 | 전통적 계층화 | DDD |
|:---|:---|:---|:---|
| **의존성** | 안쪽 → 바깥쪽 (의존성 규칙) | 위 → 아래 (계층 간) | Bounded Context별 |
| **핵심 분리** | 업무 규칙 vs 구현 | Concern별 | 도메인 모델 vs 인프라 |
| **변경 영향** | 외부 변경 → 내부 무관 | 상위 변경 → 하위 영향 | Context 변경 → 독립 |
| **테스트 용이성** | 매우 높음 (내부 무관) | 보통 | 높음 |

- **📢 섹션 요약 비유**: 클린 아키텍처는 **도시 지하철 노선도**와 같습니다. 환승역(Port)이 중간에 있어서, 한 노선이 끊어져도(프레임워크 변경) 다른 노선(업무 로직)은 영향받지 않으며, 환승駅(Adapter)만 조정하면 됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 프레임워크 전환 (Spring MVC → Quarkus)**: Entity, UseCase, Repository Port가 내부 원에 잘 분리되어 있다면, Web 프레임워크를 Spring MVC에서 Quarkus로 전환할 때 Entity와 UseCase는 전혀 수정할 필요 없이, Controller와 Adapter만 수정하면 된다.

### 도입 체크리스트
- **기술적**: 의존성 규칙(외부는 내부를 모르onos)이 강제되고 있는가? 포트-어댑터 패턴이 적용되어 있는가?
- **운영·보안적**: 단위 테스트가 외부 infrastructure 없이 실행 가능한가?

### 안티패턴
- **순환 의존성**: UseCase가 ServiceA와 ServiceB를互相 호출하여 순환 의존성이 발생하는安티패턴.
- **Fat UseCase**: UseCase에 너무 많은 책임이 집중되어 도메인 로직이 사실상 없는安티패턴.

- **📢 섹션 요약 비유**: 클린 아키텍처에서 순환 의존성이 생기면 **계곡의 두 마을**처럼 서로가 서로를 기다리는 상황처럼 아무것도 진행되지 않는 마비 상태에 빠집니다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망
- **코드 생성 도구와의 결합**: 클린 아키텍처의 템플릿 구조(Entities, UseCases, Adapters)가 정형화되어 있어, CQRS 코드 생성, 스캐폴딩 도구와 결합하여 개발 초기 속도를 높이는 접근이 주목받고 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **의존성 역전 원칙 (DIP)** | 고수준 모듈이 저수준 모듈의 추상에 의존하게 하여 결합도를 낮추는 설계 원칙이다. |
| **포함-역전 원칙 (IoC)** | 의존성 주입, Strategy 패턴 등을 통해 객체의 생성/연결을 외부에 위임하는 설계 원칙이다. |
| **헥사고날 아키텍처** | 클린 아키텍처와 동일한 목적으로, Business logic을 중앙에 두고 포트-어댑터로 외부와 연결한다. |
| **단일 책임 원칙 (SRP)** | 클래스가 하나의 변경 이유만 가져야 하는 원칙으로, 클린 아키텍처의Layer 분리 근거가 된다. |
| **인터페이스 분리 원칙 (ISP)** | 큰 인터페이스보다 작은 구체적인 인터페이스를 우선시하는 원칙으로, 포트 설계에 적용된다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. 클린 아키텍처는 **러시아 인형(마트료시카)**과 같습니다. 제일 작은 인형(핵심業務邏輯)이 맨 안에 있고, 점점 더 큰 인형(프레임워크, UI)이 바깥을 감싸고 있어요.
2. 바깥의 큰 인형을 다른 색이나 모양으로 바꿔도(UI 변경) 안의 작은 인형(핵심 로직)은 전혀 영향받지 않아요.
3. 만약 인형들이 다 들러붙어 있으면(강결합) 한 인형을 빼려고 해도全部를拆分해야 하지만, 마트료시카처럼 되면 원하는 것만 빼고 넣을 수 있어서 매우 편리해요!
