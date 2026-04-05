+++
weight = 894
title = "94. 인그레스 (Ingress)"
description = "Ingress: 단일 외부 IP를 통해 URL 경로나 호스트 이름에 따라 여러 Service로 HTTP/HTTPS 트래픽을 분기하는 L7 게이트웨이 라우팅 규칙"
date = 2026-03-26

[taxonomies]
tags = ["kubernetes", "k8s", "ingress", "http-routing", "l7-gateway", "tls-termination"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Ingress는 HTTP/HTTPS 트래픽을"단일 외부 IP"로 수신하여, URL 경로(/api, /web)나 호스트 이름(api.example.com, web.example.com)에 따라 여러 내부 Service로 라우팅하는 L7 게이트웨이이다.
> 2. **가치**: 하나의 LoadBalancer/공인 IP로"여러 웹 애플리케이션"을 호스트별/경로별로 분기할 수 있어 비용을 절감하고, SSL 종료(인증서 관리)와 URL 기반 라우팅을 提供한다.
> 3. **융합**: Ingress Controller(nginx-ingress, traefik, ALB ingress 등)가 Ingress 리소스를 읽어 라우팅 규칙을 동적으로 적용하며, Let's Encrypt와 연동하여 자동 인증서 발급/갱신도 가능하다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

Ingress는 HTTP/HTTPS 웹 트래픽을 쿠버네티스 내부의 여러 Service로 라우팅하는" L7 게이트웨이"이다. 예를 들어, "api.example.com/api"로 요청하면"backend-api Service"로, "api.example.com/web"으로 요청하면"frontend-web Service"로 분기하는 것이 가능하다. 하나의 외부 IP(LoadBalancer)로 복수의 웹 애플리케이션을 운영할 수 있어 비용 효율적이며, SSL 인증서 관리와 URL 기반 라우팅을 한 곳에서 처리한다.

### 왜 Ingress인가?

 LoadBalancer만 사용하면"하나의 Service에 하나의 IP"가 할당되므로, 여러 웹 앱(마이크로서비스 프론트엔드, API 서버, 관리 콘솔 등)을 각각 별도의 IP로 운영해야 한다. 이는 비용 낭비(각 LoadBalancer에 과금)와 관리 복잡성 증가를 초래한다. Ingress를 사용하면"하나의 IP + 하나의 Ingress"로 여러 앱을 호스트/경로 기반으로 분기할 수 있다.

### 비유

Ingress를"대형 쇼핑몰의 안내 데스크"에 비유할 수 있다. 쇼핑몰(클러스터)에는 의류관(A Service), 음식관(B Service), 문화관(C Service)이 있는데, 모든 입구에"안내 데스크"(Ingress)가 있다. 방문객은"food.mall.com"으로 오면 음식관으로, "clothes.mall.com"으로 오면 의류관으로 안내받는다. 방문객은Shopping몰의 대표 주소(단일 IP)만 알면 되고, 내부 상점들(여러 Service)의 위치는 몰라도 된다.

---

## Ⅱ. 아키키텍처 및 핵심 원리 (Deep Dive)

### Ingress 기본 구조

 Ingress 리소스는"라우팅 규칙"을 정의한다. spec.rules에 호스트 이름과 경로 기반 라우팅을指定하고, spec.tls에 SSL 인증서를指定한다. 예를 들어, "example.com/" → serviceA, "example.com/subpath" → serviceB로 라우팅하도록 설정할 수 있다. Ingress Controller가 이 Ingress 리소스를 읽고, 실제 라우팅을 수행한다.

```
[ Ingress 라우팅 예시 ]

┌─────────────────────────────────────────────────────────────────────────┐
│                    Ingress를 통한 URL 기반 라우팅                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  외부 클라이언트                                                        │
│  브라우저: https://shop.example.com/                                    │
│         │                                                               │
│         │ (HTTPS 요청, shop.example.com)                                │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Ingress Controller (nginx-ingress / ALB Ingress 등)            │   │
│  │                                                                  │   │
│  │ Ingress Rules:                                                  │   │
│  │  • host: shop.example.com                                       │   │
│  │    └─ path: /          → nginx-frontend-svc:80                │   │
│  │    └─ path: /api       → backend-api-svc:8080                  │   │
│  │    └─ path: /admin     → admin-console-svc:3000                │   │
│  │                                                                  │   │
│  │  TLS: shop.example.com → TLS 인증서 적용                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                    │                    │                      │
│         │ /                 │ /api               │ /admin               │
│         ▼                    ▼                    ▼                      │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐           │
│  │ frontend    │      │ backend-api  │      │ admin-      │           │
│  │ Service     │      │ Service      │      │ console     │           │
│  │ (nginx)     │      │ (api server) │      │ Service     │           │
│  └─────────────┘      └─────────────┘      └─────────────┘           │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Ingress의 핵심은"URL 기반 분기"이다. shop.example.com/으로 오면"프론트엔드 Service"로, shop.example.com/api로 오면"백엔드 API Service"로 분기한다. 이는 하나의 IP로 여러 웹 앱을 운영할 수 있게 해준다. TLS 설정도 Ingress에서集中管理하여, shop.example.com에 대한 인증서를 한번만 설정하면 된다.

### Ingress Controller 종류

 Ingress를動作시키려면 Ingress Controller가 필요하다. 다양한 Ingress Controller가 존재한다. **nginx-ingress-controller**: 가장 널리 사용되는, nginx 기반 Ingress Controller. **traefik**: Go로 작성된 동적 설정 reload가 가능한 Ingress Controller. **AWS ALB Ingress Controller**: AWS Application Load Balancer를 Ingress로 사용. **GCE Ingress Controller**: Google Cloud의 GKE 기본 Ingress Controller. **Istio Ingress Gateway**: Service Mesh Istio의 ingress 게이트웨이.

### SSL/TLS 종료

 Ingress는 SSL 인증서 관리를 제공한다. spec.tls에 도메인별 인증서를 Secret으로 지정하면, Ingress Controller가 TLS 종료를 수행한다. Let's Encrypt와 연동하면 인증서 자동 발급/갱신도 가능하다. TLS 종료를 Ingress에서 수행하면, 백엔드 Service와 파드는 HTTP(암호화 없음)로 통신하여 성능 오버헤드를 줄일 수 있다.

### 섹션 비유

 Ingress SSL 관리를"호텔 프론트 데스크의 카운터"에 비유할 수 있다. 방문객(클라이언트)이 호텔에 도착하면, 프론트 데스크(ingress)가 카운터에서"귀하의 카드"(TLS 인증서)를 확인하고,問題がなければ 객실(백엔드 Service)로 안내한다. 객실 내부에서는 카드를 다시 확인할 필요가 없듯이, 백엔드 Service는 HTTP로 통신하여 복잡성을 줄인다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### Ingress vs Service (LoadBalancer)

| 비교 항목 | Ingress | Service LoadBalancer |
|:---|:---|:---|
| **라우팅 레벨** | L7 (HTTP/HTTPS) | L4 (TCP/UDP) |
| **라우팅 기준** | URL 경로, 호스트 | IP/포트 |
| **SSL 종료** | 지원 | 불가 (별도 설정 필요) |
| **비용** | 단일 LB + Ingress | 각 Service당 LB |
| **용도** | HTTP/S 웹 앱 | TCP/UDP 서비스 |

### Ingress Class

 복수의 Ingress Controller가共存하는 환경에서는 IngressClass를사용하여 각 Ingress가 어떤 Controller를 사용해야 하는지指定한다. spec.ingressClassName에 IngressClass 이름을 지정하고, IngressClass의 controller 필드에 실제 Controller 이름(예: k8s.io/nginx-ingress-controller)을指定한다.

### 경로 기반 vs 호스트 기반 라우팅

 Ingress는 두 가지 방식의 라우팅을 지원한다. **경로 기반 라우팅**: example.com/app1, example.com/app2처럼同一 호스트에서 URL 경로별로 분기. **호스트 기반 라우팅**: api.example.com, web.example.com처럼 호스트 이름별로 다른 Service로 분기. 두 방식을 함께 사용할 수도 있다.

### 섹션 비유

 IngressClass를"백화점 점원의 전문 분야"에 비유할 수 있다. 한 백화점에 여러 팀(ingress class)의 점원이 있으면, 어느 팀의 고객(ingress)이 들어오면 해당 전문 점원이 응대한다. "의류"](nginx-ingress-controller)를 찾는 고객은 의류팀 점원이，"식당"](traefik)을 찾는 고객은 식당팀 점원이 응대한다. 전문 분야(IngressClass)별로 고객을 분산하여 처리한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### Ingress 기본 설정

 기본 Ingress Manifest는 apiVersion: networking.k8s.io/v1, kind: Ingress, metadata: name, spec: rules, tls로 구성된다. rules에는 호스트 이름, 경로, 백엔드 Service 이름을指定한다.

### rewrite-target 옵션

 경로 기반 라우팅에서 백엔드 Service가"/"를 기대하는 경우, ingress controller의annotation을 사용하여 URL 경로를 변환해야 한다. 예를 들어, /api → backend/api로 요청을 전달할 때, 백엔드가 "/api"를 "/api"가 아닌 "/"(根目)로 기대한다면, rewrite-target을 사용하여 경로를 변환한다.

### rate limiting과 WAF

 Ingress Controller(nginx 등)는注解(annotations)을 통해"_RATE LIMITING"(요청 속도 제한)과"WAF(Web Application Firewall)" 기능을 제공할 수 있다. 이는 외부 공격( DDoS, SQL Injection 등)에 대한 防壁으로 활용된다.

### 섹션 비유

 Ingress rate limiting을"영화관 입구 표 검사원"에 비유할 수 있다. 영화관(ingress)에 한 번에 너무 많은 인원이殺到하면 문제가 발생하므로, 표 검사원(_RATE LIMITING)이 1분당 100명만 입장시킨다. 이를 통해 無謀한 집중 요청(공격)을防止하고, 정상적인 이용객은 Whitney进场할 수 있다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대 효과

 Ingress를利用하면"다수의 웹 애플리케이션을 단일 IP로 효율적으로 운영"할 수 있다. URL 기반/호스트 기반 라우팅으로 마이크로서비스架构を整理하고, SSL/TLS 인증서를集中管理하며, rate limiting과 WAF로 安全도 확보할 수 있다.

### 핵심 정리

 Ingress는 HTTP/HTTPS 트래픽을 URL 경로나 호스트 이름에 따라 여러 Service로 라우팅하는 L7 게이트웨이이다. Ingress Controller가 Ingress 리소스를 읽어 실제 라우팅을 수행하며, SSL 종료, rewrite, rate limiting 등의 기능을 제공한다. 다수의 웹 앱을 단일 IP로 운영할 때 필수적이다.

### 섹션 비유

 Ingress를"국제공항의 도착 게이트 관리 시스템"에 비유할 수 있다.国際空港には 여러 항공사(호스트별 서비스)의航班이 도착하고, 각 항공사마다 다른 터미널(다른 Service의 파드)으로 안내되어야 한다. 도착 게이트 관리 시스템(Ingress)은"어떤 항공사航班"(호스트)이고"어디로 가는지"(경로)를 확인하고, 해당 터미널로乗客을 안내한다. 또한 여권 검사(TLS 종료)를 Gate에서 수행한다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Ingress Controller** | Ingress 리소스를 읽어 HTTP/HTTPS 라우팅을 실제 수행하는 Controller이다. |
| **IngressClass** | Ingress가 사용할 Ingress Controller를 지정하는 리소스이다. |
| **TLS/SSL 종료** | Ingress에서 HTTPS 요청을 복호화하여 백엔드는 HTTP로 통신하는功能이다. |
| **rewrite-target** | URL 경로를 백엔드 Service에 맞게 변환하는 옵션이다. |
| **Rate Limiting** | 요청 속도를 제한하여 DDoS 공격 등을防止하는 기능이다. |
| **LoadBalancer** | Ingress 앞단의 외부 노출을 담당하는 Service 유형이다. |
