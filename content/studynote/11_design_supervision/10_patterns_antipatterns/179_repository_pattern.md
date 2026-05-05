+++
weight = 179
title = "179. 레파지토리 패턴 (Repository Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 레파지토리 (Repository) 패턴은 DDD (Domain-Driven Design)에서 도메인 객체의 컬렉션처럼 동작하는 추상화 레이어로, 인프라 기술(DB)을 도메인으로부터 완전히 격리한다.
> 2. **가치**: "인메모리 컬렉션(List, Map)처럼 도메인 객체를 다룰 수 있다"는 추상화가 도메인 모델의 순수성을 지키고, JPA 교체나 DB 변경을 도메인 코드 수정 없이 가능하게 한다.
> 3. **판단 포인트**: DAO는 DB 테이블 중심(기술 관점), Repository는 도메인 Aggregate(비즈니스 관점) 중심이다. DDD를 적용하는 시스템에서는 DAO보다 Repository가 더 적합하다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### DDD와 Repository

마틴 파울러(Martin Fowler)의 『Patterns of Enterprise Application Architecture』와 에릭 에반스(Eric Evans)의 『Domain-Driven Design』에서 Repository 패턴이 공식화되었다.

Repository의 핵심 아이디어는 다음과 같다.

> **"데이터베이스가 아니라 컬렉션처럼 다루어라"**

```java
// DAO 방식 (DB 중심 사고)
userDao.executeQuery("SELECT * FROM users WHERE id = ?", id);
userDao.update("UPDATE users SET email = ? WHERE id = ?", email, id);

// Repository 방식 (도메인 객체 컬렉션 사고)
User user = userRepository.findById(id);
user.changeEmail(email); // 도메인 메서드
userRepository.save(user);
```

DAO는 "SQL을 실행한다"는 사고, Repository는 "컬렉션에서 찾아서 수정한다"는 사고다.

### Repository가 필요한 이유

| 문제 | DAO 방식의 한계 | Repository의 해결 |
|:---|:---|:---|
| 도메인 순수성 | 도메인 코드에 DB 기술 코드 침투 | 도메인은 인터페이스만 의존 |
| 테스트 어려움 | DB 없이 도메인 로직 테스트 불가 | InMemoryRepository로 도메인 테스트 |
| 애그리게이트 경계 | 테이블 단위 접근으로 애그리게이트 파편화 | 애그리게이트 루트 단위 접근 |

📢 **섹션 요약 비유**: DAO는 창고 관리인이 "창고 B구역 3번 선반에서 가져오기"라고 말하는 것이고, Repository는 "고객 컬렉션에서 홍길동씨 찾기"라고 말하는 것이다. 후자가 비즈니스 언어다.

---

## 2. 구성요소

### Repository 구조 다이어그램

```
┌──────────────────────────────────────────────────────────────┐
│                     Domain Layer                             │
│                                                              │
│  ┌────────────────┐     ┌────────────────────────────────┐   │
│  │  UserService   │────►│  <<interface>>                 │   │
│  │ (도메인 서비스)  │     │  UserRepository                │   │
│  └────────────────┘     │  + findById(UserId): User      │   │
│                         │  + findByEmail(Email): User    │   │
│  ┌────────────────┐     │  + save(User)                  │   │
│  │  User          │     │  + remove(User)                │   │
│  │ (Aggregate Root)     └────────────────┬───────────────┘   │
│  │ + changeEmail()│                      │                   │
│  └────────────────┘                      │                   │
└─────────────────────────────────────────┼────────────────────┘
                                           │ implements
┌─────────────────────────────────────────┼────────────────────┐
│             Infrastructure Layer        │                    │
│                                         │                    │
│          ┌──────────────────────────────▼──────────────┐     │
│          │  JpaUserRepository                          │     │
│          │  (JPA 구현체)                                │     │
│          └──────────────────────────────────────────────┘     │
│                                                              │
│          ┌──────────────────────────────────────────────┐     │
│          │  InMemoryUserRepository                      │     │
│          │  (테스트용 인메모리 구현체)                     │     │
│          └──────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

### Spring Data JPA Repository 계층 구조

```
Repository (최상위 인터페이스)
    │
    ▼
CrudRepository<T, ID>
│  + save(T), findById(ID), findAll(), delete(T)
│
    ▼
PagingAndSortingRepository<T, ID>
│  + findAll(Pageable), findAll(Sort)
│
    ▼
JpaRepository<T, ID>
   + flush(), saveAndFlush(), deleteInBatch()
   + findAll(Example), getOne(ID)
```

### Aggregate Root와 Repository의 1:1 관계

```
┌──────────────────────────────────────────────────────────┐
│                    Order Aggregate                        │
│                                                          │
│  ┌──────────────────┐   포함   ┌──────────────────┐      │
│  │  Order           │─────────►│  OrderItem       │      │
│  │ (Aggregate Root) │          │  (Value Object)  │      │
│  └──────────────────┘          └──────────────────┘      │
│           │                                               │
└───────────┼───────────────────────────────────────────────┘
            │
            ▼  ← Repository는 Aggregate Root만 접근
    OrderRepository (인터페이스)
    (OrderItemRepository는 별도로 존재하지 않음)
```

📢 **섹션 요약 비유**: 책장(Repository)에서 책(Aggregate)을 찾을 때, 책의 특정 페이지(하위 객체)를 직접 꺼내지 않는다. 항상 책 전체를 꺼내서 필요한 페이지를 읽는다.

---

## 3. 구조 및 동작 원리

### Repository vs DAO 상세 비교

| 비교 항목 | Repository 패턴 | DAO 패턴 |
|:---|:---|:---|
| **출처** | DDD (Eric Evans, 2003) | J2EE Core Patterns (Sun, 2001) |
| **추상화 관점** | 도메인 컬렉션 (비즈니스 관점) | DB 테이블 (기술 관점) |
| **단위** | Aggregate Root 1개 ↔ Repository 1개 | DB 테이블 1개 ↔ DAO 1개 |
| **메서드 언어** | `findByCustomerEmail()` (도메인 언어) | `selectByEmail()` (SQL 언어) |
| **도메인 모델** | 풍부한 도메인 객체 반환 | DTO/VO 반환 |
| **인프라 결합도** | 도메인에서 인프라 완전 격리 | 구현에 SQL/JDBC 노출 가능 |
| **적합 아키텍처** | DDD, 헥사고날 아키텍처 | 단순 CRUD, 3계층 아키텍처 |

### Repository 구현 전략

| 구현 방식 | 장점 | 단점 | 적합 상황 |
|:---|:---|:---|:---|
| Spring Data JPA | 코드 최소화 | 복잡한 쿼리 제한 | CRUD 위주 단순 조회 |
| JPA + @Query | 커스텀 쿼리 지원 | JPQL 학습 필요 | 중간 복잡도 |
| QueryDSL | 타입 안전 복잡 쿼리 | 초기 설정 복잡 | 복잡한 동적 쿼리 |
| InMemoryRepository | DB 없는 단위 테스트 | 실제 환경과 차이 | 테스트 전용 |

📢 **섹션 요약 비유**: DAO는 "SQL 번역가"고, Repository는 "도메인 언어 통역관"이다. 통역관은 내부적으로 SQL을 쓸 수도 있지만, 대화는 항상 도메인 언어로 한다.

---

## 4. 비교 및 트레이드오프

### Spring Data JPA 구현 예시

```java
// 도메인 계층의 Repository 인터페이스 (인프라 기술 없음)
public interface UserRepository {
    Optional<User> findById(UserId id);
    Optional<User> findByEmail(Email email);
    List<User> findAll();
    void save(User user);
    void remove(User user);
}

// 인프라 계층의 Spring Data JPA 구현
@Repository
public interface UserJpaRepository extends JpaRepository<UserEntity, Long> {
    Optional<UserEntity> findByEmail(String email);
}

// 어댑터: 인프라와 도메인을 연결
@Component
public class UserRepositoryAdapter implements UserRepository {
    private final UserJpaRepository jpaRepository;
    private final UserMapper mapper;

    @Override
    public Optional<User> findById(UserId id) {
        return jpaRepository.findById(id.getValue())
                            .map(mapper::toDomain);
    }
}

// 테스트용 InMemory 구현체 (DB 불필요)
public class InMemoryUserRepository implements UserRepository {
    private final Map<UserId, User> store = new HashMap<>();

    @Override
    public Optional<User> findById(UserId id) {
        return Optional.ofNullable(store.get(id));
    }

    @Override
    public void save(User user) {
        store.put(user.getId(), user);
    }
}
```

### 헥사고날 아키텍처(Ports & Adapters)에서의 Repository

```
┌────────────────────────────────────────────────────┐
│               Application Core (Domain)             │
│                                                    │
│  UserService ──► UserRepository (Port/Interface)   │
│                                                    │
└────────────────────────────┬───────────────────────┘
                             │ implements (Adapter)
                ┌────────────▼────────────────────┐
                │  JpaUserRepositoryAdapter        │
                │  (Infrastructure Adapter)        │
                └─────────────────────────────────┘
```

📢 **섹션 요약 비유**: 전기 콘센트 규격(Repository 인터페이스)이 표준화되어 있으면, 어떤 나라의 전자제품(JPA 어댑터, InMemory 어댑터)이든 변환 플러그만 꽂으면 동작한다.

---

## 5. 실무 적용 및 최적화 기법

### Repository 패턴 도입 기대효과

| 기대효과 | 구체적 내용 |
|:---|:---|
| **도메인 순수성** | 비즈니스 로직에 JPA, JDBC 코드 없음 |
| **테스트 용이성** | InMemoryRepository로 빠른 단위 테스트 |
| **기술 독립성** | JPA → MongoDB 전환 시 도메인 코드 무변경 |
| **DDD 실현** | 애그리게이트 경계를 Repository가 보장 |
| **팀 협업** | 도메인 팀과 인프라 팀의 독립적 개발 |

Repository 패턴은 단순한 DAO의 "업그레이드"가 아니라, **도메인 주도 설계의 철학을 코드로 실현하는 구조적 선택**이다. 복잡한 비즈니스 도메인을 가진 시스템일수록, Repository 패턴이 장기적으로 시스템의 유지보수성과 확장성을 결정짓는 핵심 설계가 된다.

📢 **섹션 요약 비유**: DAO가 창고(DB)의 "위치 기반 주소 시스템"이라면, Repository는 도서관의 "주제 기반 분류 시스템"이다. 원하는 책을 찾는 방법이 훨씬 자연스럽다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | DDD (Domain-Driven Design) | Repository 패턴의 이론적 기반 |
| 상위 개념 | 헥사고날 아키텍처 | Repository는 Secondary Port |
| 하위 개념 | Aggregate Root | Repository가 관리하는 단위 |
| 하위 개념 | Spring Data JPA | Java Repository 구현 프레임워크 |
| 연관 개념 | DAO 패턴 | 기술 관점의 유사 패턴 |
| 연관 개념 | Unit of Work 패턴 | Repository와 함께 트랜잭션 관리 |
| 연관 개념 | Specification 패턴 | 복잡한 조건 쿼리를 Repository에 전달 |

### 👶 어린이를 위한 3줄 비유 설명

- 도서관 사서(Repository)는 "홍길동이 쓴 동화책 주세요"라는 말을 알아듣는다. 창고(DB)에서 직접 꺼내오지만 우리는 그냥 요청만 하면 된다.
- DAO 방식 사서는 "3층 동관 B27 선반 5번 책 가져와"라고 말해야 알아듣는다 — 창고 구조를 외워야 한다.
- Repository는 도메인 언어(비즈니스 용어)로 말할 수 있는 스마트한 사서다.
