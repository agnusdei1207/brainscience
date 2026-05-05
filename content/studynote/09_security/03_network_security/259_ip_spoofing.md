+++
title = "IP Spoofing"
date = "2025-05-15"
weight = 259
[extra]
categories = ["security", "network-security"]
+++
## 0. 핵심 인사이트

> YES (If ACL checks IP only)

> 📝 모범 답안

- **신원 위조**: 패킷의 출발지 IP 주소를 신뢰할 수 있는 다른 IP나 존재하지 않는 IP로 위조하여 전송하는 공격 기법임.
- **인증 우회 및 은닉**: IP 주소 기반의 접근 제어(ACL)를 무력화하거나, 공격자의 실제 위치를 숨기기 위해 사용됨.
- **반사 공격의 기반**: DNS/NTP 증폭 공격 시 응답 패킷이 피해자에게 가도록 유도하는 DDoS의 핵심 구성 요소임.

### 1. 개요 및 필요성
IP Spoofing은 네트워크 통신의 기본 단위인 IP 패킷 헤더를 조작하는 전통적이고 강력한 공격이다. 인터넷 프로토콜(IP) 자체가 설계 당시 출발지 주소의 진위 여부를 검증하는 메커니즘이 부족하다는 점을 악용한다. 이는 단순한 도청을 넘어, 다른 시스템을 사칭하여 악성 데이터를 주입하거나 대규모 반사 공격을 실행하는 용도로 쓰인다.

### 2. 구성요소
공격자는 로우 소켓(Raw Socket) 등을 사용하여 패킷을 직접 구성하며, 헤더의 `Source IP Address` 필드에 임의의 값을 넣는다.

```text
[ IP Spoofing Architecture - IP 스푸핑 아키텍처 ]

   [ Attacker (Real IP: 1.1.1.1) ]
        |
        | (Forged Packet)
        | [ Src: 10.0.0.5 (Trusted) | Dst: 10.0.0.100 | Data: ... ]
        v
   [ Router / Firewall ]
        |
        |---- (Is 10.0.0.5 Allowed?) ----        v
   [ Victim Server (10.0.0.100) ]
        |
        +-- Processing request from "Trusted" 10.0.0.5
```

**주요 활용 사례:**
1. **세션 하이재킹**: 신뢰받는 호스트인 척하며 TCP 연결에 끼어들어 데이터를 탈취함.
2. **DDoS 반사 (Reflection)**: 출발지 IP를 피해자 IP로 위조하여 DNS 서버 등에 쿼리를 보내면, 증폭된 응답이 피해자에게 쏟아짐.
3. **인증 우회**: 유닉스 기반 시스템의 `rlogin`, `rsh` 등 IP 기반 신뢰 관계를 이용하는 서비스 공격.

### 3. 구조 및 동작 원리
| 비교 항목 | IP Spoofing | ARP Spoofing |
| :--- | :--- | :--- |
| **계층** | Layer 3 (Network Layer) | Layer 2 (Data Link Layer) |
| **범위** | 인터넷 전체 (라우팅 가능 시) | 로컬 네트워크 (LAN) 내부 |
| **공격 수단** | IP 헤더 주소 조작 | ARP 응답 패킷 위조 |
| **방어 기술** | Ingress/Egress Filtering, uRPF | Static ARP, DHCP Snooping |

### 4. 비교 및 트레이드오프
- **uRPF (Unicast Reverse Path Forwarding)**: 패킷이 들어온 인터페이스가 해당 출발지 IP로 돌아가는 경로와 일치하는지 확인하여 차단한다.
- **기술사적 판단**: ISP 레벨에서는 **BCP 38 (RFC 2827)** 가이드를 준수하여 자사 네트워크 외부로 나가는 패킷의 출발지 주소가 자사 대역이 아닐 경우 즉시 폐기해야 한다. 이는 전 지구적 DDoS 위협을 줄이는 가장 근본적인 사회적 합의이다.

### 5. 실무 적용 및 최적화 기법
IP Spoofing은 IPv6 환경에서도 헤더 구조상 여전히 유효한 위협이다. 따라서 IP 주소 자체를 '신분증'으로 신뢰하는 설계 철학에서 벗어나, 암호학적 인증(IPsec, TLS)을 결합한 제로 트러스트 보안 모델로의 전환이 필연적이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위**: 네트워크 보안, 신원 위조 공격
- **하위**: Blind Spoofing, Non-Blind Spoofing
- **연관**: BCP 38, uRPF, 증폭 DDoS 공격, TCP Sequence Prediction

### 👶 어린이를 위한 3줄 비유 설명
1. 친구에게 장난 편지를 보낼 때, 편지 봉투 뒷면의 '보내는 사람' 이름을 내가 아닌 선생님 이름으로 적는 거예요.
2. 편지를 받은 친구는 선생님이 보낸 줄 알고 깜짝 놀라겠죠?
3. 이렇게 남의 이름을 빌려서 가짜 편지를 보내는 것이 바로 IP 스푸핑이랍니다.
