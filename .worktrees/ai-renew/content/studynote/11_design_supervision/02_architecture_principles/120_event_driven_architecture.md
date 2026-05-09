+++
weight = 120
title = "이벤트 주도 아키텍처 (EDA, Event-Driven Architecture)"
date = "2026-03-04"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- **비동기 결합 해소**: 생산자와 소비자가 직접 호출하지 않고 이벤트를 통해 느슨하게 결합되는 아키텍처 스타일이다.
- **실시간 반응성**: 시스템 상태 변경을 실시간 스트림으로 처리하여 높은 탄력성과 확장성을 보장한다.
- **복잡도 관리 필수**: 이벤트 순서 보장, 결과적 일관성(Eventual Consistency) 및 추적의 어려움을 극복해야 한다.

### Ⅰ. 개요 (Context & Background)
이벤트 주도 아키텍처(EDA)는 시스템 내외부의 상태 변화(Event)를 감지하고, 이를 비동기적으로 전달하여 처리하는 분산 아키텍처 모델이다. 전통적인 요청-응답(Request-Response) 방식의 동기 호출 병목을 해결하기 위해 도입되었으며, 특히 마이크로서비스(MSA) 환경에서 서비스 간 결합도를 최소화하는 핵심 전략으로 활용된다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
EDA는 크게 **Event Producer(생성자)**, **Event Channel(브로커)**, **Event Consumer(소비자)**의 3단 구조로 이루어진다.

```text
[ Producer ] ----(Event)----> [ Event Broker ] ----(Subscription)----> [ Consumer A ]
 (State Change)              (Kafka/RabbitMQ)                         [ Consumer B ]
                                     |
                                     +----(Routing/Filtering)----> [ Consumer C ]

<Bilingual ASCII Diagram: EDA Flow>
- Event Producer: 상태 변화 감지 및 메시지 발행 (Publish)
- Event Broker: 메시지 저장, 라우팅 및 신뢰성 전송 (Ingress/Egress)
- Event Consumer: 메시지 수신 및 비즈니스 로직 실행 (Subscribe/Process)
```

핵심 원리는 **관심사의 분리(Separation of Concerns)**이다. 생성자는 누가 이벤트를 받는지 알 필요가 없으며(Fire and Forget), 브로커가 이를 보존하고 전달하는 책임을 진다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 요청-응답 (Request-Response) | 이벤트 주도 (Event-Driven) |
| :--- | :--- | :--- |
| **통신 방식** | 동기 (Synchronous) | 비동기 (Asynchronous) |
| **결합도** | 강결합 (Direct Call) | 느슨한 결합 (Indirect) |
| **확장성** | 상대적 낮음 (Blocking) | 매우 높음 (Elasticity) |
| **일관성** | 즉시 일관성 (ACID) | 결과적 일관성 (BASE) |
| **복잡도** | 낮음 (직관적 흐름) | 높음 (추적/디버깅 어려움) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **감리적 관점**: EDA 도입 시 **메시지 전달 보장 수준(At-least-once, Exactly-once)**에 대한 감리가 필수적이다. 메시지 중복 처리(Idempotency)가 코드 레벨에서 구현되었는지 확인해야 한다.
- **설계 전략**: 데이터의 정합성보다 시스템의 가용성이 중요한 대규모 트래픽 처리 시스템(Push 알림, 실시간 주문 체계)에 우선 적용을 권고한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
EDA는 클라우드 네이티브 환경에서 서버리스(FaaS)와 결합하여 자원 효율을 극대화한다. 미래의 아키텍처는 서버 간 직접 통신을 지양하고, 신뢰할 수 있는 메시지 버스를 통한 이벤트 스트리밍 기반의 자율적 분산 시스템으로 진화할 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 소프트웨어 아키텍처 스타일, 분산 시스템
- **하위 개념**: Pub/Sub, 메시지 브로커(Kafka), 서버리스, 리액티브 프로그래밍
- **연관 개념**: MSA, CQRS, 이벤트 소싱, 결과적 일관성

### 👶 어린이를 위한 3줄 비유 설명
- **요청-응답**: 엄마에게 "배고파요"라고 말하고 밥이 나올 때까지 앞에서 계속 기다리는 것과 같아요.
- **이벤트 주도**: 식당에서 번호표를 받고 자리에 앉아 놀고 있으면, 내 번호가 전광판에 뜰 때 음식을 가지러 가는 것과 같아요.
- **장점**: 기다리는 동안 다른 일을 할 수 있어서 훨씬 효율적이에요!
