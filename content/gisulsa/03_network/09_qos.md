+++
weight = 9
title = "09. 네트워크 QoS & 혼잡제어"
date = "2026-05-17"
[extra]
categories = "gisulsa-network"
+++

# 네트워크 QoS & TCP 혼잡제어

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

정의: 네트워크 트래픽에 우선순위를 부여하여
     중요 트래픽의 품질을 보장하는 기술
대역폭 (Bandwidth): 최대 전송 속도

### Ⅱ. 핵심 구성요소

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
```
[4가지 알고리즘]
슬로우 스타트 (Slow Start):
  cwnd = 1 → 매 RTT 2배 증가 (지수)
  SSThresh 도달 시 혼잡 회피로 전환

혼잡 회피 (Congestion Avoidance):
  cwnd += 1/cwnd per ACK (선형 증가)
  
빠른 재전송 (Fast Retransmit):


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
