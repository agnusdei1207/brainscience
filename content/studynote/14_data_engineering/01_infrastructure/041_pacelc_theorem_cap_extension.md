+++
weight = 41
title = "41. PACELC 정리 (PACELC Theorem)"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: PACELC(파셀크) 정리는 Daniel Abadi(2012)가 CAP 정리의 한계를 극복하기 위해 제안한 확장 모델로, 파티션 발생 시(P) 가용성(A)/일관성(C) 트레이드오프 외에 정상 상태에서도 지연(L, Latency)/일관성(C, Consistency) 트레이드오프가 존재함을 명시한다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

PACELC 정리 (PACELC Theorem)은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
CAP 정리 복습:
  C (Consistency): 모든 노드가 동일한 최신 데이터
  A (Availability): 항상 응답 (부분 노드 실패 무관)
  P (Partition Tolerance): 네트워크 분단 내성

CAP: 파티션 상황에서 C vs A 중 하나만 선택

CAP의 한계:
  1. 파티션은 실제로 매우 드문 상황
  2. 파티션이 없을 때의 트레이드오프는?
  3. Latency(지연)를 다루지 않음

실제 분산 시스템의 고민:
  "파티션 없을 때도 복제 일관성 vs 낮은 지연
   사이에서 선택이 필요하다"

PACELC 등장 배경:
  Daniel Abadi (Yale, 2012)
  CAP을 정상 상태(Else 조건)까지 확장
```

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```
PACELC 정리:

P (Partition 발생 시):
  A (Availability) vs C (Consistency)
  
E (Else, 정상 상태):
  L (Latency) vs C (Consistency)

전체 표기: PA/EL, PC/EL, PA/EC, PC/EC

PA/EL (가용성 + 저지연 우선):
  파티션: 가용성 선택 (일부 불일치 허용)
  정상:   저지연 선택 (복제 지연 허용)
  예: DynamoDB, Cassandra, Riak

PC/EC (일관성 우선):
  파티션: 일관성 선택 (가용성 포기)
  정상:   일관성 선택 (지연 감수)
  예: HBase, VoltDB, BigTable

PA/EC (혼합):
  파티션: 가용성, 정상: 일관성
  예: MongoDB (기본값: 가용성 우선)
  
PC/EL (혼합):
  드문 조합, 일부 NewSQL 시도
```

---

## 3. 구조 및 원리

**핵심 조건**: PACELC 정리 (PACELC Theorem)은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```
분산 데이터베이스 PACELC 분류:

PA/EL (가용성 + 저지연):
  DynamoDB: 글로벌 테이블, 최종 일관성 기본
  Cassandra: AP 설계, Tunable Consistency
  Riak: 최종 일관성 중심
  Voldemort (LinkedIn): 가용성 극대화
  
PC/EC (일관성 우선):
  HBase: HDFS 기반, 강한 일관성
  VoltDB: ACID, 분산 트랜잭션
  Zookeeper: 메타데이터 일관성 보장
  
PA/EC (가용성 우선, 정상 일관성):
  MongoDB: replica set, 기본 primary 읽기
  
PC/EL:
  드문 조합

RDBMS (분산 상황):
  MySQL Cluster: PC/EC 시도
  
NewSQL:
  CockroachDB: PC/EC + 분산 트랜잭션
  Google Spanner: PC/EC (TrueTime 활용)
  YugabyteDB: PC/EC (Raft 합의)

Tunable Consistency (Cassandra):
  QUORUM: 과반수 노드 응답 요구
  ALL: 전체 노드 응답 (강한 일관성)
  ONE: 1개 응답 (최저 지연)
```

---

## 4. 비교 및 연결

```
PACELC 기반 DB 선택 기준:

PA/EL 선택 상황:
  - 전 세계 사용자, 낮은 지연 필수
  - 일시적 불일치 허용 (SNS, 추천, 장바구니)
  - 높은 쓰기 처리량 필요
  예: 쇼핑몰 상품 추천, 소셜 피드

PC/EC 선택 상황:
  - 금융 거래, 재고 차감 (이중 청구 불허)
  - 의료 기록 (불일치 위험)
  - 강한 읽기-쓰기 일관성 필요
  예: 결제 시스템, 계좌 이체

혼합 사용 (폴리글랏 퍼시스턴스):
  결제: CockroachDB (PC/EC)
  장바구니: DynamoDB (PA/EL)
  사용자 세션: Redis (PA/EL)
  분석: Cassandra (PA/EL)

Eventual Consistency vs Strong Consistency:
  최종 일관성(PA/EL):
    모든 노드가 결국(eventually) 동기화
    "언제 동기화될지" 보장 없음
    
  강한 일관성(PC/EC):
    모든 읽기가 최신 쓰기 반영
    Raft, Paxos 합의 알고리즘 필요
    지연 증가 (Round-trip 추가)
```

---

## 5. 실무 적용 및 판단

```
글로벌 이커머스 C사 DB 설계:

요구사항:
  - 전 세계 50개국, 사용자 1억 명
  - 재고 차감: 이중 판매 절대 불가
  - 상품 카탈로그: 빠른 조회 필요
  - 사용자 장바구니: 짧은 지연 필요
  - 결제: ACID 트랜잭션 필수
  - 추천 시스템: 1초 이내 응답

PACELC 기반 DB 선택:

재고/결제 (PC/EC):
  Google Spanner
  이유: 전 세계 분산 + ACID + 강한 일관성
  비용: 높음, 지연: 중간

상품 카탈로그 (PA/EL):
  DynamoDB Global Tables
  이유: 저지연(~5ms), 최종 일관성 허용
  
장바구니 (PA/EL):
  Cassandra (DC별 복제)
  이유: 고가용성, 로컬 저지연

사용자 세션 (PA/EL):
  Redis Cluster
  이유: 인메모리, 1ms 미만 지연

추천 시스템 (PA/EL):
  Cassandra + 피처 스토어
  이유: 대규모 쓰기, 저지연 읽기

결과:
  재고 이중 판매 0건 (PC/EC 효과)
  상품 조회 P99: 12ms (PA/EL 효과)
  글로벌 가용성: 99.995%
```

---

## 6. 기대효과 및 결론

PACELC 정리 (PACELC Theorem)의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```
[CAP 정리 (Brewer, 2000)]
분산 시스템 기초 이론
네트워크 파티션 시 트레이드오프
      |
      v
[PACELC 정리 (Abadi, 2012)]
Latency 차원 추가
정상 상태 트레이드오프 명시화
      |
      v
[Tunable Consistency (Cassandra)]
QUORUM/ALL/ONE 선택 가능
애플리케이션이 일관성 수준 결정
      |
      v
[NewSQL 등장 (2015~)]
CockroachDB, Spanner (PC/EC + 분산)
SQL + 분산 + 강한 일관성 시도
      |
      v
[현재: 폴리글랏 퍼시스턴스]
한 서비스에 여러 DB 혼합
도메인별 PACELC 최적 선택
```

---

## 8. 관련 개념 맵

```
PACELC 정리
+-- 기반
|   +-- CAP 정리 (Brewer, 2000)
|   +-- Daniel Abadi 확장 (2012)
+-- 분류
|   +-- PA/EL: DynamoDB, Cassandra
|   +-- PC/EC: HBase, Spanner, CockroachDB
+-- 핵심 개념
|   +-- Eventual Consistency
|   +-- Strong Consistency (Raft/Paxos)
|   +-- Tunable Consistency
+-- 선택 기준
    +-- 금융/재고: PC/EC
    +-- 피드/추천: PA/EL
    +-- 폴리글랏: 혼합
```
