+++
weight = 97
title = "22. 스트리밍 SQL (Streaming SQL) — ksqlDB/Flink SQL/Spark Structured Streaming"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 스트리밍 SQL (Streaming SQL) — ksqlDB/Flink SQL/Spark Structured Streaming은(는) 끊임없이 들어오는 이벤트를 낮은 지연으로 처리하면서 상태·시간·정확성을 제어하는 실시간 처리 핵심 기술이다.
> **비유**: 흐르는 고속도로의 차량을 멈추지 않고 실시간으로 분류하고 통제하는 관제센터와 같다.

📝 모범 답안

## 1. 개요 및 필요성

| 효과 | 설명 |
|:---|:---|
| 개발 생산성 | SQL로 스트리밍 파이프라인 10배 빠른 개발 |
| 진입 장벽 감소 | Java/Scala API 없이 SQL로 스트리밍 구현 |
| 자동 최적화 | SQL 옵티마이저가 실행 계획 자동 생성 |
| 표준화 | 다른 팀과 쿼리 공유·재사용 용이 |

---

## 2. 구성요소

스트리밍 SQL은 **데이터 엔지니어링의 민주화**를 가능하게 하는 핵심 기술이다. 기술사 답안에서는 ksqlDB/Flink SQL/Spark Streaming SQL의 특성 비교, 스트리밍 고유 SQL 구문(TUMBLE, HOP, WATERMARK, EMIT CHANGES), 그리고 스트림-테이블 조인의 실무적 활용을 서술하면 된다.

> 스트리밍 SQL은 "강이 되어버린 데이터에 SQL 낚시 면허증"을 부여한 것이다. 이제 엔지니어뿐 아니라 SQL을 아는 분석가도 흐르는 강에서 직접 물고기(인사이트)를 잡을 수 있게 되었다.

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

스트리밍 SQL (Streaming SQL) — ksqlDB/Flink SQL/Spark Structured Streaming은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 실시간 처리의 경쟁력은 더 빨리 흘리는 것보다 시간 의미와 상태 일관성을 잃지 않는 데 있다.

---

## 7. 발전 흐름도

```text
[정적 배치 SQL — 저장된 테이블 대상 질의]
    │
    ▼
[스트리밍 SQL — 흐르는 스트림에 SQL 적용]
    │
    ▼
[Window 연산 (TUMBLE·HOP·SESSION) — 시간 구간 집계]
    │
    ▼
[Watermark — 이벤트 지연 허용 및 집계 완료 트리거]
    │
    ▼
[ksqlDB (Kafka) / Flink SQL — 프로덕션 스트리밍 SQL 표준]
```
정적 SQL 문법을 흐르는 스트림에 적용하고, 창(Window)과 워터마크(Watermark)로 시간 지연을 처리하며, ksqlDB와 Flink SQL이 각각 Kafka·범용 스트리밍 표준으로 자리잡는 흐름이다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Window Operations | 핵심 구현 | 스트리밍 SQL의 TUMBLE/HOP/SESSION |
| Watermark | Flink SQL 연동 | 이벤트 시간 기반 집계의 지연 처리 |
| Kafka (ksqlDB) | 소스 시스템 | ksqlDB의 데이터 소스 및 싱크 |
| Exactly-Once | 신뢰성 | Flink SQL 체크포인팅으로 달성 |
| CEP | 확장 기능 | Flink의 복합 이벤트 패턴 감지 |
