+++
weight = 76
title = "01. Apache Flink - 상태 기반 스트리밍処理의 完成形"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Apache Flink - 상태 기반 스트리밍処理의 完成形은(는) 끊임없이 들어오는 이벤트를 낮은 지연으로 처리하면서 상태·시간·정확성을 제어하는 실시간 처리 핵심 기술이다.
> **비유**: 흐르는 고속도로의 차량을 멈추지 않고 실시간으로 분류하고 통제하는 관제센터와 같다.

📝 모범 답안

## 1. 개요 및 필요성

Flink는 마스터-워커(Master-Worker) 아키텍처를 채택하고 있습니다.

- **JobManager**: Flink 클러스터의 조정자(Coordinator) 역할을 합니다. 사용자로부터 제출된 JobGraph를 TaskManager들의 슬롯에 배포하고, 각 태스크의 상태를 모니터링하며, 체크포인트 조정(Checkpoint Coordination)을 수행합니다. 장애 발생 시 실패한 태스크를 재시작하거나, 리소스를 재배치합니다.
- **TaskManager**: 실제 데이터 처리 연산(Transformation, Window, Sink 등)이 실행되는 곳입니다. 각 TaskManager는 하나 이상의 태스크 슬롯(Task Slot)을 보유하며, 각 슬롯은 하나의 태스크 실행을 담당합니다. 슬롯 수는 TaskManager의 CPU 코어 수에 의해 결정됩니다.
- **Slot과 Task 실행**: 슬롯은 클러스터의 자원 할당 단위입니다. 각 슬롯은 고립된 메모리(managed memory)를 할당받고, 하나의 태스크(또는 서브테스크)가 할당됩니다. 슬롯은 여러 파티션을 처리할 수 있어, 코어 수보다 더 많은 작은 태스크들을高效적으로 다중 처리할 수 있습니다.

---

## 2. 구성요소

| State Backend | 저장 위치 | 장점 | 단점 | 적합한 경우 |
|:---|:---|:---|:---|:---|
| **HashMapStateBackend** | TaskManager JVM Heap | 최상의 처리 성능 | JVM Heap 크기 한계 (메모리 제한) | 상태 크기 < 수 GB, 고성능 요구 |
| **EmbeddedRocksDBStateBackend** | RocksDB (디스크) | 큰 상태도 외부 메모리로 관리 (LMDB) | 디스크 I/O로 살짝 느림 | 상태 크기 > 수 GB, 상태 큰 워크로드 |

---

## 3. 구조 및 원리

**핵심 조건**: 이벤트 시간, 상태 저장, 지연 허용, 전달 보장이 함께 통제되어야 한다.

동작 순서:
| 비교 항목 | Apache Spark Streaming | Apache Flink |
|:---|:---|:---|
| **처리 모델** | Micro-Batch | Continuous Processing |
| **지연 시간** | ~1초+ | 수십 ms ~ 1초 |
| **상태 관리** | 외장 (checkpoint-interval 미지원) | 내장 상태 백엔드 (RocksDB) |
| **Event Time 지원** | Structured Streaming 이후 (Spark 2.3~) | 원래부터 지원 (설계 철학) |
| **복구 시간** | WAL + Lineage 재연산 | 증분 체크포인트 (빠른 복구) |
| **API 일관성** | 배치/스트리밍 unified (DataFrame) | 배치/스트리밍 unified (DataStream API) |
| ** 생태계 성숙도** | 매우 높음 (Spark 생태계 활용) | 높음 (연속 성장 중) |

- **Flink의 가장 큰 강점**: 상태가 있는(stateful) 스트리밍 연산이 필요한 경우(예: 페이지 방문 횟수를 세다가 사용자가 30분간 활동이 없으면 세션을 종료하고 카운트를 내보내는 세션 윈도우 연산) Flink의 내장 상태 관리 功能은 압도적으로 우수합니다. Spark Streaming에서는 상태 관리를 위해 별도의 외부 데이터베이스(Redis 등)를 사용해야 하는 경우가 많지만, Flink는 상태 백엔드를 내장하고 RocksDB를 통해 Huge한 상태도 디스크에서管理합니다.

---

## 4. 비교 및 연결

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **지연 요구 수준** | < 1초 SLA → Flink, 수 초 허용 → Spark Streaming | ms 단위 실시간이 필요하면 Flink |
| **상태 크기** | 수십 GB 이상 상태 → RocksDB Backend 필수 | 수 GB 이하 → HashMapStateBackend |
| **Event Time 정확도** | 규제 보고서 등 정확한 Event Time 처리 → Flink | Processing Time으로 충분 → Spark |
| **엔지니어링 역량** | Flink는 학습 곡선이 높음,熟练도 필요 | Spark는 생태계가 큼, 커뮤니티资料多 |

*(추가 실무 적용 가이드 - Flink 도입 Decision Tree)*
- **단계 1**: 지연 요구가 1초 이상입니까? → 예: Apache Spark Streaming 고려. 아니오: 다음 단계로.
- **단계 2**: 상태 저장소로複雑な 세션 윈도우, 패턴 매칭 등的状态ful 연산이 필요합니까? → 예: Apache Flink 권장. 아니오: Spark Structured Streaming도 충분.
- **단계 3**: Event Time 순서保证가 중요합니까? (예: 금융 거래 분석, inúmer崩れ克服) → 예: Apache Flink. 아니오: 어느 쪽이든 가능.
- **단계 4**: 팀이 이미 Spark 인프라를 보유하고 있습니까? → 예: Spark Streaming 우선 고려. 아니오: Flink도 충분히 검토.

---

## 5. 실무 적용 및 판단

1. **Flink SQL의 표준화 및 데이타 통합**
   Flink SQL은 Flink 1.9에서 정식 도입되어, 이제 배치와 스트리밍 쿼리를 동일한 SQL 문법으로 작성할 수 있게 되었습니다. Apache Flink의 가장 큰 강점 중 하나는"사용자가 데이터 처리 로직을 어떻게 실행할지(How)가 아니라 무엇을 원하시는지(What)"만 SQL로 기술하면, 프레임워크가 자동으로 최적의 실행 계획을 세우는 선언적(Declarative) 특성입니다. ksqlDB(Confluent)와 Flink SQL의 경쟁을 통해, 스트리밍 SQL이 실시간 분석의 표준 언어로 자리잡는 것이 가속화되고 있습니다.

2. **Flink와 레이크하우스生态系的 결합**
   Apache Iceberg와 Delta Lake가 Flink와 통합됨에 따라, 실시간 스트림을 레이크하우스에 직접 기록하고 그 위에서 일괄 분석하는"Unified Batch + Streaming" 시나리오가 보편화되고 있습니다. Uber는 Flink를 통해 Apache Hudi로 실시간 데이터 ingestion을, LinkedIn은 Kafka와 Flink를 결합하여人力资源 분석 플랫폼을実装しており, 세계적 대규모 서비스의 핵심 백본으로 Flink가 자리잡고 있습니다.

3. **Flink의 serverless 및 managed 서비스 확산**
   AWS Kinesis Data Analytics for Apache Flink(Managed Flink), Google Cloud Dataflow, Azure Stream Analytics 등 주요 클라우드 제공자들이 Flink 기반의 fully managed 스트리밍 분석 서비스를 제공함에 따라, 클러스터 관리의 부담 없이 Flink의高度な 기능을 활용하는 것이 간편해지고 있습니다. 이는"엔지니어가 오직 데이터 처리 로직에 집중"할 수 있는 환경을 만들어, Flink의 진입 장벽을 크게 낮추고 있습니다.

## 🧠 지식 맵 (Knowledge Graph)

*   **Apache Flink核心组件**
    *   **DataStream API**: 시간 기반 스트리밍 처리 (Window, Event Time, Watermark)
    *   **Table API & SQL**: 선언적 데이터 처리 (배치/스트리밍 통합)
    *   **CEP (Complex Event Processing)**: 패턴 기반 이벤트 감지
*   **Flink 상태 관리 아키텍처**
    *   **Keyed State**: 키별로 구분된 상태 (keyBy 후 사용)
    *   **Operator State**: 연산자 전체에 공유되는 상태
    *   **State Backend**: HashMap (Heap) vs RocksDB (디스크)
*   **Exactly-Once 시맨틱스 보장 메커니즘**
    *   2PC (2단계 커밋) + Checkpoint Barriers + 소스 함수 재처리 기능

---

## 6. 기대효과 및 결론

Apache Flink - 상태 기반 스트리밍処理의 完成形은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 실시간 처리의 경쟁력은 더 빨리 흘리는 것보다 시간 의미와 상태 일관성을 잃지 않는 데 있다.

---

## 7. 발전 흐름도

```text
[배치 처리]
    │
    ▼
[마이크로 배치]
    │
    ▼
[Event Stream]
    │
    ▼
[Exactly-once]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Kafka·Pulsar | 이벤트 수집·전달 계층 |
| Event Time·Watermark | 시간 의미를 정의하는 기준 |
| Checkpoint·Exactly-Once | 장애 복구와 전달 보장 핵심 |
| 실시간 OLAP·CEP | 스트리밍 결과 활용 영역 |
