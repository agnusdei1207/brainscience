+++
weight = 261
title = "261. ARP Spoofing — MAC 주소 위조"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: ARP (Address Resolution Protocol) 스푸핑은 가짜 ARP 응답을 주입해 피해자의 ARP 캐시를 오염시키고, 트래픽을 공격자 MAC (Media Access Control) 주소로 우회시키는 L2 (Layer 2) 중간자 공격이다.
> 2. **가치**: ARP는 인증이 없는 프로토콜이므로 동일 L2 세그먼트에 접근 가능한 공격자가 네트워크를 무음 도청(Passive Sniffing)하거나 세션을 탈취할 수 있다.
> 3. **판단 포인트**: Dynamic ARP Inspection (DAI)과 DHCP Snooping 바인딩 테이블의 결합이 실무 핵심 방어책이며, 스태틱 ARP 항목은 소규모 환경의 임시 방편이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

ARP (Address Resolution Protocol)는 IP 주소를 MAC 주소로 변환하는 L2 프로토콜로, RFC 826에 정의되어 있다. 설계 당시 보안 개념이 없었기 때문에 수신한 ARP 응답의 신뢰성을 검증하는 메커니즘이 존재하지 않는다. 모든 호스트는 자신이 요청하지 않은 ARP 응답(Gratuitous ARP 또는 unsolicited ARP reply)도 수신하면 캐시에 저장한다.

이 취약점을 이용하면 동일 브로드캐스트 도메인 내의 공격자가 "나는 게이트웨이 IP(192.168.1.1)의 MAC 주소다"라는 허위 ARP 응답을 지속적으로 전송해, 피해자 호스트가 게이트웨이로 향하는 모든 트래픽을 공격자에게 보내도록 유도할 수 있다.

기업 내부망, 공용 Wi-Fi, 클라우드 가상 네트워크(VPC, Virtual Private Cloud) 등 동일 서브넷 환경 어디에서나 이 공격이 가능하다. SSL/TLS 암호화가 없는 통신은 도청당하고, HTTPS도 SSL 스트리핑(SSL Stripping) 공격과 결합하면 평문으로 노출될 수 있다.

📢 **섹션 요약 비유**: "저 우체통이 네 것이다"고 계속 외치면 마을 사람들이 그 우체통이 진짜인 줄 알고 편지를 넣는 것처럼, ARP 스푸핑은 MAC 주소 주민등록을 위조한다.

---

## 2. 구성요소

### 공격 흐름

```
[정상 통신 전]
  피해자(Victim)                  게이트웨이(GW)
  IP: 192.168.1.10                IP: 192.168.1.1
  MAC: AA:AA:AA:AA:AA:AA          MAC: GG:GG:GG:GG:GG:GG

[공격자 ARP 위조 주입]
  공격자(Attacker)
  IP: 192.168.1.99
  MAC: EE:EE:EE:EE:EE:EE

  공격자 → 피해자: "192.168.1.1의 MAC은 EE:EE:EE:EE:EE:EE 입니다"
  공격자 → GW:    "192.168.1.10의 MAC은 EE:EE:EE:EE:EE:EE 입니다"

[ARP 캐시 오염 후]
  피해자 ARP 캐시:
    192.168.1.1  →  EE:EE:EE:EE:EE:EE  ← 잘못된 항목!

[트래픽 흐름 변경]
  피해자 ──▶ 공격자(도청/변조) ──▶ 게이트웨이
          ◀──────────────────── ◀──

  ※ 공격자가 패킷을 포워딩하면 피해자는 통신 이상을 눈치채지 못함
```

### 핵심 구성 요소

| 요소 | 설명 |
|:---|:---|
| ARP Request | "이 IP의 MAC은?" 브로드캐스트 질의 |
| ARP Reply | "그 IP의 MAC은 나야" 유니캐스트 응답 |
| ARP Cache | 호스트가 IP↔MAC 매핑을 임시 저장하는 테이블 (TTL 수 분) |
| Unsolicited ARP Reply | 요청 없이 전송된 ARP 응답. 대부분 호스트가 그대로 캐시에 저장 |
| Gratuitous ARP | 자신의 IP에 대한 ARP 요청/응답. 정상 사용도 있지만 스푸핑에 악용 |

### 공격 파급 효과

- **도청 (Sniffing)**: 암호화되지 않은 HTTP, FTP, Telnet 세션 내용 획득
- **세션 하이재킹**: TCP 시퀀스 번호 탈취 후 세션 탈취
- **SSL 스트리핑**: HTTPS를 HTTP로 다운그레이드시켜 평문 노출
- **DNS 스푸핑 연계**: DNS 응답 조작으로 피싱 사이트로 유도

📢 **섹션 요약 비유**: 공격자는 교차로에서 표지판을 몰래 바꿔 모든 차량이 자신의 차고를 거쳐 가도록 만드는 것이다.

---

## 3. 구조 및 동작 원리

| 방어 기술 | 원리 | 특징 |
|:---|:---|:---|
| Dynamic ARP Inspection (DAI) | DHCP Snooping 테이블 기반 ARP 패킷 검증 | 스위치 레이어에서 차단. 가장 효과적 |
| Static ARP Entry | 관리자가 IP↔MAC 수동 고정 | 소규모 환경에서만 현실적. 확장성 없음 |
| ARP Watch / 모니터링 | ARP 캐시 변동 탐지 알림 | 탐지는 가능하나 차단 불가 |
| 802.1X 포트 인증 | 포트 접속 자체를 인증 | 비인가 기기 접속 원천 차단 |
| VPN / IPSec | L3 암호화로 도청 무력화 | 스푸핑은 발생해도 내용 노출 없음 |

📢 **섹션 요약 비유**: DAI는 입구에서 주민등록증 확인, Static ARP는 방문자 명단 수기 관리, VPN은 모든 대화를 암호화한 밀봉 편지로 보내는 것이다.

---

## 4. 비교 및 트레이드오프

**DAI (Dynamic ARP Inspection) 설정 절차**:

1. 먼저 DHCP Snooping을 활성화하여 IP↔MAC↔포트 바인딩 테이블을 생성한다.
2. 신뢰 포트(Trusted Port, 업링크·DHCP 서버 연결 포트)를 제외한 모든 포트에 DAI를 적용한다.
3. 스위치는 ARP 패킷의 IP·MAC이 바인딩 테이블과 일치하는지 확인하고, 불일치 시 폐기한다.

```
! Cisco 스위치 설정 예시
ip dhcp snooping
ip dhcp snooping vlan 10
!
ip arp inspection vlan 10
!
interface GigabitEthernet0/1
  ip dhcp snooping trust        ! 업링크: 신뢰 포트
  ip arp inspection trust
!
interface GigabitEthernet0/2
  ! 일반 액세스 포트: 기본적으로 untrusted
```

**탐지 방법**:
- `arp -a` 명령으로 ARP 캐시 확인. 서로 다른 IP가 같은 MAC으로 매핑되어 있으면 스푸핑 의심.
- Wireshark 등으로 동일 MAC에서 오는 다중 IP ARP 응답 감지.
- 네트워크 모니터링 솔루션(예: XDR, NDR)의 ARP 이상 탐지 알림 활성화.

**기술사 시험 포인트**:
- "ARP 스푸핑 공격 과정과 방어 방법을 설명하라"는 빈출 문제다.
- DAI와 DHCP Snooping의 연계 관계를 반드시 설명해야 한다.
- Gratuitous ARP와의 차이점(정상 사용 vs 악용)도 서술 포인트다.

📢 **섹션 요약 비유**: 스위치가 "이 방에 들어오려면 사전에 등록된 얼굴과 이름이 일치해야 한다"고 문을 지키는 것이 DAI다.

---

## 5. 실무 적용 및 최적화 기법

ARP 스푸핑은 기술적으로 단순하지만 내부망 보안에 치명적인 위협이다. DHCP Snooping + DAI 조합을 스위치 인프라에 적용하면 이 공격을 L2에서 원천 차단할 수 있다.

클라우드 환경(AWS VPC, Azure VNet)에서는 클라우드 공급자가 소프트웨어 정의 네트워크(SDN, Software Defined Networking) 수준에서 ARP 검증을 제공하므로 기본적으로 ARP 스푸핑이 방지된다. 그러나 온프레미스 환경이나 사설 클라우드에서는 여전히 수동 설정이 필요하다.

제로 트러스트(Zero Trust) 아키텍처에서는 L2 신뢰를 배제하고 모든 통신을 mTLS (mutual Transport Layer Security)로 암호화해 ARP 스푸핑의 영향을 무력화하는 방향으로 발전하고 있다.

📢 **섹션 요약 비유**: 마을 우체국이 디지털화되어 모든 편지가 암호화·봉인되면, 편지 경로를 바꿔도 내용을 읽을 수 없는 것처럼, 암호화와 DAI를 함께 쓰면 ARP 스푸핑은 의미를 잃는다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| ARP (RFC 826) | 취약 프로토콜 | 인증 없는 L2 주소 변환 |
| Gratuitous ARP | 연관 개념 | 정상/악용 이중성 있는 ARP 변형 |
| DHCP Snooping | 방어 전제 | DAI의 바인딩 테이블 제공 |
| DAI | 핵심 방어 | 스위치 레이어 ARP 검증 |
| SSL Stripping | 연계 공격 | ARP 스푸핑 후 HTTPS 다운그레이드 |
| 802.1X | 보완 방어 | 포트 인증으로 비인가 기기 차단 |

### 👶 어린이를 위한 3줄 비유 설명
- ARP 스푸핑은 학교 게시판에 "우리 반 반장 전화번호는 내 번호야"라고 몰래 공고를 붙이는 것이다.
- 그러면 친구들이 반장에게 할 말을 모두 공격자에게 하게 된다.
- 선생님(스위치)이 게시판 공고를 학생 명부와 대조 확인하면(DAI) 가짜 공고를 바로 떼어낼 수 있다.
