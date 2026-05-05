+++
weight = 155
title = "155. ELT vs ETL — 클라우드 시대 데이터 변환 패러다임 전환"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: ELT vs ETL — 클라우드 시대 데이터 변환 패러다임 전환은(는) 원시 데이터 저장의 유연성과 분석 거버넌스의 통제를 함께 확보하기 위한 현대 데이터 플랫폼 핵심 개념이다.
> **비유**: 자유롭게 물을 모으는 저수지에 수문·정수 설비를 함께 갖춘 복합 수자원 시설과 같다.

📝 모범 답안

## 1. 개요 및 필요성

1990~2010년대 온프레미스 데이터 웨어하우스(Oracle, Teradata) 환경에서는 스토리지가 고가였고 컴퓨팅 자원도 제한적이었다. ETL은 이 제약 안에서 필요한 데이터만 정제·압축하여 DW에 적재하는 최적 방식이었다.

클라우드 시대(2010년 이후)에는 S3/ADLS 스토리지 비용이 온프레미스 대비 10~100분의 1 수준으로 하락하고, Spark/BigQuery/Snowflake의 분산 컴퓨팅이 변환 비용을 정규화했다. 이 변화가 ELT 패러다임으로의 전환을 이끌었다.

| 비교 항목 | ETL | ELT |
|:---|:---|:---|
| 변환 위치 | 스테이징 서버 (외부) | DW/레이크하우스 내부 |
| 원시 데이터 보존 | 없음 (변환 후 버림) | 있음 (Raw 계층 보존) |
| 스토리지 사용 | 최소화 (정제 후 적재) | 최대 (Raw + 변환 결과) |
| 재처리 유연성 | 낮음 (원본 없음) | 높음 (Raw에서 재변환) |
| 적합 환경 | 온프레미스 DW | 클라우드 DW / 레이크하우스 |
| 대표 도구 | Informatica, SSIS, Talend | dbt, Spark SQL, Dataflow |

---

## 2. 구성요소

```
┌────────────────────────────────────────────────────────────────┐
│                   ETL vs ELT 비교                               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  【ETL 흐름】                                                   │
│                                                                │
│  [소스] ──Extract──▶ [스테이징 서버]                            │
│                      Transform (정제·집계)                      │
│                           │                                    │
│                           └──Load──▶ [DW] ──▶ [BI 도구]        │
│                                                                │
│  【ELT 흐름】                                                   │
│                                                                │
│  [소스] ──Extract──▶ [레이크하우스 / 클라우드 DW]               │
│                      (Bronze: Raw 적재)                         │
│                           │                                    │
│                    Transform (dbt / Spark SQL)                  │
│                    Silver: 정제  Gold: 집계                     │
│                           │                                    │
│                           └──▶ [BI / ML 도구]                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**dbt (data build tool) 핵심 기능**

| 기능 | 설명 | 장점 |
|:---|:---|:---|
| Model | SQL SELECT로 변환 정의 | 선언적, 재사용 가능 |
| Test | `not_null`, `unique`, `accepted_values` | 변환 결과 자동 품질 검사 |
| Documentation | `description` 필드로 컬럼 문서화 | 자동 데이터 카탈로그 생성 |
| Lineage Graph | 모델 간 의존성 자동 시각화 | 영향 분석 즉시 파악 |
| Materialization | Table / View / Incremental / Ephemeral | 성능·비용 트레이드오프 선택 |
| Seed | CSV로 정적 참조 데이터 관리 | 코드와 데이터 함께 버전 관리 |

**dbt Incremental 모델 패턴**
```text
-- models/silver/orders_cleaned.sql
-- dbt Jinja 매크로 사용
-- { { config(materialized='incremental',
--           unique_key='order_id',
--           on_schema_change='sync_all_columns') } }

SELECT
    order_id,
    customer_id,
    amount,
    created_at
FROM source('bronze', 'orders_raw')
WHERE status != 'cancelled'
-- incremental 조건: 마지막 실행 이후 데이터만 처리
-- AND created_at > (SELECT MAX(created_at) FROM this_model)
```

---

## 3. 구조 및 원리

**핵심 조건**: 저장 포맷, 메타데이터, 트랜잭션, 거버넌스 계층을 함께 설계해야 한다.

동작 순서:
**ELT 도구 비교**

| 도구 | 실행 위치 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| dbt Core | DW/레이크하우스 내부 | 오픈소스, SQL 선언적 | Snowflake, BigQuery, Databricks |
| dbt Cloud | 관리형 SaaS | IDE + 스케줄러 + 협업 | 팀 규모 조직 |
| Spark SQL | 레이크하우스 | Python/Scala 병행 | 대규모 배치 변환 |
| Dataflow | GCP 관리형 | Apache Beam 기반 | GCP 생태계 |
| Glue | AWS 관리형 | Spark 기반, S3 통합 | AWS 생태계 |

**연관 개념 연결**

- **Medallion Architecture**: ELT의 Bronze→Silver→Gold가 Medallion 계층과 완벽히 매핑
- **Data Product**: dbt 모델이 Gold 계층 데이터 제품의 변환 로직을 담당
- **Data Lineage**: dbt가 자동으로 리니지 그래프를 생성하여 Unity Catalog와 연계

---

## 4. 비교 및 연결

**ELT 전환 체크리스트**
- [ ] 원시 데이터를 Bronze 계층에 보존하는 파이프라인 설계
- [ ] dbt 프로젝트 초기화 및 소스 등록 (`dbt source freshness` 설정)
- [ ] Silver 모델: `materialized='incremental'` + `unique_key` 설정
- [ ] Gold 모델: `materialized='table'` + 파티션 설정
- [ ] `dbt test` 실행 CI/CD 파이프라인 통합

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| ETL → ELT 전환 이유 | 클라우드 스토리지 저비용화, 분산 컴퓨팅 확장성 |
| dbt의 역할 | DW 내부 SQL 선언적 변환 + 테스트 + 리니지 자동화 |
| Incremental 모델 장점 | 전체 재처리 없이 새 데이터만 변환 → 비용·시간 절감 |
| ELT 한계 | 원시 데이터 보존으로 스토리지 비용 증가, 민감 데이터 보안 관리 필요 |

---

## 5. 실무 적용 및 판단

| 효과 | 내용 |
|:---|:---|
| 재처리 유연성 | Raw 보존으로 언제든 새 로직으로 소급 재처리 가능 |
| 운영 단순화 | 스테이징 서버 제거, DW 내부에서 모든 변환 처리 |
| 품질 가시성 | dbt test로 변환 결과 품질 자동 검증 |
| 협업 향상 | dbt 모델 = SQL 코드 → Git 버전 관리 + 코드 리뷰 |

ETL에서 ELT로의 패러다임 전환은 클라우드 빅데이터 인프라 확산과 함께 이미 완료된 흐름이다. dbt는 현재 데이터 팀 표준 도구로 자리 잡았으며, Databricks·Snowflake·BigQuery 모두 네이티브 dbt 통합을 지원한다. 기술사 시험에서는 **ETL vs ELT 전환 이유**, **dbt 핵심 기능**, **Incremental 모델 동작 원리**가 핵심 논점이다.

---

## 6. 기대효과 및 결론

ELT vs ETL — 클라우드 시대 데이터 변환 패러다임 전환은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 레이크하우스 계열 기술은 저장 유연성과 거버넌스 통제를 동시에 달성할 때 비로소 플랫폼 가치가 커진다.

---

## 7. 발전 흐름도

```text
[ETL (Extract-Transform-Load) — 소스에서 추출 후 변환, 타겟 DW에 적재]
    │
    ▼
[데이터 웨어하우스 (DW) — 정제된 구조적 데이터 중앙 저장소, ETL 전제]
    │
    ▼
[ELT (Extract-Load-Transform) — 원시 데이터 먼저 적재, 클라우드 DW에서 변환]
    │
    ▼
[데이터 레이크 (Data Lake) — 원시 데이터 무제한 적재, ELT 패러다임과 친화적]
    │
    ▼
[레이크하우스 (Lakehouse) — Delta Lake·Iceberg 기반 ELT + ACID 트랜잭션 통합]
```

이 흐름은 온프레미스 DW를 위한 ETL 패러다임이 클라우드 규모에서 ELT로 전환되고, 데이터 레이크하우스 아키텍처로 통합·발전하는 과정을 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| dbt | ELT 핵심 도구 | SQL 선언적 변환·테스트·리니지 |
| Incremental 모델 | dbt 성능 최적화 | 신규 데이터만 처리 패턴 |
| Bronze 계층 | ELT 전제 조건 | Raw 데이터 영구 보존 |
| Data Lineage | 자동화 산출물 | dbt가 생성하는 모델 의존성 그래프 |
| Medallion Architecture | 연관 패턴 | ELT 흐름 = Bronze→Silver→Gold |
| Schema-on-Read | ELT 특성 | 적재 시 스키마 강제 않음 |
