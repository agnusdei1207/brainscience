+++
title = "37. OAuth 2.0 / OIDC"
weight = 37
+++

# 37. OAuth 2.0 / OIDC

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OAuth 2.0은 사용자의 비밀번호 없이 제3자 애플리케이션에 특정 리소스 접근 권한을 위임하는 개방형 권한 부여 표준이며, OIDC는 OAuth 2.0 위에 신원 인증 레이어를 추가한 개방형 신원 증명 프로토콜이다.
> 2. **가치**: OAuth 2.0과 OIDC는 안전한Third-party 앱 연동을 가능하게 하고, 사용자에게 편의성을 제공하며, 개발자에게 표준화된 인증/권한 부여 프레임워크를 제공함으로써 현대 웹과 모바일 애플리케이션의 인증 인프라로 폭넓게 활용된다.
> 3. **융합**: OAuth 2.0과 OIDC는 SSO, API Gateway, 마이크로서비스, Zero Trust 등 다양한 보안架构과 결합하여 현대 분산 환경에서 통합적 인증과 권한 관리를 실현한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

OAuth 2.0의 개념은 2006년 Twitter의 @anywhere 프로젝트에서 기원하며, 2012년에 RFC 6749로 표준화되었다. 그 전신인 OAuth 1.0 (RFC 5849)은 2007년 발표되었으나, 복잡성과 성능 문제로 인해 이후 OAuth 2.0이主流がとなった。 OAuth 2.0은 웹, 모바일, 데스크톱 애플리케이션에서 안전하게 Third-party 서비스에 대한 접근 권한을 부여하는 Industry 표준 프로토콜로 자리잡았다.

OIDC (OpenID Connect)는 2014년에 RFC 7388으로 표준화된 OAuth 2.0 기반의 신원 인증 레이어이다. OAuth 2.0이"접근 권한의 위임"에 초점을 맞추고 있다면, OIDC는"사용자 신원의 증명"에 초점을 맞춘다. OIDC는 ID Token을 통해 사용자의 신원을 확인하고, UserInfo Endpoint를 통해 추가적인 사용자 정보를 획득할 수 있게 한다. Google, Microsoft, Facebook, GitHub 등 주요 인터넷 기업들이 OIDC/OAuth 2.0을 활용한 인증을 제공하고 있으며, 이것은 现代 웹 애플리케이션의 기본 인증 인프라가 되었다.

OAuth 2.0과 OIDC가 필요한 근본적인 이유는 현대 컴퓨팅 환경의 분산성과 상호운용성 요구 때문이다. 하나의 애플리케이션이 다양한 외부 서비스(SNS 로그인,Payment, 지도, 캘린더 등)와連携하여 동작하는 경우가 보편화되었다. 사용자가 각 외부 서비스에 대한 자격 증명을 애플리케이션에 제공해야 한다면, 보안 위험이 크게 증가한다. OAuth 2.0과 OIDC는 사용자의 자격 증명를 공유하지 않고도 필요한 리소스에 대한 접근 권한을 부여받을 수 있게 함으로써, 보안과 편의성을 동시에 달성한다.

OAuth 2.0의 핵심 개념은 Authorization Server, Resource Server, Client, 그리고 Resource Owner이다. Authorization Server는 사용자를 인증하고 Client에게 Access Token을 발급하는 서버이고, Resource Server는 Access Token을 검증하고 요청된 리소스를 제공하는 서버이다. Client는 Resource Owner의리소스에 접근하려는 애플리케이션이고, Resource Owner는 리소스의소유자(일반적으로 최종 사용자)이다. OIDC에서는 여기에 Identity Provider (IdP)가 추가되어,Authorization Server가 사용자의신원까지 증명한다.

💡 OAuth 2.0과 OIDC를hotel의 명절을 통한 방문 허가 시스템에 비유하면, hotel 투숙객( Resource Owner)이 친구( Client)에게hotel 카드를 빌려주고 싶지만, 직접 비밀번호를 알려주고 싶지 않은 상황を考えよう. 그래서 투숙객은 reception( Authorization Server / IdP)에 직접 가서 친구에게일정 기간 동안 특정 층(Scope)만 접근할 수 있는 임시 카드를 발급받게 한다. reception은 투숙객의同意确认 후 임시 카드를 발급하고, 친구는 이 카드로 해당 层のすべての部屋に訪問할 수 있다. 이 과정에서友인은투숙객의 비밀번호를 알지 못하며, 발급된 카드에는有効기간과 접근 가능한区域が限定된다. 이것은 OAuth 2.0의 권한 부여 방식과 정확히 유사하다.

📢 OAuth 2.0과 OIDC는强大的な 도구이지만, 구현 시 보안에 各별한 주의가 필요하다. 잘못된 구현은 권한 탈취, 토큰 가로챔, 세션 하이재킹 등의 심각한 보안 취약점으로 이어질 수 있다. 특히 Authorization Code 흐름의 정확한 구현, 토큰의 안전한 저장, HTTPS의 필수 사용, CSRF 방지를 위한 state 매개변수 활용 등이重要하다. 또한 OAuth 2.0과 OIDC의 차이를 명확히 이해하고, 적절한 프로토콜을 선택하여 사용하는 것이 중요하다. 단순한 로그인이 목적이라면 OIDC가 적합하고, API 접근 권한 부여가 목적이라면 OAuth 2.0이 적합하다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

OAuth 2.0과 OIDC의 기술 아키텍처는 네 주요 구성요소와 네 가지 흐름(Flow)으로 이루어진다. 네 주요 구성요소는 Resource Owner (자원 소유자), Client (클라이언트), Authorization Server (권한 부여 서버), Resource Server (자원 서버)이다. OAuth 2.0에서 Authorization Server와 Resource Server는 분리되어 있을 수 있으나, OIDC에서는 Authorization Server가 동시에 IdP( Identity Provider) 역할도 담당한다.

OAuth 2.0의 네 가지 권한 부여 흐름은 다음과 같다. 第一은 Authorization Code 흐름으로, 웹 서버 사이드 앱에 적합한 가장安全性 높은 흐름이다. Client가사용자를Authorization Server로リダイレクト하고, 사용자가认证 후 Authorization Code를 Client에게 반환하며, Client가 이를 Access Token으로 교환한다. 第二는 Implicit 흐름으로, 과거 주로 브라우저 기반 앱에 사용되었으나, security问题로 인해非推奨되었다. Access Token이 URL片段로 직접 반환되어 보안 위험이 있다. 第三는 Resource Owner Password Credentials 흐름으로, 직접적인 사용자 자격 증명을 Access Token으로 교환하는もので, 매우 신 �뢰할 수 있는第一者 앱에만 적용 가능하다. 第四는 Client Credentials 흐름으로, Client가 사용자 대신 자신의 자격 증명으로 Access Token을 획득하는もので, machine-to-machine 통신에 사용된다.

```
┌─────────────────────────────────────────────────────────────────┐
│              OAuth 2.0 Authorization Code 흐름 아키텍처              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Resource Owner                                                │
│   (User)                                                        │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────┐     1. 인증 요청 (with Client ID, Redirect URI)   │
│   │ Client  │───────────────────────────────────────────────▶   │
│   │         │     (Authorization Server)                      │
│   └────┬────┘                                                    │
│        │     2. Authorization Server 로그인 페이지 표시        │
│        │◀──────────────────────────────────────────────────    │
│        ▼                                                        │
│   ┌─────────┐     3. 사용자 인증 + 동의                        │
│   │ Resource│─────────────────────────────────────────────────▶│
│   │ Owner   │                                                   │
│   └────┬────┘     4. Authorization Code 리다이렉트            │
│        │◀──────────────────────────────────────────────────    │
│        │                                                        │
│        ▼     5. Authorization Code                              │
│   ┌─────────┐──────────────────────────────────────────────▶   │
│   │ Client  │     6. Access Token + (Option: ID Token)       │
│   │         │◀────────────────────────────────────────────────│
│   └────┬────┘                                                    │
│        │     7. Access Token으로 Resource 요청                  │
│        ▼──────────────────────────────────────────────────▶    │
│   ┌─────────┐     8. Resource 제공                             │
│   │Resource │◀────────────────────────────────────────────────│
│   │ Server  │                                                   │
│   └─────────┘                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

OIDC의 핵심 원리 중 하나는 ID Token과 UserInfo Endpoint이다. ID Token은 JWT (JSON Web Token) 형태로, 사용자의신원 정보가 포함된 token이다. ID Token은 Authorization Server의 개인 키로署名되어 있으며, Client는 공개 키를 활용하여 token의 진위 여부를 검증할 수 있다. ID Token에는 일반적으로 Issuer, Subject (사용자 ID), Audience (Client ID), 만료 시간, 발급 시간 등의 Claims가 포함된다. 추가적인 사용자 정보(프로필, 이메일 등)는 UserInfo Endpoint를 호출하여 얻을 수 있다.

OAuth 2.0의 또 다른 핵심 원리는 Scope이다. Scope는 Client가 요청하는 권한의 범위를 나타내며,Authorization Server는 사용자에게Scope별同意를 구한다. 예컨대 Google의 경우,'email' scope는 이메일 주소에, 'profile' scope는 프로필 정보에, 'calendar' scope는 캘린더 정보에 접근하기 위한 권한을 요청한다. 사용자는 원하는 Scope만 동의할 수 있으며,授权된 Scope 범위 내에서만 Access Token이有効하다.

OIDC에서 중요한 원칙 중 하나는 Discovery와 Dynamic Registration이다. OIDC는 Authorization Server의Metadata (발급자 URL, 토큰 endpoint, 사용자 정보 endpoint, 공개 키 등)를 Discovery Document (.well-known/openid-configuration)에서 제공한다. Client는 이를 통해Authorization Server에 대한 정보를 자동으로 파악할 수 있다. 또한 Client는 Dynamic Registration을 통해事前に登録 없이도 Authorization Server에 등록할 수 있다. 이러한特性により、 OAuth 2.0/OIDC는非常に 유연하고 상호운용성 높은 시스템 구축이 가능하다.

📢 OAuth 2.0과 OIDC의 아키텍처는 아마추어 스포츠league의 통합 입장권 시스템과 같다.league 사무국( Authorization Server / IdP)이 선수와 팬( Resource Owner)의 신원을 확인하고, 등록된 팀과 협력사( Client)에 한해 특정 권한( Scope)을 부여한다. 일루어alinces는league 사무국에 등록하여 공식 협력사 자격을 얻고, 사무국이 발급한 임시 입장권( Access Token)을的玩家에 제공하여league 사무국이 인정한ファン에게만 услуги를 제공한다.league 사무국이全市家伙するため、팬들은複数の팀과 협력사를单数的な情報로 즐길 수 있다.

---

## Ⅲ. 구현 및 실무 응용 (Implementation & Practice)

OAuth 2.0/OIDC 기반의 Social Login実装では、 Google, Facebook, GitHub 등의 Third-party IdP를활용하여 사용자의 인증을 수행한다.実装 순서는 다음과 같다. 먼저 애플리케이션( Client)을 IdP에 등록하여 Client ID와 Client Secret을 발급받는다. 사용자가 Social Login 버튼을 클릭하면, 애플리케이션은 사용자를 IdP의Authorization Endpoint로リダイレクト한다. 사용자가 IdP에서 로그인하고 동의하면, IdP는 Authorization Code를 애플리케이션에 반환한다. 애플리케이션은 이 Code를 사용하여 IdP의 Token Endpoint에서 Access Token과 ID Token을 교환한다. ID Token을検証하여 사용자의신원을 확인하고, 애플리케이션에適切な会员 정보를 생성하거나 기존 회원과 연결한다.

API Gateway에서의 OAuth 2.0/OIDC 활용実装では、 API Gateway가 Authorization Server의 역할을 수행하거나, 기존 IdP와Integration하여 API 접근을 제어한다. Client가 API 요청과 함께 Bearer Token ( Access Token)을携带하면, API Gateway가 토큰을検証하고 유효하면 요청을 백엔드 서비스에 전달한다. 토큰이无效하거나scope가 부족하면 요청을 거부한다. 이를 통해 여러 백엔드 서비스에统一的된 인증/권한 부여 정책을 적용할 수 있다. 또한 OAuth 2.0의 Client Credentials 흐름을 활용하여, 서비스 간(machine-to-machine) API 접근에 대한 인증을 수행할 수도 있다.

마이크로서비스 아키텍처에서의 OAuth 2.0/OIDC 활용実装では、 모든 마이크로서비스가 공통의 IdP를활용하여 인증을 수행한다. API Gateway 또는 각 마이크로서비스가 Access Token의 유효성을 IdP에 검증 요청하거나, JWT 형태의 토큰인 경우 로컬에서直接検証한다. 이렇게 하면 각 마이크로서비스가 별도의 인증 로직을 구현할 필요 없이, IdP为中心的统一的 인증 체계를 운영할 수 있다. 그러나 주의할 점은, 토큰 검증 부담이 분산되지 않고 중앙화될 수 있으므로, JWT와 같은 Stateless Token 활용과适当的한缓存 전략이 필요하다.

Enterprise SSO로의 OAuth 2.0/OIDC 활용実装에서는、 企业内部 IdP (예: Azure AD, Okta, Keycloak)가 OIDC Provider 역할을 수행한다. 企业内의 다양한 애플리케이션들이 이 IdP를 통해 SSO를 실현한다. Azure AD는 Microsoft 생태계 전반의 SSO를 제공하고, Okta와 Keycloak은跨プラットフォーム SSO를 지원한다. SAML 2.0을 지원하는レガシー 애플리케이션의 경우, OIDC와 SAML 간のプロトコル変換을 제공하는中间층을 활용하여Enterprise SSO에 통합할 수 있다.

📢 OAuth 2.0/OIDC의 실무 적용에서 중요한 것은 적절한 Flow 선택과 보안 강화이다. 각 Flow는 서로 다른Use Case에 적합하며, 보안 수준도 다르다. 웹 서버 사이드 앱에는 Authorization Code 흐름이, 모바일 앱에는 PKCE (Proof Key for Code Exchange)를 활용한 Authorization Code 흐름이 적합하다. Implicit 흐름은 security問題로 인해使用하지 않는 것이 좋다. 또한 토큰의 안전한 저장(HTTP-only cookie, secure storage), CSRF 방지를 위한 state 매개변수, 그리고 HTTPS의 필수 사용 등이 반드시 적용되어야 한다.

---

## Ⅳ. 품질 관리 및 테스트 (Quality & Testing)

OAuth 2.0/OIDC의品質評價는 보안 강도, 상호운용성,性能, 그리고用户 편의성의 네 차원으로 구분된다. 보안 강도에서는 토큰 탈취 및 재생 공격 방지, CSRF 공격 방지, Authorization Code 유출 방지, 그리고잠재적 취약성 여부가 평가된다. 특히 Implicit 흐름의 사용 여부, PKCE 적용 여부, 토큰 만료 시간, 그리고 secure flag 사용 등이重点評価項目이다. 상호운용성에서는 다양한 IdP와 Client 조합, RFC 표준 준수 여부, 그리고 Discovery/Dynamic Registration 기능이 평가된다.性能에서는 토큰 발급 및 검증 시간, 그리고 대규모 접근 시의响应能力가 평가된다.用户 편의성에서는 로그인 흐름의 원활성, 오류 메시지의 명확성, 그리고재인증 빈도 등이 평가된다.

OAuth 2.0/OIDC의テスト方法論으로는相互운용性テスト, 보안テスト, 그리고负载テスト가 활용된다.相互운용性テスト에서는 다양한 IdP (Google, Microsoft, Okta, Keycloak 등)와 다양한 Client (웹, 모바일, CLI 등) 조합에서 OAuth/OIDC가 올바르게 작동하는지를 검증한다. OAuth의 다양한 흐름(Authorization Code, Client Credentials, PKCE 등)을 모두 테스트하고, Scope 별 동작을 검증한다. 보안テスト에서는 위에서 언급한各种 보안 위협에 대한 탐지 및 방지 능력을 검증한다.특히 OWASP OAuth 테스트 가이드를 활용한 체계적 보안 테스트가推奨된다.负载テスト에서는 대규모 동시 토큰 요청, 그리고 토큰 검증 부하에서システム性能가 기준을 충족하는지를 검증한다.

OAuth 2.0/OIDC의品質管理에서特别注意해야 할 영역은 토큰 관리와 IdP 종속성이다. Access Token과 Refresh Token의 안전한 저장,有効期限 관리, 그리고トークン 취소( revocation) 메커니즘이 중요하다. 또한 외부 IdP (Social Login 등)에의종속은危险因素가 될 수 있으므로, IdP 장애 시의 대응 계획(Graceful Degradation)도 마련되어야 한다. 외부 IdP가利用不可 시에도 자체 인증 수단을 제공하는 Backup Plan이 필요하다.

📢 OAuth 2.0/OIDC의品質 관리는은행의振り込め詐欺防止 시스템과 같다. 은행에서는고객의머니を 第三者に不移転시키기 전에, 다단계 인증, 거래 한도, 이상 거래 탐지 등 다양한安全 Measures를 적용한다. OAuth/OIDC도 마찬가지로 Authorization Code, PKCE, 토큰有效期, scope 제한, 그리고잠재적 이상 접근 탐지 등의 Measures를 통해 권한 탈취와 오남용을 방지한다. 또한振り込め詐欺対策で銀行が取る 다양한 조치처럼, OAuth/OIDC도 지속 진화하는脅威에 대응하기 위해 지속적으로更新되고 있다.

---

## Ⅴ. 최신 트렌드 및 결론 (Trends & Conclusion)

OAuth 2.0/OIDC의 최신 트렌드는 크게 세 가지 방향으로 전개되고 있다. 첫째, OAuth 2.1의 등장이다. OAuth 2.0은 여러 확장功能和 있지만, 가장安全性 높은 패턴을 표준화하기 위해 OAuth 2.1이 진행 중이다. OAuth 2.1에서는 PKCE의 필수화, 리다이렉트 URI의精确매칭, 그리고 일부 흐름의非推奨 등이 포함될 예정이다. 이는 OAuth 2.0의 أفضل 구현 패턴을 정리하여 개발자들의 올바른 구현을 유도하려는 시도이다.

둘째, GNAP (Grant Negotiation and Authorization Protocol)의 개발이다. GNAP는 OAuth 2.0의후계 프로토콜로, 보다 유연하고현대적인 권한 부여 프로토콜을 제공하는 것을 목표로 한다. 현재 초안 단계이며, 긴급한 요구사항을addresses하기 위해 개발 중이다. GNAP은 OAuth 2.0의 핵심 개념을 계승하면서도, 새로운 사용 사례(기기 권한 부여, 위임된 권한管理等)への対応및セキュリティ 개선을 제공한다.

셋째, Self-Sovereign Identity (SSI)와의Integration이다. Decentralized Identity ( DID )와 블록체인 기반 신원 증명 기술이 발전함에 따라, OAuth/OIDC와 SSI를Integration하는アプローチ가 연구되고 있다. 전통적인 IdP 중심 모델에서 벗어나, 사용자가 자신의신원을 관리하는新しい paradigm으로의 evolution이 진행되고 있다. 이는 OAuth/OIDC의根本적인 변화보다는확장으로 해석할 수 있으며, 장기적으로 신원 관리의格局에 변화를 가져올 수 있다.

OAuth 2.0/OIDC의 미래를展望하면, 다음과 같은 발전이 예상된다. OAuth 2.1 또는 GNAP을 통한 보안 강화가 이루어질 것이며, SSI/ DID와의Integration이加速화될 것이다. 또한生物識別 기반 인증과 결합하여, 더욱便捷하고安全な 인증 환경이實現될 것으로 전망된다. Machine-to-Machine (M2M) 인증에서의 OAuth 활용도 확대되어, IoT, Edge Computing 등에서 안전한 Device 인증이 가능해질 것이다. 그러나 기본적인 프로토콜의 개념은 유지될 것으로 보이며, 개발자들은 OAuth/OIDC의 기초概念을 명확히 이해하고, 지속적으로 변화하는 표준을跟随하는 것이重要하다.

📢 OAuth 2.0과 OIDC는현대 웹과 모바일 애플리케이션의 인증/권한 부여를 기초부터 다시 定义한重要的標準이다. 이 프로토콜들은 개발자들에게 표준화된 안전한 인증 방법을 제공하고, 사용자들에게便捷한 접근성을 제공하며, 기업들에게統合적 인 IAM 관리 역량을 부여한다. 그러나 이들도万能은 아니며, 올바른 구현과 지속적인 보안 관리가 필수적이다. 개발자들은 OAuth/OIDC의 동작原理을 깊이 이해하고, 보안最佳实务를 준수하여应用해야 한다.

---

## 핵심 인사이트 ASCII 다이어그램 (Concept Map)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OAuth 2.0 / OIDC 개념도                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                         ┌───────────────────┐                       │
│                         │   안전한 Third-  │                       │
│                         │   party 접근 위임 │                       │
│                         └─────────┬─────────┘                       │
│                                   │                                 │
│                         ┌─────────▼─────────┐                       │
│                         │  Authorization   │                       │
│                         │  Server / IdP   │                       │
│                         └─────────┬─────────┘                       │
│                                   │                                   │
│         ┌─────────────────────────┼─────────────────────────┐     │
│         │                         │                         │     │
│ ┌───────▼───────┐         ┌───────▼───────┐         ┌───────▼──────┐│
│ │ Auth Code    │         │ PKCE + Auth   │         │ Client      ││
│ │ Flow (Web)   │         │ Code (Mobile) │         │ Credentials  ││
│ │              │         │               │         │ (M2M)       ││
│ └───────┬───────┘         └───────┬───────┘         └───────┬──────┘│
│         │                         │                         │       │
│         └─────────────────────────┼─────────────────────────┘       │
│                                   │                                   │
│                         ┌─────────▼─────────┐                       │
│                         │  Access Token    │                       │
│                         │  + ID Token (OIDC)│                       │
│                         └───────────────────┘                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 참고
- OAuth 2.0: Open Authorization 2.0 (개방형 권한 부여 2.0)
- OIDC: OpenID Connect (오픈아이디 커넥트)
- RFC: Request for Comments (인터넷 표준 문서)
- IdP: Identity Provider (신원 제공자)
- Client: 권한 부여를 요청하는 애플리케이션
- Resource Owner: 리소스 소유자 (일반적으로 사용자)
- Authorization Server: 권한 부여 서버
- Resource Server: 리소스 서버
- Scope: 권한 범위
- JWT: JSON Web Token (제이슨 웹 토큰)
- PKCE: Proof Key for Code Exchange (코드 교환용 비밀鍵)
- SSO: Single Sign-On (단일 로그인)
- SSI: Self-Sovereign Identity (자가 주권 신원)
- DID: Decentralized Identifier (분산 신원 식별자)
- GNAP: Grant Negotiation and Authorization Protocol (권한 협상 및 부여 프로토콜)
- CSRF: Cross-Site Request Forgery (사이트 간 요청 위조)
- M2M: Machine-to-Machine (머신투머신)
