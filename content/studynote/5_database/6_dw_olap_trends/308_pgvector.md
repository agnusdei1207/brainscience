+++
title = "308. PGVector"
weight = 4308
+++

> **💡 핵심 인사이트**
> PGVector는 **PostgreSQL 데이터베이스에 벡터 검색 기능을原生(네이티브)插件으로 추가하는 확장 모듈**입니다. 기존 관계형 DB의 ACID 트랜잭션, 백업, 복제, 접근 제어 등 모든 생태계를 그대로 활용하면서 LLM 임베딩의 유사도 검색을 SQL 수준에서 구현할 수 있게 합니다.
> 별도의 벡터 전용 DB( Pinecone, Milvus, Qdrant 등)를 도입할 필요 없이, **기존 PostgreSQL 인프라로 RAG(Retrieval-Augmented Generation) 파이프라인을 무설계”而 구축 가능**하다는 점이 가장 큰 매력입니다.

---

## Ⅰ. 벡터 검색의 민주화: 왜 PostgreSQL인가?

기업 시스템에서 벡터 DB를 도입할 때 가장 큰 부담은 **새로운 시스템 도입의 복잡성**입니다. 기존 PostgreSQL/MySQL/Oracle 등 관계형 DB가 있다면 그 위에 새로운 벡터 DB를 붙이는 것은:
- **운영 부담 증가**: 별도 클러스터 관리, 모니터링, 백업 정책 추가
- **데이터 동기화 문제**: 기존 데이터와 벡터 간 JOIN이 복잡해짐
- **인력 역량 필요**: 새 벡터 DB 특화 스킬 확보 필요

PGVector는 이러한 부담을 **"기존 RDB 안에 벡터 칼럼을 그냥 추가하면 된다"**는 아이디어로 해소합니다.

---

## Ⅱ. PGVector의 핵심 기능과 SQL 통합

```
[PostgreSQL 테이블에 벡터 열 추가]
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536)  -- 1536차원 임베딩 저장
);

[벡터 유사도 검색 - 코사인 유사도]
SELECT id, content,
       1 - (embedding <=> '[0.1, 0.3, ...]'::vector) AS similarity
FROM documents
ORDER BY embedding <=> '[0.1, 0.3, ...]'::vector
LIMIT 5;
-- <=> 연산자: 벡터 간 거리에 사용 (코사인 거리)
-- <#> : 음수 내적, <=> : L2 유클리디안 거리, <=> : 코사인 거리
```

**지원하는 거리 연산자 3가지:**
- **<-> (유클리디안 거리)**: 공간상 직선 거리, 이미지 벡터에 적합
- **<=> (코사인 거리)**: 방향성 유사도, 텍스트 임베딩에 가장 많이 사용
- **<#> (음수 내적)**: 내적값, 정규화된 벡터에서 코사인 유사도와 비례

**인덱스 유형 (ANN 최적화):**
- **HNSW (Hierarchical Navigable Small World)**: 기본값, 높은 검색 품질, 메모리 많이 사용
- **IVFFlat**: 메모리 제약이 있을 때, 빌드 시간 김

```
-- HNSW 인덱스 생성
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);

-- IVFFlat 인덱스 생성
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);
```

---

## Ⅲ. HNSW + PGVector: 메모리 내 그래프 ANN의威力

PGVector의 가장 강력한 인덱스는 **HNSW(Hierarchical Navigable Small World)**입니다. 이는 여러 계층의 그래프를 구축하여:

```
[ HNSW 계층 구조 ]

Layer 3:  ●───────●
         (최상층, 가장 적은 노드, 가장 빠른 길찾기)

Layer 2:  ●──●──●──●──●──●
         (중간층, 군집 간 연결)

Layer 1:  ●●●●●●●●●●●●●●●●●
         (근본층, 모든 노드 연결, 높은 정밀도)
```

**동작 원리:**
1. 상위 계층에서 시작하여 query 벡터와 가장 가까운 노드 탐색
2. 하위 계층으로 점점 내려가며 탐색 영역 수렴
3. 최하층에서 가장 가까운 이웃 결정

PGVector에서 HNSW를 사용할 때 **메모리消费量**가 핵심입니다. `embedding vector(1536)` 한 개는 1536 × 4바이트(float32) = **약 6KB**입니다. 100만 건이면 약 6GB 메모리가 필요합니다.

---

## Ⅳ. PGVector의 한계와 대안적 접근

**한계:**
1. **확장성**: 1000만 개 이상 벡터에서는 전용 벡터 DB(Milvus, Qdrant)가 성능 우위
2. **멀티テ넌시**: 대규모 멀티테넌트 환경에서는 파티셔닝 전략 필요
3. **실시간 업데이트**:频繁한 벡터 갱신 시 인덱스 리빌드 비용 발생

**대안 비교:**

| 구분 | PGVector | Milvus/Qdrant | Pinecone |
|------|----------|---------------|----------|
| 도입 비용 | 낮음 (PostgreSQL만) | 중간 (별도 클러스터) | 높음 (SaaS) |
| 확장성 | 보통 (~1000만) | 높음 (수억) | 매우 높음 |
| SQL 통합 | 완벽 | 제한적 | 제한적 |
| 관리 편의성 | 높음 | 중간 | 높음 |

---

## Ⅴ. RAG 파이프라인에서의 활용과 📢 비유

**실제 RAG(Retrieval-Augmented Generation) 파이프라인:**

```python
# Python 예시 (psycopg2 활용)
import openai
import psycopg2

# 1. 문서 임베딩 생성 및 저장
doc = "지구의 기후 변화는 심각한 문제입니다."
embedding = openai.Embedding.create(input=doc, model="text-embedding-ada-002")
vector = embedding['data'][0]['embedding']

cur.execute(
    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
    (doc, vector)
)

# 2. 사용자 질문 기반 검색
query = "환경 문제의 주요 원인은?"
query_embedding = openai.Embedding.create(input=query, model="text-embedding-ada-002")

results = cur.execute("""
    SELECT content, 1 - (embedding <=> %s::vector) AS similarity
    FROM documents
    ORDER BY embedding <=> %s::vector
    LIMIT 3
""", (query_embedding, query_embedding))
```

> 📢 **섹션 요약 비유:** PGVector는 **"이미 살고 있는 도시에 새로운 동네 카페를 열는 것"**과 같습니다. 별도의 새 건물(전용 벡터 DB)을 짓는 것(도입, 교육, 유지보수 부담)相比, 기존 마을(PostgreSQL)의 빈 공간에小店(벡터 열)을 열어서 **마을 전체의治安(ACID),公共服务(백업/복제), 기존 주민과의関係(JOIN)를 그대로利用하면서** 새로운 서비스(유사도 검색)를 제공할 수 있는 가장 현실적인 해법입니다.
