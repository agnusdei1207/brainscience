+++
weight = 1
title = "DNS resolution/DDNS"
description = "DNS 질의 과정의 상세 동작과 동적 DNS(DDNS)의 동작 원리를 다룬다."
date = 2024-02-01

[extra]
categories = ["studynote-software-engineering"]
topics = ["dns", "ddns", "name-resolution"]
study_section = ["section-10-dns-management"]

number = "905"
core_insight = "DNS resolution은 클라이언트에서 도메인 이름을 입력하면Recursive Resolver를 통해 최종 IP를 얻는 과정이며, DDNS는 DHCP로 할당받은 동적IP를DNS에 실시간으로 반영하는 기술이다."
key_points = ["Recursive vs Iterative 질의", "로컬 캐시와 네임스택 분해", "DDNS (Dynamic DNS)", "Negative Cache와 NXDOMAIN"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DNS resolution은 도메인 이름을 입력から始まり、 Recursive Resolver가 Root → TLD → Authoritative Server를 순차적으로 탐색하여IP를 찾는 과정이다.
> 2. **가치**: 분산된 数据库를 통해 확장성 있게 도메인 이름을IP로 변환하며, 캐싱을 통해 반응 속도를 높이고 부하를 분산한다.
> 3. **융합**: DDNS는 동적IP 환경에서도 도메인 이름을 통한 접근을 가능하게 하여, 가정/소규모 서버 운영에 필수적이다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

**개념**: DNS resolution은 사용자가 웹 브라우저에 도메인 이름(예: www.example.com)을 입력하면, 컴퓨터가 이를IP 주소(예: 93.184.216.34)로 변환하는 과정이다. 이 과정에는 로컬 캐시 확인, Recursive Resolver 탐색, Root/TLD/Authoritative Server 순차 탐색이 포함된다. DDNS(Dynamic DNS)는IP 주소가 동적으로 변경되는 환경(일반 가정망, 모바일)에서 도메인 이름을 통한 접근을 가능하게 하는 기술이다.

**필요성**: DNS resolution이 없으면, 人们은IP 주소만으로 웹사이트에 접근해야 한다. IPv4 주소마저 142.250.196.46같이 기억하기 어렵다. 또한IP 주소는 ISP에 의해 동적으로 변경될 수 있으며(일반 가정망), 이 경우 외부에서 도메인 이름으로 접속이 불가능하다. DDNS는 이러한 문제를 해결하여,IP가 변경되어도 도메인 이름이 계속 유효하도록 한다.

**비유**: DNS resolution은 **궁금한 이름을 검색해 주소를 찾는 일**과 같다. 친구에게「google.com 알려줘」と頼むと, 친구가 알고 있으면 바로 알려주고, 몰라서다른 친구에게 물어보고, 그래도 모르니「톱的电话번호부」(Root Server)에 가서「.com 펜네」를 찾고, 다시「google.com 관리자」(Authoritative Server)에 물어보는 거예요.

**등장 배경**: DNS resolution의 기본 개념은1983년 Paul Mockapetris가 설계했으며, 이후 30년 이상 동일한 구조로 운영되고 있다. DDNS는1990년대后半，家庭用 broadband에서 동적IP가 일반화되면서 등장했다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### DNS Resolution 상세 과정

```
┌───────────────────────────────────────────────────────────────────────┐
│                    DNS Resolution 상세 과정                              │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  상황: 웹 브라우저에 "www.example.com" 입력                            │
│                                                                       │
│  ① 로컬 캐시 확인:                                                     │
│     • OS DNS 캐시 확인 (Windows: ipconfig /displaydns)                │
│     • 브라우저 캐시 확인 (Chrome: chrome://net-internals/#dns)       │
│     • hosts 파일 확인 (/etc/hosts)                                     │
│     • 있으면 바로IP 반환 (캐시 히트)                                   │
│                                                                       │
│  ② Recursive Resolver에 질의 (예: 8.8.8.8):                           │
│     • 로컬 캐시 없음 → Recursive Resolver에 DNS 쿼리 전송             │
│     • UDP 포트 53                                                      │
│                                                                       │
│  ③ Recursive Resolver의 탐색:                                         │
│                                                                       │
│     Step 1: Root Server 질의                                          │
│     "com 도메인의 TLD Server 어디?"                                    │
│     → Root Server (a~m.root-servers.net)                           │
│     → TLD Server 목록 반환 (예: a.gtld-servers.net)                 │
│                                                                       │
│     Step 2: TLD Server (.com) 질의                                  │
│     "example.com의 Authoritative Server 어디?"                        │
│     → TLD Server가 NS 레코드 반환 (예: ns1.example.com)             │
│                                                                       │
│     Step 3: Authoritative Server 질의                                  │
│     "www.example.com의 IP?"                                          │
│     → Authoritative Server가 A 레코드 반환 (93.184.216.34)          │
│                                                                       │
│  ④ Recursive Resolver이 결과를 캐시 + 클라이언트에 반환              │
│                                                                       │
│  ⑤ 클라이언트가IP로 웹 서버에 연결                                      │
│                                                                       │
│  캐시와 TTL의 역할:                                                    │
│  • 각 DNS 레코드에는 TTL (Time To Live)이 설정됨                      │
│  • 예: A 레코드 TTL=3600 → 1시간 동안 캐시됨                         │
│  • 캐시로 인해 즉시 반영 안 될 수 있음 (DNS 변경 시 주의)               │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** DNS resolution의 핵심 설계 원칙은「분산과 캐싱」이다. 전 세계에 분산된 서버들이 협력하여 확장성 있는 이름 해결을 가능하게 한다. 각 단계에서 캐싱이 이루어지므로, 반복적인 질의는 네트워크를 거치지 않고 빠르게 처리된다. 그러나 캐싱으로 인해DNS 변경이 즉시 반영되지 않는问题가 있다. 예를 들어, 웹사이트를 새 서버로 이전할 때,旧的IP가 캐시되어 있으면 이용자가 여전히旧的 서버에 연결된다. 이를 해결하려면TTL을 사전에 짧게 설정하거나, 이전 서비스 중단 시간 동안 캐시를 명확히해야 한다.

### Negative Cache와 NXDOMAIN

DNS는 존재하지 않는 도메인에 대한 질의 결과(NXDOMAIN)도 캐시한다. Negative Cache는 이런 실패 결과도 저장하여, 반복적인 실패 질의를 방지한다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    Negative Cache 동작                                  │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  존재하지 않는 도메인 질의 시:                                          │
│                                                                       │
│  Client ──▶ "nonexistent.example.com" 쿼리 ──▶ Resolver             │
│                    │                                                  │
│                    │ (없으면)                                          │
│                    ▼                                                  │
│              Authoritative Server                                    │
│                    │                                                  │
│                    ▼                                                  │
│              NXDOMAIN (도메인 존재 안 함)                             │
│                    │                                                  │
│                    ▼                                                  │
│              Resolver가 NXDOMAIN 캐시 (Negative Cache)                │
│              • SOA Minimum TTL만큼 캐시됨 (일반적으로 300초~3600초)  │
│                    │                                                  │
│                    ▼                                                  │
│              Client에게 "nonexistent 없음" 응답                      │
│                                                                       │
│  이후 동일 도메인 질의 시:                                              │
│  • Negative Cache期限内 → 즉시 NXDOMAIN 응답                         │
│  • Cache 만료 후 → 실제 Authoritative Server에 재질의                │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  Negative Cache의 문제점:                                       │   │
│  │  • 잘못된 Negative Cache가長시간 남아있으면, 실제로 존재하는      │   │
│  │    도메인도「없음」으로 인식될 수 있음                            │   │
│  │  • 해결: SOA Minimum TTL을 합리적으로 설정                        │   │
│  │  • DNS 서버 재시작 시 Negative Cache 초기화                       │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

### DDNS (Dynamic DNS)

DDNS는IP 주소가 동적으로 변경되는 환경에서 도메인 이름을 통한 접근을 가능하게 한다. 일반 가정용 broadband에서는 ISP가IP를 동적으로 할당하며,IP가 변경되면 외부에서 해당 네트워크에 접근할 수 없다. DDNS는 변경된IP를DNS에 자동으로更新하여, 도메인 이름이 계속 유효하도록 한다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    DDNS 동작 과정                                         │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【배경】                                                              │
│  • 가정용 broadband: ISP가 동적IP 할당 (예: 121.134.77.x)           │
│  • IP가 변경되면? → 기존IP로 접속 불가                                  │
│  • DDNS: 변경된IP를DNS에 자동으로 更新                                   │
│                                                                       │
│  【DDNS 과정】                                                         │
│                                                                       │
│  [Home Server]           [DDNS Provider]        [Internet User]       │
│                                                                       │
│  │                                                                   │
│  │ ① DDNS Client가 현재IP 확인 (curl ifconfig.me 등)                │
│  │                                                                   │
│  │ ② IP 변경 감지 → DDNS Provider에 인증 + IP 업데이트 요청            │
│  │ ──────────────────────────────────────────────────────────────▶ │
│  │     URL: https://update.example.com?hostname=home&token=xxx     │
│  │     방법: HTTP GET, HTTPS GET, 또는 특화 프로토콜                  │
│  │                                                                   │
│  │ ③ DDNS Provider가 DNS A 레코드 更新 (TTL=60초 등 짧게)           │
│  │ ◀───────────────────────────────────────────────────────────── │
│  │                                                                   │
│  │ ④ Internet User가 도메인 질의 → DDNS Provider DNS가更新된IP 반환 │
│  │                                                                   │
│  │                 [Internet User]                                   │
│  │                       │                                           │
│  │                       │ "home.example.com" 쿼리                   │
│  │                       ▼                                           │
│  │              [DDNS Provider DNS]                                  │
│  │                       │                                           │
│  │                       │ Updated IP (121.134.77.y)                │
│  │                       ▼                                           │
│  │                 [Home Server] ◀── 새IP로 접속 성공!               │
│  │                                                                   │
│  DDNS Provider 예시:                                                 │
│  • dyndns.org, no-ip.com, DuckDNS, Cloudflare API 등                  │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** DDNS의 핵심은「동적IP更新の自动化」이다.従来のDNSでは、IP 주소を手動で更新する必要があった。 DDNSクライアント는 정기적으로(또는IP 변경 감지 시) DDNS Provider에 현재IP를通知한다. Provider는 해당 도메인의 A 레코드를 새IP로更新하고, 짧은 TTL(예: 60초)을 설정하여 다른利用者が即座에更新된IP를 얻을 수 있게 한다. 이를 통해 고정IP없이도 웹캠, 게임 서버, 원격 접속 등을 도메인 이름으로 이용할 수 있다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### DNS 질의 유형

| 유형 | 설명 | 사용처 |
|:---|:---|:---|
| **Recursive** | Resolver가 전 과정 처리, 최종 결과만 반환 | 클라이언트 → Resolver |
| **Iterative** | 각 서버가直接答えを返す, 다음服务器을 안내 | Resolver ↔ DNS Servers |
| **Forwarding** | 다른 Resolver에 질의 위임 | 특정 DNS 서버들 사이 |

### DDNS vs Static DNS

| 항목 | DDNS | Static DNS |
|:---|:---|:---|
| **IP 변경** | 자동 更新 | 수동 更新 |
| **적합한 환경** | 가정용 broadband, 모바일 | 서버, 기업 네트워크 |
| **갱신 지연** | 즉시(거의) | 수동 작업 필요 |
| **비용** | 무료/저렴 | 무료/비용 발생 가능 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 1 — DDNS를利用한 홈 네트워크 원격 접속**: 가정에서 NAS(Network Attached Storage)에 외부에서 접근하려는 경우. DDNS服务商에 가입하고, 공유기에 DDNS client를 설정한다. IP가 변경될 때마다 공유기가 자동으로 DDNS Provider에更新한다. 외부에서는 도메인 이름으로 NAS에 접근할 수 있다.

**시나리오 2 — DNSNegative Cache 문제 해결**:某 웹사이트迁移 후 일부 利用자가旧的 서버에 접속하는 문제. 원인: DNS Negative Cache에「없음」이缓存되어 있었다가, 새 서버IP를알아도 여전히「없음」으로 인식. 해결: DNS 변경 전 TTL을 짧게 설정(60초), 이전 호스팅 계정은 즉시停止, DNS 변경 후客户端에서 DNS 캐시flush(ipconfig /flushdns).

### 도입 체크리스트

- **기술적**: TTL 적절한 설정, Negative Cache TTL 확인, DDNS Provider 신뢰성
- **운영·보안적**: DDNS 토큰/자격 증명 安全保管, 불필요한 DNS 레코드 정리

### 안티패턴

- **너무 긴 TTL**: DNS 변경 시 반영이 늦어지며, 특히 서비스 이전 시 이용자가旧的 서버에 계속 접속하게 된다.
- **DDNS 토큰 노출**: DDNS 업데이트 URL이 노출되면 누구나IP를更改할 수 있으므로, 토큰을 安全保管해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

DNS resolution은 DNSSEC, DoH/DoT 등으로安全と privacyが強化되고 있다. DDNS는 IoT, 스마트홈 환경에서 외부 접근을 위한 필수 기술로 자리잡을 것이다. 또한 클라우드 환경에서 동적IP/프라이빗 링크를DNS에 자동 반영하는 기술도 발전하고 있다.

### 참고 표준

- RFC 1034 — Domain Names - Concepts and Facilities
- RFC 2308 — Negative Caching of DNS Queries
- RFC 2136 — Dynamic Updates in the Domain Name System (DNS UPDATE)

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Recursive Resolver** | 클라이언트 대신 DNS 질의 전체 과정을 수행하는 서버이다. |
| **Authoritative Server** | 실제 DNS 레코드를 보유한服务器로, 최종IP를 제공한다. |
| **TTL** | DNS 레코드의 캐시有効期限으로, 짧게 설정하면 변경 사항이 빠르게 반영된다. |
| **NXDOMAIN** | 존재하지 않는 도메인을 나타내는 DNS 응답 코드로, Negative Cache의 대상이 된다. |
| **DDNS** | 동적으로 변경되는IP를DNS에 자동更新하는 기술이다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. DNS 해결은 **친구한테 물어봐서 전화를 돌리는 과정**과 같아요. 친구가 모르면 다른 친구에게, 그래도 모르겠으면 큰 전화번호부(Root Server)에 가서 찾아보는 거예요.
2. Negative Cache는 **「없는 번호」도 기억하는 것**이야. 한 번 「없는 번호」라고 알려주면, 그 정보도 잠시 동안 기억해서 또 찾으러 가지 않아도 돼요.
3. DDNS는 **시리야, 내 번호 바뀐 거 알아!」라고 전화하는 것과 같아요. 집 전화번호가 바뀌면 DDNS 서비스에 새로운 번호를 알려줘서, 사람들이 항상 같은 이름(도메인)으로 우리 집에 전화할 수 있게 해줘요!
