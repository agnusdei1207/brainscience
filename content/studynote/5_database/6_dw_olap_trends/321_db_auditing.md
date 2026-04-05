+++
title = "321. DB 감사 (DB Auditing)"
weight = 4321
+++

> **💡 핵심 인사이트**
> DB 감사(DB Auditing)는 **"데이터베이스 내에서 어떤 사용자가, 언제, 무슨 객체에, 어떤 操作을 했는지를記録하고 모니터링하는 보안 활동"**입니다.
> 단순히 "누가 접속했나"를ログ하는 것을 넘어, **민감 데이터 접근 패턴의 이상 징후 탐지, 규제 준수 증거 확보(Compliance Evidence), 보안 사고 Reconstruction**에 핵심적인 역할을 합니다. PCI-DSS, SOX, GDPR, 개인정보보호법 등 다양한 규제에서 DB 감사가 의무적으로 요구됩니다.

---

## Ⅰ. DB 감사의 필수 요소: W.H.O.W.T框架

감사 로그에 반드시 기록해야 할 5가지 요소:

```
[감사 로그의 5W1H]

  ┌────────────────────────────────────────────┐
  │  WHO: "누가" 접근했는가?                    │
  │       - 사용자 계정, 호스트, IP 주소         │
  │       - Oracle: USERNAME, OS_USERNAME       │
  ├────────────────────────────────────────────┤
  │  WHAT: "무엇을" 했는가?                    │
  │       - SQL 문 (INSERT, UPDATE, DELETE)     │
  │       - 실패한 접근 시도                    │
  ├────────────────────────────────────────────┤
  │  WHEN: "언제" 발생했는가?                   │
  │       - 타임스탬프 (세션 시간, 쿼리 실행 시간)│
  ├────────────────────────────────────────────┤
  │  WHERE: "어디서" 접근했는가?                │
  │       - 스키마, 테이블, 컬럼                 │
  │       - 소스 프로그램 (SQL*Plus, Toad 등)    │
  ├────────────────────────────────────────────┤
  │  HOW: "어떻게" 했는가?                     │
  │       - 성공/실패 여부                      │
  │       - 영향 받은 행 수                     │
  │       - 수행 시간, 대기 시간                │
  └────────────────────────────────────────────┘
```

---

## Ⅱ. DB 감사 구현 방식

### 방식 1: 표준 감사 (Standard Auditing)

DBMS에 내장된 감사 기능:

```sql
-- Oracle Standard Auditing
-- 접속 감사
AUDIT CREATE SESSION;          -- 접속 시 감사
AUDIT CREATE SESSION BY ACCESS WHERE USERNAME != 'SYSTEM';

-- SQL 문 감사
AUDIT SELECT, INSERT, UPDATE, DELETE ON hr.employees;  -- DML 操作 감사
AUDIT DROP ANY TABLE;                                          -- DDL 操作 감사

-- 결과 확인
SELECT username, timestamp, action_name, obj_name, sql_text
FROM dba_audit_trail
WHERE timestamp > SYSDATE - 1;
```

### 방식 2: 세분화 감사 (Fine-Grained Auditing, FGA)

특정 조건에 부합할 때만 감사:

```sql
-- Oracle FGA: salary가 100만원 이상일 때만 감사
BEGIN
  DBMS_FGA.ADD_POLICY(
    object_schema   => 'HR',
    object_name     => 'EMPLOYEES',
    policy_name     => 'audit_high_salary',
    audit_condition => 'SALARY > 1000000',
    audit_column    => 'SALARY, BONUS',
    handler_schema  => NULL,
    handler_module  => NULL,
    enable          => TRUE,
    statement_types => 'SELECT, INSERT, UPDATE, DELETE'
  );
END;
/

-- PostgreSQL: pg_audit extension
-- postgresql.conf에 설정
-- shared_preload_libraries = 'pg_audit'
-- pg_audit.log = 'read, write, function, role, ddl'
```

### 방식 3: 캡슐 기반 감사 (Capture/Replay)

```
[캡슐 기반 감사 구조]

  ┌──────────────────────────────────────────────┐
  │           Database Activity Monitor            │
  │  ┌────────────────────────────────────────┐ │
  │  │     Traffic Captured                     │ │
  │  │                                          │ │
  │  │  Session 1 ──► SQL: INSERT INTO ...     │ │
  │  │  Session 2 ──► SQL: UPDATE ... SET     │ │
  │  │  Session 3 ──► SQL: SELECT ... WHERE   │ │
  │  │                                          │ │
  │  └────────────────────────────────────────┘ │
  │                    │                          │
  │                    ▼                          │
  │  ┌────────────────────────────────────────┐ │
  │  │  Audit Log (보안 저장소)                 │ │
  │  │  - 위조 방지를 위한 WORM(Write Once) 저장│ │
  │  │  - 중앙 집중 로그 서버 (Syslog, SIEM)   │ │
  │  └────────────────────────────────────────┘ │
  └──────────────────────────────────────────────┘
```

**대표 상용 솔루션:**
- **Oracle Audit Vault & Database Firewall**: Oracle 原산
- **IBM Guardium**: 크로스 플랫폼DB 감사
- ** Imperva**: DB 방화벽 + 감사
- ** McAfee DB Protection**: DB 보안 플랫폼

---

## III. 감사 로그 분석: 이상 접근 패턴 탐지

감사의 진정한 가치는 **"기록하는 것이 아니라 分析하는 것"**입니다:

```
[평범한 접근 패턴 vs 이상 접근 패턴]

  평범한 접근 (정상):
  - 작업 시간: 평일 9:00~18:00
  - 접속 시스템: 사내 PC (IP: 10.0.x.x)
  - 접근 테이블: 담당 부서 데이터
  - 데이터 양: 수십~수백 건/일

  이상 접근 (의심 스러운 활동):
  ┌──────────────────────────────────────────────┐
  │  1. 비정상 시간 접속                          │
  │     - 새벽 3시에 DBA 계정 접속                  │
  │     - 주말/공휴일 대량 데이터 추출              │
  │                                              │
  │  2. 비정상 대량 데이터 추출                     │
  │     - 평소 조회 건수: 100건/일                 │
  │     -，今日: 50,000건 SELECT                  │
  │     → "데이터 유출可疑"                         │
  │                                              │
  │  3. 권한 없는 데이터 접근                       │
  │     - 급여 테이블: HR팀만 접근 가능             │
  │     - 갑자기 생산팀 계정이 접근 시도             │
  │                                              │
  │  4. 실패한 접근 시도 반복                       │
  │     - 30초 내에 5회 로그인 실패                 │
  │     → "무차별 대입 공격(Brute Force) 의심"     │
  └──────────────────────────────────────────────┘
```

---

## Ⅳ. 규제 요구사항과 감사 정책 설계

**주요 규제별 요구사항:**

| 규제 | 적용 산업 | 주요 요구사항 |
|------|---------|------------|
| **PCI-DSS** | 금융 (카드 데이터) | 카드번호 접근logging, 1년간 보관 |
| **SOX** | 미국上場企業 | 재무 데이터 변경 이력, 변경자 추적 |
| **GDPR** | EU 시민 데이터 | 접근 기록, 위법 처분 증거 |
| **개인정보보호법** | 한국 | 개인정보 처리 기록, 3년간 보관 |
| **HIPAA** | 미국 의료 | 건강 정보 접근 감사 |

**감사 정책 설계 원칙:**

```sql
-- 최소한 감사해야 할 항목 (보안 기준)
AUDIT
  -- 계정 관리
  CREATE USER, DROP USER, ALTER USER,
  -- 권한 관리
  GRANT, REVOKE,
  -- DDL (구조 변경)
  CREATE ANY TABLE, DROP ANY TABLE, ALTER ANY TABLE,
  -- 민감 데이터 DML
  SELECT ON customers,  -- 고객 정보 조회
  UPDATE ON employees WHERE salary,  -- 급여 변경
  DELETE ON orders;    -- 주문 삭제
```

**오버헤드 관리:**
- 감사Level이 높을수록 성능 저하 (일반적으로 5~15% 오버헤드)
- 핵심 테이블에만 집중 감사 + 나머지는 基本 감사로 균형
- 감사 로그는 별도 저장소(로컬 디스크가 아닌 원격 서버)에 저장 → DB 성능 영향最小

---

## Ⅴ. 감사 로그 보호와 📢 비유

**감사 로그 자체도 보호해야 한다:**

```
[감사 로그 보호 전략]

  1. 로그 무결성 보장
     - 해시 체인 (이전 로그의 해시를 현재 로그에 포함)
     - 전자서명 (위조防止)
     - WORM 스토리지 (삭제/변경 불가)

  2. 로그 접근 통제
     - 감사 로그 자체도 감사 대상 (Meta Auditing)
     - DBA도 자신의 접속 기록은 삭제 불가

  3. 중앙 집중化管理
     - 각 DB 서버의 감사 로그를 중앙 SIEM으로汇聚
     - Syslog 프로토콜로 전송 (TCP/UDP 514포트)
     -Splunk, QRadar, Elastic Stack 등으로 분석
```

**감사의 함정: 로그를 많이 쌓으면 분석이 어려워진다:**
- 하루 수십 GB 감사 로그 → "아무도 안 본다"
- **AI/ML 기반 이상 탐지**: 평소 패턴과 다른 접근을 자동 탐지
- **실시간 Alert**: 위험 행동 Immediately通知

> 📢 **섹션 요약 비유:** DB 평가는 **"은행의 모든 거래 기록장"**과 같습니다. bank's 금고실(데이터베이스) 안에 어떤職員(사용자)이 어떤 시간에 어떤 행동(쿼리/DML)을 했는지 **"시계가 있는闭路电视"**가 되는 것입니다. 다만 중요한 점은, 이 기록장도 **"직원이 자기 행동 기록을 지우거나改动하면 안 되므로"** 위조 방지 장치가 있고, 이記録장 자체도 **"은행長ではない사람이 접근할 수 없게"** 별도 금고에 보관됩니다. 그리고 평价 거래냐, 이상 거래냐를 判断하는 것은 **"비서관(AI/ML)이 매일 기록을 검토해서問題가 있으면保安팀에報告하는"** 구조입니다. **"기록하고, 지키고, 분석하는"** 세 가지가 통합되어야 진정한 평가가 됩니다.
