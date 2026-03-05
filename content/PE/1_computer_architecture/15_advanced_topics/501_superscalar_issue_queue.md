+++
title = "501. 수퍼스칼라 발급 큐"
date = "2026-03-05"
[extra]
categories = "studynotes-computer-architecture"
+++

# 수퍼스칼라 발급 큐 (Superscalar Issue Queue)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 수퍼스칼라 프로세서에서 병렬로 실행 가능한 명령어들을 저장하고, 실행 유닛에 동적으로 분배하는 하드웨어 구조로, IPC(Instructions Per Cycle) 향상의 핵심 기반이다.
> 2. **가치**: 적절한 발급 큐 설계를 통해 IPC 2-8배 향상, 명령어 처리율 80-95% 달성이 가능하며, 현대 고성능 CPU의 필수 요소이다.
> 3. **융합**: 레지스터 리네이밍, 비순차 실행, 예약역과 밀접하게 연동되며, 전력 효율과 성능의 트레이드오프를 결정하는 중요 설계 요소이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
수퍼스칼라 발급 큐(Superscalar Issue Queue)는 CPU 내에서 디코딩된 명령어들이 실행 유닛(Execution Unit)으로 발급(Issue)되기 전까지 대기하는 하드웨어 버퍼이다. 수퍼스칼라 아키텍처에서는 매 클럭 사이클마다 여러 명령어를 병렬로 실행할 수 있으므로, 명령어 간의 데이터 의존성을 분석하고 실행 준비가 된 명령어들을 효율적으로 선택하여 적절한 실행 유닛에 분배하는 역할을 수행한다. 이 큐는 비순차 실행(Out-of-Order Execution)의 핵심 구성요소로, 프로그램 순서와 무관하게 데이터가 준비된 명령어부터 우선 실행할 수 있게 한다.

### 💡 비유
수퍼스칼라 발급 큐는 "고속도로 톨게이트의 스마트 차량 분류 시스템"과 같다. 여러 차선(명령어)에서 들어오는 차량들이 톨게이트 앞 대기 구역(발급 큐)에 모인다. 시스템은 각 차량의 목적지(실행 유닛), 통행권 준비 여부(데이터 의존성 해결)를 확인한 후, 준비된 차량부터 최적의 톨게이트(실행 포트)로 보낸다. 일반 차량은 일반 통행권만 있으면 되지만, 특수 차량(복잡한 연산)은 특수 통행권이 필요하므로 별도 레인에서 대기시킨다.

### 등장 배경 및 발전 과정

#### 1. 기존 기술의 치명적 한계점
- **순차 실행의 비효율성**: 단일 명령어 발급으로 인한 IPC 1.0 한계
- **파이프라인 스톨**: 데이터 의존성으로 인한 빈번한 대기
- **실행 유닛 활용률 저하**: 일부 유닛은 유휴, 다른 유닛은 대기하는 불균형

#### 2. 패러다임 변화의 역사
- **1960년대**: IBM System/360 Model 91 최초의 비순차 실행 시도
- **1980년대**: 토마술로 알고리즘 도입 (IBM RS/6000)
- **1990년대**: Intel Pentium Pro의 Reservation Station + ROB 구조
- **2000년대**: 분리형 발급 큐(Integer vs FP), 정교한 Wakeup/Select 로직
- **2010년대**: 에너지 효율형 발급 큐, 멀티코어 확장
- **2020년대**: AI 워크로드 최적화, Matrix 연산 전용 큐

#### 3. 비즈니스적 요구사항
- 데이터센터 TCO 절감: 높은 IPC로 서버당 처리량 증대
- 모바일 배터리 효율: 불필요한 발급 방지로 전력 절약
- 실시간 시스템: 결정론적 실행 시간 보장

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|--------|----------|-------------------|-----------|------|
| **Issue Queue (IQ)** | 명령어 대기 및 발급 관리 | CAM(Content Addressable Memory)으로 준비 상태 검색 | Unified/Split IQ | 톨게이트 대기 구역 |
| **Reservation Station** | 실행 유닛별 명령어 버퍼 | 오퍼랜드 준비 상태 추적, Wakeup 신호 수신 | RS Entry, Tag Matching | 유닛별 대기 라인 |
| **Wakeup Logic** | 오퍼랜드 준비 알림 | 결과 태그 브로드캐스트, 의존 명령어 활성화 | Tag Broadcast, Ready Bit | 통행권 도착 알림 |
| **Select Logic** | 발급할 명령어 선택 | 준비된 명령어 중 우선순위 기반 선택 | Age-based, Oldest-First | 다음 차량 선택 |
| **Rename Table (RAT)** | 레지스터 리네이밍 정보 | 아키텍처 레지스터 → 물리 레지스터 매핑 | Architectural → Physical | 번호표 교환 |
| **Reorder Buffer (ROB)** | 완료 순서 관리 | 비순차 실행 결과를 프로그램 순서로 커밋 | In-Order Commit | 순서 대기열 |
| **Dispatch Logic** | 디코딩된 명령어 분배 | 명령어 유형별 적절한 IQ로 라우팅 | Type-based Routing | 차선 배정 |
| **Execution Ports** | 실행 유닛 연결 포트 | 발급된 명령어를 해당 유닛으로 전달 | Port 0-6 (Intel) | 톨게이트 출구 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    수퍼스칼라 발급 큐 상세 아키텍처                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                      Front-end (Fetch/Decode)                      │    │
│   │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────────────┐   │    │
│   │  │ I-Cache │ → │ Decoder │ → │ Renamer │ → │  Dispatch Logic │   │    │
│   │  │         │   │ (4-6/cy)│   │ RAT,PRF │   │  (Route to IQs) │   │    │
│   │  └─────────┘   └─────────┘   └─────────┘   └────────┬────────┘   │    │
│   └─────────────────────────────────────────────────────┼─────────────┘    │
│                                                         │                   │
│   ══════════════════════════════════════════════════════╪═══════════════   │
│                           ▼                             │                   │
│   ┌─────────────────────────────────────────────────────▼───────────────┐  │
│   │                    Issue Queues (Unified or Split)                   │  │
│   │                                                                      │  │
│   │  ┌────────────────────────┐  ┌────────────────────────────────────┐ │  │
│   │  │   Integer Issue Queue   │  │      FP/Vector Issue Queue        │ │  │
│   │  │   (20-32 entries)       │  │      (16-24 entries)              │ │  │
│   │  │  ┌─────┬─────┬─────┐   │  │  ┌─────┬─────┬─────┬─────┐        │ │  │
│   │  │  │Entry│Entry│Entry│   │  │  │Entry│Entry│Entry│Entry│        │ │  │
│   │  │  │  0  │  1  │  2  │   │  │  │  0  │  1  │  2  │  3  │        │ │  │
│   │  │  ├─────┼─────┼─────┤   │  │  ├─────┼─────┼─────┼─────┤        │ │  │
│   │  │  │Ready│Wait │Ready│   │  │  │Wait │Ready│Wait │Ready│        │ │  │
│   │  │  │  ●  │  ○  │  ●  │   │  │  │  ○  │  ●  │  ○  │  ●  │        │ │  │
│   │  │  └─────┴─────┴─────┘   │  │  └─────┴─────┴─────┴─────┘        │ │  │
│   │  │         ↓               │  │         ↓                          │ │  │
│   │  │    [Select Logic]       │  │    [Select Logic]                  │ │  │
│   │  └──────────┬──────────────┘  └──────────┬─────────────────────────┘ │  │
│   │             │                            │                            │  │
│   │  ┌──────────▼────────────────────────────▼─────────────────────────┐ │  │
│   │  │                    Wakeup Network (Broadcast)                    │ │  │
│   │  │   Result Tag ────────────────────────────────────────────────→  │ │  │
│   │  │   (모든 IQ 엔트리에 브로드캐스트, 의존성 매칭 시 Ready 비트 설정)    │ │  │
│   │  └──────────────────────────────────────────────────────────────────┘ │  │
│   └──────────────────────────────┬───────────────────────────────────────┘  │
│                                  │                                          │
│   ═══════════════════════════════╪═══════════════ Issue/Execute ══════════  │
│                                  ▼                                          │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                    Execution Units (Ports)                            │  │
│   │                                                                       │  │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │  │
│   │  │ Port 0  │ │ Port 1  │ │ Port 2  │ │ Port 3  │ │ Port 4  │        │  │
│   │  │  ALU    │ │  ALU    │ │  Load   │ │  Store  │ │ Branch  │        │  │
│   │  │  MUL    │ │  MUL    │ │  AGU    │ │  AGU    │ │  Unit   │        │  │
│   │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘        │  │
│   │       │           │           │           │           │              │  │
│   │       └───────────┴───────────┴───────────┴───────────┘              │  │
│   │                               │                                      │  │
│   │  ┌────────────────────────────▼────────────────────────────────────┐ │  │
│   │  │            Reorder Buffer (ROB) - In-Order Commit               │ │  │
│   │  │  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐       │ │  │
│   │  │  │  0  │  1  │  2  │  3  │  4  │  5  │  6  │  7  │ ... │       │ │  │
│   │  │  │Done │Done │Wait │Done │Done │Wait │Done │Wait │     │       │ │  │
│   │  │  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘       │ │  │
│   │  │         │                                   │                   │ │  │
│   │  │    [Commit from Head]                [Wait for completion]      │ │  │
│   │  └─────────────────────────────────────────────────────────────────┘ │  │
│   └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① 명령어 발급 사이클 (4단계)

```
1. DISPATCH (분배)
   - 디코딩된 명령어가 적절한 Issue Queue로 분배
   - 리네이밍된 오퍼랜드 태그와 함께 저장
   - Ready 비트 = 모든 오퍼랜드가 준비된 경우 True

2. WAKEUP (깨우기)
   - 실행 유닛이 결과를 생성하면 태그 브로드캐스트
   - 해당 태그를 대기 중인 모든 IQ 엔트리가 Ready 비트 설정
   - Critical Path: Select가 Wakeup 다음 사이클에 수행됨

3. SELECT (선택)
   - Ready=1인 엔트리 중 발급할 명령어 선택
   - 선택 기법: Oldest-First, Age-Based, Round-Robin
   - 발급 폭(Issue Width)만큼 선택 (예: 4개/사이클)

4. ISSUE (발급)
   - 선택된 명령어를 실행 포트로 전송
   - 오퍼랜드 값은 Physical Register File에서 읽기
   - IQ에서 해당 엔트리 제거 (공간 확보)
```

#### ② Wakeup-Select Critical Path

```
문제: Wakeup과 Select가 같은 사이클에 수행되어야 함
해결: Speculative Wakeup (다음 사이클의 결과를 예측)

타이밍 다이어그램:
Cycle N:   실행 유닛에서 결과 생성
           ↓
Cycle N:   Wakeup 브로드캐스트 (같은 사이클)
           ↓
Cycle N:   Select 로직이 Ready 엔트리 선택 (같은 사이클)
           ↓
Cycle N+1: Issue (다음 사이클)

지연 시간 분석:
- Wakeup: ~10-15 FO4 (Fan-out-of-4)
- Select: ~8-12 FO4
- 총 Critical Path: ~20-25 FO4 (클럭 주기 제약)
```

#### ③ Split Issue Queue vs Unified Issue Queue

```
Split Issue Queue (분리형):
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Integer IQ      │  │ FP IQ           │  │ Memory IQ       │
│ (ALU/MUL용)     │  │ (FPU/Vector용)  │  │ (Load/Store용)  │
│ 20-32 entries   │  │ 16-24 entries   │  │ 16-32 entries   │
└─────────────────┘  └─────────────────┘  └─────────────────┘

장점:
- 각 유형별 최적화 가능
- 낮은 Wakeup/Select 지연
- 전력 효율 (사용하지 않는 IQ 끄기)

단점:
- IQ 간 밸런싱 문제 (한쪽 포화, 다른쪽 유휴)
- 더 많은 면적 필요

Unified Issue Queue (통합형):
┌─────────────────────────────────────────────────┐
│           Unified Issue Queue (40-60 entries)   │
│  [Int] [FP] [Mem] [Int] [FP] [Mem] ...          │
└─────────────────────────────────────────────────┘

장점:
- 유연한 리소스 활용
- 더 나은 IPC (타입 혼합 허용)

단점:
- 더 복잡한 Select 로직
- 높은 전력 소모
```

### 핵심 알고리즘 & 실무 코드 예시

#### Oldest-First Selection Algorithm
```python
class IssueQueue:
    def __init__(self, size=32):
        self.entries = [None] * size
        self.age = [0] * size  # 나이 (작을수록 오래됨)
        self.ready = [False] * size

    def select_oldest_ready(self, num_to_issue=4):
        """
        가장 오래된 준비된 명령어들을 선택
        """
        selected = []
        for i in range(num_to_issue):
            # Ready이고 아직 선택되지 않은 것 중 최소 나이
            min_age = float('inf')
            min_idx = -1
            for j in range(len(self.entries)):
                if self.ready[j] and j not in selected:
                    if self.age[j] < min_age:
                        min_age = self.age[j]
                        min_idx = j
            if min_idx >= 0:
                selected.append(min_idx)
        return selected

    def wakeup(self, result_tag):
        """
        결과 태그를 브로드캐스트하여 의존 명령어 활성화
        """
        for i, entry in enumerate(self.entries):
            if entry and result_tag in entry.waiting_tags:
                entry.waiting_tags.remove(result_tag)
                if len(entry.waiting_tags) == 0:
                    self.ready[i] = True

    def dispatch(self, instruction):
        """
        새 명령어를 큐에 추가
        """
        for i in range(len(self.entries)):
            if self.entries[i] is None:
                self.entries[i] = instruction
                self.ready[i] = instruction.is_ready()
                # 나이 갱신: 모든 기존 엔트리의 나이 증가
                for j in range(len(self.age)):
                    if self.entries[j] is not None:
                        self.age[j] += 1
                self.age[i] = 0  # 새 엔트리는 나이 0
                return True
        return False  # 큐 가득 참
```

#### Matrix Issue Queue (전력 효율형)
```verilog
// Verilog: Matrix Issue Queue 구조
// 각 엔트리가 독립적으로 Wakeup 상태 관리

module matrix_issue_queue #(
    parameter NUM_ENTRIES = 32,
    parameter NUM_SOURCES = 2,
    parameter TAG_WIDTH = 6
)(
    input  wire                    clk,
    input  wire                    reset,
    // Dispatch interface
    input  wire                    dispatch_valid,
    input  wire [NUM_SOURCES-1:0]  dispatch_ready_src,  // 소스 준비 여부
    input  wire [TAG_WIDTH-1:0]    dispatch_src_tag [NUM_SOURCES],
    // Wakeup interface
    input  wire                    wakeup_valid,
    input  wire [TAG_WIDTH-1:0]    wakeup_tag,
    // Select interface
    output reg  [NUM_ENTRIES-1:0]  ready_mask,
    output reg  [$clog2(NUM_ENTRIES)-1:0] selected_entry
);

    // 각 엔트리의 상태
    reg [NUM_SOURCES-1:0] src_ready [NUM_ENTRIES];
    reg [TAG_WIDTH-1:0]   src_tag   [NUM_ENTRIES][NUM_SOURCES];
    reg                   valid     [NUM_ENTRIES];
    reg [5:0]             age       [NUM_ENTRIES];

    // Ready 계산 (모든 소스가 준비되면 Ready)
    integer i, j;
    always @(*) begin
        for (i = 0; i < NUM_ENTRIES; i = i + 1) begin
            ready_mask[i] = valid[i];
            for (j = 0; j < NUM_SOURCES; j = j + 1) begin
                ready_mask[i] = ready_mask[i] & src_ready[i][j];
            end
        end
    end

    // Wakeup: 태그 매칭
    always @(posedge clk) begin
        if (wakeup_valid) begin
            for (i = 0; i < NUM_ENTRIES; i = i + 1) begin
                for (j = 0; j < NUM_SOURCES; j = j + 1) begin
                    if (src_tag[i][j] == wakeup_tag) begin
                        src_ready[i][j] <= 1'b1;
                    end
                end
            end
        end
    end

endmodule
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 발급 큐 설계 방식별 분석

| 설계 방식 | IPC | 전력 | 면적 | Wakeup 지연 | 적용 사례 |
|----------|-----|------|------|-----------|----------|
| **Unified IQ** | 높음 | 높음 | 큼 | 높음 | Intel Core, AMD Zen |
| **Split IQ (타입별)** | 중간 | 낮음 | 중간 | 낮음 | ARM Cortex, Apple M |
| **Matrix IQ** | 중간 | 매우 낮음 | 큼 | 중간 | 저전력 코어 |
| **Compact IQ** | 낮음 | 매우 낮음 | 작음 | 낮음 | 임베디드 |
| **Distributed RS** | 높음 | 중간 | 큼 | 매우 낮음 | IBM Power |

### 과목 융합 관점 분석

#### [컴퓨터구조 + 운영체제] 스케줄러와 발급 큐의 관계
```
OS 스케줄러: 스레드/프로세스 레벨 스케줄링
발급 큐: 명령어 레벨 스케줄링

연계 포인트:
1. 컨텍스트 스위치 시:
   - IQ, ROB 플러시 필요
   - RAT(레지스터 매핑) 저장/복원
   - 파이프라인 버블 발생 (~10-20 사이클)

2. SMT(Simultaneous Multithreading):
   - IQ를 스레드별로 분할 또는 공유
   - 공유 시: 한 스레드가 IQ 독점 방지 필요
   - 분할 시: IQ 활용률 저하 가능

3. 우선순위 스케줄링:
   - 실시간 스레드의 명령어 우선 발급
   - IQ Select 로직에서 스레드 우선순위 반영
```

#### [컴퓨터구조 + 컴파일러] 정적 스케줄링과 동적 발급의 시너지
```
컴파일러 정적 스케줄링:
- 명령어 순서 재배치로 데이터 의존성 완화
- 지연 숨김(Latency Hiding)을 위한 명령어 삽입
- VLIW/EPIC에서는 컴파일러가 발급 담당

동적 발급 큐:
- 런타임 의존성 해결
- 예측 불가능한 지연(캐시 미스) 대응
- 정적 스케줄링의 한계 보완

시너지 효과:
- 컴파일러: 의존성이 적은 순서로 배치
- 발급 큐: 캐시 미스 등 동적 상황 대응
- 결과: 정적+동적 최적화의 결합으로 IPC 극대화
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

#### 시나리오 1: 고성능 서버 CPU 발급 큐 설계
```
요구사항:
- 8발급(superscalar width=8) 수퍼스칼라 프로세서
- 높은 IPC, 전력은 2순위

설계 결정:
1. Unified IQ 채용
   - 총 60-80 엔트리
   - 정수/FP/메모리 명령어 혼합 수용

2. Speculative Wakeup
   - 캐시 미스 예측으로 Wakeup 지연 숨김
   - Misprediction 시 Select 취소

3. Port 할당 정책
   - 8개 실행 포트: 4 ALU, 2 AGU, 1 FPU, 1 Branch
   - 유연한 포트 바인딩

예상 성능:
- IPC: 3.5-4.0 (이론적 최대 8 대비)
- 발급 큐 활용률: 75-85%
```

#### 시나리오 2: 저전력 모바일 CPU 발급 큐 설계
```
요구사항:
- 4발급, 배터리 효율 최우선
- 면적 제약

설계 결정:
1. Split IQ 채용
   - Integer IQ: 16 entries
   - FP IQ: 12 entries
   - Memory IQ: 12 entries

2. Clock Gating
   - 사용하지 않는 IQ 섹션 클럭 차단
   - 엔트리 단위 Power Gating

3. Compact Select
   - 간단한 Round-Robin 선택
   - 복잡한 Age-Based 대신 에너지 절약

예상 성능:
- IPC: 2.0-2.5
- 전력: Unified 대비 40% 절감
```

### 도입 시 고려사항 (체크리스트)

#### 기술적 고려사항
- [ ] 발급 폭(Issue Width)과 IQ 크기 비율 (2:1 ~ 4:1)
- [ ] Wakeup-Select Critical Path 타이밍
- [ ] Misprediction 복구 메커니즘
- [ ] SMT 지원 시 스레드 격리 정책

#### 운영/보안적 고려사항
- [ ] Spectre 유사 공격 방지 (발급 예측 완화)
- [ ] 전력 관리 정책 (DVFS 연동)
- [ ] 핫스팟 온도 모니터링

### 주의사항 및 안티패턴

1. **과도한 IQ 크기**: Amdahl의 법칙에 의해 수익 체감
2. **Wakeup Misprediction**: 잘못된 Wakeup으로 발급 후 취소
3. **Head-of-Line Blocking**: IQ 앞쪽 미준비 명령어의 지연 전파
4. **Starvation**: 낮은 우선순위 명령어의 무한 대기

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 개선 전 (순차) | 개선 후 (발급 큐) | 향상률 |
|------|---------------|------------------|--------|
| IPC | 1.0 | 3.0-4.5 | +200-350% |
| 실행 유닛 활용률 | 25-35% | 70-90% | +100-150% |
| 명령어 지연(평균) | 기준 | -30-50% | -30-50% |
| 면적 오버헤드 | 0% | +15-25% | +15-25% |
| 전력 오버헤드 | 0% | +20-35% | +20-35% |

### 미래 전망 및 진화 방향

1. **AI 전용 발급 큐**
   - Matrix 연산을 위한 특화된 IQ
   - Tensor Core 연산의 효율적 발급

2. **적응형 발급 큐**
   - 워크로드 특성에 따른 IQ 크기 동적 조절
   - ML 기반 발급 예측

3. **보안 강화 발급**
   - Speculative Execution 공격 방지
   - 안전한 발급 정책

### ※ 참고 표준/가이드
- **ARM Architecture Reference Manual**: 발급 큐 권장 사항
- **Intel Optimization Manual**: 발급 정책 및 포트 할당
- **IEEE Micro**: 수퍼스칼라 발급 큐 연구 논문

---

## 📌 관련 개념 맵 (Knowledge Graph)

1. [수퍼스칼라](../5_pipelining/236_superscalar.md) - 다중 명령어 발급 아키텍처
2. [비순차 실행](../5_pipelining/238_out_of_order_execution.md) - 발급 큐의 핵심 활용 시나리오
3. [레지스터 리네이밍](../5_pipelining/239_register_renaming.md) - 발급 전 명령어 변환
4. [재주문 버퍼(ROB)](../5_pipelining/240_reorder_buffer.md) - 발급 후 완료 순서 관리
5. [예약역](../5_pipelining/241_reservation_station.md) - 발급 큐의 구현 형태
6. [파이프라인 해저드](../5_pipelining/221_pipeline_hazards.md) - 발급 큐가 해결하는 문제
7. [명령어 병렬성(ILP)](../10_parallel/385_thread_level_parallelism.md) - 발급 큐가 활용하는 병렬성

---

## 👶 어린이를 위한 3줄 비유 설명

1. **발급 큐가 뭐야?**: 놀이공원 놀이기구 앞 대기줄 같은 거야. 사람들이 줄을 서서 기다리는데, 준비된 사람부터 먼저 탈 수 있게 정리해주는 곳이야.

2. **어떻게 작동해?**: 여러 기구(실행 유닛)가 있어서 준비된 사람을 가장 적합한 기구로 보내줘. 키가 큰 사람은 롤러코스터로, 작은 사람은 회전목마로 보내는 것처럼!

3. **왜 중요해?**: 기구를 놀지 않고 최대한 많이 돌게 해서, 같은 시간에 더 많은 사람이 놀 수 있게 해줘. 발급 큐가 없으면 기구가 비어도 사람이 없어서 놀지 못할 거야!
