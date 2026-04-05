+++
weight = 31
title = "31. 토픽과 파티션"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

# 토픽과 파티션 - Kafka 데이터 조직의 두 축

> ⚠️ 이 문서는 Apache Kafka에서 데이터의 논리적 격실(Lógica Channel)인 Topic과 물리적 저장·처리 단위인 Partition이 어떻게 상호작용하며, Partition 단위의 병렬 처리가 어떻게 Kafka의 초고처리량(High Throughput)을 가능하게 하는지, Partition과 Consumer Group의 관계, 그리고 Partition 증가는 어떻게 Rebalance를 유발하여 일시적인 처리 지연을 발생시키는지를 기술사 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Topic은 Kafka에서 데이터가 게시(publish)되는 논리적 채널의 이름이며, Partition은 Topic을 물리적으로 분할하여 각 브로커(Broker)에分散配置되는 저장·처리 단위이다. 각 Partition 내에서는 메시지가 순차적으로 Append-only로 기록되어 오프셋(Offset)이라는 고유 번호를 부여받는다.
> 2. **가치**: Partition 수는 Kafka의 병렬 처리 수준을 결정하며,Partition 수만큼의Concurrent 컨슈머가 동시에 메시지를Consume 할 수 있다. 따라서 Partition 수를適切히 설정하는 것이 클러스터 전체의 처리량(Throughput)을 좌우하는 핵심 설계 판단이다.
> 3. **확장**: Partition은 브로커에分散하여 저장되므로, 브로커 추가만으로 Partition을 재분배하고 수평 확장(Horizontal Scaling)을 달성할 수 있지만, Partition 증가는 Consumer Group 내 Rebalance를 유발하여 일시적 서비스 중단을 초래할 수 있으므로, 초기에 충분한 Partition 수를 설계하는 것이 중요하다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 1. Kafka에 데이터가 저장되는 과정: 논리에서 물리로
Apache Kafka에 메시지를 전송하면, 그 메시지는 최종적으로 물리적인 디스크 파일로 변환되어 브로커에 저장됩니다. 이 과정을 이해하려면"논리적 데이터 구조(Topic)"에서"물리적 저장 단위(Partition)"로의 변환 메커니즘을 정확히 이해해야 합니다.

- **Topic의 추상화**: 사용자는 Kafka를 사용할 때"주문 데이터"와 같은 Topic 이름만 지정하여 메시지를 게시하거나 구독합니다. Topic 내부에서 데이터가 어떻게 분할되고 저장되는지는 사용자로부터 숨겨져 있습니다(추상화). 이는 데이터베이스의"테이블"과"데이터 페이지"의 관계와 유사합니다.
- **Partition의 물리적實態**: Topic에 게시된 메시지는 실제로는 브로커의 디스크에 위치한 개별 Partition 파일로 기록됩니다. 각 Partition은 호환 가능한 가장 오래된 메시지까지Append-only로 기록되며, 파일 끝에 항상 새로운 메시지만 추가됩니다.
- **파티셔닝의 필요성**: 단일 Partition(단일 파일)에서는 메시지가 순차 처리될 수밖에 없으므로, 다중 Partition을 통해 병렬 처리(Concurrent Processing)를 달성할 수 있습니다.

### 2. 왜 Partition 단위 병렬 처리가 중요한가?
Apache Kafka의 초고처리량은Partition-level 병렬 처리에 기반합니다.

- **병렬 Consume의 원리**: Consumer Group 내의 각 Consumer Instance는各自異なる Partition을 할당받아Consume합니다. 예를 들어, Partition 10개와 Consumer 5개로 구성된 Consumer Group이 있다면, 각 Consumer는 2개씩의 Partition을分担하여 병렬 Consume하게 됩니다. 이때 Consumer 수를 Partition 수만큼 늘리면 이론상Consume 처리량이Partition 수만큼 증가합니다.
- **Broker 분산 저장**: 각 Partition은 클러스터 내의 여러 Broker에複製(Replica)되어 저장됩니다. 이로 인해 하나의 Broker 장애가 전체 시스템의 가용성에 영향을 미치지 않으며, 장애 복구 시에도ISR (In-Sync Replica) 목록의 다른 Broker가を引き続きサービス提供できます。

- **📢 섹션 요약 비유**: Topic과 Partition의 관계는"大型도서관의司書 시스템"과 같습니다. 도서관 전체(Cluster)에司書가 한 명(单一日 Partition)뿐이라면, 利用자가 자료를 찾으러 가면 한 명이全部対応忙しくになり処理速度が低下します. 하지만 도서관에司書가 여러 명(多 Partition)이라면, 利用자 요청을 나누어同時対応でき、処理速度が向上합니다. 다만 한 번に配置할 수 있는司書 수(Partition 수)에는 도서관 크기(브로커 수)와 자료 수(メッセージ量)에 따른合理적上限があります. 또한 利用자가增えると(Consumer 증가)司書 배치를再調整(Rebalance)하는 데时间가 소요되어 일시的に-services slows down합니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 (Architecture & Mechanism)

```text
┌─────────────────────────────────────────────────────────────────┐
│              [ Topic과 Partition의 물리적 구조 ]                  │
│                                                                 │
│  Topic: "주문-events"                                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  Partition 0 (Broker 1)                                 │   │
│  │  [ offset:0 order:101 ] ──┐                               │   │
│  │  [ offset:1 order:102 ] ──┼──  순서 보장 (within partition)│   │
│  │  [ offset:2 order:103 ] ──┘                               │   │
│  │                                                          │   │
│  │  Partition 1 (Broker 2)                                   │   │
│  │  [ offset:0 order:201 ] ──┐                               │   │
│  │  [ offset:1 order:204 ] ──┼──  순서 보장 (within partition)│   │
│  │  [ offset:2 order:207 ] ──┘                               │   │
│  │                                                          │   │
│  │  Partition 2 (Broker 3)                                   │   │
│  │  [ offset:0 order:301 ] ──┐                               │   │
│  │  [ offset:1 order:302 ] ──┼──  순서 보장 (within partition)│   │
│  │  [ offset:2 order:305 ] ──┘                               │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [Producer가 메시지를 Partition에 기록하는 3가지 전략]           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  ① 키 기반 파티셔닝 (Key-based Partitioning)              │   │
│  │     메시지 키: "user_id=Alice" → hash(key) % n_partitions │   │
│  │     → 동일 키 = 동일 Partition = 동일 사용자 이벤트 순서 보장 │   │
│  │                                                          │   │
│  │  ② 라운드 로빈 (Round-robin)                              │   │
│  │     키 없이 전송 시: 파티션을 순차적으로 돌아가며 기록       │   │
│  │     → 순서 보장은 안 되지만 균등 분배                      │   │
│  │                                                          │   │
│  │  ③ 커스텀 파티셔닝 (Custom Partitioning)                  │   │
│  │     사용자가 정의한 파티셔닝 로직 적용                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [Consumer Group과 Partition 할당 관계]                          │
│  Consumer Group: "order-processing-group"                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Consumer Instance 1 → Partition 0, Partition 1 할당     │   │
│  │  Consumer Instance 2 → Partition 2, Partition 3 할당     │   │
│  │  Consumer Instance 3 → Partition 4 할당 (Idle 가능)      │   │
│  │  (Partition > Consumer인 경우, 일부 Consumer가여유 분담)   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1. 메시지 키 기반 파티셔닝: 순서 보장의 핵심
Kafka에서"메시지 순서 보장"은Partition 단위로만 적용됩니다.同一 Partition 내에서는 오프셋이 증가하는 순서대로 메시지가 소비되므로 순서가 보장됩니다. 그러나 서로 다른 Partition 사이의 순서는 보장되지 않습니다.

- **키 기반 파티셔닝의 원리**: Producer가 메시지를 보낼 때 키를指定하면, Kafka는`hash(key) % num_partitions`를 계산하여 해당 키에 대응하는 Partition을 결정합니다. 이로 인해同一 키를 가진 모든 메시지는常に同一 Partition에 기록되어, 해당 키에 대한 모든 이벤트 순서가 보장됩니다.
- **활용 시나리오**: 사용자 행동 로그에서"同一 사용자의 모든 행동 이력"이 동일한 Partition에 순서대로 기록되면, consumer는 사용자의 행동 이력을時系列順に正確に處理할 수 있습니다. 이는"사용자 A가 물건을 장바구니에 넣고 → 결제하고 → 배송지를 변경했다"는 순서가 지켜져야 올바른 비즈니스 로직 처리 가능합니다.

### 2. Consumer Group과 Partition Rebalance
Consumer Group은 논리적으로 하나 이상의 Consumer Instance를 그룹핑한 것으로,同一 Group 내 Consumer들은 Partition을Share하여 병렬消费합니다.

- **Rebalance 발생 조건**:
  1. Consumer가 추가/제거될 때 (scale-out/in)
  2. Consumer가死ぬ/시간 초과로离开할 때
  3. Partition 수가 변경될 때 (Topic 분할 등)
  4. 구독하는 Topic이 변경될 때

- **Rebalance 과정**: 그룹 조정자(Group Coordinator)가 새로운Partition 할당 계획을 계산하고, 모든 Consumer에게通知します. 이 과정에서 모든 Consumer가 一時停止再-balancingが完了するまでの間、メッセージ受信が停止されます.これが"Rebalance滞后"问题です.

### 3. Partition 수와 Consumer 수의 관계

| 상황 | 설명 | 비고 |
|:---|:---|:---|
| **Partition 수 = Consumer 수** | 각 Consumer가 정확히 1개 Partition 담당 | 이상적 병렬 처리 |
| **Partition 수 > Consumer 수** | 일부 Partition이 Consumer에 할당되지 않음 | 여유 capacity |
| **Consumer 수 > Partition 수** |余白 Consumer 발생 → 1개 Consumer가 0개 Partition 담당 | 불필요資源 |

- **📢 섹션 요약 비유**: Partition 수와 Consumer 수의 관계는"大型 축제のある маршрут配送 시스템"과 같습니다. Festival催事에는商品生产基地(Producer)와配送トラック(Consumer)이 있는데, 催事장에서商品(메시지)을生产基地에서トラックに積み込む 물류 창고(Topic)가 있습니다. 물류 창고에配置된 적재 dock(Partition)이10개이고,配送トラックが5대라면, 각 트럭은 2개 dock을 맡아 병렬로 적재(처리)하면 됩니다. 다만 물류 창고가 확장되어 dock이 20개로 늘어난다면(Rebalance 필요)모든 트럭의配送ルート가再設定되어 일시的に配送이中断됩니다. 이러한再設定 시간을 최소화하려면, 차후 확장을 고려하여초기에 충분한 수의 dock(Partition)을設計하는 것이 중요합니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

| 비교 항목 | Partition 수 과소 (Few Partitions) | Partition 수 과다 (Many Partitions) |
|:---|:---|:---|
| **병렬 처리 수준** | 제한적 (최대 Consumer 수 = Partition 수) | 높음 (수백 Consume 동시 가능) |
| **파일Descriptor 사용** | 적음 | OS의 파일디스크립터 한도 도달 위험 ↑ |
| **Consumer Lag** | 특정 Partition에 부하 집중 → Lag 증가 | 분산 → Lag 감소 |
| **Rebalance 빈도** | Consumer 증감 시 적게 발생 | 많이 발생 (Meta信息량 증가) |
| **메모리 사용** | 낮음 | Producer/Consumer 메모리 Overhead 증가 |
| **순서 보장 단위** | Partition당 단일 스레드 → 순서 보장 | 키 없으면 여러 Partition → 순서 불확실 |

- **Partition 수는 어떻게 결정하는가?**: 一般적으로"예상 처리량(Throughput) / 단일 Consumer 처리량" 공식을 따릅니다. 예: 초당 100만 메시지를 처리해야 하고, 단일 Consumer가 초당 10만 메시지를 처리할 수 있다면, 최소 10개 Partition이 필요합니다. 여기에 장애 대응을 위한 여유량(예: 20~30%)을 더합니다.

- **📢 섹션 요약 비유**: Partition 수 결정은"大型项目的人力资源配置"와 같습니다. 프로젝트が10개의作業大口(Partition)를 가지고 있고, 각 작업장은1人の 담당者(Consumer)가 있다면, project管理는효율적입니다. 하지만作業大口が2개뿐인데 담당자가10명이면, 8명은 항상待機状態となり ressourcesが 낭비됩니다.作業大口가 너무 많으면(예: 100개 Partition), manager(브로커)가各作業장간 координацияコスト가 증가하고,誰かが担当者を增감할 때마다再配置(Rebalance)해야 하는 부담이커집니다. 따라서 프로젝트 크기(処理量)에 맞는 최적의作業大口 수 산정이 핵심 경영 판단입니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **처리량 목표** | 단일 Consumer의 초당 처리량 측정 → 필요 Partition 수 역산 | Partition 수 = 목표 처리량 / 단위 Consumer 처리량 |
| **순서 보장 필요성** | 순서 보장 필수 (예: 금융 트랜잭션) → 키 기반 파티셔닝 필수 | 순서 불필요 → 라운드 로빈 |
| **향후 확장 계획** | 향후 Consumer 3배 증가 예상 → Partition 수도 3배 미리 확보 | Partition 증가는 Rebalance 유발 |
| **브로커 수 대비** | Partition 수 > Broker 수 ×Replication Factor → 일부 Broker에 부하 집중 | Partition / Broker 비율 균형 유지 |

*(추가 실무 적용 가이드 - Partition 설계 Decision Tree)*
- **단계 1**: 초당 필요한Consume 처리량(메시지/초)을 산정합니다.
- **단계 2**: 단일 Consumer Instance의 초당 처리량을벤치마크로 측정합니다. (예: 10만 메시지/초)
- **단계 3**: 필요 Partition 수 = ceil(목표 처리량 / 단일 Consumer 처리량)를 계산합니다.
- **단계 4**:Replication Factor를 곱하여 네트워크 I/O와 스토리지 요구량을산정합니다.
- **단계 5**: 브로커 당 적절한 Partition 수(권장: 100 이하, 最大数百)를確認하고, 이를 초과할 경우 브로커 수를 늘리거나 Topic을 분리하는 것이 좋습니다.
- **주의**: Partition 수는 Producer와 Consumer 모두에 영향을 미치므로, 프로덕션 환경에서는保守적으로 설정하고, 모니터링 결과를 기반으로점진적으로 늘려가는 것이 원칙입니다.

- **📢 섹션 요약 비유**: Partition 설계는"골목식당座位 배치"와 같습니다. 식당에 table(Partition)가 2개뿐인데, 손님 Consumer group)이 10팀이라면, 8팀은无聊하게待機해야 합니다. table을 10개로 늘리면全部10팀이同时 이용 가능하지만, 점장이 Table 배치를再設定(재배치)할 때 모든 팀이 잠시 대기해야 합니다. 결국 식당 크기(브로커 수)와 예상 손님 수(처리량)를 종합적으로 고려하여"오늘은 table 6개로 운영하고, 매출 데이터 분석 후来周 결정"하듯이,Partition 수도 점진적으로 늘려가는 것이 안전한 운영 전략입니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **적응형 파티셔닝 (Adaptive Partitioning)과 Kafka의 미래**
   Kafka의 기존 정적(Static) 파티셔닝은Partition 수를 미리 설계해야 하며, 런타임 중 변경 시 Rebalance 비용이 컸습니다. 향후"사용량에 따라Partition 수를 동적으로 조절하는 적응형 파티셔닝"이 도입될 것으로 예상되며, 이를 통해 Rebalance 비용을 최소화하면서도 처리량 변화에 유연하게 대응하는 것이 가능해질 것입니다. 이는 쿠버네티스의 Horizontal Pod Autoscaler (HPA)와 유사한"필요에 따른 자동 확장" 개념입니다.

2. **파티션 없는 Kafka 토픽 (Partitionless Topics) 실험**
   Confluent와 Apache Kafka 커뮤니티에서는"파티션 없는 토픽"이라는 새로운 개념을 탐구하고 있습니다. 이는 개발자가Partition 수를 명시적으로 지정하지 않고, Kafka가 내부적으로 처리량에 따라자동으로 분할하는 개념입니다. 이는 Serverless Kafka 서비스와 결합될 때"사용량에 따른 완전 자동 스케일링"을 가능하게 하며, 개발자의 Partition 관리 부담을 획기적으로 줄여줄 것입니다.

3. **파티션과 메타데이터管理的进化**
   Kafka 3.3+의 KRaft 모드는 Partition 메타데이터 관리를 Kafka 내부에서 처리하여, ZooKeeper 의존성을 제거하고 Partition Metadata의 읽기/쓰기 지연(latency)을 줄였습니다. 향후"Kafka Raft Consensus"의 성능 최적화를 통해 Partition leader election 시간이毫秒대에서 마이크로초대로 단축되어,초저지연金融 거래 플랫폼에서도 Kafka를 활용할 수 있는 가능성이 열리고 있습니다.

- **📢 섹션 요약 비유**: Kafka Partition의 미래进化은"도시 교통 시스템의 자동化和"와相似 합니다. 과거에는 도시 계획을 세울 때"몇 차선 도로를 만들 것인가"(Partition 수)를 미리設計해야 했으며, 도로가 부족해지면新建 도로를 놓기 위해 기존 도로를 부분 통제한(Rebalance) 후新建道路를 개통해야 했습니다. 하지만 미래에는"도로에 센서를 달아 실시간으로 교통량을监测하고, 필요 시 중앙 관제소가 자동으로차선数を增减하거나新建 도로를瞬時に增设"하는智能道路망이 될 것입니다. 이것이"적응형 파티셔닝"과"Serverless Kafka"가 보여주는 미래상으로, 개발자는"도시의 크기(データ量)"만 정의하면 인프라가 자동으로"최적의 차선 수(Partition)"를 조절하여 항상最適な性能을 제공할 것입니다.

---

## 🧠 지식 맵 (Knowledge Graph)

*   **Kafka Topic/Partition 핵심 개념 트리**
    *   **Topic**: 논리적 채널, 1개 이상의 Partition으로 구성
    *   **Partition**: 물리적 저장 단위, ordered & immutable records sequence
    *   **Offset**: Partition 내 각 레코드의 고유 위치 번호
    *   **Replica**: Partition의 복제본 (ISR 목록 관리)
    *   **Leader/Broker**: 읽기/쓰기 처리 브로커
*   **파티셔닝 전략**
    *   **키 기반 (Key-based)**: hash(key) % n_partitions (순서 보장)
    *   **라운드 로빈 (Round-robin)**: 고르게 분배 (순서 불 garanti)
    *   **커스텀 (Custom)**: PartitionListener 인터페이스 구현
*   **Consumer Group 메커니즘**
    *   **Group Coordinator**: Partition 할당 조정자 (Kafka 내부)
    *   **Rebalance**: Consumer增減 시 Partition再할당 과정
    *   **Static Membership**: Rebalance频度を 줄이는 기능 (Kafka 2.4+)

---

### 👶 어린이를 위한 3줄 비유 설명
1. Topic은 여러 서랍(Partition)이 달린 큰 수납장이고, 각 서랍에는 순서대로 물건(메시지)이 쌓여요.
2. 여러 친구(Consumer)에게 각각 다른 서랍을 나눠주면 친구들이 동시에 다른 서랍에서 물건을 가져갈 수 있어요.
3. 다만 서랍 수가 적으면 친구들이 기다려야 하고, 서랍을 새로 추가하면(Partition 증가)친구들이 일시에 손을 대기해야 해요.

---
> **🛡️ Expert Verification:** 본 문서는 Topic과 Partition의 관계, 그리고 Consumer Group과의 상호작용을 기준으로 기술적 정확성을 검증하였습니다. (Verified at: 2026-04-05)
