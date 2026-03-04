+++
title = "페이지 교체 알고리즘 심층 분석 (LRU, LFU, Clock, OPT)"
date = 2024-05-20
description = "가상 메모리 시스템의 핵심인 페이지 교체 알고리즘의 동작 원리, 성능 분석(Page Fault), 그리고 Belady의 역설(Anomalies) 극복을 위한 현대 OS의 최적화 전략"
weight = 10
[taxonomies]
categories = ["studynotes-operating_system"]
tags = ["Page-Replacement", "LRU", "LFU", "Virtual-Memory", "OS-Architecture", "Thrashing"]
+++

# 페이지 교체 알고리즘 심층 분석 (LRU, LFU, Clock, OPT)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 물리 메모리가 부족할 때 가상 메모리의 어떤 페이지를 디스크로 내보낼(Victim Selection) 것인지 결정하여, 한정된 자원으로 시스템 전체의 참조 지역성(Locality)을 극대화하는 의사결정 메커니즘입니다.
> 2. **가치**: 알고리즘 효율성에 따라 페이지 부동(Page Fault) 발생 빈도가 결정되며, 이는 곧 시스템의 응답 시간과 처리량(Throughput), 그리고 스래싱(Thrashing) 방지의 핵심 변수가 됩니다.
> 3. **융합**: 현대 운영체제는 LRU의 높은 오버헤드와 FIFO의 낮은 효율성을 절충한 **Clock 알고리즘**을 주로 채택하며, 여기에 **Working Set 모델**이나 **PFF(Page Fault Frequency)** 제어 기술을 융합하여 동적으로 가용 메모리를 관리합니다.

---

## Ⅰ. 개요 (Context & Background)

가상 메모리(Virtual Memory) 시스템은 실제 물리 메모리(RAM)보다 더 큰 프로그램을 실행할 수 있게 해주는 혁신적 기술입니다. 하지만 물리 메모리는 유한하기 때문에 새로운 페이지를 올릴 빈 공간이 없을 때 기존 페이지 중 하나를 희생(Victim)시켜 디스크의 스왑 영역으로 내려보내야 합니다. 이때 **"앞으로 가장 오랫동안 사용되지 않을 페이지"**를 정확히 예측하여 교체하는 것이 페이지 교체 알고리즘의 궁극적 목표입니다.

**💡 비유**: 책상이 좁아 공부할 책 3권만 올려둘 수 있는데, 새로운 책을 보려면 기존 책 중 하나를 책꽂이(디스크)로 돌려보내야 하는 상황과 같습니다. 이때 "방금 다 본 책"을 넣을지, "가장 오래전에 본 책"을 넣을지, 아니면 "가장 적게 본 책"을 넣을지 결정하는 규칙이 페이지 교체 알고리즘입니다.

**등장 배경 및 발전 과정**:
1. **FIFO의 한계와 Belady의 역설**: 가장 먼저 들어온 페이지를 먼저 내보내는 단순한 방식은 메모리를 늘려줬는데 오히려 페이지 부동이 늘어나는 기현상(Belady's Anomaly)을 발생시켰습니다.
2. **이론적 최적해(OPT)**: 미래의 참조 기록을 모두 안다는 가정하에 설계된 최적 알고리즘(Optimal)이 제시되었으나, 실제 구현이 불가능하여 이를 근사(Approximate)하는 연구가 가속화되었습니다.
3. **현대적 절충안 (LRU to Clock)**: 과거 기록을 기반으로 미래를 예측하는 LRU가 우수한 성능을 보였으나, 매 참조마다 시간(Timestamp)을 기록해야 하는 하드웨어 오버헤드가 컸습니다. 이를 해결하기 위해 참조 비트(Reference Bit)만 사용하는 Clock 알고리즘이 현대 OS의 표준으로 자리 잡았습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 주요 페이지 교체 알고리즘 구성 및 매커니즘

| 알고리즘 | 명칭 | 상세 역할 및 교체 기준 | 기술적 장단점 | 비유 |
|---|---|---|---|---|
| **OPT** | 최적 교체 | 앞으로 가장 오랫동안 사용되지 않을 페이지 교체 | 이론적 하한선, 구현 불가 | 예언자 |
| **FIFO** | 선입 선출 | 메모리에 올라온 지 가장 오래된 페이지를 교체 | 구현 단순, Belady의 역설 발생 | 선착순 퇴장 |
| **LRU** | Least Recently Used | 최근에 가장 오랫동안 참조되지 않은 페이지 교체 | 참조 국부성 활용 탁월, 오버헤드 높음 | 안 본 지 오래된 책 |
| **LFU** | Least Frequently Used | 참조 횟수가 가장 적은 페이지를 교체 | 장기적 참조 패턴 반영, 최근성 무시 | 인기도 낮은 책 |
| **Clock** | Second Chance | 원형 큐와 참조 비트를 사용하여 LRU를 근사 | 하드웨어 지원 용이, 효율적 실구현 | 순찰도는 경비원 |

### 정교한 구조 다이어그램: Clock 알고리즘 (Second Chance) 매커니즘

```ascii
[ Clock Algorithm (LRU Approximation) Operation ]

   Initial State: [ P1:1 ] -> [ P2:1 ] -> [ P3:0 ] -> [ P4:1 ]
                     ^
                Clock Hand (Pointer)

1. Page Fault occurs (Need to load P5)
2. Clock Hand checks P1: Bit is 1.
   -> Give Second Chance: Set Bit to 0. Move Hand to P2.
   [ P1:0 ]    [ P2:1 ] -> [ P3:0 ] -> [ P4:1 ]
                  ^

3. Hand checks P2: Bit is 1.
   -> Give Second Chance: Set Bit to 0. Move Hand to P3.
   [ P1:0 ] -> [ P2:0 ]    [ P3:0 ] -> [ P4:1 ]
                              ^

4. Hand checks P3: Bit is 0.
   -> VICTIM FOUND! Replace P3 with P5. Set Bit to 1. Move Hand to P4.
   [ P1:0 ] -> [ P2:0 ] -> [ P5:1 ]    [ P4:1 ]
                                          ^

[ Performance Comparison Curve ]
Page Faults
   ^
   |      + FIFO (High Faults, Anomaly)
   |     /
   |    + LRU / Clock (Moderate, Stable)
   |   /
   |  + OPT (Minimum Possible)
   +------------------------------> Memory Frames
```

### 심층 동작 원리: LRU의 하드웨어/소프트웨어 구현 방식

1. **Counter 방식**: 각 페이지 항목에 '사용 시간' 필드를 두고, 참조될 때마다 CPU 클럭 값을 복사합니다. 교체 시 가장 작은 값을 찾기 위해 전수 조사가 필요하여 매우 느립니다.
2. **Stack 방식**: 페이지 번호를 스택에 유지합니다. 참조되면 스택 중간에서 뽑아 맨 위로 올립니다. 교체 시 스택 맨 아래를 제거합니다. 포인터 연산 오버헤드가 큽니다.
3. **Reference Bit (Clock)**: 페이지 테이블의 1비트만 활용합니다. CPU가 참조 시 자동 1 세팅, OS가 교체 시 0으로 깎으면서 기회를 한 번 더 주는 방식입니다.

### 핵심 코드: LRU 캐시 구현 (Python OrderedDict 활용)

실무에서 캐시 시스템(Redis, Memcached) 등을 설계할 때 사용하는 LRU 로직의 정수입니다.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # 최근에 사용되었으므로 맨 뒤(Most Recent)로 이동
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        # 용량 초과 시 가장 오래된(맨 앞) 데이터 삭제
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# 사용 예시
lru = LRUCache(3)
lru.put(1, "Data1")
lru.put(2, "Data2")
lru.put(3, "Data3")
lru.get(1)          # 1번이 최근 사용됨
lru.put(4, "Data4") # 용량 초과로 가장 오래된 2번이 삭제됨
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: LRU vs LFU vs MFU

| 비교 관점 | LRU (Least Recently Used) | LFU (Least Frequently Used) | MFU (Most Frequently Used) |
|---|---|---|---|
| **판단 근거** | 참조된 시점 (Recency) | 참조된 횟수 (Frequency) | 참조된 횟수 (Frequency) |
| **핵심 가정** | 방금 쓴 건 또 쓴다. | 자주 쓴 건 또 쓴다. | 방금 많이 쓴 건 이제 안 쓴다. |
| **취약점** | 최근에 한 번만 쓰인 데이터가 남음 | 과거엔 인기 많았으나 지금은 안 쓰는 데이터 정체 | 구현이 복잡하고 성능이 대체로 낮음 |
| **구현 방식** | Linked List + Hash Map | Min-Heap + Hash Map | Max-Heap + Hash Map |
| **실무 적용** | 대부분의 OS, DB 버퍼 풀 | 캐시 만료 정책 (특정 상황) | 거의 사용되지 않음 |

### 과목 융합 관점 분석 (컴퓨터 구조 및 데이터베이스 연계)
- **컴퓨터 구조와의 융합**: CPU 내의 **TLB(Translation Lookaside Buffer)** 교체 시에도 페이지 교체 알고리즘이 사용됩니다. 하드웨어 수준에서 이루어져야 하므로 매우 단순한 LRU(Pseudo-LRU)나 Random 방식이 채택됩니다.
- **데이터베이스(DB)와의 융합**: 데이터베이스의 **Buffer Pool 관리**에서도 LRU가 쓰입니다. 하지만 DB는 풀 스캔(Full Scan) 시 중요 데이터가 밀려나는 것을 방지하기 위해, 한 번 읽은 페이지는 즉시 교체 대상으로 분류하거나 별도의 공간(Mid-point Insertion)에 두는 변형된 LRU 알고리즘을 사용합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 시스템 전반의 Thrashing 발생 및 해결 전략
**문제 상황**: 서버의 CPU 사용률은 낮은데 I/O Wait가 극도로 높고, 프로세스들이 진행되지 않는 스래싱(Thrashing) 현상이 목격되었습니다. 페이지 부동이 연쇄적으로 발생하여 시스템이 마비된 상태입니다.

**기술사의 전략적 의사결정**:
1. **Working Set 모델 적용**: 각 프로세스가 일정 시간 동안 참조하는 페이지의 집합(Working Set)을 유지할 수 있을 만큼의 프레임을 할당합니다. 합계가 물리 메모리보다 크면 프로세스 일부를 중단(Swap-out)시킵니다.
2. **PFF (Page Fault Frequency) 조절**: 프로세스의 페이지 부동율을 모니터링합니다. 상한선(Upper Bound)을 넘으면 프레임을 더 주고, 하한선(Lower Bound) 아래면 뺏어서 시스템 전체의 페이지 부동율을 최적으로 유지합니다.
3. **Global vs Local Replacement 전략**: 다른 프로세스의 프레임을 뺏어올지(Global), 자기에게 할당된 프레임 내에서만 바꿀지(Local) 결정합니다. 스래싱 억제에는 Local이 유리하나 자원 효율은 Global이 좋습니다.

### 도입 시 고려사항 및 안티패턴 (Anti-patterns)
- **안티패턴 - 너무 작은 페이지 사이즈**: 페이지 크기를 너무 작게 설정하면 페이지 테이블 크기가 커지고 페이지 부동 횟수가 증가하여 오버헤드가 폭증합니다. 현대 시스템은 4KB를 기본으로 하되, 대규모 메모리 사용 시 Huge Pages(2MB/1GB)를 활용합니다.
- **체크리스트**: 
  - 타겟 워크로드의 순차 참조 vs 무작위 참조 패턴 파악.
  - 하드웨어의 참조 비트/수정 비트(Dirty Bit) 지원 여부.
  - 스왑 공간(Swap Space)의 성능(SSD vs HDD) 및 크기 적정성.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과
- **메모리 효율성 극대화**: 참조 지역성을 잘 활용하는 알고리즘을 통해 물리 메모리의 수십 배에 달하는 논리 주소 공간을 안정적으로 운영할 수 있습니다.
- **I/O 병목 완화**: 효율적인 페이지 교체는 느린 디스크로의 스왑 접근을 줄여 시스템 전체 Latency를 수백 배 개선합니다.

### 미래 전망 및 진화 방향
- **비휘발성 메모리 (NVM/PRAM) 대응**: DRAM과 SSD 사이의 속도를 가진 NVM이 대중화되면서, 읽기/쓰기 수명과 속도 차이를 고려한 새로운 하이브리드 페이지 관리 기법이 연구되고 있습니다.
- **AI 기반 페이지 예측**: 과거의 복잡한 참조 패턴을 딥러닝(RNN/LSTM)으로 학습하여, 단순히 '최근성'이 아닌 '패턴'을 기반으로 다음 페이지를 미리 가져오거나(Prefetching) 교체하는 지능형 알고리즘이 실험 중입니다.

### ※ 참고 표준/가이드
- **POSIX.1 (mmap, madvise)**: 메모리 맵 및 OS에 페이지 교체 힌트를 주는 API 표준.
- **Intel 64 and IA-32 Architectures Software Developer's Manual**: 하드웨어 레벨의 페이지 테이블 및 참조 비트 관리 규격.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [가상 메모리(Virtual Memory)](@/studynotes/02_operating_system/02_memory_management/_index.md) : 페이지 교체가 일어나는 전체 메커니즘의 기반.
- [참조 지역성(Locality)](@/studynotes/02_operating_system/02_memory_management/_index.md) : 페이지 교체 알고리즘이 성능을 낼 수 있는 근거가 되는 원리.
- [쓰래싱(Thrashing)](@/studynotes/02_operating_system/02_memory_management/_index.md) : 부적절한 페이지 교체나 과도한 멀티프로그래밍으로 인한 성능 파멸 상태.
- [TLB](@/studynotes/01_computer_architecture/02_memory_hierarchy/_index.md) : 주소 변환 고속화를 위한 캐시로, 별도의 교체 정책을 가짐.
- [Demand Paging](@/studynotes/02_operating_system/02_memory_management/_index.md) : 필요한 시점에만 페이지를 메모리에 올리는 가상 메모리 운영 방식.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 컴퓨터 메모리는 **'작은 책상'** 같아서, 공부할 책(페이지)을 다 올려둘 수 없어요.
2. 그래서 새로운 책을 보려면 **지금 책상에 있는 책 중 하나를 책꽂이로 돌려보내야** 하는데, 이때 어떤 책을 뺄지 정하는 규칙이 '페이지 교체 알고리즘'이에요.
3. **'아까 본 책은 나중에 또 볼 확률이 높다'**는 생각으로 가장 오랫동안 안 본 책을 빼는 것이 가장 똑똑한 방법이랍니다!
