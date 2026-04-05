+++
title = "332. PageRank / BFS"
weight = 4332
+++

> **💡 핵심 인사이트**
> PageRank와 BFS(너비 우선 탐색)는 **"그래프(Network) 구조에서 핵심적인 순회(Traversal) 및 중요도 산출 알고리즘"**입니다.
> PageRank는 **"다른 노드에서 많이 링크되는 노드가重要"**라는 아이디어로 웹 페이지 순위를 매기는算法이며, BFS는 **"시작점에서 가까운 노드부터 체계적으로 탐색"**하는 그래프 순회 알고리즘입니다. PageRank가 Google 검색엔진의根基라면, BFS는 소셜 네트워크 분석, 경로 탐색, 레벨 오더婚礼请客配席 등 다양한实际问题에서 활용됩니다.

---

## Ⅰ. PageRank: 웹의 중요도를測る算法

### PageRank의 핵심 아이디어

PageRank는 **"중요한 페이지는 다른 중요 페이지에서 링크를 많이 받는다는 가정"**에 기반합니다:

```
[PageRank 개념]

  웹 페이지들 사이의 링크 관계:

        Page A (importance = ?)
           │links
           ▼
        ┌────────┐     ┌────────┐
        │ Page B │────▶│ Page C │
        └────────┘     └────────┘
           │links          │links
           ▼               ▼
        ┌────────┐     ┌────────┐
        │ Page D │◀────│ Page E │
        └────────┘     └────────┘

  직관적 의미:
  - Page C: A, B, E에서 링크됨 (3개) → 중요!
  - Page B: C에게만 링크됨 (1개) → 덜 중요
  - Page D: B에게만 링크됨 (1개) → 덜 중요
  - PageRank:links의 질(출발점 중요도)도 고려
```

### PageRank 공식

```
[PageRank 계산 공식]

  PR(A) = (1 - d)/N + d × Σ( PR(Ti) / C(Ti) )

  where:
  - PR(A): 페이지 A의 PageRank
  - d: damping factor (보통 0.85)
  - N: 전체 페이지 수
  - Ti: 페이지 A로 링크하는 페이지
  - C(Ti): 페이지 Ti가 가진 외부 링크 수
  - Σ: 모든 Ti에 대한 합산

  의미:
  - damping factor: 사용자가 무작위 페이지로 이동할 확률 (0.85)
  - 1-d: 무작위 점프할 확률 (0.15)
```

### PageRank 코드 예시

```python
import numpy as np

def pagerank(adj_matrix, d=0.85, max_iter=100, tol=1e-6):
    """
    adj_matrix: 인접 행렬 (N x N)
                adj_matrix[i][j] = 1 if i → j 링크 존재
    """
    N = adj_matrix.shape[0]

    # 초기 PageRank (균등 분배)
    pr = np.ones(N) / N

    # 반복 계산
    for _ in range(max_iter):
        new_pr = (1 - d) / N + d * adj_matrix.T.dot(pr / adj_matrix.sum(axis=1))

        # 수렴 판정
        if np.linalg.norm(new_pr - pr, 1) < tol:
            break
        pr = new_pr

    return pr

# 예시: 4개 페이지의 링크 관계
# A → B, C / B → C / C → A / D → C
adj = np.array([
    [0, 1, 1, 0],  # A → B, C
    [0, 0, 1, 0],  # B → C
    [1, 0, 0, 0],  # C → A
    [0, 0, 1, 0],  # D → C
])
pr = pagerank(adj)
print(f"PageRank: {pr}")
# 결과: C가 가장 높은 PageRank (링크를 3개 받음)
```

---

## II. BFS (Breadth-First Search): 체계적 탐색의 기본

### BFS의 원리

```
[BFS vs DFS]

  그래프:
       A
      / \
     B   C
    / \   \
   D   E   F

  BFS (Queue 기반, 레벨 순회):
  Queue: [A]
  1. A dequeue → 방문 → A의 이웃 B, C enqueue
  Queue: [B, C]
  2. B dequeue → 방문 → B의 이웃 D, E enqueue
  Queue: [C, D, E]
  3. C dequeue → 방문 → C의 이웃 F enqueue
  Queue: [D, E, F]
  4. D, E, F 순서로 dequeue/방문

  순서: A → B → C → D → E → F
  (레벨순: 0레벨 → 1레벨 → 2레벨)

  DFS (Stack 기반, 깊이 우선):
  순서: A → B → D → E → C → F
  (한 방향으로 최대한 파고들기)
```

### BFS 코드

```python
from collections import deque

def bfs(graph, start):
    """
    graph: 인접 리스트 {node: [neighbors]}
    start: 시작 노드
    """
    visited = set()
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()  # 선입선출
        if node not in visited:
            visited.add(node)
            order.append(node)
            queue.extend(graph[node] - visited)

    return order

# 예시: 길찾기
graph = {
    'A': {'B', 'C'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'C', 'E'}
}

print(bfs(graph, 'A'))
# 출력: ['A', 'B', 'C', 'D', 'E', 'F']
# → A에서 F까지의 최단 경로: A → B → E → F 또는 A → C → F
```

---

## III. PageRank와 BFS의 관계と活用

```
[PageRank와 BFS의 관계]

  공통점:
  - 둘 다 그래프/네트워크 순회 알고리즘
  - 연결된 노드들을 따라가며 정보 전파

  차이점:
  ┌────────────────┬────────────────────────┐
  │    PageRank    │         BFS            │
  ├────────────────┼────────────────────────┤
  │  모든 노드를   │ 한 시작점에서 체계적 탐색│
  │  동시에 평가   │                         │
  ├────────────────┼────────────────────────┤
  │  반복 계산으로 │ 한 번의 순회로 완료      │
  │  수렴 달성    │                         │
  ├────────────────┼────────────────────────┤
  │  중요도(순위) │ 최단 경로, 연결 요소,   │
  │  산출        │ 레벨별 탐색             │
  ├────────────────┼────────────────────────┤
  │  시간: O(I×E) │ 시간: O(V+E)            │
  │  (I=반복 횟수)│                        │
  └────────────────┴────────────────────────┘
```

### 실제 활용

```
[PageRank 활용 사례]

  1. 웹 검색 (원래 목적)
     - Google의 PageRank → 이후 더 정교한 알고리즘으로 발전
     - 현재도 인용 네트워크, 연구자 영향력 등에 활용

  2. 소셜 네트워크 중요 인물 탐지
     - 트위터에서 중요한 사용자 순위
     - 링크드인에서 영향력 있는 프로фессионал

  3. 학술 논문 인용 네트워크
     - 어떤 논문이 많이 인용되었는가?
     - H-index와 함께 활용

  4. 교통 네트워크
     - 도시별 중요도 평가
     - 고속도로 정체 구간 예측


[BFS 활용 사례]

  1. 최단 경로 찾기 (无权 그래프)
     - 미로 찾기, 네비게이션
     - 소셜 네트워크에서 "친구关系的度数" 계산

  2. 레벨별 순회
     - 조직도 레벨 탐색
     - 게임에서 동일 레벨 적 탐색

  3. 연결 요소 판별
     - 네트워크 분할 발견
     - 사회망에서 친구 그룹 분류

  4. 그레이햄 스캔 (Graham Scan)
     - 볼록 껍질(Convex Hull) 계산
```

---

## IV. PageRank와 BFS의graph DB 적용

**Neo4j (그래프 DB)에서 PageRank:**

```cypher
// Neo4j에서 PageRank 알고리즘 활용
// gds 라이브러리 사용

CALL gds.pageRank.stream({
  nodeProjection: 'Page',
  relationshipProjection: 'LINKS_TO'
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).url AS page, score
ORDER BY score DESC
LIMIT 10;
```

**Neo4j에서 BFS:**

```cypher
// 최단 경로 찾기 (BFS 기반)
MATCH (start:User {name: 'Alice'}),
      (end:User {name: 'Eve'})
MATCH path = shortestPath((start)-[:KNOWS*]-(end))
RETURN path;

// BFS로 레벨별 탐색 (친구의 친구)
MATCH (start:User {name: 'Bob'})-[:KNOWS*1..2]-(friend)
RETURN DISTINCT friend.name, LENGTH(foo(path)) AS degree
ORDER BY degree;
```

---

## Ⅴ. 알고리즘 선택 가이드と 📢 비유

**어떤 알고리즘을 선택하는가?**

```
[선택 기준]

  PageRank를 써야 할 때:
  - 전체 네트워크에서 "중요한 노드"를 찾고 싶다
  -links/인용/참조의 질을 평가하고 싶다
  - 반복적 수렴이許容된다

  BFS를 써야 할 때:
  - 시작점에서 가까운 노드를 체계적으로 찾고 싶다
  - 최단 경로를 찾고 싶다 (无权)
  - 한 번의 탐색으로 충분하다
```

> 📢 **섹션 요약 비유:** PageRank와 BFS는 **"도시의 importância를 평가하는 두 가지 방법"**과 같습니다. PageRank는 **"다른 중요한 도시에서 많이 연결되는 도시가 중요한 도시다"**라는 순환적定義로, 결국 모든 도시의重要性を迭代적으로 계산합니다. "이 도시에 사람들이 많이 오고 간다"를 직접 세는 것이 아니라, "어떤 도시에서 사람들이 많이 오고 가는가?"를繰り返し 계산해서 도달합니다. 반면 BFS는 **"시내 중심가에서 시작해서 1번으로 시작해서 바깥으로一圈一圈 넓혀나가는 것"**입니다.中心からの距離に応じて 순서대로 탐색하여, **"여기서 거기까지 가려면 어떻게 가야 가장 짧은가?"**를 확실히 찾아냅니다. PageRank가 **"全局적 중요도"**를评估한다면, BFS는 **"局部적最近접"**을探索합니다. 둘 다 그래프라는 같은 구조를 다루지만,問いと答える内容が根本的に異なります.
