+++
weight = 180
title = "180. 트랜잭션 스크립트 vs 도메인 모델 (Transaction Script vs Domain Model)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 트랜잭션 스크립트 (Transaction Script)는 단순 절차형으로 한 함수가 한 트랜잭션을 처리하고, 도메인 모델 (Domain Model)은 비즈니스 규칙과 데이터를 객체에 캡슐화한다.
> 2. **가치**: 단순 CRUD 업무엔 트랜잭션 스크립트가 빠르지만, 복잡한 비즈니스 규칙이 증가할수록 도메인 모델이 유지보수성과 확장성에서 압도적으로 유리하다.
> 3. **판단 포인트**: "비즈니스 규칙이 10개를 넘고 서로 의존한다면 도메인 모델로 전환하라" — 복잡도 임계점이 선택 기준이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 두 패턴의 등장 배경

마틴 파울러 (Martin Fowler)의 『Patterns of Enterprise Application Architecture (PoEAA)』 에서 비즈니스 로직 조직화 패턴으로 두 가지를 제시했다.

**트랜잭션 스크립트 (Transaction Script)**  
가장 자연스러운 첫 번째 접근 방법이다. 각 비즈니스 트랜잭션(사용자 요청)을 하나의 함수/메서드로 직접 구현한다.

```java
// 트랜잭션 스크립트 방식
public class OrderService {
    public void placeOrder(Long userId, List<Long> productIds, int discount) {
        // 1. 사용자 조회
        User user = userDao.findById(userId);
        // 2. 재고 확인
        for (Long pid : productIds) { /* 재고 검사 SQL */ }
        // 3. 할인 계산 로직 (인라인으로 전부 여기에)
        double total = 0;
        for (Long pid : productIds) {
            Product p = productDao.findById(pid);
            total += p.getPrice() * (1 - discount / 100.0);
        }
        // 4. 주문 저장
        orderDao.save(new OrderDto(userId, total));
        // 5. 재고 차감
        for (Long pid : productIds) { /* UPDATE SQL */ }
        // 6. 알림 발송
        emailService.send(user.getEmail(), "주문 완료");
    }
}
```

이 방식은 단순하지만 로직이 커지면 **갓 메서드 (God Method)**, **갓 클래스 (God Class)** 문제가 발생한다.

📢 **섹션 요약 비유**: 트랜잭션 스크립트는 요리법 노트다. 처음엔 간단하지만 레시피가 100개가 되면 책 전체가 뒤엉킨다. 도메인 모델은 요리법을 재료별, 조리법별로 체계적으로 분류한 요리책이다.

---

## 2. 구성요소

### 두 패턴의 구조 비교

```
[트랜잭션 스크립트 구조]
┌───────────────────────────────────────┐
│          OrderService                 │
│                                       │
│  placeOrder() ──┐                     │
│                 ├── 유효성 검사         │
│  cancelOrder()  ├── 재고 확인          │
│                 ├── 할인 계산          │
│  refundOrder()  ├── 주문 저장          │
│                 └── 알림 발송          │
│  (모든 로직이 Service에 집중됨)         │
└───────────────────────────────────────┘
        │ DTO/원시값으로만 통신
        ▼
    Database (테이블 중심)

[도메인 모델 구조]
┌──────────────────────────────────────────┐
│             Application Layer            │
│         OrderApplicationService          │
│  (조율만 담당, 비즈니스 규칙 없음)            │
└──────────────────┬───────────────────────┘
                   │ 도메인 객체 조작
┌──────────────────▼───────────────────────┐
│              Domain Layer                │
│                                          │
│  ┌─────────────────────────────────┐     │
│  │  Order (Aggregate Root)         │     │
│  │  + place(items, discountPolicy) │     │
│  │  + cancel()                     │     │
│  │  + refund()                     │     │
│  │  - validateItems()              │     │
│  └──────────┬──────────────────────┘     │
│             │ 포함                        │
│  ┌──────────▼──────────┐                 │
│  │  OrderItem          │  DiscountPolicy │
│  │  + calculatePrice() │  (인터페이스)    │
│  └─────────────────────┘                 │
└──────────────────────────────────────────┘
```

### 빈혈 도메인 모델 (Anemic Domain Model) 안티패턴

도메인 모델을 사용한다고 선언했지만, 실제로는 DTO처럼 데이터만 있고 로직은 Service에 있는 경우를 **빈혈 도메인 모델 (Anemic Domain Model)** 이라 한다. 마틴 파울러는 이를 안티패턴으로 지목했다.

| 항목 | 진정한 도메인 모델 | 빈혈 도메인 모델 (안티패턴) |
|:---|:---|:---|
| 데이터 | Order 객체 내 | Order 객체 내 |
| 비즈니스 로직 | Order 객체 내 (`order.cancel()`) | Service 내 (`orderService.cancel(order)`) |
| 캡슐화 | 완전한 캡슐화 | 깨진 캡슐화 |
| 객체지향 | OOP 원칙 준수 | 절차적 코드에 객체 껍데기만 씌움 |

📢 **섹션 요약 비유**: 빈혈 도메인 모델은 몸(데이터)은 있는데 뇌(로직)가 없는 좀비다. 진짜 도메인 모델은 스스로 생각하고 행동하는 살아있는 객체다.

---

## 3. 구조 및 동작 원리

### 트랜잭션 스크립트 vs 도메인 모델 상세 비교

| 비교 항목 | 트랜잭션 스크립트 | 도메인 모델 |
|:---|:---|:---|
| **구현 방식** | 절차적 함수/메서드 | 객체 지향 도메인 클래스 |
| **비즈니스 규칙 위치** | Service 레이어에 집중 | 도메인 객체에 캡슐화 |
| **초기 개발 속도** | 빠름 | 느림 (설계 시간 필요) |
| **복잡도 증가 시** | 급격한 코드 복잡도 증가 | 완만한 복잡도 증가 |
| **테스트** | Service 단위 테스트 (DB 의존) | 도메인 객체 단독 테스트 (DB 불필요) |
| **코드 재사용** | 낮음 (Service 메서드 중복) | 높음 (도메인 메서드 재사용) |
| **적합 시스템** | 단순 CRUD, 소규모 | 복잡한 비즈니스 규칙, 대규모 |
| **대표 예시** | 전통 PHP/ASP.NET WebForm | Spring + DDD, JPA Entity |

### 복잡도별 패턴 선택 기준

```
비즈니스
 복잡도
   ▲
   │                              도메인 모델
 높음│                          ╱
   │                        ╱
   │               임계점  ╱
   │            ─────────╳─────────
   │          ╱           ╲
 낮음│  트랜잭션              ╲ (도메인 모델 오버엔지니어링)
   │  스크립트
   └─────────────────────────────► 시스템 규모
      소규모         중규모        대규모
```

📢 **섹션 요약 비유**: 동네 분식집(단순 CRUD)에는 전자 주문 시스템(트랜잭션 스크립트)으로 충분하다. 그러나 대형 백화점(복잡한 비즈니스)에는 ERP(도메인 모델)가 필요하다.

---

## 4. 비교 및 트레이드오프

### 도메인 모델 구현 예시 (Java)

```java
// 도메인 객체: 비즈니스 규칙을 객체 안에 캡슐화
public class Order {
    private OrderId id;
    private List<OrderItem> items;
    private OrderStatus status;
    private Money totalAmount;

    // 팩토리 메서드: 주문 생성 규칙 캡슐화
    public static Order create(Customer customer, List<Product> products,
                               DiscountPolicy discountPolicy) {
        if (products.isEmpty()) throw new IllegalArgumentException("주문 항목 없음");
        if (!customer.isActive()) throw new IllegalStateException("비활성 고객");

        List<OrderItem> items = products.stream()
            .map(p -> new OrderItem(p, discountPolicy.apply(p)))
            .collect(Collectors.toList());

        Money total = items.stream()
            .map(OrderItem::getPrice)
            .reduce(Money.ZERO, Money::add);

        return new Order(OrderId.generate(), items, OrderStatus.PENDING, total);
    }

    // 도메인 행위: 취소 규칙 캡슐화
    public void cancel() {
        if (status == OrderStatus.SHIPPED)
            throw new IllegalStateException("배송 중인 주문은 취소 불가");
        this.status = OrderStatus.CANCELLED;
    }
}
```

### 기술사 시험 판단 포인트

| 상황 | 권장 패턴 | 근거 |
|:---|:---|:---|
| 단순 게시판, 설정 관리 | 트랜잭션 스크립트 | 비즈니스 규칙 단순, 과도한 추상화 불필요 |
| 전자상거래 주문 시스템 | 도메인 모델 | 할인, 배송, 반품 등 복잡한 규칙 |
| 금융 결제 시스템 | 도메인 모델 | 규칙 변경 잦음, 테스트 필수 |
| 레거시 CRUD API | 트랜잭션 스크립트 | 기존 코드와의 호환성, 점진적 전환 |

📢 **섹션 요약 비유**: 트랜잭션 스크립트는 "해야 할 일 목록"(To-do list), 도메인 모델은 "자율 관리 AI 비서"다. 할 일이 3개면 목록으로 충분하지만, 1,000개가 되면 AI 비서가 필요하다.

---

## 5. 실무 적용 및 최적화 기법

### 도메인 모델 도입 기대효과

| 기대효과 | 구체적 내용 |
|:---|:---|
| **비즈니스 규칙 응집** | 규칙이 도메인 객체에 집중 → 변경 영향 범위 최소화 |
| **테스트 용이성** | DB 없이 도메인 로직 단독 테스트 가능 |
| **코드 가독성** | `order.cancel()` vs `orderService.updateStatusToCancelled(orderId)` |
| **갓 클래스 방지** | Service가 조율 역할만 담당, 비대화 방지 |
| **DDD 적용 기반** | 애그리게이트, 바운디드 컨텍스트 설계의 기반 |

두 패턴은 우열이 없다. **"올바른 패턴을 올바른 복잡도에 적용하는 것"** 이 핵심이다. 단순한 곳에 도메인 모델을 강요하는 것도, 복잡한 곳에 트랜잭션 스크립트를 고집하는 것도 모두 기술 부채를 만든다. 기술사로서 판단 기준은 **비즈니스 규칙의 복잡도와 변경 빈도**다.

📢 **섹션 요약 비유**: 자전거(트랜잭션 스크립트)와 자동차(도메인 모델)는 모두 훌륭한 이동 수단이다. 골목길엔 자전거가, 고속도로엔 자동차가 더 적합하다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | PoEAA (Patterns of Enterprise Application Architecture) | 마틴 파울러의 엔터프라이즈 패턴 카탈로그 |
| 상위 개념 | DDD (Domain-Driven Design) | 도메인 모델 패턴의 발전된 형태 |
| 하위 개념 | Aggregate Root | 도메인 모델의 핵심 구성 요소 |
| 하위 개념 | Value Object | 도메인 모델의 불변 값 객체 |
| 연관 개념 | 빈혈 도메인 모델 안티패턴 | 도메인 모델처럼 보이지만 실제론 TS |
| 연관 개념 | Service Layer 패턴 | 트랜잭션 스크립트의 조직화된 형태 |
| 연관 개념 | Table Module 패턴 | 테이블 단위 로직 조직화 |

### 👶 어린이를 위한 3줄 비유 설명

- 트랜잭션 스크립트는 요리사가 모든 재료 준비부터 요리까지 혼자 다 하는 방식이다 — 처음엔 빠르지만 메뉴가 100개가 되면 지친다.
- 도메인 모델은 재료(도메인 객체)가 스스로 자신의 요리법을 알고 있는 방식이다 — "나는 스테이크야, 굽는 건 내가 알아서 해."
- 단순한 볶음밥(CRUD)엔 레시피 메모가 충분하고, 복잡한 프렌치 코스(복잡한 비즈니스)엔 전문 셰프(도메인 모델)가 필요하다.
