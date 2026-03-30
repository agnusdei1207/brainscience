+++
weight = 41
title = "트랜잭션 관리 (Transaction Management)"
description = "트랜잭션 관리의 핵심 개념"
date = 2026-03-26

[taxonomies]
tags = ["database", "transaction", "commit", "rollback", "savepoint"]
+++

# 트랜잭션 관리 (Transaction Management)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 트랜잭션 관리는 데이터베이스의 작업 단위인 트랜잭션의 원자성, 일관성, 고립성, 영속성을 보장하는 메커니즘이다.
> 2. **가치**: 트랜잭션 관리를 통해 다수의 操作을 하나의 논리적 단위로 묶어 안전하게 처리할 수 있다.
> 3. **융합**: 분산 트랜잭션에서 2PC (Two-Phase Commit) 프로토콜과 사티ements framework가 활용된다.

---

## Ⅰ. 주요 명령어

### COMMIT

작업을 영구적으로 저장한다.

```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 1000 WHERE account_id = 'A';
UPDATE accounts SET balance = balance + 1000 WHERE account_id = 'B';
COMMIT;  -- 모든 변경 영구 저장
```

### ROLLBACK

작업을 취소하고 이전 상태로 복원한다.

```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 1000 WHERE account_id = 'A';
-- 오류 발생!
ROLLBACK;  -- 모든 변경 취소
```

### SAVEPOINT

트랜잭션 내 중간 저장점을 생성한다.

```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 1000 WHERE account_id = 'A';
SAVEPOINT sp1;
UPDATE accounts SET balance = balance - 500 WHERE account_id = 'A';
ROLLBACK TO SAVEPOINT sp1;  -- sp1 이후 변경만 취소
COMMIT;
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. COMMIT은 **놀이 완료 후父母에게 보고**와 같아요.額을 다 쓰고 나서父母에게 완성品을 보여주는 거예요.
2. ROLLBACK은 **실수 후 다시 처음부터**와 같아요. 그림을 잘못 그렸을 때 지우고 다시 그리는 거예요.
3. SAVEPOINT는 **중간 저장**과 같아요. 게임에서 중간 보스까지만 진행된 상태를保存하는 것과 같아요.
