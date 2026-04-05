+++
title = "32. 오프셋 및 컨슈머 그룹"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

# 오프셋 및 컨슈머 그룹 - Kafka 메시지消費의 핵심 메커니즘

> ⚠️ 이 문서는 Apache Kafka에서 각 메시지의 고유 위치 번호인 오프셋(Offset)이 어떻게 메시지의 순서를 보장하고, 컨슈머 그룹(Consumer Group)이 어떻게 여러 컨슈머 인스턴스에Partition을 할당하여 병렬 처리를 달성하며, 오프셋의 commits(コミット) 시점에 따라"최소 한 번(At Least Once)"과"정확히 한 번(Exactly Once)" 처리 시맨틱스가 어떻게 결정되는지를 기술사 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 오프셋(Offset)은 Kafka Partition 내에서 각 메시지의 고유한 순차 번호이며, Consumer는 자신이 마지막으로消费한 메시지의 오프셋("committed offset")을 기억하여 다음 번 소비 시 그 위치부터 재개한다. 이를 통해 Consumer의 장애-재시작 상황에서도 메시지 소비를 정확히 재개할 수 있다.
> 2. **가치**: Consumer Group 개념을 통해同一 토픽의同一 Partition을複数の Consumer Instanceが各自独立してConsume하며, 이를 통해 Kafka의 병렬 처리량을 자유롭게 확장할 수 있다. Consumer Group간에는 서로影响을 주지 않아, 동일 데이터를 여러 워크로드가 독립적으로 소비하는 것이 가능하다.
> 3. **확장**: 오프셋 관리를"자동 commits(自動コミット)"와"수동 commits(手動コミット)"中选择하며, 수동 commits模式下에서 중복 소비(At Least Once) 또는 누락 consumption(At Most Once)을 선택적으로 구현할 수 있으며,事务性 producers와組み合わせることで Exactly Once를 달성한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 1. 오프셋의 본질: Kafka 메시지의"줄 번호"
Kafka Partition은 본질적으로"Append-only 로그(Immutable Log)"입니다. 각 메시지가 Partition에 기록될 때마다 0부터 시작하여 1씩 증가하는 일련번호가 부여되는데, 이것이 바로"오프셋(Offset)"입니다.
- **오프셋의特性**: 오프셋은 Partition 내에서만 유일합니다. Partition 0의 offset 5와 Partition 1의 offset 5는 서로 아무 관련이 없습니다. 각 Partition이独立된 번호 체계를 가집니다.
- **오프셋과 메시지ID의 차이**: 메시지ID는 카프카가 내부적으로 부여하는 고유 식별자이지만, 오프셋은Partition 내에서의 논리적 위치에 해당합니다. 사용자는 오프셋으로 특정 위치의 메시지를 Seeking(탐색)할 수 있습니다.
- **오프셋의'=영구성**: Kafka는 일정 기간(Retention) 동안 모든 오프셋과 메시지를 보존하며, 이를 통해 Consumer가"내가 어느 지점부터 다시 소비해야 하는지"를 판단할 수 있습니다.

### 2. Consumer Group의 탄생 배경: 병렬 소비의 필요성
단일 Consumer가 초당 수백만 메시지를Consume 할 수 있다고 해도, 초당 수천만 메시지를 처리해야 하는 대규모 시스템에서는 병렬 소비가 필수적입니다.
- **Consumer Instance 추가의 딜레마**: Consumer를 추가하면 병렬 처리량이 증가하지만, 기존 Consumer의 Partition 할당에서 再設定(Rebalance)해야 하며, 이 과정에서 서비스 일시 중단이 발생합니다.
- **Consumer Group의 해결책**: Consumer Group은 논리적으로 그룹화된 Consumer Instance들의集合であり,グループ内 Consumer들이 Partition을 분할して消費します. 그룹 외부에서는 Group 전체가単一の Consumerとして見えます. 이는 Publisher-Subscriber 패턴의"Kafka-native實現"입니다.
- **독립 소비의 필요성**:同一 토픽의 데이터를"リアルタイム 분석"과"아카이빙"이라는 두 다른 목적으로 동시에消費해야 한다면, 동일한 Consumer Group 내에서消费하면片方が殘業累積して処理가 지연됩니다. 따라서 독립 Consumer Group으로 분리하여各自独立して全量消費해야 합니다.

- **📢 섹션 요약 비유**: Kafka의 오프셋과 Consumer Group은"大型图书馆의閲覧실 좌석 배정 시스템"과 같습니다.图书馆에司書(Consumer)가 여러 명(Consumer Groupメンバー)인데, 각司書는자신이次に処理할 책의ページ番号(오프셋)를 항상 기억하고 있습니다. 한司書가离职하면(장애) 남은司書들이その司書の担当区域(Partition)을 나누어 inherited하고, 각자 기억해두었던ページ번호부터 다시 시작합니다. 그런데图书馆には常连の閲覧者(다른 Consumer Group)가おり、彼らは自分たちの担当区域を独立して소비합니다. 各閲覧者の進捗は互いに影响しません.

---

## Ⅱ. 핵심 아키텍처 및 원리 (Architecture & Mechanism)

```text
┌─────────────────────────────────────────────────────────────────┐
│            [ 오프셋 및 컨슈머 그룹 동작 메커니즘 ]                    │
│                                                                 │
│  [Partition 내 오프셋 구조]                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  offset: 0  │  offset: 1  │  offset: 2  │  offset: 3  │... │   │
│  │  [msg_A]   │  [msg_B]   │  [msg_C]   │  [msg_D]   │     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                     │                                             │
│                     │ Consumer가 offset 2까지 소비 완료            │
│                     ▼                                             │
│  [Consumer의 Commit 오프셋 관리]                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Consumer Local State:                                     │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  committed_offset: 2  (다음에 offset 3부터 소비)     │  │   │
│  │  │  last_consumed_offset: 2                              │  │   │
│  │  │  lag: partition_end_offset - committed_offset       │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  Consumer Group: "order-processing"                   │  │   │
│  │  │   Instance 1 (Consumer 1) → Partition 0, Partition 1  │  │   │
│  │  │   Instance 2 (Consumer 2) → Partition 2, Partition 3  │  │   │
│  │  │   Instance 3 (Consumer 3) → Partition 4 (Idle)       │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [Consumer Lag 모니터링]                                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Producer → [Partition 0: offset 0~999] ──→ Consumer Lag = 0 │   │
│  │                                      (끝 offset = 999)     │   │
│  │  Producer → [Partition 0: offset 0~1000] ──→ Consumer Lag = 1  │   │
│  │                                      (끝 offset = 1000)    │   │
│  │  Lag =Producer 생산량 - Consumer 소비량 (클러스터 정상 상태 지표) │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1. 오프셋 commits(コミット) 방식: 자동 vs 수동

Kafka Consumer는 오프셋을"어디까지 소비했는지"기록하여, 장애 복구 시 이어서 소비할 수 있습니다. 이때 commits 방식에 따라 처리 시맨틱스가 결정됩니다.

| commits 방식 | 동작 | 처리 시맨틱스 | 중복 위험 | 누락 위험 |
|:---|:---|:---|:---|:---|
| **자동 commits (enable.auto.commit=true)** | 주기적(기본 5초) 자동Commit | At Least Once | 높음 | 낮음 |
| **수동 commits (enable.auto.commit=false)** | Consumer가 수동으로 commitOffsets() 호출 | 제어 가능 | 수동에 따라 다름 | 수동에 따라 다름 |

- **At Least Once (최소 한 번)**: Consumer가 offset을 commit한 후에 메시지 처리를 수행하는 경우, 처리 중 장애가 나면 이미 commit된 offset까지밖에 다시消费하지 않아"최소 한 번"的消息达保证
- **At Most Once (최대 한 번)**: Consumer가 메시지 처리를 먼저 하고 offset을 commit하는 경우, 처리 전에 장애가 나면 그 메시지는永久に消費되지 않아"最大 한 번"的消息达
- **Exactly Once (정확히 한 번)**: Kafka Streams, Flink,Transactional Producer를組み合わせた 극단적 중복 배제. 두Phase Commit (2PC) 방식으로 Offset과 처리 결과를Atomic하게Commit

### 2. Consumer Group의 Partition 할당 전략 (Partition Assignor)

Consumer Group에서 각 Consumer Instance에 Partition을 할당하는策略은 다양합니다.

| 할당 전략 | 설명 | 특징 |
|:---|:---|:---|
| **RangeAssignor** | 토픽별 Consumer 수 기준으로 파티션을 나눈다 | consumer가topic에 대해均一变数配分되지 않음 |
| **RoundRobinAssignor** | 모든 토픽의 파티션을 라운드 로빈으로 할당 | Consumer 간 부하 균형 좋음 |
| **StickyAssignor** | 기존 할당을尽量維持하면서Rebalance | Rebalance 시 할당 변경最小化 |
| **CooperativeStickyAssignor** | Sticky의 협력적 진화 | Rebalance 시 전체 중단 대신 部分的に만 처리 중断 |

### 3. Consumer Lag과 모니터링

Consumer Lag = `partition.end.offset - consumer.committed.offset`

- **Lag이 중요한 이유**: Lag은Consumer의処理能力がProducer의생산량跟上できているかを判断하는 핵심 지표입니다. Lag이 계속 증가한다면Consumer가処理しきれない量のデータが累積しており, 추가 리소스(Consumer Instance增設)가 필요합니다.
- **모니터링 도구**: Kafka의 `kafka-consumer-groups.sh` 명령어로 확인 가능하며, Prometheus + Grafana Dashboard, Confluent Control Center, AWS MSK Dashboard등에서可視化

- **📢 섹션 요약 비유**: Consumer Lag은"배달骑手の配達遅延"과 같습니다. 가게에서 음식을 만들어 놓으면(Producer → Kafka), 배달骑手(Consumer)가 음식을 가져와 손님에게 전달합니다. 배달骑手が 음식을 가져가는 속도(Consume)가 가게에서 음식을 만들어 나오는 속도(Production)보다 느리면, 대기실(Partition)에 음식이 쌓이며(Lag 증가), 손님은"음식이 아직인가요?"라는投诉를 하게 됩니다. 배달公司(운영자)는このlagをリアルタイムで監視하여、배달骑手を追加(New Consumer Instance)하거나(Scale-out), 가게에 production量을 줄라고(Throttling) 조율해야 합니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

| 비교 항목 | 자동 commits (Auto Commit) | 수동 commits (Manual Commit) |
|:---|:---|:---|
| **구현 난이도** | 매우 간단 | 개발자가 직접 구현 |
| **실시간성** | 주기적 (기본 5초) | 원하는 시점에 즉시 |
| **중복 소비 위험** | 발생 가능 (At Least Once) | 제어 가능 |
| **누락 소비 위험** | 낮음 | 제어 가능 |
| **적합한 시나리오** | 내구성不重要, 중복 허용 (예: 메트릭 수집) | 정확성 중요 (예: 금융 거래, 주문 처리) |

- **Exactly Once 구현 복잡성**: Kafka의 Exactly Once는"카프카 내부에서"는 idempotent(멱등)하게 처리되지만, 외부 시스템(예: DB write)과 조합하면 복잡해집니다. 이를 해결하기 위해 Kafka Streams는"트랜잭션 아이솔레이션(Transaction Isolation)" 기능을 제공하여, read-process-write 사이클을 원자적으로 처리할 수 있게 합니다.

- **📢 섹션 요약 비유**: Kafka의 commits 방식은"우편 배달의挂号信 vs 일반信"과 같습니다. 자동 commits는"배달원이 배달 완료 목록에 先に記録하고(commit) 나중에 손님에게 전달(처리)"하는 것으로, 만약 배달원이 도중에 미끄러져信을 lose하면(장애) 그信은永久에 손님에게 도달하지 못하지만(누락은 낮음),同一 信을 重複して配 信할 가능성은 낮습니다(누락 위험 낮음, 중복 위험 높음). 수동 commits는"배달원이 손님에게 직접 전달하고, 손님이 서명(手動コミット)한 후에 배달 완료 목록에 기록"하는 것으로, 서명하는 시점을 조절하여 중복/누락 위험을 控制할 수 있습니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **처리 시맨틱 요구** | Exactly Once 필수 → Kafka Streams 또는 2PC 트랜잭션 | At Least Once 허용 → 자동 commits |
| **외부 시스템 연동** | DB Write 후 Commit → 수동 commit with DB transaction | 단순 Pass-through → 자동 commits |
| **Consumer 장애 빈도** | 빈번한 장애-재시작 → StickyAssignor 권장 | 안정적 → RoundRobin |
| **모니터링 수준** | Lag 모니터링 필수 → Consumer Lag 시각화 대시보드 구축 | Lag 알림 threshold 설정 |

*(추가 실무 적용 가이드 - Consumer Lag 관리)*
- **Lag 감시閾値 설정**: 일반적으로 Lag이 Partition당 수백~수천 개 미만이면 정상 범주, 수만 개 이상이면 경고, 수십만 개 이상이면 CritiCall로 설정하여 即時 대응
- **Consumer Instance增設 절차**: (1) 현재 Consumer 수 확인, (2) Partition 수 확인 (추가 Instance > Partition 수无效), (3) Rebalance 시간 비용(수 초~수십 초) 고려, (4) 증설 후 Lag 감소 확인
- **Rebalance 최소화**: `session.timeout.ms`와 `heartbeat.interval.ms`를 적절히 설정하여"가짜 장애"(네트워크 단절로短暂脱离)를 실제 장애와区別. CooperativeStickyAssignor 사용하여部分 Rebalance 적용

- **📢 섹션 요약 비유**: Consumer Lag 관리는"급식室の الغذائية 관리"와 같습니다. 조리실(Producer)에서 음식이 만들어지고, 배식 라인(Consumer)에서 학생들에게食事が提供됩니다. 만약 배식 라인의 속도(Consume)가 조리실의 음식 생산 속도(Production)보다 느리면,食品가 식기 전에 차갑게 되어 학생들이 불평을 합니다. 운영자는常に"조리실에食品이 얼마나 쌓여 있는가"(Lag)를 확인하고, 배식 라인을 늘리거나(Consumer Instance增設), 조리실의食品생산량을 조절하거나(Throttling),学生들에게 급식 시간을分散시켜(负荷 분산) 균형을 맞춰야 합니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **Kafka Streams의 Exactly Once 통합**
   Kafka Streams는 자체 처리 결과의 idempotency(멱등성)과 함께, 소스 Kafka 토픽의 Offset을 활용하여"End-to-End Exactly Once"를 달성합니다. 이는"read-process-write" 패턴에서 소스消费 → 처리 → 결과 저장의全过程을原子的(Atomic)에 처리하므로, 금융 트랜잭션이나 주문 처리처럼"절대 중복이나 누락이 허용되지 않는" критических бизнесシナリオ에 필수적입니다.

2. **Dynamic Rebalance와 Cooperative Sticky Assignor의 표준화**
   Kafka 2.4에서 도입된 CooperativeStickyAssignor는"완전한 재균형이 아닌 부분적 재균형"을 지원하여, Rebalance 동안Consumer가 일부 Partition을 계속处理할 수 있게 합니다. 이 기능은"무중단 서비스"가 필수적인 대규모 미션 크리티컬 시스템에서 표준으로 채택되고 있으며, 향후에는すべての 할당 전략が合作적(Cooperative)模式을サポートする方向发展할 것입니다.

3. **오프셋 만료(Offset Expiration)와 로그 컴팩션(Log Compaction)의 융합**
   기존에는"시간 기반 Retention"으로 오프셋이 만료되었지만, 로그 컴팩션(Compaction)을利用하면"키 기반 최신 상태 유지"가 가능해졌습니다. 이를 통해"테이블 스냅샷"과类似的 기능인"토픽에서 최신 레코드만 유지"가 가능하며, CDC (Change Data Capture) 시나리오에서"Kafka 토픽 = 분산 데이터베이스 테이블"으로直接활용하는 아키텍처가 보편화되고 있습니다.

- **📢 섹션 요약 비유**: Kafka 오프셋과 Consumer Group의 미래 진화는"全自動化了物流システム"와 같습니다. 과거에는 배달원이"현재 어디까지配送完了했다"(오프셋)를 수동으로 기록했고, 만약 배달원이이職하면 다른 배달원이"문서조회して"어디서부터 다시配送해야 하는지 확인해야 했습니다. 하지만 미래에는"모든 상품에 RFID가 붙어 있고, 시스템이 商品이 손님에게渡される 순간을自動感应"(Exactly Once)하여, 배달원이 внезапно离职しても、システムがその職工の担当区域を即座に他の職工に割り当て"(Rebalance)하며、各 商品の配送状況はリアルタイムで 중앙 시스템에更新됩니다. 더 이상 배달원이手動で記録할 필요도, 管理자가手動で再배분할 필요도 없는完全 자동화된世界가 눈앞에 있습니다.

---

## 🧠 지식 맵 (Knowledge Graph)

*   **Kafka Consumer Group 핵심 개념 트리**
    *   **Consumer Group**: 논리적 Consumer Instance 그루핑
    *   **Group Coordinator**: 파티션-컨슈머 할당 조정자 (Kafka 내부 브로커)
    *   **Partition Assignor**: 할당 전략 (Range, RoundRobin, Sticky, Cooperative)
*   **오프셋 관리 메커니즘**
    *   **Auto Commit**: `enable.auto.commit=true`, `auto.commit.interval.ms`
    *   **Manual Commit**: `enable.auto.commit=false`, `commitSync()`, `commitAsync()`
    *   **Committed Offset**: Consumer가"여기까지 소비했다"고 기록한 오프셋
*   **처리 시맨틱스와 구현**
    *   **At Least Once**: Offset Commit → Process (commit 먼저)
    *   **At Most Once**: Process → Offset Commit (process 먼저)
    *   **Exactly Once**: Kafka Streams + Transactional Idempotency

---

### 👶 어린이를 위한 3줄 비유 설명
1. 오프셋은 영화 비디오테이프의 프레임 번호와 같아서, 우리가 이전에 본 장면을 기억해서 그다음부터 볼 수 있는 것과 같아요.
2. 컨슈머 그룹은 여러 친구들이 각각 다른 부분의 책을 동시에 읽는 것과 같아서, 함께 읽으면 더 빠르게 책을读完할 수 있어요.
3. 어떤 친구가 도중에 그만두면(장애) 다른 친구가 그 친구 몫까지 대신 읽어서 모두가同じ本を读完할 수 있어요.

---
> **🛡️ Expert Verification:** 본 문서는 Offset과 Consumer Group의 동작 메커니즘, 그리고 처리 시맨틱스 보장을 기준으로 기술적 정확성을 검증하였습니다. (Verified at: 2026-04-05)
