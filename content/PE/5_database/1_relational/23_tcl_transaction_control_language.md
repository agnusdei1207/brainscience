+++
title = "TCL (Transaction Control Language) - 트랜잭션 제어 언어"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
+++

# TCL (Transaction Control Language) - 트랜잭션 제어 언어

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCL(Transaction Control Language)은 트랜잭션의 시작(BEGIN), 영구 반영(COMMIT), 취소(ROLLBACK), 중간 저장점(SAVEPOINT)을 제어하는 SQL 명령어로, DML 작업의 원자성(Atomicity)을 보장하는 핵심 메커니즘입니다.
> 2. **가치**: 적절한 TCL 사용은 데이터 무결성을 100% 보장하며, 부분 실패 시 선택적 복구를 통해 업무 연속성을 유지하고, 장애 발생 시 RTO(Recovery Time Objective)를 최소화합니다.
> 3. **융합**: TCL은 ACID의 원자성(A)과 영속성(D)을 구현하며, WAL(Write-Ahead Logging), 락킹(Locking), MVCC와 밀접하게 연동하여 일관된 트랜잭션 처리를 보장합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**TCL(Transaction Control Language)**은 데이터베이스 트랜잭션의 생명주기를 관리하는 SQL 명령어 집합입니다. DML(INSERT, UPDATE, DELETE)로 수행한 작업을 영구적으로 확정하거나 취소하는 역할을 합니다.

**TCL의 4대 핵심 명령어**:

| 명령어 | 기능 | 구문 | 상태 변화 |
|:---:|:---|:---|:---|
| **BEGIN** | 트랜잭션 시작 | BEGIN [WORK] [TRANSACTION] | Active |
| **COMMIT** | 영구 반영 | COMMIT [WORK] | Committed |
| **ROLLBACK** | 전체 취소 | ROLLBACK [WORK] | Aborted |
| **SAVEPOINT** | 중간 저장점 | SAVEPOINT 이름 | - |

**트랜잭션 상태 전이 다이어그램**:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                      트랜잭션 상태 전이 (State Transition)                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│                          BEGIN TRANSACTION                                 │
│                                │                                           │
│                                ▼                                           │
│    ┌────────────────────────────────────────────────────────────────┐     │
│    │                         ACTIVE                                  │     │
│    │                        (활동 상태)                              │     │
│    │                                                                 │     │
│    │  • SQL 문장 실행 중                                             │     │
│    │  • 데이터 읽기/쓰기 수행                                        │     │
│    │  • 락 획득 및 유지                                              │     │
│    └───────────────────────────┬────────────────────────────────────┘     │
│                                │                                           │
│              ┌─────────────────┴─────────────────┐                        │
│              │                                   │                        │
│              ▼                                   ▼                        │
│    ┌──────────────────┐              ┌──────────────────┐                 │
│    │ PARTIALLY        │              │     FAILED       │                 │
│    │ COMMITTED        │              │    (실패 상태)    │                 │
│    │ (부분 완료 상태)  │              │                  │                 │
│    │                  │              │  • 오류 발생     │                 │
│    │  • 마지막 SQL    │              │  • 무결성 위반   │                 │
│    │    실행 완료     │              │  • 데드락 감지   │                 │
│    │  • 커밋 대기     │              │                  │                 │
│    └────────┬─────────┘              └────────┬─────────┘                 │
│             │                                 │                           │
│             │ COMMIT                          │ ROLLBACK                  │
│             ▼                                 ▼                           │
│    ┌──────────────────┐              ┌──────────────────┐                 │
│    │    COMMITTED     │              │     ABORTED      │                 │
│    │   (완료 상태)     │              │   (철회 상태)    │                 │
│    │                  │              │                  │                 │
│    │  • 변경 사항     │              │  • 모든 변경     │                 │
│    │    영구 반영     │              │    취소됨        │                 │
│    │  • 락 해제       │              │  • 이전 상태     │                 │
│    │  • 리소스 정리   │              │    로 복구       │                 │
│    └──────────────────┘              └──────────────────┘                 │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

**TCL vs DML vs DDL 비교**:

| 구분 | DML | TCL | DDL |
|:---|:---|:---|:---|
| **역할** | 데이터 조작 | 트랜잭션 제어 | 구조 정의 |
| **명령어** | SELECT, INSERT, UPDATE, DELETE | COMMIT, ROLLBACK, SAVEPOINT | CREATE, ALTER, DROP |
| **트랜잭션 대상** | O | 제어자 | X (Auto Commit) |
| **롤백 가능** | COMMIT 전까지만 | COMMIT 후 불가 | X |
| **로그** | Undo + Redo | Commit Record | DDL 로그만 |

#### 2. 비유를 통한 이해

**"TCL은 온라인 쇼핑의 결제 프로세스"**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     [ 온라인 쇼핑 결제 비유 ]                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🛒 장바구니에 담기 = DML (INSERT, UPDATE, DELETE)                           │
│     → 아직 확정되지 않은 상태                                                │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  BEGIN TRANSACTION = 결제 시작 버튼 클릭                                 ││
│  │                                                                          ││
│  │  "지금부터 결제 프로세스를 시작합니다"                                   ││
│  │  → 장바구니 상태가 임시 보관됨                                           ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  SAVEPOINT = 결제 단계별 체크포인트                                      ││
│  │                                                                          ││
│  │  SAVEPOINT step1: 배송지 입력 완료                                       ││
│  │  SAVEPOINT step2: 결제 수단 선택 완료                                    ││
│  │  SAVEPOINT step3: 결제 승인 완료                                         ││
│  │                                                                          ││
│  │  → 문제 발생 시 해당 단계로 돌아갈 수 있음                               ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  COMMIT = "결제 완료" 버튼 클릭                                          ││
│  │                                                                          ││
│  │  "결제가 완료되었습니다. 주문이 확정됩니다."                             ││
│  │  → 재고 차감, 주문 생성, 결제 내역 저장                                  ││
│  │  → 모든 작업이 영구적으로 반영됨                                         ││
│  │  → 취소 불가 (별도의 취소 프로세스 필요)                                 ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  ROLLBACK = "취소" 버튼 클릭 또는 결제 실패                              ││
│  │                                                                          ││
│  │  "결제가 취소되었습니다. 장바구니로 돌아갑니다."                         ││
│  │  → 재고 차감 취소, 임시 주문 삭제                                        ││
│  │  → 모든 작업이 처음 상태로 복구됨                                        ││
│  │                                                                          ││
│  │  ROLLBACK TO SAVEPOINT step2:                                            ││
│  │  "결제 수단 선택 단계로 돌아갑니다"                                      ││
│  │  → step3(결제 승인)만 취소, step1,2는 유지                               ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 등장 배경 및 발전 과정

1. **기존 기술의 치명적 한계**:
   - 파일 시스템에서는 쓰기 작업이 즉시 반영되어 부분 실패 시 복구 불가
   - "은행 이체 중 전원 차단 → A 계좌만 차감되고 B 계좌는 입금 안 됨"
   - 데이터 무결성을 보장할 수 없음

2. **혁신적 패러다임의 도입**:
   - 1970년대 Jim Gray의 트랜잭션 개념 정립
   - ACID 특성과 함께 COMMIT/ROLLBACK 개념 확립
   - 1983년 SAVEPOINT 개념 도입 (부분 롤백 가능)
   - 현대 DBMS는 자동 커밋(Auto Commit) 모드와 명시적 트랜잭션 지원

3. **비즈니스적 요구사항**:
   - 금융 거래의 원자성 보장 ("All or Nothing")
   - 복잡한 비즈니스 프로세스의 부분 실패 대응
   - 장시간 실행 트랜잭션의 점진적 커밋 요구

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. TCL 명령어 상세 구성 요소 (표)

| 명령어 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비고 |
|:---|:---|:---|:---|:---|
| **BEGIN** | 트랜잭션 시작 | 트랜잭션 ID 할당, Undo 세그먼트 할당 | Savepoint | Oracle은 자동 시작 |
| **COMMIT** | 영구 반영 | Redo 로그 Flush, 락 해제, SCN 할당 | WAL, Fsync | 2단계 커밋 |
| **ROLLBACK** | 전체 취소 | Undo 로그 적용, 락 해제 | Undo Tablespace | Savepoint 지정 가능 |
| **SAVEPOINT** | 중간 저장점 | 현재 시점 마킹, 이름 부여 | Nested Transaction | Oracle, PostgreSQL |

#### 2. TCL 처리 아키텍처 다이어그램

```text
================================================================================
                    [ TCL Transaction Processing Architecture ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                      [ Transaction Lifecycle with TCL ]                      │
│                                                                              │
│  사용자 애플리케이션                                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │  BEGIN;                                              -- 트랜잭션 시작  │  │
│  │    │                                                                   │  │
│  │    ├─► INSERT INTO orders VALUES (...);                               │  │
│  │    │                                                                   │  │
│  │    ├─► SAVEPOINT after_order;           -- 저장점 생성                 │  │
│  │    │                                                                   │  │
│  │    ├─► INSERT INTO order_items VALUES (...);                          │  │
│  │    ├─► INSERT INTO order_items VALUES (...);                          │  │
│  │    │                                                                   │  │
│  │    ├─► SAVEPOINT after_items;           -- 저장점 생성                 │  │
│  │    │                                                                   │  │
│  │    ├─► UPDATE inventory SET stock = stock - 1;                        │  │
│  │    │   (오류 발생: 재고 부족!)                                         │  │
│  │    │                                                                   │  │
│  │    ├─► ROLLBACK TO after_items;         -- 부분 롤백                  │  │
│  │    │   (order_items 삽입으로 복구)                                     │  │
│  │    │                                                                   │  │
│  │    ├─► -- 대체 로직 수행                                               │  │
│  │    │   INSERT INTO backorders VALUES (...);                           │  │
│  │    │                                                                   │  │
│  │    └─► COMMIT;                          -- 트랜잭션 완료               │  │
│  │                                                                        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
                    [ Internal Mechanism: COMMIT ]
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  COMMIT;                                                                │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Phase 1: Prepare (준비 단계)                                           │
    │                                                                         │
    │  1. 트랜잭션 테이블에서 해당 트랜잭션 상태를 'Preparing'으로 변경       │
    │  2. 최종 Redo 레코드 생성 (Commit Record)                               │
    │  3. 모든 보류 중인 변경사항을 Redo Log Buffer에 기록                    │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Phase 2: Flush (플러시 단계) - 가장 중요!                               │
    │                                                                         │
    │  4. LGWR(Log Writer)가 Redo Log Buffer를                                │
    │     Redo Log File로 Flush (fsync)                                       │
    │  5. 디스크에 Commit Record가 기록될 때까지 대기                         │
    │  6. 이 시점이 바로 "Commit 완료" 시점                                   │
    │     → 영속성(Durability) 보장                                           │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Phase 3: Post-Commit (커밋 후 처리)                                     │
    │                                                                         │
    │  7. SCN(System Change Number) 할당                                      │
    │  8. 트랜잭션 테이블 상태를 'Committed'로 변경                            │
    │  9. 보유한 모든 Lock 해제                                               │
    │  10. 클라이언트에 "Commit complete" 응답                                │
    │  11. (비동기) DBWR가 Dirty Buffer를 Data File에 기록                    │
    └─────────────────────────────────────────────────────────────────────────┘

    ※ 중요: COMMIT은 Redo Log만 Flush, Data File은 비동기 기록
       → WAL(Write-Ahead Logging) 원칙

================================================================================
                    [ Internal Mechanism: ROLLBACK ]
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  ROLLBACK;                                                              │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Phase 1: Identify Undo Data (실행 취소 데이터 식별)                     │
    │                                                                         │
    │  1. Undo 세그먼트에서 해당 트랜잭션의 Undo 레코드 찾기                   │
    │  2. 가장 최근 변경부터 역순으로 정렬                                    │
    │  3. Undo 레코드 수만큼 반복 준비                                        │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Phase 2: Apply Undo (실행 취소 적용)                                    │
    │                                                                         │
    │  4. 각 Undo 레코드에 대해:                                              │
    │     a. 해당 데이터 블록을 버퍼 캐시로 로드                              │
    │     b. Undo 레코드의 이전 값으로 데이터 복구                            │
    │     c. 복구 작업에 대한 Redo 로그 생성                                  │
    │     d. 블록을 Dirty로 마킹                                              │
    │                                                                         │
    │  예시:                                                                  │
    │  - INSERT였으면 DELETE 수행                                             │
    │  - UPDATE였으면 이전 값으로 다시 UPDATE                                 │
    │  - DELETE였으면 INSERT 수행                                             │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Phase 3: Finalize (종료 처리)                                           │
    │                                                                         │
    │  5. 트랜잭션 테이블 상태를 'Aborted'로 변경                              │
    │  6. 보유한 모든 Lock 해제                                               │
    │  7. Undo 세그먼트 공간 반환                                             │
    │  8. 클라이언트에 "Rollback complete" 응답                               │
    └─────────────────────────────────────────────────────────────────────────┘

    ※ 주의: ROLLBACK은 COMMIT보다 비용이 높음
       → Undo 레코드 수만큼 실제 데이터 수정 필요

================================================================================
                    [ SAVEPOINT Mechanism ]
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  SAVEPOINT sp1;                                                         │
    │  ... DML 작업 ...                                                       │
    │  SAVEPOINT sp2;                                                         │
    │  ... DML 작업 ...                                                       │
    │  SAVEPOINT sp3;                                                         │
    │  ... DML 작업 (오류 발생) ...                                           │
    │  ROLLBACK TO sp2;  -- sp3 이후 작업만 취소                              │
    └─────────────────────────────────────────────────────────────────────────┘

    트랜잭션 타임라인:
    ────────────────────────────────────────────────────────────────────────▶

    BEGIN        sp1          sp2          sp3        Error    ROLLBACK TO sp2
      │           │            │            │           │            │
      ├───────────┼────────────┼────────────┼───────────┤            │
      │  유지     │   유지     │   유지     │  취소     │◀───────────┘
      │           │            │            │           │
      └───────────┴────────────┴────────────┴───────────┘
                          ↑
                    여기로 롤백

    세이브포인트 간 Undo 레코드 관리:
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │  Undo Segment:                                                          │
    │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
    │  │ Undo 1  │ │ Undo 2  │ │ Undo 3  │ │ Undo 4  │ │ Undo 5  │          │
    │  │ (sp1전) │ │ (sp1후) │ │ (sp2후) │ │ (sp3후) │ │ (Error) │          │
    │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
    │       │           │           │           │           │                │
    │       ▼           ▼           ▼           ▼           ▼                │
    │      유지        유지        유지       ROLLBACK    ROLLBACK           │
    │                              ◀─────────────────────────                │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
                    [ Auto Commit vs Explicit Transaction ]
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Auto Commit Mode (기본값)                                               │
    │                                                                         │
    │  각 SQL 문장이 자동으로 하나의 트랜잭션으로 처리                         │
    │                                                                         │
    │  INSERT INTO t1 VALUES (1);  -- 자동 COMMIT                             │
    │  INSERT INTO t2 VALUES (2);  -- 자동 COMMIT                             │
    │  UPDATE t3 SET x = 1;        -- 자동 COMMIT                             │
    │                                                                         │
    │  장점: 간편함                                                           │
    │  단점: 여러 문장을 묶어서 원자성 보장 불가                               │
    └─────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Explicit Transaction (명시적 트랜잭션)                                  │
    │                                                                         │
    │  BEGIN;                                                                 │
    │  INSERT INTO t1 VALUES (1);                                             │
    │  INSERT INTO t2 VALUES (2);                                             │
    │  UPDATE t3 SET x = 1;                                                   │
    │  COMMIT;  -- 또는 ROLLBACK;                                             │
    │                                                                         │
    │  장점: 여러 문장을 하나의 원자 단위로 처리                               │
    │  단점: 관리 필요                                                        │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
```

#### 3. 심층 동작 원리: 2단계 커밋 (Two-Phase Commit)

**분산 트랜잭션에서의 COMMIT**

```
분산 환경에서의 2PC (Two-Phase Commit)
─────────────────────────────────────────────────────────────────────────

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    Coordinator (코디네이터)                          │
    │                          (Transaction Manager)                       │
    └───────────────────────────────┬─────────────────────────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            v                       v                       v
    ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
    │  Participant  │       │  Participant  │       │  Participant  │
    │     (DB1)     │       │     (DB2)     │       │     (DB3)     │
    └───────────────┘       └───────────────┘       └───────────────┘

Phase 1: Prepare (준비 단계)
─────────────────────────────────────────────────────────────────────────
    Coordinator                        Participants
         │                                   │
         │──── PREPARE ─────────────────────▶│
         │                                   │
         │     (각 참여자는 트랜잭션을       │
         │      커밋할 준비가 되었는지       │
         │      확인하고 준비 상태로 대기)   │
         │                                   │
         │◀─── VOTE COMMIT (준비 완료) ─────│
         │◀─── VOTE COMMIT (준비 완료) ─────│
         │◀─── VOTE ABORT (준비 실패) ──────│
         │                                   │

Phase 2: Commit/Abort (확정 단계)
─────────────────────────────────────────────────────────────────────────

    [모든 참여자가 VOTE COMMIT인 경우]
         │                                   │
         │──── COMMIT ──────────────────────▶│
         │                                   │
         │     (모든 참여자가 실제 커밋 수행) │
         │                                   │
         │◀─── ACK ─────────────────────────│
         │◀─── ACK ─────────────────────────│

    [하나라도 VOTE ABORT인 경우]
         │                                   │
         │──── ABORT ───────────────────────▶│
         │                                   │
         │     (모든 참여자가 롤백 수행)      │
         │                                   │

2PC의 문제점:
- Blocking: 코디네이터 장애 시 참여자가 대기 상태로 봉쇄
- 단일 실패점: 코디네이터가 SPOF

3PC (Three-Phase Commit):
- PreCommit 단계 추가로 블로킹 문제 완화
```

#### 4. 실무 수준의 SQL 예시

```sql
-- ==============================================================================
-- TCL 실무 활용 예제: 주문 처리 시스템
-- ==============================================================================

-- [1] 기본 트랜잭션 패턴
-- ==============================================================================

-- 명시적 트랜잭션 시작
BEGIN TRANSACTION;
-- 또는
BEGIN;
-- 또는 (Oracle)
SET TRANSACTION NAME 'order_processing';

-- DML 작업 수행
INSERT INTO orders (order_id, customer_id, order_date, total_amount, status)
VALUES ('ORD-001', 'CUST-123', SYSDATE, 150000, 'PENDING');

INSERT INTO order_items (order_id, item_seq, product_id, quantity, unit_price)
VALUES ('ORD-001', 1, 'PROD-456', 2, 50000);

INSERT INTO order_items (order_id, item_seq, product_id, quantity, unit_price)
VALUES ('ORD-001', 2, 'PROD-789', 1, 50000);

-- 트랜잭션 완료
COMMIT;
-- 또는 문제 발생 시
-- ROLLBACK;

-- ==============================================================================
-- [2] SAVEPOINT 활용 패턴
-- ==============================================================================

BEGIN
    -- 주문 생성
    INSERT INTO orders (order_id, customer_id, order_date, status)
    VALUES ('ORD-002', 'CUST-456', SYSDATE, 'PENDING');

    SAVEPOINT order_created;

    -- 주문 상세 추가
    FOR i IN 1..10 LOOP
        BEGIN
            INSERT INTO order_items (order_id, item_seq, product_id, quantity)
            VALUES ('ORD-002', i, 'PROD-' || i, 1);

            -- 재고 확인
            SELECT stock_quantity INTO v_stock
            FROM inventory
            WHERE product_id = 'PROD-' || i;

            IF v_stock < 1 THEN
                -- 재고 부족 시 해당 아이템만 롤백
                ROLLBACK TO order_created;
                -- 대체 상품으로 변경
                INSERT INTO order_items (order_id, item_seq, product_id, quantity)
                VALUES ('ORD-002', i, 'PROD-ALT-' || i, 1);
            END IF;
        EXCEPTION
            WHEN OTHERS THEN
                ROLLBACK TO order_created;
                CONTINUE;
        END;
    END LOOP;

    SAVEPOINT items_created;

    -- 결제 처리
    BEGIN
        INSERT INTO payments (payment_id, order_id, amount, status)
        VALUES ('PAY-001', 'ORD-002', 150000, 'COMPLETED');
    EXCEPTION
        WHEN payment_error THEN
            ROLLBACK TO items_created;
            -- 주문은 유지하고 결제만 재시도
            INSERT INTO payment_pending (order_id, retry_count)
            VALUES ('ORD-002', 1);
    END;

    COMMIT;
END;
/

-- ==============================================================================
-- [3] 중첩 트랜잭션 패턴 (Nested Transaction)
-- ==============================================================================

-- PostgreSQL의 중첩 트랜잭션 (SAVEPOINT 활용)
BEGIN;

    INSERT INTO accounts (account_id, balance) VALUES ('A', 1000);
    SAVEPOINT sp1;

    INSERT INTO accounts (account_id, balance) VALUES ('B', 2000);
    SAVEPOINT sp2;

    INSERT INTO accounts (account_id, balance) VALUES ('C', 3000);

    -- sp2 이후만 롤백
    ROLLBACK TO sp2;
    -- C의 삽입만 취소됨

    -- 다시 시도
    INSERT INTO accounts (account_id, balance) VALUES ('C', 3500);

COMMIT;

-- ==============================================================================
-- [4] 읽기 전용 트랜잭션
-- ==============================================================================

-- 읽기 전용 트랜잭션 (성능 최적화)
SET TRANSACTION READ ONLY;

SELECT * FROM orders WHERE order_date >= SYSDATE - 7;
SELECT * FROM customers WHERE customer_id = 'CUST-123';

-- DML 시도 시 에러
-- UPDATE orders SET status = 'SHIPPED';  -- 에러!

COMMIT;

-- ==============================================================================
-- [5] 격리 수준 설정과 함께 사용
-- ==============================================================================

-- 트랜잭션 격리 수준 설정
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

BEGIN
    -- 높은 격리 수준에서의 작업
    SELECT SUM(balance) INTO v_total FROM accounts;

    -- 다른 트랜잭션의 변경과 격리됨

    UPDATE summary_table SET total_balance = v_total;
    COMMIT;
END;
/

-- ==============================================================================
-- [6] 자동 커밋 설정
-- ==============================================================================

-- MySQL
SET autocommit = 0;  -- 자동 커밋 비활성화
SET autocommit = 1;  -- 자동 커밋 활성화

-- PostgreSQL
-- psql에서 \set AUTOCOMMIT off

-- Oracle
-- 기본적으로 autocommit = off

-- ==============================================================================
-- [7] 트랜잭션 모니터링
-- ==============================================================================

-- 활성 트랜잭션 조회 (Oracle)
SELECT
    s.sid,
    s.serial#,
    s.username,
    s.status,
    t.start_time,
    t.used_urec AS undo_records,
    t.used_ublk AS undo_blocks,
    ROUND(t.used_ublk * 8 / 1024, 2) AS undo_mb,
    sq.sql_text
FROM v$session s
JOIN v$transaction t ON s.saddr = t.ses_addr
LEFT JOIN v$sql sq ON s.sql_id = sq.sql_id
WHERE s.username IS NOT NULL
ORDER BY t.start_time;

-- 세이브포인트 조회
SELECT * FROM user_savepoints;

-- 롱 러닝 트랜잭션 식별
SELECT
    sid,
    serial#,
    username,
    status,
    last_call_et AS seconds_since_last_activity,
    'Long Transaction' AS warning
FROM v$session
WHERE status = 'ACTIVE'
  AND last_call_et > 300  -- 5분 이상
  AND username IS NOT NULL;

-- ==============================================================================
-- [8] 예외 처리와 함께 사용
-- ==============================================================================

CREATE OR REPLACE PROCEDURE process_order(
    p_order_id IN VARCHAR2,
    p_customer_id IN VARCHAR2
) AS
    v_balance NUMBER;
    v_order_amount NUMBER;
    ex_insufficient_funds EXCEPTION;
BEGIN
    -- 트랜잭션 시작
    SAVEPOINT before_process;

    BEGIN
        -- 주문 금액 계산
        SELECT SUM(quantity * unit_price) INTO v_order_amount
        FROM cart_items
        WHERE customer_id = p_customer_id;

        -- 고객 잔액 확인
        SELECT balance INTO v_balance
        FROM customer_credits
        WHERE customer_id = p_customer_id;

        IF v_balance < v_order_amount THEN
            RAISE ex_insufficient_funds;
        END IF;

        -- 주문 생성
        INSERT INTO orders (order_id, customer_id, order_date, total_amount)
        VALUES (p_order_id, p_customer_id, SYSDATE, v_order_amount);

        -- 주문 상세 이동
        INSERT INTO order_items (order_id, item_seq, product_id, quantity, unit_price)
        SELECT p_order_id, rownum, product_id, quantity, unit_price
        FROM cart_items
        WHERE customer_id = p_customer_id;

        -- 장바구니 비우기
        DELETE FROM cart_items WHERE customer_id = p_customer_id;

        -- 잔액 차감
        UPDATE customer_credits
        SET balance = balance - v_order_amount
        WHERE customer_id = p_customer_id;

        -- 커밋
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('Order processed successfully');

    EXCEPTION
        WHEN ex_insufficient_funds THEN
            ROLLBACK TO before_process;
            -- 부분 주문으로 재시도 로직
            DBMS_OUTPUT.PUT_LINE('Insufficient funds, trying partial order');
            -- ...

        WHEN OTHERS THEN
            ROLLBACK;
            DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
            RAISE;
    END;

END;
/

-- ==============================================================================
-- [9] 배치 처리에서의 주기적 커밋
-- ==============================================================================

-- 대량 처리 시 주기적 커밋 (Undo 영역 폭주 방지)
DECLARE
    CURSOR c_large_data IS
        SELECT * FROM source_table
        WHERE processed_flag = 'N';

    v_count NUMBER := 0;
    v_batch_size NUMBER := 10000;
BEGIN
    FOR r IN c_large_data LOOP
        INSERT INTO target_table VALUES r;

        v_count := v_count + 1;

        -- 배치 사이즈마다 커밋
        IF MOD(v_count, v_batch_size) = 0 THEN
            COMMIT;
            DBMS_OUTPUT.PUT_LINE('Committed ' || v_count || ' records');
        END IF;
    END LOOP;

    -- 남은 레코드 커밋
    IF v_count > 0 THEN
        COMMIT;
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error at record ' || v_count || ': ' || SQLERRM);
        RAISE;
END;
/
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. TCL 명령어 비교

| 비교 항목 | COMMIT | ROLLBACK | ROLLBACK TO SAVEPOINT |
|:---|:---|:---|:---|
| **트랜잭션 종료** | O | O | X (계속 진행) |
| **데이터 반영** | 영구 반영 | 전체 취소 | 부분 취소 |
| **락 해제** | 전체 해제 | 전체 해제 | 일부 해제 |
| **Undo 사용** | 정리 | 적용 | 부분 적용 |
| **Redo 생성** | Commit Record | Undo Redo | Undo Redo |
| **성능 비용** | 낮음 | 높음 | 중간 |

#### 2. DBMS별 TCL 구현 차이

| 기능 | Oracle | PostgreSQL | MySQL | SQL Server |
|:---|:---|:---|:---|:---|
| **BEGIN** | 자동/SET TRANSACTION | BEGIN | START TRANSACTION | BEGIN TRANSACTION |
| **SAVEPOINT** | O | O | O | O |
| **중첩 트랜잭션** | Autonomous TX | SAVEPOINT로 대체 | X | O |
| **읽기 전용** | SET TRANSACTION READ ONLY | BEGIN READ ONLY | X | X |
| **2PC** | O | O | XA | O (MSDTC) |

#### 3. 과목 융합 관점 분석

**[ACID 융합] TCL과 ACID**
- 원자성(A): ROLLBACK으로 보장
- 일관성(C): 트랜잭션 경계 내 무결성 유지
- 격리성(I): 락킹과 함께 트랜잭션 격리
- 영속성(D): COMMIT + WAL로 보장

**[운영체제 융합] fsync와 COMMIT**
- COMMIT의 핵심은 Redo Log의 디스크 동기화
- OS fsync() 시스템 콜의 성능이 COMMIT 성능 결정

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

- **시나리오 1: 장시간 실행 트랜잭션**
  - 상황: 1시간 이상 실행되는 대용량 배치 작업
  - 판단:
    - Undo 영역 폭주 위험 → 주기적 커밋 필요
    - SAVEPOINT로 체크포인트 생성
    - 실패 시 마지막 SAVEPOINT부터 재시작

- **시나리오 2: 분산 트랜잭션**
  - 상황: 여러 DB에 걸친 트랜잭션
  - 판단:
    - 2PC로 원자성 보장
    - 코디네이터 장애 대비 타임아웃 설정
    - 또는 Saga 패턴으로 보상 트랜잭션 설계

- **시나리오 3: 교착 상태(Deadlock) 발생**
  - 상황: 데드락으로 인한 자동 ROLLBACK
  - 판단:
    - DBMS가 희생자 트랜잭션을 자동 ROLLBACK
    - 애플리케이션에서 재시도 로직 구현
    - 트랜잭션 범위 최소화로 데드락 확률 감소

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **트랜잭션 범위**: 최소 필수 작업만 포함
- [ ] **커밋 빈도**: Undo 영역 고려하여 적절한 커밋
- [ ] **예외 처리**: ROLLBACK 로직 명확히 정의
- [ ] **타임아웃**: 무한 대기 방지
- [ ] **감사**: 트랜잭션 시작/종료 로깅

#### 3. 안티패턴 (Anti-patterns)

- **커밋 누락**: BEGIN만 하고 COMMIT/ROLLBACK 없음
- **과도한 커밋**: 매 행마다 커밋 → 성능 저하
- **커밋 없는 롱 트랜잭션**: Undo 영역 폭주
- **자동 커밋 의존**: 명시적 트랜잭션 미사용
- **부분 롤백 오해**: ROLLBACK TO SAVEPOINT 후 COMMIT 누락

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 효과 영역 | 내용 | 정량적 지표 |
|:---|:---|:---|
| **무결성** | 원자성 보장 | 데이터 오류 0건 |
| **복구성** | 부분 실패 대응 | RTO 90% 단축 |
| **성능** | 적절한 커밋 전략 | Undo 사용량 50% 감소 |
| **안정성** | 일관된 상태 유지 | 장애 빈도 80% 감소 |

#### 2. 미래 전망

TCL은 **자동화와 분산 환경**으로 진화합니다:

1. **자동 트랜잭션 관리**: AI가 최적 커밋 시점 제안
2. **분산 트랜잭션 간소화**: Saga 패턴 자동화
3. **멀티 클라우드 트랜잭션**: 분산 2PC 최적화
4. **실시간 트랜잭션 분석**: 이상 징후 자동 탐지

#### 3. 참고 표준

- **ANSI/ISO SQL-92**: COMMIT/ROLLBACK 표준
- **X/Open XA**: 분산 트랜잭션 표준
- **ISO/IEC 9075**: SQL 트랜잭션 관리

---

### 관련 개념 맵 (Knowledge Graph)

- **[ACID](@/studynotes/5_database/1_relational/acid.md)**: TCL이 보장하는 트랜잭션 특성
- **[DML](@/studynotes/5_database/1_relational/21_dml_data_manipulation_language.md)**: TCL로 제어되는 데이터 조작
- **[WAL](@/studynotes/5_database/2_concurrency/recovery.md)**: COMMIT의 내부 메커니즘
- **[2PC](@/studynotes/5_database/2_concurrency/concurrency_control.md)**: 분산 트랜잭션의 커밋 프로토콜
- **[동시성 제어](@/studynotes/5_database/2_concurrency/concurrency_control.md)**: 락과 TCL의 연동

---

### 어린이를 위한 3줄 비유 설명

1. **게임 저장**: TCL은 비디오게임의 "저장" 버튼과 같아요. COMMIT은 저장, ROLLBACK은 다시 시작하는 거예요.

2. **세이브포인트**: 어려운 보스 전에 세이브포인트를 만들듯이, SAVEPOINT는 중간에 저장하는 거예요. 실패하면 그 지점부터 다시 시작!

3. **ALL or Nothing**: 한 번 COMMIT하면 모든 변경이 저장되고, ROLLBACK하면 모든 것이 처음으로 돌아가요. 반만 저장하는 건 없어요!
