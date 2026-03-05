+++
title = "018. 큐잉 지연 (Queueing Delay) - 라우터 버퍼"
description = "큐잉 지연의 개념, 큐잉 이론, 혼잡과의 관계, 버퍼블로트 문제 및 최적화 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["QueueingDelay", "Bufferbloat", "Congestion", "RouterBuffer", "QueuingTheory", "AQM"]
categories = ["studynotes-3_network"]
+++

# 018. 큐잉 지연 (Queueing Delay) - 라우터 버퍼

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 큐잉 지연은 패킷이 라우터나 스위치의 출력 포트 버퍼에서 전송 대기하며 보내는 시간으로, 네트워크 혼잡도에 따라 0ms에서 수백 ms까지 변동하며 가장 예측 불가능한 지연 요소입니다.
> 2. **가치**: 링크 이용률이 80%를 넘으면 큐잉 지연이 급격히 증가하며(M/M/1 큐 이론), 버퍼블로트(Bufferbloat) 현상으로 인해 실시간 트래픽 품질이 심각하게 저하될 수 있습니다.
> 3. **융합**: 큐잉 지연 관리를 위해 AQM(Active Queue Management), CoDel, FQ_CoDel, WRED 등의 기법이 사용되며, DiffServ 기반 QoS로 트래픽별 차등 서비스가 제공됩니다.

---

## I. 개요 (Context & Background)

**큐잉 지연(Queueing Delay)**은 패킷이 라우터나 스위치의 **버퍼(Queue)**에서 출력 포트로 전송되기를 기다리며 보내는 시간입니다. 전파 지연과 전송 지연이 물리적 요인에 의해 결정되는 반면, 큐잉 지연은 **네트워크 트래픽 상태**에 따라 크게 변동합니다.

### 큐잉 지연의 특징

1. **가변성**: 0ms부터 수백 ms까지 변동
2. **혼잡 의존성**: 트래픽이 많을수록 증가
3. **예측 불가능성**: 실시간 트래픽 패턴에 따라 급변
4. **버퍼 크기 영향**: 큰 버퍼는 지연 증가, 작은 버퍼는 패킷 손실

### 큐잉 지연 발생 원인

```
                    출력 포트
                       ↓
입력 패킷 ──> [ 버퍼 ] ──> 전송
              ↑
           대기열
```

- 입력 속도 > 출력 속도 → 버퍼에 패킷 축적
- 버퍼가 가득 차면 → 패킷 폐기 (Tail Drop)
- 앞의 패킷이 처리될 때까지 대기 → 큐잉 지연

**💡 비유**: 큐잉 지연을 **'은행 창구 대기'**에 비유할 수 있습니다.

- 당신(패킷)이 은행에 도착했습니다.
- 창구 직원(출력 포트)은 1명이고, 1분에 1명을 처리합니다.
- 앞에 10명이 대기 중이라면(버퍼에 10개 패킷), 당신은 10분을 기다려야 합니다. 이것이 **큐잉 지연**입니다.

**대기열이 없다면?** → 큐잉 지연 = 0
**대기열이 100명이라면?** → 큐잉 지연 = 100분

**변동성**: 당신이 갔을 때 대기열이 몇 명인지는 예측할 수 없습니다. 아침 9시에는 비어 있을 수도, 점심시간에는 50명이 있을 수도 있습니다.

**등장 배경 및 발전 과정**:

1. **초기 패킷 교환망**: 1970년대 ARPANET에서 버퍼 오버플로우로 인한 패킷 손실이 빈번했습니다.

2. **큐잉 이론의 적용**: 1980년대 M/M/1, M/M/1/K 등의 큐잉 모델이 네트워크 성능 분석에 도입되었습니다.

3. **TCP 혼잡 제어와의 연계**: 1990년대 TCP Reno의 혼잡 제어가 큐잉 지연과 상호작용한다는 점이 인식되었습니다.

4. **버퍼블로트(Bufferbloat) 발견**: 2010년대 대용량 버퍼가 오히려 지연을 악화시킨다는 문제가 대두되었습니다.

5. **AQM 기술의 표준화**: CoDel, FQ_CoDel 등의 Active Queue Management 기술이 개발되어 리눅스 커널에 탑재되었습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 상세 역할 | 단위 | 영향 요인 | 비고 |
|---------|------|----------|------|----------|------|
| **λ** | 도착률 | 패킷 도착 속도 | pps | 트래픽 부하 | 입력 |
| **μ** | 서비스율 | 패킷 처리 속도 | pps | 링크 속도 | 출력 |
| **ρ** | 이용률 | λ/μ | 무차원 | 0~1 | 혼잡도 |
| **L** | 평균 패킷 길이 | bits | bits | MTU, MSS | - |
| **K** | 버퍼 크기 | 패킷 수 | 개 | 메모리 | 제한 |
| **d_queue** | 큐잉 지연 | 대기 시간 | ms | ρ, K | 가변 |

### 정교한 구조 다이어그램: 라우터 큐 구조

```ascii
================================================================================
[ 라우터 출력 포트 큐 구조 ]
================================================================================

                     입력 포트들
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Ingress │    │ Ingress │    │ Ingress │
    │ Port 1  │    │ Port 2  │    │ Port 3  │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Switching Fabric  │
              │    (스위칭 패브릭)   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Egress Queue      │
              │   (출력 큐)         │
              │ ┌───┬───┬───┬───┐  │
              │ │ P │ P │ P │...│  │ ← 버퍼 (Buffer)
              │ └───┴───┴───┴───┘  │
              │   Tail      Head    │
              │    ↑         │      │
              │   입구      출구    │
              └──────────┬──────────┘
                         │
                         ▼
                    출력 포트
                    (링크 속도 R)


================================================================================
[ M/M/1 큐 모델 - 이용률에 따른 큐잉 지연 ]
================================================================================

큐잉 지연 공식 (M/M/1):

d_queue = (1/μ) × (ρ / (1-ρ))

여기서:
- 1/μ = 서비스 시간 = L/R (패킷 전송 시간)
- ρ = λ/μ = 이용률

이용률(ρ)    상대 지연(1/(1-ρ))    예시 (1 Gbps, 1500B)
──────────────────────────────────────────────────────
0.10         1.11x                 13.3 μs
0.25         1.33x                 16.0 μs
0.50         2.00x                 24.0 μs
0.75         4.00x                 48.0 μs
0.80         5.00x                 60.0 μs
0.90        10.00x                120.0 μs
0.95        20.00x                240.0 μs
0.99       100.00x              1,200.0 μs = 1.2 ms

※ 이용률 90%에서 큐잉 지연이 10배 증가!
  이용률 99%에서 큐잉 지연이 100배 증가!


================================================================================
[ 버퍼블로트 (Bufferbloat) 현상 ]
================================================================================

문제 상황: 과도하게 큰 버퍼

┌─────────────────────────────────────────────────────────────────────────┐
│                    큰 버퍼를 가진 라우터                                 │
│                                                                         │
│   ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐       │
│   │ TCP │ TCP │ TCP │ TCP │ TCP │ TCP │ TCP │ TCP │ TCP │ ... │       │
│   │ Bulk│Bulk │Bulk │Bulk │Bulk │Bulk │Bulk │Bulk │Bulk │     │       │
│   └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘       │
│                         ↑                                               │
│                   대용량 다운로드로                                      │
│                   버퍼가 가득 참                                         │
│                                                                         │
│   ┌─────┐                                                               │
│   │VoIP │ ← 실시간 패킷이 버퍼 끝에서 대기                               │
│   └─────┘   지연 = (버퍼 내 패킷 수) × (패킷 전송 시간)                   │
│                                                                         │
│   예: 1000개 패킷 대기 × 12μs = 12ms 지연 (VoIP에 치명적!)              │
└─────────────────────────────────────────────────────────────────────────┘

해결: AQM (Active Queue Management)

┌─────────────────────────────────────────────────────────────────────────┐
│                    AQM이 적용된 라우터                                   │
│                                                                         │
│   ┌─────┬─────┬─────┬─────┬─────┐                                       │
│   │ TCP │ TCP │ TCP │ TCP │ TCP │  ← 버퍼 크기를 작게 유지               │
│   └─────┴─────┴─────┴─────┴─────┘     (ECN 표시 또는 조기 폐기)         │
│                                                                         │
│   ┌─────┐                                                               │
│   │VoIP │ ← 실시간 패킷이 빠르게 처리됨                                  │
│   └─────┘   지연 최소화!                                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


================================================================================
[ AQM 알고리즘 비교 ]
================================================================================

┌──────────────┬──────────────────────────────────────────────────────────┐
│  Drop Tail   │ 버퍼가 가득 차면 도착하는 패킷 폐기                       │
│  (기본)      │ 문제: 글로벌 동기화, 큰 지연                              │
├──────────────┼──────────────────────────────────────────────────────────┤
│    RED       │ 확률적 조기 폐기 (Random Early Detection)                │
│              │ 버퍼가 찌그러들기 전에 미리 폐기 시작                      │
├──────────────┼──────────────────────────────────────────────────────────┤
│   WRED       │ Weighted RED - 트래픽 클래스별 다른 폐기 확률             │
│              │ QoS와 연계하여 우선순위 높은 트래픽 보호                   │
├──────────────┼──────────────────────────────────────────────────────────┤
│   CoDel      │ Controlled Delay - 지연 시간 기반 폐기                    │
│              │ "지연이 5ms 이상 100ms간 지속되면 폐기"                   │
├──────────────┼──────────────────────────────────────────────────────────┤
│  FQ_CoDel    │ Fair Queue CoDel - 흐름별 공정 큐잉                       │
│              │ 각 TCP 흐름에 공정하게 대역폭 분배 + CoDel 지연 제어      │
└──────────────┴──────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 큐잉 이론 기초

1. **M/M/1 큐 모델**:
   - M (Markovian): 포아송 도착, 지수 서비스 시간
   - 1: 단일 서버 (출력 포트)
   - 가정: 무한 버퍼, FIFO 서비스

2. **평균 대기 시간**:
   ```
   W = (1/μ) × (ρ / (1-ρ))
   ```
   - ρ → 1일 때 W → ∞ (혼잡 붕괴)

3. **M/M/1/K 큐 (유한 버퍼)**:
   ```
   패킷 손실 확률: P_loss = (1-ρ)ρ^K / (1-ρ^(K+1))
   ```
   - K가 작으면 손실 증가, 지연 감소
   - K가 크면 손실 감소, 지연 증가

4. **Little's Law**:
   ```
   L = λ × W
   ```
   - L: 시스템 내 평균 패킷 수
   - λ: 도착률
   - W: 평균 체류 시간

### 핵심 수식

```
이용률:
ρ = λ / μ = (패킷 도착률) / (패킷 서비스율)

M/M/1 평균 큐잉 지연:
d_queue = (1/μ) × (ρ / (1-ρ))

서비스 시간:
1/μ = L / R = (평균 패킷 길이) / (링크 속도)

버퍼 크기 권장 (Rule of Thumb):
B = C × RTT
- B: 버퍼 크기 (bits)
- C: 링크 용량 (bps)
- RTT: 왕복 시간 (s)

예: 10 Gbps 링크, 100ms RTT
B = 10^10 × 0.1 = 10^9 bits = 125 MB
```

### 핵심 코드: 큐잉 지연 시뮬레이터

```python
import random
import math
from dataclasses import dataclass
from typing import List, Optional
from collections import deque
from enum import Enum

class PacketType(Enum):
    BULK = "bulk"       # 대용량 전송 (TCP)
    REALTIME = "realtime"  # 실시간 (VoIP, 게임)
    CONTROL = "control"  # 제어 (ACK, DNS)

@dataclass
class Packet:
    """패킷 정의"""
    id: int
    size_bytes: int
    arrival_time: float
    packet_type: PacketType
    flow_id: int = 0

class QueueStatistics:
    """큐 통계"""
    def __init__(self):
        self.total_packets = 0
        self.dropped_packets = 0
        self.queue_delays: List[float] = []
        self.queue_lengths: List[int] = []

    @property
    def drop_rate(self) -> float:
        if self.total_packets == 0:
            return 0
        return self.dropped_packets / self.total_packets

    @property
    def avg_delay(self) -> float:
        if not self.queue_delays:
            return 0
        return sum(self.queue_delays) / len(self.queue_delays)

class NetworkQueue:
    """
    네트워크 큐 시뮬레이터
    """
    def __init__(self, service_rate_pps: float, buffer_size: int):
        """
        Args:
            service_rate_pps: 초당 패킷 처리율 (packets per second)
            buffer_size: 버퍼 크기 (패킷 수)
        """
        self.service_rate = service_rate_pps
        self.buffer_size = buffer_size
        self.queue: deque = deque()
        self.stats = QueueStatistics()
        self.current_time = 0.0

    def enqueue(self, packet: Packet) -> bool:
        """
        패킷 큐에 추가

        Returns:
            True if accepted, False if dropped
        """
        self.stats.total_packets += 1

        if len(self.queue) >= self.buffer_size:
            self.stats.dropped_packets += 1
            return False

        self.queue.append(packet)
        return True

    def dequeue(self) -> Optional[Packet]:
        """패킷 처리"""
        if not self.queue:
            return None
        return self.queue.popleft()

    def get_queue_delay(self, packet: Packet) -> float:
        """큐잉 지연 계산"""
        queue_length = len(self.queue)
        service_time = 1 / self.service_rate
        return queue_length * service_time

class M_M_1_Queue:
    """
    M/M/1 큐 이론 모델
    """
    def __init__(self, arrival_rate: float, service_rate: float):
        """
        Args:
            arrival_rate: 패킷 도착률 (λ)
            service_rate: 패킷 서비스율 (μ)
        """
        self.lambda_ = arrival_rate
        self.mu = service_rate

    @property
    def utilization(self) -> float:
        """이용률 (ρ)"""
        return self.lambda_ / self.mu

    def avg_queue_length(self) -> float:
        """평균 큐 길이 (Lq)"""
        rho = self.utilization
        if rho >= 1:
            return float('inf')
        return (rho ** 2) / (1 - rho)

    def avg_system_size(self) -> float:
        """시스템 내 평균 패킷 수 (L)"""
        rho = self.utilization
        if rho >= 1:
            return float('inf')
        return rho / (1 - rho)

    def avg_queue_delay(self) -> float:
        """평균 큐잉 지연 (Wq)"""
        rho = self.utilization
        if rho >= 1:
            return float('inf')
        return (1 / self.mu) * (rho / (1 - rho))

    def avg_system_time(self) -> float:
        """평균 체류 시간 (W)"""
        rho = self.utilization
        if rho >= 1:
            return float('inf')
        return 1 / (self.mu - self.lambda_)

class BufferbloatSimulator:
    """
    버퍼블로트 시뮬레이터
    """
    def __init__(self, link_speed_bps: int, buffer_size_packets: int,
                 avg_packet_size: int = 1500):
        """
        Args:
            link_speed_bps: 링크 속도 (bps)
            buffer_size_packets: 버퍼 크기 (패킷 수)
            avg_packet_size: 평균 패킷 크기 (bytes)
        """
        self.link_speed = link_speed_bps
        self.buffer_size = buffer_size_packets
        self.packet_size = avg_packet_size

        # 패킷당 서비스 시간
        self.service_time = (avg_packet_size * 8) / link_speed_bps

    def max_queueing_delay(self) -> float:
        """최대 큐잉 지연 (버퍼가 가득 찼을 때)"""
        return self.buffer_size * self.service_time * 1000  # ms

    def analyze_utilization(self, load_percent: float) -> dict:
        """
        특정 부하에서의 큐잉 지연 분석
        """
        rho = load_percent / 100
        if rho >= 1:
            return {'error': 'Overloaded'}

        # M/M/1 근사
        relative_delay = 1 / (1 - rho)
        absolute_delay = self.service_time * relative_delay * 1000  # ms

        return {
            'utilization': rho,
            'relative_delay_factor': relative_delay,
            'avg_queueing_delay_ms': absolute_delay,
            'buffer_delay_ms': self.max_queueing_delay()
        }

class CoDelAQM:
    """
    CoDel (Controlled Delay) AQM 시뮬레이터
    """
    def __init__(self, target: float = 5.0, interval: float = 100.0):
        """
        Args:
            target: 목표 지연 (ms)
            interval: 지속 시간 (ms)
        """
        self.target = target / 1000  # seconds
        self.interval = interval / 1000  # seconds
        self.first_above_time = 0
        self.drop_next = 0
        self.count = 0
        self.dropping = False

    def should_drop(self, sojourn_time: float, current_time: float) -> bool:
        """
        패킷 폐기 여부 결정

        Args:
            sojourn_time: 패킷 체류 시간 (seconds)
            current_time: 현재 시간 (seconds)

        Returns:
            True if packet should be dropped
        """
        if sojourn_time < self.target:
            # 목표 지연 미만 - 정상 상태
            self.dropping = False
            self.first_above_time = 0
            return False

        # 목표 지연 초과
        if self.first_above_time == 0:
            self.first_above_time = current_time + self.interval
            return False

        if current_time < self.first_above_time:
            return False

        # interval 동안 지연 초과 지속
        if not self.dropping:
            self.dropping = True
            self.drop_next = current_time
            self.count = 1
            return True

        if current_time >= self.drop_next:
            self.count += 1
            self.drop_next = current_time + self.interval / self.count
            return True

        return False

# 실무 사용 예시
if __name__ == "__main__":
    # 1. M/M/1 큐 분석
    print("=" * 60)
    print("M/M/1 큐 분석 (서비스율 1000 pps)")
    print("=" * 60)

    service_rate = 1000  # packets per second

    for arrival_rate in [100, 500, 800, 900, 950, 990]:
        queue = M_M_1_Queue(arrival_rate, service_rate)
        rho = queue.utilization
        delay = queue.avg_queue_delay() * 1000  # ms

        print(f"도착률 {arrival_rate:4d} pps (ρ={rho:.2f}): "
              f"평균 큐잉 지연 = {delay:8.2f} ms")

    # 2. 버퍼블로트 분석
    print("\n" + "=" * 60)
    print("버퍼블로트 분석 (1 Gbps, 1000 패킷 버퍼)")
    print("=" * 60)

    bb_sim = BufferbloatSimulator(
        link_speed_bps=1_000_000_000,
        buffer_size_packets=1000,
        avg_packet_size=1500
    )

    print(f"최대 큐잉 지연 (버퍼 full): {bb_sim.max_queueing_delay():.2f} ms")

    for load in [50, 75, 90, 95, 99]:
        analysis = bb_sim.analyze_utilization(load)
        print(f"부하 {load:3d}%: 평균 지연 = {analysis['avg_queueing_delay_ms']:.2f} ms")

    # 3. CoDel AQM 시뮬레이션
    print("\n" + "=" * 60)
    print("CoDel AQM 시뮬레이션 (target=5ms, interval=100ms)")
    print("=" * 60)

    codel = CoDelAQM(target=5.0, interval=100.0)

    # 다양한 지연 시나리오
    scenarios = [
        (0.003, "정상 (3ms)"),
        (0.010, "초과 (10ms)"),
        (0.020, "과부하 (20ms)"),
    ]

    for delay, desc in scenarios:
        drops = []
        for i in range(200):
            t = i * 0.001  # 1ms 간격
            drop = codel.should_drop(delay, t)
            drops.append(drop)

        drop_count = sum(drops)
        print(f"{desc}: 200패킷 중 {drop_count}개 폐기 ({drop_count/2:.1f}%)")
