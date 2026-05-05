+++
weight = 146
title = "146. 실시간 프로세스 (Real-time Process)"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++
## 0. 핵심 인사이트

> **��:** �� ���� "��� � ��" ���� �����, ��� ���� "��� 30� ��" ��� ���� �����.

> 📝 모범 답안

# ��� ���� (Real-time Process)

## . ��� ��� ��

### 1. �� � ��

��� ���(Real-time System)� �� ��� ��� ��� ��� ��(Timing Constraint)� ���� �� �����. ��� "��" ���� ��� "�� ��� �� ��"� ���� �� ����.

```
 Real-time vs General Purpose 
                                                     
  �� ��� (Best Effort):                         
  Task A: 50ms  (�� ��, �� ��)         
  Task B: 200ms  (��� ��)                   
  Task C: 1000ms  (�� �� ��)                
                                                     
  ��� ��� (Guaranteed):                        
  Task A:  10ms  (�� 10ms ��)               
  Task B:  50ms  (��� ��� ��)            
  Task C:  100ms  (���� ��)                 
                                                     

```

### 2. �� ��� vs ��� ���

| �� | Hard Real-time | Soft Real-time |
|------|----------------|----------------|
| **����** | ��� �� �� | ��, �� �� �� |
| **�� ��** | ���/�� �� | ��� �� �� |
| **��** | ��� ��, ��� ABS | ��� ����, ��� �� |
| **OS** | VxWorks, QNX, RT-Linux | �� Linux, Windows |

```
 Hard vs Soft Real-time 
                                      
  Hard:                               
  Deadline |X|        
                  �� (���)        
                                      
  Soft:                               
  Deadline |||X|||      
            ��� �� (�� ��� OK)
                                      
  General (Best Effort):               
  Deadline ||X||     
            �� ��� ��            
                                      

```

## . POSIX ��� ����

### 1. SCHED_FIFO (First In, First Out)

��� ���� �� � �� ��� ����. �� ������� �� ��� ���� ����, ����� ��(yield)��� ���� ��� ��� ����.

```
 SCHED_FIFO �� 
                                           
  ����: RT-99 > RT-50 > RT-10         
                                           
  �� >      
                                           
  RT-99:  (�� ��)       
                                          
           yield/block ��                
                                          
  RT-50:         (��)            
  RT-10:               (��)          
                                           
  ��:                                      
  - ����� �� (��/�� ����)    
  - �� ����� �� ��               
  -(Starvation) ���                  
                                           

```

### 2. SCHED_RR (Round Robin)

SCHED_FIFO� �����, �� ����� ���� �� �� ���(Time Quantum)� ���� ���� ����.

```
 SCHED_RR �� 
                                           
  ����: RT-50 (��)                   
  Time Quantum: 10ms                       
                                           
  �� >        
                                           
  Task A:              
  Task B:              
  Task C:              
         |<--10ms-->|                       
                                           
   = ��,  = ��                 
  �� ������ ��� �� ��        
                                           

```

### 3. ��� ���� �� ��

| �� | ���� �� | �� | �� ��� | �� |
|------|---------------|------|-------------|------|
| **SCHED_FIFO** | 1~99 | �� �� | �� | �� ��� |
| **SCHED_RR** | 1~99 | �� �� | �� | ��� ��� |
| **SCHED_OTHER** | 0 (nice) | CFS �� | CFS �� | �� ���� |
| **SCHED_DEADLINE** | - | EDF �� | �� �� | �� ��� |

## . ��� ���� ����

### 1. RM (Rate-Monotonic) ����

��� �� ���� �� ����� ���� **�� ����** �� ������. �� ������ ��� �� �� ���� �����.

```
 RM ���� � 
                                             
  Task-1: ��=10ms, ����=3ms  (P:�)  
  Task-2: ��=20ms, ����=4ms  (P:�)  
  Task-3: ��=50ms, ����=8ms  (P:�)  
                                             
  �� >  0  3  6  10 13 16 20 23 26 30   
  T1:    [===]   [===]    [===]    [===]    
  T2:        [====]       [====]            
  T3:            [========]                  
                                             
  CPU�� = 3/10 + 4/20 + 8/50 = 0.74     
  ��: U  n(2^(1/n) - 1)                  
       (n=3: 0.779, 0.74 < 0.779 -> ��� ��) 
                                             

```

### 2. EDF (Earliest Deadline First) ����

����� �� ��� ���� �� ���� **�� ����** ������. CPU ��� 100%�� �� ��� �� ������.

```
 EDF ���� � 
                                             
  Task-A: ��=10ms, ����=4ms            
  Task-B: ��=20ms, ����=5ms            
  Task-C: ��=50ms, ����=10ms           
                                             
  �� >  0   4   8  10  14  20  24      
  ����: B> A > C                        
  T-A:    [====]  [====]     [====]         
  T-B:         [====]      [====]          
  T-C:              [==========]            
                                             
  ���� ��� �� ���� ��          
  CPU ��� ��: U  1.0 (100%)            
  (�, ���� � �� ��� ��)          
                                             

```

### 3. RM vs EDF ��

> **��:** RM� �� ��� �� ��� �� ��� �� ����, EDF� �� ��� �� ��� ��� �� ��� �� ����.

| �� | RM | EDF |
|------|----|----|
| **����** | �� (�� ��) | �� (���� ��) |
| **CPU ��� ��** | 69%(n->inf) | 100% |
| **�� ���** | �� | �� (���� �� ��) |
| **���� ��** | ����� ���� �� | �� ��� �� |
| **�� ��** | �� �� (POSIX ��) | �� + �� �� |

## . Linux PREEMPT_RT

### 1. ��

PREEMPT_RT (Real-time Preemption) ��� �� Linux ��� ��� ����� ���� �� ����. �� 5.x �� ����� ����� ���� ��.

```
 Linux Preemption Levels 
                                             
  PREEMPT_NONE:       �� ��              
  (�� ��, �� ���)                   
                                             
  PREEMPT_VOLUNTARY:  ��� �� �� �     
  (��� �� ���)                       
                                             
  PREEMPT_FULL:      �� ��� �� ��   
  (���� ��, ���� ��� ��)      
                                             
  PREEMPT_RT:        �� �� � �� ��   
  (���, ����� ����)              
   �� �� �� ��                      
                                             

```

### 2. PREEMPT_RT �� �� ��

| �� | �� | �� |
|------|------|------|
| **���� ����** | �� ����� �� ���� �� | ���� �� ��� |
| **��� � ��** | ���� spinlock� mutex� �� | ����� �� |
| **���� ��** | � �� � ���� �� �� | |
| **���� ��** | �� �� �� �� �� �� | ����� �� |

## . �� ���

```
��� ����
 ��� ��� ��
    �� ��� (���� �� ��)
    ��� ��� (�� �� ��)
    ��: �� ��� �� �� ��
 POSIX ���� ��
    SCHED_FIFO (�� ���� FIFO)
    SCHED_RR (�� ���� Round Robin)
    SCHED_OTHER (CFS �� ����)
    SCHED_DEADLINE (EDF �� ��)
 ���� ����
    RM (Rate-Monotonic, ��, ��=����)
    EDF (Earliest Deadline First, ��)
    RM ��: U  n(2^(1/n)-1), EDF ��: U  1.0
 Linux PREEMPT_RT
    �� �� ��: NONE < VOLUNTARY < FULL < RT
    ���� ����
    ��� �� mutex� ��
    ���� �� ���
 ��� ��� ����
    �� �� �� (Worst-case Latency) ��
    ��� �� (Deterministic Execution)
    ��(Jitter) ���
 �� ��
     ���� �� ���
     ���� ���
     �� ��� (PLC)
     �� ��
```

---

## �� ��

| �� | Full Name |
|------|-----------|
| **RTOS** | Real-Time Operating System |
| **RM** | Rate-Monotonic (Scheduling) |
| **EDF** | Earliest Deadline First |
| **PREEMPT_RT** | Real-Time Preemption Patch |
| **CFS** | Completely Fair Scheduler |
| **PLC** | Programmable Logic Controller |
| **ABS** | Anti-lock Braking System |

---

## 3� ��� ��

���� ��� �� �� ��� �� ��� �� ������.
��� ���� ��� ������ ��� ��� �� ���.
�� ��� ��� �� ����, ��� ��� ��� ��� ��� ���.
