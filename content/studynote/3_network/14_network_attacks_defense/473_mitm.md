+++
weight = 14
title = "MITM (중간자 공격) 및 스니핑 (Sniffing)"
description = "MITM 공격의 원리, ARP 스푸핑, SSL 스트립핑, 세션 하이재킹, 패킷 스니핑 도구를شرح"
date = 2024-01-28

[extra]
categories = ["studynote-software-engineering"]
tags = ["mitm", "man in the middle", "arp spoofing", "session hijacking", "sniffing"]

+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MITM(Man-in-the-Middle, 중간자) 공격은 공격자가 두 당사자 사이의 통신 경로에 끼어들어 양쪽 모두의通信을 도청하고 조작할 수 있게 하는 공격으로, 기본적으로 네트워크의 투명한 존재로 위장한다.
> 2. **가치**: MITM 공격은 공개 WiFi 환경에서 특히 치명적이며, SSL/TLS 암호화 없는 HTTP 세션이나无效한 인증서検証을 통해 금융 정보, 세션 쿠키, 자격 증명을 탈취할 수 있어 피해 규모가 크다.
> 3. **융합**: 현대 MITM 방어 기술(HSTS, Certificate Pinning, HTTPS Everywhere)은 암호화와 인증 강화를 통해 투명한 공격을防止하고 있으며, DNSSEC은 DNS레벨의 MITM 공격까지 방어한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념

MITM(Man-in-the-Middle) 공격은 두 당사자(A와 B)가 서로 통신한다고 생각하지만, 실제로는 공격자(M)가 그 사이에서通信을 가로채고 탈취 또는 조작하는 공격이다. 공격자는 양쪽 모두에게 자신이另一方이라고 가장하며,通信의 내용을 도청(기밀성 침해)하거나 조작(무결성 침해)할 수 있다.

### 필요성

MITM 공격은 네트워크 수준에서 발생할 수 있는 가장基本的な 공격 중 하나이다. 공개 WiFi,企业内部 네트워크, 甚至는 ISP 수준에서 발생할 수 있으며, 공격자가同一 네트워크에 있으면 ARP 스푸핑 등을 통해很容易하게 수행할 수 있다. 특히 모바일 뱅킹, 전자상거래 등 financial 트랜잭션에서 MITM 공격이 성공하면使用자의 금융 정보가 탈취되어巨大的한 금전적 피해를 입힐 수 있다.

### 등장 배경

MITM 공격의概念은 오래되었지만, 1990년대 IEEE 802.11 WEP의 결함 발견과 함께 WiFi 환경에서의 MITM 공격이 사회적으로 주목받았다. 이후 2010년 도.firebug와 类似 도구로 HTTPS 세션의 쿠키를 탈취하는 "SideJacking" 또는 "Session Hijacking" 공격이 알려졌고, 2014년 Apple의 "goto fail"/goto-fail SSL 취약점, 2017년 KRACK( WPA2 키 재설치 공격) 등 MITM 관련 취약점이 지속적으로 발견되고 있다.

### 💡 비유

MITM 공격은 **"편지를 전달하는 우체부 사이의 악당"** 에 비유할 수 있다. A가 B에게 편지를 보낼 때,evil 우체부가 A에게 "나는 B의 우체부"라고 가장하여 편지를 横取り하고, B에게는 "나는 A의 우체부"라고 가장하여 전달한다. 양쪽 다 모르고 정상적으로通信한다고 생각하지만, evil 우체부가 내용을 읽고 조작할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### MITM 공격 절차

MITM 공격은 크게 3단계로 구성된다. 첫째, 공격 대상 사이의通信 경로에 위치하도록 하고(entry), 둘째, 해당 경로를 투명하게維持하며(establishment), 셋째, 정보를 탈취하거나 조작한다(manipulation).

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    MITM 공격의 3단계 절차                                      │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  [정상 통신]                                                           │
  │
  ///  [Alice] ◀─────────────────────────▶ [Bob]                           │
  ///           (암호화된 안전信道?)                                           │
  │
  │  [Entry: 끼어들기]                                                      │
  │
  ///  [Alice]     [Eve]      [Bob]                                         │
  ///       │       │         │                                              │
  ///       │    공격자       │                                              │
  ///       │       │         │                                              │
  ///       └───────┴─────────┘                                             │
  │         Alice와 Bob 사이에 Eve가 위치                                    │
  │
  │  [Establishment: 경로 확보]                                             │
  │
  ///  기법 1: ARP Spoofing (ARP 캐시poisoning)                             │
  ///  Eve → Alice: "Bob의 IP는 내 MAC이야" ( spoofed ARP reply)           │
  ///  Eve → Bob: "Alice의 IP는 내 MAC이야" ( spoofed ARP reply)          │
  ///  결과: Alice와 Bob 모두 Ethernet 프레임을 Eve에게 보냄                  │
  │
  ///  기법 2: DNS Spoofing ( DNS 캐시poisoning)                             │
  ///  Eve가 DNS 응답을 조작하여 합법적 도메인을 공격자 IP로 유도                │
  ///
  ///  기법 3: WiFi Evil Twin (공격자 액세스 포인트)                          │
  ///  합법 AP와 동일한 SSID의 가짜 AP를 운영하여 사용자를 유도                │
  ///
  │  [Manipulation: 탈취/조작]                                               │
  │
  ///  [패션 1: 도청 (Passive Eavesdropping)]                               │
  ///  Eve가 Alice와 Bob 사이의 통신을 단순히 지켜봄                          │
  ///  (암호화되어 있으면 내용만 있고, 암호화되지 않으면 내용도 탈취)          │
  ///
  ///  [패션 2: 세션 하이재킹 (Active Interception)]                         │
  ///  Eve가 Alice의 세션 쿠키를 탈취하여 Bob인 것처럼 위장                   │
  ///  (SideJacking: HTTPS 쿠키 탈취)                                         │
  ///
  ///  [패션 3: 내용 조작 (Active Manipulation)]                             │
  ///  Eve가 HTTP 응답의 내용을 조작 (예:银行 계좌번호 변경)                  │
  ///
  │
  │  [ARP Spoofing 상세 과정]                                              │
  │
  ///  [Alice]          [Eve]           [Bob]                                │
  ///     │              │               │                                    │
  ///     │  ARP 요청:    │               │                                    │
  ///     │──▶ "Bob IP의 MAC은?" ──▶│                                     │
  ///     │              │               │                                    │
  ///     │              │  ARP 응답 (스푸핑):                                │
  ///     │              │◀── "Bob의 MAC은 내 MAC" ──│                     │
  ///     │ ◀─── Bob의 MAC은 Eve ───│                                      │
  ///     │              │               │                                    │
  ///     │  ARP 요청:    │               │                                    │
  ///     │──▶ "Alice IP의 MAC은?" ──▶│                                     │
  ///     │              │  ARP 응답 (스푸핑):                                │
  ///     │              │◀── "Alice의 MAC은 내 MAC" ──│                   │
  ///     │ ◀─── Alice의 MAC은 Eve ───│                                      │
  ///     │              │               │                                    │
  ///     │◀════════════▶│◀════════════▶│ Alice ◀════════════▶ Bob          │
  ///     │    (Eve가 Forwarding하며 도청/조작)                               │
  │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** ARP Spoofing은 LAN 환경에서 가장 흔한 MITM 기법이다. ARP는 IP 주소를 MAC 주소로 변환하는 프로토콜로, 보안 기능이 없어서任何人이 ARP 응답을 보낼 수 있다. 공격자는 victim's ARP 캐시를 조작하여 "gateway IP → 공격자 MAC"으로 매핑하고, 동시에 gateway에게는 "victim IP → 공격자 MAC"으로 매핑하여 victim과 gateway 사이의 모든 트래픽을 통과시킨다. ARP 스푸핑이怖い 이유는 Switch环境下でもMAC 주소 테이블을 통한 정상 방어가 불가능하고, 공격자가同一 네트워크에만 있으면 누구나実行可能이기 때문이다. 또한 IPv6 환경에서는 NDP(Neighborhood Discovery Protocol) 스푸핑이 유사한 역할을 한다.

---

### SSL/TLS Stripping 및 세션 하이재킹

HTTPS 세션에서도 MITM 공격이 가능하다. SSL Stripping은 사용자가 HTTPS 접속을 시도할 때 공격자가 HTTP로 downgrading시키는 기법이고, Session Hijacking은 세션 쿠키를 탈취하여 정당한 사용자인 것처럼 위장하는 기법이다.

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                 SSL Stripping 및 세션 하이재킹 동작 원리                          │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  [SSL Stripping (HTTPS Downgrade 공격)]                                 │
  │
  ///  [victim]    [Eve]         [web server]                              │
  ///     │           │               │                                      │
  ///     │  HTTP 요청 (http://site.com/login) │                              │
  ///     │──────────▶│               │                                      │
  ///     │           │  Eve가 HTTP→HTTPS 리다이렉트 막음 +                │
  ///     │           │  HTTP 응답을 victim에게 전달                         │
  ///     │◀──────────│               │                                      │
  ///     │           │               │                                      │
  ///     │  HTTP 요청 (평문!)        │                                      │
  ///     │──────────▶│──────────────▶│  (Eve가 HTTPS 요청을 HTTP로 변환)   │
  ///     │           │               │                                      │
  ///     │  HTTP 응답 (평문!)        │                                      │
  ///     │◀──────────│◀──────────────│  (Eve가 HTTPS 응답을 HTTP로 변환)   │
  ///     │           │               │                                      │
  ///     │  ← Eve가 평문 내용을 읽고 조작 가능! →                           │
  ///
  ///  방어: HSTS (HTTP Strict Transport Security)                           │
  ///  • 웹서버가 HSTS 헤더 전송: "이 도메인은 HTTPS만 허용"                  │
  ///  • 브라우저가 이후 항상 HTTPS로만 접속 (downgrade 불가능)              │
  ///
  │  [Session Hijacking (세션 가로채기)]                                   │
  │
  ///  시나리오: Mallory가 Alice의 세션 쿠키를 탈취하여 Bob인 것처럼 위장       │
  ///
  ///  [Alice]        [Mallory]       [Server]                              │
  ///     │              │              │                                     │
  ///     │  POST /login (cred)         │                                     │
  ///     │────────────▶│──────────────▶│                                     │
  ///     │              │  인증 성공, 세션 쿠키 SET-COOKIE 반환              │
  ///     │◀────────────│◀──────────────│                                     │
  ///     │              │              │                                     │
  ///     │  이후 요청에 쿠키 포함                                        │
  ///     │◀════════════▶│◀════════════▶│                                     │
  ///     │              │              │                                     │
  ///     │         Mallory가 Alice의 쿠키를 탈취!                            │
  ///     │              │              │                                     │
  ///     │              │  쿠키만 사용해서 Same 요청! (세션 하이재킹)           │
  ///     │              │─────────────▶│  (Alice인 것처럼 Server 접근)        │
  ///     │              │              │                                     │
  ///
  ///  방어:                                                                  │
  ///  • SSL/TLS 암호화 (쿠키 가로채기 어려움)                                 │
  ///  • HttpOnly, Secure 쿠키 플래그                                         │
  ///  • Session Regeneration (로그인 후 SID 갱신)                             │
  ///  • Certificate Pinning (특정 인증서만 허용)                               │
  │
  │  [KRACK: WPA2의 키 재설치 공격]                                          │
  ///
  ///  WPA2의 4-Way Handshake 취약점:                                         │
  ///  • 공격자가 3번째 메시지(재설치 유도)를 가로챔                              │
  ///  • nonce 값이 재설정되어 동일 키 스트림으로 복호화 가능                    │
  ///  • WPA3(SAE)는 이 공격에 면역                                            │
  ///
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** SSL Stripping의 핵심 문제는 웹 서비스가 HTTP와 HTTPS를 모두 지원할 때, 공격자가 사이에서 HTTP 응답을 가로채어 HTTPS 리다이렉트를 제거하면 victim이 암호화되지 않은 HTTP 세션에서 통신하게 되는 것이다. HSTS(HTTP Strict Transport Security)는 서버가 "이 도메인은 반드시 HTTPS로만 접근해야 한다"는 정보를 브라우저에 전달하여, 이후 브라우저가 강제로 HTTPS로만 접속하게 함으로써 이 공격을防止한다. Session Hijacking은 쿠키의 HttpOnly 플래그(JavaScript 접근 불가)와 Secure 플래그(HTTPS에서만 쿠키 전송)로 완화할 수 있지만, 쿠키 자체가 탈취되면 防げない部分이 있다. 因此 서버측에서 세션 갱신(Session Regeneration)이 필수적이다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### MITM 방어 기술 종합

| 방어 기술 | 보호 대상 | 동작 원리 | 제한 |
|:---|:---|:---|:---|
| **HTTPS (SSL/TLS)** | 도청, 내용 조작 | 전체 통신 암호화 | 인증서 검증 실패 시 무력화 |
| **HSTS** | SSL Stripping | 강제 HTTPS 접속 | 첫 방문은 보호 불가 ( preload 필요) |
| **Certificate Pinning** | FAKE 인증서 | 특정 인증서만 허용 | 앱 업데이트 시핀 관리 필요 |
| **DNSSEC** | DNS Spoofing | DNS 응답에 디지털 서명 |廣范围 배포 아직 미흡 |
| **ARP Monitoring** | ARP Spoofing | ARP 테이블 이상 탐지 | 탐지만, 자동 방어는 별도 필요 |
| **VPN** | 전체 MITM | 전체 트래픽 암호화 터널 | 성능 overhead, 신뢰된 VPN 필요 |

### MITM 공격 유형별 방어 매트릭스

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    공격 유형별 방어 방법 매트릭스                                   │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  공격 유형                │ 탐지 방법              │ 방어 방법              │
  │  ───────────────────────────────────────────────────────────────────│
  │  ARP Spoofing            │ ARP 테이블 모니터링    │ 정적 ARP 설정, VLAN 분할 │
  │  DNS Spoofing            │ DNSSEC, DNS 모니터링  │ DNSSEC 활성화          │
  │  WiFi Evil Twin          │ AP 인증 정보 확인     │ WPA3, VPN 사용         │
  │  SSL Stripping           │ HSTS, HTTPS Everywhere │ HSTS Preload, VPN     │
  │  Session Hijacking       │ 쿠키 모니터링         │ HttpOnly, Session 갱신  │
  │  KRACK (WPA2)            │ WPA3으로 업그레이드   │ firmware 패치          │
  │  PHY-layer Jamming       │ 주파수 모니터링       │ 周波数 도약, RAID    │
  │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 각 MITM 공격 유형은 서로 다른 특성을 가지고 있어, 개별적인 방어 방법이 필요하다. ARP Spoofing은 VLAN 분할(VLAN Segmentation)로 확산 범위를 제한하고, 정적 ARP로 사전에 알지 못한 ARP 응답을 차단한다. DNSSEC은 DNS 응답에 공개키 기반의 디지털 서명을 붙여, 스푸핑된 DNS 응답을探索 불가능하게 만든다. 그러나 현재 DNSSEC의 실무 적용률은 높지 않아서, 추가적으로 DNS over HTTPS(DoH)나 DNS over TLS(DoT)를 활용하여 DNS 查询 자체를 암호화하는 것이 좋다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 기업 내부 MITM 공격 탐지 및 대응**: 보안팀이 내부 네트워크에서 ARP Spoofing 공격이 발생하고 있음을 탐지한 상황. ARP 테이블 모니터링 도구(例: arpwatch)로 이상 ARP 응답을 탐지하고, 공격자의 MAC/IP를特定한 후, 해당 포트를 네트워크 스위치에서 차단한다. 동시에 DHCP Snooping과 Dynamic ARP Inspection(DAI)을 활성화하여 ARP 스푸핑을 네트워크 장비 수준에서 자동으로 방지한다.

2. **시나리오 — 모바일 뱅킹 앱의 MITM 방어**: 금융 앱 개발팀이 앱의 MITM 공격 방어를 설계하는 상황. 핵심 방어 수단으로 Certificate Pinning을 적용하여, 앱이 특정 인증서(또는 공개키)만 신뢰하도록 한다. 이를 통해 공격자가 자신의 인증서를 삽입하더라도 앱이 이를 거부하여 연결이 실패한다. 그러나 핀이 앱 내에 hardcoded되어 있으므로, 핀을 업데이트하려면 앱을 업데이트해야 하는 management 부담이 있다.

3. **시나리오 — WiFi 환경에서 MITM 걱정**: 사용자가 카페의 공개 WiFi에 연결하여 온라인 활동을 수행하려는 상황. 공개 WiFi는 MITM 공격에 취약하므로, 항상 HTTPS만 사용하는 것이 기본이다. HTTPS Everywhere 브라우저 확장 프로그램을 활용하여 가능한 한 HTTPS로만 접속하도록 하고, 가능하다면 VPN을 사용하여 모든 트래픽을 암호화된 터널로 보호한다. HTTP만 지원하는 사이트는 절대 사용하지 않는다.

### 도입 체크리스트

- **기술적**:企业内部에서 HSTS가 모든 웹 서비스에 적용되어 있는가? Certificate Pinning이 모바일 앱에 적용되어 있는가? DNSSEC이 지원되는 DNS 서비스로 이전했는가?
- **운영·보안적**: ARP 모니터링이 실시되고 있는가? MITM 공격 대응 절차(SOP)가 수립되어 있는가?

### 안티패턴

- **무효한 SSL/TLS 검증**: 개발 환경에서 SSL/TLS 검증 기능을 무효화하고 production에도 동일한 코드가 남아 있으면, MITM 공격에完全히 노출된다.
- ** 自서명 인증서 (Self-signed Certificate)**: 내부적으로 自서명 인증서를 사용하면, 공격자도 동일한 인증서를 생성하여 MITM 공격에 악용될 수 있다. 내부 CA를 통한 엄격한 인증서 관리와 함께, 인증서 순환(rotation)을 정기적으로 수행해야 한다.

- **📢 섹션 요약 비유**: MITM 공격은 **"은행 턴stile 앞의 Escrow 서비스"** 에 비유할 수 있다. Alice가 Bob(은행)에게 돈을 보내려고 하는데, Mallory가 Escrow 담당이라고 속여 금액을 확인하고 조작한 후 Bob에게 전달한다. Alice와 Bob 모두 모른 채 Mallory만 거래 내용을 알게 되는 것이다. 방어(HSTS, Pinning, VPN)는 이러한 Escrow를 배제하고银行과 직접取引하는 것에 비유할 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

- **Post-Quantum Cryptography**: 양자컴퓨터가 Shor 알고리즘으로 RSA/ECC를 해결하면, 현재 TLS 1.3의 암호학적 기반이 무력화될 수 있다. NIST PQC 표준화(Round 4~5)와 함께 양자내성 키 교환으로의 전환이 필요하다.
- **零信任 네트워크 (Zero Trust)**: "절대 신뢰하지 말고, 매번 검증"하는 Zero Trust 모델이普及되면, MITM 공격의 효과를根本적으로 줄일 수 있다. 모든 통신이 인증과 암호화로 보호되고, 이상 접근 패턴은 즉시 차단된다.

### 참고 표준

- NIST SP 800-52: TLS 구현 가이드라인
- RFC 6797: HSTS (HTTP Strict Transport Security)
- RFC 7469: Certificate Pinning

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **ARP Spoofing (ARP 캐시 poison)** | LAN 환경에서 ARP 응답을 조작하여 victim의 ARP 테이블을 tampering하고, 통신 트래픽을 공격자에게 유도하는 MITM 기법이다. |
| **SSL Stripping** | HTTPS 접속을 HTTP로 downgrade하여 암호화되지 않은 평문 통신을 유도하는 MITM 기법으로, HSTS로 방어한다. |
| **Session Hijacking** | 세션 쿠키를 탈취하여 정당한 사용자인 것처럼 위장하는 기법으로, HttpOnly, Secure 플래그와 Session 갱신으로 완화한다. |
| **HSTS (HTTP Strict Transport Security)** | 서버가 브라우저에 "이 도메인은 HTTPS로만 접근하라"고 지시하여, 이후 브라우저가 HTTP downgrade를 거부하게 하는 보안 메커니즘이다. |
| **Certificate Pinning** | 앱이나 브라우저가 특정 인증서 또는 공개키만 신뢰하도록 하여, 중간에 삽입된 악성 인증서를 통한 MITM을防止한다. |
| **KRACK (Key Reinstallation Attack)** | WPA2의 4-Way Handshake 취약점을 利用하여 nonce를 재설치시키고, 동일 키 스트림으로 암호문을 해독하는 공격이다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. MITM 공격은 **"편지 사이의 악당 우체부"** 예요. A가 B에게 편지를 보내면,evil 우체부가 중간에서，横取り해서 내용을 읽고, 내용을 바꿔서 B에게 전달해요. A와 B는 모르고 있는 거예요.
2. ARP 스푸핑은 **"주소록 조작 범죄"** 예요. 친구의 전화번호를 악당이 자신의 번호로 바꿔치기하면, 친구에게 전화하면恶당이 받아버리는 거예요.
3. SSL/TLS는 그 편지를 **"암호화된 금고 갑옷"** 에 넣는 것과 같아요. 金庫의 열쇠는 받는 사람만이 가지고 있어서, 중간에서 横取り해도 열쇠가 없으면 내용을 알 수 없어요. HSTS는 "이 사람의 편지는 반드시 金庫 갑옷으로만 배달하라"고 정하는 규칙이에요.
