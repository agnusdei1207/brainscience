+++
weight = 178
title = "178. 파케이 (Parquet) 스토리지 압축 포맷 RLE 스킵 인코딩 최적 성능"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++
## 0. 핵심 인사이트

> **핵심**: Parquet은 컬럼형(Columnar) 저장 포맷으로, 분석 쿼리가 필요한 컬럼만 읽고(Column Pruning), 통계 기반으로 불필요한 Row Group을 건너뛰어(Predicate Pushdown) I/O를 최소화한다.
> 2. **가치**: RLE (Run-Length Encoding)·Dictionary Encoding·Snappy 압축 조합으로 원본 데이터 대비 5~10배 압축하면서도 쿼리 성능은 행 기반 포맷(CSV/Avro) 대비 10~100배 향상된다.
> 3. **판단 포인트**: ORC는 Hive/MapReduce 생태계에, Parquet은 Spark/Presto/Flink 멀티 엔진에, Avro는 스키마 진화가 잦은 스트리밍 직렬화에 최적이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 1.1 행 기반 vs 컬럼 기반 저장

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

### 1.2 Parquet 사용 현황

| 분야 | 활용 사례 |
|:---|:---|
| **데이터 레이크** | S3/ADLS의 기본 저장 포맷 |
| **Delta/Iceberg/Hudi** | 모든 오픈 테이블 포맷의 기반 |
| **Spark/Presto/Trino** | 기본 지원 포맷 |
| **ML 피처 스토어** | 피처 데이터 저장 |
| **데이터 웨어하우스** | Redshift Spectrum, BigQuery External Table |

📢 **섹션 요약 비유**: Parquet은 도서관의 과목별 책장 시스템이다. "수학 책 평균 두께"를 알고 싶으면 수학 책장(컬럼)만 보면 되지, 모든 책장(행)을 뒤질 필요 없다.

---

## 2. 구성요소

### 2.1 Parquet 파일 구조

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

### 2.2 인코딩 방식

#### RLE (Run-Length Encoding)

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

#### Dictionary Encoding (딕셔너리 인코딩)

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

#### Predicate Pushdown (술어 푸시다운)

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

### 2.3 압축 코덱 비교

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

📢 **섹션 요약 비유**: Parquet 인코딩은 똑똑한 압축 포장이다. 반복 값은 RLE로 "10개짜리 세트"로 묶고, 카테고리는 딕셔너리로 코드화하고, 불필요한 상자(Row Group)는 태그(통계)만 보고 건너뛴다.

---

## 3. 구조 및 동작 원리

### 3.1 Parquet vs ORC vs Avro

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

### 3.2 Bloom Filter 활용

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

### 3.3 Column Statistics vs Bloom Filter

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

📢 **섹션 요약 비유**: Parquet vs ORC vs Avro는 냉장고, 서랍, 배낭의 차이다. 냉장고(Parquet)와 서랍(ORC)은 분석용 정리 보관에 최적이고, 배낭(Avro)은 이동(스트리밍 전송) 중에 빠르게 넣고 꺼내기 좋다.

---

## 4. 비교 및 트레이드오프

### 4.1 Spark Parquet 최적화 설정

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

### 4.2 Parquet 성능 최적화 체크리스트

| 항목 | 권장 설정 | 이유 |
|:---|:---|:---|
| **Row Group 크기** | 128MB~1GB | 클수록 압축률 높음, 작을수록 스킵 세밀 |
| **Page 크기** | 1MB | 메모리-I/O 균형 |
| **압축 코덱** | ZSTD (최신) / Snappy (빠른 처리) | 용도에 따라 |
| **파티셔닝 컬럼** | 날짜, 지역 등 필터 조건 | 파티션 프루닝 |
| **Z-ORDER (Delta)** | 자주 필터링하는 컬럼 | Data Skipping 강화 |
| **통계 수집** | nullCount, minMax | Predicate Pushdown |
| **Bloom Filter** | UUID, ID 컬럼 | 고카디널리티 스킵 |

### 4.3 Parquet 파일 크기 최적화

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

📢 **섹션 요약 비유**: Parquet 최적화는 효율적인 서류 정리함이다. 서랍별 라벨(파티셔닝)로 서랍 통째로 건너뛰고, 각 서류 요약본(통계/Bloom Filter)으로 세부 검색 없이 결과를 찾는다.

---

## 5. 실무 적용 및 최적화 기법

### 5.1 Parquet 도입 효과

| 항목 | CSV | Parquet (ZSTD) | 개선률 |
|:---|:---|:---|:---|
| **저장 크기** | 100GB | 10~20GB | 5~10× 절감 |
| **쿼리 속도 (SELECT cols)** | 기준 | 10~100× 빠름 | 컬럼 수에 비례 |
| **I/O 비용 (S3)** | 100% | 10~20% | 80~90% 절감 |
| **스캔 비용 (Athena)** | $5/TB | $0.5~1/TB | 5~10× 절감 |

### 5.2 기술사 답안 핵심 논점

1. **컬럼형 저장의 핵심**: 분석 쿼리는 대부분 몇 개 컬럼만 접근 → Column Pruning으로 I/O 90% 절감
2. **RLE + Dictionary 시너지**: Dictionary로 저카디널리티 컬럼 코드화 후 RLE 적용 → 압축률 극대화
3. **Predicate Pushdown 조건**: Row Group 통계(min/max)가 필터 조건과 겹치지 않으면 전체 Row Group 스킵
4. **포맷 선택**: Parquet(분석+멀티엔진), ORC(Hive+ACID), Avro(스트리밍 직렬화)

📢 **섹션 요약 비유**: Parquet은 도서관이 "책 목록 카드(Footer 통계)"만 보고 "이 선반 전체는 1950년대 책이니까 2024년 찾으면 건너뛰세요!"라고 알려주는 지능형 색인 시스템이다.

---

### 📌 관련 개념 맵

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

---

### 👶 어린이를 위한 3줄 비유 설명

1. Parquet은 반찬을 종류별로 따로 담아두는 도시락 통이야 — "김치만 주세요"라고 하면 김치 칸만 열면 되니까 훨씬 빠르게 꺼낼 수 있어!

### 📈 관련 키워드 및 발전 흐름도

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
