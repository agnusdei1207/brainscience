+++
title = "OSI 7계층 (OSI 7 Layers)"
date = 2024-05-18
description = "OSI 7계층 참조 모델의 아키텍처, 각 계층별 프로토콜 데이터 단위(PDU), 캡슐화 메커니즘, 그리고 TCP/IP 모델과의 비교 분석"
weight = 10
+++

# OSI 7계층 네트워크 참조 모델 심층 분석 (OSI 7 Layer Architecture)

## 1. OSI 7계층 모델의 개요 (Overview)
OSI(Open Systems Interconnection) 7계층 모델은 국제표준화기구(ISO)에서 네트워크 통신의 전 과정을 7개의 논리적인 단계로 표준화한 아키텍처 모델입니다. 과거 다양한 벤더(IBM, DEC 등)가 독자적인 네트워크 프로토콜을 사용하여 기종 간 호환성이 결여되는 문제를 해결하기 위해, 이기종 시스템 간의 통신 규약을 개방형으로 정립한 것입니다.

비록 현대의 실질적인 인터넷 표준은 TCP/IP 모델이 지배하고 있으나, OSI 모델은 네트워크 문제 해결(Troubleshooting), 하드웨어 및 소프트웨어의 모듈화 설계, 그리고 학술적인 통신 원리 이해를 위한 범용적인 프레임워크로서 여전히 절대적인 권위를 가집니다.

## 2. 계층적 구조와 캡슐화 (Encapsulation Architecture)

데이터가 송신자에서 수신자로 전달될 때, 최상위 애플리케이션 계층에서 시작하여 하위 계층으로 내려가며 각 계층의 고유한 헤더(Header)가 덧붙여집니다. 이를 **캡슐화(Encapsulation)**라고 합니다. 수신 측에서는 역순으로 헤더를 벗겨내는 **역캡슐화(Decapsulation)**가 일어납니다.

```ascii
[ 송신 호스트 (Sender) ]                                          [ 수신 호스트 (Receiver) ]
 
 7. Application   [ DATA ] <-----------------------------------> [ DATA ]   Application  .7
                    |                                                ^
 6. Presentation [H6|DATA] <-----------------------------------> [H6|DATA]  Presentation .6
                    |                                                ^
 5. Session      [H5|...DATA] <--------------------------------> [H5|...DATA]    Session .5
                    |                                                ^
 4. Transport    [H4|...DATA] (Segment/Datagram) <-------------> [H4|...DATA]  Transport .4
                    |                                                ^
 3. Network      [H3|...DATA] (Packet) <---(Router)---> [H3|...DATA] Network         .3
                    |                                                ^
 2. Data Link [T2|H2|...DATA] (Frame)  <---(Switch)---> [T2|H2|...DATA] Data Link    .2
                    |                                                ^
 1. Physical   [010101010...] (Bit)    <----(Hub)-----> [010101010...] Physical      .1
```

## 3. 계층별 상세 기능 및 PDU (Protocol Data Unit)

### L1: 물리 계층 (Physical Layer)
- **핵심 역할**: 디지털 데이터(0과 1의 비트열)를 전기적, 광학적, 전파 신호로 변환하여 물리적인 매체(케이블, 광섬유, 무선)를 통해 전송합니다.
- **주요 기능**: 전송 속도 제어, 물리적 토폴로지 구성, 신호의 변조 및 복조.
- **PDU**: 비트 (Bit)
- **장비/프로토콜**: 리피터(Repeater), 허브(Hub), 케이블(UTP, 코액셜), RS-232, 100BASE-T.

### L2: 데이터 링크 계층 (Data Link Layer)
- **핵심 역할**: 물리 계층의 신뢰성 없는 전송로를 통해 인접한 노드(Node-to-Node) 간의 신뢰성 있는 데이터 전송을 보장합니다. MAC 주소를 기반으로 통신합니다.
- **주요 기능**: 
  - 프레이밍(Framing): 데이터를 프레임 단위로 분할.
  - 오류 제어(Error Control): CRC 등을 이용해 물리 계층에서 발생한 오류 검출 및 재전송(ARQ).
  - 흐름 제어(Flow Control): 송수신 속도 차이 극복.
  - 매체 접근 제어(MAC): CSMA/CD, CSMA/CA 등.
- **PDU**: 프레임 (Frame)
- **장비/프로토콜**: L2 스위치, 브릿지(Bridge), 이더넷(Ethernet, IEEE 802.3), Wi-Fi(IEEE 802.11), ARP.

### L3: 네트워크 계층 (Network Layer)
- **핵심 역할**: 발신지에서 목적지까지 데이터(패킷)를 전달하기 위한 최적의 경로(Routing)를 선택하고 논리적인 주소(IP)를 관리합니다. (End-to-End 전송의 뼈대)
- **주요 기능**: 라우팅(Routing), 논리적 주소 지정(IP Addressing), 패킷 분할 및 병합(Fragmentation).
- **PDU**: 패킷 (Packet) 또는 데이터그램(Datagram)
- **장비/프로토콜**: 라우터(Router), L3 스위치, IPv4, IPv6, ICMP, OSPF, BGP, IPsec.

### L4: 전송 계층 (Transport Layer)
- **핵심 역할**: 종단 간(End-to-End) 애플리케이션 프로세스 사이의 논리적 통신을 제공하며, 통신의 신뢰성과 포트(Port) 번호를 통한 프로세스 식별을 담당합니다.
- **주요 기능**: 연결 지향성 통신(TCP), 비연결성 통신(UDP), 신뢰성 보장, 오류 복구, 혼잡 제어(Congestion Control).
- **PDU**: 세그먼트 (Segment - TCP) / 데이터그램 (Datagram - UDP)
- **프로토콜**: TCP (Transmission Control Protocol), UDP (User Datagram Protocol).

#### [ 네트워크 및 전송 계층 활용 코드: Python Socket 통신 예제 ]
애플리케이션은 소켓 API를 통해 L4/L3 기능에 접근합니다.
```python
import socket

# TCP 소켓 생성 (L4: TCP, L3: IPv4)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 포트 바인딩 (L4 포트 8080)
server_socket.bind(('0.0.0.0', 8080))
# 연결 대기 상태로 전환 (Session 설립 대기)
server_socket.listen(5)
print("서버가 8080 포트에서 연결을 대기 중입니다...")

while True:
    # 3-Way Handshake가 완료된 클라이언트의 연결 수락
    client_socket, addr = server_socket.accept()
    print(f"클라이언트 연결됨: {addr[0]}:{addr[1]}")
    
    # 데이터 수신 (Application Data)
    data = client_socket.recv(1024)
    print(f"수신한 데이터: {data.decode('utf-8')}")
    
    # 응답 전송
    client_socket.sendall("서버 응답: 데이터 정상 수신 완료".encode('utf-8'))
    client_socket.close()
```

### L5: 세션 계층 (Session Layer)
- **핵심 역할**: 양 끝단의 응용 프로세스가 통신을 관리하기 위한 방법(세션 설정, 유지, 종료)을 제공합니다.
- **주요 기능**: 동기화(Synchronization) 지점을 제공하여, 파일 전송 중 끊김이 발생했을 때 체크포인트부터 재전송할 수 시킵니다. 통신 방식 결정(전이중, 반이중).
- **프로토콜**: NetBIOS, RPC, PPTP.

### L6: 표현 계층 (Presentation Layer)
- **핵심 역할**: 송신 측과 수신 측 사이의 데이터 형식을 일치시켜, 애플리케이션이 데이터를 이해할 수 있도록 변환합니다. 데이터의 구문(Syntax)과 의미(Semantics)를 다룹니다.
- **주요 기능**:
  - 데이터 포맷 변환 (예: EBCDIC -> ASCII)
  - 데이터 인코딩/디코딩 (예: JSON, XML, 멀티미디어 코덱)
  - 데이터 암호화/복호화 (예: TLS/SSL의 암호화 기능)
  - 데이터 압축
- **프로토콜**: JPEG, MPEG, ASCII, TLS(일부 기능).

### L7: 응용 계층 (Application Layer)
- **핵심 역할**: 사용자와 가장 가까운 계층으로, 네트워크 소프트웨어 UI 부분이나 사용자의 입출력을 처리합니다. 네트워크 서비스에 접근할 수 있는 인터페이스를 제공합니다.
- **주요 기능**: 파일 전송, 이메일, 웹 브라우징, 디렉토리 서비스 등.
- **PDU**: 데이터 (Data) 또는 메시지(Message)
- **프로토콜**: HTTP, HTTPS, FTP, SMTP, DNS, SSH, Telnet.

## 4. 실무적 의의: 고가용성과 트러블슈팅
클라우드 엔지니어나 아키텍트에게 OSI 7계층 지식은 필수적입니다.
- **장애 대응**: 사용자가 "웹사이트 접속이 안 돼요"라고 할 때, L1(케이블 단선?) -> L2(MAC 충돌?) -> L3(라우팅/IP 할당 문제? ping 테스트) -> L4(방화벽 포트 블록? telnet 테스트) -> L7(HTTP 500 에러, 애플리케이션 버그?) 순으로 논리적인 문제 해결 접근이 가능합니다.
- **보안 아키텍처 (WAF vs Firewall)**: L3/L4 계층을 방어하는 일반적인 IP/Port 기반 방화벽(Network Firewall)과, L7 계층의 페이로드를 검사하여 SQL Injection 등을 차단하는 웹 방화벽(WAF)의 차이를 완벽히 분리하여 설계할 수 있습니다.
- **로드 밸런싱 (L4 vs L7)**: L4 로드밸런서는 IP와 Port 정보만을 보고 트래픽을 분산시켜 속도가 빠릅니다. 반면 L7 로드밸런서는 HTTP 헤더, 쿠키, URI 등을 파싱하여 마이크로서비스(MSA) 환경에서 컨텍스트 기반의 지능적인 라우팅(예: /api 는 A서버군, /image 는 B서버군)을 수행할 수 있습니다.
