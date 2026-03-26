+++
title = "MVC 아키텍처"
description = "MVC 아키텍처 패턴의 개념과 실무 적용"
date = 2024-01-17
weight = 604

[taxonomies]
subjects = ["software-engineering"]
authors = ["brainscience"]
+++

# MVC 아키텍처 (Model-View-Controller Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MVC 아키텍처는 사용자 인터페이스를 분리하여 Model의 데이터, View의 표현, Controller의 입력 처력을 각각 독립적으로 관리하는 소프트웨어 설계 패턴이다.
> 2. **가치**: 1979년 Trygve Reenskaug가 Smalltalk-80을 위해 고안한 이 패턴은 UI 변경이 로직에 영향을 미치지 않도록 하고, 다중 View가 동일한 Model을 동시에 사용할 수 있게 하여 개발 생산성과 유지보수성을 크게 향상시켰다.
> 3. **융합**: 현대 웹 개발에서 React, Angular, Vue.js 등의 프레임워크가 MVC/MVP/MVVM 패턴을 변형하여 적용하고 있으며, SPA (Single Page Application)에서는 ViewModel이 View와 양방향 데이터 바인딩을 담당한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: MVC 아키텍처는 애플리케이션을 Model(데이터 및 비즈니스 로직), View(사용자 인터페이스 표현), Controller(사용자 입력 처리 및 Model-View 조정)의 세 가지 핵심 구성 요소로 분리하는 소프트웨어 설계 패턴이다. 각 구성 요소는各自的 관심사를 캡슐화하며, Observer 패턴(모델의 변경 사항이 등록된 View에 자동通知)을 통해 Model과 View의 결합도를 낮춘다.

- **필요성**: GUI(Graphic User Interface) 애플리케이션에서 사용자의 입력 처리, 데이터 관리, 화면 표시라는 세 가지 다른性质의 작업이 혼합되면, UI 변경(예: 버튼 스타일 변경)이 business logic 수정으로 이어지고, 새로운 데이터 소스 추가가 화면 표시 코드를 변경해야 하는 상황이 발생한다. MVC는 이러한 "동기적 변경의 파급"을 막기 위해, 각 작업을 독립적인 구성 요소로 분리하여 상호작용을 구조화한다.

- **💡 비유**: MVC는 **식당에서 주방(View), 웨이터(Controller), 주방장(Model)의 관계**와 같다. 고객이 주문(입력)을 하면 웨이터가 주방에 전달하고, 주방이 요리를 완성하면 웨이터가 고객에게 서빙한다. 고객이 디저트로 뭘 먹을지 몰라도(주厨의 내부 동작 모름) 웨이터와의 interaction으로 식사를顺利完成할 수 있다.

- **등장 배경 및 발전 과정**:
  1. **1979년 MVC의 탄생**: Xerox PARC의 Trygve Reenskaug가 Smalltalk-80을 위한 GUI 설계 패턴으로 MVC를 고안했다. 당시에는 그래픽 인터페이스의 복잡성이 증가하기 시작했고, 데이터, 표현, 제어를 분리하려는 요구가 있었다.

  Smalltalk-80의 MVC 구조를 시각화하면 다음과 같다.

  ```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │              Smalltalk-80 MVC 구조 (1979년 원형)                     │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │       ┌──────────┐           ┌──────────┐                         │
  │       │   View   │◀──notify──│  Model   │                         │
  │       │  (화면)  │           │  (데이터) │                         │
  │       └────┬─────┘           └────┬─────┘                         │
  │            │                      │                                │
  │            │         update       │                                │
  │            │◀─────────────────────┘                                │
  │            │                                                        │
  │            │ user action                                             │
  │            ▼                                                        │
  │       ┌──────────┐                                                  │
  │       │Controller│                                                  │
  │       │ (입력처리) │                                                  │
  │       └──────────┘                                                  │
  │                                                                     │
  │  핵심 개념:                                                         │
  │  - Model은 View와 Controller를 모르지만, Observer 패턴으로 View에   │
  │    변경 사항을通知할 수 있음                                         │
  │  - View는 Model을 구독하며, Controller는 Model을 조작                │
  │  - Controller는 사용자 입력을 해석하여 Model 또는 View를 업데이트    │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
  ```

  **[다이어그램 해설]** MVC의 혁신은 Observer 패턴을 통해 Model과 View 사이의 강한 결합을 느슨한 구독 관계로 전환한 점이다. Model의 데이터가 변경되면 Model이 등록된 모든 View에通知하고, View는 자신의 표시만 업데이트한다. Controller는 Model을 조작하거나 View를 선택하는 작업을 담당한다. 이 구조에서 새로운 View 추가(예: 같은 데이터를 표 형태로也表示)는 Model을 모르지 않아도 되며, Observer 목록에 등록하는 것만으로 구현 가능하다. 40년 지난 현재까지도 이 기본 아이디어는 현대 프론트엔드 프레임워크(React, Vue)의 상태 관리 철학으로 이어지고 있다.

  2. **1990년대 웹 MVC의 등장**: CGI (Common Gateway Interface)와 Perl/C를 사용한 초기 웹에서, 서버 사이드 MVC(Controller: 스크립트, Model: 데이터베이스, View: HTML 템플릿)가 등장했다.

  3. **2000년대 서버 사이드 MVC 프레임워크**: Java의 Struts, Spring MVC, Ruby on Rails, Django, ASP.NET MVC 등이服务器 사이드 MVC를 표준으로 자리잡았다.

  4. **2010년대 클라이언트 사이드 MVC/MVVM**: AngularJS(Angular), Backbone.js, Ember.js, Knockout.js 등이 클라이언트 사이드에서 MVC/MVVM을 구현했다.

- **📢 섹션 요약 비유**: 영화관에서 티켓 예매할 때, 매표소 직원(Controller)이 영화 정보 시스템(Model)에 확인을 요청하고, 결과는 티켓 종이(View)로 출력되는 과정과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Model** | 데이터 및 비즈니스 로직 | 상태 관리, 비즈니스 규칙 적용, 변경 notifications | Domain Object, Service Layer, Repository | 영화 데이터베이스 |
| **View** | UI 표현 및 사용자 시각反馈 | Model 데이터 렌더링, 사용자 이벤트 생성 | JSP, Thymeleaf, React, Vue, HTML/CSS | 영화 티켓 |
| **Controller** | 입력 처리 및 흐름 제어 | 사용자 요청 수신, Model 호출, View 선택 | Servlet, DispatcherServlet, Route Handler | 매표소 직원 |
| **ViewModel** | View를 위한 데이터 준비 | View에 필요한 데이터 변환, 양방향 바인딩 (MVVM) | Knockout.js observables, Vue reactive data | 티켓 정보 정리 담당 |

---

### 현대 웹 MVC 동작 흐름

전형적인 서버 사이드 MVC 웹 애플리케이션에서 HTTP 요청이 처리되는 과정을 시각화하면 다음과 같다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                  서버 사이드 MVC 요청 처리 흐름                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [브라우저]                                                         │
│      │                                                             │
│      │ 1. HTTP 요청 (GET /orders/123)                              │
│      ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    DispatcherServlet                        │   │
│  │              (Front Controller 역할)                        │   │
│  └──────────────────────────┬────────────────────────────────┘   │
│                             │                                        │
│                             │ 2. Handler Mapping                    │
│                             │    (URL → Controller 매핑)             │
│                             ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Controller: OrderController              │   │
│  │                                                             │   │
│  │  @GetMapping("/orders/{orderId}")                          │   │
│  │  public String getOrder(@PathVariable orderId, Model m) {  │   │
│  │      Order order = orderService.findById(orderId);        │   │
│  │      m.addAttribute("order", order);  // 3. Model에 데이터  │   │
│  │      return "orderDetail";  // 4. View 이름 반환             │   │
│  │  }                                                         │   │
│  └──────────────────────────┬────────────────────────────────┘   │
│                             │                                        │
│                             │ 5. View 이름                           │
│                             ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      View Resolver                          │   │
│  │           (View 이름 → 실제 View 파일 매핑)                   │   │
│  └──────────────────────────┬────────────────────────────────┘   │
│                             │                                        │
│                             │ 6. View 파일 (orderDetail.jsp)        │
│                             ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   View: JSP/Thymeleaf                        │   │
│  │                                                             │   │
│  │  <h1>주문번호: ${order.orderId}</h1>                       │   │
│  │  <p>고객: ${order.customerName}</p>                        │   │
│  │  <p>금액: ${order.totalPrice}</p>                          │   │
│  │                                                             │   │
│  └──────────────────────────┬────────────────────────────────┘   │
│                             │                                        │
│                             │ 7. 렌더링된 HTML                       │
│                             ▼                                        │
│                       [브라우저로 응답]                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 서버 사이드 MVC의 핵심은 Front Controller 패턴이다. 모든 HTTP 요청이 먼저 DispatcherServlet(Front Controller)에 집중되고, 이는 URL을 분석하여 적절한 Handler(Controller)에 위임한다. 이 구조의 장점은 인증, 로깅, 국제화 같은 공통 작업을 Front Controller 단에서 일괄 처리할 수 있다는 점이다. Controller는 비즈니스 로직 수행을 Service에 위임하고, 결과를 Model에 담아 View 이름과 함께 반환한다. ViewResolver는 반환된 View 이름을 실제 View 파일(JSP, Thymeleaf, FreeMarker 등)에 매핑하고, View는 Model의 데이터를 읽어 HTML을 생성한다. 각 단계가 명확히 분리되어 있어 테스트 가능한 구조이며, View 기술만 교체하는 것이 가능하다.

---

### MVP vs MVC vs MVVM 비교

MVC 이후에 등장한 MVP(Model-View-Presenter)와 MVVM(Model-View-ViewModel)은 각각의 변형으로, 결합도와 테스트 용이성에서 차이를 보인다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    MVC vs MVP vs MVVM 비교                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [MVC]                         [MVP]                          [MVVM]│
│                                                                     │
│  ┌────────┐    ┌────────┐      ┌────────┐    ┌────────┐     ┌────────┐│
│  │  View │◀───│Model │──────▶│ Presenter│◀───│  View │     │  View  ││
│  └───────┘    └────────┘      └────────┘    └────────┘     └────┬───┘│
│       │                            │                            │     │
│       │    사용자 조작              │    View 조작                │     │
│       ▼                            ▼                            ▼     │
│  ┌────────┐                  ┌────────┐                   ┌────────┐│
│  │Control│                  │  View  │                   │ViewModel││
│  │ ler   │                  │  ler   │                   │(양방향 ││
│  └───────┘                  └────────┘                   │바인딩) ││
│                                                            └────────┘│
│       │                            │                            │     │
│       │ Model 직접 업데이트          │ Presenter가 View 업데이트 │     │ Model │
│       │ View는 Model 구독            │ View는 수동 업데이트     │     │바인딩 │
│                                                                     │
│ 耦合도: 중간               결합도: 낮음 (View-Presenter 1:1)    결합도: 가장 낮음│
│  View ↔ Model: 직접 통신   View ↔ Model: 불가                   양방향 데이터 │
│  용도: 데스크톱/웹         용도: 안드로이드 MVP           바인딩 │
│                          용도: SPA, Vue, WPF/XAML     │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** MVC에서 View는 Model의 변경을 직접 관찰(Observer 패턴)하므로 View와 Model 사이의耦合이 완전히 제거되지 않는다. MVP에서는 Presenter가 View와 Model 사이의 완전한 중개자 역할을 하며, View는 Presenter에게 사용자 입력을 전달하고, Presenter가 View의 표시를 직접 업데이트한다. 이 구조에서 View는 완전히 수동적(Passive)이며, Mock View를 만들어 Presenter를 독립적으로 테스트할 수 있다. MVVM은 데이터 바인딩(Data Binding) 기술과 함께 사용되며, ViewModel이 View의 상태를 자동으로 동기화한다. WPF(Windows Presentation Foundation), Xamarin, Vue.js, Angular.js에서 이 패턴이 널리 사용되며, 특히 반응형 UI 구현에 적합하다.

- **📢 섹션 요약 비유**: MVC는 **호텔 컨시어지와 같아서**, 고객(View)의 요청을 받아 데이터 시스템(Model)에 확인을 요청하고, 결과를 고객에게 전달하는 역할을 합니다. MVP는 **완전히训练된 침구 대행 서비스원**처럼 모든 것을 직접 조율하며, MVVM은 **스마트홈 시스템**처럼 사용자의 조작 없이 자동으로 조명이 켜지고窗帘이 조절되는 것처럼 양방향 동기화가 이루어집니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: 전통적 MVC vs RESTful MVC vs 단일 페이지 애플리케이션 (SPA)

| 비교 항목 | 전통적 MVC (서버 사이드 렌더링) | RESTful MVC + AJAX | SPA (React/Vue/Angular) |
|:---|:---|:---|:---|
| **렌더링 위치** | 서버 (JSP, Thymeleaf) | 서버 (JSON) + 클라이언트 (DOM 조작) | 클라이언트 (JavaScript) |
| **네트워크** | 매 요청마다 전체 페이지Reload | 필요한 데이터만 AJAX | 초기 로드 후 API 통신 |
| **상태 관리** | 세션/서버 사이드 | REST API 상태 | 클라이언트 사이드 상태 |
| **반응성** | 낮음 (페이지Reload) | 중간 (부분 업데이트) | 높음 (실시간 반응) |
| **초기 로드** | 빠름 | 보통 | 느림 (첫 로드) |
| **SEO** | 우수 | 보통 | 어려움 (SSR 필요) |

- **📢 섹션 요약 비유**: MVC는 **전통적인 식당**처럼 손님이 주문하면 주방에서 전체 요리를 완성해서 내리고, RESTful AJAX는 **맘카페 키오스크**처럼 주문만 서버에 전달하고菜肴은 이미テーブルに客户提供하며, SPA는 **맛집 앱**처럼 앱이 설치되어 있으면 서버와 필요한 데이터만 주고받아即석에서 화면을 바꿉니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 쇼핑몰 상품 목록 페이지**: 사용자가 카테고리 필터를 선택하면 상품 목록이 갱신되는 기능. 전통적 MVC에서는 필터 선택 → 서버에 새 요청 → 전체 페이지Reload → 상품 목록 갱신이 발생한다. AJAX+MVC 조합에서는 필터 선택 → REST API 호출 → JSON 응답 수신 → JavaScript가 DOM만 갱신하여 부분 업데이트가 가능하고, SPA 구조에서는 필터 선택 → ViewModel의 데이터가 변경 → 데이터 바인딩이 자동으로 View를 갱신한다.

### 도입 체크리스트
- **기술적**: UI 변경 빈도는 높은가? 실시간 반응성이 요구되는가?
- **운영·보안적**: SEO가 중요한가? 초기 로드 성능이 중요한가?

### 안티패턴
- **Massive View Controller**: Controller가 너무 많은 역할을 가져 코드가 비대해지는 안티패턴으로, Service/UseCase Layer 도입으로 분리해야 한다.
- **Fat Model, Skinny Controller**: 반대로 모든 business logic을 Model에 넣어서 Model이 비대해지는 안티패턴으로, Domain Service Layer 도입이 필요하다.

- **📢 섹션 요약 비유**: Controller가 **요리사**가 되어서 재료를 사고(DAO), 요리하고(View까지 그리는) 모든 것을 처리하면 분화선처럼 느껴질 것입니다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망
- ** Islands Architecture**: 전체 SPA 대신 필요한 부분만 클라이언트 사이드에서 렌더링하고, 나머지는 서버 사이드 렌더링으로 유지하는 hybrid 접근법이 주목받고 있다. 이는 MPA(Multi-Page Application)의シンプルさと SPA의 반응성을 결합한다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Observer 패턴** | Model의 변경을 View에自動的に通知하는 MVC의 핵심 메커니즘이다. |
| **Front Controller 패턴** | 모든 요청을 단일 진입점에서 처리하여 공통 기능을 집중시키는 패턴이다. |
| **MVP (Model-View-Presenter)** | MVC의 변형으로, View와 Model의 결합도를 더 낮춘 패턴이다. |
| **MVVM (Model-View-ViewModel)** | 데이터 바인딩을 통해 View와 ViewModel이 자동 동기화되는 패턴이다. |
| **Flux/Redux 패턴** | React 기반 SPA에서 상태 관리와 데이터 흐름을 관리하는 아키텍처 패턴이다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. MVC는 **음식점**과 같아요. 손님은 View(화면)만 보고, 웨이터는 Controller(요청 전달) 역할을 하며, 주방장은 Model(재료와 레시피)을 관리해요.
2. 손님이 뭔가 시키면(View 조작), 웨이터가 주방에 알려주고(Controller), 주방에서 음식을 만들어(Model) 다시 웨이터가 손님에게 가져다줘요.
3. 그래서 손님이 메뉴판을 바꿔도(View 변경) 주방의 레시피(Model)는 그대로이고, 주방에서 재료가 없어도(데이터 없음) 메뉴판은 여전히 예쁘게 보일 수 있어요!
