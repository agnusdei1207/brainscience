+++
title = "휴리스틱 탐색 (Heuristic Search / Informed Search)"
date = "2026-03-05"
[extra]
categories = "studynotes-ai"
+++

# 휴리스틱 탐색 (Heuristic Search / Informed Search)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 휴리스틱 탐색은 목표 상태까지의 예상 비용을 추정하는 휴리스틱 함수 h(n)을 활용하여 탐색 효율을 극대화하는 전략으로, A*, IDA*, Greedy Best-First 등의 알고리즘이 있으며, 휴리스틱의 품질이 탐색 성능을 결정한다.
> 2. **가치**: 맹목적 탐색 대비 탐색 노드 수를 90% 이상 감소시킬 수 있으며, 허용적(Admissible)이고 일관적(Consistent)인 휴리스틱을 사용하면 최적해를 보장하면서도 효율적으로 탐색한다.
> 3. **융합**: 휴리스틱 탐색은 경로 계획(네비게이션), 퍼즐 해결(8-퍼즐, 15-퍼즐), 게임 AI, 로봇 모션 플래닝, 지식 그래프 추론 등 다양한 분야에서 활용되며, 머신러닝으로 휴리스틱 함수를 학습하는 연구도 진행 중이다.

---

## I. 개요 (Context & Background)

### 개념 정의

휴리스틱 탐색(Heuristic Search), 또는 정보 기반 탐색(Informed Search)은 **문제 도메인에 특화된 지식이나 규칙을 활용하여 목표 상태에 더 빠르게 도달하는 탐색 전략**이다. 여기서 휴리스틱(Heuristic)이란 "발견적 방법"으로, 완벽한 정답은 아니지만 실용적으로 유용한 추정치나 규칙을 의미한다.

**핵심 개념 - 휴리스틱 함수 h(n)**:
- 현재 상태 n에서 목표 상태까지의 예상 비용을 추정
- h(n) = 0이면 맹목적 탐색과 동일
- h(n)이 정확할수록 탐색 효율 증가

**휴리스틱의 품질 조건**:
1. **허용성(Admissibility)**: h(n) ≤ h*(n) for all n (실제 비용 과대평가 안 함)
2. **일관성(Consistency/Monotonicity)**: h(n) ≤ c(n, n') + h(n') (삼각 부등식)

### 💡 비유: "지도를 보고 길 찾기"

휴리스틱 탐색을 **"지도를 보면서 목적지까지 가는 방법"**에 비유할 수 있다.

**맹목적 탐색 = 눈 가리고 길 찾기**: 목적지가 어디에 있는지 전혀 모르는 상태에서, 모든 길을 하나씩 시도해 본다. 목적지가 바로 옆에 있어도 멀리 돌아갈 수 있다.

**휴리스틱 탐색 = 지도 보고 가기**:
- **직선 거리 휴리스틱**: "목적지까지 직선으로 5km야. 그러니 직선 거리가 줄어드는 방향으로 가자!"
- **도로망 휴리스틱**: "이 길은 고속도로니까 더 빠를 거야"
- **교통량 휴리스틱**: "지금 퇴근 시간이니 이쪽은 피하자"

휴리스틱이 완벽하면 한 번에 목적지에 도달한다. 휴리스틱이 대충이어도 맹목적 탐색보다는 훨씬 빠르다. 중요한 건 "절대로 실제보다 멀다고 추정하면 안 된다"는 것이다. 그래야 최단 경로를 놓치지 않는다.

### 등장 배경 및 발전 과정

#### 1. 맹목적 탐색의 한계

```
8-퍼즐 탐색 공간:
- 가능한 상태 수: 181,440개
- 평균 해의 깊이: ~22단계

BFS로 탐색 시:
- 탐색해야 할 노드: b^d ≈ 3^22 ≈ 310억 개 (실제론 중복 제거로 줄어듦)
- 메모리: 수 GB 필요

A* (맨해튼 거리)로 탐색 시:
- 탐색 노드: 평균 수천 개
- 메모리: 수 MB
- 속도: 수십 배~수백 배 향상
```

#### 2. 휴리스틱의 수학적 기초

1968년 Hart, Nilsson, Raphael이 A* 알고리즘을 발표하며 휴리스틱 탐색의 이론적 기초를 확립:

- **f(n) = g(n) + h(n)**: 평가 함수
- **g(n)**: 시작점에서 n까지의 실제 비용
- **h(n)**: n에서 목표까지의 추정 비용
- **허용성 증명**: h(n)이 허용적이면 A*는 최적해를 찾음

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|----------|------|
| **휴리스틱 함수** | 목표까지 예상 비용 | 거리 계산, 패턴 매칭 | h(n) | 예상 도착 시간 |
| **평가 함수** | 노드 우선순위 | f(n) = g(n) + h(n) | f(n) | 종합 점수 |
| **우선순위 큐** | 프론티어 관리 | 최소 f값 노드 우선 | Min-Heap | 대기열 |
| **상태 확장** | 자식 노드 생성 | 연산자 적용 | Expand | 다음 단계 |
| **중복 제거** | 효율성 확보 | 방문 확인, 비용 갱신 | Closed List | 방문 기록 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              A* 알고리즘 동작 다이어그램                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [탐색 공간]                              [A* 탐색 과정]

         S (g=0, h=10, f=10)                 단계 1: S 확장
        / \                                   f(S) = 0 + 10 = 10
       /   \                                  프론티어: [S]
      A     B
   (g=3,  (g=4,                             단계 2: A, B 확장
    h=7,   h=5,                              f(A) = 3 + 7 = 10
    f=10)  f=9)                              f(B) = 4 + 5 = 9 ← 선택
    / \     \                                 프론티어: [(B,9), (A,10)]
   C   D     E
(g=6, (g=7, (g=9,                           단계 3: E 확장
 h=4,  h=3,  h=0,                           f(E) = 9 + 0 = 9
 f=10) f=10) f=9)                            목표! 최단 경로 = S→B→E
                                            비용 = 4 + 5 = 9

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          휴리스틱 함수 비교 (8-퍼즐)                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [초기 상태]          [목표 상태]          휴리스틱 비교

    2 8 3                1 2 3
    1 6 4                4 5 6
    7   5                7 8

    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │  휴리스틱        │  계산 방법                    │  값   │  품질          │
    ├─────────────────────────────────────────────────────────────────────────────────┤
    │  h₁(n) = 0      │  항상 0                       │   0   │  맹목적 (BFS)  │
    │  h₂(n) = 오답수 │  잘못 위치한 타일 수           │   5   │  약함          │
    │  h₃(n) = 맨해튼 │  각 타일의 목표까지 거리 합    │   6   │  중간          │
    │  h₄(n) = 선충돌 │  맨해튼 + 행/열 충돌 보정      │   8   │  강함          │
    └─────────────────────────────────────────────────────────────────────────────────┘

    h₁ ≤ h₂ ≤ h₃ ≤ h₄ 일 때, h₄가 가장 효율적 (동일한 해를 더 적은 노드로 탐색)

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          휴리스틱 품질과 탐색 효율                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    탐색 노드 수
    ↑
    │
    │  ★ 맹목적 (h=0)
    │   ╲
    │    ╲  h₁ (약한 휴리스틱)
    │     ╲
    │      ╲  h₂ (중간 휴리스틱)
    │       ╲
    │        ╲  h₃ (강한 휴리스틱)
    │         ╲___________________
    │                              최적 (h=h*)
    └──────────────────────────────────→ 휴리스틱 정확도

    휴리스틱이 정확할수록 탐색 노드 수가 급격히 감소
```

### 심층 동작 원리

**① A* 알고리즘 (최적 탐색)**

```python
import heapq
from typing import List, Tuple, Optional, Set, Dict

def astar_search(
    graph: Dict,
    start,
    goal,
    heuristic
) -> Optional[Tuple[List, float]]:
    """
    A* 알고리즘

    f(n) = g(n) + h(n)
    - g(n): 시작점에서 n까지의 실제 비용
    - h(n): n에서 목표까지의 추정 비용 (휴리스틱)
    - f(n): n을 경유하는 경로의 총 추정 비용

    최적성 조건:
    - h(n)이 허용적 (Admissible): h(n) ≤ h*(n) for all n
    - h(n)이 일관적 (Consistent): h(n) ≤ c(n,n') + h(n')

    시간복잡도: O(b^d) (휴리스틱 품질에 따라 크게 감소)
    공간복잡도: O(b^d)
    """

    # 우선순위 큐: (f값, g값, 카운터, 노드, 경로)
    counter = 0
    open_set = [(heuristic(start, goal), 0, counter, start, [start])]

    # 방문한 노드와 그때의 최소 g값
    g_scores: Dict = {start: 0}

    # 닫힌 집합 (완전히 확장된 노드)
    closed_set: Set = set()

    while open_set:
        f, g, _, node, path = heapq.heappop(open_set)

        # 이미 더 좋은 경로로 처리되었으면 스킵
        if node in closed_set:
            continue

        # 목표 확인
        if node == goal:
            return path, g

        closed_set.add(node)

        # 확장
        for neighbor, edge_cost in graph.get(node, {}).items():
            if neighbor in closed_set:
                continue

            tentative_g = g + edge_cost

            # 더 나은 경로 발견
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                h = heuristic(neighbor, goal)
                f = tentative_g + h

                counter += 1
                heapq.heappush(open_set, (f, tentative_g, counter, neighbor, path + [neighbor]))

    return None  # 해 없음
```

**② Greedy Best-First Search (탐욕적 탐색)**

```python
def greedy_best_first_search(
    graph: Dict,
    start,
    goal,
    heuristic
) -> Optional[List]:
    """
    Greedy Best-First Search

    f(n) = h(n) (휴리스틱만 사용)

    특징:
    - 최적성 보장 없음
    - 매우 빠름 (휴리스틱이 좋을 때)
    - 지역 최적해에 갇힐 수 있음
    """

    counter = 0
    open_set = [(heuristic(start, goal), counter, start, [start])]
    visited: Set = {start}

    while open_set:
        _, _, node, path = heapq.heappop(open_set)

        if node == goal:
            return path

        for neighbor in graph.get(node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                h = heuristic(neighbor, goal)
                counter += 1
                heapq.heappush(open_set, (h, counter, neighbor, path + [neighbor]))

    return None
```

**③ IDA* (Iterative Deepening A*)**

```python
def ida_star(start, goal, heuristic, get_neighbors, cost):
    """
    IDA* (Iterative Deepening A*)

    A*의 완전성/최적성 + 반복 심화의 메모리 효율성

    공간복잡도: O(d) (매우 효율적)
    """

    def search(path, g, threshold):
        node = path[-1]
        f = g + heuristic(node, goal)

        if f > threshold:
            return f, None  # 임계값 초과

        if node == goal:
            return f, path  # 해 발견

        min_threshold = float('inf')

        for neighbor in get_neighbors(node):
            if neighbor not in path:  # 순환 방지
                new_path = path + [neighbor]
                new_g = g + cost(node, neighbor)

                result_t, result_path = search(new_path, new_g, threshold)

                if result_path is not None:
                    return result_t, result_path

                min_threshold = min(min_threshold, result_t)

        return min_threshold, None

    # 반복 심화
    threshold = heuristic(start, goal)
    path = [start]

    while True:
        result_t, result_path = search(path, 0, threshold)

        if result_path is not None:
            return result_path

        if result_t == float('inf'):
            return None  # 해 없음

        threshold = result_t  # 임계값 증가
```

**④ 대표적 휴리스틱 함수들**

```python
# 8-퍼즐 / 15-퍼즐 휴리스틱

def hamming_distance(state, goal) -> int:
    """오답 타일 수 (Hamming Distance)"""
    return sum(1 for s, g in zip(state, goal) if s != g and s != 0)

def manhattan_distance(state, goal, n=3) -> int:
    """맨해튼 거리"""
    distance = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        goal_idx = goal.index(tile)
        cur_row, cur_col = i // n, i % n
        goal_row, goal_col = goal_idx // n, goal_idx % n
        distance += abs(cur_row - goal_row) + abs(cur_col - goal_col)
    return distance

def linear_conflict(state, goal, n=3) -> int:
    """선형 충돌 (맨해튼 + 보정)"""
    md = manhattan_distance(state, goal, n)
    conflict = 0

    # 행 충돌 검사
    for row in range(n):
        for i in range(n):
            for j in range(i + 1, n):
                idx1, idx2 = row * n + i, row * n + j
                tile1, tile2 = state[idx1], state[idx2]

                if tile1 == 0 or tile2 == 0:
                    continue

                goal_row1 = goal.index(tile1) // n
                goal_row2 = goal.index(tile2) // n

                # 같은 행에 있어야 하는데 순서가 반대면 충돌
                if goal_row1 == row and goal_row2 == row:
                    goal_col1 = goal.index(tile1) % n
                    goal_col2 = goal.index(tile2) % n
                    if goal_col1 > goal_col2:
                        conflict += 2

    # 열 충돌 검사 (유사)

    return md + conflict

# 그래프/지도 휴리스틱

def euclidean_distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """유클리드 거리"""
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

def manhattan_distance_2d(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """2D 맨해튼 거리 (그리드)"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def chebyshev_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """체비쇼프 거리 (8방향 이동)"""
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 휴리스틱 탐색 알고리즘

| 알고리즘 | 평가함수 | 최적성 | 완전성 | 메모리 | 용도 |
|---------|---------|--------|--------|--------|------|
| **A*** | f=g+h | Yes* | Yes | O(b^d) | 범용 최적 탐색 |
| **IDA*** | f=g+h | Yes* | Yes | O(d) | 메모리 제약 |
| **Greedy** | f=h | No | Yes | O(b^d) | 빠른 근사 |
| **Weighted A*** | f=g+wh | No** | Yes | O(b^d) | 속도 vs 최적성 |

*h(n)이 허용적일 때
**w > 1이면 w-근사해 보장 (최적해의 w배 이내)

### 휴리스틱 품질 비교 (8-퍼즐)

| 휴리스틱 | 상대 오차 | 평균 노드 수 | 계산 비용 |
|---------|----------|-------------|----------|
| h=0 (BFS) | ∞ | ~100,000 | O(1) |
| 오답 수 | ~2-3x | ~10,000 | O(n²) |
| 맨해튼 | ~1.5x | ~1,000 | O(n²) |
| 선형충돌 | ~1.2x | ~500 | O(n³) |
| 패턴 DB | ~1.0x | ~100 | O(1) 조회 |

### 과목 융합 관점

#### 휴리스틱 탐색 × 머신러닝

- **휴리스틱 학습**: 신경망으로 휴리스틱 함수 학습
- **AlphaZero**: 뉴럴 네트워크 + MCTS로 휴리스틱 학습
- **Deep A***: GNN으로 그래프 휴리스틱 학습

#### 휴리스틱 탐색 × 로보틱스

- **RRT***: 샘플링 기반 최적 경로 탐색
- **Hybrid A***: 연속 공간 + 이산 탐색

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

#### 시나리오 1: 네비게이션 경로 탐색

**문제**: 전국 도로망에서 최단/최적 경로 찾기 (수천만 노드)

**전략**:
1. **계층적 휴리스틱**: 고속도로 → 국도 → 지방도
2. **Landmark 휴리스틱**: 주요 지점까지의 거리 미리 계산
3. **양방향 A***: 출발지와 목적지에서 동시 탐색
4. **결과**: 평균 탐색 시간 < 100ms

#### 시나리오 2: 로봇 팔 모션 플래닝

**문제**: 6자유도 로봇 팔의 충돌 없는 경로

**전략**:
1. **RRT* + 휴리스틱**: 목표 방향으로의 거리
2. **Lazy A***: 충돌 검사 지연
3. **결과**: 실시간 모션 생성 (< 10ms)

#### 시나리오 3: 비디오 게임 NPC

**문제**: 실시간 경로 찾기 (60 FPS)

**전략**:
1. **Weighted A*** (w=1.5): 속도 우선
2. **경로 캐싱**: 자주 사용하는 경로 저장
3. **시간 예산**: 프레임당 최대 2ms만 탐색
4. **결과**: CPU 3%, 자연스러운 이동

### 도입 시 고려사항

- [ ] **휴리스틱 선택**: 문제 특성에 맞는 휴리스틱 설계
- [ ] **허용성 검증**: 휴리스틱이 실제 비용 과대평가 안 함
- [ ] **메모리 vs 속도**: A* vs IDA* 선택
- [ ] **실시간성**: Weighted A* 또는 시간 제한

### 안티패턴

1. **비허용적 휴리스틱**: h(n) > h*(n) → 최적해 놓침
2. **과도한 휴리스틱 계산**: h(n) 계산이 탐색보다 느림
3. **불일치 휴리스틱**: 일관성 없으면 재오픈 빈번

---

## V. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | BFS | A* (h₁) | A* (h₂) | A* (h₃) |
|------|-----|---------|---------|---------|
| **평균 노드** | 100,000 | 10,000 | 1,000 | 100 |
| **탐색 시간** | 10s | 1s | 0.1s | 0.01s |
| **최적성** | Yes | Yes | Yes | Yes |
| **메모리** | 높음 | 높음 | 높음 | 높음 |

### 미래 전망

1. **딥러닝 기반 휴리스틱**: 문제별 최적 휴리스틱 자동 학습
2. **양자 A***: 양자 중첩으로 병렬 탐색
3. **하이브리드 방식**: 샘플링 + 휴리스틱 결합

---

## 📌 관련 개념 맵

- [A* 알고리즘](./13_astar.md) - 대표적 휴리스틱 탐색
- [맹목적 탐색](./11_uninformed_search.md) - 휴리스틱 없는 탐색
- [상태 공간 탐색](./10_state_space_search.md) - 문제 해결 프레임워크
- [강화학습](../1_dl/reinforcement_learning.md) - 학습 기반 의사결정

---

## 👶 어린이를 위한 3줄 비유

**1. 휴리스틱 탐색은 지도를 보고 길을 찾는 거예요.** 눈 가고 막연히 걷는 게 아니라, "목적지까지 직선 거리가 3km야, 그러니 이쪽으로 가자!"라고 추측하며 걷는 거예요.

**2. 좋은 휴리스틱은 정확한 추측이에요.** "직선 거리 3km면 실제로도 3~4km 걸릴 거야"라고 생각하면 최단 경로를 찾을 수 있어요. 하지만 "실제로 3km인데 10km라고 추측하면" 엉뚱한 길로 갈 수 있어요.

**3. 덕분에 훨씬 빠르게 목적지에 도착해요.** 모든 길을 다 가볼 필요 없이, 목적지 방향으로 똑똑하게 이동하니까요. 내비게이션이 최적 경로를 찾는 것도 이 원리를 사용해요!
