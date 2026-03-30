+++
weight = 6
title = "OAuth와 SAML"
description = "권한 위임 프로토콜 OAuth 2.0과 인증 프레임워크 SAML 2.0의 원리와 보안"
date = 2024-01-15
+++

# OAuth와 SAML (OAuth 2.0 & SAML 2.0)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OAuth 2.0은 제3자에게 제한된 권한으로 서비스 접근을 위임하는 승인 프로토콜(Delegation Protocol)이고, SAML 2.0은 XML 기반의 Assertion을 통해 SSO(Single Sign-On)를実現하는 인증 프레임워크이다. 둘 다 인증/인가가 아닌 인가(Authorization)를 primarily 목적으로 한다.
> 2. **가치**: Google, Facebook, GitHub 등이 OAuth 2.0을 利用하여 자사 서비스에 대한 제3자 앱의 접근을 관리하며, 기업 환경에서는 SAML 2.0이 SSO의 사실상의 표준으로 자리잡았다.
> 3. **융합**: OAuth와 SAML은OpenID Connect(OIDC)에서 OAuth 2.0위에 인증 레이어를 추가하여 양립하며, SAML은 XML 디지털 서명, OAuth는 JWT를 활용한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

OAuth 2.0(Open Authorization 2.0)은 RFC 6749로 표준화된 인가 프레임워크로, 사용자가 자사의 자원에 대한 접근 권한을 제3자 애플리케이션에授할 수 있게 한다. 핵심は "비밀번호를 공유하지 않고 접근 권한을 위임한다"는 것이다. 예를 들어, Google Drive에 저장된 문서를 타사 앱에서編集하려 할 때, 사용자는 Google에 로그인하여 해당 타사 앱에 문서 접근 권한을 부여할 수 있다. 비밀번호가 아닌 액세스 토큰(Access Token)이授되므로,万一 토큰이 Compromised되어도 비밀번호는安全である。

SAML 2.0(Security Assertion Markup Language 2.0)은 XML 기반의Assertion을 통해Identity Provider(IdP)와 Service Provider(SP) 간에 인증/인가 정보를 교환하는 프로토콜이다. 기업 환경에서员工이 SSO를 통해 여러 기업 서비스에 비밀번호 없이 접근하는 것이 대표적 사례이다.

### 필요성

과거에는 제3자 앱에 자사 서비스 접근을 허가하려면 사용자가 자신의 비밀번호를 직접 앱에 제공해야 했다. 이는セキュリティ上 큰 문제로, 앱이 비밀번호를 남용하거나 탈취될 경우 사용자 계정이 완전히 Compromised될 수 있었다. OAuth는 "비밀번호 공유 없이 권한 위임"이라는 문제를 혁신적으로 해결했다. SAML은 기업 환경에서 직원账号관리를 획기적으로 단순화하여,员工이 한 번의 로그인(주로 IdP)으로 여러 기업 서비스에 접근할 수 있게 해준다.

### 💡 비유

OAuth는 **호텔의 짐 보관소 시스템**과 같다. 짐을預かりするために、(비밀번호)를 호텔에預ける代わりに、키에 해당하는 일회용 token(열쇠)을 받아서 짐 보관소에서 짐을 찾는다.万一 token을 lost하면酒店가token을 무효화하면되고,元の 열쇠(비밀번호)는酒店에 그대로 남아 있어安全하다. SAML은 **학교 입구 얼굴 인식 시스템**과 같다. 교문staff(Identity Provider)가학생(사용자)을인식하고, 학생증을발급하면, 이 학생증만으로 도서관, 체육관, 급식실 등 모든 학교 시설에 접근할 수 있다.

### 등장 배경

OAuth 1.0은 2007년 IETFdraft로 등장했으며, Twitter, Google, Yahoo 등이採用했다. 그러나 OAuth 1.0은 서명 복잡성으로知られ、2012년 RFC 6749로 OAuth 2.0이 표준화되어 현재 대부분의 서비스에서 사용되고 있다. SAML 2.0은 2005년 OASIS 표준으로 발표되었으며, 기업 환경의 SSO를 위한 사실상의 표준이 되었다. Google, Salesforce, AWS等都がSAML 2.0을 지원한다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### OAuth 2.0 플로우

OAuth 2.0은 여러 인증 흐름(Grant Flows)을 지원하며, 가장 널리 사용되는 Authorization Code Flow with PKCE를中心으로 설명한다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │            OAuth 2.0 Authorization Code Flow (with PKCE)            │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [역할]                                                            │
  │
  │  Resource Owner: 사용자 (우리)                                         │
  │  Client: 제3자 앱 (Google Drive 편집 앱)                           │
  │  Authorization Server: Google (권한 부여 서버)                        │
  │  Resource Server: Google Drive (보호된 자원)                          │
  │
  │  [Step 1: 코드 챌린지 생성]                                          │
  │
  │  Client: code_verifier (43~128자 랜덤 문자열) 생성                   │
  │          │                                                         │
  │          ▼                                                         │
  │          code_challenge = BASE64URL(SHA256(code_verifier))          │
  │
  │  [Step 2: 권한 부여 요청]                                           │
  │
  │  Client ──▶ Authorization Server                                     │
  │          /authorize?                                                │
  │            response_type=code                                       │
  │            &client_id=xxx                                          │
  │            &redirect_uri=yyy                                        │
  │            &scope=read write                                       │
  │            &code_challenge=zzz                                      │
  │            &code_challenge_method=S256                               │
  │            &state=random                                            │
  │
  │  [Step 3: 사용자 인증 및 동의]                                       │
  │
  │  Authorization Server ◀── Resource Owner (사용자)                   │
  │         사용자 로그인 → "이 앱에 다음 권한을 부여하시겠습니까?"          │
  │         "Google Drive 읽기/쓰기 권한"                                │
  │                        │                                            │
  │                        ▼                                            │
  │         사용자가 "승인" 클릭                                          │
  │
  │  [Step 4: 인증 코드 발급]                                           │
  │
  │  Client ◀── Authorization Server                                    │
  │         /callback?code=AAA...&state=random                        │
  │         ※ Authorization Server는 이 시점에서 Client를 인증하지 않음   │
  │         ※ code는 짧은 유효 기간 (보통 60초)                          │
  │
  │  [Step 5: 액세스 토큰 요청 (Code 교환)]                              │
  │
  │  Client ──▶ Authorization Server                                    │
  │          /token                                                     │
  │          grant_type=authorization_code                               │
  │          &code=AAA...                                              │
  │          &redirect_uri=yyy                                          │
  │          &code_verifier=TTT...  ◀── Step 1에서 생성한 것            │
  │                                                                      │
  │  Authorization Server:                                              │
  │          code_challenge = BASE64URL(SHA256(code_verifier))           │
  │          일치 여부 확인 ──▶ Access Token 발급                         │
  │
  │  [Step 6: 보호된 자원 접근]                                          │
  │
  │  Client ──▶ Resource Server                                         │
  │          Authorization: Bearer eyJhbGci...                         │
  │
  │  Resource Server:                                                   │
  │          토큰 검증 ──▶ 권한(scope) 확인 ──▶ 데이터 제공               │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** OAuth 2.0의 핵심は "비밀번호 공유 없이 권한 위임"이다. Step 1에서 Client는 code_verifier를 생성하고, 이를 SHA256 해시한 값을 code_challenge로 만든다. Step 2에서 Client는 사용자를 Authorization Server로 리다이렉션시킨다. Step 3에서 사용자는Authorization Server에 직접 로그인하고, 권한 동의 여부를 판단한다. 여기서 중요한 것은 Client가 사용자의 비밀번호를 알 수 없다는 점이다. Step 4에서Authorization Server는 authorization code를 Client에 전달한다. 이 코드는 짧은 유효 기간을 가지고 있으며, 직접 사용될 수 없다. Step 5에서 Client는 authorization code와 code_verifier를 함께 제출하여Access Token을 교환한다. Authorization Server는 code_verifier의 해시가 previously 제출된 code_challenge와 일치하는지 확인한다. 이를 통해,万一 authorization code가 가로채어도攻击者는 code_verifier를 모르기 때문에Access Token을얻을 수 없다. 이것이 PKCE(Proof Key for Code Exchange)의 역할이다.

### SAML 2.0 SSO 플로우

SAML 2.0은 XML Assertion을 활용하여 IdP와 SP 간에 인증 정보를 교환한다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    SAML 2.0 SSO 플로우                                   │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [역할]                                                            │
  │
  │  Principal: 사용자 (Employee)                                       │
  │  Service Provider (SP): Salesforce (기업 CRM)                        │
  │  Identity Provider (IdP): Microsoft AD FS (기업 인증 서버)           │
  │
  │  [Step 1: SP 접근 요청]                                             │
  │
  │  Employee ──▶ Salesforce (SP)                                      │
  │             "로그인 필요" → SAML Request 생성                       │
  │                                                                      │
  │  [Step 2: IdP로 리다이렉션]                                         │
  │
  │  SP ──▶ Employee (Browser) ──▶ IdP (AD FS)                         │
  │         HTTP 302 Redirect with SAMLRequest (base64 encoded)          │
  │
  │  [Step 3: IdP에서 사용자 인증]                                       │
  │
  │  IdP ◀── Employee (Browser)                                         │
  │         employee 입력: \\contoso\\username + password                 │
  │         IdP는 Kerberos/AD를 통해사용자 인증                          │
  │
  │  [Step 4: SAML Assertion 발급]                                     │
  │
  │  IdP ──▶ Employee (Browser)                                         │
  │         SAML Response (base64 encoded, XML + 디지털 서명)            │
  │         Assertion 내용:                                              │
  │         - Subject (employee@contoso.com)                              │
  │         - Attributes (department, role)                            │
  │         - Conditions (유효 기간, Audience)                           │
  │         - Issuer (AD FS)                                             │
  │         - Signature (IdP의 비공개키로 서명)                         │
  │
  │  [Step 5: SP로 Assertion 전송]                                      │
  │
  │  Employee (Browser) ──▶ SP (Salesforce)                             │
  │         SAML Response을 POST 또는 Redirect로 전송                    │
  │
  │  [Step 6: SP에서 Assertion 검증 및 접근 허가]                        │
  │
  │  SP (Salesforce):                                                   │
  │         - IdP의 공개키로 서명 검증                                   │
  │         - Assertion 내용(Attributes) 추출                             │
  │         - 유효 기간, Audience 확인                                   │
  │         - employee@contoso.com 로ocal 계정 매핑 또는 생성             │
  │         - SSO 완료, Salesforce 접근 허가                             │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** SAML의 핵심은 Identity Provider(IdP)가 사용자를 인증하고, Service Provider(SP)에게 "이 사용자는 이미 인증되었습니다"라는Assertion을 XML 형태로 전달하는 것이다. SP는 IdP의 공개키로 서명을 검증하여 Assertion의 진위와 무결성을확인한다. Assertion에는 사용자의 식별 정보(Subject)와 권한 정보(Attributes), 그리고 유효 기간과 AudienceRestriction(어떤 SP를 위한 것인지)이 포함된다. SAMLResponse는 base64 인코딩되어 Browser를 통해 SP에 전달되는데, 이 과정에서 SAMLResponse 자체는 HTTPS로 보호된다.

### OAuth vs SAML 비교

| 비교 항목 | OAuth 2.0 | SAML 2.0 |
|:---|:---|:---|
| **기본 목적** | 권한 위임 (Authorization) | SSO/인증 (Authentication) |
| **Assertion 포맷** | JWT (JSON) | XML |
| **주 사용처** | Consumer apps, APIs | Enterprise SSO |
| **Identity Federation** | OpenID Connect 필요 | 네이티브 지원 |
| **모바일 친화성** | 높음 (PKCE) | 낮음 (XML) |
| **토큰 유형** | Access Token, Refresh Token | SAML Assertion |

- **📢 섹션 요약 비유**: OAuth는 **호텔 짐보관 대리점**과 같다. 짐을 찾으러 가면, 짐 열쇠(비밀번호)를 대리점에預ける 대신, 대리점에서 일회용 열쇠(Access Token)를 받아 짐 보관소에 가서 그 열쇠로 짐을 찾는다.万一 열쇠를 다른 사람이 取也得,Hotel에서 열쇠를 무효화하면 된다. SAML은 **학교 통합 출입증**과 같다. 교문staff(Identity Provider)가학생을認証하여 출입증(Assertion)을 발급하면, 이 출입증으로 도서관, 체육관, 급식실 등 모든 시설에 출입할 수 있다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### OpenID Connect (OIDC)와의 관계

OIDC는 OAuth 2.0위에 인증(Authentication) 레이어를 추가하여,OAuth의 권한 위임 기능과 SAML의 SSO 기능을 결합한 프로토콜이다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    OAuth 2.0 vs OIDC vs SAML                             │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [OAuth 2.0]                                                        │
  │  목적: "이 사용자가 Google Drive에 접근하는 것을 승인하시겠습니까?"     │
  │  결과: Access Token (Google Drive 접근 권한)                         │
  │  알 수 없는 것: 사용자가 누구인지 (匿名性)                              │
  │
  │  [OpenID Connect (OIDC)]                                            │
  │  목적: "이 사용자가 누구인지 확인" + 권한 위임                       │
  │  결과: ID Token (JWT) + Access Token                               │
  │  ID Token 내용: sub, name, email, picture, ...                    │
  │
  │  [SAML 2.0]                                                        │
  │  목적: "이 사용자가 기업 IdP에 의해 인증됨"을 SP에 알림              │
  │  결과: SAML Assertion (XML) + 세션                               │
  │
  │  [관계]                                                            │
  │
  │  OAuth 2.0 ──+──▶ Authorization Server + AuthN 레이어 = OIDC      │
  │               │                                                    │
  │               └──▶ SAML Assertion의 대체재 (보다轻盈, JSON 기반)    │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** OAuth 2.0은認証ではなく、"사용자의同意"에 초점을 맞춘다. Google Drive 예시에서, 사용자가 Google에 로그인했고, Google이 사용자를認識しているが、Google은 SP(App)에게사용자의이름이나 이메일을 알려주지 않는다. OIDC는 여기에 ID Token을 추가하여, 사용자의 신원 정보(Sub, Name, Email, Picture 등)를 포함하게 만든다. 따라서 OIDC는 "OAuth 2.0 + Authentication"으로 이해할 수 있으며, SAML 2.0의 대안으로 설계되었다. OIDC가 SAML보다 선호되는 이유는 JSON/JWT가 XML보다 가볍고, mobile과 API-friendly하며,基建が简单だから이다.

### 과목 융합 관점

- **암호학**: OAuth는 JWT(Access Token), SAML은 XML Digital Signature과 Encryption을 활용한다.
- **웹 보안**: OAuth 2.0은 CSRF 방지를 위해 state parameter를, PKCE를 利用하여 authorization code 탈취를 방지한다.
- **기업 보안**: SAML 2.0은 LDAP/AD 환경의 enterprise SSO의 사실상의 표준이며, AWS, Azure, GCP等都が SAML 2.0 federation을 지원한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — Google OAuth 2.0을 활용한 SSO**: 사용자가 "Google로 로그인" 버튼을 클릭하여 Google 계정으로 웹 앱에 접근하는 구조. 사용자는 Google에 로그인하고, 웹 앱에는 Google이 발급한 Access Token만 전달되므로, 비밀번호는 웹 앱에 공유되지 않는다.

2. **시나리오 — SAML 2.0 기반 기업 SSO**: 직원이 Salesforce에 접근할 때, Microsoft AD FS (IdP)를 통해 Single Sign-On. 직원은 AD credentials으로 한번만 인증하면, 이후 모든 기업 SaaS (Salesforce, ServiceNow, AWS管理等)에 SSO로 접근한다.

### 도입 체크리스트

- **기술적**: OAuth 사용 시 PKCE를 적용하고 있는가? 리다이렉트 URI를 화이트리스트로 관리하고 있는가?
- **운영·보안적**: Access Token/Rotation의 유효 기간이 적절한가? Refresh Token의 저장소가 안전한가?

### 안티패턴

- **OAuth 1.0 사용**: 서명 복잡성으로 인해 현재는 OAuth 2.0 + PKCE를 사용해야 한다.
- **State 미검증**: OAuth에서 CSRF 공격 방지를 위한 state parameter 검증을省略하면 안 된다.
- **SAML Assertion 미검증**: SP가 IdP의 공개키로 서명 검증을 수행하지 않으면 악의적인 Assertion을 받아들일 수 있다.

- **📢 섹션 요약 비유**: OAuth는 **호텔 짐보관 대리점**에서 일회용 열쇠를 받는 것과 같아서, 비밀번호를預ける 대신 일회용 열쇠로 짐을 찾는다. SAML은 **학교 통합 출입증**과 같아서, 교문에서 한 번 인증되면 출입증으로 모든 시설에 출입한다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 비밀번호 공유 | OAuth/SAML | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 제3자 앱에 비밀번호 유출 위험 | 토큰 기반으로 안전 | 비밀번호 유출 위험 제거 |
| **정성** | SSO 없음, 각 앱마다 로그인 | SSO로 편의성 향상 | 사용자 경험大幅 향상 |

### 미래 전망

OAuth와 SAML의融合が進んでいる。 OpenID Connect가 OAuth 2.0의 간단함과 SAML의 인증 기능을 결합하여, 새로운 애플리케이션에서는 OIDC가首选되고 있다. 또한 차세대 인증方式인 FIDO2/WebAuthn도 OAuth/OIDC 위에서利用될 수 있어,passwordless 인증과의融合が期待されている。

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **OAuth 2.0** | 제3자에게 제한된 권한을 위임하는 프레임워크로, Access Token을 통해 자원 접근을承認한다. |
| **PKCE** | OAuth 2.0의 authorization code 탈취를 방지하는 확장으로, code verifier와 challenge를利用한다. |
| **OIDC** | OAuth 2.0에 인증 레이어를 추가한 프로토콜으로, ID Token과 Access Token을 모두 제공한다. |
| **SAML 2.0** | XML 기반의 Assertion으로 기업 SSO를実現하는 프로토콜이다. |
| **SSO** | 한 번의 인증으로 여러 서비스에 접근할 수 있는 것으로, SAML과 OAuth/OIDC가支援한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. OAuth는 **친구에게 내library 책을 대신 찾아달라고 할 때의 방법**과 같아요. 친구에게 내 비밀图书馆 membership卡(비밀번호)를 주는 대신,library에 가서 일회용 이용券(Access Token)을 받아 친구에게 전달한다. 친구는 그券로 책은 찾을 수 있지만, 내 membership卡(비밀번호)는 알 수 없다.

2. SAML은 **우리 학교 입구에서 한 번 신분증을 확인하면, 그 신분증으로 도서관, 운동장, 컴퓨터실 등 모든 곳에 출입할 수 있는 것**과 같아요. 각 시설(SP)이 다르게student守着 있지만, 한 번 학교 Office(IdP)에서 확인되면 모두 통하는 출입증이 있다.

3. computer 세상에서도 마찬가지예요. Google로 다른 앱에ログイン할 때( OAuth), 비밀번호를 앱에 주지 않고 Google이発行한 일회용 열쇠(Access Token)을 받아 사용하며, 회사에서 여러 서비스에Login할 때(SAML)는 한번 회사 시스템(IdP)에Login하면, 그 출입증으로 Salesforce, AWS 등 모든 서비스에 SSO로 접근할 수 있어요.
