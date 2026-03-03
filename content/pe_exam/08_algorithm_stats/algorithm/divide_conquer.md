+++
title = "분할 정복 (Divide and Conquer)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 분할 정복 (Divide and Conquer)

## 핵심 인사이트 (3줄 요약)
> **문제를 작은 부분으로 나누어 해결 후 병합하는 알고리즘 설계 기법**. 분할 → 정복 → 결합의 3단계. 병합정렬, 퀵정렬, FFT의 핵심 원리.

---

## 📝 기술사 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"분할 정복의 원리와 동작 과정을 설명하고, 유사 알고리즘과 비교하여 적합한 활용 시나리오를 기술하시오."**

---

### Ⅰ. 개요

#### 1. 개념
분할 정복(Divide and Conquer)은 **큰 문제를 여러 개의 작은 문제로 나누어 해결한 후, 그 결과를 결합하여 전체 문제를 해결하는 알고리즘 설계 기법**이다. 재귀적 구조가 핵심이며, 하위 문제는 서로 독립적이어야 한다.

> 💡 **비유**: "퍼즐 맞추기" - 큰 퍼즐을 작은 구역으로 나누어 맞춘 후 전체를 완성하는 방식

**등장 배경**:
1. **기존 문제점**: 대규모 문제를 한 번에 해결하기 어려움
2. **기술적 필요성**: 독립적인 부분 문제로 분해하여 병렬 처리 가능
3. **시장 요구**: 대용량 데이터 정렬, 신호 처리 등 고성능 연산 수요

**핵심 목적**: 문제 크기를 줄여 재귀적으로 해결, 병렬화 가능

---

### Ⅱ. 구성 요소 및 핵심 원리

#### 2. 분할 정복 핵심 구성 요소

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| 분할 (Divide) | 문제를 작은 하위 문제로 분해 | 보통 크기 1/2로 분할 | 큰 퍼즐 조각 나누기 |
| 정복 (Conquer) | 하위 문제 재귀적 해결 | 충분히 작으면 직접 해결 | 작은 퍼즐 맞추기 |
| 결합 (Combine) | 하위 해를 결합하여 전체 해 구성 | 결합 비용이 성능 결정 | 퍼즐 조각 합치기 |

#### 3. 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│               분할 정복 3단계 구조                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📌 분할 정복 일반형:                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  T(n) = aT(n/b) + f(n)                             │   │
│  │                                                     │   │
│  │  • a: 하위 문제 개수                                │   │
│  │  • b: 하위 문제 크기 비율 (보통 2)                  │   │
│  │  • f(n): 분할 + 결합 비용                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  🔄 병합 정렬 예시:                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    [38,27,43,3,9,82,10]             │   │
│  │                          ↓ 분할                     │   │
│  │              [38,27,43,3]    [9,82,10]              │   │
│  │                  ↓               ↓                  │   │
│  │            [38,27] [43,3]   [9,82] [10]             │   │
│  │              ↓       ↓       ↓      ↓               │   │
│  │           [38][27] [43][3] [9][82] [10]             │   │
│  │              ↓       ↓       ↓      ↓               │   │
│  │            [27,38] [3,43]  [9,82] [10]   ← 결합     │   │
│  │                  ↓               ↓                  │   │
│  │           [3,27,38,43]     [9,10,82]                │   │
│  │                          ↓                          │   │
│  │              [3,9,10,27,38,43,82]                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 4. 동작 원리 단계별 설명

```
① 문제 분할 → ② 재귀 호출 → ③ 기저 조건 → ④ 부분 해 결합 → ⑤ 전체 해 반환
```

- **1단계 (분할)**: 입력을 a개의 하위 문제로 분할 (크기 n/b)
- **2단계 (정복)**: 각 하위 문제를 재귀적으로 해결
- **3단계 (기저)**: 문제가 충분히 작으면 직접 해결 (재귀 종료)
- **4단계 (결합)**: 하위 해를 결합하여 상위 해 구성
- **5단계 (반환)**: 최종 전체 해 반환

#### 5. Master Theorem (마스터 정리)

| 경우 | 조건 | 시간복잡도 | 예시 |
|-----|------|-----------|------|
| 1 | f(n) < n^(log_b a) | Θ(n^(log_b a)) | T(n)=2T(n/2)+1 → Θ(n) |
| 2 | f(n) = n^(log_b a) | Θ(n^(log_b a) × log n) | T(n)=2T(n/2)+n → Θ(n log n) |
| 3 | f(n) > n^(log_b a) | Θ(f(n)) | T(n)=2T(n/2)+n² → Θ(n²) |

#### 6. Python 코드 예시

```python
from typing import List, Tuple
import random

# ==================== 병합 정렬 ====================

def merge_sort(arr: List[int]) -> List[int]:
    """
    병합 정렬 - 분할 정복의 대표 예시

    시간복잡도: O(n log n)
    공간복잡도: O(n)
    안정 정렬: Yes
    """
    # 기저 조건
    if len(arr) <= 1:
        return arr

    # 분할
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # 결합 (병합)
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """두 정렬된 리스트 병합"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ==================== 퀵 정렬 ====================

def quick_sort(arr: List[int]) -> List[int]:
    """
    퀵 정렬 - 분할 정복 + 피벗

    시간복잡도: 평균 O(n log n), 최악 O(n²)
    공간복잡도: O(log n) (재귀 스택)
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    # 분할 (피벗 기준)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # 정복 + 결합
    return quick_sort(left) + middle + quick_sort(right)


def quick_sort_inplace(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    제자리 퀵 정렬 (In-place)
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = _partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_idx - 1)
        quick_sort_inplace(arr, pivot_idx + 1, high)


def _partition(arr: List[int], low: int, high: int) -> int:
    """Lomuto 파티션 스킴"""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ==================== 이진 탐색 ====================

def binary_search(arr: List[int], target: int,
                   left: int = 0, right: int = None) -> int:
    """
    이진 탐색 - 분할 정복 기반 탐색

    시간복잡도: O(log n)
    전제 조건: 배열이 정렬되어 있어야 함
    """
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1  # 찾지 못함

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, right)
    else:
        return binary_search(arr, target, left, mid - 1)


# ==================== 최대 부분 배열 (Maximum Subarray) ====================

def max_subarray(arr: List[int]) -> Tuple[int, int, int]:
    """
    최대 부분 배열 합 - 분할 정복

    Kadane 알고리즘으로 O(n) 가능하지만,
    분할 정복으로 O(n log n)에 해결

    Returns:
        (시작 인덱스, 끝 인덱스, 최대 합)
    """
    def find_max_crossing(low: int, mid: int, high: int) -> Tuple[int, int, int]:
        """중앙을 가로지르는 최대 부분 배열"""
        # 왼쪽 최대
        left_sum = float('-inf')
        sum_val = 0
        max_left = mid

        for i in range(mid, low - 1, -1):
            sum_val += arr[i]
            if sum_val > left_sum:
                left_sum = sum_val
                max_left = i

        # 오른쪽 최대
        right_sum = float('-inf')
        sum_val = 0
        max_right = mid + 1

        for i in range(mid + 1, high + 1):
            sum_val += arr[i]
            if sum_val > right_sum:
                right_sum = sum_val
                max_right = i

        return (max_left, max_right, left_sum + right_sum)

    def divide(low: int, high: int) -> Tuple[int, int, int]:
        if low == high:
            return (low, low, arr[low])

        mid = (low + high) // 2

        # 왼쪽, 오른쪽, 가로지르는 경우
        left = divide(low, mid)
        right = divide(mid + 1, high)
        cross = find_max_crossing(low, mid, high)

        # 최대값 반환
        if left[2] >= right[2] and left[2] >= cross[2]:
            return left
        elif right[2] >= left[2] and right[2] >= cross[2]:
            return right
        else:
            return cross

    return divide(0, len(arr) - 1)


# ==================== 거듭제곱 (Fast Exponentiation) ====================

def power(x: float, n: int) -> float:
    """
    거듭제곱 - 분할 정복

    시간복잡도: O(log n)

    x^n = x^(n/2) × x^(n/2)  (n이 짝수)
    x^n = x × x^((n-1)/2) × x^((n-1)/2)  (n이 홀수)
    """
    if n == 0:
        return 1
    if n < 0:
        return 1 / power(x, -n)

    half = power(x, n // 2)

    if n % 2 == 0:
        return half * half
    else:
        return x * half * half


def matrix_power(matrix: List[List[int]], n: int) -> List[List[int]]:
    """
    행렬 거듭제곱 - 피보나치 O(log n) 계산에 활용

    시간복잡도: O(log n) (행렬 곱셈 제외)
    """
    size = len(matrix)

    # 단위 행렬
    if n == 0:
        return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

    if n == 1:
        return matrix

    half = matrix_power(matrix, n // 2)

    if n % 2 == 0:
        return matrix_multiply(half, half)
    else:
        return matrix_multiply(matrix_multiply(half, half), matrix)


def matrix_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """행렬 곱셈"""
    n = len(A)
    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]

    return C


def fibonacci_fast(n: int) -> int:
    """
    피보나치 - 행렬 거듭제곱 활용

    시간복잡도: O(log n)
    """
    if n <= 1:
        return n

    # [[1,1],[1,0]]^n = [[F(n+1),F(n)],[F(n),F(n-1)]]
    base = [[1, 1], [1, 0]]
    result = matrix_power(base, n)
    return result[0][1]


# ==================== 스트라센 행렬 곱셈 ====================

def strassen_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """
    스트라센 행렬 곱셈

    시간복잡도: O(n^2.807)

    일반 행렬 곱셈: O(n³)
    스트라센: 8번 → 7번 곱셈으로 줄임
    """
    n = len(A)

    # 기저 조건
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    # 2의 거듭제곱 크기로 패딩 필요 (생략: n이 2^k라고 가정)
    mid = n // 2

    # 부분 행렬 분할
    A11 = [[A[i][j] for j in range(mid)] for i in range(mid)]
    A12 = [[A[i][j] for j in range(mid, n)] for i in range(mid)]
    A21 = [[A[i][j] for j in range(mid)] for i in range(mid, n)]
    A22 = [[A[i][j] for j in range(mid, n)] for i in range(mid, n)]

    B11 = [[B[i][j] for j in range(mid)] for i in range(mid)]
    B12 = [[B[i][j] for j in range(mid, n)] for i in range(mid)]
    B21 = [[B[i][j] for j in range(mid)] for i in range(mid, n)]
    B22 = [[B[i][j] for j in range(mid, n)] for i in range(mid, n)]

    # 7개의 곱셈
    M1 = strassen_multiply(_add(A11, A22), _add(B11, B22))
    M2 = strassen_multiply(_add(A21, A22), B11)
    M3 = strassen_multiply(A11, _sub(B12, B22))
    M4 = strassen_multiply(A22, _sub(B21, B11))
    M5 = strassen_multiply(_add(A11, A12), B22)
    M6 = strassen_multiply(_sub(A11, A21), _add(B11, B12))
    M7 = strassen_multiply(_sub(A12, A22), _add(B21, B22))

    # 결과 결합
    C11 = _add(_sub(_add(M1, M4), M5), M7)
    C12 = _add(M3, M5)
    C21 = _add(M2, M4)
    C22 = _add(_sub(_add(M1, M3), M2), M6)

    # 결과 병합
    C = [[0] * n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            C[i][j] = C11[i][j]
            C[i][j + mid] = C12[i][j]
            C[i + mid][j] = C21[i][j]
            C[i + mid][j + mid] = C22[i][j]

    return C


def _add(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def _sub(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


# ==================== 테스트 및 검증 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("분할 정복 알고리즘 테스트")
    print("=" * 50)

    # 병합 정렬
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"\n[병합 정렬]")
    print(f"원본: {arr}")
    print(f"정렬: {merge_sort(arr)}")

    # 퀵 정렬
    arr = [3, 6, 8, 10, 1, 2, 1]
    print(f"\n[퀵 정렬]")
    print(f"원본: {arr}")
    print(f"정렬: {quick_sort(arr)}")

    # 이진 탐색
    sorted_arr = [1, 3, 5, 7, 9, 11, 13]
    print(f"\n[이진 탐색]")
    print(f"배열: {sorted_arr}")
    print(f"7의 위치: {binary_search(sorted_arr, 7)}")

    # 최대 부분 배열
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    start, end, max_sum = max_subarray(arr)
    print(f"\n[최대 부분 배열]")
    print(f"배열: {arr}")
    print(f"최대 부분 배열: {arr[start:end+1]}, 합: {max_sum}")

    # 거듭제곱
    print(f"\n[거듭제곱]")
    print(f"2^10 = {power(2, 10)}")
    print(f"2^-3 = {power(2, -3):.6f}")

    # 피보나치
    print(f"\n[피보나치 O(log n)]")
    print(f"fib(10) = {fibonacci_fast(10)}")
    print(f"fib(50) = {fibonacci_fast(50)}")
```

---

### Ⅲ. 기술 비교 분석

#### 7. 대표 알고리즘 비교

| 알고리즘 | 분할 방식 | 시간복잡도 | 공간복잡도 | 결합 비용 | 특징 |
|---------|----------|-----------|-----------|----------|------|
| 병합 정렬 | 반반 분할 | O(n log n) | O(n) | O(n) | 안정 정렬 |
| 퀵 정렬 | 피벗 기준 | O(n log n) 평균 | O(log n) | O(n) | 제자리 정렬 |
| 이진 탐색 | 반반 분할 | O(log n) | O(1) | O(1) | 정렬 필수 |
| 스트라센 | 7개 부분 | O(n^2.81) | O(n²) | O(n²) | 행렬 곱셈 |
| 카라츠바 | 3개 부분 | O(n^1.58) | O(n) | O(n) | 큰 수 곱셈 |
| FFT | 짝수/홀수 | O(n log n) | O(n) | O(n) | 신호 처리 |

#### 8. 분할 정복 vs 동적계획법 vs 탐욕

| 구분 | 분할 정복 | 동적계획법 | 탐욕 알고리즘 |
|-----|----------|-----------|--------------|
| 하위 문제 | **독립적** | 중복 가능 | 없음 |
| 최적해 | 보장 | 보장 | 조건부 |
| 메모리 | 낮음 | 높음 (테이블) | 최소 |
| 적용 조건 | 분해 가능 | 최적 부분구조 | 탐욕 선택 속성 |
| 병렬화 | ★ 용이 | 어려움 | 불가능 |
| 예시 | 병합정렬, FFT | 배낭문제, LCS | 다익스트라, 프림 |

#### 9. 장단점 분석

| 장점 | 단점 |
|-----|------|
| 병렬 처리에 최적 | 재귀 호출 오버헤드 |
| 문제 단순화 | 스택 오버플로우 가능 |
| 이해/구현 용이 | 결합 비용이 크면 비효율 |
| 캐시 효율 (일부) | 작은 문제에서 오히려 느림 |
| 수학적 분석 용이 | 문제 분할이 어려울 수 있음 |

---

### Ⅳ. 실무 적용 방안

#### 10. 실무 적용 시나리오

| 적용 분야 | 구체적 적용 방법 | 기대 효과 |
|---------|----------------|----------|
| **대용량 정렬** | 병합 정렬로 외부 정렬 (디스크 기반) | TB 단위 정렬 가능 |
| **신호 처리** | FFT로 오디오/이미지 주파수 분석 | 실시간 DSP 처리 |
| **암호화** | 큰 수 거듭제곱 (모듈러 거듭제곱) | RSA 암호화 O(log n) |
| **게임 AI** | Minimax 알고리즘으로 수 탐색 | 최적 수 계산 |
| **지리 정보** | 최근접 점 쌍 문제 해결 | O(n log n) 탐색 |

#### 11. 실제 기업/서비스 사례

- **Google BigQuery**: 분할 정복 기반 대규모 데이터 처리
- **FFTW (Fastest Fourier Transform in the West)**: FFT 라이브러리, 수치 해석 표준
- **OpenSSL**: 모듈러 거듭제곱으로 RSA 암호화 최적화
- **Redis**: 정렬된 집합(Sorted Set)에 퀵 정렬 변형 사용
- **NVIDIA cuBLAS**: GPU에서 스트라센 기반 행렬 곱셈

#### 12. 도입 시 고려사항

1. **기술적**:
   - 하위 문제 독립성 확인 (중복되면 DP 고려)
   - 재귀 깊이 제한 고려 (반복적 구현으로 변환)
   - 결합 단계 최적화

2. **운영적**:
   - 병렬 처리 활용 (멀티코어/GPU)
   - 작은 문제는 반복문으로 처리

3. **보안적**:
   - 재귀 깊이 공격 방지 (깊이 제한)
   - 메모리 과다 사용 방지

4. **경제적**:
   - 라이브러리 활용 (FFTW, BLAS)
   - 병렬화 투자 대비 효과 분석

#### 13. 주의사항 / 흔한 실수

- ❌ 하위 문제 중복 미확인 → 동적계획법 필요
- ❌ 결합 단계 비용 과대 → 전체 성능 저하
- ❌ 재귀 깊이 과다 → 스택 오버플로우
- ❌ 작은 입력에도 재귀 사용 → 오버헤드

#### 14. 관련 개념

```
📌 분할 정복 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  [재귀] ←──→ [분할 정복] ←──→ [병렬 컴퓨팅]                   │
│       ↓           ↓                ↓                           │
│  [동적계획법]  [정렬 알고리즘]  [MapReduce]                    │
│                   ↓                                             │
│              [FFT/신호처리]                                     │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 재귀 (Recursion) | 기반 기법 | 분할 정복의 핵심 구조 | `[재귀](./recursion.md)` |
| 동적계획법 | 대안 | 중복 부분 문제가 있을 때 | `[DP](./dynamic_programming.md)` |
| 정렬 | 응용 | 병합정렬, 퀵정렬 | `[정렬](./sorting.md)` |
| 병렬처리 | 확장 | 분할된 문제의 병렬 수행 | 관련 문서 참조 |
| FFT | 응용 | 고속 푸리에 변환 | 신호 처리 문서 참조 |

---

### Ⅴ. 기대 효과 및 결론

#### 15. 정량적 기대 효과

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 알고리즘 효율 | O(n²) → O(n log n) 개선 | 처리 속도 10~100배 향상 |
| 병렬화 | 독립 하위 문제 병렬 처리 | 코어 수에 비례한 속도 향상 |
| 메모리 효율 | 제자리 알고리즘 선택 | 메모리 50% 절감 |
| 확장성 | 대규모 문제 해결 | TB 단위 데이터 처리 |

#### 16. 미래 전망

1. **기술 발전 방향**:
   - GPU/TPU 활용한 대규모 병렬 분할 정복
   - 양자 알고리즘 (양자 FFT, Shor 알고리즘)

2. **시장 트렌드**:
   - 빅데이터 처리 프레임워크 (MapReduce, Spark)
   - 실시간 스트림 처리

3. **후속 기술**:
   - 하이브리드 알고리즘 (분할정복 + DP)
   - 기계학습 기반 문제 분할 최적화

> **결론**: 분할 정복은 알고리즘 설계의 근간이 되는 기법으로, 병합정렬, 퀵정렬, FFT 등 핵심 알고리즘의 기반이다. 하위 문제의 독립성이 보장될 때 병렬화에 최적이며, Master Theorem으로 시간복잡도를 체계적으로 분석할 수 있다.

> **※ 참고 표준**: CLRS 'Introduction to Algorithms', Cormen et al., MIT Press

---

## 어린이를 위한 종합 설명

**분할 정복을 쉽게 이해해보자!**

분할 정복은 마치 **거대한 퍼즐을 맞추는 방법**과 같아요. 큰 퍼즐을 한 번에 다 맞추려면 너무 어렵지만, 작은 조각으로 나누어 맞춘 다음 합치면 훨씬 쉬워져요.

첫째, **나누기(Divide)**예요. 큰 문제를 반으로 나누고, 또 반으로 나누고, 아주 작아질 때까지 계속 나눠요. 마치 피자를 여러 조각으로 자르는 것과 같아요.

둘째, **해결하기(Conquer)**예요. 작아진 문제는 쉽게 해결할 수 있어요. 마치 작은 퍼즐 조각 몇 개를 맞추는 것처럼요.

셋째, **합치기(Combine)**예요. 작은 해답들을 모아서 큰 해답을 만들어요. 퍼즐 조각들을 이어 붙여서 완성하는 것과 같아요. 이렇게 하면 아주 큰 문제도 체계적으로 해결할 수 있어요!

---
