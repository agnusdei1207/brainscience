+++
title = "045. 진폭 편이 변조 (ASK - Amplitude Shift Keying)"
description = "디지털 변조 기법의 기초인 ASK의 원리, 종류, 장단점, 그리고 실무 응용 분야를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["ASK", "OOK", "AmplitudeShiftKeying", "DigitalModulation", "OpticalFiber", "IRCommunication", "RFID"]
categories = ["studynotes-3_network"]
+++

# 045. 진폭 편이 변조 (ASK - Amplitude Shift Keying)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ASK(Amplitude Shift Keying)는 반송파의 진폭을 디지털 데이터에 따라 이산적으로 변화시키는 변조 방식으로, 가장 단순한 디지털 변조 기법이며 OOK(On-Off Keying)가 대표적 구현입니다.
> 2. **가치**: 구현의 단순성, 낮은 전력 소비, 저렴한 비용으로 인해 광통신, RFID, 적외선 통신, 센서 네트워크 등 전력 및 비용 제약 환경에서 널리 활용됩니다.
> 3. **융합**: 현대 광통신의 intensity modulation, Li-Fi 가시광 통신, 그리고 저전력 IoT 통신 프로토콜(Zigbee, BLE 일부 모드)의 기반 기술로 진화하여 활용되고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

진폭 편이 변조(Amplitude Shift Keying, ASK)는 **반송파의 진폭(Amplitude)을 디지털 신호의 0과 1에 따라 변화시키는** 가장 기본적인 디지털 변조 방식입니다. 이는 아날로그 진폭 변조(AM)의 디지털 버전이라고 이해할 수 있습니다.

### ASK의 기본 정의

**수학적 표현**:
```
s(t) = A_m(t) · cos(2πf_c·t)

여기서:
- A_m(t): 변조 신호에 의한 진폭 (이산적)
- f_c: 반송파 주파수

이진 ASK (Binary ASK / OOK):
- 비트 1: s(t) = A·cos(2πf_c·t)  (반송파 ON)
- 비트 0: s(t) = 0                (반송파 OFF)
```

### ASK의 종류

| 종류 | 심볼 수 | 진폭 레벨 | 심볼당 비트 | 응용 분야 |
|------|--------|----------|------------|----------|
| **OOK** | 2 | 0, A | 1 | 광통신, RFID, IR 리모컨 |
| **2-ASK** | 2 | 0, A | 1 | 기본 ASK |
| **4-ASK** | 4 | 0, A/3, 2A/3, A | 2 | 고속 광통신 |
| **8-ASK** | 8 | 8 레벨 | 3 | 일부 유선 모뎀 |
| **M-ASK** | M | M 레벨 | log₂(M) | 이론적 일반화 |

**💡 비유**: ASK는 **'손전등 신호'**와 같습니다.
- 어둠 속에서 손전등을 켜고 끄는 것으로 메시지를 전달합니다.
- 손전등이 켜져 있으면(진폭=A) 1, 꺼져 있으면(진폭=0) 0입니다.
- 손전등의 밝기를 여러 단계로 조절하면 M-ASK가 됩니다 (밝음=11, 중간=10, 어두움=01, 꺼짐=00).
- 이 방식은 단순하지만, 다른 빛(잡음)이 있으면 구분하기 어렵습니다.

**등장 배경 및 발전 과정**:

1. **전신의 태동 (1830~1900년대)**:
   모스 부호는 사실상 가장 초기의 ASK/OOK 형태였습니다. 전신 키를 누르면 전류가 흐르고(1), 떼면 흐르지 않는(0) 방식입니다. 이 개념이 무선 통신으로 확장되었습니다.

2. **무선 전신 시대 (1900~1920년대)**:
   마르코니의 무선 전신은 스파크 갭 방식의 OOK를 사용했습니다. 단순하지만 효과적이었으며, 해상 통신에 혁명을 일으켰습니다.

3. **광통신으로의 확장 (1970년대~현재)**:
   광섬유 통신에서 레이저 다이오드를 켜고 끄는 방식의 Intensity Modulation은 본질적으로 OOK입니다. 수 Gbps의 고속 광통신도 기본 원리는 ASK입니다.

4. **현대적 응용**:
   RFID 태그, NFC, 적외선 리모컨, Li-Fi 등 전력 효율이 중요한 애플리케이션에서 ASK의 단순성이 재평가되고 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### ASK 변조기 구조

```ascii
================================================================================
[ ASK Modulator Architecture ]
================================================================================

                         +-------------+
   디지털 입력           |   레벨     |
   (비트 스트림)         |   변환기    |
   ============>-------->| (Level     |--------+
   1 0 1 1 0             |  Converter)|       |
                         +-------------+       |
                                               |
                    +--------------------------+
                    |
                    v
              +-------------+         +-------------+
              |   펄스     |         |  반송파     |
              |   성형     |-------->|   변조기    |
              |   필터     |         |  (Multiplier)|
              +-------------+         +------+------+
                                            ^
                                            |
              +-------------+               |
              |  반송파     |               |
              |  발진기     |---------------+
              | (OSC)       |   c(t) = cos(2πf_c·t)
              +-------------+
                                            |
                                            v
                                     +-------------+
                                     |  대역통과   |
                                     |  필터       |
                                     |  (BPF)      |
                                     +------+------+
                                            |
                                            v
                                     변조된 신호 s(t)

================================================================================
[ OOK Signal Generation ]
================================================================================

   입력 비트:     1     0     1     1     0     0     1
                  |     |     |     |     |     |     |
                  v     v     v     v     v     v     v

   레벨 매핑:    A     0     A     A     0     0     A

   반송파:       ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿

   OOK 출력:     ∿∿∿∿      ∿∿∿∿ ∿∿∿∿           ∿∿∿∿
                |<-1->|<-0->|<-1->|<-1->|<-0->|<-0->|<-1->|

   시간 ──────────────────────────────────────────────────>

   수학적 표현:
   s(t) = m(t) · cos(2πf_c·t)
   여기서 m(t) = A (비트 1), 0 (비트 0)

================================================================================
[ M-ASK Constellation Diagrams ]
================================================================================

   2-ASK (OOK)              4-ASK                  8-ASK

   Amplitude               Amplitude              Amplitude
       ^                       ^                      ^
       |                       |                      |
    A  |         *            A |         *        A  |         *
       |                       |       * *            |       * * * *
    0  | *                  2A/3|     *                |     * * * *
       |                       |                      |
       |                    A/3|   *                  |   * * * *
       |                       |                      |
       +---------->            +---------->           +---------->
                                0 | *                  0 | * * * *
                                  |                      |

   1 bit/symbol            2 bits/symbol          3 bits/symbol
   2 amplitude levels       4 amplitude levels     8 amplitude levels

================================================================================
[ ASK Demodulator: Envelope Detection ]
================================================================================

   수신 신호                    정류                   저역통과필터
   r(t) = s(t) + n(t)          (Rectifier)           (LPF)
         |                          |                     |
         v                          v                     v
    ∿∿∿∿   ∿∿∿∿ ∿∿∿∿        ∿∿∿∿   ∿∿∿∿ ∿∿∿∿       ___     ___ ___
                      ───>|  |  |   |  |  |  |───>|   |___|   |   |___
                                              |   |
                                              +---+
                                              |
                                              v
                                         판정기
                                      (Decision)
                                              |
                                              v
                                         디지털 출력
                                         1 0 1 1 0 0 1

   판정 임계값 (Threshold):
   - r > A/2 → 비트 1
   - r ≤ A/2 → 비트 0

================================================================================
```

### ASK의 성능 분석

#### 비트 에러율 (BER) 공식

```
이진 ASK (OOK)의 비트 에러율:

P_b = Q(√(E_b/N_0))

또는 코히어런트 검파의 경우:

P_b = (1/2)·erfc(√(E_b/(4N_0)))

여기서:
- E_b: 비트당 에너지
- N_0: 노이즈 전력 스펙트럼 밀도
- Q(x): Q-함수 (가우시안 확률)
- erfc(x): 상보 오차 함수

비교:
- BPSK: P_b = Q(√(2E_b/N_0))  ← 3dB 더 좋음
- ASK:  P_b = Q(√(E_b/N_0))
```

#### ASK의 장단점 분석

| 장점 | 단점 |
|------|------|
| 구현 매우 간단 | 잡음에 취약 (진폭 잡음 직접 영향) |
| 낮은 비용 | 낮은 스펙트럼 효율 |
| 저전력 소비 | 진폭 비선형성에 민감 |
| 대역폭 효율적 (OOK) | 다중 경로 페이딩에 취약 |
| 광통신에 적합 | 장거리 전송 부적합 |

### 심층 동작 원리: ASK 5단계 프로세스

1. **비트-심볼 매핑**:
   - 입력 비트 0 → 진폭 0 (또는 낮은 진폭)
   - 입력 비트 1 → 진폭 A (또는 높은 진폭)
   - M-ASK의 경우 log₂(M) 비트가 하나의 심볼로 매핑

2. **펄스 성형 (Pulse Shaping)**:
   - 직사각형 펄스는 무한 대역폭을 필요로 함
   - Raised Cosine, Gaussian 필터로 대역 제한
   - ISI(Intersymbol Interference) 방지

3. **반송파 변조**:
   - 베이스밴드 신호 m(t)와 반송파 c(t)의 곱
   - s(t) = m(t)·c(t) = m(t)·cos(2πf_c·t)
   - 스펙트럼이 f_c 주변으로 이동

4. **전송 및 채널**:
   - AWGN, 페이딩, 간섭 등 채널 효과
   - 수신 신호: r(t) = α·s(t-τ) + n(t)

5. **복조 및 검파**:
   - **비코히어런트**: 포락선 검파 (Envelope Detector)
   - **코히어런트**: 동기 검파 (Synchronous Detection)
   - 판정 회로가 0/1 결정

### 핵심 코드: ASK 변조/복조 시뮬레이터 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum

class DetectionType(Enum):
    """검파 방식"""
    COHERENT = "coherent"       # 동기 검파
    NON_COHERENT = "non_coherent"  # 비동기 검파 (포락선 검파)

@dataclass
class ASKConfig:
    """ASK 설정 파라미터"""
    carrier_freq: float = 10.0      # 반송파 주파수 (정규화)
    samples_per_bit: int = 100      # 비트당 샘플 수
    amplitude_high: float = 1.0     # 비트 1의 진폭
    amplitude_low: float = 0.0      # 비트 0의 진폭
    detection_type: DetectionType = DetectionType.NON_COHERENT

class ASKModulator:
    """ASK 변조기"""

    def __init__(self, config: ASKConfig):
        self.config = config

    def modulate(self, bits: List[int]) -> Tuple[np.ndarray, np.ndarray]:
        """
        비트 스트림을 ASK 신호로 변조

        Returns:
            (modulated_signal, time_array)
        """
        spb = self.config.samples_per_bit
        fc = self.config.carrier_freq
        n_bits = len(bits)
        n_samples = n_bits * spb

        # 시간 배열
        t = np.arange(n_samples) / spb

        # 반송파 생성
        carrier = np.cos(2 * np.pi * fc * t)

        # 비트를 진폭으로 매핑
        amplitude = np.zeros(n_samples)
        for i, bit in enumerate(bits):
            if bit == 1:
                amplitude[i*spb:(i+1)*spb] = self.config.amplitude_high
            else:
                amplitude[i*spb:(i+1)*spb] = self.config.amplitude_low

        # ASK 변조
        modulated = amplitude * carrier

        return modulated, t

    def modulate_m_ask(self, symbols: List[int], m: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        M-ASK 변조 (다중 레벨)

        Args:
            symbols: 심볼 값 (0 ~ M-1)
            m: 변조 차수 (2, 4, 8, ...)
        """
        spb = self.config.samples_per_bit
        fc = self.config.carrier_freq
        n_symbols = len(symbols)
        n_samples = n_symbols * spb

        t = np.arange(n_samples) / spb
        carrier = np.cos(2 * np.pi * fc * t)

        # 심볼을 균일한 진폭 레벨로 매핑
        levels = np.linspace(0, 1, m)  # 0, 1/(M-1), 2/(M-1), ..., 1

        amplitude = np.zeros(n_samples)
        for i, symbol in enumerate(symbols):
            amplitude[i*spb:(i+1)*spb] = levels[symbol]

        modulated = amplitude * carrier
        return modulated, t

class ASKDemodulator:
    """ASK 복조기"""

    def __init__(self, config: ASKConfig):
        self.config = config

    def demodulate_coherent(
        self,
        signal: np.ndarray
    ) -> Tuple[List[int], np.ndarray]:
        """
        동기 검파 (Coherent Detection)
        반송파 위상이 정확히 일치해야 함
        """
        spb = self.config.samples_per_bit
        fc = self.config.carrier_freq
        n_samples = len(signal)
        n_bits = n_samples // spb

        # 국부 반송파 생성 (위상이 정확히 일치해야 함)
        t = np.arange(n_samples) / spb
        local_carrier = np.cos(2 * np.pi * fc * t)

        # 동기 검파: 반송파와 곱한 후 저역 통과
        multiplied = signal * local_carrier * 2  # *2는 진폭 복원

        # 적분 (저역 통과 필터 역할)
        detected = np.zeros(n_bits)
        for i in range(n_bits):
            detected[i] = np.mean(multiplied[i*spb:(i+1)*spb])

        # 판정
        threshold = (self.config.amplitude_high + self.config.amplitude_low) / 2
        bits = [1 if d > threshold else 0 for d in detected]

        return bits, detected

    def demodulate_non_coherent(
        self,
        signal: np.ndarray
    ) -> Tuple[List[int], np.ndarray]:
        """
        비동기 검파 (Non-Coherent / Envelope Detection)
        반송파 위상 정보 불필요
        """
        spb = self.config.samples_per_bit
        n_samples = len(signal)
        n_bits = n_samples // spb

        # 포락선 검파: 힐버트 변환 사용
        analytic_signal = signal + 1j * np.imag(np.fft.ifft(
            np.fft.fft(signal) * 2 * np.heaviside(np.arange(n_samples) - n_samples//2, 0.5)
        ))
        envelope = np.abs(analytic_signal)

        # 각 비트 구간에서 평균
        detected = np.zeros(n_bits)
        for i in range(n_bits):
            detected[i] = np.mean(envelope[i*spb:(i+1)*spb])

        # 판정
        threshold = (self.config.amplitude_high + self.config.amplitude_low) / 2
        bits = [1 if d > threshold else 0 for d in detected]

        return bits, detected

    def demodulate(self, signal: np.ndarray) -> Tuple[List[int], np.ndarray]:
        """설정에 따른 복조 방식 선택"""
        if self.config.detection_type == DetectionType.COHERENT:
            return self.demodulate_coherent(signal)
        else:
            return self.demodulate_non_coherent(signal)

class AWGNChannel:
    """AWGN 채널 시뮬레이터"""

    def __init__(self, snr_db: float):
        self.snr_db = snr_db

    def transmit(self, signal: np.ndarray) -> np.ndarray:
        """신호에 AWGN 잡음 추가"""
        snr_linear = 10 ** (self.snr_db / 10)
        signal_power = np.mean(signal ** 2)
        noise_power = signal_power / snr_linear

        noise = np.sqrt(noise_power) * np.random.randn(len(signal))
        return signal + noise

class ASKAnalyzer:
    """ASK 성능 분석기"""

    def __init__(self, config: ASKConfig):
        self.config = config
        self.modulator = ASKModulator(config)
        self.demodulator = ASKDemodulator(config)

    def calculate_ber(self, original: List[int], decoded: List[int]) -> float:
        """비트 에러율 계산"""
        min_len = min(len(original), len(decoded))
        errors = sum(1 for i in range(min_len) if original[i] != decoded[i])
        return errors / min_len if min_len > 0 else 0.0

    def simulate_ber_vs_snr(
        self,
        bits: List[int],
        snr_range: np.ndarray,
        num_trials: int = 10
    ) -> np.ndarray:
        """SNR 대비 BER 시뮬레이션"""
        ber_results = []

        for snr_db in snr_range:
            channel = AWGNChannel(snr_db)
            ber_sum = 0

            for _ in range(num_trials):
                # 변조
                modulated, _ = self.modulator.modulate(bits)

                # 채널 통과
                noisy = channel.transmit(modulated)

                # 복조
                decoded, _ = self.demodulator.demodulate(noisy)

                # BER 계산
                ber_sum += self.calculate_ber(bits, decoded)

            ber_results.append(ber_sum / num_trials)

        return np.array(ber_results)

    def theoretical_ber(self, snr_db: np.ndarray) -> np.ndarray:
        """이론적 BER 곡선"""
        snr_linear = 10 ** (snr_db / 10)

        if self.config.detection_type == DetectionType.COHERENT:
            # 코히어런트 ASK: P_b = Q(sqrt(E_b/N_0))
            # 근사: 0.5 * erfc(sqrt(E_b/(4*N_0)))
            from scipy import special
            return 0.5 * special.erfc(np.sqrt(snr_linear / 4))
        else:
            # 비코히어런트 ASK (근사)
            # 더 복잡한 공식, 간소화하여 표현
            from scipy import special
            return 0.5 * np.exp(-snr_linear / 4)

def run_ask_simulation():
    """ASK 시뮬레이션 실행"""
    np.random.seed(42)

    # 테스트 데이터 생성
    test_bits = [int(b) for b in np.random.randint(0, 2, 1000)]

    print("=" * 70)
    print("ASK (Amplitude Shift Keying) 시뮬레이션")
    print("=" * 70)

    # 비동기 검파 (Non-Coherent)
    config_nc = ASKConfig(detection_type=DetectionType.NON_COHERENT)
    analyzer_nc = ASKAnalyzer(config_nc)

    # 동기 검파 (Coherent)
    config_c = ASKConfig(detection_type=DetectionType.COHERENT)
    analyzer_c = ASKAnalyzer(config_c)

    # SNR 범위 설정
    snr_range = np.arange(0, 20, 2)

    # BER 시뮬레이션
    ber_nc = analyzer_nc.simulate_ber_vs_snr(test_bits, snr_range)
    ber_c = analyzer_c.simulate_ber_vs_snr(test_bits, snr_range)

    print("\nSNR vs BER 결과:")
    print("-" * 50)
    print(f"{'SNR (dB)':<12} {'Non-Coherent':<15} {'Coherent':<15}")
    print("-" * 50)

    for i, snr in enumerate(snr_range):
        print(f"{snr:<12.1f} {ber_nc[i]:<15.6f} {ber_c[i]:<15.6f}")

    print("\n" + "=" * 70)
    print("결과 해석:")
    print("- 동기 검파(Coherent)가 비동기 검파보다 약 1-2dB 우수")
    print("- ASK는 BPSK보다 약 3dB 열등한 BER 성능")
    print("- 간단한 구현이 장점이지만 잡음에 취약")
    print("=" * 70)

if __name__ == "__main__":
    run_ask_simulation()
