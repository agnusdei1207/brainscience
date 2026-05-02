+++
weight = 117
title = "쿠버네티스 네트워크 폴리시 (마이크로 세그멘테이션)"
date = "2026-03-04"
[extra]
categories = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)
1. **네트워크 폴리시(Network Policy)**는 쿠버네티스 내부 파드(Pod) 간의 통신 트래픽(Inbound/Outbound)을 L3/L4 계층에서 IP와 Port 기반으로 통제하는 소프트웨어 정의 방화벽(SDN 방화벽)입니다.
2. 해커가 웹 서버 파드를 탈취하더라도, 내부 DB 파드로 횡적 이동(Lateral Movement)을 하지 못하게 차단하는 **마이크로 세그멘테이션(Micro-segmentation)**을 실현합니다.
3. 이를 구동하려면 Calico나 Cilium과 같은 네트워크 정책 기능을 지원하는 전용 CNI(Container Network Interface) 플러그인이 클러스터에 설치되어 있어야 합니다.

### Ⅰ. 개요 (Context & Background)
기본적으로 쿠버네티스 클러스터 내부의 모든 파드는 아무런 제한 없이 서로 자유롭게 통신(Default Allow All)할 수 있습니다. 이는 클라우드 네이티브 환경에서 심각한 보안 홀(Hole)을 의미합니다. 침해 사고 확산을 막고 제로 트러스트(Zero Trust) 철학을 구현하기 위해 파드 단위의 정밀한 망분리 규정이 필수적으로 요구되며, 이를 명세형(YAML) 코드로 제어하는 기술이 바로 Network Policy입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
네트워크 폴리시는 라벨 셀렉터(Label Selector)를 사용하여 타겟 파드를 식별하고, Ingress(수신)와 Egress(발신) 트래픽 규칙을 화이트리스트(Default Deny, Allow Specific) 방식으로 적용합니다.

```text
+-------------------------------------------------------------+
|               Network Policy Micro-segmentation             |
|                                                             |
|   [Attacker] -> compromises -> [Frontend Pod]               |
|                                   |  (Lateral Move Blocked) |
|                                   X                         |
|   Network Policy:                 |                         |
|   Only [Backend Pod] can access [Database Pod] on port 3306 |
|                                                             |
|  [Frontend Pod] --(Allowed)--> [Backend Pod]                |
|                                      |                      |
|                                  (Allowed)                  |
|                                      v                      |
|                                 [Database Pod]              |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 접근 통제 방식 | 인프라 방화벽 (AWS Security Group) | K8s Network Policy | 서비스 메시 (Istio Authorization) |
|---|---|---|---|
| **통제 수준** | L3/L4 (Node, VM 단위) | L3/L4 (Pod, IP/Port 단위) | L7 (HTTP Header, URL Path 단위) |
| **식별자** | IP 주소, CIDR | **K8s 라벨(Label), Namespace** | 서비스 어카운트(mTLS 인증서) |
| **동적 확장성** | Pod 재생성 시 IP 변경 대응 어려움 | 라벨 기반이므로 자동 적용 매핑 | 인증서 기반이므로 가장 강력함 |
| **운영 주체** | 클라우드 인프라 팀 | K8s/플랫폼 보안 팀 | 서비스 개발/데브옵스 팀 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **Default Deny All 정책 적용**: 네임스페이스를 생성할 때 가장 먼저 '모든 트래픽을 차단(Default Deny Ingress/Egress)'하는 정책을 깐 뒤, 통신이 필요한 서비스(예: Frontend -> API)만 명시적으로 허용(Whitelist)하는 방식으로 설계해야 강력한 보안이 유지됩니다.
* **CNI 선택**: Flannel 같은 기본 CNI는 통신망만 뚫어줄 뿐 Network Policy를 적용하지 못합니다. 상용 엔터프라이즈 환경에서는 정책 집행 성능이 우수한 Calico 기반 iptables나, 최근 eBPF 기술을 통해 커널 단에서 초고속 통제를 수행하는 Cilium을 채택하는 것이 기술사적 권장 아키텍처입니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
네트워크 폴리시를 통한 마이크로 세그멘테이션은 ISMS-P 및 클라우드 보안 인증(CSAP) 심사 시 내부망 격리 요건을 충족하는 핵심 기술입니다. 향후 L7 영역의 애플리케이션 보안까지 커버하기 위해 Istio와 같은 서비스 메시와 결합한 다층적(Defense-in-Depth) 보안 구조로 진화하고 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: 클라우드 네이티브 보안, 쿠버네티스
* **하위 개념**: Ingress/Egress, 라벨 셀렉터, CNI
* **연관 개념**: 제로 트러스트, 횡적 이동(Lateral Movement), Calico, Cilium, eBPF

### 👶 어린이를 위한 3줄 비유 설명
1. 학교에 수백 개의 교실(파드)이 있는데, 처음에는 모든 교실 문이 열려 있어서 아무나 마음대로 뛰어다닐 수 있었어요.
2. 하지만 네트워크 폴리시라는 '스마트 교문 지킴이'가 생기면, "1반 학생은 화장실만 갈 수 있고 2반에는 절대 못 들어가!"라고 규칙을 정할 수 있어요.
3. 만약 한 교실에 무서운 악당(해커)이 몰래 들어와도 다른 교실로는 넘어갈 수 없게 꽁꽁 가둬버리는 멋진 방패랍니다!
