+++
title = "인증성 (Authenticity)"
date = 2026-03-05
[extra]
categories = "studynotes-security"
+++

# 인증성 (Authenticity)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 정보의 출처, 주체의 신원, 데이터의 진위를 보장하는 보안 속성으로, PKI·전자서명·생체인식·MFA가 핵심 구현 기술이다.
> 2. **가치**: 강력한 인증성 통제는 피싱 공격을 99% 차단하며, 디지털 포렌식에서 증거 채택률을 95%까지 높인다.
> 3. **융합**: FIDO2/WebAuthn 표준은 패스워드 없는 인증을 실현하고, 블록체인은 분산 신원(DID)으로 인증성 패러다임을 혁신한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**인증성(Authenticity)**이란 정보의 출처, 통신 상대방, 시스템 주체의 신원이 진짜임을 보장하는 보안 속성이다. 이는 단순히 "누구인지 확인하는 것"을 넘어, **데이터의 출처, 메시지의 발신자, 디지털 자산의 진위**까지 포괄하는 종합적인 개념이다.

인증성은 **인증(Authentication)**과 **검증(Verification)** 두 가지 하위 개념으로 구성된다:
- **인증**: "당신은 누구인가?" - 주체의 신원 확인
- **검증**: "이 데이터는 진짜인가?" - 데이터의 진위 확인

```
┌─────────────────────────────────────────────────────────────────┐
│                     인증성 (Authenticity) 체계                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────┐      │
│   │                   인증성 보장 대상                   │      │
│   └─────────────────────────────────────────────────────┘      │
│                            │                                   │
│         ┌──────────────────┼──────────────────┐               │
│         ▼                  ▼                  ▼               │
│   ┌──────────┐       ┌──────────┐       ┌──────────┐          │
│   │  주체    │       │  데이터  │       │  시스템  │          │
│   │ 인증성   │       │ 인증성   │       │ 인증성   │          │
│   ├──────────┤       ├──────────┤       ├──────────┤          │
│   │ 사용자   │       │ 출처     │       │ 장비     │          │
│   │ 서비스   │       │ 무결성   │       │ 소프트웨어│          │
│   │ 디바이스 │       │ 타임스탬프│       │ 펌웨어   │          │
│   └────┬─────┘       └────┬─────┘       └────┬─────┘          │
│        │                  │                  │                │
│        ▼                  ▼                  ▼                │
│   ┌─────────────────────────────────────────────────────┐      │
│   │               인증성 구현 기술                       │      │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │      │
│   │  │  MFA    │ │  PKI    │ │전자서명 │ │ 생체인식│   │      │
│   │  │ FIDO2   │ │ X.509   │ │ ECDSA   │ │ 지문    │   │      │
│   │  │ OAuth   │ │ CRL/OCSP│ │ RSA-PSS │ │ 얼굴    │   │      │
│   │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │      │
│   └─────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 💡 비유

인증성은 **"신분증 확인"**과 같다.
- 공항에서 여권을 보여주고 본인임을 증명한다
- 신분증의 사진, 이름, 번호가 본인과 일치해야 한다
- 위조된 신분증은 보안 요원이 가짜임을 판별해야 한다

또 다른 비유로 **"예술 작품의 진품 감정"**이 있다.
- 박물관에 있는 명화가 진짜인지 확인한다
- 화가의 서명, 화풍, 캔버스 연대 등을 검증한다
- 위조 작품은 전문가가 감정하여 가짜임을 밝혀낸다

### 등장 배경 및 발전 과정

**1. 기존 기술의 치명적 한계점**
- **패스워드 의존**: 약한 비밀번호, 재사용, 피싱 공격 취약
- **자체 서명 인증서**: 신뢰 체계 없이 위조 가능
- **단일 요소 인증**: 한 가지 요소만 탈취하면 인증 우회

**2. 혁신적 패러다임 변화**
- **1990년대 PKI**: 공개키 기반 구조로 신뢰 체계 확립
- **2000년대 MFA**: 다중 요소 인증으로 보안 강화
- **2010년대 FIDO**: 패스워드 없는 인증 표준화
- **2020년대 DID**: 분산 신원으로 중앙 집중형 인증 탈피

**3. 비즈니스적 요구사항 강제**
- **GDPR**: "적절한 인증 수단" 요구
- **PSD2**: 금융 거래 강력 고객 인증(SCA) 의무화
- **HIPAA**: 의료 정보 접근 인증 강화

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|-----------|------|
| **PKI (공개키 기반구조)** | 신뢰 체계 구축 | CA 발급 → 인증서 검증 → 신뢰 판정 | X.509, CA, CRL, OCSP | 여권 발급소 |
| **전자서명** | 데이터 출처 인증 | 해시 → 개인키 서명 → 공개키 검증 | RSA-PSS, ECDSA, Ed25519 | 공증 |
| **MFA (다중요소인증)** | 주체 신원 강화 | 지식+소유+특징 조합 | OTP, TOTP, FIDO2 | 집 문 2단 잠금 |
| **생체인식** | 고유 신체 특징 인증 | 특징 추출 → 매칭 → 판정 | 지문, 얼굴, 홍채, 정맥 | 얼굴 확인 |
| **FIDO2/WebAuthn** | 패스워드 없는 인증 | 비대칭키 + 생체인식 + 챌린지 | CTAP2, WebAuthn | 생체인식 출입 |
| **타임스탬프** | 시점 인증 | TSA 서명 → 시간 증명 | RFC 3161, TSA | 우편 소인 |

### 인증성 보장 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    인증성 (Authenticity) 종합 아키텍처                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [사용자 인증 흐름]                                                          │
│                                                                             │
│   사용자                   인증 서버                  리소스 서버            │
│   ┌─────┐                  ┌─────┐                    ┌─────┐              │
│   │ 👤  │                  │ 🔐  │                    │ 💾  │              │
│   └──┬──┘                  └──┬──┘                    └──┬──┘              │
│      │                        │                          │                  │
│      │  1. 인증 요청          │                          │                  │
│      │  (ID + MFA)           │                          │                  │
│      │ ───────────────────────►                          │                  │
│      │                        │                          │                  │
│      │                        │ 2. 인증 처리             │                  │
│      │                        │  - 패스워드 검증         │                  │
│      │                        │  - OTP/생체인식 검증     │                  │
│      │                        │  - 위험 기반 평가        │                  │
│      │                        │                          │                  │
│      │  3. 토큰 발급          │                          │                  │
│      │  (JWT/OAuth Token)    │                          │                  │
│      │ ◄───────────────────────                          │                  │
│      │                        │                          │                  │
│      │  4. 리소스 요청        │                          │                  │
│      │  (토큰 포함)           │                          │                  │
│      │ ──────────────────────────────────────────────────►                  │
│      │                        │                          │                  │
│      │                        │  5. 토큰 검증 요청       │                  │
│      │                        │ ◄─────────────────────────                  │
│      │                        │                          │                  │
│      │                        │  6. 토큰 유효성 응답     │                  │
│      │                        │ ──────────────────────────►                  │
│      │                        │                          │                  │
│      │  7. 리소스 응답                                   │                  │
│      │ ◄─────────────────────────────────────────────────                   │
│                                                                             │
│   [PKI 기반 데이터 인증 흐름]                                                 │
│                                                                             │
│   발신자                   수신자                                           │
│   ┌─────┐                  ┌─────┐                                          │
│   │     │                  │     │                                          │
│   │ 메시지 (M)             │                                     │
│   │ ───────────────────────────►                                  │
│   │                        │                                     │
│   │ [발신자 작업]           │                                     │
│   │ 1. Hash = SHA256(M)    │                                     │
│   │ 2. Sig = Sign(Hash, d) │                                     │
│   │ 3. 전송: M + Sig + Cert│                                     │
│   │                        │                                     │
│   │                        │ [수신자 검증]                        │
│   │                        │ 4. Hash' = SHA256(M)                │
│   │                        │ 5. Hash = Verify(Sig, Cert.pub)     │
│   │                        │ 6. Hash' == Hash ?                  │
│   │                        │    → 일치: 인증성 확인               │
│   │                        │    → 불일치: 위조 의심               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: FIDO2/WebAuthn 인증

**1단계: 등록 (Registration) → 2단계: 인증 (Authentication) → 3단계: 검증 (Verification)**

```
[1단계: 등록]
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│ 사용자           │         │ 웹 서버          │         │ 인증기 (Authn)   │
│ (Browser)        │         │ (Relying Party)  │         │ (FIDO2)          │
└────────┬─────────┘         └────────┬─────────┘         └────────┬─────────┘
         │                            │                            │
         │  1. 등록 요청               │                            │
         │ ─────────────────────────────►                            │
         │                            │                            │
         │  2. Challenge + Options    │                            │
         │ ◄────────────────────────────                            │
         │                            │                            │
         │  3. navigator.credentials.create()                      │
         │ ──────────────────────────────────────────────────────────►
         │                            │                            │
         │                            │  4. 키 쌍 생성              │
         │                            │     - 공개키 (pub)         │
         │                            │     - 개인키 (priv, 보안영역)│
         │                            │     - credentialId         │
         │                            │                            │
         │  5. attestationObject + clientDataJSON                   │
         │ ◄─────────────────────────────────────────────────────────
         │                            │                            │
         │  6. 등록 완료 (공개키 저장) │                            │
         │ ─────────────────────────────►                            │
         │                            │                            │

[2단계: 인증]
         │                            │                            │
         │  7. 로그인 요청             │                            │
         │ ─────────────────────────────►                            │
         │                            │                            │
         │  8. Challenge + credentialIds                            │
         │ ◄────────────────────────────                            │
         │                            │                            │
         │  9. navigator.credentials.get()                          │
         │ ──────────────────────────────────────────────────────────►
         │                            │                            │
         │                            │  10. 생체인식/PIN 확인      │
         │                            │  11. 서명 생성              │
         │                            │      Sig = Sign(challenge, priv)
         │                            │                            │
         │  12. assertion (Sig + authData)                          │
         │ ◄─────────────────────────────────────────────────────────
         │                            │                            │
         │  13. 서명 검증             │                            │
         │ ─────────────────────────────►                            │
         │                            │                            │
         │  14. 인증 성공             │                            │
         │ ◄────────────────────────────                            │
```

### 핵심 코드: JWT 기반 인증 구현

```python
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict
from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

@dataclass
class TokenPayload:
    sub: str  # subject (user id)
    iat: int  # issued at
    exp: int  # expiration
    type: TokenType
    jti: str  # JWT ID (unique identifier)

class AuthenticityProvider:
    """
    JWT 기반 인증성 보장 구현체

    Features:
    - Access Token + Refresh Token 이중 토큰
    - 토큰 서명 검증 (RS256)
    - 토큰 폐기 목록 (Blacklist)
    - 세션 추적
    """

    def __init__(self, secret_key: str, algorithm: str = "RS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.blacklist: set = set()  # 실제로는 Redis 사용
        self.access_token_expire = timedelta(minutes=15)
        self.refresh_token_expire = timedelta(days=7)

    def generate_token_pair(self, user_id: str,
                            additional_claims: Optional[Dict] = None) -> Dict:
        """
        Access Token + Refresh Token 쌍 생성
        """
        now = datetime.utcnow()

        # Access Token
        access_jti = secrets.token_urlsafe(16)
        access_payload = {
            "sub": user_id,
            "iat": int(now.timestamp()),
            "exp": int((now + self.access_token_expire).timestamp()),
            "type": TokenType.ACCESS.value,
            "jti": access_jti,
            **(additional_claims or {})
        }
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)

        # Refresh Token
        refresh_jti = secrets.token_urlsafe(16)
        refresh_payload = {
            "sub": user_id,
            "iat": int(now.timestamp()),
            "exp": int((now + self.refresh_token_expire).timestamp()),
            "type": TokenType.REFRESH.value,
            "jti": refresh_jti,
            "access_jti": access_jti  # 연관 관계 추적
        }
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": int(self.access_token_expire.total_seconds())
        }

    def verify_token(self, token: str, expected_type: TokenType = TokenType.ACCESS) -> Dict:
        """
        토큰 검증 (인증성 확인)
        """
        try:
            # 1. 서명 검증
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # 2. 토큰 타입 확인
            if payload.get("type") != expected_type.value:
                raise ValueError(f"Invalid token type: expected {expected_type.value}")

            # 3. Blacklist 확인 (폐기된 토큰)
            jti = payload.get("jti")
            if jti in self.blacklist:
                raise ValueError("Token has been revoked")

            # 4. 추가 검증 (선택)
            # - 발급자(iss) 확인
            # - 대상자(aud) 확인
            # - 커스텀 클레임 검증

            return {
                "valid": True,
                "payload": payload,
                "user_id": payload.get("sub")
            }

        except jwt.ExpiredSignatureError:
            return {"valid": False, "error": "Token expired"}
        except jwt.InvalidSignatureError:
            return {"valid": False, "error": "Invalid signature"}
        except jwt.DecodeError:
            return {"valid": False, "error": "Invalid token format"}
        except ValueError as e:
            return {"valid": False, "error": str(e)}

    def revoke_token(self, token: str) -> bool:
        """
        토큰 폐기 (로그아웃)
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            jti = payload.get("jti")
            if jti:
                self.blacklist.add(jti)
                return True
        except:
            pass
        return False

    def refresh_access_token(self, refresh_token: str) -> Optional[Dict]:
        """
        Refresh Token으로 Access Token 갱신
        """
        verification = self.verify_token(refresh_token, TokenType.REFRESH)
        if not verification.get("valid"):
            return None

        user_id = verification.get("user_id")
        return self.generate_token_pair(user_id)

# 실무 예시
provider = AuthenticityProvider("my-secret-key")

# 토큰 발급
tokens = provider.generate_token_pair("user-123", {"role": "admin"})
print(f"Access Token: {tokens['access_token'][:50]}...")

# 토큰 검증
result = provider.verify_token(tokens['access_token'])
print(f"Token Valid: {result['valid']}")
print(f"User ID: {result.get('user_id')}")

# 토큰 폐기 (로그아웃)
provider.revoke_token(tokens['access_token'])
result = provider.verify_token(tokens['access_token'])
print(f"After Revoke: {result}")  # {'valid': False, 'error': 'Token has been revoked'}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 비교표 1: 인증 방식별 인증성 보장 수준

| 구분 | 패스워드 | OTP/TOTP | FIDO2/WebAuthn | 생체인식 | mTLS |
|------|----------|----------|----------------|----------|------|
| **피싱 저항** | 취약 | 부분 | 강함 | 강함 | 강함 |
| **재사용 공격** | 취약 | 취약 | 저항 | 저항 | 저항 |
| **중간자 공격** | 취약 | 부분 | 저항 | 저항 | 저항 |
| **사용자 편의성** | 중간 | 중간 | 높음 | 높음 | 낮음 |
| **구현 복잡도** | 낮음 | 중간 | 높음 | 높음 | 높음 |
| **비용** | 낮음 | 낮음 | 중간 | 중간 | 높음 |
| **인증성 수준** | 낮음 | 중간 | 높음 | 높음 | 매우 높음 |

### 비교표 2: PKI vs 분산 신원 (DID)

| 구분 | PKI (중앙 집중형) | DID (분산형) |
|------|-------------------|--------------|
| **신뢰 모델** | CA 중심 계층형 | P2P 분산형 |
| **신원 발급** | CA가 발급 | 본인이 생성 |
| **검증 방식** | 인증서 체인 검증 | DID Document 검증 |
| **프라이버시** | CA가 모든 정보 보유 | 사용자가 통제 |
| **단일 장애점** | CA 장애 시 전체 영향 | 없음 |
| **표준** | X.509 | W3C DID, Verifiable Credentials |
| **적용 사례** | HTTPS, 전자서명 | 블록체인 신원, 자격증명 |

### 과목 융합 관점 분석

**1. 네트워크 × 인증성**
- **TLS**: 서버 인증서로 서버 신원 확인
- **mTLS**: 양방향 인증으로 클라이언트도 검증
- **IPsec**: IKE 인증으로 VPN 게이트웨이 검증

**2. 데이터베이스 × 인증성**
- **행 레벨 보안**: 사용자별 데이터 접근 제어
- **감사 로그**: 누가, 언제, 무엇을 했는지 추적
- **TDE + 인증**: 암호화 키 접근 인증

**3. 클라우드 × 인증성**
- **IAM**: 클라우드 리소스 접근 인증
- **서비스 계정**: 서비스 간 인증
- **Workload Identity**: K8s Pod 인증

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 시나리오

**시나리오 1: 금융 서비스 MFA 도입**

```
상황: 온라인 뱅킹 피싱 공격 증가, 규제 강화

[요구사항]
① PSD2 SCA 준수 (2요소 이상 인증)
② 피싱 공격 99% 이상 차단
③ 사용자 경험 저하 최소화

[기술사적 의사결정]
┌─────────────────────────────────────────────────────────────────┐
│ [인증 레벨 설계]                                                 │
│                                                                 │
│ Level 1 (조회): 단일 요소                                        │
│ • 패스워드 또는 생체인식                                         │
│ • 위험도: 낮음                                                   │
│                                                                 │
│ Level 2 (이체): 2요소 인증                                       │
│ • 패스워드 + OTP/TOTP                                           │
│ • 또는 FIDO2 (생체인식 + 디바이스)                               │
│ • 위험도: 중간                                                   │
│                                                                 │
│ Level 3 (고액이체/설정변경): 2요소 + 추가 검증                    │
│ • FIDO2 + SMS/이메일 확인                                       │
│ • 행위 기반 분석 (UEBA)                                         │
│ • 위험도: 높음                                                   │
│                                                                 │
│ [기술 선택]                                                      │
│ • 1차: FIDO2/WebAuthn (패스워드 없는 인증)                       │
│ • 2차: TOTP (Google Authenticator)                              │
│ • 백업: SMS OTP (FIDO2 미지원 기기)                              │
└─────────────────────────────────────────────────────────────────┘
```

**시나리오 2: API 서비스 간 인증**

```
상황: 마이크로서비스 아키텍처에서 서비스 간 인증

[요구사항]
① 제로 트러스트: 모든 서비스 간 통신 인증
② 성능: 인증 오버헤드 <5ms
③ 확장성: 서비스 100개+ 지원

[기술사적 의사결정]
┌─────────────────────────────────────────────────────────────────┐
│ [Service Mesh (Istio) 기반 mTLS]                                │
│                                                                 │
│ 장점:                                                           │
│ • 자동 인증서 발급/갱신                                          │
│ • 투명한 암호화 (애플리케이션 수정 불필요)                        │
│ • 세밀한 접근 제어 (Authorization Policy)                        │
│                                                                 │
│ 구성:                                                           │
│ 1. Istio CA (Citadel)가 각 Pod에 인증서 발급                    │
│ 2. Envoy Sidecar이 mTLS 처리                                    │
│ 3. 서비스 계정 (K8s ServiceAccount) 기반 신원                    │
│                                                                 │
│ [Authorization Policy 예시]                                      │
│ apiVersion: security.istio.io/v1beta1                           │
│ kind: AuthorizationPolicy                                       │
│ metadata:                                                       │
│   name: payment-api-authz                                       │
│ spec:                                                           │
│   selector:                                                     │
│     matchLabels:                                                │
│       app: payment-api                                          │
│   rules:                                                        │
│   - from:                                                       │
│     - source:                                                   │
│         principals: ["cluster.local/ns/default/sa/order-svc"]   │
│     to:                                                         │
│     - operation:                                                │
│         methods: ["POST"]                                       │
│         paths: ["/api/v1/payments/*"]                           │
└─────────────────────────────────────────────────────────────────┘
```

### 도입 시 고려사항 체크리스트

**기술적 고려사항**
- [ ] 인증 프로토콜 선정 (OAuth 2.0, SAML, OpenID Connect)
- [ ] 토큰 저장 방식 (JWT, 세션)
- [ ] 키 관리 (KMS, HSM)
- [ ] 인증 서버 고가용성

**운영/보안적 고려사항**
- [ ] 계정 잠금 정책 (무차별 대입 공격 방지)
- [ ] 비밀번호 정책 (복잡성, 만료)
- [ ] 세션 관리 (타임아웃, 동시 로그인)
- [ ] 감사 로그 (인증 성공/실패)

**주요 안티패턴**

| 안티패턴 | 문제점 | 올바른 접근 |
|----------|--------|-------------|
| **평문 패스워드 저장** | DB 유출 시 계정 탈취 | bcrypt, Argon2 해싱 |
| **토큰 localStorage 저장** | XSS 공격 시 탈취 | HttpOnly Cookie |
| **자체 인증 프로토콜** | 보안 취약점 가능성 | 표준 프로토콜 사용 |
| **영구 토큰** | 탈취 시 무제한 사용 | 만료 + 갱신 토큰 |

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|------|---------|---------|-----------|
| **피싱 공격 성공률** | 3.4% | 0.02% | **99.4% 감소** |
| **계정 탈취 사고** | 월 15건 | 월 0건 | **100% 예방** |
| **인증 관련 헬프데스크** | 월 200건 | 월 30건 | **85% 감소** |
| **규제 준수** | 부분 | 완전 | **PSD2/GDPR 충족** |

### 미래 전망 및 진화 방향

**1. 패스워드 없는 인증 (Passwordless)**
- Apple Passkey, Microsoft Hello, Google Passkey
- FIDO2 표준 확산
- 2025년까지 주요 서비스 패스워드 폐지 예상

**2. 지속적 인증 (Continuous Authentication)**
- 행동 생체인식 (타이핑 패턴, 마우스 움직임)
- 위험 기반 적응형 인증
- 세션 전반의 실시간 검증

**3. 분산 신원 (DID)**
- W3C DID 표준
- 블록체인 기반 자기 주권 신원
- Verifiable Credentials

### ※ 참고 표준/가이드

| 표준 | 내용 | 적용 범위 |
|------|------|-----------|
| **FIPS 201-3** | PIV (Personal Identity Verification) | 미국 연방기관 |
| **NIST SP 800-63B** | 디지털 신원 가이드라인 | 미국 정부 |
| **ISO/IEC 27001 A.9** | 접근 통제 | 글로벌 |
| **PSD2 RTS** | 강력 고객 인증 (SCA) | EU 금융 |
| **FIDO2/WebAuthn** | 패스워드 없는 인증 | 글로벌 |

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [정보보안 3요소 (CIA Triad)](./1_cia_triad.md): 인증성을 포함한 확장 보안 속성
- [PKI (공개키 기반구조)](../10_pki/pki.md): 인증성 기반 인프라
- [전자서명 (Digital Signature)](../2_crypto/digital_signature.md): 데이터 인증성
- [MFA (다중요소인증)](../7_identity/mfa.md): 주체 인증 강화
- [OAuth 2.0 / OIDC](../7_identity/oauth_oidc.md): 인증 표준 프로토콜
- [제로 트러스트](./zero_trust_architecture.md): 인증 중심 보안 모델

---

## 👶 어린이를 위한 3줄 비유 설명

**🪪 여권 검사**
공항에서 여권을 보여주면 직원阿姨가 내 얼굴과 여권 사진이 같은지 확인해요. 진짜 내 여권이면 비행기를 탈 수 있어요.

**✍️ 서명 확인**
은행에서 돈을 찾을 때는 서명을 확인해요. 내 서명과 통장에 적힌 서명이 같아야만 돈을 줘요.

**👆 지문 인식**
아빠 휴대폰은 지문으로 잠금을 풀어요. 아빠 손가락만 대야 풀리고, 내 손가락은 안 돼요.

---

*최종 수정일: 2026-03-05*
*작성 기준: 정보통신기술사·컴퓨터응용시스템기술사 대비 심화 학습 자료*
