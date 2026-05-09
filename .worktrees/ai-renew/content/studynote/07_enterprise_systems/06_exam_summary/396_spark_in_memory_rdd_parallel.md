+++
weight = 396
title = "396. 스파크 인메모리 RDD 병렬 처리 (Apache Spark: RDD)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Spark는 RDD(Resilient Distributed Dataset)를 메모리에 유지하며 DAG(Directed Acyclic Graph) 실행 계획으로 연산을 지연·최적화하여 MapReduce 대비 10~100배 빠른 인메모리 분산 처리를 실현한다.
> 2. **가치**: 배치·스트리밍·ML·그래프 처리를 단일 프레임워크로 통합하여 데이터 파이프라인 복잡도를 줄이고, Scala·Python·Java·R API를 통한 범용 접근성을 제공한다.
> 3. **판단 포인트**: 지연 평가(Lazy Evaluation)와 액션(Action) 시점의 최적화 실행, 그리고 Shuffle 최소화 전략이 Spark 성능 튜닝의 핵심이다.

## Ⅰ. 개요 및 필요성

UC Berkeley AMPLab이 2009년 개발한 Apache Spark는 Hadoop MapReduce의 디스크 I/O 병목을 인메모리 캐싱으로 해결했다. RDD(Resilient Distributed Dataset)는 메모리에 파티션 단위로 분산 저장되며, Transformation(지연 실행)과 Action(즉시 실행) 연산 체계로 최적 DAG를 구성한 뒤 한 번에 실행한다.

ML(MLlib)·SQL(Spark SQL)·스트리밍(Structured Streaming)·그래프(GraphX)를 하나의 엔진으로 통합하여 데이터 플랫폼의 중심 처리 엔진으로 자리 잡았다.

📢 **섹션 요약 비유**: Spark는 칠판에 적으며 계산하는 천재 — 모든 중간 단계를 칠판(메모리)에 유지하다가 한 번에 최적 경로로 답을 낸다.

## Ⅱ. 아키텍처 및 핵심 원리

```
Driver Program (DAG 생성·배포)
       │
       ▼
  DAG Scheduler
       │
       ▼
┌──────────────────────────────────────────┐
│           Cluster Manager (YARN/K8s)      │
│  ┌──────────────┐   ┌──────────────┐     │
│  │  Executor 1  │   │  Executor 2  │     │
│  │  Task · RDD  │   │  Task · RDD  │     │
│  │  (메모리 캐시) │   │  (메모리 캐시) │     │
│  └──────────────┘   └──────────────┘     │
└──────────────────────────────────────────┘
```

| 개념 | 설명 |
|:---|:---|
| RDD (Resilient Distributed Dataset) | 불변 분산 데이터셋, 파티션 단위 메모리 저장 |
| Transformation | map, filter, join — 지연 평가(Lazy) |
| Action | count, collect, save — 즉시 실행, DAG 트리거 |
| DAG (Directed Acyclic Graph) | Transformation 체인을 최적 실행 계획으로 변환 |
| DataFrame / Dataset | RDD 위의 구조화 API (스키마 + 쿼리 최적화) |

📢 **섹션 요약 비유**: Lazy Evaluation은 장 보기 목록 — 마트 가기 전까지는 목록만 만들고, 마트(Action)에서 한 번에 모든 장을 본다.

## Ⅲ. 비교 및 연결

| 항목 | RDD | DataFrame |
|:---|:---|:---|
| 스키마 | 없음 | 있음 |
| 최적화 | 수동 | Catalyst 쿼리 최적화 자동 |
| 언어 지원 | Java/Scala/Python | 모두 동일 성능 |
| 활용 | 저수준 커스텀 처리 | 구조화 데이터 분석 |

Shuffle 최소화: repartition vs coalesce, broadcast join, partition pruning이 핵심 성능 튜닝 기법이다.

📢 **섹션 요약 비유**: DataFrame은 RDD의 정장 버전 — 같은 사람이지만 구조화된 옷(스키마)을 입어 SQL 최적화기(Catalyst)가 더 잘 이해한다.

## Ⅳ. 실무 적용 및 기술사 판단

**의사결정 포인트**:
- Shuffle 최소화: 작은 테이블은 broadcast join으로 네트워크 전송 제거
- 캐시 전략: `.cache()` vs `.persist(MEMORY_AND_DISK)` — 메모리 초과 시 디스크 fallback
- Executor 메모리 튜닝: `spark.executor.memory`, `spark.memory.fraction`
- 클라우드: Databricks (관리형 Spark), EMR (AWS), Dataproc (GCP)

📢 **섹션 요약 비유**: broadcast join은 작은 책자 복사 배포 — 큰 사전(대형 테이블)은 두고, 작은 안내서(소형 테이블)를 모든 책상(Executor)에 나눠줘 찾기를 빠르게 한다.

## Ⅴ. 기대효과 및 결론

Apache Spark는 인메모리 처리와 DAG 최적화로 배치·스트리밍·ML·SQL을 단일 플랫폼에서 처리하는 현대 데이터 엔지니어링의 표준 엔진이다. 대용량 Shuffle이 성능 병목이 되므로 파티셔닝·broadcast join·캐싱 전략의 체계적 설계가 필수이며, Delta Lake/Iceberg와 결합하면 레이크하우스의 핵심 처리 엔진으로 작동한다.

📢 **섹션 요약 비유**: Spark는 데이터 세계의 스위스 군용 칼 — 배치, 스트리밍, ML, SQL을 하나의 도구로 처리한다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| RDD (Resilient Distributed Dataset) | 핵심 추상화 | 불변 분산 메모리 데이터셋 |
| DAG (Directed Acyclic Graph) | 실행 계획 | 최적화된 연산 실행 순서 |
| Catalyst Optimizer | 쿼리 최적화 | DataFrame/SQL 자동 최적화 엔진 |
| Structured Streaming | 스트리밍 확장 | 마이크로 배치 기반 실시간 처리 |
| Delta Lake | 통합 레이어 | Spark + ACID 트랜잭션 레이크하우스 |

### 👶 어린이를 위한 3줄 비유 설명

1. Spark는 머릿속(메모리)에 모든 것을 기억하는 수학 천재 — MapReduce처럼 종이(디스크)에 쓰고 지우는 것을 안 해도 돼.
2. Lazy Evaluation은 숙제 목록 작성 — 실제로 숙제를 하는 건(Action) 나중에 한 번에 최적으로 해.
3. Shuffle은 모든 아이의 숙제를 과목별로 분류하는 것 — 이게 제일 오래 걸리니까 최소화하는 게 핵심이야!
