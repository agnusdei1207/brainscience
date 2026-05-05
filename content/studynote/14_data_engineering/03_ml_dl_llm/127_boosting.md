+++
weight = 127
title = "127. Boosting (부스팅) - 순차적 오류 보정 앙상블 학습"
date = "2026-04-19"
[extra]
categories = "studynote-dataengineering"
+++
## 0. 핵심 인사이트

> **핵심**: Boosting은 **이전 모델이 틀린 샘플에 가중치를 높여 다음 모델이 집중 학습**하는 순차적 앙상블 기법이며, 약한 학습기를 순서대로 결합하여 강한 학습기를 만든다.
> 2. **가치**: Bagging이 분산을 줄이는 데 효과적이라면, Boosting은 **편향(Bias)을 줄이는 데 탁월**하여 더 정확한 모델을 만들며, XGBoost·LightGBM이 Kaggle 우승의 대부분을 차지한다.
> 3. **판단 포인트**: AdaBoost(가중치)→Gradient Boosting(잔차)→XGBoost(정규화)→LightGBM(대용량)→CatBoost(범주형)의 발전을 이해해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Boosting 동작 원리                                 │
├───────────────────────────────────────────────────────┤
│  Round 1: 모델₁ 학습 → 오분류 샘플 가중치↑          │
│  Round 2: 모델₂ 학습 (가중치 높은 샘플 집중)         │
│  Round 3: 모델₃ 학습 (이전 오류 집중 보정)           │
│  ...                                                  │
│  Round N: 모델ₙ 학습                                 │
│                                                       │
│  최종: 모든 모델의 가중 합 → 강한 학습기             │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Boosting은 **틀린 문제만 반복 연습**하는 공부법이다. 1회차에서 틀린 문제를 2회차에서 집중적으로 풀면 점수가 올라간다.

---

## 2. 구성요소

### Boosting 알고리즘 발전

| 알고리즘 | 핵심 | 특징 |
|:---|:---|:---|
| **AdaBoost** | 가중치 기반 | 최초 Boosting (1997) |
| **Gradient Boosting** | 잔차(Residual) 학습 | 경사하강법 |
| **XGBoost** | 정규화+병렬화 | **Kaggle 표준** |
| **LightGBM** | Leaf-wise 분할 | **대용량·빠름** |
| **CatBoost** | 범주형 자동 처리 | Ordered Boosting |

- **📢 섹션 요약 비유**: AdaBoost는 1세대 교사(틀린 학생에게 더 관심), XGBoost는 AI 과외(체계적·효율적), LightGBM은 대형 학원(대규모 데이터).

---

## 3. 구조 및 동작 원리

| 비교 | Bagging | Boosting |
|:---|:---|:---|
| **학습** | 병렬 (독립) | **순차 (의존)** |
| **효과** | 분산↓ | **편향↓** |
| **과적합** | 강건 | 위험 있음 |
| **대표** | Random Forest | **XGBoost** |

---

## 4. 비교 및 트레이드오프

### XGBoost vs LightGBM

| 비교 | XGBoost | LightGBM |
|:---|:---|:---|
| **분할** | Level-wise | **Leaf-wise** |
| **속도** | 빠름 | **더 빠름** |
| **메모리** | 보통 | **적음** |
| **데이터** | 중소 | **대용량** |

---

## 5. 실무 적용 및 최적화 기법

Boosting은 **정형 데이터 ML의 최강 기법**이며, XGBoost/LightGBM이 산업·경진대회에서 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **AdaBoost** | 최초 Boosting (가중치) |
| **XGBoost** | 정규화 Gradient Boosting |
| **LightGBM** | Leaf-wise, 대용량 |
| **CatBoost** | 범주형 자동 처리 |
| **GBDT** | Gradient Boosted Decision Tree |

### 📈 관련 키워드 및 발전 흐름도

```text
[AdaBoost (Freund & Schapire, 1997)]
    │
    ▼
[Gradient Boosting (Friedman, 2001)]
    │
    ▼
[XGBoost (Chen, 2014) — Kaggle 혁명]
    │
    ▼
[LightGBM (MS, 2017) / CatBoost (Yandex, 2017)]
    │
    ▼
[현재: TabNet / AutoML — 딥러닝 vs 부스팅 융합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Boosting은 **틀린 문제만 반복 연습**하는 공부법이에요.
2. 1회차에서 틀린 문제를 **2회차에서 집중적으로** 풀면 점수가 올라요.
3. XGBoost는 이 방법의 **최고 버전**이라 대회에서 항상 우승한답니다!
