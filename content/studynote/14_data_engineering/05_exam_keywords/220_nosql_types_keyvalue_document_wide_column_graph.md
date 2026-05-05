+++
weight = 220
title = "220. NoSQL 유형 비교: 키-값·도큐먼트·Wide-Column·그래프 (NoSQL Types Comparison)"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: NoSQL은 "Not Only SQL"로, RDBMS의 엄격한 스키마와 ACID 제약을 완화하고 **수평 확장(Scale-Out)**을 통해 빅데이터 규모의 다양한 데이터 모델을 처리하기 위해 등장했다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

2000년대 후반 Google(Bigtable, 2006), Amazon(Dynamo, 2007), Facebook(Cassandra, 2008)이 기존 RDBMS로는 처리 불가능한 규모의 서비스를 위해 자체 NoSQL DB를 개발·공개하면서 NoSQL 생태계가 폭발적으로 성장했다.

**RDBMS의 한계:**
- 수평 확장(Scale-Out) 어려움 → 수직 확장(Scale-Up) 비용 폭증
- 엄격한 스키마 → 비정형 데이터 처리 불가
- ACID 트랜잭션 오버헤드 → 초고속 처리 성능 저하
- JOIN 연산 비용 → 분산 환경에서 네트워크 병목

---

## 2. 구성요소

| RDBMS ACID | NoSQL BASE | 설명 |
|:---|:---|:---|
| Atomicity | Basically Available | 일부 노드 장애에도 서비스 지속 |
| Consistency | Soft-state | 일시적 불일치 허용 |
| Isolation | Eventually Consistent | 시간이 지나면 일관성 달성 |
| Durability | - | 내구성은 유지 |

---

## 3. 구조 및 원리

**핵심 조건**: NoSQL 유형 비교: 키-값·도큐먼트·Wide-Column·그래프 (NoSQL Types Comparison)은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```
NoSQL 유형별 데이터 모델
┌──────────────┬──────────────────────────────────────────┐
│ 키-값        │  "user:1234" → { name, age, email }     │
│ (Key-Value)  │  단순 해시맵, 빠른 단일 조회             │
├──────────────┼──────────────────────────────────────────┤
│ 도큐먼트     │  { _id: 1, name: "홍길동",              │
│ (Document)   │    orders: [{...}, {...}] }             │
│              │  JSON/BSON 중첩 구조, 유연한 스키마      │
├──────────────┼──────────────────────────────────────────┤
│ 와이드 컬럼  │  Row Key │ CF:col1 │ CF:col2 │ ...      │
│ (Wide-Column)│  희소 행렬, 컬럼 패밀리 단위 저장        │
├──────────────┼──────────────────────────────────────────┤
│ 그래프       │  (노드A) -[관계:FRIENDS]-> (노드B)       │
│ (Graph)      │  노드·엣지·속성, 관계 탐색 최적화        │
└──────────────┴──────────────────────────────────────────┘
```

---

## 4. 비교 및 연결

| 항목 | 키-값 | 도큐먼트 | 와이드 컬럼 | 그래프 |
|:---|:---|:---|:---|:---|
| **대표 제품** | Redis, DynamoDB | MongoDB, Couchbase | Cassandra, HBase | Neo4j, Amazon Neptune |
| **데이터 모델** | 단순 Key→Value | JSON/BSON 도큐먼트 | 컬럼 패밀리 | 노드·엣지 그래프 |
| **쿼리 방식** | Key 기반 단순 조회 | 필드 쿼리, 인덱스 | Row Key, 범위 스캔 | Cypher, Gremlin |
| **확장성** | 매우 높음 | 높음 | 매우 높음 | 수평 확장 어려움 |
| **일관성** | 결과적/조정 가능 | 도큐먼트 단위 ACID | 결과적/조정 가능 | ACID (Neo4j) |
| **주 사용 사례** | 캐시, 세션, 리더보드 | 컨텐츠 관리, 카탈로그 | 시계열, IoT, 로그 | SNS 관계, 추천, 지식 그래프 |
| **JOIN 지원** | 없음 | 제한적 ($lookup) | 없음 | 그래프 순회 |

---

## 5. 실무 적용 및 판단

**키-값 (Key-Value):**
- Redis: 인메모리 + RDB/AOF 영속성, 자료 구조(Hash·List·Sorted Set) 지원
- DynamoDB: 서버리스, 자동 샤딩(Auto Sharding), DAX 캐시 계층

**도큐먼트 (Document):**
- MongoDB: BSON 저장, Aggregation Pipeline, Atlas Search(전문 검색)
- 스키마 유연성 → 마이크로서비스의 독립 스키마 진화에 적합

**와이드 컬럼 (Wide-Column):**
- Cassandra: 일관적 해시(Consistent Hashing) + 가십 프로토콜(Gossip Protocol), 쓰기 최적화(LSM Tree)
- HBase: Hadoop/HDFS 위에 동작, 강한 일관성, HBase → Hadoop 분석 연계

**그래프 (Graph):**
- Neo4j: Property Graph 모델, Cypher 쿼리 언어, 임베디드/클러스터 모드
- 사용 사례: 부정 탐지(Fraud Detection), 추천 엔진, 지식 그래프, SNS

| 항목 | NoSQL | NewSQL |
|:---|:---|:---|
| **목표** | 확장성·유연성 | 확장성 + ACID 보장 |
| **대표 제품** | MongoDB, Cassandra | Spanner, CockroachDB, TiDB |
| **SQL 지원** | 제한적 | 완전 SQL |
| **일관성** | 결과적 일관성 | 강한 일관성 |

| 사용 사례 | 권장 유형 | 이유 |
|:---|:---|:---|
| 웹 세션 캐시 | 키-값 (Redis) | 빠른 만료(TTL) 관리, 인메모리 |
| 사용자 프로필 | 도큐먼트 (MongoDB) | 유연한 속성, 중첩 데이터 |
| IoT 시계열 로그 | 와이드 컬럼 (Cassandra) | 쓰기 집중, 시간 범위 스캔 |
| SNS 친구 추천 | 그래프 (Neo4j) | 다단계 관계 탐색 |
| 쇼핑몰 상품 카탈로그 | 도큐먼트 (MongoDB) | 다양한 속성, 전문 검색 |
| 실시간 순위표 | 키-값 (Redis Sorted Set) | O(log n) 순위 갱신 |

1. **복합 사용 패턴**: 하나의 서비스에 여러 NoSQL 혼용 (Polyglot Persistence)
2. **RDBMS와 공존**: RDBMS는 트랜잭션 핵심, NoSQL은 캐시·로그·분석 보조
3. **운영 복잡성**: NoSQL 도입 시 관리 오버헤드 증가 → 관리형 서비스(AWS DynamoDB, Atlas) 활용

| 효과 | 정량적 목표 |
|:---|:---|
| 읽기 성능 향상 | Redis 캐시 도입으로 DB 부하 70~90% 감소 |
| 쓰기 처리량 증가 | Cassandra 클러스터 확장으로 초당 수십만 건 처리 |
| 개발 민첩성 | 스키마 없는 도큐먼트 DB로 스키마 마이그레이션 없이 기능 추가 |
| 관계 분석 속도 | 6단계 친구 찾기: RDBMS 수십 초 → Neo4j 수십 밀리초 |

---

## 6. 기대효과 및 결론

**키-값 (Key-Value):** Redis: 인메모리 + RDB/AOF 영속성, 자료 구조(Hash·List·Sorted Set) 지원 DynamoDB: 서버리스, 자동 샤딩(Auto Sharding), DAX 캐시 계층 **도큐먼트 (Document):** MongoDB: BSON 저장, Aggregation Pipeline, Atlas Search(전문 검색) 스키마 유연성 → 마이크로서비스의 독립 스키마 진화에 적합 **와이드 컬럼 (Wide-Column):** Cassandra: 일관적 해시(Consistent Hashing) + 가십 프로토콜(Gossip Protocol), 쓰기 최적화(LSM Tree) HBase: Hadoop/HDFS 위에 동작, 강한 일관성, HBase → Hadoop 분석 연계 **그래프 (Graph):** Neo4j: Property Graph 모델, Cypher 쿼리 언어, 임베디드/클러스터 모드 사용 사례: 부정 탐지(Fraud Detection), 추천 엔진, 지식 그래프, SNS 1.

NoSQL 유형 비교: 키-값·도큐먼트·Wide-Column·그래프 (NoSQL Types Comparison)의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
RDBMS (관계형, 정형 데이터)
    │
    ▼
NoSQL 4대 유형
    ├─► Key-Value: Redis · DynamoDB (캐시 · 세션)
    ├─► Document: MongoDB · CouchDB (유연 스키마)
    ├─► Wide-Column: Cassandra · HBase (대규모 쓰기)
    └─► Graph: Neo4j · Amazon Neptune (관계 탐색)
    │
    ▼
Multi-Model DB: 여러 데이터 모델 통합 지원
```
2. 도큐먼트는 **서류 봉투**야. 봉투 안에 사진도 넣고 편지도 넣고 뭐든 넣을 수 있어. 내용이 다 달라도 괜찮아.
3. 그래프는 **친구 관계도**야. 나→내 친구→내 친구의 친구를 따라가면서 "우리 학교에서 몇 다리 건너 연결됐지?" 같은 걸 빠르게 찾을 수 있어.

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 분류 | 키-값 (Redis, DynamoDB) | 단순 해시맵, 캐시·세션 최적 |
| 분류 | 도큐먼트 (MongoDB, Couchbase) | JSON/BSON, 유연한 스키마 |
| 분류 | 와이드 컬럼 (Cassandra, HBase) | 시계열·로그, 쓰기 최적화 |
| 분류 | 그래프 (Neo4j, Neptune) | 관계 탐색, SNS·추천 |
| 이론 기반 | CAP 정리 | AP vs CP 선택 근거 |
| 속성 | BASE | NoSQL의 일관성 완화 모델 |
| 진화 | NewSQL (CockroachDB, TiDB) | 확장성 + ACID 결합 |
| 설계 전략 | 폴리글랏 퍼시스턴스 | 목적별 다수 DB 혼용 |
