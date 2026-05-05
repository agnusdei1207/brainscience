+++
weight = 104
title = "분류 (Classification) 분석"
date = "2024-03-20"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 분류 (Classification) 분석은(는) 대규모 데이터에서 패턴·예측·의사결정 근거를 추출하기 위한 분석 기법 또는 모델이다.
> **비유**: 광산에서 캐낸 원석을 분류·정제해 의미 있는 보석으로 가공하는 과정과 같다.

📝 모범 답안

## 1. 개요 및 필요성

- **정의:** 이산적인 결과값(Yes/No, A/B/C)을 예측하는 기법으로, 비즈니스 영역에서 가장 광범위하게 쓰이는 분석 기퍼임.
- **활용 사례:** 스팸 메일 분류, 질병 유무 판독, 이탈 고객 예측, 이미지 객체 인식 등 무수히 많은 도메인에 적용됨.

---

## 2. 구성요소

- **프로세스:** 데이터 수집 -- **Bilingual ASCII Diagram:**
```text
[Classification Logic & Decision Boundary / 분류 로직 및 결정 경계]

   Feature Y (x2)
      ^
      |   Class A (O)    |    Class B (X)
      |         O   O    |    X     X
      |      O     O     |      X     X
      |   ---------------|----------------  <-- Optimal Boundary
      |          O   O   |   X     X
      |       O          |      X
      +---------------------------------------> Feature X (x1)

[Major Algorithms / 주요 알고리즘]
1. Logistic Regression: Probability-based (Sigmoid)
2. Decision Tree: Rule-based branching (If-Then)
3. SVM: Maximum Margin Hyperplane
4. Random Forest/Boosting: Ensemble of weak learners
```
- **평가 지표:** 혼동 행렬(Confusion Matrix) 기반의 Precision, Recall, AUC-ROC.

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 전처리, 모델 가정, 평가 지표, 해석 가능성을 함께 검토해야 한다.

동작 순서:
| 비교 항목 (Criteria) | 로지스틱 회귀 (Logistic) | 결정 트리 (Tree) | 서포트 벡터 머신 (SVM) |
| :--- | :--- | :--- | :--- |
| **모델 구조** | 선형 결합 (Linear) | 계층적 분기 (Hierarchy) | 마진 최대화 (Margin) |
| **장점 (Pros)** | 결과 해석 용이 | 데이터 전처리 불필요 | 복잡한 데이터 처리 강점 |
| **단점 (Cons)** | 선형 관계만 해석 가능 | 과적합(Overfitting) 취약 | 학습 시간 및 자원 소모 |
| **비유 (Analogy)** | 찬성/반대 확률 투표 | 스무고개 질문 | 안전 지대 확보하기 |
| **비고 (Note)** | 분류의 베이스라인 | 앙상블의 기본 단위 | 비선형 커널 트릭 활용 |

---

## 4. 비교 및 연결

- **데이터 불균형(Imbalance) 처리:** 실제 현업 데이터는 대개 편향되어 있으므로 **SMOTE**나 **Oversampling** 기법을 적용하여 모델이 소수 클래스를 학습하지 못하는 '정확도의 함정'을 피해야 함.
- **앙상블(Ensemble) 전략:** 단일 모델보다는 **XGBoost**나 **LightGBM** 같은 부스팅 모델을 사용하는 것이 실질적인 성능(Score) 확보에 유리함.
- **설명 가능성(XAI):** 딥러닝 기반 분류 시 판단 근거를 알기 어려우므로, **SHAP**이나 **LIME** 기표를 통해 변수 중요도를 역추적하는 것이 기술사적 필수 소양임.

---

## 5. 실무 적용 및 판단

- **자동화 의사결정:** 인간의 수동 판단 영역을 기계가 대체하여 비용 절감과 정밀도 향상을 달성함.
- **실시간 탐지:** 스트리밍 데이터와 결합하여 초단위로 발생하는 이상 결제나 공격 시도를 즉각 차단할 수 있음.
- **표준화된 평가:** 정량적인 평가 지표(F1, AUC)의 확립은 데이터 사이언스 프로젝트의 성공 여부를 판단하는 글로벌 표준이 됨.

---

## 6. 기대효과 및 결론

분류 (Classification) 분석은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 분석 기법의 실무 가치는 모델의 화려함보다 데이터 가정과 해석 책임을 얼마나 지키느냐에서 나온다.

---

## 7. 발전 흐름도

```text
[Supervised Learning (지도 학습)]
    │
    ▼
[Ensemble (앙상블)]
    │
    ▼
[Neural Networks (신경망)]
    │
    ▼
[Confusion Matrix (혼동 행렬)]
    │
    ▼
[SMOTE (불균형 처리)]
```

이 흐름도는 Supervised Learning (지도 학습)에서 출발해 SMOTE (불균형 처리)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

- **상위 개념:** Supervised Learning, Machine Learning
- **하위 개념:** Ensemble, Neural Networks, Softmax
- **연관 기술:** Confusion Matrix, SMOTE, Hyperparameter Tuning, XAI
