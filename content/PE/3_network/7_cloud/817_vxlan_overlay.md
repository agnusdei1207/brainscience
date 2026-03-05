+++
title = "817. VXLAN (Virtual eXtensible LAN)"
description = "VXLAN 오버레이 네트워킹의 터널링 메커니즘, VTEP 동작, EVPN 제어 평면을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["VXLAN", "Overlay", "VTEP", "EVPN", "DataCenter", "SDN", "Virtualization", "L2Extension"]
categories = ["studynotes-3_network"]
+++

# 817. VXLAN (Virtual eXtensible LAN)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: VXLAN은 L2 이더넷 프레임을 UDP 패킷으로 캡슐화하여 L3 네트워크 위에 논리적 L2 네트워크를 구축하는 오버레이 터널링 기술로, VLAN의 4,096개 한계를 1,600만 개(VNI 24비트)로 확장합니다.
> 2. **가치**: 멀티테넌트 클라우드 환경에서 서로 다른 고객의 가상 네트워크를 격리하면서도, 물리적 스위치 재구성 없이 동적으로 네트워크를 프로비저닝할 수 있습니다.
> 3. **융합**: EVPN(Ethernet VPN)을 제어 평면으로 사용하여 BGP 기반의 MAC 주소 학습, ARP 억제, 멀티캐스트 최적화를 구현하며, 쿠버네티스 CNI와 연동하여 컨테이너 네트워킹의 기반이 됩니다.

---

## Ⅰ. 개요 (Context & Background)

VXLAN(Virtual eXtensible LAN)은 데이터센터 가상화와 멀티테넌시를 위해 개발된 오버레이 네트워킹 기술입니다. 2011년 VMware, Cisco, Arista 등이 주도하여 정의했으며, 현재 IETF RFC 7348로 표준화되어 있습니다. 기존 VLAN의 12비트 ID(4,096개) 한계를 극복하고, L3 네트워크 위에서 L2 세그먼트를 확장할 수 있게 합니다.

**💡 비유**: VXLAN을 **'국제 우편 포워딩 서비스'**에 비유할 수 있습니다.
- **원본 편지(L2 프레임)**는 한국 내 주소(MAC 주소)만 적혀 있습니다.
- **국제 우편 봉투(UDP/IP)**가 편지를 감싸고, 미국 주소(외부 IP)가 적힙니다.
- **VTEP**는 **우편 물류 센터**입니다. 편지를 봉투에 넣고, 봉투를 벗깁니다.
- **VNI**는 **우편 분류 코드**입니다. 같은 코드를 가진 편지는 같은 가상 네트워크에 속합니다.

**등장 배경 및 발전 과정**:
1. **VLAN 한계 (2000년대)**: 12비트 VLAN ID는 최대 4,096개만 지원하며, 멀티테넌트 클라우드(수천 고객)에 부족했습니다.
2. **L2 스트레칭 문제**: 기존 L2 확장은 QinQ, L2TPv3 등을 사용했으나, STP 루프, 브로드캐스트 스톰 문제가 있었습니다.
3. **VXLAN 탄생 (2011년)**: UDP 기반 오버레이로 L3 네트워크 위에서 L2를 터널링합니다.
4. **EVPN 결합 (2015년~)**: BGP EVPN을 제어 평면으로 사용하여 MAC 학습, ARP 억제를 최적화했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### VXLAN 핵심 구성요소

| 구성요소 | 설명 | 비유 |
|----------|------|------|
| **VNI (VXLAN Network Identifier)** | 24비트 가상 네트워크 ID (0 ~ 16,777,215) | 우편 분류 코드 |
| **VTEP (VXLAN Tunnel Endpoint)** | VXLAN 캡슐화/디캡슐화 수행 장치 | 우편 물류 센터 |
| **Overlay Network** | 논리적 L2 네트워크 (VXLAN 터널) | 국제 우편망 |
| **Underlay Network** | 물리적 L3 네트워크 (IP 패브릭) | 실제 도로망 |
| **NVE (Network Virtualization Edge)** | VTEP의 표준 용어 (IETF) | 동일 |

### VXLAN vs VLAN 비교

| 특성 | VLAN (802.1Q) | VXLAN |
|------|--------------|-------|
| **ID 크기** | 12비트 (4,096개) | 24비트 (1,600만 개) |
| **동작 계층** | L2 | L2 over L3 (오버레이) |
| **확장성** | 스위치당 제한 | IP 패브릭까지 확장 |
| **브로드캐스트** | 전파됨 | VTEP에서 처리/억제 |
| **STP 의존** | 높음 | 낮음 (L3 패브릭) |
| **멀티테넌시** | 제한적 | 완벽 지원 |
| **표준** | IEEE 802.1Q | IETF RFC 7348 |

### VXLAN 패킷 구조

```
+------------------------------------------------------------------+
|                    VXLAN Packet Structure                         |
+------------------------------------------------------------------+

[ Outer Headers ]           [ VXLAN Header ]      [ Original Frame ]
+--------------------+      +----------------+    +----------------+
| Outer Ethernet     |      | Flags (8 bits) |    | Inner Ethernet |
| (DA, SA, Ethertype)|      |   - I bit = 1  |    | (DA, SA, Tag)  |
+--------------------+      +----------------+    +----------------+
| Outer IP Header    |      | Reserved (24)  |    | Inner IP       |
| (Src, Dst, Proto)  |      +----------------+    | Header         |
| Proto = UDP (17)   |      | VNI (24 bits)  |    +----------------+
+--------------------+      +----------------+    | Payload        |
| Outer UDP Header   |      | Reserved (8)   |    +----------------+
| Dst Port = 4789    |      +----------------+    | Inner FCS      |
| (VXLAN Port)       |                             +----------------+
+--------------------+

총 오버헤드: 50바이트
- Outer Ethernet: 14바이트
- Outer IP: 20바이트
- Outer UDP: 8바이트
- VXLAN Header: 8바이트
```

### 정교한 구조 다이어그램: VXLAN 데이터센터 아키텍처

```ascii
================================================================================
[ VXLAN Data Center Architecture: Spine-Leaf with Overlay ]
================================================================================

                           [ Spine Layer ]
                    +-----------+   +-----------+
                    |  Spine 1  |   |  Spine 2  |
                    |  (L3)     |   |  (L3)     |
                    +-----|-----+   +-----|-----+
                          |               |
          +---------------+-------+-------+---------------+
          |                       |                       |
          v                       v                       v
    +-----------+           +-----------+           +-----------+
    |  Leaf 1   |           |  Leaf 2   |           |  Leaf 3   |
    |  (VTEP)   |           |  (VTEP)   |           |  (VTEP)   |
    +-----------+           +-----------+           +-----------+
          |                       |                       |
    +-----+-----+           +-----+-----+                 |
    |           |           |           |                 |
    v           v           v           v                 v
+-------+   +-------+   +-------+   +-------+       +-------+
| VM-A  |   | VM-B  |   | VM-C  |   | VM-D  |       | VM-E  |
| VNI   |   | VNI   |   | VNI   |   | VNI   |       | VNI   |
| 10010 |   | 10020 |   | 10010 |   | 10020 |       | 10010 |
+-------+   +-------+   +-------+   +-------+       +-------+

================================================================================
[ VXLAN Encapsulation/Decapsulation Process ]
================================================================================

[ 송신 VTEP (Leaf 1) ]               [ 수신 VTEP (Leaf 2) ]

원본 L2 프레임:
+----------------------------------+
| Dst MAC: AA:BB:CC:00:00:02       |
| Src MAC:  AA:BB:CC:00:00:01       |
| Type:    0x0800 (IPv4)            |
| Payload: IP Packet                |
| FCS:     CRC                       |
+----------------------------------+
              |
              v
캡슐화 (Encapsulation):
+------------------------------------------+
| Outer Ethernet: Leaf2 MAC -> Leaf1 MAC  |
| Outer IP:        Leaf1 IP -> Leaf2 IP   |
| Outer UDP:       Src Port, Dst=4789     |
| VXLAN Header:    VNI = 10010            |
| +----------------------------------+    |
| | Dst MAC: AA:BB:CC:00:00:02       |    |
| | Src MAC:  AA:BB:CC:00:00:01       |    |
| | Payload: IP Packet                |    |
| | FCS:     CRC                       |    |
| +----------------------------------+    |
+------------------------------------------+
              |
              | IP 패브릭 전송
              v
        +-----------+    +-----------+
        |  Spine    | -> |  Spine    |
        +-----------+    +-----------+
              |
              v
디캡슐화 (Decapsulation):
+----------------------------------+
| Dst MAC: AA:BB:CC:00:00:02       |  <-- 원본 L2 프레임 복원
| Src MAC:  AA:BB:CC:00:00:01       |
| Payload: IP Packet                |
+----------------------------------+
              |
              v
        +-------+
        | VM-C  | (VNI 10010)
        +-------+

================================================================================
[ EVPN-VXLAN Control Plane ]
================================================================================

        [ BGP EVPN Route Exchange ]

    Leaf 1 (VTEP)                    Leaf 2 (VTEP)
    +-----------+                    +-----------+
    | BGP       |                    | BGP       |
    | Speaker   |                    | Speaker   |
    +-----------+                    +-----------+
          |                                |
          |  EVPN Type-2 Route (MAC/IP)    |
          |  ----------------------------> |
          |  MAC: AA:BB:CC:00:00:01        |
          |  IP:  10.1.1.10                |
          |  VNI: 10010                    |
          |  Next-Hop: Leaf1_IP            |
          |                                |
          |  <---------------------------- |
          |  EVPN Type-2 Route (MAC/IP)    |
          |  MAC: AA:BB:CC:00:00:02        |
          |  IP:  10.1.1.20                |
          |  VNI: 10010                    |
          |  Next-Hop: Leaf2_IP            |
          +--------------------------------+

    EVPN Route Types:
    - Type-1: Ethernet Auto-Discovery (멀티홈)
    - Type-2: MAC/IP Advertisement (MAC 학습)
    - Type-3: Inclusive Multicast (BUM 트래픽)
    - Type-4: Ethernet Segment (ESI)
    - Type-5: IP Prefix (L3 라우팅)
```

### 심층 동작 원리: VTEP MAC 학습 과정

**1. 데이터 평면 학습 (기존 VXLAN)**:
```
VM-A (MAC_A) -> VM-C (MAC_C) 전송:

1. VM-A가 VM-C의 MAC을 모름 → ARP 요청 (브로드캐스트)
2. VTEP Leaf 1이 ARP를 받음
3. Leaf 1은 ARP를 모든 VTEP로 멀티캐스트/유니캐스트 헤드엔드 복제
4. Leaf 2가 ARP를 받아 VM-C에게 전달
5. VM-C가 ARP 응답 → Leaf 2가 Leaf 1로 유니캐스트
6. Leaf 1이 MAC_C 학습 (데이터 평면)
```

**2. EVPN 제어 평면 학습 (최신)**:
```
EVPN BGP 기반 학습:

1. VM-A가 VM-C의 MAC을 모름 → ARP 요청
2. Leaf 1이 ARP를 캡처하고, BGP EVPN Type-2로 광고
3. 모든 VTEP가 BGP를 통해 MAC_C를 학습
4. Leaf 1은 이미 MAC_C를 알고 있음 → ARP 억제 (Proxy ARP)
5. VM-A의 ARP 요청 없이 바로 유니캐스트 전송 가능
```

### 핵심 코드: VXLAN 패킷 파싱 및 분석 (Python)

```python
import struct
from dataclasses import dataclass
from typing import Optional, Tuple
import socket

@dataclass
class VXLANHeader:
    """VXLAN 헤더 구조"""
    flags: int          # 8비트 플래그 (I 비트 포함)
    reserved1: int      # 24비트 예약
    vni: int            # 24비트 VXLAN Network Identifier
    reserved2: int      # 8비트 예약

    @property
    def is_valid(self) -> bool:
        """I 비트가 설정되어 있는지 확인"""
        return bool(self.flags & 0x08)

    @classmethod
    def parse(cls, data: bytes) -> 'VXLANHeader':
        """바이트에서 VXLAN 헤더 파싱"""
        if len(data) < 8:
            raise ValueError("VXLAN 헤더는 최소 8바이트 필요")

        # VXLAN 헤더: 4바이트 + 4바이트
        # Flags (1) + Reserved (3) + VNI (3) + Reserved (1)
        flags = data[0]
        reserved1 = struct.unpack('!I', b'\x00' + data[1:4])[0]

        # VNI는 3바이트
        vni_bytes = data[4:7]
        vni = (vni_bytes[0] << 16) | (vni_bytes[1] << 8) | vni_bytes[2]

        reserved2 = data[7]

        return cls(
            flags=flags,
            reserved1=reserved1,
            vni=vni,
            reserved2=reserved2
        )

    def pack(self) -> bytes:
        """VXLAN 헤더를 바이트로 변환"""
        header = bytearray(8)
        header[0] = self.flags | 0x08  # I 비트 설정
        # VNI는 3바이트
        header[4] = (self.vni >> 16) & 0xFF
        header[5] = (self.vni >> 8) & 0xFF
        header[6] = self.vni & 0xFF
        return bytes(header)


@dataclass
class VTEPEndpoint:
    """VTEP 엔드포인트 정보"""
    vtep_ip: str
    vtep_mac: str
    vni_list: list
    port: int = 4789  # VXLAN 표준 포트

    def is_vxlan_port(self, port: int) -> bool:
        """VXLAN 포트인지 확인"""
        return port == self.port


@dataclass
class EthernetFrame:
    """이더넷 프레임"""
    dst_mac: str
    src_mac: str
    ethertype: int
    payload: bytes
    vlan_tag: Optional[int] = None

    @classmethod
    def parse(cls, data: bytes) -> 'EthernetFrame':
        """이더넷 프레임 파싱"""
        if len(data) < 14:
            raise ValueError("이더넷 프레임은 최소 14바이트 필요")

        dst_mac = ':'.join(f'{b:02x}' for b in data[0:6])
        src_mac = ':'.join(f'{b:02x}' for b in data[6:12])
        ethertype = struct.unpack('!H', data[12:14])[0]

        offset = 14
        vlan_tag = None

        # VLAN 태그 확인 (0x8100)
        if ethertype == 0x8100:
            vlan_tag = struct.unpack('!H', data[14:16])[0]
            ethertype = struct.unpack('!H', data[16:18])[0]
            offset = 18

        payload = data[offset:]

        return cls(
            dst_mac=dst_mac,
            src_mac=src_mac,
            ethertype=ethertype,
            payload=payload,
            vlan_tag=vlan_tag
        )


class VXLANPacketProcessor:
    """
    VXLAN 패킷 처리기
    캡슐화, 디캡슐화, 분석 기능
    """

    VXLAN_PORT = 4789
    VXLAN_HEADER_SIZE = 8

    def __init__(self, local_vtep_ip: str):
        self.local_vtep_ip = local_vtep_ip
        self.vni_table: dict = {}  # VNI -> VLAN 매핑
        self.mac_table: dict = {}  # MAC -> VTEP IP 매핑 (데이터 평면 학습)

    def encapsulate(self, inner_frame: bytes, vni: int,
                    dst_vtep_ip: str, src_vtep_mac: str,
                    dst_vtep_mac: str) -> bytes:
        """
        L2 프레임을 VXLAN으로 캡슐화

        Args:
            inner_frame: 원본 이더넷 프레임
            vni: VXLAN Network Identifier
            dst_vtep_ip: 목적지 VTEP IP
            src_vtep_mac: 송신 VTEP MAC
            dst_vtep_mac: 수신 VTEP MAC

        Returns:
            캡슐화된 VXLAN 패킷
        """
        # VXLAN 헤더 생성
        vxlan_header = VXLANHeader(
            flags=0x08,  # I 비트 설정
            reserved1=0,
            vni=vni,
            reserved2=0
        )

        # UDP 헤더 (간소화)
        src_port = 12345  # 임의의 소스 포트
        dst_port = self.VXLAN_PORT
        udp_length = 8 + self.VXLAN_HEADER_SIZE + len(inner_frame)
        udp_checksum = 0  # IPv4에서 선택사항

        udp_header = struct.pack(
            '!HHHH',
            src_port,
            dst_port,
            udp_length,
            udp_checksum
        )

        # 외부 IP 헤더 (간소화 - 실제로는 20바이트+)
        outer_ip = self._build_outer_ip_header(
            src_ip=self.local_vtep_ip,
            dst_ip=dst_vtep_ip,
            protocol=17,  # UDP
            payload_len=udp_length
        )

        # 외부 이더넷 헤더
        outer_eth = self._build_outer_ethernet_header(
            dst_mac=dst_vtep_mac,
            src_mac=src_vtep_mac,
            ethertype=0x0800  # IPv4
        )

        # 전체 패킷 조립
        packet = (
            outer_eth +
            outer_ip +
            udp_header +
            vxlan_header.pack() +
            inner_frame
        )

        return packet

    def decapsulate(self, vxlan_packet: bytes) -> Tuple[bytes, int, dict]:
        """
        VXLAN 패킷 디캡슐화

        Args:
            vxlan_packet: 수신된 VXLAN 패킷

        Returns:
            (내부 프레임, VNI, 메타데이터)
        """
        # 외부 이더넷 헤더 건너뛰기 (14바이트)
        offset = 14

        # 외부 IP 헤더 파싱
        ip_version = (vxlan_packet[offset] >> 4) & 0x0F
        ip_header_len = (vxlan_packet[offset] & 0x0F) * 4

        outer_src_ip = socket.inet_ntoa(vxlan_packet[offset+12:offset+16])
        outer_dst_ip = socket.inet_ntoa(vxlan_packet[offset+16:offset+20])

        offset += ip_header_len

        # UDP 헤더 파싱
        src_port, dst_port, udp_len, checksum = struct.unpack(
            '!HHHH',
            vxlan_packet[offset:offset+8]
        )

        if dst_port != self.VXLAN_PORT:
            raise ValueError(f"VXLAN 포트가 아님: {dst_port}")

        offset += 8

        # VXLAN 헤더 파싱
        vxlan_header = VXLANHeader.parse(vxlan_packet[offset:offset+8])
        vni = vxlan_header.vni

        offset += 8

        # 내부 프레임 추출
        inner_frame = vxlan_packet[offset:]

        # MAC 학습 (데이터 평면)
        inner_eth = EthernetFrame.parse(inner_frame)
        self.mac_table[inner_eth.src_mac] = outer_src_ip

        metadata = {
            'outer_src_ip': outer_src_ip,
            'outer_dst_ip': outer_dst_ip,
            'vni': vni,
            'inner_src_mac': inner_eth.src_mac,
            'inner_dst_mac': inner_eth.dst_mac,
            'inner_ethertype': hex(inner_eth.ethertype)
        }

        return inner_frame, vni, metadata

    def _build_outer_ip_header(self, src_ip: str, dst_ip: str,
                                protocol: int, payload_len: int) -> bytes:
        """외부 IP 헤더 생성 (간소화)"""
        version_ihl = (4 << 4) | 5  # IPv4, 20바이트 헤더
        tos = 0
        total_length = 20 + payload_len
        identification = 0
        flags_offset = 0
        ttl = 64
        checksum = 0  # 실제로는 계산 필요

        src_bytes = socket.inet_aton(src_ip)
        dst_bytes = socket.inet_aton(dst_ip)

        header = struct.pack(
            '!BBHHHBBH4s4s',
            version_ihl,
            tos,
            total_length,
            identification,
            flags_offset,
            ttl,
            protocol,
            checksum,
            src_bytes,
            dst_bytes
        )

        return header

    def _build_outer_ethernet_header(self, dst_mac: str, src_mac: str,
                                      ethertype: int) -> bytes:
        """외부 이더넷 헤더 생성"""
        dst_bytes = bytes.fromhex(dst_mac.replace(':', ''))
        src_bytes = bytes.fromhex(src_mac.replace(':', ''))

        return dst_bytes + src_bytes + struct.pack('!H', ethertype)

    def get_mac_table(self) -> dict:
        """MAC 테이블 반환"""
        return self.mac_table.copy()


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("[ VXLAN Packet Processor ]")
    print("=" * 60)

    # VTEP 인스턴스 생성
    vtep = VXLANPacketProcessor(local_vtep_ip="10.0.0.1")

    # 샘플 내부 프레임 생성 (이더넷 + IP)
    inner_frame = bytes.fromhex(
        "ffffffffffff"  # Dst MAC (브로드캐스트)
        "001122334455"  # Src MAC
        "0800"          # Ethertype (IPv4)
        "4500003c0000000040010000"  # IP 헤더 (간소화)
        + b"0" * 40     # 페이로드
    )

    print("\n[ VXLAN 캡슐화 ]")
    print(f"  내부 프레임 크기: {len(inner_frame)} 바이트")
    print(f"  VNI: 10010")

    # 캡슐화
    vxlan_packet = vtep.encapsulate(
        inner_frame=inner_frame,
        vni=10010,
        dst_vtep_ip="10.0.0.2",
        src_vtep_mac="00:11:22:33:44:55",
        dst_vtep_mac="66:77:88:99:AA:BB"
    )

    print(f"  VXLAN 패킷 크기: {len(vxlan_packet)} 바이트")
    print(f"  오버헤드: {len(vxlan_packet) - len(inner_frame)} 바이트")

    # 디캡슐화
    print("\n[ VXLAN 디캡슐화 ]")
    inner, vni, metadata = vtep.decapsulate(vxlan_packet)

    print(f"  VNI: {vni}")
    print(f"  외부 출발지 IP: {metadata['outer_src_ip']}")
    print(f"  내부 출발지 MAC: {metadata['inner_src_mac']}")
    print(f"  내부 목적지 MAC: {metadata['inner_dst_mac']}")

    # MAC 테이블 확인
    print("\n[ MAC 테이블 ]")
    for mac, vtep_ip in vtep.get_mac_table().items():
        print(f"  {mac} -> {vtep_ip}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 오버레이 기술 비교

| 특성 | VXLAN | NVGRE | STT | GENEVE |
|------|-------|-------|-----|--------|
| **캡슐화** | UDP (4789) | GRE | TCP-like | UDP (6081) |
| **VNI 크기** | 24비트 | 24비트 | 64비트 | 가변 |
| **표준** | RFC 7348 | Microsoft | VMware | RFC 8926 |
| **하드웨어 지원** | 넓음 | 좁음 | 좁음 | 증가 |
| **로드밸런싱** | 우수 (UDP 해시) | 제한적 | 우수 | 우수 |
| **주요 용도** | 데이터센터 | Hyper-V | NSX | 통합 |

### EVPN-VXLAN vs 전통적 VXLAN

| 특성 | 전통적 VXLAN | EVPN-VXLAN |
|------|-------------|------------|
| **MAC 학습** | 데이터 평면 (플러딩) | 제어 평면 (BGP) |
| **ARP 처리** | 브로드캐스트 | 프록시 ARP/억제 |
| **멀티캐스트** | 필수 | 선택적 (헤드엔드 복제) |
| **루프 방지** | 없음 | EVPN Split Horizon |
| **멀티홈** | LACP | EVPN Multi-homing |
| **L3 라우팅** | 외부 라우터 필요 | Distributed Anycast GW |

### 과목 융합 관점 분석

1. **쿠버네티스와의 융합**:
   - **CNI 플러그인**: Calico, Cilium, Flannel이 VXLAN 사용
   - **파드 네트워킹**: 파드 간 통신을 위해 VXLAN 오버레이 구성
   - **Network Policy**: VXLAN 위에 보안 정책 적용

2. **SDN과의 융합**:
   - **SDN 컨트롤러**: VTEP 구성, VNI 할당 자동화
   - **트래픽 엔지니어링**: ECMP로 VXLAN 터널 부하 분산

3. **보안과의 융합**:
   - **마이크로 세그멘테이션**: VNI별 보안 정책
   - **암호화**: IPsec과 결합하여 VXLAN 암호화

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 멀티테넌트 클라우드 VXLAN 설계

**문제 상황**: 100개 테넌트를 지원하는 프라이빗 클라우드 네트워크를 설계합니다. 각 테넌트는 격리된 네트워크가 필요합니다.

**기술사의 전략적 의사결정**:

1. **VNI 할당 정책**:
   ```
   VNI 범위: 10000 ~ 99999 (89,999개 사용 가능)
   할당 규칙:
   - 10000 ~ 19999: 프로덕션 테넌트
   - 20000 ~ 29999: 개발/테스트 테넌트
   - 30000 ~ 39999: DMZ 세그먼트
   - 40000 ~ 49999: 관리 네트워크
   ```

2. **Underlay 설계**:
   - **Spine-Leaf**: 2단계 Clos 패브릭
   - **IP 주소**: 10.0.0.0/8 (Spine), 10.1.0.0/16 (Leaf)
   - **ECMP**: 최대 8경로 부하 분산

3. **EVPN 설정**:
   ```
   - BGP AS: 65000 (Spine), 65001-65100 (Leaf)
   - Route Reflector: Spine 2대
   - EVPN Address Family 활성화
   ```

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - 과도한 VNI 사용**:
  하나의 테넌트가 수십 개의 VNI를 사용하면 관리 복잡도가 급증합니다. 테넌트당 3~5개 VNI로 제한합니다.

- **안티패턴 2 - MTU 미조정**:
  VXLAN 오버헤드(50바이트)를 고려하지 않으면 단편화가 발생합니다. Underlay MTU를 최소 1600바이트로 설정합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | VLAN | VXLAN |
|----------|------|-------|
| **네트워크 세그먼트** | 4,096 | 16,777,216 |
| **프로비저닝 시간** | 시간 | 분 |
| **물리적 재구성** | 필요 | 불필요 |
| **멀티테넌시** | 제한적 | 완벽 지원 |

### 미래 전망 및 진화 방향

- **GENEVE**: VXLAN의 한계를 극복한 유연한 오버레이 프로토콜
- **SRv6 over VXLAN**: Segment Routing과 VXLAN 결합
- **eBPF 기반 VXLAN**: 커널 레벨 고성능 캡슐화

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **RFC 7348** | IETF | VXLAN Protocol |
| **RFC 8365** | IETF | EVPN for VXLAN |
| **RFC 8926** | IETF | GENEVE Protocol |

---

## 관련 개념 맵 (Knowledge Graph)
- [EVPN](./evpn_bgp_overlay.md) - BGP 기반 제어 평면
- [Spine-Leaf 아키텍처](./spine_leaf_architecture.md) - 데이터센터 패브릭
- [SDN/NFV](../6_sdn_nfv/sdn_nfv_architecture.md) - 소프트웨어 정의 네트워크
- [컨테이너 네트워킹 (CNI)](./container_networking_cni.md) - 쿠버네티스 네트워크
- [NVGRE vs VXLAN](./overlay_comparison.md) - 오버레이 기술 비교

---

## 어린이를 위한 3줄 비유 설명
1. **VXLAN**은 **국제 우편 봉투**와 같아요. 한국 편지를 미국 봉투에 넣어서 보냅니다.
2. **VTEP**는 **우체국**이에요. 편지를 봉투에 넣고, 봉투를 벗기는 일을 합니다.
3. **VNI**는 **우편 분류 코드**예요. 같은 코드를 가진 편지끼리만 서로 볼 수 있어요!
