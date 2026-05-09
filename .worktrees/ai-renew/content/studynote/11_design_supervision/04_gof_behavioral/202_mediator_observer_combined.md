+++
weight = 202
title = "202. 중재자-옵저버 혼합 패턴 (Mediator-Observer Combined Architecture)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Mediator (중재자)의 **중앙 집중 라우팅**과 Observer (옵저버)의 **느슨한 결합 이벤트 구독**을 결합하면, 확장성과 유연성을 모두 갖춘 이벤트 기반 아키텍처가 탄생한다.
> 2. **가치**: Mediator가 이벤트 채널 역할을 하고 Colleague들이 Observer로 등록함으로써, 새로운 구독자 추가 시 Mediator 코드를 수정하지 않아도 된다.
> 3. **판단 포인트**: God Object (갓 오브젝트) 위험이 있을 때 Observer 패턴으로 Mediator를 내부 분해하면 책임을 분산시킬 수 있다.

---

## Ⅰ. 개요 및 필요성

### 1-1. 두 패턴만으로는 부족한 상황

| 패턴 단독 사용 | 문제점 |
|:---|:---|
| Mediator 단독 | 이벤트 구독자 추가 시 Mediator 코드 수정 필요 → OCP 위반 가능성 |
| Observer 단독 | Subject가 많아지면 구독 관계가 복잡해져 M:N 문제 재발 |

두 패턴을 결합하면 각자의 단점을 상호 보완한다.

### 1-2. 혼합 패턴의 탄생 배경

Node.js의 `EventEmitter`, Spring의 `ApplicationEventPublisher`, Java의 `java.util.concurrent.Flow`는 모두 Mediator와 Observer가 자연스럽게 융합된 구조다.

```
  이벤트 발행자 (Publisher / Colleague)
        │
        │ publish(event)
        ▼
  ┌─────────────────────────────────────┐
  │  EventBus / EventChannel (Mediator) │
  │  (이벤트 채널 역할)                 │
  │  subscribers: Map<EventType, List>  │
  └────────────────┬────────────────────┘
                   │ notify()
          ┌────────┼────────┐
          ▼        ▼        ▼
      Handler1  Handler2  Handler3
      (Observer) (Observer) (Observer)
```

📢 **섹션 요약 비유**: Mediator는 방송국 송신탑, Observer는 TV 수신기. 방송국은 누가 TV를 켜든 관심 없이 신호를 보내고, TV는 원하는 채널만 수신한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 혼합 패턴 전체 구조

```
  ┌──────────────────────────────────────────────────────────┐
  │             EventBus (Mediator + Observable)             │
  │                                                          │
  │  subscribers: HashMap<String, List<EventListener>>       │
  │                                                          │
  │  subscribe(eventType, listener)   ← Observer 등록        │
  │  unsubscribe(eventType, listener) ← Observer 해제        │
  │  publish(eventType, data)         ← 이벤트 발행          │
  │    → subscribers.get(type)                               │
  │       .forEach(l → l.onEvent(data))                      │
  └──────────────────────────────────────────────────────────┘
           ▲                        │
           │ publish()              │ onEvent()
  ┌────────────────┐     ┌──────────────────────────────┐
  │  OrderService  │     │  Subscriber A (이메일 발송)  │
  │  (Colleague /  │     │  Subscriber B (재고 차감)    │
  │   Publisher)   │     │  Subscriber C (통계 집계)    │
  └────────────────┘     └──────────────────────────────┘
```

### 2-2. Node.js EventEmitter 분석

```javascript
// Node.js EventEmitter = Mediator + Observer 혼합
const EventEmitter = require('events');
const bus = new EventEmitter();

// Observer 등록 (subscribe)
bus.on('order.created', (order) => {
    sendConfirmationEmail(order);      // Subscriber A
});

bus.on('order.created', (order) => {
    decreaseInventory(order);         // Subscriber B
});

// Mediator를 통한 이벤트 발행
orderService.createOrder(data);
bus.emit('order.created', newOrder); // 모든 구독자에게 전파
```

### 2-3. Spring ApplicationEventPublisher 구조

```
  Spring Framework의 ApplicationContext = Mediator

  ┌─────────────────────────────────────────────────────┐
  │  ApplicationContext (Mediator)                      │
  │  ┌──────────────────────────────────────────────┐   │
  │  │  ApplicationEventMulticaster                 │   │
  │  │  → 등록된 모든 EventListener에게 이벤트 전파 │   │
  │  └──────────────────────────────────────────────┘   │
  └─────────────────────────────────────────────────────┘
         ▲                      │
         │ publishEvent()       │ @EventListener
  ┌────────────┐    ┌──────────────────────────────┐
  │ Publisher  │    │  @EventListener EmailService │
  │ Component  │    │  @EventListener StockService │
  └────────────┘    └──────────────────────────────┘

  // Publisher
  applicationEventPublisher.publishEvent(new OrderCreatedEvent(order));

  // Subscriber (자동 등록)
  @EventListener
  public void onOrderCreated(OrderCreatedEvent event) { ... }
```

📢 **섹션 요약 비유**: Spring의 EventPublisher는 "사내 방송 시스템" — 방송을 틀면 방송을 구독한 모든 부서에 동시에 전달되고, 새 부서가 생겨도 방송 장비를 바꿀 필요 없다.

---

## Ⅲ. 비교 및 연결

### 3-1. 단독 패턴 vs 혼합 패턴 비교

| 항목 | Mediator 단독 | Observer 단독 | 혼합 패턴 |
|:---|:---|:---|:---|
| **확장성** | 구독자 추가 시 코드 수정 | Subject 증가 시 복잡 | ✅ 구독자 추가 무수정 |
| **중앙 제어** | ✅ 강력 | ❌ 분산 | ✅ 이벤트 채널 중앙화 |
| **Loose Coupling** | 중간 | ✅ 강력 | ✅ 강력 |
| **이벤트 필터링** | 어려움 | 가능 | ✅ 이벤트 타입별 라우팅 |
| **디버깅** | 용이 | 어려움 | 중간 (로깅 필요) |
| **구현 복잡도** | 낮음 | 낮음 | 중간 |

### 3-2. 유사 패턴과의 관계

| 패턴 | 관계 |
|:---|:---|
| Event Sourcing | 혼합 패턴의 이벤트를 영속화(Persist)하면 Event Sourcing |
| CQRS | 이벤트 버스가 Command/Query를 라우팅 |
| Message Broker (Kafka, RabbitMQ) | 분산 환경에서의 Mediator-Observer 혼합 |
| Publish-Subscribe (Pub-Sub) | 혼합 패턴과 거의 동일한 Enterprise 패턴 |

📢 **섹션 요약 비유**: Mediator 단독은 "백화점 안내데스크(모든 안내를 직접)", Observer 단독은 "게시판(붙여두면 알아서 봄)", 혼합 패턴은 "스마트 푸시 알림(관련 사람에게만 자동 전송)".

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. God Object 방지 전략

```
  ❌ 나쁜 설계: 모든 로직이 Mediator 안에
  
  ConcreteMediator {
      onOrderCreated(order) {
          emailService.send(...)    // 이메일 로직
          inventoryService.dec(...) // 재고 로직
          analyticsService.log(...) // 통계 로직
          // Mediator가 모든 로직을 직접 실행 → God Object
      }
  }

  ✅ 좋은 설계: Mediator는 라우팅, 로직은 Subscriber에
  
  EventBus {
      publish(event) {
          subscribers.forEach(s → s.onEvent(event));
          // 단순 전파만, 로직 없음
      }
  }
  
  // 각 Subscriber가 자신의 로직을 독립적으로 처리
  EmailSubscriber.onEvent(event) { ... }
  StockSubscriber.onEvent(event) { ... }
```

### 4-2. 비동기 이벤트 처리 (Async Event Handling)

```
  동기 방식 (기본):
  Publisher → EventBus → Subscriber A (완료 대기)
                       → Subscriber B (완료 대기)
  → 전체 처리 시간 = A + B

  비동기 방식 (Spring @Async):
  Publisher → EventBus → Subscriber A (Thread Pool에서 실행)
                       → Subscriber B (Thread Pool에서 실행)
  → 전체 처리 시간 ≈ max(A, B)
```

Spring에서 `@Async + @EventListener` 조합으로 비동기 Mediator-Observer를 구현한다.

### 4-3. 기술사 서술 포인트

- 두 패턴 혼합의 **시너지**: Mediator의 중앙화 + Observer의 Loose Coupling (느슨한 결합)
- God Object 위험 언급과 **라우팅 전용 Mediator** 설계 원칙 제시
- Spring ApplicationEventPublisher, Node.js EventEmitter 등 **실제 프레임워크 사례** 언급

📢 **섹션 요약 비유**: 좋은 혼합 패턴 설계는 "유능한 이벤트 기획사" — 손님(Publisher)에게서 이벤트를 받아 참가자(Subscriber)들에게 알리되, 이벤트 진행은 각자가 한다.

---

## Ⅴ. 기대효과 및 결론

### 5-1. 기대 효과

| 효과 | 설명 |
|:---|:---|
| OCP 완전 달성 | 새 구독자 추가 시 기존 코드 무수정 |
| 도메인 이벤트 지원 | DDD (Domain-Driven Design)의 도메인 이벤트 구현 |
| 비동기 처리 자연스러운 통합 | @Async 어노테이션만으로 비동기 전환 |
| 서비스 간 결합도 최소화 | 마이크로서비스(MSA)로의 자연스러운 확장 경로 |

### 5-2. 주의사항

- **이벤트 순서 보장 어려움**: 비동기 환경에서 이벤트 처리 순서가 섞일 수 있음
- **이벤트 손실 가능성**: 구독자가 이벤트를 놓쳤을 때 재처리 메커니즘 필요 (Event Sourcing 연계)
- **순환 이벤트 위험**: A가 이벤트 발행 → B가 수신 → B가 다시 A를 트리거하는 순환 방지 필요

### 5-3. 결론

Mediator-Observer 혼합 아키텍처는 현대 이벤트 기반 시스템의 설계 표준이다. Node.js EventEmitter, Spring ApplicationEventPublisher, Kafka의 Pub-Sub 모두 이 혼합 원리를 기반으로 한다. God Object 방지와 이벤트 손실 방지 메커니즘을 함께 설계해야 완성도 높은 시스템이 된다.

📢 **섹션 요약 비유**: 혼합 패턴이 완성된 시스템은 "스마트시티의 신호 시스템" — 중앙에서 관제하되(Mediator), 각 신호등은 자율적으로 동작한다(Observer).

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Mediator Pattern | 중앙 집중 통신 패턴 |
| 상위 개념 | Observer Pattern | 이벤트 구독 패턴 |
| 연관 개념 | EventEmitter (Node.js) | 혼합 패턴의 JS 구현 |
| 연관 개념 | ApplicationEventPublisher (Spring) | 혼합 패턴의 Java 구현 |
| 연관 개념 | Pub-Sub Pattern | Enterprise 패턴의 동일 개념 |
| 연관 개념 | God Object (Anti-Pattern) | 피해야 할 설계 함정 |

### 👶 어린이를 위한 3줄 비유 설명

- 유튜브 채널(Mediator)에 구독자(Observer)들이 알림을 신청해요.
- 새 영상(이벤트)이 올라오면 구독자들에게 자동으로 알림이 가요.
- 채널은 구독자가 몇 명인지 몰라도 되고, 구독자도 다른 구독자를 몰라도 돼요!
