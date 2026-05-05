+++
weight = 218
title = "218. NoSQL BASE (Basically Available, Soft-state, Eventually Consistent) 결과적 일관성 샤딩"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: NoSQL의 BASE(Basically Available, Soft-state, Eventually Consistent) 속성은 RDBMS의 ACID(Atomicity·Consistency·Isolation·Durability)와 정반대로, 분산 환경에서 강한 일관성 대신 가용성과 성능을 택하는 설계 철학이다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

단일 서버 RDBMS는 ACID를 쉽게 보장하지만, 수십 대 서버에 걸친 분산 시스템에서 강한 일관성(Strong Consistency)을 유지하면 막대한 통신 비용과 지연이 발생한다.

```
ACID 분산 트랜잭션 문제:
  서버 A  ──── 락 획득 ────► 서버 B (응답 대기)
          ◄─── 커밋 확인 ────          │
                                      │ 네트워크 지연
                                      ▼ 50ms 지연
  → 50ms × 수백만 TPS = 시스템 마비
```

Eric Brewer는 2000년 CAP 정리로 "분산 시스템은 일관성, 가용성, 파티션 허용성 3가지를 동시에 완벽하게 지킬 수 없다"고 증명했다. NoSQL의 BASE는 이 현실을 반영한 실용적 절충이다.

---

## 2. 구성요소

| 항목 | ACID (관계형 DB) | BASE (NoSQL) |
|:---|:---|:---|
| **A** | Atomicity (원자성) | Basically Available (기본적 가용성) |
| **C** | Consistency (일관성) | Soft-state (소프트 상태) |
| **I** | Isolation (격리성) | Eventually Consistent (결과적 일관성) |
| **D** | Durability (내구성) | — |
| **우선순위** | 일관성 > 가용성 | 가용성 > 일관성 |
| **장애 시** | 트랜잭션 실패, 서비스 대기 | 서비스 계속, 나중에 일관성 회복 |

---

## 3. 구조 및 원리

**핵심 조건**: NoSQL BASE (Basically Available, Soft-state, Eventually Consistent) 결과적 일관성 샤딩은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 패턴 | 설명 | 예시 |
|:---|:---|:---|
| **Read Your Writes** | 자신이 쓴 데이터는 항상 읽을 수 있음 | 내 프로필 수정 후 즉시 반영 |
| **Monotonic Read** | 한 번 읽은 버전보다 이전 버전은 안 읽음 | 타임라인이 거꾸로 안 감 |
| **Causal Consistency** | 인과 관계 있는 이벤트는 순서 보장 | 답글은 원글 다음에 표시 |

```
데이터 구조가 고정적이고 트랜잭션이 중요한가?
  YES → RDBMS (PostgreSQL, MySQL)

데이터 구조가 동적이거나 수평 확장이 필요한가?
  YES → NoSQL

   ├── 단순 키-값 빠른 조회   → Redis / DynamoDB
   ├── JSON 도큐먼트 저장     → MongoDB
   ├── 시계열/대용량 쓰기     → Cassandra / HBase
   └── 관계 탐색              → Neo4j
```

---

## 4. 비교 및 연결

| 서비스 | 데이터 | BASE 이유 |
|:---|:---|:---|
| SNS 좋아요 수 | 수십억 건 | 1~2초 불일치 허용 가능 |
| 전자상거래 장바구니 | 사용자별 상태 | 세션 내 일관성만 필요 |
| DNS 조회 | IP 매핑 | 전파 지연 허용 |
| CDN 캐시 | 정적 파일 | TTL 기반 일관성 |

| 항목 | 문제 | 해법 |
|:---|:---|:---|
| **핫스팟** | 특정 샤드에 트래픽 집중 | 해시 샤딩 + 가상 노드(Virtual Node) |
| **교차 샤드 쿼리** | JOIN이 여러 서버 걸침 | 비정규화, 쿼리 라우터 |
| **리샤딩** | 서버 추가 시 데이터 이동 | Consistent Hashing으로 최소화 |
| **트랜잭션** | 멀티 샤드 트랜잭션 불가 | 사가(Saga) 패턴, 2PC(Two-Phase Commit) |

---

## 5. 실무 적용 및 판단

| 효과 | 내용 |
|:---|:---|
| **가용성** | 단일 노드 장애 시에도 서비스 계속 가능 |
| **확장성** | 샤드 추가만으로 처리량 선형 증가 |
| **성능** | 지역 복제로 읽기 지연 감소 |
| **비용** | 고가 단일 서버 대신 범용 서버 수평 확장 |

기술사 답안에서는 **"BASE vs ACID를 단순 대립이 아닌 비즈니스 요건에 따른 트레이드오프"**로 서술해야 한다. "언제 BASE가 적합한가"를 결과적 일관성이 허용되는 도메인(SNS, 캐시, DNS)과 허용되지 않는 도메인(금융, 재고)을 구분해 논술하고, 해시 샤딩과 일관 해시의 차이를 ASCII로 표현하면 차별화된다.

**Basically Available (기본적 가용성)**:
네트워크 파티션이나 일부 서버 장애가 발생해도 시스템은 계속 응답한다. 정확하지 않을 수 있지만 오류보다는 부분적 데이터를 반환한다.

```
예: 쇼핑몰 상품 재고 조회
  ACID (RDBMS): 재고 서버 장애 → 전체 쇼핑몰 접속 불가
  BASE (NoSQL): 재고 서버 장애 → "재고 정보 임시 불가" 표시 후 나머지 기능 정상
```

**Soft-state (소프트 상태)**:
시스템의 상태는 고정되지 않고, 시간이 지남에 따라 업데이트 없이도 변할 수 있다. 복제(Replication) 중인 데이터는 노드마다 잠시 다를 수 있다.

**Eventually Consistent (결과적 일관성)**:
모든 업데이트가 충분한 시간이 지나면 모든 복제본에 전파된다. "항상 일관적"이 아닌 "결국 일관적"이 됨을 보장한다.

```
결과적 일관성 타임라인:
  t=0  : Node A에 "user=홍길동, 등급=VIP" 업데이트
  t=10ms: Node A 반영 완료, Node B·C는 여전히 "GOLD"
  t=50ms: Node B에 복제 완료
  t=100ms: Node C에 복제 완료 → 모든 노드 일치!

  → 100ms 동안은 노드마다 다른 값을 반환할 수 있음
```

샤딩(Sharding)은 하나의 데이터셋을 여러 서버에 분산 저장하는 수평 파티셔닝(Horizontal Partitioning) 기법이다.

| 샤딩 전략 | 방식 | 장점 | 단점 |
|:---|:---|:---|:---|
| **해시 샤딩** | `shard = hash(key) % N` | 균등 분산 | 범위 쿼리 불가 |
| **범위 샤딩** | `shard = key의 범위 구간` | 범위 쿼리 용이 | 핫스팟(Hotspot) 위험 |
| **디렉토리 샤딩** | 별도 매핑 테이블 | 유연한 재배치 | 매핑 테이블 병목 |
| **지리 샤딩** | 지역별 분리 | 데이터 주권, 지연 감소 | 교차 지역 쿼리 어려움 |

```
해시 샤딩 (Consistent Hashing, 일관 해시):

사용자 ID → 해시 함수 → 샤드 번호

user_id=1001 → hash=2847  → 샤드 0 (0~3000)
user_id=1002 → hash=7231  → 샤드 2 (6000~9000)
user_id=1003 → hash=5119  → 샤드 1 (3000~6000)

┌──────────┐  ┌──────────┐  ┌──────────┐
│  샤드 0  │  │  샤드 1  │  │  샤드 2  │
│ user 1001│  │ user 1003│  │ user 1002│
│ user ...  │  │ user ...  │  │ user ...  │
└──────────┘  └──────────┘  └──────────┘
   서버 A         서버 B         서버 C
```

**일관 해시(Consistent Hashing)**: 서버 추가/제거 시 재분배되는 키의 수를 최소화하는 해시 기법. 일반 해시 대비 서버 N개 변경 시 O(K/N) 키만 이동(K=전체 키 수).

```
Cassandra의 일관성 수준 (Consistency Level):

쓰기 요청
  Client ──────────────────► 코디네이터 노드
                                  │
              ┌───────────────────┼────────────────┐
              ▼                   ▼                ▼
           노드 A              노드 B           노드 C
         (Primary)           (Replica)        (Replica)

Consistency Level 설정:
  ONE    : 1개 노드 확인 → 빠름, 일관성 약함
  QUORUM : (N/2+1)개 확인 → 균형
  ALL    : 모든 노드 확인 → 느림, 일관성 강함
```

---

## 6. 기대효과 및 결론

기술사 답안에서는 **"BASE vs ACID를 단순 대립이 아닌 비즈니스 요건에 따른 트레이드오프"**로 서술해야 한다.

NoSQL BASE (Basically Available, Soft-state, Eventually Consistent) 결과적 일관성 샤딩의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
ACID (RDBMS: 강한 일관성)
    │
    ▼
BASE (NoSQL: 유연한 일관성)
    ├─► Basically Available: 항상 응답
    ├─► Soft State: 시간이 지나면 변할 수 있음
    └─► Eventual Consistency: 최종적 일관성 보장
    │
    ▼
Sharding: 수평 분할 · Consistent Hashing
```
2. 샤딩은 학교 급식 배식대를 여러 줄로 나눈 것이야 — 줄이 많을수록 밥을 빨리 받을 수 있어!
3. 결과적 일관성은 SNS에서 내가 올린 사진이 모든 친구에게 5초 뒤에 뜨는 것 — 동시에 안 보여도 결국은 다 보게 되잖아?

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| BASE 속성 | Basically Available | 부분 장애에도 계속 응답 |
| BASE 속성 | Soft-state | 복제 중 노드마다 상태 불일치 허용 |
| BASE 속성 | Eventually Consistent | 시간 경과 후 모든 노드 일치 |
| 수평 분산 | 샤딩 (Sharding) | 데이터를 여러 서버에 분산 |
| 분산 해시 | 일관 해시 (Consistent Hashing) | 노드 변경 시 최소 재배치 |
| 비교 개념 | ACID (A·C·I·D) | 관계형 DB 트랜잭션 보장 |
| CAP 연결 | CAP 정리 (CAP Theorem) | 분산 시스템 일관성·가용성 한계 |
