+++
weight = 3
title = "TCP 혼잡 제어 (Congestion Control)"
description = "TCP의 혼잡 제어 메커니즘인 Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery를 다룬다."
date = 2024-01-27

[extra]
categories = ["studynote-software-engineering"]
topics = ["transport-layer", "tcp", "congestion-control", "aimd"]
study_section = ["section-8-transport-layer-tcp-udp"]

number = "803"
core_insight = "TCP 혼잡 제어는 네트워크가 처리할 수 있는 이상의 데이터가 전송되는 것을 방지하여, 인터넷의 안정성을 유지하는 핵심 메커니즘이다. AIMD(Slow Start+线性増加, 손실 시乘法적 감소)로 공정하고 효율적인 대역폭 활용을 달성한다."
key_points = ["Slow Start (지수적 증가)", "Congestion Avoidance (선형 증가)", "AIMD (Additive Increase, Multiplicative Decrease)", "Fast Retransmit과 Fast Recovery"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TCP 혼잡 제어는 네트워크의 혼잡 상태를检测하고, 송신 속도를 조절하여 네트워크가 붕괴하는 것을 방지하는 메커니즘이다.
> 2. **가치**: 인터넷이 혼잡 제어 없이 동작하면, 작은 버퍼를 가진 라우터에서 패킷이 무한히 queue되고, Global Synchronization으로 네트워크 利用률이 급격히 떨어진다.
> 3. **융합**: BBR, CUBIC 등 새로운 혼잡 제어 알고리즘이 등장하여, 고대역폭·저지연 네트워크에서 TCP 성능을 개선하고 있다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

**개념**: TCP 혼잡 제어(Congestion Control)는 네트워크 내의路由器 버퍼가 넘치는 것을 방지하고,/link별公平하게 대역폭을 분배하기 위한 메커니즘이다. TCP는 각 연결에 혼잡 윈도우(Congestion Window, cwnd)를 유지하며, 이는 아직 ACK되지 않은 데이터의 최대 바이트 수를 제한한다. 혼잡 윈도우는 네트워크 상태에 따라 동적으로 조절되며, AIMD(Additive Increase, Multiplicative Decrease) 원칙에 따라 동작한다.

**필요성**: 1986년 인터넷에서 심각한 혼잡 붕괴(Congestion Collapse)가 발생했다. 이는 한 라우터의 버퍼가 가득 차면서 패킷이 균일하게 분실하고, 모든 TCP 연결이 동시에 재전송을 시작하는 Global Synchronization이 발생했다. Van Jacobson이 이 문제를 해결하기 위한 혼잡 제어 알고리즘을 개발하였으며, 이는 현재 인터넷이 동작하는 핵심 기반이 되었다.

**비유**: TCP 혼잡 제어는 **고속도로 진입로 신호 시스템**과 같다. 고속도로가 비어 있으면 많은 차가 들어올 수 있지만( slow start),堵Singapore 가까워지면 조금씩 들어오는 차를 늘리고( congestion avoidance), 만약 사고가 나면大多数の車が同時に離れる( global synchronization) 대신, 조금씩 늘려나가는 거예요.

**등장 배경**: 1988년 Van Jacobson의論文「Congestion Avoidance and Control」에서 처음 제안되었으며, 이후 RFC 2581, RFC 5681 등으로 표준화되었다. 이후 SACK(选择性确认), ECN(명시적 혼잡 알림) 등의 확장 기능이 추가되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Slow Start와 Congestion Avoidance

TCP 연결이 시작되거나 재시작될 때, cwnd는 작은 값(일반적으로 1~10 MSS( Maximum Segment Size))에서 시작한다. Slow Start 단계에서는 각 ACK 수신 시 cwnd가 약 두 배로 증가한다(지수적 증가). cwnd가 Slow Start Threshold(ssthresh)에 도달하면 Congestion Avoidance 단계로 전환되어, 각 RTT마다 cwnd가 1 MSS씩線형적으로 증가한다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    Slow Start vs Congestion Avoidance                  │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Slow Start (cwnd < ssthresh):                                        │
│                                                                       │
│  cwnd = 1 MSS → 2 MSS → 4 MSS → 8 MSS → ... (지수적 증가)           │
│  ※ 각 ACK 수신 시 cwnd += MSS                                         │
│                                                                       │
│  Congestion Avoidance (cwnd >= ssthresh):                            │
│                                                                       │
│  cwnd += MSS * MSS / cwnd (매 RTT마다 1 MSS 증가)                    │
│  ※ 선형적으로 증가                                                     │
│                                                                       │
│  예시:                                                                │
│  MSS = 1460 bytes, RTT = 100ms                                        │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  Slow Start:                                                   │   │
│  │  RTT 1: cwnd = 1 MSS (1 KB)      → 1 RTT에 1 패킷            │   │
│  │  RTT 2: cwnd = 2 MSS (2 KB)      → 2 RTT에 2 패킷            │   │
│  │  RTT 3: cwnd = 4 MSS (4 KB)      → 4 RTT에 4 패킷            │   │
│  │  RTT 4: cwnd = 8 MSS (8 KB)      → 8 RTT에 8 패킷            │   │
│  │  ...                                                          │   │
│  │  10 RTT: cwnd ≈ 1 GB → 네트워크 용량 근접                      │   │
│  │                                                              │   │
│  │  Congestion Avoidance:                                         │   │
│  │  cwnd = 10 MSS → 11 MSS → 12 MSS → ... (선형)                 │   │
│  │  매 RTT마다 1 MSS씩 증가                                       │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  혼잡 감지 (손실 발생):                                                │
│  • Timeout:严厉한 손실 → ssthresh = cwnd/2, cwnd = 1 MSS (다시 Slow Start) │
│  • 3 중복 ACK: 경미한 손실 → ssthresh = cwnd/2, cwnd = ssthresh + 3 MSS   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Slow Start의 핵심 아이디어는「네트워크 용량을 사전에 알 수 없으므로, 실험적으로 탐색하자」이다. 첫 RTT에서 1 패킷을 보내고, ACK가 오면 2 패킷을 보내는 식으로 지수적으로 증가시킨다. 이렇게 하면 빠르게 네트워크 용량에 근접하면서도, 혼잡 발생 시的影响範囲を限定できる。 그러나 Slow Start는 목적지까지의往返 시간(RTT)에 비례하여 증가하므로, 초고대역폭 × 고지연 환경에서는 네트워크 용량에 도달하는 데 많은 시간이 걸린다(이를「Bandwidth-Delay Product」문제라 한다).

### AIMD (Additive Increase, Multiplicative Decrease)

AIMD는 혼잡 제어의 근본 원칙이다. 혼잡이 감지되지 않으면 선형적으로( additive) cwnd를 증가시키고, 혼잡이 감지되면乘法적으로( multiplicative) cwnd를 감소시킨다. 이 원칙은 모든 TCP 연결이 공정하게( fair) 대역폭을 공유하도록 한다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    AIMD (Additive Increase, Multiplicative Decrease)   │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  TCP 연결 A와 B가同一 네트워크를 공유하는 경우:                          │
│                                                                       │
│  ●                                                                    │
│  │                      /\ (/=3 ACK)                                 │
│  │                     /  \                                          │
│  │                    /    \ ← 곱하기적 감소 (cwnd /= 2)            │
│  │     /‾‾‾          /      \                                        │
│  │    /   \         /        \                                       │
│  │   /     \       /          \                                       │
│  │  /       \     /            \                                      │
│  │ /         \   /              \                                     │
│  │/           \ /                \                                    │
│  └──────────────────────────────────▶ 시간                          │
│  /\ = Timeout 또는 3 중복 ACK                                            │
│                                                                       │
│  과정:                                                                │
│  ① A와 B가 각각 cwnd=10으로 공유 중                                   │
│  ② 혼잡 발생 (Timeout) → 둘 다 cwnd /= 2 → cwnd=5                     │
│  ③ 선형적으로 증가 → cwnd=6 → cwnd=7 → cwnd=8...                      │
│  ④ 다시 혼잡 → 둘 다 cwnd /= 2 → cwnd=4                               │
│  ...                                                                  │
│  → 결국 두 연결은公平하게 대역폭을 분배                                  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │ 公平性 (Fairness) 수식:                                          │   │
│  │                                                                  │   │
│  │  두 TCP 연결의 대역폭 비율은 결국 1:1으로 수렴                    │   │
│  │  (같은 RTT 가정)                                                │   │
│  │                                                                  │   │
│  │  Bandwidth_A / Bandwidth_B = RTT_A / RTT_B (비례 공평)          │   │
│  │  ※ RTT가 작은 연결이 더 많은 대역폭을 확보                       │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** AIMD의 가장 큰 의장은「Global Synchronization 문제를 해결」한다는 것이다. 모든 TCP 연결이 동시에 같은 속도로 줄이고 또 같이 늘리면, 네트워크 utilization이 급격히 떨어졌다 올라갔다를 반복한다. AIMD에서는 혼잡 시 각 연결이 독립적으로 반응하여, 통계적으로全体の 트래픽이平滑化된다. 그러나 AIMD는「RTT가 짧은 연결이 유리」라는問題가 있다. 같은 cwnd라도 RTT가 짧으면 더 자주 ACK를 받고, 따라서 초당 throughput이 높아진다.

### Fast Retransmit과 Fast Recovery

TCP는 수신된 중복 ACK를 기반으로 손실된 세그먼트를 재전송한다. 3개의 중복 ACK가 수신되면, 해당 세그먼트가 분실되었음을 추정하고, RTO를 기다리지 않고 즉시 재전송한다(Fast Retransmit). 재전송 후 cwnd를 반감하고, 추가 ACK를 기다리며 계속 전송을 이어간다(Fast Recovery).

```
┌───────────────────────────────────────────────────────────────────────┐
│                    Fast Retransmit vs Fast Recovery                    │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【Fast Retransmit】                                                   │
│                                                                       │
│  상황: Segment 3이 분실된 경우                                          │
│                                                                       │
│  송신자 → [1][2][3][4][5] ────▶ 수신자                                 │
│  ◀─── [ACK=1] ────────────────  (Segment 1 수신, 다음 2 기다림)       │
│  ◀─── [ACK=1] ────────────────  (Segment 2 수신, 다음 2 기다림 - 중복) │
│  ◀─── [ACK=1] ────────────────  (Segment 2 수신, 다음 2 기다림 - 중복) │
│  ◀─── [ACK=1] ────────────────  (중복 ACK 3개)                         │
│       │                                                               │
│       │  ※ 3 중복 ACK = Segment 2 이후로 Segment 3 이후 것이 도착       │
│       │     → Segment 3이 분실되었지만, 일부 데이터는 수신됨            │
│       ▼                                                               │
│  [재전송: Segment 3] ────▶  (RTO 대기 없이 즉시)                        │
│                                                                       │
│  【Fast Recovery】                                                      │
│                                                                       │
│  Fast Retransmit 후:                                                  │
│  • cwnd = cwnd / 2 (또는 cwnd = ssthresh + 3)                         │
│  • ssthresh = cwnd / 2                                                │
│  • 추가 ACK가 오면 Congestion Avoidance로 전환                          │
│                                                                       │
│  ※ Timeout 발생 시는 Fast Recovery 없이, Slow Start로 완전히 복귀      │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  왜 3 중복 ACK인가:                                             │   │
│  │                                                               │   │
│  │  1-2 중복 ACK: 네트워크 경미한 순서 변경 (재정렬만)                │   │
│  │  3 중복 ACK: 확실한 분실 (Segment N 이후 도착 → N이 분실)         │   │
│  │  Timeout: 더 심한 문제 (아마도 심각한 혼잡)                        │   │
│  │                                                               │   │
│  │  → 상태에 따라 대응을 다르게 함 (轻微-快速再送信, 重度-慢启动)      │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Fast Retransmit의 핵심은「RTO(재전송 타임아웃)까지 기다리지 않고, 중복 ACK만으로 재전송」하는 것이다. RTO는 일반적으로 수백 ms ~ 수 초로, 그 동안 채널이 낭비된다. 반면 3 중복 ACK 상황에서는 상대방이 일시적으로 다음 세그먼트를 받을 수 없는 것이 아니라, 중간 세그먼트가 분실되었음을 거의 확실히 알 수 있으므로, 빠르게 재전송하여 지연 시간을 절약한다. Timeout은 더 심각한 상황(네트워크 경로 완전 차폐 또는 심각한 혼잡)을 나타내므로,严厉한 대응(Slow Start)이 필요하다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 혼잡 제어 알고리즘 비교

| 알고리즘 | 방식 | 특징 | 적용 |
|:---|:---|:---|:---|
| **Tahoe** | Slow Start → CA → Fast Retransmit → Slow Start | 초기 알고리즘 | 구식 |
| **Reno** | Tahoe + Fast Recovery | 1 패킷 손실에 효율적 | 보편적 |
| **NewReno** | Reno + Partial ACK 처리 | 다중 패킷 손실에 개선 | 기본 |
| **SACK** | 선택적 ACK | 손실 세그먼트 정확한 파악 | 거의 기본 |
| **CUBIC** | 비선형 (BIC에서 개선) | 고대역폭 환경에 최적 | Linux 기본 |
| **BBR** | 모델 기반 | 혼잡而非 손실 기반 | Google |

### ECN (Explicit Congestion Notification)

ECN은 패킷을 드롭하지 않고, 네트워크 혼잡을 송신자에게 알리는 메커니즘이다. 라우터가 혼잡 시 ECN 필드를 설정하고, 수신자가 이를 송신자에게ACK에 반영한다. 송신자는 혼잡을 감지하면 cwnd를 감소시킨다. 이를 통해丢包로 인한再送信レイテンシを削減できる。

```
┌───────────────────────────────────────────────────────────────────────┐
│                    ECN 동작 과정                                         │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ① 송신자: ECE (ECN-Echo) 플래그를 설정하여 패킷 전송                │
│  ② 라우터: 혼잡 시 ECN 필드를 CE (Congestion Experienced)로 표시      │
│  ③ 수신자: ECE 플래그를 수신하면, 응답 ACK에 ECE 플래그 설정          │
│  ④ 송신자: ECE 수신 시 cwnd 감소                                      │
│  ⑤ 송신자: 감소 후 CWR (Congestion Window Reduced) 플래그 전송        │
│  ⑥ 수신자: CWR 수신 시 ECE 전송 중지                                   │
│                                                                       │
│  ※ ECN이 동작하려면:                                                   │
│    • 송신자-수신자-네트워크(라우터) 모두 ECN 지원 필요                  │
│    • 현재 일부 네트워크에서 ECN 비활성화 상태                            │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 1 — 고대역폭 × 고지연 환경 (Satellite)**: 위성 네트워크에서는 RTT가 600ms 이상으로 매우 크다. Slow Start로 네트워크 용량에 도달하려면 수십 RTT가 소요된다.解决这个问题 위해, 큰 initial cwnd(IW) 설정이 권장된다. Linux 2.6.39+에서는 IW=10 MSS가 기본이며, 위성 환경에서는 더 큰 값이 유리하다.

**시나리오 2 — 데이터센터 네트워크 (DCTCP)**: 데이터센터 내부는 짧은 RTT(마이크로초~밀리초)와 낮은 혼잡이 특징이다. DCTCP( Data Center TCP)는 ECN을 활용하여 미세한 혼잡 수준을 파악하고, 부분적으로 cwnd를 조절한다. 이를 통해 레이턴시를 최소화하면서도 높은 throughput을 달성한다.

**시나리오 3 — BBR vs CUBIC**: Google이 개발한 BBR(Bottleneck Bandwidth and RTT)은 네트워크 버퍼 대신 실제 bandwidth-delay product(BDP)를 추정하여 동작한다. CUBIC 대비 낮은 큐잉 지연과 더 나은 성능을 제공하지만, 일부 네트워크 환경에서 다른 TCP 흐름과 공정하게 대역폭을 공유하지 못하는 문제가 있다.

### 도입 체크리스트

- **기술적**: 네트워크 환경에 맞는 혼잡 제어 알고리즘 선택 (대부분 기본값이 적절)
- **운영·보안적**: ECN 활성화 시 네트워크 장비가 이를 지원하는지 확인

### 안티패턴

- **비동기화 문제**: 일부 연결만 혼잡 제어를 비활성화하면, 해당 연결이 전체 대역폭을 독차지하여 다른 연결을 압도한다.
- **CUBIC의 RTT 공정성 문제**: CUBIC은 RTT에 비례하여 대역폭을 공유하므로, RTT가 짧은 연결이 불균형하게 더 많은 대역폭을 가질 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 혼잡 제어 없음 | 혼잡 제어 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | Global Synchronization → utilization 10% 미만 | utilization 70~90% | 네트워크 利用률 **8배 향상** |
| **정량** | 재전송 지연 1~5초 | 수십~수백 ms | 체감 지연 **90% 감소** |
| **정성** | 네트워크 불안정, 빈번한 타임아웃 | 안정적传输 | 서비스 신뢰성 향상 |

### 미래 전망

TCP 혼잡 제어는 끊임없이 발전하고 있다. BBR, LEDBAT, Naive 등 새로운 알고리즘이 등장하여 다양한 네트워크 환경에 최적화되고 있다. 특히 5G, Wi-Fi 6, Starlink 등 다양한 네트워크 환경에서 기존 알고리즘의 한계가 드러나면서, 상황 인식형 혼잡 제어( context-aware congestion control)가 연구되고 있다. QUIC에서는 혼잡 제어를 userspace에서 구현하여, 애플리케이션 레벨에서 최적화된 알고리즘을 선택할 수 있게 했다.

### 참고 표준

- RFC 5681 — TCP Congestion Control
- RFC 2581 — TCP Congestion Control (舊)
- RFC 7323 — TCP Window Scaling
- RFC 9000 — QUIC

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **cwnd (Congestion Window)** | 아직 ACK되지 않은 데이터의 최대 바이트 수로, 혼잡 제어의核心 변수의 하나이다. |
| **ssthresh** | Slow Start와 Congestion Avoidance를 구분하는 임계값이다. |
| **AIMD** | 혼잡 제어의 근본 원칙으로, 선형 증가와 곱하기 감소를 결합한다. |
| **Fast Retransmit** | 3 중복 ACK 시 RTO 대기 없이 즉시 재전송하는 메커니즘이다. |
| **ECN** | 패킷 드롭 대신 명시적 혼잡 알림을 제공하는 메커니즘이다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. TCP 혼잡 제어는 **물이 줄기에 동시에 많은 양동이를 붓지 않는 규칙**과 같아요. 먼저 한 두 항아리( slow start)를 채우고, 잘 되면 조금씩 늘려가면서( linear增加), 물이 넘치면( 혼잡) 절반으로 줄이고 다시 천천히 채워요.
2. Fast Retransmit은 **편지가 분실됐다는 신호**를 받은 것입니다. "3번 편지 못 받았어요!"라는 중복된 연락이 오면, 기다리지 않고 바로 재발송하는 거예요.
3. 하지만 물이 완전히 안 오면( timeout) 규칙을リセット하고 처음부터 다시 시작해야 해요. 그래서 인터넷은 물이 넘치지 않도록 서로 조율하면서大数据를 보내고 있어요!
