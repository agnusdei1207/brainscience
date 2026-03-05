+++
title = "041. 차분 부호화 (Differential Encoding)"
description = "비트 값을 전압 레벨이 아닌 전압 변화로 표현하는 차분 부호화의 원리와 극성 반전에 대한 강건성을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["DifferentialEncoding", "NRZ-I", "PolarityInversion", "ConditionDInversion", "PhaseShiftKeying"]
categories = ["studynotes-3_network"]
+++

# 041. 차분 부호화 (Differential Encoding)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 차분 부호화(Differential Encoding)는 비트 값을 절대적 전압 레벨이 아닌, 현재 신호와 이전 신호의 상대적 변화(전이)로 인코딩하는 방식으로, 1은 신호 반전, 0은 신호 유지 등으로 표현합니다.
> 2. **가치**: 차분 부호화는 신호의 절대적 극성이나 위상이 반전되어도 데이터가 보존되는 'Ambiguity Resolution' 특성을 제공하여, 크로스오버 케이블, 위상 동기 불확실성, 무선 채널의 위상 모호성 문제를 해결합니다.
> 3. **융합**: 차분 부호화는 NRZ-I(USB, SATA), Differential Manchester(Token Ring), DPSK(Differential Phase Shift Keying, 위성 통신) 등 다양한 유무선 통신 시스템에서 핵심 기술로 활용됩니다.

---

## I. 개요 (Context & Background)

차분 부호화(Differential Encoding)는 디지털 통신에서 비트 값을 표현할 때, 절대적인 신호 레벨(+V, -V, 위상 0도, 180도 등) 대신 **신호의 변화(Transition) 또는 비변화(Non-transition)**로 정보를 인코딩하는 기술입니다. 예를 들어, NRZ-I에서는 1이 들어오면 현재 전압을 반전시키고, 0이 들어오면 현재 전압을 유지합니다.

**💡 비유**: 차분 부호화는 **'에스컬레이터에서의 움직임'**과 같습니다.
- 절대 부호화(NRZ-L): "2층에 있으면 1, 1층에 있으면 0" - 현재 위치가 데이터
- 차분 부호화(NRZ-I): "움직이면(위아래로 전이하면) 1, 가만히 있으면 0" - 움직임이 데이터
- 에스컬레이터 방향이 반대로 되어 있어도(극성 반전), 움직였는지 안 움직였는지는 동일하게 관찰됩니다.

**등장 배경 및 발전 과정**:
1. **모뎀 통신의 위상 모호성 (1960년대)**: 초기 모뎀은 위상 변조(PSK)를 사용했는데, 수신측에서 송신측의 기준 위상을 알 수 없어 0도와 180도를 구분하지 못했습니다. 차분 위상 변조(DPSK)가 이 문제를 해결했습니다.
2. **시리얼 인터페이스 표준화 (1980~90년대)**: USB, SATA, PCI Express 등의 고속 직렬 인터페이스에서 NRZ-I가 채택되었습니다. 케이블 연결 방향(정상/크로스오버)에 관계없이 데이터가 보존되어야 했기 때문입니다.
3. **무선 통신 확산 (2000년대~현재)**: 무선 채널은 위상 왜곡이 심하여 차등 검출(Differential Detection)이 유리한 경우가 많습니다. π/4-DQPSK, D8PSK 등이 디지털 이동통신과 위성 통신에 사용됩니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 부호화 방식 | 0 표현 | 1 표현 | 동기화 능력 | 극성 반전 내성 | 오버헤드 | 적용 분야 |
|------------|-------|-------|-----------|--------------|----------|----------|
| **NRZ-I** | 유지 (No Change) | 반전 (Invert) | 중간 | 우수 | 0% | USB, SATA, PCIe |
| **NRZ-M (Mark)** | 유지 | 반전 | 중간 | 우수 | 0% | 자기 테이프 |
| **NRZ-S (Space)** | 반전 | 유지 | 중간 | 우수 | 0% | 특수 응용 |
| **Differential Manchester** | 경계 전이 | 경계 비전이 | 우수 | 우수 | 100% | Token Ring |
| **DPSK** | 위상 유지 | 위상 시프트 | 우수 | 우수 | 0% | 위성, 무선 |

### 정교한 구조 다이어그램: 차분 부호화 원리

```ascii
================================================================================
[ Differential Encoding Principle ]
================================================================================

Encoding Rule (NRZ-I Convention):
  - Logic 1: INVERT the current signal level
  - Logic 0: MAINTAIN the current signal level

Input Bit Stream:   1    0    1    1    0    0    1    0    1    1

================================================================================
[ Normal Transmission (Correct Polarity) ]
================================================================================

Initial State: +V

Voltage
   +V  |  +--+----+             +----+             +----+----+----+
       |  |  |    |             |    |             |    |    |    |
   0V  |  |  |    |             |    |             |    |    |    |
       |  |  |    |             |    |             |    |    |    |
   -V  |  |  |    +-------------+    +-------------+    |    |    |
       |  |           |                   |            |    |    |
       +------------------------------------------------------------------> Time
            b1   b2   b3   b4   b5   b6   b7   b8   b9  b10

Encoding Process:
  Start: +V
  b1 = 1 → Invert +V to -V
  b2 = 0 → Maintain -V
  b3 = 1 → Invert -V to +V
  b4 = 1 → Invert +V to -V
  b5 = 0 → Maintain -V
  b6 = 0 → Maintain -V
  b7 = 1 → Invert -V to +V
  b8 = 0 → Maintain +V
  b9 = 1 → Invert +V to -V
  b10 = 1 → Invert -V to +V

Decoding (based on transitions):
  b1: Transition at start → 1
  b2: No transition → 0
  b3: Transition → 1
  b4: Transition → 1
  b5: No transition → 0
  b6: No transition → 0
  b7: Transition → 1
  b8: No transition → 0
  b9: Transition → 1
  b10: Transition → 1

Decoded: [1, 0, 1, 1, 0, 0, 1, 0, 1, 1] ✓ MATCHES INPUT!

================================================================================
[ Polarity Inversion Scenario (Crossover Cable) ]
================================================================================

Imagine: Wires are swapped (+ becomes -, - becomes +)

Original Signal:                  After Wire Swap (Inverted):
   +V  |  +--+----+                     -V  |  --+----+
       |  |  |    |                         |  |  |    |
   -V  |  |  |    +--                       +V  |  |    +--
       +-----------> Time                       +-----------> Time

Signal is COMPLETELY INVERTED!

================================================================================
[ NRZ-L (Level) Decoding with Polarity Inversion - FAILURE ]
================================================================================

Original NRZ-L Encoding (1=+V, 0=-V):
Input: [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]

   +V  |  +--+       +----+----+             +----+    +----+----+
       |  |  |       |    |    |             |    |    |    |    |
   -V  |  |  +-------+    |    +-------------+    +----+    |    +-->
       +------------------------------------------------------------------> Time

After Polarity Inversion:
   +V  |  |  +-------+    |    +-------------+    +----+    |    +-->
       |  |  |       |    |    |             |    |    |    |    |
   -V  |  +--+       +----+----+             +----+    +----+----+
       +------------------------------------------------------------------> Time

NRZ-L Decoding (1=+V, 0=-V):
  b1: -V → Decoded as 0 (WRONG! Should be 1)
  b2: +V → Decoded as 1 (WRONG! Should be 0)
  b3: -V → Decoded as 0 (WRONG! Should be 1)
  ...

Decoded: [0, 1, 0, 0, 1, 1, 0, 1, 0, 0] ✗ ALL BITS INVERTED!

================================================================================
[ NRZ-I (Differential) Decoding with Polarity Inversion - SUCCESS ]
================================================================================

Original NRZ-I Signal:
   +V  |  +--+----+             +----+             +----+----+----+
       |  |  |    |             |    |             |    |    |    |
   -V  |  |  |    +-------------+    +-------------+    |    |    |
       +------------------------------------------------------------------> Time

After Polarity Inversion (all levels flipped):
   +V  |  |  |    +-------------+    +-------------+    |    |    |
       |  |  |    |             |    |             |    |    |    |
   -V  |  +--+----+             +----+             +----+----+----+
       +------------------------------------------------------------------> Time

NRZ-I Decoding (look at TRANSITIONS, not levels):
  b1: Transition occurs (even though inverted, still a transition) → 1 ✓
  b2: No transition → 0 ✓
  b3: Transition → 1 ✓
  b4: Transition → 1 ✓
  b5: No transition → 0 ✓
  b6: No transition → 0 ✓
  b7: Transition → 1 ✓
  b8: No transition → 0 ✓
  b9: Transition → 1 ✓
  b10: Transition → 1 ✓

Decoded: [1, 0, 1, 1, 0, 0, 1, 0, 1, 1] ✓ CORRECT!

KEY INSIGHT:
  Differential encoding uses TRANSITIONS, not LEVELS.
  A transition is still a transition whether +V→-V or -V→+V.
  Therefore, polarity inversion does NOT affect the decoded data!

================================================================================
[ Comparison: Absolute vs Differential Encoding ]
================================================================================

                     Absolute Encoding (NRZ-L)    Differential Encoding (NRZ-I)
                     -------------------------    -----------------------------
Data Representation: Signal Level                 Signal Change
Bit 0:               Fixed level (-V)             No change
Bit 1:               Fixed level (+V)             Change (invert)

Polarity Inversion:
  Original:          Data corrupted               Data preserved ✓
  (wire swap)

Phase Ambiguity:
  (180° rotation)    Data corrupted               Data preserved ✓

Reference Needed:    Yes (absolute ref)           No (relative change)

Self-Clocking:       Poor                         Poor (same as NRZ-L)

Complexity:          Simple                       Simple + state memory

================================================================================
```

### 심층 동작 원리: 5가지 핵심 메커니즘

1. **상태 기반 인코딩 (State-Based Encoding)**:
   - **핵심 원리**: 인코더는 '현재 상태'를 기억하고, 입력 비트에 따라 상태를 변경하거나 유지합니다.
   - **구현**: 1비트 상태 변수(현재 전압: +V 또는 -V)와 XOR 게이트로 구현합니다.
   - **수학적 표현**: `y[n] = y[n-1] XOR x[n]` (where x[n] is input bit, y[n] is output level)

2. **전이 기반 디코딩 (Transition-Based Decoding)**:
   - **핵심 원리**: 디코더는 신호 레벨이 아닌 전이 발생 여부를 관찰합니다.
   - **구현**: 현재 샘플과 이전 샘플을 비교하여 전이 여부 판단.
   - **수학적 표현**: `x[n] = 1 if y[n] ≠ y[n-1], else 0`

3. **극성 반전 내성 (Polarity Inversion Immunity)**:
   - **문제 상황**: 케이블 연결 오류, 트랜스포머 반전, 차등 신호의 +/- 교환
   - **해결 원리**: 전이는 방향성(+→- 또는 -→+)이 중요하지 않고 '전이 발생' 자체가 중요합니다.
   - **실무 이점**: USB, SATA 등에서 케이블 방향에 무관하게 동작합니다.

4. **위상 모호성 해결 (Phase Ambiguity Resolution)**:
   - **문제 상황**: PSK 변조에서 수신측이 기준 위상을 모르면 0°와 180°를 구분 못함.
   - **DPSK 해결**: 위상 절대값이 아닌 위상 변화로 데이터를 인코딩합니다.
   - **예시**: D-BPSK에서 1은 180° 위상 시프트, 0은 위상 유지.

5. **초기 상태 모호성 (Initial State Ambiguity)**:
   - **문제**: 수신측은 인코더의 초기 상태(+V 또는 -V)를 모릅니다.
   - **영향**: 첫 비트가 잘못 디코딩될 수 있습니다.
   - **해결책**:
     - 프리앰블(Preamble): 알려진 패턴으로 초기 상태 동기화
     - 차등 디코딩의 특성: 한 비트 오류 후 자동으로 동기화됨

### 핵심 코드: 차분 부호화/복호화 구현 (Python)

```python
from enum import Enum
from typing import List, Tuple
import numpy as np

class DifferentialType(Enum):
    """차분 부호화 타입"""
    NRZ_I = "NRZ-I"      # 1=Invert, 0=Maintain
    NRZ_M = "NRZ-M"      # Same as NRZ-I (Mark)
    NRZ_S = "NRZ-S"      # 0=Invert, 1=Maintain (Space)

class DifferentialCoder:
    """
    차분 부호화 구현

    특징:
    - 비트 값을 전압 레벨이 아닌 전압 변화로 인코딩
    - 극성 반전에 강건함 (Ambiguity Resolution)
    - 위상 모호성 문제 해결
    """

    def __init__(self, voltage_level: float = 1.0, initial_state: float = 1.0):
        """
        Args:
            voltage_level: 기준 전압 레벨
            initial_state: 초기 상태 (+V 또는 -V)
        """
        self.V = voltage_level
        self.initial_state = initial_state

    def encode(self, bits: List[int], diff_type: DifferentialType = DifferentialType.NRZ_I) -> np.ndarray:
        """
        차분 부호화

        Args:
            bits: 입력 비트 리스트
            diff_type: 차분 부호화 타입

        Returns:
            전압 레벨 배열
        """
        voltage = []
        current = self.initial_state

        for bit in bits:
            if diff_type == DifferentialType.NRZ_I or diff_type == DifferentialType.NRZ_M:
                # NRZ-I: 1이면 반전, 0이면 유지
                if bit == 1:
                    current = -current
            elif diff_type == DifferentialType.NRZ_S:
                # NRZ-S: 0이면 반전, 1이면 유지
                if bit == 0:
                    current = -current

            voltage.append(current)

        return np.array(voltage)

    def decode(self, voltage: np.ndarray, diff_type: DifferentialType = DifferentialType.NRZ_I) -> List[int]:
        """
        차분 복호화 (전이 기반)

        Args:
            voltage: 수신된 전압 레벨 배열
            diff_type: 차분 부호화 타입

        Returns:
            복호화된 비트 리스트
        """
        bits = []
        prev = self.initial_state

        for curr in voltage:
            if diff_type == DifferentialType.NRZ_I or diff_type == DifferentialType.NRZ_M:
                # 전이 발생 = 1, 전이 없음 = 0
                if curr != prev:
                    bits.append(1)
                else:
                    bits.append(0)
            elif diff_type == DifferentialType.NRZ_S:
                # 전이 발생 = 0, 전이 없음 = 1
                if curr != prev:
                    bits.append(0)
                else:
                    bits.append(1)

            prev = curr

        return bits

    def encode_with_preamble(self, bits: List[int], preamble: List[int] = [1, 0, 1, 0]) -> np.ndarray:
        """
        프리앰블을 포함한 차분 부호화

        프리앰블을 통해 수신측의 초기 상태 동기화 지원
        """
        full_bits = preamble + bits
        return self.encode(full_bits)

    def decode_with_preamble(self, voltage: np.ndarray, preamble_length: int = 4) -> List[int]:
        """
        프리앰블을 제거한 차분 복호화
        """
        all_bits = self.decode(voltage)
        return all_bits[preamble_length:]


class DPSKCoder:
    """
    DPSK (Differential Phase Shift Keying) 구현

    위상 변조에서의 차분 부호화
    위상 모호성(Phase Ambiguity) 문제 해결
    """

    def __init__(self):
        self.initial_phase = 0  # 초기 위상 (라디안)

    def encode_dbpsk(self, bits: List[int]) -> np.ndarray:
        """
        D-BPSK (Differential Binary PSK) 부호화

        1: 180° 위상 시프트 (π)
        0: 위상 유지 (0)
        """
        phases = []
        current_phase = self.initial_phase

        for bit in bits:
            if bit == 1:
                current_phase = (current_phase + np.pi) % (2 * np.pi)
            # 0이면 위상 유지
            phases.append(current_phase)

        return np.array(phases)

    def decode_dbpsk(self, phases: np.ndarray) -> List[int]:
        """
        D-BPSK 복호화 (차등 검출)

        위상 변화가 있으면 1, 없으면 0
        """
        bits = []
        prev_phase = self.initial_phase

        for curr_phase in phases:
            # 위상 차이 계산 (정규화)
            phase_diff = (curr_phase - prev_phase) % (2 * np.pi)

            # π에 가까우면 (180° 시프트) → 1
            if abs(phase_diff - np.pi) < np.pi / 4:
                bits.append(1)
            else:
                bits.append(0)

            prev_phase = curr_phase

        return bits

    def encode_dqpsk(self, symbols: List[int]) -> np.ndarray:
        """
        D-QPSK (Differential QPSK) 부호화

        각 심볼(0, 1, 2, 3)은 90°씩의 위상 시프트에 매핑
        """
        phase_shifts = [0, np.pi / 2, np.pi, 3 * np.pi / 2]  # 00, 01, 11, 10
        phases = []
        current_phase = self.initial_phase

        for symbol in symbols:
            current_phase = (current_phase + phase_shifts[symbol]) % (2 * np.pi)
            phases.append(current_phase)

        return np.array(phases)


def demonstrate_polarity_inversion():
    """극성 반전 시나리오 시연"""

    print("\n" + "="*70)
    print("Demonstration: Polarity Inversion Immunity")
    print("="*70)

    test_bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
    coder = DifferentialCoder()

    # 정상 부호화
    normal_wave = coder.encode(test_bits)
    decoded_normal = coder.decode(normal_wave)

    # 극성 반전 (케이블 교차)
    inverted_wave = -normal_wave  # 모든 레벨 반전
    decoded_inverted = coder.decode(inverted_wave)

    print(f"\nOriginal Bits:     {test_bits}")
    print(f"Normal Wave:       {[f'{v:+.0f}' for v in normal_wave]}")
    print(f"Inverted Wave:     {[f'{v:+.0f}' for v in inverted_wave]}")
    print(f"\nDecoded (Normal):  {decoded_normal}")
    print(f"Decoded (Inverted):{decoded_inverted}")

    print(f"\nOriginal matches decoded (normal): {test_bits == decoded_normal}")
    print(f"Original matches decoded (inverted): {test_bits == decoded_inverted}")

    if test_bits == decoded_inverted:
        print("\n✓ SUCCESS: Differential encoding preserves data despite polarity inversion!")
    else:
        print("\n✗ FAILURE: Something went wrong!")

    print("="*70)


def compare_absolute_vs_differential():
    """절대 부호화 vs 차분 부호화 비교"""

    print("\n" + "="*70)
    print("Comparison: Absolute (NRZ-L) vs Differential (NRZ-I) Encoding")
    print("="*70)

    test_bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
    diff_coder = DifferentialCoder()

    # NRZ-L (절대 부호화)
    nrz_l_wave = np.array([1 if b == 1 else -1 for b in test_bits])

    # NRZ-I (차분 부호화)
    nrz_i_wave = diff_coder.encode(test_bits)

    # 극성 반전
    nrz_l_inverted = -nrz_l_wave
    nrz_i_inverted = -nrz_i_wave

    # NRZ-L 복호화 (절대 레벨 기반)
    nrz_l_decoded_normal = [1 if v > 0 else 0 for v in nrz_l_wave]
    nrz_l_decoded_inverted = [1 if v > 0 else 0 for v in nrz_l_inverted]

    # NRZ-I 복호화 (전이 기반)
    nrz_i_decoded_normal = diff_coder.decode(nrz_i_wave)
    nrz_i_decoded_inverted = diff_coder.decode(nrz_i_inverted)

    print(f"\nInput Bits:        {test_bits}")
    print(f"\n{'Scenario':<25} | {'NRZ-L':<20} | {'NRZ-I':<20}")
    print("-"*70)
    print(f"{'Normal Transmission':<25} | {nrz_l_decoded_normal == test_bits!s:<20} | {nrz_i_decoded_normal == test_bits!s:<20}")
    print(f"{'Polarity Inverted':<25} | {nrz_l_decoded_inverted == test_bits!s:<20} | {nrz_i_decoded_inverted == test_bits!s:<20}")

    print("\nConclusion:")
    print("  NRZ-L (Absolute): Data corrupted on polarity inversion")
    print("  NRZ-I (Differential): Data preserved on polarity inversion")

    print("="*70)


def demonstrate_phase_ambiguity():
    """위상 모호성 해결 시연"""

    print("\n" + "="*70)
    print("Demonstration: Phase Ambiguity Resolution with DPSK")
    print("="*70)

    test_bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
    dpsk = DPSKCoder()

    # D-BPSK 부호화
    phases = dpsk.encode_dbpsk(test_bits)

    # 위상 모호성 시뮬레이션 (180° 위상 오프셋)
    phases_with_offset = (phases + np.pi) % (2 * np.pi)

    # 차등 검출
    decoded_normal = dpsk.decode_dbpsk(phases)
    decoded_with_offset = dpsk.decode_dbpsk(phases_with_offset)

    print(f"\nInput Bits:        {test_bits}")
    print(f"\nDecoded (Normal):  {decoded_normal}")
    print(f"Decoded (180° off):{decoded_with_offset}")

    print(f"\nNormal decoding correct: {test_bits == decoded_normal}")
    print(f"Offset decoding correct: {test_bits == decoded_with_offset}")

    if test_bits == decoded_with_offset:
        print("\n✓ DPSK resolves phase ambiguity - data preserved!")

    print("="*70)


# ==================== 실행 ====================
if __name__ == "__main__":
    demonstrate_polarity_inversion()
    compare_absolute_vs_differential()
    demonstrate_phase_ambiguity()
