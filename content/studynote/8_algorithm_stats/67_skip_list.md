+++
title = "67. 스킵 리스트 (Skip List)"
weight = 67
+++

# 67. 스킵 리스트 (Skip List)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스킵 리스트(Skip List)는 다중 레벨 연결 리스트로, 상위 레벨이 하위 레벨의 일부 노드를 "스킵"하여 검색을加速하는 자료구조이다.
> 2. **가치**: 평균 O(log N) 시간에 검색, 삽입, 삭제가 가능하며, 균형 이진 탐색 트리보다 구현이 간단하다.
> 3. **융합**: Redis의 Sorted Set, LevelDB, Lucene 등의 고성능 저장소에서 활용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

스킵 리스트(Skip List)는 1990년 William Pugh가 제안한 자료구조이다. 균형 이진 탐색 트리(AVL 트리, Red-Black Tree)와 유사한 성능(O(log N))을 제공하지만, 구현이 훨씬 간단하고 병렬 처리가 용이하다.

스킵 리스트가 중요한 이유는 **단순성과 성능의 균형** 때문이다. 이진 탐색 트리는 균형을 유지하기 위해 복잡한 회전 연산이 필요하지만, 스킵 리스트는 확률적 고도 할당을 통해 자연스럽게 균형을 유지한다. 또한, 삽입/삭제가 트리와 달리局部적이어서 병렬 처리가 용이하다.

스킵 리스트의 핵심 아이디어는 **다중 레벨链表**이다. 가장 하위 레벨(레벨 0)은 모든 원소를 순서대로 연결한다. 상위 레벨은 하위 레벨의 일부 원소를 "스킵"하면서 연결한다. 검색 시 상위 레벨에서 빠르게 이동하다가 하위 레벨로 세분화하여 검색한다.

```text
[스킵 리스트 구조]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  [4단계 스킵 리스트 예시]                                     │
│  ────────────────────────────────────────────                │
│                                                              │
│  Level 3:  HEAD ────────────────────────────── NIL           │
│            │                                              │   │
│  Level 2:  HEAD ──────────── NIL                           │   │
│            │          │                                   │   │
│  Level 1:  HEAD ──── NIL                                   │   │
│            │   │     │                                     │   │
│  Level 0:  HEAD ─→ 3 → 7 → 12 → 18 → 25 → 33 → NIL        │
│                                                              │
│  [검색 과정: 18 찾기]                                         │
│  ────────────────────────────────────────────                │
│                                                              │
│  Level 3:  HEAD ────────────────────────────── NIL           │
│            │                                              │   │
│  Level 2:  HEAD ──────────── NIL                           │   │
│            │          │     ↑ 33보다 작으니 여기서 멈춤     │   │
│  Level 1:  HEAD ──── NIL     │                             │   │
│            │   │     │       │                             │   │
│  Level 0:  HEAD ─→ 3 → 7 → 12 → 18 → 25 → 33 → NIL       │
│                      ↑      ↑ 12와 25 사이, 18 발견!        │
│                                                              │
│  [노드 고도 (Level)]                                          │
│  ────────────────────────────────────────────                │
│                                                              │
│  각 노드는 확률적으로 고도를 가진다 (보통 1/2 확률)           │
│  고도 3 노드: [value, next0, next1, next2, next3]            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- **관찰**: 스킵 리스트에서 상위 레벨로 갈수록 노드 수가 급격히 줄어든다.
- **원인**: 각 노드가 현재 레벨보다 한 레벨 위에 있을 확률이 1/2이기 때문이다.
- **결과**: 검색 시 상위 레벨에서 빠르게 스킵하면서 효율적으로 검색할 수 있다.
- **판단**: 구현의 단순성과 병렬 처리가 중요하면 스킵 리스트가 균형 트리보다 유리하다.

📢 **섹션 요약 비유**: 스킵 리스트는 **高層建物의 엘리베이터 시스템**과 같습니다. 모든 층에 정차하는 엘리베이터(단순 연결 리스트)보다,express 엘리베이터(상위 레벨)가 주요 층만 정차하여 빠르게 이동한다. 목적지에 가까워지면 해당 층에서express를 타고 내려와 lower floor를利用하여目的地에 도달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

스킵 리스트의 핵심은 **노드 고도 할당**과 **검색 경로 탐색**이다.

**노드 고도 할당**: 새 노드가 생성될 때 동전 던지기(확률 1/2)를 반복하여 고도를 결정한다. 각 레벨 i에 도달할 확률은 (1/2)^i이다. 최대 고도는 일반적으로 log₂(N)으로 제한한다.

**검색 알고리즘**: 가장 상위 레벨에서 시작한다. 현재 노드의 다음 노드가 목표 값보다 크거나 NIL이면 현재 레벨에서 아래로 내려간다. 현재 노드의 다음 노드가 목표 값보다 작으면 다음 노드로 이동한다. 레벨 0에 도달하면 목표 값의 존재 여부를 판단한다.

**삽입 알고리즘**: 검색을 수행하여 삽입 위치를 찾는다(현재 노드들 배열 업데이트). 노드의 고도를 확률적으로 결정한다. 각 레벨에서 적절한 위치에 노드를 삽입한다.

```text
[스킵 리스트 상세 알고리즘]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  [노드 구조]                                                 │
│  ────────────────────────────────────────────                │
│                                                              │
│  class SkipNode:                                             │
│      def __init__(self, value, level):                       │
│          self.value = value                                 │
│          self.forward = [None] * (level + 1)  // 각 레벨의 다음 노드
│                                                              │
│  [검색]                                                      │
│  ────────────────────────────────────────────                │
│                                                              │
│  function search(skiplist, target):                         │
│      current = skiplist.header                               │
│                                                              │
│      // 가장 상위 레벨에서 시작                               │
│      for i = skiplist.level downto 0:                       │
│          while current.forward[i].value < target:            │
│              current = current.forward[i]                   │
│                                                              │
│      // 레벨 0에서 실제 노드로 이동                           │
│      current = current.forward[0]                           │
│                                                              │
│      if current.value == target:                             │
│          return current  // 발견                             │
│      else:                                                   │
│          return None  // 미발견                              │
│                                                              │
│  [삽입]                                                      │
│  ────────────────────────────────────────────                │
│                                                              │
│  function insert(skiplist, value):                           │
│      // 1. 삽입 위치 찾기 + 업데이트할 노드 배열               │
│      update = [None] * (MAX_LEVEL)                           │
│      current = skiplist.header                               │
│                                                              │
│      for i = skiplist.level downto 0:                       │
│          while current.forward[i].value < value:             │
│              current = current.forward[i]                   │
│          update[i] = current  // 현재 위치를 저장             │
│                                                              │
│      // 2. 새 노드의 레벨 결정 (확률적)                        │
│      new_level = random_level()                              │
│                                                              │
│      // 3. 새 노드 생성 및 각 레벨에서 삽입                    │
│      new_node = SkipNode(value, new_level)                  │
│      for i = 0 to new_level:                                │
│          new_node.forward[i] = update[i].forward[i]         │
│          update[i].forward[i] = new_node                     │
│                                                              │
│  [삭제]                                                      │
│  ────────────────────────────────────────────                │
│                                                              │
│  function delete(skiplist, value):                           │
│      update = [None] * (MAX_LEVEL)                           │
│      current = skiplist.header                               │
│                                                              │
│      // 삭제 위치 찾기                                        │
│      for i = skiplist.level downto 0:                       │
│          while current.forward[i].value < value:            │
│              current = current.forward[i]                   │
│          update[i] = current                                 │
│                                                              │
│      // 노드가 존재하면 삭제                                   │
│      if current.forward[0].value == value:                  │
│          for i = 0 to skiplist.level:                       │
│              if update[i].forward[i] != current.forward[0]:  │
│                      break                                   │
│              update[i].forward[i] = current.forward[0].forward[i]
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- **관찰**: 스킵 리스트의 기대 높이는 O(log N)이다.
- **원인**: 각 레벨에 도달할 확률이 기하급수적으로 감소하기 때문이다.
- **결과**: 검색, 삽입, 삭제 모두 O(log N) 기대 시간을 가진다.
- **판단**: 레벨 할당에 Randomness를 사용하므로 최악의 경우 O(N)이 될 수 있지만, 확률적으로 극히 드물다.

📢 **섹션 요약 비유**: 스킵 리스트의 확률적 고도 할당은 **도시의 Buildings 높이 분포**와 같습니다. 모든 건물이同じ高さ이면(단순 리스트), 5층 건물을 가려면 모든 층을 지나야 한다. 그러나 도시에는 고층 건물이 있고(상위 레벨), 한 번에 빠르게 올라간 후 아래로 내려오면 효율적이다.新建건물의 높이도 확률적으로 결정된다.

---

## Ⅲ. 구현 및 실무 응용 (Implementation & Practice)

스킵 리스트의 실무 적용은 다음과 같다. **Redis Sorted Set**: 점수에 따라 정렬된 요소들의 모음으로, ZADD, ZRANGE 등의 명령어를 제공한다. 스킵 리스트를 기반으로 实现되어 있어 O(log N) 성능을 보장한다. **LevelDB/MemTable**: 키-값 저장소에서 메모리 내 인덱스로 활용된다.

**기타 활용**: **임시 데이터 정렬**: 데이터의 순서가 자주 변하지만 항상 정렬된 상태를 유지해야 하는 경우. **범위 질의**: 특정 범위의 데이터를 효율적으로 검색해야 하는 경우.

```text
[스킵 리스트 구현]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  import random                                               │
│                                                              │
│  MAX_LEVEL = 16  // 최대 레벨 (2^16 ≈ 65536 원소 지원)       │
│                                                              │
│  class SkipList:                                             │
│      def __init__(self):                                     │
│          self.header = SkipNode(None, MAX_LEVEL)              │
│          self.level = 0  // 현재 최대 레벨                    │
│                                                              │
│      def random_level(self):                                  │
│          level = 0                                           │
│          while random.random() < 0.5 and level < MAX_LEVEL:  │
│              level += 1                                     │
│          return level                                       │
│                                                              │
│      def insert(self, value):                                │
│          update = [None] * (MAX_LEVEL + 1)                   │
│          current = self.header                               │
│                                                              │
│          // 삽입 위치 찾기                                    │
│          for i in range(self.level, -1, -1):                │
│              while current.forward[i] and current.forward[i].value < value:
│                  current = current.forward[i]                 │
│              update[i] = current                             │
│                                                              │
│          // 이미 존재하면 업데이트                             │
│          if current.forward[0] and current.forward[0].value == value:
│              current.forward[0].value = value                │
│              return                                          │
│                                                              │
│          // 새 노드 삽입                                      │
│          new_level = self.random_level()                    │
│          if new_level > self.level:                         │
│              for i in range(self.level + 1, new_level + 1):│
│                  update[i] = self.header                     │
│              self.level = new_level                          │
│                                                              │
│          new_node = SkipNode(value, new_level)               │
│          for i in range(new_level + 1):                      │
│              new_node.forward[i] = update[i].forward[i]      │
│              update[i].forward[i] = new_node                 │
│                                                              │
│      def search(self, value):                               │
│          current = self.header                               │
│          for i in range(self.level, -1, -1):                │
│              while current.forward[i] and current.forward[i].value < value:
│                  current = current.forward[i]                 │
│          current = current.forward[0]                       │
│          if current and current.value == value:              │
│              return current                                  │
│          return None                                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 스킵 리스트 실무 활용은 **기차역 플랫폼 배치**와 같습니다. 모든 역에 정차하는Regional Train(lower 레벨)뿐 아니라 주요 역만 정차하는KTX(상위 레벨)가 있다.乘客은 먼저 KTX로 빠르게 이동한 후 Regional Train으로 목적지附近까지 이동한다.enna.

---

## Ⅳ. 품질 관리 및 테스트 (Quality & Testing)

스킵 리스트의 품질 관리에서 가장 중요한 것은 **무작위성 품질**과 **레벨 제한 관리**이다.

**품질 관리 체크리스트**: random_level() 함수의 무작위성이 충분히 좋은지 확인해야 한다. 레벨 0의 연결성이 깨지지 않았는지 확인해야 한다. Concurrent 접근 시 race condition을 방지하기 위한 동기화 메커니즘이 필요하다.

📢 **섹션 요약 비유**: 스킵 리스트品質 管理는 **카지노 주사위 공정성**과 같습니다. 주사위가 공정하게 제작되어야(무작위성) 모든 플레이어가平等의 기회를 가지고, 조작되면 특정 결과가 나와游戏的 재미가 없어진다. 스킵 리스트에서도 random_level()이 공정해야高水平 노드가 적절히 분포된다.

---

## Ⅴ. 최신 트렌드 및 결론 (Trends & Conclusion)

스킵 리스트의 최신 동향은 **병렬 처리**와 **고급 변형**과 관련되어 있다. **Lock-free 스킵 리스트**: Concurrent 접근을 허용하는 무잠금 구현. **배열 기반 스킵 리스트**: 포인터 대신 배열 인덱스를 사용하여 공간 효율성을 높임.

스킵 리스트는 "구현이 간단한 O(log N) 자료구조"로서, 균형 이진 트리의 대안으로 널리 활용된다.

📢 **섹션 요약 비유**: 스킵 리스트의 발전은 **우주탐사 로켓**과 같습니다.初期에는 단순한 로켓으로低軌道까지만 도달할 수 있었지만(단순 리스트), 엔진 기술을 발전시켜(고급 스킵 리스트) 더 높은 궤도(더 높은 레벨)로 진입할 수 있게 되었다. 또한, 다단계 로켓(병렬 처리)을 통해 더욱 효율적으로 목표에 도달할 수 있다.

---

## 핵심 인사이트 ASCII 다이어그램 (Concept Map)

```text
[스킵 리스트 (Skip List) 핵심 개념 맵]

         ┌─────────────────────────────────┐
         │        스킵 리스트 (Skip List)              │
         └────────────────┬────────────────┘
                          │
      ┌───────────────────┼───────────────────┐
      │                   │                    │
      ▼                   ▼                    ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  핵심 원리    │  │  시간 복잡도   │  │   실무 활용   │
│ 다중 레벨链表 │  │ O(log N)   │  │  Redis      │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ 확률적 고도   │  │ 기대값 기준   │  │ LevelDB     │
│ 할당        │  │ 균형 트리보다  │  │ 병렬 처리   │
│ 랜덤성      │  │ 구현 간단     │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

## 참고
- 모든 약어는 반드시 전체 명칭과 함께 표기
- 일어/중국어 절대 사용 금지
- 각 섹션 끝에 📢 요약 비유 반드시 추가
- 최소 800자/파일
- 파일명: 01_, 02_... 형식
