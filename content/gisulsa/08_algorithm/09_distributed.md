+++
weight = 9
title = "09. 분산 알고리즘 & 합의"
date = "2026-05-17"
[extra]
categories = "gisulsa-algorithm"
+++

# 분산 알고리즘 & 합의 프로토콜

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

정의: 분산 시스템은 다음 3가지를 동시 만족 불가
C (Consistency): 모든 노드가 동일한 데이터 응답
A (Availability): 모든 요청에 항상 응답

### Ⅱ. 핵심 구성요소

```
정의: 분산 시스템은 다음 3가지를 동시 만족 불가

C (Consistency): 모든 노드가 동일한 데이터 응답
A (Availability): 모든 요청에 항상 응답
P (Partition Tolerance): 네트워크 분할 시에도 동작

→ 실제: P는 포기 불가 → CA or CP 선택

[분류 예시]
CP 시스템: HBase, Zookeeper, Redis (클러스터)
  → 일관성 우선, 분할 시 가용성 희생
  
CA 시스템 (이론적): 단일 노드 (분할 없음 가정)

AP 시스템: Cassandra, CouchDB, DynamoDB
  → 가용성 우선, 최종 일관성

PACELC 정리 (CAP 확장):
  분할 없을 때도: 지연(L) vs 일관성(C) 트레이드오프
```
```
[Paxos]
분산 시스템 합의 문제 해결 (Lamport)
단계: Prepare → Promise → Accept → Accepted
Leader 기반, 다수결(쿼럼) 동의

[Raft]
Paxos보다 이해하기 쉬운 합의 알고리즘
역할: Leader / Follower / Candidate


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
