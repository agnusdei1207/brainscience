+++
weight = 247
title = "API Gateway 기능 (API Gateway Functions)"
date = "2026-03-25"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> XML 변환, 헤더 조작, 응답 필터링 | 클라이언트 맞춤형 데이터 제공 |

> 📝 모범 답안

- 마이크로서비스 아키텍처(MSA)의 진입점으로서 요청 라우팅, 인증, 인가, 속도 제한을 통합 관리함
- 클라이언트와 내부 서비스 간의 결합도를 낮추고 프로토콜 변환 및 오케스트레이션 기능을 제공함
- 보안 관점에서는 API 위협 차단, 데이터 마스킹, 중앙 집중형 로깅을 수행하는 핵심 통제 지점임

### 1. 개요 및 필요성
클라우드 네이티브 환경에서 서비스가 파편화됨에 따라 클라이언트가 수많은 엔드포인트를 직접 관리하기 어려워졌다. API Gateway는 이러한 복잡성을 은닉하고 공통 기능을 외재화하여 백엔드 서비스의 비즈니스 로직 집중도를 높인다.

### 2. 구성요소
```text
[API Gateway Architecture - Entry Point for MSA]

Client (Mobile/Web/IoT)
      |
      V
+---------------------------+
|       API GATEWAY         |
|---------------------------|
| - Authentication/AuthZ    | <--- Security Layer
| - Rate Limiting/Quota     | <--- Traffic Control
| - Protocol Translation    | <--- Transformation
| - Load Balancing/Routing  | <--- Routing
+---------------------------+
      |        |        |
      V        V        V
 [Service A] [Service B] [Service C] (Microservices)
```
- **핵심 원리:** 모든 외부 요청을 단일 지점으로 수렴시킨 후, 정책 엔진(Policy Engine)을 통해 검증 및 변환 과정을 거쳐 적절한 마이크로서비스로 전달함

### 3. 구조 및 동작 원리
| 기능 영역 | 세부 기능 설명 | 기대 효과 |
| :--- | :--- | :--- |
| 보안 (Security) | JWT 검증, OAuth 2.0 연동, IP 화이트리스트 | 통합 보안 정책 적용, 백엔드 부담 완화 |
| 트래픽 제어 | Rate Limiting, Throttling, Circuit Breaker | DoS 방어, 시스템 안정성 확보 |
| 관리 (Management) | 로깅, 모니터링, API 버전 관리 | 가시성 확보, 무중단 배포 지원 |
| 데이터 변환 | JSON <-
### 4. 비교 및 트레이드오프
- **실무 적용:** Kong, Apigee, AWS API Gateway 등이 널리 사용되며, 제로 트러스트 관점에서 모든 요청을 'Untrusted'로 간주하고 매번 인증을 수행하는 것이 기본임
- **기술사적 판단:** API Gateway 자체가 단일 장애점(SPOF)이 될 수 있으므로, 고가용성(HA) 구성과 성능 병목 현상에 대한 세밀한 튜닝이 필수적임

### 5. 실무 적용 및 최적화 기법
- **기대효과:** 개발 생산성 향상, 보안 사고 대응력 강화, 서비스 확장성 보장 등을 통해 엔터프라이즈 급 IT 서비스 운영의 안정성을 제공함
- **결론:** API Gateway는 단순한 프록시를 넘어 서비스 메시(Service Mesh)와 상호 보완하며 클라우드 보안 아키텍처의 중추적인 역할을 지속할 것임

### 📌 관련 개념 맵 (Knowledge Graph)
- MSA → API Gateway → Service Mesh
- API Gateway → 보안 → OAuth 2.0 / JWT / Rate Limiting
- 인프라 → Load Balancer → Reverse Proxy

### 👶 어린이를 위한 3줄 비유 설명
- 큰 성(회사 시스템)에 들어가려면 문 하나하나를 다 찾아다닐 필요 없이 '정문(API Gateway)'으로 가면 돼요.
- 정문 수문장이 누구인지 확인하고, 너무 자주 들어오지는 않는지 체크한 다음 길을 안내해 줘요.
- 복잡한 성 안쪽을 몰라도 수문장만 따라가면 원하는 방에 안전하게 도착할 수 있답니다!
