+++
weight = 88
title = "31. AVL 트리 — 자가 균형 이진 탐색 트리"
date = "2026-04-29"
[extra]
categories = "studynote-algorithm-stats"
+++

## 0. 핵심 인사이트

> **핵심**: AVL 트리는 모든 노드에서 왼쪽·오른쪽 서브트리 높이 차이(Balance Factor)가 최대 1인 자가 균형(Self-balancing) BST(Binary Search Tree)다. Adelson-Velsky & Landis(1962)가 발명했다.
> **비유**: AVL 트리은(는) 물건을 자주 꺼내는 방식에 맞춰 서랍과 선반의 구조를 설계하는 것과 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
BST 불균형 문제:
  순차 삽입 [1, 2, 3, 4, 5]:
      1
               2
                   3
                       4
                           5
  → 연결 리스트와 같아짐: 검색 O(N)

AVL 트리: 자동 균형 유지
      3
     /     2   4
   /       1       5
  → 항상 O(log N) 검색
```

- **📢 섹션 요약 비유**: BST는 무질서한 책장이다. 순서대로만 책을 꽂으면 한쪽으로 기울어진 탑이 된다. AVL 트리는 자동 정리 로봇이 있어서 한쪽이 기울면 즉시 재배치하는 균형 잡힌 책장이다.

---

## 2. 구성요소

### Balance Factor와 회전

```text
Balance Factor (BF) = 왼쪽 높이 - 오른쪽 높이

BF = -1, 0, 1 → 균형 상태
BF ≤ -2 또는 BF ≥ 2 → 불균형 → 회전 필요

4가지 회전:
  LL 불균형: 단순 우회전
      Z(BF=2)         Y
     /              /       Y(BF=1)  →    X     Z
   /
  X

  RR 불균형: 단순 좌회전 (LL의 반대)
  LR 불균형: 좌회전 후 우회전 (이중 회전)
  RL 불균형: 우회전 후 좌회전 (이중 회전)
```

### 높이와 성능

```text
N개 노드 AVL 트리:
  최소 높이: ⌊log₂N⌋
  최대 높이: 1.44 × log₂(N+2)

  N=1000:
  최소 높이: 9
  최대 높이: ≈ 14
  BST 최악:  999 (퇴화 시)

→ AVL은 최악에도 1.44× log N으로 제한
```

- **📢 섹션 요약 비유**: AVL 회전은 시소 균형 맞추기다. 한쪽이 너무 무거워지면(BF ≥ 2) 지렛대(회전)로 균형을 맞춘다. 회전 방향은 기울어진 방향에 따라 결정된다.

---

## 3. 구조 및 원리

**핵심 조건**: AVL 트리의 성능은 메모리 배치, 접근 패턴, 불변식 유지 비용에 의해 결정된다. 탐색·삽입·삭제가 어떤 경로로 일어나는지와 재구성 비용을 함께 봐야 한다.

동작 순서:
1. 저장 구조와 불변식을 정의한다.
2. 삽입·삭제·탐색 요청이 들어오면 인덱스나 포인터 경로를 따라 위치를 찾는다.
3. 구조가 깨질 경우 회전·재해시·분할·병합 같은 복구 연산을 수행한다.
4. 최종 결과를 반환하고, 다음 연산에서도 성능이 유지되도록 상태를 보존한다.

```
요청 입력
  ↓
위치 계산 또는 경로 탐색
  ↓
노드/배열 상태 갱신
  ↓
불변식 점검
  ↓
조회/수정 결과 반환 (AVL 트리)
```

| 비교 | AVL | Red-Black | B-Tree |
|:---|:---|:---|:---|
| 균형 엄격도 | 엄격 (BF±1) | 유연 (2배 높이차 허용) | N차 분기 |
| 검색 | 약간 빠름 | 약간 느림 | 디스크 최적화 |
| 삽입/삭제 | 약간 느림 | 약간 빠름 | I/O 최소화 |
| 활용 | 읽기 집중 | STL/JVM | DB·파일시스템 |

- **📢 섹션 요약 비유**: AVL·RB·B-Tree는 세 가지 정리정돈 스타일이다. AVL(완벽한 좌우 균형), RB(대충 균형하지만 빠른 수정), B-Tree(한 칸에 여러 책, 디스크 효율)로 각각 다른 강점이 있다.

---

## 4. 비교 및 연결

### AVL 트리 Python 삽입 핵심

```python
def get_height(node):
    if not node: return 0
    return node.height

def get_bf(node):
    if not node: return 0
    return get_height(node.left) - get_height(node.right)

def right_rotate(z):        # LL 회전
    y = z.left
    T3 = y.right
    y.right = z
    z.left = T3
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y

def insert(root, key):
    if not root: return Node(key)
    if key < root.key:    root.left = insert(root.left, key)
    elif key > root.key:  root.right = insert(root.right, key)
    else:                 return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    bf = get_bf(root)

    if bf > 1 and key < root.left.key:   return right_rotate(root)  # LL
    if bf < -1 and key > root.right.key: return left_rotate(root)   # RR
    if bf > 1 and key > root.left.key:   # LR
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if bf < -1 and key < root.right.key: # RL
        root.right = right_rotate(root.right)
        return left_rotate(root)
    return root
```

- **📢 섹션 요약 비유**: AVL 삽입은 자동 균형 저울이다. 물건을 올릴 때마다 저울이 기울면 반대쪽 추를 조정(회전)하여 항상 수평을 유지한다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:---|:---|
| **O(log N) 보장** | BST 퇴화 문제 해결 |
| **예측 가능성** | 최악 성능 1.44 log N으로 제한 |
| **정렬 순서** | 중위 순회로 정렬된 출력 |

현대 데이터베이스 인덱스는 디스크 I/O를 최소화하는 B+Tree를 사용하지만, 인메모리 데이터 구조(Redis Sorted Set, Java TreeMap)는 Red-Black Tree를 활용한다. AVL 트리의 개념이 이 모든 균형 BST의 이론적 기반이다.

- **📢 섹션 요약 비유**: AVL의 이론이 실전에 적용된 것이 Redis Sorted Set이다. 게임 랭킹·실시간 리더보드에서 O(log N) 검색·삽입으로 수백만 사용자 순위를 빠르게 관리한다.

---

## 6. 기대효과 및 결론

AVL 트리의 효과는 접근 패턴에 맞는 저장 구조를 제공해 탐색·삽입·삭제의 비용을 예측 가능하게 만드는 데 있다. 그러나 시간 복잡도 표기만으로는 충분하지 않고, 메모리 지역성, 재구성 비용, 동시성 충돌, 구현 복잡도가 실제 성능을 좌우한다. 결론적으로 자료구조 선택은 알고리즘보다 앞서는 설계 판단이며, 앞으로는 캐시 친화 구조·동시성 안전 구조·확률적 구조와의 결합이 더 중요해진다.

---

## 7. 발전 흐름도

```text
[BST — 이진 탐색, 최악 O(N)]
    │
    ▼
[AVL 트리 — 엄격 균형, 항상 O(log N)]
    │
    ▼
[Red-Black 트리 — 유연 균형, 빠른 삽입/삭제]
    │
    ▼
[B-Tree / B+Tree — 멀티웨이 디스크 I/O 최적화]
    │
    ▼
[Skip List — Redis, 병렬화 친화적 대안]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **BST** | AVL의 기반 자료 구조 |
| **Red-Black Tree** | AVL의 대안 균형 BST |
| **B-Tree / B+Tree** | 디스크 기반 DB 인덱스 |
| **회전 (Rotation)** | AVL/RB 균형 복구 연산 |
| **Balance Factor** | AVL 균형 판단 기준 |
