+++
title = "라우팅 알고리즘 (OSPF, BGP) 및 네트워크 경로 최적화"
date = 2024-05-19
description = "AS 내부 라우팅(IGP: OSPF)과 AS 간 라우팅(EGP: BGP)의 동작 원리, 최단 경로 알고리즘(Dijkstra) 및 정책 기반 라우팅에 대한 심층 분석"
weight = 40
[taxonomies]
categories = ["studynotes-network"]
tags = ["Routing", "OSPF", "BGP", "Algorithm", "Dijkstra", "Network"]
+++

# 라우팅 알고리즘 (Routing Algorithms: OSPF & BGP) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 네트워크 토폴로지 정보를 수집하여 데이터 패킷이 목적지까지 도달할 수 있는 최적의 경로를 결정하고 라우팅 테이블(Routing Table)을 동적으로 갱신하는 지능형 알고리즘입니다.
> 2. **가치**: OSPF는 대규모 기업 망 내에서 고속 수렴(Convergence)과 대역폭 기반의 최적 경로를 제공하며, BGP는 전 세계 인터넷의 자치 시스템(AS)을 연결하는 사실상의 표준(De facto standard) 프로토콜로 작동합니다.
> 3. **융합**: 현대의 클라우드 환경에서는 소프트웨어 정의 네트워크(SDN)와 결합하여, 물리적 거리뿐만 아니라 지연 시간(Latency) 및 비용까지 고려한 멀티 클라우드 라우팅 최적화를 실현하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

라우팅(Routing)은 네트워크 계층(L3)의 핵심 기능으로, 거대한 인터넷 망에서 패킷이 갈 길을 찾아주는 내비게이션 시스템과 같습니다. 단순히 연결된 선을 따라가는 것이 아니라, 네트워크의 혼잡도, 링크의 속도, 보안 정책 등을 종합적으로 고려하여 매 순간 최선의 선택을 내리는 복잡한 의사결정 과정입니다.

**💡 비유**: 라우팅은 **'전 세계 배달 시스템'**과 같습니다. **OSPF**는 한 도시(기업 망) 안에서 가장 빠른 길을 잘 아는 지역 퀵서비스 기사이고, **BGP**는 국가(AS) 간에 물건을 보낼 때 어떤 무역 항로나 철도를 이용할지 결정하는 국제 물류 계획가입니다.

**등장 배경 및 발전 과정**:
1. **정적 라우팅의 한계**: 초기 네트워크는 관리자가 경로를 직접 입력했으나, 망이 복잡해지고 장비 장애가 빈번해지면서 스스로 경로를 우회하는 동적 라우팅(Dynamic Routing)이 필수적으로 요구되었습니다.
2. **계층적 라우팅의 도입**: 인터넷이 거대해지자 전 세계의 모든 라우팅 정보를 한 대의 장비에 담는 것이 불가능해졌습니다. 이에 따라 관리 영역을 자치 시스템(AS: Autonomous System) 단위로 나누고, 내부용(IGP)과 외부용(EGP) 프로토콜을 분리하는 계층적 아키텍처가 정립되었습니다.
3. **지능형 경로 최적화**: 단순 홉(Hop) 수 기반인 RIP를 넘어, 링크 상태를 고려하는 OSPF와 복잡한 비즈니스 정책을 반영할 수 있는 BGP가 현대 네트워크의 중추를 형성하게 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 라우팅 프로토콜의 분류 및 특징

| 분류 | 프로토콜 | 주요 알고리즘 | 최적 경로 결정 기준 (Metric) | 특징 및 적용 범위 |
|---|---|---|---|---|
| **IGP (Link State)** | **OSPF** | Dijkstra (Shortest Path First) | Cost (대역폭에 반비례) | AS 내부, 빠른 수렴, 계층적 Area 구조 |
| **IGP (Distance Vector)** | **RIP** | Bellman-Ford | Hop Count (최대 15개) | 소규모 망, 단순함, 느린 수렴 |
| **EGP (Path Vector)** | **BGP** | Path Vector (Policy-based) | AS-Path 및 다양한 속성(Attributes) | AS 간 통신, 인터넷 백본, 정책 제어 중점 |

### 정교한 구조 다이어그램: OSPF의 Area 구조와 BGP의 AS 간 통신

```ascii
[ Global Internet (BGP Context) ]
      +--------------+      (BGP)      +--------------+
      |    AS 100    | <-------------> |    AS 200    |
      |  (ISP 'A')   |                 |  (ISP 'B')   |
      +------+-------+                 +-------+------+
             |                                 |
             | (Internal OSPF Context)         |
             v                                 v
    +-------------------+             +-------------------+
    |  OSPF Area 0      |             |  OSPF Area 0      |
    |  (Backbone)       |             |  (Backbone)       |
    +---+-----------+---+             +---+-----------+---+
        |           |                     |           |
    +---v---+   +---v---+             +---v---+   +---v---+
    | Area 1|   | Area 2|             | Area 3|   | Area 4|
    +-------+   +-------+             +-------+-------+
```

### 심층 동작 원리 (Algorithm Deep Dive)

1. **OSPF (Open Shortest Path First)**:
   - **Hello 단계**: 인접 라우터와 Hello 패킷을 교환하여 이웃 관계(Adjacency)를 맺습니다.
   - **LSA 전파**: 자신의 링크 상태 정보(LSA)를 Area 내의 모든 라우터에 플러딩(Flooding)합니다.
   - **LSDB 동기화**: 모든 라우터가 동일한 지도(Link State Database)를 가집니다.
   - **Dijkstra 계산**: 각 라우터는 자신을 루트로 하여 목적지까지의 최단 경로 나무(Shortest Path Tree)를 계산하고 라우팅 테이블에 올립니다.
2. **BGP (Border Gateway Protocol)**:
   - **Peering**: TCP 포트 179를 통해 신뢰성 있는 연결을 맺습니다.
   - **Attribute 교환**: 단순 거리가 아닌 AS-Path, Next Hop, Local Preference 등 다양한 속성을 주고받습니다.
   - **Best Path Selection**: 루프 방지를 위해 자신의 AS 번호가 포함된 경로는 폐기하며, 정의된 우선순위 규칙(13단계 이상)에 따라 최적 경로를 선정합니다.
   - **Policy Enforcement**: 국가 간 계약이나 비용에 따라 특정 AS를 경유하지 않도록 강제하는 정책 기반 라우팅을 수행합니다.

### 핵심 코드: OSPF 최적 경로 계산의 핵심, Dijkstra 알고리즘 (Python)
네트워크 비용(Metric)을 기반으로 최단 경로를 찾는 로직의 골격입니다.

```python
import heapq

def dijkstra(graph, start):
    # 각 노드까지의 최소 비용을 무한대로 초기화
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    # 우선순위 큐 (비용, 노드)
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # 이미 더 짧은 경로를 찾았다면 무시
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # 더 짧은 경로 발견 시 업데이트
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# 네트워크 토폴로지 예시 (라우터 간 Cost)
router_map = {
    'R1': {'R2': 10, 'R3': 5},
    'R2': {'R1': 10, 'R3': 2, 'R4': 1},
    'R3': {'R1': 5, 'R2': 2, 'R4': 9},
    'R4': {'R2': 1, 'R3': 9}
}

print(f"R1에서 각 라우터까지의 최단 경로 비용: {dijkstra(router_map, 'R1')}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Distance Vector vs Link State
라우팅 정보가 어떻게 전파되고 처리되는지에 대한 근본적인 차이입니다.

| 비교 관점 | Distance Vector (RIP) | Link State (OSPF) | 상세 분석 |
|---|---|---|---|
| **정보의 형태** | 이웃으로부터 듣는 "거리와 방향" (카더라 통신) | 모든 라우터가 공유하는 "전체 지도" (LSA) | Link State는 전체 구조를 알기에 루프 발생 가능성이 현저히 낮음. |
| **수렴 속도 (Convergence)** | 느림 (변화 발생 시 순차적으로 전파) | 매우 빠름 (변화 즉시 플러딩 및 재계산) | OSPF는 대규모 망에서 장애 복구 시간이 짧아 비즈니스 연속성에 유리함. |
| **자원 소모 (CPU/Mem)** | 낮음 (단순 계산) | 높음 (전체 DB 유지 및 복잡한 알고리즘) | 장비 성능이 좋아진 현대에는 OSPF의 오버헤드가 큰 문제가 되지 않음. |
| **최적 경로 기준** | 단순 홉 수 (거리) | 링크 속도 (대역폭 기반 Cost) | OSPF는 1Gbps와 10Mbps 경로를 구분하여 훨씬 효율적인 경로 선택 가능. |

### 과목 융합 관점 분석 (운영체제 및 클라우드 연계)
- **운영체제(OS)와의 융합**: 라우팅 프로토콜은 OS의 **커널 라우팅 테이블**을 조작합니다. Linux의 `Quagga`나 `FRR` 같은 소프트웨어 스택은 유저 공간에서 OSPF/BGP 로직을 수행하고, 결과값(FIB)을 커널의 Forwarding 엔진에 주입합니다. 이때 패킷 처리 속도를 높이기 위해 커널은 `XDP`나 `DPDK` 기술을 사용하여 유저 공간과 커널 공간 사이의 오버헤드를 최소화합니다.
- **클라우드(Cloud)와의 융합**: 하이브리드 클라우드 환경에서 온프레미스와 AWS VPC를 연결할 때 **BGP**가 필수적으로 사용됩니다. AWS Direct Connect Gateway는 BGP를 통해 고객사의 네트워크 대역 정보를 동적으로 수신하며, 이를 통해 수천 개의 서브넷이 자동으로 인터넷에 연결되는 자동화된 네트워크 아키텍처를 완성합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 글로벌 엔터프라이즈 네트워크 구축
**문제 상황**: 한국, 미국, 유럽에 지사를 둔 글로벌 기업이 전 세계 오피스를 하나로 묶는 전용망을 구축하려 합니다. 각 지사는 전용 회선과 인터넷 VPN을 이중화하여 사용합니다.

**기술사의 전략적 의사결정**:
1. **내부 라우팅 (OSPF)**: 각 지사 오피스 내부와 데이터센터 내부는 OSPF를 적용합니다. Area 구조를 활용하여 라우팅 업데이트 범위를 제한함으로써, 한 지사의 장애가 전 세계 네트워크의 CPU 부하로 이어지는 것을 방지합니다.
2. **지사 간 연결 (BGP)**: 지사 간 통신에는 BGP를 사용합니다. BGP의 **Community 속성**을 활용하여 트래픽의 우선순위를 부여하고, 메인 회선 장애 시 VPN 회선으로 즉시(수초 내) 전환되도록 **BFD(Bidirectional Forwarding Detection)** 기술을 병행 도입합니다.
3. **경로 최적화**: BGP의 `AS-Path Prepend` 기술을 사용하여, 한국에서 미국으로 갈 때는 일본을 거치지 않고 직통 회선을 타도록 인위적으로 경로 비용을 조절하여 지연 시간(Latency)을 최소화합니다.

### 도입 시 고려사항 및 안티패턴 (Anti-patterns)
- **안티패턴 - OSPF 단일 Area 구성**: 수천 대의 라우터를 하나의 Area 0에 넣으면, 링크 하나만 흔들려도 모든 라우터가 동시에 Dijkstra 계산을 수행하여 네트워크 전체가 마비될 수 있습니다. 반드시 계층적 설계를 준수해야 합니다.
- **체크리스트**: 
  - 라우팅 프로토콜 보안 (Password Authentication) 적용 여부.
  - BGP Full-Route 수신 시 라우터 메모리 가용량 체크.
  - 비대칭 라우팅(Asymmetric Routing)으로 인한 방화벽 패킷 드랍 가능성 검토.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과
- **가용성 극대화**: 동적 라우팅을 통해 특정 링크 장애 시 수초 내에 우회 경로를 확보함으로써 서비스 중단 시간을 99% 이상 감소시킵니다.
- **운영 자동화**: 새로운 서브넷 추가 시 관리자가 모든 라우터를 설정할 필요 없이 프로토콜에 의해 자동으로 전파되어 운영 생산성이 향상됩니다.

### 미래 전망 및 진화 방향
- **Segment Routing (SR)**: 기존의 복잡한 라우팅 제어 평면을 단순화하고, 소스 기반 라우팅을 통해 트래픽 엔지니어링을 보다 세밀하게 제어하는 기술이 차세대 백본망의 대세가 되고 있습니다.
- **AI 기반 예측 라우팅**: 과거의 트래픽 패턴을 학습하여 혼잡이 예상되는 경로를 미리 피하거나, 실시간 지연 시간을 측정하여 최적의 경로를 실시간으로 변경하는 자율 네트워크(Self-driving Network)로 진화하고 있습니다.

### ※ 참고 표준/가이드
- **RFC 2328**: OSPF Version 2 Specification.
- **RFC 4271**: A Border Gateway Protocol 4 (BGP-4).

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [OSI 7계층](@/studynotes/03_network/01_fundamentals/osi_7_layer.md) : 라우팅이 일어나는 L3(Network Layer)의 위치와 역할 이해.
- [IP 주소 체계](@/studynotes/03_network/01_fundamentals/ip_addressing.md) : 라우팅의 목적지가 되는 논리적 주소의 할당 및 서브네팅 원리.
- [BGP 하이브리드 클라우드](@/studynotes/13_cloud_architecture/_index.md) : 실무에서 BGP가 클라우드 연결에 어떻게 쓰이는지에 대한 사례.
- [SDN (Software Defined Networking)](@/studynotes/03_network/_index.md) : 제어 평면을 분리하여 중앙 집중식으로 라우팅을 관리하는 차세대 기술.
- [네트워크 보안 (Firewall)](@/studynotes/09_security/01_policy/_index.md) : 라우팅 경로상에 배치되는 보안 장비와의 정합성 고려.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 라우팅 알고리즘은 복잡한 미로 같은 인터넷 세상에서 패킷이라는 보물을 실은 트럭이 길을 잃지 않게 도와주는 **'똑똑한 내비게이션'**이에요.
2. **OSPF**는 동네 골목길을 아주 잘 알아서 가장 빠른 지름길을 알려주는 동네 형이고, **BGP**는 국가 사이를 오가는 기차나 비행기 길을 알려주는 세계 지도 같아요.
3. 도로가 막히거나 사고가 나면 내비게이션이 자동으로 다른 길을 알려주는 것처럼, 라우팅 알고리즘 덕분에 우리는 언제나 끊김 없이 유튜브를 볼 수 있답니다.