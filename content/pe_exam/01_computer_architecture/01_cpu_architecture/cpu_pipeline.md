+++
title = "CPU 파이프라인 (CPU Pipeline)"
date = 2024-05-18
description = "CPU 파이프라이닝의 원리, 해저드(Hazard)의 종류 및 해결 방안, 그리고 최신 프로세서의 심화 아키텍처(Superscalar, Out-of-Order Execution)에 대한 심층 분석"
weight = 10
+++

# CPU 파이프라인 아키텍처 심층 분석 (CPU Pipeline Architecture Deep Dive)

## 1. 개요 및 파이프라이닝의 본질 (Introduction)
CPU 파이프라이닝(Pipelining)은 하나의 명령어 실행을 여러 개의 독립적인 단계(Stage)로 분할하여, 동시에 여러 명령어를 중첩하여 실행함으로써 프로세서의 명령어 처리량(Throughput)을 극대화하는 핵심 아키텍처 설계 기법입니다. 이는 공장의 조립 라인(Assembly Line)과 동일한 원리를 컴퓨터 구조에 적용한 것으로, 현대 마이크로프로세서 성능 향상의 근간을 이룹니다.

비파이프라인(Non-pipelined) 프로세서가 한 번에 하나의 명령어만 처리하여 모든 단계가 완료될 때까지 다음 명령어가 대기해야 하는 반면, 파이프라인 프로세서는 각 클럭 사이클마다 새로운 명령어를 파이프라인에 진입시켜 이론적으로 클럭 당 하나의 명령어(CPI = 1)를 완료할 수 있도록 합니다.

## 2. 5단계 파이프라인 기본 구조 (5-Stage RISC Pipeline)
전형적인 32비트 RISC(MIPS/RISC-V) 아키텍처는 명령어 처리를 다음과 같이 5개의 고유한 단계로 나눕니다.

```ascii
[Instruction Stream]
      |
      v
+------------+   +------------+   +------------+   +------------+   +------------+
|     IF     |-->|     ID     |-->|     EX     |-->|    MEM     |-->|     WB     |
| Instr Fetch|   | Instr Decode|  | Execute /  |   | Memory Acc |   | Write Back |
|            |   | & Reg Read |   | Addr Calc  |   |            |   |            |
+------------+   +------------+   +------------+   +------------+   +------------+
      |                |                |                |                |
  [I-Cache]      [Register File]      [ALU]          [D-Cache]     [Register File]
```

1. **IF (Instruction Fetch)**: 프로그램 카운터(PC)가 가리키는 메모리 주소(주로 L1 I-Cache)에서 실행할 명령어를 인출합니다. PC는 다음 명령어 주소(PC + 4)로 자동 증가합니다.
2. **ID (Instruction Decode & Register Fetch)**: 인출된 명령어의 Opcode를 해독하고, 제어 신호를 생성하며, 레지스터 파일로부터 필요한 Source 피연산자(Operand) 값을 읽어옵니다.
3. **EX (Execute / Address Calculation)**: 산술 논리 연산 장치(ALU)를 사용하여 연산을 수행하거나, 메모리 접근을 위한 유효 주소(Effective Address)를 계산합니다. 분기 명령어의 경우 분기 조건을 평가합니다.
4. **MEM (Memory Access)**: Load 또는 Store 명령어의 경우 데이터 캐시(D-Cache)에 접근하여 데이터를 읽거나 씁니다. 연산 명령어는 이 단계를 그냥 통과합니다.
5. **WB (Write Back)**: ALU의 연산 결과나 메모리에서 읽어온 데이터를 목적지 레지스터(Destination Register)에 기록하여 상태를 갱신합니다.

## 3. 파이프라인 해저드 (Pipeline Hazards) 및 해결 방안
이론적인 파이프라인은 CPI=1을 달성해야 하지만, 실제 환경에서는 명령어 간의 의존성이나 하드웨어 자원의 충돌로 인해 파이프라인이 멈추는(Stall) 현상이 발생합니다. 이를 해저드(Hazard)라고 합니다.

### 3.1 구조적 해저드 (Structural Hazard)
**정의**: 하드웨어 자원이 부족하여 여러 명령어가 동시에 동일한 자원을 요구할 때 발생합니다. 예를 들어, 메모리가 명령어와 데이터를 분리하지 않은 단일 메모리(Von Neumann 구조)일 때, 한 명령어는 IF를 위해 메모리에 접근하고 다른 명령어는 MEM 단계에서 데이터 접근을 시도하면 충돌이 발생합니다.
**해결 방안**: 
- **하버드 아키텍처 (Harvard Architecture)**: 명령어 캐시(I-Cache)와 데이터 캐시(D-Cache)를 분리하여 동시 접근을 허용합니다.
- **자원 복제**: ALU를 여러 개 두거나, 레지스터 파일의 Read/Write 포트를 늘려 동시 처리를 지원합니다.

### 3.2 데이터 해저드 (Data Hazard)
**정의**: 이전 명령어의 연산 결과가 아직 레지스터에 기록되지(WB) 않았는데, 뒤따르는 명령어가 해당 레지스터의 값을 읽으려(ID) 할 때 발생합니다. (Read-After-Write, RAW 의존성)

```assembly
; 데이터 해저드 예시
ADD R1, R2, R3   ; R1 = R2 + R3 (EX 단계에서 결과 계산, WB에서 기록)
SUB R4, R1, R5   ; R4 = R1 - R5 (ID 단계에서 R1을 읽어야 함 -> Hazard!)
```

**해결 방안**:
- **전방 전달 (Data Forwarding / Bypassing)**: ALU에서 계산된 결과(EX 단계 완료) 또는 메모리에서 읽은 데이터(MEM 단계 완료)를 WB 단계까지 기다리지 않고, 즉시 다음 명령어의 ALU 입력으로 우회시키는 하드웨어 경로를 추가합니다.
- **파이프라인 스톨 (Pipeline Stall / Bubble)**: Load-Use Data Hazard (Load 명령어 바로 다음에 그 데이터를 사용하는 명령어가 올 때)와 같이 Forwarding만으로 해결할 수 없는 경우, NOP(No Operation)을 삽입하여 파이프라인을 1~2 사이클 정지시킵니다.
- **명령어 스케줄링 (Instruction Scheduling)**: 컴파일러가 의존성이 없는 다른 유용한 명령어를 스톨이 발생하는 위치에 재배치하여 빈 공간을 채웁니다.

### 3.3 제어 해저드 (Control Hazard)
**정의**: 분기(Branch)나 점프(Jump) 명령어에 의해 프로그램의 실행 흐름이 변경될 때 발생합니다. 분기 여부와 목적지 주소가 결정될 때까지 다음 명령어를 인출할 수 없어 파이프라인이 비워지게 됩니다. (Branch Penalty)

**해결 방안**:
- **분기 예측 (Branch Prediction)**: 
  - **정적 예측**: 항시 분기 안 함(Always Not-Taken) 또는 루프 백워드는 분기함(Backward Taken) 등으로 단순하게 예측합니다.
  - **동적 예측 (Dynamic Prediction)**: Branch History Table(BHT)이나 Branch Target Buffer(BTB)를 하드웨어에 두어, 과거의 분기 기록을 바탕으로 실행 중에 예측합니다. 2-bit Predictor 등이 널리 사용됩니다.
- **지연 분기 (Delayed Branch)**: 분기 명령어 다음에 항상 실행되는 명령어(Branch Delay Slot)를 두어, 분기 결정에 상관없이 유용한 작업을 수행하게 합니다 (최신 프로세서에서는 예측 기술의 발달로 잘 안 쓰임).

## 4. 고급 파이프라인 기술 (Advanced Microarchitecture)

파이프라인의 깊이를 늘리는 슈퍼파이프라이닝(Superpipelining) 한계를 극복하기 위해, 현대 CPU는 클럭 당 여러 명령어를 처리하는 구조를 채택했습니다.

### 4.1 슈퍼스칼라 (Superscalar)
동일한 클럭 사이클에 여러 개의 명령어를 인출하고 해독하여 여러 개의 실행 유닛(ALU, FPU 등)으로 분배하는 기술입니다. 동적(하드웨어적)으로 명령어 간의 독립성을 검사하여 병렬 실행합니다. IPC(Instructions Per Cycle)가 1을 초과하게 됩니다.

```ascii
[Fetch Unit] ---> [Decode/Issue Unit] ---+---> [Integer ALU 1] ---> [Commit]
   (Fetch N)          (Check Dependencies)|---> [Integer ALU 2] ---> [Commit]
                                          +---> [FP Multiplier] ---> [Commit]
                                          +---> [Load/Store U ] ---> [Commit]
```

### 4.2 비순차적 실행 (Out-of-Order Execution, OoOE)
명령어들이 프로그램에 작성된 순서(In-Order)대로 실행되지 않고, 데이터가 준비된 명령어부터 먼저 실행(Out-of-Order)되도록 하는 핵심 기술입니다.
1. **Fetch & Decode (In-Order)**: 명령어를 순서대로 인출/해독.
2. **Rename (Register Renaming)**: False Dependency (WAW, WAR)를 제거하기 위해 아키텍처 레지스터를 물리적 레지스터로 매핑.
3. **Dispatch & Issue**: 명령어를 예약소(Reservation Station)에 넣고, 피연산자가 준비되면 순서에 상관없이 실행 유닛으로 Issue.
4. **Execute (Out-of-Order)**: 연산 수행.
5. **Commit/Retire (In-Order)**: Reorder Buffer (ROB)를 사용하여 실행 완료된 결과를 프로그램의 원래 순서대로 레지스터나 메모리에 최종 반영(Commit). 이를 통해 예외(Exception) 처리의 정확성을 보장합니다.

## 5. C/C++ 레벨에서의 파이프라인 최적화 (Software Perspective)
개발자는 파이프라인 친화적인 코드를 작성하여 성능을 극대화할 수 있습니다. 분기 예측 실패(Branch Misprediction)를 줄이는 것이 관건입니다.

```cpp
#include <algorithm>
#include <vector>
#include <iostream>
#include <chrono>

int main() {
    std::vector<int> data(32768);
    for (int i = 0; i < 32768; ++i) data[i] = std::rand() % 256;

    // 정렬 여부에 따른 분기 예측 성능 차이
    // std::sort(data.begin(), data.end()); // 주석 해제 시 성능 급격히 향상

    long long sum = 0;
    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < 100000; ++i) {
        for (int c = 0; c < 32768; ++c) {
            // 조건 분기: 데이터가 무작위일 경우 분기 예측기가 실패율이 높아 Pipeline Flush 발생
            if (data[c] >= 128) {
                sum += data[c];
            }
            
            // 분기 예측을 피하는 방법 (Branchless Programming)
            // int t = (data[c] - 128) >> 31; // 음수면 -1(모든 비트 1), 양수면 0
            // sum += ~t & data[c];
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "Sum: " << sum << "\n";
    std::cout << "Time: " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " ms\n";
    
    return 0;
}
```
위 예제에서 데이터가 정렬되어 있다면 분기 예측기(Branch Predictor) 패턴을 쉽게 학습하여 파이프라인 스톨 없이 고속으로 실행됩니다. 반면 정렬되지 않은 상태에서는 잦은 분기 예측 실패로 인해 파이프라인 플러시(Flush) 비용이 막대하게 발생합니다.

## 6. 결론
CPU 파이프라인은 프로세서 아키텍처에서 성능을 결정짓는 가장 중요한 요소 중 하나입니다. 파이프라인의 깊이를 늘려 클럭 속도를 높이는 방식(NetBurst 아키텍처 등)에서 시작하여, 오늘날에는 Superscalar, Out-of-Order Execution, 강력한 Branch Prediction 기법을 복합적으로 적용함으로써 단일 스레드 성능의 한계를 돌파하고 있습니다. 소프트웨어 엔지니어 역시 하드웨어의 파이프라인 특성을 이해하고 Branchless 코딩 기법 등을 활용함으로써 극단적인 성능 최적화를 이끌어 낼 수 있습니다.
