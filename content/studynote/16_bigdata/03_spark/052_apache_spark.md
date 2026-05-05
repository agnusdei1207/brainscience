+++
weight = 52
title = "01. Apache Spark — 인메모리 분산 처리 엔진 (Unified Analytics Engine)"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Apache Spark — 인메모리 분산 처리 엔진 (Unified Analytics Engine)은(는) 인메모리 분산 실행과 쿼리 최적화를 통해 대화형 분석·배치·스트리밍을 빠르게 연결하는 스파크 핵심 개념이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

RDD는 스파크의 근간이 되는 불변 분산 컬렉션으로, 다음 5가지 속성이 보장되어야 합니다.

| RDD 특성 | 설명 | 예시 |
|:---|:---|:---|
| **불변성 (Immutable)** | 한 번 생성된 RDD는 수정 불가, 새 RDD만 생성 | `rdd.map(x => x * 2)` → 새 RDD 반환 |
| **분산 (Distributed)** | 클러스터 여러 노드에 파티션 단위로 저장 | 10개 노드 × 각 2 파티션 = 20 파티션 |
| **결함 허용 (Resilient)** | Lineage(작업 혈통) 그래프로 손실 자동 복구 | 부모 RDD가 손실되면 재컴퓨팅 |
| **지연 평가 (Lazy Evaluation)** | 액션 호출 전까지 변환 연산을 실행하지 않음 | `collect()` 호출 시 비로소 실행 |
| **파티셔닝 (Partitioned)** | 데이터가 사용자에게 투명하게 분할 저장 | `repartition(n)`으로 파티션 수 조절 |

---

## 2. 구성요소

스파크의 작업 실행은 Stage(단계)로 구분되는 DAG 기반입니다.

1. **사용자 코드 작성**: `sc.textFile("log.txt").filter(_.contains("ERROR")).map(_.split(",")).collect()`
2. **DAG 구성**: 스파크는 이 코드를 lazy evaluation에 따라一棵 DAG 그래프로 기록합니다. `textFile → filter → map`이 노드가 되고, `collect`가 최종 액션 노드가 됩니다.
3. **Stage 분리**: 스파크는 DAG를 분석하여 "Shuffle 경계(데이터를 네트워크로 전송해야 하는 지점)"를 기준으로 Stage를 분리합니다. Shuffle이 필요 없는 파이프라인 연산(pipeline)은同一个 Stage 내에서 모두 실행됩니다.
4. **Task 생성**: 각 Stage는 여러 태스크(Task)로 분할되어 각 파티션에 할당됩니다. 파티션이 100개면 태스크도 100개가 생성됩니다.
5. **실행**: Cluster Manager가 각 노드의 Executor에 태스크를 분배하고, 태스크는 자신의 파티션에 대해 연산을 수행합니다.

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:
| 비교 항목 | Hadoop MapReduce | Apache Spark (인메모리) |
|:---|:---|:---|
| **처리 속도** | 디스크 I/O로 인해 수십 배 느림 | 인메모리 연산으로 최대 100배 빠름 |
| **iterative ML** | 매 반복마다 디스크 읽기/쓰기 → 수일 소요 | 메모리에 데이터 유지 → 수시간 내 수렴 |
| **실시간 스트리밍** | 불가능 (별도 Storm/Spark Streaming 필요) | Structured Streaming으로 통합 처리 가능 |
| **결함 복구** | 중복 데이터로 복구 (3중 복제) | Lineage 그래프로 필요 파티션만 재컴퓨팅 |
| **메모리 요구량** | 낮음 (디스크 기반) | 높음 (클러스터 RAM 용량에 의존) |
| **가장 큰 리스크** | 확장을 해도 디스크 병목이 성능 ceiling이 됨 | OOM(메모리 부족) 시 디스크로 fell back → 성능 급락 |

---

## 4. 비교 및 연결

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **데이터 규모** | 수십 TB 이상일 때 Spark의 인메모리 장점 극대화 | 소규모(수백 GB 이하)엔 Spark 오버헤드大于 Hadoop |
| **iterative 연산 빈도** | ML 훈련, 그래프 분석 등 반복 연산 많을수록 Spark 권장 | 일회성 배치엔 Hadoop도 충분한 경우多 |
| **클러스터 메모리** | 전체 클러스터 RAM이 처리 데이터의 2배 이상일 때 안정적 | 메모리 부족 시 disk spilling으로性能劣化 |
| **실시간 요구 수준** | ms~s 단위 지연 요구 시 Structured Streaming + Flink 비교 필요 | 분 단위 지연 허용 시 Spark Streaming(DStream)도 가능 |

*(추가 실무 적용 가이드 - Spark 배포 모드 선택)*
- **Local 모드**: 개발/테스트용. 드라이버와 Executor가同一个 JVM에서 실행되어 별도 클러스터 필요 없음. 소규모 데이터 디버깅에最適.
- **Standalone 모드**: 스파크 자체内置 클러스터 매니저. 간단한 단일 클러스터 구성에 적합하지만, 프로덕션에서는 YARN/K8s 사용 권장.
- **YARN 모드**: 기존 Hadoop 인프라 활용. HDFS 데이터 محلية 처리로 네트워크 대역폭 절약. Enterprise Hadoop 사용자首选.
- **Kubernetes 모드**: Cloud-native 환경에 최적. Docker 컨테이너 기반으로 스파크 앱을 표준 쿠버네티스 파드として実行. 현대 마이크로서비스 아키텍처와 손색なし 통합.
- **실무 의사결정 트리**: (1) 기존 Hadoop 인프라 있나요? → Yes: YARN, No: (2) Cloud-nativeですか? → Yes: Kubernetes, No: Standalone)

---

## 5. 실무 적용 및 판단

1. **Spark 3.5+의 ANSI SQL 확대 및 Python 네이티브 강화**
   Spark 3.5부터 ANSI SQL:2003 표준 준수가 크게 진행되어 Oracle, PostgreSQL 등 전통 RDBMS에서 작성한 복잡한 SQL 쿼리의大多数를 스파크에서도 그대로 실행할 수 있게 되었습니다. 동시에 PySpark(파이썬)의 API가 네이티브 Scala API에 버금가는 완성도로 성숙하면서, 데이터 엔지니어와 데이터 사이언티스트 간의 언어 장벽이 사실상 사라지고 있습니다.

2. **Lakehouse 시대의 Spark 역할**
   Delta Lake, Apache Iceberg, Apache Hudi 등 레이크하우스 테이블 포맷과 Spark의 결합이 표준화되면서, 데이터 레이크의 원시 데이터에 직접 스파크 SQL을 실행하고 ACID 트랜잭션을 지원하는 "打开된 레이크하우스(Open Lakehouse)" 아키텍처가 빠르게 확산되고 있습니다. Databricks의 Photon Engine(네이티브 벡터화 실행 엔진)이나 Amazon EMR의 Spot Instance 연동 등, 비용 최적화와 성능 극대화를 동시에 추구하는 방향으로 빠르게 진화하고 있습니다.

3. **Adaptive Query Execution (AQE)의 일상화**
   Spark 3.0에서 도입된 AQE는 런타임 통계에 따라 조인 전략, 파티션 수, 데이터 셔플 분할을 자동으로 재조정하는 적응형 쿼리 실행입니다. 예를 들어, 조인 시 한쪽 데이터가 크게 쏠려 있다면(Skew Join) 자동으로 조인 키를 분할하여 처리하는 "스큐 조인 자동 해결" 기능은, 과거 엔지니어가 수동으로 코딩해야 했던 복잡한 최적화 로직을 완전히 자동화하여, 이제는 엔지니어의 주요 업무가 파라미터 튜닝이 아닌 비즈니스 로직 설계로 집중되게 하는 패러다임 시프트를 이끌고 있습니다.

## 🧠 지식 맵 (Knowledge Graph)

*   **Apache Spark 생태계 전체 트리 (Ecosystem Taxonomy)**
    *   **Spark Core** -> RDD API, Task 스케줄링, 메모리 관리, I/O 핸들링
    *   **Spark SQL** -> DataFrame/Dataset API, Catalyst Optimizer, Spark Thrift Server (ODBC/JDBC)
    *   **Structured Streaming** -> 연속 처리, 마이크로배치, 상태 관리, Watermark
    *   **MLlib** -> 분산 머신러닝 (분류/회귀/군집/협업 필터링/피처 추출)
    *   **GraphX** -> 분산 그래프 처리 (PageRank, Connected Components)
*   **Spark 실행 환경 비교**
    *   Local (개발용) < Standalone (단일 클러스터) < YARN (엔터프라이즈 Hadoop) < Kubernetes (Cloud-native)
*   **핵심 튜닝 파라미터**
    *   `spark.sql.shuffle.partitions` (기본 200, 데이터 크기에 따라 조절)
    *   `spark.sql.adaptive.enabled` (AQE 활성화, Spark 3.0+)
    *   `spark.memory.fraction` (Execution vs Storage 메모리 비율)

---

## 6. 기대효과 및 결론

Apache Spark — 인메모리 분산 처리 엔진 (Unified Analytics Engine)은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[Hadoop MapReduce]
    │
    ▼
[RDD]
    │
    ▼
[Spark SQL]
    │
    ▼
[Structured Streaming]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| RDD·DataFrame | 스파크의 기본 추상화 |
| Catalyst·AQE | 실행 계획 최적화 핵심 |
| Shuffle·Partition | 성능 병목과 튜닝 포인트 |
| Lakehouse | 스파크 기반 현대 분석 플랫폼 |
