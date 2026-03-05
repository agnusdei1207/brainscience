+++
title = "DCL (Data Control Language) - 데이터 제어 언어"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
+++

# DCL (Data Control Language) - 데이터 제어 언어

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DCL(Data Control Language)은 데이터베이스 객체(테이블, 뷰, 프로시저 등)에 대한 접근 권한을 부여(GRANT)하고 회수(REVOKE)하는 SQL 명령어 집합으로, 데이터 보안의 최전방 방어선입니다.
> 2. **가치**: 최소 권한 원칙(Principle of Least Privilege)을 구현하여 내부자 위협(Insider Threat)을 80% 이상 완화하고, GDPR, ISMS 등 규정 준수의 핵심 통제 수단입니다.
> 3. **융합**: DCL은 롤(Role) 기반 접근 제어(RBAC), 뷰(View)를 통한 행/열 수준 보안, 그리고 감사(Audit) 로그와 연동하여 종합적 데이터 보안 체계를 구축합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**DCL(Data Control Language)**은 데이터베이스의 보안을 관리하기 위해 사용자에게 권한을 부여하거나 회수하는 SQL 명령어입니다. DCL의 핵심 목표는 **"누가(Who), 어떤 객체(What)에, 어떤 작업(How)을 수행할 수 있는가?"**를 제어하는 것입니다.

**DCL의 2대 핵심 명령어**:

| 명령어 | 기능 | 구문 | 비고 |
|:---:|:---|:---|:---|
| **GRANT** | 권한 부여 | GRANT 권한 ON 객체 TO 사용자 [WITH GRANT OPTION] | 권한 위임 가능 |
| **REVOKE** | 권한 회수 | REVOKE 권한 ON 객체 FROM 사용자 [CASCADE] | 종속 권한도 회수 |

**권한의 분류**:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        데이터베이스 권한 계층 구조                           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  시스템 권한 (System Privileges)                                     │  │
│  │  • 데이터베이스 전체 작업에 대한 권한                                 │  │
│  │  • 예: CREATE SESSION, CREATE TABLE, CREATE USER, DROP ANY TABLE   │  │
│  │  • 주로 DBA에게 부여                                                 │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  객체 권한 (Object Privileges)                                       │  │
│  │  • 특정 테이블, 뷰, 시퀀스 등에 대한 작업 권한                       │  │
│  │  • 예: SELECT, INSERT, UPDATE, DELETE, EXECUTE, REFERENCES         │  │
│  │  • 객체 소유자 또는 권한 있는 사용자가 부여                          │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  롤 (Roles)                                                          │  │
│  │  • 여러 권한을 묶어서 관리하는 명명된 권한 그룹                       │  │
│  │  • 예: CONNECT, RESOURCE, DBA (Oracle)                              │  │
│  │  • 권한 관리 간소화                                                   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

**주요 객체 권한 매트릭스**:

| 권한 | 테이블 | 뷰 | 시퀀스 | 프로시저 | 패키지 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| SELECT | O | O | O | - | - |
| INSERT | O | O* | - | - | - |
| UPDATE | O | O* | - | - | - |
| DELETE | O | O* | - | - | - |
| REFERENCES | O | - | - | - | - |
| ALTER | O | - | O | - | - |
| INDEX | O | - | - | - | - |
| EXECUTE | - | - | - | O | O |
| ALL | O | O | O | O | O |

*뷰의 경우 읽기 전용 뷰는 INSERT/UPDATE/DELETE 불가

#### 2. 비유를 통한 이해

**"DCL은 건물의 출입 카드 시스템"**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     [ 건물 출입 관리 비유 ]                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🏢 데이터베이스 = 보안이 철저한 오피스 빌딩                                  │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  GRANT = 출입 카드 발급                                                  ││
│  │                                                                          ││
│  │  "홍길동 직원에게 5층 회의실 출입 권한을 드립니다"                       ││
│  │  → GRANT SELECT ON orders TO hong;                                      ││
│  │                                                                          ││
│  │  • 특정 층(테이블)만 접근 가능                                          ││
│  │  • 업무 시간(조건)만 출입 가능                                           ││
│  │  • 임시 출입증(WITH GRANT OPTION)로 타인에게도 발급 가능                 ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  REVOKE = 출입 카드 회수                                                 ││
│  │                                                                          ││
│  │  "홍길동 직원의 5층 회의실 출입 권한을 회수합니다"                       ││
│  │  → REVOKE SELECT ON orders FROM hong;                                   ││
│  │                                                                          ││
│  │  • 권한이 즉시 제거됨                                                    ││
│  │  • 홍길동이 발급한 타인의 카드도 회수(CASCADE)                           ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  ROLE = 출입 권한 그룹                                                   ││
│  │                                                                          ││
│  │  [영업팀] 역할 = 3층 + 5층 + 회의실 출입                                ││
│  │  → CREATE ROLE sales_team;                                              ││
│  │  → GRANT SELECT ON customers, orders TO sales_team;                     ││
│  │  → GRANT sales_team TO hong, kim, lee;                                  ││
│  │                                                                          ││
│  │  • 직원별로 개별 권한 부여 대신 역할 부여                                ││
│  │  • 팀 이동 시 역할만 변경하면 됨                                         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 3. 등장 배경 및 발전 과정

1. **기존 기술의 치명적 한계**:
   - 초기 DBMS는 OS 수준의 보안에만 의존
   - 모든 사용자가 동일한 권한으로 데이터 접근
   - 데이터 유출, 무단 변경, 삭제 사고 빈발

2. **혁신적 패러다임의 도입**:
   - 1970년대: RDBMS의 등장과 함께 초기 권한 관리 기능 도입
   - 1980년대: GRANT/REVOKE 명령어 표준화
   - 1990년대: 롤(Role) 기반 접근 제어(RBAC) 도입
   - 2000년대: 세밀한 접근 제어(FGAC), 행 수준 보안(RLS)
   - 2010년대~: 통합 감사, 데이터 마스킹, 동적 데이터 마스킹

3. **비즈니스적 요구사항**:
   - 개인정보보호법, GDPR, CCPA 등 데이터 보호 규제 강화
   - 내부자 위협(Insider Threat) 대응
   - 최소 권한 원칙(Least Privilege) 구현 요구
   - 보안 감사(Security Audit) 대응

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. DCL 권한 구조 상세 (표)

| 권한 유형 | 명령어 예시 | 권한 범위 | 부여자 | 비고 |
|:---|:---|:---|:---|:---|
| **시스템 권한** | CREATE SESSION | DB 접속 | DBA | 로그인 권한 |
| | CREATE TABLE | 테이블 생성 | DBA | 스키마 변경 |
| | CREATE ANY TABLE | 타 스키마 테이블 생성 | DBA | 강한 권한 |
| | DROP ANY TABLE | 타 스키마 테이블 삭제 | DBA | 위험 권한 |
| | ALTER SYSTEM | 시스템 설정 변경 | DBA | 최고 권한 |
| **객체 권한** | SELECT | 데이터 조회 | 소유자 | 가장 빈번 |
| | INSERT | 데이터 삽입 | 소유자 | |
| | UPDATE | 데이터 수정 | 소유자 | |
| | DELETE | 데이터 삭제 | 소유자 | |
| | EXECUTE | 프로시저 실행 | 소유자 | |
| **롤** | CONNECT | 기본 접속 권한 묶음 | DBA | |
| | RESOURCE | 객체 생성 권한 묶음 | DBA | |
| | DBA | 관리자 권한 묶음 | SYS | 최고 권한 |

#### 2. DCL 권한 관리 아키텍처 다이어그램

```text
================================================================================
                    [ DCL Authorization Architecture ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ User Authentication ]                              │
│                                                                              │
│   User: hong / Password: **********                                          │
│   ┌───────────────────────────────────────────────────────────────────┐     │
│   │  1. 인증 (Authentication): 신원 확인                               │     │
│   │     • 사용자 ID/Password 검증                                      │     │
│   │     • Kerberos, LDAP, SSO 통합 가능                                │     │
│   │                                                                     │     │
│   │  2. 인가 (Authorization): 권한 확인                                 │     │
│   │     • 권한 테이블 조회                                              │     │
│   │     • 롤 계층 구조 평가                                             │     │
│   │     • 객체별 접근 권한 판단                                         │     │
│   └───────────────────────────────────────────────────────────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
┌─────────────────────────────────────────────────────────────────────────────┐
│                      [ Authorization Model ]                                 │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Discretionary Access Control (DAC)                  │  │
│  │                    임의 접근 통제 (SQL GRANT/REVOKE)                   │  │
│  │                                                                        │  │
│  │   ┌─────────┐         ┌─────────┐         ┌─────────┐                │  │
│  │   │  User   │────────▶│ Grants  │────────▶│ Object  │                │  │
│  │   │ (사용자)│         │ (권한)   │         │ (객체)  │                │  │
│  │   └─────────┘         └─────────┘         └─────────┘                │  │
│  │                                                                        │  │
│  │   특징:                                                                │  │
│  │   • 객체 소유자가 권한 부여/회수                                       │  │
│  │   • WITH GRANT OPTION으로 권한 위임 가능                               │  │
│  │   • 유연하지만 관리 복잡                                               │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Role-Based Access Control (RBAC)                    │  │
│  │                    롤 기반 접근 통제                                    │  │
│  │                                                                        │  │
│  │   ┌─────────┐         ┌─────────┐         ┌─────────┐                │  │
│  │   │  User   │────────▶│  Role   │────────▶│Privilege│                │  │
│  │   │ (사용자)│         │ (롤)    │         │ (권한)  │                │  │
│  │   └─────────┘         └─────────┘         └─────────┘                │  │
│  │                                                                        │  │
│  │   특징:                                                                │  │
│  │   • 권한을 롤로 그룹화                                                 │  │
│  │   • 사용자에게 롤만 부여                                               │  │
│  │   • 관리 간소화, 업무 기반 권한 부여                                    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Fine-Grained Access Control (FGAC)                  │  │
│  │                    세밀한 접근 통제                                     │  │
│  │                                                                        │  │
│  │   ┌─────────────────────────────────────────────────────────────────┐ │  │
│  │   │  Row-Level Security (RLS) / Virtual Private Database (VPD)      │ │  │
│  │   │                                                                  │ │  │
│  │   │  SELECT * FROM orders;                                           │ │  │
│  │   │  → 자동으로 WHERE customer_id = CURRENT_USER 추가                │ │  │
│  │   │  → 사용자별로 보이는 행이 다름                                    │ │  │
│  │   └─────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                        │  │
│  │   특징:                                                                │  │
│  │   • 행/열 수준의 세밀한 제어                                          │  │
│  │   • 정책(Policy) 함수로 동적 조건 추가                                │  │
│  │   • 데이터 마스킹, 레드액션 포함                                      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
                    [ GRANT/REVOKE Flow ]
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  GRANT SELECT, INSERT ON hr.employees TO hong WITH GRANT OPTION;       │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  1. 권한 부여자 검증                                                    │
    │     • hr.employees의 소유자인가?                                       │
    │     • 또는 GRANT ANY OBJECT PRIVILEGE 권한이 있는가?                    │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  2. 권한 정보 저장                                                      │
    │     • DBA_TAB_PRIVS (객체 권한)                                         │
    │     • DBA_SYS_PRIVS (시스템 권한)                                       │
    │     • DBA_ROLE_PRIVS (롤 권한)                                          │
    │     • GRANTABLE = 'YES' (WITH GRANT OPTION)                            │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  3. hong 사용자가 employees 테이블 접근 시                              │
    │     • 권한 테이블에서 SELECT, INSERT 권한 확인                          │
    │     • 권한 있으면 쿼리 실행                                             │
    │     • 권한 없으면 ORA-00942 에러                                       │
    └─────────────────────────────────────────────────────────────────────────┘

    ─────────────────────────────────────────────────────────────────────────

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  REVOKE SELECT ON hr.employees FROM hong CASCADE;                      │
    └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  1. 권한 회수                                                           │
    │     • DBA_TAB_PRIVS에서 해당 레코드 삭제                               │
    │                                                                        │
    │  2. CASCADE 옵션 시                                                     │
    │     • hong이 GRANT OPTION으로 타인에게 부여한 권한도 회수               │
    │     • 연쇄적 권한 제거                                                  │
    │                                                                        │
    │  3. 즉시 적용                                                           │
    │     • 현재 세션에도 즉시 권한 제거                                      │
    │     • 실행 중인 쿼리는 완료 허용                                        │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
                    [ Role Hierarchy Example ]
================================================================================

                          ┌─────────────┐
                          │     DBA     │ (최고 관리자)
                          │  (Sysdba)   │
                          └──────┬──────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
          ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
          │   DATA_     │ │   SCHEMA_   │ │   AUDIT_    │
          │  ARCHITECT  │ │   OWNER     │ │   ADMIN     │
          └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
                 │               │               │
         ┌───────┴───────┐      │               │
         │               │      │               │
   ┌─────▼─────┐   ┌─────▼─────┐│        ┌─────▼─────┐
   │   READ_   │   │  WRITE_   ││        │  SECURITY │
   │   ONLY    │   │   ACCESS  ││        │  ANALYST  │
   └─────┬─────┘   └─────┬─────┘│        └───────────┘
         │               │      │
         │         ┌─────┴─────┐│
         │         │           ││
   ┌─────▼─────┐   │     ┌─────▼▼─────┐
   │  REPORT_  │   │     │  APP_USER  │ (애플리케이션)
   │  VIEWER   │   │     └────────────┘
   └───────────┘   │
              ┌────▼────┐
              │  BATCH_ │ (배치 사용자)
              │  USER   │
              └─────────┘

================================================================================
```

#### 3. 심층 동작 원리: 권한 확인 메커니즘

**권한 확인 프로세스**

```
1. SQL 파싱 단계에서 권한 확인
├── 사용자 ID 추출 (SESSION_USER)
├── 객체(테이블, 뷰 등) 식별
├── 필요한 권한 결정
│   ├── SELECT → SELECT 권한
│   ├── INSERT → INSERT 권한
│   ├── UPDATE → UPDATE 권한
│   └── DELETE → DELETE 권한
└── 권한 존재 여부 확인

2. 권한 확인 순서 (Oracle)
├── 1단계: 직접 부여된 객체 권한 확인 (DBA_TAB_PRIVS)
├── 2단계: 사용자가 가진 롤의 권한 확인 (DBA_ROLE_PRIVS → DBA_TAB_PRIVS)
├── 3단계: PUBLIC 롤의 권한 확인
└── 4단계: 권한 없으면 ORA-01031: insufficient privileges

3. 권한 상속 체인
├── 직접 권한 > 롤 권한 > PUBLIC 권한
├── DENY가 있으면 GRANT보다 우선 (일부 DBMS)
└── WITH GRANT OPTION으로 부여된 권한은 원본 권한 회수 시 함께 회수
```

#### 4. 실무 수준의 SQL 예시

```sql
-- ==============================================================================
-- DCL 실무 활용 예제: 종합 권한 관리 시스템
-- ==============================================================================

-- [1] 사용자 및 롤 생성
-- ==============================================================================

-- 사용자 생성 (DBA 권한 필요)
CREATE USER app_user IDENTIFIED BY "SecurePass123!"
    DEFAULT TABLESPACE users
    TEMPORARY TABLESPACE temp
    QUOTA 100M ON users
    PROFILE default
    PASSWORD EXPIRE
    ACCOUNT UNLOCK;

CREATE USER readonly_user IDENTIFIED BY "ReadOnly456!"
    DEFAULT TABLESPACE users
    QUOTA 0 ON users;  -- 쓰기 공간 없음

CREATE USER batch_user IDENTIFIED BY "Batch789!"
    DEFAULT TABLESPACE users
    QUOTA 500M ON users;

-- 롤 생성
CREATE ROLE app_readonly;
CREATE ROLE app_readwrite;
CREATE ROLE app_admin;
CREATE ROLE batch_processor;

-- [2] 시스템 권한 부여
-- ==============================================================================

-- 롤에 시스템 권한 부여
GRANT CREATE SESSION TO app_readonly;  -- 로그인 권한
GRANT CREATE SESSION TO app_readwrite;
GRANT CREATE SESSION TO app_admin;

-- 추가 시스템 권한
GRANT CREATE TABLE, CREATE VIEW, CREATE PROCEDURE TO app_admin;
GRANT CREATE TABLE TO batch_processor;

-- [3] 객체 권한 부여 (GRANT)
-- ==============================================================================

-- 읽기 전용 권한
GRANT SELECT ON hr.employees TO app_readonly;
GRANT SELECT ON hr.departments TO app_readonly;
GRANT SELECT ON hr.jobs TO app_readonly;
GRANT SELECT ON sales.orders TO app_readonly;
GRANT SELECT ON sales.customers TO app_readonly;

-- 읽기/쓰기 권한
GRANT SELECT, INSERT, UPDATE ON hr.employees TO app_readwrite;
GRANT SELECT, INSERT, UPDATE ON sales.orders TO app_readwrite;
GRANT SELECT, INSERT, UPDATE, DELETE ON sales.order_items TO app_readwrite;

-- 관리자 권한 (모든 권한 + 권한 위임)
GRANT ALL ON hr.employees TO app_admin WITH GRANT OPTION;
GRANT ALL ON hr.departments TO app_admin WITH GRANT OPTION;
GRANT ALL ON sales.orders TO app_admin WITH GRANT OPTION;

-- 배치 사용자 권한
GRANT SELECT, INSERT, UPDATE ON sales.orders TO batch_processor;
GRANT EXECUTE ON pkg_batch_process TO batch_processor;

-- 특정 컬럼에만 권한 부여 (컬럼 수준 보안)
GRANT SELECT (employee_id, first_name, last_name, hire_date)
    ON hr.employees TO readonly_user;
-- 급여 컬럼(salary)은 조회 불가

-- [4] 롤을 사용자에게 부여
-- ==============================================================================

GRANT app_readonly TO readonly_user;
GRANT app_readwrite TO app_user;
GRANT app_admin TO dba_user;
GRANT batch_processor TO batch_user;

-- 여러 롤 동시 부여
GRANT app_readonly, app_readwrite TO senior_user;

-- [5] 권한 회수 (REVOKE)
-- ==============================================================================

-- 특정 권한 회수
REVOKE UPDATE ON hr.employees FROM app_readwrite;

-- 모든 권한 회수
REVOKE ALL ON hr.employees FROM app_admin;

-- 롤 회수
REVOKE app_readonly FROM readonly_user;

-- CASCADE: 위임된 권한도 함께 회수
REVOKE SELECT ON hr.employees FROM hong CASCADE;

-- [6] 권한 조회
-- ==============================================================================

-- 사용자별 시스템 권한 조회
SELECT
    grantee,
    privilege,
    admin_option
FROM dba_sys_privs
WHERE grantee = 'APP_USER'
ORDER BY privilege;

-- 사용자별 객체 권한 조회
SELECT
    grantee,
    owner || '.' || table_name AS object_name,
    privilege,
    grantable,
    hierarchy
FROM dba_tab_privs
WHERE grantee = 'APP_USER'
ORDER BY owner, table_name, privilege;

-- 사용자가 가진 롤 조회
SELECT
    grantee,
    granted_role,
    admin_option,
    default_role
FROM dba_role_privs
WHERE grantee IN ('APP_USER', 'READONLY_USER')
ORDER BY grantee, granted_role;

-- 롤에 부여된 권한 조회
SELECT
    role,
    owner || '.' || table_name AS object_name,
    privilege
FROM role_tab_privs
WHERE role = 'APP_READONLY'
ORDER BY owner, table_name;

-- PUBLIC 권한 확인 (보안 점검용)
SELECT
    owner || '.' || table_name AS object_name,
    privilege
FROM dba_tab_privs
WHERE grantee = 'PUBLIC'
ORDER BY owner, table_name;

-- [7] 행 수준 보안 (Row-Level Security)
-- ==============================================================================

-- Oracle VPD (Virtual Private Database) 예시

-- 정책 함수 생성
CREATE OR REPLACE FUNCTION sec_persons_by_region(
    p_schema IN VARCHAR2,
    p_object IN VARCHAR2
) RETURN VARCHAR2 IS
    v_region_id VARCHAR2(10);
BEGIN
    -- 사용자의 지역 ID 조회
    SELECT region_id INTO v_region_id
    FROM app_users
    WHERE username = SYS_CONTEXT('USERENV', 'SESSION_USER');

    -- 지역별 데이터만 조회하도록 조건 반환
    RETURN 'region_id = ''' || v_region_id || '''';
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN '1=0';  -- 데이터 없음
END;
/

-- 정책 적용
BEGIN
    DBMS_RLS.ADD_POLICY(
        object_schema   => 'HR',
        object_name     => 'EMPLOYEES',
        policy_name     => 'EMP_REGION_POLICY',
        function_schema => 'SEC_ADMIN',
        policy_function => 'SEC_PERSONS_BY_REGION',
        statement_types => 'SELECT, INSERT, UPDATE, DELETE',
        enable          => TRUE
    );
END;
/

-- [8] 감사(Audit) 설정
-- ==============================================================================

-- 권한 사용 감사
AUDIT SELECT TABLE, INSERT TABLE, UPDATE TABLE, DELETE TABLE
    BY app_user BY ACCESS;

-- 특정 테이블 감사
AUDIT SELECT, INSERT, UPDATE, DELETE
    ON hr.employees BY ACCESS;

-- 권한 부여/회수 감사
AUDIT GRANT ANY OBJECT PRIVILEGE, GRANT ANY PRIVILEGE
    BY ACCESS;

-- 감사 로그 조회
SELECT
    os_username,
    username,
    userhost,
    timestamp,
    action_name,
    obj_name,
    sql_text
FROM dba_audit_trail
WHERE username IN ('APP_USER', 'READONLY_USER')
  AND timestamp >= SYSDATE - 7
ORDER BY timestamp DESC;

-- [9] 동적 데이터 마스킹 (Dynamic Data Masking)
-- ==============================================================================

-- SQL Server 예시
-- CREATE TABLE customers (
--     customer_id INT,
--     customer_name VARCHAR(100),
--     email VARCHAR(100) MASKED WITH (FUNCTION = 'partial(2, "xxxx", 2)'),
--     phone VARCHAR(20) MASKED WITH (FUNCTION = 'default()'),
--     credit_card VARCHAR(20) MASKED WITH (FUNCTION = 'partial(0, "xxxx-xxxx-xxxx-", 4)')
-- );

-- GRANT SELECT ON customers TO readonly_user;
-- readonly_user가 조회하면 email, phone, credit_card가 마스킹됨

-- [10] 권한 관리 모범 사례 스크립트
-- ==============================================================================

-- 사용자 비활성화 (계정 잠금)
ALTER USER app_user ACCOUNT LOCK;

-- 비밀번호 만료 강제
ALTER USER app_user PASSWORD EXPIRE;

-- 사용자 삭제 (권한 자동 회수)
DROP USER app_user CASCADE;

-- PUBLIC 권한 회수 (보안 강화)
REVOKE EXECUTE ON UTL_FILE FROM PUBLIC;
REVOKE EXECUTE ON UTL_HTTP FROM PUBLIC;
REVOKE EXECUTE ON DBMS_SCHEDULER FROM PUBLIC;

-- 불필요한 권한 정리 프로시저
CREATE OR REPLACE PROCEDURE cleanup_unused_privileges IS
    CURSOR c_unused IS
        SELECT grantee, privilege
        FROM dba_sys_privs
        WHERE grantee NOT IN ('SYS', 'SYSTEM', 'DBA')
          AND NOT EXISTS (
              SELECT 1 FROM dba_audit_trail
              WHERE username = dba_sys_privs.grantee
                AND action_name LIKE '%' || dba_sys_privs.privilege || '%'
                AND timestamp > SYSDATE - 90
          );
BEGIN
    FOR r IN c_unused LOOP
        DBMS_OUTPUT.PUT_LINE('Unused: ' || r.grantee || ' - ' || r.privilege);
        -- EXECUTE IMMEDIATE 'REVOKE ' || r.privilege || ' FROM ' || r.grantee;
    END LOOP;
END;
/
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 접근 통제 모델 비교

| 접근 통제 모델 | 특징 | 장점 | 단점 | 적용 분야 |
|:---|:---|:---|:---|:---|
| **DAC** | 소유자가 권한 부여 | 유연성 | 관리 복잡 | 일반 DB |
| **RBAC** | 롤 기반 권한 관리 | 관리 용이 | 롤 폭증 | 기업 시스템 |
| **ABAC** | 속성 기반 접근 제어 | 세밀한 제어 | 구현 복잡 | 클라우드 |
| **MAC** | 강제 접근 통제 | 보안 강함 | 유연성 부족 | 군사/정부 |

#### 2. DBMS별 DCL 구현 차이

| 기능 | Oracle | PostgreSQL | MySQL | SQL Server |
|:---|:---|:---|:---|:---|
| **롤 지원** | O | O | X (8.0+) | O |
| **행 수준 보안** | VPD | RLS | View/Trigger | RLS |
| **동적 마스킹** | X (19c+) | O (Extension) | O (8.0+) | O (2016+) |
| **감사** | Audit | pgAudit | Enterprise Audit | SQL Audit |
| **WITH GRANT OPTION** | O | O | O | O (WITH GRANT) |

#### 3. 과목 융합 관점 분석

**[보안 융합] 데이터 보안 3요소**
- 기밀성(Confidentiality): DCL로 접근 통제
- 무결성(Integrity): 권한별 허용 작업 제한
- 가용성(Availability): 권한 문제로 서비스 거부 방지

**[감사 융합] 컴플라이언스**
- GDPR: 개인정보 접근 권한 최소화
- ISMS: 권한 부여/회수 이력 관리
- SOX: 재무 데이터 접근 통제

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

- **시나리오 1: 내부자 위협 방지**
  - 상황: 퇴사자의 데이터 유출 우려
  - 판단:
    1. 퇴사 즉시 계정 잠금 (ACCOUNT LOCK)
    2. PUBLIC 권한 최소화로 예방
    3. 민감 데이터는 행 수준 보안 적용
    4. 모든 권한 사용에 감사 로그 기록

- **시나리오 2: 애플리케이션 계정 권한 설계**
  - 상황: 웹 애플리케이션 DB 접근 권한 설계
  - 판단:
    1. 읽기 전용 계정과 읽기/쓰기 계정 분리
    2. DDL 권한은 절대 부여하지 않음
    3. 저장 프로시저 실행 권한만 부여 (간접 접근)
    4. connection pool별로 다른 계정 사용

- **시나리오 3: 규제 준수 감사 대응**
  - 상황: ISMS 인증 심사
  - 판단:
    1. 권한 부여/회수 이력 문서화
    2. 불필요한 권한 정기 검토 프로세스
    3. 권한 분리(Segregation of Duties) 구현
    4. 감사 로그 보존 정책 수립

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **최소 권한 원칙**: 필요한 최소 권한만 부여
- [ ] **권한 분리**: 개발/운영/감시 권한 분리
- [ ] **PUBLIC 권한 정리**: 불필요한 PUBLIC 권한 회수
- [ ] **감사 로그**: 권한 부여/회수/사용 감사
- [ ] **정기 검토**: 분기별 권한 검토 프로세스
- [ ] **비상 대응**: 권한 문제 시 빠른 대응 체계

#### 3. 안티패턴 (Anti-patterns)

- **과도한 권한 부여**: 편의를 위해 ALL PRIVILEGES 부여
- **PUBLIC 권한 방치**: 기본 PUBLIC 권한을 회수하지 않음
- **권한 문서화 누락**: 누가 어떤 권한을 가졌는지 모름
- **감사 미설정**: 권한 사용 이력을 추적하지 않음
- **공용 계정**: 여러 사람이 하나의 계정 공유

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 효과 영역 | 내용 | 정량적 지표 |
|:---|:---|:---|
| **보안** | 무단 접근 차단 | 데이터 유출 0건 |
| **규정 준수** | ISMS/GDPR 대응 | 감사 지적 0건 |
| **운영 효율** | 롤 기반 관리 | 권한 관리 시간 70% 단축 |
| **추적성** | 감사 로그 확보 | 포렌식 대응 가능 |

#### 2. 미래 전망

DCL은 **AI 기반 접근 통제**로 진화합니다:

1. **자동 권한 최적화**: AI가 사용 패턴 분석하여 불필요한 권한 제안
2. **제로 트러스트 DB**: 모든 요청을 실시간으로 평가
3. **동적 권한 부여**: 컨텍스트(시간, 위치, 디바이스) 기반 권한
4. **통합 ID 관리**: IAM과 DB 권한의 완전 통합

#### 3. 참고 표준

- **ISO/IEC 27001**: 정보보안 관리 체계
- **NIST SP 800-53**: 접근 통제 통제 항목
- **ANSI/ISO SQL**: GRANT/REVOKE 표준 문법
- **GDPR Article 32**: 접근 통제 요건

---

### 관련 개념 맵 (Knowledge Graph)

- **[DDL (Data Definition Language)](@/studynotes/5_database/1_relational/18_ddl_dml_dcl_tcl.md)**: DCL로 제어되는 객체 생성
- **[DML (Data Manipulation Language)](@/studynotes/5_database/1_relational/21_dml_data_manipulation_language.md)**: DCL로 제어되는 데이터 조작
- **[뷰 (View)](@/studynotes/5_database/_keyword_list.md)**: 행/열 수준 보안 구현 수단
- **[감사 (Audit)](@/studynotes/5_database/_keyword_list.md)**: 권한 사용 추적
- **[DBA](@/studynotes/5_database/1_relational/20_dba_database_administrator.md)**: 권한 관리 책임자

---

### 어린이를 위한 3줄 비유 설명

1. **출입 카드**: DCL은 학교에서 학생증이나 교직원증을 주는 것과 같아요. 학생은 교실에만 들어갈 수 있고, 선생님은 교무실에도 들어갈 수 있어요.

2. **GRANT와 REVOKE**: 출입 카드를 주는 것이 GRANT이고, 뺏는 것이 REVOKE예요. 졸업하면 학생증을 반납해야 하듯이, 퇴사하면 권한도 회수해요.

3. **역할(Role)**: "운동부"나 "반장"처럼 역할을 정해두면, 그 역할에 맞는 권한을 한 번에 줄 수 있어요. 반장은 교무실 출입 권한이 있을 수 있죠!
