+++
title = "도메인 주도의 설계 (DDD)"
description = "DDD의 개념, 전략적 설계, 전술적 설계, Bounded Context"
date = 2024-01-21
weight = 608

[taxonomies]
subjects = ["software-engineering"]
authors = ["brainscience"]
+++

# 도메인 주도의 설계 (DDD, Domain-Driven Design)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DDD는 복잡한 소프트웨어 시스템에서 도메인(업무 영역)의 이해를 설계의 핵심으로 삼고, 도메인 전문가와 개발자가 공유한 언어(Ubiquitous Language)를 통해 모델을 구축하는 소프트웨어 개발 방법론이다.
> 2. **가치**: Eric Evans가 2003년 출간한 "Domain-Driven Design"에서 체계화한 이 방법은, 비즈니스 요구사항을 코드에 직접 반영하여 변경에 강한 시스템을 구축하며, MSA에서 Bounded Context 분해의 기준을 제공한다.
> 3. **융합**: DDD의 전략적 설계(Strategic Design)는 MSA의 서비스 분해에, 전술적 설계(Tactical Design)는 플루언트 API(Fluent API), 애그리게이트(Aggregate), 이벤트 소싱(Event Sourcing) 등의 구현 패턴에 직접 적용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: DDD는 복잡한 비즈니스 도메인의 본질을 모델로 표현하고, 이를 소프트웨어에 반영하는 소프트웨어 개발 방법론이다. Evans는 DDD를 "소프트웨어 프로젝트에서 비즈니스 가치와 기술 복잡성 모두에 대응할 수 있는 핵심 도메인 모델을 구축하기 위한 원칙과 패턴의 مجموعها"로 정의했다. DDD는 크게 전략적 설계(Strategic Design)와 전술적 설계(Tactical Design)로 나뉜다. 전략적 설계는 시스템의 큰 그림을 그리고, 전술적 설계는 코드 수준에서 구현 가능한 패턴을 제공한다.

- **필요성**: 대규모 엔터프라이즈 시스템에서 기술적 복잡성과 비즈니스 복잡성이 얽히면, 시스템을 어떻게 분해해야 할지, 각 모듈의 책임은 무엇으로 해야 할지 결정하기 어렵다. 전통적 분석/설계 방법론은 도메인 전문가의 지식을 소프트웨어 모델로 변환하는 과정에서 많은 정보가 손실된다. DDD는 도메인 전문가와 개발자가 공통의 언어를 사용하고, 이 언어가 코드와 설계에 그대로 반영되도록 하여, 이러한 변환 손실을 최소화한다.

- **💡 비유**: DDD는 **번역사와 외교관의 관계**와 같다. 외국과의 협상에서 번역사(설계자)가 양측의 언어와 문화를 깊이 이해하지 않으면, 협의 사항이 왜곡되어 전달된다. 도메인 전문가(외교관)와 개발자(번역사)가 같은 언어를 사용해 직접 대화하고, 그 언어가 계약서(코드)에 그대로 반영되어야 협상이 제대로 작동한다.

- **등장 배경 및 발전 과정**:
  1. **2003년 DDD의 탄생**: Eric Evans가 "Domain-Driven Design: Tackling Complexity in the Heart of Software"를 출간하여 DDD의 원칙과 패턴을 체계화했다.

  Evans의 DDD分层 구조를 시각화하면 다음과 같다.

  ```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    DDD分层 구조 (Evans의 원서 기준)                     │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  ┌───────────────────────────────────────────────────────────────┐ │
│  │                     전략적 설계 (Strategic Design)                │ │
│  │                                                               │ │
│  │  • Bounded Context: 모델이 적용되는 경계                       │ │
│  │  • Ubiquitous Language: 팀 내 공유 언어                       │ │
│  │  • Context Map: 컨텍스트 간 관계                               │ │
│  │                                                               │ │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │ │
│  │  │ 고객 관리     │  │ 주문 관리     │  │ 결제 관리     │   │ │
│  │  │ Bounded     │  │ Bounded     │  │ Bounded     │   │ │
│  │  │ Context     │  │ Context     │  │ Context     │   │ │
│  │  │              │  │              │  │              │   │ │
│  │  │ Customer    │  │ Order       │  │ Payment     │   │ │
│  │  │ Account     │  │ OrderLine   │  │ Transaction  │   │ │
│  │  │ Address     │  │ Shipment    │  │ Invoice     │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                              │                                      │
│  ┌───────────────────────────┴───────────────────────────────┐   │
│  │                     전술적 설계 (Tactical Design)             │   │
│  │                                                               │ │
│  │  • Aggregate: 일관성 경계 단위                               │   │
│  │  • Entity: 식별성을 가지는 도메인 객체                        │   │
│  │  • Value Object: 불변의 값 객체                              │   │
│  │  • Domain Event: 도메인 사건                                 │   │
│  │  • Repository: Aggregate의Persistence 추상화                │   │
│  │  • Domain Service: 애그리게이트에 넣기 어려운 로직           │   │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
  ```

  **[다이어그램 해설]** Evans의 DDD는 전략적 설계와 전술적 설계의 2단계로 구성된다. 전략적 설계는 "큰 그림"을 그리는 단계로, 전체 시스템을 Bounded Context로 나누고, 각 Context에서 Ubiquitous Language를 정의하며, Context들 사이의 관계를 Context Map으로 표현한다. 이 단계에서는 기술이 아니라 비즈니스의 본질에 집중한다. 전술적 설계는 전략적으로 정의한 Context 내에서 코드 수준으로 구현하는 단계로, Aggregate, Entity, Value Object, Domain Event, Repository, Domain Service 등의 패턴을 적용한다. 이 단계에서 개발자는 전술적 패턴을 사용하여 도메인 모델을 코드에 반영한다. 중요한 점은 전략적 설계 없이 전술적 설계만 적용하면 기술 중심의 설계에 그치고, 전술적 설계 없이 전략적 설계만 적용하면 구현으로 연결되지 않는다는 것이다.

  2. **DDD의 재조명 (2010년대)**: MSA와 결합하여 DDD의 전략적 설계(특히 Bounded Context)가 서비스 분해의 핵심 기준으로 재조명받았다. Vaughn Vernon의 "Implementing Domain-Driven Design"(2013)과 "Domain-Driven Design Distilled"(2016)가 DDD의 대중화에 기여했다.

- **📢 섹션 요약 비유**: DDD는 **도시 기획사와 건축가**의 관계와 같습니다. 도시 기획사(전략적 설계)가 어느 지역에 상가, 주거지, 공업을 배치할지 계획하면(경계 설정), 건축가(전술적 설계)가 각 건물(애그리게이트, 엔티티)의 구체적인 구조를 설계합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Bounded Context** | 도메인 모델의 유효 경계 | 특정 도메인 용어가 고유한 의미를 가지는 범위 | 마이크로서비스, 모듈 | 도시의 区 |
| **Ubiquitous Language** | 팀 내 공유 언어 | 도메인 전문가와 개발자가 공통으로 사용하는 용어와 문장 | 유스케이스, 도메인 모델, 코드 | 도시의 공식 언어 |
| **Context Map** | 컨텍스트 간 관계 시각화 |上下游 관계, 공유 커널, 소비자-공급자 등을 표현 | C4 Model, AR(Anti-Corruption Layer) | 도시 간 도로망 |
| **Aggregate** | 일관성 경계 단위 | 관련 엔티티와 값 객체를 하나로 묶은 일관성 단위 | 주문 Aggregate, 고객 Aggregate | 아파트 단위 |
| **Entity** | 식별성을 가지는 객체 | 시간이 지나도 동일한 식별성을 유지하는 객체 | Customer, Order | 주민등록번호가 있는 사람 |
| **Value Object** | 불변의 값 객체 | 식별성 없이 값으로만 정의되는 객체 | Money, Address, DateRange | 주소 (위치 자체) |
| **Domain Event** | 도메인에서 발생한 사건 | 과거에 발생한 비즈니스 사건을 표현 | OrderCreated, PaymentFailed | 사건의 기록 |

---

### Bounded Context와 Context Map

Bounded Context는 DDD의 전략적 설계에서 핵심적인概念으로, 특정 도메인 모델이 고유한 의미를 가지는 경계를 의미한다.同一 용어가 다른 Context에서는 다른 의미를 가질 수 있다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    Bounded Context 예: 전자상거래                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────┐   ┌──────────────────────────┐       │
│  │     고객 관리 Context     │   │      주문 관리 Context     │       │
│  │                          │   │                          │       │
│  │  [Customer]              │   │  [Order]                  │       │
│  │   - customerId (식별자)  │   │   - orderId (식별자)     │       │
│  │   - name                 │   │   - customerRef (참조)    │       │
│  │   - email                │   │   - orderLines           │       │
│  │   - customerType         │   │   - shippingAddress      │       │
│  │   - creditRating         │   │   - status               │       │
│  │                          │   │                          │       │
│  │  ※ "Customer"의 의미:    │   │  ※ "Customer"의 의미:    │       │
│  │    전자상거래 플랫폼       │   │    주문을 생성한 사람      │       │
│  │    가입 회원              │   │    (역할로서의 고객)       │       │
│  └──────────────────────────┘   └────────────┬─────────────┘       │
│                                               │                      │
│                                               │ Customer만 참조      │
│                                               │ (공유 없음)          │
│                                               ▼                      │
│  ┌──────────────────────────┐   ┌──────────────────────────┐       │
│  │     결제 관리 Context     │   │       배송 관리 Context     │       │
│  │                          │   │                          │       │
│  │  [Payment]              │   │  [Shipment]              │       │
│  │   - paymentId           │   │   - shipmentId           │       │
│  │   - orderId (참조)       │   │   - orderId (참조)       │       │
│  │   - amount              │   │   - trackingNumber       │       │
│  │   - paymentMethod       │   │   - carrier              │       │
│  │   - paymentStatus       │   │   - estimatedDelivery   │       │
│  │                          │   │                          │       │
│  │  ※ "Order"의 의미:      │   │  ※ "Order"의 의미:      │       │
│  │    결제 대상 주문         │   │    배송 대상 주문         │       │
│  │    (결제 Aggregate에     │   │    (배송 Aggregate에      │       │
│  │     종속)                │   │     종속)                  │       │
│  └──────────────────────────┘   └──────────────────────────┘       │
│                                                                     │
│  Context Map:                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  [고객 관리] ──공급자/소비자──▶ [주문 관리]                  │   │
│  │                                     │                        │   │
│  │                        고객 관리 ──공급자/소비자──▼           │   │
│  │                                             │                │   │
│  │                        고객 관리 ──공급자/소비자──▼           │   │
│  │                                             │                │   │
│  │                        ┌──────────┐  ┌──────────┐            │   │
│  │                        │ 결제 관리 │  │ 배송 관리 │            │   │
│  │                        └──────────┘  └──────────┘            │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 전자상거래 시스템에서 "Customer"라는 개념은 Context에 따라 다른 의미를 가진다. 고객 관리 Context에서 Customer는 플랫폼에 가입한 회원의 전체 프로필(고객 등급, 신용 등급, 이메일 등)이며, 이는 고객 관리 마이크로서비스가全權负责한다. 주문 관리 Context에서 Customer는 "주문을 생성한 사람"이라는 역할에 불과하며, 주문 Aggregate는 고객의 전체 프로필이 아니라 주문에 필요한 정보(주문자 이름, 주소)만 참조한다. 결제 관리 Context에서 Order는 "결제 대상 주문"이라는 역할을 하며, 결제 Aggregate에 종속된다. 중요한 점은 이러한 다른 의미의 Customer, Order가 각 Context 내에서 엄격히 분리되어 있다는 것이다. 이를 통해 특정 Context의 모델이 다른 Context의 내부 정보에 의존하지 않고 독립적으로 진화할 수 있다. Context Map에서는 이러한 Context 간의 관계(공급자/소비자, 공유 커널,anticorruption layer 등)를 표현한다.

---

### 전술적 설계 패턴: Aggregate, Entity, Value Object

DDD의 전술적 설계에서 가장 중요한 패턴이 Aggregate다. Aggregate는 관련 엔티티와 값 객체를 하나의 단위로 묶으며, 이 단위 안에서만 일관성이 보장된다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│              주문 Aggregate (주전술적 설계 예시)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    주문 Aggregate Root                        │   │
│  │                                                             │   │
│  │  public class Order extends AggregateRoot {                  │   │
│  │                                                             │   │
│  │      private OrderId id;        // Aggregate의 식별자       │   │
│  │      private CustomerId customerId;  // 다른 Aggregate 참조  │   │
│  │      private List<OrderLine> lines;  // 엔티티 (내부)        │   │
│  │      private OrderStatus status; // 값 객체 (내부)          │   │
│  │      private Money totalAmount;  // 값 객체                │   │
│  │                                                             │   │
│  │      // Aggregate 루트에만 외부 접근 허용                     │   │
│  │      public void addLine(Product p, int qty) {             │   │
│  │          // 도메인 규칙: 주문 상태가 PENDING时才添加          │   │
│  │          if (this.status != OrderStatus.PENDING) {         │   │
│  │              throw new IllegalStateException(...);          │   │
│  │          }                                                   │   │
│  │          OrderLine line = new OrderLine(p, qty);           │   │
│  │          this.lines.add(line);                              │   │
│  │          this.recalculateTotal();  // 내부 상태 동기화      │   │
│  │          // 도메인 이벤트 발행                                │   │
│  │          registerEvent(new OrderLineAdded(...));            │   │
│  │      }                                                       │   │
│  │                                                             │   │
│  │      // 외부에서는 직접 엔티티 수정 불가 (캡슐화)               │   │
│  │      // order.getLines().add(newLine) => 예외 발생!         │   │
│  │  }                                                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  [값 객체 (Value Object)]                                           │
│                                                                     │
│  public class Money {                                              │
│      private final BigDecimal amount;  // 불변                     │
│      private final Currency currency;                               │
│                                                                     │
│      public Money(BigDecimal amount, Currency currency) {         │
│          if (amount.compareTo(BigDecimal.ZERO) < 0) {              │
│              throw new IllegalArgumentException("음수 불가");       │   │
│          }                                                         │
│          this.amount = amount;                                      │
│          this.currency = currency;                                  │
│      }                                                              │
│                                                                     │
│      // 불변이므로 새로운 Money 객체 반환 (加减)                       │
│      public Money add(Money other) {                               │
│          if (!this.currency.equals(other.currency)) {              │
│              throw new IllegalArgumentException("통화 불일치");    │   │
│          }                                                         │
│          return new Money(this.amount.add(other.amount),           │   │
│                               this.currency);                      │   │
│      }                                                              │
│  }                                                                  │
│                                                                     │
│  핵심 규칙:                                                         │
│  1. Aggregate 루트만이 외부에서 내부 객체 접근을 관리                  │
│  2. Entity는 식별자를 가진다 (equal은 id 기준)                       │
│  3. Value Object은 불변이며, 값으로만 비교 (equal은 모든 필드 기준)   │
│  4. 다른 Aggregate 참조는 ID만 사용 (강결합 방지)                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 주문 Aggregate의 핵심 설계 원칙은 "일관성 경계"다. 주문 Aggregate 내부에는 Order(루트 엔티티), OrderLine(내부 엔티티), Money(값 객체), OrderStatus(값 객체)가 포함된다. 외부에서 주문에 OrderLine을 추가하려면 반드시 Aggregate 루트(Order)의 addLine() 메서드를 호출해야 하며, 직접 Order.lines에 add()하는 것은不允许된다. 이는 Aggregate 내부의 불변식(Invariant)을 Aggregate 루트가 통제한다는 의미다. 예를 들어, 주문 총액(totalAmount)은 OrderLine이 추가되거나 제거될 때마다 자동으로 재계산되어 항상 일관된 상태를 유지한다. 값 객체 Money는 불변으로 설계되어, 덧셈 시 새로운 Money 객체를 반환한다. 이는 다중 스레드 환경에서 동시성 문제를 방지하고, 도메인 객체의 일관성을 지키는 데 중요하다.

- **📢 섹션 요약 비유**: DDD의 Aggregate는 **아파트 관리 규칙**과 같습니다. 외부에서 내 Apartments 시설(공용 시설)을 이용하려면 반드시 관리사무소(Aggregate Root)를 거쳐야 하며, 직접 시설을 점유하거나 변경할 수 없습니다. 이를 통해 아파트 전체의 일관된 운영이 유지됩니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: DDD vs 애자일 vs SOA

| 비교 항목 | DDD | 애자일 (Agile) | SOA |
|:---|:---|:---|:---|
| **초점** | 도메인 모델링 | 프로젝트 관리 | 서비스 Integration |
| **접근** | 도메인 전문가와 협업, 공유 언어 구축 |_iterative 개발, 변화 수용 | 서비스 계약, 표준화 |
| **단위** | Bounded Context, Aggregate | Sprint, User Story | 서비스 |
| **활동** | 컨텍스트 매핑, 모델 리파인먼트 | 일일 스탠드업, 회고 | ESB, 서비스 설계 |

- **📢 섹션 요약 비유**: DDD는 **전문 분야 학술 대회**와 같습니다. 각 분야(도메인) 전문가들이 자신들만의 용어(ubiquitous Language)로 토론하고, 이를 통해 해당 분야(컨텍스트)의知見를深化시킵니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — MSA 전환 시 Bounded Context 결정**: 5년 된 전자상거래 플랫폼을 MSA로 전환할 때, DDD의 Bounded Context를 기준으로 서비스를 분해하면, 기술적 coupling이 아닌 비즈니스 Capability 중심으로 분해가 이루어져 팀별로 자율적으로 개발/배포가 가능해진다.

### 도입 체크리스트
- **기술적**: 도메인 전문가와 개발자 간 긴밀한 협업이 가능한가? 도메인 모델링 시간이 충분한가?
- **운영·보안적**: Aggregate 경계가 일관성 범위와 일치하는가?

### 안티패턴
- **Anemic Domain Model**: 도메인 객체가 데이터를 담는 그저 데이터 클래스(POJO)일 뿐 도메인 로직이 없는安티패턴. Domain Service에 모든 로직이 집중된다.
- **God Aggregate**: 너무 많은 Responsibility을 가진 거대한 Aggregate로, 성능과 동시성 문제의 원인이 된다.

- **📢 섹션 요약 비유**: DDD에서Aggregate를 잘못 설정하면 **아파트 관리사무소**가 너무 많은 역할을 떠담아 감당하지 못하는 것처럼, 시스템도 Aggregate이 비대해지면 오히려 복잡성이 증가하고 성능이 저하됩니다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망
- ** Event Sourcing + DDD의 결합**: DDD의 Aggregate에서 발생하는 Domain Event를 Event Store에 저장하여 시스템의 완전한 변경 이력을 추적하고,任何時間点的 상태를 재구성할 수 있는 Event Sourcing 패턴과의 결합이 주목받고 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Bounded Context** | DDD의 핵심 개념으로, 특정 도메인 모델이 고유한 의미를 가지는 경계를 정의하며 MSA 서비스 분해의 기준이 된다. |
| **Ubiquitous Language** | 도메인 전문가와 개발자가 공유하는 공통 언어로, 이 언어가 코드, 설계, 문서에 걸쳐 일관되게 사용된다. |
| **Aggregate** | 일관성 경계 단위로, 관련 엔티티와 값 객체를 묶고 Aggregate 루트를 통해서만 외부 접근을 허용한다. |
| **CQRS** | DDD와 결합하여 Aggregate의 명령(Aggregate 업데이트)과 查询(프로젝션)를 분리하여 각각 최적화된 모델을 사용한다. |
| **Event Sourcing** | DDD의 Domain Event를 Event Store에 저장하여 완전한 감사 로그와 시스템 재구성을 가능하게 한다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. DDD는 **우리 말로 된 요리법**과 같습니다. 영어로 된 요리법(기술용어)을 그냥 쓰는 대신, 우리 말(공유 언어)로 번역하고, 그 우리 말이 실제 요리(코드)에도 그대로 적용됩니다.
2. 컴퓨터에서 "장바구니에 물건 넣기"도 누가(누가?), 언제(시간), 어디에(어떤 장바구니에) 넣는지 같은 규칙(도메인 규칙)을 정해서 코드를 만드는 것입니다.
3. 다만 도메인 전문가(요리사)와 개발자(레시피 작성자)가 같은 언어를 쓰지 않으면, "반죽을 섞는다"는 말이 요리사에게는 "손으로 섞는다"이지만 개발자에게는 "믹서로 섞는다"가 되어버려서最后에는 전혀 다른 요리가 될 수 있어요!
