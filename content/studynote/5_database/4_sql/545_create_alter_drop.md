+++
title = "CREATE, ALTER, DROP"
description = "테이블 생성, 수정, 삭제 DDL 문"
date = 2026-03-26
weight = 45

[taxonomies]
tags = ["database", "sql", "ddl", "create", "alter", "drop"]
+++

# CREATE, ALTER, DROP

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CREATE는 테이블, 인덱스, 뷰 등 数据库 객체를 생성하고, ALTER는 기존 객체를 수정하며, DROP은 객체를 삭제하는 DDL 명령이다.
> 2. **가치**: 이 세 가지 명령으로 数据库 객체의 전체生命周期를 관리할 수 있다.
> 3. **융합**: 마이그레이션 도구 (Flyway, Liquibase)로 버전 관리되고, CI/CD 파이프라인에서 자동 실행된다.

---

## Ⅰ. CREATE

### 테이블 생성

```sql
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    city VARCHAR(20) DEFAULT '서울',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 인덱스 생성

```sql
CREATE INDEX idx_city ON customers(city);
CREATE UNIQUE INDEX idx_email ON customers(email);
```

---

## Ⅱ. ALTER

### 열 추가/수정/삭제

```sql
-- 열 추가
ALTER TABLE customers ADD phone VARCHAR(20);

-- 열 수정
ALTER TABLE customers MODIFY email VARCHAR(200) NOT NULL;

-- 열 삭제
ALTER TABLE customers DROP COLUMN phone;
```

### 제약조건 추가

```sql
ALTER TABLE orders
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);
```

---

## Ⅲ. DROP

### 테이블 삭제

```sql
DROP TABLE customers;  -- 구조 + 데이터 삭제
TRUNCATE TABLE customers;  -- 데이터만 삭제
```

### 주의

- DROP은 AUTO COMMIT이므로 롤백 불가
- DROP TABLE은 복구 불가능할 수 있음

---

## 👶 어린이를 위한 3줄 비유 설명

1. CREATE는 **새로운 상자를 만드는 것**과 같아요. 크기, 재질,用途를 정해서 만들 수 있어요.
2. ALTER는 **이미 만든 상자를改造하는 것**과 같아요. 선반을 추가하거나, 크기를 늘릴 수 있어요.
3. DROP은 **상자를 폐기하는 것**과 같아요. 다시 되돌릴 수 없으니 조심해야 해요!
