+++
weight = 206
title = "206. 아파치 스파크 (Apache Spark) 인메모리 RDD 지연 평가 계보"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: Apache Spark의 RDD (Resilient Distributed Dataset)는 불변성(Immutability)·분산성(Distribution)·내결함성(Fault Tolerance)을 가진 분산 데이터 컬렉션으로, 지연 평가(Lazy Evaluation)와 DAG (Directed Acyclic Graph) 스케줄러를 통해 MapReduce 대비 10~100배 성능을 달성한다.
> **비유**: 여러 공정이 연결된 생산 라인처럼, 앞단의 입력 품질과 중간 단계의 흐름 제어가 최종 결과를 좌우하는 구조와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

2009년 UC 버클리 AMPLab에서 시작된 Spark는 MapReduce의 두 가지 핵심 한계를 해결하기 위해 설계되었다.

| MapReduce 한계 | Spark 해결책 |
|:---|:---|
| 매 단계마다 HDFS 디스크 쓰기 | 인메모리(In-Memory) RDD로 중간 결과 보관 |
| 반복 처리 시 지수적 I/O 증가 | RDD 캐싱으로 반복 연산 시 재사용 |
| Map-Reduce 2단계만 지원 | DAG 기반 복잡한 다단계 연산 표현 가능 |
| 배치 전용 | 배치·스트리밍·ML·SQL 통합 처리 |

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```
K-Means 100 이터레이션 성능 비교
┌──────────────────────────────────────────────────────┐
│  MapReduce:                                          │
│  이터레이션 1: [HDFS 읽기] → 처리 → [HDFS 쓰기]      │
│  이터레이션 2: [HDFS 읽기] → 처리 → [HDFS 쓰기]      │
│  ...100회 반복: 총 200회 HDFS I/O → 시간: ~110분      │
│                                                      │
│  Spark:                                              │
│  이터레이션 1: [HDFS 읽기] → RDD 처리 → [RAM 캐시]   │
│  이터레이션 2: [RAM 읽기] → RDD 처리 → [RAM 캐시]    │
│  ...100회 반복: 1회 HDFS I/O, 나머지 메모리 → ~5분   │
│                                                      │
│  성능 차이: 약 22배 빠름                               │
└──────────────────────────────────────────────────────┘
```

---

## 3. 구조 및 원리

**핵심 조건**: 아파치 스파크 (Apache Spark) 인메모리 RDD 지연 평가 계보은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

RDD는 Spark의 근본 추상화로, 다음 세 가지 핵심 속성을 가진다.

```
RDD 3대 특성
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Resilient (내결함성)                                  │  │
│  │  → 파티션 손실 시 Lineage로 재계산 가능               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Distributed (분산)                                   │  │
│  │  → 파티션 단위로 여러 Executor에 분산 저장·처리       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Dataset (데이터셋)                                    │  │
│  │  → 불변(Immutable) 레코드의 컬렉션                    │  │
│  │  → 변환 시 새 RDD 생성 (원본 수정 안 됨)              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. 비교 및 연결

Spark는 Transformation을 즉시 실행하지 않고, Action이 호출될 때 전체 실행 계획을 최적화하여 한꺼번에 실행한다.

```
지연 평가 동작 방식
┌─────────────────────────────────────────────────────────────┐
│  코드:                                                      │
│  val rdd1 = sc.textFile("hdfs://data")    ← RDD 생성        │
│  val rdd2 = rdd1.filter(_.contains("error"))  ← Transformation│
│  val rdd3 = rdd2.map(_.split(","))            ← Transformation│
│  val result = rdd3.count()                    ← Action ✅   │
│                                                             │
│  실제 실행 시점: count() 호출 시에만 전체 DAG 실행          │
│  최적화: Spark가 filter + map 파이프라인을 한번에 처리       │
│          (Pipeline Fusion으로 중간 RDD 물리화 없음)          │
└─────────────────────────────────────────────────────────────┘
```

| 구분 | 설명 | 즉시 실행? | 예시 |
|:---|:---|:---|:---|
| Transformation | RDD를 새 RDD로 변환 | ❌ (지연) | map, filter, flatMap, groupBy, join |
| Action | 결과를 Driver로 반환하거나 저장 | ✅ (즉시) | count, collect, save, first, reduce |

---

## 5. 실무 적용 및 판단

```
DAG 스케줄러 처리 흐름
┌─────────────────────────────────────────────────────────────┐
│  논리적 DAG (RDD 계보):                                     │
│                                                             │
│  textFile ──▶ filter ──▶ map ──▶ groupBy ──▶ reduce        │
│                                     │                       │
│                              (셔플 발생)                    │
│                                                             │
│  물리적 실행 계획 (Stage 분리):                              │
│                                                             │
│  Stage 1: textFile → filter → map   (파이프라인 가능)       │
│                                     │                       │
│                              [셔플 경계]                    │
│                                     │                       │
│  Stage 2: groupBy → reduce          (셔플 후 실행)          │
└─────────────────────────────────────────────────────────────┘
```

**Stage 분리 기준**: 셔플이 필요한 Wide Transformation (groupBy, join, sortBy 등)이 Stage 경계를 형성한다.

| 변환 유형 | 설명 | Stage 경계 |
|:---|:---|:---|
| Narrow Transformation | 각 파티션이 부모 파티션 1개에만 의존 | ❌ (동일 Stage) |
| Wide Transformation | 여러 부모 파티션에 의존 (셔플 필요) | ✅ (Stage 분리) |
| Narrow 예시 | map, filter, union | - |
| Wide 예시 | groupByKey, join, sortByKey, distinct | - |

```
Lineage 복구 메커니즘
┌─────────────────────────────────────────────────────────────┐
│  초기 상태:                                                  │
│  HDFS → rdd1 → rdd2 → rdd3 (파티션 0,1,2,3)                │
│                                                             │
│  장애: rdd3의 파티션 2 손실                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ❌ 기존 복제 방식: 복제본 필요 (디스크/메모리 2~3배)   │  │
│  │  ✅ Lineage 방식: 계보를 따라 파티션 2만 재계산        │  │
│  │     HDFS 파티션 2 → rdd1_p2 → rdd2_p2 → rdd3_p2      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  장점: 메모리 복제 오버헤드 없음                             │
│  단점: 긴 Lineage의 재계산 비용 → 주기적 체크포인팅 권장    │
└─────────────────────────────────────────────────────────────┘
```

| API | 등장 | 특징 | 성능 |
|:---|:---|:---|:---|
| RDD | Spark 1.0 | 저수준, 타입 안전, 최대 유연성 | 수동 최적화 필요 |
| DataFrame | Spark 1.3 | 고수준, 스키마 기반, Catalyst 최적화 | 자동 최적화 |
| Dataset | Spark 1.6 | RDD 타입 안전성 + DataFrame 최적화 | DataFrame과 동일 |

> **현재 권장**: SparkSQL + Dataset/DataFrame API 사용. RDD는 저수준 제어가 필요한 경우만 사용.

Spark SQL의 Catalyst 쿼리 옵티마이저는 논리 계획(Logical Plan)을 최적화된 물리 계획(Physical Plan)으로 변환한다.

```
Catalyst 최적화 파이프라인
┌──────────────────────────────────────────────────────────────┐
│  SQL/DataFrame 코드                                          │
│          ↓                                                   │
│  Unresolved Logical Plan  (파싱)                             │
│          ↓                                                   │
│  Resolved Logical Plan    (카탈로그 메타데이터 바인딩)         │
│          ↓                                                   │
│  Optimized Logical Plan   (Catalyst 룰 기반 최적화)           │
│          │ 예: Predicate Pushdown, Column Pruning             │
│          ↓                                                   │
│  Physical Plan(s)         (여러 물리 실행 계획 생성)           │
│          ↓                                                   │
│  Selected Physical Plan   (비용 기반 최적 계획 선택)           │
│          ↓                                                   │
│  코드 생성 (Tungsten 엔진)  → JVM 바이트코드 최적화            │
└──────────────────────────────────────────────────────────────┘
```

| 최적화 기법 | 설명 | 효과 |
|:---|:---|:---|
| Predicate Pushdown | WHERE 조건을 최대한 앞 단계(소스)에서 적용 | 불필요한 데이터 로딩 방지 |
| Column Pruning | SELECT에 없는 컬럼 조기 제거 | 컬럼형 파일(Parquet) 효율 극대화 |
| Join Reordering | 작은 테이블을 앞에 배치 | 중간 결과 크기 최소화 |
| Broadcast Join | 작은 테이블을 모든 노드에 브로드캐스트 | 셔플 제거 |

```
캐싱 저장 수준 (Storage Level)
┌────────────────────────────────────────────────────────────┐
│  MEMORY_ONLY      : RAM만 사용, 부족 시 파티션 버림         │
│  MEMORY_AND_DISK  : RAM 우선, 넘치면 디스크 (권장)          │
│  DISK_ONLY        : 디스크만 (장기 캐시)                    │
│  MEMORY_ONLY_SER  : 직렬화해서 RAM에 저장 (메모리 절약)     │
│  OFF_HEAP         : JVM 밖 메모리 (GC 영향 없음)             │
└────────────────────────────────────────────────────────────┘
```

| 단계 | 기술 | 역할 |
|:---|:---|:---|
| 데이터 수집 | Kafka | 클릭 이벤트 실시간 스트리밍 |
| 스트리밍 처리 | Spark Structured Streaming | 10초 마이크로배치 윈도우 처리 |
| 특성 추출 | Spark MLlib ALS | 협업 필터링 모델 피처 계산 |
| 모델 학습 | Spark ML (RDD 캐싱) | K-Means 반복 학습 (메모리 효율) |
| 서빙 | SparkSQL + Redis | 추천 결과 캐시 |

**결과**: MapReduce 기반 대비 모델 학습 시간 1시간 → 5분 (12배 향상)

1. **RDD vs DataFrame 선택 기준**: 타입 안전성과 저수준 제어가 필요한 경우 RDD, 데이터 분석·SQL 중심이면 DataFrame/Dataset을 선택. 구체적 예시와 함께 서술.
2. **지연 평가의 양면성**: 실행 계획 최적화라는 장점이 있지만, `collect()` 전에 에러가 발견되지 않는 디버깅 어려움이 단점. `count()`나 중간 `show()`로 계보 중간 확인 필요.
3. **Lineage vs 체크포인팅**: 짧은 Lineage는 재계산이 빠르지만, Lineage가 수백 단계면 재계산 비용이 크다. `checkpoint()`를 주기적으로 설정해 Lineage를 절단하는 전략을 제시.

| 효과 영역 | 수치 사례 | 설명 |
|:---|:---|:---|
| 배치 처리 속도 | MapReduce 대비 10~100배 향상 | 인메모리 처리, Catalyst 최적화 |
| ML 학습 속도 | MapReduce 대비 100배 (반복 알고리즘) | RDD 캐싱으로 I/O 제거 |
| 코드 간결성 | 코드량 MapReduce 대비 80% 감소 | 고수준 API (SQL, DataFrame) |
| 통합성 | 배치·스트리밍·ML·SQL 단일 플랫폼 | 중복 인프라 제거 |

| 한계 | 현황 | 발전 방향 |
|:---|:---|:---|
| 메모리 의존성 | OOM (Out of Memory) 장애 빈발 | Project Tungsten (오프힙 메모리) |
| 스트리밍 지연 | Structured Streaming 수 초 지연 | Apache Flink (진정한 이벤트 스트리밍) |
| 소규모 파일 | 다수의 소규모 파일 처리 비효율 | Delta Lake, Iceberg (파일 컴팩션) |

---

## 6. 기대효과 및 결론

**Stage 분리 기준**: 셔플이 필요한 Wide Transformation (groupBy, join, sortBy 등)이 Stage 경계를 형성한다.

아파치 스파크 (Apache Spark) 인메모리 RDD 지연 평가 계보의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
MapReduce (디스크 기반, 느림)
    │
    ▼
Spark RDD: 인메모리 · Lazy Evaluation · Lineage 복구
    │
    ▼
DataFrame / Dataset API: 스키마 기반 · Catalyst 최적화
    │
    ▼
Spark SQL · Structured Streaming · MLlib
    │
    ▼
Photon (Databricks) · Spark Connect (원격 실행)
```
2. 지연 평가는 "쇼핑 목록을 다 적은 다음 한 번에 효율적으로 쇼핑하는 것"이에요. 중간에 불필요한 물건을 AI가 목록에서 지워줘요.
3. DAG는 "요리 레시피 흐름도"예요. 어떤 재료(데이터)가 어떤 순서로 섞여야 완성 요리(결과)가 나오는지 그림으로 보여줘요!

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 추상화 | RDD (Resilient Distributed Dataset) | 불변·분산·내결함 데이터 컬렉션 |
| 최적화 원리 | 지연 평가 (Lazy Evaluation) | Action 호출 시 실행 계획 일괄 최적화 |
| 장애 복구 | Lineage (계보) | 파티션 손실 시 재계산 경로 기록 |
| 실행 구조 | DAG (Directed Acyclic Graph) | 변환 단계를 방향성 비순환 그래프로 표현 |
| 최적화 엔진 | Catalyst Optimizer | SQL/DataFrame 쿼리 최적화 |
| 상위 API | DataFrame / Dataset | RDD 위의 고수준 추상화 |
| 관련 기술 | Apache Flink | 진정한 이벤트 스트리밍 (Spark 보완재) |
