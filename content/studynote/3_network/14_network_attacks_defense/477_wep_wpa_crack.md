+++
title = "무선 보안 공격: WEP/WPA 크래킹"
description = "WEP의 구조적 결함, WPA의 TKIP 공격, KRACK, 크래킹 도구(aircrack-ng), 무선 보안 강화를شرح"
date = 2024-02-01
weight = 18

[taxonomies]
subjects = ["network"]
tags = ["wep crack", "wpa crack", "krack", "aircrack", "wireless security", "wps"]

[extra]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: WEP(Wired Equivalent Privacy)은 1997년 도입된 초기 WiFi 보안 프로토콜로, RC4 스트림 암호의 구조적 결함으로 인해 5분 이내에破解 가능한 것이 입증되어 현재는 사용이 금지된다.
> 2. **가치**: WPA(WiFi Protected Access)는 WEP의 결함을克服하기 위해 TKIP를 도입했지만, 이후 Beck-Tews 공격, KRACK(Key Reinstallation Attack) 등追加적 취약점이 발견되어, 안전한 WPA2/WPA3으로의迁移이 필수적이다.
> 3. **융합**: 무선 보안 공격은 네트워크 보안 연구자와 공격자 모두에게 중요한領域이며, wireless protocol 자체의 보안 설계 원리를 이해하는 데 필수적이다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념

무선 보안 공격(Wireless Security Attack)은 WiFi 등 무선 네트워크의 보안 프로토콜을circumvent하여通信을 도청하거나Manipulate하는 공격이다. WEP의 RC4 결함, WPA의 TKIP 공격, WPA2의 KRACK, 그리고 WPS의 Brute Force 공격 등이 대표적이다.

### 필요성

무선 신호는 공간을 전파하므로 유선 네트워크와 달리 도청과 Manipulation이 매우 쉽다. 따라서 WiFi 보안 프로토콜의脆弱性을이해하는 것은 보안 담당자에게 필수적이며, 공격자도 동일한 지식을 악용하므로 방어侧은先行적으로 대응책을講じなければならない。

### 등장 배경

2000년대 WiFi 핫스팟의 확산과 함께 무선 보안 공격이 사회적으로 문제가 되었다. 2001년 Fluhrer, Mantin, Shamir이 WEP의 RC4 결함을 발표했고, 2008년 Beck-Tews가 WPA의 TKIP를 공격하는 방법을 공개했다. 2017년 KRACK이 WPA2의 4-Way Handshake 취약점을 exposed했다.

### 💡 비유

무선 보안 공격은 **"목소리가 들리는 열린 창문"** 에 비유할 수 있다. 유선은 벽에 둘러싸인密閉된 방이고, 무선은 창문을 열어놓은 상태와 같다. 보안 프로토콜은 창문에 설치하는 "커튼"이며, 커튼이 있으면 밖에서 안을 보기 어렵지만, 커튼에 구멍(WEP의 결함)이 있으면 그 구멍으로 안을 할수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### WEP 크래킹 동작 원리

WEP의 핵심 결함은 IV(Initialization Vector)의 크기(24비트)와 재사용 문제에서 비롯된다.

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    WEP 크래킹: RC4 스트림 암호의 결함                          │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  [WEP 암호화 구조]                                                     │
  ///
  ///  핵심 문제: IV 24bit → 약 5000 프레임마다 IV 충돌 발생                    │
  ///
  ///  평문(P) + CRC-32(MIC) → RC4(IV || Key) 와 XOR → 암호문(C)             │
  ///  전송: IV (평문) + C                                                     │
  ///
  │  [IV 충돌에 의한 평문 회복]                                              │
  ///
  ///  같은 IV || Key로 생성된 두 암호문 C1, C2가 있으면:                       │
  ///  C1 = P1 XOR RC4(IV||Key)                                           │
  ///  C2 = P2 XOR RC4(IV||Key)                                           │
  ///                                                                     │
  ///  C1 XOR C2 = P1 XOR P2 (RC4 값이 상쇄됨)                              │
  ///                                                                     │
  ///  따라서 두 평문의 XOR을 알면 패드 패턴을 역산할 수 있음                    │
  ///  예: “HTTP/1.0 200 OK” 등固定 平文 패턴을 알면 키 스트림 추출 가능        │
  ///
  │  [FMS 공격 (Fluhrer, Mantin, Shamir, 2001)]                             │
  ///
  ///  RC4의 " слабый 키" (weak keys) 문제를 利用:                          │
  ///  • 특정 패턴의 IV 뒤에 특정 KSA 초기값이 일정하게 반복됨                   │
  ///  • 이 경우 RC4 출력의 처음 바이트가 IV || Key의 일부를 leaks               │
  ///                                                                     │
  ///  공격자: 수백만 개의 weak IV를 수집                                       │
  ///  → 결합된 정보로부터 WEP 키를 역산                                       │
  ///  → 1~5분 내 전체 104비트 WEP 키 복원 가능!                              │
  ///
  │  [크래킹 도구: aircrack-ng]                                            │
  ///
  ///  1. monitor mode로 Packet capture                                       │
  ///     # airmon-ng start wlan0                                           │
  ///     # airodump-ng mon0                                                │
  ///                                                                     │
  ///  2. 수집된 패킷에서 weak IV 탐지                                       │
  ///     # airolib-ng db --import rawcap capture.cap                        │
  ///     # aircrack-ng db -w wordlist.txt                                  │
  ///                                                                     │
  ///  3. PTW (Ptex Tables and WEP attacks) - 더 빠른 공격                  │
  ///     # aireplay-ng -4 mon0 -b <AP MAC> -h <Client MAC>                 │
  ///     # packetforge-ng -0 -a <AP MAC> -h <Client MAC> \                │
  ///     # aircrack-ng replay_dec-*.cap                                    │
  ///
  │  [WEP 크래킹 방어]                                                      │
  ///
  ///  • WEP 사용 중단 (즉시 WPA/WPA2로迁移)                                 │
  ///  • 공유키(Shared Key) 인증도 WEP 기반이므로 공유키도安全问题                │
  ///  • 802.1X/EAP-TLS 등 enterprise 인증 도입                              │
  ///
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** WEP 크래킹의 핵심은 RC4 스트림 암호에서 IV가 재사용되는 지점(IV 충돌)을 利用하는 것이다. 스트림 암호의 안전성은 동일한 키 스트림으로 두 번 평문을 암호화하지 않아야 한다는데 기반하는데, IV가 24비트만으로 구성되면 이론적으로 약 5000프레임마다 같은 IV가出现한다. 공격자는 이 사실을 利用하여 동일 IV로 암호화된 패킷 여러 개를 수집하고,它们 사이의 XOR 연산으로 키 스트림을 추출하여, 그것을 利用하여 다른 패킷을 해독한다. aircrack-ng는 이 원리를 利用하여 대량 패킷을 수집하고 분석하는 크래킹 도구이다.

---

### WPA/WPA2 크래킹 및 KRACK

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    WPA/TKIP 공격 및 KRACK 동작 원리                            │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  [WPA (TKIP)의 취약점]                                                │
  ///
  ///  Beck-Tews 공격 (2008):                                                │
  ///  • TKIP의 Michael MIC ( Message Integrity Code) 결함 利用                │
  ///  • 12~15분의 공격 시간으로 TKIP를 깨트림 (하지만 AP 재부팅 필요)           │
  ///  • IEEE 802.11i에서 TKIP가 더 이상 권장되지 않음                          │
  ///
  ///  핵심 문제: WPA의 TKIP은 WEP의 RC4를再利用하여 호환성을 유지했기 때문에,     │
  ///            WEP의根本적 문제인 RC4 기반을 인양하지 못했다.                    │
  ///
  │  [KRACK — Key Reinstallation Attack (2017)]                            │
  ///
  ///  WPA2의 4-Way Handshake의 논리적 결함:                                    │
  ///  4-Way Handshake 메시지 3(PTK 설정)을 다시 받아도,                         │
  /// 受害자가 "相同的 nonce"로 키를 재설정할 수 있음!                              │
  ///
  ///  공격 시나리오:                                                        │
  ///  [Client]              [Attacker]                [AP]               │
  ///     │                      │                       │                    │
  ///     │───── SYN ───────────▶│───── SYN ──────────▶│                    │
  ///     │                      │                       │                    │
  ///     │◀──── SYN+ACK ─────│◀─── SYN+ACK ──────│                    │
  ///     │                      │                       │                    │
  ///     │───── 3번째 메시지 ──▶│ (Attacker가 가로챔)│                    │
  ///     │                      │───── 3번째 메시지 ──▶│  (정상 전달)       │
  ///     │◀──── 4번째 메시지 ◀──│◀─── 4번째 메시지 ◀──│                    │
  ///     │                      │                       │                    │
  ///     │  (키 설치 완료)        │                       │                    │
  ///     │                      │   [4번째 메시지를 다시 전송] │                   │
  ///     │◀──── 재전송 ◀────────│◀─── 재전송 ◀──────│                    │
  ///     │  (nonce 0으로 재설정) │                       │                    │
  ///     │                      │                       │                    │
  ///     │  ★ 재설정된 키로 이후 모든 트래픽을 해독可能 ★         │                    │
  ///
  │  [KRACK의 유형]                                                         │
  ///
  ///  • Targeted KRACK: 특정 Client를 대상으로 4-Way Handshake 가로채기        │
  ///  • Group Key KRACK: Group Key Handshake 공격                              │
  ///  • Fast BSS Transition KRACK:快速 로밍 중 키 재설치 공격                  │
  ///  • 4-Way Handshake KRACK: 상기 모든 것을 포괄하는 主공격                 │
  ///
  │  [KRACK 방어]                                                           │
  ///
  ///  • AP 및 Client firmware 업데이트 (패치 적용)                             │
  ///  • HTTPS 등 Application Layer 암호화 사용 ( end-to-end 보안)             │
  ///  • WPA3로迁移 (SAE 기반이므로 KRACK 면역)                                │
  ///
  │  [WPS (WiFi Simple Setup)의 PIN Brute Force 공격]                       │
  ///
  ///  WPS의 PIN은 8자리: 앞 4자리 + 뒤 4자리 = 2개의 독립적 검증               │
  ///  • 총 경우의 수: 10^4 × 10^4 = 1억 가지                                │
  ///  • 앞 4자리 틀리면 → 즉각 실패 (1/10,000)                             │
  ///  • 뒤 4자리 틀리면 → 실패 (1/10,000)                                   │
  ///  • 실제 공격: 평균 2~4시간 안에 PIN 복원 가능!                            │
  ///                                                                     │
  ///  ※ WPS 비활성화 필요!                                                   │
  │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** KRACK의 핵심 문제는 WPA2의 4-Way Handshake가 "메시지 3이 한 번 이상 수신되어도 키를 재설정하지 않도록防げない"다는 것이다. 정상 동작에서는 메시지 3을 한 번만 수신하고 키를 설치하지만, 공격자가メッセージ3를 가로챈 후/client에게 再び送信하면,受害자는 nonce를 0으로 재설정하고 같은 키를 다시 설치한다. 이때 nonce가 재사용되면, 이를 利用하여 기존에 잡아둔 패킷을 해독할 수 있다. 공격자는 AP와 직접 통신하지 않고 Client와 AP 사이에서消息를 전달하면서 일부러 재전송을 유발하므로, 방어하기 어렵다. 가장根本적인 방어는 WPA3(SAE 기반) 도입이며, 두 번째로 HTTPS처럼 End-to-End 암호화를 적용하여,たとえ无线层が破解されても应用层のデータは保護される。

---

### 무선 보안 공격 방어 전략

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    무선 보안 강화 체크리스트                                    │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  [즉시 확인 항목]                                                      │
  ///
  ///  □ WEP 사용 시 → WPA2/WPA3으로 即時迁移                               │
  ///  □ WPA (TKIP) 사용 시 → WPA2-AES 또는 WPA3으로迁移                     │
  ///  □ WPS 활성화 시 → WPS 비활성화 + WPA3 전환                         │
  ///  □ Default SSID/비밀번호 사용 → 고유 SSID + 복잡한 비밀번호 설정       │
  ///
  │  [WPA2/WPA3 보안 강화]                                                 │
  ///
  ///  □ WPA2-Personal (PSK) 대신 WPA2-Enterprise (RADIUS + EAP-TLS) 사용   │
  ///  □ PSK 사용 시 12자 이상 복잡한 비밀번호 (최소 20자 이상 권장)          │
  ///  □ 비밀번호 정기적 로테이션 (3~6개월마다)                                │
  ///  □ AES-CCMP (强制) → GCMP (Galois/Counter Mode Protocol) 로迁移        │
  ///  □ PMF (Protected Management Frames) 활성화                           │
  ///  □ AES-256 사용 (키 길이 최대)                                        │
  ///
  │  [네트워크 분리]                                                        │
  ///
  ///  □ Guest 네트워크와 내부 네트워크 분리                                    │
  ///  □ IoT 디바이스는 별도 VLAN에 격리                                      │
  ///  □ 관리용 SSID와 일반 SSID 분리                                         │
  ///  □ Firewall에서 Guest WLAN → 내부 네트워크 접근 차단                     │
  ///
  │  [모니터링 및 탐지]                                                     │
  ///
  ///  □ 무선 침입 탐지 시스템 (WIDS) 도입                                    │
  ///  □ Rogue AP 탐지 ( Evil Twin 탐지)                                     │
  ///  □ 무선 클라이언트流量 모니터링                                          │
  ///  □ aircrack-ng등 무선 분석 도구에 대한 알림 설정                         │
  ///
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 무선 보안 강화의 가장 중요한 첫걸음은 WEP와 WPA(TKIP)를 사용 중이라면 即時으로 WPA2-AES 또는 WPA3로迁移하는 것이다. WEP는 현재 완전히 깨져 있으므로 보안 가치가 전혀 없고, WPA(TKIP)도 실질적으로 안전한 수준이 아니다. 두 번째로 중요한 것은 WPS를 비활성화하는 것으로, WPS의 PIN Brute Force 취약점은 평균 수 시간 안에 PIN을破解할 수 있어, WPS가 활성화된 상태에서는 다른 어떤 강력한 암호화도 무력화된다. 세 번째로, Enterprise 환경에서는 WPA2-Enterprise(RADIUS + EAP-TLS)를 사용하여, 사전 공유 비밀번호 대신 인증서 기반 인증을 사용하는 것이 安全하다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 무선 보안 프로토콜 비교

| 프로토콜 | 암호화 | 키 길이 | 도입 시기 | 현재 상태 | 주요 취약점 |
|:---|:---|:---|:---|:---|:---|
| **WEP** | RC4 | 40/64-bit, 104/128-bit | 1997 | **사용 금지** | IV 충돌, FMS 공격 |
| **WPA** | TKIP + RC4 | 128-bit | 2003 | **非推奨** | Beck-Tews 공격 |
| **WPA2** | AES-CCMP | 128-bit | 2004 | **최소 권장** | KRACK (패치됨) |
| **WPA3** | AES-GCMP | 192-bit | 2018 | **권장** | dragonblood (일부) |
| **WPA3-Enterprise** | AES-GCMP-256 | 192-bit + 802.1X | 2018 | **최고 권장** | 基本 없음 |

### WEP → WPA → WPA2 → WPA3 진화 비교

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    WiFi 보안 프로토콜 진화 과정                                   │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  1997              2003              2004               2018         │
  │   │                │                  │                   │             │
  │   ▼                ▼                  ▼                   ▼             │
  /// [WEP]         → [WPA]          → [WPA2]          → [WPA3]        │
  /// RC4+CRC       TKIP+RC4        AES-CCMP         AES-GCMP          │
  /// 24bit IV       48bit IV       Counter Mode     Galois Counter    │
  /// 104bit key     Michael MIC     AES-256bit       192bit security   │
  ///                                                Suite B            │
  │   │                │                  │                   │             │
  ///   │           호환성 유지      현재 필수           SAE로 강화       │
  ///   │           WEP破绽修补        KRACK対応        .forward secrecy  │
  ///   │                                                          │
  ///   └────────────── 安全性 향상 ───────────────────────────────────▶│
  │
  │  [WPA3의 주요 개선점]                                                  │
  ///
  ///  ① SAE (Simultaneous Authentication of Equals)                         │
  ///     • Diffie-Hellman 기반 키 교환                                      │
  ///     • 사전 분산(密码 guessing) 공격 면역                                  │
  ///     • Forward Secrecy 제공                                              │
  ///                                                                      │
  ///  ② 192bit 보안 스위트 (Enterprise)                                      │
  ///     • 192-bit minimum Security strength                                 │
  ///     • Government/금융 수준 보안                                          │
  ///                                                                      │
  ///  ③ Easy Connect (DPP)                                                  │
  ///     • QR코드/NFC로 안전한 디바이스 페어링                                │
  ///     • WPS의脆弱성을 해결                                               │
  ///
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** WiFi 보안의 진화는 끊임없는 공격과 방어의軍備 Race이다. WEP은诞생 직후부터 RC4의 결함이 노출되어 수 분 내破解되었고, WPA는 이를 TKIP와 Michael MIC로 일시적으로 해결했지만, 근본적으로 RC4 기반을 탈피하지 못해再度 공격에破れた。WPA2는 AES-CCMP로 완전히 새로운 암호화 체계를 도입하여 현재까지 실질적 보안 수준을 유지하고 있지만, 2017년 KRACK이 또 다른protocol层面的脆弱性を暴露했다. WPA3는 SAE를 도입하여 이러한protocol攻撃을根本적으로 방어하며, 특히 Forward Secrecy를 제공하여 키가破解되더라도 이전의 통신은保護된다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 레거시 AP의 WPA → WPA2 업그레이드**: 10년 된 AP에서 WPA만 지원하여 즉각 WPA3로 업그레이드할 수 없는 상황. 먼저 WPA2-AES로 업데이트하고, firmware가 지원하지 않으면 AP를 교체한다. 교체 전까지는 WPA의 TKIP를 비활성화하고 AES만 사용하도록 설정한다.

2. **시나리오 — Evil Twin 공격 탐지**: 사무실 WiFi에서 Evil Twin(공격자 AP) 공격이 의심되는 상황. 탐지 방법으로 무선 IDS(WIDS)를 활용하여 동일한 SSID에 여러 BSSID가 존재하거나, 알 수 없는 AP가 탐지되면警报을 발생시킨다. 대응으로 무선 클라이언트가 접속하는 AP의 BSSID와 RSSI 프로파일을 지속적으로 모니터링하고, 변화가 감지되면 사용자에게 경고한다.

3. **시나리오 — 대규모 WiFi 네트워크 보안 감사**: 500개의 AP로 구성된 기업 WiFi 네트워크의 보안을 감사하려는 상황. aircrack-ng와 같은 도구로 샘플 AP의 패킷을 수집하여 IV traffic을 分析하고, IV 충돌이나 비정상 패턴이 감지되면 해당 AP를즉시조사한다. 또한 WIPS(Wireless Intrusion Prevention System)를 활용하여 전체 네트워크를 실시간으로 모니터링하고, Evil Twin, Rogue AP, 잘못된 채널 설정 등을 자동으로 탐지·대응한다.

### 도입 체크리스트

- **기술적**: 모든 AP가 WPA2-AES 이상을 지원하는가? WPS가 비활성화되어 있는가? PMF(Protected Management Frames)가 활성화되어 있는가?
- **운영·보안적**: 무선 네트워크 보안 정책이 수립되어 있는가? 정기적인 보안 감사가 수행되고 있는가?

### 안티패턴

- **Open WiFi 운영**: 암호화 없는 открытый WiFi는 도청, 세션 하이재킹, 맬웨어 주입에完全히 취약하다. 절대 허용해서는 안 된다.
- **Default SSID/비밀번호**: 기본 SSID와 비밀번호를 그대로 사용하면 공격자가 이를 利用하여 쉽게 네트워크에 접근할 수 있다. 반드시 변경해야 한다.

- **📢 섹션 요약 비유**: WiFi 보안의 진화는 **"나무 문 → 철문 → 금고 문"** 의 진화로 비유할 수 있다. WEP은 나무 문처럼 쉽게 부서지고, WPA는 철문을 덮었지만根本적으로 같은 재질이고, WPA2는 완전히 새로운 금고 문이지만 열쇠穴에 약간 틈이 있었고( KRACK), WPA3는 그 틈까지 봉인한 완전히 새로운 금고 문이다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

- **WPA3의普及**: WPA3는 현재 대부분의新しい AP에서 지원되지만,古い AP의比例为 많아 아직 完全導入에는 시간이 걸릴 전망이다.
- **Enhanced Open**: WPA3의 Enhanced Open은 открытый WiFi에서도 Opportunistic Wireless Encryption(OWE)을提供하여, 별도 비밀번호 없이도 암호화를 적용할 수 있게 한다.

### 참고 표준

- IEEE 802.11i: WiFi 보안 표준 (WPA2)
- IEEE 802.11w: Protected Management Frames
- WiFi Alliance WPA3 Certification

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **WEP (Wired Equivalent Privacy)** | 1997년 도입된 초기 WiFi 보안으로, RC4 스트림 암호의構造的 결함으로 인해 5분 이내에破解 가능하다. 사용이 금지된다. |
| **TKIP (Temporal Key Integrity Protocol)** | WPA에서 사용된 임시 프로토콜로, WEP의 RC4를再利用하여 호환성을 유지했지만, Beck-Tews 공격에破れた。 |
| **KRACK (Key Reinstallation Attack)** | 2017년 발견된 WPA2의 4-Way Handshake 취약점으로, nonce 재사용을 유발하여 암호화된 패킷을 해독하는 공격이다. 대부분のパッチ已经发布。 |
| **aircrack-ng** | 무선 네트워크 크래킹에 사용되는 主要 도구로, 패킷 캡처, IV 수집, WEP/WPA 크래킹 기능을 제공한다. |
| **WPS (WiFi Simple Setup)** | PIN 또는 버튼으로 간단하게 WiFi 연결을 설정하는 기능으로, PIN Brute Force 취약점이 있어 비활성화가 권장된다. |
| **SAE (Simultaneous Authentication of Equals)** | WPA3에서 도입된 Diffie-Hellman 기반의パスワード-less 인증으로, 사전 분산攻撃에免疫이고 Forward Secrecy를 제공한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. WEP 크래킹은 **"나무 문에 구멍이 뚫린 것"** 과 같아요. 나무 문이면 발로 차면 금방 부서지고, 구멍도 뚫려 있어서 안이 보이듯, WEP도 쉽게突破되고 내용이 보여요.
2. KRACK은 **"열쇠를 다시 낼설할 때 생기는 공벽"** 에 비유할 수 있어요. 금고 문을 열어서 안에 들어갔는데, 다시 열쇠를 넣으려니까 같은 열쇠를 여러 번 넣게 되어서( nonce 재사용) 금고 문이 잠기지 않아요. 그래서 안에 있는 내용을 알 수 있게 돼요.
3. WPA3의 SAE는 **"서로 모르는 사람끼리 비밀 편지를 보내는 방법"** 예요. 비밀번호를 공유하지 않고도 각자 자기만의 비밀로부터 열쇠를 만들，所以在即使 누군가 横取り해도 열쇠를 알 수 없어요.
