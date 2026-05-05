+++
weight = 169
title = "169. 정적 팩토리 메서드 (Static Factory Method)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 정적 팩토리 메서드(Static Factory Method)는 생성자(Constructor) 대신 이름 있는 정적 메서드로 인스턴스를 제공하여, 생성 의도를 명시하고 생성 제어권을 확보한다.
> 2. **가치**: 인스턴스 캐싱(Caching), 하위 타입(Subtype) 반환, 조건부 클래스 선택 등 생성자가 제공할 수 없는 유연성을 단순한 코드로 달성한다.
> 3. **판단 포인트**: 생성자가 여러 개 필요하거나, 같은 시그니처로 다른 의미의 생성이 필요하거나, 반환 타입을 유연하게 제어해야 한다면 정적 팩토리 메서드를 우선 검토하라.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 조슈아 블로흐(Joshua Bloch)의 권고

『Effective Java』 Item 1은 "생성자 대신 정적 팩토리 메서드를 고려하라(Consider static factory methods instead of constructors)"고 권고한다. 이는 생성자의 본질적 한계에서 출발한다.

### 생성자의 한계

| 한계 | 설명 | 예시 문제 |
|:---|:---|:---|
| 이름 없음 | 모든 생성자 이름은 클래스명 고정 | `new Complex(1, 0)`이 실수? 허수? 불명확 |
| 매번 새 객체 | 생성자는 항상 새 인스턴스 반환 | 불필요한 객체 생성, GC 부담 |
| 타입 고정 | 반환 타입이 항상 자신의 클래스 | 인터페이스 타입 반환 불가 |
| 동일 시그니처 불가 | 파라미터 타입·순서 같은 생성자 2개 불가 | `Point(int x, int y)`, `Point(int r, int theta)` 동시 불가 |

### 정적 팩토리 메서드가 이 한계를 극복하는 방식을 5가지 장점으로 정리한다.

📢 **섹션 요약 비유**: 가게 이름이 전부 "가게"이면 어디가 빵집이고 어디가 약국인지 모른다. 정적 팩토리 메서드는 가게에 간판(이름)을 달아주는 것과 같다.

---

## 2. 구성요소

### 5가지 장점

**장점 1. 이름 있는 생성 (Named Constructor)**

```java
// 생성자: 의도 불명확
Complex c1 = new Complex(1, 0);

// 정적 팩토리: 의도 명확
Complex c2 = Complex.ofReal(1);       // 실수 생성
Complex c3 = Complex.ofImaginary(1);  // 허수 생성
```

**장점 2. 인스턴스 캐싱 (Instance Caching / Flyweight)**

```java
// Boolean.valueOf() - 새 객체 생성 안 함
Boolean t1 = Boolean.valueOf(true);   // 캐시된 TRUE 반환
Boolean t2 = Boolean.valueOf(true);   // 동일 인스턴스 반환
// t1 == t2 → true
```

**장점 3. 하위 타입 반환 (Return Subtype)**

```java
// 인터페이스 타입 반환 → 구현 은닉
List<String> list = Collections.unmodifiableList(new ArrayList<>());
// 반환된 실제 타입은 UnmodifiableRandomAccessList, 클라이언트는 몰라도 됨
```

**장점 4. 입력에 따른 다른 클래스 반환 (Input-Dependent Class)**

```java
// 원소 수에 따라 최적 구현 반환
EnumSet<Day> small = EnumSet.of(Day.MON, Day.TUE); // RegularEnumSet (64 이하)
EnumSet<Day> large = EnumSet.allOf(BigEnum.class);  // JumboEnumSet (65 이상)
```

**장점 5. 정적 팩토리 작성 시 반환할 클래스가 없어도 됨 (Service Provider Framework)**

JDBC(Java Database Connectivity)의 `DriverManager.getConnection()`처럼, 반환될 클래스가 런타임에 결정되는 서비스 제공자 프레임워크(Service Provider Framework) 구현 가능.

### 인스턴스 제어 흐름도

```
Client
  │
  │ Boolean.valueOf(true)
  ▼
┌──────────────────────────────────────────────┐
│  Boolean (Static Factory Method)             │
│                                              │
│  valueOf(boolean b) {                        │
│    if (b)                                    │
│      return TRUE;   ◄─── 캐시된 인스턴스     │
│    else                                      │
│      return FALSE;  ◄─── 캐시된 인스턴스     │
│  }                                           │
│                                              │
│  static final Boolean TRUE  = new Boolean(true)  │
│  static final Boolean FALSE = new Boolean(false) │
└──────────────────────────────────────────────┘
```

### 네이밍 컨벤션 (Naming Convention)

| 메서드명 | 사용 맥락 | 예시 |
|:---|:---|:---|
| `of` | 여러 파라미터 집약 | `EnumSet.of(A, B, C)` |
| `from` | 단일 파라미터 타입 변환 | `Date.from(instant)` |
| `valueOf` | `of`/`from`의 장황한 버전 | `Boolean.valueOf(true)` |
| `getInstance` | 싱글턴(Singleton), 캐시 반환 | `Calendar.getInstance()` |
| `create` / `newInstance` | 매번 새 인스턴스 생성 보장 | `Array.newInstance(cls, len)` |
| `get타입` | 팩토리 클래스가 반환 타입과 다를 때 | `Files.getFileStore(path)` |
| `new타입` | 새 인스턴스, 팩토리 클래스 다를 때 | `BufferedReader.newBufferedReader()` |
| `타입` | `get타입`/`new타입`의 간결 버전 | `Collections.list(e)` |

📢 **섹션 요약 비유**: 식당 메뉴판에 "음식"이라고만 쓰지 않고 "김치찌개", "된장찌개"라고 구분하듯, 정적 팩토리는 생성 의도를 메뉴명처럼 명시한다.

---

## 3. 구조 및 동작 원리

### 생성자 vs 정적 팩토리 메서드

| 비교 항목 | 생성자 (Constructor) | 정적 팩토리 메서드 (Static Factory Method) |
|:---|:---|:---|
| **이름** | 클래스명 고정 | 의미 있는 이름 자유롭게 부여 |
| **인스턴스 제어** | 항상 새 객체 생성 | 캐싱, 싱글턴, 풀(Pool) 관리 가능 |
| **반환 타입** | 선언 클래스 타입 고정 | 인터페이스 또는 하위 타입 반환 가능 |
| **상속 여부** | 서브클래스에서 `super()` 호출 | 정적 메서드, 상속 불가 |
| **API 노출** | Javadoc에 자동 노출 | 명시적 규칙 없으면 눈에 안 띔 |
| **GoF 패턴 관계** | — | Singleton, Flyweight, Factory 구현 기반 |

### GoF 패턴 구현 기반으로서의 역할

| GoF 패턴 | 정적 팩토리 활용 |
|:---|:---|
| Singleton (싱글턴) | `getInstance()`로 단일 인스턴스 반환 |
| Flyweight (플라이웨이트) | `valueOf()`로 캐시된 공유 인스턴스 반환 |
| Factory Method (팩토리 메서드) | 정적 메서드로 서브타입 반환 |
| Abstract Factory (추상 팩토리) | 서비스 제공자 프레임워크의 등록·조회 구현 |

📢 **섹션 요약 비유**: 정적 팩토리는 여러 GoF 패턴의 "입구"를 담당하는 안내 데스크와 같다. 어떤 손님(요청)이 와도 적절한 방(구현 클래스)으로 안내한다.

---

## 4. 비교 및 트레이드오프

### 적용 시나리오 판단표

| 시나리오 | 권장 방법 |
|:---|:---|
| 같은 시그니처의 생성 방법이 2개 이상 필요 | 정적 팩토리로 이름 구분 |
| 생성 비용이 크고 재사용 가능한 불변 객체 | 캐싱 팩토리 (`valueOf` 계열) |
| 반환 타입을 숨기고 인터페이스로 노출하고 싶을 때 | 하위 타입 반환 팩토리 |
| 단순 객체 생성, 확장 없음 | 일반 생성자 유지 (복잡도 증가 방지) |

### 단점과 주의사항

**단점 1. 상속 불가**: 정적 팩토리만 갖고 생성자를 `private`으로 막으면 서브클래스를 만들 수 없다. 이는 상속보다 **합성(Composition)을 권장**하는 관점에서는 장점이기도 하다.

**단점 2. 발견성 낮음**: 생성자는 IDE에서 `new` 키워드로 자동완성되지만, 정적 팩토리 메서드는 Javadoc이나 코드 검색 없이 존재를 알기 어렵다. 네이밍 컨벤션 준수가 필수다.

### Java 표준 라이브러리 실사례

```java
// java.time 패키지 - 정적 팩토리 풍부하게 활용
LocalDate today = LocalDate.now();
LocalDate xmas  = LocalDate.of(2026, 12, 25);
LocalDate parsed = LocalDate.parse("2026-12-25");

// Optional - 명시적 생성 의도
Optional<String> present = Optional.of("hello");
Optional<String> empty   = Optional.empty();
Optional<String> nullable = Optional.ofNullable(null);
```

📢 **섹션 요약 비유**: `LocalDate.parse("2026-12-25")`는 "문자열을 날짜로 변환"이라는 의도가 명확하다. 생성자 `new LocalDate("2026-12-25")`라면 "날짜 문자열 파싱"인지 "복사"인지 헷갈릴 것이다.

---

## 5. 실무 적용 및 최적화 기법

정적 팩토리 메서드의 기대효과:

- **API 표현력 향상**: 이름으로 생성 의도 명시 → 가독성·유지보수성 개선.
- **인스턴스 수 제어**: 불필요한 객체 생성 억제 → 메모리·GC 부담 감소.
- **유연한 반환 타입**: 구현 클래스를 숨기고 인터페이스로 노출 → 캡슐화(Encapsulation) 강화.
- **조건부 최적 구현 선택**: 입력에 따라 최적화된 서브클래스 반환 → 성능 최적화.

정적 팩토리 메서드는 GoF 패턴의 구현 기반이 되는 기초 기법이다. 기술사 실무 문제에서 "생성 방식 개선", "인스턴스 관리" 주제가 나오면 이 기법을 설계 선택지로 제시할 수 있다.

📢 **섹션 요약 비유**: 정적 팩토리는 자동화된 주문 시스템이다. 고객이 "카페라떼"(이름)를 주문하면 시스템이 재고(캐시), 사이즈(타입), 준비 방법(알고리즘)을 알아서 처리해준다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Creational Pattern (생성 패턴) | 인스턴스 생성 책임 분리 패턴군 |
| 연관 개념 | Singleton Pattern (싱글턴 패턴) | `getInstance()`로 단일 인스턴스 보장 |
| 연관 개념 | Flyweight Pattern (플라이웨이트) | 캐싱 기반 공유 인스턴스 반환 |
| 연관 개념 | Factory Method Pattern (팩토리 메서드) | 동적 객체 생성, 정적 팩토리의 다형성 버전 |
| 연관 개념 | Service Provider Framework (서비스 제공자 프레임워크) | 런타임 구현 등록·조회, JDBC 방식 |
| 연관 개념 | Effective Java Item 1 | 조슈아 블로흐의 설계 권고 |
| 연관 개념 | OCP (Open-Closed Principle) | 하위 타입 반환으로 확장에 열린 API |

---

### 👶 어린이를 위한 3줄 비유 설명

- 아이스크림 가게에서 "딸기맛 주세요", "초코맛 주세요"라고 말하면 점원이 알아서 아이스크림을 가져다줘요. 직접 냉동고를 열 필요가 없어요.
- 같은 딸기맛을 또 주문하면 이미 꺼내둔 것을 가져다줘요 — 매번 새로 만들지 않아요(캐싱).
- "아이스크림"이라는 이름으로 받지만, 실제로는 소프트아이스크림인지 하드아이스크림인지 모르고, 알 필요도 없어요(하위 타입 반환).
