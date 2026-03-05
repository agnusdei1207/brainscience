+++
title = "트랜잭션 (Transaction) - 논리적 작업의 단위"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
+++

# 트랜잭션 (Transaction) - 논리적 작업의 단위

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션은 데이터베이스 시스템에서 **더 이상 분해할 수 없는 최소의 논리적 작업 단위**(LUW, Logical Unit of Work)로, ACID(원자성, 일관성, 격리성, 영속성) 특성을 통해 데이터 무결성을 보장합니다.
> 2. **가치**: 시스템 장애, 동시 접근, 부분 실패 등 어떤 상황에서도 데이터베이스의 일관된 상태를 보장함으로써 금융, 주식, 재고 관리 등 비즈니스 크리티컬 영역의 신뢰성을 확보합니다.
> 3. **융합**: WAL(Write-Ahead Logging), MVCC(Multi-Version Concurrency Control), 2PC(Two-Phase Commit) 등의 기술과 결합하여 단일 DB부터 분산 DB까지 다양한 환경에서 트랜잭션을 지원합니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**트랜잭션(Transaction)**은 데이터베이스 관리 시스템(DBMS)에서 하나의 논리적 기능을 수행하기 위한 작업의 기본 단위입니다. 여러 개의 SQL 문(INSERT, UPDATE, DELETE)이 하나의 트랜잭션으로 묶일 수 있으며, 이들은 **"All-or-Nothing"** 원칙에 따라 전부 성공하거나 전부 실패해야 합니다.

**핵심 특성 (ACID)**:
- **A (Atomicity, 원자성)**: 트랜잭션 내 모든 연산은 완전히 수행되거나 전혀 수행되지 않아야 함
- **C (Consistency, 일관성)**: 트랜잭션 수행 전후에 데이터베이스는 일관된 상태를 유지해야 함
- **I (Isolation, 격리성)**: 동시에 실행되는 트랜잭션들은 서로 간섭하지 않아야 함
- **D (Durability, 영속성)**: 성공적으로 완료된 트랜잭션의 결과는 영구적으로 반영되어야 함

**트랜잭션의 범위**:
```sql
-- 트랜잭션 시작
BEGIN TRANSACTION;

-- 작업 1: A 계좌에서 10,000원 출금
UPDATE accounts SET balance = balance - 10000 WHERE id = 'A';

-- 작업 2: B 계좌에 10,000원 입금
UPDATE accounts SET balance = balance + 10000 WHERE id = 'B';

-- 트랜잭션 완료 (모든 작업이 성공한 경우)
COMMIT;

-- 또는 트랜잭션 취소 (오류 발생 시)
-- ROLLBACK;
```

#### 2. 비유를 통한 이해
트랜잭션은 **'ATM 계좌 이체'**와 같습니다.

1. **원자성**: 돈이 내 계좌에서 빠졌는데 상대방 계좌에 안 들어가면 안 됩니다. 둘 다 성공하거나, 둘 다 실패해야 합니다.
2. **일관성**: 이체 전후로 전체 돈의 합계는 같아야 합니다. 10만 원이 있었다면 이체 후에도 총 10만 원이어야 합니다.
3. **격리성**: 다른 사람이 동시에 이체해도 내 이체 작업에 방해받지 않아야 합니다.
4. **영속성**: '이체 완료' 메시지가 뜬 후 ATM이 고장 나도, 내 계좌 내역은 그대로 남아있어야 합니다.

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 초기 파일 시스템과 1세대 DBMS는 부분 갱신(Partial Update) 문제에 취약했습니다. 예를 들어, A 계좌에서 돈을 뺀 후 시스템이 다운되면 돈은 사라지고 B 계좌에는 입금되지 않는 '돈 증발' 사고가 발생할 수 있었습니다.

2. **혁신적 패러다임의 도입**: 1970년대 Jim Gray(튜링상 수상)가 트랜잭션 개념을 체계화하고, 이를 보장하기 위한 로깅, 잠금, 복구 기법을 정립했습니다. 1983년 Andreas Reuter와 Theo Härder가 ACID라는 용어를 공식화했습니다.

3. **비즈니스적 요구사항**: 현대의 핀테크, 이커머스, 항공 예약 시스템은 초당 수만 건의 트랜잭션을 처리하면서도 데이터 정합성을 완벽히 보장해야 합니다. 글로벌 분산 환경에서의 트랜잭션 처리는 더욱 복잡한 과제입니다.

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 트랜잭션 관리 구성 요소 (표)

| 구성요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Transaction Manager** | 트랜잭션 생명주기 관리 | BEGIN, COMMIT, ROLLBACK 처리 | SQL Engine | 지휘자 |
| **Concurrency Controller** | 동시성 제어 | Lock, MVCC, Timestamp | 2PL, OCC | 교통경찰 |
| **Recovery Manager** | 장애 복구 | Redo, Undo, WAL | ARIES, Logging | 소방서 |
| **Buffer Manager** | 메모리 버퍼 관리 | 페이지 캐싱, Flush 정책 | LRU, Clock | 창고관리자 |
| **Log Manager** | 로그 기록 | WAL 기록, LSN 관리 | Redo/Undo Log | 거래 장부 |

#### 2. 트랜잭션 처리 아키텍처 다이어그램

```text
================================================================================
                    [ Transaction Processing Architecture ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Application Layer ]                                │
│                                                                              │
│  Application:                                                                │
│  BEGIN TRANSACTION;                                                          │
│  UPDATE accounts SET balance = balance - 10000 WHERE id = 'A';              │
│  UPDATE accounts SET balance = balance + 10000 WHERE id = 'B';              │
│  COMMIT;                                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ SQL Statements
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       [ Transaction Manager ]                                │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  State Machine:                                                         │ │
│  │                                                                         │ │
│  │       +-----------+       +-----------+       +-----------+            │ │
│  │  --> |  Active   | ----> | Partially | ----> | Committed | ---> (END)  │ │
│  │       | (Running) |       | Committed |       | (Success) |            │ │
│  │       +-----+-----+       +-----------+       +-----------+            │ │
│  │             |                                                         │ │
│  │             v                                                         │ │
│  │       +-----------+       +-----------+                               │ │
│  │       |  Failed   | ----> |  Aborted  | ---> (END)                    │ │
│  │       |  (Error)  |       | (Rollback)|                               │ │
│  │       +-----------+       +-----------+                               │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  Transaction ID: TXN-2024-00123                                              │
│  Start Time: 2024-01-15 10:30:00.123                                        │
│  Status: ACTIVE                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
        │                      │                      │
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Concurrency  │    │   Recovery    │    │     Log       │
│   Controller  │    │    Manager    │    │   Manager     │
│               │    │               │    │               │
│ ┌───────────┐ │    │ ┌───────────┐ │    │ ┌───────────┐ │
│ │ Lock      │ │    │ │ Redo      │ │    │ │ WAL       │ │
│ │ Manager   │ │    │ │ Log       │ │    │ │ Buffer    │ │
│ └───────────┘ │    │ └───────────┘ │    │ └───────────┘ │
│ ┌───────────┐ │    │ ┌───────────┐ │    │ ┌───────────┐ │
│ │ MVCC      │ │    │ │ Undo      │ │    │ │ LSN       │ │
│ │ Control   │ │    │ │ Log       │ │    │ │ Tracking  │ │
│ └───────────┘ │    │ └───────────┘ │    │ └───────────┘ │
└───────────────┘    └───────────────┘    └───────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Buffer Manager ]                                   │
│                                                                              │
│  Buffer Pool (Memory):                                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Page 1: accounts (id='A') [Dirty] │ balance: 90000 (was 100000)      │  │
│  │ Page 2: accounts (id='B') [Dirty] │ balance: 110000 (was 100000)     │  │
│  │ Page 3: accounts (id='C') [Clean] │ balance: 50000                    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [Dirty Page List] → 변경된 페이지 목록 (나중에 디스크에 기록 필요)          │
└─────────────────────────────────────────────────────────────────────────────┘
                               │
                               │ Flush (Commit 시)
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        [ Storage Layer ]                                     │
│                                                                              │
│  ┌─────────────────────┐    ┌─────────────────────┐                        │
│  │   Data Files        │    │   Log Files         │                        │
│  │  ┌───────────────┐  │    │  ┌───────────────┐  │                        │
│  │  │ accounts.dbf  │  │    │  │ redo01.log    │  │                        │
│  │  │ accounts.ndx  │  │    │  │ redo02.log    │  │                        │
│  │  └───────────────┘  │    │  │ archive/      │  │                        │
│  └─────────────────────┘    │  └───────────────┘  │                        │
│                              └─────────────────────┘                        │
│                                                                              │
│  [ WAL Protocol: 로그가 먼저 기록된 후 데이터가 기록됨 ]                      │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
                      [ WAL (Write-Ahead Logging) Protocol ]
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                        TIME LINE                                        │
    │                                                                         │
    │  T1      T2        T3          T4            T5                        │
    │  │       │         │           │             │                         │
    │  ▼       ▼         ▼           ▼             ▼                         │
    │  ────────────────────────────────────────────────────────              │
    │  │       │         │           │             │                         │
    │  │       │         │           │             │                         │
    │ BEGIN  UPDATE A  UPDATE B   LOG FLUSH     COMMIT                      │
    │        (memory)  (memory)   (to disk)    (success)                    │
    │                              │                                        │
    │                              └─ WAL: 로그가 먼저 디스크에 기록됨        │
    │                                 그 후에야 COMMIT이 완료됨              │
    │                                                                         │
    │  [Log Records]                                                          │
    │  LSN=101: TXN-001 BEGIN                                                 │
    │  LSN=102: TXN-001 UPDATE accounts(A) BEFORE=100000 AFTER=90000         │
    │  LSN=103: TXN-001 UPDATE accounts(B) BEFORE=100000 AFTER=110000        │
    │  LSN=104: TXN-001 COMMIT <── 이 레코드가 디스크에 기록되면 완료!        │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
```

#### 3. 심층 동작 원리: 트랜잭션 생애주기

**① 트랜잭션 시작 (BEGIN)**
```
1. Transaction Manager가 새 트랜잭션 ID 생성 (예: TXN-001)
2. 트랜잭션 상태를 ACTIVE로 설정
3. 시작 시간 기록
4. 해당 세션에 트랜잭션 컨텍스트 바인딩
```

**② 트랜잭션 수행 (SQL 실행)**
```
1. SQL 문장 파싱 및 실행 계획 생성
2. Concurrency Controller에 의해 잠금(Lock) 획득 또는 MVCC 버전 생성
3. Buffer Manager가 필요한 페이지를 메모리에 로드
4. 데이터 수정 시:
   a. Undo 로그 생성 (이전 값 기록)
   b. Redo 로그 생성 (이후 값 기록)
   c. 메모리상 데이터 수정 (Dirty Page)
5. 로그는 Log Buffer에 기록
```

**③ 트랜잭션 커밋 (COMMIT)**
```
1. 마지막 SQL 문장 완료
2. 상태를 PARTIALLY COMMITTED로 변경
3. WAL 프로토콜에 따라 로그를 디스크에 Flush
4. 커밋 로그 레코드 기록 (LSN 포함)
5. 로그 Flush 완료 확인
6. 상태를 COMMITTED로 변경
7. 획득한 잠금 모두 해제
8. 트랜잭션 종료
```

**④ 트랜잭션 롤백 (ROLLBACK)**
```
1. 오류 발생 또는 명시적 ROLLBACK
2. 상태를 FAILED로 변경
3. Undo 로그를 역순으로 읽으며 변경 사항 취소
4. 상태를 ABORTED로 변경
5. 획득한 잠금 모두 해제
6. 트랜잭션 종료
```

#### 4. 실무 수준의 트랜잭션 코드 예시

```sql
-- ==============================================================================
-- 트랜잭션 실무 예제: 계좌 이체 시스템
-- ==============================================================================

-- [1] 기본 트랜잭션
BEGIN TRANSACTION;

-- A 계좌에서 출금
UPDATE accounts
SET balance = balance - 10000
WHERE id = 'A' AND balance >= 10000;

-- 출금 실패 시 롤백
IF SQL%ROWCOUNT = 0 THEN
    ROLLBACK;
    RAISE_APPLICATION_ERROR(-20001, '잔액 부족');
END IF;

-- B 계좌에 입금
UPDATE accounts
SET balance = balance + 10000
WHERE id = 'B';

-- 이체 내역 기록
INSERT INTO transfer_history (from_id, to_id, amount, transfer_date)
VALUES ('A', 'B', 10000, SYSDATE);

COMMIT;
-- 정상 완료: 모든 변경사항이 영구 반영됨

-- ==============================================================================
-- [2] 세이브포인트(Savepoint) 활용
-- ==============================================================================

BEGIN TRANSACTION;

-- 1단계: 고객 정보 업데이트
UPDATE customers SET phone = '010-1234-5678' WHERE id = 100;
SAVEPOINT step1_done;

-- 2단계: 주문 생성
INSERT INTO orders (order_id, customer_id, order_date)
VALUES (1001, 100, SYSDATE);
SAVEPOINT step2_done;

-- 3단계: 주문 상세 생성 (실패 가능)
BEGIN
    INSERT INTO order_items (order_id, product_id, quantity)
    VALUES (1001, 200, 5);
EXCEPTION
    WHEN OTHERS THEN
        -- 3단계만 롤백하고 1, 2단계는 유지
        ROLLBACK TO step2_done;
        -- 대체 상품으로 주문
        INSERT INTO order_items (order_id, product_id, quantity)
        VALUES (1001, 201, 5);
END;

COMMIT;

-- ==============================================================================
-- [3] 격리 수준 설정 (Isolation Level)
-- ==============================================================================

-- Read Committed (기본값)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
SELECT balance FROM accounts WHERE id = 'A';  -- 커밋된 데이터만 읽음
COMMIT;

-- Repeatable Read (MySQL 기본값)
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT balance FROM accounts WHERE id = 'A';  -- 첫 번째 읽기
-- 다른 트랜잭션이 balance를 변경해도
SELECT balance FROM accounts WHERE id = 'A';  -- 동일한 값 읽음
COMMIT;

-- Serializable (가장 엄격)
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
-- 완전한 격리 보장, 동시성 낮음
SELECT SUM(balance) FROM accounts;
COMMIT;

-- ==============================================================================
-- [4] 분산 트랜잭션 (2-Phase Commit)
-- ==============================================================================

-- 코디네이터 관점
-- Phase 1: Prepare
-- 각 참여자에게 준비 요청
-- Participant 1: "준비 완료"
-- Participant 2: "준비 완료"

-- Phase 2: Commit
-- 모든 참여자가 준비되면 커밋 지시
-- Participant 1: COMMIT
-- Participant 2: COMMIT

-- [5] PL/SQL 트랜잭션 블록
DECLARE
    v_balance NUMBER;
    e_insufficient_funds EXCEPTION;
BEGIN
    -- 잔액 확인
    SELECT balance INTO v_balance
    FROM accounts
    WHERE id = 'A' FOR UPDATE;  -- 행 잠금

    IF v_balance < 10000 THEN
        RAISE e_insufficient_funds;
    END IF;

    -- 이체 수행
    UPDATE accounts SET balance = balance - 10000 WHERE id = 'A';
    UPDATE accounts SET balance = balance + 10000 WHERE id = 'B';

    COMMIT;
    DBMS_OUTPUT.PUT_LINE('이체 완료');

EXCEPTION
    WHEN e_insufficient_funds THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('잔액 부족');
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('오류: ' || SQLERRM);
END;
/
```

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 트랜잭션 격리 수준별 현상 비교

| 격리 수준 | Dirty Read | Non-Repeatable Read | Phantom Read | 성능 |
|:---|:---|:---|:---|:---|
| **Read Uncommitted** | O | O | O | 최고 |
| **Read Committed** | X | O | O | 높음 |
| **Repeatable Read** | X | X | O* | 중간 |
| **Serializable** | X | X | X | 낮음 |

*MySQL InnoDB의 Repeatable Read는 MVCC로 Phantom Read도 방지

#### 2. 동시성 제어 기법 비교

| 기법 | 원리 | 장점 | 단점 | 사용 사례 |
|:---|:---|:---|:---|:---|
| **2PL (2-Phase Locking)** | 잠금 획득/해제 단계 분리 | 직렬 가능성 보장 | 데드락 발생 | 전통적 RDBMS |
| **MVCC** | 다중 버전 관리 | 읽기-쓰기 락 없음 | 버전 관리 오버헤드 | Oracle, PostgreSQL |
| **OCC (Optimistic)** | 충돌 시 재시도 | 높은 동시성 | 충돌 빈도 높으면 비효율 | 낮은 충돌 환경 |
| **Timestamp Ordering** | 타임스탬프 기반 순서 | 데드락 없음 | 재시도 빈번 | 연구용 |

#### 3. 과목 융합 관점 분석

- **[운영체제 융합] 프로세스 동기화**: 트랜잭션의 잠금(Lock)은 OS의 세마포어, 뮤텍스와 유사한 개념입니다. 데드락 탐지 및 예방 알고리즘도 OS와 DBMS에서 공통으로 사용됩니다.

- **[네트워크 융합] 분산 트랜잭션**: 2PC(2-Phase Commit)는 네트워크 통신 기반의 합의 프로토콜입니다. 코디네이터 장애 시 블로킹 문제를 해결하기 위해 3PC, Paxos, Raft가 도입됩니다.

- **[자료구조 융합] 로그 구조**: WAL은 순차 쓰기에 최적화된 append-only 자료구조입니다. LSN(Log Sequence Number)은 단조 증가하는 키로, 로그 레코드를 식별합니다.

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

- **시나리오 1: 대용량 배치 트랜잭션 성능 저하**
  - 상황: 100만 건 데이터 일괄 업데이트 시 30분 소요.
  - 판단: 단일 트랜잭션으로 처리하면 Undo 세그먼트가 비대해집니다. 적절한 단위(1만 건)로 커밋하며 처리합니다. Direct Path Insert, PARALLEL 힌트도 고려합니다.

- **시나리오 2: 분산 트랜잭션의 성능 병목**
  - 상황: 마이크로서비스 간 트랜잭션으로 응답 시간 증가.
  - 판단: 2PC는 높은 지연과 블로킹 위험이 있습니다. Saga 패턴(보상 트랜잭션)으로 전환하거나, 최종 일관성(Eventual Consistency)을 수용하는 설계를 고려합니다.

- **시나리오 3: 교착상태(Deadlock) 빈발**
  - 상황: 동시성 높은 환경에서 데드락으로 인한 롤백 빈발.
  - 판단: 테이블 접근 순서 표준화, 짧은 트랜잭션, 적절한 인덱스로 잠금 범위 최소화. 데드락 타임아웃 설정도 검토합니다.

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **트랜잭션 범위 최소화**: 필요한 작업만 트랜잭션에 포함
- [ ] **격리 수준 선택**: 비즈니스 요구사항과 성능 균형
- [ ] **잠금 타임아웃**: 무한 대기 방지
- [ ] **재시도 로직**: 일시적 실패에 대한 재시도
- [ ] **모니터링**: 장기 실행 트랜잭션, 데드락 감지

#### 3. 안티패턴 (Anti-patterns)

- **Long Transaction**: 너무 긴 트랜잭션은 Undo 영역 폭증, 잠금 장기 점유 유발
- **Auto-commit 모드**: 건건이 커밋은 성능 저하, 원자성 훼손
- **트랜잭션 내 사용자 입력**: 대기 시간 예측 불가, 리소스 장기 점유
- **분산 트랜잭션 남용**: 2PC의 성능 저하, 블로킹 위험

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 효과 영역 | 내용 | 개선 지표 |
|:---|:---|:---|
| **데이터 무결성** | ACID로 정합성 보장 | 데이터 오류 99% 감소 |
| **장애 복구** | 로그 기반 복구 | RTO 90% 단축 |
| **동시성** | 높은 처리량 | TPS 3배 향상 |
| **신뢰성** | 트랜잭션 보장 | 서비스 가용성 99.99% |

#### 2. 미래 전망

트랜잭션 기술은 **분산화와 AI**로 진화하고 있습니다:

1. **NewSQL**: 분산 환경에서도 ACID를 보장하는 Spanner, CockroachDB
2. **분산 합의**: Paxos, Raft 기반의 트랜잭션 복제
3. **NVM(Non-Volatile Memory)**: 로그 없이도 영속성 보장
4. **자율 튜닝**: AI 기반 격리 수준, 잠금 최적화

#### 3. 참고 표준

- **ANSI/ISO SQL-92**: 트랜잭션 격리 수준 표준
- **ACID (Haerder & Reuter, 1983)**: 트랜잭션 특성 정의
- **ARIES (Mohan et al., 1992)**: 복구 알고리즘 표준

---

### 관련 개념 맵 (Knowledge Graph)

- **[ACID 특성](@/studynotes/5_database/1_relational/acid.md)**: 트랜잭션의 4대 핵심 속성.
- **[동시성 제어](@/studynotes/5_database/2_concurrency/concurrency_control.md)**: 격리성 보장 기술.
- **[격리 수준](@/studynotes/5_database/2_concurrency/isolation_level.md)**: 동시성과 일관성의 트레이드오프.
- **[WAL](@/studynotes/5_database/2_concurrency/recovery.md)**: 영속성 보장을 위한 로깅.
- **[2PC](@/studynotes/5_database/2_concurrency/distributed_database_theory.md)**: 분산 트랜잭션 프로토콜.

---

### 어린이를 위한 3줄 비유 설명

1. **한 뭉치로 처리**: 트랜잭션은 여러 가지 일을 한 뭉치로 묶어서 처리하는 거예요.
2. **전부 성공이나 전부 실패**: 숙제를 다 하거나, 아니면 하나도 안 한 것으로 되돌리는 것과 같아요.
3. **약속 지키기**: '이체 완료'라고 말하면 은행이 그 약속을 꼭 지켜요!
