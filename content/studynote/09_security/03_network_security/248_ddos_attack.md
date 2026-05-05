+++
title = "DDoS 공격 (Distributed Denial of Service)"
weight = 248
date = "2024-03-21"
[extra]
categories = ["Security", "Network"]
+++
## 0. 핵심 인사이트

> (C&C Server)

> 📝 모범 답안

- **가용성 파괴 공격**: 다수의 감염된 호스트(Zombie PC/Botnet)를 동원하여 타겟 시스템의 자원이나 대역폭을 고의적으로 고갈시켜 서비스를 마비시키는 공격임.
- **공격 양상의 지능화**: 단순 패킷 폭주에서 나아가 정상적인 애플리케이션 프로토콜을 모방하거나 암호화된 트래픽(HTTPS) 속에 숨어 탐지를 회피하는 형태로 진화함.
- **심층 방어 전략**: 단일 장비 대응보다는 ISP 클린존, 스크러빙 센터, CDN 분산 방어 등을 결합한 계층적 방어 체계 구축이 필수적임.

### 1. 개요 및 필요성
- **정의**: 분산된 다수의 공격 소스를 활용하여 대상 서버, 서비스 또는 네트워크 인프라에 감당할 수 없는 수준의 부하를 주어 정상적인 사용자 접근을 차단하는 행위임.
- **배경**: 해킹 툴의 대중화와 IoT 기기의 보안 취약성을 이용한 봇넷 구성이 용이해지면서 대규모(Tbps급) 공격이 빈번하게 발생하고 있음.
- **영향**: 기업 신뢰도 하락, 직접적인 매출 손실, 금융권의 경우 국가 경제 인프라 마비 등 막대한 유무형의 피해를 초래함.

### 2. 구성요소
```text
[ DDoS Attack Architecture: Botnet & C&C ]

   (Attacker) --[Command]--                                |
             +------------------+------------------+
             |                  |                  |
        (Bot/Zombie)       (Bot/Zombie)       (Bot/Zombie)
             |                  |                  |
             +------------------+------------------+
                                |
                      [ Flood of Packets ]
                                v
                         (Target Server)
                      [ Resource Exhaustion ]

[ 3 Main Categories of Attack ]
1. Volumetric: Bandwidth saturation (UDP Flood, Amplification)
2. Protocol: Protocol stack exploitation (SYN Flood, Ping of Death)
3. Application: Application layer logic (HTTP Flood, Slowloris)
```
- **Volumetric Attack (대역폭 점유)**: 대량의 트래픽을 전송하여 네트워크 대역폭을 포화시킴. 증폭 공격(NTP, DNS)이 대표적임.
- **Protocol Attack (자원 고갈)**: TCP/IP 스택의 약점을 이용하여 커넥션 테이블이나 시스템 자원을 점유함.
- **Application Attack (웹/앱 부하)**: 정상적인 HTTP 요청처럼 보이지만 서버 내부의 DB 쿼리나 고비용 연산을 유발하여 서버를 마비시킴.

### 3. 구조 및 동작 원리

| 공격 유형 | 주요 기법 | 대응 레이어 | 핵심 방어 기법 |
| :--- | :--- | :--- | :--- |
| **Volumetric** | UDP/ICMP Flood, Reflection | L3/L4 (ISP단) | Anycast, Rate Limiting, ACL |
| **Protocol** | SYN Flood, IP Fragments | L4 (IPS/Firewall) | SYN Cookie, TCP Reset |
| **Application** | HTTP Get/Post Flood, Slowloris | L7 (WAF) | Captcha, JS Challenge, URI 필터링 |
| **Combined** | Multi-vector Attacks | Full Stack | 지능형 통합 관제 (SIEM/SOAR) |

### 4. 비교 및 트레이드오프
- **인프라 이중화**: Anycast 기반의 DNS 배치를 통해 특정 지점의 부하를 전 세계로 분산시켜 공격 탄력성(Resilience)을 확보해야 함.
- **클라우드 활용**: 대규모 볼류메트릭 공격에 대응하기 위해 무한 확장이 가능한 클라우드 보안 서비스(Cloud WAF, Scrubbing Center) 연동이 필수적임.
- **기술사적 판단**: 단순 차단 위주의 정책은 오탐(False Positive)으로 인한 정상 고객 이탈을 초래하므로, 트래픽 프로파일링과 평판 기반 분석(IP Reputation)을 병행해야 함.

### 5. 실무 적용 및 최적화 기법
- **제로 트러스트 연계**: 모든 트래픽을 잠재적 위협으로 간주하고 지속적으로 검증하는 제로 트러스트 아키텍처가 DDoS 방어의 차세대 표준으로 부상함.
- **AI/ML 기반 탐지**: 고도화된 봇 트래픽을 구분하기 위해 머신러닝 기반의 이상 징후 탐지 알고리즘이 보안 장비에 탑재되어 실시간 대응력을 높임.
- **결론**: DDoS 방어는 기술적 도구를 넘어 비즈니스 연속성 계획(BCP)의 핵심 요소이며, 국가 및 기관 간의 위협 정보 공유(C-TAS 등)를 통한 협력적 대응이 핵심임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **Botnet**: 공격의 근원
- **Scrubbing Center**: 전문 방어 시설
- **CDN (Content Delivery Network)**: 분산 방어 수단
- **SYN Cookie**: 프로토콜 레벨 방어 기술

### 👶 어린이를 위한 3줄 비유 설명
1. 나쁜 악당이 수만 명의 가짜 손님을 식당에 보내서 자리를 다 차지하게 만들었어요.
2. 진짜 배고픈 손님들이 식당에 들어갈 수가 없게 된 상황이 바로 DDoS 공격이에요.
3. 식당 주인은 가짜 손님을 골라내는 탐정과 입구를 넓혀주는 도우미를 불러서 해결해야 해요!
