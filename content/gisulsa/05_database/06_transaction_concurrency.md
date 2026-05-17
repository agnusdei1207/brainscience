+++
weight = 6
title = "06. 클라우드 배포 모델"
date = "2026-05-17"
[extra]
categories = "gisulsa-database"
+++

# 트랜잭션 ACID & 동시성 제어

> 별점: ★★★★★ | 매회 기본 필출

---

## 답안.

### Ⅰ. 개요

격리 수준           문제 현상
────────────────────────────────────────
READ UNCOMMITTED → Dirty Read 발생

### Ⅱ. 핵심 구성요소

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
```
확장 단계: 잠금 획득 (해제 불가)
수축 단계: 잠금 해제 (획득 불가)
→ 직렬성 보장 but 교착상태 가능
```


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
