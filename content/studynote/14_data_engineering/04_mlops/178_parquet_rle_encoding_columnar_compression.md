+++
weight = 178
title = "178. 파케이 (Parquet) 스토리지 압축 포맷 RLE 스킵 인코딩 최적 성능"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: Parquet은 컬럼형(Columnar) 저장 포맷으로, 분석 쿼리가 필요한 컬럼만 읽고(Column Pruning), 통계 기반으로 불필요한 Row Group을 건너뛰어(Predicate Pushdown) I/O를 최소화한다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

파케이 (Parquet) 스토리지 압축 포맷 RLE 스킵 인코딩 최적 성능은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
행 기반 (Row-oriented, CSV/Avro):
  레코드 1: [id=1, name="Alice", age=30, salary=5000]
  레코드 2: [id=2, name="Bob",   age=25, salary=6000]
  레코드 3: [id=3, name="Carol", age=35, salary=5500]
  
  쿼리: SELECT AVG(salary) FROM employees
  → 모든 레코드의 모든 컬럼을 읽어야 함 (불필요한 I/O)

컬럼 기반 (Column-oriented, Parquet/ORC):
  id 컬럼:     [1, 2, 3, ...]
  name 컬럼:   ["Alice", "Bob", "Carol", ...]
  age 컬럼:    [30, 25, 35, ...]
  salary 컬럼: [5000, 6000, 5500, ...]
  
  쿼리: SELECT AVG(salary) FROM employees
  → salary 컬럼만 읽으면 됨 → I/O 75% 절감
  → 같은 타입 값이 연속 → 압축률 10배 향상
```

---

## 2. 구성요소

| 분야 | 활용 사례 |
|:---|:---|
| **데이터 레이크** | S3/ADLS의 기본 저장 포맷 |
| **Delta/Iceberg/Hudi** | 모든 오픈 테이블 포맷의 기반 |
| **Spark/Presto/Trino** | 기본 지원 포맷 |
| **ML 피처 스토어** | 피처 데이터 저장 |
| **데이터 웨어하우스** | Redshift Spectrum, BigQuery External Table |

---

## 3. 구조 및 원리

**핵심 조건**: 파케이 (Parquet) 스토리지 압축 포맷 RLE 스킵 인코딩 최적 성능은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 항목 | Parquet | ORC | Avro |
|:---|:---|:---|:---|
| **저장 방식** | 컬럼형 | 컬럼형 | 행 기반 |
| **압축 최적화** | ✓ | ✓ (더 나은 통계) | 제한적 |
| **읽기 성능 (분석)** | 매우 빠름 | 매우 빠름 | 느림 |
| **쓰기 성능** | 중간 | 중간 | 빠름 |
| **스키마 진화** | 제한적 | 제한적 | 강력 |
| **스트리밍 직렬화** | 부적합 | 부적합 | 최적 |
| **Hive 최적화** | 보통 | 최강 (ACID 내장) | — |
| **Spark 최적화** | 최강 | 강력 | 보통 |
| **주요 사용처** | 분석, Delta/Iceberg | Hive, HBase | Kafka, Avro Registry |

```
Parquet Bloom Filter (v2.0+):
  - 특정 컬럼에 Bloom Filter 저장
  - "이 Row Group에 값 X가 존재하는가?" 빠른 판별
  - False Positive 가능, False Negative 불가
  
  사용 예:
  SELECT * FROM events WHERE user_id = 'uuid-12345'
  
  Bloom Filter로 대부분 Row Group 스킵 가능
  (Dictionary Encoding과 달리 고카디널리티 컬럼에 효과적)
```

```
┌────────────────────────────────────────────────────────┐
│       데이터 스킵 기법 비교                             │
│                                                        │
│  Column Statistics (항상 기록):                        │
│  - min/max/null_count/distinct_count                  │
│  - 범위 필터에 효과적 (date BETWEEN, age > 30)         │
│  - 등치 필터에 범위가 넓으면 효과 제한                  │
│                                                        │
│  Dictionary Encoding:                                  │
│  - 저카디널리티: 딕셔너리로 필터링                       │
│  - 10,000개 미만 고유값에 효과적                        │
│                                                        │
│  Bloom Filter:                                         │
│  - 고카디널리티 + 등치 필터                              │
│  - user_id, session_id, UUID 등에 효과적               │
│  - 저장 오버헤드: 설정 가능 (기본 1MB/column/group)     │
└────────────────────────────────────────────────────────┘
```

---

## 4. 비교 및 연결

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .config("spark.sql.parquet.compression.codec", "zstd") \
    .config("spark.sql.parquet.mergeSchema", "false")       \
    .config("spark.sql.parquet.filterPushdown", "true")     \
    .config("spark.sql.parquet.enableVectorizedReader", "true") \
    .config("spark.hadoop.parquet.block.size", str(128*1024*1024)) \  # 128MB
    .getOrCreate()

# 파티셔닝 + 컬럼 프루닝 최적화
df = spark.read.parquet("s3://datalake/sales/")

# 1. 컬럼 프루닝: 필요한 컬럼만 선택
df.select("date", "amount", "region") \
  .filter("date >= '2024-01-01' AND date < '2024-02-01'") \
  .filter("region = 'Seoul'") \
  .groupBy("date").agg({"amount": "sum"}) \
  .write.parquet("s3://datalake/result/")

# 2. 파티션 프루닝을 위한 파티셔닝 저장
df.write \
  .partitionBy("year", "month", "region") \
  .mode("overwrite") \
  .parquet("s3://datalake/sales_partitioned/")
```

| 항목 | 권장 설정 | 이유 |
|:---|:---|:---|
| **Row Group 크기** | 128MB~1GB | 클수록 압축률 높음, 작을수록 스킵 세밀 |
| **Page 크기** | 1MB | 메모리-I/O 균형 |
| **압축 코덱** | ZSTD (최신) / Snappy (빠른 처리) | 용도에 따라 |
| **파티셔닝 컬럼** | 날짜, 지역 등 필터 조건 | 파티션 프루닝 |
| **Z-ORDER (Delta)** | 자주 필터링하는 컬럼 | Data Skipping 강화 |
| **통계 수집** | nullCount, minMax | Predicate Pushdown |
| **Bloom Filter** | UUID, ID 컬럼 | 고카디널리티 스킵 |

```
소형 파일 문제:
  S3에 수천 개의 10KB Parquet 파일 → S3 LIST API 병목
  → Spark job 시작이 수 분 걸림

해결 방법:
  1. repartition/coalesce로 출력 파일 수 조정
     df.repartition(200).write.parquet(...)
  
  2. Delta Lake OPTIMIZE (소형 파일 병합)
     OPTIMIZE table_name
  
  3. Spark 3.x AQE (Adaptive Query Execution)
     spark.conf.set("spark.sql.adaptive.enabled", "true")
     → 자동 파티션 병합
  
  권장 파일 크기: 128MB~1GB/파일
```

---

## 5. 실무 적용 및 판단

| 항목 | CSV | Parquet (ZSTD) | 개선률 |
|:---|:---|:---|:---|
| **저장 크기** | 100GB | 10~20GB | 5~10× 절감 |
| **쿼리 속도 (SELECT cols)** | 기준 | 10~100× 빠름 | 컬럼 수에 비례 |
| **I/O 비용 (S3)** | 100% | 10~20% | 80~90% 절감 |
| **스캔 비용 (Athena)** | $5/TB | $0.5~1/TB | 5~10× 절감 |

1. **컬럼형 저장의 핵심**: 분석 쿼리는 대부분 몇 개 컬럼만 접근 → Column Pruning으로 I/O 90% 절감
2. **RLE + Dictionary 시너지**: Dictionary로 저카디널리티 컬럼 코드화 후 RLE 적용 → 압축률 극대화
3. **Predicate Pushdown 조건**: Row Group 통계(min/max)가 필터 조건과 겹치지 않으면 전체 Row Group 스킵
4. **포맷 선택**: Parquet(분석+멀티엔진), ORC(Hive+ACID), Avro(스트리밍 직렬화)

```
┌─────────────────────────────────────────────────────────────┐
│                  Parquet 파일 내부 구조                       │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │                    File Header                      │     │
│  │  Magic Number: "PAR1" (4 bytes)                    │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │             Row Group 0 (기본 128MB)                │     │
│  │  ┌────────────────────────────────────────────┐   │     │
│  │  │  Column Chunk: id                           │   │     │
│  │  │  ├── Page 0 (8KB~): Dictionary Page        │   │     │
│  │  │  ├── Page 1: Data Page (RLE 인코딩)        │   │     │
│  │  │  └── Page 2: Data Page                     │   │     │
│  │  ├────────────────────────────────────────────┤   │     │
│  │  │  Column Chunk: name                         │   │     │
│  │  │  Column Chunk: age                          │   │     │
│  │  │  Column Chunk: salary                       │   │     │
│  │  └────────────────────────────────────────────┘   │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │             Row Group 1 (다음 128MB)                │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │              File Footer (메타데이터)               │     │
│  │  - 스키마 정보                                      │     │
│  │  - Row Group 통계: min/max/null_count               │     │
│  │  - Column 통계 (Predicate Pushdown 핵심)            │     │
│  │  - 인코딩/압축 방식                                 │     │
│  └────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Magic Number: "PAR1" (4 bytes)                    │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

```
원본 데이터 (status 컬럼):
  ACTIVE ACTIVE ACTIVE INACTIVE INACTIVE ACTIVE ACTIVE ACTIVE ACTIVE

RLE 인코딩:
  (ACTIVE × 3), (INACTIVE × 2), (ACTIVE × 4)
  → 9개 값 → 3개 레코드로 압축

이진 표현:
  원본: 9 × 1 byte = 9 bytes
  RLE:  3 × (1 byte count + 1 byte value) = 6 bytes → 33% 절감
  
  정수 컬럼 (반복 많을수록 효율 극대화):
  원본: [1,1,1,1,2,2,2,3,3] = 9 × 4 bytes = 36 bytes
  RLE:  [(4,1),(3,2),(2,3)] = 3 × (4+4) = 24 bytes → 33% 절감
```

```
원본 country 컬럼:
  ["Korea", "USA", "Japan", "Korea", "USA", "Korea", "Japan", "Korea"]
  
  가정: 각 문자열 5 bytes → 8 × 5 = 40 bytes

Dictionary Encoding:
  딕셔너리: {0:"Korea", 1:"USA", 2:"Japan"}  (15 bytes)
  정수 코드: [0, 1, 2, 0, 1, 0, 2, 0]       (8 bytes, 1 byte/값)
  합계: 23 bytes → 40 bytes 대비 42% 절감

  + RLE 결합:
  정수 코드: [(0×1), (1×1), (2×1), (0×1), (1×1), (0×1), (2×1), (0×1)]
  
  카디널리티 낮을수록 효율 증가
  (예: status, country, category 컬럼)
```

```
쿼리: SELECT * FROM sales WHERE date = '2024-01-15'

Parquet 통계 기반 스킵:
  ┌────────────────────────────────────────────────────┐
  │  Row Group 0: date min='2024-01-01', max='2024-01-10' │
  │              → 조건 불만족, 전체 스킵! (I/O 절감)   │
  │                                                    │
  │  Row Group 1: date min='2024-01-11', max='2024-01-20' │
  │              → 조건 만족 가능, 읽어야 함            │
  │                                                    │
  │  Row Group 2: date min='2024-01-21', max='2024-01-31' │
  │              → 조건 불만족, 전체 스킵!              │
  └────────────────────────────────────────────────────┘
  
  결과: 3개 Row Group 중 1개만 읽음 → I/O 66% 절감
```

| 코덱 | 압축률 | 압축 속도 | 해제 속도 | 특징 |
|:---|:---|:---|:---|:---|
| **Snappy** | 중간 (2~3×) | 매우 빠름 | 매우 빠름 | Google 개발, 기본값 |
| **LZ4** | 중간 (2~3×) | 최고 속도 | 최고 속도 | 실시간 처리에 최적 |
| **GZIP (Deflate)** | 높음 (4~6×) | 느림 | 중간 | 보관·전송 최적 |
| **ZSTD** | 높음 (4~6×) | 빠름 | 빠름 | Zstandard, 최신 최고 균형 |
| **Brotli** | 매우 높음 | 매우 느림 | 빠름 | 웹 전송 특화 |
| **None** | 없음 | — | — | 이미 압축된 데이터 |

```
실무 선택 기이드:
  실시간 처리 (Flink/Spark Streaming) → LZ4 또는 Snappy
  대화형 쿼리 (Presto/Athena)         → Snappy (기본)
  장기 보관 / 비용 절감               → GZIP 또는 ZSTD
  최신 Spark 3.x+                     → ZSTD 권장 (성능+압축 균형)
```

---

## 6. 기대효과 및 결론

1.

파케이 (Parquet) 스토리지 압축 포맷 RLE 스킵 인코딩 최적 성능의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
CSV/JSON (행 기반, 비압축)
    │
    ▼
열 지향 포맷: Parquet · ORC
    ├─► 컬럼별 독립 압축 (RLE · Dictionary · Snappy)
    ├─► 프레디케이트 푸시다운: 불필요 컬럼 스킵
    └─► Row Group + Page 구조: 병렬 읽기
    │
    ▼
Lakehouse 기반 테이블 포맷
    ├─► Delta Lake (.parquet + 트랜잭션 로그)
    ├─► Apache Iceberg (.parquet + 메타데이터 트리)
    └─► Apache Hudi (.parquet + Upsert)
    │
    ▼
Arrow In-Memory Format → 제로 복사 교환
```
2. RLE 압축은 "같은 말 반복 줄이기"야 — "A A A A A B B B"를 "A 5번 B 3번"으로 짧게 표현하는 거지.
3. Predicate Pushdown은 책을 하나하나 펼치는 대신, 책 표지 요약(min/max 통계)만 보고 "이 책장엔 원하는 내용 없다!"고 통째로 건너뛰는 똑똑한 도서관 검색이야.

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 경쟁 포맷 | ORC | Hive 특화 컬럼형, 내장 ACID |
| 직렬화 포맷 | Avro | 스트리밍 스키마 직렬화 |
| 인코딩 기법 | RLE | 반복 값 압축 |
| 인코딩 기법 | Dictionary Encoding | 저카디널리티 코드화 |
| 쿼리 최적화 | Predicate Pushdown | 통계 기반 Row Group 스킵 |
| 쿼리 최적화 | Column Pruning | 필요 컬럼만 읽기 |
| 고급 스킵 | Bloom Filter | 고카디널리티 등치 필터 가속 |
| 통합 | Delta Lake | Parquet 기반 ACID 레이크하우스 |
