+++
title = "037. NRZ 부호화 (Non-Return to Zero Coding)"
description = "가장 기본적인 디지털 부호화 방식인 NRZ-L과 NRZ-I의 동작 원리, 장단점, 실무 적용 사례를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["NRZ", "NRZ-L", "NRZ-I", "LineCoding", "Encoding", "Differential", "USB", "PCIe"]
categories = ["studynotes-3_network"]
+++

# 037. NRZ 부호화 (Non-Return to Zero Coding)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NRZ(Non-Return to Zero) 부호화는 비트 구간 동안 신호 레벨이 유지되는 가장 단순한 디지털 부호화 방식으로, NRZ-L(Level)은 비트 값을 전압 레벨에 직접 매핑하고, NRZ-I(Inverted)는 1 비트마다 전압을 반전시키는 차분 부호화 방식입니다.
> 2. **가치**: NRZ는 구현 복잡도가 가장 낮고 대역폭 효율이 높아(1 bit/Hz 이상), USB, PCIe, SATA 등의 고속 직렬 인터페이스에서 널리 사용되며, NRZ-I는 극성 반전에 강한 특성으로 시리얼 통신에 적합합니다.
> 3. **융합**: 현대 고속 통신에서 NRZ는 Scrambling, 8b/10b Encoding, Equalization 기술과 결합하여 10GbE, USB 3.x, PCIe 3.0 이하에서 핵심 부호화 방식으로 활용되며, PAM4로의 진화도 진행 중입니다.

---

## I. 개요 (Context & Background)

NRZ(Non-Return to Zero) 부호화는 디지털 통신에서 가장 기본적이고 널리 사용되는 선로 부호화 방식입니다. 이름에서 알 수 있듯이, 비트 구간(Bit Period) 동안 신호가 0 레벨로 돌아가지(Return) 않고 해당 비트 값에 해당하는 전압 레벨을 유지하는 특징이 있습니다. NRZ는 크게 **NRZ-L(Level)**과 **NRZ-I(Inverted)** 두 가지 변형으로 나뉩니다.

**💡 비유**: NRZ 부호화는 **'스위치의 On/Off 상태 유지'**와 같습니다.
- **NRZ-L**: 스위치를 켜면(1) 불이 계속 켜져 있고, 스위치를 끄면(0) 불이 계속 꺼져 있습니다. 각 상태가 비트 구간 동안 지속됩니다. 마치 방의 불을 켜고 끄는 것과 같습니다.
- **NRZ-I**: 스위치를 누를 때마다(1) 불의 상태가 반전됩니다. 켜져 있으면 꺼지고, 꺼져 있으면 켜집니다. 0일 때는 아무 일도 일어나지 않습니다. 마치 토글 스위치를 누르는 것과 같습니다.

**등장 배경 및 발전 과정**:
1. **초기 디지털 통신 (1960년대)**: 컴퓨터와 단말기 간 통신에서 가장 단순한 방식이 필요했습니다. NRZ는 하드웨어 구현이 가장 간단하여 RS-232C 등 초기 시리얼 통신에 채택되었습니다.
2. **고속 인터페이스 시대 (1990년대~2000년대)**: USB 1.x, PCI, ATA 등이 NRZ 기반으로 설계되었습니다. 높은 대역폭 효율(1 bit per baud)이 결정적인 장점이었습니다.
3. **현대적 진화 (2010년대~현재)**: USB 3.x, PCIe 3.0, SATA 3.0, 10GbE 등은 여전히 NRZ를 사용하지만, Scrambling과 8b/10b, 128b/132b 인코딩을 결합하여 DC 밸런스와 동기화 문제를 해결합니다. PCIe 4.0/5.0과 400GbE에서는 PAM4로 전환하여 대역폭을 두 배로 늘렸습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 부호화 방식 | 비트-전압 매핑 | 전이 특성 | DC 밸런스 | 동기화 능력 | 오버헤드 | 주요 적용 |
|------------|--------------|----------|----------|-----------|----------|----------|
| **NRZ-L** | 0=-V, 1=+V | 비트 변화 시 | 불량 | 불량 | 0% | RS-232C, 병렬 버스 |
| **NRZ-I** | 1=반전, 0=유지 | 1 비트 시 | 불량 | 중간 | 0% | USB, SATA, PCIe |
| **NRZ-M** (Mark) | 1=반전, 0=유지 | 1 비트 시 | 불량 | 중간 | 0% | 자기 테이프 |
| **NRZ-S** (Space) | 0=반전, 1=유지 | 0 비트 시 | 불량 | 중간 | 0% | 특수 응용 |

### 정교한 구조 다이어그램: NRZ-L vs NRZ-I 비교

```ascii
================================================================================
[ NRZ-L (Non-Return to Zero Level) Waveform ]
================================================================================

Input Bit Stream:   1    0    1    1    0    0    1    0    1    1
                   |    |    |    |    |    |    |    |    |    |

Voltage
   +V  |  +----+       +----+----+             +----+    +----+----+
       |  |    |       |    |    |             |    |    |    |    |
   0V  |  |    |       |    |    |             |    |    |    |    |
       |  |    |       |    |    |             |    |    |    |    |
   -V  |  |    +-------+    |    +-------------+    +----+    |    +-->
       |             |             |                       |          |
       +------------------------------------------------------------------> Time
            b1   b2   b3   b4   b5   b6   b7   b8   b9  b10

Rule: Logic 1 → +V, Logic 0 → -V
- Direct mapping between bit value and voltage level
- Bit value is "written" in the signal level

Transitions: 5 (at b2, b3, b5, b7, b8, b10)
DC Component: (+V x 6 + (-V) x 4) / 10 = +0.2V (depends on bit ratio)

================================================================================
[ NRZ-I (Non-Return to Zero Inverted) Waveform ]
================================================================================

Input Bit Stream:   1    0    1    1    0    0    1    0    1    1
                   |    |    |    |    |    |    |    |    |    |

Voltage
   +V  |  +----+----+             +----+             +----+----+----+
       |  |    |    |             |    |             |    |    |    |
   0V  |  |    |    |             |    |             |    |    |    |
       |  |    |    |             |    |             |    |    |    |
   -V  |  |    |    +-------------+    +-------------+    |    |    |
       |         |                   |                   |    |    |
       +------------------------------------------------------------------> Time
            b1   b2   b3   b4   b5   b6   b7   b8   b9  b10

Rule: Logic 1 → Invert current level, Logic 0 → Maintain current level
Initial State: +V (before b1)

Encoding Process:
  Start: +V
  b1 = 1: Invert +V → -V         [Transition!]
  b2 = 0: Maintain → -V          [No transition]
  b3 = 1: Invert -V → +V         [Transition!]
  b4 = 1: Invert +V → -V         [Transition!]
  b5 = 0: Maintain → -V          [No transition]
  b6 = 0: Maintain → -V          [No transition]
  b7 = 1: Invert -V → +V         [Transition!]
  b8 = 0: Maintain → +V          [No transition]
  b9 = 1: Invert +V → -V         [Transition!]
  b10 = 1: Invert -V → +V        [Transition!]

Transitions: 6 (at b1, b3, b4, b7, b9, b10)
Note: More transitions than NRZ-L for this pattern!

================================================================================
[ Comparison: Synchronization Problem ]
================================================================================

Case 1: Long run of zeros (00000000...)

NRZ-L:
   +V  |
       |
   0V  |
       |
   -V  |---------------------------------------------------------->
       |
       +------------------------------------------------------------------> Time
            0    0    0    0    0    0    0    0

   Problem: No transitions! Clock recovery impossible.

NRZ-I (assuming initial +V):
   +V  |---------------------------------------------------------->
       |
   0V  |
       |
   -V  |
       |
       +------------------------------------------------------------------> Time
            0    0    0    0    0    0    0    0

   Problem: SAME - No transitions for zeros! Clock recovery impossible.

Case 2: Long run of ones (11111111...)

NRZ-L:
   +V  |---------------------------------------------------------->
       |
   0V  |
       |
   -V  |
       |
       +------------------------------------------------------------------> Time
            1    1    1    1    1    1    1    1

   Problem: No transitions! Clock recovery impossible.

NRZ-I:
   +V  |----+    +----+    +----+    +----+
       |    |    |    |    |    |    |    |
   0V  |    |    |    |    |    |    |    |
       |    |    |    |    |    |    |    |
   -V  |    +----+    +----+    +----+    +---->
       |
       +------------------------------------------------------------------> Time
            1    1    1    1    1    1    1    1

   Solution: Transitions for every '1'! Clock recovery possible.

================================================================================
[ NRZ-I Differential Decoding Advantage ]
================================================================================

Scenario: Signal polarity inversion (crossover cable, reversed wiring)

Original NRZ-L Signal:
   +V  |--+    +--+
       |  |    |  |
   -V  |  +----+  +---->

After Polarity Inversion (wire swap):
   +V  |  +----+  +----    <-- WRONG! Decoded as 0 1 0 0...
       |  |    |  |
   -V  |--+    +--+

   Result: ALL BITS INVERTED! Data corrupted.

Original NRZ-I Signal:
   +V  |--+    +--+
       |  |    |  |
   -V  |  +----+  +---->

After Polarity Inversion (wire swap):
   +V  |  +----+  +----
       |  |    |  |
   -V  |--+    +--+--->

   Decoding: Look at TRANSITIONS, not levels!
   - Transition at b1 → 1
   - No transition at b2 → 0
   - Transition at b3 → 1
   - Transition at b4 → 1

   Result: SAME DATA! NRZ-I is immune to polarity inversion.

================================================================================
```

### 심층 동작 원리: 5가지 핵심 메커니즘

1. **NRZ-L 부호화 (Level Encoding)**:
   - **매핑 규칙**: 1 → +V, 0 → -V (또는 1 → +V, 0 → 0V for Unipolar NRZ-L)
   - **특징**: 비트 값이 전압 레벨에 직접 매핑됩니다. 수신측은 전압 레벨을 측정하여 0 또는 1을 판별합니다.
   - **문제점**: 0이나 1이 연속될 때 신호 전이(Transition)가 없어, 수신측에서 클럭 복구(Clock Recovery)가 어렵습니다.

2. **NRZ-I 부호화 (Differential Encoding)**:
   - **매핑 규칙**: 1 → 전압 반전, 0 → 현재 전압 유지
   - **특징**: 비트 값이 전압 레벨이 아닌 전압 변화(Transition)에 인코딩됩니다. 이를 **차분 부호화(Differential Encoding)**라 합니다.
   - **장점**: 극성 반전(Polarity Inversion)에 강합니다. 전압 레벨이 반대로 나타나도 전이 패턴은 동일하므로 데이터가 보존됩니다.

3. **클럭 복구 (Clock Recovery)**:
   - **문제**: NRZ은 신호 전이가 없을 수 있어 수신측이 송신측의 클럭과 동기화하기 어렵습니다.
   - **해결책**:
     - **별도 클럭 라인**: RS-232C에서는 별도의 클럭 신호를 사용하지 않지만, 동기식 통신에서는 별도 클럭선을 사용합니다.
     - **Scrambling**: 데이터를 랜덤화하여 연속된 0이나 1을 방지합니다.
     - **Line Coding Replacement**: 맨체스터, 8b/10b 등으로 대체합니다.

4. **DC 밸런스 (DC Balance)**:
   - **문제**: NRZ은 데이터에 따라 DC 성분이 변동합니다. 1이 많으면 양의 DC, 0이 많으면 음의 DC가 발생합니다.
   - **영향**: AC 결합(커패시터, 변압기) 회로에서 신호 왜곡(Baseline Wander)이 발생합니다.
   - **해결책**: DC 밸런싱을 위한 라인 코딩(8b/10b, 128b/132b)이나 Scrambling을 사용합니다.

5. **대역폭 효율 (Bandwidth Efficiency)**:
   - **장점**: NRZ은 1 Baud(신호 변화)당 1 bit를 전송하므로 대역폭 효율이 **1 bit/Hz**로 매우 높습니다.
   - **비교**: 맨체스터는 2 Baud/bit이므로 0.5 bit/Hz, 8b/10b는 0.8 bit/Hz입니다.
   - **적용**: 고속 인터페이스(USB 3.0, PCIe 3.0, SATA 3.0)는 NRZ + 8b/10b 조합을 사용합니다.

### 핵심 코드: NRZ 부호화/복호화 구현 (Python)

```python
from enum import Enum
from typing import List, Tuple
import numpy as np

class NRZType(Enum):
    """NRZ 부호화 타입"""
    NRZ_L = "NRZ-Level"
    NRZ_I = "NRZ-Inverted"
    NRZ_M = "NRZ-Mark"
    NRZ_S = "NRZ-Space"

class NRZCoder:
    """
    NRZ 부호화/복호화 구현

    NRZ-L (Level): 비트 값을 전압 레벨에 직접 매핑
    NRZ-I (Inverted): 1일 때마다 전압 반전
    NRZ-M (Mark): 1일 때마다 전압 반전 (NRZ-I와 동일)
    NRZ-S (Space): 0일 때마다 전압 반전
    """

    def __init__(self, voltage_level: float = 1.0, initial_state: float = 1.0):
        """
        Args:
            voltage_level: 기준 전압 레벨 (V)
            initial_state: NRZ-I의 초기 상태 (+V or -V)
        """
        self.V = voltage_level
        self.initial_state = initial_state

    def encode(self, bits: List[int], nrz_type: NRZType) -> List[float]:
        """
        NRZ 부호화

        Args:
            bits: 입력 비트 리스트
            nrz_type: NRZ 부호화 타입

        Returns:
            전압 레벨 리스트
        """
        if nrz_type == NRZType.NRZ_L:
            return self._encode_nrz_l(bits)
        elif nrz_type == NRZType.NRZ_I:
            return self._encode_nrz_i(bits)
        elif nrz_type == NRZType.NRZ_M:
            return self._encode_nrz_i(bits)  # NRZ-M == NRZ-I
        elif nrz_type == NRZType.NRZ_S:
            return self._encode_nrz_s(bits)
        else:
            raise ValueError(f"Unknown NRZ type: {nrz_type}")

    def _encode_nrz_l(self, bits: List[int]) -> List[float]:
        """NRZ-L 부호화: 1→+V, 0→-V"""
        return [self.V if bit == 1 else -self.V for bit in bits]

    def _encode_nrz_i(self, bits: List[int]) -> List[float]:
        """NRZ-I 부호화: 1→반전, 0→유지"""
        voltage = []
        current = self.initial_state

        for bit in bits:
            if bit == 1:
                current = -current  # 1이면 반전
            voltage.append(current)

        return voltage

    def _encode_nrz_s(self, bits: List[int]) -> List[float]:
        """NRZ-S 부호화: 0→반전, 1→유지"""
        voltage = []
        current = self.initial_state

        for bit in bits:
            if bit == 0:
                current = -current  # 0이면 반전
            voltage.append(current)

        return voltage

    def decode(self, voltage: List[float], nrz_type: NRZType) -> List[int]:
        """
        NRZ 복호화

        Args:
            voltage: 수신된 전압 레벨 리스트
            nrz_type: NRZ 부호화 타입

        Returns:
            복호화된 비트 리스트
        """
        if nrz_type == NRZType.NRZ_L:
            return self._decode_nrz_l(voltage)
        elif nrz_type in [NRZType.NRZ_I, NRZType.NRZ_M]:
            return self._decode_nrz_i(voltage)
        elif nrz_type == NRZType.NRZ_S:
            return self._decode_nrz_s(voltage)
        else:
            raise ValueError(f"Unknown NRZ type: {nrz_type}")

    def _decode_nrz_l(self, voltage: List[float]) -> List[int]:
        """NRZ-L 복호화: +V→1, -V→0"""
        return [1 if v > 0 else 0 for v in voltage]

    def _decode_nrz_i(self, voltage: List[float]) -> List[int]:
        """NRZ-I 복호화: 전이 발생→1, 전이 없음→0"""
        bits = []

        for i in range(len(voltage)):
            if i == 0:
                # 첫 비트: 초기 상태와 비교
                if voltage[i] != self.initial_state:
                    bits.append(1)
                else:
                    bits.append(0)
            else:
                # 이후 비트: 이전 상태와 비교
                if voltage[i] != voltage[i-1]:
                    bits.append(1)  # 전이 발생 = 1
                else:
                    bits.append(0)  # 전이 없음 = 0

        return bits

    def _decode_nrz_s(self, voltage: List[float]) -> List[int]:
        """NRZ-S 복호화: 전이 발생→0, 전이 없음→1"""
        bits = []

        for i in range(len(voltage)):
            if i == 0:
                if voltage[i] != self.initial_state:
                    bits.append(0)
                else:
                    bits.append(1)
            else:
                if voltage[i] != voltage[i-1]:
                    bits.append(0)  # 전이 발생 = 0
                else:
                    bits.append(1)  # 전이 없음 = 1

        return bits

    def count_transitions(self, voltage: List[float]) -> int:
        """신호 전이 횟수 계산"""
        transitions = 0
        for i in range(1, len(voltage)):
            if voltage[i] != voltage[i-1]:
                transitions += 1
        return transitions

    def calculate_dc_component(self, voltage: List[float]) -> float:
        """DC 성분 계산"""
        return sum(voltage) / len(voltage) if voltage else 0

    def analyze_run_length(self, voltage: List[float]) -> dict:
        """
        연속 동일 레벨 길이(Run Length) 분석
        동기화 능력 평가를 위한 지표
        """
        if not voltage:
            return {"max_run": 0, "avg_run": 0, "runs": []}

        runs = []
        current_run = 1

        for i in range(1, len(voltage)):
            if voltage[i] == voltage[i-1]:
                current_run += 1
            else:
                runs.append(current_run)
                current_run = 1

        runs.append(current_run)

        return {
            "max_run": max(runs),
            "avg_run": sum(runs) / len(runs),
            "runs": runs
        }


class ScrambledNRZCoder:
    """
    Scrambling이 적용된 NRZ 부호화
    USB 3.0, PCIe 3.0 등에서 사용되는 방식
    """

    def __init__(self, lfsr_seed: int = 0xFFFF, lfsr_polynomial: int = 0x8006):
        """
        Args:
            lfsr_seed: LFSR 초기값
            lfsr_polynomial: LFSR 다항식 (x^16 + x^5 + x^3 + x^2 + 1 = 0x8006)
        """
        self.lfsr = lfsr_seed
        self.polynomial = lfsr_polynomial
        self.nrz_coder = NRZCoder()

    def scramble(self, bits: List[int]) -> List[int]:
        """
        LFSR 기반 스크램블링
        연속된 0이나 1을 방지
        """
        scrambled = []

        for bit in bits:
            # LFSR 시프트 및 출력 비트 생성
            lfsr_bit = (self.lfsr >> 15) & 1
            self.lfsr = ((self.lfsr << 1) | lfsr_bit) & 0xFFFF

            # 입력 비트와 XOR
            scrambled_bit = bit ^ lfsr_bit
            scrambled.append(scrambled_bit)

        return scrambled

    def descramble(self, bits: List[int]) -> List[int]:
        """디스크램블링 (스크램블링과 동일 연산)"""
        return self.scramble(bits)  # XOR은 가역 연산

    def encode_with_scrambling(self, bits: List[int]) -> List[float]:
        """스크램블링 + NRZ-I 부호화"""
        scrambled = self.scramble(bits)
        return self.nrz_coder.encode(scrambled, NRZType.NRZ_I)

    def decode_with_descrambling(self, voltage: List[float]) -> List[int]:
        """NRZ-I 복호화 + 디스크램블링"""
        decoded = self.nrz_coder.decode(voltage, NRZType.NRZ_I)
        return self.descramble(decoded)


# ==================== 분석 및 시각화 ====================
def compare_nrz_types():
    """NRZ-L과 NRZ-I 비교 분석"""

    test_patterns = {
        "Alternating": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        "All Ones": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "All Zeros": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Long Zero Run": [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        "Mixed Pattern": [1, 0, 1, 1, 0, 0, 1, 0, 1, 1],
    }

    coder = NRZCoder()

    print("\n" + "="*90)
    print("NRZ-L vs NRZ-I Comparison Analysis")
    print("="*90)
    print(f"{'Pattern':<20} | {'Type':<8} | {'Transitions':<12} | {'DC Component':<14} | {'Max Run':<10}")
    print("-"*90)

    for pattern_name, bits in test_patterns.items():
        for nrz_type in [NRZType.NRZ_L, NRZType.NRZ_I]:
            voltage = coder.encode(bits, nrz_type)
            transitions = coder.count_transitions(voltage)
            dc = coder.calculate_dc_component(voltage)
            run_analysis = coder.analyze_run_length(voltage)

            print(f"{pattern_name:<20} | {nrz_type.value:<8} | {transitions:<12} | "
                  f"{dc:>+.3f}V        | {run_analysis['max_run']:<10}")

    print("="*90)


def demonstrate_polarity_inversion():
    """NRZ-I의 극성 반전 immunity 시연"""

    bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
    coder = NRZCoder()

    print("\n" + "="*70)
    print("Demonstration: NRZ-I Immunity to Polarity Inversion")
    print("="*70)

    # 원본 부호화
    original_voltage = coder.encode(bits, NRZType.NRZ_I)
    decoded_original = coder.decode(original_voltage, NRZType.NRZ_I)

    # 극성 반전 (선이 뒤집힌 경우)
    inverted_voltage = [-v for v in original_voltage]
    decoded_inverted = coder.decode(inverted_voltage, NRZType.NRZ_I)

    # NRZ-L 비교
    nrz_l_voltage = coder.encode(bits, NRZType.NRZ_L)
    inverted_nrz_l = [-v for v in nrz_l_voltage]
    decoded_nrz_l_original = coder.decode(nrz_l_voltage, NRZType.NRZ_L)
    decoded_nrz_l_inverted = coder.decode(inverted_nrz_l, NRZType.NRZ_L)

    print(f"\nOriginal Bits:       {bits}")
    print(f"\nNRZ-I Results:")
    print(f"  Decoded (Original): {decoded_original}")
    print(f"  Decoded (Inverted): {decoded_inverted}")
    print(f"  Match: {decoded_original == decoded_inverted == bits}")

    print(f"\nNRZ-L Results:")
    print(f"  Decoded (Original): {decoded_nrz_l_original}")
    print(f"  Decoded (Inverted): {decoded_nrz_l_inverted}")
    print(f"  Match: {decoded_nrz_l_original == bits}")
    print(f"  Inverted Error: {decoded_nrz_l_inverted != bits}")

    print("="*70)


def demonstrate_scrambling():
    """Scrambling 효과 시연"""

    # 긴 0 연속 패턴
    long_zero_pattern = [1] + [0] * 50 + [1]
    coder = ScrambledNRZCoder()

    print("\n" + "="*70)
    print("Effect of Scrambling on NRZ-I")
    print("="*70)

    # 스크램블링 없이
    plain_nrz = NRZCoder().encode(long_zero_pattern, NRZType.NRZ_I)
    plain_analysis = NRZCoder().analyze_run_length(plain_nrz)

    # 스크램블링과 함께
    scrambled_nrz = coder.encode_with_scrambling(long_zero_pattern)
    scrambled_analysis = NRZCoder().analyze_run_length(scrambled_nrz)

    print(f"\nInput Pattern: 1 followed by 50 zeros followed by 1")
    print(f"\nWithout Scrambling:")
    print(f"  Max Run Length: {plain_analysis['max_run']}")
    print(f"  Average Run Length: {plain_analysis['avg_run']:.2f}")

    print(f"\nWith Scrambling:")
    print(f"  Max Run Length: {scrambled_analysis['max_run']}")
    print(f"  Average Run Length: {scrambled_analysis['avg_run']:.2f}")

    print("\nScrambling reduces maximum run length significantly!")
    print("="*70)


# ==================== 실행 ====================
if __name__ == "__main__":
    compare_nrz_types()
    demonstrate_polarity_inversion()
    demonstrate_scrambling()
