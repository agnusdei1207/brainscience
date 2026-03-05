+++
title = "방화벽 (Firewall)"
date = 2026-03-05
[extra]
categories = "studynotes-security"
+++

# 방화벽 (Firewall)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 신뢰 영역(내부망)과 비신뢰 영역(외부망) 사이에서 트래픽을 제어하는 네트워크 보안 게이트웨이로, 패킷 필터링·상태 검사·프록시·차세대(NGFW) 기술이 핵심이다.
> 2. **가값**: 방화벽은 네트워크 침입의 80%를 차단하며, PCI DSS·ISMS-P 등 보안 인증의 필수 요구사항이다.
> 3. **융합**: SASE(Secure Access Service Edge)로 진화하며, ZTNA·CASB·SWG가 통합된 클라우드 네이티브 보안 플랫폼으로 발전하고 있다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**방화벽(Firewall)**이란 네트워크 보안의 제1선(first line of defense)으로, 신뢰할 수 있는 내부 네트워크와 신뢰할 수 없는 외부 네트워크(인터넷) 사이를 지나가는 트래픽을 모니터링하고, 보안 정책에 따라 허용 또는 차단하는 시스템이다.

방화벽의 핵심 기능은 **"필터링(Filtering)"**과 **"격리(Isolation)"**이다. 모든 트래픽이 방화벽을 통과하도록 네트워크를 설계하고, 정의된 규칙에 따라 위험한 트래픽을 차단한다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    방화벽 기본 개념                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   외부 네트워크 (인터넷)          내부 네트워크 (사내망)         │
│   ┌─────────────────┐            ┌─────────────────┐           │
│   │  비신뢰 영역     │            │  신뢰 영역       │           │
│   │                 │            │                 │           │
│   │  ☁️ 인터넷      │            │  🏢 서버       │           │
│   │  🌐 웹사이트    │            │  💻 PC         │           │
│   │  👨‍💻 해커      │            │  📱 모바일     │           │
│   │                 │            │                 │           │
│   └────────┬────────┘            └────────┬────────┘           │
│            │                              │                      │
│            │     ┌─────────────────┐     │                      │
│            └────▶│     방화벽       │◀────┘                      │
│                  │    🛡️ Firewall   │                            │
│                  │                 │                            │
│                  │  [필터링 규칙]   │                            │
│                  │  • IP/Port      │                            │
│                  │  • Protocol     │                            │
│                  │  • State        │                            │
│                  │  • Application  │                            │
│                  │                 │                            │
│                  │  ✅ 허용 / ❌ 차단 │                           │
│                  └─────────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 💡 비유

방화벽은 **"건물 출입구의 경비실"**과 같다.
- 건물 출입구에 경비원이 있어서 모든 방문객을 확인한다
- 허가된 사람만 들어갈 수 있고, 의심스러운 사람은 차단한다
- 24시간 감시하며 출입 기록을 남긴다

또 다른 비유로 **"국경 검문소"**가 있다.
- 국경을 넘는 모든 사람과 물품을 검사한다
- 여권과 비자를 확인하고, 위험한 물품은 압수한다
- 불법 입국을 시도하는 사람을 차단한다

### 등장 배경 및 발전 과정

**1. 기존 기술의 치명적 한계점**
- **개방형 네트워크**: 초기 인터넷은 보안 없이 설계됨
- **무차별 접근**: 누구나 어디든 접근 가능
- **웜 확산**: 1988년 Morris Worm이 인터넷의 10% 감염

**2. 혁신적 패러다임 변화**
- **1988년 1세대 패킷 필터**: IP/Port 기반 단순 필터링
- **1990년대 2세대 상태 검사**: Stateful Inspection (Check Point)
- **1990년대 3세대 프록시**: Application Layer 검사
- **2000년대 4세대 UTM**: 통합 위협 관리
- **2010년대 5세대 NGFW**: 차세대 방화벽 (DPI, 앱 인식)

**3. 비즈니스적 요구사항 강제**
- **PCI DSS**: 방화벽 설치 의무 (Req.1)
- **ISO 27001**: 네트워크 접근 통제 (A.13)
- **전자금융감독규정**: 망분리 의무

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|-----------|------|
| **패킷 필터** | IP/Port 기반 필터링 | ACL(Access Control List) 매칭 | iptables, ACL | 출입증 검사 |
| **상태 검사 엔진** | 연결 상태 추적 | State Table 관리 (SYN, EST, FIN) | Stateful Inspection | 입출입 기록 |
| **프록시** | 애플리케이션 대리 | 클라이언트-서버 간 중계 | Application Proxy | 통역사 |
| **DPI 엔진** | 페이로드 검사 | 패턴 매칭, 프로토콜 파싱 | Deep Packet Inspection | 엑스레이 |
| **IPS 엔진** | 침입 탐지/차단 | 시그니처/행위 기반 탐지 | IDS/IPS | 경비견 |
| **앱 인식** | 애플리케이션 식별 | DPI로 앱 구분 (Facebook, YouTube) | Application Control | 출석부 |

### 방화벽 진화 과정 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         방화벽 기술 진화                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [1세대: 패킷 필터 (1988~)]                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐       │
│   │  동작: 각 패킷 독립 검사                                          │       │
│   │  검사 대상: Source IP, Dest IP, Source Port, Dest Port, Protocol │       │
│   │  장점: 빠름, 단순함                                              │       │
│   │  단점: 상태 비저장, 조작된 패킷 통과 가능                         │       │
│   │                                                                  │       │
│   │  규칙 예: allow tcp any 80 → 192.168.1.10 80                    │       │
│   └─────────────────────────────────────────────────────────────────┘       │
│                                   │                                         │
│                                   ▼                                         │
│   [2세대: 상태 검사 (Stateful, 1990~)]                                       │
│   ┌─────────────────────────────────────────────────────────────────┐       │
│   │  동작: 연결 상태 추적 (State Table)                              │       │
│   │  검사 대상: 1세대 + TCP State (SYN, ACK, FIN)                   │       │
│   │  장점: TCP 연결 위조 방지, UDP/ICMP 추적                        │       │
│   │  단점: 애플리케이션 계층 검사 불가                               │       │
│   │                                                                  │       │
│   │  State Table:                                                   │       │
│   │  ┌─────────────┬───────────┬───────────┬──────────┐            │       │
│   │  │ Src IP:Port │ Dst IP:Pt │ Protocol  │ State    │            │       │
│   │  ├─────────────┼───────────┼───────────┼──────────┤            │       │
│   │  │ 10.0.0.1:50001│ 8.8.8.8:80│ TCP      │ ESTABLISHED│           │       │
│   │  └─────────────┴───────────┴───────────┴──────────┘            │       │
│   └─────────────────────────────────────────────────────────────────┘       │
│                                   │                                         │
│                                   ▼                                         │
│   [3세대: 프록시 (Application Proxy, 1995~)]                                 │
│   ┌─────────────────────────────────────────────────────────────────┐       │
│   │  동작: 클라이언트-서버 간 중계 (연결 종단)                       │       │
│   │  검사 대상: 전체 애플리케이션 데이터                            │       │
│   │  장점: 깊은 검사, IP 마스커레이딩                              │       │
│   │  단점: 느림, 프로토콜별 프록시 필요                            │       │
│   │                                                                  │       │
│   │  Client ──(1)──▶ Proxy ──(2)──▶ Server                         │       │
│   │          (별도 연결)      (별도 연결)                           │       │
│   └─────────────────────────────────────────────────────────────────┘       │
│                                   │                                         │
│                                   ▼                                         │
│   [4세대: UTM/NGFW (2000~)]                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐       │
│   │  통합 기능:                                                      │       │
│   │  • 방화벽 (Stateful)                                            │       │
│   │  • IPS (침입 방지)                                              │       │
│   │  • AV (안티바이러스)                                            │       │
│   │  • DPI (딥 패킷 인스펙션)                                        │       │
│   │  • 앱 컨트롤 (Facebook, YouTube 차단 가능)                       │       │
│   │  • 사용자 인식 (AD/LDAP 연동)                                    │       │
│   │  • VPN (IPsec/SSL)                                              │       │
│   │                                                                  │       │
│   │  대표 제품: Palo Alto, Fortinet, Cisco Firepower                │       │
│   └─────────────────────────────────────────────────────────────────┘       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: Stateful Inspection

```
[Stateful Inspection 동작 과정]

1단계: 패킷 수신
┌─────────────────────────────────────────────────────────────────┐
│ 인터페이스에서 패킷 수신                                         │
│                                                                  │
│ 패킷 구조:                                                       │
│ ┌──────────────────────────────────────────────────────────────┐│
│ │ Ethernet │ IP Header │ TCP Header │ Payload (Data)          ││
│ │ Header   │           │            │                          ││
│ └──────────────────────────────────────────────────────────────┘│
│            │             │                                       │
│            ▼             ▼                                       │
│     Src/Dst IP    Src/Dst Port, Flags                           │
└─────────────────────────────────────────────────────────────────┘

2단계: ACL 검사
┌─────────────────────────────────────────────────────────────────┐
│ ACL (Access Control List) 매칭                                   │
│                                                                  │
│ Rule 1: permit tcp any any eq 80         ← HTTP 허용            │
│ Rule 2: permit tcp any any eq 443        ← HTTPS 허용           │
│ Rule 3: deny tcp any any eq 23           ← Telnet 차단          │
│ Rule 4: deny ip 10.0.0.0/8 any           ← 사설IP 차단          │
│ Rule N: deny ip any any                  ← 기본 거부            │
│                                                                  │
│ 첫 번째 매칭되는 규칙 적용 (First Match)                         │
└─────────────────────────────────────────────────────────────────┘

3단계: State Table 검사/갱신
┌─────────────────────────────────────────────────────────────────┐
│ TCP 상태 머신 (State Machine)                                    │
│                                                                  │
│          ┌─────────────────────────────────────────────┐        │
│          │                                             │        │
│          ▼                                             │        │
│   ┌──────────┐    SYN      ┌──────────┐    SYN+ACK   │        │
│   │  CLOSED  │ ──────────▶ │ SYN_SENT │ ──────────▶  │        │
│   └──────────┘             └──────────┘              │        │
│                                                       │        │
│                            ┌──────────┐    ACK      │        │
│                      ◀──── │ESTABLISHED│ ◀─────────┘        │
│                      │     └──────────┘                      │
│                      │                                       │
│                      ▼                                       │
│   ┌──────────┐    FIN      ┌──────────┐                     │
│   │  CLOSED  │ ◀────────── │FIN_WAIT  │                     │
│   └──────────┘             └──────────┘                     │
│                                                                  │
│ State Table Entry:                                               │
│ ┌───────┬───────┬───────┬───────┬───────┬─────────┐            │
│ │Proto  │Src IP │Dst IP │Src Pt │Dst Pt │State    │            │
│ ├───────┼───────┼───────┼───────┼───────┼─────────┤            │
│ │TCP    │10.0.0.1│8.8.8.8│50001  │80     │ESTAB    │            │
│ │TCP    │10.0.0.2│9.9.9.9│50002  │443    │SYN_SENT │            │
│ └───────┴───────┴───────┴───────┴───────┴─────────┘            │
│                                                                  │
│ 규칙: State Table에 있으면 응답 패킷 허용                       │
└─────────────────────────────────────────────────────────────────┘

4단계: NAT 적용 (선택적)
┌─────────────────────────────────────────────────────────────────┐
│ NAT (Network Address Translation)                                │
│                                                                  │
│ SNAT (Source NAT): 사설IP → 공인IP                              │
│ 10.0.0.1:50001 → 203.0.113.10:50001                            │
│                                                                  │
│ DNAT (Destination NAT): 공인IP → 사설IP                         │
│ 203.0.113.10:80 → 10.0.0.100:80                                │
│                                                                  │
│ NAT Table:                                                       │
│ ┌────────────────┬────────────────┐                             │
│ │ Inside Local   │ Inside Global  │                             │
│ ├────────────────┼────────────────┤                             │
│ │ 10.0.0.1:50001 │ 203.0.113.10   │                             │
│ └────────────────┴────────────────┘                             │
└─────────────────────────────────────────────────────────────────┘

5단계: 전송/차단
┌─────────────────────────────────────────────────────────────────┐
│ 최종 결정:                                                       │
│ • PERMIT: 패킷 전송 + 로그 기록                                  │
│ • DENY: 패킷 폐기 + 로그 기록                                    │
└─────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: 방화벽 규칙 관리

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
import ipaddress

class Action(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    LOG = "LOG"

class Protocol(Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    ANY = "ANY"

@dataclass
class FirewallRule:
    """방화벽 규칙 정의"""
    rule_id: int
    action: Action
    protocol: Protocol
    source_ip: str  # CIDR 표기 가능
    source_port: Optional[int]  # None = any
    dest_ip: str
    dest_port: Optional[int]
    description: str
    enabled: bool = True

class FirewallEngine:
    """
    방화벽 규칙 엔진 (시뮬레이션)

    Features:
    - 규칙 기반 패킷 필터링
    - Stateful Inspection 시뮬레이션
    - NAT 규칙
    - 로깅
    """

    def __init__(self):
        self.rules: List[FirewallRule] = []
        self.state_table: dict = {}
        self.log: List[dict] = []

    def add_rule(self, rule: FirewallRule):
        """규칙 추가"""
        self.rules.append(rule)
        # 규칙 ID 순 정렬
        self.rules.sort(key=lambda r: r.rule_id)

    def evaluate_packet(self, src_ip: str, src_port: int,
                        dst_ip: str, dst_port: int,
                        protocol: Protocol, tcp_flags: str = None) -> Action:
        """
        패킷 평가

        Returns:
            ALLOW 또는 DENY
        """
        packet_info = {
            'src_ip': src_ip,
            'src_port': src_port,
            'dst_ip': dst_ip,
            'dst_port': dst_port,
            'protocol': protocol,
            'tcp_flags': tcp_flags
        }

        # 1. 규칙 순차 검사 (First Match)
        for rule in self.rules:
            if not rule.enabled:
                continue

            if self._match_rule(rule, packet_info):
                # 로그 기록
                self.log.append({
                    'action': rule.action.value,
                    'rule_id': rule.rule_id,
                    'packet': packet_info,
                    'description': rule.description
                })
                return rule.action

        # 2. 기본 정책 (암시적 거부)
        self.log.append({
            'action': 'DENY',
            'rule_id': 'DEFAULT',
            'packet': packet_info,
            'description': 'Default deny'
        })
        return Action.DENY

    def _match_rule(self, rule: FirewallRule, packet: dict) -> bool:
        """규칙 매칭 검사"""
        # 프로토콜 검사
        if rule.protocol != Protocol.ANY and rule.protocol.value != packet['protocol'].value:
            return False

        # 소스 IP 검사 (CIDR 지원)
        if not self._ip_match(rule.source_ip, packet['src_ip']):
            return False

        # 목적지 IP 검사
        if not self._ip_match(rule.dest_ip, packet['dst_ip']):
            return False

        # 소스 포트 검사
        if rule.source_port is not None and rule.source_port != packet['src_port']:
            return False

        # 목적지 포트 검사
        if rule.dest_port is not None and rule.dest_port != packet['dst_port']:
            return False

        return True

    def _ip_match(self, rule_ip: str, packet_ip: str) -> bool:
        """IP 주소 매칭 (CIDR 지원)"""
        if rule_ip == "any" or rule_ip == "0.0.0.0/0":
            return True

        try:
            network = ipaddress.ip_network(rule_ip, strict=False)
            address = ipaddress.ip_address(packet_ip)
            return address in network
        except ValueError:
            return rule_ip == packet_ip

    def get_log(self, limit: int = 100) -> List[dict]:
        """로그 조회"""
        return self.log[-limit:]

# 실무 예시: 기본 방화벽 규칙 설정
fw = FirewallEngine()

# 기본 규칙 추가
rules = [
    FirewallRule(10, Action.ALLOW, Protocol.TCP, "any", None, "any", 80, "HTTP 허용"),
    FirewallRule(20, Action.ALLOW, Protocol.TCP, "any", None, "any", 443, "HTTPS 허용"),
    FirewallRule(30, Action.ALLOW, Protocol.TCP, "10.0.0.0/8", None, "any", 22, "내부 SSH 허용"),
    FirewallRule(40, Action.DENY, Protocol.TCP, "any", None, "any", 23, "Telnet 차단"),
    FirewallRule(50, Action.DENY, Protocol.TCP, "any", None, "any", 3389, "RDP 차단"),
    FirewallRule(60, Action.ALLOW, Protocol.ICMP, "any", None, "any", None, "ICMP 허용"),
]

for rule in rules:
    fw.add_rule(rule)

# 패킷 테스트
test1 = fw.evaluate_packet("8.8.8.8", 50001, "10.0.0.1", 80, Protocol.TCP)
print(f"HTTP 요청: {test1.value}")  # ALLOW

test2 = fw.evaluate_packet("8.8.8.8", 50002, "10.0.0.1", 23, Protocol.TCP)
print(f"Telnet 요청: {test2.value}")  # DENY

test3 = fw.evaluate_packet("203.0.113.50", 50003, "10.0.0.1", 22, Protocol.TCP)
print(f"외부 SSH: {test3.value}")  # DENY

test4 = fw.evaluate_packet("10.0.0.100", 50004, "10.0.0.1", 22, Protocol.TCP)
print(f"내부 SSH: {test4.value}")  # ALLOW
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 비교표 1: 방화벽 유형별 비교

| 구분 | 패킷 필터 | 상태 검사 | 프록시 | NGFW |
|------|-----------|----------|--------|------|
| **계층** | L3/L4 | L3/L4 + State | L7 | L3-L7 |
| **검사 깊이** | 헤더만 | 헤더 + 상태 | 전체 | 전체 + 컨텐츠 |
| **성능** | 매우 빠름 | 빠름 | 느림 | 중간 |
| **앱 식별** | 불가 | 불가 | 가능 | 가능 |
| **IPS 통합** | 없음 | 없음 | 없음 | 있음 |
| **가격** | 낮음 | 중간 | 높음 | 높음 |

### 비교표 2: 방화벽 배치 아키텍처

| 아키텍처 | 설명 | 장점 | 단점 |
|----------|------|------|------|
| **경계 방화벽** | 내부망-외부망 경계 | 단순, 비용 저렴 | 단일 장애점 |
| **DMZ** | 3개 인터페이스 (내부/외부/DMZ) | 서버 격리 | 복잡성 증가 |
| **이중화** | Active-Active/Standby | HA 보장 | 비용 2배 |
| **내부 세그멘테이션** | 내부망 분리 | 측면 이동 차단 | 관리 복잡 |

### 과목 융합 관점 분석

**1. 네트워크 × 방화벽**
- **라우팅**: 방화벽이 라우터 역할 수행
- **VLAN**: 인터페이스별 VLAN 할당
- **QoS**: 트래픽 우선순위 관리

**2. 클라우드 × 방화벽**
- **Security Group**: AWS/.Azure 가상 방화벽
- **NACL**: 서브넷 레벨 ACL
- **WAF**: 웹 애플리케이션 방화벽

**3. 보안 운영 × 방화벽**
- **SIEM 연동**: 로그 수집 및 분석
- **SOAR**: 자동화된 대응
- **위협 인텔리전스**: 악성 IP 자동 차단

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 시나리오

**시나리오 1: 기업망 방화벽 아키텍처 설계**

```
상황: 중견기업 (직원 500명, 서버 50대)

[요구사항]
① 인터넷 접근 통제
② DMZ 서버 보호
③ 내부망 세그멘테이션
④ HA (고가용성)

[기술사적 의사결정]
┌─────────────────────────────────────────────────────────────────┐
│ [방화벽 배치 아키텍처]                                           │
│                                                                 │
│                         ┌─────────────────┐                     │
│                         │    인터넷       │                     │
│                         └────────┬────────┘                     │
│                                  │                              │
│                    ┌─────────────▼─────────────┐                │
│                    │    외부 방화벽 (NGFW)      │                │
│                    │    Active-Standby HA      │                │
│                    └─────────────┬─────────────┘                │
│                                  │                              │
│         ┌────────────────────────┼────────────────────────┐    │
│         │                        │                        │    │
│         ▼                        ▼                        ▼    │
│  ┌─────────────┐          ┌─────────────┐          ┌──────────┐│
│  │    DMZ      │          │   내부망    │          │ 관리망   ││
│  │ (Web/Mail)  │          │   (사원PC)  │          │ (서버)   ││
│  │ 10.0.1.0/24 │          │ 10.0.2.0/24 │          │10.0.3.0/24││
│  └─────────────┘          └─────────────┘          └──────────┘│
│         │                        │                        │    │
│         └────────────────────────┼────────────────────────┘    │
│                                  │                              │
│                    ┌─────────────▼─────────────┐                │
│                    │    내부 방화벽 (ISFW)      │                │
│                    │    서버/DB 세그멘테이션   │                │
│                    └───────────────────────────┘                │
│                                                                 │
│ [규칙 예시]                                                      │
│ • 인터넷 → DMZ: 80, 443만 허용                                   │
│ • 내부망 → 인터넷: 80, 443 허용, 나머지 차단                     │
│ • 내부망 → DMZ: 제한적 허용                                      │
│ • 관리망 → 전체: SSH, RDP 제한적 허용                            │
└─────────────────────────────────────────────────────────────────┘
```

### 도입 시 고려사항 체크리스트

**기술적 고려사항**
- [ ] 처리 용량 (Gbps, 동시 세션 수)
- [ ] 인터페이스 수 (포트 수)
- [ ] HA 구성 방식
- [ ] VPN 통합 여부

**운영/보안적 고려사항**
- [ ] 규칙 관리 프로세스
- [ ] 로그 보관 정책
- [ ] 정기 규칙 검토
- [ ] 장애 대응 계획

**주의사항 및 안티패턴**

| 안티패턴 | 문제점 | 올바른 접근 |
|----------|--------|-------------|
| **Allow Any Any** | 모든 트래픽 허용 | 최소 권한 원칙 |
| **규칙 과다** | 성능 저하, 관리 어려움 | 정기 정리, 그룹화 |
| **로깅 미설정** | 포렌식 불가 | 전체 로그 또는 차단 로그 |
| **단일 방화벽** | SPOF | HA 구성 |

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|------|---------|---------|-----------|
| **외부 침입 차단** | 0% | 80%+ | **80%+ 차단** |
| **악성 트래픽 탐지** | 수동 | 자동 | **실시간 탐지** |
| **규제 준수** | 미준수 | PCI DSS 준수 | **컴플라이언스** |
| **장애 대응** | 수시간 | 수분 | **MTTR 단축** |

### 미래 전망 및 진화 방향

**1. SASE (Secure Access Service Edge)**
- 네트워크 + 보안 통합 클라우드 서비스
- ZTNA, CASB, SWG 통합
- 원격 근무 지원

**2. AI 기반 위협 탐지**
- 머신러닝 기반 이상 탐지
- 자동화된 규칙 생성
- 위협 인텔리전스 통합

**3. 제로 트러스트 통합**
- 마이크로 세그멘테이션
- 지속적 검증
- 컨텍스트 기반 접근

### ※ 참고 표준/가이드

| 표준 | 내용 | 적용 범위 |
|------|------|-----------|
| **NIST SP 800-41** | 방화벽 가이드 | 미국 정부 |
| **ISO/IEC 27001 A.13** | 네트워크 보안 | 글로벌 |
| **PCI DSS Req.1** | 방화벽 요구사항 | 금융 |
| **CIS Control 9** | 네트워크 포트 제한 | 글로벌 |

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [NGFW (차세대 방화벽)](./ngfw.md): 진화된 방화벽 기술
- [IDS/IPS](./ids_ips.md): 침입 탐지/방지 시스템
- [WAF (웹 방화벽)](./waf.md): 웹 애플리케이션 보호
- [DMZ 설계](./dmz_design.md): 네트워크 분할 아키텍처
- [SASE/ZTNA](./sase_ztna.md): 클라우드 네이티브 보안
- [제로 트러스트](../1_intro/zero_trust_architecture.md): 보안 패러다임

---

## 👶 어린이를 위한 3줄 비유 설명

**🚪 아파트 경비실**
아파트 입구에 경비 아저씨가 계셔요. 모르는 사람은 들어가지 못하고, 사는 사람만 들어갈 수 있어요.

**🏰 성문 경비병**
옛날 성문에는 경비병이 있었어요. 적군은 못 들어가고, 우리 편만 들어갈 수 있게 지켰어요.

**🛂 공항 출입국 심사**
외국 여행 갈 때 공항에서 여권을 검사해요. 여권이 없거나 이상하면 비행기를 못 타요.

---

*최종 수정일: 2026-03-05*
*작성 기준: 정보통신기술사·컴퓨터응용시스템기술사 대비 심화 학습 자료*
