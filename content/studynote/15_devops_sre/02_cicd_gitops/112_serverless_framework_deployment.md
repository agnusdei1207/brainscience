+++
weight = 112
title = "112. 서버리스 프레임워크 배포 (Serverless Framework Deployment)"
date = "2026-04-19"
[extra]
categories = "studynote-devops-sre"
+++

## 0. 핵심 인사이트

> **핵심**: Serverless Framework는 AWS Lambda·Azure Functions·GCP Cloud Functions 등 **FaaS(Function as a Service)의 인프라·코드·이벤트 트리거를 `serverless.yml` 하나로 선언**하고, `sls deploy` 한 줄로 클라우드에 배포하는 오픈소스 IaC(Infrastructure as Code) 도구다.
> **비유**: 수동 배포는 레고 설명서 없이 100조각을 맞추는 것이고, Serverless Framework는 설명서(YAML) 대로 로봇이 자동으로 조립하는 것이다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

FaaS는 서버 관리 없이 함수 단위로 코드를 실행하지만, 실제 배포 시에는 **IAM 정책·API Gateway 엔드포인트·DLQ(Dead Letter Queue)·VPC 설정·환경 변수** 등 수십 가지 인프라를 구성해야 한다.

```text
┌───────────────────────────────────────────────────────┐
│    수동 배포 vs Serverless Framework 배포               │
├───────────────────────────────────────────────────────┤
│  [수동 배포]                                          │
│   AWS 콘솔 → Lambda 생성 → IAM Role 설정             │
│   → API Gateway 연동 → CloudWatch 설정               │
│   → DLQ 연결 → 환경 변수 → (30분+)                   │
│                                                       │
│  [Serverless Framework]                               │
│   serverless.yml 작성 → sls deploy → 끝!             │
│   모든 리소스가 CloudFormation으로 자동 생성           │
│   (3분)                                               │
└───────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 목표 상태 | 구현해야 할 기준선 | 주제별 설계 원칙의 출발점 |
| 자동화 절차 | 반복 작업을 일관되게 수행 | 사람 의존도를 낮춤 |
| 검증·측정 | 결과가 맞는지 확인 | 품질과 신뢰성을 정량화 |

각 요소는 독립적으로 존재하는 것이 아니라, 정의된 목표 상태를 자동화 절차가 구현하고 검증 지표가 그 결과를 다시 피드백하는 폐쇄 루프를 이룰 때 가장 큰 효과를 낸다.

---

## 3. 구조 및 원리

**핵심 조건**: 모든 변경이 버전 관리되고, 자동 검증을 통과하며, 배포 상태와 롤백 경로가 추적 가능해야 한다.

동작 순서:
1. 코드와 배포 정의를 저장소에 커밋해 변경 이력을 단일 진실 공급원으로 만든다.
2. 빌드·테스트·보안 검사를 자동 수행해 배포 가능 아티팩트를 만든다.
3. 환경별 설정을 분리하면서도 동일한 파이프라인으로 일관성을 유지한다.
4. 배포 후 메트릭과 로그를 확인하고 이상 시 즉시 롤백하거나 다음 단계 승인을 중단한다.

```text
소스 변경
   ↓
CI 검증
   ↓
아티팩트 저장
   ↓
CD/GitOps 동기화
   ↓
운영 반영·롤백
```

```yaml
service: my-api
provider:
  name: aws
  runtime: nodejs20.x
  region: ap-northeast-2
functions:
  hello:
    handler: handler.hello
    events:
      - http:
          path: /hello
          method: get
    timeout: 10
    memorySize: 256
```

| 비교 | 수동 콘솔 | Serverless Framework |
|:---|:---|:---|
| **배포 시간** | 30분+ | **3분** |
| **재현성** | 수동 (실수 위험) | **YAML 선언, 100% 재현** |
| **버전 관리** | 불가 | **Git으로 IaC 이력 관리** |
| **롤백** | 수동 복원 | **sls rollback (자동)** |

---

## 4. 비교 및 연결

| 도구 | 멀티클라우드 | 언어 | 특징 |
|:---|:---|:---|:---|
| **Serverless Framework** | ✅ (AWS/Azure/GCP) | YAML | 범용, 플러그인 생태계 풍부 |
| **AWS SAM** | AWS 전용 | YAML | CloudFormation 네이티브 |
| **SST (v3)** | AWS 전용 | TypeScript | 타입 안전, 핫 리로드 |
| **Pulumi** | ✅ | 범용 언어 | 코드로 인프라 (TypeScript/Python) |

### CI/CD 통합 체크리스트
1. **GitHub Actions**: `on: push` → `sls deploy --stage prod`.
2. **스테이지 분리**: `--stage dev/staging/prod`로 환경별 독립 스택.
3. **Cold Start 최적화**: Provisioned Concurrency 또는 WarmUp 플러그인.
4. **모니터링**: Serverless Dashboard 또는 Datadog Lambda Layer.

### 안티패턴
- **단일 거대 함수**: Lambda 1개에 모든 로직 → 모놀리스 회귀. 함수별 단일 책임 원칙 준수.

---

## 5. 실무 적용 및 판단

| 지표 | 수동 배포 | Serverless Framework | 개선 |
|:---|:---|:---|:---|
| 배포 시간 | 30분+ | **3분** | 90% 단축 |
| 인프라 재현성 | 낮음 | **100%** | IaC 확보 |
| 운영 비용 | 인스턴스 상시 과금 | **요청당 과금** | 유휴 비용 0 |

Serverless Framework v4는 AI 기반 자동 최적화(메모리·타임아웃 자동 튜닝)를 내장하여, 함수 성능과 비용의 최적점을 자동으로 찾아주는 방향으로 진화하고 있다.

---

## 6. 기대효과 및 결론

서버리스 프레임워크 배포 (Serverless Framework Deployment)을(를) 도입하면 자동화와 표준화를 통해 속도·안정성·가시성의 균형을 높일 수 있다. 다만 효과를 얻으려면 모든 변경이 버전 관리되고, 자동 검증을 통과하며, 배포 상태와 롤백 경로가 추적 가능해야 한다는 전제가 충족되어야 하며, 도구만 도입하고 운영 원칙을 바꾸지 않으면 기대 효과가 빠르게 한계에 부딪힌다.

결론적으로 서버리스 프레임워크 배포 (Serverless Framework Deployment)은(는) 개별 기능이 아니라 운영 체계 전체의 품질을 재정렬하는 방식이며, 향후에는 플랫폼화·정책화·AI 기반 최적화와 결합해 더 높은 수준의 자동 운영으로 확장된다.

---

## 7. 발전 흐름도

```text
[AWS Lambda 출시 (2014) — FaaS 개념 탄생]
    │
    ▼
[Serverless Framework (2015) — FaaS IaC 자동화]
    │
    ▼
[AWS SAM (2016) — AWS 전용 FaaS 배포 도구]
    │
    ▼
[SST (2021~) — TypeScript 네이티브, 핫 리로드]
    │
    ▼
[현재: AI 기반 자동 튜닝 — 메모리·타임아웃 최적화 자동화]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **FaaS (Lambda)** | Serverless Framework가 배포하는 대상 |
| **IaC (Infrastructure as Code)** | YAML 선언으로 인프라를 코드화 |
| **CloudFormation** | AWS에서 YAML → 실제 리소스 생성 엔진 |
| **API Gateway** | Lambda 트리거, HTTP 엔드포인트 자동 생성 |
| **Cold Start** | FaaS 최초 실행 시 지연, 최적화 필수 |
