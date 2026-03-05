+++
title = "039. 맨체스터 부호화 (Manchester Coding)"
description = "모든 비트에서 중간 전이를 보장하여 동기화 능력을 극대화한 맨체스터 부호화와 차분 맨체스터 부호화의 원리를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["Manchester", "DifferentialManchester", "LineCoding", "Ethernet", "802.3", "Synchronization", "10BASE-T"]
categories = ["studynotes-3_network"]
+++

# 039. 맨체스터 부호화 (Manchester Coding)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 맨체스터 부호화는 각 비트 구간의 중간에서 반드시 신호 전이(Transition)를 발생시키는 선로 부호화로, 0과 1을 전이 방향(하강/상승) 또는 전이 존재 여부로 표현하여 동기화 능력을 보장합니다.
> 2. **가치**: 모든 비트에서 전이가 보장되므로 별도의 클럭선 없이도 완벽한 비트 동기화가 가능하며, DC 밸런스가 0이어서 커패시터나 변압기로 AC 결합된 회로에서 이상적입니다.
> 3. **융합**: 맨체스터 부호화는 10Mbps 이더넷(IEEE 802.3 10BASE-T), RFID, 적외선 리모컨 등에서 표준으로 사용되며, 현대 고속 통신에서는 8b/10b, 64b/66b 등의 DC 밸런스 기법으로 진화했습니다.

---

## I. 개요 (Context & Background)

맨체스터 부호화(Manchester Coding)는 1949년 G. E. Thomas에 의해 개발된 선로 부호화 방식으로, 각 비트 구간의 **정확히 중간 지점에서 반드시 신호 전이(Transition)**가 발생하도록 설계되었습니다. 이 전이는 데이터 정보와 타이밍 정보를 동시에 전달하여, 수신측이 별도의 클럭 신호 없이도 송신측과 완벽하게 동기화할 수 있게 합니다.

**💡 비유**: 맨체스터 부호화는 **'박자에 맞춘 춤추기'**와 같습니다.
- 춤추는 사람은 매 박자마다 특정 동작(전이)을 수행합니다.
- 1을 표현할 때는 '왼발에서 오른발로' 이동하고, 0을 표현할 때는 '오른발에서 왼발로' 이동합니다.
- 모든 박자(비트)에서 반드시 발을 바꾸므로(전이), 박자(클럭)를 잃을 일이 없습니다.
- 마치 메트로놈 소리에 맞춰 정확히 춤추는 것과 같습니다.

**등장 배경 및 발전 과정**:
1. **이더넷 탄생 (1973년)**: 제로록스 PARC의 Robert Metcalfe가 이더넷을 개발하면서 맨체스터 부호화를 채택했습니다. 당시 네트워크는 동축케이블 기반이었고, 신뢰성 있는 동기화가 필수적이었습니다.
2. **IEEE 802.3 표준화 (1983년)**: 10Mbps 이더넷(10BASE5, 10BASE2, 10BASE-T) 표준으로 맨체스터 부호화가 공식 채택되었습니다. 이는 수십 년간 사무실 네트워크의 표준이었습니다.
3. **고속화에 따른 교체 (1990년대 중반)**: 100Mbps 이더넷(100BASE-TX)부터는 MLT-3, 4B/5B 부호화로 대체되었습니다. 맨체스터는 대역폭 효율(0.5 bit/Hz)이 낮기 때문입니다. 하지만 RFID, 무선 센서 네트워크, 적외선 통신에서는 여전히 널리 사용됩니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 부호화 방식 | 0 표현 | 1 표현 | 전이 특성 | DC 성분 | 대역폭 효율 | 표준 |
|------------|-------|-------|----------|---------|-----------|------|
| **Manchester (IEEE 802.3)** | 고→저 (High→Low) | 저→고 (Low→High) | 비트 중간 필수 | 0 | 0.5 bit/Hz | Ethernet |
| **Manchester (G. E. Thomas)** | 저→고 (Low→High) | 고→저 (High→Low) | 비트 중간 필수 | 0 | 0.5 bit/Hz | Classic |
| **Differential Manchester** | 비트 시작 전이 없음 | 비트 시작 전이 있음 | 비트 중간 필수 + 시작 선택적 | 0 | 0.5 bit/Hz | Token Ring |

### 정교한 구조 다이어그램: 맨체스터 파형 분석

```ascii
================================================================================
[ Manchester Coding (IEEE 802.3 Standard) Waveform ]
================================================================================

Input Bit Stream:   1    0    1    1    0    0    1    0    1    1
                   |    |    |    |    |    |    |    |    |    |

Voltage
   +V  |     +--+  +--+  +-----+     +-----+  +--+  +--+  +-----+
       |     |  |  |  |  |     |     |     |  |  |  |  |  |     |
   0V  |     |  |  |  |  |     |     |     |  |  |  |  |  |     |
       |     |  |  |  |  |     |     |     |  |  |  |  |  |     |
   -V  |  +--+  +--+  +--+     +-----+     +--+  +--+  +--+     +-->
       |  |                                   |
       +------------------------------------------------------------------> Time
            |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
            |<-T/2->|
            |<----- 1 bit period (T) ----->|

Encoding Rules (IEEE 802.3):
  - Logic 1: Low → High transition at mid-bit (starts at -V, ends at +V)
  - Logic 0: High → Low transition at mid-bit (starts at +V, ends at -V)

Bit-by-bit Analysis:
  b1 = 1: -V → +V (low-to-high)
  b2 = 0: +V → -V (high-to-low)
  b3 = 1: -V → +V (low-to-high)
  b4 = 1: +V (continue) → -V then +V (need transition at boundary!)
         [Boundary transition occurs because b3 ended at +V]
  ...

Key Observations:
  1. GUARANTEED transition at MID-BIT for every bit
  2. May have additional transition at bit boundary
  3. Total transitions: 1 or 2 per bit (average ~1.5)

================================================================================
[ Manchester vs G.E. Thomas Convention ]
================================================================================

Both conventions are valid - they are simply inverted versions of each other.

IEEE 802.3 Convention:        G.E. Thomas Convention:
  1 = Low → High               1 = High → Low
  0 = High → Low               0 = Low → High

Example: Bit pattern 101

IEEE 802.3:                   G.E. Thomas:
   +V  |    +--+    +--+          +V  | +--+    +--+    +--+
       |    |  |    |  |              | |  |    |  |    |  |
   0V  |    |  |    |  |          0V  | |  |    |  |    |  |
       |    |  |    |  |              | |  |    |  |    |  |
   -V  | +--+  +--+                 -V  |    +--+    +--+
       +---------------------------->    +------------------------>
        1   0   1                        1   0   1

Both produce transitions at mid-bit, just in opposite directions!

================================================================================
[ Differential Manchester Coding Waveform ]
================================================================================

Input Bit Stream:   1    0    1    1    0    0    1    0    1    1

Encoding Rules:
  - ALWAYS a transition at mid-bit (for synchronization)
  - Logic 1: NO transition at bit boundary (beginning)
  - Logic 0: YES transition at bit boundary (beginning)

Voltage
   +V  |  +--+  +--+  +-----+  +-----+  +--+  +--+  +-----+  +--+
       |  |  |  |  |  |     |  |     |  |  |  |  |  |     |  |
   0V  |  |  |  |  |  |     |  |     |  |  |  |  |  |     |  |
       |  |  |  |  |  |     |  |     |  |  |  |  |  |     |  |
   -V  |  |  +--+  +--+     +--+     +--+  +--+  +--+     +--+  +-->
       |
       +------------------------------------------------------------------> Time

Bit-by-bit Encoding (starting from +V):
  Start: +V

  b1 = 1: No boundary transition → stay at +V
          Mid-bit: +V → -V (guaranteed transition)

  b2 = 0: Boundary transition: -V → +V
          Mid-bit: +V → -V

  b3 = 1: No boundary transition → stay at -V
          Mid-bit: -V → +V

  b4 = 1: Boundary transition: +V → -V (because mid-bit ended at +V)
          Wait, no! For b4=1, NO boundary transition!
          Previous mid-bit ended at +V, so start at +V
          Mid-bit: +V → -V

  [Encoding continues...]

Key Characteristics:
  1. ALWAYS a transition at mid-bit (synchronization guaranteed)
  2. Optional transition at bit boundary (carries data)
  3. Total transitions: 1 or 2 per bit
  4. Immune to signal inversion (differential encoding)

================================================================================
[ Synchronization Advantage: Manchester vs NRZ ]
================================================================================

Case: Long run of identical bits (11111111...)

NRZ (Non-Return to Zero):
   +V  |---------------------------------------------------------->
       |
   0V  |
       |
   -V  |
       +------------------------------------------------------------------> Time
        1   1   1   1   1   1   1   1

   Problem: NO transitions! Clock recovery IMPOSSIBLE.
   After a few bits, receiver clock will drift.

Manchester:
   +V  |    +--+    +--+    +--+    +--+    +--+    +--+    +--+
       |    |  |    |  |    |  |    |  |    |  |    |  |    |  |
   0V  |    |  |    |  |    |  |    |  |    |  |    |  |    |  |
       |    |  |    |  |    |  |    |  |    |  |    |  |    |  |
   -V  | +--+    +--+    +--+    +--+    +--+    +--+    +--+    +-->
       +------------------------------------------------------------------> Time
        1   1   1   1   1   1   1   1

   Solution: Transition at EVERY mid-bit! Clock recovery GUARANTEED.
   Receiver can maintain perfect synchronization indefinitely.

================================================================================
[ DC Balance Analysis ]
================================================================================

Manchester coding achieves ZERO DC component over any bit period.

Why?
  - First half: +V or -V (depending on bit value)
  - Second half: opposite of first half
  - Average over one bit: (+V × T/2 + (-V) × T/2) / T = 0

This is TRUE for BOTH 0 and 1!

Graphical Proof:
  For bit 1: -V for T/2, +V for T/2 → Average = 0
  For bit 0: +V for T/2, -V for T/2 → Average = 0

Consequence:
  - No DC wander problem
  - Can pass through AC-coupled circuits (transformers, capacitors)
  - Ideal for ethernet over transformers (magnetic isolation)

================================================================================
```

### 심층 동작 원리: 5가지 핵심 메커니즘

1. **비트 중간 전이 보장 (Mid-Bit Transition Guarantee)**:
   - **핵심 원리**: 모든 비트의 정확히 중간 지점(T/2)에서 신호 전이가 발생합니다.
   - **IEEE 802.3 규칙**: 1 = Low→High (상승), 0 = High→Low (하강)
   - **동기화**: 수신측은 이 중간 전이를 클럭 복구의 기준으로 사용합니다.

2. **비트 경계 전이 (Bit Boundary Transition)**:
   - **발생 조건**: 비트 경계에서 전이가 발생하는지 여부는 이전 비트와 현재 비트의 조합에 따라 결정됩니다.
   - **IEEE 802.3**: 이전 비트가 1로 끝나고(+V), 현재 비트가 1로 시작해야 하면(-V), 경계에서 전이 발생.
   - **평균 전이 횟수**: 비트당 1.5회 (중간 1회 + 경계 0.5회 평균)

3. **DC 밸런스 0 (Zero DC Component)**:
   - **이유**: 각 비트 구간에서 +V와 -V의 지속 시간이 정확히 동일합니다.
   - **수학적 증명**: 비트 1의 평균 = (-V×T/2 + V×T/2)/T = 0, 비트 0도 동일.
   - **실무 이점**: 이더넷 변압기(Transformer)를 통과해도 신호 왜곡이 없습니다.

4. **차분 맨체스터 부호화 (Differential Manchester)**:
   - **추가 규칙**: 비트 경계에서의 전이 여부로 0과 1을 구분합니다.
     - 1: 비트 시작점에서 전이 없음
     - 0: 비트 시작점에서 전이 있음
   - **장점**: 신호 극성이 반전되어도(선이 뒤바뀌어도) 데이터 보존.
   - **적용**: 토큰 링(IEEE 802.5)에서 사용.

5. **대역폭 효율 vs 동기화 트레이드오프 (Bandwidth vs Synchronization Trade-off)**:
   - **대역폭 효율**: 0.5 bit/Hz (NRZ의 1/2)
   - **이유**: 맨체스터는 1 비트를 2개의 펄스(심볼)로 표현합니다.
   - **실무 영향**: 10Mbps 이더넷은 20MHz 대역폭이 필요합니다.
   - **대체**: 100Mbps 이상에서는 4B/5B + MLT-3로 대체하여 효율 개선.

### 핵심 코드: 맨체스터 부호화 구현 (Python)

```python
from enum import Enum
from typing import List, Tuple
import numpy as np

class ManchesterConvention(Enum):
    """맨체스터 부호화 규약"""
    IEEE_802_3 = "IEEE 802.3"  # 1 = Low→High, 0 = High→Low
    G_E_THOMAS = "G.E. Thomas"  # 1 = High→Low, 0 = Low→High

class ManchesterCoder:
    """
    맨체스터 부호화 구현

    특징:
    - 모든 비트의 중간에서 전이 보장
    - DC 성분이 0
    - 대역폭 효율 0.5 bit/Hz
    - 10Mbps 이더넷(IEEE 802.3) 표준
    """

    def __init__(self, voltage_level: float = 1.0, samples_per_bit: int = 100,
                 convention: ManchesterConvention = ManchesterConvention.IEEE_802_3):
        """
        Args:
            voltage_level: 기준 전압 레벨 (V)
            samples_per_bit: 비트당 샘플 수
            convention: 맨체스터 규약 (IEEE 802.3 또는 G.E. Thomas)
        """
        self.V = voltage_level
        self.samples_per_bit = samples_per_bit
        self.half_samples = samples_per_bit // 2
        self.convention = convention

    def encode(self, bits: List[int]) -> np.ndarray:
        """
        맨체스터 부호화

        IEEE 802.3:
          - Logic 1: -V → +V (Low → High at mid-bit)
          - Logic 0: +V → -V (High → Low at mid-bit)

        G.E. Thomas:
          - Logic 1: +V → -V (High → Low at mid-bit)
          - Logic 0: -V → +V (Low → High at mid-bit)
        """
        waveform = np.array([])

        for bit in bits:
            if self.convention == ManchesterConvention.IEEE_802_3:
                if bit == 1:
                    # Low → High
                    waveform = np.append(waveform, np.full(self.half_samples, -self.V))
                    waveform = np.append(waveform, np.full(self.half_samples, self.V))
                else:
                    # High → Low
                    waveform = np.append(waveform, np.full(self.half_samples, self.V))
                    waveform = np.append(waveform, np.full(self.half_samples, -self.V))
            else:  # G.E. Thomas
                if bit == 1:
                    # High → Low
                    waveform = np.append(waveform, np.full(self.half_samples, self.V))
                    waveform = np.append(waveform, np.full(self.half_samples, -self.V))
                else:
                    # Low → High
                    waveform = np.append(waveform, np.full(self.half_samples, -self.V))
                    waveform = np.append(waveform, np.full(self.half_samples, self.V))

        return waveform

    def decode(self, waveform: np.ndarray) -> List[int]:
        """
        맨체스터 복호화

        비트 중간 지점에서 전이 방향을 감지하여 비트 값 판별
        """
        bits = []
        n_bits = len(waveform) // self.samples_per_bit

        for i in range(n_bits):
            start = i * self.samples_per_bit
            mid = start + self.half_samples

            # 전반부 후반과 후반부 전반의 평균 전압 비교
            first_half_avg = np.mean(waveform[start:start + self.half_samples])
            second_half_avg = np.mean(waveform[mid:mid + self.half_samples])

            # 전이 방향 판별
            if self.convention == ManchesterConvention.IEEE_802_3:
                # Low → High = 1, High → Low = 0
                bit = 1 if second_half_avg > first_half_avg else 0
            else:
                # High → Low = 1, Low → High = 0
                bit = 1 if first_half_avg > second_half_avg else 0

            bits.append(bit)

        return bits

    def count_transitions(self, waveform: np.ndarray) -> dict:
        """
        전이 횟수 분석

        Returns:
            mid_bit_transitions: 비트 중간 전이 횟수
            boundary_transitions: 비트 경계 전이 횟수
            total_transitions: 총 전이 횟수
        """
        threshold = self.V * 0.1
        diff = np.abs(np.diff(waveform)) > threshold

        mid_bit_transitions = 0
        boundary_transitions = 0

        n_bits = len(waveform) // self.samples_per_bit

        for i in range(n_bits):
            # 비트 중간 전이 (항상 존재해야 함)
            mid_idx = i * self.samples_per_bit + self.half_samples - 1
            if mid_idx < len(diff) and diff[mid_idx]:
                mid_bit_transitions += 1

            # 비트 경계 전이
            if i > 0:
                boundary_idx = i * self.samples_per_bit - 1
                if boundary_idx < len(diff) and diff[boundary_idx]:
                    boundary_transitions += 1

        return {
            "mid_bit_transitions": mid_bit_transitions,
            "boundary_transitions": boundary_transitions,
            "total_transitions": mid_bit_transitions + boundary_transitions
        }


class DifferentialManchesterCoder:
    """
    차분 맨체스터 부호화 구현

    특징:
    - 모든 비트의 중간에서 전이 보장 (동기화)
    - 비트 시작점 전이 여부로 0/1 구분 (데이터)
    - 극성 반전에 강함
    - 토큰 링(IEEE 802.5)에서 사용
    """

    def __init__(self, voltage_level: float = 1.0, samples_per_bit: int = 100):
        self.V = voltage_level
        self.samples_per_bit = samples_per_bit
        self.half_samples = samples_per_bit // 2

    def encode(self, bits: List[int]) -> np.ndarray:
        """
        차분 맨체스터 부호화

        규칙:
        - 비트 중간: 항상 전이 (동기화)
        - 비트 시작:
          - Logic 1: 전이 없음
          - Logic 0: 전이 있음
        """
        waveform = np.array([])
        current_level = -self.V  # 초기 상태

        for bit in bits:
            # 비트 시작점 처리
            if bit == 0:
                # 0이면 비트 시작점에서 전이
                current_level = -current_level

            # 전반부
            waveform = np.append(waveform, np.full(self.half_samples, current_level))

            # 비트 중간: 항상 전이
            current_level = -current_level

            # 후반부
            waveform = np.append(waveform, np.full(self.half_samples, current_level))

        return waveform

    def decode(self, waveform: np.ndarray) -> List[int]:
        """
        차분 맨체스터 복호화

        비트 경계와 비트 중간의 전이 패턴 분석
        """
        bits = []
        n_bits = len(waveform) // self.samples_per_bit
        threshold = self.V * 0.1

        for i in range(n_bits):
            start = i * self.samples_per_bit
            mid = start + self.half_samples

            # 비트 시작점 전이 여부 확인
            if i == 0:
                # 첫 비트: 규칙에 따라 판단 (보통 1로 가정)
                bits.append(1)
            else:
                # 이전 비트 후반부 끝과 현재 비트 전반부 시작 비교
                prev_end = waveform[mid - 1] if i > 0 else waveform[start]
                curr_start = waveform[start]

                if abs(prev_end - curr_start) > threshold:
                    # 경계에서 전이 발생 = 0
                    bits.append(0)
                else:
                    # 경계에서 전이 없음 = 1
                    bits.append(1)

        return bits


def compare_coding_methods():
    """맨체스터 vs NRZ vs 차분 맨체스터 비교"""

    print("\n" + "="*80)
    print("Comparison: Manchester vs Differential Manchester")
    print("="*80)

    test_bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]

    manchester = ManchesterCoder()
    diff_manchester = DifferentialManchesterCoder()

    m_wave = manchester.encode(test_bits)
    dm_wave = diff_manchester.encode(test_bits)

    m_trans = manchester.count_transitions(m_wave)
    dm_trans = manchester.count_transitions(dm_wave)

    print(f"\nTest Pattern: {test_bits}")
    print(f"\n{'Metric':<30} | {'Manchester':<20} | {'Diff Manchester':<20}")
    print("-"*80)
    print(f"{'DC Component':<30} | {np.mean(m_wave):>+.4f} V           | {np.mean(dm_wave):>+.4f} V")
    print(f"{'Mid-bit Transitions':<30} | {m_trans['mid_bit_transitions']:>10}          | {dm_trans['mid_bit_transitions']:>10}")
    print(f"{'Boundary Transitions':<30} | {m_trans['boundary_transitions']:>10}          | {dm_trans['boundary_transitions']:>10}")
    print(f"{'Total Transitions':<30} | {m_trans['total_transitions']:>10}          | {dm_trans['total_transitions']:>10}")

    print("\n" + "="*80)


def demonstrate_synchronization():
    """동기화 능력 시연"""

    print("\n" + "="*70)
    print("Synchronization Capability Demonstration")
    print("="*70)

    # 문제 패턴: 긴 동일 비트 연속
    long_ones = [1] * 20
    long_zeros = [0] * 20

    manchester = ManchesterCoder()
    nrz_coder = NRZCoderMock()

    print("\nTest Case 1: Long run of ones (1111...)")
    print("-"*50)

    m_wave_ones = manchester.encode(long_ones)
    nrz_wave_ones = nrz_coder.encode_polar_nrz_l(long_ones)

    m_trans = manchester.count_transitions(m_wave_ones)
    nrz_trans = np.sum(np.abs(np.diff(nrz_wave_ones)) > 0.1)

    print(f"  Manchester transitions: {m_trans['total_transitions']} (guaranteed)")
    print(f"  NRZ transitions: {int(nrz_trans)} (none for all-ones!)")

    print("\nTest Case 2: Long run of zeros (0000...)")
    print("-"*50)

    m_wave_zeros = manchester.encode(long_zeros)
    nrz_wave_zeros = nrz_coder.encode_polar_nrz_l(long_zeros)

    m_trans = manchester.count_transitions(m_wave_zeros)
    nrz_trans = np.sum(np.abs(np.diff(nrz_wave_zeros)) > 0.1)

    print(f"  Manchester transitions: {m_trans['total_transitions']} (guaranteed)")
    print(f"  NRZ transitions: {int(nrz_trans)} (none for all-zeros!)")

    print("\nConclusion:")
    print("  Manchester maintains synchronization for ANY bit pattern")
    print("  NRZ fails for consecutive identical bits")

    print("="*70)


def demonstrate_dc_balance():
    """DC 밸런스 시연"""

    print("\n" + "="*70)
    print("DC Balance Analysis")
    print("="*70)

    patterns = {
        "All ones": [1] * 100,
        "All zeros": [0] * 100,
        "Alternating": [1, 0] * 50,
        "Random": np.random.randint(0, 2, 100).tolist()
    }

    manchester = ManchesterCoder()

    print(f"\n{'Pattern':<20} | {'DC Component (V)':<20} | {'Status'}")
    print("-"*60)

    for name, bits in patterns.items():
        waveform = manchester.encode(bits)
        dc = np.mean(waveform)
        status = "PERFECT" if abs(dc) < 0.001 else "IMBALANCED"
        print(f"{name:<20} | {dc:>+.6f}            | {status}")

    print("\nAll patterns have ZERO DC component!")
    print("="*70)


class NRZCoderMock:
    """비교용 NRZ 부호화 Mock"""
    def __init__(self, voltage_level: float = 1.0):
        self.V = voltage_level

    def encode_polar_nrz_l(self, bits: List[int]) -> np.ndarray:
        return np.array([self.V if b == 1 else -self.V for b in bits])


# ==================== 실행 ====================
if __name__ == "__main__":
    compare_coding_methods()
    demonstrate_synchronization()
    demonstrate_dc_balance()
