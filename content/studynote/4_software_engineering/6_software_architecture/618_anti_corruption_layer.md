+++
weight = 18
title = " Anticorruption Layer 패턴"
description = " Anticorruption Layer(ACL)의 개념, 외부 시스템 Integration"
date = 2024-01-31

[extra]
categories = ["studynote-software-engineering"]
+++

# Anticorruption Layer 패턴 (ACL, Anti-Corruption Layer)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Anticorruption Layer는 서로 다른 도메인 모델을 가진 시스템 간 통합 시, 한 시스템의 도메인 모델이 다른 시스템의 모델에 오염되는 것을 방지하는_adapter layer로, 모델 간 변환을 담당한다.
> 2. **가치**: 레거시 시스템이나 외부 시스템을 새로운 시스템과 통합할 때, 기존 모델의 constraints에 묶이지 않고 깨끗한 도메인 모델을 유지할 수 있게 한다.
> 3. **융합**: DDD의 바운디드 컨텍스트 간 통합, MSA에서 외부 API 연동, 레거시 현대화에서 널리 활용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: Anticorruption Layer는 Eric Evans가 2003년 "Domain-Driven Design"에서 제시한 패턴으로, "한 시스템의 모델이 다른 시스템의 모델의 영향을 받아 오염되는 것을 방지하는 명시적인 레이어"다. 서로 다른 도메인 모델을 가진 두 시스템(예: 신 시스템과 레거시 시스템, 또는 두MSA 서비스)이 직접 통합되면, 일방이 상대방의 모델 구조를 자신의 도메인에 반영하게 되어耦合도가 증가한다. Anticorruption Layer는 이 두 시스템 사이에 변환기(Transformer)를 두어, 각 시스템이 자신의 모델을 유지하면서도相互通信할 수 있게 한다.

- **필요성**: 20년 된 레거시 시스템을 새로운 MSA로 전환할 때, 새 시스템이 레거시의 데이터 모델(CamelCase 대신 Snake_case, 복잡한 관계형 구조 등)을 그대로 반영하면, 새 시스템의 깨끗한 도메인 모델이 레거시의 제약을 받게 된다. Anticorruption Layer는 이러한"오염"을 방지하여, 신 시스템이 레거시 시스템의 기술 부채를 흡수하지 않도록 보호한다.

- **💡 비유**: Anticorruption Layer는 **국제 회의의 동시통역사**와 같습니다. 각 나라 대표(시스템)가 자기 나라의 언어로 발언하면, 통역사(ACL)가 다른 나라 언어로 변환하여 전달합니다. 이를 통해 각 대표'는 다른 나라의文法(모델 구조)에束縛되지 않고 자신의 언어로 말할 수 있습니다.

- **등장 배경 및 발전 과정**:
  1. **2003년 Evans의 DDD**: Evans가 레거시 시스템 Integration에서 도메인 모델 오염 문제를 해결하기 위한 패턴으로 Anticorruption Layer를 제시했다.

  Anticorruption Layer의 동작을 시각화하면 다음과 같다.

  ```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                  Anticorruption Layer 동작 구조                        │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  [현대 시스템]                                                     │
  │  ┌─────────────────────────────────────────────────────────────┐   │
  │  │  깨끗한 도메인 모델                                          │   │
  │  │                                                             │   │
  │  │  class Order {                                             │   │
  │  │      Customer customer;  // 깨끗한 Customer 도메인 객체       │   │
  │  │      List<OrderItem> items;                                │   │
  │  │      Money totalAmount;  // 값 객체                        │   │
  │  │  }                                                          │   │
  │  │                                                             │   │
  │  │  ※ 현대 시스템의 규칙과 언어로 설계됨                       │   │
  │  └──────────────────────────┬────────────────────────────────┘   │
  │                               │                                        │
  │                               │ 깨끗한 도메인 모델 (자신의 언어)        │
  │                               ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────┐   │
  │  │            Anticorruption Layer (ACL)                       │   │
  │  │                                                             │   │
  │  │  ┌─────────────────────────────────────────────────────┐   │   │
  │  │  │           모델 변환기 (Transformer)                   │   │   │
  │  │  │                                                     │   │   │
  │  │  │  Order ──▶ CustomerLegacyDto                        │   │   │
  │  │  │  (현대)    ──▶ (레거시 호환 포맷)                   │   │   │
  │  │  │                                                     │   │   │
  │  │  │  CustomerLegacyDto ──▶ Customer                    │   │   │
  │  │  │  (레거시 호환 포맷) ──▶ (현대 도메인)               │   │   │
  │  │  │                                                     │   │   │
  │  │  └─────────────────────────────────────────────────────┘   │   │
  │  └──────────────────────────┬────────────────────────────────┘   │
  │                               │                                        │
  │                               │ 레거시 호환 포맷                       │
  │                               ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────┐   │
  │  │                     [레거시 시스템]                          │   │
  │  │                                                             │   │
  │  │  • SNAKE_CASE 컬럼명                                        │   │
  │  │  • 3NF 정규화된Customer 테이블                               │   │
  │  │  • COBOL 레코드 구조                                        │   │
  │  │  • CamelCase 불가                                         │   │
  │  │                                                             │   │
  │  │  ※ 레거시 시스템의 규칙과 언어 (현대 시스템이 알 필요 없음)     │   │
  │  └─────────────────────────────────────────────────────────────┘   │
  │                                                                     │
  │  핵심 가치:                                                         │
  │  • 현대 시스템은 깨끗한 도메인 모델 유지 가능                        │
  │  • 레거시 시스템의 변경이 현대 시스템에 영향주지 않음               │
  │  • 레거시 모델이 현대 시스템에 "오염"되지 않음                      │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
  ```

  **[다이어그램 해설]** Anticorruption Layer의 핵심 가치는 두 시스템 간의 결합도를 낮추는 것이다. 현대 시스템의 Order 도메인 객체는 고객 정보를 Customer 도메인 객체로 참조한다. 이 Customer는 현대 시스템의 규칙에 맞게 설계된 깨끗한 도메인 객체다. 레거시 시스템과通信할 때, ACL의 Transformer가 Customer를 레거시 시스템이 이해하는 CustomerLegacyDto(CamelCase 대신 SNAKE_CASE, 현대 시스템의 타입 대신 레거시 호환 타입)로 변환한다. 레거시 시스템에서 데이터를 받을 때도 역으로 변환한다. 이를 통해 현대 시스템은 레거시 시스템의 데이터 구조(Snake_case, 레거시 타입 등)를 내부에 반영할 필요가 없으며, 오직 ACL만 레거시 모델을 알고 있으면 된다. 결과적으로 현대 시스템은 레거시 기술 부채의"오염"에서 보호된다.

  2. **2010년대 MSA 확산과 함께**: MSA에서 외부 파트너 API, 레거시 시스템 Integration에서 ACL이 표준 패턴으로 활용되었다.

- **📢 섹션 요약 비유**: Anticorruption Layer는 **의료기와 건강보조식품 사이의 검역소**와 같습니다. 건강보조식품(외부 시스템)이 직접 의료기(현대 시스템)에 들어가면 부적합한 성분이 혼입될 수 있지만, 검역소(ACL)가 성분을 점검하고 변환하여 안전하게連携합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Transformer** | 모델 간双向 변환 | DTO ↔ Domain 변환, 포맷 변환 | MapStruct, BeanUtils, ModelMapper | 통역사 |
| **Facade** | 내부 시스템의 단순화된 接口 | 복잡한 내부 구조를 숨기고 단순接口 제공 | 내부 facade 클래스 | 보험상담원 |
| **Adapter** | 외부 시스템과의 통신 관리 | HTTP Client, 리포지토리 구현체 | REST Client, gRPC Stub | 택배营业소 |
| **검疫소 (Quarantine)** | 입력 데이터 검증 및 정화 | 입력 데이터 검사, 샌itizer | 입력 검증 라이브러리 | 세관 |

---

### ACL 구현: 레거시 주문 시스템 Integration 예시

실무에서 ACL이 어떻게 구현되는지 구체적인 예시로 살펴본다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│              Anticorruption Layer 구현 예시                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [레거시 시스템 데이터 (COBOL 레코드 구조)]                           │
│                                                                     │
│  01 ORDER-RECORD.                                                   │
│      05 ORDER-ID          PIC 9(10).                                │
│      05 CUST-NUM         PIC 9(8).                                 │
│      05 ORDER-DATE       PIC 9(8).                                │
│      05 ORDER-AMT         PIC 9(10)V99.                           │
│      05 ORDER-STATUS     PIC X(1).                                │
│  ※ SNAKE_CASE, 수치 타입,Fixed-length, EBCDIC 인코딩              │
│                                                                     │
│  [현대 시스템 도메인 모델 (Clean Domain)]                            │
│                                                                     │
│  public class Order {                                              │
│      private OrderId id;           // Value Object                │
│      private CustomerId customerId; // Customer 참조 (ID만)       │
│      private LocalDate orderDate;  // Java 8 날짜 타입           │
│      private Money totalAmount;    // Money 값 객체               │
│      private OrderStatus status;   // Enum                       │
│  }                                                                 │
│                                                                     │
│  [DTO (Data Transfer Object)]                                       │
│                                                                     │
│  public class OrderDto {  // ACL 내부에서만 사용                   │
│      private String orderId;        // String 변환                │
│      private String customerNum;    // String 변환                │
│      private String orderDate;      // String 변환                │
│      private BigDecimal totalAmt;   // 숫자 변환                  │
│      private String statusCode;     // Enum 변환                 │
│  }                                                                 │
│                                                                     │
│  [Anticorruption Layer 구현]                                       │
│                                                                     │
│  public class OrderAclService {                                    │
│                                                                     │
│      // 레거시 → 현대 시스템 변환                                    │
│      public Order toDomain(OrderDto dto) {                        │
│          return Order.builder()                                    │
│              .id(new OrderId(dto.getOrderId()))                  │
│              .customerId(new CustomerId(dto.getCustomerNum()))    │
│              .orderDate(LocalDate.parse(dto.getOrderDate(),      │
│                  DateTimeFormatter.BASIC_ISO_DATE))              │
│              .totalAmount(new Money(dto.getTotalAmt(),            │
│                  Currency.getInstance("KRW")))                   │
│              .status(OrderStatus.fromCode(dto.getStatusCode()))  │
│              .build();                                             │
│      }                                                             │
│                                                                     │
│      // 현대 시스템 → 레거시 변환                                   │
│      public OrderDto toLegacy(Order order) {                     │
│          return OrderDto.builder()                                │
│              .orderId(order.getId().value())                    │
│              .customerNum(order.getCustomerId().value())         │
│              .orderDate(order.getOrderDate().format(             │
│                  DateTimeFormatter.BASIC_ISO_DATE))             │
│              .totalAmt(order.getTotalAmount().amount())         │
│              .statusCode(order.getStatus().getCode())           │
│              .build();                                             │
│      }                                                             │
│  }                                                                 │
│                                                                     │
│  [사용: MSA 서비스 내부]                                            │
│                                                                     │
│  @Service                                                          │
│  public class OrderService {                                       │
│                                                                     │
│      private final OrderRepository orderRepository;                │
│      private final OrderAclService orderAcl;                        │
│      private final LegacyOrderGateway legacyGateway;                │
│                                                                     │
│      // 레거시 시스템의 주문 조회                                    │
│      public Order getLegacyOrder(String orderId) {                │
│          OrderDto legacyDto = legacyGateway.findById(orderId);    │
│          return orderAcl.toDomain(legacyDto);  // 변환           │
│      }                                                             │
│  }                                                                 │
│                                                                     │
│  핵심 원칙:                                                         │
│  • ACL 변환 로직은 호출하는 서비스(도메인)에 배치되지 않음           │
│  • ACL은 도메인 객체를 모르onos (단순 데이터 변환만)                  │
│  • 도메인 객체는 ACL의 존재를 모르onos                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** ACL 구현의 핵심 원칙은 변환 로직의 위치다. OrderAclService는 OrderDto(레거시 호환 포맷)와 Order(현대 도메인 모델) 간의 변환만 담당한다. 이 변환 로직은 도메인 객체(Order) 내부에 존재하지 않고, ACL 서비스에 별도로 존재한다. OrderService는 레거시 시스템에서 데이터를 조회할 때 LegacyOrderGateway를 사용하고, 조회된 OrderDto를 OrderAclService.toDomain()을 호출하여 Order 도메인 객체로 변환한다. 이 구조에서 중요한 점은, OrderService(도메인 로직)가 레거시 시스템의 데이터 구조(SNAKE_CASE, EBCDIC 등)를 몰라도 된다는 것이다. OrderAclService가 변환을全的责任を持ち, OrderService는 깨끗한 도메인 모델만 다루게 된다. 이는 추후 레거시 시스템이 새 시스템으로 교체되어도, ACL만 수정하면 되고 도메인 로직은 변경할 필요가 없다.

- **📢 섹션 요약 비유**: ACL은 **편의점의 물류 시스템**과 같습니다. 제조업체에서送来하는 상품은 각 제조사마다 다른 포장 단위와 바코드 형식을使用합니다. 편의점 물류팀(ACL)이 이러한 다양성을 편의점 내부 규격(도메인 모델)로 통일하여, 편의점 내부에서는統一된 방식으로 商品를管理합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: ACL vs Shared Kernel vs Direct Integration

| 구분 | Anticorruption Layer | Shared Kernel | Direct Integration |
|:---|:---|:---|:---|
| **耦合도** |最低 (완전 분리) | 중간 (공유 모델) | 높음 (相互의존) |
| **변환 비용** | 높음 (변환 로직 필요) | 낮음 (공유 모델) |最低 (변환 없음) |
| **레거시 오염** | 없음 (완전 격리) | 위험 (레거시 모델 공유) | 최대 (레거시 모델 직접 사용) |
| **변경 영향** |一方 변경이 타方に影響なし | 양쪽 모두 동의 필요 | 즉시 파급 |

- **📢 섹션 요약 비유**: Direct Integration은 **다른 나라 사람과 Dictionaries 없이 대화하는 것**과 같습니다. Shared Kernel은 **두 나라가共通 어휘집을 shared하는 것**과 같습니다. ACL은 **각자 전문通訳사를 두는 것**과 같습니다. 가장 확실하지만 비용이 많이 듭니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 레거시 SAP와 신 시스템 Integration**: 20년 된 SAP ERP 시스템의 데이터를 신 개발하는 주문 관리 MSA에서 사용해야 하는 상황. 각 시스템의 도메인 모델이 크게 다르므로, SAP의 IDoc/BAPI 데이터를 신 시스템의 도메인 모델로 변환하는 ACL을 구현하여, 신 시스템의 깨끗한 도메인 모델을 유지하면서 레거시 SAP와 Integration한다.

### 도입 체크리스트
- **기술적**: 변환 로직의 일관성을 보장하는가? 양� Direction 변환이 정의되어 있는가?
- **운영·보안적**: 레거시 시스템의 변경 시 ACL만 수정하면 되는가?

### 안티패턴
- **Fat ACL**: ACL에 너무 많은 로직이 포함되어 사실상 새로운 도메인 레이어가 되어버리는 안티패턴. ACL은、あくまで変換器であり、ビジネスロジックを含むべきではない。

- **📢 섹션 요약 비유**: Fat ACL은 **통역사에게iyao 조율까지 시키는 것**과 같습니다. 통역사는本来 통역(변환)만 하면 되는데,일까지 하면 통역사 본래의 역할이 희석되고 중앙 통제塔이 없는 격成为합니다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망
- **AI 기반 모델 변환**: AI/ML을活用하여 레거시 데이터 모델과 현대 도메인 모델 간의 매핑을 자동추론하고, ACL의変換 로직을 자동生成하는 도구가 연구되고 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Bounded Context** | ACL은 서로 다른 바운디드 컨텍스트 간의 Integration에서 모델 오염을防止する。 |
| **Adapter 패턴** | ACL의基幹はAdapterパターンであり、インターフェース変換を担当する。 |
| **변환기 (Transformer)** | ACL 내부에서 DTO ↔ 도메인 객체 간 변환을 담당하는组件다. |
| ** 레거시 현대화** | ACL는 레거시 시스템을 신 시스템과 Integration하면서도 깨끗한 도메인 모델을 유지하는 핵심 패턴이다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. Anticorruption Layer는 **다른 나라 옷을 입은 People에게jia를 입히기 전 검사하는 검疫소**와 같습니다. 외국 옷(레거시 모델)에 문제가 있으면(不合品)国内에 들어오지 않게 하고, 필요시juipment를 收拾해서国内에 맞춥니다.
2. 컴퓨터에서도 오래된 시스템(레거시)과 새로운 시스템이 데이터를 주고받을 때, ACL이 그 사이에서 translation을担当하여 서로의 모델에 영향받지 않게 합니다.
3. 다만 translation官(ACL)을 너무 두껍게 만들면( Fat ACL) 번역不只是 하고 내용까지dictate하여 本来의 역할이 흐트러집니다!
