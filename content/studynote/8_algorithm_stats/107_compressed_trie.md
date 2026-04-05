+++
title = "107. 압축된 트라이 (Compressed Trie / Patricia Trie)"
weight = 107
+++

# 107. 압축된 트라이 (Compressed Trie / Patricia Trie)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 압축된 트라이(Compressed Trie 또는 Patricia Trie)는 일반 트라이에서 단일 자식만 가진 노드들을 병합하여 노드 수를 줄이고 검색을 효율화한 자료구조이다.
> 2. **가치**: 문자열 검색, 자동 완성, IP 라우팅 테이블, 사전 검색 등에서 메모리를 절약하면서도 O(m) 시간 복잡도를 유지한다.
> 3. **융합**: 네트워크 장비(라우터), 모바일 키보드,search 엔진 인덱싱 등에서 광범위하게 활용되는 실용적인 자료구조이다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

압축된 트라이(Compressed Trie)는 **패트리시아 트리(Patricia Tree)**라고도 불리며, "Practical Algorithm To Retrieve Information Coded In Alphanumeric"의 약자이다. 일반 트라이(Trie)에서 모든 노드가 한 개의 자식만 가진 경우, 해당 경로상의 노드들을 하나의 노드로 병합하여 트리의 크기를 줄인다.

압축된 트라이가 중요한 이유는 **메모리 효율성** 때문이다. 일반 트라이에서 문자열 "algorithm"을 저장하려면 각 문자마다 노드를 생성하므로 9개의 노드가 필요하다. 하지만 압축된 트라이에서는 전체 문자열을 한 번에 저장하거나, 비슷한 접두사를 가진 문자열들을 효율적으로 표현할 수 있다.

트라이(Trie) 자체가 문자열 탐색에 특화된 자료구조이지만, 단일 자식만 가진 노드들이 많아지면 메모리 낭비가 심해진다. 압축된 트라이(Compressed Trie 또는 Radix Tree라고도 함)는 이러한 문제점을 해결하기 위해 도입되었다.

**기본 개념**으로 압축된 트라이에서는 각 노드가 **키(label)**와 **값(value)**을 저장한다. 키는 일반적으로 문자열 또는 문자열의 일부이고, 값은 해당 키에 대응하는 데이터이다. 노드는 2개 이상의 자식을 가질 수 있으며, 각 자식은 서로 다른 첫 문자를 가져야 한다.

```text
[일반 트라이 vs 압축된 트라이]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  [일반 트라이: "apple", "app", "apt"] 저장]                  │
│  ────────────────────────────────────────────                │
│                                                              │
│                ○ (root)                                      │
│               /                                              │
│              a                                               │
│             /                                                │
│            p                                               │
│           /                                                  │
│          p                                               │
│         / \                                                 │
│        l   t   (l: "le", t: null)                          │
│       /                                                   │
│      e                                                   │
│     /                                                     │
│    null (apple)                                           │
│                                                              │
│  노드 수: 약 12개                                             │
│                                                              │
│  [압축된 트라이: 같은 문자열 저장]                             │
│  ────────────────────────────────────────────                │
│                                                              │
│                ○ (root)                                      │
│               /                                              │
│              "app"                                           │
│             / \                                              │
│          "le"  "t"                                          │
│         /      \                                             │
│       null   null                                           │
│     (apple) (apt)                                           │
│                                                              │
│  노드 수: 5개 (60% 감소)                                      │
│                                                              │
│  [압축 트라이 노드 구조]                                      │
│  ────────────────────────────────────────────                │
│  각 노드는:                                                   │
│  • key: 노드에 저장된 문자열 (또는 문자열의 일부)             │
│  • value: 해당 키의 값 (leaf 노드에서만 유효)                │
│  • children: 자식 노드들 (정렬된 배열 또는 딕셔너리)         │
│                                                              │
│  예: "apple" 저장 시                                        │
│  • root → ["app"] → ["le"] → null                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- **관찰**: 압축된 트라이는 일반 트라이보다 노드 수가 현저히 적다.
- **원인**: 단일 자식만 가진 노드들을 병합하기 때문이다.
- **결과**: 메모리 사용량이 줄면서도 검색 시간 복잡도는 동일하게 O(m)이다.
- **판단**: 문자열 검색에서 메모리가 중요한 경우 압축된 트라이가 선호된다.

📢 **섹션 요약 비유**: 압축된 트라이는 **도서관의 주제별 책 분류 시스템**과 같습니다. "컴퓨터", "컴퓨터 프로그래밍", "컴퓨터 네트워크"를 각각 다른 칸에 모두 저장하지 않고, "컴퓨터" 아래에 "프로그래밍"과 "네트워크"라는 하위 분류만 두는 것과 같습니다. 공간을 절약하면서도 원하는 책을 찾을 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

압축된 트라이의 핵심은 **노드 병합 규칙**과 **탐색 알고리즘**이다. 일반 트라이와의 차이를 정확히 이해하면, 구현과 활용에서 오는 장점을 파악할 수 있다.

**노드 병합 규칙**에서 일반 트라이에서 어떤 노드의 자식이 하나뿐이고, 그 자식도 자식이 하나뿐이라면, 이 경로상의 모든 노드를 하나로 병합한다. 병합된 노드의 키는 원래 키들을 연결한 문자열이 된다. 예를 들어, root → "a" → "p" → "p" → "l" → "e" 경로에서 각 노드가 자식을 하나씩 가지므로, 이를 ["apple"] 하나로 표현할 수 있다.

**탐색 알고리즘(Search)**은 다음과 같이 동작한다: root에서 시작하여 모든 자식 노드의 키와 입력 문자열을 비교한다. 일치하는 자식이 있으면 해당 자식으로 이동하고, 남은 문자열과 자식의 키를 계속 비교한다. 일치하는 자식이 없으면 실패이다. 전체 문자열을 처리하고 leaf에 도달하면 성공이다. 시간 복잡도는 O(m)이며, 여기서 m은 입력 문자열의 길이이다.

**삽입 알고리즘(Insert)**은 먼저 탐색을 수행한다. 탐색 중 가장 긴 일치 prefixes을 찾는다. 일치하지 않는 부분에서 새 노드를 생성하거나 기존 노드를 분할한다. 예를 들어, ["app", "apple"]가 있을 때 "apricot"을 삽입하면, "ap"에서 분할되어 "p"와 "ricot" 새 노드가 생성된다.

```text
[압축된 트라이 탐색 동작]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  [예시: "algorithm" 검색]                                    │
│  ────────────────────────────────────────────                │
│                                                              │
│  트라이에 저장된 문자열: ["algo", "algorithm", "all", "also"]│
│                                                              │
│  Step 1: root에서 시작                                        │
│          입력: "algorithm"                                   │
│          자식: ["algo", "all"]                               │
│          → "algo"와 비교, 일치                              │
│                                                              │
│  Step 2: "algo" 노드로 이동                                   │
│          입력: "algorithm" (남은 문자: "rithm")               │
│          자식: ["rithm"]                                     │
│          → "rithm"과 비교, 일치                              │
│                                                              │
│  Step 3: leaf 도달                                           │
│          → 검색 성공                                          │
│                                                              │
│  [삽입 예시: "app"를 ["apple", "apt"]에 삽입]                 │
│  ────────────────────────────────────────────                │
│                                                              │
│  기존: root → "ap" → ["ple", "t"]                           │
│                                                              │
│  Step 1: "app" 탐색 시 "ap"에서 일치                         │
│          → "ap"은 이미 존재, 새 문자 없음                     │
│          → 기존 노드의 값을 업데이트하거나 중복 확인           │
│                                                              │
│  [삽입 예시: "api"를 ["app", "apple"]에 삽입]                 │
│  ────────────────────────────────────────────                │
│                                                              │
│  기존: root → "app" → ["le", null("app")]                   │
│                                                              │
│  Step 1: "api" 탐색 시 "ap"까지 일치                        │
│          → 다음 문자 "p" vs "i" 불일치                       │
│          → "ap" 노드 분할: "ap" → ["p", "i"]                │
│          → 분할 후: root → "ap" → ["p" → ["le", null],     │
│                                            ["i"] → null]    │
│                                                              │
│  [압축된 트라이 vs 일반 트라이 비교]                          │
│  ────────────────────────────────────────────                │
│                                                              │
│  문자열 수: 10,000개                                         │
│  평균 길이: 20자                                             │
│  총 문자 수: 200,000자                                       │
│                                                              │
│  일반 트라이: 200,000 + α 노드 (오버헤드 포함)               │
│  압축 트라이: ~10,000 * 2 = 20,000 노드 (평균)              │
│  → 약 90% 노드 감소                                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- **관찰**: 압축된 트라이는 노드 수를 크게 줄이면서 검색 시간은 동일하다.
- **원인**: 병합은 노드 수만 줄이고, 키 비교 횟수는 변하지 않기 때문이다.
- **결과**: 메모리 효율성만 향상되고 시간 효율성은 유지된다.
- **판단**: 대용량 문자열数据集에서 압축된 트라이가 필수적이다.

---

## Ⅲ. 구현 및 활용 (Implementation & Applications)

압축된 트라이의 구현은 일반 트라이보다 복잡하지만, 적절한 자료구조 선택과 알고리즘으로 효율적으로 구현할 수 있다.

**기본 구현**에서 각 노드는 key(문자열), value(데이터), children(자식 노드 맵)을 가진다._children는 일반적으로 해시 맵이나 정렬된 배열로 구현하여 빠른 접근을 가능하게 한다. Java에서는 HashMap<Character, Node> 또는 TreeMap<Character, Node>를 사용하고, C++에서는 std::map<char, Node> 또는 std::unordered_map<char, Node>를 사용한다.

**활용 사례**로 **IP 라우팅 테이블**에서 라우터는 압축된 트라이(또는 Radix Tree)를 사용하여 IP 주소 검색을 O(m) 시간에 수행한다. 각 라우팅 항목은 IP 주소의 접두사를 나타내며, 가장 긴 일치 접두사(Longest Prefix Match)를 찾아야 한다. **자동 완성/입력 예측**에서 모바일 키보드나search 바에서 사용자가 입력하는 문자열에 따라候補를 제안하는 데 사용된다. **신속한 문자열 색인**에서search 엔진이나 데이터베이스에서 텍스트 색인 구축에 활용된다. **오토마타**에서 압축된 트라이는Trie의 변형으로, 문자열 매칭 알고리즘의 기반이 된다.

```text
[압축된 트라이 구현 코드]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  class CompressedTrieNode:                                   │
│      def __init__(self, key=""):                            │
│          self.key = key           # 이 노드의 문자열          │
│          self.value = None       # 값 (leaf에서만 유효)      │
│          self.children = {}      # 자식 노드들 (key -> node)│
│                                                              │
│  class CompressedTrie:                                       │
│      def __init__(self):                                   │
│          self.root = CompressedTrieNode()                   │
│                                                              │
│      def insert(self, word, value=None):                    │
│          node = self.root                                   │
│          i = 0                                               │
│          while i < len(word):                               │
│              # 현재 노드의 키와 매칭되는 부분 찾기             │
│              match_len = self._match_length(node, word, i) │
│                                                              │
│              if match_len == len(node.key):                  │
│                  # 노드의 키와 완전히 일치                      │
│                  i += match_len                              │
│                  if i == len(word):                          │
│                      node.value = value                     │
│                      return                                  │
│                  # 다음 자식 탐색                              │
│                  if word[i] in node.children:               │
│                      node = node.children[word[i]]          │
│                  else:                                       │
│                      # 새 자식 생성                          │
│                      new_node = CompressedTrieNode(word[i:])│
│                      node.children[word[i]] = new_node      │
│                      new_node.value = value                 │
│                      return                                  │
│              else:                                           │
│                  # 일부만 일치 - 노드 분할                     │
│                  self._split_node(node, word, i, match_len, value)│
│                  return                                      │
│                                                              │
│      def _match_length(self, node, word, index):            │
│          key = node.key                                      │
│          i = 0                                               │
│          while i < len(key) and index + i < len(word):      │
│              if key[i] != word[index + i]:                  │
│                  break                                       │
│              i += 1                                          │
│          return i                                            │
│                                                              │
│      def _split_node(self, node, word, index, match_len, value):│
│          # 노드를 분할하여 새 노드 생성                         │
│          old_key = node.key                                  │
│          new_key1 = old_key[:match_len]                     │
│          new_key2 = old_key[match_len:]                      │
│          remaining_word = word[index + match_len:]          │
│                                                              │
│          # 새 중간 노드 생성                                  │
│          mid_node = CompressedTrieNode(new_key1)            │
│          node.key = new_key2                                │
│                                                              │
│          # 기존 자식을 새 중간 노드의 자식으로 이동             │
│          mid_node.children[old_key[match_len]] = node      │
│                                                              │
│          # 남은 문자열을 새 리프 노드로 추가                   │
│          if remaining_word:                                  │
│              leaf_node = CompressedTrieNode(remaining_word) │
│              leaf_node.value = value                         │
│              mid_node.children[remaining_word[0]] = leaf_node│
│          else:                                               │
│              node.value = value                              │
│                                                              │
│      def search(self, word):                                │
│          node, i = self._find_node(word)                    │
│          if node and i == len(word) and node.key == word[len(word)-len(node.key):]│
│              return node.value                               │
│          return None                                        │
│                                                              │
│      def _find_node(self, word):                             │
│          node = self.root                                   │
│          i = 0                                               │
│          while i < len(word) and node.children:             │
│              match_len = self._match_length(node, word, i)  │
│              if match_len < len(node.key):                  │
│                  return None, i                              │
│              i += match_len                                 │
│              if i == len(word):                             │
│                  return node, i                              │
│              if word[i] in node.children:                   │
│                  node = node.children[word[i]]             │
│          return node, i                                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- **관찰**: 노드 분할 로직이 가장 복잡한 부분이다.
- **원인**: 기존 키와 새 문자열 사이의 공통 접두사를 올바르게 처리해야 하기 때문이다.
- **결과**: 올바른 구현이 되면 일반 트라이보다 메모리 효율적이다.
- **판단**: 구현 시 분할 로직의 정확성을 충분히 테스트해야 한다.

---

## Ⅳ. 라디ックス 트리와의 관계 (Relationship with Radix Tree)

압축된 트라이와 라디ックス 트리(Radix Tree)는 흔히 혼용되지만,厳密には 약간의 차이가 있다. 그러나 실용적으로는 동일한 자료구조로 취급된다.

**용어 정리**에서 **Compressed Trie**는 단일 자식 노드들을 병합한 Trie를 가리키는 일반적인 용어이다. **Patricia Trie**는 Practical Algorithm To Retrieve Information Coded In Alphanumeric의 약자로, 가장 처음 소개된 압축 Trie이다. **Radix Tree**는 IP 라우팅에서 주로 사용되는 용어로, Compressed Trie와 동의어이다.

**공통점**으로 both 노드의 키를 문자열(또는 바이트열)로 저장하고, 단일 자식 노드들을 병합하며, O(m) 시간 복잡도를 가진다. 그리고 긴 문자열数据集에서 메모리를 절약한다.

**차이점**은 주로 용어의 차이이며, 기술적 차이는 거의 없다. 일부 구현에서 Radix Tree는 바이트 수준 대신 비트 수준으로 분할하는 경우도 있다.

```text
[압축된 트라이 vs 라디ックス 트리 vs Patricia]

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  [용어 비교]                                                  │
│  ────────────────────────────────────────────                │
│                                                              │
│  압축된 트라이 (Compressed Trie)                            │
│  • 가장 일반적인 용어                                       │
│  • Trie의 압축 버전                                         │
│                                                              │
│  Patricia Trie                                             │
│  • 1968년 Morrison이 제안                                   │
│  • "Compressed Trie"의 한 종류                              │
│                                                              │
│  Radix Tree                                                │
│  • IP 라우팅에서 주로 사용                                   │
│  • Patricia Trie와 사실상 동일                              │
│                                                              │
│  [핵심 특성 비교]                                            │
│  ────────────────────────────────────────────                │
│  • 노드 병합: 단일 자식만 가진 노드들을 병합                  │
│  • 시간 복잡도: O(m), m = 문자열 길이                       │
│  • 공간 복잡도: O(총 문자 수 + 노드 수)                      │
│  • 활용: 문자열 검색, IP 라우팅, 자동 완성                  │
│                                                              │
│  [IP 라우팅에서의 활용]                                       │
│  ────────────────────────────────────────────                │
│  IP: 192.168.1.0/24                                          │
│  • 24비트 접두사                                             │
│  • 가장 긴 일치 접두사 (Longest Prefix Match) 검색           │
│  • 압축된 트라이로 O(W) 시간, W = IP 비트 수 (32 또는 128)  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

- **관찰**: 세 용어 모두 비슷한 개념을 가리킨다.
- **원인**: 다른 연구자들과 분야들이 같은 개념에 다른 이름을 붙였기 때문이다.
- **결과**: 실용적으로는 동일한 자료구조로 취급하면 된다.
- **판단**: 특정 분야(예: 네트워킹)에서 특정 용어(예: Radix Tree)를 주로 사용한다.

---

## Ⅴ. 요약 및 점검 (Summary & Checklist)

압축된 트라이(Compressed Trie / Patricia Trie)는 일반 트라이에서 단일 자식만 가진 노드들을 병합하여 메모리를 절약한 문자열 탐색 트리이다. O(m) 시간 복잡도로 문자열 검색이 가능하며, IP 라우팅, 자동 완성,search 인덱싱 등에 널리 활용된다.

**핵심 점검 사항**으로 먼저, **핵심 개념**에서 단일 자식 노드 병합으로 메모리를 절약한다. 둘째, **시간 복잡도**는 O(m)이며 일반 트라이와 동일하다. 셋째, **공간 절약**은 노드 수를 크게 줄여 메모리 사용량을 감소시킨다. 넷째, **탐색/삽입** 알고리즘에서 노드 분할 로직이 핵심이다. 다섯째, **활용 분야**로 IP 라우팅, 자동 완성, 문자열 인덱싱 등이 있다. 여섯째, **용어**로 Compressed Trie, Patricia Trie, Radix Tree가 유사한 개념이다.

> **핵심 용어 정리**
> - **압축된 트라이 (Compressed Trie)**: 단일 자식 노드를 병합한 Trie
> - **Patricia Trie**: Practical Algorithm To Retrieve Information Coded In Alphanumeric
> - **라디ックス 트리 (Radix Tree)**: IP 라우팅에서 사용하는 압축된 트라이
> - **Longest Prefix Match**: 가장 긴 일치 접두사 검색
> - **노드 분할 (Node Splitting)**: 삽입 시 기존 노드를 나누는 작업

---

## 检查清单 (Checkpoint)

- [ ] 일반 트라이와 압축된 트라이의 차이점을 설명할 수 있는가?
- [ ] 압축된 트라이에서 문자열 검색이 O(m)인 이유를 설명할 수 있는가?
- [ ] 노드 분할(split)이 필요한 상황을 설명할 수 있는가?
- [ ] 압축된 트라이가 활용되는 주요 분야를 열거할 수 있는가?
- [ ] Patricia Trie와 Radix Tree가 무엇인지 알고 있는가?
- [ ] 압축된 트라이의 장점과 단점을 설명할 수 있는가?
