+++
weight = 40
title = "40. CAP 정리 (CAP Theorem)"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: CAP 정리(CAP Theorem, Brewer 2000)는 분산 데이터베이스 시스템이 일관성(Consistency)·가용성(Availability)·파티션 내성(Partition Tolerance) 세 가지를 동시에 완벽히 보장할 수 없으며, 파티션(네트워크 분리)은 실제 환경에서 불가피하므로 CP 또는 AP 중 하나를 선택해야 한다는 근본 제약이다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

CAP 정리 (CAP Theorem)은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
CAP 정리의 세 속성:

C (Consistency, 일관성):
  모든 노드가 동시에 같은 데이터를 봄
  읽기 요청 -> 항상 최신 데이터 반환
  "강한 일관성 (Strong Consistency)"

A (Availability, 가용성):
  모든 요청에 응답 (성공/실패 상관없이)
  응답이 없거나 타임아웃 없음
  "항상 응답"

P (Partition Tolerance, 파티션 내성):
  네트워크 분리 시에도 시스템 계속 동작
  메시지 손실/지연이 발생해도 작동

핵심 결론:
  P는 분산 시스템에서 포기 불가 (현실적으로 발생)
  따라서 CP or AP 선택
  
  CA 시스템 = 실질적으로 단일 노드 (분산 아님)
```

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```
CP (Consistency + Partition Tolerance):

특성:
  파티션 발생 시 -> 가용성 희생
  일부 요청에 "오류/타임아웃" 반환
  -> 잘못된 데이터 반환보다 오류 선호

대표 시스템:
  HBase:
    HDFS 기반 컬럼 스토어
    강한 일관성 (단일 리전)
    Zookeeper로 분산 코디네이션
    
  MongoDB (기본 설정):
    Primary-Secondary 복제
    Primary 장애 시 쓰기 차단 (일시적)
    
  ZooKeeper:
    분산 코디네이션 서비스
    리더 선출, 설정 관리
    Paxos 합의 알고리즘 기반

사용 케이스:
  금융 거래 (이중 인출 방지 필수)
  재고 관리 (마이너스 재고 방지)
  예약 시스템 (중복 예약 방지)
```

---

## 3. 구조 및 원리

**핵심 조건**: CAP 정리 (CAP Theorem)은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```
AP (Availability + Partition Tolerance):

특성:
  파티션 발생 시 -> 일관성 희생
  모든 요청에 응답 (최신이 아닐 수 있음)
  결과적 일관성 (Eventual Consistency)
  "나중에는 동기화됨"

대표 시스템:
  Cassandra (AP 기본):
    멀티 마스터, 모든 노드 동등
    일관성 수준 조정 가능 (ONE, QUORUM, ALL)
    파티션 시에도 계속 쓰기 허용
    
  DynamoDB:
    AWS 관리형 NoSQL
    기본 Eventually Consistent
    옵션으로 Strong Consistent 선택 가능
    
  CouchDB:
    멀티 마스터 복제
    충돌 감지 + 자동 해결 정책

사용 케이스:
  SNS 좋아요 수 (약간 틀려도 괜찮음)
  쇼핑몰 장바구니
  콘텐츠 캐싱 레이어
```

---

## 4. 비교 및 연결

```
PACELC (Daniel Abadi, 2012):
CAP의 한계를 보완한 확장 모델

CAP 한계:
  파티션 없을 때의 트레이드오프 설명 불가
  
PACELC:
  Partition 발생 시:
    A (Availability) vs C (Consistency)
    (= CAP와 동일)
  
  Else (파티션 없을 때):
    L (Latency) vs C (Consistency)

핵심: 파티션 없어도 일관성을 높이면 지연 증가

분류:
  PA/EL: Cassandra (가용성 + 저지연)
  PC/EC: HBase (일관성 우선)
  PA/EC: MongoDB (기본)
  PC/EL: ZooKeeper (강한 일관성, 높은 지연 허용)

실무 함의:
  "우리 시스템은 CAP에서 C vs A"뿐 아니라
  "정상 상태에서도 Latency vs Consistency" 고려 필요
```

---

## 5. 실무 적용 및 판단

```
이커머스 데이터베이스 설계 CAP 선택:

요구사항 분석:
  주문/결제: 절대 이중 처리 불가 -> CP 선택
  상품 재고: 마이너스 재고 방지 -> CP 선택
  장바구니: 약간의 불일치 허용 -> AP 선택
  상품 조회: 최신 가격 아니어도 OK -> AP 선택
  리뷰/댓글: 결과적 일관성 충분 -> AP 선택

데이터 저장소 선택:
  주문 DB: PostgreSQL (RDBMS, 강한 일관성)
  재고 DB: Redis + 분산 락 (Redlock)
  장바구니: DynamoDB (AP, 고가용성)
  상품 카탈로그: Elasticsearch (검색, AP)
  세션: Redis Cluster

Black Friday 트래픽 시나리오:
  상품 조회 트래픽 100배 급증
  -> AP 카탈로그 DB: 문제 없이 확장
  
  재고 차감 동시 요청 급증
  -> CP 재고 DB: 락 경합 증가 -> 일부 지연
  -> 해결: 재고 사전 예약 + 배치 차감

결론: 데이터 성격별 CP/AP 혼합 아키텍처
```

---

## 6. 기대효과 및 결론

CAP 정리 (CAP Theorem)의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```
[분산 시스템 연구 (1980s)]
Lamport Clock, Byzantine Fault
      |
      v
[CAP 추측 (Brewer, 2000)]
PODC 키노트 발표
      |
      v
[CAP 수학적 증명 (2002)]
Gilbert & Lynch 논문
      |
      v
[NoSQL 움직임 (2009~)]
Cassandra, MongoDB, DynamoDB
CAP 기반 설계 패턴 실용화
      |
      v
[PACELC 모델 (Abadi, 2012)]
CAP 한계 보완
      |
      v
[현재: 뉴SQL / 분산 SQL]
CockroachDB, Spanner: CP + 글로벌 분산
"CAP를 우회"하는 Paxos/Raft 기반 설계
```

---

## 8. 관련 개념 맵

```
CAP 정리 (CAP Theorem)
+-- 세 속성
|   +-- C (Consistency)
|   +-- A (Availability)
|   +-- P (Partition Tolerance)
+-- 시스템 유형
|   +-- CP: HBase, MongoDB, ZooKeeper
|   +-- AP: Cassandra, DynamoDB, CouchDB
+-- 확장 모델
|   +-- PACELC (Latency vs Consistency)
+-- 일관성 모델
    +-- Strong Consistency
    +-- Eventual Consistency
    +-- Read-your-writes, Monotonic Read
```
