+++
weight = 414
title = "414. CoAP UDP RESTful P2P IoT 경량 프로토콜 (CoAP)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CoAP(Constrained Application Protocol)은 UDP 기반 RESTful 메서드(GET/POST/PUT/DELETE)를 제공하는 IoT 경량 프로토콜로, HTTP의 의미론을 8byte 최소 헤더로 구현하여 MCU(Microcontroller)급 제약 환경에 적합하다.
> 2. **가치**: 브로커 없는 P2P(Peer-to-Peer) 직접 통신, UDP 기반 저지연 멀티캐스트, DTLS(Datagram TLS)로 보안을 제공하여 M2M(Machine-to-Machine) 직접 통신에 MQTT 대비 적합하다.
> 3. **판단 포인트**: CoAP은 P2P 직접 통신과 브로드캐스트/멀티캐스트가 장점이지만, UDP 특성상 패킷 손실 처리를 애플리케이션이 책임져야 하는 복잡성이 단점이다.

## Ⅰ. 개요 및 필요성

HTTP는 헤더가 수백 byte로 MCU의 제한된 메모리(수KB)와 배터리에 부담이 크다. CoAP(RFC 7252, 2014)은 IETF가 설계한 HTTP 의미론의 경량화 버전으로, UDP를 사용하여 TCP 핸드셰이크 오버헤드를 제거하고 최소 4byte 헤더로 REST 메서드를 제공한다.

6LoWPAN(IPv6 over Low-power WPAN)과 결합하여 Zigbee 메시 네트워크 위에서 IP 기반 REST 통신을 실현한다.

📢 **섹션 요약 비유**: CoAP은 다이어트 HTTP — 같은 메서드(GET/POST)를 쓰지만, 헤더(포장)를 극도로 줄여서 소형 기기에 맞췄다.

## Ⅱ. 아키텍처 및 핵심 원리

```
CoAP 메시지 구조 (최소 4byte 헤더):
 0         1         2         3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Ver| T |  TKL  |     Code      |          Message ID           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Token (0~8 bytes)  ....
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

메시지 타입:
  CON (Confirmable): ACK 필요 → 신뢰성 보장
  NON (Non-confirmable): ACK 없음 → 빠르지만 손실 가능
  ACK: 확인 응답
  RST: 재설정
```

| 항목 | CoAP | MQTT | HTTP |
|:---|:---|:---|:---|
| 전송 계층 | UDP | TCP | TCP |
| 통신 모델 | P2P RESTful | Pub/Sub 브로커 | Request/Response |
| 헤더 크기 | 4byte~ | 2byte~ | 수백 byte |
| 브로커 필요 | 불필요 | 필요 | 불필요 |
| 멀티캐스트 | 지원(UDP) | 미지원 | 미지원 |
| 적합 환경 | M2M 직접 통신 | 다대다 메시징 | 웹 API |

📢 **섹션 요약 비유**: CoAP은 기기 간 직접 통화 — MQTT가 교환원(브로커)을 통하는 반면, CoAP은 상대방 번호를 직접 눌러 연결한다.

## Ⅲ. 비교 및 연결

CoAP-Observe: HTTP의 웹훅처럼, 서버가 리소스 변경을 클라이언트에 자동 알림(Push) — MQTT 구독과 유사 기능. DTLS(Datagram TLS): CoAP + DTLS = UDP 위의 보안 전송 계층, MQTT + TLS와 유사한 보안 수준 제공.

📢 **섹션 요약 비유**: CoAP-Observe는 IoT의 알림 서비스 — 온도가 바뀌면 자동으로 알려줘, 주기적으로 확인할 필요 없이.

## Ⅳ. 실무 적용 및 기술사 판단

**의사결정 포인트**:
- MCU 직접 제어(M2M): CoAP (P2P, 브로커 불필요)
- 다대다 메시지 팬아웃: MQTT (브로커 기반 Pub/Sub)
- 스마트에너지·스마트 그리드(IEC 61968): CoAP + 6LoWPAN
- HTTP 기반 기존 인프라 연동: CoAP-HTTP 프록시 활용

📢 **섹션 요약 비유**: CoAP vs MQTT는 문자(P2P) vs 단체 카톡(브로커 기반) — 1:1 직접 통신엔 문자, 1:다 알림엔 단체 카톡이 적합하다.

## Ⅴ. 기대효과 및 결론

CoAP은 IoT M2M 직접 통신, 스마트 에너지 관리, 산업 자동화에서 HTTP 대체제로 활용된다. UDP 특성으로 인한 패킷 재전송(CON 메시지) 관리가 복잡성의 주요 원인이며, 6LoWPAN+CoAP 조합이 IPv6 기반 IoT 인터넷(Internet of Things Internet)의 핵심 프로토콜 스택이 되고 있다.

📢 **섹션 요약 비유**: CoAP은 IoT 세계의 경량 자전거 — HTTP 자동차보다 느리지만(낮은 처리량), 좁은 골목(제약 환경)에서는 훨씬 효율적이다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| UDP | 전송 계층 | TCP 대비 경량, 비연결 |
| 6LoWPAN | 네트워크 레이어 | IPv6 IoT 경량화 |
| DTLS | 보안 레이어 | UDP 위의 TLS 보안 |
| CoAP-Observe | 확장 기능 | 서버→클라이언트 Push 알림 |
| MQTT | 비교 대상 | 브로커 기반 Pub/Sub IoT 프로토콜 |

### 👶 어린이를 위한 3줄 비유 설명

1. CoAP은 다이어트 웹사이트 — 인터넷 홈페이지(HTTP)와 같은 방법(GET/POST)을 쓰지만, 훨씬 작고 빠르게 만들었어.
2. UDP를 써서 TCP보다 빠르지만 — 편지가 가끔 분실될 수 있어서, 중요한 건 확인(ACK) 요청을 보내야 해.
3. P2P는 직접 통화 — 교환원(브로커) 없이 기기끼리 직접 대화하는 것이 CoAP의 특기야!
