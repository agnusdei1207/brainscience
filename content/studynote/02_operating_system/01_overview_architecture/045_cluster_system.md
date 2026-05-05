+++
title = "045. 클러스터 시스템 — Cluster System"
weight = 45
date = "2026-04-05"
[extra]
categories = "studynote-operating-system"
+++

## 0. 핵심 인사이트

> **핵심**: 클러스터 시스템 — Cluster System은(는) 운영체제가 자원을 추상화하고 통제하는 과정에서 성능, 보호, 응답성을 동시에 조율하기 위해 필요한 핵심 개념이다.
> **비유**: 클러스터 시스템 — Cluster System은(는) 복잡한 교통을 한 번에 통제해 전체 흐름을 맞추는 신호 체계와 같다.

---

📝 모범 답안

## 1. 개요 및 필요성

```
클러스터 시스템 구조:

노드 1         노드 2         노드 3
┌──────┐       ┌──────┐       ┌──────┐
│ CPU  │       │ CPU  │       │ CPU  │
│ RAM  │       │ RAM  │       │ RAM  │
│ OS   │       │ OS   │       │ OS   │
└──┬───┘       └──┬───┘       └──┬───┘
   │              │              │
   └──────────────┼──────────────┘
                  │
        고속 네트워크 (InfiniBand, 10/100G Ethernet)

공유 스토리지:
  SAN (Storage Area Network) 또는 NAS/분산 파일시스템

클러스터 미들웨어:
  - 노드 모니터링
  - 작업 분배 (Job Scheduler)
  - 페일오버 관리
  - 공유 자원 조율

유형:
  HA 클러스터: 고가용성 (Active-Standby, Active-Active)
  HPC 클러스터: 고성능 계산 (병렬 처리)
  부하 분산 클러스터: Load Balancing
```

> 📢 **섹션 요약 비유**: 클러스터는 팀 프로젝트 — 한 명의 천재(단일 대형 서버) 대신 여러 명이 팀(노드 집합)으로 협력. 한 명 빠져도(장애) 팀은 계속 작동!

---

## 2. 구성요소

```
HA 클러스터 (High Availability Cluster):

Active-Standby (능동-대기):
  Active Node: 실제 서비스 처리
  Standby Node: 대기 (Heartbeat 모니터링)

  장애 감지:
  Active → Heartbeat 중단
  Standby → 장애 감지 → Failover

  Failover 절차:
  1. VIP (Virtual IP) Standby로 이전
  2. 공유 스토리지 마운트
  3. 서비스 프로세스 시작
  → 서비스 재개 (다운타임: 수십 초~수 분)

Active-Active (능동-능동):
  모든 노드가 서비스 처리
  부하 분산 + 고가용성 동시 달성

  한 노드 장애 → 나머지 노드가 부하 흡수

  조건: 각 노드가 독립적으로 서비스 가능해야 함
  (무상태 서비스, DB의 경우 공유 스토리지 필요)

Split-Brain 문제:
  네트워크 단절 → 두 노드 모두 Active 주장
  → 데이터 충돌

  해결: Quorum (쿼럼) 디스크/노드
  과반수 투표 방식으로 Active 결정

HA 소프트웨어:
  Linux: Pacemaker + Corosync
  Windows: WSFC (Windows Server Failover Clustering)
  오픈소스: Keepalived (L4 레벨 VIP 관리)
```

> 📢 **섹션 요약 비유**: HA 클러스터는 이중화 전원 — 메인 전원(Active)이 끊기면 자동으로 예비 전원(Standby)으로 전환. Split-Brain은 두 전원이 동시에 켜지는 쇼트 방지!

---

## 3. 구조 및 원리

**핵심 조건**: 운영체제의 해당 메커니즘은 현재 상태 정보, 자원 제약, 정책 기준이 함께 정합성을 가질 때 안정적으로 동작한다.

동작 순서:
1. **요청 또는 이벤트 발생**: 사용자 요청, 인터럽트, 시스템 호출 등으로 커널이 해당 기능을 처리할 필요가 생긴다.
2. **현재 상태 확인**: 커널은 큐, 제어 블록, 메타데이터, 자원 가용량을 확인해 실행 가능 여부와 우선순위를 판단한다.
3. **정책 적용 및 자원 배정**: 해당 주제의 핵심 정책에 따라 상태 전이, 자원 할당, 보호 검사를 수행한다.
4. **결과 반영 및 후속 처리**: 처리 결과를 시스템 상태에 기록하고 다음 인터럽트·스케줄링·복구 단계로 연결한다.

```
HPC 클러스터 (High-Performance Computing):

구성 요소:
  헤드 노드 (Head/Login Node): 작업 제출, 관리
  컴퓨트 노드 (Compute Node): 실제 계산 수행
  스토리지 노드: 공유 데이터 저장

  고속 인터커넥트:
  InfiniBand: 200 Gbps, 초저지연 (< 1 μs)
  OmniPath: Intel 고속 패브릭

작업 스케줄러:
  SLURM (Simple Linux Utility for Resource Management):
  - 노드 할당, 작업 큐 관리

  sbatch job.sh        # 작업 제출
  squeue               # 큐 상태 확인
  scontrol show node   # 노드 상태

병렬 프로그래밍:
  MPI (Message Passing Interface): 노드 간 통신
  OpenMP: 노드 내 스레드 병렬화
  Hybrid: MPI + OpenMP

  MPI 예시 (개념):
  Rank 0 (Master): 데이터 분할 → 전송
  Rank 1~N: 계산 → 결과 반환 (MPI_Reduce)

활용 분야:
  기상 예보, 분자 동역학, 유체 역학
  핵 시뮬레이션, 딥러닝 학습 (GPU 클러스터)

  Top500 슈퍼컴퓨터 = 초대형 HPC 클러스터
```

> 📢 **섹션 요약 비유**: HPC 클러스터는 수학 마라톤 팀 — 복잡한 계산(마라톤)을 여러 팀원(컴퓨트 노드)이 구간 나눠 달리고(병렬), 결과를 합쳐 빠른 답을 내요!

---

## 4. 비교 및 연결

```
HPC 클러스터 (High-Performance Computing):

구성 요소:
  헤드 노드 (Head/Login Node): 작업 제출, 관리
  컴퓨트 노드 (Compute Node): 실제 계산 수행
  스토리지 노드: 공유 데이터 저장

  고속 인터커넥트:
  InfiniBand: 200 Gbps, 초저지연 (< 1 μs)
  OmniPath: Intel 고속 패브릭

작업 스케줄러:
  SLURM (Simple Linux Utility for Resource Management):
  - 노드 할당, 작업 큐 관리

  sbatch job.sh        # 작업 제출
  squeue               # 큐 상태 확인
  scontrol show node   # 노드 상태

병렬 프로그래밍:
  MPI (Message Passing Interface): 노드 간 통신
  OpenMP: 노드 내 스레드 병렬화
  Hybrid: MPI + OpenMP

  MPI 예시 (개념):
  Rank 0 (Master): 데이터 분할 → 전송
  Rank 1~N: 계산 → 결과 반환 (MPI_Reduce)

활용 분야:
  기상 예보, 분자 동역학, 유체 역학
  핵 시뮬레이션, 딥러닝 학습 (GPU 클러스터)

  Top500 슈퍼컴퓨터 = 초대형 HPC 클러스터
```

> 📢 **섹션 요약 비유**: HPC 클러스터는 수학 마라톤 팀 — 복잡한 계산(마라톤)을 여러 팀원(컴퓨트 노드)이 구간 나눠 달리고(병렬), 결과를 합쳐 빠른 답을 내요!

---

## 5. 실무 적용 및 판단

```
비교: SMP, NUMA, 클러스터

              SMP             NUMA            클러스터
OS 이미지     단일             단일            복수 (노드별)
메모리 공유   공유             분산 공유       분산 독립
통신          공유 버스        메모리 버스      네트워크 메시지
확장성        낮음 (수십 코어) 중간            높음 (수천 노드)
프로그래밍    쉬움 (스레드)    보통            어려움 (메시지)
지연시간      최저             낮음            높음
장애 격리     낮음             중간            높음 (노드 독립)

선택 기준:
  SMP: 단일 OS 환경, 수십 코어, 높은 공유 데이터
  NUMA: 수백 코어, 메모리 지역성 최적화 필요
  클러스터: 수천 노드, 고가용성 필수, 대규모 처리량

실제 사례:
  웹 서버 팜: 부하 분산 클러스터 (Nginx + HAProxy)
  DB 서버: HA 클러스터 (Active-Standby)
  과학 계산: HPC 클러스터 (SLURM + MPI)
  빅데이터: Hadoop/Spark 클러스터
```

> 📢 **섹션 요약 비유**: SMP는 한 팀원이 여러 손(코어), NUMA는 여러 팀원이 책상 공유, 클러스터는 독립 사무실(노드)로 분리된 팀 — 분리될수록 확장성은 높지만 소통(네트워크) 비용도 증가!

---

## 6. 기대효과 및 결론

```
대규모 전자상거래 클러스터 (일 1,000만 주문):

웹 계층 (부하 분산 클러스터):
  L4 로드밸런서: HAProxy 2대 (Active-Active)
  → 웹 서버 10대 (Nginx + Node.js)
  VIP: 10.0.0.1 (Keepalived)

애플리케이션 계층:
  마이크로서비스 클러스터 (Kubernetes)
  - 주문 서비스: 20 pod
  - 결제 서비스: 10 pod
  자동 스케일링: HPA (Horizontal Pod Autoscaler)

DB 계층 (HA 클러스터):
  MySQL InnoDB Cluster (3노드):
    Primary: RW
    Secondary × 2: RO + 자동 Failover

  Redis Sentinel (3노드):
    Master: 쓰기
    Replica × 2: 읽기 + Sentinel 모니터링

스토리지:
  Ceph 분산 스토리지 클러스터
  이미지/파일: 3-way 복제

장애 시나리오:
  DB Primary 장애 →
  Sentinel 감지 (30s) →
  Secondary 자동 승격 →
  애플리케이션 자동 재연결

SLA: 99.99% 가용성 (연간 다운타임 52분)
```

> 📢 **섹션 요약 비유**: 전자상거래 클러스터는 대형마트 운영 — 계산대(웹)·창고(DB)·물류(앱)마다 여러 직원(노드), 한 명 쉬어도(장애) 나머지가 커버, 손님(트래픽) 몰려도 직원 추가(스케일아웃)!

---

## 7. 발전 흐름도

```
[초기 클러스터 (1990s)]
Beowulf 클러스터 (상용 PC + Linux)
HPC 목적
      |
      v
[HA 클러스터 상용화 (2000s)]
RHCS, Veritas Cluster
엔터프라이즈 고가용성
      |
      v
[클라우드/가상화 (2010s)]
VMware vSphere HA
AWS Auto Scaling
      |
      v
[컨테이너 클러스터 (2014~)]
Kubernetes: 컨테이너 오케스트레이션
마이크로서비스 클러스터 표준
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 클러스터 시스템 — Cluster System | 운영체제 자원 관리와 보호 정책이 실제로 적용되는 핵심 주제 |
| 커널 (Kernel) | 정책 집행, 상태 전이, 시스템 호출 처리의 중심 |
| 프로세스/스레드 | CPU, 메모리, 동기화 자원과 직접 연결되는 실행 단위 |
| 메모리/I/O | 성능 병목과 보호 요구사항이 함께 드러나는 연계 영역 |
| 가상화/보안 | 격리, 제어, 관측 확장 관점에서 해당 주제가 연결되는 상위 개념 |
