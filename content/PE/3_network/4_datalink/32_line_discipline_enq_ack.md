+++
title = "032. 회선 제어 규약 (Line Discipline) 및 ENQ/ACK/NAK/EOT"
description = "데이터 통신에서 회선 사용권을 제어하고 오류 없는 데이터 전송을 보장하는 회선 제어 규약과 ENQ/ACK/NAK/EOT 제어 문자의 동작 원리를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["LineDiscipline", "ENQ", "ACK", "NAK", "EOT", "FlowControl", "ARQ", "BSC"]
categories = ["studynotes-3_network"]
+++

# 032. 회선 제어 규약 (Line Discipline) 및 ENQ/ACK/NAK/EOT

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 회선 제어 규약은 통신 회선의 효율적이고 질서 있는 사용을 위한 규칙 체계로, ENQ(질의)/ACK(긍정응답)/NAK(부정응답)/EOT(전송종료) 제어 문자를 통해 링크 설정, 데이터 전송, 오류 제어, 링크 해제를 수행합니다.
> 2. **가치**: ENQ/ACK 핸드셰이크는 수신 준비 상태 확인으로 불필요한 재전송을 방지하고, ACK/NAK 피드백으로 ARQ(자동 재전송 요구) 기반 신뢰성을 확보하며, 현대 TCP의 3-way 핸드셰이크와 슬라이딩 윈도우의 기원이 됩니다.
> 3. **융합**: BSC(Binary Synchronous Communication) 프로토콜의 기반이며, 현대 Modbus, ASCII 제어 프로토콜, 산업용 시리얼 통신, PPP 협상 등 다양한 통신 프로토콜의 제어 메커니즘 원형입니다.

---

## Ⅰ. 개요 (Context & Background)

**회선 제어 규약(Line Discipline)**은 데이터 통신에서 송수신 간의 질서 있는 데이터 교환을 보장하는 규칙들의 집합입니다. 주요 기능은:

1. **링크 설정(Link Establishment)**: 통신 양단 간 연결 설정
2. **흐름 제어(Flow Control)**: 수신측 처리 능력에 맞춘 전송 속도 조절
3. **오류 제어(Error Control)**: 전송 오류 검출 및 재전송
4. **링크 해제(Link Termination)**: 통신 종료 및 자원 해제

**제어 문자(Control Characters)**는 ASCII 코드의 0x00~0x1F 영역에 정의된 특수 문자들로, 데이터가 아닌 통신 제어용으로 사용됩니다:

| 제어 문자 | ASCII | 명칭 | 용도 |
|----------|-------|------|------|
| **ENQ** | 0x05 | Enquiry | 수신 준비 상태 질의 |
| **ACK** | 0x06 | Acknowledge | 긍정 응답 (수신 성공) |
| **NAK** | 0x15 | Negative Acknowledge | 부정 응답 (오류 감지) |
| **EOT** | 0x04 | End of Transmission | 전송 종료 |
| **SYN** | 0x16 | Synchronous Idle | 동기 유지 |
| **STX** | 0x02 | Start of Text | 본문 시작 |
| **ETX** | 0x03 | End of Text | 본문 종료 |
| **DLE** | 0x10 | Data Link Escape | 제어 문자 확장 |

**💡 비유**: 회선 제어 규약은 **'무전기 통신 프로토콜'**과 같습니다.
- "들리세요?" (ENQ) → "네, 들립니다" (ACK)
- "메시지 보냅니다... 끝" (STX...ETX) → "받았습니다" (ACK) / "다시 보내주세요" (NAK)
- "통신 종료합니다" (EOT)

**등장 배경 및 발전 과정**:
1. **텔레타이프 시대 (1900년대 초)**: 기계식 텔레타이프에서 제어 문자 정의
2. **BSC 프로토콜 (1960년대)**: IBM이 메인프레임 통신용으로 체계화
3. **HDLC/SDLC (1970년대)**: 비트 지향 프로토콜로 발전
4. **TCP/IP (1980년대~)**: 현대적 연결 지향 프로토콜로 진화

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석: 회선 제어 상태 기계

| 상태 | 명칭 | 진입 조건 | 동작 | 탈출 조건 |
|------|------|----------|------|----------|
| **IDLE** | 대기 | 초기 상태 | 회선 감시 | ENQ 수신 |
| **SETUP** | 설정 | ENQ 송신 | ACK 대기 | ACK 수신 → XMIT |
| **XMIT** | 전송 | 설정 완료 | 데이터 송신 | ETX 송신 → WAIT |
| **WAIT** | 대기 | 데이터 송신 완료 | ACK/NAK 대기 | ACK → 계속/NAK → 재전송 |
| **TERM** | 종료 | EOT 송수신 | 링크 해제 | IDLE로 복귀 |

### 정교한 구조 다이어그램: BSC 프레임 구조 및 동작

```ascii
================================================================================
[ BSC (Binary Synchronous Communication) Frame Structure ]
================================================================================

    +------+------+----------+------+----------+------+-------+
    | SYN  | SYN  |   DLE    | STX  |  DATA   | ETX  | BCC   |
    | 0x16 | 0x16 |   0x10   | 0x02 | (Text)  | 0x03 |(CRC)  |
    +------+------+----------+------+----------+------+-------+
      ^      ^       ^         ^                 ^       ^
      |      |       |         |                 |       |
   Sync   Sync   Escape     Start            End    Error
   Byte #1 Byte #2 Sequence  of Text          of Text Detect

    For Transparent Mode (data may contain control chars):
    +------+------+----------+------+----------+----------+-------+
    | SYN  | SYN  |   DLE    | STX  |  DATA    | DLE ETX  | BCC   |
    |      |      |          |      |(binary)  |          |       |
    +------+------+----------+------+----------+----------+-------+
                                     ↑              ↑
                                 DLE STX       DLE ETX

================================================================================
[ ENQ/ACK Handshake Sequence ]
================================================================================

    Station A (Sender)                      Station B (Receiver)
         |                                        |
         |  ---------- ENQ (Are you ready?) ----->|
         |                                        |
         |          (Check if ready)              |
         |                                        |
         |<--------- ACK (Yes, ready) ------------|
         |                                        |
         |  -------- SYN SYN STX DATA ETX ------->|
         |                                        |
         |          (Verify BCC/CRC)              |
         |                                        |
         |<--------- ACK (Data OK) ---------------|
         |                                        |
         |  ---------- EOT (Done) --------------->|
         |                                        |
         |<--------- ACK (Goodbye) ---------------|
         |                                        |

================================================================================
[ Error Recovery with NAK ]
================================================================================

    Sender                                  Receiver
      |                                        |
      |  -------- SYN SYN STX DATA ETX ------->|
      |                                        | (BCC Error!)
      |<--------- NAK (Please resend) ---------|
      |                                        |
      |  -------- SYN SYN STX DATA ETX ------->| (Retransmit)
      |                                        |
      |          (BCC OK)                      |
      |<--------- ACK (Data OK) ---------------|
      |                                        |

================================================================================
[ Line Discipline State Machine ]
================================================================================

                          +-------+
                          | IDLE  |
                          +-------+
                              |
                         ENQ Tx|
                              v
    +-------+  Timeout   +-------+  ACK Rx   +-------+
    | IDLE  |<-----------| SETUP |--------->| XMIT  |
    +-------+            +-------+          +-------+
                              ^                  |
                              |                  | Data Tx
                         NAK Rx|                  v
                              |            +-------+
                              +-----------| WAIT  |
                                 Retry    +-------+
                                              |
                                         ACK Rx|
                                              v
                                         +-------+
                                         | XMIT  | (Continue)
                                         +-------+
                                              |
                                         Done  |
                                              v
                                         +-------+  ACK Rx  +-------+
                                         | TERM  |-------->| IDLE  |
                                         +-------+         +-------+
                                            |
                                       EOT Tx|
                                            v
```

### 심층 동작 원리: ENQ/ACK/NAK/EOT 상세

**1. ENQ (Enquiry, 0x05)**:
```
목적: 수신측의 준비 상태 확인

송신측 동작:
    1. ENQ 전송
    2. 타이머 시작 (T1: 응답 대기 시간)
    3. ACK 수신 대기

수신측 동작:
    1. ENQ 수신
    2. 버퍼 상태 확인
    3. 준비 완료 시 ACK 응답
    4. 준비 미완료 시 NAK 또는 무응답

타임아웃 처리:
    - T1 내 ACK 미수신 → ENQ 재전송
    - 최대 재시도 횟수 초과 → 링크 설정 실패
```

**2. ACK (Acknowledge, 0x06)**:
```
목적: 긍정 응답 - 데이터 정상 수신 확인

응답 대상:
    - ENQ: 수신 준비 완료
    - 데이터: 정상 수신 및 오류 없음

BSC의 ACK 형태:
    - ACK 0: 짝수 번째 블록 ACK (DLE 0)
    - ACK 1: 홀수 번째 블록 ACK (DLE 1)
    - 교대 사용으로 중복/손실 검출

ACK 0/1 번갈아 사용:
    Block 1 → ACK 0 → Block 2 → ACK 1 → Block 3 → ACK 0 ...
```

**3. NAK (Negative Acknowledge, 0x15)**:
```
목적: 부정 응답 - 오류 감지 또는 수신 거부

응답 대상:
    - ENQ: 수신 준비 불가 (버퍼 가득 참)
    - 데이터: 오류 감지 (BCC/CRC 불일치)

NAK 수신 시 송신측 동작:
    1. 해당 블록 재전송
    2. 재시도 카운터 증가
    3. 최대 재시도 초과 시 EOT 후 종료

BCC (Block Check Character):
    - 수신측에서 계산한 BCC와 수신된 BCC 비교
    - 불일치 시 NAK 응답
```

**4. EOT (End of Transmission, 0x04)**:
```
목적: 전송 종료 및 링크 해제

사용 시점:
    - 모든 데이터 전송 완료
    - 치명적 오류로 인한 전송 중단
    - 타임아웃 초과로 인한 링크 포기

EOT 송신 후:
    - 양측 모두 IDLE 상태로 복귀
    - 회선 자원 해제
    - 다음 ENQ 대기
```

### 핵심 코드: 회선 제어 프로토콜 구현

```python
"""
회선 제어 규약(Line Discipline) 시뮬레이션
ENQ/ACK/NAK/EOT 기반 BSC 스타일 통신 구현
"""

import enum
import time
import random
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from collections import deque


class ControlChar(enum.IntEnum):
    """ASCII 제어 문자"""
    SOH = 0x01    # Start of Header
    STX = 0x02    # Start of Text
    ETX = 0x03    # End of Text
    EOT = 0x04    # End of Transmission
    ENQ = 0x05    # Enquiry
    ACK = 0x06    # Acknowledge
    DLE = 0x10    # Data Link Escape
    NAK = 0x15    # Negative Acknowledge
    SYN = 0x16    # Synchronous Idle


class LineState(enum.Enum):
    """회선 제어 상태"""
    IDLE = "IDLE"
    SETUP = "SETUP"
    TRANSMIT = "TRANSMIT"
    WAIT_ACK = "WAIT_ACK"
    TERMINATE = "TERMINATE"


@dataclass
class BSCFrame:
    """BSC 프레임"""
    sync_bytes: bytes = bytes([ControlChar.SYN, ControlChar.SYN])
    data: bytes = b''
    block_check: bytes = b''

    def __post_init__(self):
        if not self.block_check:
            self.block_check = self._calculate_bcc()

    def _calculate_bcc(self) -> bytes:
        """BCC (Block Check Character) 계산 - LRC 방식"""
        lrc = 0
        for byte in self.data:
            lrc ^= byte
        return bytes([lrc])

    def to_bytes(self) -> bytes:
        """프레임 직렬화"""
        return (self.sync_bytes +
                bytes([ControlChar.STX]) +
                self.data +
                bytes([ControlChar.ETX]) +
                self.block_check)


@dataclass
class LineConfig:
    """회선 설정"""
    max_retries: int = 3
    timeout_ms: int = 1000
    error_rate: float = 0.05  # 5% 에러율


class LineController:
    """
    회선 제어기
    ENQ/ACK/NAK/EOT 기반 통신 제어
    """

    def __init__(self, name: str, config: LineConfig):
        self.name = name
        self.config = config
        self.state = LineState.IDLE
        self.retry_count = 0
        self.ack_sequence = 0  # ACK 0/1 교대

        # 통계
        self.stats = {
            'frames_sent': 0,
            'frames_received': 0,
            'retries': 0,
            'errors': 0,
            'bytes_transferred': 0
        }

    def send_enq(self) -> Tuple[bytes, bool]:
        """ENQ 전송"""
        print(f"[{self.name}] ENQ 전송 (수신 준비 확인)")
        self.state = LineState.SETUP
        return bytes([ControlChar.ENQ]), True

    def receive_enq(self) -> bytes:
        """ENQ 수신 처리"""
        print(f"[{self.name}] ENQ 수신 - 수신 준비 완료")
        return bytes([ControlChar.ACK])

    def send_data(self, data: bytes) -> Tuple[BSCFrame, bool]:
        """데이터 프레임 전송"""
        frame = BSCFrame(data=data)
        self.state = LineState.WAIT_ACK
        self.stats['frames_sent'] += 1
        self.stats['bytes_transferred'] += len(data)
        print(f"[{self.name}] 데이터 전송: {len(data)} bytes")
        return frame, True

    def receive_frame(self, frame: BSCFrame) -> Tuple[bytes, bool]:
        """프레임 수신 및 검증"""
        self.stats['frames_received'] += 1

        # 에러 시뮬레이션
        if random.random() < self.config.error_rate:
            print(f"[{self.name}] 프레임 수신 - BCC 오류!")
            self.stats['errors'] += 1
            return bytes([ControlChar.NAK]), False

        # BCC 검증
        expected_bcc = frame._calculate_bcc()
        if frame.block_check != expected_bcc:
            print(f"[{self.name}] 프레임 수신 - BCC 불일치")
            self.stats['errors'] += 1
            return bytes([ControlChar.NAK]), False

        # ACK 0/1 교대
        ack_char = ControlChar.DLE, ControlChar.ACK
        ack = bytes([ControlChar.DLE, 0x30 + self.ack_sequence])
        self.ack_sequence = 1 - self.ack_sequence  # 0 ↔ 1

        print(f"[{self.name}] 프레임 수신 성공 - ACK{1-self.ack_sequence} 전송")
        return ack, True

    def handle_ack(self, ack: bytes) -> bool:
        """ACK 처리"""
        if ControlChar.ACK in ack or ControlChar.DLE in ack:
            print(f"[{self.name}] ACK 수신 - 전송 성공")
            self.retry_count = 0
            self.state = LineState.TRANSMIT
            return True
        return False

    def handle_nak(self) -> Tuple[bool, int]:
        """NAK 처리"""
        print(f"[{self.name}] NAK 수신 - 재전송 필요")
        self.retry_count += 1
        self.stats['retries'] += 1

        if self.retry_count >= self.config.max_retries:
            print(f"[{self.name}] 최대 재시도 초과 - 링크 종료")
            return False, -1

        return True, self.retry_count

    def send_eot(self) -> bytes:
        """EOT 전송"""
        print(f"[{self.name}] EOT 전송 - 통신 종료")
        self.state = LineState.TERMINATE
        return bytes([ControlChar.EOT])

    def receive_eot(self) -> bytes:
        """EOT 수신"""
        print(f"[{self.name}] EOT 수신 - 통신 종료")
        self.state = LineState.IDLE
        return bytes([ControlChar.ACK])


def simulate_bsc_communication():
    """
    BSC 스타일 통신 시뮬레이션
    """
    config = LineConfig(max_retries=3, timeout_ms=1000, error_rate=0.1)

    sender = LineController("Sender", config)
    receiver = LineController("Receiver", config)

    # 전송할 데이터
    data_blocks = [
        b'Hello, this is block 1 of test data.',
        b'This is block 2 with more content.',
        b'Final block 3 completes the transmission.',
    ]

    print("=" * 60)
    print("BSC (Binary Synchronous Communication) 시뮬레이션")
    print("=" * 60)

    # 1. 링크 설정 (ENQ/ACK)
    print("\n[링크 설정 단계]")
    enq, _ = sender.send_enq()
    ack = receiver.receive_enq()
    sender.handle_ack(ack)

    # 2. 데이터 전송
    print("\n[데이터 전송 단계]")
    for i, data in enumerate(data_blocks):
        print(f"\n--- 블록 {i+1} 전송 ---")
        success = False

        while not success:
            # 데이터 전송
            frame, _ = sender.send_data(data)

            # 수신 (에러 시뮬레이션 포함)
            response, success = receiver.receive_frame(frame)

            if success:
                sender.handle_ack(response)
            else:
                retry, count = sender.handle_nak()
                if not retry:
                    print("전송 실패 - 링크 종료")
                    sender.send_eot()
                    return

        time.sleep(0.1)  # 전송 간격

    # 3. 링크 해제 (EOT)
    print("\n[링크 해제 단계]")
    eot = sender.send_eot()
    receiver.receive_eot()

    # 통계 출력
    print("\n" + "=" * 60)
    print("전송 통계")
    print("=" * 60)
    print(f"전송된 프레임: {sender.stats['frames_sent']}")
    print(f"수신된 프레임: {receiver.stats['frames_received']}")
    print(f"재시도 횟수: {sender.stats['retries']}")
    print(f"오류 횟수: {receiver.stats['errors']}")
    print(f"전송 바이트: {sender.stats['bytes_transferred']}")


def print_control_chars_table():
    """제어 문자 표 출력"""
    print("\n" + "=" * 60)
    print("ASCII 통신 제어 문자")
    print("=" * 60)
    print(f"{'문자':<6} {'Hex':<6} {'명칭':<25} {'용도'}")
    print("-" * 60)

    control_chars = [
        (ControlChar.SOH, "SOH", "Start of Header", "헤더 시작"),
        (ControlChar.STX, "STX", "Start of Text", "본문 시작"),
        (ControlChar.ETX, "ETX", "End of Text", "본문 종료"),
        (ControlChar.EOT, "EOT", "End of Transmission", "전송 종료"),
        (ControlChar.ENQ, "ENQ", "Enquiry", "상태 질의"),
        (ControlChar.ACK, "ACK", "Acknowledge", "긍정 응답"),
        (ControlChar.DLE, "DLE", "Data Link Escape", "제어 확장"),
        (ControlChar.NAK, "NAK", "Negative Acknowledge", "부정 응답"),
        (ControlChar.SYN, "SYN", "Synchronous Idle", "동기 유지"),
    ]

    for char, name, full_name, purpose in control_chars:
        print(f"{name:<6} 0x{char:02X}  {full_name:<25} {purpose}")


if __name__ == "__main__":
    # 제어 문자 테이블
    print_control_chars_table()

    # 통신 시뮬레이션
    simulate_bsc_communication()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 회선 제어 프로토콜 진화

| 프로토콜 | 시대 | 제어 방식 | 프레임 구조 | 오류 제어 | 특징 |
|---------|------|----------|------------|----------|------|
| **BSC** | 1960s | 문자 지향 | SYN SYN STX...ETX BCC | Stop-and-Wait ARQ | IBM 메인프레임 |
| **SDLC** | 1970s | 비트 지향 | Flag Addr Ctrl Data FCS Flag | Go-Back-N ARQ | IBM SNA |
| **HDLC** | 1970s | 비트 지향 | Flag Addr Ctrl Data FCS Flag | GBN/SR ARQ | ISO 표준 |
| **PPP** | 1990s | 바이트 지향 | Flag Addr Ctrl Proto Data FCS | 비트 오류 검출 | 인터넷 접속 |
| **TCP** | 1980s~ | 세그먼트 | SYN/FIN/ACK 플래그 | 슬라이딩 윈도우 | 인터넷 표준 |

### ACK/NAK vs 현대적 피드백

| 특성 | BSC ACK/NAK | TCP ACK | 현대 ARQ |
|------|-------------|---------|----------|
| **응답 방식** | 즉시 응답 | 누적 ACK | 선택적 ACK |
| **윈도우** | 없음 (1:1) | 슬라이딩 윈도우 | 동적 윈도우 |
| **지연 허용** | 낮음 | 높음 | 적응적 |
| **효율성** | 낮음 | 높음 | 매우 높음 |
| **복잡도** | 단순 | 중간 | 복잡 |

### 과목 융합 관점 분석

**1. 운영체제와의 융합**:
   - TCP/IP 스택의 소켓 연결 설정 (3-way handshake)은 ENQ/ACK의 현대적 진화
   - 커널의 네트워크 버퍼 관리 = 수신 준비 상태 관리

**2. 데이터 링크 계층과의 융합**:
   - HDLC의 RR(Receiver Ready)/RNR(Receiver Not Ready) = ACK/NAK 확장
   - PPP의 LCP(Link Control Protocol) = 링크 설정/해제 메커니즘

**3. 산업용 통신과의 융합**:
   - Modbus RTU의 응답 프레임 = ACK/NAK 구조
   - 산업용 시리얼 프로토콜에서 여전히 ENQ/ACK 사용

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 레거시 시스템과의 연동

**문제 상황**: 레거시 BSC 기반 메인프레임과 현대 TCP/IP 시스템 간 게이트웨이를 구축해야 합니다.

**기술사의 전략적 의사결정**:

1. **프로토콜 변환 계층 설계**:
   - BSC ENQ → TCP SYN 매핑
   - BSC ACK/NAK → TCP ACK/RST 매핑
   - BSC Block → TCP Segment 분할

2. **타이밍 조정**:
   - BSC: 수 ms 응답 요구
   - TCP: 수백 ms 허용
   - 버퍼링으로 타이밍 차이 흡수

3. **에러 처리 매핑**:
   - BSC NAK → TCP 재전송 요청
   - BSC EOT → TCP FIN

### 도입 시 고려사항 체크리스트

| 항목 | 확인 내용 | 중요도 |
|------|----------|--------|
| **타임아웃 설정** | 레거시와 현대 시스템 간 타이밍 호환 | 상 |
| **문자 인코딩** | EBCDIC ↔ ASCII 변환 | 상 |
| **BCC 알고리즘** | LRC/CRC 호환성 | 중 |
| **블록 크기** | MTU와 블록 크기 매핑 | 중 |
| **동기 방식** | 동기식 vs 비동기식 처리 | 상 |

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - 무한 재시도**:
  최대 재시도 횟수 없이 NAK 시 계속 재전송하면 네트워크 폭주 유발.

- **안티패턴 2 - ACK 손실 무시**:
  ACK가 손실되면 송신측은 재전송하지만 수신측은 중복 프레임을 새 프레임으로 오인 가능.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | 내용 | 정량적 지표 |
|----------|------|------------|
| **신뢰성** | ACK/NAK로 오류 검출 및 복구 | BER 10⁻⁹ 달성 |
| **호환성** | 레거시 시스템 연동 가능 | 게이트웨이 구축 비용 50% 절감 |
| **단순성** | 구현 용이, 디버깅 간편 | 개발 시간 30% 단축 |
| **교육 가치** | 통신 원리 이해에 최적 | 기본 개념 습득 효율화 |

### 미래 전망 및 진화 방향

- **IoT 경량 프로토콜**: CoAP와 같은 경량 프로토콜에서 ACK/NAK 구조 재사용
- **산업용 통신**: Modbus, PROFIBUS 등에서 지속적 사용
- **디지털 트윈**: 레거시 시스템 디지털화를 위한 프로토콜 분석 필수

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **IBM GA27-3004** | IBM | BSC (Binary Synchronous Communication) |
| **ISO 1745** | ISO | 정보 처리 - 데이터 통신 시스템의 기본 모드 제어 절차 |
| **ITU-T V.24** | ITU-T | DTE-DCE 인터페이스 회로 정의 |

---

## 관련 개념 맵 (Knowledge Graph)
- [ARQ 프로토콜](./208_stop_and_wait_arq.md) - ACK/NAK 기반 재전송
- [HDLC](./216_hdlc_protocol.md) - BSC의 후속 비트 지향 프로토콜
- [TCP 3-way 핸드셰이크](../2_transport/416_tcp_handshake.md) - ENQ/ACK의 현대적 진화
- [오류 검출](./194_crc_cyclic_redundancy.md) - BCC/CRC 오류 검출
- [흐름 제어](./213_flow_control.md) - ACK 기반 흐름 제어

---

## 어린이를 위한 3줄 비유 설명
1. **ENQ**는 **'들리세요?'**라고 묻는 거예요. 통화를 시작하기 전에 상대방이 준비되었는지 확인하는 거죠.
2. **ACK/NAK**는 **'응, 알았어!/다시 말해줘!'**예요. 내가 한 말을 잘 들었는지, 아니면 뭔가 잘못 들었는지 알려주는 거예요.
3. **EOT**는 **'이제 끝내자!'**예요. 할 말 다 했으니 통화를 끊자고 알리는 거예요. 이렇게 규칙을 정해서 대화하면 오해가 줄어들어요!
