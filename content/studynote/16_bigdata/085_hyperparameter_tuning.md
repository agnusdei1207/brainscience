+++
title = "85. 하이퍼파라미터 튜닝 (Hyperparameter Tuning)"
description = "하이퍼파라미터 튜닝의 개념, Grid Search, Random Search, Bayesian Optimization 등 다양한 기법"
date = "2026-04-05"
[taxonomies]
tags = ["하이퍼파라미터", "Hyperparameter", "GridSearch", "RandomSearch", "Bayesian", "AutoML"]
categories = ["studynote-bigdata"]
+++

# 하이퍼파라미터 튜닝 (Hyperparameter Tuning)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 하이퍼파라미터 튜닝은 모델의 학습 가능한 파라미터(가중치 등)가 아닌, 모델의 구조나 학습 과정을 제어하는 하이퍼파라미터를 최적의 값으로 조정하는 과정이다.
> 2. **가치**: 적절한 하이퍼파라미터는 모델 성능을 극적으로 향상시키며, 반대로 부적절한 하이퍼파라미터는 과소적합이나 과적합을 유발할 수 있다.
> 3. **융합**: Grid Search, Random Search, Bayesian Optimization, Hyperband, Early Stopping 등 다양한 방법론이 있으며, 문제 규모와 특성에 따라 적합한 방법을 선택해야 한다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

하이퍼파라미터(Hyperparameter)는 모델이 데이터를 학습하기 전에 미리 설정해야 하는 매개변수이다. 이는 모델이 학습하는 파라미터(예: 선형 회귀의 계수, 신경망의 가중치)와 달리, 모델의 구조나 학습 과정을 제어한다.

예를 들어, Random Forest에서"나무의 개수(n_estimators)"나"나무의 최대 깊이(max_depth)"는 하이퍼파라미터이다. 이러한 값들은 모델이 데이터에서 학습하는 것이 아니라, 연구자나 엔지니어가 미리 설정해야 한다.

하이퍼파라미터 튜닝이 필요한 이유는 하이퍼파라미터 값에 따라 모델 성능이 크게 달라지기 때문이다.

```text
[하이퍼파라미터가 성능에 미치는 영향]

Random Forest의 n_estimators (나무 개수) vs 성능:

n_estimators = 1:  정확도 0.72  ← 과소적합
n_estimators = 10: 정확도 0.81
n_estimators = 50: 정확도 0.86
n_estimators = 100: 정확도 0.88  ← 대체로 적합
n_estimators = 200: 정확도 0.89
n_estimators = 500: 정확도 0.89
n_estimators = 1000: 정확도 0.89  ← 추가 향상 거의 없음 (시간만 증가)

==> 적절한 n_estimators 선택이 성능과 효율성의 균형점 결정

[하이퍼파라미터 예시]

모델              주요 하이퍼파라미터
─────────────────────────────────────────────────────
Random Forest   n_estimators, max_depth, min_samples_split
XGBoost/LGBM    learning_rate, n_estimators, max_depth, subsample
SVM             C (Regularization), kernel, gamma
Neural Network  learning_rate, batch_size, epochs, hidden_layers
로지스틱 회귀    C (Regularization strength), penalty
```

> 📢 **섹션 요약 비유**: 하이퍼파라미터 튜닝은犹如항공기의 조종사 설정과 유사하다. 조종사(하이퍼파라미터)는 엔진의 출력(학습률), 상승률(에포크 수) 등을 사전에 설정해야 한다. 너무 낮게 설정하면 목적지에 도달하지 못하고(과소적합), 너무 높게 설정하면 제어를 잃고 추락할 수 있다(과적합). 적절한 설정이 성공적인 비행을 위해 필수적이다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 2.1 Grid Search (격자 탐색)

하이퍼파라미터 후보 값들의 가능한 모든 조합을 탐색한다.

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10]
}

# 전체 조합: 3 × 4 × 3 = 36개
grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
```

```text
[Grid Search 시각화]

max_depth
    │
 15 │  ○  ○  ○  ★
    │  ○  ○  ○
 10 │  ○  ○  ○
    │  ○  ○  ○
  5 │  ○  ○  ○
    └──────────────
       50  100 200
       n_estimators

★ = 최고 성능 점 (grid_search.best_params_)
○ = 시도된 조합

단점:
- 차원이 증가하면 조합 수가 기하급수적으로 증가 (차원 저주)
- 연속적인 최적점을 건너뛸 수 있음
```

### 2.2 Random Search (무작위 탐색)

하이퍼파라미터 공간에서 무작위로 조합을 샘플링한다.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_dist = {
    'n_estimators': randint(50, 500),
    'max_depth': randint(3, 20),
    'min_samples_split': randint(2, 20),
    'learning_rate': uniform(0.01, 0.3)  # 0.01 ~ 0.31
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(),
    param_dist,
    n_iter=100,  # 100개 조합만 무작위 샘플링
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)

random_search.fit(X_train, y_train)
```

```text
[Random Search의 이론적 근거]

Bergstra & Bengio (2012)의 研究에 따르면:
- Random Search는 고차원 공간에서 Grid Search보다 효율적
- 대부분의 하이퍼파라미터는 "중요한" 파라미터 2~3개에 불과
- Random Search는 자동으로 중요 파라미터의 더 넓은 범위를 탐색

[Grid vs Random Search]

Grid Search (9개 조합):
  max_depth: [3, 5, 10]
  learning_rate: [0.01, 0.1, 1.0]

  --> 9개의固定된 점만 탐색

Random Search (9개 조합):
  --> 9개의임의의 점, 더 넓은 범위 탐색 가능

  ┌─────────────────────┐
  │    ·      ★        │  ★ = 실제 최적점
  │  ·    ·      ·     │  · = Random Search 점
  │       ·    ·       │
  │    ·         ·    │
  │         ·         │
  └─────────────────────┘
```

### 2.3 Bayesian Optimization

이전 탐색 결과를 활용하여 다음 탐색할 지점을 체계적으로 선택한다.

```python
# scikit-optimize (skopt) 사용 예시
from skopt import BayesSearchCV
from sklearn.ensemble import GradientBoostingClassifier

search_space = {
    'n_estimators': (50, 500),
    'max_depth': (3, 15),
    'learning_rate': (0.01, 0.3, 'log-uniform')
}

bayes_search = BayesSearchCV(
    GradientBoostingClassifier(),
    search_space,
    n_iter=50,  # 50번의 순차적 탐색
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)

bayes_search.fit(X_train, y_train)
```

```text
[Bayesian Optimization 동작原理]

1. 초기 점 몇 개를 무작위로 평가

2. 대체 모델 (Surrogate Model, 예: Gaussian Process)로
   하이퍼파라미터 공간에서의 성능 곡면을 모델링

3. 획득 함수 (Acquisition Function)를 통해
   다음 탐색할 지점을 결정
   - Expected Improvement (EI): 현재 최선 대비 개선 기대값
   - Upper Confidence Bound (UCB): 탐험 vs 이용 균형

4. 선택된 지점에서 모델을 평가

5. 2-4 반복

[장점/단점]
✓ 효율적: 최소한의 평가로 최적점에 가까갈 수 있음
✓ 연속적 공간 탐색에 적합
✗ 순차적: 병렬화 어려움 (그러나 asynchronous 가능)
✗ 고차원에서 성능 저하 가능성
✗ 구현 복잡도 ↑
```

> 📢 **섹션 요약 비유**: Bayesian Optimization은犹如経験丰富的猎人と類似している. 처음에는全局를胡乱に撃つ(Random Search) 하지만, 총을 쏘고 결과를 확인하면서"이 지역에 주로물이 있을 것 같다"(Surrogate Model)를 学习한다. 그리고 이를 바탕으로 다음에 쏠 방향을 더 지능적으로 결정한다. 점점 목표에 가까워지는 것이다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

주요 하이퍼파라미터 튜닝 기법들을 비교해보자.

| 기법 | 장점 | 단점 | 적합한 상황 |
|:---|:---|:---|:---|
| **Grid Search** |系統적, 全域 탐색, 구현 간단 | 차원 저주, 비효율적 | 낮은 차원 (1~3개 파라미터) |
| **Random Search** | 고차원에 효율적, 구현 간단 | 랜덤성, reproducibility 낮음 | 4개 이상 파라미터 |
| **Bayesian Optimization** | 효율적, 연속적 공간 탐색 | 순차적, 구현 복잡 | 2~10개 파라미터, 시간 제약 |
| **Hyperband** | 조기 중지 활용, 효율적 | 리소스 제한적 | 대규모 신경망, 시간 제약 |
| **Early Stopping** | 불필요한 훈련 중지 | 다른 HP 튜닝과 결합 필요 | 딥러닝 |

```text
[하이퍼파라미터 공간 크기에 따른 方法選択]

파라미터 수: 1~2개 (저차원)
  → Grid Search: 모든 조합 탐색, 효율적

파라미터 수: 3~5개 (중간 차원)
  → Random Search 또는 Bayesian Optimization
  → Bayesian이 더 효율적이나 구현 복잡

파라미터 수: 6개 이상 (고차원)
  → Random Search (Bayesian은 한계)
  → 또는 파라미터를 그룹으로 나누어 순차 탐색

[AutoML과의 관계]
  - Hyperopt, Optuna, Ray Tune 등 AutoML 라이브러리
  - 위 방법론들을 자동화하고 통합
  - 예: Optuna는 TPE (Tree-structured Parzen Estimator) 사용
    - Bayesian Optimization의 개선된 버전
```

> 📢 **섹션 요약 비유**: 하이퍼파라미터 튜닝 기법 선택은犹如路程导航と類似している. 짧은 거리(저차원)는 지도에的全部를 확인해도 되지만(Grid), 먼 거리(고차원)에서는 적당한 길( Random 또는 Bayesian)을 利用하는 것이 효율적이다. 또한 길이 막히면 우회로를 찾는데(Hyperband/Early Stopping), 이것은 GPS 내비게이션( AutoML)이 자동으로 처리해준다.

---

### Ⅳ. 실무 적용 및 한계 (Application & Limitation)

**실무 적용:**

1. **Nested Cross Validation**
   - 하이퍼파라미터 튜닝과 모델 평가를 동시에 수행
   - 정보 누출 방지

```python
from sklearn.model_selection import GridSearchCV, cross_val_score

# 외부: 모델 평가용 (이 테스트 데이터로는 tune 안 함)
outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 내부: 하이퍼파라미터 튜닝용
inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

param_grid = {'C': [0.1, 1, 10]}
grid_search = GridSearchCV(SVC(), param_grid, cv=inner_cv)

# 전체 교차 검증으로 최종 성능 평가
scores = cross_val_score(grid_search, X, y, cv=outer_cv)
```

2. **Learning Rate Scheduler와 조기 중지**
   - 신경망에서 learning rate를 동적으로 조정
   -_validation loss가 더 이상 개선되지 않을 때 훈련 중지

3. **Optuna 활용**
   - Python용 자동 하이퍼파라미터 최적화 프레임워크
   - GPU 지원, 분산 최적화, pruning 지원

```python
import optuna
from sklearn.model_selection import cross_val_score

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0)
    }

    model = GradientBoostingClassifier(**params)
    scores = cross_val_score(model, X, y, cv=5)
    return scores.mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```

**한계점:**

1. **계산 비용**: 특히 대규모 신경망에서 하이퍼파라미터 튜닝에 상당한 시간과 컴퓨팅 자원이 필요하다.

2. **차원 저주**: 하이퍼파라미터가 많을수록 탐색 공간이 기하급수적으로 증가한다.

3. **전이 가능성 낮음**: 한 데이터셋에서 최적화된 하이퍼파라미터가 다른 데이터셋에서도最优이라는 보장이 없다.

4. **대규모 하이퍼파라미터**: 수십 개의 하이퍼파라미터를 가진 대규모 신경망 Architectures에서는 현재 방법론의 효과가 제한적이다.

> 📢 **섹션 요약 비유**: 하이퍼파라미터 튜닝은犹如料理의 양념 조율과 유사하다. 기본 레시피(모델)는 정해져 있지만, 간(소금) 량, 설탕 량, 간장 량(각 하이퍼파라미터)을調整해야 맛(성능)이 완성된다. 하지만 양념이 너무 많으면(고차원) 모든 조합을 시도하는 데 lifetime이 부족하고, 경험으로"大概この程度"를 꾹하는 것이 현명할 때도 있다.

---

### Ⅴ. 요약 및 전망 (Summary & Outlook)

하이퍼파라미터 튜닝은 머신러닝 모델의 성능을 끌어올리는重要な 과정이다. Grid Search, Random Search, Bayesian Optimization 등 다양한 方法이 있으며, 각각의 장단점과 적합한 상황이 다르다.

앞으로의 전망으로는, 더 효율적인 고차원 하이퍼파라미터 튜닝 방법론 개발, 메타러닝(Meta-Learning)을活用하여 이전 작업의 지식을 전이하는方法, 그리고 Neural Architecture Search (NAS)와의 통합 등이研究方向가 될 것이다. 또한 Hyperparameter Tuning의自动化와end-to-end 통합은 더욱 발전할 것으로 기대된다.

결론적으로, 하이퍼파라미터 튜닝은 ciência와 예술의 결합이다. 체계적인 방법론으로 효율을 높이되, 도메인 지식과 경험에 기반한 직관도 중요하다.

---

**References**
- Bergstra, J., & Bengio, Y. (2012). Random Search for Hyper-Parameter Optimization. Journal of Machine Learning Research, 13, 281-305.
- Snoek, J., Larochelle, H., & Adams, R. P. (2012). Practical Bayesian Optimization of Machine Learning Algorithms. NIPS.
- Li, L., et al. (2017). Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization. ICLR.
