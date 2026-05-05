+++
weight = 126
title = "PACELC 정리 (PACELC Theorem)"
date = "2024-05-22"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: PACELC 정리 (PACELC Theorem)은(는) 관계형 데이터베이스의 확장 한계를 넘어 분산 환경에 맞는 일관성·성능·유연성을 선택하게 하는 저장 기술이다.
> **비유**: 한 종류의 서랍장 대신 용도별 보관함을 골라 쓰는 공구실과 같다.

📝 모범 답안

## 1. 개요 및 필요성

1. **정상 시의 고민:** CAP 정리는 네트워크 장애(P)라는 극단적인 상황에만 집중함. 하지만 실제 시스템 운영 시간의 99.9%는 네트워크가 정상임.
2. **복합적 선택:** 2012년 대니얼 아바디(Daniel Abadi)가 제안한 PACELC는 "장애 시(P) A와 C 중 무엇을 택할지, 장애가 없을 때(E) L과 C 중 무엇을 택할지"를 통합함.

---

## 2. 구성요소

- **PACELC Theorem Logic & Sequential Selection**
```text
[ If Partition (P) ] --- Yes ---         |
         No (Else, E)
         |
[ If Normal (E) ] ----------- [ Choose L or C ] (Latency vs Consistency)

[ PACELC Breakdown ]
P : Partition (네트워크 단절)
A : Availability (가용성)
C : Consistency (일관성)
E : Else (정상 상황)
L : Latency (지연 시간)
C : Consistency (일관성)
```

1. **PA/EL (Availability + Latency focus):**
   - 장애 시 가용성 선택, 정상 시 응답 속도 선택. (예: DynamoDB, Cassandra). 성능 최우선.
2. **PC/EC (Consistency + Consistency focus):**
   - 장애 시 일관성 선택, 정상 시에도 일관성 선택. (예: BigTable, MongoDB). 정합성 최우선.
3. **PC/EL (Consistency + Latency focus):**
   - 장애 시 일관성을 지키지만, 정상 시에는 속도를 위해 일관성을 약간 타협함. (예: VoltDB).
4. **PA/EC (Availability + Consistency focus):**
   - 장애 시 가용성을 유지하되, 정상 시에는 일관성을 위해 지연을 감수함.

---

## 3. 구조 및 원리

**핵심 조건**: 일관성 수준, 파티셔닝, 복제, 접근 패턴을 함께 선택해야 한다.

동작 순서:
| 비교 항목 | CAP 정리 (기존) | PACELC 정리 (확장) |
| :--- | :--- | :--- |
| **핵심 질문** | 장애 시 무엇을 선택할 것인가? | 장애 시와 정상 시 각각 무엇을 선택할 것인가? |
| **범위** | 특수한 고장 상황 | 전체 운영 상황 (정상 + 장애) |
| **추가 변수** | 없음 | Latency (지연 시간) |
| **이론적 초점** | 분산 환경의 가용 한계 | 성능과 정합성의 조율 |
| **주요 활용** | NoSQL의 기본 분류 | NoSQL의 옵션 튜닝 (Consistency Level 설정 등) |

---

## 4. 비교 및 연결

1. **일관성 수준 (Consistency Level) 튜닝 (Strategy):**
   - 카산드라(Cassandra)와 같은 DB는 `QUORUM` 설정을 통해 PC/EC를 추구할 수도 있고, `ONE` 설정을 통해 PA/EL을 추구할 수도 있음. 즉, PACELC는 개발자가 런타임에 내리는 설정 결정을 정당화함.
2. **기술사적 판단:** 현대 시스템은 "단일 정답"이 없음. 동일한 데이터베이스 내에서도 '사용자 로그인 정보'는 PC/EC로, '게시글 조회수'는 PA/EL로 처리하는 등 **업무 특성에 따른 세밀한 세분화 설계**가 기술사의 진정한 실력임.

---

## 5. 실무 적용 및 판단

1. **기대효과:** 시스템이 정상일 때 발생하는 지연 시간(Latency)의 원인을 수학적으로 이해하고, 비즈니스 성능 목표(SLA)를 달성하기 위한 구조적 근거를 제공함.
2. **결론:** PACELC는 CAP의 이상적인 논의를 실무적인 엔지니어링의 영역으로 끌어내린 이론임. 이를 통해 우리는 시스템의 평상시와 비상시를 모두 아우르는 강건한 아키텍처를 설계할 수 있음.

---

## 6. 기대효과 및 결론

PACELC 정리 (PACELC Theorem)은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. NoSQL 선택은 정답 찾기가 아니라 업무 패턴에 맞는 일관성과 확장성의 균형점을 고르는 일이다.

---

## 7. 발전 흐름도

```text
[상위 개념: 분산 데이터베이스 이론]
    │
    ▼
[하위 개념: 지연 시간(Latency), 정합성 수준 (Consistency Level)]
    │
    ▼
[연관 개념: CAP 정리, BASE 원칙, 쿼럼(Quorum)]
```

이 흐름도는 상위 개념: 분산 데이터베이스 이론에서 출발해 연관 개념: CAP 정리, BASE 원칙, 쿼럼(Quorum)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

- **상위 개념:** 분산 데이터베이스 이론
- **하위 개념:** 지연 시간(Latency), 정합성 수준 (Consistency Level)
- **연관 개념:** CAP 정리, BASE 원칙, 쿼럼(Quorum)
