+++
weight = 81
title = "06. Flink 아키텍처 (Flink Architecture) — JobManager/TaskManager/JobGraph"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Flink 아키텍처 (Flink Architecture) — JobManager/TaskManager/JobGraph은(는) 끊임없이 들어오는 이벤트를 낮은 지연으로 처리하면서 상태·시간·정확성을 제어하는 실시간 처리 핵심 기술이다.
> **비유**: 흐르는 고속도로의 차량을 멈추지 않고 실시간으로 분류하고 통제하는 관제센터와 같다.

📝 모범 답안

## 1. 개요 및 필요성

| 효과 | 설명 |
|:---|:---|
| 저지연 처리 | 이벤트 단위 처리로 밀리초~수 초 지연 달성 |
| Exactly-Once 보장 | 체크포인팅 기반 정확히 한 번 처리 |
| 대규모 상태 관리 | RocksDB로 TB 규모 상태도 안정적 처리 |
| 배치+스트리밍 통합 | 동일 API로 유한/무한 데이터 처리 |

---

## 2. 구성요소

Flink 아키텍처의 핵심은 **JobManager의 중앙 조율 + TaskManager의 분산 실행 + 체크포인팅 기반 상태 내구성**이다. 기술사 답안에서는 JobManager/TaskManager/TaskSlot의 역할을 명확히 구분하고, 연산자 체이닝과 JobGraph→ExecutionGraph 변환 과정, 그리고 HA 설계 고려사항을 함께 서술하면 완성도 높은 답안이 된다.

> Flink 클러스터는 "세계적인 교향악단"과 같다. 지휘자(JobManager)가 악보(JobGraph)를 보며 각 파트(TaskManager)에 지시하고, 각 단원(TaskSlot)이 자기 파트를 정확히 연주한다. 지휘자가 쓰러져도(HA) 부지휘자(Standby JobManager)가 즉시 지휘봉을 잡는다.

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

Flink 아키텍처 (Flink Architecture) — JobManager/TaskManager/JobGraph은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 실시간 처리의 경쟁력은 더 빨리 흘리는 것보다 시간 의미와 상태 일관성을 잃지 않는 데 있다.

---

## 7. 발전 흐름도

```text
[배치 처리 (Batch Processing)]
    │
    ▼
[스트림 처리 (Stream Processing)]
    │
    ▼
[Apache Flink (Apache Flink)]
    │
    ▼
[이벤트 시간 (Event Time)]
```

이 흐름도는 배치 처리와 스트림 처리가 Apache Flink와 이벤트 시간 모델로 통합되는 흐름을 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Checkpoint (Flink) | 핵심 메커니즘 | 체크포인트 코디네이터가 JobManager에 내장 |
| DataStream API | 프로그래밍 인터페이스 | JobGraph 생성의 원천 |
| State Backend | 상태 저장 | TaskManager의 로컬 상태 저장 방식 |
| ZooKeeper | HA 의존성 | JobManager 리더 선출 |
| Operator Chaining | 최적화 기법 | JobGraph 내 연산자 통합으로 네트워크 비용 절감 |
