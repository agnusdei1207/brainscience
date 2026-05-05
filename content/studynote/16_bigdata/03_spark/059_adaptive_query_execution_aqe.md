+++
weight = 59
title = "적응형 쿼리 실행 (Adaptive Query Execution, AQE)"
date = "2024-03-23"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 적응형 쿼리 실행 (Adaptive Query Execution, AQE)은(는) 인메모리 분산 실행과 쿼리 최적화를 통해 대화형 분석·배치·스트리밍을 빠르게 연결하는 스파크 핵심 개념이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

- **정의**: 실행 단계 사이의 중간 결과물(Shuffle Map Output)의 통계를 실시간으로 분석하여, 남은 쿼리 단계를 최적화하는 기법이다.
- **배경**: 기존 Catalyst는 실행 전의 정적 통계에만 의존했다. 하지만 복잡한 필터링이나 조인을 거치면 데이터 크기가 급변하여, 처음에 세운 계획이 런타임에는 비효율적이 되는 경우가 많았다.

---

## 2. 구성요소

```text
[ AQE Runtime Optimization Cycle ]

  (Query Stage 1) --                            |
                            V
               [ Collect Runtime Statistics ]
                            |
                            V
  (Query Stage 2) <-- [ Re-optimize Plan ]
      - Merge small partitions
      - Handle skewed data
      - Switch to Broadcast Join
```

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:
| AQE 핵심 기능 | 상세 내용 | 해결하는 문제 |
| :--- | :--- | :--- |
| **Coalescing Shuffle Partitions** | 너무 작은 여러 파티션을 하나의 적절한 크기로 합침 | 작은 파티션이 너무 많아 발생하는 오버헤드 감소 |
| **Switching Join Strategies** | 조인 대상 테이블이 작아진 것을 감지하면 Broadcast Join으로 변경 | 불필요한 네트워크 셔플 방지 |
| **Optimizing Skew Join** | 특정 파티션에 데이터가 쏠린 경우(Skew) 이를 쪼개서 분산 처리 | 일부 Task만 오래 걸리는 '꼬리 지연' 현상 해결 |

---

## 4. 비교 및 연결

- **설정 활성화**: Spark 3.2 버전부터 기본 활성화되어 있으나, `spark.sql.adaptive.enabled=true` 설정을 명시적으로 확인해야 한다.
- **스큐 조인 처리**: 데이터 쏠림 현상이 심한 대규모 테이블 조인 시, 힌트(Hint)를 주지 않아도 AQE가 `spark.sql.adaptive.skewJoin.enabled`를 통해 자동으로 성능을 방어해주므로 운영 안정성이 크게 향상된다.

---

## 5. 실무 적용 및 판단

- AQE는 "데이터가 어떻게 변할지 모르니 실행하면서 배우자"는 철학을 Spark에 구현했다. 이는 클라우드 네이티브 분산 처리 환경에서 자원 예측의 불확실성을 상쇄하는 가장 강력한 무기이며, 향후 머신러닝 기반의 자동 튜닝 엔진으로 나아가는 핵심 징검다리다.

---

## 6. 기대효과 및 결론

적응형 쿼리 실행 (Adaptive Query Execution, AQE)은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[정적 쿼리 계획 (Static Query Plan) — CBO]
    │
    ▼
[런타임 통계 수집 (Runtime Statistics)]
    │
    ▼
[적응형 쿼리 실행 (AQE, Adaptive Query Execution)]
    │
    ▼
[파티션 병합 / 스큐 조인 최적화 (Skew Join)]
    │
    ▼
[ML 기반 자동 튜닝 엔진 (Auto-tuning)]
```

Spark 쿼리 최적화가 컴파일 시점 정적 계획에서 런타임 통계 기반 동적 최적화로 발전한 흐름이다.

---

## 8. 관련 개념 맵

- **부모 개념**: Apache Spark 3.0
- **자식 개념**: Partition Coalescing, Skew Join Optimization
- **연관 개념**: Catalyst Optimizer, CBO, Shuffle
