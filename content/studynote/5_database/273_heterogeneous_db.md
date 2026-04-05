+++
title = "273. 동종 분산 DB vs 이종 (Heterogeneous) 분산 DB 통합"
+++

# 273. 동종 분산 DB vs 이종 (Heterogeneous) 분산 DB 통합

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 동종 분산 DB는 동일한 DBMS 간의 분산이며, 이종 분산 DB는 서로 다른 DBMS 간의 통합으로, 이종 시스템 통합 시スキーマ 매핑과 쿼리 변환이 핵심 과제이다.
> 2. **가치**: 이종 분산 DB 통합은 기존 이기종 시스템을 단일 뷰로 통합하여 데이터 접근 편의성을 높이고, 부분적인 시스템 현대화를 가능하게 한다.
> 3. **융합**: 데이터 통합, ETL, Federated Database, CDC, 데이터 가상화와 밀접하게 연관된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 동종 분산 데이터베이스
동종 분산 데이터베이스(Homogeneous Distributed Database)는 동일한 DBMS(MySQL, PostgreSQL 등)를 사용하는 노드로 구성된 분산 데이터베이스이다. 동일한 스키마, 동일한 SQL，方針相同的 복제 및 장애 복구 메커니즘을 사용하여 통합이 비교적 단순하다.

### 이종 분산 데이터베이스
이종 분산 데이터베이스(Heterogeneous Distributed Database)는 서로 다른 DBMS(Oracle, MySQL, PostgreSQL, MongoDB 등) 간에 구성된 분산 데이터베이스이다. 각 시스템이 다른 스키마, 다른 데이터 모델, 다른 언어를 사용할 수 있어 통합이 복잡하다.

### 필요성
실제 기업 환경에서는 수십 년간 구축된 다양한 DBMS가共存한다. 이를 모두 한 번에 교체하는 것은 불가능하므로, 이종 분산 DB 통합을 통해 기존 시스템을 활용하면서도 단일 인터페이스로 접근할 수 있게 하는 것이 필요하다.

### 비유
동종 분산 DB는 같은メーカーをに乗った複数の車両と같다. 모두 동일한 操作方法으로 움직이며、通讯协议も共通している. 이종 분산 DB는他のメーカーを乗った多个の車両と같다. 操作方法が異なり、通訳가 필요한다.

📢 섹션 요약: 동종 분산 DB는 동일한 시스템으로 구성이 단순하고, 이종 분산 DB는 서로 다른 시스템 통합으로 복잡하지만 기존 자산을 활용할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 동종 vs 이종 분산 DB 구조

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    동종 vs 이종 분산 데이터베이스 구조                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [동종 분산 DB]                                                            │
│                                                                             │
│    ┌─────────────┐                                                         │
│    │  MySQL Node │                                                         │
│    │ (동일 스키마)│                                                         │
│    └──────┬──────┘                                                         │
│           │                                                                  │
│    ┌──────┴──────┐                                                         │
│    │  MySQL Node │                                                         │
│    │ (동일 스키마)│                                                         │
│    └──────┬──────┘                                                         │
│           │                                                                  │
│    ┌──────┴──────┐                                                         │
│    │  MySQL Node │                                                         │
│    │ (동일 스키마)│                                                         │
│    └─────────────┘                                                         │
│                                                                             │
│  ※ 동일 DBMS, 동일 스키마 → 통합 단순                                        │
│                                                                             │
│  [이종 분산 DB]                                                            │
│                                                                             │
│    ┌─────────────┐                                                         │
│    │   Oracle    │                                                         │
│    │ (고객 DB)   │                                                         │
│    └──────┬──────┘                                                         │
│           │                                                                  │
│    ┌──────┴──────┐                                                         │
│    │   MySQL     │                                                         │
│    │ (주문 DB)   │                                                         │
│    └──────┬──────┘                                                         │
│           │                                                                  │
│    ┌──────┴──────┐                                                         │
│    │   MongoDB   │                                                         │
│    │ (로그 DB)   │                                                         │
│    └─────────────┘                                                         │
│                                                                             │
│  ※ 다른 DBMS, 다른 스키마 → 통합 복잡                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 이종 분산 DB 통합 접근법

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    이종 분산 DB 통합 접근법                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. ETL (Extract, Transform, Load)                                         │
│  ─────────────────────────────────────                                     │
│  • 주기적으로 데이터를 추출, 변환, 적재                                      │
│  • 배치 기반, 실시간성 낮음                                                  │
│  • 예: Apache Spark, Apache Airflow, Talend                                │
│                                                                             │
│  2. 데이터 Federated Database                                              │
│  ─────────────────────────────                                             │
│  • 단일 쿼리 인터페이스로 여러 DBMS에 접근                                   │
│  • 물리적 데이터 이동 없이 논리적 통합                                         │
│  • 예: PostgreSQL Foreign Data Wrapper, Oracle Gateway                      │
│                                                                             │
│  3. CDC (Change Data Capture)                                             │
│  ─────────────────────                                                     │
│  • 변경 사항을 실시간으로 포착하여 다른 시스템에 적용                          │
│  • 예: Debezium, Oracle GoldenGate, AWS DMS                                │
│                                                                             │
│  4. 데이터 가상화 (Data Virtualization)                                     │
│  ─────────────────────────────────                                         │
│  • 물리적 데이터 이동 없이 여러 소스를 통합 뷰로 제공                          │
│  • 예: Denodo, Azure Synapse Link, Google Dataplex                        │
│                                                                             │
│  5. 메시징 기반 통합                                                        │
│  ──────────────────                                                       │
│  • 각 시스템이 이벤트/메시지를 발행하고, 중앙 버스가 전달                       │
│  • 예: Apache Kafka, Amazon Kinesis                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 이종 통합 시 핵심 과제

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    이종 분산 DB 통합 시 핵심 과제                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Schema 매핑                                                            │
│  ─────────────                                                              │
│  • 다른 스키마 간 매핑 정의                                                 │
│  • 예: Oracle의 VARCHAR2 ↔ MySQL의 VARCHAR                                 │
│  • 예: 날짜 형식, 숫자 형식 차이                                            │
│                                                                             │
│  2. Query 변환                                                             │
│  ────────────                                                              │
│  • 각 DBMS의 SQL 방언 차이 해결                                             │
│  • 예: LIMIT vs ROWNUM, IF vs DECODE                                      │
│                                                                             │
│  3. 데이터 모델 차이                                                        │
│  ──────────────────                                                       │
│  • 관계형 vs 문서형 vs 키-값 등                                             │
│  • 예: JOIN vs 임베디드 문서                                               │
│                                                                             │
│  4. 트랜잭션 관리                                                          │
│  ─────────────────                                                       │
│  • 분산 환경에서 이기종 간 트랜잭션 원자성 보장 어려움                         │
│  • Saga 패턴 등 결과적 일관성 기반 접근법 필요                               │
│                                                                             │
│  5. 성능 최적화                                                            │
│  ────────────                                                              │
│  • 네트워크 지연, 데이터 이동 비용 고려                                        │
│  • 조건 푸시다운( Predicate Pushdown)로 최적화                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]**
이종 분산 DB 통합의 핵심 과제는 서로 다른 시스템 간의 차이를 해결하는 것이다.
스키마 매핑, 쿼리 변환, 데이터 모델 차이, 트랜잭션 관리, 성능 최적화 등이
있으며, 이러한 과제를 해결하기 위한 다양한 통합 접근법(ETL, Federated DB, CDC,
데이터 가상화, 메시징)이 있다.

📢 섹션 요약: 이종 분산 DB 통합 시 스키마 매핑, 쿼리 변환, 데이터 모델 차이, 트랜잭션 관리, 성능 최적화 등의 과제가 있으며, ETL, Federated DB, CDC, 데이터 가상화 등의 접근법이 있다.

---

## Ⅲ. 구현 및 실무 응용 (Implementation & Practice)

### PostgreSQL Foreign Data Wrapper

```sql
-- PostgreSQL: Oracle을 접근하는 Foreign Data Wrapper

-- Oracle FDW 설치
CREATE EXTENSION oracle_fdw;

-- 외부 서버 정의
CREATE SERVER oracle_server FOREIGN DATA WRAPPER oracle_fdw
    OPTIONS (dbserver '//oracle_host:1521/ORCL');

-- 사용자 매핑
CREATE USER MAPPING FOR postgres SERVER oracle_server
    OPTIONS (USER 'oracle_user', PASSWORD 'oracle_password');

-- 외부 테이블 정의
CREATE FOREIGN TABLE oracle_customers (
    customer_id INTEGER,
    customer_name VARCHAR(100),
    email VARCHAR(100)
) SERVER oracle_server
    OPTIONS (TABLE 'CUSTOMERS');

-- 이제 PostgreSQL에서 Oracle 데이터를查询 가능
SELECT * FROM oracle_customers WHERE customer_id > 100;
```

### Apache Kafka를 활용한 이종 통합

```java
// Kafka Connect를活用した이종 DB 통합

// MySQL → Elasticsearch 복제 설정 (connect-distributed.properties)

{
  "name": "mysql-to-elasticsearch",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "tasks.max": "3",
    "topics": "mysql-customers",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "connection.url": "http://elasticsearch:9200",
    "type.name": "_doc",
    "key.ignore": "false"
  }
}

// Debezium CDC 설정 (MySQL 변경 사항 캡처)
{
  "name": "mysql-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "dbz123",
    "database.server.id": "184054",
    "topic.prefix": "mysql",
    "table.include.list": "mydb.customers",
    "schema.history.internal.kafka.bootstrap.servers": "kafka:9092"
  }
}
```

### 데이터 가상화 플랫폼

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    데이터 가상화 플랫폼 예시                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Denodo Platform:                                                           │
│  ─────────────────                                                         │
│  • 다양한 DBMS, 파일, API 등을 통합 뷰로 제공                                 │
│  • SELECT * FROM customers_optimized_view (내부적으로 여러 소스 JOIN)        │
│                                                                             │
│  Azure Synapse Link:                                                       │
│  ───────────────────                                                       │
│  • Cosmos DB와 Synapse SQL 간 실시간 통합                                    │
│  • HTAP 시나리오 지원                                                       │
│                                                                             │
│  Google Dataplex:                                                          │
│  ─────────────────                                                         │
│  • 다양한 스토리지(BigQuery, GCS, etc) 통합 데이터 관리                     │
│  • 데이터 레이크 및 데이터 메시 아키텍처 지원                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

📢 섹션 요약: PostgreSQL FDW, Kafka Connect, Denodo, Azure Synapse Link 등 다양한 도구로 이종 DB 통합을 구현할 수 있다.

---

## Ⅳ. 결론

동종 분산 DB는 동일 시스템으로 통합이 단순하고, 이종 분산 DB는 기존 자산을 활용하면서도 단일 뷰를 제공할 수 있다. 이종 통합 시 스키마 매핑, 쿼리 변환, 트랜잭션 관리 등의 과제가 있으므로, ETL, Federated DB, CDC, 데이터 가상화 등의 적절한 접근법을 선택해야 한다.

📢 섹션 요약: 이종 분산 DB 통합은 복잡하지만 ETL, Federated DB, CDC, 데이터 가상화 등으로 실현 가능하며, 시스템 요구사항에 맞는 접근법을 선택해야 한다.

---

## 핵심 인사이트 ASCII 다이어그램 (Concept Map)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│        Homogeneous vs Heterogeneous Distributed DB Concept Map               │
│                                                                             │
│  ┌──────────────────┐         ┌──────────────────┐                      │
│  │   Homogeneous    │         │  Heterogeneous   │                      │
│  │      DDBS        │         │      DDBS        │                      │
│  │  (동종 분산 DB)  │         │  (이종 분산 DB)  │                      │
│  └────────┬─────────┘         └────────┬─────────┘                      │
│           │                            │                                   │
│           ▼                            ▼                                   │
│  ┌──────────────────┐         ┌──────────────────┐                      │
│  │ 동일 DBMS       │         │ 다른 DBMS        │                      │
│  │ 동일 스키마       │         │ 다른 스키마       │                      │
│  │ 통합 단순        │         │ 통합 복잡        │                      │
│  └──────────────────┘         └────────┬─────────┘                      │
│                                        │                                   │
│                                        ▼                                   │
│                              ┌──────────────────┐                        │
│                              │ 통합 접근법       │                        │
│                              │ ETL | FDW | CDC  │                        │
│                              │ 데이터 가상화     │                        │
│                              └──────────────────┘                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 참고
- 동종 분산 DB는 동일한 DBMS 간 통합으로 구성이 단순하다.
- 이종 분산 DB는 서로 다른 DBMS 간 통합으로 스키마 매핑, 쿼리 변환이 필요하다.
- ETL, Federated DB, CDC, 데이터 가상화 등의 통합 접근법이 있다.
- 이종 통합 시 트랜잭션 관리와 성능 최적화가 핵심 과제이다.
