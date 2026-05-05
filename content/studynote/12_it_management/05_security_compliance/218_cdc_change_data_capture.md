+++
weight = 218
title = "218. 변경 데이터 캡처 (CDC, Change Data Capture) 데이터베이스 실시간 마이그레이션 연동망"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++

## 0. 핵심 인사이트

> **핵심**: 변경 데이터 캡처 (CDC, Change Data Capture) 데이터베이스 실시간 마이그레이션 연동망의 본질은 변경 데이터 캡처 (CDC, Change Data Capture) 데이터베이스 실시간 마이그레이션 연동망의 목적·구성·운영 기준을 명확히 설명하는 주제를 비즈니스 가치, 통제, 실행 관점에서 일관되게 연결하는 데 있다.
> **비유**: 전략과 운영 사이의 간극을 메우는 조정 메커니즘과 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

전통적인 배치 ETL은 매 시간 또는 매일 "마지막 업데이트 타임스탬프 이후" 레코드를 전체 스캔하여 DW에 동기화한다. 이 방식은 운영 DB에 주기적으로 집중 부하를 주고, DELETE된 레코드를 감지하지 못하며, 최대 수 시간의 데이터 지연이 발생한다. 특히 금융 이상거래 탐지, 실시간 재고 관리, 마이크로서비스 이벤트 연동에는 적합하지 않다.

CDC는 DB 내부의 트랜잭션 로그를 실시간으로 읽어 변경 이벤트를 생성한다. INSERT는 "after" 이미지, DELETE는 "before" 이미지, UPDATE는 "before + after" 이미지를 캡처하여, 어떤 레코드가 어떻게 바뀌었는지 정확히 전달한다.

| 방식 | 원리 | 장점 | 단점 |
|:---|:---|:---|:---|
| **로그 기반 (Log-based)** | DB 트랜잭션 로그(Binlog, WAL, Redo Log) 읽기 | 운영 부하 없음, 밀리초 실시간 | DB 로그 접근 권한 필요 |
| **트리거 기반 (Trigger-based)** | DB 트리거로 변경사항을 별도 테이블에 기록 | 모든 DB 지원 | 쓰기 부하 증가, 트리거 관리 복잡 |
| **쿼리 기반 (Query-based)** | 타임스탬프/시퀀스 컬럼 주기적 폴링 | 구현 간단 | DELETE 감지 불가, 부하 발생, 지연 |

---

## 2. 구성요소

```
┌─────────────────────────────────────────────────────────────┐
│           CDC Architecture with Debezium + Kafka            │
│                                                             │
│  Source DB                Debezium           Kafka          │
│  ┌──────────────────┐    ┌──────────┐    ┌────────────┐    │
│  │  MySQL / Postgres │    │          │    │  Topic:    │    │
│  │  ┌──────────────┐│    │ Connector│    │  db.orders │    │
│  │  │ Binlog / WAL ││───►│          │───►│ ┌────────┐ │    │
│  │  │ (변경 로그)   ││    │ (변경 이벤│    │ │INSERT  │ │    │
│  │  └──────────────┘│    │  트 생성) │    │ │UPDATE  │ │    │
│  │  ┌──────────────┐│    └──────────┘    │ │DELETE  │ │    │
│  │  │ orders table ││                    │ └────────┘ │    │
│  │  │ [row changes]││                    └─────┬──────┘    │
│  │  └──────────────┘│                          │           │
│  └──────────────────┘                          │           │
│                                                │           │
│  Downstream Consumers (다운스트림 소비자)        │           │
│  ┌────────────┐  ┌──────────┐  ┌────────────┐ │           │
│  │ Data       │  │ Search   │  │ Microservice│ │           │
│  │ Warehouse  │◄─┤ Engine   │◄─┤ Cache Sync │◄┘           │
│  │ (실시간 DW)│  │(Elastic) │  │(Redis Sync)│             │
│  └────────────┘  └──────────┘  └────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

```json
{
  "op": "u",          // 연산 유형: c(create), u(update), d(delete), r(read/snapshot)
  "before": {
    "order_id": 1001,
    "status": "PENDING",
    "amount": 50000
  },
  "after": {
    "order_id": 1001,
    "status": "CONFIRMED",
    "amount": 50000
  },
  "source": {
    "db": "ecommerce",
    "table": "orders",
    "ts_ms": 1713700000000,
    "pos": "mysql-bin.000003:1234"  // Binlog 위치
  }
}
```

| 데이터베이스 | 트랜잭션 로그 | Debezium 커넥터 |
|:---|:---|:---|
| **MySQL** | Binary Log (Binlog) | debezium-connector-mysql |
| **PostgreSQL** | WAL (Write-Ahead Log) + Replication Slot | debezium-connector-postgres |
| **Oracle** | Redo Log + LogMiner | debezium-connector-oracle |
| **MongoDB** | Oplog (Operations Log) | debezium-connector-mongodb |
| **SQL Server** | CDC Tables (내장 기능) | debezium-connector-sqlserver |

---

## 3. 구조 및 원리

| 항목 | 배치 ETL | CDC | 스트리밍 API |
|:---|:---|:---|:---|
| **데이터 신선도** | 분~시간 지연 | 밀리초 수준 | 밀리초 수준 |
| **DELETE 감지** | ❌ 불가 | ✅ 가능 | ✅ 가능 |
| **운영 DB 부하** | 높음 (주기적 풀 스캔) | 낮음 (로그 읽기) | 없음 (Push 방식) |
| **구현 복잡도** | 낮음 | 중간 | 높음 |
| **스키마 변경 대응** | 어려움 | 자동 감지 | 수동 처리 |
| **사용 사례** | 일배치 리포팅 | 실시간 동기화 | 이벤트 기반 서비스 |

| 패턴 | 설명 | 예시 |
|:---|:---|:---|
| **DB → DW 실시간 동기화** | 운영 DB 변경 즉시 DW 반영 | 주문 DB → Snowflake 실시간 |
| **DB → 검색 엔진 동기화** | RDBMS → Elasticsearch 실시간 | 상품 DB → 검색 색인 |
| **DB → Cache 동기화** | DB 변경 즉시 Redis 캐시 갱신 | 사용자 세션·프로필 캐시 |
| **이기종 DB 마이그레이션** | 서비스 중단 없는 DB 전환 | Oracle → PostgreSQL 무중단 |
| **마이크로서비스 이벤트** | DB 변경을 이벤트로 서비스 간 공유 | Outbox Pattern |

---

## 4. 비교 및 연결

마이크로서비스에서 DB 저장과 이벤트 발행의 **원자성(Atomicity)** 보장이 어려운 문제를 해결하는 패턴이다. DB 트랜잭션 내에 이벤트를 Outbox 테이블에 함께 저장하고, CDC가 Outbox 테이블 변경을 감지하여 Kafka에 발행한다.

```
[주문 서비스]
BEGIN TRANSACTION;
  INSERT INTO orders (id, status, amount) VALUES (1001, 'CREATED', 50000);
  INSERT INTO outbox (topic, payload) VALUES ('orders', '{"orderId":1001,...}');  -- CDC 감지 대상
COMMIT;
↓
[Debezium CDC]
outbox 테이블 변경 감지 → Kafka orders 토픽 발행
```

```
단계 1: CDC 설정
  Oracle (원본) → Debezium → Kafka → PostgreSQL (목적지) 동기화 시작

단계 2: 초기 스냅샷
  Oracle 전체 데이터 → PostgreSQL 초기 적재
  이후 변경사항은 CDC로 실시간 동기화

단계 3: 이중 쓰기 검증
  Oracle, PostgreSQL 동시 운영 → 데이터 정합성 검증

단계 4: 트래픽 전환
  읽기 트래픽 점진적으로 PostgreSQL로 전환 (카나리 배포)
  쓰기 트래픽 전환 후 Oracle CDC 종료
```

- **CDC 3대 방식 비교**: 로그 기반·트리거 기반·쿼리 기반의 장단점
- **Debezium 동작 원리**: 트랜잭션 로그 읽기 → Kafka 이벤트 발행 흐름
- **Outbox Pattern**: 마이크로서비스 원자적 이벤트 발행
- **무중단 이기종 DB 마이그레이션**: CDC 기반 점진적 전환 전략

---

## 5. 실무 적용 및 판단

| 효과 | 내용 |
|:---|:---|
| **실시간 데이터 동기화** | 배치 대비 지연 시간 수 시간 → 밀리초로 단축 |
| **운영 DB 부하 감소** | 배치 풀 스캔 제거, 로그 읽기로 DB 부하 최소화 |
| **완전한 변경 감지** | DELETE·UPDATE·INSERT 모두 실시간 캡처 |
| **무중단 마이그레이션** | 서비스 중단 없는 이기종 DB 전환 |
| **이벤트 기반 통합** | 마이크로서비스 간 느슨한 결합(Loose Coupling) |
| **감사 로그 자동화** | 모든 DB 변경 이력이 이벤트 스트림으로 자동 기록 |

로그 기반 CDC는 DB 슈퍼유저 권한 또는 복제 슬롯(Replication Slot)이 필요하며, 스키마 변경(DDL) 이벤트 처리가 복잡하다. 또한 대량의 CDC 이벤트가 발생하는 환경에서 Kafka 컨슈머가 따라가지 못하는 **소비자 지연(Consumer Lag)** 문제가 발생할 수 있다. 스키마 레지스트리(Schema Registry)와의 통합으로 스키마 변경을 체계적으로 관리하는 것이 필수다.

---

## 6. 기대효과 및 결론

변경 데이터 캡처 (CDC, Change Data Capture) 데이터베이스 실시간 마이그레이션 연동망를 올바르게 적용하면 의사결정의 일관성, 운영의 재현성, 통제의 추적성이 동시에 향상된다. 즉 “누가 무엇을 왜 했는가”가 남기 때문에 조직이 커질수록 효과가 커진다.

다만 변경 데이터 캡처 (CDC, Change Data Capture) 데이터베이스 실시간 마이그레이션 연동망는 문서만 잘 만들어도 성공하는 영역이 아니다. 정의와 실행이 분리되면 형식주의가 되고, 자동화만 앞서면 통제 목적이 사라진다. 따라서 표준화와 민첩성, 통제와 생산성 사이의 균형이 항상 필요하다.

향후에는 정책 코드화(Policy as Code), 실시간 관측성(Observability), AI 기반 이상 탐지와 의사결정 지원이 결합되면서 관리 체계가 더 자동화되고 증거 중심으로 진화할 가능성이 크다. 결론적으로 핵심은 도구가 아니라 기준선이며, 기준선이 명확할 때만 자동화와 확장이 의미를 가진다.

---

## 7. 발전 흐름도

```text
개별 대응
    ↓
프로세스 표준화
    ↓
변경 데이터 캡처 (CDC, Change Data Capture) 데이터베이스 실시간 마이그레이션 연동망 정착
    ↓
지표 기반 통제
    ↓
정책 코드화·AI 보조
```

---

## 8. 관련 개념 맵

| 개념 | 설명 | 연관 키워드 |
|:---|:---|:---|
| CDC (Change Data Capture) | DB 변경사항 실시간 캡처 기술 | 증분 동기화, 실시간 ETL |
| Debezium | Kafka 기반 오픈소스 CDC 솔루션 | MySQL, PostgreSQL, Kafka |
| Binlog | MySQL 트랜잭션 로그 | 복제, PITR, CDC |
| WAL (Write-Ahead Log) | PostgreSQL 트랜잭션 로그 | Replication Slot, CDC |
| Outbox Pattern | 트랜잭셔널 아웃박스로 원자적 이벤트 발행 | 마이크로서비스, Saga |
| Exactly-once | CDC 이벤트 중복·유실 없는 전달 | Kafka, 트랜잭션 |
| Consumer Lag | 소비자가 생산자 속도를 못 따라가는 상황 | Kafka 모니터링 |
| Schema Registry | CDC 이벤트 스키마 중앙 관리 | Avro, 호환성 |
