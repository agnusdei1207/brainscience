+++
title = "759. 5G NR (New Radio) 및 5G 아키텍처"
description = "5G NR 무선 접속 기술과 5G 코어 네트워크(5GC)의 SBA 아키텍처, 네트워크 슬라이싱, MEC를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["5G", "NR", "5GC", "SBA", "NetworkSlicing", "MEC", "MIMO", "Beamforming", "uRLLC", "eMBB"]
categories = ["studynotes-3_network"]
+++

# 759. 5G NR (New Radio) 및 5G 아키텍처

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 5G NR은 3GPP가 표준화한 차세대 무선 접속 기술로, FR1(Sub-6GHz)과 FR2(mmWave) 대역을 지원하며, OFDM 기반의 유연한 파라미터(서브캐리어 간격, 슬롯 길이)로 다양한 서비스(eMBB, uRLLC, mMTC)를 최적화합니다.
> 2. **가치**: 5G는 4G 대비 최대 20Gbps 다운로드, 1ms 미만 지연, 100만 개/km² 연결 밀도를 제공하며, 네트워크 슬라이싱으로 하나의 물리망 위에 논리적으로 격리된 복수의 전용망을 운영할 수 있습니다.
> 3. **융합**: 5G 코어(5GC)는 서비스 기반 아키텍처(SBA)로 마이크로서비스화되어 클라우드 네이티브 운영이 가능하며, MEC(Multi-access Edge Computing)와 결합하여 초저지연 엣지 컴퓨팅을 실현합니다.

---

## Ⅰ. 개요 (Context & Background)

5G(5th Generation)는 2019년부터 상용화된 5세대 이동통신 기술로, 3GPP(3rd Generation Partnership Project)가 표준화했습니다. 4G LTE가 "광대역 모바일 인터넷"에 집중했다면, 5G는 **eMBB(초고속 광대역)**, **uRLLC(초고신뢰 저지연)**, **mMTC(대규모 사물 연결)**의 세 가지 사용 시나리오를 동시에 지원합니다.

**💡 비유**: 5G를 **'스마트 고속도로 시스템'**에 비유할 수 있습니다.
- **FR1 (Sub-6GHz)**은 **일반 도로**입니다. 넓은 커버리지, 건물 투과율이 좋습니다.
- **FR2 (mmWave)**은 **자동차 전용 고속도로**입니다. 초고속이지만 터널(건물)을 통과하지 못합니다.
- **네트워크 슬라이싱**은 **차선 분리**입니다. 일반 차선, 버스 전용 차선, 긴급 차량 차선으로 나눕니다.
- **MEC**는 **휴게소**입니다. 데이터를 목적지까지 가지 않고 가까운 곳에서 처리합니다.
- **Massive MIMO**는 **다차선 도로**입니다. 64개, 128개 차선으로 동시에 많은 차량(사용자)을 처리합니다.

**등장 배경 및 발전 과정**:
1. **4G LTE의 한계 (2010년대)**: 최대 1Gbps 속도, 10ms 지연은 AR/VR, 자율주행, 산업용 IoT에 부족했습니다.
2. **5G 비전 정립 (2015년)**: ITU-R이 IMT-2020으로 5G 요구사항을 정의했습니다 (20Gbps, 1ms, 100만 연결).
3. **3GPP Rel-15 (2018년)**: 5G NR 첫 표준, NSA(Non-Standalone) 모드 중심
4. **3GPP Rel-16 (2020년)**: SA(Standalone), uRLLC, 산업용 IoT 강화
5. **3GPP Rel-17 (2022년)**: RedCap(Reduced Capability), NTN(Non-Terrestrial Network), XR 확장

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 5G 3대 사용 시나리오 (ITU-R IMT-2020)

| 시나리오 | 명칭 | 목표 성능 | 주요 용도 |
|----------|------|----------|----------|
| **eMBB** | Enhanced Mobile Broadband | 20 Gbps DL, 10 Gbps UL | 8K 스트리밍, AR/VR, 홀로그램 |
| **uRLLC** | Ultra-Reliable Low Latency | <1ms 지연, 99.9999% 신뢰성 | 자율주행, 원격 수술, 산업용 로봇 |
| **mMTC** | Massive Machine-Type Comms | 100만 장치/km² | 스마트시티, 스마트팜, 대규모 센서 |

### 5G 주파수 대역 (FR1, FR2)

| 대역 | 주파수 범위 | 특성 | 커버리지 | 용도 |
|------|------------|------|----------|------|
| **FR1 (Sub-6)** | 410 MHz ~ 7.125 GHz | 양호한 투과율, 중간 속도 | 수 km | 광역 커버리지 |
| **FR2 (mmWave)** | 24.25 ~ 52.6 GHz | 초고속, 낮은 투과율 | 수백 m | 밀집 지역, 실내 |

### 5G NR 파라미터 (Numerology)

| μ (mu) | 서브캐리어 간격 | 슬롯 길이 | FR | 용도 |
|--------|----------------|----------|-----|------|
| 0 | 15 kHz | 1 ms | FR1 | 저속 이동, 광역 |
| 1 | 30 kHz | 0.5 ms | FR1 | 일반 용도 |
| 2 | 60 kHz | 0.25 ms | FR1/FR2 | 고속 이동 |
| 3 | 120 kHz | 0.125 ms | FR2 | mmWave |
| 4 | 240 kHz | 0.0625 ms | FR2 | 초저지연 |

### 5G 코어 네트워크(5GC) SBA 구성요소

| NF (Network Function) | 역할 | 4G 대응 |
|----------------------|------|---------|
| **AMF** | Access and Mobility Management | MME (이동성) |
| **SMF** | Session Management Function | MME + SGW-C |
| **UPF** | User Plane Function | SGW-U + PGW-U |
| **PCF** | Policy Control Function | PCRF |
| **UDM** | Unified Data Management | HSS |
| **AUSF** | Authentication Server Function | HSS (인증) |
| **NRF** | NF Repository Function | 신규 (서비스 디스커버리) |
| **NSSF** | Network Slice Selection Function | 신규 (슬라이싱) |

### 정교한 구조 다이어그램: 5G End-to-End 아키텍처

```ascii
================================================================================
[ 5G End-to-End Architecture (SA Mode) ]
================================================================================

[ UE (User Equipment) ]
+------------------+
| 5G Smartphone   |
| AR/VR Device    |
| IoT Sensor      |
| Autonomous Car  |
+--------|---------+
         | NR (무선 인터페이스)
         v
+--------|---------+                    +------------------+
|   gNodeB (gNB)   |                    |    5G Core (5GC) |
|------------------|                    |------------------|
| - CU (Centralized|     N2/N3          | [ Control Plane ]|
|   Unit)          |<------------------>|                  |
| - DU (Distributed|     F1-C/U         |    +-------+     |
|   Unit)          |                    |    |  AMF  |<----|--- N1 (NAS)
| - RU (Radio Unit)|                    |    +-------+     |
+--------|---------+                    |        | N11     |
         | Fronthaul                    |        v         |
         v                              |    +-------+     |
+--------|---------+                    |    |  SMF  |     |
|   Transport      |                    |    +-------+     |
|   Network        |                    |        | N4      |
| (Fronthaul/      |                    |        v         |
|  Midhaul/        |                    |    +-------+     |
|  Backhaul)       |<------------------>|    |  UPF  |<----|--- N3 (User Plane)
+------------------+     N3             |    +-------+     |
                                         |        |        |
                                         |        | N6      |
                                         |        v        |
                                         |   +----------+  |
                                         |   | Data      |  |
                                         |   | Network   |  |
                                         |   +----------+  |
                                         |                 |
                                         | [ Service Mesh ]|
                                         |    +-------+    |
                                         |    |  PCF  |    |
                                         |    +-------+    |
                                         |    +-------+    |
                                         |    |  UDM  |    |
                                         |    +-------+    |
                                         |    +-------+    |
                                         |    |  NRF  |    |
                                         |    +-------+    |
                                         +-----------------+

================================================================================
[ Network Slicing Architecture ]
================================================================================

                    물리적 인프라 (공유)
    +-------------------------------------------+
    |         RAN (gNB)     |     5G Core (5GC) |
    |                       |                   |
    |   [공유 기지국]        |   [공유 UPF]      |
    +-----------|-----------+--------|----------+
                |                    |
        +-------+-------+    +-------+-------+
        |   Slice #1    |    |   Slice #2    |
        |   (eMBB)      |    |   (uRLLC)     |
        |---------------|    |---------------|
        | - 스마트폰    |    | - 자율주행    |
        | - 고속 인터넷 |    | - 산업용 IoT  |
        | - QoS: Best  |    | - QoS: 99.999%|
        | - BW: 100MHz |    | - BW: 10MHz   |
        +---------------+    +---------------+

                +-------+-------+
                |   Slice #3    |
                |   (mMTC)      |
                |---------------|
                | - 스마트미터  |
                | - 센서 네트워크|
                | - QoS: Best  |
                | - BW: 5MHz   |
                +---------------+

================================================================================
[ Massive MIMO and Beamforming ]
================================================================================

     gNB (64T64R 안테나)
     +------------------------------------------+
     |  ================================        |
     |  |  |  |  |  |  |  |  |  |  |  |        |  <- 64개 안테나 소자
     |  ================================        |
     +------------------------------------------+
              |    |    |    |    |
              v    v    v    v    v
           +----+----+----+----+----+
           | 빔 #1 | 빔 #2 | 빔 #3 |  <- 3D 빔포밍
           +----+----+----+----+----+
               |         |
            +--+--+   +--+--+
            | UE1 |   | UE2 |  <- MU-MIMO (다중 사용자)
            +-----+   +-----+

    빔포밍 이득:
    - 안테나 이득: 10log10(N) dB (N=안테나 수)
    - 64 안테나: 약 18 dB 이득
```

### 심층 동작 원리: 5G 프로토콜 스택

**제어 평면 (Control Plane)**:
```
UE                gNB                  AMF                 SMF
 |                  |                    |                   |
 |--[NAS] RRC ----->|                    |                   |
 |                  |--[NGAP] AMF------->|                   |
 |                  |                    |--[Nsmf] SMF------>|
 |                  |                    |                   |
 |<--------[NAS Security]----------------|                   |
 |                  |                    |                   |
 |<-----------[PDU Session Setup]--------|<------------------|
```

**사용자 평면 (User Plane)**:
```
UE                gNB                  UPF                 Internet
 |                  |                    |                   |
 |--[SDAP/PDCP]---->|                    |                   |
 |   [RLC/MAC/PHY]  |---[GTP-U]--------->|                   |
 |                  |    (N3 Tunnel)     |---[IP]----------->|
 |                  |                    |                   |
 |<-----------------|<-------------------|<------------------|
```

### 핵심 코드: 5G 네트워크 슬라이스 시뮬레이터 (Python)

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import uuid

class SliceType(Enum):
    """네트워크 슬라이스 타입"""
    EMBB = "eMBB"      # Enhanced Mobile Broadband
    URLLC = "uRLLC"    # Ultra-Reliable Low Latency
    MMTC = "mMTC"      # Massive Machine-Type Communications

class UEType(Enum):
    """단말 타입"""
    SMARTPHONE = "Smartphone"
    AR_VR = "AR/VR Device"
    AUTONOMOUS_VEHICLE = "Autonomous Vehicle"
    IOT_SENSOR = "IoT Sensor"
    INDUSTRIAL_ROBOT = "Industrial Robot"

@dataclass
class QoSProfile:
    """QoS 프로필"""
    name: str
    guaranteed_bitrate_dl: int  # Mbps
    guaranteed_bitrate_ul: int  # Mbps
    max_bitrate_dl: int         # Mbps
    max_bitrate_ul: int         # Mbps
    max_latency_ms: float       # ms
    packet_error_rate: float    # 0.0 ~ 1.0
    priority_level: int         # 1 (최고) ~ 255

@dataclass
class NetworkSlice:
    """네트워크 슬라이스 정의"""
    slice_id: str
    slice_type: SliceType
    sst: int  # Slice/Service Type (1: eMBB, 2: uRLLC, 3: mMTC)
    sd: str   # Slice Differentiator
    qos_profile: QoSProfile
    bandwidth_mhz: int
    users: List[str] = field(default_factory=list)
    active: bool = True

@dataclass
class UE:
    """5G 단말"""
    ue_id: str
    ue_type: UEType
    slice_id: str
    imei: str
    location: tuple  # (latitude, longitude)
    connected: bool = False
    active_bearer: Optional[str] = None

class FiveGCoreSimulator:
    """
    5G Core 네트워크 시뮬레이터
    AMF, SMF, UPF, PCF, UDM 기능 시뮬레이션
    """

    def __init__(self):
        self.slices: Dict[str, NetworkSlice] = {}
        self.ues: Dict[str, UE] = {}
        self.sessions: Dict[str, dict] = {}

        # 기본 QoS 프로필 정의
        self.qos_profiles = {
            'eMBB_Premium': QoSProfile(
                name='eMBB Premium', guaranteed_bitrate_dl=1000,
                guaranteed_bitrate_ul=500, max_bitrate_dl=2000,
                max_bitrate_ul=1000, max_latency_ms=10.0,
                packet_error_rate=1e-3, priority_level=10
            ),
            'uRLLC_Critical': QoSProfile(
                name='uRLLC Critical', guaranteed_bitrate_dl=50,
                guaranteed_bitrate_ul=50, max_bitrate_dl=100,
                max_bitrate_ul=100, max_latency_ms=1.0,
                packet_error_rate=1e-6, priority_level=1
            ),
            'mMTC_Standard': QoSProfile(
                name='mMTC Standard', guaranteed_bitrate_dl=1,
                guaranteed_bitrate_ul=1, max_bitrate_dl=10,
                max_bitrate_ul=10, max_latency_ms=100.0,
                packet_error_rate=1e-2, priority_level=100
            )
        }

    def create_slice(self, slice_type: SliceType,
                     bandwidth_mhz: int) -> NetworkSlice:
        """네트워크 슬라이스 생성"""
        slice_id = f"SST{slice_type.value}_{uuid.uuid4().hex[:8]}"

        # SST (Slice/Service Type) 할당
        sst_map = {
            SliceType.EMBB: 1,
            SliceType.URLLC: 2,
            SliceType.MMTC: 3
        }

        # QoS 프로필 선택
        qos_map = {
            SliceType.EMBB: self.qos_profiles['eMBB_Premium'],
            SliceType.URLLC: self.qos_profiles['uRLLC_Critical'],
            SliceType.MMTC: self.qos_profiles['mMTC_Standard']
        }

        slice_obj = NetworkSlice(
            slice_id=slice_id,
            slice_type=slice_type,
            sst=sst_map[slice_type],
            sd=uuid.uuid4().hex[:6],
            qos_profile=qos_map[slice_type],
            bandwidth_mhz=bandwidth_mhz
        )

        self.slices[slice_id] = slice_obj
        print(f"[5GC] 슬라이스 생성: {slice_id} ({slice_type.value}, {bandwidth_mhz}MHz)")
        return slice_obj

    def register_ue(self, ue_type: UEType, target_slice: SliceType,
                    imei: str, location: tuple) -> UE:
        """UE 등록 (AMF 기능 시뮬레이션)"""
        ue_id = f"UE_{uuid.uuid4().hex[:8]}"

        # 적절한 슬라이스 찾기
        slice_id = None
        for sid, sl in self.slices.items():
            if sl.slice_type == target_slice and sl.active:
                slice_id = sid
                break

        if not slice_id:
            print(f"[5GC] 경고: {target_slice.value} 슬라이스 없음")
            return None

        ue = UE(
            ue_id=ue_id,
            ue_type=ue_type,
            slice_id=slice_id,
            imei=imei,
            location=location
        )

        self.ues[ue_id] = ue
        self.slices[slice_id].users.append(ue_id)

        print(f"[AMF] UE 등록: {ue_id} ({ue_type.value}) → 슬라이스 {slice_id}")
        return ue

    def setup_pdu_session(self, ue_id: str) -> Optional[dict]:
        """PDU 세션 설정 (SMF 기능 시뮬레이션)"""
        if ue_id not in self.ues:
            print(f"[SMF] UE {ue_id} 없음")
            return None

        ue = self.ues[ue_id]
        slice_obj = self.slices[ue.slice_id]

        session_id = f"PDU_{uuid.uuid4().hex[:8]}"

        session = {
            'session_id': session_id,
            'ue_id': ue_id,
            'slice_id': ue.slice_id,
            'upf_ip': '10.0.0.1',
            'ue_ip': f'10.{slice_obj.sst}.{hash(ue_id) % 256}.{hash(ue_id) % 256}',
            'qos': slice_obj.qos_profile,
            'status': 'ACTIVE'
        }

        self.sessions[session_id] = session
        ue.connected = True
        ue.active_bearer = session_id

        print(f"[SMF] PDU 세션 설정: {session_id}")
        print(f"      UE IP: {session['ue_ip']}")
        print(f"      QoS: {session['qos'].name}")
        print(f"      최대 지연: {session['qos'].max_latency_ms}ms")

        return session

    def get_slice_statistics(self) -> Dict:
        """슬라이스별 통계"""
        stats = {}

        for slice_id, sl in self.slices.items():
            active_users = sum(1 for ue_id in sl.users
                               if self.ues[ue_id].connected)

            stats[slice_id] = {
                'type': sl.slice_type.value,
                'bandwidth_mhz': sl.bandwidth_mhz,
                'total_users': len(sl.users),
                'active_users': active_users,
                'qos': sl.qos_profile.name
            }

        return stats

    def simulate_handover(self, ue_id: str, new_location: tuple) -> bool:
        """핸드오버 시뮬레이션 (Xn 또는 N2 핸드오버)"""
        if ue_id not in self.ues:
            return False

        ue = self.ues[ue_id]
        old_location = ue.location
        ue.location = new_location

        print(f"[AMF] 핸드오버: {ue_id}")
        print(f"      {old_location} → {new_location}")

        return True


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("[ 5G Network Simulator ]")
    print("=" * 60)

    # 5G 코어 시뮬레이터 생성
    core = FiveGCoreSimulator()

    # 네트워크 슬라이스 생성
    print("\n[ 슬라이스 생성 ]")
    embb_slice = core.create_slice(SliceType.EMBB, bandwidth_mhz=100)
    urllc_slice = core.create_slice(SliceType.URLLC, bandwidth_mhz=20)
    mmtc_slice = core.create_slice(SliceType.MMTC, bandwidth_mhz=10)

    # UE 등록 및 PDU 세션 설정
    print("\n[ UE 등록 및 세션 설정 ]")

    # eMBB 사용자
    smartphone = core.register_ue(
        UEType.SMARTPHONE, SliceType.EMBB,
        "IMEI123456789", (37.5665, 126.9780)
    )
    if smartphone:
        core.setup_pdu_session(smartphone.ue_id)

    # uRLLC 사용자
    vehicle = core.register_ue(
        UEType.AUTONOMOUS_VEHICLE, SliceType.URLLC,
        "IMEI987654321", (37.5665, 126.9790)
    )
    if vehicle:
        core.setup_pdu_session(vehicle.ue_id)

    # mMTC 사용자
    sensor = core.register_ue(
        UEType.IOT_SENSOR, SliceType.MMTC,
        "IMEI111222333", (37.5665, 126.9800)
    )
    if sensor:
        core.setup_pdu_session(sensor.ue_id)

    # 슬라이스 통계
    print("\n[ 슬라이스 통계 ]")
    print("-" * 60)
    stats = core.get_slice_statistics()

    for slice_id, info in stats.items():
        print(f"\n{slice_id}:")
        print(f"  타입: {info['type']}")
        print(f"  대역폭: {info['bandwidth_mhz']} MHz")
        print(f"  사용자: {info['active_users']}/{info['total_users']} 활성")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 4G LTE vs 5G NR 비교

| 특성 | 4G LTE | 5G NR |
|------|--------|-------|
| **최대 속도** | 1 Gbps | 20 Gbps |
| **지연 시간** | 10 ms | < 1 ms |
| **연결 밀도** | 10만/km² | 100만/km² |
| **주파수 대역** | Sub-6GHz | Sub-6GHz + mmWave |
| **코어 네트워크** | EPC (모놀리식) | 5GC (SBA, 마이크로서비스) |
| **네트워크 슬라이싱** | 제한적 | 완전 지원 |
| **MIMO** | 4x4 MIMO | Massive MIMO (64x64+) |
| **핸드오버** | X2/S1 | Xn/N2 |
| **이동성** | 350 km/h | 500 km/h |

### NSA vs SA 모드 비교

| 특성 | NSA (Non-Standalone) | SA (Standalone) |
|------|---------------------|-----------------|
| **코어** | LTE EPC | 5G Core (5GC) |
| **제어 평면** | LTE eNB | 5G gNB |
| **사용자 평면** | LTE + 5G | 5G만 |
| **슬라이싱** | 제한적 | 완전 지원 |
| **MEC** | 제한적 | 완전 지원 |
| **도입 비용** | 낮음 | 높음 |
| **성능** | 중간 | 최고 |

### 과목 융합 관점 분석

1. **클라우드/컨테이너와의 융합**:
   - **5GC SBA**: 각 NF가 컨테이너로 배포, Kubernetes로 오케스트레이션
   - **CNF (Cloud-Native Functions)**: VNF에서 CNF로 진화

2. **SDN/NFV와의 융합**:
   - **제어/사용자 평면 분리 (CUPS)**: UPF를 엣지에 분산 배치
   - **동적 슬라이싱**: SDN 컨트롤러가 슬라이스 리소스 동적 할당

3. **AI/ML과의 융합**:
   - **지능형 무선 자원 관리**: 트래픽 패턴 예측, 빔 최적화
   - **자율 네트워크**: 장애 자가 치유, 성능 최적화

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 스마트 팩토리 5G망 구축

**문제 상황**: 자동차 제조 공장에 5G 프라이빗 네트워크를 구축해야 합니다. 산업용 로봇 100대, AGV 50대, 센서 10,000개를 지원해야 합니다.

**기술사의 전략적 의사결정**:

1. **주파수 선정**:
   - **국내: 4.7GHz 대역 (4780~4820MHz)** - 5G 특화망 전용 주파수
   - 또는 **mmWave 28GHz** - 초저지연 필요 구역

2. **슬라이스 설계**:
   ```
   Slice 1 (uRLLC): 산업용 로봇, AGV - 20MHz, 1ms 지연
   Slice 2 (mMTC): 센서 네트워크 - 5MHz, 100ms 지연
   Slice 3 (eMBB): AR 작업 지시 - 10MHz, 10ms 지연
   ```

3. **MEC 배치**:
   - 공장 내 MEC 서버 설치로 <5ms 응답 보장
   - 로봇 제어 명령을 클라우드가 아닌 로컬에서 처리

4. **UPF 배치**:
   - 공장 내 Distributed UPF로 트래픽 로컬 라우팅

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - mmWave만 사용**:
  mmWave는 벽 투과율이 낮아 실내 커버리지 확보가 어렵습니다. Sub-6GHz와 혼용해야 합니다.

- **안티패턴 2 - NSA 모드로 슬라이싱 기대**:
  NSA는 LTE EPC를 사용하므로 완전한 네트워크 슬라이싱이 불가능합니다. uRLLC 서비스에는 SA 모드가 필요합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | 4G LTE | 5G NR | 개선율 |
|----------|--------|-------|--------|
| **다운로드 속도** | 100 Mbps | 2,000 Mbps | 20x |
| **지연 시간** | 30 ms | 1 ms | 30x 단축 |
| **연결 밀도** | 1,000/km² | 100,000/km² | 100x |
| **에너지 효율** | 1x | 10x | 10x |

### 미래 전망 및 진화 방향

- **6G (2030년)**: 1 Tbps, 0.1ms 지연, THz 대역, AI 네이티브
- **5G-Advanced (Rel-18/19)**: XR 확장, RedCap 진화, NTN(위성) 통합
- **O-RAN**: 개방형 RAN으로 벤더 종속 탈피

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **3GPP TS 38.300** | 3GPP | NR and NG-RAN Overall Description |
| **3GPP TS 23.501** | 3GPP | 5G System Architecture |
| **ITU-R M.2083** | ITU | IMT-2020 Vision |
| **GSMA NG.116** | GSMA | 5G Network Slicing |

---

## 관련 개념 맵 (Knowledge Graph)
- [4G LTE/EPC](./lte_epc_architecture.md) - EPC 코어 구조
- [MIMO와 빔포밍](./mimo_beamforming.md) - 안테나 기술
- [네트워크 슬라이싱](../7_cloud/network_slicing.md) - 논리적 망 분리
- [MEC 엣지 컴퓨팅](../7_cloud/mec_edge_computing.md) - 엣지 처리
- [SDN/NFV](../7_cloud/sdn_nfv_architecture.md) - 소프트웨어 정의 네트워크

---

## 어린이를 위한 3줄 비유 설명
1. **5G**는 **초고속 도로**예요. 4G 도로보다 20배 더 넓고 빨라서 많은 차들이 막히지 않고 달릴 수 있어요.
2. **네트워크 슬라이싱**은 **차선 분리**예요. 일반 차선, 버스 전용 차선, 구급차 전용 차선처럼 용도별로 나눕니다.
3. **Massive MIMO**는 **64차선 도로**예요. 한 번에 수십 대의 차가 동시에 지나갈 수 있어요!
