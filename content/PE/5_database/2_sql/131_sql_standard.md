+++
title = "SQL (Structured Query Language) 국제 표준 (ANSI/ISO SQL)"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
++-

# SQL (Structured Query Language) 국제 표준 (ANSI/ISO SQL)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL은 관계형 데이터베이스 관리 시스템(RDBMS)에서 데이터를 정의(DDL), 조작(DML), 제어(DCL)하기 위한 선언적(Declarative) 질의 언어로, ANSI/ISO 표준에 의해 규정되어 데이터베이스 벤더 간 이식성을 보장합니다.
> 2. **가치**: 비절차적 선언형 언어로 '무엇을' 원하는지만 명시하면 옵티마이저가 '어떻게' 수행할지 결정하며, 이를 통해 개발 생산성을 높이고 SQL 인젝션 방지, 데이터 무결성 보장 등의 보안 기능을 제공합니다.
> 3. **융합**: 관계 대수(Relational Algebra)의 실용적 구현체로, 현대에는 JSON 지원, 윈도우 함수, CTE(Common Table Expression) 등 분석 기능이 확장되어 OLTP와 OLAP를 아우르는 범용 데이터 처리 언어로 진화했습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**SQL(Structured Query Language)**은 관계형 데이터베이스에서 데이터를 관리하기 위한 표준화된 프로그래밍 언어입니다. 1974년 IBM의 Donald D. Chamberlin과 Raymond F. Boyce가 개발한 SEQUEL(Structured English Query Language)이 기원이며, 현재 ANSI(미국 국립 표준 협회)와 ISO(국제 표준화 기구)에 의해 표준화되어 있습니다.

**SQL의 분류**:
- **DDL (Data Definition Language)**: CREATE, ALTER, DROP, TRUNCATE
- **DML (Data Manipulation Language)**: SELECT, INSERT, UPDATE, DELETE
- **DCL (Data Control Language)**: GRANT, REVOKE
- **TCL (Transaction Control Language)**: COMMIT, ROLLBACK, SAVEPOINT

#### 2. 💡 비유를 통한 이해
SQL은 **'레스토랑에서의 주문'**과 같습니다.

- 손님(사용자)은 메뉴판(SQL 문법)을 보고 원하는 요리(결과)를 주문합니다.
- 주문서("스테이크, 레어로, 샐러드 포함")를 작성합니다 (SQL 작성).
- 주방장(옵티마이저)이 주문서를 보고 요리 방법(실행 계획)을 결정합니다.
- 요리사(DBMS)가 실제로 요리(쿼리 수행)합니다.
- 손님은 완성된 요리(결과 집합)를 받습니다.

손님은 요리 방법을 알 필요가 없습니다. 무엇을 원하는지만 말하면 됩니다 (선언적 언어).

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 초기 데이터베이스(IMS, CODASYL)는 네비게이션 방식(어떻게 데이터에 접근할지 경로 명시)으로, 복잡하고 프로그래밍에 숙련된 전문가만 사용할 수 있었습니다.

2. **혁신적 패러다임의 도입**: 1970년 E.F. Codd의 관계형 모델 발표 후, 1974년 IBM의 SEQUEL이 영어 문장과 유사한 구문으로 데이터를 조회하는 혁신을 가져왔습니다. 1986년 ANSI SQL-86이 최초의 표준으로 채택되었습니다.

3. **비즈니스적 요구사항**: 현대 기업은 다양한 DBMS(Oracle, SQL Server, PostgreSQL, MySQL)를 사용합니다. SQL 표준은 이들 간의 이식성을 보장하고, 개발자 학습 비용을 절감합니다.

---

### Ⅱ. 아키택처 및 핵심 원리 (Deep Dive)

#### 1. SQL 표준 진화 (표)

| 표준 | 연도 | 주요 추가 기능 |
|:---|:---|:---|
| **SQL-86** | 1986 | 최초 표준, 기본 DDL/DML |
| **SQL-89** | 1989 | 참조 무결성(Referential Integrity) |
| **SQL-92** | 1992 | JOIN 구문, CAST, CASE, UNION |
| **SQL:1999** | 1999 | REGEXP, CUBE/ROLLUP, Recursive Query |
| **SQL:2003** | 2003 | 윈도우 함수, MERGE, XML |
| **SQL:2006** | 2006 | XML 관련 기능 확장 |
| **SQL:2008** | 2008 | TRUNCATE, INSTEAD OF Trigger |
| **SQL:2011** | 2011 | Temporal DB, Pipelined DML |
| **SQL:2016** | 2016 | JSON, Polymorphic Table Functions |
| **SQL:2023** | 2023 | Property Graph Queries, JSON enhancements |

#### 2. SQL 처리 아키텍처 다이어그램

```text
================================================================================
                    [ SQL Query Processing Architecture ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                           [ Client ]                                         │
│  SQL: SELECT e.name, d.dept_name                                            │
│       FROM employees e                                                       │
│       JOIN departments d ON e.dept_id = d.dept_id                           │
│       WHERE e.salary > 50000                                                │
│       ORDER BY e.name;                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ SQL Text
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          [ Parser ]                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  1. Lexical Analysis (Tokenizing)                                      │  │
│  │     SELECT, e, ., name, ,, d, ., dept_name, FROM, ...                  │  │
│  │                                                                        │  │
│  │  2. Syntax Analysis (Parsing)                                          │  │
│  │     ┌──────────────────────────────────────────────────────────┐      │  │
│  │     │                    SELECT                                 │      │  │
│  │     │                   /      \                               │      │  │
│  │     │               JOIN        ORDER BY                       │      │  │
│  │     │              /    \           |                          │      │  │
│  │     │          FROM    WHERE    e.name                        │      │  │
│  │     │           |        |                                     │      │  │
│  │     │    ┌─────┴─────┐  e.salary > 50000                      │      │  │
│  │     │    |           |                                         │      │  │
│  │     │ employees  departments                                   │      │  │
│  │     └──────────────────────────────────────────────────────────┘      │  │
│  │                                                                        │  │
│  │  3. Semantic Analysis (Validation)                                     │  │
│  │     - Check table/column existence in system catalog                   │  │
│  │     - Check data types, privileges                                     │  │
│  │     - Resolve ambiguous references                                     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                              │                                              │
│                              │ Parse Tree (Abstract Syntax Tree)           │
│                              ▼                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                       [ Optimizer ]                                    │  │
│  │                                                                        │  │
│  │  ┌─────────────────┐   ┌────────────────────────────────────────────┐ │  │
│  │  │ Rule-Based (RBO)│   │ Cost-Based (CBO)                          │ │  │
│  │  │ (Deprecated)    │   │ - Statistics: table cardinality, dist vals │ │  │
│  │  │                 │   │ - Cost Model: I/O, CPU, Network            │ │  │
│  │  │                 │   │ - Plan Enumeration: DP, Greedy            │ │  │
│  │  └─────────────────┘   └────────────────────────────────────────────┘ │  │
│  │                                                                        │  │
│  │  [ Optimization Steps ]                                                │  │
│  │  1. Query Rewriting (View Merging, Predicate Pushdown)                │  │
│  │  2. Access Path Selection (Index Scan vs Full Table Scan)             │  │
│  │  3. Join Order Optimization (Dynamic Programming)                     │  │
│  │  4. Join Method Selection (NL, Hash, Sort Merge)                      │  │
│  │                                                                        │  │
│  │  [ Generated Execution Plan ]                                          │  │
│  │  ┌────────────────────────────────────────────────────────────────┐   │  │
│  │  │ Id | Operation              | Rows | Cost |                     │   │  │
│  │  │ 0  | SELECT STATEMENT       | 100  | 50   |                     │   │  │
│  │  │ 1  |  SORT ORDER BY         | 100  | 50   |                     │   │  │
│  │  │ 2  |   HASH JOIN            | 100  | 45   |                     │   │  │
│  │  │ 3  |    TABLE ACCESS FULL   | 50   | 10   | DEPARTMENTS         │   │  │
│  │  │ 4  |    TABLE ACCESS BY IDX | 100  | 30   | EMPLOYEES           │   │  │
│  │  └────────────────────────────────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ Execution Plan
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       [ Execution Engine ]                                   │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  1. Open Cursors                                                       │  │
│  │  2. Execute Plan Tree (Volcano/Iterator Model)                         │  │
│  │     - Root calls next() on children                                    │  │
│  │     - Data flows bottom-up                                             │  │
│  │  3. Fetch Results                                                      │  │
│  │  4. Close Cursors                                                      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ Result Set
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           [ Result ]                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ name       | dept_name                                              │   │
│  │ ───────────┼─────────────                                           │   │
│  │ Alice      | Engineering                                            │   │
│  │ Bob        | Sales                                                  │   │
│  │ Carol      | Engineering                                            │   │
│  │ David      | Marketing                                              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
================================================================================
```

#### 3. 심층 동작 원리: SQL 처리 단계

1. **파싱(Parsing)**:
   - 어휘 분석(Lexical Analysis): SQL 문을 토큰으로 분리
   - 구문 분석(Syntax Analysis): 토큰을 파스 트리로 구성
   - 의미 분석(Semantic Analysis): 테이블/컬럼 존재 확인, 타입 체크

2. **최적화(Optimization)**:
   - 질의 변환(Query Rewriting): 뷰 머징, 조건 푸시다운
   - 비용 계산(Cost Estimation): 통계 정보 기반 I/O, CPU 비용 추정
   - 계획 선택(Plan Selection): 동적 계획법으로 최적 실행 계획 선택

3. **실행(Execution)**:
   - 이터레이터 모델(Iterator Model): 각 연산자가 next()를 호출
   - 데이터 흐름: 리프 노드(테이블 스캔) → 상위 노드(조인, 필터) → 루트(결과)

#### 4. 실무 수준의 SQL 예시

```sql
-- ========================================
-- DDL: 데이터 정의 언어
-- ========================================

-- 테이블 생성
CREATE TABLE employees (
    emp_id      NUMBER PRIMARY KEY,
    emp_name    VARCHAR2(100) NOT NULL,
    dept_id     NUMBER,
    salary      NUMBER(10,2) CHECK (salary > 0),
    hire_date   DATE DEFAULT SYSDATE,
    CONSTRAINT fk_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- 인덱스 생성
CREATE INDEX idx_emp_name ON employees(emp_name);
CREATE INDEX idx_emp_dept ON employees(dept_id);

-- 테이블 수정
ALTER TABLE employees ADD email VARCHAR2(100);
ALTER TABLE employees MODIFY salary NUMBER(12,2);

-- 테이블 삭제
DROP TABLE employees PURGE;  -- Oracle: 휴지통 거치지 않고 삭제
TRUNCATE TABLE employees;     -- 데이터만 삭제, 구조 유지 (DDL, 롤백 불가)

-- ========================================
-- DML: 데이터 조작 언어
-- ========================================

-- INSERT
INSERT INTO employees (emp_id, emp_name, dept_id, salary)
VALUES (1, 'John Doe', 10, 75000);

-- 다중 INSERT (Oracle)
INSERT ALL
    INTO employees VALUES (1, 'Alice', 10, 60000, SYSDATE, NULL)
    INTO employees VALUES (2, 'Bob', 20, 55000, SYSDATE, NULL)
SELECT * FROM dual;

-- UPDATE
UPDATE employees
SET salary = salary * 1.1
WHERE dept_id = 10;

-- DELETE
DELETE FROM employees
WHERE hire_date < ADD_MONTHS(SYSDATE, -36);

-- MERGE (Upsert)
MERGE INTO employees e
USING (SELECT * FROM new_employees) n
ON (e.emp_id = n.emp_id)
WHEN MATCHED THEN
    UPDATE SET e.salary = n.salary
WHEN NOT MATCHED THEN
    INSERT (emp_id, emp_name, dept_id, salary, hire_date)
    VALUES (n.emp_id, n.emp_name, n.dept_id, n.salary, n.hire_date);

-- ========================================
-- SELECT: 질의 언어
-- ========================================

-- 기본 조회
SELECT emp_name, salary
FROM employees
WHERE salary > 50000
ORDER BY salary DESC;

-- 조인
SELECT e.emp_name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id
WHERE d.location = 'SEOUL';

-- 서브쿼리
SELECT emp_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 윈도우 함수 (SQL:2003)
SELECT
    emp_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS salary_rank,
    SUM(salary) OVER (PARTITION BY dept_id) AS dept_total,
    AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg,
    LAG(salary) OVER (ORDER BY hire_date) AS prev_salary
FROM employees;

-- 공통 테이블 표현식 (CTE)
WITH top_earners AS (
    SELECT emp_name, salary, dept_id
    FROM employees
    WHERE salary > 100000
),
dept_counts AS (
    SELECT dept_id, COUNT(*) AS emp_count
    FROM employees
    GROUP BY dept_id
)
SELECT t.emp_name, t.salary, d.emp_count
FROM top_earners t
JOIN dept_counts d ON t.dept_id = d.dept_id;

-- 재귀 쿼리 (조직도)
WITH RECURSIVE org_chart AS (
    -- Anchor: 최상위 관리자
    SELECT emp_id, emp_name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive: 부하 직원
    SELECT e.emp_id, e.emp_name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.emp_id
)
SELECT * FROM org_chart ORDER BY level;

-- ========================================
-- DCL: 데이터 제어 언어
-- ========================================

-- 권한 부여
GRANT SELECT, INSERT ON employees TO hr_user;
GRANT ALL PRIVILEGES ON employees TO admin_user;

-- 권한 회수
REVOKE INSERT ON employees FROM hr_user;

-- 롤 생성 및 할당
CREATE ROLE hr_manager;
GRANT SELECT, INSERT, UPDATE ON employees TO hr_manager;
GRANT hr_manager TO user_alice;

-- ========================================
-- TCL: 트랜잭션 제어 언어
-- ========================================

BEGIN TRANSACTION;  -- 또는 SET TRANSACTION

UPDATE accounts SET balance = balance - 1000 WHERE id = 'A';
UPDATE accounts SET balance = balance + 1000 WHERE id = 'B';

SAVEPOINT after_first_update;

INSERT INTO transaction_log (from_id, to_id, amount)
VALUES ('A', 'B', 1000);

-- 정상 완료
COMMIT;

-- 오류 발생 시
-- ROLLBACK TO after_first_update;  -- 부분 롤백
-- ROLLBACK;  -- 전체 롤백
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. SQL vs 관계 대수 비교

| 비교 항목 | 관계 대수 (Relational Algebra) | SQL |
|:---|:---|:---|
| **성격** | 절차적 (Procedural) | 선언적 (Declarative) |
| **관심사** | "어떻게" 구할 것인가 | "무엇을" 구할 것인가 |
| **수학적 기반** | 집합론 | 관계 대수 + 관계 해석 |
| **연산자** | σ, π, ⋈, ∪, ∩, - | SELECT, JOIN, UNION, INTERSECT |
| **구현** | 이론적 모델 | 실용적 구현 (벤더별 확장) |
| **최적화** | 사용자가 수행 | 옵티마이저가 수행 |

#### 2. DBMS별 SQL 방언(Dialect) 비교

| 기능 | Oracle | PostgreSQL | MySQL | SQL Server |
|:---|:---|:---|:---|:---|
| **문자열 연결** | `||` | `||` | CONCAT() | `+` |
| **NULL 처리** | NVL() | COALESCE() | IFNULL() | ISNULL() |
| **페이징** | ROWNUM, FETCH | LIMIT/OFFSET | LIMIT/OFFSET | OFFSET FETCH |
| **시퀀스** | SEQUENCE | SEQUENCE/SERIAL | AUTO_INCREMENT | IDENTITY |
| **조건문** | DECODE(), CASE | CASE | CASE, IF() | CASE, IIF() |
| **날짜** | SYSDATE | NOW(), CURRENT_DATE | NOW() | GETDATE() |
| **제한** | WHERE ROWNUM <= 10 | LIMIT 10 | LIMIT 10 | TOP 10 |

#### 3. 과목 융합 관점 분석

- **[자료구조/알고리즘 융합] 옵티마이저**: SQL 최적화는 동적 계획법(Dynamic Programming), 탐욕 알고리즘(Greedy), 분기 한정(Branch and Bound) 등의 알고리즘을 사용합니다. 조인 순서 최적화는 NP-hard 문제입니다.

- **[컴파일러 융합] 파싱**: SQL 파서는 어휘 분석, 구문 분석, 의미 분석 과정을 거치며, 이는 컴파일러의 프론트엔드와 동일한 원리입니다.

- **[보안 융합] SQL 인젝션**: 동적 SQL 생성 시 사용자 입력을 검증하지 않으면 SQL 인젝션 공격에 취약합니다. Prepared Statement, 바인드 변수 사용이 필수입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

- **시나리오 1: 대규모 데이터 마이그레이션**
  - 상황: Oracle에서 PostgreSQL로 1억 건 데이터 이관.
  - 판단: 표준 SQL 사용. NVL → COALESCE, ROWNUM → LIMIT 등 방언 변환 필요. 데이터 타입 호환성 확인. Procedural Language(PL/SQL → PL/pgSQL)는 대규모 재작성 필요.

- **시나리오 2: SQL 성능 튜닝**
  - 상황: 특정 쿼리의 응답 시간이 30초로 느림.
  - 판단: 실행 계획 분석 (EXPLAIN PLAN). 인덱스 사용 여부, 조인 순서, 필터링 시점 확인. 힌트(Hint) 사용은 최후 수단. SQL 튜닝보다 스키마/인덱스 설계가 우선.

- **시나리오 3: SQL 인젝션 방지**
  - 상황: 웹 애플리케이션에서 사용자 입력을 SQL에 직접 포함.
  - 판단: Prepared Statement(PreparedStatement) 사용. 바인드 변수(?)로 사용자 입력 처리. ORM 사용 시 자동 방지. 입력값 검증은 보조 수단.

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **표준 준수**: 벤더 독자적 확장 기능 최소화
- [ ] **성능**: 실행 계획 분석, 인덱스 활용
- [ ] **보안**: SQL 인젝션 방지 (바인드 변수)
- [ ] **가독성**: 포맷팅, 명명 규칙, 주석
- [ ] **유지보수**: 복잡한 로직은 Stored Procedure보다 애플리케이션 계층에서 구현

#### 3. 안티패턴 (Anti-patterns)

- **SELECT \***: 필요한 컬럼만 지정해야 I/O와 네트워크 비용이 절감됩니다.

- **인라인 값 하드코딩**: `WHERE id = 123` 대신 `WHERE id = ?` (바인드 변수)를 사용해야 쿼리 캐시 효율이 높아집니다.

- **서브쿼리 남용**: 상관 서브쿼리(Correlated Subquery)는 성능 저하의 주범입니다. JOIN이나 윈도우 함수로 대체해야 합니다.

- **비즈니스 로직의 SQL 구현**: 복잡한 비즈니스 로직을 SQL로 구현하면 유지보수가 어렵습니다. SQL은 데이터 조작에 집중해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 효과 영역 | 내용 | 개선 지표 |
|:---|:---|:---|
| **생산성** | 선언적 언어로 간결한 코드 | 코드량 50% 감소 |
| **이식성** | 표준 준수로 DBMS 교체 용이 | 마이그레이션 비용 30% 감소 |
| **성능** | 옵티마이저의 자동 최적화 | 수동 튜닝 대비 안정적 성능 |
| **보안** | 바인드 변수로 인젝션 방지 | 보안 사고 90% 감소 |

#### 2. 미래 전망

SQL은 **AI/ML과의 통합**과 **빅데이터 처리**로 확장하고 있습니다:

1. **SQL on Hadoop/Spark**: Hive, SparkSQL로 빅데이터 처리
2. **SQL on JSON**: JSON 데이터를 SQL로 직접 조회 (PostgreSQL, MySQL, Oracle)
3. **SQL for ML**: BigQuery ML, SQL Server ML Services로 머신러닝 모델 학습/예측
4. **GraphQL vs SQL**: API 계층에서 GraphQL, 저장 계층에서 SQL의 협력 관계

#### 3. 참고 표준

- **ANSI X3.135**: American National Standard for Database Language SQL
- **ISO/IEC 9075**: Information Technology - Database Languages - SQL
- **SQL:2023**: 최신 SQL 표준

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[관계 대수](@/studynotes/5_database/1_relational/relational_algebra.md)**: SQL의 이론적 기반.
- **[옵티마이저](@/studynotes/5_database/3_optimization/query_optimization.md)**: SQL을 실행 계획으로 변환.
- **[DDL/DML/DCL](@/studynotes/5_database/1_relational/ddl_dml_dcl.md)**: SQL의 언어 분류.
- **[조인](@/studynotes/5_database/_index.md)**: SQL의 핵심 연산.
- **[트랜잭션](@/studynotes/5_database/1_relational/acid.md)**: TCL로 제어.

---

### 👶 어린이를 위한 3줄 비유 설명

1. **주문서 작성**: SQL은 식당에서 메뉴를 주문하는 것과 같아요. "스파게티 하나 주세요"라고 말하면, 주방에서 알아서 만들어요.
2. **선언적 언어**: 요리 방법을 알려주는 게 아니라, 무엇을 먹고 싶은지만 말하면 돼요. "어떻게"는 주방장(옵티마이저)이 결정해요.
3. **표준 언어**: 어떤 식당이든 메뉴판(SQL)은 비슷해요. 그래서 한 식당의 메뉴판을 알면 다른 식당에서도 주문할 수 있어요!
