+++
title = "013. 대역폭 및 대역폭-효율성 관계 (Bandwidth & Efficiency)"
description = "대역폭의 개념, 채널 용량과의 관계, 대역폭 효율성 지표 및 최적화 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["Bandwidth", "ChannelCapacity", "SpectralEfficiency", "ShannonLimit", "Throughput", "Goodput"]
categories = ["studynotes-3_network"]
+++

# 013. 대역폭 및 대역폭-효율성 관계 (Bandwidth & Efficiency)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 대역폭(Bandwidth)은 주파수 영역에서 신호가 차지하는 범위(Hz)이거나, 데이터 통신에서 단위 시간당 전송 가능한 데이터 양(bps)을 의미하며, 샤논-하틀리 정리에 의해 대역폭과 신호 대 잡음비(SNR)의 곱이 채널 용량을 결정합니다.
> 2. **가치**: 대역폭 효율성(Spectral Efficiency, bps/Hz)은 제한된 주파수 자원으로 얼마나 많은 데이터를 전송할 수 있는지를 나타내는 핵심 지표로, 5G에서는 30 bps/Hz 이상의 효율을 달성합니다.
> 3. **융합**: 대역폭 효율성 향상을 위해 변조 기술(QAM, OFDM), 코딩 기술(LDPC, 터보 코드), MIMO 안테나 기술이 복합적으로 적용되며, AI 기반 적응형 변조(Adaptive Modulation)로 최적화됩니다.

---

## I. 개요 (Context & Background)

**대역폭(Bandwidth)**은 원래 아날로그 신호 처리에서 **주파수 스펙트럼의 폭**, 즉 최고 주파수와 최저 주파수의 차이(Hz 단위)를 의미했습니다. 디지털 통신에서는 이 개념이 확장되어 **단위 시간당 전송할 수 있는 데이터 양**(bits per second, bps)을 의미하기도 합니다. 문맥에 따라 구분이 필요합니다.

### 대역폭의 두 가지 의미

1. **아날로그 대역폭 (Analog Bandwidth)**:
   - 단위: 헤르츠(Hz)
   - 정의: 신호가 차지하는 주파수 범위 (f_max - f_min)
   - 예: 음성 신호는 300Hz ~ 3400Hz, 대역폭 = 3100Hz

2. **디지털 대역폭 (Digital Bandwidth)**:
   - 단위: 비트/초(bps), 킬로비트/초(Kbps), 메가비트/초(Mbps), 기가비트/초(Gbps)
   - 정의: 단위 시간당 전송 가능한 비트 수
   - 예: 이더넷 1000BASE-T = 1 Gbps

### 대역폭 효율성 (Bandwidth Efficiency / Spectral Efficiency)

**대역폭 효율성**은 단위 대역폭당 전송할 수 있는 데이터 전송 속도로, **bps/Hz** 단위로 표현됩니다. 이는 주파수 자원을 얼마나 효율적으로 사용하는지를 나타내는 핵심 지표입니다.

```
대역폭 효율성 (η) = 데이터 전송 속도 (R) / 대역폭 (B)
단위: bps/Hz (또는 bit/s/Hz)
```

**💡 비유**: 대역폭과 대역폭 효율성을 **'도로'**에 비유할 수 있습니다.

- **대역폭**은 **도로의 차선 수**입니다. 4차선 도로는 2차선 도로보다 많은 차량이 동시에 통과할 수 있습니다.
- **데이터 전송 속도**는 **단위 시간당 통과하는 차량 수**입니다.
- **대역폭 효율성**은 **차선당 통과하는 차량 수**입니다. 4차선 도로에서 2차선 도로의 4배 차량이 통과하면 효율성이 같고, 5배가 통과하면 효율성이 더 높습니다.

**등장 배경 및 발전 과정**:

1. **주파수 자원의 희소성**: 무선 통신에서 사용할 수 있는 주파수 대역은 유한합니다. 더 많은 사용자와 서비스를 수용하기 위해 동일한 대역폭에서 더 많은 데이터를 전송하는 기술이 필요했습니다.

2. **샤논의 채널 용량 정리 (1948년)**: Claude Shannon이 수립한 정보 이론에 따르면, 채널 용량 C = B × log₂(1 + S/N)입니다. 이는 대역폭(B)과 신호 대 잡음비(S/N)의 상충 관계(Trade-off)를 보여줍니다.

3. **변조 기술의 발전**: BPSK(1 bit/symbol) → QPSK(2 bits/symbol) → 16-QAM(4 bits/symbol) → 1024-QAM(10 bits/symbol)으로 발전하며 대역폭 효율성이 지속적으로 향상되었습니다.

4. **현대적 기술**: OFDM, MIMO, LDPC 코드 등을 조합하여 5G에서는 30 bps/Hz 이상, Wi-Fi 6에서는 10 bps/Hz 이상의 효율을 달성합니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 상세 역할 | 단위 | 내부 동작 | 비유 |
|---------|------|----------|------|----------|------|
| **B** | 대역폭 (Bandwidth) | 주파수 범위 | Hz | 스펙트럼 폭 | 도로 차선 수 |
| **C** | 채널 용량 (Capacity) | 최대 전송 속도 | bps | 샤논 한계 | 최대 교통량 |
| **R** | 데이터 속도 (Data Rate) | 실제 전송 속도 | bps | 처리량 | 실제 통과 차량 |
| **S/N** | 신호 대 잡음비 | 신호 강도 비율 | dB | 신호 품질 | 도로 상태 |
| **η** | 스펙트럼 효율 | 대역폭당 속도 | bps/Hz | 전송 효율 | 차선당 차량 |
| **T** | 처리량 (Throughput) | 유효 데이터 속도 | bps | 실질 전송 | 유효 화물 |
| **G** | 굿풋 (Goodput) | 응용 데이터 속도 | bps | 순수 데이터 | 실제 짐 |

### 정교한 구조 다이어그램: 대역폭 계층 구조

```ascii
================================================================================
[ 대역폭 계층 구조: 물리 계층에서 응용 계층까지 ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                        응용 계층 (Application Layer)                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Goodput (굿풋): 실제 응용 데이터 속도                                │    │
│  │  예) HTTP 페이로드, 비디오 스트림 데이터                              │    │
│  │  Goodput = Throughput - (프로토콜 오버헤드 + 재전송)                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓ 오버헤드 감소
┌─────────────────────────────────────────────────────────────────────────────┐
│                        전송 계층 (Transport Layer)                           │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Throughput (처리량): 전송 계층에서의 유효 속도                        │    │
│  │  예) TCP 세그먼트 페이로드 속도                                       │    │
│  │  Throughput = Data Rate × (1 - Packet Loss) × Window Efficiency    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓ 오버헤드 감소
┌─────────────────────────────────────────────────────────────────────────────┐
│                        데이터 링크 계층 (Data Link Layer)                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Data Rate (데이터 속도): 프레임 단위 전송 속도                        │    │
│  │  예) 이더넷 프레임 페이로드 속도                                       │    │
│  │  Data Rate = Symbol Rate × Bits per Symbol × Coding Rate           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↓ 오버헤드 감소
┌─────────────────────────────────────────────────────────────────────────────┐
│                        물리 계층 (Physical Layer)                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Raw Bit Rate (원시 비트 속도): 물리적 전송 속도                       │    │
│  │  예) 1000BASE-T = 1 Gbps (물리적)                                    │    │
│  │  Raw Rate = Bandwidth × Spectral Efficiency                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Channel Capacity (채널 용량): 이론적 최대 속도                        │    │
│  │  Shannon: C = B × log₂(1 + S/N)                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘


================================================================================
[ 대역폭 효율성 비교: 다양한 기술의 스펙트럼 효율 ]
================================================================================

기술              대역폭        변조 방식         스펙트럼 효율
                 (MHz)                          (bps/Hz)
────────────────────────────────────────────────────────────────
GSM (2G)          0.2          GMSK              0.17
GPRS (2.5G)       0.2          GMSK              0.34
EDGE (2.75G)      0.2          8PSK              0.69
UMTS (3G)         5.0          QPSK              0.51
HSPA (3.5G)       5.0          16-QAM            3.0
LTE (4G)          20.0         64-QAM            15.0
LTE-A (4G+)       100.0        256-QAM           30.0
5G NR             100.0        256-QAM           35.0
Wi-Fi 4 (802.11n) 20.0         64-QAM            7.2
Wi-Fi 5 (802.11ac)160.0        256-QAM           10.8
Wi-Fi 6 (802.11ax)160.0        1024-QAM          12.5
Wi-Fi 7 (802.11be)320.0        4096-QAM          20.0

샤논 한계 (이론적): S/N = 20dB 기준 약 6.7 bps/Hz
                  S/N = 30dB 기준 약 10 bps/Hz


================================================================================
[ 처리량 vs 굿풋 예시: HTTP 파일 다운로드 ]
================================================================================

물리 계층 Raw Bit Rate:    100 Mbps (이더넷)
                          - 20% (이더넷 프레임 오버헤드)
데이터 링크 처리량:         80 Mbps
                          - 5% (IP 헤더)
네트워크 처리량:            76 Mbps
                          - 5% (TCP 헤더)
전송 계층 처리량:           72 Mbps
                          - 10% (TCP 재전송, ACK)
TCP 유효 처리량:           65 Mbps
                          - 15% (HTTP 헤더, 청크 오버헤드)
응용 계층 굿풋:            55 Mbps
                          ─────────────────
실제 파일 다운로드 속도:    55 Mbps = 6.875 MB/s
```

### 심층 동작 원리: 대역폭 효율성 결정 요인

1. **변조 방식 (Modulation Scheme)**:
   - **BPSK**: 1 bit/symbol → 1 bps/Hz (이론적)
   - **QPSK**: 2 bits/symbol → 2 bps/Hz
   - **16-QAM**: 4 bits/symbol → 4 bps/Hz
   - **64-QAM**: 6 bits/symbol → 6 bps/Hz
   - **256-QAM**: 8 bits/symbol → 8 bps/Hz
   - **1024-QAM**: 10 bits/symbol → 10 bps/Hz

2. **채널 코딩 (Channel Coding)**:
   - FEC(Forward Error Correction) 코드 비율이 효율성에 영향
   - 코드율 1/2: 효율 50% 감소 but 신뢰성 향상
   - 코드율 3/4: 효율 75% 유지
   - LDPC, 터보 코드는 샤논 한계에 근접

3. **MIMO (Multiple-Input Multiple-Output)**:
   - 공간 다중화로 효율성을 안테나 수만큼 증가
   - 4×4 MIMO: 단일 안테나 대비 최대 4배 향상
   - Massive MIMO (64×64): 5G에서 20~30배 향상

4. **다중 접속 (Multiple Access)**:
   - FDMA: 주파수 분할로 대역폭 분할
   - TDMA: 시간 분할로 슬롯 할당
   - CDMA: 코드 분할로 동시 접속
   - OFDMA: 직교 부반송파로 효율적 분할

### 핵심 수식: 샤논-하틀리 정리

```
채널 용량: C = B × log₂(1 + S/N)

여기서:
- C: 채널 용량 (bps)
- B: 대역폭 (Hz)
- S: 신호 전력 (W)
- N: 잡음 전력 (W)
- S/N: 신호 대 잡음비 (선형, dB 아님)

dB 변환: S/N(dB) = 10 × log₁₀(S/N)

예시:
B = 1 MHz, S/N = 20 dB (100:1)
C = 1×10⁶ × log₂(1 + 100) = 1×10⁶ × 6.66 ≈ 6.66 Mbps

스펙트럼 효율 한계: η_max = C/B = log₂(1 + S/N)
S/N = 20 dB → η_max ≈ 6.66 bps/Hz
```

### 핵심 코드: 대역폭 효율성 분석

```python
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ModulationScheme:
    """변조 방식 정의"""
    name: str
    bits_per_symbol: int
    required_snr_db: float  # BER 10⁻³ 기준

# 일반적인 변조 방식들
MODULATION_SCHEMES = [
    ModulationScheme("BPSK", 1, 7.0),
    ModulationScheme("QPSK", 2, 9.6),
    ModulationScheme("8-PSK", 3, 14.0),
    ModulationScheme("16-QAM", 4, 16.5),
    ModulationScheme("64-QAM", 6, 22.5),
    ModulationScheme("256-QAM", 8, 28.5),
    ModulationScheme("1024-QAM", 10, 34.5),
]

class BandwidthEfficiencyAnalyzer:
    """
    대역폭 효율성 분석기
    """
    def __init__(self, bandwidth_hz: float):
        self.bandwidth = bandwidth_hz

    def shannon_capacity(self, snr_db: float) -> float:
        """샤논 채널 용량 계산"""
        snr_linear = 10 ** (snr_db / 10)
        capacity = self.bandwidth * np.log2(1 + snr_linear)
        return capacity

    def spectral_efficiency_limit(self, snr_db: float) -> float:
        """스펙트럼 효율 이론적 한계"""
        snr_linear = 10 ** (snr_db / 10)
        return np.log2(1 + snr_linear)

    def practical_data_rate(self, modulation: ModulationScheme,
                           coding_rate: float = 3/4) -> float:
        """실제 데이터 전송 속도 계산"""
        symbol_rate = self.bandwidth  # Nyquist 가정
        data_rate = symbol_rate * modulation.bits_per_symbol * coding_rate
        return data_rate

    def practical_spectral_efficiency(self, modulation: ModulationScheme,
                                     coding_rate: float = 3/4) -> float:
        """실제 스펙트럼 효율"""
        return modulation.bits_per_symbol * coding_rate

    def efficiency_gap_to_shannon(self, modulation: ModulationScheme,
                                  coding_rate: float = 3/4) -> float:
        """샤논 한계 대비 효율 격차"""
        snr_db = modulation.required_snr_db
        shannon_eff = self.spectral_efficiency_limit(snr_db)
        practical_eff = self.practical_spectral_efficiency(modulation, coding_rate)

        return {
            'shannon_limit': shannon_eff,
            'practical': practical_eff,
            'gap_db': shannon_eff - practical_eff,
            'efficiency_percent': (practical_eff / shannon_eff) * 100
        }

class ThroughputCalculator:
    """
    처리량 및 굿풋 계산기
    """
    def __init__(self, raw_bitrate: float):
        """
        raw_bitrate: 물리 계층 원시 비트 전송 속도 (bps)
        """
        self.raw_bitrate = raw_bitrate

    def ethernet_effective_throughput(self, frame_size: int = 1500) -> float:
        """
        이더넷 유효 처리량 계산

        이더넷 프레임 구조:
        - Preamble + SFD: 8 bytes
        - Header (DA + SA + Type): 14 bytes
        - Payload: 46~1500 bytes
        - FCS: 4 bytes
        - Inter-frame Gap: 12 bytes
        """
        # 오버헤드 바이트
        preamble = 8
        header = 14
        fcs = 4
        ifg = 12

        total_frame = preamble + header + frame_size + fcs + ifg
        efficiency = frame_size / total_frame

        return self.raw_bitrate * efficiency

    def tcp_throughput(self, packet_loss: float = 0.0,
                       rtt: float = 0.01,  # 10ms
                       mss: int = 1460) -> float:
        """
        TCP 처리량 근사 계산

        TCP 처리량 공식 (간소화):
        Throughput ≈ (MSS / RTT) × (1 / sqrt(p))

        p: 패킷 손실률
        """
        if packet_loss == 0:
            return self.raw_bitrate

        # Mathis 공식 (간소화)
        tcp_throughput = (mss * 8) / (rtt * np.sqrt(packet_loss))

        # 물리적 한계 적용
        return min(tcp_throughput, self.raw_bitrate)

    def goodput_calculation(self, protocol_overhead: float = 0.1,
                           retransmission_rate: float = 0.02) -> float:
        """
        굿풋 (응용 계층 유효 속도) 계산

        Goodput = Raw Rate × (1 - Protocol OH) × (1 - Retransmission)
        """
        effective_rate = self.raw_bitrate
        effective_rate *= (1 - protocol_overhead)
        effective_rate *= (1 - retransmission_rate)
        return effective_rate

    def throughput_analysis(self) -> dict:
        """전체 처리량 분석"""
        return {
            'raw_bitrate': self.raw_bitrate,
            'ethernet_1500': self.ethernet_effective_throughput(1500),
            'ethernet_jumbo': self.ethernet_effective_throughput(9000),
            'goodput_typical': self.goodput_calculation(0.1, 0.02),
            'goodput_worst': self.goodput_calculation(0.15, 0.05),
        }

class BandwidthOptimizer:
    """
    대역폭 최적화 분석기
    """
    @staticmethod
    def find_optimal_modulation(available_snr_db: float,
                               schemes: List[ModulationScheme] = None) -> Tuple[ModulationScheme, float]:
        """
        주어진 SNR에서 최적의 변조 방식 선택
        """
        if schemes is None:
            schemes = MODULATION_SCHEMES

        candidates = [m for m in schemes if m.required_snr_db <= available_snr_db]

        if not candidates:
            return schemes[0], 0.0  # 가장 낮은 변조 방식

        # 비트/심볼이 가장 높은 것 선택
        optimal = max(candidates, key=lambda m: m.bits_per_symbol)
        margin = available_snr_db - optimal.required_snr_db

        return optimal, margin

    @staticmethod
    def adaptive_modulation_plan(snr_range: Tuple[float, float] = (0, 40),
                                 step: float = 2.0) -> List[dict]:
        """
        적응형 변조 계획 수립
        """
        plan = []
        for snr in np.arange(snr_range[0], snr_range[1], step):
            optimal, margin = BandwidthOptimizer.find_optimal_modulation(snr)
            plan.append({
                'snr_db': snr,
                'modulation': optimal.name,
                'bits_per_symbol': optimal.bits_per_symbol,
                'margin_db': margin
            })
        return plan

# 실무 사용 예시
if __name__ == "__main__":
    # 1. 대역폭 효율성 분석
    analyzer = BandwidthEfficiencyAnalyzer(bandwidth_hz=20e6)  # 20 MHz

    print("=" * 60)
    print("대역폭 효율성 분석 (20 MHz 채널)")
    print("=" * 60)

    for scheme in MODULATION_SCHEMES:
        gap_info = analyzer.efficiency_gap_to_shannon(scheme)
        print(f"\n{scheme.name}:")
        print(f"  이론적 최대: {gap_info['shannon_limit']:.2f} bps/Hz")
        print(f"  실제 효율: {gap_info['practical']:.2f} bps/Hz")
        print(f"  효율: {gap_info['efficiency_percent']:.1f}%")

    # 2. 처리량 분석
    throughput = ThroughputCalculator(raw_bitrate=1e9)  # 1 Gbps
    analysis = throughput.throughput_analysis()

    print("\n" + "=" * 60)
    print("처리량 분석 (1 Gbps 이더넷)")
    print("=" * 60)
    print(f"원시 비트 전송 속도: {analysis['raw_bitrate']/1e9:.2f} Gbps")
    print(f"이더넷 유효 (1500B): {analysis['ethernet_1500']/1e6:.2f} Mbps")
    print(f"이더넷 유효 (Jumbo): {analysis['ethernet_jumbo']/1e6:.2f} Mbps")
    print(f"굿풋 (일반): {analysis['goodput_typical']/1e6:.2f} Mbps")
    print(f"굿풋 (최악): {analysis['goodput_worst']/1e6:.2f} Mbps")

    # 3. 적응형 변조 계획
    print("\n" + "=" * 60)
    print("적응형 변조 계획")
    print("=" * 60)
    plan = BandwidthOptimizer.adaptive_modulation_plan()
    for entry in plan[::5]:  # 5개씩 건너뛰어 출력
        print(f"SNR {entry['snr_db']:>2}dB → {entry['modulation']:<10} "
              f"(Margin: {entry['margin_db']:.1f}dB)")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 변조 방식별 스펙트럼 효율

| 변조 방식 | 비트/심볼 | 요구 SNR (BER 10⁻³) | 이론적 효율 | 실제 효율 (3/4 코딩) |
|----------|----------|-------------------|------------|-------------------|
| **BPSK** | 1 | 7 dB | 6.66 bps/Hz | 0.75 bps/Hz |
| **QPSK** | 2 | 9.6 dB | 7.25 bps/Hz | 1.5 bps/Hz |
| **16-QAM** | 4 | 16.5 dB | 8.5 bps/Hz | 3.0 bps/Hz |
| **64-QAM** | 6 | 22.5 dB | 10.5 bps/Hz | 4.5 bps/Hz |
| **256-QAM** | 8 | 28.5 dB | 13.0 bps/Hz | 6.0 bps/Hz |

### 과목 융합 관점 분석

1. **신호처리와의 융합**:
   - **FFT/IFFT**: OFDM에서 대역폭을 부반송파로 분할하여 효율성 향상
   - **등화기(Equalizer)**: 주파수 선택적 페이딩 환경에서 대역폭 효율 유지

2. **정보이론과의 융합**:
   - **엔트로피**: 소스 코딩으로 데이터 압축, 유효 대역폭 증가
   - **상호 정보량**: MIMO 채널 용량 계산의 기초

3. **네트워크와의 융합**:
   - **QoS**: 대역폭 할당 및 트래픽 쉐이핑
   - **혼잡 제어**: TCP 혼잡 윈도우가 유효 대역폭 결정

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 5G 기지국 대역폭 계획

**문제 상황**: 100 MHz 대역폭을 가진 5G 기지국에서 eMBB(Enhanced Mobile Broadband) 서비스를 제공해야 합니다. 셀 에지 사용자의 SNR은 10dB, 셀 중심 사용자의 SNR은 25dB입니다.

**기술사의 분석 및 해결 과정**:

1. **샤논 한계 계산**:
   - 셀 에지 (10 dB): η_max = log₂(1 + 10) ≈ 3.46 bps/Hz
   - 셀 중심 (25 dB): η_max = log₂(1 + 316) ≈ 8.29 bps/Hz

2. **적응형 변조 적용**:
   - 셀 에지: QPSK + 1/2 코딩 → 1.0 bps/Hz → 100 Mbps
   - 셀 중심: 256-QAM + 3/4 코딩 → 6.0 bps/Hz → 600 Mbps

3. **MIMO 게인**: 4×4 MIMO로 4배 향상 가정
   - 셀 에지: 400 Mbps
   - 셀 중심: 2.4 Gbps

### 도입 시 고려사항 체크리스트

| 항목 | 확인 내용 | 권장 기준 |
|------|----------|----------|
| **주파수 대역** | 가용 대역폭 확보 | 서비스 요구사항 대비 1.5배 |
| **SNR 분포** | 셀 커버리지별 품질 | 적응형 변조 지원 |
| **간섭 환경** | 인접 셀 간섭 레벨 | ICIC/CoMP 고려 |
| **트래픽 패턴** | 피크 시간대 요구량 | 1.2~1.5배 프로비저닝 |

---

## V. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 | 측정 지표 | 개선 폭 |
|------|----------|---------|
| **스펙트럼 효율** | bps/Hz | 4G→5G: 2배 향상 |
| **사용자 처리량** | Mbps | 10배 향상 |
| **주파수 활용** | % | 90%+ 달성 |

### 미래 전망

- **6G**: THz 대역폭 활용, 100 bps/Hz 목표
- **AI 기반 최적화**: 실시간 대역폭 할당
- **양자 통신**: 새로운 대역폭 패러다임

### 참고 표준

| 표준 | 기관 | 내용 |
|------|------|------|
| **ITU-R SM.328** | ITU | 스펙트럼 효율 정의 |
| **3GPP TS 38.101** | 3GPP | 5G NR 주파수 대역 |
| **IEEE 802.11** | IEEE | Wi-Fi 대역폭 사양 |

---

## 관련 개념 맵 (Knowledge Graph)
- [샤논 채널 용량](./shannon_hartley_capacity.md) - 이론적 한계
- [변조 기술](./modulation_ask_fsk_psk_qam.md) - QAM 효율성
- [OFDM 다중화](./multiplexing_fdm_tdm_wdm.md) - 주파수 효율적 활용
- [MIMO 기술](../5_wireless/mimo_technology.md) - 공간 다중화
- [TCP 혼잡 제어](../2_transport/tcp_congestion_control.md) - 처리량 최적화

---

## 어린이를 위한 3줄 비유 설명
1. **대역폭**은 **'도로의 차선 수'**와 같아요. 차선이 많을수록 더 많은 차가 동시에 달릴 수 있죠.
2. **대역폭 효율성**은 **'차선당 지나가는 차 수'**예요. 똑같은 4차선 도로에서 더 많은 차를 보내면 효율이 높은 거예요.
3. **샤논 한계**는 **'물리학의 법칙'** 같은 거예요. 아무리 좋은 기술을 써도 도로가 감당할 수 있는 최대 차량 수는 정해져 있답니다!
