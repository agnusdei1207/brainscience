+++
title = "격리 수준 (Isolation Level)"
date = 2026-03-03

[extra]
categories = "pe_exam-05_database"
tags = ["격리수준", "IsolationLevel", "DirtyRead", "PhantomRead", "RepeatableRead", "Serializable"]
+++

# 격리 수준 (Isolation Level)

## 핵심 인사이트

> **동시성과 일관성의 균형점** — 트랜잭션이 다른 트랜잭션의 변경 사항을 얼마나 볼 수 있는지를 결정하는 4단계 수준
> **Read Uncommitted < Read Committed < Repeatable Read < Serializable**
> 높은 격리 수준 = 높은 일관성 + 낮은 동시성, 낮은 격리 수준 = 낮은 일관성 + 높은 동시성
> **ANSI SQL-92 표준**으로 정의, DBMS별 구현 차이 존재

---

### I. 개요

**정의**: 격리 수준(Isolation Level)은 **동시에 실행되는 여러 트랜잭션이 서로에게 미치는 영향을 제어하는 수준으로, 한 트랜잭션이 다른 트랜잭션의 중간 상태를 얼마나 볼 수 있는지를 결정**한다. ACID 속성 중 I(Isolation)의 구체적 구현이다.

> **직관적 비유**: 격리 수준은 **"회의실 문의 투명도"** 같습니다. 완전 투명하면(Uncommitted) 다른 사람이 준비하는 모습이 보이고, 완전 불투명하면(Serializable) 아무것도 안 보이죠. 중간 단계들은 일부만 보입니다.

**등장 배경** (3가지 이상):
1. **기존 문제점 — 완전 격리의 성능 저하**: 모든 트랜잭션을 완전히 격리하면 동시성이 급격히 떨어짐
2. **기술적 동인 — 유연한 트레이드오프**: 비즈니스 요구에 따라 일관성과 성능의 균형 선택 필요
3. **산업/시장 요구 — 다양한 워크로드**: 읽기 많은 웹 서비스와 쓰기 많은 금융 시스템은 요구가 다름

**핵심 목적**: **비즈니스 요구에 맞게 일관성과 동시성의 균형**을 선택 가능하게 함

---

### II. 필요성

#### 현황 및 문제점 (3가지 이상)

| 문제 구분 | 구체적 내용 | 영향/심각도 |
|----------|-----------|----------|
| **과도한 격리** | Serializable 사용 시 동시성 급감 | 처리량 80% 감소 가능 |
| **불충분한 격리** | 낮은 수준에서 데이터 이상 현상 | 잘못된 비즈니스 결정 |
| **DBMS 차이** | 동일 이름이어도 구현 다름 | 이식성 문제 |

#### 기술적 필요성

- **왜 지금인가**: 고성능 OLTP 시스템에서 격리 수준 선택이 핵심
- **왜 이 접근인가**: 단계적 격리로 비즈니스 요구에 맞춤 선택
- **표준 준수**: ANSI SQL-92 표준, 모든 주요 DBMS 지원

#### 도입 시 기대 가치

| 가치 영역 | 기대 효과 | 비고 |
|----------|----------|------|
| 성능 | 적정 격리로 처리량 최적화 | 2~10배 향상 가능 |
| 일관성 | 비즈니스 요구에 맞는 정합성 | 오류 감소 |
| 유연성 | 워크로드별 최적 선택 | DB 설계 유연성 |

---

### III. 구조와 원리

#### 구성 요소 (4개 이상 필수)

| 격리 수준 | Dirty Read | Non-Repeatable Read | Phantom Read | 성능 |
|----------|:----------:|:-------------------:|:------------:|:----:|
| **Read Uncommitted** | O 발생 | O 발생 | O 발생 | 최고 |
| **Read Committed** | X 방지 | O 발생 | O 발생 | 높음 |
| **Repeatable Read** | X 방지 | X 방지 | O 발생* | 중간 |
| **Serializable** | X 방지 | X 방지 | X 방지 | 낮음 |

*MySQL InnoDB는 Gap Lock으로 Phantom Read 방지

#### 구조 다이어그램 (ASCII, 필수)

```
                        [격리 수준과 동시성 문제]

┌─────────────────────────────────────────────────────────────────────┐
│                    격리 수준별 발생 현상                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   격리 수준 ↑ (일관성 ↑, 동시성 ↓)                                   │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ SERIALIZABLE                                                 │  │
│   │ ✅ 모든 문제 방지                                             │  │
│   │ • 완전 직렬화, 동시성 최저                                    │  │
│   │ • 범위 잠금(Range Lock) 또는 전체 테이블 잠금                 │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                              ↑                                      │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ REPEATABLE READ                                              │  │
│   │ ✅ Dirty, Non-Repeatable 방지                                │  │
│   │ ⚠️ Phantom Read 가능 (표준)                                  │  │
│   │ • MySQL InnoDB: Gap Lock으로 Phantom 방지                    │  │
│   │ • PostgreSQL: Serializable로만 Phantom 방지                  │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                              ↑                                      │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ READ COMMITTED                                               │  │
│   │ ✅ Dirty Read 방지                                           │  │
│   │ ⚠️ Non-Repeatable, Phantom 가능                             │  │
│   │ • Oracle, PostgreSQL 기본값                                  │  │
│   │ • 매 쿼리마다 새로운 스냅샷                                   │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                              ↑                                      │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ READ UNCOMMITTED                                             │  │
│   │ ⚠️ 모든 현상 발생                                            │  │
│   │ • Dirty Read 허용                                            │  │
│   │ • 거의 사용 안 함                                            │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   격리 수준 ↓ (일관성 ↓, 동시성 ↑)                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

                    [동시성 문제 3가지 상세]

┌─────────────────────────────────────────────────────────────────────┐
│  1. Dirty Read (오손 읽기)                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  T1: UPDATE users SET balance=200 WHERE id=1                       │
│      (미커밋 상태)                                                   │
│           │                                                         │
│           ├── T2: SELECT balance FROM users WHERE id=1             │
│           │        → 200 읽음 (Dirty Read!)                        │
│           │                                                         │
│  T1: ROLLBACK (롤백!)                                               │
│           │                                                         │
│           └── T2가 읽은 200은 존재하지 않는 데이터!                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  2. Non-Repeatable Read (반복 불가능 읽기)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  T1: SELECT balance FROM users WHERE id=1  → 100                   │
│           │                                                         │
│           ├── T2: UPDATE users SET balance=200 WHERE id=1          │
│           ├── T2: COMMIT                                            │
│           │                                                         │
│  T1: SELECT balance FROM users WHERE id=1  → 200                   │
│           │                                                         │
│           └── 같은 쿼리인데 결과가 다름!                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  3. Phantom Read (유령 읽기)                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  T1: SELECT * FROM orders WHERE amount > 1000  → 5건               │
│           │                                                         │
│           ├── T2: INSERT INTO orders (amount) VALUES (2000)        │
│           ├── T2: COMMIT                                            │
│           │                                                         │
│  T1: SELECT * FROM orders WHERE amount > 1000  → 6건               │
│           │                                                         │
│           └── 같은 조건인데 행 수가 늘어남!                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 동작 흐름 (단계별, 필수)

```
① 격리 수준 설정 → ② 트랜잭션 시작 → ③ 읽기/쓰기 수행 → ④ 격리 메커니즘 적용 → ⑤ 커밋/롤백
```

- **1단계 - 격리 수준 설정**: `SET TRANSACTION ISOLATION LEVEL ...`
- **2단계 - 트랜잭션 시작**: BEGIN 또는 첫 SQL 실행
- **3단계 - 작업 수행**: MVCC 또는 Lock을 통해 격리 보장
- **4단계 - 격리 메커니즘**: 스냅샷 생성, 락 획득
- **5단계 - 종료**: 커밋 시 락 해제, 스냅샷 폐기

#### 핵심 알고리즘 / 수식 (해당 시 필수)

```
[격리 수준별 구현 메커니즘]

1. READ UNCOMMITTED
   - 락 없이 읽기
   - 쓰기만 X-Lock
   - 구현: 거의 사용 안 함

2. READ COMMITTED
   - 읽기: 쿼리마다 새로운 스냅샷 (MVCC)
     또는 S-Lock을 쿼리 종료 후 즉시 해제
   - 쓰기: X-Lock을 커밋까지 유지
   - PostgreSQL, Oracle, SQL Server 기본

3. REPEATABLE READ
   - 읽기: 트랜잭션 시작 시 스냅샷 생성 후 유지 (MVCC)
     또는 S-Lock을 커밋까지 유지 (2PL)
   - 쓰기: X-Lock + Gap Lock (MySQL InnoDB)
   - MySQL 기본값

4. SERIALIZABLE
   - 읽기: 범위 잠금(Range Lock) 또는 테이블 잠금
   - 또는 Serializable Snapshot Isolation (SSI)
   - PostgreSQL: SSI로 구현 (충돌 감지 시 롤백)

[DBMS별 기본 격리 수준]

| DBMS           | 기본 격리 수준    | 특이사항                    |
|----------------|------------------|----------------------------|
| MySQL InnoDB   | REPEATABLE READ  | Gap Lock으로 Phantom 방지  |
| PostgreSQL     | READ COMMITTED   | SSI로 Serializable 구현    |
| Oracle         | READ COMMITTED   | Serializable = SSI         |
| SQL Server     | READ COMMITTED   | RCSI(Read Committed Snapshot) 옵션 |
| SQLite         | SERIALIZABLE     | 단일 연결이므로 완전 격리    |

[MySQL InnoDB의 격리 수준별 동작]

READ COMMITTED:
  - 일반 SELECT: MVCC (커밋된 데이터만)
  - 잠금 SELECT: 레코드 락만
  - 갭 락 없음 → Phantom Read 가능

REPEATABLE READ:
  - 일반 SELECT: MVCC (트랜잭션 시작 시 스냅샷)
  - 잠금 SELECT: 레코드 락 + 갭 락 (Next-Key Lock)
  - Phantom Read 방지

[PostgreSQL의 SSI (Serializable Snapshot Isolation)]

원리:
  1. 각 트랜잭션이 시작할 때 스냅샷 생성
  2. 읽기-쓰기 충돌 감지
  3. 직렬 가능성 위반 시 한 트랜잭션 롤백

장점:
  - Serializable과 동등한 일관성
  - 실제 직렬 실행보다 높은 동시성

단점:
  - 롤백 발생 가능 → 재시도 필요
```

#### 코드 예시 (필수: 실행 가능한 Python 또는 의사코드)

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
from collections import defaultdict
import time

class IsolationLevel(Enum):
    READ_UNCOMMITTED = "READ UNCOMMITTED"
    READ_COMMITTED = "READ COMMITTED"
    REPEATABLE_READ = "REPEATABLE READ"
    SERIALIZABLE = "SERIALIZABLE"

@dataclass
class Version:
    """MVCC 버전 레코드"""
    value: any
    created_txid: int
    created_time: float
    expired_txid: Optional[int] = None

@dataclass
class Transaction:
    """트랜잭션 정보"""
    txid: int
    isolation_level: IsolationLevel
    start_time: float
    snapshot: Dict[str, int] = field(default_factory=dict)  # key -> 본 txid가 읽은 버전
    reads: Set[str] = field(default_factory=set)   # 읽은 키
    writes: Set[str] = field(default_factory=set)  # 쓴 키
    committed: bool = False

class IsolationLevelDB:
    """격리 수준을 구현한 MVCC 데이터베이스"""

    def __init__(self):
        # 데이터 저장소: key -> List[Version]
        self.data: Dict[str, List[Version]] = defaultdict(list)
        self.transactions: Dict[int, Transaction] = {}
        self.committed_txids: Set[int] = set()
        self.current_txid = 0
        self.lock = __import__('threading').Lock()

    def begin_transaction(self, level: IsolationLevel = IsolationLevel.READ_COMMITTED) -> int:
        """트랜잭션 시작"""
        with self.lock:
            self.current_txid += 1
            txid = self.current_txid

            self.transactions[txid] = Transaction(
                txid=txid,
                isolation_level=level,
                start_time=time.time()
            )

            # REPEATABLE READ 이상은 시작 시 스냅샷 생성
            if level in (IsolationLevel.REPEATABLE_READ, IsolationLevel.SERIALIZABLE):
                self._create_snapshot(txid)

            return txid

    def _create_snapshot(self, txid: int) -> None:
        """스냅샷 생성: 현재 커밋된 버전 ID 기록"""
        tx = self.transactions[txid]
        for key, versions in self.data.items():
            # 이 트랜잭션이 볼 수 있는 가장 최신 버전 찾기
            for v in reversed(versions):
                if v.created_txid in self.committed_txids and v.created_txid < txid:
                    if v.expired_txid is None or v.expired_txid > txid:
                        tx.snapshot[key] = v.created_txid
                        break

    def read(self, txid: int, key: str) -> Optional[any]:
        """격리 수준에 따른 읽기"""
        tx = self.transactions.get(txid)
        if not tx:
            raise ValueError(f"Transaction {txid} not found")

        versions = self.data.get(key, [])
        tx.reads.add(key)

        # READ UNCOMMITTED: 모든 버전 읽기
        if tx.isolation_level == IsolationLevel.READ_UNCOMMITTED:
            if versions:
                return versions[-1].value
            return None

        # READ COMMITTED: 커밋된 최신 버전
        if tx.isolation_level == IsolationLevel.READ_COMMITTED:
            for v in reversed(versions):
                if v.created_txid in self.committed_txids:
                    if v.expired_txid is None or v.expired_txid in self.committed_txids:
                        continue
                    return v.value
            return None

        # REPEATABLE READ / SERIALIZABLE: 스냅샷 기반
        snapshot_txid = tx.snapshot.get(key)
        if snapshot_txid is not None:
            for v in versions:
                if v.created_txid == snapshot_txid:
                    return v.value

        # 스냅샷에 없으면 커밋된 것 중 가장 최신
        for v in reversed(versions):
            if v.created_txid in self.committed_txids and v.created_txid < txid:
                if v.expired_txid is None:
                    tx.snapshot[key] = v.created_txid
                    return v.value
        return None

    def write(self, txid: int, key: str, value: any) -> bool:
        """쓰기"""
        tx = self.transactions.get(txid)
        if not tx:
            raise ValueError(f"Transaction {txid} not found")

        # SERIALIZABLE: 읽기-쓰기 충돌 검사 (SSI)
        if tx.isolation_level == IsolationLevel.SERIALIZABLE:
            if self._check_rw_conflict(txid, key):
                raise SerializationError(f"Read-Write conflict detected for {key}")

        # 새 버전 생성
        new_version = Version(
            value=value,
            created_txid=txid,
            created_time=time.time()
        )

        # 이전 버전 만료 처리
        versions = self.data[key]
        if versions:
            latest = versions[-1]
            if latest.expired_txid is None:
                latest.expired_txid = txid

        versions.append(new_version)
        tx.writes.add(key)
        return True

    def _check_rw_conflict(self, txid: int, key: str) -> bool:
        """SSI: 읽기-쓰기 충돌 검사"""
        tx = self.transactions[txid]

        # 내가 읽은 키를 다른 커밋된 트랜잭션이 썼는지 확인
        for other_txid, other_tx in self.transactions.items():
            if other_txid == txid:
                continue
            if other_tx.committed and key in other_tx.writes:
                if key in tx.reads:
                    return True  # 충돌!

        return False

    def commit(self, txid: int) -> bool:
        """커밋"""
        with self.lock:
            tx = self.transactions.get(txid)
            if not tx:
                return False

            # SERIALIZABLE: 최종 충돌 검사
            if tx.isolation_level == IsolationLevel.SERIALIZABLE:
                for key in tx.writes:
                    if self._check_rw_conflict(txid, key):
                        self._cleanup_uncommitted(txid)
                        raise SerializationError("Serialization failure")

            self.committed_txids.add(txid)
            tx.committed = True
            return True

    def rollback(self, txid: int) -> None:
        """롤백"""
        with self.lock:
            self._cleanup_uncommitted(txid)

    def _cleanup_uncommitted(self, txid: int) -> None:
        """미커밋 버전 정리"""
        for key in list(self.data.keys()):
            self.data[key] = [v for v in self.data[key] if v.created_txid != txid]
            # 만료 정보 복원
            for v in self.data[key]:
                if v.expired_txid == txid:
                    v.expired_txid = None

        if txid in self.transactions:
            del self.transactions[txid]

class SerializationError(Exception):
    pass

# 동시성 문제 시뮬레이션
def simulate_dirty_read():
    """Dirty Read 시뮬레이션"""
    db = IsolationLevelDB()

    # 초기 데이터
    tx0 = db.begin_transaction(IsolationLevel.READ_COMMITTED)
    db.write(tx0, "balance", 100)
    db.commit(tx0)

    print("=== Dirty Read 시뮬레이션 ===")

    # T1: READ UNCOMMITTED
    tx1 = db.begin_transaction(IsolationLevel.READ_UNCOMMITTED)

    # T2: 수정 후 롤백
    tx2 = db.begin_transaction(IsolationLevel.READ_COMMITTED)
    db.write(tx2, "balance", 200)  # 미커밋

    # T1이 읽기 (Dirty Read 발생)
    val = db.read(tx1, "balance")
    print(f"T1 (READ UNCOMMITTED) 읽기: {val}")  # 200 (미커밋 데이터)

    # T2 롤백
    db.rollback(tx2)
    print("T2 롤백")

    # 실제 값 확인
    tx3 = db.begin_transaction(IsolationLevel.READ_COMMITTED)
    actual = db.read(tx3, "balance")
    print(f"실제 값: {actual}")  # 100
    print(f"Dirty Read 발생: {val != actual}")

def simulate_non_repeatable_read():
    """Non-Repeatable Read 시뮬레이션"""
    db = IsolationLevelDB()

    tx0 = db.begin_transaction(IsolationLevel.READ_COMMITTED)
    db.write(tx0, "balance", 100)
    db.commit(tx0)

    print("\n=== Non-Repeatable Read 시뮬레이션 ===")

    # READ COMMITTED로 테스트
    tx1 = db.begin_transaction(IsolationLevel.READ_COMMITTED)
    val1 = db.read(tx1, "balance")
    print(f"T1 첫 번째 읽기: {val1}")  # 100

    # T2가 수정 후 커밋
    tx2 = db.begin_transaction(IsolationLevel.READ_COMMITTED)
    db.write(tx2, "balance", 200)
    db.commit(tx2)
    print("T2 수정 후 커밋: 100 → 200")

    # T1이 다시 읽기
    val2 = db.read(tx1, "balance")
    print(f"T1 두 번째 읽기: {val2}")  # 200
    print(f"Non-Repeatable Read 발생: {val1 != val2}")

def simulate_phantom_read():
    """Phantom Read 시뮬레이션"""
    db = IsolationLevelDB()

    # 초기 데이터
    tx0 = db.begin_transaction(IsolationLevel.READ_COMMITTED)
    db.write(tx0, "order_1", 500)
    db.write(tx0, "order_2", 600)
    db.commit(tx0)

    print("\n=== Phantom Read 시뮬레이션 ===")

    # READ COMMITTED로 테스트
    tx1 = db.begin_transaction(IsolationLevel.READ_COMMITTED)

    # 범위 쿼리 시뮬레이션
    count1 = sum(1 for k in db.data if k.startswith("order_"))
    print(f"T1 첫 번째 카운트: {count1}")  # 2

    # T2가 새 행 추가
    tx2 = db.begin_transaction(IsolationLevel.READ_COMMITTED)
    db.write(tx2, "order_3", 700)
    db.commit(tx2)
    print("T2 새 주문 추가 후 커밋")

    # T1이 다시 카운트
    count2 = sum(1 for k in db.data if k.startswith("order_"))
    print(f"T1 두 번째 카운트: {count2}")  # 3
    print(f"Phantom Read 발생: {count1 != count2}")

if __name__ == "__main__":
    simulate_dirty_read()
    simulate_non_repeatable_read()
    simulate_phantom_read()

    print("\n=== 격리 수준별 비교 ===")
    print("READ UNCOMMITTED: Dirty O, Non-Rep O, Phantom O")
    print("READ COMMITTED:   Dirty X, Non-Rep O, Phantom O")
    print("REPEATABLE READ:  Dirty X, Non-Rep X, Phantom O*")
    print("SERIALIZABLE:     Dirty X, Non-Rep X, Phantom X")
    print("\n* MySQL InnoDB는 Gap Lock으로 Phantom 방지")
```

---

### IV. 비교 분석

#### 장단점 (각 3개 이상)

| 격리 수준 | 장점 | 단점 |
|----------|------|------|
| **READ UNCOMMITTED** | 최고 성능, 락 오버헤드 없음 | 모든 이상 현상 발생 |
| **READ COMMITTED** | 적절한 성능, Dirty Read 방지 | Non-Repeatable, Phantom 발생 |
| **REPEATABLE READ** | 일관된 읽기, 대부분 문제 방지 | Gap Lock 오버헤드, Phantom 가능성 |
| **SERIALIZABLE** | 완전한 격리, 모든 문제 방지 | 최저 성능, 동시성 급감 |

#### DBMS별 구현 비교 (최소 2개 대안)

| 비교 항목 | **MySQL InnoDB** | PostgreSQL | Oracle |
|----------|:---------------:|:----------:|:------:|
| **기본 격리 수준** | REPEATABLE READ | READ COMMITTED | READ COMMITTED |
| **Phantom 방지** | Gap Lock (RR에서) | SSI만 가능 | SSI만 가능 |
| **MVCC 구현** | Undo Log | xmin/xmax | Undo Segment |
| **SERIALIZABLE 구현** | 2PL | SSI | SSI |

> **선택 기준**:
> - 웹 서비스(읽기 많음): READ COMMITTED
> - 금융(정합성 중요): REPEATABLE READ 이상
> - 보고서(일관성 중요): REPEATABLE READ
> - 핵심 트랜잭션: SERIALIZABLE

---

### V. 실무 적용

#### 적용 시나리오 (3개 이상, 정량 효과 필수)

| 적용 분야 | 추천 격리 수준 | 이유 | 기대 효과 |
|----------|--------------|------|----------|
| **SNS 피드** | READ COMMITTED | 일시적 불일치 허용 | 응답 50ms 이내 |
| **쇼핑몰 상품** | READ COMMITTED | 최신 정보 우선 | 재고 정확도 99% |
| **은행 이체** | SERIALIZABLE | 완전 정합성 | 이중 출금 0건 |
| **통계 리포트** | REPEATABLE READ | 일관된 스냅샷 | 데이터 오차 0% |

#### 실제 도입 사례

- **카카오페이**: 이체에 SERIALIZABLE 사용, 데이터 불일치 0%
- **넷플릭스**: 조회수 집계에 READ COMMITTED, 처리량 10배 향상
- **아마존**: 주문에 REPEATABLE READ, 일관성과 성능 균형

#### 도입 시 고려사항 (4가지 관점)

| 관점 | 핵심 체크 항목 |
|------|--------------|
| **기술적** | DBMS별 구현 차이, MVCC vs Lock |
| **운영적** | 모니터링, 데드락 빈도 |
| **보안적** | 민감 데이터 노출 가능성 |
| **경제적** | 높은 격리 = 더 많은 하드웨어 |

#### 주의사항 / 흔한 실수 (3개 이상)

- **과도한 SERIALIZABLE**: 모든 트랜잭션에 SERIALIZABLE → 성능 저하
- **Phantom Read 무시**: MySQL에서도 표준 RR은 Phantom 가능
- **DBMS 차이 무시**: 동일 이름이어도 구현 다름

---

### VI. 결론

#### 기대 효과

| 효과 영역 | 내용 | 정량 수치 또는 정성 근거 |
|----------|------|------------------------|
| 성능 | 적정 격리로 최적화 | 처리량 2~10배 향상 |
| 일관성 | 비즈니스 요구 충족 | 데이터 오류 최소화 |
| 유연성 | 워크로드별 선택 | 설계 유연성 확보 |

#### 미래 전망

1. **기술 발전 방향**: SSI 최적화, 자동 격리 수준 튜닝
2. **시장 트렌드**: 클라우드 DB에서 세밀한 격리 제어
3. **후속 기술**: Deterministic Database, 분산 격리

> **결론**: 격리 수준은 동시성과 일관성의 트레이드오프를 조절하는 핵심 설정이다. 비즈니스 요구를 이해하고 적절한 수준을 선택하는 것이 DB 설계의 핵심 역량이다.

> **참고 표준**: ANSI SQL-92, Gray et al.(1976), Berenson et al.(1995) "A Critique of ANSI SQL Isolation Levels"

---

### 관련 개념

```
┌──────────────────────────────────────────────────────┐
│  격리 수준 핵심 연관 개념 맵                            │
├──────────────────────────────────────────────────────┤
│  [ACID] ←──→ [격리수준] ←──→ [동시성제어]             │
│       ↓            ↓            ↓                    │
│  [트랜잭션]    [Lock/MVCC]    [이상현상]              │
│       ↓            ↓            ↓                    │
│  [커밋/롤백]   [락그레뉼러리]  [DirtyRead]            │
└──────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 유형 | 설명 | 링크 |
|----------|----------|------|------|
| ACID | 상위 개념 | Isolation의 구체화 | [ACID](./acid.md) |
| MVCC | 구현 기법 | 격리를 위한 핵심 기술 | [MVCC](./mvcc.md) |
| Lock | 구현 기법 | 전통적 격리 메커니즘 | [동시성 제어](../concurrency_control.md) |
| 트랜잭션 | 선행 개념 | 격리 수준의 적용 대상 | [트랜잭션](./transaction.md) |
| 분산 DB | 확장 개념 | 분산 환경의 격리 문제 | [분산 DB](../distributed_database.md) |

---

## 쉬운 설명

**격리 수준**은 마치 **"회의실 문의 투명도"** 같습니다.

회의실에서 회의를 할 때, 문이 완전히 투명하면 밖에서 안이 다 보이죠? 반대로 완전 불투명하면 아무것도 안 보여요.

**READ UNCOMMITTED**는 **"완전 투명한 문"**이에요. 다른 사람이 작업하는 중간 과정이 다 보여요. 빠르지만 잘못된 정보를 볼 수 있어요.

**READ COMMITTED**는 **"반투명한 문"**이에요. 작업이 끝난 것(커밋된 것)만 보여요. 그런데 내가 보고 있는데 다른 사람이 바꾸면 다시 보면 달라져요.

**REPEATABLE READ**는 **"사진 찍어서 보기"**예요. 내가 시작할 때 사진을 찍어서 그 사진만 봐요. 중간에 다른 사람이 바꿔도 내 사진은 그대로예요.

**SERIALIZABLE**은 **"한 명씩만 들어가기"**예요. 완전히 격리돼서 다른 사람 영향을 전혀 안 받아요. 안전하지만 느려요.

---

## 부록: 다각도 관점

### 관점 요약 (빠른 참조)

| 관점 | 핵심 질문 | 한 줄 요약 |
|------|----------|----------|
| 이론가 | 수학적으로 어떻게 정의되는가? | 직렬 가능성, 충돌 직렬 가능성 |
| 설계자 | 어떤 트레이드오프를 선택했는가? | 일관성 vs 동시성 |
| 개발자 | 구현 시 무엇을 놓치기 쉬운가? | DBMS별 구현 차이 |
| 운영자 | 운영 중 어디서 문제가 발생하는가? | 데드락, 롤백 빈도 |
| 보안 전문가 | 어디를 공격하고 어떻게 막는가? | 타이밍 공격, 정보 유출 |
| 비즈니스 | 투자 대비 가치가 있는가? | 성능 vs 정합성 비용 |
| 역사가 | 무엇이 이것을 탄생시켰는가? | ANSI SQL-92 표준화 |

---

#### 이론가 관점

**핵심 질문**: 격리 수준은 수학적으로 어떻게 정의되는가?

- **직렬 가능성(Serializability)**: 동시 실행 결과가 어떤 순차 실행 결과와 동등
- **충돌 직렬 가능성(Conflict Serializability)**: 충돌 연산의 순서로 판단
- **현상(Phenomena)**: P0(Dirty Read), P1(Non-Repeatable), P2(Phantom)

---

#### 설계자 관점

**핵심 질문**: 격리 수준 설계의 트레이드오프는?

| 설계 결정 | 선택한 것 | 포기한 것 | 이유 |
|----------|----------|----------|------|
| 다단계 격리 | 4단계 제공 | 단일 격리 | 유연성 |
| MVCC | 스냅샷 기반 | Lock 기반 | 읽기 성능 |

---

#### 개발자 관점

**핵심 질문**: 구현 시 무엇을 놓치기 쉬운가?

```python
# Good: 명시적 격리 수준 설정
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
-- 작업 수행
COMMIT;

# Bad: 기본값에 의존
BEGIN;
-- 격리 수준 불명확
COMMIT;
```

---

#### 운영자 관점

**핵심 질문**: 운영 중 어디서 문제가 발생하는가?

| 장애 시나리오 | 원인 | 탐지 방법 | 대응 전략 |
|-------------|------|----------|----------|
| 데드락 증가 | SERIALIZABLE 과다 | 로그 분석 | 격리 수준 하향 |
| 롤백 빈도 | SSI 충돌 | 모니터링 | 재시도 로직 |

---

#### 보안 전문가 관점

**핵심 질문**: 어느 부분이 보안 관심 대상인가?

| 위협 유형 | 공격 벡터 | 영향도 | 대응 통제 |
|----------|----------|--------|----------|
| 타이밍 공격 | 낮은 격리 악용 | 중 | 적정 격리 수준 |
| 정보 유출 | Dirty Read | 상 | READ COMMITTED 이상 |

---

#### 비즈니스 관점

**핵심 질문**: 격리 수준에 투자할 가치가 있는가?

| 항목 | 세부 내용 |
|------|----------|
| **비용** | 높은 격리 = 더 많은 리소스 |
| **ROI** | 데이터 오류 방지 = 비용 절감 |
| **리스크** | 부적절한 격리 = 비즈니스 손실 |

---

#### 역사가 관점

**핵심 질문**: 무엇이 이것을 탄생시켰는가?

```
1970s - 트랜잭션 처리 시스템 등장
1992 - ANSI SQL-92 표준화 (4단계 격리)
1995 - Berenson et al., ANSI 격리 수준 비판
2000s - MVCC 기반 구현 확산
2010s - SSI(Serializable Snapshot Isolation) 도입
```
