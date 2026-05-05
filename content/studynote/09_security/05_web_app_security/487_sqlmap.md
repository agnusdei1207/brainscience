+++
weight = 487
title = "487. SQLMap (SQL 인젝션 자동화 도구)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: SQLMap은 SQL (Structured Query Language) 인젝션 취약점을 자동으로 탐지하고 익스플로잇하는 오픈소스 도구로, Error-based·Boolean-based·Time-based·Union-based 등 다양한 기법을 지원한다.
> 2. **가치**: 수동으로 수 시간이 걸리는 SQL 인젝션 분석을 자동화하여 DB (Database) 스키마·데이터 덤프, OS 명령 실행까지 가능하다.
> 3. **판단 포인트**: SQLMap은 취약점 탐지 후 자동으로 악용(exploitation)까지 진행하므로, 반드시 서면 허가를 받은 대상에만 사용해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

SQLMap은 2006년 처음 공개된 이후 SQL 인젝션 자동화 도구의 사실상 표준이 되었다. Python으로 작성되어 모든 OS에서 동작하며, MySQL·PostgreSQL·Oracle·MSSQL·SQLite 등 주요 DBMS (Database Management System)를 지원한다.

자동 탐지 기법: Error-based, Union-based, Boolean-based Blind, Time-based Blind, Stacked Queries, Out-of-Band.

📢 **섹션 요약 비유**: 금고(DB) 열기 도구—취약한 자물쇠(SQL 인젝션)를 자동으로 찾아내고 여는 스위스 아미 나이프이다.

---

## 2. 구성요소

| 기법 | 동작 원리 | 속도 |
|:---|:---|:---|
| Error-based | DB 오류 메시지 분석 | 빠름 |
| Union-based | UNION SELECT로 데이터 추출 | 빠름 |
| Boolean Blind | 참/거짓 응답 차이 분석 | 중간 |
| Time-based Blind | 응답 지연 시간 측정 | 느림 |
| Out-of-Band | DNS/HTTP 외부 채널 | 느림 |

```
[SQLMap 동작 흐름]

sqlmap -u "http://target.com/page?id=1"
  │
  ▼
파라미터 자동 식별
  id=1 → 취약 파라미터 탐지
  │
  ▼
인젝션 기법 순서 시도
  Error-based → Union → Boolean → Time
  │
  ▼
DB 정보 추출
  DB 버전, DB 명, 테이블, 컬럼, 데이터
  │
  ▼
(옵션) OS Shell / File Read/Write
```

📢 **섹션 요약 비유**: 자물쇠 따개(SQLMap)가 여러 종류의 도구(기법)를 순서대로 사용해 문을 열어본다.

---

## 3. 구조 및 동작 원리

| 옵션 | 기능 |
|:---|:---|
| `--dbs` | DB 목록 열거 |
| `--tables -D dbname` | 테이블 목록 |
| `--dump -T table` | 테이블 데이터 덤프 |
| `--os-shell` | OS 명령어 실행 |
| `--level=5 --risk=3` | 공격 강도 최대 |
| `--batch` | 비대화식 자동 실행 |

📢 **섹션 요약 비유**: 옵션들은 도구 가방 안의 각기 다른 도구—필요한 것만 꺼내 쓰면 된다.

---

## 4. 비교 및 트레이드오프

**방어 관점 활용**: WAF (Web Application Firewall) 규칙 효과 검증, 입력 검증 우회 가능 여부 확인, 파라미터화 쿼리(Parameterized Query) 적용 여부 테스트에 활용한다.

**탐지 우회 옵션**:
```
sqlmap --tamper=space2comment,between  # WAF 우회 tamper 스크립트
sqlmap --delay=2 --timeout=30          # 타이밍 조절
```

**법적 주의**: 권한 없는 대상에 SQLMap 사용은 불법이다. 버그바운티·CTF·화이트박스 테스트에만 사용한다.

📢 **섹션 요약 비유**: 자물쇠 따개는 내 집 잠긴 문을 열 때만 합법—남의 집에 쓰면 범죄이다.

---

## 5. 실무 적용 및 최적화 기법

방어자 관점에서 SQLMap은 자신의 시스템에 SQL 인젝션 취약점이 있는지 빠르게 검증하는 데 매우 유용하다. 파라미터화 쿼리와 ORM (Object-Relational Mapping)을 적용했을 때 SQLMap이 데이터를 추출하지 못하면 방어가 성공적으로 이루어진 것이다.

📢 **섹션 요약 비유**: 방어 효과를 검증하려면 직접 자물쇠(내 시스템)를 따개(SQLMap)로 시험해봐야 한다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Parameterized Query | 방어 | SQL 인젝션 근본 차단 |
| WAF | 탐지 | SQLMap 요청 시그니처 탐지 |
| Blind SQLi | 기법 | 응답 차이로 데이터 추출 |
| tamper script | 우회 | WAF 탐지 회피 기법 |

### 👶 어린이를 위한 3줄 비유 설명
SQLMap은 웹사이트의 잠긴 금고(DB)를 자동으로 열어보는 도구예요.
금고 자물쇠(SQL 쿼리)에 문제가 있으면 자동으로 찾아내고 내용물(데이터)을 꺼낼 수 있어요.
허가받은 집(내 시스템)에서만 사용해야 하고, 남의 집에 쓰면 범죄예요.
