+++
title = "017. 전송 지연 (Transmission Delay) - 패킷길이/대역폭"
description = "전송 지연의 개념, 패킷 크기와 대역폭에 따른 계산, MTU 영향 및 최적화 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["TransmissionDelay", "PacketSize", "MTU", "Bandwidth", "SerializationDelay", "MSS"]
categories = ["studynotes-3_network"]
+++

# 017. 전송 지연 (Transmission Delay) - 패킷길이/대역폭

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전송 지연은 패킷의 모든 비트를 링크에 밀어 넣는 데 걸리는 시간으로, 패킷 길이(L)를 전송 속도(R)로 나눈 값(L/R)이며, 직렬화 지연(Serialization Delay)이라고도 합니다.
> 2. **가치**: 전송 지연은 링크 대역폭에 반비례하여, 1Gbps 링크에서 1500바이트 패킷은 12μs, 10Gbps에서는 1.2μs가 소요됩니다. 저속 링크에서는 전송 지연이 전체 지연의 상당 부분을 차지합니다.
> 3. **융합**: 전송 지연 최적화를 위해 MTU 튜닝, 대역폭 증설, 패킷 크기 최적화, TSO(TCP Segmentation Offload) 등이 활용되며, 저속 IoT 링크에서는 작은 패킷 사용이 필수적입니다.

---

## I. 개요 (Context & Background)

**전송 지연(Transmission Delay)**은 송신측이 패킷의 **첫 번째 비트부터 마지막 비트까지**를 전송 매체에 밀어 넣는 데 걸리는 시간입니다. 이는 **직렬화 지연(Serialization Delay)**이라고도 불리며, 패킷을 비트 단위로 직렬화하여 전송하는 과정에서 발생합니다.

### 전송 지연 공식

```
전송 지연 (d_trans) = 패킷 길이 (L) / 전송 속도 (R)

L: 패킷 길이 (bits)
R: 링크 전송 속도 (bps)
```

### 전송 지연 vs 전파 지연

- **전송 지연**: 패킷을 링크에 **밀어 넣는** 시간 (패킷 길이/대역폭)
- **전파 지연**: 신호가 링크를 **따라 이동하는** 시간 (거리/전파 속도)

이 두 지연은 서로 **독립적**이며, 총 지연의 구성 요소입니다.

**💡 비유**: 전송 지연을 **'터널에 차량 진입'**에 비유할 수 있습니다.

- 10대의 차량(패킷 비트)이 터널(링크) 입구에 도착했습니다.
- 터널은 1초에 1대씩 진입할 수 있습니다.
- 모든 10대가 터널에 진입하는 데는 10초가 걸립니다. 이것이 **전송 지연**입니다.
- 차량이 터널을 통과하는 데 걸리는 시간은 **전파 지연**입니다.

**터널이 넓어서(대역폭 증가) 1초에 2대씩 진입할 수 있다면?**
- 10대 진입 시간: 5초 (전송 지연 50% 감소)

**차량이 20대로 늘어나면(패킷 크기 증가)?**
- 1초에 1대 진입 시: 20초 (전송 지연 2배)

**등장 배경 및 발전 과정**:

1. **초기 저속 통신**: 300 bps 모뎀 시대에는 1000비트 패킷을 전송하는 데 3.3초가 걸렸습니다. 전송 지연이 전체 지연의 대부분을 차지했습니다.

2. **고속 링크의 등장**: 10 Mbps 이더넷, 100 Mbps, 1 Gbps, 10 Gbps로 발전하면서 전송 지연은 μs 단위로 단축되었습니다.

3. **저속 IoT 링크의 부활**: LPWAN(LoRa, Sigfox), 저전력 Bluetooth 등에서는 수 kbps 대역폭으로 인해 전송 지연이 다시 중요한 이슈가 되었습니다.

4. **초고속 데이터센터**: 100 Gbps, 400 Gbps 링크에서는 전송 지연이 ns 단위로, 전파 지연이나 처리 지연이 더 중요해졌습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 상세 역할 | 단위 | 영향 관계 | 비고 |
|---------|------|----------|------|----------|------|
| **L** | 패킷 길이 | 패킷의 비트 수 | bits | 정비례 | L↑ → d↑ |
| **R** | 전송 속도 | 링크 대역폭 | bps | 반비례 | R↑ → d↓ |
| **d_trans** | 전송 지연 | L/R | s, ms, μs | - | 직렬화 시간 |
| **MTU** | 최대 전송 단위 | IP 패킷 최대 크기 | bytes | - | 1500B 표준 |
| **MSS** | 최대 세그먼트 크기 | TCP 페이로드 최대 | bytes | - | 1460B |

### 정교한 구조 다이어그램: 전송 지연 시각화

```ascii
================================================================================
[ 전송 지연의 개념 - 비트 직렬화 과정 ]
================================================================================

송신측                                        수신측
┌─────────┐                                  ┌─────────┐
│ 패킷    │                                  │         │
│┌───────┐│                                  │         │
││Bit 1  ││ ──────── R bps ────────────────> │ 수신    │
││Bit 2  ││         전송 속도                │ 버퍼    │
││Bit 3  ││                                  │         │
││  ...  ││   ┌──────────────────────────┐   │         │
││Bit N  ││   │   전송 매체 (Link)       │   │         │
│└───────┘│   │                          │   │         │
└─────────┘   └──────────────────────────┘   └─────────┘

시간 t=0:    Bit 1이 링크 진입 시작
시간 t=L/R:  Bit N이 링크 진입 완료 (전송 지연)

전송 지연 = L / R
- L = N bits (패킷 크기)
- R = 전송 속도 (bps)


================================================================================
[ 다양한 링크 속도에서의 전송 지연 비교 ]
================================================================================

패킷 크기: 1500 bytes = 12,000 bits

링크 속도        전송 지연        비고
────────────────────────────────────────────────
56 Kbps          214.3 ms        다이얼업 모뎀
1.544 Mbps        7.77 ms        T1 회선
10 Mbps           1.20 ms        이더넷
100 Mbps          0.12 ms        Fast Ethernet
1 Gbps            12 μs          Gigabit Ethernet
10 Gbps           1.2 μs         10GbE
100 Gbps          0.12 μs        100GbE
400 Gbps          0.03 μs        400GbE

※ 56 Kbps에서 400 Gbps까지: 전송 지연 7,143,000배 단축!


================================================================================
[ 패킷 크기별 전송 지연 (1 Gbps 링크) ]
================================================================================

패킷 크기         전송 지연        용도
────────────────────────────────────────────────
64 bytes         0.512 μs        이더넷 최소 프레임
576 bytes        4.608 μs        TCP MSS 최소
1280 bytes       10.24 μs        IPv6 최소 MTU
1500 bytes       12.00 μs        이더넷 표준 MTU
9000 bytes       72.00 μs        Jumbo Frame
65535 bytes     524.28 μs        IPv6 점보그램

※ 64B → 65535B: 전송 지연 1,024배 증가


================================================================================
[ 전송 지연 vs 전파 지연 비교 ]
================================================================================

시나리오: 1500 byte 패킷, 1000 km 거리

링크 속도    전송 지연    전파 지연(광섬유)    총 지연
────────────────────────────────────────────────────
1 Mbps       12 ms       5 ms                17 ms
10 Mbps      1.2 ms      5 ms                6.2 ms
100 Mbps     0.12 ms     5 ms                5.12 ms
1 Gbps       0.012 ms    5 ms                5.012 ms
10 Gbps      0.0012 ms   5 ms                5.0012 ms

※ 고속 링크에서는 전파 지연이 지배적
   저속 링크에서는 전송 지연이 지배적

전송 지연 = 전파 지연이 되는 임계 대역폭:
R_critical = L / d_prop = 12,000 bits / 5 ms = 2.4 Mbps
→ 2.4 Mbps 이하에서는 전송 지연이 더 큼


================================================================================
[ MTU와 전송 지연의 관계 ]
================================================================================

대용량 파일 전송 (1 MB = 8,388,608 bits)

MTU        패킷 수      패킷당 전송지연    총 전송 지연 (1 Gbps)
───────────────────────────────────────────────────────────
576 B      1,747 패킷    4.6 μs           8.04 ms
1500 B       683 패킷    12 μs            8.20 ms
9000 B       114 패킷    72 μs            8.21 ms

※ 총 전송 지연은 패킷 크기와 무관하게 동일!
   (L_total / R = 8,388,608 / 10^9 = 8.39 ms)

하지만 패킷 수 감소 → 처리 지연 감소, 오버헤드 감소


================================================================================
[ 직렬화 지연 (Serialization Delay) 상세 ]
================================================================================

송신 NIC 내부 동작:

┌──────────────────────────────────────────────────────────────┐
│                        송신 NIC                               │
│                                                              │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐             │
│  │ 송신     │────>│ 직렬화   │────>│ PHY      │────> 링크   │
│  │ 버퍼     │     │ (SerDes) │     │ (물리층) │             │
│  │ (병렬)   │     │ (병렬→직렬)│     │          │             │
│  └──────────┘     └──────────┘     └──────────┘             │
│       │                │                │                    │
│       │                │                │                    │
│   64/128비트     클럭 기반          아날로그                │
│   병렬 데이터    비트 직렬화        신호 변환               │
│                                                              │
└──────────────────────────────────────────────────────────────┘

직렬화 과정:
1. 버퍼에서 64/128비트 읽기 (병렬)
2. 클럭에 맞춰 1비트씩 출력
3. L 비트를 출력하는 데 L/R 시간 소요
```

### 심층 동작 원리: 전송 지연 최적화

1. **대역폭 증설**:
   - 전송 지연과 대역폭은 반비례 관계
   - 10배 대역폭 증설 → 전송 지연 1/10

2. **MTU 증가**:
   - 큰 패킷은 패킷 수를 줄여 처리 오버헤드 감소
   - Jumbo Frame (9000B)은 1500B 대비 6배 크기

3. **TSO (TCP Segmentation Offload)**:
   - CPU가 아닌 NIC가 큰 버퍼를 MTU 크기로 분할
   - CPU 부하 감소, 전송 효율 향상

4. **LRO (Large Receive Offload)**:
   - 수신측 NIC가 작은 패킷을 큰 버퍼로 결합
   - 상위 계층 처리 횟수 감소

### 핵심 수식

```
전송 지연:
d_trans = L / R

패킷 전송 시간:
t = t_0 + d_trans
- t_0: 첫 비트 전송 시작 시각
- t: 마지막 비트 전송 완료 시각

임계 대역폭 (전송 지연 = 전파 지연):
R_critical = L / d_prop

저속 링크에서의 총 지연:
d_total ≈ d_trans (d_trans >> d_prop)

고속 링크에서의 총 지연:
d_total ≈ d_prop (d_trans << d_prop)
```

### 핵심 코드: 전송 지연 분석기

```python
from dataclasses import dataclass
from typing import List, Tuple
import matplotlib.pyplot as plt

@dataclass
class LinkSpeed:
    """링크 속도 정의"""
    name: str
    speed_bps: int

# 표준 링크 속도
LINK_SPEEDS = [
    LinkSpeed("56K Modem", 56_000),
    LinkSpeed("ISDN (128K)", 128_000),
    LinkSpeed("T1", 1_544_000),
    LinkSpeed("E1", 2_048_000),
    LinkSpeed("10 Mbps Ethernet", 10_000_000),
    LinkSpeed("100 Mbps Ethernet", 100_000_000),
    LinkSpeed("1 Gbps Ethernet", 1_000_000_000),
    LinkSpeed("10 Gbps Ethernet", 10_000_000_000),
    LinkSpeed("100 Gbps Ethernet", 100_000_000_000),
    LinkSpeed("400 Gbps Ethernet", 400_000_000_000),
]

@dataclass
class PacketSize:
    """패킷 크기 정의"""
    name: str
    size_bytes: int

# 표준 패킷 크기
PACKET_SIZES = [
    PacketSize("Minimum (64B)", 64),
    PacketSize("TCP ACK (64B)", 64),
    PacketSize("TCP MSS Min (536B)", 536),
    PacketSize("TCP MSS (1460B)", 1460),
    PacketSize("MTU (1500B)", 1500),
    PacketSize("IPv6 MTU (1280B)", 1280),
    PacketSize("Jumbo (9000B)", 9000),
]

class TransmissionDelayCalculator:
    """
    전송 지연 계산기
    """

    @staticmethod
    def calculate(packet_size_bytes: int, link_speed_bps: int) -> float:
        """
        전송 지연 계산

        Args:
            packet_size_bytes: 패킷 크기 (bytes)
            link_speed_bps: 링크 속도 (bps)

        Returns:
            전송 지연 (seconds)
        """
        packet_bits = packet_size_bytes * 8
        return packet_bits / link_speed_bps

    @staticmethod
    def calculate_ms(packet_size_bytes: int, link_speed_bps: int) -> float:
        """전송 지연 (ms)"""
        return TransmissionDelayCalculator.calculate(packet_size_bytes, link_speed_bps) * 1000

    @staticmethod
    def calculate_us(packet_size_bytes: int, link_speed_bps: int) -> float:
        """전송 지연 (μs)"""
        return TransmissionDelayCalculator.calculate(packet_size_bytes, link_speed_bps) * 1_000_000

    @staticmethod
    def critical_bandwidth(packet_size_bytes: int, propagation_delay_ms: float) -> int:
        """
        임계 대역폭 계산
        전송 지연 = 전파 지연이 되는 대역폭
        """
        packet_bits = packet_size_bytes * 8
        propagation_s = propagation_delay_ms / 1000
        return int(packet_bits / propagation_s)

class MTUAnalyzer:
    """
    MTU 분석기
    """

    @staticmethod
    def analyze_file_transfer(file_size_bytes: int,
                             mtu_bytes: int,
                             link_speed_bps: int) -> dict:
        """
        파일 전송 분석

        Args:
            file_size_bytes: 파일 크기 (bytes)
            mtu_bytes: MTU (bytes)
            link_speed_bps: 링크 속도 (bps)

        Returns:
            분석 결과 딕셔너리
        """
        import math

        # 필요한 패킷 수 (IP/TCP 헤더 고려)
        mss = mtu_bytes - 40  # IP 20B + TCP 20B
        packet_count = math.ceil(file_size_bytes / mss)

        # 총 전송 데이터 (헤더 포함)
        total_bytes = packet_count * mtu_bytes
        overhead_bytes = total_bytes - file_size_bytes

        # 전송 지연
        total_bits = total_bytes * 8
        transmission_time_s = total_bits / link_speed_bps

        return {
            'file_size_bytes': file_size_bytes,
            'mtu_bytes': mtu_bytes,
            'mss_bytes': mss,
            'packet_count': packet_count,
            'total_transmitted_bytes': total_bytes,
            'overhead_bytes': overhead_bytes,
            'overhead_percent': (overhead_bytes / file_size_bytes) * 100,
            'transmission_time_ms': transmission_time_s * 1000,
        }

    @staticmethod
    def compare_mtus(file_size_bytes: int,
                    link_speed_bps: int) -> List[dict]:
        """다양한 MTU 비교"""
        results = []
        for mtu in [576, 1500, 9000]:
            result = MTUAnalyzer.analyze_file_transfer(
                file_size_bytes, mtu, link_speed_bps)
            results.append(result)
        return results

class SerializationAnalyzer:
    """
    직렬화 지연 분석기
    """

    @staticmethod
    def analyze_slow_link():
        """저속 링크 분석 (IoT, LPWAN)"""
        # IoT 장비 전형적 시나리오
        iot_scenarios = [
            ("LoRa (1 kbps)", 1_000),
            ("SigFox (100 bps)", 100),
            ("NB-IoT (250 kbps)", 250_000),
            ("BLE (1 Mbps)", 1_000_000),
            ("ZigBee (250 kbps)", 250_000),
        ]

        packet_sizes = [20, 50, 100, 200]  # bytes

        results = []
        for name, speed in iot_scenarios:
            for size in packet_sizes:
                delay_ms = TransmissionDelayCalculator.calculate_ms(size, speed)
                results.append({
                    'technology': name,
                    'speed_bps': speed,
                    'packet_size_bytes': size,
                    'transmission_delay_ms': delay_ms
                })

        return results

# 실무 사용 예시
if __name__ == "__main__":
    calc = TransmissionDelayCalculator()

    # 1. 다양한 링크 속도에서의 전송 지연
    print("=" * 70)
    print("전송 지연 분석 (1500 byte 패킷)")
    print("=" * 70)

    for link in LINK_SPEEDS:
        delay = calc.calculate_ms(1500, link.speed_bps)
        print(f"{link.name:25s}: {delay:12.4f} ms")

    # 2. 패킷 크기별 전송 지연 (1 Gbps)
    print("\n" + "=" * 70)
    print("패킷 크기별 전송 지연 (1 Gbps)")
    print("=" * 70)

    for packet in PACKET_SIZES:
        delay_us = calc.calculate_us(packet.size_bytes, 1_000_000_000)
        print(f"{packet.name:25s}: {delay_us:8.3f} μs")

    # 3. MTU 비교 분석 (10 MB 파일)
    print("\n" + "=" * 70)
    print("MTU 비교 분석 (10 MB 파일, 1 Gbps)")
    print("=" * 70)

    mtu_results = MTUAnalyzer.compare_mtus(10_000_000, 1_000_000_000)
    for result in mtu_results:
        print(f"\nMTU {result['mtu_bytes']}B:")
        print(f"  패킷 수: {result['packet_count']:,}")
        print(f"  오버헤드: {result['overhead_bytes']:,} bytes ({result['overhead_percent']:.2f}%)")
        print(f"  전송 시간: {result['transmission_time_ms']:.2f} ms")

    # 4. IoT 저속 링크 분석
    print("\n" + "=" * 70)
    print("IoT 저속 링크 전송 지연 (100 byte 패킷)")
    print("=" * 70)

    iot_results = SerializationAnalyzer.analyze_slow_link()
    for result in iot_results:
        if result['packet_size_bytes'] == 100:
            print(f"{result['technology']:20s}: {result['transmission_delay_ms']:8.1f} ms")
