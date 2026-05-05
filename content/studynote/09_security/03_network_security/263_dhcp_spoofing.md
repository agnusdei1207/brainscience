+++
weight = 263
title = "263. DHCP Spoofing — DHCP 서버 사칭"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: DHCP Spoofing (DHCP 스푸핑)은 공격자가 가짜 DHCP (Dynamic Host Configuration Protocol) 서버를 띄워 클라이언트에게 기본 게이트웨이·DNS (Domain Name System) 서버를 조작된 값으로 배포하는 L2 중간자 공격이다.
> 2. **가치**: 클라이언트가 올바른 게이트웨이를 모르면 모든 외부 트래픽이 공격자를 통과하므로, DHCP 스푸핑 하나로 전체 네트워크 트래픽의 도청·변조가 가능해진다.
> 3. **판단 포인트**: DHCP Snooping을 스위치에 활성화해 신뢰 포트(Trusted Port)에서만 DHCP 응답이 통과되도록 설정하는 것이 가장 효과적인 방어다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

DHCP는 클라이언트가 네트워크에 연결될 때 IP 주소, 서브넷 마스크, 기본 게이트웨이, DNS 서버 등을 자동으로 할당받는 프로토콜(RFC 2131)이다. 표준 DHCP는 서버 인증 메커니즘이 없으므로, 클라이언트는 가장 먼저 응답한 DHCP 서버의 정보를 신뢰한다.

공격자가 합법 서버보다 빠르게 DHCP Offer를 전송하면, 클라이언트는 기본 게이트웨이로 공격자의 IP를 설정하게 된다. 이후 모든 외부 통신 트래픽이 공격자를 경유하는 중간자(Man-in-the-Middle, MitM) 상태가 만들어진다.

기업 내부망, 캠퍼스 네트워크, 공용 Wi-Fi에서 특히 위험하다. 스마트폰·노트북 등 DHCP를 기본으로 사용하는 장치가 대상이며, 사용자는 이 공격을 전혀 눈치채지 못한다.

📢 **섹션 요약 비유**: 새 도시로 이사한 사람이 주소를 물어볼 때, 진짜 안내소(DHCP 서버)보다 빨리 "저기로 가세요"라고 잘못된 방향을 알려주는 사기꾼이 DHCP 스푸핑 공격자다.

---

## 2. 구성요소

### DHCP 4단계 핸드셰이크 (DORA)

| 단계 | 메시지 | 방향 | 내용 |
|:---|:---|:---|:---|
| Discover | DHCP Discover | 클라이언트 → 브로드캐스트 | IP 주소 요청 |
| Offer | DHCP Offer | DHCP 서버 → 클라이언트 | IP·게이트웨이·DNS 제안 |
| Request | DHCP Request | 클라이언트 → 브로드캐스트 | 특정 서버 선택 확인 |
| Acknowledge | DHCP ACK | DHCP 서버 → 클라이언트 | IP 할당 확정 |

### 공격 흐름 다이어그램

```
[정상 시나리오]
  클라이언트                합법 DHCP 서버
      │── DHCP Discover ──▶│
      │◀── DHCP Offer ─────│  GW: 192.168.1.1, DNS: 8.8.8.8
      │── DHCP Request ───▶│
      │◀── DHCP ACK ───────│
      │
      └─▶ GW: 192.168.1.1 (올바른 게이트웨이)

[DHCP 스푸핑 공격]
  클라이언트    공격자(Rogue DHCP)    합법 DHCP 서버
      │─ Discover ─▶│                │
      │◀─ Offer ────│ (더 빠르게!)   │
      │  GW: 192.168.1.99 (공격자 IP)│
      │  DNS: 1.2.3.4 (악성 DNS)     │
      │─ Request ──▶│                │
      │◀─ ACK ──────│                │
      │
      └─▶ GW: 192.168.1.99 (공격자!)
           ↓
  모든 외부 트래픽이 공격자를 경유
  공격자 ──▶ 합법 게이트웨이 포워딩 (투명 프록시)
           ↓
  도청 / 변조 / 피싱 사이트 유도
```

### DHCP Snooping 방어 원리

DHCP Snooping은 스위치가 각 포트에서 수신한 DHCP 메시지를 필터링하는 기능이다. 관리자가 지정한 신뢰 포트(합법 DHCP 서버 연결 포트, 업링크)에서만 DHCP Offer·ACK가 통과된다. 비신뢰 포트에서 오는 DHCP Offer·ACK는 즉시 폐기된다.

또한 DHCP Snooping은 클라이언트 IP↔MAC↔포트 바인딩 테이블을 생성해 DAI (Dynamic ARP Inspection)의 기반 데이터로 제공한다.

📢 **섹션 요약 비유**: 학교에서 급식 신청서는 학교 행정실(신뢰 포트)에서만 받고, 아무 학생(비신뢰 포트)이 내민 신청서는 무효 처리하는 것이 DHCP Snooping이다.

---

## 3. 구조 및 동작 원리

| 방어 기술 | 동작 레이어 | 주요 기능 | 한계 |
|:---|:---|:---|:---|
| DHCP Snooping | L2 스위치 | Rogue DHCP 서버 차단, 바인딩 테이블 생성 | 스위치별 설정 필요 |
| 802.1X 포트 인증 | L2 | 비인가 기기 접속 원천 차단 | 구축 복잡도 높음 |
| 정적 IP 할당 | IP 관리 | DHCP 의존 제거 | 관리 부담 높음 |
| IPAM (IP Address Management) | 관리 | IP 할당 현황 가시성 | 탐지 후 대응, 사전 예방 아님 |

📢 **섹션 요약 비유**: DHCP Snooping은 정문 경비원, 802.1X는 신분증 없이는 건물에 아예 못 들어오게 하는 출입 통제 시스템이다. 두 가지를 함께 쓰면 훨씬 안전하다.

---

## 4. 비교 및 트레이드오프

**DHCP Snooping 설정 절차 (Cisco IOS)**:
```
ip dhcp snooping
ip dhcp snooping vlan 10,20          ! 보호할 VLAN 지정

interface GigabitEthernet0/1         ! 합법 DHCP 서버 연결 포트
  ip dhcp snooping trust             ! 신뢰 포트: Offer/ACK 통과

interface GigabitEthernet0/2         ! 클라이언트 포트
  ip dhcp snooping limit rate 15     ! 초당 DHCP 패킷 제한 (DoS 방지)
  ! 기본값: untrusted (Offer/ACK 차단)
```

**추가 방어 고려사항**:
- **DHCP Rate Limiting**: 클라이언트 포트에서 초당 DHCP 패킷 수를 제한해 DHCP Starvation (IP 풀 고갈) 공격도 방어.
- **Option 82 (DHCP Relay Agent Information)**: 릴레이 에이전트가 클라이언트의 스위치 포트 정보를 DHCP 요청에 추가해 중앙 서버가 포트 기반 정책을 적용 가능.
- **DHCPv6 Guard**: IPv6 환경의 동등한 보호 기능.

**탐지 방법**:
- 동일 서브넷에 DHCP 서버가 2개 이상 응답하면 Rogue DHCP 의심.
- `show ip dhcp snooping statistics`로 차단된 패킷 확인.
- 네트워크 모니터링 도구로 비신뢰 포트의 DHCP Offer 발생 알림 설정.

**기술사 시험 포인트**:
- "DHCP 스푸핑 공격 원리와 DHCP Snooping 방어를 설명하라"는 단골 문제다.
- DORA 4단계를 명시하고 어느 단계에서 공격이 개입하는지 설명해야 한다.
- DHCP Snooping이 DAI의 전제 조건임을 연결해서 서술하면 가점이다.

📢 **섹션 요약 비유**: 음식 배달 앱에서 검증된 식당(신뢰 포트)만 주문받을 수 있고, 가짜 식당(비신뢰 포트)은 주문을 받을 수 없도록 플랫폼이 통제하는 것이 DHCP Snooping이다.

---

## 5. 실무 적용 및 최적화 기법

DHCP Snooping은 구성이 간단하면서 DHCP 스푸핑, DHCP Starvation, ARP 스푸핑(DAI 연계)까지 방어하는 다목적 보안 기능이다. 모든 관리형 스위치에서 지원하며, 추가 하드웨어 비용 없이 활성화할 수 있다.

클라우드 환경에서는 VPC 서브넷 내 인스턴스에 DHCP 옵션 세트(DHCP Option Set)를 고정 배포함으로써 Rogue DHCP 가능성을 원천 차단한다. 온프레미스에서는 DHCP Snooping + 802.1X + DAI 3중 방어가 내부망 L2 공격의 사실상 표준 방어 아키텍처다.

📢 **섹션 요약 비유**: 도시 가스 계량기 설치는 자격증 있는 기사(신뢰 포트)만 할 수 있고, 무자격자(비신뢰 포트)는 접근 불가. 규칙 하나로 사고를 예방한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DHCP (RFC 2131) | 취약 프로토콜 | 인증 없는 IP 자동 할당 |
| Rogue DHCP | 공격 수단 | 가짜 DHCP 서버 |
| DHCP Snooping | 핵심 방어 | 스위치 포트 기반 DHCP 필터링 |
| DAI | 연계 방어 | DHCP Snooping 테이블 활용 ARP 검증 |
| DHCP Starvation | 연관 공격 | IP 풀 고갈을 통한 DoS |
| 802.1X | 보완 방어 | 포트 인증으로 비인가 기기 차단 |
| Option 82 | 고급 기능 | 릴레이 에이전트 정보 삽입 |

### 👶 어린이를 위한 3줄 비유 설명
- DHCP는 새 학생에게 "네 자리는 3번 책상"이라고 안내해주는 선생님이다.
- 가짜 선생님(공격자)이 먼저 "네 자리는 내 옆 자리"라고 하면 학생은 그리로 간다.
- DHCP Snooping은 선생님 자격증이 있는 사람만 자리 안내를 할 수 있도록 규칙을 만든 것이다.
