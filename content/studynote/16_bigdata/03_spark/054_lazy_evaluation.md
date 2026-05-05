+++
weight = 54
title = "03. 지연 평가 (Lazy Evaluation) — 연산 최적화 전략"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 지연 평가 (Lazy Evaluation) — 연산 최적화 전략은(는) 인메모리 분산 실행과 쿼리 최적화를 통해 대화형 분석·배치·스트리밍을 빠르게 연결하는 스파크 핵심 개념이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

Lazy Evaluation은 Spark의 DAG 스케줄러와 결합될 때 비로소 진정한 힘을 발휘합니다.

- **DAG 스케줄러 역할**: Action 호출 시, DAG 스케줄러는 전체 변환 체인을 거꾸로遡って(Backwards) 분석하여, 각 파티션에 대해"이 파티션을 계산하려면 어떤父파티션이 먼저 계산되어야 하는지"를 결정합니다. 이 때 Wide Dependency(Shuffle)가 발견되면 그 지점에서 Stage를 분리합니다.
- **파이프라이닝 최적화**: Narrow Dependency로 연결된 변환들은 같은 Stage 내에서 파이프라이닝됩니다. 즉, 한 파티션에서 filter를 적용한 결과가 곧바로 map으로 들어가고, 그 결과가 또 바로 reduce로 전달되어, 중간 결과를 메모리에 저장하지 않고 스트림처럼 바로 다음 연산으로 흘려보냅니다.
- **필터 프루닝 (Filter Pruning)**: DAG를 분석하면, 어떤 필터 조건이 항상 false를 반환하는 것을 알 수 있는 경우(예: null 체크 followed by null이 아닌 필터), 아예 해당 필터 이하의 변환 체인을 실행하지 않을 수 있습니다.

---

## 2. 구성요소

**Python eager (list comprehension 즉시 평가):**
```python

result_list = [x * 2 for x in range(1000000000)]  # 10억 개 즉시 생성!
print(result_list[:5])  # 이 줄에서 비로소 출력
```

**Python lazy (generator: lazy evaluation):**
```python

result_gen = (x * 2 for x in range(1000000000))  # 계획만 기록
print(next(result_gen))  # 이 줄에서 비로소 첫 번째 값만 연산
```

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:
| 비교 항목 | Eager Evaluation | Lazy Evaluation |
|:---|:---|:---|
| **실행 시점** | 표현식 작성 시 즉시 실행 | Action 호출 시까지 미루기 |
| **메모리 사용** | 중간 결과 전체를 메모리에 저장 | 파이프라이닝으로 중간 결과 최소화 |
| **오류 발견** | Runtime(실행 시)에만 발견 | 컴파일 타임에 발견 가능한 경우多 |
| **디버깅 용이성** | 단계별로 결과 확인 가능 | 전체 플랜이 블랙박스化, 디버깅 어려움 |
| **순수 함수 보장** | 부수 효과(side effect) 있어도 실행됨 | 부수 효과가 실제로 실행되는 시점에만 발현 |

- **Lazy Evaluation의 숨은 위험: 메모리 누수의 역설**: Lazy Evaluation은"실행되지 않는 연산은 메모리를 사용하지 않는다"는 장점이 있지만, 반대로"실행되지 않은 연산의 계획(DAG)이 계속 누적된다"면 이는 이것이 메모리 누수의 원인이 될 수 있습니다. 예를 들어, 어떤 Spark 잡이 수백 개의 Transformation을 차례로 적용하는非常大的 DAG를 만들었지만, 단 한 번의 Action만 호출한다면, DAG 자체는 메모리에 유지되므로 수백 메가바이트의 실행 계획 메타데이터가 메모리를 점유하게 됩니다. 이는 Lambda 아키텍처에서 Batch Layer의非常大的 DAG를 만들 때 특히 주의해야 할 문제입니다.

---

## 4. 비교 및 연결

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **파ipelining 가능 여부** | Narrow Dependency 연속 시 → 파이프라인으로 최적화 | Wide Dependency 섞여 있으면 Stage 분리不可避免 |
| **DAG 복잡도** | 100개 이상 Transformation → 메타데이터 Overhead 증가 | 너무 긴 lineage → checkpoint 권장 |
| **Action 빈도** | 1개 RDD에 여러 Action → cache 필요 | 1개 Action만 → 불필요 캐시 제거 |
| **데이터 체인 분석** | filter→map→reduce 순서: filter를 map 이전에 적용하여 네트워크 전송량 최소화 | map→filter→reduce: 필터가 나중에 오면 불필요 데이터도 네트워크 통과 |

*(추가 실무 적용 가이드 - Lazy Evalutation 디버깅 전략)*
- **take(n) action 활용**: 전체 collect() 대신 take(n)을 사용하여 결과의 部分만 즉시 확인. take는 첫 n 개 파티션만 읽기 때문에 전체 데이터를 처리하지 않아 디버깅 속도가 매우 빠릅니다.
- **RDD.toDebugString**: RDD의 lineage 체인(실행 계획)을 문자열로 출력하여, 어떤 변환들이 어떤 순서로 연결되어 있는지 확인하는 중요한 디버깅 도구입니다.
- **queryExecution**: Spark DataFrame의 쿼리 실행 계획을 확인하는 official API로, .queryExecution.executedPlan으로 물리 계획, .queryExecution.analyzed으로 논리計画を解析할 수 있습니다.
- **실무 의사결정**: Lazy Evaluation의 "미리보기(Preview)" 기능을 활용하려면, 전체 데이터가 아닌"샘플 데이터"로 먼저 파이프라인을 테스트한 후 전체 데이터로 실행하는"2단계 개발 패턴"을 따르는 것이 업계 Best Practice입니다.

---

## 5. 실무 적용 및 판단

1. **Adaptive Query Execution (AQE)과 Lazy Evaluation의 결합**
   Spark 3.0에서 도입된 AQE는 런타임 통계를 기반으로Lazy Evaluation이 세운 실행 계획을"재조정"하는 능동적 최적화입니다. 예를 들어, 조인 시 한쪽 데이터의 크기가 예상과 달리 매우 작은 것으로 밝혀지면, Broadcast Join(작은 쪽 전체를 네트워크로全量送信하여 모든 Executor에 복제)으로 자동으로 전환합니다. 이는 기존"계획 시점(Compile Time)"의Lazy Evaluation을"실행 시점(Runtime)"까지 확장한 것으로, 동적 최적화의 새로운 지평을 열었습니다.

2. **Declarative DSL (Domain-Specific Language)의 대중화**
   Lazy Evaluation의"무엇을 계산할지(What), 아닌 어떻게 계산할지(How)"라는 선언적(Declarative) 특성은, 이제 Spark SQL, Apache Beam, Flink SQL처럼"SQL-like 언어"로 데이터를 처리하는 DSL의 대중화로 이어지고 있습니다. 사용자는"어떻게 필터를 적용하고 조인을 구현할지"가 아니라"어떤 테이블을 조인할지"만 선언하면, 프레임워크가 Lazy Evaluation + DAG 최적화를 통해 자동으로 최적의 실행 계획을 세웁니다.

3. **지연Evalusation와 메타프로그래밍의 결합**
   Scala의 macrosやRust의 procedural macros처럼, Lazy Evaluation 개념이"컴파일 타임 최적화"로 확장되고 있습니다. Apache Spark의 Catalyst Optimizer는 Scala의 木変換(Tree Transformation) 기능을 활용하여, DataFrame 연산의 논리 계획을 컴파일 시점에 최적화된 물리 계획로 변환합니다. 이는 Lazy Evaluation의"실행 전 최적화" 특성을 더 강력한"컴파일 타임 리팩토링"으로 발전시킨 것으로, 컴파일러가 불필요한 변환을 제거하고 상수 폴딩(Constant Folding)을 적용하여 런타임 비용을 최소화합니다.

## 🧠 지식 맵 (Knowledge Graph)

*   **Lazy Evaluation 적용 기술 생태계**
    *   **함수형 프로그래밍**: Haskell(순수 지연 평가), Scala(LAZY 키워드), Clojure(지연 시퀀스)
    *   **빅데이터 처리**: Apache Spark(RDD/DataFrame), Apache Flink(ストリ밍), Apache Beam(统一的 API)
    *   ** языки программирования**: Python(Generator/Iterator), Java(Stream API), JavaScript(제너레이터)
*   **Spark Lazy Evaluation 핵심 트리거**
    *   **Transformation** (Lazy): map, filter, flatMap, groupByKey, join, reduceByKey, union, distinct, repartition...
    *   **Action** (실행 개시): collect, count, sum, take, save, foreach, reduce...
*   **DAG 최적화 기법**
    *   Constant Folding (컴파일 타임 상수 연산)
    *   Predicate Pushdown (필터 조건을 下游으로 내림)
    *   Column Pruning (필요한 컬럼만 선택)
    *   Narrow→Wide 파이프라이닝

---

## 6. 기대효과 및 결론

지연 평가 (Lazy Evaluation) — 연산 최적화 전략은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[Lazy Evaluation 적용 기술 생태계]
    │
    ▼
[함수형 프로그래밍: Haskell(순수 지연 평가), Scala(LAZY 키워드), Clojure(지연 시퀀스)]
    │
    ▼
[빅데이터 처리: Apache Spark(RDD/DataFrame), Apache Flink(ストリ밍), Apache Beam(统一的 API)]
    │
    ▼
[языки программирования: Python(Generator/Iterator), Java(Stream API), JavaScript(제너레이터)]
    │
    ▼
[Spark Lazy Evaluation 핵심 트리거]
    │
    ▼
[Transformation (Lazy): map, filter, flatMap, groupByKey, join, reduceByKey, union, distinct, repartition...]
```

이 흐름도는 Lazy Evaluation 적용 기술 생태계에서 출발해 Spark Lazy Evaluation 핵심 트리거까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| RDD·DataFrame | 스파크의 기본 추상화 |
| Catalyst·AQE | 실행 계획 최적화 핵심 |
| Shuffle·Partition | 성능 병목과 튜닝 포인트 |
| Lakehouse | 스파크 기반 현대 분석 플랫폼 |
