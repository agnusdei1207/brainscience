+++
title = "026. 지연 왜곡 (Delay Distortion)"
description = "지연 왜곡의 발생 원리, 위상 지연, 군지연, 주파수 의존성, 보정 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["DelayDistortion", "GroupDelay", "PhaseDelay", "Dispersion", "Equalization", "ChannelResponse"]
categories = ["studynotes-3_network"]
+++

# 026. 지연 왜곡 (Delay Distortion)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 지연 왜곡은 채널의 주파수 응답이 비선형적이어서 서로 다른 주파수 성분이 다른 속도로 전파되어 신호 형태가 변형되는 현상입니다.
> 2. **가치**: 군지연(Group Delay) 분석은 채널 등화기(Equalizer) 설계와 광섬유 분산 보상의 핵심 이론적 기반을 제공합니다.
> 3. **융합**: 광섬유의 색분산(Chromatic Dispersion), 무선 다중경로의 위상 왜곡, 오디오의 선형성 평가 모두 지연 왜곡 이론에 기반합니다.

---

## I. 개요 (Context & Background)

지연 왜곡(Delay Distortion)은 신호를 구성하는 **각 주파수 성분이 서로 다른 시간 지연을 경험하여 신호 형태가 왜곡되는 현상**입니다. 이상적인 채널은 모든 주파수를 동일한 속도로 전달하지만, 실제 채널은 주파수에 따라 다른 위상 변화를 일으킵니다.

**핵심 개념**:

1. **위상 지연 (Phase Delay, τₚ)**:
   ```
   τₚ(ω) = -φ(ω) / ω
   ```
   특정 주파수의 위상이 얼마나 지연되는지

2. **군지연 (Group Delay, τg)**:
   ```
   τg(ω) = -dφ(ω) / dω
   ```
   신호 패킷(군)이 전달되는 지연 시간

**비유**: 지연 왜곡은 **"오케스트라에서 악기마다 소리가 다르게 늦게 도착하는 현상"**과 같습니다.
- **이상적**: 모든 악기 소리가 동시에 도착하여 완벽한 화음
- **지연 왜곡**: 피아노는 빨리, 첼로는 늦게 도착하여 음이 어긋남
- **군지연**: 전체 오케스트라 소리의 "덩어리"가 얼마나 늦게 도착하는지

**등장 배경 및 발전 과정**:
1. **전화망 분석 (1910~20년대)**: 장거리 전화 회선에서 음성 왜곡이 관찰되었습니다.
2. **Bode의 연구 (1940년대)**: Hendrik Bode가 위상-진폭 관계와 군지연을 체계화했습니다.
3. **광통신 분산 (1980년대~)**: 고속 광통신에서 분산 보상이 핵심 이슈가 되었습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 위상 지연 vs 군지연

| 구분 | 정의 | 수식 | 물리적 의미 |
|------|------|------|------------|
| **위상 지연** | 단일 주파수 위상 지연 | τₚ = -φ/ω | 반송파의 지연 |
| **군지연** | 주파수 변화에 대한 위상 변화율 | τg = -dφ/dω | 펄스/패킷의 지연 |
| **비선형 위상** | 주파수에 따른 위상 기울기 변화 | φ(ω) ≠ -ωτ | 지연 왜곡 원인 |

**선형 위상 시스템**:
```
이상적: φ(ω) = -ωτ₀ (τ₀는 상수)

위상 지연 = 군지연 = τ₀ (모든 주파수에서 동일)

H(ω) = |H(ω)| × e^(-jωτ₀)
```

**비선형 위상 시스템 (지연 왜곡)**:
```
φ(ω) ≠ -ωτ (비선형)

위상 지연 ≠ 군지연 (주파수마다 다름)

→ 펄스가 퍼짐 (Pulse Spreading)
→ 신호 왜곡 발생
```

### 정교한 구조 다이어그램: 지연 왜곡 메커니즘

```ascii
================================================================================
[ Phase Delay vs Group Delay ]
================================================================================

위상 φ(ω)
    ^
    |                        비선형 위상
    |                      /
    |                    /
    |                  /      φ(ω) = 실제 채널
    |                /
    |              /          τg = -dφ/dω = 기울기
    |            /
    |          /------------ 선형 위상 (이상적)
    |        /                  τg = 상수
    |      /
    |    /
    |  /
    +----------------------------------> ω (주파수)
    0

    기울기가 일정하면 → 군지연 일정 → 지연 왜곡 없음
    기울기가 변하면 → 군지연 변화 → 지연 왜곡 발생

================================================================================
[ Group Delay Variation and Signal Distortion ]
================================================================================

입력 펄스                    채널 (비선형 위상)                   출력 펄스
    ___                                                            ____
   |   |                                                          /    \
   |   |                        위상 응답 φ(ω)                    /      \
   |   |                    _______________                      /        \
   |   |                   /               \                    /          \
   |___|                  /                 \      ___---------/            \---------___
          ============>   /   군지연 변화     \  ==========>

    단일 펄스              주파수 성분마다 다른 지연         펄스 퍼짐 (Spreading)

    τg_low < τg_mid < τg_high
    저주파가 먼저, 고주파가 나중에 도착
    → 펄스가 시간 영역에서 확산

================================================================================
[ Frequency Domain View: Amplitude and Phase Response ]
================================================================================

|H(ω)| (진폭)
    ^
  1 |------------------.
    |                   \
    |                    \      통과 대역
    |                     \____________
  0 +-------------------------------------> ω
       ω₁               ωc              ω₂

φ(ω) (위상)
    ^
    |         /
    |        /    비선형 구간
    |       /
    |      /
    |_____/_______________________________> ω
    0    ω₁            ωc            ω₂

τg(ω) (군지연)
    ^
    |      _____
    |     /     \       군지연 리플
    |    /       \
    |   /         \_____
    |__/_______________________________> ω
       ω₁       ωc       ω₂

    이상적: τg(ω) = 상수 (평탄)
    실제: 주파수에 따라 변동 (리플)
    리플이 클수록 지연 왜곡 심각

================================================================================
[ Optical Fiber: Chromatic Dispersion ]
================================================================================

광섬유에서의 지연 왜곡 = 색분산 (Chromatic Dispersion)

시간
  ^
  | 입력 펄스           광섬유              출력 펄스
  |    ___                                 ____,
  |   |   |                               /    \
  |   |   |          λ₁ (빠름) ======>   /      \  λ₁
  |   |   |          λ₂ (보통) ======>   /        \___
  |   |___|          λ₃ (느림) ======>  /            \____
  |
  +----------------------------------------------> 거리

    파장별로 군지연이 다름
    D = dτg/dλ [ps/(nm·km)]
    SMF @ 1550nm: D ≈ 17 ps/(nm·km)

    10 Gbps 신호, 80km 전송:
    펄스 폭 증가 = |D| × L × Δλ
                = 17 × 80 × 0.1 nm = 136 ps

================================================================================
```

### 매체별 지연 왜곡 특성

| 매체 | 원인 | 군지연 특성 | 영향 | 보상 방법 |
|------|------|------------|------|----------|
| **광섬유 SMF** | 색분산 | λ에 의존 | 펄스 확산 | DCF, DSP |
| **광섬유 MMF** | 모드 분산 | 모드에 의존 | 대역폭 제한 | 단일모드 사용 |
| **동축 케이블** | 피부 효과 | √f 의존 | 고주파 지연 | 이퀄라이저 |
| **음향 채널** | 매질 특성 | f 의존 | 음질 왜곡 | FIR 보정 |
| **무선 다중경로** | 경로 차이 | 위치 의존 | 심볼 간섭 | OFDM, Rake |

### 핵심 코드: 군지연 분석 및 보상 (Python)

```python
import numpy as np
from scipy import signal
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional
from dataclasses import dataclass

@dataclass
class ChannelResponse:
    """채널 주파수 응답"""
    frequencies: np.ndarray      # 주파수 배열 (Hz)
    magnitude: np.ndarray        # 진폭 응답 |H(f)|
    phase: np.ndarray            # 위상 응답 φ(f) (rad)


class DelayDistortionAnalyzer:
    """
    지연 왜곡 분석 및 보상 클래스
    """

    def __init__(self, sample_rate: float = 1e6):
        """
        Args:
            sample_rate: 샘플링 레이트 (Hz)
        """
        self.sample_rate = sample_rate

    def calculate_phase_delay(self, phase: np.ndarray, freq: np.ndarray) -> np.ndarray:
        """
        위상 지연 계산

        τₚ(ω) = -φ(ω) / ω

        Args:
            phase: 위상 배열 (rad)
            freq: 주파수 배열 (Hz)

        Returns:
            위상 지연 배열 (초)
        """
        omega = 2 * np.pi * freq
        # 0 주파수 제외 (division by zero 방지)
        phase_delay = np.zeros_like(phase)
        mask = omega != 0
        phase_delay[mask] = -phase[mask] / omega[mask]
        return phase_delay

    def calculate_group_delay(self, phase: np.ndarray, freq: np.ndarray) -> np.ndarray:
        """
        군지연 계산

        τg(ω) = -dφ(ω) / dω

        수치 미분 사용

        Args:
            phase: 위상 배열 (rad)
            freq: 주파수 배열 (Hz)

        Returns:
            군지연 배열 (초)
        """
        omega = 2 * np.pi * freq
        d_omega = np.diff(omega)
        d_phase = np.diff(phase)

        # 수치 미분 (중앙 차분)
        group_delay = np.zeros_like(phase)
        group_delay[1:-1] = -np.gradient(phase, omega)[1:-1]
        group_delay[0] = group_delay[1]
        group_delay[-1] = group_delay[-2]

        return group_delay

    def analyze_channel(
        self,
        impulse_response: np.ndarray
    ) -> ChannelResponse:
        """
        채널 임펄스 응답으로부터 주파수 응답 분석

        Args:
            impulse_response: 채널 임펄스 응답

        Returns:
            ChannelResponse 객체
        """
        n = len(impulse_response)
        freq_response = fft(impulse_response, n)
        freqs = fftfreq(n, 1/self.sample_rate)

        # 양의 주파수만 사용
        pos_mask = freqs >= 0
        freqs_pos = freqs[pos_mask]
        h_pos = freq_response[pos_mask]

        magnitude = np.abs(h_pos)

        # 위상 언래핑 (unwrap)
        phase = np.unwrap(np.angle(h_pos))

        return ChannelResponse(
            frequencies=freqs_pos,
            magnitude=magnitude,
            phase=phase
        )

    def generate_nonlinear_phase_channel(
        self,
        n_taps: int = 101,
        cutoff_freq: float = 0.3,
        ripple_db: float = 0.5,
        group_delay_variation: float = 10.0
    ) -> np.ndarray:
        """
        비선형 위상을 가진 채널 생성

        Args:
            n_taps: 필터 탭 수
            cutoff_freq: 정규화 차단 주파수 (0~1)
            ripple_db: 군지연 리플 (dB)
            group_delay_variation: 군지연 변화량 (샘플)

        Returns:
            채널 임펄스 응답
        """
        # 기본 저역 통과 필터
        b, a = signal.butter(5, cutoff_freq, btype='low')

        # 비선형 위상 추가 (All-pass 섹션)
        # 2차 all-pass: H(z) = (a + z^-1) / (1 + a*z^-1)
        all_pass_coeff = 0.7

        # 주파수 영역에서 위상 왜곡 추가
        n_freq = 1024
        freqs = np.linspace(0, self.sample_rate/2, n_freq)

        # 기본 필터 응답
        w, h_lowpass = signal.freqz(b, a, worN=n_freq, fs=self.sample_rate)

        # 비선형 위상 추가
        # 2차 함수 형태의 위상 왜곡
        center_freq = self.sample_rate / 4
        phase_distortion = group_delay_variation * 1e-6 * (freqs - center_freq)**2 / (self.sample_rate**2)

        h_distorted = h_lowpass * np.exp(1j * (np.angle(h_lowpass) + phase_distortion * 2 * np.pi * freqs))

        # 시간 영역으로 변환
        h_full = np.concatenate([h_distorted, np.conj(h_distorted[-2:0:-1])])
        impulse_response = np.real(ifft(h_full))

        # 윈도우 적용
        window = np.zeros(len(impulse_response))
        center = len(impulse_response) // 2
        window[center-n_taps//2:center+n_taps//2+1] = 1

        return impulse_response * window

    def design_group_delay_equalizer(
        self,
        target_group_delay: np.ndarray,
        freqs: np.ndarray,
        n_taps: int = 101
    ) -> np.ndarray:
        """
        군지연 등화기 설계

        Args:
            target_group_delay: 보상할 군지연 (초)
            freqs: 주파수 배열 (Hz)
            n_taps: 필터 탭 수

        Returns:
            등화기 임펄스 응답
        """
        # 목표: 군지연을 평탄하게 만드는 all-pass 필터
        # 역 위상 특성을 가진 필터 설계

        # 평균 군지연 계산
        mean_delay = np.mean(target_group_delay)
        delay_correction = mean_delay - target_group_delay

        # 위상 보정량 계산
        # τg = -dφ/dω → φ = -∫τg dω
        omega = 2 * np.pi * freqs
        phase_correction = -np.cumsum(delay_correction) * np.diff(omega, prepend=0)

        # 주파수 응답 구성 (all-pass: |H| = 1)
        h_equalizer = np.exp(1j * phase_correction)

        # 양/음 주파수 대칭
        h_full = np.concatenate([h_equalizer, np.conj(h_equalizer[-2:0:-1])])

        # 시간 영역 변환
        impulse_response = np.real(ifft(h_full))

        # 윈도우 적용
        window = signal.windows.hann(len(impulse_response))
        impulse_response = impulse_response * window

        # 중앙 정렬
        center = len(impulse_response) // 2
        start = center - n_taps // 2
        equalizer = impulse_response[start:start + n_taps]

        return equalizer

    def apply_equalizer(
        self,
        signal_in: np.ndarray,
        equalizer: np.ndarray
    ) -> np.ndarray:
        """
        등화기 적용

        Args:
            signal_in: 입력 신호
            equalizer: 등화기 임펄스 응답

        Returns:
            등화된 신호
        """
        return np.convolve(signal_in, equalizer, mode='same')


class OpticalDispersionSimulator:
    """
    광섬유 색분산 시뮬레이터
    """

    C = 3e8  # 빛의 속도 (m/s)

    def __init__(self, dispersion_coeff: float = 17.0):
        """
        Args:
            dispersion_coeff: 색분산 계수 D [ps/(nm·km)]
                             SMF @ 1550nm: ~17 ps/(nm·km)
                             DCF: ~-100 ps/(nm·km)
        """
        self.D = dispersion_coeff * 1e-12  # s/(m·m) 단위 변환

    def calculate_pulse_broadening(
        self,
        fiber_length_km: float,
        spectral_width_nm: float,
        pulse_width_ps: float
    ) -> Tuple[float, float]:
        """
        펄스 확산 계산

        Args:
            fiber_length_km: 광섬유 길이 (km)
            spectral_width_nm: 광원 스펙트럼 폭 (nm)
            pulse_width_ps: 입력 펄스 폭 (ps)

        Returns:
            (확산된 펄스 폭 ps, 확산량 ps)
        """
        # 분산으로 인한 펄스 확산
        # Δτ = |D| × L × Δλ
        broadening_ps = abs(self.D * 1e12) * fiber_length_km * spectral_width_nm

        # 출력 펄스 폭 (제곱합의 제곱근)
        output_pulse_ps = np.sqrt(pulse_width_ps**2 + broadening_ps**2)

        return output_pulse_ps, broadening_ps

    def calculate_max_distance(
        self,
        bit_rate_gbps: float,
        spectral_width_nm: float = 0.1,
        max_broadening_fraction: float = 0.25
    ) -> float:
        """
        분산 제한 최대 전송 거리 계산

        펄스 확산이 비트 주기의 max_broadening_fraction 이하가 되도록

        Args:
            bit_rate_gbps: 비트 레이트 (Gbps)
            spectral_width_nm: 스펙트럼 폭 (nm)
            max_broadening_fraction: 최대 확산 비율

        Returns:
            최대 거리 (km)
        """
        bit_period_ps = 1000 / bit_rate_gbps  # ps
        max_broadening_ps = bit_period_ps * max_broadening_fraction

        # Δτ = D × L × Δλ → L = Δτ / (D × Δλ)
        max_distance_km = max_broadening_ps / (abs(self.D * 1e12) * spectral_width_nm)

        return max_distance_km

    def simulate_dispersion(
        self,
        signal: np.ndarray,
        fiber_length_km: float,
        wavelength_nm: float = 1550,
        sample_rate: float = 1e12
    ) -> np.ndarray:
        """
        분산 효과 시뮬레이션 (주파수 영역)

        Args:
            signal: 입력 신호
            fiber_length_km: 광섬유 길이 (km)
            wavelength_nm: 중심 파장 (nm)
            sample_rate: 샘플링 레이트 (Hz)

        Returns:
            분산된 신호
        """
        n = len(signal)
        freqs = fftfreq(n, 1/sample_rate)

        # 파장 → 주파수 변환
        center_freq = self.C / (wavelength_nm * 1e-9)

        # 주파수 오프셋
        delta_freq = freqs  # 단순화

        # 분산 위상 회전
        # φ(ω) = β₂ × L × ω² / 2
        # β₂ = -D × λ² / (2πc)
        beta2 = -self.D * (wavelength_nm * 1e-9)**2 / (2 * np.pi * self.C)

        phase_shift = beta2 * (fiber_length_km * 1000) * (2 * np.pi * delta_freq)**2 / 2

        # 주파수 영역 필터링
        signal_freq = fft(signal)
        dispersed_freq = signal_freq * np.exp(1j * phase_shift)

        dispersed_signal = np.real(ifft(dispersed_freq))

        return dispersed_signal


# 사용 예시
if __name__ == "__main__":
    # 지연 왜곡 분석
    analyzer = DelayDistortionAnalyzer(sample_rate=1e6)

    print("=" * 60)
    print("지연 왜곡 분석")
    print("=" * 60)

    # 비선형 위상 채널 생성
    channel = analyzer.generate_nonlinear_phase_channel(
        n_taps=101,
        cutoff_freq=0.3,
        group_delay_variation=5.0
    )

    # 채널 분석
    response = analyzer.analyze_channel(channel)

    # 군지연 계산
    group_delay = analyzer.calculate_group_delay(response.phase, response.frequencies)

    print(f"주파수 범위: {response.frequencies[0]/1e3:.1f} ~ {response.frequencies[-1]/1e3:.1f} kHz")
    print(f"군지연 범위: {np.min(group_delay)*1e6:.2f} ~ {np.max(group_delay)*1e6:.2f} μs")
    print(f"군지연 변동: {(np.max(group_delay) - np.min(group_delay))*1e6:.2f} μs")

    # 광섬유 분산 시뮬레이션
    print("\n" + "=" * 60)
    print("광섬유 색분산 분석")
    print("=" * 60)

    dispersion = OpticalDispersionSimulator(dispersion_coeff=17.0)

    # 10 Gbps, 80km 전송
    pulse_width, broadening = dispersion.calculate_pulse_broadening(
        fiber_length_km=80,
        spectral_width_nm=0.1,
        pulse_width_ps=100
    )

    print(f"입력 펄스 폭: 100 ps")
    print(f"80km 후 펄스 폭: {pulse_width:.1f} ps")
    print(f"펄스 확산량: {broadening:.1f} ps")

    # 최대 거리
    max_dist = dispersion.calculate_max_distance(
        bit_rate_gbps=10,
        spectral_width_nm=0.1
    )
    print(f"10 Gbps 최대 전송 거리 (분산 제한): {max_dist:.1f} km")

    print("\n=== 지연 왜곡 분석 완료 ===")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 광섬유 분산 유형 비교

| 분산 유형 | 원인 | 크기 | 보상 |
|----------|------|------|------|
| **색분산 (CD)** | 파장 의존 군지연 | 17 ps/(nm·km) | DCF, DSP |
| **모드 분산** | 모드 간 경로 차이 | 수 ns/km | SMF 사용 |
| **편광 모드 분산 (PMD)** | 편광 모드 간 차이 | 0.1~1 ps/√km | DSP |

### 과목 융합 관점 분석

1. **디지털 신호처리와의 융합**:
   - **FIR 이퀄라이저**: 군지연 왜곡을 선형 위상 FIR로 보상
   - **적응형 이퀄라이저**: LMS/RLS로 시변 채널 추적

2. **광통신과의 융합**:
   - **DSP 코히어런트 수신기**: 디지털 영역에서 CD/PMD 보상
   - **광 위상 배열**: 파장별 지연 제어

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 100G DP-QPSK 광전송 분산 보상

**문제 상황**: 100 Gbps DP-QPSK 신호를 1000km SMF로 전송합니다. 분산 보상 설계가 필요합니다.

**기술사의 전략적 의사결정**:

1. **분산 누적 계산**:
   ```
   D_total = 17 ps/(nm·km) × 1000 km = 17,000 ps/nm
         = 17 ns/nm

   변조 대역폭 ~32 GHz → Δλ ≈ 0.25 nm @ 1550nm
   펄스 확산 = 17 ns/nm × 0.25 nm = 4.25 ns
   ```

2. **보상 방안**:
   - **DCF (Dispersion Compensating Fiber)**: 매 80km마다 -1360 ps/nm DCF 삽입
   - **EDFA**: DCF 손실 보상
   - **DSP**: 잔여 분산 보상

3. **DSP 설계**:
   ```
   이퀄라이저 탭 수 ≥ 채널 메모리
   = D × L × Δf / T_symbol
   ≈ 17e-12 × 1000e3 × 32e9 / (1/32e9)
   ≈ 17 taps 안전하게 2× → 35 taps
   ```

---

## V. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 보상 없음 | DCF 보상 | DSP 보상 | 하이브리드 |
|----------|---------|---------|-----------|
| 수 km | 수백 km | 수천 km | 수천 km+ |
| 1 Gbps | 10 Gbps | 100+ Gbps | 400+ Gbps |

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **ITU-T G.655** | ITU-T | 비영분산 시프트 광섬유 |
| **ITU-T G.666** | ITU-T | 분산 보상 장치 |
| **IEEE 802.3** | IEEE | 이더넷 분산 사양 |

---

## 관련 개념 맵 (Knowledge Graph)
- [심볼 상호 간섭](./22_isi_inter_symbol_interference.md) - 지연 왜곡의 결과
- [이퀄라이저](./error_correction_codes.md) - 왜곡 보상 기술
- [광섬유 케이블](./multiplexing_techniques.md) - 분산 매체
- [OFDM](./multiplexing_fdm_tdm_wdm.md) - 주파수 분할로 왜곡 분산
- [위상 변조](./modulation_ask_fsk_psk_qam.md) - 위상 왜곡 영향

---

## 어린이를 위한 3줄 비유 설명
1. **지연 왜곡**은 **오케스트라에서 악기마다 소리가 다르게 늦게 도착하는 것**과 같아요.
2. **군지연**은 **모든 악기 소리의 '덩어리'가 얼마나 늦게 오는지**를 측정하는 거예요.
3. **등화기(Equalizer)**는 **소리를 다시 맞춰주는 지휘자**처럼 어긋난 타이밍을 바로잡아줘요!
