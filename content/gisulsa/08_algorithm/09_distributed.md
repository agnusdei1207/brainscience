+++
weight = 9
title = "09. 분산 알고리즘 & 합의"
date = "2026-05-17"
[extra]
categories = "gisulsa-algorithm"
+++

# 🎯 분산 알고리즘 & 합의 프로토콜

> **별점**: ★★★★★ | 기본 필수

## 1. CAP 정리

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

## 2. 합의 프로토콜

```
[Paxos]
분산 시스템 합의 문제 해결 (Lamport)
단계: Prepare → Promise → Accept → Accepted
Leader 기반, 다수결(쿼럼) 동의

[Raft]
Paxos보다 이해하기 쉬운 합의 알고리즘
역할: Leader / Follower / Candidate
리더 선출 → 로그 복제 → 커밋

[etcd]: Raft 기반 분산 KV
  K8s 클러스터 상태 저장

[Zookeeper]: Zab 프로토콜 (Paxos 기반)
  분산 코디네이션 (Kafka, Hadoop)
```

## 3. 분산 트랜잭션

```
[2PC (2-Phase Commit)]
Coordinator가 모든 참가자에게 준비/커밋
원자성 보장, BUT:
  블로킹: Coordinator 장애 시 참가자 대기
  단일 장애점

[사가 패턴 (Saga Pattern)]
각 서비스 로컬 트랜잭션 + 보상 트랜잭션
Choreography: 이벤트 기반 (Kafka)
Orchestration: 중앙 사가 오케스트레이터

MSA 환경의 표준 분산 트랜잭션 패턴
```

## 4. 답안 포인트

**3단락**: ① CAP 정리 & CP/AP 시스템 분류 → ② Raft 합의 & etcd/K8s 활용 → ③ 사가 패턴 & 2PC MSA 비교

## 5. 관련 개념

`MSA(★133회)` → 사가 패턴 실무 | `데이터베이스(05과목)` → ACID vs BASE | `K8s(13_cloud)` → etcd Raft 사용
