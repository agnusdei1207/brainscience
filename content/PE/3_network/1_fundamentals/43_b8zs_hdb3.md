+++
title = "043. B8ZS / HDB3 (Zero Substitution Coding)"
description = "디지털 전송에서 연속된 0비트 문제를 해결하는 B8ZS와 HDB3 라인 코딩 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["B8ZS", "HDB3", "LineCoding", "ZeroSubstitution", "Bipolar", "T1", "E1", "PulseDensity"]
categories = ["studynotes-3_network"]
+++

# 043. B8ZS / HDB3 (Zero Substitution Coding)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: B8ZS(Bipolar with 8-Zero Substitution)와 HDB3(High-Density Bipolar 3)는 AMI 코딩에서 연속된 0비트로 인한 동기화 상실 문제를 해결하기 위해, 의도적으로 위반 펄스(Violation Pulse)를 삽입하는 적응형 라인 코딩 기법입니다.
> 2. **가치**: 이들 기법은 0비트가 연속되더라도 펄스 밀도를 유지하여 수신측의 클럭 복원을 보장하고, 전송 품질을 향상시키며, T1(미국/일본) 및 E1(유럽/한국) 디지털 전송망의 표준으로 채택되었습니다.
> 3. **융합**: 현대 광통신에서는 64B/66B, 8B/10B 등으로 진화했으나, B8ZS/HDB3의 동기화 유지 원리는 여전히 직렬 통신 설계의 근간이 되며, IoT 저전력 통신에서도 개념이 활용됩니다.

---

## Ⅰ. 개요 (Context & Background)

디지털 데이터 통신에서 **연속된 0비트**는 수신측에 심각한 문제를 야기합니다. AMI(Alternate Mark Inversion) 코딩에서 1비트는 교대로 +V, -V 펄스로 전송되지만, **0비트는 전압 레벨이 0V**로 유지됩니다. 따라서 연속된 0비트가 길게 이어지면:

1. **클럭 복원 불가**: 수신측은 전압 변화에서 타이밍 정보를 추출하는데, 0V 구간에서는 변화가 없어 클럭 동기화를 잃습니다.
2. **DC 성분 누적**: 긴 0 구간 후의 펄스는 DC 오프셋을 발생시켜 증폭기 포화를 유발할 수 있습니다.
3. **전력 스펙트럼 왜곡**: 저주파 성분이 증가하여 전송 매체의 주파수 응답 특성과 매칭이 어렵습니다.

### B8ZS와 HDB3의 차이점

| 특성 | B8ZS (T1) | HDB3 (E1) |
|------|-----------|-----------|
| **표준** | ANSI T1.403 (북미) | ITU-T G.703 (유럽/한국) |
| **적용 회선** | T1 (1.544 Mbps) | E1 (2.048 Mbps) |
| **대체 대상** | 8개 연속 0 | 4개 연속 0 |
| **위반 방식** | 000VB0VB | 000V 또는 B00V |
| **위반 위치** | 8비트 중 특정 위치 | 4비트 중 마지막 비트 |

**💡 비유**: B8ZS/HDB3는 **'침묵을 깨는 암호'**와 같습니다.
- 통신 회선은 마치 대화와 같아서, 상대방이 계속 말을 해야 타이밍을 맞출 수 있습니다.
- 하지만 "00000..."라는 침묵(0비트)이 길어지면 상대방은 "아직 연결됐나?" 의심하게 됩니다.
- B8ZS/HDB3는 침묵이 너무 길어지면 "의미 없는 기침 소리(위반 펄스)"를 내어 연결을 유지합니다.
- 이 기침은 미리 정해진 패턴이라 수신측은 "이건 데이터가 아니라 동기용 신호구나" 알고 제거합니다.

**등장 배경 및 발전 과정**:

1. **AMI의 한계 발견 (1960년대)**:
   초기 T1/E1 디지털 전송망은 AMI(Alternate Mark Inversion) 코딩을 사용했습니다. 그러나 팩스 전송, 데이터 통신에서 연속된 0이 빈번히 발생하여 동기화 상실로 인한 프레임 슬립(Frame Slip) 오류가 빈번했습니다.

2. **Pulse Density 요구사항**:
   Bell Labs의 연구에 따르면 안정적인 클럭 복원을 위해 최소 12.5% 이상의 펄스 밀도(1의 비율)가 필요했습니다. 이를 위해 0을 강제로 1로 바꾸되, 수신측이 원래 데이터를 복원할 수 있는 방법이 연구되었습니다.

3. **B8ZS의 표준화 (1970년대)**:
   북미의 T1 표준(ANSI)에서 B8ZS가 채택되었습니다. 8개의 연속 0을 특정 위반 패턴으로 대체하여 동시에 두 가지 목표를 달성했습니다: (1) 펄스 밀도 유지, (2) 수신측에서 원본 데이터 복원 가능.

4. **HDB3의 표준화 및 글로벌 확산**:
   유럽의 E1 표준(ITU-T, 구 CCITT)에서는 4개 연속 0만 있어도 대체하는 더 공격적인 HDB3가 채택되었습니다. 한국을 포함한 대부분 국가가 E1/HDB3를 사용합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### AMI 코딩의 기본 원리 (선행 지식)

```
AMI (Alternate Mark Inversion):
- 1비트: +V, -V 교대로 전송 (Bipolar)
- 0비트: 0V (무편향)

예시:
데이터:      1  0  1  1  0  0  0  0  0  0  0  0  1
AMI:        +V  0 -V +V  0  0  0  0  0  0  0  0 -V
                    ↑                      ↑
                 교대 규칙              0이 8개 연속!
```

**AMI의 문제**: 0이 15개 이상 연속되면 수신측 클럭 복원 회로가 자유 주파수(Free-running)로 도약하여 타이밍 오류 발생.

### B8ZS (Bipolar with 8-Zero Substitution)

#### 동작 원리
B8ZS는 **8개의 연속 0**을 감지하면, 이를 특수한 **위반 패턴(Violation Pattern)**으로 대체합니다. 이 패턴은 AMI 규칙을 고의로 위반하는 펄스를 포함하여, 수신측이 이를 감지하고 원래의 8개 0으로 복원합니다.

```
B8ZS 대체 규칙:
- 8개 연속 0 감지 시 → 000VB0VB로 대체
  여기서:
  V = Bipolar Violation (이전 펄스와 동일 극성)
  B = Bipolar (정상 AMI 극성)

위반 패턴의 두 가지 형태 (이전 1의 극성에 따라):
1. 이전 1이 +V였을 때: 000 +V 0 -V +V -V
2. 이전 1이 -V였을 때: 000 -V 0 +V -V +V
```

#### B8ZS 인코딩 예시

```
원본 데이터:    1 0 0 0 0 0 0 0 0 1
이전 극성:      - (처음이므로 +V 가정)

AMI (B8ZS 적용 전):
               +V 0 0 0 0 0 0 0 0 -V
                  ↑ 8개 연속 0! 동기화 위험

B8ZS (8개 0을 대체):
               +V 0 0 0 +V 0 -V +V -V -V
                     ↑ V  ↑ B  ↑ V  ↑ B
                     위반     위반

               (V는 이전 +V와 같은 극성 → AMI 위반!)
               (수신측은 위반을 감지하고 8개 0으로 복원)
```

### HDB3 (High-Density Bipolar 3)

#### 동작 원리
HDB3는 **4개의 연속 0**을 감지하면 대체합니다. B8ZS보다 더 빈번하게 대체하여 더 높은 펄스 밀도를 보장합니다.

```
HDB3 대체 규칙:
- 4개 연속 0 감지 시 → 000V 또는 B00V로 대체
  선택 기준: 이전 V 펄스 이후 전송된 1(B)의 개수가
            홀수면 000V, 짝수면 B00V

여기서:
V = Bipolar Violation (이전 펄스와 동일 극성)
B = Bipolar (정상 AMI 극성의 1)
```

#### HDB3 인코딩 예시

```
원본 데이터:    1 0 0 0 0 0 0 0 1 0 0 0 0
기본 AMI:      +V 0 0 0 0 0 0 0 -V 0 0 0 0
                  ↑4개0  ↑4개0         ↑4개0

HDB3 적용:
               +V 0 0 0 +V 0 0 -V -V -V +V 0 0
                     ↑ V        ↑ V  ↑ B
                  (이전 V 후 1이 없어 홀수→000V)
                           (이전 V 후 1이 1개, 홀수→000V)
                                    (이전 V 후 1이 0개, 홀수→000V)

다른 예 (B00V 케이스):
원본:          1 1 0 0 0 0
이전 극성:     +V -V
HDB3:         +V -V +V 0 0 +V
                   ↑ B       ↑ V
             (이전 V 후 1이 2개, 짝수→B00V)
             V는 -V여야 하지만 +V가 와서 위반!
```

### 정교한 구조 다이어그램: B8ZS/HDB3 인코딩 비교

```ascii
================================================================================
[ B8ZS vs HDB3: Encoding Comparison ]
================================================================================

입력 데이터:  1  1  0  0  0  0  0  0  0  0  0  0  1  1  0  0  0  0

=== AMI (Baseline) ===
             +V -V  0  0  0  0  0  0  0  0  0  0 +V -V  0  0  0  0
                       |-- 8개 연속 0 --|          |-- 4개 연속 0 --|
                       동기화 위험!                    동기화 위험!

=== B8ZS (T1 표준) ===
             +V -V  0  0  0 -V  0 +V -V +V  0  0 +V -V  0  0  0  0
                       |-- 대체 --|  V=위반         4개 0은 대체 안함!
                          ↑
                    B8ZS는 8개 0만 대체

=== HDB3 (E1 표준) ===
             +V -V  0  0  0 +V  0  0  0 -V +V +V -V -V +V  0  0 +V
                       |V=위반|  |B=정상| V=위반          |V=위반|
                    4개 0을 000V로    4개 0을 B00V로    4개 0을 000V로

================================================================================
[ B8ZS Violation Pattern Detail ]
================================================================================

  데이터: ... 1 0 0 0 0 0 0 0 0 1 ...
                    |<-- 8 zeros -->|

  Case A: 이전 1이 +V였을 때
  ───────────────────────────────
  AMI 규칙: 다음 1은 -V여야 함

  B8ZS 출력:
     ... +V 0 0 0 +V 0 -V +V -V -V ...
               ↑   ↑   ↑   ↑
               V1  V2  B1  B2

  V1 (+V): 이전 +V와 같은 극성 → AMI 위반!
  V2 (-V): 정상 AMI 극성
  B1 (+V): V2의 -V와 다른 극성 → 정상
  B2 (-V): B1의 +V와 다른 극성 → 정상

  위반 패턴: 연속된 2개의 동일 극성 펄스
  수신측: V1과 V2 사이의 위반을 감지 → 8개 0으로 복원


  Case B: 이전 1이 -V였을 때
  ───────────────────────────────
  AMI 규칙: 다음 1은 +V여야 함

  B8ZS 출력:
     ... -V 0 0 0 -V 0 +V -V +V +V ...
               ↑   ↑   ↑   ↑
               V1  V2  B1  B2

  V1 (-V): 이전 -V와 같은 극성 → AMI 위반!

================================================================================
[ HDB3 State Machine ]
================================================================================

         +--------+     4 zeros     +--------+
         |  IDLE  | ---------------->| CHECK  |
         |        |                   |  B count|
         +--------+                   +----+---+
              ^                            |
              |          +-----------------+------------------+
              |          |                 |                  |
              |     odd B count       even B count       no B
              |          |                 |                  |
              |          v                 v                  v
              |    +----------+     +----------+      +----------+
              |    |  000V    |     |  B00V    |      |  000V    |
              |    | 대체     |     | 대체     |      | 대체     |
              |    +----+-----+     +----+-----+      +----+-----+
              |         |                |                 |
              |         +----------------+-----------------+
              |                          |
              +--------------------------+

  V (Violation): 이전 펄스와 동일 극성 (AMI 위반)
  B (Bipolar): 정상 AMI 극성의 펄스

================================================================================
[ Pulse Density Comparison ]
================================================================================

  데이터: 16비트, 1이 2개 (12.5% 펄스 밀도)

  AMI:     0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1
           |<-------- 12개 연속 0 -------->|   |<--- 7개 0 --->|
           클럭 복원 실패 가능성 높음

  B8ZS:    0 0 0 0 0 0 0 +V 0 -V +V -V 1 0 0 0 0 0 0 0 0 0 0 0 0 1
                   |<-- 대체 -->|
           펄스 5개 추가 → 밀도 향상

  HDB3:    0 0 0 +V 0 0 0 -V +V 0 0 +V -V 1 +V 0 0 0 -V 0 0 0 +V 0 1
              V     V  B     V        B  V     V        V
           4개마다 대체 → 최고 밀도

================================================================================
```

### 핵심 코드: B8ZS/HDB3 인코더/디코더 구현 (Python)

```python
from enum import Enum
from typing import List, Tuple
from dataclasses import dataclass

class Pulse(Enum):
    """펄스 상태 정의"""
    ZERO = 0       # 0V
    POSITIVE = 1   # +V
    NEGATIVE = -1  # -V

@dataclass
class CodingResult:
    """코딩 결과"""
    data: List[Pulse]
    violations: int = 0
    substitutions: int = 0

class AMIEncoder:
    """기본 AMI 인코더"""

    def __init__(self):
        self.last_polarity = Pulse.NEGATIVE  # 다음 1은 +V로 시작

    def encode(self, data: List[int]) -> List[Pulse]:
        """AMI 인코딩"""
        result = []
        for bit in data:
            if bit == 1:
                # 극성 교대
                self.last_polarity = (
                    Pulse.POSITIVE if self.last_polarity == Pulse.NEGATIVE
                    else Pulse.NEGATIVE
                )
                result.append(self.last_polarity)
            else:
                result.append(Pulse.ZERO)
        return result

class B8ZSEncoder:
    """B8ZS 인코더"""

    def __init__(self):
        self.last_polarity = Pulse.NEGATIVE

    def encode(self, data: List[int]) -> CodingResult:
        """B8ZS 인코딩"""
        result: List[Pulse] = []
        violations = 0
        substitutions = 0

        i = 0
        while i < len(data):
            # 8개 연속 0 확인
            if i + 8 <= len(data) and all(data[i:i+8] == 0 for _ in range(1)):
                zeros = data[i:i+8]
                if all(z == 0 for z in zeros):
                    # B8ZS 대체 패턴 삽입
                    if self.last_polarity == Pulse.POSITIVE:
                        # 000 +V 0 -V +V -V
                        pattern = [
                            Pulse.ZERO, Pulse.ZERO, Pulse.ZERO,
                            Pulse.POSITIVE,   # V (위반: 이전과 같은 극성)
                            Pulse.ZERO,
                            Pulse.NEGATIVE,   # 정상 극성
                            Pulse.POSITIVE,   # 정상 극성
                            Pulse.NEGATIVE    # 정상 극성
                        ]
                    else:
                        # 000 -V 0 +V -V +V
                        pattern = [
                            Pulse.ZERO, Pulse.ZERO, Pulse.ZERO,
                            Pulse.NEGATIVE,   # V (위반)
                            Pulse.ZERO,
                            Pulse.POSITIVE,   # 정상 극성
                            Pulse.NEGATIVE,   # 정상 극성
                            Pulse.POSITIVE    # 정상 극성
                        ]

                    result.extend(pattern)
                    self.last_polarity = pattern[-1]
                    violations += 2
                    substitutions += 1
                    i += 8
                    continue

            # 일반 비트 처리
            bit = data[i]
            if bit == 1:
                self.last_polarity = (
                    Pulse.POSITIVE if self.last_polarity == Pulse.NEGATIVE
                    else Pulse.NEGATIVE
                )
                result.append(self.last_polarity)
            else:
                result.append(Pulse.ZERO)
            i += 1

        return CodingResult(result, violations, substitutions)

    def decode(self, pulses: List[Pulse]) -> Tuple[List[int], int]:
        """B8ZS 디코딩"""
        result: List[int] = []
        corrections = 0

        i = 0
        while i < len(pulses):
            # B8ZS 위반 패턴 확인: 000V0VBVB
            if i + 8 <= len(pulses):
                window = pulses[i:i+8]

                # 위반 패턴 감지 (000 +V 0 -V +V -V 또는 000 -V 0 +V -V +V)
                if (window[0] == Pulse.ZERO and
                    window[1] == Pulse.ZERO and
                    window[2] == Pulse.ZERO and
                    window[3] != Pulse.ZERO and  # V
                    window[4] == Pulse.ZERO and
                    window[5] != Pulse.ZERO and  # B1
                    window[6] != Pulse.ZERO and  # B2
                    window[7] != Pulse.ZERO):    # B3

                    # 위반 패턴 확인 (V와 B1이 같은 극성이면 위반)
                    if window[3] == window[5]:
                        # 8개 0으로 복원
                        result.extend([0] * 8)
                        corrections += 1
                        i += 8
                        continue

            # 일반 펄스 처리
            if pulses[i] == Pulse.ZERO:
                result.append(0)
            else:
                result.append(1)
            i += 1

        return result, corrections

class HDB3Encoder:
    """HDB3 인코더"""

    def __init__(self):
        self.last_polarity = Pulse.NEGATIVE
        self.last_violation_polarity = Pulse.NEGATIVE

    def encode(self, data: List[int]) -> CodingResult:
        """HDB3 인코딩"""
        result: List[Pulse] = []
        violations = 0
        substitutions = 0
        ones_since_last_v = 0

        i = 0
        while i < len(data):
            # 4개 연속 0 확인
            if i + 4 <= len(data):
                if all(data[j] == 0 for j in range(i, min(i+4, len(data)))):
                    # HDB3 대체
                    if ones_since_last_v % 2 == 0:
                        # 짝수 개의 1 → B00V
                        # B는 정상 극성, V는 위반 (이전과 같은 극성)
                        b_polarity = (
                            Pulse.POSITIVE if self.last_polarity == Pulse.NEGATIVE
                            else Pulse.NEGATIVE
                        )
                        v_polarity = self.last_violation_polarity

                        pattern = [
                            b_polarity,
                            Pulse.ZERO,
                            Pulse.ZERO,
                            v_polarity  # 위반
                        ]
                        self.last_polarity = b_polarity
                        self.last_violation_polarity = (
                            Pulse.POSITIVE if v_polarity == Pulse.NEGATIVE
                            else Pulse.NEGATIVE
                        )
                    else:
                        # 홀수 개의 1 → 000V
                        v_polarity = self.last_violation_polarity
                        pattern = [
                            Pulse.ZERO,
                            Pulse.ZERO,
                            Pulse.ZERO,
                            v_polarity  # 위반
                        ]
                        self.last_violation_polarity = (
                            Pulse.POSITIVE if v_polarity == Pulse.NEGATIVE
                            else Pulse.NEGATIVE
                        )

                    result.extend(pattern)
                    violations += 1
                    substitutions += 1
                    ones_since_last_v = 0
                    i += 4
                    continue

            # 일반 비트 처리
            bit = data[i]
            if bit == 1:
                self.last_polarity = (
                    Pulse.POSITIVE if self.last_polarity == Pulse.NEGATIVE
                    else Pulse.NEGATIVE
                )
                result.append(self.last_polarity)
                ones_since_last_v += 1
            else:
                result.append(Pulse.ZERO)
            i += 1

        return CodingResult(result, violations, substitutions)

def pulse_to_string(pulses: List[Pulse]) -> str:
    """펄스 리스트를 문자열로 변환"""
    result = ""
    for p in pulses:
        if p == Pulse.ZERO:
            result += " 0 "
        elif p == Pulse.POSITIVE:
            result += "+V "
        else:
            result += "-V "
    return result

def analyze_pulse_density(pulses: List[Pulse]) -> float:
    """펄스 밀도 분석"""
    if not pulses:
        return 0.0
    non_zero = sum(1 for p in pulses if p != Pulse.ZERO)
    return non_zero / len(pulses) * 100

# 사용 예시
if __name__ == "__main__":
    # 테스트 데이터: 8개 연속 0 포함
    test_data = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

    print("=" * 60)
    print("B8ZS/HDB3 인코딩 비교")
    print("=" * 60)
    print(f"\n원본 데이터: {test_data}")
    print(f"비트 1 개수: {sum(test_data)} ({sum(test_data)/len(test_data)*100:.1f}%)")

    # B8ZS 인코딩
    b8zs_encoder = B8ZSEncoder()
    b8zs_result = b8zs_encoder.encode(test_data)
    print(f"\n--- B8ZS 인코딩 ---")
    print(f"출력 펄스: {pulse_to_string(b8zs_result.data)}")
    print(f"위반 횟수: {b8zs_result.violations}")
    print(f"대체 횟수: {b8zs_result.substitutions}")
    print(f"펄스 밀도: {analyze_pulse_density(b8zs_result.data):.1f}%")

    # HDB3 인코딩
    hdb3_encoder = HDB3Encoder()
    hdb3_result = hdb3_encoder.encode(test_data)
    print(f"\n--- HDB3 인코딩 ---")
    print(f"출력 펄스: {pulse_to_string(hdb3_result.data)}")
    print(f"위반 횟수: {hdb3_result.violations}")
    print(f"대체 횟수: {hdb3_result.substitutions}")
    print(f"펄스 밀도: {analyze_pulse_density(hdb3_result.data):.1f}%")

    # AMI (비교용)
    ami_encoder = AMIEncoder()
    ami_result = ami_encoder.encode(test_data)
    print(f"\n--- AMI (비교용) ---")
    print(f"출력 펄스: {pulse_to_string(ami_result)}")
    print(f"펄스 밀도: {analyze_pulse_density(ami_result):.1f}%")
