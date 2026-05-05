+++
weight = 171
title = "171. MVC와 복합 디자인 패턴 (MVC Composite Design Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: MVC (Model-View-Controller, 모델-뷰-컨트롤러)는 단일 패턴이 아니라 옵저버(Observer), 전략(Strategy), 컴포지트(Composite) 등 다수 GoF (Gang of Four) 패턴의 융합체(Composite Pattern)다.
> 2. **가치**: 관심사 분리(SoC, Separation of Concerns)를 통해 UI, 비즈니스 로직, 흐름 제어를 독립적으로 변경 가능하게 하여 유지보수성과 테스트 용이성을 높인다.
> 3. **판단 포인트**: MVC 변형(MVP, MVVM 등) 선택 시 "Model과 View 사이 결합 방향"과 "테스트 환경"을 기준으로 판단하라.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### GUI 애플리케이션의 역사적 문제

초기 GUI 프로그램은 UI 코드와 비즈니스 로직이 한 파일에 뒤섞여 있었다. 버튼 클릭 이벤트 핸들러 안에 DB 쿼리가 직접 있는 구조다. 이렇게 되면:

- UI 변경 시 비즈니스 로직도 함께 수정해야 한다.
- 단위 테스트(Unit Test) 시 UI를 켜야 하므로 자동화가 어렵다.
- 개발자-디자이너 간 병렬 작업이 불가능하다.

**MVC 패턴**은 이 문제를 세 역할로 책임을 분리하여 해결한다.

### MVC 세 역할의 책임

| 구성요소 | 영문 | 책임 |
|:---|:---|:---|
| **Model** | Model | 데이터와 비즈니스 로직 보유. View/Controller 독립. 상태 변경 시 Observer 통지 |
| **View** | View | 사용자 인터페이스(UI) 표현. Model 상태를 시각화. 사용자 입력 수신 |
| **Controller** | Controller | 사용자 입력 처리. Model 업데이트 지시. 어떤 View를 보여줄지 결정 |

📢 **섹션 요약 비유**: 식당에서 주방(Model)은 음식을 만들고, 홀 직원(Controller)은 주문을 받아 주방에 전달하며, 메뉴판과 음식 진열대(View)는 손님에게 무엇이 있는지 보여준다.

---

## 2. 구성요소

### MVC 흐름도와 내장된 GoF 패턴

```
사용자 입력
     │
     ▼
┌────────────────────────────────────────────────────────────────┐
│  View  (Composite 패턴: 중첩 컴포넌트 트리)                     │
│                                                                │
│  ┌──────────┐  ┌────────────────────────────────────────────┐ │
│  │ Button   │  │  Panel                                     │ │
│  └──────────┘  │  ┌───────────┐  ┌───────────────────────┐ │ │
│                │  │ TextField │  │  TableView             │ │ │
│                │  └───────────┘  └───────────────────────┘ │ │
│                └────────────────────────────────────────────┘ │
└───────────────────────┬──────────────────────────────────────┘
                        │ 이벤트 전달 (Strategy 패턴으로 교체 가능)
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  Controller  (Strategy 패턴: 요청 처리 전략 교체 가능)          │
│                                                               │
│  handleInput() → validate() → updateModel()                   │
└───────────────────────┬───────────────────────────────────────┘
                        │ Model 상태 변경
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  Model  (Observer 패턴 Subject 역할)                          │
│                                                               │
│  state: { data }                                              │
│  notifyObservers() → registered Views에게 Push/Pull 통지      │
└───────────────────────┬───────────────────────────────────────┘
                        │ 상태 변경 통지
                        ▼
                     View 업데이트
```

### 내장된 GoF 패턴 상세

**옵저버(Observer) 패턴**: Model이 Subject, View들이 Observer. Model 상태가 변하면 등록된 View 전체에 통지. Pull 방식(View가 Model 조회)과 Push 방식(Model이 변경 데이터 전달) 두 가지.

**전략(Strategy) 패턴**: Controller는 인터페이스로 추상화되어 런타임에 교체 가능. View는 다양한 Controller 전략을 사용할 수 있어 테스트용 MockController 주입 가능.

**컴포지트(Composite) 패턴**: View는 버튼, 레이블, 패널 등 컴포넌트가 트리 구조로 중첩. 단일 컴포넌트와 복합 컴포넌트를 동일 인터페이스(`Component.render()`)로 처리.

📢 **섹션 요약 비유**: MVC는 오케스트라다. 지휘자(Controller)가 음악 흐름을 제어하고, 악보(Model)가 음표를 보유하며, 악기 연주(View)가 관객에게 음악을 전달한다. 각 악기(Composite)는 개별 또는 섹션으로 묶여 동일한 방식으로 지휘된다.

---

## 3. 구조 및 동작 원리

### MVC 변형 패턴 비교

| 패턴 | 구성 | Model-View 결합 | 테스트 용이성 | 주 사용처 |
|:---|:---|:---|:---|:---|
| **MVC** | Model / View / Controller | View가 Model 직접 관찰(Observer) | 중간 (View UI 의존) | 서버사이드(Spring MVC), 전통 GUI |
| **MVP** (Model-View-Presenter) | Model / View / Presenter | View-Presenter 1:1 인터페이스 | 높음 (View 인터페이스로 목 가능) | Android, WinForms |
| **MVVM** (Model-View-ViewModel) | Model / View / ViewModel | 데이터 바인딩(Data Binding) 자동 동기화 | 높음 (ViewModel 단독 테스트) | WPF, Vue.js, Angular |
| **VIPER** (View-Interactor-Presenter-Entity-Router) | 5개 계층 | 단방향 의존 | 매우 높음 (각 계층 독립) | iOS 대규모 앱 |

### 프론트엔드 프레임워크 매핑

| 프레임워크 | 기반 패턴 | 데이터 흐름 | 특이사항 |
|:---|:---|:---|:---|
| React | 단방향 데이터 흐름 (Flux) | 부모 → 자식 (단방향) | 상태(State)가 Model 역할, 컴포넌트가 View |
| Angular | MVVM | 양방향 바인딩(Two-way Binding) | `[(ngModel)]`로 ViewModel ↔ View 자동 동기화 |
| Vue.js | MVVM 영향 | 반응형(Reactive) 시스템 | `data`가 ViewModel, 템플릿이 View |

📢 **섹션 요약 비유**: MVC는 기본형 자동차, MVP는 운전자와 차가 인터폰으로 소통하는 리무진, MVVM은 자율주행차(바인딩으로 자동 반응)다.

---

## 4. 비교 및 트레이드오프

### Spring MVC 구조 매핑

```
HTTP 요청
     │
     ▼
┌─────────────────────────────────────────────────────┐
│  DispatcherServlet (Front Controller 패턴)          │
│   → HandlerMapping  (어떤 Controller?)               │
│   → HandlerAdapter  (어떻게 호출?)                   │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
              @Controller (Controller)
                   │         │
            Model 조회    View 이름 반환
                   ↓
              Service → Repository → DB (Model 계층)
                                         │
                                         ▼
                              ViewResolver → Template (View)
```

### 기술사 논술 포인트

기술사 실무 문제에서 MVC를 다룰 때 다음 관점에서 분석하면 높은 점수를 받을 수 있다:

1. **패턴 복합성 인식**: "MVC는 단순한 3-tier 분리가 아니라 GoF 패턴들의 융합체"임을 명시.
2. **변형 선택 근거**: 팀 규모, 테스트 전략, 플랫폼(Web/Mobile/Desktop)에 따른 MVP·MVVM 선택 이유 제시.
3. **결합도(Coupling) 분석**: Model-View 결합 방향이 테스트 가능성과 직결됨을 설명.
4. **현대 프레임워크 연결**: React Flux, Vue.js 반응성 시스템을 MVC 맥락에서 해석.

| 선택 기준 | 권장 패턴 |
|:---|:---|
| 서버사이드 렌더링, 팀 규모 소형 | MVC (Spring MVC) |
| 안드로이드 Unit Test 중요 | MVP |
| 양방향 UI 바인딩, 대형 SPA | MVVM (Angular, Vue) |
| iOS 대규모 모듈 분리 | VIPER |

📢 **섹션 요약 비유**: 기술사는 "어떤 MVC 변형을 왜 골랐냐"는 질문에 "테스트 전략과 팀 구조"를 기준으로 답해야 한다. 도구가 아니라 맥락이 답을 결정한다.

---

## 5. 실무 적용 및 최적화 기법

MVC 및 변형 패턴 적용의 기대효과:

- **관심사 분리**: UI 변경이 비즈니스 로직에 영향 없음 → 병렬 개발 가능.
- **단위 테스트 가능성**: Model과 Controller를 UI 없이 독립 테스트.
- **재사용성**: 동일 Model을 Web, API, CLI 다양한 View와 조합 가능.
- **유지보수성**: 변경 범위가 명확히 계층에 국한됨.

MVC의 진정한 가치는 "3개 클래스로 코드를 나누는 것"이 아니라, **"어떤 변화가 어떤 범위에만 영향을 주도록 설계할 것인가"** 라는 변경의 지역화(Locality of Change)에 있다. GoF 패턴들의 융합체라는 관점으로 MVC를 이해해야 실무 설계에서 올바른 판단이 가능하다.

📢 **섹션 요약 비유**: MVC는 레고 세트처럼 Model·View·Controller 블록이 독립적으로 교체 가능하다. 성 테마 벽(View)을 우주 테마 벽으로 바꿔도 성안 구조(Model)는 그대로다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Architectural Pattern (아키텍처 패턴) | GoF 디자인 패턴보다 상위 수준의 구조 패턴 |
| 하위 개념 | Observer Pattern (옵저버 패턴) | Model → View 상태 통지 구현 |
| 하위 개념 | Strategy Pattern (전략 패턴) | Controller 교체 가능성 구현 |
| 하위 개념 | Composite Pattern (컴포지트 패턴) | View 위젯 트리 구조 구현 |
| 연관 개념 | SoC (Separation of Concerns, 관심사 분리) | MVC의 핵심 설계 원칙 |
| 연관 개념 | MVP (Model-View-Presenter) | View 인터페이스화로 테스트성 강화 |
| 연관 개념 | MVVM (Model-View-ViewModel) | 데이터 바인딩 기반 자동 동기화 |
| 연관 개념 | Front Controller Pattern (프론트 컨트롤러) | Spring DispatcherServlet, 단일 진입점 |

---

### 👶 어린이를 위한 3줄 비유 설명

- 놀이공원에서 안내원(Controller)이 표를 받고, 어떤 놀이기구(View)로 갈지 알려줘요. 놀이기구 자체(View)는 사람을 태우는 것만 해요.
- 놀이공원 운영 규칙(Model)은 어떤 놀이기구가 몇 살 이상 탈 수 있는지 정해요. 안내원이 바뀌어도 규칙은 변하지 않아요.
- 서로 맡은 역할이 달라서, 놀이기구 색을 바꿔도(View 변경) 운영 규칙(Model)은 건드릴 필요가 없어요.
