+++
weight = 217
title = "217. CDC (Change Data Capture) 빈로그 데이터 변경 캡처 Debezium"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: CDC(Change Data Capture)는 소스 데이터베이스에서 발생하는 INSERT·UPDATE·DELETE 변경 사항을 실시간으로 감지·캡처하여 다른 시스템에 전달하는 기술로, 전통적인 전체 테이블 복사(Full Dump) 대비 네트워크·DB 부하를 획기적으로 줄인다.
> **비유**: 여러 공정이 연결된 생산 라인처럼, 앞단의 입력 품질과 중간 단계의 흐름 제어가 최종 결과를 좌우하는 구조와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

CDC (Change Data Capture) 빈로그 데이터 변경 캡처 Debezium은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

| 방법 | 설명 | 문제점 |
|:---|:---|:---|
| **전체 복사 (Full Dump)** | 주기적으로 전체 테이블 복사 | 시간·네트워크 비용 과다, 지연 큼 |
| **타임스탬프 기반** | `updated_at > 마지막 실행 시각` 쿼리 | DELETE 감지 불가, 인덱스 필요 |
| **트리거 기반** | DB 트리거로 변경 로그 테이블 기록 | 트리거 DB 부하, 스키마 수정 필요 |
| **로그 기반 CDC** | DB 복제 로그 직접 파싱 | 추가 부하 없음, DELETE 포함 전체 변경 캡처 |

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```
레거시 방식 (전체 복사):
  소스 DB ──[매시간 전체 SELECT]──► DW / 타겟 시스템
  - 100만 건 테이블에서 변경된 100건 찾기 위해 100만 건 스캔
  - 잦은 배치로 DB 부하 급증

CDC 방식 (로그 기반):
  소스 DB ──[변경된 100건만 캡처]──► Kafka ──► DW / 타겟
  - DB 복제 로그에서 변경 이벤트만 읽음
  - 소스 DB에 추가 부하 없음
  - 실시간 (수 초 이내)
```

---

## 3. 구조 및 원리

**핵심 조건**: CDC (Change Data Capture) 빈로그 데이터 변경 캡처 Debezium은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 패턴 | 설명 | 도구 |
|:---|:---|:---|
| **실시간 DW 동기화** | OLTP→DW 실시간 복제 | Debezium + Kafka + dbt |
| **캐시 무효화** | DB 변경 시 Redis 캐시 자동 업데이트 | Debezium + Redis Sink |
| **이벤트 소싱** | DB 변경을 도메인 이벤트로 발행 | Debezium + Kafka + MSA |
| **검색 인덱스 동기화** | DB 변경을 Elasticsearch에 즉시 반영 | Debezium + ES Sink |

| 방법 | 지연 | DB 부하 | DELETE 처리 | 스키마 변경 |
|:---|:---|:---|:---|:---|
| **로그 기반 CDC** | < 1초 | 없음 | 완벽 | 별도 처리 필요 |
| **DMS (AWS Database Migration Service)** | 초 단위 | 낮음 | 완벽 | 자동 처리 |
| **JDBC 폴링** | 분 단위 | 중간 | 불가 | 자동 처리 |
| **DB 링크** | 즉시 | 높음 | 가능 | 수동 |

---

## 4. 비교 및 연결

| 항목 | 주의점 | 해법 |
|:---|:---|:---|
| **WAL 슬롯 지연** | 컨슈머가 느리면 WAL 슬롯 쌓임 → DB 디스크 풀 | 컨슈머 처리량 모니터링 |
| **스키마 변화** | DDL 변경 시 이벤트 구조 불일치 | Schema Registry + Avro 사용 |
| **초기 스냅샷** | 첫 실행 시 전체 테이블 스냅샷 (부하) | 오프 피크 타임 스냅샷 |
| **토픽 파티셔닝** | 동일 키 변경 순서 보장 필요 | 기본키 기반 파티셔닝 |

```
1단계: DB 설정
   MySQL: binlog_format=ROW, binlog_row_image=FULL
   PgSQL: wal_level=logical, max_replication_slots=5

2단계: Debezium 커넥터 배포
   Kafka Connect에 Debezium Connector 설정 JSON 배포
   소스 DB 연결 정보, 테이블 화이트리스트 설정

3단계: Kafka 토픽 확인
   dbserver.mydb.orders 토픽에 이벤트 수신 확인

4단계: Sink Connector 배포
   타겟 시스템(DW, Redis, ES)에 Sink Connector 설정
```

---

## 5. 실무 적용 및 판단

| 효과 | 내용 |
|:---|:---|
| **실시간성** | 배치 대비 지연 시간 시간 단위 → 초 단위로 단축 |
| **DB 부하 감소** | 폴링 쿼리 제거로 소스 DB CPU 20~50% 절감 |
| **데이터 일관성** | DELETE 포함 모든 변경 100% 캡처 |
| **아키텍처 단순화** | 여러 시스템에 동시 전파로 N개 배치 파이프라인 통합 |

기술사 답안에서는 **"CDC 3가지 방식의 비교와 로그 기반이 유일한 프로덕션 표준인 이유"**를 명확히 서술하고, Debezium의 이벤트 구조(op·before·after)를 활용한 Kafka 기반 실시간 동기화 파이프라인을 ASCII 다이어그램으로 표현하면 차별화된 답안이 된다.

| 방식 | 동작 원리 | DB 부하 | DELETE 감지 | 실시간성 |
|:---|:---|:---|:---|:---|
| **트리거 기반** | 트리거 → 변경 로그 테이블 | 높음 | 가능 | 가능 |
| **타임스탬프 기반** | `WHERE updated_at > ?` | 중간 | 불가 | 준실시간 |
| **로그 기반** | DB 복제 로그 파싱 | 거의 없음 | 가능 | 실시간 |

MySQL의 Binlog(Binary Log)는 MySQL 복제(Replication)를 위해 모든 변경 사항을 기록하는 로그다.

```
MySQL 서버
├── InnoDB 스토리지
│   └── 실제 데이터 변경
└── Binlog (Binary Log)
    ├── ROW 이벤트: 행 수준 변경 상세 기록
    │   INSERT: 새 행의 모든 컬럼값
    │   UPDATE: 이전 행값(before) + 이후 행값(after)
    │   DELETE: 삭제된 행의 모든 컬럼값
    └── 이진 형식으로 순서 기록
```

**Binlog 형식 설정**:
```sql
-- MySQL Binlog 형식을 ROW로 설정 (CDC 필수)
SET GLOBAL binlog_format = 'ROW';
SET GLOBAL binlog_row_image = 'FULL';  -- 변경 전후 전체 컬럼 기록
```

PostgreSQL은 WAL(Write-Ahead Log)을 통해 모든 변경을 기록한다. CDC는 논리 복제(Logical Replication) 슬롯을 통해 WAL을 읽는다.

```
PostgreSQL 서버
├── WAL (Write-Ahead Log)
│   └── 모든 변경 작업의 순서 기록
└── 논리 복제 슬롯 (Logical Replication Slot)
    └── Debezium이 이 슬롯을 통해 변경 스트림 구독
```

Debezium은 Red Hat이 개발한 오픈소스 CDC 플랫폼으로, Kafka Connect Source Connector로 동작한다.

```
┌─────────────────────────────────────────────────────────────┐
│                 CDC 파이프라인 전체 흐름                       │
│                                                             │
│  ┌──────────────┐    ┌───────────────────────────────────┐  │
│  │ MySQL/PgSQL  │    │        Kafka Connect               │  │
│  │  소스 DB     │    │  ┌─────────────────────────────┐  │  │
│  │              │    │  │   Debezium Source Connector  │  │  │
│  │  Binlog/WAL  │───►│  │  DB변경 → Kafka 이벤트 변환  │  │  │
│  │              │    │  └─────────────────────────────┘  │  │
│  └──────────────┘    └───────────────────┬───────────────┘  │
│                                          │                  │
│                       ┌──────────────────▼──────────────┐   │
│                       │         Apache Kafka             │   │
│                       │  토픽: dbserver.mydb.orders      │   │
│                       │  { op: "u", before: {...},       │   │
│                       │    after: {...}, ts_ms: ... }    │   │
│                       └──────────────────┬──────────────┘   │
│                                          │                  │
│              ┌───────────────────────────┼──────────────┐   │
│              ▼                           ▼              ▼   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐ │
│  │  DW (Snowflake)  │  │  Elasticsearch   │  │  캐시 DB  │ │
│  │  (Sink Connector)│  │  (검색 인덱스)   │  │  (Redis)  │ │
│  └──────────────────┘  └──────────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────┘
```

```json
{
  "op": "u",        // 연산 유형: c(create), u(update), d(delete), r(read/snapshot)
  "ts_ms": 1714000000000,
  "before": {       // 변경 전 행 데이터
    "order_id": 1001,
    "status": "pending",
    "amount": 5000
  },
  "after": {        // 변경 후 행 데이터
    "order_id": 1001,
    "status": "shipped",
    "amount": 5000
  },
  "source": {
    "db": "mydb",
    "table": "orders",
    "pos": 12345678  // Binlog 위치
  }
}
```

---

## 6. 기대효과 및 결론

기술사 답안에서는 **"CDC 3가지 방식의 비교와 로그 기반이 유일한 프로덕션 표준인 이유"**를 명확히 서술하고, Debezium의 이벤트 구조(op·before·after)를 활용한 Kafka 기반 실시간 동기화 파이프라인을 ASCII 다이어그램으로 표현하면 차별화된 답안이 된다.

CDC (Change Data Capture) 빈로그 데이터 변경 캡처 Debezium의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
배치 ETL (주기적 전체 복사)
    │
    ▼
CDC: 변경분만 실시간 캡처
    ├─► 로그 기반: MySQL Binlog · PostgreSQL WAL
    └─► Debezium: Kafka Connect 기반 CDC 커넥터
    │
    ▼
Outbox 패턴: 트랜잭션 보장 이벤트 발행
    │
    ▼
실시간 OLTP → OLAP 동기화 · 캐시 무효화
```
2. MySQL Binlog는 도서관의 '대출 기록지'야 — 어떤 책이 언제 누가 빌려갔고, 반납됐는지 순서대로 적혀 있어.
3. Debezium은 이 기록지를 읽어서 Kafka라는 방송 시스템으로 변환하는 '방송 번역사'야 — 그러면 여러 시스템이 동시에 소식을 들을 수 있어!

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| CDC 구현체 | Debezium | Kafka Connect 기반 오픈소스 CDC |
| MySQL 로그 | Binlog (Binary Log) | MySQL 복제 로그, CDC 소스 |
| PostgreSQL 로그 | WAL (Write-Ahead Log) | PgSQL 논리 복제 로그 |
| 이벤트 버스 | Apache Kafka | CDC 이벤트 중개 플랫폼 |
| 스키마 관리 | Schema Registry | Avro/Protobuf 스키마 버전 관리 |
| 연관 패턴 | 이벤트 소싱 (Event Sourcing) | DB 변경을 도메인 이벤트로 발행 |
