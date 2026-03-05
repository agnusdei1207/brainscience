+++
title = "021. 샤논 채널 용량 (Shannon Capacity) - ISI"
description = "샤논-하틀리 정리와 심볼 간 간섭(ISI)의 관계, 채널 용량의 이론적 한계, ISI 완화 기법 및 실무 적용 사례를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["ShannonCapacity", "ISI", "IntersymbolInterference", "ChannelCapacity", "SNR", "Equalizer"]
categories = ["studynotes-3_network"]
+++

# 021. 샤논 채널 용량과 ISI (Shannon Capacity & Inter-Symbol Interference)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 샤논-하틀리 정리 C = B × log₂(1 + S/N)는 잡음이 있는 채널의 이론적 최대 전송 속도를 정의하며, ISI(심볼 간 간섭)는 대역 제한 채널에서 심볼이 퍼져 다음 심볼에 간섭을 주어 오류율을 증가시키는 현상입니다.
> 2. **가치**: 샤논 한계는 어떤 코딩 방식으로도 넘을 수 없는 절대적 상한으로, ISI는 이 한계에 도달하는 것을 방해하는 주요 장애물입니다. ISI 제거를 위해 등화기(Equalizer), OFDM, 나이퀴스트 필터링이 사용됩니다.
> 3. **융합**: 5G/6G에서는 Massive MIMO와 OFDM을 결합하여 ISI를 완화하고, LDPC/Polar 코드로 샤논 한계에 0.1 dB 이내로 근접합니다. 이러한 기술들의 융합이 초고속 통신을 가능하게 합니다.

---

## I. 개요 (Context & Background)

### 샤논-하틀리 정리 (Shannon-Hartley Theorem)

**샤논-하틀리 정리**는 1948년 Claude Shannon이 발표한 정보 이론의 핵심 정리로, **잡음이 있는 채널에서 오류 없이 전송할 수 있는 최대 정보 전송 속도**를 규명합니다.

```
채널 용량: C = B × log₂(1 + S/N)

C: 채널 용량 (bps)
B: 채널 대역폭 (Hz)
S: 신호 전력 (W)
N: 잡음 전력 (W)
S/N: 신호 대 잡음비 (선형, 비데시벨)
```

### 심볼 간 간섭 (ISI: Inter-Symbol Interference)

**ISI**는 대역 제한 채널을 통과한 펄스가 **시간적으로 퍼지면서(spread)** 인접한 심볼의 샘플링 시점에 간섭을 주는 현상입니다. 이는:

1. **대역 제한**: 실제 채널은 무한 대역폭을 가질 수 없음
2. **다중 경로**: 무선 채널에서 신호가 여러 경로로 도착
3. **필터링 불완전**: 송수신 필터의 이상적이지 않은 응답

으로 인해 발생합니다.

**💡 비유**: ISI를 **'여러 사람이 동시에 말하는 파티'**에 비유할 수 있습니다.

- **샤논 용량**은 방의 소음 수준에서 **몇 명까지가 서로의 말을 이해하며 대화할 수 있는지**에 대한 이론적 한계입니다.
- **ISI**는 앞 사람의 말이 **메아리처럼 퍼져서** 다음 사람의 말과 섞이는 현상입니다.
- ISI가 심하면 아무리 좋은 코딩을 사용해도(= 아무리 잘 들으려 해도) 정보를 복원할 수 없습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 정교한 구조 다이어그램: 샤논 용량과 ISI의 관계

```ascii
================================================================================
[ 샤논-하틀리 채널 용량 ]
================================================================================

채널 용량 공식: C = B × log₂(1 + S/N)

┌──────────────────────────────────────────────────────────────────────────────┐
│                          채널 용량의 구성 요소                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│     대역폭 B                  S/N 비율                    용량 C            │
│  ┌─────────────┐          ┌─────────────┐           ┌─────────────┐        │
│  │             │          │             │           │             │        │
│  │  주파수     │          │  신호 강도  │           │  최대       │        │
│  │  자원       │    ×     │  ───────    │     =     │  무오류     │        │
│  │  (Hz)       │          │  잡음 강도  │           │  전송속도   │        │
│  │             │          │             │           │  (bps)      │        │
│  └─────────────┘          └─────────────┘           └─────────────┘        │
│                                                                              │
│  • B ↑ → C ↑ (선형)     • S/N ↑ → C ↑ (로그)    • 이론적 상한            │
│  • 2배 대역폭 = 2배 용량  • 10dB 증가 ≈ 3.3배    • 달성 불가, 근접 가능    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


================================================================================
[ S/N(dB)에 따른 스펙트럼 효율 한계 ]
================================================================================

S/N (dB) │  S/N (선형)  │  log₂(1+S/N)  │  효율 (bps/Hz) │  비고
─────────┼──────────────┼───────────────┼────────────────┼──────────────────
    0 dB │        1.0   │       1.0     │       1.0      │  S=N
   10 dB │       10.0   │       3.46    │       3.46     │  일반적 무선
   20 dB │      100.0   │       6.66    │       6.66     │  좋은 채널
   30 dB │     1000.0   │       9.97    │       9.97     │  우수한 채널
   40 dB │    10000.0   │      13.29    │      13.29     │  매우 우수
   50 dB │   100000.0   │      16.61    │      16.61     │  케이블/광
  100 dB │  10000000.0  │      23.25    │      23.25     │  이론적


================================================================================
[ ISI (심볼 간 간섭) 발생 메커니즘 ]
================================================================================

1. 대역 제한 채널에서의 펄스 확산

송신 심볼 1      송신 심볼 2      송신 심볼 3
    │               │               │
    ▼               ▼               ▼
  ┌───┐           ┌───┐           ┌───┐
  │ □ │           │ □ │           │ □ │  (이상적 사각 펄스)
  └───┘           └───┘           └───┘
    │               │               │
    │   채널 통과 (대역 제한)
    ▼               ▼               ▼
  ┌───┐           ┌───┐           ┌───┐
  │ ◠ │           │ ◠ │           │ ◠ │  (퍼진 펄스 = ISI)
  └───┘           └───┘           └───┘
    │             │ │             │ │
    │             │ │             │ │
    │    ←─────→ │ │ ←─────→     │ │
    │      ISI   │ │    ISI      │ │
    │            │ │             │
    ▼            ▼ ▼             ▼ ▼
  ──────────────────────────────────────────> 시간
    t₁           t₂              t₃

심볼 1의 꼬리가 심볼 2의 샘플링 시점(t₂)에 간섭!


2. 다중 경로로 인한 ISI (무선 채널)

송신기 ────────────────────────> 수신기
          │ 직접 경로 (τ₁)
          │
          └───> 건물 반사 (τ₂ > τ₁)
                  │
                  └───> 지면 반사 (τ₃ > τ₂)

수신 신호 = 직접파 + 반사파₁ + 반사파₂ + ...

  직접파:   ┌───┐
            │ □ │
            └───┘
  반사파₁:    ┌───┐
              │ □ │
              └───┘
  반사파₂:      ┌───┐
                │ □ │
                └───┘
  ───────────────────────────────────────> 시간

합성 신호 (ISI 발생!):
  ┌───┐ ┌───┐ ┌───┐
  │█████│█████│█████│  ← 심볼 경계가 불명확
  └───┘ └───┘ └───┘


================================================================================
[ ISI의 영향: 눈 다이어그램 (Eye Diagram) ]
================================================================================

ISI 없음 (이상적):           ISI 있음 (현실적):

      ┌─────┐                      ┌──┬──┐
      │     │                     ╱╲ │  │╲
      │     │                    ╱  ╲│  │ ╲╲
      │     │                   ╱    │  │   ╲
  ────┤     ├───>            ───╱─────┼──┼────╲──> 시간
      │     │                  ╲      │  │    ╱
      │     │                   ╲    │  │   ╱
      │     │                    ╲  ╱│  │  ╱
      └─────┘                     ╲╱ └──┘╱
                                     ↑
                                 열린 눈 (Eye Opening)
                                 ↑ 작을수록 ISI 심각

ISI가 심하면:
- 눈이 완전히 닫힘 → 심볼 구분 불가 → 높은 BER
- S/N 요구량 증가 → 샤논 한계 달성 어려움


================================================================================
[ ISI 완화 기법 ]
================================================================================

┌──────────────────────────────────────────────────────────────────────────────┐
│  1. 나이퀴스트 필터링 (Raised Cosine)                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  송신 필터: √(Raised Cosine)    채널    수신 필터: √(Raised Cosine)          │
│                                                                              │
│  전체 응답 = Raised Cosine (ISI 없음)                                        │
│                                                                              │
│  조건: 심볼 주기 T의 정수배에서 0                                            │
│                                                                              │
│       ┌───┐                                                                  │
│       │ ◠ │    ────────┬────────┬────────>                                  │
│       └───┘            │        │                                           │
│              -2T       -T    0  T      2T                                    │
│                         ↑                                                   │
│                    샘플링 시점                                               │
│                   (인접 심볼 기여도 = 0)                                     │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  2. 등화기 (Equalizer)                                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  채널 응답 H(f)의 역특성 1/H(f)를 적용하여 ISI 제거                          │
│                                                                              │
│  종류:                                                                       │
│  • 선형 등화기 (LE): FIR 필터                                                │
│  • 결정 피드백 등화기 (DFE): 과거 결정 사용                                  │
│  • MLSE (Viterbi): 최대 우도 시퀀스 추정                                     │
│  • 적응형 등화기: 채널 변화에 따라 계수 업데이트                              │
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                │
│  │  수신 신호   │ ──> │  등화기      │ ──> │  ISI 제거된  │                │
│  │  (ISI 포함)  │     │  H_eq(f)     │     │  신호        │                │
│  └──────────────┘     └──────────────┘     └──────────────┘                │
│                                                                              │
│  H_eq(f) ≈ 1 / H_channel(f)                                                 │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│  3. OFDM (직교 주파수 분할 다중화)                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  광대역 채널 → 다수의 협대역 부반송파로 분할                                 │
│  각 부반송파에서는 평탄한 페이딩 (ISI 영향 최소화)                            │
│                                                                              │
│  대역폭 W                                                                               │
│  ┌────────────────────────────────────┐                                     │
│  │ 부반송파 1 │ 2 │ 3 │ 4 │ ... │ N │       │                                     │
│  │  (협대역) │   │   │   │     │   │       │                                     │
│  └────────────────────────────────────┘                                     │
│                                                                              │
│  CP (Cyclic Prefix) 추가로 ISI 완전 제거:                                    │
│  ┌─────┬────────────────────────┐                                           │
│  │ CP  │      심볼 데이터        │                                           │
│  └─────┴────────────────────────┘                                           │
│    ↑                                                                        │
│  채널 지연 확산보다 김 → ISI 차단                                            │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 수식

```
1. 샤논-하틀리 정리:
   C = B × log₂(1 + S/N)

2. dB 변환:
   S/N (dB) = 10 × log₁₀(S/N)

3. S/N과 Eb/N₀의 관계:
   S/N = (R_b/B) × (E_b/N₀)

   여기서:
   - R_b: 비트 레이트 (bps)
   - E_b: 비트당 에너지 (J)
   - N₀: 잡음 전력 스펙트럼 밀도 (W/Hz)

4. 샤논 한계 (B = 1 Hz):
   C = log₂(1 + S/N) bps/Hz

5. ISI 제거 조건 (나이퀴스트):
   h(nT) = 0 for n ≠ 0
   h(0) = 1
```

### 핵심 코드: 샤논 용량 및 ISI 분석

```python
import numpy as np
from typing import Tuple, List
from dataclasses import dataclass

@dataclass
class ChannelParameters:
    """채널 파라미터"""
    bandwidth_hz: float
    snr_db: float
    noise_figure_db: float = 0.0

    @property
    def snr_linear(self) -> float:
        return 10 ** (self.snr_db / 10)

class ShannonCapacityAnalyzer:
    """
    샤논 채널 용량 분석기
    """

    @staticmethod
    def calculate_capacity(bandwidth_hz: float, snr_db: float) -> float:
        """
        샤논 용량 계산

        C = B × log₂(1 + S/N)
        """
        snr_linear = 10 ** (snr_db / 10)
        capacity = bandwidth_hz * np.log2(1 + snr_linear)
        return capacity

    @staticmethod
    def calculate_spectral_efficiency_limit(snr_db: float) -> float:
        """
        스펙트럼 효율 이론적 한계 (bps/Hz)
        """
        snr_linear = 10 ** (snr_db / 10)
        return np.log2(1 + snr_linear)

    @staticmethod
    def required_snr_for_rate(target_rate_bps: float, bandwidth_hz: float) -> float:
        """
        목표 레이트 달성에 필요한 최소 SNR
        """
        spectral_efficiency = target_rate_bps / bandwidth_hz
        if spectral_efficiency <= 0:
            return float('-inf')
        snr_linear = 2 ** spectral_efficiency - 1
        return 10 * np.log10(snr_linear)

    @staticmethod
    def required_bandwidth(target_rate_bps: float, snr_db: float) -> float:
        """
        목표 레이트 달성에 필요한 대역폭
        """
        snr_linear = 10 ** (snr_db / 10)
        efficiency = np.log2(1 + snr_linear)
        return target_rate_bps / efficiency

    @staticmethod
    def capacity_gap_to_shannon(bandwidth_hz: float, snr_db: float,
                                achieved_rate_bps: float) -> dict:
        """
        달성된 레이트와 샤논 한계의 격차
        """
        shannon_capacity = ShannonCapacityAnalyzer.calculate_capacity(
            bandwidth_hz, snr_db)
        gap_factor = shannon_capacity / achieved_rate_bps
        gap_db = 10 * np.log10(gap_factor) if gap_factor > 0 else float('inf')

        return {
            'shannon_capacity_bps': shannon_capacity,
            'achieved_rate_bps': achieved_rate_bps,
            'efficiency_percent': (achieved_rate_bps / shannon_capacity) * 100,
            'gap_db': gap_db
        }

class ISIAnalyzer:
    """
    ISI 분석기
    """

    @staticmethod
    def raised_cosine_pulse(t: np.ndarray, T: float, alpha: float) -> np.ndarray:
        """
        Raised Cosine 펄스
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            numerator = np.sin(np.pi * t / T) * np.cos(np.pi * alpha * t / T)
            denominator = (np.pi * t / T) * (1 - (2 * alpha * t / T) ** 2)
            pulse = numerator / denominator

            # 특수점 처리
            pulse[np.abs(t) < 1e-10] = 1.0

            # α = 0인 특수점
            if alpha > 0:
                special_idx = np.abs(np.abs(2 * alpha * t / T) - 1) < 1e-10
                t_special = t[special_idx]
                pulse[special_idx] = (np.sin(np.pi / (2 * alpha)) *
                                     np.cos(np.pi / 2) / 4)

        return pulse

    @staticmethod
    def multipath_channel_model(num_paths: int, max_delay_spread: float,
                                seed: int = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        다중 경로 채널 모델
        """
        if seed is not None:
            np.random.seed(seed)

        # 지연 시간
        delays = np.sort(np.random.uniform(0, max_delay_spread, num_paths))

        # 복소수 이득 (Rayleigh 페이딩)
        gains = (np.random.randn(num_paths) + 1j * np.random.randn(num_paths)) / np.sqrt(2)

        # 정규화
        gains = gains / np.sum(np.abs(gains))

        return delays, gains

    @staticmethod
    def calculate_rms_delay_spread(delays: np.ndarray, gains: np.ndarray) -> float:
        """
        RMS 지연 확산 계산
        """
        power = np.abs(gains) ** 2
        mean_delay = np.sum(delays * power)
        rms_spread = np.sqrt(np.sum((delays - mean_delay) ** 2 * power))
        return rms_spread

    @staticmethod
    def coherence_bandwidth(rms_delay_spread: float, factor: float = 1.0) -> float:
        """
        코히어런스 대역폭 계산
        """
        return factor / rms_delay_spread

class EyeDiagramGenerator:
    """
    눈 다이어그램 생성기
    """

    @staticmethod
    def generate_eye_diagram(signal: np.ndarray, samples_per_symbol: int,
                             num_symbols: int) -> np.ndarray:
        """
        눈 다이어그램 생성
        """
        eye_length = 2 * samples_per_symbol
        num_traces = len(signal) // samples_per_symbol - 1

        eye_diagram = np.zeros((eye_length, num_traces))

        for i in range(num_traces):
            start = i * samples_per_symbol
            end = start + eye_length
            if end <= len(signal):
                eye_diagram[:, i] = signal[start:end]

        return eye_diagram

    @staticmethod
    def eye_opening(eye_diagram: np.ndarray) -> dict:
        """
        눈 개방도 계산
        """
        max_values = np.max(eye_diagram, axis=1)
        min_values = np.min(eye_diagram, axis=1)

        eye_height = np.min(max_values) - np.max(min_values)
        eye_center = np.argmin(max_values - min_values)

        return {
            'eye_height': eye_height,
            'eye_center_index': eye_center,
            'is_open': eye_height > 0
        }

# 실무 사용 예시
if __name__ == "__main__":
    # 1. 샤논 용량 분석
    print("=" * 60)
    print("샤논 채널 용량 분석")
    print("=" * 60)

    shannon = ShannonCapacityAnalyzer()

    # 대역폭 20 MHz, 다양한 SNR
    bandwidth = 20e6  # 20 MHz

    for snr_db in [0, 10, 20, 30, 40]:
        capacity = shannon.calculate_capacity(bandwidth, snr_db)
        efficiency = shannon.calculate_spectral_efficiency_limit(snr_db)
        print(f"SNR {snr_db:3d} dB: 용량 = {capacity/1e6:7.2f} Mbps, "
              f"효율 = {efficiency:5.2f} bps/Hz")

    # 2. 목표 레이트에 필요한 SNR
    print("\n" + "=" * 60)
    print("100 Mbps 달성에 필요한 SNR (대역폭별)")
    print("=" * 60)

    target_rate = 100e6  # 100 Mbps

    for bw_mhz in [5, 10, 20, 40]:
        bw_hz = bw_mhz * 1e6
        req_snr = shannon.required_snr_for_rate(target_rate, bw_hz)
        print(f"대역폭 {bw_mhz:3d} MHz: 필요 SNR = {req_snr:6.2f} dB")

    # 3. 다중 경로 채널 ISI 분석
    print("\n" + "=" * 60)
    print("다중 경로 채널 ISI 분석")
    print("=" * 60)

    isi_analyzer = ISIAnalyzer()

    # 5개 경로, 최대 5μs 지연
    delays, gains = isi_analyzer.multipath_channel_model(
        num_paths=5, max_delay_spread=5e-6, seed=42)

    rms_spread = isi_analyzer.calculate_rms_delay_spread(delays, gains)
    coh_bw = isi_analyzer.coherence_bandwidth(rms_spread)

    print(f"경로 수: {len(delays)}")
    print(f"RMS 지연 확산: {rms_spread*1e6:.2f} μs")
    print(f"코히어런스 대역폭: {coh_bw/1e3:.2f} kHz")

    # 4. 샤논 한계와 실제 시스템 비교
    print("\n" + "=" * 60)
    print("실제 시스템과 샤논 한계 비교")
    print("=" * 60)

    systems = [
        ("LTE (20 MHz, 16-QAM)", 20e6, 15, 75e6),
        ("5G NR (100 MHz, 256-QAM)", 100e6, 25, 800e6),
        ("Wi-Fi 6 (160 MHz, 1024-QAM)", 160e6, 30, 1.2e9),
    ]

    for name, bw, snr, achieved_rate in systems:
        gap = shannon.capacity_gap_to_shannon(bw, snr, achieved_rate)
        print(f"\n{name}:")
        print(f"  샤논 한계: {gap['shannon_capacity_bps']/1e6:.1f} Mbps")
        print(f"  달성 레이트: {gap['achieved_rate_bps']/1e6:.1f} Mbps")
        print(f"  효율: {gap['efficiency_percent']:.1f}%")
        print(f"  격차: {gap['gap_db']:.2f} dB")
