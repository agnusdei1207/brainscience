+++
title = "MLOps (머신러닝 운영)"
description = "머신러닝 모델의 개발, 학습, 배포, 모니터링을 자동화하고 지속적으로 통합/전달하는 엔지니어링 실천법으로 DevOps의 ML 확장"
date = 2024-05-15
[taxonomies]
tags = ["MLOps", "Machine-Learning", "DevOps", "CI/CD", "Model-Deployment", "Feature-Store"]
+++

# MLOps (머신러닝 운영)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 머신러닝(ML) 모델의 전체 수명 주기(데이터 준비 - 모델 학습 - 검증 - 배포 - 모니터링 - 재학습)를 DevOps 원칙(자동화, CI/CD, 모니터링)으로 관리하여, 실험 단계의 모델을 프로덕션 환경에서 안정적으로 운영하고 지속적으로 개선하는 엔지니어링 분야입니다.
> 2. **가치**: ML 모델 배포 시간을 주/월 단위에서 시간 단위로 단축하고, 모델 드리프트(Drift)를 자동 감지하여 재학습함으로써 AI 서비스의 품질 저하를 방지하고 80% 이상의 운영 효율성을 향상시킵니다.
> 3. **융합**: 피처 스토어(Feature Store), 모델 레지스트리(Model Registry), 실험 추적(Experiment Tracking), A/B 테스팅, 카나리 배포와 결합하여 신뢰성 높은 AI 서비스를 구축합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**MLOps(Machine Learning Operations)**는 머신러닝 시스템의 **개발(Data Science)과 운영(Production Engineering) 간의 협업과 자동화**를 다루는 실천법, 문화, 도구의 집합입니다. DevOps가 소프트웨어의 CI/CD를 다룬다면, MLOps는 ML 모델의 지속적 학습(CT: Continuous Training)과 지속적 배포(CD: Continuous Deployment)를 다룹니다. MLOps의 핵심 구성 요소는:
- **데이터 파이프라인(Data Pipeline)**: 데이터 수집, 전처리, 피처 엔지니어링 자동화
- **모델 학습 파이프라인(Training Pipeline)**: 하이퍼파라미터 튜닝, 분산 학습, 실험 추적
- **모델 배포(Deployment)**: 모델 서빙, API 엔드포인트, 엣지 배포
- **모니터링(Monitoring)**: 모델 성능, 데이터 드리프트, 예측 품질 추적
- **피드백 루프(Feedback Loop)**: 재학습 트리거, 모델 버전 관리

### 2. 구체적인 일상생활 비유
요리 레스토랑을 상상해 보세요. **데이터 사이언티스트**는 새로운 요리 레시피(ML 모델)를 연구실에서 개발합니다. **MLE(MLOps 엔지니어)**는 이 레시피를 실제 주방에서 수천 명의 손님에게 서빙할 수 있도록 시스템화합니다. 재료 공급(Data Pipeline)을 안정화하고, 조리 시간(Training Time)을 최적화하고, 요리가 나가는 속도(Inference Latency)를 높이고, 맛이 변질되면(Drift) 즉시 알려주는 시스템을 만듭니다. 레시피가 개선되면 자동으로 주방에 업데이트됩니다(Continuous Training).

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (ML의 마지막 마일 문제)**:
   Gartner에 따르면 **87%의 ML 프로젝트가 프로덕션에 배포되지 못합니다**. 데이터 사이언티스트는 Jupyter Notebook에서 모델을 개발하지만, 이를 실제 서비스로 배포하는 것은 전혀 다른 기술 스택(Kubernetes, API 서버, 모니터링)이 필요합니다. 이 격차를 마지막 마일(Last Mile) 문제라 합니다.

2. **혁신적 패러다임 변화의 시작**:
   2015년 구글이 Machine Learning: The High-Interest Credit Card of Technical Debt 논문에서 ML 시스템의 엔지니어링 부채 문제를 지적했습니다. 2018년 구글이 TFX(TensorFlow Extended)를, 2019년 MLflow가 인기를 얻으며 MLOps 도구 생태계가 형성되었습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   ChatGPT, DALL-E 등 생성형 AI의 폭발적 성장과 함께 기업들은 AI를 서비스에 통합해야 합니다. 그러나 AI 모델은 시간이 지나면 성능이 저하됩니다(Data Drift). MLOps는 이를 자동으로 감지하고 재학습하여 AI 서비스의 지속적 품질을 보장합니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 관련 도구/기술 | ML 수명 주기 단계 |
| :--- | :--- | :--- | :--- | :--- |
| **Feature Store** | 피처(Feature)의 중앙 저장 및 재사용 | 피처 정의, 계산, 저장, 검색 API | Feast, Tecton, AWS Feature Store | 데이터 준비 |
| **Experiment Tracking** | 실험 파라미터, 메트릭, 아티팩트 추적 | Git과 유사한 버전 관리 for ML | MLflow, Weights & Biases, Neptune | 모델 학습 |
| **Model Registry** | 학습된 모델의 버전 관리 및 승인 | 모델 메타데이터, 서명, 태그 관리 | MLflow Registry, Seldon Core | 모델 검증 |
| **Training Pipeline** | 분산 학습, 하이퍼파라미터 튜닝 자동화 | Kubeflow Pipelines, Apache Airflow DAG | Kubeflow, Ray, SageMaker | 모델 학습 |
| **Model Serving** | 모델 추론(Inference) API 서빙 | REST/gRPC 엔드포인트, 배치 추론 | TensorFlow Serving, Triton, Seldon | 모델 배포 |
| **Model Monitoring** | 모델 성능, 드리프트, 설명 가능성 추적 | 실제 vs 예측 분포 비교, 알람 | Evidently, WhyLabs, Arize | 모델 운영 |

### 2. 정교한 구조 다이어그램: MLOps 엔드 투 엔드 파이프라인

```text
=====================================================================================================
                      [ MLOps End-to-End Architecture ]
=====================================================================================================

  [ DATA ]           [ DEVELOP ]          [ TRAIN ]            [ DEPLOY ]          [ MONITOR ]
     |                    |                    |                    |                   |
     v                    v                    v                    v                   v

+-------------+   +-------------+   +-------------+   +-------------+   +-------------+
| Data Lake   |   | Experiment  |   | Training    |   | Model       |   | Production  |
| / Warehouse |   | Environment |   | Cluster     |   | Serving     |   | Traffic     |
|             |   | (Notebook)  |   | (GPU/TPU)   |   | (K8s/Kserve)|   |             |
+------+------+   +------+------+   +------+------+   +------+------+   +------+
       |                 |                 |                 |                 |
       |                 |                 |                 |                 |
       v                 v                 v                 v                 v

+-----------------------------------------------------------------------------------------+
|                              [ MLOps Pipeline ]                                         |
|                                                                                         |
|  +-----------------------------------------------------------------------------------+  |
|  | 1. DATA PIPELINE                                                                  |  |
|  |    +---------+    +---------+    +---------+    +---------+                       |  |
|  |    | Raw     | -> | ETL     | -> | Feature | -> | Feature |                       |  |
|  |    | Data    |    | Process |    | Engineer|    | Store   |                       |  |
|  |    +---------+    +---------+    +---------+    +----+----+                       |  |
|  |                                                      |                           |  |
|  +------------------------------------------------------+---------------------------+  |
|                                                         |                              |
|  +------------------------------------------------------+---------------------------+  |
|  | 2. TRAINING PIPELINE                                            |               |  |
|  |    +---------+    +---------+    +---------+    +-----+-------+               |  |
|  |    | Load    | -> | Train   | -> | Validate| -> | Register    |               |  |
|  |    | Features|    | Model   |    | Metrics |    | to Store    |               |  |
|  |    +---------+    +---------+    +---------+    +-----+-------+               |  |
|  |      |              |              |                    |                       |  |
|  |      |         Experiment Tracking |                    |                       |  |
|  |      |         (MLflow/W&B)        |                    |                       |  |
|  +------------------------------------+--------------------+-----------------------+  |
|                                     |                    |                          |
|  +----------------------------------+--------------------+-----------------------+  |
|  | 3. DEPLOYMENT PIPELINE           |                    |                       |  |
|  |    +---------+    +---------+    +-+-------+    +-----+-------+               |  |
|  |    | Model   | -> | Package | -> | Deploy  | -> | Serve API   |               |  |
|  |    | Registry|    | (Contai-|    | Canary  |    | (TF         |               |  |
|  |    |         |    |  ner)   |    | (10%)   |    |  Serving)   |               |  |
|  |    +---------+    +---------+    +---------+    +-----+-------+               |  |
|  +--------------------------------------------------------+-----------------------+  |
|                                                           |                          |
|  +--------------------------------------------------------+-----------------------+  |
|  | 4. MONITORING PIPELINE                                   |                       |  |
|  |    +---------+    +---------+    +---------+    +-------+-------+             |  |
|  |    | Log     | -> | Detect  | -> | Alert   | -> | Trigger       |             |  |
|  |    | Predic- |    | Drift   |    | (Slack) |    | Retraining    |             |  |
|  |    | tions   |    | & Decay |    |         |    | (Back to 2)   |             |  |
|  |    +---------+    +---------+    +---------+    +---------------+             |  |
|  +---------------------------------------------------------------------------------+  |
|                                                                                       |
+---------------------------------------------------------------------------------------+

=====================================================================================================
```

### 3. 심층 동작 원리 (MLOps 핵심 메커니즘)

**1. 피처 스토어 (Feature Store) - 피처 재사용성과 일관성**
피처 스토어는 ML 피처(Feature)의 중앙 저장소입니다:
- **오프라인 스토어**: 학습용 과거 데이터 (Parquet, Delta Lake)
- **온라인 스토어**: 실시간 추론용 저지연 스토어 (Redis, DynamoDB)
- **피처 서빙 API**: store.get_online_features(feature_names, entity_keys)

이를 통해 동일한 피처가 학습과 추론에서 동일하게 계산되어 Training-Serving Skew 문제를 방지합니다.

**2. 실험 추적 (Experiment Tracking) - 재현성 보장**
모든 실험의 파라미터, 메트릭, 아티팩트를 추적합니다:
- mlflow.log_params({"learning_rate": 0.001, "batch_size": 32})
- mlflow.log_metrics({"accuracy": 0.95, "f1_score": 0.93})
- mlflow.log_artifact("model.onnx")

동일한 실험을 재현할 수 있고, 어떤 파라미터가 최고 성능을 냈는지 비교할 수 있습니다.

**3. 지속적 학습 (Continuous Training) - 드리프트 대응**
프로덕션 모델의 성능이 저하되면 자동으로 재학습이 트리거됩니다:
1. 모니터링 시스템이 데이터 드리프트 또는 예측 정확도 저하를 감지
2. Airflow/Kubeflow 파이프라인이 트리거되어 최신 데이터로 재학습
3. 새 모델이 기존 모델보다 우수하면 자동으로 카나리 배포
4. A/B 테스트로 신규 모델 검증 후 전체 트래픽 전환

### 4. 핵심 알고리즘 및 실무 코드 예시

**MLOps 파이프라인 (Kubeflow Pipelines + MLflow)**

```python
# pipelines/training_pipeline.py
import kfp
from kfp import dsl
from kfp.components import create_component_from_func
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib

# Component 1: Data Ingestion
def load_data(feature_store_path: str) -> str:
    import pandas as pd
    df = pd.read_parquet(feature_store_path)
    df.to_csv('/tmp/data.csv', index=False)
    return '/tmp/data.csv'

# Component 2: Model Training with Experiment Tracking
def train_model(data_path: str, n_estimators: int, max_depth: int) -> str:
    import mlflow
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, f1_score

    # Start MLflow experiment
    mlflow.set_experiment("customer_churn_prediction")
    with mlflow.start_run():

        # Log hyperparameters
        mlflow.log_params({
            "n_estimators": n_estimators,
            "max_depth": max_depth
        })

        # Load and split data
        df = pd.read_csv(data_path)
        X = df.drop('target', axis=1)
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        # Log metrics
        mlflow.log_metrics({
            "accuracy": accuracy,
            "f1_score": f1
        })

        # Register model (only if meets quality gate)
        if accuracy > 0.85:  # Quality Gate
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name="customer_churn_model"
            )
            print(f"Model registered with accuracy: {accuracy}")

        # Save model path for next component (using joblib instead of pickle for safety)
        model_path = '/tmp/model.joblib'
        joblib.dump(model, model_path)

    return model_path

# Component 3: Model Deployment
def deploy_model(model_path: str, model_version: int) -> str:
    import subprocess

    # Deploy to Kubernetes using Seldon Core
    deployment_yaml = f"""
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: churn-model
spec:
  predictors:
  - name: default
    replicas: 2
    graph:
      name: classifier
      implementation: SKLEARN_SERVER
      modelUri: s3://models/churn/v{model_version}
      envSecretRefName: s3-credentials
"""
    with open('/tmp/deployment.yaml', 'w') as f:
        f.write(deployment_yaml)

    subprocess.run(['kubectl', 'apply', '-f', '/tmp/deployment.yaml'])
    return f"Model v{model_version} deployed successfully"

# Define Kubeflow Pipeline
@dsl.pipeline(
    name='ML Training Pipeline',
    description='End-to-end ML training with MLOps best practices'
)
def ml_pipeline(
    feature_store_path: str = 's3://feature-store/churn_features.parquet',
    n_estimators: int = 100,
    max_depth: int = 10
):
    # Component 1: Load data
    load_task = create_component_from_func(
        load_data, base_image='python:3.9'
    )(feature_store_path=feature_store_path)

    # Component 2: Train model
    train_task = create_component_from_func(
        train_model, base_image='python:3.9'
    )(
        data_path=load_task.output,
        n_estimators=n_estimators,
        max_depth=max_depth
    )

    # Component 3: Deploy model
    deploy_task = create_component_from_func(
        deploy_model, base_image='bitnami/kubectl:latest'
    )(
        model_path=train_task.output,
        model_version=1
    )

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(ml_pipeline, 'pipeline.yaml')
```

**모델 드리프트 모니터링 (Evidently AI)**

```python
# monitoring/drift_monitoring.py
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset
from evidently.metrics import *
import pandas as pd
import numpy as np

class ModelDriftMonitor:
    def __init__(self, reference_data: pd.DataFrame):
        self.reference_data = reference_data
        self.column_mapping = ColumnMapping(
            target='target',
            prediction='prediction',
            numerical_features=['age', 'tenure', 'monthly_charges'],
            categorical_features=['contract_type', 'payment_method']
        )

    def detect_drift(self, current_data: pd.DataFrame) -> dict:
        """Detect data and concept drift"""

        # Data Drift Report
        data_drift_report = Report(metrics=[
            DataDriftPreset(),
            DatasetDriftMetric(),
            # Column-level drift
            ColumnDriftMetric(column_name='age'),
            ColumnDriftMetric(column_name='monthly_charges'),
        ])

        data_drift_report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping
        )

        # Extract drift metrics
        result = data_drift_report.as_dict()

        drift_detected = result['metrics'][1]['result']['dataset_drift']
        drift_share = result['metrics'][1]['result']['drift_share']

        # Trigger retraining if drift exceeds threshold
        if drift_detected and drift_share > 0.3:  # 30% of features drifted
            self._trigger_retraining()

        return {
            'drift_detected': drift_detected,
            'drift_share': drift_share,
            'recommendation': 'Retrain model' if drift_share > 0.3 else 'Continue monitoring'
        }

    def _trigger_retraining(self):
        """Trigger Kubeflow pipeline for retraining"""
        import requests

        response = requests.post(
            'http://kubeflow-pipeline-api/pipeline/runs',
            json={
                'pipeline_name': 'ml_training_pipeline',
                'parameters': {
                    'trigger': 'drift_detected',
                    'timestamp': pd.Timestamp.now().isoformat()
                }
            }
        )
        print(f"Retraining triggered: {response.json()}")

# Usage
if __name__ == '__main__':
    # Load reference data (from training)
    reference = pd.read_parquet('s3://data/reference_data.parquet')

    # Load current production data
    current = pd.read_parquet('s3://data/production_data_last_24h.parquet')

    monitor = ModelDriftMonitor(reference)
    drift_result = monitor.detect_drift(current)
    print(drift_result)
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: ML 운영 방식 비교

| 평가 지표 | 수동 ML (Ad-hoc) | MLOps Level 0 | MLOps Level 1 | MLOps Level 2 |
| :--- | :--- | :--- | :--- | :--- |
| **배포 방식** | 수동 스크립트 | 수동 배포 | CI/CD 자동화 | CI/CD/CT 자동화 |
| **모델 버전 관리** | 없음 | 파일명으로만 | Model Registry | 전체 라인리지 |
| **재학습** | 수동 | 수동 | 수동 트리거 | 자동 (Drift 감지) |
| **모니터링** | 없음 | 기본 메트릭 | 성능 메트릭 | 드리프트 + 설명가능성 |
| **피처 관리** | 스크립트 내 계산 | 스크립트 | Feature Store | Feature Store + 온라인 |
| **실험 추적** | 엑셀/노트 | 로컬 파일 | MLflow/W&B | 통합 플랫폼 |
| **적용 조직** | 연구실 | 소규모 팀 | 성숙한 팀 | 엔터프라이즈 |

### 2. 과목 융합 관점 분석

**MLOps + DevOps (CI/CD for ML)**
- ML 모델도 코드와 마찬가지로 버전 관리(Git), 코드 리뷰, 자동화된 테스트, 단계적 배포가 필요합니다. MLOps는 DevOps의 원칙을 ML 아티팩트(모델, 데이터, 피처)로 확장합니다.

**MLOps + DataOps (Data Pipeline Integration)**
- ML 모델은 데이터 품질에 직접적으로 영향을 받습니다. DataOps의 데이터 품질 검증, 스키마 변경 관리, 파이프라인 오케스트레이션이 MLOps의 상위 단계로 통합됩니다.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 추천 시스템 모델 성능 저하**
- **문제점**: 이커머스 추천 모델의 클릭률(CTR)이 지난 달 대비 15% 감소했습니다.
- **기술사 판단 (전략)**: MLOps 모니터링 시스템으로 원인 분석. 1) 데이터 드리프트 확인 (사용자 행동 패턴 변화) 2) 모델 노후화 확인 (6개월 전 모델 사용 중) 3) 피처 품질 저하 확인. 분석 결과, 신규 상품 카테고리가 추가되었는데 모델이 이를 학습하지 못함. 자동 재학습 파이프라인 트리거.

**[상황 B] 신규 ML 서비스 출시**
- **문제점**: 새로운 고객 이탈 예측 서비스를 3개월 내 출시해야 합니다.
- **기술사 판단 (전략)**: MLOps Level 1 수준으로 시작. 1) MLflow로 실험 추적 2) Feature Store 구축 (Feast) 3) Kubernetes 기반 모델 서빙. 레벨 2(자동 재학습)은 서비스 안정화 후 도입.

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] 피처 스토어 필요성: 다수 모델이 동일 피처를 사용하는가?
- [ ] 모델 서빙 규모: 초당 몇 건의 추론 요청이 예상되는가?
- [ ] GPU/TPU 활용: 대규모 모델 학습을 위한 컴퓨팅 리소스
- [ ] 데이터 파이프라인: 스트리밍 vs 배치 처리 요구사항

**운영적 고려사항**
- [ ] 모델 거버넌스: 누가 모델 승인/배포 권한을 가지는가?
- [ ] 규정 준수: AI 윤리, 편향성 검증, 설명 가능성 요구사항
- [ ] 비용 관리: GPU 비용, 스토리지 비용, 추론 API 비용

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: MLOps 없이 프로덕션 ML 배포**
- Jupyter Notebook에서 학습한 모델을 저장하여 API 서버에 직접 복사. 버전 관리 없음, 재현 불가능, 드리프트 감지 불가. 장애 시 원인 파악 불가.

**안티패턴 2: 지나친 자동화 (Level 2 섣부른 도입)**
- 초기 단계에서 자동 재학습 파이프라인을 구축하면, 잘못된 신호로 인해 불안정한 모델이 계속 배포될 수 있습니다. 먼저 수동 검증 프로세스를 확립한 후 자동화해야 합니다.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 수동 ML (AS-IS) | MLOps 적용 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **모델 배포 시간** | 주~월 단위 | 시간~일 단위 | **배포 속도 10배 향상** |
| **모델 프로덕션 도달률** | 13% | 80%+ | **성공률 6배 향상** |
| **드리프트 감지 시간** | 수동 분석 (주 단위) | 자동 감지 (실시간) | **대응 속도 100배 향상** |
| **재현 가능성** | 낮음 | 100% | **실험 재현 보장** |
| **운영 비용** | 높음 (수동 개입) | 낮음 (자동화) | **운영 효율성 50% 향상** |

### 2. 미래 전망 및 진화 방향
- **LLMOps (Large Language Model Ops)**: GPT-4, Claude와 같은 거대 언어 모델의 특성(Fine-tuning, RAG, Prompt Engineering, 토큰 비용)을 고려한 MLOps 확장이 활발히 연구되고 있습니다.
- **AI Platform Engineering**: MLOps가 발전하여 AI 플랫폼 엔지니어링으로 진화. 데이터 사이언티스트가 인프라를 몰라도 자동화된 플랫폼에서 모델을 개발/배포할 수 있는 셀프 서비스 환경.

### 3. 참고 표준/가이드
- **Google MLOps Guide**: MLOps 성숙도 모델 정의
- **MLflow Documentation**: 오픈소스 MLOps 플랫폼 표준
- **NIST AI Risk Management Framework**: AI 시스템 위험 관리 가이드

---

## 관련 개념 맵 (Knowledge Graph)
- **[DevOps](@/studynotes/15_devops_sre/1_sre/devops_culture.md)**: MLOps의 근간이 되는 원칙
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/3_automation/continuous_integration.md)**: 모델 배포 자동화
- **[DataOps](@/studynotes/15_devops_sre/1_sre/49_dataops.md)**: 데이터 파이프라인 자동화
- **[옵저버빌리티](@/studynotes/15_devops_sre/2_observability/observability_fundamentals.md)**: 모델 모니터링
- **[카나리 배포](@/studynotes/15_devops_sre/3_automation/deployment_strategies.md)**: 모델 점진적 배포

---

## 어린이를 위한 3줄 비유 설명
1. 요리사가 새로운 요리 레시피를 만들면, **주방에 자동으로 전달되어** 모든 손님에게 똑같이 맛있게 나가야 해요!
2. MLOps는 요리 레시피(ML 모델)를 주방에서 안전하게 만들고, 맛이 변하면 자동으로 다시 만들어주는 **요리 로봇 시스템**이에요.
3. 덕분에 요리사는 새로운 요리를 개발하는 것만 생각하면 되고, 맛없는 요리가 나가는 일이 없어져요!
