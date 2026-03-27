+++
title = "집합 연산 (SET Operations)"
description = "UNION, INTERSECT, EXCEPT/MINUS"
date = 2026-03-26
weight = 49

[taxonomies]
tags = ["database", "sql", "union", "intersect", "except"]
+++

# 집합 연산 (SET Operations)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 집합 연산은 두 개의 SELECT 결과 집합을 결합하는 연산으로, UNION (합집합), INTERSECT (교집합), EXCEPT/MINUS (차집합)가 있다.
> 2. **가치**: 여러 테이블의 결과를 하나로 합치거나, 공통된 데이터를 찾거나, 차집합을 구하는 데 활용된다.
> 3. **융합**: 분산 쿼리에서 각 서버의 결과셋을統合하는 데 활용되며, NULL 처리와 중복 제거 옵션이 중요하다.

---

## Ⅰ. UNION

두 결과의 합집합 (중복 제거)

```sql
-- 전체 고객 (국내 + 해외)
SELECT name, email FROM domestic_customers
UNION
SELECT name, email FROM international_customers;
```

### UNION ALL

중복 허용 (더 빠른 경우あり)

```sql
SELECT name FROM customers
UNION ALL
SELECT name FROM employees;  -- 중복 포함
```

---

## Ⅱ. INTERSECT

두 결과의 교집합

```sql
-- 국내 및 해외 모두 있는 고객
SELECT email FROM domestic_customers
INTERSECT
SELECT email FROM international_customers;
```

---

## Ⅲ. EXCEPT / MINUS

첫 번째 결과에서 두 번째 결과 제거

```sql
-- 국내에만 있는 고객
SELECT email FROM domestic_customers
EXCEPT
SELECT email FROM international_customers;
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. UNION은 **두 반의 학생 명단을 합치는 것**과 같아요. A반과 B반을 합치면 모든 학생이 있지만, 같은 학생이 두 번 나타나지 않아요.
2. INTERSECT는 **두 반 모두에 속한 학생**을 찾는 것이고,
3. EXCEPT는 **A반에는 있지만 B반에는 없는 학생**을 찾는 것이에요!
