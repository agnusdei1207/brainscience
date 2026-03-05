+++
title = "032. 회선 제어 규약 (Line Discipline / ENQ/ACK)"
description = "데이터통신에서 회선 제어 규약의 ENQ/ACK 메커니즘과 폴링/셀렉팅 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["LineDiscipline", "ENQ", "ACK", "Polling", "Selection", "FlowControl", "BSC", "HDLC"]
categories = ["studynotes-3_network"]
+++

# 032. 회선 제어 규약 (Line Discipline)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 회선 제어 규약(Line Discipline)은 데이터통신에서 송수신 간의 전송 순서를 제어하고, 회선의 사용권을 관리하며, 데이터 전송의 개시와 종료를 조율하는 프로토콜 수준의 통신 규약입니다.
> 2. **가치**: ENQ(Enquiry)/ACK(Acknowledgement) 기반의 핸드셰이킹을 통해 수신측의 준비 상태를 확인한 후 데이터를 전송함으로써, 전송 효율을 최적화하고 데이터 손실을 사전에 방지합니다.
> 3. **융합**: 현대 네트워크에서는 TCP 3-Way Handshake, CSMA/CD의 RTS/CTS, 그리고 무선 통신의 스케줄링 기법으로 진화하여, 다양한 통신 환경에서 세션 제어의 근간이 됩니다.

---

## Ⅰ. 개요 (Context & Background)

회선 제어 규약(Line Discipline)은 데이터통신 시스템에서 송신측과 수신측 사이의 **통신 세션을 설정, 유지, 해제**하는 절차적 규약입니다. 이는 단순히 데이터를 전기적 신호로 변환하여 전송하는 물리적 계층을 넘어, **"언제, 누가, 어떻게 데이터를 보낼 것인가"**를 제어하는 논리적 계층의 핵심 기능을 담당합니다.

회선 제어 규약의 주요 기능은 다음과 같이 분류됩니다:
1. **회선 사용권 제어**: 누가 현재 회선을 사용할 권한을 가지는지 결정
2. **전송 개시/종료 제어**: 데이터 전송의 시작과 끝을 명시적으로 표시
3. **상태 확인 및 동기화**: 수신측의 준비 상태를 확인하고 통신 파라미터를 동기화
4. **오류 복구 절차**: 전송 중단, 타임아웃, 오류 발생 시의 복구 절차 정의

**💡 비유**: 회선 제어 규약은 **'라디오 통신의 프로토콜'**과 같습니다.
- 군사 통신에서 "Over"라고 말하면 상대방에게 발언권을 넘기는 것을 의미합니다. 이것이 **회선 사용권 제어**입니다.
- "Over and Out"이라고 하면 통신을 종료하겠다는 의미입니다. 이것이 **전송 종료 제어**입니다.
- "수신 확인(Roger)?"이라고 물으면 상대방이 준비되었는지 확인하는 것입니다. 이것이 **ENQ/ACK 메커니즘**입니다.

**등장 배경 및 발전 과정**:

1. **초기 통신의 혼란 (1950~60년대)**:
   초기 데이터통신 시스템에서는 송신측이 데이터를 무조건 전송했습니다. 수신측이 준비되지 않은 상태에서 데이터가 도착하면 데이터 손실이 발생했고, 두 장치가 동시에 데이터를 전송하면 충돌(Collision)이 발생했습니다. 이러한 문제를 해결하기 위해 체계적인 회선 제어 규약이 필요했습니다.

2. **BSC(Binary Synchronous Communication)의 등장 (1960년대 후반)**:
   IBM이 개발한 BSC 프로토콜은 ENQ(Enquiry)/ACK(Acknowledgement) 제어 문자를 도입하여 수신측의 준비 상태를 확인한 후 데이터를 전송하는 **"확인 후 전송(Confirm-before-Send)"** 패러다임을 확립했습니다. 이는 현대 TCP 핸드셰이킹의 원형이 되었습니다.

3. **HDLC 및 현대적 진화 (1970년대~현재)**:
   ISO가 표준화한 HDLC(High-Level Data Link Control)는 회선 제어 기능을 프레임 구조에 통합했습니다. 오늘날 TCP/IP의 3-Way Handshake, 이더넷의 CSMA/CD, 무선 LAN의 RTS/CTS 등 모든 현대 통신 프로토콜에 회선 제어 규약의 원리가 내장되어 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 상세 역할 | 내부 동작 메커니즘 | 관련 표준/기술 | 비유 |
|---------|------|----------|-------------------|---------------|------|
| **ENQ** | Enquiry (문의) | 수신측에 전송 준비 상태 문의 | 제어 문자(0x05) 전송, 타임아웃 대기, 재시도 카운터 | BSC, ASCII | "준비됐어?" |
| **ACK** | Acknowledgement (긍정 응답) | 수신 준비 완료 및 데이터 수신 확인 | 제어 문자(0x06) 전송, 버퍼 할당 완료 신호 | BSC, TCP | "응, 준비됐어!" |
| **NAK** | Negative Ack (부정 응답) | 수신 거부 또는 오류 통보 | 제어 문자(0x15) 전송, 오류 코드 포함 가능 | BSC, ARQ | "안돼, 다시 보내" |
| **EOT** | End of Transmission (전송 종료) | 통신 세션 종료 및 회선 해제 | 제어 문자(0x04) 전송, 버퍼 해제 | BSC, HDLC | "통화 끝!" |
| **SOH** | Start of Header (헤더 시작) | 메시지 헤더의 시작 표시 | 제어 문자(0x01), 헤더 파싱 트리거 | BSC | "주소 정보 시작" |
| **STX** | Start of Text (본문 시작) | 데이터 본문의 시작 표시 | 제어 문자(0x02), 페이로드 파싱 트리거 | BSC | "내용 시작" |
| **ETX** | End of Text (본문 종료) | 데이터 본문의 종료 표시 | 제어 문자(0x03), CRC 확인 트리거 | BSC | "내용 끝" |
| **DLE** | Data Link Escape (이스케이프) | 제어 문자와 데이터 구분 | 제어 문자(0x10), 투명성 확보 | BSC | "다음은 데이터야" |

### 정교한 구조 다이어그램: ENQ/ACK 핸드셰이킹 프로세스

```ascii
================================================================================
[ Line Discipline: ENQ/ACK Handshake Sequence Diagram ]
================================================================================

   [송신측 (Sender)]                          [수신측 (Receiver)]
         |                                           |
         |  1. ENQ (Enquiry)                         |
         |  "전송 준비됐니?"                          |
         |------------------------------------------>|
         |                                           |
         |                 2. 수신측 상태 확인         |
         |                    - 버퍼 할당 가능?       |
         |                    - 프로세스 준비?        |
         |                    - 회선 상태 양호?       |
         |                                           |
         |  2-1. ACK (준비 완료)                      |
         |  "응, 준비됐어!"                           |
         |<------------------------------------------|
         |                                           |
         |  3. SOH + Header + STX + Data + ETX       |
         |     + BCC (Block Check Character)         |
         |------------------------------------------>|
         |                                           |
         |                 4. 수신측 처리              |
         |                    - 헤더 파싱             |
         |                    - 데이터 추출           |
         |                    - BCC 계산 및 검증      |
         |                                           |
         |  4-1. ACK (수신 성공)                      |
         |<------------------------------------------|
         |                                           |
         |  5. EOT (End of Transmission)             |
         |  "전송 종료할게"                           |
         |------------------------------------------>|
         |                                           |
         |                 6. 세션 정리               |
         |                    - 버퍼 해제             |
         |                    - 회선 해제             |
         |                                           |
         v                                           v

================================================================================
[ Error Scenario: NAK Response ]
================================================================================

   [송신측 (Sender)]                          [수신측 (Receiver)]
         |                                           |
         |  1. ENQ (Enquiry)                         |
         |------------------------------------------>|
         |                                           |
         |  2. NAK (준비 안됨)                        |
         |  "지금 바빠, 나중에 다시 물어봐"            |
         |<------------------------------------------|
         |                                           |
         |  3. 재시도 대기 (T1 타이머)                 |
         |     또는                                   |
         |  3. 폴링 대기 (Polling Mode)              |
         |                                           |
         v                                           v

================================================================================
[ Multipoint Line Discipline: Polling vs Selection ]
================================================================================

                    +------------------+
                    |   주국 (Primary) |
                    |    Controller    |
                    +--------|---------+
                             |
        +--------------------+--------------------+
        |                    |                    |
   [종국 A]             [종국 B]             [종국 C]
   (Secondary)          (Secondary)          (Secondary)

   [폴링(Polling) - 주국이 종국에 데이터 요청]
   주국: "종국 A, 보낼 데이터 있어?" (Poll ENQ)
   종국 A: "없어" (NAK) 또는 "있어, 이거야" (Data)

   [셀렉팅(Selection) - 주국이 종국에 데이터 전송]
   주국: "종국 B, 데이터 받을 준비 됐어?" (Select ENQ)
   종국 B: "응, 준비됐어" (ACK)
   주국: [데이터 전송]

================================================================================
```

### 심층 동작 원리: ENQ/ACK 기반 회선 제어 7단계 프로세스

1. **회선 활성화 및 초기화 (Line Activation)**:
   - 송신측은 물리적 회선이 활성화되어 있는지 확인합니다(DCD 신호 등).
   - 내부 송신 버퍼에 전송할 데이터가 있는지 확인합니다.
   - 타임아웃 타이머(T1)와 재시도 카운터를 초기화합니다.

2. **ENQ 전송 및 수신측 문의 (Enquiry)**:
   - 송신측이 ENQ(0x05) 제어 문자를 전송합니다.
   - ENQ 프레임에는 송신측 주소와 요청 유형(전송 요청/폴링 응답)이 포함될 수 있습니다.
   - 타이머 T1을 시작하여 응답 대기 시간을 측정합니다.

3. **수신측 준비 상태 확인 (Receiver Readiness Check)**:
   - 수신측은 ENQ 수신 시 다음 조건을 검사합니다:
     - 수신 버퍼가 사용 가능한가?
     - 상위 계층 애플리케이션이 데이터를 수신할 준비가 되었는가?
     - 시스템 오버로드 상태가 아닌가?
   - 모든 조건이 충족되면 ACK(0x06)를, 그렇지 않으면 NAK(0x15)를 응답합니다.

4. **ACK 수신 및 데이터 전송 (Data Transfer)**:
   - 송신측이 ACK를 수신하면 데이터 전송을 시작합니다.
   - 데이터는 다음과 같은 프레임 구조로 전송됩니다:
     ```
     [SYN][SYN][SOH][Header][STX][Data][ETX][BCC]
     ```
   - SYN(0x16)은 2개 연속으로 전송하여 동기화를 확보합니다.

5. **수신측 데이터 처리 및 검증 (Data Processing)**:
   - 수신측은 SOH, STX, ETX를 기준으로 헤더와 데이터를 분리합니다.
   - BCC(Block Check Character)를 계산하여 수신된 BCC와 비교합니다.
   - 오류가 없으면 ACK를, 오류가 있으면 NAK를 송신측에 회신합니다.

6. **오류 복구 및 재전송 (Error Recovery)**:
   - NAK 수신 시: 송신측은 동일한 데이터를 재전송합니다(최대 N회).
   - 타임아웃 발생 시: ENQ를 재전송하거나 회선 상태를 진단합니다.
   - 연속 오류 발생 시: 세션을 종료하고 상위 계층에 오류를 보고합니다.

7. **세션 종료 및 회선 해제 (Session Termination)**:
   - 모든 데이터 전송이 완료되면 송신측이 EOT(0x04)를 전송합니다.
   - 수신측은 EOT 수신 확인 ACK를 회신합니다(선택적).
   - 양측 모두 버퍼를 해제하고 회선 제어권을 반환합니다.

### 핵심 코드: ENQ/ACK 기반 회선 제어 구현 (Python)

```python
import time
import enum
from dataclasses import dataclass
from typing import Optional, Callable
from threading import Event, Thread

class ControlChar(enum.Enum):
    """BSC 제어 문자 정의"""
    SOH = 0x01  # Start of Header
    STX = 0x02  # Start of Text
    ETX = 0x03  # End of Text
    EOT = 0x04  # End of Transmission
    ENQ = 0x05  # Enquiry
    ACK = 0x06  # Acknowledgement
    DLE = 0x10  # Data Link Escape
    NAK = 0x15  # Negative Acknowledgement
    SYN = 0x16  # Synchronous Idle

@dataclass
class LineControlConfig:
    """회선 제어 설정 파라미터"""
    enq_timeout: float = 2.0        # ENQ 응답 대기 시간 (초)
    data_timeout: float = 5.0       # 데이터 응답 대기 시간 (초)
    max_retries: int = 3            # 최대 재시도 횟수
    retry_delay: float = 0.5        # 재시도 간격 (초)
    buffer_size: int = 4096         # 수신 버퍼 크기

class LineDisciplineController:
    """
    회선 제어 규약 구현체
    ENQ/ACK 핸드셰이킹 및 폴링/셀렉팅 지원
    """

    def __init__(
        self,
        config: LineControlConfig,
        send_func: Callable[[bytes], int],
        recv_func: Callable[[], bytes]
    ):
        """
        Args:
            config: 회선 제어 설정
            send_func: 물리적 전송 함수 (바이트열 -> 전송 바이트 수)
            recv_func: 물리적 수신 함수 (-> 수신된 바이트열)
        """
        self.config = config
        self._send = send_func
        self._recv = recv_func

        # 내부 상태 변수
        self._is_ready = True
        self._receive_buffer = bytearray()
        self._current_sender: Optional[str] = None

        # 동기화 객체
        self._response_event = Event()
        self._last_response: Optional[bytes] = None

    def _send_control(self, char: ControlChar) -> int:
        """제어 문자 전송"""
        frame = bytes([ControlChar.SYN.value, ControlChar.SYN.value, char.value])
        return self._send(frame)

    def _wait_response(self, timeout: float) -> Optional[bytes]:
        """응답 대기 (타임아웃 포함)"""
        self._response_event.clear()
        if self._response_event.wait(timeout):
            return self._last_response
        return None  # 타임아웃

    def establish_session(self, receiver_id: str = "") -> bool:
        """
        ENQ/ACK 기반 세션 설정
        Returns:
            True: 세션 설정 성공 (수신측 준비 완료)
            False: 세션 설정 실패
        """
        for attempt in range(self.config.max_retries):
            print(f"[송신측] ENQ 전송 (시도 {attempt + 1}/{self.config.max_retries})")

            # ENQ 전송
            self._send_control(ControlChar.ENQ)
            if receiver_id:
                self._send(f"POLL:{receiver_id}".encode())

            # 응답 대기
            response = self._wait_response(self.config.enq_timeout)

            if response is None:
                print(f"[송신측] 타임아웃 - 응답 없음")
                time.sleep(self.config.retry_delay)
                continue

            if ControlChar.ACK.value in response:
                print(f"[송신측] ACK 수신 - 세션 설정 성공")
                self._current_sender = receiver_id
                return True

            if ControlChar.NAK.value in response:
                print(f"[송신측] NAK 수신 - 수신측 준비 안됨")
                time.sleep(self.config.retry_delay)
                continue

        print(f"[송신측] 세션 설정 실패 - 최대 재시도 횟수 초과")
        return False

    def send_data(self, data: bytes, header: bytes = b"") -> bool:
        """
        데이터 전송 (BSC 프레임 구조)
        프레임 형식: [SYN][SYN][SOH][Header][STX][Data][ETX][BCC]
        """
        # BCC(Block Check Character) 계산 - LRC(Longitudinal Redundancy Check)
        bcc = 0
        for byte in data:
            bcc ^= byte  # XOR 연산

        # 프레임 조립
        frame = bytearray()
        frame.extend([ControlChar.SYN.value, ControlChar.SYN.value])

        if header:
            frame.append(ControlChar.SOH.value)
            frame.extend(header)

        frame.append(ControlChar.STX.value)
        frame.extend(data)
        frame.append(ControlChar.ETX.value)
        frame.append(bcc)

        for attempt in range(self.config.max_retries):
            print(f"[송신측] 데이터 전송 ({len(data)} bytes, 시도 {attempt + 1})")

            # 데이터 프레임 전송
            self._send(bytes(frame))

            # ACK/NAK 대기
            response = self._wait_response(self.config.data_timeout)

            if response is None:
                print(f"[송신측] 타임아웃 - 재전송")
                continue

            if ControlChar.ACK.value in response:
                print(f"[송신측] ACK 수신 - 데이터 전송 성공")
                return True

            if ControlChar.NAK.value in response:
                print(f"[송신측] NAK 수신 - 오류 발생, 재전송")
                continue

        return False

    def terminate_session(self):
        """세션 종료 (EOT 전송)"""
        print(f"[송신측] EOT 전송 - 세션 종료")
        self._send_control(ControlChar.EOT)
        self._current_sender = None

    def process_enquiry(self) -> bool:
        """
        수신측: ENQ 수신 처리
        Returns:
            True: ACK 전송 (준비 완료)
            False: NAK 전송 (준비 안됨)
        """
        # 수신 준비 상태 확인
        if not self._is_ready:
            print(f"[수신측] 준비 안됨 - NAK 전송")
            self._send_control(ControlChar.NAK)
            return False

        if len(self._receive_buffer) > self.config.buffer_size * 0.8:
            print(f"[수신측] 버퍼 부족 - NAK 전송")
            self._send_control(ControlChar.NAK)
            return False

        print(f"[수신측] 준비 완료 - ACK 전송")
        self._send_control(ControlChar.ACK)
        return True

    def process_data(self, frame: bytes) -> bool:
        """
        수신측: 데이터 프레임 처리
        BCC 검증 후 ACK/NAK 응답
        """
        try:
            # STX와 ETX 사이의 데이터 추출
            stx_idx = frame.index(ControlChar.STX.value)
            etx_idx = frame.index(ControlChar.ETX.value)

            data = frame[stx_idx + 1:etx_idx]
            received_bcc = frame[etx_idx + 1]

            # BCC 검증
            calculated_bcc = 0
            for byte in data:
                calculated_bcc ^= byte

            if calculated_bcc != received_bcc:
                print(f"[수신측] BCC 오류 - NAK 전송")
                self._send_control(ControlChar.NAK)
                return False

            # 데이터 저장
            self._receive_buffer.extend(data)
            print(f"[수신측] 데이터 수신 성공 ({len(data)} bytes) - ACK 전송")
            self._send_control(ControlChar.ACK)
            return True

        except (ValueError, IndexError) as e:
            print(f"[수신측] 프레임 파싱 오류: {e}")
            self._send_control(ControlChar.NAK)
            return False

    def set_ready(self, ready: bool):
        """수신 준비 상태 설정"""
        self._is_ready = ready


class PollingController:
    """
    다중 지점(Multipoint) 회선 제어: 폴링/셀렉팅 구현
    """

    def __init__(self, secondary_stations: list[str], controller: LineDisciplineController):
        self.stations = secondary_stations
        self.controller = controller
        self.poll_index = 0

    def poll_all(self) -> dict[str, bool]:
        """
        모든 종국에 순차적 폴링 수행
        Returns:
            {station_id: 데이터_수신_여부}
        """
        results = {}

        for station in self.stations:
            print(f"\n[주국] {station} 폴링 시작")

            if self.controller.establish_session(station):
                # 데이터 수신 시도
                # 실제 구현에서는 수신 루프가 필요
                results[station] = True
                self.controller.terminate_session()
            else:
                results[station] = False

        return results

    def select_station(self, station_id: str, data: bytes) -> bool:
        """
        특정 종국에 데이터 전송 (셀렉팅)
        """
        print(f"\n[주국] {station_id} 셀렉팅 시작")

        if not self.controller.establish_session(station_id):
            return False

        success = self.controller.send_data(data)
        self.controller.terminate_session()

        return success


# 실무 사용 예시
if __name__ == "__main__":
    # 모의 전송/수신 함수
    transmitted_data = []
    def mock_send(data: bytes) -> int:
        transmitted_data.append(data)
        return len(data)

    def mock_recv() -> bytes:
        return bytes([ControlChar.ACK.value])  # 항상 ACK 응답

    # 회선 제어기 생성
    config = LineControlConfig(
        enq_timeout=2.0,
        max_retries=3
    )
    controller = LineDisciplineController(config, mock_send, mock_recv)

    # 세션 설정 및 데이터 전송
    if controller.establish_session("STATION_A"):
        controller.send_data(b"Hello, World!")
        controller.terminate_session()
