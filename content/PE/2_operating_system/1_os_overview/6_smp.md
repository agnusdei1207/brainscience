+++
title = "대칭 다중 처리 (SMP, Symmetric Multiprocessing)"
description = "모든 CPU가 동등하게 메모리와 I/O에 접근하는 대칭 다중 처리 시스템의 아키텍처와 원리를 심층 분석합니다."
date = "2026-03-04"
[taxonomies]
tags = ["SMP", "대칭다중처리", "공유메모리", "캐시일관성", "확장성"]
categories = ["studynotes-2_operating_system"]
+++

# 대칭 다중 처리 (SMP, Symmetric Multiprocessing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다중 CPU 시스템에서 모든 프로세서가 동등한 지위로 공유 메모리와 I/O 자원에 접근하며, 운영체제가 모든 CPU를 균등하게 스케줄링하는 병렬 컴퓨팅 아키텍처. 단일 운영체제 이미지(Single OS Image)가 전체 시스템을 관리하며, 프로세스는 어떤 CPU에서도 실행 가능하다.
> 2. **가치**: 코어 수에 거의 선형적으로 비례하는 처리량 향상(4코어=3.5x, 8코어=7x), 고가용성(단일 CPU 장애 시에도 시스템 지속), 로드 밸런싱을 통한 자원 활용 최적화. 현대 서버 및 데스크톱 시스템의 표준 아키텍처.
> 3. **융합**: 멀티코어 CPU, NUMA 확장, 클라우드 가상화, 컨테이너 오케스트레이션의 기반 기술. Linux CFS(Completely Fair Scheduler), Windows Dispatcher Queue 등 현대 스케줄러의 핵심 설계 철학.

---

### Ⅰ. 개요 (Context & Background)

#### 개념
대칭 다중 처리(Symmetric Multiprocessing, SMP)는 **둘 이상의 동등한 지위를 가진 CPU가 단일 공유 메모리를 통해 상호 연결되고, 하나의 운영체제 인스턴스가 모든 CPU와 자원을 관리하는 병렬 컴퓨팅 아키텍처**를 의미한다. "대칭(Symmetric)"이라는 명칭은 모든 CPU가 메모리 접근, I/O, 인터럽트 처리에서 동등한 권한과 지연 시간을 가진다는 것을 강조한다.

SMP의 핵심 특성:
1. **단일 OS 이미지**: 하나의 커널이 모든 CPU를 관리
2. **공유 메모리**: 모든 CPU가 동일한 물리 메모리에 접근
3. **균등 접근(Uniform Access)**: 모든 CPU의 메모리 접근 시간이 동일 (이상적으로)
4. **완전 연결**: 어떤 CPU도 다른 CPU와 통신 가능

**SMP vs ASMP 핵심 차이**:
- **SMP**: 모든 CPU가 OS + Apps 실행, 완전한 대등성, 높은 확장성
- **ASMP**: Master CPU = OS, Slave CPU = Apps, 계층적 구조, 확장성 제한

#### 💡 비유
SMP를 **'민주적으로 운영되는 협동조합 주방'**에 비유할 수 있다. 모든 요리사(CPU)가 동등한 지위로 주방에 참여한다. 누구나 어떤 요리(프로세스)든 만들 수 있고, 싱크대(메모리)와 냉장고(I/O)에 자유롭게 접근한다. 주방장(OS 커널)은 특정 요리사를 통제하는 것이 아니라, 전체 주방의 작업 분배를 조율한다. 한 요리사가 아파도(장애) 다른 요리사들이 그 일을 대신하여 주방이 계속 운영된다.

#### 등장 배경 및 발전 과정

**1. 문제 인식: ASMP의 확장성 한계**
- 1970~80년대, ASMP 시스템에서 마스터 CPU 병목이 심각한 문제로 대두.
- 마스터 CPU가 모든 I/O와 시스템 콜을 처리하다 보니, 슬레이브 CPU를 아무리 추가해도 성능이 향상되지 않음.
- "마스터 CPU 사용률 100%, 슬레이브 CPU 사용률 30%"와 같은 불균형 발생.

**2. SMP의 등장**
- 1980년대, Sequent Computer Systems, Encore Computer 등에서 최초의 상용 SMP 시스템 출시.
- **핵심 혁신**:
  - 모든 CPU가 커널 진입 가능 (동시에 여러 CPU가 커널 코드 실행)
  - 캐시 일관성(Cache Coherence)을 위한 하드웨어 프로토콜(MESI)
  - 스핀락, 뮤텍스 등 다중 CPU 동기화 기법
- **결과**: 2~32 CPU까지 거의 선형적 성능 확장 달성.

**3. 멀티코어로의 진화**
- 2000년대 중반, 단일 칩에 여러 코어를 통합한 멀티코어 프로세서 등장.
- Intel Core 2 Duo (2006), AMD Athlon 64 X2 (2005)가 대중화.
- SMP의 원리가 칩 내부로 축소되어 적용.

**4. 현대: NUMA와 대규모 확장**
- 대규모 서버(64+ 코어)에서는 NUMA(Non-Uniform Memory Access)로 진화.
- 각 CPU 소켓이 로컬 메모리를 가지지만, 여전히 전체 메모리에 접근 가능.
- Linux CFS, Windows Dispatcher가 NUMA-인식 스케줄링 지원.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **다중 CPU 코어 (Multiple CPU Cores)** | 병렬 명령어 실행 | 독립적 파이프라인, 개별 캐시 계층 | x86_64, ARMv8 | 협동조합 요리사들 |
| **공유 메모리 (Shared Memory)** | 모든 CPU가 접근하는 주 메모리 | 버스/인터커넥트를 통한 균등 접근 | DDR4/DDR5, Memory Controller | 공용 싱크대 |
| **시스템 버스/인터커넥트 (System Bus)** | CPU-메모리-I/O 간 통신 | 공유 버스, 크로스바, 메시 | QPI/UPI, HyperTransport, Infinity Fabric | 주방 동선 |
| **캐시 일관성 메커니즘 (Cache Coherence)** | 다중 캐시 간 데이터 동기화 | MESI/MOESI 프로토콜, Snooping | Cache Snooping, Directory | 레시피 동기화 |
| **공유 I/O 서브시스템** | 모든 CPU가 I/O에 접근 | IRQ 밸런싱, I/O 스케줄링 | APIC, MSI-X, IRQ Affinity | 공용 냉장고 |
| **SMP 스케줄러 (SMP Scheduler)** | CPU 간 작업 분배 | 로드 밸런싱, 마이그레이션, Affinity | CFS, Load Average | 작업 분배판 |
| **동기화 프리미티브 (Synchronization Primitives)** | 다중 CPU 간 상호 배제 | 스핀락, 뮤텍스, RCU, SeqLock | CAS, Memory Barrier | 사용 중 표시판 |

#### 2. 정교한 구조 다이어그램

```text
+===========================================================================+
|            SYMMETRIC MULTIPROCESSING (SMP) ARCHITECTURE                   |
+===========================================================================+

   +-----------------------------------------------------------------------+
   |                     SYMMETRIC PROCESSORS                               |
   |                                                                       |
   |  +-----------+  +-----------+  +-----------+  +-----------+          |
   |  |   CPU 0   |  |   CPU 1   |  |   CPU 2   |  |   CPU 3   |          |
   |  | +-------+ |  | +-------+ |  | +-------+ |  | +-------+ |          |
   |  | | Core  | |  | | Core  | |  | | Core  | |  | | Core  | |          |
   |  | +-------+ |  | +-------+ |  | +-------+ |  | +-------+ |          |
   |  | | L1 I$ | |  | | L1 I$ | |  | | L1 I$ | |  | | L1 I$ | |          |
   |  | +-------+ |  | +-------+ |  | +-------+ |  | +-------+ |          |
   |  | | L1 D$ | |  | | L1 D$ | |  | | L1 D$ | |  | | L1 D$ | |          |
   |  | +-------+ |  | +-------+ |  | +-------+ |  | +-------+ |          |
   |  | | L2 $  | |  | | L2 $  | |  | | L2 $  | |  | | L2 $  | |          |
   |  | +---+---+ |  | +---+---+ |  | +---+---+ |  | +---+---+ |          |
   |  +-----|-----+  +-----|-----+  +-----|-----+  +-----|-----+          |
   |        |              |              |              |                  |
   |        +------+-------+------+-------+------+-------+                 |
   |               |                      |                                |
   |        +------v----------------------v------+                         |
   |        |       Shared L3 Cache             |                         |
   |        |   (Last Level Cache - LLC)        |                         |
   |        +----------------+------------------+                         |
   |                         |                                             |
   +-------------------------|---------------------------------------------+
                             |
   +-------------------------v---------------------------------------------+
   |                     SYSTEM INTERCONNECT                               |
   |   +---------------------------------------------------------------+   |
   |   |    QPI / UPI / HyperTransport / Infinity Fabric             |   |
   |   |    (Point-to-Point High-Speed Interconnect)                 |   |
   |   +---------------------------------------------------------------+   |
   |                         |                                             |
   |   +------------+--------+--------+------------+                       |
   |   |            |                 |            |                       |
   |   v            v                 v            v                       |
   |  +---+        +---+             +---+        +---+                    |
   |  |APIC|       |APIC|            |APIC|       |APIC|  (Local APICs)   |
   |  +---+        +---+             +---+        +---+                    |
   +-------------------------|---------------------------------------------+
                             |
   +-------------------------v---------------------------------------------+
   |                     MEMORY SUBSYSTEM                                  |
   |  +---------------------------------------------------------------+    |
   |  |                    Shared Main Memory                        |    |
   |  |  +-------------+  +-------------+  +-------------+           |    |
   |  |  |   DIMM 0    |  |   DIMM 1    |  |   DIMM 2    |  ...      |    |
   |  |  |   (DDR5)    |  |   (DDR5)    |  |   (DDR5)    |           |    |
   |  |  +-------------+  +-------------+  +-------------+           |    |
   |  +---------------------------------------------------------------+    |
   +-------------------------|---------------------------------------------+
                             |
   +-------------------------v---------------------------------------------+
   |                     I/O SUBSYSTEM                                     |
   |  +-----------+  +-----------+  +-----------+  +-----------+           |
   |  |   PCIe    |  |   SATA    |  |   USB     |  |   LAN     |           |
   |  |  (GPU,NIC)|  |  (SSD,HDD)|  | (Devices) |  |  (NIC)    |           |
   |  +-----------+  +-----------+  +-----------+  +-----------+           |
   +-----------------------------------------------------------------------+

+===========================================================================+
|                    SMP SCHEDULING & LOAD BALANCING                        |
+===========================================================================+

   Per-CPU Run Queues:
   
   CPU 0 Run Queue       CPU 1 Run Queue       CPU 2 Run Queue       CPU 3 Run Queue
   +---------------+     +---------------+     +---------------+     +---------------+
   | Task A (R)    |     | Task D (R)    |     | Task G (R)    |     | Task J (R)    |
   | Task B (R)    |     | Task E (R)    |     | Task H (R)    |     | Task K (R)    |
   | Task C (R)    |     | Task F (R)    |     | Task I (R)    |     | Task L (R)    |
   +-------+-------+     +-------+-------+     +-------+-------+     +-------+-------+
           |                     |                     |                     |
           v                     v                     v                     v
       +-------+             +-------+             +-------+             +-------+
       |Running|             |Running|             |Running|             |Running|
       | Task A|             | Task D|             | Task G|             | Task J|
       +-------+             +-------+             +-------+             +-------+

   Load Balancer Thread (runs periodically on each CPU):
   
   - If CPU 0 load > CPU 1 load:
     Migrate task from CPU 0 to CPU 1
   
   - Migration considerations:
     * Cache warmth (recently executed tasks prefer same CPU)
     * NUMA locality (task memory location)
     * CPU affinity settings (taskset, cgroups)
```

#### 3. 심층 동작 원리 (SMP 시스템 부팅 및 동작 7단계)

**① 하드웨어 초기화: BSP와 AP 구분**
- 시스템 전원 시 하드웨어가 하나의 CPU를 BSP(Boot Strap Processor)로 선정.
- BSP가 BIOS/UEFI를 실행하고 부트로더(GRUB) 로드.
- 다른 CPU들은 AP(Application Processor)로 대기.

**② 커널 초기화: AP 활성화**
- BSP에서 커널이 초기화되며 SMP 지원 설정(smp_prepare_cpus).
- 커널이 각 AP에게 SIPI(Startup Inter-Processor Interrupt) 전송.
- 각 AP가 자신의 초기화 코드(cpu_init)를 실행하고 Idle 스레드 생성.

**③ Per-CPU 데이터 구조 생성**
- 각 CPU마다 독립적인 Run Queue, 통계, IDT, GDT 생성.
- per-cpu 변수 매크로를 사용하여 CPU별 데이터 영역 할당.
- 스핀락 초기화 및 커널 동기화 기법 설정.

**④ 스케줄러 시작**
- 각 CPU가 자신의 Idle 스레드에서 시작.
- 스케줄러가 각 CPU의 Run Queue에서 실행 가능한 태스크 선택.
- 로드 밸런서(load_balance)가 주기적으로 실행되어 CPU 간 부하 분산.

**⑤ 병렬 실행 시작**
- 여러 CPU가 동시에 서로 다른 태스크 실행.
- 각 CPU는 독립적으로 Context Switch 수행.
- 커널 진입 시 커널 락(또는 세마포어)으로 보호.

**⑥ 캐시 일관성 유지**
- 한 CPU가 메모리 데이터를 수정하면 MESI 프로토콜 작동.
- Modified 캐시 라인을 다른 CPU에서 읽으려 하면 Write-back + Invalidate.
- 캐시 라인 전송이 인터커넥트를 통해 이루어짐.

**⑦ 인터럽트 분배 및 처리**
- 외부 인터럽트가 I/O APIC에서 적절한 CPU로 라우팅.
- IRQ Affinity 설정으로 특정 CPU가 특정 인터럽트 담당.
- IPI(Inter-Processor Interrupt)로 CPU 간 통신(TLB Shootdown 등).

#### 4. 핵심 알고리즘 & 실무 코드 예시

**[SMP 스핀락과 로드 밸런싱 구현]**

```c
/*
 * SMP Spinlock Implementation
 * 다중 CPU 환경에서 상호 배제를 위한 스핀락 구현
 */

#include <stdatomic.h>

typedef struct {
    atomic_int locked;  // 0: unlocked, 1: locked
} spinlock_t;

// 스핀락 초기화
void spinlock_init(spinlock_t* lock) {
    atomic_init(&lock->locked, 0);
}

// 스핀락 획득 ( busy waiting )
void spinlock_acquire(spinlock_t* lock) {
    while (atomic_exchange_explicit(&lock->locked, 1, 
                                     memory_order_acquire) == 1) {
        // 이미 잠겨 있으면 대기
        // CPU에 hint를 주어 전력 소모와 버스 트래픽 감소
        while (atomic_load_explicit(&lock->locked, 
                                     memory_order_relaxed) == 1) {
            __builtin_ia32_pause();  // x86 PAUSE 명령어
        }
    }
}

// 스핀락 해제
void spinlock_release(spinlock_t* lock) {
    atomic_store_explicit(&lock->locked, 0, memory_order_release);
}

/*
 * SMP Load Balancing Algorithm (Simplified)
 * CPU 간 부하 분산을 위한 로드 밸런싱
 */

#define NR_CPUS 8
#define LOAD_AVG_PERIOD 100  // ms

typedef struct {
    int cpu_id;
    unsigned long load_avg;    // 평균 부하
    int nr_running;            // 실행 중인 태스크 수
    int nr_queue;              // 대기 큐의 태스크 수
} cpu_load_info;

cpu_load_info cpu_data[NR_CPUS];

// 가장 한가한 CPU 찾기
int find_idlest_cpu(void) {
    int idlest_cpu = 0;
    unsigned long min_load = cpu_data[0].load_avg;
    
    for (int i = 1; i < NR_CPUS; i++) {
        if (cpu_data[i].load_avg < min_load) {
            min_load = cpu_data[i].load_avg;
            idlest_cpu = i;
        }
    }
    
    return idlest_cpu;
}

// 태스크 마이그레이션 결정
int should_migrate_task(int src_cpu, int dst_cpu) {
    // 조건 1: 목적지 CPU가 더 한가해야 함
    if (cpu_data[dst_cpu].load_avg >= cpu_data[src_cpu].load_avg)
        return 0;
    
    // 조건 2: 부하 차이가 임계값 이상이어야 함
    unsigned long load_diff = cpu_data[src_cpu].load_avg - 
                              cpu_data[dst_cpu].load_avg;
    if (load_diff < LOAD_AVG_PERIOD / 4)
        return 0;
    
    // 조건 3: 캐시 친화성 고려 ( 최근에 실행한 CPU 선호 )
    // 실제로는 task->recent_cpu 등을 확인
    
    return 1;
}

// 로드 밸런싱 수행
void load_balance(int this_cpu) {
    int busiest_cpu = -1;
    unsigned long max_load = 0;
    
    // 가장 바쁜 CPU 찾기
    for (int i = 0; i < NR_CPUS; i++) {
        if (i != this_cpu && cpu_data[i].load_avg > max_load) {
            max_load = cpu_data[i].load_avg;
            busiest_cpu = i;
        }
    }
    
    // 이 CPU와 가장 바쁜 CPU 간 부하 분산
    if (busiest_cpu >= 0 && 
        should_migrate_task(busiest_cpu, this_cpu)) {
        
        // 실제 태스크 마이그레이션 수행
        // migrate_task(task, busiest_cpu, this_cpu);
        
        printf("[CPU %d] Migrated task from CPU %d to balance load\n",
               this_cpu, busiest_cpu);
    }
}

// Per-CPU 타이머 인터럽트 핸들러 ( 주기적 로드 밸런싱 )
void scheduler_tick(int cpu) {
    // 현재 CPU의 부하 갱신
    cpu_data[cpu].load_avg = calculate_load_avg(cpu);
    
    // 주기적으로 로드 밸런싱 수행
    static int balance_counter[NR_CPUS] = {0};
    if (++balance_counter[cpu] >= LOAD_BALANCE_INTERVAL) {
        balance_counter[cpu] = 0;
        load_balance(cpu);
    }
}
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 1. SMP 확장성 분석 (Amdahl의 법칙)

| CPU 코어 수 | 이론적 가속비 | 실제 가속비 | 효율성 | 제한 요인 |
|:---|:---|:---|:---|:---|
| 2 | 2.0x | 1.9x | 95% | 락 경합 |
| 4 | 4.0x | 3.5x | 88% | 락 경합, 캐시 일관성 |
| 8 | 8.0x | 6.5x | 81% | 락 경합, 메모리 대역폭 |
| 16 | 16.0x | 11.0x | 69% | 메모리 대역폭, 인터커넥트 |
| 32 | 32.0x | 18.0x | 56% | NUMA 효과, 확장성 한계 |
| 64 | 64.0x | 28.0x | 44% | NUMA, 소프트웨어 병목 |

#### 2. 캐시 일관성 프로토콜 비교

| 프로토콜 | 상태 | 장점 | 단점 | 사용 |
|:---|:---|:---|:---|:---|
| **MESI** | M, E, S, I | 단순, 널리 사용 | Exclusive 활용 낮음 | Intel x86 |
| **MOESI** | +Owner | 더티 공유 가능 | 구현 복잡 | AMD |
| **MESIF** | +Forward | 공유 응답 최적화 | Intel 특허 | Intel NUMA |
| **Directory** | 추적 테이블 | 확장성 우수 | 지연 증가 | 대규모 NUMA |

---

### Ⅳ. 실무 적용 및 기술사적 판단

#### 시나리오 1: SMP 서버의 락 경합 최적화

**문제 상황**: 32코어 SMP 서버에서 높은 CPU 사용률에도 처리량이 8코어 수준에 머무름.

**진단**:
- perf 분석 결과 전체 CPU 시간의 40%가 스핀락 대기.
- 공유 데이터 구조(세션 테이블)에 대한 빈번한 락 획득/해제.

**기술사적 결단**:
1. **RCU(Read-Copy-Update)**: 읽기 많은 데이터에 RCU 적용.
2. **Per-CPU 변수**: 카운터, 통계를 CPU별로 분리.
3. **락 분할(Sharding)**: 단일 락을 여러 락으로 분할.
4. **Lock-free 자료구조**: 큐, 스택에 CAS 기반 구현 사용.

**성과**: 락 대기 시간 40% -> 5%, 처리량 4배 증가.

#### 시나리오 2: NUMA-인식 SMP 스케줄링

**문제 상황**: 4소켓 NUMA 서버에서 메모리 대역폭 활용이 불균형.

**진단**:
- 모든 메모리 할당이 Node 0에 집중.
- 다른 노드의 CPU가 원격 메모리 접근으로 지연 증가.

**기술사적 결단**:
```bash
# NUMA 정책 설정
numactl --interleave=all ./application  # 인터리브
numactl --cpunodebind=1 --membind=1 ./app  # 노드 바인딩
```

#### 주의사항 및 안티패턴

1. **False Sharing**: 다른 변수가 같은 캐시 라인에 위치하여 불필요한 캐시 무효화.
   - 해결: 캐시 라인 크기(64bytes)로 정렬, 패딩 추가.

2. **락 홀더 선점**: 락을 보유한 스레드가 선점되면 다른 CPU 대기.
   - 해결: 락 구간 최소화, 실시간 스레드 사용.

3. **NUMA 무시**: NUMA 시스템에서 지역성 고려 없는 메모리 할당.
   - 해결: first-touch 정책, numactl 활용.

---

### Ⅴ. 기대효과 및 결론

#### 정량적/정성적 기대효과

| 지표 | 단일 CPU | SMP 4코어 | SMP 16코어 | SMP 64코어(NUMA) |
|:---|:---|:---|:---|:---|
| **처리량 (TPS)** | 1,000 | 3,800 | 14,000 | 45,000 |
| **응답 시간** | 100ms | 28ms | 9ms | 3ms |
| **가용성** | 99% | 99.9% | 99.99% | 99.999% |
| **CPU당 비용** | 높음 | 중간 | 낮음 | 매우 낮음 |

#### 미래 전망

SMP는 **"멀티코어의 시대"**를 열었으며, 앞으로도 범용 컴퓨팅의 핵심 아키텍처로 유지될 것이다. 주요 진화 방향:

1. **코어 수 급증**: 2025년까지 서버 CPU는 128~256코어, 클라이언트는 16~32코어 보편화.
2. **이기종 코어**: P-core(성능) + E-core(효율) 하이브리드 구조(Intel, ARM).
3. **칩렛(Chiplet) 아키텍처**: 여러 다이를 패키지로 통합, 확장성과 수율 향상.
4. **소프트웨어 정의 스케줄링**: AI 기반 워크로드 예측, 동적 코어 할당.

#### 참고 표준/가이드

- **ACPI 6.0+**: 멀티프로세서 및 NUMA 구성 표준
- **UEFI**: 멀티코어 부트 프로토콜
- **POSIX Threads**: SMP 프로그래밍 표준 API
- **Linux Kernel Documentation**: Documentation/scheduler/

---

### 관련 개념 맵 (Knowledge Graph)

- [비대칭 다중 처리 (ASMP)](@/studynotes/2_operating_system/1_os_overview/5_asmp.md): SMP와 비교되는 구조
- [캐시 일관성](@/studynotes/2_operating_system/10_security_virtualization/655_cache_coherence.md): MESI 프로토콜
- [로드 밸런싱](@/studynotes/2_operating_system/3_cpu_scheduling/196_load_balancing.md): CPU 간 작업 분산
- [NUMA](@/studynotes/2_operating_system/6_main_memory/377_numa.md): 대규모 SMP 확장
- [스핀락](@/studynotes/2_operating_system/4_concurrency_sync/233_spinlock.md): SMP 동기화 기법

---

### 어린이를 위한 3줄 비유 설명

1. SMP는 **'모든 요리사가 동등한 권한을 가진 주방'**이에요. 요리사(CPU) 누구나 어떤 요리(프로그램)든 만들 수 있고, 싱크대(메모리)와 냉장고(I/O)를 똑같이 쓸 수 있어요.

2. 주방장(OS)은 특정 요리사에게만 일을 시키는 게 아니라, **'바쁘지 않은 요리사에게'** 요리를 맡겨요. 그래서 모든 요리사가 고르게 일하고, 한 요리사가 아파도 다른 요리사가 대신할 수 있어요.

3. 요리사들이 서로 같은 재료(데이터)를 쓸 때 **'누가 먼저 쓸지'** 정하는 것이 중요해요. SMP는 이것을 아주 똑똑하게 처리해서 요리사들이 서로 부딪히지 않고 효율적으로 일할 수 있게 해준답니다!
