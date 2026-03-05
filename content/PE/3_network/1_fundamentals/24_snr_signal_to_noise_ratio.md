+++
title = "024. 신호 대 잡음비 (SNR: Signal-to-Noise Ratio)"
description = "SNR의 정의, 데시벨(dB) 표현, 측정 방법, 통신 시스템 성능 영향, BER-SNR 관계를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["SNR", "SignalToNoiseRatio", "dB", "BER", "EbN0", "NoiseFigure", "LinkBudget"]
categories = ["studynotes-3_network"]
+++

# 024. 신호 대 잡음비 (SNR: Signal-to-Noise Ratio)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SNR은 신호 전력과 잡음 전력의 비율로, 통신 시스템의 신호 품질을 나타내는 가장 기본적인 지표이며, 높을수록 데이터 복원이 용이하고 오류율이 낮아집니다.
> 2. **가치**: 링크 예산(Link Budget) 계산, 변조 방식 선택, 오류 정정 코드 설계의 핵심 파라미터로, 시스템 성능과 커버리지를 결정합니다.
> 3. **융합**: Eb/N₀(비트 에너지 대 잡음 밀도), Es/N₀(심볼 에너지 대 잡음 밀도)로 확장되어, 변조 차수와 코딩 레이트에 따른 성능 비교 기준이 됩니다.

---

## I. 개요 (Context & Background)

신호 대 잡음비(Signal-to-Noise Ratio, SNR)는 **원하는 신호의 전력(S)과 방해가 되는 잡음의 전력(N)의 비율**을 나타내는 무차원 지표입니다. 모든 통신 시스템에서 수신 신호의 품질을 평가하는 가장 기본적이고 중요한 척도입니다.

**수학적 정의**:
```
SNR = 신호 전력 / 잡음 전력 = S / N

선형 스케일: SNR_linear = P_signal / P_noise
로그 스케일 (dB): SNR_dB = 10 × log₁₀(P_signal / P_noise)
                = 10 × log₁₀(S) - 10 × log₁₀(N)
                = P_signal_dBm - P_noise_dBm
```

**비유**: SNR은 **"조용한 도서관에서 목소리 크기"**와 같습니다.
- **높은 SNR**: 도서관이 조용할 때(잡음 낮음) 큰 목소리로 말하면(신호 높음) 완벽하게 들립니다.
- **낮은 SNR**: 공사장 소음(잡음 높음) 속에서 작은 목소리로 말하면(신호 낮음) 잘 안 들립니다.
- **SNR = 0 dB**: 신호와 잡음이 같은 크기 → 거의 들리지 않음

**등장 배경 및 발전 과정**:
1. **초기 무선 통신 (1900년대)**: Marconi 등이 대서양 횡단 무선 통신에서 잡음 문제를 경험했습니다.
2. **정보이론의 탄생 (1948년)**: Claude Shannon이 "A Mathematical Theory of Communication"에서 채널 용량과 SNR의 관계를 정립했습니다.
3. **디지털 통신으로의 확장**: 1960년대 이후 디지털 변조에서 Eb/N₀가 BER과의 관계를 명확히 설명하는 지표로 자리잡았습니다.
4. **현대적 측정**: 스펙트럼 분석기, 벡터 신호 분석기 등으로 정밀 측정이 가능해졌습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### dB(데시벨) 체계 상세

| 단위 | 정의 | 기준 | 용도 |
|------|------|------|------|
| **dB** | 10 × log₁₀(P₁/P₀) | 상대적 비율 | 이득, 손실, SNR |
| **dBm** | 10 × log₁₀(P/1mW) | 1 mW | 절대 전력 |
| **dBW** | 10 × log₁₀(P/1W) | 1 W | 고전력 시스템 |
| **dBμV** | 20 × log₁₀(V/1μV) | 1 μV | 케이블 TV, 안테나 |
| **dBi** | 10 × log₁₀(G/G_iso) | 등방성 안테나 | 안테나 이득 |
| **dBc** | 10 × log₁₀(P_side/P_carrier) | 반송파 전력 | 스퓨리어스 |

**dB 변환 예시**:
```
전력 비 10배    = 10 dB
전력 비 2배     = 3.01 dB ≈ 3 dB
전력 비 100배   = 20 dB
전력 비 1000배  = 30 dB
전력 비 0.5배   = -3 dB
전력 비 0.1배   = -10 dB

전압 비 10배    = 20 dB (전력은 V²에 비례)
전압 비 2배     = 6.02 dB ≈ 6 dB
```

### SNR 관련 지표 비교

| 지표 | 정의 | 용도 | 공식 |
|------|------|------|------|
| **SNR** | 신호 전력 / 잡음 전력 | 아날로그/디지털 품질 | S/N |
| **Eb/N₀** | 비트 에너지 / 잡음 PSD | 디지털 변조 성능 | (S/R) / N₀ |
| **Es/N₀** | 심볼 에너지 / 잡음 PSD | 변조+코딩 성능 | (S/Rs) / N₀ |
| **C/N** | 반송파 전력 / 잡음 전력 | 무선 링크 품질 | C/N |
| **C/I** | 반송파 전력 / 간섭 전력 | 셀룰러 설계 | C/I |
| **SINAD** | (S+I+N+D)/(I+N+D) | 오디오/수신기 품질 | (S+I+N+D)/(I+N+D) |

### 정교한 구조 다이어그램: SNR과 통신 시스템

```ascii
================================================================================
[ SNR in Communication System Chain ]
================================================================================

                    송신측                         수신측
                  +--------+                    +--------+
    데이터 -----> | 변조기 | ====> 채널 ====> | 복조기 | -----> 데이터
                  +--------+                    +--------+
                      |                             ^
                      v                             |
              +---------------+            +------------------+
              | 송신 전력 P_tx |            | 수신 전력 P_rx   |
              | (dBm)         |            | (dBm)            |
              +---------------+            +------------------+
                      |                             ^
                      v                             |
              +---------------+            +------------------+
              | 안테나 이득   |            | 안테나 이득      |
              | G_tx (dBi)   |            | G_rx (dBi)       |
              +---------------+            +------------------+
                      |                             ^
                      v            경로            |
              +---------------+    손실            +------------------+
              | EIRP         |    L_path         | 수신 신호 전력    |
              | (dBm)        | ==============>   | S = P_rx (dBm)   |
              +---------------+  +--------+      +------------------+
                                 | 잡음   |             |
                                 | 추가   |             v
                                 +--------+    +------------------+
                                               | 잡음 전력        |
                                               | N = kTB (dBm)   |
                                               +------------------+
                                                      |
                                                      v
                                               +------------------+
                                               | SNR = S - N (dB) |
                                               | 수신 품질 지표    |
                                               +------------------+

================================================================================
[ Link Budget Calculation ]
================================================================================

EIRP (Effective Isotropic Radiated Power):
    EIRP = P_tx + G_tx - L_cable (dBm)

수신 신호 전력:
    P_rx = EIRP - L_path + G_rx - L_cable (dBm)
         = P_tx + G_tx - L_path + G_rx - 2×L_cable

잡음 전력 (열잡음):
    N = k × T × B
    N_dBm = -174 + 10×log₁₀(B) + NF
    여기서:
    - k = 볼츠만 상수 = 1.38×10⁻²³ J/K
    - T = 절대 온도 (K)
    - B = 대역폭 (Hz)
    - NF = 잡음 지수 (dB)

최종 SNR:
    SNR_dB = P_rx - N_dBm
           = P_tx + G_tx - L_path + G_rx - L_cable - (-174 + 10×log₁₀(B) + NF)

================================================================================
[ SNR vs BER for Different Modulations ]
================================================================================

BER (Bit Error Rate)

    10⁻¹ |                                      o QPSK
         |                                  o
    10⁻² |                              o
         |                          o      o 16-QAM
    10⁻³ |                      o
         |                  o       o
    10⁻⁴ |              o
         |          o       o           o 64-QAM
    10⁻⁵ |      o
         |  o       o
    10⁻⁶ |o__________________________________________
         0   5   10  15  20  25  30  35  40  45 (dB)
                           Eb/N₀

    변조 차수가 높을수록 같은 BER을 얻기 위해 더 높은 SNR 필요
    - QPSK: BER 10⁻⁶ 위해 약 10.5 dB 필요
    - 16-QAM: BER 10⁻⁶ 위해 약 14.5 dB 필요
    - 64-QAM: BER 10⁻⁶ 위해 약 19 dB 필요

================================================================================
```

### 심층 동작 원리: 열잡음 계산

**열잡음 (Thermal Noise) / 존슨-나이퀴스트 잡음**:
```
잡음 전력 밀도: N₀ = kT (W/Hz)
               = 1.38 × 10⁻²³ × 290 K
               = 4.00 × 10⁻²¹ W/Hz
               = -174 dBm/Hz (실온 17°C)

대역폭 B에 대한 총 잡음 전력:
    N = kTB (Watt)
    N_dBm = -174 + 10×log₁₀(B)

예시:
    - B = 1 MHz: N = -174 + 60 = -114 dBm
    - B = 10 MHz: N = -174 + 70 = -104 dBm
    - B = 100 MHz: N = -174 + 80 = -94 dBm
```

**잡음 지수 (Noise Figure, NF)**:
```
NF = SNR_in / SNR_out (선형)
NF_dB = SNR_in_dB - SNR_out_dB

NF는 장비(증폭기, 믹서 등)가 추가하는 잡음의 양
일반적인 값:
    - LNA (저잡음 증폭기): 0.5 ~ 2 dB
    - 믹서: 6 ~ 10 dB
    - 수신기 전체: 5 ~ 15 dB
```

### 핵심 코드: SNR 계산 및 링크 예산 (Python)

```python
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List
import matplotlib.pyplot as plt

@dataclass
class LinkBudgetParams:
    """링크 예산 계산 파라미터"""
    tx_power_dbm: float = 43.0        # 송신 전력 (dBm)
    tx_antenna_gain_dbi: float = 15.0 # 송신 안테나 이득 (dBi)
    rx_antenna_gain_dbi: float = 20.0 # 수신 안테나 이득 (dBi)
    cable_loss_db: float = 2.0        # 케이블 손실 (dB)
    frequency_mhz: float = 2400.0     # 주파수 (MHz)
    distance_km: float = 10.0         # 거리 (km)
    bandwidth_hz: float = 20e6        # 대역폭 (Hz)
    noise_figure_db: float = 5.0      # 잡음 지수 (dB)
    temperature_k: float = 290.0      # 온도 (K)


class SNRCalculator:
    """
    SNR 계산 및 링크 예산 분석 클래스
    """

    BOLTZMANN_CONSTANT = 1.38e-23  # J/K

    def __init__(self, params: LinkBudgetParams):
        self.params = params

    def calculate_thermal_noise(self, bandwidth_hz: float = None) -> float:
        """
        열잡음 전력 계산 (dBm)

        Args:
            bandwidth_hz: 대역폭 (Hz). None이면 params 사용

        Returns:
            잡음 전력 (dBm)
        """
        if bandwidth_hz is None:
            bandwidth_hz = self.params.bandwidth_hz

        # N = kTB (Watt)
        noise_power_w = self.BOLTZMANN_CONSTANT * self.params.temperature_k * bandwidth_hz

        # dBm 변환: 10*log10(W/1mW)
        noise_power_dbm = 10 * np.log10(noise_power_w * 1000)

        return noise_power_dbm

    def calculate_free_space_path_loss(self, distance_km: float = None) -> float:
        """
        자유 공간 경로 손실 (FSPL) 계산

        FSPL(dB) = 20*log10(d) + 20*log10(f) + 32.44
        여기서 d는 km, f는 MHz

        Args:
            distance_km: 거리 (km)

        Returns:
            경로 손실 (dB)
        """
        if distance_km is None:
            distance_km = self.params.distance_km

        fspl_db = (20 * np.log10(distance_km) +
                   20 * np.log10(self.params.frequency_mhz) +
                   32.44)

        return fspl_db

    def calculate_eirp(self) -> float:
        """
        유효 등방성 복사 전력 (EIRP) 계산

        Returns:
            EIRP (dBm)
        """
        eirp = (self.params.tx_power_dbm +
                self.params.tx_antenna_gain_dbi -
                self.params.cable_loss_db)
        return eirp

    def calculate_received_power(self, distance_km: float = None) -> float:
        """
        수신 전력 계산

        Args:
            distance_km: 거리 (km)

        Returns:
            수신 전력 (dBm)
        """
        if distance_km is None:
            distance_km = self.params.distance_km

        eirp = self.calculate_eirp()
        path_loss = self.calculate_free_space_path_loss(distance_km)

        rx_power = (eirp - path_loss +
                   self.params.rx_antenna_gain_dbi -
                   self.params.cable_loss_db)

        return rx_power

    def calculate_snr(self, distance_km: float = None) -> float:
        """
        SNR 계산

        Args:
            distance_km: 거리 (km)

        Returns:
            SNR (dB)
        """
        rx_power = self.calculate_received_power(distance_km)
        noise_power = self.calculate_thermal_noise()
        total_noise = noise_power + self.params.noise_figure_db

        snr_db = rx_power - total_noise
        return snr_db

    def calculate_link_budget_table(self) -> List[Tuple[str, float, str]]:
        """
        링크 예산 테이블 생성

        Returns:
            (항목명, 값, 단위) 리스트
        """
        budget = [
            ("송신 전력", self.params.tx_power_dbm, "dBm"),
            ("송신 안테나 이득", self.params.tx_antenna_gain_dbi, "dBi"),
            ("케이블 손실", -self.params.cable_loss_db, "dB"),
            ("EIRP", self.calculate_eirp(), "dBm"),
            ("자유 공간 경로 손실", -self.calculate_free_space_path_loss(), "dB"),
            ("수신 안테나 이득", self.params.rx_antenna_gain_dbi, "dBi"),
            ("케이블 손실", -self.params.cable_loss_db, "dB"),
            ("수신 신호 전력", self.calculate_received_power(), "dBm"),
            ("열잡음 전력", self.calculate_thermal_noise(), "dBm"),
            ("잡음 지수", self.params.noise_figure_db, "dB"),
            ("총 잡음 전력", self.calculate_thermal_noise() + self.params.noise_figure_db, "dBm"),
            ("SNR", self.calculate_snr(), "dB"),
        ]
        return budget

    def calculate_max_range(self, min_snr_db: float = 10.0) -> float:
        """
        최대 통신 거리 계산

        Args:
            min_snr_db: 필요한 최소 SNR (dB)

        Returns:
            최대 거리 (km)
        """
        # 수신 전력 = 총 잡음 + min_snr
        # EIRP - FSPL + G_rx - L_cable = N_total + min_snr
        # FSPL = EIRP + G_rx - L_cable - N_total - min_snr

        eirp = self.calculate_eirp()
        total_noise = self.calculate_thermal_noise() + self.params.noise_figure_db

        max_path_loss = (eirp +
                        self.params.rx_antenna_gain_dbi -
                        self.params.cable_loss_db -
                        total_noise -
                        min_snr_db)

        # FSPL = 20*log10(d) + 20*log10(f) + 32.44에서 d 계산
        # 20*log10(d) = FSPL - 20*log10(f) - 32.44
        log_d = (max_path_loss -
                20 * np.log10(self.params.frequency_mhz) -
                32.44) / 20

        max_distance = 10 ** log_d
        return max_distance


class SNRAnalyzer:
    """
    SNR 분석 및 BER 계산 클래스
    """

    @staticmethod
    def q_function(x: float) -> float:
        """
        Q 함수 (가우시안 tail 확률)
        Q(x) = 0.5 * erfc(x / sqrt(2))
        """
        from scipy import special
        return 0.5 * special.erfc(x / np.sqrt(2))

    @staticmethod
    def ber_bpsk(eb_n0_db: float) -> float:
        """
        BPSK 변조의 BER

        Args:
            eb_n0_db: Eb/N₀ (dB)

        Returns:
            BER
        """
        eb_n0_linear = 10 ** (eb_n0_db / 10)
        return SNRAnalyzer.q_function(np.sqrt(2 * eb_n0_linear))

    @staticmethod
    def ber_qpsk(eb_n0_db: float) -> float:
        """
        QPSK 변조의 BER (Gray coding)
        BPSK와 동일
        """
        return SNRAnalyzer.ber_bpsk(eb_n0_db)

    @staticmethod
    def ber_16qam(eb_n0_db: float) -> float:
        """
        16-QAM의 근사 BER (Gray coding)
        """
        eb_n0_linear = 10 ** (eb_n0_db / 10)
        # 근사식
        return (3/4) * SNRAnalyzer.q_function(np.sqrt(4 * eb_n0_linear / 5))

    @staticmethod
    def ber_64qam(eb_n0_db: float) -> float:
        """
        64-QAM의 근사 BER (Gray coding)
        """
        eb_n0_linear = 10 ** (eb_n0_db / 10)
        # 근사식
        return (7/12) * SNRAnalyzer.q_function(np.sqrt(6 * eb_n0_linear / 7))

    @staticmethod
    def snr_to_eb_n0(snr_db: float, bit_rate: float, bandwidth: float) -> float:
        """
        SNR을 Eb/N₀로 변환

        Eb/N₀ = (S/R) / (N/B) = (S/N) × (B/R) = SNR × (B/R)

        Args:
            snr_db: SNR (dB)
            bit_rate: 비트 레이트 (bps)
            bandwidth: 대역폭 (Hz)

        Returns:
            Eb/N₀ (dB)
        """
        snr_linear = 10 ** (snr_db / 10)
        eb_n0_linear = snr_linear * (bandwidth / bit_rate)
        return 10 * np.log10(eb_n0_linear)

    @staticmethod
    def eb_n0_to_snr(eb_n0_db: float, bit_rate: float, bandwidth: float) -> float:
        """
        Eb/N₀를 SNR로 변환
        """
        eb_n0_linear = 10 ** (eb_n0_db / 10)
        snr_linear = eb_n0_linear / (bandwidth / bit_rate)
        return 10 * np.log10(snr_linear)

    @staticmethod
    def generate_ber_curve(modulation: str = 'bpsk',
                          eb_n0_range: Tuple[float, float] = (0, 20),
                          num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        BER 커브 생성

        Args:
            modulation: 변조 방식 ('bpsk', 'qpsk', '16qam', '64qam')
            eb_n0_range: Eb/N₀ 범위 (dB)
            num_points: 포인트 수

        Returns:
            (Eb/N₀ 배열, BER 배열)
        """
        eb_n0 = np.linspace(eb_n0_range[0], eb_n0_range[1], num_points)

        ber_funcs = {
            'bpsk': SNRAnalyzer.ber_bpsk,
            'qpsk': SNRAnalyzer.ber_qpsk,
            '16qam': SNRAnalyzer.ber_16qam,
            '64qam': SNRAnalyzer.ber_64qam,
        }

        ber = np.array([ber_funcs[modulation](e) for e in eb_n0])
        return eb_n0, ber


# 사용 예시
if __name__ == "__main__":
    # 링크 예산 계산
    params = LinkBudgetParams(
        tx_power_dbm=43.0,
        tx_antenna_gain_dbi=18.0,
        rx_antenna_gain_dbi=24.0,
        frequency_mhz=2400.0,
        distance_km=5.0,
        bandwidth_hz=20e6,
        noise_figure_db=3.0
    )

    calc = SNRCalculator(params)

    print("=" * 60)
    print("링크 예산 분석")
    print("=" * 60)

    budget = calc.calculate_link_budget_table()
    for item, value, unit in budget:
        print(f"{item:25s}: {value:8.2f} {unit}")

    print(f"\n최대 통신 거리 (SNR >= 10 dB): {calc.calculate_max_range(10):.2f} km")

    # BER 분석
    print("\n" + "=" * 60)
    print("BER vs Eb/N₀ 분석")
    print("=" * 60)

    analyzer = SNRAnalyzer()

    for mod in ['bpsk', 'qpsk', '16qam', '64qam']:
        eb_n0, ber = analyzer.generate_ber_curve(mod)
        # BER 10^-6 달성을 위한 Eb/N₀ 찾기
        idx = np.argmin(np.abs(ber - 1e-6))
        print(f"{mod.upper():8s}: BER 10⁻⁶ 위해 Eb/N₀ ≈ {eb_n0[idx]:.1f} dB")

    print("\n=== SNR 분석 완료 ===")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### SNR 유도 지표 비교

| 지표 | 정의 | 관계식 | 용도 |
|------|------|--------|------|
| **SNR** | S/N | 기본 | 전체 시스템 품질 |
| **Eb/N₀** | (S/R)/N₀ | Eb/N₀ = SNR × (B/R) | 변조 성능 비교 |
| **Es/N₀** | (S/Rs)/N₀ | Es/N₀ = SNR × (B/Rs) | 코딩 포함 성능 |
| **C/N₀** | C/N₀ | C/N₀ = SNR × B | 위성 GPS |

### 잡음 유형별 영향

| 잡음 유형 | 원인 | 주파수 특성 | 완화 방법 |
|----------|------|------------|----------|
| **열잡음** | 전자 열운동 | 백색 (평탄) | 저잡음 증폭기, 냉각 |
| **산탄 잡음** | 전자의 양자적 성질 | 1/f (저주파) | 전류 증가 |
| **플리커 잡음** | 반도체 결함 | 1/f | 차동 증폭기 |
| **충격 잡음** | 외부 전자기파 | 비정기적 | 필터링, 차폐 |
| **간섭 잡음** | 인접 채널, 타 시스템 | 협대역 | 주파수 계획, 셀 설계 |

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 위성 통신 링크 설계

**문제 상황**: GEO 위성(궤도 고도 35,786 km)에서 지구국으로 12 GHz 대역, 36 MHz 트랜스폰더로 DVB-S2 전송을 설계합니다. 필요 SNR은 16 dB (8PSK, 3/4 코드)입니다.

**기술사의 전략적 의사결정**:

1. **경로 손실 계산**:
   ```
   FSPL = 20×log₁₀(35,786×10³) + 20×log₁₀(12×10⁹) + 92.45
        = 20×7.55 + 20×10.08 + 92.45
        = 151.0 + 201.6 + 92.45
        = 205.1 dB
   ```

2. **링크 마진 확보**:
   - 강우 감쇠 (12 GHz): ~5 dB
   - 안테나 오정렬: 1 dB
   - 노화 마진: 2 dB
   - 총 마진: 8 dB
   - 필요 SNR: 16 + 8 = 24 dB

3. **파라미터 최적화**:
   - 위성 EIRP: 52 dBW
   - 지구국 G/T: 35 dB/K
   - 결과 C/N: 24 dB 달성

---

## V. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| SNR 수준 | 품질 | 적용 서비스 |
|----------|------|------------|
| > 30 dB | 우수 | 고해상도 비디오, 백홀 |
| 20-30 dB | 양호 | HD 스트리밍, VoIP |
| 10-20 dB | 보통 | 웹 브라우징, 이메일 |
| 0-10 dB | 열악 | 저속 데이터, SMS |

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **ITU-R P.372** | ITU | 라디오 잡음 |
| **IEEE 802.11** | IEEE | Wi-Fi SNR 요구사항 |
| **3GPP TS 36.101** | 3GPP | LTE UE 성능 요구사항 |

---

## 관련 개념 맵 (Knowledge Graph)
- [샤논 채널 용량](./21_shannon_capacity_isi.md) - SNR과 용량 관계
- [변조 기술](./modulation_ask_fsk_psk_qam.md) - SNR 요구사항별 변조
- [오류 정정 코드](./error_correction_codes.md) - 코딩 게인
- [링크 예산](./16_propagation_delay.md) - 전파 전파 손실
- [잡음 지수](./channel_capacity_shannon.md) - 증폭기 잡음

---

## 어린이를 위한 3줄 비유 설명
1. **SNR**은 **조용한 방에서 내 목소리가 얼마나 잘 들리는지**를 나타내는 점수예요.
2. **잡음**은 **시끄러운 건물 공사 소리**나 **텔레비전 소리**처럼 내 말을 방해하는 소리예요.
3. **높은 SNR**은 **조용한 도서관**에서 말하는 것, **낮은 SNR**은 **공사장**에서 속삭이는 것과 같아요!
