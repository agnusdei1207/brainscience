+++
weight = 124
title = "API 게이트웨이 (API Gateway)"
date = "2024-03-20"
[extra]
categories = ["design-supervision", "architecture", "msa"]
+++

## 핵심 인사이트 (3줄 요약)
1. 외부 클라이언트의 모든 요청을 한곳으로 모아 인증, 인가, 라우팅을 수행하는 마이크로서비스 아키텍처(MSA)의 '단일 진입점(Single Entry Point)'입니다.
2. 각 서비스의 복잡한 주소를 클라이언트에게 숨기고, 공통 기능(Cross-cutting Concerns)을 중앙에서 통합 처리하여 보안성과 관리 효율성을 높입니다.
3. 요청 통합(Aggregation), 프로토콜 변환, 부하 분산 등 지능형 프록시 역할을 수행하며 시스템의 추상화 계층을 제공합니다.

### Ⅰ. 개요 (Context & Background)
수백 개의 마이크로서비스가 존재하는 환경에서 클라이언트가 각 서비스의 엔드포인트를 직접 아는 것은 비효율적이며 보안에 취약합니다. API 게이트웨이(API Gateway)는 이러한 분산 환경의 무질서를 해결하기 위해 등장했습니다. 클라이언트와 백엔드 서비스 사이에서 통행을 통제하고, 다양한 기기(모바일, 웹, IoT)에 최적화된 응답을 제공하는 역할을 수행합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ Client Apps ]        [ API Gateway Layer ]         [ Backend Services ]
+------------+         +-------------------+         +---------------------+
| Web App    | ------> |  [ Request ]      | ------> | [ User Service ]    |
| Mobile App | <------ |  [ Response ]     | <------ | [ Product Service ] |
| IoT Device |         +---------|---------+         | [ Order Service ]   |
+------------+                   |                   +---------------------+
                                 v
                       +-------------------+
                       | [Common Functions]|
                       | - Auth / SSL / GZ |
                       | - Rate Limiting   |
                       | - Logging / Trace |
                       +-------------------+
```

**Bilingual Key Components:**
- **동적 라우팅 (Dynamic Routing):** 요청 URL 패턴에 따라 적절한 마이크로서비스로 트래픽을 전달합니다.
- **인증 및 인가 (Authentication & Authorization):** JWT 검증 등을 중앙에서 수행하여 백엔드 서비스의 부담을 줄입니다.
- **요청 통합 (Request Aggregation):** 여러 서비스의 데이터를 한 번의 호출로 모아서 응답하여 클라이언트의 지연 시간을 줄입니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | L4 로드밸런서 (Load Balancer) | API 게이트웨이 (API Gateway) |
| :--- | :--- | :--- |
| **작동 계층** | 전송 계층 (Layer 4) | 응용 계층 (Layer 7) |
| **주요 기능** | 단순 패킷 분산, IP/Port 기준 | 메시지 분석, 인증, 라우팅, 변환 |
| **지능화 정도** | 낮음 (H/W 중심) | 높음 (S/W 중심, 비즈니스 로직 연계) |
| **Synergy** | API 게이트웨이 앞단에서 부하 분산 | L4 뒤에서 세밀한 API 정책 통제 수행 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
실무에서 API 게이트웨이는 시스템 전체의 가용성을 좌우하는 '단일 장애점(SPOF)'이 될 수 있습니다.
- **아키텍처 설계 전략:** 게이트웨이 자체를 이중화/클러스터링하고, 특정 기기에 특화된 응답을 위해 **BFF(Backend For Frontend)** 패턴을 혼용하는 것이 기술사적 정석입니다.
- **감리 주안점:** 대규모 트래픽 발생 시 병목 현상이 생기지 않는지(Throughput), 서킷 브레이커와 연동하여 백엔드 장애를 차단하는지, 로그 수집 시 민감 정보가 마스킹되는지를 확인해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
API 게이트웨이는 MSA의 필수 요소로서 백엔드 개발자가 비즈니스 로직에만 집중할 수 있는 환경을 조성합니다. 클라우드 벤더의 관리형 서비스(AWS API Gateway 등)를 활용하여 운영 오버헤드를 줄이는 추세이며, 향후 서비스 메시(Service Mesh)와의 역할 분담을 통해 더욱 정교한 트래픽 제어 계층으로 진화할 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** MSA 아키텍처, 리버스 프록시 (Reverse Proxy)
- **하위 개념:** BFF (Backend For Frontend), Rate Limiting, Request Mapping
- **연관 개념:** JWT, OAuth 2.0, Service Discovery, Sidecar

### 👶 어린이를 위한 3줄 비유 설명
1. **API 게이트웨이**는 거대한 백화점의 '안내 데스크'와 같아요. 고객이 가고 싶은 매장을 하나하나 찾지 않아도 안내 데스크가 길을 가르쳐주죠.
2. 백화점에 들어오기 전에 가짜 손님인지 아닌지 검사하는 보안요원 역할도 한답니다.
3. 여러 매장의 물건을 한 바구니에 담아주는 역할도 해서 쇼핑이 아주 편해져요!
