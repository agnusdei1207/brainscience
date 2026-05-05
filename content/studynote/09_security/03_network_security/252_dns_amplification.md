+++
weight = 252
title = "DNS Amplification (DNS 증폭 공격)"
date = "2026-03-25"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> Response (3000+ Bytes) = 50x Amplification!

> 📝 모범 답안

- UDP 프로토콜의 비연결성과 IP 스푸핑을 악용하여, 작은 질의로 거대한 응답을 유발해 타겟을 마비시키는 반사 공격임
- 개방형 리졸버(Open Resolver)를 반사체로 활용하여 수십 배에서 수백 배의 트래픽 증폭 효과를 달성함
- 'ANY' 타입 질의나 DNSSEC 확장 레코드를 요청함으로써 응답 패킷의 크기를 극대화함

### 1. 개요 및 필요성
DNS Amplification 공격은 볼류메트릭(Volumetric) DDoS 공격의 대표적인 유형이다. 공격자가 직접 트래픽을 쏘는 것이 아니라, 전 세계에 널려 있는 취약한 DNS 서버들을 "증폭기"로 활용하기 때문에 공격 원점을 파악하기 어렵고 방어가 까다롭다.

### 2. 구성요소
```text
[DNS Amplification Attack - Reflection & Amplification]

1. Attacker (Spoofed IP = Victim's IP)
      |
      | (Small Query: EDNS0, Type=ANY)
      V
2. Open DNS Resolver (Reflector)
      |
      | (Large Response: several KB)
      V
3. Victim's Server (Target) <--- Traffic Flood!

[Amplification Factor]
Query (60 Bytes) -```
- **IP Spoofing:** UDP는 핸드셰이크가 없으므로 출발지 IP를 희생자의 IP로 위조하여 전송하면, DNS 서버는 응답을 희생자에게 보냄
- **EDNS0:** 현대 DNS 확장 프로토콜을 사용하여 512바이트 이상의 큰 패킷을 생성하도록 유도함

### 3. 구조 및 동작 원리
| 공격 유형 | 증폭 매커니즘 | 반사체 (Reflector) |
| :--- | :--- | :--- |
| **DNS Amp** | DNS 리소스 레코드 (ANY, DNSSEC) | Open Resolver (Recursive DNS) |
| NTP Amp | 'monlist' 명령어 (최근 600개 IP 목록) | NTP Server |
| Memcached Amp | Get 요청 (대량의 데이터 저장 후 조회) | Memcached Server (UDP 11211) |
| SSDP Amp | M-SEARCH 요청 | IoT 장비 (UPnP) |

### 4. 비교 및 트레이드오프
- **실무 적용:** DNS 운영자는 `recursion no` 설정을 통해 자신의 서버가 Open Resolver가 되지 않도록 차단해야 하며, ISP는 BCP38(출발지 IP 검증)을 적용하여 스푸핑 패킷 유출을 막아야 함
- **기술사적 판단:** 공격 탐지 시 증폭 공격에 사용되는 특정 질의 패턴(ANY 타입 등)을 식별하여 임계값 기반의 Rate Limiting이나 차단 정책을 에지 단에서 수행해야 함

### 5. 실무 적용 및 최적화 기법
- **기대효과:** 인프라 보호를 통해 대규모 트래픽 유입 시에도 전체 네트워크 서비스의 가용성을 유지할 수 있음
- **결론:** DNS 증폭 공격은 인터넷 거버넌스 차원의 협력이 필요한 문제로, 전 세계적인 Open Resolver 제거와 함께 DNS 프로토콜의 보안 강화가 지속적으로 요구됨

### 📌 관련 개념 맵 (Knowledge Graph)
- DDoS → Reflection Attack → Amplification Attack
- DNS → UDP → IP Spoofing
- 방어 → BCP38 → Response Rate Limiting (RRL)

### 👶 어린이를 위한 3줄 비유 설명
- 나쁜 장난꾸러기가 자기 주소 대신 친구 주소를 적어서 피자집에 "메뉴 전부 다 알려주세요!"라고 편지를 보내요.
- 피자집은 큰 메뉴판 뭉치를 친구네 집으로 배달해 버려요.
- 이런 편지를 수천 군데에 보내면 친구네 집 앞은 순식간에 메뉴판 더미로 꽉 막혀버린답니다!
