+++
weight = 12
title = "12. 동기식 전송의 문자 동기(SYN)와 비트 동기(SDLC, HDLC) 방식 비교"
date = "2026-03-10"
[extra]
categories = "studynote-network"
keywords = ["네트워크", "Synchronous", "Character Sync", "Bit Sync", "SYN", "BSC", "HDLC", "SDLC", "Bit Stuffing", "비트 스터핑"]
series = "네트워크 1200제"
+++

# 동기식 전송: 문자 동기 vs 비트 동기 방식

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 대량의 데이터를 블록 단위로 전송할 때, 데이터의 시작과 끝을 **특수 문자 SYN (Synchronization)**로 식별하느냐(문자 동기), 아니면 **특수 비트 패턴 (Flag)**으로 식별하느냐(비트 동기)의 전송 규약 차이.
> 2. **가치**: 문자 동기 방식은 단순하지만 특정 문자가 데이터에 포함될 때 혼란(투명성 문제)이 생길 수 있으며, 비트 동기 방식은 **비트 스터핑 (Bit Stuffing)**을 통해 어떤 데이터라도 전송 가능한 완전한 데이터 투명성을 보장한다.
> 3. **융합**: 현대 네트워크 프로토콜인 **PPP (Point-to-Point Protocol)**나 프레임 릴레이 (Frame Relay) 등의 모태가 되는 핵심 기술이며, 고속 데이터 링크 계층의 신뢰성 있는 통신을 가능케 하는 근간이다.

---

### Ⅰ. 문자 동기 방식 (Character-oriented / Byte-oriented)

- **정의**: **ASCII (American Standard Code for Information Interchange)**나 **EBCDIC (Extended Binary Coded Decimal Interchange Code)** 같은 특정 문자 코드를 사용하여 동기화를 유지하는 방식.
- **주요 프로토콜**: IBM의 **BSC (Binary Synchronous Communication)**.
- **매커니즘**:
  - 데이터 블록 앞에 2개 이상의 **SYN (Synchronization)** 문자를 붙여 수신 측과 동기를 맞춤.
  - 데이터 내부에 SYN 문자가 있을 경우를 대비해 **DLE (Data Link Escape)** 문자를 삽입하는 '문자 스터핑'이 필요함.

- **📢 섹션 요약 비유**: 대화 중간에 "어이!", "저기요!" 같은 추임새(SYN)를 넣어 리듬을 맞추는 소통 방식입니다.

---

### Ⅱ. 비트 동기 방식 (Bit-oriented)

- **정의**: 특정 비트 패턴(Flag)을 사용하여 프레임의 시작과 끝을 알리는 방식.
- **주요 프로토콜**: **SDLC (Synchronous Data Link Control)**, **HDLC (High-Level Data Link Control)**, **LAPB (Link Access Procedure Balanced)**.
- **매커니즘**:
  - 플래그 패턴: **`01111110` (0x7E)**를 사용.
  - **비트 스터핑 (Bit Stuffing)**: 데이터 내부에 '1'이 5개 연속으로 나오면 무조건 '0'을 하나 삽입하여 플래그와 혼동되는 것을 방지함.

- **📢 섹션 요약 비유**: 특정 색깔의 깃발(플래그)을 흔들어 이야기의 경계를 나누는 더 세련되고 똑똑한 신호 체계입니다.

---

### Ⅲ. 방식별 아키텍처 및 프레임 구조 (ASCII)

#### 1. BSC 프레임 (문자 동기)
```ascii
    [ SYN ] [ SYN ] [ SOH ] [ Header ] [ STX ] [ Text Data ] [ ETX ] [ BCC ]
    |--- Sync ---|  |-- Control ---|  |--- Information ---|  |-- Check --|
```

- **[다이어그램 해설]**: 
  - **SYN (Synchronization)** 문자로 시작하며, **SOH (Start of Heading)**로 헤더의 시작을 알린다. 
  - 본문 데이터는 **STX (Start of Text)**와 **ETX (End of Text)** 사이에 위치하며, 마지막에 에러 검출을 위한 **BCC (Block Check Character)**가 포함된다.

#### 2. HDLC 프레임 (비트 동기)
```ascii
    [ Flag ] [ Address ] [ Control ] [ Information Data ] [ FCS / CRC ] [ Flag ]
    01111110 (8 bits)    (8 bits)    (Variable Length)    (16/32 bit) 01111110
```

- **[다이어그램 해설]**: 
  - 시작과 끝을 알리는 **Flag** 비트 패턴(01111110)을 사용한다. 
  - 데이터 무결성을 위해 **FCS (Frame Check Sequence)** 또는 **CRC (Cyclic Redundancy Check)**를 사용하여 강력한 에러 제어 기능을 제공한다.

- **📢 섹션 요약 비유**: 물건을 담는 상자의 규격과 라벨을 정해 물류의 효율을 높이는 표준 포장 법규와 같습니다.

---

### Ⅳ. 상세 비교 분석표

| 구분 항목 | 문자 동기 방식 (BSC) | 비트 동기 방식 (HDLC) |
|:---|:---|:---|
| **기본 단위** | 8비트 문자 (Byte) | **비트 (Bit)** |
| **전송 제어** | 반이중 (Half-duplex) 중심 | **전이중 (Full-duplex)** 지원 |
| **투명성** | 문자 스터핑 (DLE 사용) | **비트 스터핑** (0 삽입) |
| **효율성** | 낮음 (제어 문자 오버헤드) | **높음** (가변 길이 전송 최적화) |
| **신뢰성** | 보통 | **매우 높음** (강력한 에러 제어) |

- **📢 섹션 요약 비유**: 구식 타자기(문자)와 현대적 컴퓨터(비트)의 처리 능력 차이만큼나 확연한 기술적 격차입니다.

---

### Ⅴ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 데이터 투명성 (Transparency) 보장
- **현상**: 바이너리 파일이나 압축 데이터를 보낼 때 제어 문자와 데이터가 겹쳐 통신이 끊김.
- **기술사적 결단**: 
  - 문자 기반의 레거시 시스템은 **DLE (Data Link Escape)** 문자를 이용한 이스케이프 처리를 수행해야 한다.
  - 신규 시스템 설계 시에는 무조건 **비트 지향 프로토콜 (HDLC)**을 채택하여 데이터 종류에 상관없는 범용 전송망을 구축해야 한다.

#### 2. 기술사적 인사이트: 비트 스터핑의 부작용
- 비트 스터핑은 데이터의 길이를 가변적으로 만든다. 
- 이로 인해 실제 전송되는 비트 수가 원본보다 미세하게 늘어나며, 이는 대역폭 계산 시 **Padding 오버헤드**로 고려되어야 함을 명시해야 한다.

- **📢 섹션 요약 비유**: 정보가 왜곡되지 않도록 중간에 가짜 신호(스터핑)를 섞어 진짜를 보호하는 고도의 위장 전술과 같습니다.

---

### Ⅵ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량/정성 기대효과
- **전송 효율 극대화**: 프레임 단위의 일괄 전송을 통한 채널 이용률 향상.
- **유연한 데이터 처리**: 텍스트, 멀티미디어, 코드 등 모든 형태의 정보 수용.

#### 2. 미래 전망
최근의 초고속 이더넷이나 광전송망인 **OTN (Optical Transport Network)**에서는 더 고도화된 **64B/66B 인코딩**이나 **프레임 구분자** 기술을 사용하지만, 그 근본에는 **HDLC (High-Level Data Link Control)**의 비트 동기 및 투명성 보장 철학이 고스란히 담겨 있다. 향후 6G 환경에서도 가변 길이 패킷을 초저지연으로 동기화하기 위한 차세대 비트 제어 기술이 인프라의 핵심이 될 것이다.

- **📢 섹션 요약 비유**: 과거의 지혜를 바탕으로 더 빠르고 정확한 미래의 소통 고속도로를 닦아나가는 과정입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[비트 스터핑](../../3_network/TBD_bit_stuffing.md)**: 비트 동기 방식의 핵심 동작.
- **[HDLC 프로토콜](../../3_network/TBD_hdlc.md)**: **HDLC (High-Level Data Link Control)**는 가장 널리 쓰이는 동기식 표준이다.
- **[OSI 2계층](../../3_network/TBD_datalink.md)**: 동기 방식이 주로 정의되는 **OSI (Open Systems Interconnection) 7계층** 중 데이터 링크 계층이다.
---

### 👶 어린이를 위한 3줄 비유 설명
1. **문자 동기**는 이야기 중간중간에 "잠깐만!", "이제 시작!"이라는 **말(문자)**을 넣어서 순서를 맞추는 거예요.
2. **비트 동기**는 "01111110"이라는 특별한 **깃발(비트 패턴)**을 흔들어서 이야기의 시작과 끝을 알려주는 거죠.
3. 깃발 방식은 어떤 이야기를 하더라도 깃발만 잘 보면 되니까 훨씬 깔끔하고 똑똑한 방법이랍니다!
