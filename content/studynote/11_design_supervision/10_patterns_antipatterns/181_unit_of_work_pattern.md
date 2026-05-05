+++
weight = 181
title = "181. 유닛 오브 워크 패턴 (Unit of Work Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 유닛 오브 워크 (Unit of Work) 패턴은 하나의 비즈니스 트랜잭션 내에서 발생한 객체의 변경(삽입, 수정, 삭제)을 추적하여 트랜잭션 커밋 시 한 번에 DB에 반영하는 패턴이다.
> 2. **가치**: 불필요한 중간 쿼리 제거, 데이터 일관성 보장, DB 왕복 횟수 최소화를 동시에 달성한다. JPA/Hibernate의 영속성 컨텍스트(Persistence Context)가 이 패턴의 완성도 높은 구현체다.
> 3. **판단 포인트**: 1차 캐시(반복 쿼리 제거) + 변경 감지(Dirty Checking) + 지연 쓰기(Write-Behind)의 세 메커니즘이 UoW의 핵심이며, 이를 이해해야 JPA의 동작을 정확히 예측할 수 있다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 문제 상황: 개별 쿼리의 비효율

트랜잭션 없이 객체 변경 시마다 즉시 DB에 반영하면 다음 문제가 발생한다.

```java
// 문제 있는 방식: 변경마다 즉시 DB 쿼리
user.setEmail("new@email.com"); // UPDATE users SET email = ?
user.setName("홍길동");          // UPDATE users SET name = ?
user.setPhone("010-1234-5678"); // UPDATE users SET phone = ?
// 동일 행에 대해 UPDATE 3번 실행 → 비효율
```

또한 중간에 예외가 발생하면 부분적으로만 반영된 **불일치 상태**가 될 수 있다.

### Unit of Work의 해결책

```java
// Unit of Work 방식: 변경을 메모리에 추적 후 한 번에 반영
unitOfWork.begin();
user.setEmail("new@email.com"); // 메모리에만 변경 기록
user.setName("홍길동");          // 메모리에만 변경 기록
user.setPhone("010-1234-5678"); // 메모리에만 변경 기록
unitOfWork.commit(); // 한 번의 UPDATE로 모든 변경 반영
// 예외 발생 시: unitOfWork.rollback() → 전체 취소
```

📢 **섹션 요약 비유**: 장보기 카트(Unit of Work)에 물건을 담다가 마음이 바뀌면 카트에서 꺼내면 된다. 계산대(commit)에 갔을 때 최종 목록만 결제된다. 진열대에 물건을 놓고 취소(롤백)하면 원상복구된다.

---

## 2. 구성요소

### JPA 영속성 컨텍스트 (Persistence Context) 구조

JPA의 영속성 컨텍스트(Persistence Context)가 Unit of Work의 실제 구현이다.

```
┌─────────────────────────────────────────────────────────────┐
│           영속성 컨텍스트 (Persistence Context)               │
│              = Unit of Work 구현체                           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  1차 캐시 (First-Level Cache)                        │    │
│  │                                                     │    │
│  │  Key (엔티티 클래스 + PK)    Value (엔티티 객체)       │    │
│  │  ────────────────────────  ────────────────────     │    │
│  │  User#1             →      user1 (스냅샷 보관)        │    │
│  │  User#2             →      user2 (스냅샷 보관)        │    │
│  │  Order#10           →      order10 (스냅샷 보관)      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────┐  ┌────────────────┐  ┌─────────────┐  │
│  │  쓰기 지연 저장소  │  │  삭제 목록      │  │  삽입 목록  │  │
│  │ (Write-Behind)  │  │ (DELETE 예약)  │  │ (INSERT 예약) │  │
│  └─────────────────┘  └────────────────┘  └─────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │ flush() (커밋 시 자동)
                               ▼
                          Database
```

### 변경 감지 (Dirty Checking) 메커니즘

```
엔티티 조회 시:
┌──────────┐              ┌────────────────────────────────┐
│ DB 조회   │──────────────►│ 영속성 컨텍스트                  │
│          │              │ ┌──────────┐ ┌─────────────┐  │
└──────────┘              │ │  엔티티   │ │  스냅샷(복사) │  │
                          │ │ (변경됨) │ │  (원본 보관) │  │
                          │ └──────────┘ └─────────────┘  │
                          └────────────────────────────────┘

커밋/flush 시:
[엔티티 현재 상태] vs [스냅샷 원본 상태]
         │                    │
         └───── 비교 ──────────┘
                    │
            다르면 UPDATE SQL 생성
```

| 메커니즘 | 설명 | 효과 |
|:---|:---|:---|
| **1차 캐시** | 같은 트랜잭션 내 동일 PK 재조회 시 DB 미조회 | 반복 SELECT 쿼리 제거 |
| **변경 감지 (Dirty Checking)** | 스냅샷과 현재 상태 비교, 변경 시 자동 UPDATE | `save()` 명시 호출 불필요 |
| **지연 쓰기 (Write-Behind)** | 변경 SQL을 모아서 flush 시 일괄 전송 | DB 왕복 횟수 최소화 |
| **트랜잭션 쓰기 지연** | 커밋 전까지 SQL 보류 | 부분 반영 방지 |

📢 **섹션 요약 비유**: 노트 필기(스냅샷)와 현재 노트를 비교해서 수정된 부분만 eraser로 지우고 다시 쓰는 것이 Dirty Checking이다. 처음부터 전부 다시 쓰지 않아도 된다.

---

## 3. 구조 및 동작 원리

### 영속 상태(Entity State) 전환 다이어그램

```
                   new User()
                       │
                       ▼
              ┌─────────────────┐
              │  비영속 (New)    │  ← 영속성 컨텍스트 밖
              └────────┬────────┘
                       │ em.persist()
                       ▼
              ┌─────────────────┐
              │  영속 (Managed)  │  ← UoW가 추적 중
              └────────┬────────┘
                  ┌────┴────┐
         detach() │         │ remove()
                  ▼         ▼
        ┌──────────────┐  ┌──────────────┐
        │ 준영속        │  │ 삭제          │
        │ (Detached)   │  │ (Removed)    │
        └──────────────┘  └──────────────┘
```

### Unit of Work 패턴 구현 비교

| 구현체 | 언어/프레임워크 | 핵심 API |
|:---|:---|:---|
| JPA EntityManager | Java | `persist()`, `flush()`, `commit()` |
| Hibernate Session | Java | `save()`, `flush()`, `evict()` |
| Entity Framework DbContext | C# .NET | `SaveChanges()`, `ChangeTracker` |
| SQLAlchemy Session | Python | `session.add()`, `session.commit()` |
| ActiveRecord (Rails) | Ruby | `save()`, `transaction {}` |

📢 **섹션 요약 비유**: 쇼핑몰 장바구니(1차 캐시)에 담긴 상품은 결제(commit)하기 전까지 실제로 팔린 게 아니다. 장바구니를 보고 "이건 할인됐네" 하고 가격이 바뀌어도(Dirty Checking), 결제 버튼 눌러야 최종 확정된다.

---

## 4. 비교 및 트레이드오프

### JPA에서 Unit of Work 활용 패턴

```java
@Service
@Transactional  // = Unit of Work 시작
public class OrderService {

    @Autowired
    private UserRepository userRepository;

    public void updateUserAndCreateOrder(Long userId, OrderRequest req) {
        // 1. 조회 (1차 캐시에 등록)
        User user = userRepository.findById(userId).orElseThrow();

        // 2. 도메인 변경 (UoW가 변경 추적 시작)
        user.incrementOrderCount();

        // 3. 새 엔티티 영속화
        Order order = Order.create(user, req.getItems());
        orderRepository.save(order); // INSERT 예약

        // 4. 트랜잭션 종료 시 자동 flush:
        //    - user 변경 감지 → UPDATE users SET order_count = ?
        //    - order 신규 → INSERT INTO orders ...
        //    → 하나의 DB 트랜잭션으로 일괄 처리
    }
}
```

### 주의사항 및 함정

| 함정 | 원인 | 해결 |
|:---|:---|:---|
| **N+1 문제** | 지연 로딩 연관 객체 반복 조회 | Fetch Join, BatchSize 설정 |
| **변경 감지 미작동** | 트랜잭션 밖에서 엔티티 수정 | `@Transactional` 범위 확인 |
| **동일성 보장 깨짐** | 다른 EntityManager에서 조회 | 동일 영속성 컨텍스트 사용 |
| **메모리 과부하** | 대량 데이터 영속성 컨텍스트 적재 | `clear()`, `flush()` 주기적 호출 |

📢 **섹션 요약 비유**: JPA 영속성 컨텍스트는 머릿속 메모장이다. 중요한 건 뇌(메모리)에 기억해두고, 퇴근할 때(commit) 한꺼번에 파일(DB)로 저장한다. 뇌 메모리가 너무 차면(대량 처리) 중간중간 파일로 저장(flush/clear)해야 한다.

---

## 5. 실무 적용 및 최적화 기법

### Unit of Work 도입 기대효과

| 기대효과 | 구체적 내용 |
|:---|:---|
| **DB 왕복 최소화** | 여러 변경을 하나의 트랜잭션으로 일괄 처리 |
| **데이터 일관성** | 부분 실패 없이 전부 성공 또는 전부 롤백 |
| **코드 단순화** | 명시적 UPDATE SQL 작성 불필요 (변경 감지) |
| **성능 향상** | 1차 캐시로 반복 SELECT 제거 |
| **충돌 감지** | 낙관적 잠금(Optimistic Locking)과 결합하여 동시 수정 감지 |

Unit of Work 패턴은 ORM(Object-Relational Mapping) 프레임워크의 존재 이유이기도 하다. JPA의 `@Transactional` 하나로 복잡한 UoW 관리를 자동화할 수 있지만, 내부 동작을 모르면 N+1 문제, 변경 감지 미작동, 더티 리드(Dirty Read) 같은 함정에 빠진다. **"JPA를 쓴다면 Unit of Work를 이해하는 것이 필수"** 다.

📢 **섹션 요약 비유**: 은행 ATM에서 이체할 때 출금과 입금이 동시에 성공하거나 동시에 실패해야 한다. Unit of Work는 두 변경을 묶어서 "원자성"을 보장하는 보이지 않는 ATM 보안 시스템이다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 트랜잭션 (Transaction) | ACID 속성 보장의 기반 |
| 상위 개념 | PoEAA (Martin Fowler) | Unit of Work 패턴의 공식화 출처 |
| 하위 개념 | JPA 영속성 컨텍스트 | Java에서의 UoW 구현체 |
| 하위 개념 | 변경 감지 (Dirty Checking) | UoW의 핵심 메커니즘 |
| 연관 개념 | Repository 패턴 | UoW와 협력하여 트랜잭션 관리 |
| 연관 개념 | 낙관적 잠금 (Optimistic Locking) | 동시성 충돌 감지에 UoW 활용 |
| 연관 개념 | 지연 로딩 (Lazy Loading) | UoW 내 연관 객체 로딩 전략 |

### 👶 어린이를 위한 3줄 비유 설명

- 숙제 할 때 틀린 문제를 바로 지우개로 지우지 않고, 다 풀고 나서 한꺼번에 검토하고 수정하는 것이 Unit of Work다.
- 중간에 잘못됐으면 숙제 전체를 찢어버리고(롤백) 처음부터 다시 쓰면 된다.
- JPA는 이 과정을 자동으로 해주는 "스마트 숙제 도우미"다.
