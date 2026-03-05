+++
title = "357. OSPF (Open Shortest Path First)"
description = "OSPF 링크 상태 라우팅 프로토콜의 동작 원리, Area 구조, LSA 타입, SPF 알고리즘을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["OSPF", "LinkState", "SPF", "Dijkstra", "LSA", "Area", "IGP", "Routing"]
categories = ["studynotes-3_network"]
+++

# 357. OSPF (Open Shortest Path First)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OSPF는 링크 상태(Link State) 라우팅 프로토콜로, 각 라우터가 네트워크 토폴로지의 완전한 지도(LSDB)를 구축하고 다익스트라 SPF(Shortest Path First) 알고리즘으로 최적 경로를 계산합니다.
> 2. **가치**: 대규모 엔터프라이즈 네트워크에서 계층적 Area 구조를 통해 확장성을 제공하며, 1초 이내의 빠른 컨버전스와 ECMP(Equal-Cost Multi-Path)를 통한 부하 분산을 지원합니다.
> 3. **융합**: OSPFv3는 IPv6를 지원하며, SDN 컨트롤러와 연동하여 중앙 집중식 정책 기반 라우팅과 트래픽 엔지니어링(TE) 확장을 가능하게 합니다.

---

## Ⅰ. 개요 (Context & Background)

OSPF(Open Shortest Path First)는 IETF에서 표준화한 링크 상태 기반 내부 게이트웨이 프로토콜(IGP)입니다. RIP와 같은 거리 벡터 프로토콜의 한계(홉 카운트 제한, 느린 컨버전스, 루프 문제)를 극복하기 위해 개발되었으며, 현재 엔터프라이즈 및 데이터센터 네트워크에서 가장 널리 사용되는 IGP입니다.

**💡 비유**: OSPF를 **'네비게이션 시스템'**에 비유할 수 있습니다.
- **링크 상태 데이터베이스(LSDB)**는 **전국 도로 지도**입니다. 모든 도로(링크)의 상태(대역폭, 지연, 혼잡도)를 알고 있습니다.
- **SPF 알고리즘**은 **최단 경로 탐색 엔진**입니다. 출발지에서 목적지까지 가장 빠른 경로를 계산합니다.
- **Area**는 **지역 단위**입니다. 서울 지도, 경기 지도, 부산 지도로 나누어 관리하면 전체 지도를 매번 업데이트할 필요가 없습니다.
- **LSA**는 **도로 공사 알림**입니다. "강변북로 10km 구간 정체"와 같은 정보를 인접 지역에 전파합니다.

**등장 배경 및 발전 과정**:
1. **RIP의 한계 (1980년대)**: RIP는 최대 15홉 제한, 30초 주기 업데이트, 서브넷 마스크 미지원 등 대규모 네트워크에 부적합했습니다.
2. **OSPF 탄생 (1989년)**: RFC 1131로 OSPFv1이 발표되었으나, 실험적이었습니다. 1991년 RFC 1247(OSPFv2)이 실질적인 표준이 되었습니다.
3. **IPv6 지원 (1999년)**: RFC 2740으로 OSPFv3가 발표되어 IPv6를 지원하게 되었습니다.
4. **현대적 확장**: MPLS Traffic Engineering, Segment Routing, SDN 연동 등으로 진화했습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### OSPF 핵심 개념 및 용어

| 용어 | 설명 | 비유 |
|------|------|------|
| **Router ID** | OSPF 라우터 식별자 (32비트, IP 형식) | 주민등록번호 |
| **Area** | 논리적 라우팅 도메인 그룹 (0~4,294,967,295) | 행정구역 |
| **Area 0 (Backbone)** | 중심 Area, 모든 Area는 Area 0과 연결되어야 함 | 수도권 |
| **LSDB** | Link State Database, 토폴로지 정보 저장소 | 도로 지도 |
| **LSA** | Link State Advertisement, 링크 상태 정보 광고 | 도로 정보 알림 |
| **SPF** | Shortest Path First (Dijkstra 알고리즘) | 최단 경로 계산 |
| **Cost** | 링크 비용 (기본: 10^8 / 대역폭) | 통행료 |
| **DR/BDR** | Designated Router / Backup DR, 멀티액세스 네트워크 대표 | 반장/부반장 |
| **Adjacency** | 인접성, LSA 교환을 위한 논리적 연결 | 친구 관계 |
| **Neighbor** | 물리적으로 직접 연결된 라우터 | 이웃 |

### OSPF Area 계층 구조

| Area 타입 | 설명 | LSA 제한 | 용도 |
|----------|------|----------|------|
| **Backbone (Area 0)** | 중심 Area, 모든 트래픽 통과 | 없음 | 코어 네트워크 |
| **Standard Area** | 일반 Area, Area 0과 연결 | 모든 LTA 수신 | 일반 지역 |
| **Stub Area** | 외부 경로(Type 5 LSA) 차단 | Type 1,2,3,4만 | 소규모 지역 |
| **Totally Stubby** | Type 3,4,5 모두 차단, 기본 경로만 | Type 1,2만 | 원격 지사 |
| **NSSA** | Type 5 차단, Type 7 허용 | Type 1,2,3,4,7 | 외부 연결 필요 지역 |
| **Totally NSSA** | Type 3,4,5 차단, Type 7 허용 | Type 1,2,7만 | 특수 지역 |

### OSPF LSA 타입 상세

| LSA 타입 | 명칭 | 생성자 | 범위 | 내용 |
|----------|------|--------|------|------|
| **Type 1** | Router LSA | 모든 라우터 | Area 내 | 라우터의 링크 정보 |
| **Type 2** | Network LSA | DR | Area 내 | 멀티액세스 네트워크 정보 |
| **Type 3** | Summary LSA (Network) | ABR | Area 간 | 다른 Area의 네트워크 요약 |
| **Type 4** | Summary LSA (ASBR) | ABR | Area 간 | ASBR 위치 정보 |
| **Type 5** | AS External LSA | ASBR | 전체 AS | 외부 경로 정보 |
| **Type 7** | NSSA External LSA | ASBR | NSSA 내 | NSSA 내 외부 경로 |

### 정교한 구조 다이어그램: OSPF Area 및 라우터 역할

```ascii
================================================================================
[ OSPF Hierarchical Area Architecture ]
================================================================================

                    [ 인터넷 (External AS) ]
                            |
                            | BGP
                            v
    +-----------------------+-----------------------+
    |                  ASBR                        |  <-- Autonomous System
    |          (Autonomous System Boundary         |      Boundary Router
    |              Router)                         |
    +-----------------------|-----------------------+
                            | Type 5 LSA
                            v
    +-----------------------+-----------------------+
    |              AREA 0 (Backbone)                |
    |  +-----------------------------------------+  |
    |  |           Backbone Routers              |  |
    |  |    R1 <-------> R2 <-------> R3         |  |
    |  |     |             |             |       |  |
    |  +-----|-------------|-------------|-------+  |
    |        |             |             |          |
    +--------|-------------|-------------|----------+
             | ABR         | ABR         | ABR
             | (Area       | (Area       | (Area
             |  Border     |  Border     |  Border
             |  Router)    |  Router)    |  Router)
             v             v             v
    +--------+----+  +-----+-----+  +----+--------+
    |  AREA 1     |  |  AREA 2   |  |  AREA 3     |
    | (Standard)  |  | (Stub)    |  | (NSSA)      |
    |             |  |           |  |             |
    |  R4--R5--R6 |  | R7--R8    |  | R9--R10     |
    |  |        |  |  |      |   |  |  |      |   |
    | Host    Host|  | Host Host|  |  | Host Host|  |
    +-------------+  +----------+  |  +-----------+
                                   |  +-----------+
                                   |  | External   |
                                   +--| Network    |
                                      +-----------+

================================================================================
[ OSPF Router Types and LSA Flow ]
================================================================================

[ Internal Router ]         [ ABR ]              [ ASBR ]
+----------------+     +----------------+     +----------------+
|  Area 1 Only   |     | Area 0 + Area 1|     | OSPF + BGP     |
|                |     |                |     |                |
| Type 1 LSA     |     | Type 1,2,3,4   |     | Type 1,2,5,7   |
| Type 2 LSA     |     | LSA 생성       |     | LSA 생성       |
| (if DR)        |     | (경로 요약)    |     | (외부 경로     |
|                |     |                |     |  재분배)       |
+----------------+     +----------------+     +----------------+

LSA 플러딩 방향:
  Internal Router --> ABR --> Backbone --> 다른 ABR --> 다른 Area

================================================================================
[ OSPF Packet Types ]
================================================================================

Type 1: Hello Packet
  - Neighbor 발견 및 유지
  - DR/BDR 선출
  - 주기: 기본 10초 (Broadcast), 30초 (NBMA)

Type 2: Database Description (DBD)
  - LSDB 요약 정보 교환
  - Master-Slave 관계 형성

Type 3: Link State Request (LSR)
  - 누락된 LSA 요청

Type 4: Link State Update (LSU)
  - 실제 LSA 전송
  - 유니캐스트 또는 멀티캐스트 (224.0.0.5/6)

Type 5: Link State Acknowledgment (LSAck)
  - LSA 수신 확인

================================================================================
[ SPF Algorithm Visualization (Dijkstra) ]
================================================================================

      Cost: 10        Cost: 20         Cost: 10
    R1 ======== R2 =========== R3 ======== R4
     |          |              |          |
     | Cost: 30 | Cost: 10     | Cost: 15 |
     |          |              |          |
    R5 ======== R6 =========== R7 ======== R8
      Cost: 40        Cost: 5          Cost: 25

R1에서 R8로 가는 최단 경로 계산:
  경로 1: R1-R2-R3-R4-R8 = 10+20+10+25 = 65
  경로 2: R1-R2-R6-R7-R8 = 10+10+5+25 = 50  <-- 최단!
  경로 3: R1-R5-R6-R7-R8 = 30+40+5+25 = 100

SPF 트리 (R1 기준):
    R1
    |-- R2 (10)
    |   |-- R6 (10+10=20)
    |   |   |-- R7 (20+5=25)
    |   |   |   |-- R8 (25+25=50) ✓
    |   |-- R3 (10+20=30)
    |-- R5 (30)
```

### 심층 동작 원리: OSPF 상태 머신

**OSPF Neighbor 상태 전이**:

```
Down --> Init --> 2-Way --> ExStart --> Exchange --> Loading --> Full

1. Down: 초기 상태, Hello 미수신
2. Init: Hello 수신했으나 자신의 Router ID 미포함
3. 2-Way: 양방향 통신 확립 (자신의 Router ID 포함된 Hello 수신)
   - Point-to-Point: 바로 ExStart로
   - Broadcast/NBMA: DR/BDR 선출 후 ExStart로
4. ExStart: Master-Slave 결정, DBD 시퀀스 번호 초기화
5. Exchange: DBD 패킷 교환, LSDB 요약 정보 공유
6. Loading: LSR/LSU로 상세 LSA 요청 및 수신
7. Full: 인접성 완료, LSDB 동기화 완료
```

### 핵심 코드: OSPF 비용 계산 및 경로 분석 (Python)

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
import heapq
import ipaddress

@dataclass
class Link:
    """OSPF 링크 정보"""
    local_router: str
    remote_router: str
    local_interface: str
    remote_interface: str
    bandwidth_mbps: int
    cost: int = 0
    area: str = "0"

    def __post_init__(self):
        """OSPF Cost 자동 계산: 10^8 / 대역폭(bps)"""
        if self.cost == 0:
            reference_bandwidth = 100_000_000  # 100 Mbps (OSPF 기본 참조 대역폭)
            self.cost = max(1, reference_bandwidth // (self.bandwidth_mbps * 1_000_000))

    def __hash__(self):
        return hash((self.local_router, self.remote_router))


@dataclass
class OSPFRouter:
    """OSPF 라우터 정보"""
    router_id: str
    router_type: str  # "Internal", "ABR", "ASBR", "Backbone"
    interfaces: Dict[str, str] = field(default_factory=dict)  # interface_name: ip
    lsdb: Dict[str, dict] = field(default_factory=dict)  # LSA 저장


class OSPFNetworkSimulator:
    """
    OSPF 네트워크 시뮬레이터
    SPF 알고리즘 구현 및 경로 계산
    """

    def __init__(self, reference_bandwidth: int = 100_000_000):
        """
        Args:
            reference_bandwidth: OSPF 참조 대역폭 (기본 100 Mbps)
        """
        self.ref_bw = reference_bandwidth
        self.routers: Dict[str, OSPFRouter] = {}
        self.links: List[Link] = []
        self.topology: Dict[str, Dict[str, int]] = defaultdict(dict)  # adj_list with costs

    def add_router(self, router_id: str, router_type: str = "Internal"):
        """라우터 추가"""
        self.routers[router_id] = OSPFRouter(
            router_id=router_id,
            router_type=router_type
        )

    def add_link(self, r1: str, r2: str, bandwidth_mbps: int,
                 area: str = "0", custom_cost: int = None):
        """링크 추가"""
        cost = custom_cost if custom_cost else max(1, self.ref_bw // (bandwidth_mbps * 1_000_000))

        link = Link(
            local_router=r1,
            remote_router=r2,
            local_interface=f"Gi0/{len([l for l in self.links if l.local_router == r1])}",
            remote_interface=f"Gi0/{len([l for l in self.links if l.local_router == r2])}",
            bandwidth_mbps=bandwidth_mbps,
            cost=cost,
            area=area
        )

        self.links.append(link)

        # 양방향 토폴로지 구성
        self.topology[r1][r2] = cost
        self.topology[r2][r1] = cost

    def calculate_cost(self, bandwidth_mbps: int) -> int:
        """OSPF Cost 계산"""
        return max(1, self.ref_bw // (bandwidth_mbps * 1_000_000))

    def run_spf(self, source_router: str) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
        """
        Dijkstra SPF 알고리즘 실행

        Args:
            source_router: 시작 라우터 ID

        Returns:
            distances: 각 라우터까지의 최단 거리
            paths: 각 라우터까지의 최단 경로
        """
        # 초기화
        distances = {router: float('infinity') for router in self.routers}
        distances[source_router] = 0
        previous = {router: None for router in self.routers}
        visited = set()

        # 우선순위 큐: (거리, 라우터ID)
        pq = [(0, source_router)]

        while pq:
            current_dist, current_router = heapq.heappop(pq)

            if current_router in visited:
                continue

            visited.add(current_router)

            # 인접 라우터 탐색
            for neighbor, cost in self.topology[current_router].items():
                if neighbor in visited:
                    continue

                new_dist = current_dist + cost

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current_router
                    heapq.heappush(pq, (new_dist, neighbor))

        # 경로 재구성
        paths = {}
        for router in self.routers:
            if distances[router] == float('infinity'):
                paths[router] = []
                continue

            path = []
            current = router
            while current is not None:
                path.append(current)
                current = previous[current]
            paths[router] = list(reversed(path))

        return distances, paths

    def find_ecmp_paths(self, source: str, destination: str,
                        max_paths: int = 4) -> List[Tuple[int, List[str]]]:
        """
        ECMP(Equal-Cost Multi-Path) 경로 찾기
        동일 비용의 여러 경로 탐색
        """
        distances, _ = self.run_spf(source)
        target_cost = distances.get(destination, float('infinity'))

        if target_cost == float('infinity'):
            return []

        # DFS로 동일 비용 경로 탐색
        ecmp_paths = []

        def dfs(current: str, path: List[str], cost_so_far: int):
            if len(ecmp_paths) >= max_paths:
                return

            if current == destination:
                if cost_so_far == target_cost:
                    ecmp_paths.append((cost_so_far, path.copy()))
                return

            for neighbor, link_cost in self.topology[current].items():
                if neighbor in path:
                    continue

                new_cost = cost_so_far + link_cost
                if new_cost > target_cost:
                    continue

                path.append(neighbor)
                dfs(neighbor, path, new_cost)
                path.pop()

        dfs(source, [source], 0)
        return ecmp_paths

    def generate_routing_table(self, source_router: str) -> Dict[str, dict]:
        """
        라우팅 테이블 생성
        """
        distances, paths = self.run_spf(source_router)
        routing_table = {}

        for dest_router in self.routers:
            if dest_router == source_router:
                continue

            if distances[dest_router] == float('infinity'):
                continue

            path = paths[dest_router]
            if len(path) >= 2:
                next_hop = path[1]
                routing_table[dest_router] = {
                    'destination': dest_router,
                    'next_hop': next_hop,
                    'cost': distances[dest_router],
                    'path': ' -> '.join(path),
                    'outgoing_interface': self._get_interface(source_router, next_hop)
                }

        return routing_table

    def _get_interface(self, router1: str, router2: str) -> str:
        """두 라우터 간 인터페이스 이름 찾기"""
        for link in self.links:
            if link.local_router == router1 and link.remote_router == router2:
                return link.local_interface
        return "Unknown"

    def print_topology(self):
        """토폴로지 출력"""
        print("\n[ OSPF Network Topology ]")
        print("=" * 60)
        for link in self.links:
            print(f"  {link.local_router} [{link.local_interface}] <--> "
                  f"[{link.remote_interface}] {link.remote_router}")
            print(f"    Bandwidth: {link.bandwidth_mbps} Mbps, Cost: {link.cost}, "
                  f"Area: {link.area}")
        print("=" * 60)


# 사용 예시
if __name__ == "__main__":
    # OSPF 네트워크 생성
    ospf = OSPFNetworkSimulator(reference_bandwidth=100_000_000)  # 100 Mbps 기준

    # 라우터 추가
    routers = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"]
    for r in routers:
        router_type = "ABR" if r in ["R1", "R3"] else "Internal"
        ospf.add_router(r, router_type)

    # 링크 추가 (R1-R8 토폴로지)
    ospf.add_link("R1", "R2", 1000)   # Cost: 1
    ospf.add_link("R2", "R3", 100)    # Cost: 10
    ospf.add_link("R3", "R4", 1000)   # Cost: 1
    ospf.add_link("R4", "R8", 100)    # Cost: 10
    ospf.add_link("R1", "R5", 100)    # Cost: 10
    ospf.add_link("R2", "R6", 1000)   # Cost: 1
    ospf.add_link("R5", "R6", 10)     # Cost: 100
    ospf.add_link("R6", "R7", 2000)   # Cost: 1
    ospf.add_link("R7", "R8", 100)    # Cost: 10
    ospf.add_link("R3", "R7", 1000)   # Cost: 1

    # 토폴로지 출력
    ospf.print_topology()

    # R1에서 SPF 실행
    print("\n[ SPF Algorithm Results from R1 ]")
    print("=" * 60)
    distances, paths = ospf.run_spf("R1")

    for router in sorted(distances.keys()):
        if distances[router] != float('infinity'):
            print(f"  {router}: Cost={distances[router]}, Path={' -> '.join(paths[router])}")

    # 라우팅 테이블 생성
    print("\n[ R1 Routing Table ]")
    print("=" * 60)
    routing_table = ospf.generate_routing_table("R1")

    print(f"{'Destination':<12} {'Next Hop':<10} {'Cost':<8} {'Interface':<12}")
    print("-" * 50)
    for dest, entry in sorted(routing_table.items()):
        print(f"{entry['destination']:<12} {entry['next_hop']:<10} "
              f"{entry['cost']:<8} {entry['outgoing_interface']:<12}")

    # ECMP 경로 찾기
    print("\n[ ECMP Paths from R1 to R8 ]")
    print("=" * 60)
    ecmp_paths = ospf.find_ecmp_paths("R1", "R8")

    for cost, path in ecmp_paths:
        print(f"  Cost {cost}: {' -> '.join(path)}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### OSPF vs 다른 라우팅 프로토콜 비교

| 특성 | OSPF | EIGRP | IS-IS | BGP |
|------|------|-------|-------|-----|
| **프로토콜 타입** | 링크 상태 | 고급 거리 벡터 | 링크 상태 | 경로 벡터 |
| **알고리즘** | Dijkstra SPF | DUAL | SPF | 경로 선택 |
| **메트릭** | Cost (대역폭) | 복합 (대역폭+지연) | Cost | AS-PATH 길이 등 |
| **계층 구조** | Area | Autonomous System | Level 1/2 | AS |
| **컨버전스** | 빠름 (~1초) | 매우 빠름 | 빠름 | 느림 (분 단위) |
| **표준** | IETF 표준 | Cisco 전용 (현재 개방) | ISO 표준 | IETF 표준 |
| **주요 용도** | 엔터프라이즈 | Cisco 네트워크 | ISP 백본 | 인터넷 |

### Area 설계 Best Practice

| 네트워크 규모 | Area 개수 | Area 당 라우터 수 | LSA 개수 (권장) |
|--------------|----------|------------------|----------------|
| **소규모** | 1 (Area 0만) | < 50 | < 1,000 |
| **중규모** | 3~5 | 50~100 | 1,000~5,000 |
| **대규모** | 10+ | < 100 | < 10,000 |
| **초대규모** | 50+ | < 50/Area | 분산 관리 |

### 과목 융합 관점 분석

1. **데이터베이스와의 융합**:
   - **LSDB 관리**: OSPF의 LSDB는 분산 데이터베이스 개념입니다. 각 라우터가 동일한 데이터 사본을 유지하며, 변경사항을 플러딩으로 동기화합니다.
   - **트랜잭션**: LSA 교환은 원자적(Atomic)으로 수행되며, 시퀀스 번호로 순서를 보장합니다.

2. **보안과의 융합**:
   - **OSPF 인증**: 평문, MD5, HMAC-SHA 인증으로 라우팅 정보 위변조 방지
   - **Graceful Restart**: 라우터 재시작 시 인접성 유지로 컨버전스 최소화

3. **클라우드/SDN과의 융합**:
   - **Segment Routing**: MPLS 레이블 대신 OSPF로 SR 정보 배포
   - **SDN 컨트롤러**: 컨트롤러가 OSPF 경로를 프로그래밍하여 트래픽 엔지니어링 수행

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 대형 캠퍼스 네트워크 OSPF 설계

**문제 상황**: 5개 캠퍼스, 총 500대 라우터, 2,000개 서브넷을 가진 대학교 네트워크를 설계합니다.

**기술사의 전략적 의사결정**:

1. **Area 설계**:
   - **Area 0**: 메인 데이터센터 (DC) 간 백본
   - **Area 1~5**: 각 캠퍼스별 Area 할당
   - **Area 100~110**: 원격 분교 (Stub Area)

2. **참조 대역폭 설정**:
   ```
   auto-cost reference-bandwidth 10000  (10 Gbps 기준)
   ```
   - 10G 링크: Cost 1
   - 1G 링크: Cost 10
   - 100M 링크: Cost 100

3. **DR/BDR 최적화**:
   - Point-to-Point 링크 사용 (DR 선출 불필요)
   - Broadcast 네트워크에서는 priority 조정으로 DR 제어

4. **LSA 최적화**:
   - Area 간 경로 요약 (Summary LSA)
   - External 경로 필터링

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - Area 0 미경유**:
  모든 Area 간 트래픽은 반드시 Area 0를 거쳐야 합니다. Virtual Link는 임시 해결책이며, 정규 설계에서는 피해야 합니다.

- **안티패턴 2 - 과도한 LSA 플러딩**:
  불안정한 링크가 있으면 LSA가频繁히 발생하여 CPU 부하를 유발합니다. SPF 스로틀링과 LSA throttle을 설정해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | OSPF 도입 전 (RIP) | OSPF 도입 후 | 개선율 |
|----------|------------------|-------------|--------|
| **컨버전스 시간** | 30~180초 | 1~5초 | 90%+ 단축 |
| **홉 제한** | 15홉 | 무제한 | 확장성 확보 |
| **부하 분산** | 미지원 | ECMP 지원 | 대역폭 활용 100% |
| **VLSM 지원** | 미지원 (RIPv1) | 지원 | IP 주소 효율 30% 향상 |

### 미래 전망 및 진화 방향

- **Segment Routing over OSPF**: MPLS 없이 소스 라우팅 구현
- **BIER (Bit Index Explicit Replication)**: 멀티캐스트 효율화
- **OSPFv3 확장**: SRv6, Traffic Engineering 지원 강화

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **RFC 2328** | IETF | OSPF Version 2 |
| **RFC 5340** | IETF | OSPF Version 3 (IPv6) |
| **RFC 5838** | IETF | OSPF Multi-Instance |
| **RFC 6860** | IETF | OSPFv3 GR (Graceful Restart) |

---

## 관련 개념 맵 (Knowledge Graph)
- [라우팅 알고리즘](./routing_algorithms.md) - 거리 벡터 vs 링크 상태
- [BGP](./routing_protocols_ospf_bgp.md) - AS 간 라우팅
- [MPLS](./routing_algorithms.md) - 레이블 스위칭
- [VLAN 간 라우팅](../4_switching/) - L3 스위칭
- [IS-IS](./routing_algorithms.md) - OSI 링크 상태 프로토콜

---

## 어린이를 위한 3줄 비유 설명
1. **OSPF**는 모든 라우터가 **완전한 지도**를 가지고 있어요. 각 도로(링크)가 얼마나 넓은지(대역폭) 알고 최적 경로를 찾습니다.
2. **Area**는 **지역 단위**로 지도를 나누는 거예요. 서울 지도, 부산 지도로 나누면 전체 지도를 매번 볼 필요 없죠.
3. **SPF 알고리즘**은 **네비게이션의 최단 경로 찾기**와 같아요. 여러 갈래 길 중 가장 빠른 길을 계산해 줍니다!
