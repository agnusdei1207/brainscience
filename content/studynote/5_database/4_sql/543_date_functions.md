+++
title = "날짜/시간 함수 (Date/Time Functions)"
description = "주요 SQL 날짜 및 시간 함수"
date = 2026-03-26
weight = 43

[taxonomies]
tags = ["database", "sql", "date", "time", "function"]
+++

# 날짜/시간 함수 (Date/Time Functions)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 날짜/시간 함수는 날짜와 시간 데이터를 조작, 비교, 포맷 변환하는 데 사용되는 SQL 함수다.
> 2. **가치**: 예약 시스템, 보고서 기간 설정, 기간 계산 등 날짜 관련 업무 처리에 필수적이다.
> 3. **융합**: 타임존 처리, Unix timestamp, INTERVAL 등 고급 날짜 연산이 지원되며, 시계열 데이터 분석에 활용된다.

---

## Ⅰ. 주요 날짜/시간 함수

### 1. 현재 날짜/시간

```sql
-- 현재 날짜
SELECT CURDATE(), CURRENT_DATE;

-- 현재 시간
SELECT CURTIME(), CURRENT_TIME;

-- 현재 타임스탬프
SELECT NOW(), CURRENT_TIMESTAMP;
```

### 2. 날짜 추출

```sql
-- 연도, 월, 일 추출
SELECT YEAR(order_date), MONTH(order_date), DAY(order_date)
FROM orders;

-- 요일, 주 번호
SELECT DAYOFWEEK(order_date), WEEK(order_date)
FROM orders;
```

### 3. 날짜 연산

```sql
-- 날짜 더하기/빼기
SELECT DATE_ADD(order_date, INTERVAL 7 DAY) AS delivery_date
FROM orders;

SELECT DATEDIFF(ship_date, order_date) AS days_to_ship
FROM orders;
```

### 4. 날짜 포맷

```sql
-- MySQL
SELECT DATE_FORMAT(order_date, '%Y-%m-%d') AS formatted
FROM orders;

-- Oracle
SELECT TO_CHAR(order_date, 'YYYY-MM-DD') AS formatted
FROM dual;
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 날짜 함수는 **달력 앱**과 같아요. 오늘 날짜를 알려주고, 7일 후를 계산하고, 달력을 表示할 수 있어요.
2. "내일 모레"를計算하면 (DATE_ADD) Calendar에 그려진 날짜가 되고,
3. "무슨 요일인지" 물으면 (DAYOFWEEK) 무슨 요일인지 알려주는 거예요!
