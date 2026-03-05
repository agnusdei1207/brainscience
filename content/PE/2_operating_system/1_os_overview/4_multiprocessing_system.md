+++
title = "다중 처리 시스템 (Multiprocessing System)"
description = "다중 CPU 시스템의 아키텍처와 병렬 처리 원리를 심층 분석합니다."
date = "2026-03-04"
[taxonomies]
tags = ["멀티프로세싱", "SMP", "ASMP", "병렬처리", "캐시일관성"]
categories = ["studynotes-2_operating_system"]
+++

# 다중 처리 시스템 (Multiprocessing System)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 둘 이상의 CPU(프로세서)를 단일 시스템에 탑재하여 진정한 의미의 병렬 처리(Parallelism)를 실현하는 하드웨어-소프트웨어 통합 아키텍처. 시분할이 시간적 분할(Time Division)이라면, 다중 처리는 공간적 분할(Space Division)을 통한 처리량의 선형적 증가를 목표로 한다.
> 2. **가치**: 단일 프로세서 대비 처리량(Throughput)을 코어 수에 비례하여 N배까지 향상 가능(이론적), 실제로는 70~90% 효율 달성. 고가용성(High Availability) 측면에서 한 CPU 고장 시에도 시스템 지속 운영 가능.
> 3. **융합**: 현대 서버, 데이터센터, 슈퍼컴퓨터의 표준 아키텍처이며, 멀티코어 CPU(Intel Xeon, AMD EPYC)와 클라우드 인스턴스의 기반 기술. NUMA(Non-Uniform Memory Access) 아키텍처와 결합하여 확장성 확보.

---

### Ⅰ. 개요 (Context & Background)

#### 개념
다중 처리 시스템(Multiprocessing System)은 **단일 컴퓨터 시스템 내에 둘 이상의 중앙처리장치(CPU)를 탑재하여, 여러 프로세스(또는 스레드)를 물리적으로 동시에 실행(Parallel Execution)할 수 있는 컴퓨터 아키텍처와 이를 지원하는 운영체제의 통합 체계**를 의미한다. 시분할 시스템이 단일 CPU를 시간적으로 분할하여 "동시에 실행되는 것처럼 보이게" 하는 것이라면, 다중 처리 시스템은 실제로 여러 CPU가 동시에 다른 작업을 수행하는 "진정한 병렬성(True Parallelism)"을 제공한다.

**핵심 구분**:
- **동시성(Concurrency)**: 논리적 동시 실행 (시분할, 단일 CPU)
- **병렬성(Parallelism)**: 물리적 동시 실행 (다중 CPU)

다중 처리 시스템의 주요 유형으로는 **비대칭 다중 처리(ASMP, Asymmetric Multiprocessing)**와 **대칭 다중 처리(SMP, Symmetric Multiprocessing)**가 있으며, 현대 시스템의 대다수는 SMP를 채택한다.

#### 💡 비유
다중 처리 시스템을 **'여러 명의 요리사가 있는 주방'**에 비유할 수 있다. 시분할 시스템(단일 요리사)에서는 한 명의 요리사가 여러 요리를 번갈아 만들었다면, 다중 처리 시스템에서는 요리사 4명이 각자 다른 요리를 동시에 만든다. 파스타(CPU 1), 스테이크(CPU 2), 샐러드(CPU 3), 디저트(CPU 4)가 실제로 동시에 조리된다. 결과적으로 전체 주방의 생산량이 4배로 증가한다. 단, 싱크대(메모리/I/O)와 냉장고(디스크)는 공유하므로 병목이 발생할 수 있고, 요리사들 간의 소통(동기화)이 필요하다.

#### 등장 배경 및 발전 과정

**1. 문제 인식: 단일 CPU의 물리적 한계**
- 1960~70년대, CPU 클럭 속도 향상이 무어의 법칙을 따라 급증했으나, 전력 소모와 발열이 한계에 도달.
- 단일 CPU 성능 향상의 어려움: 파이프라인 깊이 증가에 따른 분기 예측 실패 비용 증가, 메모리 대역폭 병목.
- **비즈니스적 요구**: 대규모 트랜잭션 처리(은행, 항공 예약), 과학 연산(날씨 예측, 시뮬레이션) 등 처리량이 중요한 워크로드의 폭발적 증가.

**2. 초기 다중 처리: 비대칭 구조 (ASMP)**
- 1960년대, Burroughs B5000, CDC 6600 등에서 주 프로세서(Master)와 I/O 프로세서(Slave)로 역할 분담.
- **장점**: 설계 단순, 운영체제 수정 최소화.
- **한계**: 주 프로세서 병목, 확장성 부족, 고장 시 전체 시스템 다운.

**3. 대칭 다중 처리 (SMP)의 등장**
- 1980~90년대, Sequent, Encore, Sun Microsystems 등에서 SMP 시스템 상용화.
- **핵심 혁신**: 모든 CPU가 동등한 지위로 메모리와 I/O에 접근, 운영체제가 모든 CPU를 완전히 활용.
- **결과**: 확장성 대폭 향상, 2~64 CPU 시스템까지 구현 가능.

**4. 현대: 멀티코어와 NUMA**
- 2000년대 중반, 단일 칩에 여러 코어를 탑재한 멀티코어 프로세서(Intel Core 2 Duo, AMD Athlon X2) 등장.
- 대규모 시스템에서는 NUMA(Non-Uniform Memory Access) 아키텍처로 메모리 접근 지역성 확보.
- **현재**: 서버급 시스템(Intel Xeon, AMD EPYC)에서 64~128코어, 슈퍼컴퓨터에서는 수만 코어까지 확장.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **다중 CPU 코어 (Multiple CPU Cores)** | 병렬 명령어 실행 | 각 코어 독립적 파이프라인, 명령어 캐시, 데이터 캐시 | x86_64, ARMv8, RISC-V | 여러 명의 요리사 |
| **공유 메모리 (Shared Memory)** | 모든 CPU가 접근 가능한 주 메모리 | 버스 인터페이스, 메모리 컨트롤러, 인터리빙 | DDR4/DDR5, DRAM | 공용 싱크대 |
| **버스/인터커넥트 (Bus/Interconnect)** | CPU-메모리-I/O 간 통신 경로 | 공유 버스, 크로스바, 메시 네트워크 | PCIe, QPI/UPI, HyperTransport | 주방 동선 |
| **캐시 일관성 프로토콜 (Cache Coherence)** | 다중 캐시 간 데이터 동기화 | MESI, MOESI, MESIF 프로토콜 | Snooping, Directory-based | 레시피 공유 |
| **인터럽트 컨트롤러 (Interrupt Controller)** | 인터럽트를 적절한 CPU에 분배 | I/O APIC, MSI/MSI-X, IRQ 밸런싱 | Local APIC, I/O APIC | 주방 호출벨 |
| **스핀락/뮤텍스 (Spinlock/Mutex)** | 다중 CPU 간 동기화 | 원자적 연산, 메모리 배리어, 캐시 라인 바운싱 | CAS, Test-and-Set, Ticket Lock | 싱크대 사용 순서 |
| **로드 밸런서 (Load Balancer)** | CPU 간 작업 분산 | 워크 스틸링, 마이그레이션 스레드 | CFS Load Average, NUMA Balancing | 주문 분배 |

#### 2. 정교한 구조 다이어그램

```text
+===========================================================================+
|           SYMMETRIC MULTIPROCESSING (SMP) ARCHITECTURE                    |
+===========================================================================+

   +-------------------+     +-------------------+     +-------------------+
   |     CPU 0         |     |     CPU 1         |     |     CPU 2         |
   |  +-------------+  |     |  +-------------+  |     |  +-------------+  |
   |  |   Core      |  |     |  |   Core      |  |     |  |   Core      |  |
   |  |  +-------+  |  |     |  |  +-------+  |  |     |  |  +-------+  |  |
   |  |  |  ALU  |  |  |     |  |  |  ALU  |  |  |     |  |  |  ALU  |  |  |
   |  |  +-------+  |  |     |  |  +-------+  |  |     |  |  +-------+  |  |
   |  +-------------+  |     |  +-------------+  |     |  +-------------+  |
   |  |  L1 I-Cache |  |     |  |  L1 I-Cache |  |     |  |  L1 I-Cache |  |
   |  +-------------+  |     |  +-------------+  |     |  +-------------+  |
   |  |  L1 D-Cache |  |     |  |  L1 D-Cache |  |     |  |  L1 D-Cache |  |
   |  +-------------+  |     |  +-------------+  |     |  +-------------+  |
   |  |  L2 Cache   |  |     |  |  L2 Cache   |  |     |  |  L2 Cache   |  |
   |  +------+------+  |     |  +------+------+  |     |  +------+------+  |
   +--+------+----------+     +--+------+----------+     +--+------+----------+
          |                          |                          |
          +------------+-------------+-------------+------------+
                       |                          |
               +-------v-------+          +-------v-------+
               |   L3 Cache    |          |   L3 Cache    |  (Shared Last-Level Cache)
               |  (Shared LLC) |          |  (Shared LLC) |
               +-------+-------+          +-------+-------+
                       |                          |
          +------------+------------+-------------+------------+
          |                                                    |
   +------v------+                                      +-----v------+
   |  System Bus |<--- Cache Coherence Protocol (MESI) ->| Memory Bus |
   | /Interconnect                                      | Controller |
   +------+------+                                      +-----+------+
          |                                                    |
          |                    +-------------------------------+
          |                    |                               |
   +------v------+      +------v------+              +--------v--------+
   |   I/O Hub   |      |   Memory    |              |   I/O Devices   |
   |  (Chipset)  |      |  (DRAM)     |              | (Disk, NIC, GPU)|
   +-------------+      +-------------+              +-----------------+

+===========================================================================+
|              ASYMMETRIC vs SYMMETRIC MULTIPROCESSING                      |
+===========================================================================+

   ASYMMETRIC (ASMP):                   SYMMETRIC (SMP):
   
   +-------------+                       +-------------+
   |   Master    |                       |    CPU 0    |
   |    CPU      |                       +------+------+
   +------+------|                              |
          | runs OS                      +-------+-------+
          |                              |       |       |
   +------v------+         +-------------+------+------+-------------+
   |   Slave 1   |         |    CPU 1    |    CPU 2    |    CPU 3   |
   | (User Apps) |         +------+------+------+------+-----+------+
   +-------------+                |             |            |
   |   Slave 2   |                +------+------+------------+
   | (User Apps) |                       |
   +-------------+                All Run OS & Apps
                                  (Equal Partners)

   ASMP 특징:                      SMP 특징:
   - 단일 CPU가 OS 실행            - 모든 CPU가 OS 실행
   - Slave는 사용자 프로그램만     - 모든 CPU가 사용자 프로그램 실행
   - OS 수정 최소화                - 복잡한 동기화 필요
   - Master 병목 문제              - 높은 확장성
```

#### 3. 심층 동작 원리 (SMP 시스템 부팅 및 스케줄링 6단계)

**① BIOS/UEFI 단계: BSP(Boot Strap Processor) 선정**
- 시스템 전원 시, 하드웨어가 하나의 CPU를 BSP(Boot Strap Processor)로 지정.
- BSP가 부트로더(GRUB, systemd-boot)를 메모리에 로드하고 커널 초기화 시작.
- 다른 CPU들은 AP(Application Processor)로 대기 상태 유지.

**② 커널 초기화: AP 활성화**
- 커널이 BSP에서 실행되며 APIC(Advanced Programmable Interrupt Controller) 초기화.
- SIPI(Start-up Inter-Processor Interrupt)를 각 AP에 전송하여 활성화.
- 각 AP가 자신의 초기화 루틴을 실행하고 Idle 상태로 진입.

**③ 스케줄러 초기화: CPU별 Run Queue 생성**
- 각 CPU(CPU0, CPU1, ...)에 독립적인 Run Queue(cfs_rq) 할당.
- 로드 밸런싱을 위한 통계 구조(Sched Domain, Sched Group) 구축.
- NUMA 시스템에서는 노드별 메모리 할당 정책 설정.

**④ 프로세스 스케줄링: CPU 선택**
- 새 프로세스 생성 시, 스케줄러가 최적의 CPU를 선택:
  - 캐시 친화성(Cache Affinity): 이전에 실행된 CPU 우선
  - 로드 밸런싱: 가장 한가한 CPU 선택
  - NUMA 지역성: 로컬 메모리에 가까운 CPU 우선
- wake_up_process() 호출 시 CPU 선정 로직 실행.

**⑤ 병렬 실행: 진정한 동시성**
- 각 CPU가 독립적으로 스케줄러를 실행하여 자신의 Run Queue에서 프로세스 선택.
- 물리적으로 동시에 서로 다른 프로세스 실행.
- Context Switch는 각 CPU 내에서 독립적으로 발생.

**⑥ 동기화 및 캐시 일관성**
- 한 CPU가 메모리 데이터를 수정하면, MESI 프로토콜을 통해 다른 CPU의 캐시 무효화.
- 스핀락(Spinlock) 획득 시, 다른 CPU는 해당 락이 해제될 때까지 대기.
- 인터럽트(IPI: Inter-Processor Interrupt)를 사용하여 CPU 간 통신.

#### 4. 핵심 알고리즘 & 실무 코드 예시

**[MESI 캐시 일관성 프로토콜 상태 머신]**

```c
/*
 * MESI Cache Coherence Protocol Implementation
 * 다중 처리 시스템에서 캐시 일관성을 유지하는 핵심 프로토콜
 *
 * 상태 정의:
 * M (Modified): 이 캐시 라인이 수정됨, 메모리와 다름, 유일한 사본
 * E (Exclusive): 이 캐시 라인이 메모리와 동일, 유일한 사본
 * S (Shared): 이 캐시 라인이 메모리와 동일, 다른 캐시에도 존재 가능
 * I (Invalid): 캐시 라인이 유효하지 않음
 */

typedef enum {
    MESI_INVALID = 0,
    MESI_SHARED  = 1,
    MESI_EXCLUSIVE = 2,
    MESI_MODIFIED = 3
} MESIState;

typedef struct {
    uint64_t tag;          // 캐시 라인 태그
    MESIState state;       // MESI 상태
    uint8_t data[64];      // 캐시 라인 데이터 (64 bytes)
    bool dirty;            // 더티 비트
} CacheLine;

typedef struct {
    CacheLine lines[NUM_SETS][WAYS_PER_SET];
    int cpu_id;
} Cache;

// 캐시 읽기 처리
int cache_read(Cache* cache, uint64_t addr, uint8_t* data) {
    uint64_t tag = get_tag(addr);
    int set_index = get_set_index(addr);
    
    // 캐시 라인 검색
    for (int way = 0; way < WAYS_PER_SET; way++) {
        CacheLine* line = &cache->lines[set_index][way];
        
        if (line->tag == tag && line->state != MESI_INVALID) {
            // 캐시 히트!
            memcpy(data, line->data, 64);
            
            // 상태 전이 없음 (S, E, M 모두 읽기 가능)
            return CACHE_HIT;
        }
    }
    
    // 캐시 미스 - 메모리에서 로드 필요
    return CACHE_MISS;
}

// 캐시 쓰기 처리
int cache_write(Cache* cache, uint64_t addr, uint8_t* data) {
    uint64_t tag = get_tag(addr);
    int set_index = get_set_index(addr);
    
    for (int way = 0; way < WAYS_PER_SET; way++) {
        CacheLine* line = &cache->lines[set_index][way];
        
        if (line->tag == tag && line->state != MESI_INVALID) {
            // 캐시 히트 - 쓰기 수행
            memcpy(line->data, data, 64);
            
            // 상태 전이
            switch (line->state) {
                case MESI_EXCLUSIVE:
                    // E -> M: 단순히 수정, 다른 캐시에 없음
                    line->state = MESI_MODIFIED;
                    break;
                    
                case MESI_SHARED:
                    // S -> M: 다른 캐시의 사본 무효화 필요
                    broadcast_invalidate(cache->cpu_id, addr);
                    line->state = MESI_MODIFIED;
                    break;
                    
                case MESI_MODIFIED:
                    // M -> M: 이미 수정 상태, 추가 조치 없음
                    break;
                    
                default:
                    break;
            }
            return CACHE_HIT;
        }
    }
    
    // 캐시 미스 - Write Allocate 정책에 따라 처리
    return CACHE_MISS;
}

// 다른 CPU로부터 무효화 요청 수신
void handle_invalidate(Cache* cache, uint64_t addr) {
    uint64_t tag = get_tag(addr);
    int set_index = get_set_index(addr);
    
    for (int way = 0; way < WAYS_PER_SET; way++) {
        CacheLine* line = &cache->lines[set_index][way];
        
        if (line->tag == tag) {
            if (line->state == MESI_MODIFIED) {
                // M 상태면 메모리에 먼저 쓰기 (Write-back)
                memory_write_back(addr, line->data);
            }
            // 상태를 I로 전이
            line->state = MESI_INVALID;
            return;
        }
    }
}
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 1. ASMP vs SMP 비교

| 비교 항목 | ASMP (비대칭) | SMP (대칭) |
|:---|:---|:---|
| **CPU 역할** | Master-Slave 구분 | 모든 CPU 동등 |
| **OS 실행** | Master CPU만 | 모든 CPU |
| **확장성** | 제한적 (Master 병목) | 높음 (거의 선형) |
| **복잡도** | 낮음 | 높음 (동기화) |
| **고가용성** | 낮음 (Master 장애 시 전체 다운) | 높음 (CPU 장애 시에도 운영 지속) |
| **현대 사용** | 드뭄 (임베디드 일부) | 대부분의 서버/데스크톱 |
| **대표 시스템** | 초기 메인프레임 | Linux SMP, Windows SMP |

#### 2. 캐시 일관성 프로토콜 비교

| 프로토콜 | 상태 수 | 특징 | 사용처 |
|:---|:---|:---|:---|
| **MESI** | 4 | Modified, Exclusive, Shared, Invalid | Intel, 대부분의 x86 |
| **MOESI** | 5 | MESI + Owner (더티 공유 가능) | AMD |
| **MESIF** | 6 | MESI + Forward (공유 응답 최적화) | Intel (NUMA) |
| **Directory-based** | N | 중앙 디렉토리로 추적 | 대규모 NUMA, 클러스터 |

---

### Ⅳ. 실무 적용 및 기술사적 판단

#### 시나리오 1: 대규모 웹 서버의 SMP 스케일링

**문제 상황**: 32코어 서버에서 트래픽 증가 시 CPU 사용률이 50%에서 정체. 코어 추가 효과 미미.

**진단**:
- 공유 데이터 구조(세션 캐시)에 대한 락 경합(Lock Contention) 발생.
- 캐시 라인 바운싱(Cache Line Bouncing)으로 인한 MESI 트래픽 급증.

**기술사적 결단**:
1. **락 분할(Lock Sharding)**: 단일 락을 여러 개로 분할하여 경합 감소.
2. **RCU(Read-Copy-Update)**: 읽기 많은 데이터에 RCU 적용하여 락 프리.
3. **Per-CPU 변수**: 통계, 카운터를 CPU별로 분리 후 합산.

**성과**: 32코어 활용률 50% -> 85% 향상.

#### 시나리오 2: NUMA 시스템의 메모리 최적화

**문제 상황**: 4소켓 NUMA 서버에서 특정 애플리케이션의 성능이 기대의 30% 수준.

**진단**:
- 모든 메모리 할당이 단일 노드(Node 0)에서 발생.
- 다른 노드의 CPU가 원격 메모리 접근으로 인해 지연 증가.

**기술사적 결단**:
1. **numactl 적용**: 애플리케이션을 로컬 노드에 바인딩.
2. **First-Touch 정책**: 메모리를 처음 접근하는 CPU의 노드에 할당.
3. **메모리 인터리빙**: 대역폭 집약적 워크로드에 전체 노드 분산.

#### 주의사항 및 안티패턴

1. **False Sharing**: 서로 다른 변수가 동일 캐시 라인에 있어 불필요한 캐시 무효화 발생. 패딩(Padding)으로 해결.

2. **락 홀더 선점**: 락을 보유한 CPU가 선점되면 다른 CPU들이 무한 대기. 락 구간 최소화, 실시간 스케줄링 고려.

3. **확장성 한계**: Amdahl의 법칙에 의해 순차적 코드가 병렬화 효과를 제한. 병렬화 가능 부분을 최대화해야 함.

---

### Ⅴ. 기대효과 및 결론

#### 정량적/정성적 기대효과

| 시스템 구성 | 처리량 (TPS) | 응답 시간 | 가용성 |
|:---|:---|:---|:---|
| **단일 CPU** | 1,000 | 100ms | 99% |
| **SMP 4코어** | 3,500 (3.5x) | 35ms | 99.9% |
| **SMP 16코어** | 12,000 (12x) | 15ms | 99.99% |
| **NUMA 64코어** | 45,000 (45x) | 8ms | 99.999% |

#### 미래 전망

다중 처리 시스템은 **"코어 수의 폭발적 증가"**와 **"이기종 코어(Heterogeneous Cores)"**로 진화하고 있다. ARM big.LITTLE, Intel Hybrid Architecture(P-core/E-core)는 성능 코어와 효율 코어를 조합하여 전력 효율을 극대화한다. 미래에는 수천 개의 코어를 가진 "메가코어" 프로세서와 이를 효율적으로 관리하는 OS 스케줄러가 표준이 될 것이다.

#### 참고 표준/가이드

- **ACPI (Advanced Configuration and Power Interface)**: 멀티프로세서 구성 표준
- **Intel MP Specification**: 멀티프로세서 부트 및 구성
- **NUMA (Non-Uniform Memory Access)**: 대규모 SMP 확장 아키텍처

---

### 관련 개념 맵 (Knowledge Graph)

- [대칭 다중 처리 (SMP)](@/studynotes/2_operating_system/1_os_overview/6_smp.md): SMP의 상세 기술
- [비대칭 다중 처리 (ASMP)](@/studynotes/2_operating_system/1_os_overview/5_asmp.md): ASMP의 구조와 특징
- [캐시 일관성](@/studynotes/2_operating_system/10_security_virtualization/655_cache_coherence.md): MESI 프로토콜
- [로드 밸런싱](@/studynotes/2_operating_system/3_cpu_scheduling/196_load_balancing.md): CPU 간 작업 분산
- [NUMA](@/studynotes/2_operating_system/6_main_memory/377_numa.md): 비균등 메모리 접근

---

### 어린이를 위한 3줄 비유 설명

1. 다중 처리 시스템은 **'여러 명의 요리사가 함께 일하는 큰 주방'**이에요. 요리사가 한 명이면 한 번에 하나의 요리만 만들 수 있지만, 요리사가 4명이면 4가지 요리를 동시에 만들 수 있어요.

2. 요리사들은 **'서로 다른 요리'**를 담당하지만, 싱크대(메모리)와 냉장고(저장공간)는 같이 써요. 그래서 누가 싱크대를 쓸지 잘 정하지 않으면 서로 부딪힐 수 있어요.

3. 잘 조화되면 주방의 음식이 4배나 더 빨리 나와서 손님들이 아주 만족해요! 하지만 요리사들이 서로 싸우면(동기화 문제) 오히려 더 느려질 수도 있답니다.
