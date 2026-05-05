+++
weight = 182
title = "182. 지연 로딩 (Lazy Loading)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 지연 로딩 (Lazy Loading)은 연관 객체를 즉시 조회하지 않고 가상 프록시(Virtual Proxy)를 배치해두다가 실제 접근 시점에 DB 쿼리를 실행하는 최적화 패턴이다.
> 2. **가치**: 사용하지 않을 연관 데이터를 쿼리하지 않아 초기 로딩 성능을 극적으로 향상시키지만, N+1 문제라는 위험을 동반한다.
> 3. **판단 포인트**: "@ManyToOne은 EAGER, @OneToMany는 LAZY"가 JPA 기본값이다. N+1 문제가 발생하면 Fetch Join 또는 @BatchSize로 해결하며, 이 트레이드오프를 이해하는 것이 실무 핵심이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 즉시 로딩의 문제점

Order 엔티티를 조회할 때 연관된 모든 데이터(Member, OrderItems, Product)를 즉시 로딩(Eager Loading)하면 어떻게 될까?

```sql
-- Order 조회 시 즉시 로딩으로 실행되는 쿼리
SELECT o.*, m.*, oi.*, p.*
FROM orders o
JOIN members m ON o.member_id = m.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
WHERE o.id = ?

-- 주문 목록 조회 시: N개 주문 × M개 상품 = 대규모 카테시안 곱 발생
```

주문 목록에서 주문 번호와 날짜만 보여줄 때도 Member, OrderItem, Product 전체를 조회하는 것은 낭비다.

### 지연 로딩의 아이디어

```
즉시 로딩 (Eager Loading):
  Order 조회 → [Order + Member + OrderItems + Products 전부 조회]
  모든 연관 데이터를 한 번에 가져옴 (필요 없어도)

지연 로딩 (Lazy Loading):
  Order 조회 → [Order만 조회]
                     │
                     └── member 접근 시 → [Member 조회]
                     └── items 접근 시  → [OrderItems 조회]
                     └── 접근 안 하면 → 쿼리 없음
```

📢 **섹션 요약 비유**: 백과사전을 읽을 때 모든 항목을 한 번에 외우려 하지 않는다. 필요한 항목이 생겼을 때 그 페이지를 펴는 것이 지연 로딩이다.

---

## 2. 구성요소

### 가상 프록시 (Virtual Proxy) 패턴

JPA는 지연 로딩을 위해 실제 객체 대신 **프록시(Proxy) 객체**를 반환한다.

```
em.find(Order.class, 1L) 실행 시:

[Lazy Loading 설정]
┌────────────────────────────────────────────────────────┐
│  Order 프록시 객체                                       │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │  order.id = 1        │  │  member = ??         │    │
│  │  order.date = today  │  │  (프록시: 미초기화)    │    │
│  │  order.status = PAID │  │  → 접근 시 DB 조회    │    │
│  └──────────────────────┘  └──────────────────────┘    │
└────────────────────────────────────────────────────────┘

order.getMember() 호출 시:
    ↓ 프록시 초기화 트리거
    ↓ SELECT * FROM members WHERE id = ? 실행
    ↓ 실제 Member 객체 반환
```

### 프록시 클래스 구조

```
<<interface>>              <<concrete>>         <<proxy>>
Order ◄─────────────── OrderProxy extends Order
                          │
                          │ target 필드: 실제 Order 객체 (초기엔 null)
                          │
                          │ getMember() {
                          │   if (target == null) {
                          │     target = em.load(Order.class, id);
                          │   }
                          │   return target.getMember();
                          │ }
```

### JPA 로딩 전략

| 어노테이션 | 기본 전략 | 권장 전략 | 이유 |
|:---|:---|:---|:---|
| `@ManyToOne` | EAGER | LAZY | 조회 시 불필요한 JOIN 방지 |
| `@OneToOne` | EAGER | LAZY | 같은 이유 |
| `@OneToMany` | LAZY | LAZY (기본값 유지) | 컬렉션 전체 로딩 방지 |
| `@ManyToMany` | LAZY | LAZY | 대량 데이터 방지 |

📢 **섹션 요약 비유**: 프록시는 음식 배달 앱의 "예약 버튼"이다. 버튼(프록시)은 즉시 나타나지만, 실제 음식(데이터)은 주문(접근)했을 때 배달(쿼리)된다.

---

## 3. 구조 및 동작 원리

### Eager Loading vs Lazy Loading 비교

| 비교 항목 | 즉시 로딩 (Eager Loading) | 지연 로딩 (Lazy Loading) |
|:---|:---|:---|
| **로딩 시점** | 부모 엔티티 조회 시 즉시 | 연관 객체 실제 접근 시 |
| **초기 조회 쿼리 수** | 1개 (복잡한 JOIN 포함) | 1개 (단순, JOIN 없음) |
| **총 쿼리 수** | 적음 (JOIN으로 한 번에) | 많을 수 있음 (N+1 위험) |
| **메모리 사용** | 많음 (불필요한 데이터 포함) | 적음 (필요한 것만 로드) |
| **주의 위험** | 카테시안 곱, 과다 로딩 | N+1 문제 |
| **적합 상황** | 항상 같이 사용하는 연관 객체 | 선택적으로 사용하는 연관 객체 |

### N+1 문제 및 해결 방법

```
[N+1 문제 발생 예시]
List<Order> orders = orderRepository.findAll(); // SELECT * FROM orders (1번)
for (Order order : orders) {
    order.getMember().getName(); // 각 Order마다 SELECT * FROM members (N번)
}
// 총 쿼리: 1 + N번 → 1,000개 주문 시 1,001번!

[해결 1: Fetch Join]
SELECT o FROM Order o JOIN FETCH o.member
// 1번 쿼리로 해결 (INNER JOIN)

[해결 2: @BatchSize (배치 IN 쿼리)]
@BatchSize(size = 100)
@ManyToOne(fetch = FetchType.LAZY)
private Member member;
// SELECT * FROM members WHERE id IN (?, ?, ..., ?) (N/100 번)

[해결 3: EntityGraph]
@EntityGraph(attributePaths = {"member"})
List<Order> findAll();
```

| N+1 해결 방법 | 특징 | 적합 상황 |
|:---|:---|:---|
| **Fetch Join** | 단일 쿼리로 해결, 카테시안 곱 주의 | 단순 연관 관계 |
| **@BatchSize** | IN 절로 배치 로딩 | 컬렉션 연관 |
| **@EntityGraph** | 어노테이션으로 선언적 설정 | 특정 조회 메서드 |
| **QueryDSL fetchJoin()** | 타입 안전 동적 Fetch Join | 복잡한 동적 쿼리 |

📢 **섹션 요약 비유**: N+1 문제는 편의점에서 학생 100명 도시락 주문을 받았는데, 각 학생에게 일일이 전화해서 반찬을 확인하는 것이다. Fetch Join은 한 번에 묶어서 "100개 도시락, 반찬 포함"으로 주문하는 것이다.

---

## 4. 비교 및 트레이드오프

### 지연 로딩 설정 및 주의점

```java
@Entity
public class Order {
    @Id
    private Long id;

    // 권장: LAZY로 변경
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "member_id")
    private Member member;

    // 기본값 LAZY, 유지
    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    private List<OrderItem> items = new ArrayList<>();
}

// Fetch Join 사용 예
@Query("SELECT o FROM Order o JOIN FETCH o.member WHERE o.status = :status")
List<Order> findByStatusWithMember(@Param("status") OrderStatus status);
```

### LazyInitializationException 방지

```java
// 트랜잭션 밖에서 지연 로딩 접근 시 LazyInitializationException 발생!
@Service
public class OrderService {
    @Transactional(readOnly = true)  // 트랜잭션 내에서 접근
    public OrderDto getOrder(Long id) {
        Order order = orderRepository.findById(id).orElseThrow();
        // 여기서 order.getMember() 접근 가능
        return OrderDto.from(order);
    }
}
// 트랜잭션 종료 후 Controller에서 getMember() 접근 → 예외!
```

### 기술사 판단 포인트

| 상황 | 전략 | 이유 |
|:---|:---|:---|
| 상세 페이지 (모든 연관 필요) | Fetch Join | 단일 쿼리로 완전 로딩 |
| 목록 페이지 (일부만 필요) | Lazy + 필요 시 Fetch | 불필요한 데이터 미조회 |
| 배치 처리 대용량 | Lazy + @BatchSize | 메모리 최적화 |
| 실시간 API 응답 속도 중요 | 상황별 Fetch Join | N+1 방지 필수 |

📢 **섹션 요약 비유**: 레스토랑 메뉴(Lazy)는 손님이 주문할 때 요리한다. 주문하지 않은 모든 요리를 미리 만들어놓는(Eager) 것은 낭비다. 단, 세트 메뉴(Fetch Join)는 한 번에 만들어 효율적이다.

---

## 5. 실무 적용 및 최적화 기법

### 지연 로딩 도입 기대효과

| 기대효과 | 구체적 내용 |
|:---|:---|
| **초기 로딩 성능 향상** | 불필요한 연관 데이터 미조회 |
| **메모리 최적화** | 실제 사용하는 데이터만 메모리에 적재 |
| **유연한 로딩 전략** | 화면/기능에 따라 선택적 Fetch 가능 |
| **과도한 JOIN 방지** | 복잡한 카테시안 곱 쿼리 생성 억제 |

지연 로딩은 ORM 사용 시 선택이 아닌 **필수 이해 영역**이다. N+1 문제를 모르고 지연 로딩을 사용하면 오히려 즉시 로딩보다 더 많은 쿼리가 발생한다. **"Lazy로 설정하되, 필요한 연관 관계는 반드시 Fetch Join으로 명시"** 하는 것이 JPA 실무 최적 전략이다.

📢 **섹션 요약 비유**: 넷플릭스는 당신이 실제로 재생 버튼을 누른 영상만 스트리밍한다. 가입한다고 모든 영상을 다운로드하지 않는 것이 지연 로딩이다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 프록시 패턴 (Proxy Pattern) | 가상 프록시가 지연 로딩의 기반 |
| 상위 개념 | Unit of Work 패턴 | 영속성 컨텍스트 내에서 지연 로딩 관리 |
| 하위 개념 | 가상 프록시 (Virtual Proxy) | 실제 객체 대신 배치되는 대리 객체 |
| 하위 개념 | Fetch Join | N+1 문제 해결을 위한 명시적 조인 |
| 연관 개념 | N+1 문제 | 지연 로딩의 대표적 성능 안티패턴 |
| 연관 개념 | @BatchSize | N+1 완화를 위한 IN 절 배치 로딩 |
| 연관 개념 | LazyInitializationException | 트랜잭션 외부에서 지연 로딩 접근 시 예외 |

### 👶 어린이를 위한 3줄 비유 설명

- 도서관에서 책을 빌릴 때, 책 목록(Order)만 먼저 보고, 실제로 읽고 싶은 책(Member, Item)만 대출한다 — 그것이 지연 로딩이다.
- 모든 책을 한꺼번에 집으로 가져갔다가 안 읽으면(즉시 로딩) 엄청난 낭비다.
- 하지만 책 100권을 한 번에 1권씩 100번 왕복해서 빌리면(N+1) 더 힘드니까, 필요한 책 목록을 미리 알면 한 번에 여러 권 빌려야(Fetch Join) 한다.
