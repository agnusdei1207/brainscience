+++
title = "분산 합의 알고리즘 (Paxos, Raft)"
date = 2024-05-18
description = "분산 시스템의 신뢰성을 보장하기 위한 합의 아키텍처: 난해한 Paxos와 이해하기 쉬운 Raft의 동작 원리, 상태 머신 복제(SMR) 및 고가용성 전략 심층 분석"
weight = 20
[taxonomies]
categories = ["studynotes-bigdata"]
tags = ["Consensus", "Paxos", "Raft", "Distributed System", "SMR", "Zookeeper"]
+++

# 분산 합의 알고리즘 (Paxos, Raft) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 합의(Distributed Consensus)는 네트워크 지연, 메시지 유실, 노드 장애가 빈번한 환경에서도 여러 대의 서버가 하나의 일관된 상태(State)에 도달하도록 보장하는 분산 시스템의 근간 기술입니다.
> 2. **가치**: 데이터 정합성(Consistency)과 고가용성(Availability)의 트레이드오프 관계를 해결하며, 일부 노드가 불능 상태가 되어도 과반수(Quorum) 이상의 합의만으로 시스템 전체의 연속성을 유지합니다.
> 3. **융합**: 클라우드 네이티브의 핵심인 Kubernetes(etcd), 서비스 메쉬, 분산 DB(CockroachDB, TiDB) 등 현대적 인프라의 신뢰성을 지탱하는 '디지털 근본 엔진'으로 작동하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
분산 합의 알고리즘은 분산 컴퓨팅 환경에서 여러 노드(Node)들이 특정한 값이나 상태에 대해 전원 또는 과반수가 동의하게 만드는 프로토콜입니다. 가장 원조격인 **Paxos(팍소스)**는 수학적으로 완벽하나 구현이 극도로 어려운 특징이 있으며, **Raft(래프트)**는 Paxos의 복잡성을 해결하고 '이해 가능성(Understandability)'을 최우선으로 설계되어 실제 산업계(etcd, Consul 등)에서 가장 널리 쓰이는 표준 알고리즘입니다.

### 💡 비유
- **Paxos**는 '고대 그리스 의회'와 같습니다. 복잡한 절차와 여러 명의 전령사가 오가며 투표를 진행하는데, 규칙이 너무 까다로워 의원들조차 가끔 누가 최종 결정을 내렸는지 헷갈릴 정도입니다.
- **Raft**는 '선출된 반장과 학급 회의'입니다. 학생들 중 가장 믿음직한 한 명을 반장(Leader)으로 뽑고, 모든 중요한 결정은 반장을 통해서만 전달됩니다. 반장이 갑자기 전학을 가면 다시 투표해서 새 반장을 뽑는 명확한 구조입니다.

### 등장 배경 및 발전 과정
1. **신뢰할 수 없는 네트워크**: 분산 시스템에서는 노드가 언제든 죽을 수 있고(Crash), 네트워크 패킷이 순서가 뒤바뀌거나 사라질 수 있는 환경임을 인정해야 했습니다.
2. **상태 머신 복제(SMR: State Machine Replication)**: 모든 서버가 동일한 명령을 동일한 순서로 실행하게 하여, 최종적으로 동일한 상태를 갖게 하는 복제 기술의 필요성이 대두되었습니다.
3. **FLP Impossibility 정리**: 비동기 네트워크 환경에서 단 한 개의 노드만 장애가 나도 완벽한 합의에 도달하는 것이 불가능하다는 이론적 한계를 극복하기 위해, '과반수 합의(Quorum)'라는 현실적 타협안이 제시되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. Paxos vs Raft 핵심 구성 요소 비교
| 구분 | Paxos (Roles) | Raft (States) | 핵심 역할 비유 |
| :--- | :--- | :--- | :--- |
| **제안자** | Proposer | **Leader** | 안건을 내고 결정을 주도하는 주체 |
| **수락자** | Acceptor | **Follower** | 제안된 안건에 대해 투표를 던지는 주체 |
| **학습자** | Learner | **Follower** | 최종 결정된 내용을 전달받아 실행하는 주체 |
| **상태** | 명시적 상태 변화 없음 | Follower, Candidate, Leader | 선거를 통한 명확한 권력 구조 |

### 2. Raft 합의 프로세스 데이터 플로우 (ASCII Diagram)
```text
[ Raft Leader Election & Log Replication ]

  (1) Election Term (임기) 시작
      Client  ---(Request: Set X=1)---> [ Leader ]
                                          |
  (2) Log Replication (로그 복제)          | (AppendEntries RPC)
          +-------------------------------+---------------+
          |                               |               |
    v-----v-----v                   v-----v-----v   v-----v-----v
    | Follower A|                   | Follower B|   | Follower C| (장애 노드)
    +-----------+                   +-----------+   +-----------+
          | (ACK: Log Saved)              | (ACK: Log Saved)
          +---------------+---------------+
                          |
  (3) Commit (결정 확정)   | (Majority Reached!)
      [ Leader ] --- (Commit Index Update) ---> [ All Followers ]
                                          |
      Client <---(Success Response)-------+
```

### 3. 심층 동작 원리

#### (1) Paxos의 2-Phase Commit 연계 동작
- **Phase 1 (Prepare/Promise)**: 제안자가 고유한 번호($n$)를 생성하여 수락자들에게 보냅니다. 수락자들은 자신이 받은 번호보다 큰 경우에만 약속(Promise)을 합니다.
- **Phase 2 (Accept/Accepted)**: 과반수의 약속을 받으면 제안자는 실제 값($v$)을 보냅니다. 수락자들은 이미 더 큰 번호의 제안을 약속하지 않았다면 이를 수락합니다.
- **한계**: 여러 제안자가 동시에 경쟁하면 무한 루프(Livelock)에 빠질 수 있는 'Duel' 현상이 발생하기 쉽습니다.

#### (2) Raft의 3대 핵심 서브 문제 해결
- **Leader Election (리더 선출)**: 리더가 일정 시간(Heartbeat) 동안 신호를 주지 않으면 Follower는 Candidate로 전환하고 투표를 요청합니다. **Randomized Timeout** 기법을 써서 투표가 갈리는 상황을 방지합니다.
- **Log Replication (로그 복제)**: 리더는 모든 요청을 로그에 쓰고 Follower들에게 복제합니다. 과반수가 로그를 저장했다는 응답을 주면 그제야 'Commit' 하고 상태 머신에 반영합니다.
- **Safety (안전성)**: 투표 시 자신보다 최신 로그를 가진 후보에게만 투표함으로써, 오직 정당한 데이터를 가진 노드만 리더가 될 수 있게 보장합니다.

### 4. 실무 구현 예시 (etcd/Raft 라이브러리 인터페이스 구조)
```go
// Raft 노드의 핵심 상태 전이 및 메시지 처리 인터페이스 (Go-like pseudocode)
type Node interface {
    // 클라이언트로부터 새로운 명령(Propose)을 받았을 때
    Propose(ctx context.Context, data []byte) error
    
    // 리더 선출을 위한 투표 요청 (Step)
    Step(ctx context.Context, msg pb.Message) error
    
    // 합의된 로그(Ready)를 가져와서 로컬 상태 머신에 반영
    Ready() <-chan Ready
    
    // 주기적 시간 흐름 알림 (Timeout 체크용)
    Tick()
}

// Ready 구조체: 합의가 완료되어 실제 DB에 써야 할 데이터 묶음
type Ready struct {
    Entries          []pb.Entry   // 로그에 기록할 내용
    CommittedEntries []pb.Entry   // 이미 합의되어 실행(Apply)할 내용
    Messages         []pb.Message // 타 노드에 전송할 네트워크 메시지
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 1. Paxos vs Raft 기술 심층 비교 매트릭스
| 비교 지표 | Paxos | Raft |
| :--- | :--- | :--- |
| **이해 용이성** | 매우 낮음 (수학적 증명 위주) | 높음 (현실적 설계) |
| **구현 난이도** | 매우 높음 (오픈소스마다 해석 다름) | 보통 (표준 라이브러리 다수 존재) |
| **성능 (Throughput)** | 리더가 고정되지 않으면 낮음 | 리더 집중형으로 안정적임 |
| **상태 관리** | 로그 기반이 아님 (Single value) | **Log-based (Sequence of values)** |
| **실제 사용 사례** | Google Spanner, Zookeeper(ZAB) | **Kubernetes(etcd)**, CockroachDB, InfluxDB |

### 2. 과목 융합 관점 분석 (Network + Database + Security)
- **Network**: **CAP 이론** 중 C(일관성)와 P(가용성/분할 내성)를 선택하고 A(가용성)를 일부 희생하는 모델입니다. 네트워크 단절(Partition) 시 과반수를 확보하지 못한 그룹은 서비스를 중단하여 데이터 오염을 막습니다.
- **Database**: **상태 머신 복제(SMR)** 아키텍처를 통해 분산 데이터베이스의 트랜잭션 원자성(Atomicity)을 보장합니다.
- **Security**: 리더 선출 과정에서 악의적인 노드가 권력을 찬탈하지 못하도록 **MTLS(Mutual TLS)**를 통한 노드 간 상호 인증이 필수적으로 결합됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)
**시나리오: 3개의 데이터 센터(DC)에 분산된 etcd 클러스터 운영**
- **문제점**: DC 한 곳이 통째로 마비되거나 네트워크가 끊겼을 때, 리더 선출이 무한 반복되거나 서비스가 불능 상태가 됨.
- **전략적 솔루션**: 
  1. **Quorum 설계**: 노드 수를 3, 5, 7개와 같이 홀수로 배치하여 명확한 과반수 기준 수립.
  2. **Learner 노드 활용**: 데이터 복제본은 유지하되 투표권은 없는 Learner 노드를 추가하여, 리더 선출 성능에 영향을 주지 않으면서 읽기 성능 확장.
  3. **Pre-Vote 단계 도입**: 실제 Candidate가 되기 전, 과반수의 지지를 얻을 수 있는지 미리 찔러보는 Pre-vote 단계를 활성화하여 불필요한 임기(Term) 증가 방지.

### 도입 시 고려사항 (체크리스트)
1. **디스크 I/O 성능**: Raft는 모든 로그를 디스크에 강제 동기화(fsync)하므로, SSD급 이상의 저장장치와 낮은 디스크 지연 시간이 필수적입니다.
2. **네트워크 지연 시간(RTT)**: 리더 선출의 타임아웃 시간은 네트워크 왕복 시간(RTT)보다 충분히 커야 하며, 그렇지 않으면 끊임없는 재선거가 발생합니다.
3. **스냅샷 전략**: 로그가 무한히 쌓이면 재부팅 시 복구 시간이 너무 길어집니다. 주기적으로 현재 상태를 저장하고 이전 로그를 지우는 **Snapshotting** 메커니즘이 구현되어 있는가?

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대효과
1. **정량적**: 서버 5대 구성 시 최대 2대 장애가 발생해도 서비스 무중단 유지(Availability **99.999%** 도전).
2. **정성적**: 휴먼 에러나 하드웨어 장애 상황에서도 데이터 손실 없이 완벽한 정합성 보장, 시스템 관리의 자동화 수준 향상.

### 미래 전망 및 진화 방향
- **Byzantine Fault Tolerance (BFT)**: Raft는 노드가 거짓말을 하지 않는다는 가정을 하지만, 블록체인 환경에서는 악의적 노드의 공격까지 막는 BFT 기반 합의(Tendermint 등)로 진화하고 있습니다.
- **RDMA 기반 최적화**: 네트워크 레이턴시를 극단적으로 줄이기 위해 커널을 거치지 않는 RDMA 기술을 합의 프로토콜에 이식하여 수백만 TPS를 달성하려는 시도가 이어지고 있습니다.

### ※ 참고 표준/가이드
- **In Search of an Understandable Consensus Algorithm**: Diego Ongaro & John Ousterhout (Raft 원저 논문)
- **The Part-Time Parliament**: Leslie Lamport (Paxos 원저 논문)
- **NIST IR 8202**: Blockchain Technology Overview (합의 알고리즘 표준 분류)

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [CAP Theorem](@/studynotes/16_bigdata/_index.md): 분산 시스템의 한계를 규정한 이론
- [Quorum](@/studynotes/16_bigdata/02_distributed/_index.md): 합의를 위해 필요한 최소 노드 수의 원리
- [etcd (Kubernetes Storage)](@/studynotes/13_cloud_architecture/01_native/kubernetes.md): Raft를 실제로 구현한 대표적 키-값 저장소
- [Saga Pattern](@/studynotes/04_software_engineering/01_sdlc/msa.md): 합의 알고리즘 없이 긴 트랜잭션을 처리하는 보상 중심 패턴
- [Zookeeper (ZAB Protocol)](@/studynotes/16_bigdata/_index.md): Paxos 계열의 ZAB 프로토콜을 사용하는 코디네이션 서비스

---

## 👶 어린이를 위한 3줄 비유 설명
1. **분산 합의**는 여러 친구가 똑같은 공책을 하나씩 가지고 있을 때, 모두의 공책에 똑같은 순서로 똑같은 숙제를 적는 약속이에요.
2. **Raft**는 그중에서 가장 성실한 친구를 '반장'으로 뽑아서, 반장이 시키는 순서대로만 숙제를 적기로 약속해서 헷갈리지 않게 하는 방법이랍니다.
3. 이렇게 하면 한두 명의 친구가 아파서 학교에 못 와도, 나머지 친구들이 똑같은 숙제를 계속할 수 있어서 공부가 멈추지 않아요!
