+++
title = "탐욕 알고리즘 (Greedy Algorithm)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 탐욕 알고리즘 (Greedy Algorithm)

## 핵심 인사이트 (3줄 요약)
> **매 순간 최적 선택이 전체 최적으로 이어지는 알고리즘**. 탐욕적 선택 속성 + 최적 부분 구조 필수. 다익스트라, 허프만 코딩, MST의 핵심 기법.

---

## 📝 기술사 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"탐욕 알고리즘의 원리와 동작 과정을 설명하고, 유사 알고리즘과 비교하여 적합한 활용 시나리오를 기술하시오."**

---

### Ⅰ. 개요

#### 1. 개념
탐욕 알고리즘(Greedy Algorithm)은 **각 단계에서 현재 상황에서 가장 최적인 선택을 하여 전체 문제의 최적해를 구하는 알고리즘**이다. 매 순간의 선택이 이후 선택에 영향을 주지 않는다는 가정하에 동작하며, 한 번 선택은 번복하지 않는다.

> 💡 **비유**: "매장에서 가장 싼 것만 담기" - 그 순간 최선을 선택하면 전체도 최선이 되는 방식

**등장 배경**:
1. **기존 문제점**: 완전 탐색은 지수 시간, 동적계획법은 메모리 과다
2. **기술적 필요성**: 빠른 의사결정이 필요한 실시간 시스템
3. **시장 요구**: 근사해로 충분한 최적화 문제 (스케줄링, 라우팅)

**핵심 목적**: 지역 최적 선택으로 전역 최적해 도달 (조건부 보장)

---

### Ⅱ. 구성 요소 및 핵심 원리

#### 2. 탐욕 알고리즘 필수 조건

| 조건 | 설명 | 검증 방법 |
|-----|------|----------|
| 탐욕적 선택 속성 | 지역 최적 선택 = 전역 최적해의 일부 | 수학적 귀납법, 교환 논증 |
| 최적 부분 구조 | 최적해의 부분도 최적해 | 부분 문제 독립성 확인 |
| 선택의 번복 없음 | 한 번 선택은 최종 선택 | 단방향 진행 |

#### 3. 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│               탐욕 알고리즘 동작 흐름                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📌 일반적 과정:                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. Selection: 후보 중 최적 선택                    │   │
│  │  2. Feasibility: 선택이 유효한지 확인               │   │
│  │  3. Solution: 완료되었는지 확인                     │   │
│  │  4. 반복: 미완료 시 1로 이동                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  🔄 동전 거스름 예시 (단위: 500, 100, 50, 10):              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  거스름: 860원                                       │   │
│  │                                                     │   │
│  │  Step 1: 860 ≥ 500? Yes → 500원 1개 선택           │   │
│  │          남은 금액: 360원                           │   │
│  │                                                     │   │
│  │  Step 2: 360 ≥ 100? Yes → 100원 3개 선택           │   │
│  │          남은 금액: 60원                            │   │
│  │                                                     │   │
│  │  Step 3: 60 ≥ 50? Yes → 50원 1개 선택              │   │
│  │          남은 금액: 10원                            │   │
│  │                                                     │   │
│  │  Step 4: 10 ≥ 10? Yes → 10원 1개 선택              │   │
│  │          남은 금액: 0원 → 완료                      │   │
│  │                                                     │   │
│  │  결과: 500×1 + 100×3 + 50×1 + 10×1 = 860원         │   │
│  │        총 6개 동전 (최소)                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ⚠️ 주의: 모든 동전 단위에 적용되지 않음                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  예: 30원을 20, 15, 10원으로 거슬러야 할 때         │   │
│  │      탐욕: 20 + 10 = 30 (2개)                       │   │
│  │      최적: 15 + 15 = 30 (2개)                       │   │
│  │      → 이 경우 동일하지만, 40원이면?                │   │
│  │      탐욕: 20+10+10 = 40 (3개) ❌                   │   │
│  │      최적: 20+20 = 40 (2개) ✓                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 4. 동작 원리 단계별 설명

```
① 후보 집합 생성 → ② 선택 함수로 최적 선택 → ③ 적합성 검사 → ④ 해에 포함 → ⑤ 반복/종료
```

- **1단계**: 선택 가능한 모든 후보 식별
- **2단계**: 선택 함수(Selection Function)로 최적 후보 선택
- **3단계**: 선택이 제약 조건을 만족하는지 확인
- **4단계**: 유효한 선택을 해 집합에 포함
- **5단계**: 해가 완성될 때까지 반복

#### 5. Python 코드 예시

```python
from typing import List, Tuple
import heapq

# ==================== 동전 거스름돈 ====================

def coin_change_greedy(amount: int, coins: List[int]) -> Tuple[List[int], int]:
    """
    동전 거스름돈 - 탐욕 알고리즘

    Args:
        amount: 거스름돈 금액
        coins: 동전 단위 리스트 (내림차순 정렬 필요)

    Returns:
        (각 동전별 개수 리스트, 총 동전 개수)

    주의: 모든 동전 시스템에서 최적해를 보장하지 않음
    한국/미국 화폐는 정렬된 약수 관계여서 보장됨
    """
    coins = sorted(coins, reverse=True)  # 내림차순
    counts = []

    for coin in coins:
        count = amount // coin
        counts.append(count)
        amount %= coin

    return counts, sum(counts)


# ==================== 활동 선택 문제 ====================

def activity_selection(start: List[int], finish: List[int]) -> List[int]:
    """
    활동 선택 문제 - 가장 많은 활동 선택

    Args:
        start: 각 활동의 시작 시간
        finish: 각 활동의 종료 시간

    Returns:
        선택된 활동의 인덱스 리스트

    탐욕 전략: 종료 시간이 가장 빠른 것부터 선택
    시간복잡도: O(n log n) - 정렬 필요
    """
    # 활동을 (종료시간, 시작시간, 인덱스)로 묶어 정렬
    activities = sorted(zip(finish, start, range(len(start))))

    selected = []
    last_finish = 0

    for f, s, idx in activities:
        if s >= last_finish:  # 이전 활동 종료 후 시작
            selected.append(idx)
            last_finish = f

    return selected


# ==================== 분할 가능 배낭 문제 ====================

def fractional_knapsack(capacity: int,
                        weights: List[int],
                        values: List[int]) -> Tuple[float, List[Tuple[int, float]]]:
    """
    분할 가능 배낭 문제 - 탐욕 알고리즘

    물건을 일부분만 담을 수 있음 (분할 가능)
    탐욕 전략: 가치/무게 비율이 높은 것부터 선택

    Returns:
        (총 가치, [(물건 인덱스, 담은 비율), ...])
    """
    # 가치/무게 비율로 정렬
    items = sorted(
        [(v / w, w, v, i) for i, (w, v) in enumerate(zip(weights, values))],
        reverse=True
    )

    total_value = 0
    remaining = capacity
    selected = []

    for ratio, weight, value, idx in items:
        if remaining >= weight:
            # 전체 담기
            selected.append((idx, 1.0))
            total_value += value
            remaining -= weight
        else:
            # 일부만 담기
            fraction = remaining / weight
            selected.append((idx, fraction))
            total_value += value * fraction
            break

    return total_value, selected


# ==================== 허프만 코딩 ====================

class HuffmanNode:
    def __init__(self, char: str = None, freq: int = 0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def huffman_coding(chars: List[str], freqs: List[int]) -> dict:
    """
    허프만 코딩 - 최적 접두사 코드 생성

    탐욕 전략: 빈도가 가장 낮은 두 노드를 합침
    시간복잡도: O(n log n)
    """
    # 최소 힙 생성
    heap = [HuffmanNode(c, f) for c, f in zip(chars, freqs)]
    heapq.heapify(heap)

    # 트리 구축
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    # 코드 생성
    root = heap[0]
    codes = {}

    def generate_codes(node: HuffmanNode, code: str = ""):
        if node.char:
            codes[node.char] = code
            return

        if node.left:
            generate_codes(node.left, code + "0")
        if node.right:
            generate_codes(node.right, code + "1")

    generate_codes(root)
    return codes


# ==================== 최소 신장 트리 (Prim) ====================

def prim_mst(graph: List[List[Tuple[int, int]]]) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Prim 알고리즘 - 최소 신장 트리

    탐욕 전략: 현재 트리에 연결된 최소 가중치 간선 선택

    Args:
        graph: 인접 리스트 [(인접노드, 가중치), ...]

    Returns:
        (MST 총 가중치, [(u, v, 가중치), ...])
    """
    n = len(graph)
    in_mst = [False] * n
    min_edge = [(float('inf'), -1)] * n  # (가중치, 부모)

    min_edge[0] = (0, -1)
    total_weight = 0
    mst_edges = []

    for _ in range(n):
        # 최소 간선 찾기 (탐욕 선택)
        u = -1
        for v in range(n):
            if not in_mst[v] and (u == -1 or min_edge[v][0] < min_edge[u][0]):
                u = v

        in_mst[u] = True
        total_weight += min_edge[u][0]

        if min_edge[u][1] != -1:
            mst_edges.append((min_edge[u][1], u, min_edge[u][0]))

        # 인접 노드 갱신
        for v, weight in graph[u]:
            if not in_mst[v] and weight < min_edge[v][0]:
                min_edge[v] = (weight, u)

    return total_weight, mst_edges


# ==================== 최소 신장 트리 (Kruskal) ====================

class UnionFind:
    """Union-Find (Disjoint Set Union)"""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 경로 압축
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True


def kruskal_mst(n: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Kruskal 알고리즘 - 최소 신장 트리

    탐욕 전략: 가중치가 가장 작은 간선부터 선택 (사이클 제외)
    시간복잡도: O(E log E)
    """
    edges = sorted(edges, key=lambda x: x[2])  # 가중치 순 정렬
    uf = UnionFind(n)

    total_weight = 0
    mst_edges = []

    for u, v, weight in edges:
        if uf.union(u, v):  # 사이클이 아니면
            mst_edges.append((u, v, weight))
            total_weight += weight

            if len(mst_edges) == n - 1:
                break

    return total_weight, mst_edges


# ==================== 작업 스케줄링 ====================

def job_scheduling(jobs: List[Tuple[int, int, int]]) -> Tuple[int, List[int]]:
    """
    작업 스케줄링 (최대 이익)

    Args:
        jobs: [(마감시간, 이익, 작업ID), ...]

    Returns:
        (총 이익, 선택된 작업 ID 리스트)
    """
    # 마감시간 기준 정렬
    jobs = sorted(jobs, key=lambda x: x[0])

    max_deadline = max(j[0] for j in jobs)
    slots = [None] * (max_deadline + 1)  # 각 시간 슬롯

    # 이익 내림차순으로 정렬 후 배치
    jobs_by_profit = sorted(jobs, key=lambda x: -x[1])

    total_profit = 0
    selected = []

    for deadline, profit, job_id in jobs_by_profit:
        # 가능한 가장 늦은 슬롯 찾기
        slot = deadline
        while slot > 0 and slots[slot] is not None:
            slot -= 1

        if slot > 0:
            slots[slot] = job_id
            total_profit += profit
            selected.append(job_id)

    return total_profit, selected


# ==================== 테스트 및 검증 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("탐욕 알고리즘 테스트")
    print("=" * 50)

    # 동전 거스름돈
    print("\n[동전 거스름돈]")
    coins = [500, 100, 50, 10]
    amount = 860
    counts, total = coin_change_greedy(amount, coins)
    print(f"거스름돈: {amount}원")
    for coin, count in zip(coins, counts):
        if count > 0:
            print(f"  {coin}원: {count}개")
    print(f"총 동전 개수: {total}개")

    # 활동 선택
    print("\n[활동 선택]")
    start = [1, 3, 0, 5, 8, 5]
    finish = [2, 4, 6, 7, 9, 9]
    selected = activity_selection(start, finish)
    print(f"시작: {start}")
    print(f"종료: {finish}")
    print(f"선택된 활동: {selected}")

    # 분할 가능 배낭
    print("\n[분할 가능 배낭]")
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    total_val, items = fractional_knapsack(capacity, weights, values)
    print(f"용량: {capacity}, 무게: {weights}, 가치: {values}")
    print(f"선택: {items}")
    print(f"총 가치: {total_val}")

    # 허프만 코딩
    print("\n[허프만 코딩]")
    chars = ['a', 'b', 'c', 'd', 'e', 'f']
    freqs = [5, 9, 12, 13, 16, 45]
    codes = huffman_coding(chars, freqs)
    print(f"문자: {chars}, 빈도: {freqs}")
    print(f"코드: {codes}")

    # MST (Prim)
    print("\n[Prim MST]")
    graph = [
        [(1, 2), (2, 3)],  # 0
        [(0, 2), (2, 1), (3, 4)],  # 1
        [(0, 3), (1, 1), (3, 5)],  # 2
        [(1, 4), (2, 5)]  # 3
    ]
    weight, edges = prim_mst(graph)
    print(f"MST 간선: {edges}")
    print(f"총 가중치: {weight}")
```

---

### Ⅲ. 기술 비교 분석

#### 6. Greedy vs DP vs Backtracking

| 구분 | 탐욕 | 동적계획법 | 백트래킹 |
|-----|------|----------|----------|
| 선택 방식 | 매 순간 최적 | 모든 경우 고려 | 유망한 경우만 |
| 시간복잡도 | 낮음 (보통 O(n log n)) | 높음 (O(n²)~O(2^n)) | 중간~높음 |
| 최적해 보장 | **조건부** | 항상 | 항상 |
| 메모리 | 최소 | 많음 (테이블) | 중간 (재귀 스택) |
| 적용 조건 | 탐욕 선택 속성 + 최적 부분 구조 | 최적 부분 구조 + 중복 부분 문제 | 제약 충족 문제 |
| 구현 난이도 | 낮음 | 중간 | 중간 |

#### 7. 대표 문제별 알고리즘 적용

| 문제 | 탐욕 적용 | 최적해 보장 | 대안 |
|-----|---------|-----------|------|
| 동전 거스름 (한국/미국) | ✓ | ✓ | - |
| 동전 거스름 (일반) | ✓ | ❌ | DP |
| 분할 가능 배낭 | ✓ | ✓ | - |
| 0-1 배낭 | ❌ | ❌ | DP |
| 활동 선택 | ✓ | ✓ | - |
| 최소 신장 트리 | ✓ (Prim/Kruskal) | ✓ | - |
| 최단 경로 (음수 없음) | ✓ (다익스트라) | ✓ | Bellman-Ford |
| 최단 경로 (음수 있음) | ❌ | ❌ | Bellman-Ford |
| 허프만 코딩 | ✓ | ✓ | - |

#### 8. 장단점 분석

| 장점 | 단점 |
|-----|------|
| 구현 간단 | 모든 문제에 적용 불가 |
| 빠른 수행 속도 | 최적해 보장 안 됨 (조건부) |
| 메모리 효율적 | 근사해일 수 있음 |
| 실시간 의사결정 가능 | 탐욹 조건 증명 어려움 |
| 직관적 이해 | 이전 선택 번복 불가 |

---

### Ⅳ. 실무 적용 방안

#### 9. 실무 적용 시나리오

| 적용 분야 | 구체적 적용 방법 | 기대 효과 |
|---------|----------------|----------|
| **네트워크 라우팅** | 다익스트라로 최단 경로 계산 | 패킷 전송 지연 30% 감소 |
| **압축** | 허프만 코딩으로 무손실 압축 | 파일 크기 40~60% 감소 |
| **스케줄링** | 활동 선택으로 자원 배분 | 자원 활용률 25% 향상 |
| **클러스터링** | Kruskal 기반 계층적 클러스터링 | 데이터 분석 효율화 |
| **CPU 스케줄링** | SJF(Shortest Job First) | 평균 대기 시간 최소화 |

#### 10. 실제 기업/서비스 사례

- **Google Maps**: 다익스트라/A*로 최단 경로 안내
- **ZIP/GZIP**: 허프만 코딩 + LZ77으로 압축
- **Cisco 라우터**: OSPF 프로토콜로 다익스트라 기반 라우팅
- **AWS VPC**: MST 기반 네트워크 토폴로지 최적화
- **UPS/ORION**: 탐욕 기반 배송 경로 최적화 (연료 10% 절감)

#### 11. 도입 시 고려사항

1. **기술적**:
   - 탐욹적 선택 속성 증명 필수
   - 최적해 보장 여부 확인 (0-1 배낭 vs 분할 가능 배낭)
   - 근사해로 충분한지 판단

2. **운영적**:
   - 정렬 비용 고려 (O(n log n))
   - 실시간 요구사항과 탐욹 적합성

3. **보안적**:
   - 입력 검증 (음수 가중치 등)
   - DoS 방지를 위한 입력 크기 제한

4. **경제적**:
   - 근사해로 충분하면 탐욕, 아니면 DP/분기한정
   - 오픈소스 라이브러리 활용 (NetworkX 등)

#### 12. 주의사항 / 흔한 실수

- ❌ 0-1 배낭에 탐욕 적용 → 최적해 아님
- ❌ 음수 간선 그래프에 다익스트라 → 잘못된 결과
- ❌ 탐욹 조건 미확인 → 검증 없이 적용
- ❌ 정렬 순서 오류 → 잘못된 선택

#### 13. 관련 개념

```
📌 탐욕 알고리즘 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  [최적화 이론] ←──→ [탐욕 알고리즘] ←──→ [근사 알고리즘]       │
│       ↓                  ↓                  ↓                  │
│  [동적계획법]       [MST(Prim/Kruskal)]  [지역 탐색]           │
│       ↓                  ↓                                     │
│  [분기한정]         [다익스트라]                               │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 동적계획법 | 대안 | 탐욕으로 해결 안 될 때 | `[DP](./dynamic_programming.md)` |
| 최소 신장 트리 | 응용 | Prim, Kruskal | `[MST](./mst.md)` |
| 최단 경로 | 응용 | 다익스트라 | `[최단경로](./shortest_path.md)` |
| 분할 정복 | 비교 | 독립 부분 문제 | `[분할정복](./divide_conquer.md)` |
| 근사 알고리즘 | 확장 | NP-Hard 문제 근사해 | CLRS 참조 |

---

### Ⅴ. 기대 효과 및 결론

#### 14. 정량적 기대 효과

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 알고리즘 효율 | O(2^n) → O(n log n) | 처리 속도 100배+ 향상 |
| 메모리 절약 | DP 테이블 불필요 | 메모리 90% 절감 |
| 실시간 처리 | 빠른 의사결정 | 응답 시간 <1ms |
| 구현 비용 | 단순한 코드 | 개발 시간 50% 단축 |

#### 15. 미래 전망

1. **기술 발전 방향**:
   - 기계학습 기반 탐욕 휴리스틱 학습
   - 병렬 탐욕 알고리즘

2. **시장 트렌드**:
   - 실시간 최적화 수요 증가 (자율주행, IoT)
   - 근사 알고리즘으로서의 가치 재조명

3. **후속 기술**:
   - 메타휴리스틱과 결합 (유전알고리즘 초기해)
   - 양자 탐욕 알고리즘

> **결론**: 탐욕 알고리즘은 간단하고 빠르지만, 모든 문제에 적용할 수 없다. 탐욹적 선택 속성과 최적 부분 구조가 성립하는지 확인이 선행되어야 한다. MST, 다익스트라, 허프만 코딩 등은 탐욕으로 최적해를 보장하는 대표적 사례다.

> **※ 참고 표준**: CLRS 'Introduction to Algorithms', Kleinberg & Tardos 'Algorithm Design'

---

## 어린이를 위한 종합 설명

**탐욕 알고리즘을 쉽게 이해해보자!**

탐욕 알고리즘은 마치 **편의점에서 가장 싼 물건만 골라 담는 방식**과 같아요. 매 순간 "지금 가장 좋은 게 뭐지?"를 생각하고 선택해요.

첫째, **지금 최고만 고르기**예요. 동전으로 거스름돈을 줄 때, 가장 큰 동전부터 최대한 많이 주면 돼요. 860원을 줘야 하면 500원 1개, 100원 3개, 50원 1개, 10원 1개. 이렇게 하면 동전 개수가 가장 적어져요!

둘째, **항상 최고는 아니에요**. 하지만 이 방법이 항상 정답을 주는 건 아니에요. 30원을 20원, 15원, 10원 동전으로 줘야 한다면? 탐욕대로 하면 20+10=30(2개)인데, 사실 15+15=30(2개)도 같아요. 하지만 40원이면 탐욕은 20+10+10=40(3개)인데, 20+20=40(2개)가 더 좋아요!

---
