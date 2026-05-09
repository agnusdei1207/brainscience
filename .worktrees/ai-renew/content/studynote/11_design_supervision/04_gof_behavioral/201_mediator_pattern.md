+++
weight = 201
title = "201. 중재자 패턴 (Mediator Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Mediator (중재자) 패턴은 객체 간 M:N 복잡한 직접 통신망을 1:N 구조로 단순화하여, 모든 통신이 중앙 중재자 객체를 통해서만 이루어지도록 강제한다.
> 2. **가치**: 각 Colleague (동료) 객체가 서로를 직접 참조하는 대신 중재자만 알면 되므로, 새로운 객체 추가나 기존 로직 변경이 다른 객체에 영향을 주지 않는다.
> 3. **판단 포인트**: 객체 수 증가에 따라 통신 경로가 O(n²)으로 폭발하는 문제가 있을 때 Mediator 패턴을 적용하여 O(n)으로 줄인다.

---

## Ⅰ. 개요 및 필요성

### 1-1. M:N 통신의 문제

UI 컴포넌트가 5개 있고 서로 직접 통신한다면, 통신 경로는 최대 n(n-1)/2 = 10개다. 컴포넌트가 10개가 되면 45개의 의존성이 생긴다. 이를 Spaghetti Communication (스파게티 통신)이라 한다.

```
  [ M:N 직접 통신 - 5개 컴포넌트 ]
  
  A ──────── B
  │\        /│
  │  \    /  │
  │    \  /  │
  │     \/   │
  │     /\   │
  │   /    \ │
  │ /        \│
  C ──────── D
        │
        E
  
  통신 경로: 10개 (= 5×4÷2)
  → 컴포넌트 하나 변경 시 연결된 모든 객체 영향
```

### 1-2. Mediator 적용 후

```
  [ 1:N 중재 통신 - Mediator 적용 ]
  
  A ──────┐
  B ──────┤
  C ──────┼───► Mediator ◄──── 모든 통신 집중
  D ──────┤
  E ──────┘
  
  통신 경로: 5개 (= n개)
  → 새 컴포넌트 추가 시 Mediator만 수정
```

### 1-3. 현실 세계의 사례

| 사례 | Mediator 역할 | Colleague 역할 |
|:---|:---|:---|
| ATC (Air Traffic Control, 항공 교통 관제탑) | 관제탑 | 항공기들 |
| 채팅방 | 채팅 서버 | 사용자들 |
| Spring MVC DispatcherServlet | DispatcherServlet | Controller, ViewResolver, HandlerMapping |
| 증권 거래소 | 거래 매칭 엔진 | 매수자·매도자 |
| 이벤트 버스 (Event Bus) | 버스 | 구독자·발행자 |

📢 **섹션 요약 비유**: 항공기들이 서로 직접 교신하면 충돌 위험이 있다. 관제탑(Mediator)이 모든 교신을 중계하기 때문에 안전한 비행이 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 구조 (UML 요약)

```
  «interface»                    «interface»
  Mediator                       Colleague
  ─────────────                  ────────────────
  + notify(sender, event)        + setMediator(m)
        ▲                              ▲
        │                    ┌─────────┴──────────┐
  ConcreteMediator         ColleagueA          ColleagueB
  ─────────────────
  - colleagueA: ColleagueA
  - colleagueB: ColleagueB
  + notify(sender, event)
    → 이벤트 라우팅 로직
```

### 2-2. 채팅방 예시 구현 구조

```
  ┌─────────────────────────────────────────────────────────┐
  │                   ChatRoom (Mediator)                   │
  │                                                         │
  │  participants: List<User>                               │
  │                                                         │
  │  sendMessage(from, message)                             │
  │    → participants.forEach(u →                          │
  │        if (u != from) u.receive(message))               │
  └─────────────────────────────────────────────────────────┘
        ▲              ▲              ▲
        │              │              │
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │  Alice   │  │   Bob    │  │ Charlie  │
  │ (User)   │  │  (User)  │  │  (User)  │
  │          │  │          │  │          │
  │ send()   │  │ send()   │  │ send()   │
  │ receive()│  │ receive()│  │ receive()│
  └──────────┘  └──────────┘  └──────────┘
  
  Alice가 Bob에게 메시지: Alice → ChatRoom → Bob
  (Alice는 Bob을 직접 참조하지 않음)
```

### 2-3. Spring MVC DispatcherServlet 분석

```
  HTTP Request
       │
       ▼
  DispatcherServlet (Mediator)
       │
       ├──► HandlerMapping → 어느 Controller?
       │
       ├──► HandlerAdapter → Controller 실행
       │
       ├──► Controller (Colleague) → ModelAndView
       │
       ├──► ViewResolver → View 선택
       │
       └──► View → 응답 렌더링

  Controller는 ViewResolver를 모른다.
  ViewResolver는 HandlerMapping을 모른다.
  DispatcherServlet이 모든 컴포넌트를 조율한다.
```

📢 **섹션 요약 비유**: 오케스트라 지휘자(Mediator)가 없다면 각 악기 연주자들이 서로 눈치 보며 박자를 맞춰야 한다. 지휘자가 있어야 웅장한 교향곡이 나온다.

---

## Ⅲ. 비교 및 연결

### 3-1. Mediator vs Observer vs Facade 비교

| 비교 항목 | Mediator | Observer | Facade |
|:---|:---|:---|:---|
| **통신 방향** | 양방향 | 단방향 (pub→sub) | 단방향 |
| **객체 인식** | 중재자만 인식 | 이벤트 채널만 인식 | 서브시스템 몰라도 됨 |
| **사용 목적** | 객체 간 통신 조율 | 상태 변화 알림 | 복잡한 API 단순화 |
| **Coupling 감소** | Colleague 간 | Subject-Observer 간 | 클라이언트-서브시스템 간 |
| **핵심 역할** | 라우터·조율자 | 알림 발송 | 인터페이스 단순화 |

### 3-2. Message Bus (메시지 버스)와의 관계

```
  Mediator Pattern           Message Bus (Enterprise 패턴)
  ──────────────────         ──────────────────────────────
  - 단일 Mediator 객체       - 분산 시스템의 Mediator
  - 단일 프로세스 내부        - 서비스 간 비동기 통신
  - 직접 메서드 호출          - 메시지 브로커(Kafka, RabbitMQ)
  - 동기(Synchronous)        - 비동기(Asynchronous)
  
  메시지 버스 = Mediator 패턴의 분산 버전
```

📢 **섹션 요약 비유**: Mediator는 "회사 내부 메신저 서버", Message Bus는 "국제 전신 네트워크". 규모가 다를 뿐 중재 원리는 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. MediatR 패턴 (CQRS 연계)

.NET의 MediatR 라이브러리는 Mediator 패턴을 CQRS (Command Query Responsibility Segregation)와 결합한다:

```
  [ CQRS + Mediator ]
  
  Controller
      │
      ├──► mediator.Send(CreateOrderCommand)
      │         │
      │         ▼
      │    CreateOrderHandler.Handle()
      │
      └──► mediator.Send(GetOrderQuery)
                │
                ▼
          GetOrderHandler.Handle()
  
  Controller는 Handler를 직접 모름 → 완전한 분리
```

### 4-2. God Object (갓 오브젝트) 위험

Mediator의 가장 큰 위험은 **중재자 자체가 거대해지는 것**이다:

```
  ❌ 안티패턴: 비대한 Mediator
  
  ConcreteMediator {
      비즈니스 로직 A
      비즈니스 로직 B
      비즈니스 로직 C
      UI 렌더링 로직
      데이터 검증 로직
      네트워크 통신 로직
  }
  → God Object! 유지보수 불가능

  ✅ 개선: Mediator는 라우팅만
  ConcreteMediator {
      notify(sender, event) {
          // 라우팅만 담당, 로직은 각 Handler로 위임
      }
  }
```

### 4-3. 기술사 서술 포인트

- Mediator 패턴을 설명할 때 **O(n²) → O(n) 복잡도 감소**를 수치로 표현하면 고득점
- ATC (Air Traffic Control) 비유는 시험에서도 자주 사용되는 표준 예시
- God Object 위험과 대응 방법을 함께 서술하면 심화 이해를 증명

📢 **섹션 요약 비유**: 좋은 Mediator는 "전화 교환원"처럼 연결만 해주고, 나쁜 Mediator는 "모든 결정을 혼자 내리는 독재자"처럼 된다.

---

## Ⅴ. 기대효과 및 결론

### 5-1. 기대 효과

| 효과 | 설명 |
|:---|:---|
| 복잡도 감소 | 통신 경로 O(n²) → O(n) |
| 재사용성 향상 | Colleague가 독립적 → 다른 시스템에서 재사용 가능 |
| 변경 용이성 | 통신 규칙 변경 시 Mediator만 수정 |
| 테스트 용이 | Mediator와 Colleague 독립 단위 테스트 |

### 5-2. 주의사항

- Mediator가 God Object로 비대화되지 않도록 **라우팅 전용**으로 제한
- Mediator 자체가 단일 장애점(SPOF, Single Point of Failure)이 될 수 있음 → 고가용성 설계 필요
- 동기 방식의 단일 Mediator는 **병목(Bottleneck)** 우려 → 비동기 이벤트 버스로 확장 검토

### 5-3. 결론

Mediator (중재자) 패턴은 복잡한 객체 협력 구조를 단순화하는 강력한 도구다. Spring MVC의 DispatcherServlet, 채팅 시스템, ATC 등 현실 세계와 소프트웨어 전반에 걸쳐 광범위하게 적용된다. 단, Mediator 자체의 비대화를 방지하는 설계 절제가 필수다.

📢 **섹션 요약 비유**: 훌륭한 관제탑은 항공기들이 안전하게 날 수 있도록 최소한의 지시만 한다. 너무 많은 것을 관제탑이 결정하면 관제탑 자체가 병목이 된다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF Behavioral Pattern | 행동 패턴 그룹 |
| 하위 개념 | ConcreteMediator | 실제 통신 조율 구현체 |
| 연관 개념 | Observer Pattern | Mediator와 조합 가능 |
| 연관 개념 | ATC (Air Traffic Control) | 대표적 현실 세계 비유 |
| 연관 개념 | DispatcherServlet | Spring MVC 적용 사례 |
| 연관 개념 | Message Bus | 분산 시스템에서의 Mediator |

### 👶 어린이를 위한 3줄 비유 설명

- 학교에서 친구들이 서로 직접 편지를 주고받으면 너무 복잡해요.
- 우체통(Mediator) 하나에 편지를 넣으면, 선생님이 알아서 전달해 줘요.
- 이렇게 모든 소통이 한 곳을 통하는 게 중재자 패턴이에요!
