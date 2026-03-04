+++
title = "접미사 배열 (Suffix Array)"
date = 2026-03-04

[extra]
categories = "pe_exam-algorithm_stats"
tags = ["접미사배열", "서픽스어레이", "LCP", "문자열알고리즘", "접미사트리"]
+++

# 접미사 배열 (Suffix Array)

## 핵심 인사이트

> **문자열의 모든 접미사를 사전순으로 정렬한 인덱스 배열**이다. O(n) 공간으로 접미사 트리의 핵심 기능을 제공하며, 문자열 검색, 반복 부분 문자열, LCP 등 고급 문자열 처리의 기반이다.

- **무엇**: 정렬된 접미사의 시작 인덱스 배열
- **왜 중요**: O(n log n) 구축, O(n) 공간, 다양한 응용
- **어떻게**: 정렬 + LCP 배열로 최적화

---

### Ⅰ. 개요

**정의**: 접미사 배열(Suffix Array)은 **문자열 S의 모든 접미사를 사전순으로 정렬했을 때, 각 접미사의 시작 인덱스를 저장한 배열**이다.

> 💡 **직관적 비유**: 책의 찾아보기(인덱스)와 같다. 모든 단어를 가나다순으로 정렬해두면, 원하는 단어를 빠르게 찾을 수 있다.

**등장 배경**:
1. **접미사 트리 공간 문제**: O(n) 노드지만 상수가 큼
2. **실용적 대안**: O(n) 공간, 캐시 친화적
3. **다양한 응용**: 검색, 반복 패턴, 압축

**핵심 목적**: 문자열의 모든 접미사를 효율적으로 관리하고 검색

---

### Ⅱ. 필요성

#### 현황 및 문제점

| 문제 구분 | 구체적 내용 | 영향·심각도 |
|----------|-----------|----------|
| **접미사 트리 복잡** | 구현 난이도, 메모리 | 진입 장벽 |
| **단순 검색 느림** | O(nm) | 비효율 |
| **고급 처리 불가** | 반복 패턴, LCP | 기능 부족 |

#### 기술적 필요성

- **왜 지금인가**: 바이오인포매틱스, 검색엔진, 압축
- **왜 이 접근인가**: O(n log n) 구축, O(n) 공간
- **표준 압박**: 고급 문자열 처리의 표준

#### 도입 시 기대 가치

| 가치 영역 | 기대 효과 | 비고 |
|----------|----------|------|
| 공간 | O(n) | 트리의 1/4 |
| 구축 | O(n log n) | 실용적 |
| 검색 | O(m log n) | 이진 탐색 |

---

### Ⅲ. 구조와 원리

#### 구성 요소

| 구성 요소 | 역할 | 기술적 특징 | 직관적 비유 |
|----------|------|------------|------------|
| **SA 배열** | 정렬된 접미사 인덱스 | 길이 n | "찾아보기" |
| **LCP 배열** | 인접 접미사 공통 접두사 길이 | O(n) 구축 | "공통 부분" |
| **원본 문자열** | S | 접미사 출처 | "책 본문" |

#### 접미사 배열 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    접미사 배열 예시                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  문자열 S = "banana"                                        │
│                                                             │
│  모든 접미사:                                               │
│  0: banana                                                  │
│  1: anana                                                   │
│  2: nana                                                    │
│  3: ana                                                     │
│  4: na                                                      │
│  5: a                                                       │
│                                                             │
│  사전순 정렬:                                               │
│  5: a          ← 가장 작음                                  │
│  3: ana                                                     │
│  1: anana                                                   │
│  0: banana                                                  │
│  4: na                                                      │
│  2: nana      ← 가장 큼                                     │
│                                                             │
│  접미사 배열 SA = [5, 3, 1, 0, 4, 2]                        │
│                                                             │
│  LCP 배열 (인접 접미사 간 공통 접두사 길이):                │
│  LCP[0] = 0 (시작)                                          │
│  LCP[1] = 1 (a vs ana → "a" 공통)                          │
│  LCP[2] = 3 (ana vs anana → "ana" 공통)                    │
│  LCP[3] = 0 (anana vs banana → 없음)                       │
│  LCP[4] = 2 (banana vs na → "na" 공통)                     │
│  LCP[5] = 2 (na vs nana → "na" 공통)                       │
│                                                             │
│  LCP = [0, 1, 3, 0, 2, 2]                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 핵심 수식

**접미사**:
```
Suffix(i) = S[i:], i = 0, 1, ..., n-1
```

**접미사 배열**:
```
SA[k] = Suffix(i)가 사전순 k번째일 때의 i
```

**LCP**:
```
LCP[k] = LCP(Suffix(SA[k-1]), Suffix(SA[k]))
```

#### 코드 예시

```python
def build_suffix_array_naive(s):
    """
    단순한 접미사 배열 구축
    시간: O(n² log n)
    """
    n = len(s)
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()  # 사전순 정렬
    return [idx for _, idx in suffixes]

def build_lcp_array(s, sa):
    """
    LCP 배열 구축 (Kasai 알고리즘)
    시간: O(n)
    """
    n = len(s)
    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i

    lcp = [0] * n
    k = 0

    for i in range(n):
        if rank[i] == 0:
            k = 0
            continue

        j = sa[rank[i] - 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1

        lcp[rank[i]] = k
        if k > 0:
            k -= 1

    return lcp

def build_suffix_array_manber_myers(s):
    """
    Manber-Myers 알고리즘
    시간: O(n log² n)
    """
    n = len(s)
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0] * n

    k = 1
    while k < n:
        # 2k 길이 접미사로 정렬
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))

        tmp[sa[0]] = 0
        for i in range(1, n):
            prev, cur = sa[i-1], sa[i]
            tmp[cur] = tmp[prev]
            if (rank[prev], rank[prev + k] if prev + k < n else -1) != \
               (rank[cur], rank[cur + k] if cur + k < n else -1):
                tmp[cur] += 1

        rank, tmp = tmp, rank
        if rank[sa[-1]] == n - 1:
            break
        k *= 2

    return sa

def pattern_search(s, sa, pattern):
    """
    패턴 검색 (이진 탐색)
    시간: O(m log n)
    """
    n = len(s)
    m = len(pattern)

    # 하한 찾기
    low, high = 0, n
    while low < high:
        mid = (low + high) // 2
        if s[sa[mid]:sa[mid]+m] < pattern:
            low = mid + 1
        else:
            high = mid

    start = low

    # 상한 찾기
    high = n
    while low < high:
        mid = (low + high) // 2
        if s[sa[mid]:sa[mid]+m] <= pattern:
            low = mid + 1
        else:
            high = mid

    return [sa[i] for i in range(start, low)]

def longest_repeated_substring(s, sa, lcp):
    """
    가장 긴 반복 부분 문자열
    시간: O(n)
    """
    max_lcp = max(lcp)
    if max_lcp == 0:
        return ""

    idx = lcp.index(max_lcp)
    return s[sa[idx]:sa[idx]+max_lcp]

def count_distinct_substrings(s, sa):
    """
    서로 다른 부분 문자열 개수
    시간: O(n)
    """
    n = len(s)
    lcp = build_lcp_array(s, sa)
    total = n * (n + 1) // 2  # 전체 부분 문자열
    return total - sum(lcp)

# 사용 예시
if __name__ == "__main__":
    s = "banana"

    # 접미사 배열 구축
    sa = build_suffix_array_naive(s)
    print(f"문자열: {s}")
    print(f"접미사 배열: {sa}")

    # LCP 배열
    lcp = build_lcp_array(s, sa)
    print(f"LCP 배열: {lcp}")

    # 패턴 검색
    pattern = "ana"
    positions = pattern_search(s, sa, pattern)
    print(f"'{pattern}' 검색 결과: {positions}")

    # 가장 긴 반복 부분 문자열
    lrs = longest_repeated_substring(s, sa, lcp)
    print(f"가장 긴 반복 부분 문자열: '{lrs}'")

    # 서로 다른 부분 문자열 개수
    distinct = count_distinct_substrings(s, sa)
    print(f"서로 다른 부분 문자열 개수: {distinct}")
```

---

### Ⅳ. 비교 분석

#### 장단점

| 장점 | 단점 |
|------|------|
| O(n) 공간 | 구축 O(n log n) |
| 캐시 친화적 | 패턴 검색 O(m log n) |
| 구현 단순 | 업데이트 어려움 |
| LCP 응용 다양 | 정적 문자열만 |

#### 접미사 트리 vs 배열

| 비교 | **접미사 배열** | **접미사 트리** |
|------|:--------------:|:--------------:|
| 공간 | O(n) | O(n) ~ 4n |
| 구축 | O(n log n) | O(n) |
| 검색 | O(m log n) | O(m) |
| 구현 | ★ 단순 | 복잡 |
| 캐시 | ★ 우수 | 불리 |

---

### Ⅴ. 실무 적용

#### 적용 시나리오

| 적용 분야 | 적용 방법 | 기대 효과 |
|----------|----------|----------|
| DNA 분석 | 패턴 검색 | O(m log n) |
| 압축 (BWT) | 접미사 배열 활용 | 효율적 압축 |
| 검색엔진 | 역인덱스 구축 | 빠른 검색 |
| 표절 검사 | LCP 기반 | 유사도 계산 |

#### 실제 도입 사례

- **bzip2**: Burrows-Wheeler Transform
- **BLAST**: DNA 서열 정렬
- **grep**: 패턴 검색 최적화
- ** diff**: 파일 비교

---

### Ⅵ. 결론

#### 기대 효과

| 효과 영역 | 내용 | 정량 수치 |
|----------|------|----------|
| 공간 | O(n) | 트리의 1/4 |
| 검색 | O(m log n) | 빠른 검색 |
| 응용 | LCP, 반복 패턴 | 다양한 활용 |

#### 미래 전망

1. **SA-IS**: O(n) 구축 알고리즘
2. **FM-index**: 압축 접미사 배열
3. **Wavelet Tree**: 효율적 인덱싱

> **결론**: 접미사 배열은 공간 효율적인 문자열 인덱싱 도구다. LCP와 결합하면 강력하다.

> **참고 표준**: Gusfield "Algorithms on Strings", CP-Algorithms

---

### 관련 개념

| 관련 개념 | 관계 유형 | 설명 | 링크 |
|----------|----------|------|------|
| 문자열 매칭 | 응용 | 패턴 검색 | [string_matching](./string_matching.md) |
| Trie | 관련 | 접두사 트리 | [trie](../data_structure/trie.md) |
| 정렬 | 기반 | 접미사 정렬 | [sorting](./sorting.md) |

---

## 쉬운 설명

**접미사 배열**은 마치 **책의 찾아보기**와 같습니다.

"banana"라는 단어에서:
- a (위치 5)
- ana (위치 3)
- anana (위치 1)
- banana (위치 0)
- na (위치 4)
- nana (위치 2)

이렇게 모든 접미사를 사전순으로 정렬한 게 접미사 배열입니다.

**LCP**는 "인접한 두 단어가 얼마나 같은지"를 보여줍니다:
- "a" vs "ana" → 1글자 같음
- "ana" vs "anana" → 3글자 같음

이걸로 반복되는 패턴을 찾을 수 있습니다!

---

## 부록: 다각도 관점

### 관점 요약

| 관점 | 핵심 |
|------|------|
| 🔢 이론가 | O(n log n) 구축 |
| 🏛️ 설계자 | 공간 효율 |
| 💻 개발자 | Kasai 알고리즘 |
| 🔧 운영자 | 정적 데이터 |
| 📜 역사가 | Manber-Myers 1990 |