+++
weight = 8
title = "08. CAP 정리 & PACELC"
date = "2026-05-17"
[extra]
categories = "gisulsa-database"
+++

# 🎯 CAP 정리 & PACELC 이론

> **별점**: ★★★★★ | ★134회 기출

## 1. CAP 정리 (Brewer's Theorem)

분산 시스템은 **동시에 3가지를 모두 보장할 수 없다**.

| 속성 | 의미 |
|------|------|
| **C** (Consistency) | 모든 노드가 동시에 같은 데이터 |
| **A** (Availability) | 모든 요청에 응답 (오류 없이) |
| **P** (Partition Tolerance) | 네트워크 분할 시에도 동작 |

```
[분산 DB 선택]
CA 시스템: 단일 서버 RDBMS (분산 환경 불가)
CP 시스템: HBase, Zookeeper, MongoDB (일관성 우선, 분할 시 가용성 포기)
AP 시스템: Cassandra, DynamoDB, CouchDB (가용성 우선, 최종 일관성)

실제: P는 필수 → CP vs AP 선택이 핵심
```

## 2. PACELC — CAP의 확장

```
[PACELC 모델]
P가 있을 때 (Partition): A(가용성) vs C(일관성)
P가 없을 때 (Else):      L(지연) vs C(일관성)

예시:
- MySQL (PA/EL): 분산 시 가용성, 정상 시 지연 낮음
- DynamoDB (PA/EL): 가용성 + 낮은 지연 우선
- HBase (PC/EC): 일관성 + 일관성 (항상 강한 일관성)
- CockroachDB (PC/EC): NewSQL, 강한 일관성
```

## 3. 최종 일관성 (Eventual Consistency)

```
AP 시스템의 일관성 보장 방식:
- 모든 업데이트는 결국 모든 노드에 전파됨
- 읽기 시 일시적 불일치 허용
- 벡터 클럭 / 버전 벡터로 충돌 해결
```

## 4. 답안 포인트

**3단락**: ① CAP 정리 3가지 속성 & 왜 동시 불가 → ② CP vs AP 시스템 선택 기준 → ③ PACELC로 지연 고려 & NewSQL 등장

## 5. 관련 개념

`NoSQL(★133회)` → AP 시스템 대표 | `분산DB 투명성(★131회)` → 위치·분할·복제 투명성 | `NewSQL` → CA+P 시도
