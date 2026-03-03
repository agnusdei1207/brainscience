+++
title = "동적 프로그래밍 (Dynamic Programming)"
date = 2026-03-03

[extra]
categories = "pe_exam-algorithm_stats"
+++

<!-- 목차 -->
<!-- Ⅰ. 개요 -->
<!-- Ⅱ. 구성 요소 및 핵심 원리 -->
<!-- Ⅲ. 기술 비교 분석 -->
<!-- Ⅳ. 실무 적용 방안 -->
<!-- Ⅴ. 기대 효과 및 결론 -->
<!-- 어린이를 위한 종합 설명 -->

# 동적 프로그래밍 (Dynamic Programming)

## 핵심 인사이트 (3줄 요약)
> **동적 프로그래밍(DP)**은 중복되는 부분 문제를 메모이제이션하여 지수 시간을 다항 시간으로 최적화하는 알고리즘 설계 기법이다. **최적 부분 구조**와 **중복 부분 문제**가 필요조건이며, Top-Down(재귀+캐시)과 Bottom-Up(반복문) 두 방식이 있다. LCS, 배낭 문제, LIS가 기술사 시험 핵심 유형이다.

---

### Ⅰ. 개요

**개념**: 동적 프로그래밍(Dynamic Programming, DP)은 **복잡한 문제를 겹치는 부분 문제(Overlapping Subproblems)로 분해하고, 각 부분 문제의 결과를 저장·재사용(Memoization)하여 전체 최적해를 효율적으로 구하는 알고리즘 설계 기법**이다.

> 💡 **비유**: "피보나치 수열 계산" — 매번 처음부터 계산하지 말고, 이미 계산한 값은 적어두고 재사용!

**등장 배경**:
1. **기존 문제점**: 순수 재귀로 피보나치 계산 시 O(2^n) — fib(50)은 우주 나이보다 오래 걸림
2. **기술적 필요성**: 최적화 문제에서 중복 계산 제거로 지수 시간 → 다항 시간 단축
3. **시장/산업 요구**: git diff(LCS), 로그 분석(편집 거리), 포트폴리오 최적화(배낭) 등 실무 적용

**핵심 목적**: 중복 계산 제거를 통한 알고리즘 효율화

---

### Ⅱ. 구성 요소 및 핵심 원리

**DP 적용 조건**:
| 조건 | 설명 | 예시 |
|------|------|------|
| **최적 부분 구조** | 전체 최적해가 부분 최적해로 구성됨 | 최단 경로 = min(A→B→C, A→D→C) |
| **중복 부분 문제** | 동일 부분 문제가 반복 등장 | fib(5) = fib(4) + fib(3), fib(3) 중복 |

**구조 다이어그램**:
```
    Top-Down (메모이제이션)           Bottom-Up (타뷸레이션)
    ┌─────────────────────────────┐   ┌─────────────────────────────┐
    │  문제                       │   │  기저 사례                  │
    │    ↓ 재귀 호출              │   │  dp[0], dp[1]...            │
    │  부분 문제                   │   │    ↓ 반복문                 │
    │    ↓ 또 재귀                 │   │  dp[2] = dp[0] + dp[1]      │
    │  캐시 확인 → 있으면 반환      │   │    ↓ 계속                   │
    │  없으면 계산 후 캐시 저장     │   │  dp[3] = dp[1] + dp[2]      │
    │    ↓                        │   │    ↓                        │
    │  최종 결과                   │   │  최종 결과 dp[n]            │
    └─────────────────────────────┘   └─────────────────────────────┘

    피보나치 호출 트리 (중복 계산 시각화)
    ┌─────────────────────────────────────────────────────────────┐
    │                         fib(5)                              │
    │                        /      \                             │
    │                   fib(4)      fib(3)                        │
    │                  /     \      /     \                       │
    │              fib(3)  fib(2) fib(2)  fib(1)                  │
    │              /    \   /   \   ↓       │                     │
    │          fib(2) fib(1) ↓   ↑  중복!   │                     │
    │           /   \    │   중복!          │                     │
    │       fib(1) fib(0)│                 │                     │
    │                                                             │
    │  fib(3) 2번, fib(2) 3번 중복 계산 → O(2^n)                 │
    │  DP 적용 시 각 값 한 번만 계산 → O(n)                       │
    └─────────────────────────────────────────────────────────────┘

    LCS DP 테이블 구성
    ┌─────────────────────────────────────────────────────────────┐
    │      ""   B   D   C   A   B   (Y)                          │
    │  "" [ 0   0   0   0   0   0 ]                               │
    │  A  [ 0   0   0   0   1   1 ]                               │
    │  B  [ 0   1   1   1   1   2 ]  ← LCS = 2                   │
    │  C  [ 0   1   1   2   2   2 ]  ← LCS = 2                   │
    │  B  [ 0   1   1   2   2   3 ]  ← LCS = 3                   │
    │  D  [ 0   1   2   2   2   3 ]  ← LCS = 3                   │
    │  A  [ 0   1   2   2   3   3 ]  ← LCS = 3                   │
    │  B  [ 0   1   2   2   3   4 ]  ← LCS = 4 ✓                 │
    │  (X)                                                        │
    │                                                             │
    │  점화식:                                                    │
    │    if X[i]==Y[j]: dp[i][j] = dp[i-1][j-1] + 1              │
    │    else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])             │
    └─────────────────────────────────────────────────────────────┘
```

**동작 원리**:
```
① 문제 분해 → ② 부분 문제 식별 → ③ 기저 사례 정의 → ④ 점화식 도출 → ⑤ 순서대로 계산 → ⑥ 최적해 도출
```

**핵심 알고리즘/공식**:
```
LCS (최장 공통 부분수열):
  dp[i][j] = {
    dp[i-1][j-1] + 1,          if X[i] == Y[j]
    max(dp[i-1][j], dp[i][j-1]), otherwise
  }
  시간: O(mn), 공간: O(mn) → O(n) 최적화 가능

0-1 배낭 (Knapsack):
  dp[i][w] = max(
    dp[i-1][w],                  # i번째 물건 안 넣음
    dp[i-1][w-weight[i]] + value[i]  # i번째 물건 넣음
  ) if weight[i] <= w
  시간: O(nW), 공간: O(nW) → O(W) 최적화 가능

LIS (최장 증가 부분수열):
  O(n²): dp[i] = max(dp[j] + 1) for all j < i and arr[j] < arr[i]
  O(n log n): 이진탐색으로 tails 배열 관리
```

**코드 예시 (Python)**:
```python
"""
동적 프로그래밍 핵심 알고리즘 구현
- 피보나치 (Top-Down vs Bottom-Up)
- LCS (최장 공통 부분수열)
- 0-1 배낭 문제
- LIS (최장 증가 부분수열)
- 편집 거리 (Levenshtein Distance)
"""
from typing import List, Tuple, Optional
from functools import lru_cache
import bisect


# ============== 피보나치 ==============

def fib_recursive(n: int) -> int:
    """순수 재귀 - O(2^n) - 매우 느림!"""
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_memoization(n: int, memo: dict = None) -> int:
    """
    Top-Down (메모이제이션) - O(n)
    재귀 + 캐시
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memoization(n - 1, memo) + fib_memoization(n - 2, memo)
    return memo[n]


def fib_tabulation(n: int) -> int:
    """
    Bottom-Up (타뷸레이션) - O(n)
    반복문 + 테이블
    """
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def fib_optimized(n: int) -> int:
    """공간 최적화 - O(n) 시간, O(1) 공간"""
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


# ============== LCS ==============

def lcs_length(X: str, Y: str) -> int:
    """LCS 길이만 계산 - O(mn)"""
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def lcs_string(X: str, Y: str) -> Tuple[str, int]:
    """
    LCS 문자열과 길이 반환
    역추적 포함
    """
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # DP 테이블 채우기
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 역추적로 실제 문자열 복원
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs_chars.append(X[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(lcs_chars)), dp[m][n]


def lcs_optimized(X: str, Y: str) -> int:
    """공간 최적화 LCS - O(n) 공간"""
    m, n = len(X), len(Y)
    # 이전 행만 유지
    prev = [0] * (n + 1)

    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr

    return prev[n]


# ============== 0-1 배낭 문제 ==============

def knapsack_01(weights: List[int], values: List[int], W: int) -> int:
    """
    0-1 배낭 문제 - O(nW)
    각 물건을 한 번만 넣을 수 있음
    """
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            # i번째 물건 안 넣음
            dp[i][w] = dp[i - 1][w]
            # i번째 물건 넣음 (무게 가능 시)
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])

    return dp[n][W]


def knapsack_01_optimized(weights: List[int], values: List[int], W: int) -> int:
    """공간 최적화 0-1 배낭 - O(W) 공간"""
    n = len(weights)
    dp = [0] * (W + 1)

    # 뒤에서부터 업데이트 (중복 선택 방지)
    for i in range(n):
        for w in range(W, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[W]


def knapsack_items(weights: List[int], values: List[int], W: int) -> Tuple[int, List[int]]:
    """선택한 물건 인덱스도 반환"""
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])

    # 선택한 물건 역추적
    items = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            items.append(i - 1)
            w -= weights[i - 1]

    return dp[n][W], items[::-1]


# ============== LIS ==============

def lis_n2(arr: List[int]) -> int:
    """
    LIS 길이 - O(n²)
    dp[i] = arr[i]로 끝나는 LIS 길이
    """
    n = len(arr)
    if n == 0:
        return 0

    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def lis_nlogn(arr: List[int]) -> int:
    """
    LIS 길이 - O(n log n)
    이진 탐색 활용
    tails[i] = 길이 i+1인 LIS의 마지막 원소 최솟값
    """
    tails = []
    for x in arr:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


def lis_sequence(arr: List[int]) -> List[int]:
    """LIS 실제 수열 반환 - O(n log n)"""
    n = len(arr)
    if n == 0:
        return []

    tails = []
    tails_idx = []  # tails의 각 위치에 해당하는 arr 인덱스
    prev_idx = [-1] * n  # 각 원소의 이전 원소 인덱스

    for i, x in enumerate(arr):
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[pos] = x
            tails_idx[pos] = i

        if pos > 0:
            prev_idx[i] = tails_idx[pos - 1]

    # 역추적
    result = []
    curr = tails_idx[-1]
    while curr != -1:
        result.append(arr[curr])
        curr = prev_idx[curr]

    return result[::-1]


# ============== 편집 거리 ==============

def edit_distance(word1: str, word2: str) -> int:
    """
    편집 거리 (Levenshtein Distance) - O(mn)
    삽입, 삭제, 교체 연산
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 기저 사례
    for i in range(m + 1):
        dp[i][0] = i  # 삭제만
    for j in range(n + 1):
        dp[0][j] = j  # 삽입만

    # DP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # 같음
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,     # 삭제
                    dp[i][j - 1] + 1,     # 삽입
                    dp[i - 1][j - 1] + 1  # 교체
                )

    return dp[m][n]


# ============== 실행 예시 ==============

if __name__ == "__main__":
    print("=" * 60)
    print(" 동적 프로그래밍 (Dynamic Programming)")
    print("=" * 60)

    # 피보나치
    print("\n[피보나치]")
    n = 30
    print(f"  fib({n}) 메모이제이션: {fib_memoization(n)}")
    print(f"  fib({n}) 타뷸레이션: {fib_tabulation(n)}")
    print(f"  fib({n}) 최적화: {fib_optimized(n)}")

    # LCS
    print("\n[LCS]")
    X, Y = "ABCBDAB", "BDCAB"
    lcs_str, lcs_len = lcs_string(X, Y)
    print(f"  X: {X}")
    print(f"  Y: {Y}")
    print(f"  LCS: '{lcs_str}' (길이: {lcs_len})")

    # 배낭
    print("\n[0-1 배낭]")
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    W = 5
    max_val, items = knapsack_items(weights, values, W)
    print(f"  무게: {weights}")
    print(f"  가치: {values}")
    print(f"  용량: {W}")
    print(f"  최대 가치: {max_val}")
    print(f"  선택 물건: {items}")

    # LIS
    print("\n[LIS]")
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"  배열: {arr}")
    print(f"  LIS 길이 O(n²): {lis_n2(arr)}")
    print(f"  LIS 길이 O(n log n): {lis_nlogn(arr)}")
    print(f"  LIS 수열: {lis_sequence(arr)}")

    # 편집 거리
    print("\n[편집 거리]")
    w1, w2 = "kitten", "sitting"
    print(f"  '{w1}' → '{w2}': {edit_distance(w1, w2)}")


print("\n" + "=" * 60)
print(" Top-Down vs Bottom-Up 비교")
print("=" * 60)
print("""
┌─────────────────┬──────────────────┬────────────────────┐
│      항목        │   Top-Down       │     Bottom-Up      │
├─────────────────┼──────────────────┼────────────────────┤
│ 접근 방향       │ 큰 문제 → 작은    │ 작은 문제 → 큰     │
│ 구현 방식       │ 재귀 + 캐시       │ 반복문 + 테이블    │
│ 필요한 계산     │ 필요한 것만       │ 모든 부분 문제     │
│ 스택 오버플로   │ 위험 (재귀 깊이)  │ ★ 안전             │
│ 코드 직관성     │ ★ 직관적          │ 명시적 상태 전이   │
│ 실무 선호       │ 제한적            │ ★ 대부분           │
└─────────────────┴──────────────────┴────────────────────┘
""")

---

### Ⅲ. 기술 비교 분석

**장단점 분석**:
| 장점 (DP) | 단점 (DP) |
|----------|----------|
| 지수 시간 → 다항 시간 단축 | 점화식 도출이 어려움 |
| 최적해 보장 | 공간 복잡도 증가 가능 |
| 중복 계산 완전 제거 | 모든 부분 문제 해결 필요 |
| 구조적 문제 해결 | 문제마다 다른 접근 필요 |

**DP vs 탐욕 vs 분할정복 비교**:
| 비교 항목 | 완전 탐색 | 분할 정복 | 탐욕 (Greedy) | ★ DP |
|---------|----------|----------|-------------|------|
| 중복 계산 | ★★ 많음 | 없음 | 없음 | ★ 저장·재사용 |
| 최적해 보장 | ★ 보장 | ★ 보장 | 비보장 | ★ 보장 |
| 시간 복잡도 | O(2^n)~O(n!) | O(n log n) | ★ O(n) | O(n²)~O(nW) |
| 적용 조건 | 제약 없음 | 독립 부분문제 | 탐욕 선택 성질 | 최적 부분구조+중복 |
| 대표 예시 | 순열·조합 | 병합정렬, FFT | 크루스칼, 다익스트라 | ★ LCS, 배낭, LIS |

> **★ 선택 기준**: 최적해 보장 필요 + 부분 문제 중복 → DP, 탐욕 선택 성질 만족 → Greedy

**기술 진화 계보**:
```
완전 탐색 → 분할 정복 → DP(1950s) → 메모이제이션 최적화 → tabulation → 공간 최적화
```

---

### Ⅳ. 실무 적용 방안

**기술사적 판단**:
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **git diff** | LCS로 파일 차이 계산 | diff 속도 10배 향상 |
| **맞춤법 검사** | 편집 거리로 오타 교정 | 교정 정확도 95% |
| **물류 최적화** | 배낭 문제로 적재 최적화 | 비용 20% 절감 |
| **DNA 분석** | LCS/편집거리로 서열 비교 | 분석 시간 100배 단축 |
| **금융 포트폴리오** | 배낭 변형으로 자산 배분 | 수익률 15% 향상 |

**실제 도입 사례**:
- **Git**: LCS 기반 diff 알고리즘 — 파일 변경사항 최소화
- **Google**: 편집 거리로 검색어 오타 교정 — "did you mean?"
- **생물정보학**: DNA 서열 정렬 (BLAST) — 유전자 유사도 분석
- **금융**: 포트폴리오 최적화 (배낭 변형) — 위험 대비 수익 최대화

**도입 시 고려사항**:
1. **기술적**: 점화식 도출, 메모리 제약, 부분 문제 식별
2. **운영적**: 캐시 크기, 재귀 깊이 제한, 테이블 크기
3. **보안적**: 타이밍 공격 방지 (상수 시간 구현)
4. **경제적**: 공간 vs 시간 트레이드오프

**주의사항 / 흔한 실수**:
- ❌ 부분 문제 식별 실패로 DP 미적용
- ❌ 점화식 오류로 잘못된 최적해
- ❌ 메모리 초과 (공간 최적화 미적용)
- ❌ 재귀 깊이 초과 (Bottom-Up 필요)

**관련 개념 / 확장 학습**:
```
📌 DP 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  DP 핵심 연관 개념 맵                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [분할 정복] ←──────→ [DP] ←──────→ [탐욕 알고리즘]            │
│        ↓               ↓                 ↓                      │
│   [재귀]          [메모이제이션]      [최적 선택]                │
│        ↓               ↓                 ↓                      │
│   [백트래킹]       [LCS/배낭/LIS]    [다익스트라]                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 분할 정복 | 선행 개념 | DP의 기반 | `[divide_conquer](./divide_conquer.md)` |
| 탐욕 알고리즘 | 대안 기법 | 더 빠르지만 조건 엄격 | `[greedy](./greedy.md)` |
| 그래프 | 응용 분야 | 최단 경로 (플로이드) | `[shortest_path](./shortest_path.md)` |
| 백트래킹 | 관련 기법 | DP + 가지치기 | `[backtracking](./backtracking.md)` |
| 메모이제이션 | 핵심 기술 | 결과 캐싱 | — |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과**:
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 시간 단축 | 지수 → 다항 시간 | O(2^n) → O(n²) |
| 최적해 보장 | 항상 최적 | 100% 정확도 |
| 메모리 효율 | 공간 최적화 | O(n)으로 축소 |

**미래 전망**:
1. **기술 발전 방향**: 자동 DP 도출, ML 기반 최적화
2. **시장 트렌드**: 실시간 최적화, 스트리밍 DP
3. **후속 기술**: Approximate DP, Online DP

> **결론**: 동적 프로그래밍은 중복 계산 제거를 통한 최적화의 핵심 기법으로, 최적 부분 구조와 중복 부분 문제의 식별이 핵심이다. LCS, 배낭, LIS는 기술사 시험의 단골 유형이며, Top-Down과 Bottom-Up의 장단점을 이해하고 상황에 맞게 선택하는 능력이 필수다.

> **※ 참고 표준**: CLRS 'Introduction to Algorithms' Ch.15, T. H. Cormen, LeetCode DP Patterns

---

## 어린이를 위한 종합 설명

**동적 프로그래밍은 "메모하면서 풀기"야!**

```
상상해보세요:
  피보나치 수열을 계산해야 해요!
  1, 1, 2, 3, 5, 8, 13, 21...

  ❌ 매번 처음부터 계산하기:
    "8을 구하려면... 5+3... 5를 구하려면... 3+2..."
    "3을 또 구하려면... 2+1..." → 3을 두 번 계산했어! 😫

  ✅ 이미 계산한 건 적어두기:
    "3 = 2+1, 적어놓자!" 📝
    "또 3이 필요하면? 적어둔 거 보자!" → 1초 만에 끝! 😊
```

**배낭 문제 (가방에 물건 넣기)**:
```
가방에 물건을 넣어요 (무게 5kg 제한):

  🍎 사과 (2kg, 3만원)
  🍌 바나나 (3kg, 4만원)
  🍊 오렌지 (4kg, 5만원)
  🍇 포도 (5kg, 6만원)

  어떤 걸 넣어야 가장 비싸게 담을까요?

  DP 방식:
    ① 무게 1부터 시작: 아무것도 못 넣어
    ② 무게 2: 사과(3만원) 넣을 수 있어!
    ③ 무게 3: 사과+바나나(7만원)!
    ④ 무게 4: 오렌지 vs 사과+바나나? → 7만원이 더 커!
    ⑤ 무게 5: 포도(6만원) vs 사과+바나나(7만원)? → 7만원!

  정답: 사과+바나나 = 7만원! 💰
```

**LCS (공통으로 긴 순서 찾기)**:
```
내 쇼핑 목록: 🍎 → 🍌 → 🍊 → 🍇
친구 목록:   🍌 → 🍇 → 🍎 → 🍊

둘 다 있는 순서대로 된 건?
  🍌 → 🍊 (길이 2) ✓
  🍎 → 🍊 (길이 2) ✓

  DP로 표를 만들어서 구해요! 📊
```

**비밀**: 어려운 문제를 작은 문제로 쪼개서, 한 번 푼 건 다시 안 풀기! 🧩✨
