+++
weight = 145
title = "NUMA-인식 스레드 스케줄링"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

# NUMA-인식 스레드 스케줄링 (NUMA-Aware Thread Scheduling)

## Ⅰ. NUMA 아키텍처 개념

### 1. NUMA (Non-Uniform Memory Access)

NUMA는 다중 프로세서 시스템에서 각 CPU가 로컬 메모리를 가지며, 다른 CPU의 메모리(원격 메모리)에 접근할 때 더 큰 지연이 발생하는 아키텍처다. 대규모 서버 시스템(4소켓 이상)의 표준 구조다.

> **비유:** 각 방에 자기 책상(로컬 메모리)이 있지만, 옆방 책상(원격 메모리)에서 물건을 가져올 때는 더 오래 걸리는 기숙사와 같다.

```
┌──────────── NUMA 아키텍처 개요 ────────────┐
│                                               │
│  NUMA Node 0           NUMA Node 1            │
│  ┌──────────────┐     ┌──────────────┐       │
│  │  Local Mem 0  │     │  Local Mem 1  │       │
│  │  (16GB)       │     │  (16GB)       │       │
│  └──────┬───────┘     └──────┬───────┘       │
│         │                     │                 │
│  ┌──────┴───────┐     ┌──────┴───────┐       │
│  │ P0  P1  P2  P3│     │ P4  P5  P6  P7│       │
│  └──────────────┘     └──────────────┘       │
│         │                     │                 │
│         └──Interconnect──┘                   │
│          (QPI/UPI/HyperTransport)             │
│                                               │
│  로컬 접근: ~80ns                             │
│  원격 접근: ~150~200ns (2~3배 느림)          │
│                                               │
└───────────────────────────────────────────────┘
```

### 2. 로컬 메모리 vs 원격 메모리

| 구분 | 설명 | 지연 시간 | 대역폭 |
|------|------|-----------|--------|
| **로컬 메모리** | 동일 NUMA 노드의 메모리 | 낮음 (~80ns) | 높음 |
| **원격 메모리** | 다른 NUMA 노드의 메모리 | 높음 (~150ns+) | 낮음 |

```
┌────────── 로컬 vs 원격 메모리 접근 ──────────┐
│                                                │
│  CPU(P0)의 메모리 요청:                         │
│                                                │
│  [로컬 접근]                                   │
│  P0 ──> Local Mem 0: 80ns ──> 데이터 획득     │
│         ★ 빠름, 대역폭 충분                    │
│                                                │
│  [원격 접근]                                   │
│  P0 ──> Interconnect ──> Remote Mem 1          │
│         150~200ns + 대역폭 경합 ──> 데이터     │
│         ▲ 느림, 인터커넥트 병목 가능           │
│                                                │
└────────────────────────────────────────────────┘
```

## Ⅱ. NUMA 인식 스케줄링 기법

### 1. 스케줄링 원칙

NUMA 인식 스케줄링의 핵심은 스레드를 해당 스레드가 사용하는 메모리와 동일한 NUMA 노드에서 실행하도록 배치하는 것이다.

```
┌────────── NUMA 인식 스케줄링 최적화 ─────────┐
│                                               │
│  최적 배치 (NUMA-aware):                      │
│  Node 0: Thread-A + Mem-A (동일 노드)         │
│  Node 1: Thread-B + Mem-B (동일 노드)         │
│                                               │
│  ┌──────────┐    ┌──────────┐                 │
│  │ Th-A+Mem │    │ Th-B+Mem │                 │
│  │ (Node 0) │    │ (Node 1) │                 │
│  └──────────┘    └──────────┘                 │
│                                               │
│  비최적 배치 (NUMA-unaware):                   │
│  Node 0: Thread-A 실행                        │
│  Node 0의 Thread-A가 Node 1의 Mem-B 접근       │
│  -> 인터커넥트를 통한 원격 접근 발생           │
│                                               │
└───────────────────────────────────────────────┘
```

### 2. 메모리 정책 설정

| 정책 | API/명령어 | 설명 |
|------|------------|------|
| **기본 (Local)** | `set_mempolicy(MPOL_DEFAULT)` | 로컬 노드 메모리 우선 할당 |
| **바인드 (Bind)** | `set_mempolicy(MPOL_BIND)` | 지정 노드에서만 할당 |
| **선호 (Preferred)** | `set_mempolicy(MPOL_PREFERRED)` | 지정 노드 선호, 부족 시 타 노드 |
| **인터리브 (Interleave)** | `set_mempolicy(MPOL_INTERLEAVE)` | 여러 노드에 번갈아 할당 |
| **mbind** | `mbind()` | 특정 메모리 영역에 정책 적용 |

```c
#include <numaif.h>
#include <numa.h>

// 전체 프로세스 메모리를 Node 0에 바인딩
unsigned long nodemask = 1UL << 0;  // Node 0
set_mempolicy(MPOL_BIND, &nodemask, MAXNODES);

// 특정 메모리 영역을 Node 0, 1에 인터리브
unsigned long nodemask2 = (1UL << 0) | (1UL << 1);
mbind(ptr, size, MPOL_INTERLEAVE, &nodemask2, MAXNODES, 0);
```

## Ⅲ. numactl과 AutoNUMA

### 1. numactl 명령어

```
┌────────────── numactl 사용법 ──────────────┐
│                                               │
│  # 하드웨어 NUMA 정보 확인                    │
│  numactl --hardware                           │
│                                               │
│  # 특정 노드에서 프로세스 실행                 │
│  numactl --cpunodebind=0 --membind=0 ./app    │
│                                               │
│  # 선호 노드 지정                              │
│  numactl --preferred=0 ./app                  │
│                                               │
│  # 인터리브 정책                               │
│  numactl --interleave=0,1 ./app               │
│                                               │
│  # 현재 프로세스의 NUMA 정보 확인              │
│  numastat -p <PID>                            │
│                                               │
└───────────────────────────────────────────────┘
```

### 2. AutoNUMA 자동 균형

리눅스 커널의 AutoNUMA 기능은 자동으로 메모리 페이지를 자주 접근하는 노드로 마이그레이션한다.

```
┌────────────── AutoNUMA 동작 원리 ──────────────┐
│                                                   │
│  1. 초기 상태:                                    │
│     Thread-X (Node 0) ──> Mem-P (Node 1) 원격   │
│                                                   │
│  2. 커널이 원격 접근 빈도 모니터링               │
│     PFN (Page Frame Number) 당 접근 통계 수집    │
│                                                   │
│  3. 임계치 초과 시 자동 마이그레이션:             │
│     Mem-P를 Node 1에서 Node 0으로 이동            │
│     Thread-X (Node 0) ──> Mem-P (Node 0) 로컬   │
│                                                   │
│  4. 설정:                                         │
│     /proc/sys/kernel/numa_balancing = 1 (활성화)  │
│     /proc/sys/kernel/numa_balancing_scan_period   │
│                                                   │
└───────────────────────────────────────────────────┘
```

> **비유:** AutoNUMA는 도서관에서 자주 쓰는 책을 멀리 있는 서가에서 내 자리 옆으로 자동으로 옮겨주는 도서관 사서와 같다.

## Ⅳ. 성능 영향

### 1. 메모리 집약적 워크로드의 영향

```
┌───────── 성능 비교: NUMA-aware vs Unaware ──────┐
│                                                    │
│  워크로드: 대규모 인메모리 데이터베이스            │
│  (256GB 메모리, 4 NUMA 노드, 64코어)              │
│                                                    │
│  ┌─────────────────────────────────────────┐      │
│  │ throughput (ops/sec)                     │      │
│  │                                          │      │
│  │  NUMA-aware  ████████████████████  100%  │      │
│  │  NUMA-blind  ████████             55%   │      │
│  │  AutoNUMA    ████████████████     85%   │      │
│  │                                          │      │
│  └─────────────────────────────────────────┘      │
│                                                    │
│  원격 메모리 접근: 2~3배 지연                       │
│  대규모 시스템에서는 1.5~3배 성능 차이              │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 2. 성능 영향 요인

| 요인 | 영향 정도 | 설명 |
|------|-----------|------|
| **메모리 접근 패턴** | 매우 큼 | 순차적 vs 랜덤 접근 |
| **데이터 크기** | 큼 | L3 캐시를 초과하는 경우 영향 극대화 |
| **스레드 수** | 중간 | 노드당 스레드 밸런스 |
| **인터커넥트 대역폭** | 큼 | QPI/UPI 대역폭에 따라 원격 접근 비용 변동 |

## Ⅴ. 지식 그래프

```
NUMA-인식 스레드 스케줄링
├── NUMA 아키텍처
│   ├── Non-Uniform Memory Access
│   ├── 다중 노드, 각 노드에 로컬 메모리
│   ├── 로컬 접근 (~80ns) vs 원격 접근 (~150ns+)
│   └── 인터커넥트 (QPI/UPI)로 노드 간 통신
├── NUMA 인식 스케줄링 기법
│   ├── 스레드와 메모리를 동일 노드에 배치
│   ├── first-touch 정책 (초기 접근 노드에 할당)
│   └── 페이지 마이그레이션 (동적 재배치)
├── 메모리 정책
│   ├── set_mempolicy() (프로세스 전체)
│   ├── mbind() (특정 메모리 영역)
│   ├── MPOL_BIND, MPOL_PREFERRED, MPOL_INTERLEAVE
│   └── numactl 명령행 도구
├── AutoNUMA 자동 균형
│   ├── 커널이 원격 접근 통계 자동 수집
│   ├── 빈번한 원격 페이지를 로컬로 마이그레이션
│   └── numa_balancing 커널 파라미터
├── 성능 영향
│   ├── 메모리 집약적 워크로드: 2~3배 차이
│   ├── 대규모 데이터베이스, HPC에 중요
│   └── 인터커넥트 대역폭이 병목
└── 최적화 전략
    ├── numactl로 수동 노드 바인딩
    ├── first-touch 초기화 패턴 사용
    └── AutoNUMA 활성화 + 모니터링
```

---

## 약어 정리

| 약어 | Full Name |
|------|-----------|
| **NUMA** | Non-Uniform Memory Access |
| **QPI** | QuickPath Interconnect |
| **UPI** | Ultra Path Interconnect |
| **HPC** | High-Performance Computing |
| **PFN** | Page Frame Number |
| **MPOL** | Memory Policy |

---

## 3줄 어린이 설명
컴퓨터가 아주 커져서 여러 그룹으로 나뉘면, 각 그룹마다 자기 메모리를 가집니다.
가까운 메모리를 쓰면 빠르지만 멀리 있는 메모리를 쓰면 느려요.
그래서 일꾼과 메모리를 같은 그룹에 배치하면 2~3배나 빨라집니다.
