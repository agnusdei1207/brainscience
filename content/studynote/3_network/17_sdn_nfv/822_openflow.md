+++
weight = 822
title = "OpenFlow"
+++

# OpenFlow

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OpenFlow는 SDN (Software-Defined Networking)에서 SDN Controller와 네트워크 장비(스위치, 라우터) 간의 통신을 위한 표준화된southbound 인터페이스 프로토콜로, Controller가 스위치의 Flow table을programmatically 제어하여 패킷 전달 경로를 동적으로 변경한다.
> 2. **가치**: OpenFlow의 표준화使得不同厂商의 네트워크 장비와 SDN Controller가 상호운용될 수 있게 되어, 네트워크 벤더 종속을 줄이고, 네트워크 자동화와 혁신을加速시킨다.
> 3. **융합**: OpenFlow 1.0에서 1.5까지 발전하며, VXLAN 지원, MPLS 태그 처리, 테이블 재진입 (table-miss)等的功能을追加하고, ONF (Open Networking Foundation)에서 표준화를 주도하며, ODL (OpenDaylight), ONOS, Ryu 등의 Controller에서广泛하게 지원된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

OpenFlow는 SDN 아키텍처에서 Controller(제어 평면)와 네트워크 장비(데이터 평면) 사이의 통신을 담당하는 southbound 인터페이스 프로토콜이다. 2008년 스탠포드 대학에서 처음 제안되었고, ONF (Open Networking Foundation)에서 표준화를 주도했다. OpenFlow의 핵심은 스위치 내부에 Flow table을두고, 이 table에 대한 모든 제어를 Controller에서 이루어지게 하는 것이다. 스위치에 새로운 플로우 규칙을 추가하거나, 기존 규칙을 수정하거나, 통계 정보를 수집하는 모든 작업이 OpenFlow 메시지를 통해 수행된다.

### 왜 OpenFlow 같은 southbound 인터페이스가 필요한가

전통적인 네트워크 장비에서는 제어 평면(라우팅 프로토콜, 스위칭 프로토콜)이 장비 내부에 내장되어 있어서, 외부에서 이를programmatically 제어할 수 없었다. 각厂商는 자체적인 CLI (Command-Line Interface)나 SNMP (Simple Network Management Protocol) 기반 관리만을提供했다. OpenFlow는 네트워크 장비의 내부 동작(특히 Flow table)에 대한 표준화된 접근 방식을提供하여, 어떤厂商 장비든 동일한 방식으로 제어할 수 있게 했다.

전통적 네트워크 장비 관리 vs OpenFlow 기반 관리의 차이를 비교하면, 폐쇄적 vs 개방적 제어의差异가 부각된다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │         전통적 네트워크 장비 vs OpenFlow 기반 관리 비교                    │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  [전통적 네트워크 장비 관리]                                          │
  │                                                                     │
  │  네트워크 관리자                                                     │
  │       │                                                              │
  │       ├──CLI: 장비에 직접 명령어 입력                                  │
  │       ├──SNMP: 간단한 모니터링/설정 (MIB 기반)                        │
  │       └──XML/NETCONF: 설정 관리 (설정에 가까움, 동적 제어는 어려움)      │
  │              │                                                       │
  │              ▼                                                       │
  │       ┌──────────────────────────────────────────┐                   │
  │       │          네트워크 장비 (내부 불투명)         │                   │
  │       │  ┌─────────────────────────────────────┐ │                   │
  │       │  │  제어 평면 (라우팅 프로토콜)         │ │                   │
  │       │  │     (외부 접근 불가)                 │ │                   │
  │       │  └─────────────────────────────────────┘ │                   │
  │       │  ┌─────────────────────────────────────┐ │                   │
  │       │  │        데이터 평면 (Switching)       │ │                   │
  │       │  │     (외부 접근 불가)                 │ │                   │
  │       │  └─────────────────────────────────────┘ │                   │
  │       └──────────────────────────────────────────┘                   │
  │                                                                     │
  │  문제:厂商 종속, 외부에서 동적 제어 어려움                               │
  │                                                                     │
  │  [OpenFlow 기반 관리]                                                │
  │                                                                     │
  │  ┌──────────────┐                                                   │
  │  │SDN Controller│  ←── REST API (Northbound) ←── 네트워크 앱           │
  │  │              │                                                   │
  │  │  - Topology 관리                                                │
  │  │  - 경로 계산                                                    │
  │  │  - Flow 규칙 배포                                                │
  │  └───────┬──────┘                                                   │
  │          │                                                           │
  │          │ OpenFlow (Southbound API)                                  │
  │          │                                                           │
  │          ▼                                                           │
  │  ┌──────────────────────────────────────────┐                        │
  │  │         OpenFlow 스위치 (내부 공개)        │                        │
  │  │  ┌─────────────────────────────────────┐  │                        │
  │  │  │    Flow Table (외부에서 제어 가능)    │  │                        │
  │  │  │  Match: Dst IP, Src IP, Port ...   │  │                        │
  │  │  │  Action: Forward, Drop, Modfiy ...  │  │                        │
  │  │  └─────────────────────────────────────┘  │                        │
  │  │  ┌─────────────────────────────────────┐  │                        │
  │  │  │    Group Table (복수 액션 처리)      │  │                        │
  │  │  └─────────────────────────────────────┘  │                        │
  │  └──────────────────────────────────────────┘                        │
  │                                                                     │
  │  장점: 개방적 표준,厂商 독립, 동적 제어,全局적 최적화 가능             │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 전통적 네트워크 장비에서는 제어 평면과 데이터 평면이 모두 장비 내부에 캡슐화되어 있어, 외부에서 이들에 대해programmatically 접근하는 것이 불가능했다. 관리자는 CLI나 SNMP를 통해 일부 설정과 모니터링만 가능했지만, 패킷 전달 경로를 동적으로 변경하거나 Flow 수준에서 제어를 하는 것은厂商都不敢对外开放实现细节었다. OpenFlow는 이러한 장비 내부의 Flow table을 외부에 공개하고, Controller가 이를 표준화된 방식으로programmatically 제어할 수 있게 한다. OpenFlow 스위치는 Flow table과 Group table을 가지며, Controller는 OpenFlow 프로토콜을 통해 이 table에 규칙을 추가/수정/삭제할 수 있다. 예를 들어, Controller가「목적지 IP가 10.0.0.1인 패킷은 포트 3으로 전달하라」는 규칙을 설치하면, 스위치는 해당 패킷을 수신했을 때 그 규칙에 따라 동작한다. 이 구조의 핵심 가치는 Controller가 네트워크 전체를 보고全局적으로 최적의 경로를 계산할 수 있다는 것이다. 각 스위치가 개별적으로 라우팅을 결정하는 전통적 방식과 달리, Controller 기반 방식에서는全县의 교통 흐름을 파악하고 최적의 라우팅을 Central에서 결정한다.

### 등장 배경

1. **스탠포드大学的先行研究**: 2008년 스탠포드 대학의 Nick McKeown 교수 연구진이「OpenFlow: Enabling Innovation in Campus Networks」논문에서 처음으로 제안했다.
2. **네트워크 혁신에 대한 수요**: 기존 네트워크 장비가 새로운 프로토콜과 기능을 빠르게 지원하지 못하면서, 네트워크를 software적으로 제어하여 혁신을加速하려는 수요가 있었다.
3. **ONF (Open Networking Foundation) 설립**: 2011년 Google, Facebook, Microsoft, Verizon 등이 참여하여 ONF를 설립하고, OpenFlow의 표준화와 확산을 추진했다.

### 💡 비유

OpenFlow는，好像是一家 기업이全县の交警システム(전통적 네트워크 장비)에서、全県の交通 흐름을 파악하는中央管制室(SDN Controller)을新建하고、各信号機(스위치)에直接命令을 내려全县の交通을最適化するものと 같다. 各信号기에設置된microscopes sensor(OpenFlow)가中央管制室에全县의 상황을 실시간으로 전달하고, 中央管制실은全县의交通流量全局를 고려하여、各信号기에 명령을 내린다.

### 📢 섹션 요약 비유

 OpenFlow는，好像是一家 식당에서厨房 도우미(OpenFlow 스위치)가中央管理室(Controller)에 실시간으로厨房 상황을 보고하고, 中央管理室에서全县の厨房에統一적인 지시를 내려 체계적으로 움직이는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Flow Table** | 패킷 매칭 규칙을 저장하는 테이블 | Match Fields, Priority, Counters, Actions으로 구성 | OpenFlow 1.0+ | 信号パターン表 |
| **Match Fields** | 패킷 매칭 조건 | Src/Dst MAC, VLAN ID, Ethertype, Src/Dst IP, TCP/UDP Port 등 | L2~L4 매칭 | 信号 判断 기준 |
| **Action** | 매칭된 패킷에 대한 처리 동작 | Forward, Drop, Modify, Send to Controller 등 | OpenFlow Spec | 信号 작동命令 |
| **Controller** | 네트워크의 brain, Flow 규칙을 배포 | Topology 파악, 경로 계산, 스위치에 규칙 배포 | OpenDaylight, ONOS, Ryu | 中央管制室 |
| **OpenFlow Channel** | Controller와 스위치 간의 관리 채널 | TLS (Transport Layer Security) 또는 TCP 연결 | OpenFlow 1.0+ | 中央관제-교ocrps통신망 |
| **Group Table** | 복수의 Action을一组로 처리 | All, Select, Indirect, Fast Failover 그룹 타입 | OpenFlow 1.1+ | 一括処理装置 |

### OpenFlow 패킷 처리 과정

OpenFlow 스위치에서 패킷이 어떻게 처리되는지 상세 단계를 추적하면 다음과 같다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                  OpenFlow 패킷 처리 과정                               │
  ├─────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  [패킷 수신]                                                        │
  │       │                                                             │
  │       ▼                                                             │
  │  ┌─────────────────────────────────────────────────────────────┐   │
  │  │              Flow Table #0 에서 패킷 매칭                      │   │
  │  │                                                             │   │
  │  │  ┌─────────────────────────────────────────────────────┐   │   │
  │  │  │  Match Fields        │ Priority │    Action        │   │   │
  │  │  ├─────────────────────────────────────────────────────┤   │   │
  │  │  │  Dst IP=10.0.0.5    │   100    │ Forward:port3     │   │   │
  │  │  │  TCP DstPort=443   │    90    │ Forward:port2     │   │   │
  │  │  │  VLAN=100          │    80    │ Drop              │   │   │
  │  │  │  * (default)       │     1    │ Controller        │   │   │
  │  │  └─────────────────────────────────────────────────────┘   │   │
  │  │                                                             │   │
  │  │  매칭 순서: Priority 높은 순서대로评估                         │   │
  │  └─────────────────────────────────────────────────────────────┘   │
  │       │                                                             │
  │       ├── 매칭 발견 ──▶ 해당 Action 실행                              │
  │       │                (Forward, Drop, Modify 등)                   │
  │       │                                                             │
  │       └── 매칭 발견되지 않음 (Table-miss) ──▶                                              │
  │                │                                                     │
  │                ├── Controller에게 패킷 전송 (Packet-In)                │
  │                ├── 다음 Table으로 전송 (Table-Miss)                   │
  │                └── 패킷 드롭 ( Drop)                                  │
  │                                                                     │
  │  [Controller와의 상호작용]                                            │
  │                                                                     │
  │  Packet-In 메시지 (스위치 → Controller):                              │
  │  ┌─────────────────────────────────────────────────────────────┐   │
  │  │  OpenFlow Header: Type=Packet-In                          │   │
  │  │  Match: Src IP=192.168.1.10, Dst IP=10.0.0.5               │   │
  │  │  In Port: 1, Buffer ID: 123, Total Len: 64bytes           │   │
  │  └─────────────────────────────────────────────────────────────┘   │
  │       │                                                             │
  │       ▼                                                             │
  │  Controller가 경로 계산 후:                                          │
  │       │                                                             │
  │       ▼                                                             │
  │  Flow-Mod 메시지 (Controller → 스위치):                               │
  │  ┌─────────────────────────────────────────────────────────────┐   │
  │  │  OpenFlow Header: Type=Flow-Mod                            │   │
  │  │  Match: Dst IP=10.0.0.5                                     │   │
  │  │  Action: Forward:port3                                     │   │
  │  │  Idle Timeout: 60s (해당 시간 동안 미사용 시 규칙 삭제)      │   │
  │  │  Hard Timeout: 300s (해당 시간 후 무조건 규칙 삭제)         │   │
  │  └─────────────────────────────────────────────────────────────┘   │
  │                                                                     │
  │  [OpenFlow 버전별 주요 기능]                                          │
  │                                                                     │
  │  OpenFlow 1.0 (2009):                                               │
  │  - 레이어 2, 3, 4 매칭 (12-tuple)                                   │
  │  - 단일 Flow Table                                                   │
  │  - 주요 Action: Forward, Drop, Modify                                │
  │                                                                     │
  │  OpenFlow 1.1 (2011):                                               │
  │  - Multiple Flow Tables (테이블 체인)                                │
  │  - Group Table 추가                                                 │
  │  - MPLS, VLAN 액션 추가                                              │
  │                                                                     │
  │  OpenFlow 1.3 (2012): [현재主流 버전]                               │
  │  - Per-flow Metering                                                │
  │  --table-miss 규칙 표준화                                            │
  │  - IPv6 지원                                                         │
  │                                                                     │
  │  OpenFlow 1.4 (2013):                                               │
  │  - Optical 포트 지원                                                 │
  │  - Flow expires mechanism                                            │
  │                                                                     │
  │  OpenFlow 1.5 (2014):                                               │
  │  - Ingress Engine (스위치 진입 시 처리)                              │
  │  - Clone Action                                                     │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** OpenFlow 스위치에 패킷이 도착하면, 먼저 Flow Table #0에서 매칭 규칙을 찾는다. 각 규칙은 Match Fields(매칭 조건), Priority(우선순위), Counters(통계), Actions(동작)으로 구성된다. 가장 높은 우선순위에서부터 순서대로评估하고, 매칭되는 규칙을 찾으면 해당 Action을 실행한다. 매칭되는 규칙이 없으면 Table-miss가 발생하고, 이는 설정에 따라 Controller에게 패킷을 전송하거나(Packet-In), 다음 테이블로 전달하거나, 또는 패킷을 드롭한다. Controller가 Packet-In을 받으면全县의 topology를 참고하여 최적의 경로를 계산하고, Flow-Mod 메시지를 통해 해당 스위치에 새로운 규칙을 설치한다. 규칙에는 Idle Timeout(트래픽 미발생 시 삭제)과 Hard Timeout(시간 경과 후 삭제)이 있어, 불필요한 규칙이 오래 유지되는 것을 방지한다. OpenFlow 버전별로 기능이 추가되어, 1.1에서는 테이블 체인과 그룹 테이블이, 1.3에서는 metering과 IPv6가 추가됐다. 현재主流는 1.3이며, 많은商用/OpenFlow 스위치와 Controller가 이를 지원한다. 실무에서 중요한 점은 Flow table 크기(메모리)이다. 스위치에 설치 가능한 Flow 규칙 수는 하드웨어에 따라 제한적이므로, 너무 세밀한 규칙은 스위치 메모리를 고갈시킬 수 있다.

### 📢 섹션 요약 비유

 OpenFlow 패킷 처리 과정은，好像是一家交警이全县の信号 Pattern表( Flow Table)에 따라全县의 신호등을制御하는 것과 같다. 새로운 상황(매칭되지 않는 패킷)이 발생하면中央管制室(Controller)에 보고하고, 中央管制室에서全县을 보고 판단하여適切な信号 Pattern을 내려보낸다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교 1: OpenFlow vs 다른 Southbound 인터페이스

| 비교 항목 | OpenFlow | NETCONF | OVSDB |
|:---|:---|:---|:---|
| **초점** | 데이터 평면 제어 (패킷 전달) | 네트워크 설정 관리 | Open vSwitch 관리 |
| **추상화 수준** | Flow 규칙 (저수준) | 설정/상태 관리 (고수준) | 데이터베이스 스키마 |
| **주 용도** | 동적 경로 제어, 트래픽 engineering | 설정 배포, 백업 | vSwitch 설정 |
| **표준화** | ONF | IETF | RFC 7047 |
| **동기 방식** | 비동기 (메시지 기반) | RPC (동기/비동기) | RPC |

### 비교 2: OpenFlow 1.0 vs 1.3

| 기능 | OF 1.0 | OF 1.3 |
|:---|:---|:---|
| **Flow Table 수** | 1개 | 복수 (테이블 체인) |
| **매칭 필드** | L2~L4 (12-tuple) | L2~L4 + IPv6, MPLS 등 |
| **Group Table** | 없음 | 지원 |
| **Meter Table** | 없음 | 지원 (QoS/_RATE_LIMITING) |
| **주 사용처** | 단순 L2/L3 스위칭 | 복잡한 서비스 체인, 트래픽 공학 |

### 과목 융합 관점

- **SDN Controller**: OpenFlow는 SDN Controller가 네트워크 장비와 통신하기 위한 주된 southbound 인터페이스로 사용된다. ODL (OpenDaylight), ONOS, Ryu 등의 Controller가 OpenFlow를 지원하며, 다양한 플러그인을 통해 동시에 여러 southbound 프로토콜을 사용할 수 있다.
- **네트워크 가상화**: OpenFlow와 VXLAN을 결합하면, Controller가 VXLAN 캡슐화를 동적으로 제어할 수 있다. VM이 다른 호스트로 마이그레이션될 때, Controller가 해당 VXLAN 터널의Flow 규칙을 실시간으로 업데이트한다.

### 📢 섹션 요약 비유

 OpenFlow와 NETCONF의 차이는，好似交通事故 해결에서 현장의 순찰관(OpenFlow)이 실시간으로交通を制御하는 것과, 중앙의 행정官员(NETCONF)이事後に行政処理する 것의 차이와 같다. 각기 다른 역할을 하며, 실제 네트워크 관리에서는 둘 다 필요하다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 대규모 데이터센터의 동적 트래픽 분산**: 특정 서버로의 트래픽이 급증할 때, SDN Controller가 OpenFlow를 통해 해당 구간의 스위치에 새로운 Flow 규칙을 설치하여 트래픽을 분산시켜야 하는 상황. 아키텍트는 ODL Controller를 활용하여, 특정 IP 대역으로의 트래픽이 증가하면 자동으로 우선순위 높은 Flow 규칙을 설치하고, 부하가 줄어들면 해당 규칙을 자동으로 삭제한다.

2. **시나리오 — 大学 캠퍼스 네트워크의 Guest/VLAN 격리**: 大学 캠퍼스에서 Guest 네트워크와 내부 네트워크를 OpenFlow 기반으로 격리해야 하는 상황. 아키텍트는 OpenFlow 스위치에서 VLAN 태그 기반으로 Flow 규칙을 나누고, Guest 트래픽은 별도의 VLAN으로 격리하여 보안 수준을 높였다.

### 도입 체크리스트

- **기술적**: 스위치의 OpenFlow 버전 지원 여부와 Flow table 크기를 확인했는가? Controller의 고가용성(클러스터) 구성이 되어 있는가?
- **운영·보안적**: OpenFlow 채널의 보안(TLS 암호화)을 설정했는가? Controller 접근에 대한 인증/인가 체계가 마련되어 있는가?

### 안티패턴

- **Flow 규칙 폭발 (Rule Explosion)**: 세밀한粒度の Flow 규칙을 많이 설치하면, 스위치의 Flow table이 고갈되어 새로운 규칙을 수용하지 못하게 된다. Aggregated 된 규칙을 使用하고, 필요 이상으로 세밀한 규칙은避ける。
- **Controller 과부하**: 대량의 패킷이 Controller로 전송되면(Packet-In), Controller가 Bottle neck이 될 수 있다. 따라서 Packet-In을최소화하고, 가능한 한 스위치 내에서 처리되도록 Flow 규칙을 사전 설치해야 한다.

### 📢 섹션 요약 비유

 Flow 규칙 폭발은，好像是一家 관제실에서全县의 모든 개별 상황에 각각다른 대응 명령을 내리면、信号 Pattern表( Flow Table)가溢れして、관제실의処理능력이감당하지 못하는 상황과 같다.

---

## Ⅴ. 기대효과 및 결론

OpenFlow는 SDN의 핵심 southbound 인터페이스로서, 네트워크 장비에 대한 개방적이고 표준화된 제어를 가능하게 했다. 그러나 아직완벽한 표준은 아니며, 일부厂商은自有 기능을 위해 OpenFlow의 향상된 버전이나 독자적인 확장만 지원하는 경우도 있다. ONF는 terus 표준화를 추진하고 있으며, 5G와 Edge Computing 환경에서 새로운 활용 사례가開發되고 있다.

### 📢 섹션 요약 비유

 OpenFlow의 미래は，就好像全县의AI管理信号システムが、 Accident予測と事前回避を自動で行う智能化へと発展하는 것과 같이、 Controller와 스위치의 역할分工がより高度化し、リアルタイムな最適化가実現する。

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **SDN Controller** | OpenFlow를 통해 네트워크 장비의 Flow table을 제어하는 중앙 집중식 제어 평면 소프트웨어다. |
| **Flow Table** | OpenFlow 스위치에서 패킷 매칭 규칙을 저장하는 테이블로, Match Fields, Priority, Actions로 구성된다. |
| **Packet-In** | OpenFlow 스위치에서 매칭되지 않는 패킷을 Controller에게 전송하는 메시지다. |
| **Flow-Mod** | Controller가 스위치에 Flow 규칙을 추가/수정/삭제하는 메시지다. |
| **Southbound API** | Controller와 네트워크 장비 간 통신을 위한 인터페이스로, OpenFlow, NETCONF, OVSDB 등이 있다. |
| **ONF (Open Networking Foundation)** | OpenFlow와 SDN의 표준화를 주도하는 非营利 표준화 기관이다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. OpenFlowは，好像是一家全校の放送 시스템(SDN)에서、放送室(Controller)이各县의 信号제어반(OpenFlow 스위치)에直接命令을 내려 全校の 信号을中央管理하는 것과 같아요.
2. 만약 어떤 信号제어반이处理할 수 없는 상황(매칭되지 않는 패킷)을 만나면, 바로 방송실에 연락하고(Packet-In), 방송실에서 全县의 상황을 파악하여 적절한 命令을 다시 내려보낸다(Flow-Mod).
3. 이렇게 하면全县의 信号을 한 곳에서 효율적으로管理해서、새로운 상황(트래픽 패턴 변화)에 대응하는 것이 빠르고 정확해진다!
