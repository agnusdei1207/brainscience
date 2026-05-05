+++
weight = 178
title = "178. 인터셉터/필터 패턴 (Interceptor / Filter Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 인터셉터 (Interceptor)와 필터 (Filter)는 AOP (Aspect-Oriented Programming)의 횡단 관심사(인증, 로깅, 인코딩)를 요청/응답 처리 파이프라인에서 분리하는 체인 패턴이다.
> 2. **가치**: 핵심 비즈니스 로직에 영향을 주지 않고 공통 처리를 추가/제거할 수 있어 개방-폐쇄 원칙(OCP, Open-Closed Principle)을 실현한다.
> 3. **판단 포인트**: Filter는 서블릿 컨테이너 레벨(모든 요청 대상), Interceptor는 Spring 컨텍스트 레벨(Spring Bean 접근 가능)이라는 위치 차이가 선택 기준이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 횡단 관심사 문제

소프트웨어에는 **핵심 관심사 (Core Concern)** 와 **횡단 관심사 (Cross-Cutting Concern)** 가 있다.

- **핵심 관심사**: 주문 처리, 결제, 상품 조회 등 비즈니스 로직
- **횡단 관심사**: 인증(Authentication), 인가(Authorization), 로깅(Logging), 트랜잭션(Transaction), 성능 측정

횡단 관심사를 각 Controller/Service에 직접 코딩하면 다음 문제가 발생한다.

```
[문제 있는 구조] - 횡단 관심사 코드 중복
┌────────────────────────────────────────────┐
│  UserController                            │
│    if (!isAuthenticated()) return 401; ◄── 중복!
│    log.info("Request received");       ◄── 중복!
│    // 실제 비즈니스 로직 5줄              │
└────────────────────────────────────────────┘
┌────────────────────────────────────────────┐
│  OrderController                           │
│    if (!isAuthenticated()) return 401; ◄── 중복!
│    log.info("Request received");       ◄── 중복!
│    // 실제 비즈니스 로직 3줄              │
└────────────────────────────────────────────┘
```

Filter와 Interceptor는 이 횡단 관심사를 **파이프라인의 특정 시점에 삽입**함으로써 핵심 로직을 깨끗하게 유지한다.

📢 **섹션 요약 비유**: 공항 보안 검색대(Filter/Interceptor)는 어느 항공사 비행기를 타든 동일하게 통과해야 한다. 각 항공사(Controller)가 자체 보안 검색을 운영할 필요가 없다.

---

## 2. 구성요소

### Filter와 Interceptor의 위치 비교

```
HTTP 요청
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│               서블릿 컨테이너 (Tomcat, Jetty)                  │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                 │
│  │ Filter 1 │──►│ Filter 2 │──►│ Filter 3 │                 │
│  │(인코딩)   │   │(CORS)    │   │(XSS 방어) │                 │
│  └──────────┘   └──────────┘   └──────────┘                 │
│                                      │                       │
│                               ┌──────▼──────────────────┐   │
│                               │  DispatcherServlet       │   │
│                               │   (Spring MVC)           │   │
│                               │                          │   │
│                               │  ┌────────────────────┐  │   │
│                               │  │  Interceptor 1     │  │   │
│                               │  │  (인증/인가)         │  │   │
│                               │  ├────────────────────┤  │   │
│                               │  │  Interceptor 2     │  │   │
│                               │  │  (성능 측정)         │  │   │
│                               │  └────────┬───────────┘  │   │
│                               │           │               │   │
│                               │  ┌────────▼───────────┐  │   │
│                               │  │    Controller       │  │   │
│                               │  └────────────────────┘  │   │
│                               └──────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
HTTP 응답
```

### Interceptor의 3단계 생명주기

Spring HandlerInterceptor는 3개의 메서드로 요청 처리 전/후를 감싼다.

```
┌─────────────────────────────────────────────────────────────┐
│                    요청 처리 흐름                              │
│                                                             │
│  preHandle()       Handler 실행      postHandle()           │
│  ─────────────►  ──────────────►  ─────────────►           │
│  true 반환 시        비즈니스         ModelAndView            │
│  처리 계속           로직 실행         수정 가능               │
│                                                             │
│                                  afterCompletion()          │
│  ◄─────────────────────────────────────────────────────     │
│  응답 완료 후 항상 실행 (예외 발생 시에도)                       │
└─────────────────────────────────────────────────────────────┘
```

| 메서드 | 실행 시점 | 반환값 | 주요 용도 |
|:---|:---|:---|:---|
| `preHandle()` | Controller 실행 전 | boolean (true=계속) | 인증, 인가, 파라미터 검증 |
| `postHandle()` | Controller 실행 후, View 렌더링 전 | void | 모델 데이터 추가, 응답 수정 |
| `afterCompletion()` | View 렌더링 완료 후 | void | 리소스 정리, 성능 로그 기록 |

📢 **섹션 요약 비유**: 인터셉터는 도로 톨게이트(preHandle), 목적지 도착 후 주차 확인(postHandle), 귀가 후 정산(afterCompletion)의 3단계로 여행 전체를 감싸는 서비스다.

---

## 3. 구조 및 동작 원리

### Filter vs Spring Interceptor 비교

| 비교 항목 | Java EE Filter | Spring Interceptor |
|:---|:---|:---|
| **실행 위치** | 서블릿 컨테이너 레벨 | Spring DispatcherServlet 이후 레벨 |
| **스펙** | Servlet Spec (`javax.servlet.Filter`) | Spring Framework (`HandlerInterceptor`) |
| **Spring Bean 접근** | 불가 (컨테이너 레벨) | 가능 (Spring Context 내) |
| **적용 범위** | 모든 요청 (정적 파일 포함) | DispatcherServlet 처리 요청만 |
| **처리 가능 대상** | HttpServletRequest/Response 원본 | Controller 정보, ModelAndView |
| **주요 용도** | 인코딩, CORS, XSS 방어, 압축 | 인증/인가, 로깅, 성능 측정 |
| **설정 방식** | `@WebFilter` 또는 `FilterRegistrationBean` | `WebMvcConfigurer.addInterceptors()` |

### Filter Chain 패턴

```
Filter 체인 처리 흐름:

Request ──► [Filter1] ──► [Filter2] ──► [Filter3] ──► Servlet
                                                           │
Response ◄── [Filter1] ◄── [Filter2] ◄── [Filter3] ◄── 처리
```

각 Filter는 `chain.doFilter(request, response)` 호출로 다음 Filter에 제어를 넘긴다. 호출하지 않으면 요청 처리가 중단된다(예: 인증 실패 시).

📢 **섹션 요약 비유**: Filter는 양파 껍질처럼 겹겹이 쌓여 있다. 안쪽(Servlet)으로 들어갈 때도, 바깥쪽으로 나올 때도 각 껍질(Filter)을 통과한다.

---

## 4. 비교 및 트레이드오프

### Spring Interceptor 구현 예시

```java
// Interceptor 구현
@Component
public class AuthInterceptor implements HandlerInterceptor {

    @Autowired
    private TokenService tokenService; // Spring Bean 주입 가능!

    @Override
    public boolean preHandle(HttpServletRequest request,
                             HttpServletResponse response,
                             Object handler) throws Exception {
        String token = request.getHeader("Authorization");
        if (!tokenService.isValid(token)) {
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED);
            return false; // 처리 중단
        }
        return true; // 계속 진행
    }

    @Override
    public void afterCompletion(HttpServletRequest request,
                                HttpServletResponse response,
                                Object handler, Exception ex) {
        // 성능 측정 로그 기록
        long elapsed = System.currentTimeMillis() - startTime;
        log.info("Request {} took {}ms", request.getRequestURI(), elapsed);
    }
}

// Interceptor 등록
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new AuthInterceptor())
                .addPathPatterns("/api/**")
                .excludePathPatterns("/api/auth/**");
    }
}
```

### 실무 활용 패턴

| 활용 사례 | Filter 또는 Interceptor | 이유 |
|:---|:---|:---|
| 문자 인코딩 (UTF-8) | Filter | Servlet 전 단계에서 처리 필요 |
| CORS 헤더 추가 | Filter | 모든 요청에 적용, Spring 불필요 |
| XSS (Cross-Site Scripting) 방어 | Filter | 요청/응답 스트림 조작 필요 |
| JWT 인증/인가 | Interceptor | Spring Bean(TokenService) 필요 |
| API 성능 로깅 | Interceptor | preHandle/afterCompletion 조합 |
| 요청 압축/압축 해제 | Filter | Servlet 전 단계 처리 |

📢 **섹션 요약 비유**: 건물 입구 보안 게이트(Filter)와 층별 출입 카드 리더기(Interceptor)는 역할이 다르다. 게이트는 건물에 들어오는 모든 사람에게, 카드 리더기는 특정 층(Spring 컨텍스트)의 사람에게만 적용된다.

---

## 5. 실무 적용 및 최적화 기법

### 도입 기대효과

| 기대효과 | 설명 |
|:---|:---|
| **관심사 분리** | 비즈니스 로직이 인증/로깅 코드로 오염되지 않음 |
| **재사용성** | 동일 Interceptor를 여러 URL 패턴에 적용 |
| **유지보수성** | 인증 로직 변경 시 Interceptor 하나만 수정 |
| **OCP 실현** | 새 공통 처리 추가 시 기존 코드 수정 없이 확장 |
| **테스트 독립성** | Interceptor 단독으로 단위 테스트 가능 |

Filter와 Interceptor 패턴은 AOP의 핵심 사상인 **"관심사의 외부화"** 를 HTTP 요청 처리 파이프라인에 적용한 실용적 패턴이다. Spring Security도 내부적으로 Filter Chain으로 구현되어 있어, 이 패턴에 대한 깊은 이해는 실무와 기술사 시험 모두에서 필수적이다.

📢 **섹션 요약 비유**: 배관 시스템에서 정수 필터(Filter)와 수도꼭지 필터(Interceptor)는 다른 위치에서 물을 정화한다. 둘 다 없으면 마실 수 없는 물이 나온다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | AOP (Aspect-Oriented Programming) | 횡단 관심사 분리 패러다임 |
| 상위 개념 | Chain of Responsibility 패턴 | Filter Chain의 이론적 기반 |
| 하위 개념 | Servlet Filter | Java EE 표준 Filter 인터페이스 |
| 하위 개념 | HandlerInterceptor | Spring MVC Interceptor 인터페이스 |
| 연관 개념 | Front Controller 패턴 | DispatcherServlet이 Interceptor를 관리 |
| 연관 개념 | Spring Security | SecurityFilterChain 기반 보안 처리 |
| 연관 개념 | Decorator 패턴 | Filter는 요청/응답을 감싸는 Decorator |

### 👶 어린이를 위한 3줄 비유 설명

- 학교 급식소(Controller)에 들어가기 전에 손 씻기 검사대(Filter)와 배지 확인대(Interceptor)를 통과해야 한다.
- 손 씻기 검사(Filter)는 학교 건물 입구에서 모든 학생에게 공통으로 적용된다.
- 배지 확인(Interceptor)은 급식소 담당 선생님(Spring)이 관리하며, 특정 메뉴를 먹기 전후에도 체크할 수 있다.
