+++
title = "512. 메시 프로토콜 상태 전이도"
date = "2026-03-05"
[extra]
categories = "studynotes-computer-architecture"
+++

# 메시 프로토콜 상태 전이도 (MESI Protocol State Diagram)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 캐시 일관성 프로토콜(MESI)에서 캐시 라인이 가질 수 있는 네 가지 상태(Modified, Exclusive, Shared, Invalid)와 그 전이 조건을 정의한 상태 머신으로, 멀티코어 시스템의 데이터 일관성을 보장하는 핵심 메커니즘이다.
> 2. **가치**: 상태 전이를 최소화하는 최적화를 통해 불필요한 버스 트랜잭션을 30-50% 감소시키며, Exclusive 상태를 도입하여 단일 프로세서 쓰기 시 무효화 트래픽을 완전히 제거한다.
> 3. **융합**: 캐시 계층 구조, 버스/인터커넥트 프로토콜, 메모리 일관성 모델과 밀접하게 연관되며, MOESI, MESIF 등 확장 프로토콜의 기반이 된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
MESI 프로토콜 상태 전이도는 캐시 일관성을 유지하기 위한 프로토콜에서 각 캐시 라인이 가질 수 있는 상태와 상태 간 전이 조건을 체계적으로 표현한 다이어그램이다. MESI는 Modified(수정됨), Exclusive(배타적), Shared(공유됨), Invalid(무효됨)의 네 가지 상태를 정의하며, 각 상태는 캐시 라인의 현재 데이터 소유권과 수정 가능 여부를 나타낸다. 이 상태 머신은 로컬 프로세서의 읽기/쓰기 요청과 다른 프로세서의 버스 트랜잭션에 따라 상태를 전이시킨다.

### 💡 비유
MESI 상태 전이는 "도서관 책 대출 시스템"과 같다. Invalid는 "책이 없음", Shared는 "여러 사람이 읽기만 할 수 있음", Exclusive는 "혼자만 읽고 있어서 곧 쓸 수도 있음", Modified는 "내가 메모를 해서 원본과 달라짐" 상태다. 누군가 책을 빌리거나 반납하면, 시스템이 자동으로 다른 사람들의 대출 상태를 업데이트한다.

### 등장 배경 및 발전 과정

#### 1. 기존 기술의 치명적 한계점
- **Write-Through 오버헤드**: 모든 쓰기가 메모리로 전파되어 버스 대역폭 낭비
- **Write-Back 불일치**: 캐시간 데이터 불일치 발생 가능
- **단순 프로토콜의 비효율**: MSI 프로토콜에서 단일 프로세서 쓰기도 무효화 필요

#### 2. 패러다임 변화의 역사
- **1980년대 이전**: Write-Through 캐시
- **1983년**: MSI 프로토콜 (Illinois)
- **1980년대 중반**: MESI 프로토콜 (Intel, Illinois)
- **1990년대**: MOESI (AMD), MESIF (Intel)
- **2000년대 이후**: Directory 기반 프로토콜과 결합

#### 3. 비즈니스적 요구사항
- 멀티코어 확장성: 코어 수 증가에도 일관성 유지
- 전력 효율: 불필요한 버스 트랜잭션 감소
- 성능: 캐시 히트율 및 지연시간 최적화

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 (표)

| 상태 | 의미 | 데이터 유효 | 수정 가능 | 메모리와 일치 | 다른 캐시 존재 가능 |
|------|------|------------|-----------|--------------|-------------------|
| **M (Modified)** | 이 캐시만 수정 보유 | O | O | X (dirty) | X |
| **E (Exclusive)** | 이 캐시만 소유 | O | O (M로 전이) | O | X |
| **S (Shared)** | 여러 캐시가 공유 | O | X (무효화 필요) | O | O |
| **I (Invalid)** | 유효하지 않음 | X | X | - | - |

### 정교한 상태 전이 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    MESI 프로토콜 상태 전이도 (State Transition Diagram)            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                           ┌─────────────────┐                                  │
│                           │                 │                                  │
│                           │    MODIFIED     │                                  │
│                           │      (M)        │                                  │
│                           │                 │                                  │
│                           └────────┬────────┘                                  │
│                              ╱     │     ╲                                     │
│                             ╱      │      ╲                                    │
│                    BusRd   ╱       │        ╲  Local Write                     │
│                   (Flush) ╱        │         ╲ (Hit, 트랜잭션 없음)              │
│                          ╱         │          ╲                                │
│                         ╱          │           ╲                               │
│         ┌──────────────▼───┐      │      ┌─────▼──────────────┐               │
│         │                  │      │      │                    │               │
│         │     SHARED       │      │      │    EXCLUSIVE       │               │
│         │       (S)        │      │      │        (E)         │               │
│         │                  │      │      │                    │               │
│         └────────┬─────────┘      │      └─────────┬──────────┘               │
│             ╱    │    ╲           │          ╱     │     ╲                     │
│            ╱     │     ╲          │         ╱      │      ╲                    │
│   BusRdX  ╱      │      ╲  BusRd  │  BusRd ╱       │       ╲ Local Read       │
│  (Inval) ╱       │       ╲ (Stay) │ (→S)  ╱        │        ╲ (Hit)           │
│         ╱        │        ╲       │      ╱         │         ╲                │
│        ╱         │         ╲      │     ╱          │          ╲               │
│  ┌────▼─────┐    │    ┌─────▼─────┐ ┌▼────────┐    │    ┌──────▼──────┐       │
│  │          │    │    │           │ │         │    │    │             │       │
│  │  INVALID │◀───┴───▶│  SHARED   │ │EXCLUSIVE│    │    │  MODIFIED   │       │
│  │    (I)   │         │    (S)    │ │   (E)   │    │    │     (M)     │       │
│  │          │         │           │ │         │    │    │             │       │
│  └──────────┘         └───────────┘ └─────────┘    │    └─────────────┘       │
│       ▲                                         ╱ │                            │
│       │                                        ╱  │                            │
│       │                               Local  ╱   │                            │
│       │                              Read   ╱    │                            │
│       │                             Miss  ╱      │                            │
│       │                                  ╱       │                            │
│       └────────────────────────────────╱────────┘                            │
│                                                                             │
│  ════════════════════════════════════════════════════════════════════════════ │
│                           상세 전이 조건표                                     │
│  ════════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│  현재 상태 │ 로컬 읽기      │ 로컬 쓰기      │ BusRd (다른 코어 읽기)         │
│  ─────────┼───────────────┼───────────────┼───────────────────────────────── │
│  I        │ I→S/E (Miss)  │ I→M (Miss)    │ I (상관없음)                    │
│  S        │ S (Hit)       │ S→M (BusUpgr) │ S (유지)                        │
│  E        │ E (Hit)       │ E→M (트랜잭션X)│ E→S                             │
│  M        │ M (Hit)       │ M (Hit)       │ M→S (Flush)                     │
│                                                                             │
│  현재 상태 │ BusRdX (다른 코어 쓰기) │ BusUpgr (다른 코어 승격)                │
│  ─────────┼───────────────────────┼────────────────────────────────────────── │
│  I        │ I (상관없음)          │ I (상관없음)                            │
│  S        │ S→I                   │ S→I                                    │
│  E        │ E→I                   │ (발생하지 않음)                         │
│  M        │ M→I (Flush)           │ (발생하지 않음)                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① Invalid (I) 상태에서의 전이
```
I → S (로컬 읽기 미스):
1. 프로세서가 읽기 요청
2. 캐시 미스 → BusRd 발행
3. 다른 캐시에 없으면: 메모리에서 로드 → E
4. 다른 캐시에 있으면: 메모리/다른 캐시에서 로드 → S

I → E (로컬 읽기 미스, 다른 캐시에 없음):
1. 프로세서가 읽기 요청
2. 캐시 미스 → BusRd 발행
3. 다른 캐시에서 공유 신호 없음
4. 메모리에서 로드 → E (배타적 소유)

I → M (로컬 쓰기 미스):
1. 프로세서가 쓰기 요청
2. 캐시 미스 → BusRdX 발행
3. 다른 캐시 있으면 무효화
4. 데이터 로드 + 수정 → M
```

#### ② Shared (S) 상태에서의 전이
```
S → S (로컬 읽기 히트):
- 캐시 히트, 상태 유지
- 버스 트랜잭션 없음

S → M (로컬 쓰기):
1. 프로세서가 쓰기 요청
2. 다른 공유자가 있을 수 있음
3. BusUpgr (또는 BusRdX) 발행
4. 다른 캐시 무효화
5. 상태 → M, 데이터 수정

S → I (BusRdX 또는 BusUpgr 수신):
1. 다른 캐시가 쓰기 요청
2. 무효화 신호 수신
3. 상태 → I
```

#### ③ Exclusive (E) 상태에서의 전이 - 핵심 최적화
```
E → E (로컬 읽기 히트):
- 캐시 히트, 상태 유지

E → M (로컬 쓰기) ★ 핵심:
1. 프로세서가 쓰기 요청
2. 이 캐시만 데이터를 가지고 있음 (Exclusive)
3. 버스 트랜잭션 없이 바로 쓰기 가능!
4. 상태 → M

이것이 MESI의 핵심 혁신:
- MSI에서는 S→M 전이 시 항상 무효화 필요
- MESI에서는 E→M 전이 시 무효화 불필요
- 단일 프로세서 워크로드에서 트래픽 대폭 감소

E → S (BusRd 수신):
1. 다른 캐시가 읽기 요청
2. 데이터 제공 (Flush 또는 메모리)
3. 상태 → S (이제 공유)
```

#### ④ Modified (M) 상태에서의 전이
```
M → M (로컬 읽기/쓰기 히트):
- 모든 접근이 히트
- 버스 트랜잭션 없음
- 가장 이상적인 상태

M → S (BusRd 수신):
1. 다른 캐시가 읽기 요청
2. Dirty 데이터를 메모리에 Write-back
3. 다른 캐시에 데이터 제공
4. 상태 → S

M → I (BusRdX 수신):
1. 다른 캐시가 배타적 쓰기 요청
2. Dirty 데이터를 메모리에 Write-back
3. 다른 캐시에 데이터 제공
4. 상태 → I
```

### 핵심 알고리즘 & 실무 코드 예시

#### MESI 상태 머신 시뮬레이터
```python
from dataclasses import dataclass
from typing import Optional, List, Dict
from enum import Enum

class MESIState(Enum):
    MODIFIED = "M"
    EXCLUSIVE = "E"
    SHARED = "S"
    INVALID = "I"

class BusTransaction(Enum):
    BUS_READ = "BusRd"
    BUS_READ_X = "BusRdX"
    BUS_UPGRADE = "BusUpgr"
    FLUSH = "Flush"
    NONE = "None"

@dataclass
class CacheLine:
    state: MESIState
    data: int
    dirty: bool = False

@dataclass
class TransactionResult:
    new_state: MESIState
    bus_transaction: BusTransaction
    data_provided: bool = False
    cache_to_cache_transfer: bool = False
    write_back_needed: bool = False

class MESICacheController:
    def __init__(self, cache_id: int):
        self.cache_id = cache_id
        self.cache: Dict[int, CacheLine] = {}

    def process_local_read(self, address: int,
                          shared_signal: bool) -> TransactionResult:
        """로컬 프로세서의 읽기 요청 처리"""
        if address in self.cache:
            line = self.cache[address]

            if line.state == MESIState.INVALID:
                # 실제로는 미스지만, 시뮬레이션을 위해 포함
                return self._handle_read_miss(address, shared_signal)

            # Hit in any valid state
            return TransactionResult(
                new_state=line.state,
                bus_transaction=BusTransaction.NONE
            )

        return self._handle_read_miss(address, shared_signal)

    def _handle_read_miss(self, address: int,
                         shared_signal: bool) -> TransactionResult:
        """읽기 미스 처리"""
        if shared_signal:
            # 다른 캐시에 데이터가 있음
            self.cache[address] = CacheLine(MESIState.SHARED, 0)
            return TransactionResult(
                new_state=MESIState.SHARED,
                bus_transaction=BusTransaction.BUS_READ,
                data_provided=True
            )
        else:
            # 다른 캐시에 없음 → Exclusive
            self.cache[address] = CacheLine(MESIState.EXCLUSIVE, 0)
            return TransactionResult(
                new_state=MESIState.EXCLUSIVE,
                bus_transaction=BusTransaction.BUS_READ,
                data_provided=True
            )

    def process_local_write(self, address: int) -> TransactionResult:
        """로컬 프로세서의 쓰기 요청 처리"""
        if address in self.cache:
            line = self.cache[address]

            if line.state == MESIState.INVALID:
                return self._handle_write_miss(address)

            elif line.state == MESIState.MODIFIED:
                # 이미 M, 아무 것도 필요 없음
                return TransactionResult(
                    new_state=MESIState.MODIFIED,
                    bus_transaction=BusTransaction.NONE
                )

            elif line.state == MESIState.EXCLUSIVE:
                # E → M, 버스 트랜잭션 없음! (핵심 최적화)
                line.state = MESIState.MODIFIED
                line.dirty = True
                return TransactionResult(
                    new_state=MESIState.MODIFIED,
                    bus_transaction=BusTransaction.NONE
                )

            elif line.state == MESIState.SHARED:
                # S → M, 무효화 필요
                line.state = MESIState.MODIFIED
                line.dirty = True
                return TransactionResult(
                    new_state=MESIState.MODIFIED,
                    bus_transaction=BusTransaction.BUS_UPGRADE
                )

        return self._handle_write_miss(address)

    def _handle_write_miss(self, address: int) -> TransactionResult:
        """쓰기 미스 처리"""
        self.cache[address] = CacheLine(MESIState.MODIFIED, 0, dirty=True)
        return TransactionResult(
            new_state=MESIState.MODIFIED,
            bus_transaction=BusTransaction.BUS_READ_X,
            data_provided=True
        )

    def process_bus_transaction(self, address: int,
                                transaction: BusTransaction,
                                is_provider: bool = False) -> TransactionResult:
        """버스 트랜잭션 수신 처리 (스누핑)"""
        if address not in self.cache:
            return TransactionResult(
                new_state=MESIState.INVALID,
                bus_transaction=BusTransaction.NONE
            )

        line = self.cache[address]
        old_state = line.state

        if transaction == BusTransaction.BUS_READ:
            if old_state == MESIState.INVALID:
                return TransactionResult(old_state, BusTransaction.NONE)

            elif old_state == MESIState.MODIFIED:
                # Flush data, then share
                line.state = MESIState.SHARED
                return TransactionResult(
                    new_state=MESIState.SHARED,
                    bus_transaction=BusTransaction.FLUSH,
                    data_provided=True,
                    write_back_needed=True
                )

            elif old_state == MESIState.EXCLUSIVE:
                line.state = MESIState.SHARED
                return TransactionResult(
                    new_state=MESIState.SHARED,
                    bus_transaction=BusTransaction.NONE
                )

            elif old_state == MESIState.SHARED:
                return TransactionResult(
                    new_state=MESIState.SHARED,
                    bus_transaction=BusTransaction.NONE
                )

        elif transaction == BusTransaction.BUS_READ_X:
            # Other wants exclusive ownership
            if old_state == MESIState.MODIFIED:
                # Must flush data first
                line.state = MESIState.INVALID
                return TransactionResult(
                    new_state=MESIState.INVALID,
                    bus_transaction=BusTransaction.FLUSH,
                    data_provided=True,
                    write_back_needed=True
                )
            else:
                # Just invalidate
                line.state = MESIState.INVALID
                return TransactionResult(
                    new_state=MESIState.INVALID,
                    bus_transaction=BusTransaction.NONE
                )

        elif transaction == BusTransaction.BUS_UPGRADE:
            if old_state == MESIState.SHARED:
                line.state = MESIState.INVALID
                return TransactionResult(
                    new_state=MESIState.INVALID,
                    bus_transaction=BusTransaction.NONE
                )

        return TransactionResult(old_state, BusTransaction.NONE)

class MESISystemSimulator:
    """전체 MESI 시스템 시뮬레이터"""

    def __init__(self, num_caches: int = 4):
        self.num_caches = num_caches
        self.caches = [MESICacheController(i) for i in range(num_caches)]
        self.stats = {
            'reads': 0,
            'writes': 0,
            'bus_transactions': 0,
            'invalidations': 0,
            'write_backs': 0,
            'exclusive_to_modified': 0  # E→M 최적화 횟수
        }

    def read(self, cache_id: int, address: int) -> TransactionResult:
        """캐시에서 읽기 수행"""
        self.stats['reads'] += 1

        # Check if any other cache has this address
        shared_signal = any(
            i != cache_id and
            address in self.caches[i].cache and
            self.caches[i].cache[address].state != MESIState.INVALID
            for i in range(self.num_caches)
        )

        result = self.caches[cache_id].process_local_read(address, shared_signal)

        # Process snoop responses
        if result.bus_transaction != BusTransaction.NONE:
            self.stats['bus_transactions'] += 1

            for i in range(self.num_caches):
                if i != cache_id:
                    snoop_result = self.caches[i].process_bus_transaction(
                        address, result.bus_transaction
                    )
                    if snoop_result.write_back_needed:
                        self.stats['write_backs'] += 1

        return result

    def write(self, cache_id: int, address: int) -> TransactionResult:
        """캐시에서 쓰기 수행"""
        self.stats['writes'] += 1

        result = self.caches[cache_id].process_local_write(address)

        # Track E→M optimization
        if address in self.caches[cache_id].cache:
            if self.caches[cache_id].cache[address].state == MESIState.MODIFIED:
                if result.bus_transaction == BusTransaction.NONE:
                    self.stats['exclusive_to_modified'] += 1

        # Process snoop responses
        if result.bus_transaction != BusTransaction.NONE:
            self.stats['bus_transactions'] += 1

            for i in range(self.num_caches):
                if i != cache_id:
                    snoop_result = self.caches[i].process_bus_transaction(
                        address, result.bus_transaction
                    )
                    if snoop_result.new_state == MESIState.INVALID:
                        self.stats['invalidations'] += 1
                    if snoop_result.write_back_needed:
                        self.stats['write_backs'] += 1

        return result

    def print_stats(self):
        print("\n=== MESI 시스템 통계 ===")
        print(f"읽기 요청: {self.stats['reads']}")
        print(f"쓰기 요청: {self.stats['writes']}")
        print(f"버스 트랜잭션: {self.stats['bus_transactions']}")
        print(f"무효화: {self.stats['invalidations']}")
        print(f"Write-back: {self.stats['write_backs']}")
        print(f"E→M 최적화: {self.stats['exclusive_to_modified']}")

        if self.stats['writes'] > 0:
            opt_rate = self.stats['exclusive_to_modified'] / self.stats['writes']
            print(f"E→M 최적화 비율: {opt_rate:.1%}")

# 시뮬레이션 실행
def run_mesi_simulation():
    sim = MESISystemSimulator(num_caches=4)

    # 시나리오 1: 단일 프로세서 워크로드 (E→M 최적화 활용)
    print("=== 시나리오 1: 단일 프로세서 워크로드 ===")
    sim.read(0, 0x1000)   # Miss → E (다른 캐시에 없음)
    sim.write(0, 0x1000)  # E → M (버스 트랜잭션 없음!)
    sim.write(0, 0x1000)  # M → M (히트)
    sim.read(0, 0x1000)   # M → M (히트)

    # 시나리오 2: 공유 읽기
    print("\n=== 시나리오 2: 공유 읽기 ===")
    sim.read(1, 0x2000)   # Miss → E
    sim.read(2, 0x2000)   # 캐시 1이 S로, 캐시 2도 S
    sim.read(3, 0x2000)   # 모두 S

    # 시나리오 3: 공유 후 쓰기
    print("\n=== 시나리오 3: 공유 후 쓰기 ===")
    sim.read(0, 0x3000)   # → S (여러 캐시가 공유)
    sim.read(1, 0x3000)
    sim.write(0, 0x3000)  # S → M, 다른 캐시 무효화 필요

    sim.print_stats()

if __name__ == "__main__":
    run_mesi_simulation()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 캐시 일관성 프로토콜

| 프로토콜 | 상태 수 | 단일 쓰기 트래픽 | 공유 쓰기 트래픽 | 복잡도 | 특징 |
|----------|---------|-----------------|-----------------|--------|------|
| **MSI** | 3 | 높음 (항상 무효화) | 높음 | 낮음 | 기본형 |
| **MESI** | 4 | 낮음 (E→M 무트랜잭션) | 높음 | 중간 | E 상태 추가 |
| **MOESI** | 5 | 낮음 | 낮음 (Owner 공유) | 높음 | O 상태 추가 |
| **MESIF** | 5 | 낮음 | 중간 | 높음 | F 상태 (Forward) |
| **Dragon** | 4 | 낮음 | 낮음 (Update) | 높음 | Update 기반 |

### 과목 융합 관점 분석

#### [컴퓨터구조 + OS] OS가 MESI에 미치는 영향
```
페이지 할당과 MESI 상태:

1. First-Touch 할당
   - 페이지를 처음 접근한 코어에 할당
   - 초기 상태가 E가 될 확률 높음
   - E→M 최적화 활용 증가

2. NUMA 인식 스케줄링
   - 같은 데이터를 접근하는 스레드를 같은 소켓에 배치
   - S 상태 공유 증가 (소켓 내)
   - 소켓 간 트래픽 감소

3. Huge Page
   - 2MB/1GB 페이지 사용
   - TLB 미스 감소 → 페이지 테이블 접근 감소
   - 간접적으로 캐시 일관성 트래픽 감소
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

#### 시나리오 1: 프로토콜 선택
```
상황: 8코어 x86 서버 CPU 설계
요구: 높은 단일 스레드 성능 + 멀티스레드 처리량

분석:
- 단일 스레드: MESI의 E→M 최적화 유리
- 멀티스레드: 공유 데이터 많음

결정: MOESI (또는 MESIF)
- Owner/Forward 상태로 공유 데이터 제공 오버헤드 감소
- Modified 데이터를 여러 캐시가 공유할 때 유리
```

### 도입 시 고려사항 (체크리스트)

#### 기술적 고려사항
- [ ] 워크로드 특성 (단일/공유 비율)
- [ ] 코어 수와 확장성
- [ ] 버스/인터커넥트 대역폭
- [ ] 전력 예산

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | MSI | MESI | 향상률 |
|------|-----|------|--------|
| 단일 쓰기 트래픽 | 100% | 0-20% | -80~100% |
| 전체 버스 트래픽 | 100% | 60-80% | -20~40% |
| 캐시 히트율 | 기준 | +5-10% | +5-10% |

### 미래 전망 및 진화 방향

1. **Heterogeneous Coherence**: CPU-GPU 간 일관성
2. **CXL Coherence**: 멀티 소켓/노드 일관성
3. **TM-based Coherence**: 트랜잭셔널 메모리 활용

---

## 📌 관련 개념 맵 (Knowledge Graph)

1. [캐시 일관성](../11_synchronization/402_cache_coherence.md) - MESI가 해결하는 문제
2. [스누핑 프로토콜](../11_synchronization/403_snooping_protocol.md) - MESI 구현 방식
3. [MOESI 프로토콜](../11_synchronization/408_moesi_protocol.md) - MESI 확장
4. [Write-Back 캐시](../6_cache/277_write_back.md) - M 상태와 연관
5. [버스 트랜잭션](../9_interconnect/344_bus.md) - 상태 전이 매커니즘

---

## 👶 어린이를 위한 3줄 비유 설명

1. **MESI가 뭐야?**: 장난감을 여러 친구가 같이 쓸 때, 누가 가지고 있는지 적어두는 규칙이에요. "나만 가짐", "같이 씀", "버림" 같은 상태가 있어요.

2. **왜 4가지가 필요해요?**: "나만 읽고 있어서 곧 쓸 수도 있어요"(E) 상태가 없으면, 쓸 때마다 "다른 친구 있어?" 하고 물어봐야 해요. E 상태가 있으면 안 물어봐도 돼요!

3. **어떻게 바뀌어요?**: 친구가 장난감을 달라고 하면 "같이 씀"으로 바뀌고, 누가 고치려고 하면 "버림"으로 바뀌어요. 규칙대로 하면 싸우지 않고 잘 쓸 수 있어요!
