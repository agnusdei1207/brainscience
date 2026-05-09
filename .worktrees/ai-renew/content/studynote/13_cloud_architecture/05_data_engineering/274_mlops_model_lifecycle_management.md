+++
weight = 274
title = "274. MLOps - ML 모델 생명주기 자동화"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MLOps(Machine Learning Operations)는 ML 모델의 개발→훈련→검증→배포→모니터링→재훈련 전체 생명주기를 DevOps 원칙으로 자동화하여 실험실의 모델이 안정적인 프로덕션 서비스로 전환되도록 하는 엔지니어링 실천이다.
> 2. **가치**: ML 모델 87%가 프로덕션에 배포되지 못한다는 통계처럼, 개발과 운영 사이의 간극을 메우는 것이 MLOps의 본질 — 특히 Concept Drift(개념 드리프트)가 발생하면 자동으로 재훈련을 트리거하는 지속적 학습 파이프라인이 핵심이다.
> 3. **판단 포인트**: MLOps 성숙도 3단계 — Level 0(수동 프로세스) → Level 1(ML 파이프라인 자동화) → Level 2(CI/CD 완전 자동화) — 조직의 현재 수준을 파악하고 단계별 개선 로드맵을 제시하는 것이 기술사 답안의 핵심이다.

---

## Ⅰ. 개요 및 필요성

데이터 과학자가 Jupyter 노트북에서 정확도 95%의 사기 탐지 모델을 개발했다. 이 모델을 프로덕션에서 실행하기까지의 여정:

- 노트북 코드 → 프로덕션 파이썬 패키지로 리팩토링
- 학습 데이터 버전 관리
- 모델 검증 및 A/B 테스트
- 컨테이너화 및 API 서빙
- 성능 모니터링
- 6개월 후 사기 패턴이 변화 → 모델 재훈련

이 전체 과정을 수작업으로 관리하면 실수와 비일관성이 빈발한다. **MLOps**는 이를 코드로 정의하고 자동화한다.

```
[MLOps 생명주기]

데이터 준비 → Feature Engineering → 모델 훈련 → 모델 평가
     │                                              │
     │         재훈련 트리거 ◄──── 드리프트 감지    │
     │         (자동)                               ▼
     └─────────────────────────────────────── 모델 등록
                                                    │
                                              CD 배포 파이프라인
                                                    │
                                         모니터링 → Canary 배포 → 전체 배포
```

📢 **섹션 요약 비유**: MLOps는 공장 자동화 라인이다. 데이터 과학자가 설계한 제품(모델)을 수작업으로 만들지 않고, 컨베이어 벨트(파이프라인)가 자동으로 생산·검사·출하한다. 불량(드리프트)이 감지되면 설계를 자동으로 수정(재훈련)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### MLOps 3대 핵심 구성요소

```
[MLOps 삼위일체]

           데이터 파이프라인
           ┌────────────────┐
           │ 데이터 수집      │
           │ Feature 엔지니어링│
           │ 품질 검증        │
           └────────┬────────┘
                    │
           ML 파이프라인
           ┌────────▼────────┐
           │ 모델 훈련 자동화 │
           │ 하이퍼파라미터   │
           │ 튜닝 (AutoML)   │
           │ 실험 추적        │
           └────────┬────────┘
                    │
           CD 파이프라인
           ┌────────▼────────┐
           │ 모델 검증        │
           │ A/B 테스트       │
           │ Canary 배포      │
           │ 모니터링/알림    │
           └─────────────────┘
```

### Concept Drift vs Data Drift

| 드리프트 유형 | 정의 | 예시 | 탐지 방법 |
|:---|:---|:---|:---|
| **Data Drift** | 입력 Feature 분포 변화 | 사용자 연령대 분포 변화 | PSI, KL Divergence |
| **Concept Drift** | Feature-Label 관계 변화 | 사기 패턴 자체가 변화 | 모델 성능 지표 모니터링 |
| **Label Drift** | 레이블 분포 변화 | 사기 비율 급감/급증 | 레이블 분포 추적 |
| **Prediction Drift** | 예측 분포 변화 | 모델 출력 점수 분포 변화 | 예측값 분포 모니터링 |

### MLOps 성숙도 모델 (Google MLOps)

| 레벨 | 특징 | 자동화 수준 |
|:---|:---|:---|
| **Level 0** | 수동 프로세스, 사일로 | 스크립트, 수작업 배포 |
| **Level 1** | ML 파이프라인 자동화 | 훈련 파이프라인, CT(Continuous Training) |
| **Level 2** | CI/CD 완전 자동화 | 자동 재훈련, 자동 배포, 자동 롤백 |

📢 **섹션 요약 비유**: MLOps 성숙도는 요리 자동화 수준이다. Level 0는 셰프가 매번 직접 요리, Level 1은 표준 레시피와 계량 도구 사용, Level 2는 로봇 주방에서 재료 감지 → 레시피 조정 → 자동 요리까지 완전 자동화된 상태다.

---

## Ⅲ. 비교 및 연결

### MLOps 도구 생태계

| 범주 | 도구 | 특징 |
|:---|:---|:---|
| **실험 추적** | MLflow, W&B (Weights & Biases) | 파라미터·메트릭·아티팩트 버전 관리 |
| **파이프라인 오케스트레이션** | Kubeflow, Apache Airflow, ZenML | ML 파이프라인 DAG 정의·실행 |
| **모델 레지스트리** | MLflow Registry, AWS SageMaker, Azure ML | 모델 버전·상태 관리 |
| **모델 서빙** | Triton, TF Serving, BentoML | GPU 최적화, 멀티 모델 서빙 |
| **모니터링** | Evidently AI, Arize AI, Seldon | Feature·예측 드리프트 감지 |
| **완전 관리형** | AWS SageMaker, Azure ML, Vertex AI | 전체 MLOps 스택 통합 |

### DevOps vs MLOps 차이

| 항목 | DevOps | MLOps |
|:---|:---|:---|
| **버전 관리 대상** | 코드 | 코드 + 데이터 + 모델 |
| **테스트** | 기능 테스트 | 기능 + 모델 성능 + 데이터 품질 |
| **모니터링** | 가용성·응답시간 | + 모델 성능·드리프트 |
| **배포 실패 원인** | 코드 버그 | + 데이터 변화, 모델 성능 저하 |
| **재배포 트리거** | 코드 변경 | + 데이터 변화, 드리프트 |

📢 **섹션 요약 비유**: MLOps가 DevOps와 다른 점은 "제품이 시간에 따라 알아서 낡아간다"는 것이다. 소프트웨어는 코드를 바꾸지 않으면 동일하게 동작하지만, ML 모델은 세상이 변하면 성능이 저하된다. MLOps는 이 "알아서 낡아가는 문제"까지 자동으로 관리해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### MLflow 실험 추적 예시

```python
import mlflow
import mlflow.sklearn

with mlflow.start_run():
    # 파라미터 기록
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)

    # 모델 훈련
    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)

    # 메트릭 기록
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("auc", roc_auc_score(y_test, model.predict_proba(X_test)[:,1]))

    # 모델 저장
    mlflow.sklearn.log_model(model, "fraud_detector")
    mlflow.set_tag("drift_status", "stable")
```

### 드리프트 감지 및 자동 재훈련

```python
# Evidently AI로 Data Drift 감지
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=training_data, current_data=production_data)

drift_results = report.as_dict()
if drift_results["metrics"][0]["result"]["dataset_drift"]:
    # 드리프트 감지 → 자동 재훈련 파이프라인 트리거
    trigger_retraining_pipeline()
    notify_team("Data drift detected, retraining triggered")
```

### 기술사 시험 판단 포인트

- **MLOps Level 0→2 단계 진화**: 수동 → ML 파이프라인 자동화 → CI/CD 완전 자동화
- **드리프트 3종 구분**: Data Drift(입력 분포) vs Concept Drift(관계 변화) vs Prediction Drift(출력 분포)
- **Continuous Training (CT)**: 새 데이터가 쌓이면 자동으로 재훈련 — MLOps의 핵심 자동화 요소

📢 **섹션 요약 비유**: Concept Drift는 어제의 날씨 패턴으로 만든 우산 예보 모델이, 기후 변화로 패턴이 바뀌어 내일 비를 예측하지 못하는 것이다. 모델이 잘못된 게 아니라 세상이 바뀐 것이다. MLOps는 이 변화를 감지하고 자동으로 새 모델을 훈련한다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 영역 | 효과 |
|:---|:---|
| **배포 속도** | 모델 개발 → 프로덕션 배포 기간 단축 (수주 → 수일) |
| **신뢰성** | 자동 검증 + 모니터링으로 프로덕션 장애 최소화 |
| **지속 성능** | 드리프트 자동 탐지 + 재훈련으로 모델 성능 유지 |
| **협업 효율** | 데이터 과학자 + ML 엔지니어 + DevOps 역할 명확화 |

### 한계 및 주의사항

- **초기 구축 비용**: MLOps 인프라 구축에 상당한 엔지니어링 투자 필요
- **과도한 자동화**: 모든 재훈련을 자동화하면 잘못된 데이터로 훈련된 모델이 자동 배포될 위험
- **조직 문화**: 데이터 과학자와 엔지니어 간 사일로를 깨는 조직 변화 필요
- **툴 과잉**: 수십 개의 MLOps 도구 중 조직에 맞는 최소 스택 선택이 어려움

📢 **섹션 요약 비유**: MLOps는 스타트업에게 과잉 투자일 수 있다. 모델 1~2개를 수동으로 관리하는 초기 단계에서 완전한 MLOps 파이프라인을 구축하면 오히려 속도가 느려진다. "지금 필요한 자동화"부터 시작하여 성숙도를 단계적으로 높이는 것이 실용적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 피처 스토어 | MLOps의 데이터 레이어 (Feature 일관성 보장) |
| 모델 레지스트리 | MLOps의 모델 버전 관리 레이어 |
| Concept Drift | MLOps의 재훈련 트리거 주요 원인 |
| Kubeflow | K8s 기반 ML 파이프라인 오케스트레이션 |
| DevOps | MLOps의 기반 원칙 (CI/CD, 자동화, 모니터링) |
| A/B 테스트 | 신규 모델의 안전한 점진적 배포 기법 |

### 👶 어린이를 위한 3줄 비유 설명
1. MLOps는 AI 선수(모델)의 트레이닝 관리 시스템이야. 연습(훈련)→경기(배포)→성적 분석(모니터링)→보완 훈련(재훈련)을 자동으로 해줘.
2. 사기 패턴이 바뀌면(Concept Drift) AI가 낡아져. MLOps는 이걸 감지하고 "새 훈련이 필요해!"라고 자동으로 알려줘.
3. 데이터 과학자가 모델을 만들기만 하면, 나머지 배포·모니터링·업데이트는 MLOps 시스템이 알아서 해주는 거야!
