+++
title = "DML (Data Manipulation Language) - 데이터 조작 언어"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
+++

# DML (Data Manipulation Language) - 데이터 조작 언어

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DML(Data Manipulation Language)은 데이터베이스 내에 저장된 데이터를 조회(SELECT), 삽입(INSERT), 수정(UPDATE), 삭제(DELETE)하는 SQL 명령어 집합으로, 사용자와 DBMS 간의 데이터 상호작용을 위한 핵심 인터페이스입니다.
> 2. **가치**: 효율적인 DML 작성은 데이터 처리 성능을 10배~100배까지 차이를 만들며, 대량 데이터 처리 시 배치(Batch) 최적화로 트랜잭션 처리량(Throughput)을 극대화합니다.
> 3. **융합**: DML은 트랜잭션 관리(ACID), 동시성 제어(Locking), 옵티마이저(실행계획)와 밀접하게 연동하며, INSERT/UPDATE/DELETE는 로깅(WAL)과 복구 메커니즘을 트리거합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**DML(Data Manipulation Language)**은 관계형 데이터베이스에서 데이터를 조작(Manipulate)하기 위한 SQL 명령어의 하위 집합입니다. DDL(데이터 정의)과 DCL(데이터 제어)과 함께 SQL의 3대 구성 요소 중 하나입니다.

**DML의 4대 핵심 명령어 (CRUD)**:

| 명령어 | 분류 | 기능 | 비고 |
|:---:|:---:|:---|:---|
| **SELECT** | 조회(Read) | 데이터 검색 및 조회 | 가장 빈번하게 사용, Read-Only |
| **INSERT** | 생성(Create) | 새로운 데이터 행 추가 | 단일/다중 행 삽입 가능 |
| **UPDATE** | 수정(Update) | 기존 데이터 값 변경 | WHERE 절로 대상 행 지정 필수 |
| **DELETE** | 삭제(Delete) | 데이터 행 제거 | WHERE 절 생략 시 전체 삭제 |

**DML vs DDL vs DCL 비교**:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        SQL 명령어 계층 구조                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  DDL (Data Definition Language) - 데이터 정의                        │  │
│  │  CREATE, ALTER, DROP, TRUNCATE, RENAME                               │  │
│  │  → 스키마, 테이블, 인덱스 등 구조 정의                                │  │
│  │  → Auto Commit (암시적 커밋)                                         │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  DML (Data Manipulation Language) - 데이터 조작 ⭐                    │  │
│  │  SELECT, INSERT, UPDATE, DELETE, MERGE                               │  │
│  │  → 데이터 내용 조회 및 변경                                           │  │
│  │  → 명시적 Commit/Rollback 필요 (트랜잭션 제어)                        │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  DCL (Data Control Language) - 데이터 제어                           │  │
│  │  GRANT, REVOKE                                                       │  │
│  │  → 권한 부여 및 회수                                                  │  │
│  │  → Auto Commit (암시적 커밋)                                         │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  TCL (Transaction Control Language) - 트랜잭션 제어                  │  │
│  │  COMMIT, ROLLBACK, SAVEPOINT                                         │  │
│  │  → DML 작업의 영구 반영 또는 취소                                     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

#### 2. 비유를 통한 이해

**"DML은 도서관의 대출 시스템"**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     [ 도서관 비유로 이해하는 DML ]                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  📚 데이터베이스 = 도서관의 책장 (책들이 저장된 곳)                            │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  SELECT = 책 찾기/읽기                                                   ││
│  │  • "컴퓨터 과학 책 중 2020년 이후 발간된 책 목록을 보여줘"               ││
│  │  • 데이터를 훼손하지 않고 읽기만 함 (Read-Only)                          ││
│  │  • 여러 조건으로 검색 가능                                               ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  INSERT = 새 책 등록                                                     ││
│  │  • "새로 들어온 'AI 입문서'를 빈자리에 꽂아줘"                           ││
│  │  • 기존 책에 영향 없이 새로운 책 추가                                    ││
│  │  • 책장에 공간이 있어야 함                                               ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  UPDATE = 책 정보 수정                                                   ││
│  │  • "이 책의 저자명이 틀렸어, 올바르게 수정해줘"                          ││
│  │  • 기존 책의 내용을 변경                                                 ││
│  │  • 어떤 책인지 정확히 지정해야 함 (WHERE)                                ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  DELETE = 책 폐기                                                        ││
│  │  • "낡아서 못 쓰는 이 책을 치워줘"                                       ││
│  │  • 책장에서 완전히 제거                                                  ││
│  │  • 한 번 치우면 다시 찾을 수 없음 (복구 어려움)                          ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 등장 배경 및 발전 과정

1. **기존 기술의 치명적 한계**:
   - 초기 파일 시스템은 프로그래밍 언어(COBOL, Fortran)로 직접 데이터에 접근
   - 데이터 조작을 위해 복잡한 파일 I/O 코드를 작성해야 함
   - 데이터 무결성, 동시성 제어를 개발자가 직접 구현해야 했음

2. **혁신적 패러다임의 도입**:
   - 1970년 E.F. Codd의 관계형 모델 제안
   - 1974년 IBM의 System R에서 SEQUEL(Structured English Query Language) 개발 → SQL의 전신
   - SQL-86(1986): 최초의 ANSI SQL 표준, DML 포함
   - SQL-92(1992): 현대 SQL의 기반이 되는 표준 확립
   - SQL:1999, SQL:2003, SQL:2008, SQL:2011, SQL:2016: 윈도우 함수, MERGE, JSON 등 지속 확장

3. **비즈니스적 요구사항**:
   - 비전문가도 쉽게 데이터에 접근 가능한 언어 요구
   - 대량 데이터 처리를 위한 효율적인 명령어 필요
   - 트랜잭션 무결성을 보장하는 데이터 조작 방식 필요

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. DML 명령어 상세 구성 요소 (표)

| 명령어 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 롤백 가능 |
|:---|:---|:---|:---|:---:|
| **SELECT** | 데이터 조회 | 파싱 → 최적화 → 실행 → 결과 반환 | 인덱스, 조인, 파티션 프루닝 | N/A (Read) |
| **INSERT** | 데이터 삽입 | Redo/Undo 로그 생성 → 버퍼 캐시 수정 | Direct Path Insert, Bulk Bind | O |
| **UPDATE** | 데이터 수정 | 이전 값 Undo 로그 → 새 값 Redo 로그 | 인덱스 갱신, Row Migration | O |
| **DELETE** | 데이터 삭제 | Undo 로그로 삭제 전 값 저장 → Redo 로그 | 인덱스 삭제, Space 재사용 | O |
| **MERGE** | 조건부 삽입/수정 | Upsert (INSERT + UPDATE 결합) | ON CONFLICT, REPLACE INTO | O |

#### 2. DML 처리 아키텍처 다이어그램

```text
================================================================================
                    [ DML Processing Architecture ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Client Application ]                               │
│                                                                              │
│   SQL Statement: SELECT * FROM orders WHERE customer_id = 123               │
│   SQL Statement: INSERT INTO orders VALUES (...)                            │
│   SQL Statement: UPDATE orders SET status = 'SHIPPED' WHERE ...             │
│   SQL Statement: DELETE FROM orders WHERE order_id = 999                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ SQL Text
                                    v
┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Query Processing Pipeline ]                        │
│                                                                              │
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐                 │
│  │   Parser      │──▶│  Optimizer    │──▶│  Executor     │                 │
│  │   (파싱)      │   │  (최적화)      │   │  (실행)       │                 │
│  │               │   │               │   │               │                 │
│  │ • 구문 분석   │   │ • 실행계획    │   │ • 데이터 접근 │                 │
│  │ • 의미 분석   │   │ • 비용 계산   │   │ • 연산 수행   │                 │
│  │ • 파스 트리   │   │ • 규칙/비용   │   │ • 결과 반환   │                 │
│  └───────────────┘   └───────────────┘   └───────────────┘                 │
│         │                   │                   │                           │
│         │                   │                   │                           │
│         v                   v                   v                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Shared Pool (Memory)                              │   │
│  │  • Library Cache (SQL 커서, 실행계획 캐싱)                           │   │
│  │  • Data Dictionary Cache (메타데이터)                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
┌─────────────────────────────────────────────────────────────────────────────┐
│                      [ Buffer Cache & Logging ]                              │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Buffer Cache (SGA)                                  │  │
│  │                                                                        │  │
│  │    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                │  │
│  │    │ Block 1 │  │ Block 2 │  │ Block 3 │  │ Block N │                │  │
│  │    │ (Dirty) │  │ (Clean) │  │ (Dirty) │  │ (Clean) │                │  │
│  │    └─────────┘  └─────────┘  └─────────┘  └─────────┘                │  │
│  │                                                                        │  │
│  │    DML 작업 시:                                                        │  │
│  │    1. 데이터 블록를 버퍼로 로드                                        │  │
│  │    2. 버퍼 내에서 데이터 수정 (Dirty Mark)                             │  │
│  │    3. 변경 사항을 Redo Log Buffer에 기록                               │  │
│  │    4. Undo 데이터를 Undo Tablespace에 기록                             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐        │
│  │    Redo Log Buffer           │  │    Undo Tablespace           │        │
│  │    (변경 후 값)               │  │    (변경 전 값)               │        │
│  │                              │  │                              │        │
│  │  • 모든 DML 변경 기록        │  │  • 롤백을 위한 이전 값       │        │
│  │  • WAL (Write-Ahead Log)     │  │  • 읽기 일관성 (Read Consist │        │
│  │  • 장애 복구용               │  │  • MVCC 지원                 │        │
│  └──────────────────────────────┘  └──────────────────────────────┘        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ DBWR (Database Writer)
                                    │ LGWR (Log Writer)
                                    v
┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Physical Storage ]                                 │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Data Files                                          │  │
│  │  • 테이블 데이터 (Heap/Cluster/IOT)                                    │  │
│  │  • 인덱스 데이터 (B+Tree)                                              │  │
│  │  • LOB 데이터 (별도 세그먼트)                                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Redo Log Files                                      │  │
│  │  • 순환 로그 파일                                                      │  │
│  │  • 장애 시 복구에 사용                                                 │  │
│  │  • Archived Log (아카이브 모드 시)                                     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
                    [ DML Statement Lifecycle ]
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  INSERT INTO employees (id, name, dept) VALUES (100, 'Kim', 'Sales');   │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
    1. Parsing                          v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  • SQL 문법 검사                                                        │
    │  • 테이블/컬럼 존재 확인 (Data Dictionary)                              │
    │  • 권한 확인                                                            │
    │  • 파스 트리 생성                                                       │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
    2. Optimization                     v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  • 실행계획 생성                                                        │
    │  • 인덱스 사용 여부 결정                                                │
    │  • 통계 정보 기반 비용 계산                                             │
    │  • 실행계획 캐싱 (Soft Parse)                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
    3. Execution                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  • 트랜잭션 시작 (Active 상태)                                          │
    │  • Undo 세그먼트 할당 (롤백용)                                          │
    │  • 데이터 블록을 버퍼 캐시로 로드                                      │
    │  • Redo Log Buffer에 변경 기록                                         │
    │  • Undo Log에 이전 값 기록                                              │
    │  • 버퍼 캐시에서 데이터 수정 (Dirty Block)                              │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
    4. Commit                           v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  • SCN (System Change Number) 할당                                     │
    │  • Redo Log Buffer를 Redo Log File로 Flush (Force)                     │
    │  • 트랜잭션 완료 (Committed 상태)                                       │
    │  • 락 해제                                                              │
    │  • 사용자에게 'Commit complete' 반환                                   │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
    5. Post-Commit                      v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  • DBWR이 Dirty Block을 데이터 파일에 비동기 기록                       │
    │  • Undo 세그먼트 정리                                                   │
    │  • 관련 인덱스 갱신                                                     │
    │  • 통계 정보 갱신 (지연 가능)                                           │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
```

#### 3. 심층 동작 원리: 각 DML 명령어의 내부 처리

**SELECT 문 처리 과정**

```
1. 쿼리 파싱 (Query Parsing)
├── Lexical Analysis (어휘 분석): SQL 토큰화
├── Syntax Analysis (구문 분석): 문법 검사
├── Semantic Analysis (의미 분석): 객체 존재 및 권한 확인
└── Parse Tree 생성

2. 쿼리 최적화 (Query Optimization)
├── Query Rewrite (쿼리 변환)
│   ├── View Merging
│   ├── Subquery Unnesting
│   └── Predicate Pushdown
├── Access Path Selection (접근 경로 선택)
│   ├── Full Table Scan
│   ├── Index Range Scan
│   ├── Index Fast Full Scan
│   └── Index Skip Scan
├── Join Order & Method (조인 순서 및 방식)
│   ├── Nested Loops
│   ├── Hash Join
│   └── Sort Merge Join
└── Execution Plan 생성

3. 쿼리 실행 (Query Execution)
├── 데이터 블록 로드 (Buffer Cache)
├── 필터링 (WHERE 조건 적용)
├── 조인 수행
├── 정렬 (ORDER BY)
├── 그룹화 (GROUP BY)
└── 결과 집합 반환

4. 결과 반환 (Result Return)
├── ResultSet 생성
├── 네트워크 전송
└── 클라이언트 수신
```

**INSERT 문 처리 과정**

```
1. 사전 검증
├── 테이블 존재 및 INSERT 권한 확인
├── 컬럼 타입 호환성 검증
├── 제약조건(Constraint) 확인 준비
│   ├── NOT NULL
│   ├── PRIMARY KEY
│   ├── UNIQUE
│   ├── FOREIGN KEY
│   └── CHECK
└── 트리거(Trigger) 존재 확인

2. 공간 할당
├── Free List 검색 (여유 블록 탐색)
├── High Water Mark (HWM) 확장 필요 시
├── 새 익스텐트 할당 (필요 시)
└── 블록 내 행 슬롯 할당

3. 로깅 및 실행
├── Undo 레코드 생성 (롤백용)
├── Redo 레코드 생성 (복구용)
├── 버퍼 캐시에 행 삽입
├── 인덱스 갱신 (있는 경우)
│   ├── 각 인덱스에 새 엔트리 추가
│   └── 인덱스 분할(Split) 발생 가능
└── Lob 세그먼트 갱신 (LOB 컬럼 시)

4. 제약조건 검증
├── NOT NULL 체크
├── UNIQUE 체크 (인덱스 조회)
├── FOREIGN KEY 체크 (참조 무결성)
└── CHECK 제약 평가

5. 트리거 실행 (BEFORE/AFTER INSERT)
```

**UPDATE 문 처리 과정**

```
1. 대상 행 식별
├── WHERE 조건으로 검색
├── 행 잠금 (Row Lock / TX Lock)
├── 현재 값 읽기 (Consistent Read)
└── 갱신 가능 여부 확인

2. 변경 전 로깅 (Undo)
├── 변경 전 이미지 (Before Image) 저장
├── MVCC를 위한 과거 버전 생성
└── 롤백 세그먼트 기록

3. 변경 수행
├── Redo 로그 생성 (변경 후 값)
├── 버퍼 캐시에서 값 수정
├── Dirty Block 마킹
└── Row Migration 체크
    └── 행 크기 증가 시 다른 블록으로 이동

4. 인덱스 동기화
├── 인덱스 키 값 변경 시
│   ├── 기존 인덱스 엔트리 삭제
│   └── 새 인덱스 엔트리 삽입
└── 인덱스 분할/병합 가능

5. 제약조건 재검증
├── 변경된 컬럼의 UNIQUE 체크
├── 변경된 컬럼의 FK 체크
└── CHECK 제약 평가
```

**DELETE 문 처리 과정**

```
1. 대상 행 식별 및 잠금
├── WHERE 조건으로 검색
├── 행 배타 잠금 (X-Lock)
└── 자식 테이블 FK 참조 확인

2. 삭제 전 로깅 (Undo)
├── 삭제할 행의 전체 데이터 저장
├── RowID 기록
└── 롤백 시 복원 가능

3. 삭제 수행
├── Redo 로그 생성 (삭제 마크)
├── 버퍼 캐시에서 행 삭제 마킹
├── 블록 공간 통계 갱신
└── HWM 아래 공간으로 유지

4. 인덱스 정리
├── 모든 인덱스에서 해당 엔트리 삭제
├── 인덱스 블록 병합 가능
└── B+Tree 리프 노드 정리

5. 참조 무결성 처리
├── ON DELETE CASCADE: 자식 행도 삭제
├── ON DELETE SET NULL: 자식 FK를 NULL로
└── RESTRICT: 자식 참조 시 에러
```

#### 4. 실무 수준의 SQL 예시

```sql
-- ==============================================================================
-- DML 실무 활용 예제: 전자상거래 주문 시스템
-- ==============================================================================

-- [1] SELECT: 다양한 조회 패턴
-- ==============================================================================

-- 기본 조회
SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    status
FROM orders
WHERE order_date >= DATE '2026-01-01'
  AND status IN ('CONFIRMED', 'SHIPPED')
ORDER BY order_date DESC, order_id DESC
FETCH FIRST 100 ROWS ONLY;

-- 조인 조회 (고객 + 주문 + 주문상세)
SELECT
    c.customer_name,
    c.email,
    o.order_id,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS line_total
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date BETWEEN DATE '2026-01-01' AND DATE '2026-03-31'
  AND c.customer_grade = 'VIP'
ORDER BY o.order_date DESC, o.order_id, oi.item_seq;

-- 집계 조회 (월별 매출)
SELECT
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    COUNT(DISTINCT order_id) AS order_count,
    COUNT(DISTINCT customer_id) AS customer_count,
    SUM(total_amount) AS total_sales,
    AVG(total_amount) AS avg_order_value
FROM orders
WHERE order_date >= DATE '2025-01-01'
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
HAVING SUM(total_amount) > 10000000
ORDER BY month DESC;

-- 윈도우 함수 (누적 매출, 순위)
SELECT
    order_date,
    daily_sales,
    SUM(daily_sales) OVER (ORDER BY order_date) AS cumulative_sales,
    RANK() OVER (ORDER BY daily_sales DESC) AS sales_rank
FROM (
    SELECT
        order_date,
        SUM(total_amount) AS daily_sales
    FROM orders
    WHERE order_date >= DATE '2026-01-01'
    GROUP BY order_date
)
ORDER BY order_date;

-- ==============================================================================
-- [2] INSERT: 다양한 삽입 패턴
-- ==============================================================================

-- 단일 행 삽입
INSERT INTO customers (customer_id, customer_name, email, phone, grade)
VALUES ('C00123', '홍길동', 'hong@example.com', '010-1234-5678', 'NORMAL');

-- 다중 행 삽입 (Values List)
INSERT INTO order_items (order_id, item_seq, product_id, quantity, unit_price)
VALUES
    ('ORD001', 1, 'P1001', 2, 50000),
    ('ORD001', 2, 'P1002', 1, 120000),
    ('ORD001', 3, 'P1003', 5, 5000);

-- 서브쿼리를 이용한 삽입 (INSERT INTO ... SELECT)
INSERT INTO customer_summary (customer_id, total_orders, total_amount, last_order_date)
SELECT
    c.customer_id,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_amount,
    MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ON DUPLICATE KEY UPDATE
    total_orders = VALUES(total_orders),
    total_amount = VALUES(total_amount),
    last_order_date = VALUES(last_order_date);

-- 대량 데이터 직접 경로 삽입 (Direct Path Insert)
INSERT /*+ APPEND */ INTO orders_archive
SELECT * FROM orders
WHERE order_date < DATE '2025-01-01';

-- ==============================================================================
-- [3] UPDATE: 안전한 수정 패턴
-- ==============================================================================

-- 기본 UPDATE (반드시 WHERE 절 사용!)
UPDATE customers
SET
    grade = 'VIP',
    updated_at = SYSDATE,
    updated_by = USER
WHERE customer_id = 'C00123';

-- 서브쿼리를 이용한 UPDATE
UPDATE products p
SET
    stock_quantity = (
        SELECT COALESCE(SUM(s.quantity), 0)
        FROM stock_transactions s
        WHERE s.product_id = p.product_id
    ),
    last_stock_update = SYSDATE
WHERE p.category_id = 'ELECTRONICS';

-- CASE 문을 이용한 조건부 UPDATE
UPDATE orders
SET status = CASE
    WHEN status = 'PENDING' AND order_date < SYSDATE - 3 THEN 'CANCELLED'
    WHEN status = 'CONFIRMED' AND shipping_date IS NOT NULL THEN 'SHIPPED'
    WHEN status = 'SHIPPED' AND delivery_date IS NOT NULL THEN 'DELIVERED'
    ELSE status
END,
    updated_at = SYSDATE
WHERE status IN ('PENDING', 'CONFIRMED', 'SHIPPED');

-- UPDATE with JOIN (MySQL)
UPDATE orders o
JOIN customers c ON o.customer_id = c.customer_id
SET o.discount_rate = 0.1
WHERE c.grade = 'VIP' AND o.status = 'PENDING';

-- MERGE (UPSERT) - Oracle
MERGE INTO product_prices pp
USING (
    SELECT product_id, new_price
    FROM price_updates
    WHERE update_date = TRUNC(SYSDATE)
) pu
ON (pp.product_id = pu.product_id)
WHEN MATCHED THEN
    UPDATE SET
        pp.price = pu.new_price,
        pp.updated_at = SYSDATE
WHEN NOT MATCHED THEN
    INSERT (product_id, price, created_at)
    VALUES (pu.product_id, pu.new_price, SYSDATE);

-- ==============================================================================
-- [4] DELETE: 안전한 삭제 패턴
-- ==============================================================================

-- 기본 DELETE (반드시 WHERE 절 사용!)
DELETE FROM cart_items
WHERE cart_id = 'CART001' AND product_id = 'P1001';

-- 서브쿼리를 이용한 DELETE
DELETE FROM order_items
WHERE order_id IN (
    SELECT order_id
    FROM orders
    WHERE status = 'CANCELLED'
      AND order_date < SYSDATE - 30
);

-- EXISTS를 이용한 DELETE
DELETE FROM customer_temp t
WHERE EXISTS (
    SELECT 1
    FROM customers c
    WHERE c.customer_id = t.customer_id
);

-- 파티션 단위 삭제 (TRUNCATE 대안 - 로깅 가능)
DELETE FROM order_history
WHERE order_date < DATE '2020-01-01';

-- 대량 삭제 시 청크 단위 처리 (성능 최적화)
-- (실제로는 PL/SQL 또는 프로그램 루프로 처리)
DELETE FROM audit_logs
WHERE log_date < DATE '2023-01-01'
  AND ROWNUM <= 10000;  -- 1만 건씩 삭제

-- ==============================================================================
-- [5] 트랜잭션 제어와 함께 사용
-- ==============================================================================

-- 트랜잭션 시작
BEGIN TRANSACTION;

-- 주문 생성
INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
VALUES ('ORD-2026-001', 'C00123', SYSDATE, 'CONFIRMED', 250000);

-- 주문 상세 생성
INSERT INTO order_items (order_id, item_seq, product_id, quantity, unit_price)
VALUES ('ORD-2026-001', 1, 'P1001', 1, 150000);

INSERT INTO order_items (order_id, item_seq, product_id, quantity, unit_price)
VALUES ('ORD-2026-001', 2, 'P1002', 2, 50000);

-- 재고 차감
UPDATE products
SET stock_quantity = stock_quantity - 1
WHERE product_id = 'P1001';

UPDATE products
SET stock_quantity = stock_quantity - 2
WHERE product_id = 'P1002';

-- 세이브포인트 설정
SAVEPOINT after_order_created;

-- 결제 정보 생성
INSERT INTO payments (payment_id, order_id, amount, payment_method, status)
VALUES ('PAY-001', 'ORD-2026-001', 250000, 'CREDIT_CARD', 'COMPLETED');

-- 문제 발생 시 롤백
-- ROLLBACK TO after_order_created;

-- 정상 완료 시 커밋
COMMIT;

-- ==============================================================================
-- [6] DML 성능 최적화 팁
-- ==============================================================================

-- 대량 INSERT: 배치 처리
-- Java/Python에서 배치 사이즈 설정 (예: 1000건 단위)
/*
PreparedStatement pstmt = conn.prepareStatement(
    "INSERT INTO orders VALUES (?, ?, ?, ?)"
);
for (Order order : orders) {
    pstmt.setString(1, order.getId());
    pstmt.setString(2, order.getCustomerId());
    pstmt.setDate(3, order.getDate());
    pstmt.setBigDecimal(4, order.getAmount());
    pstmt.addBatch();

    if (++count % 1000 == 0) {
        pstmt.executeBatch();
    }
}
pstmt.executeBatch();
*/

-- 대량 UPDATE: 인덱스 활용
-- 비효율적: 풀 스캔 후 업데이트
UPDATE large_table SET column1 = 'value' WHERE status = 'OLD';

-- 효율적: 인덱스를 통한 범위 스캔 (status 컬럼에 인덱스 존재 시)
CREATE INDEX idx_large_table_status ON large_table(status);
UPDATE large_table SET column1 = 'value' WHERE status = 'OLD';

-- 대량 DELETE: 파티션 활용
-- 비효율적: DELETE로 행 단위 삭제
DELETE FROM logs WHERE log_date < '2023-01-01';

-- 효율적: 파티션 단위 삭제 (DROP PARTITION)
ALTER TABLE logs DROP PARTITION p2022_q4;
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. DML 명령어별 특성 비교

| 비교 항목 | SELECT | INSERT | UPDATE | DELETE |
|:---|:---:|:---:|:---:|:---:|
| **데이터 변경** | X (Read-Only) | O | O | O |
| **트랜잭션 대상** | X | O | O | O |
| **Undo 로그** | X | O | O | O |
| **Redo 로그** | X | O | O | O |
| **인덱스 영향** | 읽기만 | 추가 | 삭제+추가 | 삭제 |
| **락 유형** | S-Lock (공유) | X-Lock (배타) | X-Lock (배타) | X-Lock (배타) |
| **트리거 종류** | INSTEAD OF | BEFORE/AFTER | BEFORE/AFTER | BEFORE/AFTER |
| **WHERE 절** | 필수 아님 | 사용 불가 | 필수 권장 | 필수 권장 |

#### 2. DML vs DDL 비교

| 비교 항목 | DML | DDL |
|:---|:---|:---|
| **대상** | 데이터 (행) | 구조 (스키마) |
| **롤백 가능** | O (COMMIT 전) | X (자동 커밋) |
| **트랜잭션** | 트랜잭션의 대상 | 트랜잭션 종료 |
| **락** | 행/테이블 락 | DDL Lock (배타적) |
| **로그** | Redo + Undo | Redo만 |
| **캐시 영향** | 버퍼 캐시 | 라이브러리 캐시 무효화 |

#### 3. 과목 융합 관점 분석

**[트랜잭션 융합] ACID와 DML**
- DML(INSERT/UPDATE/DELETE)은 ACID 트랜잭션의 대상
- 원자성: DML들은 All-or-Nothing 단위로 처리
- 격리성: 동시 DML 수행 시 락킹 또는 MVCC로 격리 보장

**[옵티마이저 융합] 실행계획과 DML**
- SELECT: 가장 복잡한 최적화 대상
- INSERT: 인덱스 유지보수 비용 계산
- UPDATE: 행 이동(Migration) 가능성 고려
- DELETE: 인덱스 삭제 비용, 공간 재사용

**[보안 융합] DML과 접근 통제**
- SELECT: 읽기 권한 필요
- INSERT/UPDATE/DELETE: 쓰기 권한 필요
- 뷰(View)를 통한 DML 제한 가능 (WITH CHECK OPTION)

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

- **시나리오 1: 대량 데이터 삭제 성능 문제**
  - 상황: 1억 건의 로그 데이터를 DELETE로 삭제 시 성능 저하
  - 판단:
    - 단순 DELETE는 모든 행에 Undo/Redo 로그 생성 → 비효율
    - 대안 1: TRUNCATE (롤백 불가, DDL)
    - 대안 2: 파티션 DROP (순간 삭제)
    - 대안 3: 청크 단위 DELETE + COMMIT 반복

- **시나리오 2: 동시 UPDATE로 인한 락 경합**
  - 상황: 인기 상품의 재고 차감 시 락 대기 증가
  - 판단:
    - 행 단위 락으로 인한 직렬화
    - 대안 1: Redis로 선점 처리 후 비동기 DB 반영
    - 대안 2: 낙관적 락(Optimistic Lock) + 재시도
    - 대안 3: 채번 방식으로 분산 (상품별 재고를 여러 행으로 분산)

- **시나리오 3: SELECT 성능 저하**
  - 상황: 복잡한 조인 쿼리의 응답 시간 증가
  - 판단:
    - 실행계획 분석으로 병목 지점 식별
    - 인덱스 추가, 조인 순서 변경, 서브쿼리 → 조인 변환
    - 최종적으로는 반정규화 또는 Materialized View 고려

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **WHERE 절 필수**: UPDATE/DELETE 시 WHERE 절 누락 방지
- [ ] **트랜잭션 범위**: DML 작업 단위 최적화
- [ ] **배치 처리**: 대량 DML은 배치 단위로 분할
- [ ] **인덱스 영향**: DML 시 인덱스 유지보수 비용 고려
- [ ] **트리거 검토**: DML 트리거로 인한 성능 영향 확인
- [ ] **제약조건**: FK, CHECK 제약으로 인한 성능 저하 검토

#### 3. 안티패턴 (Anti-patterns)

- **WHERE 없는 UPDATE/DELETE**: 전체 테이블 수정/삭제
- **무한 루프 DML**: 트리거 내에서 자기 테이블 DML
- **과도한 커밋**: 매 행마다 커밋 → 성능 저하
- **드라이빙 테이블 오류**: 대량 테이블을 선행으로 조인
- **함수 인덱스 무시**: 컬럼에 함수 적용 시 인덱스 미사용

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 효과 영역 | 내용 | 정량적 지표 |
|:---|:---|:---|
| **성능** | 최적화된 DML 작성 | 쿼리 응답 시간 50~90% 개선 |
| **안정성** | 트랜잭션 무결성 | 데이터 정합성 100% |
| **생산성** | 표준화된 DML 패턴 | 개발 시간 30% 단축 |
| **확장성** | 배치 처리 최적화 | 처리량 10배 향상 |

#### 2. 미래 전망

DML은 **AI와 자동화**로 진화합니다:

1. **자동 SQL 튜닝**: AI가 비효율적 DML을 자동 최적화
2. **자연어 to SQL**: 자연어 질문을 DML로 자동 변환
3. **실시간 스트림 DML**: INSERT만으로 실시간 분석
4. **선형적 확장**: 분산 DB에서 DML의 수평 확장

#### 3. 참고 표준

- **ANSI/ISO SQL-92/99/2003**: DML 표준 문법
- **SQL:2016**: JSON DML 지원
- **ISO/IEC 9075**: SQL 표준 규격

---

### 관련 개념 맵 (Knowledge Graph)

- **[DDL (Data Definition Language)](@/studynotes/5_database/1_relational/18_ddl_dml_dcl_tcl.md)**: DML과 함께 SQL의 핵심 구성 요소
- **[트랜잭션 ACID](@/studynotes/5_database/1_relational/acid.md)**: DML이 보장해야 하는 트랜잭션 특성
- **[옵티마이저](@/studynotes/5_database/_keyword_list.md)**: DML 실행계획 생성
- **[동시성 제어](@/studynotes/5_database/2_concurrency/concurrency_control.md)**: 동시 DML 수행 시 격리 보장
- **[인덱스](@/studynotes/5_database/1_relational/b_tree_index.md)**: DML 성능에 영향을 미치는 핵심 구조

---

### 어린이를 위한 3줄 비유 설명

1. **책장에서 책 찾기 (SELECT)**: 도서관에서 내가 읽고 싶은 책을 찾아서 읽는 것과 같아요. 책에는 아무런 해를 끼치지 않아요.

2. **새 책 꽂기 (INSERT)**: 도서관에 새로 들어온 책을 빈자리에 꽂는 것이에요. 다른 책들을 건드리지 않고 새 책만 추가해요.

3. **책 정보 수정하고 치우기 (UPDATE/DELETE)**: 책의 제목이 틀렸으면 바로잡고(UPDATE), 너무 낡은 책은 치워버리는(DELETTE) 것과 같아요.
