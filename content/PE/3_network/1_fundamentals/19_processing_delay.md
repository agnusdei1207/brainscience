+++
title = "019. 처리 지연 (Processing Delay) - 헤더 검사, 라우팅"
description = "처리 지연의 개념, 라우터/스위치 내부 동작, 하드웨어 가속 기술 및 최적화 방안을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["ProcessingDelay", "RouterArchitecture", "ASIC", "TCAM", "FastPath", "LPM"]
categories = ["studynotes-3_network"]
+++

# 019. 처리 지연 (Processing Delay) - 헤더 검사, 라우팅

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 처리 지연은 라우터나 스위치가 패킷을 수신하여 헤더를 검사하고, 라우팅 테이블을 조회하며, 출력 포트를 결정하는 데 걸리는 시간으로, 소프트웨어 기반은 ms 단위, ASIC 기반은 μs 단위, 최신 스위치는 ns 단위까지 단축됩니다.
> 2. **가치**: 고속 라우터에서는 TCAM(Ternary Content Addressable Memory)을 활용한 병렬 최장 접두사 일치(LPM) 검색으로 10ns 이내의 라우팅 결정이 가능하며, 이는 선속(Line Rate) 처리의 핵심 기술입니다.
> 3. **융합**: 처리 지연 최적화를 위해 Fast Path/Slow Path 분리, ASIC/NP(Network Processor) 활용, P4 프로그래밍 가능 데이터 평면, SmartNIC/DPU 오프로드 등의 기술이 복합적으로 적용됩니다.

---

## I. 개요 (Context & Background)

**처리 지연(Processing Delay)**은 라우터나 스위치가 수신한 패킷의 **헤더를 분석**하고, **라우팅 테이블을 조회**하여 **출력 포트를 결정**하는 데 걸리는 시간입니다. 이는 장비의 **처리 능력(Processing Power)**과 **아키텍처**에 따라 크게 달라집니다.

### 처리 지연의 구성 요소

1. **헤더 검사 (Header Inspection)**:
   - 이더넷 헤더: MAC 주소, VLAN 태그
   - IP 헤더: 목적지 IP, TTL, 체크섬
   - TCP/UDP 헤더: 포트 번호, 시퀀스 번호

2. **라우팅 테이블 조회 (Route Lookup)**:
   - 목적지 IP에 대한 최장 접두사 일치(Longest Prefix Match)
   - L2 스위치: MAC 주소 테이블 조회
   - ACL(Access Control List) 매칭

3. **의사결정 (Decision Making)**:
   - 출력 인터페이스 결정
   - QoS 분류 및 마킹
   - 필터링 및 폴리싱

4. **헤더 수정 (Header Modification)**:
   - TTL 감소, 체크섬 재계산
   - VLAN 태그 추가/제거
   - NAT 주소 변환

**💡 비유**: 처리 지연을 **'우편물 분류 센터'**에 비유할 수 있습니다.

- 우편물(패킷)이 분류 센터(라우터)에 도착합니다.
- 직원(프로세서)이 봉투의 **주소를 읽고**(헤더 검사)
- **어느 지역으로 보낼지 결정하기 위해** 주소록을 확인합니다(라우팅 테이블 조회)
- 적절한 **트럭(출력 포트)**에 싣습니다.

**소프트웨어 기반 분류**: 직원이 주소록을 한 페이지씩 넘겨서 찾습니다 → 수 초 소요
**TCAM 기반 분류**: 자동 분류 기계가 1초에 수만 개를 처리합니다 → 밀리초 이하

**등장 배경 및 발전 과정**:

1. **초기 소프트웨어 라우터 (1980년대)**: UNIX 시스템에서 동작하는 라우터는 CPU가 직접 패킷을 처리하여 ms 단위의 처리 지연이 있었습니다.

2. **ASIC 기반 스위칭 (1990년대)**: 시스코, 주니퍼 등이 전용 ASIC(Application Specific Integrated Circuit)를 개발하여 μs 단위로 처리 지연을 단축했습니다.

3. **TCAM 도입**: 라우팅 테이블 조회를 병렬로 수행하는 TCAM이 도입되어 조회 시간을 ns 단위로 단축했습니다.

4. **NP(Network Processor) 등장**: 프로그래밍 가능하면서도 고속인 네트워크 프로세서가 개발되어 유연성과 성능을 동시에 확보했습니다.

5. **P4와 SmartNIC**: 2010년대 후반부터 P4 언어로 프로그래밍 가능한 데이터 평면과 SmartNIC/DPU가 등장하여 처리 지연을 추가로 단축하고 있습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 상세 역할 | 소요 시간 | 구현 기술 | 비고 |
|---------|------|----------|----------|----------|------|
| **Ingress** | 수신 처리 | 프레임 수신, CRC 검사 | ns~μs | PHY, MAC | H/W |
| **Parsing** | 헤더 파싱 | 필드 추출, 검증 | ns | Parser | H/W |
| **Lookup** | 테이블 조회 | LPM, ACL 매칭 | ns~μs | TCAM, SRAM | H/W |
| **Decision** | 의사결정 | 출력 포트, 액션 | ns | Logic | H/W |
| **Modification** | 헤더 수정 | TTL, 체크섬 | ns | Modifier | H/W |
| **Queuing** | 큐잉 | 출력 큐 할당 | ns | Buffer Mgmt | H/W |
| **Egress** | 송신 처리 | 프레임 송신 | ns | MAC, PHY | H/W |

### 정교한 구조 다이어그램: 라우터 처리 파이프라인

```ascii
================================================================================
[ 라우터 패킷 처리 파이프라인 ]
================================================================================

                               패킷 처리 파이프라인
                                      │
입력 ──────────────────────────────────────────────────────────────> 출력

┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ Ingress │   │ Header  │   │ Table   │   │ Header  │   │ Egress  │
│ Process │──>│ Parsing │──>│ Lookup  │──>│ Modify  │──>│ Process │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
     │             │             │             │             │
     │             │             │             │             │
     ▼             ▼             ▼             ▼             ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│- PHY    │   │- L2 해석 │   │- LPM    │   │- TTL    │   │- 큐잉   │
│  수신   │   │- L3 해석 │   │  검색   │   │  감소   │   │- 스케줄 │
│- CRC    │   │- L4 해석 │   │- ACL    │   │- Checksum│   │- MAC    │
│  검사   │   │- 필드   │   │  매칭   │   │  갱신   │   │  송신   │
│         │   │  추출   │   │- NextHop│   │- VLAN   │   │- PHY    │
│         │   │         │   │  결정   │   │  태그   │   │  송신   │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘


================================================================================
[ Fast Path vs Slow Path 아키텍처 ]
================================================================================

                    ┌─────────────────────────────────────────┐
                    │              패킷 수신                   │
                    └──────────────────┬──────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────────┐
                    │         헤더 분석 및 분류                 │
                    └──────────────────┬──────────────────────┘
                                       │
                    ┌──────────────────┴──────────────────────┐
                    │                                         │
                    ▼                                         ▼
        ┌───────────────────────┐             ┌───────────────────────┐
        │      FAST PATH        │             │      SLOW PATH        │
        │   (하드웨어 가속)      │             │    (소프트웨어 처리)   │
        ├───────────────────────┤             ├───────────────────────┤
        │ • 일반 유니캐스트     │             │ • 제어 패킷           │
        │ • 단순 포워딩        │             │   (OSPF, BGP)         │
        │ • TCAM 기반 조회     │             │ • 예외 상황           │
        │ • 처리 시간: ns~μs   │             │ • 복잡한 기능         │
        │ • 처리량: Tbps       │             │   (Tunnel, IPsec)     │
        │                      │             │ • 처리 시간: μs~ms    │
        │ [ASIC/NP]            │             │ [CPU]                 │
        └───────────────────────┘             └───────────────────────┘
                    │                                         │
                    └──────────────────┬──────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────────┐
                    │              패킷 송신                   │
                    └─────────────────────────────────────────┘


================================================================================
[ TCAM (Ternary Content Addressable Memory) 구조 ]
================================================================================

일반 SRAM vs TCAM:
┌─────────────────────────────────────────────────────────────────┐
│                        일반 SRAM                                │
│   주소  │    데이터                                              │
│   0x00  │    192.168.1.0/24                                     │
│   0x01  │    10.0.0.0/8                                         │
│   ...   │    ...                                                │
│                                                                 │
│   검색: 주소로 접근 → 데이터 읽기 (순차 검색 필요)               │
│   검색 시간: O(N)                                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         TCAM                                    │
│   데이터 (패턴)     │    마스크    │    결과                    │
│   11000000.10101000│    11111111  │    포트 1                  │
│   .00000001.00000000│   .11111111 │                            │
│   00001010.00000000│    11111111  │    포트 2                  │
│   .00000000.00000000│   .00000000 │                            │
│   xxxxxxxx.xxxxxxxx│    00000000  │    기본 경로               │
│                                                                 │
│   검색: 내용으로 병렬 접근 → 모든 엔트리 동시 비교               │
│   검색 시간: O(1) - 단일 클럭 사이클                            │
│   특징: 0, 1, X(Don't Care) 3가지 상태 저장                    │
└─────────────────────────────────────────────────────────────────┘

TCAM 검색 예시:
검색 키: 192.168.1.100
        ↓ 병렬 비교
엔트리 1: 192.168.1.0/24 → 매칭 (마스크 24비트)
엔트리 2: 10.0.0.0/8     → 불일치
엔트리 3: 0.0.0.0/0      → 매칭 (기본 경로)

결과: 가장 긴 마스크(24비트) 매칭 → 포트 1로 포워딩


================================================================================
[ 처리 지연 비교: 다양한 플랫폼 ]
================================================================================

플랫폼                    처리 지연         처리량          비고
────────────────────────────────────────────────────────────────
소프트웨어 라우터 (Linux)   100 μs ~ 1 ms    < 1 Gbps      CPU 기반
엔터프라이즈 라우터         10 ~ 50 μs       10~100 Gbps   ASIC
데이터센터 스위치          1 ~ 5 μs         1~10 Tbps     High-end ASIC
백본 라우터                < 1 μs           100+ Tbps     최신 ASIC + TCAM
SmartNIC                   100 ns ~ 1 μs    100~400 Gbps  FPGA/ASIC
DPU                        50 ~ 500 ns      200+ Gbps     전용 칩


================================================================================
[ 라우팅 테이블 조회 알고리즘 ]
================================================================================

1. 선형 검색 (Linear Search)
   - 모든 엔트리 순차 검색
   - 시간 복잡도: O(N)
   - 소규모 테이블에만 적합

2. 트라이 (Trie) 구조
   - 이진 트리 기반 검색
   - 시간 복잡도: O(W), W = 주소 길이
   - IPv4: 32단계, IPv6: 128단계

3. Patricia 트라이
   - 경로 압축 트라이
   - 메모리 효율 개선
   - 리눅스 커널 기본 알고리즘

4. TCAM
   - 병렬 하드웨어 검색
   - 시간 복잡도: O(1)
   - 고성능 라우터 필수

┌───────────────────────────────────────────────────────────────┐
│                     IPv4 Trie 예시                             │
│                                                               │
│                        Root                                   │
│                       /    \                                  │
│                      0      1                                 │
│                     /        \                                │
│                    0          1                               │
│                   /            \                              │
│              10.0.0.0/8     192.168.0.0/16                   │
│               /    \              \                           │
│          10.0.0.0/16  10.1.0.0/16   192.168.1.0/24           │
│                                                               │
│  검색: 192.168.1.100 → Root-1-1-...-192.168.1.0/24           │
└───────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 라우팅 결정 과정

1. **L2 헤더 처리**:
   - 목적지 MAC 확인: 브로드캐스트, 멀티캐스트, 유니캐스트 분류
   - VLAN 태그 확인 및 분리
   - 이더타입 확인: IPv4(0x0800), IPv6(0x86DD), ARP(0x0806)

2. **L3 헤더 처리**:
   - 목적지 IP 주소 추출
   - TTL 확인 및 감소 (TTL=0이면 ICMP Time Exceeded)
   - 체크섬 검증
   - 옵션 필드 처리 (있는 경우)

3. **라우팅 테이블 조회**:
   - LPM(Longest Prefix Match) 수행
   - 일치하는 엔트리 중 가장 긴 마스크 선택
   - Next-hop IP와 출력 인터페이스 결정

4. **ACL 및 정책 적용**:
   - 방화벽 규칙 매칭
   - QoS 분류 및 마킹
   - 폴리싱(Policing) 및 쉐이핑(Shaping)

5. **헤더 수정**:
   - TTL 감소 및 체크섬 재계산
   - 출발지/목적지 MAC 주소 변경 (L2 다음 홉)
   - VLAN 태그 추가/변경/제거

### 핵심 코드: 라우팅 테이블 조회 시뮬레이터

```python
from dataclasses import dataclass
from typing import List, Optional, Tuple
import ipaddress

@dataclass
class RouteEntry:
    """라우팅 테이블 엔트리"""
    network: str          # CIDR 표기법 (예: "192.168.1.0/24")
    next_hop: str         # 다음 홉 IP
    interface: str        # 출력 인터페이스
    metric: int = 0       # 메트릭 (낮을수록 우선)

    @property
    def prefix_length(self) -> int:
        """프리픽스 길이 반환"""
        return int(self.network.split('/')[1])

    @property
    def network_addr(self) -> int:
        """네트워크 주소를 정수로 반환"""
        return int(ipaddress.ip_network(self.network, strict=False).network_address)

    def matches(self, dest_ip: str) -> bool:
        """목적지 IP가 이 경로와 매칭되는지 확인"""
        dest = ipaddress.ip_address(dest_ip)
        network = ipaddress.ip_network(self.network, strict=False)
        return dest in network

class RoutingTable:
    """
    라우팅 테이블 구현
    """
    def __init__(self):
        self.entries: List[RouteEntry] = []

    def add_route(self, entry: RouteEntry):
        """경로 추가"""
        self.entries.append(entry)
        # 프리픽스 길이 내림차순 정렬 (LPM용)
        self.entries.sort(key=lambda e: e.prefix_length, reverse=True)

    def lookup_linear(self, dest_ip: str) -> Optional[RouteEntry]:
        """
        선형 검색 (소프트웨어 기반)
        시간 복잡도: O(N)
        """
        for entry in self.entries:
            if entry.matches(dest_ip):
                return entry
        return None

    def lookup_lpm(self, dest_ip: str) -> Optional[RouteEntry]:
        """
        최장 접두사 일치 (Longest Prefix Match)
        정렬된 테이블에서 첫 번째 매칭 = 최장 프리픽스
        """
        dest = ipaddress.ip_address(dest_ip)

        best_match = None
        best_prefix_len = -1

        for entry in self.entries:
            network = ipaddress.ip_network(entry.network, strict=False)
            if dest in network and entry.prefix_length > best_prefix_len:
                best_match = entry
                best_prefix_len = entry.prefix_length

        return best_match

class TrieNode:
    """트라이 노드"""
    def __init__(self):
        self.children: dict = {}  # 0, 1
        self.route: Optional[RouteEntry] = None

class IPTrie:
    """
    IP 주소용 트라이 (Trie) 구조
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, entry: RouteEntry):
        """경로 삽입"""
        network = ipaddress.ip_network(entry.network, strict=False)
        prefix_len = entry.prefix_length

        node = self.root
        for i in range(prefix_len):
            # 네트워크 주소의 i번째 비트
            bit = (int(network.network_address) >> (31 - i)) & 1

            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]

        node.route = entry

    def lookup(self, dest_ip: str) -> Optional[RouteEntry]:
        """
        트라이 검색
        시간 복잡도: O(W), W = 주소 길이
        """
        dest = int(ipaddress.ip_address(dest_ip))

        node = self.root
        best_match = None

        for i in range(32):
            bit = (dest >> (31 - i)) & 1

            if node.route:
                best_match = node.route

            if bit not in node.children:
                break
            node = node.children[bit]

        # 마지막 노드 확인
        if node.route:
            best_match = node.route

        return best_match

class TCAM:
    """
    TCAM (Ternary Content Addressable Memory) 시뮬레이터
    """
    @dataclass
    class TCAMEntry:
        pattern: int      # 검색 패턴 (32비트)
        mask: int         # 마스크 (관심 비트 표시)
        entry: RouteEntry

    def __init__(self):
        self.entries: List[TCAM.TCAMEntry] = []

    def insert(self, entry: RouteEntry):
        """TCAM 엔트리 추가"""
        network = ipaddress.ip_network(entry.network, strict=False)
        prefix_len = entry.prefix_length

        # 패턴: 네트워크 주소
        pattern = int(network.network_address)

        # 마스크: 상위 prefix_len 비트만 1
        mask = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF

        self.entries.append(TCAM.TCAMEntry(pattern, mask, entry))
        # 마스크 길이 내림차순 정렬 (우선순위)
        self.entries.sort(key=lambda e: bin(e.mask).count('1'), reverse=True)

    def lookup(self, dest_ip: str) -> Optional[RouteEntry]:
        """
        TCAM 검색 (병렬 검색 시뮬레이션)
        모든 엔트리 동시 비교 → 시간 복잡도 O(1)
        """
        dest = int(ipaddress.ip_address(dest_ip))

        for tcam_entry in self.entries:
            # 패턴 매칭: (dest & mask) == pattern
            if (dest & tcam_entry.mask) == (tcam_entry.pattern & tcam_entry.mask):
                return tcam_entry.entry

        return None

class ProcessingDelayBenchmark:
    """
    처리 지연 벤치마크
    """
    @staticmethod
    def benchmark_lookup(table: RoutingTable, trie: IPTrie, tcam: TCAM,
                        dest_ips: List[str], iterations: int = 1000) -> dict:
        import time

        # 선형 검색
        start = time.perf_counter()
        for _ in range(iterations):
            for ip in dest_ips:
                table.lookup_linear(ip)
        linear_time = (time.perf_counter() - start) / (iterations * len(dest_ips))

        # LPM 검색
        start = time.perf_counter()
        for _ in range(iterations):
            for ip in dest_ips:
                table.lookup_lpm(ip)
        lpm_time = (time.perf_counter() - start) / (iterations * len(dest_ips))

        # 트라이 검색
        start = time.perf_counter()
        for _ in range(iterations):
            for ip in dest_ips:
                trie.lookup(ip)
        trie_time = (time.perf_counter() - start) / (iterations * len(dest_ips))

        # TCAM 검색 (시뮬레이션)
        start = time.perf_counter()
        for _ in range(iterations):
            for ip in dest_ips:
                tcam.lookup(ip)
        tcam_time = (time.perf_counter() - start) / (iterations * len(dest_ips))

        return {
            'linear_us': linear_time * 1_000_000,
            'lpm_us': lpm_time * 1_000_000,
            'trie_us': trie_time * 1_000_000,
            'tcam_us': tcam_time * 1_000_000
        }

# 실무 사용 예시
if __name__ == "__main__":
    # 라우팅 테이블 생성
    routes = [
        RouteEntry("0.0.0.0/0", "10.0.0.1", "eth0"),           # 기본 경로
        RouteEntry("10.0.0.0/8", "10.0.0.254", "eth1"),        # 사설망 A
        RouteEntry("172.16.0.0/12", "172.16.0.1", "eth2"),     # 사설망 B
        RouteEntry("192.168.0.0/16", "192.168.0.1", "eth3"),   # 사설망 C
        RouteEntry("192.168.1.0/24", "192.168.1.1", "eth4"),   # 세부 서브넷
        RouteEntry("8.8.8.0/24", "1.1.1.1", "wan0"),           # Google DNS
    ]

    # 각 구조에 경로 추가
    routing_table = RoutingTable()
    ip_trie = IPTrie()
    tcam = TCAM()

    for route in routes:
        routing_table.add_route(route)
        ip_trie.insert(route)
        tcam.insert(route)

    # 검색 테스트
    test_ips = [
        "8.8.8.8",          # Google DNS
        "192.168.1.100",    # 사설망 세부 서브넷
        "192.168.2.50",     # 사설망 C (다른 서브넷)
        "10.10.10.10",      # 사설망 A
        "1.1.1.1",          # 인터넷 (기본 경로)
    ]

    print("=" * 60)
    print("라우팅 테이블 조회 결과")
    print("=" * 60)

    for ip in test_ips:
        result = routing_table.lookup_lpm(ip)
        if result:
            print(f"{ip:16s} → {result.network:20s} via {result.interface}")
        else:
            print(f"{ip:16s} → 매칭 없음")

    # 성능 비교
    print("\n" + "=" * 60)
    print("조회 알고리즘 성능 비교 (평균 조회 시간)")
    print("=" * 60)

    benchmark = ProcessingDelayBenchmark.benchmark_lookup(
        routing_table, ip_trie, tcam, test_ips, iterations=10000)

    print(f"선형 검색:    {benchmark['linear_us']:8.3f} μs")
    print(f"LPM 검색:     {benchmark['lpm_us']:8.3f} μs")
    print(f"트라이 검색:  {benchmark['trie_us']:8.3f} μs")
    print(f"TCAM 검색:    {benchmark['tcam_us']:8.3f} μs (시뮬레이션)")
