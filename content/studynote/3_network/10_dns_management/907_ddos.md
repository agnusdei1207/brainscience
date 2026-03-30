+++
weight = 3
title = "DDoS (Distributed Denial of Service) 공격"
description = "DNS 기반 DDoS 공격의 유형, 증상, 그리고 방어 메커니즘을 다룬다."
date = 2024-02-03

[extra]
categories = ["studynote-software-engineering"]
topics = ["dns", "ddos", "dns-security", "amplification"]
study_section = ["section-10-dns-management"]

number = "907"
core_insight = "DDoS 공격은 다수의 분산 호스트에서標적服务器에大量 트래픽을 흘려보내 서비스를 마비시키는 공격이다. DNS는 amplification 공격의 반사점으로 악용되며, Anycast, Rate Limiting, DDoS Mitigation Service 등으로 방어한다."
key_points = ["DNS Amplification 공격", "Anycast 기반 분산", "Rate Limiting과 RRL", "DDoS Mitigation Service"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DDoS 공격은 다수의 분산 호스트에서標적服务器에大量 요청/트래픽을 흘려보내 정상적인 서비스를 방해하는 공격이다.
> 2. **가치**: DNS는 작은 요청으로 큰 응답을 생성하는 amplification 특성이 있어, DNS 기반 DDoS 공격의 반사점으로 악용되기 좋다.
> 3. **융합**: 현대 DDoS 공격은 대규모 분산 Botnet(Zombie PC)으로 수행되며, 공격 규모가 1Tbps를 넘기도 한다. Anycast, CDN, 전문 DDoS 방어 서비스로 대응한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

**개념**: DDoS(Distributed Denial of Service) 공격은 한명의攻撃자가 아니라, Internet에 감염된 수천~수백만 대의 Zombie PC(殲尸 네트워크/Botnet)로 구성된 네트워크로부터 동시에標적服务器에大量 트래픽을 흘려보내 서비스不能用하게 만드는 공격이다. DNS와 관련된 DDoS 공격으로는 DNS Server를 직접Target으로 하는 공격, DNS를 reflector/amplifier로悪用하는 공격이 있다.

**필요성**: DDoS 공격은 웹 서비스, 온라인 게임, 금융 서비스 등을 마비시켜 실질적인 피해를준다. 2016년 Mirai Botnet은 수십만 IoT 기기를 감염시켜,DNS 서비스 제공자 Dyn에 대규모 DDoS를 수행하여Twitter, Netflix, Reddit 등 주요 웹사이트를 마비시켰다. DDoS 공격은 범죄적인 Leroy 하지만,防御 측도 다층적 방어 체계 구축이 필수적이다.

**비유**: DDoS 공격은 **갑자기 수만 명의 사람들이 한 가게에殺到하여 正当な利用客이 들어올 수 없게 하는 것**과 같다. 가게 앞에 갑자기 사람들이殺到하면, 점원은 누가 진짜 고객인지 구분할 수 없어 영업을 계속할 수 없다. DNS Amplification 공격은「수천 개의 우체국에 가짜 우편물을 전달하고, 그_RESPONSE를 희생된 우체국에 보내게 하는」공격과 같다.

**등장 배경**: DDoS 개념은 1996년~2000년경 인터넷에서 처음 모습을 드러냈으며, 이후 지속적으로高度化되어 왔다. 2000년대: SYN Flood, UDP Flood, 2010년대: DNS Amplification, Application Layer Flood, 2020년대: Mirai(IoT Botnet), Ransom DDoS 등 다양해졌다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### DNS Amplification 공격

DNS Amplification 공격은 DNS의 질의-응답 비대칭성(작은 요청, 큰 응답)을悪用한다. 공격자는偽装된 출발지 IP(희생자의 IP)로 DNS Query를 보내고,権威 DNS Server는 해당 IP로 큰 응답을 보내 희생자를洪水한다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    DNS Amplification 공격 과정                           │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【공격 구조】                                                         │
│                                                                       │
│        [Botnet]                                                       │
│       Zombie PC들                                                      │
│           │                                                           │
│           │ ① 작은 DNS Query (예: ANY records)                        │
│           │    출발지 IP → 희생자 IP ( Spoofed)                        │
│           ▼                                                           │
│     ┌─────────────┐                                                    │
│     │ 중간 DNS    │ resolver들                  ┌──────────────────┐    │
│     │ resolvers   │◀────── ② Query ──────────│  희생자 IP       │    │
│     └─────────────┘                             │  (Target)       │    │
│           │                                     └──────────────────┘    │
│           │ ③ 큰 DNS Response (수 KB~수십 KB) ◀─                     │
│           │    출발지: DNS Server                                    │
│           │    목적지: 희생자 IP                                      │
│           │                                                            │
│           │ (수천 개 DNS Server × 수십 대 Botnet = 수십 Gbps ~ 수백 Gbps)   │
│           ▼                                                            │
│  【Amplification Factor】                                              │
│                                                                       │
│  • DNS Request: ~50 바이트                                             │
│  • DNS ANY Response: ~4,000 바이트 (기본)                              │
│  • DNSSEC signed large response: ~10,000+ 바이트                      │
│  • Amplification Factor: 약 50~200배                                  │
│                                                                       │
│  예시:                                                                 │
│  • 공격자: 10Gbps 의 Botnet 트래픽                                     │
│  • DNS Server 응답: 100배 증폭                                         │
│  • 희생자: 1Tbps 의 트래픽 수신 →帯域幅 逼迫 → 서비스 마비              │
│                                                                       │
│  【防御 방법】                                                          │
│  • DNS Server에서 IP Spoofing 방지 (uRPF)                             │
│  • DNS Response Rate Limiting (RRL)                                   │
│  • Anycast로 공격 트래픽 분산                                          │
│  • DDoS Mitigation Service 활용                                        │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** DNS Amplification 공격의 핵심은「IP Spoofing」이다. UDP 기반 DNS Query는 출발지 IP를spoof하기 쉽다. 공격자가 희생자의 IP를 출발지로 설정하면, DNS Server의 응답이 희생자에게 집중된다. amplification factor가 크면 클수록(예: DNSSEC 서명된 큰 응답), 적은 공격자 트래픽으로 대규모 피해가 가능하다.因此、 DNS Server 운영자는 IP Spoofing 방지와 RRL(Response Rate Limiting)을 필수적으로 적용해야 한다.

### 주요 DDoS 공격 유형

| 유형 | 대상 | 특징 | 방어 |
|:---|:---|:---|:---|
| **SYN Flood** | 서버 | TCP SYN만 보내고ACK 기다리지 않음 | SYN cookies, 증가 |
| **UDP Flood** | 네트워크 | 대량 UDP 패킷 전송 | Rate Limiting |
| **HTTP Flood** | 애플리케이션 | 정상 HTTP 요청 대량 전송 | CAPTCIA, JS Challenge |
| **DNS Amplification** | DNS Server | 작은 요청 × 큰 응답 | RRL, Anycast |
| **NTP Amplification** | NTP Server | monlist 쿼리 활용 | NTP 버전 업그레이드 |
| **Memcached Amplification** | Memcached | 큰 값을 작은 요청으로 | UDP 포트 비활성화 |

### DDoS 방어 메커니즘

```
┌───────────────────────────────────────────────────────────────────────┐
│                    DDoS 방어 체계                                         │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【1단계: 네트워크 경계】                                               │
│  • Rate Limiting: 특정IP/프로토콜당 트래픽량 제한                       │
│  • uRPF (Unicast Reverse Path Forwarding): IP 스푸핑 검증             │
│  • ACL (Access Control List): 불필요한 프로토콜/포트 차단              │
│                                                                       │
│  【2단계: Anycast/CDN】                                                │
│  • Anycast: 동일한IP를전 세계 여러 서버에 광고 → 공격 분산              │
│  • CDN: 캐시로 직접 콘텐츠 제공하고, 공격 트래픽을 Origin에 도달 전에 차단  │
│  • Cloudflare, Akamai, AWS CloudFront 등                              │
│                                                                       │
│  【3단계: DDoS Mitigation Service】                                     │
│  • 트래픽을scrubbing center로 전환 → 정화 후 정상 트래픽만 전달        │
│  • Prolexic, Radware, Cloudflare (DDoS Protection) 등                  │
│  • 공격 규모가帯域幅을 超える 경우 → 희생자IP을 블랙홀(Null Route)       │
│                                                                       │
│  【4단계: 애플리케이션 레벨 방어】                                       │
│  • CAPTCHIA/JS Challenge: 봇 vs 정상 이용자 구분                      │
│  • Rate Limiting: 특정 API endpoint당 요청 수 제한                      │
│  • WAF (Web Application Firewall): 애플리케이션 계층 공격 방어          │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** DDoS 방어는多層防御(Defense in Depth)가 원칙이다. 네트워크 경계에서의 기본 Rate Limiting과 ACL이 첫防壁이고, Anycast/CDN이攻撃トラフィックを分散시킨다. 그래도 해결되지 않으면 전문 DDoS Mitigation Service가traffic을분석하고 악성 패킷을 솎아낸다. 애플리케이션 계층 공격에는 WAF와 CAPTCHA 등으로 대응한다. 효과적인 DDoS 방어를 위해서는攻撃규모에 맞는 적절한 방어 단계의 조합이 필요하다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### DNS DDoS 방어 기술 비교

| 기술 | 동작 | 적용 위치 | 한계 |
|:---|:---|:---|:---|
| **RRL** | 동일 destination에 대한 반복 응답을 제한 | DNS Server | 소규모 공격에 효과 |
| **Anycast** | 다중 서버에 동일IP 광고 | 네트워크 레벨 |帯域幅 기반 공격에 효과 |
| **DNSSEC** | 응답 서명 → 위조/변조 탐지 | DNS Protocol | amplification 자체는 못 막음 |
| ** Rate Limiting** | IP/프로토콜당 트래픽량 제한 | 네트워크 장비 | 정상 트래픽도 영향 가능 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 1 — DNS Server DDoS 방어**:権威 DNS Server를 운영하는 경우, Bind의 Rate Limiting, Knot DNS의 Response Rate Limiting을 활성화한다. Anycast를 활용하여攻撃트래픽을分散시킨다. Cloudflare, Akamai 등의 DNS 서비스利用도 고려한다. 공격 발생 시, DNS 쿼리 패턴을분석하여特定域名만 응답하도록 임시 설정한다.

**시나리오 2 —DNS Cache Poisoning 방어**: DNS Cache Poisoning(파밍 공격)은 공격자가 DNS 응답을조작하여利用자를 가짜 网站로誘導한다. 방어 방법: DNS 응답의 UDP 소스 포트 검증(0이 아닌随机 포트),_QUERY ID 랜덤화, DNSSEC 적용으로 응답 무결성 검증. Windows Server 2016+는 randomized UDP source port를기본 제공한다.

### 도입 체크리스트

- **기술적**: DNS Server에 RRL 활성화, DNSSEC 적용, Anycast/CDN 활용
- **운영·보안적**: DDoS 대응 매뉴얼 수립, ISP와 DDoS Mitigation Service 연동 체계, 정기적인 대응訓練

### 안티패턴

- **DNS Server의 과도한放任**: 외부에서 아무 DNS 쿼리나 수락하면 amplification 공격에悪용될 수 있다._authoritative DNS는 재귀적 질의를 수락하지 않도록 설정해야 한다.
- **ISP 네트워크 차단**: DDoS 공격 시 ISP가 희생자IP를 Null Route하면 공격은 멈추지만 정상 서비스도 마비된다. 사전에 DDoS Mitigation Service 연동을 맺어두어야 한다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

DDoS 공격 규모는 매년 증가하고 있으며, 1Tbps를 넘는 공격도보고되고 있다. IoT 기기의 확산으로 Botnet 규모가 더 커지고, Ransom DDoS(恐喝 목적)도 증가하고 있다. 반면 AI 기반 DDoS 탐지/방어 기술도 발전하고 있으며, Zero Trust Architecture와 결합한 종합적 보안 체계가 주목받는다.

### 참고 표준

- RFC 5358 — DNS Response Rate Limiting (RRL)
- RFC 2827 — Network Ingress Filtering
- NIST SP 800-177 — Trustworthy Email

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Botnet** | 감염된 컴퓨터들의 네트워크로, DDoS 공격의 출발점이 된다. |
| **Amplification** | 작은 요청으로 큰 응답을 유도하는 공격 기법이다. |
| **Anycast** | 동일IP를다중 서버에 광고하여 트래픽을分散시키는 기법이다. |
| **RRL** | DNS Server에서 동일 destination에 대한 반복 응답을 제한하는 기법이다. |
| **Scrubbing Center** | DDoS 트래픽을分析하여 악성 패킷을 제거하는 전문 서비스이다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. DDoS 공격은 **갑자기 수만 명의 사람들이 카페에殺到해서, 진짜 손님이 들어올 수 없게 하는 것**과 같아요. 한 명이 아니고 엄청 많은 사람들이 동시에殺到하니까, 누가 진짜 손님인지 구별할 수 없어요.
2. DNS Amplification은 **数名の 악당들이「여기서 많이 시식해 주세요」라고 속여서, 도도Thousands의 사람들이 희생자의 집에殺到하게 하는 거예요. 한 통의 전화로 Thousands의 택배가殺到하는 거죠.
3. 그래서！カフェ에서는「한 사람당 한 번만 주문 가능」이라는 규칙을 정해두고 (Rate Limiting),警察( DDoS Mitigation Service)의 도움을 받아서, 진짜 손님과 공격자를 구별해야 해요!
