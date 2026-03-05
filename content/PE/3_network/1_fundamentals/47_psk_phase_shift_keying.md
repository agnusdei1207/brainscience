+++
title = "047. 위상 편이 변조 (PSK - Phase Shift Keying)"
description = "디지털 변조 기법인 PSK의 원리, 종류(BPSK, QPSK, 8-PSK), 성상도, 장단점, 그리고 위성통신, WiFi, 5G 등 실무 응용을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["PSK", "BPSK", "QPSK", "PhaseShiftKeying", "Constellation", "CoherentDetection", "Satellite"]
categories = ["studynotes-3_network"]
+++

# 047. 위상 편이 변조 (PSK - Phase Shift Keying)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PSK(Phase Shift Keying)는 반송파의 위상(Phase)을 디지털 데이터에 따라 이산적으로 변화시키는 변조 방식으로, 일정한 진폭(Constant Envelope)을 유지하며 높은 전력 효율과 잡음 내성을 동시에 제공합니다.
> 2. **가치**: BPSK(1bit/symbol)에서 QPSK(2bit/symbol), 8-PSK(3bit/symbol)로 확장하며 스펙트럼 효율을 높일 수 있고, 위성통신, WiFi(802.11), 블루투스, RFID 등 핵심 무선 기술의 기반이 됩니다.
> 3. **융합**: QAM(Quadrature Amplitude Modulation)의 위상 성분으로 진화하여 5G NR의 256-QAM, WiFi 6의 1024-QAM 등 초고속 무선 통신의 기초가 되며, CO-OFDM 광통신에도 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

위상 편이 변조(Phase Shift Keying, PSK)는 **반송파의 위상(Phase)을 디지털 신호의 값에 따라 변화시키는** 디지털 변조 방식입니다. 위상은 0°에서 360°까지의 값을 가질 수 있으며, 이를 이산적인 값으로 나누어 데이터를 표현합니다.

### PSK의 기본 정의

**수학적 표현**:
```
s(t) = A·cos(2πf_c·t + φ_k)

여기서:
- φ_k: 심볼 k에 해당하는 위상
- A: 일정한 진폭
- f_c: 반송파 주파수

BPSK:
- 비트 0: s(t) = A·cos(2πf_c·t + 0°)
- 비트 1: s(t) = A·cos(2πf_c·t + 180°)

QPSK:
- 00: s(t) = A·cos(2πf_c·t + 45°)
- 01: s(t) = A·cos(2πf_c·t + 135°)
- 11: s(t) = A·cos(2πf_c·t + 225°)
- 10: s(t) = A·cos(2πf_c·t + 315°)
```

### PSK의 종류

| 종류 | 위상 상태 | 심볼당 비트 | 성상도 점 | 스펙트럼 효율 | 주요 응용 |
|------|----------|------------|----------|-------------|----------|
| **BPSK** | 2 (0°, 180°) | 1 | 2 | 1 bps/Hz | RFID, GPS |
| **QPSK** | 4 (45° 간격) | 2 | 4 | 2 bps/Hz | 위성, WiFi |
| **OQPSK** | 4 (Offset) | 2 | 4 | 2 bps/Hz | CDMA, Zigbee |
| **π/4-DQPSK** | 4 (Differential) | 2 | 8 위치 | 2 bps/Hz | GSM, TETRA |
| **8-PSK** | 8 (45° 간격) | 3 | 8 | 3 bps/Hz | EDGE, 위성 |
| **16-PSK** | 16 (22.5° 간격) | 4 | 16 | 4 bps/Hz | 거의 사용 안함 |

**💡 비유**: PSK는 **'시계 바늘 위치'**와 같습니다.
- 시계 바늘이 12시(0°)를 가리키면 0, 6시(180°)를 가리키면 1입니다. 이것이 BPSK입니다.
- 12시, 3시, 6시, 9시를 사용하면 2비트(00, 01, 11, 10)를 표현할 수 있습니다. 이것이 QPSK입니다.
- 시계를 더 세분화하여 8개 위치를 사용하면 3비트를 표현할 수 있습니다 (8-PSK).
- 바늘 길이(진폭)는 항상 일정하므로 전력 효율이 좋습니다.

**등장 배경 및 발전 과정**:

1. **우주 통신의 요구 (1960년대)**:
   초기 위성 통신과 심우주 통신에서는 전력이 귀한 자원이었습니다. BPSK는 동일 BER을 달성하기 위해 FSK보다 3dB, ASK보다 6dB 적은 전력을 필요로 하여 우주 통신의 표준이 되었습니다.

2. **스펙트럼 효율의 요구 (1970~80년대)**:
   주파수 자원이 부족해지면서 BPSK의 1 bit/symbol으로는 부족했습니다. QPSK(2 bits/symbol), 8-PSK(3 bits/symbol)가 개발되어 같은 대역폭에 더 많은 데이터를 전송할 수 있게 되었습니다.

3. **디지털 이동통신 (1990~2000년대)**:
   GSM은 GMSK를 사용했지만, EDGE(Enhanced Data rates for GSM Evolution)는 8-PSK를 도입하여 3배 속도 향상을 달성했습니다. WiFi 802.11b는 BPSK/QPSK, 802.11a/g는 16/64-QAM(PSK 기반)을 사용합니다.

4. **현대 통신 시스템**:
   5G NR, WiFi 6/7, 위성 인터넷(Starlink) 등은 QAM의 위상 성분으로 PSK 개념을 계승하고 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### PSK 변조기 구조

```ascii
================================================================================
[ PSK Modulator Architecture: I/Q Modulation ]
================================================================================

   비트 스트림                          직렬-병렬 변환
   ============>                       (Serial-to-Parallel)
   b_0 b_1 b_2 b_3 ...                      |
         |                                  v
         |                          +-------+-------+
         |                          |       |       |
         |                          |  I    |  Q    |
         |                          |  비트  |  비트  |
         |                          +-------+-------+
         |                              |       |
         v                              v       v
   +-------------+              +-------------+ +-------------+
   | 심볼 매핑   |              | 레벨 변환   | | 레벨 변환   |
   | (Gray Code)|              | +1/-1       | | +1/-1       |
   +------+------+              +------+------+ +------+------+
          |                            |               |
          v                            v               v
   +-------------+              +-------------+ +-------------+
   | I/Q 성분    |              | 펄스 성형   | | 펄스 성형   |
   | 분리        |              | 필터        | | 필터        |
   +------+------+              +------+------+ +------+------+
          |                            |               |
          |                            v               v
          |                     +------+------+ +------+------+
          |                     | × cos(ω_c·t) | | × -sin(ω_c·t)|
          |                     +------+------+ +------+------+
          |                            |               |
          |                            +-------+-------+
          |                                    |
          v                                    v
   +-------------+                     +-------------+
   | 변조된 신호  |<--------------------|    SUM      |
   | s(t)        |                     +-------------+
   +-------------+

   수학적 표현:
   s(t) = I(t)·cos(2πf_c·t) - Q(t)·sin(2πf_c·t)

   QPSK의 경우:
   I(t), Q(t) ∈ {+1/√2, -1/√2}

================================================================================
[ PSK Constellation Diagrams ]
================================================================================

   BPSK (1 bit/symbol)         QPSK (2 bits/symbol)

        Q                              Q
        ^                              ^
        |                              |
   ------+------> I               01 * + * 11   (Gray Coding)
        |                          \   |   /
        |                           \  |  /
      * | * (0°,180°)              00 * + * 10
        |                              / | \
        |                             /  |  \
        v                            00 *   * 10
                                     01 *   * 11
                                     00 * + * 10   <-- Wait, let me fix
                                         |
        두 점이 180° 떨어짐              v

   정정된 QPSK:
        Q
        ^
        |      * 01 (135°)
        |     / \
   00 * + - + - + - * 10 (315°)
   (180°)|     \ /
        |      * 11 (225°)
        |
        +----------------> I
              * 00 (45°)

   8-PSK (3 bits/symbol)        16-PSK (4 bits/symbol)

        Q                              Q
        ^                              ^
        |                              |
   010 *     * 000                *   *   *   *
        |   / \                        \   /
   011 * +     + * 111               * * * * * *
        |  \   /                          |
   110 *   *   * 100                   * * * * * *
        |                              /   \
   101 *     * 001                    *   *   *   *
        |
        +---------> I                  +-----------> I

   8개 점, 45° 간격              16개 점, 22.5° 간격

================================================================================
[ PSK Signal Waveforms ]
================================================================================

   입력 비트:     0     1     0     0     1     1

   BPSK:
   위상:         0°   180°   0°    0°   180°  180°

   신호:
        ┐     ┌──┐        ┐     ┌──┐┌──┐
   A    │     │  │        │     │  ││  │
        │     │  │        │     │  ││  │
   0 ───┼───┐ │  │┌───┐   │   ┐ │  ││  │
        │   │ │  ││   │   │   │ │  ││  │
   -A   ┘   └─┘  └┘   ┘   └───┘ ┘  └┘  ┘

        |<0°->|<180>|<0°->|<0°->|<180>|<180>|

   QPSK (비트 쌍):
   입력:  01    11    00    10
   위상: 135°  225°   45°  315°

   I 성분: -1/√2, -1/√2, +1/√2, +1/√2
   Q 성분: +1/√2, -1/√2, +1/√2, -1/√2

================================================================================
[ PSK Coherent Demodulator ]
================================================================================

   수신 신호 r(t) = s(t) + n(t)

                    +-------------+
   r(t) ───────────>| 대역통과필터 |────+────────────────────+───>
                    +-------------+    |                    |
                                       v                    v
                    +-------------+  +------+          +------+
                    | 국부발진기   |->| × cos|          | × -sin|
                    | (LO) f_c,φ  |  +------+          +------+
                    +-------------+      |                  |
                                         v                  v
                    +-------------+  +------+          +------+
                    | 위상 동기    |  | LPF  |          | LPF  |
                    | (Carrier    |  +------+          +------+
                    | Recovery)   |      |                  |
                    +-------------+      v                  v
                                      +----+            +----+
                                      | I  |            | Q  |
                                      +----+            +----+
                                           \            /
                                            \          /
                                             \        /
                                              \      /
                                               \    /
                                                \  /
                                                 \/
                                              +-------+
                                              | 판정  |
                                              | 회로  |
                                              +---+---+
                                                  |
                                                  v
                                            디지털 출력
                                             00 01 10 11

   핵심: 위상 동기(Carrier Recovery)가 필수!
   - Costas Loop
   - Squaring Loop
   - Decision-Directed Loop

================================================================================
```

### PSK의 성능 분석

#### 비트 에러율 (BER) 공식

```
BPSK (Coherent):
P_b = Q(√(2E_b/N_0))

QPSK (Coherent):
P_b = Q(√(2E_b/N_0))  (BPSK와 동일한 BER)

M-PSK (Coherent):
P_s ≈ 2·Q(√(2k·E_b/N_0)·sin(π/M))

여기서:
- k = log₂(M) bits/symbol
- E_b/N_0: 비트 에너지 대 잡음비
- M: 심볼 개수

SNR 요구사항 (BER = 10^-5):
- BPSK: 9.6 dB
- QPSK: 9.6 dB
- 8-PSK: 13.0 dB
- 16-PSK: 17.2 dB
```

### 핵심 코드: PSK 변조/복조 구현 (Python)

```python
import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum

class PSKType(Enum):
    """PSK 종류"""
    BPSK = 2
    QPSK = 4
    PSK8 = 8
    PSK16 = 16

@dataclass
class PSKConfig:
    """PSK 설정 파라미터"""
    psk_type: PSKType = PSKType.QPSK
    samples_per_symbol: int = 100
    carrier_freq: float = 10.0  # 정규화 주파수

    @property
    def bits_per_symbol(self) -> int:
        return int(np.log2(self.psk_type.value))

class PSKModulator:
    """PSK 변조기"""

    def __init__(self, config: PSKConfig):
        self.config = config
        self.constellation = self._generate_constellation()

    def _generate_constellation(self) -> Dict[int, complex]:
        """성상도 생성"""
        M = self.config.psk_type.value
        constellation = {}

        # Gray 코딩 적용
        gray_code = self._generate_gray_code(int(np.log2(M)))

        for i in range(M):
            angle = 2 * np.pi * i / M
            symbol = np.exp(1j * angle)
            constellation[gray_code[i]] = symbol

        return constellation

    def _generate_gray_code(self, n_bits: int) -> List[int]:
        """Gray 코드 생성"""
        if n_bits <= 0:
            return [0]

        result = [0, 1]
        for i in range(1, n_bits):
            result = result + [x + (1 << i) for x in reversed(result)]
        return result

    def bits_to_symbols(self, bits: List[int]) -> List[int]:
        """비트를 심볼로 변환"""
        bps = self.config.bits_per_symbol
        symbols = []

        for i in range(0, len(bits), bps):
            if i + bps <= len(bits):
                symbol = 0
                for j in range(bps):
                    symbol = (symbol << 1) | bits[i + j]
                symbols.append(symbol)

        return symbols

    def modulate(self, bits: List[int]) -> Tuple[np.ndarray, np.ndarray, List[complex]]:
        """PSK 변조"""
        sps = self.config.samples_per_symbol
        fc = self.config.carrier_freq
        symbols = self.bits_to_symbols(bits)

        n_symbols = len(symbols)
        n_samples = n_symbols * sps
        t = np.arange(n_samples) / sps

        # 심볼을 I/Q로 변환
        symbol_sequence = []
        for symbol in symbols:
            symbol_sequence.append(self.constellation[symbol])

        # 업샘플링
        i_signal = np.zeros(n_samples)
        q_signal = np.zeros(n_samples)

        for i, sym in enumerate(symbol_sequence):
            i_signal[i*sps:(i+1)*sps] = sym.real
            q_signal[i*sps:(i+1)*sps] = sym.imag

        # I/Q 변조
        carrier_i = np.cos(2 * np.pi * fc * t)
        carrier_q = -np.sin(2 * np.pi * fc * t)

        modulated = i_signal * carrier_i + q_signal * carrier_q

        return modulated, t, symbol_sequence

class PSKDemodulator:
    """PSK 복조기"""

    def __init__(self, config: PSKConfig):
        self.config = config
        self.constellation = self._generate_constellation()

    def _generate_constellation(self) -> Dict[int, complex]:
        modulator = PSKModulator(self.config)
        return modulator.constellation

    def demodulate(
        self,
        signal: np.ndarray,
        symbol_sequence: List[complex]
    ) -> Tuple[List[int], List[complex]]:
        """코히어런트 PSK 복조"""
        sps = self.config.samples_per_symbol
        fc = self.config.carrier_freq
        n_samples = len(signal)
        n_symbols = n_samples // sps
        t = np.arange(n_samples) / sps

        # 국부 반송파 (완벽한 위상 동기 가정)
        carrier_i = np.cos(2 * np.pi * fc * t)
        carrier_q = -np.sin(2 * np.pi * fc * t)

        # I/Q 검파
        i_demod = signal * carrier_i * 2
        q_demod = signal * carrier_q * 2

        # 심볼 판정
        detected_symbols = []
        constellation_points = list(self.constellation.values())
        constellation_keys = list(self.constellation.keys())

        for i in range(n_symbols):
            start = i * sps
            end = (i + 1) * sps

            i_val = np.mean(i_demod[start:end])
            q_val = np.mean(q_demod[start:end])
            detected = complex(i_val, q_val)

            # 최근접 이웃 탐색
            distances = [abs(detected - point) for point in constellation_points]
            nearest_idx = np.argmin(distances)
            detected_symbols.append(constellation_keys[nearest_idx])

        # 심볼을 비트로 변환
        bits = []
        bps = self.config.bits_per_symbol
        for symbol in detected_symbols:
            for j in range(bps - 1, -1, -1):
                bits.append((symbol >> j) & 1)

        return bits, detected_symbols

    def calculate_ber(self, original: List[int], decoded: List[int]) -> float:
        """BER 계산"""
        min_len = min(len(original), len(decoded))
        errors = sum(1 for i in range(min_len) if original[i] != decoded[i])
        return errors / min_len if min_len > 0 else 0.0

class AWGNChannel:
    """AWGN 채널"""
    def __init__(self, snr_db: float):
        self.snr_db = snr_db

    def transmit(self, signal: np.ndarray) -> np.ndarray:
        snr_linear = 10 ** (self.snr_db / 10)
        signal_power = np.mean(np.abs(signal) ** 2)
        noise_power = signal_power / snr_linear
        noise = np.sqrt(noise_power / 2) * (
            np.random.randn(len(signal)) + 1j * np.random.randn(len(signal))
        )
        return signal + noise.real

def plot_constellation(modulator: PSKModulator):
    """성상도 시각화"""
    import matplotlib.pyplot as plt

    constellation = modulator.constellation
    points = list(constellation.values())
    labels = list(constellation.keys())

    fig, ax = plt.subplots(figsize=(8, 8))

    # 단위원 그리기
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3)

    # 성상도 점 표시
    for label, point in zip(labels, points):
        ax.scatter(point.real, point.imag, s=100, c='blue')
        ax.annotate(f'{label:0{int(np.log2(len(points)))}d}',
                   (point.real, point.imag),
                   textcoords="offset points",
                   xytext=(5,5), ha='center')

    ax.set_xlabel('In-phase (I)')
    ax.set_ylabel('Quadrature (Q)')
    ax.set_title(f'{modulator.config.psk_type.name} Constellation')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

    plt.tight_layout()
    plt.show()

def run_psk_simulation():
    """PSK 시뮬레이션"""
    np.random.seed(42)

    print("=" * 70)
    print("PSK (Phase Shift Keying) 시뮬레이션")
    print("=" * 70)

    for psk_type in [PSKType.BPSK, PSKType.QPSK, PSKType.PSK8]:
        config = PSKConfig(psk_type=psk_type)
        modulator = PSKModulator(config)
        demodulator = PSKDemodulator(config)

        # 테스트 비트 생성
        n_bits = 1000 * config.bits_per_symbol
        test_bits = [int(b) for b in np.random.randint(0, 2, n_bits)]

        # 변조
        signal, t, symbols = modulator.modulate(test_bits)

        # 다양한 SNR에서 BER 측정
        print(f"\n--- {psk_type.name} ---")
        print(f"Bits per symbol: {config.bits_per_symbol}")
        print(f"Constellation points: {len(modulator.constellation)}")

        for snr_db in [5, 10, 15, 20]:
            channel = AWGNChannel(snr_db)
            noisy = channel.transmit(signal)
            decoded, _ = demodulator.demodulate(noisy, symbols)
            ber = demodulator.calculate_ber(test_bits, decoded)
            print(f"SNR = {snr_db:2d} dB: BER = {ber:.6f}")

if __name__ == "__main__":
    run_psk_simulation()
