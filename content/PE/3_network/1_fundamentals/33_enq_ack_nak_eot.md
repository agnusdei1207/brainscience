+++
title = "033. 통신 제어문자 (ENQ/ACK/NAK/EOT)"
description = "데이터통신의 핵심 제어문자 ENQ, ACK, NAK, EOT의 정의, 동작 메커니즘, 활용 시나리오를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["ENQ", "ACK", "NAK", "EOT", "ControlCharacters", "BSC", "ASCII", "Handshaking"]
categories = ["studynotes-3_network"]
+++

# 033. 통신 제어문자 (ENQ/ACK/NAK/EOT)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ENQ/ACK/NAK/EOT는 ASCII 제어문자 집합의 통신 제어 문자들로, 데이터통신에서 세션 설정(ENQ), 긍정 응답(ACK), 부정 응답(NAK), 세션 종료(EOT)를 표현하는 프로토콜 수준의 신호 체계입니다.
> 2. **가치**: 이들 제어문자는 송수신 간의 명확한 의사소통 프로토콜을 정의하여, 통신 신뢰성을 보장하고 오류 복구 메커니즘을 표준화하며, 이기종 시스템 간 상호 운용성을 확보합니다.
> 3. **융합**: 현대 프로토콜에서도 TCP의 SYN/ACK/FIN 플래그, HTTP 상태 코드, MQTT의 CONNACK/PUBACK 등으로 개념이 계승되어, 모든 계층의 통신 제어 기반으로 작동합니다.

---

## Ⅰ. 개요 (Context & Background)

통신 제어문자(Communication Control Characters)는 **ASCII(American Standard Code for Information Interchange)** 문자 집합의 하위 영역(0x00~0x1F)에 정의된 특수 문자들로, 데이터 자체가 아닌 **통신 과정을 제어**하는 데 사용됩니다. 이 중 ENQ(Enquiry), ACK(Acknowledgement), NAK(Negative Acknowledgement), EOT(End of Transmission)는 데이터통신의 **핸드셰이킹, 응답 확인, 오류 통보, 세션 종료**를 담당하는 핵심 제어문자입니다.

**제어문자의 역사적 배경**:
- 1963년 미국 표준 협회(ASA, 현 ANSI)가 ASCII를 표준화할 때, 데이터 처리뿐만 아니라 통신 제어를 위한 32개의 제어 문자(0x00~0x1F)를 포함시켰습니다.
- 이 중 10개(CC group)가 통신 제어 전용으로 할당되었으며, ENQ/ACK/NAK/EOT는 그 핵심을 이룹니다.

**💡 비유**: 통신 제어문자는 **'군사 라디오 통신의 구호'**와 같습니다.
- **ENQ**는 "상황 보고 바람(Roger?)" - 상대방 상태 확인
- **ACK**는 "수신 양호(Roger that)" - 메시지 잘 받았음 확인
- **NAK**는 "재전송 요청(Say again)" - 메시지 이상, 다시 보내라
- **EOT**는 "통신 종료(Over and Out)" - 대화 끝

**등장 배경 및 발전 과정**:

1. **전신틀(Teletype) 시대의 유산 (1930~50년대)**:
   초기 전신틀 기기는 기계적 릴레이로 동작했으며, 통신 제어를 위해 특수한 기능 코드가 필요했습니다. 이때 도입된 제어 코드가 ASCII 제어문자의 원형이 되었습니다.

2. **BSC 프로토콜의 체계화 (1960년대)**:
   IBM의 Binary Synchronous Communication(BSC) 프로토콜이 ENQ/ACK/NAK/EOT를 체계적으로 활용하여 **동기식 데이터 링크 제어**의 표준을 확립했습니다. 이는 HDLC, SDLC, TCP/IP 등 후속 프로토콜에 지대한 영향을 미쳤습니다.

3. **현대적 진화**:
   오늘날 이들 제어문자는 문자 그대로 전송되기보다, 개념적으로 계승되어 TCP 플래그 비트, HTTP 상태 코드, 애플리케이션 계층 프로토콜의 응답 코드로 변형되어 사용됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### ASCII 제어문자 상세 분석

| 제어문자 | 16진수 | 10진수 | 약어 의미 | 통신상 역할 | BSC 용도 | 비유 |
|---------|--------|--------|----------|------------|----------|------|
| **ENQ** | 0x05 | 5 | Enquiry (문의) | 수신측 상태 확인 요청 | 회선 설정 요청, 폴링 | "준비됐어?" |
| **ACK** | 0x06 | 6 | Acknowledge (긍정 응답) | 성공적 수신 확인 | 준비 완료, 수신 성공 | "응, OK!" |
| **NAK** | 0x15 | 21 | Negative Ack (부정 응답) | 수신 실패 또는 거부 | 준비 안됨, 오류 발생 | "안돼, 다시!" |
| **EOT** | 0x04 | 4 | End of Transmission | 전송 종료 선언 | 세션 해제, 회선 해제 | "통화 끝!" |
| **SYN** | 0x16 | 22 | Synchronous Idle | 동기화 신호 | 비트/문자 동기화 | "주의!" |
| **SOH** | 0x01 | 1 | Start of Header | 헤더 시작 표시 | 주소 정보 시작 | "주소:" |
| **STX** | 0x02 | 2 | Start of Text | 본문 시작 표시 | 데이터 시작 | "내용:" |
| **ETX** | 0x03 | 3 | End of Text | 본문 종료 표시 | 데이터 끝 | "내용 끝" |
| **DLE** | 0x10 | 16 | Data Link Escape | 투명성 확보 | 제어문자 이스케이프 | "\" |
| **ETB** | 0x17 | 23 | End of Trans. Block | 블록 전송 종료 | 멀티블록 전송 구분 | "임시 저장" |

### 정교한 구조 다이어그램: 제어문자 기반 통신 시퀀스

```ascii
================================================================================
[ Communication Control Characters: Complete Transaction Flow ]
================================================================================

   송신측 (Sender)                                    수신측 (Receiver)
   ===========                                    ================
         |                                               |
         |  Phase 1: Session Establishment (세션 설정)    |
         |                                               |
         |  [SYN][SYN][ENQ]                              |
         |  "통신 준비되셨습니까?"                         |
         |---------------------------------------------->|
         |                                               |
         |                      [내부 상태 확인]           |
         |                       - 버퍼 여유 공간?         |
         |                       - 프로세스 준비?          |
         |                       - 회선 상태?              |
         |                                               |
         |              [SYN][SYN][ACK]                   |
         |              "네, 준비되었습니다"               |
         |<----------------------------------------------|
         |                                               |
         |  Phase 2: Data Transfer (데이터 전송)          |
         |                                               |
         |  [SYN][SYN][SOH]Header[STX]Data[ETX][BCC]     |
         |  "데이터 보냅니다"                              |
         |---------------------------------------------->|
         |                                               |
         |                      [BCC 계산 및 검증]         |
         |                       - XOR checksum 수행      |
         |                       - 수신 BCC와 비교         |
         |                                               |
         |                 [성공 시]                       |
         |              [SYN][SYN][ACK]                   |
         |              "잘 받았습니다"                    |
         |<----------------------------------------------|
         |                                               |
         |                 [실패 시]                       |
         |              [SYN][SYN][NAK]                   |
         |              "오류! 다시 보내주세요"            |
         |<----------------------------------------------|
         |                                               |
         |  [동일 데이터 재전송]                           |
         |---------------------------------------------->|
         |                                               |
         |  Phase 3: Session Termination (세션 종료)      |
         |                                               |
         |  [SYN][SYN][EOT]                              |
         |  "통신 종료하겠습니다"                          |
         |---------------------------------------------->|
         |                                               |
         |              [SYN][SYN][ACK]                   |
         |              "종료 확인"                        |
         |<----------------------------------------------|
         |                                               |
         v                                               v

================================================================================
[ NAK Response Scenarios: 다양한 거부 상황 ]
================================================================================

   시나리오 A: 수신측 버퍼 부족
   ---------------------------------
   송신측: [ENQ]
   수신측: [NAK] (Buffer Overflow)
   -> 송신측: T1 타이머 후 재시도 또는 대기

   시나리오 B: BCC 오류 (전송 중 비트 손실)
   ---------------------------------
   송신측: [SOH]Header[STX]Data[ETX][BCC]
   수신측: BCC 불일치 감지
   수신측: [NAK] (CRC Error)
   -> 송신측: 동일 블록 재전송

   시나리오 C: 수신측 장애
   ---------------------------------
   송신측: [ENQ]
   수신측: 응답 없음 (Timeout)
   -> 송신측: N회 재시도 후 회선 장애 판정

   시나리오 D: 프레임 순서 오류
   ---------------------------------
   송신측: Block #2 전송 (Block #1 누락)
   수신측: [NAK] (Sequence Error)
   -> 송신측: Block #1부터 재전송 (GBN ARQ)

================================================================================
[ TCP/IP vs BSC Control Characters Mapping ]
================================================================================

   BSC 제어문자          TCP 플래그              HTTP 상태
   =============         ===========            ==========
   ENQ (0x05)     -->    SYN                    N/A
   ACK (0x06)     -->    ACK                    200 OK
   NAK (0x15)     -->    RST                    400/500 Error
   EOT (0x04)     -->    FIN                    Connection: close
   SYN (0x16)     -->    (TCP Header)           N/A

================================================================================
```

### 심층 동작 원리: 각 제어문자별 상세 메커니즘

#### 1. ENQ (Enquiry, 0x05) - 문의/상태 확인

**동작 원리**:
- 송신측이 수신측에게 **"데이터를 보내도 되는가?"**를 묻는 제어문자입니다.
- BSC에서는 `[SYN][SYN][ENQ]` 형태로 전송되며, 다중 지점 회선에서는 종국 주소를 포함합니다.

**내부 처리 과정**:
1. 송신측: ENQ 전송 후 T1 타이머(일반적으로 3초) 시작
2. 수신측: ENQ 수신 시 인터럽트 발생
3. 수신측: 내부 상태 검사 (버퍼, 프로세스, 회선)
4. 수신측: ACK(준비됨) 또는 NAK(준비 안됨) 응답
5. 송신측: 응답 수신 시 타이머 정지, 타임아웃 시 재시도

**폴링/셀렉팅 모드**:
```
폴링 ENQ:  [SYN][SYN][ENQ][SA][UA]  (SA: 종국주소, UA: 유니버설주소)
셀렉팅 ENQ: [SYN][SYN][ENQ][SA][DA]  (DA: 목적지 주소)
```

#### 2. ACK (Acknowledgement, 0x06) - 긍정 응답

**동작 원리**:
- 수신측이 **"메시지를 성공적으로 수신했다"**는 것을 송신측에 확인시켜주는 제어문자입니다.
- BSC에서 ACK는 두 가지 상황에서 사용됩니다:
  1. ENQ에 대한 응답: "전송 준비 완료"
  2. 데이터 프레임에 대한 응답: "데이터 수신 성공"

**ACK 프레임 구조**:
```
[SYN][SYN][ACK]           (기본 형태)
[SYN][SYN][DLE][ACK]      (투명 전송 모드)
[SYN][SYN][ACK][Seq#]     (시퀀스 번호 포함 - Alternating Bit Protocol)
```

**Alternating Bit Protocol (ABP)**:
- ACK0과 ACK1을 교대로 사용하여 **중복 프레임**을 검출합니다.
- ACK0: 짝수 번호 프레임에 대한 응답
- ACK1: 홀수 번호 프레임에 대한 응답

#### 3. NAK (Negative Acknowledgement, 0x15) - 부정 응답

**동작 원리**:
- 수신측이 **"메시지 수신에 실패했거나 거부한다"**는 것을 통보하는 제어문자입니다.
- NAK 수신 시 송신측은 **재전송**을 수행합니다.

**NAK 발생 원인별 분류**:

| 원인 | NAK 코드 | 설명 | 송신측 대응 |
|------|---------|------|-----------|
| 버퍼 부족 | NAK(0x15) | 수신 버퍼 가득 참 | 대기 후 재시도 |
| BCC 오류 | NAK | 체크섬 불일치 | 동일 프레임 재전송 |
| 프레임 오류 | NAK | 길이/구조 위반 | 프레임 재구성 후 전송 |
| 순서 오류 | NAK | 시퀀스 번호 불일치 | 누락 프레임부터 재전송 |
| 타임아웃 | (무응답) | 응답 없음 | ENQ 재전송 |

**NAK vs 타임아웃 차이**:
- NAK: 수신측이 명시적으로 "거부"를 표현 → 즉시 재전송
- 타임아웃: 수신측 응답 자체가 없음 → 회선 상태 의심, ENQ 재전송

#### 4. EOT (End of Transmission, 0x04) - 전송 종료

**동작 원리**:
- 송신측이 **"모든 데이터 전송을 완료했다"**는 것을 수신측에 알리고 세션을 종료합니다.
- EOT 수신 시 수신측은:
  1. 수신 버퍼를 상위 계층에 전달
  2. 회선 자원을 해제
  3. (선택적) ACK로 종료 확인

**EOT 사용 시나리오**:
```
정상 종료:
[Data Block N] --> [ACK] --> [EOT] --> [ACK]

강제 종료 (에러 상황):
[Error Detected] --> [EOT] --> 회선 해제
```

### 핵심 코드: 제어문자 기반 통신 시뮬레이터 (Python)

```python
import enum
import time
from dataclasses import dataclass, field
from typing import Optional, Deque
from collections import deque
import random

class ControlChar(enum.Enum):
    """ASCII 통신 제어문자 정의"""
    SOH = 0x01  # Start of Header
    STX = 0x02  # Start of Text
    ETX = 0x03  # End of Text
    EOT = 0x04  # End of Transmission
    ENQ = 0x05  # Enquiry
    ACK = 0x06  # Acknowledgement
    DLE = 0x10  # Data Link Escape
    NAK = 0x15  # Negative Acknowledgement
    SYN = 0x16  # Synchronous Idle
    ETB = 0x17  # End of Transmission Block

@dataclass
class CommunicationStats:
    """통신 통계 정보"""
    enq_sent: int = 0
    enq_received: int = 0
    ack_sent: int = 0
    ack_received: int = 0
    nak_sent: int = 0
    nak_received: int = 0
    eot_sent: int = 0
    eot_received: int = 0
    data_bytes_sent: int = 0
    data_bytes_received: int = 0
    retransmissions: int = 0

@dataclass
class BSCFrame:
    """BSC 프레임 구조"""
    syn1: int = ControlChar.SYN.value
    syn2: int = ControlChar.SYN.value
    control: Optional[int] = None
    header: bytes = b""
    data: bytes = b""
    bcc: int = 0

    def to_bytes(self) -> bytes:
        """프레임을 바이트열로 변환"""
        frame = bytearray([self.syn1, self.syn2])

        if self.control:
            frame.append(self.control)

        if self.header:
            frame.append(ControlChar.SOH.value)
            frame.extend(self.header)

        if self.data:
            frame.append(ControlChar.STX.value)
            frame.extend(self.data)
            frame.append(ControlChar.ETX.value)
            frame.append(self.bcc)

        return bytes(frame)

    @classmethod
    def create_enq(cls) -> 'BSCFrame':
        """ENQ 프레임 생성"""
        return cls(control=ControlChar.ENQ.value)

    @classmethod
    def create_ack(cls) -> 'BSCFrame':
        """ACK 프레임 생성"""
        return cls(control=ControlChar.ACK.value)

    @classmethod
    def create_nak(cls) -> 'BSCFrame':
        """NAK 프레임 생성"""
        return cls(control=ControlChar.NAK.value)

    @classmethod
    def create_eot(cls) -> 'BSCFrame':
        """EOT 프레임 생성"""
        return cls(control=ControlChar.EOT.value)

    @classmethod
    def create_data_frame(cls, data: bytes, header: bytes = b"") -> 'BSCFrame':
        """데이터 프레임 생성 (BCC 포함)"""
        bcc = 0
        # BCC는 STX 이후 ETX까지의 모든 바이트에 대해 XOR
        for byte in data:
            bcc ^= byte

        return cls(
            control=None,
            header=header,
            data=data,
            bcc=bcc
        )

class CommunicationEndpoint:
    """
    통신 단말 시뮬레이터
    ENQ/ACK/NAK/EOT 기반 통신 구현
    """

    def __init__(
        self,
        name: str,
        error_rate: float = 0.0,
        buffer_size: int = 4096
    ):
        self.name = name
        self.error_rate = error_rate
        self.buffer_size = buffer_size

        # 상태 변수
        self._receive_buffer: Deque[bytes] = deque()
        self._is_ready = True
        self._current_session: Optional[str] = None

        # 통계
        self.stats = CommunicationStats()

        # 타임아웃 설정
        self.enq_timeout = 3.0
        self.data_timeout = 5.0
        self.max_retries = 3

    def send_enq(self, channel: 'CommunicationChannel', target: str) -> bool:
        """ENQ 전송 및 ACK 대기"""
        for attempt in range(self.max_retries):
            self.stats.enq_sent += 1
            frame = BSCFrame.create_enq()
            print(f"[{self.name}] ENQ 전송 (시도 {attempt + 1}/{self.max_retries})")

            channel.transmit(self.name, target, frame.to_bytes())

            # 응답 대기
            response = channel.receive(self.name, timeout=self.enq_timeout)

            if response is None:
                print(f"[{self.name}] 타임아웃 - 응답 없음")
                continue

            # 응답 분석
            if len(response) >= 3:
                ctrl = response[2]
                if ctrl == ControlChar.ACK.value:
                    self.stats.ack_received += 1
                    print(f"[{self.name}] ACK 수신 - 세션 설정 성공")
                    self._current_session = target
                    return True
                elif ctrl == ControlChar.NAK.value:
                    self.stats.nak_received += 1
                    print(f"[{self.name}] NAK 수신 - 수신측 준비 안됨")

            time.sleep(0.5)

        return False

    def receive_enq(self, channel: 'CommunicationChannel', sender: str):
        """ENQ 수신 처리"""
        self.stats.enq_received += 1
        print(f"[{self.name}] ENQ 수신 from {sender}")

        # 준비 상태 확인
        if not self._is_ready or len(self._receive_buffer) >= self.buffer_size:
            self.stats.nak_sent += 1
            response = BSCFrame.create_nak()
            print(f"[{self.name}] NAK 전송 - 준비 안됨")
        else:
            self.stats.ack_sent += 1
            response = BSCFrame.create_ack()
            print(f"[{self.name}] ACK 전송 - 준비 완료")
            self._current_session = sender

        channel.transmit(self.name, sender, response.to_bytes())

    def send_data(
        self,
        channel: 'CommunicationChannel',
        data: bytes,
        header: bytes = b""
    ) -> bool:
        """데이터 전송 및 ACK/NAK 대기"""
        if not self._current_session:
            print(f"[{self.name}] 오류: 세션이 설정되지 않음")
            return False

        for attempt in range(self.max_retries):
            frame = BSCFrame.create_data_frame(data, header)
            print(f"[{self.name}] 데이터 전송 ({len(data)} bytes, 시도 {attempt + 1})")

            channel.transmit(self.name, self._current_session, frame.to_bytes())
            self.stats.data_bytes_sent += len(data)

            # 응답 대기
            response = channel.receive(self.name, timeout=self.data_timeout)

            if response is None:
                print(f"[{self.name}] 타임아웃")
                self.stats.retransmissions += 1
                continue

            if len(response) >= 3:
                ctrl = response[2]
                if ctrl == ControlChar.ACK.value:
                    self.stats.ack_received += 1
                    print(f"[{self.name}] ACK 수신 - 전송 성공")
                    return True
                elif ctrl == ControlChar.NAK.value:
                    self.stats.nak_received += 1
                    self.stats.retransmissions += 1
                    print(f"[{self.name}] NAK 수신 - 재전송")

            time.sleep(0.3)

        return False

    def receive_data(self, channel: 'CommunicationChannel', frame_bytes: bytes):
        """데이터 프레임 수신 처리"""
        try:
            # 프레임 파싱
            stx_idx = frame_bytes.index(ControlChar.STX.value)
            etx_idx = frame_bytes.index(ControlChar.ETX.value)

            data = frame_bytes[stx_idx + 1:etx_idx]
            received_bcc = frame_bytes[etx_idx + 1]

            # BCC 검증
            calculated_bcc = 0
            for byte in data:
                calculated_bcc ^= byte

            # 에러 시뮬레이션
            if random.random() < self.error_rate:
                calculated_bcc ^= 0xFF  # 강제로 BCC 불일치

            if calculated_bcc != received_bcc:
                self.stats.nak_sent += 1
                response = BSCFrame.create_nak()
                print(f"[{self.name}] BCC 오류 - NAK 전송")
            else:
                self._receive_buffer.append(data)
                self.stats.ack_sent += 1
                self.stats.data_bytes_received += len(data)
                response = BSCFrame.create_ack()
                print(f"[{self.name}] 데이터 수신 성공 ({len(data)} bytes) - ACK 전송")

            if self._current_session:
                channel.transmit(self.name, self._current_session, response.to_bytes())

        except (ValueError, IndexError) as e:
            print(f"[{self.name}] 프레임 파싱 오류: {e}")
            response = BSCFrame.create_nak()
            if self._current_session:
                channel.transmit(self.name, self._current_session, response.to_bytes())

    def send_eot(self, channel: 'CommunicationChannel'):
        """EOT 전송 (세션 종료)"""
        if self._current_session:
            self.stats.eot_sent += 1
            frame = BSCFrame.create_eot()
            print(f"[{self.name}] EOT 전송 - 세션 종료")
            channel.transmit(self.name, self._current_session, frame.to_bytes())
            self._current_session = None

    def receive_eot(self, channel: 'CommunicationChannel'):
        """EOT 수신 처리"""
        self.stats.eot_received += 1
        print(f"[{self.name}] EOT 수신 - 세션 종료")
        # ACK로 종료 확인 (선택적)
        self._current_session = None

    def get_received_data(self) -> bytes:
        """수신된 모든 데이터 반환"""
        result = b"".join(self._receive_buffer)
        self._receive_buffer.clear()
        return result

class CommunicationChannel:
    """통신 채널 시뮬레이터"""

    def __init__(self, error_rate: float = 0.0, delay: float = 0.1):
        self.error_rate = error_rate
        self.delay = delay
        self._buffers: dict[str, Deque[bytes]] = {}

    def register(self, endpoint: str):
        """단말 등록"""
        self._buffers[endpoint] = deque()

    def transmit(self, sender: str, receiver: str, data: bytes):
        """데이터 전송"""
        time.sleep(self.delay)  # 전파 지연 시뮬레이션

        # 에러 주입 (비트 에러)
        if random.random() < self.error_rate:
            # 랜덤한 위치에 비트 에러 발생
            data = bytearray(data)
            error_pos = random.randint(0, len(data) - 1)
            data[error_pos] ^= (1 << random.randint(0, 7))
            data = bytes(data)

        if receiver in self._buffers:
            self._buffers[receiver].append(data)

    def receive(self, endpoint: str, timeout: float = 1.0) -> Optional[bytes]:
        """데이터 수신"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if endpoint in self._buffers and self._buffers[endpoint]:
                return self._buffers[endpoint].popleft()
            time.sleep(0.01)
        return None

# 사용 예시
if __name__ == "__main__":
    # 통신 채널 생성
    channel = CommunicationChannel(error_rate=0.1, delay=0.05)
    channel.register("SENDER")
    channel.register("RECEIVER")

    # 통신 단말 생성
    sender = CommunicationEndpoint("SENDER")
    receiver = CommunicationEndpoint("RECEIVER")

    # 통신 시뮬레이션
    print("=" * 60)
    print("통신 시뮬레이션 시작")
    print("=" * 60)

    # 1. 세션 설정
    if sender.send_enq(channel, "RECEIVER"):
        # 2. 데이터 전송
        test_data = b"Hello, BSC Protocol! This is a test message."
        sender.send_data(channel, test_data)

        # 3. 세션 종료
        sender.send_eot(channel)

    print("\n" + "=" * 60)
    print("통신 통계")
    print("=" * 60)
    print(f"송신측 - ENQ: {sender.stats.enq_sent}, ACK수신: {sender.stats.ack_received}")
    print(f"수신측 - ENQ: {receiver.stats.enq_received}, ACK송신: {receiver.stats.ack_sent}")
