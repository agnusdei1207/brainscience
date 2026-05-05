+++
weight = 56
title = "05. Spark SQL — 분산 구조적 쿼리 처리"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Spark SQL — 분산 구조적 쿼리 처리은(는) 인메모리 분산 실행과 쿼리 최적화를 통해 대화형 분석·배치·스트리밍을 빠르게 연결하는 스파크 핵심 개념이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

| 효과 | 설명 |
|:---|:---|
| 생산성 향상 | SQL 한 줄로 PB 규모 데이터 쿼리 |
| 성능 개선 | MapReduce 대비 최대 100배 빠른 분산 SQL |
| 통합 인터페이스 | SQL, Python, Scala, Java, R 모두 동일 엔진 |
| 기존 자산 활용 | Hive 테이블, 메타스토어 그대로 재사용 |
| 레이크하우스 기반 | Delta Lake/Iceberg와 결합해 ACID SQL 처리 |

---

## 2. 구성요소

- 복잡한 비구조적 변환은 여전히 RDD/Python UDF가 유연하나 성능 저하 주의
- Pandas UDF(벡터화 UDF)로 Python 생태계와 고성능 연동 가능
- Spark Connect (3.4+): 클라이언트-서버 분리 아키텍처로 원격 SQL 실행 지원

> Spark SQL은 빅데이터 세계의 "만능 칼"이다. SQL이라는 친숙한 언어로 Hadoop의 방대한 창고를 제트기 속도로 뒤질 수 있게 해주며, 앞으로는 클라우드 어디서나 원격으로 이 칼을 사용할 수 있는 시대(Spark Connect)로 진화하고 있다.

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:

---

## 4. 비교 및 연결

---

## 5. 실무 적용 및 판단

---

## 6. 기대효과 및 결론

Spark SQL — 분산 구조적 쿼리 처리은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[Catalyst Optimizer]
    │
    ▼
[Tungsten Engine]
    │
    ▼
[AQE (Adaptive Query Execution)]
    │
    ▼
[Hive Metastore]
    │
    ▼
[Delta Lake]
```

이 흐름도는 Catalyst Optimizer에서 출발해 Delta Lake까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Catalyst Optimizer | 내부 구성 | SQL/DataFrame → 최적 실행 계획 변환 |
| Tungsten Engine | 내부 구성 | 물리 실행 최적화, 메모리/CPU 효율화 |
| AQE | 확장 기능 | 런타임 재최적화, Skew Join 자동 처리 |
| Hive Metastore | 통합 대상 | 테이블 메타데이터 공유 |
| Delta Lake | 응용 | Spark SQL 위의 ACID 트랜잭션 계층 |
| DataFrame API | 동등 인터페이스 | SQL과 동일 실행 계획 생성 |
