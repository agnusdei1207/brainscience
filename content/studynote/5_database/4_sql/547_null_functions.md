+++
title = "NULL 처리 함수"
description = "NVL, COALESCE, IFNULL 등 NULL 처리 함수"
date = 2026-03-26
weight = 47

[taxonomies]
tags = ["database", "sql", "null", "coalesce", "nvl"]
+++

# NULL 처리 함수

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NULL 처리 함수는 NULL 값을 다른 값으로 변환하거나, NULL 여부를判定하는 함수들이다.
> 2. **가치**: NULL은 "알려지지 않은 값"으로, 이를 적절히 처리해야 정확한 결과와 기본 키 무결성을 보장할 수 있다.
> 3. **융합**: COALESCE는 여러 열 중 첫 번째非NULL 값을 반환하여 데이터 통합에 활용된다.

---

## Ⅰ. 주요 NULL 처리 함수

### 1. NVL / IFNULL

```sql
-- Oracle NVL
SELECT NVL(phone, '없음') FROM customers;

-- MySQL IFNULL
SELECT IFNULL(phone, '없음') FROM customers;
```

### 2. COALESCE

```sql
-- 여러 값 중 첫 번째非NULL 값
SELECT COALESCE(phone, email, '연락처 없음') FROM customers;
```

### 3. NULLIF

```sql
-- 두 값이 같으면 NULL, 다르면 첫 번째 값
SELECT NULLIF(price, 0) FROM products;  -- price가 0이면 NULL 반환
```

---

## Ⅱ. NULL 관련 조건

```sql
-- NULL 값 찾기
SELECT * FROM customers WHERE phone IS NULL;

-- 非NULL 값 찾기
SELECT * FROM customers WHERE phone IS NOT NULL;
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. NULL은 **"아직 정하지 않은 값"**과 같아요. future birthday를 기다리고 있는 것과 같아요.
2. NVL은 **"값이 없으면 '없음'이라고 표시해"**라는 것과 같아요. 선물을 안 받으면 "선물 없음"이라고 쓰는 거예요.
3. COALESCE는 **"전화번호가 없으면 이메일, 그것도 없으면 주소"**로 차례로 찾아보는 것과 같아요!
