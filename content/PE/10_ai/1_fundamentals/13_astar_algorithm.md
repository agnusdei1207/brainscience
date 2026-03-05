+++
title = "A* (A-Star) 알고리즘"
date = "2026-03-05"
[extra]
categories = "studynotes-ai"
+++

# A* (A-Star) 알고리즘

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: A* 알고리즘은 1968년 Hart, Nilsson, Raphael이 제안한 최적 경로 탐색 알고리즘으로, 평가 함수 f(n) = g(n) + h(n)을 통해 현재까지의 실제 비용과 목표까지의 예상 비용을 결합하여 최적해를 효율적으로 탐색한다.
> 2. **가치**: 허용적(Admissible)이고 일관적(Consistent)인 휴리스틱을 사용할 때 최적성을 보장하며, 맹목적 탐색 대비 탐색 노드 수를 90% 이상 감소시켜 네비게이션, 게임 AI, 로봇 경로 계획 등에서 표준 알고리즘으로 자리 잡았다.
> 3. **융합**: A*는 D* (동적 환경), Hybrid A* (연속 공간), Weighted A* (속도-정확도 트레이드오프), Bidirectional A* (양방향 탐색) 등으로 확장되어 자율주행, 실시간 로봇 내비게이션, 비디오 게임 등에서 핵심적으로 활용된다.

---

## I. 개요 (Context & Background)

### 개념 정의

A*(A-Star) 알고리즘은 **그래프에서 최단 경로를 찾는 최적의 휴리스틱 탐색 알고리즘**으로, 다음 세 가지 핵심 개념으로 구성된다:

1. **g(n) - 실제 비용**: 시작점에서 현재 노드 n까지의 누적된 실제 경로 비용
2. **h(n) - 휴리스틱 추정**: 현재 노드 n에서 목표 노드까지의 예상 비용
3. **f(n) - 평가 함수**: f(n) = g(n) + h(n), 노드 n을 경유하는 전체 경로의 추정 비용

A*는 f(n)이 가장 작은 노드부터 우선적으로 확장하며, 이는 "가장 유망한 경로"를 먼저 탐색한다는 의미다.

### 💡 비유: "스마트한 내비게이션"

A* 알고리즘을 **"완벽한 추측 능력을 가진 내비게이션"**에 비유할 수 있다.

**기본 내비게이션 = 다익스트라**: "지금까지 온 거리가 가장 짧은 길부터 탐색해 보자." 출발지에서 조금씩 퍼져나가며 모든 방향을 동등하게 탐색한다. 목적지가 바로 남쪽에 있어도 북쪽도 똑같이 탐색한다.

**A* 내비게이션 = 스마트 추측**: "지금까지 10km 왔고, 목적지까지 직선 거리가 5km야. 그러니 총 15km 정도 걸릴 거야. 이게 가장 짧아 보이는 길이네!" 목적지 방향을 고려하여 유망한 길을 먼저 탐색한다.

**휴리스틱의 역할**: "직선 거리"라는 추측이 정확할수록, 즉 h(n)이 실제 남은 거리에 가까울수록 더 빠르게 목적지에 도달한다. 하지만 추측이 실제보다 크면("직선 거리가 10km인데 실제로는 5km밖에 안 되는 길") 최단 경로를 놓칠 수 있다. 그래서 A*는 항상 "실제보다 작거나 같게" 추측해야 한다.

### 등장 배경 및 발전 과정

#### 1. 기존 알고리즘의 한계

**다익스트라 알고리즘의 비효율성**:
- 1956년 에츠허르 다익스트라가 제안
- 목표 방향에 대한 정보 없이 모든 방향을 동등하게 탐색
- f(n) = g(n) (휴리스틱 h(n) = 0인 A*의 특수한 경우)
- 목표가 명확히 알려진 경우에도 불필요한 탐색 수행

```
다이스트라 vs A* 탐색 공간 비교:

    S = 시작, G = 목표

    다익스트라:               A* (휴리스틱 사용):
    ┌─────────────────┐      ┌─────────────────┐
    │ ○ ○ ○ ○ ○ ○ ○ ○ │      │ ○ ○ ○           │
    │ ○ ○ ○ ○ ○ ○ ○ ○ │      │ ○ ○ ○ ○         │
    │ ○ ○ S ○ ○ ○ ○ ○ │      │ ○ S ○ ○ ○       │
    │ ○ ○ ○ ○ ○ ○ ○ ○ │      │     ○ ○ ○ G     │
    │ ○ ○ ○ ○ ○ ○ ○ G │      │           ○     │
    └─────────────────┘      └─────────────────┘
    (거의 모든 노드 탐색)     (목표 방향 집중 탐색)
```

#### 2. A*의 혁신

1968년, 스탠퍼드 연구소(SRI)의 Hart, Nilsson, Raphael이 A*를 발표:
- **휴리스틱 통합**: 도메인 지식을 탐색에 활용
- **최적성 증명**: 허용적 휴리스틱 하에서 최적해 보장
- **완전성 보장**: 해가 존재하면 반드시 찾음

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|----------|------|
| **OPEN 리스트** | 탐색 대기 노드 | 우선순위 큐 (Min-Heap) | f(n) 기준 정렬 | 대기열 |
| **CLOSED 리스트** | 확장 완료 노드 | 해시셋/딕셔너리 | 중복 방지 | 방문 기록 |
| **g_score** | 시작~n 실제 비용 | 누적 비용 저장 | 최소값 갱신 | 이동 거리 |
| **h_score** | n~목표 추정 비용 | 휴리스틱 함수 | 계산 또는 조회 | 예상 거리 |
| **f_score** | 총 추정 비용 | f = g + h | 우선순위 결정 | 총 점수 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              A* 알고리즘 상세 동작 다이어그램                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [초기화]                                                                [종료 조건]
        │                                                                         ▲
        ▼                                                                         │
    ┌───────────────────────────────────────────────────────────────────────────────┐│
    │                         A* 메인 루프                                           ││
    │                                                                               ││
    │   ┌─────────────────────────────────────────────────────────────────────────┐ ││
    │   │  OPEN 리스트 (우선순위 큐)                                               │ ││
    │   │  ┌─────────────────────────────────────────────────────────────────────┐│ ││
    │   │  │ (f=10,g=0,S) ← pop (최소 f값)                                       ││ ││
    │   │  │ (f=12,g=5,A)                                                        ││ ││
    │   │  │ (f=15,g=7,B)                                                        ││ ││
    │   │  │ ...                                                                 ││ ││
    │   │  └─────────────────────────────────────────────────────────────────────┘│ ││
    │   └─────────────────────────────────────────────────────────────────────────┘ ││
    │                              │                                               ││
    │                              │ pop (f 최소)                                  ││
    │                              ▼                                               ││
    │   ┌─────────────────────────────────────────────────────────────────────────┐ ││
    │   │  현재 노드 n 처리                                                        │ ││
    │   │  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐             │ ││
    │   │  │ 목표 확인    │────▶│ CLOSED 추가   │────▶│  자식 확장   │             │ ││
    │   │  │ n == goal?  │ Yes │              │     │              │             │ ││
    │   │  └──────────────┘     └──────────────┘     └──────────────┘             │ ││
    │   │        │ No                                                           │ ││
    │   └────────┴────────────────────────────────────────────────────────────────┘ ││
    │                              │                                               ││
    │                              │ 각 자식 n'에 대해                             ││
    │                              ▼                                               ││
    │   ┌─────────────────────────────────────────────────────────────────────────┐ ││
    │   │  자식 노드 처리                                                          │ ││
    │   │                                                                         │ ││
    │   │  ┌──────────────────────────────────────────────────────────────────┐   │ ││
    │   │  │  새로운 g 계산: g' = g(n) + cost(n, n')                           │   │ ││
    │   │  │                                                                 │   │ ││
    │   │  │  if n' in CLOSED and g' >= g(n'):                               │   │ ││
    │   │  │      continue  (이미 더 좋은 경로로 방문함)                        │   │ ││
    │   │  │                                                                 │   │ ││
    │   │  │  if n' not in OPEN or g' < g(n'):                               │   │ ││
    │   │  │      g(n') = g'                                                 │   │ ││
    │   │  │      h(n') = heuristic(n', goal)                                │   │ ││
    │   │  │      f(n') = g' + h(n')                                         │   │ ││
    │   │  │      parent(n') = n                                             │   │ ││
    │   │  │      if n' not in OPEN:                                         │   │ ││
    │   │  │          add n' to OPEN                                         │   │ ││
    │   │  └──────────────────────────────────────────────────────────────────┘   │ ││
    │   └─────────────────────────────────────────────────────────────────────────┘ ││
    │                              │                                               ││
    │                              └───────────────────────────────────────────────┘│
    │                                                                               ││
    └───────────────────────────────────────────────────────────────────────────────┘│
                                                                                     │
    [해 없음] ◀──────────────────── OPEN 리스트 공空 ─────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              A* 탐색 예시 (격자 그리드)                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    S = 시작, G = 목표, # = 벽, 숫자 = f값

    초기 상태:                           탐색 진행:

    ┌───┬───┬───┬───┬───┐              ┌───┬───┬───┬───┬───┐
    │ S │   │   │   │   │              │ S │ 4 │ 5 │   │   │
    ├───┼───┼───┼───┼───┤              ├───┼───┼───┼───┼───┤
    │   │ # │ # │   │   │              │ 4 │ # │ # │ 6 │   │
    ├───┼───┼───┼───┼───┤    ────▶     ├───┼───┼───┼───┼───┤
    │   │   │   │   │   │              │ 5 │ 6 │ 6 │ 6 │ 6 │
    ├───┼───┼───┼───┼───┤              ├───┼───┼───┼───┼───┤
    │   │   │   │   │ G │              │   │   │ 7 │ 7 │ G │
    └───┴───┴───┴───┴───┘              └───┴───┴───┴───┴───┘

    최단 경로: S → (0,1) → (1,0) → (2,0) → (2,1) → (2,2) → (2,3) → (3,4) → G
```

### 심층 동작 원리

**① 알고리즘 의사코드**

```python
function A*(start, goal, h):
    """
    A* 알고리즘 의사코드

    입력:
        start: 시작 노드
        goal: 목표 노드
        h: 휴리스틱 함수 h(n, goal)

    출력:
        최단 경로 또는 실패
    """

    # OPEN 리스트: 우선순위 큐 (f값 기준)
    OPEN = PriorityQueue()
    OPEN.add(start, f=0 + h(start, goal))

    # g(n): 시작에서 n까지의 최단 거리
    g_score = {start: 0}

    # f(n): g(n) + h(n)
    f_score = {start: h(start, goal)}

    # 경로 추적용
    came_from = {}

    # CLOSED 리스트: 확장 완료된 노드
    CLOSED = Set()

    while OPEN is not empty:
        # f값이 최소인 노드 선택
        current = OPEN.pop_min()

        # 목표 도달 확인
        if current == goal:
            return reconstruct_path(came_from, current)

        # CLOSED로 이동
        CLOSED.add(current)

        # 자식 노드 확장
        for neighbor in get_neighbors(current):
            # 이미 확장된 노드면 스킵
            if neighbor in CLOSED:
                continue

            # 새로운 g값 계산
            tentative_g = g_score[current] + cost(current, neighbor)

            # 더 나은 경로가 아니면 스킵
            if neighbor in g_score and tentative_g >= g_score[neighbor]:
                continue

            # 경로 갱신
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g
            f_score[neighbor] = tentative_g + h(neighbor, goal)

            # OPEN에 추가 (또는 갱신)
            if neighbor not in OPEN:
                OPEN.add(neighbor, f_score[neighbor])
            else:
                OPEN.update(neighbor, f_score[neighbor])

    return FAILURE  # 경로 없음

function reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.prepend(current)
    return path
```

**② 완전한 Python 구현**

```python
import heapq
from typing import List, Tuple, Dict, Set, Optional, Callable
from dataclasses import dataclass, field

@dataclass(order=True)
class Node:
    """A* 탐색 노드"""
    f_score: float
    g_score: float = field(compare=False)
    node: any = field(compare=False)
    parent: Optional['Node'] = field(default=None, compare=False)

class AStar:
    """A* 알고리즘 구현"""

    def __init__(
        self,
        get_neighbors: Callable,
        cost: Callable,
        heuristic: Callable,
        is_goal: Callable
    ):
        """
        Args:
            get_neighbors: 노드 -> 이웃 노드 리스트 반환
            cost: (노드1, 노드2) -> 비용 반환
            heuristic: (노드, 목표) -> h값 반환
            is_goal: 노드 -> 목표 여부 반환
        """
        self.get_neighbors = get_neighbors
        self.cost = cost
        self.heuristic = heuristic
        self.is_goal = is_goal

    def search(self, start, goal) -> Optional[Tuple[List, float]]:
        """
        A* 탐색 수행

        Returns:
            (경로, 총비용) 또는 None
        """
        # 초기화
        h = self.heuristic(start, goal)
        start_node = Node(f_score=h, g_score=0, node=start)

        # OPEN 리스트 (우선순위 큐)
        open_heap = [start_node]
        open_set = {start: start_node}

        # CLOSED 리스트
        closed_set: Set = set()

        # g_score 딕셔너리 (빠른 조회용)
        g_scores: Dict = {start: 0}

        while open_heap:
            # f값이 최소인 노드 pop
            current = heapq.heappop(open_heap)
            current_node = current.node

            # 이미 처리된 노드면 스킵
            if current_node in closed_set:
                continue

            # 목표 확인
            if self.is_goal(current_node) or current_node == goal:
                return self._reconstruct_path(current), current.g_score

            # CLOSED로 이동
            closed_set.add(current_node)
            del open_set[current_node]

            # 자식 확장
            for neighbor in self.get_neighbors(current_node):
                if neighbor in closed_set:
                    continue

                # 새로운 g값 계산
                tentative_g = current.g_score + self.cost(current_node, neighbor)

                # 더 나은 경로가 아니면 스킵
                if neighbor in g_scores and tentative_g >= g_scores[neighbor]:
                    continue

                # 갱신
                g_scores[neighbor] = tentative_g
                h = self.heuristic(neighbor, goal)
                f = tentative_g + h

                new_node = Node(
                    f_score=f,
                    g_score=tentative_g,
                    node=neighbor,
                    parent=current
                )

                if neighbor in open_set:
                    # 기존 노드 대체 (지연 삭제 방식)
                    open_set[neighbor] = new_node
                else:
                    open_set[neighbor] = new_node

                heapq.heappush(open_heap, new_node)

        return None  # 경로 없음

    def _reconstruct_path(self, node: Node) -> List:
        """경로 복원"""
        path = []
        while node:
            path.append(node.node)
            node = node.parent
        return list(reversed(path))


# 그리드 기반 예시
class GridAStar:
    """2D 그리드에서의 A* 구현"""

    def __init__(self, grid: List[List[int]], allow_diagonal: bool = True):
        """
        Args:
            grid: 0=이동가능, 1=장애물
            allow_diagonal: 대각선 이동 허용 여부
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.allow_diagonal = allow_diagonal

    def heuristic_manhattan(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """맨해튼 거리 (4방향)"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def heuristic_diagonal(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """체비쇼프 거리 (8방향)"""
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return max(dx, dy)  # 또는 D * max(dx, dy) + D2 * min(dx, dy)

    def heuristic_euclidean(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """유클리드 거리"""
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """이웃 위치 반환"""
        r, c = pos
        neighbors = []

        # 4방향
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if self.allow_diagonal:
            moves += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] == 0:  # 장애물이 아니면
                    neighbors.append((nr, nc))

        return neighbors

    def cost(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """이동 비용"""
        dr = abs(a[0] - b[0])
        dc = abs(a[1] - b[1])
        if dr + dc == 2:  # 대각선
            return 1.414  # sqrt(2)
        return 1.0

    def find_path(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        """경로 찾기"""

        # 휴리스틱 선택
        if self.allow_diagonal:
            h = self.heuristic_diagonal
        else:
            h = self.heuristic_manhattan

        astar = AStar(
            get_neighbors=self.get_neighbors,
            cost=self.cost,
            heuristic=h,
            is_goal=lambda x: x == goal
        )

        result = astar.search(start, goal)
        return result[0] if result else None


# 사용 예시
if __name__ == "__main__":
    # 10x10 그리드
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    finder = GridAStar(grid, allow_diagonal=True)
    start = (0, 0)
    goal = (9, 9)

    path = finder.find_path(start, goal)

    if path:
        print(f"경로 발견! 길이: {len(path)}")
        print(f"경로: {path}")
    else:
        print("경로 없음")
```

**③ A* 최적성 증명 요약**

```
A* 최적성 증명 (허용적 휴리스틱):

정의:
- h(n)이 허용적(Admissible): 모든 n에 대해 h(n) ≤ h*(n)
- h*(n): n에서 목표까지의 실제 최단 비용

정리: h가 허용적이면 A*는 최적해를 찾는다.

증명 개요:
1. A*가 목표 노드 G를 선택했다고 가정
2. f(G) = g(G) + h(G) = g(G) + 0 = g(G) (목표의 h=0)
3. 다른 어떤 경로 P의 비용이 g(G)보다 작다고 가정 (모순 유도)
4. P 상의 어떤 노드 n은 OPEN 리스트에 있어야 함
5. f(n) = g(n) + h(n) ≤ g(n) + h*(n) = P의 비용 < g(G)
6. 따라서 f(n) < f(G)인데, A*는 최소 f를 선택하므로 G보다 n을 먼저 선택했어야 함
7. 모순! 따라서 g(G)는 최적해다.
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### A* 변형 알고리즘 비교

| 알고리즘 | 특징 | 최적성 | 용도 |
|---------|------|--------|------|
| **A*** | f=g+h | Yes* | 범용 |
| **Weighted A*** | f=g+wh (w>1) | No** | 속도 우선 |
| **Dynamic A* (D*)** | 동적 환경 대응 | Yes | 로봇 내비게이션 |
| **D* Lite** | D*의 단순화 | Yes | 실시간 경로 |
| **Hybrid A*** | 연속 공간 | Near-optimal | 자율주행 |
| **Bidirectional A*** | 양방향 탐색 | Yes | 대규모 그래프 |
| **Jump Point Search** | 그리드 최적화 | Yes | 그리드 맵 |
| **Theta*** | Any-angle 경로 | Yes | 자연스러운 경로 |

*h 허용적일 때
**w-근사해 (최적해의 w배 이내)

### 과목 융합 관점

#### A* × 운영체제

- **메모리 관리**: OPEN/CLOSED 리스트의 효율적 관리
- **캐싱**: 휴리스틱 계산 결과 캐시
- **병렬화**: 멀티코어 활용한 병렬 A*

#### A* × 네트워크

- **라우팅 프로토콜**: OSPF, IS-IS의 SPF 알고리즘
- **네트워크 게임**: 실시간 경로 동기화
- **CDN**: 최적 서버 선택

#### A* × 머신러닝

- **휴리스틱 학습**: Neural Network로 h(n) 학습
- **AlphaZero 스타일**: MCTS + 학습된 휴리스틱

---

## IV. 실무 적용 및 기술사적 판단

### 실무 시나리오

#### 시나리오 1: 네비게이션 시스템

**전략**:
1. **계층적 A***: 고속도로망 → 지방도망 계층 분리
2. **Landmark 휴리스틱**: 주요 지점까지의 거리 미리 계산
3. **양방향 탐색**: 출발지/목적지에서 동시 시작
4. **결과**: 전국 도로망에서 < 100ms 탐색

#### 시나리오 2: 실시간 게임

**전략**:
1. **Weighted A*** (w=1.5): 속도 우선
2. **경로 캐싱**: 자주 사용하는 경로 저장
3. **타임 슬라이싱**: 프레임당 일정 시간만 탐색
4. **결과**: 60 FPS 유지, 자연스러운 NPC 이동

#### 시나리오 3: 자율주행

**전략**:
1. **Hybrid A***: 연속 좌표 + 이산 그리드 결합
2. **Non-holonomic 제약**: 차량 운동학 반영
3. **Reed-Shepp 곡선**: 조향 가능 경로
4. **결과**: 주차 시나리오에서 실시간 경로 생성

### 도입 시 고려사항

- [ ] **휴리스틱 선택**: 문제 특성에 맞는 h(n) 설계
- [ ] **허용성 검증**: h(n) ≤ h*(n) 확인
- [ ] **메모리 관리**: 대규모 맵에서의 메모리 최적화
- [ ] **실시간성**: 타임 아웃 및 근사 해

### 안티패턴

1. **비허용적 휴리스틱**: h(n) > h*(n) → 최적해 상실
2. **과도한 정밀도**: 불필요한 부동소수점 정밀도
3. **메모리 누수**: OPEN/CLOSED 정리 안 함

---

## V. 기대효과 및 결론

### 정량적 효과

| 알고리즘 | 탐색 노드 | 시간 | 메모리 |
|---------|----------|------|--------|
| BFS | 100,000 | 1.0s | 높음 |
| 다익스트라 | 100,000 | 1.0s | 높음 |
| A* (h₁) | 10,000 | 0.1s | 중간 |
| A* (h₂) | 1,000 | 0.01s | 낮음 |

### 미래 전망

1. **딥러닝 기반 휴리스틱**: 자동 최적 h(n) 학습
2. **양자 A***: 양자 중첩으로 병렬 탐색
3. **실시간 D***: 동적 환경에서 즉각 대응

---

## 📌 관련 개념 맵

- [휴리스틱 탐색](./12_heuristic_search.md) - 정보 기반 탐색
- [맹목적 탐색](./11_uninformed_search.md) - 다익스트라, BFS
- [상태 공간 탐색](./10_state_space_search.md) - 문제 해결 프레임워크

---

## 👶 어린이를 위한 3줄 비유

**1. A*는 똑똑한 내비게이션이에요.** "지금까지 3km 왔고, 목적지까지 직선 거리가 2km야. 그러니 총 5km쯤 걸릴 거야!"라고 계산하면서 가장 짧을 것 같은 길을 먼저 가요.

**2. 중요한 건 "절대로 실제보다 멀다고 추측하지 않는 것"이에요.** "직선 거리 2km인데 5km라고 하면" 최단 경로를 놓칠 수 있거든요. 그래서 항상 조심스럽게 추측해요.

**3. 덕분에 빠르고 정확하게 목적지에 도착해요!** 모든 길을 다 가볼 필요 없이, 목적지 쪽으로 똑똑하게 이동하니까요. 우리가 쓰는 내비게이션 앱도 이 알고리즘을 사용해요!
