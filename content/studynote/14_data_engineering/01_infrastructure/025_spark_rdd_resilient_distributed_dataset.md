+++
weight = 25
title = "25. Spark RDD (Resilient Distributed Dataset) — 내결함성 분산 데이터셋"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: RDD (Resilient Distributed Dataset, 내결함성 분산 데이터셋)는 Apache Spark의 핵심 추상화로, 클러스터 전체에 분산된 불변(Immutable) 데이터 파티션의 집합이다. Resilient는 "복원력 있는(내결함성)"을 의미하며, 리니지(Lineage) 정보를 통해 노드 장애 시 실패한 파티션만 재계산하여 자동 복구한다.
> **비유**: 여러 공정이 연결된 생산 라인처럼, 앞단의 입력 품질과 중간 단계의 흐름 제어가 최종 결과를 좌우하는 구조와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

Spark RDD (Resilient Distributed Dataset) — 내결함성 분산 데이터셋은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```text
┌────────────────────────────────────────────────────────────┐
│              RDD 핵심 특성                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. 분산 (Distributed): 여러 노드에 파티션으로 분산 저장     │
│  2. 불변 (Immutable): 한번 생성 후 수정 불가, 변환만 가능    │
│  3. 내결함성 (Resilient): 리니지 그래프로 자동 재계산 복구   │
│  4. 지연 실행 (Lazy): Action 호출 시만 실제 계산 수행        │
│  5. 타입 안전 (Type-safe): 컴파일 타임 타입 체크              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```python
from pyspark import SparkContext
sc = SparkContext()

# 1. RDD 생성
rdd = sc.textFile("s3://bucket/data.txt")  # 외부 데이터에서 생성

# 2. Transformation (변환) - Lazy: 실행 계획만 등록
words = rdd.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda w: (w, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)

# 3. Action (액션) - Eager: 실제 계산 트리거
result = counts.collect()   # 드라이버로 수집
counts.saveAsTextFile("s3://bucket/output")  # 저장
```

---

## 3. 구조 및 원리

**핵심 조건**: Spark RDD (Resilient Distributed Dataset) — 내결함성 분산 데이터셋은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```text
Spark API 계층:
┌───────────────────────────────────────────────┐
│      고수준 (High-Level)                        │
│  Spark SQL / DataFrames / Datasets (ML, ETL)   │
│      ↓ Catalyst Optimizer + Tungsten           │
│      중수준 (Mid-Level)                         │
│  Dataset[T] (Scala/Java 타입 안전 DataFrame)   │
│      ↓ RDD 기반 실행                            │
│      저수준 (Low-Level)                         │
│  RDD (직접 파티션/셔플 제어 필요 시)             │
└───────────────────────────────────────────────┘
```

---

## 4. 비교 및 연결

```text
textFile → flatMap → map → reduceByKey
   ↓           ↓       ↓        ↓
Stage1:    Stage2:  Stage2:  Stage3:
읽기       변환     변환    셔플+집계

리니지 (Lineage):
rdd → words → pairs → counts
      (만약 pairs 손실 → words부터 재계산)
```

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:---|:---|
| **인메모리 처리** | MapReduce 대비 10~100배 성능 향상 |
| **내결함성** | 리니지 기반 자동 장애 복구 |
| **유연성** | 커스텀 파티셔닝·직렬화 완전 제어 |

Spark 3.x에서 RDD는 Adaptive Query Execution (AQE)과 직접 통합되지 않아 DataFrame 대비 자동 최적화 혜택이 적다. GraphX, MLlib의 내부 구현은 여전히 RDD 기반이나, 사용자 API는 DataFrame 기반으로 이전하고 있다.

| 항목 | RDD | DataFrame |
|:---|:---|:---|
| **스키마** | 없음 (타입 추론 없음) | 있음 (컬럼 이름·타입) |
| **최적화** | 없음 (수동 최적화) | Catalyst Optimizer 자동 최적화 |
| **직렬화** | Java 직렬화 (느림) | Tungsten 인코더 (빠름) |
| **사용 권장** | 비정형 데이터, 커스텀 파티셔닝 | 정형 데이터, 일반 분석 |

```python
# DataFrame은 조인 키 기반 파티셔닝만 지원
# 커스텀 파티셔닝이 필요한 경우 RDD 직접 사용
from pyspark import SparkContext

def hash_partition(key):
    # 특정 비즈니스 로직 기반 파티셔닝
    return ord(key[0]) % 100

graph_rdd = sc.parallelize(edges)     .partitionBy(100, hash_partition)     .persist()  # 반복 접근을 위해 메모리 캐시

# 그래프 알고리즘 반복 실행 (ML, PageRank 등)
for i in range(100):
    graph_rdd = graph_rdd.map(update_function)
```

단순 집계·필터링에 RDD를 사용하는 안티패턴. DataFrame이 동일 로직에서 Catalyst 최적화로 2~5배 빠르다. RDD는 DataFrame으로 표현 불가한 복잡한 커스텀 로직에만 사용해야 한다.

---

## 6. 기대효과 및 결론

Spark 3.x에서 RDD는 Adaptive Query Execution (AQE)과 직접 통합되지 않아 DataFrame 대비 자동 최적화 혜택이 적다.

Spark RDD (Resilient Distributed Dataset) — 내결함성 분산 데이터셋의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
[MapReduce — 디스크 기반 분산 처리, 느림]
    │
    ▼
[Spark RDD — 인메모리 분산 처리, 리니지 기반 복구]
    │
    ▼
[DataFrame/Dataset — 스키마+Catalyst 자동 최적화]
    │
    ▼
[Structured Streaming — 통합 배치·스트리밍 API]
    │
    ▼
[Delta Lake + Spark — ACID 트랜잭션 레이크하우스]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **DataFrame/Dataset** | RDD 기반의 고수준 최적화 API |
| **Catalyst Optimizer** | DataFrame의 자동 쿼리 최적화 엔진 |
| **리니지 (Lineage)** | RDD 내결함성의 핵심 메커니즘 |
| **DAG 스케줄러** | RDD 연산 그래프를 Stage로 분해 |
| **Tungsten** | 메모리·CPU 효율 최적화 실행 엔진 |
