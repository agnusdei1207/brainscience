+++
title = "038. RZ 부호화 (Return to Zero Coding)"
description = "비트 구간 중간에 0 레벨로 복귀하는 RZ 부호화의 동작 원리, 동기화 장점, 대역폭 단점을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["RZ", "ReturnToZero", "LineCoding", "Encoding", "Synchronization", "ClockRecovery", "Optical"]
categories = ["studynotes-3_network"]
+++

# 038. RZ 부호화 (Return to Zero Coding)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RZ(Return to Zero) 부호화는 각 비트 구간의 후반부를 항상 0 레벨(무신호)로 유지하는 선로 부호화 방식으로, 비트마다 신호 전이를 보장하여 수신측의 클럭 복구 능력을 극대화합니다.
> 2. **가치**: RZ는 모든 비트에서 전이(Transition)가 발생하므로 동기화 능력이 가장 우수하며, 광섬유 통신과 일부 무선 시스템에서 펄스 형태의 신호 전송에 활용됩니다.
> 3. **융합**: RZ의 동기화 장점은 맨체스터 부호화로 계승되었으며, 광통신에서는 RZ 펄스 형태가 CSRZ, RZ-DQPSK 등의 고급 변조 방식으로 진화하여 장거리 고속 전송에 활용됩니다.

---

## I. 개요 (Context & Background)

RZ(Return to Zero) 부호화는 각 비트 구간(Bit Period) 동안 신호가 반드시 0 레벨(무신호 또는 기준 레벨)로 복귀(Return)하는 선로 부호화 방식입니다. 일반적으로 비트 구간의 전반부에만 정보를 싣고, 후반부는 0 레벨로 유지합니다. 이로 인해 **모든 비트에서 신호 전이(Transition)가 발생**하므로 수신측의 클럭 복구가 매우 용이합니다.

**💡 비유**: RZ 부호화는 **'모스 부호의 짧은 펄스'**와 같습니다.
- 모스 부호에서 '·'(짧은 신호)와 '-'(긴 신호)는 모두 신호가 끝나면 무음 상태로 돌아갑니다.
- RZ도 마찬가지로, 비트 값(0 또는 1)을 짧은 펄스로 표현한 후 반드시 0 레벨로 돌아갑니다.
- 마치 숫자를 셀 때 손가락을 폈다가 접는 동작을 반복하는 것과 같습니다. 숫자를 표시한 후 항상 기본 상태로 돌아오죠.

**등장 배경 및 발전 과정**:
1. **초기 전신 및 무선 통신 (1900년대)**: 스파크 갭 송신기와 초기 무선 장비는 펄스 형태의 신호를 생성했습니다. 이는 자연스럽게 RZ 형태였습니다.
2. **디지털 통신의 발전 (1960~70년대)**: NRZ의 동기화 문제를 해결하기 위해 RZ가 고려되었지만, 대역폭 요구량이 두 배로 증가한다는 단점으로 인해 널리 채택되지는 않았습니다.
3. **광섬유 통신 (1980년대~현재)**: 광섬유에서는 레이저를 켜고 끄는 펄스 형태가 자연스럽습니다. RZ 펄스는 타이밍 정보를 명확히 제공하므로 장거리 고속 광통신(WDM, OTN)에서 여전히 사용됩니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 부호화 방식 | 비트 표현 | 신호 전이 | DC 성분 | 대역폭 요구 | 동기화 능력 | 적용 분야 |
|------------|----------|----------|---------|------------|-----------|----------|
| **Unipolar RZ** | 1=+V→0V, 0=0V | 1에서만 | 존재 | 2x Bit Rate | 중간 | 초기 시스템 |
| **Polar RZ** | 1=+V→0V, 0=-V→0V | 모든 비트 | 0 (이상적) | 2x Bit Rate | 우수 | 광섬유, 연구용 |
| **Bipolar RZ** | 1=±V→0V 교대, 0=0V | 1에서만 | 0 | 2x Bit Rate | 우수 | 특수 응용 |

### 정교한 구조 다이어그램: RZ 파형 분석

```ascii
================================================================================
[ Unipolar RZ (Return to Zero) Waveform ]
================================================================================

Input Bit Stream:   1    0    1    1    0    0    1    0    1    1
                   |    |    |    |    |    |    |    |    |    |

Voltage
   +V  |  +--+       +--+  +--+             +--+       +--+  +--+
       |  |  |       |  |  |  |             |  |       |  |  |  |
   0V  |--+  +-------+  +--+  +-------------+  +-------+  +--+  +-->
       |
       +------------------------------------------------------------------> Time
            |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
            |<-T/2->|<-- T/2 -->|
            |<- 1 bit period (T) -->|

Rule:
  - Logic 1: +V for first half, 0V for second half
  - Logic 0: 0V for entire bit period

Characteristics:
  - Transitions only for logic 1 (two transitions: +V→0V and 0V→+V at next 1)
  - Logic 0 has no transitions (synchronization problem for consecutive 0s)
  - DC component: non-zero (depends on ratio of 1s to 0s)

================================================================================
[ Polar RZ (Return to Zero) Waveform ]
================================================================================

Input Bit Stream:   1    0    1    1    0    0    1    0    1    1

Voltage
   +V  |  +--+              +--+  +--+             +--+       +--+  +--+
       |  |  |              |  |  |  |             |  |       |  |  |  |
   0V  |--+  +--+-----------+  +--+  +--+----------+  +-------+  +--+  |
       |     |  |          |          |  |         |                   |
   -V  |     +--+----------+          +--+---------+                   +-->
       |
       +------------------------------------------------------------------> Time

Rule:
  - Logic 1: +V for first half, 0V for second half
  - Logic 0: -V for first half, 0V for second half

Characteristics:
  - GUARANTEED transitions for EVERY bit! (Best synchronization)
  - Two transitions per bit: at start and mid-bit
  - DC component: ideally zero (if balanced 1s and 0s)

Transitions Analysis:
  Bit 1: 0→+V (start), +V→0 (mid)
  Bit 0: 0→-V (start), -V→0 (mid)
  Total: 4 transitions per 2 bits = 2 transitions per bit

================================================================================
[ Bandwidth Comparison: NRZ vs RZ ]
================================================================================

Power Spectral Density (PSD)

Power
  |
  |    NRZ (Non-Return to Zero)
  |      /\
  |     /  \
  |    /    \______________
  |   /                      \___________
  |  /                                    \
  | /                                       \
  |/__________________________________________\________ Frequency
  0        1/(2T)     1/T      3/(2T)     2/T
  |<-- Main lobe: 0 to 1/T -->|

  |
  |    RZ (Return to Zero)
  |           /\
  |          /  \
  |         /    \
  |    ___ /      \    ___
  |   /   |        \ /   \
  |  /    |         X     \      (Null at 1/T removed!)
  | /     |        / \     \___
  |/______|_______/   \___________\_____ Frequency
  0       |       |           |
       1/(2T)   1/T         2/T
  |<-- Main lobe extends to 2/T -->|

Key Observations:
  - RZ bandwidth is approximately 2x that of NRZ
  - NRZ first null at f = 1/T (bit rate)
  - RZ first null at f = 2/T (twice bit rate)
  - RZ has more high-frequency components

================================================================================
[ Timing Diagram: Clock Recovery Comparison ]
================================================================================

Case: Long run of alternating bits (10101010...)

NRZ Signal:
  +V  |--+  +--+  +--+  +--+  +--
      |  |  |  |  |  |  |  |  |
  -V  |  +--+  +--+  +--+  +--+
      +------------------------------> Time
        1 0  1 0  1 0  1 0

  Transitions: At every bit boundary
  Clock Recovery: EXCELLENT (one transition per bit)

RZ Signal:
  +V  |+--+  +--+  +--+  +--+  +--
      |  |  |  |  |  |  |  |  |
  0V  |  +--+  +--+  +--+  +--+
  -V  |
      +------------------------------> Time
        1 0  1 0  1 0  1 0

  Transitions: At start and mid-bit of every bit
  Clock Recovery: SUPERIOR (two transitions per bit)

Case: Long run of zeros (00000000...)

NRZ Signal:
  +V  |
      |
  -V  |--------------------------------
      +------------------------------> Time
        0  0  0  0  0  0  0  0

  Transitions: NONE!
  Clock Recovery: FAILED (clock drift inevitable)

Polar RZ Signal:
  +V  |
      |
  0V  |  +--+  +--+  +--+  +--+  +--+
      |  |  |  |  |  |  |  |  |  |  |
  -V  |  |  |  |  |  |  |  |  |  |  |
      +--+  +--+  +--+  +--+  +--+  --> Time
        0    0    0    0    0    0

  Transitions: At start and mid-bit of EVERY bit!
  Clock Recovery: EXCELLENT (maintained for all-zeros)

================================================================================
```

### 심층 동작 원리: 5가지 핵심 메커니즘

1. **비트 내 펄스 생성 (Pulse Generation within Bit)**:
   - **RZ의 핵심**: 비트 구간 T의 전반부(T/2)에만 정보를 싣고, 후반부는 0 레벨로 유지합니다.
   - **듀티 사이클**: RZ는 50% 듀티 사이클(펄스 폭 = T/2)을 가집니다.
   - **펄스 형태**: Unipolar RZ는 양의 펄스만, Polar RZ는 양/음 펄스를 모두 사용합니다.

2. **보장된 신호 전이 (Guaranteed Transitions)**:
   - **Polar RZ의 장점**: 모든 비트(0과 1 모두)에서 최소 2회의 전이가 발생합니다.
     - 비트 시작: 0V → ±V
     - 비트 중간: ±V → 0V
   - **동기화 보장**: 클럭 복구 회로(PLL, CDR)가 모든 비트에서 기준 신호를 얻습니다.

3. **대역폭 요구 증가 (Increased Bandwidth Requirement)**:
   - **주파수 스펙트럼**: RZ 신호는 NRZ 대비 2배의 대역폭을 필요로 합니다.
   - **수학적 분석**: 펄스 폭이 T/2이므로, 첫 번째 널(Null) 주파수는 f = 2/T입니다.
   - **실무 영향**: 동일한 비트 레이트를 전송하려면 NRZ보다 2배 빠른 샘플링이 필요합니다.

4. **DC 밸런스 (DC Balance)**:
   - **Polar RZ**: 이상적으로 DC 성분이 0입니다. +V 펄스와 -V 펄스의 평균이 0V이기 때문입니다.
   - **Unipolar RZ**: DC 성분이 존재합니다. 1과 0의 비율에 따라 DC 레벨이 변동합니다.

5. **광섬유 적용 (Optical Fiber Application)**:
   - **레이저 구동**: 레이저 다이오드는 켜짐(ON)과 꺼짐(OFF) 상태만 가집니다. 이는 Unipolar RZ와 유사합니다.
   - **RZ vs NRZ in Optical**:
     - NRZ: 레이저가 비트 구간 전체 동안 켜져 있음 → 평균 광전력 높음
     - RZ: 레이저가 반 구간만 켜짐 → 평균 광전력 낮음, 비선형 효과 감소

### 핵심 코드: RZ 부호화 구현 (Python)

```python
from enum import Enum
from typing import List, Tuple
import numpy as np

class RZType(Enum):
    """RZ 부호화 타입"""
    UNIPOLAR_RZ = "Unipolar RZ"
    POLAR_RZ = "Polar RZ"
    BIPOLAR_RZ = "Bipolar RZ"

class RZCoder:
    """
    RZ (Return to Zero) 부호화 구현

    특징:
    - 비트 구간의 전반부에만 정보를 싣고 후반부는 0V로 유지
    - Polar RZ는 모든 비트에서 전이를 보장하여 동기화 능력 우수
    - 대역폭 요구량이 NRZ의 2배
    """

    def __init__(self, voltage_level: float = 1.0, samples_per_bit: int = 100):
        """
        Args:
            voltage_level: 기준 전압 레벨 (V)
            samples_per_bit: 비트당 샘플 수
        """
        self.V = voltage_level
        self.samples_per_bit = samples_per_bit
        self.half_samples = samples_per_bit // 2

    def encode(self, bits: List[int], rz_type: RZType) -> np.ndarray:
        """
        RZ 부호화

        Args:
            bits: 입력 비트 리스트
            rz_type: RZ 부호화 타입

        Returns:
            전압 레벨 배열 (파형)
        """
        if rz_type == RZType.UNIPOLAR_RZ:
            return self._encode_unipolar_rz(bits)
        elif rz_type == RZType.POLAR_RZ:
            return self._encode_polar_rz(bits)
        elif rz_type == RZType.BIPOLAR_RZ:
            return self._encode_bipolar_rz(bits)
        else:
            raise ValueError(f"Unknown RZ type: {rz_type}")

    def _encode_unipolar_rz(self, bits: List[int]) -> np.ndarray:
        """
        Unipolar RZ 부호화
        1: +V → 0V (전반부 +V, 후반부 0V)
        0: 0V → 0V (전체 0V)
        """
        waveform = np.array([])

        for bit in bits:
            if bit == 1:
                # 전반부: +V, 후반부: 0V
                waveform = np.append(waveform, np.full(self.half_samples, self.V))
                waveform = np.append(waveform, np.zeros(self.half_samples))
            else:
                # 전체: 0V
                waveform = np.append(waveform, np.zeros(self.samples_per_bit))

        return waveform

    def _encode_polar_rz(self, bits: List[int]) -> np.ndarray:
        """
        Polar RZ 부호화
        1: +V → 0V (전반부 +V, 후반부 0V)
        0: -V → 0V (전반부 -V, 후반부 0V)
        """
        waveform = np.array([])

        for bit in bits:
            if bit == 1:
                # 전반부: +V, 후반부: 0V
                waveform = np.append(waveform, np.full(self.half_samples, self.V))
                waveform = np.append(waveform, np.zeros(self.half_samples))
            else:
                # 전반부: -V, 후반부: 0V
                waveform = np.append(waveform, np.full(self.half_samples, -self.V))
                waveform = np.append(waveform, np.zeros(self.half_samples))

        return waveform

    def _encode_bipolar_rz(self, bits: List[int]) -> np.ndarray:
        """
        Bipolar RZ 부호화 (AMI와 RZ 결합)
        0: 0V → 0V (전체 0V)
        1: ±V → 0V (전반부 ±V 교대, 후반부 0V)
        """
        waveform = np.array([])
        last_mark = -self.V  # 직전 1의 극성

        for bit in bits:
            if bit == 1:
                # 극성 교대
                last_mark = -last_mark
                waveform = np.append(waveform, np.full(self.half_samples, last_mark))
                waveform = np.append(waveform, np.zeros(self.half_samples))
            else:
                waveform = np.append(waveform, np.zeros(self.samples_per_bit))

        return waveform

    def decode(self, waveform: np.ndarray, rz_type: RZType) -> List[int]:
        """
        RZ 복호화

        비트 구간의 전반부 중앙에서 샘플링하여 비트 값 판별
        """
        bits = []
        n_bits = len(waveform) // self.samples_per_bit

        # 샘플링 포인트: 각 비트의 1/4 지점 (전반부 중앙)
        sample_point = self.samples_per_bit // 4

        for i in range(n_bits):
            start = i * self.samples_per_bit
            sample = waveform[start + sample_point]

            if rz_type == RZType.UNIPOLAR_RZ:
                bit = 1 if sample > self.V * 0.5 else 0
            elif rz_type == RZType.POLAR_RZ:
                bit = 1 if sample > 0 else 0
            elif rz_type == RZType.BIPOLAR_RZ:
                bit = 1 if abs(sample) > self.V * 0.5 else 0
            else:
                raise ValueError(f"Unknown RZ type: {rz_type}")

            bits.append(bit)

        return bits

    def count_transitions(self, waveform: np.ndarray) -> int:
        """신호 전이 횟수 계산"""
        diff = np.diff(waveform)
        threshold = self.V * 0.1  # 작은 임계값
        transitions = np.sum(np.abs(diff) > threshold)
        return int(transitions)

    def calculate_dc_component(self, waveform: np.ndarray) -> float:
        """DC 성분 계산"""
        return float(np.mean(waveform))

    def analyze_synchronization_quality(self, bits: List[int], rz_type: RZType) -> dict:
        """
        동기화 품질 분석

        Returns:
            max_zero_run: 연속 0의 최대 길이 (Unipolar RZ에서 문제)
            max_one_run: 연속 1의 최대 길이
            transitions_per_bit: 비트당 평균 전이 횟수
        """
        waveform = self.encode(bits, rz_type)
        transitions = self.count_transitions(waveform)
        transitions_per_bit = transitions / len(bits) if bits else 0

        # 연속 동일 비트 길이 분석
        max_zero_run = 0
        max_one_run = 0
        current_zero_run = 0
        current_one_run = 0

        for bit in bits:
            if bit == 0:
                current_zero_run += 1
                current_one_run = 0
                max_zero_run = max(max_zero_run, current_zero_run)
            else:
                current_one_run += 1
                current_zero_run = 0
                max_one_run = max(max_one_run, current_one_run)

        return {
            "max_zero_run": max_zero_run,
            "max_one_run": max_one_run,
            "transitions_per_bit": transitions_per_bit,
            "dc_component": self.calculate_dc_component(waveform)
        }


def compare_nrz_vs_rz():
    """NRZ와 RZ의 성능 비교 분석"""

    print("\n" + "="*80)
    print("NRZ vs RZ Performance Comparison")
    print("="*80)

    test_patterns = {
        "Alternating (1010...)": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        "All Ones (1111...)": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "All Zeros (0000...)": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Mixed Pattern": [1, 0, 1, 1, 0, 0, 1, 0, 1, 1],
        "Long Zero Run": [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    }

    rz_coder = RZCoder()

    print(f"\n{'Pattern':<25} | {'RZ Type':<12} | {'DC (V)':<8} | {'Trans/Bit':<10} | {'Sync Quality'}")
    print("-"*80)

    for pattern_name, bits in test_patterns.items():
        for rz_type in [RZType.UNIPOLAR_RZ, RZType.POLAR_RZ]:
            analysis = rz_coder.analyze_synchronization_quality(bits, rz_type)

            # 동기화 품질 평가
            if rz_type == RZType.POLAR_RZ:
                sync_quality = "EXCELLENT"  # 모든 비트에서 전이 보장
            else:
                if analysis["max_zero_run"] > 3:
                    sync_quality = "POOR"  # 0 연속 시 동기화 불가
                else:
                    sync_quality = "GOOD"

            print(f"{pattern_name:<25} | {rz_type.value:<12} | "
                  f"{analysis['dc_component']:>+.3f}   | "
                  f"{analysis['transitions_per_bit']:>+.2f}       | "
                  f"{sync_quality}")

    print("="*80)


def demonstrate_clock_recovery():
    """클럭 복구 능력 시연"""

    print("\n" + "="*70)
    print("Clock Recovery Capability Demonstration")
    print("="*70)

    rz_coder = RZCoder()

    # 문제 패턴: 긴 0 연속
    problem_pattern = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    print(f"\nInput Pattern: {problem_pattern}")
    print("\nUnipolar RZ Analysis:")

    unipolar_analysis = rz_coder.analyze_synchronization_quality(
        problem_pattern, RZType.UNIPOLAR_RZ
    )
    print(f"  Max Zero Run: {unipolar_analysis['max_zero_run']} bits")
    print(f"  Transitions/Bit: {unipolar_analysis['transitions_per_bit']:.2f}")
    print(f"  Problem: No transitions during zero run = Clock drift!")

    print("\nPolar RZ Analysis:")
    polar_analysis = rz_coder.analyze_synchronization_quality(
        problem_pattern, RZType.POLAR_RZ
    )
    print(f"  Max Zero Run: {polar_analysis['max_zero_run']} bits")
    print(f"  Transitions/Bit: {polar_analysis['transitions_per_bit']:.2f}")
    print(f"  Solution: Transitions for EVERY bit = Stable clock!")

    print("="*70)


def bandwidth_analysis():
    """대역폭 분석"""

    print("\n" + "="*70)
    print("Bandwidth Requirement Analysis")
    print("="*70)

    bit_rate = 1e9  # 1 Gbps

    print(f"\nAssumed Bit Rate: {bit_rate/1e9:.1f} Gbps")
    print(f"Bit Period (T): {1/bit_rate*1e9:.3f} ns")

    nrz_bandwidth = bit_rate  # 첫 번째 널 주파수
    rz_bandwidth = 2 * bit_rate  # RZ의 첫 번째 널 주파수

    print(f"\nNRZ Bandwidth Requirement:")
    print(f"  First Null Frequency: {nrz_bandwidth/1e9:.1f} GHz")
    print(f"  Minimum Sampling Rate: {2*nrz_bandwidth/1e9:.1f} GSa/s (Nyquist)")

    print(f"\nRZ Bandwidth Requirement:")
    print(f"  First Null Frequency: {rz_bandwidth/1e9:.1f} GHz")
    print(f"  Minimum Sampling Rate: {2*rz_bandwidth/1e9:.1f} GSa/s (Nyquist)")

    print(f"\nBandwidth Penalty: {rz_bandwidth/nrz_bandwidth:.1f}x")

    print("\nTrade-off:")
    print("  RZ provides better synchronization at the cost of 2x bandwidth")
    print("  Modern systems often use NRZ + scrambling or 8b/10b instead")

    print("="*70)


# ==================== 실행 ====================
if __name__ == "__main__":
    compare_nrz_vs_rz()
    demonstrate_clock_recovery()
    bandwidth_analysis()
