+++
weight = 6
title = "06. 클라우드 배포 모델"
date = "2026-05-17"
[extra]
categories = "gisulsa-database"
+++

# 🎯 트랜잭션 ACID & 동시성 제어

> **별점**: ★★★★★ | 매회 기본 필출

## 1. ACID 속성

| 속성 | 의미 | 구현 |
|------|------|------|
| **원자성(A)** | 전부 or 전무 | UNDO 로그, 롤백 |
| **일관성(C)** | 제약조건 항상 유지 | 무결성 제약 |
| **격리성(I)** | 트랜잭션 간 간섭 없음 | 잠금, MVCC |
| **지속성(D)** | 완료 후 영속 보장 | WAL, REDO 로그 |

## 2. 격리 수준 (Isolation Level)

```
격리 수준           문제 현상
────────────────────────────────────────
READ UNCOMMITTED → Dirty Read 발생
READ COMMITTED   → Non-Repeatable Read 발생  
REPEATABLE READ  → Phantom Read 발생 (기본값 InnoDB)
SERIALIZABLE     → 문제 없음 (성능 최저)

동시성 문제:
- Dirty Read: 미확정 데이터 읽기
- Non-Repeatable Read: 같은 쿼리 결과 변경
- Phantom Read: 없던 행이 나타남

MVCC (Multi-Version Concurrency Control):
읽기 = 스냅샷 읽기 (잠금 없음) → 동시성 극대화
쓰기 = 잠금으로 충돌 방지
```

## 3. 2PL (2-Phase Locking)

```
확장 단계: 잠금 획득 (해제 불가)
수축 단계: 잠금 해제 (획득 불가)
→ 직렬성 보장 but 교착상태 가능
```

## 4. 답안 포인트

**3단락**: ① ACID 4속성 정의 → ② 격리 수준별 특성·문제 비교표 → ③ MVCC vs 2PL 현대 적용

## 5. 관련 개념

`교착상태(DB)` → 잠금 순환 | `분산 트랜잭션` → 2PC(2단계 커밋) | `MVCC` → PostgreSQL/InnoDB 기본
