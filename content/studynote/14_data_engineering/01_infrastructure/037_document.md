+++
weight = 37
title = "37. 문서 저장소 (Document Store)"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: 문서 저장소(Document Store)는 JSON·BSON·XML 형태의 반정형 문서를 고유 ID와 함께 저장하는 NoSQL 데이터베이스로, 스키마를 사전에 정의하지 않아도 다양한 구조의 문서를 유연하게 저장할 수 있다.
> **비유**: 자료를 아무 곳에나 쌓는 창고가 아니라, 찾고 연결하고 다시 활용할 수 있도록 질서를 부여한 보관 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

문서 저장소 (Document Store)은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
문서 (Document) 예시 (JSON):
{
  "_id": "order_12345",
  "customer": {
    "id": "user_789",
    "name": "홍길동",
    "email": "hong@example.com"
  },
  "items": [
    {"product_id": "prod_001", "name": "노트북", "qty": 1, "price": 1500000},
    {"product_id": "prod_002", "name": "마우스", "qty": 2, "price": 30000}
  ],
  "total": 1560000,
  "status": "shipped",
  "created_at": "2024-01-15T10:30:00Z"
}

컬렉션 (Collection) = 관계형 DB의 테이블 (스키마 없음)
문서 (Document) = 관계형 DB의 행 (JSON 형식)
필드 (Field) = 관계형 DB의 열 (동적)
```

---

## 2. 구성요소

```
데이터 모델링 핵심 선택:

내포 (Embedding):
  관련 데이터를 한 문서 안에 포함
  
  {
    "order_id": "order_001",
    "items": [  // 주문 항목을 내포
      {"product": "노트북", "qty": 1}
    ]
  }
  
  장점: 단일 읽기로 완전한 데이터
        조인 없음, 빠른 조회
  단점: 데이터 중복, 문서 크기 증가
  적합: 함께 자주 조회되는 데이터

참조 (Reference):
  다른 문서의 ID만 저장
  
  {
    "order_id": "order_001",
    "customer_id": "user_789"  // 참조만 저장
  }
  
  장점: 중복 없음, 정규화
  단점: 여러 번 조회 필요
  적합: 독립적으로 업데이트되는 데이터
```

| 전략    | 장점               | 단점            | 사용 경우          |
|-------|------------------|--------------|--------------------|
| 내포   | 단일 읽기, 빠름    | 중복, 크기     | 함께 조회하는 관계  |
| 참조   | 중복 없음, 정규화  | 여러 번 조회   | 독립 엔티티         |

---

## 3. 구조 및 원리

**핵심 조건**: 문서 저장소 (Document Store)은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
orders = db["orders"]

# 삽입 (Insert)
result = orders.insert_one({
    "customer": "홍길동",
    "total": 50000,
    "status": "pending"
})

# 조회 (Find)
order = orders.find_one({"customer": "홍길동"})
all_orders = orders.find({"status": "pending"})

# 업데이트 (Update)
orders.update_one(
    {"_id": result.inserted_id},
    {"$set": {"status": "shipped"}}
)

# 배열 조작 ($push, $pull)
orders.update_one(
    {"_id": result.inserted_id},
    {"$push": {"items": {"product": "키보드", "qty": 1}}}
)

# 집계 파이프라인 (Aggregation)
pipeline = [
    {"$match": {"status": "shipped"}},
    {"$group": {"_id": "$customer", "total": {"$sum": "$total"}}}
]
result = list(orders.aggregate(pipeline))
```

---

## 4. 비교 및 연결

```
상품 카탈로그 예시:

RDBMS 방식:
  products 테이블 + attributes 테이블
  + product_attributes (조인 테이블)
  -> 3개 테이블 조인 필요

  문제: 전자제품/의류/식품 마다 속성이 달라
        스키마가 폭발적으로 복잡해짐

문서 저장소 방식:
  {
    "name": "삼성 TV",
    "category": "electronics",
    "specs": {"resolution": "4K", "size": "65인치", "hdmi": 4}
  }
  {
    "name": "청바지",
    "category": "clothing",
    "specs": {"size": "32", "color": "blue", "material": "cotton"}
  }
  
  -> 각 상품마다 다른 속성을 유연하게 저장!
```

---

## 5. 실무 적용 및 판단

```
문제 상황:
  전자제품(해상도·주파수)과 의류(사이즈·색상)를
  같은 테이블에 저장 -> RDBMS 한계

MongoDB 솔루션:
  products 컬렉션에 다양한 구조의 문서 저장
  인덱스: 카테고리, 가격, 이름에 인덱스 생성
  
  인덱스 생성:
    db.products.createIndex({"category": 1, "price": -1})
    -> 카테고리별 가격 내림차순 조회 최적화

  전문 검색 (Full Text Search):
    db.products.createIndex({"name": "text", "description": "text"})
    db.products.find({"$text": {"$search": "무선 헤드폰"}})

  결과:
    RDBMS 대비 상품 조회 응답시간 40% 개선
    스키마 변경 없이 새 카테고리 즉시 추가
```

---

## 6. 기대효과 및 결론

문서 저장소 (Document Store)의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```
[RDBMS 한계 (2000s)]
반정형 데이터 증가
스키마 유연성 요구
      |
      v
[CouchDB, MongoDB 등장 (2007~2009)]
JSON 문서 저장
수평 확장, 스키마리스
      |
      v
[MongoDB Atlas (2016~)]
클라우드 완전 관리형 MongoDB
      |
      v
[현재: 멀티모델 DB]
MongoDB가 문서 + 검색 + 분석 통합
Vector Search 추가 (AI 임베딩 저장)
```

---

## 8. 관련 개념 맵

```
문서 저장소 (Document Store)
+-- 저장 형식: JSON/BSON/XML
+-- 핵심 개념
|   +-- 내포 (Embedding) vs 참조 (Reference)
|   +-- 스키마리스 (Schema-less)
|   +-- 컬렉션 / 문서 / 필드
+-- 주요 제품
|   +-- MongoDB (가장 널리 사용)
|   +-- Firestore (서버리스 Google)
|   +-- CouchDB (분산 동기화)
+-- 사용 시나리오
    +-- 상품 카탈로그 (다양한 속성)
    +-- 사용자 프로필 (중첩 데이터)
    +-- 콘텐츠 관리 시스템 (CMS)
```
