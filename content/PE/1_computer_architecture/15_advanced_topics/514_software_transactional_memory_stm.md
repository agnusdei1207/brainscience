+++
title = "514. 소프트웨어 트랜잭셔널 메모리 (STM)"
date = "2026-03-05"
[extra]
categories = "studynotes-computer-architecture"
+++

# 소프트웨어 트랜잭셔널 메모리 (STM, Software Transactional Memory)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어로 구현된 트랜잭셔널 메모리로, 하드웨어 지원 없이 메모리 연산들의 원자성을 보장하며, 락 기반 동기화의 복잡성을 추상화한다.
> 2. **가치**: 모든 플랫폼에서 동작하며 용량 제한이 없어 HTM보다 유연하지만, 오버헤드가 커서(2-10배) 높은 경합 환경에서는 성능 저하가 발생할 수 있다.
> 3. **융합**: 메모리 관리, 가비지 컬렉션, 컴파일러 최적화와 밀접하게 연관되며, 함수형 프로그래밍 패러다임과 잘 맞는다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
소프트웨어 트랜잭셔널 메모리(STM)는 하드웨어 지원 없이 순수 소프트웨어로 트랜잭셔널 메모리를 구현한 것이다. STM은 메모리 접근을 추적하기 위해 소프트웨어 자료구조(Read Set, Write Set)를 사용하며, 충돌 감지와 롤백을 런타임 라이브러리나 컴파일러가 처리한다. HTM에 비해 오버헤드가 크지만, 하드웨어 제약이 없고 모든 시스템에서 동작한다는 장점이 있다.

### 💡 비유
STM은 "은행의 계좌 이체 시스템"과 같다. HTM은 계산기(하드웨어)로 빠르게 계산하지만 용량이 제한되고, STM은 장부(소프트웨어)에 모든 거래를 적어가며 계산한다. 장부 방식은 느리지만, 거래 내역을 무제한으로 적을 수 있고 어느 은행에서나 사용할 수 있다.

### 등장 배경 및 발전 과정

#### 1. 기존 기술의 치명적 한계점
- **HTM의 제약**: 하드웨어 의존, 용량 제한
- **락의 복잡성**: 구현 어렵고 버그 발생
- **이식성**: HTM은 구형 시스템에서 사용 불가

#### 2. 패러다임 변화의 역사
- **1995년**: Shavit & Touitou가 STM 개념 제안
- **2000년대**: Haskell STM, Clojure STM
- **2005년**: Herlihy 등이 lock-free STM
- **2010년대**: TL2 (Transactional Locking II)
- **현재**: Haskell, Clojure, Scala 등 함수형 언어에서 널리 사용

---

## Ⅱ. 아키프텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|--------|----------|-------------------|-----------|------|
| **Read Set** | 읽은 메모리 위치 추적 | 해시 테이블/리스트로 주소 저장 | Hash Map, Bloom Filter | 읽기 목록 |
| **Write Set** | 쓴 메모리 위치와 값 저장 | 주소→(새 값, 이전 값) 매핑 | Hash Map, Log | 쓰기 일지 |
| **버전 관리자** | 메모리 위치별 버전 추적 | 글로벌 카운터 또는 타임스탬프 | Vector Clock | 수정 번호 |
| **락 매니저** | 충돌 해결을 위한 락 | Fine-grained 락 또는 optimistic | Striped Lock | 예약 시스템 |
| **로그** | 롤백을 위한 이전 값 저장 | Undo Log | Write-Ahead Log | 백업 |
| **커밋 프로토콜** | 원자적 커밋 보장 | 2-Phase Commit, Validation | ACID | 승인 절차 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    소프트웨어 트랜잭셔널 메모리 (STM) 아키텍처                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │                        사용자 코드 (User Code)                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐  │ │
│  │  │  atomic {                                                          │  │ │
│  │  │      x = account1.balance;   // Read                               │  │ │
│  │  │      y = account2.balance;   // Read                               │  │ │
│  │  │      account1.balance = x - 100;  // Write                         │  │ │
│  │  │      account2.balance = y + 100;  // Write                         │  │ │
│  │  │  }  // Commit                                                      │  │ │
│  │  └─────────────────────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                          │
│                                      ▼                                          │
│  ════════════════════════════════════════════════════════════════════════════  │
│                          STM 런타임 (STM Runtime)                               │
│  ════════════════════════════════════════════════════════════════════════════  │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │                      트랜잭션 컨텍스트 (Transaction Context)               │ │
│  │  ┌───────────────────────────────────────────────────────────────────────┐│ │
│  │  │  Thread-Local Storage에 저장되는 상태:                                 ││ │
│  │  │                                                                       ││ │
│  │  │  ┌─────────────────┐    ┌─────────────────────────────────────────┐  ││ │
│  │  │  │   Read Set      │    │   Write Set                              │  ││ │
│  │  │  │  ┌───────────┐  │    │  ┌───────────────────────────────────┐  │  ││ │
│  │  │  │  │ Addr → Ver│  │    │  │ Addr → (Old Value, New Value)    │  │  ││ │
│  │  │  │  ├───────────┤  │    │  ├───────────────────────────────────┤  │  ││ │
│  │  │  │  │ 0x100 → 5 │  │    │  │ 0x200 → (1000, 900)              │  │  ││ │
│  │  │  │  │ 0x200 → 5 │  │    │  │ 0x300 → (500, 600)               │  │  ││ │
│  │  │  │  │ ...       │  │    │  │ ...                              │  │  ││ │
│  │  │  │  └───────────┘  │    │  └───────────────────────────────────┘  │  ││ │
│  │  │  └─────────────────┘    └─────────────────────────────────────────┘  ││ │
│  │  │                                                                       ││ │
│  │  │  상태: ACTIVE | COMMITTED | ABORTED                                   ││ │
│  │  │  시작 시간: start_timestamp                                           ││ │
│  │  └───────────────────────────────────────────────────────────────────────┘│ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │                   글로벌 메타데이터 (Global Metadata)                      │ │
│  │                                                                           │ │
│  │  ┌────────────────────────────────────────────────────────────────────┐  │ │
│  │  │  글로벌 카운터 (Global Clock)                                       │  │ │
│  │  │  ┌──────────────────────────────────────────────────────────────┐  │  │ │
│  │  │  │  0  │  1  │  2  │  3  │  4  │ ... │  N  │  N+1 │             │  │  │ │
│  │  │  └──────────────────────────────────────────────────────────────┘  │  │ │
│  │  │  ▲ 현재 시간                                                         │  │ │
│  │  │  - 각 커밋마다 증가                                                   │  │ │
│  │  │  - 버전 확인에 사용                                                   │  │ │
│  │  └────────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                           │ │
│  │  ┌────────────────────────────────────────────────────────────────────┐  │ │
│  │  │  메모리 메타데이터 (각 객체별)                                        │  │ │
│  │  │  ┌──────────────────────────────────────────────────────────────┐  │  │ │
│  │  │  │  Object Addr │ Version/Lock │ Data                          │  │  │ │
│  │  │  ├──────────────┼──────────────┼────────────────────────────────┤  │  │ │
│  │  │  │  0x1000      │  ver=5       │  account1                      │  │  │ │
│  │  │  │  0x2000      │  ver=7       │  account2                      │  │  │ │
│  │  │  │  ...         │  ...         │  ...                           │  │  │ │
│  │  │  └──────────────┴──────────────┴────────────────────────────────┘  │  │ │
│  │  └────────────────────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │                    STM 연산 흐름 (Operation Flow)                          │ │
│  │                                                                           │ │
│  │  ① BEGIN:                                                                │ │
│  │     start_time = global_clock.read()                                     │ │
│  │     read_set.clear(); write_set.clear()                                  │ │
│  │                                                                           │ │
│  │  ② READ(addr):                                                           │ │
│  │     if (addr in write_set) return write_set[addr].new_value              │ │
│  │     value = *addr                                                        │ │
│  │     version = get_version(addr)                                          │ │
│  │     if (version > start_time) → CONFLICT → ABORT                         │ │
│  │     read_set.add(addr, version)                                          │ │
│  │     return value                                                         │ │
│  │                                                                           │ │
│  │  ③ WRITE(addr, value):                                                   │ │
│  │     old_value = *addr                                                    │ │
│  │     write_set.add(addr, old_value, value)                                │ │
│  │                                                                           │ │
│  │  ④ COMMIT (Two-Phase):                                                   │ │
│  │     Phase 1 - Lock & Validate:                                           │ │
│  │       - lock all write_set addrs                                         │ │
│  │       - validate all read_set versions unchanged                         │ │
│  │     Phase 2 - Write & Release:                                           │ │
│  │       - write new values to memory                                       │ │
│  │       - update versions                                                  │ │
│  │       - release locks                                                    │ │
│  │                                                                           │ │
│  │  ⑤ ROLLBACK:                                                             │ │
│  │     - restore old values (if written)                                    │ │
│  │     - clear read/write sets                                              │ │
│  │     - restart or fallback                                                │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① Optimistic 동시성 제어 (TL2 알고리즘)
```
TL2 (Transactional Locking II) 동작:

1. 시작 (Begin)
   - 글로벌 카운터에서 현재 시간 읽기: start_time
   - Read Set, Write Set 초기화

2. 읽기 (Read)
   a) Write Set에 있으면 새 값 반환
   b) 없으면 메모리에서 읽기
   c) 읽은 후 버전 확인
   d) 버전이 start_time 이후면 → 충돌 → Abort

3. 쓰기 (Write)
   - Write Set에 (주소, 이전값, 새값) 추가
   - 실제 메모리 쓰기는 Commit 시까지 지연

4. 커밋 (Commit) - 2단계
   Phase 1: Locking & Validation
   - Write Set의 모든 주소 락 획득
   - Read Set의 모든 버전이 변경되지 않았는지 확인
   - 하나라도 실패하면 Abort

   Phase 2: Write & Release
   - Write Set의 새 값을 메모리에 기록
   - 글로벌 카운터 증가하여 새 버전 할당
   - 모든 락 해제
```

#### ② 충돌 감지와 해결
```
충돌 유형:

1. Read-Write Conflict
   Tx1이 addr X를 읽음 (버전 5)
   Tx2가 addr X를 씀 (버전 6)
   Tx1이 커밋 시 확인 → 버전 불일치 → Tx1 Abort

2. Write-Write Conflict
   Tx1과 Tx2 모두 addr X에 쓰려 함
   둘 다 Write Set에 addr X
   커밋 시 락 획득 경쟁 → 한쪽만 성공

해결 전략:

1. Immediate Abort
   - 충돌 감지 즉시 Abort
   - 단순하지만 불필요한 Abort 많음

2. Contention Manager
   - 충돌 시 정책에 따라 한쪽 선택
   - Back-off, Priority, Karma 등

3. Early Release
   - Read Set에서 더 이상 필요 없는 항목 제거
   - 충돌 확률 감소
```

### 핵심 알고리즘 & 실무 코드 예시

#### 간단한 STM 구현 (Python 예시)
```python
import threading
from dataclasses import dataclass, field
from typing import Dict, Set, Any, Optional, List
from enum import Enum
import time
import random

class TransactionState(Enum):
    ACTIVE = "active"
    COMMITTED = "committed"
    ABORTED = "aborted"

@dataclass
class ReadEntry:
    address: int
    version: int

@dataclass
class WriteEntry:
    address: int
    old_value: Any
    new_value: Any

class TransactionContext:
    """스레드별 트랜잭션 컨텍스트"""
    def __init__(self):
        self.state = TransactionState.ACTIVE
        self.start_time = 0
        self.read_set: Dict[int, ReadEntry] = {}
        self.write_set: Dict[int, WriteEntry] = {}
        self.retry_count = 0

class STMGlobalState:
    """글로벌 STM 상태"""
    def __init__(self):
        self.global_clock = 0
        self.lock = threading.Lock()
        # 메모리 위치별 버전 정보
        self.versions: Dict[int, int] = {}
        # 메모리 위치별 실제 데이터
        self.memory: Dict[int, Any] = {}
        # 메모리 위치별 락
        self.location_locks: Dict[int, threading.Lock] = {}

    def get_version(self, address: int) -> int:
        return self.versions.get(address, 0)

    def get_lock(self, address: int) -> threading.Lock:
        if address not in self.location_locks:
            self.location_locks[address] = threading.Lock()
        return self.location_locks[address]

# 글로벌 STM 상태
stm_global = STMGlobalState()
# 스레드 로컬 컨텍스트
thread_local = threading.local()

def get_context() -> TransactionContext:
    if not hasattr(thread_local, 'context'):
        thread_local.context = TransactionContext()
    return thread_local.context

class STMRef:
    """STM 관리 메모리 참조"""
    def __init__(self, address: int, initial_value: Any = None):
        self.address = address
        with stm_global.lock:
            if address not in stm_global.memory:
                stm_global.memory[address] = initial_value
                stm_global.versions[address] = 0

    def read(self) -> Any:
        """트랜잭션 내 읽기"""
        ctx = get_context()

        # Write Set에 있으면 새 값 반환
        if self.address in ctx.write_set:
            return ctx.write_set[self.address].new_value

        # 메모리에서 읽기
        with stm_global.lock:
            value = stm_global.memory.get(self.address)
            version = stm_global.versions.get(self.address, 0)

        # 버전 확인
        if version > ctx.start_time:
            raise STMConflictError("Version changed after start")

        # Read Set에 추가
        ctx.read_set[self.address] = ReadEntry(self.address, version)
        return value

    def write(self, value: Any):
        """트랜잭션 내 쓰기"""
        ctx = get_context()

        # 현재 값 확인 (Read Set에 없으면 읽기)
        if self.address not in ctx.read_set and self.address not in ctx.write_set:
            old_value = self.read()
        elif self.address in ctx.write_set:
            old_value = ctx.write_set[self.address].old_value
        else:
            old_value = ctx.read_set[self.address]

        # Write Set에 추가
        ctx.write_set[self.address] = WriteEntry(self.address, old_value, value)

class STMConflictError(Exception):
    """STM 충돌 예외"""
    pass

class STM:
    """STM 메인 클래스"""

    @staticmethod
    def begin():
        """트랜잭션 시작"""
        ctx = get_context()
        ctx.state = TransactionState.ACTIVE
        ctx.read_set.clear()
        ctx.write_set.clear()

        with stm_global.lock:
            ctx.start_time = stm_global.global_clock

    @staticmethod
    def commit():
        """트랜잭션 커밋 (2-Phase)"""
        ctx = get_context()

        if ctx.state != TransactionState.ACTIVE:
            raise Exception("Transaction not active")

        # Phase 1: Lock & Validate
        locks_to_release = []
        try:
            # 모든 Write Set 주소 락 획득
            for addr in sorted(ctx.write_set.keys()):  # 정렬로 데드락 방지
                lock = stm_global.get_lock(addr)
                lock.acquire()
                locks_to_release.append((addr, lock))

            # Read Set 검증
            with stm_global.lock:
                for addr, entry in ctx.read_set.items():
                    current_version = stm_global.versions.get(addr, 0)
                    if current_version != entry.version:
                        raise STMConflictError(f"Read conflict at {addr}")

            # Phase 2: Write & Release
            with stm_global.lock:
                # 새 값 기록
                for addr, entry in ctx.write_set.items():
                    stm_global.memory[addr] = entry.new_value

                # 버전 업데이트
                stm_global.global_clock += 1
                new_version = stm_global.global_clock
                for addr in ctx.write_set:
                    stm_global.versions[addr] = new_version

            ctx.state = TransactionState.COMMITTED

        except STMConflictError:
            ctx.state = TransactionState.ABORTED
            raise

        finally:
            # 락 해제
            for addr, lock in locks_to_release:
                lock.release()

    @staticmethod
    def rollback():
        """트랜잭션 롤백"""
        ctx = get_context()
        ctx.state = TransactionState.ABORTED
        ctx.read_set.clear()
        ctx.write_set.clear()

    @staticmethod
    def atomic(func, *args, max_retries=10, **kwargs):
        """원자적 실행 래퍼"""
        retries = 0
        while retries < max_retries:
            try:
                STM.begin()
                result = func(*args, **kwargs)
                STM.commit()
                return result
            except STMConflictError:
                STM.rollback()
                retries += 1
                # 백오프
                time.sleep(random.random() * 0.001 * retries)

        raise Exception(f"Transaction failed after {max_retries} retries")

# 사용 예시
def transfer_money(from_account: STMRef, to_account: STMRef, amount: int):
    """트랜잭셔널 계좌 이체"""
    def do_transfer():
        balance_from = from_account.read()
        balance_to = to_account.read()

        if balance_from < amount:
            raise ValueError("Insufficient funds")

        from_account.write(balance_from - amount)
        to_account.write(balance_to + amount)
        return True

    return STM.atomic(do_transfer)

# 테스트
def test_stm():
    print("=== STM 테스트 ===")

    # 계좌 생성
    account1 = STMRef(1, 1000)
    account2 = STMRef(2, 500)

    # 이체 테스트
    print(f"초기: A1={account1.read()}, A2={account2.read()}")

    # 동시 이체 시뮬레이션
    def worker1():
        for _ in range(100):
            try:
                transfer_money(account1, account2, 10)
            except:
                pass

    def worker2():
        for _ in range(100):
            try:
                transfer_money(account2, account1, 5)
            except:
                pass

    t1 = threading.Thread(target=worker1)
    t2 = threading.Thread(target=worker2)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(f"최종: A1={account1.read()}, A2={account2.read()}")
    print(f"총합: {account1.read() + account2.read()} (1500이어야 함)")

if __name__ == "__main__":
    test_stm()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: STM vs HTM

| 항목 | HTM | STM | 하이브리드 |
|------|-----|-----|-----------|
| **하드웨어 요구** | 필요 | 불필요 | 선택적 |
| **용량 제한** | 있음 (~32KB) | 없음 | HTM 제한까지 |
| **오버헤드** | 낮음 (5-20%) | 높음 (100-500%) | 중간 |
| **이식성** | 제한적 | 높음 | 중간 |
| **일관성** | 강함 | 강함 | 강함 |

### 과목 융합 관점 분석

#### [프로그래밍 언어 + 컴퓨터구조] 언어별 STM
```
Haskell STM:
- 모나드 기반, 순수 함수형
- compose 가능한 트랜잭션
- 가장 성숙한 STM

Clojure STM:
- Ref 타입으로 STM 관리
- MVCC (Multi-Version Concurrency Control)
- 동적 타이핑과 잘 맞음

Java (상위 레벨):
- AtomicReference 등
- STM 라이브러리 존재
- JVM 최적화와 결합
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단

#### 시나리오 1: 언어 선택
```
상황: 높은 동시성 요구사항
요구: 개발 생산성과 성능 균형

분석:
- Haskell: STM 지원 최고, 학습 곡선
- Clojure: JVM 생태계, 동시성 좋음
- Python/Java: STM 라이브러리 제한적

결정: Clojure
- STM 내장, JVM 호환
- 함수형 스타일과 STM 궁합 좋음
```

---

## Ⅴ. 기대효과 및 결론

### 정량적/정성적 기대효과

| 지표 | 락 | STM (낮은 경합) | STM (높은 경합) |
|------|-----|-----------------|-----------------|
| 처리량 | 기준 | +50~100% | -30~0% |
| 개발 복잡도 | 높음 | 낮음 | 낮음 |
| 데드락 | 가능 | 불가능 | 불가능 |

---

## 📌 관련 개념 맵 (Knowledge Graph)

1. [HTM](./513_transactional_memory_htm.md) - 하드웨어 기반 TM
2. [락](../11_synchronization/413_hardware_synchronization.md) - 대안 동기화
3. [CAS](../11_synchronization/415_compare_and_swap.md) - Lock-free 기반
4. [캐시 일관성](../11_synchronization/402_cache_coherence.md) - 동시성 기반

---

## 👶 어린이를 위한 3줄 비유 설명

1. **STM이 뭐야?**: 장부에 모든 일을 적어가며 하는 게임이에요. 무슨 일을 했는지 다 적어두고, 문제가 생기면 장부를 보고 처음으로 돌아가요.

2. **HTM과 뭐가 달라요?**: HTM은 계산기로 빠르게 하지만 작은 계산만 가능해요. STM은 장부로 하니까 천천히 하지만 아주 큰 계산도 할 수 있어요.

3. **언제 써요?**: 어떤 컴퓨터에서든 쓸 수 있어요. 새 컴퓨터가 없어도, 오래된 컴퓨터에서도 트랜잭셔널 메모리를 쓸 수 있어요!
