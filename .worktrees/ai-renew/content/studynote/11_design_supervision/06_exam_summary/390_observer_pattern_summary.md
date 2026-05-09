+++
weight = 390
title = "390. 옵저버 (Observer) 패턴 1:N 상태 구독 알림"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 옵저버 (Observer) 패턴은 객체의 상태 변화를 관심 있는 모든 구독자에게 자동으로 알려주는 1:N 의존 관계 패턴으로, MVC (Model-View-Controller) 패턴의 핵심을 이루고 이벤트 기반 아키텍처의 기반이 된다.
> 2. **가치**: 발행자 (Publisher)가 구독자 (Subscriber)에 대해 알 필요 없어 느슨한 결합을 달성하며, 런타임에 구독자를 동적으로 추가·제거할 수 있다.
> 3. **판단 포인트**: 구독자 수가 많거나 알림 빈도가 높으면 성능 문제가 발생할 수 있고, 순환 알림 (Circular Notification)이 발생하지 않도록 주의해야 한다.

## Ⅰ. 개요 및 필요성

뉴스 구독 서비스: 독자가 신문사를 구독하면, 새 기사가 발행될 때마다 독자에게 알림이 간다. 신문사(발행자)는 구독자 목록만 관리하고, 구독자가 누구인지 알 필요가 없다.

**구성 요소:**
- `Subject` (Publisher): 상태를 가지며 Observer 목록 관리
- `Observer` (Subscriber): 상태 변화 알림을 받는 인터페이스
- `ConcreteSubject`: 실제 상태 관리, 변화 시 notify
- `ConcreteObserver`: 실제 업데이트 처리

📢 **섹션 요약 비유**: 옵저버는 유튜브 채널 구독이다. 채널(Subject)이 새 영상을 올리면 구독자(Observer) 모두에게 자동 알림이 간다.

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌─────────────────────────────────────────────────────────────────┐
│              Observer 패턴 구조                                 │
├─────────────────────────────────────────────────────────────────┤
│  <<interface>> Subject                                          │
│  + attach(Observer)                                             │
│  + detach(Observer)                                             │
│  + notify()                                                     │
│         △                                                       │
│  ConcreteSubject                                                │
│  - state: T                                                     │
│  - observers: List<Observer>                                    │
│  + setState(newState)                                           │
│    → this.state = newState                                      │
│    → notify() → observers.forEach(o → o.update(this))          │
│                                                                 │
│  <<interface>> Observer                                         │
│  + update(subject)                                              │
│         △                                                       │
│  ConcreteObserverA    ConcreteObserverB                         │
│  + update() → 화면 갱신  + update() → 로그 기록                │
└─────────────────────────────────────────────────────────────────┘
```

| 푸시 vs 풀 방식 | 특징 | 장단점 |
|:---|:---|:---|
| 푸시 (Push) | Subject가 변경 데이터를 전달 | 구독자가 필요 없는 데이터도 받을 수 있음 |
| 풀 (Pull) | 구독자가 Subject에서 직접 조회 | 필요한 데이터만 조회, 최신 상태 보장 |

📢 **섹션 요약 비유**: 푸시는 신문이 집으로 배달되는 것, 풀은 독자가 직접 신문사에 가서 가져오는 것이다.

## Ⅲ. 비교 및 연결

| 항목 | 옵저버 (동기) | 이벤트 버스 (비동기) | 메시지 큐 |
|:---|:---|:---|:---|
| 실행 방식 | 동기, 순차 | 비동기 | 비동기, 분산 |
| 결합도 | 느슨 | 매우 느슨 | 완전 분리 |
| 성능 | 단일 프로세스 | 멀티스레드 | 분산 시스템 |
| 예시 | Java Observable | Spring EventBus | Kafka, RabbitMQ |

📢 **섹션 요약 비유**: 옵저버는 같은 건물 내 내선 전화, 이벤트 버스는 사내 메신저, 메시지 큐는 국제 우편이다.

## Ⅳ. 실무 적용 및 기술사 판단

**MVC 패턴과의 연계:**
- Model = Subject (상태 변화 시 notify)
- View = Observer (update 시 화면 갱신)
- Controller는 Model과 View를 연결

**Spring EventBus:**
`@EventListener` + `ApplicationEventPublisher`로 스프링 빈 간 이벤트 발행/구독

**MSA 도메인 이벤트:**
Aggregate 상태 변화 시 도메인 이벤트 발행 → Kafka/RabbitMQ → 다른 서비스 구독 = 분산 옵저버

�� **섹션 요약 비유**: MSA의 이벤트 기반 아키텍처는 옵저버 패턴을 서비스 경계 너머로 확장한 것이다.

## Ⅴ. 기대효과 및 결론

옵저버 패턴은 느슨한 결합과 동적 구독 관리로 확장성 있는 이벤트 기반 시스템의 기반을 제공한다. 기술사 시험에서는 MVC와의 연계, 푸시/풀 방식 비교, MSA 이벤트 기반 아키텍처로의 확장을 명확히 서술해야 한다.

📢 **섹션 요약 비유**: 옵저버 패턴은 단톡방과 같다. 방장(Subject)이 메시지를 보내면 모든 참가자(Observer)가 동시에 받는다.

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF 행동 패턴 | 옵저버의 분류 |
| 연관 패턴 | MVC | 옵저버 패턴 응용 |
| 연관 개념 | 이벤트 기반 아키텍처 | 옵저버의 분산 확장 |
| 연관 개념 | 메시지 큐 (Kafka) | MSA에서의 비동기 옵저버 |

### 👶 어린이를 위한 3줄 비유 설명

- 유튜브에서 좋아하는 채널을 구독하면 새 영상이 올라올 때마다 알림이 와요.
- 채널은 구독자가 누구인지 몰라도 알림을 보낼 수 있어요.
- 언제든지 구독 취소(detach)를 하면 더 이상 알림이 오지 않아요.
