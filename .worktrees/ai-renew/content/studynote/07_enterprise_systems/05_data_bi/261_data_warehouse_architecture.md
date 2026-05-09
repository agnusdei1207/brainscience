+++
weight = 261
title = "데이터 웨어하우스 (Data Warehouse) 아키텍처"
date = "2024-03-21"
[extra]
categories = "studynote-enterprise"
+++

## 핵심 인사이트 (3줄 요약)
1. **의사결정 지원의 통합 저장소**: 데이터 웨어하우스(DW)는 기업 내 여러 운영 시스템(OLTP)의 데이터를 주제별로 통합하여 분석 목적에 맞게 최적화한 비즈니스 지능의 핵심 기지이다.
2. **4대 핵심 특징**: 주제 지향성(Subject), 통합성(Integrated), 시계열성(Time-variant), 비휘발성(Non-volatile)을 통해 장기적인 추세 분석과 전략 수립을 가능하게 한다.
3. **ETL을 통한 가치 정제**: 원천 데이터의 추출(E), 변환(T), 적재(L) 과정을 거치며 데이터의 정합성을 확보하고 분석 가능한 형태로 정제한다.

---

### Ⅰ. 개요 (Context & Background)
현대 기업은 분산된 수많은 시스템에서 초 단위로 발생하는 데이터를 마주하고 있다. 하지만 운영 시스템(ERP, CRM 등)은 빠른 트랜잭션 처리가 목적이지 분석을 위한 구조가 아니다. 이를 해결하기 위해 **데이터 웨어하우스(DW)**는 분석 전용 저장 공간을 구축하여 경영진에게 과거부터 현재까지의 통합된 가시성을 제공한다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

엔터프라이즈 DW 아키텍처는 데이터의 흐름에 따라 **소스 - 스테이징 - DW - DM - 활용**의 계층 구조를 갖는다.

```text
[ Data Source ]        [ Data Integration Layer ]     [ Analysis Layer ]
( ERP )-----+         +---------------------+        +-----------------+
            |         |  ( ETL Engine )     |        |   ( OLAP )      |
( CRM )-----|--( E )-->  [ Staging Area ]   |--( L )--> [ Enterprise DW ]
            |         |  [ Transformation ] |        |                 |
( Legacy )--+         +---------------------+        +--------+--------+
                                                              |
                                                     +--------+--------+
                                                     | ( Data Marts )  |
                                                     | [ Fin ] [ Mkt ] |
                                                     +-----------------+
```

1. **Operational Data (소스)**: 운영 시스템의 원천 데이터.
2. **Staging Area (스테이징)**: 데이터를 원형 그대로 복사하여 임시 저장하는 공간. 운영 DB 부하 방지.
3. **ETL (추출-변환-적재)**: 데이터의 정제(Cleaning)와 표준화가 이루어지는 핵심 프로세스.
4. **EDW (엔터프라이즈 DW)**: 전사적 관점의 통합 데이터 저장소 (Inmon 방식).
5. **Data Mart (데이터 마트)**: 특정 부서나 주제에 맞게 요약/분리된 소규모 DW (Kimball 방식).

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 데이터 웨어하우스 (DW) | 운영 데이터베이스 (DB) | 데이터 레이크 (Lake) |
| :--- | :--- | :--- | :--- |
| **목적** | 의사결정 분석 (OLAP) | 실시간 트랜잭션 (OLTP) | 대규모 원시 데이터 탐색 |
| **데이터 구조** | 정형화, 비정규화 (Star Schema) | 정형화, 정규화 (3NF) | 비정형/반정형 원시 데이터 |
| **Schema 전략** | Schema-on-write (엄격함) | Schema-on-write (엄격함) | Schema-on-read (유연함) |
| **사용자** | 경영진, 분석가, 데이터 과학자 | 실무자, 응용 프로그램 | 데이터 과학자, 머신러닝 엔지니어 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **클라우드 전환 (Modern DW)**: 온프레미스 DW의 용량 한계와 하드웨어 비용 문제를 해결하기 위해 Snowflake, BigQuery와 같은 클라우드 네이티브 DW로의 전환이 가속화되고 있다.
2. **SCD(Slowly Changing Dimension) 전략**: 차원 데이터(예: 주소)가 변할 때 이력을 남길 것인가(Type 2) 아니면 덮어쓸 것인가(Type 1)에 대한 설계가 DW 분석 신뢰도의 핵심이다.
3. **기술사적 판단**: 최근에는 DW와 Data Lake의 장점을 결합한 **Lakehouse** 아키텍처가 부상하고 있다. DW는 결과론적 분석(Descriptive)뿐만 아니라 예측 분석(Predictive)을 위한 AI 모델 학습 데이터 공급처로서 그 위상이 강화되고 있다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
DW 아키텍처는 기업의 데이터 자산을 지능화하는 가장 견고한 기반이다. 향후 실시간 스트리밍 데이터와의 결합(Lambda/Kappa Architecture)을 통해 **'리얼타임 엔터프라이즈(RTE)'**를 구현하는 것이 궁극적인 지향점이다. 데이터의 단순 저장을 넘어 통찰(Insight)을 뽑아내는 능력이 기업의 경쟁력이 된다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: Business Intelligence, Enterprise Architecture
- **자식 개념**: Data Mart, ODS, Dimensional Modeling
- **연관 개념**: ETL, ELT, OLAP, Star Schema, Big Data

---

### 👶 어린이를 위한 3줄 비유 설명
1. DW는 학교 도서관처럼 모든 정보를 **주제별로 잘 정리해 둔 커다란 책꽂이**예요.
2. 매일매일 쓰는 일기장(운영 DB)과 달리, DW는 **오랫동안 모아둔 기록**을 한꺼번에 살펴볼 때 아주 편리해요.
3. 여러 정보를 하나로 합치고 틀린 글자를 고쳐서(ETL) 깨끗한 정보만 모아두는 곳이랍니다.
