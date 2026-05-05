+++
weight = 292
title = "292. VPN 집선장치 (VPN Concentrator)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: VPN 집선장치(VPN Concentrator)는 수백~수천 개의 원격 VPN 터미널 세션을 하나의 전용 하드웨어에서 종단(Termination)하여, 라우터·방화벽에 가해지는 암호화 부하를 분리한다.
> 2. **가치**: 전용 ASICs(Application-Specific Integrated Circuits)로 TLS/IPsec 암호화 오프로드(Offload)를 처리하므로, 범용 소프트웨어 VPN 대비 처리량이 수십 배 높고 지연이 낮다.
> 3. **판단 포인트**: 규모가 수십 명 이하이면 소프트웨어 VPN으로 충분하지만, 동시 접속 수백 명 이상이거나 SLA(Service Level Agreement) 요건이 있을 때 하드웨어 Concentrator + HA(High Availability) 이중화가 필수다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

재택근무·원격 지사 연결이 일상화되면서 기업 네트워크는 단일 인터넷 경계를 넘어 분산된 엔드포인트를 수용해야 한다. VPN(Virtual Private Network)은 공용 인터넷 위에 암호화된 터널을 구성하여 사설 네트워크를 확장하는 핵심 기술이다. 그러나 라우터나 방화벽에서 VPN 기능을 겸용할 경우, 암호화·복호화 연산이 패킷 포워딩 성능을 잠식한다.

VPN Concentrator는 이 암호화 처리를 전담하는 **단일 목적(Purpose-built) 장비**다. 처음에는 Cisco의 VPN 3000 시리즈처럼 물리적 어플라이언스 형태로 등장했고, 이후 ASA(Adaptive Security Appliance)·Palo Alto·Fortinet 등이 통합 보안 어플라이언스 안에 Concentrator 기능을 내재화했다. 최근에는 클라우드 기반 VPN 게이트웨이(AWS Site-to-Site VPN, Azure VPN Gateway)도 같은 역할을 수행한다.

동시 터널 수가 늘어날수록 세션 상태 테이블, 암호화 키 관리, QoS(Quality of Service) 정책이 복잡해진다. Concentrator는 이를 전용 하드웨어 칩과 분리된 관리 평면(Management Plane)으로 처리하여 확장성을 보장한다.

📢 **섹션 요약 비유**: 공항 출입국 심사대에서 모든 승객이 한 창구에 몰리면 줄이 막힌다. VPN Concentrator는 전용 심사 부스를 별도로 설치해 VPN 승객(암호화 트래픽)만 빠르게 처리하는 것과 같다.

---

## 2. 구성요소

### 내부 구성 요소

| 구성 요소 | 역할 |
|:---|:---|
| 암호화 오프로드 엔진 (Crypto Offload ASIC) | IPsec ESP/AH, TLS 암·복호화를 하드웨어에서 처리 |
| 세션 상태 테이블 (Session State Table) | 각 VPN 터널의 SA(Security Association) 정보 유지 |
| IKE 데몬 (Internet Key Exchange Daemon) | 키 협상(Phase 1/2 또는 IKEv2) 처리 |
| 로드 밸런서 (Load Balancer) | 클러스터 내 Concentrator 간 세션 분산 |
| HA 관리자 (High Availability Manager) | 액티브·스탠바이 간 상태 동기화, 페일오버 |

```
인터넷
   │
   ▼
┌──────────────────────────────────┐
│        VPN Concentrator Cluster  │
│                                  │
│  ┌──────────────┐  ┌────────────┐│
│  │  Active Unit │  │Standby Unit││
│  │  ┌─────────┐ │  │            ││
│  │  │Crypto   │ │  │  State     ││
│  │  │ASIC     │ │  │  Sync ◀──▶ ││
│  │  └─────────┘ │  │            ││
│  └──────────────┘  └────────────┘│
│          │                       │
│    ┌─────▼─────┐                 │
│    │  Session  │                 │
│    │  Table    │                 │
│    └─────┬─────┘                 │
└──────────┼───────────────────────┘
           ▼
     내부 사설 네트워크 (LAN)
```

**IKEv2(Internet Key Exchange version 2)** 기반 IPsec 터널은 다음 순서로 수립된다.

1. **SA_INIT**: 알고리즘 협상, DH(Diffie-Hellman) 키 교환
2. **AUTH**: 인증서 또는 PSK(Pre-Shared Key)로 상호 인증
3. **CREATE_CHILD_SA**: 데이터 채널 IPsec SA 생성
4. 이후 **ESP(Encapsulating Security Payload)** 패킷으로 암호화 통신

HA 구성에서 액티브 유닛이 장애를 일으키면, 스탠바이 유닛이 세션 테이블을 그대로 이어받아 **Stateful Failover**를 수행한다. 이때 기존 VPN 클라이언트는 재인증 없이 연결을 유지할 수 있다.

📢 **섹션 요약 비유**: 비행기 두 대가 항상 같은 항로 정보를 공유하다가, 기장이 갑자기 쓰러지면 부기장이 조종간을 넘겨받아 승객이 흔들림 없이 목적지에 도달하는 것과 같다.

---

## 3. 구조 및 동작 원리

### 소프트웨어 VPN vs 하드웨어 VPN Concentrator

| 항목 | 소프트웨어 VPN | 하드웨어 Concentrator |
|:---|:---|:---|
| 동시 터널 수 | 수십~수백 (CPU 한계) | 수천~수만 (ASIC 처리) |
| 암호화 처리 방식 | 범용 CPU | 전용 암호화 ASIC |
| 지연 (Latency) | 상대적으로 높음 | 마이크로초 단위 처리 |
| HA·이중화 | 별도 구성 복잡 | 내장 Stateful Failover |
| 초기 비용 | 낮음 | 높음 |
| 운영 복잡도 | 서버 관리와 동일 | 전용 CLI/GUI |
| 적합 규모 | 소규모 (< 100명) | 중대형 (100명 이상) |
| 클라우드 전환 | 가상 어플라이언스 | Cloud VPN Gateway |

📢 **섹션 요약 비유**: 작은 동네 빵집은 오너가 직접 빵을 굽지만(소프트웨어 VPN), 대형 프랜차이즈 본사는 전용 제과 공장을 두어 수십만 개를 찍어낸다(하드웨어 Concentrator).

---

## 4. 비교 및 트레이드오프

### 설계 체크리스트

**규모 산정**: 동시 접속 피크 기준으로 Concentrator 처리량(Mbps)과 세션 수(Session Count)를 산정한다. 일반적으로 피크의 150% 여유를 확보한다.

**HA 구성 선택**:
- **Active/Standby**: 구성 단순, 자원 낭비 50%
- **Active/Active**: 로드 밸런싱으로 자원 활용률 향상, 단 세션 동기화 오버헤드 증가

**분할 터널링 (Split Tunneling) 정책**: 사내 트래픽만 VPN 터널로 보내고, 일반 인터넷은 로컬 브레이크아웃하면 Concentrator 부하를 크게 줄일 수 있다. 단, 보안 정책 우회 위험을 DLP(Data Loss Prevention)·CASB(Cloud Access Security Broker) 보완 통제로 관리해야 한다.

**인증 연동**: RADIUS(Remote Authentication Dial-In User Service) 또는 LDAP(Lightweight Directory Access Protocol) 서버와 연동하여 사용자 계정을 중앙 관리하고, MFA(Multi-Factor Authentication)를 적용한다.

**기술사 논술 포인트**: "VPN Concentrator 도입 시 핵심 판단 요소를 서술하라"는 문항에는 ①처리량·동시 세션 수 산정, ②HA 토폴로지 선택, ③분할 터널링 보안 보완, ④클라우드 환경에서의 가상화(vConcentrator) 전환 방향까지 4단계로 논리를 구성한다.

📢 **섹션 요약 비유**: 도로 설계사가 다리를 놓을 때 현재 통행량만 보는 게 아니라, 10년 후 교통량까지 예측해 차선 수를 정하는 것처럼, Concentrator 도입도 미래 확장성을 먼저 계산해야 한다.

---

## 5. 실무 적용 및 최적화 기법

VPN Concentrator의 핵심 가치는 **암호화 처리의 전문화**에 있다. 범용 인프라에 암호화 부담을 지우지 않고, 전용 하드웨어로 분리함으로써 네트워크 전체의 안정성과 예측 가능성이 높아진다.

제로 트러스트(Zero Trust) 아키텍처가 확산되면서 VPN 자체를 ZTNA(Zero Trust Network Access)로 대체하는 흐름도 있다. 그러나 레거시 애플리케이션 호환성, 규정 준수(Compliance) 요건, 내부 망 접근 제어 측면에서 IPsec/SSL VPN Concentrator는 당분간 기업 네트워크의 핵심 장비로 남는다.

HA·로드 밸런싱 구성을 통해 **가용성(Availability)** 과 **처리량(Throughput)** 을 동시에 확보하고, SIEM(Security Information and Event Management)과 연동한 실시간 로그 분석으로 이상 접근을 탐지하는 것이 현대적 운영 기준이다.

📢 **섹션 요약 비유**: VPN Concentrator는 수십 개의 전화를 동시에 받을 수 있는 콜센터 전용 교환기와 같다. 한 대로 모든 고객 전화를 처리하며, 교환기가 고장 나도 예비 교환기가 즉시 이어받는다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| IPsec (IP Security) | 프로토콜 | Concentrator가 처리하는 주요 터널 프로토콜 |
| IKEv2 (Internet Key Exchange v2) | 키 교환 | 터널 수립 시 인증·키 협상 담당 |
| SSL/TLS VPN | 프로토콜 | 웹 브라우저 기반 원격 접속 VPN |
| HA (High Availability) | 가용성 | 이중화 구성으로 단일 장애점 제거 |
| Split Tunneling | 트래픽 정책 | VPN 터널과 로컬 인터넷 경로 분리 |
| ZTNA (Zero Trust Network Access) | 대체 아키텍처 | 애플리케이션 단위 접근 제어로 VPN 대체 |
| RADIUS | 인증 연동 | 사용자 인증 중앙화 프로토콜 |

### 👶 어린이를 위한 3줄 비유 설명

1. VPN은 공개 도로에 투명한 보호 튜브를 씌워 비밀 편지를 안전하게 배달하는 것과 같아요.
2. VPN Concentrator는 그 튜브 입구를 수천 개 동시에 열고 닫는 전문 문지기 기계예요.
3. 문지기가 두 명 대기하다가 한 명이 쓰러지면 나머지 한 명이 바로 대신하니까 편지가 항상 안전하게 도착해요.
