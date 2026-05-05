+++
weight = 183
title = "183. 데이터 손실 제로 아키텍처 (Zero Data Loss Architecture)"
date = "2026-04-21"
[extra]
categories = "studynote-devops-sre"
+++

## 0. 핵심 인사이트

> **핵심**: RPO=0(Recovery Point Objective = 0)은 "장애 시 데이터 손실이 전혀 없어야 한다"는 최고 수준의 데이터 보호 요구사항으로, 동기식 복제(Synchronous Replication)와 분산 트랜잭션이 핵심 기술이다.
> **비유**: RPO=0은 마치 두 장소에 동시에 저장되는 금고 — 어느 쪽이 터져도 나머지 한 곳에 완전한 내용이 남아있어, 단 한 줄의 기록도 사라지지 않는다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

데이터 손실은 단순한 기술 문제가 아니라 비즈니스 생존 문제다. 2022년 Gartner 조사에 따르면 IT 다운타임의 평균 비용은 분당 5,600달러이며, 금융 거래 데이터나 의료 기록의 손실은 직접 비용 외에 법적 제재와 브랜드 손상으로 이어진다.

RPO(Recovery Point Objective)는 "장애 발생 시 얼마나 오래된 데이터까지 손실을 허용하는가"를 정의한다. RPO=24시간은 하루치 데이터 손실을 허용하고, RPO=0은 트랜잭션 하나도 잃지 않겠다는 의미다. 비용과 복잡도는 RPO가 0에 가까울수록 지수적으로 증가한다.

Zero Data Loss 아키텍처의 핵심은 쓰기 작업이 완료되기 전에 적어도 2개 이상의 물리적으로 분리된 위치에 데이터가 기록되었음을 보장하는 것이다. 이를 위해 동기식 복제(Synchronous Replication), Raft/Paxos 기반 분산 합의(Distributed Consensus), WAL(Write-Ahead Log) 동기 전송이 사용된다.

RPO=0을 달성하더라도 RTO(Recovery Time Objective)는 별도로 관리해야 한다. 데이터는 손실이 없어도 복구 시간이 길면 서비스 중단 시간이 길어진다. Zero Data Loss + 빠른 페일오버(Failover)를 함께 구현하는 것이 완전한 비즈니스 연속성 아키텍처다.

---

## 2. 구성요소

### Zero Data Loss 구현 패턴

```
【동기식 복제 (Synchronous Replication)】

클라이언트
    │ 쓰기 요청
    ▼
┌──────────────┐
│  Primary DB   │
│  1. WAL 기록  │
│  2. 복제 전송 │──────────────→ ┌──────────────┐
│  3. ACK 대기  │ ← ─ ─ ─ ─ ─ ─│  Replica DB  │
│  4. 커밋 완료 │   복제 ACK 수신 │  WAL 수신    │
└──────────────┘               └──────────────┘
    │
    │ 커밋 완료 응답 (양쪽 기록 확인 후)
    ▼
  클라이언트

【분산 합의 기반 (Raft 예시)】

┌──────────┐    ┌──────────┐    ┌──────────┐
│ Leader   │───→│ Follower1│    │ Follower2│
│ (Primary)│←───│          │    │          │
│          │───────────────────→│          │
│  쿼럼 ACK│←───────────────────│          │
│  (2/3 후 │                   │          │
│   커밋)  │                   │          │
└──────────┘                   └──────────┘
  quorum = floor(N/2) + 1
  N=3 → 2개 ACK 필요
```

### RPO 수준별 기술 매핑

| RPO 목표 | 기술 | 비용 | 레이턴시 영향 |
|:---|:---|:---|:---|
| RPO=0 | 동기 복제, Raft 합의 | 매우 높음 | +수ms~수십ms |
| RPO<1분 | 반동기 복제 (Semi-sync) | 높음 | +1~10ms |
| RPO<5분 | 비동기 복제 + 짧은 간격 | 중간 | 미미 |
| RPO<1시간 | 시간별 스냅샷 | 낮음 | 없음 |
| RPO<24시간 | 일별 백업 | 매우 낮음 | 없음 |

### RPO/RTO Matrix

| 구분 | 설명 | 달성 기술 |
|:---|:---|:---|
| RPO=0, RTO≈0 | 무중단 + 무손실 | Active-Active 다중화 |
| RPO=0, RTO>0 | 무손실 + 수동 페일오버 | 동기 복제 + 수동 전환 |
| RPO>0, RTO≈0 | 빠른 복구 + 소량 손실 | 비동기 복제 + 자동 페일오버 |
| RPO>0, RTO>0 | 백업 복원 | 정기 백업 |

---

## 3. 구조 및 원리

**핵심 조건**: 측정 가능한 SLI, 합의된 SLO, 실행 가능한 경보·복구 절차가 하나의 폐쇄 루프를 이뤄야 한다.

동작 순서:
1. 사용자 경험을 대표하는 지표를 선택해 서비스 상태를 수치화한다.
2. 허용 가능한 목표치와 에러 버짓을 정해 변화 속도와 안정성의 기준선을 만든다.
3. 메트릭·로그·트레이스로 이상 징후를 탐지하고 원인을 빠르게 국소화한다.
4. 장애 이후 포스트모템과 자동화를 통해 토일을 줄이고 재발 방지책을 시스템에 반영한다.

```text
서비스 요청
   ↓
측정(SLI)
   ↓
목표(SLO)·예산
   ↓
알림·복구
   ↓
학습·자동화
```

### 데이터베이스별 Zero Data Loss 구현

| DB | 구현 방식 | 특이사항 |
|:---|:---|:---|
| PostgreSQL | Synchronous Streaming Replication | `synchronous_commit=on` |
| MySQL/Aurora | Semi-Synchronous Replication | 최소 1개 Replica ACK 필요 |
| TiDB/CockroachDB | Raft 기반 내장 합의 | 네이티브 RPO=0 |
| Oracle | Data Guard Maximum Protection | 전통 엔터프라이즈 표준 |
| Kafka | `acks=all` + ISR | 메시지 큐 레벨 보장 |

---

## 4. 비교 및 연결

| 항목 | 동기 복제 | 비동기 복제 |
|:---|:---|:---|
| RPO | 0 | RPL(Replication Lag)만큼 손실 가능 |
| 쓰기 레이턴시 | 복제 왕복 시간 추가 | 추가 없음 |
| Replica 장애 영향 | Primary 쓰기 차단 | Primary 계속 운영 |
| 지리적 분산 | 제한적 (레이턴시 증가) | 가능 |

### PostgreSQL 동기 복제 설정 예시

```sql
-- postgresql.conf
synchronous_commit = on          -- 기본값, 동기 복제 활성화
synchronous_standby_names = 'FIRST 1 (replica1, replica2)'
-- 최소 1개 Replica에 WAL 전달 확인 후 커밋

-- 성능과 RPO 균형을 위한 옵션
-- synchronous_commit = remote_write  → 디스크 쓰기 전 ACK (약간 빠름)
-- synchronous_commit = remote_apply  → 적용 완료 후 ACK (가장 안전)
```

---

## 5. 실무 적용 및 판단

| 시나리오 | 설계 결정 | 이유 |
|:---|:---|:---|
| 금융 거래 시스템 | RPO=0, 동기 복제 + Active-Active | 법적 요구사항, 0 손실 |
| 이커머스 주문 | RPO<1분, 반동기 복제 | 비용·성능 균형 |
| 분석 데이터 | RPO<1시간, 비동기 복제 | 손실 허용, 성능 우선 |
| 로그 데이터 | RPO<24시간, 일별 스냅샷 | 재현 가능, 비용 최소화 |
| 멀티 리전 | Active-Active + CRDT | 지리적 분산, 충돌 해결 |

Zero Data Loss 아키텍처는 금융·의료·법률 분야의 핵심 시스템에서 선택이 아닌 필수다. 데이터 손실 한 건이 몇십억 원의 손해로 이어질 수 있는 환경에서, 동기 복제와 분산 합의 프로토콜의 레이턴시 비용(수 ms)은 충분히 정당화된다.

한계로는 동기 복제가 Replica 네트워크 장애 시 Primary 쓰기 차단을 유발할 수 있다는 점과, 지리적으로 멀리 분산된 복제에서는 레이턴시가 수십 ms까지 증가해 쓰기 성능에 심각한 영향을 줄 수 있다는 점이다. 이를 해결하기 위해 지역별 Primary와 복제 지연 허용 정책(Degraded Mode)을 함께 설계해야 한다.

향후 eBPF 기반 커널 레벨 복제 최적화, NVMe-oF 원격 직접 메모리 접근, 지속성 메모리(Persistent Memory) 활용으로 동기 복제의 레이턴시 비용이 더욱 줄어들어 RPO=0이 더 광범위한 시스템에 적용 가능해질 것이다.

---

## 6. 기대효과 및 결론

데이터 손실 제로 아키텍처 (Zero Data Loss Architecture)을(를) 도입하면 자동화와 표준화를 통해 속도·안정성·가시성의 균형을 높일 수 있다. 다만 효과를 얻으려면 측정 가능한 SLI, 합의된 SLO, 실행 가능한 경보·복구 절차가 하나의 폐쇄 루프를 이뤄야 한다는 전제가 충족되어야 하며, 도구만 도입하고 운영 원칙을 바꾸지 않으면 기대 효과가 빠르게 한계에 부딪힌다.

결론적으로 데이터 손실 제로 아키텍처 (Zero Data Loss Architecture)은(는) 개별 기능이 아니라 운영 체계 전체의 품질을 재정렬하는 방식이며, 향후에는 플랫폼화·정책화·AI 기반 최적화와 결합해 더 높은 수준의 자동 운영으로 확장된다.

---

## 7. 발전 흐름도

```text
전통 운영 모니터링
    ↓
SRE 지표화
    ↓
옵저버빌리티 확장
    ↓
카오스·자동 복구
    ↓
AIOps·예측 운영
```

---

## 8. 관련 개념 맵

| 분류 | 관련 개념 |
|:---|:---|
| 상위 개념 | 비즈니스 연속성 (BCP), 재해 복구 (DR), RPO/RTO |
| 연관 기술 | Raft 합의 알고리즘, WAL (Write-Ahead Log), 동기 복제, Semi-sync 복제 |
| 비교 대상 | 동기 복제 vs 비동기 복제, RPO=0 vs RPO>0, Active-Active vs Active-Standby |
