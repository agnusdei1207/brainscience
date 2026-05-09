+++
weight = 119
title = "모델-뷰-컨트롤러 (MVC, Model-View-Controller)"
date = "2024-03-20"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- 비즈니스 로직(Model), 사용자 인터페이스(View), 흐름 제어(Controller)를 분리하여 시스템의 **결합도를 낮추고 재사용성**을 극대화함.
- 사용자 요청 시 Controller가 흐름을 제어하고, Model이 데이터를 처리하며, View가 결과를 시각적으로 표현하는 명확한 **관심사 분리** 구조임.
- 웹 애플리케이션 및 모바일 앱의 가장 기초적이고 필수적인 아키텍처 패턴으로, 개발 및 유지보수의 효율성을 보장함.

### Ⅰ. 개요 (Context & Background)
- 1970년대 스몰토크(Smalltalk) 언어에서 GUI 프로그래밍을 위해 처음 제안되었으며, 이후 웹 프레임워크(Spring, Django 등)의 표준으로 자리 잡음.
- 코드의 복잡성을 관리하고, 디자인과 로직의 독립적인 개발을 가능하게 하여 대규모 프로젝트 운영에 필수적인 구조임.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ MVC Pattern Interaction ]

       (Request)      (Route/Control)      (Handle Data)
  User --------> Controller -------------> Model
                   ^   |                     |
                   |   | (Update View)       | (Provide Data)
                   |   v                     |
                   +-- View <----------------+
                       (Display / UI)

* 핵심: Model과 View는 직접적으로 소통하지 않음 (느슨한 결합)
```
- **Model**: 데이터와 비즈니스 로직을 담당함. 상태가 변경되면 관찰자(Observer) 패턴 등을 통해 알림을 보낼 수도 있음.
- **View**: 사용자에게 보여지는 화면(UI). Model의 데이터를 시각적으로 렌더링함.
- **Controller**: 사용자의 입력을 받아 해석하고 Model과 View를 연결하여 전체적인 흐름을 조정함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | MVC (Web Standard) | MVP (Mobile focused) | MVVM (Modern Frontend) |
| :--- | :--- | :--- | :--- |
| **핵심 요소** | Model-View-Controller | Model-View-Presenter | Model-View-ViewModel |
| **상호 작용** | Controller가 중심 통제 | Presenter가 View와 1:1 매핑 | 데이터 바인딩(Binding) 중심 |
| **의존성** | View와 Model 간 간접 의존 | View와 Presenter 강결합 | View와 Model 완전 독립 |
| **주 사용처** | Spring MVC, Rails | 초기 Android 앱 | Vue.js, React, Swift(SwiftUI) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **판단 지표**: 단순한 CRUD 기능 중심의 프로젝트부터 복잡한 엔터프라이즈 시스템까지 광범위하게 적용 가능하며, 특히 서버 사이드 렌더링(SSR) 환경에서 최적임.
- **적용 전략**: Controller에 비즈니스 로직을 넣지 않는 'Fat Model, Skinny Controller' 원칙을 준수하여 도메인 중심 설계를 유지해야 함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 시스템의 **유연성(Flexibility)**과 **확장성(Extensibility)**을 확보하여 다양한 디바이스 및 인터페이스 환경에 대응 가능함.
- 향후 MSA 환경에서도 각 마이크로서비스 내부의 견고한 구현 패턴으로 지속적으로 사용될 핵심 아키텍처임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 소프트웨어 아키텍처, 디자인 패턴
- **파생 패턴**: MVC 모델 1(JSP 중심), MVC 모델 2(Servlet 중심)
- **관련 패턴**: 옵저버 패턴, 전략 패턴, 컴포지트 패턴

### 👶 어린이를 위한 3줄 비유 설명
- 식당에서 '요리사(Model)', '웨이터(Controller)', '메뉴판(View)'의 역할과 같아요.
- 손님이 웨이터에게 주문하면 요리사는 음식을 만들고, 메뉴판을 보고 음식을 고르는 것과 같아요.
- 서로 하는 일이 정해져 있어서 한 사람이 아파도 다른 사람이 그 일을 대신할 수 있는 구조예요.
