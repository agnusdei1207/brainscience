+++
weight = 262
title = "데이터 마트 (Data Mart) 개념 및 설계"
date = "2024-03-21"
[extra]
categories = "studynote-enterprise"
+++

## 핵심 인사이트 (3줄 요약)
1. **부서별 맞춤형 분석 환경**: 데이터 마트(DM)는 전사적 데이터 웨어하우스(DW)로부터 특정 부서(마케팅, 재무 등)나 특정 비즈니스 영역에 필요한 데이터만을 추출하여 구축한 소규모 분석 저장소이다.
2. **빠른 응답 및 사용성 극대화**: 전사 데이터를 다 뒤질 필요 없이 필요한 데이터만 요약·구성되어 있어 쿼리 성능이 빠르고 현업 사용자가 이해하기 쉬운 구조를 가진다.
3. **상향식(Kimball) vs 하향식(Inmon) 접근**: DW를 먼저 구축하고 마트를 만드는 하향식과, 마트를 먼저 구축하여 통합해가는 상향식 전략으로 구분된다.

---

### Ⅰ. 개요 (Context & Background)
모든 부서가 거대한 엔터프라이즈 데이터 웨어하우스(EDW)를 직접 사용하는 것은 비효율적이다. 마케팅팀은 고객 행동 데이터가 중요하고, 재무팀은 회계 장부가 중요하다. **데이터 마트(Data Mart)**는 이러한 부서별 '데이터 사일로'를 해소하면서도 각자의 업무에 최적화된 데이터 뷰(View)를 제공하기 위해 설계된다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

데이터 마트는 EDW로부터 파생되거나(Dependent), 운영 시스템에서 직접 구축될(Independent) 수 있다.

```text
[ Architecture Types ]

1. Dependent DM (의존형)      2. Independent DM (독립형)
   ( EDW )                      ( Operational DB )
      |                                |
      +----( ETL/Filter )              +----( ETL/Filter )
      |                                |
[ Data Mart ]                    [ Data Mart ]
( Finance )                      ( Marketing )
```

*   **의존형 마트 (Dependent DM)**: EDW를 원천으로 하여 데이터의 정합성(Consistency)이 보장된다. 중앙 집중 통제가 가능하다.
*   **독립형 마트 (Independent DM)**: EDW 없이 직접 운영 시스템에서 데이터를 가져온다. 구축 속도는 빠르나 부서 간 데이터 불일치(Island of Data)가 발생할 위험이 크다.
*   **설계 기법**: 주로 **스타 스키마(Star Schema)**를 사용하여 현업이 BI 도구로 쉽게 분석할 수 있도록 비정규화된 구조를 취한다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 데이터 웨어하우스 (EDW) | 데이터 마트 (Data Mart) |
| :--- | :--- | :--- |
| **분석 범위** | 전사적 (Enterprise-wide) | 특정 부서/주제 (Department-specific) |
| **데이터 크기** | 대용량 (TB~PB) | 중소용량 (GB~TB) |
| **데이터 상세도** | 상세 데이터 (Atomic) | 요약 데이터 (Summarized) 중심 |
| **구축 기간** | 수개월 ~ 수년 (Long-term) | 수주 ~ 수개월 (Short-term) |
| **원천 데이터** | 다수의 운영 시스템 | EDW 또는 특정 운영 시스템 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **데이터 거버넌스의 유지**: 독립형 마트가 난립하면 "A팀 매출 숫자와 B팀 매출 숫자가 다르다"는 문제가 발생한다. 가능한 EDW를 중심으로 한 의존형 마트 구조를 지향해야 한다.
2. **가상 데이터 마트 (Virtual DM)**: 물리적으로 데이터를 복제하지 않고, 뷰(View)나 데이터 가상화 기술을 통해 논리적인 마트를 구성하여 스토리지 비용을 절감할 수 있다.
3. **기술사적 판단**: 빅데이터 시대에는 모든 데이터를 EDW에 넣기보다, **Data Lake**에 원시 데이터를 쌓고 필요한 시점에 **Data Mart**로 빠르게 가공하여 서빙하는 'Just-in-time' 분석 환경 구축이 트렌드이다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
데이터 마트는 분석의 **민첩성(Agility)**을 부여한다. 현업 사용자에게 최적화된 데이터를 제공함으로써 의사결정의 속도를 높이고, IT 부서의 리포팅 업무 부하를 줄여준다. 결과적으로 데이터 민주화(Data Democratization)를 실현하는 실질적인 접점이 된다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: Business Intelligence, Data Warehousing
- **자식 개념**: Dependent DM, Independent DM, Star Schema
- **연관 개념**: OLAP, BI Tools, ETL, Data Island, Data Democratization

---

### 👶 어린이를 위한 3줄 비유 설명
1. 데이터 마트는 거대한 대형마트(DW)에서 내가 좋아하는 **사탕 코너(특정 주제)**만 따로 떼어놓은 작은 가게와 같아요.
2. 마트 전체를 돌아다닐 필요 없이 **내가 원하는 것만 빨리 찾을 수 있어**서 아주 편리해요.
3. 하지만 사탕 가게의 가격이 대형마트랑 다르면 안 되니까, **정보를 잘 맞춰두는 것**이 중요하답니다.
