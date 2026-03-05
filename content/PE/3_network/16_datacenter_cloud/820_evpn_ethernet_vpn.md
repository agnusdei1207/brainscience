+++
title = "820. EVPN (Ethernet VPN)"
date = "2026-03-05"
[extra]
categories = "studynotes-03_network"
+++

# 820. EVPN (Ethernet VPN)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: BGP(Border Gateway Protocol) 라우팅 프로토콜을 제어 평면(Control Plane)으로 사용하여, 데이터센터 내의 수많은 가상 머신과 컨테이너의 MAC 주소와 IP 주소를 동적으로 학습하고 전파하는 차세대 L2/L3 VPN 표준이다.
> 2. **가치**: 기존 L2 네트워크의 고질적인 문제인 브로드캐스트 스톰(Broadcast Storm)과 플러딩(Flooding)을 억제하고, 오버레이 터널링(주로 VXLAN)과 결합하여 완벽한 멀티 테넌트 환경과 액티브-액티브(Active-Active) 다중 경로 로드밸런싱을 제공한다.
> 3. **융합**: Spine-Leaf 토폴로지, VXLAN 터널링, BGP 라우팅 등 언더레이(Underlay)와 오버레이(Overlay) 아키텍처를 결합하는 현대 클라우드 데이터센터 네트워킹의 "두뇌" 역할을 수행한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
EVPN(Ethernet Virtual Private Network, RFC 7432)은 물리적 IP 네트워크 위에 가상의 이더넷(L2) 망과 라우팅(L3) 망을 동시에 구축할 수 있게 해주는 컨트롤 플레인 프로토콜이다. 패킷을 '어떻게 쌀 것인가(Data Plane)'는 VXLAN이나 MPLS가 담당하고, '어디로 보내야 하는가(Control Plane)'는 EVPN이 BGP를 통해 지시한다.

### 💡 비유
EVPN은 **"초거대 물류 네트워크의 AI 관제 시스템"**과 같다.
과거에는 물건(패킷)을 보낼 때 주소를 모르면 온 동네에 "철수네 집 아는 사람!" 하고 확성기로 소리쳐야 했다(ARP Flooding). 하지만 EVPN 관제 시스템(BGP)이 도입되면, 누군가 새로 이사 오자마자(VM 생성) 관제탑이 즉시 전국 모든 우체국(스위치)에 "철수네 집은 3번 구역에 있다"고 장부를 업데이트해 준다. 이제 우체부들은 소리칠 필요 없이 장부만 보고 조용하고 정확하게 물건을 배달할 수 있다.

### 등장 배경 및 발전 과정

#### 1. 기존 기술(VPLS, VXLAN Multicast)의 치명적 한계
- **VPLS의 한계**: 초기 이더넷 VPN 기술인 VPLS(Virtual Private LAN Service)는 여전히 전통적인 MAC 학습 방식(데이터 평면에서의 플러딩)을 사용했기 때문에 네트워크가 커지면 브로드캐스트 스톰으로 망이 마비되었다.
- **순수 VXLAN의 한계**: VXLAN도 MAC 주소를 찾기 위해 멀티캐스트(Multicast)를 사용했다(Flood-and-Learn). 이는 대규모 데이터센터에서 설정이 매우 복잡하고 트래픽 낭비가 극심했다.

#### 2. 패러다임 변화 (컨트롤 플레인의 도입)
스위치가 데이터를 주고받으면서 주소를 배우는 원시적인 방식(Data-plane Learning)을 버리고, 인터넷을 지탱하는 가장 강력한 라우팅 프로토콜인 **BGP의 확장(MP-BGP)**을 통해 MAC 주소와 IP 주소를 서로 통신하여 장부에 미리 적어두는 방식(Control-plane Learning)으로 진화하였다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/개념 | 비유 |
|--------|----------|-------------------|----------------|------|
| **MP-BGP** | 정보 전파 및 동기화 프로토콜 | EVPN용으로 확장된 BGP(AFI 25, SAFI 70)를 사용하여 MAC/IP 라우팅 정보 교환 | Control Plane | 전국 전화번호부 |
| **VTEP (VLAN Tunnel End Point)** | 터널 생성 및 패킷 캡슐화 | Leaf 스위치로 동작하며, EVPN 장부를 보고 VXLAN으로 데이터를 포장하여 전송 | Data Plane (VXLAN) | 물류 포장 및 발송소 |
| **EVPN Route Types** | 다양한 라우팅 메시지 종류 | MAC/IP 광고(Type 2), 브로드캐스트 제어(Type 3), 이더넷 세그먼트(Type 1/4) 등 5가지 핵심 메시지 사용 | BGP Update Msg | 전보의 종류 |
| **ARP Suppression** | 브로드캐스트 억제 | VTEP이 로컬 캐시를 보고 호스트의 ARP 요청(누구냐?)에 대리 응답(Proxy ARP) | BGP 기반 캐싱 | 비서의 대신 대답 |
| **Anycast Gateway** | 분산 라우팅 지원 | 모든 Leaf 스위치가 동일한 기본 게이트웨이 IP/MAC을 공유하여 최적 경로 라우팅 | L3 Routing | 전국 공통 콜센터 |

### 정교한 구조 다이어그램 (ASCII Art)

```ascii
================================================================================
[ EVPN - VXLAN Data Center Architecture ]
================================================================================

                           [ Spine Layer (BGP Route Reflector) ]
                          ┌─────────────────┐ ┌─────────────────┐
                          │   Spine SW 1    │ │   Spine SW 2    │
                          │(EVPN 장부 통합) │ │(EVPN 장부 통합) │
                          └─┬──────┬──────┬─┘ └─┬──────┬──────┬─┘
                            │      │      │     │      │      │
  ════ BGP Update (Type 2: MAC/IP) ═════════════════════════════════════════════
                            │      │      │     │      │      │
          ┌─────────────────▼┐   ┌─▼──────▼─┐   ┌▼──────▼─┐   ┌▼─────────────────┐
          │     Leaf SW 1    │   │Leaf SW 2 │   │Leaf SW 3│   │     Leaf SW 4    │
          │      (VTEP)      │   │ (VTEP)   │   │ (VTEP)  │   │      (VTEP)      │
          │ [BGP EVPN Table] │   │          │   │         │   │ [BGP EVPN Table] │
          │ VM1_MAC -> Leaf1 │   │          │   │         │   │ VM1_MAC -> Leaf1 │
          │ VM2_MAC -> Leaf4 │   │          │   │         │   │ VM2_MAC -> Leaf4 │
          └───────┬──────────┘   └──────────┘   └─────────┘   └──────────┬───────┘
                  │                                                      │
             ┌────▼────┐                                            ┌────▼────┐
             │   VM 1  │ (ARP Request: "VM 2 MAC이 뭐야?")          │   VM 2  │
             │ IP: 1.1 │ <------------------------------------------│ IP: 1.2 │
             │ MAC: M1 │   * Leaf 1이 BGP 장부를 보고 즉시 대답함   │ MAC: M2 │
             └─────────┘     (ARP 억제: 다른 곳에 플러딩 안 함)     └─────────┘
```

### 심층 동작 원리 (Step-by-Step)

#### ① BGP를 통한 MAC/IP 정보 학습 (Control Plane Learning)
1. **VM 생성**: Leaf 1 아래에 가상 머신(VM 1)이 부팅되어 네트워크에 연결된다.
2. **로컬 감지**: Leaf 1은 ARP나 DHCP 트래픽을 감시하여 VM 1의 MAC(M1)과 IP(1.1)를 로컬 테이블에 기록한다.
3. **BGP 전파**: Leaf 1은 Spine 스위치(Route Reflector)를 향해 **EVPN Type 2 라우트(MAC/IP Advertisement Route)** 메시지를 쏜다. "내 밑에 M1(1.1)이 있으니 나한테 보내라."
4. **전역 동기화**: Spine 스위치는 이 메시지를 다른 모든 Leaf 스위치(Leaf 2, 3, 4)에게 복사해 뿌려준다. 이제 모든 스위치는 VM 1의 위치를 알게 된다.

#### ② ARP 억제 (ARP Suppression / Proxy ARP)
VM 1이 VM 2(아직 통신해 본 적 없음)에게 데이터를 보내려 할 때, 먼저 ARP 요청(브로드캐스트)을 보낸다. 기존 방식이라면 이 요청이 데이터센터 전체 스위치로 복사되어(Flooding) 폭풍을 일으킨다.
하지만 EVPN 환경에서는 **Leaf 1이 이미 BGP를 통해 VM 2의 MAC을 알고 있으므로**, 트래픽을 네트워크로 흘려보내지 않고 자신이 직접 VM 1에게 대리 응답(Proxy ARP Reply)을 해버린다. 브로드캐스트가 완벽히 차단된다.

#### ③ Anycast Gateway (최적 라우팅)
만약 VM 1(서브넷 A)이 VM 3(서브넷 B)과 통신해야 한다면, 중간에 라우팅(L3)이 필요하다. EVPN은 모든 Leaf 스위치에 똑같은 게이트웨이 IP와 MAC을 설정(Anycast Gateway)한다. VM 1은 자기가 물려있는 Leaf 1에서 즉시 라우팅을 수행하고, VXLAN으로 포장하여 목적지 Leaf로 직행시킨다 (분산 라우팅, Distributed Routing). 특정 중앙 라우터에 트래픽이 몰리는 헤어핀(Hair-pinning) 병목이 사라진다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### EVPN vs 기존 아키텍처 비교

| 기능 및 지표 | 전통적 L2 (VLAN + STP) | 순수 VXLAN (Flood & Learn) | BGP EVPN + VXLAN |
|--------------|------------------------|---------------------------|------------------|
| **토폴로지** | 트리 구조 (Active-Standby) | Spine-Leaf (Active-Active) | Spine-Leaf (Active-Active) |
| **학습 방식**| 트래픽 기반 (Data Plane) | 트래픽 기반 (Data Plane, 멀티캐스트) | **BGP 라우팅 (Control Plane)** |
| **트래픽 제어**| 브로드캐스트 플러딩 막지 못함 | 멀티캐스트로 플러딩 (낭비 심함) | **ARP 억제로 플러딩 원천 차단** |
| **게이트웨이**| 중앙 집중형 (Core 스위치) | 중앙 집중형 | **분산형 (Anycast Gateway)** |
| **다중 경로**| STP 블로킹으로 절반 낭비 | ECMP로 100% 활용 | ECMP 100% 활용 |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**상황**: 금융 그룹의 차세대 데이터센터(SDDC) 구축. K8s 기반 마이크로서비스와 레거시 DB가 혼재되어 있으며, 망 분리 규정에 따라 수백 개의 테넌트(부서별 논리망)를 완벽히 격리해야 함. 또한 무중단 서비스를 위해 이중화된 스위치(Active-Active) 구성이 필수적임.
**전략적 설계**:
1. **EVPN-VXLAN 아키텍처 채택**: 물리 망(Underlay)은 OSPF나 eBGP로 라우팅만 되게 단순하게 구성하고, 그 위에서 **BGP EVPN**을 컨트롤 플레인으로, **VXLAN**을 데이터 플레인으로 사용하는 오버레이 망을 구축한다.
2. **이더넷 세그먼트 식별자(ESI) 활용**: 기존 MC-LAG(MLAG) 같은 벤더 종속적인 스위치 이중화 기술을 버리고, EVPN의 표준 기능인 ESI(Ethernet Segment Identifier, Type 1/4 라우트)를 활용하여 서버를 두 대의 Leaf 스위치에 Active-Active로 무손실 연결한다.
3. **VRF (Virtual Routing and Forwarding) 분리**: 부서별로 VRF를 분리하여 테넌트 간 트래픽 섞임을 하드웨어 레벨에서 원천 차단(Micro-segmentation 효과)한다.

### 주의사항 및 안티패턴 (Anti-patterns)
- **과도한 BGP 세션 폭발**: Leaf 스위치가 너무 많아지면 서로 BGP 세션을 맺는 것(Full Mesh) 자체가 엄청난 부하를 유발한다. 반드시 Spine 스위치를 **Route Reflector(RR)**로 설정하여 BGP 업데이트를 중앙에서 중계하도록 토폴로지를 설계해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 정량적 기대효과
- **트래픽 절감**: BUM(Broadcast, Unknown Unicast, Multicast) 트래픽의 플러딩을 95% 이상 억제하여 코어 스위치의 대역폭 낭비 방지.
- **성능 향상**: 분산 Anycast 게이트웨이를 통한 최단 경로 라우팅으로 East-West(서버 간) 지연 시간 극소화.

### 미래 전망 및 진화 방향
EVPN은 데이터센터 내부(Intra-DC)를 넘어, 전 세계에 흩어진 데이터센터 간의 연동(DCI, Data Center Interconnect)을 위한 핵심 프로토콜로 진화했다. 더 나아가 최신 클라우드 네이티브 환경에서는 CNI(Container Network Interface) 플러그인인 Calico, Cilium 등이 BGP EVPN 스피커를 내장하여, 물리 스위치뿐만 아니라 파드(Pod) 레벨까지 EVPN 아키텍처가 침투하는 **엔드투엔드(End-to-End) EVPN** 생태계로 확장되고 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [VXLAN](./817_vxlan.md) - EVPN이 주소를 찾은 후 실제로 데이터를 포장하는 역할 (Data Plane)
- [BGP (Border Gateway Protocol)](../6_network_ip/423_bgp.md) - EVPN의 기반이 되는 인터넷 표준 라우팅 프로토콜
- [SDN (소프트웨어 정의 네트워킹)](../17_sdn_nfv/850_sdn_concept.md) - 제어/데이터 평면을 분리한다는 EVPN의 핵심 사상
- [스파인-리프 아키텍처](./802_spine_leaf_architecture.md) - EVPN이 동작하는 최적의 물리적 토폴로지

---

## 👶 어린이를 위한 3줄 비유 설명
1. **EVPN이 뭔가요?**: 동네 우체국장님들(스위치)이 모여서 매일매일 "누가 어디로 이사 갔는지"를 완벽하게 정리해 놓은 마법의 주소록(BGP)이에요.
2. **왜 필요해요?**: 옛날엔 편지를 보낼 때 주소를 모르면 온 동네 사람들에게 "혹시 철수 알아요?" 하고 시끄럽게 소리쳐야 해서 동네가 너무 시끄러웠거든요.
3. **무엇이 좋아지나요?**: 이제는 주소록만 딱 펼쳐보면 철수가 어딨는지 1초 만에 알 수 있으니까, 시끄러운 소음 없이 편지를 가장 빠른 지름길로 슝~ 하고 보낼 수 있어요!
