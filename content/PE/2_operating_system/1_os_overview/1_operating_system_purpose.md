+++
title = "운영체제 (Operating System)의 목적"
description = "자원 관리, 편의성, 성능 향상을 목적으로 하는 운영체제의 핵심 원리와 아키텍처를 심층 분석합니다."
date = "2026-03-04"
[taxonomies]
tags = ["운영체제", "자원관리", "추상화", "시스템소프트웨어"]
categories = ["studynotes-2_operating_system"]
+++

# 운영체제 (Operating System)의 목적

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 하드웨어 자원(CPU, 메모리, 저장장치, I/O 장치)을 추상화(Abstraction)하여 응용 프로그램과 사용자에게 논리적이고 일관된 서비스 인터페이스를 제공하는 시스템 소프트웨어의 정점. 커널(Kernel)은 하드웨어와 소프트웨어 사이의 유일한 중재자(Arbitrator)로서 자원 할당의 절대 권한을 행사한다.
> 2. **가치**: 다중 프로그래밍(Multiprogramming)을 통한 CPU 이용률 90% 이상 달성, 시분할(Time-sharing) 기반 응답 시간 100ms 이내 보장, 메모리 가상화를 통한 물리 메모리 대비 10배 이상의 주소 공간 제공 등 시스템 자원의 극한 활용과 사용자 편의성을 동시에 확보.
> 3. **융합**: 클라우드 컴퓨팅의 하이퍼바이저(Hypervisor), 컨테이너 런타임(Docker, containerd), 서버리스(Function-as-a-Service) 플랫폼의 기반이 되며, eBPF와 같은 커널 확장 기술을 통해 관측성(Observability)과 보안의 새로운 패러다임을 제시.

---

### Ⅰ. 개요 (Context & Background)

#### 개념
운영체제(Operating System, OS)는 컴퓨터 하드웨어와 사용자 및 응용 프로그램 사이에 위치하여 **자원 관리(Resource Management)**, **편의성 제공(Convenience)**, **성능 향상(Performance Enhancement)**이라는 삼위일체의 목적을 달성하는 핵심 시스템 소프트웨어다. 운영체제는 단순한 프로그램의 집합이 아니라, 컴퓨터 시스템 전체를 통제하는 '정부(Government)'와 같은 역할을 수행한다. 하드웨어라는 물리적 자원을 소유하지는 않으나, 이를 효율적이고 공정하게 배분하여 시스템 전체의 목표(Throughput, Response Time, Fairness)를 달성하는 최고 관리자다.

운영체제의 존재 이유는 크게 세 가지로 요약된다. 첫째, **자원 관리(Resource Management)**는 CPU 시간, 메모리 공간, 저장장치 용량, I/O 대역폭 등 한정된 하드웨어 자원을 여러 프로세스 사이에 배분하고, 상호 간섭을 방지하며(Isolation), 자원 낭비를 최소화하는 것이다. 둘째, **편의성(Convenience)**은 하드웨어의 복잡성을 추상화하여 사용자와 개발자가 저수준 하드웨어 제어를 신경 쓰지 않고도 직관적인 인터페이스(GUI, CLI, API)를 통해 컴퓨터를 활용할 수 있게 하는 것이다. 셋째, **성능 향상(Performance Enhancement)**은 시스템 자원의 이용률(Utilization)을 극대화하고, 처리량(Throughput)을 증대하며, 응답 시간(Response Time)과 대기 시간(Turnaround Time)을 최소화하는 것이다.

#### 💡 비유
운영체제를 **'초고속 열차의 종합 관제 센터'**에 비유할 수 있다. 열차(프로세스)들은 각자 목적지(작업)를 향해 달려야 하지만, 선로(CPU), 역 플랫폼(메모리), 전력 공급(I/O 자원)은 한정되어 있다. 관제 센터(OS)는 모든 열차의 출발 시간을 조율하고(Scheduling), 선로 충돌을 예방하며(Synchronization/Mutual Exclusion), 승객(사용자)들이 안전하고 편안하게 이용할 수 있도록 안내 방송과 표지판(Interface/Abstraction)을 제공한다. 관제 센터가 없다면 열차들은 서로 충돌하고, 승객들은 어느 열차에 타야 할지조차 알 수 없는 혼란에 빠질 것이다.

#### 등장 배경 및 발전 과정
1. **1세대 (1940~1950년대): 운영체제 부재 시대**
   - 초기 컴퓨터(ENIAC, UNIVAC)는 프로그래머가 하드웨어를 직접 제어해야 했다.
   - **치명적 한계**: I/O 대기 시간 동안 CPU가 100% 유휴 상태로 방치되어 비용 대비 효율이 극악이었다. 당시 컴퓨터 가격이 현대 가치로 수십억 원에 달했음을 고려하면, 이는 경제적 낭비의 극치였다.

2. **2세대 (1955~1965년대): 일괄 처리 시스템(Batch Processing)의 탄생**
   - IBM 7094 등에서 **Resident Monitor**가 도입되어 작업 전환을 자동화했다.
   - **혁신적 변화**: 작업(Job)들을 미리 묶어서(Batch) 순차 처리함으로써 설정 시간(Setup Time)을 절감.
   - **남은 한계**: 여전히 I/O 연산 중 CPU가 대기해야 하는 병목 현상 지속.

3. **3세대 (1965~1980년대): 다중 프로그래밍과 시분할 시스템**
   - **다중 프로그래밍(Multiprogramming)**: I/O 대기 중인 프로세스의 CPU를 다른 프로세스에 양도하여 CPU 이용률을 획기적으로 향상.
   - **시분할 시스템(Time-sharing)**: IBM CTSS, MULTICS, UNIX 등이 등장하여 각 사용자에게 짧은 시간 할당량(Time Quantum)을 교차 배분, 실시간 대화형(Interactive) 컴퓨팅을 구현.
   - **비즈니스적 요구**: 은행, 항공 예약, 온라인 트랜잭션 처리(OLTP) 등 실시간성이 요구되는 산업 분야의 폭발적 성장이 이를 강제했다.

4. **4세대 (1980년~현재): 개인용 컴퓨터, 분산 시스템, 클라우드 네이티브**
   - PC의 보급과 함께 MS-DOS, Windows, macOS, Linux가 대중화.
   - 인터넷과 클라우드 컴퓨팅의 등장으로 **분산 운영체제(Distributed OS)**, **가상화/컨테이너 기술**, **서버리스 컴퓨팅**으로 진화.
   - **현재 시장 요구**: 초연결 사회(IoT, 5G)에서의 실시간 처리, 제로 트러스트 보안, 에너지 효율성, 그리고 양자 컴퓨팅과의 융합이 새로운 패러다임을 형성 중.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **프로세스 관리자 (Process Manager)** | 프로세스 생성/종료, 스케줄링, 동기화 제어 | PCB(Task Struct) 관리, Context Switch, CPU 스케줄링 알고리즘(CFS, RR, Priority) 적용, IPC 메커니즘 제공 | POSIX fork/exec, signal, semaphore | 교차로 신호등 제어관 |
| **메모리 관리자 (Memory Manager)** | 메모리 할당/해제, 주소 변환, 보호 | 페이지 테이블 관리, TLB 조회, 페이지 교체 알고리즘(LRU, Clock), 스와핑, COW(Copy-on-Write) | MMU, PAE, NUMA, Buddy System, Slab Allocator | 부동산 중개인 |
| **파일 시스템 관리자 (File System Manager)** | 데이터 영속성, 계층적 디렉터리, 접근 제어 | inode 관리, 블록 할당(Extent, Bitmap), 저널링, 버퍼 캐시, VFS 추상화 계층 | ext4, XFS, NTFS, NFS, SMB, FUSE | 도서관 사서 |
| **I/O 서브시스템 (I/O Subsystem)** | 장치 구동, 버퍼링, 캐싱, 스풀링 | 장치 드라이버 로딩, DMA 제어, 인터럽트 핸들링, 블록/문자 장치 추상화 | SCSI, NVMe, USB, PCIe, DMA, Interrupt | 항만 하역 크레인 |
| **보호 및 보안 모듈 (Protection & Security)** | 권한 검증, 접근 통제, 인증 | User/Kernel Mode 분리, ACL/Capability 검사, Audit Logging, 샌드박싱 | Ring 0-3, SELinux, AppArmor, Seccomp | 성벽 경비대 |
| **네트워크 스택 (Network Stack)** | 통신 프로토콜 처리, 소켓 관리 | 패킷 캡슐화/역캡슐화, 라우팅 테이블 조회, 소켓 버퍼 관리, Checksum 계산 | TCP/IP, UDP, DNS, HTTP, eBPF XDP | 국제 우편물류 센터 |
| **장치 드라이버 인터페이스 (Device Driver Interface)** | 하드웨어 추상화, 표준화된 장치 접근 | 레지스터 읽기/쓰기, 인터럽트 등록, DMA 전송 요청, 버퍼 관리 | LKM(Loadable Kernel Module), UEFI, ACPI | 만능 번역기 |

#### 2. 정교한 구조 다이어그램

```text
+------------------------------------------------------------------------------+
|                    OPERATING SYSTEM ARCHITECTURE (Layered View)              |
+------------------------------------------------------------------------------+

  +-------------------------------------------------------------------------+
  | USER LAYER (Ring 3)                                                     |
  |  +---------+ +---------+ +---------+ +---------+ +---------+            |
  |  | Browser | | Office  | |   IDE   | | Database| |  Game   |            |
  |  |(Chrome) | |(MS Word)| |(VS Code)| |(PostgreSQL)|(Overwatch)|         |
  |  +----+----+ +----+----+ +----+----+ +----+----+ +----+----+            |
  |       |           |           |           |           |                  |
  |  +----v-----------v-----------v-----------v-----------v------+          |
  |  |              System Call Interface (API Layer)             |          |
  |  |   open() | read() | write() | fork() | exec() | socket()  |          |
  |  +-------------------------------------------------------------+          |
  +-------------------------------------------------------------------------+
                                       |
                          =============|=============
                          |  System Call  |  (Trap: int 0x80 / syscall)
                          =============|=============
                                       |
  +-------------------------------------------------------------------------+
  | KERNEL LAYER (Ring 0)                                                   |
  |                                                                         |
  |  +-------------------------------------------------------------------+ |
  |  |                    SYSTEM CALL HANDLER & DISPATCHER               | |
  |  +-------------------------------------------------------------------+ |
  |                                       |                                |
  |  +------------+ +------------+ +------+-------+ +------------+ +------+ |
  |  |  PROCESS   | |  MEMORY    | | FILE SYSTEM  | |  NETWORK   | | I/O  | |
  |  |  MANAGER   | |  MANAGER   | | (VFS Layer)  | |   STACK    | |SUBSYS| |
  |  +------------+ +------------+ +--------------+ +------------+ +------+ |
  |  | - Scheduler| | - Paging   | | - inode Cache| | - TCP/IP   | |Buffer| |
  |  | - PCB/TCB  | | - TLB Flush| | - dentryCache| | - Socket   | |Cache | |
  |  | - IPC      | | - Swap     | | - Block Alloc| | - Routing  | |Spool | |
  |  | - Signal   | | - COW      | | - Journaling | | - netfilter| | DMA  | |
  |  | - cgroups  | | - kmalloc  | | - Quota      | | - eBPF XDP | | IRQ  | |
  |  +------------+ +------------+ +--------------+ +------------+ +------+ |
  |                                       |                                |
  |  +-------------------------------------------------------------------+ |
  |  |              DEVICE DRIVERS (Block | Char | Network | Misc)       | |
  |  |   [NVMe Driver] [GPU Driver] [NIC Driver] [USB Driver]            | |
  |  +-------------------------------------------------------------------+ |
  +-------------------------------------------------------------------------+
                                       |
  +-------------------------------------------------------------------------+
  | HARDWARE LAYER (Physical Components)                                    |
  |  +---------+ +---------+ +---------+ +---------+ +---------+ +--------+ |
  |  |   CPU   | |  DRAM   | |NVMe SSD | |   NIC   | |   GPU   | |  I/O   | |
  |  |(x86/ARM)| | (DDR5)  | | (PCIe)  | |(Ethernet)| | (PCIe)  | | Ports  | |
  |  +---------+ +---------+ +---------+ +---------+ +---------+ +--------+ |
  +-------------------------------------------------------------------------+
```

#### 3. 심층 동작 원리 (시스템 콜 처리 7단계)

**① 사용자 요청 발생 (User Space)**
- 응용 프로그램이 read(fd, buffer, size) 함수 호출
- 표준 C 라이브러리(glibc)가 함수를 래핑하여 시스템 콜 번호(rax 레지스터 = 0)와 인자들을 레지스터(rdi, rsi, rdx)에 적재

**② 트랩(Trap) 발생 및 모드 전환**
- syscall 명령어 실행 시 CPU가 User Mode(Ring 3)에서 Kernel Mode(Ring 0)로 전환
- Mode Bit가 1 -> 0으로 변경되고, RIP 레지스터가 커널 진입점(MSR_LSTAR)으로 점프

**③ 컨텍스트 저장 (Context Save)**
- 커널은 사용자 레지스터(General Purpose Registers, Flags, RIP, RSP)를 커널 스택 또는 pt_regs 구조체에 저장
- 이는 시스템 콜 완료 후 사용자 프로세스를 정확히 복원하기 위함

**④ 시스템 콜 디스패칭 (Dispatch)**
- 시스템 콜 번호를 인덱스로 하여 sys_call_table에서 해당 핸들러 함수(sys_read) 주소 획득
- 함수 포인터를 통해 실제 커널 함수 호출

**⑤ 서비스 수행 (Service Execution)**
- 파일 디스크립터 테이블에서 fd에 해당하는 file 객체 조회
- VFS(Virtual File System) 계층을 통해 실제 파일 시스템(ext4, NFS 등)의 read 연산 호출
- 페이지 캐시(Page Cache) 확인: Hit 시 즉시 반환, Miss 시 디스크 I/O 요청

**⑥ 결과 반환 및 모드 복원 (Return to User)**
- 결과값(읽은 바이트 수 또는 에러 코드)을 rax 레지스터에 저장
- iretq 또는 sysretq 명령어로 사용자 모드 복귀
- 저장된 레지스터 값을 복원하고 사용자 코드의 다음 명령어부터 재개

**⑦ 사용자 공간에서 결과 확인**
- glibc가 rax 레지스터 값을 확인하여 성공/실패 판단
- 실패 시 errno 변수에 에러 코드 설정, 애플리케이션에 -1 반환

#### 4. 핵심 알고리즘 & 실무 코드 예시

**[리눅스 커널 CFS(Completely Fair Scheduler) vruntime 갱신 알고리즘]**

```c
/*
 * Linux Kernel - kernel/sched/fair.c
 * CFS vruntime 갱신 로직 (간소화 버전)
 *
 * vruntime: 가상 실행 시간으로, 실행 시간을 가중치로 정규화한 값
 *           낮은 vruntime을 가진 태스크가 우선 스케줄링됨
 */
static void update_curr(struct cfs_rq *cfs_rq)
{
    struct sched_entity *curr = cfs_rq->curr;
    u64 now = rq_clock_task(rq_of(cfs_rq));
    u64 delta_exec;

    if (!curr)
        return;

    /* 실제 실행된 시간 계산 */
    delta_exec = now - curr->exec_start;
    if (unlikely((s64)delta_exec <= 0))
        return;

    curr->exec_start = now;

    /* 가중치 기반 vruntime 갱신
     * vruntime += delta_exec * (NICE_0_LOAD / curr->load.weight)
     * - 낮은 우선순위(높은 nice 값) 태스크는 vruntime이 더 빠르게 증가
     * - 결과적으로 CPU 시간을 덜 배분받음
     */
    curr->vruntime += calc_delta_fair(delta_exec, curr);

    /* 태스크의 실행 통계 갱신 */
    update_min_vruntime(cfs_rq);
}
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 1. 운영체제 목적별 핵심 지표 비교표

| 목적 | 핵심 지표 (KPI) | 측정 방법 | 최적화 기법 | 목표 수치 |
|:---|:---|:---|:---|:---|
| **자원 관리 (Resource Management)** | CPU 이용률, 메모리 활용률, I/O 대역폭 | top, vmstat, iostat, perf | 다중 프로그래밍, 페이징, I/O 버퍼링 | CPU 80%+, Memory 90%+ |
| **편의성 (Convenience)** | API 직관성, 학습 곡선, 오류 메시지 품질 | 사용자 만족도 조사, HCI 지표 | GUI/CLI 개선, 매뉴얼, IDE 통합 | NPS 50+ |
| **성능 향상 (Performance)** | Throughput, Latency, Response Time | 벤치마크(TPC-C, SPEC), APM | 캐싱, 프리페칭, 비동기 I/O | Latency < 100ms |
| **보호 및 보안 (Protection)** | 무결성, 가용성, 기밀성 | 취약점 스캔, 침투 테스트 | ASLR, DEP, SELinux, Seccomp | CVE 0건 |

#### 2. 운영체제 유형별 목적 달성 전략 비교

| OS 유형 | 자원 관리 전략 | 편의성 전략 | 성능 최적화 전략 | 대표 사례 |
|:---|:---|:---|:---|:---|
| **범용 OS (General Purpose)** | 균형 잡힌 스케줄링(CFS), 동적 메모리 할당 | 풍부한 GUI, POSIX 호환 API | 캐싱, 버퍼링, 선점형 멀티태스킹 | Linux, Windows, macOS |
| **실시간 OS (RTOS)** | 우선순위 기반 선점, 우선순위 상속 | 최소한의 API, 결정론적 응답 | Lock-free 자료구조, 고정 파티션 | VxWorks, QNX, FreeRTOS |
| **임베디드 OS** | 메모리 풋프린트 최소화, 정적 할당 | 제한적 인터페이스, 크로스 컴파일 | 이벤트 기반, 저전력 모드 | FreeRTOS, Zephyr, ThreadX |
| **분산 OS** | 분산 자원 스케줄링, 부하 분산 | 투명한 원격 접근, 단일 시스템 이미지 | RPC, 분산 캐시, 복제 | Google Borg, Apache Mesos |

---

### Ⅳ. 실무 적용 및 기술사적 판단

#### 시나리오 1: 고빈도 트레이딩 시스템(HFT)의 초저지연 OS 튜닝

**문제 상황**: 주식 트레이딩 시스템에서 마이크로초(us) 단위의 지연이 수익/손실을 결정짓는 상황. 표준 Linux 커널의 Context Switch 오버헤드와 인터럽트 처리 지연이 병목.

**기술사적 결단**:
1. **커널 우회(Kernel Bypass)**: DPDK 또는 OpenOnload를 사용하여 네트워크 패킷 처리를 사용자 공간에서 직접 수행. 커널 네트워크 스택(Interrupt -> SoftIRQ -> Socket Buffer)을 완전히 생략.
2. **CPU 고정(CPU Pinning)**: 트레이딩 스레드를 전용 코어에 바인딩하여 캐시 일관성(Cache Coherence) 유지 및 마이그레이션 오버헤드 제거.
3. **실시간 커널 패치(PREEMPT_RT)**: 스핀락을 뮤텍스로 변환하고, 인터럽트를 스레드화하여 선점 포인트를 극대화.
4. **Huge Pages 활용**: 2MB 또는 1GB Huge Pages를 사용하여 TLB Miss를 95% 이상 감소.

**성과**: 평균 왕복 지연시간(Round-trip Latency)을 50us에서 2us로 단축 (25배 개선).

#### 시나리오 2: 대규모 클라우드 인프라의 리소스 격리 및 QoS 보장

**문제 상황**: 멀티테넌트 클라우드 환경에서 하나의 테넌트가 과도한 CPU/메모리를 독점하여 다른 테넌트의 서비스 품질 저하 (Noisy Neighbor 문제).

**기술사적 결단**:
1. **cgroups v2 도입**: CPU, Memory, I/O에 대한 계층적 리소스 제한 설정. cpu.max로 CPU 할당량 제한, memory.max로 OOM Killer 트리거 포인트 설정.
2. **네임스페이스 격리**: PID, NET, MNT, UTS 등을 분리하여 테넌트 간 완전한 가시성 격리.
3. **CFS Bandwidth Control**: cpu.cfs_quota_us와 cpu.cfs_period_us를 조합하여 CPU 시간을 절대적 할당량으로 제한.

```bash
# cgroups v2 예시: 컨테이너 A에 CPU 2코어, Memory 4GB 제한
echo 200000 > /sys/fs/cgroup/container_a/cpu.max  # 2코어 (200ms/100ms)
echo 4G > /sys/fs/cgroup/container_a/memory.max
```

#### 도입 시 고려사항 (체크리스트)

**기술적 고려사항**:
- [ ] 커널 버전 호환성: 최신 기능(eBPF, cgroups v2)을 위해 Linux 4.18+ 권장
- [ ] 하드웨어 지원: Intel VT-x/AMD-V 가상화 지원 여부 확인
- [ ] 드라이버 가용성: 특수 하드웨어(GPU, FPGA, SmartNIC)의 커널 드라이버 존재 여부

**운영/보안적 고려사항**:
- [ ] Observability 도구 배포: Prometheus + eBPF 기반 모니터링 스택 구축
- [ ] 보안 강화: SELinux 정책 수립, Seccomp 필터 적용, Kernel Hardening
- [ ] 장애 대응: Kdump/kexec 기반 커널 크래시 덤프 분석 체계 확립

#### 주의사항 및 안티패턴

1. **오버커밋(Overcommit) 남용**: 메모리 오버커밋(VM 확약 메모리 > 물리 메모리)은 OOM Killer를 빈번히 트리거하여 서비스 중단을 유발할 수 있다. 항상 충분한 여유 메모리(20%+)를 확보하라.

2. **Context Switch 폭주**: 너무 많은 스레드 생성은 캐시 스래싱(Cache Thrashing)과 TLB 플러시로 인해 오히려 성능을 저하시킨다. 스레드 풀(Thread Pool)과 Work Queue를 사용하여 동시성을 제어하라.

3. **I/O 블로킹 남용**: 동기식 블로킹 I/O를 메인 루프에서 사용하면 CPU가 대기 상태로 낭비된다. Linux AIO, io_uring, epoll을 활용한 비동기 I/O 패턴으로 전환하라.

---

### Ⅴ. 기대효과 및 결론

#### 정량적/정성적 기대효과

| 개선 항목 | 적용 전 | 적용 후 | 개선율 |
|:---|:---|:---|:---|
| **CPU 이용률** | 45% (단일 작업) | 92% (다중 프로그래밍) | +104% |
| **평균 응답 시간** | 500ms (일괄 처리) | 50ms (시분할) | -90% |
| **메모리 활용률** | 60% (고정 분할) | 95% (가상 메모리) | +58% |
| **시스템 가용성** | 99.5% | 99.99% (HA 구성) | +0.49%p |
| **보안 사고 건수** | 연 12건 | 연 1건 (강화 정책) | -92% |

#### 미래 전망 및 진화 방향

1. **eBPF 기반 커널 프로그래밍**: 2025년 이후 eBPF는 네트워킹, 보안, 관측성을 넘어 스케줄링과 메모리 관리까지 확장될 전망. 커널 수정 없이 런타임에 핵심 기능을 주입할 수 있는 '안전한 커널 확장' 패러다임이 주류가 될 것이다.

2. **유니커널(Unikernel)과 서버리스의 융합**: 클라우드 네이티브 환경에서 단일 애플리케이션을 위한 초경량 OS(Unikernel)가 서버리스 플랫폼과 결합하여, 부팅 시간 10ms 이하, 메모리 풋프린트 5MB 이하의 극한 효율을 달성할 것이다.

3. **AI-Driven OS 최적화**: 머신러닝 기반의 예측적 자원 할당, 워크로드 특성 분석을 통한 자동 스케줄링 튜닝, 이상 징후 탐지 및 자동 복구가 OS의 표준 기능으로 통합될 것이다.

4. **양자 컴퓨팅과의 공존**: 양자 컴퓨터 제어를 위한 특수 OS(Quantum OS)가 등장하고, 하이브리드 클래식-양자 워크로드를 관리하는 통합 운영체제가 연구될 것이다.

#### 참고 표준/가이드

- **POSIX.1-2017 (IEEE Std 1003.1)**: 유닉스/리눅스 계열 OS의 시스템 인터페이스 표준
- **ISO/IEC 9945**: POSIX 국제 표준 규격
- **LSB (Linux Standard Base)**: 리눅스 배포판 간 호환성 표준
- **FHS (Filesystem Hierarchy Standard)**: 유닉스 파일 시스템 계층 구조 표준
- **NIST SP 800-53**: 연방 정보 시스템 보안 통제 가이드 (OS 보안 설정)

---

### 관련 개념 맵 (Knowledge Graph)

- [커널 아키텍처](@/studynotes/2_operating_system/1_os_overview/22_kernel_role.md): 운영체제의 핵심인 커널의 역할과 모놀리식/마이크로커널 구조 비교
- [시스템 콜](@/studynotes/2_operating_system/1_os_overview/13_system_call.md): 사용자 공간과 커널 공간 간의 인터페이스 메커니즘
- [다중 프로그래밍](@/studynotes/2_operating_system/1_os_overview/2_multiprogramming.md): CPU 이용률 극대화를 위한 핵심 기법
- [시분할 시스템](@/studynotes/2_operating_system/1_os_overview/3_time_sharing_system.md): 실시간 대화형 컴퓨팅을 위한 스케줄링 기법
- [듀얼 모드](@/studynotes/2_operating_system/1_os_overview/11_dual_mode.md): 보호와 격리를 위한 하드웨어 지원 메커니즘

---

### 어린이를 위한 3줄 비유 설명

1. 운영체제는 **'수퍼마켓의 똑똑한 매니저'**예요. 매장에는 사과(CPU), 바나나(메모리), 우유(저장공간) 같은 물건들이 한정되어 있지만, 매니저는 모든 손님(프로그램)이 공평하게 물건을 살 수 있게 도와줘요.

2. 매니저는 손님이 줄을 서면 **'누가 먼저 왔는지'**와 **'얼마나 급한 손님인지'**를 생각해서 순서를 정해요. 덕분에 한 손님이 물건을 독차지하지 않고, 모든 손님이 빠르고 즐겁게 쇼핑을 마칠 수 있답니다.

3. 또 매니저는 **'물건이 어디 있는지'** 손님들이 쉽게 찾을 수 있게 안내판을 만들어줘요. 손님들은 복잡한 창고 구조를 몰라도 안내판만 보고 원하는 물건을 찾을 수 있어서 정말 편해요!
