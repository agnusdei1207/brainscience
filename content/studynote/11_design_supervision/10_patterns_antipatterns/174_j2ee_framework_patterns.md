+++
weight = 174
title = "174. J2EE 프레임워크 패턴 (J2EE Framework Patterns)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: J2EE (Java 2 Platform, Enterprise Edition) / Jakarta EE 패턴은 엔터프라이즈 계층(Presentation → Business → Integration) 간 관심사를 분리하여 유지보수성과 확장성을 확보하는 구조적 설계 언어다.
> 2. **가치**: DAO, DTO, Front Controller, Service Locator 등 각 패턴은 특정 계층의 반복적인 설계 문제를 표준화하여 팀 간 공통 어휘를 제공한다.
> 3. **판단 포인트**: 각 패턴의 위치(계층)와 역할 경계를 명확히 해야 한다. 혼용(예: DAO 안에 비즈니스 로직)은 관심사 분리 원칙을 위반하는 대표적 실수다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### J2EE 패턴의 역사적 배경

1990년대 후반 엔터프라이즈 Java 애플리케이션이 복잡해지면서, 반복적인 설계 문제들이 나타났다. Sun Microsystems의 Alur, Crupi, Malks가 2003년 출판한 『Core J2EE Patterns』에서 이를 정리했다. GoF 패턴이 클래스·객체 수준의 설계라면, J2EE 패턴은 **계층(Layer) 수준의 설계**다.

현재 공식 명칭은 **Jakarta EE** (이클립스 재단 이전 후)이지만, 패턴 명칭과 개념은 그대로 사용된다.

### 3계층 아키텍처와 패턴 매핑

```
┌─────────────────────────────────────────────────────────────┐
│  Presentation Layer (프레젠테이션 계층)                       │
│                                                             │
│  Front Controller ─ Application Controller ─ View Helper   │
│  Intercepting Filter ─ Composite View                       │
└──────────────────────────┬──────────────────────────────────┘
                           │ (Business Delegate 경유)
┌──────────────────────────▼──────────────────────────────────┐
│  Business Layer (비즈니스 계층)                               │
│                                                             │
│  Session Facade ─ Application Service ─ Domain Model        │
│  Service Locator ─ Transfer Object Assembler                 │
└──────────────────────────┬──────────────────────────────────┘
                           │ (DAO 경유)
┌──────────────────────────▼──────────────────────────────────┐
│  Integration Layer (통합 계층)                               │
│                                                             │
│  DAO (Data Access Object) ─ Service Activator               │
│  Domain Store ─ Web Service Broker                           │
└─────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 백화점의 안내 데스크(Front Controller), 매장 직원(Business), 창고 담당(DAO)이 각자 역할이 분명하듯, J2EE 패턴은 대형 시스템의 역할 분담표다.

---

## 2. 구성요소

### 7대 핵심 패턴 상세

#### 1. DAO (Data Access Object, 데이터 접근 객체)

DB 접근 로직을 비즈니스 로직에서 분리. 영속성(Persistence) 계층 추상화.

```java
public interface UserDAO {
    User findById(Long id);
    void save(User user);
    void delete(Long id);
}
public class UserJpaDAO implements UserDAO { ... }   // JPA 구현
public class UserJdbcDAO implements UserDAO { ... }  // JDBC 구현
```

DB 기술(JPA, JDBC, MongoDB)을 교체해도 서비스 계층은 무변경.

#### 2. DTO (Data Transfer Object, 데이터 전송 객체)

계층 간 데이터 전송. 비즈니스 로직 없음, getter/setter/직렬화만 보유.

#### 3. Front Controller (프론트 컨트롤러)

모든 HTTP 요청이 단일 진입점을 통과. Spring의 `DispatcherServlet`이 대표 구현체.

```
모든 요청 → DispatcherServlet → HandlerMapping → Controller → View
```

#### 4. Business Delegate (비즈니스 위임자)

프레젠테이션 계층이 비즈니스 서비스를 직접 호출하지 않고 위임자(Delegate)를 통해 호출. 원격 서비스 예외 처리, 캐싱 등을 위임자가 담당.

#### 5. Service Locator (서비스 로케이터)

JNDI (Java Naming and Directory Interface, 자바 네이밍 및 디렉터리 인터페이스) 조회, EJB 룩업 등 서비스 탐색 로직을 캡슐화.

```java
// DI(Dependency Injection)와 반대 개념: 클라이언트가 직접 서비스를 조회
UserService svc = (UserService) ServiceLocator.getService("UserService");
```

⚠️ **DI (Dependency Injection, 의존성 주입)**가 가능한 환경(Spring)에서는 Service Locator는 안티패턴으로 간주된다. 의존성이 숨겨지고 테스트가 어려워진다.

#### 6. Session Facade (세션 파사드)

여러 EJB (Enterprise JavaBeans) 호출을 단일 세션 빈(Session Bean)으로 묶어 클라이언트 측 원격 호출 횟수를 최소화.

##> 📖 학습 보조

## 7. Transfer Object Assembler (전송 객체 조립자)

여러 비즈니스 컴포넌트의 데이터를 조합하여 복합 DTO를 구성.

📢 **섹션 요약 비유**: DAO는 창고 직원, DTO는 배달 박스, Front Controller는 건물 정문 보안 게이트, Business Delegate는 비서, Service Locator는 전화번호부 직접 찾기, Session Facade는 한 번에 여러 심부름을 처리해주는 매니저다.

---

## 3. 구조 및 동작 원리

### 계층별 패턴 책임 요약표

| 패턴 | 계층 | 핵심 책임 | DI와의 관계 |
|:---|:---|:---|:---|
| **Front Controller** | Presentation | 모든 요청의 단일 진입점, 라우팅 | DI로 Handler 주입 |
| **Application Controller** | Presentation | 요청 → 액션/뷰 매핑 결정 | — |
| **Business Delegate** | Presentation↔Business | 비즈니스 서비스 접근 추상화, 예외 변환 | DI로 대체 가능 |
| **Session Facade** | Business | 원격 EJB 호출 묶음, 트랜잭션 경계 | Spring @Service로 진화 |
| **Service Locator** | Business | 서비스 룩업 캡슐화 | DI로 대체 권장 |
| **DAO** | Integration | DB 접근 추상화 | Spring Data JPA로 진화 |
| **DTO** | 전 계층 간 | 데이터 운반, 직렬화 | — |

### J2EE 패턴과 현대 Spring 매핑

| J2EE 패턴 | Spring 대응 기술 |
|:---|:---|
| Front Controller | `DispatcherServlet` |
| Session Facade | `@Service` + `@Transactional` |
| DAO | `@Repository` + Spring Data JPA |
| Service Locator | `@Autowired` (DI로 완전 대체) |
| DTO | POJO DTO + MapStruct/ModelMapper |
| Business Delegate | Spring AOP (관점 지향 프로그래밍)로 횡단관심사 처리 |

📢 **섹션 요약 비유**: J2EE 패턴은 자동차가 없던 시대의 이동 방법(마차, 가마, 걷기)이다. 현대 Spring은 자동차다. 원리(이동)는 같지만 수단(DI, AOP)이 발전했다.

---

## 4. 비교 및 트레이드오프

### DAO 패턴 계층 분리의 실무 가치

```
Service Layer
     │
     │ UserDAO 인터페이스 호출
     ▼
┌────────────────────────────────────┐
│  UserDAO (Interface)               │
│  findById(id) : User               │
│  save(user)                        │
└────────────┬───────────────────────┘
             │
    ┌────────┴──────────┐
    ▼                   ▼
UserJpaDAO          UserMongoDAO
(운영 환경)          (테스트 환경)
```

서비스 계층은 DAO 인터페이스만 알므로, 운영 DB(JPA)와 테스트 인메모리(H2)를 동일 코드로 테스트 가능.

### Service Locator 안티패턴 식별

```java
// 안티패턴: Service Locator
class OrderService {
    void placeOrder(Order o) {
        // 의존성이 메서드 내부에 숨어있음 → 테스트 어려움
        PaymentGateway pg = ServiceLocator.get("PaymentGateway");
        pg.charge(o);
    }
}

// 권장: DI (Dependency Injection)
class OrderService {
    private final PaymentGateway paymentGateway;  // 의존성 명시적 선언

    OrderService(PaymentGateway pg) { this.paymentGateway = pg; }

    void placeOrder(Order o) {
        paymentGateway.charge(o);
    }
}
```

DI 방식은 의존성이 생성자에 명시되어 테스트 시 Mock 주입이 쉽다.

### 기술사 논술 포인트

| 관점 | 서술 내용 |
|:---|:---|
| 계층 분리 | 각 패턴이 어느 계층에 속하고 왜 그 계층에 있어야 하는지 |
| 현대적 진화 | J2EE 패턴 → Spring 기술 매핑 |
| DI와의 관계 | Service Locator 한계와 DI 장점 비교 |
| 테스트 관점 | DAO 인터페이스 → 목(Mock) 주입 → 단위 테스트 가능 |

📢 **섹션 요약 비유**: J2EE 패턴을 아는 기술사는 "왜 DAO가 있는가"를 "테스트 가능성과 DB 교체 유연성"으로 설명할 수 있다. 패턴 이름만 나열하는 것과 목적을 설명하는 것은 다른 수준이다.

---

## 5. 실무 적용 및 최적화 기법

J2EE 패턴 적용의 기대효과:

- **관심사 분리**: 계층별 역할이 명확히 분리되어 병렬 개발 가능.
- **유지보수성**: 한 계층의 기술 교체(DB→클라우드 저장소)가 다른 계층에 미치는 영향 최소화.
- **테스트 용이성**: DAO 인터페이스, Mock Business Delegate로 계층별 독립 테스트.
- **표준화**: 팀 간 공통 설계 어휘 형성 → 코드 리뷰 효율 향상.

J2EE 패턴은 특정 기술(EJB, JNDI)에 종속된 해결책이 많지만, 그 근본 아이디어(계층 분리, 접근 추상화, 단일 진입점)는 현대 마이크로서비스(Microservices) 아키텍처에도 그대로 적용된다. API 게이트웨이(Front Controller), Repository 패턴(DAO), 서비스 메시(Service Locator의 진화)가 그 사례다.

📢 **섹션 요약 비유**: J2EE 패턴은 기업 조직도다. 담당자, 부서, 역할이 명확해야 대기업(엔터프라이즈 시스템)이 혼돈 없이 운영된다. 조직도가 없으면 모두가 모든 일을 하다 아무것도 제대로 안 된다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Enterprise Architecture Pattern | 계층 수준의 설계 패턴 |
| 하위 개념 | DAO (Data Access Object) | DB 접근 추상화 |
| 하위 개념 | DTO (Data Transfer Object) | 계층 간 데이터 운반 |
| 하위 개념 | Front Controller | 단일 요청 진입점 |
| 연관 개념 | DI (Dependency Injection) | Service Locator의 현대적 대안 |
| 연관 개념 | Spring Framework | J2EE 패턴의 현대적 구현체 |
| 연관 개념 | Jakarta EE | J2EE의 현재 공식 명칭 |
| 연관 개념 | Layered Architecture (계층형 아키텍처) | J2EE 패턴의 기반 구조 |

---

### 👶 어린이를 위한 3줄 비유 설명

- Front Controller는 학교 정문 선생님이에요. 모든 학생이 정문을 통과해야 하고, 선생님이 "1반은 왼쪽, 2반은 오른쪽"으로 안내해요.
- DAO는 도서관 사서예요. 책(데이터)이 어디 있는지는 사서만 알고, 학생(서비스)은 "이 책 빌려주세요"라고만 하면 돼요.
- DTO는 책을 담아 나르는 가방이에요. 가방은 책을 옮기기만 하고, 책 내용을 바꾸거나 읽지 않아요.
