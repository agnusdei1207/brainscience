+++
title = "037. B+Tree (B+트리)"
date = "2026-03-05"
weight = 37
[extra]
categories = "studynotes-database"
tags = ["database", "index", "b-plus-tree", "rdbms", "range-query"]
+++

# 037. B+Tree (B+트리)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: B+Tree는 B-Tree를 개선한 인덱스 자료구조로, 모든 데이터를 리프 노드에만 저장하고 내부 노드는 탐색 경로(Route) 역할만 수행하며, 리프 노드 간 연결 리스트로 범위 검색을 최적화한다.
> 2. **가치**: 내부 노드에 데이터가 없어 더 많은 키를 저장할 수 있어 트리 높이가 낮아지고, 리프 노드 연결 리스트로 순차 접근이 O(n)으로 보장되어 현대 RDBMS 인덱스의 사실상 표준이다.
> 3. **융합**: MySQL InnoDB, Oracle, PostgreSQL 등 주요 RDBMS의 기본 인덱스 구조이며, 클러스터드/넌클러스터드 인덱스, 커버링 인덱스 등 다양한 최적화 기법의 기반이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**B+Tree**는 1970년대 후반에 B-Tree를 개선하여 만들어진 균형 트리로, 다음과 같은 핵심 특징을 갖는다:

1. **데이터 저장 위치**: 모든 실제 데이터(레코드/포인터)는 리프 노드에만 저장
2. **내부 노드 역할**: 키와 자식 포인터만 저장 (인덱스/라우팅 역할)
3. **리프 노드 연결**: 리프 노드들이 연결 리스트(Singly/Doubly Linked List)로 연결됨
4. **키 중복**: 내부 노드의 키가 리프 노드에 중복되어 존재 가능

### 💡 비유

B+Tree를 **다층 백화점**에 비유할 수 있다:
- **내부 노드**: 각 층의 안내 데스크 ("남성복은 3층, 여성복은 4층")
  - 실제 상품이 없고, 방향만 안내
  - 안내판은 작아서 많은 안내 정보를 담을 수 있음
- **리프 노드**: 실제 매장 층 (상품이 진열된 곳)
  - 모든 상품(데이터)이 여기에 있음
- **연결 리스트**: 각 매장 층의 에스컬레이터/이동 통로
  - 3층에서 4층으로 순차적으로 이동 가능
  - 범위 쇼핑("3층부터 5층까지 둘러보기")에 최적

**B-Tree와의 핵심 차이**: B-Tree는 안내 데스크에도 상품이 있지만, B+Tree는 안내 데스크는 순수 안내만!

### 등장 배경 및 발전 과정

1. **B-Tree의 한계 (1970년대)**:
   - 내부 노드에도 데이터가 있어 분기율(Fan-out)이 낮음
   - 범위 검색 시 비순차적 접근 발생
   - 노드 크기 대비 저장 효율이 낮음

2. **B+Tree의 등장**:
   - 내부 노드에서 데이터 제거 → 분기율 증가 → 트리 높이 감소
   - 리프 노드 연결 리스트 → 순차 접근 최적화
   - 범위 쿼리 성능 대폭 향상

3. **현대 RDBMS 채택**:
   - Oracle: 1979년부터 B+Tree 기반 인덱스
   - MySQL InnoDB: 클러스터드 B+Tree 인덱스
   - PostgreSQL: B-Tree (실제로는 B+Tree 변형)

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. B+Tree 구조 상세

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    B+TREE ARCHITECTURE (Order m = 4)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                           ┌─────────────┐                                   │
│                           │   [50]      │ ← Root (Internal Node)            │
│                           │  /    \     │   Only Keys, No Data              │
│                           └───┬─────┬───┘                                   │
│                        ┌──────┘     └──────┐                                │
│                        ▼                   ▼                                │
│              ┌─────────────────┐   ┌─────────────────┐                      │
│              │ [20 | 35]       │   │ [65 | 80]       │ ← Internal Nodes     │
│              │  /   |   \      │   │  /   |   \      │   Only Keys          │
│              └──────┼────┬─────┘   └──────┼────┬─────┘                      │
│          ┌──────────┘    └──────────┐  ┌───┘    └──────────┐               │
│          ▼               ▼          ▼  ▼                     ▼              │
│    ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐              │
│    │10|D|20|D  │→ │20|D|35|D  │→ │35|D|50|D  │→ │50|D|65|D  │              │
│    └───────────┘  └───────────┘  └───────────┘  └───────────┘              │
│          ↑              ↑              ↑              ↑                     │
│          └──────────────┴──────────────┴──────────────┘                     │
│                    Leaf Nodes (Linked List)                                 │
│                    All Data Stored Here                                     │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  LEGEND:                                                             │   │
│  │  • Internal Node: [K1 | K2] - Keys only, routing purpose            │   │
│  │  • Leaf Node: [K1 | D1 | K2 | D2] - Keys + Data/Pointers            │   │
│  │  • → : Linked List pointers (for range scan)                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. B+Tree 노드 구조 상세 분석

#### 내부 노드 (Internal Node)

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                    INTERNAL NODE STRUCTURE                               │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ Header | P0 | K0 | P1 | K1 | P2 | K2 | ... | K(n-1) | P(n)      │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  • Header: is_leaf=false, num_keys, etc.                                │
│  • Pi: Pointer to child i (i = 0 to n)                                  │
│  • Ki: Key i (i = 0 to n-1), Maximum n = m-1 keys                       │
│                                                                          │
│  Invariant:                                                              │
│  • P0 → all keys < K0                                                   │
│  • Pi → K(i-1) ≤ all keys < Ki                                          │
│  • P(n) → all keys ≥ K(n-1)                                             │
│                                                                          │
│  Fan-out = Number of pointers = num_keys + 1                            │
│  In B+Tree: Higher fan-out than B-Tree (no data in internal nodes)      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

#### 리프 노드 (Leaf Node)

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                    LEAF NODE STRUCTURE                                   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ Hdr | Prev | Next | K0,D0 | K1,D1 | K2,D2 | ... | K(n),D(n)     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  • Header: is_leaf=true, num_keys                                       │
│  • Prev: Pointer to previous leaf (for reverse scan)                    │
│  • Next: Pointer to next leaf (for forward range scan)                  │
│  • Ki,Di: Key-Data pairs                                                │
│                                                                          │
│  Data (Di) can be:                                                       │
│  1. Record Pointer (ROWID in Oracle, TID in PostgreSQL)                │
│  2. Full Record (Clustered Index in InnoDB)                             │
│  3. Primary Key (Secondary Index in InnoDB)                             │
│                                                                          │
│  Leaf Node Characteristics:                                              │
│  • Contains ALL keys (some duplicated from internal nodes)              │
│  • Linked horizontally for sequential access                            │
│  • Always at same depth (balanced tree)                                 │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 3. B+Tree 핵심 연산

#### 3.1 정확 일치 검색 (Point Query)

```python
def bplus_tree_search(node, key):
    """
    B+Tree 정확 일치 검색
    시간 복잡도: O(log n) - 항상 리프까지 내려감
    디스크 I/O: h회 (h = 트리 높이)

    Note: B-Tree와 달리 항상 리프 노드까지 내려감
    """
    # 리프 노드에 도달할 때까지
    while not node.is_leaf:
        i = 0
        # 이진 탐색으로 자식 찾기
        while i < node.num_keys and key >= node.keys[i]:
            i += 1
        node = disk_read(node.pointers[i])  # Disk I/O

    # 리프 노드에서 키 찾기
    for i in range(node.num_keys):
        if node.keys[i] == key:
            return node.data[i]  # 데이터 반환

    return None  # 키 없음
```

#### 3.2 범위 검색 (Range Query)

```python
def bplus_tree_range_search(node, start_key, end_key):
    """
    B+Tree 범위 검색
    핵심 장점: 리프 노드 연결 리스트 활용

    시간 복잡도: O(log n + k)
    - log n: 시작 위치 찾기
    - k: 결과 레코드 수
    """
    results = []

    # 1. 시작 키가 있는 리프 노드 찾기
    leaf = find_leaf(node, start_key)

    # 2. 리프 노드 연결 리스트를 따라 순차 검색
    while leaf is not None:
        for i in range(leaf.num_keys):
            if leaf.keys[i] > end_key:
                return results  # 범위 종료
            if leaf.keys[i] >= start_key:
                results.append(leaf.data[i])

        # 다음 리프 노드로 이동 (연결 리스트)
        leaf = leaf.next  # O(1) - 추가 디스크 I/O 없이 다음 노드

    return results
```

#### 3.3 삽입 (Insert) 연산

```python
def bplus_tree_insert(tree, key, data):
    """
    B+Tree 삽입 알고리즘

    핵심:
    1. 데이터는 항상 리프 노드에 삽입
    2. 리프 노드 분할 시 키가 부모로 승격
    3. 분할된 키가 리프에도 유지됨 (B-Tree와 차이)
    """

    # 1. 삽입할 리프 노드 찾기
    leaf = find_leaf(tree.root, key)

    # 2. 리프 노드에 공간이 있으면 삽입
    if leaf.num_keys < tree.max_keys:
        insert_into_leaf(leaf, key, data)
        return

    # 3. 리프 노드가 꽉 찼으면 분할
    insert_into_leaf_after_splitting(tree, leaf, key, data)


def insert_into_leaf_after_splitting(tree, leaf, key, data):
    """
    리프 노드 분할

    B-Tree와의 차이:
    - B-Tree: 중간 키가 부모로 이동, 자식 노드에서 제거
    - B+Tree: 중간 키가 부모로 복사(Copy-up), 리프 노드에 유지
    """
    # 임시 공간에 기존 키 + 새 키 정렬
    temp_keys = sorted(leaf.keys + [key])
    temp_data = sorted_by_key(leaf.data + [data])

    mid = len(temp_keys) // 2

    # 새 리프 노드 생성
    new_leaf = create_leaf_node()

    # 분할
    leaf.keys = temp_keys[:mid]
    leaf.data = temp_data[:mid]
    new_leaf.keys = temp_keys[mid:]
    new_leaf.data = temp_data[mid:]

    # 연결 리스트 갱신
    new_leaf.next = leaf.next
    leaf.next = new_leaf
    new_leaf.prev = leaf

    # 부모 노드에 중간 키 삽입 (Copy-up)
    # 핵심: 첫 번째 키를 부모로 복사, 리프에도 유지!
    insert_into_parent(tree, leaf, new_leaf.keys[0], new_leaf)


def insert_into_parent(tree, left, key, right):
    """
    부모 노드에 키 삽입
    전파되는 분할 처리
    """
    parent = left.parent

    # 루트 분할인 경우
    if parent is None:
        new_root = create_internal_node()
        new_root.keys = [key]
        new_root.pointers = [left, right]
        tree.root = new_root
        return

    # 부모에 공간이 있으면 삽입
    if parent.num_keys < tree.max_keys:
        insert_into_node(parent, key, right)
        return

    # 부모도 꽉 찼으면 분할
    insert_into_node_after_splitting(tree, parent, key, right)
```

### 4. B+Tree 실제 구현: MySQL InnoDB

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    InnoDB B+Tree Architecture                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CLUSTERED INDEX (Primary Key):                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │                         [PK: 50]                                    │   │
│  │                        /        \                                   │   │
│  │                 [PK: 25]        [PK: 75]                            │   │
│  │                 /    \          /    \                              │   │
│  │            [10,Full] [25,Full] [50,Full] [75,Full]                  │   │
│  │                                                                     │   │
│  │  • Leaf nodes contain FULL ROW DATA                                │   │
│  │  • Data is physically ordered by Primary Key                       │   │
│  │  • Secondary indexes point to PK, not directly to data             │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  SECONDARY INDEX (Non-Unique):                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │                      [Name: 'Kim']                                  │   │
│  │                      /          \                                   │   │
│  │            ['Hong','Lee']    ['Park','Yoon']                        │   │
│  │                                                                     │   │
│  │  Leaf: [Name, PK] pairs → Then lookup Clustered Index              │   │
│  │                                                                     │   │
│  │  Example:                                                           │   │
│  │  Leaf Node: [('Hong', 10), ('Lee', 25), ('Park', 50)]              │   │
│  │              ↓            ↓            ↓                            │   │
│  │         Find PK=10, PK=25, PK=50 in Clustered Index                │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Page Size: 16KB (default)                                                 │
│  • Each node = One Page                                                    │
│  • ~1000 keys per internal node (assuming 16-byte keys)                    │
│  • Height 3 can index ~1 billion rows                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5. B+Tree 성능 분석

#### 높이 계산 (MySQL InnoDB 기준)

```
InnoDB Page Size: 16KB
Average Key Size: 16 bytes (e.g., BIGINT)
Pointer Size: 6 bytes (InnoDB internal pointer)

Internal Node Capacity:
  Keys per page ≈ 16KB / (16 + 6) ≈ 727 keys
  Fan-out ≈ 728 children

Maximum Rows Indexable:
  Height 1: 727 rows (root is leaf)
  Height 2: 727 × 727 ≈ 528,529 rows
  Height 3: 727 × 727 × 727 ≈ 384 million rows
  Height 4: 727 × 727 × 727 × 727 ≈ 279 billion rows

결론: 대부분의 실무 테이블은 Height 3 이내!
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. B-Tree vs B+Tree 심층 비교

| 비교 항목 | B-Tree | B+Tree | 설명 |
|:---|:---|:---|:---|
| **데이터 저장** | 모든 노드 | 리프 노드만 | B+Tree가 내부 노드에 더 많은 키 저장 |
| **키 중복** | 없음 | 리프에 중복 가능 | B+Tree는 키가 내부/리프 모두 존재 가능 |
| **범위 검색** | 비효율적 | 최적화 | B+Tree 리프 연결 리스트 |
| **트리 높이** | 상대적으로 높음 | 상대적으로 낮음 | B+Tree 분기율(Fan-out) 높음 |
| **검색 일관성** | 변동 (노드별 상이) | 일관됨 (항상 리프) | B+Tree는 항상 동일한 I/O |
| **공간 효율** | 중간 | 높음 | B+Tree 내부 노드가 작음 |

### 2. 인덱스 유형별 B+Tree 활용

| 인덱스 유형 | 데이터 저장 방식 | B+Tree 구조 | 사용 사례 |
|:---|:---|:---|:---|
| **클러스터드 인덱스** | 리프에 전체 레코드 | 리프 = 데이터 페이지 | PK, 빈번 범위 조회 |
| **넌클러스터드 인덱스** | 리프에 ROWID/PK | 리프 = 포인터 | 일반 인덱스 |
| **커버링 인덱스** | 리프에 조회 컬럼 포함 | INCLUDE 컬럼 | 인덱스만으로 조회 완료 |
| **유니크 인덱스** | 동일 + 중복 방지 | 제약조건 추가 | 고유 식별자 |

### 3. DBMS별 B+Tree 구현 차이

| DBMS | 페이지 크기 | 클러스터드 인덱스 | 특징 |
|:---|:---|:---|:---|
| **MySQL InnoDB** | 16KB | PK 기본 | 세컨더리 인덱스가 PK 참조 |
| **Oracle** | 8KB | 선택적 | 리프에 ROWID 저장 |
| **PostgreSQL** | 8KB | 없음 |Heap Table + 모든 인덱스가 넌클러스터드 |
| **SQL Server** | 8KB | PK 또는 지정 | 클러스터드/넌클러스터드 구분 |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 시나리오 1: 대규모 이커머스 상품 검색

**문제 상황**: 1억 개 상품, 카테고리별 + 가격 범위 검색 요구

**기술사적 결단**:
1. **복합 인덱스 설계**: `(category_id, price)` 복합 B+Tree 인덱스
2. **커버링 인덱스**: 자주 조회되는 `product_name, thumbnail_url` INCLUDE
3. **파티셔닝**: 카테고리별 파티션으로 프루닝 효과

```sql
-- MySQL InnoDB 예시
CREATE INDEX idx_category_price
ON products (category_id, price)
INCLUDE (product_name, thumbnail_url, stock_qty);
```

### 시나리오 2: 시계열 데이터 인덱싱

**문제 상황**: 로그 데이터 10억 건, 시간 범위 조회 최적화

**기술사적 결단**:
1. **B+Tree + 파티셔닝**: 일별/월별 파티션
2. **Fill Factor 100%**: 로그는 UPDATE 없음 → 공간 효율 극대화
3. **Cold/Hot 분리**: 최근 데이터만 빠른 스토리지

### 도입 시 고려사항 (체크리스트)

**설계 체크리스트**
- [ ] 클러스터드 vs 넌클러스터드 인덱스 선택
- [ ] 복합 인덱스 컬럼 순서 (선행 컬럼 활용)
- [ ] Fill Factor 설정 (쓰기 빈도 고려)
- [ ] 페이지 크기와 예상 데이터 양

**운영 체크리스트**
- [ ] 인덱스 높이 모니터링
- [ ] 단편화율 확인 및 REBUILD 주기
- [ ] 통계 정보 갱신 빈도

### 안티패턴 (Anti-patterns)

1. **과도한 세컨더리 인덱스**: 쓰기 성능 저하, InnoDB 경우 2회 탐색
2. **낮은 선택도 컬럼 선행**: 인덱스 효율 저하
3. **클러스터드 인덱스에 긴 컬럼**: 리프 노드 크기 증가 → 분할 빈번

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 항목 | 풀 스캔 | B+Tree 인덱스 | 개선 효과 |
|:---|:---|:---|:---|
| **포인트 쿼리** | O(n) | O(log n) | 수천~수백만 배 |
| **범위 쿼리 (k건)** | O(n) | O(log n + k) | 선형 → 로그+선형 |
| **디스크 I/O** | n/pagesize | h (3~4) | 99.9% 감소 |
| **순차 스캔** | 최적 | 최적 (리프 링크) | 동일 |

### 미래 전망 및 진화 방향

1. **Learned Index**: ML 기반 인덱스로 B+Tree 대체 시도 (Google, MIT 연구)
2. **Hybrid Index**: 워크로드에 따라 B+Tree/Hash/LSM 자동 전환
3. **Persistent Memory B+Tree**: Intel Optane 등 NVM 최적화

### ※ 참고 표준/가이드

- **MySQL 8.0 Reference Manual**: InnoDB Index Structure
- **Oracle Database Concepts**: B-Tree Indexes
- **PostgreSQL Documentation**: Index Types

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [[036_B-Tree]](./36_b_tree.md): B+Tree의 기반이 되는 균형 트리
- [[154_인덱스_기본]](./154_index_basic.md): B+Tree 기반 인덱스 개념
- [[159_클러스터드_인덱스]](./159_clustered_index.md): 물리적 정렬 인덱스
- [[160_넌클러스터드_인덱스]](./160_nonclustered_index.md): 보조 인덱스
- [[161_결합_인덱스]](./161_composite_index.md): 다중 컬럼 인덱스

---

## 👶 어린이를 위한 3줄 비유 설명

1. **B+Tree는 상품이 1층에만 있는 백화점이에요**: 2층, 3층은 안내 데스크만 있고, 모든 상품(데이터)은 1층 매장(리프 노드)에만 있어요. 그래서 안내판이 아주 많은 정보를 담을 수 있답니다.

2. **1층 매장들이 서로 연결되어 있어요**: 1층의 왼쪽 매장에서 오른쪽 매장으로 쭉~ 걸어갈 수 있어요. 그래서 "빨간 옷부터 파란 옷까지 보여줘!"라고 하면 쭉~ 걸어가면서 볼 수 있어요.

3. **상품을 찾는 엘리베이터 이동이 아주 적어요**: 안내 데스크가 효율적이라서, 아무리 많은 상품이 있어도 엘리베이터를 3~4번만 타면 원하는 상품을 찾을 수 있어요!
