+++
title = "제로 트러스트 아키텍처 (Zero Trust Architecture)"
description = "네트워크 내부든 외부든 모든 사용자, 기기, 서비스를 신뢰하지 않고 지속적으로 검증하는 보안 모델"
date = 2024-05-15
[taxonomies]
tags = ["Zero-Trust", "Security", "Network", "mTLS", "IAM", "Identity"]
+++

# 제로 트러스트 아키텍처 (Zero Trust Architecture)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: "절대 신뢰하지 말고, 항상 검증하라(Never Trust, Always Verify)"는 원칙하에 네트워크 경계(Perimeter) 내부든 외부든 **모든 접속 요청을 명시적으로 검증**하고, 최소 권한(Least Privilege)만 부여하며, 지속적인 모니터링을 수행하는 근본적 보안 패러다임입니다.
> 2. **가치**: 전통적 경계 기반 보안(방화벽, VPN)의 한계를 극복하고, 내부자 위협(Insider Threat), 랜섬웨어의 수평 이동(Lateral Movement), 클라우드/원격 근무 환경의 보안 문제를 해결하여 보안 사고 피해를 80% 이상 감소시킵니다.
> 3. **융합**: 서비스 메시(mTLS), IAM(Identity and Access Management), 마이크로 세그멘테이션, SASE(Secure Access Service Edge), PAM(Privileged Access Management)과 결합하여 현대적 Zero Trust 엔터프라이즈 보안을 실현합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**제로 트러스트(Zero Trust)**는 2010년 Forrester Research의 John Kindervag가 제안한 보안 모델로, **"기본적으로 아무것도 신뢰하지 않는다"**는 원칙을 기반으로 합니다. 핵심 원칙:
1. **명시적 검증(Explicit Verification)**: 모든 접근 요청을 인증하고 승인
2. **최소 권한 접근(Least Privilege Access)**: 필요한 최소한의 권한만 부여
3. **위반 가정(Assume Breach)**: 침해는 이미 발생했다고 가정하고 영향 최소화

Zero Trust는 "사내 네트워크에 있으면 신뢰한다"는 전통적 경계 보안을 완전히 거부합니다. 사무실 WiFi에 연결된 기기라도, 다시 인증해야 합니다.

### 2. 구체적인 일상생활 비유
전통적 보안은 **회사 건물 출입문**입니다. 출입문만 통과하면 내부 어디든 자유롭게 돌아다닐 수 있습니다. **Zero Trust**는 **각 방마다 있는 보안 게이트**입니다. 회의실에 들어갈 때도, 서류실에 들어갈 때도, 심지어 화장실에 갈 때도 다시 카드키를 찍어야 합니다. 그리고 "왜 여기 왔어?"라는 질문에 답해야만 문이 열립니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (Perimeter Security의 붕괴)**:
   전통적 보안은 "외부는 위험, 내부는 안전"이라고 가정했습니다. 그러나: 1) 클라우드로 경계가 사라짐 2) 원격 근무로 사내 네트워크 개념이 희미해짐 3) 내부자 위협(Insider Threat) 증가 4) 해커가 한 번 침투하면 내부에서 자유롭게 이동(Lateral Movement).

2. **혁신적 패러다임 변화의 시작**:
   2010년 Forrester가 Zero Trust 개념 제안. 2014년 Google이 BeyondCorp으로 내부 Zero Trust 구현. 2020년 NIST SP 800-207로 Zero Trust 표준화. 2021년 미국 행정명령 14028로 연방정부 Zero Trust 의무화.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   랜섬웨어, 공급망 공격(SolarWinds) 대응, 원격 근무 보안, 클라우드 마이그레이션 보안, GDPR/CCPA 개인정보 보호 규정 준수를 위해 Zero Trust는 필수가 되었습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 |
| :--- | :--- | :--- | :--- |
| **Policy Engine(PE)** | 접근 결정(Deny/Allow) | Context 기반 정책 평가 | OPA, Casbin |
| **Policy Administrator(PA)** | 정책 실행 및 세션 설정 | 토큰 발급, 터널 생성 | ZTNA Gateway |
| **Policy Enforcement Point(PEP)** | 트래픽 차단/허용 | 방화벽, 프록시, 사이드카 | Istio, Envoy |
| **Identity Provider(IdP)** | 사용자/기기 인증 | SSO, MFA, 디바이스 상태 체크 | Okta, Azure AD |
| **Data Plane** | 트래픽 전송 및 보안 | mTLS 암호화, 마이크로 세그멘테이션 | Service Mesh |
| **Control Plane** | 정책 관리 및 배포 | 중앙 집중식 정책 정의 | ZTNA Controller |

### 2. 정교한 구조 다이어그램: Zero Trust 아키텍처

```text
=====================================================================================================
                      [ Zero Trust Architecture - Never Trust, Always Verify ]
=====================================================================================================

  [ Traditional Perimeter Security ]              [ Zero Trust Architecture ]
  ════════════════════════════════════            ═══════════════════════════

     +-------------------------+                    +-------------------------+
     | Trusted Internal Network|                    | Untrusted Everywhere    |
     | +---------------------+ |                    |                         |
     | | App Server          | |                    |    Every access must    |
     | | DB Server           | |                    |    be verified!         |
     | | File Server         | |                    |                         |
     | +----------+----------+ |                    +-----------+-------------+
     |            ^            |                                |
     |  TRUSTED   |            |                                v
     | (Implicit) |            |                    +-------------------------+
     +------------|------------+                    | 1. Identity Verification |
                  |                                 |    - Who are you? (AuthN)|
        +---------|---------+                       |    - MFA, SSO            |
        | Firewall/VPN      |                       +------------+------------+
        | (Single Perimeter)|                                    |
        +---------+---------+                                    v
                  ^                                 +-------------------------+
                  |                                 | 2. Device Posture       |
     [ External ] |                                 |    - Is device secure?  |
     (Untrusted)  |                                 |    - OS patched?        |
                  |                                 |    - Antivirus active?  |
                  v                                 +------------+------------+
        +---------+---------+                                    |
        | Internet Users    |                                    v
        +-------------------+                       +-------------------------+
                                                    | 3. Context Evaluation   |
                                                    |    - Where from?        |
                                                    |    - When?              |
                                                    |    - What resource?     |
                                                    +------------+------------+
                                                                 |
                                                                 v
                                                    +-------------------------+
                                                    | 4. Policy Decision      |
                                                    |    - Allow / Deny       |
                                                    |    - Least Privilege    |
                                                    +------------+------------+
                                                                 |
                                                                 v
                                                    +-------------------------+
                                                    | 5. Encrypted Access     |
                                                    |    - mTLS Tunnel        |
                                                    |    - Microsegmented     |
                                                    +-------------------------+

=====================================================================================================

                      [ Zero Trust in Kubernetes - Service Mesh ]
=====================================================================================================

  [ Service A ]              [ Istio Control Plane ]              [ Service B ]
       |                            |                                   |
       v                            v                                   v

+-------------+            +-------------------+            +------------------+
| Application |            | istiod            |            | Application      |
| Container   |            | - Certificate     |            | Container        |
+------+------+            |   Authority (CA)  |            +--------+---------+
       |                   | - Policy Engine   |                     |
       v                   +--------+----------+                     v
+-------------+                     |                        +-------------+
| Envoy Proxy |<---- mTLS Tunnel ---+---- mTLS Tunnel ------->| Envoy Proxy |
| (Sidecar)   |                     |                        | (Sidecar)   |
| - AuthN     |                     |                        | - AuthN     |
| - AuthZ     |                     v                        | - AuthZ     |
| - Encryption|            +-------------------+             | - Encryption|
+-------------+            | Policy Repository |             +-------------+
       |                   | - RBAC Rules      |                    |
       |                   | - Access Policies |                    |
       +-------------------+-------------------+--------------------+

  Every service-to-service call is:
  1. Authenticated (mTLS)
  2. Authorized (OPA/ABAC)
  3. Encrypted (TLS 1.3)
  4. Logged (Audit Trail)

=====================================================================================================
```

### 3. 심층 동작 원리 (Zero Trust 핵심 메커니즘)

**1. 지속적 검증 (Continuous Verification)**
전통적 인증은 "로그인 한 번 = 세션 전체 신뢰"입니다. Zero Trust는 **지속적 검증**을 수행합니다:
- 세션 타임아웃: 짧은 세션(1시간) + 정기 재인증
- 디바이스 상태 체크: OS 버전, 패치 상태, 감염 여부 실시간 확인
- 행위 분석: 비정상적 접근 패턴 감지 시 즉시 차단

**2. 최소 권한 (Least Privilege)**
필요한 순간에 필요한 권한만 부여합니다:
- Just-In-Time(JIT) 권한: 요청 시에만 권한 부여, 사용 후 즉시 회수
- Just-Enough-Access(JEA): "읽기 전용" vs "읽기/쓰기" 세분화
- Role-Based vs Attribute-Based: RBAC + ABAC 조합

**3. 마이크로 세그멘테이션 (Micro-Segmentation)**
네트워크를 작은 단위로 분할하여 수평 이동(Lateral Movement)을 차단합니다:
- East-West Traffic 제어: 서비스 간 통신도 방화벽 규칙 적용
- Zero Trust Network Access(ZTNA): 애플리케이션 레벨 게이트웨이
- Network Policy(K8s): Pod 간 통신을 기본 Deny로 설정

### 4. 핵심 알고리즘 및 실무 코드 예시

**Kubernetes Network Policy (기본 Deny All)**

```yaml
# network-policy-default-deny.yaml
# Step 1: Deny all ingress traffic by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}  # Selects all pods in namespace
  policyTypes:
  - Ingress
  # No ingress rules = deny all

---
# Step 2: Deny all egress traffic by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Egress
  # No egress rules = deny all

---
# Step 3: Allow specific traffic only (whitelist)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080

---
# Step 4: Allow backend to database only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-to-database
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  # Allow DNS resolution
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

**Istio AuthorizationPolicy (서비스 메시 mTLS + RBAC)**

```yaml
# istio-authorization.yaml
# Deny all requests by default
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}
  # Empty selector = deny all

---
# Allow frontend to call backend with JWT authentication
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: backend-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  # Rule 1: Require valid JWT from trusted issuer
  - from:
    - source:
        requestPrincipals: ["https://auth.mycompany.com/*"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
    when:
    # Require specific scope
    - key: request.auth.claims[scope]
      values: ["read:backend", "write:backend"]
    # Require device posture check (via custom claim)
    - key: request.auth.claims[device_trust_level]
      values: ["high", "medium"]
```

**OPA(Open Policy Agent) Policy as Code**

```rego
# policies/rbac.rego
package authz

import input.user
import input.resource
import input.action

# Default deny
default allow = false

# Allow if user has role with required permission
allow {
    # Get user's roles
    user_roles := user.roles[_]

    # Get permissions for role
    role_perms := data.roles[user_roles].permissions[_]

    # Check if permission matches request
    role_perms.resource == resource.type
    role_perms.action == action

    # Additional conditions
    match_conditions(role_perms.conditions)
}

# Role definitions (loaded from external data)
# data.roles = {
#   "admin": {
#     "permissions": [
#       {"resource": "*", "action": "*"}
#     ]
#   },
#   "developer": {
#     "permissions": [
#       {"resource": "pod", "action": "read"},
#       {"resource": "pod", "action": "list"},
#       {"resource": "log", "action": "read"}
#     ]
#   }
# }

match_conditions(conditions) {
    # Time-based access (business hours only)
    not conditions.business_hours_only
}
match_conditions(conditions) {
    conditions.business_hours_only
    current_hour := time.clock(time.now_ns())[0]
    current_hour >= 9
    current_hour < 18
}
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 보안 모델 비교

| 평가 지표 | 경계 보안(Perimeter) | VPN + 방화벽 | Zero Trust |
| :--- | :--- | :--- | :--- |
| **신뢰 가정** | 내부는 신뢰 | VPN 연결 후 신뢰 | 아무것도 신뢰 안 함 |
| **인증** | 1회(로그인) | 1회(VPN) | 지속적 |
| **네트워크 접근** | 전체 | 전체 | 최소 필요만 |
| **수평 이동** | 허용됨 | 허용됨 | 차단됨 |
| **원격 근무** | VPN 필요 | VPN 필요 | ZTNA 직접 |
| **클라우드 적용** | 어려움 | 어려움 | 용이 |

### 2. 과목 융합 관점 분석

**Zero Trust + DevSecOps**
- DevSecOps는 코드 레벨 보안(Shift-Left), Zero Trust는 런타임 보안. 두 가지가 결합하여 "코드부터 운영까지" Zero Trust를 실현합니다.

**Zero Trust + 서비스 메시**
- Istio/Linkerd의 mTLS가 서비스 간 Zero Trust를 구현합니다. 모든 트래픽이 인증되고 암호화됩니다.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 랜섬웨어로 인한 수평 이동 방지**
- **문제점**: 한 대의 서버가 감염되면 전체 네트워크로 랜섬웨어가 전파됩니다.
- **기술사 판단 (전략)**: Zero Trust 마이크로 세그멘테이션으로 서버 간 통신을 기본 Deny. 필요한 통신만 명시적 Allow. 한 서버 감염 시 다른 서버로 전파 차단.

**[상황 B] 원격 근무자 보안**
- **문제점**: 재택근무자가 공용 WiFi에서 VPN 없이 회사 자원에 접근해야 합니다.
- **기술사 판단 (전략)**: VPN 대신 ZTNA(Zero Trust Network Access) 도입. 디바이스 상태 체크 후 애플리케이션 레벨 게이트웨이로 직접 접근. 전체 네트워크가 아닌 특정 앱에만 접근 허용.

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] Identity Provider 선정: Okta, Azure AD, Google Workspace
- [ ] MFA 필수: TOTP, FIDO2/WebAuthn
- [ ] Device Posture: 디바이스 보안 상태 체크 솔루션

**운영적 고려사항**
- [ ] 단계적 도입: VPN -> ZTNA -> Full Zero Trust
- [ ] 사용자 교육: "왜 자꾸 로그인해야 하나요?" 불만 해소
- [ ] 레거시 시스템: Zero Trust 미지원 시스템 격리 전략

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: Zero Trust 도구만 도입하고 정책 없음**
- 도구(도구)는 있지만 "누가 무엇에 접근 가능한가?"에 대한 정책이 없으면 Zero Trust가 작동하지 않습니다. 정책 먼저 정의해야 합니다.

**안티패턴 2: 일부에만 Zero Trust 적용**
- 핵심 시스템만 Zero Trust, 나머지는 기존 방식 = 여전히 취약. 전체 시스템에 Zero Trust를 적용해야 효과가 있습니다.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 경계 보안 (AS-IS) | Zero Trust (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **수평 이동** | 허용 | 차단 | **공격 전파 0%** |
| **내부자 위협** | 탐지 어려움 | 지속 검증 | **위협 탐지 90% 향상** |
| **원격 근무 보안** | VPN 취약 | ZTNA | **접근 보안 강화** |
| **규정 준수** | 부분적 | 완전 | **컴플라이언스 달성** |

### 2. 미래 전망 및 진화 방향
- **SASE(Secure Access Service Edge)**: 네트워크와 보안을 클라우드로 통합한 Zero Trust 플랫폼.
- **Decentralized Identity(DID)**: 블록체인 기반 탈중앙화 신원으로 Zero Trust Identity 강화.

### 3. 참고 표준/가이드
- **NIST SP 800-207**: Zero Trust Architecture 표준
- **US Executive Order 14028**: 연방정부 Zero Trust 의무화
- **Forrester Zero Trust eXtended**: Zero Trust 구현 프레임워크

---

## 관련 개념 맵 (Knowledge Graph)
- **[DevSecOps](@/studynotes/15_devops_sre/5_devsecops/241_devsecops_principles.md)**: Zero Trust와 함께하는 보안 체계
- **[서비스 메시](@/studynotes/13_cloud_architecture/1_native/service_mesh.md)**: mTLS 기반 Zero Trust 구현
- **[mTLS](@/studynotes/15_devops_sre/4_iac/207_mtls.md)**: 상호 TLS 인증
- **[마이크로 세그멘테이션](@/studynotes/15_devops_sre/5_devsecops/253_microsegmentation.md)**: 네트워크 분할 보안
- **[IAM](@/studynotes/15_devops_sre/5_devsecops/iam.md)**: 신원 및 접근 관리

---

## 어린이를 위한 3줄 비유 설명
1. 옛날에는 **학교 정문만 통과하면** 교실, 체육관, 급식실 어디든 갈 수 있었어요.
2. Zero Trust는 **모든 문마다 선생님이 서서** "너 누구야? 어디 갈 거야? 왜 가?" 하고 물어보는 거예요.
3. 덕분에 나쁜 사람이 학교에 들어와도 한 방밖에 못 돌아다녀요. 다음 방으로 가려면 또 선생님한테 검사받아야 하니까요!
