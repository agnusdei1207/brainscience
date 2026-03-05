+++
title = "042. 블록 부호화 (4B/5B, 8B/10B Coding)"
description = "m비트를 n비트(n>m)로 매핑하여 DC 밸런스와 동기화를 보장하는 블록 부호화 기법의 원리를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["4B5B", "8B10B", "BlockCoding", "DCBalance", "Ethernet", "PCIe", "FiberChannel"]
categories = ["studynotes-3_network"]
+++

# 042. 블록 부호화 (4B/5B, 8B/10B Coding)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 블록 부호화는 m비트의 데이터를 n비트(n>m)의 코드워드로 매핑하여, DC 밸런스(0과 1의 균형), 충분한 전이(Transition), 제어 코드 전송을 동시에 보장하는 라인 코딩 기술입니다.
> 2. **가치**: 4B/5B는 100Mbps 이더넷(100BASE-TX/FX)과 FDDI에서, 8B/10B는 기가비트 이더넷(1000BASE-X), PCIe, USB 3.0, SATA에서 표준으로 채택되어 고속 신뢰성 통신의 핵심이 되었습니다.
> 3. **융합**: 8B/10B는 IBM의 Peter Franaszek과 Al Widmer가 개발했으며, 이후 64B/66B(10GbE), 128B/132B(USB 3.1), 128B/130B(PCIe 3.0+)로 진화하여 오버헤드를 최소화하는 방향으로 발전했습니다.

---

## I. 개요 (Context & Background)

블록 부호화(Block Coding) 또는 mB/nB 코딩은 m비트의 입력 데이터 블록을 n비트(n>m)의 출력 코드워드로 변환하는 선로 부호화 기술입니다. 추가된 (n-m)비트는 **DC 밸런스 유지**, **동기화를 위한 전이 보장**, **제어 신호 전송**의 세 가지 목적으로 사용됩니다.

**💡 비유**: 블록 부호화는 **'암호화된 메시지 작성'**과 같습니다.
- 원본 메시지(4비트 데이터)를 그대로 보내면, 같은 문자가 반복될 때(예: AAAAA) 패턴이 드러납니다.
- 블록 부호화는 각 문자를 더 긴 암호(5비트 코드워드)로 변환합니다. A는 'XK7P'로, B는 'QM3T'로...
- 이 암호는 0과 1의 개수가 항상 비슷하게 유지되도록 설계되어 있어, 어떤 메시지를 보내도 균형이 맞습니다.
- 또한 특별한 암호('K28.5' 등)는 "여기서부터 데이터 시작" 같은 제어 신호로 사용됩니다.

**등장 배경 및 발전 과정**:
1. **NRZ의 한계 극복 (1980년대)**: FDDI(Fiber Distributed Data Interface, 100Mbps 광섬유 망)에서 NRZ의 동기화 문제를 해결하기 위해 4B/5B가 개발되었습니다.
2. **IBM의 혁신 (1983년)**: IBM의 Peter Franaszek과 Al Widmer가 8B/10B를 발명했습니다. DC 밸런스와 전이 밀도를 동시에 보장하는 획기적인 설계로, 이후 수십 년간 업계 표준이 되었습니다.
3. **고속화에 따른 진화 (2000년대~)**: 10GbE에서는 8B/10B의 25% 오버헤드가 부담스러워 64B/66B가 개발되었습니다. PCIe 3.0, USB 3.1 등도 128B/130B, 128B/132B로 전환했습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 부호화 방식 | 입력/출력 비트 | 오버헤드 | DC 밸런스 | 전이 밸런스 | 대역폭 효율 | 적용 표준 |
|------------|--------------|---------|----------|-----------|-----------|----------|
| **4B/5B** | 4 → 5 | 25% | 중간 | 우수 | 80% | 100BASE-TX/FX, FDDI |
| **8B/10B** | 8 → 10 | 25% | 우수 | 우수 | 80% | 1000BASE-X, PCIe 1/2, USB 3.0 |
| **64B/66B** | 64 → 66 | 3.1% | 우수 | 양호 | 97% | 10GBASE-R, 40GBASE-R |
| **128B/130B** | 128 → 130 | 1.5% | 우수 | 양호 | 98.5% | PCIe 3.0+ |
| **128B/132B** | 128 → 132 | 3.1% | 우수 | 양호 | 97% | USB 3.1/3.2 |

### 정교한 구조 다이어그램: 4B/5B 부호화

```ascii
================================================================================
[ 4B/5B Encoding Table ]
================================================================================

4B/5B maps every 4-bit nibble to a 5-bit codeword.

Requirements for valid 5B codewords:
  1. No more than three consecutive 0s
  2. At least two transitions per codeword (for clock recovery)
  3. Special control symbols for framing

Data Codewords:
+----------+------------+----------+------------+
| 4-bit    | 5-bit      | 4-bit    | 5-bit      |
| Data     | Code       | Data     | Code       |
+----------+------------+----------+------------+
| 0000 (0) | 11110      | 1000 (8) | 10010      |
| 0001 (1) | 01001      | 1001 (9) | 10011      |
| 0010 (2) | 10100      | 1010 (A) | 10110      |
| 0011 (3) | 10101      | 1011 (B) | 10111      |
| 0100 (4) | 01010      | 1100 (C) | 11010      |
| 0101 (5) | 01011      | 1101 (D) | 11011      |
| 0110 (6) | 01110      | 1110 (E) | 11100      |
| 0111 (7) | 01111      | 1111 (F) | 11101      |
+----------+------------+----------+------------+

Control Codewords (for framing):
+----------+------------+----------------------------------------+
| Symbol   | 5-bit      | Function                               |
+----------+------------+----------------------------------------+
| Idle (I) | 11111      | Line idle (continuous 1s)              |
| J        | 11000      | Start delimiter part 1                 |
| K        | 10001      | Start delimiter part 2                 |
| T        | 01101      | End delimiter (Reset)                  |
| R        | 00111      | End delimiter (Reset)                  |
| S        | 11001      | Start of packet                        |
| Q        | 00000      | Quiet (unused - violates run length!)  |
| H        | 00100      | Halt (error signal)                    |
+----------+------------+----------------------------------------+

================================================================================
[ 4B/5B Encoding Process ]
================================================================================

Example: Encoding the byte 0xA5 (binary: 1010 0101)

Input: 1010 0101
        ^^^^ ^^^^
        |    |
        |    +-- Lower nibble: 0101 (5)
        +------- Upper nibble: 1010 (A)

Encoding:
  Upper nibble (A = 1010) → 10110
  Lower nibble (5 = 0101) → 01011

Output (10 bits): 10110 01011

+-------+          +---------+
| 1010  |  4B/5B   |  10110  |
| (A)   |--------->|         |
+-------+          +---------+
                        |
                        v
+-------+          +---------+
| 0101  |  4B/5B   |  01011  |
| (5)   |--------->|         |
+-------+          +---------+

Final 10-bit output: 1011001011

================================================================================
[ 4B/5B Combined with NRZI ]
================================================================================

4B/5B alone doesn't guarantee DC balance. It's typically combined with NRZI:

Data → 4B/5B Encoding → NRZI Encoding → Physical Medium

Example transmission:
  Original:   0xA5 = 1010 0101
  4B/5B:      10110 01011
  NRZI:       -+--+ +--+- (transitions for 1s)

NRZI ensures transitions for every '1', and 4B/5B ensures enough 1s exist!

================================================================================
[ 8B/10B Encoding Structure ]
================================================================================

8B/10B splits the 8-bit byte into:
  - 5-bit group (D.x.y notation, or control K.x.y)
  - 3-bit group

Encoding:
  5-bit (EDCBA) → 6-bit (abcdei) using 5B/6B table
  3-bit (HGF)   → 4-bit (fghj) using 3B/4B table

Result: 10-bit codeword (abcdeifghj)

+--------+          +--------+          +------------------+
| 8-bit  |          | 5-bit  |  5B/6B   | 6-bit            |
| Byte   |--------->| Group  |--------->| (abcdei)         |
| HGFEDCBA|         | EDCBA  |          |                  |
+--------+          +--------+          +------------------+
     |                                       |
     | 3-bit group                           |
     v                                       v
+--------+          3B/4B   +--------+   +--------+
| HGF    |----------------->| 4-bit  |   | Full   |
|        |                  | (fghj) |   | 10-bit |
+--------+                  +--------+   +--------+
                                            abcdeifghj

================================================================================
[ 8B/10B Running Disparity (RD) Control ]
================================================================================

KEY INNOVATION: Running Disparity ensures DC balance over time!

Each 10-bit codeword has TWO possible encodings:
  - Positive Disparity (RD+): More 1s than 0s, or equal
  - Negative Disparity (RD-): More 0s than 1s, or equal

The encoder tracks the current Running Disparity (RD):
  - If current RD is positive, use negative-disparity codeword
  - If current RD is negative, use positive-disparity codeword
  - This ensures long-term DC balance!

Example: Data Byte D0.0 (0x00)

6-bit part (5B/6B):
  RD- encoding: 100111
  RD+ encoding: 011000

4-bit part (3B/4B):
  RD- encoding: 1010
  RD+ encoding: 0101

Full 10-bit codewords:
  RD-: 100111 1010 (6 ones, 4 zeros = RD+)
  RD+: 011000 0101 (4 ones, 6 zeros = RD-)

Encoding Process:
  Start with RD- (negative)

  Byte 1: Use RD- codeword → Result is RD+, switch to RD+
  Byte 2: Use RD+ codeword → Result is RD-, switch to RD-
  ...

This ensures the cumulative difference between 1s and 0s stays bounded!

================================================================================
[ Running Disparity State Machine ]
================================================================================

                    +------------------+
                    |   Current RD     |
                    +--------+---------+
                             |
              +--------------+--------------+
              |                             |
              v                             v
        RD- (Negative)               RD+ (Positive)
        (More 0s recently)           (More 1s recently)
              |                             |
              |                             |
    +---------v---------+         +---------v---------+
    | Select codeword   |         | Select codeword   |
    | with RD+ bias     |         | with RD- bias     |
    +---------+---------+         +---------+---------+
              |                             |
              |                             |
              v                             v
        Output has                Output has
        net RD+ effect            net RD- effect
              |                             |
              |                             |
              +------------+----------------+
                           |
                           v
                    Update RD for
                    next codeword

RD Update Rules:
  - If codeword has equal 1s and 0s (neutral): RD unchanged
  - If codeword has more 1s (RD+): Switch to RD- for next
  - If codeword has more 0s (RD-): Switch to RD+ for next

Result: Maximum DC offset = ±1 codeword bias = bounded DC wander

================================================================================
[ Control Symbols in 8B/10B ]
================================================================================

Control symbols (K-codes) are used for:
  - Packet delimiters (Start-of-Packet, End-of-Packet)
  - Idle sequences
  - Error signaling
  - Link management

Common K-codes:
+----------+------------+----------------------------------------+
| Symbol   | 8-bit Hex  | Function                               |
+----------+------------+----------------------------------------+
| K28.0    | 1C         | Reserved / Vendor specific             |
| K28.1    | 3C         |not used alone                          |
| K28.2    | 5C         |not used alone                          |
| K28.3    | 7C         | Reserved                               |
| K28.4    | 9C         |not used alone                          |
| K28.5    | BC         | COMMA - Sync pattern (001111 1010)     |
| K28.6    | DC         |not used alone                          |
| K28.7    | FC         | Reserved                               |
| K23.7    | F7         | Packet Start (PCIe)                    |
| K27.7    | FB         | Packet End (PCIe)                      |
| K29.7    | FD         | Packet End / Comma                     |
| K30.7    | FE         | Packet End                             |
+----------+------------+----------------------------------------+

K28.5 (COMMA) Pattern:
  RD-: 001111 1010 (unique bit pattern for synchronization)
  RD+: 110000 0101

  This pattern is used for:
    - Bit synchronization (comma detection)
    - Byte boundary alignment
    - Link initialization

================================================================================
```

### 심층 동작 원리: 5가지 핵심 메커니즘

1. **mB/nB 매핑 (mB/nB Mapping)**:
   - **핵심 원리**: m비트 입력을 n비트 출력으로 매핑합니다 (n > m).
   - **코드 공간**: 2^n개의 가능한 출력 중에서 '좋은' 특성을 가진 2^m개를 선택합니다.
   - **좋은 특성**: 충분한 전이, 제한된 연속 0, 적절한 DC 밸런스.

2. **Running Disparity (RD, 8B/10B의 핵심)**:
   - **정의**: 누적된 1과 0의 차이. RD+는 1이 많음, RD-는 0이 많음.
   - **동작**: 각 코드워드는 RD+ 버전과 RD- 버전이 있습니다. 현재 RD와 반대 부호의 코드워드를 선택하여 RD를 상쇄합니다.
   - **결과**: 장기적으로 DC 성분이 0에 수렴합니다.

3. **전이 밀도 보장 (Transition Density Guarantee)**:
   - **4B/5B**: 최대 연속 0이 3개로 제한됩니다.
   - **8B/10B**: 최대 연속 0 또는 1이 5개로 제한됩니다.
   - **효과**: 클럭 복구 회로(PLL, CDR)가 안정적으로 동작합니다.

4. **제어 심볼 (Control Symbols)**:
   - **K-코드**: 일반 데이터와 구별되는 특별한 코드워드입니다.
   - **용도**: 패킷 시작/종료, 아이들 패턴, 오류 신호, 동기화(Comma).
   - **Comma 패턴**: K28.5의 '0011111' 또는 '1100000'은 바이트 경계 탐지에 사용됩니다.

5. **오버헤드 vs 신뢰성 트레이드오프 (Overhead vs Reliability)**:
   - **8B/10B**: 25% 오버헤드지만 강력한 DC 밸런스와 전이 보장.
   - **64B/66B**: 3.1% 오버헤드로 줄였지만, Scrabmling에 의존하여 DC 밸런스 달성.
   - **진화 방향**: 더 높은 속도에서는 오버헤드 최소화가 중요해집니다.

### 핵심 코드: 4B/5B 및 8B/10B 구현 (Python)

```python
from enum import Enum
from typing import List, Tuple, Dict
import numpy as np

class RunningDisparity(Enum):
    """Running Disparity 상태"""
    NEGATIVE = -1  # RD-: More 0s recently
    POSITIVE = 1   # RD+: More 1s recently

class FourBFiveBCoder:
    """
    4B/5B 부호화 구현

    특징:
    - 4비트 데이터를 5비트 코드워드로 매핑
    - FDDI, 100BASE-TX/FX에서 사용
    - NRZI와 결합하여 사용
    """

    # 4B/5B 데이터 코드 테이블
    DATA_CODES = {
        0x0: 0b11110, 0x1: 0b01001, 0x2: 0b10100, 0x3: 0b10101,
        0x4: 0b01010, 0x5: 0b01011, 0x6: 0b01110, 0x7: 0b01111,
        0x8: 0b10010, 0x9: 0b10011, 0xA: 0b10110, 0xB: 0b10111,
        0xC: 0b11010, 0xD: 0b11011, 0xE: 0b11100, 0xF: 0b11101,
    }

    # 4B/5B 제어 코드 테이블
    CONTROL_CODES = {
        'I': 0b11111,  # Idle
        'J': 0b11000,  # Start delimiter 1
        'K': 0b10001,  # Start delimiter 2
        'T': 0b01101,  # End delimiter (Reset)
        'R': 0b00111,  # End delimiter (Reset)
        'S': 0b11001,  # Start of packet
        'H': 0b00100,  # Halt
    }

    def encode_byte(self, byte: int) -> Tuple[int, int]:
        """
        1바이트(8비트)를 2개의 5비트 코드워드로 인코딩

        Returns:
            (upper_5b, lower_5b)
        """
        upper_nibble = (byte >> 4) & 0xF
        lower_nibble = byte & 0xF

        upper_5b = self.DATA_CODES[upper_nibble]
        lower_5b = self.DATA_CODES[lower_nibble]

        return upper_5b, lower_5b

    def encode(self, data: bytes) -> List[int]:
        """
        바이트 시퀀스를 5비트 코드워드 시퀀스로 인코딩
        """
        codewords = []

        for byte in data:
            upper, lower = self.encode_byte(byte)
            codewords.append(upper)
            codewords.append(lower)

        return codewords

    def decode(self, codewords: List[int]) -> bytes:
        """
        5비트 코드워드 시퀀스를 바이트로 디코딩
        """
        # 역 매핑 테이블 생성
        reverse_data = {v: k for k, v in self.DATA_CODES.items()}

        result = bytearray()

        for i in range(0, len(codewords), 2):
            if i + 1 >= len(codewords):
                break

            upper = codewords[i]
            lower = codewords[i + 1]

            if upper not in reverse_data or lower not in reverse_data:
                raise ValueError(f"Invalid codeword at position {i}")

            byte = (reverse_data[upper] << 4) | reverse_data[lower]
            result.append(byte)

        return bytes(result)

    def encode_with_delimiters(self, data: bytes) -> List[int]:
        """
        시작/종료 구분자를 포함한 인코딩
        """
        codewords = []

        # Start delimiter: J K
        codewords.append(self.CONTROL_CODES['J'])
        codewords.append(self.CONTROL_CODES['K'])

        # Data
        codewords.extend(self.encode(data))

        # End delimiter: T R
        codewords.append(self.CONTROL_CODES['T'])
        codewords.append(self.CONTROL_CODES['R'])

        return codewords

    def analyze_transition_density(self, codewords: List[int]) -> dict:
        """전이 밀도 분석"""
        bit_stream = []
        for cw in codewords:
            for i in range(4, -1, -1):
                bit_stream.append((cw >> i) & 1)

        # 연속 0의 최대 길이
        max_zero_run = 0
        current_run = 0
        for bit in bit_stream:
            if bit == 0:
                current_run += 1
                max_zero_run = max(max_zero_run, current_run)
            else:
                current_run = 0

        # 전이 횟수
        transitions = sum(1 for i in range(1, len(bit_stream))
                         if bit_stream[i] != bit_stream[i-1])

        return {
            'max_zero_run': max_zero_run,
            'transitions': transitions,
            'total_bits': len(bit_stream),
            'transition_density': transitions / (len(bit_stream) - 1) if len(bit_stream) > 1 else 0
        }


class EightBTenBCoder:
    """
    8B/10B 부호화 구현 (단순화 버전)

    특징:
    - 8비트 데이터를 10비트 코드워드로 매핑
    - Running Disparity 제어로 DC 밸런스 보장
    - 1000BASE-X, PCIe 1/2, USB 3.0, SATA에서 사용
    """

    # 5B/6B 인코딩 테이블 (단순화 - 실제는 더 복잡함)
    # 형식: {입력 5비트: (RD- 코드, RD+ 코드)}
    FIVEB_SIXB = {
        0b00000: (0b100111, 0b011000),  # D0
        0b00001: (0b011101, 0b100010),  # D1
        0b00010: (0b101101, 0b010010),  # D2
        0b00011: (0b110001, 0b110001),  # D3 (neutral)
        0b00100: (0b110101, 0b001010),  # D4
        0b00101: (0b101001, 0b101001),  # D5 (neutral)
        0b00110: (0b011001, 0b011001),  # D6 (neutral)
        0b00111: (0b111000, 0b000111),  # D7
        0b01000: (0b111001, 0b000110),  # D8
        0b01001: (0b100101, 0b100101),  # D9 (neutral)
        0b01010: (0b010101, 0b010101),  # D10 (neutral)
        0b01011: (0b110100, 0b110100),  # D11 (neutral)
        0b01100: (0b001101, 0b001101),  # D12 (neutral)
        0b01101: (0b101100, 0b101100),  # D13 (neutral)
        0b01110: (0b011100, 0b011100),  # D14 (neutral)
        0b01111: (0b010111, 0b101000),  # D15
        0b10000: (0b011011, 0b100100),  # D16
        0b10001: (0b100011, 0b100011),  # D17 (neutral)
        0b10010: (0b010011, 0b010011),  # D18 (neutral)
        0b10011: (0b110010, 0b110010),  # D19 (neutral)
        0b10100: (0b001011, 0b001011),  # D20 (neutral)
        0b10101: (0b101010, 0b101010),  # D21 (neutral)
        0b10110: (0b011010, 0b011010),  # D22 (neutral)
        0b10111: (0b111010, 0b000101),  # D23
        0b11000: (0b110011, 0b001100),  # D24
        0b11001: (0b100110, 0b100110),  # D25 (neutral)
        0b11010: (0b010110, 0b010110),  # D26 (neutral)
        0b11011: (0b110110, 0b001001),  # D27
        0b11100: (0b001110, 0b001110),  # D28 (neutral)
        0b11101: (0b101110, 0b010001),  # D29
        0b11110: (0b011110, 0b100001),  # D30
        0b11111: (0b101011, 0b010100),  # D31
    }

    # 3B/4B 인코딩 테이블
    THREEB_FOURB = {
        0b000: (0b1011, 0b0100),  # D.x.0 (RD-, RD+)
        0b001: (0b1001, 0b1001),  # D.x.1 (neutral)
        0b010: (0b0101, 0b0101),  # D.x.2 (neutral)
        0b011: (0b1100, 0b0011),  # D.x.3
        0b100: (0b1101, 0b0010),  # D.x.4
        0b101: (0b1010, 0b1010),  # D.x.5 (neutral)
        0b110: (0b0110, 0b0110),  # D.x.6 (neutral)
        0b111: (0b1110, 0b0001),  # D.x.7 (or alternate for P7)
    }

    def __init__(self):
        self.rd = RunningDisparity.NEGATIVE  # 초기 상태

    def encode_byte(self, byte: int) -> int:
        """
        8비트 바이트를 10비트 코드워드로 인코딩

        8비트 = HGF EDCBA (3비트 + 5비트)
        10비트 = abcdei fghj (6비트 + 4비트)
        """
        # 하위 5비트와 상위 3비트 분리
        d = byte & 0x1F  # EDCBA
        hgf = (byte >> 5) & 0x07  # HGF

        # 5B/6B 인코딩
        if d not in self.FIVEB_SIXB:
            raise ValueError(f"Invalid 5-bit input: {d:05b}")

        rd_minus_6b, rd_plus_6b = self.FIVEB_SIXB[d]

        # 현재 RD에 따라 선택
        if self.rd == RunningDisparity.NEGATIVE:
            six_bit = rd_minus_6b
        else:
            six_bit = rd_plus_6b

        # 6비트의 DC 밸런스 계산
        ones_6b = bin(six_bit).count('1')
        zeros_6b = 6 - ones_6b

        # RD 업데이트 (6비트 후)
        if ones_6b > zeros_6b:
            self.rd = RunningDisparity.POSITIVE
        elif zeros_6b > ones_6b:
            self.rd = RunningDisparity.NEGATIVE
        # 같으면 유지

        # 3B/4B 인코딩
        if hgf not in self.THREEB_FOURB:
            raise ValueError(f"Invalid 3-bit input: {hgf:03b}")

        rd_minus_4b, rd_plus_4b = self.THREEB_FOURB[hgf]

        if self.rd == RunningDisparity.NEGATIVE:
            four_bit = rd_minus_4b
        else:
            four_bit = rd_plus_4b

        # 10비트 결합 (abcdei fghj)
        ten_bit = (six_bit << 4) | four_bit

        # 최종 RD 업데이트
        ones_total = bin(ten_bit).count('1')
        zeros_total = 10 - ones_total

        if ones_total > zeros_total:
            self.rd = RunningDisparity.POSITIVE
        elif zeros_total > ones_total:
            self.rd = RunningDisparity.NEGATIVE

        return ten_bit

    def encode(self, data: bytes) -> List[int]:
        """바이트 시퀀스 인코딩"""
        self.rd = RunningDisparity.NEGATIVE  # 초기화
        return [self.encode_byte(b) for b in data]

    def calculate_dc_balance(self, codewords: List[int]) -> dict:
        """DC 밸런스 분석"""
        total_ones = 0
        total_zeros = 0

        for cw in codewords:
            ones = bin(cw).count('1')
            zeros = 10 - ones
            total_ones += ones
            total_zeros += zeros

        return {
            'total_ones': total_ones,
            'total_zeros': total_zeros,
            'dc_offset': (total_ones - total_zeros) / (total_ones + total_zeros)
                         if (total_ones + total_zeros) > 0 else 0
        }


def compare_4b5b_8b10b():
    """4B/5B와 8B/10B 비교"""

    print("\n" + "="*80)
    print("Comparison: 4B/5B vs 8B/10B")
    print("="*80)

    # 테스트 데이터
    test_data = bytes([0x00, 0xFF, 0x55, 0xAA, 0x12, 0x34, 0x56, 0x78])

    # 4B/5B
    coder_4b5b = FourBFiveBCoder()
    codewords_4b5b = coder_4b5b.encode(test_data)
    analysis_4b5b = coder_4b5b.analyze_transition_density(codewords_4b5b)

    # 8B/10B
    coder_8b10b = EightBTenBCoder()
    codewords_8b10b = coder_8b10b.encode(test_data)
    analysis_8b10b = coder_8b10b.calculate_dc_balance(codewords_8b10b)

    print(f"\nTest Data: {test_data.hex()}")
    print(f"\n{'Metric':<25} | {'4B/5B':<20} | {'8B/10B':<20}")
    print("-"*70)
    print(f"{'Overhead':<25} | {'25%':<20} | {'25%':<20}")
    print(f"{'Max Zero Run (4B/5B)':<25} | {analysis_4b5b['max_zero_run']:<20} | {'N/A':<20}")
    print(f"{'Transition Density':<25} | {analysis_4b5b['transition_density']:.2%:<20} | {'N/A':<20}")
    print(f"{'DC Offset':<25} | {'Variable':<20} | {analysis_8b10b['dc_offset']:+.4f}")
    print(f"{'DC Balance Guarantee':<25} | {'No':<20} | {'Yes':<20}")

    print("\nConclusion:")
    print("  4B/5B: Simple, good transition density, no DC balance guarantee")
    print("  8B/10B: RD control ensures bounded DC offset")

    print("="*80)


def demonstrate_running_disparity():
    """Running Disparity 동작 시연"""

    print("\n" + "="*70)
    print("8B/10B Running Disparity Demonstration")
    print("="*70)

    coder = EightBTenBCoder()

    # 0x00 (D0.0)을 여러 번 인코딩
    test_byte = 0x00
    print(f"\nEncoding 0x{test_byte:02X} five times:")

    for i in range(5):
        coder.rd = RunningDisparity.NEGATIVE if i == 0 else coder.rd
        prev_rd = coder.rd
        codeword = coder.encode_byte(test_byte)
        new_rd = coder.rd

        ones = bin(codeword).count('1')
        zeros = 10 - ones

        print(f"  Round {i+1}: RD {prev_rd.name:>8} → "
              f"codeword 0x{codeword:03X} ({ones} ones, {zeros} zeros) → "
              f"RD {new_rd.name:>8}")

    print("\nRunning Disparity alternates to maintain DC balance!")

    print("="*70)


# ==================== 실행 ====================
if __name__ == "__main__":
    compare_4b5b_8b10b()
    demonstrate_running_disparity()
