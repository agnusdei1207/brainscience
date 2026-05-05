+++
weight = 36
title = "36. 키-값 저장소 (Key-Value Store)"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: 키-값 저장소(Key-Value Store)는 고유한 키(Key)에 임의의 값(Value)을 연결해 저장하는 가장 단순한 NoSQL 구조로, 해시 테이블의 분산·영속화 버전이다.
> **비유**: 자료를 아무 곳에나 쌓는 창고가 아니라, 찾고 연결하고 다시 활용할 수 있도록 질서를 부여한 보관 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

키-값 저장소 (Key-Value Store)은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
구조: 해시 맵의 분산 영속화 버전

key: "session:user_1234"
value: {"user_id":1234, "username":"홍길동", "role":"admin", "exp":1735689600}

기본 연산:
  SET key value           <- O(1)
  GET key                 <- O(1)
  DEL key                 <- O(1)
  EXISTS key              <- O(1)
  EXPIRE key seconds      <- TTL 설정

특징:
  - 키: 임의 문자열 (최대 512MB, Redis 기준)
  - 값: 문자열, JSON, 바이너리 등 임의 형식
  - 스키마 없음 (Schema-less)
```

---

## 2. 구성요소

```
Redis (Remote Dictionary Server) 특성:

메모리 기반 (초고속):
  10만 TPS 이상, 1ms 미만 응답

데이터 구조 (단순 키-값 넘어서):
  String: SET/GET (캐시, 카운터)
  List:   LPUSH/RPUSH (큐, 스택)
  Set:    SADD/SMEMBERS (고유 방문자)
  Sorted Set: ZADD/ZRANGE (리더보드)
  Hash:   HSET/HGET (사용자 프로필)
  Stream: XADD (이벤트 로그)

영속화 (Durability):
  RDB: 주기적 스냅샷 (성능 우선)
  AOF: 모든 쓰기 로그 (데이터 안전 우선)
```

| 사용 패턴       | Redis 자료구조  | 명령           |
|--------------|--------------|---------------|
| 세션 저장      | String + TTL  | SET + EXPIRE  |
| 실시간 카운터  | String        | INCR          |
| 중복 제거      | Set           | SADD          |
| 리더보드       | Sorted Set    | ZADD + ZRANGE |
| 메시지 큐      | List          | LPUSH + BRPOP |

---

## 3. 구조 및 원리

**핵심 조건**: 키-값 저장소 (Key-Value Store)은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```
DynamoDB 특성:
  완전 관리형 (서버리스)
  단일 자릿수 밀리초 응답
  자동 수평 확장 (수천 TPS -> 수백만 TPS)
  
  기본 키 설계:
  - Partition Key (PK): 데이터 분산 키
  - Sort Key (SK): 파티션 내 정렬 (선택)
  
  예시 설계:
  PK: "USER#1234"
  SK: "ORDER#2024-01-01"
  -> 단일 사용자의 모든 주문을 효율적으로 쿼리
```

| 비교       | Redis           | DynamoDB          |
|-----------|-----------------|-------------------|
| 저장 위치  | 메모리 (주) + 디스크| 디스크 (SSD)    |
| 지연       | < 1 ms          | 1-9 ms            |
| 확장       | 클러스터 수동 설정| 완전 자동          |
| 비용 모델  | 인스턴스         | 요청/스토리지 종량제|
| 일관성     | 최종 일관성      | 강한/최종 일관성 선택|

---

## 4. 비교 및 연결

```
1. Cache-Aside (Lazy Loading):
   앱 -> Redis에 요청
   Redis 미스 -> DB 쿼리 -> Redis에 저장 -> 반환
   
2. Write-Through:
   쓰기 시 DB와 캐시에 동시 저장
   항상 캐시와 DB 동기화
   
3. Write-Behind:
   쓰기 시 캐시에만 저장
   비동기로 DB 반영 (고성능, 데이터 손실 위험)

4. TTL (Time To Live):
   SET session:1234 {...} EX 3600
   1시간 후 자동 만료
```

---

## 5. 실무 적용 및 판단

```
이커머스 Redis 사용 패턴:

1. 세션: SET session:{token} {json} EX 1800
2. 상품 캐시: SET product:{id} {json} EX 3600
3. 재고 카운터: DECR stock:{product_id}
4. 장바구니: HSET cart:{user_id} {product_id} {qty}
5. 인기 상품: ZINCRBY popular:daily {product_id} 1
6. 속도 제한: INCR rate:{ip}:{minute} + EXPIRE
7. 분산 락: SET lock:{resource} {uuid} NX EX 30
```

---

## 6. 기대효과 및 결론

키-값 저장소 (Key-Value Store)의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```
[초기 캐시 기술]
Memcached (2003): 단순 메모리 캐시
      |
      v
[Redis 등장 (2009)]
인메모리 + 다양한 자료구조 + 영속화
Memcached를 대부분 대체
      |
      v
[DynamoDB (Amazon, 2012)]
서버리스 분산 키-값 서비스
      |
      v
[Redis Enterprise / Redis Cloud]
글로벌 분산 Redis, Active-Active
      |
      v
[현재: Redis Stack + AI 기능]
Vector 검색, JSON, TimeSeries 내장
AI 임베딩 벡터 저장소로 활용
```

---

## 8. 관련 개념 맵

```
키-값 저장소
+-- Redis (인메모리)
|   +-- 자료구조: String/List/Set/ZSet/Hash
|   +-- 영속화: RDB / AOF
|   +-- 클러스터: 샤딩 + 레플리케이션
+-- DynamoDB (서버리스)
|   +-- PK + SK 설계
|   +-- 자동 확장
|   +-- GSI (글로벌 보조 인덱스)
+-- 캐시 패턴
|   +-- Cache-Aside / Write-Through / Write-Behind
|   +-- TTL (만료 시간)
+-- 관련 NoSQL
    +-- Memcached (단순 캐시)
    +-- Cassandra (열 기반)
    +-- Aerospike (인메모리 + NVMe)
```
