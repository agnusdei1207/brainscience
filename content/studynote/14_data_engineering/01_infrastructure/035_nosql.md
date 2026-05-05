+++
weight = 35
title = "35. NoSQL 데이터베이스"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: NoSQL (Not Only SQL)은 관계형 DB의 고정 스키마와 ACID 트랜잭션을 일부 포기하는 대신, 수평 확장(Scale-Out)·고가용성·대용량 비정형 데이터 처리에 최적화된 데이터 저장 패러다임이다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

NoSQL 데이터베이스은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
RDBMS                    NoSQL
+-- 고정 스키마           +-- 유연한 스키마
+-- ACID 트랜잭션         +-- BASE (결과적 일관성)
+-- 수직 확장 (Scale-Up) +-- 수평 확장 (Scale-Out)
+-- SQL 표준             +-- 각 DB별 고유 API
+-- 관계 모델            +-- 문서/키값/그래프 등
```

| 항목          | RDBMS          | NoSQL             |
|-------------|----------------|-------------------|
| 스키마        | 고정            | 유연 (Schema-less)|
| 확장         | 수직            | 수평              |
| 트랜잭션      | ACID            | BASE / 결과적 일관성|
| 쿼리 언어     | SQL             | DB별 API          |
| 조인         | 복잡한 조인 가능 | 조인 어려움 / 비정규화|
| 적합 워크로드 | 정형 + OLTP     | 대용량, 비정형, 빠른 쓰기|

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```
1. 키-값 (Key-Value)
   key: "user:1001"
   value: { name: "홍길동", age: 30 }
   예시: Redis, DynamoDB, Memcached
   장점: 단순, 초고속 읽기/쓰기

2. 문서 (Document)
   {
     "_id": "order_001",
     "items": [{"sku": "A1", "qty": 2}],
     "total": 5000
   }
   예시: MongoDB, Firestore, CouchDB
   장점: JSON 유사 구조, 계층적 데이터

3. 열 (Column-Family)
   RowKey: "user#001"
   CF:info -> { name, email, signup_date }
   CF:activity -> { last_login, page_views }
   예시: Cassandra, HBase, BigTable
   장점: 시계열, 대용량 쓰기

4. 그래프 (Graph)
   (홍길동)-[:FOLLOWS]->(김철수)
   예시: Neo4j, Amazon Neptune
   장점: 관계 탐색 (SNS, 추천, 사기 탐지)
```

---

## 3. 구조 및 원리

**핵심 조건**: NoSQL 데이터베이스은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```
CAP 정리:
분산 시스템에서 Consistency, Availability,
Partition Tolerance 중 최대 2개만 보장 가능

        C (일관성)
       / \
      /   \
CA    /     \ CP
    /         \
   /     AP    \
  A (가용성) -- P (분단 허용)

NoSQL 대부분: AP 선택 (가용성 + 분단 허용)
  -> 결과적 일관성 (Eventually Consistent)
```

| DB        | CAP 선택 | 특성                     |
|----------|---------|--------------------------|
| MongoDB   | CP/AP   | 설정에 따라 선택 가능     |
| Cassandra | AP      | 결과적 일관성, 고가용성   |
| HBase     | CP      | 강한 일관성, ZooKeeper    |
| Redis     | CP      | 메모리, 단일 노드 강함    |
| DynamoDB  | AP      | 글로벌 분산, 결과적 일관성|

---

## 4. 비교 및 연결

```
ACID (RDBMS):
  Atomicity  - 트랜잭션 원자성 (All or Nothing)
  Consistency - 무결성 제약 항상 유지
  Isolation  - 트랜잭션 간 격리
  Durability - 커밋된 데이터 영구 보존

BASE (NoSQL):
  Basically Available  - 기본 가용성 보장
  Soft State           - 상태가 변할 수 있음
  Eventually Consistent - 결과적으로 일관성 수렴
```

---

## 5. 실무 적용 및 판단

| 데이터 유형    | 저장소         | 이유                        |
|-------------|--------------|------------------------------|
| 상품 카탈로그  | MongoDB      | JSON 구조, 유연한 스키마      |
| 세션/장바구니  | Redis        | 빠른 키-값, TTL 지원         |
| 주문 이력     | MySQL/PostgreSQL | ACID, 재무 정합성 필요      |
| 추천 시스템   | Neo4j        | 그래프 관계 탐색 (구매 패턴)  |
| 클릭스트림    | Cassandra    | 시계열 대용량 쓰기           |

---

## 6. 기대효과 및 결론

NoSQL 데이터베이스의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```
[RDBMS 독주 시대 (1970s~2000s)]
관계형 모델, SQL 표준, ACID
      |
      v
[웹 2.0 스케일 문제 (2003~2008)]
Google Bigtable (2006), Amazon Dynamo (2007)
대용량 수평 확장 필요성
      |
      v
[NoSQL 붐 (2009~2012)]
MongoDB, Cassandra, Redis 등장
"NoSQL" 용어 확산
      |
      v
[NewSQL 등장 (2012~)]
Google Spanner, CockroachDB
ACID + 수평 확장 동시 달성
      |
      v
[현재: 다중 모델 DB]
한 DB가 여러 모델 지원
CosmosDB, ArangoDB, YugabyteDB
```

---

## 8. 관련 개념 맵

```
NoSQL
+-- 4대 모델
|   +-- 키-값: Redis, DynamoDB
|   +-- 문서: MongoDB, Firestore
|   +-- 열: Cassandra, HBase
|   +-- 그래프: Neo4j, Neptune
+-- 이론
|   +-- CAP 정리 (CP/AP/CA)
|   +-- BASE (vs ACID)
|   +-- 수평 확장 (Sharding)
+-- 적용 패턴
    +-- 세션 저장 (Redis)
    +-- 이벤트 소싱 (Cassandra)
    +-- 콘텐츠 관리 (MongoDB)
    +-- 사기 탐지 (Neo4j)
```
