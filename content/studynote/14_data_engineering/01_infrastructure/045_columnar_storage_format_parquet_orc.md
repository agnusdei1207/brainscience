+++
weight = 45
title = "45. 컬럼형 저장 형식 — Parquet & ORC"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: 컬럼형 저장 형식(Columnar Storage Format)은 행(Row) 대신 열(Column) 단위로 데이터를 저장해 분석 쿼리의 I/O를 극적으로 줄이는 빅데이터 핵심 기술 — 수백만 행에서 특정 열 5개만 조회할 때 행 기반은 전체 행을 읽지만, 컬럼형은 해당 열만 읽는다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

컬럼형 저장 형식 — Parquet & ORC은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
저장 형식 비교:

샘플 데이터 (3행 × 4열):
  id | name  | age | salary
  1  | Alice |  30 | 5000
  2  | Bob   |  25 | 4000
  3  | Carol |  35 | 6000

행 기반 (Row-Oriented):
  저장: [1,Alice,30,5000][2,Bob,25,4000][3,Carol,35,6000]
  
  장점: 행 단위 CRUD 빠름 (OLTP)
  단점: 전체 열 다 읽어야 함 (분석)

컬럼 기반 (Column-Oriented):
  저장: [1,2,3][Alice,Bob,Carol][30,25,35][5000,4000,6000]
  
  장점: 필요한 열만 읽음 (OLAP)
  압축률 높음 (같은 타입 데이터)

쿼리 차이:
  SELECT AVG(salary) FROM employees
  
  행 기반: id, name, age, salary 모두 읽음 (100%)
  컬럼형: salary 열만 읽음 (25%)
  
  1억 행, 100열 테이블:
  행 기반: 5개 열 쿼리 → 100열 전부 읽음
  컬럼형: 5개 열 쿼리 → 5열만 읽음 (95% I/O 절감)

압축 효율:
  컬럼 내 데이터 = 동일 타입 + 유사 값
  
  salary열: 4000, 5000, 4500, 5200...
  → 델타 인코딩: +0, +1000, -500, +700
  → RLE: 같은 값 반복 (부서 코드 등)
  → 압축률 5~10× 일반적
```

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```
Apache Parquet:
  Apache Foundation 오픈소스 (2013)
  Twitter + Cloudera 공동 개발
  
파일 구조:
  ┌─────────────────────────────┐
  │ Magic Number (PAR1)         │
  ├─────────────────────────────┤
  │ Row Group 1                 │
  │   Column Chunk A            │
  │     Page 1, Page 2, ...     │
  │   Column Chunk B            │
  │     Page 1, Page 2, ...     │
  ├─────────────────────────────┤
  │ Row Group 2                 │
  │   ...                       │
  ├─────────────────────────────┤
  │ Footer (메타데이터)          │
  │   스키마, 통계(Min/Max)      │
  │   Row Group 오프셋          │
  │ Magic Number (PAR1)         │
  └─────────────────────────────┘

핵심 구성:
  Row Group: 기본 128MB~1GB
    → 병렬 처리 단위
  Column Chunk: 열 데이터 블록
  Page: 인코딩·압축 단위 (1MB)

인코딩:
  Dictionary Encoding: 반복 값 사전화
  RLE (Run-Length Encoding): 연속 값 압축
  Bit Packing: 정수 소형 비트 패킹
  Delta Encoding: 연속 증가 값

압축 코덱:
  Snappy (기본): 빠름, 적당한 압축률
  GZIP: 높은 압축률, 느림
  LZ4: 초고속, 중간 압축률
  ZSTD: 빠름 + 높은 압축률 (권장)

술어 푸시다운:
  Row Group Footer 통계:
  min_value=1000, max_value=5000
  
  WHERE salary > 6000:
  → 이 Row Group 건너뜀! (I/O 절감)
```

---

## 3. 구조 및 원리

**핵심 조건**: 컬럼형 저장 형식 — Parquet & ORC은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```
Apache ORC (Optimized Row Columnar):
  Hive 프로젝트에서 탄생 (2013)
  Hortonworks 개발
  
파일 구조:
  ┌───────────────────────────┐
  │ ORC Header (Magic: ORC)   │
  ├───────────────────────────┤
  │ Stripe 1                  │
  │   Index Data              │
  │   Row Data (컬럼별)        │
  │   Stripe Footer           │
  ├───────────────────────────┤
  │ Stripe 2                  │
  │   ...                     │
  ├───────────────────────────┤
  │ File Footer               │
  │   Stripe 목록              │
  │   스키마                   │
  │   통계                    │
  │ Postscript                │
  └───────────────────────────┘

Stripe = Parquet Row Group (기본 256MB)

ORC 특화 기능:

1. ACID 트랜잭션:
   Hive 3.0+ 지원
   INSERT, UPDATE, DELETE 지원
   (Parquet는 기본 append-only)

2. Bloom Filter:
   특정 값 존재 여부 빠른 확인
   WHERE id = 12345 → Bloom Filter로 Stripe 스킵

3. 경량 인덱스:
   Row Index (10,000행마다 통계)
   Bloom Filter Index

4. LLAP (Live Long and Process):
   Hive LLAP과 통합 최적화
   인메모리 캐시

ORC 적합 환경:
  Hive 기반 데이터 웨어하우스
  UPDATE/DELETE 필요한 SCD(천천히 변하는 차원)
  Hive ACID 트랜잭션
```

---

## 4. 비교 및 연결

```
비교표:

항목           | CSV      | Parquet   | ORC
---------------|----------|-----------|----------
저장 방식      | 행 기반  | 컬럼 기반 | 컬럼 기반
압축 지원      | 없음     | 있음      | 있음
스키마 내장    | 없음     | 있음      | 있음
읽기 성능 (분석) | 낮음  | 높음      | 높음
ACID 트랜잭션  | 없음     | 없음(기본)| 있음 (Hive)
파싱 오버헤드  | 없음     | 있음      | 있음
생태계 지원    | 범용     | Spark 최적| Hive 최적
Bloom Filter   | 없음     | 있음(선택)| 있음
복잡 타입 지원 | 없음     | 중첩 스키마| 중첩 스키마

선택 가이드:
  CSV: 소규모 데이터, 호환성 최우선
  Parquet: Spark, Presto/Trino, Athena, Iceberg
  ORC: Hive, Hive ACID 트랜잭션 필요 시

현재 트렌드:
  Parquet → Apache Iceberg, Delta Lake 표준
  ORC → Hive 기반 환경
  
  Delta Lake: Parquet 기반 + ACID 보완
  Apache Iceberg: Parquet/ORC/Avro 지원
  
성능 벤치마크 (1억 행, 10열 중 3열 쿼리):
  CSV:     100s
  Parquet: 8s   (ZSTD 압축, 술어 푸시다운)
  ORC:     10s  (ZLIB 압축, Bloom Filter)
```

---

## 5. 실무 적용 및 판단

```
전자상거래 데이터 레이크 최적화:

초기 상황:
  S3에 CSV 파일 적재
  Athena 쿼리: 일 주문 분석 → 10~30분
  비용: 쿼리당 $50~200 (스캔 비용)

문제 진단:
  Athena = Presto 기반 (S3 스캔)
  CSV: 스키마 없음, 압축 없음, 전체 스캔
  
  일 주문 테이블: 5억 행, 50열
  주요 쿼리: 5열만 사용, 날짜 필터링

최적화 전략:

1. CSV → Parquet 변환 (ZSTD 압축):
   Glue ETL로 일배치 변환
   
   결과:
   CSV: 500GB/일 → Parquet: 80GB/일 (84% 압축)

2. Hive 파티셔닝:
   S3 키: s3://bucket/orders/year=2024/month=01/day=15/
   
   WHERE order_date = '2024-01-15'
   → 해당 파티션만 스캔

3. Row Group 크기 최적화:
   Row Group = 256MB (대용량 배치 쿼리 최적)

4. 술어 푸시다운 최적화:
   컬럼 순서 = 카디널리티 높은 것 먼저
   → Bloom Filter 효과 극대화

결과:
  쿼리 시간: 10~30분 → 30~90초
  스캔 비용: $50~200 → $2~8 (96% 절감)
  월 Athena 비용: 500만원 → 20만원
  
  추가: Delta Lake 전환으로 ACID 지원
  (일 데이터 수정 필요 케이스 처리)
```

---

## 6. 기대효과 및 결론

컬럼형 저장 형식 — Parquet & ORC의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```
[RC File / SequenceFile (2000s)]
Hadoop 초기 컬럼형 시도
제한적 기능
      |
      v
[Parquet + ORC 등장 (2013)]
Hadoop 생태계 표준 컬럼형
Twitter/Hortonworks 주도
      |
      v
[Delta Lake / Iceberg / Hudi (2016~)]
컬럼형 + ACID + 스냅샷
레이크하우스 패러다임
      |
      v
[현재: 오픈 테이블 포맷]
Apache Iceberg 표준 부상
Parquet 기반 멀티엔진
AWS, Snowflake, Databricks 지원
```

---

## 8. 관련 개념 맵

```
컬럼형 저장 형식
+-- Apache Parquet
|   +-- Row Group / Column Chunk / Page
|   +-- 압축 (Snappy, ZSTD)
|   +-- 술어 푸시다운
+-- Apache ORC
|   +-- Stripe / Index / Bloom Filter
|   +-- Hive ACID
+-- 비교
|   +-- CSV (행 기반)
|   +-- Avro (직렬화)
+-- 상위 기술
    +-- Delta Lake (Parquet + ACID)
    +-- Apache Iceberg (Parquet/ORC)
    +-- Apache Hudi
```
