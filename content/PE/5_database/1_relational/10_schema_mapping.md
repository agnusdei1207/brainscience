+++
title = "10. 스키마 매핑 (Schema Mapping)"
description = "외부/개념/내부 스키마 간의 사상(Mapping) 메커니즘"
date = "2026-03-05"
[taxonomies]
tags = ["schema-mapping", "data-independence", "view-mapping", "physical-mapping"]
categories = ["studynotes-5_database"]
+++

# 10. 스키마 매핑 (Schema Mapping)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스키마 매핑은 3단계 스키마 간의 대응 관계를 정의하는 것으로, 외부/개념 매핑은 논리적 독립성을, 개념/내부 매핑은 물리적 독립성을 보장합니다.
> 2. **가치**: 매핑을 통해 하위 스키마 변경이 상위 스키마에 영향을 주지 않아, 유지보수 비용을 70% 이상 절감하고 시스템 가용성을 99.9%까지 유지합니다.
> 3. **융합**: 현대 ORM, API 게이트웨이, 데이터 가상화 등에서 매핑 개념이 확장 적용되어 계층 간 추상화의 핵심 기술로 자리잡았습니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**스키마 매핑(Schema Mapping)**은 ANSI/SPARC 3단계 아키텍처에서 인접한 스키마 계층 간의 대응 관계를 정의하는 규칙 집합입니다. 이 매핑을 통해 데이터 독립성이 실현됩니다.

**두 가지 매핑 유형**:

1. **외부/개념 매핑 (External/Conceptual Mapping)**
   - 외부 스키마(뷰)와 개념 스키마(전체 논리 구조) 간의 대응
   - 뷰 정의의 SELECT 문이 매핑 규칙 역할
   - 논리적 데이터 독립성 보장

2. **개념/내부 매핑 (Conceptual/Internal Mapping)**
   - 개념 스키마와 내부 스키마(물리 저장) 간의 대응
   - 테이블과 파일, 인덱스 간의 매핑
   - 물리적 데이터 독립성 보장

#### 2. 비유를 통한 이해

**번역기**로 비유:

```
외부/개념 매핑 = 영어-한국어 번역기
- 사용자가 영어로 요청 → 한국어(개념)로 변환
- 한국어 문장이 바뀌어도 영어 요청 방식은 그대로

개념/내부 매핑 = 한국어-기계어 변환기
- 한국어 명령 → 기계가 이해하는 코드
- 기계 구조가 바뀌어도 한국어 명령은 그대로
```

#### 3. 매핑의 필요성

**문제 상황 (매핑 없음)**:
- 스키마 변경 시 모든 응용 프로그램 수정
- 물리적 구조 변경 시 논리적 구조도 변경
- 유지보수 비용 증가, 시스템 불안정

**해결책 (매핑 도입)**:
- 계층 간 인터페이스(매핑)를 통한 격리
- 하위 계층 변경이 상위 계층에 전파되지 않음
- 데이터 독립성 실현

---

### II. 아키텍처 및 핵심 원리

#### 1. 매핑 유형별 구성 (표)

| 매핑 유형 | 역할 | 구현 방식 | 독립성 |
|:---|:---|:---|:---|
| **외부/개념** | 뷰 → 테이블 변환 | CREATE VIEW 문 | 논리적 |
| **개념/내부** | 테이블 → 파일 변환 | 저장 정의, 인덱스 | 물리적 |

#### 2. 스키마 매핑 다이어그램

```text
+================================================================================+
|                        SCHEMA MAPPING ARCHITECTURE                              |
+================================================================================+
|                                                                                 |
|  [EXTERNAL SCHEMA]                                                             |
|  +--------------------------------------------------------------------------+  |
|  | View: sales_customer_view                                                |  |
|  | +----------------------------------------------------------------------+ |  |
|  | | customer_name | order_count | total_amount | grade                   | |  |
|  | +----------------------------------------------------------------------+ |  |
|  +--------------------------------------------------------------------------+  |
|                                      |                                          |
|                                      |                                          |
|                      +---------------+---------------+                          |
|                      |    EXTERNAL/CONCEPTUAL       |                          |
|                      |         MAPPING              |                          |
|                      |                              |                          |
|                      |  View Definition:            |                          |
|                      |  - Column Mapping            |                          |
|                      |  - Row Filtering             |                          |
|                      |  - Join Expansion            |                          |
|                      |  - Expression Transform      |                          |
|                      +---------------+--------------+                          |
|                                      |                                          |
|                                      v                                          |
|  [CONCEPTUAL SCHEMA]                                                           |
|  +--------------------------------------------------------------------------+  |
|  | Tables: CUSTOMER, ORDER, ORDER_ITEM                                      |  |
|  | +----------------+      +----------------+      +----------------+        |  |
|  | | CUSTOMER       |      | ORDER          |      | ORDER_ITEM     |        |  |
|  | +----------------+      +----------------+      +----------------+        |  |
|  | | customer_id(PK)|<-----| order_id(PK)   |<-----| order_id(FK)   |        |  |
|  | | name           |      | customer_id(FK)|      | item_seq(PK)   |        |  |
|  | | email          |      | order_date     |      | product_id(FK) |        |  |
|  | | phone          |      | total_amount   |      | quantity       |        |  |
|  | +----------------+      +----------------+      | unit_price     |        |  |
|  |                                                 +----------------+        |  |
|  +--------------------------------------------------------------------------+  |
|                                      |                                          |
|                      +---------------+---------------+                          |
|                      |    CONCEPTUAL/INTERNAL       |                          |
|                      |         MAPPING              |                          |
|                      |                              |                          |
|                      |  Storage Definition:         |                          |
|                      |  - Table -> File Mapping     |                          |
|                      |  - Index -> B+Tree Mapping   |                          |
|                      |  - Column -> Page Offset     |                          |
|                      |  - Partition -> Tablespace   |                          |
|                      +---------------+--------------+                          |
|                                      |                                          |
|                                      v                                          |
|  [INTERNAL SCHEMA]                                                             |
|  +--------------------------------------------------------------------------+  |
|  | Files & Indexes                                                          |  |
|  | +----------------+      +----------------+      +----------------+        |  |
|  | | customers.ibd  |      | orders.ibd     |      | order_items.ibd|        |  |
|  | +----------------+      +----------------+      +----------------+        |  |
|  | | Clustered B+   |      | Clustered B+   |      | Clustered B+   |        |  |
|  | | idx_name(B+T)  |      | idx_cust(B+T)  |      | idx_order(B+T) |        |  |
|  | +----------------+      +----------------+      +----------------+        |  |
|  +--------------------------------------------------------------------------+  |
|                                                                                 |
+================================================================================+
```

#### 3. 심층 동작 원리: 매핑 변환 과정

**외부/개념 매핑 예시**:

```sql
-- 1. 외부 스키마 (뷰)
CREATE VIEW sales_customer_view AS
SELECT
    c.name AS customer_name,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_amount,
    CASE
        WHEN SUM(o.total_amount) >= 1000000 THEN 'VIP'
        WHEN SUM(o.total_amount) >= 500000 THEN 'GOLD'
        ELSE 'SILVER'
    END AS grade
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- 2. 사용자 쿼리
SELECT customer_name, grade
FROM sales_customer_view
WHERE order_count > 10;

-- 3. 매핑 변환 (View Expansion)
SELECT c.name AS customer_name,
    CASE
        WHEN SUM(o.total_amount) >= 1000000 THEN 'VIP'
        WHEN SUM(o.total_amount) >= 500000 THEN 'GOLD'
        ELSE 'SILVER'
    END AS grade
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 10;

-- 4. 개념/내부 매핑 (실행 계획)
-- IDX_CUSTOMERS_PK (customer_id) 사용
-- IDX_ORDERS_CUSTOMER (customer_id) 사용
-- Hash Aggregate로 GROUP BY
```

#### 4. 핵심 알고리즘: 쿼리 재작성

```python
"""
스키마 매핑을 통한 쿼리 재작성 알고리즘
"""

class SchemaMapper:
    """스키마 계층 간 매핑 엔진"""

    def __init__(self, catalog):
        self.catalog = catalog

    def map_external_to_conceptual(self, query: str) -> str:
        """
        외부 스키마 쿼리를 개념 스키마 쿼리로 변환
        """
        # 1. 쿼리 파싱
        parsed = self._parse(query)

        # 2. 뷰 식별
        views = self._find_views(parsed)

        # 3. 각 뷰 확장
        for view_name in views:
            view_def = self.catalog.get_view(view_name)
            parsed = self._expand_view(parsed, view_name, view_def)

        # 4. 조건 푸시다운
        parsed = self._push_predicates(parsed)

        # 5. 최적화된 SQL 생성
        return self._generate_sql(parsed)

    def _expand_view(self, query: dict, view_name: str, view_def: dict) -> dict:
        """
        뷰를 기본 테이블로 확장
        """
        # 뷰의 FROM 절로 대체
        query['from'] = view_def['from']

        # 컬럼 매핑 적용
        column_mapping = view_def['column_mapping']
        for i, col in enumerate(query['select']):
            if col['name'] in column_mapping:
                query['select'][i] = column_mapping[col['name']]

        # WHERE 조건 병합
        if 'where' in view_def:
            query['where'] = self._merge_conditions(
                query.get('where'),
                view_def['where']
            )

        return query

    def _push_predicates(self, query: dict) -> dict:
        """
        조건 푸시다운 최적화
        - 외부 쿼리의 WHERE 조건을 뷰 내부로 밀어넣음
        """
        if 'where' not in query:
            return query

        # 조건을 서브쿼리 내부로 이동
        # (예: HAVING -> WHERE 변환)
        for condition in query['where']:
            if self._can_push_down(condition, query):
                query = self._do_push_down(condition, query)

        return query

    def map_conceptual_to_internal(self, query: str) -> dict:
        """
        개념 스키마 쿼리를 내부 실행 계획으로 변환
        """
        # 1. 쿼리 최적화
        optimized = self._optimize(query)

        # 2. 물리적 연산자 선택
        plan = self._choose_operators(optimized)

        # 3. 인덱스 선택
        plan = self._choose_indexes(plan)

        # 4. 조인 순서 결정
        plan = self._determine_join_order(plan)

        return plan
```

---

### III. 융합 비교 및 다각도 분석

#### 1. 매핑 유형별 상세 비교

| 비교 항목 | 외부/개념 매핑 | 개념/내부 매핑 |
|:---|:---|:---|
| **변환 방향** | 뷰 → 테이블 | 테이블 → 파일 |
| **주요 기능** | SQL 확장, 조건 병합 | 인덱스 선택, 페이지 접근 |
| **복잡도** | SQL 수준 | 물리적 수준 |
| **성능 영향** | 중간 | 높음 |
| **자동화** | 부분적 | 대부분 자동 |

#### 2. 데이터 독립성 달성 메커니즘

| 독립성 유형 | 달성 방법 | 예시 |
|:---|:---|:---|
| **논리적** | 외부/개념 매핑 | 컬럼 추가 시 뷰 unchanged |
| **물리적** | 개념/내부 매핑 | 인덱스 추가 시 쿼리 unchanged |

---

### IV. 실무 적용 및 기술사적 판단

#### 1. 실무 시나리오

**시나리오 1: 스키마 변경의 투명성**
- **상황**: customers 테이블에 grade 컬럼 추가
- **문제**: 기존 응용프로그램 영향 우려
- **해결**: 외부/개념 매핑(뷰)이 변경 흡수
- **결과**: 응용프로그램 수정 없음

**시나리오 2: 성능 최적화의 투명성**
- **상황**: 인덱스 추가, 파티셔닝 적용
- **해결**: 개념/내부 매핑이 최적화 수행
- **결과**: 쿼리 변경 없이 성능 향상

#### 2. 매핑 설계 가이드

1. **뷰 단순화**: 복잡한 중첩 뷰 지양
2. **성능 고려**: 매핑 비용을 고려한 설계
3. **문서화**: 매핑 규칙의 명확한 문서화

---

### V. 기대효과 및 결론

#### 1. 기대효과

| 구분 | 매핑 없음 | 매핑 있음 |
|:---|:---|:---|
| **스키마 변경 영향** | 전체 전파 | 격리 |
| **유지보수 비용** | 높음 | 70% 절감 |
| **시스템 안정성** | 낮음 | 높음 |

#### 2. 참고 표준

- ANSI/SPARC Three-Level Architecture
- ISO/IEC 9075 SQL Standard

---

### 관련 개념 맵

- **[데이터 독립성](@/studynotes/5_database/1_relational/4_data_independence.md)**: 매핑이 제공하는 핵심 가치
- **[3단계 스키마](@/studynotes/5_database/1_relational/6_three_schema_architecture.md)**: 매핑의 대상 계층
- **[뷰](@/studynotes/5_database/2_sql/view.md)**: 외부/개념 매핑의 구현

---

### 어린이를 위한 3줄 비유

1. **번역가**: 외국어를 하는 친구가 있으면 영어 책을 한국어로 번역해줄 수 있어요. 스키마 매핑은 이런 번역가처럼 서로 다른 언어(스키마)를 연결해줘요!

2. **어댑터**: 핸드폰 충전기를 콘센트에 꽂을 때 어댑터가 필요하죠? 스키마 매핑도 서로 다른 모양의 스키마를 연결해주는 어댑터예요!

3. **중계소**: 라디오 방송국에서 보내는 신호를 중계소가 우리 집 라디오로 보내주죠? 스키마 매핑도 이렇게 중간에서 신호(데이터)를 전달해줘요!
