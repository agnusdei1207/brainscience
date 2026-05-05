+++
weight = 57
title = "Catalyst Optimizer"
date = "2024-03-23"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Catalyst Optimizer은(는) 인메모리 분산 실행과 쿼리 최적화를 통해 대화형 분석·배치·스트리밍을 빠르게 연결하는 스파크 핵심 개념이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

- **정의**: Spark SQL과 DataFrame/Dataset API의 하단에서 작동하는 확장 가능한 쿼리 옵티마이저 프레임워크다.
- **배경**: 개발자가 작성한 SQL이나 DataFrame 코드는 항상 최적의 성능을 보장하지 않는다. Catalyst는 이를 분석하여 데이터 필터링 시점 최적화(Predicate Pushdown), 필요한 열만 선택(Projection Pruning) 등을 자동으로 수행한다.

---

## 2. 구성요소

```text
[ Catalyst Optimization Pipeline ]

 (Unresolved)     (Resolved)      (Optimized)      (Physical)
 Logical Plan --      |               |               |               |              |
  [Analyzer]      [Catalyst]      [Optimizer]    [Cost Model]    [Tungsten]
      |               |               |               |              |
  Catalog info    Standard Rules   CBO/RBO        Selection       Java Bytecode
```

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:
| 단계 | 주요 역할 | 최적화 예시 |
| :--- | :--- | :--- |
| **Analysis** | 메타데이터(Catalog)를 참조해 테이블/컬럼 존재 확인 | 잘못된 컬럼명 체크 및 바인딩 |
| **Logical Optimization** | 논리적인 관계 대수 최적화 (RBO) | Predicate Pushdown (필터링 우선 수행) |
| **Physical Planning** | 실제 실행 가능한 여러 계획 생성 및 CBO 적용 | Broadcast Join vs Shuffle Join 선택 |
| **Code Generation** | 런타임에 최적화된 Java 바이트코드 생성 | 전체 쿼리를 하나의 함수처럼 실행 (Whole-stage CodeGen) |

---

## 4. 비교 및 연결

- **CBO(Cost-Based Optimizer) 활성화**: 데이터 통계 정보가 최신일 때 최적의 성능을 낸다. `ANALYZE TABLE` 명령을 통해 통계를 생성하면 Catalyst가 조인 순서를 더 지능적으로 결정한다.
- **디버깅 전략**: `explain(true)` 명령을 사용하면 분석 전(Parsed), 분석 후(Analyzed), 최적화 후(Optimized), 물리적(Physical) 계획을 모두 확인하여 병목 지점을 파악할 수 있다.

---

## 5. 실무 적용 및 판단

- Catalyst 덕분에 Spark는 언어(Python, Scala, SQL)에 상관없이 동일한 고성능을 보장할 수 있게 되었다. 최근에는 기계 학습 모델을 쿼리 최적화에 도입하거나, 런타임 상황에 따라 계획을 수정하는 AQE(Adaptive Query Execution)와 결합되어 더욱 진화하고 있다.

---

## 6. 기대효과 및 결론

Catalyst Optimizer은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[논리 계획 (Logical Plan)]
    │
    ▼
[물리 계획 (Physical Plan)]
    │
    ▼
[Catalyst Optimizer (Catalyst Optimizer)]
    │
    ▼
[코드 생성 (Code Generation)]
```

이 흐름도는 논리 계획이 물리 계획을 거쳐 Catalyst Optimizer와 코드 생성으로 구체화되는 흐름을 보여준다.

---

## 8. 관련 개념 맵

- **부모 개념**: Apache Spark, Spark SQL
- **자식 개념**: RBO(Rule-Based), CBO(Cost-Based), Code Generation
- **연관 개념**: Tungsten Engine, AQE, DataFrame API
