+++
title = "020. 나이퀴스트 채널 용량 (Nyquist Capacity) - 무잡음 채널"
description = "나이퀴스트 채널 용량 공식, 무잡음 채널의 이론적 최대 전송 속도, 심볼 레이트와의 관계 및 실제 적용 사례를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["NyquistCapacity", "NoiselessChannel", "SymbolRate", "BaudRate", "M_aryModulation", "ISI"]
categories = ["studynotes-3_network"]
+++

# 020. 나이퀴스트 채널 용량 (Nyquist Capacity) - 무잡음 채널

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 나이퀴스트 채널 용량 공식 C = 2B log₂(M)은 무잡음 이상 채널에서 대역폭 B(Hz)와 신호 레벨 수 M을 사용하여 달성할 수 있는 최대 데이터 전송 속도를 정의합니다.
> 2. **가치**: 이 공식은 대역폭과 심볼 레이트의 관계(최대 2B baud)를 확립하고, 다진 변조(M-ary Modulation)를 통한 전송 속도 향상의 이론적 근거를 제공합니다.
> 3. **융합**: 나이퀴스트 공식은 샤논-하틀리 정리의 특수 케이스로, 실제 시스템에서는 잡음과 ISI(심볼 간 간섭)로 인해 이 이론적 한계에 근접하는 것이 도전 과제입니다.

---

## I. 개요 (Context & Background)

**나이퀴스트 채널 용량(Nyquist Capacity)**은 **무잡음(Noiseless)** 이상 채널에서 달성할 수 있는 **이론적 최대 데이터 전송 속도**를 나타냅니다. 이는 1928년 Harry Nyquist가 발표한 **샘플링 정리**와 **심볼 전송 이론**에 기반합니다.

### 나이퀴스트 공식

```
무잡음 채널 용량: C = 2B log₂(M)

C: 최대 데이터 전송 속도 (bps)
B: 채널 대역폭 (Hz)
M: 신호 레벨 수 (심볼 수)
```

### 핵심 개념

1. **대역폭(B)**: 채널이 전달할 수 있는 주파수 범위
2. **심볼 레이트(Symbol Rate)**: 초당 전송되는 심볼 수 (Baud)
3. **다진 변조(M-ary)**: M개의 서로 다른 신호 레벨 사용

### 나이퀴스트 샘플링 정리

```
최대 심볼 레이트 = 2B (baud)
```

대역폭 B의 채널에서 초당 최대 2B 개의 심볼을 전송할 수 있습니다.

**💡 비유**: 나이퀴스트 용량을 **'도로 교통량'**에 비유할 수 있습니다.

- **대역폭(B)**: 도로의 차선 수와 같습니다. 더 넓은 도로는 더 많은 차량이 동시에 통과할 수 있습니다.
- **심볼 레이트(2B)**: 도로의 신호등이 초당 깜빡일 수 있는 최대 횟수입니다.
- **신호 레벨 수(M)**: 각 신호등이 표현할 수 있는 색상 수입니다. 빨/노/초 3색이면 M=3, 더 많은 색상을 구분할 수 있으면 더 많은 정보를 전달합니다.

**2차선 도로(B=2)에서 신호등이 3색(M=3)이라면:**
```
C = 2 × 2 × log₂(3) = 4 × 1.585 ≈ 6.34 "정보 단위/초"
```

**등장 배경 및 발전 과정**:

1. **Harry Nyquist의 연구 (1924-1928)**: Western Electric(현 Bell Labs)에서 전신 신호 전송 문제를 연구하며 "특정 대역폭에서 전송할 수 있는 최대 펄스 수"를 규명했습니다.

2. **다진 변조의 발전**: 1960~70년대 QPSK, 8-PSK, 16-QAM 등의 다진 변조 기술이 개발되면서 나이퀴스트 공식의 log₂(M) 항이 실제로 활용되기 시작했습니다.

3. **現代 통신 시스템**: 5G NR은 1024-QAM(M=1024)까지 사용하여 대역폭 효율을 극대화합니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 상세 역할 | 단위 | 예시 | 비고 |
|---------|------|----------|------|------|------|
| **C** | 채널 용량 | 최대 데이터 속도 | bps | 1 Mbps | 결과값 |
| **B** | 대역폭 | 주파수 범위 | Hz | 100 kHz | 입력값 |
| **M** | 레벨 수 | 신호 상태 수 | 개 | 4 (QPSK) | 입력값 |
| **2B** | 최대 심볼 레이트 | 초당 심볼 | baud | 200 kbaud | 나이퀴스트 한계 |
| **log₂(M)** | 비트/심볼 | 심볼당 비트 | bits | 2 bits | 변조 효율 |

### 정교한 구조 다이어그램: 심볼 전송과 대역폭

```ascii
================================================================================
[ 나이퀴스트 심볼 전송 원리 ]
================================================================================

대역폭 B의 이상 채널 (주파수 응답: 직사각형)

     ┌────────────────────────────────────┐
     │                                    │
  1  │            통과 대역               │
     │                                    │
     │        (대역폭 B)                  │
  0  │                                    │
     └────────────────────────────────────┘
          -B/2       0        +B/2     주파수 (Hz)

최대 심볼 레이트 = 2B (baud)

예: B = 1 MHz → 최대 2M 심볼/초


================================================================================
[ 심볼 레이트와 데이터 레이트의 관계 ]
================================================================================

데이터 레이트 = 심볼 레이트 × 비트/심볼

              C = (2B) × log₂(M)

비트/심볼이 클수록 (M이 클수록) 동일 대역폭에서 더 빠른 전송 가능

┌─────────────────────────────────────────────────────────────────────────────┐
│            M값에 따른 비트/심볼 비교                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  M = 2 (Binary)                                                             │
│  ┌───┐                                                                       │
│  │ 0 │  → 1 bit/symbol                                                       │
│  └───┘                                                                       │
│  │ 1 │                                                                       │
│  └───┘                                                                       │
│                                                                             │
│  M = 4 (QPSK)                                                                │
│  ┌───┬───┐                                                                   │
│  │00 │01 │  → 2 bits/symbol                                                  │
│  └───┴───┘                                                                   │
│  ┌───┬───┐                                                                   │
│  │10 │11 │                                                                   │
│  └───┴───┘                                                                   │
│                                                                             │
│  M = 16 (16-QAM)                                                             │
│  ┌───┬───┬───┬───┐                                                           │
│  │0000│0001│0010│0011│  → 4 bits/symbol                                      │
│  └───┴───┴───┴───┘                                                           │
│  ┌───┬───┬───┬───┐                                                           │
│  │0100│0101│0110│0111│                                                       │
│  └───┴───┴───┴───┘                                                           │
│  ┌───┬───┬───┬───┐                                                           │
│  │1000│1001│1010│1011│                                                       │
│  └───┴───┴───┴───┘                                                           │
│  ┌───┬───┬───┬───┐                                                           │
│  │1100│1101│1110│1111│                                                       │
│  └───┴───┴───┴───┘                                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


================================================================================
[ 다양한 대역폭과 M값에 따른 채널 용량 ]
================================================================================

대역폭(B)  │  M=2   │  M=4   │  M=16  │  M=64  │  M=256 │ M=1024
          │ 1b/sym │ 2b/sym │ 4b/sym │ 6b/sym │ 8b/sym │10b/sym
──────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────
  1 kHz   │   2 Kbps│   4 Kbps│   8 Kbps│  12 Kbps│  16 Kbps│  20 Kbps
 10 kHz   │  20 Kbps│  40 Kbps│  80 Kbps│ 120 Kbps│ 160 Kbps│ 200 Kbps
100 kHz   │ 200 Kbps│ 400 Kbps│ 800 Kbps│1.2 Mbps │1.6 Mbps │2.0 Mbps
  1 MHz   │   2 Mbps│   4 Mbps│   8 Mbps│  12 Mbps│  16 Mbps│  20 Mbps
 10 MHz   │  20 Mbps│  40 Mbps│  80 Mbps│ 120 Mbps│ 160 Mbps│ 200 Mbps
100 MHz   │ 200 Mbps│ 400 Mbps│ 800 Mbps│1.2 Gbps │1.6 Gbps │2.0 Gbps

공식: C = 2B × log₂(M)


================================================================================
[ ISI (Inter-Symbol Interference)와 나이퀴스트 필터 ]
================================================================================

문제: 실제 채널에서는 펄스가 확산되어 다음 심볼에 간섭

    심볼 1        심볼 2        심볼 3
      │             │             │
  ────┼─────────────┼─────────────┼────> 시간
      │             │             │
      ▼             ▼             ▼
    ┌───┐         ┌───┐         ┌───┐
    │   │         │   │         │   │  이상적 펄스
    │   │         │   │         │   │
    └───┘         └───┘         └───┘

실제 채널 통과 후 (확산):
    ┌─┐┌─┐       ┌─┐┌─┐       ┌─┐
    │ └┘ │       │ └┘ │       │ └┘ │  ISI 발생!
    └────┘       └────┘       └────┘
          ↑             ↑
          └─ 간섭 ──────┘

해결: 나이퀴스트 필터 (Raised Cosine)

    이상적: 사각형 펄스
    실제: sinc 파형 (영점에서 샘플링 → ISI 없음)

    h(t) = sin(πt/T) / (πt/T)  (이상적 sinc)

    Raised Cosine (실용적):
    - 롤오프 팩터 α (0~1)
    - 대역폭 = (1+α)/(2T) = (1+α) × (심볼 레이트)/2


================================================================================
[ 나이퀴스트 vs 샤논: 이론적 한계 비교 ]
================================================================================

나이퀴스트 (무잡음):
┌─────────────────────────────────────────────────────────────────┐
│  C = 2B × log₂(M)                                               │
│                                                                 │
│  특징:                                                          │
│  • 잡음 없는 이상적 채널                                         │
│  • M(레벨 수)을 무한히 늘리면 용량도 무한대                      │
│  • 현실적 한계: 레벨 구분이 어려워짐                             │
│                                                                 │
│  적용: 이론적 상한, 설계 가이드                                  │
└─────────────────────────────────────────────────────────────────┘

샤논-하틀리 (잡음 채널):
┌─────────────────────────────────────────────────────────────────┐
│  C = B × log₂(1 + S/N)                                          │
│                                                                 │
│  특징:                                                          │
│  • AWGN(백색 가우스 잡음) 채널                                   │
│  • S/N(신호 대 잡음비)이 용량 제한                               │
│  • 이론적 최대: 달성 불가능하지만 근접 가능                      │
│                                                                 │
│  적용: 실제 시스템의 절대적 상한                                 │
└─────────────────────────────────────────────────────────────────┘

관계:
• 나이퀴스트는 "M을 얼마나 크게 만들 수 있는가?" → 실제로는 잡음이 제한
• 샤논은 "S/N이 주어졌을 때 최대 용량" → 현실적 한계
• M → ∞ 이면 심볼 간 구분 불가 → 샤논 한계로 수렴
```

### 심층 동작 원리

1. **대역폭 제한**:
   - 이상적 저역 통과 필터: 대역폭 B 내의 주파수만 통과
   - 임펄스 응답: sinc 함수, 주기 T = 1/(2B)에서 영점

2. **심볼 레이트 제한**:
   - 나이퀴스트 속도: 2B 심볼/초
   - 이 속도로 전송 시 ISI 없이 심볼 복원 가능

3. **다진 변조의 효과**:
   - M개의 레벨 → log₂(M) 비트를 하나의 심볼로 전송
   - 레벨 수 증가 → 비트 레이트 증가

4. **현실적 제약**:
   - 레벨 구분을 위해서는 높은 S/N 필요
   - 클럭 지터, 위상 잡음 등 추가 오차원

### 핵심 수식 유도

```
나이퀴스트 심볼 레이트:
R_s ≤ 2B (baud)

비트 레이트:
R_b = R_s × log₂(M)

조합:
C = R_b = 2B × log₂(M)

예제:
B = 1 MHz, M = 64 (64-QAM)
C = 2 × 10⁶ × log₂(64) = 2 × 10⁶ × 6 = 12 Mbps
```

### 핵심 코드: 나이퀴스트 용량 계산기

```python
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ModulationScheme:
    """변조 방식 정의"""
    name: str
    m: int  # 신호 레벨 수

    @property
    def bits_per_symbol(self) -> int:
        return int(np.log2(self.m))

# 표준 변조 방식
MODULATION_SCHEMES = [
    ModulationScheme("BPSK", 2),
    ModulationScheme("QPSK", 4),
    ModulationScheme("8-PSK", 8),
    ModulationScheme("16-QAM", 16),
    ModulationScheme("32-QAM", 32),
    ModulationScheme("64-QAM", 64),
    ModulationScheme("256-QAM", 256),
    ModulationScheme("1024-QAM", 1024),
]

class NyquistCapacityCalculator:
    """
    나이퀴스트 채널 용량 계산기
    """

    @staticmethod
    def calculate_capacity(bandwidth_hz: float, m: int) -> float:
        """
        나이퀴스트 용량 계산

        Args:
            bandwidth_hz: 대역폭 (Hz)
            m: 신호 레벨 수

        Returns:
            채널 용량 (bps)
        """
        return 2 * bandwidth_hz * np.log2(m)

    @staticmethod
    def calculate_max_symbol_rate(bandwidth_hz: float) -> float:
        """
        최대 심볼 레이트 계산 (이상적)
        """
        return 2 * bandwidth_hz

    @staticmethod
    def calculate_required_bandwidth(data_rate_bps: float, m: int) -> float:
        """
        목표 데이터 레이트에 필요한 대역폭 계산
        """
        return data_rate_bps / (2 * np.log2(m))

    @staticmethod
    def calculate_required_m(bandwidth_hz: float, target_rate_bps: float) -> int:
        """
        목표 레이트를 달성하기 위한 최소 M 계산
        """
        bits_per_symbol = target_rate_bps / (2 * bandwidth_hz)
        return int(2 ** np.ceil(bits_per_symbol))

    @staticmethod
    def compare_modulations(bandwidth_hz: float) -> List[dict]:
        """
        다양한 변조 방식의 용량 비교
        """
        results = []
        for scheme in MODULATION_SCHEMES:
            capacity = NyquistCapacityCalculator.calculate_capacity(
                bandwidth_hz, scheme.m)
            results.append({
                'modulation': scheme.name,
                'm': scheme.m,
                'bits_per_symbol': scheme.bits_per_symbol,
                'capacity_bps': capacity,
                'capacity_mbps': capacity / 1e6
            })
        return results

class RaisedCosineFilter:
    """
    Raised Cosine 필터 (나이퀴스트 필터) 분석
    """

    def __init__(self, roll_off: float, symbol_period: float):
        """
        Args:
            roll_off: 롤오프 팩터 (0~1)
            symbol_period: 심볼 주기 (초)
        """
        self.alpha = roll_off
        self.T = symbol_period

    @property
    def bandwidth(self) -> float:
        """
        필터 대역폭 (Hz)
        """
        return (1 + self.alpha) / (2 * self.T)

    @property
    def nyquist_bandwidth(self) -> float:
        """
        나이퀴스트 최소 대역폭
        """
        return 1 / (2 * self.T)

    def frequency_response(self, f: np.ndarray) -> np.ndarray:
        """
        주파수 응답
        """
        H = np.ones_like(f, dtype=complex)

        f_nyq = self.nyquist_bandwidth
        f_rolloff_start = f_nyq * (1 - self.alpha)
        f_rolloff_end = f_nyq * (1 + self.alpha)

        # 롤오프 구간
        rolloff_mask = (np.abs(f) >= f_rolloff_start) & (np.abs(f) <= f_rolloff_end)
        f_rolloff = np.abs(f[rolloff_mask])

        H[rolloff_mask] = 0.5 * (1 + np.cos(
            (np.pi * self.T / self.alpha) * (f_rolloff - f_rolloff_start)
        ))

        # 차단 구간
        H[np.abs(f) > f_rolloff_end] = 0

        return H

    def excess_bandwidth_percent(self) -> float:
        """
        초과 대역폭 (%)
        """
        return self.alpha * 100

class NyquistISIAnalyzer:
    """
    ISI 분석기
    """

    @staticmethod
    def sinc_pulse(t: np.ndarray, T: float) -> np.ndarray:
        """
        이상적 sinc 펄스 (나이퀴스트 펄스)
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            pulse = np.sin(np.pi * t / T) / (np.pi * t / T)
            pulse[t == 0] = 1.0  # 0/0 = 1
        return pulse

    @staticmethod
    def raised_cosine_pulse(t: np.ndarray, T: float, alpha: float) -> np.ndarray:
        """
        Raised Cosine 펄스
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            numerator = np.sin(np.pi * t / T) * np.cos(np.pi * alpha * t / T)
            denominator = (np.pi * t / T) * (1 - (2 * alpha * t / T) ** 2)

            pulse = numerator / denominator

            # 특수점 처리
            pulse[np.abs(t) < 1e-10] = 1.0
            pulse[np.abs(np.abs(2 * alpha * t / T) - 1) < 1e-10] = (
                np.sin(np.pi / (2 * alpha)) * np.pi / 4
            )

        return pulse

# 실무 사용 예시
if __name__ == "__main__":
    calculator = NyquistCapacityCalculator()

    # 1. 다양한 변조 방식의 용량 비교 (10 MHz 대역폭)
    print("=" * 60)
    print("나이퀴스트 용량 비교 (대역폭: 10 MHz)")
    print("=" * 60)

    results = calculator.compare_modulations(10e6)
    for r in results:
        print(f"{r['modulation']:10s} (M={r['m']:4d}): "
              f"{r['capacity_mbps']:8.1f} Mbps ({r['bits_per_symbol']} b/sym)")

    # 2. 목표 레이트에 필요한 M 계산
    print("\n" + "=" * 60)
    print("100 Mbps 달성에 필요한 M (대역폭별)")
    print("=" * 60)

    for bw_mhz in [5, 10, 20, 50]:
        bw_hz = bw_mhz * 1e6
        m_req = calculator.calculate_required_m(bw_hz, 100e6)
        bps = np.log2(m_req)
        print(f"대역폭 {bw_mhz:3d} MHz: M ≥ {m_req:5d} "
              f"({bps:.1f} bits/symbol)")

    # 3. Raised Cosine 필터 분석
    print("\n" + "=" * 60)
    print("Raised Cosine 필터 분석")
    print("=" * 60)

    for alpha in [0.0, 0.25, 0.5, 1.0]:
        rc = RaisedCosineFilter(roll_off=alpha, symbol_period=1e-6)
        print(f"α = {alpha:.2f}: 대역폭 = {rc.bandwidth/1e6:.3f} MHz, "
              f"초과 = {rc.excess_bandwidth_percent():.0f}%")
