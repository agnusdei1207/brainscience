+++
title = "110. 스킵 리스트 (Skip List)"
weight = 110
+++

# 110. 스킵 리스트 (Skip List)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스킵 리스트(Skip List)는 다층 연결 리스트(Multi-level Linked List)로 구성되어, 빠르게 요소를 탐색할 수 있는 확률적(Probabilistic) 자료구조이다.
> 2. **가치**: 균형 이진 트리와 유사한 O(log n) 검색 성능을 제공하면서도, 구현이 훨씬简单하고 동적 리밸런싱이 필요 없다.
> 3. **융합**: Redis의 Sorted Set, LevelDB, Lucene 등의 실시간 정렬된 데이터 저장소에서 핵심 자료구조로 활용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

스킵 리스트(Skip List)는 William Pugh가 1990년 논문에서 처음 소개한 자료구조로, **확률적 균형 이진 탐색 트리**라고도 불린다. 기본 아이디어는 정렬된 연결 리스트에서 일부 요소를 "건너뛰어" 더 빠르게 탐색할 수 있도록 하는 것이다.

스킵 리스트가 중요한 이유는 **구현의 단순성**과 **우수한 성능** 때문이다. 레드-블랙 트리(Red-Black Tree)나 AVL 트리 같은 전통적인 균형 이진 트리는 삽입과 삭제 시 복잡한 회전 작업으로 리밸런싱을 수행해야 한다. 반면, 스킵 리스트는 확률적으로 레벨을 결정하여 리밸런싱 없이도 O(log n) 성능을 달성한다.

스킵 리스트의 핵심 아이디어는 **고속도로 연결 리스트**와 같다. 일반 연결 리스트에서는 한 노드씩 순차적으로 이동해야 하지만, 스킵 리스트에서는Express lane을 통해 여러 노드를 건너뛸 수 있다. 이렇게 하면 탐색 시간을 크게 단축할 수 있다.

```text
[스킵 리스트 기본 구조]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  [일반 연결 리스트: 탐색 O(n)]                               │
│  ────────────────────────────────────────────                │
│  HEAD → [1] → [5] → [9] → [12] → [18] → [25] → NULL        │
│                한 단계씩 이동해야 함                           │
│                                                              │
│  [스킵 리스트: 탐색 O(log n)]                                │
│  ────────────────────────────────────────────                │
│  LEVEL 3: HEAD ───────────────────────────────→ NULL        │
│           (Express lane - 건너뛰기)                          │
│  LEVEL 2: HEAD ──────────────── → [12] ───────→ NULL        │
│  LEVEL 1: HEAD ────── → [5] ── → [9] ── → [12] → [18] → NULL│
│  LEVEL 0: HEAD → [1] → [5] → [9] → [12] → [18] → [25] → NULL│
│                                                              │
│  예: 18 찾기                                                 │
│  Step 1: LEVEL 3: HEAD → NULL (범위 초과) → LEVEL 2로       │
│  Step 2: LEVEL 2: HEAD → [12] (12 < 18) → LEVEL 1로        │
│  Step 3: LEVEL 1: [12] → [18] (발견!)                       │
│                                                              │
│  [노드 구조]                                                 │
│  ────────────────────────────────────────────                │
│  각 노드는 여러 레벨의 포인터를 가짐:                          │
│  Node {                                                     │
│      value: 데이터 값                                         │
│      forward[0]: LEVEL 0 포인터 (다음 노드)                   │
│      forward[1]: LEVEL 1 포인터                               │
│      forward[2]: LEVEL 2 포인터                               │
│      ...                                                     │
│  }                                                          │
│                                                              │
│  레벨 결정: 확률 p (보통 0.5 = 1/2)로 각 레벨에 포함될 확률   │
│  레벨 0: 항상 100%, 레벨 1: 50%, 레벨 2: 25%, ...           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- **관찰**: 스킵 리스트의 높이가 log n이면 탐색도 O(log n)이다.
- **원인**: 각 레벨에서 approximately 절반씩 건너뛸 수 있기 때문이다.
- **결과**: 평균적으로 O(log n) 시간에 탐색이 가능하다.
- **판단**: 확률적 자료구조이지만 실제 성능은 결정적 자료구조와匹敵한다.

📢 **섹션 요약 비유**: 스킵 리스트는 **비행기 창구역과 철도역**의 차이와 같습니다. 모든 역에 정차하는 기차는 느리지만, 급행열차는 주요 역만 정차하여 빠르게 이동합니다. 스킵 리스트는 이러한 계층적 정차 시스템을 연결 리스트에 적용하여, 일부 요소들을 "급행 정차역"으로 만들어 탐색 속도를 향상시킵니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

스킵 리스트의 핵심은 **레벨 기반 탐색**과 **확률적 레벨 할당**이다. 이를 이해하면 탐색, 삽입, 삭제 동작이 자연스럽게 파악된다.

**레벨 기반 탐색(Search)**은 다음과 같이 동작한다: 가장 높은 레벨에서 시작하여, 현재 노드의 다음 노드가 탐색 대상보다 작은 동안 오른쪽으로 이동한다. 더 이상 이동할 수 없으면 현재 레벨보다 하나 낮은 레벨로 내려간다. 레벨 0에 도달할 때까지 또는 값을 찾을 때까지 반복한다. 시간 복잡도는 O(log n)이다.

**레벨 할당(Level Assignment)**에서 새 노드가 어떤 레벨을 가질지는 무작위로 결정된다. 동전 던지기(Coin Toss) 방식을 사용한다: 0.5 확률로 레벨 1에 포함, 0.25 확률로 레벨 2에 포함, 0.125 확률로 레벨 3에 포함... 실제로는 레벨의 최대값을 제한(maxLevel)하여 무한히 높아지는 것을 방지한다.

**삽입(Insert)**은 먼저 탐색하여 삽입 위치를 찾는다. 무작위로 새 노드의 레벨을 결정한다. 새 노드를 생성하여 적절한 레벨에 삽입한다. 모든 레벨에서 predecessor 포인터를 업데이트한다.

**삭제(Delete)**는 탐색하여 삭제할 노드를 찾는다. 모든 레벨에서 predecessor 포인터를 다음 노드로 업데이트한다. 노드를 메모리에서 해제한다.

```text
[스킵 리스트 연산 상세]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  [탐색 알고리즘: search(x)]                                   │
│  ────────────────────────────────────────────                │
│  current = HEAD                                              │
│  for i = maxLevel downto 0:                                 │
│      while current.forward[i].value < x:                     │
│          current = current.forward[i]                      │
│      # 더 이상 이동 불가, 한 레벨 내림                         │
│  current = current.forward[0]  # LEVEL 0로                  │
│  if current.value == x:                                     │
│      return current  # 발견                                  │
│  else:                                                      │
│      return NULL     # 없음                                   │
│                                                              │
│  [레벨 결정: randomLevel()]                                  │
│  ────────────────────────────────────────────                │
│  level = 0                                                   │
│  while random() < p and level < MAX_LEVEL:                  │
│      level += 1                                              │
│  return level                                               │
│                                                              │
│  예: p = 0.5, MAX_LEVEL = 4                                 │
│  random() = 0.7 → level = 0                                 │
│  random() = 0.3 → level = 1                                 │
│  random() = 0.1 → level = 2 → random() = 0.8 < 0.5 → 종료  │
│                                                              │
│  [삽입: insert(x)]                                          │
│  ────────────────────────────────────────────                │
│  1. search(x)로 삽입 위치 찾기                               │
│  2. newLevel = randomLevel()                               │
│  3. update[0..newLevel] 배열에 각 레벨의 predecessor 저장    │
│  4. 새 노드 생성                                            │
│  5. for i = 0 to newLevel:                                 │
│       newNode.forward[i] = update[i].forward[i]           │
│       update[i].forward[i] = newNode                       │
│                                                              │
│  [삭제: delete(x)]                                          │
│  ────────────────────────────────────────────                │
│  1. search(x)로 삭제할 노드 찾기                             │
│  2. 모든 레벨에서 predecessor 포인터 갱신                     │
│  3. 노드 메모리 해제                                        │
│                                                              │
│  [시간 복잡도]                                               │
│  ────────────────────────────────────────────                │
│  연산        평균        최악                               │
│  탐색       O(log n)    O(n)                               │
│  삽입       O(log n)    O(n)                               │
│  삭제       O(log n)    O(n)                               │
│  ※ 레벨이 log n에 근접할 확률이 높으므로 평균 O(log n)      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- **관찰**: 스킵 리스트의 모든 연산이 O(log n) 평균 시간에 수행된다.
- **원인**: 레벨이 log n에 근접할 확률이 높기 때문이다.
- **결과**: 균형 이진 트리와 유사한 성능을 제공한다.
- **판단**: 그러나 최악의 경우 O(n)이 될 수 있음을 유의해야 한다.

---

## Ⅲ. 구현 및 활용 (Implementation & Applications)

스킵 리스트의 구현은 상대적으로 간단하여 실제 시스템에서 널리 사용된다. 특히 동적 리밸런싱이 필요 없다는 장점이 있다.

**기본 구현**에서 각 노드는 값과 포인터 배열(forward)을 가진다. 헤드 노드는 모든 레벨의 시작점이며, sentinel 역할을 한다. MAX_LEVEL은 일반적으로 log n으로 설정하지만, 구현 단순화를 위해 고정값(예: 16 또는 32)을 사용하기도 한다.

**Redis에서의 활용**에서 Sorted Set은 스킵 리스트로 구현되어 있다. 각 요소는 score로 정렬되며, O(log n) 삽입, 삭제, 순위 찾기가 가능하다. ZADD, ZRANGE, ZRANK 등의 명령어가 스킵 리스트 기반으로 동작한다.

**기타 활용**으로 **이벤트 스케줄러**에서 시간 순으로 정렬된 이벤트 관리에 사용된다. **네트워크 라우팅**에서 라우팅 테이블 관리에 사용될 수 있다. **멤버십 테스트**에서 확률적 집합 멤버십에 활용된다.

```text
[스킵 리스트 구현 코드]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  class SkipListNode:                                         │
│      def __init__(self, value, max_level):                  │
│          self.value = value                                 │
│          self.forward = [None] * (max_level + 1)            │
│                                                              │
│  class SkipList:                                            │
│      def __init__(self, max_level=16, p=0.5):              │
│          self.MAX_LEVEL = max_level                        │
│          self.p = p  # 레벨 증가 확률                        │
│          self.HEAD = SkipListNode(None, self.MAX_LEVEL)   │
│          self.level = 0  # 현재 최대 레벨                    │
│                                                              │
│      def random_level(self):                                │
│          level = 0                                          │
│          while random.random() < self.p and level < self.MAX_LEVEL:│
│              level += 1                                      │
│          return level                                        │
│                                                              │
│      def search(self, target):                               │
│          current = self.HEAD                                 │
│          for i in range(self.level, -1, -1):                │
│              while current.forward[i] and current.forward[i].value < target:│
│                  current = current.forward[i]                │
│          current = current.forward[0]                       │
│          if current and current.value == target:            │
│              return current                                 │
│          return None                                         │
│                                                              │
│      def insert(self, value):                                │
│          update = [None] * (self.MAX_LEVEL + 1)             │
│          current = self.HEAD                                │
│                                                              │
│          # predecessor 찾기                                  │
│          for i in range(self.level, -1, -1):                │
│              while current.forward[i] and current.forward[i].value < value:│
│                  current = current.forward[i]                │
│              update[i] = current                             │
│                                                              │
│          new_level = self.random_level()                    │
│          if new_level > self.level:                         │
│              for i in range(self.level + 1, new_level + 1):│
│                  update[i] = self.HEAD                       │
│              self.level = new_level                         │
│                                                              │
│          new_node = SkipListNode(value, self.MAX_LEVEL)    │
│          for i in range(0, new_level + 1):                  │
│              new_node.forward[i] = update[i].forward[i]    │
│              update[i].forward[i] = new_node                │
│                                                              │
│      def delete(self, value):                                │
│          update = [None] * (self.MAX_LEVEL + 1)             │
│          current = self.HEAD                                │
│                                                              │
│          for i in range(self.level, -1, -1):                │
│              while current.forward[i] and current.forward[i].value < value:│
│                  current = current.forward[i]                │
│              update[i] = current                             │
│                                                              │
│          current = current.forward[0]                       │
│          if current and current.value == value:             │
│              for i in range(0, self.level + 1):            │
│                  if update[i].forward[i] != current:       │
│                      break                                   │
│                  update[i].forward[i] = current.forward[i] │
│              # 불필요해진 레벨 정리                           │
│              while self.level > 0 and self.HEAD.forward[self.level] is None:│
│                  self.level -= 1                             │
│                                                              │
│  [Redis Sorted Set 활용 예]                                  │
│  ────────────────────────────────────────────                │
│  ZADD leaderboard 100 "player1"  # 점수 100으로 추가         │
│  ZADD leaderboard 200 "player2"  # 점수 200으로 추가         │
│  ZRANK leaderboard "player1"    # player1의 순위 (0부터)   │
│  ZRANGE leaderboard 0 9          # 상위 10명 조회            │
│                                                              │
│  내부: score → member 매핑이 스킵 리스트로 저장              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- **관찰**: 스킵 리스트는 균형 이진 트리보다 구현이 훨씬 간단하다.
- **원인**: 회전이나 복잡한 리밸런싱 로직이 필요 없기 때문이다.
- **결과**: 실무에서 균형 이진 트리 대신 자주 사용된다.
- **판단**: 특히 동적 리밸런싱이 어려운 concurrent 환경에서 유용하다.

---

## Ⅳ. 균형 이진 트리와의 비교 (Comparison with Balanced BST)

스킵 리스트와 균형 이진 트리(AVL, 레드-블랙 트리)는 모두 O(log n) 검색을 제공하지만, 구조와 동작에서 중요한 차이가 있다.

**공통점**으로 both O(log n) 평균/최악 시간 복잡도를 제공한다. 둘 다 동적 데이터 구조로 삽입, 삭제, 검색을 지원한다. 그리고 정렬된 순서로 순회가 가능하다.

**장단점 비교**에서 스킵 리스트의 **장점**은 구현이 간단하고, 동적 리밸런싱이 필요 없으며, concurrent 확장이 용이하고, 레벨을 통한 범위 쿼리가 효율적이다. **단점**은 최악 O(n) 가능성이 있고, 포인터 오버헤드가 있으며, 캐시 지역성이 나쁘다.

균형 이진 트리의 **장점**은 최악 O(log n)이 보장되고, 캐시 지역성이 좋으며, 포인터 오버헤드가 적다. **단점**은 구현이 복잡하고, 회전 작업의 비용이 크며, concurrent 확장이 어렵다.

**Concurrent 환경**에서 스킵 리스트가 유리하다. 각 레벨의 포인터 수정이局所적이어서 락(Lock)의粒度が 작다. 반면 균형 이진 트리의 회전은 전체 트리에 영향을 미칠 수 있다. Java의 ConcurrentSkipListMap이 스킵 리스트 기반으로 concurrent 맵을 구현한다.

```text
[스킵 리스트 vs 균형 이진 트리]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  [시간 복잡도 비교]                                           │
│  ────────────────────────────────────────────                │
│                                                              │
│              스킵 리스트           레드-블랙 트리              │
│  탐색       O(log n) 평균       O(log n) 보장               │
│  삽입       O(log n) 평균       O(log n) 보장               │
│  삭제       O(log n) 평균       O(log n) 보장               │
│  순회       O(n)               O(n)                        │
│  범위 쿼리   O(k + log n)      O(k + log n)                │
│                                                              │
│  [메모리 사용 비교]                                          │
│  ────────────────────────────────────────────                │
│                                                              │
│  스킵 리스트:                                                │
│  • 각 노드: 값 + log n 레벨의 포인터                          │
│  • 평균: n * (1 + 1/2 + 1/4 + ...) = 2n 포인터              │
│                                                              │
│  레드-블랙 트리:                                              │
│  • 각 노드: 값 + 좌우 포인터 + 색상                           │
│  • 총: n * 3 포인터 (레드-블랙额外 정보 포함)                │
│                                                              │
│  [Concurrent 접근 비교]                                      │
│  ────────────────────────────────────────────                │
│                                                              │
│  스킵 리스트:                                                │
│  • 레벨 단위 락 가능 (세밀한 동시성 제어)                       │
│  • 삽입 시 상위 레벨 포인터만 수정                            │
│  • Java: ConcurrentSkipListMap                             │
│                                                              │
│  레드-블랙 트리:                                              │
│  • 회전 시 여러 노드 동시 수정 가능성                          │
│  • 전체 트리 또는 서브트리 단위 락 필요                        │
│  • Java: synchronized + TreeMap (느림)                     │
│                                                              │
│  [선택 기준]                                                  │
│  ────────────────────────────────────────────                │
│  스킵 리스트 선택:                                           │
│  • concurrent 환경                                            │
│  • 구현 단순성 중요                                           │
│  • 범위 쿼리 빈번                                            │
│                                                              │
│  레드-블랙 트리 선택:                                         │
│  • 최악 시간 보장 중요                                        │
│  • 캐시 지역성 중요                                           │
│  • 복잡한 범위 쿼리                                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- **관찰**: 스킵 리스트는 concurrent 환경에서 더 선호된다.
- **원인**: 세밀한 락킹이 가능하고, 회전 작업이 없기 때문이다.
- **결과**: 고성능 concurrent 시스템에서 스킵 리스트가 많이 사용된다.
- **판단**: 대부분의 경우 스킵 리스트로 충분한 성능을 제공한다.

---

## Ⅴ. 요약 및 점검 (Summary & Checklist)

스킵 리스트(Skip List)는 확률적 다층 연결 리스트로, O(log n) 평균 검색 성능을 제공하는 동적 자료구조이다. 구현이 간단하고 concurrent 확장이 용이하여 실무에서 널리 사용된다.

**핵심 점검 사항**으로 먼저, **구조**에서 다층 연결 리스트, 레벨이 확률적으로 결정된다. 둘째, **탐색**은 상위 레벨에서 하위 레벨로 이동하며 O(log n)이다. 셋째, **레벨 할당**은 동전 던지기 방식으로 확률 0.5로 레벨 증가한다. 넷째, **시간 복잡도**는 평균 O(log n)이고, 최악 O(n)이다. 다섯째, **장점**으로 구현 단순성, 동적 리밸런싱 불필요, concurrent 친화적이다. 여섯째, **활용**으로 Redis Sorted Set, ConcurrentSkipListMap 등이 있다.

> **핵심 용어 정리**
> - **스킵 리스트 (Skip List)**: 다층 연결 리스트 기반 확률적 자료구조
> - **레벨 (Level)**: 노드가 가지는 포인터의 수
> - **MAX_LEVEL**: 레벨의 최대값
> - **p (확률)**: 각 레벨에 포함될 확률 (보통 0.5)
> - **ConcurrentSkipListMap**: Java의 thread-safe 스킵 리스트 기반 Map

---

## 检查清单 (Checkpoint)

- [ ] 스킵 리스트의 기본 구조를 설명할 수 있는가?
- [ ] 스킵 리스트에서 탐색이 O(log n)인 이유를 설명할 수 있는가?
- [ ] 레벨이 확률적으로 결정되는 방법을 설명할 수 있는가?
- [ ] 스킵 리스트와 레드-블랙 트리의 장단점을 비교할 수 있는가?
- [ ] 스킵 리스트가 concurrent 환경에서 유리한 이유를 설명할 수 있는가?
- [ ] 스킵 리스트가 활용되는 실제 시스템을 열거할 수 있는가?
