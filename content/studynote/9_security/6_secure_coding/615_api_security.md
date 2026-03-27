+++
title = "API 보안"
description = "REST, GraphQL, gRPC 등 현대 API 아키텍처의 보안 전략"
date = 2024-01-15
weight = 15
+++

# API 보안 (API Security)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: API 보안은 내부 로직을 외부에 노출하는 API Gateway로서의 특성上, 인증(Authentication), 인가(Authorization), 입력 검증(Input Validation), 출력 인코딩(Output Encoding), 속도限制(Rate Limiting), 감사 로깅(Audit Logging) 등의 다층 방어를 통해 malicious traffic과 무단 접근을 방지하는 것이다.
> 2. **가치**: 현대 애플리케이션의 대부분이 API를 통해 데이터를 교환하며, 2023년 Akamai 보고에 따르면 전 세계 인터넷 트래픽의 30%이상이 API 호출이다. 주요 유출 사고(2019년 Facebook, 2021년 LinkedIn)의 상당수가 API 취약점을 利用했다.
> 3. **융합**: API 보안은 OAuth 2.0, OpenID Connect, JWT, TLS, WAF, API Gateway, GraphQL Security, GraphQL Shield 등 인증/인가 프로토콜과 깊이 결합한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

API 보안(API Security)은 웹 API, REST API, GraphQL, gRPC, WebSocket 등 다양한 API 아키텍처를 악의적인 abuse나 부적절한 사용으로부터 보호하는 종합적 보안 전략이다. API는 내부 데이터와 로직을外部에 노출하는窓口 역할을 하므로, 적절한 인증과 인가 없이는 누구나 민감 데이터에 접근할 수 있게 된다. 또한 API는 입력의 출입구가 되므로, 입력 검증과 출력 인코딩이 없으면 SQL 주입, XSS, 명령어 주입 등의 서버사이드 취약점의piercing이 가능하다. API 보안은 이러한 모든 공격 벡터를カバー하기 위해 인증, 인가, 입력 검증, 속도 제한, 감사 로깅, TLS 적용 등을 포함한다.

### 필요성

API가 중요한 이유는다음과 같다. First, API는 데이터의 主入口(Entry Point)로서, 모바일 앱, 웹 앱, 제3자 서비스, IoT 장치 등이 모두 API를 통해 백엔드 데이터에 접근한다. 따라서 API의 보안이 곧 데이터의 보안으로 이어진다. Second, APIsms Stateless하게 설계되는 경우가 많아, 각각의 요청이독립적으로 인증되어야 하며, 이는 전통적인 세션 기반 인증과는 다른 보안 접근이 필요하다. Third, REST API는 HTTP를 기반으로 하므로, 웹 취약점(SQL 주입, XSS, CSRF 등)이 동일하게 적용되며, GraphQL은 추가적으로 쿼리 복잡도 공격, 인트로스펙션 남용, 배치 공격 등의 고유한 보안 위협이 있다. Fourth, 제3자에게 API를開放하면 Attack Surface이 확대되어, 악의적인 제3자뿐 아니라，合法的であってもセキュリティ이 부족한 제3자를 통한 유출也可能성이 있다.

### 💡 비유

API 보안은 고급 호텔의コンシェルジュ 데스크와 같다. 호텔 손님(인증된 사용자)은コンシェルジュ(API)를 통해 방 키(데이터 접근)를 요청하고,コンシェルジュ는 손님의 identity와 권한을 확인한 후(인가) 방 키를 제공한다. 만약コンシェルジュ가 아무런 확인 없이 방 키를提供하면, 누구나hotel의모든 방에 접근할 수 있게 된다. 또한 손님이 이상한 요청("100번 방의 열쇠를 줘")을 하면(입력 검증 실패), 그것을 처리해서는 안 된다.レート限制は、"同一人からの過剰なリクエスト"防备する。

### 등장 배경 및 발전 과정

2000년 Roy Fielding의博士論文에서REST(Representational State Transfer)가 소개되면서 웹 API의 패러다임이 확립되었고, 2000년대後반 Salesforce, Amazon, eBay 등이公共 API를提供하기 시작했다. 2010년대에는 Facebook이 GraphQL을, Google이 gRPC를 도입하여 새로운API 아키텍처가 등장했다. 2019년 OAuth 2.0 RFC 6749, 2020년 OpenID Connect 1.0의 표준화로API 인증/인가의 기본 프레임워크가 성숙했다. 2021년 OWASP는 "API Security Top 10"을 발표하여 API 특유의 보안 위협(Broken Object Level Authorization, Broken Authentication, Excessive Data Exposure, Lack of Resources & Rate Limiting 등)을 정리했다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### OWASP API Security Top 10

OWASP API Security Top 10은 API에 특화된 가장 위험한 보안 위협을 순위로 정리한 것으로, 2019년 첫 版이 发布되었고 2023년에 更新되었다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    OWASP API Security Top 10 (2023)                     │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [API1: Broken Object Level Authorization (BOLA)]                  │
  │
  │  설명: API가 객체 접근 제어를 제대로 구현하지 않아, 공격자가 다른         │
  │        사용자의 객체에 접근 가능한 취약점                                │
  │  예시: GET /api/orders/{orderId} 에서 orderId을 조작하여 타인의 주문 접근  │
  │  방어: 객체 단위 인가 검사, 사용자-객체 관계 검증                       │
  │
  │  [API2: Broken Authentication]                                       │
  │
  │  설명: API 인증 메커니즘이不安全하게 구현되어, 정체성을偽装하거나        │
  │        세션을탈취할 수 있는 취약점                                       │
  │  예시: JWT 서명 검증 없음, 평문 비밀번호 전송, 부적절한 세션 무효화       │
  │  방어: JWT 검증, MFA, 안전한 세션 관리                                  │
  │
  │  [API3: Broken Object Property Level Authorization]                │
  │
  │  설명: 객체의 특정 속성에 대한 접근 제어가 없어, 민감 속성이 노출되는       │
  │  예시: 관리자 속성(isAdmin) 반환, 비밀번호 hash 포함 응답               │
  │  방어: 속성 단위 인가 검사, 민감 데이터 필터링                           │
  │
  │  [API4: Unrestricted Resource Consumption]                          │
  │
  │  설명: API가 자원 소비를 제한하지 않아, DoS나 과금 리스크가 있는          │
  │  예시: 무제한 파일 업로드, 과도한 DB 쿼리, 큰 페이징                      │
  │  방어: Rate Limiting, 리소스 할당량 설정, 페이징 제한                     │
  │
  │  [API5: Broken Function Level Authorization]                        │
  │
  │  설명: 관리자 기능에 대한 접근 제어가 부적절하여, 일반 사용자가            │
  │        관리자 API에 접근 가능한 취약점                                    │
  │  예시: POST /api/admin/users 에서 관리자 권한 검증 없음                  │
  │  방어: 역할 기반 접근 제어, 명시적 권한 검사                              │
  │
  │  [API6: Unrestricted Access to Sensitive Business Flows]            │
  │
  │  설명: 민감한 비즈니스 흐름(비밀번호 변경, 계정 삭제 등)에 대한           │
  │        접근 제어가 없어,自動化された 공격에 노출                           │
  │  예시: 무차별 비밀번호 시도, 계정 열거, 자동화된 선물 코드 redemption      │
  │  방어: Rate Limiting, CAPTCHA, 계정 잠금 정책                           │
  │
  │  [API7: Server Side Request Forgery (SSRF)]                        │
  │
  │  설명: API가 사용자 제공 URL을 검증 없이 가져와서, 내부 시스템에          │
  │        접근 가능한 취약점                                                │
  │  예시: GET /api/fetch?url=http://169.254.169.254/metadata           │
  │  방어: URL 화이트리스트, DNS rebinding 보호,Ingress/Egress 필터링       │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** BOLA(Broken Object Level Authorization)는 API Security Top 10의 1위로, 가장 흔한 API 취약점이다. API가 GET /api/orders/123으로 주문 정보를 반환할 때,攻击자가订单 ID만 바꿔서 GET /api/orders/456으로 다른 사용자의 주문 정보에 접근할 수 있다. 방어 위해서는 각 API endpoint에서 요청자의 권한을 검증하여, 요청 객체에 대한 접근 권한이 있는지 확인해야 한다. Broken Authentication은 JWT 토큰을 검증하지 않거나, 인증 토큰을URL 파라미터로 전달(로깅/히스토리 노출)하는 등의 부적절한 구현에서 비롯된다. Excessive Data Exposure는 API가 기본적으로 모든 객체를 반환하고, 클라이언트 사이드에서 필터링하도록 기대하는 설계에서 발생한다. 이는 프론트엔드 필터링만으로는 부족하며, API Gateway 또는응답 직전 필터링을 통해 불필요한 데이터가 반환되지 않도록 해야 한다.

### API 인증 전략

API 인증은 요청자를 식별하는 메커니즘으로,API 키, Basic Authentication, Bearer Token(JWT), OAuth 2.0, OpenID Connect 등 다양한 방식이 있다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    API 인증 방식 비교                                    │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [API 키 (API Key) - ⚠️ 단순하지만 제한적]                            │
  │
  │  사용: X-API-Key: abc123... 헤더                                     │
  │  장점: 단순, 이해하기 쉬움                                            │
  │  단점: rotation 어려움, 권한 모델 없음, 누구에게나 유효                │
  │  권장: 공개 데이터/ Rate-limited API에 만성                              │
  │
  │  [Basic Authentication - ⚠️ TLS 필수]                                 │
  │
  │  사용: Authorization: Basic base64(username:password)               │
  │  장점: 간단한 구현                                                    │
  │  단점: 매 요청마다 자격 증명 전송, SSO 불가                            │
  │  권장: 내부 서비스 간 통신 (TLS 필수)                                   │
  │
  │  [JWT (JSON Web Token) - ✅ 널리 사용]                                │
  │
  │  사용: Authorization: Bearer eyJhbGciOiJIUzI1...                      │
  │  구조: Header.Payload.Signature                                       │
  │  장점: Stateless, 확장 가능, 서명/암호화 가능                          │
  │  단점: 토큰 크기, rotation 관리 필요                                   │
  │  권장: 일반적인 웹/모바일 앱 API 인증                                  │
  │
  │  [OAuth 2.0 + OpenID Connect - ✅ 권장 (특히 제3자 액세스)]            │
  │
  │  사용: Authorization Code Flow + PKCE (권장)                         │
  │  흐름: 사용자가 서비스 A에서 서비스 B 데이터 접근-authorize 요청        │
  │        → 사용자 identity provider에서 인증                            │
  │        → 서비스 A에 authorization code 전달                           │
  │        → 서비스 A가 authorization code를 token으로 교환                │
  │  장점: credential 공유 없음, 세분화된 권한(Scope) 관리, SSO           │
  │  권장: 제3자 앱 통합, SSO, 마이크로서비스 인증                         │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** API 키는 가장 단순한 인증 방식으로, API 제공자가API 소비자에게 고유 키를 부여하고, 소비자는 매 요청 시 해당 키를 헤더에 포함한다. 그러나 키 유출 시rotation이 어려우며,API 키 자체에 권한 개념이 없으므로 모든API에 대한 접근 권한을 보유한다. Basic Authentication은 username:password를 base64로 인코딩하여 전송하므로,TLS 없이는 패킷 스니핑으로 자격 증명이 탈취될 수 있다. JWT는 Self-contained Token으로, 토큰 자체에 사용자 정보와 권한(Claims)이 포함되어 있어 서버에서 검증이 가능하다. Stateless하므로 확장성이 뛰어나지만, 토큰이 노출되면有効时间内はずっと有効이다. 따라서 토큰 lifetime을 적절히 설정하고, HttpOnly 쿠키로 관리하거나refresh 토큰 메커니즘을 활용해야 한다. OAuth 2.0은 제3자에게 제한된 권한으로 서비스 접근을 허용하는delegation 프로토콜로, OpenID Connect는 OAuth 2.0 위에ID federation 레이어를 추가하여 사용자 인증을 가능하게 한다.

### GraphQL 보안

GraphQL은 REST와 다른 고유한 보안 위협을 가지며, 쿼리 복잡도, 인트로스펙션 남용, 배치 공격,_subscriptions에 대한 DDoS 등이 있다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    GraphQL 보안 위협 및 방어                             │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [威胁 1: 쿼리 복잡도 공격]                                           │
  │
  │  예시: nestedQuery { user { posts { comments { author { posts {...} }}}}}  │
  │  위험: 다단계 중첩 쿼리로 서버 자원 고갈                               │
  │  방어: 쿼리 깊이 제한 (maxDepth), 복잡도 분석 (query cost analysis)    │
  │
  │  [威胁 2: 인트로스펙션 남용]                                           │
  │
  │  예시: __schema, __type으로 전체 API 스키마 탈취                     │
  │  위험: 공격자에게API 구조Mapper提供                                    │
  │  방어: 프로덕션에서 인트로스펙션 비활성화 또는 권한 설정                 │
  │
  │  [威胁 3: 배치 공격 (Batching Attack)]                                │
  │
  │  예시: POST /graphql에 다수의 쿼리를 배열로 전송                      │
  │       [ {query: "query { user(id:1) {...} }"},                       │
  │         {query: "query { user(id:2) {...} }"}, ... ]                  │
  │  위험: Rate Limiting 우회, 一括 데이터 탈취                            │
  │  방어: 요청 레벨 Rate Limiting, 쿼리 수 제한                          │
  │
  │  [防御 전략]                                                         │
  │
  │  - Depth Limiting: 최대 중첩 깊이 제한                                │
  │  - Complexity Limiting: 쿼리 복잡도 점수 기반 제한                   │
  │  - Pagination: pageSize 기본값 설정, 최대값 제한                     │
  │  - Introspection 비활성화 (프로덕션)                                  │
  │  - Queryallow-list: 사전 승인된 쿼리만許可                           │
  │  - Timeouts: 쿼리 실행 시간 제한                                      │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** GraphQL의 인트로스펙션 기능은 개발 단계에서는API 스키마를 탐색하기에 유용하지만, 공격자에게 전체API 구조(어떤 타입, 어떤 필드가 있는지)를一览同仁に提供하여,攻撃者は표적화된 공격을策划할 수 있다. 따라서 프로덕션 환경에서는 인트로스펙션을 비활성화하거나, 최소한 권한이 있는 사용자만 접근 가능하도록 설정해야 한다. 쿼리 복잡도 공격은 10단계 이상 중첩된 쿼리로 서버의 computation 자원을 소진시키는 공격으로, GraphQL Shield, graphql-rate-limit 등의 라이브러리로 쿼리 깊이와 복잡도를制限해야 한다.

- **📢 섹션 요약 비유**: API 보안은은행의 ATM 시스템과 같다. ATM(API)은 누구나(Authentication) 접근할 수 있지만, 자신의 계좌(개별 객체 접근)에만 접근이 허용되고(Authorization), 한 사람당 하루 인출 가능액(레이트 리밋)이 제한되며, 이상한 요청(입력 검증)이 있으면 거절하고, 모든 거래가 기록(로깅)되어야安全가保障된다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### REST vs GraphQL vs gRPC 보안 비교

| 측면 | REST | GraphQL | gRPC |
|:---|:---|:---|:---|
| **인증** | API Key, JWT, OAuth | JWT, OAuth | mTLS, JWT |
| **인가** | RBAC, ABAC | 필드 단위 인가 | RBAC, ALTS |
| **입력 검증** | 스키마/템플릿 검증 | GraphQL 스키마 기반 자동 검증 | Protocol Buffers |
| **Rate Limiting** | API Gateway |Apollo, graphql-rate-limit | Envoy, proxy |
| **주 위협** | BOLA, 과도한 데이터 노출 | 쿼리 복잡도, 인트로스펙션 | 프로토콜漏洞 |

### 과목 융합 관점

- **네트워크 보안**: API Gateway(WAF)가API 앞단에서 DDoS, SQL 주입, XSS 등 전통적 웹 공격을 탐지하고, TLS로 전송 구간을 암호화한다.
- **마이크로서비스**: Kubernetes/Ingress Controller에서 mTLS(상호 TLS) 통신으로 서비스 간API 통신을 보호하고, 서비스 메시(Service Mesh)가 사이드카로API 보안을 제공한다.
- **규제 준수**: PCI DSS는 카드 데이터 API 접근에 강력한 인증과 암호화를 요구하며, GDPR은 개인데이터 처리에 대한API 접근을 logs에 기록하도록要求한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — API Gateway를 통한API 보안**: AWS API Gateway + Lambda로 구축된서버리스 API에, Cognito로JWT 인증을 적용하고, API Gateway의기본 Rate Limiting(초당 100요청)을 설정하며, WAF를 통합하여OWASP Top 10 공격을 탐지/차단하는 구조 구현.

2. **시나리오 — GraphQL API의 인트로스펙션 보호**: Apollo Server GraphQL API에서 프로덕션 환경에서는 인트로스펙션을 비활성화하고, 쿼리 최대 깊이를 10으로 제한하며, 복잡도 분석을 통해 비용이 1000을 초과하는 쿼리를 거부하도록 구현.

### 도입 체크리스트

- **기술적**: 모든 API endpoint에서 인증/인가가 적용되어 있는가? Rate Limiting이 설정되어 있는가? 입력 검증이 되어 있는가?
- **조직적**: API 보안 정책(API 키 관리, 접근 권한 관리)이 수립되어 있는가?

### 안티패턴

- **BOLA (Broken Object Level Authorization)**: API가 user_id만 검증하지 않고 객체를 반환하는 것은 가장 흔한 API 취약점이다.
- **과도한 데이터 반환**: API가 객체의 모든 필드를 반환하고, 클라이언트에서 필터링하도록 기대하는 것은 Dangerous하다.
- **Rate Limiting 부재**: Rate Limiting이 없으면 무차별 대입, 데이터 탈취, DDoS 공격에 노출된다.

- **📢 섹션 요약 비유**: API 보안은콘서트会場의 입구 관리와 같다. 표(API Key/토큰)를 가지고 있는 사람만이 입장에 허용되고(인증), 표 종류에 따라 좌석 등급이 다르게(인가) 하고, 한 사람이 표를 여러 번 났을 경우(레이트 리밋) 퇴장시키고,袋 Inspection(입력 검증)을 해서 위험 물질은 반입을 차단하며, 모든 출입이 기록(로깅)되어야event가 안전하게 진행된다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | API 보안 미도입 | API 보안 도입 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | API 유출 사고 5건 | 0건 | 사고 100% 방지 |
| **정량** | Rate Limiting 없어 DDoS | Rate Limiting + WAF | DDoS 방어 |
| **정성** | API 보안 정책 부재 | OAuth 2.0 + RBAC | 안전한 제3자 통합 |

### 미래 전망

GraphQL, gRPC, WebSocket 등 새로운API 기술의 보편화와 함께API 보안의 중요성이 더해 증가하고 있다. 또한 API Gateway, Service Mesh, WAAP(Web Application and API Protection) 등의 통합 보안 플랫폼이API 보안을 더 효율적으로 만들어주고 있다. AI/ML 기반 API 보안 모니터링(Aban, Splunk 등)도 발전하여, 비정상적API 사용 패턴을 실시간으로 탐지하고 대응하는 것이 가능해지고 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **OAuth 2.0** | 제3자에게 제한된 권한으로 서비스 접근을 허용하는delegation 프로토콜로, API 보안의核心이다. |
| **JWT** | Self-contained Token으로, Stateless한API 인증을 가능하게 하며, 서명/암호화되어 무결성을 보장한다. |
| **OWASP API Security Top 10** | API에 특화된 주요 보안 위협을 순위로 정리한 것으로,API 보안の優先순위 결정에 활용된다. |
| **API Gateway** | API 앞단의Proxy/방어벽으로, 인증, Rate Limiting, WAF 등을 제공한다. |
| **GraphQL Security** | GraphQL 특유의 보안 위협(쿼리 복잡도, 인트로스펙션, 배치 공격)을방어하기 위한_specialized 기법이다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. API 보안은 **학교 도서관의 도서 대출 시스템**과 같아요. 학생증(API Key/토큰)을 가지고 있는 사람만이 도서를 대출(데이터 접근)할 수 있고, 대출 할 수 있는 도서 수는 제한되어 있으며(레이트 리밋), 무효한 학생증으로는 아무 책도 대출할 수 없어요.

2. 만약 시스템이 学生証(인증) 확인만 하고, 해당 학생이 이미 대출 중인 책인지는 확인하지 않으면(인가 검증 실패), 한 사람이 동일한 책을 여러 번 대출 받을 수 있어요. 이것은 도서관 시스템의問題인 동시에, 보안漏洞과 같아요.

3. 컴퓨터의 API도 마찬가지예요. 누군가API를 통해 데이터에 접근하려고 하면(요청), 그 사람이 정말 그 데이터에 접근할 권한이 있는지를 확인하고(인가), 요청 횟수를 제한하며(레이트 리밋), 이상한 요청(입력 검증)은 거부해야 시스템이安全하게 작동해요.
