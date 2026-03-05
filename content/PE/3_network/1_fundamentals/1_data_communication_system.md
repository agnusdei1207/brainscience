+++
title = "001. 데이터통신 시스템 구성요소 (Data Communication System Components)"
description = "DTE, DCE, CCU로 구성된 데이터통신 시스템의 핵심 구조와 상호동작 메커니즘을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["DTE", "DCE", "CCU", "DataCommunication", "Network", "RS-232C", "FEP"]
categories = ["studynotes-3_network"]
+++

# 001. 데이터통신 시스템 구성요소

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터통신 시스템은 데이터를 생성·처리하는 단말장치(DTE), 데이터를 전송 신호로 변환하는 회선종단장치(DCE), 그리고 통신 과정을 제어하는 통신제어장치(CCU)의 유기적 결합으로 구성되는 계층적 아키텍처입니다.
> 2. **가치**: 각 구성요소의 명확한 역할 분담을 통해 물리적 신호 변환과 논리적 데이터 처리를 분리하여, 이기종 장비 간의 상호 운용성을 보장하고 통신 품질을 최적화합니다.
> 3. **융합**: 현대 클라우드 및 IoT 환경에서 DTE는 스마트 센서와 서버로, DCE는 모뎀과 네트워크 인터페이스 카드(NIC)로, CCU는 프로토콜 스택과 드라이버로 진화하여 소프트웨어 정의 통신의 기반이 됩니다.

---

## Ⅰ. 개요 (Context & Background)

데이터통신 시스템(Data Communication System)은 정보를 생성하는 송신측부터 정보를 수신하는 수신측까지, 데이터가 안정적이고 효율적으로 전달되도록 하는 하드웨어와 소프트웨어의 통합 체계입니다. 이 시스템은 크게 데이터를 생산하고 소비하는 **DTE(Data Terminal Equipment)**, 데이터를 전송 매체에 적합한 신호로 변환하는 **DCE(Data Circuit-terminating Equipment)**, 그리고 통신 과정 전반을 제어하고 오류를 관리하는 **CCU(Communication Control Unit)**로 구성됩니다.

**💡 비유**: 데이터통신 시스템은 **'국제 우편 시스템'**과 같습니다.
- **DTE(단말장치)**는 편지를 쓰고 읽는 사람(송수신자)입니다. 편지의 내용(데이터)을 생성하고 최종적으로 소비합니다.
- **DCE(회선종단장치)**는 우체국의 분류기와 우편 트럭입니다. 편지를 봉투에 넣고(인코딩), 트럭에 싣고(변조), 도로(전송 매체)를 통해 이동시킵니다.
- **CCU(통신제어장치)**는 우체국의 관리 시스템입니다. 우편 요금을 확인하고(흐름 제어), 주소가 틀리지 않았는지 검사하며(오류 제어), 배송 경로를 지정합니다(라우팅).

**등장 배경 및 발전 과정**:
1. **초기 통신의 혼란 (1960년대 이전)**: 각 통신 장비 제조사가 독자적인 인터페이스와 프로토콜을 사용하여 서로 다른 장비 간 연결이 거의 불가능했습니다. 데이터 처리 장치와 전송 장치의 경계도 모호했습니다.
2. **표준화의 탄생**: EIA(Electronic Industries Alliance)와 ITU-T(국제전기통신연합)가 RS-232C, V.24 등의 표준을 제정하면서 DTE와 DCE의 인터페이스를 명확히 정의했습니다. 이는 벤더 중립적 통신의 시초가 되었습니다.
3. **현대적 진화**: 오늘날 DTE는 컴퓨터, 스마트폰, IoT 센서 등으로 확장되었고, DCE는 모뎀, DSU, CSU, NIC 등 다양한 형태로 분화되었습니다. CCU의 기능은 운영체제 커널의 네트워크 스택과 전용 프로토콜 프로세서로 분산 구현됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 상세 역할 | 내부 동작 메커니즘 | 관련 표준/기술 | 비유 |
|---------|------|----------|-------------------|---------------|------|
| **DTE** | Data Terminal Equipment (단말장치) | 데이터 생성, 처리, 저장 및 사용자 인터페이스 제공 | CPU, 메모리, 스토리지, 애플리케이션 소프트웨어 동작 | RS-232C, USB, Ethernet | 편지 작성자 |
| **DCE** | Data Circuit-terminating Equipment (회선종단장치) | 디지털 데이터를 전송 매체에 적합한 신호로 변환 및 복원 | 부호화(Encoding), 변조(Modulation), 동기화(Sync), 증폭 | V.35, RS-449, X.21, DSU/CSU | 우편 분류기/트럭 |
| **CCU** | Communication Control Unit (통신제어장치) | 통신 세션 제어, 오류 검출/정정, 흐름 제어, 프로토콜 처리 | HDLC/SDLC 컨트롤러, CRC 연산, 버퍼 관리, 인터럽트 처리 | ISO 1745, IBM BSC | 우체국 관리자 |
| **FEP** | Front-End Processor (전위처리기) | 호스트 컴퓨터의 통신 부하 분산 및 프로토콜 변환 | 폴링, 코드 변환, 메시지 조립/분해, 암호화 | SNA, DECnet | 비서 |
| **MUX** | Multiplexer (다중화기) | 다수의 저속 채널을 하나의 고속 채널로 통합 | TDM, FDM, STDM, 셀 어셈블리 | T1/E1, SONET/SDH | 우편물 묶음 배송 |

### 정교한 구조 다이어그램: 데이터통신 시스템 계층 구조

```ascii
================================================================================
[ Data Communication System Architecture: End-to-End Flow ]
================================================================================

[ 송신측 (Sender Side) ]                              [ 수신측 (Receiver Side) ]

+------------------+                                  +------------------+
|      사용자      |                                  |      사용자      |
+--------|---------+                                  +--------|---------+
         | 데이터                                            | 데이터
         v                                                   v
+------------------+         +------------------+      +------------------+
|  DTE (단말장치)  |         |  통신 회선       |      |  DTE (단말장치)  |
| +--------------+ |         |   (Physical      |      | +--------------+ |
| | Application  | |         |    Medium)       |      | | Application  | |
| | (응용 프로그램)| |========>|  꼬임쌍선/동축/  |=====>| | (응용 프로그램)| |
| +--------------+ |  디지털  |  광섬유/무선     | 디지털| +--------------+ |
| | OS Network   | |  비트    |                  | 비트  | | OS Network   | |
| | Stack (CCU)  | | 스트림   +------------------+ 스트림| | Stack (CCU)  | |
| +--------------+ |                                                |
+--------|---------+                                                |
         | 데이터 패킷                                              |
         v                                                   ^
+------------------+                                              |
|  DCE (회선종단)  |                                              |
| +--------------+ |         +------------------+                |
| | Line Encoder | |         |  중계기/증폭기   |                |
| | (부호화기)    |=========>|  (Repeater)      |================
| +--------------+ | 아날로그 +------------------+ 아날로그
| | Modulator    | | 신호           ^                     신호  |
| | (변조기)      | |               | 전기적/광학적             |
| +--------------+ |               | 신호 변환                |
+--------|---------+               v                          |
         |                                       +------------------+
         | 물리적 신호                           |  DCE (회선종단)  |
         v                                       | +--------------+ |
+------------------+                              | | Demodulator  | |
|  DCE 인터페이스  |                              | | (복조기)      | |
|  (RS-232C, V.35) |                              | +--------------+ |
+------------------+                              | | Line Decoder | |
                                                  | | (복호화기)    | |
                                                  | +--------------+ |
                                                  +------------------+
================================================================================

[ DTE-DCE Interface Protocol Stack ]
+------------------+
| Application Layer| <-- DTE 영역 (데이터 처리)
+------------------+
| Transport Layer  | <-- CCU 기능 (오류/흐름 제어)
+------------------+
| Network Layer    |
+------------------+
+==================+ <-- DTE-DCE 경계 (Physical Interface)
| Physical Layer   | <-- DCE 영역 (신호 변환)
+==================+
| Transmission     | <-- 전송 매체
| Medium           |
+==================+
```

### 심층 동작 원리: 데이터 전송 5단계 프로세스

1. **데이터 생성 및 패키징 (DTE → CCU)**:
   - 사용자 애플리케이션이 생성한 원시 데이터는 CCU(또는 OS 네트워크 스택)로 전달됩니다.
   - CCU는 데이터를 적절한 크기의 패킷으로 분할하고, 헤더(주소, 순서 번호 등)와 트레일러(오류 검출 코드)를 부착합니다.
   - HDLC, PPP 등의 데이터 링크 프로토콜에 따라 프레이밍(Framing)을 수행합니다.

2. **신호 변환 및 인코딩 (CCU → DCE)**:
   - 패키징된 디지털 비트 스트림이 DTE 인터페이스(RS-232C, V.35 등)를 통해 DCE로 전달됩니다.
   - DCE의 라인 인코더가 비트를 전송 매체에 적합한 전기적 신호(NRZ, Manchester 등)로 변환합니다.
   - 필요시 변조기(Modulator)가 아날로그 반송파에 데이터를 실어 변조(ASK, FSK, PSK, QAM)합니다.

3. **전송 매체 통과 및 중계**:
   - 변환된 신호는 꼬임쌍선, 동축케이블, 광섬유, 또는 무선 매체를 통해 전파됩니다.
   - 장거리 전송 시 중계기(Repeater)나 증폭기(Amplifier)가 신호를 재생하거나 증폭합니다.
   - 교환기(Switch)나 라우터가 패킷을 다음 홉(Hop)으로 포워딩합니다.

4. **신호 수신 및 복원 (DCE → CCU)**:
   - 수신측 DCE의 복조기(Demodulator)가 아날로그 신호에서 데이터를 추출(복조)합니다.
   - 라인 디코더가 전기적 신호를 다시 디지털 비트 스트림으로 변환합니다.
   - DCE는 동기화(Synchronization)를 통해 비트 경계를 식별하고, 클럭 복원을 수행합니다.

5. **오류 검사 및 데이터 처리 (CCU → DTE)**:
   - CCU는 수신된 프레임의 CRC(Cyclic Redundancy Check)를 계산하여 오류 여부를 검사합니다.
   - 오류가 없으면 응답(ACK)을 송신측에 회신하고, 오류가 있으면 재전송 요청(NAK)을 보냅니다.
   - 오류 없는 데이터는 순서 번호에 따라 재조립(Reassembly)된 후 애플리케이션에 전달됩니다.

### 핵심 코드: RS-232C 시리얼 통신 DTE-DCE 인터페이스 제어 (Python)

```python
import serial
import time
from enum import Enum

class RS232Signal(Enum):
    """RS-232C 제어 신호 정의"""
    DTR = serial.DTR   # Data Terminal Ready (DTE 준비 완료)
    RTS = serial.RTS   # Request To Send (송신 요청)
    CTS = serial.CTS   # Clear To Send (송신 허가 - DCE 응답)
    DSR = serial.DSR   # Data Set Ready (DCE 준비 완료)
    DCD = serial.CD    # Data Carrier Detect (반송파 감지)
    RI  = serial.RI    # Ring Indicator (호 착신 표시)

class DTEInterface:
    """
    DTE(Data Terminal Equipment) 인터페이스 제어 클래스
    RS-232C 하드웨어 핸드셰이킹 및 데이터 송수신 구현
    """
    def __init__(self, port: str, baudrate: int = 9600):
        self.serial_conn = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1.0,
            xonxoff=False,    # 소프트웨어 흐름 제어 비활성화
            rtscts=True       # 하드웨어 흐름 제어(RTS/CTS) 활성화
        )
        self._initialize_handshake()

    def _initialize_handshake(self):
        """
        DTE-DCE 핸드셰이킹 초기화
        1. DTR 신호를 High로 설정하여 DTE가 준비되었음을 DCE에 알림
        2. DSR 신호를 확인하여 DCE가 준비되었는지 확인
        """
        # DTE 준비 신호 활성화
        self.serial_conn.setDTR(True)
        print("[DTE] DTR 신호 활성화 - DTE 준비 완료")

        # DCE 준비 대기 (최대 5초)
        timeout = 5.0
        start_time = time.time()
        while not self.serial_conn.getDSR():
            if time.time() - start_time > timeout:
                raise TimeoutError("[DTE] DCE 응답 대기 시간 초과")
            time.sleep(0.1)
        print("[DTE] DSR 신호 감지 - DCE 준비 완료")

    def send_data(self, data: bytes) -> int:
        """
        하드웨어 흐름 제어를 통한 데이터 송신
        RTS/CTS 핸드셰이킹 과정:
        1. DTE가 RTS 신호를 High로 설정 (송신 요청)
        2. DCE가 준비되면 CTS 신호를 High로 응답 (송신 허가)
        3. DTE가 데이터를 전송
        4. 전송 완료 후 RTS 신호를 Low로 설정
        """
        # 송신 요청 신호 활성화
        self.serial_conn.setRTS(True)

        # DCE의 송신 허가(CTS) 대기
        timeout = 2.0
        start_time = time.time()
        while not self.serial_conn.getCTS():
            if time.time() - start_time > timeout:
                self.serial_conn.setRTS(False)
                raise TimeoutError("[DTE] CTS 대기 시간 초과")
            time.sleep(0.01)

        # 데이터 송신
        bytes_written = self.serial_conn.write(data)
        self.serial_conn.flush()  # 버퍼 비우기

        # 송신 완료 후 RTS 비활성화
        self.serial_conn.setRTS(False)
        print(f"[DTE] {bytes_written} 바이트 송신 완료")
        return bytes_written

    def receive_data(self, size: int = 1024) -> bytes:
        """
        데이터 수신
        DCD(Data Carrier Detect) 신호를 확인하여 정상 수신 여부 검증
        """
        # 반송파 감지 확인 (데이터 수신 중)
        if not self.serial_conn.getCD():
            print("[DTE] 경고: 반송파 미감지 상태")

        data = self.serial_conn.read(size)
        if data:
            print(f"[DTE] {len(data)} 바이트 수신 완료")
        return data

    def close(self):
        """연결 종료 및 신호 해제"""
        self.serial_conn.setDTR(False)
        self.serial_conn.setRTS(False)
        self.serial_conn.close()
        print("[DTE] 연결 종료")

# 실무 사용 예시
if __name__ == "__main__":
    # Linux: /dev/ttyS0 또는 /dev/ttyUSB0
    # Windows: COM1, COM2, ...
    dte = DTEInterface(port="/dev/ttyUSB0", baudrate=115200)

    try:
        # 데이터 송신
        message = b"Hello, DCE! This is DTE speaking.\r\n"
        dte.send_data(message)

        # 데이터 수신
        response = dte.receive_data()
        print(f"수신된 데이터: {response.decode('utf-8', errors='ignore')}")
    finally:
        dte.close()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: DTE vs DCE vs CCU 기능 매트릭스

| 비교 관점 | DTE (Data Terminal Equipment) | DCE (Data Circuit-terminating Equipment) | CCU (Communication Control Unit) |
|----------|-------------------------------|------------------------------------------|----------------------------------|
| **주요 기능** | 데이터 생성, 처리, 저장 | 신호 변환, 동기화, 인터페이스 | 오류 제어, 흐름 제어, 세션 관리 |
| **동작 계층** | L7~L5 (응용~세션) | L1 (물리), L2 (데이터링크 일부) | L2~L4 (데이터링크~전송) |
| **데이터 형태** | 비트 스트림, 패킷, 메시지 | 전기적/광학적 신호, 심볼 | 프레임, 세그먼트 |
| **대표 장비** | PC, 서버, 스마트폰, IoT 센서 | 모뎀, DSU/CSU, NIC, TA | 통신 컨트롤러, FEP, 프로토콜 스택 |
| **인터페이스** | RS-232C, USB, Ethernet (MII) | V.35, RS-449, G.703, RJ-45 | 소프트웨어 API, 하드웨어 레지스터 |
| **클럭 소스** | 외부 클럭 수신 (동기식) | 클럭 생성 및 공급 (마스터) | 클럭 기반 타이머 관리 |
| **오류 처리** | 애플리케이션 레벨 재시도 | 신호 레벨 증폭/재생 | CRC 계산, ARQ 수행 |

### DTE-DCE 인터페이스 표준 비교

| 표준 | 최대 속도 | 거리 | 커넥터 | 주요 용도 | 특징 |
|------|----------|------|--------|----------|------|
| **RS-232C** | 20 Kbps | 15m | DB-25, DB-9 | 단거리 시리얼 통신 | 비동기식, 단말-모뎀 연결 |
| **RS-422** | 10 Mbps | 1200m | DB-37 | 산업용 통신 | 차동 신호, 노이즈 내성 |
| **RS-449** | 2 Mbps | 60m | DB-37 | RS-232C 개선판 | 기계적/전기적 특성 분리 |
| **V.35** | 48 Kbps~2Mbps | 60m | Winchester | WAN 라우터 연결 | 동기식, 고속 디지털 회선 |
| **X.21** | 64 Kbps~2Mbps | 200m | DB-15 | 공중 데이터망 | 디지털 인터페이스, 회선 절감 |

### 과목 융합 관점 분석 (OS 및 보안 연계)

1. **운영체제(OS)와의 융합**:
   - **DTE의 네트워크 스택**: 현대 OS(Linux, Windows)의 커널은 CCU의 기능을 소프트웨어로 구현합니다. TCP/IP 스택이 오류 검출(Checksum), 흐름 제어(Sliding Window), 혼잡 제어(Congestion Control)를 수행합니다.
   - **인터럽트 처리**: DCE(NIC)가 패킷을 수신하면 하드웨어 인터럽트를 발생시키고, OS의 ISR(Interrupt Service Routine)이 이를 처리하여 상위 계층으로 전달합니다.
   - **Zero-Copy 기술**: DTE와 DCE 간의 데이터 복사 오버헤드를 줄이기 위해 `sendfile()` 시스템 콜이나 `mmap()`을 사용하여 커널 버퍼를 직접 참조합니다.

2. **보안(Security)와의 융합**:
   - **DCE 레벨 암호화**: 최신 모뎀과 DSU는 하드웨어 암호화 모듈을 탑재하여 물리 계층에서부터 데이터를 보호합니다.
   - **CCU의 인증 기능**: 통신 세션 설정 시 CCU가 상대방의 신원을 확인(CHAP, EAP 등)하고, 무단 접속을 차단합니다.
   - **DTE의 방화벽 연동**: DTE의 OS는 수신된 패킷을 방화벽(iptables, Windows Firewall)에 전달하여 보안 정책을 적용합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 통신 사업자 백본망 구축

**문제 상황**: 통신 사업자가 기업 고객에게 1Gbps 전용선 서비스를 제공하기 위해, 고객 구내에 설치할 DCE 장비와 중앙 국사의 CCU 시스템을 설계해야 합니다.

**기술사의 전략적 의사결정**:

1. **DCE 선정: DSU/CSU vs 광모뎀**:
   - **분석**: 고객 구내까지 광케이블이 이미 포설되어 있으므로, 전기적 신호를 광신호로 변환하는 광모뎀(Optical Modem) 또는 미디어 컨버터(Media Converter)가 적합합니다.
   - **결정**: 관리 편의성을 위해 L2 스위칭 기능이 통합된 **광네트워크 단말장치(ONT, Optical Network Terminal)**를 선택합니다. 이는 DCE 기능과 간단한 CCU 기능(포트 미러링, VLAN 태깅)을 통합 제공합니다.

2. **CCU 기능 분산: FEP 도입 여부**:
   - **분석**: 1,000개 이상의 전용선 고객을 관리해야 하므로, 중앙 라우터가 모든 CCU 기능(PPP 세션 관리, 인증, 과금 데이터 수집)을 수행하기에 부하가 심각합니다.
   - **결정**: **FEP(Front-End Processor)**를 라우터 앞단에 배치하여 PPP 종단, 인증(RADIUS 연동), 간단한 패킷 필터링을 오프로드합니다. 라우터는 라우팅과 QoS 처리에 집중합니다.

3. **DTE-DCE 인터페이스 표준 준수**:
   - **분석**: 다양한 벤더의 라우터(Cisco, Juniper, Huawei)와 연동해야 하므로 표준 인터페이스가 필수입니다.
   - **결정**: 광 인터페이스는 **Gigabit Ethernet(1000BASE-LX)** 표준을 따르고, 전기적 인터페이스는 **G.703** 표준을 준수하는 장비만 도입합니다. 벤더 종속적인 사설 프로토콜은 배제합니다.

### 도입 시 고려사항 체크리스트

| 항목 | 확인 내용 | 중요도 |
|------|----------|--------|
| **클럭 동기화** | DCE 장비의 클럭 소스(Master/Slave) 설정 확인 | 상 |
| **케이블 핀아웃** | DTE-DCE 간 케이블 타입(Straight-through vs Cross-over) 검증 | 상 |
| **흐름 제어** | 하드웨어 흐름 제어(RTS/CTS) 활성화 여부 확인 | 중 |
| **표준 호환성** | 인터페이스 표준(RS-232C, V.35, X.21) 호환성 검증 | 상 |
| **접지 및 차폐** | 전기적 노이즈 방지를 위한 접지 상태 확인 | 중 |
| **에러 레이트** | 비트 에러율(BER) 측정 및 기준치 이내 확인 | 상 |

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - DTE와 DCE의 역할 혼동**:
  일부 엔지니어가 라우터를 DTE로 분류하는 실수를 범합니다. 라우터는 네트워크 계층(L3) 장비이지만, WAN 포트에 연결될 때는 DTE 역할을, LAN 포트에 연결될 때는 DCE 역할을 수행할 수 있습니다. **연결 방향성(어느 쪽이 클럭을 공급하는가?)**에 따라 DTE/DCE 역할이 결정됩니다.

- **안티패턴 2 - 무리한 케이블 연장**:
  RS-232C 표준은 15m를 권장하지만, 저품질 케이블로 50m 이상 연장하면 신호 감쇠와 노이즈로 인해 통신 오류가 빈번합니다. 이 경우 RS-422/485로 전환하거나 광컨버터를 사용해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | 내용 | 정량적 지표 |
|----------|------|------------|
| **상호 운용성** | 표준화된 DTE-DCE 인터페이스로 이기종 장비 간 연결 | 벤더 교체 시 호환성 문제 0% |
| **유지보수 효율** | 계층별 역할 분담으로 장애 격리 용이 | 평균 수리 시간(MTTR) 40% 단축 |
| **확장성** | DCE 교체만으로 전송 매체 변경 가능 | 네트워크 업그레이드 비용 30% 절감 |
| **진단 용이성** | 인터페이스 레벨에서 루프백 테스트 가능 | 장애 원인 식별 시간 60% 단축 |

### 미래 전망 및 진화 방향

- **소프트웨어 정의 통신(Software-Defined Communication)**: DCE의 변조/부호화 기능이 소프트웨어(SDR, Software Defined Radio)로 구현되어, 펌웨어 업데이트만으로 새로운 통신 표준(5G, Wi-Fi 7)을 지원할 수 있게 됩니다.

- **AI 기반 CCU**: 머신러닝이 적용된 CCU가 트래픽 패턴을 학습하여 선제적으로 오류를 예측하고, 자동으로 전송 파라미터를 최적화하는 자율 통신으로 진화할 것입니다.

- **양자 통신 DCE**: 양자 키 분배(QKD)를 지원하는 DCE가 물리 계층에서부터 양자 암호화 통신을 가능하게 하여, 해킹이 원천적으로 불가능한 보안 통신을 실현할 것입니다.

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **EIA RS-232C** | EIA | Interface Between DTE and DCE Employing Serial Binary Data Interchange |
| **ITU-T V.35** | ITU-T | Data Transmission at 48 Kilobits per Second Using 60-108 kHz Group Band Circuits |
| **ITU-T X.21** | ITU-T | Interface Between DTE and DCE for Synchronous Operation on Public Data Networks |
| **ISO 2110** | ISO | Data Communication - 25-Pin DTE/DCE Interface Connector and Pin Assignments |
| **ITU-T V.24** | ITU-T | List of Definitions for Interchange Circuits in the DTE-DCE Interface |

---

## 참고 문헌 및 출처
- Tanenbaum, A. S., & Wetherall, D. J. (2021). Computer Networks (6th ed.). Pearson.
- Stallings, W. (2021). Data and Computer Communications (10th ed.). Pearson.
- ITU-T V.24, V.35, X.21 표준 문서
- EIA RS-232C 표준 규격서

---

## 관련 개념 맵 (Knowledge Graph)
- [OSI 7계층 모델](./osi_7_layer.md) - DTE, DCE, CCU가 각각 동작하는 계층의 이해
- [물리 계층 인코딩](./line_coding_nrz_rz_manchester.md) - DCE가 수행하는 NRZ, Manchester 부호화 기법
- [오류 제어 기법](./error_detection_parity_crc.md) - CCU가 수행하는 ARQ, FEC 메커니즘
- [변조 기술](./modulation_ask_fsk_psk_qam.md) - DCE의 변조기가 수행하는 ASK, FSK, PSK, QAM
- [다중화 기술](./multiplexing_fdm_tdm_wdm.md) - MUX 장비의 FDM, TDM, WDM 기법
- [전송 모드](./transmission_modes_duplex.md) - 단방향, 반이중, 전이중 통신 방식

---

## 어린이를 위한 3줄 비유 설명
1. **DTE**는 편지를 쓰고 읽는 **사람**이에요. 컴퓨터나 스마트폰으로 메시지를 만들어내는 역할을 하죠.
2. **DCE**는 편지를 배달하는 **우체국과 트럭**이에요. 우리가 쓴 디지털 메시지를 전기 신호나 빛 신호로 바꿔서 멀리 보내줍니다.
3. **CCU**는 모든 게 제대로 가고 있는지 확인하는 **우체국 직원**이에요. 편지가 중간에 떨어졌는지, 주소가 틀리지 않았는지 검사하고 고쳐줍니다!
