+++
title = "278. Thread 프로토콜"
weight = 278
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Thread는 Google(当时的 Nest Labs)가 주도하여 2014년에 도입한 **IPv6 기반 저전력 무선 Mesh 네트워크 프로토콜**로, IEEE 802.15.4 (2.4GHz, 250kbps) 물리층 위에 IPv6 스택을 올려 **"인터넷에 직접 연결되는 IoT Mesh 네트워크"**를実現합니다.
> 2. **가치**: Thread의 가장 큰 혁신은 **"Border Router 외에는 Gateway/Hub가 필요 없다"**는 점입니다. 각 Thread 노드가 직접 IPv6로 인터넷에 접근하여 클라우드 서비스와原生적으로 연동됩니다.
> 3. **융합**: Thread는 **Matter 스마트홈 표준의 唯一한 무선 전송 계층(Transport Layer)**으로 채택되어, Matter의 가장 중요한 技术基础设施 역할을 하며, 지그비/Thread/BLE/Wi-Fi 모두를 통합하는 스마트홈의 lingua franca가 될 전망입니다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

Thread는 Google 산하 Nest Labs에서 2014년에 도입한 **IPv6 기반 저전력 무선 Mesh 네트워크 프로토콜**입니다. Thread Group(결성된 업계 컨소시엄)이 표준을管理하며, Qualcomm, Apple, Amazon, Samsung 등 570개 이상의 기업이 참여하고 있습니다.

Thread의 설계 목표는 단순합니다: **"저전력, IPv6 기반, Mesh 네트워크를 스마트홈에 제공한다."** 이를 위해 Google은 이미 스마트홈에서 활용되던 기술(Jennic, OpenThread)을 기반으로 직접 개발했으며, 이후 Nest Hub, Nest Learning Thermostat 등 제품에率先 적용되었습니다.

### Thread vs Zigbee — 設計 철學의根本的 차이

```
┌──────────────────────────────────────────────────────────────┐
│              Thread vs Zigbee — IP 기반 vs 독자적 프로토콜                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [Zigbee — 독자적 프로토콜 스택]                                   │
│   ┌──────────────────────────────────────────────────────┐  │
│   │  Application  │ Proprietary Cluster Library (ZCL)  │  │
│   │  Network     │ AODV (독자 라우팅)                  │  │
│   │  MAC        │ IEEE 802.15.4                        │  │
│   │  Physical    │ 2.4 GHz                             │  │
│   └──────────────────────────────────────────────────────┘  │
│   → 인터넷 연동: Gateway 필수 (별도 변환 필요)                   │
│                                                              │
│  [Thread — IPv6 기반 스택]                                        │
│   ┌──────────────────────────────────────────────────────┐  │
│   │  Application  │ Matter / OpenThread Application    │  │
│   │  Network     │ IPv6 / Thread RPL (Routing)          │  │
│   │  MAC        │ IEEE 802.15.4                        │  │
│   │  Physical    │ 2.4 GHz                             │  │
│   └──────────────────────────────────────────────────────┘  │
│   → 인터넷 연동: **Border Router만으로 直接 IPv6**              │
│                                                              │
│  🌟 핵심: Thread = IEEE 802.15.4 + IPv6 + Mesh Routing       │
│     즉, Thread는 IEEE 802.15.4 "위에" IPv6를 포팅한 것!          │
└──────────────────────────────────────────────────────────────┘
```

### Thread Group의 창설 멤버들

Thread는 2014년 Google이 도입했으나, 2015년경 **Thread Group**이 결성되어 산업 컨소시엄으로 발전했습니다:

| founding member | 주요 역할 |
|:---|:---|
| **Nest Labs (Google)** | 프로토콜 개발 주도, OpenThread 오픈소스 |
| **ARM** | 디바이스 칩 설계 (Cortex-M) |
| **Silead** | 보안 칩 설계 |
| **Qualcomm, TI, Silicon Labs** | Thread 칩 공급 |
| **Samsung, Yale** | 스마트홈 기기 적용 |
| **Apple, Amazon** | 플랫폼 연동 |

- **📢 섹션 요약 비유**: Thread의 IPv6 기반 설계는 **"전 세계 모든 집이 같은 우편 번호를 가진다면"**과 같습니다. Zigbee는 각 동네마다 독자적인 주소 체계를 가지고 있어, 다른 동네 우체부(다른 프로토콜)가 편지를 배달하려면 **"동네 간 중계 담당 (Gateway)"**을 반드시 거쳤습니다. Thread는 **"전 세계 통합 주소 체계(IPv6)"**를 도입하여, 어떤 동네에서 보내든 **별도의 중계자 없이** 전 세계 어디든 직접 배달됩니다. 이로 인해 중간에 중계자가 없으므로 **배달 속도가 빨라지고, 중계자 고장 시 배달 실패 위험이 없어집니다**.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Thread 프로토콜 스택 — IPv6 Native

```
┌──────────────────────────────────────────────────────────────┐
│                 Thread 프로토콜 스택 구조                                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [Application Layer]                                         │
│   ┌──────────────────┐  ┌──────────────────┐            │
│   │ Matter Protocol   │  │ OpenThread       │            │
│   │ (CSA 관리)        │  │ Application      │            │
│   └────────┬─────────┘  └──────────────────┘            │
│            │                                                  │
│  [Transport Layer]                                          │
│   ┌──────────────────┐  ┌──────────────────┐            │
│   │   UDP             │  │    TCP           │            │
│   └────────┬─────────┘  └──────────────────┘            │
│            │                                                  │
│  [Network Layer]                                            │
│   ┌─────────────────────────────────────────────────────┐ │
│  │           IPv6 (Internet Protocol version 6)            │ │
│  │                  (Native IPv6 Stack)                  │ │
│  │             + Thread RPL (Mesh Routing)               │ │
│  └──────────────────────────┬────────────────────────────┘ │
│                              │                               │
│  [MAC + Physical Layer]                                       │
│   ┌─────────────────────────────────────────────────────┐ │
│  │          IEEE 802.15.4 (2.4 GHz, 250 kbps)           │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                              │
│  🌟 핵심: Thread 노드는 "IPv6 호환 기기"로 동작하여,             │
│     별도의 주소 변환(NAT) 없이도 인터넷과直接通信 가능!            │
└──────────────────────────────────────────────────────────────┘
```

### Thread Mesh 라우팅 — RPL 프로토콜

Thread는 네트워크 라우팅에 **RPL(IPv6 Routing Protocol for Low-Power and Lossy Networks)**을 채택합니다. RPL은 IoT 환경에 최적화된 Distance Vector 라우팅 프로토콜로, 다음과 같은 특성이 있습니다:

| RPL 특성 | 설명 |
|:---|:---|
| **DIO/DIS/DAO 메시지** | 라우팅 정보 교환을 위한 3가지 ICMPv6 메시지 |
| **DIO (DIO Object)** | 라우팅 메트릭 정보를广播 |
| **DAO (Destination Advertisement Object)** | 목적지 정보를 상위 노드에送信 |
| **Path Cost** |hop count + link quality 기반 최적 경로 선택 |
| **DIO flooding** | 네트워크 전체에 대한拓扑 정보传播 |

```
┌──────────────────────────────────────────────────────────────┐
│              Thread RPL 라우팅 — DODAG (Destination-Oriented DAG)              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                         ┌──── ROOT (Border Router)          │
│                         │  (Internet에 直接 연결)              │
│                         │                                    │
│                         │  DIO Flooding                     │
│                         ▼                                    │
│                     ┌────┴────┐                              │
│                    (Router A) (Router B)                    │
│                    /    |     \                             │
│                   /     |      \                            │
│               (Node C) (Node D) (Node E)                   │
│                                                              │
│  ※ DODAG (Destination-Oriented DAG):                       │
│   - Root( Border Router)부터 leaf 노드까지 트리 형태 구성         │
│   - 각 노드는 Parent/Child 관계로 계층화                       │
│   - 데이터는 Root 방향으로 상향으로 흐름                       │
│                                                              │
│  🌟 Thread 노드는 항상 1개 이상의 Parent을 가지고,               │
│     모든 Communication은 Router/Root 경유                    │
└──────────────────────────────────────────────────────────────┘
```

### Thread 노드 유형 — 3가지 역할

| 노드 유형 | 설명 | Router 가능 | 전원 |
|:---|:---|:---|:---|
| **Full Thread Device (FTD)** | 모든 Thread 기능 지원, Router 역할 가능 | ✅ | 무조건 전원 필요 |
| **Minimal Thread Device (MTD)** | Router 불가능, End Device 역할만 | ❌ | 배터리 가능 |
| **Border Router** | Thread ↔ Wi-Fi/Ethernet/IPv6 네트워크 간 게이트웨이 | ✅ | 무조건 전원 필요 |

### Thread의 6lowpan — IPv6의 IEEE 802.15.4 적용

Thread의 핵심 Enabling 기술 중 하나는 **6LoWPAN (IPv6 over Low-Power Wireless Personal Area Networks)**입니다. IEEE 802.15.4의 최대 프레임 크기(127바이트)에는 IPv6 헤더(40바이트)가 直接 담기엔 너무 큽니다. 6LoWPAN은 이를 해결하기 위해 **헤더 압축(Hierarchical Header Compression)**과 **단편화(Fragmentation)**를 적용합니다.

- **📢 섹션 요약 비유**: Thread의 IPv6 + 6LoWPAN 적용은 **"국제 우편 규약"**과 같습니다. 전 세계 우편 규정(IPv6)이 定착되어 있어 모든 나라에서統一 주소 체계를 사용하지만, 각国の郵政 network( IEEE 802.15.4)가 定着自己的信封尺寸(프레임 크기)에 제한があります. 各국의 우편 규약에서는大きな 国际小包를 해당 国size에 맞게 分解脱着小包로 분할하고(단편화), 信封면)에 필요한情報만 간소하게 기재하는 규칙(헤더 압축)을 정했습니다. Thread도 마찬가지 — IPv6의 모든 주소 정보를 802.15.4 네트워크에서 효율적으로 전송하기 위해 6LoWPAN이 **"국제 소포를国内小包로 분할하고,封筒에 필요한情報만 간소하게 기재"**하여 전송합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### Thread vs Zigbee vs Wi-Fi — 스마트홈 프로토콜 비교

| 구분 | Thread | Zigbee | Wi-Fi |
|:---|:---|:---|:---|
| **IP 기반** | ✅ **IPv6 Native** | ❌ (독자적) | ✅ (IPv4/IPv6) |
| **Gateway 필요** | Border Router만으로 충분 | **Coordinator/Gateway 필수** | AP만으로 충분 |
| **데이터 속도** | 250 kbps | 250 kbps | **54 Mbps~** |
| **전력 소비** | **Ultra Low** | 低 | 高 |
| **Mesh 지원** | ✅ Native | ✅ Native | ✅ (메쉬 모델) |
| **Matter 호환** | ✅ **主要 전송 계층** | ✅ (Matter 패널링) | ✅ |
| **인터넷 연동** | Border Router로 직접 | Gateway 필수 | AP로 직접 |

### Thread vs Bluetooth Mesh — Mesh 비교

| 구분 | Thread | Bluetooth Mesh |
|:---|:---|:---|
| ** alaplication层** | IPv6 (표준 인터넷) | 독자적 (Generic Attribute Profile) |
| **네트워크規模** | 수백 개 노드 | **수만 개 노드** |
| **라우팅** | RPL ( Distance Vector) | Managed Flooding (관리된 flood) |
| **패킷 크기** | IEEE 802.15.4 (128B) | BLE (37B advertising) |
| **주요 용도** | 스마트홈 (특히 Matter) | 빌딩 automation, 산업 |

### Matter — Thread의 Killer App

**Matter**는 CSA(Connectivity Standards Alliance, 전身 Zigbee Alliance)가 관리하는 **새로운 스마트홈 표준**이며, Thread는 Matter의 **主要 전송 계층(Major Transport)**으로 채택되었습니다:

```
  ┌──────────────────────────────────────────────────────────────┐
  │              Matter 프로토콜 — Thread/Wi-Fi/BLE 위에서 동작                        │
  ├──────────────────────────────────────────────────────────────┤
  │                                                              │
  │                     ┌─────────────────┐                       │
  │                     │  Matter Device  │                       │
  │                     │  (애플리케이션)   │                       │
  │                     └────────┬────────┘                       │
  │                              │                                │
  │                     ┌────────▼────────┐                       │
  │                     │  Matter Stack   │                       │
  │                     │  (공통 애플리케이션 레이어)               │
  │                     └────────┬────────┘                       │
  │                              │                                │
  │         ┌────────────────────┼────────────────────┐        │
  │         │                    │                    │        │
  │         ▼                    ▼                    ▼        │
  │  ┌────────────┐    ┌────────────┐    ┌────────────┐       │
  │  │   Thread   │    │   Wi-Fi    │    │    BLE     │       │
  │  │ (Primary)  │    │ (Fallback) │    │ (Paring)  │       │
  │  └────────────┘    └────────────┘    └────────────┘       │
  │                                                              │
  │  🌟 Matter Device는 우선 Thread으로 연결을 시도하고,           │
  │     실패 시 Wi-Fi로, Pairing 시 BLE로 연결됩니다.            │
  └──────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Thread와 Matter의 관계는 **"고속도로와 고속버스"**와 같습니다. 고속도로( Thread)는 차(데이터)가 이동하는 **물리적 infrastructure**이고, 고속버스( Matter)는 그 highway를 **어떤公司的 버스坐着運行하는가**를定한 규칙입니다. 버스회사가 바뀌더라도( Matterを構成する企业 달라져도) highway 위에서运行的 버스(データ)의 基本 движение 원칙은 변하지 않습니다. 그리고 高性能な 버스( Thread bus)에는 全회사의 버스가 탈 수 있는 것처럼(상호운용성), Matter 생태계에 속한 기기는 어느 회사의 Matter 기기와도 연동됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실전 시나리오 — Google Nest Hub와 Thread

Google Nest Hub (2nd gen)는 Thread Border Router 기능을탑재하고 있어, Nest Hub에 직접 연결된 Thread 기기들이 Wi-Fi 네트워크 없이도 인터넷에 연결됩니다:

- **연결 방식**: Nest Hub (Border Router) → Thread Mesh → Thread 기기들 (Nest Learning Thermostat, Nest Protect 등)
- **동작**: Nest Thermostat가 Nest Hub의 Thread Border Router를 통해 직접 IPv6으로 클라우드 서비스와通信. 별도의 Thread Coordinator나 Gateway가 필요 없습니다.
- **判断**: Thread의 가장 큰 강점이 드러나는 사례입니다. **"Hub가 반드시 필요한 것은 아니다"** — Border Router만 있으면 나머지 노드들이 자율적으로 Mesh를 구성하고 인터넷에 연결됩니다.

### 실전 시나리오 — Matter + Thread 스마트홈

Matter-compatible한 스마트 조명 시스템을 구축하는 경우:

- **기기**: Philips Hue (Zigbee, Matter 펌웨어 지원), Eve Energy (Thread), Apple HomePod mini (Thread Border Router)
- **연결**: HomePod mini가 Thread Border Router로 동작하며, Thread 기기들과 Matter 네트워크를 동시에管理. Hue 조명도 Matter 펌웨어를 받아 Hue Bridge를 통해 Matter에 연동
- **사용자 경험**: Apple Home 앱에서 Hue 조명, Eve 에너지 센서, Thread 센서를 ** unified Interface로 제어**
- **判断**: Matter의 핵심 가치는 이러한 **상호 연동성**입니다. 어느 회사의 기기든, 어느 플랫폼이든 unified하게 연동되는 것이 Matter의 목표입니다.

### 설계 시 체크리스트

1. **Border Router 확보**: Thread 기기만으로는 인터넷에 직접 연결할 수 없습니다. 반드시 **Border Router(AP, smartphone, HomePod 등)**가 필요합니다
2. **Router/End Device 분리**: 저전력 기기(배터리)는 **Minimal Thread Device(MTD/End Device)**로 설정하여 라우팅 부담을 줄입니다
3. **네트워크 규모**: Thread는 일반적으로 **수백 개 노드**에 적합합니다. 수천 개 이상의 노드가 필요하다면 Bluetooth Mesh가 더 적합합니다
4. **Matter 전환**: 신규 설계에서는 Matter-compatible Thread 칩을 선택하여 향후 Matter 생태계에 편하게 통합되도록 합니다

- **📢 섹션 요약 비유**: Thread의 Border Router 구조는 **"국제 우대 여행 패스"**와 같습니다. 어느 국제机场에 입국하려면 **"여권(IPv6 호환 기기)"**이 있어야 하고, **"입국 심사대(Border Router)"**를 통과해야 합니다. 일단 심사대를 통과하면( Border Router 경유)境内의 어디든 편하게 이동할 수 있습니다( Thread Mesh 내 통신). 다만 입국 심사대가 없으면( Border Router 없음) 국제旅行者(Thread 노드)는境外(인터넷)에 出입할 수 없습니다. 그래서 Thread 네트워크에는 **반드시 최소 1개의 Border Router**가 필요하며, 이것이 없으면 Thread 노드는 **"여권은 있지만 입국 심시가 없는 섬에 갇힌旅行者"**와 같은处境에 놓입니다.

---

## Ⅴ. 기대효과 및 결론

### Thread 도입의 기대효과

| 구분 | Zigbee 기반 | Thread 기반 | 개선 효과 |
|:---|:---|:---|:---|
| **인터넷 연동** | Gateway 필수 (별도 비용) | Border Router로 직접 | **장비 비용 절감** |
| **상호운용성** | 벤더 독자적 | **Matter 호환으로 全社 상호연동** | **에코시스템 확대** |
| **개발 난이도** | 독자적 스택, Gateway 개발 필요 | **표준 IPv6 활용** | **개발 시간 단축** |
| **보안** | 네트워크 키 공유 모델 | **IPv6 IPsec 활용** | **보안 강화** |
| **확장성** | 제한적 | **수백 개 노드** | **대규모 네트워크** |

### 결론 및 전망

Thread는 **"IoT의 IPv6 전환"**을 의미합니다. 기존의 독자적 스택(Zigbee)이各自의 규칙으로 통신하던 것과 달리, Thread는 **표준 IPv6 위에 구축**되어, 네트워크 레벨에서 이미 검증된 기술(IPv6, TCP/UDP, TLS)을 그대로 활용합니다. 이것이 개발자들에게 **"배우는 것이 적다"**는 것을意味하며, 결과적으로 **더 빠른 개발, 더 낮은 비용, 더 높은 상호운용성**으로 이어집니다.

Matter의 등장과 함께 Thread는 스마트홈의 **사실 상 전송 표준**으로 자리잡을 전망입니다. 2024년 이후 출시되는 대부분의 新規 스마트홈 기기는 Matter를 지원할 것이며, 그 기기들中 많은 수가 Thread를 전송 계층으로 활용할 것입니다.

> **결론**: Thread는 스마트홈의 **"표준화 선구자"**입니다. 기존의 독자적 프로토콜各自的izard城堡를 쌓던 것과 달리, Thread는城门을 열어 **표준 IPv6라는 International Street**에 연결했습니다. 그리고 Matter는 그 International Street을 **"统一된 Plaza(Matter)"**로拡張하여, 어느 나라 사람(기기의)이라도 들어와서交易(데이터 교환)할 수 있게 되었습니다. Thread의 가치를 超える 없음 — 全IoT 네트워크가 서로 연결되는 **"세번째 물결"**이 바로 Thread입니다.

- **📢 섹션 요약 비유**: Thread는 **"평화 통일의架道"**입니다. 남과 북이 독자적 철도 체계를 가지고 있어 서로 연결되지 않았다면, 통일后就京元 построены는 **"경의선 자동профиль( 标准 gauge)"**와 같습니다. Thread가 경의선이고( IEEE 802.15.4 기반), IPv6가표준 궤도이며(1435mm), Matter가 통일 이후 주파수로走る統一된 열차(데이터 포맷)입니다. 이제 열차는 어느 나라 궤도에서든 运行可能해집니다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 관련 개념 | 관계 설명 |
|:---|:---|
| **Matter** | CSA 관리 스마트홈 통합 표준. Thread, Wi-Fi, BLE 위에서 동작하는 애플리케이션 레이어 |
| **OpenThread** | Google이 오픈소스로 공개한 Thread 스택. GitHub에서 利用可能 |
| **Border Router** | Thread ↔ Wi-Fi/Ethernet/IPv6 간의 gateway. Thread 기기의 인터넷 연결 허가 |
| **6LoWPAN** | IPv6를 IEEE 802.15.4 네트워크에 적용하기 위한 헤더 압축·단편화 프로토콜 |
| **RPL (Routing Protocol for LLN)** | Low-Power and Lossy Networks용 IPv6 라우팅 프로토콜. Thread의 Mesh 라우팅에 활용 |
| **Zigbee** | Thread와 같은 IEEE 802.15.4 기반이나, 독자적 네트워크/애플리케이션 스택 사용. Matter Compatible |

---

## 👶 어린이를 위한 3줄 비유 설명

1. **Thread는 "국제 우편 시스템"**예요. 전 세계 어디서든 같은 우편 번호(IPv6)를 쓰면 어느 나라에서든 편지를 보낼 수 있어요. Zigbee는 각 동네마다 다른 우편 체계를 써서gateway(통역)가 있어야 했는데, Thread는 gateway가 거의 필요 없어요!
2. Thread에서는 **"여권을 가지고 있는 모든 사람이 Border Router(입국 심사대)"를 지나면 국제 통신**을 할 수 있어요. 각 기기가 "IPv6 여권"을 가지고 있으면 별도의 동네 중계인(Coordinator) 없이도 internet와直接 통신해요.
3. **Matter는 "전 세계 통합 우편 규약"**이에요. 이제 어느 나라 우체국이든, 어느 회사 택배이든, 같은 규약으로 편지를 보내면 받을 수 있어요. Thread 위에서 Matter 규약을跑하면 어느 기기든 서로 이야기할 수 있어요 — 이것이 **"스마트홈의 평화 통일"**이에요!
