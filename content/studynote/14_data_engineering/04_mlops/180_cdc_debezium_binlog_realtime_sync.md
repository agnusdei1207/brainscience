+++
weight = 180
title = "180. CDC (Change Data Capture) 실시간 로그 캡처 데베지움 (Debezium) 파이프 동기망"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CDC (Change Data Capture, 변경 데이터 캡처)는 데이터베이스의 변경 사항(INSERT/UPDATE/DELETE)을 트랜잭션 로그에서 실시간으로 캡처하여 다른 시스템에 전파하는 기술로, 애플리케이션 부하 없이 데이터 동기화를 구현한다.
> 2. **가치**: Debezium은 MySQL Binlog, PostgreSQL WAL, Oracle Redo Log를 통해 밀리초 단위 지연으로 DW·데이터 레이크·마이크로서비스를 실시간 동기화하며, 기존 ETL 배치의 T+1 지연을 근실시간으로 단축한다.
> 3. **판단 포인트**: 로그 기반(Log-based) CDC가 트리거 기반·쿼리 기반 대비 DB 부하 최소·정확한 삭제 캡처·모든 변경 순서 보장 측면에서 프로덕션 최선책이지만, CDC 활성화를 위한 DB 설정 변경이 필요하다.

---

## Ⅰ. 개요 및 필요성

### 1.1 데이터 동기화 전통 방식의 한계

```
전통 ETL 방식:
  Source DB ──→ (야간 배치) ──→ DW
  
  문제:
  1. T+1 지연: 오늘 거래가 내일 DW에 반영
  2. 전체 테이블 스캔: DB 부하 급증 (새벽 3시 배치)
  3. 삭제(DELETE) 감지 불가: 논리 삭제만 가능
  4. 중간 상태 소실: A→B→C 변경 시 C만 감지
  
CDC 개선:
  Source DB ──→ (로그 스트리밍) ──→ Kafka ──→ DW
  
  장점:
  1. 밀리초 단위 실시간 반영
  2. WAL/Binlog 읽기 → 소스 DB 부하 최소
  3. 물리적 DELETE 완벽 캡처
  4. 모든 중간 변경 이력 보존
```

### 1.2 CDC 구현 방식 비교

| 방식 | 원리 | 장점 | 단점 |
|:---|:---|:---|:---|
| **로그 기반 (Log-based)** | DB 트랜잭션 로그 파싱 | DB 부하 최소, 정확한 순서, DELETE 감지 | DB 설정 변경 필요 |
| **트리거 기반 (Trigger-based)** | DB 트리거로 변경 기록 테이블 작성 | 구현 단순 | DB 부하 증가, 모든 DML에 트리거 |
| **쿼리 기반 (Query-based)** | updated_at 컬럼 주기적 폴링 | 구현 매우 단순 | 폴링 지연, DELETE 감지 불가 |
| **이벤트 기반** | 앱이 직접 이벤트 발행 | 유연함 | 앱 코드 변경, 누락 위험 |

📢 **섹션 요약 비유**: CDC는 창고의 CCTV 시스템이다. 직원이 물건을 옮길 때마다 일일이 보고할 필요 없이(트리거/쿼리 기반 부담), CCTV(트랜잭션 로그)가 자동으로 모든 움직임을 기록한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Debezium 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│              Debezium 기반 CDC 파이프라인                     │
│                                                              │
│  소스 데이터베이스                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  MySQL:       Binary Log (Binlog) ─────────────────┐│   │
│  │  PostgreSQL:  Write-Ahead Log (WAL) ───────────────┤│   │
│  │  Oracle:      Redo Log ────────────────────────────┤│   │
│  │  SQL Server:  Transaction Log ─────────────────────┤│   │
│  │  MongoDB:     Oplog ───────────────────────────────┘│   │
│  └─────────────────────────────────────────────────────┘   │
│                    │                                         │
│                    ▼ Debezium Connector (Kafka Connect)      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Kafka Connect (분산 커넥터 플랫폼)                   │   │
│  │  ├── Source Connector (Debezium)                    │   │
│  │  │   - 로그 파싱 → 이벤트 생성                       │   │
│  │  │   - 스키마 레지스트리 연동 (Avro/JSON)            │   │
│  │  │   - 커서 상태 관리 (오프셋 추적)                  │   │
│  │  └── Sink Connector                                 │   │
│  │      - JDBC Sink (DW 동기화)                        │   │
│  │      - Elasticsearch Sink                           │   │
│  │      - S3 Sink (데이터 레이크)                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                    │                                         │
│                    ▼                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Kafka Topic: dbserver.mydb.orders (테이블별 토픽)    │   │
│  │  이벤트 구조:                                         │   │
│  │  {                                                   │   │
│  │    "before": {"id":1, "amount":100},  ← 변경 전      │   │
│  │    "after":  {"id":1, "amount":150},  ← 변경 후      │   │
│  │    "op":     "u",                     ← 연산 타입     │   │
│  │    "ts_ms":  1705046400000,           ← 타임스탬프    │   │
│  │    "source": {"db":"mydb",                           │   │
│  │               "table":"orders",                     │   │
│  │               "pos": 12345678}       ← 로그 위치     │   │
│  │  }                                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                    │                                         │
│         ┌──────────┼──────────────────────┐                 │
│         ▼          ▼                      ▼                  │
│     Data DW    Elasticsearch         Data Lake (S3)         │
│    (Redshift)  (실시간 검색)           (Parquet/Delta)       │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 DB별 CDC 설정

#### MySQL Binlog 설정

```sql
-- MySQL my.cnf 설정
[mysqld]
server-id         = 1
log_bin           = mysql-bin
binlog_format     = ROW        -- 행 단위 변경 기록 (CDC 필수)
binlog_row_image  = FULL       -- 전체 행 기록 (before/after)
expire_logs_days  = 7          -- 로그 보존 기간

-- Debezium 전용 사용자 권한
CREATE USER 'debezium'@'%' IDENTIFIED BY 'password';
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'debezium'@'%';
FLUSH PRIVILEGES;
```

#### PostgreSQL WAL 설정

```sql
-- postgresql.conf 설정
wal_level = logical           -- 논리적 복제 레벨 (CDC 필수)
max_replication_slots = 4     -- 복제 슬롯 수
max_wal_senders = 4           -- WAL 발신자 수

-- Debezium 전용 복제 슬롯 생성
SELECT pg_create_logical_replication_slot(
  'debezium_slot', 'pgoutput'
);

-- 복제 권한 부여
CREATE ROLE debezium REPLICATION LOGIN;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;
```

### 2.3 Debezium 이벤트 작동 원리

```
이벤트 타입 (op 필드):
  "c" → CREATE (INSERT)
  "u" → UPDATE
  "d" → DELETE
  "r" → READ (초기 스냅샷)

초기 스냅샷 단계:
  1. 소스 테이블 전체 스캔 (op="r")
  2. 현재 Binlog 포지션 기록
  3. 이후 변경은 Binlog에서 실시간 스트리밍

오프셋 관리:
  - Kafka Connect가 처리한 Binlog 위치 추적
  - Kafka Topic "__connect-offsets"에 저장
  - 재시작 시 마지막 처리 위치부터 재시작
```

### 2.4 스키마 레지스트리 통합

```
┌────────────────────────────────────────────────────────┐
│  Confluent Schema Registry + Debezium                  │
│                                                        │
│  Source DB                                             │
│  ├── 컬럼 추가: ALTER TABLE orders ADD COLUMN tax INT  │
│  └── Debezium이 자동 감지 → 스키마 진화 이벤트         │
│                                                        │
│  Schema Registry:                                      │
│  - 이전 스키마 (v1): {id, amount}                     │
│  - 새 스키마 (v2):   {id, amount, tax}                │
│  - 호환성 검사: BACKWARD / FORWARD / FULL             │
│                                                        │
│  Sink Connector:                                       │
│  - 스키마 v2 감지 → DW 테이블에 컬럼 자동 추가        │
│  - 또는 변환 SMT(Single Message Transform)으로 처리   │
└────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Debezium + Kafka는 공장의 실시간 생산 로그 시스템이다. 각 생산 라인(DB 테이블)의 모든 변경이 자동으로 기록(CDC)되어 중앙 모니터링 센터(Kafka)에 실시간 전달된다.

---

## Ⅲ. 비교 및 연결

### 3.1 CDC 도구 비교

| 도구 | 개발사 | 강점 | 지원 DB |
|:---|:---|:---|:---|
| **Debezium** | Red Hat | 오픈소스, Kafka 통합 | MySQL, PG, Oracle, MongoDB, SQL Server |
| **AWS DMS** | AWS | 완전 관리형, 마이그레이션 | 주요 상용 DB |
| **Fivetran** | Fivetran | SaaS, 다양한 커넥터 | 100+ 소스 |
| **Airbyte** | Airbyte | 오픈소스 ELT | 300+ 커넥터 |
| **Maxwell** | Zendesk | MySQL 특화, 경량 | MySQL 전용 |
| **Canal** | Alibaba | MySQL 특화 | MySQL 전용 |

### 3.2 CDC 토폴로지 패턴

```
패턴 1: DB → Debezium → Kafka → 단일 Sink
  가장 단순한 구성, 단일 타겟 동기화

패턴 2: DB → Debezium → Kafka → 멀티 Sink
  ┌──────────────────────────────────────────────┐
  │  MySQL ──→ Debezium ──→ Kafka                │
  │                              │               │
  │               ┌──────────────┼─────────────┐ │
  │               ▼              ▼             ▼  │
  │          Elasticsearch    Redshift        S3  │
  │          (검색 인덱스)    (데이터 웨어하우스) (레이크) │
  └──────────────────────────────────────────────┘

패턴 3: 마이크로서비스 이벤트 스트리밍 (Outbox Pattern)
  ┌──────────────────────────────────────────────┐
  │  Order Service ──→ orders 테이블              │
  │                 └──→ outbox 테이블            │
  │                      │                       │
  │                      ▼ Debezium CDC           │
  │                   Kafka Topic                │
  │                      │                       │
  │          ┌───────────┴──────────────┐        │
  │          ▼                          ▼        │
  │    Inventory Service          Notification   │
  └──────────────────────────────────────────────┘
```

### 3.3 Outbox 패턴 (Transactional Outbox)

```
문제: 마이크로서비스에서 DB 저장 + 이벤트 발행의 원자성 보장
  ┌──────────────────────────────────────────────┐
  │  Without Outbox:                             │
  │  BEGIN TX                                    │
  │  INSERT INTO orders ...    ← 성공             │
  │  COMMIT                    ← 성공             │
  │  Kafka.publish(event)      ← 실패! (이중화)  │
  │  → DB는 저장됐지만 이벤트 누락!              │
  │                                              │
  │  With Outbox Pattern:                        │
  │  BEGIN TX                                    │
  │  INSERT INTO orders ...    ← 성공             │
  │  INSERT INTO outbox        ← 성공 (동일 TX)  │
  │  COMMIT                    ← 원자적 성공      │
  │                                              │
  │  Debezium → outbox 테이블 CDC → Kafka        │
  │  → DB 저장과 이벤트 발행의 원자성 보장!      │
  └──────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Outbox 패턴은 편지를 직접 우체통에 넣는 대신, 일단 서랍에 보관하고(Outbox) 우편부(Debezium)가 주기적으로 수거하는 방식이다. 편지 분실 없이 안전하게 전달된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 Debezium Connector 설정

```json
{
  "name": "mysql-source-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql-host",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "secret",
    "database.server.id": "12345",
    "topic.prefix": "dbserver",
    "database.include.list": "mydb",
    "table.include.list": "mydb.orders,mydb.customers",
    "snapshot.mode": "initial",
    "include.schema.changes": "true",
    
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "false",
    "transforms.unwrap.delete.handling.mode": "rewrite",
    
    "key.converter": "io.confluent.kafka.serializers.KafkaAvroSerializer",
    "value.converter": "io.confluent.kafka.serializers.KafkaAvroSerializer",
    "schema.registry.url": "http://schema-registry:8081"
  }
}
```

### 4.2 CDC 기반 실시간 DW 동기화

```
┌─────────────────────────────────────────────────────────────┐
│     CDC 기반 실시간 DW (Lambda Architecture vs 순수 CDC)     │
│                                                              │
│  전통 Lambda Architecture:                                   │
│  Source DB ──→ 배치(Spark) ──→ DW (T+1)                    │
│           └──→ 스트리밍(Flink) ──→ 집계 테이블 (근실시간)    │
│  → 두 파이프라인 유지 비용 높음                              │
│                                                              │
│  CDC 기반 단순화:                                            │
│  Source DB ──→ Debezium ──→ Kafka ──→ Flink ──→ DW         │
│  → 하나의 파이프라인으로 배치 + 실시간 통합                  │
│  → Kafka의 내구성으로 배치 처리도 가능                       │
│                                                              │
│  실시간 DW 패턴 (Redshift/Snowflake):                        │
│  Kafka JDBC Sink ──→ DW 스테이징 테이블                     │
│  Flink ──→ MERGE INTO DW 타겟 테이블 (UPSERT)               │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 CDC 지연 모니터링

| 지표 | 설명 | 임계값 |
|:---|:---|:---|
| **CDC 레이턴시** | DB 변경 → Kafka 도착 시간 | < 1초 |
| **싱크 레이턴시** | Kafka → 타겟 도착 시간 | < 5초 |
| **로그 위치 지연** | 현재 로그 포지션 vs Debezium 처리 위치 | 모니터링 |
| **Kafka Consumer Lag** | 프로듀서 vs 컨슈머 오프셋 차이 | < 10,000 |
| **커넥터 오류율** | 처리 실패 이벤트 비율 | < 0.01% |

📢 **섹션 요약 비유**: CDC 모니터링은 물 파이프의 유량계와 수압 측정과 같다. 파이프 어디에서 막히거나(지연 급증) 누수(데이터 손실)가 있으면 즉시 알림을 보내야 한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 CDC 도입 효과

| 항목 | 배치 ETL | CDC (Debezium) |
|:---|:---|:---|
| **데이터 지연** | T+1 (수 시간) | < 1초 |
| **소스 DB 부하** | 야간 집중 피크 | 지속적 저부하 |
| **DELETE 감지** | 불가 (논리 삭제만) | 완전 감지 |
| **중간 상태 보존** | 최종 상태만 | 모든 변경 이력 |
| **운영 복잡도** | 단순 | 중간 (Kafka Connect 관리) |

### 5.2 기술사 답안 핵심 논점

1. **로그 기반 CDC의 우위**: WAL/Binlog 파싱은 소스 DB 쿼리 부하 없이 모든 변경(삭제 포함)을 순서대로 캡처 — 트리거·쿼리 기반 대비 완전성과 효율성 모두 우월
2. **Debezium + Kafka 조합**: Kafka Connect 플랫폼이 장애 복구·오프셋 관리·스케일아웃을 자동 처리 — 복잡한 CDC 운영을 표준화
3. **Outbox 패턴**: 마이크로서비스에서 DB 저장과 이벤트 발행의 원자성 보장 — 분산 트랜잭션 없이 이벤트 기반 일관성 달성
4. **실시간 DW 활용**: CDC로 Lambda Architecture의 이중 파이프라인을 단일화하여 운영 비용 절감

📢 **섹션 요약 비유**: CDC는 데이터 세계의 실시간 뉴스 통신사다. 세상에서 일어나는 모든 변화(DB 변경)를 밀리초 단위로 포착하여 전 세계 구독자(Sink 시스템)에게 즉시 전달한다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 기술 | MySQL Binlog | 행 단위 변경 이진 로그 |
| 핵심 기술 | PostgreSQL WAL | 쓰기 전 로그, 논리 복제 기반 |
| CDC 플랫폼 | Debezium | Kafka Connect 기반 오픈소스 CDC |
| 메시지 버스 | Kafka | 변경 이벤트 중계 |
| 이벤트 패턴 | Outbox Pattern | 원자적 DB 저장 + 이벤트 발행 |
| 스키마 관리 | Schema Registry | Avro 스키마 버전화 |
| 쿼리 패턴 | MERGE/UPSERT | CDC 이벤트를 타겟에 반영 |
| 아키텍처 | Kappa Architecture | 배치 없이 스트리밍만으로 처리 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. CDC는 도서관 책 대출 기록이야 — 누가 어떤 책을 가져갔는지, 반납했는지, 새 책이 들어왔는지 모든 변화를 실시간으로 기록해.

### 📈 관련 키워드 및 발전 흐름도

```text
배치 ETL (주기적 전체 복사)
    │
    ▼
CDC (Change Data Capture): 변경분만 실시간 캡처
    ├─► 로그 기반 CDC: MySQL Binlog · PostgreSQL WAL
    └─► 쿼리 기반 CDC: 타임스탬프 비교 (레거시)
    │
    ▼
Debezium (오픈소스 CDC 커넥터)
    └─► DB → Kafka Connect → Kafka Topic → 소비자
    │
    ▼
실시간 동기화 파이프라인
    ├─► OLTP → OLAP 실시간 복제
    ├─► 캐시 무효화 · 검색 인덱스 동기화
    └─► Event Sourcing · 마이크로서비스 데이터 통합
```
2. Debezium은 DB 일기를 읽는 탐정이야 — DB가 매일 쓰는 일기(트랜잭션 로그)를 분석해서 "오늘 주문이 3건 생기고 1건 취소됐어!"를 알려줘.
3. Outbox 패턴은 편지를 직접 우체통에 넣는 대신 서랍에 먼저 보관하는 거야 — 편지 쓰기(DB 저장)와 발송(이벤트 발행)이 한 번에 실패하거나 한 번에 성공해서 편지를 잃어버릴 일이 없어!
