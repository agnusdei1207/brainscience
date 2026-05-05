+++
weight = 82
title = "07. DataStream API / Table API & SQL — Flink 두 계층 처리"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: DataStream API / Table API & SQL — Flink 두 계층 처리은(는) 끊임없이 들어오는 이벤트를 낮은 지연으로 처리하면서 상태·시간·정확성을 제어하는 실시간 처리 핵심 기술이다.
> **비유**: 흐르는 고속도로의 차량을 멈추지 않고 실시간으로 분류하고 통제하는 관제센터와 같다.

📝 모범 답안

## 1. 개요 및 필요성

| 효과 | 설명 |
|:---|:---|
| 개발 생산성 | SQL 알면 스트리밍 앱 빠르게 개발 가능 |
| 최적화 자동화 | Table API/SQL은 Flink 옵티마이저가 자동 최적화 |
| 유연성 | 두 API 혼용으로 선언적+절차적 처리 결합 |
| 생태계 통합 | JDBC, Kafka, ES 등 다양한 커넥터 |

---

## 2. 구성요소

Flink의 DataStream API와 Table API/SQL은 **상호 보완적인 두 층의 프로그래밍 모델**이다. 기술사 답안에서는 두 API의 추상화 수준 차이, 내부적으로 동일한 실행 엔진으로 컴파일된다는 통합성, 그리고 스트리밍 SQL의 고유 구문(TUMBLE, HOP, SESSION 윈도우)을 서술하는 것이 핵심이다.

> Flink의 두 API는 "같은 공장의 두 입구"다. 자동화 생산 라인(Table API/SQL)으로 들어가면 로봇이 알아서 처리하고, 수작업 라인(DataStream API)으로 들어가면 세밀하게 직접 제어한다. 두 라인의 결과물은 같은 공장 창고에 모인다.

---

## 3. 구조 및 원리

**핵심 조건**: 이벤트 시간, 상태 저장, 지연 허용, 전달 보장이 함께 통제되어야 한다.

동작 순서:

---

## 4. 비교 및 연결

---

## 5. 실무 적용 및 판단

---

## 6. 기대효과 및 결론

DataStream API / Table API & SQL — Flink 두 계층 처리은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 실시간 처리의 경쟁력은 더 빨리 흘리는 것보다 시간 의미와 상태 일관성을 잃지 않는 데 있다.

---

## 7. 발전 흐름도

```text
[Flink RDD]
    │
    ▼
[DataStream API]
    │
    ▼
[Table API/SQL]
    │
    ▼
[통합 스트리밍]
    │
    ▼
[Kappa 아키텍처]
```

Flink의 스트리밍 API가 저수준 RDD에서 고수준 SQL까지 통합되며 카파 아키텍처로 수렴하는 흐름이다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Flink 아키텍처 | 실행 환경 | DataStream/Table API의 실행 기반 |
| 윈도우 연산 | 핵심 활용 | TUMBLE/HOP/SESSION 윈도우 |
| Watermark | 연동 개념 | Table API의 WATERMARK 정의와 연동 |
| Kafka 커넥터 | Source/Sink | 가장 많이 사용되는 스트리밍 소스 |
| CEP (Complex Event Processing) | 확장 기능 | DataStream API 위의 패턴 감지 라이브러리 |
