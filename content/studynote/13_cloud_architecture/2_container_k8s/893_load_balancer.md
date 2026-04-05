+++
weight = 893
title = "93. LoadBalancer"
description = "LoadBalancer: 클라우드 인프라와 연동하여 외부 공인 IP를 할당받고 외부 트래픽을 Service로 분산시키는 쿠버네티스 Service 유형"
date = 2026-03-26

[taxonomies]
tags = ["kubernetes", "k8s", "loadbalancer", "service", "cloud-integration", "external-access"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LoadBalancer는 Service 유형의 하나로, 클라우드 인프라(AWS ELB, Azure LB, GCP CLB 등)와 연동하여 외부 공인 IP를 프로비저닝하고, 해당 IP로 들어오는 외부 트래픽을 내부 Service로 분산시키는 방식이다.
> 2. **가치**: 사용자는"단일 공인 IP"만 알면 되고, 클라우드에서 자동으로 로드밸런서가 구성되어 고가용성과 확장성을 제공한다. 외부에서 애플리케이션에 접근하는 가장 일반적인 프로덕션 방식이다.
> 3. **융합**: NodePort의 상위 버전으로, 내부적으로 NodePort를 사용하면서 클라우드 네이티브 LB 기능을 추가한다. Ingress와 함께 사용하면 HTTP/HTTPS L7 라우팅도 가능하다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

LoadBalancer는 쿠버네티스 Service 유형 중"외부 노출"의 최종形態이다. NodePort가"노드의 물리 포트"를 откры하고, ClusterIP가"내부 가상 IP"만 제공한다면, LoadBalancer는"클라우드 인프라의 관리형 로드밸런서"를 프로비저닝하여"공인 IP"를 할당받는다. 외부 클라이언트가 이 공인 IP로 요청을 보내면, 클라우드 로드밸런서가 이를 노드에 분산하고, 노드의 Kube-proxy가 다시 내부 Service로 전달한다.

### 왜 LoadBalancer인가?

NodePort의 경우"노드의 IP:Port"를 알아야 하는데, 노드가 여러 대이면"어떤 노드의 IP를 사용해야 하는가"라는 문제가 있다. 또한 노드가 장애 나면 해당 노드의 IP로 접근할 수 없다. LoadBalancer는"단일 공인 IP"만 제공하여 이러한 문제를 해결한다. 클라우드 로드밸런서가 자동으로 여러 노드에 트래픽을 분산하므로, 특정 노드 장애 시에도 다른 노드로 우회된다.

### 비유

LoadBalancer를"국제공항의 대규모 터미널"에 비유할 수 있다. 수백 개의 게이트(노드 포트)가 있지만, 승객(외부 클라이언트)은"터미널 번호 1번"이라는 단일 입구만 알면 된다. 터미널 내부의 안내 시스템(로드밸런서)이 각 게이트로 승객을 균형 있게分散하고, 특정 게이트(노드)가 닫혀도 다른 게이트로 우회한다.

---

## Ⅱ. 아키키텍처 및 핵심 원리 (Deep Dive)

### LoadBalancer 동작 원리

 LoadBalancer Service를 생성하면, 다음 과정이 자동으로 수행된다. (1) 쿠버네티스가 각 노드에 NodePort를 откры한다. (2) 쿠버네티스가 클라우드 提供자의 로드밸런서를 프로비저닝하도록 요청한다. (3) 클라우드 提供자(예: AWS)가"Network Load Balancer(NLB)" 또는"Classic Load Balancer(CLB)"를 생성하고, 공인 IP를 할당한다. (4) 로드밸런서의 대상 그룹이 NodePort를 통해 노드들을 등록한다.

```
[ LoadBalancer 통신 흐름 ]

┌─────────────────────────────────────────────────────────────────────────┐
│                    LoadBalancer 통신 흐름                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  외부 클라이언트 (브라우저)                                             │
│  URL: https://203.0.113.100/                                           │
│         │                                                               │
│         │ (203.0.113.100으로 요청)                                      │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  클라우드 로드밸런서 (AWS NLB / Azure LB / GCP CLB)             │   │
│  │                                                                  │   │
│  │  공인 IP: 203.0.113.100                                         │   │
│  │  프로토콜: TCP:80 → NodePort 30080으로 분산                     │   │
│  │                                                                  │   │
│  │  대상 그룹:                                                      │   │
│  │  • Node #1:30080 (10.0.0.1)                                    │   │
│  │  • Node #2:30080 (10.0.0.2)                                    │   │
│  │  • Node #3:30080 (10.0.0.3)                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         │ (노드 중 하나에서 수신)                                        │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Worker Node #1 (10.0.0.1)                                      │   │
│  │                                                                  │   │
│  │  [NodePort 30080]                                               │   │
│  │       │                                                          │   │
│  │       │ Kube-proxy가 ClusterIP Service로 전달                   │   │
│  │       ▼                                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────┐ │   │
│  │  │  ClusterIP Service: 10.100.0.100 (nginx-svc)                │ │   │
│  │  └─────────────────────────────────────────────────────────────┘ │   │
│  │       │                                                          │   │
│  │       │ Kube-proxy가 백엔드 파드로 분산                          │   │
│  │       ▼                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │   │
│  │  │ nginx-0  │  │ nginx-1  │  │ nginx-2  │                      │   │
│  │  └──────────┘  └──────────┘  └──────────┘                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** LoadBalancer의 핵심은"클라우드 인프라との連携"이다. 외부 클라이언트는"단일 공인 IP"만 알면 되고, 클라우드 로드밸런서가 노드 간 부하를分散한다. 만약 Node #1이 장애 나면, 로드밸런서가 자동으로 Node #2, #3만 대상으로 등록하고, Node #1로는 트래픽을 보내지 않는다. 이로 인해"고가용성"이 자동으로 обеспечивается.

### 클라우드 별 LB 유형

 각 클라우드 提供자마다 다른 유형의 로드밸런서를 제공한다. **AWS**: Network Load Balancer (NLB, L4), Application Load Balancer (ALB, L7, Ingress와 연동), Classic Load Balancer (CLB, 레거시). **Azure**: Load Balancer (L4), Application Gateway (L7). **GCP**: Network Load Balancer (L4), Cloud Load Balancing (L7, Ingress와 연동). 쿠버네티스 Service의 LoadBalancer는 통상 L4 레벨에서 동작하며, L7 HTTP/HTTPS 라우팅이 필요하면 Ingress와 함께 사용한다.

### 비용 Considerations

 LoadBalancer는"클라우드 리소스"이기 때문에 비용이 발생한다. 각 클라우드 提供자마다 다르지만, 일반적으로"시간당 LB 사용료 + 데이터 처리량 기반료"가 부과된다. 대규모 서비스가 아닌 경우, 비용을 고려하여 NodePort + Ingress로 대체하거나, 서비스 메시(Istio, Linkerd)의 ingress 게이트웨이를 활용할 수 있다.

### 섹션 비유

 클라우드 LoadBalancer를"항구的大型 크레인 조율 시스템"에 비유할 수 있다. 항구에는 수십 개의 크레인(노드)이 있고, 각 크레인의 작업 속도가 다르다. 조율 시스템(로드밸런서)이 화물선(클라이언트)의 요청을 받아 현재 가장 덜 바쁜 크레인을 선택하여 화물을下ろ搬运한다. 만약 특정 크레인(노드)이故障이면, 조율 시스템이 이를 감지하고 다른 크레인으로 자동 우회한다. 항구 운영자는"조율 시스템의 번호"(공인 IP)만 알면 된다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### LoadBalancer vs Ingress

| 비교 항목 | LoadBalancer | Ingress |
|:---|:---|:---|
| **레벨** | L4 (TCP/UDP) | L7 (HTTP/HTTPS) |
| **프로토콜** | 모든 | HTTP/HTTPS만 |
| **URL 라우팅** | 불가 | 가능 |
| **SSL 종료** | 불가 (별도 설정 필요) | 가능 |
| **비용** | LB당 비용 | Ingress 컨트롤러당 비용 |
| **용도** | TCP/UDP 서비스 | HTTP 웹 서비스 |

### 내부 LoadBalancer

 대부분의 클라우드 提供자는"Internal LoadBalancer"를 지원한다. 이는"사설 IP"만 할당받는 LoadBalancer로, VPC 내부에서만 접근 가능하고 외부 인터넷에는 노출되지 않는다. 내부 마이크로서비스 간 통신에서"단일 진입점"이 필요할 때 활용된다.

### LoadBalancer와 Ingress의 조합

 HTTP/HTTPS 웹 서비스의 경우, 통상"LoadBalancer + Ingress" 조합을 사용한다. LoadBalancer는 L4 레벨에서 동작하여 TCP 트래픽을 수신하고, Ingress Controller가 L7 레벨에서 HTTP Host/Path 기반 라우팅을 수행한다. 이 조합이 HTTPS 인증서 관리와 URL 라우팅을 모두 해결하는 가장 일반적인 패턴이다.

### 섹션 비유

 LoadBalancer + Ingress 조합을"대형 관홀의 안내 시스템"에 비유할 수 있다. 대형 쇼핑몰(LoadBalancer)의 안내 데스크가 1층 로비에 있고, 방문객은"1층 안내 데스크"(공인 IP)만 알면 된다. 안내 데스크(LoadBalancer)가"3층 음식점"(Service A)과"4층 영화관"(Service B)을 모두 관리하며, 각 층의 안내 키오스크(Ingress)가"3층 5번 매장"(파드)으로具体的に案内한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### LoadBalancer 설정

 LoadBalancer Service를 생성하려면 spec.type을"LoadBalancer"로 설정하고, port(LB 포트), targetPort(백엔드 포트)를指定한다. cloud provider에 따라 몇 가지注解(annotations)을 추가하여 LB 유형이나 기능을制御할 수 있다.

### health check 설정

 클라우드 로드밸런서는"대상 노드"또는"대상 파드"에 대한 health check를 수행한다. health check에 실패한 노드/파드는 로드밸런서 대상에서 자동으로 제외된다. health check 설정(interval, timeout, threshold)은 cloud provider의 기본값을 사용하거나 커스터마이즈할 수 있다.

### 비용 최적화

 매 Service마다 별도의 LoadBalancer를プロ비저닝하면 비용이 증가한다. 비용을 최적화하려면"여러 Namespaces의 Service를 단일 Ingress으로统一라우팅"하거나,"Service Mesh의 ingress 게이트웨이"를 활용하여 단일 LoadBalancer로 여러 서비스를 운영하는 것이 좋다.

### 섹션 비유

 LoadBalancer 비용을"호텔 커넥션 수수료"에 비유할 수 있다. 객실(파드)마다 전용 전화 회선(LoadBalancer)을 연결하면通信品質は最高だが、コストが大幅に上昇한다. 따라서 대부분의 호텔은"로비 전화 교환 시스템"(Ingress)으로 여러 객실을统一관리하여, 비용을 절감하면서도 한 전화번호로 모든 객실에 도달할 수 있다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대 효과

 LoadBalancer를 이용하면"고가용성 외부 진입점"을 提供받을 수 있다. 단일 공인 IP로 여러 노드에 트래픽을 분산하고, 노드 장애 시 자동 우회하며, 클라우드 인프라의 관리형 서비스를 활용하여 운영 부담을 줄일 수 있다.

### 핵심 정리

 LoadBalancer는 클라우드 인프라와 연동하여 외부 공인 IP를 할당받고, 외부 트래픽을 내부 Service로 분산시키는 Service 유형이다. NodePort를 기반으로 하며, 클라우드 提供자의 로드밸런서를 활용한다. L4 레벨에서 동작하여 TCP/UDP 모두 지원하며, L7 HTTP/HTTPS 라우팅이 필요하면 Ingress와 함께 사용한다.

### 섹션 비유

 LoadBalancer를"국제 특급열차의 중앙 관제소"에 비유할 수 있다. 열차(트래픽)가 분기점(로드밸런서)에 도착하면, 관제소가 현재 상황(노드 상태)을 파악하고 가장 적절한 노선으로 열차를 направ한다. 특정 구간(노드)에 문제(장애)가 생기면, 관제소가即座에 우회 노선(다른 노드)으로 열차를 재 направ한다. 열차 이용객은"중앙 관제소가管理하는 노선"만 알면目的地에 도착할 수 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **NodePort** | LoadBalancer는 내부적으로 NodePort를 사용하여 노드에 트래픽을 전달한다. |
| **ClusterIP** | LoadBalancer는 내부적으로 ClusterIP Service를 생성하여 백엔드를 관리한다. |
| **Ingress** | L7 HTTP/HTTPS 라우팅이 필요할 때 LoadBalancer와 함께 사용된다. |
| **클라우드 LB** | AWS NLB/ALB, Azure Load Balancer, GCP Cloud Load Balancing 등 |
| **Internal LB** | VPC 내부에서만 접근 가능한 사설 IP 기반 LoadBalancer이다. |
| **Health Check** | 로드밸런서가 노드/파드의可用性を주기적으로 확인하는 기능이다. |
