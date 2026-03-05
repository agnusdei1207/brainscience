+++
title = "015. 지연 (Latency/Delay) - 데이터 관점"
description = "네트워크 지연의 개념, 구성 요소, 측정 방법 및 최적화 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["Latency", "Delay", "RTT", "Ping", "OneWayDelay", "Jitter", "NetworkPerformance"]
categories = ["studynotes-3_network"]
+++

# 015. 지연 (Latency/Delay) - 데이터 관점

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지연(Latency)은 데이터가 소스에서 목적지까지 도달하는 데 걸리는 총 시간으로, 전파 지연, 전송 지연, 처리 지연, 큐잉 지연의 합으로 구성되며, 단방향 지연(One-way Delay)과 왕복 지연(RTT, Round Trip Time)으로 구분됩니다.
> 2. **가치**: 지연은 사용자 체감 품질(QoE)에 직접적인 영향을 미치며, 실시간 애플리케이션(VoIP, 온라인 게임, 원격 수술)에서는 100ms 이하의 초저지연이 필수적입니다. 5G uRLLC는 1ms 지연을 목표로 합니다.
> 3. **융합**: 지연 최적화를 위해서는 CDN 엣지 배치, TCP Fast Open, QUIC 0-RTT, Edge Computing, 프리페칭 등이 복합적으로 적용되며, 네트워크 경로 최적화와 프로토콜 효율화가 결합됩니다.

---

## I. 개요 (Context & Background)

**지연(Latency 또는 Delay)**은 데이터 패킷이 송신측에서 생성되어 수신측에 도달할 때까지 걸리는 시간입니다. 대역폭이 "얼마나 많은 데이터를 보낼 수 있는가"를 나타낸다면, 지연은 "데이터가 얼마나 빨리 도착하는가"를 나타냅니다.

### 지연의 주요 구성 요소

네트워크 지연은 일반적으로 다음 4가지 요소의 합으로 구성됩니다:

1. **전파 지연 (Propagation Delay)**: 신호가 물리적 매체를 통해 이동하는 시간
2. **전송 지연 (Transmission Delay)**: 패킷을 링크에 밀어 넣는 시간
3. **처리 지연 (Processing Delay)**: 라우터/스위치에서 헤더 검사 및 라우팅 결정 시간
4. **큐잉 지연 (Queueing Delay)**: 라우터 버퍼에서 대기하는 시간

```
총 지연 = 전파 지연 + 전송 지연 + 처리 지연 + 큐잉 지연
```

### 단방향 지연 vs 왕복 지연

- **단방향 지연 (One-Way Delay, OWD)**: 소스 → 목적지까지의 시간
- **왕복 지연 (Round-Trip Time, RTT)**: 소스 → 목적지 → 소스까지의 시간
- 일반적으로 **RTT ≈ 2 × OWD** (대칭 경로 가정)

**💡 비유**: 지연을 **'우편 배송 시간'**에 비유할 수 있습니다.

- **전파 지연**은 **트럭이 도로를 달리는 시간**입니다. 거리가 멀수록 오래 걸립니다. 서울에서 부산까지는 약 4시간, 미국까지는 비행기로 약 14시간입니다.

- **전송 지연**은 **트럭에 짐을 싣는 시간**입니다. 1톤짜리 택배를 싣는 것은 1분이면 되지만, 10톤 컨테이너는 10분이 걸립니다.

- **처리 지연**은 **물류 센터에서 분류하는 시간**입니다. 주소를 확인하고 어느 트럭에 실을지 결정합니다.

- **큐잉 지연**은 **물류 센터에서 대기하는 시간**입니다. 앞에 다른 택배가 많으면 기다려야 합니다.

**등장 배경 및 발전 과정**:

1. **초기 네트워크의 지연 인식**: 1960년대 ARPANET에서 왕복 시간이 몇 초에 달했습니다. 이는 당시의 낮은 전송 속도와 긴 경로 때문이었습니다.

2. **광통신의 도래**: 1980년대 광섬유가 보급되면서 전파 지연이 크게 단축되었습니다. 빛의 속도(약 200,000 km/s in fiber)가 전기 신호보다 빠르기 때문입니다.

3. **실시간 애플리케이션의 등장**: 1990년대 VoIP, 2000년대 온라인 게임, 2010년대 클라우드 게임이 등장하면서 지연이 중요한 품질 지표가 되었습니다.

4. **초저지연 통신**: 5G uRLLC(Ultra-Reliable Low Latency Communications)는 1ms 이하의 지연을 목표로 하며, 자율주행, 원격 수술, 산업 자동화를 가능하게 합니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 상세 역할 | 단위 | 영향 요인 | 비고 |
|---------|------|----------|------|----------|------|
| **d_prop** | 전파 지연 | 신호 이동 시간 | ms, s | 거리/전파 속도 | d/v |
| **d_trans** | 전송 지연 | 패킷 송출 시간 | ms, s | 패킷크기/대역폭 | L/R |
| **d_proc** | 처리 지연 | 라우팅 처리 | μs, ms | 장비 성능 | ASIC 가속 |
| **d_queue** | 큐잉 지연 | 버퍼 대기 | ms | 혼잡도 | 가변적 |
| **OWD** | 단방향 지연 | 송신→수신 | ms | 상기 4개 합 | 측정 어려움 |
| **RTT** | 왕복 지연 | 송신→수신→송신 | ms | ≈ 2 × OWD | Ping 측정 |
| **Jitter** | 지터 | 지연 변동 | ms | RTT 편차 | 실시간 품질 |

### 정교한 구조 다이어그램: 지연 구성 요소

```ascii
================================================================================
[ 패킷 지연의 4가지 구성 요소 ]
================================================================================

송신 호스트                            수신 호스트
┌─────────────┐                      ┌─────────────┐
│ Application │                      │ Application │
└──────┬──────┘                      └──────▲──────┘
       │                                    │
       │ 패킷 생성                          │ 패킷 수신
       ▼                                    │
┌─────────────┐                      ┌──────┴──────┐
│   TCP/IP    │                      │   TCP/IP    │
│   Stack     │                      │   Stack     │
└──────┬──────┘                      └──────▲──────┘
       │                                    │
       │ d_trans (전송 지연)                │
       │ = L / R                           │
       ▼                                    │
┌─────────────┐    d_prop (전파 지연) ┌──────┴──────┐
│   NIC       │ ────────────────────> │   NIC       │
│   송신      │    = d / v           │   수신      │
└─────────────┘                       └─────────────┘

                    ┌─────────────────────────────────┐
                    │         라우터 (Router)          │
                    │                                  │
   패킷 진입 ─────> │  ┌─────────┐    ┌─────────┐    │ ─────> 패킷 출발
                    │  │입력 인터페이스│──>│ 스위칭  │    │
                    │  └─────────┘    │ 패브릭  │    │
                    │       │         └────┬────┘    │
                    │       │              │         │
                    │       ▼              ▼         │
                    │  ┌─────────┐    ┌─────────┐    │
                    │  │ d_proc  │    │ d_queue │    │
                    │  │처리 지연 │    │큐잉 지연 │    │
                    │  └─────────┘    └─────────┘    │
                    │                                  │
                    └─────────────────────────────────┘


================================================================================
[ 전파 지연 (Propagation Delay) 상세 ]
================================================================================

전파 지연 공식: d_prop = 거리(d) / 전파 속도(v)

전파 속도:
- 진공 중 빛: 299,792 km/s (약 3 × 10⁸ m/s)
- 광섬유 중 빛: 약 200,000 km/s (굴절률 1.5)
- 동축 케이블: 약 200,000 km/s
- 무선 전파: 약 300,000 km/s (공기 중)

예시:
- 서울-부산 (400 km, 광섬유): 400/200,000 = 2 ms
- 서울-뉴욕 (11,000 km, 광섬유): 11,000/200,000 = 55 ms
- 서울-위성 (36,000 km × 2, 무선): 72,000/300,000 = 240 ms
- 지구-달 (384,000 km): 1.28초


================================================================================
[ 전송 지연 (Transmission Delay) 상세 ]
================================================================================

전송 지연 공식: d_trans = 패킷 길이(L) / 전송 속도(R)

예시:
- 1500바이트 패킷, 1 Mbps 링크: (1500 × 8) / 10⁶ = 12 ms
- 1500바이트 패킷, 1 Gbps 링크: (1500 × 8) / 10⁹ = 0.012 ms = 12 μs
- 64바이트 패킷, 1 Gbps 링크: (64 × 8) / 10⁹ = 0.512 μs


================================================================================
[ 처리 지연 (Processing Delay) 상세 ]
================================================================================

처리 지연 구성요소:
1. 헤더 검사: 목적지 주소 확인
2. 라우팅 테이블 조회: 출력 인터페이스 결정
3. TTL 감소: IPv4 TTL 필드 감소
4. 체크섬 검증/계산
5. QoS 분류

처리 지연 범위:
- 소비자용 라우터: 1~10 ms
- 엔터프라이즈 라우터: 0.1~1 ms
- 데이터센터 스위치 (ASIC): 1~10 μs


================================================================================
[ 큐잉 지연 (Queueing Delay) 상세 ]
================================================================================

큐잉 지연 특성:
- 가장 변동성이 큰 지연 요소
- 트래픽 부하에 따라 0 ~ 수백 ms까지 변동
- 버퍼 크기와 트래픽 패턴에 의존

큐잉 지연 공식 (M/M/1 큐 근사):
d_queue = (L/R) × (ρ / (1 - ρ))

여기서:
- L: 평균 패킷 길이
- R: 링크 전송 속도
- ρ: 링크 이용률 (0 < ρ < 1)

이용률별 큐잉 지연 (1 Gbps, 1500B 평균):
- ρ = 0.5: 12 μs × 1 = 12 μs
- ρ = 0.8: 12 μs × 4 = 48 μs
- ρ = 0.9: 12 μs × 9 = 108 μs
- ρ = 0.99: 12 μs × 99 = 1.188 ms
```

### 심층 동작 원리: 지연 측정 메커니즘

1. **Ping (ICMP Echo Request/Reply)**:
   - ICMP Echo Request 전송 시 시간 기록
   - Echo Reply 수신 시 시간 기록
   - RTT = 수신 시간 - 송신 시간
   - 한계: ICMP가 우선순위에서 밀릴 수 있음

2. **TCP 핸드셰이크 기반 측정**:
   - SYN 전송 시간 기록
   - SYN+ACK 수신 시간 기록
   - RTT = 수신 시간 - 송신 시간

3. **단방향 지연 측정 (OWD)**:
   - 양측 시계 동기화 필수 (PTP, NTP)
   - 송신측 타임스탬프와 수신측 타임스탬프 차이
   - 한계: 시계 동기화 오차가 측정에 포함됨

4. **왕복 지연 변동성 (Jitter)**:
   - 연속적인 RTT 측정값의 표준편차
   - VoIP, 비디오 스트리밍에서 중요한 품질 지표

### 핵심 수식: 지연 계산

```
총 지연 (Total Delay):

d_total = d_prop + d_trans + d_proc + d_queue

전파 지연: d_prop = d / v
- d: 거리 (m)
- v: 전파 속도 (m/s)

전송 지연: d_trans = L / R
- L: 패킷 길이 (bits)
- R: 전송 속도 (bps)

처리 지연: d_proc (장비 의존적)
- 일반적 범위: μs ~ ms

큐잉 지연: d_queue (트래픽 의존적)
- 이론적 근사: (L/R) × (ρ / (1-ρ))
- ρ: 링크 이용률
```

### 핵심 코드: 지연 분석기

```python
import time
import socket
import struct
import statistics
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

class DelayType(Enum):
    PROPAGATION = "전파 지연"
    TRANSMISSION = "전송 지연"
    PROCESSING = "처리 지연"
    QUEUEING = "큐잉 지연"

@dataclass
class DelayMeasurement:
    """지연 측정 결과"""
    timestamp: float
    rtt_ms: float
    owd_ms: Optional[float] = None

class DelayAnalyzer:
    """
    네트워크 지연 분석기
    """

    # 전파 속도 (m/s)
    PROPAGATION_SPEEDS = {
        'fiber': 200_000_000,      # 광섬유
        'copper': 200_000_000,     # 동축 케이블
        'wireless': 300_000_000,   # 무선 (공기 중)
        'vacuum': 299_792_458      # 진공
    }

    def __init__(self):
        self.measurements: List[DelayMeasurement] = []

    def calculate_propagation_delay(self, distance_km: float,
                                    medium: str = 'fiber') -> float:
        """
        전파 지연 계산

        Args:
            distance_km: 거리 (km)
            medium: 전송 매체 ('fiber', 'copper', 'wireless', 'vacuum')

        Returns:
            전파 지연 (ms)
        """
        distance_m = distance_km * 1000
        speed = self.PROPAGATION_SPEEDS.get(medium, 200_000_000)
        delay_seconds = distance_m / speed
        return delay_seconds * 1000  # ms 변환

    def calculate_transmission_delay(self, packet_size_bytes: int,
                                     link_speed_bps: int) -> float:
        """
        전송 지연 계산

        Args:
            packet_size_bytes: 패킷 크기 (bytes)
            link_speed_bps: 링크 속도 (bps)

        Returns:
            전송 지연 (ms)
        """
        packet_bits = packet_size_bytes * 8
        delay_seconds = packet_bits / link_speed_bps
        return delay_seconds * 1000  # ms 변환

    def calculate_total_delay(self, distance_km: float,
                              packet_size_bytes: int,
                              link_speed_bps: int,
                              num_hops: int = 1,
                              processing_delay_per_hop_ms: float = 0.1,
                              queueing_factor: float = 1.0) -> dict:
        """
        총 지연 계산

        Args:
            distance_km: 총 거리 (km)
            packet_size_bytes: 패킷 크기 (bytes)
            link_speed_bps: 링크 속도 (bps)
            num_hops: 홉 수
            processing_delay_per_hop_ms: 홉당 처리 지연 (ms)
            queueing_factor: 큐잉 지연 승수 (1.0 = 기본)

        Returns:
            지연 구성 요소 딕셔너리
        """
        # 전파 지연
        d_prop = self.calculate_propagation_delay(distance_km)

        # 전송 지연 (홉 수만큼 반복)
        d_trans = self.calculate_transmission_delay(packet_size_bytes, link_speed_bps) * num_hops

        # 처리 지연
        d_proc = processing_delay_per_hop_ms * num_hops

        # 큐잉 지연 (추정)
        base_queue = 0.1  # 기본 큐잉 지연 (ms)
        d_queue = base_queue * queueing_factor * num_hops

        return {
            'propagation_ms': d_prop,
            'transmission_ms': d_trans,
            'processing_ms': d_proc,
            'queueing_ms': d_queue,
            'total_ms': d_prop + d_trans + d_proc + d_queue
        }

class RTTMeasurer:
    """
    RTT 측정기 (TCP 기반)
    """
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def measure_tcp_rtt(self, host: str, port: int = 80) -> Optional[float]:
        """
        TCP 연결을 통한 RTT 측정

        Returns:
            RTT (ms) 또는 None (실패 시)
        """
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((host, port))
            end_time = time.time()
            sock.close()

            rtt = (end_time - start_time) * 1000  # ms 변환
            return rtt
        except Exception as e:
            print(f"연결 실패: {e}")
            return None

    def measure_multiple(self, host: str, port: int = 80,
                         count: int = 10) -> List[float]:
        """다중 RTT 측정"""
        rtts = []
        for _ in range(count):
            rtt = self.measure_tcp_rtt(host, port)
            if rtt is not None:
                rtts.append(rtt)
            time.sleep(0.1)
        return rtts

class JitterCalculator:
    """
    지터(Jitter) 계산기
    """
    @staticmethod
    def calculate_jitter(rtts: List[float]) -> dict:
        """
        지터 계산

        Args:
            rtts: RTT 측정값 리스트 (ms)

        Returns:
            지터 통계 딕셔너리
        """
        if len(rtts) < 2:
            return {'jitter_ms': 0, 'min_ms': 0, 'max_ms': 0}

        # 연속적인 RTT 차이의 절대값
        differences = [abs(rtts[i+1] - rtts[i]) for i in range(len(rtts)-1)]

        # RFC 3550 방식의 지터 계산 (평균)
        jitter = statistics.mean(differences)

        return {
            'jitter_ms': jitter,
            'min_rtt_ms': min(rtts),
            'max_rtt_ms': max(rtts),
            'avg_rtt_ms': statistics.mean(rtts),
            'std_dev_ms': statistics.stdev(rtts) if len(rtts) > 1 else 0,
            'range_ms': max(rtts) - min(rtts)
        }

class DelayBudgetAnalyzer:
    """
    지연 예산 분석기 (실시간 애플리케이션용)
    """
    # 애플리케이션별 권장 지연 예산 (ms)
    DELAY_BUDGETS = {
        'voip': {'one_way': 150, 'rtt': 300},
        'video_conference': {'one_way': 200, 'rtt': 400},
        'online_gaming': {'one_way': 50, 'rtt': 100},
        'cloud_gaming': {'one_way': 30, 'rtt': 60},
        'remote_surgery': {'one_way': 10, 'rtt': 20},
        'autonomous_driving': {'one_way': 5, 'rtt': 10},
    }

    def analyze_delay_budget(self, application: str,
                            measured_owd_ms: float) -> dict:
        """
        지연 예산 분석

        Args:
            application: 애플리케이션 유형
            measured_owd_ms: 측정된 단방향 지연 (ms)

        Returns:
            지연 예산 분석 결과
        """
        budget = self.DELAY_BUDGETS.get(application.lower())
        if not budget:
            return {'error': f'알 수 없는 애플리케이션: {application}'}

        budget_owd = budget['one_way']
        remaining = budget_owd - measured_owd_ms
        utilization = (measured_owd_ms / budget_owd) * 100

        return {
            'application': application,
            'budget_owd_ms': budget_owd,
            'measured_owd_ms': measured_owd_ms,
            'remaining_budget_ms': remaining,
            'budget_utilization_percent': utilization,
            'status': 'OK' if remaining > 0 else 'EXCEEDED'
        }

# 실무 사용 예시
if __name__ == "__main__":
    # 1. 지연 구성 요소 분석
    analyzer = DelayAnalyzer()

    print("=" * 60)
    print("지연 구성 요소 분석")
    print("=" * 60)

    # 서울-뉴욕 (11,000 km)
    delay_seoul_ny = analyzer.calculate_total_delay(
        distance_km=11000,
        packet_size_bytes=1500,
        link_speed_bps=10_000_000_000,  # 10 Gbps
        num_hops=15,
        processing_delay_per_hop_ms=0.05,
        queueing_factor=1.5
    )

    print("\n서울-뉴욕 (11,000 km, 10 Gbps):")
    for key, value in delay_seoul_ny.items():
        print(f"  {key}: {value:.3f} ms")

    # 2. 전파 지연 비교
    print("\n" + "=" * 60)
    print("전파 지연 비교 (10,000 km)")
    print("=" * 60)

    for medium in ['fiber', 'wireless', 'vacuum']:
        delay = analyzer.calculate_propagation_delay(10000, medium)
        print(f"  {medium:10s}: {delay:.2f} ms")

    # 3. 전송 지연 비교
    print("\n" + "=" * 60)
    print("전송 지연 비교 (1500 byte 패킷)")
    print("=" * 60)

    for speed_name, speed in [('1 Mbps', 1e6), ('100 Mbps', 1e8),
                               ('1 Gbps', 1e9), ('10 Gbps', 1e10)]:
        delay = analyzer.calculate_transmission_delay(1500, speed)
        print(f"  {speed_name:10s}: {delay:.4f} ms")

    # 4. 지연 예산 분석
    budget_analyzer = DelayBudgetAnalyzer()

    print("\n" + "=" * 60)
    print("지연 예산 분석 (측정된 OWD: 45ms)")
    print("=" * 60)

    for app in ['voip', 'online_gaming', 'cloud_gaming', 'autonomous_driving']:
        analysis = budget_analyzer.analyze_delay_budget(app, 45)
        status = analysis.get('status', 'N/A')
        remaining = analysis.get('remaining_budget_ms', 0)
        print(f"  {app:20s}: {status:10s} (잔여: {remaining:.1f}ms)")
