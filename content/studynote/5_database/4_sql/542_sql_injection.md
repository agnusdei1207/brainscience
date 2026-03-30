+++
weight = 42
title = "SQL 인젝션 (SQL Injection)"
description = "SQL 인젝션 공격과 방지 방법"
date = 2026-03-26

[taxonomies]
tags = ["database", "sql", "security", "injection"]
+++

# SQL 인젝션 (SQL Injection)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL 인젝션은 응용 程序의 입력 검증 부재로 인해 악의적인 SQL 코드가 실행되는 보안 공격 기법이다.
> 2. **가치**: SQL 인젝션을 이해하고 방지하면 데이터베이스 보안과 정보 보호에 필수적인 방어선을 구축할 수 있다.
> 3. **융합**: Prepared Statement, Stored Procedure, 입력 검증 등의 방어 기법이 활용된다.

---

## Ⅰ. 공격 원리

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SQL 인젝션 공격 원리                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [취약한 코드: 문자열 결합]                                          │
│                                                                     │
│   query = "SELECT * FROM users " +                                  │
│            "WHERE id = '" + userId + "' AND pwd = '" + pwd + "'"   │
│                                                                     │
│   [정상 입력]                                                        │
│   userId = "user1", pwd = "pass123"                               │
│   → SELECT * FROM users WHERE id = 'user1' AND pwd = 'pass123'   │
│                                                                     │
│   [악의적 입력]                                                      │
│   userId = "' OR '1'='1", pwd = "' OR '1'='1"                   │
│   → SELECT * FROM users WHERE id = '' OR '1'='1' AND pwd = '' OR '1'='1'
│   → '1'='1'은 항상 TRUE → 전체 테이블 조회!                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 방어 기법

### 1. Prepared Statement

```sql
-- Java 예시
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE id = ? AND pwd = ?"
);
stmt.setString(1, userId);
stmt.setString(2, pwd);
```

### 2. Stored Procedure

```sql
CREATE PROCEDURE login_check(
    IN p_user_id VARCHAR(50),
    IN p_pwd VARCHAR(50)
)
BEGIN
    SELECT * FROM users
    WHERE id = p_user_id AND pwd = p_pwd;
END;
```

### 3. 입력 검증

```sql
-- 입력값 검증
IF NOT input MATCHES '^[a-zA-Z0-9_]+$' THEN
    -- 오류 처리
END IF;
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. SQL 인젝션은 **食堂에서 장래서 음식에 다른 것을 섞는** 것과 같아요. "김치찌개 주세요"에 "김치찌개 + 약간 다른 음식"을 섞으면 이상한 음식이 되는 거예요.
2. Prepared Statement는 **配方 대로 요리**하는 것과 같아요. 材料를 직접 넣는 게 아니라, 순서대로 넣으니까 다른 재료가 섞일 수 없어요.
3. 컴퓨터에서도 이렇게 방어 처리를 하면 해킹으로 부터 보호받을 수 있어요!
