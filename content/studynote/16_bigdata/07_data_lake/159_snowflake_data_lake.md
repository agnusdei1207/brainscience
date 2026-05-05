+++
weight = 159
title = "159. Snowflake on Data Lake — External Table과 Iceberg 지원"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Snowflake on Data Lake — External Table과 Iceberg 지원은(는) 원시 데이터 저장의 유연성과 분석 거버넌스의 통제를 함께 확보하기 위한 현대 데이터 플랫폼 핵심 개념이다.
> **비유**: 자유롭게 물을 모으는 저수지에 수문·정수 설비를 함께 갖춘 복합 수자원 시설과 같다.

📝 모범 답안

## 1. 개요 및 필요성

Snowflake는 2012년 Amazon Redshift를 대체할 완전 클라우드 네이티브 DW로 출발했다. 스토리지와 컴퓨팅을 분리하고, 쿼리량에 따라 Virtual Warehouse를 독립적으로 조정하는 혁신적 아키텍처로 시장을 장악했다.

그러나 데이터 레이크하우스 패러다임이 부상하면서 Snowflake는 객체 스토리지의 데이터를 직접 쿼리하는 External Table, 오픈 포맷인 Iceberg Table, 그리고 Python 코드를 Snowflake 내에서 실행하는 Snowpark를 출시하여 레이크하우스 기능을 보강하고 있다.

| Snowflake 진화 단계 | 핵심 기능 | 포지셔닝 |
|:---|:---|:---|
| 1세대 (2014~) | Virtual Warehouse, Time Travel | Cloud DW |
| 2세대 (2018~) | Data Sharing, Secure View | Data Exchange |
| 3세대 (2021~) | Snowpark, External Table | Analytics Platform |
| 4세대 (2023~) | Iceberg Table, Arctic (AI) | Lakehouse + AI |

---

## 2. 구성요소

```
┌──────────────────────────────────────────────────────────────────┐
│               Snowflake 레이크하우스 아키텍처                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │         외부 객체 스토리지 (S3 / ADLS Gen2 / GCS)        │     │
│  │         Parquet / Iceberg 형식 파일                      │     │
│  └──────────────────┬─────────────────────────────────────┘     │
│                     │                                           │
│           ┌─────────┴─────────┐                                 │
│           │                   │                                 │
│  ┌────────▼───────┐  ┌────────▼────────────┐                   │
│  │ External Table │  │ Snowflake-Managed    │                   │
│  │ (메타데이터만)  │  │ Iceberg Table       │                   │
│  │ 스키마 정의,   │  │ (Snowflake가 카탈로그│                   │
│  │ 직접 파일 읽기 │  │  관리, 외부 엔진도   │                   │
│  └────────────────┘  │  읽기 가능)          │                   │
│                      └────────────────────┘                    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │          Virtual Warehouse (컴퓨팅, 독립 스케일)          │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │     │
│  │  │ XSmall   │  │  Large   │  │  Snowpark (Python/   │  │     │
│  │  │ (SQL 분석)│  │  (ETL)   │  │  Java/Scala 실행)    │  │     │
│  │  └──────────┘  └──────────┘  └──────────────────────┘  │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │          Cloud Services Layer (메타데이터·쿼리 최적화)    │     │
│  └────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

**External Table vs Iceberg Table vs Internal Table**

| 항목 | Internal Table | External Table | Iceberg Table |
|:---|:---|:---|:---|
| 데이터 위치 | Snowflake 스토리지 | S3/ADLS/GCS (외부) | S3/ADLS/GCS (외부) |
| 포맷 | Micro-partition (독점) | Parquet/ORC (사용자 관리) | Apache Iceberg |
| ACID 보장 | 완전 | 없음 (읽기 전용) | Iceberg 스펙 따름 |
| 외부 엔진 접근 | 불가 | 파일 직접 접근 가능 | Spark/Trino 등 접근 가능 |
| 타임 트래블 | 90일 | 없음 | Iceberg 스냅샷 |
| 비용 | Snowflake 스토리지 비용 | 외부 스토리지 비용만 | 외부 스토리지 비용만 |

---

## 3. 구조 및 원리

**핵심 조건**: 저장 포맷, 메타데이터, 트랜잭션, 거버넌스 계층을 함께 설계해야 한다.

동작 순서:
**Snowflake vs Databricks — 레이크하우스 관점**

| 항목 | Snowflake | Databricks |
|:---|:---|:---|
| 스토리지 포맷 | 독점(Internal) + Iceberg(External) | Delta Lake (오픈소스) |
| SQL 경험 | 최상 (ANSI SQL 완전 지원) | 좋음 (Spark SQL) |
| ML/AI 지원 | Snowpark ML (성장 중) | 최고 수준 (MLflow 내장) |
| 스트리밍 | Snowpipe (마이크로 배치) | Structured Streaming (진정한 스트리밍) |
| 오픈 포맷 | Iceberg 지원 (부분) | Delta + Iceberg + Hudi |
| 운영 모델 | 완전 서버리스 | 클러스터 관리 일부 필요 |

**Snowpark 활용**
- Python DataFrame API를 Snowflake 내에서 실행 (데이터 이동 없음)
- ML 모델 훈련을 Snowflake Warehouse 위에서 직접 수행
- Snowflake ML Functions: LLM·예측 모델을 SQL 함수처럼 호출

---

## 4. 비교 및 연결

**Snowflake 레이크하우스 도입 시나리오**

- **SQL 우선 조직**: 기존 Snowflake DW 투자 보존 + 레이크 데이터 통합 쿼리
- **비용 최적화**: 비활성 데이터를 Snowflake 스토리지에서 S3 External Table로 이전
- **멀티엔진 환경**: Iceberg Table로 Spark·Trino와 Snowflake가 동일 테이블 공유
- **데이터 공유**: Secure Data Sharing으로 파트너사에 실시간 데이터 피드 제공

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| Virtual Warehouse 동작 | 독립 컴퓨팅 클러스터, 쿼리별 자동 확장, 사용 시간만 과금 |
| External Table 한계 | 파티션 프루닝 효율 낮음, ACID 없음, 쓰기 불가 |
| Iceberg Table 이점 | 외부 엔진과 공유 가능, Iceberg ACID, 파티션 진화 |
| Snowpark 활용 이유 | Python 코드를 Snowflake 내에서 실행 → 데이터 이동 없음 |

---

## 5. 실무 적용 및 판단

| 효과 | 내용 |
|:---|:---|
| 스토리지 비용 절감 | External Table로 비활성 데이터를 저비용 객체 스토리지에 보존 |
| 멀티엔진 유연성 | Iceberg Table로 Spark/Trino/Snowflake 공유 접근 |
| SQL 생산성 유지 | 레이크 데이터를 기존 SQL 쿼리 패턴으로 접근 |
| 데이터 공유 | Snowflake Data Exchange로 파트너사와 실시간 공유 |

Snowflake는 SQL 네이티브 강점을 유지하면서 레이크하우스 기능을 점진적으로 강화하는 전략을 취하고 있다. Iceberg 지원 심화, Snowpark ML 성장, Arctic(AI 통합)이 2024~2025년 주요 방향이다. 기술사 시험에서는 **Virtual Warehouse 스케일 분리 원리**, **External Table vs Internal Table 트레이드오프**, **Snowflake vs Databricks 포지셔닝 비교**가 핵심 논점이다.

---

## 6. 기대효과 및 결론

Snowflake on Data Lake — External Table과 Iceberg 지원은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 레이크하우스 계열 기술은 저장 유연성과 거버넌스 통제를 동시에 달성할 때 비로소 플랫폼 가치가 커진다.

---

## 7. 발전 흐름도

```text
[기존 데이터 웨어하우스 (DW) — 정형 데이터 전용, 비용 높음, 비정형 처리 불가]
    │
    ▼
[데이터 레이크 (Data Lake) — 원시 데이터 모든 형식 저장, 스키마 온 리드]
    │
    ▼
[Snowflake External Table — S3/GCS 오브젝트 스토리지를 Snowflake에서 SQL 조회]
    │
    ▼
[Apache Iceberg 통합 — 오픈 테이블 포맷, ACID 트랜잭션·타임 트래블 지원]
    │
    ▼
[데이터 레이크하우스 (Data Lakehouse) — DW 성능 + 데이터 레이크 유연성 통합]
    │
    ▼
[데이터 메시 (Data Mesh) — 도메인별 분산 소유권, Snowflake Data Sharing 연동]
```
이 흐름은 정형 데이터 전용 DW의 한계를 데이터 레이크로 극복하고, Snowflake의 외부 테이블·Iceberg 통합을 통해 레이크하우스 아키텍처로 수렴하며, 데이터 메시 패러다임과 결합하는 현대 데이터 플랫폼의 진화를 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Virtual Warehouse | 컴퓨팅 레이어 | 독립 스케일, 사용 시간 과금 |
| External Table | 레이크 통합 | 객체 스토리지 직접 쿼리 (읽기 전용) |
| Iceberg Table | 오픈 포맷 통합 | 멀티엔진 공유, ACID 보장 |
| Snowpark | 코드 실행 | Python/Java/Scala Snowflake 내 실행 |
| Data Sharing | 외부 공유 | 복사 없는 실시간 데이터 공유 |
| Micro-partition | 내부 스토리지 | 자동 클러스터링, 16~512MB 블록 |
