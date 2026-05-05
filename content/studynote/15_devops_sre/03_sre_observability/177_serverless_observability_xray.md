+++
weight = 177
title = "177. 서버리스 옵저버빌리티 (Serverless Observability)"
date = "2026-04-21"
[extra]
categories = "studynote-devops-sre"
+++

## 0. 핵심 인사이트

> **핵심**: FaaS(Function as a Service) 환경에서는 에이전트 상주 불가·짧은 생명주기·콜드 스타트라는 세 가지 제약이 전통적 관측 방법을 무력화한다.
> **비유**: 서버리스 관측은 마치 팝업 스토어 수천 곳을 동시에 모니터링하는 것 — 각 스토어가 잠깐 열렸다 닫히므로, 일반 CCTV(에이전트)를 설치할 수 없어 입장권(Trace ID)으로 모든 동선을 추적한다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

서버리스(Serverless) 아키텍처에서 함수(Function)는 요청마다 새 컨테이너에서 실행되고 수백 밀리초~수 초 만에 사라진다. 전통적 관측 도구는 장기 실행 프로세스에 에이전트(Agent)를 심어 메트릭을 지속 수집하는 방식인데, FaaS에서는 에이전트를 상주시킬 프로세스가 존재하지 않는다.

AWS Lambda 기준으로 함수는 이벤트 하나에 반응해 실행되며, 동시에 수천 개의 인스턴스가 병렬 실행될 수 있다. 이 수천 개의 짧은 실행 각각에서 발생하는 로그, 메트릭, 트레이스를 일관되게 수집·연결하지 못하면 "왜 이 요청이 느렸는지", "어떤 외부 호출에서 실패했는지" 전혀 알 수 없다.

AWS X-Ray는 이 문제를 해결하기 위해 Lambda 런타임에 내장된 추적 계층을 제공한다. X-Ray SDK를 함수 코드에 통합하거나 OpenTelemetry Lambda Layer를 추가하면 코드 변경 없이 자동 계측(Auto-Instrumentation)이 가능하다. 이를 통해 Lambda → DynamoDB → SNS → 외부 API 호출 체인 전체가 단일 Trace로 가시화된다.

서버리스 관측성의 핵심 과제는 세 가지다. 첫째 콜드 스타트(Cold Start) 지연 추적, 둘째 함수 간 호출 컨텍스트 전파, 셋째 비동기 이벤트 체인(SQS → Lambda → S3)에서의 Trace 연결이다. 이 세 가지를 해결해야 진정한 서버리스 관측성을 달성할 수 있다.

---

## 2. 구성요소

### AWS X-Ray 기반 서버리스 추적 흐름

```
클라이언트 요청
      │
      ▼
┌─────────────────────┐
│   API Gateway        │  ← X-Ray 트레이스 시작 (Root Segment)
│   (Trace Header 주입) │
└──────────┬──────────┘
           │  X-Amzn-Trace-Id 헤더 전파
           ▼
┌─────────────────────┐
│   AWS Lambda         │
│   ┌───────────────┐  │
│   │ OTel Layer    │  │  ← 자동 계측 Lambda Layer
│   │ (Auto-Instr.) │  │
│   └───────┬───────┘  │
│           │ Sub-Segment 생성         │
└───────────┼──────────┘
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
┌────────┐    ┌──────────────┐
│DynamoDB│    │  외부 HTTP API│  ← 각 호출이 Sub-Segment로 기록
└────────┘    └──────────────┘
    │                │
    └───────┬────────┘
            ▼
┌─────────────────────┐
│   X-Ray Service Map  │  ← 서비스 의존성 자동 시각화
│   + Trace Timeline  │
└─────────────────────┘
```

### 서버리스 관측 핵심 메트릭

| 메트릭 | 의미 | 임계값 기준 |
|:---|:---|:---|
| Cold Start Duration | Init Phase + Runtime Init 합산 | Java: <3s, Node.js: <500ms |
| Invocation Duration | 함수 실제 실행 시간 | P99 < SLO 기준 |
| Concurrent Executions | 동시 실행 함수 수 | 계정 한도(기본 1,000) 주의 |
| Throttles | 동시성 한도 초과 거부 횟수 | > 0 즉시 알람 |
| Error Rate | 4xx/5xx 비율 | SLO 기반 Error Budget |
| Iterator Age | Kinesis/SQS 이벤트 처리 지연 | < 1분 권장 |

### Lambda Layer 자동 계측 설정 예시

```yaml
functions:
  myFunction:
    handler: handler.main
    layers:
      - arn:aws:lambda:us-east-1:901920570463:layer:aws-otel-nodejs-amd64-ver-1-18-1:2
    environment:
      AWS_LAMBDA_EXEC_WRAPPER: /opt/otel-handler
      OPENTELEMETRY_COLLECTOR_CONFIG_FILE: /var/task/collector.yaml
```

---

## 3. 구조 및 원리

**핵심 조건**: 측정 가능한 SLI, 합의된 SLO, 실행 가능한 경보·복구 절차가 하나의 폐쇄 루프를 이뤄야 한다.

동작 순서:
1. 사용자 경험을 대표하는 지표를 선택해 서비스 상태를 수치화한다.
2. 허용 가능한 목표치와 에러 버짓을 정해 변화 속도와 안정성의 기준선을 만든다.
3. 메트릭·로그·트레이스로 이상 징후를 탐지하고 원인을 빠르게 국소화한다.
4. 장애 이후 포스트모템과 자동화를 통해 토일을 줄이고 재발 방지책을 시스템에 반영한다.

```text
서비스 요청
   ↓
측정(SLI)
   ↓
목표(SLO)·예산
   ↓
알림·복구
   ↓
학습·자동화
```

---

## 4. 비교 및 연결

| 항목 | 전통 APM (에이전트 기반) | 서버리스 관측 |
|:---|:---|:---|
| 에이전트 방식 | 장기 실행 프로세스에 상주 | Lambda Layer / SDK 통합 |
| 메트릭 수집 | Pull(Prometheus) / Push(StatsD) | CloudWatch EMF (Embedded Metric Format) |
| 트레이스 전파 | HTTP 헤더 + 에이전트 자동 주입 | X-Amzn-Trace-Id 헤더 수동/자동 |
| 비용 | 에이전트 오버헤드 (CPU/메모리) | 데이터 수집·전송 비용 |
| 비동기 연결 | 쉬움 (동일 프로세스) | 어려움 (SQS 메시지에 TraceId 내포 필요) |

| 도구 | 강점 | 약점 |
|:---|:---|:---|
| AWS X-Ray | Lambda 네이티브 통합, 서비스 맵 | AWS 종속적 |
| Datadog Serverless | 멀티 클라우드, 상세 프로파일링 | 비용 높음 |
| Lumigo | 서버리스 전문, 페이로드 추적 | 소규모 SaaS |
| OpenTelemetry | 벤더 중립, 표준화 | 초기 설정 복잡 |

### 콜드 스타트 감소 전략과 관측 연계

| 전략 | 관측 방법 | 효과 |
|:---|:---|:---|
| Provisioned Concurrency | `ProvisionedConcurrencyUtilization` 메트릭 | 콜드 스타트 제거 |
| 런타임 최적화 (Node.js → Rust) | Cold Start Duration 비교 트레이스 | 초기화 시간 단축 |
| 의존성 경량화 (Tree Shaking) | 배포 패키지 크기 모니터링 | Init Phase 단축 |
| VPC 배제 (필요 시만 VPC) | ENI 연결 시간 Sub-Segment 분석 | VPC 콜드 스타트 수백 ms 절약 |

---

## 5. 실무 적용 및 판단

- **비동기 트레이스 연결**: SQS 메시지 Body에 `traceId`를 JSON 필드로 포함시켜 Consumer Lambda에서 컨텍스트 복원
- **Cold Start SLO**: 사용자 요청 경로의 Lambda에는 Provisioned Concurrency, 배경 처리용 Lambda는 일반 실행으로 분리 관리
- **비용 최적화**: X-Ray 샘플링 비율을 운영(5%)과 개발(100%)로 분리하여 비용 통제

서버리스 관측 체계를 구축하면 "함수가 느린데 이유를 모름" 상태에서 벗어나 콜드 스타트, 외부 서비스 지연, 이벤트 처리 지연 각각의 원인을 정확히 진단할 수 있다. X-Ray Service Map은 수십 개 Lambda 함수 간 의존성을 자동으로 시각화하여 아키텍처 복잡도가 증가해도 전체 그림을 유지한다.

한계는 데이터 수집 비용이다. Lambda 호출 수가 수백만 건에 달하면 X-Ray 트레이스와 CloudWatch Logs 비용이 급증한다. 이를 제어하기 위해 샘플링 전략과 로그 레벨 조정이 반드시 병행되어야 한다.

미래 방향으로는 eBPF 기반 커널 레벨 계측이 FaaS 환경으로 확장되거나, AI가 함수 호출 패턴을 학습해 이상(Anomaly)을 자동 감지하는 AIOps와의 통합이 예상된다.

---

## 6. 기대효과 및 결론

서버리스 옵저버빌리티 (Serverless Observability)을(를) 도입하면 자동화와 표준화를 통해 속도·안정성·가시성의 균형을 높일 수 있다. 다만 효과를 얻으려면 측정 가능한 SLI, 합의된 SLO, 실행 가능한 경보·복구 절차가 하나의 폐쇄 루프를 이뤄야 한다는 전제가 충족되어야 하며, 도구만 도입하고 운영 원칙을 바꾸지 않으면 기대 효과가 빠르게 한계에 부딪힌다.

결론적으로 서버리스 옵저버빌리티 (Serverless Observability)은(는) 개별 기능이 아니라 운영 체계 전체의 품질을 재정렬하는 방식이며, 향후에는 플랫폼화·정책화·AI 기반 최적화와 결합해 더 높은 수준의 자동 운영으로 확장된다.

---

## 7. 발전 흐름도

```text
전통 운영 모니터링
    ↓
SRE 지표화
    ↓
옵저버빌리티 확장
    ↓
카오스·자동 복구
    ↓
AIOps·예측 운영
```

---

## 8. 관련 개념 맵

| 분류 | 관련 개념 |
|:---|:---|
| 상위 개념 | 분산 추적 (Distributed Tracing), 옵저버빌리티 (Observability) |
| 연관 기술 | AWS X-Ray, OpenTelemetry Lambda Layer, CloudWatch EMF, Datadog Serverless |
| 비교 대상 | 에이전트 기반 APM vs Layer 기반 서버리스 추적, Cold Start vs Warm Start |
