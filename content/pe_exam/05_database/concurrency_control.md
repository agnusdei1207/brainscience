+++
title = "동시성 제어 (Concurrency Control)"
date = 2025-03-01

[extra]
categories = "pe_exam-database"
+++

# 동시성 제어 (Concurrency Control)

## 핵심 인사이트 (3줄 요약)
> **다수 트랜잭션이 동시 실행될 때 데이터 일관성을 보장하는 핵심 메커니즘**. 로킹(2PL), MVCC, 타임스탬프 기법이 대표적. 직렬 가능성(Serializability)이 이론적 기준, 성능과 일관성의 트레이드오프가 핵심 과제.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 동시성 제어(Concurrency Control)는 **여러 트랜잭션이 동시에 실행될 때, 상호 간섭으로 인한 데이터 불일치를 방지하고 직렬 가능성(Serializability)을 보장하는 데이터베이스 관리 기법**이다. ACID 중 I(Isolation)를 담당한다.

> 💡 **비유**: 동시성 제어는 **"화장실 열쇠 관리"** 같아요. 화장실(데이터)을 한 사람이 쓰고 있을 때 다른 사람은 대기해야 하죠. 하지만 MVCC는 **"비디오 대여점"** 같아요. 한 사람이 대여한 비디오를 다른 사람도 복사본으로 볼 수 있죠!

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 동시성 문제(Anomaly)**: 갱신 손실, 오손 읽기, 반복 불가능 읽기, 유령 읽기 발생
2. **기술적 필요성 - 성능과 일관성 균형**: 순차 실행은 안전하지만 성능 저하, 병렬 실행은 빠르지만 위험
3. **시장/산업 요구 - 고성능 OLTP**: 초당 수만 건 트랜잭션 처리하면서도 데이터 정합성 필수

**핵심 목적**: **직렬 가능성 보장**하면서 **동시성 최대화** (Throughput 향상)

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **공유 락 (S-Lock)** | 읽기 전용 잠금 | 여러 트랜잭션 동시 획득 가능 | 도서관 대출 |
| **베타 락 (X-Lock)** | 읽기+쓰기 잠금 | 단독 획득만 가능 | 화장실 열쇠 |
| **MVCC** | 다중 버전 관리 | 읽기 차단 없음 | 사본 제공 |
| **타임스탬프** | 트랜잭션 순서 부여 | 락 없이 순서 보장 | 접수 번호 |
| **교착상태 감지** | Deadlock Detection | 주기적 대기 그래프 검사 | 교통 체증 감지 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────┐
│                    동시성 문제 (Anomaly) 4가지                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Lost Update (갱신 손실)                                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  T1: READ(x=100) → x=x+10 → WRITE(x=110)                    │   │
│  │  T2:    READ(x=100) → x=x+20 → WRITE(x=120)                 │   │
│  │  결과: x=120 (T1의 +10이 사라짐!)                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  2. Dirty Read (오손 읽기)                                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  T1: WRITE(x=200) ─────────────────────→ ROLLBACK           │   │
│  │  T2:          READ(x=200) → 사용 (없는 데이터!)              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  3. Non-repeatable Read (반복 불가능 읽기)                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  T1: READ(x=100) ────────────────→ READ(x=200)              │   │
│  │  T2:          UPDATE(x=200) → COMMIT                         │   │
│  │  같은 쿼리가 다른 결과!                                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  4. Phantom Read (유령 읽기)                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  T1: SELECT WHERE age>20 → 5행 ────→ SELECT → 6행           │   │
│  │  T2:           INSERT(age=25) → COMMIT                       │   │
│  │  갑자기 새로운 행이 나타남!                                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    2단계 로킹 프로토콜 (2PL)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   락 보유 수                                                        │
│        ↑                                                            │
│        │      ┌───────┐                                            │
│        │     /        │  축소 단계                                 │
│        │    /  확장   │  (Unlock만 가능)                           │
│        │   /   단계   │                                            │
│        │  /  (Lock만  │                                            │
│        │ /   가능)    │                                            │
│        │/             │                                            │
│        └──────────────┴───→ 시간                                    │
│              ↑                                                       │
│          Lock Point                                                  │
│     (이 시점 이후 unlock 시작)                                       │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  Strict 2PL: 모든 X-Lock을 커밋/롤백까지 보유               │  │
│   │  → 연쇄 복귀(Cascading Rollback) 방지                       │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    MVCC (다중 버전 동시성 제어)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [데이터 구조]                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  id │ name   │ salary │ tx_id_start │ tx_id_end │ ptr       │  │
│   ├────┼────────┼────────┼─────────────┼───────────┼────────────┤  │
│   │  1 │ 홍길동 │  5000  │     100     │   NULL    │ ──────────┐│  │
│   │  1 │ 홍길동 │  4500  │      50     │    100    │ ←────────┘│  │
│   │  1 │ 홍길동 │  4000  │      10     │     50    │           │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   [읽기 작업]                                                       │
│   - 자신의 tx_id보다 작은 tx_id_start를 가진 버전 읽기              │
│   - 쓰기와 충돌 없음!                                               │
│                                                                     │
│   [쓰기 작업]                                                       │
│   - 새 버전 생성, 이전 버전의 tx_id_end 갱신                        │
│   - 읽기와 충돌 없음!                                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 트랜잭션 시작 → ② 락/MVCC 적용 → ③ 읽기/쓰기 수행 → ④ 충돌 검사 → ⑤ 커밋/롤백
```

- **1단계 - 트랜잭션 시작**: BEGIN TRANSACTION, 트랜잭션 ID 할당
- **2단계 - 락/MVCC 적용**: 접근 전 필요한 락 획득 또는 스냅샷 생성
- **3단계 - 읽기/쓰기 수행**: 데이터 접근, MVCC의 경우 적절한 버전 선택
- **4단계 - 충돌 검사**: 낙관적 제어의 경우 검증 단계에서 충돌 확인
- **5단계 - 커밋/롤백**: 모든 락 해제, MVCC의 경우 가비지 컬렉션 수행

**핵심 알고리즘/공식** (해당 시 필수):

```
[락 호환성 매트릭스]
              요청한 락
              S      X
보유 락  S   O(✓)   X(대기)
         X   X(대기) X(대기)

[교착상태 4가지 필요조건 (Coffman 조건)]
1. 상호 배제 (Mutual Exclusion): 자원은 한 번에 하나만 사용
2. 점유 대기 (Hold and Wait): 자원 가진 채 다른 자원 대기
3. 비선점 (No Preemption): 강제로 자원 뺏기 불가
4. 순환 대기 (Circular Wait): 대기 사이클 형성

→ 하나라도 제거하면 교착상태 발생 안 함!

[교착상태 해결 전략]
1. 예방 (Prevention):
   - 모든 자원 미리 획득
   - 자원 순서 부여 (A → B 순서로만 획득)

2. 회피 (Avoidance):
   - Wait-Die: 오래된 T가 대기, 새로운 T는 사망(롤백)
   - Wound-Wait: 오래된 T가 선점, 새로운 T는 대기

3. 탐지 (Detection):
   - 대기 그래프(Wait-For Graph) 주기적 검사
   - 사이클 존재 시 교착상태

4. 복구 (Recovery):
   - 희생자(Victim) 선택하여 롤백
   - 기아(Starvation) 방지: 롤백 횟수 고려

[MVCC 가시성 규칙 (PostgreSQL 스타일)]
버전이 보이려면:
1. tx_id_start < 현재_tx_id (이전에 생성)
2. tx_id_end가 NULL이거나 > 현재_tx_id (아직 종료 안 됨)
3. 생성한 트랜잭션이 커밋됨

[격리 수준별 발생 문제]
격리 수준        | Dirty Read | Non-repeat | Phantom | Lost Update
-----------------|------------|------------|---------|------------
READ UNCOMMITTED|     O      |     O      |    O    |     O
READ COMMITTED   |     X      |     O      |    O    |     O
REPEATABLE READ  |     X      |     X      |    O    |     O
SERIALIZABLE     |     X      |     X      |    X    |     X
```

**코드 예시** (필수: Python 또는 의사코드):
```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum
import threading
import time
from collections import defaultdict

class LockType(Enum):
    SHARED = "S"      # 읽기 전용
    EXCLUSIVE = "X"   # 읽기 + 쓰기

@dataclass
class Lock:
    """락 정보"""
    transaction_id: int
    lock_type: LockType
    resource: str

@dataclass
class Transaction:
    """트랜잭션 정보"""
    id: int
    start_time: float
    state: str = "active"  # active, committed, aborted
    locks: List[Lock] = field(default_factory=list)

class LockManager:
    """2PL 기반 락 매니저"""

    def __init__(self):
        self.locks: Dict[str, List[Lock]] = defaultdict(list)
        self.transactions: Dict[int, Transaction] = {}
        self.wait_for_graph: Dict[int, Set[int]] = defaultdict(set)
        self.lock = threading.Lock()

    def begin_transaction(self, tx_id: int) -> Transaction:
        """트랜잭션 시작"""
        tx = Transaction(id=tx_id, start_time=time.time())
        self.transactions[tx_id] = tx
        return tx

    def acquire_lock(self, tx_id: int, resource: str,
                     lock_type: LockType, timeout: float = 5.0) -> bool:
        """락 획득 (호환성 검사 + 대기)"""
        start = time.time()

        while time.time() - start < timeout:
            with self.lock:
                # 기존 락과 호환성 검사
                compatible = True
                blocking_txs = set()

                for existing_lock in self.locks[resource]:
                    if existing_lock.transaction_id == tx_id:
                        continue  # 자신의 락

                    # 호환성 검사
                    if not self._is_compatible(existing_lock.lock_type, lock_type):
                        compatible = False
                        blocking_txs.add(existing_lock.transaction_id)

                if compatible:
                    # 락 획득
                    new_lock = Lock(tx_id, lock_type, resource)
                    self.locks[resource].append(new_lock)
                    self.transactions[tx_id].locks.append(new_lock)

                    # 대기 그래프에서 제거
                    if tx_id in self.wait_for_graph:
                        del self.wait_for_graph[tx_id]
                    return True
                else:
                    # 대기 그래프 갱신
                    self.wait_for_graph[tx_id] = blocking_txs

                    # 교착상태 검사
                    if self._detect_deadlock(tx_id):
                        raise DeadlockException(f"Deadlock detected for T{tx_id}")

            time.sleep(0.01)  # 짧은 대기 후 재시도

        return False  # 타임아웃

    def _is_compatible(self, existing: LockType, requested: LockType) -> bool:
        """락 호환성 검사"""
        if existing == LockType.SHARED and requested == LockType.SHARED:
            return True
        return False

    def release_lock(self, tx_id: int, resource: str) -> None:
        """락 해제"""
        with self.lock:
            self.locks[resource] = [
                l for l in self.locks[resource]
                if l.transaction_id != tx_id
            ]

    def release_all_locks(self, tx_id: int) -> None:
        """트랜잭션 모든 락 해제"""
        tx = self.transactions.get(tx_id)
        if tx:
            for lock in tx.locks:
                self.release_lock(tx_id, lock.resource)
            tx.locks.clear()

    def _detect_deadlock(self, tx_id: int) -> bool:
        """교착상태 검사 (대기 그래프 사이클 탐지)"""
        visited = set()
        rec_stack = set()

        def dfs(node: int) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.wait_for_graph.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True  # 사이클 발견

            rec_stack.remove(node)
            return False

        return dfs(tx_id)

class DeadlockException(Exception):
    """교착상태 예외"""
    pass

@dataclass
class MVCCVersion:
    """MVCC 버전 레코드"""
    value: any
    created_by: int      # 생성한 트랜잭션 ID
    deleted_by: Optional[int] = None  # 삭제한 트랜잭션 ID

class MVCCManager:
    """MVCC 기반 동시성 제어"""

    def __init__(self):
        self.data: Dict[str, List[MVCCVersion]] = defaultdict(list)
        self.committed_txs: Set[int] = set()
        self.current_tx_id = 0
        self.lock = threading.Lock()

    def begin_transaction(self) -> int:
        """새 트랜잭션 ID 할당"""
        with self.lock:
            self.current_tx_id += 1
            return self.current_tx_id

    def read(self, key: str, tx_id: int) -> Optional[any]:
        """스냅샷 읽기 (자신의 트랜잭션 ID보다 작은 커밋된 버전)"""
        versions = self.data.get(key, [])

        for version in reversed(versions):
            # 자신이 생성한 미커밋 버전
            if version.created_by == tx_id and tx_id not in self.committed_txs:
                if version.deleted_by is None:
                    return version.value
                else:
                    return None  # 자신이 삭제함

            # 커밋된 버전 중 가시성 확인
            if version.created_by in self.committed_txs:
                if version.created_by < tx_id:
                    # 삭제되지 않았거나, 삭제 후에 시작한 트랜잭션
                    if version.deleted_by is None:
                        return version.value
                    elif version.deleted_by > tx_id:
                        return version.value

        return None

    def write(self, key: str, value: any, tx_id: int) -> bool:
        """새 버전 생성"""
        # 기존 버전 찾기
        versions = self.data.get(key, [])
        old_version = None

        for v in versions:
            if v.created_by == tx_id:
                old_version = v
                break

        if old_version:
            # 자신의 버업데이트
            old_version.value = value
        else:
            # 새 버전 생성
            self.data[key].append(MVCCVersion(value=value, created_by=tx_id))

            # 이전 커밋 버전의 deleted_by 설정
            for v in reversed(versions[:-1]):
                if v.created_by in self.committed_txs:
                    # 충돌 검사
                    if v.deleted_by is None:
                        v.deleted_by = tx_id
                    break

        return True

    def commit(self, tx_id: int) -> bool:
        """트랜잭션 커밋"""
        with self.lock:
            self.committed_txs.add(tx_id)
        return True

    def rollback(self, tx_id: int) -> None:
        """트랜잭션 롤백 (버전 제거)"""
        with self.lock:
            for key in self.data:
                self.data[key] = [
                    v for v in self.data[key]
                    if v.created_by != tx_id
                ]
                # deleted_by 복원
                for v in self.data[key]:
                    if v.deleted_by == tx_id:
                        v.deleted_by = None

    def garbage_collect(self, oldest_active_tx: int) -> None:
        """오래된 버전 정리 (가비지 컬렉션)"""
        with self.lock:
            for key in self.data:
                self.data[key] = [
                    v for v in self.data[key]
                    if v.created_by >= oldest_active_tx or
                       (v.deleted_by is not None and v.deleted_by >= oldest_active_tx)
                ]

# 동시성 문제 시뮬레이터
class ConcurrencySimulator:
    """동시성 제어 시뮬레이션"""

    def __init__(self, use_mvcc: bool = True):
        if use_mvcc:
            self.manager = MVCCManager()
        else:
            self.manager = LockManager()
        self.use_mvcc = use_mvcc
        self.results = {}

    def simulate_lost_update(self) -> Dict:
        """갱신 손실 시뮬레이션"""
        # 초기값 설정
        if self.use_mvcc:
            tx0 = self.manager.begin_transaction()
            self.manager.write("balance", 100, tx0)
            self.manager.commit(tx0)

            # 두 트랜잭션이 동시에 읽고 수정
            tx1 = self.manager.begin_transaction()
            tx2 = self.manager.begin_transaction()

            # 둘 다 같은 값 읽음
            v1 = self.manager.read("balance", tx1)  # 100
            v2 = self.manager.read("balance", tx2)  # 100

            # 둘 다 수정
            self.manager.write("balance", v1 + 10, tx1)  # 110
            self.manager.write("balance", v2 + 20, tx2)  # 120

            # 커밋 순서에 따라 결과 결정
            self.manager.commit(tx1)
            self.manager.commit(tx2)

            final = self.manager.read("balance", 999)

            return {
                "initial": 100,
                "tx1_add": 10,
                "tx2_add": 20,
                "expected": 130,
                "actual": final,
                "lost_update": final != 130
            }
        else:
            return {"message": "Lock-based simulation requires blocking"}

    def simulate_dirty_read(self) -> Dict:
        """오손 읽기 시뮬레이션"""
        if self.use_mvcc:
            tx0 = self.manager.begin_transaction()
            self.manager.write("data", "A", tx0)
            self.manager.commit(tx0)

            tx1 = self.manager.begin_transaction()
            tx2 = self.manager.begin_transaction()

            # T1이 수정 (미커밋)
            self.manager.write("data", "B", tx1)

            # T2가 읽기 (MVCC에서는 이전 커밋 버전 읽음)
            v2 = self.manager.read("data", tx2)

            # T1이 롤백
            self.manager.rollback(tx1)

            # T2가 읽은 값 확인
            return {
                "t1_wrote": "B",
                "t2_read": v2,
                "t1_rolled_back": True,
                "dirty_read_prevented": v2 == "A"  # MVCC는 이전 버전 읽음
            }

# 사용 예시
if __name__ == "__main__":
    print("=== 2PL Lock Manager Demo ===")
    lock_mgr = LockManager()

    tx1 = lock_mgr.begin_transaction(1)
    tx2 = lock_mgr.begin_transaction(2)

    # S-Lock 호환
    print(f"T1 S-Lock on A: {lock_mgr.acquire_lock(1, 'A', LockType.SHARED)}")
    print(f"T2 S-Lock on A: {lock_mgr.acquire_lock(2, 'A', LockType.SHARED)}")  # OK

    # X-Lock 비호환
    print(f"T1 X-Lock on B: {lock_mgr.acquire_lock(1, 'B', LockType.EXCLUSIVE)}")
    # T2는 대기하게 됨

    lock_mgr.release_all_locks(1)
    lock_mgr.release_all_locks(2)

    print("\n=== MVCC Demo ===")
    mvcc = MVCCManager()

    tx1 = mvcc.begin_transaction()
    mvcc.write("item", "v1", tx1)
    mvcc.commit(tx1)

    tx2 = mvcc.begin_transaction()
    tx3 = mvcc.begin_transaction()

    # T2가 읽기
    print(f"T2 reads: {mvcc.read('item', tx2)}")  # v1

    # T3가 수정
    mvcc.write("item", "v2", tx3)
    mvcc.commit(tx3)

    # T2는 여전히 이전 버전
    print(f"T2 reads after T3 commit: {mvcc.read('item', tx2)}")  # v1 (스냅샷)

    # 새 트랜잭션은 최신 버전
    tx4 = mvcc.begin_transaction()
    print(f"T4 reads: {mvcc.read('item', tx4)}")  # v2

    print("\n=== Lost Update Simulation ===")
    sim = ConcurrencySimulator(use_mvcc=True)
    result = sim.simulate_lost_update()
    print(result)
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| 장점 | 단점 |
|-----|------|
| **데이터 일관성**: 직렬 가능성 보장 | **성능 저하**: 락 대기, 충돌로 인한 처리량 감소 |
| **ACID 보장**: Isolation 완벽 구현 | **교착상태 위험**: 2PL의 경우 데드락 발생 가능 |
| **트랜잭션 안전성**: 이상 현상 방지 | **구현 복잡도**: MVCC, 타임스탬프 관리 오버헤드 |
| **표준화**: SQL 표준 격리 수준 | **트레이드오프**: 일관성 vs 동시성 균형 필요 |

**동시성 제어 기법별 비교** (필수: 최소 2개 대안):
| 비교 항목 | 2PL (로킹) | MVCC | 타임스탬프 |
|---------|-----------|------|-----------|
| **핵심 특성** | 락으로 상호 배제 | ★ 버전으로 비차단 | 순서로 직렬화 |
| **읽기 차단** | O (S/X 충돌) | X (★ 비차단) | X |
| **쓰기 차단** | O | 부분 (충돌 시) | X |
| **교착상태** | O (★ 위험) | X | X |
| **오버헤드** | 낮음 | 중간 (버전 관리) | 중간 (타임스탬프) |
| **적합 환경** | 전통적 OLTP | ★ 읽기 많은 웹 | 실시간 시스템 |
| **대표 DBMS** | Oracle, MySQL | PostgreSQL, MySQL(InnoDB) | 일부 연구용 |

| 비교 항목 | 비관적 제어 | 낙관적 제어 |
|---------|-----------|-----------|
| **가정** | 충돌이 자주 발생 | 충돌이 드물다 |
| **락 사용** | O (미리 획득) | X (검증 시에만) |
| **동시성** | 낮음 | ★ 높음 |
| **충돌 시** | 대기 | 롤백 후 재시도 |
| **적합 환경** | 높은 경합 | 낮은 경합, 읽기 많음 |

> **★ 선택 기준**:
> - **2PL**: 높은 정합성 요구, 쓰기 많은 환경
> - **MVCC**: 읽기 많은 웹 서비스, PostgreSQL/MySQL(InnoDB)
> - **낙관적**: 낮은 충돌률, 분산 환경

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **금융 이체 시스템** | SERIALIZABLE 격리 + 2PL | 이중 출금 100% 방지 |
| **전자상거래 재고** | 낙관적 락 + 버전 컬럼 | 동시 주문 처리율 3배 향상 |
| **SNS 피드 조회** | MVCC + READ COMMITTED | 피드 조회 응답 50ms 이내 |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1 - PostgreSQL**: MVCC 기본 채택, 동시 읽기/쓰기 차단 없이 처리량 10배 향상
- **사례 2 - MySQL InnoDB**: MVCC + 레코드 락 혼합, 갭 락으로 팬텀 리드 방지
- **사례 3 - Oracle**: 다중 버전 읽기 일관성(Statement-level, Transaction-level) 제공

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**:
   - 격리 수준 선택 (비용 vs 정합성)
   - 락 타임아웃 설정
   - 교착상태 감지 주기
   - MVCC 가비지 컬렉션
2. **운영적**:
   - 락 대기 모니터링
   - 교착상태 발생 빈도 추적
   - 장기 실행 트랜잭션 관리
   - 격리 수준별 성능 테스트
3. **보안적**:
   - 권한 없는 데이터 접근과 무관
   - 트랜잭션 로그 보호
4. **경제적**:
   - 높은 격리 수준 = 낮은 처리량
   - MVCC 저장 공간 오버헤드
   - 동시성 vs 일관성 비용 분석

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ **과도한 락**: 너무 높은 격리 수준 → 성능 급격히 저하
- ❌ **장기 트랜잭션**: 락 장시간 보유 → 전체 시스템 지연
- ❌ **교착상태 무시**: 감지 안 하면 시스템 멈춤
- ❌ **MVCC 공간 무시**: 버전 누적 → 디스크 폭증, 정기 VACUUM 필요

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 동시성 제어와 밀접하게 연관된 핵심 개념들

┌─────────────────────────────────────────────────────────────────┐
│  동시성 제어 핵심 연관 개념 맵                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [트랜잭션] ←──→ [동시성제어] ←──→ [인덱싱]                    │
│       ↓              ↓               ↓                          │
│   [ACID]        [교착상태]      [락매니저]                       │
│       ↓              ↓               ↓                          │
│   [회복기법]    [격리수준]      [MVCC]                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| **트랜잭션** | 선행 개념 | 동시성 제어 대상 | `[트랜잭션](../transaction.md)` |
| **교착상태** | 하위 개념 | 동시성 제어의 부작용 | `[교착상태](../../02_operating_system/deadlock.md)` |
| **회복 기법** | 보완 개념 | 롤백 시 데이터 복구 | `[회복기법](./recovery.md)` |
| **분산DB** | 확장 개념 | 분산 환경 동시성 | `[분산DB](./distributed_database.md)` |
| **인덱싱** | 보완 기술 | 락과 인덱스 상호작용 | `[인덱싱](./relational/indexing.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **데이터 일관성** | 이상 현상 방지 | 데이터 오류 0건 |
| **처리량** | 동시 트랜잭션 증가 | TPS 3~5배 향상 |
| **응답 시간** | 비차단 읽기 | 평균 50ms 이내 |
| **가용성** | 교착상태 자동 해결 | 장애 시간 0분 |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**: Deterministic Database로 교착상태 원천 방지, 분산 합의(Raft/Paxos) 기반 동시성
2. **시장 트렌드**: NewSQL에서 분산 동시성 제어, Spanner의 TrueTime 같은 글로벌 타임스탬프
3. **후속 기술**: 분산 MVCC, CRDT(Conflict-free Replicated Data Types)로 낙관적 동시성 확장

> **결론**: 동시성 제어는 데이터베이스의 핵심 기능으로, 성능과 일관성의 트레이드오프를 어떻게 관리하느냐가 시스템 품질을 결정한다. MVCC가 현대 DBMS의 주류로 자리 잡았으나, 2PL도 여전히 높은 정합성이 필요한 영역에서 사용된다.

> **※ 참고 표준**: ANSI SQL-92 격리 수준, Gray's Transaction Processing, PostgreSQL MVCC 문서

---

## 어린이를 위한 종합 설명 (필수)

**동시성 제어**은(는) 마치 **"놀이공원 대기줄 관리"** 같아요.

놀이공원에서 인기 있는 롤러코스터를 타려고 해요. 한 번에 한 명만 탈 수 있다면 줄이 너무 길어지겠죠? 그래서 **여러 명이 동시에 탈 수 있게 하되, 안전하게 관리하는 방법**이 필요해요.

**락(Lock)** 방식은 **"화장실 열쇠"** 같아요. 한 사람이 열쇠를 가지고 들어가면, 다른 사람은 나올 때까지 기다려야 해요. 안전하지만 오래 기다려야 하죠.

**MVCC** 방식은 **"비디오 대여점"** 같아요. 원본은 하나지만, 필요한 사람마다 복사본을 빌려줄 수 있어요. 여러 사람이 동시에 볼 수 있죠! 대신 복사본이 많아지면 정리가 필요해요.

**교착상태(Deadlock)**는 **"좁은 길에서 마주친 두 자동차"** 같아요. 서로 "비켜주세요"라고 하면서도, 상대방이 먼저 비켜주길 기다리는 상황이에요. 둘 다 움직이지 못하죠!

동시성 제어 덕분에 많은 사람이 **안전하게, 그리고 빠르게** 데이터를 사용할 수 있어요! 🎢🔒
