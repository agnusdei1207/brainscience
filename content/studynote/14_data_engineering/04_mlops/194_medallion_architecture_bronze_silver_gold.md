+++
weight = 194
title = "194. 메달리온 아키텍처 (Medallion Architecture) Bronze/Silver/Gold 테이블 정제 적재"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: 메달리온 아키텍처(Medallion Architecture)는 원시 데이터(Bronze) → 정제 데이터(Silver) → 비즈니스 집계(Gold) 3계층으로 데이터 품질을 점진적으로 향상하는 데이터 레이크하우스 설계 패턴이다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

Databricks가 정의한 메달리온 아키텍처는 전통적 데이터 웨어하우스의 경직성과 데이터 레이크의 품질 문제를 동시에 해결하는 **데이터 레이크하우스(Lakehouse)** 설계 패턴이다.

---

## 2. 구성요소

| 아키텍처 | 문제점 |
|:---|:---|
| 전통 데이터 웨어하우스 | 스키마 변경 어려움, 비정형 데이터 처리 불가 |
| 데이터 레이크 (단순) | "데이터 늪(Data Swamp)" — 품질 관리 부재 |
| 람다 아키텍처 | 배치/스트림 코드 이중화, 운영 복잡성 |

---

## 3. 구조 및 원리

**핵심 조건**: 메달리온 아키텍처 (Medallion Architecture) Bronze/Silver/Gold 테이블 정제 적재은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 항목 | Inmon DW | Kimball DM | Data Vault | 메달리온 |
|:---|:---|:---|:---|:---|
| 설계 원칙 | 3NF 정규화 | 스타 스키마 | Hub-Satellite | 계층별 품질 향상 |
| 스키마 유연성 | 낮음 | 중간 | 높음 | 매우 높음 |
| 원본 보존 | 없음 | 없음 | 있음(Hub) | 완전 보존(Bronze) |
| 학습 난이도 | 높음 | 중간 | 높음 | 낮음 |
| 비정형 데이터 | 불가 | 불가 | 어려움 | 가능 |
| 재처리 용이성 | 어려움 | 어려움 | 중간 | 쉬움(Bronze 재처리) |
| 주요 도구 | Teradata, Oracle | Redshift, Snowflake | Snowflake, dbt | Databricks, Delta |

```
데이터 접근 권한 계층화

╔══════════════════════════════════════════╗
║  GOLD          (비즈니스 사용자, 분석가)  ║
║  ─ 최종 집계 데이터 조회                 ║
║  ─ BI 도구 (Tableau, Power BI) 연결     ║
╠══════════════════════════════════════════╣
║  SILVER         (데이터 분석가, 데이터팀) ║
║  ─ 정제된 데이터 분석                    ║
║  ─ 머신러닝 피처 엔지니어링              ║
╠══════════════════════════════════════════╣
║  BRONZE          (데이터 엔지니어만)      ║
║  ─ 원시 데이터 접근                     ║
║  ─ 재처리 및 디버깅                     ║
╚══════════════════════════════════════════╝
```

| 계층 | 스트리밍 처리 방식 |
|:---|:---|
| Bronze | Kafka/Kinesis → Delta Streaming Writer |
| Silver | Structured Streaming + Trigger.Once |
| Gold | Micro-batch 집계 (5분~1시간 윈도우) |

---

## 4. 비교 및 연결

```
단계 1: Bronze 구성 (1주)
  ├─ 소스 시스템별 Kafka 토픽 연결
  ├─ Delta Lake 테이블 생성
  └─ Auto Loader로 자동 적재 설정

단계 2: Silver 구성 (2~4주)
  ├─ 데이터 품질 규칙 정의
  ├─ PII 마스킹 정책 적용
  └─ Great Expectations 데이터 검증

단계 3: Gold 구성 (지속적)
  ├─ 비즈니스 지표 정의 (KPI)
  ├─ dbt 모델로 변환 로직 관리
  └─ BI 도구 연결
```

| 도구 | 계층 | 기능 |
|:---|:---|:---|
| Great Expectations | Bronze→Silver | 데이터 검증 규칙 |
| dbt Tests | Silver→Gold | SQL 기반 테스트 |
| Delta Lake Constraints | Bronze | 제약 조건 강제 |
| Databricks DLT (Delta Live Tables) | 전체 | 선언적 파이프라인 |

```
[주문 이벤트 발생]

    Kafka Topic: order-events
         │
         ▼
    BRONZE: orders_raw
    ┌─────────────────────────────────────┐
    │ order_id, raw_json, ingested_at,    │
    │ source_system, partition, offset    │
    │ (변환 없음, 장기 보존)               │
    └────────────────┬────────────────────┘
                     │ Spark Streaming
                     ▼
    SILVER: orders_cleaned
    ┌─────────────────────────────────────┐
    │ order_id, user_id_hash, amount,     │
    │ status, created_at(timestamp),      │
    │ (중복 제거, PII 해시, 타입 변환)     │
    └────────────────┬────────────────────┘
                     │ dbt 모델
                     ▼
    GOLD: daily_order_summary
    ┌─────────────────────────────────────┐
    │ date, total_orders, total_revenue,  │
    │ avg_order_value, cancellation_rate  │
    │ (일별 KPI 집계)                     │
    └─────────────────────────────────────┘
```

| 비교 항목 | 선택 기준 |
|:---|:---|
| 메달리온 선택 | 스키마 불확실, 비정형 데이터 많음, 애자일 환경 |
| Kimball 선택 | 안정적 쿼리 패턴, OLAP 성능 최우선 |
| Inmon 선택 | 대기업 표준화, 복잡한 데이터 거버넌스 |
| Data Vault 선택 | 이력 관리 최우선, 규제 산업 |

---

## 5. 실무 적용 및 판단

| 효과 | 정량 지표 |
|:---|:---|
| 데이터 품질 향상 | Bronze → Gold 오류율 95% 감소 |
| 재처리 용이성 | Bronze 원본으로 언제든 재처리 |
| 거버넌스 강화 | 계층별 접근 권한으로 보안 강화 |
| 개발 생산성 | dbt 모듈화로 변환 로직 재사용 |
| 장애 복구 | Delta Time Travel로 즉시 롤백 |

```
메달리온 데이터로 ML 파이프라인 구성

GOLD 레이어 피처 데이터
    │
    ▼
Feature Store (Databricks / Feast)
    │
    ├──→ 모델 학습 (MLflow 추적)
    └──→ 온라인 서빙 (Redis 조회)
         실시간 예측 API
```

메달리온 아키텍처는 데이터 레이크의 "데이터 늪" 문제를 계층별 품질 향상으로 해결하는 실용적 패턴이다. Delta Lake와의 결합으로 ACID 보장, 시간 여행, 스키마 진화를 모두 지원하며, 기술사 관점에서는 **스키마 유연성 vs 쿼리 성능** 트레이드오프를 이해하고, 조직의 데이터 성숙도에 맞는 아키텍처 선택 근거를 제시할 수 있어야 한다.

```
외부 데이터 소스
(운영 DB, 로그, API, 스트림)
        │
        ▼
┌───────────────────┐
│   BRONZE 레이어    │  ← 원시 데이터 그대로 적재
│   (동메달)         │    스키마 없음, 이력 보존
└────────┬──────────┘
         │ 정제/검증 ETL
         ▼
┌───────────────────┐
│   SILVER 레이어    │  ← 정제·표준화 데이터
│   (은메달)         │    PII 마스킹, 중복 제거
└────────┬──────────┘
         │ 집계/비즈니스 로직
         ▼
┌───────────────────┐
│    GOLD 레이어     │  ← 비즈니스 집계 데이터
│   (금메달)         │    Feature Store, 대시보드
└───────────────────┘
```

Bronze는 소스 시스템에서 데이터를 **있는 그대로(Raw)** 적재하는 레이어다. 변환 없이 원본 보존이 핵심이다.

| 특성 | 내용 |
|:---|:---|
| 데이터 형태 | JSON, CSV, Parquet, Avro, 이진 데이터 |
| 스키마 | Schemaless 또는 느슨한 스키마 |
| 목적 | 감사 추적(Audit), 재처리 원본 |
| 보존 기간 | 무기한 (규정에 따라) |
| 접근 권한 | 엔지니어만 접근 |

```
Bronze 레이어 적재 예시 (Databricks)

df = spark.read \
     .format("kafka") \
     .option("kafka.bootstrap.servers", "...") \
     .load()

# 원본 그대로 Delta 저장 (변환 없음)
df.write \
  .format("delta") \
  .mode("append") \
  .save("/mnt/bronze/orders/")
```

Bronze 데이터를 **정제, 검증, 표준화**하여 분석 가능한 형태로 변환한다.

| 처리 항목 | 상세 내용 |
|:---|:---|
| 데이터 타입 캐스팅 | 문자열 → 날짜, 정수 등 |
| 결측값 처리 | NULL 처리, 기본값 설정 |
| 중복 제거 | deduplicate by primary key |
| PII 마스킹 | 이메일, 전화번호 해시화 |
| 스키마 표준화 | 컬럼명 통일, 단위 정규화 |
| 데이터 검증 | not_null, referential integrity |

```
Silver 레이어 변환 예시

from pyspark.sql.functions import col, sha2, to_timestamp

df_bronze = spark.read.format("delta") \
                      .load("/mnt/bronze/orders/")

df_silver = df_bronze \
    .dropDuplicates(["order_id"]) \
    .withColumn("email_masked", sha2(col("email"), 256)) \
    .withColumn("created_at", to_timestamp("created_at_str")) \
    .filter(col("order_id").isNotNull()) \
    .drop("email", "created_at_str")

df_silver.write \
         .format("delta") \
         .mode("overwrite") \
         .option("mergeSchema", "true") \
         .save("/mnt/silver/orders/")
```

Silver 데이터에 **비즈니스 로직을 적용한 집계 데이터**로, 최종 사용자가 직접 소비한다.

| 사용 목적 | 구현 방식 |
|:---|:---|
| 비즈니스 대시보드 | 일/주/월 집계 KPI 테이블 |
| ML Feature Store | 모델 학습용 피처 집계 |
| 데이터 마트 | 부서별 최적화 뷰 |
| 실시간 API 서빙 | 사전 집계된 고성능 조회 |

```
┌─────────────────────────────────────────────────────────┐
│              Delta Lake 핵심 기능                         │
│                                                         │
│  ┌──────────────────┐  ┌──────────────────────────────┐ │
│  │ ACID 트랜잭션     │  │ Time Travel (시간 여행)        │ │
│  │                  │  │                              │ │
│  │ 동시 읽기/쓰기    │  │ DESCRIBE HISTORY orders;     │ │
│  │ 충돌 없는 업데이트│  │ SELECT * FROM orders         │ │
│  │ Commit Log 기반  │  │ VERSION AS OF 5;             │ │
│  └──────────────────┘  └──────────────────────────────┘ │
│                                                         │
│  ┌──────────────────┐  ┌──────────────────────────────┐ │
│  │ Schema Evolution  │  │ Z-Ordering (클러스터링)        │ │
│  │                  │  │                              │ │
│  │ 컬럼 추가 자동 반영│  │ 쿼리 성능 최적화              │ │
│  │ 하위 호환성 유지  │  │ 데이터 스킵핑                 │ │
│  └──────────────────┘  └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

| Delta Lake 기능 | 메달리온 활용 |
|:---|:---|
| ACID 트랜잭션 | Bronze 동시 적재 안전성 |
| Time Travel | Silver 재처리 시 이전 버전 조회 |
| Schema Evolution | Gold 새 컬럼 추가 무중단 |
| OPTIMIZE/VACUUM | 소파일 병합, 만료 버전 정리 |
| Change Data Feed | Bronze → Silver 증분 처리 |

---

## 6. 기대효과 및 결론

메달리온 아키텍처는 데이터 레이크의 "데이터 늪" 문제를 계층별 품질 향상으로 해결하는 실용적 패턴이다.

메달리온 아키텍처 (Medallion Architecture) Bronze/Silver/Gold 테이블 정제 적재의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
Raw 데이터 수집 (CSV · JSON · 로그)
    │
    ▼
Bronze 계층: 원시 데이터 그대로 적재 (append-only)
    │
    ▼
Silver 계층: 정제 · 스키마 적용 · 중복 제거 · 조인
    │
    ▼
Gold 계층: 비즈니스 KPI · 집계 테이블 · ML 피처
    │
    ▼
소비: BI 대시보드 · ML 파이프라인 · Ad-hoc 분석
```
2. Bronze는 마치 창고에 쌓아둔 재료 상자예요. 버리지 않고 다 보관해서, 나중에 "아, 이게 필요했구나!" 할 때 꺼낼 수 있어요.
3. Gold는 손님(사용자)이 바로 쓸 수 있도록 예쁘게 포장된 선물 같아요. 복잡한 계산은 이미 다 끝났고, 바로 숫자만 보면 돼요.

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 아키텍처 패턴 | Medallion Architecture (메달리온) | Bronze/Silver/Gold 3계층 품질 향상 |
| 스토리지 엔진 | Delta Lake | ACID + Time Travel + Schema Evolution |
| 비교 | Inmon DW | 3NF 정규화 기반 DW |
| 비교 | Kimball DM | 스타 스키마 기반 DM |
| 비교 | Data Vault | Hub-Satellite 이력 관리 |
| 플랫폼 | Databricks Lakehouse | 메달리온 표준 구현 환경 |
| 품질 관리 | Great Expectations | 데이터 검증 프레임워크 |
| 변환 관리 | dbt | SQL 기반 Silver→Gold 변환 |
| 실시간 처리 | Delta Live Tables (DLT) | 선언적 스트리밍 파이프라인 |
