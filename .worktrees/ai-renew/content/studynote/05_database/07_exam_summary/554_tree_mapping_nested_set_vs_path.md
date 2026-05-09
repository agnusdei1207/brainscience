+++
title = "계층형 데이터 모델링 (Nested Set vs. Nested Path)"
weight = 554
date = "2026-03-04"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
- **계층 구조의 RDB 매핑:** 트리 구조 데이터를 관계형 데이터베이스(RDB)에 효율적으로 저장하고 조회하기 위해 Adjacency List, Nested Set, Nested Path 등 다양한 기법 활용.
- **Nested Set (중첩 집합):** 노드의 좌우(Left/Right) 범위를 지정하여 서브트리 전체 조회를 고속화하나, 데이터 변경(CUD) 시 전체 노드 갱신 오버헤드 발생.
- **Nested Path (Materialized Path):** 노드의 경로 정보(예: '1/2/3')를 문자열로 저장하여 조회가 직관적이며, 정규 표현식 또는 문자열 검색을 통해 계층 탐색 성능 확보.

### Ⅰ. 개요 (Context & Background)
조직도, 카테고리, 댓글의 답글 구조 등 현실의 데이터는 많은 경우 **계층형(Hierarchical)** 구조를 가집니다. 이를 2차원 표 형태인 RDB에 저장할 때, 전통적인 '부모 참조(Adjacency List)' 방식은 무한 재귀 조인(Recursive Join)으로 인한 성능 저하 문제가 발생하므로, 대용량 처리와 조회 속도 최적화를 위해 Nested Set이나 Nested Path 같은 비정규화된 설계 기법이 실무에서 널리 사용됩니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
두 모델은 계층 구조를 선형적인 속성으로 변환하여 조회 효율을 극대화합니다.

```text
[Hierarchical Tree Example]          [Nested Set Mapping (L/R)]
        (A)                          +--------+---+---+
       /   \                         | Node   | L | R |
     (B)   (C)                       +--------+---+---+
    /   \                            | (A)    | 1 | 6 |
  (D)   (E)                          | (B)    | 2 | 5 |
                                     | (C)    | 6 | 7 | (Example logic)
                                     +--------+---+---+
[Nested Path (Materialized Path)]
+--------+-----------+               [Comparison Visualization]
| Node   | Path      |               Nested Set:  [1 [2 [3 4] 5] 6]
+--------+-----------+               Nested Path: /Root/Parent/Child
| (D)    | /A/B/D    |
+--------+-----------+
```

1. **Nested Set 모델:** 노드를 삽입할 때 트리를 순회하며 번호를 부여. 특정 노드 `X`의 하위 노드들은 `X.Left < Child.Left < X.Right` 조건을 만족하는 모든 노드가 되어 한 번의 `BETWEEN` 쿼리로 전체 서브트리 추출이 가능.
2. **Nested Path (Materialized Path):** 각 노드에 루트부터 자신까지의 경로를 컬럼에 저장. `LIKE '/A/B/%'`와 같은 인덱스 레인지 스캔을 통해 하위 구조를 탐색.
3. **트레이드오프:** Nested Set은 조회에 최강이지만 삽입/삭제 시 번호를 재계산(Update)해야 하므로 '정적인 트리'에 적합하고, Nested Path는 경로의 길이 제한이 있으나 변경이 상대적으로 유연함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 (Comparison) | Adjacency List (기본) | Nested Set (중첩 집합) | Nested Path (경로 저장) |
|---|---|---|---|
| **저장 방식** | 부모 ID 참조 (FK) | L, R 범위 값 저장 | 전체 경로 문자열 저장 |
| **하위 조회** | 재귀 호출 (Recursive) | `BETWEEN` 연산 (최상) | `LIKE` 연산 (중상) |
| **데이터 변경** | 매우 빠름 (단일 행) | 매우 느림 (전체 재조정) | 보통 (하위 경로 갱신) |
| **복잡도** | 단순 (정규화) | 매우 복잡 | 보통 (비정규화) |
| **추천 용어** | 댓글, 단순 조직도 | 고정된 상품 카테고리 | 파일 시스템 경로, 대댓글 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
데이터베이스 설계자는 트리의 규모와 읽기/쓰기 비율을 고려하여 기법을 선택해야 합니다.
- **현대적 접근:** 최근 RDBMS(Oracle, PostgreSQL 등)는 `WITH RECURSIVE` 또는 `CONNECT BY`를 통해 Adjacency List의 조회 성능을 엔진 레벨에서 최적화하므로, 극단적인 조회 성능이 필요한 경우가 아니라면 유지보수가 쉬운 기본 방식을 우선 고려합니다.
- **기술사적 판단:** 분산 DB 환경이나 대규모 카테고리 시스템에서는 Nested Path 방식에 GIN 인덱스나 전문 검색 인덱스를 조합하여 조회 유연성을 확보하는 것이 MSA 환경의 데이터 분산 관점에서 더욱 유리할 것으로 판단됩니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
계층형 모델링은 데이터 구조의 복잡성을 성능으로 치환하는 과정입니다. Nested Set과 Nested Path는 단순히 '저장'을 넘어 '어떻게 효과적으로 읽을 것인가'에 대한 RDB의 한계를 극복하는 전략입니다. 향후 NoSQL(Graph DB)과의 연동을 통해 복잡한 관계망은 그래프 엔진에 맡기고, 정형화된 계층은 RDB의 이러한 특화 모델로 관리하는 하이브리드 전략이 표준화될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **트리 구조:** Adjacency List, Adjacency Matrix, Nested Set, Materialized Path
- **SQL 기능:** CTE (Common Table Expression), RECURSIVE, CONNECT BY
- **성능 요소:** 인덱스 레인지 스캔, 전파 갱신(Cascading Update)

### 👶 어린이를 위한 3줄 비유 설명
1. **Adjacency List**는 친구에게 "우리 아빠는 누구야"라고 물어물어 할아버지까지 찾아가는 보물찾기예요.
2. **Nested Set**은 도서관 책꽂이 번호처럼 1번부터 100번까지 번호를 미리 매겨서 한눈에 찾는 방법이고요.
3. **Nested Path**는 "우리 집 주소는 대한민국 서울시 강남구..."처럼 전체 주소를 이름표에 미리 써두는 방법이랍니다!
