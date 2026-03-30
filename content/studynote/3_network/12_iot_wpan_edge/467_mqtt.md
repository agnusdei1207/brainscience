+++
weight = 8
title = "MQTT (Message Queuing Telemetry Transport) 프로토콜"
description = "MQTT의 구조, QoS 수준, 발행-구독 모델, 브로커 역할, IoT messaging에서의 활약을شرح"
date = 2024-01-22

[extra]
categories = ["studynote-software-engineering"]
tags = ["mqtt", "iot", "messaging", "pub-sub", "protocol", "qos"]

+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MQTT는 발행-구독(Publish-Subscribe) 모델 기반의 경량 메시징 프로토콜로, TCP/IP 위에 구축되어 대역폭이 제한된 IoT(Internet of Things) 환경에서도 최소한의 오버헤드로 효율적으로 메시지를 전달할 수 있도록 설계되었다.
> 2. **가치**: MQTT는 브로커(Broker) 기반의 간접通信 구조를 통해 송신자와 수신자가 직접 연결되지 않아도 되어, 수천 개의 센서/액추에이터가 동시에 메시지를 주고받을 수 있는 확장성(scalability)을 제공한다.
> 3. **융합**: MQTT는 클라우드 플랫폼(AWS IoT Core, Azure IoT Hub, Google Cloud IoT)과紧密结合되어 있으며, 최근 MQTT 5.0에서 Session Present와 공유 구독(Shared Subscription) 기능이 추가되어 enterprise 수준의 기능이 강화되었다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념

MQTT(Message Queuing Telemetry Transport)는 1999년 IBM의 Dr. Andy Stanford-Clark과 Arcom(지금은 Eurotech)의 Arlen Nipper가 석유 파이프라인 모니터링을 위해 설계한 메시징 프로토콜이다. 핵심 설계 목표는 저대역폭, 고지연, 불안정 네트워크 환경에서도 동작하는 신뢰할 수 있는 메시징이었다. HTTP의 요청-응답(Request-Response) 모델과 달리, MQTT는 발행-구독(Pub-Sub) 모델을 채택하여 송신측과 수신측의 결합(coupling)을 줄였다.

### 필요성

기존 HTTP/RESTful 방식은 각 센서가 중앙 서버에 직접Polling해야 하므로, 센서가 수천 개로 증가하면 서버 부하와 네트워크 트래픽이 폭발적으로 증가하는 문제(Fan-out problem)가 있었다. 또한 센서는 배터리 수명을 연장하기 위해 평소에 연결을 유지하지 않고 필요한 순간만 Wake-up해야 하므로, HTTP의 연결 수립 오버헤드(三次 рукопожатия)는致命的이었다.

### 등장 배경

MQTT의最初の版本(MQTT v3.1)은 2010년 Apache ActiveMQ에 공개적으로 발표되었고, 2014년 OASIS(Organization for the Advancement of Structured Information Standards)에 의해 표준화되었다. 이후 2017년 MQTT 5.0이正式リリース되어 클러스터링 지원, 사용자 속성(User Properties),否认reason 등 enterprise 기능이 추가되었다. 현재 MQTT는 50%+ 시장 점유율을 가진 IoT messaging 표준으로 자리매김했다.

### 💡 비유

MQTT는 **"우체국 시스템"** 에 비유할 수 있다. 기존의 우편(REST/HTTP)은 발신인이 각 수취인에게 직접 편지를 배달해야 했지만, MQTT는 중앙 우체국(브로커)을 통해 모든 편지를集中管理하고, 각 가정에서는 필요한 종류의 편지만 사서함에서 찾아보는 구조이다. 발신인은 누군가에게 보낸 것인지 알 필요 없이 우체국에 던지기만 하면 되고, 수신인도 누가 보냈는지 몰라도自己所 interesse하는 정보만 읽으면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### MQTT 구성 요소

MQTT 시스템은 Publisher, Broker, Subscriber 3가지 핵심 구성 요소로 이루어진다. Publisher(발행자)는 센서나 디바이스로서 데이터를 생성하여 브로커에 전송하고, Subscriber(구독자)는 관심 있는 주제의 메시지를 브로커로부터 수신하며, Broker는 발행자와 구독자 사이에서 메시지를 라우팅하는 중앙 허브 역할을 한다.

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Publisher (발행자)** | 센서/디바이스에서 데이터 생성 | 토픽(Topic)을 지정하여 브로커에 메시지 발행 | 센서, MCU, 임베디드 장치 | 신문사 |
| **Subscriber (구독자)** | 관심 토픽 메시지 수신 | 브로커에 구독 요청, 토픽 기반 필터링 | 앱, 클라우드 서비스, 제어 시스템 | 구독자 |
| **Broker (브로커)** | 메시지 라우팅, QoS 처리 | 토픽 관리, 구독자 목록 유지, 메시지 전달 | Mosquito, HiveMQ, EMQ | 우체국 |
| **Topic (토픽)** | 메시지의 논리적 주소 체계 | /-separated 계층 구조 (예: home/living/temp) | MQTT的灵魂 | 우편 번호 |
| **QoS (서비스 품질)** | 메시지 전달 보장의 세 수준 | At most once (0), At least once (1), Exactly once (2) | 메시지 신뢰성 레벨 | 등기/일반 우편 |

---

### 발행-구독 모델 동작

MQTT의 발행-구독 모델에서 가장 중요한 개념은 토픽(Topic)이다. 토픽은 /로 구분된 계층적 문자열로, 예컨대 building/floor1/room1/temperature와 같은 형태를 갖는다. Publisher는 특정 토픽에 메시지를 발행하고, Subscriber는 특정 토픽 패턴을 구독함으로써 관심 있는 메시지만 수신한다. 브로커는 이 매칭을 수행하여 해당 토픽을 구독한 모든 Subscriber에게 메시지를 전달한다.

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                 MQTT 발행-구독(Pub-Sub) 모델 동작 원리                         │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  [MQTT 아키텍처 개요]                                                    │
  │
  │      [Sensor A] ──PUBLISH──┐                                            │
  │      Topic: home/lv1/temp │                                            │
  │                            ▼                                            │
  │      [Sensor B] ──PUBLISH──┤                                            │
  │      Topic: home/lv2/temp ├──── [Broker] ──SUBSCRIBE──▶ [App 1]        │
  │                            │                      (home/lv1/+)          │
  │      [Sensor C] ──PUBLISH──┤                                            │
  │      Topic: home/kitchen ──┘                                            │
  │                                                                     │
  │      [App 2] ◀──SUBSCRIBE── [Broker] ◀──SUBSCRIBE── [Cloud]            │
  │      Topic: home/#          (home/kitchen)                            │
  │                                                                     │
  │  [토픽(Topic) 계층 구조]                                               │
  │
  │  home/                                                              │
  │  ├── livingroom/                                                    │
  │  │   ├── temperature ──────────── (Sensor: temp_lv1)                   │
  │  │   ├── humidity ────────────── (Sensor: hum_lv1)                    │
  │  │   └── light ───────────────── (Sensor: light_lv1)                 │
  │  ├── kitchen/                                                       │
  │  │   ├── temperature ──────────── (Sensor: temp_ktchn)                │
  │  │   └── gas ──────────────────── (Sensor: gas_detector)              │
  │  └── bedroom/                                                        │
  │      └── temperature                                                 │
  │                                                                     │
  │  [와일드카드 구독]                                                     │
  │  • + (단일 레벨): home/+/temperature → livingroom, kitchen, bedroom   │
  │                    의 모든 temperature 수신                           │
  │  • # (다중 레벨): home/# → home 아래 전체 토픽 수신                   │
  │
  │  [MQTT CONNECT/FLOW 절차]                                             │
  │
  │   Client ──────── CONNECT ────────────────▶ Broker                     │
  │   Client ◀─────── CONNACK ──────────────── Broker                      │
  │   │  (clientId, keepAlive, cleanSession, will, credentials)            │
  │   │                                                              │
  │   │  PUBLISH (topic, payload, QoS, retain, messageId)                │
  │   │ ───────────────────────────────────────────────────────────▶   │
  │   │  ◀── PUBACK ──────────────────────────────────────────────────   │
  │   │  (QoS 1 이상일 경우)                                             │
  │   │                                                              │
  │   │  SUBSCRIBE (topics, messageId)                                 │
  │   │ ───────────────────────────────────────────────────────────▶   │
  │   │  ◀── SUBACK ──────────────────────────────────────────────────   │
  │   │                                                              │
  │   │  PUBLISH ←── (토픽 매칭 구독자에게 전달) ──────────────────────   │
  │   │                                                              │
  │   │  PINGREQ ───────────────────────────────────────────────────▶  │
  │   │  ◀── PINGRESP ────────────────────────────────────────────────  │
  │   │  (keepAlive 주기마다, connection 유지를 위해)                    │
  │   │                                                              │
  │   │  DISCONNECT ────────────────────────────────────────────────▶   │
  │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** MQTT의 CONNECT에서 가장 중요한 파라미터는 clientId, keepAlive, cleanSession이다. clientId는 각 클라이언트를 구분하는 고유 식별자이고, keepAlive는 클라이언트가 브로커에게 alive임을 알리는 주기(초 단위)이며, cleanSession=true이면 연결 종료 시 구독/메시지가 모두 삭제되고, cleanSession=false이면 브로커가 Durable Subscription을提供하여 재연결 시에도 이전 메시지를 받을 수 있다. PUBLISH 메시지의 QoS 수준에 따라 메시지 전달 신뢰성이 결정되는데, QoS 0(At most once)는 네트워크 오류 시 메시지가 유실될 수 있고, QoS 1(At least once)은 중복 가능성이 있더라도 최소 1회는 전달이 보장되며, QoS 2(Exactly once)는 중복 없이 정확히 1회 전달을 보장하지만 latency가 가장 높다.

---

### QoS (Quality of Service) 수준

MQTT의 QoS는 네트워크 상태와 신뢰성 요구에 따라 3단계로 구분된다.

| QoS 수준 | 이름 | 전달 보장 | 네트워크 비용 | 사용 시나리오 |
|:---|:---|:---|:---|:---|
| **QoS 0** | At most once | 보장 없음 |最低 (1번 전송) | 일시적 데이터, 빠르게 전달 중요 |
| **QoS 1** | At least once | 최소 1회 |中等 (2번 왕복) | 중요하지만 중복 허용 환경 |
| **QoS 2** | Exactly once | 정확히 1회 |最高 (4번 왕복) | 결제, 중요 제어 명령 |

---

### MQTT 5.0 새로운 기능

MQTT 5.0은 2017년 출시되어 여러 enterprise 기능이 추가되었다.

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    MQTT 5.0 새로운 기능                                       │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  [Session and Delivery Enhancements]                                      │
  │
  │  ① Session Expiry Interval                                               │
  │     • CONNECT에서 cleanSession 대신 sessionExpiryInterval 지정           │
  │     • 연결 종료 후에도 session 정보 유지 시간 설정 가능                     │
  │     • 예: sessionExpiryInterval=3600 → 1시간 후 자동 삭제                 │
  │
  │  ② Message Expiry Interval                                               │
  │     • PUBLISH에서 messageExpiryInterval 지정                             │
  │     • 지정 시간內 미|delivery된 메시지는 자동 폐기                       │
  │     • 예: MQTT-SN에서 sensor 데이터의 시간敏感性反映                      │
  │
  │  ③ Reason Code & Reason String                                            │
  │     • CONNACK, PUBACK, SUBACK 등에詳細な 이유 코드 포함                   │
  │     • CONNECT 실패 시 원인 파악 용이                                        │
  │
  │  [Shared Subscription (공유 구독)]                                        │
  │
  │  $share/{share-name}/{topic-filter}                                       │
  │
  │  예: $share/sensors/home/lv1/temp                                        │
  │
  │   [Sensor A] ────PUBLISH──┐                                              │
  │                           ▼                                              │
  │   [Sensor B] ────PUBLISH──┤                                              │
  │                           ▼  [Broker]                                     │
  │   [Sensor C] ────PUBLISH──┤                                              │
  │                           ▼                                              │
  │   ┌─────────────────────────────────────────────────────┐               │
  │   │  공유 구독자 그룹                                    │               │
  │   │  [Worker 1] | [Worker 2] | [Worker 3]               │               │
  │   │  (메시지가 round-robin으로 분배, 부하 분산)          │               │
  │   └─────────────────────────────────────────────────────┘               │
  │
  │  [User Properties]                                                       │
  │  • PUBLISH 메시지에 key-value 메타데이터 첨부 가능                         │
  │  • 예: {"source": "temp_sensor", "location": "livingroom"]              │
  │  • 이를 통해 메시지 라우팅/필터링이 application 레벨에서 가능              │
  │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** MQTT 5.0의 가장 중요한 추가 기능 중 하나는 Shared Subscription이다. 기존 MQTT에서 한 토픽을 여러 Subscriber가 구독하면 모든 Subscriber가 동일한 메시지를 받지만, Shared Subscription에서는 $share/{group-name}/{topic} 형태로 구독하여 메시지가 그룹 내 Subscriber들에게 round-robin으로 분배된다. 이는 로드밸런싱이 필요한 대규모 데이터 처리 시스템에서 필수적이다. 예를 들어, 수백만 개의 센서가 데이터를 보내면 이를 여러 Worker instance가 나누어 처리하는 구조를 만들 수 있다. Session Expiry Interval은 cleanSession의 세분화된 버전으로, 연결 종료 후 session 정보를 얼마나 유지할지를精确하게 설정할 수 있어, 이동 환경에서 네트워크 일시 단절 시에도 session을 복원할 수 있다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### MQTT vs HTTP vs CoAP 비교

| 비교 항목 | MQTT | HTTP | CoAP |
|:---|:---|:---|:---|
| **모델** | Pub-Sub | Request-Response | Request-Response |
| **전송** | TCP | TCP | UDP |
| **오버헤드** | 2바이트 최소 | 수십 바이트 | 4바이트 최소 |
| **QoS** | 0/1/2 3단계 | 없음 (재시도) | 0/1 2단계 |
| **Bidirectionality** | 양방향, NAT超え | Pull only | 양방향 가능 |
| **대역폭 효율** | 높음 |낮음 | 매우 높음 |
| **주 용도** | IoT 센서/cmd | Web API | M2M, constrained |
| **보안** | TLS 지원 | TLS 지원 | DTLS 지원 |

### MQTT vs CoAP 용도 선택 가이드

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                  MQTT vs CoAP 선택 결정 트리                                  │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  [질문 1: 주 데이터 흐름이 어떤 형태인가?]                                  │
  │       │                                                               │
  │       ├─ "여러 센서가 중앙으로 보고" (Fan-out from sensors)            │
  │       │    → MQTT 선택 (Pub-Sub가 자연스러움)                          │
  │       │                                                               │
  │       └─ "중앙이 여러 디바이스를 제어" (Fan-in to actuators)           │
  │            → CoAP 선택 (Request-Response가 자연스러움)                  │
  │                                                               │
  │  [질문 2: 메시지 전달 신뢰성이 얼마나 중요한가?]                          │
  │       │                                                               │
  │       ├─ "정확히 1회 전달이 필수" (결제, 제어 cmd)                      │
  │       │    → MQTT QoS 2 선택                                          │
  │       │                                                               │
  │       └─ "가끔 유실되어도 괜찮음" (주변 환경 데이터)                      │
  │            → MQTT QoS 0 또는 CoAP 선택                                 │
  │                                                               │
  │  [질문 3: 네트워크 환경이 어떤가?]                                      │
  │       │                                                               │
  │       ├─ "안정적 TCP/IP 네트워크"                                       │
  │       │    → MQTT 또는 HTTP REST 중 선택                              │
  │       │                                                               │
  │       └─ "unstable, packet loss 높은 환경"                             │
  │            → CoAP (UDP 기반, 재전송 控制 가능)                          │
  │                                                               │
  │  [질문 4: 클라이언트 리소스 수준은?]                                    │
  │       │                                                               │
  │       ├─ "풍부한 리소스 (라즈베리파이 등)"                               │
  │       │    → MQTT 브로커에 연결 가능                                   │
  │       │                                                               │
  │       └─ "엄청난 constrained (8KB RAM MCU)"                           │
  │            → CoAP 선택 ( lebih 가벼운)                                │
  │                                                               │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** MQTT와 CoAP는 각각 다른 최적화 목표를 가지고 있다. MQTT는 Publish-Subscribe 모델의 특성상 다수의 센서가 중앙 허브에 데이터를 보고, 여러 소비자가 이를 구독하는 시나리오에 매우 적합하다. 브로커를 통해 메시지가 라우팅되므로 Publisher와 Subscriber가 서로를 알 필요가 없어 결합도가 낮고, 확장성이 우수하다. CoAP는 REST 모델에 가까우면서 UDP 기반으로 동작하여 오버헤드가 매우 작고, request-response 패턴이 중앙에서 디바이스를 제어하는 시나리오에 자연스럽다. 따라서 대규모 센서 데이터 수집(예: 기상 관측, 공장 센서 모니터링)에는 MQTT가 적합하고, 중앙에서 디바이스를 주기적으로 폴링하거나 제어하는 시나리오(예: 스마트 조명 On/Off)에는 CoAP가 적합하다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 공장 IoT 환경에서 MQTT 기반 데이터 수집**: 공장 환경에서 1,000개 이상의 센서(온도, 압력, 진동)가 MQTT를 통해 중앙 데이터 플랫폼에 데이터를 전송하려는 상황. 핵심 이슈는 브로커의 스케일링이다. 단일 브로커가 1,000개 이상의 연결을 처리해야 하므로, 브로커 클러스터링(clustering)이 필요하다. Mosquito, HiveMQ, EMQ 등 클러스터링을 지원하는 브로커를 선택하고, 메시지 throughput에 따라 브로커 인스턴스를水平 확장(scale-out)해야 한다. QoS 수준은 센서 유형에 따라 다르게 설정해야 한다 — 공정-critical 데이터는 QoS 2, 일반 모니터링 데이터는 QoS 0이 적절하다.

2. **시나리오 — MQTT를 활용한 대규모 원격 제어**: 스마트 그리드 환경에서 중앙 시스템이 10만 개의 스마트 미터를 제어(requiring time synchronization)하려는 상황. MQTT의 Publish-Subscribe 모델은 원래 데이터 수집에 유리하지만, 控制 명령을 전달할 때는 주의가 필요하다. Subscriber가 연결되어 있지 않으면 메시지가 유실될 수 있으므로, QoS 1 이상을 사용하고, Session Expiry Interval을 활용하여 제어 명령의有效期限을 설정해야 한다. 또한 retained 메시지를 활용하여 마지막 명령 상태를 유지하고, 미터가 재연결 시 최신 제어 명령을 받을 수 있도록 해야 한다.

3. **시나리오 — MQTT-SN 환경에서의 센서 네트워크**: 배터리 구동 센서 네트워크에서 MQTT-SN(MQTT for Sensor Networks)을 활용하려는 상황. MQTT-SN은 UDP를 기반으로 하며, 센서처럼 항상 연결을 유지할 수 없는 디바이스를 위해 designed되었다. 핵심 기능은 sleep 상태 지원으로, 센서가 sleep에서 깨어나서 PUBLISH하고 다시 sleep에 들어가는 방식이다. Broker와_gateway(SN) 사이에만 MQTT over TCP를 사용하고, 센서와 Gateway 사이에는 MQTT-SN over UDP를 사용하여, 센서의 에너지 소모를 최소화한다.

### 도입 체크리스트

- **기술적**: MQTT 브로커의 클러스터링/고가용성(HA) 구성이 수립되어 있는가? QoS 수준이 데이터 중요도에 따라 적절히 설정되어 있는가? Topic 구조가 확장성을 고려한 계층 구조로 설계되어 있는가?
- **운영·보안적**: MQTT over TLS(포트 8883) 또는 WebSocket over TLS(포트 443)를 사용하여 보안을 적용하고 있는가? 브로커에 접근 가능한 클라이언트를 authentication/authorization mechanism으로 제한하고 있는가?

### 안티패턴

- **토픽 구조 미설계**: 모든 메시지를 하나의 토픽에 쏟아부으면 구독자가 불필요한 데이터를 많이 받게 되어 네트워크 bandwidth가 낭비된다. 적절한 계층적 토픽 구조를 설계하고, 필요한 수준의 와일드카드 구독을 활용해야 한다.
- **QoS 2 과용**: QoS 2는 확실한 전달 보장이 있지만 4번의 왕복(PUBACK, PUBREC, PUBREL, PUBCOMP)이 필요하므로 latency가 높고 네트워크 비용이 크다. 실제로 QoS 0으로 충분한 일반 데이터에 QoS 2를 적용하면 불필요한 오버헤드가 발생한다.

- **📢 섹션 요약 비유**: MQTT의 발행-구독 모델은 **"잡지사-구독자"** 관계에 비유할 수 있다. 잡지사가 잡지를 발행(PUBLISH)하면, 해당 잡지를 구독한 사람들만 우편함을 통해 잡지를 받는다. 구독자는 누가 언제 잡지를 보냈는지 몰라도自己所 관심한 잡지만 받으면 된다. QoS는 우편 방법 선택에 비유할 수 있는데, 일반 우편(QoS 0)은 빠르지만 유실될 수 있고, 등기 우편(QoS 1)은 확실히 전달되지만 조금遅く, 그리고 빠른 등기(QoS 2)는 가장 확실하지만 비용이 크다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | HTTP Polling | MQTT QoS 0 | MQTT QoS 2 | 개선 효과 |
|:---|:---|:---|:---|:---|
| **정량** | 대역폭: 높음 (매번 전체 헤더) | 대역폭: 낮음 (2바이트 오버헤드) | 대역폭: 중간 | **75%+ 대역폭 절감** |
| **정량** | 지연: 50~200ms | 지연: 5~20ms | 지연: 20~50ms | **지연 70% 감소** |
| **정성** | 직접 연결, 결합 강함 | 브로커 간접, 결합 ↓ | 정확 전달 보장 | **확장성/신뢰성 향상** |

### 미래 전망

- **MQTT 5.0 확대 adoption**: Session Expiry, Shared Subscription 등 enterprise 기능의 추가로, 기존에 Kafka나 AMQP를 사용하던 기업 환경에서도 MQTT로 전환하는 사례가 증가하고 있다.
- **MQTT over QUIC**: IETF에서 표준화 중인 QUIC(표준 HTTP/3의 기반) 전송 계층을 MQTT에 적용하여, 핸드셰이크 오버헤드를 줄이고 멀티플렉싱을 지원하여，进一步적인 latency 감소와 mobility 지원 향상이 예상된다.

### 참고 표준

- OASIS MQTT v5.0 Specification (2017)
- MQTT v3.1.1 (2014, 가장 널리 사용)
- MQTT-SN v1.2 (2015, 센서 네트워크용)

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    MQTT 프로토콜 발전 및 미래 방향                             │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  1999         2010          2014          2017          2023+           │
  │   │            │             │             │              │               │
  │   ▼            ▼             ▼             ▼              ▼               │
  │ [발명]    → [v3.1]    → [v3.1.1]   → [v5.0]    → [MQTT over QUIC]   │
  │  석유         Apache         OASIS         Session       저지연·모빌리티   │
  │  파이프라인    공개           표준화         Expiry       지원 향상       │
  │  모니터링                   (현재 주류)     Shared Sub                    │
  │                                                                     │
  │   └────────────── 기업 adoption 확대 ─────────────────────────────▶│
  │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** MQTT는 탄생의 이유가 석유 파이프라인 원격 모니터링이었듯이, 당초 산업용 M2M 통신에 초점을 맞추었다. 시간이 지나면서 클라우드 IoT 플랫폼의 등장으로 소비전자/스마트홈 영역으로 급격히 확산되었고, MQTT 5.0의 enterprise 기능 추가로 전통적인 ESB(Enterprise Service Bus) 시장을浸食하고 있다. 향후 MQTT over QUIC이 실현되면, 현재의 TCP 기반 핸드셰이크 오버헤드가 줄어들어 고속 이동 환경(자율주행차, drone)에서의 MQTT 활용도가 더욱 높아질 전망이다.

- **📢 섹션 요약 비유**: MQTT의 진화는 **"전세زون 발송 시스템의 진화"** 에 비유할 수 있다. 처음에는 등기 우편(QoS 2)만 가능했지만, 나중에는 일반 우편(QoS 0)도 가능해졌고, 사서함租赁서비스(Session Expiry)를 활용하면 잠깐不在の間에도 우편을 보관해줄 수 있게 되었다. 공유 구독(Shared Subscription)은 여러 명이 공동 구독하여 우편 비용을 나누는 것과 같다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Publish-Subscribe 모델** | MQTT의 핵심 메시징 패턴으로, Publisher와 Subscriber가 브로커를 통해 간접 통신하여 결합도를 낮추고 확장성을 높인다. |
| **QoS (Quality of Service)** | MQTT에서 메시지 전달 신뢰성을 결정하는 3단계 레벨로, 서비스 요구에 따라 선택적으로 적용하여 네트워크 오버헤드와 신뢰성 간의 트레이드오프를 관리한다. |
| **Broker (브로커)** | MQTT의 중앙 메시지 라우팅 노드로, 발행자의 메시지를 적절한 구독자에게 전달하며, 클라이언트 연결 관리, 세션 유지, 메시지 보존(Retained) 등의 역할을 담당한다. |
| **Topic (토픽)** | MQTT에서 메시지의 논리적 주소로, /-separated 계층적 구조를 사용하여 메시지를 분류하고 구독자 Pallon에 따라 필터링한다. |
| **MQTT-SN** | MQTT for Sensor Networks의 약자로, UDP 기반, sleep 지원, gateway架构 등으로 제한된 센서 환경에 최적화된 변형이다. |
| **Clean Session** | MQTT CONNECT에서 설정하는 옵션으로, true이면 연결 종료 시 구독/메시지가 모두 삭제되고, false이면 재연결 시에도 session과 구독, QoS 1/2 메시지를恢复한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. MQTT는 **"우체국 친구들"** 에 비유할 수 있어요. 신문사(발행자)가 신문을 우체국(브로커)에 가져다 주면, 우체국에서는 그 신문을 구독한各家(구독자)에게 배달해줘요.各家에서는 누가 신문을 보냈는지 몰라도 되고, 신문사에서도 누가 받는지 몰라도 되서 편하다고 느껴요.
2. 토픽은 **"우편 번호"** 같은 거예요. 우편 번호가 다르면 다른地区로 배달되듯이, "/집/거실/온도"와 "/집/주방/온도"는 다른Topics으로 취급되어, 거실 온도만 받고 싶은 사람은 "/집/+ /온도"처럼订阅하면 돼요.
3. QoS는 **"편지 부치기 방법"** 과 같아요. 일반 우편(QoS 0)은 제일 빠르지만 가끔 유실될 수 있고, 등기 우편(QoS 1)은 반드시 도착하지만 조금 늦어지고, 빠른 등기 우편(QoS 2)은 제일 확실하지만代价(시간과 비용)이 많이 들어요.
