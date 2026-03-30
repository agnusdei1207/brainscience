+++
weight = 143
title = "스레드 고정 Thread Affinity/Pinning"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

# 스레드 고정 Thread Affinity/Pinning

## Ⅰ. 개념 및 정의

### 1. 스레드 어피니티 (Thread Affinity)

스레드 어피니티는 특정 스레드를 특정 CPU 코어에 바인딩(고정)하는 기법이다. 운영체제의 스케줄러가 스레드를 임의로 마이그레이션하는 것을 방지하여 성능을 최적화한다.

> **비유:** 한 직원에게 항상 같은 작업대를 배정하면, 도구 위치를 기억해 작업 속도가 빨라지는 것과 같다.

```
┌───────────── 스레드 고정 (Pinning) ─────────────┐
│                                                   │
│   스레드-1  ───────  코어-0 (고정)               │
│   스레드-2  ───────  코어-1 (고정)               │
│   스레드-3  ───────  코어-2 (고정)               │
│                                                   │
│   OS 스케줄러 마이그레이션 불가 (Hard)            │
│                                                   │
└───────────────────────────────────────────────────┘

┌─────────── 스레드 자유 이동 (기본) ──────────────┐
│                                                   │
│   스레드-1  ──> 코어-0 ──> 코어-2 ──> 코어-1    │
│   스레드-2  ──> 코어-1 ──> 코어-0 ──> 코어-3    │
│                                                   │
│   OS 스케줤러가 임의로 이동                       │
│   캐시 미스 증가 가능                              │
│                                                   │
└───────────────────────────────────────────────────┘
```

### 2. 소프트 어피니티 vs 하드 어피니티

| 구분 | 정의 | 강제성 |
|------|------|--------|
| **Soft Affinity** | OS가 이전 코어를 선호하도록 힌트 제공 | 권장, 강제 아님 |
| **Hard Affinity** | 특정 코어에 강제 바인딩 | 강제, 다른 코어 이동 불가 |

```
┌─────────────── Soft vs Hard Affinity ───────────────┐
│                                                      │
│  Soft Affinity:                                      │
│  ┌─────────┐    (선호)    ┌──────────┐              │
│  │ Thread 1 │ ─────────> │  Core 0  │              │
│  └─────────┘              └──────────┘              │
│       │           (가능하면 다른 코어도 사용)          │
│       └──────────────> Core 2 (부하 시)              │
│                                                      │
│  Hard Affinity:                                      │
│  ┌─────────┐    (강제)    ┌──────────┐              │
│  │ Thread 1 │ ══════════ │  Core 0  │              │
│  └─────────┘              └──────────┘              │
│       │           (다른 코어 사용 불가)               │
│       ╳──────> Core 2 (금지)                         │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Ⅱ. 구현 방법

### 1. 리눅스 시스템 콜

**`sched_setaffinity()`**: 프로세스/스레드의 CPU 어피니티 마스크를 설정한다.

```
┌────────── CPU Affinity Mask (4-Core) ───────────┐
│                                                    │
│  Bit:    [3]  [2]  [1]  [0]                      │
│  Core:    3    2    1    0                        │
│                                                    │
│  Mask = 0x03 (0000 0011) -> Core 0, 1만 허용      │
│  Mask = 0x05 (0000 0101) -> Core 0, 2만 허용      │
│  Mask = 0x0F (0000 1111) -> 모든 코어 허용        │
│                                                    │
└────────────────────────────────────────────────────┘
```

```c
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>

void set_thread_affinity(int core_id) {
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(core_id, &cpuset);

    // 현재 스레드를 core_id에 고정
    pthread_setaffinity_np(pthread_self(),
                           sizeof(cpu_set_t), &cpuset);
}
```

### 2. 명령행 도구

| 도구 | 용도 | 예시 |
|------|------|------|
| **taskset** | 프로세스 CPU 마스크 설정 | `taskset -c 0,1 ./app` |
| **cgroups cpuset** | 컨테이너/그룹 CPU 할당 | `cgcreate -g cpuset:/mygroup` |
| **numactl** | NUMA 노드 + CPU 바인딩 | `numactl --cpunodebind=0 ./app` |
| **pthread_setaffinity_np** | 스레드 단위 바인딩 (C API) | `CPU_SET(0, &cpuset)` |

### 3. cgroups cpuset

```
┌──────── cgroups cpuset 계층 구조 ────────┐
│                                            │
│  /sys/fs/cgroup/cpuset/                    │
│  ├── root/                                 │
│  │   ├── cpuset.cpus = "0-7"              │
│  │   └── cpuset.mems = "0-1"              │
│  ├── realtime/                             │
│  │   ├── cpuset.cpus = "0-3"              │
│  │   └── cpuset.mems = "0"                │
│  └── batch/                                │
│      ├── cpuset.cpus = "4-7"              │
│      └── cpuset.mems = "1"                │
│                                            │
└────────────────────────────────────────────┘
```

> **비유:** cgroups cpuset은 공장의 작업 구역을 나누어, 실시간 작업은 정밀 기계 구역에, 일반 작업은 대량 생산 구역에 배정하는 것과 같다.

## Ⅲ. 성능 이점

### 1. 캐시 웜스 (Cache Warmth)

스레드가 동일 코어에서 실행되면 L1/L2 캐시 데이터가 유효하여 캐시 히트율이 향상된다.

```
┌─────────── Cache Warmth Effect ───────────┐
│                                             │
│  코어 0에서 연속 실행:                      │
│  ┌──────────┐                              │
│  │ L1 Cache │ HIT HIT HIT HIT HIT (90%+)   │
│  └──────────┘                              │
│                                             │
│  코어 마이그레이션 후:                       │
│  ┌──────────┐                              │
│  │ L1 Cache │ MISS MISS HIT HIT HIT (50%)  │
│  └──────────┘                              │
│  (새 코어의 캐시는 비어있음)                │
│                                             │
└─────────────────────────────────────────────┘
```

### 2. TLB 플러시 감소

코어 전환 시 TLB(Translation Lookaside Buffer)가 무효화되므로, 동일 코어 유지로 페이지 테이블 변환 오버헤드를 줄인다.

| 효과 | 설명 | 기대 효과 |
|------|------|-----------|
| **캐시 히트율 향상** | L1/L2 캐시 재사용 | 10~30% 성능 향상 |
| **TLB 미스 감소** | 페이지 테이블 캐시 유지 | 5~15% 메모리 접근 향상 |
| **브랜치 예측 향상** | 분기 예측기 유지 | 2~5% 연산 향상 |
| **파이프라인 효율** | 명령어 캐시 유지 | 일관된 실행 속도 |

## Ⅳ. 주요 활용 분야

### 1. 실시간 시스템 (Real-time Systems)

```
┌───────── Real-time CPU Isolation ──────────┐
│                                              │
│  Core 0-1: [Real-time Tasks] (Hard Pinned)  │
│              │                                 │
│              ├── 타이머 인터럽트 최소화        │
│              ├── 인터럽트 핸들러 제외          │
│              └── 결정적 응답 시간 보장        │
│                                              │
│  Core 2-7: [General Purpose Tasks]           │
│              │                                 │
│              ├── OS 서비스                     │
│              ├── 네트워크 I/O                  │
│              └── 로깅, 모니터링               │
│                                              │
└──────────────────────────────────────────────┘
```

### 2. 고빈도 트레이딩 (HFT, High-Frequency Trading)

마이크로초 단위의 지연이 중요한 금융 거래에서 코어 고정은 결정적 응답 시간을 보장한다.

### 3. DPDK (Data Plane Development Kit)

```
┌─────────────── DPDK Poll Mode ───────────────┐
│                                                │
│  Core 0:  RX Poll ──> [Pkt Process] ──> TX    │
│  Core 1:  RX Poll ──> [Pkt Process] ──> TX    │
│  Core 2:  RX Poll ──> [Pkt Process] ──> TX    │
│                                                │
│  - 인터럽트 없이 폴링 (Busy-wait)             │
│  - 각 코어가 독립적인 큐 처리                  │
│  - 캐시 라인 밀림 방지 (RSS + Pinning)        │
│                                                │
└────────────────────────────────────────────────┘
```

## Ⅴ. 지식 그래프

```
스레드 고정 Thread Affinity/Pinning
├── 핵심 개념
│   ├── 스레드를 특정 CPU 코어에 바인딩
│   ├── 소프트 어피니티 (OS 힌트)
│   └── 하드 어피니티 (강제 바인딩)
├── 구현 방법
│   ├── sched_setaffinity() 시스템 콜
│   ├── taskset (프로세스 단위)
│   ├── cgroups cpuset (그룹 단위)
│   ├── numactl (NUMA 노드 단위)
│   └── pthread_setaffinity_np (스레드 단위)
├── 성능 이점
│   ├── 캐시 웜스 (L1/L2 히트율 향상)
│   ├── TLB 플러시 감소
│   ├── 브랜치 예측기 유지
│   └── 결정적 실행 시간 보장
├── 활용 분야
│   ├── 실시간 시스템 (CPU 격리)
│   ├── 고빈도 트레이딩 (지연 최소화)
│   ├── DPDK (데이터 플레인 폴링)
│   └── 데이터베이스 (쿼리 처리 스레드)
└── 주의사항
    ├── 로드 불균형 가능성
    ├── 오버커밋 시 성능 저하
    └── 코어 수보다 많은 스레드 시 문제
```

---

## 약어 정리

| 약어 | Full Name |
|------|-----------|
| **TLB** | Translation Lookaside Buffer |
| **HFT** | High-Frequency Trading |
| **DPDK** | Data Plane Development Kit |
| **RSS** | Receive Side Scaling |
| **NUMA** | Non-Uniform Memory Access |

---

## 3줄 어린이 설명

컴퓨터의 일꾼이 항상 같은 자리에서 일하게 정해주는 방법입니다.
같은 자리를 쓰면 도구를 다시 꺼낼 필요 없어 일이 빨라져요.
주식 거래처럼 아주 빠르고 정확하게 일해야 할 때 씁니다.
