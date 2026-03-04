+++
title = "교착상태 (Deadlock)"
date = 2024-05-18
description = "운영체제 프로세스 관리의 핵심 문제인 데드락의 정의, 발생 조건, 자원 할당 그래프, 예방/회피 알고리즘(Banker's Algorithm 구현) 및 탐지/복구 기법 심층 분석"
weight = 20
+++

# 프로세스 교착상태 (Deadlock) 심층 분석 및 해결 알고리즘

## 1. 교착상태 (Deadlock)의 정의
교착상태(Deadlock)란 다중 프로그래밍 환경에서 두 개 이상의 프로세스나 스레드가 서로가 가진 자원을 무한정 기다리며, 그 결과 시스템의 일부 또는 전체가 영구적으로 멈춰버리는 현상을 의미합니다. 각 프로세스는 실행을 계속하기 위해 다른 프로세스가 점유하고 있는 자원이 해제되기를 기다리지만, 그 자원을 가진 프로세스 역시 또 다른 프로세스의 자원을 기다리고 있어 어느 프로세스도 상태를 변경할 수 없는 순환 대기 상태에 빠진 것입니다.

## 2. 교착상태 발생의 4가지 필요충분조건 (Coffman Conditions)
다음 네 가지 조건이 시스템 내에서 **동시에** 성립할 때만 교착상태가 발생할 수 있습니다. (하나라도 깨지면 데드락은 발생하지 않습니다.)

1. **상호 배제 (Mutual Exclusion)**: 한 번에 오직 하나의 프로세스만이 해당 자원을 사용할 수 있어야 합니다. (예: 프린터, Mutex Lock)
2. **점유와 대기 (Hold and Wait)**: 최소한 하나의 자원을 점유한 상태에서, 다른 프로세스가 점유하고 있는 자원을 추가로 할당받기 위해 대기하는 프로세스가 존재해야 합니다.
3. **비선점 (No Preemption)**: 다른 프로세스에 할당된 자원을 강제로 빼앗을 수 없어야 합니다. 자원을 점유하고 있는 프로세스가 태스크를 종료한 후 스스로 반납할 때까지 기다려야 합니다.
4. **순환 대기 (Circular Wait)**: 대기하고 있는 프로세스의 집합 {P0, P1, ..., Pn}에서 P0는 P1이 점유한 자원을, P1은 P2를, ..., Pn은 P0가 점유한 자원을 대기하는 폐쇄된 원(Cycle) 형태의 체인이 존재해야 합니다.

## 3. 자원 할당 그래프 (Resource Allocation Graph, RAG)
시스템의 교착상태 여부를 시각적으로 분석하기 위해 방향성 그래프인 RAG를 사용합니다.
- **정점(Vertex)**: 프로세스(P, 원), 자원 타입(R, 사각형)
- **간선(Edge)**:
  - 요청 간선(Request Edge): P_i -> R_j (프로세스가 자원을 요청)
  - 할당 간선(Assignment Edge): R_j -> P_i (자원이 프로세스에 할당됨)

```ascii
[ 자원 할당 그래프 예시 - 교착상태 발생 ]

         +-------+                 +-------+
         |  R1   |                 |  R2   |
         +-------+                 +-------+
           |   ^                     |   ^
   할당    |   | 요청        할당    |   | 요청
 (R1->P1)  v   | (P2->R1)  (R2->P2)  v   | (P1->R2)
         ( P1 )----------------->( P2 )
                   요청 (P1->R2)
```
*그래프 내에 사이클(Cycle)이 존재하며, 각 자원 타입의 인스턴스가 1개일 경우 사이클은 곧 교착상태를 의미합니다.*

## 4. 교착상태 처리 전략 (Deadlock Handling Strategies)

### 4.1 교착상태 예방 (Deadlock Prevention)
교착상태의 4가지 조건 중 최소 하나를 구조적으로 불가능하게 만들어 원천 차단하는 보수적인 방법입니다.
- **상호 배제 부정**: 읽기 전용 파일과 같이 공유 가능한 자원을 사용합니다. (그러나 하드웨어적 한계로 완벽한 적용 불가)
- **점유와 대기 부정**: 프로세스가 실행되기 전에 필요한 모든 자원을 한 번에 요청하고 할당받게 합니다. (자원 효율성 극히 저하, 기아 상태 발생 가능)
- **비선점 부정**: 자원을 점유한 프로세스가 다른 자원을 요청할 때 즉시 할당받지 못하면, 현재 점유한 모든 자원을 자발적으로 반납하게 합니다.
- **순환 대기 부정**: 모든 자원 타입에 고유한 우선순위 번호를 부여하고, 프로세스는 항상 오름차순으로만 자원을 요청하도록 강제합니다. (가장 현실적이고 많이 쓰이는 예방 기법)

### 4.2 교착상태 회피 (Deadlock Avoidance) - Dijkstra의 Banker's Algorithm
운영체제가 프로세스의 자원 요청을 동적으로 검사하여, 시스템이 **안전 상태(Safe State)** 에 머무를 수 있는 경우에만 자원을 할당하는 기법입니다.

- **안전 상태**: 시스템이 어떤 순서로든 모든 프로세스에 자원을 할당하여 데드락 없이 완료시킬 수 있는 상태 (Safe Sequence 존재).
- **불안전 상태**: 데드락이 발생할 '가능성'이 있는 상태.

#### [ 은행원 알고리즘 (Banker's Algorithm) Python 구현 예제 ]
은행(운영체제)이 고객(프로세스)에게 대출(자원)을 해줄 때 파산하지 않고 모든 고객의 요구를 들어줄 수 있는지를 판단하는 알고리즘입니다.

```python
import numpy as np

def is_safe_state(available, max_demand, allocation):
    num_processes = len(allocation)
    num_resources = len(available)
    
    # Need 행렬 계산: 각 프로세스가 추가로 필요로 하는 자원의 양
    need = max_demand - allocation
    
    finish = [False] * num_processes
    work = available.copy()
    safe_sequence = []
    
    while len(safe_sequence) < num_processes:
        allocated_in_this_round = False
        
        for p in range(num_processes):
            if not finish[p]:
                # 프로세스 p의 Need가 현재 가용 자원(Work) 이하인지 확인
                if all(need[p][r] <= work[r] for r in range(num_resources)):
                    # 자원을 할당하고 실행 완료 후 반납한다고 가정
                    for r in range(num_resources):
                        work[r] += allocation[p][r]
                    
                    finish[p] = True
                    safe_sequence.append(p)
                    allocated_in_this_round = True
                    break # 처음부터 다시 검사하기 위해 루프 탈출
                    
        # 이번 라운드에서 어떤 프로세스에게도 자원을 줄 수 없다면 불안전 상태
        if not allocated_in_this_round:
            return False, []
            
    return True, safe_sequence

# 시스템 상태 초기화 (3개의 프로세스, 3개의 자원 타입)
# 가용 자원 (Available)
available = np.array([3, 3, 2])

# 최대 요구량 (Max Demand)
max_demand = np.array([
    [7, 5, 3],  # P0
    [3, 2, 2],  # P1
    [9, 0, 2]   # P2
])

# 현재 할당량 (Allocation)
allocation = np.array([
    [0, 1, 0],  # P0
    [2, 0, 0],  # P1
    [3, 0, 2]   # P2
])

is_safe, sequence = is_safe_state(available, max_demand, allocation)

if is_safe:
    print(f"시스템은 안전 상태입니다. Safe Sequence: {sequence}")
else:
    print("시스템은 불안전 상태입니다. (교착상태 발생 가능성 존재)")
```

### 4.3 교착상태 탐지 및 복구 (Detection and Recovery)
현대 운영체제(Windows, Linux)는 회피나 예방 알고리즘이 시스템 성능을 크게 저하시키기 때문에, 교착상태를 방치(Ostrich Algorithm)하거나 드물게 발생할 경우 이를 탐지하고 복구하는 방식을 취합니다.

1. **탐지 (Detection)**:
   - 인스턴스가 하나인 경우: 자원 할당 그래프에서 대기 그래프(Wait-for Graph)를 도출하여 사이클 탐지(DFS/BFS 활용).
   - 인스턴스가 여러 개인 경우: Shoshani/Coffman 알고리즘(은행원 알고리즘과 유사한 탐지 알고리즘) 적용.

2. **복구 (Recovery)**:
   - **프로세스 종료 (Process Termination)**: 교착상태에 관련된 모든 프로세스를 강제 종료하거나, 순환 대기가 깨질 때까지 하나씩 희생자(Victim)를 선택하여 강제 종료시킵니다.
   - **자원 선점 (Resource Preemption)**: 희생자 프로세스를 선택하여 자원을 빼앗아 다른 프로세스에 할당합니다. 이때 희생자 프로세스는 롤백(Rollback)되어야 하며, 동일한 프로세스가 계속 희생되는 기아 상태(Starvation)를 방지하기 위해 비용 함수를 고려해야 합니다.

## 5. 결론 및 실무적 관점
실제 소프트웨어 개발, 특히 멀티스레딩 프로그래밍(Java, C++, Rust 등)에서는 데드락이 매우 빈번하게 발생하는 크리티컬한 버그입니다. 개발자는 Lock을 획득하는 순서를 전역적으로 고정(Lock Ordering)하거나, `try_lock()`과 같은 타임아웃 기반의 락 획득 메커니즘을 사용해야 합니다. 최근 Rust와 같은 언어는 소유권(Ownership) 및 라이프타임 모델을 통해 컴파일 타임에 데이터 레이스를 방지하며, 데드락 방지를 위한 안전한 동시성 모델(Actor 모델, 채널 등)을 강제하여 아키텍처 수준에서 안정성을 담보하고 있습니다.
