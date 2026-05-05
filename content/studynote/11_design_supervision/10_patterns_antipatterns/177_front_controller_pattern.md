+++
weight = 177
title = "177. 프론트 컨트롤러 패턴 (Front Controller Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 프론트 컨트롤러 (Front Controller) 패턴은 모든 HTTP 요청을 단일 진입점이 받아서 공통 처리(인증, 로깅, 세션) 후 적절한 핸들러로 라우팅하는 구조다.
> 2. **가치**: 공통 로직의 중복 제거와 요청 처리 흐름의 일관성 보장이 핵심이며, Spring MVC의 DispatcherServlet이 이 패턴의 대표 구현체다.
> 3. **판단 포인트**: 웹 애플리케이션에서 인증/인가, 로깅, 예외 처리 등 횡단 관심사를 한 곳에서 관리해야 할 때 프론트 컨트롤러 패턴이 최적 해결책이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 패턴 등장 배경

초기 서블릿 기반 웹 개발에서는 각 URL마다 별도의 서블릿을 작성했다. 예를 들어 `LoginServlet`, `OrderServlet`, `UserServlet`이 각각 존재하면 다음 문제가 발생한다.

- **코드 중복**: 세션 확인, 로깅, 한글 인코딩 설정이 모든 서블릿에 반복된다.
- **인증 취약점**: 한 서블릿에서 인증 체크를 빠뜨리면 보안 허점이 생긴다.
- **변경 비용 증가**: 공통 처리 방식을 변경하면 모든 서블릿을 수정해야 한다.

프론트 컨트롤러 (Front Controller) 패턴은 **"단일 진입점(Single Entry Point)"** 원칙으로 이 문제를 해결한다.

### 핵심 아이디어

모든 요청을 하나의 컨트롤러가 받아서 처리하되, 실제 비즈니스 처리는 개별 핸들러(Command 객체)에게 위임한다.

```
모든 요청 →  [Front Controller]  → 라우팅 → [개별 핸들러 A]
                     │                   → [개별 핸들러 B]
                     │                   → [개별 핸들러 C]
              공통 처리 수행
              (인증, 로깅, 인코딩)
```

📢 **섹션 요약 비유**: 아파트 경비실(Front Controller)이 모든 방문자를 확인한 후 해당 세대(개별 핸들러)로 안내한다. 세대마다 자체 경비를 두지 않아도 된다.

---

## 2. 구성요소

### Spring MVC DispatcherServlet 처리 흐름

Spring MVC는 프론트 컨트롤러 패턴의 가장 완성도 높은 구현체다.

```
HTTP 요청
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│                   DispatcherServlet                       │
│                  (Front Controller)                       │
│                                                           │
│  1. HandlerMapping 조회 → 어떤 Controller를 쓸까?          │
│  2. HandlerAdapter 조회 → Controller를 어떻게 실행할까?    │
│  3. 실행 → ModelAndView 반환                               │
│  4. ViewResolver 조회 → 어떤 View 템플릿을 쓸까?           │
│  5. View 렌더링                                            │
└──────────────────────────────────────────────────────────┘
    │
    │  HandlerMapping      HandlerAdapter     ViewResolver
    │  (URL → Handler)     (Handler 실행)     (View 이름 → 파일)
    │
    ▼
HTTP 응답
```

### 구성 요소 상세

| 구성 요소 | 역할 | Spring 구현체 예시 |
|:---|:---|:---|
| Front Controller | 단일 진입점, 공통 처리 | `DispatcherServlet` |
| Handler Mapping | URL → 핸들러 매핑 | `RequestMappingHandlerMapping` |
| Handler Adapter | 핸들러 실행 방법 결정 | `RequestMappingHandlerAdapter` |
| Handler (Controller) | 실제 비즈니스 처리 | `@Controller` 클래스 |
| View Resolver | 뷰 이름 → 실제 파일 경로 | `InternalResourceViewResolver` |
| View | 응답 렌더링 | Thymeleaf, JSP |

### 시퀀스 다이어그램

```
Client    DispatcherServlet    HandlerMapping    Controller    ViewResolver    View
  │              │                   │               │              │           │
  │──요청────────►│                   │               │              │           │
  │              │──핸들러 조회────────►│               │              │           │
  │              │◄──핸들러 반환───────│               │              │           │
  │              │──handle()──────────────────────────►│              │           │
  │              │◄──ModelAndView─────────────────────│              │           │
  │              │──뷰 이름 조회───────────────────────────────────────►│           │
  │              │◄──View 반환────────────────────────────────────────│           │
  │              │──render()──────────────────────────────────────────────────────►│
  │◄─응답─────────────────────────────────────────────────────────────────────────│
```

📢 **섹션 요약 비유**: DispatcherServlet은 오케스트라 지휘자다. 바이올린(Controller), 피아노(ViewResolver), 첼로(HandlerMapping)가 각자 연주하지만 지휘자 없이는 화음이 나오지 않는다.

---

## 3. 구조 및 동작 원리

### Front Controller vs Page Controller 비교

| 비교 항목 | Front Controller | Page Controller |
|:---|:---|:---|
| **진입점** | 단일 진입점 (DispatcherServlet) | 페이지마다 별도 컨트롤러 |
| **공통 처리** | 한 곳에서 집중 처리 | 각 컨트롤러에서 중복 처리 |
| **URL 라우팅** | HandlerMapping이 중앙 집중 관리 | URL-클래스 1:1 매핑 |
| **유지보수** | 공통 로직 변경 시 한 곳만 수정 | 모든 페이지 컨트롤러 수정 필요 |
| **복잡도** | 초기 설정 복잡, 장기적으로 유리 | 단순, 규모 증가 시 관리 어려움 |
| **대표 프레임워크** | Spring MVC, Struts | 초기 JSP/Servlet 방식 |

### Front Controller 관련 패턴 비교

| 패턴 | 관계 | 역할 |
|:---|:---|:---|
| Front Controller | 기반 패턴 | 단일 진입점 + 라우팅 |
| Interceptor/Filter | 협력 패턴 | 공통 처리를 체인으로 분리 |
| Command | 협력 패턴 | 개별 요청 처리를 객체로 캡슐화 |
| Composite View | 협력 패턴 | 레이아웃 재사용 |

📢 **섹션 요약 비유**: Front Controller는 공항 수속 카운터, Page Controller는 항공사마다 별도 건물이다. 공항 수속 카운터에서 모든 승객을 처리한 후 각 게이트(Handler)로 보낸다.

---

## 4. 비교 및 트레이드오프

### Spring Boot에서의 DispatcherServlet 설정

Spring Boot는 자동 설정으로 `DispatcherServlet`을 `/` 경로에 등록한다.

```java
// Spring Boot 자동 설정 (별도 web.xml 불필요)
// application.properties
spring.mvc.servlet.path=/api

// Controller 예시
@RestController
@RequestMapping("/users")
public class UserController {
    @GetMapping("/{id}")
    public UserDto getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}
```

### HandlerMapping 우선순위

```
요청 URL 매핑 시 우선순위:
1. RequestMappingHandlerMapping (@RequestMapping 어노테이션)
2. BeanNameUrlHandlerMapping    (빈 이름 기반 매핑)
3. SimpleUrlHandlerMapping      (직접 URL 패턴 설정)
```

### 기술사 시험 판단 포인트

| 질문 | 핵심 답변 |
|:---|:---|
| Front Controller의 단점은? | 단일 컨트롤러 병목 가능성, 설정 복잡성 증가 |
| DispatcherServlet 스레드 안전성? | 무상태(Stateless) 설계로 멀티스레드 안전 |
| 필터(Filter)와의 차이? | Filter는 서블릿 컨테이너 레벨, DispatcherServlet은 Spring 레벨 |
| 예외 처리는? | `@ExceptionHandler`, `HandlerExceptionResolver`로 중앙 처리 |

📢 **섹션 요약 비유**: 콜센터 대표 번호(Front Controller)에 전화하면 자동 응답(HandlerMapping)이 "영업 부서면 1번, 기술 지원이면 2번"으로 안내한다. 부서(Controller)마다 별도 번호를 외울 필요가 없다.

---

## 5. 실무 적용 및 최적화 기법

### Front Controller 도입 기대효과

| 기대효과 | 구체적 내용 |
|:---|:---|
| **공통 로직 중앙화** | 인증, 로깅, CORS, 인코딩 설정을 한 곳에서 관리 |
| **보안 강화** | 모든 요청이 보안 검사를 반드시 통과 |
| **개발 생산성** | 핸들러 개발자는 비즈니스 로직만 집중 |
| **일관된 에러 처리** | 예외 처리를 중앙 집중화 |
| **테스트 용이성** | Mock HandlerMapping으로 라우팅 테스트 가능 |

프론트 컨트롤러 패턴은 현대 웹 프레임워크의 사실상 표준 아키텍처가 되었다. Spring MVC, Django, Laravel, Ruby on Rails 모두 이 패턴을 기반으로 구축되어 있다. 핵심은 **"공통 관심사를 집중화하되, 개별 처리는 위임"** 이라는 단순하지만 강력한 원칙이다.

📢 **섹션 요약 비유**: 좋은 회사에는 모든 직원이 지켜야 할 취업 규칙(공통 처리)이 있고, 각 팀은 자신의 업무(비즈니스 로직)에 집중한다. Front Controller는 취업 규칙을 자동으로 적용하는 인사부다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | MVC 패턴 | Model-View-Controller 아키텍처 패턴 |
| 상위 개념 | Single Entry Point | 단일 진입점 설계 원칙 |
| 하위 개념 | DispatcherServlet | Spring MVC의 Front Controller 구현체 |
| 하위 개념 | HandlerMapping | URL과 핸들러를 연결하는 전략 객체 |
| 연관 개념 | Interceptor 패턴 | Front Controller 전/후 횡단 처리 |
| 연관 개념 | Command 패턴 | 개별 요청을 객체로 캡슐화 |
| 연관 개념 | Strategy 패턴 | HandlerAdapter에서 실행 전략 선택 |

### 👶 어린이를 위한 3줄 비유 설명

- 학교 정문(Front Controller)에서 모든 학생의 출석 체크와 복장 검사를 한 번에 한다.
- 검사가 끝나면 학생들은 각자 교실(개별 Controller)로 이동해서 공부한다.
- 정문이 없다면 각 교실마다 선생님이 출입구를 지키며 출석 체크를 해야 한다 — 엄청난 낭비다.
