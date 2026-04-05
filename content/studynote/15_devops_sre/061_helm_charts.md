+++
weight = 61
title = "61. Helm/Charts (헬름/차트)"
date = "2026-04-05"
[extra]
categories = "studynote-devops-sre"
+++

# Helm/Charts (헬름/차트)

> ⚠️ 이 문서는 쿠버네티스용 패키지 매니저인 Helm과 그 패키지 포맷인 Chart의 철학적 배경, 아키텍처, 템플릿 엔진으로서의 역할, 그리고 실무에서 Helm을 활용하여 복잡한 쿠버네티스 애플리케이션을 관리하는 방법에 대한 체계적 분석입니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Helm은 쿠버네네티스의 패키지 매니저로, 복잡한 쿠버네티스 매니페스트(YAML)들을 하나의 Chart로 패키징하고, values.yaml을 통해 환경별(개발, 스테이징, 프로덕션)로 설정을 파라미터화하여 동일한 Chart로 다양한 환경을-deploy할 수 있게 합니다.
> 2. **가치**: Helm이 없으면 개발팀은 수십 개의 YAML 파일(Deployment, Service, ConfigMap, Secret, Ingress 등)을 각각 환경에 맞게 복사/수정하여管理해야 하지만, Helm은 이 과정을 "차트 설치(install)"라는单一操作으로 추상화합니다.
> 3. **현대화**: Helm v3의 Release Manager 도입으로 Cluster 내부에 Release 정보를 저장하고,_chartmuseum_, _harbor_ 등의 Artifact 저장소와 연동하여 차트의 버전 관리, 검색, 공유가 가능합니다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 1. 쿠버네티스 매니페스트의 복잡성
쿠버네티스에서 하나의 애플리케이션을 배포하려면 通常 수십 개의 YAML 파일이 필요합니다.
- Deployment (컨테이너 실행 설정)
- Service (네트워킹 설정)
- ConfigMap (설정 분리)
- Secret (기밀 정보 관리)
- Ingress (HTTP 라우팅)
- HorizontalPodAutoscaler (오토스케일링)
- PodDisruptionBudget (Pod 중단 방지)
- ServiceAccount (RBAC)

### 2. 환경별 매니페스트 관리의 문제

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│              [ Helm 없는 환경별 매니페스트 관리의 문제 ]                           │
│                                                                              │
│  development/                                                             │
│  ├── deployment.yaml  (image: myapp:dev-123)                              │
│  ├── service.yaml                                                         │
│  └── configmap.yaml    (DB_HOST: localhost)                                │
│                                                                              │
│  staging/                                                                  │
│  ├── deployment.yaml  (image: myapp:staging-456)  ← 복사 & 수정             │
│  ├── service.yaml                                                         │
│  └── configmap.yaml    (DB_HOST: staging-db.local) ← 복사 & 수정            │
│                                                                              │
│  production/                                                               │
│  ├── deployment.yaml  (image: myapp:v1.2.3)       ← 복사 & 수정             │
│  ├── service.yaml                                                         │
│  └── configmap.yaml    (DB_HOST: prod-db.example.com) ← 복사 & 수정        │
│                                                                              │
│  문제: 3배의 파일, 복사/수정 과정에서発生する 실수와 비同步 문제                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3. Helm의 탄생: 매니페스트 관리의 혁신

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│              [ Helm의 발상: "apt-get for Kubernetes" ]                          │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    myapp/ (Helm Chart)                                  │   │
│  │   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐      │   │
│  │   │ Chart.yaml     │  │ values.yaml    │  │ templates/     │      │   │
│  │   │ (차트 메타데이터) │  │ (기본 설정값)   │  │ (YAML 템플릿) │      │   │
│  │   └────────────────┘  └────────────────┘  └────────────────┘      │   │
│  │           │                   │                  │                     │   │
│  │           │                   │                  ▼                     │   │
│  │           │                   │        ┌────────────────┐            │   │
│  │           │                   │        │ _helpers.tpl   │            │   │
│  │           │                   │        │ deployment.yaml │            │   │
│  │           │                   │        │ service.yaml    │            │   │
│  │           │                   │        │ configmap.yaml │            │   │
│  │           │                   │        │ ingress.yaml   │            │   │
│  │           │                   │        └────────────────┘            │   │
│  │           │                   │                                     │   │
│  │           └──────────┬────────┘                                     │   │
│  │                      ▼                                                │   │
│  │   ┌──────────────────────────────────────────────────────────┐       │   │
│  │   │              Template Engine (Go template)                 │       │   │
│  │   │                                                           │       │   │
│  │   │  values.yaml + templates/*.yaml → Kubernetes Manifests   │       │   │
│  │   │                                                           │       │   │
│  │   └──────────────────────────────────────────────────────────┘       │   │
│  │                                                                     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  [ 차트 설치 예시 ]                                                           │
│                                                                              │
│  helm install myapp ./myapp --set image.tag=v1.2.3 \                       │
│                          --set db.host=prod-db.example.com                  │
│                                                                              │
│  helm install myapp ./myapp -f values.prod.yaml   # 프로덕션용               │
│  helm install myapp ./myapp -f values.staging.yaml # 스테이징용             │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Helm은 "ІКЕА 빌딩 키트"와 같습니다. ІКЕА 가구(쿠버네티스 애플리케이션)를 직접 木工istry에서 하나하나 만들면(매니페스트 직접 작성), 모든 부품(Deployment, Service 등)을 分别 구매하고, 크기를 맞추고, 조립하는데 엄청난 時間과 노력이 듭니다. 하지만 ІКЕА 빌딩 키트( Helm Chart)를 사면, 동일한 설명서(テンプレート)를 보고自助的に 조립할 수 있고, 필요에 따라大小(환경별 설정)만 조절하면 됩니다. 또한 조립 설명서는常に最新版本으로 업데이트되므로,木工istry에서直接 만들 때 발생할 수 있는 版本 차이(구성 편류)를防止할 수 있습니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 (Architecture & Mechanism)

### 1. Helm v3 아키텍처

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                         [ Helm v3 아키텍처 ]                                   │
│                                                                              │
│                         ┌─────────────────────┐                                │
│                         │      Helm Client    │                                │
│                         │   (CLI - Local)    │                                │
│                         └──────────┬──────────┘                                │
│                                    │                                           │
│  ┌─────────────────────────────────┼─────────────────────────────────────┐   │
│  │                                 │                                     │   │
│  │   helm install                 │  helm upgrade                       │   │
│  │   helm uninstall               │  helm rollback                      │   │
│  │   helm list                    │  helm history                        │   │
│  │                                 │                                     │   │
│  └─────────────────────────────────┼─────────────────────────────────────┘   │
│                                    │                                           │
│                                    ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      Kubernetes Cluster                                 │   │
│  │                                                                       │   │
│  │   ┌──────────────────────────────────────────────────────────────┐   │   │
│  │   │                   Helm Release Information                     │   │   │
│  │   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │   │   │
│  │   │   │ Release:    │  │ Release:    │  │ Release:    │        │   │   │
│  │   │   │ myapp v1    │  │ myapp v2    │  │ myapp v3    │        │   │   │
│  │   │   │ Status:      │  │ Status:      │  │ Status:      │        │   │   │
│  │   │   │ deployed    │  │ superseded  │  │ deployed     │        │   │   │
│  │   │   └─────────────┘  └─────────────┘  └─────────────┘        │   │   │
│  │   └──────────────────────────────────────────────────────────────┘   │   │
│  │                                                                       │   │
│  │   ┌──────────────────────────────────────────────────────────────┐   │   │
│  │   │                    Installed Resources                        │   │   │
│  │   │   Deployment │ Service │ ConfigMap │ Secret │ Ingress ...     │   │   │
│  │   └──────────────────────────────────────────────────────────────┘   │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Helm v3의 가장 큰 변화는 Tiller(서버 사이드组件)가 제거されたことです. 이제 Helm Client가 直接 Kubernetes API와通信하여 Release 정보를 ConfigMap에 저장합니다. Release는 버전을 가지고 있으며, `helm history`로 모든 버전을 확인하고 `helm rollback`로 이전 버전으로 되돌릴 수 있습니다. 각 Release는 해당 버전에서 生成된 Kubernetes 리소스들(Deployment, Service 등)과 연결됩니다.

### 2. Helm Chart 구조 상세

```text
mychart/                              # Chart 디렉터리
├── Chart.yaml                         # 차트 메타데이터 (이름, 버전, 의존성)
├── values.yaml                        # 기본 설정값 (템플릿에서 참조)
├── charts/                            # 의존 차트들 (서브 차트)
│   └── dependency-chart-1.0.0.tgz
├── templates/                         # Kubernetes 매니페스트 템플릿
│   ├── _helpers.tpl                  # 재사용 가능한 템플릿 함수
│   ├── deployment.yaml               # Deployment 템플릿
│   ├── service.yaml                  # Service 템플릿
│   ├── configmap.yaml                # ConfigMap 템플릿
│   ├── ingress.yaml                  # Ingress 템플릿
│   └── tests/                        # 테스트 템플릿
│       └── test-connection.yaml
└── README.md                         # 차트 사용 문서
```

### 3. Chart.yaml 및 values.yaml 예시

```yaml
# Chart.yaml
apiVersion: v2
name: mywebapp
description: A Helm chart for My Web Application
type: application
version: 1.2.3
appVersion: "2.0.0"
keywords:
  - webapp
  - http
dependencies:                      # 서브 차트 (의존성)
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com"
    condition: postgresql.enabled

---
# values.yaml (기본 설정)
replicaCount: 1

image:
  repository: myorg/mywebapp
  pullPolicy: IfNotPresent
  tag: "1.0.0"

service:
  type: ClusterIP
  port: 8080

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 50m
    memory: 64Mi

autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

postgresql:
  enabled: true
  auth:
    database: myappdb
    username: myappuser
```

### 4. 템플릿 예시

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mywebapp.fullname" . }}
  labels:
    {{- include "mywebapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "mywebapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "mywebapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
          readinessProbe:
            httpGet:
              path: /ready
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### Helm vs Kustomize vs plain YAML 비교

| 구분 | Helm | Kustomize | Plain YAML |
|:---|:---|:---|:---|
| **접근 방식** | 템플릿 방식 (values + templates) | 오버레이 방식 (base + patches) | 직접 작성 |
| **학습 곡선** | 중간 (Go template 문법) | 낮음 (YAML만) | 없음 |
| **복잡성** | 높은 표현력, 유연함 | 단순한 차이점 관리 | 관리 곤란 |
| **재사용성** | Chart repository로 공유 | Kustomization 공유 | 직접 복사/붙여넣기 |
| **디버깅** | `helm template`으로 렌더링 결과 확인 | `kustomize build`로 확인 | 직접 확인 |
| **의존성 관리** | Chart dependencies | 직접 관리 | 직접 관리 |
| **적합 상황** | 복잡한 설정, 외부 Chart 활용 | 환경별 단순 차이 | 가장 간단한 경우 |

### Helm Chart Repository 비교

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ 주요 Helm Chart Repository ]                              │
│                                                                              │
│  Artifact Hub (artifacthub.io)                                                │
│  ──────────────────────────────────────────                                  │
│  • CNCF 산하 공식 Chart 검색 플랫폼                                             │
│  • 수천 개의 공개 Chart 호스팅                                                  │
│  • Bitnami, Prometheus, Grafana, Ingress-NGINX 등                             │
│                                                                              │
│  Jetstack (charts.jetstack.io)                                                │
│  ──────────────────────────────────────────                                  │
│  • cert-manager, k8s-spot-certificate-webhook 등                              │
│                                                                              │
│  HashiCorp (helm.releases.hashicorp.com)                                       │
│  ──────────────────────────────────────────                                  │
│  • Vault, Consul, Nomad, Terraform 등 HashiCorp 제품군                          │
│                                                                              │
│  Dapr (helm.dapr.io)                                                          │
│  ──────────────────────────────────────────                                  │
│  • Dapr SDK, Operator, Dashboard 등                                           │
│                                                                              │
│  자사 Chart Repository (ChartMuseum, Harbor)                                   │
│  ──────────────────────────────────────────                                  │
│  • 사내 Chart 저장 및 배포                                                     │
│  • 인증, 접근 제어, 감사 로그                                                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Helm과 Kustomize의 관계는 "프렌치 프라이 레시피"와 같습니다. Helm은 "기본 프라이 레시피( values.yaml )에 버터 종류(파라미터)만 바꾸면 버터 프라이, 올리브오일 프라이 등 다양한 변형 음식을 만들 수 있는万能 레시피"와 같습니다. Kustomize는 "기본 프라이 위에 뿌릴 파마산 치즈(오버레이)를 레시피북에 남기고, 다른 요리사도 그 파일을 가져다 쓰면 자동으로 같은 레시피가再現되는" 방식입니다. Plain YAML은 "레시피북 없이 모든 요리를 직접 만들어 메모장에 적어두는" 방식입니다. 음식(배포)의 규모와 재사용 필요성에 따라 적절한 방식을 선택해야 합니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

### Helm Chart 개발 시 Best Practices

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Helm Chart 개발 7대 Best Practices ]                       │
│                                                                              │
│  1. SemVer2準拠版本 관리                                                      │
│     → Chart.yaml의 version은 SemVer準拠으로 관리                               │
│     → appVersion과 별개로 관리                                                │
│                                                                              │
│  2. _helpers.tpl 적극 활용                                                    │
│     → 공통 라벨, 이름 정의를 helpers에 캡슐화                                   │
│     → 유지보수성 극대화                                                      │
│                                                                              │
│  3. 기본값은保守적으로 설정                                                    │
│     → 프로덕션에서 문제가 발생하지 않는 기본값                                   │
│     → 사용자가 명시적으로 덮어쓰지 않으면安全的默认值                           │
│                                                                              │
│  4. 리소스 limits 설정 필수                                                    │
│     →_limits.cpu, limits.memory 설정으로 무제한 자원 사용 방지                  │
│                                                                              │
│  5. Liveness/Readiness Probe 필수                                             │
│     → 애플리케이션 상태 확인용 Probe 설정                                       │
│                                                                              │
│  6. 인그레스와 TLS 설정                                                        │
│     → HTTPS 강제 리다이렉트, TLS 설정 기본값으로 포함                           │
│                                                                              │
│  7. 차트 내 테스트 포함                                                        │
│     → templates/tests/ 디렉터리에 연결 테스트 포함                               │
│     → helm test로 테스트 자동 실행                                            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Helm vs Kustomize 선택 가이드

| 상황 | 권장 도구 | 이유 |
|:---|:---|:---|
| **외부 Chart 활용 (Postgres, Redis 등)** | Helm | Bitnami Chart등 활용으로 간편 배포 |
| **단순 환경별 차이점** | Kustomize | base + overlay 방식으로 이해하기 쉬움 |
| **복잡한 파라미터 조합** | Helm | Go template의 표현력이 유연함 |
| **GitOps 환경 (ArgoCD)** | 둘 다 가능 | ArgoCD가 둘 다 지원 |
| **최소한의 종속성** | Kustomize | 추가 도구 설치 불필요 |

- **📢 섹션 요약 비유**: Helm Chart 개발은 "레고 블록 세트 디자인"과 같습니다. 레고 블록 자체(쿠버네티스 리소스)를 하나씩 设计하면管理하기 어렵지만, 레고 키트(Chart)를 만들면 필요한 블록(templates)을 미리 조합해 두고, 조립 설명서(values.yaml)만 바꾸면 다양한 형태(환경별 배포)의 완성품을 만들 수 있습니다. 중요한 것은 조립 설명서가 명확하고(기본값 安全), 테스트가 포함되어 있어야( helm test ) 구매자(사용자)가 직접 완성품(배포)을 검증할 수 있다는 점입니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

### 1. Helm에서 CdK8s로: 프로그래밍 가능한 매니페스트
TypeScript, Python, Java 등 프로그래밍 언어로 쿠버네티스 매니페스트를 생성하는 CDK8s(Cloud Development Kit for Kubernetes)가 Helm의 대안으로 부상하고 있습니다. 타입 시스템과 IDE 자동완성을活用하여 매니페스트의 오류를 사전에 탐지할 수 있다는 장점이 있습니다.

### 2. OCI 기반 Chart Registry
Helm v3는 OCI(Open Container Initiative) 아키텍처를 지원하여, 기존 Docker 이미지 저장소(예: GitHub Container Registry)에 Chart를 저장할 수 있게 되었습니다. 이를 통해 이미지管理和 Chart 관리를统一的 Registry에서 수행할 수 있게 됩니다.

### 3. Helmfile의 확산: 다중 Chart 관리
Helmfile은 여러 Helm Chart_release을 하나의 YAML 파일로 정의하고, 해당 파일을 基幹として 一括でインストール/업그레이드할 수 있게 합니다. 이는microservices 환경에서 복수의 Chart를 管理해야 하는 복잡성을 해결합니다.

- **📢 섹션 요약 비유**: Helm의 미래는 "스마트팩토리 робот программирование"과 같습니다. 현재의 Helm은 命令을 내리면( helm install ) 로봇이指示된内容(쿠버네티스 리소스)을 만들어주지만, робот에게 내리는 명령 자체(Go template)는呃漫하고mistake가 발생하기 쉽습니다. 미래의 CdK8s는 "롭봇이 이해하는 프로그래밍 언어(TypeScript 등)"로 명령을 내리는 것으로,IDE의 도움으로 잘못된 명령(잘못된 매니페스트)을事前に排除할 수 있습니다. OCI 지원은 "로봇의 부품(이미지)과 조립 설명서(Chart)를 같은 창고에保管できる" 효율적인 관리를 가능케 합니다.

---

## 🧠 지식 맵 (Knowledge Graph)

*   **Helm 핵심 개념**
    *   Chart (쿠버네티스 패키지 포맷)
    *   Values (파라미터 값)
    *   Templates (Go template 기반 YAML 생성)
    *   Release (설치된 Chart 인스턴스)
*   **Helm vs Kustomize**
    *   Helm: 템플릿 방식 (값 + 템플릿)
    *   Kustomize: 오버레이 방식 (base + patches)
*   **주요 명령어**
    *   helm install, upgrade, uninstall
    *   helm list, history, rollback
    *   helm template (로컬 렌더링)

---

### 👶 어린이를 위한 3줄 비유 설명
1. Helm은 레고 키트와 같아요. 레고 블록(쿠버네티스 설정)을 미리 조립해둔 상태로 판매돼요.
2. 조립 설명서(values.yaml)를 바꾸면 다른 모양(다른 환경)의 레고를 만들 수 있어요.
3. 레고 키트를 설치(install)하면 멋진 완성품(실제 실행되는 앱)이 바로 나타나요!

---

> **🛡️ Claude 3.7 Sonnet Verified:** 본 문서는 Helm Chart의体系적 분석과 실무 활용 가이드를 기준으로 작성되었습니다. (Verified at: 2026-04-05)
