+++
title = "DBMS 언어 체계 (DDL/DML/DCL/TCL)"
description = "데이터 정의어, 조작어, 제어어, 트랜잭션 제어어의 완전한 이해"
date = "2026-03-05"
[taxonomies]
tags = ["database", "ddl", "dml", "dcl", "tcl", "sql"]
categories = ["studynotes-5_database"]
+++

# 18. DBMS 언어 체계 (DDL / DML / DCL / TCL)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DBMS 언어는 데이터 정의(DDL), 데이터 조작(DML), 데이터 제어(DCL), 트랜잭션 제어(TCL)의 4대 카테고리로 구성되며, 이는 ANSI/ISO SQL 표준의 기본 구조입니다.
> 2. **가치**: DDL은 스키마 관리, DML은 CRUD 연산, DCL은 보안/권한, TCL은 트랜잭션 무결성을 담당하여 데이터베이스의 전 수명주기를 관리합니다.
> 3. **융합**: 현대 ORM, Migration Tool(Flyway, Liquibase), 데이터 거버넌스 도구는 이 4대 언어 체계를 추상화하여 제공합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**DBMS 언어 체계**는 데이터베이스 시스템과 상호작용하기 위한 명령어들의 분류 체계입니다. ANSI/ISO SQL 표준은 데이터베이스 언어를 다음 4가지로 분류합니다:

| 언어 분류 | 정의 | 주요 명령어 | 대상 |
|:---|:---|:---|:---|
| **DDL (Data Definition Language)** | 데이터 정의 언어 | CREATE, ALTER, DROP, TRUNCATE | 스키마, 구조 |
| **DML (Data Manipulation Language)** | 데이터 조작 언어 | SELECT, INSERT, UPDATE, DELETE | 데이터 |
| **DCL (Data Control Language)** | 데이터 제어 언어 | GRANT, REVOKE | 권한, 보안 |
| **TCL (Transaction Control Language)** | 트랜잭션 제어 언어 | COMMIT, ROLLBACK, SAVEPOINT | 트랜잭션 |

**상세 정의**:

1. **DDL (데이터 정의어)**
   - 데이터베이스 구조(스키마)를 정의, 수정, 삭제
   - 메타데이터(Data Dictionary)에 영향
   - **Auto Commit** (명시적 커밋 없이 즉시 반영)
   - DDL 로그가 별도 관리됨

2. **DML (데이터 조작어)**
   - 데이터의 CRUD (Create, Read, Update, Delete) 연산
   - 트랜잭션의 대상 (COMMIT/ROLLBACK 가능)
   - 가장 빈번하게 사용되는 SQL

3. **DCL (데이터 제어어)**
   - 데이터베이스 객체에 대한 접근 권한 관리
   - 보안 정책의 핵심
   - 권한 부여(GRANT)와 취소(REVOKE)

4. **TCL (트랜잭션 제어어)**
   - 논리적 작업 단위(트랜잭션)의 완료/취소
   - ACID 특성 보장의 핵심
   - DML 연산과 밀접하게 연동

#### 2. 💡 비유를 통한 이해

**도서관 관리 시스템**으로 비유할 수 있습니다:

| 언어 | 도서관 비유 | 예시 |
|:---|:---|:---|
| **DDL** | 도서관 건축/리모델링 | "책장을 설치하다", "열람실을 확장하다", "책장을 철거하다" |
| **DML** | 책 대출/반납/조회 | "책을 대출하다", "책을 반납하다", "책을 찾다" |
| **DCL** | 출입 권한 관리 | "회원에게 열람증을 발급하다", "회원의 권한을 정지하다" |
| **TCL** | 대출 기록 확정/취소 | "대출을 확정하다", "대출을 취소하다", "중간 저장점" |

**자동차로 비유**:
- **DDL**: 자동차 설계 변경 (새 모델 출시, 부품 교체)
- **DML**: 운전 (시동, 주행, 정지)
- **DCL**: 열쇠 권한 (운전 허용/금지)
- **TCL**: 주행 기록 저장/취소

#### 3. 등장 배경 및 발전 과정

**1단계: 초기 파일 시스템 (1960년대 이전)**
- 프로그램과 데이터가 혼재
- 데이터 정의가 코드에 하드코딩
- 권한 관리 없음

**2단계: DBMS 등장과 언어 분리 (1970년대)**
- IBM IMS: DL/1 (Data Language/1)
- DDL과 DML의 개념적 분리
- 전용 언어로 인한 학습 곡선

**3단계: SQL 표준화 (1980년대)**
- 1986년: ANSI SQL-86 표준
- DDL, DML, DCL 통합 문법
- 선언적 언어로의 전환

**4단계: 현대적 확장 (1990년대~현재)**
- TCL의 공식화
- PL/SQL, T-SQL 등 절차적 확장
- ORM, Migration Tool의 추상화

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. DBMS 언어 체계 상세 (표)

| 언어 | 명령어 | 기능 | 실행 시점 | 롤백 가능 | 권한 |
|:---|:---|:---|:---|:---|:---|
| **DDL** | CREATE | 객체 생성 | 즉시 | 불가* | CREATE ANY |
| | ALTER | 객체 수정 | 즉시 | 불가* | ALTER ANY |
| | DROP | 객체 삭제 | 즉시 | 불가* | DROP ANY |
| | TRUNCATE | 데이터 전체 삭제 | 즉시 | 불가* | DELETE |
| **DML** | SELECT | 데이터 조회 | TCL 시 | 해당없음 | SELECT |
| | INSERT | 데이터 삽입 | TCL 시 | 가능 | INSERT |
| | UPDATE | 데이터 수정 | TCL 시 | 가능 | UPDATE |
| | DELETE | 데이터 삭제 | TCL 시 | 가능 | DELETE |
| | MERGE | 삽입+수정 통합 | TCL 시 | 가능 | INSERT, UPDATE |
| **DCL** | GRANT | 권한 부여 | 즉시 | 불가 | GRANT OPTION |
| | REVOKE | 권한 회수 | 즉시 | 불가 | GRANT OPTION |
| **TCL** | COMMIT | 트랜잭션 확정 | 즉시 | 불가 | - |
| | ROLLBACK | 트랜잭션 취소 | 즉시 | - | - |
| | SAVEPOINT | 저장점 설정 | 즉시 | 부분 | - |

*참고: Oracle FLASHBACK, SQL Server SNAPSHOT 등 일부 복구 가능

#### 2. DBMS 언어 처리 아키텍처 다이어그램

```text
+============================================================================+
|                         SQL LANGUAGE PROCESSING                             |
+============================================================================+
|                                                                             |
|  [사용자]                                                                   |
|     |                                                                       |
|     v                                                                       |
|  +---------------------------------------------------------------------+   |
|  |                    SQL STATEMENT CLASSIFIER                          |   |
|  |  +---------+  +---------+  +---------+  +---------+                  |   |
|  |  |   DDL   |  |   DML   |  |   DCL   |  |   TCL   |                  |   |
|  |  +----+----+  +----+----+  +----+----+  +----+----+                  |   |
|  +-------|----------|----------|----------|-----------------------------+   |
|          |          |          |          |                                 |
|          v          v          v          v                                 |
|  +---------------------------------------------------------------------+   |
|  |                        PARSER & AUTHORIZER                           |   |
|  |  +----------------+  +----------------+  +----------------+         |   |
|  |  | Syntax Check   |  | Semantic Check |  | Privilege Check|         |   |
|  |  +----------------+  +----------------+  +----------------+         |   |
|  +---------------------------------------------------------------------+   |
|          |          |          |          |                                 |
|          v          v          v          v                                 |
|  +---------------------------------------------------------------------+   |
|  |                          EXECUTOR                                    |   |
|  |                                                                      |   |
|  |  [DDL Path]              [DML Path]            [DCL Path]           |   |
|  |  +---------------+       +---------------+      +---------------+    |   |
|  |  | Data Dict     |       | Optimizer     |      | Privilege     |    |   |
|  |  | Update        |       | (Cost-based)  |      | Table Update  |    |   |
|  |  +---------------+       +---------------+      +---------------+    |   |
|  |        |                       |                      |             |   |
|  |        v                       v                      v             |   |
|  |  +---------------+       +---------------+      +---------------+    |   |
|  |  | Schema Lock   |       | Execution     |      | Auto Commit   |    |   |
|  |  | (Exclusive)   |       | Engine        |      |               |    |   |
|  |  +---------------+       +---------------+      +---------------+    |   |
|  |                               |                                     |   |
|  |  [TCL Path]                   v                                     |   |
|  |  +---------------+       +---------------+                          |   |
|  |  | Transaction   |       | Buffer        |                          |   |
|  |  | Manager       |<----->| Manager       |                          |   |
|  |  +---------------+       +---------------+                          |   |
|  +---------------------------------------------------------------------+   |
|          |                       |                      |                 |
|          v                       v                      v                 |
|  +---------------------------------------------------------------------+   |
|  |                     STORAGE LAYER                                    |   |
|  |  +----------------+  +----------------+  +----------------+         |   |
|  |  | Data Files     |  | Index Files    |  | Log Files      |         |   |
|  |  +----------------+  +----------------+  +----------------+         |   |
|  |  +----------------+  +----------------+                              |   |
|  |  | Data Dictionary|  | Control Files  |                              |   |
|  |  +----------------+  +----------------+                              |   |
|  +---------------------------------------------------------------------+   |
|                                                                             |
+============================================================================+
```

#### 3. 심층 동작 원리: 각 언어별 처리 과정

**1단계: DDL (Data Definition Language) 처리**

```sql
-- DDL 예시와 내부 동작

-- 1. CREATE: 테이블 생성
CREATE TABLE employees (
    emp_id      NUMBER(10) PRIMARY KEY,
    emp_name    VARCHAR2(100) NOT NULL,
    dept_id     NUMBER(5),
    salary      NUMBER(10,2) CHECK (salary > 0),
    CONSTRAINT fk_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
/*
내부 동작:
1. 문법/의미 검사 (Syntax/Semantic Check)
2. 권한 검증 (CREATE TABLE 권한)
3. 스키마 락 획득 (Exclusive Lock)
4. Data Dictionary에 메타데이터 저장
   - USER_TABLES, USER_TAB_COLUMNS, USER_CONSTRAINTS 등
5. 데이터 파일에 초기 익스텐트 할당
6. 자동 커밋 (DDL은 묵시적 커밋)
7. 의존 객체 무효화 (Invalidate)
*/

-- 2. ALTER: 테이블 수정
ALTER TABLE employees ADD (hire_date DATE DEFAULT SYSDATE);
/*
내부 동작:
1. 테이블 락 획득 (Exclusive Lock)
2. Data Dictionary 갱신
3. 기존 데이터에 대한 DEFAULT 값 적용 여부 결정
4. 자동 커밋
*/

-- 3. DROP: 테이블 삭제
DROP TABLE employees CASCADE CONSTRAINTS;
/*
내부 동작:
1. 테이블 락 획득
2. 종속 객체 확인 (View, FK 등)
3. Data Dictionary에서 메타데이터 삭제
4. 휴지통 이동 (Oracle) 또는 즉시 삭제 (PURGE 옵션)
5. 공간 해제
6. 자동 커밋
*/

-- 4. TRUNCATE: 데이터 전체 삭제
TRUNCATE TABLE employees;
/*
내부 동작:
1. 테이블 락 획득 (DDL 취급)
2. High Water Mark (HWM) 리셋
3. 인덱스도 함께 TRUNCATE
4. 로그 최소화 (DELETE 대비 훨씬 빠름)
5. 공간 즉시 해제
6. 자동 커밋 (ROLLBACK 불가)
*/
```

**2단계: DML (Data Manipulation Language) 처리**

```sql
-- DML 예시와 내부 동작

-- 1. INSERT: 데이터 삽입
INSERT INTO employees (emp_id, emp_name, dept_id, salary)
VALUES (1001, '홍길동', 10, 50000000);
/*
내부 동작:
1. 구문 분석 및 권한 검증
2. 제약조건 검사 (PK 중복, FK 참조, CHECK 조건)
3. 트랜잭션 시작 (Implicit)
4. Redo Log에 변경 사항 기록
5. Undo Segment에 이전 이미지 저장
6. 버퍼 캐시에 블록 로드 후 수정
7. Lock 획득 (행 레벨)
8. 트랜잭션 활성 상태 유지 (COMMIT 대기)
*/

-- 2. UPDATE: 데이터 수정
UPDATE employees
SET salary = salary * 1.1
WHERE dept_id = 10;
/*
내부 동작:
1. 옵티마이저가 실행 계획 수립
2. WHERE 조건에 맞는 행 검색 (Full Scan 또는 Index Scan)
3. 각 행에 대해:
   - Row Lock 획득
   - Undo Segment에 이전 값 저장
   - Redo Log에 변경 사항 기록
   - 버퍼 캐시에서 데이터 수정
4. 영향받은 행 수 반환
5. 트랜잭션 활성 상태 유지
*/

-- 3. DELETE: 데이터 삭제
DELETE FROM employees WHERE emp_id = 1001;
/*
내부 동작:
1. 대상 행 검색 및 Lock 획득
2. Undo Segment에 삭제 전 데이터 저장
3. Redo Log에 DELETE 연산 기록
4. 행을 '삭제됨'으로 표시 (실제 공간 해제는 나중에)
5. 인덱스 항목 삭제
6. 트랜잭션 활성 상태 유지
*/

-- 4. SELECT: 데이터 조회
SELECT e.emp_name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE e.salary > 40000000;
/*
내부 동작:
1. Parser가 SQL 분석 → Parse Tree 생성
2. Optimizer가 실행 계획 수립:
   - 통계 정보 확인
   - 조인 순서 결정
   - 인덱스 사용 여부 결정
   - 비용 계산
3. Executor가 실행 계획 수행:
   - 데이터 블록 읽기 (Buffer Cache 우선)
   - 조인 연산 수행 (Nested Loop, Hash Join 등)
   - 필터링 적용
4. 결과 집합 반환
5. 일관성 읽기 보장 (MVCC)
*/
```

**3단계: DCL (Data Control Language) 처리**

```sql
-- DCL 예시와 내부 동작

-- 1. GRANT: 권한 부여
GRANT SELECT, INSERT, UPDATE ON employees TO hr_user;
/*
내부 동작:
1. 권한 검증 (GRANT OPTION 보유 여부)
2. System Privilege Table 갱신
   - DBA_TAB_PRIVS, USER_TAB_PRIVS 등
3. 권한 부여 로그 기록 (Audit)
4. 자동 커밋
*/

-- 시스템 권한 부여
GRANT CREATE TABLE, CREATE VIEW TO developer;
/*
시스템 권한:
- CREATE SESSION: 로그인 권한
- CREATE TABLE: 테이블 생성 권한
- CREATE PROCEDURE: 프로시저 생성 권한
- DBA: 모든 권한
*/

-- 롤(Role)을 이용한 권한 관리
CREATE ROLE hr_role;
GRANT SELECT, INSERT ON employees TO hr_role;
GRANT SELECT ON departments TO hr_role;
GRANT hr_role TO hr_user;
/*
롤의 장점:
- 권한 그룹화
- 일괄 부여/회수
- 관리 용이성
*/

-- 2. REVOKE: 권한 회수
REVOKE UPDATE ON employees FROM hr_user;
/*
내부 동작:
1. 권한 검증
2. System Privilege Table에서 해당 권한 삭제
3. 이미 시작된 세션에는 즉시 적용되지 않을 수 있음
4. 자동 커밋
*/
```

**4단계: TCL (Transaction Control Language) 처리**

```sql
-- TCL 예시와 내부 동작

-- 트랜잭션 시작 (Implicit)
UPDATE accounts SET balance = balance - 100000 WHERE account_id = 'A';
UPDATE accounts SET balance = balance + 100000 WHERE account_id = 'B';

-- 1. COMMIT: 트랜잭션 확정
COMMIT;
/*
내부 동작:
1. 트랜잭션 테이블에서 트랜잭션 상태를 'COMMITTED'로 변경
2. Redo Log Buffer를 디스크에 Flush
3. SCN (System Change Number) 할당
4. Lock 해제
5. Undo Segment 정리
6. 버퍼 캐시의 Dirty Block을 Dirty List에 등록
7. 트랜잭션 종료 알림
*/

-- 2. ROLLBACK: 트랜잭션 취소
ROLLBACK;
/*
내부 동작:
1. Undo Segment를 이용해 변경 사항 역순으로 취소
2. Redo Log에 Undo 연산 기록
3. Lock 해제
4. 트랜잭션 종료 알림
5. 버퍼 캐시 블록 복원
*/

-- 3. SAVEPOINT: 중간 저장점
SAVEPOINT transfer_complete;
-- 작업 계속...
ROLLBACK TO SAVEPOINT transfer_complete;  -- 저장점까지 롤백
COMMIT;  -- 저장점 이후 작업만 커밋
/*
내부 동작:
1. SAVEPOINT 설정 시 현재 SCN 기록
2. ROLLBACK TO 시 해당 SCN까지 Undo 수행
3. SAVEPOINT 이후의 Lock만 해제
4. 트랜잭션은 계속 활성 상태
*/
```

#### 4. 실무 수준의 DDL/DML/DCL/TCL 통합 스크립트

```python
"""
데이터베이스 마이그레이션 및 운영 스크립트
DDL, DML, DCL, TCL을 종합적으로 활용
"""

import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    DBMS 언어 체계를 활용한 데이터베이스 관리 클래스
    """

    def __init__(self, connection_string: str):
        self.conn_string = connection_string
        self.conn = None

    @contextmanager
    def transaction(self):
        """TCL을 이용한 트랜잭션 컨텍스트 매니저"""
        conn = psycopg2.connect(self.conn_string)
        conn.autocommit = False  # 명시적 트랜잭션
        try:
            yield conn
            conn.commit()  # TCL: COMMIT
            logger.info("Transaction committed successfully")
        except Exception as e:
            conn.rollback()  # TCL: ROLLBACK
            logger.error(f"Transaction rolled back: {e}")
            raise
        finally:
            conn.close()

    # ==================== DDL ====================

    def create_schema(self) -> None:
        """DDL: 스키마 생성"""
        with self.transaction() as conn:
            cursor = conn.cursor()

            # DDL: 테이블 생성
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    dept_id     SERIAL PRIMARY KEY,
                    dept_name   VARCHAR(50) NOT NULL UNIQUE,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    emp_id      SERIAL PRIMARY KEY,
                    emp_name    VARCHAR(100) NOT NULL,
                    dept_id     INTEGER REFERENCES departments(dept_id),
                    salary      DECIMAL(10,2) CHECK (salary > 0),
                    email       VARCHAR(100) UNIQUE,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # DDL: 인덱스 생성
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_employees_dept
                ON employees(dept_id)
            """)

            # DDL: 트리거 생성 (updated_at 자동 갱신)
            cursor.execute("""
                CREATE OR REPLACE FUNCTION update_updated_at()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql
            """)

            cursor.execute("""
                DROP TRIGGER IF EXISTS trg_employees_updated_at ON employees;
                CREATE TRIGGER trg_employees_updated_at
                    BEFORE UPDATE ON employees
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at()
            """)

            logger.info("Schema created successfully")

    def alter_table_add_column(self) -> None:
        """DDL: 테이블 변경"""
        with psycopg2.connect(self.conn_string) as conn:
            conn.autocommit = True  # DDL은 자동 커밋
            cursor = conn.cursor()

            cursor.execute("""
                ALTER TABLE employees
                ADD COLUMN IF NOT EXISTS hire_date DATE DEFAULT CURRENT_DATE
            """)

            logger.info("Column added successfully")

    def truncate_table(self) -> None:
        """DDL: 데이터 전체 삭제 (TRUNCATE)"""
        with psycopg2.connect(self.conn_string) as conn:
            conn.autocommit = True
            cursor = conn.cursor()

            # TRUNCATE는 DDL이므로 자동 커밋, ROLLBACK 불가
            cursor.execute("TRUNCATE TABLE employees RESTART IDENTITY CASCADE")
            logger.info("Table truncated successfully")

    # ==================== DML ====================

    def insert_employee(self, emp_name: str, dept_id: int,
                       salary: float, email: str) -> int:
        """DML: 데이터 삽입"""
        with self.transaction() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO employees (emp_name, dept_id, salary, email)
                VALUES (%s, %s, %s, %s)
                RETURNING emp_id
            """, (emp_name, dept_id, salary, email))

            emp_id = cursor.fetchone()[0]
            logger.info(f"Employee inserted: {emp_id}")
            return emp_id

    def batch_insert_employees(self, employees: list) -> None:
        """DML: 배치 삽입 (성능 최적화)"""
        with self.transaction() as conn:
            cursor = conn.cursor()

            # executemany를 이용한 배치 삽입
            cursor.executemany("""
                INSERT INTO employees (emp_name, dept_id, salary, email)
                VALUES (%(name)s, %(dept_id)s, %(salary)s, %(email)s)
            """, employees)

            logger.info(f"Batch inserted {len(employees)} employees")

    def update_employee_salary(self, emp_id: int, new_salary: float) -> bool:
        """DML: 데이터 수정"""
        with self.transaction() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE employees
                SET salary = %s
                WHERE emp_id = %s
            """, (new_salary, emp_id))

            affected = cursor.rowcount > 0
            logger.info(f"Update affected rows: {cursor.rowcount}")
            return affected

    def delete_employee(self, emp_id: int) -> bool:
        """DML: 데이터 삭제"""
        with self.transaction() as conn:
            cursor = conn.cursor()

            cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))

            affected = cursor.rowcount > 0
            logger.info(f"Delete affected rows: {cursor.rowcount}")
            return affected

    def select_employees_by_dept(self, dept_id: int) -> list:
        """DML: 데이터 조회"""
        with psycopg2.connect(self.conn_string) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT e.emp_id, e.emp_name, e.salary, d.dept_name
                FROM employees e
                JOIN departments d ON e.dept_id = d.dept_id
                WHERE e.dept_id = %s
                ORDER BY e.emp_name
            """, (dept_id,))

            return cursor.fetchall()

    # ==================== DCL ====================

    def create_user(self, username: str, password: str) -> None:
        """DCL: 사용자 생성"""
        with psycopg2.connect(self.conn_string) as conn:
            conn.autocommit = True  # DCL은 자동 커밋
            cursor = conn.cursor()

            cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
                sql.Identifier(username)
            ), (password,))

            logger.info(f"User created: {username}")

    def grant_privileges(self, username: str, privileges: str,
                        table_name: str) -> None:
        """DCL: 권한 부여"""
        with psycopg2.connect(self.conn_string) as conn:
            conn.autocommit = True
            cursor = conn.cursor()

            cursor.execute(sql.SQL("GRANT {} ON {} TO {}").format(
                sql.SQL(privileges),
                sql.Identifier(table_name),
                sql.Identifier(username)
            ))

            logger.info(f"Granted {privileges} on {table_name} to {username}")

    def revoke_privileges(self, username: str, privileges: str,
                         table_name: str) -> None:
        """DCL: 권한 회수"""
        with psycopg2.connect(self.conn_string) as conn:
            conn.autocommit = True
            cursor = conn.cursor()

            cursor.execute(sql.SQL("REVOKE {} ON {} FROM {}").format(
                sql.SQL(privileges),
                sql.Identifier(table_name),
                sql.Identifier(username)
            ))

            logger.info(f"Revoked {privileges} on {table_name} from {username}")

    # ==================== TCL (Advanced) ====================

    def transfer_salary(self, from_emp: int, to_emp: int,
                       amount: float) -> None:
        """TCL: SAVEPOINT를 이용한 부분 롤백 예시"""
        with psycopg2.connect(self.conn_string) as conn:
            conn.autocommit = False
            cursor = conn.cursor()

            try:
                # 출금
                cursor.execute("""
                    UPDATE employees SET salary = salary - %s
                    WHERE emp_id = %s AND salary >= %s
                """, (amount, from_emp, amount))

                if cursor.rowcount == 0:
                    raise ValueError("Insufficient balance or employee not found")

                # SAVEPOINT 설정
                cursor.execute("SAVEPOINT after_withdrawal")

                # 입금
                cursor.execute("""
                    UPDATE employees SET salary = salary + %s
                    WHERE emp_id = %s
                """, (amount, to_emp))

                if cursor.rowcount == 0:
                    # SAVEPOINT까지 롤백
                    cursor.execute("ROLLBACK TO SAVEPOINT after_withdrawal")
                    raise ValueError("Recipient employee not found")

                # 커밋
                conn.commit()
                logger.info(f"Transfer completed: {amount} from {from_emp} to {to_emp}")

            except Exception as e:
                conn.rollback()
                logger.error(f"Transfer failed: {e}")
                raise

# 사용 예시
if __name__ == '__main__':
    db = DatabaseManager("postgresql://user:pass@localhost/testdb")

    # DDL: 스키마 생성
    db.create_schema()

    # DCL: 사용자 생성 및 권한 부여
    db.create_user("hr_user", "secure_password")
    db.grant_privileges("hr_user", "SELECT, INSERT, UPDATE", "employees")

    # DML: 데이터 조작
    dept_id = 1
    emp_id = db.insert_employee("홍길동", dept_id, 50000000, "hong@example.com")

    # TCL: 트랜잭션
    db.transfer_salary(emp_id, 2, 1000000)
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. DDL vs DML vs DCL vs TCL 비교

| 비교 항목 | DDL | DML | DCL | TCL |
|:---|:---|:---|:---|:---|
| **목적** | 구조 정의 | 데이터 조작 | 권한 관리 | 트랜잭션 관리 |
| **주요 명령** | CREATE, ALTER, DROP | SELECT, INSERT, UPDATE, DELETE | GRANT, REVOKE | COMMIT, ROLLBACK, SAVEPOINT |
| **Auto Commit** | O | X | O | - |
| **롤백 가능** | X* | O | X | - |
| **락 유형** | 스키마 락 (배타적) | 행 락, 테이블 락 | 메타데이터 락 | - |
| **실행 빈도** | 낮음 | 매우 높음 | 낮음 | 높음 |
| **로그** | DDL 로그 | Redo/Undo 로그 | Audit 로그 | 트랜잭션 로그 |

#### 2. DELETE vs TRUNCATE 심층 비교

| 비교 항목 | DELETE | TRUNCATE |
|:---|:---|:---|
| **분류** | DML | DDL |
| **WHERE 조건** | 지원 (선택적 삭제) | 미지원 (전체 삭제) |
| **롤백** | 가능 | 불가능* |
| **로그** | 행별 로그 (많음) | 페이지별 로그 (적음) |
| **속도** | 느림 | 매우 빠름 |
| **공간 해제** | 유지 | 즉시 해제 |
| **인덱스** | 개별 삭제 | 함께 TRUNCATE |
| **트리거** | 실행됨 | 실행 안 됨 |
| **HWM 리셋** | 안 됨 | 됨 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 대용량 데이터 삭제**
- 상황: 1억 건의 로그 데이터 삭제
- 판단: DELETE vs TRUNCATE
- 전략:
  - 전체 삭제: TRUNCATE (속도 100배 이상)
  - 조건부 삭제: DELETE + BATCH (10만 건씩)
  - 파티션 활용: DROP PARTITION

**시나리오 2: 스키마 변경 시 무중단**
- 상황: 운영 중인 테이블에 컬럼 추가
- 판단: DDL은 락을 유발
- 전략:
  - Online DDL 활용 (MySQL 5.6+, PostgreSQL)
  - 저시간대 실행
  - pt-online-schema-change 도구

**시나리오 3: 권한 관리 체계화**
- 상황: 100명의 사용자, 50개 테이블
- 판단: 개별 GRANT는 관리 어려움
- 전략:
  - Role 기반 권한 관리 (RBAC)
  - 읽기 전용 Role, 읽기/쓰기 Role 분리
  - 정기적 권한 감사

#### 2. 도입 시 고려사항 (체크리스트)

**DDL 설계 체크리스트**:
- [ ] 데이터 타입 최적화
- [ ] 제약조건 (PK, FK, CHECK, NOT NULL)
- [ ] 인덱스 전략
- [ ] 파티셔닝 필요성
- [ ] DDL 롤백 방안

**DML 작성 체크리스트**:
- [ ] WHERE 조건 누락 방지
- [ ] 배치 처리 고려
- [ ] 인덱스 활용 확인
- [ ] 트랜잭션 범위 최소화
- [ ] Deadlock 방지

**DCL 관리 체크리스트**:
- [ ] 최소 권한 원칙 (Principle of Least Privilege)
- [ ] Role 기반 관리
- [ ] 정기적 권한 감사
- [ ] 민감 데이터 접근 통제

#### 3. 안티패턴 (Anti-patterns)

1. **무조건 TRUNCATE**: WHERE 조건 필요한데 TRUNCATE 사용
   - 해결: DELETE + LIMIT 또는 파티션

2. **과도한 권한 부여**: 모든 사용자에게 ALL PRIVILEGES
   - 해결: 최소 권한 원칙 적용

3. **트랜잭션 범위 과대**: 너무 긴 트랜잭션
   - 해결: 짧은 트랜잭션으로 분할

4. **DDL 실행 시간 미고려**: 업무 시간 대규모 DDL
   - 해결: 유지보수 시간 활용

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 무분별 사용 | 체계적 관리 | 개선 효과 |
|:---|:---|:---|:---|
| **DDL 실행 시간** | 업무 중단 | 유지보수 시간 | 서비스 안정성 향상 |
| **대용량 삭제** | DELETE (시간) | TRUNCATE (초) | 100배 이상 향상 |
| **권한 사고** | 빈번 | 드묾 | 보안 사고 90% 감소 |
| **트랜잭션 실패** | 잦음 | 드묾 | 데이터 무결성 보장 |

#### 2. 미래 전망 및 진화 방향

**DDL의 진화**:
- **Online DDL**: 무중단 스키마 변경
- **Schema Migration Tool**: Flyway, Liquibase
- **GitOps for Schema**: IaC 기반 스키마 관리

**DCL의 진화**:
- **Attribute-Based Access Control (ABAC)**: 속성 기반 접근 제어
- **Zero Trust Database**: 지속적 인증/인가
- **Data Masking**: 동적 데이터 마스킹

#### 3. 참고 표준/가이드

| 표준 | 내용 | 적용 범위 |
|:---|:---|:---|
| **ANSI/ISO SQL** | SQL 표준 언어 | 전체 DBMS |
| **NIST AC-3** | 접근 통제 | 보안 인증 |
| **CIS Benchmark** | DB 보안 설정 | 보안 강화 |

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[SQL](@/studynotes/5_database/2_sql/_index.md)**: DDL/DML/DCL/TCL의 구체적 문법
- **[트랜잭션](@/studynotes/5_database/4_transaction/_index.md)**: TCL의 이해
- **[무결성 제약조건](@/studynotes/5_database/1_relational/integrity_constraints.md)**: DDL의 제약 정의
- **[인덱스](@/studynotes/5_database/5_indexing/_index.md)**: DDL의 인덱스 생성
- **[보안](@/studynotes/5_database/9_security/_index.md)**: DCL의 권한 관리

---

### 👶 어린이를 위한 3줄 비유 설명

1. **건축과 인테리어**: 집을 짓는 게 DDL이에요. 벽을 세우고 방을 만들죠. 가구를 배치하고 물건을 쓰는 게 DML이에요. 누가 집에 들어올 수 있는지 정하는 게 DCL이에요!

2. **장난감 정리함 만들기**: 정리함을 조립하는 게 DDL(CREATE), 장난감을 넣고 빼는 게 DML(INSERT, DELETE), 친구에게 "이건 만지지 마"라고 하는 게 DCL(GRANT, REVOKE)이에요!

3. **게임 세이브**: 게임을 저장하는 게 COMMIT, 실수했을 때 다시 불러오는 게 ROLLBACK이에요. 중간 저장점은 SAVEPOINT! 이렇게 게임 진행을 관리하는 게 TCL이에요!
