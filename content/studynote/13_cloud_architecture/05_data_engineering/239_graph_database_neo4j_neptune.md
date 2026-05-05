+++
weight = 239
title = "239. 그래프 저장소 (Graph DB) - Neo4j / Neptune"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++
## 0. 핵심 인사이트

> **핵심**: 그래프 DB는 데이터를 **노드(Node)·엣지(Edge)·속성(Property)**으로 표현하며, 수십 단계의 관계 탐색(Multi-hop Traversal)을 RDBMS의 복잡한 재귀 JOIN 없이 **포인터 체이닝**으로 밀리초에 수행한다.
> 2. **가치**: 소셜 네트워크의 "친구의 친구", 사기 탐지의 "이 계좌와 3단계 이내에 연결된 의심 계좌", 추천 엔진의 "유사 고객이 구매한 상품" 같은 **관계 중심 쿼리**에서 RDBMS 대비 1,000배 이상 빠르다.
> 3. **판단 포인트**: 데이터가 **그물망(Graph) 형태**로 연결되고 관계 탐색이 핵심 쿼리 패턴이면 그래프 DB가 최적이지만, 단순 조인이 아닌 **진정한 다중 홉 관계**가 있어야 투자 가치가 있다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

RDBMS에서 "이 사용자의 친구의 친구의 친구 목록"을 구하려면 self-join을 3번 수행한다. 관계 깊이가 깊어질수록 JOIN 횟수가 기하급수적으로 증가하고, 수천만 노드의 SNS에서는 수초~수분이 걸린다.

그래프 DB는 이 관계를 물리적 포인터로 저장하여, 탐색이 O(depth)로 일정하다.

```
[RDBMS vs Graph DB 관계 탐색 비교]
시나리오: "김철수의 3단계 친구 네트워크 탐색"

RDBMS:
SELECT DISTINCT u3.name
FROM friends f1
JOIN friends f2 ON f1.friend_id = f2.user_id
JOIN friends f3 ON f2.friend_id = f3.user_id
JOIN users u3 ON f3.friend_id = u3.id
WHERE f1.user_id = '김철수'
→ 1,000만 사용자 시: 수분 소요

Graph DB (Cypher):
MATCH (u:Person {name:'김철수'})-[:FRIENDS*1..3]-(friend)
RETURN DISTINCT friend.name
→ 같은 데이터: 밀리초 소요

이유: Graph DB는 포인터를 따라가는 것(인접 리스트 탐색)
     RDBMS는 매번 전체 테이블 조인
```

📢 **섹션 요약 비유**: 그래프 DB는 지하철 노선도다. A역에서 C역까지 가는 경로를 찾을 때, 전체 노선도 모든 역을 다 확인하지 않고 연결된 선(엣지)만 따라가면 빠르게 경로를 찾는다. RDBMS는 매번 전체 역 목록을 조회해야 한다.

---

## 2. 구성요소

### 그래프 DB 기본 구조

```
[그래프 모델]
노드(Node): 실체
  (:Person {name:'김철수', age:28})
  (:Product {name:'책', price:15000})
  (:Company {name:'네이버'})

엣지(Edge/Relationship): 관계
  -[:FRIENDS {since:2020}]->
  -[:PURCHASED {date:'2024-01-15'}]->
  -[:WORKS_AT {role:'개발자'}]->

속성(Property): 노드/엣지의 속성 값

[그래프 예시]
(김철수:Person) -[:FRIENDS]-> (이영희:Person)
(이영희:Person) -[:PURCHASED]-> (책:Product)
(김철수:Person) -[:WORKS_AT]-> (네이버:Company)
```

### Cypher 쿼리 언어 (Neo4j)

```cypher
// 추천 엔진: 나와 같은 책을 구매한 사람들이 구매한 다른 책
MATCH (me:Person {name:'김철수'})-[:PURCHASED]->(book:Product)
      <-[:PURCHASED]-(similar:Person)-[:PURCHASED]->(rec:Product)
WHERE NOT (me)-[:PURCHASED]->(rec)
RETURN rec.name, COUNT(similar) AS score
ORDER BY score DESC
LIMIT 10;

// 사기 탐지: 3단계 이내 의심 계좌 연결
MATCH (account:Account {id:'ACC001'})-[:TRANSFERRED*1..3]-(suspect:Account)
WHERE suspect.risk_score > 0.8
RETURN account, suspect, 
       length(path) AS hops
ORDER BY hops;

// 가장 짧은 경로 (Shortest Path)
MATCH p = shortestPath(
  (a:Person {name:'A'})-[:KNOWS*]-(b:Person {name:'B'})
)
RETURN p;
```

### Amazon Neptune 아키텍처

```
[Amazon Neptune]
완전 관리형 그래프 DB (Multi-AZ 고가용성)

지원 쿼리 언어:
  - Gremlin (Apache TinkerPop)
  - SPARQL (RDF 기반 지식 그래프)
  - openCypher (Neo4j Cypher 호환)

특징:
  - 최대 수십억 관계 저장
  - 읽기 레플리카 최대 15개
  - S3 백업 자동화
  - VPC 내부 격리
```

📢 **섹션 요약 비유**: Cypher 쿼리는 가계도 추적이다. "할아버지의 자녀의 자녀(손자)"를 찾을 때, RDBMS는 전체 가족 DB를 3번 훑어야 하지만, 그래프 DB는 할아버지 노드에서 화살표(엣지)를 따라 바로 손자까지 도달한다.

---

## 3. 구조 및 동작 원리

### 그래프 DB 활용 사례 상세

| 사용 사례 | 그래프 모델 | 쿼리 패턴 |
|:---|:---|:---|
| **소셜 네트워크** | Person-[:FRIENDS]->Person | 친구 추천, 공통 친구 수 |
| **추천 엔진** | User-[:BOUGHT]->Product | 협업 필터링 추천 |
| **FDS (사기 탐지)** | Account-[:TRANSFERRED]->Account | 의심 계좌 관계망 분석 |
| **지식 그래프** | Concept-[:IS_A]->Category | 의미적 관계 추론 |
| **IAM 권한 분석** | User-[:HAS_ROLE]->Role-[:CAN_ACCESS]->Resource | 접근 경로 파악 |
| **공급망 관리** | Supplier-[:SUPPLIES]->Factory | 병목 공급사 분석 |
| **네트워크 토폴로지** | Server-[:CONNECTS]->Router | 장애 전파 경로 추적 |

### Graph DB vs RDBMS 성능 비교 (관계 탐색)

```
[벤치마크: 소셜 네트워크 1억 사용자]
탐색 깊이  RDBMS (MySQL)    Neo4j
2단계 친구    0.016초        0.01초  (유사)
3단계 친구    30.267초       0.168초 (180배 차이)
4단계 친구    시간 초과       1.359초 (수천 배 차이)
5단계 친구    시간 초과       2.132초

결론: 관계 깊이 증가 시 RDBMS 지수 폭발, Graph DB 선형 증가
```

📢 **섹션 요약 비유**: 그래프 DB vs RDBMS 성능 차이는 동네 길 찾기와 GPS 내비게이션의 차이다. RDBMS는 지도 전체를 다 펼쳐보고 경로를 찾는 것, 그래프 DB는 연결된 길(엣지)만 따라가므로 관계가 복잡해질수록 차이가 커진다.

---

## 4. 비교 및 트레이드오프

### FDS (사기 탐지 시스템) 구현 예시

```cypher
// 단계 1: 의심 거래 패턴 식별
MATCH (a:Account)-[t:TRANSFERRED]->(b:Account)
WHERE t.amount > 1000000
  AND t.timestamp > datetime() - duration('PT1H')
WITH a, b, t
// 단계 2: 관련 계좌 네트워크 분석
MATCH (b)-[:TRANSFERRED*1..3]-(suspicious:Account)
WHERE suspicious.blacklisted = true
WITH a, COUNT(suspicious) AS risk_count
WHERE risk_count > 0
// 단계 3: 위험 계좌 표시
SET a.risk_score = a.risk_score + risk_count * 0.1
RETURN a.account_id, a.risk_score
ORDER BY a.risk_score DESC;
```

### 데이터 모델링 원칙

```
[그래프 모델링 체크리스트]
□ 노드: 주요 실체 (사람, 상품, 계좌)
□ 엣지: 관계 동사 (FRIENDS, BOUGHT, TRANSFERRED)
□ 방향성: 엣지에 방향 부여 (단방향/양방향)
□ 속성: 필터링에 필요한 속성을 노드/엣지에 추가
□ 인덱스: 시작 노드 검색 속도 최적화
□ 관계 타입: 과다한 타입 분화 피하기

[안티패턴]
❌ RDBMS 테이블 구조를 그대로 그래프로 변환
❌ 모든 속성을 노드로 변환 (속성은 노드 안에)
❌ 단순 계층 구조를 그래프로 구현 (트리 구조는 RDBMS도 충분)
```

📢 **섹션 요약 비유**: 그래프 DB 데이터 모델링은 인물 관계도 그리기다. 사람(노드)과 관계(엣지)를 명확히 정의하면, 복잡한 관계망도 한눈에 파악하고 원하는 경로를 빠르게 찾을 수 있다.

---

## 5. 실무 적용 및 최적화 기법

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **다중 홉 탐색 속도** | RDBMS JOIN 대비 최대 1,000배 이상 빠른 관계 쿼리 |
| **실시간 추천** | 수십억 관계 중 맞춤 추천을 밀리초에 계산 |
| **FDS 정확도** | 직접 연결이 아닌 간접 관계망 분석으로 사기 탐지 정확도 향상 |
| **지식 그래프** | AI 추론·설명 가능 AI의 기반 데이터 구조 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **수평 확장 어려움** | 그래프 파티셔닝이 RDBMS보다 복잡 (크로스-파티션 탐색 비용) |
| **OLAP 집계 약함** | 전체 집계 쿼리보다 관계 탐색에 특화 |
| **학습 곡선** | Cypher/Gremlin 새로운 쿼리 언어 학습 필요 |
| **틈새 요건** | 진정한 다중 홉 관계가 없으면 RDBMS 대비 우위 없음 |

📢 **섹션 요약 비유**: 그래프 DB는 관계 탐정이다. 수십 단계로 얽힌 복잡한 관계망에서 빠르게 범인(의심 계좌, 추천 상품)을 찾아내지만, 단순한 숫자 집계(회계 장부 합산)는 일반 스프레드시트(RDBMS)가 더 빠르다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| Cypher 쿼리 언어 | Neo4j의 그래프 패턴 매칭 쿼리 언어 |
| Amazon Neptune | AWS 완전 관리형 그래프 DB |
| 지식 그래프 | 그래프 DB 기반 AI 추론 데이터 구조 |
| FDS (사기 탐지) | 그래프 관계망 분석의 핵심 사용 사례 |
| 추천 엔진 | 협업 필터링을 그래프로 구현 |
| SPARQL | RDF 지식 그래프 쿼리 언어 (Neptune 지원) |
| 폴리글랏 퍼시스턴스 | RDBMS + 그래프 DB 함께 쓰는 전략 |

### 👶 어린이를 위한 3줄 비유 설명
1. 그래프 DB는 친구 관계 지도다. 점(노드)은 사람이고, 선(엣지)은 친구 관계다. "친구의 친구를 소개해줘"라는 요청에, 선만 따라가면 바로 찾을 수 있다.
2. Neo4j의 Cypher 쿼리는 보물찾기 지도 읽기다. "A에서 출발해서 B를 거쳐 C까지 가는 길을 찾아라"처럼, 패턴을 그림으로 그리듯 쿼리를 작성한다.
3. 사기 탐지에서 그래프 DB는 거미줄 탐지기다. 의심스러운 계좌(점)가 여러 단계의 송금(선)으로 연결된 거미줄 패턴을 빠르게 발견해, 직접 연결되지 않은 의심 계좌도 찾아낸다.
