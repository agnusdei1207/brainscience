+++
title = "21. DML (Data Manipulation Language) - 데이터 조작 언어"
weight = 21
[taxonomies]
categories = ["studynotes-데이터베이스"]
+++

# 21. DML (Data Manipulation Language) - 데이터 조작 언어

## Ⅰ. DML의 개요

### 1. DML(Data Manipulation Language)의 정의
* 데이터베이스에 저장된 실제 데이터를 다루기 위한 언어로, 사용자가 데이터를 검색(조회), 삽입, 수정, 삭제할 수 있도록 지원하는 명령 체계입니다.
* DDL이 데이터베이스의 '뼈대'를 만든다면, DML은 그 뼈대 안에 '살'을 채우고 움직이게 하는 역할을 합니다. 데이터베이스와 응용 프로그램(또는 사용자) 간의 실질적인 데이터 트랜잭션이 DML을 통해 발생합니다.

### 2. 주요 명령어 및 특성
* **주요 명령어:** `SELECT`(검색/조회), `INSERT`(삽입), `UPDATE`(수정), `DELETE`(삭제)
* **트랜잭션(Transaction) 관리 종속성:** DDL과 달리 대부분의 DML 연산(특히 `INSERT`, `UPDATE`, `DELETE`)은 Auto-Commit되지 않으며, `COMMIT` 또는 `ROLLBACK` 명령(TCL)을 통해 명시적으로 트랜잭션을 제어해야 합니다. (DBMS 설정에 따라 다를 수 있으나 이론적 기본은 논리적 작업 단위를 가짐)

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. DML의 처리 메커니즘
DML 질의문(특히 복잡한 `SELECT` 문)이 RDBMS에 전달되면, 시스템은 최소의 비용(Disk I/O, CPU 시간)으로 데이터를 처리하기 위해 일련의 복잡한 최적화 과정을 거칩니다.

### 2. 질의 실행 및 버퍼 캐시 아키텍처 (ASCII 다이어그램)

```text
[DML Execution Engine and Buffer Cache Flow]

       [Client Application] (Issues DML: UPDATE, SELECT ...)
                |
                v
+-------------------------------------------------------------+
|                     DBMS Server Process                     |
|                                                             |
|  1. Parser (문법 및 권한 체크)                              |
|  2. Optimizer (Cost-Based 최적의 실행 계획 도출)            |
|  3. Row Source Generator (실행 가능한 코드 생성)            |
+-------------------------+-----------------------------------+
                          |
                          v
+-------------------------------------------------------------+
|                  Database Memory Area (SGA/Shared Pool)     |
|                                                             |
|  [ Data Buffer Cache ]      [ Redo Log Buffer ] (For I,U,D) |
|  - 메모리에 데이터 블록 적재  - 변경 내역(Log) 순차 기록    |
|  - 실제 읽기/쓰기 발생      - 복구(Recovery) 기반 제공      |
+-------------+---------------------------+-------------------+
              |                           |
        (Cache Miss 시)             (Commit 발생 시)
              |                           |
              v                           v
+-------------------------+   +-------------------------------+
|    Physical Data Files  |   |     Physical Log Files        |
|  (Disk Storage)         |   |  (Disk Storage)               |
+-------------------------+   +-------------------------------+
```
* **원리 설명:** DML 작업은 디스크의 데이터 파일에 직접 쓰기/읽기를 수행하지 않습니다. 메모리의 '데이터 버퍼 캐시'에 블록을 올린 후 연산을 수행(Logical I/O)하며, 변경된 내역(`UPDATE`, `INSERT`, `DELETE`)은 트랜잭션 안전성을 위해 '리두 로그 버퍼'를 거쳐 디스크 로그 파일에 순차적으로 기록(Write-Ahead Logging)됩니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 1. 질의(Query) 문장 `SELECT`의 특수성 분석
`SELECT` 문은 데이터를 변경하지 않으므로 트랜잭션의 상태를 변경(Commit/Rollback 대상)하지 않는다는 점에서 `INSERT/UPDATE/DELETE`와 구별됩니다.
그러나 `SELECT`는 데이터베이스 부하의 90% 이상을 차지하는 핵심 요소입니다. `SELECT` 처리 시 일관된 읽기(Consistent Read)를 보장하기 위해, DBMS는 다른 트랜잭션이 수정 중인 데이터에 접근할 때 언두(Undo) 세그먼트를 활용하여 쿼리 시작 시점의 데이터 스냅샷을 재구성하여 제공하는 다중 버전 동시성 제어(MVCC, Multi-Version Concurrency Control) 기술을 사용합니다.

### 2. 대량 데이터 조작 시의 `DELETE` vs `TRUNCATE` (DML vs DDL)
DML인 `DELETE`는 로우(Row) 단위로 잠금(Lock)을 걸고 데이터를 지우며, 모든 삭제 내역을 언두/리두 로그에 기록합니다. 이는 트랜잭션 복구를 가능하게 하지만 수백만 건의 데이터 처리 시 시스템 병목과 언두 공간의 고갈(Snapshot Too Old 등)을 유발합니다. 반면 DDL인 `TRUNCATE`는 스토리지 단에서 데이터 블록 할당을 해제하므로 압도적으로 빠르지만, 트랜잭션 보호를 받을 수 없습니다. 실무에서는 목적에 따라 이 두 가지를 명확히 구분하여 사용해야 합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 1. 실무 적용: DML 성능 튜닝과 인덱스의 역설
* **읽기(`SELECT`) 성능 극대화:** 조인(Join) 방식(Nested Loop, Hash, Sort Merge)의 이해와 인덱스 스캔을 유도하여 디스크 I/O를 최소화하는 것이 핵심입니다.
* **인덱스의 역설:** `SELECT` 성능을 높이기 위해 무분별하게 생성된 인덱스는, 반대로 `INSERT`, `UPDATE`, `DELETE` DML 작업 시 치명적인 성능 저하를 일으킵니다. 데이터를 조작할 때마다 연관된 모든 인덱스 트리(B-Tree) 구조를 함께 갱신하고 재정렬해야 하는 오버헤드(Index Maintenance Overhead)가 발생하기 때문입니다.

### 2. 기술사적 통찰 (데이터 아키텍처 관점)
DML의 동시 다발적 발생은 시스템의 락(Lock) 경합 및 데드락(Deadlock)의 주요 원인이 됩니다. 기술사는 트랜잭션 격리 수준(Isolation Level)을 비즈니스 요구사항에 맞게 조율(예: Read Committed vs Serializable)하여 동시성과 데이터 정합성 간의 최적의 균형(Trade-off)을 찾아내야 합니다.
또한, 쓰기(`INSERT/UPDATE/DELETE`) 트랜잭션이 대량으로 발생하는 시스템의 경우, 읽기 부하를 분리하기 위해 CQRS (Command and Query Responsibility Segregation) 패턴이나 리드 레플리카(Read Replica) 아키텍처를 도입하여 DML과 `SELECT` 간의 상호 간섭을 물리적으로 차단하는 엔터프라이즈 레벨의 설계 역량이 요구됩니다.

---

## Ⅴ. 기대효과 및 결론

### 1. 최적화된 DML 활용의 기대효과
* **트랜잭션 안전성 보장:** DML 명령어와 TCL(Commit, Rollback)의 정확한 조합을 통해 ACID 특성을 준수하여 데이터의 논리적 무결성을 철저히 보호할 수 있습니다.
* **시스템 응답성 향상:** 실행 계획(Execution Plan) 분석에 기반한 DML 튜닝은 디스크 I/O를 최소화하고 CPU 효율을 높여 애플리케이션의 전반적인 응답 시간을 획기적으로 개선합니다.

### 2. 결론
DML은 데이터베이스의 심장을 뛰게 하는 동력원입니다. 단순한 데이터의 조회를 넘어, 대용량 트랜잭션 환경에서 동시성과 무결성을 잃지 않으면서 데이터를 조작하는 것은 매우 고도의 기술적 난이도를 가집니다.
DBMS의 비절차적 특성을 이해하고 내부 옵티마이저가 최적의 경로로 DML을 수행하도록 이끄는 능력(SQL 튜닝 및 아키텍처 설계)은 데이터베이스 전문가를 넘어 전체 IT 시스템 아키텍트가 갖추어야 할 가장 기본적이면서도 궁극적인 핵심 역량입니다. 향후 AI 기반 자율 튜닝 데이터베이스 시대가 도래하더라도, DML의 동작 원리와 I/O 메커니즘에 대한 깊은 이해는 시스템 아키텍처 결정의 변함없는 기준이 될 것입니다.