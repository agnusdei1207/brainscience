+++
weight = 277
title = "277. IPsec 모드 — Transport/Tunnel"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Transport Mode는 원본 IP 헤더를 유지한 채 페이로드만 보호하고, Tunnel Mode는 원본 IP 패킷 전체를 새 IP 패킷으로 캡슐화해 내부 IP 주소 정보까지 은폐한다.
> 2. **가치**: Site-to-Site VPN (Virtual Private Network)에는 Tunnel Mode가 필수이고, Host-to-Host 직접 암호화에는 Transport Mode가 효율적이며, 두 모드는 오버헤드와 보호 범위의 트레이드오프로 선택한다.
> 3. **판단 포인트**: Tunnel Mode가 원본 IP 헤더를 은폐하는 것이 단순한 추가 기능이 아니라, 내부망 토폴로지 노출을 방지하는 보안 요소임을 강조해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

IPsec이 IP 패킷을 어느 수준까지 보호할 것인가를 결정하는 것이 바로 **운용 모드(Operation Mode)**다. Transport Mode와 Tunnel Mode는 AH/ESP 프로토콜 모두에 적용 가능한 독립적인 개념이다.

Transport Mode는 **두 호스트가 직접 통신할 때** 사용한다. 원본 IP 헤더가 노출되므로 라우팅은 기존 인프라를 그대로 활용한다. 오버헤드가 적고 E2E (End-to-End) 보안을 제공하지만, 내부 IP 주소가 노출된다는 단점이 있다.

Tunnel Mode는 **게이트웨이 간 또는 게이트웨이-호스트 간 통신**에 사용한다. 원본 IP 패킷 전체를 페이로드로 취급하고 새 IP 헤더를 추가한다. 이를 통해 원본 송·수신자 IP 주소(내부망 주소)를 완전히 은폐하며, 기업 VPN의 표준 구성이다.

두 모드의 핵심 차이는 "새 IP 헤더 추가 여부"와 "원본 IP 헤더의 보호 여부"다. Tunnel Mode는 원본 IP 헤더 자체가 페이로드가 되므로 암호화(ESP 사용 시) 또는 인증(AH/ESP 모두) 대상이 된다.

📢 **섹션 요약 비유**: Transport Mode는 편지에 직접 자물쇠를 채우는 것이고, Tunnel Mode는 편지를 봉투에 넣고 그 봉투에 자물쇠를 채우는 것이다. 봉투를 보는 사람은 원래 편지의 주소조차 알 수 없다.

---

## 2. 구성요소

### Transport Mode vs Tunnel Mode 패킷 구조 (ESP 기준)

```
[원본 IPv4 패킷]
┌────────────┬─────────────────────────────────────────────┐
│ IP Header  │  TCP/UDP Payload                            │
│ (src: A   │                                             │
│  dst: B)  │                                             │
└────────────┴─────────────────────────────────────────────┘

[Transport Mode - ESP 적용]
┌────────────┬──────────┬──────────────────────────┬───────┐
│ IP Header  │ ESP 헤더 │  암호화된 TCP/UDP Payload │ESP 트 │
│(수정됨:   │ (SPI+Seq)│                           │레일러 │
│ proto=50) │          │ ← 암호화 범위 →           │+ ICV  │
└────────────┴──────────┴──────────────────────────┴───────┘
원본 IP 헤더는 노출 (라우터 참조 가능)

[Tunnel Mode - ESP 적용]
┌──────────────┬──────────┬──────────────────────────────────────────┬───────┐
│ 새 IP Header │ ESP 헤더 │  암호화된 [원본 IP Header + Payload]     │ESP 트 │
│ (src: GW1   │(SPI+Seq) │                                          │레일러 │
│  dst: GW2)  │          │ ← 암호화 범위 (내부 IP 주소 은폐!) →    │+ ICV  │
└──────────────┴──────────┴──────────────────────────────────────────┴───────┘
새 IP 헤더만 노출 (게이트웨이 IP), 내부 src/dst 은폐
```

### 모드별 특성 비교

| 특성 | Transport Mode | Tunnel Mode |
|:---|:---|:---|
| **IP 헤더** | 원본 유지 (부분 수정) | 새 헤더 추가, 원본 은폐 |
| **내부 IP 노출** | ⚠️ 노출됨 | ✅ 은폐됨 |
| **오버헤드** | 낮음 (20바이트 추가) | 높음 (40+바이트 추가) |
| **구성 복잡도** | 낮음 | 중간 |
| **적용 주체** | 두 호스트 직접 | 게이트웨이 포함 가능 |
| **토폴로지 노출** | 내부 IP 구조 노출 | 완전 은폐 |
| **주요 사용 사례** | 호스트 간 직접 암호화 | VPN, 게이트웨이 연결 |

📢 **섹션 요약 비유**: Transport Mode는 투명 봉투에 내용물만 잠그는 것이고, Tunnel Mode는 불투명 봉투에 원래 봉투채 넣어 배송 정보까지 숨기는 것이다.

---

## 3. 구조 및 동작 원리

### Site-to-Site VPN vs Host-to-Host 시나리오

```
[Site-to-Site VPN (Tunnel Mode)]

본사 내부망          GW1          인터넷          GW2          지사 내부망
10.0.1.0/24 ────────[암호화]────────────────────[복호화]──────── 10.0.2.0/24
                                   ↑
                        새 IP: GW1→GW2
                        내부 10.0.1.x → 10.0.2.x 은폐
                        직원은 VPN 클라이언트 설치 불필요

[Remote Access VPN (Tunnel Mode)]

재택 PC              인터넷           VPN GW          기업 내부망
(클라이언트)──────────────────────────[복호화]──────── 10.0.1.0/24
VPN 클라이언트 설치                가상 IP 할당
                                    (예: 10.10.0.1)

[Host-to-Host (Transport Mode)]

서버 A ──────────[직접 ESP/AH]────────── 서버 B
10.0.1.1                                 10.0.2.1
IPsec 정책 직접 설정, 낮은 오버헤드
마이크로세그멘테이션에 활용
```

### AH/ESP × Transport/Tunnel 조합 매트릭스

| 조합 | 인증 | 암호화 | NAT | 실무 사용 |
|:---|:---|:---|:---|:---|
| AH + Transport | 페이로드+일부 IP | ❌ | ❌ | 드물음 |
| AH + Tunnel | 전체(새 IP 포함) | ❌ | ❌ | 거의 없음 |
| ESP + Transport | 페이로드 | ✅ | ✅ | E2E 암호화 |
| ESP + Tunnel | 원본 패킷 전체 | ✅ | ✅ | **VPN 표준** |
| AH+ESP + Transport | 전체 | ✅ | ❌ | 드물음 |
| AH+ESP + Tunnel | 전체 | ✅ | ❌ | 드물음 |

📢 **섹션 요약 비유**: Tunnel Mode + ESP는 "내부 봉투+내용물을 잠그고, 겉 봉투만 배달부에게 보이는" 이중 보안이다. VPN이 바로 이 원리다.

---

## 4. 비교 및 트레이드오프

**IPsec Tunnel Mode 활용: 클라우드-온프레미스 연결**

```
온프레미스 데이터센터              AWS VPC (Virtual Private Cloud)
Router/FW                          Virtual Private Gateway
(IP: 203.0.113.1) ─── IPsec ───── (IP: 52.x.x.x)
                     Tunnel Mode
                     ESP + AES-256-GCM
                     IKEv2 + ECDH P-256
                     PFS (Perfect Forward Secrecy) 활성화

내부 트래픽: 10.0.0.0/8 ←→ 172.16.0.0/12
외부에는 203.0.113.1 ↔ 52.x.x.x만 노출
```

**Transport Mode 활용: 서버 간 마이크로세그멘테이션**

```
앱 서버 (10.0.1.10) ──[ESP Transport]── DB 서버 (10.0.1.20)
IPsec 정책:
  src=10.0.1.10, dst=10.0.1.20, proto=tcp, port=5432
  → ESP Transport Mode, AES-128-GCM
  → 같은 서브넷이지만 도청 불가
```

이 패턴은 Zero Trust 아키텍처에서 내부망 East-West 트래픽을 암호화하는 표준 방법이다.

**기술사 답안 포인트**: Tunnel Mode가 "토폴로지 은폐"라는 추가 보안 가치를 제공한다는 점을 Transport Mode와의 단순 오버헤드 비교를 넘어 설명해야 한다. 특히 공격자가 패킷 분석으로 내부 IP 주소 구조를 파악하는 네트워크 정찰(Reconnaissance) 공격을 Tunnel Mode가 방어함을 언급한다.

📢 **섹션 요약 비유**: 군사 작전에서 병력 이동 경로를 숨기려면 병사에게 방탄복을 입히는 것(Transport)으로는 부족하다. 전체 부대를 철수된 트럭으로 이송(Tunnel)해야 이동 자체가 노출되지 않는다.

---

## 5. 실무 적용 및 최적화 기법

Transport Mode와 Tunnel Mode는 적용 시나리오에 따라 선택해야 하는 보완적 도구다. 기업 VPN의 95% 이상은 Tunnel Mode + ESP를 사용하며, 이는 NAT 호환성, 내부 토폴로지 은폐, 게이트웨이 집중 관리의 세 가지 장점을 동시에 충족하기 때문이다.

마이크로세그멘테이션과 Zero Trust의 확산으로 Transport Mode의 사용이 점차 증가하는 추세다. 서버 간 통신에 개별 IPsec 정책을 적용하는 방식은 Linux Kernel의 XFRM 서브시스템, Windows IPsec Policy 등으로 자동화가 가능해졌다.

📢 **섹션 요약 비유**: Tunnel Mode는 지하 고속도로, Transport Mode는 차량에 방탄 유리를 달기. 목적지와 경로를 숨기려면 전자가, 차량만 보호하려면 후자가 적합하다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| AH / ESP | 하위 프로토콜 | 두 모드 모두에서 사용 가능 |
| IKE (Internet Key Exchange) | 키 관리 | 모드와 독립적으로 SA 협상 |
| Site-to-Site VPN | 주요 적용 | Tunnel Mode의 대표 사례 |
| 마이크로세그멘테이션 | 적용 확장 | Transport Mode로 E2E 암호화 |
| Zero Trust | 아키텍처 | Transport Mode 확산 배경 |
| NAT-T (NAT Traversal) | 환경 요건 | Tunnel Mode + ESP에 필요 |

### 👶 어린이를 위한 3줄 비유 설명
Transport Mode는 편지 내용만 봉투에 넣고 주소는 밖에 쓰는 것이에요.
Tunnel Mode는 편지 봉투 전체를 또 다른 봉투에 넣어서 원래 주소까지 숨기는 거예요.
VPN은 Tunnel Mode를 써서 인터넷에서 우리 회사 주소(IP)가 보이지 않게 해요!
