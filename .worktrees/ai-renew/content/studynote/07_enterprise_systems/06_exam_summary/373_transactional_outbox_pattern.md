+++
weight = 373
title = "373. 트랜잭셔널 아웃박스 비동기 메시지 보장 (Transactional Outbox Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 트랜잭셔널 아웃박스(Transactional Outbox) 패턴은 DB 변경과 메시지 발행을 같은 로컬 트랜잭션으로 묶어, DB 저장은 성공했지만 메시지 발행이 실패하는 이중 쓰기(Dual Write) 문제를 근본적으로 해결한다.
> 2. **가치**: 비즈니스 데이터 변경과 이벤트 발행의 원자성(Atomicity)을 로컬 DB 트랜잭션으로 보장하여, Kafka 등 메시지 브로커 장애 시에도 이벤트가 유실되지 않는 최소 1회(At-least-once) 전달을 보장한다.
> 3. **판단 포인트**: 아웃박스 테이블 폴링 방식(Polling)과 CDC(Change Data Capture) 방식 중 DB 부하·실시간성·인프라 복잡도를 고려하여 선택해야 하며, 중복 전달을 수신 측에서 멱등성으로 처리해야 한다.

## Ⅰ. 개요 및 필요성

MSA에서 서비스가 DB를 업데이트하고 이벤트를 메시지 브로커(Kafka)로 발행하는 코드를 작성할 때, 두 작업이 원자적으로 처리되지 않는 이중 쓰기 문제가 발생한다.

시나리오 A: DB 저장 성공 → Kafka 발행 중 서버 재시작 → 이벤트 유실
시나리오 B: Kafka 발행 성공 → DB 저장 실패 → 이벤트는 있지만 데이터 없음

이 문제를 해결하기 위해 Chris Richardson이 제안한 Outbox 패턴은 "메시지를 업무 DB의 Outbox 테이블에 같은 트랜잭션으로 저장 → 별도 릴레이 프로세스가 Outbox에서 읽어 메시지 브로커로 발행"하는 2단계 접근이다.

📢 **섹션 요약 비유**: 트랜잭셔널 아웃박스는 우체통처럼, 편지(메시지)를 우체통(Outbox 테이블)에 넣는 것과 물건 구매(DB 저장)를 동시에 하고, 우편배달부(Message Relay)가 나중에 가져가는 방식이다.

## Ⅱ. 아키텍처 및 핵심 원리

### 트랜잭셔널 아웃박스 흐름

```
비즈니스 서비스
  ├── BEGIN TRANSACTION
  │     ├── 비즈니스 DB 테이블 UPDATE/INSERT
  │     └── Outbox 테이블 INSERT
  │           {event_type, payload, status=PENDING}
  └── COMMIT TRANSACTION  ← 원자적 처리

                   ↓ (별도 프로세스)
           Message Relay (릴레이)
           ├── Outbox 테이블 폴링 (PENDING 조회)
           ├── Kafka/RabbitMQ 발행
           └── status = PUBLISHED 업데이트

                   ↓
           메시지 소비자 서비스
           (중복 방지: 이벤트 ID 기반 멱등 처리)
```

### 아웃박스 테이블 설계

```sql
CREATE TABLE outbox_events (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type  VARCHAR(100) NOT NULL,  -- Order, Payment
    aggregate_id    VARCHAR(100) NOT NULL,  -- 도메인 객체 ID
    event_type      VARCHAR(100) NOT NULL,  -- OrderCreated
    payload         JSONB        NOT NULL,  -- 이벤트 데이터
    status          VARCHAR(20)  DEFAULT 'PENDING',
    created_at      TIMESTAMP    DEFAULT NOW(),
    published_at    TIMESTAMP
);
CREATE INDEX idx_outbox_status ON outbox_events(status, created_at);
```

### CDC (Change Data Capture) 방식

```
Debezium CDC:
  PostgreSQL WAL (Write-Ahead Log)
       ↓ 변경 이벤트 캡처
  Debezium Connector
       ↓ 자동 Kafka 발행
  Kafka Topic
  
  장점: 폴링 불필요, 실시간 처리
  단점: Debezium 인프라 복잡도
```

📢 **섹션 요약 비유**: CDC 방식은 감시 카메라처럼, DB 변경 로그(WAL)를 실시간으로 감시하여 변경 즉시 메시지를 발행하는 자동 감지 방식이다.

## Ⅲ. 비교 및 연결

### 폴링 vs CDC 방식 비교

| 구분 | Outbox 폴링 (Polling) | CDC (Debezium) |
|:---|:---|:---|
| 구현 복잡도 | 낮음 | 높음 (Debezium 설정) |
| DB 부하 | 폴링 쿼리 주기적 발생 | WAL 읽기 (최소 부하) |
| 실시간성 | 폴링 주기 지연 (초~분) | 거의 실시간 (밀리초) |
| DB 의존성 | 모든 DB 적용 가능 | WAL 지원 DB (PostgreSQL 권장) |
| 인프라 | Message Relay 서비스 | Kafka Connect + Debezium |

### Outbox vs Saga의 조합

Saga 패턴에서 각 로컬 트랜잭션 후 이벤트를 발행해야 할 때, Outbox 패턴을 적용하면 Saga 이벤트 유실 없이 최소 1회 전달을 보장할 수 있다.

📢 **섹션 요약 비유**: 폴링과 CDC의 차이는 메시지함을 주기적으로 확인하는 것(폴링)과 새 메시지가 도착하면 알림이 오는 것(CDC)의 차이다.

## Ⅳ. 실무 적용 및 기술사 판단

### 구현 시 핵심 고려사항

1. **멱등성(Idempotency)**: 소비자는 같은 이벤트가 2번 이상 도달해도 동일한 결과 보장
2. **Outbox 정리**: PUBLISHED 된 이벤트는 주기적으로 삭제 (테이블 비대화 방지)
3. **재시도 정책**: 발행 실패 시 지수 백오프 재시도 + Dead Letter Queue
4. **모니터링**: PENDING 상태 이벤트가 임계값 초과 시 알림 (발행 지연 탐지)

### 선택 기준

```
소규모 서비스, 빠른 구현 → 폴링 방식 (Spring Scheduled + Outbox)
대규모 트래픽, 실시간 요구 → Debezium CDC
Kafka 없는 환경 → Amazon SQS + Outbox 폴링
```

📢 **섹션 요약 비유**: Outbox 테이블 정리는 발송 완료된 편지함 비우기처럼, 이미 보낸(PUBLISHED) 메시지를 주기적으로 삭제해야 창고(DB)가 넘치지 않는다.

## Ⅴ. 기대효과 및 결론

트랜잭셔널 아웃박스 패턴 적용으로 ①DB 저장과 메시지 발행의 원자성 보장, ②메시지 유실(at-most-once) 위험 제거, ③분산 트랜잭션(2PC) 없이 이벤트 기반 통합 신뢰성 확보, ④시스템 장애 후 자동 메시지 재발행 가능 등의 효과를 거둔다.

**한계**: 폴링 방식은 DB에 추가 부하를 주며, CDC는 인프라 복잡도가 증가한다. 또한 최소 1회 전달(At-least-once) 보장이므로 중복 메시지 처리(소비자 멱등성)는 반드시 소비자 측에서 구현해야 한다.

📢 **섹션 요약 비유**: At-least-once 보장은 중요 서류 등기 우편처럼, "최소 한 번은 전달"을 보장하지만 서명(멱등성)이 있어야 중복 수령을 방지할 수 있다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Saga 패턴 | 연계 | Saga 이벤트 발행의 원자성 보장 |
| 이벤트 소싱 | 연계 | 이벤트 스토어 → 외부 발행의 신뢰성 보장 |
| CDC (Debezium) | 구현 방식 | WAL 기반 실시간 이벤트 캡처·발행 |
| Kafka | 메시지 브로커 | Outbox에서 발행되는 이벤트의 목적지 |
| 멱등성 | 필수 요건 | At-least-once 중복 처리 방지 |

### 👶 어린이를 위한 3줄 비유 설명

1. Outbox 패턴은 일기장 + 우체통처럼, 일기(DB 업데이트)와 편지 봉투(Outbox 테이블)를 동시에 작성해두면, 우편배달부(릴레이)가 나중에 안전하게 배달해요.
2. 이렇게 하면 "일기는 썼는데 편지가 사라진" 사고(메시지 유실)가 절대 일어나지 않아요.
3. 가끔 편지가 두 번 배달되더라도(중복), 받는 사람(소비자)이 "이미 받은 것!"이라고 표시해두면(멱등성) 문제없어요.
