+++
title = "다중 프로그래밍 (Multiprogramming)"
description = "CPU 활용도 극대화를 위한 다중 프로그래밍 기법의 핵심 원리와 아키텍처를 심층 분석합니다."
date = "2026-03-04"
[taxonomies]
tags = ["다중프로그래밍", "CPU이용률", "메모리상주", "I/O버퍼링"]
categories = ["studynotes-2_operating_system"]
+++

# 다중 프로그래밍 (Multiprogramming)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단일 CPU 시스템에서 여러 프로그램을 메모리에 동시에 상주시켜, I/O 대기 중인 프로세스의 CPU를 다른 프로세스에 할당함으로써 CPU 유휴 시간(Idle Time)을 최소화하는 메모리 관리 패러다임. 운영체제가 프로세스 전환(Context Switch)을 능동적으로 수행하여 하드웨어 자원의 점유율을 극대화한다.
> 2. **가치**: 일괄 처리 시스템 대비 CPU 이용률을 20% 미만에서 80% 이상으로 약 4배 이상 향상시키며, 처리량(Throughput)을 단위 시간당 작업 수 기준으로 3~5배 증대. 하드웨어 투자 대비 ROI를 획기적으로 개선한다.
> 3. **융합**: 시분할 시스템(Time-sharing)의 기반 기술로 진화하였으며, 현대 멀티태스킹 OS, 하이퍼바이저 기반 가상화, 그리고 컨테이너 오케스트레이션(Kubernetes)의 근간이 되는 핵심 개념이다.

---

### Ⅰ. 개요 (Context & Background)

#### 개념
다중 프로그래밍(Multiprogramming)은 **단일 CPU 시스템에서 둘 이상의 프로그램을 주기억장치(Main Memory)에 동시에 적재(Load)하여, 실행 중인 프로세스가 I/O 연산 등으로 대기 상태(Blocked/Waiting)에 진입할 때 CPU를 다른 준비 상태(Ready)의 프로세스에 즉시 할당함으로써 CPU의 유휴 시간을 최소화하는 운영체제 기법**이다. 이는 단순한 프로그램 동시 실행이 아니라, CPU라는 가장 비싼 하드웨어 자원의 활용률을 극한으로 끌어올리기 위한 경제적 필연성에서 탄생했다.

다중 프로그래밍의 핵심 통찰은 **"I/O 연산은 CPU 연산보다 10^6배 이상 느리다"**는 것이다. 디스크 읽기(약 10ms) 동안 CPU는 수백만 개의 명령어를 실행할 수 있다. 따라서 단일 프로그램이 I/O를 기다리는 동안 CPU를 방치하는 것은 슈퍼컴퓨터를 탁상시계로 사용하는 것과 같은 낭비다. 다중 프로그래밍은 이 낭비를 제거한다.

#### 💡 비유
다중 프로그래밍을 **'요리사 한 명이 여러 요리를 동시에 진행하는 주방'**에 비유할 수 있다. 요리사(CPU)가 파스타 소스를 끓이며(Porcess A) 10분간 대기해야 한다면, 그 사이에 샐러드를 만들고(Process B), 스테이크를 굽는(Process C) 작업을 번갈아 수행한다. 요리사가 쉬지 않고 계속 일하게 함으로써 전체 요리 완성 시간을 단축하고, 주방의 생산성을 극대화하는 것이다. 단, 요리사가 동시에 두 가지 요리를 할 수는 없지만(단일 CPU), 전환(Switching)이 매우 빠르면 거의 동시에 진행되는 것처럼 보인다.

#### 등장 배경 및 발전 과정

**1. 문제 인식: 일괄 처리 시스템의 치명적 한계**
- 1950~60년대 초반 일괄 처리(Batch Processing) 시스템에서는 한 번에 하나의 작업(Job)만 실행되었다.
- I/O 바운드 작업(카드 리더, 프린터, 테이프 드라이브)이 CPU를 점유하면, CPU는 I/O 완료를 기다리며 완전히 유휴 상태가 되었다.
- **구체적 사례**: IBM 7094에서 1,000개의 카드를 읽는 데 약 30초 소요. 이 시간 동안 CPU는 아무것도 하지 않고 대기.
- **경제적 타격**: 당시 메인프레임 가격이 현대 가치로 수백억 원에 달했음을 고려하면, CPU 이용률 10% 이하는 기업에게 치명적 손실이었다.

**2. 해결책의 등장: 다중 프로그래밍**
- 1960년대 중반, IBM OS/360의 MFT(Multiprogramming with Fixed Tasks)와 MVT(Multiprogramming with Variable Tasks)가 최초의 상용 다중 프로그래밍 OS로 등장.
- **핵심 혁신**: 메모리를 여러 파티션으로 분할하여 여러 작업을 동시에 상주시키고, 인터럽트(Interrupt) 기반 I/O 완료 통지를 통해 CPU 전환을 자동화.
- **결과**: CPU 이용률이 20% 미만에서 70~80%로 급증.

**3. 진화: 시분할 시스템으로의 확장**
- 다중 프로그래밍은 여전히 일괄 처리 중심이었으며, 사용자와의 실시간 상호작용(Interactive)이 불가능했다.
- 1960년대 후반, MIT의 CTSS(Compatible Time-Sharing System)와 MULTICS가 다중 프로그래밍에 **시분할(Time-sharing)** 개념을 결합하여 현대 OS의 원형을 완성.

**4. 현대적 적용**
- 현대 OS(Linux, Windows, macOS)는 모두 다중 프로그래밍을 기본으로 작동.
- 클라우드 서버에서는 하이퍼바이저가 여러 VM(가상 머신)을 다중 프로그래밍 방식으로 스케줄링.
- 컨테이너(Docker, Kubernetes) 또한 동일한 원리로 단일 호스트에서 수백 개의 컨테이너를 실행.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **메모리 파티셔닝 (Memory Partitioning)** | 여러 프로세스를 메모리에 동시 상주 | 고정 파티션(Fixed), 가변 파티션(Variable), 세그멘테이션, 페이징 | MFT, MVT, Virtual Memory | 오피스 칸막이 |
| **작업 큐 (Job Queue)** | 실행 대기 프로세스 관리 | FIFO, Priority, Multi-level Queue | Ready Queue, Wait Queue | 은행 대기번호표 |
| **I/O 인터럽트 핸들러 (I/O Interrupt Handler)** | I/O 완료 시 CPU 통지 | 벡터드 인터럽트, ISR(Interrupt Service Routine) | PIC, APIC, MSI | 알림 서비스 |
| **디스패처 (Dispatcher)** | CPU 제어권 이양 | Context Save/Restore, 모드 전환, PCB 교체 | Context Switch | 릴레이 경기 바통 |
| **프로세스 상태 관리자 (Process State Manager)** | 프로세스 생애주기 제어 | New -> Ready -> Running -> Blocked -> Terminated | PCB, State Diagram | 공항 관제탑 |
| **스케줄러 (Scheduler)** | 다음 실행 프로세스 선정 | FCFS, SJF, Priority, Round Robin | Short-term, Medium-term, Long-term | 심사위원단 |
| **I/O 버퍼 (I/O Buffer)** | 속도 차이 완충 | Circular Buffer, Double Buffering, Spooling | DMA, Ring Buffer | 대기실 |

#### 2. 정교한 구조 다이어그램

```text
+===========================================================================+
|              MULTIPROGRAMMING ARCHITECTURE - MEMORY & CPU FLOW            |
+===========================================================================+

   +-------------------+         +-------------------+
   |    JOB POOL       |         |   DISK STORAGE    |
   | (Disk Queue)      |         |  (Backing Store)  |
   +--------+----------+         +---------+---------+
            |                              ^
            | Job Scheduler                | I/O Request
            | (Long-term)                  |
            v                              |
   +--------+----------+         +---------+---------+
   |   READY QUEUE     |<--------|   WAIT QUEUES     |
   | (Process A, B, C) |         | (I/O Wait, Event)  |
   +--------+----------+         +---------+---------+
            |                              ^
            | CPU Scheduler                | I/O Complete
            | (Short-term)                 | Interrupt
            v                              |
   +--------+----------+         +---------+---------+
   |       CPU         |-------->|    I/O DEVICES    |
   |   (Executing)     |         | (Disk, Net, etc)  |
   |   Process A       |         +-------------------+
   +-------------------+

+===========================================================================+
|                    MEMORY PARTITION LAYOUT (Fixed Example)                |
+===========================================================================+

   +---------------------------+ 0x0000
   |      OPERATING SYSTEM     |  (Kernel Space)
   |    (Resident Monitor)     |
   +---------------------------+ 0x1000
   |      PARTITION 1          |  (User Process A - Running)
   |    64 KB Boundary         |    - Text Segment
   |                           |    - Data Segment
   |                           |    - Stack/Heap
   +---------------------------+ 0x11000
   |      PARTITION 2          |  (User Process B - Ready)
   |    64 KB Boundary         |    - Text Segment
   |                           |    - Data Segment
   |                           |    - Stack/Heap
   +---------------------------+ 0x21000
   |      PARTITION 3          |  (User Process C - Blocked)
   |    64 KB Boundary         |    - Text Segment
   |                           |    - Data Segment
   |                           |    - Stack/Heap
   +---------------------------+ 0x31000
   |      FREE SPACE           |  (Available for Allocation)
   +---------------------------+ 0x40000

+===========================================================================+
|                    PROCESS STATE TRANSITION DIAGRAM                       |
+===========================================================================+

                     +-------+
                     |  NEW  |
                     +---+---+
                         | Admission (Long-term Scheduler)
                         v
    +-----------+    +-------+    +-----------+
    |  BLOCKED  |<---| READY |<---| TERMINATED|
    | (Waiting) |    | (Queued)|   | (Exit)    |
    +-----+-----+    +---+---+    +-----------+
          ^              |              ^
          |              | Dispatch     | Exit
          | I/O Wait     v              |
          |         +-------+           |
          +---------|RUNNING|-----------+
         I/O Complete +-------+         |
                         |              |
                         +--------------+

   Key Transitions:
   1. NEW -> READY: Job Scheduler admits process to memory
   2. READY -> RUNNING: CPU Scheduler (Dispatcher) selects process
   3. RUNNING -> BLOCKED: Process initiates I/O or waits for event
   4. BLOCKED -> READY: I/O completes, interrupt wakes process
   5. RUNNING -> READY: Time quantum expires (preemptive)
   6. RUNNING -> TERMINATED: Process completes execution
```

#### 3. 심층 동작 원리 (다중 프로그래밍 실행 사이클 6단계)

**① 초기 적재 (Initial Loading)**
- 장기 스케줄러(Long-term Scheduler)가 작업 풀(Job Pool)에서 적절한 작업을 선정.
- 메모리 관리자가 가용 파티션에 프로세스를 적재하고 PCB(Process Control Block) 생성.
- 프로세스 상태를 NEW -> READY로 전이하고 Ready Queue의 Tail에 추가.

**② CPU 할당 (CPU Dispatch)**
- 단기 스케줄러(Short-term/CPU Scheduler)가 Ready Queue의 Head에서 프로세스 선정.
- 디스패처(Dispatcher)가 Context Switch를 수행: 현재 실행 중인 프로세스의 레지스터를 PCB에 저장, 선정된 프로세스의 PCB에서 레지스터 복원.
- 프로세스 상태를 READY -> RUNNING으로 전이.

**③ I/O 요청 발생 (I/O Request)**
- 실행 중인 프로세스가 read(), write() 등의 I/O 시스템 콜 호출.
- 커널이 I/O 요청을 장치 드라이버에 전달하고 DMA(Direct Memory Access) 전송 시작.
- 프로세스는 I/O 완료까지 대기해야 하므로 상태를 RUNNING -> BLOCKED로 전이.
- 해당 프로세스를 적절한 Wait Queue(Device Queue)로 이동.

**④ CPU 전환 (Context Switch)**
- CPU가 방출되었으므로 스케줄러가 즉시 Ready Queue에서 다음 프로세스를 선정.
- 새로운 프로세스에 CPU를 할당하고 실행 시작.
- **핵심**: 이 시점에서 CPU는 유휴 상태가 아니라 다른 유용한 작업을 수행 중.

**⑤ I/O 완료 및 인터럽트 (I/O Completion)**
- I/O 장치가 DMA 전송을 완료하면 CPU에 인터럽트(Interrupt) 신호 전송.
- CPU가 현재 작업을 중단하고 인터럽트 핸들러(ISR) 실행.
- ISR은 대기 중이던 프로세스의 상태를 BLOCKED -> READY로 전이하고 Ready Queue에 재등록.

**⑥ 재스케줄링 (Rescheduling)**
- 인터럽트 처리 후, 스케줄러가 Ready Queue를 재평가.
- 우선순위에 따라 방금 I/O가 완료된 프로세스가 즉시 실행될 수도, 대기할 수도 있음.
- 이 사이클이 모든 프로세스가 종료될 때까지 반복.

#### 4. 핵심 알고리즘 & 실무 코드 예시

**[다중 프로그래밍 환경의 프로세스 스케줄링 시뮬레이션]**

```python
"""
Multiprogramming Process Scheduler Simulation
다중 프로그래밍 환경에서 I/O 바운드와 CPU 바운드 프로세스의
상호작용을 시뮬레이션하는 코드

핵심 개념:
- I/O 바운드 프로세스: CPU 버스트가 짧고 I/O 버스트가 김
- CPU 바운드 프로세스: CPU 버스트가 길고 I/O 버스트가 짧음
- 다중 프로그래밍은 이 두 유형이 혼재할 때 최대 효과 발휘
"""

import heapq
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class ProcessState(Enum):
    NEW = 1
    READY = 2
    RUNNING = 3
    BLOCKED = 4
    TERMINATED = 5

@dataclass(order=True)
class Process:
    pid: int
    name: str
    cpu_bursts: List[int]  # CPU 실행 시간 리스트 (ms)
    io_bursts: List[int]   # I/O 대기 시간 리스트 (ms)
    priority: int = 0
    state: ProcessState = ProcessState.NEW
    current_burst_index: int = 0
    remaining_cpu: int = 0
    waiting_for_io_until: int = 0
    total_wait_time: int = 0
    total_cpu_time: int = 0
    
    def __post_init__(self):
        if self.cpu_bursts:
            self.remaining_cpu = self.cpu_bursts[0]

class MultiprogrammingScheduler:
    def __init__(self, degree_of_multiprogramming: int = 3):
        self.dom = degree_of_multiprogramming  # 메모리에 상주 가능한 최대 프로세스 수
        self.ready_queue: List[Process] = []
        self.waiting_queue: List[Process] = []
        self.current_process: Optional[Process] = None
        self.clock: int = 0
        self.cpu_idle_time: int = 0
        self.completed_processes: List[Process] = []
        
    def admit_process(self, process: Process):
        """장기 스케줄러: 프로세스를 메모리에 적재"""
        if len(self.ready_queue) + (1 if self.current_process else 0) < self.dom:
            process.state = ProcessState.READY
            heapq.heappush(self.ready_queue, (process.priority, process))
            print(f"[Clock {self.clock}] {process.name} admitted to memory")
        else:
            print(f"[Clock {self.clock}] Memory full, {process.name} waits in job pool")
    
    def schedule(self):
        """단기 스케줄러: 다음 실행할 프로세스 선정"""
        if not self.current_process and self.ready_queue:
            _, next_process = heapq.heappop(self.ready_queue)
            next_process.state = ProcessState.RUNNING
            self.current_process = next_process
            print(f"[Clock {self.clock}] {next_process.name} starts CPU burst")
    
    def execute(self, time_slice: int = 1):
        """CPU 실행 (1ms 단위)"""
        # I/O 완료 확인
        self.check_io_completion()
        
        if self.current_process:
            # CPU 실행
            self.current_process.remaining_cpu -= time_slice
            self.current_process.total_cpu_time += time_slice
            self.clock += time_slice
            
            # CPU 버스트 완료 확인
            if self.current_process.remaining_cpu <= 0:
                self.handle_cpu_burst_complete()
        else:
            # CPU 유휴
            self.cpu_idle_time += time_slice
            self.clock += time_slice
    
    def handle_cpu_burst_complete(self):
        """CPU 버스트 완료 시 처리"""
        proc = self.current_process
        proc.current_burst_index += 1
        
        # 더 이상 CPU 버스트가 없으면 종료
        if proc.current_burst_index >= len(proc.cpu_bursts):
            proc.state = ProcessState.TERMINATED
            self.completed_processes.append(proc)
            print(f"[Clock {self.clock}] {proc.name} TERMINATED")
        else:
            # I/O 대기로 전환
            io_duration = proc.io_bursts[proc.current_burst_index - 1]
            proc.waiting_for_io_until = self.clock + io_duration
            proc.state = ProcessState.BLOCKED
            self.waiting_queue.append(proc)
            print(f"[Clock {self.clock}] {proc.name} blocked for I/O ({io_duration}ms)")
        
        self.current_process = None
        self.schedule()  # 즉시 다음 프로세스 스케줄
    
    def check_io_completion(self):
        """I/O 완료 확인 및 프로세스 웨이크업"""
        completed = []
        for proc in self.waiting_queue:
            if proc.waiting_for_io_until <= self.clock:
                proc.state = ProcessState.READY
                # 다음 CPU 버스트 준비
                if proc.current_burst_index < len(proc.cpu_bursts):
                    proc.remaining_cpu = proc.cpu_bursts[proc.current_burst_index]
                heapq.heappush(self.ready_queue, (proc.priority, proc))
                completed.append(proc)
                print(f"[Clock {self.clock}] {proc.name} I/O complete, back to READY")
        
        for proc in completed:
            self.waiting_queue.remove(proc)
    
    def calculate_metrics(self):
        """성능 지표 계산"""
        total_turnaround = sum(
            self.clock for _ in self.completed_processes
        )
        total_wait = sum(p.total_wait_time for p in self.completed_processes)
        
        cpu_utilization = (self.clock - self.cpu_idle_time) / self.clock * 100
        throughput = len(self.completed_processes) / self.clock * 1000
        
        return {
            "CPU Utilization": f"{cpu_utilization:.1f}%",
            "Throughput": f"{throughput:.2f} processes/second",
            "Total Clock": f"{self.clock}ms",
            "CPU Idle Time": f"{self.cpu_idle_time}ms"
        }

# 시뮬레이션 실행 예시
if __name__ == "__main__":
    scheduler = MultiprogrammingScheduler(degree_of_multiprogramming=3)
    
    # I/O 바운드 프로세스 (짧은 CPU, 긴 I/O)
    p1 = Process(pid=1, name="TextEditor", 
                 cpu_bursts=[5, 3, 4, 2], 
                 io_bursts=[20, 15, 25], priority=1)
    
    # CPU 바운드 프로세스 (긴 CPU, 짧은 I/O)
    p2 = Process(pid=2, name="Compiler", 
                 cpu_bursts=[50, 30, 40], 
                 io_bursts=[5, 3], priority=2)
    
    # 혼합형 프로세스
    p3 = Process(pid=3, name="WebServer", 
                 cpu_bursts=[10, 8, 12, 6, 5], 
                 io_bursts=[10, 12, 8, 5], priority=1)
    
    scheduler.admit_process(p1)
    scheduler.admit_process(p2)
    scheduler.admit_process(p3)
    
    while len(scheduler.completed_processes) < 3 and scheduler.clock < 500:
        scheduler.execute()
        scheduler.schedule()
    
    print("\n=== Performance Metrics ===")
    for k, v in scheduler.calculate_metrics().items():
        print(f"{k}: {v}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 1. 다중 프로그래밍 vs 일괄 처리 vs 시분할 비교

| 비교 항목 | 일괄 처리 (Batch) | 다중 프로그래밍 (Multiprogramming) | 시분할 (Time-sharing) |
|:---|:---|:---|:---|
| **메모리 상주 프로세스** | 1개 | N개 (제한적) | N개 (동적) |
| **CPU 전환 트리거** | 작업 종료 시 | I/O 대기 시 | 시간 할당량 만료 + I/O |
| **CPU 이용률** | 10~20% | 70~90% | 80~95% |
| **응답 시간** | 수 분 ~ 수 시간 | 수 초 ~ 수 분 | 100ms 이내 |
| **상호작용성** | 없음 | 제한적 | 실시간 대화형 |
| **복잡도** | 낮음 | 중간 | 높음 |
| **대표 시스템** | IBM 7094 | IBM OS/360 MFT | UNIX, CTSS |

#### 2. 다중 프로그래밍의 정도(Degree of Multiprogramming)별 성능 분석

| DOM (메모리 상주 프로세스 수) | CPU 이용률 | 스래싱(Thrashing) 위험 | 메모리 요구량 | 적정 용도 |
|:---|:---|:---|:---|:---|
| 1 (단일 프로그래밍) | 15~25% | 없음 | 최소 | 임베디드, RTOS |
| 2~3 | 60~75% | 매우 낮음 | 중간 | 데스크톱 |
| 4~8 | 80~90% | 낮음 | 높음 | 서버 |
| 16~32 | 90~95% | 중간 | 매우 높음 | 대규모 서버 |
| 64+ | 95%+ (이론적) | 높음 | 극히 높음 | HPC, 클라우드 |

---

### Ⅳ. 실무 적용 및 기술사적 판단

#### 시나리오 1: 메인프레임에서의 다중 프로그래밍 최적화

**문제 상황**: 은행 메인프레임에서 야간 배치 작업의 처리 시간이 SLA(4시간)를 초과. CPU 이용률은 40%에 불과.

**진단**:
- 대부분의 작업이 I/O 바운드(DB 조회, 파일 읽기)인데도 DOM이 2로 설정되어 있음.
- I/O 대기 중인 작업이 CPU를 점유하지 않음에도 다른 작업이 메모리에 없어 CPU가 유휴 상태.

**기술사적 결단**:
1. **DOM 증대**: 2 -> 8로 증가하여 더 많은 작업을 메모리에 상주.
2. **I/O 중첩(Overlapping)**: 여러 작업의 I/O를 병렬로 처리하도록 I/O 채널(Channel) 증설.
3. **작업 순서 최적화**: I/O 집약적 작업과 CPU 집약적 작업을 교차 배치.

**성과**: CPU 이용률 40% -> 85% 향상, 배치 완료 시간 4시간 -> 1.5시간 단축.

#### 시나리오 2: 클라우드 VM 인스턴스의 vCPU 오버커밋

**문제 상황**: 퍼블릭 클라우드에서 물리 CPU 32코어에 128 vCPU를 할당(4배 오버커밋). 일부 VM에서 CPU 경합(Steal Time) 발생.

**진단**:
- 모든 VM이 동시에 CPU를 요구하면 다중 프로그래밍 큐가 폭주.
- 과도한 Context Switch로 인해 캐시 효율 저하.

**기술사적 결단**:
1. **CPU Pinning**: 실시간성이 중요한 VM은 전용 코어에 바인딩.
2. **CPU Quota**: cgroups를 통해 각 VM의 CPU 사용량 상한 설정.
3. **버스트 가능(Burstable) VM**: 일반 VM은 기본 할당량 이상 사용 시 경쟁 허용.

#### 주의사항 및 안티패턴

1. **스래싱(Thrashing)**: DOM을 과도하게 높이면 각 프로세스의 Working Set이 메모리에 못 들어가 빈번한 페이지 폴트 발생 -> CPU가 페이지 교체에만 몰두 -> 오히려 CPU 이용률 급락.

2. **기아(Starvation)**: 우선순위 기반 스케줄링에서 낮은 우선순위 프로세스가 영원히 실행되지 않을 수 있음. Aging 기법으로 방지.

3. **교착 상태(Deadlock)**: 여러 프로세스가 상호 배제 자원을 점유한 채 대기하면 시스템 전체가 멈출 수 있음. 교착 상태 탐지 및 예방 메커니즘 필수.

---

### Ⅴ. 기대효과 및 결론

#### 정량적/정성적 기대효과

| 지표 | 일괄 처리 | 다중 프로그래밍 | 개선율 |
|:---|:---|:---|:---|
| **CPU 이용률** | 15~25% | 75~90% | +300~400% |
| **처리량 (Jobs/hr)** | 12 | 50 | +317% |
| **평균 대기 시간** | 30분 | 5분 | -83% |
| **하드웨어 ROI** | 20% | 85% | +325% |

#### 미래 전망

다중 프로그래밍의 핵심 원리는 현대 컴퓨팅의 모든 영역에서 여전히 유효하다. 클라우드 네이티브 환경에서는 **컨테이너 스케줄러(Kubernetes)**가, 서버리스에서는 **Function-as-a-Service 런타임**이 다중 프로그래밍의 역할을 수행한다. GPU 컴퓨팅에서는 **스트림 멀티프로세서(SM)**가 수천 개의 스레드를 다중 프로그래밍 방식으로 스위칭한다. 이 원리를 이해하는 것은 모든 시스템 성능 최적화의 출발점이다.

#### 참고 표준/가이드

- **IBM OS/360 MFT/MVT**: 최초의 상용 다중 프로그래밍 OS
- **POSIX.1**: 다중 프로세스 관리 표준 API (fork, exec, wait)
- **IEEE 1003.1b**: 실시간 확장 (메모리 고정, 스케줄링)

---

### 관련 개념 맵 (Knowledge Graph)

- [시분할 시스템](@/studynotes/2_operating_system/1_os_overview/3_time_sharing_system.md): 다중 프로그래밍의 진화된 형태
- [CPU 스케줄링](@/studynotes/2_operating_system/3_cpu_scheduling/_index.md): 다중 프로그래밍의 핵심 알고리즘
- [메모리 관리](@/studynotes/2_operating_system/6_main_memory/_index.md): 파티셔닝과 가상 메모리
- [인터럽트](@/studynotes/2_operating_system/1_os_overview/16_interrupt.md): I/O 완료 통지 메커니즘
- [프로세스 상태](@/studynotes/2_operating_system/2_process_thread/86_process_state.md): 다중 프로그래밍의 상태 머신

---

### 어린이를 위한 3줄 비유 설명

1. 다중 프로그래밍은 **'한 명의 요리사가 여러 요리를 번갈아 만드는 것'**과 같아요. 파스타 소스가 끓는 동안(컴퓨터가 다른 일을 하는 동안) 요리사는 가만히 있지 않고 샐러드를 만들거나 스테이크를 구워요.

2. 이렇게 하면 요리사(CPU)가 **'쉴 새 없이 바쁘게 일'**할 수 있어서, 식당(컴퓨터)에서 더 많은 손님(프로그램)에게 더 빨리 음식을 내어줄 수 있답니다.

3. 만약 요리사가 하나의 요리가 완전히 끝날 때까지 다른 요리를 전혀 하지 않는다면(다중 프로그래밍이 없다면), 식당은 엄청나게 비효율적이 되어 손님들이 너무 오래 기다려야 할 거예요!
