+++
weight = 123
title = "마이크로서비스 아키텍처 (MSA)"
date = "2024-03-20"
[extra]
categories = ["design-supervision", "architecture"]
+++

## 핵심 인사이트 (3줄 요약)
1. 시스템을 비즈니스 도메인 단위의 작고 독립적인 서비스로 분해하여 민첩성과 확장성을 극대화한 아키텍처입니다.
2. 각 서비스는 독립적인 DB와 배포 주기를 가지며, API(REST, gRPC)를 통해 상호 통신하는 느슨한 결합(Loose Coupling)을 지향합니다.
3. 분산 트랜잭션 처리(Saga)와 복잡한 운영 오케스트레이션(K8s)이 필수적으로 요구되는 '복잡성과의 트레이드 오프' 구조입니다.

### Ⅰ. 개요 (Context & Background)
마이크로서비스 아키텍처(Microservices Architecture, MSA)는 거대하고 단일화된 모놀리식(Monolithic) 시스템의 한계를 극복하기 위해 등장했습니다. 코드베이스가 커질수록 빌드/배포 시간이 기하급수적으로 증가하고, 작은 수정에도 전체 시스템을 재시작해야 하는 유연성 부족 문제를 해결합니다. 특히 클라우드 네이티브 환경에서 자원 효율성과 장애 격리(Fault Isolation)를 달성하기 위한 현대 소프트웨어 공학의 정수입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
[ Client Side ]        [ API Gateway Layer ]         [ Microservices Domain ]
+------------+         +-------------------+         +---------------------+
| Web/Mobile | ------> |  Authentication   | ------> | [Order Service]     |
|   App      |         |  Routing/Limits   |         |  (Order DB)         |
+------------+         +-------------------+         +----------|----------+
                               |                                | (Event)
                               v                                v
                       +-------------------+         +---------------------+
                       | Service Discovery | <-----> | [Payment Service]   |
                       | (Service Registry)|         |  (Payment DB)       |
                       +-------------------+         +---------------------+
```

**Bilingual Key Components:**
- **독립적 배포 (Independent Deployment):** 각 서비스는 상호 영향 없이 개별적으로 업데이트 가능합니다.
- **폴리글랏 퍼시스턴스 (Polyglot Persistence):** 서비스 특성에 맞춰 RDBMS, NoSQL 등 최적의 DB를 각각 선택합니다.
- **데브옵스 친화 (DevOps Friendly):** CI/CD 파이프라인 자동화와 컨테이너화(Docker/K8s)가 MSA의 근간이 됩니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 모놀리식 (Monolithic) | 마이크로서비스 (MSA) |
| :--- | :--- | :--- |
| **구조 (Structure)** | 단일 프로세스 내 모든 모듈 포함 | 독립적인 프로세스들의 분산 집합 |
| **데이터베이스** | 통합 DB (Shared DB) | 서비스별 개별 DB (Database per Service) |
| **확장성** | 시스템 전체 스케일 아웃 | 필요한 서비스만 선별적 확장 |
| **복잡도** | 초기 설계 단순, 유지보수 난해 | 설계 및 운영 복잡도 매우 높음 |
| **트랜잭션** | ACID (강한 일관성) | 결과적 일관성 (Eventual Consistency) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
기술사로서 MSA 도입 시 가장 경계해야 할 것은 '맹목적 추종'입니다. 서비스 간 네트워크 오버헤드와 분산 환경의 추적(Tracing) 난이도가 높기 때문입니다.
- **도입 전략:** 도메인 주도 설계(DDD)를 통해 바운디드 컨텍스트(Bounded Context)를 명확히 정의한 후, 핵심 도메인부터 점진적으로 분산하는 스트랭글러 피그(Strangler Fig) 패턴을 권장합니다.
- **감리 주안점:** 서비스 간 통신 보안(mTLS), 장애 전파 방지(Circuit Breaker), 그리고 분산 트랜잭션 실패 시의 보상 트랜잭션(Compensating Transaction) 로직 구현 여부를 집중 점검해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
MSA는 비즈니스의 빠른 변화에 즉각 대응할 수 있는 '민첩성(Agility)'을 제공합니다. 향후 플랫폼 비즈니스의 대형화와 AI 서비스 연계가 심화됨에 따라, 서버리스(Serverless)와 결합된 더욱 경량화된 MSA가 표준이 될 것입니다. 결론적으로 MSA는 단순한 기술적 선택이 아닌, 조직 구조와 개발 문화를 포함한 비즈니스 혁신의 도구입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 클라우드 네이티브 (Cloud Native), 분산 시스템 (Distributed Systems)
- **하위 개념:** API Gateway, Service Mesh, Saga Pattern, Sidecar Pattern
- **연관 개념:** DDD, Docker, Kubernetes, DevOps

### 👶 어린이를 위한 3줄 비유 설명
1. **모놀리식**은 모든 방이 하나로 합쳐진 거대한 텐트 같아요. 한 곳이 찢어지면 텐트 전체를 바꿔야 하죠.
2. **마이크로서비스**는 여러 개의 작은 레고 블록 방들이 모여 있는 마을 같아요. 주방 블록이 고장 나도 거실 블록은 멀쩡하답니다.
3. 블록들을 따로따로 고치거나 더 크게 만들 수 있어서 아주 편리해요!
