+++
title = "054. 카탈로그 매니저 (Catalog Manager)"
date = "2026-03-05"
weight = 54
[extra]
categories = "studynotes-database"
tags = ["database", "catalog", "metadata", "system-catalog", "data-dictionary"]
+++

# 054. 카탈로그 매니저 (Catalog Manager)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 카탈로그 매니저는 시스템 카탈로그(메타데이터)에 접근하여 테이블 구조, 인덱스 정보, 통계 등을 옵티마이저와 실행 엔진에 제공하는 모듈이다.
> 2. **가치**: CBO 옵티마이저가 비용 계산을 위해 테이블/인덱스 통계를 조회하고, 실행 엔진이 컬럼 타입 정보를 획득하는 데 필수적이다.
> 3. **융합**: 카탈로그는 시스템 테이블에 저장되며, DDL 실행 시 자동 갱신되고 캐싱을 통해 접근 성능을 최적화한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
**카탈로그 매니저(Catalog Manager)**는 데이터 사전(Data Dictionary) 또는 시스템 카탈로그(System Catalog)에 저장된 메타데이터를 관리하고 접근하는 DBMS 구성 요소다.

### 💡 비유
카탈로그 매니저를 **도서관 도서 목록 시스템**에 비유할 수 있다:
- **책(DB 테이블)**: 실제 데이터
- **도서 목록(카탈로그)**: 책의 제목, 저자, 위치 정보
- **사서(카탈로그 매니저)**: 목록에서 정보 찾아줌

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 시스템 카탈로그 구조
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SYSTEM CATALOG STRUCTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    METADATA CATEGORIES                                │  │
│   ├─────────────────────────────────────────────────────────────────────┤  │
│   │                                                                      │  │
│   │   TABLE METADATA                                                     │  │
│   │   • Table names, Schema                                              │  │
│   │   • Column names, Types, Constraints                                 │  │
│   │   • Primary/Foreign Keys                                             │  │
│   │                                                                      │  │
│   │   INDEX METADATA                                                     │  │
│   │   • Index names, Types (B+Tree, Hash)                               │  │
│   │   • Indexed columns, Order                                          │  │
│   │   • Statistics (height, leaf pages)                                 │  │
│   │                                                                      │  │
│   │   STATISTICS                                                         │  │
│   │   • Row count (cardinality)                                          │  │
│   │   • Distinct values (NDV)                                            │  │
│   │   • Data distribution histograms                                     │  │
│   │   • Clustering factor                                                │  │
│   │                                                                      │  │
│   │   VIEW METADATA                                                      │  │
│   │   • View definitions                                                 │  │
│   │   • Dependencies                                                     │  │
│   │                                                                      │  │
│   │   PRIVILEGE METADATA                                                 │  │
│   │   • User permissions                                                 │  │
│   │   • Role assignments                                                 │  │
│   │                                                                      │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    DBMS CATALOG TABLES (MySQL 예시)                   │  │
│   ├─────────────────────────────────────────────────────────────────────┤  │
│   │                                                                      │  │
│   │   INFORMATION_SCHEMA:                                                │  │
│   │   • TABLES, COLUMNS                                                  │  │
│   │   • STATISTICS, INDEXES                                              │  │
│   │   • KEY_COLUMN_USAGE                                                 │  │
│   │                                                                      │  │
│   │   mysql database:                                                    │  │
│   │   • user, db, tables_priv                                            │  │
│   │   • innodb_table_stats, innodb_index_stats                          │  │
│   │                                                                      │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 주요 카탈로그 뷰
| 뷰 (MySQL) | 설명 |
|:---|:---|
| `INFORMATION_SCHEMA.TABLES` | 테이블 정보 |
| `INFORMATION_SCHEMA.COLUMNS` | 컬럼 정보 |
| `INFORMATION_SCHEMA.STATISTICS` | 인덱스 통계 |
| `INFORMATION_SCHEMA.KEY_COLUMN_USAGE` | 키 제약조건 |

---

## Ⅲ. 융합 비교 및 다각도 분석

### 1. DBMS별 카탈로그 위치
| DBMS | 위치 | 특징 |
|:---|:---|:---|
| **MySQL** | INFORMATION_SCHEMA | SQL 표준 준수 뷰 |
| **Oracle** | Data Dictionary (SYS 스키마) | DBA_, ALL_, USER_ 접두사 |
| **PostgreSQL** | pg_catalog 스키마 | 시스템 카탈로그 테이블 |
| **SQL Server** | sys 스키마 | 카탈로그 뷰 |

### 2. 통계 정보 갱신
```sql
-- MySQL
ANALYZE TABLE employees;

-- PostgreSQL
ANALYZE employees;

-- Oracle
DBMS_STATS.GATHER_TABLE_STATS('HR', 'EMPLOYEES');

-- SQL Server
UPDATE STATISTICS employees;
```

---

## Ⅳ. 실무 적용

### 카탈로그 조회 예시
```sql
-- 테이블 정보 조회
SELECT table_name, table_rows, data_length
FROM information_schema.tables
WHERE table_schema = 'mydb';

-- 인덱스 정보 조회
SELECT index_name, column_name, cardinality
FROM information_schema.statistics
WHERE table_name = 'employees';

-- 컬럼 정보 조회
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'employees';
```

---

## 📌 관련 개념 맵
- [[011_시스템_카탈로그]](./11_system_catalog.md): 메타데이터 저장소
- [[012_메타데이터]](./12_metadata.md): 데이터에 대한 데이터
- [[052_옵티마이저]](./52_optimizer.md): 통계 정보 활용

---

## 👶 어린이를 위한 3줄 비유
1. **도서관 목록**: 도서관에 어떤 책이 있는지 목록으로 정리해둔 것과 같아요. 책을 찾을 때 목록을 보면 어디 있는지 알 수 있죠.

2. **학교 명부**: 학교에 어떤 학생이 있는지 명부에 적어둔 것처럼, 데이터베이스에 어떤 테이블이 있는지 카탈로그에 적어둬요.

3. **색인 카드**: 백과사전 맨 앞에 어떤 내용이 몇 페이지에 있는지 적어둔 것과 같아요. 필요한 정보를 빨리 찾을 수 있죠!
