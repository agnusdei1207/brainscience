+++
weight = 9
title = "CoAP (Constrained Application Protocol) 프로토콜"
description = "CoAP의 구조, HTTP/REST 매핑, UDP 기반 동작, DTLS 보안, IoT 환경 최적화를شرح"
date = 2024-01-23

[extra]
categories = ["studynote-software-engineering"]
tags = ["coap", "iot", "m2m", "rest", "constrained", "protocol"]

+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CoAP(Constrained Application Protocol)은 UDP 기반의 경량 프로토콜로, 자원이 제한된 IoT 디바이스(8KB RAM, 100KB Flash)에서도 동작할 수 있도록 설계되었으며, HTTP/REST 모델과 매핑되어 웹 기술과 IoT의 통합을 쉽게 한다.
> 2. **가치**: CoAP은 MQTT와 달리 Request-Response 모델을 채택하여 중앙에서 디바이스를 직접 제어하는 시나리오에 적합하며, Confirmable(CON)/Non-confirmable(NON) 메시지와 Observe 기능을 통해 다양한 신뢰성 수준을 제공한다.
> 3. **융합**: CoAP은 6LoWPAN, IPv6, UDP를 기반으로 차세대 IoT 네트워크(IPv6-enabled low-power WPAN)의 핵심 프로토콜로 자리잡았으며, HTTP와 CoAP 사이의proxy를 통해 웹 서비스와 직접 연동 가능하다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념

CoAP은 IETF(Internet Engineering Task Force)의 RFC 7252로 표준화된 프로토콜로, "Constrained"라는 이름이 말해주듯이 매우 제한된 자원(limited RAM, limited processing power, limited power budget)을 가진 디바이스를 위해 설계되었다. CoAP의 설계 철학은 "웹을 소형 디바이스로 확장하는 것"으로, HTTP의 Request-Response 모델을踏襲하면서도 UDP 기반의 lightweight한 프로토콜로 만들었다.

### 필요성

기존 HTTP/TCP 스택은 자원이 풍부한 서버/클라이언트 환경에서는問題 없지만, 8-bit MCU, 8KB RAM, 100KB Flash만搭载한 센서 노드에서는 TCP 핸드셰이크(3-way handshake)와 HTTP 헤더의 오버헤드가 디바이스의 처리 능력과 전력 budget을 초과할 수 있다. CoAP은 이를 해결하기 위해 UDP(1바이트 오버헤드)와 4바이트 고정 헤더를 사용한다.

### 등장 배경

CoAP은 2010년 IETF에서 standardization 과정이 시작되어 2014년 RFC 7252로 공식 발표되었다. 배경에는 6LoWPAN(IPv6 over Low-Power Wireless Personal Area Networks) 표준화의 영향이 크다. 6LoWPAN이 IPv6를 IEEE 802.15.4 네트워크에 올리는 방법을 정의했으나, TCP/IP 스택 전체를 포팅하기에는 MCU가 부족했기 때문에, UDP 기반의 경량 Application 프로토콜이 필요했다.

### 💡 비유

CoAP은 **"우편 대신 택배를 이용하는 것"** 에 비유할 수 있다. HTTP는 택배짐을 보낼 때마다 계약서(HTTP header)를 잔뜩 쓰지만, CoAP은 간단한 영수증(CoAP header)만 붙여서 보낸다. UDP 기반이라 전화를 해서 상대방이 받았는지 확인(CON)하거나, 확인 없이 그냥 던져놓고(CONFIRMABLE 없이) 떠나버릴 수도 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### CoAP 메시지 구조

CoAP의 메시지는 4바이트 고정 헤더와 가변 Option, Payload로 구성된다. 이는 이더넷 프레임(14바이트)보다도 작은 엄청나게 간결한 구조이다.

| 필드 | 크기 | 설명 |
|:---|:---|:---|
| **Version (Ver)** | 2 bits | 프로토콜 버전 (현재 1) |
| **Type (T)** | 2 bits | 0=Confirmable(CON), 1=Non-confirmable(NON), 2=ACK, 3=Reset |
| **Token Length (TKL)** | 4 bits | Token 필드의 길이 (0~8바이트) |
| **Code** | 8 bits | 요청: 0.01=GET, 0.02=POST, 0.03=PUT, 0.04=DELETE / 응답: 2.xx=Success, 4.xx=Client Error, 5.xx=Server Error |
| **Message ID** | 16 bits | 중복 detection과 matching에 사용 |
| **Token** | 0~8 bytes | 요청/응답 matching에 사용 |
| **Options** | 가변 | URI Path, Content-Format, Max-Age 등 |
| **Payload** | 가변 | 실제 데이터, Payload Marker(0xFF) 이후 |

---

### CoAP Request-Response 모델

CoAP은 HTTP의 GET/POST/PUT/DELETE 메서드를踏襲하지만, UDP 위에서 동작하므로 신뢰성을 위해 자체 메커니즘(ACK/Retransmission)을 갖는다. Confirmable(CON) 메시지는 상대방의 ACK 또는 RST(Reset)를 기다리고, Non-confirmable(NON) 메시지는 확인 없이 전송한다.

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    CoAP 메시지 교환 패턴                                        │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  [GET 요청 (Confirmable - CON)]                                        │
  │
  │  Client                                               Server                │
  │    │                                                      │                │
  │    │  CON [GET]  GET /sensor/temp   Message-ID=0x1234    │                │
  │    │ ──────────────────────────────────────────────────▶  │                │
  │    │  (재전송: 0.5s, 1s, 2s, 4s... timeout)               │                │
  │    │                                                      │                │
  │    │  ACK [2.00 OK]  2.05  Content   Message-ID=0x1234    │                │
  │    │ ◀────────────────────────────────────────────────── │                │
  │    │  (payload: "temperature=23.5")                       │                │
  │
  │  [GET 요청 + Piggybacked Response]                                        │
  │
  │  Client                                               Server                │
  │    │                                                      │                │
  │    │  CON [GET]  GET /sensor/temp   Message-ID=0x1234    │                │
  │    │ ──────────────────────────────────────────────────▶  │                │
  │    │                                                      │                │
  │    │  ACK [2.00 OK]  2.00  Content   Message-ID=0x1234    │                │
  │    │ ◀────────────────────────────────────────────────── │                │
  │    │  (즉시 응답, RTT ≈ 1홉 latency)                      │                │
  │
  │  [POST 요청 + Separate Response (异步)]                                    │
  │
  │  Client                                               Server                │
  │    │                                                      │                │
  │    │  CON [POST] POST /actuator   Message-ID=0x1234     │                │
  │    │ ──────────────────────────────────────────────────▶  │                │
  │    │  ACK                                                   │                │
  │    │ ◀────────────────────────────────────────────────── │                │
  │    │              (서버가 처리 중... )                      │                │
  │    │                                                      │                │
  │    │  CON [2.01 Created]    Message-ID=0x5678   (separate) │                │
  │    │ ◀────────────────────────────────────────────────── │                │
  │    │                                                      │                │
  │    │  ACK                                                   │                │
  │    │ ──────────────────────────────────────────────────▶  │                │
  │
  │  [Observe (서버→클라이언트 지속 알림)]                                       │
  │
  │  Client                                               Server                │
  │    │                                                      │                │
  │    │  CON [GET] GET /sensor/temp   Observe:0             │                │
  │    │ ──────────────────────────────────────────────────▶  │                │
  │    │                                                      │                │
  │    │  ACK [2.00 OK]  Observe:12, ...                    │                │
  │    │ ◀────────────────────────────────────────────────── │                │
  │    │  (payload: temperature=23.5)                        │                │
  │    │                                                      │                │
  │    │  ... (센서 값이 변할 때마다)                          │                │
  │    │                                                      │                │
  │    │  CON [2.00 OK]  Observe:12, ...                    │                │
  │    │ ◀────────────────────────────────────────────────── │                │
  │    │  (payload: temperature=24.1) ← 값 변화!              │                │
  │    │                                                      │                │
  │    │  ACK                                                   │                │
  │    │ ──────────────────────────────────────────────────▶  │                │
  │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** CoAP의 가장 중요한 특징 중 하나는 Piggybacked Response이다. 서버가 요청을 수신하고 즉시 응답할 수 있는 경우, ACK 메시지 안에 응답 데이터를 함께 실어 보낸다. 이를 통해 1-RTT(Round Trip Time) latency로 요청-응답이 완료된다. 반면 서버가 즉시 응답할 수 없는 경우(예: 센서에서 데이터를 수집하는 데 시간이 오래 걸리는 경우), 먼저 빈 ACK을 보내고 나중에 CON 메시지로 결과를 보낸다. 이 경우 client는 ACK 후 두 번째 CON 메시지를 기다려야 하므로 latency가 증가한다. Observe 기능은 MQTT의 Subscribe와 유사하게, 클라이언트가 자원에 "관찰자(Observer)"로 등록하고, 서버는 자원의 상태가 변화할 때마다 클라이언트에게 알림(notification)을 보낸다. 단, MQTT가 broker를 통해 간접 통신하는 반면, CoAP Observe는 서버가 직접 클라이언트에게 알림을 보내는 direct 통신이다.

---

### CoAP 옵션과 Content-Format

CoAP은 HTTP의 헤더와 유사한 기능을 Options으로 제공한다. 주요 옵션에는 URI-Path, URI-Query, Content-Format, Accept, Observe, Max-Age 등이 있다. Content-Format은 payload의 MIME 타입을 나타내며, IANA에 등록된 포맷(예: text/plain, application/json, application/xml, application/cbor)이 있다.

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    CoAP과 HTTP의 비교 및 매핑                                │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  CoAP                                   HTTP                             │
  │  ──────────────────────────────────────────────────────────────────────│
  │  coap://host:port/path               http://host:port/path             │
  │  GET /path                           GET /path                         │
  │  POST /path                          POST /path                        │
  │  PUT /path                           PUT /path                         │
  │  DELETE /path                        DELETE /path                      │
  │  Content-Format                      Content-Type                      │
  │  Observe                             (long polling / WebSocket)        │
  │  Block (대용량 전송)                   Chunked transfer                  │
  │
  │  [CoAP-HTTP Proxy를 통한 상호 연동]                                        │
  │
  │  ┌───────────────────────────────────────────────────────────────────┐  │
  │  │                                                                   │  │
  │  │  [CoAP Device] ◀──coap──▶ [Proxy] ◀──http──▶ [HTTP Server]     │  │
  │  │                                                                   │  │
  │  │  GET /sensor/temp                                              │  │
  │  │  Accept: application/json                                       │  │
  │  │                                                                   │  │
  │  │  Proxy가 HTTP로 변환:                                            │  │
  │  │  GET /sensor/temp                                               │  │
  │  │  Accept: application/json                                        │  │
  │  │                                                                   │  │
  │  │  HTTP Server 응답:                                              │  │
  │  │  HTTP/1.1 200 OK                                                │  │
  │  │  Content-Type: application/json                                   │  │
  │  │  {"temperature": 23.5}                                          │  │
  │  │                                                                   │  │
  │  │  Proxy가 CoAP으로 변환:                                          │  │
  │  │  2.00 Content                                                   │  │
  │  │  Content-Format: application/json                                 │  │
  │  │  {"temperature": 23.5}                                          │  │
  │  │                                                                   │  │
  │  └───────────────────────────────────────────────────────────────────┘  │
  │
  │  [CoAP Block Transfer (대용량 데이터 분할 전송)]                              │
  │
  │  GET /large/data                                                  │
  │  ─────────────────────────────────────────────────────────▶        │
  │                                                                     │
  │  2.00 Content  Block2=0/64/true  ← 64바이트만 우선 수신                  │
  │  ◀────────────────────────────────────────────────────────────────  │
  │                                                                     │
  │  GET /large/data  Block2=1/64/true  ← 다음 블록 요청                   │
  │  ─────────────────────────────────────────────────────────▶        │
  │                                                                     │
  │  2.00 Content  Block2=1/64/false  ← 마지막 블록 (more=false)          │
  │  ◀────────────────────────────────────────────────────────────────  │
  │                                                                     │
  │  전체 데이터를 64바이트 단위로 분할하여 전송, 메모리 제약 해결             │
  │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** CoAP-HTTP Proxy는 CoAP 환경과 HTTP/RESTful 웹 환경 사이의 브릿지 역할을 한다. 이는 기존 웹 서비스에 CoAP 센서/디바이스를 연동할 수 있게 해준다. 예를 들어, 웹 어플리케이션이 HTTP로 CoAP 디바이스의 온도 센서 값을 요청하면, Proxy가 이를 CoAP GET으로 변환하여 디바이스에 전달하고, 응답을 다시 HTTP로 변환하여 웹 어플리케이션에 전달한다. CoAP의 Block Transfer 기능은 대용량 데이터를 작은 블록으로 분할 전송하는 것으로, 이는 6LoWPAN(IPv6 over IEEE 802.15.4)의 최대 전송 단위(MTU)가 127바이트에 불과하기 때문에 필수적이다. 따라서 CoAP 메시지가 127바이트를 초과하면 자동으로 Block 옵션을 사용하여 분할 전송한다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### CoAP vs MQTT vs HTTP 비교

| 비교 항목 | CoAP | MQTT | HTTP/1.1 | HTTP/2 |
|:---|:---|:---|:---|:---|
| **전송** | UDP | TCP | TCP | TCP |
| **헤더 크기** | 4 bytes + options | 2 bytes minimum | 수십~수백 바이트 | 압축 가능 |
| **모델** | Request-Response | Pub-Sub | Request-Response | Request-Response |
| **양방향성** | 네이티브 지원 | 네이티브 지원 | Pull only | Pull only |
| **QoS** | CON/NON/ACK | 0/1/2 | 재시도 | 재시도 |
| **Observe/Push** | Observe 옵션 | SUBSCRIBE | polling | Server Push |
| **디바이스 적합성** | 매우 높음 (8KB RAM) | 보통 (32KB RAM) | 낮음 | 낮음 |
| **NAT超え** |艰难 (UDP) | 용이 (TCP+브로커) |艰难 |艰难 |

### CoAP의 가장 적합한 사용 시나리오

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    CoAP이 가장 적합한 IoT 시나리오                           │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  [CoAP 선택이 가장 좋은 경우]                                             │
  │
  │  ✓ 중앙에서 센서를 폴링 (request-response) — 온도/습도 주기적 읽기          │
  │  ✓ 자원이 극도로 제한된 MCU (8KB RAM, 100KB Flash)                        │
  │  ✓ UDP만 사용 가능한 환경 (6LoWPAN, IEEE 802.15.4)                       │
  │  ✓ 빠른 응답 시간 필요 (piggybacked response로 1-RTT)                    │
  │  ✓ 웹 서비스와 직접 연동 필요 (HTTP-CoAP Proxy 활용)                       │
  │  ✓ 센서가 능동적으로 서버에 연결하기 어려운 환경 (서버가 먼저 요청)           │
  │
  │  [CoAP이 맞지 않는 경우]                                                  │
  │
  │  ✗ 수천 개의 센서가 동시에 중앙에 데이터 전송 (MQTT가 더 효율적)             │
  │  ✗ TCP 기반의 안정적 연결 필요 (NAT traversal 등)                         │
  │  ✗ 복잡한 트랜잭션/세션 관리 필요                                        │
  │  ✗ 기존 MQTT 인프라 활용 중 (broker-based architecture 필요)             │
  │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** CoAP과 MQTT는 각각 다른 사용 시나리오에 최적화되어 있다. CoAP의 Request-Response 모델은 중앙에서 센서/디바이스를 폴링하거나 제어하는 시나리오에 자연스러우며, MQTT의 Publish-Subscribe 모델은 다수의 센서가 능동적으로 데이터를 중앙에 보고하고, 여러 소비자가 이를 구독하는 시나리오에 유리하다. 실제로 대규모 IoT 시스템에서는 두 프로토콜을 혼용하는 것이 일반적이다. 예를 들어, 센서는 CoAP으로 서버에 능동적으로 데이터를 보고하고(이는 CoAPObserve나 MQTT PUBLISH 모두 가능), 서버가 센서를 제어할 때는 MQTT SUBSCRIBE를 통해 관련 명령을 받는 구조를 만들 수 있다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 6LoWPAN/RPL 환경에서의 CoAP**: IEEE 802.15.4(최대 127바이트 MTU)와 IPv6를 함께 사용하는 6LoWPAN 환경에서 CoAP을 활용하려는 상황. 이 조합에서는 CoAP 메시지가 6LoWPAN의 단편화(fragmentation) 제한(6LoWPAN PATCH는 1280바이트 단편화를 지원)을 넘을 수 있으므로, Block 옵션을活用하여 작은 블록으로 분할 전송해야 한다. 또한 UDP의 unreliable 특성을 감안하여, 중요한 제어 명령에는 CON(Confirmable) 타입을 사용하고, 주기적 센서 데이터에는 NON(Non-confirmable) 타입을 사용하는 것이 적절하다.

2. **시나리오 — CoAP-DTLS 보안 적용**: CoAP에 보안을 적용할 때 DTLS(Datagram Transport Layer Security)를 사용한다. DTLS은 UDP 기반의 TLS로, 핸드셰이크 오버헤드가 있지만 상호 인증과 암호화된 통신이 가능하다. constrained 환경에서 DTLS의 영향은 무시할 수 없으므로, 적절한 cipher suite 선택(예: TLS_PSK_WITH_AES_128_CCM_8 등 lightweight cipher)과 재전송 타이머 값 조정이 필요하다.

3. **시나리오 — HTTP-CoAP 연동 게이트웨이**: 기존 웹 서비스에 새로운 IoT 센서를 연동하려는 상황에서, 센서가 CoAP만 지원하고 웹 서비스가 HTTP REST API만 받는 경우. 이 때는 CoAP-HTTPProxy를 활용하여, HTTP GET 요청을 CoAP GET으로 변환하여 센서에서 데이터를 가져오고, 이를 다시 HTTP로 변환하여 웹 서비스에 전달한다.

### 도입 체크리스트

- **기술적**: CoAP 메시지 크기가 6LoWPAN MTU(127바이트)를 초과하는 경우 Block 옵션을 사용하는 것이 필수적인가? DTLS 적용 시 constrained 디바이스의 성능 영향이 수용 가능한가?
- **운영·보안적**: CoAP 서버에DoS 공격(Rapid CON 메시지 전송으로 인한 재전송 Flooding)이 가능하므로, Rate Limiting과 함께 네트워크 접근 제어를 적용해야 한다.

### 안티패턴

- **NAT 환경에서의 CoAP**: UDP 기반의 CoAP은 NAT 환경에서 문제가 발생할 수 있다. NATTraversal을 위해打个小小的ICE(Interactive Connectivity Establishment) 같은 기술이 필요하며, 이는 CoAP의 lightweight 특성을 somewhat 훼손한다. 이 경우 MQTT over WebSocket처럼 TCP 기반의 프로토콜을 고려해야 한다.
- **과도한 Observe 등록**: 클라이언트가 너무 많은 자원에 Observe 등록을 하면 서버의 부담이 가중되고, 네트워크 bandwidth가 증가한다. 필요한 자원에만 Observe를 등록하고, Max-Age 옵션을 활용하여 알림 빈도를 조정해야 한다.

- **📢 섹션 요약 비유**: CoAP은 **"간소한 우편 배달"** 에 비유할 수 있다. 기존의등기우편(HTTP/TCP)은 열쇠와 계약서를 잔뜩 쓰지만, CoAP은 간단한 영수증(CONFIRMABLE)만 붙여서 보내거나, 아예 확인 없이 그냥 던져놓고(CONFIRMABLE 없이) 떠나버린다. 중대한 물건(CON)에는 확인 전화(ACK)를 받지만, 가벼운 물건(NON)에는 확인 없이 그냥 놓아둔다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | HTTP | CoAP (avg) | CoAP (optimized) |
|:---|:---|:---|:---|
| **정량** | 패킷 크기: 800B+ | 패킷 크기: 50~100B | 패킷 크기: 20~50B |
| **정량** | 레이턴시: 50~100ms | 레이턴시: 5~20ms | 레이턴시: 1~5ms |
| **정성** | 범용성 최고 | IoT 최적 | MCU 적용 가능 |

### 미래 전망

- **CoAP-DTLS 자동화**: DTLS의証明서 관리 복잡성을 해결하기 위해, CoAP 디바이스 간 PSK(Pre-Shared Key) 기반의 lightweight 보안이主流될 전망이다.
- **WebRTC와 CoAP 융합**: 브라우저의 WebRTC가 UDP를 직접 지원하게 되면서, 웹 어플리케이션에서 직접 CoAP을 활용하는 시나리오가可能出现할 수 있다.

### 참고 표준

- RFC 7252: CoAP 핵심 사양
- RFC 7641: CoAP Observe
- RFC 7959: CoAP Block-Wise Transfer
- RFC 8323: CoAP over TCP/TLS

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    CoAP/REST/OAuth/IoT 보안 통합 아키텍처                     │
  ├─────────────────────────────────────────────────────────────────────────┤
  │
  │  ┌───────────────────────────────────────────────────────────────────┐  │
  │  │                        IoT Gateway / Cloud                        │  │
  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │  │
  │  │  │ CoAP     │  │ HTTP     │  │ MQTT     │  │ WebSocket│         │  │
  │  │  │ Server   │  │ REST API │  │ Broker   │  │ Server   │         │  │
  │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘         │  │
  │  │       │              │              │              │               │  │
  │  │       └──────────────┼──────────────┴──────────────┘               │  │
  │  │                      │                                              │  │
  │  │              ┌───────┴───────┐                                      │  │
  │  │              │   OAuth 2.0   │ ← 공통 인증/인가 플랫폼               │  │
  │  │              └───────────────┘                                      │  │
  │  └───────────────────────────────────────────────────────────────────┘  │
  │                              │                                           │
  │  ┌──────────────────────────┴───────────────────────────────────────┐ │
  │  │                    Transport: UDP / DTLS / TCP/TLS                   │ │
  │  └───────────────────────────────────────────────────────────────────┘ │
  │                              │                                           │
  │  ┌──────────────────────────┴───────────────────────────────────────┐ │
  │  │               IEEE 802.15.4 / 6LoWPAN / BLE                       │ │
  │  └───────────────────────────────────────────────────────────────────┘ │
  │
  └─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** IoT 시스템에서 CoAP은 종종 OAuth 2.0과 함께 사용되어 보안을 제공한다. 클라이언트가 IoT Gateway 또는 Cloud에 접근할 때 OAuth 2.0 Access Token을 획득하고, 이를 CoAP 요청의 옵션에 포함시켜 보안을 적용한다. CoAP over DTLS는 디바이스 간 직접 보안을 제공하고, CoAP over TCP/TLS는 NAT 환경에서 사용될 수 있다.

- **📢 섹션 요약 비유**: CoAP은 **"아기 자전거"** 에 비유할 수 있다.HTTP는 성인용、自行车처럼 덩치가 크지만功能이 다양하고, CoAP은 어린이가 타는 작은 자전거처럼 작고 가볍지만, 자기가 타고 가야 할 곳(자원의 URI)만 정확히 알면 된다. 거기에 DTLS는 자전거에 경적을 붙이는 것으로, 누가 탈 것인지를確認(인증)하고 길을 잃지 않게(암호화) 해준다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **UDP 기반** | CoAP은 TCP 대신 UDP를 사용하여 핸드셰이크 오버헤드를 제거하고, lightweight한 메시지 교환을 가능하게 한다. 그러나 UDP의 unreliable 특성을 own mechanism(CON/NON/ACK)으로 보완한다. |
| **RFC 7252** | CoAP의 핵심 표준으로, 메시지 형식, 코드, 옵션, 프록시 기능 등을 정의한다. |
| **Observe (RFC 7641)** | CoAP에서 서버가 클라이언트에게 자원 상태 변화를 능동적으로 알릴 수 있는 기능으로, MQTT의 SUBSCRIBE와 유사하다. |
| **DTLS** | Datagram TLS로, UDP 기반의 TLS이다. CoAP에 보안을 적용할 때 사용되며, TCP 기반 TLS와 유사한 인증/암호화 기능을 제공한다. |
| **6LoWPAN** | IPv6 over Low-Power Wireless Personal Area Networks로, IEEE 802.15.4 네트워크에서 IPv6를 사용하기 위한 adaptation layer이다. CoAP은 6LoWPAN과 밀접하게 연동되어 사용된다. |
| **Block Transfer (RFC 7959)** | CoAP에서 대용량 데이터를 작은 블록으로 분할하여 전송하는 메커니즘으로, 6LoWPAN의 작은 MTU에 대응하기 위해 필수적이다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. CoAP은 **"아기-sized 우편袋子"** 예요. 成人大小的 우편袋(TCP/HTTP)는 너무 크고 무거워서 작은 IoT 우체국(IoT devices)에서는받지 못해요. 그래서 아기-sized袋子(CoAP)는 작고 가벼워서 작은 우체국에도 잘 들어가요.
2. Confirmable(CON)은 **"반드시 확인 받기"** 예요. 물건을 보낼 때 "다 받았어?" 확인 전화를 받을 때까지 계속 확인하는 것이고, Non-confirmable(NON)은 **"그냥 놓고 올게"** 예요. 확인 전화 대신 그냥 드롭하고 떠나는 것이에요.
3. CoAP의 Observe는 **"우편 편지함 알림"** 예요. 일반 우편은 우체국에 가야 새로운 편지가 있는지 알 수 있지만, Observe는 새로운 편지가 들어오면 자동으로 알림을 받아볼 수 있어요. 그렇게 하면 항상 기다리지 않고도 새로운 온도나 소리等信息을 바로 알 수 있어요.
