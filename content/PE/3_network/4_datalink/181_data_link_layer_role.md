+++
title = "181. 데이터 링크 계층의 역할 (Data Link Layer Functions)"
description = "OSI 7계층 모델의 데이터 링크 계층이 수행하는 프레이밍, 흐름 제어, 오류 제어, 회선 제어의 핵심 기능을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["DataLinkLayer", "Framing", "FlowControl", "ErrorControl", "LLC", "MAC", "OSI"]
categories = ["studynotes-3_network"]
+++

# 181. 데이터 링크 계층의 역할 (Data Link Layer Functions)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 링크 계층은 물리 계층이 제공하는 비트 전송 서비스 위에 신뢰성 있는 프레임 전송을 보장하는 계층으로, 프레이밍, 흐름 제어, 오류 제어, 회선 제어의 4대 핵심 기능을 수행합니다.
> 2. **가치**: 물리적 전송 오류를 검출/정정하고 수신측 버퍼 오버플로우를 방지하며, 매체 접근을 제어하여 상위 네트워크 계층에 투명하고 신뢰성 있는 링크 서비스를 제공합니다.
> 3. **융합**: 이더넷(MAC), WiFi(802.11), PPP, HDLC 등 모든 2계층 프로토콜의 기반이며, 소프트웨어 정의 네트워킹(SDN)과 네트워크 가상화에서도 데이터 링크 계층의 개념이 확장되어 적용됩니다.

---

## Ⅰ. 개요 (Context & Background)

데이터 링크 계층(Data Link Layer)은 **OSI 7계층 모델의 제2계층**으로, 물리 계층(1계층)과 네트워크 계층(3계층) 사이에서 신뢰성 있는 데이터 전송을 담당합니다. 이 계층은 **노드 대 노드(Node-to-Node)** 통신을 제공하며, 네트워크 장비 간 직접 연결된 링크에서의 데이터 전송을 관리합니다.

### 데이터 링크 계층의 4대 핵심 기능

| 기능 | 영문명 | 핵심 역할 | 주요 기법 |
|------|--------|----------|----------|
| **프레이밍** | Framing | 비트 스트림을 프레임 단위로 구분 | 플래그, 바이트 카운트, 비트 스터핑 |
| **흐름 제어** | Flow Control | 수신측 처리 능력에 맞춘 전송 속도 조절 | 정지-대기, 슬라이딩 윈도우 |
| **오류 제어** | Error Control | 전송 오류의 검출 및 정정 | ARQ, FEC, CRC |
| **회선 제어** | Link Control | 통신 세션 설정 및 매체 접근 제어 | ENQ/ACK, CSMA/CD, 토큰 패싱 |

### 데이터 링크 계층의 서브 계층

```
+---------------------------+
|       네트워크 계층 (3)    |
+---------------------------+
|   LLC (Logical Link       |  <- IEEE 802.2
|        Control)           |     흐름/오류 제어
+---------------------------+
|   MAC (Media Access       |  <- IEEE 802.3/11/5
|        Control)           |     매체 접근 제어
+---------------------------+
|       물리 계층 (1)        |
+---------------------------+
```

**💡 비유**: 데이터 링크 계층은 **'우체국의 등기 우편 처리'**와 같습니다.
- **프레이밍**: 편지를 봉투에 넣고 주소를 적는 것
- **흐름 제어**: 받는 사람이 처리할 수 있는 만큼만 편지를 보내는 것
- **오류 제어**: 편지가 찢어지거나 잃어버렸는지 확인하고 재발송
- **회선 제어**: 누가 먼저 편지를 보낼지 순서 정하기

**등장 배경 및 발전 과정**:

1. **초기 데이터통신의 신뢰성 문제 (1960년대 이전)**:
   초기 통신 시스템은 단순히 비트를 전송할 뿐, 오류 검출이나 흐름 제어가 없었습니다. 전송 오류는 빈번했고, 수신측 버퍼 오버플로우로 인한 데이터 손실이 일상적이었습니다.

2. **BSC와 HDLC의 표준화 (1960~70년대)**:
   IBM의 BSC(Binary Synchronous Communication)와 ISO의 HDLC(High-Level Data Link Control)가 데이터 링크 제어의 표준으로 자리잡았습니다. 이들은 프레이밍, 흐름 제어, 오류 제어를 체계화했습니다.

3. **LAN의 등장과 IEEE 802 표준 (1980년대)**:
   이더넷(IEEE 802.3), 토큰 링(IEEE 802.5), 무선 LAN(IEEE 802.11) 등 다양한 LAN 기술이 등장하면서, 데이터 링크 계층은 LLC와 MAC으로 분화되었습니다.

4. **현대적 진화 (1990년대~현재)**:
   고속 이더넷(1G~400G), WiFi(802.11a/b/g/n/ac/ax/be), 그리고 데이터 센터용 프로토콜(Fibre Channel, InfiniBand)로 진화했습니다. SDN과 VXLAN 같은 오버레이 기술에서도 데이터 링크 계층의 개념이 가상화되어 적용됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 데이터 링크 계층의 구조

```ascii
================================================================================
[ Data Link Layer Architecture ]
================================================================================

   송신측 (Sender)                                      수신측 (Receiver)
   =============                                      ===============

   네트워크 계층                                        네트워크 계층
        |                                                   ^
        v                                                   |
   +---------------+                               +---------------+
   | 1. 프레이밍   |                               | 4. 프레임     |
   |   - 헤더 추가 |                               |    분해       |
   |   - 트레일러  |                               |    - 헤더 제거|
   |   (FCS 추가)  |                               |    - FCS 검증 |
   +---------------+                               +---------------+
        |                                                   ^
        v                                                   |
   +---------------+                               +---------------+
   | 2. 흐름 제어  |                               | 3. 흐름 제어  |
   |   - 윈도우    |    <---- ACK/NACK ----        |   - 버퍼 관리 |
   |   - 대기      |                               |   - ACK 생성  |
   +---------------+                               +---------------+
        |                                                   ^
        v                                                   |
   +---------------+                               +---------------+
   | 오류 제어     |    <---- 재전송 요청 ----      | 오류 제어     |
   | - CRC 계산    |                               | - CRC 검증    |
   | - ARQ 수행    |                               | - ARQ 처리    |
   +---------------+                               +---------------+
        |                                                   ^
        v                                                   |
   물리 계층 =================> 비트 스트림 ============> 물리 계층

================================================================================
[ Data Link Layer Frame Structure ]
================================================================================

   일반적인 프레임 구조:

   +------+--------+--------+--------+----------+--------+------+
   | 플래그|  주소  |  제어  |  정보  |   데이터  |  FCS   |플래그 |
   | Flag | Address| Control|  Info  | Payload  |  CRC   | Flag |
   +------+--------+--------+--------+----------+--------+------+
     1B      1-2B     1-2B     가변      가변       2-4B    1B

   [필드별 상세]

   플래그 (Flag): 01111110 (HDLC) 또는 10101011 (이더넷 SFD)
   - 프레임 시작/끝 표시
   - 비트 스터핑으로 데이터 내 플래그와 구분

   주소 (Address):
   - 목적지/출발지 MAC 주소 (이더넷)
   - 명령/응답 식별 (HDLC)

   제어 (Control):
   - 프레임 유형 (I-Frame, S-Frame, U-Frame)
   - 순서 번호 (N(S), N(R))
   - P/F 비트 (Poll/Final)

   정보/데이터 (Information/Payload):
   - 상위 계층에서 전달받은 데이터
   - 가변 길이 (MTU 제한)

   FCS (Frame Check Sequence):
   - CRC-16 또는 CRC-32
   - 프레임 무결성 검증

================================================================================
[ Flow Control Mechanisms ]
================================================================================

   [1] 정지-대기 (Stop-and-Wait)

   송신측                          수신측
      |                               |
      |------- Frame 0 ----------->   |
      |        (대기)                 | (처리)
      |<------ ACK 0 --------------   |
      |                               |
      |------- Frame 1 ----------->   |
      |        (대기)                 | (처리)
      |<------ ACK 1 --------------   |

   효율 = 1 / (1 + 2a)
   여기서 a = 전파 지연 / 전송 시간

   문제: 대역폭이 클수록 효율 급감


   [2] 슬라이딩 윈도우 (Sliding Window)

   송신측 윈도우 (Window Size = 4)
   +---+---+---+---+---+---+---+---+
   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
   +---+---+---+---+---+---+---+---+
     ^   ^   ^   ^
     |--- 윈도우 ---|

   ACK 수신 시 윈도우 슬라이드:

   +---+---+---+---+---+---+---+---+
   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
   +---+---+---+---+---+---+---+---+
             ^   ^   ^   ^
             |--- 윈도우 ---|

   효율 = W / (1 + 2a)  (W: 윈도우 크기)
   W가 충분히 크면 효율 → 1

================================================================================
[ Error Control: ARQ Protocols ]
================================================================================

   [1] Stop-and-Wait ARQ

   - 타임아웃 시 단일 프레임 재전송
   - 구현 단순, 효율 낮음

   [2] Go-Back-N ARQ (GBN)

   송신측                          수신측
      |                               |
      |------- Frame 0 ----------->   |
      |------- Frame 1 ----------->   |
      |------- Frame 2 ---X-------->  |  (에러!)
      |------- Frame 3 ----------->   | (폐기: 순서 오류)
      |------- Frame 4 ----------->   | (폐기)
      |<------ NAK 2 --------------   |
      |                               |
      |------- Frame 2 ----------->   | (재전송)
      |------- Frame 3 ----------->   |
      |------- Frame 4 ----------->   |

   - 오류 프레임부터 모두 재전송
   - 수신측 버퍼 불필요, 대역폭 낭비


   [3] Selective Repeat ARQ (SR)

   송신측                          수신측
      |                               |
      |------- Frame 0 ----------->   |
      |------- Frame 1 ----------->   |
      |------- Frame 2 ---X-------->  |  (에러!)
      |------- Frame 3 ----------->   | (버퍼링)
      |------- Frame 4 ----------->   | (버퍼링)
      |<------ NAK 2 --------------   |
      |                               |
      |------- Frame 2 ----------->   | (재전송만)
      |<------ ACK 3,4 ------------   | (버퍼된 프레임 ACK)

   - 오류 프레임만 선택적 재전송
   - 수신측 버퍼링 필요, 효율 최고

================================================================================
```

### 데이터 링크 계층 서비스 프리미티브

| 서비스 유형 | 설명 | 예시 |
|------------|------|------|
| **비연결형 비확인** | 프레임 전송 후 확인 없음 | 이더넷 기본 모드 |
| **비연결형 확인** | 개별 프레임에 ACK 응답 | 802.11 ACK |
| **연결형** | 연결 설정-데이터 전송-연결 해제 | HDLC ABM |

### 핵심 코드: 데이터 링크 계층 시뮬레이터 (Python)

```python
import numpy as np
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Deque
from collections import deque
import random

class FrameType(Enum):
    """프레임 유형"""
    I_FRAME = "Information"    # 정보 프레임
    S_FRAME = "Supervisory"    # 감독 프레임
    U_FRAME = "Unnumbered"     # 비번호 프레임

class ARQType(Enum):
    """ARQ 유형"""
    STOP_WAIT = "StopAndWait"
    GO_BACK_N = "GoBackN"
    SELECTIVE_REPEAT = "SelectiveRepeat"

@dataclass
class Frame:
    """프레임 구조"""
    seq_num: int = 0
    ack_num: int = 0
    frame_type: FrameType = FrameType.I_FRAME
    data: bytes = b""
    fcs: int = 0

    def calculate_fcs(self) -> int:
        """FCS 계산 (CRC-16 간소화)"""
        crc = 0
        for byte in self.data:
            crc ^= byte
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        self.fcs = crc
        return crc

    def verify_fcs(self) -> bool:
        """FCS 검증"""
        return self.calculate_fcs() == self.fcs

@dataclass
class DataLinkConfig:
    """데이터 링크 설정"""
    window_size: int = 4
    max_seq: int = 7          # 3비트 시퀀스 번호
    frame_timeout: float = 2.0
    arq_type: ARQType = ARQType.GO_BACK_N
    error_rate: float = 0.0   # 프레임 에러율

class DataLinkSender:
    """데이터 링크 송신측"""

    def __init__(self, config: DataLinkConfig):
        self.config = config
        self.send_window: Deque[Frame] = deque(maxlen=config.window_size)
        self.send_base = 0      # 윈도우 시작
        self.next_seq = 0       # 다음 전송 시퀀스
        self.timer_running = False
        self.buffer: List[Frame] = []  # 전송 대기 버퍼

    def send_data(self, data: bytes) -> Frame:
        """데이터 전송"""
        if (self.next_seq - self.send_base) % (self.config.max_seq + 1) >= self.config.window_size:
            return None  # 윈도우 가득참

        frame = Frame(
            seq_num=self.next_seq,
            data=data,
            frame_type=FrameType.I_FRAME
        )
        frame.calculate_fcs()

        self.buffer.append(frame)
        self.send_window.append(frame)
        self.next_seq = (self.next_seq + 1) % (self.config.max_seq + 1)

        return frame

    def receive_ack(self, ack_num: int) -> List[Frame]:
        """ACK 수신 처리"""
        acked_frames = []

        # 윈도우 슬라이드
        while self.send_base != ack_num:
            if self.send_window:
                acked_frames.append(self.send_window.popleft())
            self.send_base = (self.send_base + 1) % (self.config.max_seq + 1)

        return acked_frames

    def timeout_handler(self) -> List[Frame]:
        """타임아웃 처리 (재전송)"""
        if self.config.arq_type == ARQType.STOP_WAIT:
            return [self.buffer[-1]] if self.buffer else []
        elif self.config.arq_type == ARQType.GO_BACK_N:
            # 윈도우 내 모든 프레임 재전송
            return list(self.send_window)
        else:  # SELECTIVE_REPEAT
            return list(self.send_window)

class DataLinkReceiver:
    """데이터 링크 수신측"""

    def __init__(self, config: DataLinkConfig):
        self.config = config
        self.expected_seq = 0
        self.receive_buffer: dict = {}  # SR용 버퍼
        self.received_frames: List[Frame] = []

    def receive_frame(self, frame: Frame) -> Optional[int]:
        """프레임 수신 처리"""
        # 에러 시뮬레이션
        if random.random() < self.config.error_rate:
            return None  # 에러, NAK 전송

        # FCS 검증
        if not frame.verify_fcs():
            return None

        if self.config.arq_type == ARQType.STOP_WAIT:
            return self._process_stop_wait(frame)
        elif self.config.arq_type == ARQType.GO_BACK_N:
            return self._process_gbn(frame)
        else:
            return self._process_sr(frame)

    def _process_stop_wait(self, frame: Frame) -> Optional[int]:
        """Stop-and-Wait 처리"""
        if frame.seq_num == self.expected_seq:
            self.received_frames.append(frame)
            self.expected_seq = (self.expected_seq + 1) % 2
            return frame.seq_num
        return None

    def _process_gbn(self, frame: Frame) -> Optional[int]:
        """Go-Back-N 처리"""
        if frame.seq_num == self.expected_seq:
            self.received_frames.append(frame)
            self.expected_seq = (self.expected_seq + 1) % (self.config.max_seq + 1)
            return frame.seq_num
        else:
            # 순서 오류: 폐기하고 이전 ACK 재전송
            return (self.expected_seq - 1) % (self.config.max_seq + 1)

    def _process_sr(self, frame: Frame) -> Optional[int]:
        """Selective Repeat 처리"""
        # 버퍼에 저장
        self.receive_buffer[frame.seq_num] = frame

        # 순차적으로 수신 완료된 프레임 확인
        ack_num = None
        while self.expected_seq in self.receive_buffer:
            self.received_frames.append(self.receive_buffer.pop(self.expected_seq))
            self.expected_seq = (self.expected_seq + 1) % (self.config.max_seq + 1)

        return self.expected_seq

class DataLinkSimulator:
    """데이터 링크 시뮬레이터"""

    def __init__(self, config: DataLinkConfig):
        self.config = config
        self.sender = DataLinkSender(config)
        self.receiver = DataLinkReceiver(config)

    def simulate_transmission(self, n_frames: int = 20) -> dict:
        """전송 시뮬레이션"""
        frames_sent = 0
        frames_acked = 0
        retransmissions = 0

        for i in range(n_frames):
            data = f"Frame_{i}".encode()
            frame = self.sender.send_data(data)

            if frame is None:
                # 윈도우 가득참, ACK 대기
                continue

            frames_sent += 1

            # 전송 시뮬레이션
            ack = self.receiver.receive_frame(frame)

            if ack is not None:
                acked = self.sender.receive_ack(ack)
                frames_acked += len(acked)
            else:
                # 재전송
                retrans_frames = self.sender.timeout_handler()
                retransmissions += len(retrans_frames)

        throughput = frames_acked / frames_sent if frames_sent > 0 else 0

        return {
            'frames_sent': frames_sent,
            'frames_acked': frames_acked,
            'retransmissions': retransmissions,
            'throughput': throughput,
            'efficiency': frames_acked / n_frames
        }

def run_data_link_demo():
    """데이터 링크 데모"""
    print("=" * 70)
    print("데이터 링크 계층 시뮬레이션")
    print("=" * 70)

    for arq_type in [ARQType.STOP_WAIT, ARQType.GO_BACK_N, ARQType.SELECTIVE_REPEAT]:
        config = DataLinkConfig(
            window_size=4 if arq_type != ARQType.STOP_WAIT else 1,
            arq_type=arq_type,
            error_rate=0.1
        )

        simulator = DataLinkSimulator(config)
        result = simulator.simulate_transmission(n_frames=50)

        print(f"\n--- {arq_type.value} ---")
        print(f"전송 프레임: {result['frames_sent']}")
        print(f"ACK 프레임: {result['frames_acked']}")
        print(f"재전송: {result['retransmissions']}")
        print(f"처리율: {result['throughput']:.4f}")
        print(f"효율: {result['efficiency']:.4f}")

if __name__ == "__main__":
    run_data_link_demo()
