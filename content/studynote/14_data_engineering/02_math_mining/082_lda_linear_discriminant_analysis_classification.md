+++
weight = 82
title = "82. 선형 판별 분석 (LDA: Linear Discriminant Analysis)"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: 선형 판별 분석(LDA)은 PCA와 같은 차원 축소 기법이지만, 정답 라벨(Y)을 활용하여 "클래스(집단)를 가장 잘 구별할 수 있는 축"을 찾아내는 **지도 학습(Supervised Learning)** 기반의 차원 축소 및 분류(Classification) 알고리즘이다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

빅데이터 분류 문제에서 변수의 수가 너무 많아지면 모델이 학습 방향을 잃어버리는 '차원의 저주'가 발생합니다. 앞서 다룬 PCA(주성분 분석)는 데이터 전체의 퍼짐(분산)만을 고려하기 때문에, 정작 "사과와 바나나를 구별하는 데 핵심적인 정보"는 지워버리고 쓸데없는 분산을 남길 위험이 존재합니다. 이러한 비지도 학습의 한계를 극복하기 위해 제안된 것이 바로 **LDA(Linear Discriminant Analysis)**입니다. LDA는 데이터가 속한 범주(Class) 정보를 적극적으로 활용하여, 집단 간의 차이를 가장 극명하게 보여주는 선형 축을 찾아 투영시킵니다. 즉, 차원 축소와 분류 모델링을 동시에 수행할 수 있는 스마트한 알고리즘입니다.

---

## 2. 구성요소

LDA의 최적화 메커니즘은 두 가지 분산 행렬(Scatter Matrix)을 정의하고 이들의 비율(Ratio)을 최대화하는 고유값(Eigenvalue) 문제를 푸는 것입니다.
1. **$S_B$ (Between-class Scatter Matrix)**: 서로 다른 클래스 중심(Mean)들 간의 거리. (이 값은 클수록 좋다)
2. **$S_W$ (Within-class Scatter Matrix)**: 동일 클래스 내에서 데이터들이 뭉쳐있는 정도. (이 값은 작을수록 좋다)
3. **목적 함수**: $J(W) = \frac{W^T S_B W}{W^T S_W W}$ 를 최대화하는 투영 행렬 $W$를 구합니다.

```text
+---------------------------------------------------------------+
|         LDA (Linear Discriminant Analysis) Mechanism          |
+---------------------------------------------------------------+
|  [Bad Projection (Like PCA)]    [Good Projection (LDA)]       |
|                                                               |
|        Class A      Class B        Class A          Class B   |
|         ooo          xxx             ooo              xxx     |
|          ooo        xxx               ooo            xxx      |
|           ooo      xxx                 ooo          xxx       |
|                                                               |
|  --+---------+---------+-->    --+----------+----------+-->   |
|   Mixed Projection Axis        Discriminant Axis (LDA)        |
|  (Hard to separate A & B)      (A & B are clearly separated)  |
|                                                               |
| [Mathematical Pipeline]                                       |
|  1. Compute d-dimensional mean vectors for different classes. |
|  2. Compute Within-class Scatter Matrix (S_W).                |
|  3. Compute Between-class Scatter Matrix (S_B).               |
|  4. Compute Eigenvectors & Eigenvalues for (S_W^-1 * S_B).    |
|  5. Sort Eigenvectors by decreasing Eigenvalues.              |
|  6. Choose Top-K Eigenvectors to form transformation matrix W.|
|  7. Project samples onto the new subspace: Y = X * W          |
+---------------------------------------------------------------+
```

---

## 3. 구조 및 원리

**핵심 조건**: 선형 판별 분석 (LDA: Linear Discriminant Analysis)은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 비교 항목 | PCA (주성분 분석) | LDA (선형 판별 분석) |
| :--- | :--- | :--- |
| **목적** | 데이터의 **분산 최대화** (정보량 보존) | 클래스 간 **분리도 최대화** (분류 성능 극대화) |
| **학습 방법** | **비지도 학습** (Unsupervised) | **지도 학습** (Supervised) |
| **라벨(Y) 유무** | 필요 없음 (X 변수들만 사용) | **반드시 필요함** (클래스 소속 정보 필수) |
| **축소 가능한 최대 차원** | 변수의 개수 (D) | **클래스 개수 - 1** (C - 1) |
| **취약점** | 클래스 구분에 중요한 정보가 손실될 수 있음 | 정규분포 가정을 위배하거나, $S_W$ 행렬의 역행렬을 구할 수 없는 경우(소규모 데이터) 취약함 |

동작 순서:
1. **입력 정의**: 해당 주제가 다루는 데이터·요청·상태를 명확히 식별한다. 입력 경계가 불분명하면 품질 검증과 책임 분리가 무너진다.
2. **처리 규칙 적용**: 저장 구조, 연산 로직, 분산 처리, 학습 규칙 중 핵심 메커니즘을 실행한다. 이 단계가 성능·확장성·정확도를 결정한다.
3. **결과 검증**: 정합성, 지연, 비용, 품질 지표를 확인해 운영 가능한 상태인지 판단한다. 이 검증이 없으면 실험은 가능해도 서비스화는 어렵다.
4. **운영 피드백 반영**: 드리프트, 부하 변화, 장애, 스키마 변화에 대응해 구조를 다시 조정한다. 실무에서는 이 폐쇄 루프가 기술의 지속성을 만든다.

```text
[입력/이벤트]
      ↓
[저장·정제·변환]
      ↓
[핵심 연산/학습/질의]
      ↓
[검증·배포·활용]
      ↓
[모니터링·재조정]
```

---

## 4. 비교 및 연결

현업 머신러닝 파이프라인에서 분류(Classification) 과제를 수행할 때, LDA는 단순한 차원 축소를 넘어 분류기(Classifier) 자체로도 훌륭한 성능을 발휘합니다.
1. **차원 제약 조건의 인식**: LDA가 생성할 수 있는 새로운 축(차원)의 최대 개수는 `(클래스 개수 - 1)`입니다. 즉, 개와 고양이를 분류하는 2진 분류(Binary Classification) 문제에서는 수백 개의 변수가 단 **1개**의 차원(1D 축)으로 극단적으로 압축됩니다. 이는 강력한 압축률을 자랑하지만, 복잡한 비선형 데이터 구조를 담아내기에는 한계가 있음을 인지해야 합니다.
2. **다중 공선성과 PCA와의 융합**: 데이터 변수들 간에 다중 공선성(Multicollinearity)이 너무 심하면 LDA 내부에서 역행렬 연산 시 오류(Singular Matrix)가 발생할 수 있습니다. 기술사적 최적화 전략으로는 **먼저 PCA를 적용하여 다중 공선성을 제거한 뒤, 그 결과물에 LDA를 적용하는 하이브리드 파이프라인(PCA -> LDA)**을 구축하여 수학적 안정성과 분류 성능을 동시에 취하는 방식을 권장합니다.

---

## 5. 실무 적용 및 판단

LDA는 통계학과 패턴 인식 분야에서 가장 역사 깊고 견고한 선형 판별 알고리즘입니다. 딥러닝(Deep Learning) 시대가 도래하면서 신경망 자체가 은닉층(Hidden Layer)을 통해 더 강력한 비선형 차원 축소와 판별을 수행하게 되었지만, 데이터의 양이 적거나 완벽한 화이트박스(White-box) 모델 해석력이 요구되는 의료 진단, 금융 신용 평가 도메인에서는 여전히 LDA가 기준선(Baseline) 모델로 강력하게 군림하고 있습니다. LDA의 "클래스 내부는 뭉치고, 클래스 간은 멀게 한다"는 우아한 수학적 철학은 현대의 대조 학습(Contrastive Learning)이나 샴 네트워크(Siamese Network)의 손실 함수(Loss Function) 설계 철학으로 고스란히 계승되어 그 명맥을 이어가고 있습니다.

---

## 6. 기대효과 및 결론

LDA는 통계학과 패턴 인식 분야에서 가장 역사 깊고 견고한 선형 판별 알고리즘입니다.

선형 판별 분석 (LDA: Linear Discriminant Analysis)의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
피셔 판별 분석 (Fisher's LDA, 1936)
    │
    ▼
LDA: 클래스 간 분산 최대화 + 클래스 내 분산 최소화
    │
    ├─► 차원 축소: 최대 (C-1)개 축으로 압축
    └─► 분류기: 가우시안 사후 확률로 직접 분류
    │
    ▼
PCA → LDA 하이브리드 파이프라인 (실무 표준)
    │
    ▼
비선형 확장
    ├─► QDA (이차 판별 분석) — 클래스별 공분산 허용
    ├─► Kernel LDA — 커널 트릭 적용
    └─► 대조 학습 (Contrastive Learning) — LDA 철학의 딥러닝 계승
```

---

## 8. 관련 개념 맵

* **상위 개념**: 지도 학습(Supervised Learning), 차원 축소(Dimensionality Reduction)
* **핵심 수학**: 분산 행렬(Scatter Matrix), 고유값 분해(Eigen Decomposition)
* **비교/응용 기법**: PCA(주성분 분석), QDA(이차 판별 분석), 대조 학습(Contrastive Learning)
