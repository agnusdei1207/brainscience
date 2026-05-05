+++
weight = 99
title = "24. 실시간 OLAP (Real-time OLAP) — Apache Druid/Pinot/ClickHouse"
date = "2026-04-29"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 실시간 OLAP (Real-time OLAP, Online Analytical Processing)은 스트리밍으로 유입되는 데이터를 수초~수 밀리초의 지연으로 즉시 컬럼형(Columnar) 스토어에 적재하고 서브초(Sub-second) 내에 집계·분석 쿼리를 처리하는 분석 아키텍처로, Apache Druid·Apache Pinot·ClickHouse가 대표 구현체다.
> **비유**: 흐르는 고속도로의 차량을 멈추지 않고 실시간으로 분류하고 통제하는 관제센터와 같다.

📝 모범 답안

## 1. 개요 및 필요성

기존 OLAP(배치 기반 DW)은 데이터 적재부터 분석까지 T+1(다음 날)이 표준이었다. 실시간 마케팅·운영·IoT 환경에서 T+1 분석은 너무 늦다.

```text
┌──────────────────────────────────────────────────────────────┐
│          기존 OLAP vs 실시간 OLAP 비교                         │
├──────────────────────────┬───────────────────────────────────┤
│    기존 OLAP (배치)        │    실시간 OLAP                    │
├──────────────────────────┼───────────────────────────────────┤
│  배치 ETL → T+1 적재       │  스트리밍 직접 적재, T+수초         │
│  야간 집계 (수 시간)        │  서브초(< 1초) 쿼리 응답           │
│  Snowflake, Redshift      │  Druid, Pinot, ClickHouse         │
│  복잡한 JOIN 지원           │  JOIN 제한, 사전 집계 최적화        │
│  정확한 ACID               │  Eventually Consistent            │
└──────────────────────────┴───────────────────────────────────┘
```

---

## 2. 구성요소

### Apache Druid 아키텍처

```text
[이벤트 소스] → Kafka → [실시간 인제스션 노드]
                              │ (실시간 분할·인덱싱)
                              ▼
                    [히스토리컬 노드 (Parquet+인덱스 저장)]
                              │
                    [쿼리 노드 (서브초 집계 처리)]
                              │
                    [브로커 (쿼리 라우팅)]
                              │
                    [대시보드 / API]
```

### 실시간 OLAP 3대 엔진 비교

| 항목 | Apache Druid | Apache Pinot | ClickHouse |
|:---|:---|:---|:---|
| **강점** | 시계열 이벤트 집계 | 낮은 지연 조회 | SQL 편의성, 높은 압축률 |
| **적합 사례** | 광고 클릭 분석, 모니터링 | 실시간 개인화 추천 | 로그 분석, DW 대안 |
| **JOIN** | 제한적 | 제한적 | 광범위 지원 |
| **주요 사용** | Netflix, Uber, Twitter | LinkedIn, Uber Eats | Cloudflare, Yandex |

---

## 3. 구조 및 원리

**핵심 조건**: 이벤트 시간, 상태 저장, 지연 허용, 전달 보장이 함께 통제되어야 한다.

동작 순서:
실시간 OLAP는 람다 아키텍처(Lambda Architecture)의 Speed Layer나 카파 아키텍처(Kappa Architecture)의 스트림 처리 레이어로 통합된다.

| 아키텍처 | 실시간 OLAP 역할 |
|:---|:---|
| **람다 아키텍처** | Speed Layer + Serving Layer |
| **카파 아키텍처** | 스트림 처리 후 서빙 레이어 |
| **레이크하우스** | 실시간 테이블 포맷(Iceberg+Delta)과 결합 |

---

## 4. 비교 및 연결

### 실무 시나리오: 광고 플랫폼 실시간 성과 대시보드
1초 이내 광고 클릭·노출·전환 지표 집계.

1. **소스**: Kafka 클릭 이벤트 (초당 500,000 이벤트).
2. **적재**: Druid 실시간 인제스션 (세그먼트 1분 단위 생성).
3. **사전 집계**: 광고ID × 시간별 클릭/노출/CTR 롤업 저장.
4. **쿼리**: `SELECT ad_id, SUM(clicks), SUM(impressions), AVG(ctr) FROM events WHERE ts > NOW() - INTERVAL '1' HOUR GROUP BY ad_id`
5. **결과**: 200ms 내 응답 → 광고 입찰 실시간 최적화 가능.

### 안티패턴
- 실시간 OLAP로 복잡한 다단계 JOIN 쿼리를 실행하려는 안티패턴. Druid/Pinot는 Star 스키마의 단순한 사실 테이블(Fact Table) 집계에 최적화되어 있고, 복잡한 JOIN은 쿼리 타임아웃을 유발한다. JOIN이 많은 분석은 Snowflake/BigQuery 같은 전통 DW가 적합하다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| **실시간 분석** | 이벤트 발생 후 수초 내 조회 | T+수초 |
| **쿼리 속도** | 수십억 행 집계 서브초 응답 | < 1초 |
| **운영 최적화** | 실시간 지표로 즉각 의사결정 | 광고 CTR 실시간 조정 |

실시간 OLAP는 Apache Iceberg·Delta Lake 기반 스트리밍 테이블과 결합하여 "실시간 레이크하우스(Real-time Lakehouse)" 아키텍처로 발전하고 있으며, ClickHouse의 MaterializedView와 Kafka 직접 연동이 실시간 데이터 파이프라인의 단순화 방향으로 주목받고 있다.

---

## 6. 기대효과 및 결론

실시간 OLAP (Real-time OLAP) — Apache Druid/Pinot/ClickHouse은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 실시간 처리의 경쟁력은 더 빨리 흘리는 것보다 시간 의미와 상태 일관성을 잃지 않는 데 있다.

---

## 7. 발전 흐름도

```text
[배치 OLAP — T+1 적재, 야간 집계, DW]
    │
    ▼
[실시간 OLAP — 스트리밍 즉시 적재, 서브초 쿼리]
    │
    ▼
[Druid/Pinot/ClickHouse — 실시간 OLAP 3대 엔진]
    │
    ▼
[람다/카파 아키텍처 통합 — 배치+실시간 유니파이]
    │
    ▼
[Real-time Lakehouse — Iceberg+Delta+실시간 OLAP]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Apache Druid** | 시계열 이벤트 집계에 특화된 실시간 OLAP |
| **Apache Pinot** | 낮은 지연 조회에 특화된 LinkedIn 오픈소스 |
| **ClickHouse** | SQL 친화적 컬럼형 실시간 OLAP |
| **람다 아키텍처** | Speed Layer에 실시간 OLAP 통합 |
| **컬럼형 스토리지** | 실시간 OLAP 쿼리 성능의 기반 기술 |
