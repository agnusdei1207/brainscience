+++
title = "쿠버네티스 (Kubernetes)"
date = 2024-05-18
description = "클라우드 네이티브 아키텍처의 핵심인 쿠버네티스의 선언적 상태 관리, 마스터/워커 노드 컴포넌트 구조, 핵심 리소스 객체 및 선언형 YAML 기반의 운영 메커니즘"
weight = 10
+++

# 쿠버네티스 아키텍처 및 내부 메커니즘 심층 분석 (Kubernetes)

## 1. 쿠버네티스의 본질과 선언적(Declarative) 철학
쿠버네티스(Kubernetes, K8s)는 구글의 내부 오케스트레이션 시스템인 보그(Borg)의 노하우를 바탕으로 오픈소스화된 컨테이너 오케스트레이션 플랫폼입니다. 단순한 컨테이너 배포 도구를 넘어, 수천 대의 서버로 구성된 클러스터 전체를 거대한 하나의 컴퓨터처럼 다루게 해주는 클라우드 네이티브 운영체제라 할 수 있습니다.

쿠버네티스의 가장 핵심적인 설계 철학은 **"선언적 상태 관리(Declarative State Management)"**입니다. 관리자가 명령적(Imperative)으로 "A 컨테이너를 실행하고, B포트를 열어라"라고 지시하는 것이 아니라, "웹 서버 3개가 항상 떠 있고, 이들은 80번 포트로 통신해야 한다"라는 '원하는 상태(Desired State)'를 YAML로 선언합니다. 그러면 쿠버네티스의 다양한 컨트롤러들이 현재 상태(Current State)를 지속적으로 감시하며 원하는 상태와 일치하도록 끊임없이 제어 루프(Control Loop)를 실행합니다.

## 2. 쿠버네티스 클러스터 아키텍처 구성

쿠버네티스 클러스터는 클러스터를 통제하는 **컨트롤 플레인(Control Plane / Master Node)**과 실제 워크로드(애플리케이션)가 구동되는 **워커 노드(Worker Node)**로 물리적/논리적으로 분리됩니다.

```ascii
[ Kubernetes Cluster Architecture ]

+-----------------------------------------------------------+
|                   Control Plane (Master Node)             |
|                                                           |
|  +--------------+   +---------------+   +--------------+  |
|  | Kube-apiserver|---|  etcd (DB)    |   | Scheduler    |  |
|  +--------------+   +---------------+   +--------------+  |
|         |                   |                   |         |
|  +--------------+   +---------------+           |         |
|  | Controller   |---| Cloud Cont.   |           |         |
|  | Manager      |   | Manager       |           |         |
|  +--------------+   +---------------+           |         |
+---------|-------------------|-------------------|---------+
          |                   |                   |
          |               ( Network )             |
          v                   v                   v
+-------------------+ +-------------------+ +-------------------+
|   Worker Node 1   | |   Worker Node 2   | |   Worker Node N   |
| +---------------+ | | +---------------+ | | +---------------+ |
| |    Kubelet    | | | |    Kubelet    | | | |    Kubelet    | |
| +---------------+ | | +---------------+ | | +---------------+ |
| +---------------+ | | +---------------+ | | +---------------+ |
| |  Kube-Proxy   | | | |  Kube-Proxy   | | | |  Kube-Proxy   | |
| +---------------+ | | +---------------+ | | +---------------+ |
| [Pod] [Pod] [Pod] | | [Pod] [Pod] [Pod] | | [Pod] [Pod] [Pod] |
| (Container Runtime) | (Container Runtime) | (Container Runtime) |
+-------------------+ +-------------------+ +-------------------+
```

### 2.1 컨트롤 플레인 (Control Plane) 컴포넌트
- **kube-apiserver**: 쿠버네티스 아키텍처의 프론트엔드이자 중앙 허브. 클러스터 외부의 사용자(kubectl) 및 내부의 모든 컴포넌트들은 오직 API 서버와 REST API를 통해 통신합니다.
- **etcd**: 클러스터의 모든 설정 정보와 리소스의 상태 데이터가 저장되는 고가용성 Key-Value 저장소. 쿠버네티스의 유일한 단일 진실 공급원(Single Source of Truth)입니다.
- **kube-scheduler**: 생성된 파드(Pod)를 구동할 최적의 워커 노드를 결정합니다. 노드의 리소스 가용성, 하드웨어 제약(Taint/Toleration), 어피니티(Affinity) 규칙을 종합적으로 평가하여 스케줄링합니다.
- **kube-controller-manager**: 노드 컨트롤러, 레플리카셋 컨트롤러 등 다양한 백그라운드 스레드를 구동하여 클러스터의 상태를 'Desired State'로 맞추는 핵심 조정자 역할을 합니다.

### 2.2 워커 노드 (Worker Node) 컴포넌트
- **kubelet**: 각 노드에 실행되는 에이전트로, API 서버로부터 지시를 받아 컨테이너 런타임(containerd, CRI-O 등)과 상호작용하며 파드의 생명주기를 관리하고 상태를 API 서버에 보고합니다.
- **kube-proxy**: 노드의 네트워크 규칙(iptables 또는 IPVS)을 관리하여 파드 간 통신과 외부 트래픽을 파드로 라우팅(로드 밸런싱)하는 네트워크 에이전트입니다.
- **Container Runtime**: 컨테이너의 실제 실행을 담당하는 소프트웨어. (Docker는 현재 CRI에서 Deprecated 되었으며 containerd가 주로 쓰임)

## 3. 핵심 리소스 객체 (Core Resource Objects)
- **Pod (파드)**: 쿠버네티스의 가장 작은 배포 단위. 하나 이상의 밀접하게 결합된 컨테이너의 그룹으로, IP와 스토리지를 공유합니다. (단일 컨테이너 = 단일 파드가 일반적)
- **ReplicaSet (레플리카셋)**: 명시된 동일한 파드의 복제본(Replica) 개수가 항상 실행되도록 보장하여 고가용성을 제공합니다.
- **Deployment (디플로이먼트)**: 레플리카셋의 상위 개념으로, 무중단 롤링 업데이트(Rolling Update), 롤백(Rollback) 등 애플리케이션의 배포 생명주기를 관리합니다. (가장 많이 사용됨)
- **Service (서비스)**: 동적으로 생성/삭제되며 IP가 변하는 파드들에게 고정된 단일 진입점(Virtual IP)과 도메인 네임(DNS)을 제공하고 로드밸런싱을 수행합니다. (ClusterIP, NodePort, LoadBalancer 타입)
- **Ingress (인그레스)**: 외부 HTTP/HTTPS 트래픽을 클러스터 내부의 서비스로 라우팅하는 L7 로드밸런서 및 API 게이트웨이 역할을 합니다.

## 4. 선언적 인프라 배포 코드 (Production YAML Example)
웹 애플리케이션을 고가용성(3중화)으로 배포하고, 내부 로드밸런싱을 구성하는 프로덕션 레벨의 YAML 예제입니다.

```yaml
---
# 1. Deployment: 애플리케이션 배포 및 복제본 관리
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: webserver
spec:
  replicas: 3 # 항상 3개의 파드 복제본 유지 (원하는 상태 선언)
  selector:
    matchLabels:
      app: webserver # 이 라벨을 가진 파드를 관리 대상으로 지정
  strategy:
    type: RollingUpdate # 무중단 배포 전략
    rollingUpdate:
      maxUnavailable: 1 # 업데이트 중 최대 중단 허용 수
      maxSurge: 1       # 업데이트 중 최대 초과 생성 허용 수
  template: # 생성할 파드의 템플릿
    metadata:
      labels:
        app: webserver
    spec:
      containers:
      - name: nginx-container
        image: nginx:1.24.0-alpine
        ports:
        - containerPort: 80
        resources: # 리소스 할당량 제어 (OOM 방지)
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "250m"
            memory: "256Mi"
        livenessProbe: # 헬스 체크 (실패 시 파드 재시작)
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 10

---
# 2. Service: 네트워크 엔드포인트 노출 (로드밸런서)
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: ClusterIP # 클러스터 내부 전용 IP 할당
  selector:
    app: webserver # 동일한 라벨의 파드들로 트래픽 분산
  ports:
    - protocol: TCP
      port: 80        # 서비스(Virtual IP)가 수신할 포트
      targetPort: 80  # 파드가 수신 중인 실제 포트
```

## 5. 결론 및 실무적 통찰
마이크로서비스 아키텍처(MSA)를 도입한 현대 IT 환경에서 쿠버네티스는 단순한 인프라가 아니라 애플리케이션을 정의하는 플랫폼 그 자체가 되었습니다. 데브옵스(DevOps) 엔지니어나 아키텍트는 쿠버네티스의 컴포넌트 간 비동기적 통신 방식과 제어 루프 패턴을 이해해야 하며, Helm이나 Kustomize와 같은 패키지 매니저, ArgoCD/Flux를 통한 GitOps 기반의 배포 파이프라인(CI/CD)을 구축할 수 있는 역량을 갖추어야 합니다.
