+++
title = "7. 외부 스키마 (External Schema)"
description = "사용자 관점의 데이터베이스 뷰와 서브스키마"
date = "2026-03-05"
[taxonomies]
tags = ["external-schema", "view", "subschema", "data-independence", "user-perspective"]
categories = ["studynotes-5_database"]
+++

# 7. 외부 스키마 (External Schema)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 외부 스키마는 개별 사용자나 응용 프로그램이 데이터베이스를 바라보는 관점(View)을 정의한 것으로, 전체 데이터 중 사용자에게 필요한 부분만을 보여주는 논리적 부분집합입니다.
> 2. **가치**: 외부 스키마는 데이터 보안(민감정보 은닉), 단순화(복잡성 숨김), 독립성(논리적 변경 격리)을 제공하여 사용자별 맞춤 데이터 접근을 가능하게 합니다.
> 3. **융합**: 현대 시스템에서는 API 응답 모델, GraphQL 스키마, 마이크로서비스 DTO 등으로 외부 스키마 개념이 확장 적용되고 있습니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**외부 스키마(External Schema)**는 ANSI/SPARC 3단계 아키텍처에서 최상위 계층에 위치하며, 개별 사용자나 응용 프로그램이 데이터베이스를 인식하는 방식을 정의합니다. 서브스키마(Sub-schema) 또는 사용자 뷰(User View)라고도 불립니다.

**외부 스키마의 핵심 특성**:

1. **사용자 중심**: 각 사용자 그룹의 업무 요구사항에 맞는 데이터만 제공
2. **부분 집합**: 전체 데이터베이스의 일부분만 포함
3. **다양성**: 동일 데이터에 대해 사용자별로 다른 관점 제공
4. **보안**: 민감한 데이터 컬럼/행에 대한 접근 제어
5. **단순화**: 복잡한 조인, 계산 로직 숨김

**외부 스키마 구현 방식**:
- **뷰(View)**: RDBMS에서 가장 일반적인 구현
- **동의어(Synonym)**: 객체 이름의 별칭
- **가상 테이블(Virtual Table)**: 물리적 저장 없는 논리적 테이블

#### 2. 비유를 통한 이해

**백화점 층별 안내도**로 비유:

```
백화점 전체 (개념 스키마)
- 1~10층, 수천 개의 매장

각 고객이 보는 것 (외부 스키마):
- 쇼핑 고객: 1층 화장품, 2층 여성의류, 3층 남성의류
- 식사 고객: 지하 식당가, 10층 푸드코트
- 직원: 사원용 엘리베이터, 탈의실, 창고
```

각 사용자는 자신에게 필요한 정보만 접근하며, 나머지는 존재를 알지 못합니다.

#### 3. 등장 배경

**문제 상황**:
- 모든 사용자가 전체 데이터베이스 구조를 이해해야 함
- 보안상 민감한 데이터 노출 위험
- 데이터 구조 변경 시 모든 사용자 영향

**해결책으로서 외부 스키마**:
- 사용자별 맞춤 데이터 관점 제공
- 데이터 추상화와 보안 계층 확보
- 논리적 데이터 독립성 실현

---

### II. 아키텍처 및 핵심 원리

#### 1. 외부 스키마 구성 요소 (표)

| 구성 요소 | 설명 | 예시 |
|:---|:---|:---|
| **뷰 정의** | SELECT 문으로 정의된 가상 테이블 | CREATE VIEW ... AS SELECT ... |
| **컬럼 부분집합** | 필요한 컬럼만 선택 | 개인정보에서 연락처만 노출 |
| **행 부분집합** | 조건에 맞는 행만 선택 | 부서별 데이터 분리 |
| **파생 컬럼** | 계산된 가상 컬럼 | 할인율, 합계 등 |
| **데이터 변환** | 포맷팅, 마스킹 | 주민번호 뒷자리 * 처리 |

#### 2. 외부 스키마 다이어그램

```text
+================================================================================+
|                        EXTERNAL SCHEMA ARCHITECTURE                             |
+================================================================================+
|                                                                                 |
|  [개념 스키마: 전체 데이터베이스]                                                 |
|                                                                                 |
|  +------------------+     +------------------+     +------------------+        |
|  | EMPLOYEES        |     | SALARIES         |     | DEPARTMENTS      |        |
|  +------------------+     +------------------+     +------------------+        |
|  | emp_id (PK)      |     | emp_id (FK)      |     | dept_id (PK)     |        |
|  | name             |     | base_salary      |     | dept_name        |        |
|  | ssn              |     | bonus            |     | location         |        |
|  | dept_id (FK)     |     | effective_date   |     | manager_id       |        |
|  | hire_date        |     +------------------+     +------------------+        |
|  | address          |                                                          |
|  | phone            |                                                          |
|  +------------------+                                                          |
|                                                                                 |
|         |                    |                    |                            |
|         v                    v                    v                            |
|                                                                                 |
|  +---------------------------외부 스키마------------------------------------+    |
|  |                                                                          |    |
|  |  [영업팀 뷰]              [인사팀 뷰]            [경리팀 뷰]              |    |
|  |  +-----------------+    +-----------------+    +-----------------+        |    |
|  |  | sales_emp_view  |    | hr_emp_view     |    | payroll_view    |        |    |
|  |  +-----------------+    +-----------------+    +-----------------+        |    |
|  |  | emp_id          |    | emp_id          |    | emp_id          |        |    |
|  |  | name            |    | name            |    | name            |        |    |
|  |  | dept_name       |    | dept_name       |    | dept_name       |        |    |
|  |  | phone           |    | hire_date       |    | total_salary    |        |    |
|  |  +-----------------+    | address         |    | bonus           |        |    |
|  |                         | (SSN 마스킹)    |    +-----------------+        |    |
|  |  (민감정보 제외)        +-----------------+    (급여 정보만)              |    |
|  |                         (인사 관련 정보)                                  |    |
|  +--------------------------------------------------------------------------+    |
|                                                                                 |
|  [관리자 뷰]                         [외부 파트너 뷰]                          |
|  +-------------------------------+    +-------------------------------+          |
|  | manager_dashboard_view        |    | partner_customer_view        |          |
|  +-------------------------------+    +-------------------------------+          |
|  | department                    |    | customer_name                |          |
|  | employee_count                |    | order_summary                |          |
|  | total_salary_budget           |    | (개인정보 완전 제외)          |          |
|  | avg_performance_score         |    +-------------------------------+          |
|  +-------------------------------+                                              |
+================================================================================+
```

#### 3. 심층 동작 원리

**뷰 생성과 쿼리 변환 과정**:

```sql
-- 1. 개념 스키마 (기본 테이블)
CREATE TABLE employees (
    emp_id      NUMBER PRIMARY KEY,
    name        VARCHAR2(100),
    ssn         VARCHAR2(14),      -- 주민등록번호
    dept_id     NUMBER,
    hire_date   DATE,
    base_salary NUMBER(10,2),
    phone       VARCHAR2(20)
);

-- 2. 외부 스키마 정의 (뷰)
CREATE VIEW hr_emp_view AS
SELECT
    emp_id,
    name,
    -- SSN 마스킹
    SUBSTR(ssn, 1, 6) || '-*******' AS masked_ssn,
    dept_id,
    hire_date,
    -- 연봉 등급으로 변환
    CASE
        WHEN base_salary >= 100000 THEN 'S'
        WHEN base_salary >= 70000 THEN 'A'
        WHEN base_salary >= 50000 THEN 'B'
        ELSE 'C'
    END AS salary_grade,
    phone
FROM employees
WHERE dept_id IN (SELECT dept_id FROM departments WHERE active = 'Y');

-- 3. 사용자 쿼리
SELECT name, salary_grade
FROM hr_emp_view
WHERE hire_date >= '2024-01-01';

-- 4. DBMS 내부 변환 (뷰 확장)
SELECT name,
    CASE
        WHEN base_salary >= 100000 THEN 'S'
        WHEN base_salary >= 70000 THEN 'A'
        WHEN base_salary >= 50000 THEN 'B'
        ELSE 'C'
    END AS salary_grade
FROM employees
WHERE dept_id IN (SELECT dept_id FROM departments WHERE active = 'Y')
  AND hire_date >= TO_DATE('2024-01-01', 'YYYY-MM-DD');
```

#### 4. 핵심 알고리즘: 뷰 병합 (View Merging)

```python
"""
뷰 병합 알고리즘 (View Merging)
- 옵티마이저가 뷰 쿼리를 기본 테이블 쿼리로 변환
"""

class ViewMerger:
    """뷰를 기본 테이블 쿼리로 병합하는 옵티마이저 컴포넌트"""

    def merge_view(self, outer_query: dict, view_definition: dict) -> dict:
        """
        뷰 참조를 실제 테이블 참조로 변환
        """
        result = {
            'select_columns': [],
            'from_tables': [],
            'where_conditions': [],
            'group_by': [],
            'having': None,
            'order_by': []
        }

        # 1. SELECT 컬럼 병합
        result['select_columns'] = self._merge_select(
            outer_query['select_columns'],
            view_definition['select_columns']
        )

        # 2. FROM 테이블 병합
        result['from_tables'] = view_definition['from_tables']

        # 3. WHERE 조건 병합 (Predicate Pushdown)
        result['where_conditions'] = (
            view_definition['where_conditions'] +
            outer_query['where_conditions']
        )

        # 4. GROUP BY 병합
        if view_definition['group_by']:
            result['group_by'] = view_definition['group_by']

        # 5. ORDER BY 전파
        result['order_by'] = outer_query['order_by']

        return result

    def _merge_select(self, outer_cols: list, view_cols: list) -> list:
        """외부 쿼리의 SELECT를 뷰 정의와 매핑"""
        merged = []
        for col in outer_cols:
            if col in view_cols:
                # 뷰의 컬럼 정의로 대체
                merged.append(view_cols[col])
            else:
                merged.append(col)
        return merged
```

---

### III. 융합 비교 및 다각도 분석

#### 1. 외부 스키마 vs 개념 스키마 비교

| 비교 항목 | 외부 스키마 | 개념 스키마 |
|:---|:---|:---|
| **대상** | 개별 사용자/앱 | 조직 전체 |
| **범위** | 데이터 부분집합 | 전체 데이터 |
| **개수** | 여러 개 가능 | 1개 |
| **보안** | 민감정보 은닉 | 전체 정보 포함 |
| **목적** | 사용자 편의성 | 데이터 통합 관리 |

#### 2. 뷰의 종류별 특징

| 뷰 종류 | 정의 | 특징 | 용도 |
|:---|:---|:---|:---|
| **단순 뷰** | 단일 테이블 기반 | DML 가능 | 컬럼 선택, 행 필터링 |
| **복합 뷰** | 조인, 집계 포함 | DML 제한 | 복잡한 쿼리 단순화 |
| **인라인 뷰** | FROM 절 서브쿼리 | 일회용 | 동적 데이터 처리 |
| **구체화된 뷰** | 물리적 저장 | 성능 향상 | 대용량 집계 |

---

### IV. 실무 적용 및 기술사적 판단

#### 1. 실무 시나리오

**시나리오 1: 개인정보 보호**
- **요구사항**: 고객 SSN, 연락처 마스킹
- **해결**: 뷰에서 SUBSTR, REPLACE 함수로 마스킹
- **결과**: 일반 사용자는 마스킹된 데이터만 접근

**시나리오 2: 부서별 데이터 격리**
- **요구사항**: 영업팀은 자사 고객만 조회
- **해결**: 뷰에 WHERE dept_id = USER_DEPT 조건
- **결과**: 행 수준 보안(Row-Level Security) 구현

**시나리오 3: 복잡한 쿼리 단순화**
- **요구사항**: 5개 테이블 조인 분석 쿼리
- **해결**: 뷰로 조인 로직 캡슐화
- **결과**: 사용자는 단순 SELECT만 수행

#### 2. 안티패턴

1. **뷰 중첩(Chained Views)**: 뷰 위에 뷰 생성 시 성능 저하
2. **과도한 뷰**: 모든 테이블에 뷰 생성은 오버헤드
3. **복잡한 뷰 DML**: 집계/조인 뷰의 무분별한 DML 시도

---

### V. 기대효과 및 결론

#### 1. 기대효과

| 구분 | 도입 전 | 도입 후 |
|:---|:---|:---|
| **데이터 보안** | 모든 컬럼 노출 | 민감정보 은닉 |
| **쿼리 복잡도** | 높음 | 낮음 |
| **변경 영향** | 전체 사용자 | 뷰만 수정 |

#### 2. 참고 표준

- ANSI/SPARC 3-Level Architecture
- ISO/IEC 9075 (SQL View)

---

### 관련 개념 맵

- **[데이터 독립성](@/studynotes/5_database/1_relational/4_data_independence.md)**: 외부 스키마가 제공하는 독립성
- **[뷰](@/studynotes/5_database/2_sql/view.md)**: 외부 스키마의 SQL 구현
- **[3단계 스키마](@/studynotes/5_database/1_relational/6_three_schema_architecture.md)**: 전체 아키텍처

---

### 어린이를 위한 3줄 비유

1. **맞춤형 메뉴판**: 친구가 땅콩 알레르기가 있으면 땅콩 없는 메뉴만 보여주는 메뉴판을 만들어줄 수 있어요. 외부 스키마는 이렇게 각 사람에게 맞는 정보만 보여주는 특별한 메뉴판이에요!

2. **학급 신문**: 학급 신문에는 우리 반 소식만 나오죠? 전교생 소식이 아니라. 외부 스키마도 이렇게 사용자가 필요한 정보만 골라서 보여줘요!

3. **비밀 다이어리 키**: 다이어리에 비밀번호를 걸면 내용 중 일부만 보이게 할 수 있어요. 외부 스키마는 이렇게 중요한 건 숨기고 필요한 것만 보여주는 마법 키예요!
