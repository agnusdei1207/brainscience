+++
weight = 172
title = "172. 빌더 패턴과 불변 객체 (Builder Pattern & Immutable Object)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 빌더(Builder) 패턴은 복잡한 객체 생성 과정을 단계적으로 분리하여 가독성을 높이고, 생성 완료 시점에 검증(Validation)하여 불변 객체(Immutable Object)를 안전하게 반환한다.
> 2. **가치**: 텔레스코핑 생성자(Telescoping Constructor) 안티패턴과 자바빈즈(JavaBeans)의 불일관 상태(Inconsistent State) 문제를 동시에 해결한다.
> 3. **판단 포인트**: 생성자 파라미터가 4개 이상이거나, 선택적 필드가 많거나, 멀티스레드(Multi-thread) 환경에서 안전한 불변 객체가 필요할 때 빌더 패턴을 적용하라.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 불변 객체의 필요성

불변 객체(Immutable Object)는 생성 이후 상태가 절대 변하지 않는 객체다. 이 특성은 세 가지 강점을 제공한다:

1. **스레드 안전성(Thread Safety)**: 상태 변경이 없으므로 동기화(Synchronization) 없이 여러 스레드에서 공유 가능.
2. **부작용 없음(Side-Effect Free)**: 메서드가 객체 상태를 변경하지 않으므로 예측 가능.
3. **자유로운 공유 및 캐싱**: 같은 값이면 재사용 가능. `String`, `Integer` 등 Java 기본 타입이 불변.

### 불변 객체 생성의 딜레마

불변 객체는 생성 후 상태를 바꿀 수 없으므로, **생성 시점에 모든 필드를 설정**해야 한다. 필드가 많을수록 생성자 파라미터가 폭발적으로 늘어난다.

```java
// 텔레스코핑 생성자(Telescoping Constructor) 안티패턴
new NutritionFacts(240, 8)
new NutritionFacts(240, 8, 100)
new NutritionFacts(240, 8, 100, 0)
new NutritionFacts(240, 8, 100, 0, 35)
new NutritionFacts(240, 8, 100, 0, 35, 27)  // 무슨 숫자인지 알 수 없음
```

이 코드는 어떤 파라미터가 무엇을 의미하는지 전혀 알 수 없다. 빌더 패턴이 이를 해결한다.

📢 **섹션 요약 비유**: 피자 주문 시 "치즈, 토마토, 올리브, 페퍼로니, 엑스트라 치즈" 순서를 외워서 전화해야 하는 것(텔레스코핑)보다, 주문서에 원하는 것에 체크하는 것(빌더)이 훨씬 명확하다.

---

## 2. 구성요소

### 빌더 패턴 구조도

```
┌─────────────────────────────────────────────────────────────┐
│                    NutritionFacts (불변 객체)                 │
│                                                             │
│  private final int servingSize   (필수)                     │
│  private final int servings      (필수)                     │
│  private final int calories      (선택, 기본값 0)           │
│  private final int fat           (선택, 기본값 0)           │
│  private final int sodium        (선택, 기본값 0)           │
│                                                             │
│  private NutritionFacts(Builder b) { ... }  ← private 생성자│
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  static Builder (내부 정적 클래스)                    │  │
│  │                                                      │  │
│  │  servingSize(int)  → Builder  (메서드 체이닝)         │  │
│  │  servings(int)     → Builder                         │  │
│  │  calories(int)     → Builder                         │  │
│  │  fat(int)          → Builder                         │  │
│  │  sodium(int)       → Builder                         │  │
│  │  build()           → NutritionFacts (검증 후 생성)   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 빌더 패턴 코드 예시

```java
NutritionFacts cocaCola = new NutritionFacts.Builder(240, 8)
    .calories(100)
    .sodium(35)
    .carbohydrate(27)
    .build();    // ← build() 호출 시 검증 및 불변 객체 생성
```

`build()` 메서드 내부에서 필수 필드 누락, 범위 초과 등을 검증하고 위반 시 `IllegalStateException`을 던진다. **생성이 완료된 객체는 항상 유효한 상태**임이 보장된다.

### Lombok @Builder 활용

```java
@Builder
@Value  // 불변 객체 + getter 자동 생성
public class User {
    String name;
    String email;
    int age;
    String address;  // 선택 필드 (기본값 null)
}

// 사용
User user = User.builder()
    .name("홍길동")
    .email("hong@example.com")
    .age(30)
    .build();
```

📢 **섹션 요약 비유**: 건물 설계도(Builder)를 먼저 완성하고, 시공 완료(build()) 후에야 열쇠를 잠가버린다. 완공 후에는 내부를 바꿀 수 없고, 짓는 중에만 수정할 수 있다.

---

## 3. 구조 및 동작 원리

### 세 가지 생성 방식 비교

| 비교 항목 | 텔레스코핑 생성자 | 자바빈즈(JavaBeans) | 빌더 패턴 |
|:---|:---|:---|:---|
| **가독성** | 매우 낮음 (파라미터 순서 암기 필요) | 높음 (set메서드 이름 명확) | 매우 높음 (메서드 체이닝) |
| **불변성** | 가능 | **불가** (setter가 상태 변경) | **가능** (build() 후 불변) |
| **스레드 안전** | 가능 | **불안전** (불일관 상태 노출) | 가능 (불변 객체) |
| **생성 완료 검증** | 가능 (복잡) | **불가** (setter 이후 검증 시점 불명확) | **가능** (build() 에서 일괄 검증) |
| **선택 필드 처리** | 오버로딩 폭발 | setter 선택 호출 | default 값 + 선택 setter |
| **상속 지원** | 어려움 | 가능 | Abstract Builder 패턴으로 가능 |
| **사용 예시** | — | POJO DTO 생성 | 복잡한 도메인 객체, Config 객체 |

### Java `record`와의 비교

Java 16+의 `record` 타입은 불변 객체를 언어 수준에서 지원한다.

| 항목 | `record` | 빌더 패턴 |
|:---|:---|:---|
| 문법 간결성 | 매우 간결 | 보통 (별도 Builder 클래스) |
| 선택 필드 | 어려움 (전체 파라미터 생성자만) | 쉬움 |
| 검증 로직 | compact constructor에서 가능 | build()에서 가능 |
| 상속 | 불가 | 가능 (Abstract Builder) |
| Lombok 대체 | 부분 대체 가능 | — |

📢 **섹션 요약 비유**: 자바빈즈는 레고를 조립한 뒤에도 부품을 계속 교체할 수 있는 완구지만, 그러다 팔이 빠지는(불일관 상태) 사고가 난다. 빌더는 완성 후 에폭시(불변)로 굳혀 절대 부품이 빠지지 않게 한다.

---

## 4. 비교 및 트레이드오프

### 불변 객체 설계 체크리스트

| 항목 | 방법 |
|:---|:---|
| 모든 필드 `final` 선언 | 컴파일 타임에 재할당 차단 |
| 생성자를 `private` 또는 `package-private`으로 | 외부 직접 생성 차단 |
| 방어적 복사(Defensive Copy) | 컬렉션 필드는 `Collections.unmodifiableList()` 래핑 |
| mutable 객체 필드 게터 방어적 반환 | 배열 반환 시 `Arrays.copyOf()` |
| 서브클래싱 차단 | 클래스를 `final`로 선언 |

### 실무 적용 예시: HTTP 요청 빌더

```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Authorization", "Bearer " + token)
    .timeout(Duration.ofSeconds(30))
    .GET()
    .build();
```

Java 11 `HttpRequest`는 빌더 패턴을 네이티브로 적용한 대표 사례다. 불변 객체이므로 여러 스레드에서 동일 `HttpRequest`를 재사용 가능하다.

### 기술사 판단 기준

| 상황 | 권장 방법 |
|:---|:---|
| 파라미터 3개 이하, 모두 필수 | 일반 생성자 |
| 파라미터 4개 이상 또는 선택 필드 많음 | 빌더 패턴 |
| 멀티스레드 안전 불변 객체 필요 | 빌더 + final 필드 |
| 단순 데이터 운반(DTO) | 자바빈즈 또는 record |
| 도메인 객체, 설정 객체 | 빌더 패턴 (Lombok @Builder 활용) |

📢 **섹션 요약 비유**: 자동차 공장에서 컨베이어(빌더)를 따라 엔진 → 내장재 → 도색을 단계별로 조립하고, 최종 품질 검사(build() 검증)를 통과한 차만 출고된다. 출고 후 공장이 차 내부를 임의로 바꾸지 않는다.

---

## 5. 실무 적용 및 최적화 기법

빌더 패턴 + 불변 객체 조합의 기대효과:

- **가독성**: 파라미터 이름을 메서드명으로 표현하여 코드 자체가 문서화.
- **안전성**: 멀티스레드 환경에서 동기화 없이 공유 가능.
- **일관성**: `build()` 완료 후 항상 유효한 상태 보장.
- **유지보수성**: 선택 필드 추가 시 기존 코드 수정 없이 Builder에만 추가.

『Effective Java』 Item 2는 "생성자 파라미터가 많다면 빌더를 고려하라"고 권고한다. 이 패턴은 단순한 편의 기법이 아니라 **설계 원칙(불변성, 유효성 검증 시점, 캡슐화)을 동시에 달성하는 설계 도구**임을 이해해야 한다.

📢 **섹션 요약 비유**: 빌더 패턴은 "주문서 + 품질 검사 + 납품 봉인"을 하나의 프로세스로 묶은 것이다. 주문서가 불완전하면 봉인이 거부되고, 한 번 봉인된 상품은 내용이 절대 바뀌지 않는다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Creational Pattern (생성 패턴) | GoF 5대 생성 패턴 중 하나 |
| 하위 개념 | Fluent Interface (플루언트 인터페이스) | 메서드 체이닝으로 가독성 높인 API 스타일 |
| 연관 개념 | Immutable Object (불변 객체) | 생성 후 상태 변경 불가 객체, 스레드 안전 |
| 연관 개념 | Telescoping Constructor (텔레스코핑 생성자) | 빌더가 해결하는 안티패턴 |
| 연관 개념 | Lombok @Builder | 빌더 패턴 자동 생성 어노테이션 |
| 연관 개념 | Java record | 불변 데이터 클래스를 언어 수준에서 지원 |
| 연관 개념 | Defensive Copy (방어적 복사) | 불변성 유지를 위한 컬렉션 복사 기법 |
| 연관 개념 | Thread Safety (스레드 안전) | 불변 객체의 핵심 이점 |

---

### 👶 어린이를 위한 3줄 비유 설명

- 모래성을 만들 때 모래를 조금씩 조금씩 쌓고(빌더 단계), 다 만들면 단단한 시멘트로 굳혀요(build()).
- 굳은 다음엔 누가 와서 함부로 모래를 빼거나 바꿀 수 없어요(불변 객체).
- 처음부터 시멘트를 혼자 넣으려면(텔레스코핑 생성자) 엄청 무겁고 헷갈리니까, 빌더가 하나씩 도와주는 거예요.
