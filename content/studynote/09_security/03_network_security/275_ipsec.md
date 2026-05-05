+++
weight = 275
title = "275. IPsec (Internet Protocol Security)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: IPsec (Internet Protocol Security)은 IP 패킷 자체를 인증·암호화하는 **네트워크 레이어(Layer 3)** 보안 프레임워크로, 상위 애플리케이션이 변경 없이 투명하게 보호받는 것이 핵심 가치다.
> 2. **가치**: RFC 4301로 표준화된 IPsec은 VPN (Virtual Private Network)의 핵심 프로토콜로, AH (Authentication Header)와 ESP (Encapsulating Security Payload) 두 프로토콜을 Transport/Tunnel 두 모드로 운용한다.
> 3. **판단 포인트**: IPsec은 구성 요소(AH/ESP/IKE)와 모드(Transport/Tunnel)의 조합이 복잡하므로, 각 컴포넌트의 역할과 적용 시나리오를 매트릭스로 정리해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

인터넷의 기반 프로토콜인 IP는 보안을 전혀 고려하지 않고 설계됐다. 패킷 위조, 도청, 재전송 공격에 원천적으로 취약하다. TLS (Transport Layer Security)가 응용 레이어에서 특정 애플리케이션을 보호하는 반면, IPsec은 **IP 계층에서 모든 트래픽을 투명하게 보호**한다는 차별점이 있다.

IPsec의 핵심 장점은 **투명성(Transparency)**이다. TCP (Transmission Control Protocol), UDP (User Datagram Protocol), ICMP (Internet Control Message Protocol) 등 모든 상위 프로토콜이 애플리케이션 수정 없이 IPsec 보호를 받는다. 반면 TLS는 각 애플리케이션이 TLS 라이브러리를 명시적으로 사용해야 한다.

IPsec은 1990년대 IETF (Internet Engineering Task Force)에서 IPv6 필수 요소로 설계됐으나, IPv4에서도 선택적 확장으로 광범위하게 사용된다. RFC 4301(IPsec 아키텍처), RFC 4302(AH), RFC 4303(ESP), RFC 7296(IKEv2)이 현재 표준이다.

주요 사용 사례: Site-to-Site VPN (기업 거점 간 연결), Remote Access VPN (재택근무자 기업망 접근), 클라우드-온프레미스 하이브리드 연결, 라우터 간 동적 라우팅 프로토콜 보호.

📢 **섹션 요약 비유**: IPsec은 모든 편지를 배달 전에 자동으로 봉투에 넣고 봉인하는 우체국 시스템이다. 편지 쓰는 사람(애플리케이션)은 봉투를 신경 쓸 필요가 없다.

---

## 2. 구성요소

### IPsec 컴포넌트 구조

```
┌─────────────────────────────────────────────────────────┐
│                    IPsec 아키텍처                        │
│                                                         │
│  ┌─────────────┐    ┌─────────────────────────────┐    │
│  │ 보안 정책   │    │    IKE (Internet Key         │    │
│  │ 데이터베이스│    │    Exchange) v2              │    │
│  │ (SPD)       │    │    SA 협상 및 키 관리         │    │
│  └──────┬──────┘    └──────────────┬──────────────┘    │
│         │                          │                    │
│         ▼                          ▼                    │
│  ┌─────────────────────────────────────────┐           │
│  │  보안 연관 데이터베이스 (SAD, Security  │           │
│  │  Association Database)                  │           │
│  │  SA = SPI + 알고리즘 + 키 + 수명        │           │
│  └─────────────┬───────────────────────────┘           │
│                │                                        │
│         ┌──────┴──────┐                                │
│         ▼             ▼                                 │
│    ┌─────────┐  ┌───────────┐                         │
│    │   AH    │  │    ESP    │                          │
│    │ 인증 전용│  │ 인증+암호화│                         │
│    └─────────┘  └───────────┘                         │
└─────────────────────────────────────────────────────────┘
```

### IPsec 핵심 개념

| 개념 | 설명 | 비고 |
|:---|:---|:---|
| SA (Security Association) | 단방향 보안 매개변수 집합 | 양방향 = 2개 SA |
| SPI (Security Parameters Index) | SA 식별자 (32비트) | 패킷에 포함 |
| SPD (Security Policy Database) | 트래픽별 IPsec 처리 정책 | Bypass/Discard/Protect |
| SAD (Security Association Database) | 활성 SA 목록 | SPI로 검색 |
| AH (Authentication Header) | 프로토콜 번호 51 | 무결성+인증, 암호화 없음 |
| ESP (Encapsulating Security Payload) | 프로토콜 번호 50 | 무결성+인증+암호화 |
| IKE (Internet Key Exchange) | SA 자동 협상 프로토콜 | UDP 포트 500/4500 |

**암호 알고리즘** (RFC 8221 현행 권고):
- 기밀성: AES-GCM-128/256 (권장), 3DES (레거시)
- 무결성: HMAC-SHA2-256/384/512
- 키 교환: ECDH (Elliptic Curve Diffie-Hellman) P-256/P-384

📢 **섹션 요약 비유**: SA는 두 사람이 사전에 정한 "암호 규칙 계약서"이고, SPD는 "어떤 편지에 어떤 봉투를 쓸지"의 규정집이다.

---

## 3. 구조 및 동작 원리

### IPsec vs TLS vs SSH 비교

| 구분 | IPsec | TLS | SSH |
|:---|:---|:---|:---|
| **계층** | Layer 3 (네트워크) | Layer 4-7 (전송-응용) | Layer 7 (응용) |
| **투명성** | 완전 투명 | 앱 수정 필요 | 앱 수정 필요 |
| **보호 대상** | 모든 IP 트래픽 | 특정 TCP 연결 | SSH 세션 |
| **키 관리** | IKE 자동 | TLS 핸드셰이크 | SSH 키 교환 |
| **VPN 용도** | 네이티브 지원 | TLS-VPN (OpenVPN 등) | SSH 터널링 |
| **NAT 환경** | AH 불가, ESP-NAT-T | 완전 지원 | 완전 지원 |
| **성능 오버헤드** | 낮음 (커널 레벨) | 중간 | 중간 |

### IPsec VPN 구성 유형

| 유형 | 구성 | 사용 사례 |
|:---|:---|:---|
| Site-to-Site | 두 게이트웨이 간 터널 | 본사-지사 연결 |
| Remote Access | 클라이언트-게이트웨이 | 재택근무 VPN |
| Host-to-Host | 두 호스트 직접 연결 | 서버 간 암호화 통신 |

📢 **섹션 요약 비유**: IPsec은 모든 도로에 자동으로 터널을 만드는 것이고, TLS는 특정 차량(앱)에만 방탄 코팅을 하는 것이다.

---

## 4. 비교 및 트레이드오프

**Linux strongSwan 기반 IPsec VPN 설정 예시**

```
# /etc/ipsec.conf
conn site-to-site
    authby=secret
    left=203.0.113.1         # 로컬 게이트웨이 IP
    leftsubnet=10.0.1.0/24  # 로컬 내부 네트워크
    right=203.0.113.2        # 원격 게이트웨이 IP
    rightsubnet=10.0.2.0/24 # 원격 내부 네트워크
    keyexchange=ikev2
    esp=aes256gcm16-sha256-ecp256  # ESP 암호 스위트
    ike=aes256-sha256-ecp256       # IKE 암호 스위트
    auto=start
```

**클라우드 환경 IPsec 적용**:
- AWS: Customer Gateway + Virtual Private Gateway → Site-to-Site VPN
- Azure: VPN Gateway IKEv2/IKEv1 지원
- GCP: Cloud VPN HA (High Availability) mode

**보안 강화 포인트**:
1. **PFS (Perfect Forward Secrecy)**: 세션마다 새 키 교환 (DH Group 14 이상)
2. **Dead Peer Detection (DPD)**: 연결 끊긴 SA 자동 삭제
3. **SA 수명 제한**: 3600초 또는 1GB 데이터 후 재협상
4. **안티리플레이 윈도우**: 64 패킷 이상 설정

📢 **섹션 요약 비유**: IPsec VPN은 두 도시 사이에 전용 지하 터널을 뚫는 것이다. 인터넷이라는 공공 도로를 쓰지만, 내용은 터널 안에서만 이동한다.

---

## 5. 실무 적용 및 최적화 기법

IPsec은 네트워크 인프라 수준의 보안을 제공하는 성숙한 표준으로, 기업 VPN의 70% 이상이 IPsec 기반이다. 특히 MPLS (Multiprotocol Label Switching) 대체 SD-WAN (Software-Defined WAN) 솔루션이 증가하면서 IPsec over 인터넷의 중요성이 더 커졌다.

Zero Trust 아키텍처로 전환하는 기업도 네트워크 세그멘테이션 레이어에서 IPsec을 유지하는 경우가 많다. 마이크로세그멘테이션과 IPsec을 결합하면 "이미 침입한 공격자"의 내부 이동을 차단하는 East-West 트래픽 보안이 가능하다.

📢 **섹션 요약 비유**: IPsec은 아파트 현관문(방화벽)과 개인 금고(암호화)의 중간 어딘가에 있다. 건물 복도를 걷는 것 자체가 안전해지는 효과다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| AH (Authentication Header) | 구성요소 | 인증·무결성, 암호화 없음, NAT 불가 |
| ESP (Encapsulating Security Payload) | 구성요소 | 인증+암호화, NAT 지원 |
| IKE (Internet Key Exchange) | 구성요소 | SA 자동 협상, UDP 500/4500 |
| SA (Security Association) | 핵심 개념 | 단방향 보안 파라미터 집합 |
| VPN (Virtual Private Network) | 응용 | IPsec Tunnel Mode 기반 |
| TLS (Transport Layer Security) | 비교 대상 | Layer 4-7, 앱 수정 필요 |

### 👶 어린이를 위한 3줄 비유 설명
IPsec은 모든 편지가 우체국을 나가기 전에 자동으로 봉인되는 것과 같아요.
편지 쓰는 사람(앱)은 봉인 방법을 몰라도 되고, 우체국(OS)이 알아서 해줘요.
두 우체국(게이트웨이)이 미리 "우리끼리만 아는 봉인 규칙"을 정해두는 거예요!
