+++
weight = 318
title = "318. ARP 캐시 오염 (ARP Cache Poisoning)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: ARP 캐시 오염(ARP Cache Poisoning)은 ARP (Address Resolution Protocol)의 인증 없는 설계를 악용해 가짜 MAC 주소를 네트워크 이웃에게 브로드캐스트하고, 피해자의 ARP 캐시(Cache) 테이블을 오염시켜 트래픽을 탈취하는 L2 계층 공격이다.
> 2. **가치**: 동일 L2 네트워크 내에서 암호화되지 않은 트래픽(HTTP, Telnet, FTP)을 실시간 도청하거나, HTTPS 세션도 SSLStrip 공격과 결합하면 탈취 가능하므로, 내부 네트워크 보안에서 핵심 방어 대상이다.
> 3. **판단 포인트**: DAI (Dynamic ARP Inspection)가 핵심 방어 기술이며, DHCP 스누핑(DHCP Snooping) 바인딩 테이블과 연동하여 IP-MAC 매핑 신뢰성을 검증하는 원리를 정확히 이해해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

ARP는 1982년 RFC 826으로 정의된 프로토콜로, IP 주소를 MAC (Media Access Control) 주소로 변환하는 L2/L3 경계 역할을 한다. 문제는 ARP가 "무신뢰(Stateless)" 설계라는 점이다. ARP Reply는 Request가 없어도 보낼 수 있으며(Gratuitous ARP), 수신 측은 이를 그대로 캐시에 저장한다. 인증이나 검증 메커니즘이 전혀 없다.

공격자는 이 취약점을 이용해 "나는 게이트웨이(192.168.1.1)이고, 내 MAC은 AA:BB:CC:DD:EE:FF야"라는 거짓 ARP Reply를 피해자들에게 지속적으로 보낸다. 피해자들은 이를 신뢰하고 ARP 캐시를 갱신하며, 이후 모든 외부 통신이 공격자를 경유하게 된다. 이것이 MITM (Man-in-the-Middle) 공격의 전형적인 L2 구현이다.

내부망 보안 사고에서 ARP 캐시 오염은 가장 빈번하게 활용되는 공격 기법 중 하나다. Ettercap, Arpspoof, Bettercap 같은 공개 도구로 클릭 몇 번이면 실행 가능하므로 기술 장벽이 낮다.

📢 **섹션 요약 비유**: ARP 캐시 오염은 동네 게시판에 "우체국 주소가 바뀌었어요, 이제 우리 집으로 편지 보내세요"라는 가짜 공지를 붙이는 것이다. 주민들이 이를 믿고 편지를 보내면 우편물이 모두 공격자 손에 들어간다.

---

## 2. 구성요소

### ARP 캐시 오염 공격 흐름

```
정상 상태:
  피해자 A (192.168.1.10) ──► 게이트웨이 (192.168.1.1, MAC: 00:11:22:33:44:55)
  피해자 B (192.168.1.20) ──► 게이트웨이 (192.168.1.1, MAC: 00:11:22:33:44:55)

공격 시작 (Gratuitous ARP 전송):
  공격자 → 피해자 A: "192.168.1.1 = AA:BB:CC:DD:EE:FF" (공격자 MAC)
  공격자 → 피해자 B: "192.168.1.10 = AA:BB:CC:DD:EE:FF" (공격자 MAC)
  공격자 → 게이트웨이: "192.168.1.10 = AA:BB:CC:DD:EE:FF"

공격 성공 후 (MITM 상태):
  피해자 A ──► 공격자 ──► 게이트웨이 (트래픽 도청)
  피해자 B ──► 공격자 ──► 피해자 A   (트래픽 도청)
```

### ARP 동작 원리와 취약점

```
┌──────────────────────────────────────────────┐
│  정상 ARP 흐름                               │
│                                              │
│  호스트 A: "192.168.1.1 MAC이 뭐야?" (Broadcast)│
│       │                                     │
│       ▼                                     │
│  게이트웨이: "내 MAC은 00:11:22:33:44:55야" │
│       │                                     │
│       ▼                                     │
│  호스트 A ARP 캐시: 192.168.1.1 → 00:11:... │
│                                              │
│  취약점: 응답 인증 없음 + Gratuitous ARP 수용│
│  → 공격자 무응답 요청 없이도 캐시 덮어쓰기 가능│
└──────────────────────────────────────────────┘
```

### 핵심 방어 기술 비교

| 방어 기술 | 동작 원리 | 적용 위치 | 특징 |
|:---|:---|:---:|:---|
| DAI (Dynamic ARP Inspection) | DHCP Snooping 테이블과 ARP 패킷 IP-MAC 비교 | 스위치 | 가장 강력한 방어 |
| 정적 ARP 항목 (Static ARP) | 수동으로 신뢰 IP-MAC 매핑 고정 | 호스트 | 소규모에서만 실용적 |
| IPSG (IP Source Guard) | 포트별 IP-MAC 트래픽 필터링 | 스위치 | DAI와 함께 사용 |
| 포트 보안 (Port Security) | 포트당 허용 MAC 수 제한 | 스위치 | MAC Flooding 방어 겸용 |
| ARP 모니터링 도구 | Arpwatch 등으로 MAC 변화 감지 | 서버/관리 | 탐지만 가능, 차단 불가 |

📢 **섹션 요약 비유**: DAI는 스위치에 경비원을 세우는 것이다. ARP 패킷이 들어올 때마다 "이 IP-MAC 쌍이 DHCP 장부에 있어?"를 확인하고, 없으면 바로 차단한다.

---

## 3. 구조 및 동작 원리

### DAI (Dynamic ARP Inspection) 동작 상세

| 단계 | 처리 내용 |
|:---|:---|
| DHCP Snooping 활성화 | 스위치가 DHCP 교환을 감청해 IP-MAC-포트 바인딩 테이블 구축 |
| Trusted 포트 설정 | 업링크 포트는 신뢰(Trusted)로 설정 → ARP 검사 생략 |
| Untrusted 포트 ARP 검사 | 모든 ARP 패킷의 IP-MAC 쌍을 바인딩 테이블과 비교 |
| 불일치 시 드롭 | 바인딩 테이블에 없는 IP-MAC 조합의 ARP는 차단 + 로그 |
| 정적 바인딩 추가 | DHCP 미사용 장비는 수동으로 IP-MAC 바인딩 등록 |

### 공격 연계 시나리오

```
ARP 캐시 오염
    │
    ├── MITM 트래픽 도청
    │   ├── HTTP → 평문 탈취
    │   ├── HTTPS + SSLStrip → 세션 쿠키 탈취
    │   └── DNS 응답 변조 (DNS Spoofing)
    │
    ├── DoS (Denial of Service)
    │   └── 잘못된 MAC 주소 → 패킷 블랙홀
    │
    └── 세션 하이재킹 (Session Hijacking)
        └── TCP 세션 탈취 → 인증 우회
```

📢 **섹션 요약 비유**: IPSG + DAI + 포트 보안은 세 겹의 검문소다. 포트 보안은 신분증 개수 제한, DHCP Snooping은 실제 주소 등록부, DAI는 등록부와 현재 신분증 대조다.

---

## 4. 비교 및 트레이드오프

### Cisco 스위치 DAI 설정 예시

```
! DHCP Snooping 활성화
ip dhcp snooping
ip dhcp snooping vlan 10,20,30

! DAI 활성화
ip arp inspection vlan 10,20,30

! 업링크 포트 Trusted 설정
interface GigabitEthernet0/1
  ip dhcp snooping trust
  ip arp inspection trust

! 엔드포인트 포트 Rate-Limit (DoS 방어)
interface GigabitEthernet0/2
  ip arp inspection limit rate 100

! 정적 ARP 바인딩 (DHCP 미사용 장비)
arp access-list STATIC_ARP
  permit ip host 192.168.1.100 mac host 00:50:56:AA:BB:CC
ip arp inspection filter STATIC_ARP vlan 10
```

### IPSG (IP Source Guard) 추가 설정

```
interface GigabitEthernet0/2
  ip verify source
! → 포트에서 수신된 패킷의 IP-MAC을 DHCP Snooping 테이블과 비교
!   불일치 패킷 전부 드롭
```

### 기술사 시험 판단 포인트

시험에서 ARP 캐시 오염 관련 문제는 주로 두 가지 형태다. 첫째, 공격 메커니즘 설명 → "Gratuitous ARP + 인증 부재"를 핵심으로 서술. 둘째, 방어 방안 논술 → DAI와 DHCP Snooping의 연계 동작, 신뢰/비신뢰 포트 구분을 도식과 함께 설명. "왜 DAI만으로는 부족하고 IPSG가 필요한가"를 계층적으로 설명하면 고득점이다.

📢 **섹션 요약 비유**: 기술사 답안에서 ARP 방어는 "누가 어디서 들어오는지 장부에 적고(DHCP Snooping), 들어오는 패킷과 장부를 대조하고(DAI), 모르는 패킷은 문 앞에서 차단(IPSG)"이라는 3단계 논리로 서술해야 한다.

---

## 5. 실무 적용 및 최적화 기법

DAI와 DHCP Snooping을 스위치 레벨에서 활성화하면, 내부 네트워크에서 발생하는 ARP 캐시 오염 공격의 대부분을 자동으로 차단할 수 있다. 공격자가 동일 L2 세그먼트에 물리적으로 접근했더라도, 트래픽 탈취가 불가능해진다.

포트 보안(Port Security)을 추가로 적용하면 MAC Flooding 공격도 방어하여 스위치가 허브(Hub)처럼 동작하는 상태를 막을 수 있다. 이들 설정은 스위치 CLI에서 수 분 내에 적용 가능하며, 별도 장비 구매 없이 기존 인프라에서 구현된다는 점에서 비용 효율이 높다.

장기적으로는 IPv6 환경으로의 전환과 함께 NDP (Neighbor Discovery Protocol) 기반 공격(NDPv6 Spoofing)으로 위협이 확장되므로, RA Guard (Router Advertisement Guard)와 IPv6 Source Guard도 병행 적용이 필요하다.

📢 **섹션 요약 비유**: ARP 방어 완료는 동네 우편함에 잠금장치를 달고, 집배원 명단을 확인하고, 모르는 배달부가 오면 경비에게 신고하는 체계를 갖춘 것이다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| ARP (Address Resolution Protocol) | 공격 대상 프로토콜 | IP → MAC 변환, RFC 826 |
| Gratuitous ARP | 공격 수단 | 요청 없이 보내는 ARP Reply |
| MITM (Man-in-the-Middle) | 공격 결과 | ARP 오염 후 트래픽 도청 |
| DAI (Dynamic ARP Inspection) | 핵심 방어 | DHCP Snooping 테이블 기반 ARP 검증 |
| DHCP Snooping | DAI 전제조건 | IP-MAC-포트 바인딩 테이블 구축 |
| IPSG (IP Source Guard) | 보완 방어 | 포트 단위 IP-MAC 필터링 |
| 포트 보안 (Port Security) | 추가 방어 | 포트당 허용 MAC 수 제한 |
| SSLStrip | 연계 공격 | ARP 오염 후 HTTPS를 HTTP로 다운그레이드 |

### 👶 어린이를 위한 3줄 비유 설명

- ARP 캐시 오염은 동네 게시판에 "우리 집이 우체국이야"라는 가짜 공지를 붙이는 거야.
- 주민들이 이를 믿으면 편지가 모두 공격자 집으로 가서 내용이 들켜버려.
- 방어는 스위치가 "진짜 우체국 주소 장부"를 갖고 있어서 가짜 공지를 바로 거부하는 거야.
