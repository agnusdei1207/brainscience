+++
title = "데이터베이스 정규화 (Normalization)"
date = 2024-05-18
description = "관계형 데이터베이스의 이상 현상을 제거하기 위한 정규화 이론(1NF ~ 5NF), 함수적 종속성(FD), 반정규화(Denormalization) 전략 및 실무 SQL 예제"
weight = 30
+++

# 데이터베이스 정규화 심층 분석 (Database Normalization)

## 1. 정규화의 목적 및 이상 현상 (Anomalies)
데이터베이스 정규화(Normalization)는 관계형 데이터 모델에서 데이터의 중복을 최소화하고 데이터의 무결성(Integrity)을 보장하기 위해 릴레이션(테이블)을 분해하는 논리적 설계 과정입니다. 정규화를 수행하지 않은 테이블은 갱신 과정에서 논리적 모순이 발생하는 **이상 현상(Anomaly)**을 겪게 됩니다.

### 1.1 3가지 이상 현상
- **삽입 이상 (Insertion Anomaly)**: 새로운 데이터를 삽입하기 위해 불필요한 데이터까지 강제로 입력해야 하는 현상. (예: 아직 부서에 배정되지 않은 신입사원을 추가하려 할 때 부서 코드가 기본키의 일부라면 삽입 불가)
- **삭제 이상 (Deletion Anomaly)**: 특정 데이터를 삭제할 때 연관된 다른 유용한 데이터까지 연쇄적으로 삭제(Cascade Deletion)되는 현상.
- **갱신 이상 (Update Anomaly)**: 중복 저장된 데이터 중 일부만 갱신되어 데이터 간의 불일치(Inconsistency)가 발생하는 현상.

## 2. 함수적 종속성 (Functional Dependency, FD)
정규화 이론의 핵심은 속성(Attribute)들 간의 함수적 종속성을 파악하는 것입니다.
X 값을 알면 Y 값을 유일하게 결정할 수 있을 때, "Y는 X에 함수적으로 종속된다"라고 하며 `X -> Y`로 표기합니다.
- **결정자(Determinant)**: X
- **종속자(Dependent)**: Y
- **완전 함수 종속 (Full Functional Dependency)**: X가 여러 속성의 집합(복합키)일 때, Y가 X의 전체에만 종속되고 X의 진부분집합에는 종속되지 않는 경우.
- **부분 함수 종속 (Partial Functional Dependency)**: Y가 기본키 X의 일부에만 종속되는 경우.
- **이행적 함수 종속 (Transitive Functional Dependency)**: X -> Y 이고 Y -> Z 일 때, 논리적으로 X -> Z 가 성립하는 경우.

```ascii
[ 함수적 종속성 다이어그램 (FD Diagram) 예시 ]

   +----------------+   완전 함수 종속    +-------------+
   | (학번, 과목코드) | -----------------> |    성적     |
   +----------------+                     +-------------+
          |                                      ^
          |             부분 함수 종속           |
          +--------------------------------------+ (잘못된 설계)
```

## 3. 정규형 (Normal Forms) 단계별 분석

정규화는 순차적으로 진행되며, 상위 정규형은 하위 정규형의 조건을 모두 만족해야 합니다.

### 3.1 제1정규형 (1NF: First Normal Form)
- **조건**: 릴레이션의 모든 속성 값이 **원자값(Atomic Value)**만을 가져야 합니다. 즉, 하나의 컬럼에 배열이나 리스트와 같은 다중 값이 들어갈 수 없습니다.

```sql
-- [1NF 위반 예시]
-- 전화번호 컬럼에 '010-1111-2222, 02-333-4444' 형태의 다중 값이 존재.
-- [1NF 정규화 후]
CREATE TABLE Employee (
    EmpID INT,
    Name VARCHAR(50)
);
CREATE TABLE EmployeePhone (
    EmpID INT,
    Phone VARCHAR(20),
    PRIMARY KEY (EmpID, Phone),
    FOREIGN KEY (EmpID) REFERENCES Employee(EmpID)
);
```

### 3.2 제2정규형 (2NF)
- **조건**: 1NF를 만족하고, 기본키가 아닌 모든 속성이 기본키에 **완전 함수 종속**되어야 합니다. (부분 함수 종속 제거)
- 주로 복합키(Composite Key)를 사용하는 테이블에서 발생합니다.

### 3.3 제3정규형 (3NF)
- **조건**: 2NF를 만족하고, 기본키가 아닌 모든 속성들 간에 **이행적 함수 종속이 없어야** 합니다.
- `A -> B` 이고 `B -> C` 일 때 `C`를 분리합니다.

```sql
-- [3NF 정규화 대상 예시]
-- 주문(주문번호(PK), 고객ID, 고객등급, 할인율)
-- 함수종속: 주문번호 -> 고객ID, 고객ID -> 고객등급, 고객등급 -> 할인율
-- 이행적 종속 발생!

-- [3NF 정규화 후 테이블 분리]
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    Grade VARCHAR(10),
    FOREIGN KEY (Grade) REFERENCES GradeDiscount(Grade)
);

CREATE TABLE GradeDiscount (
    Grade VARCHAR(10) PRIMARY KEY,
    DiscountRate DECIMAL(5,2)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);
```

### 3.4 BCNF (Boyce-Codd Normal Form)
- **조건**: 3NF를 만족하고, 릴레이션의 **모든 결정자가 후보키(Candidate Key)**여야 합니다. (강한 3정규형)
- 후보키가 여러 개 존재하고 중첩될 때 주로 발생합니다. (예: 수강(학번, 과목, 교수) 테이블에서 (학번, 과목)이 PK인데, '교수 -> 과목' 종속성이 존재하지만 교수는 후보키가 아닌 경우).

### 3.5 제4정규형(4NF) 및 제5정규형(5NF)
- **4NF**: 다치 종속(Multi-Valued Dependency, MVD; A ->> B) 제거.
- **5NF**: 조인 종속(Join Dependency) 제거.
- 실무에서는 비즈니스 로직의 복잡도와 성능 문제로 인해 BCNF까지만 수행하는 것이 일반적입니다.

## 4. 반정규화 (Denormalization) 전략
정규화는 데이터 정합성을 높이지만, 테이블의 분할로 인해 데이터를 조회할 때 다수의 `JOIN` 연산이 필요하게 되어 읽기(Read) 성능이 저하될 수 있습니다. 이를 해결하기 위해 성능 향상을 목적으로 의도적으로 정규화 원칙을 위배하는 것을 **반정규화**라고 합니다.

### 4.1 반정규화 기법
1. **테이블 병합**: 1:1 관계 또는 1:N 관계의 테이블을 잦은 조인 회피를 위해 병합.
2. **테이블 분할**: 수직 분할(컬럼 기준 분할, 파티셔닝), 수평 분할(로우 기준 분할, 샤딩).
3. **중복 컬럼 추가**: 조인 비용을 줄이기 위해 부모 테이블의 컬럼을 자식 테이블에 중복 저장.
4. **계산된(Derived) 컬럼 추가**: 총합, 평균 등 매번 계산하기 무거운 데이터를 테이블에 미리 저장 (예: 트리거를 이용한 잔액 유지).

## 5. 결론
아키텍트는 데이터베이스 설계 시 "읽기 중심(OLAP)인가, 쓰기 중심(OLTP)인가?"를 명확히 해야 합니다. OLTP 시스템에서는 데이터 무결성을 위해 BCNF 수준의 엄격한 정규화가 필수적이며, OLAP(데이터 웨어하우스) 시스템에서는 조회 성능 극대화를 위해 스타 스키마(Star Schema)와 같은 반정규화된 차원 모델링을 전략적으로 채택해야 합니다.
