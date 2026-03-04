+++
title = "Software Quality Attributes (ISO/IEC 25010)"
description = "소프트웨어 품질 관리의 핵심 지표이자 평가 기준이 되는 ISO/IEC 25010 표준을 다각도로 분석하고, 아키텍처 의사결정 시 반영되는 품질 속성들의 상충 관계(Trade-off)와 이를 극복하는 전략적 접근법을 심층 조명합니다."
date = 2024-03-24
[taxonomies]
tags = ["software_engineering", "quality_management", "iso_25010", "architecture", "trade_off", "performance", "security", "reliability"]
categories = ["studynotes-04_software_engineering"]
+++

# 소프트웨어 품질 속성 (Software Quality Attributes: ISO/IEC 25010)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 시스템이 이해관계자의 명시적/암묵적 요구를 얼마나 만족시키는가를 정량적, 정성적으로 평가하는 다차원적 품질 평가 모델의 국제 표준입니다.
> 2. **가치**: 아키텍처 설계 시 기능적 요구사항(Functional Requirements)을 넘어, 시스템의 지속 가능성과 생존을 결정짓는 비기능적 요구사항(NFR)의 측정 및 검증 기준을 제공합니다.
> 3. **융합**: 고가용성 설계, 무중단 배포(DevOps), 분산 데이터베이스(CAP 정리), 제로 트러스트 보안 모델 등 현대 시스템 아키텍처의 모든 영역과 직결되는 기초 뼈대입니다.

---

## Ⅰ. 개요 (Context & Background)

소프트웨어 품질 속성(Software Quality Attributes)은 시스템이 제공하는 기능이 '어떻게' 수행되어야 하는지 규정하는 비기능적 요구사항(Non-Functional Requirements)의 집합입니다. 과거 기능 위주의 개발 시대에서는 버그가 없는 상태만을 품질로 여겼으나, 현대의 복잡한 분산 환경에서는 확장성, 가용성, 보안성 등의 품질 속성이 비즈니스의 성패를 직접적으로 가릅니다. ISO/IEC 25010 (SQuaRE)은 기존 ISO/IEC 9126을 계승하여 클라우드, 모바일, MSA 환경에 부합하도록 제품 품질(Product Quality)과 사용시 품질(Quality in Use)을 체계적으로 분류한 국제 표준입니다.

**💡 일상생활 비유: 고성능 스포츠카의 품질**
소프트웨어를 스포츠카에 비유해보겠습니다. '달리고 멈춘다'는 것은 기능(Function)입니다. 그러나 '얼마나 빨리 0에서 100km/h에 도달하는가'(성능 효율성), '충돌 시 탑승자를 얼마나 안전하게 보호하는가'(신뢰성 및 보안성), '부품 교체가 얼마나 쉬운가'(유지보수성), '다른 브랜드의 타이어와 호환되는가'(호환성)는 품질 속성입니다. 고객이 수억 원을 지불하는 이유는 기능 때문이 아니라 압도적인 품질 속성 때문입니다.

**등장 배경 및 발전 과정**
1. **모놀리틱 아키텍처의 한계**: 과거 단일 서버 환경에서는 기능 구현 자체에 급급하였으며, 시스템 규모가 커짐에 따라 스파게티 코드, 메모리 누수, 유지보수 불가라는 치명적 한계에 봉착했습니다.
2. **비기능적 요구사항의 대두**: 대규모 분산 환경과 MSA(Microservices Architecture)가 도래하면서, 네트워크 지연(Latency), 장애 전파(Cascading Failure), 데이터 정합성 문제 등이 발생했고, 이를 체계적으로 제어할 기준이 필요해졌습니다.
3. **표준화의 요구**: ISO/IEC 9126의 한계(보안, 호환성 분리 부족)를 극복하기 위해 ISO/IEC 25010이 제정되었으며, 현재는 소프트웨어 아키텍처 평가 방법론(ATAM, CBAM)의 핵심 평가 기준이자 감리/감사의 법적, 기술적 근거로 강제되고 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

ISO/IEC 25010의 '제품 품질(Product Quality)' 모델은 8개의 주특성(Characteristics)과 31개의 부특성(Sub-characteristics)으로 구성됩니다. 이는 아키텍처 설계 시 각 컴포넌트가 달성해야 할 목표치를 명세합니다.

### 1. 제품 품질 8대 주특성 구성 요소

| 요소명 (Characteristic) | 상세 역할 및 하위 특성 | 내부 동작 및 평가 메커니즘 | 관련 프로토콜/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **기능 적합성** (Functional Suitability) | 요구된 기능을 정확하고 적절하게 제공하는가? (완전성, 정확성, 적절성) | 테스트 케이스 커버리지, 경계값 분석, 동등 분할을 통한 검증 | TDD, BDD, JUnit | 자동차의 엑셀과 브레이크 작동 |
| **성능 효율성** (Performance Efficiency) | 할당된 자원 대비 응답 시간, 처리량은 적절한가? (시간 효율성, 자원 활용성, 용량) | APM(Application Performance Monitoring), 프로파일링, 로드 밸런싱 | JMeter, Redis Cache, CDN | 스포츠카의 연비와 가속력 |
| **호환성** (Compatibility) | 다른 시스템/환경과 정보 교환 및 공존이 가능한가? (공존성, 상호운용성) | API 규격 검증, 프로토콜 변환, 컨테이너 격리(Docker) | REST, gRPC, OAuth 2.0 | 다양한 충전 규격을 지원하는 포트 |
| **사용성** (Usability) | 사용자가 이해하고 배우고 사용하기 쉬운가? (학습성, 조작성, 오류 방지, 접근성 등) | A/B 테스트, 사용자 행동 분석, 휴리스틱 평가 | WCAG, React, UI/UX 패턴 | 직관적인 인포테인먼트 UI |
| **신뢰성** (Reliability) | 명시된 조건에서 특정 기간 동안 기능을 유지하는가? (성숙성, 가용성, 결함 허용성, 복구력) | 카오스 엔지니어링, 다중화(Active-Active), Circuit Breaker | Kubernetes, Chaos Monkey | 펑크가 나도 달릴 수 있는 런플랫 타이어 |
| **보안성** (Security) | 정보와 데이터를 보호하고 권한을 통제하는가? (기밀성, 무결성, 부인 방지, 책임성, 인증성) | 암호화 알고리즘, IAM 적용, 침투 테스트 | TLS 1.3, JWT, RBAC | 스마트키 암호화 및 도난 방지 시스템 |
| **유지보수성** (Maintainability) | 수정, 개선, 적응을 효율적으로 할 수 있는가? (모듈성, 재사용성, 분석성, 변경성, 테스트성) | 정적 코드 분석, 의존성 역전, 결합도/응집도 평가 | SonarQube, Design Patterns | 부품 교체가 쉬운 모듈형 엔진룸 |
| **이식성** (Portability) | 한 환경에서 다른 환경으로 이전하기 쉬운가? (적응성, 설치성, 대체성) | 크로스 플랫폼 빌드, 환경 설정 분리(12-Factor App) | Docker, JVM, WAS | 가솔린에서 전기차로 변환 가능한 섀시 |

### 2. 품질 속성 트리 및 아키텍처 다이어그램 (ATAM 관점)

소프트웨어 아키텍처는 이러한 품질 속성들을 달성하기 위해 다양한 전술(Tactics)을 조합하여 설계됩니다. 아래는 신뢰성, 성능 효율성, 보안성을 달성하기 위한 클라우드 네이티브 아키텍처의 품질 속성 전개 구조입니다.

```text
+---------------------------------------------------------------------------------------------------+
|                        [ISO/IEC 25010 Quality Attribute Architecture]                             |
+---------------------------------------------------------------------------------------------------+
|   [Client Layer]     |                      [Security: TLS 1.3, WAF]                              |
|   Web / Mobile       |-->   [Usability] Responsive UI, [Compatibility] Cross-browser              |
+----------------------+----------------------------------------------------------------------------+
|        |                                                                                          |
|        V (Rate Limiting, JWT Auth)                                                                |
+----------------------+----------------------------------------------------------------------------+
|   [API Gateway]      |  [Security] Authentication (JWT), Authorization (RBAC)                     |
|   (Kong / APIGW)     |  [Performance] Rate Limiting, Response Caching (Redis)                     |
+----------------------+----------------------------------------------------------------------------+
|        |                                                                                          |
|        V (gRPC/REST)    +--> [Service B] (User)   --+                                             |
+----------------------+  |                           |                                             |
|   [Service Mesh]     |--+--> [Service C] (Order)  --+--> [Reliability] Circuit Breaker, Retries   |
|   (Istio / Linkerd)  |  |                           |    [Maintainability] Modularity (Microservices)
|                      |--+--> [Service D] (Pay)    --+                                             |
+----------------------+----------------------------------------------------------------------------+
|        |                                                                                          |
|        V (Async Events)                                                                           |
+----------------------+----------------------------------------------------------------------------+
|   [Message Broker]   |  [Reliability] Fault Tolerance, Async Decoupling                           |
|   (Kafka / RabbitMQ) |  [Performance] Burst Traffic Handling (Buffering)                          |
+----------------------+----------------------------------------------------------------------------+
|        |                                                                                          |
|        V (Data Access)                                                                            |
+----------------------+----------------------------------------------------------------------------+
|   [Data Storage]     |  [Reliability] Active-Active Replication, [Performance] Sharding           |
|  (PostgreSQL, Redis) |  [Security] Data at Rest Encryption (AES-256)                              |
+---------------------------------------------------------------------------------------------------+
```

### 3. 심층 동작 원리 및 아키텍처 전술 (Architecture Tactics)

품질 속성을 시스템에 내재화하기 위해 아키텍트는 구체적인 **전술(Tactics)**을 사용합니다.
1. **신뢰성(결함 허용성) 달성 메커니즘**: 
   - ① 모니터링 에이전트가 서비스 응답 지연을 감지 (Timeout 발생).
   - ② 서킷 브레이커(Circuit Breaker) 패턴 발동 (상태를 Open으로 전환하여 후속 요청을 즉시 차단, 장애 전파 방지).
   - ③ Fallback 로직 실행 (캐시된 이전 데이터 반환 또는 기본 응답 제공).
   - ④ 일정 시간(Sleep Window) 후 Half-Open 상태로 전환하여 서비스 정상화 여부 테스트 (Ping).
   - ⑤ 정상 응답 확인 시 Closed 상태로 복귀하여 정상 라우팅 재개.
2. **성능 효율성 달성 로직**:
   - 데이터베이스 병목을 막기 위해 조회 쿼리(Read)와 쓰기/수정(Write) 트랜잭션을 분리하는 CQRS 패턴 및 Read-Replica 아키텍처를 도입합니다.
   - 캐싱 전략(Cache-Aside, Write-Through)을 사용하여 I/O 대기 시간을 최소화합니다.

### 4. 핵심 알고리즘 및 실무 코드 (서킷 브레이커 구현 예시)

신뢰성(Reliability) 중 결함 허용성을 구현하는 Java (Resilience4j) 기반 서킷 브레이커 설정 스니펫입니다.

```java
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig;
import java.time.Duration;

// 신뢰성(Reliability) 확보를 위한 Circuit Breaker 설정
CircuitBreakerConfig circuitBreakerConfig = CircuitBreakerConfig.custom()
    .failureRateThreshold(50) // 실패율 50% 이상 시 Open (에러 감지)
    .slowCallRateThreshold(50) // 느린 호출 50% 이상 시 Open (성능 저하 감지)
    .waitDurationInOpenState(Duration.ofMillis(1000)) // Open 상태 유지 시간 (1초 대기)
    .slowCallDurationThreshold(Duration.ofSeconds(2)) // 2초 이상 지연을 느린 호출로 간주
    .permittedNumberOfCallsInHalfOpenState(3) // Half-Open 상태에서 허용할 테스트 호출 수
    .minimumNumberOfCalls(10) // 실패율 계산을 위한 최소 호출 횟수
    .build();

CircuitBreaker circuitBreaker = CircuitBreaker.of("backendService", circuitBreakerConfig);

// 실제 서비스 호출에 데코레이터 적용
Supplier<String> restrictedSupplier = CircuitBreaker
    .decorateSupplier(circuitBreaker, () -> backendService.doSomething());

// 예외 시 Fallback 처리 (장애 허용성 보장)
Try.ofSupplier(restrictedSupplier)
    .recover(throwable -> "Fallback Data: " + throwable.getMessage())
    .get();
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 품질 속성 간의 Trade-off (상충 관계) 분석표

아키텍처 설계의 본질은 무한한 자원 하에서 완벽을 기하는 것이 아니라, 제한된 제약 사항 속에서 품질 속성 간의 **트레이드오프(Trade-off)**를 조율하는 것입니다.

| 상충되는 속성 A (목표) | 상충되는 속성 B (희생) | 발생 원인 및 아키텍처적 딜레마 | 해결 전략 (Mitigation) |
| :--- | :--- | :--- | :--- |
| **보안성 (Security)** | **성능 (Performance)** | 복잡한 암호화 알고리즘(AES, RSA), 무결성 해시 계산, 패킷 딥 인스펙션은 막대한 CPU 자원과 연산 지연을 초래함. | 하드웨어 가속(SSL Offloading), 비대칭 키 교환 후 대칭 키 통신, Edge 보안 계층 위임. |
| **신뢰성/가용성** | **성능 (Performance)** | 장애를 대비한 데이터 다중 복제(Replication), 정합성 검증 프로세스, 분산 락 메커니즘이 응답 시간을 크게 늘림. | 비동기 복제, 최종적 일관성(Eventual Consistency) 모델 도입, 중요도에 따른 다이어링(Tiering). |
| **유지보수성** | **성능 (Performance)** | 모듈화, 추상화 계층화, 객체 지향적 디자인 패턴의 과도한 사용은 함수 호출 스택을 깊게 만들고 메모리 오버헤드를 유발. | 성능에 민감한 Core 모듈은 인라인 최적화, 저수준 언어(Rust/C++) 사용, JIT 컴파일러 활용. |
| **보안성 (Security)** | **사용성 (Usability)** | 2FA/MFA, 복잡한 비밀번호 규칙, 잦은 세션 만료 정책은 사용자의 피로도를 높이고 이탈률을 증가시킴. | FIDO, 생체 인증(Biometrics), 위험 기반 인증(Risk-Based Authentication), SSO(Single Sign-On). |

### 2. 과목 융합 관점 분석
- **OS 및 인프라**: 이식성(Portability)과 신뢰성(Reliability)은 OS 수준의 컨테이너 기술(Docker), 리소스 격리(cgroups, namespaces), 그리고 쿠버네티스의 오토스케일링 및 Self-healing 메커니즘을 통해 극대화됩니다.
- **분산 데이터베이스**: 신뢰성과 성능 효율성의 트레이드오프는 분산 시스템의 **CAP 정리(Consistency, Availability, Partition Tolerance)**와 직결됩니다. 데이터베이스 설계 시 완벽한 일관성(C)을 유지하면 가용성(A)과 성능이 희생되는 구조적 문제를 안고 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)
- **시나리오 A: 금융권 차세대 시스템 구축 (보안성과 신뢰성 최우선)**
  - **문제**: 기존 모놀리틱 시스템의 잦은 장애와 느린 유지보수 속도로 인해 MSA 전환을 추진하나, 금융 규제 준수를 위해 트랜잭션 무결성과 데이터 기밀성, 그리고 무중단 가용성이 요구됨.
  - **의사결정**: 성능 손실을 감수하더라도 서비스 간 모든 통신에 mTLS(Mutual TLS)를 적용하여 보안성을 확보. 2PC(Two-Phase Commit) 대신 Saga 패턴과 보상 트랜잭션을 결합하여 신뢰성과 성능 간의 타협점을 도출. 망분리 환경을 고려한 이식성 높은 프라이빗 클라우드(PaaS) 아키텍처 선택.
- **시나리오 B: 글로벌 OTT 스트리밍 서비스 (성능 효율성과 사용성 최우선)**
  - **문제**: 전 세계 수천만 사용자가 동시에 접속 시 네트워크 병목 발생, 동영상 버퍼링에 따른 사용자 이탈(사용성 저하).
  - **의사결정**: 글로벌 CDN 캐싱을 통해 원본 서버 부하를 줄여 성능 효율성 극대화. 사용자 네트워크 상태(Bandwidth)를 실시간 측정하여 화질을 동적으로 조절하는 ABR(Adaptive Bitrate) 알고리즘을 도입하여 열악한 환경에서도 중단 없는 사용성 보장.

### 2. 도입 시 고려사항 (체크리스트)
- **품질 시나리오 구체화**: "시스템은 빨라야 한다"가 아니라, "정상 운영 상태에서 사용자 로그인 요청 시 10,000 TPS 환경에서 99%의 응답이 200ms 이내에 완료되어야 한다"와 같이 자극(Stimulus), 환경, 응답, 측정 지표를 명확히 정의(ATAM 품질 시나리오 양식 활용).
- **기술 부채(Technical Debt) 관리**: 프로젝트 초기 시장 선점을 위해 유지보수성을 포기하고 기능 구현에 집중했다면, 안정화 단계에서는 리팩토링을 통해 유지보수성과 보안성 지표를 끌어올리는 전략적 접근이 필수.
- **관측 가능성(Observability)**: 성능과 신뢰성을 지속 평가하기 위해 단순 로깅을 넘어 Tracing(OpenTelemetry), Metrics(Prometheus), Logging(ELK)의 3요소를 완벽히 구축해야 함.

### 3. 주의사항 및 안티패턴 (Anti-patterns)
- **골드 플레이팅(Gold Plating)**: 요구되지 않은 과도한 품질 수준을 달성하기 위해 자원과 일정을 낭비하는 행위. 예컨대, 하루 접속자 100명인 내부 관리자 시스템에 99.999%의 가용성과 글로벌 스케일 아키텍처를 적용하는 것은 오버엔지니어링입니다.
- **비기능적 요구사항 후반부 반영**: 아키텍처 설계가 모두 끝나고 개발 막바지에 성능 테스트나 보안 진단을 수행하여 아키텍처 전반을 뒤엎는 치명적인 재작업 발생.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (Ad-hoc 개발) | 도입 후 (ISO 25010 기반 설계) | 정량적 지표 및 효과 |
| :--- | :--- | :--- | :--- |
| **비용(TCO)** | 잦은 장애 복구 및 기술 부채로 인한 높은 O&M 비용 | 아키텍처 조기 최적화로 유지보수 비용 절감 | 시스템 생애 주기 비용 30% 이상 절감 |
| **리스크** | 릴리즈 후 보안 취약점 노출 및 대규모 서비스 중단 | 설계 단계의 위협 모델링으로 선제적 방어 | 장애 시간(Downtime) 99% 감소 (SLA 달성) |
| **비즈니스** | 사용자 불만 가중, 이탈률 상승 | 안정적인 성능과 높은 사용성으로 고객 경험 극대화 | NPS(순추천고객지수) 및 잔존율 상승 |

### 2. 미래 전망 및 진화 방향
클라우드 네이티브, AI, Edge Computing의 발전으로 품질 속성 평가의 패러다임도 변하고 있습니다. 인공지능이 코드를 분석하여 실시간으로 유지보수성과 보안 취약점을 측정(AI-driven QA)하고, 머신러닝 기반의 이상 탐지가 신뢰성을 예측 방어하는 형태로 진화할 것입니다. 또한 지속 가능성(Sustainability)이 새로운 비공식적 품질 속성으로 대두되며, 탄소 배출을 줄이는 그린 컴퓨팅 기반의 성능 효율성이 주목받고 있습니다.

### 3. ※ 참고 표준/가이드
- **ISO/IEC 25010**: System and software quality models.
- **SEI ATAM**: Architecture Tradeoff Analysis Method.
- **ISO/IEC 27001**: Information security management.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [`[ATAM (Architecture Tradeoff Analysis Method)]`](@/studynotes/11_design_supervision/02_evaluation/architecture_evaluation.md) : 품질 속성 요구사항을 도출하고 트레이드오프를 분석하는 핵심 아키텍처 평가 방법론.
- [`[MSA (Microservices Architecture)]`](@/studynotes/04_software_engineering/01_sdlc_methodology/msa.md) : 유지보수성과 확장성은 뛰어나지만 분산 환경에 따른 신뢰성과 성능 설계가 어려운 아키텍처 스타일.
- [`[CAP Theorem]`](@/studynotes/05_database/02_concurrency_control/distributed_database_theory.md) : 분산 데이터베이스 환경에서 신뢰성(일관성, 가용성, 파티션 허용성) 간의 트레이드오프를 수학적으로 증명한 이론.
- [`[Chaos Engineering]`](@/studynotes/15_devops_sre/01_sre_fundamentals/sre_principles.md) : 신뢰성과 결함 허용성을 실무에서 검증하기 위해 고의로 장애를 주입하는 SRE 방법론.
- [`[CI/CD]`](@/studynotes/15_devops_sre/03_automation/cicd_gitops.md) : 유지보수성과 배포의 신뢰성을 보장하는 자동화 파이프라인.

---

## 👶 어린이를 위한 3줄 비유 설명
1. **기능 vs 품질**: '스마트폰으로 전화를 건다'는 건 기능이고, '통화 음질이 깨끗하고 배터리가 오래 간다'는 건 품질 속성이에요.
2. **트레이드오프(저울질)**: 자동차의 쇠판을 아주 두껍게 만들면 튼튼해서 안전하지만(보안성/신뢰성), 너무 무거워져서 느려지고 기름을 많이 먹어요(성능 효율성 감소). 완벽한 건 없으니 상황에 맞게 타협해야 해요.
3. **ISO 25010**: 그래서 전 세계 똑똑한 사람들이 모여 "좋은 소프트웨어란 이런 8가지 기준을 만족해야 해!"라고 정해놓은 거대한 체크리스트이자 규칙책입니다.
