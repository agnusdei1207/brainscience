+++
title = "011. 비동기식 전송 - 시작/정지 비트 (Start/Stop Bit)"
description = "비동기식 전송의 핵심 요소인 시작 비트와 정지 비트의 원리, 타이밍 복원 메커니즘 및 프레이밍 에러 분석을 심도 있게 다룹니다."
date = "2026-03-05"
[taxonomies]
tags = ["StartBit", "StopBit", "AsyncTransmission", "FramingError", "UART", "RS-232", "BitSynchronization"]
categories = ["studynotes-3_network"]
+++

# 011. 비동기식 전송 - 시작/정지 비트 (Start/Stop Bit)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시작 비트는 Low(0) 신호로 수신측에 문자 전송 시작을 알리는 트리거 역할을 하며, 정지 비트는 High(1) 신호로 문자 종료를 알리고 수신측이 다음 문자를 준비할 시간을 제공합니다.
> 2. **가치**: 시작 비트의 하강 에지(Falling Edge)를 기준으로 수신측이 타이밍을 복원함으로써, 별도의 클럭 신호 없이도 문자 단위 동기화를 달성하여 하드웨어 복잡도를 획기적으로 줄입니다.
> 3. **융합**: 시작/정지 비트 방식은 UART, RS-232C, USB 저속 모드 등 다양한 시리얼 통신의 기반이 되며, 현대의 고속 통신에서도 패킷 시작/종료 구분의 근본적 개념으로 계승됩니다.

---

## I. 개요 (Context & Background)

비동기식 전송(Asynchronous Transmission)에서 가장 핵심적인 요소는 **시작 비트(Start Bit)**와 **정지 비트(Stop Bit)**입니다. 이 두 비트는 개별 문자(보통 8비트)를 프레임(Frame)으로 감싸서, 수신측이 언제 데이터가 시작되고 끝나는지를 인식할 수 있게 합니다.

**시작 비트(Start Bit)**는 항상 논리 Low(0)로 전송됩니다. 전송 매체가 유휴(Idle) 상태에서 High(1)를 유지하다가 Low로 떨어지는 순간, 수신측은 이를 문자의 시작 신호로 인식합니다. 이 **High→Low 하강 에지(Falling Edge)**가 바로 타이밍 동기화의 기준점이 됩니다.

**정지 비트(Stop Bit)**는 항상 논리 High(1)로 전송됩니다. 문자의 모든 데이터 비트가 전송된 후 High 상태를 유지함으로써: (1) 수신측에 문자 종료를 알리고, (2) 수신측이 다음 문자를 처리할 시간을 제공하며, (3) 프레이밍 에러(Framing Error)를 검출할 수 있게 합니다.

**💡 비유**: 시작/정지 비트를 **'엘리베이터 문'**에 비유할 수 있습니다.
- **시작 비트**는 엘리베이터 문이 **열리는 순간**입니다. 문이 열린다는 신호(Low)를 받으면 승객(수신측)은 사람(데이터)이 타고내리는 것을 준비합니다.
- **데이터 비트**는 승객이 **실제로 타고내리는 시간**입니다.
- **정지 비트**는 엘리베이터 문이 **닫히는 순간**입니다. 문이 닫히면(High) 이번 승객의 탑승이 끝났음을 알리고, 다음 승객을 위한 준비 시간을 갖습니다.

**등장 배경 및 발전 과정**:

1. **기계식 텔레타이프의 필요성 (1900년대 초)**: 모스 부호에서 인간이 타이밍을 조절하던 것과 달리, 기계적 텔레타이프는 자동으로 타이밍을 인식할 방법이 필요했습니다.

2. **Start-Stop 방식의 고안**: 1908년 E. E. Kleinschmidt가 시작/정지 비트 개념을 도입한 텔레타이프를 발명했습니다. 이는 회전하는 캠(Cam)과 솔레노이드를 이용해 기계적으로 구현되었습니다.

3. **RS-232C 표준화 (1960년대)**: EIA(Electronic Industries Alliance)가 시작/정지 비트를 포함한 비동기식 직렬 통신 표준을 제정했습니다.

4. **UART의 보편화 (1970년대~현재)**: 단일 집적회로(IC)로 시작/정지 비트 생성 및 검출 기능을 구현한 UART(Universal Asynchronous Receiver-Transmitter)가 모든 마이크로컨트롤러에 내장되어 산업 표준이 되었습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 상세 역할 | 전기적 상태 | 지속 시간 | 내부 동작 메커니즘 | 관련 파라미터 |
|---------|----------|------------|----------|-------------------|--------------|
| **Idle State** | 대기 상태 | High (Mark) | 무제한 | 송신 버퍼 비어있음 | - |
| **Start Bit** | 전송 시작 트리거 | Low (Space) | 1 비트 시간 | 타이머 시작, 샘플링 클럭 리셋 | 항상 1비트 |
| **Data Bit 0** | 최하위 비트 | Low/High | 1 비트 시간 | LSB First 전송 | 5~8 비트 중 하나 |
| **Data Bit 1~7** | 데이터 비트 | Low/High | 각 1 비트 | 순차적 비트 전송 | 데이터 길이 설정 |
| **Parity Bit** | 오류 검출 (선택) | Low/High | 1 비트 | XOR 연산으로 계산 | Even/Odd/None |
| **Stop Bit** | 전송 종료 및 휴지 | High (Mark) | 1~2 비트 | 타이머 정지, 버퍼 갱신 | 1, 1.5, 2 비트 |
| **Gap/Idle** | 다음 문자 대기 | High (Mark) | 가변 | 송신 버퍼 폴링 | 최소 0 비트 |

### 정교한 구조 다이어그램: 시작/정지 비트 타이밍

```ascii
================================================================================
[ 비동기식 전송 프레임 구조 - 8N1 (8 Data, No Parity, 1 Stop) ]
================================================================================

         Start  D0   D1   D2   D3   D4   D5   D6   D7   Stop  Idle
          |     |    |    |    |    |    |    |    |    |     |
Timeline: |_____|____|____|____|____|____|____|____|____|-----|_____
          |  0  | D0 | D1 | D2 | D3 | D4 | D5 | D6 | D7 |  1  |  1
          |     |    |    |    |    |    |    |    |    |     |
          +--^--+----+----+----+----+----+----+----+----+--^--+
             |                                      |
        Falling Edge                          Rising Edge
        (타이밍 시작)                         (문자 종료)


================================================================================
[ 수신측 샘플링 타이밍 - 16x 오버샘플링 ]
================================================================================

비트 클럭 (Baud Rate):  ____----____----____----____----____----____
                        Start    D0      D1      D2      D3     ...

16x 오버샘플링 클럭:    |'|'|'|'|'|'|'|'|'|'|'|'|'|'|'|'|
                        ^   ^   ^   ^   ^   ^   ^   ^   ^
                        |   |   |   |   |   |   |   |   |
                        |   |   |   |   |   |   |   |   +-- Stop Bit 샘플
                        |   |   |   |   |   |   |   +-- D7 샘플 (중앙)
                        |   |   |   |   |   |   +-- D6 샘플 (중앙)
                        |   |   |   |   |   +-- ... (계속)
                        |   |   |   |   +-- D1 샘플 (중앙)
                        |   |   |   +-- D0 샘플 (중앙)
                        |   |   +-- 1.5 비트 시간 경과 (Start Bit 중앙)
                        |   +-- 카운터 시작
                        +-- Start Bit 하강 에지 감지


================================================================================
[ 정지 비트 변형 - 1, 1.5, 2 Stop Bits ]
================================================================================

1 Stop Bit:      Start D0...D7 Stop|Start ...
                       |<--1T-->|

1.5 Stop Bits:   Start D0...D7 Stop  |Start ...
                       |<---1.5T--->|

2 Stop Bits:     Start D0...D7 Stop  Stop|Start ...
                       |<-----2T----->|

참고: Stop Bit는 항상 High(1) 상태 유지
      Stop Bit 시간 동안 수신측은 다음 Start Bit 감지 준비


================================================================================
[ 프레이밍 에러 (Framing Error) 발생 시나리오 ]
================================================================================

정상 수신:
Idle(1) -> Start(0) -> D0-D7 -> Stop(1) -> Idle(1)
                                   ^
                                   +-- Stop Bit = 1 확인 OK

프레이밍 에러:
Idle(1) -> Start(0) -> D0-D7 -> Stop(0) -> ... (에러!)
                                   ^
                                   +-- Stop Bit != 1 -> Framing Error!

원인:
1. 클럭 주파수 불일치 (송/수신측)
2. 노이즈로 인한 비트 왜곡
3. 케이블 길이 초과로 인한 신호 감쇠
4. 잘못된 설정 (Data Bits, Stop Bits 불일치)
```

### 심층 동작 원리: 5단계 타이밍 복원 프로세스

1. **Idle 상태 모니터링**:
   - 수신측은 전송 라인을 지속적으로 모니터링하며 High(1) 상태를 유지합니다.
   - 16x 오버샘플링을 사용하는 경우, 16개의 클럭 주기마다 입력을 샘플링합니다.

2. **Start Bit 하강 에지 감지**:
   - High→Low 전이가 감지되면, 수신측은 이를 Start Bit로 인식합니다.
   - 내부 카운터를 0으로 리셋하고, 16x 클럭 카운팅을 시작합니다.

3. **Start Bit 유효성 검사**:
   - 카운터가 8(또는 24)에 도달하면 Start Bit의 중앙을 샘플링합니다.
   - 여전히 Low(0)이면 정상 Start Bit로 확정하고, High(1)이면 노이즈로 간주하고 무시합니다.

4. **데이터 비트 샘플링**:
   - 각 데이터 비트의 중앙(카운터 16, 32, 48, ...)에서 샘플링을 수행합니다.
   - 샘플링된 비트는 시프트 레지스터에 순차적으로 저장됩니다.
   - LSB(Least Significant Bit)부터 수신되므로 적절히 조합합니다.

5. **Stop Bit 확인 및 프레이밍 에러 검출**:
   - Stop Bit 위치(마지막 데이터 비트 + 16 클럭)에서 샘플링합니다.
   - High(1)이면 정상 종료, Low(0)이면 **Framing Error**를 발생시킵니다.
   - 수신된 바이트는 버퍼에 저장되고 CPU에 인터럽트를 발생시킵니다.

### 핵심 수식: 클럭 허용 오차 계산

```
최대 허용 클럭 오차 = ±(0.5 / N) × 100%

여기서 N = 총 프레임 비트 수 (Start + Data + Parity + Stop)

예시: 8N1 설정 (N = 10비트)
최대 허용 오차 = ±(0.5 / 10) × 100% = ±5%

실제 안전 마진 적용: ±2~3% 권장
```

### 핵심 코드: Start/Stop Bit 생성 및 검출

```python
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum

class BitState(Enum):
    HIGH = 1   # Mark, Idle
    LOW = 0    # Space, Start

@dataclass
class UARTFrame:
    """비동기식 전송 프레임 구조"""
    start_bit: BitState
    data_bits: List[BitState]
    parity_bit: BitState = BitState.HIGH  # 선택적
    stop_bits: List[BitState] = None      # 1~2개

    def __post_init__(self):
        if self.stop_bits is None:
            self.stop_bits = [BitState.HIGH]

class StartStopBitAnalyzer:
    """
    시작/정지 비트 분석 및 타이밍 복원 시뮬레이터
    """
    def __init__(self, data_bits: int = 8, stop_bit_count: int = 1, parity: str = 'none'):
        self.data_bits = data_bits
        self.stop_bit_count = stop_bit_count
        self.parity = parity  # 'none', 'even', 'odd'

    def create_frame(self, byte_data: int) -> List[BitState]:
        """바이트 데이터를 프레임으로 변환"""
        frame = []

        # 1. Start Bit (항상 LOW)
        frame.append(BitState.LOW)

        # 2. Data Bits (LSB First)
        data_bits_list = []
        for i in range(self.data_bits):
            bit = (byte_data >> i) & 1
            data_bits_list.append(BitState.HIGH if bit else BitState.LOW)
        frame.extend(data_bits_list)

        # 3. Parity Bit (선택적)
        if self.parity != 'none':
            ones_count = bin(byte_data).count('1')
            if self.parity == 'even':
                parity_bit = BitState.HIGH if ones_count % 2 == 0 else BitState.LOW
            else:  # odd
                parity_bit = BitState.LOW if ones_count % 2 == 0 else BitState.HIGH
            frame.append(parity_bit)

        # 4. Stop Bits (항상 HIGH)
        for _ in range(self.stop_bit_count):
            frame.append(BitState.HIGH)

        return frame

    def detect_framing_error(self, frame: List[BitState]) -> Tuple[bool, str]:
        """
        프레이밍 에러 검출
        반환: (에러 여부, 에러 메시지)
        """
        # Stop Bit 위치 계산
        frame_length = 1 + self.data_bits  # Start + Data
        if self.parity != 'none':
            frame_length += 1

        # Stop Bit 확인
        for i in range(self.stop_bit_count):
            stop_pos = frame_length + i
            if stop_pos >= len(frame):
                return True, f"Stop Bit {i+1} 누락"

            if frame[stop_pos] != BitState.HIGH:
                return True, f"Stop Bit {i+1}가 HIGH가 아님 (Framing Error)"

        return False, "정상"

    def decode_frame(self, frame: List[BitState]) -> Tuple[int, bool, str]:
        """
        프레임에서 데이터 복원
        반환: (복원된 바이트, 에러 여부, 메시지)
        """
        # Start Bit 확인
        if frame[0] != BitState.LOW:
            return 0, True, "Start Bit가 LOW가 아님"

        # Data Bits 추출
        data_start = 1
        data_end = data_start + self.data_bits
        data_bits_list = frame[data_start:data_end]

        # LSB First로 조합
        byte_data = 0
        for i, bit in enumerate(data_bits_list):
            if bit == BitState.HIGH:
                byte_data |= (1 << i)

        # Parity 검사 (선택적)
        parity_error = False
        if self.parity != 'none':
            parity_pos = data_end
            if parity_pos < len(frame):
                received_parity = frame[parity_pos]
                ones_count = bin(byte_data).count('1')

                if self.parity == 'even':
                    expected = BitState.HIGH if ones_count % 2 == 0 else BitState.LOW
                else:
                    expected = BitState.LOW if ones_count % 2 == 0 else BitState.HIGH

                if received_parity != expected:
                    parity_error = True

        # Framing Error 검사
        framing_error, msg = self.detect_framing_error(frame)

        if framing_error:
            return byte_data, True, msg
        elif parity_error:
            return byte_data, True, "Parity Error"
        else:
            return byte_data, False, "정상"

class ClockRecoverySimulator:
    """
    클럭 복원 및 샘플링 타이밍 시뮬레이터
    """
    def __init__(self, baud_rate: int = 9600, oversampling: int = 16):
        self.baud_rate = baud_rate
        self.oversampling = oversampling
        self.bit_time = 1.0 / baud_rate
        self.sample_time = self.bit_time / oversampling

    def simulate_reception(self, signal: List[float], start_pos: int) -> List[int]:
        """
        Start Bit 위치에서 시작하여 16x 오버샘플링으로 비트 복원
        signal: 아날로그 신호 레벨 리스트 (0.0 ~ 1.0)
        """
        recovered_bits = []
        current_pos = start_pos

        # Start Bit 중앙 샘플링 (1.5 비트 시간 후)
        start_center = start_pos + int(1.5 * self.oversampling)
        if start_center < len(signal):
            start_sample = 1 if signal[start_center] > 0.5 else 0
            if start_sample != 0:
                print("경고: Start Bit 중앙이 LOW가 아님")

        # 각 비트의 중앙에서 샘플링
        for bit_num in range(10):  # 8 data + 1 parity + 1 stop (예시)
            bit_center = start_pos + int((1.5 + bit_num) * self.oversampling)
            if bit_center < len(signal):
                bit_value = 1 if signal[bit_center] > 0.5 else 0
                recovered_bits.append(bit_value)

        return recovered_bits

    def calculate_timing_tolerance(self, frame_bits: int) -> float:
        """
        클럭 허용 오차 계산
        """
        # 마지막 비트(Stop Bit)에서 샘플링 오차가 0.5비트를 넘지 않아야 함
        max_drift_per_bit = 0.5 / frame_bits
        return max_drift_per_bit * 100  # 퍼센트로 변환

# 실무 사용 예시
if __name__ == "__main__":
    # 프레임 분석기 생성 (8N1 설정)
    analyzer = StartStopBitAnalyzer(data_bits=8, stop_bit_count=1, parity='none')

    # 'A' (0x41 = 01000001) 문자 프레임 생성
    char_a = ord('A')
    frame = analyzer.create_frame(char_a)

    print(f"문자 'A' (0x{char_a:02X}) 프레임:")
    print(f"  Start: {frame[0].name}")
    print(f"  Data:  {[b.name for b in frame[1:9]]}")
    print(f"  Stop:  {frame[9].name}")

    # 프레임 디코딩
    decoded, error, msg = analyzer.decode_frame(frame)
    print(f"\n복원된 문자: '{chr(decoded)}' (0x{decoded:02X})")
    print(f"에러 여부: {error}, 메시지: {msg}")

    # 클럭 허용 오차 계산
    simulator = ClockRecoverySimulator(baud_rate=9600)
    tolerance = simulator.calculate_timing_tolerance(10)  # 10비트 프레임
    print(f"\n클럭 허용 오차: ±{tolerance:.2f}%")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Stop Bit 설정별 특성

| Stop Bits | 지속 시간 | 적용 분야 | 장점 | 단점 |
|-----------|----------|----------|------|------|
| **1 bit** | 1 T (비트 시간) | 일반적인 PC 통신 | 효율적 (80%) | 처리 시간 부족 가능 |
| **1.5 bits** | 1.5 T | 기계식 텔레타이프 | 기계적 여유 | 현대적 사용 드묾 |
| **2 bits** | 2 T | 노이즈 환경, 구형 장비 | 안전 마진 큼 | 효율 저하 (72.7%) |

### Framing Error 원인 분석

| 원인 | 발생 메커니즘 | 증상 | 해결 방안 |
|------|--------------|------|----------|
| **클럭 불일치** | 송수신측 보 레이트 차이 | 누적 오차로 Stop Bit 위치 어긋남 | 정밀 크리스털 오실레이터 사용 |
| **노이즈** | 외부 전자기 간섭 | 비트 왜곡, False Start | 차폐 케이블, 트위스티드 페어 |
| **케이블 길이** | 신호 감쇠 및 지연 | 신호 레벨 저하 | 리피터 사용, 케이블 단축 |
| **설정 불일치** | Data/Stop Bits 불일치 | 지속적 Framing Error | 양측 설정 확인 |

### 과목 융합 관점 분석

1. **디지털 논리회로와의 융합**:
   - **에지 검출 회로**: High→Low 하강 에지를 감지하기 위해 D 플립플롭과 NOT 게이트를 조합한 회로가 사용됩니다.
   - **시프트 레지스터**: 수신된 비트를 순차적으로 저장하고 병렬 데이터로 변환합니다.
   - **상태 머신(FSM)**: Idle → Start → Data → Parity → Stop 상태 전이를 제어합니다.

2. **신호처리와의 융합**:
   - **오버샘플링**: 16x 오버샘플링은 나이퀴스트 샘플링 정리를 넘어서 타이밍 정밀도를 높입니다.
   - **필터링**: 디바운스(Debounce) 필터가 노이즈로 인한 False Start를 방지합니다.

3. **프로토콜과의 융합**:
   - **HDLC vs 비동기**: HDLC는 플래그(01111110)로 프레임 경계를 표시하는 반면, 비동기는 Start/Stop Bit를 사용합니다.
   - **PPP 비동기 매핑**: PPP는 비동기식 링크에서 0x7E를 Start/Stop 프레임에 캡슐화합니다.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 산업용 시리얼 통신 트러블슈팅

**문제 상황**: 공장 자동화 시스템에서 PLC와 센서 간 RS-485 통신에서 간헐적으로 Framing Error가 발생하여 데이터가 손실됩니다.

**기술사의 분석 및 해결 과정**:

1. **문제 분석**:
   - 오실로스코프로 신호 파형 확인 결과, Stop Bit 구간에서 노이즈 스파이크 발견
   - 센서 장비의 클럭 정밀도가 ±3%로 확인 (요구: ±2%)

2. **해결 방안**:
   - **Stop Bits 증가**: 1 bit → 2 bits로 변경하여 수신측 여유 시간 확보
   - **보 레이트 하향**: 115200 bps → 57600 bps로 변경하여 타이밍 마진 증가
   - **하드웨어 개선**: 정밀 크리스털 오실레이터(±50 ppm)로 교체

3. **결과**:
   - Framing Error 발생률: 10⁻² → 10⁻⁶으로 개선
   - 통신 신뢰성 99.999% 달성

### 도입 시 고려사항 체크리스트

| 항목 | 확인 내용 | 권장 값 |
|------|----------|---------|
| **클럭 정밀도** | 크리스털 오실레이터 오차 | ±100 ppm 이하 |
| **케이블 길이** | RS-232C 최대 거리 | 15m 이하 |
| **노이즈 환경** | 전자기 간섭 레벨 | 차폐 케이블 필수 |
| **Stop Bits** | 수신측 처리 속도 | 2 bits 권장 (여유) |
| **Flow Control** | 하드웨어/소프트웨어 | RTS/CTS 권장 |

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - Stop Bit 생략 시도**: 일부 개발자가 전송 효율을 높이기 위해 Stop Bit를 생략하려 합니다. 그러나 Stop Bit 없이는 수신측이 문자 경계를 인식할 수 없어 통신이 불가능합니다.

- **안티패턴 2 - 내장 RC 오실레이터 사용**: 마이크로컨트롤러의 내부 RC 오실레이터는 ±10% 이상의 오차가 발생할 수 있어, 비동기식 통신에 부적합합니다.

---

## V. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 | Start/Stop Bit 사용 시 |
|------|----------------------|
| **하드웨어 단순화** | 별도 클럭 라인 불필요 |
| **비용 절감** | UART 칩 1개로 양방향 통신 |
| **설계 용이성** | 타이밍 복원 자동화 |
| **호환성** | 모든 시리얼 장비와 호환 |

### 미래 전망

- **USB 3.x 이상**: Start/Stop 대신 8b/10b 또는 128b/132b 인코딩 사용
- **무선 통신**: 패킷 preamble이 Start Bit 역할 수행
- **양자 통신**: 새로운 동기화 패러다임 요구

### 참고 표준

| 표준 | 기관 | 내용 |
|------|------|------|
| **RS-232C** | EIA/TIA | Start/Stop Bit 정의 |
| **UART 16550** | Industry | 표준 UART 레지스터 맵 |
| **ISO/IEC 8825** | ISO | ASN.1 인코딩 (비동기적 개념) |

---

## 관련 개념 맵 (Knowledge Graph)
- [동기식/비동기식 전송](./10_synchronous_asynchronous_transmission.md) - 전송 방식 비교
- [오류 검출 기법](./error_detection_parity_crc.md) - 패리티 검사
- [RS-232C 인터페이스](../3_routing/rs232_interface.md) - 물리적 인터페이스
- [UART 컨트롤러](../4_switching/uart_controller.md) - 하드웨어 구현
- [HDLC 프로토콜](../4_switching/hdlc_protocol.md) - 동기식 대안

---

## 어린이를 위한 3줄 비유 설명
1. **Start Bit**는 선생님이 **"발표 시작!"**이라고 외치는 것과 같아요. 이 신호를 듣고 친구들은 지금부터 말을 잘 들어야 한다는 것을 알게 됩니다.
2. **Stop Bit**는 선생님이 **"발표 끝!"**이라고 말하는 것과 같아요. 발표가 끝났다는 신호를 듣고 친구들은 다음 발표자를 기다릴 준비를 합니다.
3. 만약 "끝!"이라고 했는데 말이 계속되면, 친구들은 **"이상하다?"**라고 생각하겠죠? 이게 바로 **Framing Error**예요!
