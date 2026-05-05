+++
weight = 147
title = "147. DDD (Domain-Driven Design) - 도메인 주도 설계"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: DDD(Domain-Driven Design, 도메인 주도 설계)는 에릭 에반스(Eric Evans)가 2003년 제안한 소프트웨어 설계 방법론으로, **비즈니스 도메인(Domain)의 핵심 개념과 규칙을 코드 모델에 직접 반영**함으로써 복잡한 비즈니스 로직을 다루는 소프트웨어의 복잡도를 관리하는 접근법이다.
> **비유**: 복잡한 시스템을 작은 운영 규칙으로 정리해 안정적으로 굴러가게 만드는 교통 관제 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
DDD 전술적 패턴 (Tactical Patterns)

  ┌─────────────────────────────────────────────────────────────┐
  │                      Aggregate Root                         │
  │  ┌──────────────┐   ┌──────────────┐   ┌───────────────┐   │
  │  │    Entity    │   │  Value Object │   │    Domain     │   │
  │  │ (식별자 있음) │   │ (식별자 없음) │   │    Event      │   │
  │  │  Order       │   │  Money       │   │ OrderPlaced   │   │
  │  │  Customer    │   │  Address     │   │ PaymentDone   │   │
  │  └──────────────┘   └──────────────┘   └───────────────┘   │
  └─────────────────────────────────────────────────────────────┘
           │                                        │
  ┌────────▼────────┐                    ┌──────────▼─────────┐
  │   Repository    │                    │   Domain Service   │
  │ (영속성 추상화)  │                    │ (여러 객체 협력 로직) │
  └─────────────────┘                    └───────────────────-┘
```

| 빌딩 블록 | 설명 | 예시 |
|:---|:---|:---|
| **Entity** | 고유 식별자(ID)로 구별되는 객체 | `Order(id=1)`, `Customer(id=42)` |
| **Value Object** | 값으로 동일성을 정의하는 불변 객체 | `Money(100, "KRW")`, `Address` |
| **Aggregate** | 하나의 일관성 경계를 형성하는 Entity+VO 집합 | Order = 주문 + 주문 항목들 |
| **Aggregate Root** | Aggregate의 진입점; 외부는 Root만 접근 | `Order` (OrderItem은 직접 접근 불가) |
| **Repository** | Aggregate 영속성(저장·조회) 추상화 | `OrderRepository.findById()` |
| **Domain Event** | 도메인에서 일어난 사실 표현 | `OrderPlaced`, `PaymentReceived` |
| **Domain Service** | 단일 Entity에 속하지 않는 비즈니스 로직 | `TransferService.transfer(from, to)` |

---

## 2. 구성요소

```text
컨텍스트 맵 (Context Map) 예시

  ┌─────────────────┐          ┌─────────────────┐
  │  주문 컨텍스트   │          │  배송 컨텍스트   │
  │  (Order BC)     │ ──ACL──► │  (Delivery BC)  │
  │                 │          │                 │
  │  Customer       │          │  Shipment       │
  │  Order          │          │  TrackingNumber  │
  └─────────────────┘          └─────────────────┘
          │                            │
    Anti-Corruption Layer             │
    (언어 변환: Customer→Recipient)    │
          │                            │
  ┌───────▼────────────────────────────▼──┐
  │  결제 컨텍스트 (Payment BC)            │
  │  Payment, Invoice, Refund            │
  └───────────────────────────────────────┘
```

---

## 3. 구조 및 원리

**핵심 조건**: 분산 서비스 환경에서는 서비스 경계, 상태 관리, 호출 정책, 장애 격리, 데이터 일관성 전략이 명확해야 전체 시스템이 안정적으로 동작한다.

동작 순서:
1. 요청이 API 게이트웨이·이벤트 소스·메시지 브로커를 통해 유입된다.
2. 서비스 디스커버리와 라우팅 계층이 적절한 실행 주체를 결정한다.
3. 각 서비스나 함수가 독립적으로 로직을 수행하고 필요한 데이터를 조회·갱신한다.
4. 비동기 이벤트, 보상 트랜잭션, 캐시 전략으로 분산 일관성 문제를 완화한다.
5. 관측성·재시도·회로 차단·배포 전략으로 장애 전파를 제어한다.

### DDD와 MSA의 연관

DDD의 Bounded Context가 MSA의 서비스 경계와 자연스럽게 매핑된다.

| DDD 개념 | MSA 대응 |
|:---|:---|
| Bounded Context | 마이크로서비스 경계 |
| Aggregate Root | 서비스의 핵심 도메인 객체 |
| Domain Event | 서비스 간 이벤트 메시지 (Kafka 등) |
| Repository | 서비스별 독립 DB |
| Context Map | 서비스 간 통신 계약 (API, 메시지) |

### 전술적 vs. 전략적 DDD

| 구분 | 범위 | 주요 패턴 |
|:---|:---|:---|
| **전술적 DDD** | 단일 BC 내부 구현 | Entity, VO, Aggregate, Repository, Domain Service |
| **전략적 DDD** | 전체 시스템 설계 | Bounded Context, Context Map, Ubiquitous Language |

---

## 4. 비교 및 연결

### DDD 적용 판단 기준

**DDD 적합 상황**:
- 복잡한 비즈니스 규칙 (금융·의료·보험·물류)
- 도메인 전문가와 긴밀한 협업이 가능한 환경
- 장기 유지보수·확장이 예상되는 핵심 시스템

**DDD 불필요 상황**:
- 단순 CRUD (게시판, 쇼핑 카탈로그 조회)
- 빠른 프로토타이핑 필요 (MVP)
- 도메인 전문가 협업이 어려운 환경

### 안티패턴

**빈약한 도메인 모델(Anemic Domain Model)**: Entity가 getter/setter만 가진 데이터 백(Data Bag)으로 전락하고, 모든 비즈니스 로직이 Service 레이어에 몰린 상태. DDD 용어를 쓰지만 실질적으로는 트랜잭션 스크립트 패턴이다.

**Aggregate 경계 과도한 확장**: 하나의 Aggregate에 너무 많은 Entity를 묶으면 동시성 충돌(낙관적 잠금 실패)과 DB 부하가 발생한다. Aggregate는 강한 일관성이 필요한 최소 단위로만 묶어야 한다.

---

## 5. 실무 적용 및 판단

DDD를 적용하면 코드가 비즈니스 언어와 일치하게 되어, 도메인 전문가와 개발자가 **동일한 모델을 보며 소통**할 수 있다. Bounded Context로 복잡도가 격리되며, 각 컨텍스트는 독립적으로 발전·배포할 수 있어 MSA와 자연스럽게 결합한다.

**한계**: DDD는 학습 곡선이 가파르고, 도입 초기 오버헤드가 크다. 잘못 적용하면 오히려 복잡도를 높인다. 단순한 시스템에는 Active Record 패턴이나 Transaction Script가 더 실용적이다.

DDD는 "코드를 비즈니스처럼 만드는 것"이 아니라, **"비즈니스와 코드가 같은 언어를 쓰게 만드는 것"** 이라는 관점으로 이해해야 한다.

---

## 6. 기대효과 및 결론

DDD (Domain-Driven Design) - 도메인 주도 설계를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 DDD (Domain-Driven Design) - 도메인 주도 설계의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
모놀리식 아키텍처 → 복잡도 증가 → 유지보수 어려움
    │
    ▼
DDD (Domain-Driven Design, 2003 Eric Evans)
    │
    ├─► 전략적 패턴: Bounded Context / Context Map
    ├─► 전술적 패턴: Entity / VO / Aggregate / Repository
    │
    ▼
유비쿼터스 언어 — 코드와 도메인 언어 일치
    │
    ▼
MSA 서비스 분리 기준으로 Bounded Context 활용
    │
    ▼
CQRS + 이벤트 소싱 — 도메인 이벤트 기반 아키텍처
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **유비쿼터스 언어 (Ubiquitous Language)** | DDD의 핵심; 개발자+도메인 전문가 공통 용어 |
| **바운디드 컨텍스트 (Bounded Context)** | MSA 서비스 분리 기준; 언어·모델의 적용 경계 |
| **이벤트 소싱 (Event Sourcing)** | 도메인 이벤트를 상태 변경의 기록으로 사용 |
| **CQRS (Command Query Responsibility Segregation)** | 명령(쓰기)와 조회(읽기) 모델 분리; DDD와 자주 결합 |
| **MSA (Microservices Architecture)** | Bounded Context → 서비스 경계의 자연스러운 매핑 |

---
