+++
weight = 39
title = "문자열 함수 (String Functions)"
description = "주요 SQL 문자열 함수"
date = 2026-03-26

[taxonomies]
tags = ["database", "sql", "string", "function"]
+++

# 문자열 함수 (String Functions)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 문자열 함수는 SQL에서 문자열 데이터를 조작하고 변환하는 함수로, 데이터 정제, 포맷 변환, 검색 등에 필수적이다.
> 2. **가치**: 문자열 함수를 활용하면 응용 程序에서 처리해야 할 작업을 DBMS 차원에서 효율적으로 처리할 수 있다.
> 3. **융합**: 오라클, MySQL, PostgreSQL 등 각 DBMS가 расширен된 문자열 함수를 提供하며, 정규식 지원 등 고급 기능이追加되고 있다.

---

## Ⅰ. 주요 문자열 함수

### 1. 연결 함수

```sql
-- CONCAT: 문자열 연결
SELECT CONCAT(first_name, ' ', last_name) FROM employees;

-- CONCAT_WS: 구분자와 함께 연결
SELECT CONCAT_WS(', ', city, district) FROM addresses;
```

### 2. 길이 함수

```sql
-- LENGTH: 문자 수
SELECT LENGTH(name) FROM customers;

-- CHAR_LENGTH: 문자 수 (오라클 제외)
SELECT CHAR_LENGTH(name) FROM customers;
```

### 3. 추출 함수

```sql
-- SUBSTRING: 부분 문자열 추출
SELECT SUBSTRING(phone, 1, 3) FROM customers;

-- LEFT/RIGHT: 좌/우측부터 추출
SELECT LEFT(name, 1) FROM customers;
SELECT RIGHT(phone, 4) FROM customers;
```

### 4. 변환 함수

```sql
-- UPPER/LOWER: 대/소문자 변환
SELECT UPPER(name) FROM customers;
SELECT LOWER(email) FROM customers;

-- TRIM: 공백 제거
SELECT TRIM(name) FROM customers;
```

### 5. 검색 함수

```sql
-- LIKE: 패턴 매칭
SELECT * FROM customers WHERE name LIKE '김%';

-- POSITION/INSTR: 위치 찾기
SELECT POSITION('@' IN email) FROM customers;
```

### 6. 치환 함수

```sql
-- REPLACE: 문자열 치환
SELECT REPLACE(phone, '-', '') FROM customers;

-- TRANSLATE: 문자별 치환 (오라클)
SELECT TRANSLATE(phone, '- )', '') FROM customers;
```

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **CONCAT** | 여러 문자열을 하나로 연결하는 함수다. |
| **SUBSTRING** | 문자열의 일부를 추출하는 함수다. |
| **LIKE** | 패턴 기반 문자열 검색 연산자다. |
| **REPLACE** | 문자열 내 특정 문자열을 치환하는 함수다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. 문자열 함수는 **글자玩游戏**과 같아요. 글자를 합치고 (연결), 자르고 (추출), 다른 글자로 바꾸고 (치환) 할 수 있어요.
2. 예를 들어 "서울"과 "특별시"를 합치면 (연결) "서울특별시가" 돼요.
3. 컴퓨터로 글자를 다룰 때 문자열 함수를 쓰면 복잡한 것도 쉽게 처리할 수 있어요!
