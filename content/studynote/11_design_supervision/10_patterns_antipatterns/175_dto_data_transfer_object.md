+++
weight = 175
title = "175. DTO 패턴 (DTO, Data Transfer Object)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: DTO (Data Transfer Object, 데이터 전송 객체)는 계층 간 통신 시 여러 번의 원격 호출을 단 한 번으로 줄이기 위해 필요한 데이터를 하나의 객체에 묶어 전송하는 패턴이다.
> 2. **가치**: 비즈니스 로직을 갖지 않는 순수 데이터 컨테이너로서, 도메인 모델(Domain Model)의 내부 구조를 외부에 노출하지 않고 API 응답 형태를 자유롭게 제어할 수 있다.
> 3. **판단 포인트**: VO (Value Object), Entity, 도메인 모델과의 혼용은 응집도 붕괴와 빈혈 도메인 모델(Anemic Domain Model) 안티패턴을 유발하므로 각 개념의 경계를 명확히 구분해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 마틴 파울러(Martin Fowler)의 DTO 정의

마틴 파울러는 『Patterns of Enterprise Application Architecture (엔터프라이즈 애플리케이션 아키텍처 패턴)』(2002)에서 DTO를 다음과 같이 정의했다:

> "단순히 데이터를 저장하고 가져오는 것 외에 다른 기능이 없는 객체. 원격 인터페이스 호출 횟수를 최소화하기 위해 사용된다."

### 원격 호출 비용 문제

EJB (Enterprise JavaBeans) 환경에서 원격 메서드 호출(RMI, Remote Method Invocation)은 로컬 호출보다 수백~수천 배 느리다. 사용자 정보를 조회할 때:

```
[DTO 없이]
getName()    → 원격 호출 1회
getEmail()   → 원격 호출 2회
getAddress() → 원격 호출 3회
getAge()     → 원격 호출 4회
... 총 N번 호출 → 네트워크 왕복 N회

[DTO 사용]
getUserDTO() → 원격 호출 1회로 모든 데이터 수신
```

현대 Spring 환경에서도 프레젠테이션 계층과 서비스 계층이 별도 JVM이거나, REST API 응답 형식을 도메인 모델과 분리해야 할 때 DTO는 여전히 유효하다.

### DTO의 핵심 특성 3가지

1. **비즈니스 로직 없음**: getter/setter만 보유. 단순 데이터 컨테이너.
2. **직렬화(Serialization) 가능**: 네트워크 전송 또는 계층 간 전달을 위해 `Serializable` 구현.
3. **계층 경계의 데이터 형식 제어**: 도메인 모델을 그대로 노출하지 않고 API 응답에 필요한 필드만 선택.

📢 **섹션 요약 비유**: DTO는 식당에서 음식을 배달할 때 쓰는 포장 박스다. 박스 안에 음식이 담겨 있고, 박스 자체는 조리하거나 맛을 바꾸는 기능이 없다. 배달만 한다.

---

## 2. 구성요소

### 계층별 DTO 변환 흐름

```
┌────────────────────────────────────────────────────────────────┐
│  Client (Browser / Mobile / 외부 시스템)                        │
│                                                                │
│  요청 DTO (Request DTO): { "name": "홍길동", "email": "..." }   │
└───────────────────────────┬────────────────────────────────────┘
                            │ HTTP POST /api/users
                            ▼
┌────────────────────────────────────────────────────────────────┐
│  Controller Layer (컨트롤러 계층)                               │
│                                                                │
│  @RequestBody UserCreateRequest request                        │
│  → UserService.create(request)                                 │
└───────────────────────────┬────────────────────────────────────┘
                            │ DTO → Domain Entity 변환
                            ▼
┌────────────────────────────────────────────────────────────────┐
│  Service Layer (서비스 계층)                                    │
│                                                                │
│  User entity = mapper.toEntity(request);  ← 변환               │
│  User saved  = userRepository.save(entity);                    │
│  UserResponse response = mapper.toDTO(saved);  ← 변환         │
└───────────────────────────┬────────────────────────────────────┘
                            │ 응답 DTO 반환
                            ▼
┌────────────────────────────────────────────────────────────────┐
│  응답 DTO (Response DTO): { "id": 1, "name": "홍길동" }        │
│  (비밀번호 해시, 내부 상태 등 민감 정보 제외)                   │
└────────────────────────────────────────────────────────────────┘
```

### DTO 변환 도구: MapStruct vs ModelMapper

| 항목 | MapStruct | ModelMapper |
|:---|:---|:---|
| **변환 방식** | 컴파일 타임 코드 생성 | 런타임 리플렉션(Reflection) |
| **성능** | 매우 빠름 (일반 Java 코드 수준) | 느림 (리플렉션 오버헤드) |
| **타입 안전성** | 높음 (컴파일 오류로 즉시 감지) | 낮음 (런타임 오류 가능) |
| **설정 방식** | 어노테이션 기반 인터페이스 정의 | 코드 또는 설정 |
| **권장 사용** | 대부분의 신규 프로젝트 | 간단한 프로토타입 |

```java
// MapStruct 예시
@Mapper(componentModel = "spring")
public interface UserMapper {
    UserResponse toDTO(User user);
    User toEntity(UserCreateRequest request);
}
// 컴파일 시 구현체 자동 생성 → 런타임 오버헤드 없음
```

📢 **섹션 요약 비유**: MapStruct는 미리 만들어진 이삿짐 운반 매뉴얼(컴파일 코드)이고, ModelMapper는 이사할 때마다 즉흥적으로 어떻게 옮길지 생각하는(리플렉션) 방식이다.

---

## 3. 구조 및 동작 원리

### DTO vs 유사 개념 구분표

| 개념 | 영문 | 불변성 | 비즈니스 로직 | 영속성 ID | 주요 목적 |
|:---|:---|:---|:---|:---|:---|
| **DTO** | Data Transfer Object | 선택 | 없음 | 없음 | 계층 간 데이터 운반 |
| **VO** | Value Object (값 객체) | 필수 | 제한적 | 없음 | 비즈니스 의미 있는 값 표현 |
| **Entity** | Entity | 선택 | 포함 | 있음 (PK) | JPA 영속성 관리 |
| **Domain Model** | Domain Model | 선택 | 핵심 포함 | 있음 | 비즈니스 행위 표현 |
| **DDD VO** | DDD Value Object | 필수 | 포함 가능 | 없음 | 도메인 의미 있는 불변 값 |

### VO와 DTO의 혼동 주의

```java
// VO (Value Object) - 불변, equals/hashCode 재정의 필수
public final class Money {
    private final BigDecimal amount;
    private final Currency currency;

    // equals/hashCode 로 값 동등성 비교
    // 같은 금액, 같은 통화 = 같은 VO
}

// DTO - 가변 가능, 식별자 없음, 로직 없음
public class OrderSummaryDTO {
    private Long orderId;
    private BigDecimal totalAmount;
    private String status;
    // getter/setter만 보유
}
```

📢 **섹션 요약 비유**: VO(값 객체)는 "1만 원"이라는 개념 자체(같은 금액이면 같은 것)이고, DTO는 영수증(데이터를 옮기는 종이)이다. Entity는 고유 번호가 찍힌 주민등록증(식별자 있음)이다.

---

## 4. 비교 및 트레이드오프

### JSON API 응답 DTO 설계 원칙

```java
// 도메인 모델: 내부 상태 모두 보유
public class User {
    private Long id;
    private String name;
    private String passwordHash;  // 절대 외부 노출 금지
    private LocalDateTime createdAt;
    private UserRole role;
    private List<Order> orders;   // 관계 전체 로드 지양
}

// 응답 DTO: 클라이언트에 필요한 것만
public class UserSummaryDTO {
    private Long id;
    private String name;
    private String roleName;
    // passwordHash 없음, orders 없음
}

// 상세 조회 DTO: 상황에 따라 다른 DTO
public class UserDetailDTO {
    private Long id;
    private String name;
    private String email;
    private String roleName;
    private int orderCount;  // orders 전체 대신 집계값만
}
```

### 빈혈 도메인 모델(Anemic Domain Model) 안티패턴 경계

빈혈 도메인 모델은 도메인 객체가 DTO처럼 데이터만 가지고 비즈니스 로직이 없는 상태다. 마틴 파울러는 이를 안티패턴으로 규정했다.

| 상태 | 설명 | 문제점 |
|:---|:---|:---|
| **정상**: DTO 사용 | 계층 경계에서 데이터 운반용으로만 DTO 사용 | — |
| **안티패턴**: 도메인 객체가 DTO화 | 도메인 모델에 비즈니스 로직 없음, 서비스 계층에 로직 집중 | 객체지향 설계 원칙 위반, 절차적 프로그래밍 |

```java
// 안티패턴: 도메인이 데이터만 보유
class Order {
    private Long id;
    private BigDecimal amount;
    // 비즈니스 메서드 없음
}

// OrderService에 모든 로직이 집중 → 빈혈 도메인
class OrderService {
    void apply10PercentDiscount(Order o) {
        o.setAmount(o.getAmount().multiply(BigDecimal.valueOf(0.9)));
    }
}

// 권장: 도메인이 비즈니스 로직 보유
class Order {
    private BigDecimal amount;
    public void applyDiscount(BigDecimal rate) {
        if (rate.compareTo(BigDecimal.ZERO) < 0) throw new IllegalArgumentException();
        this.amount = amount.multiply(BigDecimal.ONE.subtract(rate));
    }
}
```

### DTO 설계 원칙 요약

| 원칙 | 내용 |
|:---|:---|
| 단방향 의존 | DTO → Domain, Domain → DTO 금지 (순환 의존 방지) |
| 최소 필드 원칙 | 클라이언트에 필요한 필드만 포함 |
| 명확한 네이밍 | `UserDTO` 대신 `UserCreateRequest`, `UserSummaryResponse` |
| 변환 책임 분리 | Mapper 클래스(MapStruct)에 변환 로직 집중 |
| API 버전 관리 | v1/v2 API별 DTO 분리 → 하위 호환성 보장 |

📢 **섹션 요약 비유**: DTO는 마치 레스토랑 메뉴판처럼, 주방(도메인 모델)의 실제 조리 방법을 숨기고 손님(클라이언트)에게 보기 좋은 형태로만 정보를 제공한다.

---

## 5. 실무 적용 및 최적화 기법

DTO 패턴 적용의 기대효과:

- **도메인 모델 보호**: 내부 구현(비밀번호 해시, 내부 상태 플래그 등)을 외부로부터 은닉.
- **API 안정성**: 도메인 변경이 API 응답에 자동으로 영향을 주지 않음. 버전 관리 가능.
- **네트워크 최적화**: 필요한 필드만 전송하여 페이로드(Payload) 최소화.
- **계층 분리 명확화**: 각 계층이 자신의 언어(Request DTO, Response DTO, Entity)로 대화.

DTO의 가장 중요한 교훈은 "역할의 명확성"이다. DTO는 데이터를 운반하는 책임만 지고, 비즈니스 로직은 도메인 모델이 담당한다. 이 경계를 무너뜨리는 순간 빈혈 도메인 모델 안티패턴이 시작된다. 기술사 설계 논술에서 "DTO 남용으로 도메인 모델이 빈혈 상태가 되는 리스크"를 언급하면 높은 수준의 설계 판단력을 보여줄 수 있다.

📢 **섹션 요약 비유**: DTO는 훌륭한 집배원(데이터 운반)이지만, 집배원이 편지 내용을 고쳐 쓰기 시작하면(비즈니스 로직 추가) 우편 시스템이 무너진다. 역할의 경계를 지키는 것이 DTO 패턴의 본질이다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | J2EE Patterns (J2EE 패턴) | Transfer Object 패턴이 공식 명칭 |
| 연관 개념 | VO (Value Object, 값 객체) | 불변 + 동등성(equals), DTO와 혼동 주의 |
| 연관 개념 | Entity | 영속성 ID 보유 JPA 관리 객체 |
| 연관 개념 | Domain Model (도메인 모델) | 비즈니스 로직 포함, DTO의 대척점 |
| 연관 개념 | MapStruct | 컴파일 타임 DTO 변환 코드 생성 도구 |
| 연관 개념 | Anemic Domain Model (빈혈 도메인 모델) | DTO 남용으로 발생하는 안티패턴 |
| 연관 개념 | DDD Value Object | DDD 맥락의 불변 도메인 값 객체 |
| 연관 개념 | Serialization (직렬화) | DTO의 계층 간 전송 기반 기술 |

---

### 👶 어린이를 위한 3줄 비유 설명

- DTO는 학교에서 집으로 가져오는 알림장이에요. 선생님(서비스)이 필요한 내용만 써서 부모님(클라이언트)에게 전달해요.
- 알림장은 학교 비밀(도메인 내부 로직)을 다 쓰지 않고, 부모님이 알아야 할 것만 담아요.
- 알림장이 직접 숙제를 하거나(비즈니스 로직) 선생님 대신 결정하면 안 돼요 — 그냥 전달자예요.
