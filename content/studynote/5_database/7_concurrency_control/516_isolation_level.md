+++
title = "격리 수준 (Isolation Level)"
description = "트랜잭션 격리 수준의 개념과 네 가지 표준 수준에 대해 설명"
date = 2024-01-01
weight = 516

[taxonomies]
subjects = ["database"]
+++
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 격리 수준(Isolation Level)은 동시 실행되는 트랜잭션 간의 간섭 정도를 조절하는 수준으로, READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE의 네 가지 표준 수준이 있다.
> 2. **가치**: 높은 격리 수준은 데이터 일관성을 보장하지만 성능(동시성)이 저하되고, 낮은 격리 수준은 성능은 좋지만 일관성 위험이 증가한다.
> 3. **융합**: 격리 수준은 2PL과 결합되어 구현되며, 각 수준에서 발생할 수 있는 이상 현상(Dirty Read, Non-repeatable Read, Phantom Read)이 정의되어 있다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념
격리 수준(Isolation Level)은 ANSI SQL 표준에서 정의한 트랜잭션 간 간섭 허용 정도로, 네 가지 수준이 있다. 각 수준은 특정 종류의 이상 현상(Anomaly)을 허용하거나 방지한다.

### 네 가지 격리 수준과 이상 현상

| 격리 수준 | Dirty Read | Non-repeatable Read | Phantom Read |
|:---|:---|:---|:---|
| **READ UNCOMMITTED** | 허용 | 허용 | 허용 |
| **READ COMMITTED** | 방지 | 허용 | 허용 |
| **REPEATABLE READ** | 방지 | 방지 | 허용 |
| **SERIALIZABLE** | 방지 | 방지 | 방지 |

### 필요성
모든 트랜잭션을 SERIALIZABLE로 처리하면 데이터 일관성은 보장되지만, 성능이 크게 저하된다. 애플리케이션의 요구에 맞는 적절한 격리 수준 선택이 필요하다.

### 비유
격리 수준은ynchronized의程度와 같다. 가장 강한同步(격리)는 모든人が順番待ち하지만(정확하지만 느림), 약한同步(격리)는 여러人が同時进行하지만(빠르지만不 정확한 경우あり) 있다.

### 섹션 요약 비유
격리 수준 선택은 운동장의 격자 영역 선택과 같다. 격자를 작게(강한 격리) 하면 동시에 사용할 수 있는人数가 줄지만, 격자 크래프트(격리 수준 강도)가 좋아진다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 각 격리 수준 상세 동작

```text
  ┌───────────────────────────────────────────────────────────────────────┐
  │                    격리 수준별 동작 예시                                   │
  ├───────────────────────────────────────────────────────────────────────┤
  │
  │   [READ UNCOMMITTED]                                                 │
  │   T1: UPDATE SET salary = 100 WHERE dept = 'IT';  -- COMMIT 전      │
  │   T2: SELECT salary FROM IT;         -- T1 COMMIT 전인데 T1의 변경을 읽음  │
  │   Result: T2는 T1의 미 COMMIT 변경을 읽음 (Dirty Read)              │
  │
  │   [READ COMMITTED]                                                   │
  │   T1: SELECT salary FROM IT;  -- salary = 50                       │
  │   T2: UPDATE SET salary = 100 WHERE dept = 'IT'; -- COMMIT           │
  │   T1: SELECT salary FROM IT;  -- salary = 100 (다시 읽으면 다른 값!)   │
  │   Result: Non-repeatable Read 발생                                  │
  │
  │   [REPEATABLE READ]                                                  │
  │   T1: SELECT * FROM employee;  -- 3건                               │
  │   T2: INSERT INTO employee VALUES (4, ...); -- COMMIT                │
  │   T1: SELECT * FROM employee;  -- 여전히 3건 (팬텀 로우 허용)         │
  │   Result: Phantom Read 발생 (새 행 삽입은 감지 못함)                   │
  │
  │   [SERIALIZABLE]                                                     │
  │   T1: SELECT COUNT(*) FROM employee;  -- 3                          │
  │   T2: INSERT INTO employee VALUES (4, ...);                         │
  │   T1: SELECT COUNT(*) FROM employee;  -- 4 (또는 오류 발생)           │
  │   Result: 범위 잠금으로 Phantom Read 방지                            │
  │
  └───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 각 격리 수준에서 허용되는 이상 현상은 그 수준에 따라 다르다. READ UNCOMMITTED는 가장 낮은 수준으로, 다른 트랜잭션의 미 COMMIT 변경도 읽을 수 있어 Dirty Read가 발생할 수 있다. READ COMMITTED는 COMMIT된 변경만 읽지만, 같은 트랜잭션 내에서도 재읽기 시 값이 달라질 수 있어 Non-repeatable Read가 발생한다. REPEATABLE READ는 같은 트랜잭션 내의 재읽기를 보장하지만, 새 행 삽입은 감지하지 못하는 Phantom Read가 발생한다. SERIALIZABLE은最强的 격리로, 범위 잠금(Range Lock)을 통해 Phantom Read까지 방지하지만, 동시성이 가장 크게 저하된다.

### DBMS별 기본 격리 수준

| DBMS | 기본 격리 수준 |
|:---|:---|
| **Oracle** | READ COMMITTED |
| **PostgreSQL** | READ COMMITTED |
| **MySQL InnoDB** | REPEATABLE READ |
| **SQL Server** | READ COMMITTED |

### 섹션 요약 비유
격리 수준은 운동 경기의ルールと 같다. 조깅 대회(READ UNCOMMITTED)는 다른 주자를 뛰어넘어도 되지만(다른 트랜잭션의 변경 읽기), 마라톤(READ COMMITTED)은 다른 주자를 넘을 수 없고, 단거리 달리기(SERIALIZABLE)는 정확한 차道上에서만 달릴 수 있다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: 격리 수준 vs 동시성/일관성

| 격리 수준 | 동시성 | 일관성 보장 | 성능 영향 |
|:---|:---|:---|:---|
| **READ UNCOMMITTED** | 가장 높음 | 가장 낮음 | 가장 낮음 |
| **READ COMMITTED** | 높음 | 중간 | 낮음 |
| **REPEATABLE READ** | 중간 | 높음 | 중간 |
| **SERIALIZABLE** | 가장 낮음 | 가장 높음 | 가장 높음 |

### 섹션 요약 비유
격리 수준 선택은 보안 강도와便利性の 트레이드오프와 같다. 가장 강한 보안(격리)은 출입证件을매번 확인하므로(잠금 획득) 시간이 걸리고, 낮은 보안은 빠르지만 위험이 따른다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 — 금융 vs 웹 애플리케이션**: 금융 시스템에서는 REPEATABLE READ 또는 SERIALIZABLE을 사용하여, 동일 트랜잭션 내의 재읽기가 동일한 결과를 보장해야 한다. 반면 소셜 미디어에서는 READ COMMITTED로 충분하며, 실제로 몇 초간의 불일치는許容される。

### 도입 체크리스트
- **기술적**: 애플리케이션이 요구하는 일관성이 어느 수준인지 분석하고, 그에 맞는 격리 수준을 선택해야 한다.
- **운영·보안적**: 격리 수준을 높이면 잠금 경합이 증가하여 전체 처리량이 저하될 수 있다.

### 안티패턴
- **불필요한 SERIALIZABLE**: 대부분의 웹 애플리케이션에서 READ COMMITTED로 충분한데 SERIALIZABLE을 사용하면 성능만 불필요하게 저하된다.
- **격리 수준 무시**: 개발자가 격리 수준을意識하지 않고 코딩하면, 특정 환경에서 일관성 문제가 발생할 수 있다.

### 섹션 요약 비유
격리 수준 선택은 집안 보안 시스템 선택과 같다.、银行級 보안을住宅에 도입하면 불편하고 비용이 들지만, 소규모 가게에는 적합하다.

---

## Ⅴ. 기대효과 및 결론

### 격리 수준 선택 가이드

| 상황 | 권장 격리 수준 |
|:---|:---|
| **읽기 전용レポート** | READ COMMITTED |
| **계좌 잔액 조회** | REPEATABLE READ |
| **금융 거래/송금** | SERIALIZABLE |
| **简单한 상태 조회** | READ COMMITTED |

### 섹션 요약 비유
격리 수준 선택은 건강검진 항목 선택과 같다. 전체 검진(격리 강함)은 정확하지만 비용과 시간이 많이 들고, 기본 검진(격리 약함)은 빠르게 하지만 놓칠 수 있는 항목이 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **2PL** | 격리 수준은 2PL 프로토콜 위에서 구현되며, 잠금 모드와 범위에 따라 수준이 결정된다. |
| **Dirty Read** | READ UNCOMMITTED에서만 허용되는 이상 현상으로, 미 COMMIT 데이터를 읽는 것이다. |
| **Non-repeatable Read** | READ COMMITTED에서 허용되는 이상 현상으로, 재읽기 시 값이 달라지는 것이다. |
| **Phantom Read** | REPEATABLE READ에서 허용되는 이상 현상으로, 새 행의 삽입/삭제가 감지되는 것이다. |
| **SERIALIZABLE** | 最強의 격리 수준으로, 범위 잠금을 통해 모든 이상 현상을 방지한다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. 격리 수준은 **운동장의 규칙**과 같아서, 격자(잠금)가 촘촘하면(격리 강함) 다른 사람과 충돌하지 않지만, 함께 놀 수 있는 친구가 줄어들어요.
2. 격자间距が広いと(격리 약함) 더 많은 친구와 놀 수 있지만(동시성), 때때로 서로 부딪힐 수 있어요(불일치).
3. 금융 시스템은 정확한 成續가 중요하니까(Strong 격리), 친구との 게임(社交 앱)은 조금 틀려도 괜찮아요(Weak 격리)!
