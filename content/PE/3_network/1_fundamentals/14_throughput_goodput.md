+++
title = "014. 처리량 및 굿풋 (Throughput vs Goodput)"
description = "네트워크 성능 지표인 처리량(Throughput)과 굿풋(Goodput)의 개념, 차이점, 측정 방법 및 최적화 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["Throughput", "Goodput", "BandwidthUtilization", "ProtocolOverhead", "NetworkPerformance", "TCPWindow"]
categories = ["studynotes-3_network"]
+++

# 014. 처리량 및 굿풋 (Throughput vs Goodput)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 처리량(Throughput)은 단위 시간당 성공적으로 전달된 데이터의 총량(프로토콜 오버헤드 포함)이며, 굿풋(Goodput)은 실제 응용 계층에서 사용 가능한 유용한 데이터 양(오버헤드 제외)입니다.
> 2. **가치**: 굿풋은 사용자가 체감하는 실제 데이터 전송 속도를 나타내며, 처리량 대비 굿풋 비율이 높을수록 프로토콜 효율성이 좋습니다. 이더넷에서 굿풋은 일반적으로 처리량의 90~95% 수준입니다.
> 3. **융합**: 처리량 최적화를 위해서는 TCP 윈도우 크기 조정, MTU 최적화, 프로토콜 오버헤드 감소, Jumbo Frame 사용 등이 복합적으로 적용되며, 네트워크 장비의 하드웨어 가속이 활용됩니다.

---

## I. 개요 (Context & Background)

네트워크 성능을 평가할 때 가장 기본이 되는 지표가 **처리량(Throughput)**과 **굿풋(Goodput)**입니다. 두 지표는 모두 "얼마나 많은 데이터가 전송되었는가"를 나타내지만, 측정 기준과 의미가 다릅니다.

### 처리량 (Throughput)

**처리량(Throughput)**은 단위 시간당 소스에서 목적지로 성공적으로 전달된 **모든 비트의 양**입니다. 여기에는 사용자 데이터뿐만 아니라 **프로토콜 오버헤드**(헤더, 트레일러, ACK 패킷 등)도 포함됩니다.

```
처리량 = (사용자 데이터 + 프로토콜 오버헤드) / 시간
단위: bps, Kbps, Mbps, Gbps
```

### 굿풋 (Goodput)

**굿풋(Goodput)**은 단위 시간당 응용 계층에 실제로 전달된 **유용한 데이터의 양**입니다. 프로토콜 오버헤드와 재전송된 데이터는 제외됩니다.

```
굿풋 = 순수 응용 데이터 / 시간
단위: bps, Kbps, Mbps, Gbps

굿풋 = 처리량 - (프로토콜 오버헤드 + 재전송 데이터)
```

### 처리량 vs 대역폭

- **대역폭(Bandwidth)**: 채널의 **이론적 최대** 전송 용량
- **처리량(Throughput)**: **실제 측정된** 전송 속도

```
대역폭 활용률 = 처리량 / 대역폭 × 100%
```

**💡 비유**: 처리량과 굿풋을 **'택배 배송'**에 비유할 수 있습니다.

- **처리량(Throughput)**은 **택배 트럭이 운반한 총 무게**입니다. 여기에는 상품뿐만 아니라 박스, 송장, 완충재, 택배 기사의 체중까지 모두 포함됩니다.

- **굿풋(Goodput)**은 **고객이 실제로 받은 상품의 무게**입니다. 박스, 송장, 완충재는 제외하고 순수 상품만 계산합니다.

- 만약 트럭이 1000kg을 운반했는데, 그중 상품이 800kg이고 박스/완충재가 200kg이라면, 처리량은 1000kg, 굿풋은 800kg입니다. 효율은 80%입니다.

**등장 배경 및 발전 과정**:

1. **초기 네트워크 성능 측정**: 1970년대 ARPANET에서는 단순히 "얼마나 많은 데이터가 전송되었나"만 측정했습니다.

2. **프로토콜 오버헤드 인식**: TCP/IP가 보편화되면서 헤더 오버헤드(IP 20바이트 + TCP 20바이트)가 대역폭의 상당 부분을 차지한다는 점이 인식되었습니다.

3. **굿풋 개념의 등장**: 사용자 체감 성능을 정확히 측정하기 위해 "실제 유용한 데이터"만을 계산하는 굿풋 개념이 도입되었습니다.

4. **현대적 최적화**: 오늘날 Zero-Copy, RDMA, TOE(TCP Offload Engine) 등의 기술로 오버헤드를 최소화하여 처리량과 굿풋의 격차를 줄이는 연구가 진행되고 있습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 상세 역할 | 단위 | 포함 여부 | 비고 |
|---------|------|----------|------|----------|------|
| **Raw Rate** | 원시 속도 | 물리 계층 전송 속도 | bps | - | 이더넷 1Gbps |
| **Protocol OH** | 프로토콜 오버헤드 | 헤더, 트레일러 | bps | Throughput O / Goodput X | IP+TCP=40B |
| **Retransmission** | 재전송 | 중복 전송 데이터 | bps | Throughput O / Goodput X | 손실 복구 |
| **ACK Traffic** | 응답 트래픽 | 확인 응답 패킷 | bps | Throughput O / Goodput X | TCP ACK |
| **Throughput** | 처리량 | 총 전송 데이터 | bps | - | 오버헤드 포함 |
| **Goodput** | 굿풋 | 유용한 데이터 | bps | - | 오버헤드 제외 |
| **Efficiency** | 효율 | 굿풋/처리량 | % | - | 90%+ 목표 |

### 정교한 구조 다이어그램: 처리량 vs 굿풋 계층

```ascii
================================================================================
[ 처리량과 굿풋의 관계 - 프로토콜 스택 관점 ]
================================================================================

송신측                                    수신측
┌─────────────────────┐                  ┌─────────────────────┐
│   응용 계층         │                  │   응용 계층         │
│  ┌───────────────┐  │                  │  ┌───────────────┐  │
│  │ 사용자 데이터 │──┼──────────────────┼─>│ 사용자 데이터 │  │ ← GOODPUT
│  │  (1000 bytes) │  │                  │  │  (1000 bytes) │  │
│  └───────────────┘  │                  │  └───────────────┘  │
└─────────────────────┘                  └─────────────────────┘
          ↓ HTTP 헤더 (+200 bytes)               ↑
┌─────────────────────┐                  ┌─────────────────────┐
│   표현/세션 계층     │                  │   표현/세션 계층     │
│  데이터: 1200 bytes  │                  │  데이터: 1200 bytes  │
└─────────────────────┘                  └─────────────────────┘
          ↓ TCP 헤더 (+20 bytes)                ↑
┌─────────────────────┐                  ┌─────────────────────┐
│   전송 계층 (TCP)    │                  │   전송 계층 (TCP)    │
│  세그먼트: 1220 bytes│                  │  세그먼트: 1220 bytes│
└─────────────────────┘                  └─────────────────────┘
          ↓ IP 헤더 (+20 bytes)                 ↑
┌─────────────────────┐                  ┌─────────────────────┐
│   네트워크 계층 (IP) │                  │   네트워크 계층 (IP) │
│  패킷: 1240 bytes   │                  │  패킷: 1240 bytes   │
└─────────────────────┘                  └─────────────────────┘
          ↓ 이더넷 프레임 (+38 bytes)           ↑
┌─────────────────────┐                  ┌─────────────────────┐
│   데이터 링크 계층   │                  │   데이터 링크 계층   │
│  프레임: 1278 bytes │ ────────────────> │  프레임: 1278 bytes │ ← THROUGHPUT
└─────────────────────┘                  └─────────────────────┘
          ↓ 물리 계층 인코딩                    ↑
┌─────────────────────┐                  ┌─────────────────────┐
│   물리 계층         │                  │   물리 계층         │
│  비트 스트림        │ ────────────────> │  비트 스트림        │
└─────────────────────┘                  └─────────────────────┘

                    ┌────────────────────────────────┐
                    │  Goodput: 1000 bytes           │
                    │  Throughput: 1278 bytes        │
                    │  Efficiency: 78.2%             │
                    │  Overhead: 278 bytes (21.8%)   │
                    └────────────────────────────────┘


================================================================================
[ 이더넷 프레임 오버헤드 상세 분석 ]
================================================================================

┌───────────────────────────────────────────────────────────────────────┐
│                        이더넷 프레임 구조                              │
├───────────┬───────────┬────────────────────────────────────┬──────────┤
│ Preamble  │  Header   │           Payload                  │  Trailer │
│  (8B)     │  (14B)    │         (46~1500B)                 │  (4B+FCS)│
├───────────┼───────────┼────────────────────────────────────┼──────────┤
│ 7B Pre    │ 6B DA     │         사용자 데이터              │  4B CRC  │
│ + 1B SFD  │ 6B SA     │         + 상위 계층 헤더           │          │
│           │ 2B Type   │                                    │          │
└───────────┴───────────┴────────────────────────────────────┴──────────┘
       ↓
+ Inter-Frame Gap (12B)

최대 페이로드: 1500 bytes (MTU)
전체 프레임: 8 + 14 + 1500 + 4 + 12 = 1538 bytes

이더넷 효율 = 1500 / 1538 = 97.5%

Jumbo Frame (9000B MTU):
전체 프레임: 8 + 14 + 9000 + 4 + 12 = 9038 bytes
효율 = 9000 / 9038 = 99.6%


================================================================================
[ TCP/IP 오버헤드 상세 분석 ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────┐
│                         TCP/IP 패킷 구조                                 │
├─────────────────┬───────────────────┬───────────────────────────────────┤
│   IP Header     │    TCP Header     │           TCP Payload              │
│    (20 B)       │     (20 B)        │         (variable)                 │
├─────────────────┼───────────────────┼───────────────────────────────────┤
│ Version: 4bits  │ Src Port: 16bits  │                                   │
│ IHL: 4bits      │ Dst Port: 16bits  │                                   │
│ ToS: 8bits      │ Seq Num: 32bits   │         응용 데이터                │
│ Total Len: 16b  │ Ack Num: 32bits   │                                   │
│ ID: 16bits      │ Offset: 4bits     │         (MSS: 1460B max)          │
│ Flags: 16bits   │ Flags: 12bits     │                                   │
│ TTL: 8bits      │ Window: 16bits    │                                   │
│ Protocol: 8b    │ Checksum: 16bits  │                                   │
│ Checksum: 16b   │ Urgent: 16bits    │                                   │
│ Src IP: 32bits  │ Options: (가변)   │                                   │
│ Dst IP: 32bits  │                   │                                   │
└─────────────────┴───────────────────┴───────────────────────────────────┘

TCP/IP 오버헤드: 20 + 20 = 40 bytes (최소)
MSS (Maximum Segment Size): 1460 bytes (1500 MTU - 40B header)

TCP/IP 효율 = 1460 / 1500 = 97.3%


================================================================================
[ 종합 효율 계산 예시 ]
================================================================================

시나리오: HTTP 파일 다운로드 (1500 byte 이더넷 프레임)

1. 이더넷 프레임 효율: 1500 / 1538 = 97.5%
2. TCP/IP 효율: 1460 / 1500 = 97.3%
3. HTTP 헤더 효율 (평균 200B 가정): 1260 / 1460 = 86.3%

종합 효율 = 97.5% × 97.3% × 86.3% = 81.9%

100 Mbps 링크에서:
- 이론적 최대 Throughput: 100 Mbps
- 실제 Throughput: ~97.5 Mbps (이더넷 효율)
- Goodput: ~81.9 Mbps (종합 효율)
```

### 심층 동작 원리: 처리량 영향 요인

1. **프로토콜 오버헤드**:
   - 이더넷: Preamble(8B) + Header(14B) + FCS(4B) + IFG(12B) = 38 bytes
   - IP: 20 bytes (옵션 없음)
   - TCP: 20 bytes (옵션 없음)
   - 총 오버헤드: 38 + 40 = 78 bytes per packet

2. **재전송 오버헤드**:
   - 패킷 손실 시 TCP 재전송 발생
   - 손실률 p에 따른 처리량 감소: T ≈ T_max × (1 - √p)

3. **ACK 트래픽**:
   - TCP ACK 패킷: 40 bytes (IP + TCP 헤더)
   - 지연된 ACK로 2패킷당 1 ACK로 감소 가능

4. **윈도우 크기 제한**:
   - TCP 윈도우가 대역폭×지연시간(BDP)보다 작으면 처리량 제한
   - 필요 윈도우 = 대역폭 × RTT

### 핵심 수식: TCP 처리량 근사

```
1. 이상적 TCP 처리량:
   Throughput = Window Size / RTT

2. 패킷 손실 고려 (Mathis 공식):
   Throughput ≈ (MSS / RTT) × (C / √p)

   여기서:
   - MSS: Maximum Segment Size
   - RTT: Round Trip Time
   - C: 상수 (약 1.22)
   - p: 패킷 손실률

3. 대역폭-지연 곱 (Bandwidth-Delay Product, BDP):
   BDP = Bandwidth × RTT

   예) 1 Gbps 링크, RTT 10ms:
   BDP = 10⁹ × 0.01 = 10⁷ bits = 1.25 MB

   필요 윈도우 크기: 최소 1.25 MB
```

### 핵심 코드: 처리량/굿풋 분석기

```python
from dataclasses import dataclass
from typing import List, Tuple
import time

@dataclass
class ProtocolOverhead:
    """프로토콜 오버헤드 정의"""
    name: str
    header_bytes: int
    trailer_bytes: int = 0

# 표준 프로토콜 오버헤드
ETHERNET_OVERHEAD = ProtocolOverhead("Ethernet", 14, 4)  # Header + FCS
IP_OVERHEAD = ProtocolOverhead("IPv4", 20, 0)
TCP_OVERHEAD = ProtocolOverhead("TCP", 20, 0)
UDP_OVERHEAD = ProtocolOverhead("UDP", 8, 0)

# 물리 계층 오버헤드
PREAMBLE_SFD = 8  # bytes
INTER_FRAME_GAP = 12  # bytes

class ThroughputAnalyzer:
    """
    처리량 및 굿풋 분석기
    """
    def __init__(self, mtu: int = 1500):
        self.mtu = mtu
        self.preamble_sfd = PREAMBLE_SFD
        self.ifg = INTER_FRAME_GAP

    def calculate_ethernet_efficiency(self, payload_size: int) -> float:
        """이더넷 프레임 효율 계산"""
        # 이더넷 프레임 크기
        frame_size = (self.preamble_sfd +
                     ETHERNET_OVERHEAD.header_bytes +
                     payload_size +
                     ETHERNET_OVERHEAD.trailer_bytes +
                     self.ifg)

        return payload_size / frame_size

    def calculate_tcp_ip_efficiency(self, payload_size: int) -> float:
        """TCP/IP 효율 계산"""
        total_size = (IP_OVERHEAD.header_bytes +
                     TCP_OVERHEAD.header_bytes +
                     payload_size)
        return payload_size / total_size

    def calculate_total_efficiency(self, app_data_size: int,
                                   protocol_overhead: int = 0) -> float:
        """종합 전송 효율 계산"""
        # TCP 페이로드
        tcp_payload = app_data_size + protocol_overhead

        # IP 패킷 크기
        ip_packet_size = IP_OVERHEAD.header_bytes + TCP_OVERHEAD.header_bytes + tcp_payload

        # 이더넷 프레임 효율
        eth_efficiency = self.calculate_ethernet_efficiency(ip_packet_size)

        # TCP/IP 효율
        tcp_ip_efficiency = self.calculate_tcp_ip_efficiency(tcp_payload)

        # 종합 효율
        return eth_efficiency * tcp_ip_efficiency * (app_data_size / tcp_payload)

    def calculate_goodput(self, raw_bandwidth: float,
                          app_data_size: int,
                          protocol_overhead: int = 0) -> float:
        """
        굿풋 계산

        Args:
            raw_bandwidth: 원시 대역폭 (bps)
            app_data_size: 응용 데이터 크기 (bytes)
            protocol_overhead: 응용 계층 프로토콜 오버헤드 (bytes)
        """
        efficiency = self.calculate_total_efficiency(app_data_size, protocol_overhead)
        return raw_bandwidth * efficiency

class TCPThroughputModel:
    """
    TCP 처리량 모델
    """
    def __init__(self, mss: int = 1460, rtt: float = 0.01):
        self.mss = mss  # Maximum Segment Size (bytes)
        self.rtt = rtt  # Round Trip Time (seconds)

    def ideal_throughput(self, window_size: int) -> float:
        """이상적 TCP 처리량 (윈도우 크기 제한)"""
        # 윈도우 크기는 bytes 단위
        throughput_bps = (window_size * 8) / self.rtt
        return throughput_bps

    def loss_limited_throughput(self, loss_rate: float) -> float:
        """패킷 손실 제한 처리량 (Mathis 공식)"""
        if loss_rate <= 0:
            return float('inf')

        # Mathis 공식: T ≈ (MSS / RTT) × (C / √p)
        # C ≈ 1.22 for TCP Reno
        C = 1.22
        throughput_bps = (self.mss * 8 / self.rtt) * (C / (loss_rate ** 0.5))
        return throughput_bps

    def bandwidth_delay_product(self, bandwidth: float) -> int:
        """
        대역폭-지연 곱 계산
        필요한 최소 윈도우 크기 반환
        """
        # BDP = Bandwidth × RTT (bits)
        bdp_bits = bandwidth * self.rtt
        bdp_bytes = bdp_bits / 8
        return int(bdp_bytes)

    def optimal_window_size(self, bandwidth: float) -> int:
        """최적 윈도우 크기 계산"""
        bdp = self.bandwidth_delay_product(bandwidth)
        # BDP의 1.5~2배를 버퍼로 권장
        return int(bdp * 1.5)

class NetworkPerformanceMonitor:
    """
    네트워크 성능 모니터링
    """
    def __init__(self):
        self.measurements: List[dict] = []

    def measure_throughput(self, data_transferred: int,
                          duration: float,
                          include_overhead: bool = True) -> float:
        """
        처리량 측정

        Args:
            data_transferred: 전송된 데이터 (bytes)
            duration: 소요 시간 (seconds)
            include_overhead: 오버헤드 포함 여부
        """
        throughput_bps = (data_transferred * 8) / duration
        return throughput_bps

    def calculate_goodput_ratio(self, goodput: float,
                                throughput: float) -> float:
        """굿풋 비율 계산"""
        if throughput == 0:
            return 0.0
        return goodput / throughput

    def analyze_session(self, total_bytes: int,
                        useful_bytes: int,
                        retransmitted_bytes: int,
                        duration: float) -> dict:
        """
        세션 성능 분석
        """
        throughput = self.measure_throughput(total_bytes, duration)
        goodput = self.measure_throughput(useful_bytes, duration)
        retransmit_overhead = self.measure_throughput(retransmitted_bytes, duration)

        return {
            'throughput_mbps': throughput / 1e6,
            'goodput_mbps': goodput / 1e6,
            'goodput_ratio': self.calculate_goodput_ratio(goodput, throughput),
            'retransmit_overhead_mbps': retransmit_overhead / 1e6,
            'efficiency_loss_percent': (1 - goodput / throughput) * 100
        }

# 실무 사용 예시
if __name__ == "__main__":
    # 1. 이더넷 효율 분석
    analyzer = ThroughputAnalyzer(mtu=1500)

    print("=" * 60)
    print("이더넷 전송 효율 분석")
    print("=" * 60)

    # 1500바이트 페이로드 (최대)
    eff_1500 = analyzer.calculate_ethernet_efficiency(1500)
    print(f"1500B 페이로드 효율: {eff_1500*100:.2f}%")

    # 64바이트 페이로드 (최소)
    eff_64 = analyzer.calculate_ethernet_efficiency(64)
    print(f"64B 페이로드 효율: {eff_64*100:.2f}%")

    # Jumbo Frame
    analyzer_jumbo = ThroughputAnalyzer(mtu=9000)
    eff_jumbo = analyzer_jumbo.calculate_ethernet_efficiency(9000)
    print(f"9000B (Jumbo) 효율: {eff_jumbo*100:.2f}%")

    # 2. TCP 처리량 분석
    tcp_model = TCPThroughputModel(mss=1460, rtt=0.01)  # 10ms RTT

    print("\n" + "=" * 60)
    print("TCP 처리량 분석 (RTT = 10ms)")
    print("=" * 60)

    # 윈도우 크기별 처리량
    for window_kb in [16, 64, 256, 1024]:
        window_bytes = window_kb * 1024
        throughput = tcp_model.ideal_throughput(window_bytes)
        print(f"윈도우 {window_kb:5d} KB: {throughput/1e6:8.2f} Mbps")

    # 대역폭-지연 곱
    print("\n" + "=" * 60)
    print("대역폭-지연 곱 (BDP) 분석")
    print("=" * 60)

    for bandwidth_mbps in [100, 1000, 10000]:
        bdp = tcp_model.bandwidth_delay_product(bandwidth_mbps * 1e6)
        optimal_window = tcp_model.optimal_window_size(bandwidth_mbps * 1e6)
        print(f"대역폭 {bandwidth_mbps:5d} Mbps: BDP = {bdp/1024:8.1f} KB, "
              f"권장 윈도우 = {optimal_window/1024:8.1f} KB")

    # 3. 종합 성능 분석
    print("\n" + "=" * 60)
    print("세션 성능 분석 예시")
    print("=" * 60)

    monitor = NetworkPerformanceMonitor()
    session_analysis = monitor.analyze_session(
        total_bytes=100_000_000,      # 100 MB 전송
        useful_bytes=82_000_000,      # 82 MB 유용 데이터
        retransmitted_bytes=5_000_000, # 5 MB 재전송
        duration=10.0                  # 10초
    )

    print(f"처리량: {session_analysis['throughput_mbps']:.2f} Mbps")
    print(f"굿풋: {session_analysis['goodput_mbps']:.2f} Mbps")
    print(f"굿풋 비율: {session_analysis['goodput_ratio']*100:.1f}%")
    print(f"재전송 오버헤드: {session_analysis['retransmit_overhead_mbps']:.2f} Mbps")
    print(f"효율 손실: {session_analysis['efficiency_loss_percent']:.1f}%")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: MTU별 전송 효율

| MTU | 이더넷 효율 | TCP/IP 효율 | 종합 효율 | 1Gbps에서 굿풋 |
|-----|-----------|------------|----------|---------------|
| **64B** | 52.4% | 13.3% | 7.0% | 70 Mbps |
| **576B** | 91.4% | 88.9% | 81.2% | 812 Mbps |
| **1500B** | 97.5% | 97.3% | 94.9% | 949 Mbps |
| **9000B** | 99.6% | 99.6% | 99.2% | 992 Mbps |

### 과목 융합 관점 분석

1. **운영체제와의 융합**:
   - **Zero-Copy**: `sendfile()` 시스템 콜로 커널 버퍼에서 직접 전송
   - **TCP 버퍼 튜닝**: `/proc/sys/net/ipv4/tcp_rmem`, `tcp_wmem`
   - **TSO (TCP Segmentation Offload)**: NIC가 TCP 세그먼트 분할 수행

2. **컴퓨터구조와의 융합**:
   - **DMA (Direct Memory Access)**: CPU 개입 없이 메모리-NIC 간 데이터 전송
   - **PCIe 대역폭**: x16 Gen4 = 32 GB/s, 네트워크 대역폭의 병목이 아님

3. **데이터베이스와의 융합**:
   - **배치 전송**: 작은 쿼리를 모아서 전송하여 오버헤드 분산
   - **압축 전송**: 네트워크 대역폭 절약, CPU 비용 증가

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 대용량 파일 전송 최적화

**문제 상황**: 데이터센터 간 10TB 파일 전송이 필요하며, 현재 1Gbps 링크에서 18시간이 소요됩니다. 전송 시간을 단축해야 합니다.

**기술사의 분석 및 해결 과정**:

1. **현재 상황 분석**:
   - 이론적 최소 시간: 10TB / 1Gbps = 10 × 8 × 10¹² / 10⁹ = 80,000초 ≈ 22시간
   - 실제 18시간: 효율 약 122% (압축 또는 중복 제거 사용 중)

2. **최적화 방안**:
   - **링크 업그레이드**: 1Gbps → 10Gbps (10배)
   - **Jumbo Frame**: MTU 1500 → 9000 (5% 효율 향상)
   - **TCP 튜닝**: 윈도우 크기 증가 (BDP 기반)
   - **병렬 스트림**: 4개 TCP 연결 동시 사용

3. **결과 예측**:
   - 10Gbps + Jumbo Frame + TCP 튜닝: 10TB / 9.5Gbps ≈ 2.3시간

### 도입 시 고려사항 체크리스트

| 항목 | 확인 내용 | 권장 설정 |
|------|----------|----------|
| **MTU** | 경로 상 최소 MTU | 1500B (안전), 9000B (Jumbo) |
| **TCP 윈도우** | BDP 대비 충분한 크기 | BDP × 2 |
| **버퍼 크기** | 송수신 버퍼 | 윈도우 크기 이상 |
| **동시 연결** | 병렬 처리 | 4~8개 |

---

## V. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 최적화 항목 | 효율 향상 | 굿풋 증가 |
|------------|----------|----------|
| **Jumbo Frame** | +5% | +5% |
| **TCP 튜닝** | +20% | +20% |
| **병렬 전송** | +300% | +300% |
| **압축** | - | +50~200% |

### 미래 전망

- **400G 이더넷**: 데이터센터 백본 대역폭 확장
- **RDMA**: 커널 우회로 오버헤드 제거
- **QUIC**: UDP 기반으로 TCP 오버헤드 감소

---

## 관련 개념 맵 (Knowledge Graph)
- [대역폭 효율성](./13_bandwidth_efficiency.md) - 스펙트럼 효율
- [TCP 혼잡 제어](../2_transport/tcp_congestion_control.md) - 처리량 제어
- [TCP 흐름 제어](../2_transport/tcp_flow_control_window.md) - 윈도우 크기
- [이더넷 프레임](../4_switching/ethernet_frame.md) - 프레임 구조
- [MTU와 단편화](../3_routing/mtu_fragmentation.md) - 패킷 크기

---

## 어린이를 위한 3줄 비유 설명
1. **처리량**은 **'트럭에 실린 모든 짐의 무게'**예요. 여기에는 물건뿐만 아니라 박스, 완충재, 송장도 모두 포함돼요.
2. **굿풋**은 **'실제 물건의 무게만'**이에요. 박스나 송장은 빼고, 진짜 받고 싶었던 물건만 따로 재는 거예요.
3. **효율이 좋다**는 건 **'박스가 얇고 가볍다'**는 뜻이에요. 같은 트럭에 더 많은 물건을 실을 수 있으니까요!
