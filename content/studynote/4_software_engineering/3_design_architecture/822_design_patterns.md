+++
title = "디자인 패턴 개요"
description = "Design Patterns Overview"
category = "4_software_engineering"
weight = 822
+++

# 디자인 패턴 개요 (Design Patterns Overview)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 디자인 패턴 (Design Patterns)은 소프트웨어 설계에서 자주 반복的に 발생하는 문제에 대한 재사용 가능한解决方案으로, Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides (GoF, Gang of Four)가 1994년 저서에서 23가지 패턴을 체계적으로 정리했다.
> 2. **가치**: 디자인 패턴을 활용하면"훌륭한 설계자의 경험"을 차용하여 설계 시간을 단축하고, 코드 가독성과 유지보수성을 향상시키며, 팀 내 공통 언어로 의사소통 효율성을 높인다.
> 3. **융합**: 디자인 패턴은 SOLID 원칙을 实现하는 구체적 구조이며, Microservices (Service Discovery), Reactive Systems (Observer), Dependency Injection (Factory) 등 현대적 아키텍처의 이론적 기반이다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: 디자인 패턴은"설계の問題 solutions"이다.建築에서優 architect가 반복的に 사용하는 구조가 있지만, 初経験 设计者가 그것을 모르면 처음부터 다시設計해야 하는 것처럼, 소프트웨어에서도 반복적으로 발생하는 설계 문제에 대한 Standard Solutions이 존재한다. GoF (Gang of Four)는 이解决方案을 23가지 패턴으로 정리하여"Design Patterns: Elements of Reusable Object-Oriented Software" (1994)에 체계화했다.

- **필요성**: 모든 설계를 처음부터創作物 Inventor하면 시간 낭비이고, 既知の問題에 대한 没意味한 再発明日이 발생한다. デザイン パターン知识는"설계 문제 해결사의 도구 상자"와 같아서, 问题가发生时 적절한 패턴을 선택하여 再発明日을 줄일 수 있다.

- **💡 비유**: 디자인 패턴은"요리 레시피"와 같다. 모든 요리를 처음부터 开发하면 시간이 오래 걸리지만,"볶음밥 레시피", "김치찌개 레시피"처럼 검증된 레시피를 알면 每食 새롭게 开发할 필요 없이 料理할 수 있다. 소프트웨어에서도"Strategy 패턴", "Observer 패턴"처럼 검증된 설계 구조를 재사용할 수 있다.

- **등장 배경**: 1994년 Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides (GoF)가 저술한"Design Patterns"에서 23가지 패턴을 정리했다. 이 책은 소프트웨어 설계 분야에 있어"바벨과 같은" 존재로 평가받는다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### GoF 23가지 패턴의 분류

| 분류 | 패턴 수 | 핵심 개념 | 대표 패턴 |
|:---|:---|:---|:---|
| **생성 (Creational)** | 5개 | 객체 생성 로직 분리 | Factory Method, Abstract Factory, Singleton, Builder, Prototype |
| **구조 (Structural)** | 7개 | 클래스/객체 조합으로 큰 구조 형성 | Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy |
| **행동 (Behavioral)** | 11개 | 객체 간 책임/알고리즘 할당 | Observer, Strategy, Command, Iterator, Mediator, Memento, State, Template Method, Visitor, Chain of Responsibility, Interpreter |

### 주요 디자인 패턴 구조도

```text
  ┌─────────────────────────────────────────────────────────────────┐
  │              디자인 패턴 3대 분류                                   │
  ├─────────────────────────────────────────────────────────────────┤
  │
  │  [1. 생성 패턴 - 객체 creation 로직 분리]
  │
  │     ┌──────────────┐        ┌──────────────┐
  │     │  Factory     │        │  Singleton   │
  │     │  Method      │        │              │
  │     ├──────────────┤        ├──────────────┤
  │     │ subclass이   │        │ 하나의       │
  │     │ 생성할 객체  │        │ 인스턴스만   │
  │     │ 를 결정      │        │ 존재         │
  │     └──────────────┘        └──────────────┘
  │
  │  [2. 구조 패턴 - 클래스/객체 조합]
  │
  │     ┌──────────────┐        ┌──────────────┐
  │     │  Adapter     │        │  Decorator   │
  │     ├──────────────┤        ├──────────────┤
  │     │ 기존 인터페이스│       │ 새로운 기능   │
  │     │ 를 다른       │        │ 동적으로     │
  │     │ 형태로 변환    │        │ 추가        │
  │     └──────────────┘        └──────────────┘
  │
  │  [3. 행동 패턴 - 책임/알고리즘 분리]
  │
  │     ┌──────────────┐        ┌──────────────┐
  │     │  Observer    │        │  Strategy    │
  │     ├──────────────┤        ├──────────────┤
  │     │ 상태 변화 시 │        │ 알고리즘     │
  │     │ 의존 객체   │        │ 군을        │
  │     │ 에게 통지   │        │ 서로 다름     │
  │     └──────────────┘        └──────────────┘
  │
  └─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 생성 패턴은"객체를 만드는 방법"을 추상화하여 클라이언트 코드와 객체 생성 로직을 분리한다. Factory Method는 하위 클래스에서 생성할 객체를 결정하게 하고, Singleton은 하나의 인스턴스만 존재하도록 보장한다. 구조 패턴은"객체들을 어떻게 조합하여 더 큰 구조를 만드는가"를 다룬다. Adapter는 호환되지 않는 接口를 조정하고, Decorator는 동적으로 기능을 추가한다. 행동 패턴은"객체 간 책임과 알고리즘을 어떻게 분배하는가"를 다룬다. Observer는 상태 변화를 관련 객체에 자동으로 알리고, Strategy는 알고리즘 군을 서로 대체 가능하게 만든다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 디자인 패턴 vs 아키텍처 패턴

| 항목 | 디자인 패턴 | 아키텍처 패턴 |
|:---|:---|:---|
| **범위** | 클래스/모듈 수준 | 시스템 전체 수준 |
| **예시** | Observer, Factory, Strategy | MVC, Microservices, Layered |
| **세부 수준** | 상세 설계 | 상위 구조 설계 |
| **문제 대상** | 구현 단계의 반복적 문제 | 설계 단계의 구조적 문제 |

- **📢 섹션 요약 비유**: 디자인 패턴은"장난감 블록组合说明"과 같다. 블록 조합 방법은 정해져 있어서 (Creational: 조립 방법, Structural: 배치 방법, Behavioral: 작동 방식), 이 방법을 알면 누구나 원하는 장난감을 만들 수 있다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 패턴 선택 가이드

| 상황 | 적합한 패턴 | 고려 사항 |
|:---|:---|:---|
| **객체 생성 로직이 복잡할 때** | Builder, Factory Method | 생성 알고리즘과 객체 표현 분리 |
| **하나의 인스턴스만 필요할 때** | Singleton | 테스트 어렵고 전역 상태 문제 - 사용 자제 |
| **인터페이스가 호환되지 않을 때** | Adapter | 기존 코드 재사용 가능 |
| **동적으로 기능을 추가하고 싶을 때** | Decorator | 상속 대신 조합 사용 |
| **상태에 따라 동작이 달라질 때** | State, Strategy | if-else 체인 회피 |
| **변경 사항을 자동 반영하고 싶을 때** | Observer | event-driven 구조 |

### 안티패턴

- **Patternitis**: 패턴을 쓰기 위해 패턴을 쓰는 상황. 실제 문제보다 패턴 적용에 집중
- **God Class와 Singleton 오남용**: Singleton은全局状態类似的弊病을 가지고 있어 무분별한 사용 금지
- **패턴과 코드 불일치**: 패턴을 적용한 듯하지만 실제로는 pattern의 본질을 따르지 않는"假的 Pattern"

- **📢 섹션 요약 비유**: 디자인 패턴은"설계 레시피"와 같다. 요리사가 모든 요리를 처음 开发하면时间과食材浪费가 발생하지만, 검증된 레시피를 따르면 효율적으로料理할 수 있듯이, 디자인 패턴을 알면 효율적으로 설계를 진행할 수 있다. 그러나 레시피가 없는데 레시피를 억지로 적용하려는 경우도 있다 (Patternitis).

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 패턴 미사용 | 패턴 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 설계 시간 100% | 설계 시간 30~50%↓ | **재설계 시간 절감** |
| **정성** | 설계 불일치 ↓ | 팀 내 공통 언어로 소통↑ | 의사소통 효율성↑ |

### 미래 전망

- **패턴과 AI**: AI 코드 어시스턴트가 패턴 적용을 추천하고, 자동으로 리팩토링을 제안하는方向으로 발전

### 참고 표준

- **GoF (Gang of Four) - Design Patterns: Elements of Reusable Object-Oriented Software (1994)**
- **Martin Fowler - Patterns of Enterprise Application Architecture (PoEAA)**

- **📢 섹션 요약 비유**: 디자인 패턴은"설계의 만화력"과 같다. 100권 이상의 책을全部начать 읽을 필요 없이,핵심 영역만 빠르게 읽고,"여기这部分은 이미 다른 설계자들이 문제를 해결한 바 있어"라는 걸 利用하면 효율적인 设iser가 될 수 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **SOLID Principles** | SOLID 원칙은 디자인 패턴을 올바르게 적용하기 위한 前置 조건이며, SOLID를 따르면 대부분의 패턴이 자연스럽게 적용된다. |
| **Creational Patterns** | Singleton, Factory Method, Builder, Prototype, Abstract Factory가 속하며, 객체 생성 로직을 추상화하여 결합도를 낮춘다. |
| **Structural Patterns** | Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy가 속하며, 클래스/객체 조합으로 큰 구조를 형성한다. |
| **Behavioral Patterns** | Observer, Strategy, Command, Iterator 등이 속하며, 객체 간 책임과 알고리즘의 할당을 관리한다. |
| **MVC (Model-View-Controller)** | 복합 패턴으로, Observer (Model→View), Strategy (Controller), Composite (View) 등이 결합된 아키텍처 패턴이다. |
| **Microservices** | Microservices의 Service Discovery, Circuit Breaker 등은GoF 패턴에서 유래한 기술적 개념을 활용한다. |
| **Anti-Patterns** | 디자인 패턴의 오남용, 특히 Singleton 과다사용과 Patternitis (패턴을 위한 패턴)가 대표적인 안티패턴이다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. 디자인 패턴은"장난감 조립 예제집"과 같아. 예쁜 장난감 건물을 만드는데,"기둥은 이렇게 세우고, 지붕은 이렇게 얹고, 문은 이렇게 달아"라는 예제가 있으면 그 예제를 따라하면 되잖아. 그 예제가"패턴"이야.
2. 패턴을 다 외우면 새로운 것을 开发할 필요 없이,"이 상황엔 이 패턴이랑 저 상황엔 저 패턴"을 적용하면 돼. 마치 요리 레시피를 아는셰프처럼.
3. 그런데 무리하게 패턴을 적용하면 안 돼. 예를 들어"이 요리엔 무조건김치찌개 레시피를 적용해야 한다"고 하면 이상하잖아? 그래서"적절한 상황에 적절한 패턴"을 적용하는 것이 중요해!
