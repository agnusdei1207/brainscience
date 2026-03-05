+++
title = "6. 3단계 스키마 아키텍처 (ANSI/SPARC)"
description = "외부, 개념, 내부 스키마의 구조와 매핑 메커니즘"
date = "2026-03-05"
[taxonomies]
tags = ["three-schema", "ansi-sparc", "data-independence", "database-architecture"]
categories = ["studynotes-5_database"]
+++

# 6. 3단계 스키마 아키텍처 (ANSI/SPARC)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ANSI/SPARC 3단계 스키마 아키텍처는 데이터베이스를 외부(사용자 관점), 개념(전체 논리 구조), 내부(물리 저장)의 3계층으로 분리하고, 계층 간 매핑을 통해 데이터 독립성을 실현하는 표준 프레임워크입니다.
> 2. **가치**: 이 아키텍처를 통해 물리적 저장 구조 변경 시 응용 프로그램 수정 없이 100% 호환성을 보장하며, 유지보수 비용을 70% 이상 절감합니다.
> 3. **융합**: 현대 MVC 패턴, 마이크로서비스, API 게이트웨이 등에서 3단계 추상화 개념이 확장 적용되어 시스템 아키텍처의 기본 원칙으로 자리잡았습니다.

---

### Ⅰ. 개요 (Context & Background) - [최소 500자 이상]

#### 1. 개념 및 기술적 정의

**3단계 스키마 아키텍처**는 1975년 미국 국립 표준 협회(ANSI)의 표준 계획 및 요구 사항 위원회(SPARC - Standards Planning and Requirements Committee)에서 제안한 데이터베이스 시스템의 표준 아키텍처입니다.

**3단계 구조**:

1. **외부 스키마 (External Schema / 사용자 관점)**
   - 개별 사용자나 응용 프로그램이 보는 데이터베이스의 일부분
   - 각 사용자 그룹별로 서로 다른 뷰(View) 제공
   - 데이터의 논리적 부분 집합 (Subset)
   - 서브 스키마(Sub-schema)라고도 함

2. **개념 스키마 (Conceptual Schema / 조직 전체 관점)**
   - 조직 전체의 데이터베이스 구조를 정의
   - 모든 사용자가 공유하는 통합된 논리적 구조
   - 데이터 간의 관계, 제약조건, 보안 요구사항 포함
   - ERD(Entity-Relationship Diagram)로 표현

3. **내부 스키마 (Internal Schema / 물리적 관점)**
   - 데이터의 물리적 저장 구조
   - 인덱스, 저장 방식, 압축, 암호화 등
   - 실제 디스크에 저장되는 형태
   - 성능 최적화를 위한 세부 사항

**2가지 매핑 (Mapping)**:

1. **외부/개념 매핑 (External/Conceptual Mapping)**
   - 외부 스키마와 개념 스키마 간의 대응 관계
   - 논리적 데이터 독립성 제공

2. **개념/내부 매핑 (Conceptual/Internal Mapping)**
   - 개념 스키마와 내부 스키마 간의 대응 관계
   - 물리적 데이터 독립성 제공

#### 2. 💡 비유를 통한 이해

**백화점**으로 비유할 수 있습니다:

```
+-------------------+
|  고객 (영업팀)     |  외부 스키마 = 고객이 보는 매장 진열
|  - 1층: 화장품     |  (각 고객은 자신이 원하는 매장만 방문)
|  - 2층: 의류       |
+-------------------+
         ↕ (엘리베이터/에스컬레이터 = 외부/개념 매핑)
+-------------------+
|  매장 설계도       |  개념 스키마 = 백화점 전체 평면도
|  - 전체 층별 구성   |  (건물 전체의 구조와 배치)
|  - 매장 간 연결     |
+-------------------+
         ↕ (시공 도면 = 개념/내부 매핑)
+-------------------+
|  건물 구조도       |  내부 스키마 = 건물의 골조와 설비
|  - 기둥, 보 위치    |  (물리적 기반 시설)
|  - 전기, 배관       |
+-------------------+
```

**물리적 독립성 예시**:
- 건물의 배관을 교체해도 매장 진열(외부)이나 평면도(개념)는 변하지 않음

**논리적 독립성 예시**:
- 매장 배치를 변경해도 각 고객이 보는 진열(외부)은 그대로 유지 가능

#### 3. 등장 배경 및 발전 과정

**문제 상황 (1970년대 초)**:
- 1세대 DBMS (IMS, IDS)는 응용 프로그램과 데이터 구조가 강하게 결합
- 파일 시스템의 데이터 종속성 문제가 DBMS로 이어짐
- 물리적 구조 변경 시 응용 프로그램 수정 불가피

**해결책 제시 (1975)**:
- ANSI/SPARC에서 3단계 스키마 제안
- 데이터 추상화와 독립성 개념 정립
- 이론적 프레임워크 제공

**관계형 모델과의 결합 (1980년대)**:
- Codd의 관계형 모델이 3단계 스키마를 구현
- SQL이 외부 인터페이스로 정착
- 뷰(View)가 외부 스키마 구현

**현대적 확장**:
- ORM: 추가적인 추상화 계층
- API Layer: 서비스 지향 외부 스키마
- Cloud-Native: 스토리지/컴퓨팅 분리

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [최소 1,000자 이상]

#### 1. 3단계 스키마 구성 요소 상세 (표)

| 계층 | 스키마 | 관점 | 정의 내용 | 사용자 | 예시 |
|:---|:---|:---|:---|:---|:---|
| **1** | 외부 스키마 | 사용자 | 사용자가 보는 데이터 부분집합 | 일반 사용자, 응용 프로그래머 | 뷰(View), 서브스키마 |
| **2** | 개념 스키마 | 조직 | 전체 데이터 논리 구조 | DBA, 데이터 설계자 | ERD, 테이블 정의 |
| **3** | 내부 스키마 | 물리 | 데이터 물리 저장 구조 | 시스템 프로그래머 | 인덱스, 파일 구조 |

#### 2. 정교한 3단계 스키마 아키텍처 다이어그램

```text
+==================================================================================+
|                  ANSI/SPARC Three-Schema Architecture                             |
+==================================================================================+
|                                                                                   |
|   USER 1           USER 2           USER 3           APPLICATION                  |
|  (영업팀)         (인사팀)         (경리팀)          (주문시스템)                   |
|      |               |               |                   |                         |
|      v               v               v                   v                         |
|  +-------+       +-------+       +-------+          +-------+                     |
|  | View  |       | View  |       | View  |          | View  |                     |
|  | 영업용 |       | 인사용 |       | 경리용 |          | 주문용 |                     |
|  +-------+       +-------+       +-------+          +-------+                     |
|                                                                                   |
|  |<------------------ EXTERNAL SCHEMA (외부 스키마) ------------------>|          |
|                                                                                   |
|      |               |               |                   |                         |
|      +---------------+---------------+-------------------+                         |
|                              |                                                    |
|                              | External/Conceptual Mapping                        |
|                              | (외부/개념 매핑)                                    |
|                              v                                                    |
|  +-----------------------------------------------------------------------------+  |
|  |                         CONCEPTUAL SCHEMA                                    |  |
|  |                           (개념 스키마)                                       |  |
|  |                                                                             |  |
|  |   +-------------+       +-------------+       +-------------+               |  |
|  |   |  CUSTOMER   |       |   ORDER     |       |  EMPLOYEE   |               |  |
|  |   +-------------+       +-------------+       +-------------+               |  |
|  |   | *customer_id|<------| *order_id   |       | *emp_id     |               |  |
|  |   |  name       |       |  customer_id|       |  name       |               |  |
|  |   |  phone      |       |  order_date |       |  dept_id    |               |  |
|  |   |  address    |       |  total_amt  |       |  salary     |               |  |
|  |   |  credit_lim |       |  status     |       |  hire_date  |               |  |
|  |   +-------------+       +-------------+       +-------------+               |  |
|  |         |                     |                     |                       |  |
|  |         |    +----------------+                     |                       |  |
|  |         |    |                                      |                       |  |
|  |         v    v                                      v                       |  |
|  |   +-------------+       +-------------+       +-------------+               |  |
|  |   | ORDER_ITEM  |       |  DEPARTMENT |       |   SALARY    |               |  |
|  |   +-------------+       +-------------+       +-------------+               |  |
|  |   | *order_id   |       | *dept_id    |       | *emp_id     |               |  |
|  |   | *item_seq   |       |  dept_name  |       |  base_sal   |               |  |
|  |   |  product_id |       |  location   |       |  bonus      |               |  |
|  |   |  quantity   |       |  manager_id |       |  effective  |               |  |
|  |   |  unit_price |       +-------------+       +-------------+               |  |
|  |   +-------------+                                                           |  |
|  |                                                                             |  |
|  |   [Integrity Constraints]                                                   |  |
|  |   - PK: customer_id, order_id, emp_id, dept_id                             |  |
|  |   - FK: order.customer_id -> customer.customer_id                          |  |
|  |   - FK: order_item.order_id -> order.order_id                              |  |
|  |   - CHECK: salary > 0, total_amt >= 0                                       |  |
|  +-----------------------------------------------------------------------------+  |
|                              |                                                    |
|                              | Conceptual/Internal Mapping                        |
|                              | (개념/내부 매핑)                                    |
|                              v                                                    |
|  +-----------------------------------------------------------------------------+  |
|  |                          INTERNAL SCHEMA                                     |  |
|  |                            (내부 스키마)                                      |  |
|  |                                                                             |  |
|  |   [Storage Structure]                                                       |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |   | Tablespace: USERS_TBLSP                                              |   |  |
|  |   | - Location: /data/oradata/users01.dbf                                |   |  |
|  |   | - Size: 100 GB, Autoextend: ON                                       |   |  |
|  |   | - Block Size: 8 KB                                                   |   |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |                                                                             |  |
|  |   [Index Structure]                                                         |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |   | Index Name          | Type   | Columns              | Tablespace    |   |  |
|  |   |---------------------|--------|----------------------|---------------|   |  |
|  |   | PK_CUSTOMER         | B+Tree | customer_id          | IDX_TBLSP     |   |  |
|  |   | IDX_CUSTOMER_NAME   | B+Tree | name                 | IDX_TBLSP     |   |  |
|  |   | IDX_ORDER_CUST_DATE | B+Tree | customer_id,order_dt | IDX_TBLSP     |   |  |
|  |   | IDX_ORDER_DATE      | Bitmap | order_date           | IDX_TBLSP     |   |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |                                                                             |  |
|  |   [Partitioning]                                                            |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |   | Table: ORDER                                                          |   |  |
|  |   | Partitioning Type: RANGE                                               |   |  |
|  |   | Partition Key: order_date                                              |   |  |
|  |   | - P_2024_Q1: 2024-01-01 to 2024-04-01                                 |   |  |
|  |   | - P_2024_Q2: 2024-04-01 to 2024-07-01                                 |   |  |
|  |   | - P_2024_Q3: 2024-07-01 to 2024-10-01                                 |   |  |
|  |   | - P_2024_Q4: 2024-10-01 to 2025-01-01                                 |   |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |                                                                             |  |
|  |   [Compression & Encryption]                                                |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |   | Compression: Advanced Row Compression (OLTP)                          |   |  |
|  |   | Encryption: TDE (Transparent Data Encryption) - AES-256               |   |  |
|  |   +---------------------------------------------------------------------+   |  |
|  +-----------------------------------------------------------------------------+  |
|                              |                                                    |
+==============================|====================================================+
                               v
+==================================================================================+
|                            PHYSICAL STORAGE                                      |
|  +------------------+  +------------------+  +------------------+                |
|  |  SSD (Primary)   |  |  HDD (Archive)   |  |  Tape (Backup)   |                |
|  |  /data/oradata/  |  |  /archive/ora/   |  |  /backup/tape/   |                |
|  +------------------+  +------------------+  +------------------+                |
+==================================================================================+
```

#### 3. 심층 동작 원리: 매핑 처리 과정

**외부/개념 매핑 (External/Conceptual Mapping)**

```text
사용자 쿼리 (외부 스키마):
SELECT customer_name, total_orders
FROM sales_view
WHERE region = '서울';

뷰 정의 (외부 스키마):
CREATE VIEW sales_view AS
SELECT c.name AS customer_name,
       c.region,
       COUNT(o.order_id) AS total_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.region;

매핑 변환 (개념 스키마):
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.region = '서울'
GROUP BY c.customer_id, c.name;
```

**개념/내부 매핑 (Conceptual/Internal Mapping)**

```text
개념 스키마 쿼리:
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.region = '서울'
GROUP BY c.customer_id, c.name;

내부 스키마 실행 계획:
1. IDX_CUSTOMER_REGION (Bitmap)으로 서울 지역 고객 식별
2. IDX_ORDER_CUSTOMER (B+Tree)로 주문 정보 조인
3. 파티션 프루닝: ORDER 테이블에서 필요한 파티션만 스캔
4. 해시 집계로 GROUP BY 수행
5. 버퍼 캐시 활용, 필요시 디스크 I/O
```

#### 4. 핵심 알고리즘: 쿼리 변환 (Query Transformation)

```python
"""
3단계 스키마 매핑을 통한 쿼리 변환 알고리즘
"""

class ThreeSchemaMapper:
    """3단계 스키마 매핑 엔진"""

    def __init__(self, catalog):
        self.catalog = catalog

    def transform_query(self, external_query: str) -> str:
        """
        외부 스키마 쿼리를 내부 실행 가능한 쿼리로 변환
        """
        # 1. 외부 쿼리 파싱
        parsed = self.parse(external_query)

        # 2. 외부/개념 매핑: 뷰 확장
        conceptual_query = self.external_to_conceptual(parsed)

        # 3. 개념/내부 매핑: 물리적 최적화
        internal_plan = self.conceptual_to_internal(conceptual_query)

        return internal_plan

    def external_to_conceptual(self, parsed_query) -> str:
        """
        외부 스키마 -> 개념 스키마 변환
        - 뷰 확장 (View Expansion)
        - 열 이름 매핑
        """
        # 뷰 참조 식별
        view_refs = self.find_view_references(parsed_query)

        for view_name in view_refs:
            # 뷰 정의 조회
            view_def = self.catalog.get_view_definition(view_name)

            # 뷰를 기본 테이블로 확장
            parsed_query = self.expand_view(parsed_query, view_name, view_def)

        # 조건 병합 (Predicate Pushdown)
        parsed_query = self.push_predicates(parsed_query)

        return self.generate_sql(parsed_query)

    def conceptual_to_internal(self, conceptual_query: str) -> dict:
        """
        개념 스키마 -> 내부 스키마 변환
        - 인덱스 선택
        - 파티션 프루닝
        - 조인 순서 최적화
        """
        # 통계 정보 수집
        stats = self.catalog.get_statistics()

        # 가능한 실행 계획 생성
        plans = self.generate_plans(conceptual_query, stats)

        # 비용 기반 최적화
        best_plan = self.select_best_plan(plans)

        return best_plan

    def expand_view(self, query, view_name, view_definition):
        """
        뷰를 기본 테이블 쿼리로 확장
        """
        # 뷰의 SELECT 절을 서브쿼리로 대체
        # 열 이름 매핑 적용
        # WHERE 조건 병합
        pass

# 예시: 매핑 과정
"""
[외부 쿼리 - 영업팀 사용자]
SELECT customer_name, order_count
FROM sales_customer_view
WHERE customer_grade = 'VIP';

[뷰 정의]
CREATE VIEW sales_customer_view AS
SELECT c.name AS customer_name,
       CASE WHEN c.credit_limit >= 10000 THEN 'VIP'
            ELSE 'NORMAL' END AS customer_grade,
       (SELECT COUNT(*) FROM orders o
        WHERE o.customer_id = c.customer_id) AS order_count
FROM customers c;

[개념 쿼리 - 확장 후]
SELECT c.name,
       (SELECT COUNT(*) FROM orders o
        WHERE o.customer_id = c.customer_id)
FROM customers c
WHERE CASE WHEN c.credit_limit >= 10000 THEN 'VIP'
           ELSE 'NORMAL' END = 'VIP';

[최적화된 내부 실행 계획]
1. IDX_CUSTOMER_CREDIT (B+Tree)로 credit_limit >= 10000 필터링
2. NESTED LOOP JOIN으로 orders 집계
3. 결과 반환
"""
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개 이상]

#### 1. 3단계 스키마 vs 다른 아키텍처 비교

| 비교 항목 | 3단계 스키마 | MVC 패턴 | OSI 7계층 |
|:---|:---|:---|:---|
| **영역** | 데이터베이스 | 소프트웨어 | 네트워크 |
| **계층 수** | 3단계 | 3단계 | 7계층 |
| **핵심 목표** | 데이터 독립성 | 관심사 분리 | 프로토콜 표준화 |
| **매핑** | 외부/개념, 개념/내부 | Controller가 Model-View 연결 | 각 계층 간 인터페이스 |
| **추상화** | 데이터 추상화 | UI/로직 분리 | 통신 추상화 |

#### 2. 매핑 유형별 특성 비교

| 매핑 유형 | 역할 | 복잡도 | 성능 영향 | 유지보수 |
|:---|:---|:---|:---|:---|
| **외부/개념 매핑** | 뷰 -> 테이블 | 높음 | 중간 | DBA |
| **개념/내부 매핑** | 테이블 -> 파일 | 중간 | 높음 | DBMS 자동 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision) - [최소 800자 이상]

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 대규모 스키마 마이그레이션**
- **상황**: 레거시 시스템의 개념 스키마 전면 개편
- **문제**: 200개 응용 프로그램 영향 우려
- **전략**: 외부 스키마(뷰)를 그대로 유지하며 개념 스키마만 변경
- **결과**: 무중단 마이그레이션 달성

**시나리오 2: 성능 최적화를 위한 내부 스키마 변경**
- **상황**: 쿼리 응답 시간 10초로 SLA 위반
- **전략**: 내부 스키마만 최적화 (인덱스, 파티셔닝)
- **결과**: 개념/외부 스키마 변경 없이 응답 시간 0.5초로 개선

#### 2. 도입 시 고려사항 (체크리스트)

**외부 스키마 설계**:
- [ ] 사용자 그룹별 뷰 정의
- [ ] 보안 정책 반영 (마스킹, 필터링)
- [ ] 성능 고려 (복잡한 뷰 지양)

**개념 스키마 설계**:
- [ ] 정규화 수준 결정
- [ ] 무결성 제약조건 정의
- [ ] 확장성 고려

**내부 스키마 설계**:
- [ ] 인덱스 전략
- [ ] 파티셔닝 전략
- [ ] 스토리지 최적화

#### 3. 안티패턴 (Anti-patterns)

1. **Direct Table Access**: 뷰 없이 테이블 직접 접근
2. **Bypass Mapping**: 스키마 계층 무시
3. **Over-Complex Views**: 너무 복잡한 뷰 정의

---

### Ⅴ. 기대효과 및 결론 (Future & Standard) - [최소 400자 이상]

#### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|:---|:---|:---|:---|
| **스키마 변경 영향** | 전체 앱 수정 | 뷰만 수정 | 95% 감소 |
| **유지보수 비용** | 높음 | 낮음 | 70% 절감 |
| **데이터 독립성** | 없음 | 완전 보장 | 품질 향상 |

#### 2. 미래 전망

- API 레이어로 외부 스키마 개념 확장
- GraphQL 스키마와의 융합
- 자동 매핑 최적화 (AI 기반)

#### 3. 참고 표준

- ANSI/X3/SPARC (1975)
- ISO/IEC 9075 (SQL)

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[데이터 독립성](@/studynotes/5_database/1_relational/4_data_independence.md)**: 3단계 스키마의 목표
- **[스키마](@/studynotes/5_database/1_relational/5_schema_definition.md)**: 각 계층의 구조 정의
- **[뷰](@/studynotes/5_database/2_sql/view.md)**: 외부 스키마의 구현
- **[DBMS](@/studynotes/5_database/1_relational/3_dbms_definition.md)**: 아키텍처를 구현하는 시스템

---

### 👶 어린이를 위한 3줄 비유 설명

1. **햄버거 가게**: 손님은 메뉴판만 보고 주문해요(외부 스키마). 주방에는 재료가 어떻게 쌓여있는지 정리된 창고가 있고(내부 스키마), 그 사이에 가게 전체가 어떻게 운영되는지 규칙이 있어요(개념 스키마)!

2. **학교 건물**: 학생들은 자기 교실만 알면 돼요(외부). 학교 전체 평면도에는 모든 교실이 있고(개념), 건물 지하에는 기계실과 배관이 있어요(내부). 각각이 따로 관리되죠!

3. **스마트폰 앱**: 우리는 앱 화면만 봐요(외부). 앱 뒤에는 데이터가 어떻게 정리되어 있는지 구조가 있고(개념), 실제 데이터는 멀리 있는 서버 컴퓨터에 저장돼요(내부)!
