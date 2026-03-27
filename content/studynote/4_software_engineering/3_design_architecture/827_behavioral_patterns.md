+++
title = "행동 패턴"
description = "Behavioral Design Patterns"
category = "4_software_engineering"
+++

# 행동 패턴 (Behavioral Design Patterns)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 행동 패턴 (Behavioral Patterns)은 객체 간 책임과 알고리즘을 어떻게 할당하고, 객체 간 communication을 어떻게組織하는かを扱う GoF 디자인 패턴으로, Observer, Strategy, Command, Iterator, Mediator, Memento, State, Template Method, Visitor, Chain of Responsibility, Interpreter의 11개 패턴이 포함된다.
> 2. **가치**: 행동 패턴을 활용하면"무엇을 하는가"와"어떻게 하는가"를 분리하여, 알고리즘의 교체/변경이 객체 구조에 영향을 미치지 않게 하고, 객체 간 communication을 느슨하게 결합할 수 있다.
> 3. **융합**: Observer 패턴은 Reactive Programming (RxJS, RxJava)의 기반이 되고, State 패턴은 게임 개발, 워크플로 엔진, Vending Machine 등에 활용되며, Command 패턴은Undo/Redo, Macro Recording 등에 활용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: 행동 패턴은"객체들 사이에서 behavior를 어떻게 분배하고, communication을 어떻게 처리하는가?"를 다룬다. 예를 들어"여러 객체가同一イベント에反応해야 할 때"그 relation을Hard-coding하면 결합도가 높아지고 변경이 어려워진다. Observer 패턴은"하나의 주제가 변하면 여러 관찰자에게自動的に通知される" 구조를 통해 이문제를 해결한다.

- **필요성**: 객체지향 시스템에서 가장 빈번하게 변하는 것은"행위 (behavior)"다. Business 로직이 바뀌면 여러 객체에 걸쳐 영향을 미치는데, 이때 행동 패턴을活用하면"영향을 받는 객체"와"그 연결 방식"을 분리할 수 있어 변경의 영향을局部化할 수 있다.

- **💡 비유**: 행동 패턴은"소방 시스템"과 같다. 화기 감지기가 동작하면 (Subject), 모든スプリン클러가 동시에 작动感知らせ (Observer). 만약 이러한 연결이Hard-coding되어 있으면, 새로운 sprinkler 추가 시 감지기도 수정해야 하지만, Observer 패턴을 활용하면 감지기는 sprinkler 추가에 대해 알 필요가 없어진다.

- **등장 배경**: 1994년 GoF (Gang of Four)의"Design Patterns"에서 체계화되었으며, 이후 Reactive Programming, Event-Driven Architecture 등 다양한 영역으로 확장되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 주요 행동 패턴

| 패턴 | 핵심 아이디어 | 사용 시점 | 예시 |
|:---|:---|:---|:---|
| **Observer** | 상태 변화를 관련 객체에 자동通知 | 1:N 의존 관계, event handling | MVC/MVVM의 Model-View |
| **Strategy** | 알고리즘 군을 서로 대체 가능하게 | 다양한 알고리즘 선택 시 | 정렬 전략 |
| **Command** | 요청을 객체로 캡슐화 | Undo/Redo, 작업 큐 | GUI 버튼 액션 |
| **Iterator** | 내부 표현 없이 순회 | 컬렉션 순회 abstraction | Java Iterator |
| **Mediator** | 객체 간 직접 통신 대신 mediator 통해 | 객체 간 복잡한 상호작용 |机场管制塔 |
| **State** | 상태에 따라 동작이 변경 | 상태 기계 구현 | 게임 캐릭터 상태 |
| **Template Method** | 알고리즘의 구조는 고정, 일부 단계는 하위에서 | 공정 틀 결정, 세부 구현은 하위에서 |
| **Visitor** | 알고리즘을 객체에서 분리 | 기존 객체 구조에 새 操作追加 | 파일 시스템遍历 |
| **Chain of Responsibility** | 요청을 처리할 때까지 체인으로 연결 | 요청 처리자 순서 미정 | event handling |

### Observer 패턴 구조

```text
  ┌─────────────────────────────────────────────────────────────────┐
  │                    Observer 패턴 구조                                   │
  ├─────────────────────────────────────────────────────────────────┤
  │
  │  [Subject (주제)]                 [Observer (관찰자)]               │
  │  ┌──────────────────────┐          ┌──────────────────────┐        │
  │  │ - observers: List    │────────▶ │ + update()          │        │
  │  ├──────────────────────┤          └──────────────────────┘        │
  │  │ + attach(observer)   │                   ▲                     │
  │  │ + detach(observer)   │                   │                     │
  │  │ + notify()          │         ┌─────────┴─────────┐          │
  │  └──────────┬───────────┘         │                     │          │
  │             │                     │ + update()      │ + update()  │
  │             │                     │ (구체 Observer A) │ (구체 Observer B) │
  │             │                     └─────────────────┘                │
  │             │ notify() 호출 시                                                │
  │  ┌──────────┴───────────┐                                           │
  │  │ state = newValue     │                                           │
  │  │ for obs in observers │                                           │
  │  │   obs.update(state) │                                           │
  │  └─────────────────────┘                                           │
  │
  │  예시: 주식 가격 변동 → 다수의 Trader에게 자동通知
  │
  │  [주식 가격 예시]                                                    │
  │
  │  ┌─────────────┐                              ┌─────────────┐     │
  │  │ StockPrice  │ ──── notifications ────▶ │   Trader A   │     │
  │  │ (Subject)   │                              └─────────────┘     │
  │  └─────────────┘                              ┌─────────────┐     │
  │       │                                        │   Trader B   │     │
  │       │ subscribe()                             └─────────────┘     │
  │       ▼                                        ┌─────────────┐     │
  │  ┌─────────────┐                              │   Trader C   │     │
  │  │ StockDisplay │                              └─────────────┘     │
  │  │(Observer)   │                                               │
  │  └─────────────┘                                               │
  │
  │  ※ StockPrice가 변경되면 모든 구독 Trader/Display에 자동通知       │
  │
  └─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Observer 패턴의 핵심은"발행-구독 (Publish-Subscribe)" 구조다. Subject (주제)는 자신의 상태를 관찰하는 Observer들을 목록으로 관리한다. Subject의 상태가 변경되면 attach/detach로 Observer를 추가/제거하고, notify()를 호출하여 모든 Observer의 update() 메서드를 호출한다. Observer는 Subject에 직접 결합되지 않고"구독"을 통해 연결되므로, Observer 추가/제거가 Subject에 영향을 미치지 않는다. 이는 결합도를 낮추고 유연성을 높이는 핵심 설계이다.

---

## Ⅲ. Strategy vs State vs Command 비교

| 패턴 | 목적 | 결정 주체 | 사용 시점 |
|:---|:---|:---|:---|
| **Strategy** | 알고리즘 선택 | 클라이언트 | 런타임에 알고리즘 전환 |
| **State** | 상태에 따른 동작 변경 | 객체 내부 상태 | 상태 전이 로직 분리 |
| **Command** | 요청을 객체로 캡슐화 | 클라이언트 | Undo/Redo, 큐잉 |

- **📢 섹션 요약 비유**: 행동 패턴은"조직 내 역할 분담"과 같다. Observer는"사소식 담당" (변경 사항 전달), Strategy는"전문가 pool" (어떤 전문가를 언제 쓸지), State는"직급별 권한" (상태에 따라 다른 행위), Command는"작업 지시서" (실행과 명령 자체의 분리).

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 패턴 선택 가이드

| 상황 | 적합한 패턴 |
|:---|:---|
| 여러 객체에 상태 변경을通知해야 할 때 | Observer |
| 알고리즘을 런타임에 선택해야 할 때 | Strategy |
| 요청을 캡슐화하여 Undo/Redo해야 할 때 | Command |
| 컬렉션 순회 로직을 숨기고 싶을 때 | Iterator |
| 객체 간 통신을 중앙화하고 싶을 때 | Mediator |
| 상태에 따라 동작이 달라질 때 | State |
| 알고리즘 뼈대는 고정, 일부 단계만 변할 때 | Template Method |
| operação를 기존 객체 구조에 추가하고 싶을 때 | Visitor |
| 요청 처리자를 동적으로 결정하고 싶을 때 | Chain of Responsibility |

### 안티패턴

- **Observer 과다**: 너무 많은 Observer가 하나의 Subject를 관찰하면通知コスト이 증가
- **State 패턴 오남용**: 단순 if-else로 해결 가능한 것을 굳이 State 패턴으로 만들면 과도한抽象化

- **📢 섹션 요약 비유**: 행동 패턴은"영화 제작의 역할分担"과 같아. Observer는"스태프들에게Cambodian을 알리는 AD (Assistant Director)", Strategy는"장면마다 다른 촬영 방법론 선택", State는"배우의 신분 (학생/직장인/군인)에 따른 다른 연기", Command는"각 클립 (명령)을 편집기에 던지는 조작".

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

- **Reactive Programming**: Observer 패턴의 확장인 Reactive Programming (RxJava, RxJS)이 비동기 데이터 스트림 처리의 표준으로 자리잡음

### 참고 표준

- **GoF - Design Patterns**: 행동 패턴의 원천 출처

- **📢 섹션 요약 비유**: 행동 패턴은"오케스트라 지휘 시스템"과 같아. 지휘자 (Mediator)가 각 악기 (객체)에 언제, 어떻게 연주할지를 지시하고, Violinists (Strategy)는 그 지시에 따라 다양한 연주법을 선택하며, Conductor의 지시 (Command)는 녹음되어Undo가 가능하다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Observer Pattern** | 행동 패턴의 하나로, 1:N 의존 관계에서 객체 상태 변경을 자동通知する。 Reactive Programming의 기반이 된다. |
| **Strategy Pattern** | 알고리즘 군을 인터페이스로 캡슐화하여, 클라이언트가 런타임에 알고리즘을 선택할 수 있게 한다. |
| **Command Pattern** | 요청을 객체로 캡슐화하여, Undo/Redo, 작업 큐잉,宏 Recording등에 활용된다. |
| **State Pattern** | 객체 내부 상태에 따라 동작이 자동으로 전환되도록 하는 패턴으로, FSM (Finite State Machine) 구현에 활용된다. |
| **Mediator Pattern** | 객체 간 직접 통신을 막고 중앙 mediator를 통해 통신하게 함으로써 결합도를 낮춘다. |
| **Event-Driven Architecture** | Observer 패턴의 확장으로, собы트의 발신과 처리를 분리하는 아키텍처 스타일이다. |
| **Reactive Programming** | Observer 패턴과 Iterator 패턴을 결합한 개념으로,非同期数据 streams를宣言的に 처리한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. 행동 패턴은"소방대와 주민의 역할 분담"과 같아. Observer는"화재 발생 시 주민들에게 동시에 알리는 구조" (火灾 감지기→주민들에게 simultaneity 알림), Strategy는"어떤 진화 방법을 쓸지 선택" (폭발 진화→물 진화 등), State는"게임 캐릭터가 상태에 따라 다르게 움직임" (앉기→걷기→달리기).
2. Observer 패턴의 예로"유튜브 채널 구독"을 생각하면 돼. 채널主 (Subject)가 새 영상을 올리면 구독자 (Observer) 모두에게 동시에 알림이 간다.
3. Strategy 패턴은"음식 올림픽에서 어떤 요리법을 선택할지"와 같아. 같은 재료(입력)에 대해서도 퓨전 요리, Italian, Japanese 등 어떤 요리법(전략)을 쓸지에 따라 결과가 달라진다.
