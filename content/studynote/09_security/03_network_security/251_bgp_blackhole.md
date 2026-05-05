+++
weight = 251
title = "BGP Blackhole (BGP 블랙홀)"
date = "2026-03-25"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> [ISP Edge] --X--> [Target Server]

> 📝 모범 답안

- 대규모 DDoS 공격 트래픽이 타겟 네트워크로 유입되기 전, ISP 레벨에서 해당 IP로의 트래픽을 무효화(Discard) 처리하는 기법임
- 특정 IP를 희생시킴으로써 전체 네트워크 인프라의 마비(Collateral Damage)를 방지하는 방어 수단임
- RTBH(Remote Triggered Black Hole) 메커니즘을 통해 공격 발생 시 신속하게 전파 및 대응함

### 1. 개요 및 필요성
볼류메트릭(Volumetric) DDoS 공격이 네트워크 대역폭을 초과할 때, 타겟 서버뿐만 아니라 동일 회선을 공유하는 다른 서비스들까지 마비될 수 있다. BGP Blackhole은 공격 대상이 되는 IP로 향하는 모든 트래픽을 네트워크 입구에서 차단하여 인프라 전체를 보호하는 "살을 주고 뼈를 취하는" 전략이다.

### 2. 구성요소
```text
[BGP Blackhole / RTBH Mechanism]

1. Attack Detection (DDoS Monitor)
2. Trigger Router sends BGP Update to ISP
   - Target IP Route with "Next-Hop = Null0"
   - Specific Community Tag (e.g., 65535:666)
3. ISP Edge Routers receive Update
4. Traffic to Target IP is Dropped at the edge!

   [Attacker] ----                       |
                  (Dropped here)
```
- **Null0 Routing:** 패킷을 실제로 전송하지 않고 휴지통(Null 인터페이스)으로 보내버리는 논리적 처리 방식임
- **RTBH:** 원격에서 트리거 라우터가 BGP 광고를 통해 ISP 전체 에지 라우터에 블랙홀 정책을 즉시 적용하는 방식임

### 3. 구조 및 동작 원리
| 구분 | BGP Blackhole | DDoS Scrubbing (세척) |
| :--- | :--- | :--- |
| 대응 방식 | 해당 IP 트래픽 전량 차단 (Drop) | 공격 트래픽만 필터링 (Clean) |
| 비용 | 저렴 (ISP 기본 제공 가능) | 비쌈 (전문 장비/서비스 필요) |
| 서비스 가용성 | 해당 IP 서비스 불능 (Self-DoS) | 정상 트래픽 유지 가능 |
| 목적 | 인프라 보호 및 생존 | 비즈니스 연속성 유지 |

### 4. 비교 및 트레이드오프
- **실무 적용:** ISP와의 사전 협의(BGP Community 값 정의)가 필수적이며, 공격 규모가 감당 가능한 범위를 넘었을 때 최후의 수단으로 발동함
- **기술사적 판단:** 공격자가 타겟 IP를 지속적으로 변경하며 공격할 경우 블랙홀 대상이 늘어나 서비스 전체가 마비될 위험이 있으므로, Anycast 기반 분산 대응이나 Scrubbing 센터와 병행 운용해야 함

### 5. 실무 적용 및 최적화 기법
- **기대효과:** 상위 ISP 네트워크단에서 트래픽을 차단함으로써 내부망 대역폭 고갈을 완벽히 방어하고, 2차 피해를 방지함
- **결론:** BGP Blackhole은 강력하지만 파괴적인 방어 기법으로, 정교한 탐지 시스템과 결합하여 오탐으로 인한 서비스 차단을 최소화하는 거버넌스 수립이 중요함

### 📌 관련 개념 맵 (Knowledge Graph)
- DDoS 방어 → BGP Blackhole → RTBH (Remote Triggered Black Hole)
- BGP → Community Attribute → Null0 Interface
- DDoS 유형 → Volumetric Attack → Bandwidth Exhaustion

### 👶 어린이를 위한 3줄 비유 설명
- 고속도로에 엄청나게 많은 가짜 트럭(공격 트래픽)이 몰려와서 모든 차가 꼼짝달싹 못 하게 됐어요.
- 고속도로 입구에서 "이 주소로 가는 트럭은 무조건 낭떠러지로 보내라"고 명령을 내리는 거예요.
- 비록 그 주소로 가는 진짜 편지는 못 받게 되지만, 다른 사람들이 다니는 길은 시원하게 뚫리게 된답니다!
