+++
weight = 267
title = "데이터 프로파일링 (Data Profiling)"
date = "2024-03-21"
[extra]
categories = "studynote-enterprise"
+++

## 핵심 인사이트 (3줄 요약)
1. 원천 데이터(Source Data)의 메타데이터를 수집하고 통계적 특성을 분석하여 데이터의 품질 상태, 구조, 패턴을 체계적으로 진단하는 기술입니다.
2. ETL 과정 전후에 수행되어 데이터 정제(Cleansing) 전략을 수립하고, 데이터 웨어하우스(DW)로의 잘못된 데이터 유입을 사전에 차단하는 역할을 합니다.
3. 데이터의 일관성, 완전성, 유효성을 수치화하여 데이터 거버넌스 및 품질 관리 체계의 객관적 근거를 제공합니다.

### Ⅰ. 개요 (Context & Background)
- **배경**: 엔터프라이즈 환경에서 데이터의 소스가 복잡해지고 파편화되면서, 분석 결과의 신뢰성을 확보하기 위한 데이터 품질(Data Quality) 진단의 중요성이 증대되었습니다.
- **정의**: 데이터 소스로부터 데이터 구조, 내용, 상호 관계 및 비즈니스 규칙 준수 여부를 분석하여 통계적 정보를 생성하는 일련의 활동입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **핵심 원리**: 컬럼 분석(Column Analysis), 관계 분석(Relationship Analysis), 도메인 분석(Domain Analysis)을 단계적으로 수행합니다.

```text
[ Data Profiling Process Flow ]

  [ Source DB ]      [ Profiling Engine ]      [ Analysis Report ]
  +-----------+      +------------------+      +-----------------+
  | Raw Data  | -->  |  1. Column Info  | -->  |  - Cardinality  |
  | Table A   |      |  2. Cross-Table  |      |  - Null Counts  |
  | Table B   |      |  3. Rule Check   |      |  - Outlier List |
  +-----------+      +------------------+      +-----------------+
                           ^
                           |
                     [ Data Dictionary ]
                     - Meta info
                     - Business Rules

* Primary Key Discovery: 후보 키(Candidate Key) 식별 및 중복 검사
* Functional Dependency: 컬럼 간 종속 관계 및 비즈니스 로직 유효성 검증
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
- **데이터 프로파일링 vs 데이터 정제 (Cleansing)**

| 비교 항목 | 데이터 프로파일링 (Profiling) | 데이터 정제 (Cleansing) |
| :--- | :--- | :--- |
| 주요 활동 | 조사 및 진단 (Diagnosis) | 수정 및 보완 (Treatment) |
| 수행 시점 | 분석/정제 전 (Prior) | 프로파일링 결과 기반 (After) |
| 주요 결과물 | 품질 진단 리포트, 통계치 | 무결한 데이터, 표준화 데이터 |
| 목적 | 데이터 상태 파악 | 데이터 품질 향상 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **기술사적 판단**: 데이터 프로파일링은 일회성 작업이 아닌 **'지속적 모니터링'** 관점으로 접근해야 합니다. 특히 최근 **데이터 레이크(Data Lake)** 환경에서 데이터 늪(Data Swamp)을 방지하기 위한 필수 선행 공정으로 자리 잡고 있습니다.
- **실무 전략**: 모든 데이터를 전수 조사하기보다는 중요도가 높은 핵심 데이터(Core Data)를 중심으로 프로파일링 범위를 설정하고, 자동화 도구를 활용하여 오탐율을 낮추는 전략이 필요합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 데이터 결함으로 인한 비즈니스 의사결정 오류를 최소화하고, ETL 개발 기간 및 데이터 통합 리스크를 대폭 절감할 수 있습니다.
- **결론**: 데이터 프로파일링은 'Garbage In, Garbage Out'을 막는 최전방 방어선이며, 향후 AI 기반의 자동 프로파일링 기술로 진화하여 데이터 관리 생산성을 높일 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
1. **Metadata Management**: 데이터의 기원, 정의, 구조 정보를 전사적으로 관리하는 체계
2. **Data Lineage**: 데이터의 생성부터 소멸까지의 흐름을 추적하는 기술
3. **Information Quality (IQ)**: 정보의 가용성, 신뢰성 등 사용자 관점의 품질 수준

### 👶 어린이를 위한 3줄 비유 설명
1. 데이터 프로파일링은 요리사가 요리하기 전에 '재료의 상태를 확인하는 것'과 같아요.
2. 당근이 썩지는 않았는지, 상추가 신선한지 꼼꼼하게 살펴보는 거예요.
3. 재료가 싱싱해야 맛있는 요리가 나오듯, 데이터가 깨끗해야 훌륭한 결과가 나온답니다!
