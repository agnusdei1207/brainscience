+++
title = "시스템 카탈로그 (System Catalog) / 데이터 사전 (Data Dictionary)"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
+++

# 시스템 카탈로그 (System Catalog) / 데이터 사전 (Data Dictionary)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시스템 카탈로그는 DBMS가 데이터베이스의 구조, 제약조건, 사용자 권한, 인덱스 정보 등 모든 메타데이터(Metadata)를 체계적으로 저장하고 관리하는 내부 데이터베이스로, '데이터에 대한 데이터'를 의미하는 데이터 사전(Data Dictionary)의 물리적 구현체입니다.
> 2. **가치**: 옵티마이저의 실행 계획 수립, 무결성 제약조건 검증, 접근 통제(Access Control) 등 DBMS 핵심 기능의 효율성을 300% 이상 향상시키며, 사용자와 DBA가 데이터베이스 구조를 신속하게 파악할 수 있는 단일 진실 공급원(Single Source of Truth) 역할을 수행합니다.
> 3. **융합**: 운영체제의 파일 시스템 메타데이터(inode, superblock) 개념과 연계되며, 데이터 거버넌스(Data Governance) 프레임워크의 메타데이터 관리(Metadata Management) 기반 기술로 확장되어 기업 데이터 자산 관리의 핵심 인프라를 구성합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**시스템 카탈로그(System Catalog)**는 데이터베이스 관리 시스템(DBMS) 내부에서 자체적으로 생성하고 유지관리하는 특수한 테이블들의 집합으로, 데이터베이스에 저장된 데이터의 구조, 타입, 관계, 인덱스, 뷰, 사용자 권한, 제약조건 등 모든 스키마 정보를 저장합니다. 이를 **메타데이터(Metadata)**라고 하며, '데이터에 대한 데이터'라는 의미에서 **데이터 사전(Data Dictionary)** 또는 **데이터 딕셔너리(Data Dictionary)**라고도 불립니다.

시스템 카탈로그는 일반 사용자 테이블과 달리 DBMS가 자동으로 관리하며, DDL(CREATE, ALTER, DROP) 명령이 실행될 때마다 실시간으로 갱신됩니다. 사용자는 SELECT 문을 통해서만 조회할 수 있으며, 직접적인 INSERT/UPDATE/DELETE는 엄격히 금지됩니다. 이는 메타데이터의 무결성을 보장하기 위한 핵심 설계 원칙입니다.

#### 2. 💡 비유를 통한 이해
시스템 카탈로그는 **'도서관의 도서 목록 카드 시스템'**에 비유할 수 있습니다.
- 도서관에 있는 수만 권의 책(실제 데이터)을 찾기 위해서는 책 제목, 저자, 출판연도, 위치(서가 번호) 등의 정보가 기록된 목록 카드(메타데이터)가 필요합니다.
- 사서가 새 책을 입고하거나 폐기할 때마다 목록 카드도 자동으로 갱신되어야 하며, 일반 이용자는 목록 카드를 읽을 수만 있고 임의로 수정할 수 없습니다.
- 목록 카드가 없으면 도서관의 책들은 단순한 종이 더미에 불과하며, 원하는 정보를 찾는 것은 불가능에 가깝습니다.

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 초기 파일 처리 시스템에서는 데이터의 구조 정보가 애플리케이션 코드에 하드코딩되어 있었습니다. 스키마가 변경될 때마다 관련된 모든 프로그램을 수정해야 했으며, 데이터의 의미나 구조를 파악하기 위해서는 소스 코드를 직접 분석해야 하는 비효율적인 구조였습니다.

2. **혁신적 패러다임의 도입**: 1970년대 CODASYL(Conference on Data Systems Languages) 위원회에서 데이터 사전의 개념을 정립하고, 데이터의 정의를 중앙 집중화하여 데이터 독립성을 확보하는 방향으로 발전했습니다. 이후 관계형 데이터베이스의 등장과 함께 시스템 테이블 형태의 물리적 구현체인 시스템 카탈로그가 표준화되었습니다.

3. **비즈니스적 요구사항**: 현대 기업 환경에서는 데이터 자산의 파악, 영향 분석(Impact Analysis), 규제 대응(GDPR, CCPA 등)을 위해 데이터의 출처, 변환 이력, 접근 권한 등을 추적하는 메타데이터 관리가 필수적이 되었습니다. 시스템 카탈로그는 이러한 데이터 거버넌스의 기반 인프라 역할을 수행합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 시스템 카탈로그 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 저장 정보 | 비유 |
|:---|:---|:---|:---|:---|
| **SYSOBJECTS** | 데이터베이스 객체 정보 관리 | 객체 생성 시 ID 부여 및 타입별 분류 저장 | 테이블, 뷰, 인덱스, 프로시저 등 객체 메타데이터 | 도서관 자산 대장 |
| **SYSCOLUMNS** | 컬럼(속성) 정보 관리 | 테이블별 컬럼 순서, 타입, 길이 등 상세 정의 | 컬럼명, 데이터 타입, NULL 허용 여부, 기본값 | 책 상세 정보 카드 |
| **SYSINDEXES** | 인덱스 구조 정보 관리 | 인덱스 생성 시 B+Tree 구조 메타데이터 저장 | 인덱스명, 키 컬럼, 높이, 리프 페이지 수 | 색인 카드 |
| **SYSCONSTRAINTS** | 제약조건 정보 관리 | 무결성 규칙 정의 및 위반 시 액션 지정 | PK, FK, CHECK, UNIQUE 제약조건 | 대출 규정 안내문 |
| **SYSUSERS** | 사용자 및 권한 정보 관리 | 인증(Authentication) 및 인가(Authorization) 지원 | 사용자명, 역할(Role), 객체별 권한 | 회원 명부 |
| **SYSVIEWS** | 뷰 정의 정보 관리 | 뷰 생성 SQL문 저장 및 의존성 추적 | 뷰명, 정의 SQL, 기반 테이블 정보 | 가상 도서 목록 |
| **SYSPROCEDURES** | 저장 프로시저/트리거 관리 | 컴파일된 실행 코드 및 파라미터 정보 저장 | 프로시저명, 파라미터, 실행 계획 | 작업 매뉴얼 |
| **SYSSTATISTICS** | 통계 정보 관리 | 옵티마이저를 위한 데이터 분포 정보 수집 | 테이블 행 수, 컬럼 카디널리티, 히스토그램 | 도서 대출 통계 |

#### 2. 시스템 카탈로그 아키텍처 다이어그램

```text
================================================================================
                     [ Database Management System Architecture ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                           [ Query Processor ]                                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────────────┐  │
│  │   Parser     │───>│  Optimizer   │───>│   Execution Engine           │  │
│  │ (SQL Parsing)│    │(Plan Making) │    │  (Plan Execution)            │  │
│  └──────────────┘    └──────┬───────┘    └──────────────────────────────┘  │
└─────────────────────────────│───────────────────────────────────────────────┘
                              │
                              │ Read Metadata
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     [ System Catalog (Data Dictionary) ]                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐    │
│  │   SYSOBJECTS       │  │   SYSCOLUMNS       │  │   SYSINDEXES       │    │
│  │  ───────────────   │  │  ───────────────   │  │  ───────────────   │    │
│  │  obj_id | name     │  │  col_id | name     │  │  idx_id | name     │    │
│  │  type   | crdate   │  │  type   | length   │  │  root   | levels   │    │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘    │
│                                                                              │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐    │
│  │   SYSCONSTRAINTS   │  │   SYSUSERS         │  │   SYSSTATISTICS    │    │
│  │  ───────────────   │  │  ───────────────   │  │  ───────────────   │    │
│  │  const_id | type   │  │  user_id| name     │  │  tab_id | rows     │    │
│  │  cols    | rule    │  │  role   | privs    │  │  dist   | histogram│    │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘    │
│                                                                              │
│  [ Cache Layer: Data Dictionary Cache in Shared Pool/Buffer Pool ]          │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  LRU Cache for frequently accessed metadata (Parsed SQL, Plans)   │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ DDL Trigger Update
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       [ User Data Storage ]                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Table Data Files | Index Data Files | Transaction Log Files       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
                    [ System Catalog Access Flow ]
================================================================================
1. DDL Execution (CREATE TABLE employees (...))
   └──> Parser validates syntax
   └──> System Catalog locked (exclusive for DDL)
   └──> New entries inserted into SYSOBJECTS, SYSCOLUMNS, SYSCONSTRAINTS
   └──> Data files allocated for physical storage

2. DML Execution (SELECT * FROM employees WHERE dept = 'IT')
   └──> Parser checks if 'employees' exists in SYSOBJECTS (cache miss -> disk read)
   └──> Optimizer reads SYSSTATISTICS for cardinality estimates
   └──> Optimizer reads SYSINDEXES for available access paths
   └──> Execution plan generated and cached

3. DCL Execution (GRANT SELECT ON employees TO user01)
   └──> Permission validation against SYSUSERS
   └──> New entry in system privilege tables
   └──> Cache invalidation for affected users
================================================================================
```

#### 3. 심층 동작 원리: DDL 처리와 카탈로그 갱신

DDL(Data Definition Language) 명령이 실행될 때 시스템 카탈로그는 다음과 같은 단계로 갱신됩니다:

1. **구문 분석 및 권한 검증**: Parser가 DDL 문법을 분석하고, 현재 사용자가 해당 객체에 대한 CREATE/ALTER/DROP 권한을 가지고 있는지 SYSUSERS 테이블에서 확인합니다.

2. **배타적 잠금 획득**: 시스템 카탈로그에 대한 동시 변경을 방지하기 위해 메타데이터 잠금(Metadata Lock)을 획득합니다. 이는 DDL 수행 중 다른 세션의 DDL/DML을 대기시킵니다.

3. **의존성 검사**: DROP이나 ALTER의 경우, 해당 객체를 참조하는 다른 객체(외래키, 뷰, 프로시저 등)가 있는지 SYSDEPENDS 테이블에서 조회하여 연쇄 영향을 분석합니다.

4. **메타데이터 갱신**: 트랜잭션 내에서 관련 시스템 테이블들에 INSERT/UPDATE/DELETE를 수행합니다. 이때 카탈로그 변경 사항도 로그에 기록되어 장애 시 복구 가능합니다.

5. **캐시 무효화**: 공유 풀(Shared Pool)에 캐싱된 관련 실행 계획과 파싱 트리를 무효화하여, 다음 쿼리 수행 시 갱신된 메타데이터를 참조하도록 합니다.

#### 4. 실무 수준의 SQL 및 내부 동작 예시

```sql
-- ========================================
-- 시스템 카탈로그 조회 예시 (SQL Server)
-- ========================================

-- 1. 사용자 테이블 목록 조회
SELECT t.object_id, t.name, t.create_date, t.modify_date,
       s.name AS schema_name
FROM   sys.tables t
JOIN   sys.schemas s ON t.schema_id = s.schema_id
ORDER  BY t.name;

-- 2. 특정 테이블의 컬럼 상세 정보
SELECT c.name AS column_name,
       ty.name AS data_type,
       c.max_length,
       c.precision,
       c.is_nullable,
       c.is_identity
FROM   sys.columns c
JOIN   sys.types ty ON c.user_type_id = ty.user_type_id
WHERE  c.object_id = OBJECT_ID('dbo.employees');

-- 3. 인덱스 구조 분석
SELECT i.name AS index_name,
       i.type_desc,
       i.is_unique,
       i.is_primary_key,
       c.name AS column_name,
       ic.is_descending_key
FROM   sys.indexes i
JOIN   sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
JOIN   sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
WHERE  i.object_id = OBJECT_ID('dbo.employees')
ORDER  BY i.name, ic.key_ordinal;

-- 4. 외래키 제약조건 조회
SELECT fk.name AS fk_name,
       tp.name AS parent_table,
       ref.name AS referenced_table,
       c.name AS column_name
FROM   sys.foreign_keys fk
JOIN   sys.tables tp ON fk.parent_object_id = tp.object_id
JOIN   sys.tables ref ON fk.referenced_object_id = ref.object_id
JOIN   sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
JOIN   sys.columns c ON fkc.parent_object_id = c.object_id AND fkc.parent_column_id = c.column_id;

-- ========================================
-- Oracle 시스템 카탈로그 조회 (데이터 딕셔너리 뷰)
-- ========================================

-- 1. 모든 테이블 조회 (USER_TABLES, ALL_TABLES, DBA_TABLES)
SELECT table_name, num_rows, blocks, avg_row_len, last_analyzed
FROM   user_tables
ORDER  BY table_name;

-- 2. 컬럼 정보 (USER_TAB_COLUMNS)
SELECT column_name, data_type, data_length, nullable, data_default
FROM   user_tab_columns
WHERE  table_name = 'EMPLOYEES';

-- 3. 인덱스 정보 (USER_INDEXES, USER_IND_COLUMNS)
SELECT i.index_name, i.index_type, c.column_name, c.column_position
FROM   user_indexes i
JOIN   user_ind_columns c ON i.index_name = c.index_name
WHERE  i.table_name = 'EMPLOYEES';

-- 4. 제약조건 정보 (USER_CONSTRAINTS)
SELECT constraint_name, constraint_type,
       search_condition, r_constraint_name
FROM   user_constraints
WHERE  table_name = 'EMPLOYEES';
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 주요 DBMS별 시스템 카탈로그 비교

| 비교 항목 | Oracle | SQL Server | MySQL | PostgreSQL |
|:---|:---|:---|:---|:---|
| **카탈로그 명칭** | Data Dictionary | System Catalog | Information Schema | System Catalog |
| **주요 저장 위치** | SYSTEM 테이블스페이스 | master 데이터베이스 | mysql 데이터베이스 | pg_catalog 스키마 |
| **조회 인터페이스** | DBA_/ALL_/USER_ 뷰 | sys.*/INFORMATION_SCHEMA | INFORMATION_SCHEMA | pg_catalog.* |
| **메타데이터 캐시** | Shared Pool (Row Cache) | Buffer Pool + Plan Cache | Table Definition Cache | RelCache + CatCache |
| **통계 정보 관리** | DBMS_STATS 패키지 | UPDATE STATISTICS | ANALYZE TABLE | ANALYZE |
| **실시간 갱신** | DDL 즉시 반영 | DDL 즉시 반영 | DDL 즉시 반영 | DDL 즉시 반영 |

#### 2. 데이터 사전(Data Dictionary) vs 데이터 디렉터리(Data Directory) 비교

| 구분 | 데이터 사전 (Data Dictionary) | 데이터 디렉터리 (Data Directory) |
|:---|:---|:---|
| **정의** | 사용자와 DBMS가 모두 접근 가능한 메타데이터 저장소 | DBMS 내부적으로만 접근 가능한 메타데이터 저장소 |
| **접근 권한** | SELECT 권한으로 조회 가능 (DBA_/USER_ 뷰) | 시스템 내부 전용, 사용자 직접 접근 불가 |
| **저장 내용** | 테이블 구조, 인덱스, 뷰 정의, 권한 등 | 내부 포인터, 버퍼 정보, 락 상태 등 |
| **활용 목적** | 사용자 쿼리, 보고서, 데이터 분석 | DBMS 성능 최적화, 무결성 검증 |
| **표준화** | ANSI/ISO SQL 표준 (INFORMATION_SCHEMA) | DBMS 벤더별 독자적 구현 |

#### 3. 과목 융합 관점 분석

- **[운영체제 융합] 파일 시스템 메타데이터와의 연계**: OS의 파일 시스템은 inode, superblock 등의 메타데이터를 통해 파일의 위치, 크기, 권한을 관리합니다. DBMS의 시스템 카탈로그는 이와 유사한 개념이지만, 데이터의 논리적 구조(스키마)까지 포함하여 더 풍부한 정보를 제공합니다. DBMS는 OS 파일 시스템 위에 구축되므로, 두 계층의 메타데이터가 일관성을 유지하는 것이 중요합니다.

- **[보안 융합] 접근 통제와 감사 추적**: 시스템 카탈로그의 SYSUSERS, SYSPRIVS 테이블은 RBAC(Role-Based Access Control) 구현의 기반이 됩니다. 또한, 메타데이터 변경 이력을 추적함으로써 누가 언제 어떤 스키마 변경을 수행했는지 감사(Audit) 기능을 제공합니다. ISMS, SOX, GDPR 등 규제 준수를 위한 필수 요소입니다.

- **[네트워크 융합] 분산 DB의 글로벌 카탈로그**: 분산 데이터베이스 환경에서는 각 노드의 로컬 카탈로그뿐만 아니라, 전체 분산 시스템의 데이터 위치를 파악하는 글로벌 카탈로그(Global Catalog)가 필요합니다. 이는 위치 투명성(Location Transparency)을 제공하는 핵심 인프라입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

- **시나리오 1: 대량 DDL 배치 수행 시 성능 저하**
  - 상황: 야간 배치로 500개 테이블의 스키마를 변경해야 하는데, DDL 수행 중 시스템 전체가 응답하지 않는 현상 발생.
  - 판단: DDL은 시스템 카탈로그에 배타적 잠금을 걸므로, 연속된 DDL 수행 시 메타데이터 잠금 대기가 누적됩니다. 기술사는 DDL을 작은 단위로 분할하고, `wait_timeout` 설정을 조정하며, low-peak 시간대에 분산 실행하는 전략을 수립해야 합니다.

- **시나리오 2: 통계 정보 부정확으로 인한 실행 계획 오류**
  - 상황: 데이터 이관 후 특정 쿼리의 성능이 100배 저하됨. 원인 분석 결과, 시스템 카탈로그의 통계 정보(SYSSTATISTICS)가 갱신되지 않아 옵티마이저가 잘못된 실행 계획을 수립함.
  - 판단: 대량 데이터 적재 후에는 반드시 통계 정보 갱신(ANALYZE/UPDATE STATISTICS)을 수행해야 합니다. 기술사는 자동 통계 수집 작업(Auto-Analyzer)을 모니터링하고, 필요시 수동으로 즉시 갱신하는 운영 프로세스를 확립해야 합니다.

- **시나리오 3: 카탈로그 손상에 의한 DB 시작 실패**
  - 상황: 정전 후 DB 재기작 시 "catalog corruption" 에러로 인해 DB가 시작되지 않음.
  - 판단: 시스템 카탈로그는 DBMS의 뇌와 같아서 손상 시 복구가 매우 어렵습니다. 기술사는 정기적인 카탈로그 백업(mysqldump --all-databases --routines --triggers), 바이너리 로그 보관, 그리고 벤더 기술 지원 요청 프로세스를 사전에 정립해야 합니다.

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **카탈로그 캐시 크기**: Shared Pool, Buffer Pool 내 카탈로그 캐시 영역의 적절한 크기 설정 (전체 메모리의 10-15% 권장)
- [ ] **통계 정보 갱신 주기**: 데이터 변동량에 따른 자동 통계 수집 주기 설정 (일일/주간)
- [ ] **메타데이터 잠금 타임아웃**: DDL 대기로 인한 애플리케이션 타임아웃 방지를 위한 `lock_wait_timeout` 설정
- [ ] **카탈로그 백업 전략**: 일반 데이터 백업과 별도로 메타데이터 전용 백업 스케줄 수립
- [ ] **접근 권한 최소화**: 일반 사용자의 시스템 카탈로그 조회 권한 제한 (민감 정보 노출 방지)

#### 3. 안티패턴 (Anti-patterns)

- **직접 카탈로그 수정**: 사용자가 `UPDATE sysobjects SET ...` 등으로 시스템 카탈로그를 직접 수정하는 것은 치명적입니다. 무결성 파괴, DB 시작 실패, 데이터 손실 등 복구 불가능한 장애를 유발합니다. 반드시 DDL 명령을 통해서만 갱신해야 합니다.

- **통계 정보 수집 생략**: "통계 수집은 성능을 저하시킨다"는 오해로 통계 정보를 수집하지 않으면, 옵티마이저가 최악의 실행 계획을 수립하여 전체 시스템 성능이 급락할 수 있습니다.

- **카탈로그 조회 쿼리 과다**: 모니터링 시스템이 1초마다 시스템 카탈로그를 조회하면, 메타데이터 잠금 경합이 발생하여 실제 업무 쿼리의 성능이 저하됩니다. 조회 주기를 30초 이상으로 설정하거나, 성능 뷰(DMV)를 활용해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 효과 영역 | 내용 | 목표 수치 |
|:---|:---|:---|
| **쿼리 성능 최적화** | 정확한 통계 정보 기반 실행 계획 수립 | 평균 쿼리 응답시간 40% 단축 |
| **데이터 무결성 보장** | 자동 제약조건 검증 | 무결성 위반 0건 |
| **운영 효율성** | 신속한 스키마 파악 및 영향 분석 | 장애 대응 시간 60% 단축 |
| **규제 준수** | 메타데이터 기반 데이터 자산 관리 | 감사 지적사항 90% 감소 |

#### 2. 미래 전망

시스템 카탈로그는 **AI 기반 자율 데이터베이스(Autonomous Database)**의 핵심 구성 요소로 진화하고 있습니다. Oracle Autonomous Database와 같은 차세대 DBMS는 머신러닝 알고리즘을 통해 통계 정보를 자동 수집하고, 인덱스를 자동 생성/삭제하며, 스키마를 자동 튜닝하는 기능을 제공합니다.

또한, **데이터 메시(Data Mesh)** 아키텍처의 확산과 함께 분산된 데이터 도메인 간의 메타데이터 표준화 및 연계를 위한 기술(Apache Atlas, DataHub 등)이 주목받고 있으며, 시스템 카탈로그의 개념이 단일 DBMS를 넘어 전사적 메타데이터 관리 플랫폼으로 확장되고 있습니다.

#### 3. 참고 표준

- **ANSI/ISO SQL-92/99**: INFORMATION_SCHEMA 표준 뷰 정의
- **ISO/IEC 11179**: 메타데이터 레지스트리(Metadata Registry) 표준
- **DCMI (Dublin Core Metadata Initiative)**: 메타데이터 요소 표준

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[3단계 스키마 아키텍처](@/studynotes/5_database/1_relational/three_schema_architecture.md)**: 시스템 카탈로그는 개념 스키마와 내부 스키마의 메타데이터를 저장하는 저장소입니다.
- **[데이터 독립성](@/studynotes/5_database/1_relational/data_independence.md)**: 카탈로그는 논리적/물리적 데이터 독립성을 구현하기 위한 매핑 정보를 관리합니다.
- **[옵티마이저](@/studynotes/5_database/3_optimization/query_optimization.md)**: 비용 기반 옵티마이저는 시스템 카탈로그의 통계 정보를 기반으로 실행 계획을 수립합니다.
- **[DBMS 언어 (DDL/DML/DCL)](@/studynotes/5_database/1_relational/ddl_dml_dcl.md)**: DDL 명령은 시스템 카탈로그를 자동으로 갱신합니다.
- **[데이터 거버넌스](@/studynotes/5_database/_index.md)**: 시스템 카탈로그는 기업 데이터 거버넌스의 기반 인프라입니다.

---

### 👶 어린이를 위한 3줄 비유 설명

1. **도서관 목록 카드**: 시스템 카탈로그는 도서관에 어떤 책들이 있는지, 어디에 있는지, 누가 빌릴 수 있는지 적어둔 목록 카드 같아요.
2. **자동으로 갱신되는 목록**: 사서가 새 책을 넣거나 없앨 때마다 목록 카드도 저절로 바뀌어요. 누구나 목록은 볼 수 있지만, 마음대로 고칠 수는 없어요.
3. **빠른 책 찾기**: 이 목록이 있어야 도서관에서 원하는 책을 금방 찾을 수 있어요. 목록이 없으면 수만 권의 책 속에서 헤매게 될 거예요!
