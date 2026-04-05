+++
weight = 890
title = "90. 서비스 (Service)"
description = "Service: 오토스케일링과 파드 재생성 시 동적으로 변하는 파드IP를抽象화하여 고정된 진입점(ClusterIP)과 도메인 네임을 제공하는 쿠버네티스 네트워킹 리소스"
date = 2026-03-26

[taxonomies]
tags = ["kubernetes", "k8s", "service", "clusterip", "service-discovery", "load-balancing"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Service는 쿠버네티스에서"논리적 서비스 접근점"으로, 복수의 백엔드 파드를 grouping하고 고정된 ClusterIP(가상 IP)와 DNS 이름을 제공한다. 파드가 IP가 수시로 바뀌어도(재생성, 스케일링) Service의 IP는固定되어 있어 클라이언트는 이를 통해 백엔드에 접근한다.
> 2. **가치**: 마이크로서비스 아키텍처에서"서비스 디스커버리"를実現하고, 로드밸런싱을 통해 트래픽을 복수의 백엔드에分散하여 고가용성과 확장성을 제공한다.
> 3. **융합**: Kube-proxy가 Service의 ClusterIP로 들어오는 트래픽을 실제 백엔드 파드로 라우팅하며, Endpoint Controller가 Service와 백엔드 파드의 관계를 관리한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

쿠버네티스에서 Service는"일관된 진입점"을 제공하는 리소스이다. 예를 들어, "nginx" Deployment로 3개의 파드를 실행했다고 하자. 이 파드들의IP는 각각 10.244.1.10, 10.244.1.11, 10.244.2.15로 서로 다르다. 클라이언트가"파드 10.244.1.10에 요청을 보내야 한다"고 알고 있다면, 파드가 재생성될 때마다IP가 바뀌므로 클라이언트의 설정도 계속 변경해야 한다. Service는 이러한"동적 IP" 문제를 해결한다. Service의 IP(예: 10.100.0.100)는固定되고, 클라이언트는 이 IP만 알면 Service가 관리하는 모든 백엔드 파드에 접근할 수 있다.

### 왜 Service인가?

마이크로서비스 환경에서는 수많은 서비스가 서로를 호출한다. 만약 서비스A가 서비스B의IP를 하드코딩했다면, 서비스B가 스케일링되거나 재생성될 때마다 서비스A의 설정도 변경해야 한다. Service를 사용하면"호출したいサービス名"만 알면 되며, 해당 서비스의 백엔드IP 목록은 Kube-proxy가 자동으로管理한다. 이로 인해 서비스 간 결합도가 낮아지고, 독립적인 배포와 스케일링이 가능해진다.

### 비유

Service를"고급 호텔의 전화 예약 시스템"에 비유할 수 있다. 호텔에 객실(파드)이 100개 있고, 각 객실의 내선 번호는时常 바뀐다(파드 IP 변경). 고객(클라이언트)이 바로 객실에 전화하려면"현재 객실 번호"를 알아야 하므로 번거롭다. 그러나"레스토랑预约专柜(서비스)"에 전화하면, 예약 담당자가 현재 사용 가능한 객실 중 하나를 선택하여 연결해준다. 고객은"레스토랑预约专柜"의 번호만 알면 되고, 객실이 바뀌어도 예약 담당자가 이를 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Service 유형

 쿠버네티스의 Service에는 네 가지 유형이 있다. **ClusterIP**는 클러스터 내부에서만 접근 가능한固定 IP를 할당하며, 기본 유형이다. **NodePort**는 각 노드의特定 포트(30000~32767)를 열고, 해당 포트로 들어오는 트래픽을 Service로 전달한다. **LoadBalancer**는 클라우드 인프라와 연동하여 외부 로드밸런서를プロビジョ닝하고, 공인 IP를 할당받는다. **ExternalName**은 서비스명을 CNAME으로 매핑하여 외부 서비스에 접근할 수 있게 한다.

### Service 생성 과정

 Service가 생성되면 다음 과정이 자동으로 수행된다. (1) API Server가 Service를 저장한다. (2) Endpoint Controller가 해당 Service의 label selector와 매칭되는 파드 목록을監視한다. (3) 매칭되는 파드가 있으면 해당 파드IP를 Endpoints 리소스에 등록한다. (4) Kube-proxy가 이 Endpoints 변경을 감지하고, ClusterIP로 들어오는 트래픽을 백엔드 파드로 라우팅하는 iptables/IPVS 규칙을 설정한다.

```
[ Service와 Endpoints의 관계 ]

┌─────────────────────────────────────────────────────────────────────────┐
│                         Service 생성 과정                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Service 생성 (nginx-svc: ClusterIP 10.100.0.100)                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  apiVersion: v1                                                 │   │
│  │  kind: Service                                                  │   │
│  │  metadata:                                                       │   │
│  │    name: nginx-svc                                              │   │
│  │  spec:                                                          │   │
│  │    selector:                                                    │   │
│  │      app: nginx                                                 │   │
│  │    ports:                                                       │   │
│  │      - port: 80                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  2. Endpoints Controller가 파드 감시 (app=nginx 레이블)                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  파드 목록:                                                     │   │
│  │  • nginx-abc123 (10.244.1.10:80) - Running ✅                    │   │
│  │  • nginx-def456 (10.244.1.11:80) - Running ✅                    │   │
│  │  • nginx-ghi789 (10.244.2.15:80)  - Running ✅                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  3. Endpoints 리소스 자동 생성                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  apiVersion: v1                                                 │   │
│  │  kind: Endpoints                                                │   │
│  │  metadata:                                                       │   │
│  │    name: nginx-svc                                              │   │
│  │  subsets:                                                       │   │
│  │    - addresses:                                                 │   │
│  │        - ip: 10.244.1.10                                        │   │
│  │        - ip: 10.244.1.11                                        │   │
│  │        - ip: 10.244.2.15                                        │   │
│  │      ports:                                                     │   │
│  │        - port: 80                                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  4. Kube-proxy가 iptables 규칙 설정                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  ClusterIP 10.100.0.100:80 → 백엔드 파드 IPs:80 분산             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Service의 핵심은"라벨 셀렉터"와"Endpoints"의 조합이다. 셀렉터가"app=nginx"인 Service가 생성되면, Endpoints Controller가 이 셀렉터에 매칭되는 모든 파드를 찾아 그IP를 Endpoints에 등록한다. Kube-proxy는 이 Endpoints를Watch하여, ClusterIP로 들어오는 트래픽을 해당IP들(10.244.1.10, 10.244.1.11, 10.244.2.15)으로 분산한다. 만약 nginx-abc123 파드가 삭제되면, Endpoints Controller가 이를 감지하여 Endpoints에서 해당IP를 제거하고, Kube-proxy가 iptables 규칙을 갱신한다.

### DNS 등록

 Service가 생성되면 CoreDNS에 의해 DNS 레코드가自動登録된다. <service-name>.<namespace>.svc.cluster.local"라는FQDN으로 접근 가능하며, 같은 네임스페이스 내에서는 간단히 <service-name>만으로도 접근 가능하다. 파드 내부에서는 /etc/resolv.conf에 nameserver로CoreDNS의IP(기본 10.244.0.10)가 설정되어 있어, 서비스 이름解決하면対応する ClusterIP를 반환한다.

### Session Affinity

 spec.sessionAffinity: ClientIP로 설정하면,同一 클라이언트IPからの 요청을同一 백엔드 파드에固定할 수 있다. 이는 세션 상태가 특정 파드의 메모리에 저장된 경우 유용하다. 그러나 기본값은 None으로, 무작위 분산이다.

### 섹션 비유

 Service의 DNS 등록을"기업内线 전화번호부"에 비유할 수 있다. 신입 사원이 입사하면(파드 생성),、人事팀(Endpoints Controller)이 전화번호부에 이름과 내선 번호를 등록한다. 이제全社員은"철수 씨"가 싶다고"내선 204번으로 전화"하면(서비스 DNS로 접근), 인사팀이 현재 철수 씨의 자리(파드 IP)를 연결해준다. 철수 씨가 자리를 옮기면(파드 재생성),人事팀이 전화번호부를 업데이트한다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### Service vs Ingress

| 비교 항목 | Service | Ingress |
|:---|:---|:---|
| **작동 레이어** | L4 (TCP/UDP) | L7 (HTTP/HTTPS) |
| **접근 범위** | 클러스터 내부/외부 | 외부에서만 |
| **라우팅 기준** | IP/포트 | URL 경로, 호스트 이름 |
| **용도** | 내부 마이크로서비스 통신 | 외부 HTTP 접근 |

### Headless Service

 spec.clusterIP: None으로 설정하면 Headless Service가 생성된다. 이는"단일 ClusterIP를 할당하지 않고", DNS 查询時に直接 파드 IP들을 반환한다. StatefulSet과 함께 사용하여 각 파드에 직접 접근할 때 활용된다.

### Service와 파드数の動的変化

 Service의 가장 큰 가치는"파드数の動的変化への自動 대응"이다. HPA가 오토스케일링으로 파드를 늘리거나 줄이면, Endpoints Controller가 자동으로 Endpoints를 업데이트하고, Kube-proxy가 트래픽 라우팅을 조정한다. 이 과정이 자동화되어 있어, 클라이언트는 파드 수의 변화를意識할 필요가 없다.

### 섹션 비유

 Service와 HPA의 연계롤"호텔 예약 시스템의自動拡張"에 비유할 수 있다. 성수기에는 객실 담당자(파드)를 늘리고(Scale Out), 비수기에는 줄인다(Scale In). 예약 담당자(Endpoints Controller)가 실시간으로 사용 가능한 담당자 수를 전화번호부(DNS)에 반영하고, 안내 데스크(Kube-proxy)가 전화(트래픽)를 자동으로 배분한다. 고객은"호텔 번호"만 알면 되고, 운영 상황에 신경 쓸 필요가 없다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### Service manifest 작성

 기본 Service Manifest는 apiVersion: v1, kind: Service, metadata: name, spec: selector, ports로 구성된다. selector는"이 레이블을 가진 파드"를 백엔드로 삼겠다는 의미이고, ports는"어떤 포트로 접근하고, 어떤 백엔드 포트로 전달할지"를 정의한다.

### 문제 해결

**문제: Service에 접근 불가** - `kubectl get endpoints <service-name>`으로 백엔드 파드가 등록되었는지 확인하고, `kubectl describe service <service-name>`으로 셀렉터와 포트 설정을 확인한다.

**문제: 특정 백엔드로만 트래픽集中** - Kube-proxy가 IPVS 모드에서 Least-Connection 알고리즘을 사용하도록 설정하고, IPVS 모드로 전환한다.

### 서비스 검색

同一 클러스터 내에서는 서비스 DNS를 통해, 외부에서는 NodePort, LoadBalancer, 또는 Ingress를 통해 Service에 접근한다.外部 클라이언트가 내부 Service에 접근해야 하는 경우, NodePort 또는 LoadBalancer를 사용하고, SSL 인증서가 필요하면 Ingress와 함께 사용한다.

### 섹션 비유

 Service 선택을"고객 등급별 안내 방식"에 비유할 수 있다. ClusterIP는"동선 내에서 이동하는 내부 고객"에게 제공하고, NodePort는"직접 입구에 도착하는 방문객"에게 제공하고, LoadBalancer는"전용 셔틀버스를 갖춘 VIP 고객"에게 제공한다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대 효과

 Service를利用하면"동적으로 변하는 백엔드 파드를抽象화"할 수 있어, 마이크로서비스 간 통신이 간소화되고, 서비스 발견이 자동화되며, 로드밸런싱으로 고가용성이 제공된다.

### 핵심 정리

 Service는 복수의 백엔드 파드를 논리적 그룹으로 묶고, 고정 ClusterIP와 DNS 이름을 제공하는 네트워킹 리소스이다. Endpoints Controller가 파드 목록을 관리하고, Kube-proxy가 트래픽을 분산한다. ClusterIP, NodePort, LoadBalancer, ExternalName 등 다양한 유형이 있어, 용도에 맞게 선택할 수 있다.

### 섹션 비유

 Service를"항구 화물 집하역"에 비유할 수 있다. 수많은 선적 화물(요청)이 항구에 도착하면, 집하역 관리자(Service)이 이를 분석하여 적절한 창고(파드)로 분배한다. 각 창고(파드)의 위치가 바뀌어도(재생성), 집하역 관리자가 이를 추적하므로 화물 제공자는 집하역 번호만 알면 된다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **ClusterIP** | Service의 기본 유형으로, 클러스터 내부에서만 접근 가능한 가상 IP이다. |
| **Endpoints** | Service의 백엔드 파드IP 목록으로, Kube-proxy가 트래픽 분산에 사용한다. |
| **Kube-proxy** | Service ClusterIP로 들어오는 트래픽을 백엔드 파드로 라우팅하는 네트워크 프록시이다. |
| **CoreDNS** | Service DNS 레코드를管理하여, 서비스 이름解決을可能하게 한다. |
| **Session Affinity** | 동일 클라이언트의 요청을 동일 백엔드 파드에固定하는 기능이다. |
| **Headless Service** | clusterIP: None으로 설정되어, DNS查询時に直接 파드 IP들을 반환한다. |
| **Ingress** | L7 레벨에서 HTTP/HTTPS 트래픽을 Service로 라우팅하는 리소스이다. |
