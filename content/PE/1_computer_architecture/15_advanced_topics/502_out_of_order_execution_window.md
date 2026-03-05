+++
title = "502. 비순차 실행 윈도우"
date = "2026-03-05"
[extra]
categories = "studynotes-computer-architecture"
+++

# 비순차 실행 윈도우 (Out-of-Order Execution Window)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비순차 실행 프로세서가 명령어 간 의존성을 분석하며 병렬 실행할 수 있는 명령어들의 범위로, ROB 크기, 발급 큐 용량, 물리 레지스터 수에 의해 결정된다.
> 2. **가치**: 실행 윈도우 크기가 클수록 메모리 지연을 더 효과적으로 숨길 수 있어, IPC 1.5-3배 향상 및 메모리 병목 완화 효과를 달성한다.
> 3. **융합**: 캐시 미스, 분기 예측 실패 등의 장지연 이벤트 발생 시 실행 윈도우 내 독립 명령어들을 최대한 활용하여 성능 손실을 최소화한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
비순차 실행 윈도우(Out-of-Order Execution Window, OoO Window)는 CPU가 프로그램 순서와 관계없이 실행할 수 있는 명령어들의 집합이다. 프로세서는 이 윈도우 내에서 데이터 의존성이 없는 명령어들을 찾아 먼저 실행함으로써, 메모리 접근 지연이나 캐시 미스로 인한 대기 시간을 유용한 작업으로 채울 수 있다. 실행 윈도우의 크기는 하드웨어 리소스(ROB 엔트리 수, 발급 큐 크기, 물리 레지스터 수)에 의해 제한되며, 현대 고성능 CPU에서는 200-600+ 명령어까지 처리할 수 있다.

### 💡 비유
비순차 실행 윈도우는 "뷔페 레스토랑에서 여러 손님이 동시에 음식을 가져가는 상황"과 같다. 앞사람이 스테이크를 기다리는 동안(메모리 대기), 뒷사람은 샐러드 코너로 가서 바로 음식을 가져갈 수 있다(독립 명령어 실행). 창문(윈도우) 크기가 클수록 더 많은 손님이 동시에 움직일 수 있어, 전체 식사 시간이 단축된다. 하지만 창문이 너무 크면 직원이 주문을 관리하기 어렵고(하드웨어 복잡도), 혼란이 발생할 수 있다.

### 등장 배경 및 발전 과정

#### 1. 기존 기술의 칼명적 한계점
- **순차 실행의 파이프라인 스톨**: 데이터 의존성으로 인해 후속 명령어가 대기
- **메모리 지연 숨김 불가**: 캐시 미스 발생 시 수십~수백 사이클 동안 CPU 유휴
- **ILP(Instruction-Level Parallelism) 미활용**: 프로그램 내 숨은 병렬성을 발견 못함

#### 2. 패러다임 변화의 역사
- **1967년**: IBM System/360 Model 91 최초의 비순차 실행
- **1990년**: IBM RS/6000 토마술로 알고리즘 상용화
- **1995년**: Intel Pentium Pro, ROB 기반 비순차 실행 (윈도우 크기 ~40)
- **2000년**: Intel Pentium 4, 윈도우 크기 ~126
- **2010년**: Intel Sandy Bridge, 윈도우 크기 ~168
- **2020년**: Apple M1, 윈도우 크기 ~600+
- **2024년**: Intel Raptor Lake, 윈도우 크기 ~500+

#### 3. 비즈니스적 요구사항
- 데이터센터: 메모리 대역폭 활용 극대화
- 모바일: 배터리 효율과 성능 균형
- AI/ML: 대규모 행렬 연산의 병렬성 활용

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|--------|----------|-------------------|-----------|------|
| **Reorder Buffer (ROB)** | 비순차 실행 결과를 순차적으로 커밋 | 168-600+ 엔트리, Head/Tail 포인터 관리 | In-Order Commit | 주문 순서 대기열 |
| **Issue Queue (IQ)** | 실행 대기 명령어 저장 및 발급 | 32-128 엔트리, Wakeup/Select 로직 | CAM, Age-based Selection | 주문 처리 대기 |
| **Physical Register File** | 리네이밍된 레지스터 저장 | 128-384+ 레지스터, Free List 관리 | Register Renaming | 번호표 보관함 |
| **Load/Store Queue (LSQ)** | 메모리 연산 순서 관리 | 64-128 엔트리, 주소 의존성 추적 | Memory Disambiguation | 배달 주문 관리 |
| **Rename Table (RAT)** | 아키텍처→물리 레지스터 매핑 | 16-32 엔트리 (x86 GPR), Checkpointing | Speculative Rename | 예약 현황판 |
| **Free List** | 사용 가능한 물리 레지스터 목록 | 비트맵 또는 FIFO 큐로 관리 | Register Allocation | 빈 번호표 목록 |
| **Branch Order Buffer** | 분기 예측 복구용 상태 저장 | 예측 실패 시 롤백 | Checkpoint, Rename Recovery | 주문 취소 내역 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  비순차 실행 윈도우 (Out-of-Order Execution Window)           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │              In-Order Front-end (Fetch → Decode → Rename)            │   │
│  │  ┌─────────┐   ┌──────────┐   ┌────────────────────────────────┐   │   │
│  │  │ Fetch   │ → │ Decode   │ → │ Rename (RAT + Free List)       │   │   │
│  │  │ 4-6/cyc │   │ 4-6/cyc  │   │ Arch Reg → Physical Reg Map    │   │   │
│  │  └─────────┘   └──────────┘   └──────────────────┬─────────────┘   │   │
│  └──────────────────────────────────────────────────┼──────────────────┘   │
│                                                     │                      │
│  ═══════════════════════════════════════════════════╪═══════════════════   │
│                          ▼                          │                      │
│  ┌──────────────────────────────────────────────────▼──────────────────┐   │
│  │                 OUT-OF-ORDER EXECUTION WINDOW                        │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐│   │
│  │  │                                                                 ││   │
│  │  │   ┌─────────────────────────────────────────────────────────┐   ││   │
│  │  │   │            Reorder Buffer (ROB) - 224 entries           │   ││   │
│  │  │   │  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐      │   ││   │
│  │  │   │  │  0  │  1  │  2  │  3  │  4  │  5  │  6  │  7  │ ...  │   ││   │
│  │  │   │  │ Done│ Done│ Done│Exec │ Wait│ Wait│Alloc│     │      │   ││   │
│  │  │   │  │  ✓  │  ✓  │  ✓  │     │     │     │     │      │   ││   │
│  │  │   │  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘      │   ││   │
│  │  │   │         ↑ Head (Commit)              ↑ Tail (Allocate)  │   ││   │
│  │  │   └─────────────────────────────────────────────────────────┘   ││   │
│  │  │                                                                 ││   │
│  │  │   ┌───────────────────────┐  ┌───────────────────────────────┐  ││   │
│  │  │   │   Integer IQ (64)     │  │     FP/Vector IQ (48)         │  ││   │
│  │  │   │  ┌─────┬─────┬─────┐  │  │  ┌─────┬─────┬─────┬─────┐   │  ││   │
│  │  │   │  │Ready│Wait │Ready│  │  │  │Ready│Ready│Wait │Wait │   │  ││   │
│  │  │   │  └─────┴─────┴─────┘  │  │  └─────┴─────┴─────┴─────┘   │  ││   │
│  │  │   └───────────┬───────────┘  └───────────┬───────────────────┘  ││   │
│  │  │               │                          │                       ││   │
│  │  │   ┌───────────▼──────────────────────────▼────────────────────┐ ││   │
│  │  │   │              Execution Units (ALU, MUL, FPU, etc.)         │ ││   │
│  │  │   │   [Port0] [Port1] [Port2] [Port3] [Port4] [Port5] [Port6] │ ││   │
│  │  │   └───────────────────────────┬───────────────────────────────┘ ││   │
│  │  │                               │                                 ││   │
│  │  │   ┌───────────────────────────▼───────────────────────────────┐ ││   │
│  │  │   │        Physical Register File (PRF) - 288 registers       │ ││   │
│  │  │   │  [P0] [P1] [P2] ... [P287] ← Data values, Tags            │ ││   │
│  │  │   └───────────────────────────────────────────────────────────┘ ││   │
│  │  │                                                                 ││   │
│  │  │   ┌─────────────────────────────────────────────────────────┐   ││   │
│  │  │   │         Load/Store Queue (LSQ) - 128 entries            │   ││   │
│  │  │   │  ┌────────────────────┐  ┌────────────────────────────┐ │   ││   │
│  │  │   │  │  Load Queue (64)   │  │   Store Queue (64)         │ │   ││   │
│  │  │   │  │  [Addr] [Data]     │  │   [Addr] [Data] [Commit]   │ │   ││   │
│  │  │   │  └────────────────────┘  └────────────────────────────┘ │   ││   │
│  │  │   └─────────────────────────────────────────────────────────┘   ││   │
│  │  │                                                                 ││   │
│  │  └─────────────────────────────────────────────────────────────────┘│   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                     │                      │
│  ═══════════════════════════════════════════════════╪═══════════════════   │
│                          ▼                          │                      │
│  ┌──────────────────────────────────────────────────▼──────────────────┐   │
│  │                 In-Order Commit (ROB → Arch State)                   │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐│   │
│  │  │  Commit: 결과를 아키텍처 상태에 반영, Physical Reg 해제         ││   │
│  │  │  Exception/Precise Interrupt 처리                              ││   │
│  │  └─────────────────────────────────────────────────────────────────┘│   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① 실행 윈도우의 구성 및 제한 요소

```
실행 윈도우 크기 = min(ROB 크기, IQ 크기 × 발급 비율, PRF 크기, LSQ 크기)

1. ROB (Reorder Buffer)
   - 비순차 실행 명령어의 최대 개수 결정
   - Intel Core: 224 entries (Sunny Cove)
   - Apple M1: ~600 entries
   - AMD Zen 4: 256 entries

2. Issue Queue (IQ)
   - 동시에 발급 대기 가능한 명령어 수
   - IQ가 가득 차면 Dispatch Stall
   - 일반적으로 ROB의 30-50% 크기

3. Physical Register File (PRF)
   - 리네이밍에 필요한 레지스터 수
   - 최소: 아키텍처 레지스터 + ROB 엔트리
   - 실제: 2-3배 더 많음 (중복 할당 방지)

4. Load/Store Queue (LSQ)
   - 메모리 연산 추적 용량
   - 메모리密集 워크로드에서 윈도우 크기 제한
```

#### ② 실행 윈도우 내 의존성 그래프

```
프로그램 코드:
  1. LD  R1, [A]      ; 캐시 미스 (200 사이클)
  2. ADD R2, R1, 1    ; R1 의존
  3. LD  R3, [B]      ; 독립
  4. MUL R4, R3, 2    ; R3 의존
  5. ADD R5, R2, R4   ; R2, R4 의존
  6. ST  [C], R5      ; R5 의존

의존성 그래프:
         1.LD(A)
            │
            ▼
         2.ADD ─────────────────┐
            (R1 대기)            │
                                 │
    3.LD(B)                      │
       │                         │
       ▼                         │
    4.MUL ───────────────────────┤
       (R3 대기, 1과 병렬)        │
                                 │
            ▼                    ▼
              5.ADD (R2, R4 대기)
                   │
                   ▼
              6.ST (R5 대기)

실행 순서 (비순차):
  사이클 0:   1.LD 발급 (캐시 미스), 3.LD 발급 (히트)
  사이클 5:   3.LD 완료 → 4.MUL 발급
  사이클 10:  4.MUL 완료 (R4 준비), R1 아직 대기
  사이클 200: 1.LD 완료 → 2.ADD 발급
  사이클 202: 2.ADD 완료 → 5.ADD 발급 (R2, R4 모두 준비)
  사이클 204: 5.ADD 완료 → 6.ST 발급

효과: 200 사이클 대기 중 다른 작업 수행 → 전체 시간 단축
```

#### ③ 실행 윈도우 확장 기법

```
1. ROB 확장
   - 더 많은 비순차 명령어 수용
   - Apple M1: 600+ entries (경쟁사 2배)
   - Trade-off: 면적, 전력 증가

2. 분기 예측과 결합
   - 예측된 경로의 명령어도 윈도우에 포함
   - Misprediction 시 롤백
   - 예측 정확도 중요

3. SMT (Simultaneous Multithreading)
   - 윈도우를 스레드 간 공유 또는 분할
   - 한 스레드의 병목을 다른 스레드로 숨김

4. Checkpoint/Restore
   - 윈도우 상태 저장으로 빠른 복구
   - 분기 예측 실패 시 오버헤드 감소
```

### 핵심 알고리즘 & 실무 코드 예시

#### 실행 윈도우 시뮬레이터
```python
class OutOfOrderExecutionWindow:
    def __init__(self, rob_size=224, iq_size=64, prf_size=288):
        self.rob_size = rob_size
        self.iq_size = iq_size
        self.prf_size = prf_size

        self.rob = []  # Reorder Buffer
        self.iq = []   # Issue Queue
        self.prf = {}  # Physical Register File
        self.free_regs = list(range(prf_size))
        self.rat = {}   # Register Alias Table

    def get_window_size(self):
        """현재 실행 윈도우 크기 반환"""
        return len(self.rob)

    def can_dispatch(self):
        """새 명령어 디스패치 가능 여부"""
        return (len(self.rob) < self.rob_size and
                len(self.iq) < self.iq_size and
                len(self.free_regs) > 0)

    def dispatch(self, instr):
        """명령어를 실행 윈도우에 추가"""
        if not self.can_dispatch():
            return False

        # 물리 레지스터 할당
        phys_reg = self.free_regs.pop(0)
        old_reg = self.rat.get(instr.dest, None)
        self.rat[instr.dest] = phys_reg

        # ROB 엔트리 생성
        rob_entry = {
            'instr': instr,
            'phys_reg': phys_reg,
            'old_reg': old_reg,
            'ready': False,
            'value': None
        }
        self.rob.append(rob_entry)

        # IQ에 추가 (의존성 확인)
        operands_ready = self._check_operands_ready(instr)
        iq_entry = {
            'rob_idx': len(self.rob) - 1,
            'instr': instr,
            'ready': operands_ready
        }
        self.iq.append(iq_entry)

        return True

    def _check_operands_ready(self, instr):
        """명령어의 오퍼랜드 준비 상태 확인"""
        for src in instr.sources:
            if src in self.rat:
                phys_reg = self.rat[src]
                if phys_reg not in self.prf:
                    return False
        return True

    def issue(self):
        """준비된 명령어 발급"""
        for i, entry in enumerate(self.iq):
            if entry['ready']:
                # 발급 후 IQ에서 제거
                return self.iq.pop(i)
        return None

    def complete(self, rob_idx, value):
        """명령어 완료 처리"""
        self.rob[rob_idx]['ready'] = True
        self.rob[rob_idx]['value'] = value
        phys_reg = self.rob[rob_idx]['phys_reg']
        self.prf[phys_reg] = value

        # Wakeup: 의존 명령어들 활성화
        self._wakeup_dependents(phys_reg)

    def _wakeup_dependents(self, ready_reg):
        """의존 명령어들 Wakeup"""
        for entry in self.iq:
            if not entry['ready']:
                instr = entry['instr']
                for src in instr.sources:
                    if src in self.rat and self.rat[src] == ready_reg:
                        # 해당 소스가 준비됨
                        pass  # 실제로는 모든 소스 확인 필요
                if self._check_operands_ready(instr):
                    entry['ready'] = True

    def commit(self):
        """순차적 커밋"""
        committed = []
        while self.rob and self.rob[0]['ready']:
            entry = self.rob.pop(0)
            # 이전 물리 레지스터 해제
            if entry['old_reg'] is not None:
                self.free_regs.append(entry['old_reg'])
            committed.append(entry)
        return committed
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 실행 윈도우 크기별 성능 분석

| 프로세서 | ROB 크기 | IQ 크기 | PRF 크기 | IPC (SPECint) | 전력 효율 |
|---------|---------|---------|---------|--------------|----------|
| **Intel Skylake** | 224 | 64 | 288 | 2.8 | 중간 |
| **Intel Sunny Cove** | 352 | 96 | 352 | 3.2 | 중간 |
| **AMD Zen 3** | 256 | 72 | 192 | 3.0 | 높음 |
| **Apple M1 Firestorm** | 600+ | 180+ | 380+ | 3.5+ | 매우 높음 |
| **ARM Cortex-X1** | 224 | 64 | 192 | 2.6 | 높음 |

### 과목 융합 관점 분석

#### [컴퓨터구조 + 운영체제] 인터럽트와 실행 윈도우
```
Precise Interrupt 문제:
- 인터럽트 발생 시점의 정확한 상태 복구 필요
- 비순차 실행으로 순서가 뒤섞임
- ROB를 통한 순차적 커밋으로 해결

처리 과정:
1. 인터럽트 발생
2. 파이프라인 플러시
3. ROB에서 커밋되지 않은 명령어 폐기
4. RAT를 아키텍처 상태로 복원
5. 물리 레지스터 해제
6. ISR 진입

오버헤드: ~50-100 사이클 (윈도우 크기에 비례)
```

#### [컴퓨터구조 + 컴파일러] ILP 추출과 실행 윈도우
```
컴파일러의 역할:
- 정적 명령어 스케줄링
- 의존성 거리 증가 (윈도우 내 병렬성 향상)
- 루프 언롤링으로 ILP 증가

예시:
// 원본 코드
for (i=0; i<N; i++) {
    a[i] = b[i] + c[i];
}

// 언롤링 (4x)
for (i=0; i<N; i+=4) {
    a[i]   = b[i]   + c[i];
    a[i+1] = b[i+1] + c[i+1];
    a[i+2] = b[i+2] + c[i+2];
    a[i+3] = b[i+3] + c[i+3];
}

효과: 실행 윈도우 내 4개의 독립 연산 → 병렬 실행 가능
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

#### 시나리오 1: 실행 윈도우 크기 결정
```
요구사항: 새로운 CPU 설계에서 실행 윈도우 크기 결정

분석 요소:
1. 목표 워크로드 분석
   - 메모리密集: 큰 윈도우 유리
   - 계산密集: 작은 윈도우도 충분

2. 전력/면적 예산
   - ROB 224→352: 면적 +15%, 전력 +12%
   - IPC 향상: +8-12%

3. 클럭 주파수 영향
   - 큰 윈도우: 더 복잡한 로직 → 클럭 감소 가능

결정:
- 일반용: ROB 224, IQ 64
- 고성능용: ROB 352, IQ 96
- 모바일용: ROB 160, IQ 48
```

#### 시나리오 2: 캐시 미스 시 실행 윈도우 활용
```
상황: L3 캐시 미스로 100+ 사이클 대기

실행 윈도우 역할:
1. 미스 명령어 이후의 독립 명령어 계속 실행
2. 윈도우가 클수록 더 많은 작업 숨김 가능

계산:
- 윈도우 크기: 224
- 평균 IPC: 3.0
- 이론적 숨김 가능 사이클: 224 / 3.0 ≈ 75 사이클

결론:
- 100사이클 미스의 ~75%를 숨길 수 있음
- 더 큰 윈도우로 개선 가능
```

### 도입 시 고려사항 (체크리스트)

#### 기술적 고려사항
- [ ] ROB/IQ/PRF 크기 균형
- [ ] Wakeup/Select Critical Path 타이밍
- [ ] 분기 예측 실패 시 롤백 오버헤드
- [ ] SMT 지원 시 리소스 분할 정책

#### 운영/보안적 고려사항
- [ ] Spectre 공격 방지 (윈도우 내 추측 실행 제한)
- [ ] 전력 관리 (윈도우 활용률 기반 DVFS)
- [ ] 핫스팟 관리 (균등 분산)

### 주의사항 및 안티패턴

1. **과도한 윈도우 확장**: 수익 체감, IPC 향상 < 면적 증가
2. **불균형한 리소스**: IQ가 병목인데 ROB만 늘림
3. **메모리 월低估**: 캐시 미스 빈도 과소평가

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 순차 실행 | 작은 윈도우 | 큰 윈도우 | 향상률 |
|------|----------|------------|----------|--------|
| IPC | 1.0 | 2.0-2.5 | 3.0-3.5 | +200-250% |
| 메모리 지연 숨김 | 0% | 40-60% | 70-85% | - |
| 면적 오버헤드 | 0% | +10% | +25% | - |
| 전력 오버헤드 | 0% | +15% | +30% | - |

### 미래 전망 및 진화 방향

1. **AI 특화 실행 윈도우**: Matrix 연산용 대형 윈도우
2. **적응형 윈도우**: 워크로드별 동적 크기 조절
3. **보안 강화**: Speculative 실행 제어

### ※ 참고 표준/가이드
- **Intel Optimization Manual**: 실행 윈도우 활용 가이드
- **ARM Architecture Reference Manual**: OoO 실행 모델
- **IEEE Micro**: 실행 윈도우 연구 논문

---

## 📌 관련 개념 맵 (Knowledge Graph)

1. [비순차 실행](../5_pipelining/238_out_of_order_execution.md) - 실행 윈도우의 핵심 활용 시나리오
2. [재주문 버퍼(ROB)](../5_pipelining/240_reorder_buffer.md) - 실행 윈도우의 핵심 구성요소
3. [수퍼스칼라 발급 큐](./501_superscalar_issue_queue.md) - 실행 윈도우 내 명령어 발급
4. [레지스터 리네이밍](../5_pipelining/239_register_renaming.md) - 물리 레지스터 할당
5. [분기 예측](../5_pipelining/231_branch_prediction.md) - 실행 윈도우 확장
6. [캐시 메모리](../6_cache/259_cache_memory.md) - 메모리 지연 숨김
7. [명령어 병렬성(ILP)](../10_parallel/385_thread_level_parallelism.md) - 실행 윈도우가 활용하는 병렬성

---

## 👶 어린이를 위한 3줄 비유 설명

1. **실행 윈도우가 뭐야?**: 요리사가 한 번에 볼 수 있는 주문서들의 묶음이야. 주문서가 많을수록 재료가 늦게 와도 다른 요리를 먼저 할 수 있어.

2. **왜 중요해?**: 하나의 요리가 늦어져도 다른 요리들을 계속 만들 수 있어서, 손님들이 전체적으로 더 빨리 음식을 받을 수 있어.

3. **어떻게 돼?**: 큰 창문(윈도우)으로 많은 주문을 한눈에 보면, "이건 재료가 오니까 저걸 먼저 하자!"라고 스마트하게 순서를 바꿀 수 있어!
