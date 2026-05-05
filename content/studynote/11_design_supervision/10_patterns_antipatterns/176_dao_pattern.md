+++
weight = 176
title = "176. DAO 패턴 (Data Access Object Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: DAO (Data Access Object) 패턴은 비즈니스 로직과 데이터베이스 접근 코드를 명확히 분리하는 구조적 설계 패턴이다.
> 2. **가치**: Service 레이어는 DAO 인터페이스만 의존하므로 JDBC, JPA, MyBatis 등 구현 기술을 교체해도 상위 레이어 코드가 변경되지 않는다.
> 3. **판단 포인트**: 테스트 용이성(Mock DAO 주입), 기술 교체 유연성, 반복 코드 제거 세 가지가 동시에 충족될 때 DAO 패턴의 도입 가치가 최대화된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

DAO (Data Access Object) 패턴은 Sun Microsystems의 J2EE Core Patterns에서 처음 공식화된 구조적 패턴으로, **도메인/비즈니스 로직과 데이터 영속성(Persistence) 접근 코드를 별도의 계층으로 분리**하는 것이 핵심이다.

### 등장 배경

데이터베이스 접근 코드(SQL, Connection 획득, ResultSet 매핑)가 비즈니스 로직 코드와 혼재하면 다음 문제가 발생한다.

- **기술 종속성**: JDBC 코드가 Service 곳곳에 퍼지면 JPA로 전환 시 전체 Service를 수정해야 한다.
- **테스트 불가**: DB 연결 없이 단위 테스트를 작성하기 어렵다.
- **중복 코드**: 동일한 SQL 문자열이 여러 클래스에 흩어진다.
- **관심사 혼재**: '어떤 데이터를 가져올 것인가(비즈니스)'와 '어떻게 가져올 것인가(기술)'가 뒤섞인다.

### 3계층 아키텍처 내 위치

```
┌─────────────────────────────┐
│   Presentation Layer        │  ← Controller, View
├─────────────────────────────┤
│   Service / Business Layer  │  ← Business Logic, Transaction
├─────────────────────────────┤
│   DAO / Persistence Layer   │  ← Data Access Object
├─────────────────────────────┤
│   Database / Storage        │  ← RDBMS, NoSQL, File
└─────────────────────────────┘
```

DAO 레이어는 데이터베이스 바로 위에서 **영속성 계층(Persistence Layer)** 의 역할을 담당하며, 위 계층(Service)에는 인터페이스만 노출한다.

📢 **섹션 요약 비유**: 레스토랑에서 셰프(Service)는 재료가 냉장고에서 왔는지 창고에서 왔는지 모른다. 재료 조달 담당자(DAO)만 알고 있다. 셰프는 "재료 주세요"만 하면 된다.

---

## 2. 구성요소

### DAO 패턴의 구성 요소

| 구성 요소 | 역할 | 예시 |
|:---|:---|:---|
| DAO Interface | Service가 의존하는 계약 | `UserDao` |
| DAO Implementation | 실제 DB 접근 구현 | `UserDaoJdbcImpl`, `UserDaoJpaImpl` |
| Transfer Object (VO/DTO) | 계층 간 데이터 전달 객체 | `UserDto` |
| Data Source | DB 커넥션 풀 | `HikariCP`, `JNDI DataSource` |

### 클래스 구조 다이어그램

```
┌──────────────────┐        ┌──────────────────┐
│   UserService    │        │  <<interface>>   │
│                  │───────►│    UserDao       │
│ + findUser(id)   │        │ + findById(id)   │
└──────────────────┘        │ + save(user)     │
                            │ + delete(id)     │
                            └────────┬─────────┘
                                     │ implements
              ┌──────────────────────┼─────────────────────┐
              ▼                      ▼                     ▼
  ┌───────────────────┐  ┌──────────────────┐  ┌──────────────────┐
  │ UserDaoJdbcImpl   │  │ UserDaoJpaImpl   │  │ UserDaoMockImpl  │
  │ (JDBC 구현)        │  │ (JPA 구현)        │  │ (테스트용 Mock)   │
  └───────────────────┘  └──────────────────┘  └──────────────────┘
```

Service는 `UserDao` 인터페이스만 바라보기 때문에 구현체를 교체해도 Service 코드는 변경이 없다.

### 데이터 흐름

```
HTTP 요청
    │
    ▼
┌──────────────┐   호출   ┌──────────────┐   호출   ┌──────────────┐
│  Controller  │─────────►│   Service    │─────────►│     DAO      │
│              │          │              │          │  Interface   │
└──────────────┘          └──────────────┘          └──────┬───────┘
                                                           │ 위임
                                                    ┌──────▼───────┐
                                                    │  DAO Impl    │
                                                    │ (JDBC/JPA)   │
                                                    └──────┬───────┘
                                                           │ SQL
                                                    ┌──────▼───────┐
                                                    │   Database   │
                                                    └──────────────┘
```

📢 **섹션 요약 비유**: 인터페이스는 USB 포트 규격이다. 마우스(JDBC 구현), 키보드(JPA 구현) 어떤 것을 꽂아도 컴퓨터(Service)는 동일하게 동작한다.

---

## 3. 구조 및 동작 원리

### DAO vs Repository 패턴 비교

| 비교 항목 | DAO 패턴 | Repository 패턴 |
|:---|:---|:---|
| **관점** | 데이터베이스 테이블 / 기술 접근 관점 | 도메인 모델 / 컬렉션 관점 |
| **출처** | J2EE Core Patterns (Sun) | DDD (Domain-Driven Design, Eric Evans) |
| **추상화 단위** | DB 테이블 1개 ↔ DAO 1개 | 도메인 Aggregate Root ↔ Repository 1개 |
| **반환 타입** | ResultSet, DTO, VO | 도메인 엔티티(Entity), 애그리게이트 |
| **적합 상황** | CRUD 중심 단순 시스템 | 복잡한 비즈니스 규칙을 가진 도메인 모델 |
| **기술 결합도** | 구현체에 JDBC/SQL 노출 가능 | 인프라 기술이 도메인에 영향 없어야 함 |

### DAO vs Active Record 비교

| 비교 항목 | DAO 패턴 | Active Record 패턴 |
|:---|:---|:---|
| **구조** | 도메인 객체와 DB 접근 코드 분리 | 도메인 객체가 DB 접근 메서드도 포함 |
| **복잡도** | 클래스 수 多 (인터페이스 + 구현) | 클래스 수 少 (하나로 통합) |
| **테스트** | Mock DAO 주입으로 단위 테스트 용이 | DB 연결 의존으로 단위 테스트 어려움 |
| **대표 예시** | Spring Data JPA | Ruby on Rails ActiveRecord |

📢 **섹션 요약 비유**: DAO는 "주방장(Service)과 식재료 공급자(DAO)가 별도 계약"이고, Active Record는 "식재료가 스스로 냉장고에서 꺼내오는" 구조다.

---

## 4. 비교 및 트레이드오프

### Spring 환경에서의 DAO 구현 예시

```java
// DAO 인터페이스 (계약)
public interface UserDao {
    Optional<User> findById(Long id);
    List<User> findAll();
    void save(User user);
    void deleteById(Long id);
}

// JDBC 구현체
@Repository
public class UserDaoJdbcImpl implements UserDao {
    private final JdbcTemplate jdbcTemplate;

    @Override
    public Optional<User> findById(Long id) {
        String sql = "SELECT * FROM users WHERE id = ?";
        return jdbcTemplate.queryForObject(sql, userRowMapper(), id);
    }
}

// JPA 구현체 (교체 시 Service 코드 무변경)
@Repository
public class UserDaoJpaImpl implements UserDao {
    @PersistenceContext
    private EntityManager em;

    @Override
    public Optional<User> findById(Long id) {
        return Optional.ofNullable(em.find(User.class, id));
    }
}
```

### 기술사 시험 판단 포인트

| 상황 | DAO 적용 여부 | 이유 |
|:---|:---|:---|
| 단순 CRUD REST API | 적용 권장 | 기술 독립성, 테스트 용이성 |
| 스크립트성 배치 처리 | 선택적 | 과도한 추상화가 오히려 복잡성 증가 |
| 레거시 시스템 통합 | 필수 | 기존 DB 스키마 변경 없이 레이어 추가 |
| 마이크로서비스 전환 | 필수 | 서비스별 데이터 접근 독립성 보장 |

📢 **섹션 요약 비유**: 건물 설계 시 전기 배선(DB 접근)을 벽 안에 매립(코드 혼재)하면 나중에 수리가 어렵다. 전선 관(DAO 인터페이스)을 통해 배선하면 언제든 교체 가능하다.

---

## 5. 실무 적용 및 최적화 기법

### DAO 패턴 도입 시 기대효과

| 기대효과 | 구체적 내용 |
|:---|:---|
| **기술 독립성** | JDBC → JPA → MyBatis 전환 시 Service 코드 무변경 |
| **테스트 용이성** | Mock DAO 주입으로 DB 없는 단위 테스트 가능 |
| **코드 중복 제거** | SQL 쿼리를 DAO에 집중화, 여러 Service에서 재사용 |
| **유지보수성** | 데이터 접근 로직 변경 시 DAO만 수정 |
| **관심사 분리** | 비즈니스 규칙과 인프라 기술의 명확한 경계 |

DAO 패턴은 단순해 보이지만 **엔터프라이즈 애플리케이션의 생존 능력**을 결정하는 핵심 설계 원칙이다. 데이터베이스 기술은 계속 진화하지만(RDBMS → NewSQL → NoSQL), DAO 인터페이스가 견고하면 비즈니스 로직은 영향을 받지 않는다. 이것이 기술 부채를 최소화하면서 시스템을 장기간 유지보수할 수 있는 비결이다.

📢 **섹션 요약 비유**: 좋은 건축가는 건물의 수도 파이프를 교체할 수 있도록 설계한다. DAO는 시스템의 "수도 파이프 교체 설계도"다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 3계층 아키텍처 | Presentation - Service - Persistence 분리 |
| 상위 개념 | 관심사 분리 (SoC) | Separation of Concerns 원칙 |
| 하위 개념 | Transfer Object (DTO/VO) | DAO와 Service 간 데이터 전달 객체 |
| 하위 개념 | Data Source | JDBC Connection Pool (HikariCP 등) |
| 연관 개념 | Repository 패턴 | DDD 관점의 DAO 발전형 |
| 연관 개념 | Active Record 패턴 | 도메인 객체가 DB 접근 포함 (DAO의 반대) |
| 연관 개념 | Unit of Work 패턴 | 트랜잭션 범위 내 변경 추적 및 일괄 반영 |

### 👶 어린이를 위한 3줄 비유 설명

- 도서관 사서(DAO)는 책을 어디서 가져오는지(지하 창고인지, 2층 서고인지) 알고, 학생(Service)은 그냥 "이 책 주세요"만 하면 된다.
- 사서가 바뀌어도(JDBC → JPA), 학생은 똑같이 "이 책 주세요"만 하면 된다.
- 가짜 사서(Mock DAO)를 세워두면 진짜 창고 없이도 책 빌리는 연습(테스트)을 할 수 있다.
