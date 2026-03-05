+++
title = "012. 동기식 전송 - 문자 동기/비트 동기방식 (Character Sync vs Bit Sync)"
description = "동기식 전송의 문자 동기방식(SYN, BSC)과 비트 동기방식(SDLC, HDLC)의 원리, 구조, 장단점 및 실무 적용을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["CharacterSync", "BitSync", "SYN", "BSC", "HDLC", "SDLC", "Flag", "BitStuffing"]
categories = ["studynotes-3_network"]
+++

# 012. 동기식 전송 - 문자 동기/비트 동기방식 (Character Sync vs Bit Sync)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 문자 동기방식은 SYN 문자(0x16)를 사용하여 바이트 단위 경계를 확립하는 BSC(Binary Synchronous Communication) 방식이며, 비트 동기방식은 플래그 패턴(01111110)을 사용하여 비트 단위 경계를 확립하는 HDLC/SDLC 방식입니다.
> 2. **가치**: 문자 동기방식은 구현이 간단하고 8비트 문자 기반 시스템에 적합하지만, 비트 동기방식은 임의 길이의 데이터와 2진 데이터 모두를 효율적으로 전송할 수 있어 현대 통신의 표준이 되었습니다.
> 3. **융합**: 비트 동기방식은 HDLC, PPP, 이더넷 등 현대 네트워크 프로토콜의 기반이 되며, 비트 스터핑 기술은 데이터 투명성(Data Transparency)을 보장하는 핵심 메커니즘입니다.

---

## I. 개요 (Context & Background)

동기식 전송에서 송수신 양단이 연속적인 비트 스트림을 주고받을 때, 수신측은 **어디서부터 어디까지가 하나의 프레임인지**를 구분할 수 있어야 합니다. 이를 **프레임 동기화(Frame Synchronization)**라고 하며, 크게 **문자 동기방식(Character-Oriented Synchronization)**과 **비트 동기방식(Bit-Oriented Synchronization)**으로 나뉩니다.

### 문자 동기방식 (Character-Oriented Synchronization)

**문자 동기방식**은 IBM의 **BSC(Binary Synchronous Communication)** 프로토콜에서 사용된 방식으로, 8비트 **SYN(0x16) 문자**를 두 개 연속으로 전송하여 바이트 경계를 확립합니다. 수신측은 비트 스트림에서 SYN 문자 패턴을 검색하고, 이를 기준으로 이후의 데이터를 바이트 단위로 해석합니다.

- **동기 문자**: SYN (0x16 = 00010110)
- **특징**: 8비트 문자 단위 처리
- **프로토콜**: IBM BSC (Binary Synchronous Communication)
- **한계**: 8비트 정렬 필요, 임의의 2진 데이터 전송 어려움

### 비트 동기방식 (Bit-Oriented Synchronization)

**비트 동기방식**은 **HDLC(High-Level Data Link Control)**, **SDLC(Synchronous Data Link Control)**, **PPP** 등에서 사용되는 방식으로, 특정 비트 패턴인 **플래그(Flag = 01111110)**를 프레임의 시작과 끝에 배치합니다. 비트 스터핑(Bit Stuffing) 기술을 통해 데이터 내에 플래그와 동일한 패턴이 나타나는 것을 방지합니다.

- **플래그 패턴**: 01111110 (0x7E)
- **특징**: 비트 단위 처리, 데이터 투명성 보장
- **프로토콜**: HDLC, SDLC, PPP, LAPB, LAPD, Frame Relay
- **장점**: 임의 길이의 2진 데이터 전송 가능

**💡 비유**: 문자 동기방식과 비트 동기방식을 **'페이지 구분'**에 비유할 수 있습니다.

- **문자 동기방식**은 **책의 페이지 번호**와 같습니다. 각 페이지가 특정 문자(SYN)로 시작하므로, 페이지 번호가 보이면 "여기서부터 새 페이지다"라고 알 수 있습니다. 하지만 모든 페이지가 같은 크기(8비트)여야 합니다.

- **비트 동기방식**은 **책갈피**와 같습니다. 책갈피(플래그)를 꽂아서 읽던 페이지를 표시합니다. 책갈피는 어디에나 꽂을 수 있고, 페이지 크기와 상관없이 정확한 위치를 표시합니다.

**등장 배경 및 발전 과정**:

1. **문자 동기방식의 등장 (1960년대)**: IBM이 메인프레임과 단말기 간 통신을 위해 BSC 프로토콜을 개발했습니다. 당시 대부분의 데이터가 문자(EBCDIC, ASCII) 형태였으므로 문자 기반 동기화가 자연스러웠습니다.

2. **비트 동기방식의 개발 (1970년대)**: IBM이 SDLC(Synchronous Data Link Control)를 개발하고, 이를 기반으로 ISO가 HDLC(High-Level Data Link Control)를 표준화했습니다. 컴퓨터 간 통신에서 2진 데이터(이미지, 실행 파일 등)의 전송 필요성이 증가하면서 문자 독립적인 방식이 요구되었습니다.

3. **현대적 진화**: 오늘날 대부분의 데이터 링크 프로토콜(HDLC, PPP, Frame Relay, 이더넷)은 비트 동기방식을 기반으로 합니다. 이더넷은 프리앰블(Preamble)과 SFD(Start Frame Delimiter)를 사용하는 변형된 방식을 사용합니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 문자 동기방식 | 비트 동기방식 | 내부 동작 |
|---------|------|--------------|--------------|----------|
| **동기 패턴** | SYN / Flag | SYN (0x16) 2개 | Flag (01111110) | 비트 패턴 검색 |
| **위치** | 배치 | 프레임 시작 | 프레임 시작/끝 | 양쪽 감싸기 |
| **데이터 단위** | 정렬 | 8비트 문자 | 비트 스트림 | 가변 길이 |
| **투명성 확보** | 방법 | DLE 문자 스터핑 | 비트 스터핑 | 패턴 회피 |
| **프로토콜** | 대표 | IBM BSC | HDLC, SDLC, PPP | 계층 구조 |
| **오버헤드** | 비용 | 낮음 (SYN 2바이트) | 중간 (Flag 2바이트) | 프레임당 |

### 정교한 구조 다이어그램: 문자 동기 vs 비트 동기

```ascii
================================================================================
[ 문자 동기방식 - BSC 프레임 구조 ]
================================================================================

   SYN   SYN   SOH   Header  STX   Data   ETX   BCC
  (0x16)(0x16)(0x01)  (가변) (0x02) (가변) (0x03) (2B)

    |<--- 동기 확립 --->|<- 제어 ->|<-- 데이터 -->|<- 종료 ->|

   - SYN 2개 연속: 바이트 동기 확립
   - SOH (Start of Header): 헤더 시작
   - STX (Start of Text): 데이터 시작
   - ETX (End of Text): 데이터 종료
   - BCC (Block Check Character): 오류 검출

   한계:
   1. 데이터 내에 STX, ETX 등 제어 문자가 있으면 문제 발생
   2. 해결: DLE(Data Link Escape) 문자 스터핑 사용
      예) DLE STX -> 실제 STX가 아닌 데이터로 처리
      예) DLE DLE -> 실제 DLE 문자


================================================================================
[ 비트 동기방식 - HDLC 프레임 구조 ]
================================================================================

  Flag   Address  Control  Information   FCS    Flag
 01111110  8bit    8bit     (가변)      16bit  01111110
    |                                  |
    +---------- 프레임 경계 ------------+

   - Flag (01111110): 프레임 시작/종료 표시
   - Address: 대상 주소
   - Control: 프레임 유형 및 시퀀스 번호
   - Information: 사용자 데이터 (가변 길이)
   - FCS: CRC-16 오류 검출

   데이터 투명성 확보 (비트 스터핑):
   - 송신측: 1이 5개 연속되면 0을 삽입
   - 수신측: 1이 5개 연속 후 0이면 제거


================================================================================
[ 비트 스터핑 (Bit Stuffing) 상세 동작 ]
================================================================================

원본 데이터:    0  1  1  1  1  1  1  0  1  0  ...
                    |<-- 1이 6개 연속 -->|
                    |  Flag와 혼동 가능! |

송신측 스터핑:  0  1  1  1  1  1  0  1  0  1  0  ...
                          ^     ^
                          |     +-- 원래 0
                          +-- 삽입된 0 (스터핑)

수신측 디스터핑: 0  1  1  1  1  1  1  0  1  0  ...
                          ^     ^
                          |     +-- 원래 0 유지
                          +-- 삽입된 0 제거

규칙:
- 송신: 1이 5개 연속되면 무조건 0을 삽입
- 수신: 1이 5개 연속 후 0이면 제거
- 수신: 1이 6개 연속 후 0이면 Flag로 인식


================================================================================
[ 문자 스터핑 (Character Stuffing) - BSC의 DLE 사용 ]
================================================================================

원본 데이터:    ...  DLE  STX  Data  ETX  ...

문제: STX, ETX가 제어 문자로 오인됨

송신측 스터핑:  ...  DLE  DLE  DLE  STX  Data  DLE  ETX  ...
                          ^          ^           ^
                          |          |           +-- DLE 추가
                          +-- DLE를 데이터로 처리

수신측 디스터핑: ...  DLE  STX  Data  ETX  ...
                          ^
                          +-- DLE 제거 후 원래 데이터 복원

규칙:
- 송신: 데이터 내의 DLE를 DLE DLE로 치환
- 수신: DLE DLE를 DLE로 복원
```

### 심층 동작 원리: 5단계 동기화 프로세스

#### 문자 동기방식 (BSC) 동작 과정

1. **SYN 문자 검색**:
   - 수신측은 비트 스트림에서 0x16 (00010110) 패턴을 실시간으로 검색합니다.
   - 8비트 슬라이딩 윈도우를 사용하여 매 비트마다 새로운 8비트를 검사합니다.

2. **이중 SYN 확인**:
   - 첫 번째 SYN이 검출되면, 바로 다음 8비트가 SYN인지 확인합니다.
   - 두 개의 SYN이 연속으로 검출되면 바이트 동기가 확립된 것으로 간주합니다.

3. **문자 경계 확정**:
   - 이 시점부터 수신측은 8비트 단위로 데이터를 끊어서 해석합니다.
   - SOH, STX, ETX 등의 제어 문자를 인식하여 프레임 구조를 파악합니다.

4. **DLE 스터핑 처리**:
   - 데이터 내에 DLE(0x10)가 나타나면 다음 문자를 제어 문자가 아닌 데이터로 처리합니다.
   - DLE DLE가 나타나면 하나의 DLE 데이터로 복원합니다.

5. **프레임 종료**:
   - ETX(0x03) 또는 ETB(0x17)가 검출되면 프레임 종료로 간주합니다.
   - BCC(Block Check Character)를 확인하여 오류를 검출합니다.

#### 비트 동기방식 (HDLC) 동작 과정

1. **플래그 검색**:
   - 수신측은 비트 스트림에서 01111110 패턴을 검색합니다.
   - 8비트 시프트 레지스터와 패턴 매칭 회로를 사용합니다.

2. **비트 스터핑 디코딩**:
   - 플래그 이후의 비트 스트림에 대해 디스터핑을 수행합니다.
   - 1이 5개 연속된 후 0이 나타나면 그 0을 제거합니다.

3. **필드 경계 인식**:
   - 디스터핑된 비트 스트림에서 Address (8비트), Control (8비트)를 순차적으로 추출합니다.
   - Information 필드는 가변 길이이므로 종료 플래그까지를 데이터로 간주합니다.

4. **FCS 검증**:
   - FCS(Frame Check Sequence)를 CRC-16 알고리즘으로 검증합니다.
   - 오류가 없으면 데이터를 상위 계층으로 전달합니다.

5. **플래그로 프레임 종료**:
   - 01111110 패턴이 다시 나타나면 프레임 종료로 간주합니다.
   - 연속된 두 플래그 사이에 최소 하나의 0이 있어야 합니다.

### 핵심 코드: 비트 스터핑 구현

```python
from typing import List, Tuple

class BitStuffing:
    """
    HDLC 비트 스터핑/디스터핑 구현
    """
    FLAG = [0, 1, 1, 1, 1, 1, 1, 0]  # 01111110

    @staticmethod
    def stuff_bits(data_bits: List[int]) -> List[int]:
        """
        비트 스터핑 수행
        규칙: 1이 5개 연속되면 0을 삽입
        """
        stuffed = []
        consecutive_ones = 0

        for bit in data_bits:
            stuffed.append(bit)

            if bit == 1:
                consecutive_ones += 1
                # 1이 5개 연속되면 0 삽입
                if consecutive_ones == 5:
                    stuffed.append(0)
                    consecutive_ones = 0
            else:
                consecutive_ones = 0

        return stuffed

    @staticmethod
    def destuff_bits(stuffed_bits: List[int]) -> Tuple[List[int], bool]:
        """
        비트 디스터핑 수행
        규칙: 1이 5개 연속 후 0이면 그 0을 제거
        반환: (디스터핑된 비트, 플래그 감지 여부)
        """
        destuffed = []
        consecutive_ones = 0
        i = 0

        while i < len(stuffed_bits):
            bit = stuffed_bits[i]

            if consecutive_ones == 5:
                # 1이 5개 연속된 후
                if bit == 0:
                    # 0이면 스터핑된 비트 - 제거
                    consecutive_ones = 0
                    i += 1
                    continue
                elif bit == 1:
                    # 1이면 6개 연속 - 플래그의 일부
                    # 실제로는 플래그 검출 로직에서 처리
                    pass

            destuffed.append(bit)

            if bit == 1:
                consecutive_ones += 1
            else:
                consecutive_ones = 0

            i += 1

        return destuffed, False

class HDLCFramer:
    """
    HDLC 프레임 생성 및 파싱
    """
    def __init__(self):
        self.stuffer = BitStuffing()

    def create_frame(self, address: int, control: int, data: bytes) -> List[int]:
        """
        HDLC 프레임 생성
        """
        frame_bits = []

        # 1. Opening Flag
        frame_bits.extend(BitStuffing.FLAG)

        # 2. Address (8 bits)
        addr_bits = self._byte_to_bits(address)
        frame_bits.extend(self.stuffer.stuff_bits(addr_bits))

        # 3. Control (8 bits)
        ctrl_bits = self._byte_to_bits(control)
        frame_bits.extend(self.stuffer.stuff_bits(ctrl_bits))

        # 4. Information (variable)
        for byte in data:
            data_bits = self._byte_to_bits(byte)
            frame_bits.extend(self.stuffer.stuff_bits(data_bits))

        # 5. FCS (simplified - 실제로는 CRC-16)
        fcs = self._calculate_fcs(address, control, data)
        fcs_bits = self._bytes_to_bits(fcs)
        frame_bits.extend(self.stuffer.stuff_bits(fcs_bits))

        # 6. Closing Flag
        frame_bits.extend(BitStuffing.FLAG)

        return frame_bits

    def parse_frame(self, frame_bits: List[int]) -> dict:
        """
        HDLC 프레임 파싱
        """
        # 플래그 제거
        if frame_bits[:8] != BitStuffing.FLAG or frame_bits[-8:] != BitStuffing.FLAG:
            raise ValueError("Invalid frame: Flag not found")

        # 플래그 사이의 비트 추출
        payload_bits = frame_bits[8:-8]

        # 디스터핑 (실제로는 스트림 처리)
        destuffed, _ = BitStuffing.destuff_bits(payload_bits)

        # 필드 추출
        address = self._bits_to_byte(destuffed[0:8])
        control = self._bits_to_byte(destuffed[8:16])

        # FCS 제외한 데이터 (마지막 16비트 = FCS)
        data_bits = destuffed[16:-16]
        data = bytes([self._bits_to_byte(data_bits[i:i+8])
                     for i in range(0, len(data_bits), 8)])

        received_fcs = self._bits_to_bytes(destuffed[-16:])

        return {
            'address': address,
            'control': control,
            'data': data,
            'fcs': received_fcs
        }

    @staticmethod
    def _byte_to_bits(byte: int) -> List[int]:
        return [(byte >> (7 - i)) & 1 for i in range(8)]

    @staticmethod
    def _bytes_to_bits(data: bytes) -> List[int]:
        bits = []
        for byte in data:
            bits.extend(HDLCFramer._byte_to_bits(byte))
        return bits

    @staticmethod
    def _bits_to_byte(bits: List[int]) -> int:
        result = 0
        for bit in bits:
            result = (result << 1) | bit
        return result

    @staticmethod
    def _bits_to_bytes(bits: List[int]) -> bytes:
        return bytes([HDLCFramer._bits_to_byte(bits[i:i+8])
                     for i in range(0, len(bits), 8)])

    @staticmethod
    def _calculate_fcs(address: int, control: int, data: bytes) -> bytes:
        """간소화된 FCS 계산 (실제로는 CRC-16-CCITT)"""
        # 실제 구현에서는 CRC-16-CCITT 사용
        crc = 0xFFFF
        for byte in [address, control] + list(data):
            crc ^= byte
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc.to_bytes(2, 'little')

class BSCCharacterSync:
    """
    BSC 문자 동기방식 구현
    """
    SYN = 0x16  # Synchronous Idle
    SOH = 0x01  # Start of Header
    STX = 0x02  # Start of Text
    ETX = 0x03  # End of Text
    EOT = 0x04  # End of Transmission
    DLE = 0x10  # Data Link Escape

    def __init__(self):
        self.sync_established = False

    def establish_sync(self, bit_stream: List[int]) -> bool:
        """
        SYN 문자 2개로 동기 확립
        """
        syn_bits = self._byte_to_bits(self.SYN)
        double_syn = syn_bits + syn_bits  # 16비트

        # 비트 스트림에서 SYN SYN 패턴 검색
        for i in range(len(bit_stream) - 15):
            if bit_stream[i:i+16] == double_syn:
                self.sync_established = True
                return True

        return False

    def create_frame(self, header: bytes, data: bytes) -> bytes:
        """
        BSC 프레임 생성
        """
        frame = bytearray()

        # SYN SYN
        frame.append(self.SYN)
        frame.append(self.SYN)

        # SOH + Header
        if header:
            frame.append(self.SOH)
            frame.extend(self._stuff_characters(header))

        # STX + Data + ETX
        frame.append(self.STX)
        frame.extend(self._stuff_characters(data))
        frame.append(self.ETX)

        # BCC (Block Check Character) - 간소화
        bcc = self._calculate_bcc(bytes(frame[2:]))  # SYN 제외
        frame.extend(bcc)

        return bytes(frame)

    def _stuff_characters(self, data: bytes) -> bytes:
        """
        DLE 문자 스터핑
        데이터 내의 DLE를 DLE DLE로 치환
        """
        stuffed = bytearray()
        for byte in data:
            if byte == self.DLE:
                stuffed.append(self.DLE)
                stuffed.append(self.DLE)
            else:
                stuffed.append(byte)
        return bytes(stuffed)

    def _destuff_characters(self, data: bytes) -> bytes:
        """
        DLE 디스터핑
        DLE DLE를 DLE로 복원
        """
        destuffed = bytearray()
        i = 0
        while i < len(data):
            if data[i] == self.DLE and i + 1 < len(data):
                if data[i + 1] == self.DLE:
                    destuffed.append(self.DLE)
                    i += 2
                    continue
            destuffed.append(data[i])
            i += 1
        return bytes(destuffed)

    @staticmethod
    def _byte_to_bits(byte: int) -> List[int]:
        return [(byte >> (7 - i)) & 1 for i in range(8)]

    @staticmethod
    def _calculate_bcc(data: bytes) -> bytes:
        """LRC (Longitudinal Redundancy Check) 계산"""
        lrc = 0
        for byte in data:
            lrc ^= byte
        return bytes([lrc])

# 실무 사용 예시
if __name__ == "__main__":
    # HDLC 비트 동기방식
    hdlc = HDLCFramer()
    frame = hdlc.create_frame(
        address=0x01,
        control=0x00,  # I-Frame
        data=b"Hello, HDLC!"
    )
    print(f"HDLC 프레임 길이: {len(frame)} 비트")

    parsed = hdlc.parse_frame(frame)
    print(f"주소: {parsed['address']:02X}")
    print(f"데이터: {parsed['data']}")

    # BSC 문자 동기방식
    bsc = BSCCharacterSync()
    bsc_frame = bsc.create_frame(
        header=b"DEST01",
        data=b"Hello, BSC!"
    )
    print(f"\nBSC 프레임 길이: {len(bsc_frame)} 바이트")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 문자 동기 vs 비트 동기

| 비교 관점 | 문자 동기방식 (BSC) | 비트 동기방식 (HDLC) |
|----------|---------------------|---------------------|
| **동기 단위** | 8비트 문자 | 비트 |
| **동기 패턴** | SYN (0x16) 2개 | Flag (01111110) |
| **투명성 확보** | DLE 문자 스터핑 | 비트 스터핑 |
| **데이터 제약** | 8비트 문자만 | 임의 2진 데이터 |
| **오버헤드** | 낮음 (SYN 2바이트) | 중간 (스터핑 오버헤드) |
| **프로토콜** | IBM BSC | HDLC, PPP, Frame Relay |
| **현대적 사용** | 레거시 시스템 | 광범위하게 사용 |
| **구현 복잡도** | 낮음 | 중간 |

### 과목 융합 관점 분석

1. **프로그래밍 언어와의 융합**:
   - **비트 조작**: C 언어의 비트 연산자(<<, >>, &, |, ^)가 비트 스터핑 구현에 필수적입니다.
   - **상태 머신**: 프레임 파싱은 유한 상태 머신(FSM)으로 모델링됩니다.

2. **운영체제와의 융합**:
   - **PPP 드라이버**: 리눅스 커널의 PPP 드라이버는 HDLC 프레이밍을 소프트웨어로 구현합니다.
   - **직렬 드라이버**: UART 드라이버는 하드웨어적 비트 동기를 소프트웨어적 프레임 동기와 결합합니다.

3. **보안과의 융합**:
   - **PPP over SONET**: 비트 동기 기반 PPP 위에 IPsec을 구현하여 보안 터널을 생성합니다.
   - **프레임 위조 방지**: Flag 패턴과 FCS를 통한 프레임 무결성 검증이 1차 방어선입니다.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 레거시 시스템 연동

**문제 상황**: 1980년대 구축된 은행 메인프레임이 BSC 프로토콜을 사용하는데, 최신 서버와 연동해야 합니다.

**기술사의 전략적 의사결정**:

1. **분석**: 레거시 메인프레임은 문자 동기방식(BSC)만 지원하며, 프로토콜 변환이 불가피합니다.

2. **해결 방안**:
   - **프로토콜 게이트웨이** 구축: BSC ↔ HDLC/PPP 변환
   - TCP/IP 래퍼: BSC 데이터를 TCP 페이로드로 캡슐화

3. **구현**: DLE 스터핑과 비트 스터핑 간 변환 로직 구현

### 도입 시 고려사항 체크리스트

| 항목 | 문자 동기방식 | 비트 동기방식 |
|------|--------------|--------------|
| **데이터 타입** | 텍스트 위주 | 2진 데이터 포함 |
| **레거시 연동** | IBM 메인프레임 | 현대적 네트워크 |
| **대역폭 효율** | 중간 | 높음 |
| **구현 난이도** | 낮음 | 중간 |

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - 2진 데이터에 문자 동기 사용**: 이미지, 실행 파일 등의 2진 데이터를 BSC로 전송하면 DLE 스터핑 오버헤드가 과도해집니다.

- **안티패턴 2 - 비트 스터핑 없이 HDLC 사용**: 플래그 패턴이 데이터에 포함되면 프레임 경계가 잘못 인식됩니다.

---

## V. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 | 비트 동기방식 |
|------|--------------|
| **데이터 투명성** | 100% 보장 |
| **전송 효율** | 95%+ |
| **프로토콜 호환** | HDLC, PPP, Frame Relay |

### 미래 전망

- **이더넷**: 프리앰블 + SFD 방식으로 진화
- **광통신**: 8b/10b, 64b/66b 인코딩으로 클럭 복원 통합

### 참고 표준

| 표준 | 기관 | 내용 |
|------|------|------|
| **ISO 3309** | ISO | HDLC 프레임 구조 |
| **IBM GA27-3004** | IBM | BSC 프로토콜 사양 |
| **RFC 1662** | IETF | PPP in HDLC Framing |

---

## 관련 개념 맵 (Knowledge Graph)
- [동기식/비동기식 전송](./10_synchronous_asynchronous_transmission.md) - 전송 방식 비교
- [HDLC 프로토콜](../4_switching/hdlc_protocol.md) - 비트 동기 기반 프로토콜
- [오류 검출 기법](./error_detection_parity_crc.md) - CRC 기반 FCS
- [PPP 프로토콜](../2_transport/ppp_protocol.md) - HDLC 프레이밍 활용

---

## 어린이를 위한 3줄 비유 설명
1. **문자 동기방식**은 **'줄넘기의 박자'**와 같아요. "하나, 둘, 셋!" 같은 구호(SYN 문자)에 맞춰 8명씩 차례로 넘습니다.
2. **비트 동기방식**은 **'책갈피'**와 같아요. 책갈피(플래그)를 꽂아서 어디까지 읽었는지 표시하면, 페이지 크기와 상관없이 정확한 위치를 알 수 있어요.
3. 둘의 차이는 **'정해진 간격' vs '표시판'**과 같아요. 줄넘기는 정해진 박자가 필요하지만, 책갈피는 아무 곳에나 꽂을 수 있답니다!
