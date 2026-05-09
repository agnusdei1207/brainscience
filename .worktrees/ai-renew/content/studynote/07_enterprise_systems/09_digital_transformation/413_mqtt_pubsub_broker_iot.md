+++
weight = 413
title = "413. MQTT Pub/Sub 브로커 기반 경량 IoT 프로토콜 (MQTT)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MQTT(Message Queuing Telemetry Transport)는 TCP/IP 위에서 브로커(Broker) 기반 Pub/Sub 패턴으로 동작하는 경량 IoT 메시지 프로토콜로, 저대역폭·고지연·불안정 네트워크 환경에 최적화되어 있다.
> 2. **가치**: 2~7byte의 최소 헤더 크기, QoS(Quality of Service) 0/1/2 수준 선택, 브로커 기반 비동기 디커플링으로 수백만 IoT 기기의 실시간 메시지 처리를 지원한다.
> 3. **판단 포인트**: QoS 0(최소 1회, 손실 가능) vs QoS 1(최소 1회, 중복 가능) vs QoS 2(정확히 1회, 고비용)의 선택이 신뢰성과 오버헤드 간 핵심 트레이드오프다.

## Ⅰ. 개요 및 필요성

1999년 IBM의 Andy Stanford-Clark과 Arlen Nipper가 원유 파이프라인 SCADA 시스템 원격 모니터링을 위해 설계한 MQTT는 위성 링크 같은 불안정·고지연·저대역폭 환경에서도 신뢰성 있는 메시지 전달을 목표로 했다. HTTP REST 대비 헤더 오버헤드가 수십 배 작아 배터리 구동 IoT 기기에 이상적이며, OASIS 표준(2013)으로 공식화됐다.

📢 **섹션 요약 비유**: MQTT는 IoT의 엽서 — 짧고(경량 헤더) 많이 보낼 수 있으며, 우체국(브로커)이 원하는 사람(구독자)에게만 배달한다.

## Ⅱ. 아키텍처 및 핵심 원리

```
Publisher          MQTT Broker           Subscriber
(온도 센서)         (Mosquitto, HiveMQ)   (대시보드, AI)
─────────          ─────────────         ─────────────
온도 = 25℃  ──────>│ Topic: factory/     │──────> 온도 모니터링
PUBLISH            │ sensor/temp         │         (구독)
QoS 1              │ 메시지 라우팅        │
                   │ 세션 관리            │──────> 알람 시스템
                   │ Retain/LWT           │         (구독)
                   └─────────────────────┘

QoS 레벨:
  QoS 0: 최대 1회 전달 (Fire and Forget) - 손실 가능
  QoS 1: 최소 1회 전달 (At Least Once) - 중복 가능
  QoS 2: 정확히 1회 (Exactly Once) - 4단계 핸드셰이크
```

| 기능 | 설명 |
|:---|:---|
| Topic | 계층적 메시지 채널 (factory/floor1/sensor/+) |
| Retain | 마지막 메시지를 브로커에 보존 (새 구독자에게 즉시 전달) |
| LWT (Last Will and Testament) | 비정상 종료 시 브로커가 미리 설정한 메시지 발행 |
| Keep Alive | 주기적 PINGREQ로 연결 상태 확인 |
| Clean Session | 세션 상태(미전달 메시지) 유지 여부 |

📢 **섹션 요약 비유**: LWT(유언)는 기기의 비상 연락망 — 기기가 갑자기 연결을 끊으면 브로커가 자동으로 "연결 끊김" 메시지를 대신 발행한다.

## Ⅲ. 비교 및 연결

| 항목 | MQTT | HTTP REST |
|:---|:---|:---|
| 통신 모델 | Pub/Sub (비동기) | Request/Response (동기) |
| 헤더 크기 | 2~7byte | 수백 byte |
| 연결 방식 | 지속 연결(TCP) | 요청마다 연결 |
| 저전력 적합성 | 매우 높음 | 낮음 |
| 브로커 필요 | 필요 | 불필요 |

MQTT over WebSocket: 웹 브라우저에서 MQTT 브로커에 직접 구독·발행 가능 → 실시간 대시보드 구현.

📢 **섹션 요약 비유**: MQTT vs HTTP는 방송(MQTT) vs 전화(HTTP) — 방송은 한 번 보내면 많은 사람이 듣고, 전화는 한 명씩 연결해야 한다.

## Ⅳ. 실무 적용 및 기술사 판단

**의사결정 포인트**:
- 배터리 IoT(수년 수명): QoS 0 + LoRa/NB-IoT + MQTT
- 산업 제어(손실 불허): QoS 2 + TLS/mTLS 보안
- 클라우드 연동: AWS IoT Core, Azure IoT Hub 모두 MQTT 지원
- 브로커 선택: Mosquitto(경량), HiveMQ(엔터프라이즈), AWS IoT Core(관리형)

📢 **섹션 요약 비유**: QoS 선택은 배달 옵션 — 택배(QoS 0), 등기(QoS 1), 본인 수령 확인 등기(QoS 2) 중 중요도에 따라 선택한다.

## Ⅴ. 기대효과 및 결론

MQTT는 IoT 메시지 통신의 사실상 표준으로, AWS IoT·Azure IoT·Google Cloud IoT에서 기본 프로토콜로 채택됐다. 경량성과 QoS 유연성이 강점이나, 보안 기본값 부재(MQTT 3.1.1은 인증 선택적)와 클라이언트 상태 추적 복잡성이 한계다. MQTT 5.0에서 향상된 오류 보고·흐름 제어·공유 구독이 추가되어 엔터프라이즈 적용성이 높아졌다.

📢 **섹션 요약 비유**: MQTT는 IoT 세계의 우편 제도 — 단순하고 신뢰할 수 있으며, 전 세계 수십억 기기가 이 제도(표준)를 따른다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Pub/Sub | 통신 패턴 | 발행자-구독자 비동기 분리 |
| QoS (Quality of Service) | 신뢰성 수준 | 0/1/2 단계 메시지 전달 보증 |
| LWT (Last Will and Testament) | 내결함성 | 비정상 종료 자동 알림 |
| Mosquitto | 구현체 | 오픈소스 경량 MQTT 브로커 |
| MQTT 5.0 | 최신 표준 | 향상된 흐름 제어·오류 보고 |

### 👶 어린이를 위한 3줄 비유 설명

1. MQTT는 학교 방송 — 선생님(발행자)이 스피커(브로커)에 대고 말하면, 듣고 싶은 반(구독자)에만 전달돼.
2. QoS 0은 방송 중 잡음 OK(손실 허용), QoS 2는 모두가 들었는지 확인하는 출석 확인이야.
3. LWT는 기기의 유언장 — 갑자기 꺼지면 "저 지금 죽었어요" 메시지가 자동으로 나가도록 미리 설정해 두는 것!
