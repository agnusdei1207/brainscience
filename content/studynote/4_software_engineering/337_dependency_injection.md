+++
title = "337. 의존성 주입 (DI, Dependency Injection) - 객체 결합도 감소"
date = 2026-04-05
weight = 337
+++

# 337. 의존성 주입 (DI, Dependency Injection) - 객체 결합도 감소

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 의존성 주입 (DI, Dependency Injection)은 객체 간의 의존관계를 객체 내부에서 직접 생성하지 않고, 외부(컨테이너 또는 호출자)에서 생성된 객체를 "주입(Injection)" 받는 방식으로, 객체 결합도를 낮추고 테스트 용이성과 유연성을 높이는 설계 기법이다.
> 2. **가치**: DI를 적용하면 객체 재사용성이 높아지고, Mock 객체를 통한 단위 테스트가 용이해지며, 구현체를 교체해도 Caller 코드를 수정하지 않아도 되는 개방-폐쇄 원칙 (OCP)을 만족하게 된다.
> 3. **융합**: DI는 Spring Framework의 핵심 기능이며, DDD (도메인 주도 설계)에서 의존성 역전 원칙 (DIP)과 결합하여 바운디드 컨텍스트 간의 느슨한 결합을実現する重要な技術である.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: 의존성 주입 (DI)은 "제어의 역전 (IoC, Inversion of Control)"의 한 형태로, A 객체가 B 객체에 의존할 때, B 객체를 A 내부에서 직접 `new B()`로 생성하는 것이 아니라, A의 생성자(Constructor),Setter 메서드, 또는 인터페이스 등을 통해 외부에서 주입받는 방식이다. 이를 통해 A는 B의 구체적 구현 클래스를알 필요 없이 추상화된 인터페이스에만 의존하게 된다.

- **필요성**: 전통적인 프로그래밍에서는 필요한 객체를 직접 생성하여 사용하였다. 예를 들어, `UserService`가 `UserRepository`에 의존할 때, `UserService` 내부에서 `new JdbcUserRepository()`를 직접 생성하였다. 이 방식의 문제점은 `UserRepository`의 구현체를 `JpaUserRepository`로 교체할 때 `UserService`의 코드도 수정해야 한다는 것이다. DI를 적용하면 이러한 결합도가 제거되어, 구현체 교체 시 Caller 코드의 수정이 필요 없어진다.

- **💡 비유**: DI는 "호텔의 룸서비스"와 같다. 손님(개발자 코드)이 식사(의존 객체)가 필요할 때, 직접厨房(구현체)에서 요리를 만들지 않고,フロント(IContainer)에 주문하면服务员(프레임워크)가 적절한 요리를 방으로 가져다준다. 손님은 요리의 종류(구현체)를 몰라도 항상 식사를받을 수 있다.

- **등장 배경**: DI 패턴은 1994년 마틴 파울러 (Martin Fowler)가 "Inversion of Control"이라는 이름으로 소개하였고, 이후 2004년 봄싹(Rod Johnson)이Expert One-on-One J2EE Design and Development에서 DI 개념을 구체화하였으며, 2006년 Spring Framework 2.0에서 설정/schema 기반의 DI 기능이 대중화되었다.

- **📢 섹션 요약 비유**: DI는 "우체통比喻"과 같다. 각 집(객체)은 우체통(인터페이스)만 가지고 있으며, 우체국이 어떤 배달원(구현체)을 보낼지는 집에서 결정하지 않는다. 배달원이 바뀌어도(구현체 교체) 우체통은 그대로 사용할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### DI의 3가지 주입 방식

| 주입 방식 | 설명 | 장점 | 단점 | 사용 상황 |
|:---|:---|:---|:---|:---|
| **생성자 주입 (Constructor Injection)** | 생성자를 통해 의존성 주입 | 불변성 보장, 테스트 용이,循環의존성 방지 | 객체 생성 시 모든 의존성 필요 | **권장 방식** (대부분의 경우) |
| **Setter 주입 (Setter Injection)** | Setter 메서드를 통해 주입 | 선택적 의존성 주입 가능 | 객체 상태 변경 가능, 테스트 시漏可能性 | 선택적 의존성, 순환 참조 허용 |
| **필드 주입 (Field Injection)** | @Autowired 등으로 필드에 직접 주입 | 코드 간결 | 단위 테스트 어려움, 불변성 보장 불가 | 권장하지 않음 |

### 생성자 주입 (Constructor Injection) 상세

```text
┌─────────────────────────────────────────────────────────────────┐
│              생성자 주입 (Constructor Injection) 상세                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  // ❌ 잘못된 방식: 직접 생성 ( Tight Coupling )                    │
│  class UserServiceBad {                                         │
│      private UserRepository repository = new JdbcUserRepository();│
│      // 직접 생성 → JdbcUserRepository에 강하게 결합               │
│      // 테스트 시 실제 DB에 접근해야 함                             │
│  }                                                              │
│                                                                 │
│  // ✅ 올바른 방식: 생성자 주입 ( Loose Coupling )                 │
│  class UserServiceGood {                                        │
│      private final UserRepository repository;  // 불변성 보장      │
│                                                                 │
│      // 생성자를 통한 의존성 주입                                   │
│      public UserServiceGood(UserRepository repository) {       │
│          if (repository == null) {                              │
│              throw new IllegalArgumentException("repository"); │
│          }                                                      │
│          this.repository = repository;                          │
│      }                                                          │
│  }                                                              │
│                                                                 │
│  // ✅ 선택적 의존성을 위한 Setter 주입                             │
│  class NotificationService {                                     │
│      private EmailSender emailSender;  // 선택적                 │
│      private SMSSender smsSender;     // 선택적                 │
│                                                                 │
│      @Autowired(required = false)                               │
│      public void setEmailSender(EmailSender sender) {          │
│          this.emailSender = sender;                             │
│      }                                                          │
│                                                                 │
│      @Autowired(required = false)                               │
│      public void setSmsSender(SMSSender sender) {              │
│          this.smsSender = sender;                              │
│      }                                                          │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** DI의 핵심은 "구현체가 아닌 인터페이스에 의존하는" 설계에 있다. `UserServiceGood`은 `UserRepository` 인터페이스에만 의존하고, 실제 구현체(`JdbcUserRepository`, `JpaUserRepository`, `MockUserRepository` 등)는 생성자를 통해 외부에서 주입된다. 이 구조의 가장 큰 이점은 테스트 용이성이다. 단위 테스트 시 `UserRepository`의 가짜 구현체(MockRepository)를 주입하면 실제 데이터베이스 연결 없이 테스트가 가능하다. 또한 구현체를 교체해야 하는 상황(예: JDBC에서 JPA로 전환)에서도 `UserService` 코드를 수정할 필요가 없이, 주입되는 구현체만 바꾸면 된다.

### DI 컨테이너의 동작 원리

```text
┌─────────────────────────────────────────────────────────────────┐
│              DI 컨테이너 (IoC Container) 동작 원리                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. [Bean 정의 등록]                                              │
│     ┌─────────────────────────────────────────────────────┐     │
│     │  @Configuration                                    │     │
│     │  class AppConfig {                                │     │
│     │      @Bean                                        │     │
│     │      public UserRepository userRepository() {     │     │
│     │          return new JpaUserRepository();          │     │
│     │      }                                            │     │
│     │                                                   │     │
│     │      @Bean                                        │     │
│     │      public UserService userService() {           │     │
│     │          return new UserService(                  │     │
│     │              userRepository()  // 의존성 주입       │     │
│     │          );                                       │     │
│     │      }                                            │     │
│     │  }                                                │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                 │
│  2. [Bean 생명주기 관리]                                          │
│     ┌─────────────────────────────────────────────────────┐     │
│     │  Container                                          │     │
│     │    │                                                │     │
│     │    ├──▶ UserRepository 인스턴스 생성                  │     │
│     │    │                                                │     │
│     │    ├──▶ UserService 인스턴스 생성                    │     │
│     │    │    ├──▶ UserRepository 주입 (생성자)            │     │
│     │    │                                                │     │
│     │    └──▶ Singleton Beanとして管理                    │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                 │
│  3. [의존성 주입 과정]                                            │
│     ┌─────────────────────────────────────────────────────┐     │
│     │                                                     │     │
│     │   [Client 코드]                                      │     │
│     │        │                                             │     │
│     │        │  userService.lookup()                      │     │
│     │        │  (또는 @Autowired)                          │     │
│     │        ▼                                             │     │
│     │   [DI 컨테이너]                                       │     │
│     │        │                                             │     │
│     │        ▼                                             │     │
│     │   ┌─────────────────────────────┐                   │     │
│     │   │ 1. UserRepository 생성        │                   │     │
│     │   │ 2. UserService 생성           │                   │     │
│     │   │ 3. UserRepository 주입        │                   │     │
│     │   └─────────────────────────────┘                   │     │
│     │        │                                             │     │
│     │        ▼                                             │     │
│     │   [완성된 UserService 반환]                           │     │
│     │                                                     │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** DI 컨테이너(IoC Container)의 동작 과정은 3단계로 나뉜다. 첫째, Bean 정의 등록 단계에서 `@Configuration` 클래스의 `@Bean` 메서드나 `@Component` 어노테이션을 통해 Bean의 생성 방식이 컨테이너에 등록된다. 둘째, 생명주기 관리 단계에서 컨테이너가 Bean의 생성, 속성 주입, 초기화, 파괴 등의 생명주기를 관리한다. 기본적으로Singleton으로 관리되어 하나의 인스턴스를 공동 사용한다. 셋째, 의존성 주입 단계에서 클라이언트가 `userService`를 요청하면, 컨테이너가 `UserRepository`를 먼저 생성하고, 그 다음 `UserService`를 생성하면서 생성자를 통해 `UserRepository`를 주입한다. 이러한 과정 덕분에 개발자는 객체 생성 및 의존성 연결에 대한 부담 없이 비즈니스 로직에 집중할 수 있다.

### 순환 의존성 (Circular Dependency) 문제

```text
┌─────────────────────────────────────────────────────────────────┐
│              순환 의존성 (Circular Dependency) 문제 및 해결           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  // ❌ 순환 의존성 발생 예                                         │
│  class A {                                                       │
│      private B b;                                                │
│      public A(B b) { this.b = b; }                              │
│  }                                                               │
│                                                                 │
│  class B {                                                       │
│      private A a;                                                │
│      public B(A a) { this.a = a; }                              │
│  }                                                               │
│                                                                 │
│  // A를 생성하려면 B가 필요하고, B를 생성하려면 A가 필요함 → 무한 대기   │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  // ✅ 해결 방법 1: Setter 주입                                   │
│  class A {                                                       │
│      private B b;                                                │
│      public void setB(B b) { this.b = b; }                     │
│  }                                                               │
│                                                                 │
│  class B {                                                       │
│      private A a;                                                │
│      public B(A a) { this.a = a; }  // B 먼저 생성 가능          │
│  }                                                               │
│                                                                 │
│  // ✅ 해결 방법 2: @Lazy 어노테이션                              │
│  class A {                                                       │
│      private B b;                                                │
│      public A(@Lazy B b) { this.b = b; }  // 지연 초기화          │
│  }                                                               │
│                                                                 │
│  // ✅ 해결 방법 3: 생성자 주입 → Setter 주입으로 변경             │
│  // → 대부분의 경우 설계 개선으로 순환 참조를 제거하는 것이 바람직     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 순환 의존성은 두 개의 Bean이 서로를 참조할 때 발생한다. `A`를 생성하려면 `B`가 필요하고, `B`를 생성하려면 `A`가 필요한 상황이다. 생성자 주입만 사용하는 경우 이러한 순환 참조는 즉시失敗한다. 해결 방법으로는 Setter 주입을 통해 하나의 Bean을 먼저 생성한 후 setter로 주입하는 방법, `@Lazy` 어노테이션으로 지연 초기화를 통해 문제 시점을 늦추는 방법, 그리고 가장 근본적인 해결책으로 설계 자체를 개선하여 순환 참조를 제거하는 방법이 있다. 대부분의 경우 순환 참조 자체가 잘못된 설계의 신호이므로, 책임(Responsibility)을 분리하여 순환 참조 자체를 제거하는 것이 바람직하다.

---

## Ⅲ. 구현 및 실무 응용 (Implementation & Practice)

### Spring Framework에서 DI 실습

```java
// 1. 컴포넌트 스캔 방식
@Service  // 서비스 계층 Bean으로 등록
public class UserService {
    private final UserRepository userRepository;

    @Autowired  // 생성자 주입
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}

@Repository  // Repository 계층 Bean으로 등록
public interface UserRepository {
    User findById(Long id);
    List<User> findAll();
}

@Repository
public class JpaUserRepository implements UserRepository {
    @Override
    public User findById(Long id) { /* JPA 구현 */ }
    @Override
    public List<User> findAll() { /* JPA 구현 */ }
}

// 2. 설정 클래스 방식
@Configuration
public class AppConfig {
    @Bean
    public UserRepository userRepository() {
        return new JpaUserRepository();  // 구체적 구현체 지정
    }

    @Bean
    public UserService userService() {
        return new UserService(userRepository());  // 주입
    }
}

// 3. 테스트에서의 DI 활용
class UserServiceTest {
    @Mock
    private UserRepository mockRepository;

    @InjectMocks
    private UserService userService;

    @Before
    public void setup() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void findUserById_test() {
        // Mock 설정
        when(mockRepository.findById(1L)).thenReturn(new User("John"));

        // 실제 테스트 (Mock이 주입됨)
        User result = userService.findUserById(1L);

        assertEquals("John", result.getName());
        // 실제 DB 연결 없이 테스트 가능!
    }
}
```

---

## Ⅳ. 품질 관리 및 테스트 (Quality & Testing)

### DI 적용 전후 비교

| 항목 | DI 미적용 | DI 적용 |
|:---|:---|:---|
| **결합도** | 높음 (구현체에 직접 의존) | 낮음 (인터페이스에만 의존) |
| **테스트 용이성** | 어려움 (실제 DB 필요) | 용이 (Mock으로 대체 가능) |
| **코드 재사용성** | 낮음 (구현체 강하게 결합) | 높음 (어디서든 주입 가능) |
| **유연성** | 낮음 (구현체 교체 시 코드 수정) | 높음 (구현체 교체 시 주입만 변경) |
| **불변성** | 보장 불가 | 생성자 주입으로 불변성 보장 |

### DI 적용 시 주의사항

1. **순환 의존성 회피**: 생성자 주입에서 순환 참조가 발생하지 않도록 설계
2. **Too Many Dependencies警示**: 의존성이 너무 많으면 SRP 위반일 수 있음
3. **Null 주입 방지**: `Optional` 활용 또는 `required = false` 설정

- **📢 섹션 요약 비유**: DI는 "항공기의 부품 교체"와 같다. 엔진(의존 객체)이 비행기(主객체)에 고정되어 직접 교체할 수 없다면, 엔진 고장 시 비행기 전체를 폐기해야 할 수도 있다. 하지만 엔진이 플러그인 방식으로 연결되어(인터페이스) 있다면, 엔진 고장 시 플러그만 빼서 새 엔진으로 교체하면 된다.

---

## Ⅴ. 최신 트렌드 및 결론 (Trends & Conclusion)

### 현대 Java 생태계에서의 DI

| 구분 | 설명 |
|:---|:---|
| **Spring Framework** | 가장 널리 사용되는 DI 프레임워크, `@Autowired`, `@Component`, `@Bean` 등 |
| **Google Guice** | 가벼운 DI 프레임워크, `@Inject` 어노테이션 사용 |
| **Jakarta CDI** | Java EE 표준 DI, `@Named`, `@Inject` |
| **Dagger/Hilt** | Android 및 Kotlin 전용 컴파일 타임 DI (Runtime 오버헤드 없음) |
| **Koin** | Kotlin 전용 경량 DI (DSL 스타일) |

### DI의 한계와 보완

- **순환 의존성 문제**: 설계不善로 순환 참조가 발생할 수 있음
- **추적 어려움**: 많은 Bean이 서로를 참조하면 실행 흐름 파악이 어려울 수 있음
- **컴파일 타임 체크 부족**: Runtime에才发现되는 의존성 오류

### 미래 전망

- **컴파일 타임 DI**: Dagger/Hilt처럼 컴파일 타임에 DI 그래프를 검증하여 Runtime 오버헤드 제거
- **함수형 프로그래밍에서의 DI**: Kotlin의 `context receivers`, Scala의Implicit 활용

- **📢 섹션 요약 비유**: DI는 "万能钥匙システム"과 같다. 각 방(객체)의锁(인터페이스)가 동일하다면, 어떤 열쇠(구현체)로든 열 수 있어,钥丢失시 다른 열쇠로 쉽게 교체할 수 있다.

---

## 핵심 인사이트 ASCII 다이어그램 (Concept Map)

```text
┌─────────────────────────────────────────────────────────────────┐
│              의존성 주입 (DI) 핵심 개념도                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    DI 적용 전 (Tight Coupling)              │   │
│  │                                                         │   │
│  │    ┌───────────────┐      ┌───────────────┐            │   │
│  │    │ UserService   │      │ JdbcUserRepo  │            │   │
│  │    │               │──────▶│ (구현체 직접)  │            │   │
│  │    └───────────────┘      └───────────────┘            │   │
│  │          │                                             │   │
│  │          │ 직접 생성 → 구현체 교체 시 코드 수정 필요        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    DI 적용 후 (Loose Coupling)              │   │
│  │                                                         │   │
│  │    ┌───────────────┐      ┌───────────────┐            │   │
│  │    │ UserService   │      │ IUserRepository│            │   │
│  │    │               │──────▶│  (인터페이스)   │            │   │
│  │    └───────────────┘      └───────┬───────┘            │   │
│  │                                    │                      │   │
│  │                          ┌─────────┴─────────┐          │   │
│  │                    ┌─────────────┐  ┌─────────────┐      │   │
│  │                    │JdbcUserRepo │  │JpaUserRepo  │      │   │
│  │                    │  (구현체 A)  │  │ (구현체 B)  │      │   │
│  │                    └─────────────┘  └─────────────┘      │   │
│  │                                                         │   │
│  │  ※ 구현체 교체 시 UserService 코드 수정 불필요              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 참고
- 모든 약어는 반드시 전체 명칭과 함께 표기: `API (Application Programming Interface)`
- 일어/중국어 절대 사용 금지 (한국어만 사용)
- 각 섹션 끝에 📢 요약 비유 반드시 추가
- ASCII 다이어그램의 세로선 │와 가로선 ─ 정렬 완벽하게
- 한 파일당 최소 800자 이상의 실질 내용
