+++
title = "절차적 DML vs 비절차적 DML (Procedural vs Non-procedural)"
description = "네비게이션 방식과 선언적 방식의 데이터 조작 언어 비교 분석"
date = "2026-03-05"
[taxonomies]
tags = ["database", "dml", "procedural", "non-procedural", "declarative", "sql"]
categories = ["studynotes-5_database"]
+++

# 19. 절차적 DML vs 비절차적 DML (Procedural vs Non-procedural DML)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 절차적 DML은 데이터에 접근하는 방법(How)을 명시하는 네비게이션 방식이며, 비절차적 DML은 원하는 결과(What)만 선언하는 방식으로, SQL이 대표적인 비절차적 언어입니다.
> 2. **가치**: 비절차적 DML(SQL)은 옵티마이저가 최적의 실행 계획을 수립하므로 개발 생산성을 5~10배 향상시키며, DBMS 독립적인 코드 작성이 가능합니다.
> 3. **융합**: 현대 데이터베이스는 SQL(비절차적)에 PL/SQL, T-SQL 등 절차적 확장을 결합하여 두 방식의 장점을 통합하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**절차적 DML(Procedural DML)**은 데이터에 접근하고 조작하는 구체적인 절차(How)를 사용자가 명시하는 방식입니다. 레코드 간의 이동 경로, 반복문, 조건문 등을 직접 제어합니다.

**비절차적 DML(Non-procedural DML)**은 원하는 결과(What)만 선언하고, 데이터에 접근하는 방법은 DBMS에 위임하는 방식입니다. 사용자는 "무엇을 원하는가"만 표현합니다.

| 구분 | 절차적 DML | 비절차적 DML |
|:---|:---|:---|
| **정의** | "어떻게" 할 것인가 명시 | "무엇을" 원하는가 선언 |
| **대표 언어** | IMS DL/1, CODASYL DML, PL/SQL | SQL (Structured Query Language) |
| **제어권** | 사용자가 완전히 제어 | DBMS 옵티마이저가 제어 |
| **레코드 접근** | 한 번에 하나씩 (Navigation) | 집합 단위 (Set-at-a-time) |
| **반복문** | 명시적 Loop 필요 | 암시적 (SQL 엔진 처리) |
| **최적화** | 사용자 책임 | 옵티마이저 책임 |
| **학습 곡선** | 높음 | 낮음 |
| **이식성** | 낮음 (DBMS 종속) | 높음 (SQL 표준) |

**비유를 통한 이해**:
- **절차적**: "지도를 보고 직접 운전하기" - 어디서 좌회전, 어디서 우회전할지 모두 지시
- **비절차적**: "내비게이션에 목적지 입력하기" - 목적지만 입력하면 최적 경로는 내비게이션이 결정

#### 2. 💡 비유를 통한 이해

**음식 주문**으로 비유:

**절차적 주문 (레시피 방식)**:
```
1. 냉장고에서 달걀 2개를 꺼낸다
2. 프라이팬을 가스레인지에 올린다
3. 불을 중불로 켠다
4. 달걀을 깨서 프라이팬에 넣는다
5. 2분간 굽는다
6. 소금을 한 꼬집 뿌린다
7. 접시에 담는다
```
→ 과정을 하나하나 지시

**비절차적 주문 (메뉴 주문)**:
```
"달걀 프라이 2인분 주세요"
```
→ 결과만 요청, 과정은 요리사에게 위임

**또 다른 비유 - 택시**:
- **절차적**: "여기서 출발해서 사거리에서 좌회전, 다음 신호등에서 우회전해서..."
- **비절차적**: "서울역으로 가주세요"

#### 3. 등장 배경 및 발전 과정

**1단계: 절차적 DML의 시대 (1960~1970년대)**
- IMS DL/1: 계층형 DB에서의 네비게이션 언어
- CODASYL DML: 망형 DB에서의 SET 네비게이션
- 특징: 레코드 단위 처리, 명시적 포인터 이동

**2단계: 비절차적 DML의 혁명 (1970년대)**
- 1970년: E.F. Codd의 관계형 모델 발표
- 1974년: IBM SEQUEL (Structured English Query Language)
- 1979년: Oracle 최초 상용 SQL DBMS
- 특징: 집합 단위 처리, 선언적 표현

**3단계: 절차적 확장의 등장 (1980~1990년대)**
- Oracle PL/SQL: SQL + 절차적 로직
- Sybase/SQL Server T-SQL: SQL + 제어문
- PostgreSQL PL/pgSQL
- 이유: 비즈니스 로직의 DB 내장

**4단계: 현대적 융합 (2000년대~현재)**
- SQL:1999/2003: 절차적 기능 표준화
- Stored Procedure, Trigger, User-Defined Function
- ORM + Native Query 하이브리드

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 절차적 vs 비절차적 DML 상세 비교 (표)

| 비교 항목 | 절차적 DML | 비절차적 DML (SQL) |
|:---|:---|:---|
| **접근 방식** | Navigation (네비게이션) | Association (연관) |
| **처리 단위** | Record-at-a-time | Set-at-a-time |
| **제어 구조** | Loop, If-Then-Else | WHERE, GROUP BY, HAVING |
| **데이터 독립성** | 낮음 (구조 종속) | 높음 (구조 독립) |
| **최적화** | 사용자 책임 | 옵티마이저 자동 |
| **버그 가능성** | 높음 (복잡한 로직) | 낮음 (간결한 표현) |
| **성능 튜닝** | 코드 변경 필요 | 인덱스/힌트로 가능 |
| **이식성** | 낮음 (DBMS 종속) | 높음 (SQL 표준) |
| **생산성** | 낮음 | 높음 |
| **적합 업무** | 복잡한 비즈니스 로직 | 대량 데이터 조회/조작 |

#### 2. 절차적 DML 처리 과정 다이어그램

```text
+============================================================================+
|                    PROCEDURAL DML EXECUTION FLOW                            |
+============================================================================+
|                                                                             |
|  [응용 프로그램]                                                             |
|       |                                                                     |
|       v                                                                     |
|  +---------------------------------------------------------------------+   |
|  |            1. 네비게이션 경로 설계 (사용자 책임)                        |   |
|  |                                                                      |   |
|  |  예: 학생 → 수강 → 과목 → 교수                                        |   |
|  |      루트에서 시작해 각 레코드를 순차적으로 방문                        |   |
|  +---------------------------------------------------------------------+   |
|       |                                                                     |
|       v                                                                     |
|  +---------------------------------------------------------------------+   |
|  |            2. 레코드 단위 처리 (Record-at-a-time)                      |   |
|  |                                                                      |   |
|  |  LOOP                                                                |   |
|  |    FETCH next_record                                                 |   |
|  |    IF condition THEN                                                 |   |
|  |       PROCESS record                                                 |   |
|  |    END IF                                                            |   |
|  |  END LOOP                                                            |   |
|  +---------------------------------------------------------------------+   |
|       |                                                                     |
|       v                                                                     |
|  +---------------------------------------------------------------------+   |
|  |            3. 물리적 포인터 따라 이동                                  |   |
|  |                                                                      |   |
|  |  Record A --ptr--> Record B --ptr--> Record C                        |   |
|  |                                                                      |   |
|  |  [성능] 포인터 직접 접근으로 빠름                                      |   |
|  |  [단점] 구조 변경 시 코드 수정 필요                                     |   |
|  +---------------------------------------------------------------------+   |
|                                                                             |
+============================================================================+

+============================================================================+
|                    NON-PROCEDURAL DML (SQL) EXECUTION                       |
+============================================================================+
|                                                                             |
|  [사용자 SQL]                                                                |
|       |                                                                     |
|       v                                                                     |
|  +---------------------------------------------------------------------+   |
|  |            1. 선언적 표현 (What, not How)                              |   |
|  |                                                                      |   |
|  |  SELECT emp_name, salary                                             |   |
|  |  FROM employees                                                      |   |
|  |  WHERE dept_id = 10 AND salary > 5000                                |   |
|  |                                                                      |   |
|  |  → "무엇을" 원하는지만 표현                                            |   |
|  +---------------------------------------------------------------------+   |
|       |                                                                     |
|       v                                                                     |
|  +---------------------------------------------------------------------+   |
|  |            2. 옵티마이저가 실행 계획 수립                               |   |
|  |                                                                      |   |
|  |  +----------------+    +----------------+    +----------------+      |   |
|  |  |  Parser        | -> |  Query Rewrite | -> |  Optimizer     |      |   |
|  |  |  (구문 분석)   |    |  (쿼리 변환)   |    |  (비용 계산)   |      |   |
|  |  +----------------+    +----------------+    +----------------+      |   |
|  |                                                      |               |   |
|  |                                                      v               |   |
|  |                                    +--------------------------------+  |   |
|  |                                    |  Execution Plan Selection       |  |   |
|  |                                    |  - Index Scan vs Full Scan     |  |   |
|  |                                    |  - Join Order & Method          |  |   |
|  |                                    |  - Parallel Execution           |  |   |
|  |                                    +--------------------------------+  |   |
|  +---------------------------------------------------------------------+   |
|       |                                                                     |
|       v                                                                     |
|  +---------------------------------------------------------------------+   |
|  |            3. 집합 단위 처리 (Set-at-a-time)                           |   |
|  |                                                                      |   |
|  |  +--------+  +--------+  +--------+  +--------+                      |   |
|  |  | Record1|  | Record5|  | Record8|  | Record12|   ← 조건 만족 행    |   |
|  |  +--------+  +--------+  +--------+  +--------+                      |   |
|  |       \           /           \          /                           |   |
|  |        \         /             \        /                            |   |
|  |         +-------+---------------+------+                             |   |
|  |                    |                                                   |   |
|  |                    v                                                   |   |
|  |            [Result Set]                                                |   |
|  +---------------------------------------------------------------------+   |
|                                                                             |
+============================================================================+
```

#### 3. 심층 동작 원리: 코드 비교

**시나리오**: 부서번호 10의 직원 중 급여가 5000 이상인 직원의 이름과 급여 조회

**1) 절차적 DML (IMS DL/1 스타일)**:
```cobol
* IMS DL/1 Procedural DML Example
* 학생-수강-과목 계층 구조에서 특정 조건의 데이터 조회

WORKING-STORAGE SECTION.
01  EMPLOYEE-RECORD.
    05 EMP-ID        PIC X(10).
    05 EMP-NAME      PIC X(30).
    05 DEPT-ID       PIC X(5).
    05 SALARY        PIC 9(7)V99.

01  SSA-LIST.
    05 FILLER        PIC X(20) VALUE 'DEPARTMENT(DEPT_ID=10)'.
    05 FILLER        PIC X(20) VALUE 'EMPLOYEE             '.

PROCEDURE DIVISION.
    * 1. 부모 부서 레코드 찾기
    MOVE 'DEPARTMENT(DEPT_ID=10)' TO SSA-DEPT.
    CALL 'CBLTDLI' USING GU, PCB, IOAREA, SSA-DEPT.
    IF DB-STATUS NOT = '  ' GO TO EXIT-PARA.

    * 2. 해당 부서의 첫 번째 직원 찾기
    CALL 'CBLTDLI' USING GN, PCB, IOAREA, 'EMPLOYEE'.

    * 3. 루프로 모든 직원 순회
    PERFORM UNTIL DB-STATUS NOT = '  '
        * 레코드 데이터 가져오기
        GET EMPLOYEE-RECORD

        * 조건 검사 (급여 >= 5000)
        IF SALARY >= 5000
            DISPLAY EMP-NAME ' ' SALARY
        END-IF

        * 다음 직원으로 이동
        CALL 'CBLTDLI' USING GN, PCB, IOAREA, 'EMPLOYEE'
    END-PERFORM.

EXIT-PARA.
    STOP RUN.
```

**2) 절차적 확장 SQL (PL/SQL 스타일)**:
```sql
-- PL/SQL: SQL에 절차적 로직 추가

DECLARE
    -- 커서 선언 (명시적 레코드 순회)
    CURSOR emp_cursor IS
        SELECT emp_name, salary
        FROM employees
        WHERE dept_id = 10;

    v_emp_name employees.emp_name%TYPE;
    v_salary   employees.salary%TYPE;
    v_count    NUMBER := 0;
    v_total    NUMBER := 0;

BEGIN
    -- 커서 열기
    OPEN emp_cursor;

    -- 루프로 레코드 순회
    LOOP
        -- 한 번에 한 레코드씩 가져오기
        FETCH emp_cursor INTO v_emp_name, v_salary;

        -- 더 이상 레코드가 없으면 종료
        EXIT WHEN emp_cursor%NOTFOUND;

        -- 조건 검사 (급여 >= 5000)
        IF v_salary >= 5000 THEN
            DBMS_OUTPUT.PUT_LINE(v_emp_name || ': ' || v_salary);
            v_count := v_count + 1;
            v_total := v_total + v_salary;
        END IF;

    END LOOP;

    -- 커서 닫기
    CLOSE emp_cursor;

    DBMS_OUTPUT.PUT_LINE('총 ' || v_count || '명, 평균 급여: ' || (v_total/v_count));

EXCEPTION
    WHEN OTHERS THEN
        IF emp_cursor%ISOPEN THEN
            CLOSE emp_cursor;
        END IF;
        RAISE;
END;
/
```

**3) 비절차적 DML (SQL)**:
```sql
-- 순수 SQL: 선언적 표현

-- 단순 조회
SELECT emp_name, salary
FROM employees
WHERE dept_id = 10 AND salary >= 5000;

-- 집계까지 한 번에
SELECT
    COUNT(*) AS emp_count,
    AVG(salary) AS avg_salary
FROM employees
WHERE dept_id = 10 AND salary >= 5000;

-- 윈도우 함수로 순위까지
SELECT
    emp_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM employees
WHERE dept_id = 10 AND salary >= 5000;
```

#### 4. 실무 수준의 절차적 vs 비절차적 비교

```python
"""
절차적 방식 vs 비절차적 방식 비교 구현
동일한 기능을 두 방식으로 구현
"""

import sqlite3
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Employee:
    emp_id: int
    emp_name: str
    dept_id: int
    salary: float

class ProceduralVsNonProcedural:
    """절차적 vs 비절차적 DML 비교"""

    def __init__(self, db_path: str = ':memory:'):
        self.conn = sqlite3.connect(db_path)
        self._setup_database()

    def _setup_database(self):
        """테스트 데이터베이스 생성"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INTEGER PRIMARY KEY,
                emp_name TEXT NOT NULL,
                dept_id INTEGER,
                salary REAL
            )
        """)

        # 테스트 데이터
        test_data = [
            (1, '홍길동', 10, 6000),
            (2, '김철수', 10, 4500),
            (3, '이영희', 10, 7000),
            (4, '박민수', 20, 5500),
            (5, '정수진', 10, 8000),
        ]
        cursor.executemany(
            "INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?)",
            test_data
        )
        self.conn.commit()

    # ==================== 절차적 방식 ====================

    def procedural_approach(self, dept_id: int, min_salary: float) -> List[Tuple]:
        """
        절차적 방식: 레코드를 하나씩 순회하며 조건 검사

        특징:
        - 명시적인 루프
        - 레코드 단위 처리
        - 로직이 코드에 드러남
        """
        cursor = self.conn.cursor()

        # 모든 레코드 가져오기 (필터링 없이)
        cursor.execute("SELECT emp_id, emp_name, dept_id, salary FROM employees")

        result = []

        # 명시적 루프로 각 레코드 처리
        for row in cursor:
            emp = Employee(*row)

            # 조건 검사를 코드로 명시
            if emp.dept_id == dept_id and emp.salary >= min_salary:
                # 로직 수행
                result.append((emp.emp_name, emp.salary))

        return result

    def procedural_with_cursor(self, dept_id: int, min_salary: float) -> List[Tuple]:
        """
        절차적 방식: 커서를 이용한 명시적 제어
        """
        cursor = self.conn.cursor()

        # 커서 선언
        cursor.execute("SELECT emp_id, emp_name, dept_id, salary FROM employees")

        result = []
        row_count = 0
        match_count = 0

        # 명시적 FETCH 루프
        while True:
            row = cursor.fetchone()  # 한 번에 한 행씩
            if row is None:
                break  # 더 이상 레코드 없음

            row_count += 1
            emp = Employee(*row)

            # 조건 검사
            if emp.dept_id == dept_id and emp.salary >= min_salary:
                match_count += 1
                # 복잡한 로직 수행 가능
                bonus = emp.salary * 0.1 if emp.salary > 7000 else emp.salary * 0.05
                result.append((emp.emp_name, emp.salary, bonus))

        print(f"처리된 행: {row_count}, 조건 일치: {match_count}")
        return result

    # ==================== 비절차적 방식 ====================

    def non_procedural_approach(self, dept_id: int, min_salary: float) -> List[Tuple]:
        """
        비절차적 방식: SQL로 원하는 결과만 선언

        특징:
        - 루프 없음
        - 집합 단위 처리
        - 로직은 SQL 엔진이 처리
        - 선언적 표현
        """
        cursor = self.conn.cursor()

        # 무엇을 원하는지만 선언
        cursor.execute("""
            SELECT emp_name, salary
            FROM employees
            WHERE dept_id = ? AND salary >= ?
        """, (dept_id, min_salary))

        # 결과 집합 반환
        return cursor.fetchall()

    def non_procedural_with_aggregation(self, dept_id: int, min_salary: float) -> dict:
        """
        비절차적 방식: 복잡한 집계도 한 번에
        """
        cursor = self.conn.cursor()

        # 모든 계산을 SQL에 위임
        cursor.execute("""
            SELECT
                COUNT(*) AS emp_count,
                AVG(salary) AS avg_salary,
                MAX(salary) AS max_salary,
                MIN(salary) AS min_salary,
                SUM(salary) AS total_salary
            FROM employees
            WHERE dept_id = ? AND salary >= ?
        """, (dept_id, min_salary))

        row = cursor.fetchone()
        return {
            'emp_count': row[0],
            'avg_salary': row[1],
            'max_salary': row[2],
            'min_salary': row[3],
            'total_salary': row[4]
        }

    def non_procedural_with_window_function(self, dept_id: int, min_salary: float) -> List[Tuple]:
        """
        비절차적 방식: 윈도우 함수로 순위 계산까지
        """
        cursor = self.conn.cursor()

        # 복잡한 계산도 선언적 표현
        cursor.execute("""
            SELECT
                emp_name,
                salary,
                RANK() OVER (ORDER BY salary DESC) AS salary_rank,
                PERCENTILE_RANK() OVER (ORDER BY salary) AS percentile,
                SUM(salary) OVER (PARTITION BY dept_id) AS dept_total
            FROM employees
            WHERE dept_id = ? AND salary >= ?
            ORDER BY salary DESC
        """, (dept_id, min_salary))

        return cursor.fetchall()

# 비교 실행
if __name__ == '__main__':
    db = ProceduralVsNonProcedural()

    print("=" * 60)
    print("절차적 방식 결과:")
    print("=" * 60)
    procedural_result = db.procedural_with_cursor(10, 5000)
    for row in procedural_result:
        print(f"  {row}")

    print("\n" + "=" * 60)
    print("비절차적 방식 결과:")
    print("=" * 60)
    non_procedural_result = db.non_procedural_approach(10, 5000)
    for row in non_procedural_result:
        print(f"  {row}")

    print("\n" + "=" * 60)
    print("비절차적 방식 + 집계:")
    print("=" * 60)
    agg_result = db.non_procedural_with_aggregation(10, 5000)
    print(f"  {agg_result}")

    print("\n" + "=" * 60)
    print("비절차적 방식 + 윈도우 함수:")
    print("=" * 60)
    window_result = db.non_procedural_with_window_function(10, 5000)
    for row in window_result:
        print(f"  {row}")

    print("\n" + "=" * 60)
    print("코드 라인 수 비교:")
    print("=" * 60)
    print(f"  절차적 방식: 약 25줄 (루프, 조건문, 변수 관리)")
    print(f"  비절차적 방식: 약 5줄 (SQL 문장만)")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 절차적 vs 비절차적 성능 비교

| 비교 항목 | 절차적 DML | 비절차적 DML (SQL) | 비고 |
|:---|:---|:---|:---|
| **네트워크 왕복** | 많음 (레코드당) | 적음 (한 번) | SQL 유리 |
| **DBMS 최적화** | 불가능 | 가능 (옵티마이저) | SQL 유리 |
| **메모리 사용** | 클라이언트 부담 | DB 서버 부담 | 상황별 다름 |
| **복잡한 로직** | 유리 (세밀한 제어) | 제한적 | 절차적 유리 |
| **일괄 처리** | 느림 | 빠름 | SQL 유리 |
| **트랜잭션 관리** | 명시적 | 암시적 | 상황별 다름 |

#### 2. 언제 절차적 DML을 쓸 것인가?

**절차적 DML이 유리한 경우**:
1. 복잡한 비즈니스 로직 (조건문, 반복문 많음)
2. 행 단위 트리거 로직
3. 예외 처리가 많은 로직
4. DBMS 간 이식성이 중요하지 않은 경우
5. 성능 최적화를 직접 제어해야 하는 경우

**비절차적 DML이 유리한 경우**:
1. 대량 데이터 조회/조작
2. 집계, 그룹핑, 정렬
3. 간단한 CRUD 연산
4. DBMS 독립적인 코드 필요
5. 개발 생산성 중시

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 복잡한 계산 로직**
- 상황: 급여 계산 (세금, 보너스, 공제 등 복잡한 규칙)
- 판단: 비즈니스 로직은 절차적으로, 데이터 조회는 비절차적으로
- 전략:
  - SQL로 데이터 조회
  - PL/SQL 또는 애플리케이션에서 계산
  - SQL로 결과 저장

**시나리오 2: 대량 데이터 마이그레이션**
- 상황: 1억 건의 데이터 변환
- 판단: 비절차적 방식 (SQL 한 방 쿼리)
- 전략:
  - INSERT INTO ... SELECT 구문
  - 병렬 처리 활성화
  - 배치 커밋

**시나리오 3: 행 단위 검증**
- 상황: 각 행마다 다른 규칙 적용
- 판단: 절차적 방식 (커서)
- 전략:
  - 커서로 순회
  - 행별로 다른 로직 적용
  - 예외 처리

#### 2. 도입 시 고려사항 (체크리스트)

**절차적 DML 선택 기준**:
- [ ] 행 단위로 다른 로직이 필요한가?
- [ ] 복잡한 예외 처리가 필요한가?
- [ ] DBMS 최적화보다 직접 제어가 필요한가?
- [ ] 기존 절차적 코드와의 통합이 필요한가?

**비절차적 DML 선택 기준**:
- [ ] 대량 데이터를 처리하는가?
- [ ] 로직이 단순한가?
- [ ] DBMS 간 이식성이 중요한가?
- [ ] 개발 속도가 중요한가?

#### 3. 안티패턴 (Anti-patterns)

1. **SQL로 모든 것을**: 복잡한 로직을 SQL로 억지로 표현
   - 해결: 복잡한 로직은 PL/SQL 또는 애플리케이션으로

2. **절차적 과다 사용**: 단순 조회도 커서로 처리
   - 해결: 집합 연산으로 변경

3. **네트워크 왕복 최소화 무시**: 레코드마다 쿼리 실행
   - 해결: JOIN, 서브쿼리로 한 번에

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 절차적 DML | 비절차적 DML | 개선 효과 |
|:---|:---|:---|:---|
| **코드 라인 수** | 100줄 | 10줄 | 90% 감소 |
| **개발 시간** | 1일 | 1시간 | 8배 단축 |
| **성능 (대량)** | 느림 | 빠름 | 10~100배 |
| **유지보수성** | 낮음 | 높음 | 용이 |

#### 2. 미래 전망 및 진화 방향

**비절차적 DML의 진화**:
- **SQL:2016/2023**: JSON, Graph, AI 확장
- **LLM + SQL**: 자연어에서 SQL 자동 생성

**절차적 DML의 진화**:
- **WebAssembly in DB**: 브라우저 독립적 절차적 코드
- **Python in PostgreSQL**: PL/Python 확장

**하이브리드 접근**:
- **SQL + UDF**: 선언적 + 절차적 결합
- **ORM + Native Query**: 추상화 + 제어 결합

#### 3. 참고 표준/가이드

| 표준 | 내용 | 적용 범위 |
|:---|:---|:---|
| **ANSI/ISO SQL** | 비절차적 DML 표준 | 모든 RDBMS |
| **SQL/PSM** | 절차적 SQL 표준 | Stored Procedure |
| **PL/SQL** | Oracle 절차적 확장 | Oracle DB |
| **T-SQL** | SQL Server 절차적 확장 | MS SQL Server |

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[DML](@/studynotes/5_database/1_relational/18_ddl_dml_dcl_tcl.md)**: 데이터 조작어의 기본
- **[옵티마이저](@/studynotes/5_database/3_optimization/query_optimization.md)**: 비절차적 DML의 최적화 엔진
- **[관계 대수](@/studynotes/5_database/1_relational/relational_algebra.md)**: 비절차적 언어의 이론적 기반
- **[Stored Procedure](@/studynotes/5_database/2_sql/stored_procedure.md)**: 절차적 확장의 현대적 구현

---

### 👶 어린이를 위한 3줄 비유 설명

1. **요리법 vs 배달 앱**: 요리법은 "이렇게 하고 저렇게 하고" 하나하나 알려주죠? 이게 절차적이에요. 배달 앱은 "치킨 한 마리요"라고만 하면 되죠? 이게 비절차적이에요!

2. **네비게이션 vs 지도**: 지도를 보고 직접 길을 찾는 건 절차적이에요. "여기서 좌회전, 저기서 우회전"이라고요. 내비게이션은 목적지만 입력하면 최적 경로를 알아서 찾아줘요. 이게 비절차적이에요!

3. **장난감 정리**: "장난감 하나를 집어서 상자에 넣고, 또 하나 집어서 넣고..."라고 하는 건 절차적이에요. "장난감을 다 상자에 넣어!"라고 하는 건 비절차적이에요. SQL은 후자예요!
