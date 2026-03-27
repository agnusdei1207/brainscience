+++
title = "집계 함수 (Aggregate Functions)"
description = "주요 SQL 집계 함수"
date = 2026-03-26
weight = 40

[taxonomies]
tags = ["database", "sql", "aggregate", "count", "sum", "avg"]
+++

# 집계 함수 (Aggregate Functions)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 집계 함수는 여러 행의 값을 하나로 합산/평균/카운트하는 함수로, 데이터 분석과 리포팅에 필수적이다.
> 2. **가치**: GROUP BY와 함께 사용하여 카테고리별 통계, 전체 합계, 평균 등을 효과적으로 산출한다.
> 3. **융합**: 윈도우 함수 (Window Function)로 발전하여, 그룹 내 비율, 누적 합계 등高度な分析功能을 지원한다.

---

## Ⅰ. 주요 집계 함수

### 1. COUNT - 개수 세기

```sql
-- 전체 행 수
SELECT COUNT(*) FROM orders;

-- NULL이 아닌 값의 개수
SELECT COUNT(shipping_date) FROM orders;

-- 중복 제외 개수
SELECT COUNT(DISTINCT customer_id) FROM orders;
```

### 2. SUM - 합계

```sql
-- 전체 합계
SELECT SUM(amount) FROM orders;

-- NULL 무시
SELECT SUM(amount) FROM orders WHERE amount IS NOT NULL;
```

### 3. AVG - 평균

```sql
-- 평균 값
SELECT AVG(price) FROM products;

-- 소수점 처리
SELECT ROUND(AVG(price), 2) FROM products;
```

### 4. MAX/MIN - 최대/최소

```sql
-- 최대/최소 값
SELECT MAX(price), MIN(price) FROM products;

-- 날짜의 최대/최소
SELECT MAX(order_date), MIN(order_date) FROM orders;
```

---

## Ⅱ. GROUP BY와 집계 함수

```sql
-- 카테고리별 합계
SELECT category, SUM(amount) AS total_amount
FROM orders
GROUP BY category
HAVING SUM(amount) > 1000000;
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 집계 함수는 **반 전체의 체력 측정 결과**와 같아요. 전체 평균, 최고身高,最低体重 등을 한 번에 구할 수 있어요.
2. "반별로" (GROUP BY) 평균을 내면 각 반의 평균 체력이 각각 나와요.
3. 이렇게 하면 여러 데이터를 하나씩 세지 않고 한 번에 결과를 얻을 수 있어요!
