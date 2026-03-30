+++
weight = 48
title = "CASE 식 (CASE Expression)"
description = "SQL의 CASE 조건 표현식"
date = 2026-03-26

[taxonomies]
tags = ["database", "sql", "case", "conditional"]
+++

# CASE 식 (CASE Expression)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CASE 식은 SQL에서 조건부逻辑을 구현하는 표현식으로, IF-THEN-ELSE 구조를 지원한다.
> 2. **가치**: 복잡한 IF-THEN-ELSE 논리를 쿼리 내에서 직접 표현하여 응용 程序 코드를 줄이고, 데이터 변환/분류에 활용된다.
> 3. **융합**: SELECT, WHERE, ORDER BY 등 다양한 절에서 사용되며, GROUP BY의HAVING과 결합하여 조건부 집계가 가능하다.

---

## Ⅰ. CASE 식 기본

### 단순 CASE

```sql
SELECT
    product_name,
    price,
    CASE category
        WHEN 'electronics' THEN '전자제품'
        WHEN 'food' THEN '식품'
        ELSE '기타'
    END AS category_name
FROM products;
```

### 검색 CASE

```sql
SELECT
    name,
    age,
    CASE
        WHEN age < 20 THEN '청소년'
        WHEN age < 40 THEN '청년'
        WHEN age < 60 THEN '중년'
        ELSE '노년'
    END AS age_group
FROM customers;
```

---

## Ⅱ. 응용 예시

### 조건부 집계

```sql
SELECT
    COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending,
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) AS cancelled
FROM orders;
```

### ORDER BY에서 사용

```sql
SELECT * FROM products
ORDER BY
    CASE
        WHEN priority = 'high' THEN 1
        WHEN priority = 'medium' THEN 2
        ELSE 3
    END;
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. CASE는 **음식점 메뉴판의条件별価格**과 같아요. "LARGE는 +1000원, SMALL은 -500원"과 같이情形에 따라処理を分けられる 거예요.
2. "만약 ~이면 ~이고, 그렇지 않으면 ~"라는 조건을 Programming 없이 바로 쓸 수 있어요.
3. 그래서 CASE를 쓰면 복잡한条件도 쉽게表現할 수 있어요!
