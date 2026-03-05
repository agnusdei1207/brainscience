+++
title = "ArgoCD (아고씨디)"
description = "쿠버네티스를 위한 선언적 GitOps 지속적 배포 도구로 Git 리포지토리와 클러스터 상태를 자동 동기화"
date = 2024-05-15
[taxonomies]
tags = ["ArgoCD", "GitOps", "Kubernetes", "CD", "Declarative", "Continuous-Deployment"]
+++

# ArgoCD (아고씨디)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 쿠버네티스를 위해 설계된 **선언적 GitOps 지속적 배포(Continuous Deployment) 도구**로, Git 리포지토리에 정의된 목표 상태(Desired State)와 클러스터의 실제 상태(Actual State)를 지속적으로 비교하고 자동으로 동기화하는 CNCF 졸업 프로젝트입니다.
> 2. **가치**: UI 대시보드로 전체 클러스터 상태를 시각화하고, `git revert`로 즉시 롤백하며, Multi-cluster 배포와 Progressive Delivery(Argo Rollouts)까지 지원하여 쿠버네티스 배포의 사실상 표준이 되었습니다.
> 3. **융합**: Helm, Kustomize, Jsonnet과 같은 템플릿 도구와 통합되고, CI 파이프라인(GitHub Actions), 시크릿 관리(Vault), 카나리 배포(Argo Rollouts)와 결합하여 완전한 GitOps 플랫폼을 구성합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**ArgoCD(Automated GitOps Continuous Delivery for Kubernetes)**는 쿠버네티스 네이티브 GitOps 지속적 배포 도구입니다. 핵심 특징:
- **선언적(Declarative)**: Git에 YAML/Helm/Kustomize로 목표 상태 정의
- **자동 동기화(Automated Sync)**: Git과 클러스터 간 상태 불일치 시 자동 수정
- **시각화(UI/CLI)**: 전체 애플리케이션 토폴로지와 동기화 상태를 대시보드로 확인
- **롤백(Rollback)**: Git 히스토리 기반으로 이전 상태로 즉시 복원
- **Multi-cluster**: 단일 ArgoCD 인스턴스로 여러 클러스터 관리

### 2. 구체적인 일상생활 비유
건물 관리 시스템을 상상해 보세요. **설계도(Git)**에는 "이 방에는 책상 5개, 의자 5개가 있어야 한다"고 적혀 있습니다. **ArgoCD**는 매일 설계도와 실제 방을 비교하는 로봇입니다. 의자가 하나 없으면 자동으로 가져다 놓고, 누군가 불필요한 서랍을 두면 치워버립니다. 설계도를 수정하면 로봇이 자동으로 반영합니다. "방 상태"를 일일이 관리할 필요 없이 "설계도"만 관리하면 됩니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (kubectl의 한계)**:
   `kubectl apply -f`로 배포할 때의 문제: 1) 누가 언제 무엇을 배포했는지 추적 불가 2) 클러스터 내부에서 수동 변경(Drift) 감지 불가 3) 롤백이 복잡함 4) 멀티 클러스터 배포 어려움.

2. **혁신적 패러다임 변화의 시작**:
   2018년 Intuit가 개발하고 CNCF에 기증. 2020년 CNCF 졸업 프로젝트(Graduated Project)가 되며 쿠버네티스 생태계의 GitOps 표준 도구로 자리잡았습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   규정 준수(SOC 2) 요구사항 충족, 24/7 배포 자동화, 멀티 클라우드/멀티 클러스터 관리 필요성으로 기업들이 ArgoCD를 대규모로 도입하고 있습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 비고 |
| :--- | :--- | :--- | :--- |
| **API Server** | REST/gRPC API 제공, UI 서빙 | 인증, 인가, Webhook 처리 | Deployment |
| **Repo Server** | Git 리포지토리 캐시 및 클론 | 로컬 캐시로 Git 조회 속도 향상 | Deployment |
| **Application Controller** | Git vs 클러스터 상태 비교 및 동기화 | Reconciliation Loop 실행 | Deployment |
| **Redis** | 캐시 및 세션 저장소 | Application 상태 캐싱 | StatefulSet |
| **Application CRD** | 배포할 앱 정의 | source, destination, syncPolicy | Custom Resource |
| **AppProject CRD** | 멀티 테넌시 격리 | namespace, cluster, repository 제한 | Custom Resource |

### 2. 정교한 구조 다이어그램: ArgoCD 아키텍처

```text
=====================================================================================================
                      [ ArgoCD Architecture - Kubernetes Native GitOps ]
=====================================================================================================

  [ Git Repositories ]                    [ ArgoCD Components ]                [ Target Clusters ]
       |                                         |                                    |
       v                                         v                                    v

+------------------+            +----------------------------------+         +------------------+
| App Config Repo  |            |  argocd namespace                |         |  prod-cluster    |
| (YAML/Helm/      |            |                                  |         |                  |
|  Kustomize)      |            |  +------------------------+     |         | +--------------+ |
+--------+---------+            |  | argocd-server          |     |         | | Namespaces    | |
         |                      |  | (API + UI)             |     |         | | - myapp-prod  | |
         |                      |  | - Authentication       |     |         | | - backend-prod| |
         |  Clone/Cache         |  | - RBAC                 |     |         | +------+-------+ |
         v                      |  +-----------+------------+     |         |        |         |
+------------------+            |              |                  |         |        |         |
| Helm Chart Repo  |            |              v                  |         |  Sync  |         |
| (Artifact Hub)   |            |  +------------------------+     |         |        v         |
+--------+---------+            |  | argocd-repo-server     |     |  Sync   | +--------------+ |
         |                      |  | - Git Clone            | <------------+-| Deployments   | |
         |                      |  | - Helm Template        |     |         | | Services      | |
         v                      |  | - Kustomize Build      |     |         | | ConfigMaps    | |
+------------------+            |  +-----------+------------+     |         | +--------------+ |
| Docker Registry  |            |              |                  |         |                  |
| (Image Store)    |            |              |                  |         +------------------+
+------------------+            |              v                  |
                                |  +------------------------+     |
                                |  | argocd-application-    |     |
                                |  | controller             |     |
                                |  | - Reconciliation Loop  |     |
                                |  | - Compare Git vs K8s   |     |
                                |  | - Trigger Sync         |     |
                                |  +-----------+------------+     |
                                |              |                  |
                                |              v                  |
                                |  +------------------------+     |
                                |  | argocd-redis           |     |
                                |  | (Cache Store)          |     |
                                |  +------------------------+     |
                                |                                  |
                                |  +------------------------+     |
                                |  | Custom Resources       |     |
                                |  | - Application CRD      |     |
                                |  | - AppProject CRD       |     |
                                |  | - ApplicationSet CRD   |     |
                                |  +------------------------+     |
                                +----------------------------------+

=====================================================================================================

                      [ ArgoCD Application CRD Structure ]
=====================================================================================================

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default           # AppProject for multi-tenancy

  source:                    # WHERE to get the config
    repoURL: https://github.com/org/k8s-configs
    targetRevision: main     # Branch, Tag, or Commit
    path: apps/myapp         # Directory in repo

  destination:               # WHERE to deploy
    server: https://kubernetes.default.svc
    namespace: myapp-prod

  syncPolicy:                # HOW to sync
    automated:
      prune: true            # Delete resources not in Git
      selfHeal: true         # Revert manual changes
    syncOptions:
    - CreateNamespace=true

status:                      # Computed by controller
  sync:
    status: Synced           # Synced | OutOfSync | Unknown
    revision: abc123...
  health:
    status: Healthy          # Healthy | Degraded | Progressing

=====================================================================================================
```

### 3. 심층 동작 원리 (ArgoCD 핵심 메커니즘)

**1. 조정 루프 (Reconciliation Loop)**
Application Controller가 3분(default)마다 실행:
1. Git 리포지토리에서 매니페스트 조회 (Repo Server 통해 캐시)
2. 클러스터에서 실제 리소스 조회 (K8s API)
3. Diff 비교: Live vs Target 상태
4. OutOfSync이면 SyncPolicy에 따라 자동/수동 동기화

**2. 동기화 전략 (Sync Strategies)**
- **Manual Sync**: 사용자가 UI/CLI에서 수동으로 Sync 클릭
- **Automated Sync**: Git 변경 감지 시 자동 Sync
- **Self-Heal**: 클러스터 내 수동 변경 감지 시 자동 복구
- **Prune**: Git에서 삭제된 리소스를 클러스터에서도 삭제

**3. Health Status 평가**
ArgoCD는 리소스 타입별로 Health 상태를 평가:
- **Deployment**: 모든 Pod가 Ready이면 Healthy
- **StatefulSet**: 모든 Pod가 Running이면 Healthy
- **Service**: Endpoints가 존재하면 Healthy
- **Custom**: Lua 스크립트로 커스텀 Health 체크 가능

### 4. 핵심 알고리즘 및 실무 코드 예시

**ArgoCD ApplicationSet (Multi-Cluster/Multi-App)**

```yaml
# argocd/applicationset.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-multi-cluster
  namespace: argocd
spec:
  # Generate Applications from Git directories
  generators:
  # Generator 1: List of clusters
  - list:
      elements:
      - cluster: https://kubernetes.default.svc
        env: production
      - cluster: https://staging-cluster.example.com
        env: staging

  # Generator 2: Git directories
  - git:
      repoURL: https://github.com/org/k8s-configs.git
      revision: main
      directories:
      - path: apps/*

  template:
    metadata:
      name: '{{path.basename}}-{{env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/k8s-configs.git
        targetRevision: main
        path: '{{path}}/overlays/{{env}}'
      destination:
        server: '{{cluster}}'
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
        - CreateNamespace=true
```

**AppProject (Multi-Tenancy 격리)**

```yaml
# argocd/appproject.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: team-a
  namespace: argocd
spec:
  # Description
  description: Project for Team A

  # Source repositories (where configs come from)
  sourceRepos:
  - 'https://github.com/team-a/*'

  # Destination clusters and namespaces (where to deploy)
  destinations:
  - namespace: 'team-a-*'
    server: https://kubernetes.default.svc
  - namespace: 'team-a-*'
    server: https://prod-cluster.example.com

  # Allowed K8s resource types
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  - group: 'rbac.authorization.k8s.io'
    kind: ClusterRole

  namespaceResourceBlacklist:
  - group: ''
    kind: ResourceQuota  # Team cannot create ResourceQuota

  # Sync windows (maintenance windows)
  syncWindows:
  - kind: deny
    schedule: '0 0 * * *'  # No syncs at midnight UTC
    duration: 1h
    namespaces:
    - team-a-prod
```

**ArgoCD CLI 사용 예시**

```bash
# Login to ArgoCD
argocd login argocd.example.com --grpc-web

# List applications
argocd app list

# Get application details
argocd app get myapp

# Sync application
argocd app sync myapp

# Sync with prune (delete removed resources)
argocd app sync myapp --prune

# Rollback to previous revision
argocd app rollback myapp

# History of deployments
argocd app history myapp

# Diff between Git and cluster
argocd app diff myapp

# Wait for sync to complete
argocd app wait myapp --sync

# Set auto-sync
argocd app set myapp --sync-policy automated

# Add webhook (Git -> ArgoCD notification)
argocd proj add-destination team-a https://new-cluster.com
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: CD 도구 비교

| 평가 지표 | ArgoCD | FluxCD | Spinnaker | Jenkins X |
| :--- | :--- | :--- | :--- | :--- |
| **아키텍처** | K8s Controller | K8s Controller | Microservices | K8s Controller |
| **UI** | 강력한 UI | 제한적 (Weave UI 별도) | 강력한 UI | 없음 |
| **Multi-cluster** | 지원 | 지원 | 지원 | 지원 |
| **Rollback** | Git 기반 | Git 기반 | Pipeline 기반 | Git 기반 |
| **학습 곡선** | 낮음 | 중간 | 높음 | 중간 |
| **CNCF 상태** | Graduated | Graduated | Archived | Archived |
| **카나리 배포** | Argo Rollouts | Flagger | Kayenta | 미지원 |

### 2. 과목 융합 관점 분석

**ArgoCD + Helm/Kustomize**
- Helm Chart 또는 Kustomize로 매니페스트를 템플릿화하고, ArgoCD가 이를 렌더링하여 배포합니다. 환경별(Dev/Staging/Prod) 오버레이를 쉽게 관리합니다.

**ArgoCD + Argo Rollouts (Progressive Delivery)**
- ArgoCD는 배포 상태 관리, Argo Rollouts은 배포 전략(카나리, 블루-그린)을 담당합니다. 두 도구가 통합되어 Progressive Delivery를 GitOps 방식으로 구현합니다.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 100개 마이크로서비스 배포 관리**
- **문제점**: 100개의 서비스를 각각 수동으로 배포하고 추적하는 것이 불가능합니다.
- **기술사 판단 (전략)**: ApplicationSet으로 100개 서비스를 단일 템플릿으로 관리. AppProject로 팀별 격리. UI 대시보드로 전체 상태를 한눈에 확인.

**[상황 B] 보안 규정 준수 (감사 추적)**
- **문제점**: "누가 언제 어떤 변경을 했는가?"에 대한 감사 로그가 필요합니다.
- **기술사 판단 (전략)**: ArgoCD의 모든 배포는 Git 커밋과 연동됩니다. `argocd app history`로 모든 배포 이력을 확인할 수 있고, Git 커밋 로그가 곧 감사 로그입니다.

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] Repo 구조: Monorepo vs Polyrepo
- [ ] Sync 빈도: 기본 3분, Webhook으로 실시간화 가능
- [ ] 리소스 제한: 대규모 클러스터에서 컨트롤러 리소스 증설 필요

**운영적 고려사항**
- [ ] RBAC: ArgoCD 자체 인증 또는 SSO(OIDC) 연동
- [ ] 백업: Application CRD와 AppProject를 Git에 저장
- [ ] HA 구성: argocd-server, repo-server 다중 복제

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: 단일 Application에 모든 리소스 포함**
- 1000개 리소스를 단일 Application에 넣으면 Sync 시간이 길어지고, UI 로딩이 느려집니다. 서비스 단위로 Application을 분리해야 합니다.

**안티패턴 2: selfHeal 없이 수동 변경 허용**
- `selfHeal: false`로 두면 클러스터 내 수동 변경이 Git과 달라도 자동 복구되지 않습니다. 프로덕션에서는 `selfHeal: true` 권장.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | kubectl 배포 (AS-IS) | ArgoCD GitOps (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **배포 추적** | CI 로그 검색 | Git + UI 대시보드 | **가시성 100%** |
| **롤백 시간** | 30분 이상 | 10초 | **롤백 99% 단축** |
| **드리프트 감지** | 수동 | 실시간 자동 | **100% 탐지** |
| **멀티 클러스터** | 스크립트 작성 | 단일 UI 관리 | **운영 효율 10배** |

### 2. 미래 전망 및 진화 방향
- **Argo Rollouts 통합 강화**: Progressive Delivery(카나리, 블루-그린)가 ArgoCD UI에 완전히 통합됩니다.
- **AI 기반 배포 검증**: 메트릭 기반 자동 롤백, Anomaly Detection 통합.

### 3. 참고 표준/가이드
- **ArgoCD Documentation**: 공식 문서 및 베스트 프랙티스
- **OpenGitOps (CNCF)**: GitOps 표준 정의
- **GitOps Patterns (Weaveworks)**: GitOps 설계 패턴

---

## 관련 개념 맵 (Knowledge Graph)
- **[GitOps](@/studynotes/15_devops_sre/3_automation/86_gitops.md)**: ArgoCD가 구현하는 운영 모델
- **[FluxCD](@/studynotes/15_devops_sre/3_automation/90_fluxcd.md)**: ArgoCD의 대안 GitOps 도구
- **[Helm](@/studynotes/15_devops_sre/3_automation/92_helm.md)**: ArgoCD와 통합되는 패키지 매니저
- **[Kubernetes](@/studynotes/13_cloud_architecture/1_native/kubernetes.md)**: ArgoCD의 배포 대상
- **[배포 전략](@/studynotes/15_devops_sre/3_automation/deployment_strategies.md)**: Argo Rollouts과 연동

---

## 어린이를 위한 3줄 비유 설명
1. 레고 조립 설명서를 Git에 올려두면, **로봇이 알아서 조립**해요! 설명서가 바뀌면 로봇이 자동으로 수정하죠.
2. ArgoCD는 이 로봇의 **똑똑한 뇌**예요. "지금 레고가 설명서랑 다르네?" 하고 알아서 고쳐줘요.
3. 덕분에 우리는 설명서만 잘 쓰면 돼요. 로봇이 알아서 조립하고, 고치고, 되돌려주니까요!
