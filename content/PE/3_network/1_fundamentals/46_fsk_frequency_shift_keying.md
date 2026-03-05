+++
title = "046. 주파수 편이 변조 (FSK - Frequency Shift Keying)"
description = "디지털 변조 기법인 FSK의 원리, 종류(BFSK, M-FSK, MSK, GFSK), 장단점, 그리고 블루투스, 모뎀 등 실무 응용을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["FSK", "FrequencyShiftKeying", "MSK", "GFSK", "Bluetooth", "Modem", "DigitalModulation"]
categories = ["studynotes-3_network"]
+++

# 046. 주파수 편이 변조 (FSK - Frequency Shift Keying)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: FSK(Frequency Shift Keying)는 반송파의 주파수를 디지털 데이터에 따라 이산적으로 변화시키는 변조 방식으로, 비트 0과 1을 서로 다른 주파수의 정현파로 표현하여 진폭 잡음에 강한 특성을 가집니다.
> 2. **가치**: 일정한 진폭(Constant Envelope)으로 인해 비선형 증폭기 사용이 가능하고 전력 효율이 높으며, 블루투스(GFSK), DECT 전화기, 모뎀(V.21/V.23) 등에서 널리 활용됩니다.
> 3. **융합**: MSK(Minimum Shift Keying), GMSK(Gaussian MSK)로 진화하여 GSM 이동통신의 기반이 되었으며, LoRa(LPWAN)의 CSS(Chirp Spread Spectrum)도 FSK의 확장 개념입니다.

---

## Ⅰ. 개요 (Context & Background)

주파수 편이 변조(Frequency Shift Keying, FSK)는 **반송파의 주파수(Frequency)를 디지털 신호의 0과 1에 따라 변화시키는** 디지털 변조 방식입니다. 이는 아날로그 주파수 변조(FM)의 디지털 버전입니다.

### FSK의 기본 정의

**수학적 표현**:
```
s(t) = A·cos(2π·f_i·t + φ)

여기서:
- f_i: 비트 i에 해당하는 주파수
- 비트 0: f_0 주파수
- 비트 1: f_1 주파수

이진 FSK (Binary FSK):
s_0(t) = A·cos(2π·f_0·t)  (비트 0)
s_1(t) = A·cos(2π·f_1·t)  (비트 1)
```

### FSK의 종류

| 종류 | 설명 | 주파수 차이 | 응용 분야 |
|------|------|------------|----------|
| **BFSK** | Binary FSK, 2개 주파수 | Δf ≥ R/2 | 기본 FSK |
| **M-FSK** | M개 주파수 사용 | 다중 | 군사 통신 |
| **MSK** | Minimum Shift Keying | Δf = R/2 | GSM |
| **GMSK** | Gaussian-filtered MSK | Δf = R/2 | GSM, DECT |
| **GFSK** | Gaussian-filtered FSK | 가변 | 블루투스 |
| **2FSK/4FSK** | 2/4 레벨 FSK | 다중 | 차세대 이동통신 |

**💡 비유**: FSK는 **'피리 부는 법'**과 같습니다.
- 낮은 음(주파수 f_0)을 불면 0, 높은 음(주파수 f_1)을 불면 1입니다.
- 음량(진폭)은 일정하게 유지하면서 음높이만 바꿉니다.
- 주변 소음(잡음)이 있어도 음높이는 구별할 수 있어 ASK보다 잡음에 강합니다.
- 음과 음 사이가 너무 가까우면 구분하기 어렵고(MSF 필요), 너무 멀면 대역폭 낭비입니다.

**등장 배경 및 발전 과정**:

1. **전신타자기(Teletype) 시대 (1930~60년대)**:
   전신타자기는 주파수 변환 방식으로 동작했습니다. 0과 1을 서로 다른 톤(Tone)으로 전송하여 잡음 환경에서도 신뢰성 있는 통신을 가능케 했습니다.

2. **음향 모뎀의 등장 (1960~90년대)**:
   전화선을 통한 데이터 통신을 위해 V.21(300bps), V.23(1200bps) 등의 FSK 모뎀 표준이 개발되었습니다. 이들은 전화 대역(300-3400Hz) 내에서 두 주파수를 사용했습니다.

3. **이동통신으로의 확장 (1980~2000년대)**:
   GSM 디지털 이동통신은 GMSK(Gaussian Minimum Shift Keying)를 채택하여 스펙트럼 효율과 전력 효율을 동시에 달성했습니다. 블루투스는 GFSK를 사용합니다.

4. **저전력 광역 통신망 (LPWAN)**:
   LoRa, Sigfox 등 IoT 통신 기술에서 변형된 FSK 기술이 활용되어 수 km 거리를 저전력으로 전송합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### FSK 변조 시스템 구조

```ascii
================================================================================
[ FSK Modulator Architecture ]
================================================================================

                         +-------------+
   디지털 입력           |  주파수    |
   (비트 스트림)         |  선택기    |         +-------------+
   ============>-------->| (Frequency |------->|  VCO        |
   1 0 1 1 0             |  Selector) |        | (Voltage    |
                         +-------------+        |  Controlled |-----> s(t)
                                 |              |  Oscillator)|
                                 v              +-------------+
                         +-------------+
                         |  룩업      |
                         |  테이블    |
                         |  f_0 ↔ 0   |
                         |  f_1 ↔ 1   |
                         +-------------+

   대안 구현: 두 개의 독립적인 발진기 사용
   +--------+                        +--------+
   | OSC f_0|---\                    |  BPF   |--->
   +--------+    \    +----------+   |  f_0   |
                 --->| Switch   |---+--------+
   +--------+    /    | (MUX)    |   |  BPF   |
   | OSC f_1|---/     +----------+   |  f_1   |
   +--------+                        +--------+

================================================================================
[ FSK Signal Waveform ]
================================================================================

   입력 비트:     1     0     1     1     0     0     1
                  |     |     |     |     |     |     |
   주파수:       f_1   f_0   f_1   f_1   f_0   f_0   f_1

   FSK 출력:

   고주파 (f_1): ∿∿∿∿     ∿∿∿∿ ∿∿∿∿           ∿∿∿∿
               |\  /|    |\  /|\  /|          |\  /|
               | \/ |    | \/ | \/ |          | \/ |
               | /\ |    | /\ | /\ |          | /\ |
               |/  \|    |/  \|/  \|          |/  \|

   저주파 (f_0):      ~~~~               ~~~~ ~~~~
                     |\  /|             |\  /|\  /|
                     | \/ |             | \/ | \/ |
                     | /\ |             | /\ | /\ |
                     |/  \|             |/  \|/  \|

   결합된 FSK:   ∿∿∿∿~~~~∿∿∿∿∿∿∿∿~~~~~~~~∿∿∿∿
                |<-1->|<-0->|<-1->|<-0->|<-0->|<-1->|

   시간 ──────────────────────────────────────────────────>

================================================================================
[ FSK Power Spectrum ]
================================================================================

   전력 스펙트럼 밀도 (PSD)

   |P(f)|
     ^
     |                    +-------+
     |                    |       |
     |    +-------+       |  S_1  |       +-------+
     |    |       |       | (f_1) |       |       |
     |    |  S_0  |       |       |       | 다중  |
     |    | (f_0) |       +---+---+       | 사이드|
     |    |       |           |           | 밴드  |
     +----+-------+-----------+-----------+-------+----> f
          f_0     |     f_c   |     f_1
                  |           |
                  +-----+-----+
                    대역폭 B

   필요 대역폭: B ≈ 2·Δf + 2·R_b
   (Carson's Rule 근사)

   여기서:
   - Δf = |f_1 - f_0| / 2: 주파수 편차
   - R_b: 비트 레이트
   - m_f = 2·Δf / R_b: 변조 지수

================================================================================
[ FSK Demodulator: Non-Coherent Detection ]
================================================================================

   수신 FSK 신호 r(t)

   +----------------+         +------+
   |    대역통과    |         | 판정 |
   |    필터 BPF    |----+--->| 회로 |---> 비트 출력
   +----------------+    |    +------+
                         |
   +----------------+    |    검출된 신호
   |  BPF f_0  |----+--->|    d_0(t)
   |  (저주파) |         |
   +-------+----+         |    +----------------+
           |              +--->|  d_0(t)        |
           v              |    |   ∧∧∧  ∧∧    |--> 0
   +-------+----+         |    |  /  \ /  \    |
   | 포락선    |--------->+    +----------------+
   | 검파器   |          |
   +-------+----+          |    +----------------+
           |               +--->|  d_1(t)        |
           v                    |      ∧∧   ∧  |--> 1
   +-------+----+              |     /  \ /  \ |
   | 저역통과   |              +----------------+
   | 필터 LPF  |
   +-----------+

   동일 구조가 f_1 (고주파)에 대해 반복됨

   판정: d_1 > d_0 이면 비트 1, 아니면 비트 0

================================================================================
```

### FSK의 핵심 파라미터

#### 변조 지수 (Modulation Index)

```
h = (f_1 - f_0) / R_b = 2·Δf / R_b

여기서:
- h < 1: Narrowband FSK (대역폭 효율적)
- h = 0.5: MSK (Minimum Shift Keying)
- h = 1: Sunde's FSK (직교 FSK)
- h > 1: Wideband FSK (잡음 내성 높음)
```

#### 직교 조건 (Orthogonality)

```
두 FSK 신호가 직교하기 위한 조건:

∫ s_0(t)·s_1(t) dt = 0

최소 주파수 간격:
Δf_min = R_b / 2  (MSK의 경우)

직교 FSK (h = 1):
Δf = R_b
```

### FSK의 성능 분석

#### 비트 에러율 (BER)

```
비동기 검파 (Non-Coherent):

P_b = (1/2)·exp(-E_b/(2·N_0))

동기 검파 (Coherent):

P_b = Q(√(E_b/N_0))

비교:
- Coherent FSK ≈ BPSK와 유사
- Non-Coherent FSK는 약 1-2dB 열등
```

### 핵심 코드: FSK 변조/복조 구현 (Python)

```python
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum

class FSKType(Enum):
    """FSK 종류"""
    BFSK = "BFSK"
    MSK = "MSK"
    GFSK = "GFSK"

@dataclass
class FSKConfig:
    """FSK 설정 파라미터"""
    f_0: float = 980.0        # 비트 0 주파수 (Hz)
    f_1: float = 1180.0       # 비트 1 주파수 (Hz)
    sample_rate: float = 8000.0  # 샘플링 레이트 (Hz)
    bit_rate: float = 300.0   # 비트 레이트 (bps)
    fsk_type: FSKType = FSKType.BFSK

    @property
    def samples_per_bit(self) -> int:
        return int(self.sample_rate / self.bit_rate)

    @property
    def modulation_index(self) -> float:
        return (self.f_1 - self.f_0) / self.bit_rate

class FSKModulator:
    """FSK 변조기"""

    def __init__(self, config: FSKConfig):
        self.config = config

    def modulate(self, bits: List[int]) -> Tuple[np.ndarray, np.ndarray]:
        """비트 스트림을 FSK 신호로 변조"""
        spb = self.config.samples_per_bit
        n_bits = len(bits)
        n_samples = n_bits * spb

        # 시간 배열
        t = np.arange(n_samples) / self.config.sample_rate

        # 위상 연속성을 위한 위상 누적
        phase = 0.0
        signal = np.zeros(n_samples)

        for i, bit in enumerate(bits):
            freq = self.config.f_1 if bit == 1 else self.config.f_0
            start = i * spb
            end = (i + 1) * spb

            # 위상 연속적 FSK (Continuous Phase FSK)
            t_bit = t[start:end] - t[start]
            signal[start:end] = np.cos(2 * np.pi * freq * t_bit + phase)

            # 다음 비트의 초기 위상 계산
            phase += 2 * np.pi * freq * (spb / self.config.sample_rate)
            phase = phase % (2 * np.pi)

        return signal, t

    def modulate_msk(self, bits: List[int]) -> Tuple[np.ndarray, np.ndarray]:
        """MSK (Minimum Shift Keying) 변조"""
        config = self.config
        spb = config.samples_per_bit
        n_bits = len(bits)
        n_samples = n_bits * spb
        t = np.arange(n_samples) / config.sample_rate

        # MSK: h = 0.5, Δf = R_b/2
        f_c = (config.f_0 + config.f_1) / 2
        delta_f = config.bit_rate / 2

        signal = np.zeros(n_samples)
        phase = 0.0

        for i, bit in enumerate(bits):
            start = i * spb
            end = (i + 1) * spb
            t_bit = t[start:end] - t[start]

            # 비트에 따른 주파수 편차
            freq = f_c + (delta_f if bit == 1 else -delta_f)
            signal[start:end] = np.cos(2 * np.pi * freq * t_bit + phase)

            phase += 2 * np.pi * freq * (spb / config.sample_rate)
            phase = phase % (2 * np.pi)

        return signal, t

class FSKDemodulator:
    """FSK 복조기"""

    def __init__(self, config: FSKConfig):
        self.config = config

    def demodulate_noncoherent(
        self,
        signal: np.ndarray
    ) -> Tuple[List[int], np.ndarray]:
        """비동기 검파 (Non-Coherent Detection)"""
        spb = self.config.samples_per_bit
        n_samples = len(signal)
        n_bits = n_samples // spb
        t = np.arange(n_samples) / self.config.sample_rate

        # 각 주파수에 대한 상관기 (Correlator)
        energy_f0 = np.zeros(n_bits)
        energy_f1 = np.zeros(n_bits)

        for i in range(n_bits):
            start = i * spb
            end = (i + 1) * spb
            segment = signal[start:end]
            t_seg = t[start:end]

            # f_0 주파수 성분 에너지
            cos_f0 = np.cos(2 * np.pi * self.config.f_0 * t_seg)
            sin_f0 = np.sin(2 * np.pi * self.config.f_0 * t_seg)
            energy_f0[i] = np.sum(segment * cos_f0)**2 + np.sum(segment * sin_f0)**2

            # f_1 주파수 성분 에너지
            cos_f1 = np.cos(2 * np.pi * self.config.f_1 * t_seg)
            sin_f1 = np.sin(2 * np.pi * self.config.f_1 * t_seg)
            energy_f1[i] = np.sum(segment * cos_f1)**2 + np.sum(segment * sin_f1)**2

        # 판정
        detected = energy_f1 - energy_f0
        bits = [1 if e > 0 else 0 for e in detected]

        return bits, detected

    def demodulate_pll(self, signal: np.ndarray) -> List[int]:
        """PLL 기반 복조"""
        # 간소화된 PLL 복조 (실제는 더 복잡)
        # 위상 변화율로 주파수 추정

        spb = self.config.samples_per_bit
        n_bits = len(signal) // spb
        bits = []

        for i in range(n_bits):
            start = i * spb
            end = (i + 1) * spb
            segment = signal[start:end]

            # 순시 주파수 추정 (위상 미분)
            analytic = segment + 1j * np.imag(
                np.fft.ifft(np.fft.fft(segment) * 2 *
                           np.heaviside(np.arange(len(segment)) - len(segment)//2, 0.5))
            )
            phase = np.unwrap(np.angle(analytic))
            freq_estimate = np.mean(np.diff(phase) * self.config.sample_rate / (2 * np.pi))

            # 주파수에 따른 판정
            threshold = (self.config.f_0 + self.config.f_1) / 2
            bits.append(1 if freq_estimate > threshold else 0)

        return bits

class AWGNChannel:
    """AWGN 채널"""
    def __init__(self, snr_db: float):
        self.snr_db = snr_db

    def transmit(self, signal: np.ndarray) -> np.ndarray:
        snr_linear = 10 ** (self.snr_db / 10)
        signal_power = np.mean(signal ** 2)
        noise_power = signal_power / snr_linear
        noise = np.sqrt(noise_power) * np.random.randn(len(signal))
        return signal + noise

def run_fsk_simulation():
    """FSK 시뮬레이션"""
    np.random.seed(42)

    # V.21 모뎀 파라미터 (300 bps)
    config = FSKConfig(
        f_0=980, f_1=1180,
        sample_rate=8000,
        bit_rate=300,
        fsk_type=FSKType.BFSK
    )

    print("=" * 70)
    print("FSK (Frequency Shift Keying) 시뮬레이션")
    print("=" * 70)
    print(f"\n변조 지수 h = {config.modulation_index:.2f}")
    print(f"샘플당 비트 수 = {config.samples_per_bit}")

    # 테스트 비트
    test_bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]

    modulator = FSKModulator(config)
    demodulator = FSKDemodulator(config)

    # 변조
    signal, t = modulator.modulate(test_bits)

    # 채널
    channel = AWGNChannel(snr_db=15)
    noisy_signal = channel.transmit(signal)

    # 복조
    decoded_bits, detected = demodulator.demodulate_noncoherent(noisy_signal)

    print(f"\n원본 비트: {test_bits}")
    print(f"복조 비트: {decoded_bits}")

    errors = sum(1 for i in range(len(test_bits)) if test_bits[i] != decoded_bits[i])
    print(f"에러 수: {errors}/{len(test_bits)}")
    print(f"BER: {errors/len(test_bits):.4f}")

if __name__ == "__main__":
    run_fsk_simulation()
