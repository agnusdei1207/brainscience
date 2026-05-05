+++
weight = 321
title = "데이터 마이닝 프레임워크 (CRISP-DM & KDD)"
date = "2024-03-21"
[extra]
categories = "studynote-ict-convergence"
+++
## 0. 핵심 인사이트

> (2) Data Understanding

> 📝 모범 답안

1. **데이터 기반 가치 창출**: 데이터 마이닝 프레임워크는 방대한 데이터 속에 숨겨진 유의미한 패턴과 지식을 발견하기 위한 체계적인 절차를 제공한다.
2. **반복적 및 단계적 프로세스**: 데이터의 이해부터 전처리, 모델링, 평가에 이르기까지 일관된 단계를 거치며, 필요시 이전 단계로 회귀하는 유연성을 지닌다.
3. **글로벌 표준 CRISP-DM**: 비즈니스 이해를 최우선으로 하는 CRISP-DM은 산업계에서 가장 널리 쓰이며, 학술적인 KDD와 함께 데이터 분석의 양대 산맥을 이룬다.

---

### 1. 개요 및 필요성
데이터 마이닝(Data Mining)은 단순히 도구를 돌리는 것이 아니라, 비즈니스 목적을 달성하기 위한 지식 발견의 여정이다. 이를 위해 **KDD(Knowledge Discovery in Databases)**는 데이터 중심의 학술적 절차를, **CRISP-DM(Cross-Industry Standard Process for Data Mining)**은 비즈니스 실행 중심의 산업 표준 절차를 제안하여 분석의 성공률을 높인다.

---

### 2. 구성요소

CRISP-DM은 6단계의 순환 구조를 가지며, KDD는 데이터 선택부터 평가까지의 흐름을 강조한다.

```text
[ CRISP-DM Cycle ]
(1) Business Understanding <---             |                           |
             +-----------+---------------+
                         |
                (3) Data Preparation <---> (4) Modeling
                         |                     |
                         +-----------+---------+
                                     |
                                (5) Evaluation --(Fail)--> Back to Step 1
                                     |
                                (6) Deployment
```

1. **Business Understanding (비즈니스 이해)**: 비즈니스 목표 설정 및 데이터 마이닝 요구사항 파악.
2. **Data Understanding (데이터 이해)**: 초기 데이터 수집 및 데이터 특성 파악, 품질 확인.
3. **Data Preparation (데이터 준비)**: 분석용 데이터셋 구축 (Cleansing, Transformation).
4. **Modeling (모델링)**: 다양한 알고리즘(회귀, 분류, 군집 등) 적용 및 파라미터 튜닝.
5. **Evaluation (평가)**: 비즈니스 목적에 부합하는지 평가하고 이전 단계 검토.
6. **Deployment (전개)**: 실무 시스템 적용 및 결과 리포팅.

---

### 3. 구조 및 동작 원리

| 비교 항목 | KDD (Knowledge Discovery) | CRISP-DM (Business Standard) | SEMMA (SAS Method) |
| :--- | :--- | :--- | :--- |
| **주요 특징** | 학술적, 데이터 중심 지식 발견 | 산업 표준, 비즈니스 중심 | SAS 솔루션 중심의 분석 절차 |
| **단계 구성** | 5단계 (Selection~Evaluation) | 6단계 (Biz Understand~Deploy) | 5단계 (Sample~Assess) |
| **중점 사항** | 기술적 무결성과 지식 추출 | 비즈니스 성과와 반복성 | 분석 기법의 효율적 적용 |
| **상호 작용** | 일직선적 흐름 강조 | 단계 간 유연한 피드백 순환 | 도구 활용 중심의 순환 |

---

### 4. 비교 및 트레이드오프
1. **분석 과제 성격에 따른 선택**: 프로젝트가 비즈니스 가치 창출 중심이라면 CRISP-DM을, 원천 데이터의 새로운 특성을 찾는 탐색적 성격이 강하다면 KDD를 추천한다.
2. **데이터 거버넌스와의 연계**: 데이터 준비(Preparation) 단계는 전체 시간의 60~80%를 차지하므로, 평소에 잘 정제된 데이터 레이크나 마스터 데이터 관리(MDM)가 구축되어 있어야 한다.
3. **기술사적 판단**: 최근 MLOps의 확산으로 인해 Deployment 단계 이후의 **지속적 모니터링(Monitoring)**과 **재학습(Retraining)** 단계가 CRISP-DM의 7번째 단계로 실질적으로 추가되고 있는 추세이다.

---

### 5. 실무 적용 및 최적화 기법
데이터 마이닝 프레임워크는 데이터 팀과 현업 부서 간의 **공통 언어**를 제공한다. 향후 생성형 AI와 자동화된 ML(AutoML) 환경에서도 이러한 기초적인 분석 프로세스는 여전히 프로젝트의 성패를 가르는 나침반 역할을 할 것이다. 결론적으로 절차의 준수가 곧 분석 품질의 신뢰도로 이어진다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: Data Science, Analytics Methodology
- **자식 개념**: Data Cleansing, Machine Learning, Evaluation Metrics
- **연관 개념**: MLOps, Big Data, Business Intelligence (BI)

---

### 👶 어린이를 위한 3줄 비유 설명
1. 데이터 마이닝은 산더미 같은 흙더미에서 **반짝이는 보석(지식)**을 찾아내는 작업이에요.
2. 보석을 찾기 위해서는 **"어떤 보석이 필요한지(비즈니스)"** 먼저 생각하고, 땅을 파고, 보석을 닦는 순서(프레임워크)가 필요해요.
3. 순서 없이 그냥 파기만 하면 시간만 낭비할 수 있으니, 꼭 **분석 지도**를 보고 따라가야 한답니다.
