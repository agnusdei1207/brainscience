+++
title = "610. 프론트엔드 패턴 (MVC, MVP, MVVM)"
date = "2026-03-05"
[extra]
categories = "studynotes-software-engineering"
+++

# 610. 프론트엔드 패턴 (MVC, MVP, MVVM) - 화면과 로직의 아름다운 분리

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사용자에게 보이는 **화면(View)**, 실제 데이터를 다루는 **모델(Model)**, 그리고 이 둘 사이의 흐름을 제어하는 **컨트롤러 계열(C, P, VM)**을 분리하여 코드의 스파게티화를 막는 UI 설계 아키텍처 패턴이다.
> 2. **진화**: 초기의 MVC가 뷰와 모델의 의존성을 완전히 끊지 못해 복잡해지자, 인터페이스를 통해 뷰를 완전히 격리한 **MVP**, 그리고 양방향 데이터 바인딩을 통해 제어 코드를 자동화한 **MVVM**으로 진화했다.
> 3. **가치**: UI 디자인(퍼블리셔)과 비즈니스 로직(개발자)의 병렬 개발을 가능하게 하고, UI 환경(웹, 모바일 등)이 바뀌어도 모델 로직을 그대로 재사용할 수 있게 하며 테스트 용이성을 극대화한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
GUI(Graphical User Interface) 애플리케이션을 만들 때, 버튼 클릭 이벤트를 처리하는 코드와 데이터베이스에서 값을 가져오는 코드를 한 파일에 섞어 쓰면 유지보수가 불가능해진다. 이 문제를 해결하기 위해 '관심사 분리(Separation of Concerns)' 철학을 화면단에 적용한 것이 이 세 가지 패턴이다.

### 💡 비유
- **패턴 없는 코드**: 손님이 주방에 불쑥 들어와서 직접 냉장고(데이터)를 열어 요리를 꺼내 먹는 식당이다. 손님이 다칠 수도 있고 주방이 엉망이 된다.
- **M-V-C/P/VM 패턴**: 손님(View)은 예쁜 식당 홀에 앉아 메뉴판만 본다. 웨이터(Controller/Presenter/ViewModel)가 손님의 주문을 받아 주방장(Model)에게 전달한다. 주방장이 요리를 완성하면 웨이터가 다시 손님 테이블(View)로 가져다준다. 손님과 주방장은 서로 얼굴을 볼 필요가 없다.

### 등장 배경: 'Fat Controller'와 'View의 독립성'
데스크톱 앱 시절 탄생한 MVC 패턴은 시간이 지나며 Controller가 너무 뚱뚱해지고 View와 Model 사이에 미세한 결합이 남는 문제를 보였다. 이후 모바일 앱과 SPA(Single Page Application) 웹 환경이 발전하면서, View를 더 철저하게 분리하기 위한 MVP와 데이터 상태 동기화를 프레임워크가 알아서 해주는 MVVM이 대세로 자리 잡았다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 3대 패턴의 구조적 차이 (ASCII Diagram)

```ascii
[ 1. MVC (Model-View-Controller) ]
   (User Input) ──> [ Controller ] ──(Update)──> [ Model ]
                          │                          │ (State Change Event)
                          └────────(Select)────────> [ View ] <───┘
   * 특징: Controller가 입력을 받고 Model을 조작함. View는 Model의 상태 변화를 관찰하여 스스로 화면을 갱신함 (의존성 존재).

[ 2. MVP (Model-View-Presenter) ]
   (User Input) ──> [ View ] ──(Interface)──> [ Presenter ] ──(Update/Read)──> [ Model ]
                       ▲                             │
                       └──────────(Update UI)────────┘
   * 특징: View와 Model은 서로 완전히 모름. Presenter가 중간에서 1:1로 View의 인터페이스를 호출해 화면을 강제로 그림.

[ 3. MVVM (Model-View-ViewModel) ]
   (User Input) ──> [ View ] <══(Data Binding)══> [ ViewModel ] ──(Update/Read)──> [ Model ]
   * 특징: View가 ViewModel의 데이터를 관찰(Observer). ViewModel의 데이터가 바뀌면 프레임워크(React, Vue 등)가 마법처럼 View를 자동으로 갱신함. ViewModel은 View를 전혀 모름.
```

### 핵심 구성 요소 및 차이점 상세

#### ① MVC (Model-View-Controller)
- **Controller의 역할**: 사용자의 입력(클릭, 타이핑)을 가장 먼저 받는 진입점이다.
- **문제점**: 웹 환경에서는 View와 Controller가 거의 한 몸처럼 강하게 결합(JSP, ASP 등)되어 테스트가 매우 어렵다.

#### ② MVP (Model-View-Presenter)
- **Presenter의 역할**: Controller와 달리 View의 인터페이스(Contract)를 통해서만 화면을 조작한다. "텍스트 박스에 'Hello'라고 적어라"라고 명시적으로 지시한다.
- **장점**: View 로직을 순수 자바(Java/C#) 코드로 100% Mocking 하여 유닛 테스트하기 가장 완벽한 구조다. (Android 초창기 대세).
- **단점**: View와 Presenter가 1:1로 매핑되어, 화면이 복잡해질수록 Presenter 코드가 기하급수적으로 길어진다.

#### ③ MVVM (Model-View-ViewModel)
- **ViewModel의 역할**: View를 표현하기 위한 '상태 데이터(State)'를 들고 있는 모델이다. 화면에 보여줄 텍스트, 체크박스 상태 등이 변수에 담겨 있다.
- **양방향 데이터 바인딩**: MVVM의 핵심. ViewModel의 변수값이 바뀌면 View의 글자가 자동으로 바뀌고, 사용자가 View에 글을 쓰면 ViewModel의 변수값이 자동으로 바뀐다. (개발자가 UI 업데이트 코드를 짤 필요가 없음).

---

## Ⅲ. 융합 비교 및 다각도 분석

### MVC vs MVP vs MVVM 심층 비교

| 비교 항목 | MVC | MVP | **MVVM** |
|:---:|:---|:---|:---|
| **입력 진입점** | Controller | View | **View** |
| **의존성 (View-Model)**| 약간 존재함 (View가 Model 관찰)| **완벽히 격리됨** | **완벽히 격리됨** |
| **View-제어자 관계**| 1 : N | 1 : 1 (강결합 인터페이스) | **N : 1 (다대일 바인딩 가능)**|
| **UI 업데이트 방식**| 수동 (또는 Model 이벤트 수신)| 수동 (Presenter가 직접 지시) | **자동 (프레임워크의 Data Binding)**|
| **테스트 용이성** | 낮음 | **매우 높음 (수동 제어)** | 높음 (데이터만 검증하면 됨) |
| **대표 기술 스택** | Spring MVC, Ruby on Rails | Android (전통적), WinForms | **React, Vue.js, WPF, SwiftUI**|

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (프론트엔드 아키텍처 선택)

**상황**: 사용자가 버튼을 누르면 서버에서 주식 데이터를 실시간으로 가져와 수십 개의 차트와 표에 쉴 새 없이 뿌려주는 복잡한 웹 대시보드(SPA)를 만들어야 한다.
**판단 및 패턴 적용 전략**:
1. **패턴 선정**: DOM(화면 요소)을 자바스크립트로 일일이 찾아다니며 수정하는 MVP/MVC 방식은 코드 복잡도를 감당할 수 없다. 상태(State)가 변하면 화면이 알아서 변하는 **MVVM 방식**이 압도적으로 유리하다.
2. **프레임워크 채택**: MVVM 사상을 완벽히 구현하는 **Vue.js** 또는 **React.js**(정확히는 단방향 Flux/MVVM 혼합)를 도입한다.
3. **계층 분리**: 
   - **View**: HTML/CSS 기반의 컴포넌트 렌더링만 담당.
   - **ViewModel**: `useState`, `Ref` 등을 이용해 화면에 그릴 상태(주식 가격 변수) 유지 및 가공.
   - **Model**: Axios/Fetch로 서버 API를 찔러 데이터를 가져오는 순수 비즈니스 통신 로직.
4. **결과**: 서버 데이터(Model)가 변경되어 ViewModel 변수에 들어가면 화면 30군데가 개발자의 개입 없이 자동으로 깜빡이며 최신화됨. 버그 발생률 70% 감소.

### 안티패턴 및 고려사항
- **비대한 뷰모델 (God ViewModel)**: MVVM이 편하다고 ViewModel 파일 하나에 서버 통신 로직(Model), 데이터 파싱, 화면 상태 제어 로직을 몽땅 구겨 넣는 현상. 이렇게 되면 MVC의 'Fat Controller' 문제가 재현된다. Model(비즈니스 로직) 영역은 반드시 ViewModel 밖으로 쪼개 내야 한다.

---

## Ⅴ. 미래 전망 및 결론

### 결론: 바인딩(Binding)의 승리
결국 UI 아키텍처의 역사는 "개발자가 화면의 픽셀(DOM)을 직접 건드리는 짓을 어떻게 안 할 수 있을까?"에 대한 투쟁의 역사였다. 그 싸움은 데이터 바인딩이라는 무기를 들고나온 MVVM의 압승으로 귀결되며 현대 프론트엔드의 표준이 되었다.

### 미래 전망
최근 React 중심의 진영에서는 MVVM을 넘어 데이터 흐름을 단방향으로 완전히 통제하는 **'Flux 아키텍처 (Redux 등)'**와 혼합된 형태가 대세를 이루고 있다. 앞으로는 상태(State) 관리의 복잡성을 AI가 예측하여 최적의 렌더링 시점을 계산하는 선언적(Declarative) UI 패러다임이 더욱 고도화될 전망이다.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [단방향 데이터 흐름 (Flux/Redux)](../../4_software_engineering/4_architecture/react_flux.md) - MVVM의 양방향 바인딩 단점을 보완한 최신 패턴
- [옵저버 패턴 (Observer Pattern)](./604_design_patterns_23.md) - MVVM의 데이터 바인딩을 가능하게 하는 핵심 디자인 패턴
- [클린 아키텍처](./608_clean_architecture.md) - 이 패턴들(프레젠테이션 계층)을 감싸고 있는 더 거대한 설계 철학
- [관심사 분리 (SoC)](./602_information_hiding.md) - 이 패턴들을 탄생시킨 대원칙

---

## 👶 어린이를 위한 3줄 비유 설명
1. **프론트엔드 패턴이 뭔가요?**: 인형극을 할 때 무대(화면)에서 인형을 움직이는 사람(뷰)과 뒤에서 대본을 쓰는 사람(모델)이 서로 싸우지 않게 역할을 딱 나눠주는 규칙이에요.
2. **MVC, MVP, MVVM은 어떻게 다른가요?**: 인형과 대본을 연결하는 방식이 달라요. MVC는 감독님이 가운데서 소리치는 거고, MVP는 감독님이 인형의 팔다리를 직접 꼼꼼하게 만져주는 방식이에요.
3. **가장 많이 쓰는 MVVM은요?**: 인형에 '마법의 마리오네트 실(데이터 바인딩)'을 달아놔서, 뒤에서 대본(데이터)만 슬쩍 고치면 무대 위 인형이 알아서 춤을 추게 만드는 가장 편하고 신기한 방식이랍니다!
