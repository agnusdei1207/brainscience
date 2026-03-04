+++
title = "Distributed Database Theory (CAP, PACELC, Sharding)"
description = "분산 시스템의 근간이 되는 CAP 정리와 이를 확장한 PACELC 이론, 그리고 대규모 데이터 처리를 위한 샤딩(Sharding) 아키텍처를 심층 분석하여 고가용성과 일관성 사이의 전략적 선택 방안을 제시합니다."
date = 2024-03-24
[taxonomies]
tags = ["database", "distributed_system", "cap_theorem", "pacelc", "sharding", "consistency", "availability", "partition_tolerance"]
categories = ["studynotes-05_database"]
+++

# 분산 데이터베이스 이론 (CAP, PACELC, Sharding)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 환경에서 데이터 일관성(Consistency), 가용성(Availability), 파티션 허용성(Partition Tolerance) 사이의 근본적인 트레이드오프를 정의하고, 장애 시와 정상 시의 동작을 결정하는 이론적 체계입니다.
> 2. **가치**: 단일 서버의 물리적 한계를 넘어 무한 확장 가능한 수평적 확장성(Scale-out)을 제공하며, 비즈니스 특성에 맞는 최적의 정합성 모델을 선택할 수 있는 설계 가이드를 제공합니다.
> 3. **융합**: NoSQL 데이터베이스(HBase, Cassandra, MongoDB)와 뉴SQL(Spanner, TiDB), 그리고 클라우드 네이티브 아키텍처의 데이터 계층 설계의 핵심 원리입니다.

---

## Ⅰ. 개요 (Context & Background)

현대 IT 인프라는 폭발적으로 증가하는 데이터와 트래픽을 처리하기 위해 단일 고성능 서버(Scale-up)에서 저가용성 범용 서버의 집합(Scale-out)으로 패러다임이 전환되었습니다. 분산 데이터베이스는 물리적으로 떨어진 여러 노드에 데이터를 분산 저장하고 관리하면서도, 사용자에게는 하나의 거대한 논리적 시스템으로 보이게 하는 기술입니다. 이 과정에서 필연적으로 발생하는 네트워크 단절과 지연 시간(Latency) 하에서 어떻게 시스템의 신뢰성을 유지할 것인가가 분산 데이터베이스 이론의 핵심 과제입니다.

**💡 일상생활 비유: 여러 지점을 둔 프랜차이즈 식당**
한 식당이 인기가 많아져 전국에 지점을 냈다고 가정해봅시다. (분산 시스템)
- **일관성(C)**: 서울 지점에서 메뉴 가격을 올리면 부산 지점에서도 즉시 동일한 가격으로 팔아야 합니다.
- **가용성(A)**: 서울과 부산 사이의 통신이 끊겨도(P), 각 지점은 손님에게 음식을 계속 팔아야 합니다.
- **파티션 허용성(P)**: 지점 간 전화선이 끊기는 상황입니다.
만약 본사가 "무조건 전국 가격이 똑같아야 해!"(C)라고 고집한다면, 통신이 끊겼을 때 부산 지점은 가격 확인이 안 되어 장사를 중단해야 합니다(A 포기). 반대로 "통신이 끊겨도 일단 장사는 해야지!"(A)라고 하면 지점마다 가격이 달라질 수 있습니다(C 포기).

**등장 배경 및 발전 과정**
1. **RDBMS의 한계**: 전통적인 관계형 데이터베이스는 강한 일관성(ACID)을 준수하지만, 분산 환경에서 수평적 확장이 매우 어렵고 가용성이 떨어지는 한계가 있었습니다.
2. **Web 2.0과 빅데이터**: 구글, 아마존, 페이스북 등 거대 플랫폼의 등장으로 수조 건의 데이터를 초저지연으로 처리해야 하는 요구사항이 발생했습니다.
3. **CAP 정리의 등장 (2000년)**: Eric Brewer가 "분산 시스템은 C, A, P 중 두 가지만 선택할 수 있다"는 정리를 발표하며 NoSQL 부흥의 이론적 토대를 마련했습니다. 이후 2012년 Daniel Abadi가 정상 상황에서의 지연 시간까지 고려한 PACELC로 이를 확장했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 분산 시스템 이론의 핵심 요소

| 요소명 | 상세 역할 및 정의 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Consistency (일관성)** | 모든 노드가 같은 시점에 동일한 데이터를 보장 | Read/Write 락, 동기 복제(Synchronous Replication) | RDBMS, Paxos, Raft | 전국 지점 동시 가격 인상 |
| **Availability (가용성)** | 모든 요청에 대해 성공/실패 응답을 보장 (일부 노드 장애 시에도) | 로드 밸런싱, 리플리카 비동기 복제, 무상태 서버 | Cassandra, DynamoDB | 전화 안 돼도 일단 장사 |
| **Partition Tolerance (파티션 허용성)** | 노드 간 네트워크 단절 상황에서도 시스템 유지 | 고장 감지(Heartbeat), 쿼럼(Quorum) 기반 의사결정 | Gossip Protocol | 전화선 끊김 대비 |
| **Sharding (샤딩)** | 데이터를 특정 기준(Key)에 따라 물리적으로 분할 저장 | 해시 함수, 범위 분할, 룩업 테이블 기반 분배 | Vitess, MongoDB Sharding | 손님 성씨별로 전담 지점 배정 |
| **Replication (복제)** | 동일 데이터를 여러 노드에 복제하여 가용성 확보 | Master-Slave, Multi-Master, Leaderless | MySQL Group Replication | 메뉴판 복사본 비치 |

### 2. 분산 데이터베이스 구조 다이어그램 (Sharded Architecture)

아래 다이어그램은 애플리케이션 계층에서 샤딩 프록시를 거쳐 물리적 데이터 노드로 데이터가 분산되는 대규모 분산 DB의 구조입니다.

```text
                                [Application Layer]
                                         |
                                         V
        +-----------------------------------------------------------------------+
        |                    [Sharding Proxy / Middleware]                      |
        | (Route queries based on Shard Key, Merge Results, Transaction Coord.) |
        +-----------------------------------------------------------------------+
                |                        |                        |
        +-------V-------+        +-------V-------+        +-------V-------+
        |   [Shard 1]   |        |   [Shard 2]   |        |   [Shard 3]   |
        |  (A-G users)  |        |  (H-N users)  |        |  (O-Z users)  |
        +---------------+        +---------------+        +---------------+
          /     |     \            /     |     \            /     |     \
     [Leader] [Rep] [Rep]     [Leader] [Rep] [Rep]     [Leader] [Rep] [Rep]
        (Consistency via Consensus: Raft / Paxos / 2PC)
```

### 3. 심층 동작 원리

#### A. CAP 정리의 심층 해석
- **CP 시스템 (Consistency + Partition Tolerance)**: 네트워크 파티션 발생 시, 데이터 일관성을 위해 서비스를 중단(가용성 포기)합니다. 주로 금융 결제, 재고 관리 등 정합성이 생명인 서비스에 사용됩니다. (예: HBase, MongoDB Default, Redis)
- **AP 시스템 (Availability + Partition Tolerance)**: 네트워크 파티션 발생 시, 데이터가 틀릴 수 있더라도 서비스는 계속 제공(일관성 포기)합니다. 나중에 네트워크가 복구되면 데이터 정합성을 맞춥니다(Eventual Consistency). (예: Cassandra, DynamoDB, CouchDB)
- **CA 시스템**: 분산 시스템에서는 네트워크 장애(P)가 반드시 발생하므로, 이론적으로 존재하기 어렵거나 단일 노드 시스템에 해당합니다.

#### B. PACELC 이론 (CAP의 확장)
CAP는 '장애 상황'만을 가정하지만, PACELC는 '정상 상황'에서의 지연 시간(Latency) 트레이드오프를 추가합니다.
- **P(If Partition)**: 파티션 발생 시 **A(Availability)**와 **C(Consistency)** 중 무엇을 택할 것인가?
- **E(Else)**: 정상 상황 시 **L(Latency)**과 **C(Consistency)** 중 무엇을 택할 것인가?
- **예시 (PA/EL)**: 장애 시 가용성 택, 정상 시 응답 속도(Latency)를 위해 일관성을 양보함 (DynamoDB).

#### C. 샤딩(Sharding) 메커니즘
데이터를 쪼개는 방식에는 크게 3가지가 있습니다.
1. **Hash Sharding**: 샤드 키를 해싱하여 결과값에 따라 노드 배치. 데이터가 균등하게 분산되나 노드 증설 시 데이터 재배치(Resharding) 비용이 큼. (Consistent Hashing으로 해결 가능)
2. **Range Sharding**: 특정 범위(예: 날짜, ID 범위)로 분할. 특정 범위에 데이터가 몰리는 'Hotspot' 문제 발생 가능.
3. **Directory Sharding**: 어떤 데이터가 어느 샤드에 있는지 별도의 룩업 테이블(Metadata Store) 관리. 유연하지만 메타데이터 서버가 병목이 될 수 있음.

### 4. 실무 코드 및 알고리즘 (Consistent Hashing Concept)

샤딩 시 노드 추가/제거 시 데이터 이동을 최소화하는 **Consistent Hashing**의 개념적 구현입니다.

```python
import hashlib

class ConsistentHashing:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = dict()
        self.sorted_keys = []
        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def get_node(self, item):
        if not self.ring:
            return None
        key = self._hash(item)
        for node_key in self.sorted_keys:
            if key <= node_key:
                return self.ring[node_key]
        return self.ring[self.sorted_keys[0]]

    def _hash(self, val):
        return int(hashlib.md5(val.encode()).hexdigest(), 16)

# 사용 예시
ch = ConsistentHashing(["Node-A", "Node-B", "Node-C"])
print(f"User123 resides in: {ch.get_node('User123')}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. CAP vs ACID vs BASE 비교

분산 DB를 이해하기 위해서는 전통적인 트랜잭션 이론(ACID)과 분산 환경의 가용성 중심 이론(BASE)을 비교해야 합니다.

| 구분 | ACID (Traditional RDBMS) | BASE (Distributed NoSQL) |
| :--- | :--- | :--- |
| **철학** | 완벽한 정합성 및 비관적 제어 | 고가용성 보장 및 낙관적 제어 |
| **핵심 요소** | Atomicity, Consistency, Isolation, Durability | Basically Available, Soft state, Eventual consistency |
| **데이터 정합성** | 강한 일관성 (Immediate Consistency) | 최종적 일관성 (Eventual Consistency) |
| **확장성** | 수직적 확장 (Scale-up) 위주 | 수평적 확장 (Scale-out) 위주 |
| **장점** | 데이터 무결성 완벽 보장 | 뛰어난 확장성 및 장애 내구성 |
| **단점** | 고비용, 분산 환경 확장 한계 | 일시적 데이터 불일치 발생 가능 |

### 2. 과목 융합 관점 분석
- **네트워크**: CAP의 'P(Partition)'는 네트워크 계층의 신뢰성과 직결됩니다. TCP의 재전송 메커니즘이나 타임아웃 설정은 분산 DB가 장애를 판단하는 중요한 파라미터가 됩니다.
- **운영체제**: 데이터 복제 과정에서의 I/O 성능과 메모리 버퍼링은 OS의 파일 시스템 처리 능력 및 커널 수준의 네트워크 스택 성능에 의존합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)
- **시나리오 A: 이커머스 장바구니 서비스 (AP 중심 설계)**
  - **상황**: 블랙프라이데이와 같은 대규모 트래픽 발생 시, 서버 한두 대가 죽더라도 고객은 장바구니에 물건을 담을 수 있어야 함.
  - **판단**: 장바구니 데이터는 조금 늦게 동기화되어도(최종적 일관성) 결제 단계에서 다시 검증하면 됨. 따라서 가용성을 극대화한 Cassandra와 같은 AP 시스템을 도입하고, Read Repair나 Anti-entropy 과정을 통해 데이터를 정정하는 전략 수립.
- **시나리오 B: 은행 계좌 이체 시스템 (CP 중심 설계)**
  - **상황**: A 계좌에서 100만 원을 빼서 B 계좌로 넣는 도중 네트워크 단절 발생.
  - **판단**: 돈이 복사되거나 사라지면 절대 안 됨. 가용성이 일시적으로 떨어지더라도(시스템 응답 불가) 무조건 강한 일관성을 보장하는 Spanner 또는 Raft 합의 알고리즘 기반의 분산 DB를 사용하고, 2PC(Two-Phase Commit) 또는 Saga 패턴으로 분산 트랜잭션 관리.

### 2. 도입 시 고려사항 (체크리스트)
- **데이터 모델링**: 샤딩을 도입할 경우, 샤드 간 조인(Cross-shard Join)은 성능을 파괴합니다. 데이터 모델링 단계에서 조인이 필요 없도록 비정규화하거나, 동일한 샤드 키를 공유하도록 설계해야 합니다.
- **Shard Key 선정**: 특정 샤드에만 부하가 몰리지 않도록 카드널리티(Cardinality)가 높고 시간 순차적이지 않은 키를 선정해야 합니다.
- **Quorum 설정**: Read Quorum(R) + Write Quorum(W) > Number of Replicas(N) 공식을 통해 일관성 수준을 동적으로 조절해야 합니다.

### 3. 주의사항 및 안티패턴 (Anti-patterns)
- **과도한 샤딩 (Over-sharding)**: 데이터 규모가 작음에도 불구하고 향후 확장을 위해 너무 많은 샤드로 쪼개면 관리 오버헤드와 쿼리 성능 저하만 초래합니다.
- **샤드 키 변경 불가**: 운영 중인 시스템에서 샤드 키를 바꾸는 것은 거의 불가능에 가까운 재구축 작업을 의미합니다. 초기 설계 시 신중을 기해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (Single Node) | 도입 후 (Distributed/Sharded) | 비고 |
| :--- | :--- | :--- | :--- |
| **처리량 (Throughput)** | 서버 사양에 고착 (Max 10k TPS) | 선형적 증가 (Shard 수 비례, 100k+ TPS) | 비용 대비 성능 향상 |
| **가용성 (SLA)** | Single Point of Failure (99.9%) | Multi-Region/Node 복제 (99.999%+) | 비즈니스 연속성 확보 |
| **데이터 크기** | 디스크 물리 한계 (수 TB) | 무제한 확장 (수 PB 이상) | 빅데이터 처리 가능 |

### 2. 미래 전망 및 진화 방향
- **NewSQL의 부상**: Google Spanner, CockroachDB와 같이 CAP의 한계를 극복하기 위해 원자 시계(Atomic Clock)나 정교한 합의 알고리즘을 사용하여 강한 일관성과 수평적 확장을 동시에 잡으려는 시도가 표준이 되고 있습니다.
- **Serverless Database**: 개발자가 샤딩이나 복제를 고민하지 않아도 클라우드가 트래픽에 따라 자동으로 샤드를 늘리고 줄이는 추상화된 데이터 레이어로 진화하고 있습니다.

### 3. ※ 참고 표준/가이드
- **IEEE Standard for Distributed Database Architecture**
- **NoSQL Ecosystem Standards (de facto)**

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [`[ACID & BASE]`](@/studynotes/05_database/01_relational/acid.md) : 트랜잭션의 엄격함과 유연함 사이의 철학적 차이.
- [`[Consensus Algorithms (Raft/Paxos)]`](@/studynotes/02_operating_system/02_process_thread/_index.md) : 분산 노드 간에 일관된 상태를 합의하기 위한 핵심 알고리즘.
- [`[Microservices Architecture (MSA)]`](@/studynotes/04_software_engineering/01_sdlc/msa.md) : 서비스별로 독자적인 분산 DB를 가지며 Polyglot Persistence를 구현하는 아키텍처.
- [`[Event Driven Architecture]`](@/studynotes/15_devops_sre/03_automation/cicd_gitops.md) : 최종적 일관성을 구현하기 위해 메시지 브로커를 활용하는 방식.

---

## 👶 어린이를 위한 3줄 비유 설명
1. **CAP 정리**: "전국 지점이 모두 똑같은 정보를 가질지(C), 아니면 통신이 끊겨도 손님을 받을지(A)"를 결정하는 세 가지 선택지 중 두 가지만 고를 수 있다는 마법의 규칙이에요.
2. **샤딩**: 엄청나게 큰 백과사전을 한 권에 담을 수 없어서 "ㄱ~ㄹ", "ㅁ~ㅅ" 하는 식으로 여러 권으로 나눠서 여러 친구가 나눠 들고 있는 것과 같아요.
3. **결론**: 무조건 똑똑한 것보다(일관성), 상황에 따라 조금 틀려도 빠르게 대답해주는 게(가용성) 더 중요할 때가 있다는 것을 배우는 이론입니다.
