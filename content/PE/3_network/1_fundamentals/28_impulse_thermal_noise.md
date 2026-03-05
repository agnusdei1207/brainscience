+++
title = "028. 충격 잡음 / 열 잡음 (Impulse Noise / Thermal Noise)"
description = "통신 시스템에 영향을 미치는 충격 잡음과 열 잡음의 물리적 원리, 발생 메커니즘, 특성 차이 및 대응 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["ImpulseNoise", "ThermalNoise", "JohnsonNyquist", "EMI", "NoiseFigure", "LNA"]
categories = ["studynotes-3_network"]
+++

# 028. 충격 잡음 / 열 잡음 (Impulse Noise / Thermal Noise)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 열 잡음은 도체 내 전자의 무질서한 열 운동에서 발생하는 연속적이고 예측 불가능한 기저 잡음이며, 충격 잡음은 번개, 스위칭, 모터 등 외부 요인에 의해 발생하는 짧고 강력한 버스트형 잡음입니다.
> 2. **가치**: 열 잡음은 통신 시스템의 절대적인 성능 하한을 결정하며 수신기 감도 설계의 핵심이 되고, 충격 잡음은 버스트 오류를 유발하여 FEC/인터리빙 설계의 중요한 고려사항이 됩니다.
> 3. **융합**: IoT 센서 네트워크의 전자기 호환성(EMC) 설계, 스마트 그리드의 PLC 통신 잡음 대책, 자율주행 차량의 전자기 간섭 방지 등 다양한 분야에서 필수적인 잡음 제어 기술의 기반이 됩니다.

---

## Ⅰ. 개요 (Context & Background)

**열 잡음(Thermal Noise)**은 존슨 잡음(Johnson Noise)이라고도 하며, 모든 전도성 물질에서 전자의 열적 운동에 의해 발생하는 피할 수 없는 물리적 현상입니다. 1928년 J.B. Johnson이 발견하고 H. Nyquist가 이론적으로 설명했습니다.

**충격 잡음(Impulse Noise)**은 천둥/번개, 전기 스위치, 모터, 내연기관 점화 시스템, 전력선 등에서 발생하는 짧은 지속 시간(마이크로초~밀리초)과 높은 진폭을 가진 비정상적인 잡음입니다.

**💡 비유**:
- **열 잡음**은 **'조용한 방의 배경 소음'**입니다. 아무리 조용한 방이라도 완전히 무음일 수 없고, 공기 분자의 움직임, 건물의 미세 진동 등으로 인해 항상 작은 소음이 존재합니다.
- **충격 잡음**은 **'갑작스러운 문 닫는 소리'**입니다. 조용한 방에 누군가가 갑자기 문을 쾅 닫으면 순간적으로 큰 소리가 나고, 이 소리는 짧지만 다른 소리를 완전히 덮어버립니다.

**등장 배경 및 발전 과정**:
1. **열 잡음의 발견 (1928년)**: Bell Labs의 Johnson이 저항체에서 온도에 비례하는 잡음 전압을 측정했고, Nyquist가 열역학적 관점에서 이론식을 유도했습니다.
2. **충격 잡음의 인식 (1930~40년대)**: 라디오 방송 초기, 천둥번개와 자동차 점화 시스템이 방송 수신에 미치는 영향이 문제시되면서 연구가 시작되었습니다.
3. **현대적 대응**: 디지털 통신에서는 인터리빙(Interleaving), FEC, 스프레드 스펙트럼 등의 기술로 충격 잡음에 대응하고, 저잡음 증폭기(LNA), 냉각 시스템으로 열 잡음을 최소화합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석: 잡음 유형 비교

| 특성 | 열 잡음 (Thermal Noise) | 충격 잡음 (Impulse Noise) |
|------|------------------------|--------------------------|
| **발생 원인** | 전자의 열 운동 (브라운 운동) | 외부 전자기 교란 (번개, 스위칭 등) |
| **지속 시간** | 연속적 (항상 존재) | 순간적 (μs ~ ms) |
| **주파수 특성** | 백색 (평탄한 PSD) | 광대역 (스펙트럼 확산) |
| **진폭 분포** | 가우스 분포 | 비가우스 (장尾 분포, Heavy-tail) |
| **발생 주기** | 지속적 | 불규칙/간헐적 |
| **예측 가능성** | 통계적으로 예측 | 거의 불가능 |
| **대응 기법** | 저잡음 설계, 냉각 | 필터링, 인터리빙, FEC |

### 정교한 구조 다이어그램: 잡음 발생 메커니즘

```ascii
================================================================================
[ Thermal Noise: Microscopic Origin ]
================================================================================

    Conductor (Resistor R)
    +--------------------------------------------------+
    |  e⁻ →  ← e⁻   e⁻ →     ← e⁻  e⁻ →              |
    |     ↗  ↘       ↗    ↘       ↗    ↘             |
    |    e⁻    e⁻        e⁻      e⁻      e⁻          |
    |  ← e⁻  e⁻ →  ← e⁻    → e⁻  ← e⁻  e⁻ →          |
    |                                                  |
    |  Random thermal motion of electrons             |
    |  (Temperature dependent, T > 0K)                |
    +--------------------------------------------------+
                         |
                         v
        +-------------------------------+
        | Random Voltage Fluctuation    |
        |  v_n(t) with RMS: √(4kTRB)   |
        +-------------------------------+

================================================================================
[ Impulse Noise: Sources and Waveform ]
================================================================================

    External Sources                  Impulse Noise Waveform
    +------------------+             Amplitude
    | Lightning        |                  |
    +------------------+                  |  *
    | Switching Motions|                  | * *
    +------------------+                  |*   *
    | Ignition Systems |             -----*----*-------- Time
    +------------------+                  *   *
    | Power Line Spikes|                  *
    +------------------+                      (μs ~ ms)
    | Industrial EMI   |
    +------------------+

================================================================================
[ Time Domain Comparison ]
================================================================================

Thermal Noise (Continuous)
Amplitude
  |    ~~~~ ~~~~  ~~ ~~~  ~~
  |  ~~ ~~~~~ ~~~ ~ ~~~ ~ ~~
  | ~~~ ~~~ ~~~~ ~ ~~~~~ ~~  <- Constant low-level fluctuation
  |~ ~~~~~ ~~~ ~~~~ ~~ ~~~~
  +-------------------------------------------> Time

Impulse Noise (Sporadic)
Amplitude
  |
  |              *                   *
  |             * *                 * *
  |    *       *   *       *       *   *
  |   * *     *     *     * *     *     *
  |--*---*---*-------*---*---*---*-------*---*-> Time
  |         *             *
  |   (Bursts with high amplitude)
```

### 심층 동작 원리

**1. 열 잡음의 물리적 메커니즘**:
```
존슨-나이퀴스트 공식:
        Vn² = 4kTRB

        Vn = √(4kTRB)  [Volt RMS]

여기서:
        k = 볼츠만 상수 = 1.38 × 10⁻²³ J/K
        T = 절대 온도 [Kelvin]
        R = 저항 [Ohm]
        B = 대역폭 [Hz]

노이즈 전력 밀도:
        N₀ = kT  [Watts/Hz]
        N₀(dBm/Hz) = -174 + 10log₁₀(T/290)

실온(290K)에서:
        N₀ = 4.00 × 10⁻²¹ W/Hz
        N₀ = -174 dBm/Hz (노이즈 플로어)
```

**2. 충격 잡음의 발생 메커니즘**:
- **번개(Lightning)**: 대기 중 방전으로 인한 광대역 전자기 펄스 (수 ms)
- **스위칭(Switching)**: 릴레이, 접점의 아크 방전 (수 μs ~ 수 ms)
- **모터(Motor)**: 브러시 접촉 불량, 역기전력 (수 ms, 주기적)
- **전력선(Power Line)**: 부하 급변, 차단기 동작 (수 ms ~ 수 s)
- **산업 설비**: 용접기, 고주파 가열기 (연속/간헐적)

**3. 충격 잡음의 특성 모델**:
- **중간 급증(Middleton) Class A/B 모델**: 임펄스 잡음의 통계적 모델
- **Gilbert-Elliot 모델**: 상태 천이 모델 (Good/Bad 상태)
- **Poisson 도달 모델**: 임펄스 발생 시간이 포아송 과정을 따름

### 핵심 코드: 열 잡음 및 충격 잡음 시뮬레이션

```python
"""
열 잡음 및 충격 잡음 시뮬레이션
통신 시스템에서 두 잡음이 신호에 미치는 영향 비교
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple

@dataclass
class NoiseParameters:
    """잡음 파라미터 클래스"""
    temperature: float = 290.0      # Kelvin (실온)
    resistance: float = 50.0        # Ohm
    bandwidth: float = 1e6          # Hz (1 MHz)
    impulse_rate: float = 100       # impulses/second
    impulse_amplitude: float = 0.5  # Volts (peak)
    impulse_duration: float = 1e-6  # seconds (1 μs)


class ThermalNoiseGenerator:
    """
    열 잡음 생성기
    존슨-나이퀴스트 공식에 기반한 가우시안 백색 잡음 생성
    """
    def __init__(self, params: NoiseParameters):
        self.params = params
        self.k_boltzmann = 1.380649e-23

    def calculate_noise_voltage_rms(self) -> float:
        """열 잡음 RMS 전압 계산"""
        v_rms = np.sqrt(4 * self.k_boltzmann *
                       self.params.temperature *
                       self.params.resistance *
                       self.params.bandwidth)
        return v_rms

    def calculate_noise_power_dbm(self) -> float:
        """열 잡음 전력 (dBm) 계산"""
        # P = V²/R, dBm = 10*log10(P/1mW)
        v_rms = self.calculate_noise_voltage_rms()
        power_watts = (v_rms ** 2) / self.params.resistance
        power_dbm = 10 * np.log10(power_watts / 0.001)
        return power_dbm

    def generate(self, num_samples: int) -> np.ndarray:
        """열 잡음 샘플 생성"""
        v_rms = self.calculate_noise_voltage_rms()
        noise = np.random.normal(0, v_rms, num_samples)
        return noise


class ImpulseNoiseGenerator:
    """
    충격 잡음 생성기
    Poisson 과정에 기반한 임펄스 잡음 생성
    """
    def __init__(self, params: NoiseParameters, sample_rate: float):
        self.params = params
        self.sample_rate = sample_rate

    def generate(self, duration: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        충격 잡음 생성

        Returns:
            noise: 잡음 신호
            impulse_indices: 임펄스 발생 위치
        """
        num_samples = int(duration * self.sample_rate)
        noise = np.zeros(num_samples)

        # Poisson 과정으로 임펄스 발생 시간 결정
        expected_impulses = self.params.impulse_rate * duration
        num_impulses = np.random.poisson(expected_impulses)

        # 균일 분포로 발생 시간 결정
        impulse_times = np.random.uniform(0, duration, num_impulses)
        impulse_indices = (impulse_times * self.sample_rate).astype(int)

        # 유효한 인덱스만 선택
        impulse_indices = impulse_indices[impulse_indices < num_samples]

        # 각 임펄스의 지속 시간 (샘플 수)
        impulse_width = int(self.params.impulse_duration * self.sample_rate)

        # 임펄스 생성 (지수 감쇠 형태)
        for idx in impulse_indices:
            # 임펄스 모양: 급격히 상승 후 지수 감쇠
            end_idx = min(idx + impulse_width, num_samples)
            t = np.arange(end_idx - idx)

            # 감쇠 상수
            decay_tau = impulse_width / 5

            # 임펄스 파형: 지수 감쇠
            amplitude = self.params.impulse_amplitude * np.random.choice([-1, 1])
            impulse_shape = amplitude * np.exp(-t / decay_tau)

            noise[idx:end_idx] += impulse_shape

        return noise, impulse_indices


def plot_noise_comparison():
    """
    열 잡음과 충격 잡음의 비교 시각화
    """
    # 파라미터 설정
    params = NoiseParameters(
        temperature=290,
        resistance=50,
        bandwidth=1e6,
        impulse_rate=50,
        impulse_amplitude=0.01,
        impulse_duration=1e-5
    )

    sample_rate = 1e6  # 1 MHz
    duration = 0.01   # 10 ms
    num_samples = int(duration * sample_rate)
    time = np.linspace(0, duration, num_samples)

    # 잡음 생성
    thermal_gen = ThermalNoiseGenerator(params)
    impulse_gen = ImpulseNoiseGenerator(params, sample_rate)

    thermal_noise = thermal_gen.generate(num_samples)
    impulse_noise, impulse_idx = impulse_gen.generate(duration)

    # 결합된 잡음
    combined_noise = thermal_noise + impulse_noise

    # 계산된 값 출력
    print(f"열 잡음 RMS 전압: {thermal_gen.calculate_noise_voltage_rms()*1e6:.2f} μV")
    print(f"열 잡음 전력: {thermal_gen.calculate_noise_power_dbm():.2f} dBm")
    print(f"생성된 임펄스 수: {len(impulse_idx)}")

    # 그래프 그리기
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

    # 열 잡음
    axes[0].plot(time * 1000, thermal_noise * 1e6, 'b-', linewidth=0.5)
    axes[0].set_ylabel('Thermal Noise (μV)')
    axes[0].set_title('Thermal Noise (Gaussian, Continuous)')
    axes[0].grid(True, alpha=0.3)

    # 충격 잡음
    axes[1].plot(time * 1000, impulse_noise * 1e3, 'r-', linewidth=0.5)
    axes[1].set_ylabel('Impulse Noise (mV)')
    axes[1].set_title('Impulse Noise (Sporadic, High Amplitude)')
    axes[1].grid(True, alpha=0.3)

    # 결합된 잡음
    axes[2].plot(time * 1000, combined_noise * 1e3, 'g-', linewidth=0.5)
    axes[2].set_ylabel('Combined Noise (mV)')
    axes[2].set_title('Combined Thermal + Impulse Noise')
    axes[2].grid(True, alpha=0.3)

    # 신호 + 잡음 (예시)
    signal_freq = 10000  # 10 kHz
    signal = 0.01 * np.sin(2 * np.pi * signal_freq * time)
    signal_plus_noise = signal + combined_noise

    axes[3].plot(time * 1000, signal_plus_noise * 1e3, 'purple', linewidth=0.5)
    axes[3].set_ylabel('Signal+Noise (mV)')
    axes[3].set_xlabel('Time (ms)')
    axes[3].set_title('Signal Corrupted by Thermal + Impulse Noise')
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('noise_comparison.png', dpi=150)
    plt.show()


def calculate_effect_on_ber():
    """
    잡음이 BER에 미치는 영향 분석
    """
    print("\n=== 잡음이 BER에 미치는 영향 ===")

    # SNR 범위
    snr_db_range = np.arange(0, 15, 1)

    # 열 잡음만 있는 경우의 BER (BPSK)
    from scipy.special import erfc

    print("\nSNR(dB) | Thermal Only | With Impulse (10%)")
    print("-" * 45)

    for snr_db in snr_db_range:
        # 이론적 BER (열 잡음만)
        snr_lin = 10 ** (snr_db / 10)
        ber_thermal = 0.5 * erfc(np.sqrt(snr_lin))

        # 임펄스 잡음 추가 (10% 확률로 완전 오류)
        impulse_error_rate = 0.10
        ber_combined = (1 - impulse_error_rate) * ber_thermal + impulse_error_rate * 0.5

        print(f"  {snr_db:2d}    |  {ber_thermal:.2e}  |  {ber_combined:.2e}")


if __name__ == "__main__":
    # 잡음 시각화
    plot_noise_comparison()

    # BER 영향 분석
    calculate_effect_on_ber()

    # 실온 노이즈 플로어 계산 예시
    print("\n=== 실온 노이즈 플로어 ===")
    k = 1.380649e-23
    T = 290  # 실온
    for bw_name, bw in [("1 Hz", 1), ("1 kHz", 1e3), ("1 MHz", 1e6), ("10 MHz", 10e6)]:
        noise_power_w = k * T * bw
        noise_power_dbm = 10 * np.log10(noise_power_w / 0.001)
        print(f"{bw_name}: {noise_power_dbm:.2f} dBm")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 잡음 완화 기법

| 기법 | 열 잡음 대응 | 충격 잡음 대응 | 원리 | 적용 예시 |
|------|------------|--------------|------|----------|
| **냉각** | 매우 효과적 | 무효 | T↓ → P_n ↓ | 위성 IR 센서 |
| **LNA** | 효과적 | 무효 | NF 최소화 | 모든 수신기 |
| **대역 제한 필터** | 효과적 | 부분 효과 | B↓ → P_n ↓ | IF 필터 |
| **리미터** | 무효 | 효과적 | 진폭 제한 | FM 수신기 |
| **블랭킹** | 무효 | 효과적 | 임펄스 구간 제거 | 디지털 수신기 |
| **인터리빙** | 무효 | 매우 효과적 | 버스트 분산 | DVB, LTE |
| **FEC** | 효과적 | 매우 효과적 | 오류 정정 | 모든 디지털 통신 |
| **스프레드 스펙트럼** | 효과적 | 효과적 | 처리 이득 | GPS, CDMA |

### 과목 융합 관점 분석

**1. 전자기학과의 융합**:
   - 충격 잡음의 원인인 번개, 스위칭은 전자기 유도 법칙으로 설명됩니다.
   - 패러데이 케이지, 케이블 차폐 등 EMC 설계가 충격 잡음 방지의 핵심입니다.
   - 케이블의 차폐 효과(Shielding Effectiveness)는 dB로 표현됩니다.

**2. 확률/통계와의 융합**:
   - 열 잡음의 진폭 분포는 정규 분포(N(0, σ²))를 따릅니다.
   - 충격 잡음의 발생은 포아송 과정으로 모델링됩니다.
   - 임펄스 간격은 지수 분포를 따릅니다.

**3. 반도체 물리와의 융합**:
   - FET의 열 잡음은 채널 저항에서 발생합니다.
   - 저잡음 증폭기(LNA)는 낮은 등가 잡음 저항을 가진 트랜지스터를 사용합니다.
   - GaAs, InP 등의 화합물 반도체가 낮은 잡음 특성을 제공합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: PLC(Power Line Communication) 시스템 설계

**문제 상황**: 스마트 그리드용 PLC 통신 시스템을 설계해야 합니다. 전력선은 충격 잡음이 매우 심한 환경입니다.

**기술사의 전략적 의사결정**:

1. **잡음 환경 분석**:
   - 전력선 충격 잡음 특성: 주파수 1kHz~10MHz, 지속시간 10μs~100ms
   - 주요 발생원: 스위칭 전원, 인버터, 모터 구동

2. **물리 계층 설계**:
   - OFDM 변조 채택: 2~30MHz 대역, 다수의 부반송파로 충격 잡음 분산
   - 인터리빙 깊이: 10ms 이상으로 충격 잡음 분산 효과 극대화
   - FEC: LDPC 코드 (부호율 1/2~3/4)로 버스트 오류 정정

3. **MAC 계층 설계**:
   - CSMA/CA + ACK: 충격 잡음으로 인한 패킷 손실 시 재전송
   - 적응형 전력 제어: 잡음 레벨에 따른 송신 전력 조절

### 도입 시 고려사항 체크리스트

| 항목 | 확인 내용 | 중요도 |
|------|----------|--------|
| **잡음 측정** | 실제 환경에서 열 잡음/충격 잡음 레벨 측정 | 상 |
| **EMC 규정** | 충격 잡음 발생 장비의 EMC 규정 준수 여부 | 상 |
| **필터 설계** | 대역통과 필터, 노치 필터 설계 적절성 | 중 |
| **접지 설계** | 적절한 접지로 외부 잡음 유입 방지 | 상 |
| **차폐 효과** | 케이블, 커넥터의 차폐 성능 확인 | 중 |

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - 열 잡음만 고려한 설계**:
  AWGN만 가정하고 충격 잡음을 무시하면 실제 환경에서 BER이 급격히 악화됩니다. 특히 산업 환경, PLC, 차량 통신에서 치명적입니다.

- **안티패턴 2 - 과도한 냉각**:
  수신기 감도 향상을 위해 냉각 비용을 과도하게 투입하는 실수. 시스템 전체 잡음은 LNA, 믹서 등 여러 단의 기여도를 합산해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | 내용 | 정량적 지표 |
|----------|------|------------|
| **수신 감도 향상** | 열 잡음 최소화로 약한 신호 수신 | 감도 3~10 dB 개선 |
| **BER 개선** | 충격 잡음 대응으로 버스트 오류 감소 | BER 10배 개선 |
| **통신 신뢰성** | 잡음 내성 설계로 링크 안정화 | 가용성 99.9% 달성 |
| **비용 절감** | 과설계 방지 및 최적 부품 선정 | RF 부품 비용 15% 절감 |

### 미래 전망 및 진화 방향

- **AI 기반 잡음 분류**: 머신러닝으로 열 잡음/충격 잡음/간섭을 실시간 구분하여 적응적 대응

- **양자 한계 돌파**: 초전도 양자 증폭기로 열 잡음 한계를 돌파하는 극저잡음 수신기

- **인지 무선(Cognitive Radio)**: 잡음 환경을 실시간 감지하여 주파수, 변조 방식을 자동 전환

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **ITU-T G.9960** | ITU-T | G.hn PLC 표준 (잡음 대응 포함) |
| **IEEE 1901** | IEEE | Power Line Communication 표준 |
| **CISPR 16** | IEC | 무선 장해 측정 방법 |
| **MIL-STD-461** | DoD | 전자기 간섭 제어 요구사항 |

---

## 관련 개념 맵 (Knowledge Graph)
- [백색 잡음/가우스 잡음](./27_white_noise_gaussian.md) - 열 잡음의 통계적 특성
- [신호 대 잡음비](./24_snr_signal_to_noise_ratio.md) - SNR과 잡음의 관계
- [오류 정정 코드](./error_correction_codes.md) - 잡음 대응을 위한 FEC
- [전송 매체](../3_media_physical/) - 케이블 차폐와 잡음 유입
- [대역폭 및 효율성](./13_bandwidth_efficiency.md) - 대역폭과 잡음 전력의 관계

---

## 어린이를 위한 3줄 비유 설명
1. **열 잡음**은 **'항상 들리는 작은 소음'**이에요. 아무리 조용한 방이라도 완전 무음이 아니듯, 전자 기기에도 항상 작은 잡음이 있어요.
2. **충격 잡음**은 **'갑자기 울리는 큰 소리'**예요. 천둥소리나 문을 쾅 닫는 소리처럼, 짧지만 아주 큰 잡음이 갑자기 터져요!
3. **대응 방법**은 **'귀를 막거나 다시 듣기'**예요. 열 잡음은 더 좋은 이어폰으로, 충격 잡음은 큰 소리가 날 때 잠시 멈췄다가 다시 듣는 것으로 해결해요!
