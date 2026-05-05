+++
weight = 262
title = "262. Gratuitous ARP — 무상 ARP"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Gratuitous ARP (GARP, 무상 ARP)는 자신의 IP 주소를 목적지로 하는 ARP 요청 또는 응답으로, 정상 목적(IP 충돌 감지, 장애 절체 MAC 갱신)과 악의적 목적(ARP 캐시 오염) 양면을 가진 이중적 프로토콜 동작이다.
> 2. **가치**: GARP는 VRRP (Virtual Router Redundancy Protocol), HSRP (Hot Standby Router Protocol) 등 HA (High Availability) 시나리오에서 필수적으로 사용되므로 무조건 차단할 수 없고 맥락에 따른 선택적 제어가 요구된다.
> 3. **판단 포인트**: 비신뢰 포트에서 발생하는 GARP는 DAI (Dynamic ARP Inspection)로 차단하고, 신뢰 포트(업링크, HA 피어)에서만 GARP를 허용하는 것이 실무 원칙이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

일반 ARP는 "이 IP를 가진 장치의 MAC 주소를 알려 달라"는 질의 응답이다. 반면 Gratuitous ARP는 자신의 IP를 다시 브로드캐스트하는 자기 발신(Self-Addressed) ARP다. 이름의 "Gratuitous(무상의)"는 "요청받지 않았음에도 불구하고 전송한다"는 의미다.

정상적인 활용 사례:
1. **IP 충돌 감지 (Duplicate IP Detection)**: 새 장치가 IP를 할당받은 뒤 해당 IP로 GARP를 전송한다. 응답이 오면 다른 장치가 이미 그 IP를 사용 중임을 감지한다.
2. **장애 절체 MAC 갱신**: VRRP/HSRP Failover 시 신규 마스터 라우터가 GARP를 전송해 스위치의 MAC 테이블과 호스트 ARP 캐시를 새 MAC으로 갱신한다.
3. **NIC (Network Interface Card) 교체 후 캐시 갱신**: 서버 NIC를 교체하면 IP는 동일하지만 MAC이 바뀌므로 GARP로 네트워크에 변경 사실을 알린다.

악의적 활용: 공격자는 피해자 IP에 대한 GARP를 전송해 네트워크 전체의 ARP 캐시를 자신의 MAC으로 교체할 수 있다. 이것이 ARP 스푸핑의 핵심 메커니즘 중 하나다.

📢 **섹션 요약 비유**: GARP는 이사 온 주민이 "나는 이 주소에 이사 왔다"고 마을 방송을 하는 것이다. 정상이면 실제 이사이지만, 사기꾼이 방송하면 남의 집 주소를 자기 것으로 바꾸는 것이 된다.

---

## 2. 구성요소

### GARP 패킷 구조

| 필드 | 정상 ARP Request | Gratuitous ARP |
|:---|:---|:---|
| 하드웨어 타입 | 1 (Ethernet) | 1 (Ethernet) |
| 오퍼레이션 코드 | 1 (Request) 또는 2 (Reply) | 1 또는 2 (구현마다 상이) |
| 발신자 MAC | 자신의 MAC | 자신의 MAC |
| 발신자 IP | 자신의 IP | 자신의 IP |
| 목적지 MAC | 00:00:00:00:00:00 (모름) | FF:FF:FF:FF:FF:FF (브로드캐스트) |
| 목적지 IP | 질의 대상 IP | **자신의 IP** (← 핵심 차이) |

### GARP 동작 흐름

```
[정상: VRRP Failover 시 GARP]

  마스터 라우터 장애 발생
          │
          ▼
  백업 라우터 → 마스터로 승격
          │
          ▼
  GARP 브로드캐스트 전송
  ARP: "Virtual IP 10.0.0.1의 MAC은 이제 BB:BB:BB:BB:BB:BB 입니다"
          │
  ┌───────┴──────────────────────┐
  │         L2 스위치              │
  │  MAC 테이블 갱신               │
  │  10.0.0.1 → BB:BB:BB:BB:BB:BB │
  └───────────────────────────────┘
          │
  호스트 ARP 캐시도 자동 갱신
  → 트래픽 절체 완료

[악의적: 공격자 GARP]

  공격자 → GARP 브로드캐스트:
  "게이트웨이 IP 192.168.1.1의 MAC은 EE:EE:EE:EE:EE:EE"
          │
          ▼
  모든 호스트 ARP 캐시 오염
  → 게이트웨이 트래픽이 공격자로 향함
```

### DAI에서의 GARP 처리

DAI는 GARP 패킷도 DHCP Snooping 바인딩 테이블과 대조한다. 바인딩 테이블에 없는 IP를 발신자 IP로 가진 GARP는 위조로 판단해 폐기한다. 따라서 DHCP Snooping이 정확한 테이블을 유지해야 DAI가 GARP를 올바르게 판단할 수 있다.

📢 **섹션 요약 비유**: 이사 방송을 마을 주민 명부(DHCP Snooping 테이블)와 대조해 명부에 없는 사람이 방송하면 방송을 끊는 것이 DAI다.

---

## 3. 구조 및 동작 원리

| 구분 | 정상 GARP | 악의적 GARP |
|:---|:---|:---|
| 발신자 | 실제 IP 소유자 (HA 라우터, 서버) | 공격자 |
| 목적 | MAC 캐시 갱신, 충돌 감지 | ARP 캐시 오염 |
| 발생 빈도 | 이벤트 기반 (드물게) | 지속적 (주기적 전송) |
| 포트 위치 | 신뢰 포트 (업링크, HA 인터페이스) | 비신뢰 액세스 포트 |
| DAI 처리 | 신뢰 포트는 검증 없이 통과 | 비신뢰 포트에서 테이블 불일치 시 폐기 |

📢 **섹션 요약 비유**: 반장이 자신의 번호를 게시판에 다시 붙이는 것(정상)과 다른 사람이 반장 번호인 척 붙이는 것(악의적)은 행동은 같아 보여도 의도와 결과가 완전히 다르다.

---

## 4. 비교 및 트레이드오프

**GARP 제한 보안 설정**:

1. **DAI + DHCP Snooping**: 비신뢰 포트의 GARP를 자동 필터링. 가장 효과적인 방어.
2. **스태틱 ARP 바인딩**: 중요 장치(게이트웨이, 서버)의 IP↔MAC을 정적 등록. GARP 수신 시 캐시 갱신 무시.
3. **arpwatch / XDR 모니터링**: GARP 발생 시 알림을 보내 관리자가 이상 여부를 판단.
4. **OS 레벨 GARP 수용 설정 (Linux)**:
```bash
# GARP로 인한 ARP 캐시 갱신 제한
sysctl -w net.ipv4.conf.all.arp_accept=0
sysctl -w net.ipv4.conf.all.drop_gratuitous_arp=1
```

**HA 시나리오에서 GARP 허용 필요성**:
- VRRP RFC 5798, HSRP, CARP (Common Address Redundancy Protocol) 등 모든 HA 프로토콜은 Failover 시 GARP를 사용해 네트워크 수렴(Convergence)을 가속한다.
- GARP를 전면 차단하면 Failover 후 트래픽이 수십 초~수 분간 블랙홀로 빠지는 장애가 발생한다.
- 따라서 "신뢰 포트는 GARP 허용, 비신뢰 포트는 차단"이 황금 원칙이다.

**기술사 시험 포인트**:
- GARP의 정상 사용(HA)과 악의적 사용(ARP 스푸핑)을 함께 서술해야 높은 점수를 받는다.
- "DAI 설정만으로 GARP를 완전 차단하면 어떤 문제가 생기는가?"라는 함정 질문에 HA 장애 시나리오로 답해야 한다.
- Linux의 `drop_gratuitous_arp` 커널 파라미터는 서버 강화(Hardening) 맥락에서 자주 언급된다.

📢 **섹션 요약 비유**: 구급차(HA 라우터)는 사이렌을 울리며 주차 금지 구역에 설 수 있지만, 일반 차(공격자)는 안 된다. 규칙이 신뢰 등급에 따라 달라야 한다.

---

## 5. 실무 적용 및 최적화 기법

GARP의 이중성을 이해하면 ARP 기반 보안 설계에서 "차단"과 "허용"의 경계를 정확히 설정할 수 있다. 무조건 차단하면 HA 인프라가 마비되고, 무조건 허용하면 ARP 스푸핑에 무방비 상태가 된다.

DAI의 신뢰/비신뢰 포트 구분과 DHCP Snooping 바인딩 테이블의 정확한 관리가 이 균형을 유지하는 핵심이다. 또한 GARP를 주기적으로 전송하는 이상 행동을 탐지하는 NDR (Network Detection and Response) 솔루션의 도입이 고도화된 방어를 가능하게 한다.

📢 **섹션 요약 비유**: 마을 방송은 이장(신뢰 포트)만 할 수 있게 하고, 일반 주민이 방송실에 접근하면 막는 것처럼, 포트 신뢰 등급으로 GARP를 관리해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| ARP (RFC 826) | 기반 프로토콜 | GARP의 상위 프로토콜 |
| ARP Spoofing | 악의적 활용 | GARP를 이용한 캐시 오염 |
| VRRP / HSRP | 정상 활용 | HA Failover 시 GARP 사용 |
| DHCP Snooping | 방어 전제 | DAI의 바인딩 테이블 제공 |
| DAI | 핵심 방어 | GARP 포함 ARP 패킷 검증 |
| `drop_gratuitous_arp` | OS 방어 | Linux 커널 수준 GARP 차단 |

### 👶 어린이를 위한 3줄 비유 설명
- GARP는 "나 이 집으로 이사 왔어요!"라고 마을 전체에 알리는 방송이다.
- 진짜 이사 온 사람이 하면 유용하고, 사기꾼이 남의 주소로 방송하면 큰일 난다.
- 그래서 마을 이장(신뢰 포트)이 하는 방송만 믿고, 모르는 사람 방송은 무시하는 것이 안전하다.
