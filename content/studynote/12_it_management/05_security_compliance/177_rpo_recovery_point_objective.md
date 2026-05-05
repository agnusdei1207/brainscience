+++
weight = 177
title = "RPO (Recovery Point Objective)"
date = "2024-03-20"
[extra]
categories = ["it-management", "bcp-drs"]
+++
## 0. 핵심 인사이트

> |

> 📝 모범 답안

1. 재난 발생 시 데이터 유실을 감내할 수 있는 최대 허용 시점으로, 데이터의 무결성 복구 목표를 의미합니다.
2. 비즈니스 연속성을 위해 잃어버려도 되는 '데이터의 양'을 시간 단위로 정의한 지표입니다.
3. RPO=0(데이터 무결성 100% 보장)을 달성하려면 실시간 동기 복제(Synchronous Replication) 기술이 필수적입니다.

### 1. 개요 및 필요성
재해 상황에서 단순히 시스템을 다시 켜는 것(RTO)보다 더 중요한 것은 "어떤 시점의 데이터를 가지고 다시 시작하느냐"입니다. RPO(Recovery Point Objective, 복구 목표 시점)는 사고 발생 전 마지막으로 성공한 백업이나 복제 시점을 정의합니다. 이는 금융, 의료 등 데이터의 정합성이 생명인 분야에서 가장 중요하게 다뤄지는 업무 연속성 지표입니다.

### 2. 구성요소

```text
[ Timeline of Data Loss ]
      (Last Successful Backup)      (Disaster Occurs)
             Point A                      Point B
                | <---------- RPO ----------                v                             v
----------------+-----------------------------+-------------> (Time)
                |      [ Data Loss Gap ]      |
                | - Transactions Lost         |
                | - Re-entry Required         |
```

**Bilingual Key Components:**
- **데이터 무결성 목표 (Data Integrity Goal):** 재해 후 복구된 데이터가 얼마나 최신 상태인지를 나타냅니다.
- **실시간 동기 복제 (Sync Replication):** RPO=0을 위해 주 센터와 DR 센터의 DB를 실시간으로 똑같이 맞춥니다.
- **비동기 복제 (Async Replication):** 일정한 시간 간격(예: 1시간)을 두고 데이터를 전송하며, RPO가 0보다 큽니다.

### 3. 구조 및 동작 원리

| 비교 항목 | RPO (Recovery Point Objective) | RTO (Recovery Time Objective) |
| :--- | :--- | :--- |
| **관심 자산** | 데이터 (Data) | 서비스/시스템 (Service/System) |
| **측정 포인트** | 과거 시점 (Past Point) | 미래 복구 소요 시간 (Future Duration) |
| **기술적 대응** | Replication, Snapshot, Backup | Clustering, Failover, HA |
| **장애 시 영향** | 데이터 재입력/복구 노동 발생 | 비즈니스 거래 중단 및 신뢰도 하락 |

### 4. 비교 및 트레이드오프
기술사로서 RPO는 데이터의 중요도와 네트워크 대역폭(Cost) 사이의 트레이드 오프를 최적화해야 합니다.
- **전략적 설계:** RPO를 0으로 설정하면 주 센터의 성능이 저하(데이터 복제 대기)될 수 있습니다. 금융 거래 같은 고부가가치 데이터는 Sync 방식을, 로그나 통계 데이터는 Async 방식을 적용하는 하이브리드 전략이 필요합니다.
- **감리 주안점:** 백업 주기가 RPO 목표를 준수하고 있는지, 백업본의 정합성이 실제로 보장되는지(Restore Test), 그리고 원격지 전송 시 네트워크 지연이 RPO를 초과하지 않는지 점검해야 합니다.

### 5. 실무 적용 및 최적화 기법
RPO는 기업의 데이터 자산 보호 수준을 나타내는 척도입니다. 최근에는 스토리지 기반의 스냅샷과 클라우드 기반의 실시간 스트리밍 복제가 보편화되면서 RPO 단축 비용이 예전보다 많이 저렴해졌습니다. 향후에는 블록체인 기반의 분산 원장 기술을 통해 원천적으로 데이터 유실이 불가능한(RPO=0) 고신뢰 아키텍처가 확산될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** BCP (Business Continuity Planning), Disaster Recovery
- **하위 개념:** Synchronous/Asynchronous Replication, Snapshot
- **연관 개념:** RTO, Data Integrity, CDC (Change Data Capture)

### 👶 어린이를 위한 3줄 비유 설명
1. **RPO**는 게임을 하다가 컴퓨터가 꺼졌을 때, "얼마나 전으로 돌아가야 하느냐"를 정하는 약속이에요.
2. 5분 전 세이브 데이터로 시작할지, 아니면 아침에 했던 처음부터 다시 할지 미리 정해두는 거죠.
3. 세이브(백업)를 자주 할수록 데이터는 안전하지만, 게임이 조금씩 느려질 수도 있어요!
