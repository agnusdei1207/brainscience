+++
weight = 458
title = "458. OAuth 2.0 / OIDC 토큰 위임 인증 인가 분산 (OAuth 2.0 / OpenID Connect)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OAuth 2.0은 리소스 소유자(사용자)가 제3자 애플리케이션에게 자원 접근 권한을 '위임'하는 인가(Authorization) 프레임워크이며, OIDC(OpenID Connect)는 OAuth 2.0 위에 구축된 인증(Authentication) 레이어로 ID 토큰을 추가한다.
> 2. **가치**: 사용자가 구글 계정 비밀번호를 제3자 앱에 제공하지 않고도 구글 Drive 접근을 허용할 수 있어, 크리덴셜 공유 없는 안전한 API 접근 위임이 현대 마이크로서비스·소셜 로그인의 기반이 된다.
> 3. **판단 포인트**: OAuth 2.0의 적절한 Flow 선택이 보안의 핵심이며, SPA/모바일 앱은 반드시 PKCE(Proof Key for Code Exchange)를 적용하여 인가 코드 인터셉트 공격을 방어해야 한다.

## Ⅰ. 개요 및 필요성

"구글로 로그인" 버튼을 누를 때 일어나는 일이 바로 OAuth 2.0 + OIDC이다. 사용자는 구글 비밀번호를 앱에 주지 않고도, 구글이 발급한 토큰으로 앱이 구글 프로필 정보에 접근할 수 있게 한다. 이것이 '위임(Delegation)' 개념이다.

현대 마이크로서비스 아키텍처에서 서비스 간 API 호출 인가도 OAuth 2.0 기반이다. 서비스 A가 서비스 B의 API를 호출할 때, 발급받은 액세스 토큰(JWT)을 HTTP 헤더에 포함시켜 인가된 요청임을 증명한다.

OAuth 2.0과 OIDC는 현대 IAM(Identity and Access Management) 체계의 언어(프로토콜)이다. 기술사는 이 두 표준의 차이(인가 vs 인증)와 적절한 Flow를 이해해야 안전한 API 보안 아키텍처를 설계할 수 있다.

📢 **섹션 요약 비유**: OAuth 2.0은 호텔에서 발레파킹 서비스에 차 열쇠를 맡기는 것처럼, "주차장만 이용해도 돼, 트렁크는 열지 마"라고 제한된 권한(Scope)을 명시하고 주는 위임 체계이다.

## Ⅱ. 아키텍처 및 핵심 원리

### OAuth 2.0 구성 요소

| 역할 | 설명 | 예시 |
|:---|:---|:---|
| Resource Owner | 자원 소유자 (사용자) | 구글 Drive 파일 소유자 |
| Client | 자원에 접근하려는 앱 | 캘린더 앱 |
| Authorization Server | 인가 서버 (토큰 발급) | 구글 OAuth 서버 |
| Resource Server | 실제 API 서버 | 구글 Drive API |

### Authorization Code Flow (PKCE 포함)

```
┌──────────────────────────────────────────────────────────────┐
│        OAuth 2.0 Authorization Code Flow with PKCE           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Client → Auth Server:                                    │
│     GET /authorize?response_type=code                        │
│     &code_challenge=BASE64(SHA256(verifier)) [PKCE]          │
│                                                              │
│  2. Auth Server → User: 로그인 + 동의 화면 표시              │
│                                                              │
│  3. Auth Server → Client: Redirect with ?code=XXXXXXXX      │
│                                                              │
│  4. Client → Auth Server:                                    │
│     POST /token { code, code_verifier } [PKCE 검증]          │
│                                                              │
│  5. Auth Server → Client:                                    │
│     { access_token, refresh_token, id_token(OIDC) }         │
│                                                              │
│  6. Client → Resource Server:                                │
│     GET /api/data                                            │
│     Authorization: Bearer {access_token}                    │
│                                                              │
│  PKCE 핵심: code_verifier(랜덤값)를 Client만 알고 있어       │
│            인가 코드가 탈취되어도 토큰 교환 불가             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### OAuth 2.0 Grant Type 비교

| Grant Type | 적합 환경 | 보안 수준 | 현재 권고 |
|:---|:---|:---:|:---|
| Authorization Code + PKCE | SPA, 모바일, 웹앱 | ✅ 최고 | 권장 |
| Client Credentials | 서버-서버 (M2M) | ✅ 높음 | 권장 |
| Device Authorization | TV, IoT 기기 | ✅ 좋음 | 권장 |
| Implicit | — | ❌ 낮음 | **사용 금지** |
| Resource Owner Password | — | ❌ 낮음 | **사용 금지** |

### OIDC ID Token (JWT)

```json
// OIDC ID Token 페이로드 예시
{
  "iss": "https://accounts.google.com",
  "sub": "1234567890",
  "aud": "my-client-id",
  "exp": 1712345678,
  "iat": 1712342078,
  "email": "user@example.com",
  "name": "홍길동"
}
```

📢 **섹션 요약 비유**: ID Token은 여권처럼, 발급 기관(iss)·소유자(sub)·유효기간(exp) 정보가 담긴 공식 신분증으로 위조 방지 서명(JWT 서명)이 되어 있다.

## Ⅲ. 비교 및 연결

### OAuth 2.0 vs OIDC vs SAML 비교

| 항목 | OAuth 2.0 | OIDC | SAML 2.0 |
|:---|:---|:---|:---|
| 목적 | 인가 (Authorization) | 인증 (Authentication) | 인증 + 인가 |
| 토큰 형식 | 불투명/JWT | JWT (ID Token) | XML Assertion |
| 주요 사용 | API 접근 위임 | 소셜 로그인 | 기업 SSO (레거시) |
| 모바일 적합성 | ✅ | ✅ | ✗ (XML 무거움) |

### 토큰 수명 및 갱신 전략

- Access Token: 단명 (15분~1시간) → API 접근 권한
- Refresh Token: 장명 (수일~수개월) → 새 Access Token 발급
- Refresh Token Rotation: 갱신 시마다 새 Refresh Token 발급 (탈취 탐지 가능)

📢 **섹션 요약 비유**: Access Token은 일일 출입증(단명), Refresh Token은 장기 허가증(장명)처럼, 매일 새 출입증을 장기 허가증으로 갱신하는 이중 구조가 보안과 편의성을 동시에 달성한다.

## Ⅳ. 실무 적용 및 기술사 판단

### 마이크로서비스 API 게이트웨이 인가 설계

1. **토큰 검증 집중화**: API Gateway에서 JWT 서명 검증 + 만료 확인 (각 마이크로서비스 중복 검증 제거)
2. **Scope 세분화**: `read:profile` `write:orders` 등 최소 권한 원칙 적용
3. **PKCE 강제화**: 클라이언트 SDK에서 Implicit Flow 제거 및 PKCE 기본값 설정
4. **토큰 폐기(Revocation)**: Refresh Token 즉시 폐기 API 구현 (로그아웃, 의심 활동 감지 시)
5. **mTLS 조합**: 고보안 B2B API는 OAuth 2.0 + mTLS Sender-Constrained Token으로 토큰 바인딩

📢 **섹션 요약 비유**: API Gateway의 JWT 검증은 공항 출입국 심사처럼, 탑승구(마이크로서비스)마다 여권을 확인하는 대신 입국장(Gateway)에서 한 번에 검증하여 내부 이동을 신뢰하는 효율적 보안 게이트이다.

## Ⅴ. 기대효과 및 결론

**기대효과**:
- 비밀번호 공유 없는 API 접근 위임으로 자격증명 탈취 위험 제거
- 소셜 로그인 통합으로 사용자 온보딩 마찰 80% 감소
- 마이크로서비스 간 표준 인가 프로토콜로 일관된 보안 아키텍처

**한계 및 전제조건**:
- JWT 탈취 시 만료까지 사용 가능 → 단명 토큰 + 실시간 폐기 체계 필요
- Authorization Server가 단일 장애점(SPOF) → HA(고가용성) 구성 필수
- 복잡한 Grant Type 선택 오류 시 보안 취약점 발생 (Implicit Flow 여전히 잔존)

📢 **섹션 요약 비유**: OAuth 2.0의 토큰 위임은 마치 전세 계약처럼, 집 주인(Resource Owner)이 열쇠 전부를 주지 않고 특정 방(Scope)에만 접근 가능한 임시 열쇠(Access Token)를 세입자(Client)에게 주는 제한된 신뢰 체계이다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| OIDC | 상위 확장 | OAuth 2.0 위에 인증 레이어 추가 |
| PKCE | 보안 강화 | SPA/모바일의 인가 코드 탈취 방어 |
| JWT | 토큰 형식 | Access Token/ID Token의 표준 형식 |
| SAML | 비교 표준 | 기업 SSO의 레거시 XML 기반 표준 |
| FIDO2 | 보완 기술 | 비밀번호 대체 (인증), OAuth는 인가 |
| API Gateway | 적용 위치 | JWT 검증 집중화 및 Scope 시행 지점 |

### 👶 어린이를 위한 3줄 비유 설명

1. OAuth는 엄마(구글) 허락을 받아 친구(앱)가 내 장난감 일부를 빌려 쓸 수 있게 해주는 허락증이에요.
2. 엄마는 "블록 세트만 빌려줘, 인형은 안 돼"라고 범위(Scope)를 정할 수 있어요.
3. OIDC는 그 허락증에 "이 아이는 정말 우리 아이가 맞아요!"라는 신분 확인 스티커를 추가해주는 것이에요.
