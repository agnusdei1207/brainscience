+++
weight = 23
title = "23. 지연 평가 (Lazy Evaluation)"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: 지연 평가(Lazy Evaluation)는 식(Expression)의 결과가 실제로 필요한 시점까지 계산을 미루는 평가 전략으로, 불필요한 연산을 원천 차단하고 무한 시퀀스(Infinite Sequence) 같은 자료구조를 유한 메모리에서 처리할 수 있게 한다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

지연 평가(Lazy Evaluation)는 함수형 프로그래밍(Functional Programming)에서 시작된 개념으로, 연산 결과가 명시적으로 요구될 때까지 계산을 지연시키는 프로그램 실행 전략이다.

즉시 평가(Eager Evaluation)에서는 `map(f, huge_list)`처럼 거대한 리스트 전체를 변환해 메모리에 올리지만, 결국 처음 10개 결과만 사용한다면 나머지 수백만 건의 연산은 낭비다. 지연 평가는 이 문제를 연산을 "레시피(실행 계획)"로만 기억하고, 결과가 필요할 때 그 레시피를 실행하는 방식으로 해결한다.

```text
┌────────────────────────────────────────────────────────────┐
│           즉시 평가 vs 지연 평가 비교                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  [즉시 평가 (Eager)]                                        │
│  data = [1..1000000]                                       │
│  result = filter(>100, map(*2, data))  ← 즉시 전체 실행     │
│  first_10 = take(10, result)                               │
│  → 100만 번 연산 후 10개만 사용 (낭비!)                      │
│                                                            │
│  [지연 평가 (Lazy)]                                         │
│  data = [1..∞]  ← 무한 리스트 (메모리에 없음!)               │
│  result = filter(>100, map(*2, data))  ← 실행 계획만 기록   │
│  first_10 = take(10, result)  ← 여기서 실제 10번만 실행     │
│  → 딱 10개 계산 (최적!)                                     │
└────────────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

Apache Spark는 지연 평가를 RDD (Resilient Distributed Dataset, 분산 탄력 데이터셋) 연산의 핵심 원리로 채택한다.

| 구분 | 연산 예시 | 실행 시점 | 설명 |
|:---|:---|:---|:---|
| **Transformation (변환)** | map, filter, groupBy, join | 지연 — Action까지 실행 안 함 | DAG에 단계만 기록 |
| **Action (행동)** | collect, count, save, show | 즉시 실행 | DAG를 실제로 실행 트리거 |

```text
┌──────────────────────────────────────────────────────────┐
│           Spark 지연 평가 DAG 최적화 흐름                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  RDD.filter(condition)  ← Transformation 1 (기록만)       │
│     .map(transform)     ← Transformation 2 (기록만)       │
│     .join(other_rdd)    ← Transformation 3 (기록만)       │
│     .count()            ← Action! 여기서 DAG 실행         │
│                                                          │
│  Catalyst Optimizer 개입:                                 │
│  filter → map → join  →  filter를 join 앞으로 이동!        │
│  (Predicate Pushdown: 데이터 줄인 후 join → 비용 80% 절감)  │
└──────────────────────────────────────────────────────────┘
```

`collect()`는 드라이버 메모리로 전체 RDD를 가져오므로 대용량 데이터에 절대 사용 금지.
- `persist()`/`cache()`로 자주 재사용하는 RDD를 메모리에 체크포인트.
- `explain()`으로 Spark SQL 실행 계획(Physical/Logical Plan) 확인 후 최적화 여부 점검.

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가 (Lazy Evaluation)은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 평가 전략 | 언어/시스템 | 메모리 | 최적화 가능 | 무한 시퀀스 |
|:---|:---|:---|:---|:---|
| **즉시 평가 (Eager)** | Python list, Java, C | 즉시 소비 | 어려움 | 불가 |
| **지연 평가 (Lazy)** | Haskell, Spark RDD, Python Generator | 필요 시 소비 | 가능 (Optimizer) | 가능 |
| **부분 지연 (Short-Circuit)** | Python and/or, Java &&·｜｜ | 조건부 소비 | 조건부 | 불가 |

지연 평가는 Haskell에서 기본 평가 전략이며, Scala·Kotlin에서는 `lazy val`, `Sequence`로 선택적 지연 평가를 지원한다. 데이터 엔지니어링에서는 Spark SQL의 Catalyst Optimizer가 지연 평가 기반 실행 계획을 물리 실행 계획(Physical Plan)으로 최적화하는 과정이 핵심이다.

동작 순서:
1. **입력 정의**: 해당 주제가 다루는 데이터·요청·상태를 명확히 식별한다. 입력 경계가 불분명하면 품질 검증과 책임 분리가 무너진다.
2. **처리 규칙 적용**: 저장 구조, 연산 로직, 분산 처리, 학습 규칙 중 핵심 메커니즘을 실행한다. 이 단계가 성능·확장성·정확도를 결정한다.
3. **결과 검증**: 정합성, 지연, 비용, 품질 지표를 확인해 운영 가능한 상태인지 판단한다. 이 검증이 없으면 실험은 가능해도 서비스화는 어렵다.
4. **운영 피드백 반영**: 드리프트, 부하 변화, 장애, 스키마 변화에 대응해 구조를 다시 조정한다. 실무에서는 이 폐쇄 루프가 기술의 지속성을 만든다.

```text
[입력/이벤트]
      ↓
[저장·정제·변환]
      ↓
[핵심 연산/학습/질의]
      ↓
[검증·배포·활용]
      ↓
[모니터링·재조정]
```

---

## 4. 비교 및 연결

```python
# 즉시 평가: 100만 개 리스트 메모리에 올림
big_list = [x*2 for x in range(1_000_000)]

# 지연 평가: 필요할 때 하나씩 생성
lazy_gen = (x*2 for x in range(1_000_000))
first_10 = [next(lazy_gen) for _ in range(10)]  # 10번만 실행
```

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| **I/O 최소화** | 불필요 데이터 처리 원천 차단 | I/O 60~80% 절감 |
| **메모리 효율** | 무한 시퀀스도 유한 메모리로 처리 | OOM 에러 방지 |
| **최적화 기회** | Optimizer의 실행 계획 재배치 허용 | 잡 시간 50~75% 단축 |

지연 평가는 Spark SQL의 Adaptive Query Execution (AQE, 적응형 쿼리 실행)과 결합하여 실행 중 실시간으로 파티션 크기와 조인 전략을 동적으로 최적화하는 방향으로 진화하고 있다. 데이터 엔지니어는 지연 평가의 원리를 이해해야 Spark 잡 성능 튜닝과 비용 최적화를 실질적으로 수행할 수 있다.

10억 건 로그 데이터에서 오류 코드 500인 건만 집계하는 Spark 잡이 느리다.

1. **문제**: `join` 후 `filter`를 수행하는 잘못된 연산 순서 (Transformation 기록 순서 오류).
2. **분석**: Spark UI에서 DAG를 확인 → Join Stage 전 데이터가 10억 건.
3. **해결**: `filter(error_code == 500)`을 `join` 앞으로 이동 (Predicate Pushdown 활용).
4. **결과**: Join 대상 데이터 90% 감소 → 잡 실행 시간 75% 단축.

Spark DataFrame 연산을 Action 없이 무한정 체이닝하는 코드. Transformation이 수백 단계 쌓이면 DAG가 지나치게 커져 Catalyst Optimizer의 최적화 비용 자체가 폭증한다. 중간에 `checkpoint()`로 Lineage를 잘라주는 것이 필요하다.

---

## 6. 기대효과 및 결론

지연 평가는 Spark SQL의 Adaptive Query Execution (AQE, 적응형 쿼리 실행)과 결합하여 실행 중 실시간으로 파티션 크기와 조인 전략을 동적으로 최적화하는 방향으로 진화하고 있다.

지연 평가 (Lazy Evaluation)의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
[함수형 프로그래밍 (Haskell) — 기본 평가 전략으로 지연 평가]
    │
    ▼
[Python Generator / Scala Lazy Val — 선택적 지연 평가]
    │
    ▼
[Spark RDD Transformation — 분산 지연 평가 + DAG]
    │
    ▼
[Catalyst Optimizer — 지연 평가 기반 실행 계획 최적화]
    │
    ▼
[AQE (Adaptive Query Execution) — 런타임 동적 최적화]
```
함수형 언어의 지연 평가 개념이 Python Generator, Spark RDD로 이어지며, Catalyst Optimizer와 AQE를 통해 런타임 적응형 최적화로 진화하는 흐름이다.

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Spark RDD/DataFrame** | 지연 평가 기반 분산 데이터셋; Transformation-Action 구조 |
| **DAG (Directed Acyclic Graph)** | Spark의 실행 계획 그래프; 지연 평가로 빌드된 후 Action으로 실행 |
| **Catalyst Optimizer** | Spark SQL의 지연 평가 기반 논리·물리 실행 계획 최적화기 |
| **Python Generator** | 파이썬에서 지연 평가를 구현하는 `yield` 기반 이터레이터 |
| **Predicate Pushdown** | 필터 조건을 데이터 소스 근처로 이동시켜 처리 데이터 최소화 |
