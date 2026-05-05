+++
weight = 176
title = "176. 분산 DB 쿼리 플랜 지연 역추적 (Slow Query Tracing)"
date = "2026-04-21"
[extra]
categories = "studynote-devops-sre"
+++

## 0. 핵심 인사이트

> **핵심**: 분산 DB에서 슬로우 쿼리는 단일 노드 문제가 아니라 여러 샤드·레플리카·네트워크 홉이 뒤얽힌 복합 지연이다.
> **비유**: 분산 DB 슬로우 쿼리 역추적은 마치 여러 도시를 연결하는 택배 네트워크에서 어느 물류 센터에서 지연이 발생했는지 배송 추적 바코드로 찾아내는 것과 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

분산 데이터베이스 환경에서 단일 쿼리는 수십 개의 샤드(Shard)와 레플리카(Replica)에 분산 실행된다. 이때 슬로우 쿼리(Slow Query)는 단순한 "느린 SQL"이 아니라 네트워크 레이턴시, 잠금 대기(Lock Wait), 플랜 캐시 미스(Plan Cache Miss), 파티션 프루닝(Partition Pruning) 실패 등 여러 요인이 겹쳐 발생한다.

전통적인 RDBMS에서는 `EXPLAIN ANALYZE` 한 줄로 문제를 찾을 수 있었지만, TiDB·CockroachDB·Vitess 같은 분산 DB에서는 각 노드가 독립적인 실행 계획을 선택한다. 특정 샤드의 데이터 스큐(Data Skew)나 Hot Spot이 전체 쿼리 지연의 원인이 되어도, 쿼리 레벨 관측 없이는 식별이 불가능하다.

SRE 관점에서 슬로우 쿼리는 서비스 SLO(Service Level Objective) 직격탄이다. 쿼리 하나가 커넥션 풀(Connection Pool)을 고갈시키면 연쇄 타임아웃이 발생한다. 따라서 슬로우 쿼리 탐지를 메트릭·로그·트레이스 세 채널로 동시에 관측하는 통합 파이프라인이 필수다.

OpenTelemetry의 DB Span Attributes(`db.statement`, `db.operation`, `db.sql.table`)를 활용하면 APM(Application Performance Monitoring) 트레이스에 쿼리 계획 정보를 내포할 수 있다. 이를 통해 "어플리케이션 요청 → 게이트웨이 → DB 쿼리 실행 → 특정 샤드 레이턴시"까지 단일 추적으로 역추적(Backtracing)이 가능해진다.

---

## 2. 구성요소

### 분산 쿼리 실행 흐름 및 추적 포인트

```
애플리케이션 (OTel SDK 계측)
       │
       │ Trace ID 생성
       ▼
┌──────────────────────┐
│   DB 드라이버 레이어  │  ← db.statement, db.operation 태깅
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  쿼리 라우터/프록시   │  ← Vitess, ProxySQL, pgBouncer
│  (샤드 결정, 파싱)    │
└──────┬───────┬───────┘
       │       │
  ┌────▼───┐ ┌─▼──────┐
  │ 샤드 A │ │ 샤드 B  │  ← 각 샤드 EXPLAIN 결과 수집
  │ 노드 1 │ │ 노드 2  │
  └────────┘ └────────┘
       │           │
       └─────┬─────┘
             ▼
┌────────────────────────┐
│  슬로우 쿼리 로그 집계  │  ← slow_query.log → Loki/Elasticsearch
│  + 트레이스 스팬 병합   │  ← Jaeger / Tempo
└────────────────────────┘
             │
             ▼
┌────────────────────────┐
│  Grafana 대시보드       │
│  P50/P95/P99 분포      │
│  샤드별 레이턴시 히트맵  │
└────────────────────────┘
```

### 슬로우 쿼리 탐지 계층별 도구

| 계층 | 도구/방법 | 수집 정보 |
|:---|:---|:---|
| DB 엔진 | `slow_query_log`, `pg_stat_statements` | 실행 시간, 행 스캔 수, 잠금 대기 |
| 쿼리 플랜 | `EXPLAIN ANALYZE`, `EXPLAIN FORMAT=JSON` | 비용 추정치, 실제 로우 수, 루프 수 |
| APM 트레이스 | OpenTelemetry DB Span | 전체 호출 경로, 부모-자식 Span |
| 분산 추적 백엔드 | Jaeger, Grafana Tempo | Trace ID 기반 역추적 |
| 메트릭 집계 | Prometheus `histogram_quantile` | P99 레이턴시 SLO 모니터링 |

---

## 3. 구조 및 원리

**핵심 조건**: 측정 가능한 SLI, 합의된 SLO, 실행 가능한 경보·복구 절차가 하나의 폐쇄 루프를 이뤄야 한다.

동작 순서:
1. 사용자 경험을 대표하는 지표를 선택해 서비스 상태를 수치화한다.
2. 허용 가능한 목표치와 에러 버짓을 정해 변화 속도와 안정성의 기준선을 만든다.
3. 메트릭·로그·트레이스로 이상 징후를 탐지하고 원인을 빠르게 국소화한다.
4. 장애 이후 포스트모템과 자동화를 통해 토일을 줄이고 재발 방지책을 시스템에 반영한다.

```text
서비스 요청
   ↓
측정(SLI)
   ↓
목표(SLO)·예산
   ↓
알림·복구
   ↓
학습·자동화
```

1. **탐지(Detect)**: `long_query_time` 임계값 초과 쿼리를 슬로우 쿼리 로그에 기록
2. **상관 분석(Correlate)**: 로그의 Query ID를 Trace Span ID와 JOIN하여 호출 컨텍스트 결합
3. **근본 원인 분석(RCA)**: EXPLAIN 결과에서 Index Scan vs Full Scan 여부, 통계 최신성(Stale Stats) 확인

---

## 4. 비교 및 연결

| 항목 | 단일 RDBMS | 분산 DB |
|:---|:---|:---|
| 쿼리 플랜 | 단일 EXPLAIN으로 충분 | 샤드별 EXPLAIN 필요 |
| 병목 원인 | 인덱스 미사용, Lock | 데이터 스큐, 크로스 샤드 JOIN |
| 추적 도구 | `pg_stat_statements` | OTel + Jaeger 필수 |
| Hot Spot | 테이블 레벨 | 파티션/샤드 레벨 |
| 통계 갱신 | ANALYZE (단일 노드) | 분산 통계 수집 (Global Stats) |

| 기술 | 역할 | 관측 레벨 |
|:---|:---|:---|
| OpenTelemetry | 계측 표준 | 트레이스 + 메트릭 + 로그 통합 |
| Percona Monitoring | MySQL 전용 모니터링 | 쿼리 핑거프린트 분석 |
| pgBadger | PostgreSQL 로그 분석기 | 오프라인 배치 분석 |
| AWS RDS Insights | 관리형 DB 성능 인사이트 | 대기 이벤트 시각화 |

### 슬로우 쿼리 탐지 Prometheus Alert 예시

```yaml
groups:
- name: slow_query
  rules:
  - alert: SlowQueryP99High
    expr: |
      histogram_quantile(0.99,
        rate(db_query_duration_seconds_bucket[5m])
      ) > 1.0
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "P99 쿼리 레이턴시 1초 초과"
      description: "샤드={{ $labels.shard }}, 테이블={{ $labels.table }}"
```

---

## 5. 실무 적용 및 판단

| 시나리오 | 판단 | 근거 |
|:---|:---|:---|
| Full Table Scan 탐지 | 인덱스 추가 또는 쿼리 리팩토링 | `rows_examined >> rows_sent` 비율 |
| 특정 샤드만 슬로우 | 데이터 스큐 → 리샤딩 검토 | 샤드별 P99 히트맵 불균등 |
| 통계 오류(Stale Stats) | `ANALYZE TABLE` 스케줄링 | 쿼리 플랜 비용 추정치 오차 |
| 크로스 샤드 JOIN | 비정규화 또는 읽기 전용 복제본 활용 | 네트워크 홉 수 증가 |
| 커넥션 풀 고갈 | 슬로우 쿼리 킬 + 커넥션 타임아웃 단축 | `Threads_running` 급증 |

분산 DB 슬로우 쿼리 역추적 체계를 구축하면 P99 레이턴시 SLO 위반 사전 감지율이 크게 향상된다. 쿼리 핑거프린트(Fingerprint) 집계를 통해 동일 패턴의 반복 슬로우 쿼리를 조기에 발견하고 인덱스 최적화나 쿼리 리팩토링으로 선제 대응할 수 있다.

OpenTelemetry와 쿼리 플랜 정보의 통합은 "어플리케이션 코드 → DB 쿼리 → 물리적 실행 노드"까지의 전체 인과 관계를 단일 화면에서 확인하는 Full-Stack Observability를 실현한다.

한계로는 실시간 EXPLAIN ANALYZE가 운영 DB에 부하를 줄 수 있으므로 샘플링(Sampling) 비율 조정이 필요하다. 또한 분산 추적 데이터 보존 비용이 높아 핫 데이터(최근 7일)와 콜드 데이터(요약본)를 계층화하는 티어링 전략이 요구된다.

향후에는 AI 기반 쿼리 플랜 자동 제안(Auto-Tuning Advisor)과 결합하여 슬로우 쿼리 탐지 즉시 최적 인덱스를 자동 생성하는 자율 운영(Autonomous Operations) 방향으로 발전할 것이다.

---

## 6. 기대효과 및 결론

분산 DB 쿼리 플랜 지연 역추적 (Slow Query Tracing)을(를) 도입하면 자동화와 표준화를 통해 속도·안정성·가시성의 균형을 높일 수 있다. 다만 효과를 얻으려면 측정 가능한 SLI, 합의된 SLO, 실행 가능한 경보·복구 절차가 하나의 폐쇄 루프를 이뤄야 한다는 전제가 충족되어야 하며, 도구만 도입하고 운영 원칙을 바꾸지 않으면 기대 효과가 빠르게 한계에 부딪힌다.

결론적으로 분산 DB 쿼리 플랜 지연 역추적 (Slow Query Tracing)은(는) 개별 기능이 아니라 운영 체계 전체의 품질을 재정렬하는 방식이며, 향후에는 플랫폼화·정책화·AI 기반 최적화와 결합해 더 높은 수준의 자동 운영으로 확장된다.

---

## 7. 발전 흐름도

```text
전통 운영 모니터링
    ↓
SRE 지표화
    ↓
옵저버빌리티 확장
    ↓
카오스·자동 복구
    ↓
AIOps·예측 운영
```

---

## 8. 관련 개념 맵

| 분류 | 관련 개념 |
|:---|:---|
| 상위 개념 | APM (Application Performance Management), 분산 추적 (Distributed Tracing) |
| 연관 기술 | OpenTelemetry, Jaeger, Grafana Tempo, Prometheus, slow_query_log |
| 비교 대상 | 단일 RDBMS 튜닝 vs 분산 DB 튜닝, pgBadger vs OTel |
