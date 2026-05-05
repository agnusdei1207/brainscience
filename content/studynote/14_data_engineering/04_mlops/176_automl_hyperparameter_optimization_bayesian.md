+++
weight = 176
title = "176. AutoML (Automated Machine Learning) 하이퍼파라미터 최적화 베이지안 탐색"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++
## 0. 핵심 인사이트

> **핵심**: AutoML (Automated Machine Learning)은 피처 엔지니어링·모델 선택·하이퍼파라미터 최적화를 자동화하여 ML 전문가가 아닌 도메인 전문가도 고품질 모델을 개발할 수 있게 한다.
> 2. **가치**: 베이지안 최적화(Bayesian Optimization)는 대리 모델(Surrogate Model)로 탐색 공간을 효율적으로 좁혀, Grid Search 대비 10~100배 적은 실험으로 최적 하이퍼파라미터를 발견한다.
> 3. **판단 포인트**: Hyperband의 조기 종료(Early Stopping)는 샘플 수보다 자원 효율이 중요할 때, 베이지안 최적화는 실험 비용이 높고 샘플 효율이 중요할 때 선택해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 1.1 하이퍼파라미터 최적화의 문제

```
딥러닝 하이퍼파라미터 공간 예시:
  ┌────────────────────────────────────────────┐
  │  학습률 (lr): [1e-5, 1e-1] (로그 스케일)   │
  │  배치 크기: {32, 64, 128, 256, 512}        │
  │  레이어 수: {2, 4, 6, 8, 12}               │
  │  드롭아웃: [0, 0.5]                         │
  │  가중치 감쇠: [1e-5, 1e-1]                  │
  │  활성화 함수: {relu, gelu, selu, tanh}     │
  │  옵티마이저: {Adam, AdamW, SGD, Ranger}    │
  │                                            │
  │  조합 수: 거의 무한대                        │
  │  각 실험 비용: GPU 수시간~수일             │
  │  → 브루트포스 탐색 불가능!                  │
  └────────────────────────────────────────────┘
```

### 1.2 AutoML 전체 파이프라인

| 단계 | 자동화 내용 | 주요 방법 |
|:---|:---|:---|
| **데이터 전처리** | 결측치, 인코딩, 스케일링 | 휴리스틱 규칙, 학습된 변환 |
| **피처 엔지니어링** | 다항식 피처, 상호작용, 선택 | 진화 알고리즘, 강화학습 |
| **모델 선택 (Model Selection)** | 최적 알고리즘 선택 | 메타학습, 포트폴리오 |
| **HPO (Hyperparameter Optimization)** | 하이퍼파라미터 최적화 | 베이지안, Hyperband |
| **NAS (Neural Architecture Search)** | 신경망 구조 탐색 | 강화학습, 진화, 경사하강 |
| **앙상블** | 모델 조합 | 스태킹, 보팅 |

📢 **섹션 요약 비유**: AutoML은 AI 모델 개발의 자동 튜닝 피트 스톱과 같다. 레이서(데이터 과학자)가 핸들을 잡는 동안, 피트 크루(AutoML)가 자동으로 최적 타이어(하이퍼파라미터)를 선택한다.

---

## 2. 구성요소

### 2.1 Grid Search vs Random Search

```
┌─────────────────────────────────────────────────────────┐
│        Grid Search vs Random Search 비교                 │
│                                                          │
│  Grid Search:          Random Search:                    │
│  ┌────────────┐        ┌────────────┐                   │
│  │ × × × × × │        │  ·    ·    │                   │
│  │ × × × × × │        │     ·   ·  │                   │
│  │ × × × × × │        │  ·    ·    │                   │
│  │ × × × × × │        │     ·   ·  │                   │
│  │ × × × × × │        │  ·    ·  · │                   │
│  └────────────┘        └────────────┘                   │
│  25개 실험              10개 실험                         │
│  (불필요한 조합 포함)   (중요 영역 커버 가능)              │
│                                                          │
│  Bergstra & Bengio (2012):                               │
│  "대부분 HPO에서 Random Search가 Grid보다 효율적"        │
│  (많은 HP가 실제로 무관함 → 차원의 저주)                 │
└─────────────────────────────────────────────────────────┘
```

### 2.2 베이지안 최적화 (Bayesian Optimization)

```
┌─────────────────────────────────────────────────────────────┐
│           베이지안 최적화 작동 원리                            │
│                                                              │
│  목표: f(x) = 모델 성능(x = 하이퍼파라미터)을 최대화          │
│  제약: f(x) 평가 비용이 매우 높음 (한 번 실험 = 수시간)       │
│                                                              │
│  반복 알고리즘:                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │  1. 초기 N개 랜덤 실험으로 관측 데이터 D 수집       │     │
│  │                                                    │     │
│  │  2. 대리 모델(Surrogate Model) 학습:                │     │
│  │     - 가우시안 프로세스 (Gaussian Process)          │     │
│  │     - TPE (Tree-structured Parzen Estimator)       │     │
│  │     - 랜덤 포레스트 (SMAC)                          │     │
│  │     → f(x)의 사후 분포 P(y|x, D) 추정              │     │
│  │                                                    │     │
│  │  3. 획득 함수(Acquisition Function)으로 다음 점 선택│     │
│  │     - EI (Expected Improvement): E[max(f(x)-f*,0)]│     │
│  │     - UCB (Upper Confidence Bound): μ + κσ        │     │
│  │     - PI (Probability of Improvement)              │     │
│  │                                                    │     │
│  │  4. f(x_next) 실제 평가                             │     │
│  │  5. D에 추가, 2로 돌아가기                           │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

#### 가우시안 프로세스 시각화

```
성능                                            
  ↑                                            
1.0│        ┌─┐ GP 예측 (불확실성 포함)          
  │       /█│█\  μ(x) ± 2σ(x)                 
0.8│      / █│█ \                               
  │●    /  █│█  \   ●                          
0.6│   /   █│█   \ /                            
  │  /    █│█    ●                             
0.4│ ●    █│█                                  
  │      █│█                                   
0.2│     █│█                                   
  └────────────────────────────────→ 하이퍼파라미터
  ●: 관측된 실험점   █: 탐색 우선 영역 (높은 불확실성 or 기대값)
```

### 2.3 Hyperband 알고리즘

Hyperband는 랜덤 서치 + 조기 종료(Early Stopping)를 결합하여 자원 효율을 극대화한다.

```
┌─────────────────────────────────────────────────────────────┐
│               Hyperband 스케줄 예시                           │
│                                                              │
│  총 자원 예산: R = 81 epoch                                   │
│  다운샘플링 비율: η = 3                                       │
│                                                              │
│  Bracket 0 (가장 공격적 제거):                                │
│  라운드  1: 81개 설정 × 1 epoch   → 상위 27개 선택           │
│  라운드  2: 27개 설정 × 3 epoch   → 상위 9개 선택            │
│  라운드  3:  9개 설정 × 9 epoch   → 상위 3개 선택            │
│  라운드  4:  3개 설정 × 27 epoch  → 상위 1개 선택            │
│  라운드  5:  1개 설정 × 81 epoch  → 최종 승자                │
│                                                              │
│  Bracket 1 (중간 제거):                                      │
│  라운드  1: 34개 설정 × 3 epoch   → 상위 11개               │
│  ...                                                         │
│                                                              │
│  핵심: 초기에 저성능 설정을 빠르게 제거하여 자원 절약         │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 BOHB (Bayesian Optimization + Hyperband)

```
BOHB = 베이지안 최적화 + Hyperband 조기 종료 결합:

  Hyperband의 자원 효율 +
  베이지안 최적화의 샘플 효율
  ↓
  각 브래킷에서 최저 자원 레벨에서는 무작위 샘플링,
  상위 자원 레벨에서는 TPE 베이지안 최적화 적용
```

📢 **섹션 요약 비유**: Hyperband는 100명의 마라톤 선수 중 5km 지점에서 하위 67명을 탈락시키고, 10km에서 다시 하위를 탈락시켜 최고의 선수만 남기는 토너먼트 방식이다.

---

## 3. 구조 및 동작 원리

### 3.1 HPO 방법 비교

| 방법 | 탐색 효율 | 자원 효율 | 구현 복잡도 | 병렬화 | 적합 상황 |
|:---|:---|:---|:---|:---|:---|
| **Grid Search** | 낮음 | 낮음 | 단순 | 쉬움 | HP 수 2~3개, 범위 좁을 때 |
| **Random Search** | 중간 | 중간 | 단순 | 쉬움 | 빠른 탐색, 다차원 |
| **Bayesian (GP)** | 높음 | 높음 | 복잡 | 어려움 | 실험 비용 높음, 연속형 HP |
| **TPE** | 높음 | 높음 | 중간 | 가능 | 대규모 조건부 공간 |
| **Hyperband** | 중간 | 매우 높음 | 중간 | 쉬움 | 학습 곡선 평가 가능 |
| **BOHB** | 매우 높음 | 매우 높음 | 높음 | 가능 | 대규모 분산 HPO |

### 3.2 NAS (Neural Architecture Search)

```
NAS 방법 분류:
  ┌──────────────────────────────────────────────┐
  │  탐색 공간 (Search Space):                    │
  │  - 셀 구조 (Cell-based): 반복 블록 설계        │
  │  - 전체 네트워크: 레이어 수/크기 탐색          │
  │                                              │
  │  탐색 전략 (Search Strategy):                 │
  │  - 강화학습 (NASNet, 구글 2017): RL 에이전트  │
  │  - 진화 알고리즘 (AmoebaNet)                  │
  │  - 경사하강 (DARTS): 연속 완화로 미분 가능    │
  │  - 원샷 NAS (ENAS, SNAS): 슈퍼넷 공유         │
  │                                              │
  │  비용:                                        │
  │  NASNet: GPU 1,800일 (구글 TPU 수십 개)       │
  │  DARTS: GPU 4일                               │
  │  EfficientNet: NAS + 복합 스케일링            │
  └──────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: NAS는 레고 블록(레이어)으로 최적의 성을 설계하는 로봇이다. 수천 가지 배치를 시험해보고 가장 효율적인 구조를 자동으로 발견한다.

---

## 4. 비교 및 트레이드오프

### 4.1 주요 AutoML 도구 비교

| 도구 | 개발사 | 강점 | 약점 |
|:---|:---|:---|:---|
| **Optuna** | Preferred Networks | 경량, TPE, Hyperband, 시각화 | 분산 확장 제한 |
| **Ray Tune** | Anyscale | 대규모 분산, 다양한 스케줄러 | 설정 복잡 |
| **Hyperopt** | MontrealAI | TPE 원조, 심플 | 활성 개발 중단 |
| **AutoKeras** | Google Brain | 케라스 통합, NAS 내장 | 딥러닝 전용 |
| **H2O AutoML** | H2O.ai | 표형 데이터 최적화, 앙상블 | 딥러닝 제한 |
| **AutoGluon** | AWS | 빠른 기준선, 앙상블 | 커스터마이징 어려움 |
| **FLAML** | Microsoft | 비용 효율 최적화 | 상대적으로 신생 |

### 4.2 Optuna 구현 예시

```python
import optuna
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score

def objective(trial):
    # 하이퍼파라미터 탐색 공간 정의
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'max_depth': trial.suggest_int('max_depth', 2, 10),
        'learning_rate': trial.suggest_float('learning_rate', 1e-4, 1.0, log=True),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 20),
    }
    
    model = GradientBoostingClassifier(**params, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
    return scores.mean()

# TPE 샘플러 + Hyperband 조기 종료
sampler = optuna.samplers.TPESampler(seed=42)
pruner = optuna.pruners.HyperbandPruner()

study = optuna.create_study(
    direction='maximize',
    sampler=sampler,
    pruner=pruner
)
study.optimize(objective, n_trials=200, n_jobs=4)  # 병렬 4 workers

print(f"최적 AUC: {study.best_value:.4f}")
print(f"최적 파라미터: {study.best_params}")

# 중요도 분석
importance = optuna.importance.get_param_importances(study)
```

### 4.3 분산 HPO 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│        Ray Tune 분산 HPO 아키텍처                            │
│                                                              │
│  드라이버 (Head Node)                                        │
│  ┌──────────────────────────────────────────────┐          │
│  │  Tune Controller                              │          │
│  │  - 탐색 알고리즘 (ASHA / BOHB / PBT)         │          │
│  │  - 트라이얼 스케줄링                           │          │
│  │  - 결과 집계 및 중간 보고                      │          │
│  └────────────────────────┬─────────────────────┘          │
│                           │                                  │
│  ┌──────────┬─────────────┼────────────┬──────────┐        │
│  │Worker 0  │ Worker 1    │ Worker 2   │ Worker 3 │        │
│  │Trial #1  │ Trial #2    │ Trial #3   │ Trial #4 │        │
│  │GPU:0     │ GPU:1       │ GPU:2      │ GPU:3    │        │
│  └──────────┴─────────────┴────────────┴──────────┘        │
│                                                              │
│  ASHA (Asynchronous Successive Halving Algorithm):           │
│  완료된 트라이얼 즉시 평가 → 비동기 조기 종료               │
└─────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 분산 HPO는 여러 팀이 동시에 다른 레시피로 요리를 만들고, 중간에 맛이 없는 팀은 탈락시켜(조기 종료) 자원을 아끼는 병렬 요리 대회다.

---

## 5. 실무 적용 및 최적화 기법

### 5.1 AutoML 도입 효과

| 항목 | 수동 튜닝 | AutoML (베이지안+Hyperband) |
|:---|:---|:---|
| **탐색 실험 수** | 전문가 경험 의존 | 체계적 10~100× 효율화 |
| **최적화 품질** | 전문가 수준 | 동등하거나 능가 |
| **소요 시간** | 주 단위 | 시간~일 단위 |
| **재현성** | 낮음 | 높음 (시드 고정) |
| **전문가 의존도** | 높음 | 낮음 |

### 5.2 기술사 답안 핵심 논점

1. **베이지안 최적화 핵심**: 대리 모델(GP/TPE)이 불확실성을 추정하고, 획득 함수(EI/UCB)가 탐색-활용 균형을 자동 조정
2. **Hyperband의 장점**: 조기 종료로 저성능 설정에 자원 낭비 방지, Random Search의 탐색 다양성 유지
3. **BOHB 조합**: 베이지안의 샘플 효율 + Hyperband의 자원 효율 = 실무 최선택
4. **NAS 트렌드**: DARTS(미분 가능) > RL 기반(비용 과다), EfficientNet 계열이 NAS의 실용적 결과물

📢 **섹션 요약 비유**: AutoML은 AI 개발의 자동 네비게이션이다. 목적지(최적 성능)까지 수동으로 길을 찾는 대신(수동 튜닝), 경험 지도(베이지안 대리 모델)를 만들고 막힌 길은 과감히 우회(조기 종료)하여 최단 경로를 자동으로 찾는다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 기반 이론 | 베이지안 최적화 | 사후 분포 업데이트 기반 탐색 |
| 대리 모델 | 가우시안 프로세스 | 불확실성 정량화 가능한 회귀 |
| 대리 모델 | TPE | Parzen 추정기 기반, 조건부 공간 강점 |
| 획득 함수 | Expected Improvement | 현재 최고보다 개선 기대치 최대화 |
| 자원 효율 | Hyperband | 조기 종료 기반 자원 최적 배분 |
| 통합 | BOHB | 베이지안 + Hyperband 결합 |
| 구조 탐색 | NAS | 신경망 아키텍처 자동 탐색 |
| 도구 | Optuna | 경량 Python HPO 프레임워크 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. AutoML은 AI 모델의 자동 조리법 찾기야 — 어떤 재료(피처)를 얼마나(하이퍼파라미터) 넣어야 가장 맛있는지 AI가 스스로 실험해서 알아내!

### 📈 관련 키워드 및 발전 흐름도

```text
수동 하이퍼파라미터 튜닝 (Grid Search · Random Search)
    │
    ▼
베이지안 최적화 (Bayesian Optimization)
    ├─► Surrogate Model (GP · TPE)
    └─► 탐색-활용 균형 (Acquisition Function)
    │
    ▼
AutoML 플랫폼
    ├─► NAS (Neural Architecture Search): 모델 구조 자동 탐색
    ├─► AutoFeature: 피처 자동 생성 · 선택
    └─► Google AutoML · H2O · Auto-sklearn
    │
    ▼
LLM 기반 AutoML: 자연어로 ML 파이프라인 생성
```
2. 베이지안 최적화는 요리 대회에서 지금까지의 실험 결과를 기억하고, "이 조합이 맛있을 것 같다!"는 방향으로 점점 좁혀가는 영리한 탐정 방식이야.
3. Hyperband는 100개 레시피 중 맛없는 건 중간에 탈락시키는 빠른 선발전 — 자원을 아끼면서 최고의 레시피를 찾아내는 거야!
