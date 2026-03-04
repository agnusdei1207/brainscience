+++
title = "쿠버네티스 (Kubernetes)"
date = 2024-05-18
description = "클라우드 네이티브 아키텍처의 핵심인 쿠버네티스의 선언적 상태 관리, 마스터/워커 노드 컴포넌트 구조, 핵심 리소스 객체 및 선언형 YAML 기반의 운영 메커니즘"
weight = 10
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Kubernetes", "K8s", "Cloud Native", "Orchestration", "Docker", "Container"]
+++

# 쿠버네티스 아키텍처 및 내부 메커니즘 심층 분석 (Kubernetes)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 분산된 컴퓨팅 자원을 하나의 거대한 리소스 풀로 추상화하여, 컨테이너화된 애플리케이션의 배포, 확장 및 관리를 자동화하는 '클라우드 운영체제'급 오픈소스 오케스트레이션 플랫폼입니다.
> 2. **가치**: **선언적 상태 관리(Declarative State Management)**와 제어 루프(Control Loop)를 통해 인프라 운영의 복잡성을 제거하며, 셀프 힐링(Self-healing) 및 무중단 배포를 실현하여 비즈니스 민첩성을 극대화합니다.
> 3. **융합**: 마이크로서비스 아키텍처(MSA), 서비스 메시(Service Mesh), GitOps 배포 모델과 융합되어 현대적 소프트웨어 공급망의 표준 인프라로 자리매김하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

쿠버네티스(Kubernetes, K8s)는 구글이 15년 이상 운영해 온 내부 컨테이너 관리 시스템인 '보그(Borg)'의 기술적 정수를 결합하여 오픈소스화한 프로젝트입니다. 단순히 컨테이너를 실행하는 도구를 넘어, 수천 대의 서버로 구성된 클러스터 전체를 지능적으로 제어하고 애플리케이션의 생명주기를 완벽하게 관리하는 통합 플랫폼입니다.

**💡 비유**: 쿠버네티스는 거대한 선단의 **'자율주행 함대 사령관'**과 같습니다. 사령관(Master)에게 "항상 5척의 보급선(Pod)이 특정 간격을 유지하며 항해해야 한다"라고 명령(YAML 선언)만 내리면, 폭풍우가 몰아쳐 배 한 척이 침몰하더라도 사령관은 즉시 새로운 배를 띄워 원래의 5척 상태를 복구해냅니다.

**등장 배경 및 발전 과정**:
1. **모놀리식의 한계와 컨테이너의 부상**: 서비스 규모가 커지며 거대한 단일 애플리케이션(Monolith)은 수정과 배포가 불가능한 수준에 이르렀고, 이를 해결하기 위해 프로세스를 격리하여 배포하는 도커(Docker) 컨테이너 기술이 각광받기 시작했습니다.
2. **컨테이너 정글(Container Jungle)**: 컨테이너 수가 수백, 수천 개로 늘어나자 어떤 컨테이너가 어디서 실행되는지, 장애가 난 컨테이너를 어떻게 살릴지, 트래픽을 어떻게 분산할지에 대한 관리의 임계점에 도달했습니다.
3. **오케스트레이션의 표준화**: 아파치 메소스(Mesos), 도커 스웜(Swarm) 등 여러 경쟁자가 있었으나, 쿠버네티스는 강력한 확장성(CRD), 구글의 운영 노하우, 그리고 거대한 생태계(CNCF)를 바탕으로 컨테이너 오케스트레이션의 사실상 표준(De facto standard)이 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: 마스터(Control Plane)와 워커 노드 아키텍처

| 컴포넌트 명칭 | 상세 역할 및 내부 동작 메커니즘 | 관련 기술/프로토콜 | 비유 |
|---|---|---|---|
| **kube-apiserver** | 모든 통신의 중앙 허브. REST API를 통해 클러스터 상태를 조회/변경 | REST, JSON/YAML | 창구 직원 |
| **etcd** | 클러스터의 모든 상태를 저장하는 분산 Key-Value DB. Raft 알고리즘 기반 고가용성 보장 | Raft Consensus | 장부(원장) |
| **kube-scheduler** | 파드(Pod)를 구동할 최적의 노드를 리소스 가용성, 정책 등에 따라 결정 | Scheduling Algo | 배정 팀장 |
| **Controller Manager** | 클러스터의 상태를 '원하는 상태'로 유지하는 제어 루프 실행 (Node, Replica 등) | Control Loop | 감시관 |
| **kubelet** | 워커 노드마다 실행되는 에이전트. 파드 내 컨테이너의 실행 상태 관리 및 보고 | CRI (Container Runtime) | 현장 작업반장 |
| **kube-proxy** | 노드별 네트워크 규칙 관리 및 서비스(Service) 추상화를 통한 로드밸런싱 구현 | iptables, IPVS | 안내원 |

### 정교한 구조 다이어그램: 제어 평면과 데이터 평면의 분리

```ascii
[ Control Plane (Master Node) ]                                [ External User / CI/CD ]
+-----------------------------------------------------------+               |
|   +--------------+      +----------------+                |               | kubectl apply -f
|   | API Server   | <--- |   etcd (DB)    |                | <-------------+
|   +-------+------+      +-------+--------+                |
|           |                     |                         |
|   +-------v------+      +-------v--------+                |
|   | Scheduler    |      | Controller Mgr |                |
|   +--------------+      +----------------+                |
+-----------+---------------------+-------------------------+
            |                     |
      (GRPC / TLS)          (Heartbeats)
            |                     |
+-----------v---------------------v-------------------------+
| [ Worker Node 1 ]              [ Worker Node 2 ]          |
| +--------------+               +--------------+           |
| |   Kubelet    |               |   Kubelet    |           |
| +------+-------+               +------+-------+           |
|        | (CRI)                        |                   |
| +------v-------+               +------v-------+           |
| | Container R. |               | Container R. |           |
| | [Pod] [Pod]  |               | [Pod] [Pod]  |           |
| +--------------+               +--------------+           |
| +--------------+               +--------------+           |
| |  Kube-Proxy  |               |  Kube-Proxy  |           |
| +--------------+               +--------------+           |
+-----------------------------------------------------------+
```

### 심층 동작 원리 (파드 배포 사이클: 0 -> 1)
관리자가 `kubectl apply -f deployment.yaml` 명령을 내리면 내부에서는 다음과 같은 정밀한 연쇄 반응이 일어납니다.

1. **API 수신 및 인증**: API Server가 요청을 수신하고 인증(Authentication) 및 인가(Authorization)를 거쳐 etcd에 Deployment 객체를 기록합니다.
2. **Deployment Controller 개입**: Controller Manager 내부의 Deployment Controller가 etcd의 변화를 감지하고, 지정된 개수(Replicas)만큼의 ReplicaSet을 생성합니다.
3. **ReplicaSet Controller 개입**: ReplicaSet Controller는 실제로 생성되어야 할 파드(Pod) 객체가 부족함을 인지하고, 파드 객체들을 생성하여 etcd에 미할당 상태로 저장합니다.
4. **스케줄링(Scheduling)**: Scheduler는 노드가 할당되지 않은 파드를 발견하고, 워커 노드들의 자원 상황을 필터링/스코어링하여 최적의 노드를 선택한 뒤 API Server를 통해 파드 정보에 노드 이름을 업데이트합니다.
5. **Kubelet 실행**: 해당 워커 노드의 Kubelet은 자신에게 할당된 파드를 인지하고, 컨테이너 런타임(CRI)에게 컨테이너 이미지 인출 및 실행을 명령합니다.
6. **네트워크 설정**: CNI(Container Network Interface) 플러그인이 파드에 가상 IP를 할당하고 네트워크 네임스페이스를 설정하여 통신 준비를 마칩니다.

### 핵심 코드: 프로덕션급 Deployment 및 Service 구성 (YAML)
리소스 제한(Limits)과 헬스 체크(Liveness/Readiness Probe)가 포함된 실무 수준의 매니페스트입니다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: brainscience-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: brainscience
  template:
    metadata:
      labels:
        app: brainscience
    spec:
      containers:
      - name: api-container
        image: brainscience/api:v1.2.0
        ports:
        - containerPort: 8080
        # 리소스 관리: OOM(Out Of Memory) 및 CPU Throttling 방지
        resources:
          requests:
            cpu: "250m"
            memory: "512Mi"
          limits:
            cpu: "500m"
            memory: "1Gi"
        # 헬스 체크: 자가 치유(Self-healing)의 근간
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  type: ClusterIP
  selector:
    app: brainscience
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Kubernetes vs Docker Swarm
두 플랫폼 모두 컨테이너 오케스트레이션을 제공하지만 철학적 차이가 뚜렷합니다.

| 비교 관점 | Kubernetes (K8s) | Docker Swarm | 상세 분석 |
|---|---|---|---|
| **설계 철학** | 확장성(Extensibility)과 세밀한 제어 중점 | 단순함(Simplicity)과 사용자 친화성 중점 | K8s는 배우기 어렵지만 복잡한 엔터프라이즈 환경에 적합함. |
| **리소스 단위** | Pod (하나 이상의 컨테이너 그룹) | Service (단일 컨테이너 이미지 기준) | K8s의 Pod 구조는 사이드카(Sidecar) 패턴 구현에 매우 유리함. |
| **고가용성 기법** | etcd 기반 분기 합의(Raft) 및 다중 컨트롤러 | 내장된 Raft 합의 엔진 사용 | K8s는 컴포넌트가 분리되어 있어 대규모 클러스터(5000노드 이상) 확장에 유리함. |
| **네트워크 모델** | CNI 기반 플러그인 방식 (Calico, Cilium 등) | 내장된 Overlay Network (VXLAN) | K8s는 네트워크 정책(NetworkPolicy)을 통해 미세한 방화벽 제어가 가능함. |

### 과목 융합 관점 분석 (운영체제 및 보안 연계)
- **운영체제(OS)와의 융합**: 쿠버네티스는 Linux 커널의 **Namespaces**(격리)와 **Cgroups**(자원 제한) 기능을 고도로 추상화하여 사용합니다. 파드는 네트워크 네임스페이스를 공유하여 로컬 호스트 통신을 수행하고, Cgroups를 통해 특정 컨테이너가 노드 전체의 CPU를 점유하는 '노이지 네이버(Noisy Neighbor)' 문제를 차단합니다.
- **보안(Security)과의 융합**: 제로 트러스트(Zero Trust) 관점에서 쿠버네티스는 **RBAC(Role-Based Access Control)**을 통해 API 접근을 제한하고, **Pod Security Admission**을 통해 특권(Privileged) 컨테이너 실행을 방지합니다. 또한 서비스 메시(Istio 등)와 결합하여 파드 간 통신을 상호 TLS(mTLS)로 자동 암호화합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 트래픽 폭증 시의 Auto-scaling 전략
**문제 상황**: 이커머스 서비스의 타임 세일 이벤트로 인해 평소 대비 100배 이상의 트래픽이 유입될 것으로 예상됩니다. 시스템은 성능 저하 없이 유연하게 대응해야 합니다.

**기술사의 전략적 의사결정**:
1. **HPA (Horizontal Pod Autoscaler) 설정**: CPU/Memory 사용량뿐만 아니라, Prometheus 커스텀 메트릭(예: 초당 요청 수)을 기반으로 파드 개수를 수초 내에 수백 개로 자동 확장합니다.
2. **CA (Cluster Autoscaler) 연계**: 워커 노드들의 자원이 부족해지면 클라우드 제공자(AWS/GCP)의 API를 호출하여 새로운 가상 머신(EC2 등)을 클러스터에 즉시 추가합니다.
3. **Graceful Shutdown 보장**: 파드가 급격히 줄어들 때 처리 중인 트래픽이 유실되지 않도록 `preStop` 훅을 설정하여 커넥션 드레이닝(Connection Draining)을 수행합니다.

### 도입 시 고려사항 및 안티패턴 (Anti-patterns)
- **안티패턴 - Resource Limit 미설정**: 리소스 제한이 없는 파드는 무한정 자원을 소비하여 동일 노드의 다른 핵심 파드를 죽게 만듭니다. 모든 파드에는 반드시 `requests`와 `limits`를 명시해야 합니다.
- **체크리스트**: 
  - 상태값 저장(Stateful) 애플리케이션에 대한 Persistent Volume 전략 수립 여부.
  - 마스터 노드(Control Plane)의 3중화 및 etcd 백업 주기 설정.
  - Image Scanning을 통한 취약점 컨테이너 배포 차단 체계 구축.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과
- **운영 효율 향상**: 수동 배포 및 복구 작업이 자동화되어 운영 인건비가 50% 이상 절감됩니다.
- **인프라 이용률 최적화**: 빈 패킹(Bin-packing) 알고리즘을 통해 서버 자원을 촘촘하게 사용함으로써 클라우드 비용을 20~30% 절감할 수 있습니다.

### 미래 전망 및 진화 방향
- **Serverless Kubernetes**: 사용자가 노드 관리를 전혀 신경 쓰지 않는 AWS Fargate와 같은 서버리스 모델이 대중화되고 있습니다.
- **Edge Computing 연계**: K3s와 같이 경량화된 쿠버네티스를 통해 엣지 디바이스나 IoT 기기까지 오케스트레이션 영역이 확장되고 있습니다.

### ※ 참고 표준/가이드
- **CNCF (Cloud Native Computing Foundation)**: 쿠버네티스 표준 및 생태계 프로젝트 관리 기관.
- **CRI / CNI / CSI**: 컨테이너 런타임, 네트워크, 스토리지 인터페이스의 업계 표준 규격.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [도커 (Docker)](@/studynotes/13_cloud_architecture/_index.md) : 쿠버네티스가 관리하는 가장 기본적인 컨테이너 기술.
- [서비스 메시 (Istio)](@/studynotes/13_cloud_architecture/_index.md) : 쿠버네티스 위에서 마이크로서비스 간의 통신과 보안을 제어하는 상위 레이어.
- [Helm 패키지 매니저](@/studynotes/13_cloud_architecture/_index.md) : 복잡한 쿠버네티스 리소스를 템플릿화하여 쉽게 관리하는 도구.
- [관측 가능성 (Observability)](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md) : 수많은 파드의 로그와 메트릭을 수집하여 가시성을 확보하는 필수 기술.
- [CI/CD (ArgoCD)](@/studynotes/15_devops_sre/_index.md) : Git을 소스로 삼아 쿠버네티스 클러스터의 상태를 동기화하는 배포 자동화 모델.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 쿠버네티스는 수많은 로봇(컨테이너)을 지휘하는 **'로봇 부대 사령관'**이에요.
2. "청소 로봇 3대, 요리 로봇 2대를 항상 유지해!"라고 적힌 편지를 사령관에게 주면, 로봇이 고장 나도 사령관이 알아서 새 로봇으로 교체해줘요.
3. 덕분에 사람이 일일이 로봇을 고치러 가지 않아도, 로봇 부대는 언제나 완벽하게 일을 해낸답니다.