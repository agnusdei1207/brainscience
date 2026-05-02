+++
weight = 5
title = "합병 정렬 (Merge Sort)"
date = "2025-05-15"
[extra]
categories = "studynote-algorithm"
+++

## 핵심 인사이트 (3줄 요약)
- **분할 정복(Divide & Conquer)** 패러다임을 사용하는 대표적인 **O(n log n)** 보장 안정 정렬 알고리즘이다.
- 데이터의 상태와 무관하게 일관된 성능을 보장하며, 연결 리스트(Linked List) 정렬 시 최적의 효율을 보인다.
- 추가적인 메모리 공간(**O(n)**)이 필요하다는 단점이 있으나, 외부 정렬(External Sort)의 근간이 되는 핵심 기술이다.

### Ⅰ. 개요 (Context & Background)
합병 정렬(Merge Sort)은 존 폰 노이만(John von Neumann)에 의해 제안된 알고리즘으로, 문제를 쪼개어 각각을 해결한 뒤 다시 합쳐 전체를 정렬하는 **분할 정복** 기법을 적용한다. 특히 데이터가 메모리에 모두 올라오지 못하는 대용량 환경에서 보조 기억 장치를 활용하는 **외부 정렬(External Sort)**의 기본 원리로 널리 활용되며, 동일한 키 값의 상대적 순서를 보존하는 **안정 정렬(Stable Sort)**이라는 특징이 있다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
합병 정렬은 (1) 분할(Divide), (2) 정복(Conquer/Sort), (3) 결합(Combine/Merge)의 3단계를 재귀적으로 수행한다.

```text
[Merge Sort Architecture: Divide and Conquer]

1. Divide (분할): Split array into two halves
   [ 38 | 27 | 43 | 3 | 9 | 82 | 10 ]
             /            \
     [ 38 | 27 | 43 ]    [ 3 | 9 | 82 | 10 ]
       /      \            /         \
   [ 38 ]  [ 27 | 43 ]  [ 3 | 9 ]  [ 82 | 10 ]
   
2. Conquer (정복): Sort sub-arrays (Recursively)
   [ 38 ]  [ 27 ] [ 43 ] [ 3 ] [ 9 ] [ 82 ] [ 10 ]

3. Combine/Merge (결합): Merge sorted sub-arrays back
      \      /            \      /
     [ 27 | 38 | 43 ]    [ 3 | 9 | 10 | 82 ]
             \            /
   [ 3 | 9 | 10 | 27 | 38 | 43 | 82 ] (Sorted)

[Merge Operation Principle]
- Two pointers (i, j) compare elements from two sorted blocks.
- Smaller element is moved to temporary array.
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Criteria) | 합병 정렬 (Merge Sort) | 퀵 정렬 (Quick Sort) | 힙 정렬 (Heap Sort) |
| :--- | :--- | :--- | :--- |
| **시간 복잡도 (최악)** | **O(n log n)** | O(n²) | O(n log n) |
| **공간 복잡도** | **O(n)** (추가 공간 필요) | O(log n) | O(1) (In-place) |
| **안정성 (Stability)** | **안정 (Stable)** | 불안정 (Unstable) | 불안정 (Unstable) |
| **특이 사항** | 데이터 순차 접근 유리 | 캐시 지역성 우수 | 데이터 무작위 접근 |
| **활용 분야** | 연결 리스트, 외부 정렬 | 일반적인 내부 정렬 | 우선순위 큐 기반 정렬 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **(연결 리스트 최적화)** 순차적 접근 방식이므로 포인터 변경만으로 정렬이 가능하여, 무작위 접근이 느린 **Linked List** 환경에서 퀵 정렬보다 우월한 성능을 보인다.
- **(외부 정렬 전략)** 메모리보다 큰 파일을 정렬할 때, 파일을 블록 단위로 읽어 각각 합병 정렬한 뒤 최종적으로 **Multi-way Merge**를 통해 하나의 정렬된 파일로 병합하는 방식을 사용한다.
- **(판단)** 실시간 반응 속도가 중요한 시스템에서는 O(n)의 추가 메모리 할당 부하가 병목이 될 수 있으므로, 메모리 제약이 엄격한 임베디드 환경에서는 힙 정렬이나 인트로 정렬(Introsort)을 고려해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
합병 정렬은 복잡도 하한선인 O(n log n)을 모든 케이스에서 보장한다는 점에서 **신뢰성**이 매우 높다. 현대의 **Timsort**(Python, Java 기본 정렬)는 합병 정렬과 삽입 정렬을 최적으로 결합한 형태로 진화하였으며, 이는 대규모 데이터 처리 인프라의 표준 알고리즘으로 자리매김하고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: 분할 정복(Divide and Conquer), 안정 정렬(Stable Sort)
- **자식/확장 개념**: Timsort, 2-way Merge, Multi-way External Merge, 폰 노이만 아키텍처
- **유사 개념**: 퀵 정렬(Quick Sort), 힙 정렬(Heap Sort)

### 📈 관련 키워드 및 발전 흐름도

```text
[분할 정복 (Divide and Conquer)]
    │
    ▼
[안정 정렬 (Stable Sort)]
    │
    ▼
[Timsort]
    │
    ▼
[폰 노이만 아키텍처]
    │
    ▼
[퀵 정렬 (Quick Sort)]
```

이 흐름도는 분할 정복 (Divide and Conquer)에서 출발해 퀵 정렬 (Quick Sort)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 뒤죽박죽 섞인 장난감 카드를 반으로 계속 나누어서 카드가 딱 1장이 될 때까지 쪼개요.
2. 이제 두 명의 친구가 가진 작은 카드 더미를 보면서, 번호가 작은 순서대로 예쁘게 합쳐요.
3. 이 과정을 반복하면 커다란 카드 더미 전체가 번호 순서대로 딱 맞춰져요!
