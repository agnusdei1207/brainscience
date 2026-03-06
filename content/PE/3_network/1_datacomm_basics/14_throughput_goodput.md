+++
title = "처리량 (Throughput)과 굿풋 (Goodput)"
weight = 14
categories = ["studynotes-네트워크"]
+++

# 처리량 (Throughput)과 굿풋 (Goodput) 심층 분석

## Ⅰ. 개요 (Introduction)
네트워크 성능을 평가할 때 '대역폭(Bandwidth)'이 물리적인 최대 전송 능력을 나타낸다면, **처리량(Throughput)**과 **굿풋(Goodput)**은 사용자가 실제로 경험하는 네트워크의 실효 속도를 나타내는 지표입니다. 
*   **처리량(Throughput)**: 단위 시간당 특정 노드나 링크를 성공적으로 통과한 전체 데이터의 양(오버헤드 포함).
*   **굿풋(Goodput)**: 단위 시간당 목적지 애플리케이션에 성공적으로 전달된 **유효한 페이로드(Payload)** 데이터의 양(오버헤드 및 재전송 제외).
네트워크 엔지니어링에서는 대역폭의 낭비를 줄이고 궁극적으로 애플리케이션 관점의 굿풋을 극대화하는 것이 핵심 목표입니다.

## Ⅱ. 아키텍처 및 핵심 원리 (Architecture & Core Principles)

### 1. 프로토콜 스택과 오버헤드 원리
데이터가 네트워크를 통과할 때 OSI 7계층을 거치며 각 계층의 헤더(Header)와 트레일러(Trailer)가 추가됩니다. 이러한 캡슐화(Encapsulation) 과정은 물리적 링크의 대역폭을 차지하지만, 최종 애플리케이션 입장에서는 유효 데이터가 아니므로 굿풋을 감소시키는 원인이 됩니다.

### 2. 아키텍처 및 흐름도 (ASCII Diagram)
아래 다이어그램은 대역폭에서 굿풋이 도출되는 감쇠 과정을 계층별 오버헤드 관점에서 보여줍니다.

```text
+---------------------------------------------------------+
|                  Link Bandwidth (Capacity)              |
|   [=================================================]   | 100%
+---------------------------------------------------------+
                              | (- Physical Layer Coding, Inter-frame gaps, Preambles)
+---------------------------------------------------------+
|                    Throughput (L2/L3)                   |
|   [=========================================]           | ~85-95%
|   (Excludes Physical Layer Overhead/Errors)             |
+---------------------------------------------------------+
                              | (- MAC Header/FCS, IP Header, TCP/UDP Header)
                              | (- Retransmissions due to packet loss/errors)
+---------------------------------------------------------+
|                      Goodput (App Layer)                |
|   [=================================]                   | ~70-80%
|   (Only the pure Application Payload delivered)         |
+---------------------------------------------------------+
```

### 3. 수학적 논리 (Calculation Logic)
굿풋(G)은 다음과 같이 근사화할 수 있습니다.
$G = \frac{\text{Data Size}}{\text{Data Size} + \text{Headers Size}} \times \text{Throughput} \times (1 - \text{Packet Loss Rate})$
예를 들어, 1460 바이트의 TCP 페이로드, 20 바이트 TCP 헤더, 20 바이트 IP 헤더, 18 바이트 이더넷 헤더를 가정할 경우, 순수 페이로드의 비율은 $1460 / (1460 + 20 + 20 + 18) \approx 96\%$가 되며, 여기에 재전송 확률을 감안한 것이 실제 굿풋이 됩니다.

## Ⅲ. 융합 비교 및 다각도 분석 (Comparative & Multi-dimensional Analysis)

### 1. Throughput vs Goodput
| 구분 | 처리량 (Throughput) | 굿풋 (Goodput) |
|---|---|---|
| **측정 기준점** | 네트워크 계층 (주로 L2/L3) | 애플리케이션 계층 (L7) |
| **오버헤드 포함 여부** | 프로토콜 헤더 등 각종 제어 정보 포함 | 순수 사용자 데이터(Payload)만 포함 |
| **재전송 처리** | 재전송된 패킷도 처리량 트래픽에 합산됨 | 중복/재전송 패킷은 제외됨 (성공한 유효 데이터만) |
| **성능 체감** | 라우터/스위치 등 장비 관점의 처리 능력 | 사용자 경험(QoE), 파일 전송 시간 등 체감 성능 |

### 2. 프로토콜별 굿풋 특성 (TCP vs UDP)
*   **TCP**: 신뢰성 보장을 위해 3-Way Handshake, ACK 확인, 흐름 제어, 혼잡 제어를 수행합니다. 네트워크 지연(RTT)이나 패킷 손실이 발생하면 혼잡 윈도우(CWND)를 줄여 굿풋이 급격히 저하될 수 있습니다. (BDP 고려 필요)
*   **UDP**: 전송 제어 오버헤드가 적어 대역폭을 최대한 Throughput으로 변환할 수 있으나, 패킷 손실 시 복구 메커니즘이 없어 애플리케이션 단의 처리에 따라 굿풋이 결정됩니다.

## Ⅳ. 실무 적용 및 기술사적 판단 (Practical Application & Professional Engineer's Perspective)

### 1. 굿풋 극대화를 위한 실무 기법
*   **Jumbo Frame 도입**: MTU(Maximum Transmission Unit)를 1500바이트에서 9000바이트로 늘려 헤더의 비율을 줄임으로써 굿풋을 향상시킵니다 (데이터센터 내부 통신에 주로 적용).
*   **TCP 최적화**: 위성 통신이나 장거리 광통신망(LFN, Long Fat Network) 환경에서는 BDP(Bandwidth-Delay Product)가 크기 때문에 Window Scaling Option(RFC 1323)을 적용하고, TCP BBR과 같은 최신 혼잡 제어 알고리즘을 사용하여 굿풋을 방어해야 합니다.

### 2. 기술사적 통찰 (Expert Perspective)
성능 테스트(BMT/PoC) 시 벤더가 제시하는 장비의 스루풋 스펙은 종종 "초당 패킷 처리수(PPS, Packets Per Second)"나 64-byte의 작은 패킷을 기준으로 부풀려지는 경향이 있습니다. 기술사는 반드시 iperf 등을 통해 실제 서비스 모델과 유사한 패킷 사이즈 및 프로토콜 믹스 환경에서 **App 레벨의 굿풋을 실측**하고 이를 기준으로 네트워크를 설계 및 검증해야 합니다.

## Ⅴ. 기대효과 및 결론 (Expected Effects & Conclusion)

네트워크 관리를 대역폭 중심에서 굿풋 중심으로 전환함으로써, 진정한 사용자 체감 품질(QoE)을 개선할 수 있습니다. 
불필요한 재전송을 줄이고 프로토콜 오버헤드를 최소화하는 구조적 개선은, 추가적인 회선 증설 없이도 실질적인 대역폭 확장 효과를 가져옵니다. 따라서 향후 네트워크 인프라는 트래픽의 단순 전달을 넘어, AI 기반의 트래픽 분석을 통해 굿풋을 실시간으로 극대화하는 자율 제어형 네트워크(Autonomous Network)로 발전해야 할 것입니다.
