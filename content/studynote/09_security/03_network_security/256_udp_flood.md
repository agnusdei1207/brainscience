+++
weight = 256
title = "UDP 플러딩 (UDP Flood) 공격"
date = "2024-03-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> |   Victim    |

> 📝 모범 답안

1. **자원 고갈 공격**: 비연결성(Connectionless) 프로토콜인 UDP를 사용하여 위조된 출발지 IP로부터 대량의 패킷을 임의의 포트로 전송, 대역폭 및 호스트 자원을 고갈시키는 볼류메트릭 DDoS임.
2. **ICMP Unreachable 유발**: 존재하지 않는 포트로 UDP 패킷을 수신한 희생자 서버가 ICMP 에러 메시지를 응답하게 함으로써 서버 부하를 가중시킴.
3. **위조(Spoofing) 용이성**: TCP와 달리 3-Way Handshake가 없어 IP 위조가 매우 쉬우며, 이로 인해 근원지 추적이 어려운 특성을 지님.

### 1. 개요 및 필요성
- **개념**: 전송 계층(L4)에서 대량의 UDP 패킷을 임의의 포트로 쏟아부어 네트워크 장비(라우터, 방화벽)와 서버의 회선 및 CPU를 마비시키는 공격임.
- **배경**: 영상 스트리밍, 온라인 게임 등 실시간 서비스에 주로 사용되는 UDP의 특성(무상태성, 속도 우선)을 악용함.

### 2. 구성요소
#### 1. UDP Flood 공격 매커니즘
- **과정**: 공격자(Botnet) → 희생자 IP(Random Port 1~65535) → 희생자 서버의 처리 부하 발생.

```text
[ UDP Flood Attack Architecture ]
+-----------+    UDP Packets (e.g., 64 bytes)    +-------------+
|  Bot #1   | ---------------------------------+-----------+    [Dst Port: 12345 (Random)]      |   Server    |
                                                 +-------------+
+-----------+    UDP Packets (e.g., 64 bytes)           |
|  Bot #2   | --------------------------------->        |
+-----------+    [Dst Port: 54321 (Random)]             | 1. Listen check
                                                        | 2. No Service found
                                                        | 3. Send ICMP Error
                                                        V
                                                 +-------------+
                                                 | ICMP Dest   |
                                                 | Unreachable |
                                                 +-------------+
[ Overhead: Bandwidth + CPU for Port Check + ICMP Generation ]
```

#### 2. 기술적 특성
- **No Handshake**: 연결 설정 과정이 없어 즉각적인 공격 수행이 가능함.
- **포트 스캐닝 형태**: 특정 포트가 아닌 전체 포트를 무작위로 공격하여 특정 서비스 차단이 어려움.

### 3. 구조 및 동작 원리

| 비교 항목 | UDP Flood | SYN Flood | ICMP Flood |
| :--- | :--- | :--- | :--- |
| **계층** | L4 (UDP) | L4 (TCP) | L3 (ICMP) |
| **타겟 자원** | 대역폭, ICMP 생성 부하 | 서버 백로그 큐 (Backlog) | 대역폭, 처리 부하 |
| **공격 방식** | 비연결형 다량 전송 | 연결 반개방 (Half-open) | Echo Request 다량 전송 |
| **방어 기술** | Rate Limit, ACL | SYN Cookie, Proxy | ICMP 차단 (Rate Limit) |

### 4. 비교 및 트레이드오프
- **방응 전략**:
    1. **UDP 임계치 관리**: IDS/IPS 및 방화벽에서 단위 시간당 수신되는 UDP 패킷 수(PPS)를 제한.
    2. **불필요한 포트 차단**: 서버에서 사용하지 않는 모든 UDP 포트를 방화벽 수준에서 화이트리스트 방식으로 제어.
    3. **ICMP 응답 제한**: 서버 설정에서 "Destination Unreachable" 메시지 전송을 차단하거나 속도를 조절하여 리소스 소모 방지.
- **기술사적 판단**: 단순한 UDP Flood는 현대의 고성능 네트워크 장비로 일정 부분 방어가 가능하지만, **증폭 공격(DRDoS)**과 결합될 경우 단일 인프라로 막아내기 불가능한 수준에 이름. 따라서 ISP 수준의 스크러빙 센터(Scrubbing Center) 연동이 필수적임.

### 5. 실무 적용 및 최적화 기법
- **기대효과**: 네트워크 가용성을 확보하고 실시간 서비스의 무중단 운영을 보장함.
- **결론**: UDP는 네트워크 효율성을 위해 탄생했지만, 보안적 측면에서는 '무책임한 전송'이 될 수 있음. 따라서 서비스 설계 시 UDP를 사용한다면 반드시 하위 인프라에서 강력한 ACL과 모니터링 체계를 갖추어야 함.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: DDoS, Volumetric Attack
- **하위 개념**: Fraggle Attack, DNS/NTP Amplification
- **대응 도구**: Arbor Networks, F5 Silverline

### 👶 어린이를 위한 3줄 비유 설명
1. 누군가 벨을 누르고 도망가는 장난을 1초에 수천 번씩 하는 것과 같아요.
2. 집주인은 누가 왔는지 확인하러 현관문까지 계속 왔다 갔다 하느라 너무 힘들어서 다른 일을 아무것도 못 하게 돼요.
3. 결국 너무 많은 가짜 벨 소리 때문에 진짜 손님이 와도 문을 열어줄 수가 없게 되는 거죠.
