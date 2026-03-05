+++
title = "040. AMI 부호화 (Alternate Mark Inversion)"
description = "1 비트마다 극성을 교대로 변화시켜 DC 성분을 제거하는 AMI 부호화와 Pseudoternary 부호화의 원리를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["AMI", "AlternateMarkInversion", "Pseudoternary", "LineCoding", "T1", "E1", "B8ZS", "HDB3"]
categories = ["studynotes-3_network"]
+++

# 040. AMI 부호화 (Alternate Mark Inversion)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: AMI(Alternate Mark Inversion) 부호화는 0은 0V로, 1(Mark)은 +V와 -V를 교대로 표현하는 3-레벨 선로 부호화로, 연속된 1의 DC 성분을 상쇄하여 DC 밸런스 0을 달성합니다.
> 2. **가치**: AMI는 DC 성분이 0이고, AMI 위반(Bipolar Violation)을 통해 오류 검출이 가능하며, T1/E1 디지털 전화망의 표준 부호화로 수십 년간 통신망의 근간을 형성했습니다.
> 3. **융합**: AMI의 단점(연속 0 동기화 문제)을 해결하기 위해 B8ZS, HDB3 등의 Zero Suppression 기술이 개발되었으며, 이 개념은 현대 DSL, 광통신 시스템으로 진화했습니다.

---

## I. 개요 (Context & Background)

AMI(Alternate Mark Inversion, 교대 마크 반전) 부호화는 3개의 신호 레벨(+V, 0V, -V)을 사용하는 양극성(Bipolar) 선로 부호화 방식입니다. 이름에서 알 수 있듯이, 'Mark'(1 비트)의 극성이 교대로(Alternately) 반전(Inversion)됩니다. 0 비트는 0V(무신호)로 표현됩니다.

**💡 비유**: AMI 부호화는 **'양발 번갈아 딛기'**와 같습니다.
- 앞으로 나아갈 때(1을 전송할 때) 왼발과 오른발을 번갈아 딛습니다.
- 첫 번째 1은 왼발(+V), 두 번째 1은 오른발(-V), 세 번째 1은 다시 왼발(+V)...
- 제자리에 서 있을 때는(0을 전송할 때) 아무 발도 움직이지 않습니다(0V).
- 이렇게 하면 왼쪽으로나 오른쪽으로 치우치지 않고(DC 성분 0), 균형을 유지하며 나아갈 수 있습니다.

**등장 배경 및 발전 과정**:
1. **디지털 전화망의 탄생 (1962년)**: Bell Labs가 T1 디지털 전송 시스템을 개발하면서 AMI를 채택했습니다. 기존 아날로그 전화선으로 24개의 음성 채널을 디지털로 전송하기 위해서였습니다.
2. **국제 표준화**: 유럽은 E1(2.048 Mbps), 북미는 T1(1.544 Mbps)로 표준화되었으며, 둘 다 AMI를 기본 부호화로 사용했습니다.
3. **Zero Suppression 진화**: AMI의 단점(연속 0에서 동기화 불가)을 해결하기 위해 B8ZS(Bipolar with 8-Zero Substitution, 북미)와 HDB3(High-Density Bipolar 3, 유럽)가 개발되었습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 부호화 방식 | 0 표현 | 1 표현 | DC 성분 | 동기화 능력 | 오류 검출 | 적용 표준 |
|------------|-------|-------|---------|-----------|----------|----------|
| **AMI** | 0V | ±V 교대 | 0 (이상적) | 0 연속 시 불가 | AMI 위반 | T1, E1 |
| **Pseudoternary** | ±V 교대 | 0V | 0 (이상적) | 1 연속 시 불가 | 위반 | 특수 응용 |
| **B8ZS** | 0V (8개 0시 치환) | ±V 교대 | 0 | 우수 | 위반 패턴 | T1 (북미) |
| **HDB3** | 0V (4개 0시 치환) | ±V 교대 | 0 | 우수 | 위반 패턴 | E1 (유럽) |

### 정교한 구조 다이어그램: AMI 파형 및 위반 탐지

```ascii
================================================================================
[ AMI (Alternate Mark Inversion) Waveform ]
================================================================================

Input Bit Stream:   1    0    1    1    0    0    1    0    1    1
                   |    |    |    |    |    |    |    |    |    |

Voltage
   +V  |  +--+              +--+                   +--+         +--+
       |  |  |              |  |                   |  |         |  |
   0V  |--+  +-------+------+  +---------+---------+  +---------+  |
       |          |                |     |                |        |
   -V  |          |                |     +----------------+        |
       |          |                |                               |
       +------------------------------------------------------------------> Time
            b1   b2   b3   b4   b5   b6   b7   b8   b9  b10

Encoding Rule:
  - Logic 0: 0V (no pulse)
  - Logic 1 (Mark): Alternates between +V and -V

Bit-by-bit Encoding:
  b1 = 1: First mark → +V
  b2 = 0: Space → 0V
  b3 = 1: Second mark → -V (alternates!)
  b4 = 1: Third mark → +V (alternates!)
  b5 = 0: Space → 0V
  b6 = 0: Space → 0V
  b7 = 1: Fourth mark → -V (alternates!)
  b8 = 0: Space → 0V
  b9 = 1: Fifth mark → +V (alternates!)
  b10 = 1: Sixth mark → -V (alternates!)

DC Component Analysis:
  +V appears: 3 times (b1, b4, b9)
  -V appears: 3 times (b3, b7, b10)
  0V appears: 4 times (b2, b5, b6, b8)
  Average: (3×+V + 3×-V + 4×0) / 10 = 0 ✓

================================================================================
[ Bipolar Violation Detection ]
================================================================================

Normal AMI Pattern:      1    0    1    1    0    1
                         +V       -V   +V       -V
                         |        |    |        |
Voltage                  |        |    |        |
   +V  |  +--+           +--+             +--+
       |  |  |           |  |             |  |
   0V  |--+  +-----+-----+  +-----+-------+  |
       |        |                   |        |
   -V  |        |                   |        +-->
       |        |                   |
       +----------------------------------------------> Time
            b1   b2   b3   b4   b5   b6

  Pattern: +V, 0, -V, +V, 0, -V
  Rule Check: Alternating polarity maintained ✓
  Status: NO VIOLATION

Corrupted AMI Pattern:  1    0    1    1    0    1   [Error at b4]
                         +V       -V   -V!      +V
                         |        |    |        |
                         |        |    |        |
Voltage                         XXX  <-- VIOLATION!
   +V  |  +--+           +--+                   +--+
       |  |  |           |  |                   |  |
   0V  |--+  +-----+-----+  +-----+-------+-----+  |
       |        |                   |              |
   -V  |        |                   +-----------+ |
       |        |                                ||
       +---------------------------------------------> Time
            b1   b2   b3   b4   b5   b6

  Pattern: +V, 0, -V, -V(!), 0, +V
  Rule Check: b3=-V, b4=-V → SAME polarity!
  Status: BIPOLAR VIOLATION DETECTED!
  Action: Report error, may trigger recovery

================================================================================
[ Synchronization Problem: Long Zero Run ]
================================================================================

Input:  0    0    0    0    0    0    0    0    1

Voltage
   +V  |                                      +--+
       |                                      |  |
   0V  |--------------------------------------  +-->
       |
   -V  |
       +----------------------------------------------------------> Time
            0    0    0    0    0    0    0    0    1

  Problem: No transitions for 8 consecutive zeros!
  Result: Clock recovery circuit drifts
  Impact: Data loss, framing errors

================================================================================
[ B8ZS (Bipolar with 8-Zero Substitution) Solution ]
================================================================================

Input:  0    0    0    0    0    0    0    0    1

Normal AMI would be all zeros (no transitions)

B8ZS Substitution Rule:
  If 8 consecutive zeros detected, replace with:
  0  0  0  V  B  0  V  B
  where V = Bipolar Violation, B = Normal Bipolar

Actual Transmission:
  0    0    0    0V   1B   0    0V   1B   1
  (assuming last mark was +V)

Voltage
   +V  |                      +--+        +--+     +--+
       |                      |  |        |  |     |  |
   0V  |------------+---------+  +--------+  +-----+  |
       |            |                |              |
   -V  |            +----------------+              +-->
       |
       +----------------------------------------------------------> Time
            0    0    0    V    B    0    V    B    1

  Pattern sent: 0, 0, 0, -V(violation), +V, 0, -V(violation), +V, -V

Receiver:
  1. Detects two intentional bipolar violations
  2. Recognizes B8ZS pattern
  3. Replaces with 8 zeros
  4. Clock maintained through intentional violations!

================================================================================
[ HDB3 (High-Density Bipolar 3) Solution ]
================================================================================

Input:  0    0    0    0    1    0    0    0    0

HDB3 Substitution Rule:
  If 4 consecutive zeros detected, replace with:
  - If last mark was +V: 0 0 0 +V (violation)
  - If last mark was -V: 0 0 0 -V (violation)
  - Every 2nd substitution: B 0 0 V (substitute first 0 too)

Assuming: Previous mark was +V

Voltage
   +V  |                                +--+
       |                                |  |
   0V  |------------+-------------------+  +-------->
       |            |
   -V  |            +-----------------------------+
       |
       +----------------------------------------------------------> Time
            0    0    0    V    1    0    0    0    V

  First 4-zeros: Replaced with 000V (V = +V violation)
  Second 4-zeros: Replaced with 000V (V = -V violation)

Result: Maximum 3 consecutive zeros, clock always recoverable!

================================================================================
```

### 심층 동작 원리: 5가지 핵심 메커니즘

1. **교대 마크 반전 (Alternate Mark Inversion)**:
   - **핵심 규칙**: 0은 0V, 1은 직전 1과 반대 극성(+V 또는 -V)
   - **상태 추적**: 인코더와 디코더 모두 '마지막 1의 극성'을 기억해야 합니다.
   - **구현**: 1비트 상태 플립플롭 또는 카운터로 구현합니다.

2. **DC 밸런스 (Zero DC Component)**:
   - **이유**: +V 펄스와 -V 펄스의 개수가 항상 같거나 최대 1개 차이입니다.
   - **수학적 증명**: 연속된 1의 경우 +V, -V, +V, -V... 순서이므로 평균이 0입니다.
   - **이점**: AC 결합 회로(변압기, 커패시터)에서 신호 왜곡 없이 전송 가능합니다.

3. **AMI 위반 탐지 (Bipolar Violation Detection)**:
   - **위반 정의**: 연속된 두 개의 1이 같은 극성을 가질 때
   - **오류 검출**: 수신측은 AMI 규칙 위반을 감지하여 전송 오류를 탐지합니다.
   - **오류율 추정**: 위반 발생 빈도로 채널 오류율을 추정할 수 있습니다.

4. **Zero Suppression (B8ZS, HDB3)**:
   - **문제**: AMI에서 연속 0이 길면 동기화 불가
   - **B8ZS**: 8개 연속 0을 특정 위반 패턴으로 치환 (북미 T1)
   - **HDB3**: 4개 연속 0마다 위반 펄스 삽입 (유럽 E1)
   - **원리**: 의도적 위반 패턴으로 0 전송과 동시에 클럭 복구 가능

5. **Pseudoternary 부호화**:
   - **AMI의 역**: 0을 ±V 교대로, 1을 0V로 표현
   - **장단점**: AMI와 동일하지만, 1이 많은 데이터에 유리
   - **적용**: 특수 응용 분야에서 가끔 사용

### 핵심 코드: AMI 부호화 및 B8ZS 구현 (Python)

```python
from enum import Enum
from typing import List, Tuple, Optional
import numpy as np

class AMIViolationType(Enum):
    """AMI 위반 타입"""
    NONE = "No Violation"
    UNINTENTIONAL = "Unintentional (Error)"
    B8ZS_INTENTIONAL = "B8ZS Intentional"
    HDB3_INTENTIONAL = "HDB3 Intentional"

class AMICoder:
    """
    AMI (Alternate Mark Inversion) 부호화 구현

    특징:
    - 3-레벨 부호화: +V, 0V, -V
    - 0은 0V, 1은 ±V 교대
    - DC 성분 0
    - 오류 검출 가능 (AMI 위반)
    """

    def __init__(self, voltage_level: float = 1.0):
        self.V = voltage_level
        self.last_mark_polarity = -1  # -1 = last was -V, +1 = last was +V

    def encode(self, bits: List[int]) -> np.ndarray:
        """
        AMI 부호화

        Args:
            bits: 입력 비트 리스트

        Returns:
            전압 레벨 리스트
        """
        voltage = []
        self.last_mark_polarity = -1  # 초기화

        for bit in bits:
            if bit == 1:
                # 1이면 이전과 반대 극성
                self.last_mark_polarity = -self.last_mark_polarity
                voltage.append(self.V * self.last_mark_polarity)
            else:
                # 0이면 0V
                voltage.append(0)

        return np.array(voltage)

    def decode(self, voltage: np.ndarray) -> Tuple[List[int], List[AMIViolationType]]:
        """
        AMI 복호화 및 위반 탐지

        Returns:
            복호화된 비트 리스트, 위반 타입 리스트
        """
        bits = []
        violations = []
        expected_polarity = -1  # 다음 1에서 예상되는 극성

        for i, v in enumerate(voltage):
            if v == 0:
                bits.append(0)
                violations.append(AMIViolationType.NONE)
            else:
                bits.append(1)
                # 극성 검사
                current_polarity = 1 if v > 0 else -1

                if current_polarity == expected_polarity:
                    violations.append(AMIViolationType.NONE)
                else:
                    violations.append(AMIViolationType.UNINTENTIONAL)

                expected_polarity = -current_polarity

        return bits, violations

    def reset_state(self):
        """인코더 상태 초기화"""
        self.last_mark_polarity = -1


class B8ZSCoder:
    """
    B8ZS (Bipolar with 8-Zero Substitution) 부호화

    T1 회선(북미)에서 사용
    8개 연속 0을 특정 패턴으로 치환하여 동기화 유지
    """

    # B8ZS 치환 패턴: 000VB0VB (V=violation, B=normal bipolar)
    # 실제 전송: 000 (-V) (+V) 0 (-V) (+V) 또는 000 (+V) (-V) 0 (+V) (-V)

    def __init__(self, voltage_level: float = 1.0):
        self.V = voltage_level
        self.last_mark_polarity = -1

    def encode(self, bits: List[int]) -> np.ndarray:
        """B8ZS 부호화 (8개 연속 0 치환 포함)"""
        voltage = []
        i = 0

        while i < len(bits):
            # 8개 연속 0 확인
            if i + 8 <= len(bits) and all(bits[i+j] == 0 for j in range(8)):
                # B8ZS 치환 패턴 적용
                # 000VB0VB (V=violation, B=bipolar)
                # V: 이전 극성과 동일 (위반)
                # B: 이전 극성과 반대 (정상)

                violation_polarity = self.last_mark_polarity  # 위반: 이전과 동일
                bipolar_polarity = -self.last_mark_polarity   # 정상: 이전과 반대

                # 0 0 0 V B 0 V B
                voltage.extend([0, 0, 0])
                voltage.append(self.V * violation_polarity)
                voltage.append(self.V * bipolar_polarity)
                voltage.append(0)
                voltage.append(self.V * violation_polarity)
                voltage.append(self.V * bipolar_polarity)

                self.last_mark_polarity = bipolar_polarity  # 마지막 B의 극성
                i += 8
            else:
                # 일반 AMI 부호화
                bit = bits[i]
                if bit == 1:
                    self.last_mark_polarity = -self.last_mark_polarity
                    voltage.append(self.V * self.last_mark_polarity)
                else:
                    voltage.append(0)
                i += 1

        return np.array(voltage)

    def decode(self, voltage: np.ndarray) -> List[int]:
        """B8ZS 복호화 (치환 패턴을 8개 0으로 복원)"""
        bits = []
        i = 0

        while i < len(voltage):
            # B8ZS 패턴 확인 (000VB0VB)
            if i + 8 <= len(voltage):
                pattern = voltage[i:i+8]
                if self._is_b8zs_pattern(pattern):
                    # 8개 0으로 복원
                    bits.extend([0] * 8)
                    i += 8
                    continue

            # 일반 복호화
            bits.append(0 if voltage[i] == 0 else 1)
            i += 1

        return bits

    def _is_b8zs_pattern(self, pattern: np.ndarray) -> bool:
        """B8ZS 치환 패턴인지 확인"""
        # 000VB0VB 형태 확인
        # 위치 3, 4, 6, 7이 0이 아니고, 위치 0, 1, 2, 5가 0
        if not (pattern[0] == 0 and pattern[1] == 0 and pattern[2] == 0 and pattern[5] == 0):
            return False

        # V와 B의 극성 관계 확인
        v1, b1 = pattern[3], pattern[4]
        v2, b2 = pattern[6], pattern[7]

        if v1 == 0 or b1 == 0 or v2 == 0 or b2 == 0:
            return False

        # V1 == V2 (같은 극성의 위반) 그리고 B1 == B2
        return v1 == v2 and b1 == b2


class HDB3Coder:
    """
    HDB3 (High-Density Bipolar 3) 부호화

    E1 회선(유럽)에서 사용
    4개 연속 0마다 위반 펄스 삽입
    """

    def __init__(self, voltage_level: float = 1.0):
        self.V = voltage_level
        self.last_mark_polarity = -1
        self.pulse_count_since_last_substitution = 0

    def encode(self, bits: List[int]) -> np.ndarray:
        """HDB3 부호화 (4개 연속 0 치환 포함)"""
        voltage = []
        i = 0
        ones_count = 0  # 치환 후 1의 개수

        while i < len(bits):
            # 4개 연속 0 확인
            if i + 4 <= len(bits) and all(bits[i+j] == 0 for j in range(4)):
                # HDB3 치환 규칙
                # 이전 치환 후 1의 개수가 홀수면 000V
                # 이전 치환 후 1의 개수가 짝수면 B00V

                if ones_count % 2 == 1:
                    # 000V 패턴
                    violation_polarity = self.last_mark_polarity
                    voltage.extend([0, 0, 0, self.V * violation_polarity])
                    self.last_mark_polarity = violation_polarity
                else:
                    # B00V 패턴
                    bipolar_polarity = -self.last_mark_polarity
                    violation_polarity = bipolar_polarity
                    voltage.extend([self.V * bipolar_polarity, 0, 0, self.V * violation_polarity])
                    self.last_mark_polarity = violation_polarity

                ones_count = 0  # 치환 후 리셋
                i += 4
            else:
                # 일반 AMI 부호화
                bit = bits[i]
                if bit == 1:
                    self.last_mark_polarity = -self.last_mark_polarity
                    voltage.append(self.V * self.last_mark_polarity)
                    ones_count += 1
                else:
                    voltage.append(0)
                i += 1

        return np.array(voltage)


def compare_zero_suppression():
    """Zero Suppression 기술 비교"""

    print("\n" + "="*80)
    print("Zero Suppression Comparison: AMI vs B8ZS vs HDB3")
    print("="*80)

    # 문제 패턴: 8개 연속 0
    test_pattern = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    ami = AMICoder()
    b8zs = B8ZSCoder()
    hdb3 = HDB3Coder()

    ami_wave = ami.encode(test_pattern)
    b8zs_wave = b8zs.encode(test_pattern)
    hdb3_wave = hdb3.encode(test_pattern)

    print(f"\nInput Pattern: {test_pattern}")
    print(f"{'Coding':<10} | {'Max Zero Run':<15} | {'Transitions':<12} | {'DC Balance'}")
    print("-"*70)

    # 최대 0 연속 길이 계산
    def max_zero_run(wave):
        max_run = 0
        current = 0
        for v in wave:
            if v == 0:
                current += 1
                max_run = max(max_run, current)
            else:
                current = 0
        return max_run

    # 전이 횟수 계산
    def count_transitions(wave):
        return np.sum(np.abs(np.diff(wave)) > 0.1)

    print(f"{'AMI':<10} | {max_zero_run(ami_wave):<15} | {count_transitions(ami_wave):<12} | {np.mean(ami_wave):+.4f}")
    print(f"{'B8ZS':<10} | {max_zero_run(b8zs_wave):<15} | {count_transitions(b8zs_wave):<12} | {np.mean(b8zs_wave):+.4f}")
    print(f"{'HDB3':<10} | {max_zero_run(hdb3_wave):<15} | {count_transitions(hdb3_wave):<12} | {np.mean(hdb3_wave):+.4f}")

    print("\nConclusion:")
    print("  AMI: 8 consecutive zeros = synchronization lost")
    print("  B8ZS: Intentional violations at 8 zeros = sync maintained")
    print("  HDB3: Intentional violations at every 4 zeros = sync maintained")

    print("="*80)


def demonstrate_violation_detection():
    """AMI 위반 탐지 시연"""

    print("\n" + "="*70)
    print("AMI Bipolar Violation Detection Demonstration")
    print("="*70)

    ami = AMICoder()

    # 정상 패턴
    normal_pattern = [1, 0, 1, 1, 0, 1]
    normal_wave = ami.encode(normal_pattern)
    _, normal_violations = ami.decode(normal_wave)

    print(f"\nNormal Pattern: {normal_pattern}")
    print(f"Encoded: {[f'{v:+.1f}' if v != 0 else ' 0.0' for v in normal_wave]}")
    print(f"Violations: {[v.value for v in normal_violations]}")

    # 오류 주입 패턴 (3번째 비트 오류)
    corrupted_wave = normal_wave.copy()
    corrupted_wave[2] = corrupted_wave[1]  # 같은 극성으로 오류 주입

    _, corrupted_violations = ami.decode(corrupted_wave)

    print(f"\nCorrupted Pattern (b3 error):")
    print(f"Encoded: {[f'{v:+.1f}' if v != 0 else ' 0.0' for v in corrupted_wave]}")
    print(f"Violations: {[v.value for v in corrupted_violations]}")

    print("\nAMI can detect transmission errors through bipolar violations!")

    print("="*70)


# ==================== 실행 ====================
if __name__ == "__main__":
    compare_zero_suppression()
    demonstrate_violation_detection()
