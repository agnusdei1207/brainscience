+++
weight = 77
title = "02. Apache Kafka - 메시징에서 데이터 허브로의 진화"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Apache Kafka - 메시징에서 데이터 허브로의 진화은(는) 끊임없이 들어오는 이벤트를 낮은 지연으로 처리하면서 상태·시간·정확성을 제어하는 실시간 처리 핵심 기술이다.
> **비유**: 흐르는 고속도로의 차량을 멈추지 않고 실시간으로 분류하고 통제하는 관제센터와 같다.

📝 모범 답안

## 1. 개요 및 필요성

- **Topic (토픽)**: Kafka에서 데이터가 发布되는 논리적 채널입니다. RDBMS의 테이블과 유사하지만, 스키마가 없으며 단순히"이름이 있는 데이터 스트림"입니다.
- **Partition (파티션)**: 토픽을 물리적으로 분할한 단위입니다. 각 파티션은 클러스터의 여러 브로커에分散して配置되며, 각 파티션 내에서는 메시지가 순차적으로 Append-only로 기록됩니다. 파티션 수는 토픽의 병렬 처리 수준을 결정하며, 파티션 수 만큼의 컨슈머가 동시에 메시지를 소비할 수 있습니다.
- **Offset (오프셋)**: 각 파티션 내에서 메시지의 고유한 위치 번호입니다. `offset=0`이 첫 번째 메시지이며, 이후 각 메시지는 고유한 오프셋을 가집니다. Consumer는 자신이 마지막으로消费한 오프셋(`committed offset`)을覚えておいて、次のメッセージ부터再開します。

---

## 2. 구성요소

Kafka의 가장 중요한 설계 특성 중 하나는 Producer와 Consumer의 완전한 분리입니다.

- **Producer(생산자)**: 메시지를 생성하여 특정 토픽의 특정 파티션에ublish합니다. 파티션 선택 전략은 기본적으로 라운드 로빈(Round-robin)이지만, 메시지의 키(Key)를 지정하면同一 키를 가진 메시지는同一 파티션에 순서 보장으로 기록됩니다.
- **Consumer(소비자)**: 컨슈머는 자신이 읽은 오프셋을 관리합니다. Kafka는 Consumer Group(소비자 그룹) 개념을 지원하여,同一 그룹 내의 컨슈머들은各자 다른 파티션을 할당받아 병렬로 소비합니다. 다른 그룹의 컨슈머는 서로独立적으로 같은 메시지를 소비할 수 있어, 1:N 배포가 가능합니다.

---

## 3. 구조 및 원리

**핵심 조건**: 이벤트 시간, 상태 저장, 지연 허용, 전달 보장이 함께 통제되어야 한다.

동작 순서:
| 비교 항목 | Apache Kafka | RabbitMQ / ActiveMQ (전통적 MOM) |
|:---|:---|:---|
| **메시지 보존 (Retention)** | 설정 기간(시간~무제한) 동안 보존, Replay 가능 | Consumption 후 즉시 삭제 (일반적) |
| **메시지 순서 보장** | 파티션 내에서 순서 보장 | 큐 단위 순서 보장, 분산 환경에선 제한적 |
| **컨슈머 모델** | 컨슈머 그룹별 독립消费 (Pub-Sub) | 포인트 투 포인트 (하나만 소비) |
| **처리량 (Throughput)** | 초당 수백만 건 (Sequential I/O) | 초당数万~数十万 건 |
| **메시지 필터링/라우팅** | 키 기반 파티셔닝만 (파티션 단위) | exchange 타입별 다양한 라우팅 (topic, headers, etc.) |
| **메시지 크기** | 기본 1MB, 설정으로 수 MB까지 | 일반적으로 수 KB ~ 수십 KB |

- **Kafka의 가장 큰 강점**: "이벤트 소싱(Event Sourcing)"과 "CDC (Change Data Capture)" 아키텍처에서 Kafka는 핵심 인프라로 활용됩니다. 예를 들어, 데이터베이스의 모든 변경 사항(INSERT/UPDATE/DELETE)을 Kafka topic으로 publish하고, 이를 여러 Sink(Redshift, Elasticsearch, BigQuery 등)가 동시에消费하면, 하나의 데이터 원본(DB)에서 다양한 목적지(분석, 검색, 캐시 갱신 등)로의Real-time 데이터 파이프라인을 구성할 수 있습니다.

---

## 4. 비교 및 연결

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **메시지 순서 요구** | 순서 보장이 필수 (예: 금융 거래) → 키 기반 파티셔닝 필수 | 파티션 수 = 키별 파티션 수 고려 |
| **내구성 요구 수준** | 장애 시 절대 데이터 손실 불가 → acks=all + min.insync.replicas=2 | 데이터 소실 허용 수준에 따라 acks 조절 |
| **리텐션 기간** | Replay 필요 (예: CDC, 감사 로그) → 긴 Retention | 일회성 처리면 짧은 Retention으로 스토리지 절약 |
| **컨슈머 독립성** | 다수의 독립적인 컨슈머가同一 데이터 필요 → Kafka | 하나의 컨슈머만 필요 → RabbitMQ 고려 |

*(추가 실무 적용 가이드 - Kafka Topic 설계 Best Practices)*
- **파티션 수 결정**: 파티션 수는 컨슈머 수의 상한을 결정합니다. 파티션 수 = 최대 동시 컨슈머 수로 설계하되, 향후扩展을 고려하여 余白을 둡니다. 파티션 추가 후에는 키와 파티션 간 매핑이 변경될 수 있어 주의가 필요합니다.
- **메시지 키 활용**: 순서 보장이 필요한 메시지(예:同一 사용자의 모든 이벤트)에는同一 키(예: user_id)를 사용하여同一 파티션에 순서대로 기록되도록 합니다.
- **컴팩션(Compaction)**: 로그 컴팩션 모드를 설정하면,同一 키의 최신 메시지만 보존하여 무제한 Retention이 가능하며, 최신 상태 조회(테이블 스냅샷과 유사)가 가능합니다.
- **실무 의사결정**: Kafka를 이벤트 버스(Enterprise Service Bus, ESB) 대안으로 활용할 때는, 토픽 수와 파티션 수가 클러스터 자원의 한계에 도달하지 않도록 모니터링하고, 필요한 경우 주기적으로旧토픽을 아카이브/삭제하는 kebijakan를 수립해야 합니다.

---

## 5. 실무 적용 및 판단

1. **KRaft (Kafka Raft) 모드의 일상화: ZooKeeper 의존성 제거**
   Kafka 3.3 (2022)에서 정식 도입된 KRaft 모드는, 분산 코디네이션을 위해 외부 의존성(ZooKeeper)을 제거하고 Kafka 자체의 Raft 프로토콜 구현(KRaft)을 사용하여 클러스터 메타데이터를 Kafka 내부에서管理합니다. 이를 통해" ZooKeeper 단일 장애점(SPOF) 제거"와"운영 복잡성 감소"라는 두 가지 목표를 동시에 달성하며, 향후 모든 Kafka 클러스터가 KRaft 모드로 마이그레이션되는 것이 예상됩니다.

2. **Kafka와 레이크하우스/스트리밍 SQL의 심화 통합**
   Confluent의 ksqlDB, Apache Flink SQL, Spark Structured Streaming 등 다양한 스트리밍 SQL 엔진이 Kafka를 네이티브 소스로 활용하는 사례가 급증하고 있습니다. 특히"Kafka topic을 테이블로 조회"하거나"Kafka Streams를 사용하여 실시간 aggregated view를 생성"하는功能が 표준화됨에 따라, Kafka는 단순한 메시징 Infra에서"실시간 데이터 접근을 위한 가상화된视图(View)" 역할로 진화하고 있습니다.

3. **Serverless Kafka와 Managed Service의 확산**
   AWS MSK Serverless, Confluent Cloud의 Serverless Tier 등 완전 관리형 Kafka 서비스가 확산됨에 따라, 클러스터 프로비저닝, 브로커 모니터링, 리밸런싱 등의 운영 부담이 크게 감소하고 있습니다. 이는 엔지니어가"Kafka 운영"이 아닌"Kafka를 활용한 데이터 스트림 설계"에 집중할 수 있는 환경을 만들어, Kafka의 진입 장벽을 획기적으로 낮추고 있습니다.

## 🧠 지식 맵 (Knowledge Graph)

*   **Apache Kafka 핵심概念**
    *   **Topic**: 논리적 데이터 채널 (파티션들의集合)
    *   **Partition**: 물리적 처리 단위, 각 파티션은ordered, immutable sequence of records
    *   **Offset**: 파티션 내 레코드 고유 위치 번호
    *   **Producer**: 메시지 게시자 (키 기반 파티셔닝)
    *   **Consumer Group**: 컨슈머들의 논리적 그룹 (파티션 공유)
*   **Kafka 내구성 메커니즘**
    *   **ISR (In-Sync Replica)**: 리더와 동기화된 복제본 집합
    *   **acks**: 생산자 확인 응답 설정 (0, 1, all)
    *   **min.insync.replicas**: 동기화 필수 최소 리플리카 수
*   **Kafka 버전 변화**
    *   Kafka 0.8~2.x: ZooKeeper 의존 (컨트롤러, 메타데이터)
    *   Kafka 3.3+ (KRaft): ZooKeeper 제거, 자체 Raft 프로토콜

---

## 6. 기대효과 및 결론

Apache Kafka - 메시징에서 데이터 허브로의 진화은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 실시간 처리의 경쟁력은 더 빨리 흘리는 것보다 시간 의미와 상태 일관성을 잃지 않는 데 있다.

---

## 7. 발전 흐름도

```text
[전통적 MOM]
    │
    ▼
[Pub/Sub]
    │
    ▼
[Append-only Log]
    │
    ▼
[KRaft/Serverless Kafka]
```

이 흐름도는 전통적 MOM에서 Pub/Sub와 Append-only Log로 발전해 KRaft/Serverless Kafka로 진화하는 메시징 구조의 변화를 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Kafka·Pulsar | 이벤트 수집·전달 계층 |
| Event Time·Watermark | 시간 의미를 정의하는 기준 |
| Checkpoint·Exactly-Once | 장애 복구와 전달 보장 핵심 |
| 실시간 OLAP·CEP | 스트리밍 결과 활용 영역 |
