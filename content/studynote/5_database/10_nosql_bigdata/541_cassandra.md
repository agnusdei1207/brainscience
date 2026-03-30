+++
weight = 541
title = "Apache Cassandra"
description = "고성능 분산 NoSQL 데이터베이스 Cassandra의 특징과 아키텍처에 대해 설명"
date = 2024-01-01

[extra]
categories = ["studynote-software-engineering"]
+++
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Cassandra는 Amazon Dynamo의 분산 설계를 기반으로 한 列指向 (Column-Oriented) NoSQL로, 대규모 쓰기 처리에 최적화된 리더 없는(Leaderless) 아키텍처를 가진다.
> 2. **가치**: 단일障害점(Single Point of Failure)가 없으며,线性 확장(Linear Scalability)과 constant-time 지연(latency)을 제공한다.
> 3. **융합**: Cassandra는 CAP 이론에서 AP(가용성 + 분단 내성)를 선택하며,.Eventual Consistency를 기본으로 제공한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념
Cassandra는 Facebook(현재 Meta)에서 개발하고 Apache Software Foundation에 기증한 분산 NoSQL 데이터베이스다. Google's BigTable의 데이터 모델과 Amazon Dynamo의 분산 설계를 결합한 것으로, 열 중심(Column-Family) 데이터 모델을 사용한다.

### 필요성
엄청난规模的 쓰기 workload(소셜 미디어 메시지, IoT 센서 데이터, 로그 수집 등)를 처리하면서도 가용성을 절대적으로 보장해야 하는 환경에서, 전통적인 RDBMS나 단일 리더 복제는 충분하지 않았다.

### 비유
Cassandra는分散型 달력システムと 같다. 모든 참여자(노드)가 동시에 달력을 更新(쓰기)하고, 어느 참여자가 없어도(가용성) 달력을 볼 수(읽기) 있다.

### 섹션 요약 비유
Cassandra는 다중 지도 제작과 같다. 여러 제작자(노드)가 동시에 다른 지역의 지도를 그리고, 연락이 두절(파티션)되어도 각자 가진 지역의 최신 지도는 활용할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Cassandra 아키텍처

```text
  ┌───────────────────────────────────────────────────────────────────────┐
  │                    Cassandra 아키텍처                                    │
  ├───────────────────────────────────────────────────────────────────────┤
  │
  │   [Ring 구조]                                                         │
  │
  │           Node1  ──▶  Node2  ──▶  Node3  ──▶  Node4  ──▶  Node1       │
  │              │                                      │                   │
  │              └──────────────────────────────────────┘                   │
  │                         (논리적 Ring)                                     │
  │
  │   [데이터 분산: Consistent Hashing]                                      │
  │
  │      Partition Key ──▶ Murmur3 Hash ──▶ Token Range ──▶ 노드 할당       │
  │
  │   [복제 전략]                                                         │
  │      RF=3: 각 데이터가 3개 노드에 복제됨                                 │
  │      예: N1 → N2, N2 → N3, N3 → N1 (Ring 복제)                         │
  │
  │   [쓰기 동작]                                                         │
  │   Client ──▶ [Coordinator] ──▶ [W nodes]                               │
  │                  │                                                      │
  │                  ├──▶ Node1 (로컬)                                       │
  │                  ├──▶ Node2 (복제)                                      │
  │                  └──▶ Node3 (복제)                                      │
  │              ※ W nodes确认 후 응답                                       │
  │
  └───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Cassandra는 Ring 구조로 노드가 배치되고, Murmur3 해시 함수를 사용하여 데이터를 분산한다. 각 노드는 토큰 범위를responsible로担当하며, 복제 전략(NetworkTopologyStrategy, SimpleStrategy)에 따라 다른 노드에 복제본을 저장한다. 쓰기 시에는 Coordinator 노드가 클라이언트 요청을受け、설정된 W(Write Consistency Level)만큼의 노드에 쓰기를confirmed하고 응답한다. W + R > N 공식(여기서 N은 복제係数)으로 일관성 수준을 조절한다. 예를 들어 N=3, W=2, R=2이면 W+R=4>3이므로 Strong Consistency가 보장된다.

### CQL (Cassandra Query Language)

| 명령 | 설명 |
|:---|:---|
| **CREATE KEYSPACE** | 키스페이스 생성 (RDBMS의 DATABASE 생성에 해당) |
| **CREATE TABLE** | 테이블 생성 |
| **SELECT** | 읽기 (partition key 기반) |
| **INSERT/UPDATE** | 쓰기 (upsert语义) |
| **BATCH** | 복수 문 명령 배치 |

### 섹션 요약 비유
CQL은 Cassandra의界面로, SQL과 유사하지만"partition key 없으면 전체 스캔"이라는 근본적差异가 있다. SQL은索引가 없으면 차차 찾는다면, CQL은 해당 건물을 직접 찾아가는 것과 같다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: Cassandra vs MongoDB

| 구분 | Cassandra | MongoDB |
|:---|:---|:---|
| **CAP 분류** | AP | CP |
| **데이터 모델** | 列指向 | 문서 지향 |
| **쓰기 성능** | 매우 높음 | 높음 |
| **읽기 성능** | 보통~높음 | 높음 |
| **JOIN** | 비권장 | $lookup으로 가능 |
| **트랜잭션** | 단일 파티션만 | 복수 문 지원 (4.0+) |

### W+R > N 일관성 공식

| 설정 | 일관성 수준 | 설명 |
|:---|:---|:---|
| **W=1, R=1** | Weak | 하나만 확인하면 응답 |
| **W=2, R=1** | Strong (N=3) | 충분한 확인 |
| **W=3, R=1** | Strongest | 모든 노드 확인 |
| **W=1, R=2** | Eventual | quorum 미달성 |

### 섹션 요약 비유
W+R > N 공식은宝物 발견 공식과 같다.treasure map가 3개 있는데(복제), 2개에서 발견되면(쓰기 2 + 읽기 1)宝物은 확실한 것이다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 — IoT 센서 데이터 수집**: 수백만 IoT 센서가 초당 데이터를 전송하는 환경에서 Cassandra는 엄청난 쓰기 처리량을 활용한다. 각 센서 ID가 Partition Key가 되어 데이터가 분산되고, 센서별 최신 값만 유지하는 TTL(Time-To-Live)와 결합하면 효율적인 시계열 데이터 관리 가능하다.

### 도입 체크리스트
- **기술적**: Partition Key 설계가 접근 패턴을 반영해야 한다. Partition Key 기반이 아닌 쿼리는 전체 파티션을 스캔하여 성능 저하가 심하다.
- **운영·보안적**: Multi-datacenter 복제를 통해 geographical한 disaster recovery가 가능하다.

### 안티패턴
- **파티션 키 설계 부주의**: 파티션 키가 너무 cardinalities가 낮으면(예: gender) 일부 노드에 데이터가集中한다.
- **인덱스 과다**: Secondary index를 남용하면 쿼리가 모든 파티션에 전파되어 성능이 급격히 저하된다.

### 섹션 요약 비유
Cassandra의 Partition Key 설계 실수는 우편번호를 잘못 쓴 것과 같다. 우편번호가 틀리면 편지가 잘못된 지역으로 가고, 그 지역에서는 해당 우편번호가 없어서 배달이 어렵다.

---

## Ⅴ. 기대효과 및 결론

### Cassandra strengths

| 구분 | 효과 |
|:---|:---|
| **쓰기 처리량** | 초당 수백만 쓰기 |
| **가용성** | 99.99% uptime 보장 |
| **확장성** | 노드 추가 시 linear 성능 증가 |
| **지연 시간** |常数 시간 (분산 해시테이블) |

### 미래 전망
- **Cassandra 5.0**:enas: 스토어드 프로시저 기능 강화, 검색 기능 통합
- **ScyllaDB**: Cassandra compatible하지만 C++으로 rewrite하여 더 높은 성능 제공

### 섹션 요약 비유
Cassandra의 강점은 обработка заказов в ресторане быстрого питанияと 같다. 여러 카운터(노드)에서 동시에 주문받고, 어느 카운터가 고장 나도 다른 카운터가 대응하고, 주문은 빠르게 처리된다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **CAP 이론** | Cassandra는 AP를 선택하여 가용성을 우선시한다. |
| **Consistent Hashing** | Cassandra의 데이터 분산 알고리즘으로, 노드 추가/제거 시 데이터 이동을 최소화한다. |
| **W+R > N** | Cassandra의 일관성 수준을 조절하는 공식으로, W(쓰기), R(읽기), N(복제 수)으로 결정된다. |
| **Gossip Protocol** | Cassandra 노드 간 상태 공유 프로토콜로, 중앙 관리자 없이 분산되어 동작한다. |
| **TTL** | Time-To-Live로, 데이터의有効期限을 설정하여 자동 삭제할 수 있다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. Cassandra는 **여러 명에게 동시에 같은 메모장을 복사해서 쓰는 것**과 같아서, 하나가 없어져도 다른 메모장에서 볼 수 있어요.
2. 그리고 메모장은 항상 정해진 순서대로(해시) 页が配置되어 있어서, 원하는 页을 빠르게 찾을 수 있어요.
3. 그런데頁을 찾는 방법(파티션 키)을 잘 정해야 해요.頁 번호 대신 그림으로 찾으면(파티션 키 부적절) 찾기 어려워져요!
