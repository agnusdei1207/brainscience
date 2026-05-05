+++
weight = 102
title = "탐색적 데이터 분석 (EDA, Exploratory Data Analysis)"
date = "2025-05-22"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 탐색적 데이터 분석 (EDA, Exploratory Data Analysis)은(는) 대규모 데이터에서 패턴·예측·의사결정 근거를 추출하기 위한 분석 기법 또는 모델이다.
> **비유**: 광산에서 캐낸 원석을 분류·정제해 의미 있는 보석으로 가공하는 과정과 같다.

📝 모범 답안

## 1. 개요 및 필요성

빅데이터 분석에서 가장 위험한 것은 성급한 결론입니다. EDA는 존 튜키(John Tukey)가 제안한 방법론으로, 단순히 요약 통계량(평균 등)에만 의존하지 않고 저항성(Resistancy)과 잔차(Residual) 분석 등을 통해 데이터의 '속살'을 파악합니다. 이는 분석의 정확도를 높이고 불필요한 시행착오를 줄이는 핵심 절차입니다.

---

## 2. 구성요소

EDA의 4대 핵심 원칙과 분석 워크플로우 아키텍처입니다.

```text
[ EDA Iteration Loop & 4 Core Principles ]

  [ Raw Data ] --                         ^                          |
                         | (Discovery)              v
                  [ Model Design ] <--- [ Insights / Hypothesis ]

[ 4 Principles of EDA ]
1. Resistance (저항성): 이상치(Outlier)에 영향을 덜 받는 척도 사용.
2. Residual (잔차): 관찰값과 예측값의 차이를 분석하여 숨은 패턴 탐색.
3. Re-expression (재표현): 로그 변환 등으로 데이터 구조를 단순화/정규화.
4. Revelation (현시성): 그래프를 통한 시각화로 데이터를 한눈에 보여줌.
```

**핵심 원리:**
1. **일변량 분석 (Univariate)**: 변수 하나의 분포(히스토그램, 박스플롯)와 중심 경향성 확인.
2. **이변량 분석 (Bivariate)**: 두 변수 간의 상관관계(산점도, 상관계수) 및 인과 관계의 실마리 탐색.
3. **다변량 분석 (Multivariate)**: 3개 이상의 변수 조합을 통해 복합적인 영향도 파악 (히트맵, PCA 등).
4. **시각화의 힘**: '안스콤의 4분할(Anscombe's Quartet)' 예시처럼 요약 통계가 같아도 그래프는 완전히 다를 수 있음을 명심해야 함.

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 전처리, 모델 가정, 평가 지표, 해석 가능성을 함께 검토해야 한다.

동작 순서:
| 비교 항목 | 탐색적 분석 (EDA) | 확증적 분석 (CDA, Confirmatory) |
| :--- | :--- | :--- |
| **목적** | 패턴 발견, 가설 수립 | 가설 검증, 유의성 확정 |
| **자세** | 개방적, 유연함, 탐정(Detective) | 보수적, 엄격함, 판사(Judge) |
| **주요 도구** | 그래프, 산점도, 상자 수염 그림 | p-value, 신뢰구간, t-test, ANOVA |
| **수행 시점** | 분석의 시작 (Pre-processing) | 분석의 결론 (Verification) |
| **상호 작용** | EDA에서 발견한 패턴을 CDA에서 검증하는 상호보완 관계 |

---

## 4. 비교 및 연결

* **적용 전략 (Implementation Strategy)**:
  * **데이터 시각화 도구 활용**: Python의 Seaborn, Plotly 등을 활용하여 동적 시각화를 수행하고, 데이터의 층(Layer)별 특징 파악.
  * **반복적 프로세스**: 한 번의 EDA로 끝나지 않고, 피처 엔지니어링(Feature Engineering) 후에 다시 EDA를 수행하여 데이터의 변화를 지속적으로 관찰.
* **기술사적 판단 (Architectural Judgment)**:
  * 빅데이터 환경에서 모든 행을 시각화하는 것은 불가능함. 따라서 신뢰할 수 있는 무작위 샘플링(Sampling)을 통해 EDA를 수행하거나, 데이터 레이크의 메타데이터를 활용한 '프로파일링(Profiling)' 자동화 시스템 구축이 필수적임.

---

## 5. 실무 적용 및 판단

EDA는 분석 모델의 품질(Garbage In, Garbage Out 방지)을 결정짓는 가장 중요한 공정입니다. 향후에는 AI가 자동으로 데이터의 특징을 파악하여 가장 적합한 시각화와 이상 징후 보고서를 생성해 주는 'Auto-EDA' 도구들이 데이터 거버넌스 시스템의 표준 기능으로 통합될 것입니다.

---

## 6. 기대효과 및 결론

탐색적 데이터 분석 (EDA, Exploratory Data Analysis)은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 분석 기법의 실무 가치는 모델의 화려함보다 데이터 가정과 해석 책임을 얼마나 지키느냐에서 나온다.

---

## 7. 발전 흐름도

```text
[시각화 기술: Histogram, Box Plot, Scatter Matrix, Heatmap]
    │
    ▼
[데이터 정제: Outlier Detection, Imputation, Scaling]
    │
    ▼
[분석 기구: Correlation Analysis, Feature Importance, Anscombe's Quartet]
```

이 흐름도는 시각화 기술: Histogram, Box Plot, Scatter Matrix, Heatmap에서 출발해 분석 기구: Correlation Analysis, Feature Importance, Anscombe's Quartet까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

* **시각화 기술**: Histogram, Box Plot, Scatter Matrix, Heatmap
* **데이터 정제**: Outlier Detection, Imputation, Scaling
* **분석 기구**: Correlation Analysis, Feature Importance, Anscombe's Quartet
