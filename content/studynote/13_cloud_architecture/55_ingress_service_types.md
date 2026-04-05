+++
weight = 55
title = "55. Ingress/Service 타입"
date = "2026-04-05"
[taxonomies]
tags = ["Cloud", "Kubernetes", "K8s", "Ingress", "Service", "LoadBalancer"]
categories = ["13_cloud_architecture"]
+++

# Ingress/Service 타입

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: Service는 파드를 네트워크에 노출하는 쿠버네티스 네트워킹 추상화이며, Ingress는 HTTP/HTTPS URL 경로나 호스트 이름 기반으로 다수의 Service로 L7 라우팅하는 외부 진입점이다.
> 2. **가치**: 이 계층 구조는 외부 트래픽이 LoadBalancer → Ingress → Service → Pod 순서로 흐르며, 단일 공인 IP로 수십 개의 서비스를 구분하여提供服务할 수 있게 한다.
> 3. **융합**: Ingress와 Service는 쿠버네티스 네트워킹 모델의 핵심이며, Ingress 컨트롤러(nginx-ingress, Traefik)와 클라우드 네이티브 LB가 결합하여 완전한 L4/L7负载分散(로드밸런싱)을 실현한다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

쿠버네티스에서 실행되는 파드는 동적으로 생성되고 IP가 수시로 변경된다. 게다가 파드는 클러스터 내부에서만 접근 가능하므로,外部(외부)에서 트래픽을 보내려면 네트워크 추상화가 필수적이다. Service는 이러한 요구를 해결하기 위해 파드를 하나의 논리적 서비스로 grouping하고 고정 ClusterIP를 할당하는 역할을 한다. 하지만 Service의ClusterIP는 단순히 파드를 그룹화할 뿐, URL 경로나 호스트 이름에 따른 라우팅은 불가능하다. 수십 개의 마이크로서비스를 운영하는 MSA 환경에서 각각의 서비스에 대해 하나의 LoadBalancer를 생성하면 비용이 엄청나게 增加하고 관리 복잡도도指数関数的に(지수함수적으로) 증가한다.

Ingress는 이 문제의终极적(궁극적) 해결책으로, 단일 외부 IP 주소에서 HTTP/HTTPS 요청을 분석하여 다수의 백엔드 서비스로 라우팅한다. 예를 들어 `api.example.com/users`로 오는 요청은 User Service로, `api.example.com/products`로 오는 요청은 Product Service로 보내는 것이 가능하다. 이는 비용을 크게 절감하고, SSL/TLS 종료를 Ingress에서集中管理하며, 캐싱과 rate limiting 같은 L7 기능을提供할 수 있게 한다.

```text
[외부 트래픽 → Ingress → Service → Pod 흐름]
┌──────────────────────────────────────────────────────────────────────────────┐
│                         외부 인터넷                                             │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │ HTTPS (443)
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  [Ingress Controller]  ★ 단일 외부 IP                                         │
│  - Host: api.example.com → user-svc:8080                                     │
│  - Host: api.example.com → product-svc:8080                                  │
│  - Path: /admin → admin-svc:8080                                             │
│  - TLS Termination (SSL offload)                                            │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   │ 내부 HTTP
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
     ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
     │  User Svc    │      │ Product Svc  │      │  Admin Svc   │
     │ ClusterIP:80 │      │ ClusterIP:80 │      │ ClusterIP:80 │
     └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
            │                    │                    │
            ▼                    ▼                    ▼
     ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
     │ Pod: user-1  │      │Pod: product-1│      │Pod: admin-1  │
     │ Pod: user-2  │      │Pod: product-2│      │ Pod: admin-2 │
     └──────────────┘      └──────────────┘      └──────────────┘
```

이 구조의 핵심은 Ingress가 HTTP/HTTPS 레벨의 정보를 사용한 정교한 라우팅을 제공한다는 점이다. Service의 ClusterIP는 단순히 "어떤 파드에 보내야 하는가"만을 알려주지만, Ingress는 "어떤 호스트/경로의 요청을 어느 서비스로 보낼 것인가"를 URL 기준으로 결정한다. 이로 인해 비용이 절감되고, SSL 인증서 관리가集中화되며, 웹 애플리케이션 방화벽(WAF), 인증, 캐시 등의 고급 기능을Ingress 계층에서 수행할 수 있다.

📢 **섹션 요약 비유**: Ingress와 Service의 관계는 국제공항의 여객 교통 시스템과 같습니다. Ingress는공항欢迎您(텃间的) 안내 데스크로서 "서울에서 온 여객은 1번 게이트로, 부산에서 온 여객은 2번 게이트로" 분류하는 것이며, Service는 각 게이트에서 버스를 타고 목적지(파드)로 이동하는 것입니다. 단일 공항 건물(단일 Ingress IP)에서 수많은 목적지(수백 개 서비스)로 효율적으로 여객을 분산시키는 구조입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**Service 타입**은 네 가지 종류가 있으며, 각각 다른 네트워크 시나리오에 사용된다. **ClusterIP**는 클러스터 내부에서만 통신 가능한 기본 타입으로, backend 서비스 간 내부 통신에 가장 많이 사용된다. **NodePort**는 워커 노드의静态 포트(기본 30000~32767)를 열어 외부 트래픽을 수신하는 방식으로, 개발/데모 환경이나 매우 간단한 외부 노출에 적합하다. **LoadBalancer**는 클라우드 벤더의-managed LB(예: AWS NLB, GCP Cloud LB)와連携하여 외부 공인 IP를 할당받는 방식으로, Production 환경에서 외부 트래픽을 수신하는 표준 방식이다. **ExternalName**은 클러스터 내부 DNS에 외부 서비스(예: `mysql.prod.example.com`)를 매핑하여, 나중에 서비스 이름 변경 시에도 코드를 修改하지 않고 유지보수할 수 있게 한다.

```text
[Service 타입별 통신 범위]
┌─────────────────────────────────────────────────────────────────────┐
│ NodePort (외부 접속 허용)                                           │
│                                                                      │
│  ☁️ 인터넷 ──→ [노드 IP:30000] ──→ [Service:ClusterIP] ──→ [Pod]    │
│               포트 변환                                                │
├─────────────────────────────────────────────────────────────────────┤
│ LoadBalancer (클라우드 LB 연동)                                      │
│                                                                      │
│  ☁️ 인터넷 ──→ [클라우드 LB] ──→ [노드 IP:동적 포트] ──→ [Pod]     │
│               공인 IP 자동 할당                                        │
├─────────────────────────────────────────────────────────────────────┤
│ ClusterIP (내부 전용)                                                │
│                                                                      │
│  [파드 A] ──→ [Service:ClusterIP] ──→ [파드 B]                     │
│               오직 클러스터 내부 통신                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Ingress**는 사실 쿠버네티스 리소스일 뿐이며, Ingress 리소스를 처리하려면 반드시 Ingress Controller가 클러스터에 설치되어 있어야 한다. Ingress Controller는 Ingress 리소스의 규칙을 읽고 실제로 트래픽을 라우팅하는 运行 중인(실행중인) 파드이다. 대표적으로 **NGINX Ingress Controller**가 가장 널리 사용되며, **Traefik**, **HAProxy**, **Contour** 등이 있다. Ingress 리소스는 호스트 기반 라우팅(`host: example.com`), 경로 기반 라우팅(`path: /api`), TLS 종료, 단일 IP에 여러 호스트 묶기 등 다양한 기능을 지원한다.

```yaml
# Ingress Manifest 예시
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /  # 경로 재작성
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /users
        pathType: Prefix
        backend:
          service:
            name: user-svc
            port:
              number: 80
      - path: /products
        pathType: Prefix
        backend:
          service:
            name: product-svc
            port:
              number: 80
  tls:
  - hosts:
    - api.example.com
    secretName: api-tls-secret  # TLS 인증서
```

Ingress의 동작原理은 다음과 같다. 외부 요청이 들어오면 Ingress Controller가Host와Path를 检查하고 해당하는 Service를 결정한다. Service는Endpoints를 통해 실제 파드 IP 목록을얻고, kube-proxy(iptables/IPVS)가 파드 중 하나로 트래픽을 전달한다. 이 과정에서 Ingress Controller는 TLS를 종료(SSL offload)하여 내부 통신은 평문 HTTP로 처리하므로 성능을 최적화할 수 있다.

📢 **섹션 요약 비유**: Ingress Controller는酒店(호텔)의 벨매니저와 같습니다.客人が(손님이) 호텔 로비(Ingress)에 들어오면, 벨매니저가 「2층 203호실은restaurant로, 3층 301호실은 짐寄存처로」 라고 지도(경로 기반 라우팅)를 나눠주고, 짐을寄存하고(SSL 종료) 각客室(파드)으로 안내하는 것입니다. 벨매니저가 없으면 손님은 방을 찾을 수 없고, 경로를 잘못 안내하면 다른 손님의 방에 들어갈 수도 있습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

Service 타입 선택은 환경과 시나리오에 따라 달라진다. **단순 내부 통신**에는 ClusterIP가 적합하고, **외부 임시 접속**에는 NodePort가 간편하다. 그러나 NodePort는 포트 번호가随机(무작위)로 할당되고, 하나의 포트에 하나의 서비스만 매핑되므로 확장성이 떨어진다. 따라서 **Production 외부 LB**에는 반드시 LoadBalancer를 사용해야 하며, 클라우드 벤더의 NLB(Network Load Balancer, L4)나 ALB(Application Load Balancer, L7)와Integration하여 성능과 기능을確保해야 한다.

| 서비스 타입 | 적합한 시나리오 | 장점 | 단점 |
|:---|:---|:---|:---|
| ClusterIP | 마이크로서비스 간 내부 통신 | 단순, 빠름 | 외부 접근 불가 |
| NodePort | 개발/데모, 임시 외부 노출 | 간단한 설정 | 포트 관리 복잡, 보안 이슈 |
| LoadBalancer | Production 외부 LB | 클라우드 통합, 관리 용이 | 비용 (LB당 과금) |
| ExternalName | 외부 서비스 DNS 매핑 | 코드 변경 없이 리다이렉션 | 단방향 참조만 |

Ingress와 Service의 조합은 MSA에서特に(특히) 중요하다. MSA에서는数十에서数百 개의 서비스가 존재하며, 각각에 대해 LoadBalancer를 생성하면 비용이 엄청나게 增加한다. Ingress를 사용하면 단일 IP와 단일 LB로 모든 서비스를 라우팅하므로 비용이 크게 절감된다. 또한 Ingress는 경로 기반 라우팅뿐만 아니라, ** Canary Deployment**(신버전을 일부 사용자에게만 노출), **A/B 테스트**(트래픽을 비율로 분할), **Blue-Green Deployment**(무중단 전환) 등을 구현하는 데도 활용된다.

```text
[Canary Deployment via Ingress]
┌─────────────────────────────────────────────────────────────────┐
│                    Ingress Controller                            │
│  - weight: v1=90%, v2=10%                                       │
│    (트래픽 90%는 구버전, 10%만 신버전으로)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
     ┌──────────────────┐         ┌──────────────────┐
     │  Service (v1)    │         │  Service (v2)   │
     │  pod-v1: 9개     │         │  pod-v2: 1개     │
     └──────────────────┘         └──────────────────┘
```

Ingress Controller 선택도 중요한 결정이다. NGINX Ingress Controller는 풍부한 기능을持ち Community驱动으로 지속적으로 업데이트되며, AWS ALB Ingress Controller는 AWS ALB를 직접 사용하여 클라우드 네이티브 기능(	WPS, 로그 분석 등)을活用할 수 있다. Traefik은 Istio와Integration하기 쉽고, Contour는 Envoy 기반의高性能을 제공한다.

📢 **섹션 요약 비유**: Service 타입 선택은 등산을 위해등산로를選択하는 것과 같습니다. ClusterIP는 산길 오름길(내부 전용 길)이고, NodePort는 가파른 비상구덜기(임시), LoadBalancerはynchronously(비동기)大型 Cable Car(케이블카)로 항아리까지 빠르게 이동하게 합니다. Ingress는山頂에 있는 종합 안내소로서, 등산객(트래픽)이 오면 각 루트(파드)로 분산시키는 원procal(원쁠) 길잡이입니다.

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

Production 환경에서 Ingress를 운영할 때는 다음要点(요점)을 반드시 고려해야 한다. First, 단일 Ingress Controller의 단일 장애점을 방지하기 위해 Ingress Controller를DaemonSet으로 배포하고 replicas를 2개 이상 설정해야 한다. Second, TLS 인증서는 Let's Encrypt와 같은 자동화 도구를 사용하여 갱신漏れ(만료)를防止해야 한다. Third, Ingress의Host는 반드시 실제 도메인 이름으로 설정해야 하며, IP 기반 라우팅은避けた(피해야) 한다. Fourth, 대규모 트래픽 환경에서는 Ingress Controller의 리소스 limits를 충분하게 설정하여 CPU/메모리 포화 상태를 방지해야 한다.

Service의 서비스 검색(Discovery)도 중요한 고려사항이다. 쿠버네티스는 클러스터 내부 DNS(CoreDNS)를 통해 서비스 이름으로 자동 등록하고, `{service-name}.{namespace}.svc.cluster.local`形式으로解析可能である.同一 네임스페이스 내에서는 단순히 서비스 이름만으로 접근할 수 있어 애플리케이션 코드에서 하드코딩된 IP 대신 서비스 이름을 사용할 수 있다. 이는 파드의 IP가 동적으로 변하는 쿠버네티스 환경에서 필수적인 기능이다.

```text
[Production Ingress/Svc 安全运营 체크리스트]
1. Ingress Controller 강화
   ├─ replicas: 2+ (고가용성)
   ├─ resources: requests/limits 설정
   ├─ topologySpreadConstraints: 노드 분산 배치
   └─ prometheus metrics 활성화 (모니터링)

2. TLS/SSL 관리
   ├─ cert-manager + Let's Encrypt 자동화
   ├─ 인증서 만료 모니터링 (Alert)
   └─ TLS 버전: 1.2 이상만 허용

3. Rate Limiting & QoS
   ├─ nginx.ingress.kubernetes.io/limit-rps: 요청 수 제한
   ├─ annotation 기반 whitelist/blacklist IP
   └─ Web Application Firewall (WAF) 연동

4. 서비스 검색
   ├─ CoreDNS replicas: 2+ (가용성)
   ├─ headless Service ( StatefulSet 분산 DNS)
   └─ EndpointSlice 활성화 (대규모 환경 성능)
```

또한 Ingress와 Service의 연동에서 주의해야 할 점이 있다. Ingress의backend는 Service 이름이며, Service는Endpoints를 통해 실제 파드를 추적한다. 파드가 아직 준비되지 않았거나(ready=false)Endpoint가 비어있으면Ingress Controller는 해당_backend로 트래픽을 보내지 않는다. 따라서 readinessProbe가 필수이며, Ingress의 health check 설정과Service의 readinessProbe 설정이 서로 일치해야 한다.

📢 **섹션 요약 비유**: Ingress/Svc 운영은 항구의 톤널 교통 통제 시스템과 같습니다. Ingress Controller는 톤널 입구의 신호 제어기이고, Service는 톤널 내부의 분기점이며, Pod는 톤널 끝의 도착지입니다. 신호 제어기가 고장 나면 전체 톤널이 마비되고(HA 필요), 도착지가 준비되지 않으면(Endpoint 없음) 신호 제어기가 해당 길로 트래픽을 보내지 않습니다(자동 차단).

### Ⅴ. 기대효과 및 결론 (Future & Standard)

Ingress와 Service 타입을 적절히 활용하면, MSA 환경에서 외부 접근을 효율적으로 관리하고 비용을 크게 절감할 수 있다. 단일 Ingress IP로 수백 개의 서비스를 라우팅하면, 각각의 서비스에 LoadBalancer를 provisioning하는 것 대비 연간 수천 달러의 비용을 절감할 수 있다. 또한 TLS 종료를Ingress에서集中管理하면证书管理의 복잡도를 줄이고, WAF나 rate limiting과 같은 L7 기능을 중앙에서 적용하여 보안성을 높일 수 있다.

| 기대 효과 | 도입 전 (서비스당 LB) | 도입後 (Ingress 통합) | 효과 |
|:---|:---|:---|:---|
| 외부 IP 수 | 100개 (100 서비스) | 1개 (Ingress 1개) | 99% 감소 |
| TLS 인증서 관리 | 100개 개별 관리 | 1곳 중앙 관리 | 90% 간소화 |
| 비용 (LB) | $500/월 (100 LB) | $20/월 (NLB 1개) | 96% 절감 |
| 경로 기반 라우팅 | 불가 | 완전 지원 | 새 기능 획득 |

미래에는 Ingress와 Service 메쉬(Service Mesh)가 더욱 긴밀하게 통합될 것으로 예상된다. Istio와 같은 서비스 메시에서는 Ingress Gateway를 통해 외부 트래픽을 수신하고, 사이드카 프록시(Envoy)가 mTLS와流量管理(트래픽 관리)를 담당하는架构으로 발전하고 있다. 또한 Ingress 리소스의 표준화进程中(진행중)이며, Gateway API(Gateway API v1)是新的Ingress標準으로 점진적 확대되고 있다. 결론적으로, Ingress와 Service 타입은 쿠버네티스 네트워킹의 양대 축이며, 둘을 적절히 조합하여 비용 효율적이고安全하며高性能な(高性能인) 클라우드 네이티브 네트워크를 구축할 수 있다.

📢 **섹션 요약 비유**: Ingress와 Service의 조합은 세계적 특급 호텔의 방 배정 시스템과 같습니다.ingressは(인그레스는) 세계 어디에서든 하나의 대표 번호(공인 IP)로 호텔에 연락하면 되고, 리셉션(서비스)이 방 번호를 배정하며, 각 방(파드)이 실제 고객을 받아들입니다. 고객은 방 번호를 몰라도 되며, 호텔이 내부에서 모두 적절히 안내합니다. 방이 바뀌어도(파드 재시작) 고객은 같은 번호로 연락하면 됩니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- kube-proxy | Service의 ClusterIP로 들어오는 트래픽을 실제 파드로 분산시키는 노드 레벨 네트워크 에이전트
- Endpoints | Service에 의해 관리되는 파드 IP 목록 (Service의 Selector에 의해 자동 업데이트)
- CoreDNS | 쿠버네티스 내부 DNS 서버 (서비스 검색을 담당)
- Ingress Controller | Ingress 리소스를 처리하여 실제 HTTP/HTTPS 라우팅을 수행하는 파드
- Gateway API | Ingress의 차세대 표준 (더 표현력 풍부한 라우팅 규칙 지원)

### 👶 어린이를 위한 3줄 비유 설명
1. Service는 놀이공원의 버스 정류장과 같아요. 버스(파드)가 자주 오고가고 이름을外人(외부)에 알려면 정류장 이름(Service 이름)이 필요해요.
2. Ingress는 놀이공원 입구의 안내소예요. "경쟁구는 오른쪽, 먹거리는 왼쪽" 이렇게 길을 알려주면 원하는 곳에 도착할 수 있어요.
3. 이 두 가지를 함께 쓰면 작은 안내소 하나로 수천 명의 손님을 각각 다른 놀이기구에 효율적으로 보낼 수 있어요!
