+++
title = "5. 스키마 (Schema)"
description = "데이터베이스 스키마의 정의, 유형 및 설계 원칙"
date = "2026-03-05"
[taxonomies]
tags = ["schema", "database-design", "ddl", "metadata", "data-model"]
categories = ["studynotes-5_database"]
+++

# 5. 스키마 (Schema)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스키마는 데이터베이스의 논리적 구조와 제약조건을 명세한 메타데이터로, 데이터가 어떻게 조직되고 저장되며 어떤 규칙을 따라야 하는지를 정의하는 청사진입니다.
> 2. **가치**: 잘 설계된 스키마는 데이터 무결성을 99% 이상 보장하고, 쿼리 성능을 50~200% 향상시키며, 유지보수 비용을 60% 이상 절감합니다.
> 3. **융합**: 스키마 레지스트리, 스키마리스 NoSQL, GraphQL 스키마, Protocol Buffers 등으로 진화하며 분산 시스템과 API 계층으로 개념이 확장되고 있습니다.

---

### I. 개요 (Context & Background) - [최소 500자 이상]

#### 1. 개념 및 기술적 정의

**스키마(Schema)**란 데이터베이스에 저장되는 데이터의 구조, 데이터 타입, 제약조건, 그리고 데이터 간의 관계를 정의한 명세서입니다. 스키마는 데이터베이스의 '설계도' 또는 '청사진' 역할을 하며, DBMS가 데이터를 어떻게 저장하고 관리할지를 결정합니다.

**스키마의 구성 요소 (3요소)**:

1. **구조 (Structure)**: 데이터의 논리적 형태와 관계
   - 릴레이션(테이블), 속성(컬럼), 튜플(행)
   - 개체 간의 관계 (1:1, 1:N, M:N)

2. **연산 (Operation)**: 데이터 조작 방법
   - 검색, 삽입, 삭제, 갱신 연산
   - 관계 대수, 관계 해석

3. **제약조건 (Constraint)**: 데이터 무결성 규칙
   - 개체 무결성 (Primary Key)
   - 참조 무결성 (Foreign Key)
   - 도메인 무결성 (Data Type, CHECK)
   - 사용자 정의 무결성 (Trigger, Rule)

**스키마 vs 인스턴스**:
- **스키마 (Schema/Intension/내포)**: 데이터베이스의 구조 - 정적, 자주 변하지 않음
- **인스턴스 (Instance/Extension/외연)**: 특정 시점의 실제 데이터 - 동적, 지속적 변화

```
스키마 (구조):
CREATE TABLE students (
    student_id NUMBER PRIMARY KEY,
    name VARCHAR2(50) NOT NULL,
    major VARCHAR2(30)
);

인스턴스 (데이터):
INSERT INTO students VALUES (1, '홍길동', '컴퓨터공학');
INSERT INTO students VALUES (2, '김철수', '경영학');
```

#### 2. 비유를 통한 이해

**건축 설계도**로 비유할 수 있습니다:

| 스키마 개념 | 건축 비유 |
|:---|:---|
| 스키마 | 건물 설계도 (청사진) |
| 인스턴스 | 실제 건물과 거주자들 |
| DDL | 설계도 작성 도구 |
| 제약조건 | 건축 법규, 안전 기준 |
| 메타데이터 | 건물 정보 (면적, 층수, 용도) |

#### 3. 등장 배경 및 발전 과정

**1단계: 파일 시스템 (스키마 개념 없음)** - 응용 프로그램이 파일 구조에 직접 의존

**2단계: 초기 DBMS (물리적 스키마)** - 계층형, 망형 모델에서 물리적 구조 정의

**3단계: 관계형 모델 (3단계 스키마)** - ANSI/SPARC 3단계 스키마 제안 (1975)

**4단계: 객체지향 확장** - 클래스 다이어그램, UML, ORM

**5단계: 스키마리스와 진화** - NoSQL, GraphQL 스키마, Protocol Buffers

---

### II. 아키텍처 및 핵심 원리 (Deep Dive) - [최소 1,000자 이상]

#### 1. 스키마 유형 및 구성 (표)

| 스키마 유형 | 계층 | 정의 | 관리 주체 | 변경 빈도 |
|:---|:---|:---|:---|:---|
| **외부 스키마** | 사용자 | 개별 사용자/앱 관점의 뷰 | 응용 개발자 | 낮음 |
| **개념 스키마** | 조직 | 전체 논리 구조 | DBA | 중간 |
| **내부 스키마** | 시스템 | 물리적 저장 구조 | 시스템 엔지니어 | 높음 |

#### 2. 정교한 스키마 구조 다이어그램

```text
+================================================================================+
|                        DATABASE SCHEMA ARCHITECTURE                             |
+================================================================================+
|                                                                                 |
|  +---------------------------------------------------------------------------+ |
|  |                        CONCEPTUAL SCHEMA (개념 스키마)                      | |
|  |                                                                           | |
|  |  +----------+     +----------+     +----------+     +----------+          | |
|  |  | CUSTOMER |     | ORDER    |     | PRODUCT  |     | EMPLOYEE |          | |
|  |  +----------+     +----------+     +----------+     +----------+          | |
|  |  | PK: id   |     | PK: id   |     | PK: id   |     | PK: id   |          | |
|  |  | name     |     | FK: cust_|     | name     |     | name     |          | |
|  |  | email    |     | order_dt |     | price    |     | dept_id  |          | |
|  |  | phone    |     | total    |     | category |     | salary   |          | |
|  |  | status   |     | status   |     | stock    |     | hire_dt  |          | |
|  |  +----------+     +----------+     +----------+     +----------+          | |
|  |                                                                           | |
|  |  [제약조건 Constraints]                                                    | |
|  |  PRIMARY KEY (id)                                                         | |
|  |  FOREIGN KEY (customer_id) REFERENCES customer(id)                        | |
|  |  CHECK (salary > 0)                                                       | |
|  |  UNIQUE (email)                                                           | |
|  |  NOT NULL (name)                                                          | |
|  +---------------------------------------------------------------------------+ |
|                                                                                 |
|  +---------------------------------------------------------------------------+ |
|  |                        EXTERNAL SCHEMAS (외부 스키마)                       | |
|  |  +------------------------+    +------------------------+                 | |
|  |  | sales_customer_view    |    | hr_employee_view       |                 | |
|  |  +------------------------+    +------------------------+                 | |
|  |  | customer_id            |    | employee_id            |                 | |
|  |  | customer_name          |    | employee_name          |                 | |
|  |  | order_count            |    | department_name        |                 | |
|  |  | total_purchase         |    | salary_grade           |                 | |
|  |  +------------------------+    +------------------------+                 | |
|  +---------------------------------------------------------------------------+ |
|                                                                                 |
|  +---------------------------------------------------------------------------+ |
|  |                        INTERNAL SCHEMA (내부 스키마)                        | |
|  |  [Storage Structure]                                                      | |
|  |  +------------------+  +------------------+  +------------------+          | |
|  |  | Tablespace: USERS|  | Tablespace: INDEX|  | Tablespace: LOG  |          | |
|  |  | Size: 100GB      |  | Size: 50GB       |  | Size: 20GB       |          | |
|  |  +------------------+  +------------------+  +------------------+          | |
|  |  [Index Structure]                                                        | |
|  |  | PK_CUSTOMER_ID: B+Tree, Height 3, Leaf Blocks 5000                     | |
|  |  | IDX_CUSTOMER_EMAIL: Hash, Buckets 10000                                | |
|  |  | IDX_ORDER_DATE: Bitmap, Compressed                                     | |
|  +---------------------------------------------------------------------------+ |
+================================================================================+
```

#### 3. 심층 동작 원리: DDL 처리 과정

**DDL 문장 처리 7단계**:

```sql
CREATE TABLE employees (
    emp_id      NUMBER(10) PRIMARY KEY,
    emp_name    VARCHAR2(100) NOT NULL,
    dept_id     NUMBER(5) REFERENCES departments(dept_id),
    salary      NUMBER(10,2) CHECK (salary > 0),
    hire_date   DATE DEFAULT SYSDATE,
    email       VARCHAR2(100) UNIQUE
);
```

**단계 1: 구문 분석 (Parsing)** - Parse Tree 생성

**단계 2: 의미 분석 (Semantic Analysis)** - 데이터 타입 유효성, 참조 테이블 존재 확인

**단계 3: 메타데이터 갱신 (Catalog Update)** - System Catalog에 테이블/컬럼 정보 기록

**단계 4: 물리적 공간 할당 (Space Allocation)** - Tablespace에서 Extent 할당

**단계 5: 인덱스 생성 (Index Creation)** - PK, Unique 인덱스 자동 생성

**단계 6: 트리거/기본값 처리** - DEFAULT 값 설정

**단계 7: DDL 완료 및 커밋** - 암시적 커밋, 권한 부여

#### 4. 핵심 알고리즘: 스키마 검증 (Schema Validation)

```python
"""
스키마 검증 알고리즘
- DML 실행 전 제약조건 검사
"""

import re
from typing import Tuple, Optional

class SchemaValidator:
    """데이터 무결성 제약조건 검증기"""

    def __init__(self, schema_catalog):
        self.catalog = schema_catalog

    def validate_insert(self, table_name: str, record: dict) -> Tuple[bool, Optional[str]]:
        """
        INSERT 전 제약조건 검증
        Returns: (is_valid, error_message)
        """
        schema = self.catalog.get_table_schema(table_name)

        # 1. NOT NULL 검증
        for column, constraints in schema['columns'].items():
            if constraints.get('nullable') == False:
                if column not in record or record[column] is None:
                    return (False, f"NULL value not allowed for {column}")

        # 2. Data Type 검증
        for column, value in record.items():
            col_type = schema['columns'][column]['data_type']
            if not self._validate_type(value, col_type):
                return (False, f"Type mismatch for {column}")

        # 3. CHECK 제약조건 검증
        for constraint in schema.get('check_constraints', []):
            if not self._evaluate_check(record, constraint['expression']):
                return (False, f"Check constraint violated: {constraint['name']}")

        # 4. UNIQUE 제약조건 검증 (DB 조회 필요)
        for constraint in schema.get('unique_constraints', []):
            if self._exists_unique_violation(table_name, constraint, record):
                return (False, f"Unique constraint violated: {constraint['name']}")

        # 5. Primary Key 검증
        pk_columns = schema['primary_key']['columns']
        pk_values = tuple(record[col] for col in pk_columns)
        if self._exists_pk(table_name, pk_values):
            return (False, "Primary key violation")

        # 6. Foreign Key 검증 (참조 무결성)
        for fk in schema.get('foreign_keys', []):
            fk_values = [record[col] for col in fk['columns']]
            if not self._exists_reference(fk['ref_table'], fk['ref_columns'], fk_values):
                return (False, f"Foreign key violation: {fk['name']}")

        return (True, None)

    def _validate_type(self, value, data_type: str) -> bool:
        """데이터 타입 검증"""
        type_validators = {
            'NUMBER': lambda v: isinstance(v, (int, float)),
            'VARCHAR2': lambda v: isinstance(v, str),
            'DATE': lambda v: isinstance(v, str),  # 문자열로 날짜 표현
            'BOOLEAN': lambda v: isinstance(v, bool),
        }
        base_type = data_type.split('(')[0]
        return type_validators.get(base_type, lambda v: True)(value)

    def _evaluate_check(self, record: dict, expression: str) -> bool:
        """
        CHECK 제약조건 평가 - 안전한 파싱 방식
        SQL Injection 방지를 위해 정규식 기반 파싱 사용
        """
        # 간단한 비교 패턴 매칭: "salary > 0", "status = 'A'"
        pattern = r"(\w+)\s*(>|<|=|>=|<=|!=|<>)\s*(\d+\.?\d*|'[^']*')"
        match = re.match(pattern, expression.strip())

        if not match:
            return True  # 지원하지 않는 표현식은 통과

        column, operator, value = match.groups()
        col_value = record.get(column)

        if col_value is None:
            return True  # NULL인 경우 CHECK 제약 조건 평가 안함

        # 문자열 값 처리
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
            col_value = str(col_value)
        else:
            value = float(value) if '.' in value else int(value)
            col_value = float(col_value) if isinstance(col_value, float) else int(col_value)

        # 연산 수행
        ops = {
            '>': lambda a, b: a > b,
            '<': lambda a, b: a < b,
            '=': lambda a, b: a == b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b,
            '!=': lambda a, b: a != b,
            '<>': lambda a, b: a != b,
        }

        return ops.get(operator, lambda a, b: True)(col_value, value)

    def _exists_unique_violation(self, table_name, constraint, record) -> bool:
        """UNIQUE 제약조건 위반 확인 (DB 조회)"""
        # 실제 구현에서는 DB 조회
        return False

    def _exists_pk(self, table_name, pk_values) -> bool:
        """PK 중복 확인 (DB 조회)"""
        # 실제 구현에서는 DB 조회
        return False

    def _exists_reference(self, ref_table, ref_columns, values) -> bool:
        """FK 참조 확인 (DB 조회)"""
        # 실제 구현에서는 DB 조회
        return True
```

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개 이상]

#### 1. 스키마 접근 방식 비교

| 비교 항목 | Schema-on-Write (RDBMS) | Schema-on-Read (Data Lake) | Schemaless (NoSQL) |
|:---|:---|:---|:---|
| **정의 시점** | 데이터 입력 시 | 데이터 조회 시 | 없음 |
| **유연성** | 낮음 | 높음 | 매우 높음 |
| **데이터 품질** | 높음 (사전 검증) | 낮음 (사후 검증) | 낮음 |
| **쿼리 성능** | 높음 | 중간 | 높음 |
| **적합한 용도** | OLTP, 트랜잭션 | 분석, 탐색 | 로그, 세션 |

#### 2. 스키마 변경 연산 비교

| DDL 연산 | 영향도 | 실행 시간 | 롤백 가능성 | 주의사항 |
|:---|:---|:---|:---|:---|
| **ADD COLUMN** | 낮음 | 빠름 | 가능 (일부) | DEFAULT 값 권장 |
| **DROP COLUMN** | 높음 | 느림 | 불가능 | 데이터 손실 주의 |
| **MODIFY COLUMN** | 높음 | 느림 | 제한적 | 데이터 변환 필요 |

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [최소 800자 이상]

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 대용량 테이블 스키마 변경**
- **상황**: 10억 건의 주문 테이블에 컬럼 추가 필요
- **전략**: Online DDL 사용, 새 테이블 생성 후 데이터 복사, Blue-Green 전환
- **결과**: 무중단 스키마 변경

**시나리오 2: 스키마 버전 관리**
- **전략**: Flyway/Liquibase 도입, 마이그레이션 스크립트 버전 관리

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] 정규화 수준 결정 (3NF, BCNF)
- [ ] 적절한 데이터 타입 선택
- [ ] 제약조건 정의 (PK, FK, CHECK)
- [ ] 인덱스 전략 수립

#### 3. 안티패턴 (Anti-patterns)

1. **Over-Normalization**: 과도한 정규화로 성능 저하
2. **God Table**: 모든 컬럼을 하나의 테이블에
3. **Meaningless Names**: 컬럼명의 의미 불명확

---

### V. 기대효과 및 결론 (Future & Standard) - [최소 400자 이상]

#### 1. 정량적/정성적 기대효과

| 구분 | 스키마 설계 미흡 | 스키마 설계 적절 | 개선 효과 |
|:---|:---|:---|:---|
| **데이터 무결성** | 70% | 99.9% | 42% 향상 |
| **쿼리 성능** | 기준 | 2~3배 향상 | 200% 증가 |
| **유지보수 비용** | 높음 | 낮음 | 60% 절감 |

#### 2. 미래 전망

- 스키마 레지스트리 (Confluent Schema Registry)
- AI 기반 스키마 추천 및 최적화
- 자가 진화 스키마 (Self-evolving Schema)

---

### 관련 개념 맵 (Knowledge Graph)

- **[데이터 독립성](@/studynotes/5_database/1_relational/4_data_independence.md)**: 스키마 계층 분리의 목적
- **[3단계 스키마](@/studynotes/5_database/1_relational/6_three_schema_architecture.md)**: 스키마의 계층 구조
- **[정규화](@/studynotes/5_database/3_normalization/normalization.md)**: 스키마 설계 원칙
- **[DDL](@/studynotes/5_database/2_sql/ddl.md)**: 스키마 정의 언어

---

### 어린이를 위한 3줄 비유 설명

1. **레고 조립 설명서**: 레고로 무언가를 만들 때 설명서가 있죠? 스키마는 이 설명서와 같아요. 어떤 블록이 어디에 들어가야 하는지 정해줘요!

2. **학교 시간표**: 학교에서 월요일 몇 시에 수학, 몇 시에 체육인지 정해진 시간표가 있죠? 스키마도 이렇게 어떤 데이터가 어디에 어떻게 들어가야 하는지 정해주는 규칙이에요!

3. **주문서 양식**: 식당에서 주문할 때 메뉴 이름, 수량, 가격이 적힌 주문서를 쓰죠? 스키마는 이 주문서처럼 어떤 정보를 적어야 하는지 정해놓은 틀이에요!
