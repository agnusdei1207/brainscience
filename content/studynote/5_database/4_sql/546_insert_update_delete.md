+++
title = "INSERT, UPDATE, DELETE"
description = "데이터 조작 DML 문"
date = 2026-03-26
weight = 46

[taxonomies]
tags = ["database", "sql", "dml", "insert", "update", "delete"]
+++

# INSERT, UPDATE, DELETE

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: INSERT는 데이터를 삽입하고, UPDATE는 기존 데이터를 수정하며, DELETE는 데이터를 삭제하는 DML 명령이다.
> 2. **가치**: 이 세 가지 명령으로 데이터의 CRUD (Create, Read, Update, Delete) 操作을 수행한다.
> 3. **융합**: 트랜잭션과 결합하여 원자성을 보장받고, 복제 환경에서slave 서버로の伝播된다.

---

## Ⅰ. INSERT

### 데이터 삽입

```sql
-- 방법 1: 모든 열에 값 삽입
INSERT INTO customers VALUES ('C001', '김철수', 'kim@test.com', '서울');

-- 방법 2: 열 목록 지정
INSERT INTO customers (customer_id, name, email, city)
VALUES ('C002', '이영희', 'lee@test.com', '부산');

-- 방법 3: 서브쿼리
INSERT INTO backup_customers
SELECT * FROM customers WHERE created_at < '2024-01-01';
```

---

## Ⅱ. UPDATE

### 데이터 수정

```sql
-- 조건부 수정
UPDATE customers
SET city = '인천', email = 'newemail@test.com'
WHERE customer_id = 'C001';

-- 복수 열 수정
UPDATE products
SET price = price * 0.9, updated_at = NOW()
WHERE category = '할인상품';
```

---

## Ⅲ. DELETE

### 데이터 삭제

```sql
-- 조건부 삭제
DELETE FROM customers
WHERE city = '서울' AND created_at < '2020-01-01';

-- 전체 삭제 (TRUNCATE vs DELETE)
DELETE FROM customers;  -- 롤백 가능
TRUNCATE TABLE customers;  -- 롤백 불가, 더 빠름
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. INSERT는 **새로운 메모를 추가하는 것**과 같아요.纸上에 새로운情報を書き加える 거예요.
2. UPDATE는 **기존 메모를修正하는 것**과 같아요. "오늘 Meeting 3시"를 "4시"로 바꾸는 거예요.
3. DELETE는 **메모를 지우는 것**과 같아요.紙から情報を抹消する 거예요.
