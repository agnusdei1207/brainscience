+++
weight = 152
title = "152. 메달리온 아키텍처 (Medallion Architecture) — Delta Lake 기반 3계층"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 메달리온 아키텍처 (Medallion Architecture) — Delta Lake 기반 3계층은(는) 원시 데이터 저장의 유연성과 분석 거버넌스의 통제를 함께 확보하기 위한 현대 데이터 플랫폼 핵심 개념이다.
> **비유**: 자유롭게 물을 모으는 저수지에 수문·정수 설비를 함께 갖춘 복합 수자원 시설과 같다.

📝 모범 답안

## 1. 개요 및 필요성

Multi-Tier Architecture(009)가 개념적 설계 원칙이라면, 메달리온 아키텍처는 이를 **Delta Lake 위에 구현한 Databricks 공식 패턴**이다. Medallion이라는 이름은 Bronze→Silver→Gold가 올림픽 메달처럼 품질이 높아진다는 비유에서 유래했다.

핵심 차별점은 Delta Lake의 ACID 트랜잭션, 타임 트래블, 스키마 진화 기능을 활용하여 각 계층 간 데이터 이동을 신뢰성 있게 처리한다는 점이다. 기존 Hadoop 기반 레이크에서는 파이프라인 중간 실패 시 오염된 데이터가 남아있어 재처리가 복잡했으나, Delta Lake는 원자적 커밋으로 이 문제를 해결한다.

| 구분 | 개념 | Databricks 구현 |
|:---|:---|:---|
| Bronze | 원시 데이터 보존 | AutoLoader + Delta append-only |
| Silver | 정제·조인·이력 | MERGE INTO + SCD Type 2 |
| Gold | 집계·KPI | Spark SQL + dbt + DLT |
| 오케스트레이션 | 계층 간 의존성 | Databricks Workflows / DLT |

---

## 2. 구성요소

```
┌──────────────────────────────────────────────────────────────────┐
│              Medallion Architecture (Databricks 구현)             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐   AutoLoader / COPY INTO                       │
│  │  원본 소스    │ ──────────────────────────▶ 🥉 BRONZE           │
│  │  (S3 Raw)   │                              Delta Table        │
│  └──────────────┘                             - 스키마: 원본 그대로│
│                                               - 파티션: 적재 날짜  │
│                                               - 모드: append-only │
│                                                      │           │
│                              MERGE INTO (upsert)     │           │
│                              + SCD Type 2 변환        │           │
│                                                      ▼           │
│                                              🥈 SILVER           │
│                                              Delta Table         │
│                                              - 중복 제거          │
│                                              - null 처리          │
│                                              - 비즈니스 키 정의    │
│                                              - 품질 기대값 검사    │
│                                                      │           │
│                              Spark SQL / dbt 집계    │           │
│                                                      ▼           │
│                                              🥇 GOLD             │
│                                              Delta Table         │
│                                              - 일별/월별 집계     │
│                                              - Star 스키마        │
│                                              - BI 최적화 파티션   │
│                                                      │           │
│                                          [Power BI / Tableau /   │
│                                           Databricks SQL]        │
└──────────────────────────────────────────────────────────────────┘
```

**Databricks 구현 도구 매핑**

| 계층 | 핵심 도구 | 명령/기능 |
|:---|:---|:---|
| Bronze 수집 | AutoLoader | `cloudFiles` 소스, 자동 스키마 추론 |
| Bronze 수집 (배치) | COPY INTO | 멱등성 보장 파일 적재 |
| Silver 변환 | MERGE INTO | upsert + SCD Type 2 |
| 품질 검사 | DLT Expectations | `@dlt.expect`, `@dlt.expect_or_drop` |
| Gold 집계 | dbt / Spark SQL | 선언적 SQL 변환 |
| 파이프라인 관리 | Delta Live Tables | 의존성 자동 해결, 재처리 지원 |

---

## 3. 구조 및 원리

**핵심 조건**: 저장 포맷, 메타데이터, 트랜잭션, 거버넌스 계층을 함께 설계해야 한다.

동작 순서:
**AutoLoader vs COPY INTO 비교**

| 항목 | AutoLoader | COPY INTO |
|:---|:---|:---|
| 처리 방식 | 스트리밍 (신규 파일 자동 감지) | 배치 (명시적 실행) |
| 멱등성 | 처리된 파일 자동 추적 | 기본 멱등성 보장 |
| 스케일 | 수백만 파일 처리 가능 | 수천 파일 적합 |
| 스키마 추론 | 자동 (컬럼 추가 시 진화) | 수동 지정 |
| 사용 시점 | 지속적 스트리밍 파이프라인 | 일회성/주기적 배치 |

**DLT (Delta Live Tables) 특징**

- 선언적 파이프라인: `@dlt.table` 데코레이터로 의존성 자동 해결
- 품질 기대값: `@dlt.expect_or_drop("valid_price", "price > 0")` 형태로 품질 규칙 코드화
- 증분 처리 자동화: STREAMING TABLE로 선언 시 AutoLoader 기반 증분 처리 자동 구성
- 변경 데이터 캡처: `APPLY CHANGES INTO`로 CDC 스트림을 SCD 테이블로 변환

---

## 4. 비교 및 연결

**Silver 계층 SCD Type 2 구현 패턴**
```sql
MERGE INTO silver.customers AS target
USING bronze.customers_cdc AS source
ON target.customer_id = source.customer_id
  AND target.is_current = true
WHEN MATCHED AND source.updated_at > target.valid_from THEN
  UPDATE SET is_current = false, valid_to = source.updated_at
WHEN NOT MATCHED THEN
  INSERT (customer_id, name, email, valid_from, valid_to, is_current)
  VALUES (source.customer_id, source.name, source.email,
          source.updated_at, '9999-12-31', true)
```

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| Medallion과 Multi-Tier 차이 | Medallion = Delta Lake 기반 구현 표준, Multi-Tier = 일반 설계 원칙 |
| AutoLoader 동작 원리 | S3/ADLS 이벤트 알림 구독 → 신규 파일 자동 감지 → Delta append |
| DLT Expectations 역할 | 품질 규칙 코드화 → 위반 시 격리/드롭/경고 중 선택 가능 |
| Gold 파티션 전략 | 쿼리 필터 기준 컬럼(date, region) 파티션 + Z-ORDER 적용 |

---

## 5. 실무 적용 및 판단

| 효과 | 내용 |
|:---|:---|
| 표준화 | Databricks 사용 조직 간 코드·아키텍처 재사용 |
| 신뢰성 | Delta ACID로 파이프라인 실패 시 오염 없음 |
| 품질 가시성 | DLT Expectations 대시보드로 계층별 품질 지표 실시간 모니터링 |
| 운영 효율 | AutoLoader 자동 스케일링으로 파일 수 증가에도 무중단 운영 |

메달리온 아키텍처는 Databricks 플랫폼의 베스트 프랙티스로 공식화되었으며, 비 Databricks 환경에서도 동일한 원칙을 Apache Spark + Iceberg/Hudi로 구현하는 사례가 늘고 있다. 기술사 시험에서는 **AutoLoader vs COPY INTO 차이**, **SCD Type 2 MERGE 패턴**, **DLT Expectations 품질 관리**가 핵심 논점이다.

---

## 6. 기대효과 및 결론

메달리온 아키텍처 (Medallion Architecture) — Delta Lake 기반 3계층은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 레이크하우스 계열 기술은 저장 유연성과 거버넌스 통제를 동시에 달성할 때 비로소 플랫폼 가치가 커진다.

---

## 7. 발전 흐름도

```text
[원시 데이터 수집 (Raw Ingestion) — 다양한 소스에서 무결 저장]
    │
    ▼
[브론즈 레이어 (Bronze) — 원시 데이터 그대로 보존]
    │
    ▼
[실버 레이어 (Silver) — 정제·표준화·중복 제거]
    │
    ▼
[골드 레이어 (Gold) — 비즈니스 집계·분석용 최종 데이터]
    │
    ▼
[레이크하우스 (Lakehouse) — 메달리온 위에 ACID 트랜잭션 지원]
    │
    ▼
[데이터 메시 (Data Mesh) — 도메인별 메달리온 자율 관리]
```
메달리온 아키텍처는 원시 데이터의 가치를 브론즈→실버→골드 정제 단계로 점진적으로 높이며, 레이크하우스와 데이터 메시의 데이터 품질 기반을 제공한다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| AutoLoader | Bronze 수집 | `cloudFiles` 기반 자동 증분 적재 |
| COPY INTO | Bronze 배치 수집 | 멱등성 보장 명령 |
| MERGE INTO | Silver 변환 | upsert + SCD Type 2 구현 |
| DLT | 파이프라인 관리 | 의존성 자동 해결, 품질 기대값 |
| SCD Type 2 | 이력 관리 | valid_from/valid_to/is_current 패턴 |
| dbt | Gold 집계 | SQL 선언적 변환 도구 |
