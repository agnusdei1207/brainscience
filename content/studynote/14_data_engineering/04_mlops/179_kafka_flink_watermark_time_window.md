+++
weight = 179
title = "179. 카프카 (Kafka) + 플링크 (Flink) 시간 창 (Time Window) 워터마크 (Watermark)"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: Kafka + Flink 조합은 분산 메시지 브로커와 상태 기반(Stateful) 스트림 처리를 결합하여, 수억 이벤트/초 규모의 실시간 분석 파이프라인을 구축한다.
> **비유**: 여러 공정이 연결된 생산 라인처럼, 앞단의 입력 품질과 중간 단계의 흐름 제어가 최종 결과를 좌우하는 구조와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

카프카 (Kafka) + 플링크 (Flink) 시간 창 (Time Window) 워터마크 (Watermark)은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
배치 처리의 한계:
  사기 탐지: T+1일에 발견 → 이미 피해 발생
  실시간 추천: 5분 전 클릭 기반 → 이미 페이지 이탈
  IoT 이상 감지: 1시간 평균 → 장비 이미 고장
  
스트리밍 처리로 해결:
  사기 탐지: 거래 후 100ms 이내 차단
  실시간 추천: 현재 세션 행동 기반
  IoT 이상 감지: 초당 센서 데이터 실시간 모니터링
```

---

## 2. 구성요소

```
┌─────────────────────────────────────────────────────────────┐
│              Apache Kafka 클러스터 구조                       │
│                                                              │
│  Producer → Topic (파티션 분산)  → Consumer Group           │
│                                                              │
│  Topic: "user-events" (파티션 4개)                           │
│  ┌────────────────────────────────────────────────────┐     │
│  │ Partition 0: [msg0] [msg1] [msg4] [msg8] ...        │     │
│  │ Partition 1: [msg2] [msg5] [msg9] ...               │     │
│  │ Partition 2: [msg3] [msg6] [msg10] ...              │     │
│  │ Partition 3: [msg7] [msg11] ...                     │     │
│  └────────────────────────────────────────────────────┘     │
│         │                  │                                 │
│  Broker 1              Broker 2                              │
│  (Leader: P0, P2)      (Leader: P1, P3)                     │
│  (Follower: P1, P3)    (Follower: P0, P2)                   │
│                                                              │
│  Consumer Group A:                                           │
│  - Consumer 0 ← Partition 0, 1                              │
│  - Consumer 1 ← Partition 2, 3                              │
│  (파티션 수 = 최대 병렬 컨슈머 수)                            │
└─────────────────────────────────────────────────────────────┘
```

| Kafka 핵심 개념 | 설명 |
|:---|:---|
| **Topic** | 메시지 범주, 논리적 채널 |
| **Partition** | 토픽의 물리적 분할, 병렬성 단위 |
| **Offset** | 파티션 내 메시지 순서 번호 |
| **Consumer Group** | 소비자 집합, 파티션 균등 할당 |
| **Retention** | 메시지 보존 기간 (기본 7일) |
| **Replication Factor** | 복제 수 (고가용성) |

---

## 3. 구조 및 원리

**핵심 조건**: 카프카 (Kafka) + 플링크 (Flink) 시간 창 (Time Window) 워터마크 (Watermark)은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 시맨틱 | 정의 | 구현 방법 | 성능 영향 |
|:---|:---|:---|:---|
| **At-Most-Once** | 최대 1회 (손실 가능) | 체크포인트 없음 | 가장 빠름 |
| **At-Least-Once** | 최소 1회 (중복 가능) | Flink Checkpoint | 중간 |
| **Exactly-Once** | 정확히 1회 | Flink CP + Kafka TxAPI | 오버헤드 있음 |

```
Flink + Kafka Exactly-Once (2PC):

  ┌────────────────────────────────────────────────────────┐
  │  정상 처리 흐름:                                        │
  │                                                        │
  │  1. Flink Checkpoint 시작                              │
  │  2. 각 Kafka Sink에 Pre-commit (트랜잭션 열기)          │
  │  3. Checkpoint 완료 신호                               │
  │  4. 모든 Sink에 Commit (트랜잭션 확정)                  │
  │  → Kafka 토픽에 메시지 최종 가시화                     │
  │                                                        │
  │  장애 발생 시:                                          │
  │  2단계 사이 장애 → Checkpoint 재시작 → 트랜잭션 롤백   │
  │  → 정확히 한 번만 전달 보장                             │
  │                                                        │
  │  조건:                                                  │
  │  - Kafka transactional.id 설정                         │
  │  - Flink CheckpointingMode.EXACTLY_ONCE                │
  │  - isolation.level = read_committed (소비자 설정)       │
  └────────────────────────────────────────────────────────┘
```

| 항목 | Kafka | Kafka Streams | Flink |
|:---|:---|:---|:---|
| **역할** | 메시지 브로커 | 경량 스트림 처리 | 분산 스트림 처리 |
| **상태 관리** | Partition 기반 | RocksDB (로컬) | RocksDB + 원격 |
| **Checkpoint** | 오프셋 커밋 | Changelog Topic | 분산 스냅샷 |
| **이벤트 타임** | ✗ | 제한적 | ✓ (완전 지원) |
| **복잡한 조인** | ✗ | 제한적 | ✓ |
| **규모** | N/A (브로커) | 중소규모 | 대규모 |
| **운영 복잡도** | 낮음 | 낮음 | 높음 |

---

## 4. 비교 및 연결

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetResetStrategy
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.common.time import Time, Duration
from pyflink.common.watermark_strategy import WatermarkStrategy

env = StreamExecutionEnvironment.get_execution_environment()
env.enable_checkpointing(60000)  # 60초 체크포인트 간격

# Kafka Source 설정
kafka_source = KafkaSource.builder() \
    .set_bootstrap_servers("kafka:9092") \
    .set_topics("user-events") \
    .set_group_id("flink-consumer-group") \
    .set_starting_offsets(KafkaOffsetResetStrategy.LATEST) \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .build()

# Watermark 전략 설정 (Event Time + 30초 지연 허용)
watermark_strategy = WatermarkStrategy \
    .for_bounded_out_of_orderness(Duration.of_seconds(30)) \
    .with_timestamp_assigner(EventTimestampAssigner())

stream = env.from_source(
    kafka_source,
    watermark_strategy,
    "Kafka Source"
)

# 5분 Tumbling Window에서 사용자별 이벤트 수 집계
result = stream \
    .key_by(lambda event: event['user_id']) \
    .window(TumblingEventTimeWindows.of(Time.minutes(5))) \
    .aggregate(CountAggregateFunction()) \
    .filter(lambda count: count.event_count > 100)  # 이상 탐지

result.print()
env.execute("Fraud Detection Job")
```

| 파라미터 | 기본값 | 권장값 | 목적 |
|:---|:---|:---|:---|
| `num.partitions` | 1 | CPU 코어 수 × 배수 | 병렬성 |
| `replication.factor` | 1 | 3 (프로덕션) | 고가용성 |
| `batch.size` | 16KB | 1~2MB | 처리량 향상 |
| `linger.ms` | 0 | 5~20ms | 배치 누적 |
| `compression.type` | none | lz4/zstd | 처리량/비용 |
| `max.poll.records` | 500 | 1000~5000 | 소비자 처리량 |
| `fetch.min.bytes` | 1 | 1MB | 소비자 배치 |

```java
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Checkpoint 설정
env.enableCheckpointing(60_000L); // 60초마다
env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30_000L);
env.getCheckpointConfig().setCheckpointTimeout(120_000L);
env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);

// 상태 백엔드 (RocksDB: 대용량 상태)
env.setStateBackend(new EmbeddedRocksDBStateBackend());
env.getCheckpointConfig().setCheckpointStorage("s3://flink-checkpoints/");
```

---

## 5. 실무 적용 및 판단

| 항목 | 배치 처리 | Kafka + Flink |
|:---|:---|:---|
| **지연 시간** | 분~시간 | 밀리초 |
| **처리 규모** | 제한적 | 수억 이벤트/초 |
| **정확성 보장** | 재처리로 보장 | Exactly-Once |
| **장애 복구** | 전체 재실행 | 마지막 체크포인트부터 |
| **Event Time 집계** | 파일 기준 가능 | Watermark로 정확 보장 |

1. **Watermark 설계**: 허용 지연 시간(lateness tolerance)은 데이터 품질과 지연 레이턴시의 트레이드오프 — 너무 짧으면 데이터 손실, 너무 길면 출력 지연
2. **Exactly-Once 조건**: Flink Checkpoint + Kafka Transactional API 둘 다 필요, 하나만으로는 At-Least-Once
3. **파티션 수 설계**: Kafka 파티션 수 = Flink 병렬도의 상한, 나중에 늘리기 어려우므로 여유 있게 설정
4. **윈도우 선택**: 집계 결과가 중복 없어야 함 → Tumbling, 이동 평균·이상 감지 → Sliding, 세션 분석 → Session

```
┌─────────────────────────────────────────────────────────────┐
│           Apache Flink 클러스터 아키텍처                      │
│                                                              │
│  ┌──────────────────────┐                                    │
│  │  JobManager (마스터)  │                                    │
│  │  - Job 스케줄링       │                                    │
│  │  - Checkpoint 조정    │                                    │
│  │  - 장애 복구 관리     │                                    │
│  └──────────┬───────────┘                                    │
│             │                                                │
│  ┌──────────┼──────────────────────────────────────┐        │
│  │          │                                       │        │
│  ▼          ▼          ▼          ▼                 │        │
│  TaskManager  TaskManager  TaskManager  TaskManager │        │
│  (Slot × N)   (Slot × N)   (Slot × N)   (Slot × N) │        │
│                                                     │        │
│  Task Slot = 병렬 처리 단위                          │        │
│  Pipeline:  Source → Transform → Window → Sink      │        │
│             (각 단계 = 별도 스레드/슬롯)             │        │
└─────────────────────────────────────────────────────┘        
```

```
┌─────────────────────────────────────────────────────────────┐
│                    3가지 시간 개념                             │
│                                                              │
│  Event Time (이벤트 발생 시간):                               │
│  → 실제 사건이 발생한 시간 (이벤트 페이로드에 포함)           │
│  → 가장 정확한 시간적 의미론                                  │
│  → Watermark 필요 (늦은 도착 처리)                           │
│                                                              │
│  Processing Time (처리 시간):                                │
│  → Flink 서버가 이벤트를 처리하는 시간                        │
│  → 구현 간단, 지연 적음                                       │
│  → 네트워크 지연에 따라 결과 달라짐 (재현 불가)               │
│                                                              │
│  Ingestion Time (수집 시간):                                 │
│  → Kafka에서 Flink Source가 이벤트를 받은 시간               │
│  → Event Time과 Processing Time의 중간                       │
└─────────────────────────────────────────────────────────────┘
```

```
늦은 데이터 (Late Data) 문제:

  시간축:    [10:00] [10:01] [10:02] [10:03] [10:04]
  Kafka 도착: 10:00  10:02  10:01  10:03  → 10:01이 늦게 도착!
  
  "10:00~10:02 창에서 10:02에 집계하면 10:01 데이터 누락!"

Watermark 해결:
  W(t) = max_event_time_seen - lateness_tolerance
  
  예: 최신 이벤트 타임 = 10:05, 허용 지연 = 30초
  Watermark = 10:04:30
  
  → "10:04:30 이전 이벤트는 모두 도착했다고 가정"
  → 10:00~10:03 윈도우는 Watermark가 10:03을 넘으면 닫힘
  → 30초 이내 지연 데이터는 처리, 30초 초과 → 늦은 데이터로 처리

┌──────────────────────────────────────────────────────────┐
│  Watermark 진행 흐름                                     │
│                                                          │
│  이벤트 스트림:                                          │
│  t=100 t=102 t=103 t=101 t=105 t=104 t=110 ...          │
│  │     │     │     │     │     │     │                   │
│  W=90  W=92  W=93  W=92  W=95  W=95  W=100              │
│                                                          │
│  (Watermark = 이벤트 타임 최댓값 - 10초 지연 허용)      │
│  (모노토닉 증가, 절대 감소하지 않음)                    │
└──────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────┐
│                     Flink 윈도우 종류                         │
│                                                              │
│  Tumbling Window (비중첩 고정 창):                            │
│  [────10분────][────10분────][────10분────]                  │
│  완전 비중첩, 각 이벤트가 정확히 1개 창에 속함               │
│  용도: 분당 거래 건수, 10분 합계                             │
│                                                              │
│  Sliding Window (슬라이딩 창):                               │
│  [────────10분────────]                                      │
│     [────────10분────────]                                   │
│        [────────10분────────]                                │
│  5분 슬라이드 → 각 이벤트가 2개 창에 중복 속함              │
│  용도: 이동 평균, 이상 탐지                                  │
│                                                              │
│  Session Window (세션 창):                                   │
│  [──이벤트들──] 30초 공백 [──이벤트들──]                    │
│  활동 없으면 창 닫힘, 사용자 세션 분석에 적합               │
│                                                              │
│  Global Window:                                              │
│  [────────────────────────────────]                          │
│  트리거 조건 만족 시 처리 (예: 100개 이벤트마다)            │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 기대효과 및 결론

1.

카프카 (Kafka) + 플링크 (Flink) 시간 창 (Time Window) 워터마크 (Watermark)의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
배치 처리 (MapReduce · Spark Batch)
    │
    ▼
메시지 브로커: Kafka (Topic · Partition · Offset)
    ├─► Producer → Broker → Consumer
    └─► Consumer Group: 파티션별 병렬 소비
    │
    ▼
스트림 처리 엔진: Apache Flink
    ├─► 이벤트 시간 (Event Time) 기반 처리
    ├─► 워터마크 (Watermark): 지연 데이터 허용 범위
    └─► 시간 창 (Window): Tumbling · Sliding · Session
    │
    ▼
실시간 분석: Kafka + Flink → 실시간 대시보드 · 이상 탐지
```
2. Watermark는 "30분 기다렸으니 늦은 편지는 포기하고 결산하자"는 우체부의 규칙 — 무한정 기다릴 수 없으니 기준을 정하는 거야.
3. Exactly-Once는 "편지가 반드시 딱 한 번만 배달되도록" 하는 등기 우편 시스템 — Flink 세이브포인트 + Kafka 트랜잭션이 함께 있어야 가능해!

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 메시지 브로커 | Kafka | 분산 발행-구독 스트리밍 플랫폼 |
| 스트림 처리 | Flink | 상태 기반 분산 스트림 처리 엔진 |
| 시간 개념 | Event Time | 실제 이벤트 발생 시간 |
| 지연 처리 | Watermark | 늦은 이벤트 허용 기준 진행 표시 |
| 집계 단위 | Tumbling Window | 비중첩 고정 크기 시간 창 |
| 집계 단위 | Sliding Window | 중첩 슬라이딩 시간 창 |
| 신뢰성 | Exactly-Once | 2PC 기반 정확히 한 번 처리 |
| 경쟁 기술 | Spark Structured Streaming | 마이크로배치 기반 스트리밍 |
