+++
title = "MVC, MVP, MVVM 패턴"
description = "MVC, MVP, MVVM Patterns"
category = "4_software_engineering"
+++

# MVC, MVP, MVVM 패턴

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MVC (Model-View-Controller), MVP (Model-View-Presenter), MVVM (Model-View-ViewModel)은 UI 기반 애플리케이션에서 Business Logic과 UI를 분리하기 위한 아키텍처 패턴으로, 각각 Model-View 관계와 Controller/Presenter/ViewModel의 역할이 다르다.
> 2. **가치**: UI와 Business Logic을 분리하면 테스트 가능성이 향상되고 (Business Logic이 View에 의존하지 않음), 팀 협업이 용이해지며 (프론트엔드/백엔드 독립 개발), 코드 재사용성이 높아진다.
> 3. **융합**: MVC는 전통적 웹 앱 (Ruby on Rails, Django), MVP는 안드로이드 전통 개발, MVVM은 현대적 프론트엔드 (Vue.js, Angular), WPF 등에서 활용되며, Reactive Programming과 결합하여 상태 관리 복잡성을 관리한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: MVC, MVP, MVVM은 모두"관심사 분리 (Separation of Concerns)"를 실현하기 위한 UI 아키텍처 패턴이다. UI (화면 표시)와 Business Logic (데이터 처리)을 분리하면, UI를 바꿔도 Business Logic에 영향이 없고, Business Logic을 테스트해도 UI가 필요 없다.

- **필요성**: UI는频繁하게 변경되고, Business Logic은 상대적으로 안정적이다. 만약这两者가 결합되어 있으면, UI 변경 시 Business Logic에 버그가 발생할 수 있고, Business Logic 테스트를 하려면 UI까지 구축해야 하는 문제가 발생한다.

- **💡 비유**: MVC 계열 패턴은"음식점의 주방과 홀 분리"와 같다. 홀 (View)은 고객에게 음식을 제공하고, 주방 (Model)은 음식을 만들고, 매니저 (Controller/Presenter)는 홀의 주문을 주방에 전달하고 결과를 반환한다. 홀과 주방이 직접 연결되면 고객이 바뀌면 주방까지 다시 教育해야 하지만, 매니저가 주中介하면 독립적으로 운영할 수 있다.

- **등장 배경**:
  - **MVC**: 1979년 Trygve Reenskaug (Smalltalk-80)에서 유래
  - **MVP**: 1990년대 후반 Microsoft (Delphi, COM)에서 Win32 앱 개발을 위해 발전
  - **MVVM**: 2005년 Microsoft (WPF, XAML)에서 데이터 바인딩을 위해 도입

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### MVC vs MVP vs MVVM 비교

| 항목 | MVC | MVP | MVVM |
|:---|:---|:---|:---|
| **媒介** | Controller | Presenter | ViewModel |
| **View↔Model** | 직접 연결 | Presenter가 View에 업데이트 | 데이터 바인딩으로 자동 동기화 |
| **View의 책임** | UI 표시만 | UI + 사용자 입력 처리 | UI 표시 + 상태 유지 |
| **双向 통신** | 한 방향 (Model→View) | 양방향 | 양방향 (바인딩) |
| **적합한 경우** | 전통적 웹 앱 | 데스크톱 앱 | Rich Client / SPA |

### MVC 구조

```text
  ┌─────────────────────────────────────────────────────────────────┐
  │                    MVC (Model-View-Controller) 구조                   │
  ├─────────────────────────────────────────────────────────────────┤
  │
  │   사용자 ──▶ Controller ──▶ Model ──▶ Controller ──▶ View
  │                    ▲         │              │
  │                    │         │              │
  │                    │         ▼              │
  │                    │       View            │
  │                    │       업데이트         │
  │                    │                       │
  │   ※ Model은 View에 대해 알지 못한다 (단방향)              │
  │
  │   예: Ruby on Rails, Django
  │
  └─────────────────────────────────────────────────────────────────┘
```

### MVVM 구조 (데이터 바인딩 기반)

```text
  ┌─────────────────────────────────────────────────────────────────┐
  │                    MVVM (Model-View-ViewModel) 구조                      │
  ├─────────────────────────────────────────────────────────────────┤
  │
  │              데이터 바인딩 (양방향 자동 동기화)
  │                  ⟷⟷⟷⟷⟷⟷⟷⟷⟷
  │                 ⟷             ⟷
  │   ┌──────────┐  ⟷  ┌──────────┐  ⟷  ┌──────────┐
  │   │   Model   │◀──▶│ ViewModel │◀──▶│   View    │
  │   └──────────┘     └──────────┘     └──────────┘
  │
  │   ※ ViewModel은 View의"가상 표현"                     │
  │   ※ ViewModel ↔ View가 데이터 바인딩으로 자동 동기화         │
  │   ※ View는 ViewModel의 메서드를 호출하고, ViewModel의       │
  │     속성 변경 시 View가 자동 업데이트                     │
  │
  │   예: Vue.js, Angular, WPF
  │
  └─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** MVC에서 Controller는"조정자"로, 사용자 입력을 받아 Model을 업데이트하고, 그 결과를 View에 전달한다. Model은 View에 대해 알지 못하므로 단방향 흐름이 형성된다. 반면 MVVM에서는 ViewModel이 View의"가상 모델" 역할을 하며, 데이터 바인딩 (Data Binding)을 통해 ViewModel의 속성 변경 시 View가 자동으로 업데이트된다. 이 차이는"프레젠터가 명령을 내리는" 것과"데이터가 스스로 업데이트되는 것"의 차이다. MVVM의 장점은 UI 코드가 ViewModel의 상세実装知识 없이도 동작할 수 있다는 것이며, 이는 Team에서 View와 ViewModel의 독립적 개발을 가능케 한다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 각 패턴의 강점과 약점

| 패턴 | 강점 | 약점 |
|:---|:---|:---|
| **MVC** | 단순함, 명확한 흐름 | View와 Model 직접 연결 가능 (紧耦合), 테스트 어려움 |
| **MVP** | View와 Presenter 완전 분리, 테스트 용이 | View 업데이트 코드가Presenter에 집중 |
| **MVVM** | 데이터 바인딩으로 UI 자동 업데이트, 생산성↑ | 데이터 바인딩의 복잡성, 디버깅 어려움 |

- **📢 섹션 요약 비유**: MVC는"传令将士"와 같다.将士(Controller)가 전해들은命令(입력)을 military에게(Model)에 전달하고, 그 결과를 다시将士에게 알려 View를更新한다. MVVM은" thérapeut"와 같다.치료사가환자의증상을代理하여약물(Model)을 조절하고, 환자의 상태가 자동으로 更新된다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 프레임워크별 선택 가이드

| 프레임워크 | 권장 패턴 | 이유 |
|:---|:---|:---|
| **React** | MVC / Flux / Redux | Component가 View+Controller 역할 |
| **Vue.js** | MVVM (가까움) | 데이터 바인딩으로 Vuex와 결합 |
| **Angular** | MVVM | Zone.js로 자동 변경 감지 |
| **Ruby on Rails** | MVC | 전형적 Server-side MVC |
| **Spring MVC** | MVC | 서버 사이드 웹 MVC |

### 안티패턴

- **Massive View Controller**: Controller가 너무 많은 역할을 하여 발생하는 안티패턴. 해결: MVC → MVP/MVVM으로 리팩토링
- **Two-way binding blues**: 양방향 바인딩으로 인해 변경 사항 추적이 어려운 상황

- **📢 섹션 요약 비유**: MVC 계열 패턴은"호르몬과 기관지"와 같다. 호르몬(MVC: Controller)이 폐(Model)에 명령을 전달하고, 폐가 산소를 처리하면 호르몬이 이를 받아 혈관(View)을 통해全身에 공급한다. MVVM은"자동 온도 조절기"와 같다. 온도 조절기(ViewModel)가 난방기(Model)를 조절하고, 온도 변화가 자동으로 체온(View)에 반영된다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

- **Reactive + MVVM**: Reactive Programming (RxJS, RxJava)과 MVVM의 결합으로, 복잡한 비동기 상태 관리를 더 체계적으로处理可能

### 참고 표준

- **Microsoft .NET WPF**: MVVM 패턴의典型적 实现
- **Vue.js**: MVVM에 영향을 받은 프론트엔드 프레임워크

- **📢 섹션 요약 비유**: MVC 계열 패턴은"조직도"와 같다. View는고객에게 서비스를 제공하는 현장 직원, Model은재고를 관리하는 창고 관리자, Controller/Presenter/ViewModel은它们之间的协调者다.協調者가 없으면 현장과 창고가直接 소통하게 되어混乱하지만,協調者가 개입하면 업무가 체계적으로 처리된다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Observer Pattern** | MVVM의 데이터 바인딩은 Observer 패턴을 활용하여 구현되며, Model 변경 시 View에 자동으로通知される。 |
| **SOLID Principles** | MVC/MVP/MVVM은 SRP를 实现하여, View (UI)와 Business Logic (Model)을 분리한다. |
| **Data Binding** | MVVM의 핵심 기술로, View와 ViewModel 간의 자동 동기화를実現する。 |
| **Flux/Redux** | React 생태계의 상태 관리 패턴으로, MVC의 복잡한 양방향 데이터 흐름을 단방향으로简化했다。 |
| **Flux** | Frontend 상태 관리 패턴으로, MVC의 문제를 해결하기 위해 단일 Store와 순환 데이터 흐름을 사용한다. |
| **Microservices** | Microservices 환경에서도 View-Model 분리의 개념이 적용되며, API Gateway가 MVC의 Controller 역할을 수행한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. MVC는"학교의.organdon": 선생님(Controller)이 학생(View)의 요청을 받아 교무실(Model)에 전달하고, 결과를 다시 선생님에게 알려 학생에게伝える. MVP는"학생会の副会长": 副会长(Presenter)가学生 Viewと教務間の調整う担う.
2. MVVM은"스마트홈 시스템"과 같아. 스마트폰(View)이 온도조절기(ViewModel)에 연결되어 있고, 온도조절기가 난방기(Model)을 조절하면, 집 안 온도가 자동으로 스마트폰에 표시된다.
3. 세 패턴 모두"고객(View)이요리를 주문하면, 주방(Model)이요리를 하고, 중개자(Controller/Presenter/ViewModel)가요리를 전달하는 것"이라는 동일 结构을 가지고 있으나, 중개자의 역할과 데이터 전달 방식이 다르다.
