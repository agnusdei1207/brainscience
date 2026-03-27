+++
title = "Kerberos 인증"
description = "대규모 네트워크를 위한 통합 인증 프로토콜 Kerberos의 원리와 보안"
date = 2024-01-15
weight = 5
+++

# Kerberos 인증 (Kerberos Authentication)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kerberos는 MIT Athena 프로젝트에서 개발된 대칭키 암호화 기반의 네트워크 인증 프로토콜로, 단일 사인온(SSO)을 통해 사용자가 한 번의 인증으로 여러 서비스에 접근할 수 있으며, 모든 통신이加密化되어 있어 네트워크 스니핑를 통한 정보 유출을 방지한다.
> 2. **가치**: Microsoft Active Directory의 기반 인증 프로토콜로、Windows Server, Exchange, SharePoint 등의 핵심 통신 보호에 사용되며, 대칭키 암호화의 효율성과 중앙 집중형 인증 관리로 인해 대규모 企业環境에서 표준으로 자리잡았다.
> 3. **융합**: Kerberos는 대칭키 암호학(DES, AES), 공개키 암호학(PKI, X.509), 시간 동기화(NTP), 그리고icket lifetimes와授权의 관점에서 중앙집중식 접근 제어와 깊이 결합한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

Kerberos는 대칭키 암호화(주로 AES)를 기반으로 한 네트워크 인증 프로토콜로, 사용자와 서비스가 서로를 인증할 수 있도록وسط의 신뢰할 수 있는 제3자(KDC: Key Distribution Center)가음을 수행한다. Kerberos의 핵심 원칙은 "비밀번호를 네트워크로 전송하지 않는다"는 것이다. 사용자는 비밀번호에서 파생된 키로初始認証을 수행하지만, 이후 모든 통신에서는 대칭 키를基とした加密化이 적용되어秘密情報がネットワーク上に流れることがない。

Kerberos는 Greek mythology에서冥界의 문을 지키는 세-headed 개에서 유래했으며, 이는Authentication의守护者を 의미한다.

### 필요성

네트워크 환경에서 사용자를 인증하는 것은 중요한 문제이다. 사용자가 네트워크 서비스에 접근할 때, 그 서비스는 해당 사용자를信用해야 한다. 그러나 각 서비스가 직접 사용자를 인증하려면, 모든 서비스가 비밀번호 데이터베이스를 보유해야 하고, 사용자는 각 서비스마다 비밀번호를 입력해야 한다. Kerberos는 중앙 집중형 인증을 통해この問題を解決する。 사용자는 한 번 로그인하여 TGT(티켓Granting Ticket)를 발급받고, 이 TGT를 利用하여 각 서비스의 티켓을请求한다. 모든 과정이 대칭키 암호화로 보호되어, 网络上에서 비밀번호나 중요한 정보가流れることがない。

### 💡 비유

Kerberos는 **고급 레스토랑의 VIP member system**과 같다. 입구에서 회원卡(비밀번호)를 제시하면、レセプショニスト가 확인 후 VIP 티켓(TGT)을 발급한다. 이후 레스토랑 내의 모든 서비스(바, 메인 룸, 카페 등)에 접근할 때마다 VIP 티켓을 제시하면 별도의 비밀번호 없이 접근이 가능하다. 모든 과정이内部システムで管理되고、외부에서는 누구가 무엇을 이용하는지 알 수 없다.

### 등장 배경

1980년대 MIT Athena 프로젝트에서 개발되었으며,1993년 RFC 1510로 표준화되었다.2005년 RFC 4120으로 업데이트되어 현재는 AES 암호화 지원,、SPNEGO negotiation,Extensions등이 포함된 최신 버전이 사용된다. Microsoft는 Windows 2000부터 Active Directory의 기본 인증 프로토콜로 Kerberos를 채택하여 기업 환경에서 대규모 사용되고 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Kerberos 아키텍처 구성 요소

Kerberos 시스템은 세 가지 주요 구성 요소로 이루어진다: Client, Application Server, 그리고 Key Distribution Center (KDC).

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    Kerberos 아키텍처                                      │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  ┌─────────────────────────────────────────────────────────────┐   │
  │  │                     Key Distribution Center (KDC)              │   │
  │  │                                                           │   │
  │  │  ┌─────────────────────┐      ┌─────────────────────┐      │   │
  │  │  │   Authentication   │      │    Ticket Granting │      │   │
  │  │  │      Service        │      │       Service       │      │   │
  │  │  │        (AS)        │      │        (TGS)       │      │   │
  │  │  │                     │      │                    │      │   │
  │  │  │  - 사용자 인증       │      │  - TGT 검증       │      │   │
  │  │  │  - TGT 발급         │      │  - 서비스 티켓 발급 │      │   │
  │  │  └─────────────────────┘      └─────────────────────┘      │   │
  │  │              │                        │                     │   │
  │  │              └───────────┬────────────┘                     │   │
  │  │                          │                                   │   │
  │  │              Database (Account Info + Master Key)            │   │
  │  └─────────────────────────────────────────────────────────────┘   │
  │                          │                                          │
  │                          ▼                                          │
  │         ┌─────────────────────────────────────┐                  │
  │         │         Application Server            │                  │
  │         │  (File Server, DB Server, Web, etc.) │                  │
  │         └─────────────────────────────────────┘                  │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** KDC는 Kerberos 시스템의核心で、Authentication Service (AS)와 Ticket Granting Service (TGS)로 구성된다. AS는 사용자를 인증하고 TGT를 발급하는 역할을 하며, TGS는 TGT를 검증하고 다른 서비스에 대한 티켓을 발급하는 역할을 한다. KDC는 모든 사용자和服务의 master key를 저장하고 있으며,、これらの 키는 사전에 각 사용자/서비스와 KDC 之间에서 공유되어 있다.

### Kerberos 인증 흐름

Kerberos 인증은 크게 세 단계로 구성된다: Initial Authentication, Service Ticket Acquisition, 그리고 Service Access.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    Kerberos 인증 흐름                                      │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [Phase 1: 초기 인증 - KRB_AS_REQ / KRB_AS_REP]                    │
  │
  │  Client ──▶ Authentication Service (AS)                              │
  │
  │  Client: "나는 사용자 Alice이고, 내 비밀번호로 인증하고 싶다"          │
  │              │                                                      │
  │              │  KRB_AS_REQ (encrypted with user's key)              │
  │              │  - client_name, realm, timestamp                       │
  │              ▼                                                      │
  │         AS는 사용자의 master key로 복호화하여認証                     │
  │              │                                                      │
  │              ▼                                                      │
  │  Client ◀── KRB_AS_REP                                               │
  │         - TGT (Ticket Granting Ticket) - service로의 access 없음     │
  │         - Session Key (client-TGS 간 공유 키)                         │
  │              │                                                      │
  │              │  TGT는 TGS의master key로 encrypted                   │
  │              │  Session Key는 사용자의 master key로 encrypted         │
  │              ▼                                                      │
  │         사용자는 비밀번호로 Session Key를 복호화하여 기억             │
  │
  │  [Phase 2: 서비스 티켓 요청 - KRB_TGS_REQ / KRB_TGS_REP]           │
  │
  │  Client ──▶ Ticket Granting Service (TGS)                            │
  │
  │  "나는 파일 서버에 접근하고 싶다 (TGT 첨부)"                         │
  │              │                                                      │
  │              │  KRB_TGS_REQ                                          │
  │              │  - TGT, Authenticator (client info)                  │
  │              │  - service_principal_name (원하는 서비스)              │
  │              ▼                                                      │
  │         TGS는 TGT를 자신의master key로 복호화하여 검증               │
  │              │                                                      │
  │              │  "이 사용자는 유효한 TGT를 가지고 있다"                 │
  │              ▼                                                      │
  │  Client ◀── KRB_TGS_REP                                              │
  │         - 특정 서비스용 Ticket                                        │
  │         - Client-Service 간 Session Key                              │
  │
  │  [Phase 3: 서비스 접근 - KRB_AP_REQ / KRB_AP_REP]                  │
  │
  │  Client ──▶ Application Server                                      │
  │
  │  "파일 서버에 접근하겠다 (서비스 티켓 첨부)"                          │
  │              │                                                      │
  │              │  KRB_AP_REQ                                           │
  │              │  - 서비스 티켓, Authenticator                         │
  │              ▼                                                      │
  │         Application Server는 자신의master key로 티켓 복호화           │
  │              │                                                      │
  │              │  "이 사용자는 인증되었고, 이 서비스 접근 권한이 있다"    │
  │              ▼                                                      │
  │  Client ◀── Application Server                                      │
  │         (Mutual Authentication - 서버도client에게 자신을 인증)      │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Phase 1에서 사용자는 자신의 비밀번호로 Authentication Service에 접근한다. AS는 사용자의 master key로 요청을 복호화하여 사용자를 인증하고, TGT와 Session Key를 발급한다. 사용자는 자신의 비밀번호로 Session Key를 복호화하여 유지한다. 중요한 점은, 사용자의 비밀번호에서 파생된 키가 直接 네트워크에流れることはなく、복호화된 결과만 로컬에서 사용된다. Phase 2에서 사용자는 TGT를 첨부하여 Ticket Granting Service에 서비스 티켓을 요청한다. TGS는 TGT를 검증하여 사용자의 신원을 확인하고, 서비스용 티켓과 해당 서비스와 사용자 간의 Session Key를 발급한다. Phase 3에서 사용자는 서비스 티켓을 Application Server에 제시한다. Application Server는 자신의 master key로 티켓을 복호화하여 검증한다. Kerberos는 상호 인증(Mutual Authentication)을 지원하여, 사용자에게服务服务器を確認，也能防止恶意的服务器欺骗。

### Kerberos 보안 특성

Kerberos는 다양한 보안 메커니즘을 통해 네트워크 인증의安全性を保障한다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    Kerberos 보안 특성                                    │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [1. 비밀번호 네트워크 전송 없음]                                      │
  │
  │  ❌ 위험: 다른 프로토콜 (FTP, Telnet 등)                            │
  │     사용자 비밀번호가 네트워크를 통해 평문으로 전송                      │
  │                                                                     │
  │  ✅ Kerberos:                                                        │
  │     비밀번호에서 파생된 키로 복호화 작업만 Local에서 수행               │
  │     네트워크에는 이미 암호화된 상태의 인증 정보만 흐른다                 │
  │
  │  [2. 상호 인증 (Mutual Authentication)]                             │
  │
  │  Client ──▶ Service: "접근 요청"                                      │
  │     Service ──▶ Client: "내가 맞는지 확인" (Challenge/Response)      │
  │                                                                     │
  │  ◀── 서비스도 사용자에게 자신을 인증해야 함                             │
  │  ◀── 악의적인 서버 (스푸핑) 방지                                      │
  │
  │  [3. Single Sign-On (SSO)]                                          │
  │
  │  사용자는 한 번만 인증 (TGT 획득)                                    │
  │  이후 여러 서비스 접근 시 추가 인증 불필요                              │
  │  각 서비스 티켓은 해당 서비스에만 유효                                  │
  │
  │  [4.icket 제한된 유효 기간]                                          │
  │
  │  TGT: 일반적으로 8~10시간                                           │
  │  서비스 티켓: 일반적으로 수분~수시간                                  │
  │                                                                     │
  │  ◀── 티켓이 도난되어도 제한된 시간 동안만 사용 가능                    │
  │
  │  [5. Cross-Realm 인증 지원]                                         │
  │
  │  다른 Kerberos 도메인(Realm)의 사용자에게서                           │
  │ _cross-realm trust__를 통해 서비스 접근 허용                           │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Kerberos의 가장 중요한 보안 특성 중 하나는秘密である。 사용자가 Authentication Service에 접근할 때, 사용자의 비밀번호에서 파생된 키는 오직 로컬에서 만 복호화에 사용되고, 네트워크上에는 이미 암호화된 상태의 인증 정보만이 흐른다. 따라서 네트워크 스니핑을 통해 비밀번호를 탈취하는 것이 불가능하다. Mutual Authentication은 사용자가 서비스에 접근할 때,服务服务器也必须向用户证明自己的身份，防止恶意服务器的欺骗。 SSO를 통해 사용자는 한 번의 인증으로 여러 서비스에 접근할 수 있어 편의성과 安全性を同時に達成する。 티켓의 유효 기간이 제한되어 있어,万一 티켓이 도난되어도 제한된 시간 동안만 사용 가능하다는 것도重要なセキュリティ上の考慮事项である。

- **📢 섹션 요약 비유**: Kerberos는 **고급 카지노의 VIP chip system**과 같다. 입구에서 회원증을 보여주고(비밀번호 확인) VIP chip (TGT)을 받으면, 이후 블랙잭 테이블, 룰렛, 바 등 어떤 테이블에서도 VIP chip만 제시하면 되고, 각 테이블staff도 VIP chip이 진짜인지 확인할 수 있다. 모든 것이 내부 관리되므로 외부에서 누가 무엇을 하는지 알 수 없으며, chip에는 유효 기간이 있어서 도난되어도 오래되면 무효가 된다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### Kerberos vs 其他 인증 프로토콜

| 비교 항목 | Kerberos | NTLM | LDAP | SAML/OIDC |
|:---|:---|:---|:---|:---|
| **암호화** | 대칭키 (AES) | MD4/NTLM hash | plaintext/简单bind | XML/JSON 서명 |
| **SSO** | 네이티브 지원 | 동일 도메인만 | 제한적 | 웹 SSO |
| **티켓 방식** | 티켓 기반 | LM/NTLM 해시 | 클라이언트 credentials |Assertion |
| **주 사용처** | Windows AD | 레거시 Windows | Directory service | 웹/App |
| **공격 어려움** | 높음 | 낮음 | 중간 | 높음 |

### 과목 융합 관점

- **운영체제**: Microsoft Windows Active Directory에서 기본 인증 프로토콜로 사용되며,모든Windows Server 및 많은Enterprise Application에서 지원된다.
- **암호학**: 대칭키 암호화(AES, DES)를 기반으로 하며, 티켓 발급 시키의 키 배포 문제를 해결한다.
- **네트워크**: NTP(Network Time Protocol)와의 동기화가 필수적이며, 시간 어긋남이 크면 티켓 검증에 실패한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — Windows AD 환경의 파일 서버 접근**: 사용자가 Windows 도메인에 로그인하면, Kerberos를 통해 TGT가 자동으로 발급되고, 이후 파일 서버, SharePoint, Exchange 등 다양한 서비스에 별도의 로그인 없이 접근한다.

2. **시나리오 — Kerberos 공격: Pass the Ticket**: 공격자가 메모리에서 TGT를 탈취하여 자신의 세션에 주입하고,受害자의 권한으로 서비스에 접근하는 공격. 방어를 위해 CredGuard (Credential Guard)를 통해lsass.exe를 보호하고, 티켓ifetime을 줄이며, Lateral Movement를 모니터링한다.

### 도입 체크리스트

- **기술적**: KDC가 安全하게管理되고 있는가? 티켓 lifetime이 적절한가?
- **운영·보안적**: NTP 동기화가 유지되고 있는가? Pass the Ticket 공격에 대한 방어가 되어 있는가?

### 안티패턴

- **긴 티켓 수명**: 티켓 수명이 길면 도난 시 더 오래 활용될 수 있다.
- **느슨한 Cross-Realm Trust**: 불필요하게 넓은 trust 설정은 공격 표면을 확대한다.
- **느슨한时钟 동기화**: NTP 동기화 오류가 크면 티켓 검증에 실패하거나, 공격에 활용될 수 있다.

- **📢 섹션 요약 비유**: Kerberos는 **카지노 VIP 시스템**과 같다. 회원증 확인 후 VIP chip을 받으면, 어떤 테이블에서도 chip만 제시하면 되고,staff도 chip의 진위를 확인할 수 있다. 모든 것이 중앙 chip로 관리되고, chip에는 유효 기간이 있어 도난 시에도 제한된 시간만 사용할 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 개별 인증 | Kerberos SSO | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | N개 서비스에 N회 인증 필요 | 1회 인증으로 N개 접근 | 사용자 편의성 대폭 향상 |
| **정성** | 네트워크 평문 비밀번호 유출 위험 | 대칭키加密化으로 안전 | 정보 유출 위험 최소화 |

### 미래 전망

Kerberos는 현재 Windows AD 환경의 표준 인증 프로토콜로 자리잡고 있으나, 차세대 인증(FIDO2, WebAuthn, PKI)과의 통합이 진행되고 있다. Microsoft는 Windows Hello for Business를 통해 FIDO2/WebAuthn과 Kerberos를 연결하여, passwordless 인증을 Kerberos 환경에서 가능하게 하고 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **KDC (Key Distribution Center)** | Kerberos의核心 구성 요소로, Authentication Service와 Ticket Granting Service로 구성된다. |
| **TGT (Ticket Granting Ticket)** | 사용자가 KDC로부터 발급받는 티켓으로, 이를 利用하여 서비스 티켓을 요청한다. |
| **Single Sign-On (SSO)** | 한 번의 인증으로 여러 서비스에 접근할 수 있는 능력으로, Kerberos가네이티브하게支援한다. |
| **Active Directory** | Microsoft의目录服务로, Kerberos를기본 인증 프로토콜로 활용한다. |
| **Pass the Ticket** | Kerberos 티켓을 탈취하여 공격에 활용하는手法으로, Credential Guard 등으로 방어한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. Kerberos는 **우리 학교에서 여러 동아리에 들어갈 때의 시스템**과 같아요. 먼저 선생님께(Authentication Service) 회원증을 보여주고(비밀번호 확인) 특별한 티켓(TGT)을 받으면, 이후 음악부, 미술부, 과학부 등 어떤 동아리에 가도 그 티켓만 보여주면 들어갈 수 있어요. 각 동아리staff도 티켓의 진위를 확인할 수 있죠.

2. 중요한 점은学校外에서는(네트워크를 통해) 비밀이나 개인 정보를やり取り하지 않는다는 거예요. 안에 들어갈 때는 미리 безопас하게處理되어 있고, 외부에서는 아무도 무슨 동아리에 가는지 알 수 없어요.

3. 그리고 그 티켓에는有效 기간이 있어서, 도난再怎么しても 시간이 지나면 사용할 수 없게 되어 있어요. 이것이 바로 Kerberos의 보안 방법이고, 학교(기업)에서는 이 시스템으로 학생들(직원)의 일처리(서비스 접근)를安全하게管理하는 거예요.
