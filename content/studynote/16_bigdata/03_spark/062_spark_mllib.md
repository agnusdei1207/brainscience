+++
weight = 62
title = "스파크 엠엘립 (Spark MLlib) - 분산 머신러닝 라이브러리"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 스파크 엠엘립 (Spark MLlib) - 분산 머신러닝 라이브러리은(는) 인메모리 분산 실행과 쿼리 최적화를 통해 대화형 분석·배치·스트리밍을 빠르게 연결하는 스파크 핵심 개념이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

- **정의**: 스파크 에코시스템 내에서 분산 분류, 회귀, 군집, 추천 시스템 및 차원 축소 알고리즘을 수행하기 위한 라이브러리이다.
- **배경**: 단일 노드 머신러닝 라이브러리(scikit-learn 등)로는 처리 불가능한 '테라바이트(TB) 급 대용량 데이터'를 분산 병렬 학습하기 위해 고안되었다.
- **주요 활용**: 대규모 사용자 대상의 상품 추천 시스템, 실시간 로그 기반 사기 탐지(FDS), 대규모 텍스트 데이터의 토픽 모델링 등 빅데이터 분석의 최전선에서 활용된다.

---

## 2. 구성요소

#### 1. ML 파이프라인(Pipeline) 구조
```text
[ Raw Data (DataFrame) ]
      |
      V [ Transformer ] (e.g., Tokenizer, Scaler) --      |
      V [ Estimator ] (e.g., Logistic Regression) --> [ Model (Transformer) ]
      |
      V [ Evaluator ] (e.g., BinaryClassificationEvaluator) --> [ Performance Metric ]
```

#### 2. 핵심 알고리즘 카테고리
- **Classification & Regression**: 로지스틱 회귀, 랜덤 포레스트, GBT(Gradient Boosted Trees), SVM 등
- **Collaborative Filtering**: ALS(Alternating Least Squares) 기반의 대규모 추천 시스템 알고리즘
- **Clustering**: K-means, Gaussian Mixture, LDA(Latent Dirichlet Allocation) 등
- **Dimensionality Reduction**: PCA(주성분 분석), SVD(특이값 분해)

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:
| 비교 항목 | Scikit-learn (Python) | Spark MLlib |
| :--- | :--- | :--- |
| **처리 데이터 규모** | 단일 노드 메모리 한계 (GB 수준) | 클러스터 분산 메모리 (TB/PB 수준) |
| **학습 방식** | 단일 CPU/GPU 위주 학습 | 수백 개의 워커 노드 병렬 학습 |
| **API 편의성** | 매우 높음, 라이브러리 풍부 | ML Pipeline 도입 후 매우 개선됨 |
| **병목 지점** | 연산 속도 및 메모리 부족 | 네트워크 셔플링(Shuffle) 발생 |
| **사용 사례** | 모델 연구 및 중소형 데이터 | 대규모 서비스 운영 및 배치 학습 |

---

## 4. 비교 및 연결

- **데이터 엔지니어링의 중요성**: MLlib 성능의 80%는 학습 알고리즘보다 앞단의 데이터 전처리(`VectorAssembler` 등)와 피처 엔지니어링 효율화에서 결정된다.
- **하이퍼파라미터 튜닝 최적화**: `CrossValidator`를 사용한 대규모 병렬 튜닝 시 클러스터 자원이 급격히 소모될 수 있으므로, 그리드 서치(Grid Search) 범위를 신중히 설정해야 한다.
- **모델 서빙(Serving) 전략**: 학습된 MLlib 모델을 실시간 추론에 사용할 경우, Spark 클러스터 오버헤드를 피하기 위해 PMML이나 MLeap 같은 표준 포맷으로 익스포트하여 경량 서버에서 서빙하는 방식이 선호된다.

---

## 5. 실무 적용 및 판단

- **기대효과**: 데이터 분석가가 복잡한 분산 프로그래밍 지식 없이도 고성능 대규모 머신러닝 시스템을 직접 구축하고 배포할 수 있게 한다.
- **결론**: MLlib은 빅데이터 플랫폼으로서의 스파크의 가치를 완성하는 조각이다. 향후 딥러닝 프레임워크와의 연동(Spark deep learning pipelines) 및 분산 학습 표준화를 통해 데이터 과학의 대중화를 이끌 핵심 기술로 남을 것이다.

---

## 6. 기대효과 및 결론

스파크 엠엘립 (Spark MLlib) - 분산 머신러닝 라이브러리은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[원시 피처 데이터 (Raw Feature Data) — DataFrame·RDD로 메모리 로딩]
    │
    ▼
[피처 엔지니어링 (Feature Engineering) — MLlib Pipeline으로 전처리·변환]
    │
    ▼
[모델 학습 (Model Training) — 분산 클러스터 병렬 알고리즘 수행]
    │
    ▼
[모델 평가 (Model Evaluation) — CrossValidator·TrainValidationSplit]
    │
    ▼
[모델 배포 (Model Serving) — MLflow·Spark Structured Streaming 연동]
```

이 흐름은 Spark MLlib가 피처 전처리부터 분산 학습·평가·서빙까지 머신러닝 파이프라인을 일원화하는 과정을 나타낸다.

---

## 8. 관련 개념 맵

1. **Transformer**: 데이터를 다른 데이터로 변환하는 알고리즘 (추론 포함)
2. **Estimator**: 데이터를 학습하여 모델(Transformer)을 생성하는 알고리즘
3. **ALS (Alternating Least Squares)**: 행렬 분해 기반의 추천 시스템 핵심 알고리즘
