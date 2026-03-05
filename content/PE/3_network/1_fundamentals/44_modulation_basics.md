+++
title = "044. 변조 (Modulation) 개요 및 필요성"
description = "데이터통신에서 변조의 정의, 필요성, 기본 원리, 그리고 다양한 변조 방식의 기초를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["Modulation", "CarrierWave", "ASK", "FSK", "PSK", "QAM", "Wireless", "Analog"]
categories = ["studynotes-3_network"]
+++

# 044. 변조 (Modulation) 개요 및 필요성

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 변조(Modulation)는 정보를 담은 기저대역 신호(Baseband Signal)를 반송파(Carrier Wave)에 실어 전송 가능한 대역통과 신호(Bandpass Signal)로 변환하는 과정으로, 신호의 주파수, 진폭, 위상 중 하나 이상을 제어하여 정보를 인코딩합니다.
> 2. **가치**: 변조는 안테나 크기 최적화, 주파수 분할 다중화(FDM), 전파 전달 특성 활용, 잡음 내성 향상 등 데이터통신의 핵심 기술적 난제를 해결하여 무선 및 유선 통신을 가능하게 합니다.
> 3. **융합**: 5G/6G의 1024-QAM, Wi-Fi 7의 4096-QAM, 위성통신의 QPSK, 광통신의 CO-OFDM 등 현대 통신 시스템의 스펙트럼 효율과 성능은 고도화된 변조 기술에 의해 결정됩니다.

---

## Ⅰ. 개요 (Context & Background)

변조(Modulation)는 **저주파 정보 신호를 고주파 반송파에 실어 전송하는 과정**입니다. 이는 데이터통신에서 가장 근본적이면서도 중요한 신호 처리 기술 중 하나입니다.

### 변조의 정의

**수학적 정의**:
```
반송파(Carrier): c(t) = A·cos(2πf_c·t + φ)

변조된 신호: s(t) = A(t)·cos(2πf_c·t + φ(t))

여기서:
- A(t): 시간에 따라 변하는 진폭 (ASK/AM)
- f_c: 반송파 주파수
- φ(t): 시간에 따라 변하는 위상 (PSK/PM)
- 주파수 변조 시: cos(2π·∫f(t)dt + φ)
```

### 변조의 핵심 필요성 4가지

| 필요성 | 문제 상황 | 변조에 의한 해결 | 실제 적용 |
|--------|----------|-----------------|----------|
| **안테나 크기** | 저주파는 안테나가 수 km 필요 | 고주파 사용으로 안테나 cm 단위로 축소 | 스마트폰 안테나 |
| **다중화** | 여러 신호가 동시에 충돌 | 주파수별 분리 (FDM) | 라디오, TV 채널 |
| **전파 전달** | 저주파는 전리층 투과/흡수 | 적절한 주파수 대역 선택 | 단파, 마이크로파 |
| **잡음 내성** | 기저대역은 잡음에 취약 | 변조로 SNR 개선 | FM의 잡음 제거 |

**💡 비유**: 변조는 **'택배 포장과 배송'** 과정과 같습니다.
- **정보 신호(Baseband)**는 보내려는 편지나 물건입니다.
- **반송파(Carrier)**는 택배 트럭입니다. 트럭 없이 물건을 도로에 던져놓으면 목적지까지 갈 수 없습니다.
- **변조 과정**은 물건을 트럭에 싣는 것입니다. 트럭의 종류(주파수)에 따라 갈 수 있는 곳이 다릅니다.
- **다중화(FDM)**는 여러 물건을 다른 트럭에 나눠 싣는 것입니다. 모든 물건을 한 트럭에 넣으면 섞여버립니다.

**등장 배경 및 발전 과정**:

1. **무선 통신의 태동 (1900년대 초)**:
   마르코니의 무선 전신은 스파크 갭(Spark Gap) 방식으로 넓은 대역폭을 차지했습니다. 여러 국국이 동시에 송신하면 간섭이 심각했습니다. 이를 해결하기 위해 연속파(Continuous Wave)와 정현파 반송파를 사용하는 현대적 변조 기술이 개발되었습니다.

2. **아날로그 변조의 황금기 (1920~1960년대)**:
   AM(Amplitude Modulation) 라디오 방송(1920년), FM(Frequency Modulation) 방송(1933년)이 상용화되었습니다. 이 시기에 변조 이론이 확립되었고, 스펙트럼 효율과 잡음 특성 분석이 체계화되었습니다.

3. **디지털 변조의 등장 (1960~1990년대)**:
   컴퓨터 통신의 발전과 함께 디지털 데이터를 효율적으로 전송하는 디지털 변조(ASK, FSK, PSK, QAM)가 개발되었습니다. 모뎀 기술의 진화(300bps → 56Kbps)는 변조 기술 발전의 역사였습니다.

4. **고차 변조와 적응형 변조 (2000년대~현재)**:
   스펙트럼 효율을 극대화하기 위해 64-QAM, 256-QAM, 1024-QAM 등 고차 변조가 도입되었습니다. 채널 상태에 따라 동적으로 변조 방식을 변경하는 적응형 변조(Adaptive Modulation)가 4G/5G의 핵심 기술이 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 변조 방식 분류 체계

```ascii
================================================================================
[ Modulation Taxonomy ]
================================================================================

                         변조 (Modulation)
                               |
          +--------------------+--------------------+
          |                                         |
    아날로그 변조                              디지털 변조
    (Analog Modulation)                    (Digital Modulation)
          |                                         |
    +-----+-----+                           +-------+-------+
    |           |                           |               |
   진폭        각도                        키잉            ASK
   (AM)      (각변조)                   (Shift Keying)     |
             |     |                         |             FSK
            주파수 위상                    +--+--+          |
            (FM)  (PM)                     |     |        PSK
                                          선형   비선형    |
                                         (Linear)(Non-linear)
                                           |        |     QAM
                                        ASK/PSK   FSK/MSK   |
                                                                   OFDM
================================================================================
```

### 기본 변조 방식 상세 분석

| 변조 방식 | 제어 파라미터 | 수학적 표현 | 심볼당 비트 | 스펙트럼 효율 | 잡음 내성 |
|----------|-------------|-------------|------------|-------------|----------|
| **ASK** | 진폭 | A·cos(ω_c·t) | 1 (OOK) | 낮음 | 낮음 |
| **BFSK** | 주파수 | cos(ω_1·t) or cos(ω_2·t) | 1 | 중간 | 높음 |
| **BPSK** | 위상 | cos(ω_c·t) or -cos(ω_c·t) | 1 | 낮음 | 매우 높음 |
| **QPSK** | 위상 | cos(ω_c·t + π/4·n) | 2 | 중간 | 높음 |
| **8-PSK** | 위상 | 8개 위상 상태 | 3 | 높음 | 중간 |
| **16-QAM** | 진폭+위상 | 16개 성상도 점 | 4 | 높음 | 중간 |
| **64-QAM** | 진폭+위상 | 64개 성상도 점 | 6 | 매우 높음 | 낮음 |
| **256-QAM** | 진폭+위상 | 256개 성상도 점 | 8 | 극히 높음 | 낮음 |

### 정교한 구조 다이어그램: 변조 시스템 아키텍처

```ascii
================================================================================
[ Modulation System Architecture ]
================================================================================

[ 송신측 (Transmitter) ]                                    [ 수신측 (Receiver) ]

+-------------+     +-------------+     +-------------+     +-------------+
| 정보원      |     | 디지털      |     | 변조기      |     | 전력        |
| (Source)    |---->| - 채널코딩  |---->| (Modulator) |---->| 증폭기      |
|             |     | - 심볼매핑  |     |             |     | (PA)        |
+-------------+     +-------------+     +-------------+     +------+------+
                                                                   |
                                                                   v
+-------------+     +-------------+     +-------------+     +-------------+
| 정보 싱크    |     | 디지털      |     | 복조기      |     | 대역통과    |
| (Sink)      |<----| - 심볼검출  |<----| (Demodulator)|<----| 필터        |
|             |     | - 채널디코딩|     |             |     | (BPF)       |
+-------------+     +-------------+     +-------------+     +------+------+
                                                                   |
                                                                   v
                    +-------------------------------------------+
                    |              전송 매체                      |
                    |  +------+  +------+  +------+  +------+   |
                    |  |잡음  |  |페이딩|  |간섭  |  |감쇠  |   |
                    |  +------+  +------+  +------+  +------+   |
                    +-------------------------------------------+

================================================================================
[ Modulation Process: Time Domain View ]
================================================================================

[1] 디지털 입력 (비트 스트림)
    1  0  1  1  0  0  1  0
    |--||--||--||--||--||--|
    B1  B2  B3  B4  B5  B6

[2] 심볼 매핑 (QPSK 예시: 2비트 → 1심볼)
    B1,B2 → 10 → 위상 270° (−j)
    B3,B4 → 11 → 위상 315° (−1−j)/√2
    B5,B6 → 01 → 위상 90°  (+j)

[3] 반송파 변조 (I/Q 변조)
           I축                           Q축
            ^                             ^
            |        * (11)               |     * (01)
      ------+------>                ------+------>
            |    * (10)                   |
            |                             |

[4] 변조된 신호 (시간 영역)

    s(t) = √(E_s)·cos(2πf_c·t + φ_k)

    진폭은 일정, 위상이 심볼마다 변화

    +V  ┐     ┌──┐        ┐     ┌──┐
        │     │  │        │     │  │
    0   ├───┐│  │┌───┐    ├───┐│  │┌───
        │   ││  ││   │    │   ││  ││
    -V  ┘   └┘  └┘   ┘    ┘   └┘  └┘

        |<- symbol ->|<- symbol ->|
             φ=270°        φ=90°

================================================================================
[ Constellation Diagram: BPSK → QPSK → 16-QAM ]
================================================================================

    BPSK (1 bit/symbol)      QPSK (2 bits/symbol)    16-QAM (4 bits/symbol)

          Q                            Q                           Q
          ^                            ^                           ^
          |                            |     1001 *  1011 *        |
    ------+------> I             ------+------> I            ------+------> I
          |                            |     1000 *  1010 *        |
        * | *                        * | *                       * | *
          | 0                          |                         0001* 0011*
          |                          01* | *11                      |
        * | *                        00* | *10                    0000* 0010*
          |                            |                           |
          |                            |     0101 *  0111 *        |
          |                            |     0100 *  0110 *        |
          v                            v                           v

    2개 점 = 1비트           4개 점 = 2비트            16개 점 = 4비트
    최고 잡음 내성           높은 잡음 내성            중간 잡음 내성

================================================================================
```

### 심층 동작 원리: 변조의 4단계 프로세스

#### 1단계: 디지털 데이터 → 심볼 매핑

```
입력 비트 스트림: 10110010...

심볼 크기 M=4 (QPSK)인 경우:
- 2비트씩 그룹화: 10 | 11 | 00 | 10
- 각 그룹을 심볼에 매핑:
  00 → s_0 = (1+j)/√2   (45°)
  01 → s_1 = (-1+j)/√2  (135°)
  11 → s_2 = (-1-j)/√2  (225°)
  10 → s_3 = (1-j)/√2   (315°)
```

#### 2단계: I/Q 성분 분리

```
심볼 s_k = I_k + j·Q_k

QPSK 예시:
s_3 = (1-j)/√2
I_3 = 1/√2 (동상 성분)
Q_3 = -1/√2 (직교 성분)

I축: cos(ω_c·t)와 곱해짐
Q축: -sin(ω_c·t)와 곱해짐 (90° 위상 천이)
```

#### 3단계: 반송파 변조

```
s(t) = I(t)·cos(2πf_c·t) - Q(t)·sin(2πf_c·t)

      = √(I²+Q²)·cos(2πf_c·t + arctan(Q/I))

QPSK s_3의 경우:
s(t) = √(1/2 + 1/2)·cos(2πf_c·t - π/4)
     = cos(2πf_c·t - π/4)
     = cos(2πf_c·t + 315°)
```

#### 4단계: 대역 제한 및 전송

```
펄스 성형 필터 (Pulse Shaping Filter):
- Raised Cosine 필터 (롤오프 팩터 α)
- ISI(Inter-Symbol Interference) 방지
- 대역폭 = (1+α)·R_s (R_s: 심볼 레이트)

예: R_s = 1 Msps, α = 0.5
    대역폭 = 1.5 MHz
```

### 핵심 코드: 다양한 변조 방식 구현 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from enum import Enum
from dataclasses import dataclass

class ModulationType(Enum):
    """변조 방식 열거형"""
    ASK = "ASK"
    BPSK = "BPSK"
    QPSK = "QPSK"
    QAM16 = "16-QAM"

@dataclass
class ModulationParams:
    """변조 파라미터"""
    modulation_type: ModulationType
    samples_per_symbol: int = 100
    carrier_freq: float = 10.0  # 정규화 주파수

class Modulator:
    """디지털 변조기 구현"""

    def __init__(self, params: ModulationParams):
        self.params = params
        self.constellation = self._generate_constellation()

    def _generate_constellation(self) -> np.ndarray:
        """성상도(Constellation) 생성"""
        mod_type = self.params.modulation_type

        if mod_type == ModulationType.ASK:
            # OOK (On-Off Keying)
            return np.array([0, 1])

        elif mod_type == ModulationType.BPSK:
            # Binary PSK: 0°, 180°
            return np.array([1+0j, -1+0j])

        elif mod_type == ModulationType.QPSK:
            # QPSK: 45°, 135°, 225°, 315° (Gray coding)
            return np.array([
                1+1j,   # 00
                -1+1j,  # 01
                -1-1j,  # 11
                1-1j    # 10
            ]) / np.sqrt(2)

        elif mod_type == ModulationType.QAM16:
            # 16-QAM 성상도
            points = []
            for i in [-3, -1, 1, 3]:
                for q in [-3, -1, 1, 3]:
                    points.append(complex(i, q))
            return np.array(points) / np.sqrt(10)  # 정규화

        else:
            raise ValueError(f"지원하지 않는 변조 방식: {mod_type}")

    def bits_to_symbols(self, bits: List[int]) -> np.ndarray:
        """비트를 심볼로 변환"""
        mod_type = self.params.modulation_type

        if mod_type == ModulationType.ASK:
            # 1비트 → 1심볼
            symbols = np.array([self.constellation[b] for b in bits])

        elif mod_type == ModulationType.BPSK:
            # 1비트 → 1심볼
            symbols = np.array([self.constellation[b] for b in bits])

        elif mod_type == ModulationType.QPSK:
            # 2비트 → 1심볼
            symbols = []
            for i in range(0, len(bits), 2):
                if i + 1 < len(bits):
                    idx = bits[i] * 2 + bits[i+1]
                    symbols.append(self.constellation[idx])
            symbols = np.array(symbols)

        elif mod_type == ModulationType.QAM16:
            # 4비트 → 1심볼
            symbols = []
            for i in range(0, len(bits), 4):
                if i + 3 < len(bits):
                    idx = bits[i]*8 + bits[i+1]*4 + bits[i+2]*2 + bits[i+3]
                    symbols.append(self.constellation[idx])
            symbols = np.array(symbols)

        return symbols

    def modulate(self, symbols: np.ndarray) -> np.ndarray:
        """심볼을 변조된 신호로 변환"""
        sps = self.params.samples_per_symbol
        fc = self.params.carrier_freq
        n_symbols = len(symbols)
        n_samples = n_symbols * sps

        t = np.arange(n_samples) / sps

        # 반송파 생성
        carrier_i = np.cos(2 * np.pi * fc * t)
        carrier_q = -np.sin(2 * np.pi * fc * t)

        # 심볼 업샘플링
        upsampled_i = np.zeros(n_samples)
        upsampled_q = np.zeros(n_samples)

        for i, symbol in enumerate(symbols):
            upsampled_i[i*sps:(i+1)*sps] = symbol.real
            upsampled_q[i*sps:(i+1)*sps] = symbol.imag

        # I/Q 변조
        modulated = upsampled_i * carrier_i + upsampled_q * carrier_q

        return modulated, t

    def demodulate(self, signal: np.ndarray) -> np.ndarray:
        """수신 신호를 심볼로 복원"""
        sps = self.params.samples_per_symbol
        fc = self.params.carrier_freq
        n_samples = len(signal)
        n_symbols = n_samples // sps

        t = np.arange(n_samples) / sps

        # 국부 발진기 (Local Oscillator)
        carrier_i = np.cos(2 * np.pi * fc * t)
        carrier_q = -np.sin(2 * np.pi * fc * t)

        # 코히어런트 검파
        i_demod = signal * carrier_i
        q_demod = signal * carrier_q

        # 저역 통과 필터링 (적분)
        symbols_i = np.zeros(n_symbols, dtype=complex)
        for i in range(n_symbols):
            start = i * sps
            end = (i + 1) * sps
            symbols_i[i] = np.mean(i_demod[start:end]) + 1j * np.mean(q_demod[start:end])

        return symbols_i

    def symbols_to_bits(self, symbols: np.ndarray) -> List[int]:
        """심볼을 비트로 복원"""
        bits = []
        constellation = self.constellation
        mod_type = self.params.modulation_type

        for symbol in symbols:
            # 최근접 성상도 점 탐색 (Minimum Distance Detection)
            distances = np.abs(constellation - symbol)
            nearest_idx = np.argmin(distances)

            if mod_type == ModulationType.ASK:
                bits.append(nearest_idx)
            elif mod_type == ModulationType.BPSK:
                bits.append(nearest_idx)
            elif mod_type == ModulationType.QPSK:
                # 2비트 디코딩
                bits.extend([nearest_idx // 2, nearest_idx % 2])
            elif mod_type == ModulationType.QAM16:
                # 4비트 디코딩
                bits.extend([
                    (nearest_idx >> 3) & 1,
                    (nearest_idx >> 2) & 1,
                    (nearest_idx >> 1) & 1,
                    nearest_idx & 1
                ])

        return bits

    def calculate_ber(
        self,
        original_bits: List[int],
        decoded_bits: List[int]
    ) -> float:
        """비트 에러율(BER) 계산"""
        min_len = min(len(original_bits), len(decoded_bits))
        errors = sum(1 for i in range(min_len) if original_bits[i] != decoded_bits[i])
        return errors / min_len if min_len > 0 else 0.0

    def calculate_spectral_efficiency(self) -> float:
        """스펙트럼 효율 계산 (bits/s/Hz)"""
        mod_type = self.params.modulation_type

        efficiency_map = {
            ModulationType.ASK: 0.5,    # 이론적 최대
            ModulationType.BPSK: 1.0,
            ModulationType.QPSK: 2.0,
            ModulationType.QAM16: 4.0
        }

        return efficiency_map.get(mod_type, 0.0)

class AWGNChannel:
    """AWGN (Additive White Gaussian Noise) 채널"""

    def __init__(self, snr_db: float):
        self.snr_db = snr_db

    def add_noise(self, signal: np.ndarray) -> np.ndarray:
        """신호에 잡음 추가"""
        snr_linear = 10 ** (self.snr_db / 10)
        signal_power = np.mean(np.abs(signal) ** 2)
        noise_power = signal_power / snr_linear

        noise = np.sqrt(noise_power / 2) * (
            np.random.randn(len(signal)) + 1j * np.random.randn(len(signal))
        )

        return signal + noise.real  # 실수 신호인 경우

def run_modulation_demo():
    """변조 데모 실행"""
    # 테스트 비트 생성
    np.random.seed(42)
    test_bits = [int(b) for b in np.random.randint(0, 2, 32)]

    print("=" * 70)
    print("디지털 변조 시스템 데모")
    print("=" * 70)

    for mod_type in [ModulationType.BPSK, ModulationType.QPSK, ModulationType.QAM16]:
        print(f"\n--- {mod_type.value} ---")

        # 변조기 생성
        params = ModulationParams(modulation_type=mod_type)
        modulator = Modulator(params)

        # 변조
        symbols = modulator.bits_to_symbols(test_bits)
        modulated, t = modulator.modulate(symbols)

        # 채널 통과 (AWGN)
        channel = AWGNChannel(snr_db=20)
        noisy_signal = channel.add_noise(modulated)

        # 복조
        decoded_symbols = modulator.demodulate(noisy_signal)
        decoded_bits = modulator.symbols_to_bits(decoded_symbols)

        # 성능 평가
        ber = modulator.calculate_ber(test_bits, decoded_bits)
        spectral_eff = modulator.calculate_spectral_efficiency()

        print(f"입력 비트 수: {len(test_bits)}")
        print(f"심볼 수: {len(symbols)}")
        print(f"스펙트럼 효율: {spectral_eff} bits/s/Hz")
        print(f"BER (SNR=20dB): {ber:.6f}")
        print(f"성상도 크기: {len(modulator.constellation)} 점")

if __name__ == "__main__":
    run_modulation_demo()
