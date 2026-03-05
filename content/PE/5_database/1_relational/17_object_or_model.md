+++
title = "객체지향/객체관계형 데이터 모델 (OODBMS/ORDBMS)"
description = "객체지향 개념과 데이터베이스의 융합, ODMG, SQL:1999 객체 확장 심층 분석"
date = "2026-03-05"
[taxonomies]
tags = ["database", "oodbms", "ordbms", "object-oriented", "sql-1999"]
categories = ["studynotes-5_database"]
+++

# 17. 객체지향/객체관계형 데이터 모델 (OODBMS / ORDBMS)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OODBMS는 객체지향 프로그래밍의 캡슐화, 상속, 다형성 개념을 데이터베이스에 적용한 모델이며, ORDBMS는 관계형 DB에 객체 개념을 확장한 하이브리드 모델입니다.
> 2. **가치**: 임피던스 불일치(Impedance Mismatch) 문제를 해결하여 복잡한 도메인 모델링에서 개발 생산성을 30~50% 향상시키며, SQL:1999 이후 PostgreSQL, Oracle 등에서 객체 기능을 지원합니다.
> 3. **융합**: 현대 ORM(JPA, Hibernate), Document DB(MongoDB), 그리고 복합 타입(JSON) 지원의 이론적 기반을 제공합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**객체지향 데이터베이스 관리 시스템(OODBMS, Object-Oriented DBMS)**은 객체지향 프로그래밍 언어(C++, Java, Smalltalk)의 개념을 데이터베이스로 직접 확장한 시스템입니다. 데이터와 연산(메서드)을 하나의 객체로 캡슐화하고, 상속과 다형성을 지원합니다.

**객체관계형 데이터베이스 관리 시스템(ORDBMS, Object-Relational DBMS)**은 관계형 데이터베이스의 기반 위에 객체지향 개념을 확장한 시스템입니다. SQL 표준(SQL:1999)을 기반으로 사용자 정의 타입(UDT), 상속, 참조 타입 등을 지원합니다.

**핵심 개념 비교**:

| 개념 | OODBMS | ORDBMS |
|:---|:---|:---|
| **기반** | 순수 객체지향 | 관계형 + 객체 확장 |
| **쿼리 언어** | OQL (ODMG) | SQL:1999+ |
| **호환성** | OO 언어와 완벽 호환 | SQL + 객체 기능 |
| **대표 제품** | ObjectStore, GemStone | PostgreSQL, Oracle, Informix |
| **표준** | ODMG 3.0 | SQL:1999, SQL:2003 |

**등장 배경: 임피던스 불일치(Impedance Mismatch)**:
```
[객체지향 프로그래밍]          [관계형 데이터베이스]
        Class                    ↔      Table
        Object                   ↔      Row
        Attribute                ↔      Column
        Reference (OID)          ↔      Foreign Key
        Method                   ↔      Stored Procedure?
        Inheritance              ↔      ??? (지원 안 함)
        Collection (List, Set)   ↔      ??? (지원 안 함)

=> 이 mismatch로 인한 변환 비용이 개발의 30~40% 차지!
```

#### 2. 💡 비유를 통한 이해

**자동차 설계와 제조**로 비유할 수 있습니다:

- **RDBMS (부품 중심)**: 엔진, 타이어, 핸들을 각각 따로 보관하고, 조립 설명서를 보고 필요할 때 조립
  - 유연하지만 매번 조립 필요
  - 부품 간 관계는 설명서(FK)로만 파악

- **OODBMS (완성품 중심)**: 조립된 상태의 자동차를 통째로 저장
  - 엔진은 자동차 안에, 타이어도 자동차 안에
  - 자동차는 '달리다()', '정지하다()' 메서드도 가짐
  - 꺼내자마자 바로 사용 가능

- **ORDBMS (모듈형 하이브리드)**: 부품도 따로, 조립된 모듈도 따로 저장
  - 엔진 모듈(복합 타입)을 테이블에 저장
  - 기존 SQL도 사용하고, 객체 기능도 사용

#### 3. 등장 배경 및 발전 과정

**1단계: 문제 인식 (1980년대 초)**
- C++, Smalltalk 등 OOP 언어의 대중화
- RDBMS와의 임피던스 불일치로 인한 생산성 저하
- CAD/CAM, GIS 등 복잡한 데이터 모델링 요구

**2단계: OODBMS 등장 (1980년대 중~후반)**
- 1985년: ObjectStore, GemStone, Ontos 등 등장
- 1993년: ODMG 1.0 표준 발표
- 특징: OO 언어와 완벽한 통합, 영속성 투명성

**3단계: ORDBMS 대응 (1990년대 중반)**
- 1997년: Informix Universal Server, Oracle 8
- SQL:1999 표준에 객체 기능 추가
- 기존 RDBMS에 객체 확장

**4단계: 경쟁과 현대 (2000년대~현재)**
- OODBMS: 틈새 시장(CAD, 과학 계산)으로 축소
- ORDBMS: PostgreSQL, Oracle의 객체 기능 강화
- ORM: Hibernate, JPA가 사실상 표준
- NoSQL: Document DB가 유연한 객체 저장 제공

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. OODBMS/ORDBMS 핵심 개념 (표)

| 개념 | OODBMS 정의 | ORDBMS 정의 | SQL:1999 대응 |
|:---|:---|:---|:---|
| **객체 식별자 (OID)** | 시스템 생성 고유 ID | REF 타입 | REF type |
| **캡슐화** | 데이터 + 메서드 | UDT + 메서드 | CREATE TYPE |
| **상속** | 단일/다중 상속 | 타입 계층 | UNDER |
| **복합 타입** | 중첩 객체 | ROW 타입, ARRAY | ROW, ARRAY |
| **컬렉션** | List, Set, Bag | ARRAY, MULTISET | ARRAY, MULTISET |
| **다형성** | 메서드 오버라이딩 | 타입별 메서드 | 메서드 디스패치 |
| **참조** | 객체 참조 (포인터) | REF 타입 | REF type |
| **질의 언어** | OQL (객체 질의 언어) | SQL 확장 | SQL:1999 |

#### 2. ORDBMS 아키텍처 다이어그램

```text
+============================================================================+
|                    OBJECT-RELATIONAL DBMS ARCHITECTURE                      |
+============================================================================+
|                                                                             |
|  +---------------------------------------------------------------------+   |
|  |                    APPLICATION LAYER                                 |   |
|  |  +----------------+  +----------------+  +----------------+         |   |
|  |  |  Java Objects  |  |  Python Objects|  |  C++ Objects   |         |   |
|  |  +-------+--------+  +-------+--------+  +-------+--------+         |   |
|  +----------|-------------------|-------------------|------------------+   |
|             |                   |                   |                     |
|             v                   v                   v                     |
|  +---------------------------------------------------------------------+   |
|  |                      OR-MAPPING LAYER                               |   |
|  |  +----------------+  +----------------+  +----------------+         |   |
|  |  |  Hibernate     |  |  SQLAlchemy    |  |  Native Driver |         |   |
|  |  +-------+--------+  +-------+--------+  +-------+--------+         |   |
|  +----------|-------------------|-------------------|------------------+   |
|             |                   |                   |                     |
|             +-------------------+-------------------+                     |
|                                 |                                          |
|                                 v                                          |
|  +---------------------------------------------------------------------+   |
|  |                    ORDBMS ENGINE (PostgreSQL/Oracle)                 |   |
|  |  +---------------------------+  +---------------------------+        |   |
|  |  |   RELATIONAL ENGINE       |  |   OBJECT EXTENSIONS       |        |   |
|  |  |  - Table/Row/Column       |  |  - User-Defined Types     |        |   |
|  |  |  - SQL Parser             |  |  - Inheritance (UNDER)    |        |   |
|  |  |  - Optimizer              |  |  - Methods (Functions)    |        |   |
|  |  |  - Index (B-Tree, Hash)   |  |  - REF Types              |        |   |
|  |  +---------------------------+  +---------------------------+        |   |
|  |  +---------------------------+  +---------------------------+        |   |
|  |  |   COMPLEX TYPES           |  |   COLLECTIONS             |        |   |
|  |  |  - ROW Type               |  |  - ARRAY                  |        |   |
|  |  |  - Composite Type         |  |  - MULTISET               |        |   |
|  |  |  - JSON/JSONB             |  |  - Nested Tables          |        |   |
|  |  +---------------------------+  +---------------------------+        |   |
|  +---------------------------------------------------------------------+   |
|                                 |                                          |
|                                 v                                          |
|  +---------------------------------------------------------------------+   |
|  |                      STORAGE ENGINE                                 |   |
|  |  +----------------+  +----------------+  +----------------+         |   |
|  |  |  Table Pages   |  |  Index Pages   |  |  TOAST (Large) |         |   |
|  |  +----------------+  +----------------+  +----------------+         |   |
|  +---------------------------------------------------------------------+   |
|                                                                             |
+============================================================================+
```

#### 3. 심층 동작 원리: SQL:1999 객체 확장

**1단계: 사용자 정의 타입 (UDT) 생성**
```sql
-- SQL:1999 / PostgreSQL 객체 타입 정의

-- 복합 타입 (Composite Type)
CREATE TYPE address_type AS (
    street      VARCHAR(100),
    city        VARCHAR(50),
    postal_code VARCHAR(10),
    country     VARCHAR(50)
);

-- 객체 타입 (Table 타입)
CREATE TYPE person_type AS (
    id          INTEGER,
    name        VARCHAR(100),
    birth_date  DATE,
    address     address_type  -- 중첩 타입
);

-- 상속을 이용한 타입 계층 (PostgreSQL)
CREATE TABLE persons (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    birth_date  DATE
);

CREATE TABLE employees (
    salary      DECIMAL(10,2),
    hire_date   DATE,
    dept_id     INTEGER
) INHERITS (persons);  -- persons 테이블 상속

-- employees는 id, name, birth_date, salary, hire_date, dept_id 모두 가짐
```

**2단계: 배열 및 컬렉션 타입**
```sql
-- PostgreSQL 배열 타입
CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100),
    tags        VARCHAR(50)[],  -- 문자열 배열
    prices      DECIMAL(10,2)[3]  -- 고정 길이 배열
);

-- 배열 데이터 삽입
INSERT INTO products (name, tags, prices)
VALUES ('노트북', ARRAY['전자기기', '컴퓨터', '필수품'], ARRAY{1200000.00, 1100000.00, 1000000.00});

-- 배열 요소 접근
SELECT name, tags[1] AS first_tag, array_length(tags, 1) AS tag_count
FROM products;

-- 배열 연산
SELECT * FROM products WHERE '전자기기' = ANY(tags);  -- 배열 포함 검색

-- JSON 타입 (현대 ORDBMS의 핵심)
CREATE TABLE documents (
    id      SERIAL PRIMARY KEY,
    data    JSONB  -- Binary JSON (인덱싱 가능)
);

INSERT INTO documents (data) VALUES (
    '{
        "title": "객체지향 DB 개론",
        "authors": ["홍길동", "김철수"],
        "metadata": {
            "year": 2026,
            "publisher": "기술출판사"
        }
    }'
);

-- JSON 경로 쿼리
SELECT data->>'title' AS title,
       data->'metadata'->>'year' AS year
FROM documents;

-- JSON 인덱싱
CREATE INDEX idx_documents_data ON documents USING GIN (data);
```

**3단계: 참조 타입 (REF)**
```sql
-- 객체 참조를 이용한 관계 표현 (Oracle 스타일)

-- 타입 정의
CREATE OR REPLACE TYPE dept_type AS OBJECT (
    dept_id     NUMBER,
    dept_name   VARCHAR2(50)
);

-- 타입 테이블 생성
CREATE TABLE departments OF dept_type (
    PRIMARY KEY (dept_id)
);

-- REF 타입을 이용한 참조
CREATE OR REPLACE TYPE emp_type AS OBJECT (
    emp_id      NUMBER,
    emp_name    VARCHAR2(100),
    dept_ref    REF dept_type,  -- 객체 참조
    MEMBER FUNCTION get_dept_name RETURN VARCHAR2
);

CREATE TABLE employees OF emp_type (
    PRIMARY KEY (emp_id)
);

-- 참조를 통한 접근 (DEREF)
SELECT e.emp_name, DEREF(e.dept_ref).dept_name
FROM employees e;
```

#### 4. 실무 수준의 OODBMS/ORDBMS 구현 예시

```python
"""
객체지향 데이터 모델링과 ORM을 이용한 구현
SQLAlchemy (Python ORM) 예시
"""

from sqlalchemy import (
    create_engine, Column, Integer, String, Float,
    ForeignKey, JSON, Array, Date
)
from sqlalchemy.orm import (
    declarative_base, relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from typing import List, Optional
from datetime import date
import json

Base = declarative_base()

# ==================== 복합 타입 모델링 ====================

class Address:
    """값 타입 (Value Object) - 주소"""
    def __init__(self, street: str, city: str, postal_code: str):
        self.street = street
        self.city = city
        self.postal_code = postal_code

    def to_dict(self) -> dict:
        return {
            'street': self.street,
            'city': self.city,
            'postal_code': self.postal_code
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Address':
        return cls(**data)

# ==================== 상속 매핑 (Joined Table Inheritance) ====================

class Person(Base):
    """기본 클래스 - 상속 계층의 루트"""
    __tablename__ = 'persons'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[Optional[date]] = mapped_column(Date)
    type: Mapped[str]  # Discriminator column

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'person'
    }

class Employee(Person):
    """Person을 상속받은 Employee (1:1 상속)"""
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(ForeignKey('persons.id'), primary_key=True)
    salary: Mapped[float] = mapped_column(Float)
    hire_date: Mapped[date] = mapped_column(Date)
    dept_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))

    # 관계 (Reference)
    department: Mapped['Department'] = relationship(back_populates='employees')

    __mapper_args__ = {
        'polymorphic_identity': 'employee'
    }

# ==================== 컬렉션 타입 (배열, JSON) ====================

class Department(Base):
    """부서 - 컬렉션 타입 포함"""
    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    location: Mapped[Optional[dict]] = mapped_column(JSONB)  # JSON 타입
    tags: Mapped[Optional[list]] = mapped_column(ARRAY(String))  # 배열 타입

    # 1:N 관계
    employees: Mapped[List['Employee']] = relationship(back_populates='department')

    # 메서드 (캡슐화의 일부)
    def add_employee(self, employee: Employee) -> None:
        """직원 추가 메서드"""
        employee.dept_id = self.id
        employee.department = self

    def get_average_salary(self) -> float:
        """평균 급여 계산 메서드"""
        if not self.employees:
            return 0.0
        return sum(e.salary for e in self.employees) / len(self.employees)

# ==================== OQL 스타일 쿼리 ====================

class Product(Base):
    """제품 - 중첩 객체 예시"""
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    attributes: Mapped[dict] = mapped_column(JSONB)  # 유연한 속성 저장

    # attributes 예시:
    # {
    #   "specs": {"cpu": "M3", "ram": "16GB"},
    #   "colors": ["Space Gray", "Silver"],
    #   "price_history": [{"date": "2026-01-01", "price": 1500000}]
    # }

# ==================== 사용 예시 ====================

def demonstrate_oodbms_patterns():
    """OODBMS/ORDBMS 패턴 시연"""
    engine = create_engine('postgresql://user:pass@localhost/testdb')
    Base.metadata.create_all(engine)

    from sqlalchemy.orm import Session
    with Session(engine) as session:
        # 1. 객체 생성 및 저장 (영속화)
        dept = Department(
            name='엔지니어링팀',
            location=Address('서울 강남구', '서울', '06234').to_dict(),
            tags=['개발', '연구', '핵심부서']
        )
        session.add(dept)
        session.flush()  # ID 할당

        # 2. 상속 객체 생성
        emp = Employee(
            name='홍길동',
            birth_date=date(1990, 5, 15),
            salary=50000000,
            hire_date=date(2020, 3, 1)
        )
        dept.add_employee(emp)

        # 3. 컬렉션 활용
        product = Product(
            name='MacBook Pro',
            attributes={
                'specs': {'cpu': 'M3 Pro', 'ram': '18GB', 'storage': '512GB'},
                'colors': ['Space Black', 'Silver'],
                'warranty_years': 1
            }
        )
        session.add(product)

        session.commit()

        # 4. OQL 스타일 쿼리 (JSON 경로)
        products = session.query(Product).filter(
            Product.attributes['specs']['cpu'].astext == 'M3 Pro'
        ).all()

        # 5. 다형성 쿼리 (상속)
        persons = session.query(Person).all()  # Person과 Employee 모두 조회
        for p in persons:
            print(f"{type(p).__name__}: {p.name}")

        # 6. 메서드 호출 (캡슐화)
        avg_salary = dept.get_average_salary()
        print(f"평균 급여: {avg_salary:,}원")

if __name__ == '__main__':
    demonstrate_oodbms_patterns()
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. RDBMS vs OODBMS vs ORDBMS 심층 비교

| 비교 항목 | RDBMS | OODBMS | ORDBMS |
|:---|:---|:---|:---|
| **데이터 모델** | 관계형 (테이블) | 객체지향 | 관계형 + 객체 |
| **복합 타입** | 미지원 | 완벽 지원 | 지원 (UDT, JSON) |
| **상속** | 미지원 | 완벽 지원 | 부분 지원 |
| **메서드** | Stored Proc | 객체 메서드 | UDF, 메서드 |
| **쿼리 언어** | SQL | OQL | SQL:1999+ |
| **임피던스 불일치** | 높음 | 없음 | 낮음 |
| **트랜잭션** | ACID 완벽 | ACID 지원 | ACID 완벽 |
| **표준화** | SQL 표준 | ODMG (소멸) | SQL:1999 표준 |
| **시장 점유율** | 압도적 | 틈새 | 성장 중 |

#### 2. ORM vs OODBMS 비교

| 비교 항목 | ORM (Hibernate/JPA) | OODBMS (ObjectStore) |
|:---|:---|:---|
| **저장소** | RDBMS 위에서 동작 | 전용 저장소 |
| **성능** | 변환 오버헤드 존재 | 직접 저장으로 빠름 |
| **호환성** | SQL DB와 호환 | 독자적 |
| **학습 곡선** | 중간 | 높음 |
| **생태계** | 매우 큼 | 작음 |
| **트랜잭션** | RDBMS에 의존 | 자체 지원 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: CAD/CAM 시스템 설계**
- 상황: 복잡한 설계 데이터(수천 개의 부품, 다단계 조립)
- 판단: RDBMS로는 모델링 복잡도가 너무 높음
- 전략:
  - OODBMS 또는 Document DB 검토
  - 복잡한 객체 그래프를 자연스럽게 저장
  - 버전 관리와 임시 객체 지원 필요

**시나리오 2: 엔터프라이즈 시스템의 JSON 활용**
- 상황: 유연한 메타데이터 저장 필요
- 판단: ORDBMS의 JSON/JSONB 타입 활용
- 전략:
  - PostgreSQL JSONB + GIN 인덱스
  - 정형 데이터는 컬럼, 비정형은 JSON
  - JSON Path 쿼리로 유연한 검색

**시나리오 3: JPA/Hibernate 도입**
- 상황: Java 기반 웹 애플리케이션
- 판단: ORM을 통한 임피던스 불일치 해결
- 전략:
  - JPA 표준 준수
  - 적절한 상속 매핑 전략 선택
  - N+1 문제 해결 (Fetch Join)

#### 2. 도입 시 고려사항 (체크리스트)

**ORDBMS 기능 활용 체크리스트**:
- [ ] JSON/JSONB 컬럼 활용 검토
- [ ] 배열 타입 (ARRAY) 필요성
- [ ] 상속 매핑 전략 선택
- [ ] 복합 타입 (Composite Type) 정의
- [ ] GIN/GiST 인덱스 활용

**ORM 도입 체크리스트**:
- [ ] 엔티티 설계 (식별자, 연관관계)
- [ ] 상속 전략 (SINGLE_TABLE, JOINED, TABLE_PER_CLASS)
- [ ] 지연 로딩 vs 즉시 로딩
- [ ] 2차 캐시 필요성
- [ ] 벌크 연산 최적화

#### 3. 안티패턴 (Anti-patterns)

1. **God Object**: 하나의 객체에 너무 많은 속성/메서드
   - 해결: 적절한 응집도로 분리

2. **Over-JSON**: 모든 것을 JSON에 넣기
   - 해결: 자주 조회하는 속성은 컬럼으로

3. **Deep Inheritance**: 너무 깊은 상속 계층
   - 해결: Composition over Inheritance

4. **N+1 Query**: ORM 사용 시 연관 객체 지연 로딩
   - 해결: Fetch Join, EntityGraph

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 순수 RDBMS | ORDBMS + ORM | 개선 효과 |
|:---|:---|:---|:---|
| **개발 생산성** | 기준 | +30~50% | 객체 매핑 자동화 |
| **임피던스 불일치** | 높음 | 낮음 | 변환 코드 80% 감소 |
| **유연성** | 낮음 (스키마 고정) | 높음 (JSON) | 스키마 변경 용이 |
| **쿼리 성능** | 높음 | 중간~높음 | JSON 인덱스 활용 |

#### 2. 미래 전망 및 진화 방향

**ORDBMS의 진화**:
- **JSON/JSONB 고도화**: JSON Path, JSON Schema
- **Multi-Model**: 관계형 + 문서 + 그래프 + 벡터 통합
- **AI-Native**: 객체 인식 자동 매핑

**OODBMS의 틈새 시장**:
- **실시간 시스템**: 게임, 시뮬레이션
- **과학 계산**: 생물정보학, 천문학
- **Embedded DB**: 모바일, IoT

#### 3. 참고 표준/가이드

| 표준 | 내용 | 적용 범위 |
|:---|:---|:---|
| **ODMG 3.0** | OODBMS 표준 (역사적) | ObjectStore 등 |
| **SQL:1999** | 객체 관계 확장 | ORDBMS 표준 |
| **SQL:2003** | XML, 배열 타입 | 현대 RDBMS |
| **JPA 2.2** | Java Persistence API | Java ORM 표준 |

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[관계형 데이터 모델](@/studynotes/5_database/1_relational/relational_model.md)**: ORDBMS의 기반
- **[NoSQL](@/studynotes/5_database/1_relational/nosql.md)**: Document DB의 객체 저장
- **[정규화](@/studynotes/5_database/1_relational/normalization.md)**: 객체 매핑 시 고려사항
- **[ER 모델](@/studynotes/5_database/1_relational/er_model.md)**: 개념적 모델링과 객체 매핑
- **[SQL](@/studynotes/5_database/2_sql/_index.md)**: SQL:1999 객체 확장

---

### 👶 어린이를 위한 3줄 비유 설명

1. **장난감 로봇**: 장난감 로봇은 팔도 있고 다리도 있고, '앞으로 가기', '뒤로 가기' 같은 기능도 함께 가지고 있어요. 이렇게 데이터와 기능이 하나로 묶여 있는 게 '객체'예요!

2. **레고 조립 설명서**: 레고 기본 블록(관계형 DB)만으로는 복잡한 로봇을 만들기 어려워요. 그래서 특수 부품(객체 기능)을 추가해서 더 멋진 걸 만들 수 있게 한 게 'ORDBMS'예요!

3. **프링글스 통**: 감자칩이 층층이 쌓여 있듯이, 데이터도 상자(테이블) 안에 층층이 들어갈 수 있어요. JSON은 감자칩 맛처럼 다양한 정보를 한 통에 담을 수 있게 해줘요!
