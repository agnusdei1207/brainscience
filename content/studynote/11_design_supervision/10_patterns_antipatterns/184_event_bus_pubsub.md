+++
weight = 184
title = "184. 이벤트 버스 / 발행-구독 패턴 (Event Bus / Publish-Subscribe Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 퍼블리시/서브스크라이브 (Publish/Subscribe) 패턴은 이벤트 발행자(Publisher)와 구독자(Subscriber) 사이에 브로커(Broker)를 두어 완전한 결합도 제거(Decoupling)를 달성하는 비동기 통신 구조다.
> 2. **가치**: Publisher는 누가 구독하는지 모르고, Subscriber는 누가 발행하는지 모른다 — 이 "무지(Ignorance)"가 마이크로서비스 간 독립적 배포와 확장을 가능하게 한다.
> 3. **판단 포인트**: Observer 패턴과의 결정적 차이는 브로커의 존재다. Observer는 발행자가 구독자를 직접 알고 호출하지만, Pub/Sub은 브로커를 통해 완전히 분리된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 강결합 통신의 문제

서비스 A가 서비스 B, C, D를 직접 호출하면 다음 문제가 생긴다.

```
[강결합 구조 문제]
     Service A
     │   │   │
     │   │   └──► Service D (배포 중단 시 A도 영향)
     │   └──────► Service C (버전 변경 시 A 수정)
     └──────────► Service B (일시 장애 시 A 실패)

문제점:
- 단일 책임 위반: A가 B, C, D 모두 알아야 함
- 장애 전파: D 장애 → A 타임아웃
- 확장 어려움: 새 구독자 E 추가 시 A 코드 수정
```

### Pub/Sub 패턴의 해결책

```
[Pub/Sub 구조]
Service A (Publisher)
     │
     │ 이벤트 발행
     ▼
  [Message Broker]  ← 이벤트 라우팅
  (Kafka, RabbitMQ)
     │
     ├──► Service B (Subscriber)
     ├──► Service C (Subscriber)
     └──► Service D (Subscriber)

장점:
- A는 B, C, D를 모름
- B, C, D는 독립적으로 처리
- E가 추가되어도 A 수정 불필요
```

📢 **섹션 요약 비유**: 신문사(Publisher)는 독자(Subscriber)가 몇 명인지, 누구인지 모른다. 우체국(Broker)이 구독자 목록을 관리하고 신문을 배달한다. 독자가 늘어도 신문사는 그냥 인쇄하면 된다.

---

## 2. 구성요소

### 이벤트 버스 vs 메시지 브로커 구조 비교

```
[이벤트 버스 (In-Process)]
┌─────────────────────────────────────────────┐
│             Application Process              │
│                                             │
│  Publisher ──► EventBus ──► Subscriber A   │
│                    │                         │
│                    └──────► Subscriber B    │
│                                             │
│  (Spring ApplicationEventPublisher 등)       │
└─────────────────────────────────────────────┘

[메시지 브로커 (Cross-Process)]
┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  Service A       │     │  Kafka / MQ     │     │  Service B       │
│  (Publisher)     │────►│  (Broker)       │────►│  (Subscriber)    │
│                  │     │  Topic/Queue    │     │                  │
└──────────────────┘     └─────────────────┘     └──────────────────┘
```

### Apache Kafka 토픽 구조

```
Topic: "order-events"
┌────────────────────────────────────────────────────────┐
│  Partition 0: [Event1][Event3][Event5][Event7]...      │
│  Partition 1: [Event2][Event4][Event6][Event8]...      │
│  Partition 2: [Event9][Event10][Event11]...            │
└────────────────────────────────────────────────────────┘
         │                      │
         ▼                      ▼
  Consumer Group A       Consumer Group B
  (재고 서비스 구독)       (알림 서비스 구독)
  ├── Consumer 1          ├── Consumer 1
  └── Consumer 2          └── Consumer 2
  (독립적으로 처리)        (독립적으로 처리)
```

### 핵심 개념

| 개념 | 설명 | Kafka 용어 |
|:---|:---|:---|
| **Publisher (발행자)** | 이벤트를 생성하여 브로커에 전송 | Producer |
| **Subscriber (구독자)** | 특정 토픽의 이벤트를 수신하여 처리 | Consumer |
| **Broker (중간 매개자)** | 이벤트를 수신, 저장, 라우팅 | Kafka Broker |
| **Topic (토픽)** | 이벤트 분류 채널 | Topic |
| **Consumer Group** | 동일 토픽을 공유 처리하는 구독자 그룹 | Consumer Group |

📢 **섹션 요약 비유**: Kafka는 라디오 방송국이다. 방송국(Broker)이 음악(이벤트)을 FM 주파수(Topic)에 방송하면, 라디오(Subscriber)를 가진 누구든 독립적으로 들을 수 있다.

---

## 3. 구조 및 동작 원리

### Pub/Sub vs Observer 패턴 비교

| 비교 항목 | Observer 패턴 | Pub/Sub 패턴 |
|:---|:---|:---|
| **결합도** | 발행자가 구독자 목록을 직접 관리 | 브로커를 통해 완전 분리 |
| **통신 방식** | 동기 (동일 프로세스 내) | 비동기 (브로커 경유) |
| **위치** | 동일 프로세스/JVM 내 | 다른 서비스/프로세스 가능 |
| **구독자 인지** | 발행자가 구독자 목록 알고 있음 | 발행자가 구독자 모름 |
| **필터링** | 발행자가 제어 | 토픽/구독 조건으로 브로커 제어 |
| **메시지 보장** | 없음 (메모리 내) | 영속화, At-Least-Once 등 |
| **대표 예시** | Java 이벤트 리스너, GUI 이벤트 | Kafka, RabbitMQ, Google Pub/Sub |

### 메시지 큐(MQ) 비교

| 브로커 | 모델 | 특징 | 적합 상황 |
|:---|:---|:---|:---|
| **Apache Kafka** | Pub/Sub + Log | 영속 로그, 높은 처리량, 재처리 가능 | 이벤트 스트리밍, 로그 집계 |
| **RabbitMQ** | AMQP 기반 | 복잡한 라우팅, 낮은 지연 | 작업 큐, 마이크로서비스 |
| **AWS SNS/SQS** | Pub/Sub + 큐 | 완전 관리형, AWS 통합 | 클라우드 네이티브 |
| **Google Cloud Pub/Sub** | Pub/Sub | 자동 확장, 전 세계 분산 | GCP 기반 서비스 |
| **Spring ApplicationEvent** | 인프로세스 Pub/Sub | Spring Bean 내부 이벤트 | 동일 애플리케이션 내 |

📢 **섹션 요약 비유**: Observer는 선생님이 학생들을 직접 불러서 공지하는 것이고, Pub/Sub은 학교 방송실(Broker)에서 방송하면 모든 교실(Subscriber)이 자율적으로 듣는 것이다.

---

## 4. 비교 및 트레이드오프

### Spring Boot + Kafka 이벤트 발행/구독 예시

```java
// 이벤트 DTO
public record OrderCreatedEvent(Long orderId, Long userId, BigDecimal amount) {}

// Publisher (주문 서비스)
@Service
public class OrderService {
    private final KafkaTemplate<String, OrderCreatedEvent> kafkaTemplate;

    public void createOrder(OrderRequest req) {
        // 주문 처리 로직...
        Order order = orderRepository.save(new Order(req));

        // 이벤트 발행 (Subscriber가 누구인지 모름)
        kafkaTemplate.send("order-events", new OrderCreatedEvent(
            order.getId(), req.getUserId(), order.getTotalAmount()
        ));
    }
}

// Subscriber 1: 재고 서비스
@Component
public class InventoryEventHandler {
    @KafkaListener(topics = "order-events", groupId = "inventory-service")
    public void handleOrderCreated(OrderCreatedEvent event) {
        inventoryService.decreaseStock(event.orderId());
    }
}

// Subscriber 2: 알림 서비스 (독립적 추가, 주문 서비스 수정 없음)
@Component
public class NotificationEventHandler {
    @KafkaListener(topics = "order-events", groupId = "notification-service")
    public void handleOrderCreated(OrderCreatedEvent event) {
        emailService.sendOrderConfirmation(event.userId(), event.orderId());
    }
}
```

### 이벤트 설계 주의사항

| 주의사항 | 설명 | 해결 |
|:---|:---|:---|
| **이벤트 순서 보장** | 파티션 내에서만 순서 보장 | 동일 키로 동일 파티션 라우팅 |
| **중복 처리 (At-Least-Once)** | 네트워크 오류 시 재발행 | 멱등성(Idempotency) 설계 |
| **이벤트 스키마 진화** | 이벤트 구조 변경 시 하위 호환 | Avro Schema Registry 사용 |
| **Dead Letter Queue** | 처리 실패 이벤트 | DLQ로 격리 후 모니터링 |

📢 **섹션 요약 비유**: 카카오톡 단체 채팅방(Topic)에 메시지를 보내면, 방에 있는 모든 사람(Subscriber)이 읽는다. 보내는 사람은 누가 방에 있는지 몰라도 된다.

---

## 5. 실무 적용 및 최적화 기법

### Pub/Sub 도입 기대효과

| 기대효과 | 구체적 내용 |
|:---|:---|
| **서비스 간 결합도 제거** | 발행자/구독자 독립 배포 가능 |
| **확장성** | 구독자 추가 시 발행자 수정 불필요 |
| **비동기 처리** | 동기 대기 없이 작업 위임 |
| **장애 격리** | 구독자 장애가 발행자에 영향 없음 |
| **이벤트 재처리** | Kafka 로그로 과거 이벤트 재처리 가능 |

Pub/Sub 패턴과 이벤트 버스는 마이크로서비스 아키텍처의 **결합도 해소 핵심 도구**이다. 특히 도메인 이벤트(Domain Event) 중심의 이벤트 소싱(Event Sourcing) 아키텍처와 결합하면 시스템의 확장성과 감사 추적(Audit Trail) 능력이 크게 향상된다.

📢 **섹션 요약 비유**: 각 부처가 대통령에게 직접 보고하는 대신, 국무조정실(Broker)을 통해 안건을 처리하면 대통령(Publisher)은 모든 부처(Subscriber)를 알 필요가 없다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 이벤트 주도 아키텍처 (EDA) | Pub/Sub의 아키텍처 패러다임 |
| 상위 개념 | 마이크로서비스 아키텍처 | Pub/Sub으로 서비스 간 결합 제거 |
| 하위 개념 | Apache Kafka | 대표적 메시지 브로커 구현 |
| 하위 개념 | Topic / Consumer Group | Kafka의 Pub/Sub 핵심 구성 |
| 연관 개념 | Observer 패턴 | 브로커 없는 동기식 Pub/Sub |
| 연관 개념 | 이벤트 소싱 (Event Sourcing) | 이벤트를 상태 변경의 유일한 소스로 |
| 연관 개념 | CQRS | 쓰기 이벤트와 읽기 모델 분리 |

### 👶 어린이를 위한 3줄 비유 설명

- 마트(Publisher)에서 할인 소식(이벤트)을 전단지(Broker)를 통해 뿌리면, 관심 있는 동네 주민(Subscriber)만 자발적으로 마트에 온다.
- 마트는 누가 올지 모르고, 주민도 마트가 할인 결정을 어떻게 했는지 모른다.
- 새 주민이 이사 와서 전단지를 구독해도 마트는 아무것도 바꿀 필요가 없다.
