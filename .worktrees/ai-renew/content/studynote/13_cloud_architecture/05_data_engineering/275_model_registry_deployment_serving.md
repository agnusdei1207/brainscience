+++
weight = 275
title = "275. 모델 레지스트리 / 서빙 (Model Registry & Serving)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 모델 레지스트리(Model Registry)는 ML 모델의 버전·메타데이터·상태(Staging/Production/Archived)를 중앙 관리하는 Git 같은 저장소이고, 모델 서빙(Model Serving)은 이 모델을 REST API 또는 gRPC로 실시간 추론 서비스로 제공하는 인프라다.
> 2. **가치**: 모델 레지스트리 없이는 "지금 프로덕션에서 어떤 버전의 모델이 돌고 있는가?"를 파악하기 어렵고, 성능 저하 시 이전 버전으로의 즉각적 롤백이 불가능하다 — 모델도 소프트웨어처럼 버전 관리와 배포 파이프라인이 필요하다.
> 3. **판단 포인트**: GPU 추론 최적화(Triton + TensorRT), Canary/Shadow 배포, A/B 테스트 3가지가 안전한 모델 배포의 핵심 — 특히 금융·의료 분야에서는 추론 결과의 설명 가능성(XAI)과 감사 로그가 규제 요건으로 추가된다.

---

## Ⅰ. 개요 및 필요성

모델 레지스트리와 서빙 인프라가 없는 조직의 현실: 여러 버전의 모델 파일이 S3 버킷에 날짜별로 저장되어 있고, 어떤 모델이 프로덕션에서 실행 중인지, 왜 그 모델을 선택했는지 아무도 모른다. 성능 문제가 발생해도 롤백할 방법이 없다.

```
[모델 레지스트리 상태 전환]

실험 → 스테이징 → 프로덕션 → 아카이브

None ──▶ Staging ──▶ Production ──▶ Archived
         │              │
    (검증 통과)   (새 모델로 교체 또는
                 성능 저하 시 아카이브)
         │
    (검증 실패) ──▶ None (등록 취소)
```

📢 **섹션 요약 비유**: 모델 레지스트리는 의약품 승인 시스템이다. 신약(새 모델)은 임상 시험(Staging 검증)을 통과해야 시판(Production 배포)할 수 있고, 모든 이력이 기록되어 부작용 발생 시 즉시 회수(롤백)할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### MLflow Model Registry 워크플로우

```python
import mlflow

# 실험 완료 후 모델 등록
with mlflow.start_run():
    # 훈련 및 메트릭 기록
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("f1_score", 0.92)

    # 모델 저장 및 레지스트리에 등록
    mlflow.sklearn.log_model(
        model,
        artifact_path="fraud_model",
        registered_model_name="FraudDetector"
    )

# 스테이징으로 전환
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="FraudDetector",
    version=3,
    stage="Staging"
)

# 검증 통과 후 프로덕션으로 전환
client.transition_model_version_stage(
    name="FraudDetector",
    version=3,
    stage="Production"
)

# 이전 프로덕션 버전 아카이브
client.transition_model_version_stage(
    name="FraudDetector",
    version=2,
    stage="Archived"
)
```

### 모델 서빙 아키텍처

```
[모델 서빙 계층 구조]

클라이언트 요청
      │
      ▼
API Gateway (Rate Limiting, 인증)
      │
      ▼
Model Serving Layer
┌─────────────────────────────────────────┐
│  Triton Inference Server                │
│  ┌──────────────┐ ┌──────────────────┐ │
│  │ Model A v3  │ │  Model B v2      │ │
│  │ (TensorRT)  │ │  (ONNX Runtime)  │ │
│  └──────────────┘ └──────────────────┘ │
│  Dynamic Batching (처리량 최적화)        │
│  GPU 메모리 풀링                         │
└─────────────────────────────────────────┘
      │
      ▼
Feature Store (실시간 Feature 조회)
      │
      ▼
추론 결과 + 설명 (XAI)
```

### Canary 배포 및 A/B 테스트

```
[안전한 모델 배포 전략]

Shadow 배포 (위험도 최소):
실제 트래픽 ──▶ 현재 모델 v2 (서비스 응답)
                   │
              병렬 실행 (응답 미사용)
                   ▼
           신규 모델 v3 (결과 로깅만)
→ 실트래픽에서 v3 성능 검증, 사용자 영향 없음

Canary 배포:
트래픽의 5% ──▶ 신규 모델 v3
트래픽의 95% ──▶ 현재 모델 v2
→ 점진적으로 v3 비율 증가
→ 문제 발생 시 즉시 v2로 100% 복구

A/B 테스트:
그룹 A (50%) ──▶ 모델 v2
그룹 B (50%) ──▶ 모델 v3
→ 통계적 유의성 확인 후 전환
```

📢 **섹션 요약 비유**: Canary 배포는 탄광의 카나리아 새다. 위험한 광산에 새를 먼저 보내 독가스가 있으면 새가 먼저 죽는다. 신규 모델을 5% 트래픽에 먼저 노출하여 문제를 조기 발견하고, 안전하면 나머지 95%로 확대한다.

---

## Ⅲ. 비교 및 연결

### 모델 서빙 도구 비교

| 도구 | 최적화 | 지원 프레임워크 | 특징 |
|:---|:---|:---|:---|
| **TF Serving** | TensorFlow 전용 | TensorFlow/Keras | 안정적, TF 생태계 |
| **Triton Inference Server** | GPU 최적화 | TF, PyTorch, ONNX, TensorRT | 멀티 모델, 동적 배치 |
| **TorchServe** | PyTorch 전용 | PyTorch | 간단한 설정 |
| **ONNX Runtime** | CPU/GPU 최적화 | 다수 (ONNX 포맷) | 크로스 플랫폼 |
| **BentoML** | 범용 | 모든 프레임워크 | Python 친화적 |
| **KServe** | K8s 통합 | 다수 | K8s 네이티브 MLOps |

### SLA 기반 서빙 최적화

| 지연 요건 | 최적화 전략 | 도구 |
|:---|:---|:---|
| < 10ms (초실시간) | TensorRT 양자화, GPU 배치 | Triton + TensorRT |
| 10~100ms (실시간) | ONNX 최적화, 배치 추론 | ONNX Runtime |
| 100ms~1s (준실시간) | 일반 모델 서빙 | TF Serving, TorchServe |
| > 1s (배치) | 대용량 배치 추론 | Spark ML, SageMaker Batch |

📢 **섹션 요약 비유**: 서빙 최적화는 패스트푸드 주문 처리와 같다. 주문이 몰리면 같은 종류 주문을 묶어서(동적 배치) 처리하고, 미리 반조리된 재료(양자화된 모델)로 만들면 1개씩 개별 조리보다 훨씬 빠르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 모델 서빙 API 예시

```python
# BentoML: 모델 서빙 API 정의
import bentoml
from bentoml.io import JSON, NumpyNdarray

# 레지스트리에서 모델 로드
fraud_model = bentoml.sklearn.get("fraud_detector:production")
fraud_runner = fraud_model.to_runner()

svc = bentoml.Service("fraud_detection_svc", runners=[fraud_runner])

@svc.api(input=JSON(), output=JSON())
def predict(input_data: dict) -> dict:
    features = preprocess(input_data)
    score = fraud_runner.predict.run(features)
    return {
        "fraud_probability": float(score[0]),
        "decision": "fraud" if score[0] > 0.7 else "normal",
        "model_version": fraud_model.info.version
    }
```

### 모델 성능 모니터링 지표

| 지표 | 설명 | 알림 기준 |
|:---|:---|:---|
| **Precision/Recall** | 사기 탐지 정확도 | 기준치 대비 5% 하락 |
| **P99 추론 지연** | 99th 백분위 응답 시간 | SLA 초과 |
| **예측 분포** | 모델 출력 점수 분포 | PSI > 0.2 |
| **Feature 드리프트** | 입력 Feature 분포 변화 | PSI > 0.1 |
| **처리량(TPS)** | 초당 추론 요청 수 | 이상 급증/급감 |

### 기술사 시험 판단 포인트

- **레지스트리 상태 관리**: None → Staging → Production → Archived 4단계 명확히 서술
- **Canary vs A/B 테스트 차이**: Canary는 점진적 트래픽 전환(위험 최소화), A/B는 통계적 비교(성능 검증)
- **GPU 추론 최적화**: TensorRT 양자화(INT8) + 동적 배치 = 처리량 수십 배 향상

📢 **섹션 요약 비유**: 모델 레지스트리 없는 ML 서비스는 약국에 성분표 없는 약이 있는 것이다. 어떤 성분(코드·데이터)으로 만들어졌는지, 언제 검증받았는지 모르면 안전하게 처방(배포)할 수 없다. 레지스트리는 모든 약의 성분표·유통기한·승인 이력을 관리하는 시스템이다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 영역 | 효과 |
|:---|:---|
| **안전한 배포** | Canary/Shadow 배포로 신규 모델 위험 최소화 |
| **즉각 롤백** | 레지스트리에서 이전 버전 즉시 복구 |
| **성능 유지** | 지속 모니터링으로 드리프트 조기 탐지 |
| **규제 준수** | 모델 버전·결정 근거 감사 로그 자동 기록 |

### 한계 및 주의사항

- **서빙 인프라 비용**: GPU 기반 서빙 인프라는 고비용 → 배치 추론 vs 실시간 서빙 선택 중요
- **모델 로딩 시간**: 대형 모델(LLM)은 수십 초~수 분의 로딩 시간 → 사전 로딩·Warm Pool 필요
- **버전 관리 복잡성**: 모델 + 코드 + 데이터 + Feature의 버전이 모두 맞아야 재현성 보장
- **레이턴시 요건**: 10ms 이하 요건은 GPU + TensorRT + 동적 배치로도 달성 어려운 경우 있음

📢 **섹션 요약 비유**: 완벽한 모델 서빙 인프라는 최신 공항 시스템이다. 비행기(모델)가 제시간에 이·착륙하려면 활주로(GPU 서버), 관제탑(레지스트리), 비상 대응(롤백), 승객 안전(모니터링)이 모두 필요하다. 어느 하나라도 부족하면 지연이나 사고가 난다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| MLflow Registry | 오픈소스 모델 레지스트리 |
| Triton Inference Server | NVIDIA GPU 최적화 멀티 모델 서빙 |
| TensorRT | GPU 추론 최적화 (양자화, 레이어 병합) |
| Canary 배포 | 점진적 모델 트래픽 전환 |
| A/B 테스트 | 통계적 모델 성능 비교 |
| KServe | K8s 네이티브 ML 서빙 프레임워크 |

### 👶 어린이를 위한 3줄 비유 설명
1. 모델 레지스트리는 AI의 이력서 보관함이야. v1, v2, v3 이력서가 보관되어 있고, 지금 일하는 버전이 어디 있는지 바로 알 수 있어.
2. Canary 배포는 새 메뉴를 식당 한 테이블에서만 먼저 테스트하는 거야. 손님들 반응이 좋으면 전체 메뉴로 확대하고, 나쁘면 즉시 원래 메뉴로 돌아가.
3. TensorRT는 요리를 반조리 상태로 미리 준비해두는 거야. 주문이 들어오면 마저 완성만 하면 되니까 훨씬 빠르게 나올 수 있어!
