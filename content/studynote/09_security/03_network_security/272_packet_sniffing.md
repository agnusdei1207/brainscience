+++
weight = 272
title = "272. 패킷 스니핑 (Packet Sniffing)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: 패킷 스니핑(Packet Sniffing)은 네트워크를 지나는 패킷을 캡처·분석하는 행위로, NIC (Network Interface Card)의 프로미스큐어스 모드(Promiscuous Mode) 활성화가 핵심 기술 원리다.
> 2. **가치**: 합법적 도구(Wireshark)로 네트워크 진단에 필수적이지만, 동일 원리로 평문 자격증명·세션 쿠키·민감 데이터를 탈취할 수 있어 TLS (Transport Layer Security) 암호화 강제가 유일한 근본 방어책이다.
> 3. **판단 포인트**: 허브(Hub) vs 스위치(Switch) 환경에서 스니핑 범위가 달라지며, 스위치 환경에서는 ARP (Address Resolution Protocol) 스푸핑이나 포트 미러링을 통해 우회하므로 암호화가 핵심이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

이더넷 네트워크의 기본 원리는 **공유 매체(Shared Medium)**다. NIC는 자신의 MAC (Media Access Control) 주소로 향하는 프레임만 처리하지만, 프로미스큐어스 모드로 설정하면 같은 세그먼트의 **모든 패킷**을 캡처한다.

네트워크 관리자에게 스니핑은 필수 진단 도구다. 지연(Latency) 분석, 애플리케이션 오류 추적, 보안 인시던트 조사 모두 패킷 분석 없이는 불가능하다. Wireshark, tcpdump, tshark가 대표적인 합법적 도구다.

반면 공격자는 동일 원리로 **평문(Plaintext)으로 전송되는 자격증명, 세션 쿠키, 이메일 내용**을 가로챈다. 특히 공용 무선랜(Public Wi-Fi) 환경에서 암호화 없는 HTTP, FTP (File Transfer Protocol), TELNET 트래픽은 스니핑에 완전히 노출된다. 2010년 Firesheep 도구는 Wi-Fi에서 Facebook 세션 쿠키를 원클릭으로 탈취해 보안 커뮤니티에 충격을 주었고, 이후 주요 웹서비스의 HTTPS 전환을 앞당겼다.

📢 **섹션 요약 비유**: 패킷 스니핑은 동네 공중파 라디오를 듣는 것과 같다. 암호화(TLS) 없이 전송하면 같은 주파수를 듣는 누구나 내용을 알 수 있다.

---

## 2. 구성요소

### 유선 환경: 허브 vs 스위치 비교

```
[허브 환경 - 모든 포트에 브로드캐스트]

PC-A ──┐
PC-B ──┤──[허브]── 공격자(C)
PC-C ──┘
         ↑
    C는 A→B 패킷도 수신
    (프로미스큐어스 모드 ON)

[스위치 환경 - MAC 테이블 기반 유니캐스트]

PC-A ──┐
PC-B ──┤──[스위치]── 공격자(C)
PC-C ──┘
         ↑
    정상: C는 A→B 패킷 미수신
    우회: ARP 스푸핑으로 MAC 테이블 오염
```

### 스위치 환경 우회 기법

| 기법 | 원리 | 비고 |
|:---|:---|:---|
| ARP 스푸핑 (Spoofing) | 위조 ARP 응답으로 MAC 테이블 오염 | 스위치 환경 주요 우회 수단 |
| MAC 플러딩 (Flooding) | MAC 테이블 고갈로 허브 동작 유도 | 스위치 보호 기능으로 방어 가능 |
| 포트 미러링 (SPAN) | 관리자 권한으로 포트 트래픽 복사 | 정당한 관리 목적이나 내부자 위협 |
| DHCP 스푸핑 | 가짜 게이트웨이 제공 | IP 레벨 MITM 유도 |

### 무선 환경 스니핑

무선 LAN (Local Area Network)은 더 위험하다. 공유 매체 특성상 같은 채널의 모든 프레임을 수신할 수 있으며, 모니터 모드(Monitor Mode) 활성화 시 프레임 전체를 캡처한다.

- **WEP (Wired Equivalent Privacy)**: RC4 취약점으로 수분 내 크래킹 가능
- **WPA (Wi-Fi Protected Access)**: TKIP (Temporal Key Integrity Protocol) 취약점 존재
- **WPA2-Personal**: PMK (Pairwise Master Key) 오프라인 사전 공격 가능
- **WPA3**: SAE (Simultaneous Authentication of Equals) 핸드셰이크로 오프라인 공격 차단

📢 **섹션 요약 비유**: 스위치는 편지를 정확한 주소로 배달하지만, ARP 스푸핑은 우체부에게 "우리 집 주소가 바뀌었어요"라고 거짓말해 편지를 빼돌리는 것이다.

---

## 3. 구조 및 동작 원리

### 스니핑 탐지 및 방어 기법

| 구분 | 기법 | 설명 |
|:---|:---|:---|
| **암호화** | TLS 1.3 / HTTPS | 캡처해도 해독 불가 |
| **암호화** | SSH (Secure Shell), SFTP | 평문 TELNET/FTP 대체 |
| **암호화** | VPN (Virtual Private Network) | 전체 트래픽 터널링 |
| **탐지** | 프로미스큐어스 모드 탐지 | ARP 응답 시간 이상 감지 |
| **탐지** | IDS (Intrusion Detection System) | 비정상 트래픽 패턴 알람 |
| **방어** | 동적 ARP 검사 (DAI, Dynamic ARP Inspection) | ARP 스푸핑 차단 |
| **방어** | 802.1X 포트 인증 | 비인가 장비 연결 차단 |
| **방어** | 물리 보안 | 공격자 네트워크 접근 원천 차단 |

### Wireshark 실습 예시 (합법적 진단)

```
# tcpdump 예시: 특정 호스트의 HTTP 트래픽 캡처
tcpdump -i eth0 -w capture.pcap host 192.168.1.1 and port 80

# Wireshark 필터: HTTP POST 요청만 표시
http.request.method == "POST"

# TLS 핸드셰이크 분석
tls.handshake.type == 1    # ClientHello
tls.handshake.type == 2    # ServerHello

# 암호화 여부 확인: TLS 캡처 시 Application Data만 보임
# 자격증명 평문 노출 없음 (암호화 효과 확인)
```

📢 **섹션 요약 비유**: TLS는 유리창 편지함을 금고 투입구로 바꾸는 것이다. 스니퍼가 패킷을 가져가도 내용을 읽을 수 없다.

---

## 4. 비교 및 트레이드오프

**계층별 방어 전략**

```
Layer 7 (응용)  │ HTTPS 강제, HSTS 헤더
                │ 암호화되지 않은 프로토콜 금지 (HTTP, FTP, TELNET)
─────────────────┼──────────────────────────────
Layer 4 (전송)  │ TLS 1.3 최소 요구
                │ 취약한 암호 스위트(Cipher Suite) 비활성화
─────────────────┼──────────────────────────────
Layer 3 (네트워크)│ IPsec 터널 모드 VPN
                │ DNSSEC (DNS Security Extensions)
─────────────────┼──────────────────────────────
Layer 2 (데이터링크)│ 동적 ARP 검사 (DAI)
                │ 포트 보안 (Port Security)
                │ 802.1X 인증
─────────────────┼──────────────────────────────
Layer 1 (물리)  │ 물리적 포트 잠금, CCTV, 접근 통제
```

**무선 환경 권장 설정**:
- WPA3-Enterprise (802.1X + EAP-TLS) 사용
- SSID (Service Set Identifier) 분리: 업무망 / 게스트망 / IoT망
- 클라이언트 격리(Client Isolation) 활성화
- 무선 IDS/IPS 배포로 불법 AP (Access Point) 탐지

**기술사 답안 포인트**: 스니핑 자체는 수동적 공격이지만, ARP 스푸핑과 결합하면 능동적 MITM으로 발전한다. "탐지보다 암호화 우선"이 설계 원칙임을 강조해야 한다.

📢 **섹션 요약 비유**: 대화 내용을 못 엿듣게 하려면 방음벽(탐지)보다 외국어로 말하는 것(암호화)이 더 확실하다.

---

## 5. 실무 적용 및 최적화 기법

패킷 스니핑 방어의 핵심은 단 하나: **암호화**다. 탐지 기법은 보조 수단이며, ARP 검사나 802.1X는 내부망 위협 완화에 유효하지만 암호화를 대체하지 못한다.

현대 웹 생태계에서 HTTPS는 선택이 아닌 기본이며, Let's Encrypt로 무료 TLS 인증서가 보편화된 이후 "비용 문제"라는 핑계도 사라졌다. 내부망도 예외 없이 암호화(Zero Trust 원칙)하는 방향이 정답이다.

📢 **섹션 요약 비유**: 과거에는 집 안에서는 속삭여도 됐지만, 이제는 집 안에도 도청기가 있을 수 있다. Zero Trust = 어디서든 암호화.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| TLS (Transport Layer Security) | 핵심 방어 | 캡처해도 해독 불가 |
| ARP 스푸핑 | 연계 공격 | 스위치 환경 스니핑 우회 |
| Wireshark / tcpdump | 도구 | 합법적 패킷 분석 도구 |
| MITM (Man-In-The-Middle) | 발전 형태 | 스니핑 + 트래픽 조작 |
| 프로미스큐어스 모드 | 기술 원리 | 모든 패킷 수신 NIC 설정 |
| 802.1X | 보완 방어 | 포트 인증으로 비인가 장비 차단 |

### 👶 어린이를 위한 3줄 비유 설명
패킷 스니핑은 공원에서 사람들이 나누는 대화를 멀리서 듣는 것과 같아요.
암호화(TLS)는 외국어로 대화하는 것이에요. 들어도 무슨 말인지 몰라요!
그래서 인터넷에서는 항상 HTTPS(자물쇠 표시) 사이트를 쓰는 게 중요해요.
