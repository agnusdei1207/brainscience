+++
title = "036. 선로 부호화 - 단극성/극성/양극성 (Unipolar/Polar/Bipolar Coding)"
description = "디지털 데이터를 물리적 신호로 변환하는 선로 부호화 기법의 핵심인 단극성, 극성, 양극성 부호화의 원리와 특성을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["LineCoding", "Unipolar", "Polar", "Bipolar", "NRZ", "Encoding", "Signal", "DCComponent"]
categories = ["studynotes-3_network"]
+++

# 036. 선로 부호화 - 단극성/극성/양극성 (Line Coding)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 선로 부호화(Line Coding)는 디지털 비트 스트림을 전송 매체에 적합한 디지털 신호 파형으로 변환하는 기술로, 단극성(Unipolar), 극성(Polar), 양극성(Bipolar)은 전압 레벨 할당 방식에 따른 세 가지 기본 분류입니다.
> 2. **가치**: 적절한 선로 부호화 선택은 DC 성분 제거, 동기화 능력, 대역폭 효율, 오류 검출 능력 등 통신 품질의 핵심 지표를 결정하며, 전송 거리와 매체 특성에 최적화된 통신을 가능하게 합니다.
> 3. **융합**: 현대 고속 통신에서 이 기술은 PAM4, Gray Coding, Scrambling 등과 결합하여 400GbE, 5G NR, PCIe 6.0 등의 차세대 인터페이스의 기반이 됩니다.

---

## I. 개요 (Context & Background)

선로 부호화(Line Coding) 또는 디지털-디지털 변조(Digital-to-Digital Encoding)는 이진 비트(0과 1)를 전송 매체(꼬임쌍선, 동축케이블, 광섬유 등)를 통해 전송 가능한 전기적 신호나 광 신호로 변환하는 기술입니다. 이때 **단극성(Unipolar)**, **극성(Polar)**, **양극성(Bipolar)**은 신호 레벨의 할당 방식에 따른 가장 기본적인 세 가지 분류입니다.

**💡 비유**: 선로 부호화는 **'모스 부호의 전송 방식'**과 같습니다.
- **단극성**: "짧은 신호(0V)와 긴 신호(+5V)만 사용"하는 방식입니다. 신호가 있거나 없거나 두 가지만 표현합니다. 마치 손전등을 켰다 껐다하는 것과 같습니다.
- **극성**: "짧은 신호(-5V)와 긴 신호(+5V)를 사용"하는 방식입니다. 양방향 전압을 사용하여 0과 1을 명확히 구분합니다. 마치 왼손과 오른손을 번갈아 드는 것과 같습니다.
- **양극성**: "세 가지 신호(0V, +V, -V)를 규칙적으로 사용"하는 방식입니다. 0은 0V, 1은 +V와 -V가 번갈아 나타납니다. 마치 왼발, 오른발을 교대로 내딛는 보행과 같습니다.

**등장 배경 및 발전 과정**:
1. **초기 전신 통신 (1840년대)**: 모스 부호는 사실상 최초의 디지털 부호화였습니다. 전류가 흐르거나(ON) 흐르지 않거나(OFF)하는 단극성 방식이었습니다.
2. **전화망 디지털화 (1960년대)**: PCM(Pulse Code Modulation) 도입과 함께 효율적인 선로 부호화가 필요해졌습니다. AMI(Alternate Mark Inversion)라는 양극성 부호화가 T1 회선에 채택되었습니다.
3. **고속 네트워크 시대 (1990년대~현재)**: 이더넷, USB, PCIe 등의 고속 인터페이스에서는 NRZ, MLT-3, PAM4 등 다양한 선로 부호화가 사용됩니다. 최근에는 400GbE에서 PAM4(4레벨 부호화)가 채택되어 대역폭 효율을 극대화하고 있습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 부호화 방식 | 신호 레벨 | 비트 표현 | DC 성분 | 동기화 능력 | 대역폭 | 오류 검출 | 적용 예시 |
|------------|----------|----------|---------|-----------|--------|----------|----------|
| **단극성 (Unipolar)** | 2개 (0, +V) | 0=0V, 1=+V | 존재 (높음) | 약함 | 넓음 | 없음 | 초기 전신, 로직 회로 |
| **극성 (Polar)** | 2개 (-V, +V) | 0=-V, 1=+V | 존재 (중간) | 중간 | 중간 | 없음 | NRZ-L, RS-232C |
| **양극성 (Bipolar/AMI)** | 3개 (-V, 0, +V) | 0=0V, 1=±V 교대 | 없음 (이상적) | 강함 | 좁음 | 있음 | T1/E1, 전화망 |

### 정교한 구조 다이어그램: 선로 부호화 파형 비교

```ascii
================================================================================
[ Line Coding Waveform Comparison: Unipolar vs Polar vs Bipolar ]
================================================================================

Input Bit Stream:   1    0    1    1    0    0    1    0    1    1
                   |    |    |    |    |    |    |    |    |    |
Bit Duration:      T_b  T_b  T_b  T_b  T_b  T_b  T_b  T_b  T_b  T_b

================================================================================
1. Unipolar NRZ (Non-Return to Zero) - 단극성
================================================================================

Voltage
   +V  |  +----+       +----+----+             +----+    +----+----+
       |  |    |       |    |    |             |    |    |    |    |
   0V  |--+    +-------+    |    +-------------+    +----+    |    +-->
       |                   |                                    |
       |
       +------------------------------------------------------------------> Time
            1    0    1    1    0    0    1    0    1    1

Characteristics:
  - Logic 1: +V (positive voltage)
  - Logic 0: 0V (no signal)
  - DC Component: HIGH (average > 0 when more 1s)
  - Synchronization: POOR (long runs of 0s = no transitions)

================================================================================
2. Polar NRZ-L (Non-Return to Zero Level) - 극성
================================================================================

Voltage
   +V  |  +----+       +----+----+             +----+    +----+----+
       |  |    |       |    |    |             |    |    |    |    |
   0V  |--+    |       |    |    |             |    |    |    |    |
       |       |       |    |    |             |    |    |    |    |
   -V  |       +-------+    |    +-------------+    +----+    |    +-->
       |                   |                                    |
       +------------------------------------------------------------------> Time
            1    0    1    1    0    0    1    0    1    1

Characteristics:
  - Logic 1: +V (positive voltage)
  - Logic 0: -V (negative voltage)
  - DC Component: MEDIUM (depends on 1s/0s ratio)
  - Synchronization: MEDIUM (transitions on every bit change)

================================================================================
3. Polar NRZ-I (Non-Return to Zero Inverted) - 극성 반전
================================================================================

Voltage
   +V  |  +----+----+             +----+             +----+----+----+
       |  |    |    |             |    |             |    |    |    |
   0V  |--+    |    |             |    |             |    |    |    |
       |       |    |             |    |             |    |    |    |
   -V  |       |    +-------------+    +-------------+    |    |    |
       |                   |                   |          |    |    |
       +------------------------------------------------------------------> Time
            1    1    0    1    0    0    1    0    1    1

Rule: Invert voltage level for each '1', maintain for '0'
Initial State: +V
  Bit 1: Invert -> -V
  Bit 1: Invert -> +V
  Bit 0: Maintain -> +V
  Bit 1: Invert -> -V
  ...and so on

================================================================================
4. Bipolar AMI (Alternate Mark Inversion) - 양극성
================================================================================

Voltage
   +V  |  +----+       +----+                   +----+         +----+
       |  |    |       |    |                   |    |         |    |
   0V  |--+    +-------+    +---------+---------+    +---------+    |
       |                            |                                |
   -V  |                            |                   +----+       |
       |                            +-------------------+    |       |
       +------------------------------------------------------------------> Time
            1    0    1    1    0    0    1    0    1    1

Mark (1) Alternation: +V, then -V, then +V, then -V, ...
  Bit 1: +V
  Bit 0: 0V
  Bit 1: -V (alternates!)
  Bit 1: +V (alternates!)
  Bit 0: 0V
  Bit 0: 0V
  Bit 1: -V (alternates!)
  ...

Characteristics:
  - Logic 1: Alternates between +V and -V
  - Logic 0: 0V
  - DC Component: ZERO (ideal)
  - Synchronization: GOOD (transitions for every 1)
  - Error Detection: YES (violation of alternation rule)

================================================================================
[ Power Spectral Density Comparison ]
================================================================================

Power
Density
   |
   |    Unipolar NRZ
   |    /\
   |   /  \
   |  /    \___________
   | /                   \
   |/_____________________\___________________ Frequency
   0
   |
   |    Polar NRZ
   |      /\
   |     /  \
   |    /    \
   |   /      \___________
   |  /                    \
   | /                       \
   |/__________________________\____________ Frequency
   0
   |
   |    Bipolar AMI
   |        /\
   |       /  \
   |      /    \
   |     /      \
   |    /        \___
   |   /             \_______
   |  /                       \_______________ Frequency
   | /____________________________________________
   0

Note: Bipolar AMI has power concentrated at 1/2 bit rate (better bandwidth)

================================================================================
```

### 심층 동작 원리: 5가지 핵심 메커니즘

1. **신호 레벨 할당 (Signal Level Assignment)**:
   - **단극성**: 0과 1을 0V와 +V로만 매핑합니다. 가장 단순하지만, 신호가 없을 때(0)와 전송 중단을 구분하기 어렵습니다.
   - **극성**: 0과 1을 각각 -V와 +V로 매핑합니다. 두 상태 모두 에너지를 가지므로 전송 중단과 구분이 가능합니다.
   - **양극성**: 0은 0V, 1은 직전 1의 극성과 반대로 매핑합니다. 이 규칙을 **AMI(Alternate Mark Inversion) 규칙**이라 합니다.

2. **DC 성분 관리 (DC Component Management)**:
   - **DC 성분 문제**: 신호의 평균 전압이 0V가 아니면, AC 결합(커패시터, 변압기)된 회로에서 신호 왜곡이 발생합니다. 또한 광섬유에서는 DC 성분을 전송할 수 없습니다.
   - **단극성**: 1이 많으면 평균이 +V 쪽으로 치우쳐 DC 성분이 큽니다.
   - **극성**: 1과 0의 비율이 같으면 DC 성분이 0이지만, 데이터 패턴에 따라 변동합니다.
   - **양극성**: 이상적으로 DC 성분이 0입니다. +V와 -V가 교대로 나타나 평균이 상쇄되기 때문입니다.

3. **동기화 능력 (Synchronization Capability)**:
   - **비트 동기화**: 수신측은 송신측의 클럭과 동기화되어야 비트 경계를 식별할 수 있습니다. 신호 전이(Transition)가 이 동기화의 기준이 됩니다.
   - **단극성**: 0이 연속되면 전이가 없어 동기화가 깨집니다.
   - **극성 NRZ-L**: 0이나 1이 연속되면 전이가 없습니다.
   - **양극성**: 1이 나타날 때마다 전이가 발생하지만, 0이 연속되면 여전히 문제입니다.

4. **대역폭 효율 (Bandwidth Efficiency)**:
   - **주파수 스펙트럼**: 신호의 주파수 성분 분포입니다. 스펙트럼이 좁을수록 대역폭 효율이 높습니다.
   - **단극성/극성**: 저주파 성분(DC 근처)에 에너지가 집중되어 있어 AC 결합 회로에서 문제가 됩니다.
   - **양극성**: DC 성분이 0이고, 에너지가 비트 레이트의 절반 주파수에 집중되어 있습니다.

5. **오류 검출 능력 (Error Detection)**:
   - **양극성 위반(Bipolar Violation)**: AMI에서 두 개의 연속된 1이 같은 극성을 가지면 전송 오류입니다. 이를 탐지하여 상위 계층에 보고할 수 있습니다.

### 핵심 코드: 선로 부호화 시뮬레이터 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from typing import List, Tuple
from dataclasses import dataclass

class LineCodingType(Enum):
    """선로 부호화 타입 정의"""
    UNIPOLAR_NRZ = "Unipolar NRZ"
    POLAR_NRZ_L = "Polar NRZ-L"
    POLAR_NRZ_I = "Polar NRZ-I"
    BIPOLAR_AMI = "Bipolar AMI"
    MANCHESTER = "Manchester"

@dataclass
class LineCodingResult:
    """선로 부호화 결과"""
    voltage_levels: np.ndarray
    time_points: np.ndarray
    dc_component: float
    transitions: int
    bandwidth_estimate: float

class LineCoder:
    """
    선로 부호화 시뮬레이터
    다양한 Line Coding 방식을 구현하고 분석
    """

    def __init__(self, voltage_level: float = 5.0, samples_per_bit: int = 100):
        """
        Args:
            voltage_level: 기준 전압 레벨 (V)
            samples_per_bit: 비트당 샘플 수 (파형 해상도)
        """
        self.V = voltage_level
        self.samples_per_bit = samples_per_bit

    def encode(self, bits: List[int], coding_type: LineCodingType) -> LineCodingResult:
        """
        비트 스트림을 선로 부호화하여 파형 생성

        Args:
            bits: 입력 비트 리스트 (0과 1)
            coding_type: 부호화 방식

        Returns:
            LineCodingResult: 부호화 결과
        """
        if coding_type == LineCodingType.UNIPOLAR_NRZ:
            voltage = self._encode_unipolar_nrz(bits)
        elif coding_type == LineCodingType.POLAR_NRZ_L:
            voltage = self._encode_polar_nrz_l(bits)
        elif coding_type == LineCodingType.POLAR_NRZ_I:
            voltage = self._encode_polar_nrz_i(bits)
        elif coding_type == LineCodingType.BIPOLAR_AMI:
            voltage = self._encode_bipolar_ami(bits)
        elif coding_type == LineCodingType.MANCHESTER:
            voltage = self._encode_manchester(bits)
        else:
            raise ValueError(f"Unknown coding type: {coding_type}")

        # 시간 축 생성
        n_samples = len(voltage)
        time = np.linspace(0, len(bits), n_samples)

        # DC 성분 계산
        dc_component = np.mean(voltage)

        # 전이(Transition) 횟수 계산
        transitions = np.sum(np.abs(np.diff(voltage)) > 0.1 * self.V)

        # 대역폭 추정 (전이 횟수 기반 근사)
        # 실제로는 FFT를 수행해야 정확하지만, 간단한 추정치 사용
        bandwidth_estimate = transitions / (2 * len(bits)) if len(bits) > 0 else 0

        return LineCodingResult(
            voltage_levels=voltage,
            time_points=time,
            dc_component=dc_component,
            transitions=transitions,
            bandwidth_estimate=bandwidth_estimate
        )

    def _encode_unipolar_nrz(self, bits: List[int]) -> np.ndarray:
        """단극성 NRZ 부호화"""
        voltage = np.array([])
        for bit in bits:
            level = self.V if bit == 1 else 0
            voltage = np.append(voltage, np.full(self.samples_per_bit, level))
        return voltage

    def _encode_polar_nrz_l(self, bits: List[int]) -> np.ndarray:
        """극성 NRZ-L (Level) 부호화"""
        voltage = np.array([])
        for bit in bits:
            level = self.V if bit == 1 else -self.V
            voltage = np.append(voltage, np.full(self.samples_per_bit, level))
        return voltage

    def _encode_polar_nrz_i(self, bits: List[int]) -> np.ndarray:
        """극성 NRZ-I (Inverted) 부호화"""
        voltage = np.array([])
        current_level = self.V  # 초기 상태

        for bit in bits:
            if bit == 1:
                current_level = -current_level  # 1이면 반전
            voltage = np.append(voltage, np.full(self.samples_per_bit, current_level))

        return voltage

    def _encode_bipolar_ami(self, bits: List[int]) -> np.ndarray:
        """양극성 AMI 부호화"""
        voltage = np.array([])
        last_mark_level = -self.V  # 직전 1의 극성 (다음은 +V부터 시작)

        for bit in bits:
            if bit == 1:
                last_mark_level = -last_mark_level  # 극성 교대
                level = last_mark_level
            else:
                level = 0

            voltage = np.append(voltage, np.full(self.samples_per_bit, level))

        return voltage

    def _encode_manchester(self, bits: List[int]) -> np.ndarray:
        """맨체스터 부호화 (IEEE 802.3 표준)"""
        voltage = np.array([])
        half_samples = self.samples_per_bit // 2

        for bit in bits:
            if bit == 1:
                # 1: -V → +V (low-to-high transition at mid-bit)
                voltage = np.append(voltage, np.full(half_samples, -self.V))
                voltage = np.append(voltage, np.full(half_samples, self.V))
            else:
                # 0: +V → -V (high-to-low transition at mid-bit)
                voltage = np.append(voltage, np.full(half_samples, self.V))
                voltage = np.append(voltage, np.full(half_samples, -self.V))

        return voltage

    def detect_bipolar_violation(self, bits: List[int]) -> List[Tuple[int, str]]:
        """
        양극성 AMI 위반 탐지

        Returns:
            위반이 발생한 비트 위치와 설명 리스트
        """
        violations = []
        last_mark_level = -self.V

        for i, bit in enumerate(bits):
            if bit == 1:
                expected_level = -last_mark_level
                # 실제 부호화에서 위반 발생 시 탐지 로직
                # (실제 수신 신호와 비교 필요하지만, 여기서는 시뮬레이션 생략)
                last_mark_level = -last_mark_level

        return violations

    def calculate_power_spectrum(self, voltage: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        전력 스펙트럼 밀도(PSD) 계산

        Returns:
            주파수 축, 전력 스펙트럼
        """
        # FFT 수행
        n = len(voltage)
        fft_result = np.fft.fft(voltage)
        power_spectrum = np.abs(fft_result) ** 2 / n

        # 주파수 축 (정규화된 주파수)
        freq = np.fft.fftfreq(n, d=1/self.samples_per_bit)

        # 양의 주파수만 선택
        positive_freq_idx = freq >= 0
        return freq[positive_freq_idx], power_spectrum[positive_freq_idx]


# ==================== 시각화 함수 ====================
def plot_line_coding_comparison(bits: List[int], voltage_level: float = 5.0):
    """모든 부호화 방식 비교 시각화"""

    coder = LineCoder(voltage_level=voltage_level)
    coding_types = [
        LineCodingType.UNIPOLAR_NRZ,
        LineCodingType.POLAR_NRZ_L,
        LineCodingType.POLAR_NRZ_I,
        LineCodingType.BIPOLAR_AMI,
        LineCodingType.MANCHESTER
    ]

    fig, axes = plt.subplots(len(coding_types) + 1, 1, figsize=(14, 10))
    fig.suptitle(f'Line Coding Comparison\nInput Bits: {bits}', fontsize=14, fontweight='bold')

    # 비트 경계 표시용
    for ax in axes[:-1]:
        for i in range(len(bits) + 1):
            ax.axvline(x=i, color='gray', linestyle='--', alpha=0.3, linewidth=0.5)

    # 각 부호화 방식별 파형 그리기
    for i, coding_type in enumerate(coding_types):
        result = coder.encode(bits, coding_type)

        axes[i].plot(result.time_points, result.voltage_levels, 'b-', linewidth=1.5)
        axes[i].set_ylabel('Voltage (V)')
        axes[i].set_title(f'{coding_type.value}\n'
                         f'DC={result.dc_component:.2f}V, '
                         f'Transitions={result.transitions}')
        axes[i].set_ylim(-voltage_level * 1.3, voltage_level * 1.3)
        axes[i].grid(True, alpha=0.3)
        axes[i].axhline(y=0, color='black', linewidth=0.5)

    # 비트 값 표시 (최상단)
    axes[-1].set_xlim(0, len(bits))
    axes[-1].set_ylim(-0.5, 1.5)
    for i, bit in enumerate(bits):
        axes[-1].text(i + 0.5, 0.5, str(bit), ha='center', va='center',
                      fontsize=20, fontweight='bold')
    axes[-1].set_xlabel('Bit Period')
    axes[-1].set_ylabel('Bit Value')
    axes[-1].set_title('Input Bit Stream')
    axes[-1].set_yticks([])

    plt.tight_layout()
    plt.savefig('/tmp/line_coding_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Plot saved to /tmp/line_coding_comparison.png")


def analyze_dc_component():
    """DC 성분 분석: 다양한 비트 패턴에서의 DC 성분 비교"""

    coder = LineCoder()
    patterns = {
        "Alternating (101010...)": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        "All Ones (111111...)": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "All Zeros (000000...)": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Random Pattern": [1, 0, 1, 1, 0, 0, 1, 0, 1, 1],
        "Long Run of Zeros": [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    }

    coding_types = [
        LineCodingType.UNIPOLAR_NRZ,
        LineCodingType.POLAR_NRZ_L,
        LineCodingType.BIPOLAR_AMI
    ]

    print("\n" + "="*80)
    print("DC Component Analysis")
    print("="*80)
    print(f"{'Pattern':<25} | {'Unipolar':>10} | {'Polar':>10} | {'Bipolar':>10}")
    print("-"*80)

    for pattern_name, bits in patterns.items():
        results = {ct: coder.encode(bits, ct) for ct in coding_types}
        print(f"{pattern_name:<25} | "
              f"{results[LineCodingType.UNIPOLAR_NRZ].dc_component:>10.2f}V | "
              f"{results[LineCodingType.POLAR_NRZ_L].dc_component:>10.2f}V | "
              f"{results[LineCodingType.BIPOLAR_AMI].dc_component:>10.2f}V")

    print("="*80)


# ==================== 실행 예시 ====================
if __name__ == "__main__":
    # 테스트 비트 패턴
    test_bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]

    print("="*60)
    print("Line Coding Simulator")
    print("="*60)

    # 파형 비교 그래프 생성
    plot_line_coding_comparison(test_bits)

    # DC 성분 분석
    analyze_dc_component()

    # 각 방식별 상세 분석
    coder = LineCoder()
    print("\n" + "="*60)
    print("Detailed Analysis for Each Coding Type")
    print("="*60)

    for coding_type in LineCodingType:
        result = coder.encode(test_bits, coding_type)
        print(f"\n{coding_type.value}:")
        print(f"  DC Component: {result.dc_component:.3f} V")
        print(f"  Transitions: {result.transitions}")
        print(f"  Bandwidth Estimate: {result.bandwidth_estimate:.2f} x Bit Rate")
