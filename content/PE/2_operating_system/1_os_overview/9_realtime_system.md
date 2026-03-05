+++
title = "실시간 시스템 (Real-time System)"
description = "엄격한 시간 제약을 만족해야 하는 Hard vs Soft 실시간 시스템의 아키텍처와 원리를 심츭 분석합니다."
date = "2026-03-04"
[taxonomies]
tags = ["실시간시스템", "RTOS", "Hard실시간", "Soft실시간", "마감시간"]
categories = ["studynotes-2_operating_system"]
+++

# 실시간 시스템 (Real-time System)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 작업의 논리적 정확성뿐만 아니라 **시간적 정확성(Temporal Correctness)**이 필수적인 컴퓨팅 시스템. 모든 작업은 엄격하게 정의된 마감 시간(Deadline) 내에 완료되어야 하며, 이를 보장하기 위해 결정론적 스케줄링(Rate-Monotonic, EDF), 우선순위 상속, 선점형 커널 등의 특수 기법을 적용한다.
> 2. **가치**: 항공기 제어, 자동차 브레이크 시스템, 의료 기기, 산업 자동화 등 인명 안전과 직결된 분야에서 99.999999% 이상의 타임라인 보장. 마감 시간 초과 시 단순한 성능 저하가 아니라 시스템 실패(Failure)로 간주.
> 3. **융합**: 자율주행차, 산업용 로봇, 스마트 팩토리, 5G 통신망, 의료 로봇 등 IoT와 AI가 결합된 안전-중요(Safety-Critical) 시스템의 핵심 기반. PREEMPT_RT 패치를 통해 Linux도 실시간성을 확보.

---

### Ⅰ. 개요 (Context & Background)

#### 개념
실시간 시스템(Real-time System)은 **작업의 완료가 논리적으로 올바른 것뿐만 아니라, 지정된 시간 제약(Time Constraint) 내에 이루어져야만 올바른 것으로 간주되는 컴퓨팅 시스템**을 의미한다. "실시간(Real-time)"이라는 용어는 "매우 빠른" 것을 의미하는 것이 아니라, **"예측 가능하고 보장된(Predictable & Guaranteed)"** 응답 시간을 의미한다.

**실시간 시스템의 핵심 개념**:
- **마감 시간(Deadline)**: 작업이 반드시 완료되어야 하는 시점
- **최악 실행 시간(WCET, Worst-Case Execution Time)**: 작업이 수행될 수 있는 최대 시간
- **결정론적 동작(Deterministic Behavior)**: 실행 시간의 상한이 보장됨
- **시간적 정확성(Temporal Correctness)**: 마감 시간 준수 여부가 정확성의 척도

**Hard vs Soft 실시간 시스템**:
- **Hard Real-time**: 마감 시간 초과 = 시스템 실패 (인명 피해, 환경 파괴)
- **Soft Real-time**: 마감 시간 초과 = 성능 저하 (사용자 경험 악화)

#### 💡 비유
실시간 시스템을 **'심장 박동 조절기(인공 심장)'**에 비유할 수 있다. 심장 박동 조절기는 1초에 한 번씩 정확하게 전기 신호를 보내야 한다. 신호를 0.1초 늦게 보내는 것은 단순한 "늦음"이 아니라 환자의 생명을 위협하는 "실패"다. 반면, 비디오 플레이어가 1초 늦게 프레임을 표시하는 것은 사용자가 약간 불편할 뿐 생명에는 지장이 없다. 전자가 Hard Real-time, 후자가 Soft Real-time이다.

#### 등장 배경 및 발전 과정

**1. 문제 인식: 범용 OS의 비결정론적 동작**
- 일반 운영체제(Windows, 일반 Linux)는 처리량(Throughput)과 공평성(Fairness)을 최적화.
- 인터럽트 지연, 스케줄링 지연, 페이지 폴트 등으로 인해 응답 시간이 불확정적.
- 안전-중요 시스템에서는 이러한 불확정성이 용납되지 않음.

**2. 실시간 OS(RTOS)의 등장**
- 1970~80년대, VxWorks, QNX, VRTX 등 전용 RTOS 개발.
- **핵심 혁신**:
  - 선점형 커널(Preemptible Kernel)
  - 우선순위 기반 스케줄링
  - 우선순위 상속(Priority Inheritance)
  - 고정 크기 메모리 할당
- **적용 분야**: 우주 항공, 군사, 산업 자동화

**3. 임베디드 RTOS의 대중화**
- 1990년대~2000년대, uC/OS, FreeRTOS, ThreadX 등 경량 RTOS 등장.
- 마이크로컨트롤러 기반 시스템(가전, 자동차 ECU)에 광범위하게 적용.

**4. 현대: 리눅스 실시간화와 자율주행**
- Linux PREEMPT_RT 패치로 Linux의 실시간성 확보.
- 자율주행차, 드론, 산업용 로봇에서 Hard/Soft 실시간 요구사항 혼재.
- 안전 표준(ISO 26262, IEC 61508)이 실시간성 요구사항 규정.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **실시간 스케줄러 (Real-time Scheduler)** | 마감 시간 준수를 위한 작업 순서 결정 | RM(Rate-Monotonic), EDF(Earliest Deadline First), DM(Deadline Monotonic) | POSIX SCHED_FIFO, SCHED_RR | 수술실 일정 관리자 |
| **선점형 커널 (Preemptible Kernel)** | 커널 모드에서도 선점 허용 | 커널 락을 뮤텍스로 변환, 인터럽트 스레드화 | PREEMPT_RT, RT-Linux | 언제든 중단 가능한 회의 |
| **우선순위 상속 (Priority Inheritance)** | 우선순위 역전 방지 | 락 보유자의 우선순위를 대기자의 우선순위로 상향 | PIP, PCP | 긴급 환자 우선 수술 |
| **고정 메모리 할당 (Fixed Memory Allocation)** | 메모리 단편화 및 할당 지연 방지 | 메모리 풀, 슬랩 할당, 동적 할당 금지 | Memory Pool, Heap Partition | 미리 준비된 도구 상자 |
| **실시간 시계 (Real-time Clock)** | 정밀한 타이밍 측정 및 제어 | 고해상도 타이머, 이벤트 카운터 | hrtimer, TSC, HPET | 스톱워치 |
| **인터럽트 처리 (Interrupt Handling)** | 낮은 지연의 이벤트 응답 | 인터럽트 스레드화, 우선순위 인터럽트 | Nested Interrupt, FIQ | 응급실 호출 시스템 |
| **WCET 분석 도구 (WCET Analysis Tools)** | 최악 실행 시간 예측 | 정적 분석, 하드웨어 모델링 | aiT, RapiTime, OTAWA | 시간 측정기 |

#### 2. 정교한 구조 다이어그램

```text
+===========================================================================+
|              REAL-TIME OPERATING SYSTEM ARCHITECTURE                      |
+===========================================================================+

   +-----------------------------------------------------------------------+
   |                    APPLICATION LAYER                                   |
   |  +-----------------+  +-----------------+  +-----------------+        |
   |  | Hard RT Task 1  |  | Hard RT Task 2  |  | Soft RT Task    |        |
   |  | (Brake Control) |  | (Engine Control)|  | (Infotainment)  |        |
   |  | Priority: 99    |  | Priority: 95    |  | Priority: 50    |        |
   |  | Period: 10ms    |  | Period: 20ms    |  | Aperiodic       |        |
   |  +--------+--------+  +--------+--------+  +--------+--------+        |
   +-----------|--------------------|--------------------|------------------+
               |                    |                    |
   +-----------v--------------------v--------------------v------------------+
   |                    REAL-TIME KERNEL                                    |
   |  +-----------------------------------------------------------------+ |
   |  |                  REAL-TIME SCHEDULER                            | |
   |  |  +-----------------------------------------------------------+  | |
   |  |  | Priority Queue (Ordered by Deadline/Priority)            |  | |
   |  |  | [P99: Task1] -> [P95: Task2] -> [P90: ...] -> [P50: Task] |  | |
   |  |  +-----------------------------------------------------------+  | |
   |  |                         |                                       | |
   |  |  +----------------------v--------------------------------------+ | |
   |  |  |           Scheduling Algorithms                              | | |
   |  |  |  - Rate-Monotonic (RM): static priority, period-based       | | |
   |  |  |  - EDF: dynamic priority, earliest deadline first          | | |
   |  |  |  - Deadline Monotonic (DM): deadline-based                  | | |
   |  |  +-------------------------------------------------------------+ | |
   |  +-----------------------------------------------------------------+ |
   |                                                                       |
   |  +-----------------------------------------------------------------+ |
   |  |              PREEMPTIBLE KERNEL SERVICES                       | |
   |  |  +-------------+  +-------------+  +-------------+             | |
   |  |  | Real-time  |  | Priority   |  | Interrupt   |             | |
   |  |  | Mutex      |  | Inheritance|  | Threading   |             | |
   |  |  +-------------+  +-------------+  +-------------+             | |
   |  +-----------------------------------------------------------------+ |
   |                                                                       |
   |  +-----------------------------------------------------------------+ |
   |  |                   TIMING SERVICES                               | |
   |  |  +------------------+  +------------------+                    | |
   |  |  | High-Resolution  |  | Periodic Timer   |                    | |
   |  |  | Timer (hrtimer)  |  | (Tickless)       |                    | |
   |  |  +------------------+  +------------------+                    | |
   |  +-----------------------------------------------------------------+ |
   +-----------------------------------------------------------------------+
               |                    |                    |
   +-----------v--------------------v--------------------v------------------+
   |                    HARDWARE LAYER                                      |
   |  +-------------+  +-------------+  +-------------+  +-------------+   |
   |  | CPU with   |  | High-Res   |  | Interrupt  |  | Memory     |   |
   |  | Determin-  |  | Clock/Timer|  | Controller |  | (Fixed)    |   |
   |  | istic Exec.|  | (HPET/TSC) |  | (APIC)     |  | Pools      |   |
   |  +-------------+  +-------------+  +-------------+  +-------------+   |
   +-----------------------------------------------------------------------+

+===========================================================================+
|                    HARD vs SOFT REAL-TIME COMPARISON                      |
+===========================================================================+

   HARD REAL-TIME SYSTEM:           SOFT REAL-TIME SYSTEM:
   
   Timeline:                         Timeline:
   |----|----|----|----|----|       |----|----|----|----|----|
   D    |    D    |    D    |       D    |    D    x    D    |
        |         |         |                  ^             |
        OK        OK        OK                 Missed        OK
                                              (degraded QoS)

   Characteristics:                  Characteristics:
   - Missing deadline = FAILURE      - Missing deadline = degraded
   - Safety-critical                 - Best-effort
   - Deterministic guarantee         - Statistical guarantee
   - Examples:                       - Examples:
     * Airbag deployment               * Video streaming
     * Anti-lock brakes                * Online gaming
     * Nuclear reactor control         * Audio playback
     * Pacemaker                       * UI responsiveness
```

#### 3. 심층 동작 원리 (실시간 스케줄링 6단계)

**① 작업 도착 및 분석**
- 주기적(Periodic) 또는 비주기적(Aperiodic) 작업이 시스템에 도착.
- 각 작업의 특성 파악: 주기(Period), 마감 시간(Deadline), WCET, 우선순위.

**② 스케줄러 분석(Schedulability Analysis)**
- Rate-Monotonic 분석: `U = sum(Ci/Ti) <= n(2^(1/n) - 1)` (Liu & Layland)
- 모든 작업이 마감 시간을 준수할 수 있는지 사전 검증.
- 불가능하면 작업 조정 또는 하드웨어 업그레이드 필요.

**③ 우선순위 할당**
- **RM(Rate-Monotonic)**: 주기가 짧을수록 높은 우선순위 (정적)
- **EDF(Earliest Deadline First)**: 마감 시간이 가까울수록 높은 우선순위 (동적)
- 우선순위 큐에 작업 등록.

**④ 선점형 스케줄링 실행**
- 가장 높은 우선순위 작업에 CPU 할당.
- 더 높은 우선순위 작업 도착 시 즉시 선점(Preemption).
- 커널 모드에서도 선점 가능(PREEMPT_RT).

**⑤ 우선순위 역전 방지**
- 낮은 우선순위 작업이 락을 보유 중인 경우 문제 발생 가능.
- **Priority Inheritance Protocol**: 락 보유자의 우선순위를 대기자의 우선순위로 일시 상향.
- 또는 **Priority Ceiling Protocol**: 락 획득 시 미리 최대 우선순위로 상향.

**⑥ 마감 시간 준수 확인**
- 작업 완료 시점과 마감 시간 비교.
- Hard RT: 초과 시 시스템 실패 처리(Fail-safe).
- Soft RT: 초과 시 QoS 저하 로깅.

#### 4. 핵심 알고리즘 & 실무 코드 예시

**[Rate-Monotonic 스케줄링 분석 및 구현]**

```c
/*
 * Rate-Monotonic (RM) Scheduling Analysis
 * 실시간 시스템에서 가장 널리 사용되는 정적 우선순위 스케줄링 알고리즘
 *
 * RM 스케줄링 규칙:
 * - 주기(Period)가 짧은 작업이 더 높은 우선순위를 가짐
 * - 선점형(Preemptive) 스케줄링
 * 
 * 스케줄 가능성 조건 (Liu & Layland, 1973):
 * U = sum(Ci/Ti) <= n * (2^(1/n) - 1)
 * 
 * 여기서:
 * - Ci: 작업 i의 최악 실행 시간 (WCET)
 * - Ti: 작업 i의 주기 (Period)
 * - n: 작업의 수
 * - U: CPU 이용률
 */

#include <stdio.h>
#include <math.h>
#include <stdbool.h>

#define MAX_TASKS 10

typedef struct {
    int id;
    double wcet;      // Worst-Case Execution Time (ms)
    double period;    // Period (ms)
    double deadline;  // Relative Deadline (ms)
    int priority;     // Assigned Priority (RM: higher = shorter period)
    double response_time;  // Worst-Case Response Time
} RTTask;

// Liu-Layland 스케줄 가능성 테스트 (충분 조건)
bool rm_sufficient_test(RTTask tasks[], int n) {
    double utilization = 0.0;
    
    printf("\n=== Rate-Monotonic Schedulability Analysis ===\n");
    printf("Task | WCET(C) | Period(T) | U = C/T\n");
    printf("-----|---------|-----------|--------\n");
    
    for (int i = 0; i < n; i++) {
        double u = tasks[i].wcet / tasks[i].period;
        utilization += u;
        printf(" T%d  |  %.2f   |   %.2f    | %.4f\n", 
               tasks[i].id, tasks[i].wcet, tasks[i].period, u);
    }
    
    // Liu-Layland 상한 계산
    double rm_bound = n * (pow(2.0, 1.0/n) - 1.0);
    
    printf("\nTotal Utilization: U = %.4f\n", utilization);
    printf("RM Bound (n=%d):   U_rm = %.4f\n", n, rm_bound);
    
    if (utilization <= rm_bound) {
        printf("Result: SCHEDULABLE (U <= U_rm)\n");
        return true;
    } else if (utilization <= 1.0) {
        printf("Result: MAYBE SCHEDULABLE (U_rm < U <= 1.0)\n");
        printf("        Need Response Time Analysis\n");
        return false;  // 추가 분석 필요
    } else {
        printf("Result: NOT SCHEDULABLE (U > 1.0)\n");
        return false;
    }
}

// 응답 시간 분석 (Response Time Analysis - 필요 조건이자 충분 조건)
double response_time_analysis(RTTask tasks[], int n, int task_index) {
    RTTask* task = &tasks[task_index];
    double R = task->wcet;  // 초기값
    double R_prev = 0;
    int iteration = 0;
    const int MAX_ITER = 100;
    
    printf("\n--- Response Time Analysis for Task T%d ---\n", task->id);
    
    while (R != R_prev && iteration < MAX_ITER) {
        R_prev = R;
        double interference = 0.0;
        
        // 더 높은 우선순위 작업들의 간섭 계산
        for (int i = 0; i < n; i++) {
            if (tasks[i].priority > task->priority) {
                // ceil(R / Ti) * Ci
                interference += ceil(R_prev / tasks[i].period) * tasks[i].wcet;
            }
        }
        
        R = task->wcet + interference;
        iteration++;
        
        printf("Iteration %d: R = %.2f ms\n", iteration, R);
        
        if (R > task->deadline) {
            printf("DEADLINE MISSED! R (%.2f) > D (%.2f)\n", 
                   R, task->deadline);
            return -1;  // 마감 시간 초과
        }
    }
    
    task->response_time = R;
    printf("Final Response Time: R = %.2f ms (Deadline = %.2f ms)\n",
           R, task->deadline);
    
    if (R <= task->deadline) {
        printf("DEADLINE MET!\n");
        return R;
    }
    
    return -1;
}

// RM 우선순위 할당 (주기가 짧을수록 높은 우선순위)
void assign_rm_priorities(RTTask tasks[], int n) {
    // 버블 정렬로 주기 기준 정렬 (오름차순)
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (tasks[j].period > tasks[j+1].period) {
                RTTask temp = tasks[j];
                tasks[j] = tasks[j+1];
                tasks[j+1] = temp;
            }
        }
    }
    
    // 우선순위 할당 (주기가 짧을수록 높은 우선순위)
    for (int i = 0; i < n; i++) {
        tasks[i].priority = n - i;  // 1 ~ n
    }
}

int main() {
    // 실시간 작업 정의 (예: 자동차 제어 시스템)
    RTTask tasks[MAX_TASKS] = {
        {1, 1.0, 10.0, 10.0, 0, 0},   // 브레이크 제어 (10ms 주기)
        {2, 2.0, 20.0, 20.0, 0, 0},   // 엔진 제어 (20ms 주기)
        {3, 5.0, 50.0, 50.0, 0, 0},   // 센서 융합 (50ms 주기)
        {4, 10.0, 100.0, 100.0, 0, 0} // 디스플레이 (100ms 주기)
    };
    int n = 4;
    
    // RM 우선순위 할당
    assign_rm_priorities(tasks, n);
    
    printf("=== Task Set After Priority Assignment ===\n");
    printf("Task | WCET | Period | Deadline | Priority\n");
    printf("-----|------|--------|----------|----------\n");
    for (int i = 0; i < n; i++) {
        printf(" T%d  | %.1f |  %.1f  |   %.1f   |    %d\n",
               tasks[i].id, tasks[i].wcet, tasks[i].period, 
               tasks[i].deadline, tasks[i].priority);
    }
    
    // 스케줄 가능성 테스트
    bool schedulable = rm_sufficient_test(tasks, n);
    
    // 응답 시간 분석 (필요 시)
    if (!schedulable) {
        printf("\n=== Detailed Response Time Analysis ===\n");
        for (int i = 0; i < n; i++) {
            if (response_time_analysis(tasks, n, i) < 0) {
                printf("\nSYSTEM NOT SCHEDULABLE!\n");
                return 1;
            }
        }
        printf("\nALL DEADLINES MET - SYSTEM SCHEDULABLE!\n");
    }
    
    return 0;
}
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 1. Hard vs Soft vs Firm 실시간 시스템 비교

| 구분 | Hard Real-time | Soft Real-time | Firm Real-time |
|:---|:---|:---|:---|
| **마감 시간 초과 결과** | 시스템 실패 | 성능 저하 | 부분적 결과 폐기 |
| **예시** | 에어백, 심박 조절기 | 비디오 스트리밍 | 주식 트레이딩 |
| **보장 수준** | 100% 결정론적 | 통계적 보장 | 대부분 보장 |
| **사용 OS** | VxWorks, QNX, FreeRTOS | Linux, Windows | Linux RT |
| **비용** | 높음 | 낮음 | 중간 |
| **인명 피해 가능성** | 높음 | 없음 | 낮음 |

#### 2. 실시간 스케줄링 알고리즘 비교

| 알고리즘 | 우선순위 결정 | 복잡도 | 이용률 상한 | 장점 | 단점 |
|:---|:---|:---|:---|:---|:---|
| **Rate-Monotonic (RM)** | 정적 (주기) | O(1) | n(2^(1/n)-1) | 단순, 예측 가능 | 차선 최적 |
| **EDF (Earliest Deadline First)** | 동적 (마감 시간) | O(n log n) | 100% | 최적 | 오버헤드, Domino Effect |
| **Deadline Monotonic (DM)** | 정적 (마감 시간) | O(1) | varies | 마감 < 주기 시 유리 | 일반성 낮음 |
| **Fixed Priority** | 설계자 지정 | O(1) | varies | 유연성 | 분석 어려움 |

---

### Ⅳ. 실무 적용 및 기술사적 판단

#### 시나리오 1: 자율주행차 실시간 제어 시스템

**문제 상황**: 자율주행차에서 감지->판단->제어 파이프라인이 100ms 내 완료되어야 함.

**기술사적 분석**:
- 카메라, 라이다 센서 데이터 수집: 20ms
- 객체 인식 AI 추론: 30ms
- 경로 계획: 20ms
- 차량 제어 명령: 10ms
- **총 WCET**: 80ms (여유 20ms)

**결단**:
1. **Linux PREEMPT_RT**: 커널의 선점성을 극대화하여 지연 예측.
2. **CPU 고정(Isolation)**: 제어 스레드를 전용 코어에 바인딩(`isolcpus`).
3. **SCHED_FIFO**: 실시간 스케줄링 정책 적용.
4. **우선순위 상속 뮤텍스**: 우선순위 역전 방지.

#### 시나리오 2: 산업용 로봇 제어

**문제 상황**: 로봇 팔의 모터 제어가 1ms 주기로 정밀하게 수행되어야 함.

**기술사적 결단**:
1. **RTOS 선택**: VxWorks 또는 EtherCAT 마스터 전용 RTOS.
2. **고속 통신**: EtherCAT (주기 1ms, 지터 < 100μs).
3. **폐루프 제어**: PID 제어 루프가 매 1ms마다 실행.

#### 주의사항 및 안티패턴

1. **WCET 과소 추정**: 최악의 경우 실행 시간을 낙관적으로 추정하면 마감 시간 초과 발생. 항상 여유 있게 설계.

2. **비결정론적 코드**: 동적 메모리 할당, 가비지 컬렉션, 페이지 폴트 등을 실시간 코드에서 금지.

3. **우선순위 역전 무시**: 락 사용 시 PIP/PCP를 적용하지 않으면 고우선순위 작업이 무한 대기.

---

### Ⅴ. 기대효과 및 결론

#### 정량적/정성적 기대효과

| 지표 | 범용 OS | Soft RT | Hard RT |
|:---|:---|:---|:---|
| **최대 인터럽트 지연** | 수십 ms | 수 ms | < 100μs |
| **스케줄링 지연** | 불확정 | < 1ms | < 100μs |
| **마감 시간 준수율** | ~99% | ~99.9% | 100% |
| **안전 인증** | 불가능 | 제한적 | ISO 26262, IEC 61508 |

#### 미래 전망

실시간 시스템은 **"자율 시스템"**의 시대와 함께 더욱 중요해지고 있다. 주요 발전 방향:

1. **AI + 실시간**: 실시간 AI 추론을 위한 하드웨어 가속기(NPU, TPU)와 RTOS의 통합.
2. **이기종 실시간**: CPU + FPGA + GPU의 혼합 실시간 처리.
3. **클라우드 RT**: 5G/6G 네트워크를 통한 분산 실시간 제어(Cloud Robotics).
4. **안전 인증 자동화**: 실시간 시스템의 안전성 검증을 위한 형식적 방법(Formal Methods) 도입.

#### 참고 표준/가이드

- **POSIX.1-2001 (Real-time Extension)**: 실시간 시스템 API 표준
- **OSEK/VDX**: 자동차용 RTOS 표준
- **ISO 26262**: 자동차 기능 안전 표준
- **IEC 61508**: 산업용 기능 안전 표준
- **AUTOSAR**: 자동차 소프트웨어 아키텍처 표준

---

### 관련 개념 맵 (Knowledge Graph)

- [실시간 스케줄링](@/studynotes/2_operating_system/3_cpu_scheduling/201_realtime_scheduling.md): RM, EDF 알고리즘
- [우선순위 역전](@/studynotes/2_operating_system/4_concurrency_sync/242_priority_inversion.md): PIP, PCP 해결책
- [RTOS](@/studynotes/2_operating_system/10_security_virtualization/623_rtos.md): 실시간 운영체제
- [임베디드 시스템](@/studynotes/2_operating_system/1_os_overview/10_embedded_system.md): 실시간의 주요 적용 분야
- [인터럽트 지연](@/studynotes/2_operating_system/3_cpu_scheduling/204_latency.md): 실시간성의 핵심 지표

---

### 어린이를 위한 3줄 비유 설명

1. 실시간 시스템은 **'수술실의 의사'**와 같아요. 심장 수술을 할 때 의사는 정확한 시간에 정확한 동작을 해야 해요. 1초만 늦어도 환자에게 큰 문제가 생길 수 있죠.

2. **'빠른 것'**보다 **'정확한 시간에'** 하는 것이 더 중요해요. 비디오 게임에서 화면이 조금 늦게 나오는 건 괜찮지만, 자동차 브레이크가 1초 늦게 작동하면 사고가 나요!

3. 그래서 실시간 시스템을 만드는 사람들은 **'얼마나 오래 걸릴지'**를 아주 정확하게 계산해요. 혹시라도 늦어지면 안 되니까요. 이런 시스템은 비행기, 기차, 자동차 같은 곳에서 우리를 지켜준답니다!
