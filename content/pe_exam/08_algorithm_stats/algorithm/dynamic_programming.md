+++
title = "동적 프로그래밍 유형별 완전 정리 (Dynamic Programming Patterns)"
date = 2026-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 동적 프로그래밍 유형별 완전 정리 (Dynamic Programming Patterns)

## 핵심 인사이트 (3줄 요약)
> **중복 부분 문제를 메모이제이션하거나 테이블로 해결하는 최적화 기법**. 최적 부분 구조와 중복 부분 문제가 존재해야 적용 가능. 기술사 시험에서 LCS·배낭·최장증가수열(LIS) 유형이 핵심이다.

## 1. 개념과 조건

```
동적 프로그래밍 적용 조건 (2가지 모두 필요):

1. 최적 부분 구조 (Optimal Substructure):
   전체 최적해가 부분 최적해로 구성됨
   예: 최단경로 A→C = min(A→B + B→C, A→D + D→C)

2. 중복 부분 문제 (Overlapping Subproblems):
   같은 부분 문제가 반복 등장
   예: 피보나치 fib(5) = fib(4) + fib(3)
              fib(4) = fib(3) + fib(2)'  ← fib(3) 중복!
```

## 2. Top-Down vs Bottom-Up 비교

```
Top-Down (메모이제이션):     Bottom-Up (타뷸레이션):
━━━━━━━━━━━━━━━━━━━━━━       ━━━━━━━━━━━━━━━━━━━━━━
재귀 + 캐시                  반복문 + 테이블
큰 문제 → 작은 문제          작은 문제 → 큰 문제
직관적, 스택오버플로우        빠름, 공간 최적화 가능
필요한 것만 계산             모두 계산

피보나치 예시:
Top-Down:                    Bottom-Up:
def fib(n, memo={}):         def fib(n):
  if n in memo:                dp = [0] * (n+1)
    return memo[n]             dp[1] = 1
  if n <= 1: return n          for i in range(2, n+1):
  memo[n] = fib(n-1,memo)        dp[i] = dp[i-1] + dp[i-2]
           + fib(n-2,memo)     return dp[n]
  return memo[n]
```

## 3. 핵심 DP 유형별 완전 정리

### 유형 1: LCS (Longest Common Subsequence - 최장 공통 부분수열)

```
입력: X = "ABCBDAB", Y = "BDCAB"
출력: LCS = "BCAB" 또는 "BDAB" (길이 4)

알고리즘:
if X[i] == Y[j]: dp[i][j] = dp[i-1][j-1] + 1
else:             dp[i][j] = max(dp[i-1][j], dp[i][j-1])

dp 테이블:
    ""  B  D  C  A  B
""  [0  0  0  0  0  0]
A   [0  0  0  0 ①1  1]
B   [0 ②1  1  1  1 ③2]
C   [0  1  1 ④2  2  2]
B   [0  1  1  2  2 ⑤3]
D   [0  1 ⑥2  2  2  3]
A   [0  1  2  2 ⑦3  3]
B   [0  1  2  2  3 ⑧4]

시간복잡도: O(mn)
공간복잡도: O(mn) → O(n) 최적화 가능 (1행씩만 유지)
```

```python
def lcs(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n+1) for _ in range(m+1)]
    
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # 역추적 (실제 문자열 복원)
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            result.append(X[i-1])
            i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(result)), dp[m][n]

X, Y = "ABCBDAB", "BDCAB"
seq, length = lcs(X, Y)
print(f"LCS: {seq}, 길이: {length}")  # BCAB, 4
```

---

### 유형 2: 0/1 배낭 문제 (0/1 Knapsack)

```
입력: 물건 n개, 각각 무게(w)·가치(v), 배낭 용량 W
출력: 배낭에 넣을 수 있는 최대 가치

물건: [(무게2,가치3), (무게3,가치4), (무게4,가치5), (무게5,가치6)]
W=5

점화식:
if w[i] > j:  dp[i][j] = dp[i-1][j]  # 못 넣음
else:         dp[i][j] = max(dp[i-1][j],       # 안 넣음
                             dp[i-1][j-w[i]] + v[i])  # 넣음

dp 테이블 (행=물건, 열=용량):
        0  1  2  3  4  5
없음    [0  0  0  0  0  0]
(2,3)  [0  0  3  3  3  3]
(3,4)  [0  0  3  4  4  7]  ← 무게2+무게3=가치3+4=7
(4,5)  [0  0  3  4  5  7]
(5,6)  [0  0  3  4  5  7]  ← W=5에 무게5짜리 가치6보다 7이 큼

최대 가치: 7
```

```python
def knapsack_01(weights, values, W):
    n = len(weights)
    dp = [[0] * (W+1) for _ in range(n+1)]
    
    for i in range(1, n+1):
        for j in range(W+1):
            dp[i][j] = dp[i-1][j]  # 기본: 안 넣음
            if weights[i-1] <= j:
                dp[i][j] = max(dp[i][j],
                               dp[i-1][j - weights[i-1]] + values[i-1])
    
    # 공간 최적화: 1D dp (뒤에서 앞으로 채우기)
    dp1d = [0] * (W+1)
    for i in range(n):
        for j in range(W, weights[i]-1, -1):  # 역순!
            dp1d[j] = max(dp1d[j], dp1d[j - weights[i]] + values[i])
    
    return dp[n][W], dp1d[W]

w = [2, 3, 4, 5]
v = [3, 4, 5, 6]
max_val, max_val_1d = knapsack_01(w, v, 5)
print(f"최대 가치: {max_val}")  # 7
```

---

### 유형 3: LIS (Longest Increasing Subsequence - 최장 증가 부분수열)

```
입력: [10, 9, 2, 5, 3, 7, 101, 18]
출력: LIS 길이 = 4 ([2, 3, 7, 101] 또는 [2, 5, 7, 101])

O(n²) DP:
dp[i] = A[i]로 끝나는 LIS 길이

  i:    0   1   2   3   4   5   6    7
A[i]: [10,  9,  2,  5,  3,  7, 101, 18]
dp:   [ 1,  1,  1,  2,  2,  3,  4,  4]

for i in range(n):
    for j in range(i):
        if A[j] < A[i]:
            dp[i] = max(dp[i], dp[j] + 1)

O(n log n) 이진탐색 최적화:
tails 배열 유지: 각 길이의 LIS 마지막 원소 최솟값
  10        → [10]
   9        → [9]
   2        → [2]
   5        → [2, 5]
   3        → [2, 3]
   7        → [2, 3, 7]
 101        → [2, 3, 7, 101]
  18        → [2, 3, 7, 18]  ← 이진탐색으로 101 위치에 18 교체
LIS 길이 = len(tails) = 4
```

```python
import bisect

def lis_n2(arr):
    n = len(arr)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

def lis_nlogn(arr):
    tails = []
    for x in arr:
        pos = bisect.bisect_left(tails, x)  # 이진탐색
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)

arr = [10, 9, 2, 5, 3, 7, 101, 18]
print(f"LIS (O(n²)): {lis_n2(arr)}")       # 4
print(f"LIS (O(n log n)): {lis_nlogn(arr)}") # 4
```

## 4. DP 유형 비교표

| 유형 | 상태 정의 | 점화식 핵심 | 복잡도 | 응용 |
|------|---------|-----------|--------|------|
| **LCS** | dp[i][j] = X[0..i], Y[0..j] LCS 길이 | 문자 같으면 +1 | O(mn) | 문서 비교, git diff |
| **배낭** | dp[i][j] = 물건i까지 용량j일 때 최대값 | 넣기 vs 안넣기 | O(nW) | 투자 최적화, 자원 배분 |
| **LIS** | dp[i] = arr[i]로 끝나는 LIS 길이 | 이전보다 크면 +1 | O(n²)/O(n log n) | 주가 분석, 패킷 정렬 |
| **편집거리** | dp[i][j] = X[i]→Y[j] 최소 연산 수 | 삽입·삭제·교체 | O(mn) | 맞춤법 검사 |
| **동전** | dp[i] = 금액i 만들 최소 동전 수 | dp[i] = min(dp[i-c]+1) | O(nW) | 거스름돈, 수익 최대화 |
| **행렬곱** | dp[i][j] = 행렬i..j 곱 최소 연산 | 분할점 k 탐색 | O(n³) | 컴파일러 최적화 |

## 5. 탐욕 vs DP 선택 기준

```
탐욕 (Greedy):                    DP:
━━━━━━━━━━━━━━━━━━━━              ━━━━━━━━━━━━━━━━━━━━
현재 최선 → 전체 최선            모든 경우 탐색 → 최적
교환 성질 필요                   최적 부분 구조 + 중복 부분
빠름: O(n log n) 內              느림: O(n²)~O(2^n)
예: 활동 선택, 거스름돈*, 다익스트라  예: 배낭, LCS, LIS

*거스름돈: 한국 동전으로는 탐욕 O, 임의 동전 시스템은 DP 필요
```

## 6. 실무에서? (기술사적 판단)
- **git diff**: LCS로 두 파일 차이 계산
- **맞춤법 검사**: 편집거리(Levenshtein Distance)
- **바이오인포매틱스**: 유전자 서열 정렬 (LCS/편집거리)
- **금융 최적화**: 포트폴리오(배낭 변형)
- **기술사 포인트**: LCS·배낭·LIS 점화식, Top-Down vs Bottom-Up

## 7. 관련 개념
- 분할 정복 (Divide & Conquer)
- 탐욕 알고리즘 (Greedy)
- 백트래킹
- 알고리즘 복잡도

---

---


## 📝 기술사 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"동적 프로그래밍(DP)의 개념과 적용 조건을 설명하고, Memoization(하향식)과 Tabulation(상향식)을 비교하여 LCS·배낭 문제에 적용 방안을 논하시오."**

---

### Ⅰ. 개요

**동적 프로그래밍(Dynamic Programming, DP)**이란 큰 문제를 **겹치는 부분 문제(Overlapping Subproblems)**로 분할하고, 각 부분 문제의 결과를 **메모이제이션(저장·재사용)**하여 전체 최적해를 효율적으로 구하는 알고리즘 설계 기법이다.

- **등장 배경**: 재귀(분할정복)로 피보나치를 계산 시 동일 부분 문제를 기하급수적으로 중복 계산 → O(2^n) → DP 적용 시 O(n)
- **핵심 목적**: 중복 계산 제거로 지수 시간 복잡도를 다항 시간으로 감소

**DP 적용 2대 조건**:
1. **최적 부분 구조 (Optimal Substructure)**: 전체 최적해 = 부분 문제 최적해 조합
2. **겹치는 부분 문제 (Overlapping Subproblems)**: 동일 부분 문제가 반복 등장

---

### Ⅱ. 구성 요소 및 핵심 원리

#### 1. Memoization(하향식) vs Tabulation(상향식) 비교

| 항목 | Memoization (Top-Down) | Tabulation (Bottom-Up) |
|-----|-------------------|--------------------|
| **접근 방향** | 큰 문제 → 작은 문제 (재귀) | 작은 문제 → 큰 문제 (반복문) |
| **구현 방식** | 재귀 + 캐시 딕셔너리 | DP 테이블 반복 채우기 |
| **필요 계산** | 필요한 부분만 계산 | 모든 부분 문제 계산 |
| **스택 오버플로** | 재귀 깊이 제한으로 위험 | ★ 안전 (반복문) |
| **코드 직관성** | ★ 직관적 (재귀 구조) | 명시적 상태 전이 필요 |
| **실무 선호** | 일부 부분 문제만 필요 시 | ★ 대부분 실무 (안전·빠름) |

#### 2. 대표 DP 유형 및 점화식

```
LCS (최장 공통 부분 수열):
  dp[i][j] = {
    dp[i-1][j-1] + 1,         if A[i] == B[j]
    max(dp[i-1][j], dp[i][j-1]), otherwise
  }
  복잡도: O(mn), 공간: O(mn)

0-1 배낭 (Knapsack):
  dp[i][w] = max(
    dp[i-1][w],                      # 물건 i 미선택
    dp[i-1][w-wi] + vi               # 물건 i 선택 (무게 허용 시)
  )
  복잡도: O(nW), 공간: O(nW) → O(W) 최적화 가능

LIS (최장 증가 부분 수열):
  dp[i] = max(dp[j] + 1) for j < i and arr[j] < arr[i]
  기본: O(n²) / 이진탐색 최적화: O(n log n)
```

---

### Ⅲ. 기술 비교 분석: DP vs 유사 기법

| 항목 | 완전 탐색 | 분할정복 | 탐욕(Greedy) | 동적 프로그래밍 |
|-----|---------|---------|------------|----------------|
| **중복 계산** | ★★ 매우 많음 | 없음 (독립 부분문제) | 없음 | ★ 저장·재사용 |
| **최적해 보장** | ★ 보장 | ★ 보장 | 비보장 (일부만) | ★ 보장 |
| **시간 복잡도** | O(2^n)~O(n!) | O(n log n) | O(n) | O(n²)~O(nW) |
| **적용 조건** | 제약 없음 | 독립 부분문제 | 탐욕 선택 성질 | 최적 부분구조+중복 |
| **활용 예** | 순열·조합 탐색 | 병합정렬, FFT | 크루스칼, 다익스트라 | LCS, 배낭, LIS |

**★ 선택 기준**: 최적해 보장이 필요하고, 부분 문제 간 중복이 있다면 DP. 탐욕이 최적 선택 성질을 만족하면 Greedy가 DP보다 훨씬 빠름.

---

### Ⅳ. 실무 적용 방안

| 분야 | 문제 | DP 적용 |
|-----|-----|---------|
| **생물정보학** | DNA 서열 유사도 분석 | LCS로 유전자 서열 비교 |
| **물류 최적화** | 배낭 용량 내 최대 가치 화물 선적 | 0-1 배낭 문제 |
| **금융** | 주가 예측 모델 | LIS (상승 추세 탐지) |
| **NLP** | 문장 편집 거리 계산 | Edit Distance (DP 변형) |
| **게임 AI** | 상태 공간 최적 경로 탐색 | 메모이제이션 + Alpha-Beta Pruning |

---

### Ⅴ. 기대 효과 및 결론

| 효과 | 내용 | 정량 목표 |
|-----|-----|---------|
| **시간 복잡도** | 지수 → 다항 시간으로 감소 | O(2^n) → O(n²) (피보나치) |
| **알고리즘 설계** | 복잡한 최적화 문제 체계적 분해 | 개발 시간 단축 |
| **실무 확장성** | 메모이제이션으로 결과 캐싱 | 시스템 응답시간 개선 |

#### 결론
> 동적 프로그래밍은 최적화 문제 해결의 가장 강력한 도구 중 하나로, **최적 부분 구조와 겹치는 부분 문제라는 두 조건의 식별**이 핵심이다. LCS·배낭·LIS는 기술사 시험의 단골이며, 분할정복·탐욕과의 비교를 통해 문제 특성에 맞는 알고리즘 선택 능력이 요구된다.

> **※ 참고**: T. H. Cormen "Introduction to Algorithms" (CLRS), LeetCode DP 문제 패턴

---


## 어린이를 위한 종합 설명

**동적 프로그래밍은 "메모하면서 풀기"야!**

```
피보나치 수열:
  1, 1, 2, 3, 5, 8, 13, 21...
  
  ❌ 매번 처음부터 계산: 느려!
  ✅ 이미 계산한 건 적어두기: 빨라!

이게 동적 프로그래밍! 📝
```

**배낭 문제:**
```
배낭에 물건 넣기 (무게 5kg 제한):
  사과(2kg, 3만원) 넣을까 말까?
  바나나(3kg, 4만원) 넣을까 말까?
  → 표 만들어서 최대 가치 찾기!
```

**LCS:**
```
내 쇼핑 목록: 사과 바나나 체리
친구 목록: 바나나 딸기 체리
공통 = "바나나 체리" (LCS!)
```

**비밀**: DP는 복잡한 문제를 작은 문제로 조개는 마법이에요! ✨
