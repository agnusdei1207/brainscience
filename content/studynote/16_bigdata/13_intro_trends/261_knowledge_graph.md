+++
title = "049. 지식 그래프 — Knowledge Graph"
weight = 261
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 지식 그래프 — Knowledge Graph은(는) 빅데이터 전략과 거시적 변화 방향을 이해하기 위한 정책·시장·기술 트렌드 개념이다.
> **비유**: 멀리서 지형과 조류를 함께 보며 데이터 산업의 큰 흐름을 읽는 전망대와 같다.

📝 모범 답안

## 1. 개요 및 필요성

```
지식 그래프 (Knowledge Graph):
  개체(Entity) + 관계(Relation) = 그래프

삼중항 (Triple: S-P-O):
  Subject - Predicate - Object
  
  예:
  (구글, 설립자, 래리 페이지)
  (래리 페이지, 국적, 미국)
  (구글, 본사위치, 마운틴뷰)
  (마운틴뷰, 위치국가, 미국)

그래프 구조:
  노드: 개체 (구글, 래리 페이지, 마운틴뷰)
  엣지: 관계 (설립자, 국적, 본사위치)
  
  래리 페이지 → (설립) → 구글
  래리 페이지 → (국적) → 미국
  구글 → (본사) → 마운틴뷰

RDF (Resource Description Framework):
  W3C 표준 형식
  
  <구글> <설립자> <래리 페이지> .
  <래리 페이지> <국적> <미국> .
  
  SPARQL: RDF 쿼리 언어
  
  "구글 설립자의 국적은?"
  SELECT ?country
  WHERE {
    <구글> <설립자> ?founder .
    ?founder <국적> ?country .
  }

온톨로지 (Ontology):
  지식 그래프의 스키마/개념 계층
  
  클래스: 사람, 회사, 장소
  속성: 이름, 설립일, 위치
  관계: 설립자, 소속, 위치
  
  OWL (Web Ontology Language): W3C 표준
```

---

## 2. 구성요소

```
주요 지식 그래프:

1. Google Knowledge Graph (2012):
   20 billion 팩트, 570 million 개체
   검색 결과 오른쪽 "지식 패널" 제공
   
   기능:
   "아인슈타인" 검색 → 생년, 국적, 업적 즉시 표시
   "파리" → 에펠탑, 루브르, 인구, 날씨 연결

2. Wikidata (2012, Wikimedia):
   오픈 지식 그래프
   100M+ 개체, 1.4B+ 삼중항
   
   SPARQL 쿼리:
   "1950년 이후 태어난 한국 대통령 목록"

3. DBpedia:
   Wikipedia에서 자동 추출한 지식 그래프
   구조화되지 않은 Wikipedia → 트리플

4. Freebase → Wikidata:
   Google이 인수 후 Wikidata로 통합

5. 도메인 특화:
   의료: SNOMED-CT, UMLS
   금융: FIBO (금융 산업 온톨로지)
   법률: LegalKG
   기업: 각 회사 내부 엔터프라이즈 KG

지식 그래프 구축 방법:
  수동 큐레이션: 높은 품질, 낮은 확장성
  자동 추출 (NLP): 텍스트에서 관계 추출
  크라우드소싱: 위키피디아, Wikidata
  하이브리드: 자동 추출 + 인간 검증
```

---

## 3. 구조 및 원리

**핵심 조건**: 정책, 거버넌스, 플랫폼 구조, 산업 활용 방향을 함께 읽어야 한다.

동작 순서:
```
지식 그래프 임베딩 (KGE):
  개체와 관계를 연속 벡터 공간에 표현
  
  목적:
  유사한 개체 → 가까운 벡터
  관계 추론 → 벡터 연산으로

TransE (2013):
  핵심 아이디어:
  head + relation ≈ tail
  
  (파리, 수도, 프랑스)
  V(파리) + V(수도) ≈ V(프랑스)
  
  비유:
  V(왕) - V(남성) + V(여성) ≈ V(여왕)  ← Word2Vec과 유사!
  
  학습: 올바른 트리플의 score를 높임
  score = -||h + r - t||

관계 추론:
  "구글의 CEO는?" → 지식 그래프에 없는 경우
  
  V(구글) + V(CEO) → 가장 가까운 개체 = V(순다 피차이)
  
  링크 예측 (Link Prediction):
  누락된 관계 자동 예측
  → 지식 그래프 완성

응용:
  추천 시스템: "이 영화 좋아하면 → 같은 감독 추천"
  질의응답: "설명 가능한" 추론 경로 제공
  이상 탐지: 비정상적 관계 탐지
```

---

## 4. 비교 및 연결

```
Graph RAG (Knowledge Graph + RAG):
  벡터 검색의 한계를 지식 그래프로 보완

벡터 RAG 한계:
  "삼성의 반도체 사업부 CEO는 누구인가?"
  → 벡터 검색: 관련 문서 5개 검색
  → 문서에 명시적 답변이 없으면 실패
  → LLM 환각 가능

Graph RAG 강점:
  (삼성전자, has_division, 반도체사업부)
  (반도체사업부, has_ceo, 경계현)
  
  → 그래프 탐색으로 정확한 답변
  → 추론 경로 설명 가능: "삼성전자 → 반도체사업부 → CEO"

구현 방식:

Microsoft GraphRAG (2024):
  1. 문서 → NLP → 개체/관계 추출 → 지식 그래프 구축
  2. 질의 → 그래프 탐색 + 벡터 검색 결합
  3. 두 결과 통합 → LLM 답변 생성
  
  Community Detection: Leiden 알고리즘
  계층적 요약 생성 (Global Search)

Neo4j + LLM:
  CYPHER 쿼리 자동 생성:
  "삼성의 반도체 CEO는?" →
  MATCH (c:Company)-[:HAS_DIVISION]->(d:Division)-[:HAS_CEO]->(p:Person)
  WHERE c.name = '삼성'
  RETURN p.name

장점:
  다단계 추론 가능
  답변 추론 경로 투명
  도메인 지식 명시적 구조화

단점:
  지식 그래프 구축 비용
  갱신 지연 (KG 최신화 어려움)
```

---

## 5. 실무 적용 및 판단

```
글로벌 은행 금융 지식 그래프 구축:

배경:
  AML (Anti-Money Laundering) 탐지 강화
  단순 규칙 기반 → 복잡한 관계망 탐지 불가
  
  기존 문제:
  A → B → C → D (4단계 간접 송금)
  규칙 기반: A-D 직접 연결 없어 탐지 불가

지식 그래프 구축:

개체:
  Person, Company, Account, Transaction
  Country, HighRiskCountry

관계:
  OWNS_ACCOUNT, CONTROLS_COMPANY
  SENDS_TO, RELATED_TO, LOCATED_IN
  IS_SANCTIONED, IS_HIGH_RISK

데이터 소스 통합:
  핵심 뱅킹 DB → 계좌, 거래
  KYC 데이터 → 고객 신원, 관계사
  OFAC 제재 리스트 → 제재 개체
  Panama Papers 데이터 (오픈) → 페이퍼 컴퍼니

구현 (Neo4j):
  MATCH path = (suspicious:Account)-
               [:SENDS_TO*2..5]-
               (target:Account)
  WHERE suspicious.country IN ['고위험국가']
  AND ALL(tx IN relationships(path)
          WHERE tx.amount > 10000)
  RETURN path, length(path)

결과:
  "4홉 이내 간접 연결" 탐지:
  직접 탐지 불가했던 네트워크 5개 발견
  의심 계좌 탐지율: 34% → 89%
  허위 양성(False Positive): 12% 감소
  
  Graph ML 추가:
  GNN(그래프 신경망)으로 패턴 학습
  → 새로운 자금 세탁 패턴 자동 탐지
```

---

## 6. 기대효과 및 결론

지식 그래프 — Knowledge Graph은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 거시 트렌드는 개별 제품 비교보다 데이터 산업 구조가 어디로 이동하는지 판단하게 해 주는 기준점이다.

---

## 7. 발전 흐름도

```
[시맨틱 웹 (1999, Tim Berners-Lee)]
RDF, OWL 표준
링크드 데이터
      |
      v
[Freebase (2007)]
최초 대규모 KG
위키피디아 연계
      |
      v
[Google Knowledge Graph (2012)]
검색 혁신
지식 패널 도입
      |
      v
[지식 그래프 임베딩 (2013~)]
TransE 등장
관계 추론 가능
      |
      v
[Graph RAG (2024)]
LLM + 지식 그래프
환각 방지, 추론 투명성
```

## 👶 어린이를 위한 3줄 비유 설명

1. 지식 그래프 = 세상 관계도 — "래리 페이지→설립→구글", "구글→본사→마운틴뷰". 개체와 관계를 연결한 거대한 네트워크!
2. KGE = 개체를 별자리에 배치 — 비슷한 것(서울, 도쿄)은 가깝게. V(서울)+V(수도)≈V(한국). 벡터 연산으로 관계 추론!
3. Graph RAG = 지식 맵 안내원 — 벡터 검색(광범위 검색)으로 못 찾을 때 지식 그래프(관계 지도)로 논리적 탐색. 추론 경로 설명 가능!

---

## 8. 관련 개념 맵

```
지식 그래프 (Knowledge Graph)
+-- 기본 구조
|   +-- 삼중항 (S-P-O)
|   +-- RDF, SPARQL
|   +-- 온톨로지 (OWL)
+-- 주요 KG
|   +-- Google KG, Wikidata
|   +-- 도메인 특화 KG
+-- 임베딩
|   +-- TransE, RotatE
|   +-- 링크 예측
+-- 응용
|   +-- Graph RAG
|   +-- AML 탐지
|   +-- 추천 시스템
+-- 도구
    +-- Neo4j, Amazon Neptune
    +-- RDFlib, Stardog
```
