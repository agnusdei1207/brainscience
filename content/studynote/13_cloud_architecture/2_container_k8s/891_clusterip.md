+++
weight = 891
title = "91. ClusterIP"
description = "ClusterIP: 쿠버네티스 Service의 기본 유형으로, 클러스터 내부에서만 접근 가능한 가상 IP를 할당하는 서비스"
date = 2026-03-26

[taxonomies]
tags = ["kubernetes", "k8s", "clusterip", "service", "internal-access", "virtual-ip"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ClusterIP는 쿠버네티스 Service의 기본 유형으로, 클러스터 내부에서만 접근 가능한"가상 IP"를 Service에 할당한다. 이 IP는 쿠버네티스 클러스터의 사설 네트워크 내에서만 유효하며, 외부에서는 직접 접근할 수 없다.
> 2. **가치**: 클러스터 내부의 마이크로서비스들이 서로를 호출할 때, 파드의 동적 IP가 아닌 서비스명을 통해 일관된 진입점으로 접근할 수 있게 해준다.
> 3. **융합**: Kube-proxy가 ClusterIP로 들어오는 트래픽을 실제 백엔드 파드로 라우팅하며, CoreDNS가 서비스 이름을 ClusterIP로 해결한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

ClusterIP는 쿠버네티스 Service를 생성할 때 기본으로 할당되는"클러스터 내부 전용 가상 IP"이다. 예를 들어, "my-app"이라는 Service를 생성하면 10.100.0.100과 같은 ClusterIP가 할당된다. 이 IP는 클러스터 내부의 어떤 파드에서든 접근 가능하지만, 클러스터 외부(예: 사용자의 브라우저)에서는 직접 접근할 수 없다. 이는"내부 서비스 간 통신"에만 사용되며, 외부에서 접근하려면 NodePort, LoadBalancer, 또는 Ingress 등을 통해야 한다.

### 왜 ClusterIP인가?

쿠버네티스 환경에서 파드의 IP는永久적이지 않다. 파드가 재생성되면 새 IP가 할당되고, 스케일링 되면 새로운IP가 추가된다. 만약 클라이언트가"파드 IP 10.244.1.10에 요청"이라고 하드코딩했다면, 해당 파드가 재생성될 때마다 클라이언트의 설정도 변경해야 한다. ClusterIP는 이러한"IP의 동적 변화" 문제를 해결한다. Service의 ClusterIP는 파드와 달리 변경되지 않으며, 클라이언트는 이 ClusterIP만 알면 된다.

### 비유

ClusterIP를"고급 사내 네트워킹"에 비유할 수 있다. 회사 내에서 각 직원(파드)은"사내 전화 내선 번호"를 가지고 있고, 이를 자주 변경하지 않는다. 반면"부서 대표 번호"(ClusterIP)는部署 상황이 바뀐다고 해도 동일하게 유지된다. 직원은"부서 대표 번호"에만 전화하면 되고, 부서 내誰が担当者は自動選択된다.社外之人(外部 클라이언트)는 사내 네트웍에 직접 접속할 수 없듯이, ClusterIP도 클러스터 외부에서 접근할 수 없다.

---

## Ⅱ. 아키키텍처 및 핵심 원리 (Deep Dive)

### ClusterIP 할당 방식

ClusterIP는"서비스용으로予約된IP 대역"에서自動 할당된다. kube-apiserver의 --service-cluster-ip-range 플래그로指定된 범위(예: 10.100.0.0/16) 내에서 사용되지 않는 IP가自動選択される。 ClusterIP를 明示적으로 指定하려면 spec.clusterIP에원하는 IP를 설정할 수 있지만,이미 使用중인 IP는 사용할 수 없다. "None"을 설정하면 Headless Service가 된다.

### Kube-proxy와의 협력

ClusterIP로 들어오는 트래픽은 Kube-proxy가管理한다. Service가 생성되면, Kube-proxy는 iptables(또는 IPVS) 규칙을 생성하여, ClusterIP:port로 들어오는 요청을 실제 백엔드 파드IP:port로 NAT한다. 이 과정은 커널 공간에서 직접 처리되어 효율적이다.

```
[ ClusterIP 통신 흐름 ]

┌─────────────────────────────────────────────────────────────────────────┐
│                    ClusterIP 통신 흐름                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [클라이언트 파드]                                                        │
│  app: my-client                                                        │
│  /etc/resolv.conf:                                                     │
│    nameserver 10.244.0.10 (CoreDNS)                                    │
│                                                                         │
│  코드: requests.get("http://my-app:80")                               │
│         │                                                               │
│         │ (DNS解決)                                                     │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  CoreDNS: my-app.default.svc.cluster.local → 10.100.0.100       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  [ClusterIP 10.100.0.100으로 요청 전송]                                  │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Kube-proxy (iptables/IPVS)                                       │   │
│  │  ClusterIP:10.100.0.100 → NAT → 백엔드 파드IP 중 하나             │   │
│  │  • 10.244.1.10:80 (확률 33%)                                    │   │
│  │  • 10.244.1.11:80 (확률 33%)                                    │   │
│  │  • 10.244.2.15:80 (확률 33%)                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  [백엔드 파드 중 하나로 요청 전달]                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 클라이언트 파드에서"my-app:80"으로 요청을 보내면, 首先 CoreDNS가 이 이름을ClusterIP(10.100.0.100)로解決한다. 그 후, 요청이 ClusterIP로 전송되고, Kube-proxy가 이를 가로채 실제 백엔드 파드IP 중 하나로 NAT한다. 클라이언트는"my-app"만 알면 되고, 백엔드가 뭐든(파드IP가 뭐든) Service가 알아서 처리한다.

### 내부 DNS 해결

 Service 이름의 FQDN(정규화된 도메인 이름)은"<service-name>.<namespace>.svc.cluster.local"이다. 같은 네임스페이스 내에서는 <service-name>만으로도 접근 가능하고, 다른 네임스페이스에서는<service-name>.<namespace>로 접근할 수 있다. CoreDNS가 이 DNS 레코드를管理하며, Service 생성/삭제 시 자동으로 DNS 레코드가追加/削除される.

### 외부 접근과의 비교

| 접근 방식 | 범위 | 외부 노출 | 용도 |
|:---|:---|:---|:---|
| **ClusterIP** | 클러스터 내부만 | 아니오 | 마이크로서비스 간 통신 |
| **NodePort** | 클러스터 외부+내부 | 예 (노드 IP:Port) | 개발/단위 테스트 |
| **LoadBalancer** | 클러스터 외부+내부 | 예 (공인 IP) | 프로덕션 외부 노출 |
| **Ingress** | HTTP/HTTPS만 | 예 (도메인 기반) | 웹 애플리케이션 외부 노출 |

### 섹션 비유

 ClusterIP의 DNS解決을"기업 내 이름서베"에 비유할 수 있다. 신입사원"홍길동"이 입사하면(파드 생성),人事팀(Endpoints Controller)이 이름서를 업데이트하고, CoreDNS(전화 번호부)가 이를反映한다. 이제"개발팀"(Service 이름)이라고 검색하면,人事팀이 현재 휴가 중이거나會議 중인 사람以外的"개발팀 구성원"을 자동 선택하여 연결해준다.社外之人는 이 이름서를 열람할 수 없듯이, ClusterIP도 외부에서 접근할 수 없다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### ClusterIP vs NodePort vs LoadBalancer

 ClusterIP는"클러스터 내부 통신 전용"이고, NodePort는"노드의 특정 포트를 열어 외부 접근"을 허용하며, LoadBalancer는"클라우드 인프라의 로드밸런서를 프로비저닝"하여 외부 접근을 허용한다. 일반적으로 외부 노출이 필요하면 Ingress를 사용하고, TCP/UDP 레벨에서 외부 노출이 필요하면 LoadBalancer를 사용하며, 내부 통신에는 ClusterIP만으로 충분하다.

### Headless Service와의 비교

 ClusterIP에 None을 설정하면 Headless Service가 된다. 일반 ClusterIP는"단일 가상 IP"를 제공하여 Kube-proxy가 트래픽을 분산한다. 반면 Headless Service는"가상 IP 없음"으로, DNS 쿼리 시 직접 파드IP 목록을 반환한다. 이는 StatefulSet에서 각 파드에 직접 접근해야 하는 경우에 사용된다.

### ClusterIP의 제한

 ClusterIP는"클러스터 내부에서만" 접근 가능하다. 따라서"외부에서 웹 애플리케이션에 접근"하려면 ClusterIP만으로는 부족하고, NodePort, LoadBalancer, 또는 Ingress가 필요하다. 또한 ClusterIP는"내부 로드밸런싱"만 지원하고, URL 기반 라우팅 등 L7 기능은 지원하지 않는다.

### 섹션 비유

 ClusterIP와 LoadBalancer의 관계를"국내 전용 고속도로"와"해외 항공편"에 비유할 수 있다. ClusterIP는 국내 전용 고속도로로, 国内에서만(클러스터 내부)에서만使用可能하고,国外からの直接 접속은 할 수 없다. LoadBalancer는 해외 항공편으로,国内外联通이 가능하지만, 운영 비용이 훨씬 높다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### ClusterIP 선택적 지정

 spec.clusterIP에 IP를指定すると、そのIPが自動的に使用される。既存のServiceと重複するIPは指定不可で、未使用のIP만指定 가능하다. 通常は автоматически 할당된IP를 사용하며, 明示적指定はテスト나特定の架构을 구축할 때만 필요하다.

### 여러 Port 서비스

 하나의 Service에서 여러 포트를 사용할 수 있다. 예를 들어, 서비스가 80(http)과 443(https) 두 포트를 exposed하면, spec.ports 배열에 두 항목을 모두 추가한다. 단, 모든 포트의 targetPort가 동일한 레이블 셀렉터의 파드를 가리켜야 한다.

### 외부 서비스 참조

 다른 네임스페이스의 Service나 외부 IP를 Service로 참조할 수 있다.ExternalName Service(spec.type: ExternalName)를 사용하면 서비스 이름을 CNAME으로 매핑하여 외부 서비스에 접근할 수 있다. 이는 마이크로서비스가 외부 데이터베이스나 API를 호출할 때活用된다.

### 섹션 비유

 여러 포트 서비스롤"문화센터 복합건물"에 비유할 수 있다. 건물 안에"미술관"(포트 80), "도서관"(포트 443), "미술학원"(포트 8080)이 있는데, 모두同一의 건물 번호(ClusterIP)를 공유한다. 찾는 곳이 다르면port를 다르게 하여同一 건물 내에서 서로 다른 시설을 찾을 수 있다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대 효과

 ClusterIP를 이용하면"마이크로서비스 간의 느슨한 결합(Loose Coupling)"을実現할 수 있다. 클라이언트는"서비스명"만 알면 되고, 백엔드 파드의 IP나数は意識할 필요가 없다. 이로 인해 서비스 배포, 스케일링, 업데이트가 독립적으로 수행될 수 있다.

### 핵심 정리

 ClusterIP는 Service의 기본 유형으로, 클러스터 내부에서만 접근 가능한 가상 IP를 할당한다. CoreDNS가 서비스 이름을 ClusterIP로 해결하고, Kube-proxy가 트래픽을 백엔드 파드에 분산한다. 내부 마이크로서비스 통신에 사용되며, 외부 노출이 필요하면 NodePort, LoadBalancer, 또는 Ingress를 사용한다.

### 섹션 비유

 ClusterIP를"고객 자동 안내 키오스크"에 비유할 수 있다. 키오스크(ClusterIP)에"한식당을 찾는다"고 하면(서비스명 요청), 시스템이 현재 영업 중이고待機可能한 seats가 있는 한식당(백엔드 파드) 중 하나를 자동 선택하여 길을 안내한다. 고객은"어떤 한식당인지"를 몰라도 항상 가까운空闲한 한식당으로 안내받을 수 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Service** | ClusterIP, NodePort, LoadBalancer 등 다양한 유형의 서비스 접근점을 제공한다. |
| **Kube-proxy** | ClusterIP로 들어오는 트래픽을 백엔드 파드로 라우팅하는 네트워크 프록시이다. |
| **CoreDNS** | 서비스 이름을 ClusterIP로 해결하는 DNS 서버이다. |
| **Endpoints** | Service의 백엔드 파드IP 목록이다. |
| **Headless Service** | clusterIP: None으로 설정되어 DNS解決 시 직접 파드IP 목록을 반환한다. |
| **NodePort** | 노드 IP의 특정 포트를 열어 외부에서 Service에 접근할 수 있게 한다. |
| **LoadBalancer** | 클라우드 인프라의 로드밸런서를 프로비저닝하여 외부 접근을 허용한다. |
