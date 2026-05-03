+++
weight = 151
title = "151. AWS Lambda, Google Cloud Functions, Azure Functions"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: AWS Lambda, Google Cloud Functions, Azure Functions는 3대 퍼블릭 클라우드의 대표 FaaS (Function as a Service) 서비스로, 모두 이벤트 기반 자동 확장·밀리초 과금을 지원하나 트리거 생태계·최대 실행 시간·런타임 지원이 다르다.
> 2. **가치**: 벤더별 FaaS를 정확히 비교·선택하면 기존 클라우드 인프라와의 통합 비용을 최소화하고 이벤트 소스 다양성을 극대화할 수 있다.
> 3. **판단 포인트**: 이미 AWS 생태계에 있으면 Lambda, GCP의 BigQuery·Pub/Sub 연동이 핵심이면 Cloud Functions, Azure DevOps·Active Directory 통합이 필요하면 Azure Functions가 최적이다.

---

## Ⅰ. 개요 및 필요성

서버리스가 주류가 되면서 3대 메이저 클라우드 벤더가 각각 독자 FaaS 서비스를 출시했다. 2014년 AWS Lambda가 최초 공개되었고, 이후 Google Cloud Functions(2016), Azure Functions(2016)이 뒤를 이었다. 세 서비스는 모두 "코드만 올리면 자동 실행" 원칙을 공유하지만, 런타임 지원 목록·최대 실행 시간·트리거 종류·VPC (Virtual Private Cloud) 통합 방식 등에서 차이를 보인다.

기업이 멀티클라우드 전략을 채택하거나, 기존 클라우드 마이그레이션을 계획할 때 벤더별 FaaS 특성을 정확히 이해하는 것은 아키텍처 결정의 핵심이다. 특히 콜드 스타트 성능, 메모리 설정 범위, 동시 실행 한도 (Concurrency Limit) 등은 SLA (Service Level Agreement) 달성 여부에 직결된다.

📢 **섹션 요약 비유**: 세 FaaS 서비스는 같은 자동차 택시지만 제조사가 달라 네비게이션(트리거)·연비(과금)·속도 제한(실행 시간)이 조금씩 다른 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | AWS Lambda | Google Cloud Functions | Azure Functions |
|:---|:---|:---|:---|
| 최초 출시 | 2014 | 2016 | 2016 |
| 최대 실행 시간 | 15분 | 9분 (Gen 2 기준 60분) | 10분 (소비 플랜), 무제한(전용 플랜) |
| 메모리 범위 | 128MB ~ 10,240MB | 128MB ~ 32,768MB | 동적 (소비량 기반) |
| 지원 런타임 | Node.js, Python, Java, Go, Ruby, .NET, 커스텀 | Node.js, Python, Go, Java, Ruby, PHP, .NET | Node.js, Python, Java, C#, F#, PowerShell |
| 주요 트리거 | API GW, S3, SQS, DynamoDB, SNS, EventBridge | HTTP, Pub/Sub, Cloud Storage, Firestore | HTTP, Event Grid, Service Bus, Blob, Timer |
| 과금 단위 | 요청 수 + GB-초 | 요청 수 + GHz-초 + 네트워크 | 요청 수 + GB-초 |
| 무료 한도 (월) | 100만 요청, 40만 GB-초 | 200만 호출, 40만 GB-초 | 100만 요청, 40만 GB-초 |
| VPC 통합 | VPC Lambda 지원 | VPC Connector 필요 | VNET Integration 지원 |

```text
┌────────────────────────────────────────────────────────────────────┐
│                  3대 FaaS 서비스 비교                              │
│                                                                    │
│  ┌──────────────┐    ┌──────────────────┐    ┌─────────────────┐  │
│  │  AWS Lambda  │    │ Cloud Functions  │    │ Azure Functions │  │
│  │              │    │   (Google)       │    │   (Microsoft)   │  │
│  │ ▶ S3/SQS 강점│    │ ▶ Pub/Sub/BQ 강점│    │ ▶ .NET/AAD 강점 │  │
│  │ ▶ 15분 한도  │    │ ▶ 60분 한도(Gen2)│    │ ▶ Durable 지원  │  │
│  │ ▶ 레이어 지원│    │ ▶ 자동 HTTPS     │    │ ▶ 바인딩 모델   │  │
│  └──────┬───────┘    └────────┬─────────┘    └────────┬────────┘  │
│         │                    │                        │           │
│         └────────────────────┴────────────────────────┘           │
│                    공통: 이벤트 트리거 → 자동 실행                 │
│                    공통: ms 과금 + 자동 수평 확장                  │
│                    공통: 상태 비저장 (Stateless)                   │
└────────────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 세 FaaS는 삼성·애플·LG 스마트폰 — 앱(코드) 실행은 다 되지만, 생태계(SDK, 연동 서비스)는 제조사마다 강점이 다르다.

---

## Ⅲ. 비교 및 연결

| 구분 | AWS Lambda | Azure Functions (Durable) |
|:---|:---|:---|
| 장기 워크플로우 | Step Functions 별도 서비스 | Durable Functions 내장 |
| 로컬 개발 경험 | SAM CLI / CDK | Azure Functions Core Tools |
| 오케스트레이션 | EventBridge Pipes | Logic Apps 통합 |
| 에지 실행 | Lambda@Edge (CloudFront) | Azure Static Web Apps |

**Azure Durable Functions** 특징: 상태를 유지하며 워크플로우를 구성할 수 있어 일반 서버리스 제약(무상태)을 일부 극복한다. Orchestrator Function이 Activity Function들을 순차·병렬 조율한다.

📢 **섹션 요약 비유**: Durable Functions는 서버리스 세계의 지휘자 — 무상태 단독 악기(함수)들을 오케스트라로 묶어 장기 연주(워크플로우)를 가능하게 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**벤더 선택 기준**
1. **기존 클라우드 스택**: AWS 중심 → Lambda + EventBridge; GCP 중심 → Cloud Functions + Pub/Sub
2. **엔터프라이즈 AAD 연동**: Azure Functions + Managed Identity 조합
3. **장기 실행 필요**: Azure Durable Functions 또는 Google Cloud Run (컨테이너)
4. **멀티클라우드·벤더 락인 회피**: Knative 기반 오픈소스 FaaS 검토

**공통 모범 사례**
- 함수 패키지 크기 최소화 → 콜드 스타트 감소
- 환경 변수·Secrets Manager로 설정 외부화 (12-Factor App 원칙)
- 멱등성 (Idempotency) 보장 → 중복 호출 안전 처리
- Dead Letter Queue (DLQ) 설정 → 실패 이벤트 재처리

📢 **섹션 요약 비유**: 벤더 선택은 통신사 선택과 같다 — 가족이 모두 같은 통신사면 묶음 할인(생태계 통합 이점)을 받을 수 있다.

---

## Ⅴ. 기대효과 및 결론

3대 FaaS 서비스는 각자의 클라우드 생태계 깊이 통합되어 있어, 해당 벤더의 다른 서비스와 함께 사용할 때 가장 강력한 시너지를 발휘한다. AWS Lambda는 방대한 트리거 생태계와 Layer(공유 라이브러리) 기능, Google Cloud Functions는 Pub/Sub·BigQuery와의 데이터 파이프라인 통합, Azure Functions는 .NET 개발자 경험과 Durable 워크플로우가 강점이다.

멀티클라우드 환경에서는 Knative나 OpenFaaS를 이용해 특정 벤더 API에 종속되지 않는 이식 가능한 FaaS 아키텍처를 구성하는 것이 장기적으로 유리하다.

📢 **섹션 요약 비유**: 3대 FaaS는 각자 최강 홈구장을 가진 스포츠 팀 — 자기 구장(생태계)에서는 압도적이지만 원정(멀티클라우드)에서는 중립 도구(Knative)가 필요하다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| AWS Lambda | 최초 상용 FaaS, 가장 넓은 트리거 생태계 |
| Google Cloud Functions | GCP 데이터 파이프라인 (Pub/Sub, BigQuery) 통합 |
| Azure Functions | .NET·AAD 통합, Durable Functions 워크플로우 |
| Knative | 오픈소스 FaaS, 벤더 락인 탈출 대안 |
| 콜드 스타트 (Cold Start) | 3개 벤더 공통 해결 과제 |
| API Gateway | HTTP 트리거 공통 진입점 |

### 👶 어린이를 위한 3줄 비유 설명
1. Lambda, Cloud Functions, Azure Functions는 세 나라의 자동 로봇 공장이에요 — 일(코드)을 시키면 알아서 기계를 켜고 만들어 준다는 건 같아요.

### 📈 관련 키워드 및 발전 흐름도

```text
각 CSP의 FaaS 구현
    ├─► AWS Lambda: 가장 오래된 · 생태계 최대
    ├─► GCP Cloud Functions: GCP 통합 · gen2
    └─► Azure Functions: Durable Functions 확장
    │
    ▼
통합 이식: Knative · OpenFaaS (멀티클라우드)
```
2. 하지만 어느 나라 부품(다른 클라우드 서비스)을 쓰느냐에 따라 어울리는 공장이 달라요.
3. 나라를 바꾸고 싶다면 Knative라는 '만국 공통 설계도'를 쓰면 어느 나라 공장에서도 똑같이 만들 수 있어요.
