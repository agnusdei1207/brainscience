+++
weight = 704
title = "MPLS (Multiprotocol Label Switching)"
description = "레이블 기반的高速 패킷 전달 기술 MPLS의 동작 원리와 Traffic Engineering을 다룬다."
date = 2024-01-24

[extra]
categories = ["studynote-software-engineering"]
topics = ["mpls", "label-switching", "traffic-engineering"]
study_section = ["section-7-routing-tunneling-qos"]

number = "704"
core_insight = "MPLS는 IP 헤더 분석 없이 레이블(Label)만으로高速路由决定하여,话音やビデオなどのリアルタイムトラフィックに低遅延转发を提供する。TE(Traffic Engineering) 기능을 통해 네트워크 관리자는 명시적으로トラフィック路径を制御できる。"
key_points = ["레이블 스위칭 (IP 대신)", "LIB (Label Information Base)", "LDP (Label Distribution Protocol)", "MPLS TE (Traffic Engineering)"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MPLS는 IP 헤더 대신 짧은 레이블(Label)을 기반으로 경로를 결정하여,高速なパケット転送を実現する 네트워크 기술이다.
> 2. **가치**: 실시간 트래픽(VoIP, Video)에 낮은 지연을 제공하며, 네트워크 관리자가 명시적으로トラフィック 경로를 제어할 수 있는 Traffic Engineering 기능을 제공한다.
> 3. **융합**: MPLS는 VPN, VPLS, EVPN 등 다양한 서비스의 기반 기술이며, SD-WAN의 Underlay 네트워크로 활용되기도 한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

**개념**: MPLS (Multiprotocol Label Switching)는送信자가 데이터 그램의 IP 헤더를 분석하는 대신,事前に割り当てられた短いえ조금(Label)만 보고高速に转发する 기술이다. 레이블은 32비트 길이로, 20비트 레이블 값, 3비트 EXP(Experimental, QoS 용), 1비트 Bottom of Stack, 8비트 TTL로 구성된다. MPLS 도메인 내의 첫 번째 라우터(Edge LSR)는 IP 헤더를 분석하여 레이블을 할당하고, 도메인 내부의 LSR(Label Switching Router)은 IP 분석 없이 레이블만 보고 스위칭한다.

**필요성**: 전통적인 IP 라우팅에서는 모든 라우터가 목적지 IP 주소를 기반으로 최단 경로를 계산한다. 그러나 이러한 과정이 복잡하고 지연이 발생하며, 특정トラフィック를 원하는 경로로 강제하기 어렵다. MPLS는 레이블 스위칭을 통해 경로 계산 부담을 줄이고, 명시적 경로 설정(TE)을 가능하게 하여, 대역폭이 제한적인 핵심 네트워크에서 효율적인 트래픽 관리가 가능해졌다.

**비유**: MPLS는 **고속도로 톨게이트 시스템**과 같다.目的地別に最短 경로를 찾는 것은IP 라우팅) cars must individually find their way, causing delays at each intersection. With MPLS, a quick ticket (label) is issued at the toll gate entrance, and subsequent tolls just read the ticket to direct cars along the pre-determined route without requiring each driver to make routing decisions.

**등장 배경**: MPLS는 1990년대 후반 Cisco의 Tag Switching과 IETF의 표준화를 결합하여 2001년 RFC 3031로 표준화되었다. 원래 BGP와 IP의 속도를 높이기 위한 기술이었으나, 현재는 VPN 서비스, Traffic Engineering, QoS 보장 등 다양한用途で活用されている。

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### MPLS 레이블 구조와 동작

MPLS 도메인은 Edge LSR(LABEL Switching Router)과 Core LSR로 구성된다. Ingress LSR은 IP 패킷을 수신하고, FEC(Forwarding Equivalence Class)에 따라 레이블을 할당한다. Core LSR은 수신된 레이블을 기반으로 스위칭만 수행하며, Egress LSR은 레이블을剥离하고 IPとして転送する。

```
┌───────────────────────────────────────────────────────────────────────┐
│                    MPLS 레이블 구조 및 동작 과정                          │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  MPLS 레이블 (32비트):                                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │   Label (20비트)    │  EXP (3비트) │ BoS │   TTL (8비트)   │   │
│  │   값: 16~1,048,575  │  QoS/CoS    │ 1비트│   홉 카운트     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  • Label: 레이블 값 (16은 예약, 0~15는 특수 용도)                      │
│  • EXP: QoS/CoS(Class of Service) 정보를 전달                        │
│  • BoS (Bottom of Stack): 스택의 마지막 레이블 여부                     │
│  • TTL: 레이블 스위칭 구간의 홉 수                                        │
│                                                                       │
│  동작 과정:                                                            │
│                                                                       │
│  [호스트 A] ──▶ [Ingress LSR] ──▶ [Core LSR1] ──▶ [Core LSR2] ──▶ [Egress LSR] ──▶ [호스트 B] │
│  192.168.1.10      R1               R2           R3            R4    10.0.0.20     │
│                    Edge             Core         Core           Edge  │
│                                                                       │
│  ① Ingress (R1): IP 헤더 분석 → FEC 결정 → 레이블 할당 (예: Label 100)    │
│     IP: Src=192.168.1.10, Dst=10.0.0.20  ──▶  Label=100 추가        │
│                                                                       │
│  ② Core LSR1 (R2): 수신 레이블(100) → LIB 조회 → 출력 레이블(200)으로 교체 │
│     수신: Label=100  ──▶  출력: Label=200                              │
│     ※ IP 헤더 분석 없음 (순수 레이블 스위칭)                            │
│                                                                       │
│  ③ Core LSR2 (R3): 수신 레이블(200) → LIB 조회 → 출력 레이블(300)으로 교체 │
│     수신: Label=200  ──▶  출력: Label=300                              │
│                                                                       │
│  ④ Egress (R4): 수신 레이블(300) → 레이블 제거 → IPとして転送           │
│     Label=300 제거 ──▶ IP: Dst=10.0.0.20 ──▶ 호스트 B 전달           │
│                                                                       │
│  MPLS 스택 (여러 레이블):                                               │
│  ┌──────────┬──────────┬──────────┬───────────────────────┐           │
│  │ Label 3  │ Label 2  │ Label 1  │ IP Header + Payload   │           │
│  │ (outer)  │          │ (inner)  │                       │           │
│  └──────────┴──────────┴──────────┴───────────────────────┘           │
│   ◀────────── Pop (제거) ──────────                                    │
│   ◀─────────────────────── Swap ────────────────────────              │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** MPLS의 핵심 이점은 Core LSR에서 IP 헤더 분석이 필요 없다는 것이다. 모든 Core LSR이 단순히 수신 레이블을 LUT(Lookup Table)에서查找하여 출력 레이블로 교체한다. これにより、IP 주소/class 에 따라 라우팅 테이블 전체를 탐색하는 시간을 절약하고, 레이블 스위칭만으로高速转发可以实现する。 특히 경로 상에 여러 LSR이 있더라도, 각 LSR은 자신의 LUT만 보면 되므로 O(1) 복잡도의 고정 시간 처리가 가능하다. 그러나 실제로는 CE-ROUTER 간 IP 라우팅+OAM(Operations, Administration, Management) 비용이 있어, 단순 IP 대비 비용 효율성이 항상 우세한 것은 아니다.

### LDP (Label Distribution Protocol)와 RSVP-TE

MPLS에서 레이블을 할당하고 분배하는 프로토콜로 LDP(Label Distribution Protocol)와 RSVP-TE(Resource Reservation Protocol Traffic Engineering)이 있다. LDP은 IGP(OSPF, IS-IS)와 연동하여 최단 경로 기반의 레이블을 분배한다. RSVP-TE은 Traffic Engineering 확장으로서, 명시적 경로 설정과 대역폭 예약 기능을 제공한다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    LDP vs RSVP-TE                                       │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【LDP (Label Distribution Protocol)】                                  │
│                                                                       │
│  동작:                                                                │
│  • IGP (OSPF, IS-IS)가 라우팅 테이블 결정                              │
│  • LDP가 라우팅 테이블에 따라 레이블 매핑 분배                          │
│  • 기본 경로 (IGP 최단 경로)만 지원                                    │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  R1 ─── OSPF ─── R2 ─── OSPF ─── R3                         │   │
│  │  │                                                         │   │
│  │  └──────── LDP (Label Mapping) ──────────────────────────┘  │   │
│  │                                                             │   │
│  │  LDP가 R1→R2: Label 100 할당, R2→R3: Label 200 할당         │   │
│  └───────────────────────────────────────────────────────────────┘   │
│  → IGP 최단 경로 외의 경로 설정 불가                                   │
│                                                                       │
│  【RSVP-TE (Resource Reservation Protocol - Traffic Engineering)】    │
│                                                                       │
│  동작:                                                                │
│  • 명시적 경로 설정 (strict/loose explicit path)                       │
│  • 대역폭 예약 ( bandwidth reservation)                               │
│  • Fast Reroute (FRR) 지원                                            │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  R1 ──── R2 ──── R3 ──── R4                                  │   │
│  │    │                                                 │        │   │
│  │    └──────── RSVP-TE (명시적 경로 + 대역폭 예약) ─────────┘        │   │
│  │                                                             │   │
│  │  Admin: R1→R2→R4 경로로 100Mbps 예약                         │   │
│  │  → IGP 최단 경로(R1→R2→R3→R4)와 다르더라도 설정 가능           │   │
│  └───────────────────────────────────────────────────────────────┘   │
│  → Traffic Engineering에 필수                                         │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  RSVP-TE 주요 객체:                                            │   │
│  │  • SESSION: 목적지 세션 식별                                    │   │
│  │  • SENDER_TEMPLATE: 송신자 정보                                │   │
│  │  • LABEL_REQUEST: 레이블 요청                                 │   │
│  │  • LABEL: 레이블 할당                                          │   │
│  │  • RECORD_ROUTE: 실제 사용 경로 기록                           │   │
│  │  • BANDWIDTH: 대역폭 예약량                                    │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** LDP는 IGP 최단 경로에 기반하므로 별도의 경로 제어 없이 자동으로 레이블을 분배한다. 그러나 IGP 최단 경로 외의 경로를 설정할 수 없으므로, 트래픽 부하 분산이나 특정 경로 선호가 불가능하다. 반면 RSVP-TE는 관리자가 명시적으로 경로를 설정하고 대역폭을 예약할 수 있다. 예를 들어, 핵심 업무 트래픽은 low-latency 경로로, 백업 트래픽은 alternate 경로로 유도할 수 있다. 이러한 RSVP-TE의 TE 기능은 대규모 서비스 프로바이더 네트워크에서 필수적이다.

### MPLS VPN (L3VPN, L2VPN)

MPLS의 주요 应用으로 MPLS VPN이 있다. L3VPN(也说 BGP MPLS VPN)은 VRF(Virtual Routing and Forwarding)를 기반으로 각 고객에게 격리된 라우팅 도메인을 제공한다. L2VPN은 고객의 레이어 2(イーサネット) 트래픽을 MPLS 백본上で переда하여, 고객이 자신의 라우팅을 완전히 관리할 수 있게 한다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    MPLS L3VPN (BGP MPLS VPN) 구조                       │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【VRF (Virtual Routing and Forwarding)】                              │
│  • 각 고객에게 격리된 라우팅 테이블 제공                                │
│  • RD (Route Distinguisher): VPN 경로 구분 (64비트 접두사)            │
│  • RT (Route Target): VPN 경로Import/Export 정책                      │
│                                                                       │
│         Customer A (VRF-A)          Customer B (VRF-B)               │
│              │                           │                             │
│         [CE1]─┴─ [PE1:VRF-A]───┐   [CE3]─┴─ [PE1:VRF-B]            │
│                                │                                   │
│                          [MPLS Backbone]                              │
│                                │                                   │
│         [CE2]─┬─ [PE2:VRF-A]───┘   [CE4]─┬─ [PE2:VRF-B]            │
│              │                           │                             │
│              │                           │                             │
│         Customer A                 Customer B                        │
│         (격리된 라우팅)               (격리된 라우팅)                  │
│                                                                       │
│  동작:                                                                │
│  ① CE1이 IP 루트 PE1에 광고                                           │
│  ② PE1: VRF-A 테이블에 저장 + RD 추가 → VPNv4 경로                     │
│  ③ PE1: iBGP로 다른 PE (PE2)에게 VPNv4 광고 (RD 포함)                 │
│  ④ PE2: RT 정책으로 VRF-A로 Import 여부 결정                          │
│  ⑤ PE2: CE2에게 VRF-A 관련 경로만 광고                                │
│  ⑥ CE2는 Customer A 경로만 인식 (Customer B와是完全隔离)               │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  MPLS L3VPN의 장점:                                             │   │
│  │  • 고객마다 격리된 라우팅 테이블 (보안)                          │   │
│  │  • 서비스 프로바이더는 IP 주소 체계 모름 (고객 자율성)            │   │
│  │  • 단일 백본으로 수천 개의 VPN 서비스 제공 가능 (확장성)         │   │
│  │  • CE는 MPLS，不需要额外的 프로토콜                               │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** MPLS L3VPN의 핵심은 VRF와 RD/RT 메커니즘이다. RD(Route Distinguisher)는 64비트 접두사로, 서로 다른 VPN에서 동일한 IP 주소 체계(예: 10.0.0.0/8)를 사용하더라도 고유하게 구분할 수 있게 한다. RT(Route Target)은 BGP 확장 커뮤니티属性으로, 어떤 VPN 경로를 import/export할지 정책적으로 제어한다. 이를 통해 서비스 프로바이더는 단일 MPLS 백본에서 수천 개의 고객 VPN을 격리하여 제공할 수 있으며, 각 고객은 자신만의 IP 주소 체계를完全に自律的に管理할 수 있다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### MPLS vs IP Routing

| 비교 항목 | Traditional IP Routing | MPLS |
|:---|:---|:---|
| **转发 방법** | 각 라우터에서 IP 헤더 분석 + 라우팅 테이블 조회 | 레이블만 교체 (IP 분석 불필요) |
| **경로 제어** | IGP에 의존 | LDP/RSVP-TE로 명시적 제어 가능 |
| **확장성** | 대규모 네트워크에 적합 | 더 높은 확장성 (运营商에서 주로使用) |
| **QoS** | DiffServ 기반 | EXP 필드로 세밀한 QoS 가능 |
| **트래픽 엔지니어링** | 제한적 | RSVP-TE로 상세한 TE 가능 |
| **비용** | 낮음 | 높음 (专用 장비/라이선스) |
| **주요 용도** | 일반 기업 네트워크 | 서비스 프로바이더, 대기업 본사-지사 |

### MPLS L2VPN vs L3VPN

| 비교 항목 | L2VPN (VPLS, EVPN) | L3VPN (BGP MPLS VPN) |
|:---|:---|:---|
| **격리 수준** | 레이어 2 (イーサ넷) | 레이어 3 (IP) |
| **고객 라우팅** | 고객이 完全自律적 관리 | 고객 또는 SP가 관리 가능 |
| **확장성** | 중간 | 매우 높음 |
| **STP 필요성** | VPLS는 STP 필요, EVPN은 불필요 | 불필요 |
| **주요 용도** | 데이터센터互联, 고객 LAN 확장 | 기업 site-to-site VPN |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 1 — 글로벌 기업의 MPLS VPN**: 본사(서울), 지사(东京, 纽约)로 구성된글로벌 기업. 각 사이트를 MPLS L3VPN으로 연결. 본사 VRF에는 全 LLC의 경로가 있고,各地点 VRF에는 해당 지역의 경로만 있다.voice/비디오 트래픽은 별도의 VPN 또는 CoS优先级으로 처리. 각 site의 CE는简单地 MPLS 연결만 하면 되고, IP 주소 체계는 masing-masing 관리.

**시나리오 2 — MPLS TE를 통한 트래픽 부하 분산**: 서비스 프로바이더 백본에서, 주요 코어 라우터 간链接에 트래픽이集中되지 않도록 RSVP-TE로 대체 경로를 설정. Primary 경로( R1→R2→R5)와 Secondary 경로( R1→R3→R4→R5)를 명시적으로 설정하고, 각각 70%, 30%의 트래픽을 할당. 이를 통해 특정 링크의 과부하를 방지하고, 네트워크利用率的을 均一하게 유지.

**시나리오 3 — 데이터센터 간 L2VPN (EVPN)**: 두 데이터센터 간 레이어 2 연결이 필요한 경우, EVPN(Ethernet VPN)을 사용.同一 IP 주소 체계가 양쪽 데이터센터에存在하고, VMotion 등이 가능하다. VPLS와 달리 EVPN은 경로가 MAC 학습으로 최적화되어, 불필요한 트래픽 flood를 줄인다.

### 도입 체크리스트

- **기술적**: MPLS 도메인의 모든 장비가 MPLS를 지원하는가? LDP/RSVP-TE 선택이 적절한가? MPLS TTL 처리 방식이 올바른가?
- **운영·보안적**: CE-PE 연결에서 라우팅 정책이 올바르게 설정되었는가? VRF 간 격리가 필요한 경우 RT 정책이 적절한가?

### 안티패턴

- **불필요한 MPLS 도입**: 소규모 네트워크( sites 3개 미만)에서는 MPLS의 복잡성과 비용이 이점을上回ることがある. 간단한 site-to-site VPN이 더 적합할 수 있다.
- **LDP/RSVP 혼합**: 동일한 MPLS 도메인에서 LDP와 RSVP-TE를混用하면 경로 불일치가 발생할 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | Traditional IP | MPLS 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 각 홉마다 IP 분석 | 레이블 스위칭만 | 홉당 지연 **30~50% 감소** |
| **정량** | 경로 제어 불가 | RSVP-TE로 명시적 경로 설정 | 트래픽 부하 분산 **균형화** |
| **정성** | VPN 서비스 불가 | L2/L3 VPN 서비스 | 새 수익원 창출 가능 |

### 미래 전망

MPLS는 현재 네트워크의 핵심 기반이지만, SDN/SD-WAN의 발전과 함께 그 역할이 변화하고 있다. SD-WAN은 MPLS 대신 인터넷 연결을 활용하여もっと安価に、そして柔軟な WAN을 제공하려고 한다. 그러나话音やその他のリアルタイム 트래픽에는 여전히 MPLS의 보장된 QoS가 필요하다. 향후에는 Hybrid WAN(SD-WAN + MPLS) 구성이 표준이 될 것으로 예상되며, MPLS는 핵심 업무 트래픽의 보장된 전송로로서 가치를 유지할 것이다.

### 참고 표준

- RFC 3031 — Multiprotocol Label Switching Architecture
- RFC 3036 — LDP Specification
- RFC 3209 — RSVP-TE: Extensions to RSVP for LSP Tunnels
- RFC 4364 — BGP/MPLS IP Virtual Private Networks (L3VPN)
- RFC 7207 — Framework for EVPN

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Label Switching** | IP 헤더 대신 레이블을 기반으로高速转发する技术であり、MPLSの核心である。 |
| **LDP** | 레이블을 분배하는 기본 프로토콜로, IGP 최단 경로에 기반한다. |
| **RSVP-TE** | MPLS TE를 위한 확장된 RSVP로, 명시적 경로 설정과 대역폭 예약을 제공한다. |
| **MPLS VPN** | MPLS 백본 기반으로 고객에게 격리된 L2 또는 L3 VPN을 제공한다. |
| **VRF** | MPLS VPN에서 각 고객에게 격리된 라우팅 테이블을 제공하는 기술이다. |
| **SD-WAN** | 소프트웨어 정의 WAN으로, MPLS를 대체하거나 hybrid로 활용하여より灵活な WAN을 만든다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. MPLS는 고속도로의 **ETC 카드 시스템**과 같아요.目的地ごとに道案内( 라우팅)を受ける 대신, 入园장에서短い조금(레이블)을 받고,後の料金所ではその조금만見て.direction。所以在高速公路上没有停止或方向 decision delays, allowing vehicles to pass quickly.
2. MPLS의 레이블은 **行李标签**과 같아요. 각 짐箱(패킷)에 도착지 기내식(레이블)이 붙어 있어서,滑走路上の转运担当者は 개봉하여内容를 확인할 필요 없이、标签만 보고次の目的地에 보내면 돼요.
3. 하지만！这个 고속도로를 놓으려면 특별한 기계( MPLS 장비)가 필요해서 비용이 많이 들어, 그래서 전 세상에 다 설치되어 있지는 않아요. 주로큰 기업들( 기업)과通信사(运营商)가 서로 연결할 때 주로 써요!
