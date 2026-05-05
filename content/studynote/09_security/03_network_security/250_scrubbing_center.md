+++
title = "스크러빙 센터 (Scrubbing Center)"
weight = 250
date = "2024-03-21"
[extra]
categories = ["Security", "Network"]
+++
## 0. 핵심 인사이트

>

> 📝 모범 답안

- **DDoS 전문 정화 시설**: 대규모 DDoS 공격 트래픽을 스크러빙 센터로 우회(Redirect)시켜 악성 패킷만 필터링하고 정상 트래픽만 본래 서버로 전달하는 보안 서비스임.
- **대역폭 확장성 제공**: 개별 기업이 감당하기 어려운 수백 Gbps~Tbps급의 볼류메트릭 공격을 클라우드 급 대역폭을 통해 수용하고 처리함.
- **BGP 및 DNS 기반 우회**: 공격 발생 시 BGP 라우팅 변경이나 DNS CNAME 전환을 통해 즉각적인 트래픽 제어가 가능한 유연한 아키텍처를 가짐.

### 1. 개요 및 필요성
- **등장 배경**: 좀비 PC와 IoT 봇넷을 이용한 DDoS 공격 규모가 기하급수적으로 커지면서, 기업 내부의 온프레미스 보안 장비만으로는 회선 대역폭 자체가 포화되는 한계가 발생함.
- **정의**: 인터넷 구간과 내부 네트워크 사이에 위치하여 유입되는 모든 트래픽 중 오염된(Dirty) 트래픽을 씻어내고 깨끗한(Clean) 트래픽만 통과시키는 특수 목적 보안 인프라임.
- **핵심 가치**: 서비스 가용성(Availability) 보장 및 공격 대응을 위한 인프라 투자 비용 절감.

### 2. 구성요소
```text
[ Scrubbing Center Operation Flow ]

 (Internet) ----[ Mixed Traffic (Normal + DDoS) ]----                           |
            [ Bipartite Routing Update (BGP) ]
                           |
                           v
              +----------------------------+
              |    SCRUBBING CENTER        |
              |----------------------------|
              | 1. Traffic Analysis        |
              | 2. Filtering (L3/L4/L7)    |
              | 3. Clean Pipe Extraction   |
              +----------------------------+
                           |
            [ Clean Traffic via GRE/VPN/Direct ]
                           |
                           v
                    (Target Server)

[ Key Technologies ]
1. BGP Hijacking (Safe): Traffic redirection using AS-Path or Communities.
2. GRE Tunneling: Returning clean traffic to original data center.
3. Behavioral Analysis: Differentiating bots from human users.
```
- **트래픽 유입(Redirection)**: 공격 감지 시 타겟 네트워크의 대역을 스크러빙 센터로 알림으로써 전 세계 트래픽을 센터로 집중시킴.
- **정밀 분석 및 차단(Mitigation)**: 시그니처, 행위 분석, 챌린지 응답(JS Challenge 등)을 통해 정교한 L7 공격까지 필터링함.
- **회귀(Return Traffic)**: 필터링된 깨끗한 트래픽만 GRE 터널링이나 전용선을 통해 실제 서버로 안전하게 전달함.

### 3. 구조 및 동작 원리

| 항목 | 온프레미스 방어 | 스크러빙 센터 (클라우드) | CDN 기반 방어 (Edge) |
| :--- | :--- | :--- | :--- |
| **대역폭 수용량** | 자사 회선 용량에 제한됨 | 수 Tbps급 대구경 회선 | 전 세계 에지 노드 분산 수용 |
| **방어 시점** | 내부 유입 시점 | 외부 정화 센터 거침 | 인터넷 에지 구간 (가장 빠름) |
| **구축 비용** | 하드웨어 도입 비용 높음 | 사용량 기반 과금 (OPEX) | 통합 플랫폼 이용료 |
| **특징** | 보안 정책 직접 통제 가능 | 대규모 공격 방어 최적화 | 웹 가속과 보안 동시 제공 |

### 4. 비교 및 트레이드오프
- **하이브리드 전략**: 평상시에는 온프레미스 장비로 대응하고, 임계치를 넘는 대규모 공격 시에만 스크러빙 센터로 전환하는 'Cloud Signalling' 체계 구축이 효율적임.
- **도입 고려 사항**: 트래픽 우회 시 발생하는 레이턴시(Latency)와 GRE 터널링에 따른 MTU(Maximum Transmission Unit) 파편화 문제를 사전 검토해야 함.
- **기술사적 판단**: 금융, 게임 등 가용성이 생명인 비즈니스에서는 가입형 스크러빙 서비스를 상시 대기(Always-on) 상태로 두어 0-sec 대응 체계를 마련해야 함.

### 5. 실무 적용 및 최적화 기법
- **글로벌 위협 헌팅**: 전 세계 각지의 스크러빙 센터에서 수집된 위협 데이터를 AI로 분석하여 제로데이 공격에 대한 선제적 방어가 가능해짐.
- **표준화 동향**: SECaaS(Security as a Service)의 일환으로 클라우드 보안 아키텍처의 필수 요소로 자리 잡고 있음.
- **결론**: 스크러빙 센터는 현대의 '디지털 소방서'와 같으며, 대규모 사이버 재난 상황에서 비즈니스를 보호하기 위한 최후의 방어선임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **BGP (Border Gateway Protocol)**: 우회 기술의 핵심
- **GRE (Generic Routing Encapsulation)**: 트래픽 회귀 터널
- **DDoS Mitigation**: 상위 보안 전략
- **Anycast**: 분산 수용 기술

### 👶 어린이를 위한 3줄 비유 설명
1. 우리 집으로 들어오는 수돗물에 흙탕물이 섞여 들어오고 있어요.
2. 집 입구에서 막으면 물이 넘치니까, 마을 정수장(스크러빙 센터)으로 물을 먼저 보내서 깨끗하게 씻어내요.
3. 정수장에서 깨끗해진 맑은 물만 다시 우리 집 수도꼭지로 보내주는 거예요!
