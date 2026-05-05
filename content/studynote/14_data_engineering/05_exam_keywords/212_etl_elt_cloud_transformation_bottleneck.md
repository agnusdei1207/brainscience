+++
weight = 212
title = "212. ETL vs ELT (Extract-Transform-Load vs Extract-Load-Transform) 클라우드 전이"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: ETL(Extract, Transform, Load)은 중간 변환 서버에서 먼저 정제 후 DW에 적재하지만, ELT(Extract, Load, Transform)는 원본 데이터를 클라우드 DW에 먼저 적재 후 DW 내부의 막대한 컴퓨팅 파워로 변환한다.
> **비유**: 여러 공정이 연결된 생산 라인처럼, 앞단의 입력 품질과 중간 단계의 흐름 제어가 최종 결과를 좌우하는 구조와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

ETL(Extract, Transform, Load)은 1970~80년대 온프레미스(On-Premise) 데이터 웨어하우스 시대에 탄생했다. 소스 시스템에서 데이터를 추출(Extract)하고, 중간 서버에서 정제·변환(Transform)한 뒤, 최종 DW에 적재(Load)하는 순서다.

```
┌───────────┐    ┌──────────────────────┐    ┌─────────────┐
│  소스 DB  │───►│  ETL 서버 (변환)     │───►│  DW/목적지  │
│  ERP/CRM  │    │  데이터 정제         │    │  Teradata   │
│  파일/API │    │  타입 변환           │    │  Oracle DW  │
└───────────┘    │  비즈니스 룰 적용    │    └─────────────┘
                 └──────────────────────┘
                   ↑ 병목 지점 (Bottleneck)
                   처리 용량 = ETL 서버 CPU/메모리
```

**ETL의 병목 문제**: 모든 변환이 중간 ETL 서버를 통과하므로, 데이터 볼륨이 늘어날수록 ETL 서버가 단일 장애점(SPOF, Single Point of Failure)이자 성능 병목이 된다.

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

클라우드 DW는 스토리지와 컴퓨팅을 분리하여, 컴퓨팅 노드를 탄력적으로 확장한다. 이 환경에서는 변환을 DW 내부에서 수행하는 것이 훨씬 효율적이다.

---

## 3. 구조 및 원리

**핵심 조건**: ETL vs ELT (Extract-Transform-Load vs Extract-Load-Transform) 클라우드 전이은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

ETL에서 ELT로의 전환은 단순한 순서 변경이 아니라 **책임의 이동**이다.

```
ETL 시대:
  소스 ──► [ETL 서버가 모든 책임] ──► DW
           ↑ 병목, 단일 실패점

ELT 시대:
  소스 ──► DW RAW ──► [DW 컴퓨팅이 책임] ──► DW MART
                      ↑ 탄력적 확장, 원본 보존
```

현대 데이터 아키텍처에서 ELT는 데이터 메시(Data Mesh) 패턴과 결합된다. 각 도메인 팀이 자신의 RAW 데이터를 DW에 적재(Load)하고, 도메인별 dbt 프로젝트로 변환(Transform)하여 데이터 프로덕트(Data Product)를 생성한다.

최근에는 DW에서 분석한 결과를 운영 시스템(CRM, 이메일 마케팅)으로 다시 내보내는 **Reverse ETL** 패턴도 주목받는다. Census, Hightouch 같은 도구가 이를 담당한다.

---

## 4. 비교 및 연결

```
데이터가 민감하고 정제 전 적재가 불가한가?
       ↓ YES
       ETL (금융·의료 컴플라이언스 환경)

       ↓ NO
클라우드 DW를 사용하고 대용량인가?
       ↓ YES
       ELT + dbt (BigQuery, Snowflake, Redshift)

       ↓ NO (온프레미스, 소규모)
       ETL (Informatica, Talend, SSIS)
```

| 항목 | 주의점 |
|:---|:---|
| **데이터 품질** | RAW 적재 후 변환 실패 시 오염 데이터가 DW에 체류 |
| **비용 관리** | 클라우드 DW 쿼리 비용 — 비효율 SQL이 과금 폭탄 |
| **보안** | 민감 데이터가 RAW 레이어에 노출 → 컬럼 마스킹 필수 |
| **거버넌스** | dbt Lineage + 데이터 카탈로그(Data Catalog)로 계보 관리 |

---

## 5. 실무 적용 및 판단

| 효과 | 정량적 지표 |
|:---|:---|
| **파이프라인 구축 속도** | 전통 ETL 대비 개발 기간 40~60% 단축 |
| **유연성** | 비즈니스 룰 변경 시 dbt 모델만 수정 (재ETL 불필요) |
| **비용** | ETL 전용 서버 운영 비용 제거 |
| **신뢰성** | RAW 보존으로 어떤 시점으로든 재처리 가능 |

기술사 답안에서는 **"변환 병목의 위치가 아키텍처 선택을 결정한다"**는 관점에서 서술해야 한다. ETL은 데이터 품질과 컴플라이언스 우선, ELT는 속도와 유연성 우선의 설계 철학이며, 현대 클라우드 환경에서는 ELT + dbt + 데이터 카탈로그의 조합이 표준 스택으로 자리잡고 있다.

| 항목 | ETL (Extract-Transform-Load) | ELT (Extract-Load-Transform) |
|:---|:---|:---|
| **변환 위치** | 중간 ETL 서버 (외부) | 목적지 DW 내부 |
| **적재 데이터** | 정제된 최종 데이터 | 원시(Raw) 데이터 |
| **스케일링** | ETL 서버 수직/수평 확장 필요 | DW 컴퓨팅 탄력적 확장 |
| **지연 시간** | 변환 완료 후 적재 → 지연 큼 | 즉시 적재 → 변환은 별도 |
| **원본 보존** | 변환 후 원본 불일치 발생 가능 | Raw 데이터 항상 보존 |
| **적합 환경** | 온프레미스, 레거시 DW | 클라우드 DW (Snowflake, BigQuery) |
| **대표 도구** | Informatica, Talend, SSIS | dbt, Spark SQL, BigQuery TRANSFORM |

```
┌────────────┐   Extract   ┌──────────────────────────────────────┐
│  소스 시스템│──────────►│            클라우드 DW               │
│  MySQL/API │             │                                      │
│  S3/Kafka  │   Load      │  ┌──────────┐   Transform            │
│            │──────────►│  │ RAW 레이어│──────────────►  │
└────────────┘             │  └──────────┘                │       │
                           │                              ▼       │
                           │                    ┌──────────────┐  │
                           │                    │ STAGING 레이어│  │
                           │                    └──────┬───────┘  │
                           │                           │ dbt/SQL  │
                           │                           ▼          │
                           │                    ┌──────────────┐  │
                           │                    │ MART 레이어   │  │
                           │                    └──────────────┘  │
                           └──────────────────────────────────────┘
```

dbt(Data Build Tool)는 ELT의 Transform 단계를 SQL 파일과 YAML 설정으로 코드화하는 오픈소스 프레임워크다.

```yaml
# dbt 모델 예시: models/staging/stg_orders.sql
SELECT
  order_id,
  customer_id,
  CAST(order_date AS DATE)   AS order_date,
  amount / 100.0             AS amount_usd  -- 센트→달러 변환
FROM {{ source('raw', 'orders') }}
WHERE status != 'cancelled'
```

**dbt 장점**:
- SQL 기반이라 데이터 분석가도 변환 로직 작성 가능
- 계보(Lineage) 자동 추적 — 어떤 테이블이 어디서 왔는지 시각화
- 테스트(not_null, unique, accepted_values) 내장
- Git 기반 버전 관리로 CI/CD(Continuous Integration/Deployment) 파이프라인 통합

대용량 비정형 데이터의 경우 Spark가 ELT의 Transform 엔진으로 동작한다.

```python
# Spark ELT Transform 예시
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

spark = SparkSession.builder.appName("ELT-Transform").getOrCreate()

# RAW 데이터 로드 (Load 단계에서 이미 S3에 저장된 데이터)
raw_df = spark.read.parquet("s3://data-lake/raw/orders/")

# Transform: 타입 변환, 필터, 집계
transformed_df = (
    raw_df
    .withColumn("order_date", to_date(col("order_date_str")))
    .filter(col("amount") > 0)
    .groupBy("customer_id", "order_date")
    .agg({"amount": "sum"})
)

# 결과를 DW 또는 데이터 마트(Data Mart)에 저장
transformed_df.write.mode("overwrite").parquet("s3://data-lake/mart/daily_orders/")
```

---

## 6. 기대효과 및 결론

기술사 답안에서는 **"변환 병목의 위치가 아키텍처 선택을 결정한다"**는 관점에서 서술해야 한다.

ETL vs ELT (Extract-Transform-Load vs Extract-Load-Transform) 클라우드 전이의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
ETL: Extract → Transform → Load (DW 외부 변환)
    │ 클라우드 컴퓨팅 저렴화
    ▼
ELT: Extract → Load → Transform (DW 내부 변환)
    ├─► dbt: SQL 기반 변환 자동화
    └─► BigQuery · Snowflake 컴퓨팅 활용
    │
    ▼
실시간 ETL/ELT: Kafka + Flink 스트리밍 변환
```
2. ELT는 책을 일단 도서관에 다 가져다 넣고, 도서관 안에 있는 빠른 기계로 분류하는 방식이야.
3. 어느 게 더 좋냐고? 도서관(클라우드)이 크고 빠르다면 ELT가 훨씬 편리해 — 책을 기다리게 하지 않아도 되거든!

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| ETL 변환 도구 | Informatica / Talend / SSIS | 전통 온프레미스 ETL 도구 |
| ELT 변환 도구 | dbt (Data Build Tool) | SQL 기반 ELT Transform 프레임워크 |
| ELT 엔진 | Apache Spark | 대규모 분산 변환 처리 |
| 클라우드 DW | Snowflake / BigQuery / Redshift | ELT 변환을 내부에서 수행 |
| 데이터 계층 | RAW → STAGING → MART | ELT의 3단계 레이어 구조 |
| 역방향 | Reverse ETL | DW → 운영 시스템으로 역방향 이동 |
