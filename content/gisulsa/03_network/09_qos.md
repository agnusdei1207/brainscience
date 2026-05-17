+++
weight = 9
title = "09. 네트워크 QoS & 혼잡제어"
date = "2026-05-17"
[extra]
categories = "gisulsa-network"
+++

# 🎯 네트워크 QoS & TCP 혼잡제어

> **별점**: ★★★★★ | 기본 필수

## 1. QoS (Quality of Service)

```
정의: 네트워크 트래픽에 우선순위를 부여하여
     중요 트래픽의 품질을 보장하는 기술

[QoS 지표]
대역폭 (Bandwidth): 최대 전송 속도
지연 (Latency): 패킷 전송 시간
지터 (Jitter): 지연 변동성
패킷 손실률 (Packet Loss Rate)

[QoS 메커니즘]
분류 (Classification): 트래픽 종류 식별
표시 (Marking): DSCP/CoS 비트 설정
폴리싱 (Policing): 임계값 초과 패킷 드롭
셰이핑 (Shaping): 초과 패킷 큐에 버퍼링
스케줄링:
  PQ (Priority Queuing): 높은 우선순위 먼저
  WFQ (Weighted Fair Queuing): 가중치 공정 분배
  CBWFQ: 클래스 기반 WFQ
```

## 2. TCP 혼잡 제어

```
[4가지 알고리즘]
슬로우 스타트 (Slow Start):
  cwnd = 1 → 매 RTT 2배 증가 (지수)
  SSThresh 도달 시 혼잡 회피로 전환

혼잡 회피 (Congestion Avoidance):
  cwnd += 1/cwnd per ACK (선형 증가)
  
빠른 재전송 (Fast Retransmit):
  타임아웃 대기 없이 3 중복 ACK → 즉시 재전송

빠른 복구 (Fast Recovery):
  손실 패킷 재전송 후 슬로우 스타트 건너뜀
  cwnd = SSThresh + 3

[TCP 혼잡 제어 알고리즘 진화]
Tahoe: 슬로우 스타트 + 혼잡 회피
Reno: + 빠른 재전송/복구
CUBIC: 함수 기반 (Linux 기본)
BBR: 대역폭+RTT 기반 (Google)
QUIC: UDP 기반 신세대 (HTTP/3)
```

## 3. HTTP/3 & QUIC

```
[QUIC (Quick UDP Internet Connections)]
Google 개발 → IETF 표준화
UDP 기반 (TLS 1.3 내장)

[HTTP/3 = HTTP/2 over QUIC]
HTTP/1.1: TCP, Head-of-Line 블로킹
HTTP/2: 멀티플렉싱, 단 TCP HoL 블로킹
HTTP/3: QUIC 스트림 독립 → HoL 해결

이점:
연결 수립: TLS 1.3 + 0-RTT 재연결
패킷 손실: 스트림 독립적 재전송
이동성: IP 변경 시 연결 유지 (Connection ID)
```

## 4. 답안 포인트

**3단락**: ① QoS 지표 & 폴리싱/셰이핑/스케줄링 → ② TCP 혼잡 제어 4단계 & CUBIC/BBR → ③ QUIC/HTTP/3 & HoL 블로킹 해결

## 5. 관련 개념

`5G(★133회)` → URLLC = 저지연 QoS 보장 | `CDN(클라우드)` → QoS + HTTP/3 최적화 | `SDN(05번)` → 소프트웨어 QoS 정책
