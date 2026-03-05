+++
title = "027. 백색 잡음 / 가우스 잡음 (White Noise / Gaussian Noise)"
description = "통신 시스템의 근본적인 열잡음인 백색 가우스 잡음(AWGN)의 물리적 원리, 통계적 특성, 통신 성능에 미치는 영향을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["WhiteNoise", "GaussianNoise", "AWGN", "ThermalNoise", "SNR", "CommunicationTheory", "Shannon"]
categories = ["studynotes-3_network"]
+++

# 027. 백색 잡음 / 가우스 잡음 (White Noise / Gaussian Noise)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 백색 잡음은 모든 주파수 대역에서 균일한 파워 스펙트럼 밀도를 가지는 이상적인 잡음 모델로, 열잡음(Thermal Noise)이 그 대표적 예시이며 가우스 분포를 따르는 확률 변수로 모델링됩니다.
> 2. **가치**: AWGN(Additive White Gaussian Noise) 채널 모델은 통신 시스템 성능 분석의 기준점을 제공하며, 샤논 채널 용량 정리의 핵심 전제가 되어 통신 이론의 수학적 기반을 확립합니다.
> 3. **융합**: 5G/6G 통신의 MMSE 등화기, AI 기반 채널 추정, 양자 통신의 shot noise 분석 등 현대 통신 기술의 잡음 처리 알고리즘 설계에 필수적인 이론적 토대입니다.

---

## Ⅰ. 개요 (Context & Background)

**백색 잡음(White Noise)**은 가시광선의 백색광이 모든 파장을 포함하듯이, 모든 주파수 성분을 동일한 크기로 포함하는 잡음을 의미합니다. 수학적으로는 파워 스펙트럼 밀도(Power Spectral Density, PSD)가 주파수에 무관하게 일정한 상수인 신호로 정의됩니다. **가우스 잡음(Gaussian Noise)**은 순간적인 진폭이 정규 분포(가우스 분포)를 따르는 통계적 특성을 가진 잡음입니다.

통신 이론에서 이 두 가지 특성을 결합한 **AWGN(Additive White Gaussian Noise)** 모델은 가장 기본적이고 널리 사용되는 채널 모델입니다.

**💡 비유**: 백색 잡음은 **'비 오는 소리'**와 같습니다.
- 비가 내릴 때 수많은 빗방울이 각기 다른 크기와 속도로 떨어지며 내는 소리가 합쳐져서 '쉬익-'하는 균일한 소리가 됩니다.
- 각 빗방울의 소리는 예측 불가능하지만(가우스 분포), 전체적으로는 모든 주파수 성분이 고르게 섞여 있습니다(백색 특성).
- 이 소리가 우리가 듣고자 하는 음악(신호) 위에 겹쳐져서 음질을 저하시키는 것과 같습니다.

**등장 배경 및 발전 과정**:
1. **물리적 발견 (1900년대 초)**: 존슨(Johnson)과 나이퀴스트(Nyquist)가 도체 내 전자의 무질서한 열 운동에서 발생하는 열잡음(Thermal Noise)을 발견하고, 그 크기가 절대 온도에 비례함을 수식화했습니다.
2. **통신 이론의 정립 (1948년)**: 클로드 샤논(Claude Shannon)이 "A Mathematical Theory of Communication" 논문에서 AWGN 채널 모델을 도입하여 채널 용량 공식을 유도했습니다. 이는 디지털 통신의 이론적 한계를 제시한里程碑였습니다.
3. **현대적 확장**: 오늘날 AWGN 모델은 기본 성능 분석의 출발점이며, 실제 환경의 페이딩, 간섭 등을 추가한 복잡한 채널 모델의 기저에 깔려 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석: 잡음의 분류 체계

| 잡음 유형 | 원인 | 주파수 특성 | 분포 특성 | 대응 기법 |
|----------|------|------------|----------|----------|
| **백색 잡음 (White Noise)** | 열잡음, 샷 잡음 | 평탄한 PSD (모든 주파수) | 보통 가우스 | 대역폭 제한, 필터링 |
| **열잡음 (Thermal Noise)** | 전자의 열 운동 | 백색 (온도 의존) | 가우스 | 냉각, 저잡음 증폭기(LNA) |
| **샷 잡음 (Shot Noise)** | 전하의 이산적 이동 | 백색 (전류 의존) | 포아송/가우스 | 전류 레벨 최적화 |
| **핑크 잡음 (1/f Noise)** | 반도체 결함 등 | PSD ∝ 1/f | 비가우스 | 차단 주파수 회피 |
| **충격 잡음 (Impulse)** | 번개, 스위칭 | 광대역, 순간적 | 비정상적 | 리미터, 클리퍼 |

### 정교한 구조 다이어그램: AWGN 채널 모델

```ascii
================================================================================
[ Additive White Gaussian Noise (AWGN) Channel Model ]
================================================================================

                        +---------------------------------+
                        |      AWGN Channel Model         |
                        +---------------------------------+
                                   |
     +--------+      +--------+    v    +--------+      +--------+
     |  Tx    |      |        |   n(t)   |        |      |  Rx    |
     | Source |----->|  s(t)  |-------> (+) ----->|  r(t)  |----->| Detector|
     +--------+      +--------+          ^       +--------+      +--------+
                                       |
                                       |  n(t) ~ N(0, σ²)
                                       |
                        +---------------------------------+
                        |  White Gaussian Noise Source    |
                        |                                 |
                        |  PSD: N₀/2 (Watts/Hz)          |
                        |  PDF: p(n) = (1/√(2πσ²))e^(-n²/2σ²)  |
                        +---------------------------------+

================================================================================
[ Power Spectral Density Comparison ]
================================================================================

Power
Spectral
Density
(S(f))
  |
N₀/2 |=========================================  <- White Noise (Flat PSD)
     |
     |        /\
     |       /  \
     |      /    \                              <- Colored Noise
     |_____/      \_____
     |                  \
     |                   \____
     +-----------------------------------------> Frequency (f)
     0      f₁       f₂       f₃       f₄

================================================================================
[ Gaussian Probability Density Function ]
================================================================================

Probability
Density
p(n)
  |                    *
  |                  *   *
  |                *       *
  |              *           *
  |            *               *
  |          *                   *
  |        *                       *
  |      *                           *
  |    *                               *
  |  *                                   *
  |*_______________________________________*_____ Amplitude (n)
    -3σ   -2σ   -σ    0    +σ   +2σ   +3σ

    |← 68.27% →|← 95.45% →|← 99.73% →|

================================================================================
[ Time Domain Representation ]
================================================================================

Amplitude
  |      Signal + Noise
  |    ╱╲  ╱╲    ╱╲
  |   ╱  ╲╱  ╲  ╱  ╲    ← Corrupted signal
  |  ╱        ╲╱    ╲
  |───────────────────────────────────── Time (t)
  |      ╲  ╱╲  ╱╲    ╱
  |       ╲╱  ╲╱  ╲  ╱
  |              ╲╱

  Clean Signal (Smooth) + White Noise (Jagged) = Corrupted Signal
```

### 심층 동작 원리: 열잡음의 물리적 기원

**1. 열잡음의 물리적 메커니즘**:
   - 도체 내 자유 전자는 절대 온도 0K이상에서 무작위 열 운동을 합니다.
   - 이 운동은 전압/전류의 무작위한 요동(Fluctuation)을 유발합니다.
   - 존슨-나이퀴스트 공식: `Vn² = 4kTRB`
     - `k` = 볼츠만 상수 (1.38 × 10⁻²³ J/K)
     - `T` = 절대 온도 (Kelvin)
     - `R` = 저항 (Ohms)
     - `B` = 대역폭 (Hz)

**2. 백색 특성의 유래**:
   - 열잡음의 상관 시간(Correlation Time)은 전자 충돌 주기인 10⁻¹⁴초 수준으로 매우 짧습니다.
   - 이는 실질적으로 수 GHz까지 평탄한 주파수 스펙트럼을 의미합니다.
   - "백색"이라는 명칭은 백색광처럼 모든 주파수 성분이 균등하다는 의미입니다.

**3. 가우스 분포의 유래 (중심 극한 정리)**:
   - 열잡음은 수십억 개의 전자 충돌의 합입니다.
   - 중심 극한 정리(Central Limit Theorem)에 의해 독립적인 무작위 변수의 합은 가우스 분포를 따릅니다.
   - 따라서 순간 잡음 전압은 정규 분포 N(0, σ²)를 따릅니다.

### 핵심 수식 및 코드: SNR과 BER 분석

```python
"""
AWGN 채널 시뮬레이션 및 BER(비트 오류율) 분석
BPSK 변조에서 SNR에 따른 BER 성능 확인
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

class AWGNChannel:
    """
    AWGN 채널 모델 시뮬레이션 클래스
    """
    def __init__(self, snr_db: float):
        """
        Args:
            snr_db: 신호 대 잡음비 (dB)
        """
        self.snr_db = snr_db
        self.snr_linear = 10 ** (snr_db / 10)

    def add_noise(self, signal: np.ndarray) -> np.ndarray:
        """
        신호에 AWGN 잡음을 더함

        Args:
            signal: 송신 신호 (정규화된 에너지)

        Returns:
            잡음이 더해진 수신 신호
        """
        # 신호 전력 계산
        signal_power = np.mean(np.abs(signal) ** 2)

        # 잡음 전력 계산 (SNR = Signal Power / Noise Power)
        noise_power = signal_power / self.snr_linear
        noise_std = np.sqrt(noise_power)

        # 가우스 잡음 생성 (평균 0, 표준편차 noise_std)
        noise = np.random.normal(0, noise_std, signal.shape)

        return signal + noise


class BPSKModulator:
    """
    BPSK (Binary Phase Shift Keying) 변조/복조
    """
    @staticmethod
    def modulate(bits: np.ndarray) -> np.ndarray:
        """비트를 BPSK 심볼로 변환: 0 -> +1, 1 -> -1"""
        return 1 - 2 * bits  # 0->+1, 1->-1

    @staticmethod
    def demodulate(symbols: np.ndarray) -> np.ndarray:
        """BPSK 심볼을 비트로 변환: 양수->0, 음수->1"""
        return (symbols < 0).astype(int)


def simulate_bpsk_ber(snr_db: float, num_bits: int = 1_000_000) -> float:
    """
    BPSK 변조 시스템의 BER 시뮬레이션

    Args:
        snr_db: SNR (dB)
        num_bits: 시뮬레이션할 비트 수

    Returns:
        비트 오류율 (BER)
    """
    # 랜덤 비트 생성
    tx_bits = np.random.randint(0, 2, num_bits)

    # BPSK 변조
    tx_symbols = BPSKModulator.modmodate(tx_bits)

    # AWGN 채널 통과
    channel = AWGNChannel(snr_db)
    rx_symbols = channel.add_noise(tx_symbols)

    # BPSK 복조
    rx_bits = BPSKModulator.demodulate(rx_symbols)

    # BER 계산
    ber = np.mean(tx_bits != rx_bits)

    return ber


def theoretical_bpsk_ber(snr_db: float) -> float:
    """
    BPSK의 이론적 BER (AWGN 채널)
    BER = Q(√(2 * Eb/N₀)) = 0.5 * erfc(√(Eb/N₀))

    Args:
        snr_db: SNR (dB) = Eb/N₀ (dB)

    Returns:
        이론적 비트 오류율
    """
    snr_linear = 10 ** (snr_db / 10)
    # Q(x) = 0.5 * erfc(x/√2)
    # BER = Q(√(2*SNR))
    ber = 0.5 * erfc(np.sqrt(snr_linear))
    return ber


def plot_ber_vs_snr():
    """
    SNR 대 BER 곡선 그리기 (이론값 vs 시뮬레이션)
    """
    snr_range_db = np.arange(0, 13, 1)
    theoretical_bers = []
    simulated_bers = []

    for snr_db in snr_range_db:
        theoretical_bers.append(theoretical_bpsk_ber(snr_db))
        # 시뮬레이션 (비트 수는 BER 레벨에 따라 조정)
        num_bits = max(100_000, int(100 / theoretical_bpsk_ber(snr_db)))
        sim_ber = simulate_bpsk_ber(snr_db, num_bits)
        simulated_bers.append(sim_ber)
        print(f"SNR = {snr_db} dB: 이론 BER = {theoretical_bers[-1]:.2e}, 시뮬 BER = {sim_ber:.2e}")

    plt.figure(figsize=(10, 6))
    plt.semilogy(snr_range_db, theoretical_bers, 'b-', linewidth=2, label='Theoretical')
    plt.semilogy(snr_range_db, simulated_bers, 'ro', markersize=8, label='Simulated')
    plt.grid(True, which='both', linestyle='--')
    plt.xlabel('SNR (Eb/N₀) [dB]')
    plt.ylabel('Bit Error Rate (BER)')
    plt.title('BPSK BER Performance in AWGN Channel')
    plt.legend()
    plt.tight_layout()
    plt.savefig('bpsk_ber_awgn.png', dpi=150)
    plt.show()


def calculate_thermal_noise_voltage(resistance: float, temperature: float, bandwidth: float) -> float:
    """
    존슨-나이퀴스트 열잡음 전압 RMS 계산

    Args:
        resistance: 저항 (Ohm)
        temperature: 온도 (Kelvin)
        bandwidth: 대역폭 (Hz)

    Returns:
        열잡음 전압 RMS (Volt)
    """
    k_boltzmann = 1.380649e-23  # 볼츠만 상수 (J/K)
    v_n_squared = 4 * k_boltzmann * temperature * resistance * bandwidth
    return np.sqrt(v_n_squared)


# 실무 예시: 50옴 안테나 시스템의 열잡음 계산
if __name__ == "__main__":
    # 예시 1: 50Ω 안테나, 실온(290K), 1MHz 대역폭
    R = 50  # Ohm
    T = 290  # Kelvin (약 17°C)
    B = 1e6  # 1 MHz

    noise_voltage = calculate_thermal_noise_voltage(R, T, B)
    noise_power = (noise_voltage ** 2) / R
    noise_power_dbm = 10 * np.log10(noise_power / 0.001)

    print(f"열잡음 전압 RMS: {noise_voltage * 1e6:.2f} μV")
    print(f"열잡음 전력: {noise_power * 1e12:.2f} pW")
    print(f"열잡음 전력: {noise_power_dbm:.2f} dBm")
    print(f"노이즈 플로어 (N₀): {10*np.log10(k_boltzmann*T*1000):.2f} dBm/Hz")

    # 예시 2: SNR 요구사항 계산
    # 수신기 감도 = 열잡음 + SNR_req + NF
    required_snr_db = 10  # BPSK에서 BER 10⁻³ 달성에 필요
    noise_figure_db = 3   # 전형적인 수신기 노이즈 피겨
    sensitivity_dbm = noise_power_dbm + required_snr_db + noise_figure_db

    print(f"\n수신기 감도: {sensitivity_dbm:.2f} dBm")
    print(f"수신기 감도: {sensitivity_dbm - 30:.2f} dBW")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 잡음 유형별 특성

| 잡음 유형 | 수학적 모델 | PSD | PDF | 주요 발생원 | 통신 영향 |
|----------|------------|-----|-----|-----------|----------|
| **백색 가우스 (AWGN)** | n(t) ~ N(0, σ²) | N₀/2 (상수) | 정규 분포 | 열잡음, 우주 배경 | SNR 저하, BER 증가 |
| **핑크 잡음 (1/f)** | PSD ∝ 1/f | 1/f | 비대칭 | 반도체 결함 | 저주파 왜곡 |
| **브라운 잡음 (1/f²)** | PSD ∝ 1/f² | 1/f² | 가우스 (적분 후) | 무작위 워크 | 저주파 집중 |
| **충격 잡음** | δ 함수 합 | 광대역 | 지수/비정상 | 번개, 스위칭 | 버스트 오류 |
| **양자 잡음 (Shot)** | 포아송 과정 | N₀/2 | 포아송→가우스 | 전류 이산성 | 고주파수 한계 |

### 통신 시스템 설계 관점 비교

| 설계 관점 | AWGN 채널 고려사항 | 설계 해결책 |
|----------|-------------------|------------|
| **변조 방식** | SNR 대역폭 트레이드오프 | 적응형 변조 (AMC) |
| **채널 코딩** | 임의 오류 발생 | FEC (Turbo, LDPC) |
| **대역폭** | 노이즈 전력 ∝ B | 대역폭 효율적 변조 |
| **송신 전력** | SNR ∝ P | 전력 제어, EIRP 제한 |
| **수신기** | 노이즈 피겨(NF) | LNA, 저잡음 설계 |

### 과목 융합 관점 분석

**1. 확률/통계와의 융합**:
   - AWGN은 확률 변수(	Random Variable)의 대표적 응용입니다.
   - BER 분석은 Q-함수, erfc 함수, Chernoff Bound 등의 확률 이론을 활용합니다.
   - 잡음의 상관 함수(Correlation Function)와 PSD는 Wiener-Khinchin 정리로 연결됩니다.

**2. 신호 처리와의 융합**:
   - 매치 필터(Matched Filter)는 AWGN 하에서 최대 SNR을 제공합니다.
   - Welch's method, Periodogram 등으로 실제 PSD를 추정합니다.
   - 적응 필터(LMS, RLS)가 잡음을 추정하여 제거합니다.

**3. 물리학과의 융합**:
   - 열잡음은 통계 역학(Statistical Mechanics)의 에너지 등분배 법칙과 연결됩니다.
   - 양자 역학적 shot noise는 전하의 이산성(Discreteness)에서 기인합니다.
   - 초전도 회로에서 열잡음이 사라지는 현상을 활용합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 위성 통신 링크 예산 설계

**문제 상황**: 정지 궤도(GEO) 위성 통신 시스템에서 지구국 수신기의 노이즈 플로어를 계산하고, 요구 SNR을 만족하기 위한 링크 예산을 수립해야 합니다.

**기술사의 전략적 의사결정**:

1. **노이즈 플로어 계산**:
   - 안테나 온도 T_ant = 20K (우주 공간)
   - 수신기 온도 T_rx = 100K
   - 시스템 온도 T_sys = T_ant + T_rx = 120K
   - 노이즈 전력 밀도 N₀ = kT_sys = 1.38×10⁻²³ × 120 = 1.66×10⁻²¹ W/Hz
   - 노이즈 플로어 (@ 36MHz BW) = N₀ × B = -125 dBm

2. **링크 마진 확보**:
   - 필요 CNR (Carrier-to-Noise Ratio) = 15 dB (QPSK, FEC 1/2)
   - 구현 마진 = 3 dB
   - 강우 감쇠 마진 = 5 dB
   - 총 필요 마진 = 23 dB

3. **설계 결정**:
   - LNA(저잡음 증폭기)를 안테나 근처에 배치하여 케이블 손실로 인한 SNR 열화 방지
   - 대역폭 36MHz로 제한하여 노이즈 전력 최소화

### 도입 시 고려사항 체크리스트

| 항목 | 확인 내용 | 중요도 |
|------|----------|--------|
| **시스템 온도** | 안테나, LNA, 믹서 등 전체 잡음 온도 합산 | 상 |
| **대역폭 제한** | 필터링으로 노이즈 전력 제한 | 상 |
| **동적 범위** | ADC 양자화 잡음이 열잡음 이하인지 확인 | 중 |
| **쉴딩** | 외부 전자기 간섭(EMI) 차단 | 상 |
| **접지** | 그라운드 루프로 인한 잡음 유입 방지 | 중 |

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - 노이즈 피겨 과소평가**:
  수신기의 NF를 단일 값으로만 보고, 주파수/온도 변화를 무시하는 실수. 실제로는 대역별, 온도별 NF 변화를 고려해야 합니다.

- **안티패턴 2 - 이상적 AWGN 가정 오용**:
  실제 환경에서는 임펄스 잡음, 간섭, 페이딩이 존재함에도 AWGN만으로 시스템을 설계하면 성능이 크게 저하됩니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | 내용 | 정량적 지표 |
|----------|------|------------|
| **설계 정확도** | 정확한 노이즈 모델링으로 시스템 예측 신뢰성 향상 | 링크 마진 오차 ±1 dB 이내 |
| **성능 최적화** | 최적 SNR 달성을 위한 파라미터 튜닝 | 수신 감도 3 dB 개선 |
| **비용 절감** | 과설계 방지 및 최적 부품 선정 | RF 부품 비용 20% 절감 |
| **품질 보증** | BER 성능 예측과 실측값 일치 | 양산 수율 95% 이상 |

### 미래 전망 및 진화 방향

- **양자 잡음 한계**: 초저온 및 양자 증폭기를 활용하여 열잡음 한계를 돌파하는 양자 수신기가 연구되고 있습니다.

- **AI 기반 잡음 추정**: 딥러닝이 실제 채널의 잡음 통계적 특성을 학습하여, 비가우스/비백색 잡음 환경에서도 최적 복조를 수행합니다.

- **6G 테라헤르츠 대역**: THz 통신에서는 분자 흡수 잡음이 추가되어 기존 AWGN 모델 이상의 복잡한 채널 모델이 필요합니다.

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **ITU-R P.372** | ITU-R | Radio Noise |
| **IEEE 1453** | IEEE | Standard Definitions of Terms for Radio Noise and Interference |
| **MIL-STD-461** | DoD | Requirements for the Control of Electromagnetic Interference |

---

## 관련 개념 맵 (Knowledge Graph)
- [샤논 채널 용량](./21_shannon_capacity_isi.md) - AWGN 채널의 최대 전송 용량
- [신호 대 잡음비](./24_snr_signal_to_noise_ratio.md) - 신호와 잡음의 전력 비율
- [변조 기술](./modulation_ask_fsk_psk_qam.md) - AWGN 하에서의 변조 성능
- [오류 정정 코드](./error_correction_codes.md) - AWGN 오류 정정 기법
- [대역폭 및 효율성](./13_bandwidth_efficiency.md) - 대역폭과 노이즈의 관계

---

## 어린이를 위한 3줄 비유 설명
1. **백색 잡음**은 **비 오는 소리** 같아요. 수많은 빗방울이 만드는 '쉬익-'하는 소리처럼, 모든 주파수가 섞여서 만드는 잡음이에요.
2. **가우스**는 **키 순서로 줄 세우기**와 비슷해요. 대부분의 잡음은 평균 크기 근처에 있고, 아주 크거나 작은 잡음은 드물다는 것을 수학으로 표현한 거예요.
3. **AWGN**은 **음악에 섞인 비 소리**예요. 우리가 듣고 싶은 음악(신호) 위에 비 소리(잡음)가 겹쳐서, 비가 많이 올수록 음악이 잘 안 들리는 것처럼 통신 품질이 나빠져요!
