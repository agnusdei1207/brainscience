+++
title = "22. 부울 대수 (Boolean Algebra)"
description = "디지털 논리회로의 수학적 기초인 부울 대수의 원리와 응용 심층 분석"
date = "2026-03-05"
[taxonomies]
tags = ["부울대수", "Boolean Algebra", "논리연산", "디지털회로", "조지 불", "진리표", "논리게이트"]
categories = ["studynotes-1_computer_architecture"]
+++

# 22. 부울 대수 (Boolean Algebra)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 부울 대수는 1854년 조지 불(George Boole)이 제안한 이진 논리 체계로, 참(1)과 거짓(0) 두 값만을 사용하여 AND, OR, NOT 연산을 수행하는 수학적 체계이다.
> 2. **가치**: 모든 디지털 컴퓨터의 논리적 기반을 제공하며, 복잡한 회로를 수학적으로 간소화하여 게이트 수를 30~50% 감소시켜 칩 면적과 전력 소비를 획기적으로 줄인다.
> 3. **융합**: 프로그래밍 언어의 조건문, 데이터베이스 쿼리(SQL WHERE절), 검색 엔진 필터링, AI 의사결정 트리 등 현대 컴퓨팅 전 영역에서 필수적으로 활용된다.

---

### I. 개요 (Context & Background)

#### 개념 정의

**부울 대수(Boolean Algebra)**는 두 값(참/거짓, 1/0, ON/OFF)만을 다루는 대수 체계로, 일반 대수와는 다른 독자적인 연산 법칙을 갖는다. 1854년 영국의 수학자 조지 불(George Boole)이 저서 "The Laws of Thought"에서 처음 제안하였으며, 1938년 클로드 섀넌(Claude Shannon)이 이를 전자 스위치 회로에 적용함으로써 현대 디지털 컴퓨터의 이론적 기반이 되었다.

부울 대수의 세 가지 기본 연산:
- **AND (논리곱)**: A * B 또는 A AND B, 두 입력이 모두 1일 때만 1 출력
- **OR (논리합)**: A + B 또는 A OR B, 두 입력 중 하나라도 1이면 1 출력
- **NOT (논리부정)**: A' 또는 NOT A, 입력의 반대값 출력

#### 비유

> **부울 대수는 "스위치의 언어"와 같다.**
>
> 전기 스위치는 켜짐(1)과 꺼짐(0) 두 상태만 있다. 스위치 두 개를 직렬로 연결하면 둘 다 켜야 전구가 켜진다(AND). 병렬로 연결하면 하나만 켜도 전구가 켜진다(OR). 스위치를 반대로 동작하게 하면 NOT이다. 부울 대수는 이런 스위치들의 조합을 수학으로 표현한 것이다.

#### 등장 배경 및 발전 과정

1. **1854년: 조지 불의 창시**
   - "The Laws of Thought"에서 논리적 추론을 수학적으로 표현
   - 심볼릭 로직의 기초 확립
   - 인간의 사고 과정을 기호화하려는 철학적 시도

2. **1938년: 클로드 섀넌의 응용**
   - MIT 석사 논문 "A Symbolic Analysis of Relay and Switching Circuits"
   - 부울 대수를 전화 교환기 릴레이 회로 설계에 적용
   - 디지털 회로 설계의 수학적 기반 제공

3. **1940~50년대: 컴퓨터 시대 개막**
   - 폰 노이만 구조 컴퓨터의 논리 설계에 적용
   - ENIAC, EDVAC 등 초기 컴퓨터의 회로 설계
   - 논리 게이트의 표준화

4. **1960년대~현재: VLSI 및 CAD 도구**
   - 부울 대수 간소화 알고리즘 (Quine-McCluskey, Espresso)
   - HDL(Hardware Description Language)의 기반
   - 자동 논리 합성 도구의 이론적 토대

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 부울 대수 기본 공식표

| 공식명 | AND 형식 | OR 형식 | 비고 |
|--------|----------|---------|------|
| **항등 법칙** | A * 1 = A | A + 0 = A | 항등원 |
| **영/일 법칙** | A * 0 = 0 | A + 1 = 1 | 지배원 |
| **멱등 법칙** | A * A = A | A + A = A | 동일원 |
| **보수 법칙** | A * A' = 0 | A + A' = 1 | 상보성 |
| **이중 부정** | (A')' = A | - | NOT NOT |
| **교환 법칙** | A * B = B * A | A + B = B + A | 순서 무관 |
| **결합 법칙** | (A*B)*C = A*(B*C) | (A+B)+C = A+(B+C) | 그룹 무관 |
| **분배 법칙** | A*(B+C) = A*B + A*C | A+(B*C) = (A+B)*(A+C) | 전개/인수 |
| **드모르간 법칙** | (A*B)' = A' + B' | (A+B)' = A' * B' | 변환 핵심 |
| **흡수 법칙** | A*(A+B) = A | A+(A*B) = A | 제거 |
| **결합 흡수** | A + A'*B = A + B | A*(A'+B) = A*B | 유용한 변환 |

#### 부울 대수 연산 구조 다이어그램

```
                    부울 대수 연산 체계
    ┌────────────────────────────────────────────────────────────────┐
    │                                                                │
    │   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
    │   │  입력 변수   │     │  부울 연산   │     │  출력 함수   │    │
    │   │  A, B, C... │ ──▶ │ AND/OR/NOT  │ ──▶ │   F(A,B,C)  │    │
    │   └─────────────┘     └─────────────┘     └─────────────┘    │
    │          │                   │                   │           │
    │          │    ┌──────────────┴──────────────┐    │           │
    │          │    │         연산 법칙           │    │           │
    │          │    │  - 교환, 결합, 분배        │    │           │
    │          │    │  - 드모르간, 흡수          │    │           │
    │          │    │  - 최소화 (간소화)         │    │           │
    │          │    └─────────────────────────────┘    │           │
    │          │                   │                   │           │
    │          ▼                   ▼                   ▼           │
    │   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
    │   │  진리표     │     │  논리 회로  │     │  게이트망   │    │
    │   │Truth Table  │     │Logic Circuit│     │Gate Network │    │
    │   └─────────────┘     └─────────────┘     └─────────────┘    │
    │                                                                │
    │   ┌───────────────────────────────────────────────────────┐   │
    │   │                기본 게이트 진리표                       │   │
    │   ├───────────────────────────────────────────────────────┤   │
    │   │  A  │  B  │ AND │ OR  │ XOR │ NAND│ NOR │            │   │
    │   ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤            │   │
    │   │  0  │  0  │  0  │  0  │  0  │  1  │  1  │            │   │
    │   │  0  │  1  │  0  │  1  │  1  │  1  │  0  │            │   │
    │   │  1  │  0  │  0  │  1  │  1  │  1  │  0  │            │   │
    │   │  1  │  1  │  1  │  1  │  0  │  0  │  0  │            │   │
    │   └───────────────────────────────────────────────────────┘   │
    │                                                                │
    └────────────────────────────────────────────────────────────────┘
```

#### 5단계 부울 함수 간소화 프로세스

```
┌──────────────────────────────────────────────────────────────────┐
│         부울 함수 간소화 (Boolean Function Simplification)        │
└──────────────────────────────────────────────────────────────────┘

Step 1: [문제 정의 (Problem Definition)]
        ┌────────────────────────────────────────────────────┐
        │ - 요구사항을 진리표로 작성                         │
        │ - 출력이 1이 되는 모든 입력 조합 식별             │
        │ - 예: F(A,B,C) = Sigma m(1,3,5,7)                 │
        │   (입력 001, 011, 101, 111일 때 출력 1)           │
        └────────────────────────────────────────────────────┘
                                │
                                ▼
Step 2: [표준형 변환 (Canonical Form)]
        ┌────────────────────────────────────────────────────┐
        │ - 최소항(Minterm) 또는 최대항(Maxterm) 전개       │
        │ - SOP(Sum of Products) 또는 POS 형식              │
        │ - F = A'B'C + A'BC + AB'C + ABC                   │
        │   (각 항은 입력 조합 하나를 나타냄)               │
        └────────────────────────────────────────────────────┘
                                │
                                ▼
Step 3: [대수적 간소화 (Algebraic Simplification)]
        ┌────────────────────────────────────────────────────┐
        │ - 부울 대수 공식 적용                              │
        │ - 흡수 법칙: A + AB = A                           │
        │ - 결합 법칙으로 공통 인수 추출                    │
        │ - F = A'C(B+B') + AC(B'+B) = A'C + AC             │
        │ - 추가 간소화: A'C + AC = C(A'+A) = C             │
        └────────────────────────────────────────────────────┘
                                │
                                ▼
Step 4: [카르노 맵 검증 (Karnaugh Map Verification)]
        ┌────────────────────────────────────────────────────┐
        │ - 그룹화로 최적화 확인                             │
        │ - 인접한 1들을 2^n 크기로 그룹화                  │
        │ - 모든 1이 C열에 위치 → F = C                    │
        │ - 더 이상 간소화 불가 확인                        │
        └────────────────────────────────────────────────────┘
                                │
                                ▼
Step 5: [회로 구현 (Circuit Implementation)]
        ┌────────────────────────────────────────────────────┐
        │ - 최소화된 식을 게이트로 변환                      │
        │ - 게이트 수, 단계 수 확인                          │
        │ - F = C (단일 와이어, 게이트 불필요!)             │
        │ - 원래 4개 최소항이 1개 변수로 축소               │
        └────────────────────────────────────────────────────┘
```

#### 핵심 알고리즘: Quine-McCluskey 간소화

```python
#!/usr/bin/env python3
"""
Quine-McCluskey 알고리즘 구현
부울 함수의 최소 간소화를 위한 체계적 방법
- 다변수 함수에서 카르노 맵의 한계를 극복
- 컴퓨터 프로그램으로 구현 가능한 알고리즘적 접근
"""

from itertools import combinations
from typing import List, Set, Tuple, Dict

def count_ones(binary: str) -> int:
    """이진수의 1 개수 세기"""
    return binary.count('1')

def differs_by_one(a: str, b: str) -> Tuple[bool, str]:
    """두 이진수가 한 비트만 다른지 확인하고 결합 결과 반환"""
    diff_pos = -1
    count = 0
    for i, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            count += 1
            diff_pos = i
            if count > 1:
                return False, ""
    if count == 1:
        result = list(a)
        result[diff_pos] = '-'
        return True, ''.join(result)
    return False, ""

def quine_mccluskey(minterms: List[int], num_vars: int) -> List[str]:
    """
    Quine-McCluskey 알고리즘으로 부울 함수 간소화

    Args:
        minterms: 출력이 1인 최소항 리스트 (예: [1, 3, 5, 7])
        num_vars: 변수 개수

    Returns:
        간소화된 항(product term) 리스트
    """
    # 1단계: 최소항을 이진수로 변환하고 1의 개수로 그룹화
    groups: Dict[int, List[str]] = {}
    for m in minterms:
        binary = format(m, f'0{num_vars}b')
        ones = count_ones(binary)
        if ones not in groups:
            groups[ones] = []
        groups[ones].append(binary)

    # 2단계: 인접 그룹 간 결합 (Prime Implicant 찾기)
    prime_implicants: Set[str] = set()
    while groups:
        new_groups: Dict[int, List[str]] = {}
        used: Set[str] = set()

        group_keys = sorted(groups.keys())
        for i in range(len(group_keys) - 1):
            g1, g2 = group_keys[i], group_keys[i + 1]
            if g2 - g1 != 1:
                continue

            for a in groups[g1]:
                for b in groups[g2]:
                    can_combine, combined = differs_by_one(a, b)
                    if can_combine:
                        ones = count_ones(combined.replace('-', '0'))
                        if ones not in new_groups:
                            new_groups[ones] = []
                        if combined not in new_groups[ones]:
                            new_groups[ones].append(combined)
                        used.add(a)
                        used.add(b)

        # 사용되지 않은 항은 Prime Implicant
        for group in groups.values():
            for term in group:
                if term not in used:
                    prime_implicants.add(term)

        groups = new_groups

    return list(prime_implicants)

def term_to_expression(term: str, variables: str = "ABC") -> str:
    """이진 항을 부울 식으로 변환"""
    result = []
    for i, bit in enumerate(term):
        if bit == '1':
            result.append(variables[i])
        elif bit == '0':
            result.append(variables[i] + "'")
        # '-'는 생략 (해당 변수无关)
    return ' * '.join(result) if result else '1'

# 예시 사용
if __name__ == "__main__":
    # F(A,B,C) = Sigma m(1, 3, 5, 7) 간소화
    # 진리표: C=1일 때만 출력 1
    minterms = [1, 3, 5, 7]
    num_vars = 3

    print("=== Quine-McCluskey 알고리즘 ===")
    print(f"입력 최소항: {minterms}")
    print(f"이진수 표현: {[format(m, '03b') for m in minterms]}")

    primes = quine_mccluskey(minterms, num_vars)
    print(f"\nPrime Implicants: {primes}")

    # 결과 해석
    print("\n간소화된 항:")
    for p in primes:
        expr = term_to_expression(p)
        print(f"  {p} -> {expr}")

    # 최종 간소화된 식: F = C
    # (모든 최소항에서 C가 1이므로, --1 → C)
    print("\n최종 간소화된 식: F = C")
```

---

### III. 융합 비교 및 다각도 분석

#### 기본 게이트 vs 부울 연산 비교

| 부울 연산 | 기호 | 게이트 | 진리표 특징 | CMOS 트랜지스터 수 |
|-----------|------|--------|-------------|-------------------|
| A * B | AND | AND | 1개만 1 | 6 (4 NMOS + 2 PMOS) |
| A + B | OR | OR | 3개가 1 | 6 (2 NMOS + 4 PMOS) |
| A' | NOT | NOT | 반전 | 2 (1 NMOS + 1 PMOS) |
| (A*B)' | NAND | NAND | 1개만 0 | 4 (2 NMOS + 2 PMOS) |
| (A+B)' | NOR | NOR | 1개만 1 | 4 (2 NMOS + 2 PMOS) |
| A XOR B | XOR | XOR | 2개가 1 | 12~14 (복합 구조) |

#### 부울 대수 vs 일반 대수 비교

| 항목 | 일반 대수 | 부울 대수 | 차이점 |
|------|-----------|-----------|--------|
| **변수 값** | 무한 실수 | 0 또는 1 | 이산 vs 연속 |
| **덧셈** | 1+1=2 | 1+1=1 (OR) | 논리합 |
| **곱셈** | 2*3=6 | 1*1=1 (AND) | 논리곱 |
| **분배 법칙** | A(B+C)=AB+AC | A+(BC)=(A+B)(A+C) | 이중 분배 |
| **보수** | -A (음수) | A' (반대값) | NOT 연산 |
| **멱등성** | A+A=2A | A+A=A | 흡수됨 |
| **흡수 법칙** | 없음 | A+AB=A | 고유 법칙 |
| **드모르간** | 없음 | (AB)'=A'+B' | 핵심 변환 |

#### SOP vs POS 형식 비교

| 항목 | SOP (Sum of Products) | POS (Product of Sums) |
|------|------------------------|------------------------|
| **형식** | 항들의 합 (OR 결합) | 인자들의 곱 (AND 결합) |
| **예시** | F = AB + CD + EF | F = (A+B)(C+D)(E+F) |
| **기본 단위** | Minterm (최소항) | Maxterm (최대항) |
| **추출 방식** | 출력 1인 행 | 출력 0인 행 |
| **구현** | AND-OR 게이트 | OR-AND 게이트 |
| **NAND 변환** | 용이 | 복잡 |
| **적용** | PLD, PAL | ROM 기반 |

#### 과목 융합 분석

| 융합 과목 | 부울 대수 연계 내용 | 시너지 효과 |
|-----------|---------------------|-------------|
| **프로그래밍** | if조건, 논리 연산자(&&, ||, !) | 조건문 최적화, 비트 연산 |
| **데이터베이스** | SQL WHERE절, 불린 검색 | 쿼리 최적화, 인덱스 활용 |
| **네트워크** | 패킷 필터링, ACL, 방화벽 규칙 | 규칙 최적화, 중복 제거 |
| **알고리즘** | 비트마스크, 상태 압축, DP | 메모리 절약, 연산 속도 |
| **AI/ML** | 결정 트리, 규칙 기반 시스템 | 해석 가능한 모델 |
| **컴파일러** | 조건부 점프 최적화, 데드 코드 제거 | 코드 크기 감소 |

---

### IV. 실무 적용 및 기술사적 판단

#### 실무 시나리오

**시나리오 1: ALU 비교기 설계에서 부울 간소화**
```
요구사항: 4비트 비교기(Equal detector) 설계

원래 식:
F = (A3⊙B3)*(A2⊙B2)*(A1⊙B1)*(A0⊙B0)
  = (A3'B3'+A3B3)*(A2'B2'+A2B2)*(A1'B1'+A1B1)*(A0'B0'+A0B0)

각 XNOR 게이트 분해:
- XNOR = NOT(XOR) = (AB + A'B')
- 4개 XNOR * 각 5게이트 = 20게이트
- 3개 AND = 3게이트
- 총 23게이트

간소화: XOR 성질 활용
F = (A3⊕B3)'*(A2⊕B2)'*(A1⊕B1)'*(A0⊕B0)'
  = NOR(A3⊕B3, A2⊕B2, A1⊕B1, A0⊕B0)

간소화 후 게이트 수:
- 4개 XOR * 각 4게이트 = 16게이트
- 1개 4입력 NOR = 2게이트
- 총 18게이트
게이트 절감: 22%
```

**시나리오 2: 상태 머신 다음 상태 논리 최적화**
```
문제: 8상태 FSM의 다음 상태 논리 간소화

원래 식: S_next = f(S_current, inputs) - 42개의 product term
- 8개 상태 (3비트) + 5개 입력 = 8개 변수
- PLD 리소스 부족 문제

Espresso 알고리즘 적용:
1. 진리표 생성 (256행)
2. Prime Implicant 도출
3. Essential PI 선택
4. 간소화 결과: 18개 product term

효과:
- PLD/CPLD 리소스 57% 절감
- 전력 소모 40% 감소
- 타이밍 여유 2ns 개선 (경로 감소)
- 발열 문제 해결
```

**시나리오 3: 검색 엔진 필터링 쿼리 최적화**
```
요구사항: 전자상거래 상품 필터링 로직 최적화

원래 쿼리 (비효율적):
WHERE (category='A' AND price<100) OR
      (category='A' AND price>=100 AND rating>4) OR
      (category='B' AND price<50)

부울 대수 간소화:
1. category='A'로 묶기:
   category='A' AND (price<100 OR (price>=100 AND rating>4))

2. 흡수 법칙 적용:
   price<100 OR (price>=100 AND rating>4)
   = (price<100 OR price>=100) AND (price<100 OR rating>4)
   = TRUE AND (price<100 OR rating>4)
   = price<100 OR rating>4

개선된 쿼리:
WHERE (category='A' AND (price<100 OR rating>4))
   OR (category='B' AND price<50)

효과:
- 쿼리 실행 시간 60% 단축
- 인덱스 활용률 40% 향상
- DB 서버 부하 35% 감소
```

#### 도입 시 고려사항 체크리스트

```
[설계 관련]
  □ 모든 입력 조합에 대한 진리표 작성 여부
  □ Don't care 조건 식별 및 활용
  □ 최소화 도구 선택 (카르노 맵, Espresso, Q-M)
  □ 다중 출력 함수 간 공통 항 활용

[구현 관련]
  □ 게이트 수 제약 확인 (FPGA LE, ASIC 면적)
  □ 지연 시간 제약 (Critical path 분석)
  □ 팬아웃 제약 확인
  □ 입력/출력 버퍼링 필요성

[검증 관련]
  □ 시뮬레이션으로 모든 조합 테스트
  □ 형식 검증 (Formal Verification)
  □ 정적 타이밍 분석
  □ 글리치(Hazard) 발생 가능성 검토

[유지보수 관련]
  □ 문서화 (진리표, 카르노 맵, 간소화 과정)
  □ 설계 의도 명확히 기록
  □ 변경 시 재검증 프로세스
```

#### 안티패턴 및 주의사항

```
[Anti-pattern 1] "무조건 간소화하면 좋다"
   → 지연 시간이 증가할 수 있음 (단계 증가)
   → 게이트 수 vs 단계 수 트레이드오프 고려
   → Critical path는 간소화하지 않는 전략 필요

[Anti-pattern 2] "진리표 없이 직접 코딩"
   → 누락된 조건 발생 가능
   → 체계적 접근 필수
   → Karnaugh Map으로 시각화 권장

[Anti-pattern 3] "Don't care를 무시"
   → 최적화 기회 손실
   → Hazard 발생 가능
   → Static/Mynamic Hazard 검토 필요

[Anti-pattern 4] "단일 게이트 타입 고집"
   → NAND만 사용 등 과도한 제약
   → 적절한 게이트 조합이 더 효율적
   → Technology Mapping 단계에서 최적화

[Anti-pattern 5] "CAD 도구 맹신"
   → 도구도 완벽하지 않음
   → 결과 검증 필요
   → 휴리스틱 알고리즘의 한계 이해
```

---

### V. 기대효과 및 결론

#### 정량적/정성적 기대효과

| 구분 | 간소화 전 | 간소화 후 | 개선 효과 |
|------|-----------|-----------|-----------|
| 게이트 수 | 100개 | 60개 | 40% 감소 |
| 회로 지연 | 10ns | 7ns | 30% 단축 |
| 전력 소모 | 100mW | 60mW | 40% 감소 |
| 칩 면적 | 1mm^2 | 0.6mm^2 | 40% 절감 |
| 설계 시간 | 2주 | 1주 | 50% 단축 |
| 검증 케이스 | 256개 | 60개 | 77% 감소 |

#### 미래 전망

1. **AI 기반 논리 합성**
   - 머신러닝으로 최적 간소화 탐색
   - Reinforcement Learning 활용
   - 자동 HDL 코드 생성

2. **양자 부울 대수**
   - 양자 게이트 설계를 위한 확장
   - Toffoli, CNOT 게이트 등
   - 양자 회로 최적화

3. **가역 논리 (Reversible Logic)**
   - 저전력 회로를 위한 가역 게이트
   - 열 손실 없는 연산 (Landauer 한계 극복)
   - 양자 컴퓨팅과의 연계

4. **삼진 논리 (Ternary Logic)**
   - 0, 1, 2 세 가지 값
   - 정보 밀도 향상
   - Balanced Ternary 시스템

#### 참고 표준/가이드

- **IEEE 1076**: VHDL Language Reference Manual
- **IEEE 1364**: Verilog HDL Standard
- **IEEE 1800**: SystemVerilog Standard
- **IEC 61131-3**: PLC Programming Languages (LD, FBD, ST)
- **IEEE 1164**: Multi-valued Logic System (std_logic)

---

### 관련 개념 맵 (Knowledge Graph)

- [23. 드모르간의 법칙](./23_de_morgans_law.md) - 부울 대수의 핵심 변환 법칙, NAND/NOR 변환 기반
- [24. 진리표](./24_truth_table.md) - 부울 함수의 입력-출력 매핑을 표로 표현
- [25. 카르노 맵](./25_karnaugh_map.md) - 부울 함수 시각적 간소화 도구, 2차원 그리드
- [27. 논리 게이트](./27_logic_gates.md) - 부울 연산의 물리적 구현, AND/OR/NOT 게이트
- [26. 최소항과 최대항](./26_minterm.md) - 부울 함수의 표준형 기본 단위
- [69. FPGA](./69_fpga.md) - 부울 함수를 하드웨어로 구현하는 프로그래밍 가능 플랫폼

---

### 어린이를 위한 3줄 비유 설명

**부울 대수는 "예/아니요 놀이의 규칙"과 같아요!**

1. 부울 대수에서는 모든 질문이 "예(1)" 또는 "아니요(0)"로만 대답해요. "비가 오고(AND) 날이 흐리면" 두 가지가 모두 예일 때만 예라고 하죠! 이렇게 간단한 규칙들이 모여서 복잡한 것도 표현할 수 있어요.

2. "점심을 먹었거나(OR) 간식을 먹었으면 배부르다"에서는 둘 중 하나만 예여도 배부르다고 해요. 이런 규칙들을 조합하면 엄청나게 복잡한 결정도 할 수 있답니다!

3. 컴퓨터는 수십억 개의 스위치로 이루어져 있어요. 각 스위치는 켜짐(1)과 꺼짐(0)만 알지만, 부울 대수로 이들을 조합하면 게임도 하고 영화도 보고 인터넷도 할 수 있는 마법이 일어나요!
