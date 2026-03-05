+++
title = "044. 디비전 (Division, ÷)"
date = "2026-03-05"
weight = 44
[extra]
categories = "studynotes-database"
tags = ["database", "relational-algebra", "division", "forall"]
+++

# 044. 디비전 (Division, ÷)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 디비전(Division, ÷)은 릴레이션 R이 릴레이션 S의 모든 속성값을 포함하는 튜플을 찾는 관계 대수 연산자로, "모든(∀)" 조건을 표현한다.
> 2. **가치**: "모든 과목을 이수한 학생", "모든 제품을 구매한 고객" 같은 전칭(∀) 질의를 표현할 수 있는 유일한 관계 대수 연산자다.
> 3. **융합**: SQL에는 직접적인 디비전 연산이 없어 NOT EXISTS의 이중 중첩으로 구현하며, 이는 RDBMS에서 가장 이해하기 어려운 패턴 중 하나다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**디비전(Division, ÷)**은 릴레이션 R(A, B)과 릴레이션 S(B)가 주어졌을 때, S의 모든 B값에 대해 (A, B) 쌍이 R에 존재하는 A값들을 찾는 연산이다. 수학적으로는:

```
R ÷ S = {t | ∀s ∈ S, (t, s) ∈ R}
```

### 💡 비유

디비전을 **체크리스트 완수**에 비유할 수 있다:
- 체크리스트 S: [수학, 영어, 과학]
- 학생들의 이수 과목 R:
  - Kim: [수학, 영어] → 불완료 ✗
  - Lee: [수학, 영어, 과학] → 완료 ✓
  - Park: [수학, 영어, 과학, 사회] → 완료 ✓
- R ÷ S = {Lee, Park}

### 활용 예시

1. "모든 필수 과목을 이수한 학생 찾기"
2. "모든 부서에 프로젝트 참여한 직원 찾기"
3. "모든 태그가 붙은 게시글 찾기"

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 디비전 연산 구조

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DIVISION OPERATION (÷)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  R (수강):                              S (필수 과목):                      │
│  ┌──────┬────────┐                     ┌────────┐                          │
│  │ 학생 │ 과목   │                     │ 과목   │                          │
│  ├──────┼────────┤                     ├────────┤                          │
│  │ Kim  │ Math   │                     │ Math   │                          │
│  │ Kim  │ English│                     │ English│                          │
│  │ Lee  │ Math   │                     └────────┘                          │
│  │ Lee  │ English│                                                         │
│  │ Lee  │ Science│                     R ÷ S 결과:                         │
│  │ Park │ Math   │                     ┌──────┐                            │
│  │ Park │ English│                     │ 학생 │                            │
│  └──────┴────────┘                     ├──────┤                            │
│                                         │ Kim  │                            │
│  Kim: Math, English (S의 모든 과목 ✓)  │ Lee  │                            │
│  Lee: Math, English, Science (모두 ✓)  └──────┘                            │
│  Park: Math만 (English 없음 ✗)                                             │
│                                                                             │
│  특성:                                                                      │
│  • 차수: deg(R ÷ S) = deg(R) - deg(S)                                      │
│  • 카디널리티: |R ÷ S| ≤ |π_R-S(R)|                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 디비전의 대수적 정의

```text
R(A, B) ÷ S(B) = π_A(R) - π_A((π_A(R) × S) - R)

풀이:
1. π_A(R): R에 있는 모든 A값
2. π_A(R) × S: 모든 (A, B) 조합
3. (π_A(R) × S) - R: R에 없는 조합
4. π_A(3): 불완전한 A값들
5. π_A(R) - 4: 완전한 A값들
```

### 3. SQL 구현 (이중 NOT EXISTS)

```sql
-- "모든 필수 과목을 이수한 학생 찾기"

-- 방법 1: 이중 NOT EXISTS (가장 일반적)
SELECT DISTINCT 학생
FROM R R1
WHERE NOT EXISTS (
    SELECT *
    FROM S
    WHERE NOT EXISTS (
        SELECT *
        FROM R R2
        WHERE R2.학생 = R1.학생
        AND R2.과목 = S.과목
    )
);

-- 해석: "S에 있는 어떤 과목도 수강하지 않은 경우가 없는 학생"
--      = "S의 모든 과목을 수강한 학생"

-- 방법 2: GROUP BY + HAVING COUNT
SELECT 학생
FROM R
WHERE 과목 IN (SELECT 과목 FROM S)
GROUP BY 학생
HAVING COUNT(DISTINCT 과목) = (SELECT COUNT(*) FROM S);

-- 방법 3: NOT IN + 서브쿼리
SELECT DISTINCT 학생 FROM R R1
WHERE 학생 NOT IN (
    SELECT R2.학생
    FROM (SELECT DISTINCT 학생 FROM R) R2, S
    WHERE NOT EXISTS (
        SELECT * FROM R R3
        WHERE R3.학생 = R2.학생 AND R3.과목 = S.과목
    )
);
```

### 4. 디비전 구현 다이어그램

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DIVISION IMPLEMENTATION LOGIC                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  질의: "모든 S를 가진 R 찾기"                                               │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  FOR each candidate A in R:                                          │   │
│  │      found_all = TRUE                                                │   │
│  │      FOR each B in S:                                                │   │
│  │          IF (A, B) NOT IN R THEN                                     │   │
│  │              found_all = FALSE                                       │   │
│  │              BREAK                                                   │   │
│  │      IF found_all THEN                                               │   │
│  │          OUTPUT A                                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  NOT EXISTS 패턴으로 변환:                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  NOT EXISTS (                                                        │   │
│  │      SELECT * FROM S                                                 │   │
│  │      WHERE NOT EXISTS (                                              │   │
│  │          SELECT * FROM R                                             │   │
│  │          WHERE R.A = :candidate_A AND R.B = S.B                      │   │
│  │      )                                                               │   │
│  │  )                                                                   │   │
│  │                                                                      │   │
│  │  "R에 (A, B)가 없는 S.B가 존재하지 않는다"                          │   │
│  │  = "모든 S.B에 대해 R에 (A, B)가 있다"                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 1. 디비전 vs 다른 연산자

| 연산자 | 의미 | SQL 패턴 |
|:---|:---|:---|
| 셀렉트 | "어떤 조건을 만족하는" | WHERE |
| 프로젝트 | "어떤 속성을" | SELECT |
| 조인 | "어떤 관계가 있는" | JOIN |
| 디비전 | "모든 것을 가진" | NOT EXISTS 이중 |

### 2. 관계 대수의 완전성

디비전은 기본 연산자들로 표현 가능:
```
R ÷ S = π_(R-S)(R) - π_(R-S)(π_(R-S)(R) × S - R)
```

따라서 디비전은 필수 연산자는 아니지만, 편의성과 가독성을 위해 사용된다.

---

## Ⅳ. 실무 적용

### 시나리오: 복잡한 비즈니스 규칙 구현

**문제**: "모든 필수 교육을 이수한 직원에게만 자격증 발급"

```sql
-- 자격증 발급 대상 조회
SELECT e.emp_id, e.emp_name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM required_trainings rt
    WHERE NOT EXISTS (
        SELECT 1 FROM completed_trainings ct
        WHERE ct.emp_id = e.emp_id
        AND ct.training_id = rt.training_id
    )
);
```

### 성능 고려사항

1. **인덱스 활용**: (emp_id, training_id) 복합 인덱스
2. **GROUP BY 대안**: 대량 데이터에서 더 효율적일 수 있음
3. **Materialized View**: 자주 실행되는 경우

---

## Ⅴ. 기대효과 및 결론

### 정량적/정성적 기대효과

| 구현 방식 | 가독성 | 성능 |
|:---|:---|:---|
| 이중 NOT EXISTS | 낮음 (이해 어려움) | 중간 |
| GROUP BY + HAVING | 높음 | 높음 (대량 데이터) |

---

## 📌 관련 개념 맵

- [[040_순수_관계_연산자]](./40_relational_operators.md): 전체 관계 연산자
- [[038_관계_대수]](./38_relational_algebra.md): 관계 대수 체계
- [서브쿼리](../2_sql/subquery.md): SQL 서브쿼리 패턴

---

## 👶 어린이를 위한 3줄 비유

1. **모든 과제를 한 친구**: 선생님이 "수학, 영어, 과학 과제를 다 한 사람만 칭찬해요!"라고 할 때, 세 과목을 모두 끝낸 친구만 찾는 것과 같아요.

2. **체크리스트 완성**: 준비물 체크리스트에 있는 연필, 지우개, 자를 모두 가지고 온 친구만 찾는 거예요. 하나라도 빠지면 안 돼요!

3. **전체를 다 한 사람**: "빨강, 파랑, 노랑 색연필로 그림을 다 그린 사람?"이라고 물으면 세 가지 색으로 모두 그린 사람만 손을 드는 것과 같아요.
