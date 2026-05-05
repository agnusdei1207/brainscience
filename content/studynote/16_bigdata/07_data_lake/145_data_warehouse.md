+++
weight = 145
title = "데이터 웨어하우스 (Data Warehouse)"
date = "2024-05-22"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 데이터 웨어하우스 (Data Warehouse)은(는) 원시 데이터 저장의 유연성과 분석 거버넌스의 통제를 함께 확보하기 위한 현대 데이터 플랫폼 핵심 개념이다.
> **비유**: 자유롭게 물을 모으는 저수지에 수문·정수 설비를 함께 갖춘 복합 수자원 시설과 같다.

📝 모범 답안

## 1. 개요 및 필요성

운영 시스템(OLTP)은 트랜잭션 처리에 최적화되어 있어 복잡한 분석 쿼리에는 부적합하다. 데이터 웨어하우스는 빌 인먼(Bill Inmon)과 랄프 킴벌(Ralph Kimball)의 이론을 바탕으로, 과거부터 현재까지의 데이터를 분석하기 좋은 형태로 통합하여 기업의 전략적 의사결정을 돕는 기술이다.

---

## 2. 구성요소

데이터 웨어하우스는 ETL 과정을 통해 원천 시스템에서 데이터를 가져와 전용 저장소에 적재한다.

```text
[ Data Warehouse Architecture / 데이터 웨어하우스 아키텍처 ]

    Source Systems (ERP, CRM)          Data Warehouse (DW)             BI & Analytics
    +-------------------+       +-----------------------+       +-------------------+
    | [Operational DB]  |       |     [Staging Area]    |       |  Reporting Tools  |
    | [Flat Files]      | ----    | [External API]    |       +-----------+-----------+       +---------+---------+
    +---------+---------+                   |                             |
                                            v                             v
                                +-----------+-----------+       +---------+---------+
                                |      Data Marts       | ----> |  Ad-hoc Analysis  |
                                | (Sales, Finance, etc) |       |  (Excel, BI)      |
                                +-----------------------+       +-------------------+
```

1. **4대 특징 (Inmon)**:
   - **주제 중심적 (Subject Oriented)**: 고객, 상품 등 특정 주제별 데이터 구성.
   - **통합적 (Integrated)**: 전사의 데이터를 표준화된 포맷으로 통합.
   - **시계열적 (Time Variant)**: 과거의 이력 데이터를 보존.
   - **비휘발성 (Non-volatile)**: 한 번 적재된 데이터는 삭제되지 않음.
2. **모델링**: 스타 스키마(Star Schema)와 눈송이 스키마(Snowflake Schema)를 사용하여 분석 속도를 최적화한다.

---

## 3. 구조 및 원리

**핵심 조건**: 저장 포맷, 메타데이터, 트랜잭션, 거버넌스 계층을 함께 설계해야 한다.

동작 순서:
| 비교 항목 | 데이터 웨어하우스 (DW) | 운영 데이터베이스 (OLTP) |
| :--- | :--- | :--- |
| **주요 목적** | 의사결정 지원 및 분석 | 일상적 트랜잭션 처리 |
| **데이터 범위** | 과거 이력 포함 (수년) | 현재 상태 위주 (수개월) |
| **작업 단위** | 복잡한 대량의 쿼리 | 작고 빠른 트랜잭션 |
| **핵심 기술** | OLAP, MPP, Columnar Storage | SQL, Indexing, Normalization |

---

## 4. 비교 및 연결

1. **MPP 아키텍처**: 최신 클라우드 DW(Snowflake, BigQuery)는 수많은 컴퓨팅 노드를 병렬로 사용하여 수조 건의 데이터를 초 단위로 쿼리한다.
2. **ELT의 부상**: 클라우드 DW의 강력한 연산력을 활용하기 위해 정제 작업을 DW 내부에서 수행하는 ELT(Extract, Load, Transform) 방식이 선호된다.
3. **PE 관점의 판단**: DW는 품질이 검증된 'Single Source of Truth'여야 한다. 데이터 정합성(Consistency)과 계보 관리가 뒷받침되지 않으면 신뢰할 수 없는 분석 결과를 낳게 된다.

---

## 5. 실무 적용 및 판단

데이터 웨어하우스는 사라지지 않고 데이터 레이크와 결합하여 '데이터 레이크하우스'로 진화하고 있다. 정형 데이터의 정밀함과 비정형 데이터의 방대함을 동시에 아우르는 하이브리드 전략이 향후 기업 데이터 아키텍처의 표준이 될 것이며, 이는 AI 기반의 자동화된 통찰(Augmented Analytics)을 이끌어낼 것이다.

---

## 6. 기대효과 및 결론

데이터 웨어하우스 (Data Warehouse)은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 레이크하우스 계열 기술은 저장 유연성과 거버넌스 통제를 동시에 달성할 때 비로소 플랫폼 가치가 커진다.

---

## 7. 발전 흐름도

```text
[상위 개념: Data Infrastructure, Business Intelligence]
    │
    ▼
[하위 개념: Data Mart, ETL/ELT, Star Schema, OLAP]
    │
    ▼
[연관 개념: OLTP vs OLAP, MPP, Data Lakehouse]
```

이 흐름도는 상위 개념: Data Infrastructure, Business Intelligence에서 출발해 연관 개념: OLTP vs OLAP, MPP, Data Lakehouse까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

- **상위 개념**: Data Infrastructure, Business Intelligence
- **하위 개념**: Data Mart, ETL/ELT, Star Schema, OLAP
- **연관 개념**: OLTP vs OLAP, MPP, Data Lakehouse
