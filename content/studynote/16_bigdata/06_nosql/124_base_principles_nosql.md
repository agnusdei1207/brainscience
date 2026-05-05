+++
weight = 124
title = "BASE 원칙 (Basically Available, Soft State, Eventual Consistency)"
date = "2024-05-22"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: BASE 원칙 (Basically Available, Soft State, Eventual Consistency)은(는) 관계형 데이터베이스의 확장 한계를 넘어 분산 환경에 맞는 일관성·성능·유연성을 선택하게 하는 저장 기술이다.
> **비유**: 한 종류의 서랍장 대신 용도별 보관함을 골라 쓰는 공구실과 같다.

📝 모범 답안

## 1. 개요 및 필요성

1. **RDBMS의 한계:** 전통적인 ACID(원자성, 일관성, 고립성, 지속성)는 데이터의 무결성을 보장하지만, 수천 개의 서버가 연결된 빅데이터 환경에서는 성능 저하와 가용성 하락을 유발함.
2. **BASE의 탄생:** 대규모 웹 서비스(Amazon, Google)에서 수평 확장(Scale-out)을 위해 일관성을 "결과적"으로 타협하되, 가용성을 극대화하는 새로운 트랜잭션 모델이 필요하게 됨.

---

## 2. 구성요소

- **BASE Principle Workflow & Distributed Replication**
```text
[ Data Write (Node A) ]      [ Propagation Delay ]      [ Data Read (Node B) ]
+---------------------+      +-------------------+      +---------------------+
| Value = 10 (Update) | --- (Asynchronous Sync) ---+---------------------+                                 +---------------------+
                                       |                           |
                                       |                           v
                                       |                (Eventually Consistency)
                                       +--------------> | Value = 10 (Synced) |
                                                        +---------------------+
[ Key Pillars of BASE ]
1. BA: Basically Available (기본적 가용성)
2. S : Soft State (소프트 스테이트)
3. E : Eventual Consistency (결과적 일관성)
```

1. **Basically Available (BA):**
   - 시스템의 일부분에 장애가 발생하더라도, 전체 시스템이 멈추지 않고 기본적인 응답을 제공함. 완벽한 응답은 아니더라도 가용한 상태를 유지함.
2. **Soft State (S):**
   - 데이터의 상태가 외부의 입력 없이도 시간이 지남에 따라 변할 수 있음. 노드 간 동기화가 진행 중일 때, 특정 시점의 데이터는 "확정된 상태"가 아닐 수 있음을 의미함.
3. **Eventual Consistency (E):**
   - 특정 시간 동안 새로운 업데이트가 없다면, 결국 모든 복제본(Replica)은 동일한 값으로 수렴함. 일시적인 불일치를 허용하여 성능 병목을 제거함.

---

## 3. 구조 및 원리

**핵심 조건**: 일관성 수준, 파티셔닝, 복제, 접근 패턴을 함께 선택해야 한다.

동작 순서:
| 비교 항목 | ACID (RDBMS) | BASE (NoSQL) | 융합 분석 |
| :--- | :--- | :--- | :--- |
| **핵심 가치** | 일관성 (Consistency) | 가용성 (Availability) | ACID는 신뢰성, BASE는 성능 |
| **시스템 상태** | 강한 일관성 (Strong) | 결과적 일관성 (Eventual) | 데이터 중요도에 따라 혼용 |
| **트랜잭션 관리** | 비관적 락 (Pessimistic) | 낙관적 방식 (Optimistic) | 동시성 제어 방식의 차이 |
| **확장성** | 수직 확장 (Scale-up) | 수평 확장 (Scale-out) | 빅데이터 처리는 수평 확장이 대세 |
| **사용 사례** | 금융, 결제, 인사 관리 | SNS, 로그, 카트, 댓글 | 정합성 vs 실시간성 선택 |

---

## 4. 비교 및 연결

1. **비즈니스 도메인별 선택 (Strategy):**
   - **SNS 뉴스피드:** 친구의 글이 1초 늦게 보여도 문제없으므로 BASE가 적합함.
   - **계좌 이체:** 1원이라도 틀리면 치명적이므로 반드시 ACID를 유지해야 함.
2. **기술사적 판단:** 현대 아키텍처는 "Polyglot Persistence"를 지향함. 주문 정보는 RDBMS(ACID)에, 대량의 상품 조회 로그는 NoSQL(BASE)에 저장하여 성능과 안전성을 동시에 확보하는 것이 핵심 설계 역량임.

---

## 5. 실무 적용 및 판단

1. **기대효과:** 전 지구적 규모의 분산 시스템(Global Distribution)에서 지연 시간(Latency)을 최소화하고, 무한한 확장을 가능하게 하여 현대 인터넷 서비스의 기술적 근간이 됨.
2. **결론:** BASE는 일관성을 포기한 것이 아니라, 성능을 위해 "일관성의 시점"을 늦춘 지혜로운 타협임. 분산 데이터베이스 설계자는 BASE 원칙을 통해 서비스 가용성의 임계치를 돌파할 수 있음.

---

## 6. 기대효과 및 결론

BASE 원칙 (Basically Available, Soft State, Eventual Consistency)은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. NoSQL 선택은 정답 찾기가 아니라 업무 패턴에 맞는 일관성과 확장성의 균형점을 고르는 일이다.

---

## 7. 발전 흐름도

```text
[상위 개념: 분산 데이터베이스, NoSQL]
    │
    ▼
[하위 개념: 결과적 일관성, 가용성 (Availability)]
    │
    ▼
[연관 개념: CAP 정리, PACELC 이론, ACID]
```

이 흐름도는 상위 개념: 분산 데이터베이스, NoSQL에서 출발해 연관 개념: CAP 정리, PACELC 이론, ACID까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

- **상위 개념:** 분산 데이터베이스, NoSQL
- **하위 개념:** 결과적 일관성, 가용성 (Availability)
- **연관 개념:** CAP 정리, PACELC 이론, ACID
