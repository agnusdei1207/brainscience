+++
weight = 210
title = "210. 데이터 레이크하우스 (Data Lakehouse)"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++

## 0. 핵심 인사이트

> **핵심**: 데이터 레이크하우스 (Data Lakehouse)의 본질은 데이터 레이크의 유연성/확장성과 DW의 ACID 트랜잭션 성능을 융합한 차세대 플랫폼 (Databricks 델타 레이크 등)를 비즈니스 가치, 통제, 실행 관점에서 일관되게 연결하는 데 있다.
> **비유**: 대형 프로젝트의 건강 상태를 수치로 읽어 내는 계기판과 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

데이터 레이크는 원시 데이터를 저렴하게 저장하지만, ACID 부재로 인한 "데이터 스왐프(Data Swamp)" 문제, 스키마 불일치, ML과 SQL 간 도구 분리가 단점이다. 반면 DW는 정형 데이터에 강하지만 비정형·반정형 데이터 처리, ML 피처(Feature) 데이터 통합, 클라우드 오브젝트 스토리지 직접 활용에 제약이 있다.

2020년 Databricks가 제안한 Lakehouse 패러다임은 오브젝트 스토리지를 단일 진실 원천(Single Source of Truth)으로 유지하면서, 그 위에 **메타데이터 레이어(Open Table Format)**를 추가해 DW 수준의 신뢰성을 달성한다. 이로써 데이터 엔지니어·데이터 과학자·SQL 분석가가 동일 데이터를 서로 다른 도구로 접근할 수 있다.

| 포맷 | 주도 | 핵심 특징 |
|:---|:---|:---|
| **Delta Lake** | Databricks | 트랜잭션 로그(_delta_log), Spark 네이티브 |
| **Apache Iceberg** | Netflix/Apple | 열 수준 통계, Hidden Partitioning, 멀티엔진 |
| **Apache Hudi** | Uber | Upsert 최적화, CDC(Change Data Capture) 친화 |

---

## 2. 구성요소

```
┌─────────────────────────────────────────────────────────────┐
│              Delta Lake Lakehouse Architecture              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Object Storage (S3 / GCS / ADLS)       │   │
│  │  ┌───────────────────┐   ┌──────────────────────┐   │   │
│  │  │   Parquet Files   │   │   _delta_log/        │   │   │
│  │  │  (Data Files)     │   │  ┌────────────────┐  │   │   │
│  │  │  part-0001.parquet│   │  │ 00000.json     │  │   │   │
│  │  │  part-0002.parquet│   │  │ 00001.json     │  │   │   │
│  │  │  part-0003.parquet│   │  │ 00002.checkpoint│  │   │   │
│  │  └───────────────────┘   │  └────────────────┘  │   │   │
│  │                          └──────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│               ▲                        ▲                    │
│               │   트랜잭션 보장         │  메타데이터 추적   │
│  ┌────────────┴────┐        ┌──────────┴──────────┐        │
│  │  Query Engine   │        │  Metadata Layer     │        │
│  │ ┌─────────────┐ │        │  - Schema 관리      │        │
│  │ │ Apache Spark│ │        │  - ACID 로그        │        │
│  │ │ Trino/Presto│ │        │  - Time Travel      │        │
│  │ │ Flink       │ │        │  - Data Versioning  │        │
│  │ └─────────────┘ │        └─────────────────────┘        │
│  └─────────────────┘                                        │
└─────────────────────────────────────────────────────────────┘
```

Delta Lake는 오브젝트 스토리지가 기본적으로 ACID를 지원하지 않는 문제를 **트랜잭션 로그(_delta_log)** 로 해결한다. 모든 쓰기 작업은 원자적으로 JSON 로그 파일에 기록되며, 충돌 감지 시 낙관적 동시성 제어(Optimistic Concurrency Control)를 적용한다. 이로써 다수의 Spark 작업이 동시에 같은 테이블을 읽고 쓰더라도 일관성이 유지된다.

```sql
-- 특정 버전으로 데이터 조회
SELECT * FROM delta.`/data/sales` VERSION AS OF 10;

-- 특정 시점 기준 조회
SELECT * FROM delta.`/data/sales` TIMESTAMP AS OF '2026-01-01 00:00:00';

-- 이전 버전으로 롤백
RESTORE TABLE sales TO VERSION AS OF 5;
```

---

## 3. 구조 및 원리

| 항목 | Delta Lake | Apache Iceberg | Apache Hudi |
|:---|:---|:---|:---|
| **주도 조직** | Databricks | Netflix, Apple | Uber |
| **파티션 방식** | 디렉터리 기반 | Hidden Partitioning | 파티션 진화 지원 |
| **Upsert 성능** | MERGE 지원 | MERGE 지원 | Copy-on-Write / Merge-on-Read |
| **멀티엔진** | Spark 중심 | Flink, Trino, Spark | Spark, Flink |
| **Time Travel** | 버전·타임스탬프 | 스냅샷 기반 | 커밋 타임라인 |
| **강점** | Spark 생태계 통합 | 대규모 테이블 관리 | CDC, 근실시간 수집 |

| 계층 | 별칭 | 데이터 상태 | 처리 내용 |
|:---|:---|:---|:---|
| **Bronze** | Raw Layer | 원시 데이터 | 소스 그대로 적재, 변경 불가 이력 보존 |
| **Silver** | Cleansed Layer | 정제 데이터 | 중복 제거, 형식 통일, 기본 품질 검증 |
| **Gold** | Curated Layer | 집계·비즈니스 데이터 | 도메인별 집계, BI/ML 최종 소비 |

---

## 4. 비교 및 연결

| 조건 | 권장 아키텍처 |
|:---|:---|
| 정형 데이터, 고정 스키마, SQL 분석 중심 | 전통적 DW (Snowflake, BigQuery) |
| 비정형 포함, ML/AI 워크로드, 비용 민감 | Data Lakehouse (Delta Lake, Iceberg) |
| 실시간 CDC + 배치 혼합 | Hudi 기반 Lakehouse |
| 완전 관리형, Spark 생태계 | Databricks Lakehouse Platform |
| 레거시 DW + 신규 Lake 통합 | 점진적 Lakehouse 전환 |

Lakehouse에서는 운영 중 스키마를 변경해도 기존 데이터가 유효하게 유지된다. Delta Lake는 `MERGE SCHEMA` 옵션으로 새 컬럼 추가를 자동 처리하며, 하위 호환성(Backward Compatibility)을 보장한다.

```python

df.write.format("delta") \
    .option("mergeSchema", "true") \
    .mode("append") \
    .save("/data/sales")
```

- **Lakehouse vs DW vs Data Lake 3각 비교**: 각 아키텍처의 설계 원칙, 적합 워크로드, 비용 구조
- **Delta Lake ACID 구현 원리**: 트랜잭션 로그 구조, 낙관적 동시성 제어
- **Medallion Architecture**: Bronze/Silver/Gold 3계층의 역할과 데이터 품질 단계
- **Time Travel 활용 시나리오**: GDPR 삭제 요청, 실수 데이터 복원, 데이터 감사

---

## 5. 실무 적용 및 판단

| 효과 | 설명 |
|:---|:---|
| **인프라 단순화** | DW + Data Lake 이중 관리 → 단일 플랫폼으로 통합 |
| **데이터 신선도 향상** | 배치(Batch) + 스트리밍 통합 처리로 Near-Real-Time 분석 |
| **ML/BI 통합** | 동일 데이터셋에서 SQL 분석과 ML 피처 엔지니어링 동시 수행 |
| **비용 절감** | 클라우드 오브젝트 스토리지 단가($0.02/GB) 활용, DW 스토리지 대비 10분의 1 수준 |
| **거버넌스 강화** | ACID + 타임 트래블로 데이터 감사 및 규정 준수 용이 |

Lakehouse는 **데이터 메시(Data Mesh)** 와 결합하여 도메인별 분산 Lakehouse를 연합하는 방향으로 진화하고 있다. 또한 Apache Arrow 기반 인메모리 컬럼 포맷과 결합하여 쿼리 성능이 지속적으로 향상되고 있으며, **AI/ML 피처 스토어(Feature Store)** 와 네이티브 통합이 표준화되는 추세다.

Lakehouse는 "하나의 플랫폼으로 모든 데이터 워크로드를"이라는 목표로 기업 데이터 아키텍처의 미래 표준으로 자리잡고 있다.

---

## 6. 기대효과 및 결론

데이터 레이크하우스 (Data Lakehouse)를 올바르게 적용하면 의사결정의 일관성, 운영의 재현성, 통제의 추적성이 동시에 향상된다. 즉 “누가 무엇을 왜 했는가”가 남기 때문에 조직이 커질수록 효과가 커진다.

다만 데이터 레이크하우스 (Data Lakehouse)는 문서만 잘 만들어도 성공하는 영역이 아니다. 정의와 실행이 분리되면 형식주의가 되고, 자동화만 앞서면 통제 목적이 사라진다. 따라서 표준화와 민첩성, 통제와 생산성 사이의 균형이 항상 필요하다.

향후에는 정책 코드화(Policy as Code), 실시간 관측성(Observability), AI 기반 이상 탐지와 의사결정 지원이 결합되면서 관리 체계가 더 자동화되고 증거 중심으로 진화할 가능성이 크다. 결론적으로 핵심은 도구가 아니라 기준선이며, 기준선이 명확할 때만 자동화와 확장이 의미를 가진다.

---

## 7. 발전 흐름도

```text
수작업 보고
    ↓
표준 지표 정의
    ↓
데이터 레이크하우스 (Data Lakehouse) 정착
    ↓
대시보드 기반 모니터링
    ↓
예측형 의사결정
```

---

## 8. 관련 개념 맵

| 개념 | 설명 | 연관 키워드 |
|:---|:---|:---|
| Delta Lake | Databricks의 오픈 테이블 포맷 | 트랜잭션 로그, ACID, Time Travel |
| Apache Iceberg | Netflix 주도 오픈 테이블 포맷 | Hidden Partitioning, 멀티엔진 |
| Apache Hudi | Uber 주도 CDC 친화 포맷 | Upsert, MoR, CoW |
| Medallion Architecture | Bronze/Silver/Gold 3계층 데이터 품질 모델 | 데이터 레이크, 품질 관리 |
| Time Travel | 과거 버전 데이터 조회·복원 | 버전 관리, GDPR, 데이터 감사 |
| Schema Evolution | 운영 중 스키마 변경 허용 | 하위 호환성, mergeSchema |
| ACID (Atomicity/Consistency/Isolation/Durability) | 트랜잭션 4대 특성 | 동시성 제어, 낙관적 잠금 |
| Feature Store | ML 피처 저장·재사용 저장소 | MLOps, Feast, Tecton |
