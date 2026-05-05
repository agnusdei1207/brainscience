+++
weight = 171
title = "171. 설명 가능한 AI (XAI, Explainable AI) - LIME, SHAP 기여도 분석"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: XAI (Explainable AI)는 블랙박스 모델의 예측 근거를 인간이 이해할 수 있는 형태로 변환하여, AI 신뢰성과 규제 준수를 동시에 달성하는 기술이다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

XAI (Explainable AI, 설명 가능한 인공지능)는 AI/ML 모델의 예측 결과와 의사결정 과정을 인간이 이해하고 검증할 수 있도록 설명을 제공하는 기술 및 방법론의 총칭이다.

```
블랙박스 모델의 문제:
  입력 X ──→ [복잡한 신경망/앙상블] ──→ 출력 Y
              (내부 작동 불투명)
  
  "왜 이 사람의 대출이 거절됐나?" → 알 수 없음

XAI 적용 후:
  입력 X ──→ [모델] ──→ 출력 Y + 설명 E
                          "소득 낮음(-0.3), 부채 높음(-0.5)이 주요 원인"
```

---

## 2. 구성요소

| 동인 (Driver) | 세부 내용 |
|:---|:---|
| **신뢰성 (Trust)** | 의사결정자가 모델 예측을 신뢰하고 활용하기 위한 근거 제공 |
| **디버깅 (Debugging)** | 모델 편향(Bias), 데이터 누수(Leakage) 탐지 |
| **규제 준수 (Compliance)** | EU AI Act, GDPR의 설명 요구권(Right to Explanation) |
| **공정성 (Fairness)** | 차별적 피처 사용 여부 감지 |
| **도메인 검증** | 의료·금융 전문가가 모델 로직의 타당성 검증 |

---

## 3. 구조 및 원리

**핵심 조건**: 설명 가능한 AI (XAI, Explainable AI)은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 항목 | LIME | SHAP |
|:---|:---|:---|
| **이론 기반** | 국소 선형 근사 | 게임 이론 (Shapley Value) |
| **설명 범위** | 로컬(Local) 전용 | 로컬 + 전역(Global) 모두 |
| **일관성 (Consistency)** | 낮음 (샘플링 랜덤성) | 높음 (수학적 보장) |
| **공정성 공리 만족** | ✗ 불만족 | ✓ 효율성, 대칭성, 허상 공리 만족 |
| **계산 속도** | 빠름 (선형 회귀) | TreeSHAP: 빠름, KernelSHAP: 느림 |
| **해석 안정성** | 낮음 (실행마다 다를 수 있음) | 높음 |
| **이미지/텍스트 지원** | ✓ (슈퍼픽셀/토큰 섭동) | 제한적 |
| **주요 시각화** | Bar chart, 텍스트 하이라이팅 | Force plot, Beeswarm, Waterfall |

```
┌─────────────────────────────────────────────────────────────┐
│                    XAI 방법론 분류                            │
├──────────────────┬──────────────────────────────────────────┤
│  모델 고유       │  의사결정 트리, 선형 회귀, GAM             │
│  (Intrinsic)     │  → 자체가 해석 가능한 구조                 │
├──────────────────┼──────────────────────────────────────────┤
│  사후 해석       │  Feature Importance (RF, XGBoost)         │
│  전역(Global)    │  PDP (Partial Dependence Plot)            │
│                  │  ALE (Accumulated Local Effects)          │
│                  │  SHAP Global (Mean |SHAP|)                │
├──────────────────┼──────────────────────────────────────────┤
│  사후 해석       │  LIME                                      │
│  로컬(Local)     │  SHAP (개별 예측)                          │
│                  │  ANCHOR (규칙 기반 설명)                    │
│                  │  Counterfactual Explanations               │
├──────────────────┼──────────────────────────────────────────┤
│  신경망 특화     │  Grad-CAM (이미지 분류)                    │
│                  │  Attention Visualization (NLP)             │
│                  │  TCAV (개념 기반 설명)                     │
└──────────────────┴──────────────────────────────────────────┘
```

| 분야 | 설명 요구사항 | 주요 XAI 기법 |
|:---|:---|:---|
| **의료 AI (Medical AI)** | 진단 근거, 오류 시 책임 추적 | Grad-CAM, SHAP |
| **신용평가 (Credit Scoring)** | 거절 사유 고객 통보 의무 | LIME, SHAP Force Plot |
| **자율주행 (Autonomous Driving)** | 사고 시 의사결정 로그 | Attention Map, Saliency |
| **채용 AI (Hiring AI)** | 차별 방지, 공정성 감사 | SHAP, Counterfactual |
| **법원 양형 AI** | 판사 보조 근거 제시 | 의사결정 트리, LIME |

---

## 4. 비교 및 연결

```
EU AI Act (2024년 발효) 고위험 AI 의무:
  ┌────────────────────────────────────────────────────┐
  │  고위험 AI 카테고리                                  │
  │  - 의료기기, 채용 시스템, 신용평가                   │
  │  - 교육 평가, 법 집행, 이민 관리                    │
  │                                                    │
  │  의무 사항:                                         │
  │  1. 설명 가능성 문서화 (Technical Documentation)    │
  │  2. 인간 감독(Human Oversight) 메커니즘             │
  │  3. 투명성(Transparency) 고지                      │
  │  4. 정확성·견고성·사이버보안 기준 준수              │
  └────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────┐
│              XAI 통합 MLOps 파이프라인                        │
│                                                              │
│  데이터 수집 → 피처 엔지니어링 → 모델 학습                     │
│                                      │                       │
│                                      ▼                       │
│                              모델 평가                        │
│                              │        │                      │
│                              ▼        ▼                      │
│                         성능 지표   XAI 분석                  │
│                         (AUC, F1)  (SHAP, LIME)              │
│                              │        │                      │
│                              ▼        ▼                      │
│                         임계값 통과?  편향 감지?               │
│                              │        │                      │
│                              ▼        ▼                      │
│                         모델 배포   피처 제거/수정             │
│                              │                               │
│                              ▼                               │
│                    서빙 중 온라인 SHAP 설명 API               │
│                    (각 예측마다 설명 리포트 생성)              │
└─────────────────────────────────────────────────────────────┘
```

```python
import shap
import lime
import lime.tabular
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

# 모델 학습
model = GradientBoostingClassifier()
model.fit(X_train, y_train)

# ── SHAP 기여도 분석 ──
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# 전역 Feature Importance
shap.summary_plot(shap_values, X_test, feature_names=feature_names)

# 개별 예측 설명 (Force Plot)
shap.force_plot(
    explainer.expected_value,
    shap_values[0],
    X_test.iloc[0],
    feature_names=feature_names
)

# ── LIME 설명 ──
lime_explainer = lime.tabular.LimeTabularExplainer(
    X_train,
    feature_names=feature_names,
    class_names=['거절', '승인'],
    mode='classification'
)
lime_exp = lime_explainer.explain_instance(
    X_test.iloc[0],
    model.predict_proba,
    num_features=10
)
lime_exp.show_in_notebook()
```

| 도구 | 지원 기법 | 언어 | 강점 |
|:---|:---|:---|:---|
| **SHAP** | TreeSHAP, KernelSHAP, DeepSHAP | Python | 수학적 엄밀성, 시각화 풍부 |
| **LIME** | LIME (텍스트/이미지/표형) | Python | 범용성, 직관적 |
| **ELI5** | Feature Importance, LIME | Python | sklearn 통합 |
| **Alibi** | SHAP, Counterfactual, Anchors | Python | 프로덕션 서빙 |
| **What-If Tool** | Interactive 분석 | Python/TF | Google 시각화 도구 |
| **Captum** | Integrated Gradients | Python/PyTorch | PyTorch 공식 지원 |

---

## 5. 실무 적용 및 판단

| 관점 | 기대효과 |
|:---|:---|
| **비즈니스** | 모델 신뢰도 상승 → 의사결정자의 AI 활용률 증가 |
| **개발/운영** | 모델 편향 조기 발견, 디버깅 비용 절감 |
| **규제** | EU AI Act, GDPR 컴플라이언스 자동화 |
| **사용자** | 공정한 AI 결정 이의신청 근거 제공 |
| **사회적** | AI 차별 방지, 알고리즘 투명성 확보 |

```
현재 한계:
  ┌─────────────────────────────────────────┐
  │  1. 계산 비용: KernelSHAP O(2^n) 복잡도  │
  │  2. 설명 충실도: 근사이므로 완전하지 않음  │
  │  3. LLM 설명: 텍스트 생성 모델 해석 어려움│
  │  4. 적대적 설명: 의도적 오도 가능         │
  └─────────────────────────────────────────┘

발전 방향:
  ┌─────────────────────────────────────────┐
  │  1. LLM-based 자연어 설명 생성           │
  │  2. 인과적 XAI (Causal Explanation)      │
  │  3. 다중 모달 설명 (이미지+텍스트)        │
  │  4. 실시간 스트리밍 XAI                  │
  └─────────────────────────────────────────┘
```

1. **LIME vs SHAP 선택 기준**: 빠른 탐색적 분석 → LIME, 수학적 보장이 필요한 규제 대응 → SHAP
2. **EU AI Act 연결**: 고위험 AI에 대한 설명 의무는 XAI의 제도적 필수 요소
3. **MLOps 통합 위치**: 학습 후 평가 단계에서 XAI를 자동화하여 편향 감지 게이트로 활용
4. **전역 vs 로컬 설명 조합**: 전역 SHAP으로 모델 전반을 감사하고, 로컬 LIME/SHAP으로 개별 결정을 설명

```
┌─────────────────────────────────────────────────────┐
│              해석 가능성 분류                         │
├───────────────────┬─────────────────────────────────┤
│  범위(Scope)      │  고유(Intrinsic) vs 사후(Post-hoc)│
├───────────────────┼─────────────────────────────────┤
│  로컬(Local)      │  개별 예측 설명                   │
│  전역(Global)     │  모델 전체 동작 설명               │
├───────────────────┼─────────────────────────────────┤
│  모델 불문        │  LIME, SHAP (임의 모델 적용 가능)  │
│  (Model-agnostic) │                                  │
│  모델 특정        │  Attention Map, Decision Tree     │
│  (Model-specific) │  Feature Importance (RF)         │
└───────────────────┴─────────────────────────────────┘
```

LIME은 2016년 Marco Ribeiro 등이 제안한 방법으로, 개별 예측 주변에서 **국소 선형 모델(Locally Linear Model)**로 블랙박스를 근사한다.

```
┌─────────────────────────────────────────────────────────┐
│                  LIME 동작 원리                           │
│                                                          │
│  원본 샘플 x ──→ 주변 섭동(Perturbation) 생성             │
│                  x' = {x₁', x₂', ..., xₙ'}              │
│                         │                                │
│                         ▼                                │
│  블랙박스 모델 f(x') ──→ 예측값 수집                       │
│                         │                                │
│                         ▼                                │
│  거리 기반 가중치 π(x, x') 계산                            │
│  (원본과 가까울수록 높은 가중치)                            │
│                         │                                │
│                         ▼                                │
│  가중 선형 회귀 학습:                                      │
│  g = argmin L(f, g, π) + Ω(g)                            │
│                         │                                │
│                         ▼                                │
│  설명: 각 피처의 선형 계수 = 기여도                         │
└─────────────────────────────────────────────────────────┘
```

```
설명 모델 g 선택:
  ξ(x) = argmin_{g ∈ G} L(f, g, π_x) + Ω(g)

  L: 블랙박스 f와 설명 모델 g의 차이(손실)
  π_x: 샘플 x 근방의 가중치 커널
  Ω(g): 설명 모델의 복잡도 패널티
  G: 선형 모델 계열
```

SHAP은 2017년 Scott Lundberg가 제안한 방법으로, **게임 이론의 샤플리 값(Shapley Value)**을 피처 기여도 계산에 적용한다.

```
게임 이론 유추:
  n명의 플레이어(피처)가 협력해 전체 이익(예측값)을 창출
  → 각 플레이어의 공정한 기여도 = 샤플리 값

샤플리 값 계산:
  φᵢ = Σ_{S⊆F\{i}} [|S|!(|F|-|S|-1)!/|F|!] × [f(S∪{i}) - f(S)]

  S: 피처 i를 제외한 부분 집합
  F: 전체 피처 집합
  f(S): 피처 집합 S만 사용했을 때의 예측값
```

```
┌──────────────────────────────────────────────────────────────┐
│                    SHAP 값 분해                               │
│                                                              │
│  예측값 = 기저값(base value) + Σ SHAP(피처ᵢ)                 │
│                                                              │
│  예시: 신용대출 승인 확률 0.73                                 │
│                                                              │
│  기저값: 0.50 (전체 평균)                                      │
│  ┌─────────────────────────────────────┐                     │
│  │ 소득 높음    : +0.18 ████████       │                     │
│  │ 신용점수 높음: +0.12 ██████         │                     │
│  │ 부채비율 낮음: +0.08 ████           │                     │
│  │ 연체이력 없음: +0.05 ███            │                     │
│  │ 고용기간 짧음: -0.10 ████████ (부정)│                     │
│  └─────────────────────────────────────┘                     │
│  최종 예측: 0.50 + 0.18 + 0.12 + 0.08 + 0.05 - 0.10 = 0.73 │
└──────────────────────────────────────────────────────────────┘
```

| 알고리즘 | 적용 모델 | 특징 |
|:---|:---|:---|
| **TreeSHAP** | 트리 계열 (XGBoost, LightGBM, RF) | O(TLD²) 정확한 계산, 빠름 |
| **DeepSHAP** | 딥러닝 (PyTorch, TensorFlow) | DeepLIFT 기반 근사 |
| **LinearSHAP** | 선형 모델 | 정확한 해석적 계산 |
| **KernelSHAP** | 임의 모델 (Model-agnostic) | LIME 가중치 + 샤플리 수식 결합 |
| **GradientSHAP** | 미분 가능 모델 | 그라디언트 × 입력 기반 |

---

## 6. 기대효과 및 결론

1.

설명 가능한 AI (XAI, Explainable AI)의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
블랙박스 모델 (DNN · 앙상블)
    │ "왜 이렇게 예측했는가?"
    ▼
해석 가능 모델 (Intrinsic)
    ├─► 의사결정 트리 · 선형 회귀 · GAM
    │
사후 해석 (Post-hoc)
    ├─► 로컬: LIME (국소 선형 근사) · SHAP (샤플리 값)
    ├─► 전역: PDP · ALE · Mean |SHAP|
    └─► 이미지: Grad-CAM · Saliency Map
    │
    ▼
규제 대응: EU AI Act · GDPR 설명 요구권
    │
    ▼
LLM-based 자연어 설명 · 인과적 XAI (미래)
```

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 기반 이론 | Shapley Value | 협력 게임 이론의 공정 분배 원칙 |
| 로컬 설명 | LIME | 국소 선형 근사로 개별 예측 설명 |
| 통합 설명 | SHAP | 로컬+전역 통합, 수학적 일관성 |
| 이미지 특화 | Grad-CAM | 합성곱 신경망 히트맵 시각화 |
| 반사실적 설명 | Counterfactual | "X를 바꾸면 결과가 달라진다" |
| 규제 연결 | EU AI Act | 고위험 AI 설명 의무 법제화 |
| MLOps 통합 | Model Card | 모델 특성과 한계 공식 문서화 |
| 편향 감지 | Fairness Audit | XAI로 보호 속성 기여도 검사 |
