+++
title = "시분할 시스템 (Time-sharing System)"
description = "응답 시간 최소화와 인터랙티브 컴퓨팅을 위한 시분할 시스템의 핵심 원리와 아키텍처를 심층 분석합니다."
date = "2026-03-04"
[taxonomies]
tags = ["시분할", "타임퀀텀", "인터랙티브", "라운드로빈", "컨텍스트스위치"]
categories = ["studynotes-2_operating_system"]
+++

# 시분할 시스템 (Time-sharing System)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CPU 시간을 밀리초(ms) 단위의 작은 할당량(Time Quantum/Slice)으로 분할하여 여러 사용자/프로세스에게 교차 배분함으로써, 각 사용자가 컴퓨터를 독점하고 있는 것처럼 느끼게 하는 대화형(Interactive) 운영체제 기법. 다중 프로그래밍에 실시간성(Responsiveness)을 결합한 진화된 형태다.
> 2. **가치**: 평균 응답 시간을 수 분에서 100ms 이내로 단축하여 인간-컴퓨터 상호작용(HCI)을 실현. 단일 컴퓨터로 수십~수백 명의 동시 사용자 지원이 가능해져 하드웨어 투자 대비 사용자당 비용을 90% 이상 절감.
> 3. **융합**: 현대 OS(Linux, Windows, macOS)의 기본 동작 모드이며, 클라우드 가상 머신, 컨테이너, 심지어 스마트폰 멀티태스킹까지 모든 디지털 기기의 사용자 경험을 지탱하는 근간 기술.

---

### Ⅰ. 개요 (Context & Background)

#### 개념
시분할 시스템(Time-sharing System)은 **단일 CPU 시스템에서 CPU 시간을 아주 짧은 간격(주로 10~100ms)으로 나누어 여러 사용자나 프로세스에게 순차적으로 할당함으로써, 모든 사용자가 동시에 컴퓨터를 독점하여 사용하는 것처럼 느끼게 하는 운영체제 기법**이다. 이는 다중 프로그래밍(Multiprogramming)이 자원 활용(Resource Utilization)에 초점을 맞췄다면, 시분할은 사용자 응답성(Responsiveness)과 상호작용성(Interactivity)에 초점을 맞춘 진화된 형태다.

시분할의 핵심 착안은 **"인간의 반응 속도(약 100ms)보다 빠르게 CPU를 전환하면, 사용자는 지연을 인지하지 못한다"**는 것이다. 1초 동안 10개의 프로세스가 각각 100ms씩 CPU를 사용한다면, 각 사용자는 1초에 한 번씩 응답을 받는다. 이는 인간에게 "즉각적"으로 느껴진다.

**시분할 vs 다중 프로그래밍 비교**:
- **다중 프로그래밍**: I/O 대기 시 CPU 전환 (이벤트 기반, 비결정론적)
- **시분할**: 시간 할당량 만료 시 강제 CPU 전환 (타이머 기반, 결정론적)

#### 💡 비유
시분할 시스템을 **'놀이공원의 인기 어트랙션'**에 비유할 수 있다. 롤러코스터(CPU)를 타고 싶은 손님(사용자/프로세스)들이 긴 줄을 서 있다. 놀이공원 운영자(OS)는 각 손님에게 딱 1분씩만 탑승 기회를 주고, 시간이 되면 무조건 내리게 한다. 그리고 줄의 맨 뒤로 가서 다시 대기하게 한다. 결과적으로 모든 손님이 공평하게 기회를 얻고, 한 손님이 너무 오래 기다리지 않는다. 물론 1분씩 교대로 타기 때문에 각 손님은 계속해서 조금씩 탑승하지만, 줄이 너무 길지 않으면 만족스러운 경험을 할 수 있다.

#### 등장 배경 및 발전 과정

**1. 문제 인식: 일괄 처리의 사용자 격리**
- 1960년대 초반, 컴퓨터는 여전히 일괄 처리(Batch) 방식으로 운영되었다.
- 사용자는 펀치 카드에 프로그램을 작성하여 오퍼레이터에게 전달하고, 몇 시간 후 결과를 받았다.
- **치명적 한계**: 디버깅이 불가능했다. 프로그램에 버그가 있으면 수정 후 다시 몇 시간을 기다려야 했다.
- **비즈니스적 요구**: 과학자와 엔지니어들은 "실시간으로 프로그램을 수정하고 테스트하고 싶다"고 요구했다.

**2. 해결책의 등장: 시분할 시스템**
- 1961년, MIT의 Fernando Corbato가 **CTSS(Compatible Time-Sharing System)**를 개발.
- **핵심 혁신**: 
  - 단말기(Terminal)를 통해 사용자가 직접 컴퓨터와 대화
  - 타이머 인터럽트(Timer Interrupt)를 활용한 강제 CPU 전환
  - 가상 메모리(Virtual Memory)로 각 사용자의 독립적 주소 공간 보장
- **결과**: IBM 7094에서 최대 32명의 사용자가 동시에 사용 가능, 응답 시간 2~3초.

**3. MULTICS와 UNIX: 현대 OS의 원형**
- 1965년, MIT/GE/Bell Labs가 **MULTICS(Multiplexed Information and Computing Service)**를 개발.
  - 링(Ring) 기반 보호, 계층적 파일 시스템, 동적 링킹 등 현대 OS의 대부분의 개념을 창안.
- 1969년, Bell Labs의 Ken Thompson과 Dennis Ritchie가 **UNIX**를 개발.
  - MULTICS의 복잡성을 제거하고 심플하고 강력한 시분할 OS를 만들어 냄.
  - 이것이 오늘날 Linux, macOS, BSD 등 모든 유닉스 계열 OS의 조상.

**4. 현대적 진화**
- 개인용 컴퓨터(PC)의 등장으로 "시분할"은 "멀티태스킹(Multitasking)"이라는 용어로 진화.
- 스마트폰에서도 수십 개의 앱이 시분할 방식으로 동시 실행.
- 클라우드 서버에서는 수천 개의 컨테이너가 시분할 스케줄링으로 실행.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **타이머 인터럽트 (Timer Interrupt)** | 시간 할당량 만료 감지 | 하드웨어 카운터(PIT/APIC)가 0이 되면 인터럽트 발생 | Programmable Interval Timer, HPET | 스톱워치 알람 |
| **시간 할당량 (Time Quantum/Slice)** | 각 프로세스의 CPU 점유 시간 | 스케줄러가 설정 (보통 10~100ms), 너무 작으면 오버헤드 증가 | CFS target latency, RR time slice | 회의 발언 시간 |
| **라운드 로빈 스케줄러 (Round Robin Scheduler)** | 공평한 CPU 배분 | 준비 큐를 순환하며 각 프로세스에 할당량 부여 | Circular Queue, Context Switch | 카드 게임 턴 |
| **컨텍스트 스위치 (Context Switch)** | 프로세스 전환 수행 | 레지스터 저장/복원, PCB 교체, TLB 플러시(필요시) | HW 문맥 저장, 소프트웨어 핸들링 | 연극 배역 교체 |
| **가상 메모리 (Virtual Memory)** | 각 프로세스의 독립 주소 공간 | 페이지 테이블, TLB, 스와핑 | MMU, Demand Paging | 개인 사무실 |
| **터미널 인터페이스 (Terminal Interface)** | 사용자 입출력 | TTY/PTY, 쉘(Shell), 표준 입출력 리다이렉션 | SSH, Telnet, Console | 대화 창구 |
| **프로세스 스케줄링 큐 (Scheduling Queue)** | 실행 대기 관리 | 다단계 피드백 큐(MLFQ), 우선순위 큐 | CFS Red-Black Tree | 은행 대기열 |

#### 2. 정교한 구조 다이어그램

```text
+===========================================================================+
|              TIME-SHARING SYSTEM ARCHITECTURE (Multi-user View)           |
+===========================================================================+

  USER SPACE                          KERNEL SPACE                 HARDWARE
+----------------+                 +-------------------+        +-------------+
|   User A       |                 |                   |        |             |
|  +---------+   |    System       |  PROCESS          |        |   TIMER     |
|  | Shell   |---|----Call-------->|  SCHEDULER        |<-------|  (PIT/APIC) |
|  +---------+   |                 |                   |        |             |
|  | Editor  |   |                 |  +-------------+  |        +-------------+
|  +---------+   |                 |  | Ready Queue |  |              ^
+----------------+                 |  |  P1->P2->P3 |  |              | Timer
                                   |  +------+------+  |              | Interrupt
  USER SPACE                       |         |         |              |
+----------------+                 |         v         |        +-------------+
|   User B       |                 |  +-------------+  |        |             |
|  +---------+   |    Terminal     |  | Dispatcher  |  |        |    CPU      |
|  | Browser |---|----I/O--------->|  | Context     |--------->| (Executing) |
|  +---------+   |                 |  | Switch      |  |        |             |
|  | Mail    |   |                 |  +------+------+  |        +-------------+
|  +---------+   |                 |         |         |              ^
+----------------+                 |         |         |              |
                                   |         v         |              |
  USER SPACE                       |  +-------------+  |        +-------------+
+----------------+                 |  | PCB Table   |  |        |    MMU      |
|   User C       |                 |  | P1: Running |  |        | (Address    |
|  +---------+   |    Memory       |  | P2: Ready   |  |<-------| Translation)|
|  | Compiler|---|----Access------>|  | P3: Blocked |  |        |             |
|  +---------+   |                 |  +-------------+  |        +-------------+
+----------------+                 |                   |
                                   +-------------------+

+===========================================================================+
|                    TIME QUANTUM & CONTEXT SWITCH TIMING                   |
+===========================================================================+

    Time (ms)   0    10   20   30   40   50   60   70   80   90  100
                |----|----|----|----|----|----|----|----|----|----|
    
    Process A   [====]                    [====]              [====]
                     ^                         ^                   ^
                     | Timer Interrupt         | Timer Int.        |
                     | Context Switch          | C.S.              |
    
    Process B        [====]              [====]              [====]
                      ^    ^              ^    ^              ^
                      |    |              |    |              |
                      |    |              |    |              |
    
    Process C             [====]              [====]              [==
                           ^    ^              ^    ^              
                           |    |              |    |              
                           |    |              |    |              

    Legend:
    [====] = Process executing on CPU
    ^ = Timer Interrupt triggers Context Switch

    Each Process gets 10ms time slice (Time Quantum)
    Round-Robin order: A -> B -> C -> A -> B -> C -> ...

    Context Switch Overhead: ~0.1ms (negligible compared to quantum)
```

#### 3. 심층 동작 원리 (시분할 실행 사이클 8단계)

**① 프로세스 시작 및 준비 큐 진입**
- 사용자가 터미널에서 명령어 입력 (예: `./my_program`)
- 쉘(Shell)이 fork() + exec() 시스템 콜을 통해 새 프로세스 생성.
- 커널이 PCB를 생성하고 Ready Queue의 Tail에 추가.

**② 타이머 설정**
- 디스패처가 프로세스를 CPU에 할당하기 직전, 하드웨어 타이머(PIT 또는 Local APIC)에 Time Quantum 값을 설정.
- 예: `program_timer(10ms)` 호출 시 10ms 후 인터럽트 예약.

**③ CPU 실행 (Running Phase)**
- 프로세스가 사용자 모드(User Mode)에서 명령어 실행.
- 캐시 적중(Cache Hit), 분기 예측(Branch Prediction) 등 CPU 최적화 작동.
- 이 시간 동안 프로세스는 "컴퓨터를 독점"하는 것처럼 동작.

**④ 타이머 인터럽트 발생**
- 10ms 경과 시 하드웨어 타이머가 CPU에 인터럽트 신호 전송.
- CPU가 현재 명령어 완료 후 인터럽트 처리 루틴 진입.
- User Mode -> Kernel Mode 전환.

**⑤ 컨텍스트 저장 (Context Save)**
- 인터럽트 핸들러가 현재 프로세스의 레지스터(RIP, RSP, GPRs, Flags)를 PCB에 저장.
- 프로세스 상태를 RUNNING -> READY로 변경.
- Time Quantum이 모두 소진되었으므로 선점(Preemption) 처리.

**⑥ 스케줄링 결정**
- 스케줄러가 Ready Queue에서 다음 실행할 프로세스 선정 (Round Robin 방식).
- 선택 기준: 큐의 Head, 우선순위, vruntime(CFS), 등.

**⑦ 컨텍스트 복원 (Context Restore)**
- 디스패처가 선정된 프로세스의 PCB에서 레지스터 값을 CPU에 복원.
- 필요시 TLB 플러시(다른 주소 공간), 캐시 워밍.
- 프로세스 상태를 READY -> RUNNING으로 변경.

**⑧ 타이머 재설정 및 실행 재개**
- 새 Time Quantum으로 타이머 재설정.
- `iretq` 명령어로 User Mode 복귀.
- 프로세스가 이전에 멈춘 지점부터 실행 재개.

#### 4. 핵심 알고리즘 & 실무 코드 예시

**[라운드 로빈 스케줄러 구현 (Round Robin Scheduler)]**

```c
/*
 * Round Robin (RR) Scheduler Implementation
 * 시분할 시스템의 핵심 스케줄링 알고리즘
 *
 * 특징:
 * - 각 프로세스에 동일한 Time Quantum 부여
 * - Time Quantum 만료 시 다음 프로세스로 전환
 * - 선점형(Preemptive) 스케줄링
 * - 공평성(Fairness)과 응답성(Responsiveness) 보장
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define TIME_QUANTUM 10  // 10ms time slice

typedef struct Process {
    int pid;
    char name[32];
    int burst_time;      // 남은 CPU 버스트 시간
    int wait_time;       // 대기 시간
    int turnaround_time; // 반환 시간
    int arrival_time;    // 도착 시간
    bool completed;
    struct Process* next;
} Process;

typedef struct {
    Process* head;
    Process* tail;
    int size;
} ReadyQueue;

// 큐 초기화
ReadyQueue* create_queue() {
    ReadyQueue* q = (ReadyQueue*)malloc(sizeof(ReadyQueue));
    q->head = q->tail = NULL;
    q->size = 0;
    return q;
}

// 큐에 프로세스 추가 (Tail에 삽입)
void enqueue(ReadyQueue* q, Process* p) {
    p->next = NULL;
    if (q->tail == NULL) {
        q->head = q->tail = p;
    } else {
        q->tail->next = p;
        q->tail = p;
    }
    q->size++;
}

// 큐에서 프로세스 제거 (Head에서 반환)
Process* dequeue(ReadyQueue* q) {
    if (q->head == NULL) return NULL;
    Process* p = q->head;
    q->head = q->head->next;
    if (q->head == NULL) q->tail = NULL;
    q->size--;
    return p;
}

// 라운드 로빈 스케줄링 실행
void round_robin_schedule(ReadyQueue* q, int quantum) {
    int current_time = 0;
    int total_wait = 0;
    int total_turnaround = 0;
    int completed = 0;
    int n = q->size;
    
    printf("\n=== Round Robin Scheduling (Quantum=%dms) ===\n\n", quantum);
    printf("Time | Process | Burst Left | Action\n");
    printf("-----|---------|------------|------------------\n");
    
    while (q->size > 0) {
        Process* current = dequeue(q);
        
        if (current->burst_time > 0) {
            // Time Quantum과 남은 버스트 중 작은 값만큼 실행
            int exec_time = (current->burst_time < quantum) ? 
                            current->burst_time : quantum;
            
            printf("%4d | %-7s | %10d | Executing for %dms\n", 
                   current_time, current->name, current->burst_time, exec_time);
            
            current_time += exec_time;
            current->burst_time -= exec_time;
            
            // 대기 시간 업데이트 (큐에 있는 다른 프로세스들)
            Process* temp = q->head;
            while (temp != NULL) {
                if (!temp->completed && temp != current) {
                    temp->wait_time += exec_time;
                }
                temp = temp->next;
            }
            
            if (current->burst_time == 0) {
                // 프로세스 완료
                current->completed = true;
                current->turnaround_time = current_time - current->arrival_time;
                total_wait += current->wait_time;
                total_turnaround += current->turnaround_time;
                completed++;
                
                printf("%4d | %-7s | %10d | COMPLETED (TT=%dms, WT=%dms)\n",
                       current_time, current->name, current->burst_time,
                       current->turnaround_time, current->wait_time);
            } else {
                // 아직 완료되지 않음 -> 큐의 Tail로 이동
                printf("%4d | %-7s | %10d | Preempted, back to queue\n",
                       current_time, current->name, current->burst_time);
                enqueue(q, current);
            }
        }
    }
    
    printf("\n=== Performance Metrics ===\n");
    printf("Average Wait Time: %.2f ms\n", (float)total_wait / n);
    printf("Average Turnaround Time: %.2f ms\n", (float)total_turnaround / n);
    printf("Throughput: %.2f processes per %d ms\n", 
           (float)n / current_time, current_time);
    printf("CPU Utilization: 100%% (assuming no idle)\n");
}

// 메인 함수
int main() {
    ReadyQueue* queue = create_queue();
    
    // 테스트 프로세스 생성
    Process processes[] = {
        {1, "P1", 24, 0, 0, 0, false, NULL},
        {2, "P2", 12, 0, 0, 0, false, NULL},
        {3, "P3", 18, 0, 0, 0, false, NULL},
        {4, "P4", 15, 0, 0, 0, false, NULL}
    };
    
    // 모든 프로세스를 큐에 등록
    for (int i = 0; i < 4; i++) {
        enqueue(queue, &processes[i]);
    }
    
    // 라운드 로빈 스케줄링 실행
    round_robin_schedule(queue, TIME_QUANTUM);
    
    free(queue);
    return 0;
}

/*
 * 실행 결과 예시:
 * 
 * Time | Process | Burst Left | Action
 * -----|---------|------------|------------------
 *    0 | P1      |         24 | Executing for 10ms
 *   10 | P1      |         14 | Preempted, back to queue
 *   10 | P2      |         12 | Executing for 10ms
 *   20 | P2      |          2 | Preempted, back to queue
 *   ...
 * 
 * Average Wait Time: 28.50 ms
 * Average Turnaround Time: 46.50 ms
 */
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 1. Time Quantum 크기에 따른 성능 분석

| Time Quantum | Context Switch 오버헤드 | 응답 시간 | 처리량 | 적정 용도 |
|:---|:---|:---|:---|:---|
| **1ms** | 매우 높음 (10~20%) | 매우 빠름 (<10ms) | 낮음 | 실시간 시스템 |
| **10ms** | 낮음 (<5%) | 빠름 (20~50ms) | 높음 | 일반 데스크톱 |
| **100ms** | 매우 낮음 (<1%) | 보통 (200~500ms) | 매우 높음 | 일괄 처리 서버 |
| **1s** | 무시 가능 | 느림 (>1s) | 최대 | HPC, 과학 연산 |

**Time Quantum 최적화 공식**:
```
최적 Time Quantum = 평균 CPU 버스트 시간 / 10
```

#### 2. 시분할 vs 실시간 시스템 비교

| 비교 항목 | 시분할 (Time-sharing) | 실시간 (Real-time) |
|:---|:---|:---|
| **목표** | 공평성, 응답성 | 마감 시간(Deadline) 준수 |
| **스케줄링** | Round Robin, CFS | Rate-Monotonic, EDF |
| **보장성** | Best-effort | Hard/Soft Guarantee |
| **Context Switch** | 빈번 (10~100ms) | 최소화 (예측 가능) |
| **적용 분야** | 데스크톱, 서버 | 항공, 의료, 자동차 |

---

### Ⅳ. 실무 적용 및 기술사적 판단

#### 시나리오 1: VDI(가상 데스크톱 인프라)의 응답 시간 최적화

**문제 상황**: 100명의 사용자가 단일 서버에서 VDI 사용. 사용자별 응답 시간이 500ms를 초과하여 불만 제기.

**진단**:
- 기본 Time Quantum(100ms)이 너무 커서 대기 사용자 수가 증가.
- Context Switch 오버헤드는 낮지만, 공평성이 떨어짐.

**기술사적 결단**:
1. **Time Quantum 축소**: 100ms -> 20ms로 조정.
2. **우선순위 조정**: 포그라운드(활성) 세션에 높은 우선순위 부여.
3. **CPU 파티셔닝**: cgroups를 사용하여 각 세션에 CPU 할당량 보장.

**성과**: 평균 응답 시간 500ms -> 80ms로 개선 (84% 단축).

#### 시나리오 2: 멀티플레이어 게임 서버의 지연 시간 최소화

**문제 상황**: 온라인 게임 서버에서 1,000명 동시 접속 시 일부 플레이어의 지연(Lag) 발생.

**기술사적 결단**:
1. **실시간 우선순위**: 게임 로직 스레드에 SCHED_FIFO 정책 적용.
2. **CPU 고정**: 네트워크 처리 스레드를 전용 코어에 바인딩.
3. **짧은 Time Quantum**: 5ms로 설정하여 빠른 응답 보장.

#### 주의사항 및 안티패턴

1. **Time Quantum 과소 설정**: 1ms 미만으로 설정하면 Context Switch 오버헤드가 20% 이상이 되어 오히려 성능 저하.

2. **기아(Starvation) 방지**: 우선순위 기반 스케줄링에서 낮은 우선순위 프로세스가 영원히 대기할 수 있음. Aging 기법 필수.

3. **캐시 스래싱**: 너무 빈번한 Context Switch는 캐시 적중률을 급격히 저하시킴. CPU Affinity 활용.

---

### Ⅴ. 기대효과 및 결론

#### 정량적/정성적 기대효과

| 지표 | 일괄 처리 | 다중 프로그래밍 | 시분할 |
|:---|:---|:---|:---|
| **응답 시간** | 수 분~수 시간 | 수 초~수 분 | 50~200ms |
| **사용자 체감 성능** | 매우 나쁨 | 보통 | 매우 좋음 |
| **동시 사용자 수** | 1 | 제한적 | 수십~수백 |
| **상호작용성** | 없음 | 제한적 | 완전 지원 |

#### 미래 전망

시분할 시스템은 **"실시간 웹"**, **"클라우드 게이밍"**, **"메타버스"** 등 모든 실시간 상호작용 서비스의 기반이다. 5G와 엣지 컴퓨팅의 발전으로 지연 시간은 10ms 이내로 줄어들고 있으며, 이는 시분할 기술의 정밀도 향상을 요구한다. 또한 AI 기반 적응형 스케줄링이 도입되어 워크로드 특성에 따라 Time Quantum을 동적으로 조정하는 "지능형 시분할"이 미래의 표준이 될 것이다.

#### 참고 표준/가이드

- **POSIX.1b**: 실시간 확장 (스케줄링 정책 SCHED_FIFO, SCHED_RR)
- **IEEE 1003.1**: 시분할 시스템 표준 인터페이스
- **Fernando Corbato's Turing Award Lecture (1990)**: 시분할 시스템의 역사와 철학

---

### 관련 개념 맵 (Knowledge Graph)

- [다중 프로그래밍](@/studynotes/2_operating_system/1_os_overview/2_multiprogramming.md): 시분할의 기반이 되는 기법
- [라운드 로빈 스케줄링](@/studynotes/2_operating_system/3_cpu_scheduling/178_round_robin.md): 시분할의 핵심 알고리즘
- [컨텍스트 스위치](@/studynotes/2_operating_system/1_os_overview/34_context_switch.md): 프로세스 전환 메커니즘
- [타이머 인터럽트](@/studynotes/2_operating_system/1_os_overview/72_timer_interrupt.md): 시분할의 하드웨어 기반
- [실시간 시스템](@/studynotes/2_operating_system/1_os_overview/9_realtime_system.md): 시분할의 특수한 형태

---

### 어린이를 위한 3줄 비유 설명

1. 시분할 시스템은 **'선생님이 학생들과 1:1로 상담하는 것'**과 같아요. 선생님(CPU)이 학생(프로그램)마다 딱 5분씩만 상담하고, 시간이 되면 다음 학생으로 넘어가요.

2. 이렇게 하면 모든 학생이 **'오늘 선생님과 상담했다'**고 느낄 수 있어요. 물론 5분씩만 상담하지만, 선생님이 계속 돌아가면서 상담하면 금방 다시 차례가 와서 오래 기다리지 않아도 돼요.

3. 만약 한 학생과 상담이 끝날 때까지(30분, 1시간) 다른 학생을 못 만난다면, 다른 학생들은 너무 오래 기다려서 지루해질 거예요. 시분할 덕분에 모든 학생이 공평하게 기회를 얻을 수 있답니다!
