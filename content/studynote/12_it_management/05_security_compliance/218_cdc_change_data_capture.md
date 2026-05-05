+++
weight = 218
title = "218. CDC (Change Data Capture)"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++
## 0. 핵심 인사이트

> **핵심**: CDC(Change Data Capture, 변경 데이터 캡처)는 데이터베이스의 변경사항(INSERT/UPDATE/DELETE)을 실시간으로 감지·캡처하여 다운스트림 시스템에 전달하는 기술로, 전체 테이블 스캔(Full Table Scan) 없이 증분(Incremental) 변경 데이터만 효율적으로 동기화한다.
> 2. **가치**: 로그 기반(Log-based) CDC는 DB 트랜잭션 로그(Redo Log, WAL, Binlog)를 읽어 운영 DB에 추가 부하 없이 밀리초 수준의 실시간 동기화를 달성하며, Debezium 오픈소스는 MySQL/PostgreSQL/Oracle/MongoDB 등 주요 DB를 Kafka와 연결하는 표준 솔루션이 됐다.
> 3. **판단 포인트**: 운영 DB와 DW/데이터 레이크 간 실시간 동기화, 무중단 이기종 DB 마이그레이션, 마이크로서비스 간 이벤트 기반 데이터 공유가 필요할 때 CDC가 최적이며, 방식 선택 시 **로그 기반 > 트리거 기반 > 쿼리 기반** 순으로 운영 부하가 낮다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 1.1 배치 ETL의 한계와 CDC 등장
전통적인 배치 ETL은 매 시간 또는 매일 "마지막 업데이트 타임스탬프 이후" 레코드를 전체 스캔하여 DW에 동기화한다. 이 방식은 운영 DB에 주기적으로 집중 부하를 주고, DELETE된 레코드를 감지하지 못하며, 최대 수 시간의 데이터 지연이 발생한다. 특히 금융 이상거래 탐지, 실시간 재고 관리, 마이크로서비스 이벤트 연동에는 적합하지 않다.

CDC는 DB 내부의 트랜잭션 로그를 실시간으로 읽어 변경 이벤트를 생성한다. INSERT는 "after" 이미지, DELETE는 "before" 이미지, UPDATE는 "before + after" 이미지를 캡처하여, 어떤 레코드가 어떻게 바뀌었는지 정확히 전달한다.

### 1.2 CDC의 3대 구현 방식

| 방식 | 원리 | 장점 | 단점 |
|:---|:---|:---|:---|
| **로그 기반 (Log-based)** | DB 트랜잭션 로그(Binlog, WAL, Redo Log) 읽기 | 운영 부하 없음, 밀리초 실시간 | DB 로그 접근 권한 필요 |
| **트리거 기반 (Trigger-based)** | DB 트리거로 변경사항을 별도 테이블에 기록 | 모든 DB 지원 | 쓰기 부하 증가, 트리거 관리 복잡 |
| **쿼리 기반 (Query-based)** | 타임스탬프/시퀀스 컬럼 주기적 폴링 | 구현 간단 | DELETE 감지 불가, 부하 발생, 지연 |

📢 **섹션 요약 비유**: CDC 방식 비교는 뉴스 수집 방법과 같다. 로그 기반은 뉴스통신 실시간 수신(부하 없이 즉각), 트리거 기반은 기자가 사건마다 메모를 남기는 방식(즉각이지만 기자 부담 증가), 쿼리 기반은 매 시간 뉴스 사이트를 직접 방문하는 방식(간단하지만 지연과 부하 발생)이다.

---

## 2. 구성요소

### 2.1 Debezium + Kafka CDC 아키텍처

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

### 2.2 CDC 이벤트 구조 (Debezium 예시)

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

### 2.3 DB별 로그 기반 CDC 메커니즘

| 데이터베이스 | 트랜잭션 로그 | Debezium 커넥터 |
|:---|:---|:---|
| **MySQL** | Binary Log (Binlog) | debezium-connector-mysql |
| **PostgreSQL** | WAL (Write-Ahead Log) + Replication Slot | debezium-connector-postgres |
| **Oracle** | Redo Log + LogMiner | debezium-connector-oracle |
| **MongoDB** | Oplog (Operations Log) | debezium-connector-mongodb |
| **SQL Server** | CDC Tables (내장 기능) | debezium-connector-sqlserver |

📢 **섹션 요약 비유**: 로그 기반 CDC는 블랙박스 영상 복사와 같다. 차량(운영 DB) 주행 중 블랙박스(트랜잭션 로그)가 모든 순간을 기록하고, 별도 분석가(Debezium)가 블랙박스 영상을 복사해 분석한다. 차량 운전(운영 DB 처리)에는 전혀 영향을 주지 않는다.

---

## 3. 구조 및 동작 원리

### 3.1 CDC vs 배치 ETL vs 스트리밍 비교

| 항목 | 배치 ETL | CDC | 스트리밍 API |
|:---|:---|:---|:---|
| **데이터 신선도** | 분~시간 지연 | 밀리초 수준 | 밀리초 수준 |
| **DELETE 감지** | ❌ 불가 | ✅ 가능 | ✅ 가능 |
| **운영 DB 부하** | 높음 (주기적 풀 스캔) | 낮음 (로그 읽기) | 없음 (Push 방식) |
| **구현 복잡도** | 낮음 | 중간 | 높음 |
| **스키마 변경 대응** | 어려움 | 자동 감지 | 수동 처리 |
| **사용 사례** | 일배치 리포팅 | 실시간 동기화 | 이벤트 기반 서비스 |

### 3.2 CDC 활용 패턴

| 패턴 | 설명 | 예시 |
|:---|:---|:---|
| **DB → DW 실시간 동기화** | 운영 DB 변경 즉시 DW 반영 | 주문 DB → Snowflake 실시간 |
| **DB → 검색 엔진 동기화** | RDBMS → Elasticsearch 실시간 | 상품 DB → 검색 색인 |
| **DB → Cache 동기화** | DB 변경 즉시 Redis 캐시 갱신 | 사용자 세션·프로필 캐시 |
| **이기종 DB 마이그레이션** | 서비스 중단 없는 DB 전환 | Oracle → PostgreSQL 무중단 |
| **마이크로서비스 이벤트** | DB 변경을 이벤트로 서비스 간 공유 | Outbox Pattern |

📢 **섹션 요약 비유**: CDC + Kafka 조합은 실시간 번역 이어폰과 같다. 한국어(원천 DB)로 말하는 즉시 Debezium(번역기)이 영어(Kafka 이벤트)로 변환하고, 여러 외국인(다운스트림 소비자)이 동시에 실시간으로 듣는다. 강연자(운영 DB)는 평소와 동일하게 한국어로 말하기만 하면 된다.

---

## 4. 비교 및 트레이드오프

### 4.1 Outbox Pattern (트랜잭셔널 아웃박스)

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

### 4.2 이기종 DB 무중단 마이그레이션 전략

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

### 4.3 기술사 핵심 출제 포인트
- **CDC 3대 방식 비교**: 로그 기반·트리거 기반·쿼리 기반의 장단점
- **Debezium 동작 원리**: 트랜잭션 로그 읽기 → Kafka 이벤트 발행 흐름
- **Outbox Pattern**: 마이크로서비스 원자적 이벤트 발행
- **무중단 이기종 DB 마이그레이션**: CDC 기반 점진적 전환 전략

📢 **섹션 요약 비유**: Outbox Pattern은 우편함을 활용한 확실한 배달 방법이다. "편지 작성(DB 저장)"과 "우편함에 넣기(Outbox 테이블 삽입)"를 한 번에 처리하고, 집배원(Debezium CDC)이 우편함을 보고 편지를 가져가 발송한다. 직접 우체국에 뛰어가다 넘어지는(API 직접 호출 실패) 위험이 없다.

---

## 5. 실무 적용 및 최적화 기법

### 5.1 CDC 도입 효과

| 효과 | 내용 |
|:---|:---|
| **실시간 데이터 동기화** | 배치 대비 지연 시간 수 시간 → 밀리초로 단축 |
| **운영 DB 부하 감소** | 배치 풀 스캔 제거, 로그 읽기로 DB 부하 최소화 |
| **완전한 변경 감지** | DELETE·UPDATE·INSERT 모두 실시간 캡처 |
| **무중단 마이그레이션** | 서비스 중단 없는 이기종 DB 전환 |
| **이벤트 기반 통합** | 마이크로서비스 간 느슨한 결합(Loose Coupling) |
| **감사 로그 자동화** | 모든 DB 변경 이력이 이벤트 스트림으로 자동 기록 |

### 5.2 한계 및 고려사항
로그 기반 CDC는 DB 슈퍼유저 권한 또는 복제 슬롯(Replication Slot)이 필요하며, 스키마 변경(DDL) 이벤트 처리가 복잡하다. 또한 대량의 CDC 이벤트가 발생하는 환경에서 Kafka 컨슈머가 따라가지 못하는 **소비자 지연(Consumer Lag)** 문제가 발생할 수 있다. 스키마 레지스트리(Schema Registry)와의 통합으로 스키마 변경을 체계적으로 관리하는 것이 필수다.

📢 **섹션 요약 비유**: CDC는 실시간 CCTV 모니터링과 같다. 건물(운영 DB) 안에서 일어나는 모든 움직임(변경)을 CCTV(트랜잭션 로그)가 기록하고, 경비실(Debezium)이 실시간으로 화면을 보며 이상 징후를 즉시 알린다. 건물 주민(운영 DB 사용자)은 CCTV 존재를 신경 쓰지 않고 일상생활을 한다.

---

### 📌 관련 개념 맵

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

---

### 👶 어린이를 위한 3줄 비유 설명

1. CDC는 CCTV 자동 알림 시스템이야. 가게(운영 DB)에서 물건이 팔리거나(INSERT), 바뀌거나(UPDATE), 없어질(DELETE) 때마다 자동으로 본부(다운스트림 시스템)에 알림이 가. 가게 주인(DB 운영팀)은 아무것도 하지 않아도 돼.
2. 로그 기반 CDC는 CCTV 녹화 파일을 복사해서 분석하는 방식이야. 가게 직원(DB 운영)은 평소처럼 일하고, 별도 분석가(Debezium)가 녹화 파일만 복사해 어떤 일이 있었는지 파악해.
3. Outbox Pattern은 중요한 편지를 보낼 때 우편함에 넣는 것과 동시에 복사본을 캐비닛(Outbox 테이블)에 보관하는 방식이야. 편지가 분실돼도 캐비닛을 보고 다시 보낼 수 있어서 확실히 전달되지.
