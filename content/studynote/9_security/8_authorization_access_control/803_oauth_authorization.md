+++
title = "OAuth 2.0 인가"
description = "OAuth 2.0의 권한 위임(Delegation) 원리와 보안"
date = 2024-01-15
weight = 3
+++

# OAuth 2.0 인가 (OAuth 2.0 Authorization)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OAuth 2.0은 사용자가 비밀번호를 공유하지 않고도 제3자 애플리케이션에 자신의 자원(데이터, 서비스)에 대한 제한된 접근 권한을 위임할 수 있게 하는 인가 프레임워크이다.
> 2. **가치**: 2012년 RFC 6749로 표준화된 이후 Google, GitHub, Facebook, Microsoft 등 주요 플랫폼이採用하여, 안전한 제3자 접근 관리가 가능해졌다.
> 3. **융합**: OAuth 2.0은 암호학(JWT, 서명), 보안(CSRF 방어, PKCE), 그리고 거버넌스(OAuth Scope)와 깊이 결합한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

OAuth 2.0(Open Authorization 2.0)은 RFC 6749로 표준화된 인가 프레임워크로, 사용자가 비밀번호를 제3자에게提供하지 않고도, 해당 서비스에 저장된 자원에 대한 접근 권한을 제한적으로 위임할 수 있게 한다. 예를 들어, Dropbox에 저장된 사진 Galleries를 Adobe Photoshop 앱에서편집하려 할 때, 사용자는 Adobe에 Dropbox 비밀번호를 제공하는 대신, Dropbox에서 Adobe에게 "照片 Galleries 읽기/쓰기 권한"만 부여할 수 있다. 이 과정에서 Adobe는 사용자의 Dropbox 비밀번호를 알지 못하며, 부여된 권한范围内 에서만 데이터에 접근 가능하다.

### 필요성

과거에는 제3자 앱에 자사 서비스 접근을 허가하려면 사용자가 직접 비밀번호를 제공해야 했다. 이 방식에는 여러 문제점이 있다. First, 앱이 비밀번호를 저장/남용할 수 있다. Second,万一 앱에서 정보 유출이 발생하면 비밀번호连带して被害が拡大한다. Third, 사용자는 비밀번호를 변경할 수 없는데, 앱에서 여전히 접근 가능한 문제가 있다. OAuth 2.0은 이러한 문제를 해결하여, 사용자의 비밀번호를 공유하지 않고도 접근 권한을 제어할 수 있게 한다.

### 💡 비유

OAuth 2.0은 **호텔 짐보관 대리점 시스템**과 같다. 짐을 찾으러 가는데 짐 열쇠가 없으니, 짐보관소 직원에가 내 비밀번호를告知하는 대신, 짐보관소가 임시 열쇠(Access Token)를発行해서 그것으로 짐을 찾게 해준다.万一 임시 열쇠가 도난되면, 호텔에서 그 열쇠를無効화하면되고, 내 비밀번호는 여전히安全하다.

### 등장 배경

2006년 Twitter가 OpenID와 OAuth의 선구자인 AuthProxy를 사용하기 시작했으며, 2007년 Google, Yahoo, Microsoft 등이참여하여 OAuth 1.0이诞生했다. 그러나 OAuth 1.0은cryptographic 서명 요구사항이복잡하여実装가 어려웠다. 2012년 IETF는 OAuth 2.0(RFC 6749)를 발표하여간소화된授权流程을 표준화했다. 이후 2018년 OAuth 2.0 PKCE(RFC 7636)가Extensions되어 public client에서의安全性이 크게 향상되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### OAuth 2.0 핵심 역할

OAuth 2.0은 네 가지 핵심 역할로 구성된다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    OAuth 2.0 역할                                           │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [Resource Owner (자원 소유자)]                                       │
  │  - 자원에 대한 접근 권한을 부여하는 사람                               │
  │  - 예: Dropbox 사용자, Google 사용자                                  │
  │
  │  [Client (클라이언트)]                                               │
  │  - Resource Owner's 대신에 보호된 자원에 접근하려는 애플리케이션       │
  │  - 예: Adobe Photoshop, Airbnb, Notion                               │
  │
  │  [Authorization Server (인준 서버)]                                    │
  │  - Resource Owner를 authentication하고, Client에 access token 발급      │
  │  - 예: Google Auth Server, Dropbox Auth Server                        │
  │
  │  [Resource Server (자원 서버)]                                        │
  │  - 보호된 자원을 호스팅하고, access token을 검증하여 접근을制御        │
  │  - 예: Google Drive API, Dropbox API                                  │
  │
  │  [흐름]                                                            │
  │
  │  Resource Owner ──▶ Client ──▶ Authorization Server                   │
  │       │                    │                    │                  │
  │       │                    │  1. 권한 부여 요청   │                  │
  │       │                    │◀── 2. Resource Owner 인증 + 동의 │  │
  │       │                    │                    │                  │
  │       │                    │  3. Authorization Code │            │
  │       │                    │◀──────────────────────────────│  │
  │       │                    │                                       │
  │       │                    │  4. Access Token 요청 (+ Code)    │
  │       │                    │◀── 5. Access Token ──────────────│  │
  │       │                    │                                       │
  │       │◀───────── Authorization Server ─────────────────────│  │
  │       │                                                        │
  │       │  6. Access Token으로 Resource Server 접근              │
  │       │◀────────────────────────────────────────────────────│  │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Resource Owner는 자원의 실제 소유자(일반 사용자)이고, Client는 Resource Owner's 대신 보호된 자원에 접근하려는 애플리케이션이다. Authorization Server는 Resource Owner를 인증하고(Client를 인증하는 것이 아님), Resource Owner의 동의的基础上 Access Token을 발급한다. Resource Server는 Access Token을 검증하여 보호된 자원에 대한 접근을 허용/차단한다. 이 구조에서 핵심은 "비밀번호는 절대로 Client에게 흐르지 않는다"는 것이다.

### OAuth 2.0 Grant Types

OAuth 2.0은 다양한 사용 사례를サポートするために 여러 Grant Type을 제공한다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    OAuth 2.0 Grant Types                                   │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [1. Authorization Code Grant (가장 권장)]                           │
  │
  │  - Confidential Client용 (서버 사이드)                                │
  │  - Authorization Code + PKCE로 security 강화                       │
  │  - 웹 앱, 모바일 앱, 데스크톱 앱 모두適用                              │
  │
  │  [2. PKCE (Proof Key for Code Exchange)]                             │
  │
  │  - Public Client (SPA, 모바일 앱)용安全强化                           │
  │  - code_verifier + code_challenge 메커니즘                          │
  │  - Authorization Code 가로채기 방지                                   │
  │
  │  [3. Client Credentials Grant]                                        │
  │
  │  - Client가 자체 ресур에 접근할 때                                     │
  │  - 사용자 context 없음 (데몬/마이크로서비스)                          │
  │
  │  [4. Device Code Grant]                                               │
  │
  │  - 스마트 TV, CLI 도구等 입력受限 장치용                               │
  │  - 사용자가 별도 장치에서 코드 입력                                    │
  │
  │  [5. Refresh Token Grant]                                             │
  │
  │  - Access Token 만료 시 새 Access Token 획득                           │
  │  - Refresh Token은 장기 저장, Access Token은短期                     │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Authorization Code Grant는 가장 널리 사용되는 Flow로, 처음에는 Confidential Client(서버 사이드 웹 앱)용으로 설계되었다. PKCE(Proof Key for Code Exchange)는 Public Client(SPA, 모바일 앱)에서도 안전한 사용을위해 도입된 확장으로, code verifier와 code challenge를利用한다. Client Credentials Grant는 사용자가 아닌 시스템(데몬, 백그라운드 서비스)이 자체 자원에 접근할 때 사용된다. Refresh Token Grant를 통해 Access Token이 만료되었을 때 사용자가 다시 로그인할 필요 없이 Refresh Token으로 새로운 Access Token을 획득할 수 있다.

### Scope (범위)

Scope는 Access Token으로 어떤 자원 중 어떤 작업까지 가능한지를정의한다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    OAuth 2.0 Scope 예시                                    │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [Google APIs Scope]                                                 │
  │
  │  https://www.googleapis.com/auth/drive          # Google Drive 전체     │
  │  https://www.googleapis.com/auth/drive.readonly # Google Drive 읽기만  │
  │  https://www.googleapis.com/auth/gmail.readonly # Gmail 읽기만        │
  │
  │  [Scope 요청 예시]                                                   │
  │
  │  GET /authorize?                                                    │
  │    response_type=code                                                │
  │    &client_id=my_app                                                │
  │    &scope=openid profile email https://www.googleapis.com/auth/drive │
  │    &redirect_uri=https://myapp.com/callback                        │
  │
  │  [동의 화면에서 사용자에게 표시되는 정보]                             │
  │
  │  "my_app가 다음에 접근을 요청합니다:                                  │
  │    - Google Drive 파일 읽기 및 쓰기                                  │
  │    - Gmail 주소록 읽기                                               │
  │    - 기본 프로필 정보 (이름, 이메일)"                                │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Scope는 OAuth 2.0에서 권한의粒度를 정의한다. 예를 들어, Google Drive에 대한 읽기/쓰기 전체 접근, 읽기 전용 접근, 또는 Gmail 읽기만 가능하도록 세분화할 수 있다. Resource Owner는 Scope를 확인하고 동의 여부를 판단한다. Client는 필요한 최소한의 Scope만 요청해야 하며(Minimum Privilege), 불필요하게 넓은 Scope를 요청하면 사용자의不信을 사거나 보안 위험이 증가한다.

- **📢 섹션 요약 비유**: OAuth 2.0은 **호텔 짐보관 대리점**과 같다. 짐을 찾으러 가는데, 짐 열쇠가 없으니 대리점에가 짐보관소에서 임시 열쇠(Access Token)를받고, 그 열쇠로 짐을 찾는다.万一 그 임시 열쇠가 도난되면酒店에서无效化하면 되고, 내 실제 열쇠(비밀번호)는안전하게酒店에 남아있다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### OAuth 2.0 vs SAML

| 비교 항목 | OAuth 2.0 | SAML 2.0 |
|:---|:---|:---|
| **기본 목적** | Authorization (권한 위임) | SSO (Authentication) |
| **주 사용처** | Consumer Apps, API | Enterprise SSO |
| **Assertion 포맷** | JWT/Access Token | XML Assertion |
| **프로토콜 특성** | Stateless (Token) | Stateful (Session) |

### 과목 융합 관점

- **암호학**: Access Token은 JWT形式로서 서명(RSA, HMAC)을 통해 무결성과 발급자 인증이保障된다.
- **보안**: PKCE는 Authorization Code 가로채기 공격을방어하며, CSRF 방지를 위해 state parameter 사용이 권장된다.
- **거버넌스**: OAuth Scope는 조직 내 권한 위임의olicy를 정의하고 준수하는 데 활용된다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — Google API OAuth 2.0**: 웹 앱이 Google Calendar에 접근할 때, 사용자에게 Google 로그인 + 권한 동의를 요청하고, Authorization Code를 Access Token으로 교환하여 Google Calendar API를 호출.

2. **시나리오 — GitHub OAuth + PKCE**: SPA에서 GitHub OAuth를 사용할 때, PKCE를 적용하여 Authorization Code 가로채기 공격을 방지하고, HTTPS 리다이렉트만 허용.

### 도입 체크리스트

- **기술적**: PKCE를 적용하고 있는가? Redirect URI를 화이트리스트로 관리하고 있는가?
- **운영·보안적**: Client Secret을 안전하게管理하고 있는가? Refresh Token의 유효 기간을 제한하고 있는가?

### 안티패턴

- **Implicit Grant 사용 (대안 있음)**: Implicit Grant는 보안 문제가 있어 Authorization Code + PKCE로 대체되어야 한다.
- ** broad Scope 요청**: 필요한 권한보다 넓은 Scope를 요청하면 사용자의不信과 보안 위험이 증가한다.
- **State 미검증**: CSRF 공격 방지를 위한 state parameter 검증을省略하면 안 된다.

- **📢 섹션 요약 비유**: OAuth 2.0은 **호텔 짐보관 대리점**과 같다. 짐 열쇠(비밀번호)를 대리점에預ける代わりに、임시 열쇠(Access Token)를 받는다.万一 열쇠가 도난되면酒店에서无效化할 수 있고, 내 실제 열쇠는안전하다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 비밀번호 공유 | OAuth 2.0 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 비밀번호 유출 시 全 권한 노출 | 토큰 단위로 권한 제한 | 노출 최소화 |
| **정성** | 제3자 앱에 비밀번호 제공 의무 | 비밀번호 공유 불필요 | 사용자 신뢰 향상 |

### 미래 전망

OAuth 2.0은 현재 업계 표준이지만, GNAP(Grant Negotiation and Authorization Protocol)라는 차세대 프로토콜이 IETF에서 논의되고 있다. 또한 OAuth와 OIDC의融合, 그리고 FIDO2/WebAuthn과의统合이 진행되고 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Access Token** | 보호된 자원에 접근하기 위한 증서로, 유효 기간과 Scope를 포함한다. |
| **Refresh Token** | Access Token 만료 시 새 Access Token을 획득하기 위해 사용되는 장기 증서이다. |
| **PKCE** | Public Client에서 Authorization Code 가로채기 공격을방어하기 위한 확장이다. |
| **Scope** | Access Token으로 어떤 자원에 어떤 작업까지 가능한지를정의하는 권한 범위이다. |
| **OIDC** | OAuth 2.0에 인증 레이어를 추가하여 ID Token을 제공하는 프로토콜이다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. OAuth는 **호텔 짐보관 대리점에서 내 짐을 찾을 때, 내 비밀번호(호텔 회원번호)를 대리점staff에게주는 대신, 대리점에서 임시 열쇠(Access Token)를发行해서 그 열쇠로 짐을 찾게 해주는 것**과 같아요.

2.万一 그 임시 열쇠를盗贼가 가지면,酒店에서그 열쇠를無効화하면 되기 때문에, 내 실제 비밀번호(실제 열쇠)는酒店에 남아있어서安全해요.

3. computer 세상에서도 마찬가지예요. Dropbox에 저장된 파일을 다른 앱(예: Adobe)에서 열고 싶을 때, Dropbox 비밀번호를 Adobe에 주는 대신, Dropbox에서 Adobe에게 "내 파일 읽기/쓰기 권한만" 부여하는臨時 열쇠(Access Token)를 발급받아서 사용하는 거예요.万一 Adobe가 해킹당해도 내 Dropbox 비밀번호는安全하고,酒店에서臨時 열쇠를無効화하면 돼요.
