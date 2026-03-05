+++
title = "맹목적 탐색 (Uninformed Search / Blind Search)"
date = "2026-03-05"
[extra]
categories = "studynotes-ai"
+++

# 맹목적 탐색 (Uninformed Search / Blind Search)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 맹목적 탐색은 문제의 도메인 지식이나 휴리스틱 없이, 오직 상태 공간의 구조만을 활용하여 체계적으로 탐색하는 전략으로, DFS(깊이 우선), BFS(너비 우선), UCS(균일 비용) 등의 방식이 있다.
> 2. **가치**: 구현의 단순성과 문제 독립성으로 인해 모든 탐색 문제에 범용적으로 적용 가능하며, BFS는 최단 경로를, DFS는 메모리 효율성을, UCS는 가중 그래프에서의 최적 경로를 보장한다.
> 3. **융합**: 맹목적 탐색은 휴리스틱 탐색(A*, IDA*)의 기반이 되며, 반복 심화(Iterative Deepening), 양방향 탐색(Bidirectional Search) 등으로 최적화되어 실제 시스템에서 여전히 핵심 알고리즘으로 활용된다.

---

## I. 개요 (Context & Background)

### 개념 정의

맹목적 탐색(Uninformed Search), 또는 무정보 탐색(Blind Search)은 **탐색 과정에서 문제에 특화된 지식이나 휴리스틱 정보를 전혀 사용하지 않고, 상태 공간의 구조적 특성만을 이용하여 체계적으로 탐색하는 방식**이다. 이는 휴리스틱 탐색(Informed Search)과 대비되는 개념으로, 목표 상태가 어디에 있는지, 어떤 경로가 더 유망한지에 대한 정보 없이 오직 탐색 전략에만 의존한다.

주요 맹목적 탐색 알고리즘:

1. **깊이 우선 탐색 (DFS, Depth-First Search)**: 가장 깊은 노드부터 확장 (LIFO)
2. **너비 우선 탐색 (BFS, Breadth-First Search)**: 가장 얕은 노드부터 확장 (FIFO)
3. **균일 비용 탐색 (UCS, Uniform Cost Search)**: 경로 비용이 가장 낮은 노드부터 확장
4. **깊이 제한 탐색 (DLS, Depth-Limited Search)**: 깊이에 제한을 둔 DFS
5. **반복 심화 탐색 (IDS, Iterative Deepening Search)**: 깊이 제한을 점진적으로 증가

### 💡 비유: "눈 가리고 미로 찾기"

맹목적 탐색을 **"눈을 가린 채 미로에서 출구 찾기"**에 비유할 수 있다.

**맹목적 탐색 = 눈 가린 미로 탐색**: 출구가 어디에 있는지 전혀 모르는 상태에서, 오직 벽을 더듬으며 이동해야 한다. "출구가 동쪽에 있을 것 같다"라는 추측도 할 수 없다. 오직 "이 길은 가봤으니 다른 길을 가보자"라는 식의 체계적인 방문만 가능하다.

**DFS 전략 = 한 길만 판다**: 한 갈림길에서 한 방향을 선택하면, 막다른 골목이 나올 때까지 계속 그 길만 간다. 막히면 바로 직전 갈림길로 돌아와서 다른 방향을 시도한다. 메모리는 적게 쓰지만, 출구가 바로 옆에 있어도 멀리 돌아갈 수 있다.

**BFS 전략 = 동시에 여러 길**: 모든 갈릴길을 동시에 조금씩 확장해 나간다. 마치 물이 퍼지듯이 모든 방향으로 균등하게 진행한다. 출구가 얕은 곳에 있으면 빨리 찾지만, 기억해야 할 길이 너무 많아진다.

**UCS 전략 = 비용 따져가기**: 각 길마다 이동 비용이 다르다면, 지금까지 가장 적은 비용이 든 길부터 우선적으로 확장한다. 통행료가 비싼 고속도로보다는 무료 도로를 먼저 탐색하는 식이다.

### 등장 배경 및 발전 과정

#### 1. 기존 기술의 치명적 한계점

**무작위 탐색의 비효율성**이 근본적 문제였다. 초기 AI 연구에서 문제 해결을 위해 무작위로 상태를 시도하는 방식은 다음과 같은 치명적 문제에 직면했다:

```
무작위 탐색의 문제점:

1. 중복 방문:
   - 같은 상태를 수없이 다시 방문
   - 이미 실패한 경로를 또 시도

2. 무한 루프:
   - 상태 A → B → C → A ... 순환
   - 영원히 빠져나오지 못함

3. 불완전성:
   - 해가 존재해도 찾을 확률이 낮음
   - 언제 끝날지 알 수 없음

4. 비최적성:
   - 찾은 해가 최적인지 알 수 없음
   - 바로 옆의 해를 놓치고 먼 길을 찾을 수 있음
```

#### 2. 패러다임의 혁신적 전환: 체계적 탐색

**"무식하지만 체계적으로 탐색하라"**는 통찰이 혁신을 가져왔다. 도메인 지식이 없더라도, 탐색 자체를 체계적으로 수행하면:

- **완전성(Completeness)**: 해가 존재하면 반드시 찾음
- **최적성(Optimality)**: 찾은 해가 최적임을 보장
- **효율성(Efficiency)**: 중복을 제거하여 탐색 공간 축소

#### 3. 시장 및 산업에서의 비즈니스적 요구사항

- **네트워크 라우팅**: 최단 경로 탐색 (BFS/UCS 기반)
- **소셜 네트워크**: 친구의 친구 찾기 (BFS)
- **파일 시스템**: 디렉토리 구조 탐색 (DFS)
- **웹 크롤링**: 페이지 링크 순회 (BFS/DFS)
- **게임 AI**: 맵 탐색 및 경로 찾기

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|----------|------|
| **프론티어** | 탐색 대기 노드 | 스택(DFS), 큐(BFS), 우선순위큐(UCS) | Open List | 대기열 |
| **방문 집합** | 중복 방지 | 해시셋, 비트마스크 | Closed List | 방문 기록 |
| **상태 확장** | 자식 노드 생성 | 연산자 적용 | Expand | 다음 단계 |
| **경로 추적** | 해 경로 복원 | 부모 포인터 | Backtracking | 발자취 |
| **종료 조건** | 탐색 완료 판단 | 목표 테스트, 프론티어 공실 | Goal Test | 도착 확인 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          맹목적 탐색 전략 비교 다이어그램                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [그래프 구조]                    [DFS 탐색 순서]              [BFS 탐색 순서]

         A                              A (1)                       A (1)
       / | \                            |                          / | \
      B  C  D                           B (2)                    B  C  D (2,3,4)
     / \    \                           |                       / \    \
    E   F    G                          E (3)                  E   F    G (5,6,7)
        |    |                          |                          |
        H    I                          F (4)                      H (8)
           /                            |                          |
          J                             H (5)                      I (9)
                                        |
                                        G (6)
                                        |
                                        I (7)
                                        |
                                        J (8)

    DFS: A→B→E→F→H→G→I→J (깊이 우선, 스택)
    BFS: A→B→C→D→E→F→G→H→I→J (너비 우선, 큐)

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              탐색 알고리즘별 프론티어 변화                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    DFS (LIFO 스택):                    BFS (FIFO 큐):

    단계  프론티어          방문         단계  프론티어          방문
    ────  ────────────────  ────        ────  ────────────────  ────
    0     [A]               {}          0     [A]               {}
    1     [D,C,B]           {A}         1     [B,C,D]           {A}
    2     [D,C,F,E]         {A,B}       2     [C,D,E,F]         {A,B}
    3     [D,C,F]           {A,B,E}     3     [D,E,F,G]         {A,B,C}
    4     [D,C,H]           {A,B,E,F}   4     [E,F,G]           {A,B,C,D}
    5     [D,C]             {...,H}     5     [F,G]             {...,E}
    6     [D,G]             {...,C}     6     [G,H]             {...,F}
    7     [D,I]             {...,G}     7     [H,I]             {...,G}
    8     [D,J]             {...,I}     8     [I,J]             {...,H}
    9     [D]               {...,J}     9     [J]               {...,I}
    10    []                {...,D}     10    []                {...,J}

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          균일 비용 탐색 (UCS) - 가중 그래프                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [가중 그래프]                      [UCS 탐색 순서]

         A ──4── B                       단계  노드  누적비용  프론티어(비용)
         │       │                       ────  ────  ────────  ───────────────
         2       3                       0     A     0        [(A,0)]
         │       │                       1     -     -        [(B,4), (C,2)]
         C ──5── D                       2     C     2        [(B,4), (D,7)]
              /   \                      3     B     4        [(D,7), (E,9)]
             1     6                     4     D     7        [(E,9), (F,13)]
            /       \                    5     E     8        [(F,13)] ← 목표!
           E ──1──── F

    최단 경로: A → C → D → E (비용: 2+5+1=8)
    (BFS는 A→B→D→E 경로 선택했을 것: 비용 4+3+1=8, 동일하지만 BFS는 비용 고려 안함)
```

### 심층 동작 원리 (5단계 알고리즘 분석)

**① 깊이 우선 탐색 (DFS)**

```python
def depth_first_search(graph, start, goal):
    """
    깊이 우선 탐색 (DFS)
    - LIFO 스택 사용
    - 완전성: 무한 경로 없을 때만 보장
    - 최적성: 보장 안됨
    - 시간복잡도: O(b^m)
    - 공간복잡도: O(b*m)
    """
    stack = [(start, [start])]  # (노드, 경로)
    visited = set()

    while stack:
        node, path = stack.pop()  # LIFO

        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path  # 해 발견

        # 자식 노드를 스택에 추가 (역순으로 추가하여 왼쪽 자식부터 방문)
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None  # 해 없음

# 특징:
# 1. 메모리 효율적: 현재 경로만 저장
# 2. 깊은 해에 빠르게 도달
# 3. 무한 깊이 경로에서 실패 가능
# 4. 최단 경로 보장 없음
```

**② 너비 우선 탐색 (BFS)**

```python
from collections import deque

def breadth_first_search(graph, start, goal):
    """
    너비 우선 탐색 (BFS)
    - FIFO 큐 사용
    - 완전성: 항상 보장
    - 최적성: 균일 비용일 때 보장
    - 시간복잡도: O(b^d)
    - 공간복잡도: O(b^d)
    """
    queue = deque([(start, [start])])  # (노드, 경로)
    visited = set([start])

    while queue:
        node, path = queue.popleft()  # FIFO

        if node == goal:
            return path  # 해 발견 (최단 경로)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # 해 없음

# 특징:
# 1. 최단 경로 보장 (균일 비용)
# 2. 얕은 해에 최적
# 3. 메모리 집약적: 모든 노드 저장
# 4. 완전한 탐색 보장
```

**③ 균일 비용 탐색 (UCS)**

```python
import heapq

def uniform_cost_search(graph, start, goal):
    """
    균일 비용 탐색 (UCS)
    - 우선순위 큐 사용 (비용 기준)
    - 완전성: 항상 보장 (비용 > 0)
    - 최적성: 항상 보장
    - 시간복잡도: O(b^(C*/ε))
    - 공간복잡도: O(b^(C*/ε))
    """
    # (누적비용, 카운터, 노드, 경로)
    counter = 0
    pq = [(0, counter, start, [start])]
    visited = {}  # 노드 → 최소 비용

    while pq:
        cost, _, node, path = heapq.heappop(pq)

        # 이미 더 낮은 비용으로 방문했으면 스킵
        if node in visited and visited[node] <= cost:
            continue

        visited[node] = cost

        if node == goal:
            return path, cost  # 최적 경로 발견

        for neighbor, edge_cost in graph.get(node, {}).items():
            new_cost = cost + edge_cost

            if neighbor not in visited or visited[neighbor] > new_cost:
                counter += 1
                heapq.heappush(pq, (new_cost, counter, neighbor, path + [neighbor]))

    return None, float('inf')  # 해 없음

# 특징:
# 1. 가중 그래프에서 최적 경로 보장
# 2. A*의 h(n)=0인 특수한 경우
# 3. 비용이 균일하면 BFS와 동일
```

**④ 깊이 제한 탐색 (DLS)**

```python
def depth_limited_search(graph, start, goal, limit):
    """
    깊이 제한 탐색 (DLS)
    - DFS에 깊이 제한 추가
    - 무한 경로 문제 해결
    """
    def recursive_dls(node, depth, path, visited):
        if node == goal:
            return path

        if depth == 0:
            return None  # 깊이 한계 도달

        visited.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                result = recursive_dls(neighbor, depth - 1, path + [neighbor], visited)
                if result is not None:
                    return result

        visited.remove(node)  # 백트래킹
        return None

    return recursive_dls(start, limit, [start], set())
```

**⑤ 반복 심화 탐색 (IDS)**

```python
def iterative_deepening_search(graph, start, goal, max_depth=100):
    """
    반복 심화 탐색 (IDS / IDDFS)
    - DFS의 메모리 효율 + BFS의 완전성/최적성
    - 시간복잡도: O(b^d)
    - 공간복잡도: O(b*d)
    """
    for depth in range(max_depth):
        result = depth_limited_search(graph, start, goal, depth)

        if result is not None:
            return result  # 해 발견

        # 선택적: 깊이별로 노드 수 카운트하여 조기 종료 판단 가능

    return None  # max_depth 내에 해 없음

# 특징:
# 1. BFS의 완전성/최적성 + DFS의 메모리 효율성
# 2. 상위 레벨 중복 탐색 (오버헤드 적음)
# 3. 실제로 매우 효율적인 알고리즘
```

### 핵심 알고리즘: 통합 맹목적 탐색 프레임워크

```python
from abc import ABC, abstractmethod
from collections import deque
import heapq
from typing import Generic, TypeVar, Optional, List, Tuple, Set

T = TypeVar('T')

class SearchStrategy(ABC, Generic[T]):
    """탐색 전략 추상 클래스"""

    @abstractmethod
    def create_frontier(self, initial_state: T) -> None:
        """프론티어 초기화"""
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """프론티어가 비었는지 확인"""
        pass

    @abstractmethod
    def get_next(self) -> Tuple[T, float, List[T]]:
        """다음 탐색 노드 반환 (상태, 비용, 경로)"""
        pass

    @abstractmethod
    def add(self, state: T, cost: float, path: List[T]) -> None:
        """프론티어에 노드 추가"""
        pass

class DFSStrategy(SearchStrategy[T]):
    """DFS 전략 (LIFO 스택)"""
    def __init__(self):
        self.stack = []

    def create_frontier(self, initial_state: T):
        self.stack = [(initial_state, 0, [initial_state])]

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def get_next(self) -> Tuple[T, float, List[T]]:
        return self.stack.pop()

    def add(self, state: T, cost: float, path: List[T]):
        self.stack.append((state, cost, path))

class BFSStrategy(SearchStrategy[T]):
    """BFS 전략 (FIFO 큐)"""
    def __init__(self):
        self.queue = deque()

    def create_frontier(self, initial_state: T):
        self.queue.append((initial_state, 0, [initial_state]))

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def get_next(self) -> Tuple[T, float, List[T]]:
        return self.queue.popleft()

    def add(self, state: T, cost: float, path: List[T]):
        self.queue.append((state, cost, path))

class UCSStrategy(SearchStrategy[T]):
    """UCS 전략 (우선순위 큐)"""
    def __init__(self):
        self.counter = 0
        self.heap = []

    def create_frontier(self, initial_state: T):
        self.counter = 0
        self.heap = [(0, self.counter, initial_state, [initial_state])]

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def get_next(self) -> Tuple[T, float, List[T]]:
        cost, _, state, path = heapq.heappop(self.heap)
        return state, cost, path

    def add(self, state: T, cost: float, path: List[T]):
        self.counter += 1
        heapq.heappush(self.heap, (cost, self.counter, state, path))

class GraphSearch(Generic[T]):
    """그래프 탐색 엔진"""

    def __init__(self, graph: dict, strategy: SearchStrategy[T]):
        self.graph = graph
        self.strategy = strategy

    def search(self, start: T, goal: T) -> Optional[List[T]]:
        """일반화된 그래프 탐색"""

        self.strategy.create_frontier(start)
        visited: Set[T] = set()
        best_cost: dict[T, float] = {start: 0}

        while not self.strategy.is_empty():
            state, cost, path = self.strategy.get_next()

            # 이미 더 좋은 경로로 방문했으면 스킵
            if state in visited and best_cost.get(state, float('inf')) <= cost:
                continue

            visited.add(state)
            best_cost[state] = cost

            # 목표 확인
            if state == goal:
                return path

            # 확장
            for neighbor, edge_cost in self.graph.get(state, {}).items():
                new_cost = cost + edge_cost

                if neighbor not in visited or best_cost.get(neighbor, float('inf')) > new_cost:
                    self.strategy.add(neighbor, new_cost, path + [neighbor])

        return None

# 사용 예시
if __name__ == "__main__":
    # 가중 그래프 정의
    graph = {
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'D': 3},
        'C': {'A': 2, 'D': 5},
        'D': {'B': 3, 'C': 5, 'E': 1, 'F': 6},
        'E': {'D': 1, 'F': 1},
        'F': {'D': 6, 'E': 1}
    }

    # DFS
    dfs_search = GraphSearch(graph, DFSStrategy())
    dfs_path = dfs_search.search('A', 'E')
    print(f"DFS 경로: {dfs_path}")

    # BFS
    bfs_search = GraphSearch(graph, BFSStrategy())
    bfs_path = bfs_search.search('A', 'E')
    print(f"BFS 경로: {bfs_path}")

    # UCS
    ucs_search = GraphSearch(graph, UCSStrategy())
    ucs_path = ucs_search.search('A', 'E')
    print(f"UCS 경로: {ucs_path}")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 맹목적 탐색 알고리즘

| 속성 | DFS | BFS | UCS | DLS | IDS |
|------|-----|-----|-----|-----|-----|
| **완전성** | No* | Yes | Yes** | No | Yes |
| **최적성** | No | Yes*** | Yes | No | Yes*** |
| **시간복잡도** | O(b^m) | O(b^d) | O(b^(C*/ε)) | O(b^ℓ) | O(b^d) |
| **공간복잡도** | O(bm) | O(b^d) | O(b^(C*/ε)) | O(bℓ) | O(bd) |
| **자료구조** | 스택 | 큐 | 우선순위큐 | 스택 | 스택 |
| **용도** | 깊은 해 | 얕은 해 | 가중 그래프 | 제한된 깊이 | 일반적 |

*유한 그래프에서만 완전
**비용 > 0일 때만
***균일 비용일 때만

b: 분기율, d: 해의 깊이, m: 최대 깊이, ℓ: 깊이 제한
C*: 최적해 비용, ε: 최소 비용

### 과목 융합 관점 분석

#### 맹목적 탐색 × 자료구조

- **스택/큐 구현**: 연결리스트 vs 배열 기반 성능 비교
- **해시셋 최적화**: 방문 집합의 메모리-시간 트레이드오프
- **우선순위 큐**: 이진 힙 vs 피보나치 힙

#### 맹목적 탐색 × 운영체제

- **파일 시스템 탐색**: 디렉토리 DFS/BFS 순회
- **메모리 관리**: 탐색 중 메모리 할당/해제
- **프로세스 스케줄링**: 탐색 작업의 우선순위

#### 맹목적 탐색 × 네트워크

- **라우팅 프로토콜**: OSPF (UCS 기반), RIP (거리 벡터)
- **네트워크 토폴로지**: 스패닝 트리 (BFS 기반)
- **패킷 전파**: 브로드캐스트 (BFS)

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

#### 시나리오 1: 소셜 네트워크 친구 추천

**문제**: 사용자의 2~3단계 이내 친구 중 추천 대상 찾기

**전략적 의사결정**:
- **BFS 선택**: 2~3단계 내 모든 사용자 균등 탐색
- **양방향 BFS**: 사용자와 후보군에서 동시 시작
- **결과**: 탐색 시간 60% 단축, 추천 품질 유지

#### 시나리오 2: 게임 맵 탐색

**문제**: 실시간 전략 게임에서 유닛 이동 경로 (60 FPS 유지)

**전략적 의사결정**:
- **IDS 선택**: 메모리 제한 + 최단 경로 필요
- **깊이 제한 동적 조절**: 프레임 시간에 따라 제한 조정
- **결과**: CPU 점유율 5% 이내, 자연스러운 이동

#### 시나리오 3: 물류 배송 경로

**문제**: 도로별 통행료/시간이 다른 최적 배송 경로

**전략적 의사결정**:
- **UCS 선택**: 비용 기반 최적 경로 필요
- **다목적 확장**: 시간, 비용, 거리 동시 고려
- **결과**: 배송 비용 15% 절감

### 도입 시 고려사항

- [ ] **해의 깊이 예측**: 얕은 해 → BFS, 깊은 해 → DFS/IDS
- [ ] **메모리 제약**: 메모리 제한적 → DFS/IDS
- [ ] **최적성 필요**: 최단/최적 경로 필요 → BFS/UCS
- [ ] **가중 그래프**: 비용이 다르면 → UCS

### 안티패턴

1. **무한 루프 DFS**: 순환 그래프에서 방문 체크 없는 DFS
2. **메모리 폭발 BFS**: 넓은 그래프에서 BFS
3. **비용 무시 BFS**: 가중 그래프에서 BFS로 최적 경로 시도

---

## V. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 무작위 | DFS | BFS | IDS |
|------|--------|-----|-----|-----|
| **완전성** | No | No* | Yes | Yes |
| **최적성** | No | No | Yes** | Yes** |
| **메모리** | 낮음 | 낮음 | 높음 | 낮음 |
| **구현 복잡도** | 낮음 | 낮음 | 낮음 | 중간 |

### 미래 전망

1. **하이브리드 탐색**: 맹목적 + 휴리스틱 결합
2. **병렬 탐색**: 멀티코어 활용한 병렬 BFS/DFS
3. **양자 탐색**: 양자 중첩으로 동시 다중 경로 탐색

---

## 📌 관련 개념 맵

- [A* 알고리즘](./12_astar_algorithm.md) - 휴리스틱 기반 최적 탐색
- [상태 공간 탐색](./10_state_space_search.md) - 문제 해결 프레임워크
- [휴리스틱 탐색](./13_heuristic_search.md) - 정보 기반 탐색
- [그래프 알고리즘](../../5_algorithms/1_graph/) - 그래프 이론 기초

---

## 👶 어린이를 위한 3줄 비유

**1. 맹목적 탐색은 눈 가리고 숨바꼭질하는 거예요.** 친구가 어디 숨었는지 전혀 모르는 상태에서, 한 칸씩 이동하며 찾아야 해요. "아마 저쪽에 있을 거야"라는 추측도 할 수 없어요.

**2. 두 가지 방법이 있어요.** 한 방향으로 끝까지 가보는 방법(깊이 우선), 모든 방향을 동시에 조금씩 늘려가는 방법(너비 우선). 전자는 멀리 있는 친구를 빨리 찾을 수 있고, 후자는 가까이 있는 친구를 확실히 찾아요.

**3. 이 방법들은 나중에 더 똑똑한 탐색의 기본이 돼요.** 지도를 보고 찾는 방법을 배우기 전에, 먼저 눈 가리고 찾는 법부터 연습하는 것이죠. 단순하지만 모든 탐색의 시작점이에요!
