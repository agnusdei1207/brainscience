+++
title = "036. B-Tree (다진 탐색 트리)"
date = "2026-03-05"
weight = 36
[extra]
categories = "studynotes-database"
tags = ["database", "index", "b-tree", "data-structure", "disk-io"]
+++

# 036. B-Tree (다진 탐색 트리)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: B-Tree는 1972년 Rudolf Bayer가 제안한 자가 균형 다진 탐색 트리(Self-balancing M-ary Search Tree)로, 디스크 I/O를 최소화하기 위해 노드당 여러 키를 저장하고 트리의 높이를 낮게 유지하는 핵심 인덱스 자료구조다.
> 2. **가치**: O(log n)의 검색/삽입/삭제 시간 복잡도를 보장하며, 블록 단위 디스크 접근 패턴에 최적화되어 대용량 데이터베이스의 인덱스 표준 자료구조로 자리 잡았다.
> 3. **융합**: 운영체제의 페이지 캐싱, 파일 시스템의 블록 관리, 데이터베이스의 버퍼 풀과 밀접하게 연동되며, B+Tree로 진화하여 현대 RDBMS의 기본 인덱스 구조가 되었다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**B-Tree(Balanced Tree, B트리)**는 이진 탐색 트리를 일반화한 다진 탐색 트리(M-ary Search Tree)로, 다음 특성을 갖는 자가 균형 트리다:

1. **모든 리프 노드가 동일한 깊이**: 균형 유지로 검색 성능 보장
2. **노드당 다수의 키 저장**: 한 노드에 여러 키와 포인터를 저장
3. **최소 50% 채움 보장**: (차수 m 기준) 각 노드는 최소 ⌈m/2⌉개의 키를 가짐
4. **디스크 친화적 설계**: 노드 크기를 디스크 블록 크기와 일치시켜 I/O 최소화

### 💡 비유

B-Tree를 **다층 주차장**에 비유할 수 있다:
- **루트 노드**: 주차장 입구의 안내판 ("A-D층은 왼쪽, E-H층은 오른쪽")
- **내부 노드**: 각 층의 안내표지 ("A-B는 앞쪽, C-D는 뒤쪽")
- **리프 노드**: 실제 주차 공간
- **키 값**: 차량 번호 또는 층수
- **분할(Split)**: 주차장이 꽉 차면 새로운 층을 추가
- **병합(Merge)**: 주차 공간이 비면 층을 합침

이진 트리가 2개의 선택지(왼쪽/오른쪽)만 제공한다면, B-Tree는 각 층에서 수백 개의 선택지를 제공하여 엘리베이터(디스크 헤드) 이동 횟수를 획기적으로 줄인다.

### 등장 배경 및 발전 과정

1. **이진 탐색 트리의 한계 (1960년대)**:
   - 최악의 경우 O(n)까지 퇴보 (편향 트리)
   - 메모리 기반 설계로 디스크 접근 비용 고려 안 함
   - 노드당 1개 키만 저장 → 깊이 증가 → 디스크 I/O 폭증

2. **B-Tree의 탄생 (1972년)**:
   - Rudolf Bayer와 Edward McCreight가 "Organization and Maintenance of Large Ordered Indexes" 논문 발표
   - 디스크 기반 데이터베이스를 위한 최적화된 구조 제안
   - 노드 크기를 디스크 블록(보통 4KB~8KB)과 일치시켜 1회 I/O로 여러 키 처리

3. **B+Tree로의 진화 (1970년대 후반)**:
   - 리프 노드에만 실제 데이터 저장
   - 리프 노드 간 연결 리스트로 범위 검색 최적화
   - 현대 RDBMS(MySQL InnoDB, Oracle, PostgreSQL)의 표준

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. B-Tree 구조 상세

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    B-TREE STRUCTURE (Order m = 3)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌─────────────────────┐                             │
│                         │    [50 | 80]        │ ← Root Node                 │
│                         │   /   |    \        │   (2 keys, 3 pointers)      │
│                         └───────┼─────┬───────┘                             │
│                    ┌─────────────┘     └─────────────┐                      │
│                    ▼                               ▼                       │
│         ┌──────────────────┐           ┌──────────────────┐                │
│         │  [20 | 35]       │           │  [65 | 75]       │                │
│         │  /   |    \      │           │  /   |    \      │                │
│         └──────┼─────┬─────┘           └──────┼─────┬─────┘                │
│        ┌───────┘     └───────┐        ┌───────┘     └───────┐              │
│        ▼                     ▼        ▼                     ▼              │
│  ┌──────────┐        ┌──────────┐  ┌──────────┐       ┌──────────┐         │
│  │ [10 | 15]│        │ [25 | 30]│  │ [55 | 60]│       │ [85 | 90]│         │
│  └──────────┘        └──────────┘  └──────────┘       └──────────┘         │
│       ↑                   ↑            ↑                   ↑               │
│       └───────────────────┴────────────┴───────────────────┘               │
│                          Leaf Nodes (All same depth)                        │
│                                                                             │
│  Properties:                                                                │
│  • Order m = 3: Max 2 keys per node, Min 1 key per non-root node           │
│  • Height = 3: Maximum 3 disk I/Os to find any key                         │
│  • All leaves at same depth: Guaranteed O(log n) search                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. B-Tree 노드 구조 상세 분석

| 구성 요소 | 설명 | 크기 (일반적) | 역할 |
|:---|:---|:---|:---|
| **키 (Keys)** | 정렬된 검색 키 값들 | 가변 (최대 m-1개) | 탐색 경로 결정 |
| **포인터 (Pointers)** | 자식 노드 주소 | m개 | 다음 레벨 연결 |
| **데이터 (Data)** | 실제 레코드 또는 포인터 | 가변 | 리프 노드에 저장 |
| **노드 헤더** | 노드 메타데이터 | 8~16 bytes | 키 개수, 리프 여부 등 |

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    B-TREE NODE INTERNAL STRUCTURE                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────┐       │
│  │ Hdr │ P0   │ K0   │ P1   │ K1   │ P2   │ K2   │ P3   │ ... │       │
│  │     │      │      │      │      │      │      │      │     │       │
│  └─────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴─────┘       │
│                                                                         │
│  Hdr = Node Header (is_leaf, num_keys, etc.)                           │
│  P0, P1, P2... = Child Pointers (m개, m = order)                       │
│  K0, K1, K2... = Keys (m-1개)                                          │
│                                                                         │
│  Invariant: P0 → keys < K0 < P1 → keys < K1 < P2 → keys < ...         │
│                                                                         │
│  Key Range for Pi:                                                      │
│  • P0: (-∞, K0)                                                        │
│  • Pi: (K(i-1), Ki) for 0 < i < num_keys                              │
│  • P(num_keys): (K(num_keys-1), +∞)                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. B-Tree 핵심 연산

#### 3.1 검색 (Search) 연산

```python
def btree_search(node, key):
    """
    B-Tree 검색 알고리즘
    시간 복잡도: O(log n) - 트리 높이에 비례
    디스크 I/O: O(h) - h는 트리 높이

    Args:
        node: 현재 노드 (루트에서 시작)
        key: 검색할 키 값

    Returns:
        (found, node, index) 또는 (False, None, None)
    """
    i = 0

    # 현재 노드에서 키 위치 찾기
    while i < node.num_keys and key > node.keys[i]:
        i += 1

    # 키를 찾은 경우
    if i < node.num_keys and key == node.keys[i]:
        return (True, node, i)

    # 리프 노드이면 키가 없음
    if node.is_leaf:
        return (False, None, None)

    # 자식 노드로 이동 (디스크 I/O 발생)
    child = disk_read(node.pointers[i])  # ← Disk I/O
    return btree_search(child, key)
```

#### 3.2 삽입 (Insert) 연산 - 분할(Split) 메커니즘

```python
def btree_insert(tree, key):
    """
    B-Tree 삽입 알고리즘
    핵심: 삽입 전에 분할을 미리 수행 (Proactive Splitting)

    1. 리프 노드에 공간이 있으면 그냥 삽입
    2. 공간이 없으면 노드를 분할 후 삽입
    3. 분할이 상위로 전파될 수 있음
    """

    root = tree.root

    # 루트가 꽉 찼으면 미리 분할
    if root.num_keys == tree.max_keys:
        new_root = create_node(is_leaf=False)
        new_root.pointers[0] = root
        btree_split_child(new_root, 0)
        tree.root = new_root
        btree_insert_nonfull(new_root, key)
    else:
        btree_insert_nonfull(root, key)


def btree_split_child(parent, index):
    """
    노드 분할 핵심 알고리즘

    Before Split (y is full, m=5, max_keys=4):
    ┌────────────────────────────────┐
    │  [10 | 20 | 30 | 40 | 50]      │ ← Node y (full)
    └────────────────────────────────┘

    After Split:
         ┌─────────────┐
         │  [30]       │ ← Middle key promoted
         └──────┬──────┘
           ┌────┴────┐
           ▼         ▼
    ┌───────────┐  ┌───────────┐
    │[10 | 20]  │  │[40 | 50]  │
    └───────────┘  └───────────┘
     Node y         Node z (new)
    """
    y = parent.pointers[index]  # 분할할 노드
    z = create_node(is_leaf=y.is_leaf)  # 새 노드

    # 중간값 계산
    mid = tree.order // 2  # t = ceil(m/2)
    mid_key = y.keys[mid]

    # 키 복사 (중간 이후 → 새 노드)
    z.num_keys = tree.order - mid - 1
    for j in range(z.num_keys):
        z.keys[j] = y.keys[mid + 1 + j]

    # 포인터 복사 (내부 노드인 경우)
    if not y.is_leaf:
        for j in range(z.num_keys + 1):
            z.pointers[j] = y.pointers[mid + 1 + j]

    # 원래 노드 크기 조정
    y.num_keys = mid

    # 부모 노드에 중간 키 삽입
    for j in range(parent.num_keys, index, -1):
        parent.pointers[j + 1] = parent.pointers[j]
        parent.keys[j] = parent.keys[j - 1]

    parent.keys[index] = mid_key
    parent.pointers[index + 1] = z
    parent.num_keys += 1

    # 디스크 쓰기
    disk_write(parent)
    disk_write(y)
    disk_write(z)


def btree_insert_nonfull(node, key):
    """공간이 있는 노드에 삽입"""
    i = node.num_keys - 1

    if node.is_leaf:
        # 리프 노드: 올바른 위치에 키 삽입
        while i >= 0 and key < node.keys[i]:
            node.keys[i + 1] = node.keys[i]
            i -= 1
        node.keys[i + 1] = key
        node.num_keys += 1
        disk_write(node)
    else:
        # 내부 노드: 적절한 자식으로 이동
        while i >= 0 and key < node.keys[i]:
            i -= 1
        i += 1

        # 자식이 꽉 찼으면 미리 분할
        child = disk_read(node.pointers[i])
        if child.num_keys == tree.max_keys:
            btree_split_child(node, i)
            if key > node.keys[i]:
                i += 1

        btree_insert_nonfull(disk_read(node.pointers[i]), key)
```

#### 3.3 삭제 (Delete) 연산 - 병합(Merge) 메커니즘

```python
def btree_delete(node, key):
    """
    B-Tree 삭제 알고리즘
    핵심: 삭제 전에 최소 키 개수를 보장 (Proactive Merging/Borrowing)

    Cases:
    1. 키가 리프 노드에 있음 → 바로 삭제
    2. 키가 내부 노드에 있음 → predecessor/successor로 대체
    3. 자식이 최소 키 개수 → borrow 또는 merge
    """
    idx = find_key_index(node, key)

    # Case 1: 키가 이 노드에 있고 리프 노드
    if idx < node.num_keys and node.keys[idx] == key:
        if node.is_leaf:
            remove_from_leaf(node, idx)
        else:
            remove_from_internal(node, idx)
        return

    # 키가 이 노드에 없음
    if node.is_leaf:
        raise KeyError(f"Key {key} not found")

    # 자식 노드로 재귀
    flag = (idx == node.num_keys)

    # 자식이 최소 키 개수면 채워줌
    child = disk_read(node.pointers[idx])
    if child.num_keys < tree.min_keys:
        fill_child(node, idx)

    # fill 후 인덱스 조정
    if flag and idx > node.num_keys:
        btree_delete(node.pointers[idx - 1], key)
    else:
        btree_delete(node.pointers[idx], key)


def remove_from_internal(node, idx):
    """내부 노드에서 키 삭제"""
    k = node.keys[idx]

    # 왼쪽 자식이 충분하면 predecessor 사용
    left_child = disk_read(node.pointers[idx])
    if left_child.num_keys >= tree.min_keys:
        pred = get_predecessor(left_child)
        node.keys[idx] = pred
        btree_delete(left_child, pred)
        return

    # 오른쪽 자식이 충분하면 successor 사용
    right_child = disk_read(node.pointers[idx + 1])
    if right_child.num_keys >= tree.min_keys:
        succ = get_successor(right_child)
        node.keys[idx] = succ
        btree_delete(right_child, succ)
        return

    # 둘 다 불충분하면 병합
    merge_children(node, idx)
    btree_delete(left_child, k)


def fill_child(node, idx):
    """자식 노드가 최소 키 개수 미만일 때 채우기"""

    # 왼쪽 형제에서 빌려오기
    if idx > 0:
        left_sibling = disk_read(node.pointers[idx - 1])
        if left_sibling.num_keys > tree.min_keys:
            borrow_from_prev(node, idx)
            return

    # 오른쪽 형제에서 빌려오기
    if idx < node.num_keys:
        right_sibling = disk_read(node.pointers[idx + 1])
        if right_sibling.num_keys > tree.min_keys:
            borrow_from_next(node, idx)
            return

    # 빌려올 수 없으면 병합
    if idx > 0:
        merge_children(node, idx - 1)
    else:
        merge_children(node, idx)
```

### 4. B-Tree vs B+Tree 비교

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    B-TREE vs B+TREE COMPARISON                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  B-TREE:                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     [50 | Data50]                                   │   │
│  │                    /       \                                        │   │
│  │          [30 | Data30]     [70 | Data70]                            │   │
│  │          /     \            /      \                                │   │
│  │    [20|D20] [40|D40]    [60|D60] [80|D80]                           │   │
│  │                                                                     │   │
│  │  • Data stored in ALL nodes (internal + leaf)                      │   │
│  │  • No linked list between leaves                                    │   │
│  │  • Single search path to data                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  B+TREE:                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     [50 | 70]           ← Internal: Keys only       │   │
│  │                    /       \                                         │   │
│  │          [30]          [60 | 70]        ← Internal: Keys only       │   │
│  │          /    \         /    \                                       │   │
│  │    [20|D20]→[30|D30]→[40|D40]→[50|D50]→[60|D60]→[70|D70]            │   │
│  │              ↑_________________________________________↑             │   │
│  │                    Linked List at Leaf Level                        │   │
│  │                                                                     │   │
│  │  • Data stored ONLY in leaf nodes                                   │   │
│  │  • Leaf nodes linked (sequential access)                            │   │
│  │  • Internal nodes have duplicate keys (for routing)                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Key Difference for RDBMS:                                                  │
│  • B+Tree: Better for range queries (linked list traversal)                │
│  • B+Tree: More keys per internal node (no data → more branching)          │
│  • B+Tree: Consistent query performance (always reach leaf)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5. B-Tree 수학적 분석

#### 높이 계산

```
B-Tree의 최소 높이 h (차수 m, 키 개수 n):

각 내부 노드는 최소 ⌈m/2⌉개의 자식을 가짐
따라서 최소 노드 개수:
  Level 0: 1 (root)
  Level 1: 2
  Level 2: 2⌈m/2⌉
  Level 3: 2⌈m/2⌉²
  ...
  Level h: 2⌈m/2⌉^(h-1)

최소 리프 노드 개수: 2⌈m/2⌉^(h-1)

최소 키 개수:
n ≥ 1 + 2(⌈m/2⌉ - 1) + 2⌈m/2⌉(⌈m/2⌉ - 1) + ... + 2⌈m/2⌉^(h-1)(⌈m/2⌉ - 1)
n ≥ 1 + 2(⌈m/2⌉^(h-1) - 1)(⌈m/2⌉ - 1) / (⌈m/2⌉ - 1)
n ≥ 2⌈m/2⌉^(h-1) - 1

따라서:
h ≤ log_⌈m/2⌉((n+1)/2)

예시: m = 100, n = 1,000,000
h ≤ log_50(500,000.5) ≈ 3.15 → 최대 4 레벨 (4회 디스크 I/O)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 인덱스 자료구조 비교

| 특성 | B-Tree | B+Tree | Hash Index | LSM-Tree |
|:---|:---|:---|:---|:---|
| **검색 시간** | O(log n) | O(log n) | O(1) 평균 | O(log n) |
| **범위 검색** | 가능 | 최적화 | 불가능 | 가능 |
| **공간 효율** | 중간 | 높음 (내부 노드) | 높음 | 높음 |
| **쓰기 성능** | 중간 | 중간 | 높음 | 매우 높음 |
| **주요 용도** | 파일 시스템 | RDBMS 인덱스 | 메모리 DB | NoSQL |
| **디스크 친화도** | 높음 | 매우 높음 | 낮음 | 높음 |

### 2. 데이터베이스 시스템별 B-Tree/B+Tree 구현

| DBMS | 인덱스 구조 | 노드 크기 | 특징 |
|:---|:---|:---|:---|
| **MySQL InnoDB** | B+Tree | 16KB (페이지) | 클러스터드 인덱스, 리프 노드에 전체 레코드 |
| **Oracle B-Tree** | B+Tree | 8KB (블록) | 리프 노드에 ROWID 저장 |
| **PostgreSQL B-Tree** | B+Tree | 8KB (페이지) | MVCC 지원, 여러 버전 관리 |
| **SQL Server** | B+Tree | 8KB (페이지) | 클러스터드/넌클러스터드 구분 |

### 3. 과목 융합: 운영체제와 B-Tree

| 운영체제 개념 | B-Tree와의 연관 |
|:---|:---|
| **페이지 캐시** | B-Tree 노드 = OS 페이지, 캐시 히트 시 메모리 접근 |
| **디스크 스케줄링** | 순차 접근 vs 랜덤 접근, B-Tree 리프 링크 활용 |
| **버퍼 관리** | LRU로 B-Tree 노드 교체, 핫 노드 캐싱 |
| **파일 시스템** | B-Tree 기반 디렉토리 구조 (ReiserFS, HFS+) |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 시나리오 1: 대용량 테이블 인덱스 설계

**문제 상황**: 1억 건의 사용자 로그 테이블에 인덱스 생성 필요

**기술사적 결단**:
1. **B+Tree 선택**: 범위 조회가 빈번하므로 B+Tree가 유리
2. **페이지 크기 최적화**: 기본 8KB vs 16KB 트레이드오프 분석
3. **Fill Factor 설정**: 쓰기 빈도에 따라 70~90% 조정

### 시나리오 2: 인덱스 단편화 해결

**문제 상황**: 잦은 INSERT/DELETE로 인덱스 단편화 발생, 성능 저하

**기술사적 결단**:
1. **주기적 REBUILD**: `ALTER INDEX ... REBUILD`
2. **Fill Factor 조정**: 더 낮은 Fill Factor로 여유 공간 확보
3. **파티셔닝 고려**: 대량 데이터는 파티션 단위로 관리

### 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] 예상 데이터 양과 트리 높이 계산
- [ ] 디스크 블록 크기와 노드 크기 매핑
- [ ] 메모리 버퍼 풀 크기와 캐시 히트율
- [ ] 동시성 제어 (래치 vs 락)

**운영적 고려사항**
- [ ] 인덱스 모니터링 (깊이, 단편화율)
- [ ] 주기적 유지보수 계획
- [ ] 백업 시 인덱스 포함 여부

### 안티패턴 (Anti-patterns)

1. **과도한 인덱스 생성**: 쓰기 성능 저하, 저장 공간 낭비
2. **낮은 선택도 컬럼 인덱싱**: B-Tree 효율 저하 (비트맵 인덱스 고려)
3. **인덱스 컬럼 순서 무시**: 결합 인덱스 선행 컬럼 미사용

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 항목 | 풀 스캔 | B-Tree 인덱스 스캔 | 개선 효과 |
|:---|:---|:---|:---|
| **검색 시간 (1억 건)** | ~30초 | ~10ms | 3,000배 향상 |
| **디스크 I/O** | 1,000,000+ | 3~4 | 99.9% 감소 |
| **범위 조회 (1만 건)** | ~30초 | ~100ms | 300배 향상 |

### 미래 전망 및 진화 방향

1. **Adaptive B-Tree**: 워크로드 패턴에 따라 자동으로 구조 최적화
2. **Hybrid Index**: B-Tree + Hash 결합으로 다양한 쿼리 패턴 지원
3. **NVMe 최적화 B-Tree**: SSD 특성을 고려한 노드 크기 및 분할 전략

### ※ 참고 표준/가이드

- **Rudolf Bayer (1972)**: "Organization and Maintenance of Large Ordered Indexes"
- **Knuth, TAOCP Vol. 3**: Sorting and Searching
- **Database System Concepts (Silberschatz)**: Indexing Chapter

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [[037_B+Tree]](./37_b_plus_tree.md): B-Tree를 개선한 RDBMS 표준 인덱스 구조
- [[054_옵티마이저]](./54_optimizer.md): B-Tree 인덱스를 활용한 실행 계획 수립
- [[050_버퍼_풀]](./50_buffer_pool.md): B-Tree 노드 캐싱을 통한 I/O 최소화
- [[033_파일_저장_구조]](./33_file_storage_structure.md): 디스크 블록과 B-Tree 노드 매핑
- [[해시_인덱스]](./57_hash_index.md): 등등 검색에 특화된 대안 인덱스

---

## 👶 어린이를 위한 3줄 비유 설명

1. **B-Tree는 엘리베이터가 많은 주차장이에요**: 일반 주차장은 2층만 있지만, B-Tree 주차장은 각 층마다 수백 개의 구역이 있어서 원하는 차를 찾을 때 엘리베이터를 타는 횟수가 아주 적어요.

2. **한 층에 여러 차가 들어가요**: B-Tree의 각 층(노드)에는 여러 대의 차(데이터)가 들어갈 수 있어서, 엘리베이터가 멈추는 횟수를 줄일 수 있답니다.

3. **층이 꽉 차면 새 층을 만들어요**: 한 층이 꽉 차면 자동으로 층을 나눠서, 주차장이 항상 효율적으로 정리되요. 그래서 차를 찾는 시간이 절대 길어지지 않아요!
