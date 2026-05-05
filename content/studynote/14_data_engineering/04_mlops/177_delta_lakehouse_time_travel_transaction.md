+++
weight = 177
title = "177. 델타 레이크하우스 (Delta Lakehouse) 스냅샷 롤백 Time Travel 트랜잭션"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: Delta Lake는 Parquet 기반 데이터 레이크에 ACID 트랜잭션과 트랜잭션 로그(Delta Log)를 추가하여, 데이터 레이크의 유연성과 데이터 웨어하우스의 신뢰성을 결합한 Lakehouse 아키텍처를 구현한다.
> **비유**: 여러 공정이 연결된 생산 라인처럼, 앞단의 입력 품질과 중간 단계의 흐름 제어가 최종 결과를 좌우하는 구조와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

델타 레이크하우스 (Delta Lakehouse) 스냅샷 롤백 Time Travel 트랜잭션은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
전통적 데이터 레이크 문제:
  ┌────────────────────────────────────────────┐
  │  S3/HDFS 위 Parquet 파일들                  │
  │                                            │
  │  문제 1: 동시성 — 여러 프로세스가 동시에    │
  │         같은 파일 쓰면 → 데이터 오염        │
  │                                            │
  │  문제 2: 원자성 없음 — 10GB 데이터 쓰다    │
  │         중간에 실패 → 반쪽짜리 데이터 잔류  │
  │                                            │
  │  문제 3: 스키마 불일치 — 컬럼 추가 시       │
  │         기존 쿼리 실패                       │
  │                                            │
  │  문제 4: 소형 파일 문제 — 스트리밍 적재 시  │
  │         수천 개 소형 파일 → 쿼리 성능 저하  │
  └────────────────────────────────────────────┘
```

---

## 2. 구성요소

```
┌────────────────────────────────────────────────────────┐
│                  Lakehouse 패러다임                     │
│                                                        │
│  Data Lake (S3/ADLS/GCS)                               │
│  + ACID 트랜잭션 (Delta Log)                           │
│  + 스키마 적용 & 진화                                   │
│  + Time Travel                                         │
│  + 감사 로그                                           │
│  + DML 지원 (UPDATE, DELETE, MERGE)                    │
│  = Lakehouse                                           │
│                                                        │
│  BI 도구    ML 플랫폼   스트리밍   Ad-hoc 쿼리          │
│     │           │          │           │               │
│     └───────────┴──────────┴───────────┘               │
│                       │                                │
│              단일 저장소 (오픈 포맷)                    │
└────────────────────────────────────────────────────────┘
```

| 특성 | Data Lake | Data Warehouse | Lakehouse |
|:---|:---|:---|:---|
| **저장 비용** | 낮음 | 높음 | 낮음 |
| **스키마** | 유연(Schema-on-Read) | 엄격(Schema-on-Write) | 강제(Schema Enforcement) |
| **ACID 트랜잭션** | ✗ | ✓ | ✓ |
| **비정형 데이터** | ✓ | ✗ | ✓ |
| **ML 통합** | ✓ | 제한적 | ✓ |
| **실시간 쿼리** | 느림 | 빠름 | 빠름 |

---

## 3. 구조 및 원리

**핵심 조건**: 델타 레이크하우스 (Delta Lakehouse) 스냅샷 롤백 Time Travel 트랜잭션은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 항목 | Delta Lake | Apache Iceberg | Apache Hudi |
|:---|:---|:---|:---|
| **주도 조직** | Databricks | Netflix/Apple | Uber |
| **오픈 거버넌스** | Linux Foundation | Apache | Apache |
| **엔진 지원** | Spark 최적화 | Spark, Flink, Trino | Spark, Flink |
| **Time Travel** | ✓ (버전/타임스탬프) | ✓ | ✓ |
| **MERGE/UPSERT** | ✓ | ✓ | ✓ (COW/MOR) |
| **스트리밍 증분** | 제한적 | ✓ | 강력 (특화) |
| **파일 포맷** | Parquet | Parquet/ORC/Avro | Parquet/ORC |
| **카탈로그** | Hive, Unity Catalog | Hive, REST, Glue | Hive |
| **멀티 테이블 트랜잭션** | ✓ (Databricks) | 개발 중 | ✗ |

```
COW (Copy-On-Write):
  UPSERT 시 전체 Parquet 파일 재작성
  → 읽기 빠름, 쓰기 느림 (배치에 적합)

MOR (Merge-On-Read):
  UPSERT를 Avro 델타 파일에만 기록
  READ 시 베이스 + 델타 병합
  → 쓰기 빠름, 읽기 약간 느림 (스트리밍에 적합)
```

---

## 4. 비교 및 연결

```python
from delta.tables import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# ① OPTIMIZE: 소형 파일 병합
spark.sql("OPTIMIZE sales_table")

# ② Z-ORDER: 자주 필터링하는 컬럼 기준 클러스터링
spark.sql("OPTIMIZE sales_table ZORDER BY (region, product_id)")

# ③ VACUUM: 오래된 파일 삭제 (기본 7일 보존 후 정리)
spark.sql("VACUUM sales_table RETAIN 168 HOURS")

# ④ Auto-Optimize (Databricks): 자동 소형 파일 병합
spark.sql("""
  ALTER TABLE sales_table
  SET TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
  )
""")

# ⑤ Data Skipping: 통계 기반 Row Group 스킵
# Delta Log의 min/max 통계로 자동 동작
spark.sql("SELECT * FROM sales_table WHERE region = 'Seoul'")
```

```python
# Change Data Feed 활성화
spark.sql("""
  ALTER TABLE sales_table
  SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
""")

# 변경 데이터 읽기 (CDC 대신 CDF 활용)
changes_df = spark.read.format("delta") \
    .option("readChangeFeed", "true") \
    .option("startingVersion", 10) \
    .table("sales_table")

# 변경 타입: insert / update_preimage / update_postimage / delete
changes_df.filter("_change_type = 'delete'").show()
```

```
Delta Lake + MLflow 통합으로 ML 재현성:
  ┌──────────────────────────────────────────────────┐
  │  MLflow Run 기록:                                 │
  │  - 데이터 버전: delta_version=42                  │
  │  - 데이터 타임스탬프: 2024-01-15 09:00:00         │
  │                                                  │
  │  재현 시:                                         │
  │  training_data = spark.read.format("delta")      │
  │      .option("versionAsOf", 42)                  │
  │      .load("/data/features")                     │
  │  → 동일 데이터로 모델 재학습 가능                 │
  └──────────────────────────────────────────────────┘
```

---

## 5. 실무 적용 및 판단

| 항목 | 기존 Data Lake | Delta Lakehouse |
|:---|:---|:---|
| **데이터 일관성** | 보장 불가 | ACID 보장 |
| **장애 복구** | 수동 재처리 | RESTORE + Time Travel |
| **ML 재현성** | 스냅샷 별도 관리 | 버전 번호로 자동 |
| **스키마 변경** | 전체 재처리 | 온라인 스키마 진화 |
| **규정 준수 (GDPR)** | 어려움 | DELETE + VACUUM |

1. **Delta Log의 역할**: JSON 기반 트랜잭션 로그가 ACID와 Time Travel의 핵심 — 로그를 재생하면 임의 시점 복원 가능
2. **Data Skipping**: Delta Log의 min/max 통계로 Row Group 스킵 → 쿼리 성능 10~100× 향상
3. **MERGE 패턴**: CDC 통합의 핵심, SCD Type 2 이력 관리에도 활용
4. **생태계 선택**: Databricks 환경 → Delta Lake, 멀티 쿼리 엔진 → Iceberg, 실시간 증분 → Hudi

```
┌─────────────────────────────────────────────────────────────┐
│                 Delta Lake 저장소 구조                        │
│                                                              │
│  /data/sales_table/                                          │
│  ├── _delta_log/                    ← 트랜잭션 로그           │
│  │   ├── 00000000000000000000.json  ← 버전 0 (테이블 생성)   │
│  │   ├── 00000000000000000001.json  ← 버전 1 (첫 INSERT)     │
│  │   ├── 00000000000000000002.json  ← 버전 2 (UPDATE)        │
│  │   ├── 00000000000000000010.json  ← 버전 10 (체크포인트)    │
│  │   └── 00000000000000000010.checkpoint.parquet             │
│  ├── part-00000-xxx.parquet         ← 실제 데이터 파일        │
│  ├── part-00001-xxx.parquet                                  │
│  └── part-00002-xxx.parquet                                  │
│                                                              │
│  Delta Log JSON 버전 1 예시:                                  │
│  {                                                           │
│    "add": {"path": "part-00001.parquet",                     │
│            "size": 1234567,                                  │
│            "stats": {"numRecords": 10000,                    │
│                      "minValues": {"date": "2024-01-01"},    │
│                      "maxValues": {"date": "2024-01-31"}}},  │
│    "commitInfo": {"timestamp": 1705046400000,                │
│                   "operation": "WRITE",                      │
│                   "operationParameters": {...}}              │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

```
ACID 보장 메커니즘:
  ┌────────────────────────────────────────────────┐
  │  원자성(Atomicity):                             │
  │  Delta Log에 커밋 전까지 데이터 파일 추가만    │
  │  (미완성 파일은 로그에 없으므로 무시됨)         │
  │                                                │
  │  일관성(Consistency):                           │
  │  스키마 적용(Schema Enforcement)으로            │
  │  잘못된 데이터 거부                             │
  │                                                │
  │  격리성(Isolation):                             │
  │  낙관적 동시성 제어(Optimistic Concurrency)     │
  │  충돌 감지 후 재시도 or 실패                    │
  │                                                │
  │  영속성(Durability):                            │
  │  S3/ADLS 다중 복제로 영구 보존                  │
  └────────────────────────────────────────────────┘
```

```
Delta Lake Time Travel 쿼리:

  -- 버전 번호로 특정 시점 쿼리
  SELECT * FROM sales_table VERSION AS OF 5;
  
  -- 타임스탬프로 쿼리
  SELECT * FROM sales_table TIMESTAMP AS OF '2024-01-15 12:00:00';
  
  -- Spark DataFrame API
  df_v5 = spark.read.format("delta")
              .option("versionAsOf", 5)
              .load("/data/sales_table")
  
  df_yesterday = spark.read.format("delta")
                     .option("timestampAsOf", "2024-01-14")
                     .load("/data/sales_table")
  
  -- 롤백 (버전 5로 되돌리기)
  spark.sql("""
    RESTORE TABLE sales_table TO VERSION AS OF 5
  """)
  
  -- 변경 이력 확인
  spark.sql("DESCRIBE HISTORY sales_table").show()
```

```sql
-- CDC (Change Data Capture) 데이터 반영: MERGE 구문
MERGE INTO target_sales t
USING source_changes s
ON t.order_id = s.order_id
WHEN MATCHED AND s.operation = 'DELETE' THEN DELETE
WHEN MATCHED AND s.operation = 'UPDATE' THEN
  UPDATE SET t.amount = s.amount, t.status = s.status
WHEN NOT MATCHED AND s.operation = 'INSERT' THEN
  INSERT (order_id, amount, status, created_at)
  VALUES (s.order_id, s.amount, s.status, s.created_at);
```

```
MERGE 내부 동작:
  1. 기존 파일 스캔 (매칭 레코드 식별)
  2. 변경된 파일만 새 Parquet 파일로 재작성
  3. 기존 파일 → Delta Log에 "remove" 기록
  4. 새 파일 → Delta Log에 "add" 기록
  5. 커밋 (원자적)
```

```
스키마 진화 지원 모드:
  ┌─────────────────────────────────────────────┐
  │  mergeSchema 옵션:                          │
  │  df.write.option("mergeSchema", "true")     │
  │  .mode("append").format("delta")            │
  │  .save("/data/sales_table")                 │
  │                                             │
  │  지원 변경:                                  │
  │  ✓ 새 컬럼 추가 (기존 레코드 = NULL)         │
  │  ✓ NULL 가능 컬럼 타입 변경 (일부)           │
  │                                             │
  │  미지원 변경:                                │
  │  ✗ 기존 컬럼 삭제                            │
  │  ✗ 기존 컬럼 타입 변경 (호환 불가)           │
  └─────────────────────────────────────────────┘
```

---

## 6. 기대효과 및 결론

1.

델타 레이크하우스 (Delta Lakehouse) 스냅샷 롤백 Time Travel 트랜잭션의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
Data Lake (S3 원시 저장) → 스키마 관리 불가
    │
    ▼
Data Warehouse → ETL 비용 높음, 유연성 부족
    │
    ▼
Data Lakehouse (레이크 + 웨어하우스 통합)
    ├─► Delta Lake (Databricks): ACID + Time Travel
    ├─► Apache Iceberg (Netflix): 파티션 진화
    └─► Apache Hudi (Uber): Upsert + CDC 특화
    │
    ▼
Parquet 기반 · 스냅샷 격리 · 트랜잭션 로그
    │
    ▼
Unity Catalog → 데이터 거버넌스 통합
```
2. ACID 트랜잭션은 데이터를 저장할 때 "전부 성공하거나, 전부 실패하거나"만 되는 규칙이야 — 절반만 저장된 이상한 상태는 절대 생기지 않아.
3. Time Travel은 도서관 책에 번호를 매겨서 "버전 5번 책"이라고 하면 그 날의 책을 정확히 꺼내주는 것과 같아!

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 메커니즘 | Delta Log | JSON 트랜잭션 로그, ACID 기반 |
| 경쟁 기술 | Apache Iceberg | 멀티 엔진 오픈 테이블 포맷 |
| 경쟁 기술 | Apache Hudi | 증분/스트리밍 특화 |
| 최적화 | Z-ORDER | 클러스터링으로 Data Skipping 향상 |
| CDC 통합 | Change Data Feed | 변경 데이터 스트림 |
| 관리 플랫폼 | Databricks Unity Catalog | Delta Lake 거버넌스 중앙화 |
| 파일 포맷 | Parquet | Delta Lake 기반 저장 포맷 |
| 아키텍처 | Medallion | Bronze→Silver→Gold 레이어 |
