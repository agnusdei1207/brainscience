+++
title = "039. 일반 집합 연산자 (Set Operations)"
date = "2026-03-05"
weight = 39
[extra]
categories = "studynotes-database"
tags = ["database", "relational-algebra", "set-operations", "union", "intersection"]
+++

# 039. 일반 집합 연산자 (Set Operations)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 일반 집합 연산자는 수학의 집합론(Set Theory)에서 유래한 연산자로, 합집합(Union), 교집합(Intersection), 차집합(Difference), 카티션 프로덕트(Cartesian Product)를 포함한다.
> 2. **가치**: 두 릴레이션 간의 집합 조작을 가능하게 하며, SQL의 UNION, INTERSECT, EXCEPT/MINUS, CROSS JOIN으로 직접 구현된다.
> 3. **융합**: Union Compatibility(합집합 호환성) 조건은 차수(Degree)와 속성 도메인(Domain)의 일치를 요구하며, 카티션 프로덕트는 조인(Join)의 이론적 기반이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**일반 집합 연산자**는 관계 대수에서 두 개의 릴레이션을 입력받아 집합론적 연산을 수행하는 연산자들이다. 이 연산자들은 릴레이션을 튜플의 집합으로 취급하여 수학적 집합 연산을 적용한다.

### 💡 비유

**일반 집합 연산자를 서로 다른 반의 학생 목록**에 비유할 수 있다:
- **합집합**: 두 반 학생 전체 명단 (중복 제거)
- **교집합**: 두 반에 모두 속한 학생 (전과 학생)
- **차집합**: A반에만 있는 학생 (B반 학생 제외)
- **카티션 프로덕트**: A반 학생 × B반 학생의 모든 가능한 짝 (체육대회 2인 조합)

### Union Compatibility (합집합 호환성)

합집합, 교집합, 차집합 연산을 수행하려면 두 릴레이션이 **Union Compatible**해야 한다:
1. **동일한 차수(Degree)**: 속성(컬럼) 개수가 같아야 함
2. **대응 속성의 도메인 호환**: 같은 순서의 속성들이 호환 가능한 도메인을 가져야 함

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 합집합 (Union, ∪)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         UNION (∪) - 합집합                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  정의: R ∪ S = {t | t ∈ R ∨ t ∈ S}                                          │
│  R 또는 S에 속하는 모든 튜플 (중복 제거)                                    │
│                                                                             │
│  R:                    S:                    R ∪ S:                         │
│  ┌──────┬───────┐     ┌──────┬───────┐     ┌──────┬───────┐                │
│  │ ID   │ Name  │     │ ID   │ Name  │     │ ID   │ Name  │                │
│  ├──────┼───────┤     ├──────┼───────┤     ├──────┼───────┤                │
│  │ 1    │ Kim   │     │ 2    │ Lee   │     │ 1    │ Kim   │                │
│  │ 2    │ Lee   │     │ 3    │ Park  │     │ 2    │ Lee   │                │
│  └──────┴───────┘     │ 4    │ Choi  │     │ 3    │ Park  │                │
│                       └──────┴───────┘     │ 4    │ Choi  │                │
│                                             └──────┴───────┘                │
│                                                                             │
│  SQL:                                                                       │
│  SELECT * FROM R                                                            │
│  UNION                        -- 중복 자동 제거                              │
│  SELECT * FROM S;                                                           │
│                                                                             │
│  SQL (중복 허용):                                                           │
│  SELECT * FROM R UNION ALL SELECT * FROM S;                                 │
│                                                                             │
│  특성:                                                                      │
│  • 교환법칙: R ∪ S = S ∪ R                                                 │
│  • 결합법칙: (R ∪ S) ∪ T = R ∪ (S ∪ T)                                     │
│  • |R ∪ S| ≤ |R| + |S|                                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 교집합 (Intersection, ∩)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       INTERSECTION (∩) - 교집합                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  정의: R ∩ S = {t | t ∈ R ∧ t ∈ S}                                          │
│  R과 S 모두에 속하는 튜플                                                   │
│                                                                             │
│  R:                    S:                    R ∩ S:                         │
│  ┌──────┬───────┐     ┌──────┬───────┐     ┌──────┬───────┐                │
│  │ ID   │ Name  │     │ ID   │ Name  │     │ ID   │ Name  │                │
│  ├──────┼───────┤     ├──────┼───────┤     ├──────┼───────┤                │
│  │ 1    │ Kim   │     │ 2    │ Lee   │     │ 2    │ Lee   │                │
│  │ 2    │ Lee   │     │ 3    │ Park  │     └──────┴───────┘                │
│  │ 5    │ Jung  │     │ 4    │ Choi  │                                      │
│  └──────┴───────┘     │ 5    │ Jung  │     1 row (Lee만 공통)              │
│                       └──────┴───────┘                                       │
│                                                                             │
│  SQL:                                                                       │
│  SELECT * FROM R                                                            │
│  INTERSECT                   -- MySQL는 미지원, 다른 방식 필요              │
│  SELECT * FROM S;                                                           │
│                                                                             │
│  MySQL 대안:                                                                │
│  SELECT R.* FROM R INNER JOIN S ON R.ID = S.ID AND R.Name = S.Name;        │
│  또는: SELECT * FROM R WHERE ID IN (SELECT ID FROM S);                      │
│                                                                             │
│  특성:                                                                      │
│  • 교환법칙: R ∩ S = S ∩ R                                                 │
│  • 결합법칙: (R ∩ S) ∩ T = R ∩ (S ∩ T)                                     │
│  • |R ∩ S| ≤ min(|R|, |S|)                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. 차집합 (Difference, -)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DIFFERENCE (-) - 차집합                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  정의: R - S = {t | t ∈ R ∧ t ∉ S}                                          │
│  R에는 있지만 S에는 없는 튜플                                               │
│                                                                             │
│  R:                    S:                    R - S:                         │
│  ┌──────┬───────┐     ┌──────┬───────┐     ┌──────┬───────┐                │
│  │ ID   │ Name  │     │ ID   │ Name  │     │ ID   │ Name  │                │
│  ├──────┼───────┤     ├──────┼───────┤     ├──────┼───────┤                │
│  │ 1    │ Kim   │     │ 2    │ Lee   │     │ 1    │ Kim   │                │
│  │ 2    │ Lee   │     │ 3    │ Park  │     │ 5    │ Jung  │                │
│  │ 5    │ Jung  │     │ 4    │ Choi  │     └──────┴───────┘                │
│  └──────┴───────┘     │ 5    │ Jung  │                                      │
│                       └──────┴───────┘     Kim, Jung (R에만 있음)          │
│                                                                             │
│  SQL:                                                                       │
│  SELECT * FROM R                                                            │
│  EXCEPT                      -- Oracle: MINUS                               │
│  SELECT * FROM S;            -- MySQL: NOT EXISTS 또는 LEFT JOIN           │
│                                                                             │
│  MySQL 대안:                                                                │
│  SELECT R.* FROM R LEFT JOIN S ON R.ID = S.ID WHERE S.ID IS NULL;          │
│  또는: SELECT * FROM R WHERE ID NOT IN (SELECT ID FROM S);                  │
│                                                                             │
│  특성:                                                                      │
│  • 비교환법칙: R - S ≠ S - R                                               │
│  • 비결합법칙: (R - S) - T ≠ R - (S - T)                                   │
│  • |R - S| ≤ |R|                                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4. 카티션 프로덕트 (Cartesian Product, ×)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                  CARTESIAN PRODUCT (×) - 카티션 프로덕트                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  정의: R × S = {(r, s) | r ∈ R ∧ s ∈ S}                                     │
│  R의 각 튜플과 S의 각 튜플의 모든 가능한 조합                               │
│                                                                             │
│  R (학생):             S (과목):            R × S:                          │
│  ┌──────┬───────┐     ┌──────┬───────┐     ┌──────┬───────┬──────┬───────┐│
│  │ S_ID │ Name  │     │ C_ID │ Course│     │S_ID  │ Name  │C_ID  │Course ││
│  ├──────┼───────┤     ├──────┼───────┤     ├──────┼───────┼──────┼───────┤│
│  │ 1    │ Kim   │     │ 101  │ Math  │     │ 1    │ Kim   │ 101  │ Math  ││
│  │ 2    │ Lee   │     │ 102  │ Eng   │     │ 1    │ Kim   │ 102  │ Eng   ││
│  └──────┴───────┘     └──────┴───────┘     │ 2    │ Lee   │ 101  │ Math  ││
│                                             │ 2    │ Lee   │ 102  │ Eng   ││
│  2 rows                2 rows               └──────┴───────┴──────┴───────┘│
│                                                                             │
│                                            2 × 2 = 4 rows                  │
│                                                                             │
│  SQL:                                                                       │
│  SELECT * FROM R, S;                       -- CROSS JOIN                    │
│  SELECT * FROM R CROSS JOIN S;                                              │
│                                                                             │
│  특성:                                                                      │
│  • 차수: deg(R × S) = deg(R) + deg(S)                                      │
│  • 카디널리티: |R × S| = |R| × |S|                                         │
│  • 교환법칙: R × S ≠ S × R (컬럼 순서 다름, 의미상 동일)                   │
│  • 결합법칙: (R × S) × T = R × (S × T)                                     │
│                                                                             │
│  주의: 대용량 테이블 간 카티션 프로덕트는 결과가 폭발적으로 증가!           │
│        100만 × 100만 = 1조 행                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5. 일반 집합 연산자 비교 요약

| 연산자 | 기호 | SQL | 결과 크기 | 교환법칙 | 결합법칙 |
|:---|:---|:---|:---|:---|:---|
| 합집합 | ∪ | UNION | ≤ \|R\| + \|S\| | O | O |
| 교집합 | ∩ | INTERSECT | ≤ min(\|R\|, \|S\|) | O | O |
| 차집합 | - | EXCEPT/MINUS | ≤ \|R\| | X | X |
| 카티션 | × | CROSS JOIN | \|R\| × \|S\| | X* | O |

*컬럼 순서만 다르고 의미상 동일

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. SQL 표준별 지원 현황

| 연산 | ANSI SQL | Oracle | MySQL | PostgreSQL | SQL Server |
|:---|:---|:---|:---|:---|:---|
| UNION | O | O | O | O | O |
| UNION ALL | O | O | O | O | O |
| INTERSECT | O | O | X | O | O |
| INTERSECT ALL | O | X | X | O | O |
| EXCEPT | O | X (MINUS) | X | O | O |
| EXCEPT ALL | O | X | X | O | O |

### 2. 카티션 프로덕트와 조인의 관계

```
Cartesian Product: R × S (모든 조합)
        ↓
Selection 추가: σ_condition(R × S) = R ⋈_condition S (조인)

모든 조인은 카티션 프로덕트 + 조건 필터링으로 표현 가능!
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 시나리오 1: 데이터 병합

**문제 상황**: 여러 지사의 고객 데이터를 통합해야 함

**기술사적 결단**:
```sql
-- UNION ALL이 성능상 유리 (중복 검사 생략)
SELECT * FROM branch_a_customers
UNION ALL
SELECT * FROM branch_b_customers;

-- 중복 제거가 필요한 경우
SELECT * FROM branch_a_customers
UNION
SELECT * FROM branch_b_customers;
```

### 시나리오 2: 미구매 고객 찾기

**문제 상황**: 전체 회원 중 한 번도 구매하지 않은 회원 식별

**기술사적 결단**:
```sql
-- 차집합 활용
SELECT * FROM members
EXCEPT
SELECT DISTINCT m.* FROM members m
JOIN orders o ON m.member_id = o.member_id;

-- 또는 NOT EXISTS (성능상 더 유리할 수 있음)
SELECT * FROM members m
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.member_id);
```

### 안티패턴

1. **UNION vs UNION ALL 오용**: 중복 제거가 불필요한데 UNION 사용 → 불필요한 정렬 연산
2. **카티션 프로덕트 실수**: JOIN 조건 누락 → 의도치 않은 CROSS JOIN 발생

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 항목 | 적절한 연산자 사용 시 |
|:---|:---|
| **UNION ALL vs UNION** | 중복 검사 생략으로 30~50% 성능 향상 |
| **INTERSECT vs JOIN** | 가독성 향상, 의도 명확화 |
| **EXCEPT vs NOT IN** | NULL 처리 일관성 확보 |

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [[038_관계_대수]](./38_relational_algebra.md): 집합 연산자를 포함한 전체 연산 체계
- [[040_순수_관계_연산자]](./40_relational_operators.md): 관계형 모델 고유의 연산자
- [[132_내부_조인]](../2_sql/132_inner_join.md): 카티션 프로덕트 + 조건의 구현
- [[150_집합_연산자_SQL]](../2_sql/150_set_operators_sql.md): SQL에서의 집합 연산 구현

---

## 👶 어린이를 위한 3줄 비유 설명

1. **합집합은 두 반 명단 합치기**: 1반 명단과 2반 명단을 합쳐서, 같은 이름은 한 번만 적는 전체 명단을 만드는 거예요.

2. **교집합은 공통 친구 찾기**: 내 친구 목록과 너의 친구 목록에서 우리 둘 다 아는 친구들만 골라내는 거예요.

3. **차집합은 나만의 친구 찾기**: 내 친구 중에서 너는 모르는 친구들만 골라내는 거예요. 반대로 하면 너만 아는 친구들이 나오겠죠?
