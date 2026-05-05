+++
weight = 87
title = "30. 트라이 (Trie) — 문자열 검색의 효율적 자료 구조"
date = "2026-04-29"
[extra]
categories = "studynote-algorithm-stats"
+++

## 0. 핵심 인사이트

> **핵심**: 트라이(Trie, Prefix Tree)는 문자열 집합을 저장하고 검색하는 트리 자료 구조다. 루트에서 리프까지의 경로가 하나의 문자열을 나타내며, 공통 접두사(Prefix)를 공유하는 문자열들이 같은 노드를 공유한다.
> **비유**: 트라이 (Trie)은(는) 물건을 자주 꺼내는 방식에 맞춰 서랍과 선반의 구조를 설계하는 것과 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
트라이 구조 ("CAT", "CAR", "CAN", "DOG" 삽입):

      루트
      /       C    D
     |    |
     A    O
   / | \  |
  T  R  N  G
(CAT)(CAR)(CAN)(DOG)

공통 접두사 "CA"를 두 노드가 공유!
검색 "CAR": C→A→R 이동, O(3) = O(L)
```

- **📢 섹션 요약 비유**: 트라이는 도서관 분류 시스템이다. "컴퓨터과학" 서가 안에 "컴퓨터과학-알고리즘", "컴퓨터과학-네트워크"가 함께 있어서 "컴퓨터과학"이라는 공통 접두사를 공유한다.

---

## 2. 구성요소

### 트라이 노드 구조

```python
class TrieNode:
    def __init__(self):
        self.children = {}     # 자식 노드 딕셔너리
        self.is_end = False    # 단어 끝 여부

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):       # O(L)
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):       # O(L)
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix): # O(L) - 자동완성!
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True  # 접두사 존재 확인
```

- **📢 섹션 요약 비유**: 트라이 삽입은 주소록에 연락처 추가와 같다. 성(C)→이름 첫 글자(A)→두 번째 글자(T) 순으로 트리를 따라 이동하며 새 분기가 필요한 곳에서만 새 노드를 만든다.

---

## 3. 구조 및 원리

**핵심 조건**: 트라이 (Trie)의 성능은 메모리 배치, 접근 패턴, 불변식 유지 비용에 의해 결정된다. 탐색·삽입·삭제가 어떤 경로로 일어나는지와 재구성 비용을 함께 봐야 한다.

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
조회/수정 결과 반환 (트라이 (Trie))
```

| 비교 | 트라이 | 해시맵 | BST |
|:---|:---|:---|:---|
| 검색 시간 | O(L) | O(L) 평균 | O(L log N) |
| 접두사 검색 | ✅ O(L) | ❌ O(N) | ❌ O(N) |
| 메모리 | 많음 (포인터) | 적음 | 중간 |
| 자동 완성 | ✅ 최적 | ❌ | ❌ |

- **📢 섹션 요약 비유**: 트라이·해시맵·BST는 책 찾는 방법이다. 제목 전체 암기(해시맵), 알파벳 순 사전(BST), 접두사로 관련 책 모아보기(트라이). 접두사 검색에는 트라이가 압도적이다.

---

## 4. 비교 및 연결

### 자동 완성 구현

```python
def autocomplete(trie, prefix, max_results=5):
    """접두사로 시작하는 단어 모두 반환"""
    results = []

    # 접두사까지 이동
    node = trie.root
    for ch in prefix:
        if ch not in node.children:
            return []
        node = node.children[ch]

    # DFS로 모든 완성 단어 수집
    def dfs(node, current):
        if len(results) >= max_results:
            return
        if node.is_end:
            results.append(current)
        for ch, child in node.children.items():
            dfs(child, current + ch)

    dfs(node, prefix)
    return results
```

### 압축 트라이 (Radix Tree)

```text
일반 트라이:
  C → A → T (3 노드)

압축 트라이:
  CAT (1 노드에 "CAT" 저장)
  CAR → R (공통 접두사 "CA" 이후 분기)

  "CA" ─── "T" (CAT)
            └── "R" (CAR)
            └── "N" (CAN)
```

- **📢 섹션 요약 비유**: 압축 트라이는 주소 약어 시스템이다. "서울특별시 강남구"를 매번 쓰는 대신 공통 부분을 하나로 압축하여 "서울강남-역삼", "서울강남-삼성"으로 저장하는 것과 같다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:---|:---|
| **자동 완성** | 접두사 기반 O(L) 검색 |
| **사전 구현** | 효율적 단어 저장·검색 |
| **IP 라우팅** | CIDR 접두사 매칭 (Longest Prefix Match) |

LLM(대형 언어 모델)에서 트라이는 토큰화(Tokenization) 단계에서 활용된다. BPE(Byte Pair Encoding)·WordPiece 같은 서브워드 토큰화에서 어휘 사전 탐색에 트라이 기반 빠른 매칭이 사용된다. 수백만 토큰의 어휘에서 O(L) 검색이 LLM 추론 속도를 지킨다.

- **📢 섹션 요약 비유**: LLM 토큰화의 트라이는 사전 빠른 검색이다. 문장 "Hello World"를 단어로 분리할 때, 수백만 단어 사전에서 "Hell", "Hello", "HelloW"... 를 빠르게 매칭하는 것이 트라이의 역할이다.

---

## 6. 기대효과 및 결론

트라이 (Trie)의 효과는 접근 패턴에 맞는 저장 구조를 제공해 탐색·삽입·삭제의 비용을 예측 가능하게 만드는 데 있다. 그러나 시간 복잡도 표기만으로는 충분하지 않고, 메모리 지역성, 재구성 비용, 동시성 충돌, 구현 복잡도가 실제 성능을 좌우한다. 결론적으로 자료구조 선택은 알고리즘보다 앞서는 설계 판단이며, 앞으로는 캐시 친화 구조·동시성 안전 구조·확률적 구조와의 결합이 더 중요해진다.

---

## 7. 발전 흐름도

```text
[해시맵·BST — 일반 문자열 저장·검색]
    │
    ▼
[트라이 (Trie) — 접두사 공유 O(L) 검색]
    │
    ▼
[압축 트라이 (Radix Tree) — 메모리 최적화]
    │
    ▼
[Aho-Corasick — 다중 패턴 매칭 (실패 링크 추가)]
    │
    ▼
[LLM 토큰화 — BPE 어휘 사전 트라이 매칭]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **압축 트라이** | 메모리 효율화 (Radix Tree) |
| **자동 완성** | 트라이의 핵심 응용 |
| **Longest Prefix Match** | IP 라우팅 트라이 활용 |
| **BPE 토큰화** | LLM 어휘 트라이 매칭 |
| **Aho-Corasick** | 다중 패턴 매칭 트라이 확장 |
