+++
weight = 604
title = "ICMP (Internet Control Message Protocol)"
description = "네트워크 계층의 제어 및 오류 보고 프로토콜 ICMP의 구조와 활용을 다룬다."
date = 2024-01-18

[extra]
categories = ["studynote-software-engineering"]
topics = ["network-layer", "icmp", "network-diagnosis"]
study_section = ["section-6-network-layer-ip"]

number = "604"
core_insight = "ICMP는 IP 수준의 제어 메시지 및 오류 보고 프로토콜로, ping, traceroute 등의 진단 도구에서 활용되며, 네트워크 신뢰성과 보안에 중요한 역할을 한다."
key_points = ["IP 수준의 제어/오류 보고", "Type + Code 조합으로 메시지 식별", "ping (Echo), traceroute 활용", "ICMP 기반 공격 방어 (ICMP 필터링)"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ICMP (Internet Control Message Protocol)는 IP 프로토콜의 제어 및 오류 보고를 담당하는 네트워크 계층 프로토콜로, RFC 792로 표준화되었다.
> 2. **가치**: 네트워크 진단 (ping, traceroute), 오류 보고 (목적지 도달 불가, 시간 초과), 라우팅 최적화 (ICMP Redirect)에 필수적인 역할을 수행한다.
> 3. **융합**: ICMP는 네트워크 보안과 직결되며, ICMP 기반 공격 (Smurf, Ping of Death, ICMP Tunneling)을 방지하기 위한 필터링 정책과 DDoS 완화 기술이 중요하다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

**개념**: ICMP는 IP 프로토콜의 상위에서 작동하는 네트워크 계층 프로토콜로, IP 패킷 전달 과정에서 발생하는 오류를 보고하고, 네트워크 상태를 진단하며, 라우팅을 최적화하는 기능을 제공한다. ICMP 메시지는 IP 헤더의 Protocol 필드 값이 1로 설정되어 구분된다. ICMP는 신뢰성 있는 전송을 보장하지는 않으며, 오류 발생 시 스스로 오류를 보고할 뿐 스스로 복구하지는 않는다. 메시지 유형은 Type (1바이트)과 Code (1바이트)의 조합으로 결정되며, 각 조합이 특정 의미을 갖는다.

**필요성**: IP는 비연결형 프로토콜로, 목적지 도달 가능성, 경로 상태, 네트워크 혼잡 등에 대한 피드백 메커니즘이 없다. ICMP는 이러한 IP의 limitations을 보완하여, 목적지 도달 불가 시 송신자에게 알려주고, 패킷 생존 시간 초과 시 경고하며, 네트워크 경로 문제를 진단할 수 있게 한다. 특히 인터넷 상에서 문제를 격리하고 진단하는 데 ICMP는 없어서는 안 될 도구이다.

**비유**: ICMP는 인터넷의 **신고 전화**와 같다. 택배 (IP 패킷)가 배달되지 못했을 때, 택배 회사가 발신자에게 "수신지 주소를 찾을 수 없습니다", "수신자가不在입니다", "도로가堵られて 배달이 어렵습니다"などと 알려주는 것이다. 이를 통해 발신자는問題の原因を把握し, 적절한 조치를 취할 수 있다.

**등장 배경**: 1981년 RFC 777, RFC 792로 표준화된 ICMP는 이후 IPv6 환경에서는 ICMPv6 (RFC 4443)로 확장되었으며, Neighbor Discovery, Multicast Group Management 등의 기능이 추가되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### ICMP 헤더 구조

ICMP 메시지는 8바이트 헤더와 가변 길이 데이터 영역으로 구성된다. Type 필드는 메시지 유형을, Code 필드는同一 Type 내의 상세 유형을 나타낸다. Checksum은 ICMP 메시지 전체의 오류 검출을 위해 사용되며, Rest of Header (또는 Message Body)는 Type/Code에 따라異なる構造を持つ다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    ICMP 메시지 구조                                    │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │   0                   1                   2                   3    │  │
│  │   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1│  │
│  │  ├─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┤│  │
│  │  │    Type     │    Code     │        Header Checksum         ││  │
│  │  │   (8비트)    │   (8비트)    │          (16비트)               ││  │
│  │  ├─────────────┴─────────────┴─────────────────────────────────┤│  │
│  │  │              Rest of Header (32비트)                         ││  │
│  │  │         (Type/Code에 따라 의미가 다름)                        ││  │
│  │  ├──────────────────────────────────────────────────────────────┤│  │
│  │  │                   ICMP Data (가변 길이)                      ││  │
│  │  │              (원본 IP 헤더 + 처음 8바이트 페이로드 포함)       ││  │
│  │  └──────────────────────────────────────────────────────────────┘│  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  주요 ICMP Type/Code 조합:                                            │
│                                                                       │
│  Type 0  (Echo Reply)           — ping 응답                           │
│  Type 3  (Dest Unreachable)     — 목적지 도달 불가                    │
│         Code 0: Network unreachable                                   │
│         Code 1: Host unreachable                                     │
│         Code 2: Protocol unreachable                                │
│         Code 3: Port unreachable                                     │
│         Code 4: Fragmentation needed (DF bit set)                    │
│         Code 5: Source route failed                                  │
│                                                                       │
│  Type 8  (Echo Request)           — ping 요청                        │
│                                                                       │
│  Type 11 (Time Exceeded)         — TTL/시간 초과                      │
│         Code 0: TTL expired in transit                                │
│         Code 1: Fragment reassembly time exceeded                    │
│                                                                       │
│  Type 12 (Parameter Problem)     — 헤더 파라미터 오류                  │
│                                                                       │
│  Type 40 (Traceroute,单向)       —Traceroute 용 (Linux)               │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** ICMP 메시지의 핵심 설계 원칙은 "오류 발생 시 원인을_reportする" 것이다. 특히 오류 보고 메시지에는 반드시 원인 사건을 유발한 원본 IP 헤더와 처음 8바이트 (일반적으로 TCP/UDP 포트 번호 또는 ICMP ID/sequence 번호)를 포함한다. 이를 통해 수신자가 어떤 연결/프로세스에 대한 오류인지 идентифика션할 수 있다. 단, ICMP 오류 메시지는 다른 ICMP 오류 메시지를 유발하지 않도록 설계되어 있어, ICMP 메시지의 폭증에 따른 악순환을 방지한다.

### ping과 Echo/Echo Reply

ping은 ICMP Echo Request/Reply를 활용하여 목적지까지의 기본 연결성을 확인하는 도구이다. 송신지는 ICMP Echo Request (Type 8)를 보내고, 수신지는 ICMP Echo Reply (Type 0)로 응답한다. ping의 출력에는 목적지 응답 시간 (RTT, Round Trip Time), 패킷 분실률 등의 정보가 포함되어 네트워크 상태를 파악하는 데 활용된다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    ping 동작 과정                                       │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  [Host A]                          [Host B]                           │
│  192.168.1.10                       192.168.1.20                      │
│                                                                       │
│  ① Echo Request 전송 (Type 8, Code 0):                                │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │ IP Header:                                                     │   │
│  │   Src: 192.168.1.10  Dst: 192.168.1.20                        │   │
│  │ ICMP Header:                                                  │   │
│  │   Type: 8 (Echo Request)                                      │   │
│  │   Code: 0                                                     │   │
│  │   Identifier: 0x1234 (ping 프로세스 ID)                        │   │
│  │   Sequence Number: 1                                          │   │
│  │ Data: 'abcdefghijklmnopqrstuvwxyz...' (패드 데이터)             │   │
│  └───────────────────────────────────────────────────────────────┘   │
│           │                                                           │
│           ▼                                                           │
│  ② Echo Reply 수신 (Type 0, Code 0):                                  │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │ IP Header:                                                     │   │
│  │   Src: 192.168.1.20  Dst: 192.168.1.10  ◀─ 반대로               │   │
│  │ ICMP Header:                                                  │   │
│  │   Type: 0 (Echo Reply)                                        │   │
│  │   Code: 0                                                     │   │
│  │   Identifier: 0x1234 (원본 요청과 동일)                        │   │
│  │   Sequence Number: 1 (원본 요청과 동일)                        │   │
│  │ Data: 'abcdefghijklmnopqrstuvwxyz...' (동일)                   │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ping 실행 결과 예시:                                                  │
│  $ ping -c 4 192.168.1.20                                             │
│  PING 192.168.1.20 (192.168.1.20) 56(84) bytes of data.               │
│  64 bytes from 192.168.1.20: icmp_seq=1 ttl=64 time=0.321 ms         │
│  64 bytes from 192.168.1.20: icmp_seq=2 ttl=64 time=0.289 ms         │
│  64 bytes from 192.168.1.20: icmp_seq=3 ttl=64 time=0.275 ms         │
│  64 bytes from 192.168.1.20: icmp_seq=4 ttl=64 time=0.301 ms         │
│                                                                       │
│  --- 192.168.1.20 ping statistics ---                                │
│  4 packets transmitted, 4 received, 0% packet loss, time 3002ms     │
│  rtt min/avg/max/mdev = 0.275/0.296/0.321/0.017 ms                   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** ping의 Identifier (ID)와 Sequence Number는 동일 호스트에서 실행된 복수의 ping 프로세스를 구분하는 데 사용된다. Unix/Linux 시스템에서는 각 ping 프로세스가 고유한 ID (프로세스 PID 또는 random 값)를 사용하며, Windows에서는 기본적으로 0이 사용된다. Identifier와 Sequence Number가 일치하는 Request/Reply 쌍을 매칭하여, 비동기적으로 도착하는 응답이나 중복 응답을 올바르게 처리한다. RTT (Round Trip Time)가 높으면 네트워크 지연이 크고, packet loss가 있으면 네트워크 경로에 문제가 있음을暗示한다.

### traceroute와 TTL 초과

traceroute는 ICMP Time Exceeded 메시지 (Type 11, Code 0)를 활용하여 목적지까지의 경로와 각 홉의 지연 시간을 측정한다. TTL을 1부터 단계적으로 증가시키면서 UDP 패킷 (또는 ICMP Echo Request)을 보내면, 각 라우터에서 TTL=0이 되어 ICMP Time Exceeded가 반환된다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    traceroute 동작 과정                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  traceroute는 UDP 목적지 포트를 점점 증가시키며 전송:                   │
│  TTL=1: UDP → 192.168.1.1 (게이트웨이)                                  │
│  라우터가 TTL=0 초과 → ICMP Time Exceeded (Type 11, Code 0) 회신      │
│  → 첫 홉 IP/지연 시간 기록                                              │
│                                                                       │
│  TTL=2: UDP → 다음 라우터                                               │
│  → 두 번째 홉 IP/지연 시간 기록                                         │
│  ...                                                                  │
│                                                                       │
│  목적지 도달 시:                                                        │
│  → UDP 포트에 도달할 수 없다는 ICMP Dest Unreachable (Type 3, Code 3)  │
│                                                                       │
│  traceroute 결과 예시:                                                  │
│  $ traceroute -I 8.8.8.8                                              │
│  traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets       │
│  1  192.168.1.1 (192.168.1.1)  1.234 ms   0.890 ms   0.801 ms         │
│  2  10.0.0.1 (10.0.0.1)        5.678 ms   5.432 ms   5.401 ms         │
│  3  72.14.215.85              15.321 ms  15.198 ms  15.102 ms         │
│  4  108.170.252.129           14.567 ms  14.432 ms  14.398 ms         │
│  5  8.8.8.8 (8.8.8.8)         14.321 ms  14.198 ms  14.102 ms         │
│                                                                       │
│  각 홉별 3회 측정 (기본값) → 평균 지연 시간 표시                        │
│  * 표시: 해당 라우터가 ICMP 응답을 차단하여 경유지만 확인               │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │  traceroute 변형:                                               │  │
│  │  • -I: ICMP Echo Request 사용 (기본)                            │  │
│  │  • -T: TCP SYN 사용 (방화벽이 UDP를 차단하는 경우)               │  │
│  │  • -U: UDP 사용 (기본, -I 없이)                                  │  │
│  │  • -m max_ttl: 최대 TTL 값 설정 (기본 30)                       │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** traceroute의 핵심 원리는 "TTL을阶段性으로 늘려가며 각 라우터에서 되돌아오는 Time Exceeded 메시지를 수집하는 것"이다. 각 라우터는 패킷을 전달할 때 TTL을 1 감소시키며, TTL이 0이 되면 패킷을 폐기하고 송신자에게 ICMP Time Exceeded (Type 11, Code 0)를 반환한다. 이를 통해 첫 번째 라우터(TTL=1), 두 번째 라우터(TTL=2) 등을 순차적으로 파악할 수 있다. 마지막 홉에서는 목적지가 UDP 패킷을 수신하지만 해당 포트가 열려 있지 않으므로, ICMP Port Unreachable (Type 3, Code 3)로 응답하여 traceroute 종료를 감지한다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### ICMP Type별 용도 정리

| Type | Code | 의미 | 주요 용도 |
|:---|:---|:---|:---|
| 0 | 0 | Echo Reply | ping 응답, 연결성 확인 |
| 3 | 0~15 | Destination Unreachable | 목적지 도달 불가 원인 보고 |
| 3 | 0 | Network Unreachable | 라우팅 경로 없음 |
| 3 | 1 | Host Unreachable | 호스트 응답 없음 |
| 3 | 3 | Port Unreachable | 포트 열려 있지 않음 (traceroute) |
| 3 | 4 | Fragmentation Needed | PMTUD (Path MTU Discovery) |
| 8 | 0 | Echo Request | ping 요청 |
| 11 | 0 | TTL Expired | traceroute |
| 11 | 1 | Fragment Reassembly Time Exceeded | 분할 조립 시간 초과 |
| 12 | 0 | IP Header Bad | 헤더 오류 |

### ICMP 기반 공격 및 방어

ICMP는 네트워크 진단에 필수적이지만, 다양한 공격에 악용될 수 있다. **Smurf 공격**은 ICMP Echo Request를Broadcast로 변환하여 대규모 반사형 DDoS를 수행한다. **Ping of Death**는 규정 초과 크기의 패킷을 fragmentation하여 시스템 오류를 유발한다 (현재는 대부분 차단됨). **ICMP Tunneling**은 ICMP 패킷 내부에 데이터를 캡슐화하여 방화벽을 우회한다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    주요 ICMP 기반 공격                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ① Smurf 공격 (DDoS Reflector Attack)                                  │
│     공격자 ──▶ 라우터 (broadcast) ──▶ 피해자 (amplification)           │
│                                                                       │
│     과정:                                                              │
│     1. 공격자가 피해자 IP로 위장한 ICMP Echo Request를 broadcast 전송   │
│     2.路由器가 broadcast를 네트워크 전체에 전파                           │
│     3. 모든 호스트가 피해자 IP로 Echo Reply 전송                         │
│     4. 피해자는 amplified traffic로 인해 서비스 불능                     │
│                                                                       │
│     방어:                                                              │
│     • 라우터에서 directed broadcast 차단                               │
│     • 퍼드侧에서 ICMP Echo Request_rate 제한                          │
│     • CISCO: "no ip directed-broadcast"                               │
│                                                                       │
│  ② Ping of Death                                                       │
│     - IPv4 패킷의 최대 MTU (65,535바이트)보다 큰 패킷을 전송           │
│     - 단편화 후 합산 시 버퍼 오버플로우 발생                            │
│     - 현대 OS는 대부분 방어되어 실효성 낮음                             │
│                                                                       │
│  ③ ICMP Tunneling (코딩)                                               │
│     - ICMP Echo Request/Reply 데이터 부분에 터널링 데이터 삽입          │
│     - 방화벽이 ICMP를 허용하면 우회 가능                                │
│     - Example: ICMPTX, ptunnel                                          │
│                                                                       │
│     방어:                                                              │
│     • ICMP 페이로드 크기/패턴 모니터링                                  │
│     • IDS/IPS에서 ICMP 터널 시그니처 탐지                               │
│     • 네트워크 세그먼트 분리                                            │
│                                                                       │
│  ④ ICMP Redirect 공격                                                  │
│     - 공격자가 ICMP Redirect를 보내 경로를 변경                         │
│     - MITM 공격으로 발전 가능                                          │
│                                                                       │
│     방어:                                                              │
│     • 기본적으로大多数 OS가 ICMP Redirect 무시 (보안 설정)               │
│     • 보안 장비에서 ICMP Redirect 필터링                               │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** ICMP 기반 공격의 공통된 특성은 "정상적인 ICMP 기능을 역이용"한다는 점이다. 따라서 완벽한 ICMP 차단은 네트워크 진단과 관리에 심각한 지장을 초래한다. 적절한 보안 정책은 ICMP 타입별로 세분화하여, 불필요한 ICMP는 차단하고 필요한 ICMP는 허용하되, rate limiting과 모니터링을 병행하는 것이다. 예를 들어, ICMP Echo Request (ping)를 완전히 차단하기보다는, rate limiting (초당 N개까지만 허용)하여 DDoS 반사 공격의 효과를 줄이고, 동시에 IDS에서 비정상적 ICMP 패턴을 탐지하는 것이 합리적이다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 1 — Path MTU Discovery (PMTUD)**: IPv4 환경에서 큰 패킷이 작은 MTU의 링크를 통과해야 할 때, 라우터가 ICMP Destination Unreachable (Type 3, Code 4, "Fragmentation Needed") 메시지를 반환한다. 송신자는 이 메시지를 받아 패킷 크기를 줄여 재전송한다. 그러나 일부 네트워크에서 ICMP가 차단되면, 송신자는 작은 패킷만 수신하게 되어 성능이 급격히 저하된다 (ICMP Blackhole). 이를 해결하기 위해 TCP PMTUD는 최소값으로 떨어지지 전까지 패킷 크기를 점진적으로 조절한다.

**시나리오 2 — 네트워크 진단에서의 ICMP 활용**: 네트워크 장애 시的第一步은 보통 ping으로 기본 연결성을 확인하는 것이다. ping이 실패하면 traceroute로 어느 홉에서 문제가 발생하는지 파악하고, ICMP Type/Code로 구체적인 원인을 추정한다. 예를 들어, "Destination Host Unreachable"은 ARP 단계의 문제를, "Request Timed Out"은 경로상의 방화벽이 ICMP를 차단하거나 TTL이 0이 된 것을暗示한다.

**시나리오 3 — IPv6 환경에서의 ICMPv6**: IPv6에서는 ICMPv6 (RFC 4443)가 ARP를 대체하고 (NDP), 주소 자동 설정, 중복 주소 검출, 라우터 발견 등에 핵심적인 역할을 수행한다. ICMPv6 메시지 중 생존에 필수적인 것은 반드시 허용해야 하며, 이를 차단하면 IPv6 연결성이 완전히 손상될 수 있다. 예를 들어, Packet Too Big (Type 2) 메시지가 차단되면 Path MTU Discovery가 작동하지 않는다.

### 도입 체크리스트

- **기술적**: 네트워크 장치별 ICMP 처리 정책 확인, PMTUD 동작 여부 검증, traceroute 결과에서 불명확한 홉 조사
- **운영·보안적**: 주요 ICMP 타입 (Echo, Time Exceeded, Destination Unreachable) 허용하되 rate limiting 적용, ICMP 기반 공격 시그니처 모니터링, 특정 ICMP 타입 (Redirect, Router Advertisement) 차단은 필요한 위치만

### 안티패턴

- **ICMP 완전 차단**: 보안을 위해 ICMP를 모두 차단하면, 경로 MTU 발견이 실패하고, 네트워크 진단이 불가능해지며, 외부에서 내부 문제 파악이 어렵다.
- **ICMP 무차별 허용**: 모든 ICMP를 허용하면 Smurf, DDoS 반사 공격의 대상이 될 수 있다. 특히 directed broadcast와 large ICMP 패킷은 주의가 필요하다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | ICMP 미사용 | ICMP 사용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 네트워크 장애 원인 파악 불가 | 홉 단위 장애 지점 특정 | MTTR (Mean Time To Repair) **60% 감소** |
| **정량** | PMTUD 실패로 항상 작은 패킷 | 큰 패킷으로 효율적 전송 | 네트워크 처리량 **20% 향상** (MTU 차이) |
| **정성** | DDoS 보호 유리 | DDoS 반사 공격 위험 | 적절한 rate limiting으로 균형 유지 |

### 미래 전망

ICMP는 네트워크 계층의 근본적인 부분으로서, 그 역할이 크게 변하지 않을 것이다. IPv6 환경에서 ICMPv6의 역할이 더욱 중요해지고 있으며, 특히 NDP (Neighbor Discovery Protocol)의 핵심 구성 요소로 활용된다. 반면, 네트워크 보안 환경에서 ICMP의 역할은 계속 논쟁의 대상이 될 것이며, 세분화된 ICMP 정책 (type별 허용/차단, rate limiting, 모니터링)이 표준 화려할 것으로 예상된다.

### 참고 표준

- RFC 792 — Internet Control Message Protocol
- RFC 4443 — Internet Control Message Protocol (ICMPv6) for IPv6
- RFC 1812 — Requirements for IP Version 4 Routers
- NIST SP 800-42 — Guideline on Network Security Testing (ICMP 보안)

ICMP는 네트워크의 "신고 전화"로서, 적절한 관리가 네트워크 운영의 핵심이다. ICMP를 완전히 차단하는 것은 네트워크 가시성과 진단 능력을 스스로 포기하는行為이며, 반면 무차별 허용은 보안 위험을 초래한다. 적정한 ICMP 정책의 수립과 유지가 네트워크 전문가의 중요한 역할이다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **ping** | ICMP Echo Request/Reply를 활용한 연결성 진단 도구로, RTT와 packet loss를 측정한다. |
| **traceroute** | ICMP Time Exceeded와 UDP를 활용하여 목적지까지의 홉별 경로와 지연 시간을 측정한다. |
| **PMTUD (Path MTU Discovery)** | ICMP Destination Unreachable (Fragmentation Needed)를 활용하여 경로 상의 최대 MTU를 찾는 메커니즘이다. |
| **ARP** | IP 주소를 MAC 주소로 변환하는 프로토콜로, ICMP와 함께 네트워크 계층의 핵심 구성 요소이다. |
| **ICMPv6 (IPv6)** | IPv6 환경에서 ICMP를 확장한 프로토콜로, NDP, DAD, Router Discovery 등의 기능을 제공한다. |
| **NDP (Neighbor Discovery Protocol)** | IPv6에서 ARP, Router Discovery, ICMP Redirect를 통합한 프로토콜로, ICMPv6 메시지를 활용한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. ICMP는 택배 (IP 패킷)가 Delayed됐을 때 "어디서 문제가 생겼는지"를 알려주는 **택배 추적 문자**와 같아요. "수신지에 갈 수 없어요", "도로가堵新加坡", "수령인이 없어요"など 다양한 이유를 сообщи다.
2. ping은 "당신 연결되세요?"라고 **전화벨을 울리는** 것이고, traceroute는 각铎관（日本）の通过点をチェックして教えてくれる **경유지 추적 서비스**예요.
3. 하지만 이 서비스를 악용하면 "폭탄 전화" (ICMP DDoS 공격)가 될 수 있어서,現代의 택배 회사는通过량을 제한하거나（中国, 속도限制）보안檢索을 해요!
