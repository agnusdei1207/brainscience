+++
title = "188. PL/SQL (Oracle), T-SQL (SQL Server) - 절차적 SQL 언어"
weight = 188
+++
## 0. 핵심 인사이트

> **핵심 인사이트**: 순수 SQL은 "모든 직원의 급여를 가져와"라는 선언적 명령어일 뿐, "급여가 300만 원 이하면 10% 올리고, 아니면 냅둬라" 같은 프로그래밍 로직을 짤 수 없다. 그래서 SQL 뼈대에 IF, WHILE, 변수 같은 프로그래밍 살을 붙여 강력하게 진화시킨 언어가 절차적 SQL이다.

> 📝 모범 답안

## 1. 개요 및 필요성
전통적인 표준 SQL은 데이터를 조작하고 정의하는 '선언적 언어'로, 루프(반복)나 조건 분기 처리가 불가능합니다. 
이를 극복하기 위해 DBMS 벤더들이 **표준 SQL에 변수 선언, 제어 구조(IF, LOOP, FOR), 예외 처리(Exception) 등의 프로그래밍 기능을 추가 확장한 언어**입니다. 이 언어로 스토어드 프로시저(Stored Procedure)나 트리거를 작성합니다.

## 2. 구성요소

| DBMS | 절차적 언어 명칭 | 설명 |
|:---|:---|:---|
| **Oracle** | **PL/SQL** (Procedural Language/SQL) | 오라클에서 사용하는 가장 대표적이고 강력한 절차적 SQL입니다. 블록(Block) 구조로 되어 있습니다. |
| **SQL Server** | **T-SQL** (Transact-SQL) | 마이크로소프트 SQL Server와 Sybase에서 사용하는 절차적 언어입니다. |
| **MySQL** | **SQL/PSM** 기반 루틴 | MySQL과 MariaDB에서 스토어드 프로시저 등을 만들 때 사용하는 자체 절차적 문법입니다. |

## 3. 구조 및 동작 원리
PL/SQL은 무조건 아래의 3단 블록(Block) 구조로 작성됩니다.

```sql
DECLARE
    -- [선택] 선언부: 사용할 변수, 상수, 커서(Cursor)를 선언합니다.
    v_salary NUMBER;
BEGIN
    -- [필수] 실행부: 실제 비즈니스 로직(SQL문, IF문, LOOP문)을 작성합니다.
    SELECT salary INTO v_salary FROM employees WHERE emp_id = 100;
    
    IF v_salary < 3000 THEN
        UPDATE employees SET salary = salary * 1.1 WHERE emp_id = 100;
    END IF;
EXCEPTION
    -- [선택] 예외 처리부: 에러(예: 데이터 없음, 0으로 나누기) 발생 시 처리 로직
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('해당 직원이 없습니다.');
END;
```

## 4. 비교 및 트레이드오프
절차적 SQL에서 가장 중요한 개념 중 하나입니다.
`SELECT`를 하면 결과가 여러 줄(Row)이 나오는데, PL/SQL 변수는 한 번에 한 개의 값만 담을 수 있습니다. 이때 여러 줄의 결과를 메모리에 올려두고, **루프(FOR/WHILE)를 돌면서 한 줄씩 데이터를 꺼내서 처리할 수 있게 해주는 포인터(지시자)** 가 바로 커서입니다.

> 📢 **섹션 요약 비유**: 일반 SQL이 엑셀에서 단순히 '합계(SUM)' 함수를 쓰는 것이라면, PL/SQL이나 T-SQL은 엑셀의 'VBA 매크로'를 짜는 것과 같습니다. 조건에 따라 셀의 색깔을 바꾸고 다른 시트로 복사하는 등 복잡한 알고리즘을 엑셀 안에서 완벽하게 자동화할 수 있게 해주는 강력한 스크립트입니다.
