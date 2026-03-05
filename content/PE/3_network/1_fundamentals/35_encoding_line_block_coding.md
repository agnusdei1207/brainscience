+++
title = "035. 부호화 (Encoding) - Line Coding & Block Coding"
description = "디지털 통신에서 비트를 전송 매체에 적합한 신호로 변환하는 선로 부호화(Line Coding)와 블록 부호화(Block Coding)의 원리, 종류, 특성을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["Encoding", "LineCoding", "BlockCoding", "NRZ", "Manchester", "4B5B", "8B10B"]
categories = ["studynotes-3_network"]
+++

# 035. 부호화 (Encoding) - Line Coding & Block Coding

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 부호화는 디지털 비트 스트림을 전송 매체의 물리적 특성에 맞는 전기적/광학적 신호로 변환하는 기술로, 선로 부호화(L1 계층)는 비트-신호 매핑을, 블록 부호화(L2 계층)는 비트 패턴 변환을 수행합니다.
> 2. **가치**: 선로 부호화는 DC 성분 제거, 동기화 능력, 대역폭 효율, 오류 검출 능력을 결정하며, 블록 부호화(4B/5B, 8B/10B)는 동기화 향상과 DC 밸런싱을 통해 고속 통신을 가능하게 합니다.
> 3. **융합**: 이더넷 100BASE-TX(4B/5B+MLT-3), 기가비트 이더넷(8B/10B), PCIe(8B/10B), USB 3.0(8B/10B), HDMI(8B/10B) 등 모든 고속 직렬 인터페이스의 핵심 기술입니다.

---

## Ⅰ. 개요 (Context & Background)

**부호화(Encoding)**는 디지털 통신 시스템에서 이진 비트(0, 1)를 전송 매체를 통해 전송할 수 있는 물리적 신호로 변환하는 과정입니다. 크게 두 가지로 분류됩니다:

1. **선로 부호화(Line Coding)**: 비트를 전압/전류/광 레벨로 직접 매핑
2. **블록 부호화(Block Coding)**: 비트 그룹을 다른 비트 그룹으로 매핑 (mB/nB)

선로 부호화의 주요 목표:
- **DC 성분 제거**: 변압기 결합 회로에서 신호 왜곡 방지
- **동기화**: 클럭 복원을 위한 충분한 전이 제공
- **대역폭 효율**: 최소 대역폭으로 최대 데이터 전송
- **오류 검출**: 부호 위반으로 에러 감지

**💡 비유**: 부호화는 **'모스 부호'**와 같습니다.
- 선로 부호화: 점(.)과 선(-)을 짧은/긴 신호로 매핑
- 블록 부호화: 자주 쓰는 글자를 짧은 부호로, 드문 글자를 긴 부호로 매핑
- 좋은 부호는 '듣기 좋고', '구분하기 쉽고', '빨리 전송'할 수 있어야 합니다!

**등장 배경 및 발전 과정**:
1. **전신타전기 시대 (1830년대)**: 모스 부호 - 최초의 부호화
2. **디지털 통신 초기 (1960년대)**: NRZ, Manchester - 단순 부호화
3. **고속 통신 (1990년대~)**: 4B/5B, 8B/10B, 64B/66B - 블록 부호화

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석: 선로 부호화 기법

| 기법 | 비트 '0' | 비트 '1' | DC 평균 | 동기화 | 대역폭 | 응용 |
|------|---------|---------|--------|--------|--------|------|
| **NRZ-L** | Low | High | 비0 가능 | 낮음 | B/2 | 느린 통신 |
| **NRZ-I** | 유지 | 반전 | 비0 가능 | 낮음 | B/2 | USB |
| **Manchester** | High→Low | Low→High | 0 | 높음 | B | 10BASE-T |
| **Diff Manchester** | 1:중간반전, 0:시작반전 | 0 | 높음 | B | 토큰링 |
| **AMI** | 0V | +V/-V 교대 | 0 | 중간 | B/2 | T1/E1 |
| **MLT-3** | 4레벨 순환 | 0 | 중간 | B/4 | 100BASE-TX |

### 정교한 구조 다이어그램: 선로 부호화 파형

```ascii
================================================================================
[ Line Coding Waveform Comparison ]
================================================================================

Data:        1  0  1  1  0  0  1  0  1  1  1  0

NRZ-L (Non-Return to Zero - Level):
    +V  ───────┐          ┌──────────┐      ┌──────────
               │          │          │      │
    0V         └──────────┘          └──────┘
               1  0  1  1  0  0  1  0  1  1  1  0

NRZ-I (Non-Return to Zero - Inverted):
    +V  ──────────────┐  ┌──────┐      ┌──────────────
                      │  │      │      │
    0V         ┌──────┘  └──────┘──────┘
               1  0  1  1  0  0  1  0  1  1  1  0
               ↑        ↑        ↑              ↑
             Invert   Invert   Invert         Invert

Manchester (IEEE 802.3):
    +V  ─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─
        │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
    0V  └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─
        1   0   1   1   0   0   1   0   1   1   1   0
        ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑
       H-L L-H H-L H-L L-H L-H H-L L-H H-L H-L H-L L-H

Differential Manchester:
    +V  ─┐ ┌─┐   ┌─┐ ┌─┐   ┌─┐   ┌─┐   ┌─┐ ┌─┐ ┌─┐
        │ │ │   │ │ │ │   │ │   │ │   │ │ │ │ │ │
    0V  └─┘ └───┘ └─┘ └───┘ └───┘ └───┘ └─┘ └─┘ └─┘
        1   0   1   1   0   0   1   0   1   1   1   0
            ↑       ↑       ↑       ↑
          Trans  NoTrans Trans NoTrans

AMI (Alternate Mark Inversion):
    +V  ─────────┐          ┌──────────────────────
                │          │
    0V          └──────────┘──────────────────────
                │          │              │
    -V  ────────┘──────────┘──────────────┘──────
        1  0  1  1  0  0  1  0  1  1  1  0
        ↑        ↑        ↑        ↑  ↑
       +V       -V       +V       -V +V

================================================================================
[ Block Coding: 4B/5B Example ]
================================================================================

Input (4 bits):  0 0 0 0  0 0 0 1  0 0 1 0  1 1 1 1
                 (   0  )  (   1  )  (   2  )  (   F  )
                     │         │         │         │
                     v         v         v         v
Output (5 bits): 1 1 1 1 0  0 1 0 0 1  1 0 1 0 0  1 1 1 0 1
                 (  0x1E )  (  0x09 )  (  0x14 )  (  0x1D )

Purpose of 4B/5B:
    - Guarantee transitions for clock recovery
    - No more than 3 consecutive zeros
    - DC balance improvement
    - Control symbols (J, K, T, R, S, Q)

================================================================================
[ 8B/10B DC Balance Mechanism ]
================================================================================

Running Disparity (RD):
    RD+ : More 1s transmitted than 0s (expecting 0s)
    RD- : More 0s transmitted than 1s (expecting 1s)

Example: Encoding D0.0 (Data 0, abcdei = 000000, fgh = 000)

    For RD-: abcdei   fgh  → 100111 0100 (10 bits)
             5 bits   3 bits
    For RD+: abcdei   fgh  → 011000 1011 (inverse of certain bits)

    Each encoded symbol ensures:
    - Disparity is either 0, +2, or -2
    - Running disparity alternates to maintain DC balance

================================================================================
[ Protocol Stack with Encoding Layers ]
================================================================================

    +------------------+
    | Application      |
    +------------------+
    | Transport (TCP)  |
    +------------------+
    | Network (IP)     |
    +------------------+
    | Data Link (MAC)  |
    +------------------+
    | Block Coding     |  ← 8B/10B, 64B/66B (adds overhead)
    +------------------+
    | Line Coding      |  ← NRZ, Manchester, MLT-3
    +------------------+
    | Physical Medium  |  ← Copper, Fiber, Wireless
    +------------------+
```

### 심층 동작 원리

**1. NRZ (Non-Return to Zero) 상세**:
```
NRZ-L (Level):
        0 → -V (Low)
        1 → +V (High)

        장점: 단순, 대역폭 효율적 (B/2)
        단점: DC 성분, 연속 비트에서 동기화 상실

NRZ-I (Inverted on 1):
        0 → 레벨 유지
        1 → 레벨 반전

        장점: 차동 신호, 극성 무관
        단점: 연속 0에서 동기화 상실

대역폭 요구사항:
        NRZ의 최소 대역폭 = 비트율 / 2

        예: 1 Gbps → 최소 500 MHz
```

**2. Manchester 부호화 상세**:
```
Manchester (IEEE 802.3, G.E. Thomas):
        0 → Low→High (중간 상승 천이)
        1 → High→Low (중간 하강 천이)

        또는 (IEEE 표준 역):
        0 → High→Low
        1 → Low→High

특징:
        - 각 비트 중간에 항상 천이 발생 → 클럭 복원 용이
        - DC 성분 = 0 (항상 High/Low 시간 동일)
        - 대역폭 = 비트율 (NRZ의 2배)

예: 10 Mbps Ethernet → 10 MHz 대역폭 필요
```

**3. 블록 부호화 (4B/5B, 8B/10B)**:
```
4B/5B (100 Mbps Ethernet):
        4비트 입력 → 5비트 출력 (25% 오버헤드)

        주요 규칙:
        - 최대 3개 연속 0 허용
        - 최소 2개 1 보장
        - 제어 심볼: J(11000), K(10001), T(01101), R(00111)

        속도 계산:
        100 Mbps 데이터 → 125 Mbaud (5/4 × 100)

8B/10B (Gigabit Ethernet, PCIe):
        8비트 입력 → 10비트 출력 (25% 오버헤드)

        특징:
        - Running Disparity (RD)로 DC 밸런싱
        - 최대 5개 연속 동일 비트
        - 최소 3개 1, 3개 0 보장

        인코딩 구조:
        8비트 = 5비트(abcdei) + 3비트(fgh)
        → 10비트 = abcdei를 6비트로 + fgh를 4비트로

64B/66B (10G+ Ethernet):
        64비트 데이터 + 2비트 헤더 (3% 오버헤드)
        - 동기화를 위해 스크램블링 사용
```

### 핵심 코드: 부호화 시뮬레이션

```python
"""
선로 부호화 및 블록 부호화 시뮬레이션
NRZ, Manchester, 4B/5B, 8B/10B 구현
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from itertools import product


# ===============================
# Line Coding Implementation
# ===============================

def nrz_l_encode(bits: List[int]) -> List[int]:
    """NRZ-L 부호화: 0 → -1, 1 → +1"""
    return [1 if b else -1 for b in bits]


def nrz_i_encode(bits: List[int]) -> List[int]:
    """NRZ-I 부호화: 1에서 반전"""
    encoded = []
    level = -1
    for b in bits:
        if b:
            level = -level  # 1이면 반전
        encoded.append(level)
    return encoded


def manchester_encode(bits: List[int]) -> List[int]:
    """Manchester 부호화: 0 → Low-High, 1 → High-Low"""
    encoded = []
    for b in bits:
        if b:
            encoded.extend([1, -1])   # 1: High → Low
        else:
            encoded.extend([-1, 1])   # 0: Low → High
    return encoded


def ami_encode(bits: List[int]) -> List[int]:
    """AMI 부호화: 1은 +1/-1 교대"""
    encoded = []
    polarity = 1
    for b in bits:
        if b:
            encoded.append(polarity)
            polarity = -polarity
        else:
            encoded.append(0)
    return encoded


# ===============================
# Block Coding Implementation
# ===============================

# 4B/5B 코드 테이블
CODE_4B5B: Dict[int, int] = {
    0x0: 0b11110, 0x1: 0b01001, 0x2: 0b10100, 0x3: 0b10101,
    0x4: 0b01010, 0x5: 0b01011, 0x6: 0b01110, 0x7: 0b01111,
    0x8: 0b10010, 0x9: 0b10011, 0xA: 0b10110, 0xB: 0b10111,
    0xC: 0b11010, 0xD: 0b11011, 0xE: 0b11100, 0xF: 0b11101,
}

# 4B/5B 제어 심볼
CONTROL_4B5B = {
    'J': 0b11000,  # Start delimiter 1
    'K': 0b10001,  # Start delimiter 2
    'T': 0b01101,  # End delimiter 1
    'R': 0b00111,  # End delimiter 2
    'S': 0b11001,  # Set
    'Q': 0b00011,  # Reset
    'I': 0b11111,  # Idle
    'H': 0b00100,  # Halt (error)
}


def encode_4b5b(data_nibbles: List[int]) -> List[int]:
    """4B/5B 부호화"""
    encoded = []
    for nibble in data_nibbles:
        if nibble in CODE_4B5B:
            encoded.append(CODE_4B5B[nibble])
        else:
            raise ValueError(f"Invalid nibble: {nibble}")
    return encoded


def decode_5b4b(five_bit_symbols: List[int]) -> List[int]:
    """4B/5B 복호화"""
    decode_table = {v: k for k, v in CODE_4B5B.items()}
    decoded = []
    for symbol in five_bit_symbols:
        if symbol in decode_table:
            decoded.append(decode_table[symbol])
        else:
            decoded.append(None)  # Error
    return decoded


def analyze_4b5b_properties():
    """4B/5B 부호화 특성 분석"""
    print("\n4B/5B 부호화 분석:")
    print("=" * 50)

    max_zeros = 0
    min_ones = float('inf')

    for nibble, code in CODE_4B5B.items():
        binary = format(code, '05b')

        # 연속 0 계산
        zero_runs = [len(run) for run in binary.split('1') if run]
        max_zero_run = max(zero_runs) if zero_runs else 0
        max_zeros = max(max_zeros, max_zero_run)

        # 1의 개수
        ones_count = binary.count('1')
        min_ones = min(min_ones, ones_count)

        print(f"0x{nibble:X} → {binary} (1s: {ones_count}, max zeros: {max_zero_run})")

    print(f"\n최대 연속 0: {max_zeros}")
    print(f"최소 1의 개수: {min_ones}")


# 8B/10B 간소화 구현
class Encoder8B10B:
    """8B/10B 부호화 (간소화 버전)"""

    def __init__(self):
        self.running_disparity = -1  # RD-로 시작

    def encode_byte(self, byte: int) -> Tuple[int, int]:
        """
        8비트를 10비트로 부호화
        실제 구현은 복잡한 lookup table 필요
        """
        # 8비트를 5비트 + 3비트로 분리
        abcdei = byte & 0x1F          # 하위 5비트
        fgh = (byte >> 5) & 0x07      # 상위 3비트

        # 간소화: 실제는 lookup table 사용
        # 여기서는 교육적 목적으로 단순화

        # 5B/6B + 3B/4B 결합
        # 실제는 disparity 고려한 복잡한 매핑

        encoded_6 = self._encode_5b6b(abcdei)
        encoded_4 = self._encode_3b4b(fgh)

        # Running disparity 업데이트
        encoded_10 = (encoded_6 << 4) | encoded_4

        return encoded_10, self.running_disparity

    def _encode_5b6b(self, data: int) -> int:
        """5B/6B 부호화 (간소화)"""
        # 실제는 복잡한 lookup table
        # 교육적 목적으로 단순화
        return (data << 1) | ((data >> 4) & 1)  # 예시

    def _encode_3b4b(self, data: int) -> int:
        """3B/4B 부호화 (간소화)"""
        return (data << 1) | ((data >> 2) & 1)  # 예시


def plot_line_coding_comparison():
    """
    선로 부호화 파형 비교 시각화
    """
    # 테스트 데이터
    bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0]

    # 각 부호화 적용
    nrz_l = nrz_l_encode(bits)
    nrz_i = nrz_i_encode(bits)
    manchester = manchester_encode(bits)
    ami = ami_encode(bits)

    fig, axes = plt.subplots(5, 1, figsize=(14, 10), sharex=True)

    # 원본 비트
    ax = axes[0]
    ax.step(range(len(bits)), bits, where='mid', linewidth=2)
    ax.set_ylabel('Original Bits')
    ax.set_ylim([-0.5, 1.5])
    ax.set_yticks([0, 1])
    ax.grid(True, alpha=0.3)

    # NRZ-L
    ax = axes[1]
    ax.step(range(len(nrz_l)), nrz_l, where='mid', linewidth=2)
    ax.set_ylabel('NRZ-L')
    ax.set_ylim([-1.5, 1.5])
    ax.grid(True, alpha=0.3)

    # NRZ-I
    ax = axes[2]
    ax.step(range(len(nrz_i)), nrz_i, where='mid', linewidth=2)
    ax.set_ylabel('NRZ-I')
    ax.set_ylim([-1.5, 1.5])
    ax.grid(True, alpha=0.3)

    # Manchester
    ax = axes[3]
    ax.step(range(len(manchester)), manchester, where='mid', linewidth=2)
    ax.set_ylabel('Manchester')
    ax.set_ylim([-1.5, 1.5])
    ax.grid(True, alpha=0.3)

    # AMI
    ax = axes[4]
    ax.step(range(len(ami)), ami, where='mid', linewidth=2)
    ax.set_ylabel('AMI')
    ax.set_ylim([-1.5, 1.5])
    ax.set_xlabel('Bit Index')
    ax.grid(True, alpha=0.3)

    plt.suptitle('Line Coding Comparison', fontsize=14)
    plt.tight_layout()
    plt.savefig('line_coding_comparison.png', dpi=150)
    plt.show()


def analyze_bandwidth_requirements():
    """
    대역폭 요구사항 분석
    """
    print("\n" + "=" * 60)
    print("대역폭 요구사항 비교")
    print("=" * 60)

    data_rates = [10, 100, 1000, 10000]  # Mbps

    print(f"{'데이터율':<12} {'NRZ (B/2)':<15} {'Manchester (B)':<15} {'4B/5B':<15}")
    print("-" * 60)

    for rate in data_rates:
        nrz_bw = rate / 2
        manchester_bw = rate
        block_bw = rate * 1.25

        print(f"{rate} Mbps{'':<6} {nrz_bw:.1f} MHz{'':<8} {manchester_bw:.1f} MHz{'':<8} {block_bw:.1f} MHz")


if __name__ == "__main__":
    # 선로 부호화 파형 비교
    plot_line_coding_comparison()

    # 4B/5B 분석
    analyze_4b5b_properties()

    # 대역폭 요구사항
    analyze_bandwidth_requirements()

    # 부호화 예시
    print("\n" + "=" * 60)
    print("4B/5B 부호화 예시")
    print("=" * 60)

    test_data = [0x0, 0x1, 0x5, 0xF]
    encoded = encode_4b5b(test_data)

    for nibble, code in zip(test_data, encoded):
        print(f"0x{nibble:X} (0b{format(nibble, '04b')}) → 0b{format(code, '05b')} (0x{code:02X})")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 고속 인터페이스 부호화

| 인터페이스 | 속도 | 부호화 | 오버헤드 | DC 밸런스 | 특징 |
|----------|------|--------|---------|----------|------|
| **10BASE-T** | 10 Mbps | Manchester | 100% | 완벽 | 간단, 높은 대역폭 |
| **100BASE-TX** | 100 Mbps | 4B/5B + MLT-3 | 25% | 양호 | 3레벨 전송 |
| **1000BASE-T** | 1 Gbps | 8B/10B + PAM-5 | 25% | 완벽 | 4페어, 5레벨 |
| **10GBASE-R** | 10 Gbps | 64B/66B | 3% | 스크램블 | 낮은 오버헤드 |
| **PCIe Gen 1-2** | 2.5-5 GT/s | 8B/10B | 25% | 완벽 | RD 기반 |
| **PCIe Gen 3+** | 8+ GT/s | 128B/130B | 1.5% | 스크램블 | 매우 낮은 오버헤드 |
| **USB 3.0** | 5 Gbps | 8B/10B | 25% | 완벽 | RD 기반 |
| **USB 3.1+** | 10+ Gbps | 128B/132B | 3% | 스크램블 | 낮은 오버헤드 |

### 과목 융합 관점 분석

**1. 디지털 회로와의 융합**:
   - SERDES (Serializer/Deserializer)에서 부호화/복호화 수행
   - PLL (Phase-Locked Loop)로 클럭 복원
   - CDR (Clock and Data Recovery) 회로

**2. 신호 무결성(SI)과의 융합**:
   - DC 차단 변압기를 통과하려면 DC 성분 0 필수
   - ISI (Inter-Symbol Interference) 최소화를 위한 부호화
   - Jitter 누적 방지

**3. 광통신과의 융합**:
   - 광섬유는 DC 성분 전송 불가 → DC 밸런스 필수
   - 8B/10B, 64B/66B 광 트랜시버에 표준 사용
   - 전력 소모 최소화를 위한 효율적 부호화

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 커스텀 고속 직렬 링크 설계

**문제 상황**: FPGA 기반 커스텀 고속 직렬 링크를 설계해야 합니다. 1Gbps 데이터 전송이 필요합니다.

**기술사의 전략적 의사결정**:

1. **부호화 선택 기준**:
   - 대역폭: 1.25 GHz 이하 선호 (PCB 비용)
   - DC 밸런스: 광 커플러 사용으로 필수
   - 복잡도: FPGA 리소스 제약

2. **후보 기법 비교**:
   | 기법 | 유효 속도 | 라인 속도 | DC 밸런스 | FPGA 리소스 |
   |------|----------|----------|----------|------------|
   | 8B/10B | 1 Gbps | 1.25 Gbps | 완벽 | 낮음 |
   | 64B/66B | 1 Gbps | 1.03 Gbps | 스크램블 | 중간 |
   | 128B/130B | 1 Gbps | 1.016 Gbps | 스크램블 | 높음 |

3. **결정**: 8B/10B 채택
   - 이유: 검증된 기술, 낮은 복잡도, 완벽한 DC 밸런스, 풍부한 IP

### 도입 시 고려사항 체크리스트

| 항목 | 확인 내용 | 중요도 |
|------|----------|--------|
| **DC 밸런스** | AC 결합 회로 사용 여부 | 상 |
| **대역폭** | 매체/PCB 대역폭 제약 | 상 |
| **클럭 복원** | 천이 밀도 요구사항 | 상 |
| **오버헤드** | 유효 데이터율 vs 라인 속도 | 중 |
| **지연** | 인코딩/디코딩 레이턴시 | 중 |
| **에러 전파** | 부호화 오류의 영향 범위 | 중 |

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - DC 밸런스 무시**:
  AC 결합 회로에서 NRZ를 사용하면 연속 동일 비트에서 기준 레벨이 이동하여 비트 에러 발생.

- **안티패턴 2 - 과도한 오버헤드**:
  저속 링크에서 8B/10B를 사용하면 25% 대역폭 낭비. 상황에 맞는 부호화 선택 필요.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | 내용 | 정량적 지표 |
|----------|------|------------|
| **신뢰성** | 동기화 향상으로 비트 에러 감소 | BER 10⁻¹² 달성 |
| **호환성** | 표준 부호화로 장비 간 상호운용 | 표준 준수 100% |
| **효율성** | 적정 부호화로 대역폭 활용 | 유효 데이터율 97%+ |
| **단순성** | 검증된 기술로 개발 기간 단축 | 개발 시간 30% 단축 |

### 미래 전망 및 진화 방향

- **PAM-4/8**: 멀티레벨 부호화로 대역폭 효율 2~3배 향상
- **DFE/MLSE**: 채널 등화와 결합한 적응형 부호화
- **양자 통신**: 단일 광자 기반 부호화 기술

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **IEEE 802.3** | IEEE | 이더넷 PHY 부호화 |
| **PCI Express** | PCI-SIG | PCIe 부호화 스펙 |
| **USB 3.x** | USB-IF | USB 부호화 스펙 |
| **OIF-CEI** | OIF | 공통 전기 I/O |

---

## 관련 개념 맵 (Knowledge Graph)
- [NRZ/RZ/Manchester](./37_nrz_rz_manchester.md) - 선로 부호화 상세
- [4B/5B, 8B/10B](./42_4b5b_8b10b.md) - 블록 부호화 상세
- [대역폭](./13_bandwidth_efficiency.md) - 대역폭과 부호화
- [동기식 전송](./10_synchronous_asynchronous_transmission.md) - 클럭 동기화
- [AMI/B8ZS/HDB3](./43_b8zs_hdb3.md) - PCM 선로 부호화

---

## 어린이를 위한 3줄 비유 설명
1. **부호화**는 **'모스 부호'** 같아요. 글자를 점(.)과 선(-)의 신호로 바꾸는 거예요.
2. **선로 부호화**는 **'점은 짧게, 선은 길게'** 보내는 규칙이에요. 0과 1을 전기 신호로 바꾸는 방법이죠.
3. **블록 부호화**는 **'자주 쓰는 글자는 짧은 부호로'** 보내는 거예요. 효율적으로 전송하기 위해 4비트를 5비트로 늘려서, 신호가 섞이지 않게 해요!
