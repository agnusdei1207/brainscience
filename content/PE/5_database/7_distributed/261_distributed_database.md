+++
title = "분산 데이터베이스 (Distributed Database)"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
+++

# 분산 데이터베이스 (Distributed Database)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산 데이터베이스는 물리적으로 분산된 여러 노드에 데이터를 저장하면서도, 논리적으로는 단일 시스템처럼 투명하게 접근할 수 있게 하는 데이터베이스 아키텍처입니다.
> 2. **가치**: 지리적 분산으로 재해 복구 능력을 강화하고, 수평 확장(Scale-out)으로 페타바이트급 데이터 처리가 가능하며, 지역별 최적화로 글로벌 서비스의 응답 속도를 개선합니다.
> 3. **융합**: 위치 투명성, 분할 투명성, 복제 투명성, 장애 투명성 등 6대 투명성을 통해 네트워크, 합의 알고리즘(Paxos, Raft), CAP 정리와 결합하여 고가용성 데이터 인프라를 구축합니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**분산 데이터베이스(Distributed Database, DDB)**는 논리적으로는 하나의 통합된 데이터베이스처럼 보이지만, 물리적으로는 통신 네트워크로 연결된 여러 컴퓨터 노드에 데이터가 분산 저장되는 데이터베이스 시스템입니다. 사용자는 데이터가 어디에 저장되어 있는지 알 필요 없이, 마치 단일 시스템에 접근하듯 투명하게 데이터를 조작할 수 있습니다.

**핵심 구성 요소**:
- **노드(Node)**: 독립적인 데이터베이스 서버 (CPU, 메모리, 디스크 보유)
- **네트워크(Network)**: 노드 간 통신 인프라
- **분산 DBMS (DDBMS)**: 분산 환경을 관리하는 미들웨어
- **글로벌 스키마(Global Schema)**: 전체 분산 DB의 논리적 구조
- **로컬 스키마(Local Schema)**: 각 노드의 물리적 저장 구조

**분산 데이터베이스의 목표**:
1. **투명성(Transparency)**: 사용자가 분산을 인식하지 않음
2. **신뢰성(Reliability)**: 일부 노드 장애 시에도 서비스 지속
3. **가용성(Availability)**: 24x7 서비스 보장
4. **확장성(Scalability)**: 노드 추가로 성능 선형 증가
5. **자율성(Autonomy)**: 각 노드의 독립적 운영

#### 2. 비유를 통한 이해
분산 데이터베이스는 **'체인점을 가진 프랜차이즈'**와 같습니다.

- **중앙 본사(글로벌 스키마)**: 모든 매장의 통합 관점
- **각 지점(노드)**: 독립적으로 운영되는 로컬 매장
- **통신망(네트워크)**: 본사와 지점, 지점 간 연결
- **투명성**: 고객은 어떤 지점에서 주문하든 동일한 메뉴와 서비스 경험
- **장애 허용**: 한 지점이 문을 닫아도 다른 지점에서 서비스

**투명성의 비유**:
- **위치 투명성**: 어느 지점에 재고가 있는지 모르고 주문
- **복제 투명성**: 같은 상품이 여러 지점에 있어도 모름
- **분할 투명성**: 상품이 지역별로 분배되어 있어도 통합 카탈로그로 조회

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 중앙 집중형 데이터베이스는 단일 장애점(SPOF, Single Point of Failure) 문제, 지리적 거리로 인한 응답 지연, 그리고 수직 확장의 물리적/경제적 한계에 직면했습니다.

2. **혁신적 패러다임의 도입**:
   - 1970년대: 분산 데이터베이스 개념 연구 시작
   - 1980년대: Oracle, Sybase 등 초기 분산 DB 제품
   - 2000년대: 구글 Bigtable, 아마존 Dynamo, Yahoo PNUTS
   - 2010년대: NewSQL (Spanner, CockroachDB, TiDB)
   - 2020년대: 클라우드 네이티브 분산 DB (Aurora, Spanner Cloud)

3. **비즈니스적 요구사항**: 글로벌 기업은 전 세계 사용자에게 100ms 이내 응답을 제공해야 합니다. 또한 자연재해, 정전, 네트워크 장애 등에도 서비스 중단 없이 운영해야 합니다. 분산 DB는 이러한 요구사항을 충족하는 핵심 인프라입니다.

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 분산 데이터베이스 6대 투명성 (표)

| 투명성 | 상세 내용 | 구현 기술 | 비유 |
|:---|:---|:---|:---|
| **위치 투명성** (Location) | 데이터의 물리적 위치 은닉 | 네임 서버, 디렉터리 | 어느 지점인지 모름 |
| **분할 투명성** (Fragmentation) | 데이터 분할 여부 은닉 | 분할 스키마, 글로벌 뷰 | 통합 카탈로그 |
| **복제 투명성** (Replication) | 데이터 복제 여부 은닉 | 복제 관리자, 동기화 | 재고 동기화 |
| **병행 투명성** (Concurrency) | 동시 접근 제어 은닉 | 분산 락, MVCC | 대기열 관리 |
| **장애 투명성** (Failure) | 노드 장애 은닉 | 페일오버, 복제 | 대체 지점 운영 |
| **지역 사상 투명성** (Local Mapping) | 이기종 DB 통합 은닉 | 게이트웨이, 변환기 | 통화 변환 |

#### 2. 분산 데이터베이스 아키텍처 다이어그램

```text
================================================================================
                  [ Distributed Database Architecture ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                          [ Global Users ]                                    │
│                                                                              │
│  User A (Seoul)         User B (New York)        User C (London)           │
│       │                      │                        │                      │
└───────┼──────────────────────┼────────────────────────┼──────────────────────┘
        │                      │                        │
        ▼                      ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       [ Distributed DBMS Layer ]                             │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    [ Global Schema Manager ]                            │ │
│  │  - 전체 데이터베이스의 논리적 구조 정의                                │ │
│  │  - 분할 및 복제 정책 관리                                              │ │
│  │  - 글로벌 질의 최적화 (Global Query Optimization)                      │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    [ Distributed Transaction Manager ]                  │ │
│  │                                                                         │ │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │ │
│  │  │ 2-Phase Commit   │  │ Distributed Lock │  │ Recovery Manager │     │ │
│  │  │ (Coordinator)    │  │ Manager          │  │ (Log Replication)│     │ │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    [ Replication & Fragmentation ]                      │ │
│  │                                                                         │ │
│  │  Fragmentation: Horizontal (행 분할), Vertical (열 분할)               │ │
│  │  Replication: Synchronous (동기), Asynchronous (비동기)                │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
        │                      │                        │
        │ Network              │ Network                │ Network
        ▼                      ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Distributed Nodes ]                                │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                          [ Site 1: Asia ]                               │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Local DBMS (Node 1)                                              │  │ │
│  │  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐     │  │ │
│  │  │  │ Customer DB    │  │ Order DB       │  │ Product DB     │     │  │ │
│  │  │  │ (Asia region)  │  │ (Asia orders)  │  │ (Replica)      │     │  │ │
│  │  │  └────────────────┘  └────────────────┘  └────────────────┘     │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        [ Site 2: Americas ]                             │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Local DBMS (Node 2)                                              │  │ │
│  │  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐     │  │ │
│  │  │  │ Customer DB    │  │ Order DB       │  │ Product DB     │     │  │ │
│  │  │  │ (Americas)     │  │ (Americas)     │  │ (Primary)      │     │  │ │
│  │  │  └────────────────┘  └────────────────┘  └────────────────┘     │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         [ Site 3: Europe ]                              │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Local DBMS (Node 3)                                              │  │ │
│  │  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐     │  │ │
│  │  │  │ Customer DB    │  │ Order DB       │  │ Product DB     │     │  │ │
│  │  │  │ (Europe)       │  │ (Europe)       │  │ (Replica)      │     │  │ │
│  │  │  └────────────────┘  └────────────────┘  └────────────────┘     │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
                    [ Data Fragmentation Strategy ]
================================================================================

    [ Horizontal Fragmentation (수평 분할) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Customer Table:                                                        │
    │                                                                         │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │ Site 1 (Asia):  SELECT * FROM customer WHERE region = 'Asia'    │   │
    │  │ Site 2 (Americas): SELECT * FROM customer WHERE region = 'US'   │   │
    │  │ Site 3 (Europe): SELECT * FROM customer WHERE region = 'EU'     │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    │  장점: 지역별 데이터 접근 최적화, 병렬 처리 가능                       │
    └─────────────────────────────────────────────────────────────────────────┘

    [ Vertical Fragmentation (수직 분할) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Customer Table → 분할:                                                 │
    │                                                                         │
    │  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐   │
    │  │ Fragment 1        │  │ Fragment 2        │  │ Fragment 3        │   │
    │  │ (기본 정보)       │  │ (연락처)          │  │ (마케팅)          │   │
    │  │ - customer_id (PK)│  │ - customer_id (PK)│  │ - customer_id (PK)│   │
    │  │ - name            │  │ - email           │  │ - preferences     │   │
    │  │ - birth_date      │  │ - phone           │  │ - last_contact    │   │
    │  └───────────────────┘  └───────────────────┘  └───────────────────┘   │
    │                                                                         │
    │  장점: 컬럼별 보안 적용, 자주 사용하는 컬럼만 분리                      │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
                     [ Replication Strategy ]
================================================================================

    [ Synchronous Replication (동기 복제) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │  Client ──WRITE──> Primary ──SYNC──> Replica 1 ──SYNC──> Replica 2    │
    │                           │              │                │             │
    │                           │              │                │             │
    │                           ▼              ▼                ▼             │
    │                        [WAIT]         [WAIT]           [WAIT]          │
    │                           │              │                │             │
    │                           └──────────────┴────────────────┘             │
    │                                          │                              │
    │                                          ▼                              │
    │                                       [ACK]                             │
    │                                          │                              │
    │                                          ▼                              │
    │  Client <─────────────────────────── [COMMIT]                           │
    │                                                                         │
    │  장점: 강한 일관성  단점: 높은 지연, 가용성 저하                        │
    └─────────────────────────────────────────────────────────────────────────┘

    [ Asynchronous Replication (비동기 복제) ]
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │  Client ──WRITE──> Primary ──ASYNC──> Replica 1 ──ASYNC──> Replica 2  │
    │                           │                                             │
    │                           ▼                                             │
    │  Client <───────────── [COMMIT]  (Replica 기다리지 않음)               │
    │                                                                         │
    │  장점: 낮은 지연, 높은 가용성  단점: 일시적 불일치 가능                 │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
```

#### 3. 심층 동작 원리: 분산 트랜잭션 프로토콜

**① 2단계 커밋 (2-Phase Commit, 2PC)**

```text
[ 2-Phase Commit Protocol ]

Phase 1: PREPARE
┌─────────────────────────────────────────────────────────────────────────────┐
│  Coordinator                      Participant 1        Participant 2       │
│       │                                │                     │              │
│       │──PREPARE──────────────────────>│                     │              │
│       │─────────────────────────────────PREPARE─────────────>│              │
│       │                                │                     │              │
│       │                                │──READY/VOTE_YES────>│              │
│       │<──READY/VOTE_YES───────────────│                     │              │
│       │                                │                     │              │
│       │<───────────────────────────────READY/VOTE_YES────────│              │
│       │                                │                     │              │
│  [ All Participants Ready? ]           │                     │              │
│       │                                │                     │              │
└───────┼────────────────────────────────┼─────────────────────┼──────────────┘
        │                                │                     │
        │                                │                     │
Phase 2: COMMIT                          │                     │
┌───────┼────────────────────────────────┼─────────────────────┼──────────────┐
│       │                                │                     │              │
│       │──COMMIT────────────────────────>│                     │              │
│       │─────────────────────────────────COMMIT───────────────>│              │
│       │                                │                     │              │
│       │                                │──ACK───────────────>│              │
│       │<──ACK──────────────────────────│                     │              │
│       │<───────────────────────────────ACK───────────────────│              │
│       │                                │                     │              │
│  [ Transaction Committed ]             │                     │              │
│       │                                │                     │              │
└───────┴────────────────────────────────┴─────────────────────┘

[ Blocking Problem ]
- Coordinator 장애 시 Participant가 무한 대기 상태에 빠짐
- 해결책: 3-Phase Commit, Timeout, Paxos/Raft
```

**② 3단계 커밋 (3-Phase Commit, 3PC)**

```text
[ 3-Phase Commit Protocol ]

Phase 1: CAN-COMMIT (타임아웃 가능)
Phase 2: PRE-COMMIT (새로운 단계)
Phase 3: DO-COMMIT

특징:
- Non-blocking: 어느 단계에서든 타임아웃으로 종료 가능
- Coordinator 장애 시에도 참여자가 합의하여 진행/중단 결정

단점:
- 네트워크 지연 증가
- 구현 복잡도 증가
```

**③ Paxos 알고리즘 (합의 프로토콜)**

```text
[ Paxos Algorithm ]

역할:
- Proposer: 값을 제안하는 노드
- Acceptor: 제안을 승인/거부하는 노드
- Learner: 합의된 값을 학습하는 노드

Phase 1: Prepare
1. Proposer가 n(제안 번호)을 선택하여 Prepare(n) 전송
2. Acceptor는 n이 자신이 본 가장 큰 번호면 Promise(n) 응답

Phase 2: Accept
1. Proposer가 Accept(n, value) 전송
2. 과반수 Acceptor가 승인하면 합의 완료

특징:
- 비잔틴 장애 허용 안 함 (Crash-failure만 허용)
- 과반수(Quorum) 합의
- 메시지 지연이 많음
```

**④ Raft 알고리즘 (Paxos 단순화)**

```text
[ Raft Algorithm ]

역할:
- Leader: 모든 요청 처리, 로그 복제
- Follower: Leader의 로그 수신 및 적용
- Candidate: 리더 선출 시 후보

리더 선출 (Leader Election):
1. Follower가 타임아웃 → Candidate로 전환
2. 랜덤 타임아웃 후 RequestVote 전송
3. 과반수 투표 획득 시 Leader 됨

로그 복제 (Log Replication):
1. Client 요청 → Leader가 로그에 추가
2. AppendEntries RPC로 Followers에 복제
3. 과반수 확인(Commit) 후 클라이언트에 응답

특징:
- 이해하기 쉬운 설계
- Leader-based (단순화)
- MongoDB, CockroachDB, etcd에서 사용
```

#### 4. 실무 수준의 분산 DB 설계 예시

```sql
-- ==============================================================================
-- 분산 데이터베이스 설계: 글로벌 전자상거래 시스템
-- ==============================================================================

-- [1] 글로벌 스키마 정의 (논리적 통합 뷰)
-- Global Schema: 모든 지역에서 동일한 논리 구조

CREATE TABLE customers (
    customer_id   BIGINT PRIMARY KEY,
    name          VARCHAR(100),
    email         VARCHAR(255),
    region        VARCHAR(20),  -- 'APAC', 'AMERICAS', 'EMEA'
    created_at    TIMESTAMP
);

CREATE TABLE orders (
    order_id      BIGINT PRIMARY KEY,
    customer_id   BIGINT REFERENCES customers(customer_id),
    order_date    TIMESTAMP,
    total_amount  DECIMAL(10,2),
    region        VARCHAR(20)
);

CREATE TABLE products (
    product_id    BIGINT PRIMARY KEY,
    name          VARCHAR(200),
    price         DECIMAL(10,2),
    stock         INT
);

-- [2] 수평 분할 (Horizontal Fragmentation)
-- 지역별로 고객/주문 데이터 분산

-- Site 1: Asia-Pacific (APAC)
-- Fragment: customers_apac = σ_region='APAC'(customers)
CREATE TABLE customers_apac (
    -- customers와 동일한 구조
    -- CHECK 제약으로 region = 'APAC'만 허용
    CHECK (region = 'APAC')
);

-- Site 2: Americas
-- Fragment: customers_americas = σ_region='AMERICAS'(customers)
CREATE TABLE customers_americas (
    CHECK (region = 'AMERICAS')
);

-- Site 3: Europe, Middle East, Africa (EMEA)
-- Fragment: customers_emea = σ_region='EMEA'(customers)
CREATE TABLE customers_emea (
    CHECK (region = 'EMEA')
);

-- [3] 복제 전략 (Replication Strategy)

-- 완전 복제 (Full Replication): products 테이블
-- 모든 사이트에 복제 (읽기 많은 마스터 데이터)
-- Site 1, 2, 3 모두 products 테이블 보유

-- 부분 복제 (Partial Replication): 고객 요약
-- 자주 조회되는 요약 정보만 복제
CREATE TABLE customer_summary_replica AS
SELECT customer_id, name, email, region
FROM customers;

-- [4] 분산 질의 (Distributed Query)

-- 로컬 질의 (Local Query): 단일 사이트
-- Site 1에서 아시아 고객 조회
SELECT * FROM customers_apac WHERE customer_id = 1001;

-- 원격 질의 (Remote Query): 원격 사이트
-- Site 1에서 Site 2의 미국 고객 조회
SELECT * FROM customers@site2_americas WHERE customer_id = 2001;

-- 글로벌 질의 (Global Query): 전체 사이트 통합
-- 전체 고객 수 조회 (병렬 수행)
SELECT COUNT(*) FROM customers;  -- 각 사이트에서 병렬 수행 후 결과 집계

-- 분산 조인 (Distributed Join)
-- 아시아 고객의 주문 조회 (customers@site1 JOIN orders@site1)
SELECT c.name, o.order_id, o.total_amount
FROM customers_apac c
JOIN orders_apac o ON c.customer_id = o.customer_id;

-- [5] 분산 트랜잭션

-- 글로벌 트랜잭션: 여러 사이트에 걸친 원자적 연산
BEGIN DISTRIBUTED TRANSACTION;

-- Site 1: 아시아 창고에서 재고 감소
UPDATE inventory@site1_apac
SET stock = stock - 1
WHERE product_id = 100;

-- Site 2: 미국 창고에 주문 생성
INSERT INTO orders@site2_americas (order_id, customer_id, product_id, quantity)
VALUES (10001, 2001, 100, 1);

-- Site 3: 유럽 배송 정보 생성 (직배송)
INSERT INTO shipments@site3_emea (shipment_id, order_id, destination)
VALUES (50001, 10001, 'Paris, France');

-- 2-Phase Commit으로 원자성 보장
COMMIT;  -- 모든 사이트가 준비되면 커밋

-- [6] CAP 정리 기반 일관성 레벨 선택 (Cassandra 스타일)

-- 강한 일관성 (Strong Consistency): W + R > N
-- W=2, R=2, N=3 → 최신 데이터 보장
CONSISTENCY QUORUM;  -- 과반수 읽기/쓰기

-- 최종 일관성 (Eventual Consistency): 낮은 지연
-- W=1, R=1, N=3 → 빠른 응답, 일시적 불일치 허용
CONSISTENCY ONE;

-- [7] CockroachDB 스타일 분산 SQL

-- 자동 분산 및 복제
CREATE TABLE orders (
    order_id INT PRIMARY KEY,  -- 자동으로 범위 분할
    customer_id INT,
    total DECIMAL(10,2)
) PARTITION BY RANGE (order_id);

-- 존 기반 배치 (Zone-based placement)
ALTER TABLE orders PARTITION BY RANGE (order_id) (
    PARTITION asia VALUES FROM (1) TO (1000000),
    PARTITION americas VALUES FROM (1000001) TO (2000000),
    PARTITION emea VALUES FROM (2000001) TO (MAXVALUE)
);

-- 배치 제약 (각 파티션을 특정 지역에 저장)
ALTER PARTITION asia OF TABLE orders CONFIGURE ZONE USING
    constraints = '[+region=asia]';

-- Online Schema Change (중단 없는 스키마 변경)
ALTER TABLE orders ADD COLUMN shipping_address VARCHAR(500);
```

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 분산 DB 아키텍처 유형 비교

| 아키텍처 | 특징 | 장점 | 단점 | 대표 사례 |
|:---|:---|:---|:---|:---|
| **Shared-Disk** | 디스크 공유, 노드 독립 | 쉬운 마이그레이션 | 디스크 병목 | Oracle RAC |
| **Shared-Nothing** | 완전 독립, 네트워크만 공유 | 수평 확장 용이 | 복잡한 조인 | Cassandra, MongoDB |
| **Shared-Memory** | 메모리 공유 | 초고속 통신 | 확장성 한계 | 단일 서버 |
| **Hybrid** | 계층적 조합 | 유연성 | 복잡도 | Aurora |

#### 2. 합의 알고리즘 비교

| 알고리즘 | 메시지 복잡도 | 용도 | 장애 허용 | 사용 사례 |
|:---|:---|:---|:---|:---|
| **2PC** | O(N) | 분산 트랜잭션 | Coordinator 장애 시 블로킹 | 전통적 DDBMS |
| **Paxos** | O(N²) | 합의 | F < N/2 | Chubby, Spanner |
| **Raft** | O(N) | 리더 선출+복제 | F < N/2 | etcd, CockroachDB |
| **PBFT** | O(N²) | 비잔틴 장애 허용 | F < N/3 | 블록체인 |

#### 3. 과목 융합 관점 분석

- **[네트워크 융합] 지연과 대역폭**: 분산 DB는 네트워크 지연(Latency)에 민감합니다. 리전 간 통신은 수십~수백 ms 지연이 발생하므로, 데이터 지역성(Locality) 확보와 비동기 복제가 중요합니다.

- **[알고리즘 융합] 합의 프로토콜**: Paxos, Raft는 분산 시스템의 핵심 알고리즘입니다. FLP Impossibility에 따라 비동기 시스템에서 완벽한 합의는 불가능하므로, 타임아웃과 리더 선출로 우회합니다.

- **[보안 융합] 데이터 일관성과 무결성**: 분산 환경에서는 네트워크 분할 시 일관성과 가용성의 트레이드오프가 발생합니다. CAP 정리에 따른 적절한 선택이 필요합니다.

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

- **시나리오 1: 글로벌 서비스의 데이터 배치 전략**
  - 상황: 미국, 유럽, 아시아에 사용자 분포. 각 지역 응답 시간 100ms 이내 요구.
  - 판단: 사용자 데이터는 지역별 수평 분할(Horizontal Fragmentation). 마스터 데이터(상품, 카테고리)는 전체 복제(Full Replication). 쓰기는 Primary Region, 읽기는 Local Region에서 수행.

- **시나리오 2: 재해 복구(Disaster Recovery) 설계**
  - 상황: 단일 리전 장애 시에도 서비스 지속 필요. RPO 0, RTO 1분 요구.
  - 판단: 멀티 리전 동기 복제(Synchronous Replication). 자동 페일오버 구성. Route 53 또는 Global Load Balancer로 트래픽 자동 전환.

- **시나리오 3: 분산 트랜잭션 성능 저하**
  - 상황: 2PC로 인한 트랜잭션 지연 증가.
  - 판단: Saga 패턴으로 전환 (보상 트랜잭션). 또는 최종 일관성(Eventual Consistency) 수용. TCC(Try-Confirm-Cancel) 패턴도 검토.

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **데이터 지역성**: 사용자 위치 기반 데이터 배치
- [ ] **복제 전략**: 동기 vs 비동기, 전체 vs 부분
- [ ] **분할 키 설계**: 핫스팟 방지, 질의 패턴 고려
- [ ] **합의 알고리즘**: Raft, Paxos, 2PC 선택
- [ ] **모니터링**: 분산 추적(Distributed Tracing), 메트릭

#### 3. 안티패턴 (Anti-patterns)

- **과도한 분산**: 불필요한 분산은 복잡도만 증가
- **잘못된 분할 키**: 핫스팟으로 확장성 저하
- **동기 복제 남용**: 지역 간 동기 복제는 높은 지연
- **분산 조인 과다**: 네트워크 오버헤드 증가

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 효과 영역 | 내용 | 개선 지표 |
|:---|:---|:---|
| **가용성** | 멀티 리전 복제 | 99.999% 가용성 |
| **성능** | 지역별 데이터 배치 | 응답 시간 80% 단축 |
| **확장성** | 수평 확장 | 선형 성능 증가 |
| **재해 복구** | 자동 페일오버 | RTO < 1분 |

#### 2. 미래 전망

분산 데이터베이스는 **Serverless, Edge Computing, AI**로 진화합니다:

1. **Serverless 분산 DB**: 사용량 기반 과금, 자동 스케일링 (Aurora Serverless, Spanner)
2. **Edge Database**: 엣지 노드에서 실시간 처리 (SQLite, EdgeDB)
3. **AI 기반 최적화**: 쿼리 라우팅, 데이터 배치 자동화
4. **Quantum-Safe**: 양자 내성 암호 적용 분산 DB

#### 3. 참고 표준

- **CAP Theorem (Eric Brewer, 2000)**: 분산 시스템 트레이드오프
- **Paxos (Leslie Lamport, 1998)**: 합의 알고리즘
- **Raft (Diego Ongaro, 2014)**: 이해하기 쉬운 합의 알고리즘

---

### 관련 개념 맵 (Knowledge Graph)

- **[CAP 정리](@/studynotes/5_database/2_concurrency/distributed_database_theory.md)**: 분산 시스템의 근본적 트레이드오프.
- **[2PC](@/studynotes/5_database/2_concurrency/distributed_database_theory.md)**: 분산 트랜잭션 프로토콜.
- **[NoSQL](@/studynotes/5_database/6_nosql/274_nosql_overview.md)**: 분산 아키텍처 기반 데이터베이스.
- **[트랜잭션](@/studynotes/5_database/4_transaction/191_transaction.md)**: 분산 환경에서의 ACID 보장.
- **[샤딩](@/studynotes/5_database/_keyword_list.md)**: 데이터 분할 기법.

---

### 어린이를 위한 3줄 비유 설명

1. **체인점**: 분산 데이터베이스는 전 세계에 있는 프랜차이즈 체인점과 같아요.
2. **통합 주문**: 고객은 어느 지점에서 주문하든 같은 메뉴를 받을 수 있어요.
3. **하나가 아파도**: 한 지점이 문을 닫아도 다른 지점에서 서비스해요!
