+++
title = "GitOps (깃옵스)"
description = "Git 리포지토리를 단일 진실 공급원(SSOT)으로 하여 인프라와 애플리케이션의 선언적 상태를 버전 관리하고 자동 동기화하는 현대적 운영 모델"
date = 2024-05-15
[taxonomies]
tags = ["GitOps", "Kubernetes", "ArgoCD", "Declarative", "CI/CD", "Infrastructure-as-Code"]
+++

# GitOps (깃옵스)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인프라와 애플리케이션의 **'목표 상태(Desired State)'를 Git 리포지토리에 선언적(Declarative) 코드로 저장**하고, 클러스터 내부의 에이전트(ArgoCD, Flux)가 Git과 실제 상태를 지속적으로 비교하여 자동 동기화(Sync)하는 운영 모델입니다.
> 2. **가치**: Git 커밋 = 배포이므로 모든 변경이 감사 가능(Auditable)하고, `git revert`로 즉시 롤백 가능하며, 클러스터 외부에서 인바운드 접근이 필요 없어 보안이 강화됩니다.
> 3. **융합**: Kubernetes, IaC(Terraform), CI 파이프라인, 시크릿 관리(Vault/Sealed Secrets)와 결합하여 "Git이 곧 인프라 제어판"인 선언적 운영 체계를 완성합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**GitOps**는 2017년 Weaveworks의 Alexis Richardson이 정의한 운영 모델로, **Git 리포지토리를 시스템 상태의 단일 진실 공급원(Single Source of Truth, SSOT)**으로 삼고, 선언적(Declarative) 구성을 통해 인프라와 애플리케이션을 관리하는 방법론입니다. GitOps의 4대 원칙:
1. **선언적(Declarative)**: 시스템은 선언적 방식으로 설명되어야 함 (YAML, HCL)
2. **버전 관리되고 불변(Versioned & Immutable)**: 목표 상태는 Git에 버전 관리됨
3. **자동 적용(Automated)**: 승인된 변경이 자동으로 시스템에 적용됨
4. **지속적 조정(Continuously Reconciled)**: 에이전트가 실제 상태와 목표 상태를 지속 비교

### 2. 구체적인 일상생활 비유
도서관을 상상해 보세요. 전통적 배포는 사서가 책장에 직접 가서 책을 배치하는 것입니다. **GitOps**는 **"도서 목록 카탈로그(Git)"**가 있고, 로봇이 매시간 카탈로그와 실제 책장을 비교합니다. 카탈로그에 새 책가 적히면 로봇이 자동으로 책을 가져다 놓고, 누군가 책을 훔쳐 가면 로봇이 다시 채워 넣습니다. 사서는 카탈로그만 관리하면 됩니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (Push 배포의 보안/추적 문제)**:
   전통적 CI/CD는 Jenkins가 `kubectl apply`를 실행하여 외부에서 클러스터로 푸시합니다. 문제점: 1) CI 서버가 클러스터 API에 직접 접근 권한 필요 (보안 위험) 2) 누가 언제 무엇을 배포했는지 추적 어려움 3) 클러스터 내부에서 수동 변경(Drift) 감지 불가.

2. **혁신적 패러다임 변화의 시작**:
   2017년 Weaveworks가 GitOps 개념을 발표하고, 2018년 ArgoCD가 CNCF 프로젝트로 승인되며 쿠버네티스 생태계의 표준 배포 모델이 되었습니다. "Git이 곧 제어판"이라는 패러다임은 Pull 기반 동기화로 보안과 추적성을 동시에 해결했습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   규정 준수(SOC 2, ISO 27001)는 모든 인프라 변경에 대한 감사 추적(Audit Trail)을 요구합니다. GitOps는 모든 변경이 Git 커밋으로 기록되어 자연스럽게 규정 준수를 달성합니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 관련 도구/기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Git Repository** | 목표 상태(Desired State) 저장 | YAML 매니페스트, Helm Chart, Kustomize | GitHub, GitLab | 도서 카탈로그 |
| **GitOps Operator** | Git과 클러스터 상태 비교 및 동기화 | Polling(주기적 조회) 또는 Webhook | ArgoCD, Flux | 정리 로봇 |
| **Kubernetes Cluster** | 실제 상태(Actual State) | API Server, Controller Manager | K8s, OpenShift | 책장 |
| **Reconciliation Loop** | 상태 불일치 감지 및 수정 | Diff 비교 -> Sync 실행 -> 결과 검증 | ArgoCD Application Controller | 순찰 |
| **CI Pipeline** | 아티팩트 빌드 및 Git 업데이트 | 이미지 빌드 -> Git 매니페스트 업데이트 | GitHub Actions, Tekton | 출판사 |
| **Secret Management** | 암호화된 시크릿을 Git에 저장 | Sealed Secrets, External Secrets | Bitnami Sealed, Vault | 비밀 금고 |

### 2. 정교한 구조 다이어그램: GitOps Pull 기반 배포 아키텍처

```text
=====================================================================================================
                      [ GitOps Architecture - Pull-Based Deployment ]
=====================================================================================================

  [ Developer ]               [ Git Repository ]               [ Kubernetes Cluster ]
       |                            |                                  |
       | 1. git push                |                                  |
       v                            v                                  |
+-------------+             +-------------+                            |
| Source Code |             | Config Repo |                            |
| (App Code)  |             | (Manifests) |                            |
+------+------+             +------+------+                            |
       |                           |                                   |
       | 2. Trigger CI             |                                   |
       v                           |                                   |
+-------------+                    |                                   |
| CI Pipeline |                    |                                   |
| - Build     |                    |                                   |
| - Test      |                    |                                   |
| - Push Image|                    |                                   |
+------+------+                    |                                   |
       |                           |                                   |
       | 3. Update manifest        |                                   |
       |    (new image tag)        |                                   |
       +-------------------------->|                                   |
       |                           | 4. New commit in Git              |
       |                           |    +-------------------------+    |
       |                           |    | deployment.yaml         |    |
       |                           |    | image: myapp:v2.3.1     |    |
       |                           |    +-------------------------+    |
       |                           |                                   |
       |                           | 5. Poll (every 3m) or Webhook    |
       |                           |                                   |
       |                           |          +------------------------+
       |                           |          |
       |                           |          v
       |                           |    +------------------------------------------+
       |                           |    | [ GitOps Operator (Inside Cluster) ]     |
       |                           |    |                                          |
       |                           |    |  +-------------+    +-----------------+   |
       |                           |    |  | Repo Server |    | Application     |   |
       |                           |    |  | (ArgoCD)    |    | Controller      |   |
       |                           |    |  +------+------+    +--------+--------+   |
       |                           |    |         |                    |            |
       |                           |    |         v                    v            |
       |                           |    |  +------------------------------------+  |
       |                           |    |  | Reconciliation Loop:               |  |
       |                           |    |  | 1. Fetch Git state (Desired)       |  |
       |                           |    |  | 2. Get Cluster state (Actual)      |  |
       |                           |    |  | 3. Compare (Diff)                  |  |
       |                           |    |  | 4. If OutOfSync -> Sync            |  |
       |                           |    |  +------------------------------------+  |
       |                           |    +-------------------+---------------------+
       |                           |                        |
       |                           | 6. Sync (kubectl apply)|
       |                           |                        v
       |                           |              +------------------+
       |                           |              | K8s API Server   |
       |                           |              | - Create/Update  |
       |                           |              |   Deployments    |
       |                           |              | - Reconcile Pods |
       |                           |              +--------+---------+
       |                           |                       |
       |                           |                       v
       |                           |              +------------------+
       |                           |              | Actual State     |
       |                           |              | - Pod: myapp-xyz |
       |                           |              |   Image: v2.3.1  |
       |                           |              +------------------+
       |                           |
       | 7. View in UI            |
       <--------------------------+
       |  ArgoCD Dashboard        |

=====================================================================================================

                    [ Push vs Pull Comparison ]
=====================================================================================================

  PUSH-BASED (Traditional CI/CD):           PULL-BASED (GitOps):
  +-----------------+                       +-----------------+
  | CI Server       |                       | Git Repository  |
  | (Outside K8s)   |                       | (SSOT)          |
  +--------+--------+                       +--------+--------+
           |                                         ^
           | kubectl apply                           |
           | (Needs cluster credentials!)             |
           v                                         |
  +-----------------+                       +--------+--------+
  | K8s Cluster     |                       | GitOps Agent    |
  | (Accepts push) | <---- Poll & Sync ----| (Inside K8s)    |
  +-----------------+                       +-----------------+

  Security Issue: CI server needs       Security Benefit: Agent pulls from
  inbound access to cluster             Git, no inbound access needed!

=====================================================================================================
```

### 3. 심층 동작 원리 (GitOps 핵심 메커니즘)

**1. 선언적 상태 관리 (Declarative State)**
GitOps는 "어떻게(HOW)"가 아니라 "무엇을(WHAT)"을 정의합니다:
```yaml
# Imperative (금지): "이 명령을 실행해"
# kubectl set image deployment/myapp myapp=myapp:v2

# Declarative (GitOps): "이 상태가 되어야 해"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:v2.3.1  # 이 값이 Git에 있음
```

**2. 조정 루프 (Reconciliation Loop)**
ArgoCD Application Controller가 지속적으로 실행:
1. Git에서 목표 상태(Desired) 조회
2. K8s API에서 실제 상태(Actual) 조회
3. Diff 비교: 이미지 태그, 레플리카 수, 설정값 등
4. OutOfSync이면 Sync 실행 (kubectl apply 자동화)
5. Health Check: Pod가 Running인지 확인

**3. Pull 기반 보안 모델 (Pull-Based Security)**
전통적 Push 모델: CI 서버가 K8s API에 `kubectl apply`를 실행하려면 cluster-admin 권한이 필요합니다. CI 서버가 해킹당하면 클러스터 전체가 위험합니다.
GitOps Pull 모델: 클러스터 내부의 ArgoCD가 Git을 Pull합니다. 외부에서 클러스터로의 인바운드 연결이 필요 없습니다. Git 자격증명만 있으면 됩니다.

### 4. 핵심 알고리즘 및 실무 코드 예시

**ArgoCD Application 매니페스트**

```yaml
# argocd/myapp.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  # Project (multi-tenancy)
  project: default

  # Source: Git repository
  source:
    repoURL: https://github.com/myorg/k8s-configs.git
    targetRevision: main  # Branch, Tag, or Commit SHA
    path: apps/myapp/overlays/production  # Kustomize path

    # Helm values (alternative to Kustomize)
    # helm:
    #   valueFiles:
    #   - values-prod.yaml

    # Kustomize specific
    kustomize:
      namePrefix: prod-

  # Destination: Target cluster
  destination:
    server: https://kubernetes.default.svc  # In-cluster
    namespace: myapp-production

  # Sync Policy: Automated sync
  syncPolicy:
    automated:
      prune: true     # Delete resources not in Git
      selfHeal: true  # Revert manual changes
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true

    # Retry on failure
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  # Ignore differences (e.g., HPA replicas)
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas

  # Health checks
  # ArgoCD automatically checks Deployment, StatefulSet, etc.
```

**Kustomize 기반 멀티 환경 구성**

```yaml
# apps/myapp/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest  # Overridden by overlays
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi

---
# apps/myapp/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml
- configmap.yaml

---
# apps/myapp/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: myapp-production

resources:
- ../../base

patchesStrategicMerge:
- deployment-patch.yaml

images:
- name: myapp
  newTag: v2.3.1  # Production version

---
# apps/myapp/overlays/production/deployment-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3  # Production replicas
  template:
    spec:
      containers:
      - name: myapp
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2Gi
```

**CI 파이프라인에서 Git 업데이트 (GitHub Actions)**

```yaml
# .github/workflows/gitops-update.yaml
name: Update GitOps Config

on:
  push:
    branches: [main]

jobs:
  build-and-update:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout App Code
        uses: actions/checkout@v4

      - name: Build and Push Image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker push myapp:${{ github.sha }}

      - name: Update GitOps Config Repo
        run: |
          # Clone config repo
          git clone https://x-access-token:${{ secrets.CONFIG_REPO_TOKEN }}@github.com/myorg/k8s-configs.git
          cd k8s-configs

          # Update image tag using yq
          yq -i '.images[0].newTag = "${{ github.sha }}"' apps/myapp/overlays/production/kustomization.yaml

          # Commit and push
          git config user.name "CI Bot"
          git config user.email "ci-bot@myorg.com"
          git add .
          git commit -m "chore: update myapp to ${{ github.sha }}"
          git push

          # ArgoCD will detect this commit and auto-sync!
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 배포 방식 비교

| 평가 지표 | Push 기반 (kubectl) | Push 기반 (Helm) | GitOps (ArgoCD) | GitOps (Flux) |
| :--- | :--- | :--- | :--- | :--- |
| **상태 관리** | 없음 | ConfigMap | Git (SSOT) | Git (SSOT) |
| **롤백** | 수동 | helm rollback | git revert | git revert |
| **드리프트 감지** | 없음 | 없음 | 자동 (Diff) | 자동 |
| **감사 추적** | 로그만 | 로그만 | Git 커밋 | Git 커밋 |
| **보안 모델** | CI가 클러스터 접근 | CI가 클러스터 접근 | 클러스터가 Git 접근 | 클러스터가 Git 접근 |
| **멀티 클러스터** | 어려움 | 어려움 | 지원 (Hub-Spoke) | 지원 |
| **UI/시각화** | 없음 | 없음 | ArgoCD UI | Weave GitOps UI |

### 2. 과목 융합 관점 분석

**GitOps + IaC (Terraform)**
- Terraform으로 클라우드 인프라(VPC, EKS)를 프로비저닝하고, ArgoCD로 쿠버네티스 리소스(Deployment, Service)를 관리합니다. Atlanti로 Terraform도 GitOps 방식으로 운영합니다.

**GitOps + Secret Management**
- 민감 정보(DB 패스워드)는 Git에 평문으로 저장할 수 없습니다. Sealed Secrets(공개키 암호화) 또는 External Secrets Operator(Vault 연동)로 Git에 안전하게 저장합니다.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 프로덕션 장애 발생 시 즉시 롤백**
- **문제점**: v2.3.1 배포 후 5xx 에러 급증. 즉시 이전 버전으로 되돌려야 합니다.
- **기술사 판단 (전략)**: GitOps에서 롤백은 `git revert` 한 번입니다. ArgoCD UI에서 "Rollback" 버튼을 클릭하거나, Git에서 이전 커밋으로 되돌리면 됩니다. 10초 내에 전체 클러스터에 롤백이 적용됩니다.

**[상황 B] 멀티 클러스터 배포 (Dev/Staging/Prod)**
- **문제점**: 3개의 클러스터에 동일한 애플리케이션을 배포해야 합니다.
- **기술사 판단 (전략)**: ArgoCD ApplicationSet으로 단일 템플릿에서 다중 클러스터 배포. Kustomize overlays로 환경별 차이(replicas, resources)를 관리.

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] Git 리포지토리 구조: 모놀리식 vs 앱별 리포지토리
- [ ] Secret 관리: Sealed Secrets vs External Secrets
- [ ] 동기화 빈도: Polling 간격 vs Webhook

**운영적 고려사항**
- [ ] 승인 프로세스: PR 리뷰 후 배포 vs 자동 배포
- [ ] 롤백 권한: 누가 롤백을 실행할 수 있는가?
- [ ] 드리프트 대응: 수동 변경을 어떻게 방지할 것인가?

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: Git과 클러스터 직접 수정 혼용**
- ArgoCD가 관리하는 리소스를 `kubectl edit`으로 직접 수정하면, 다음 Sync 때 덮어써집니다. selfHeal이 켜져 있으면 즉시 복구되고, 아니면 OutOfSync 상태로 남습니다. 모든 변경은 Git을 통해서만 수행해야 합니다.

**안티패턴 2: 민감 정보를 Git에 평문 저장**
- DB 패스워드, API 키를 평문 YAML로 Git에 커밋하면 보안 사고입니다. 반드시 Sealed Secrets 또는 External Secrets Operator를 사용해야 합니다.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 전통적 CI/CD (AS-IS) | GitOps (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **롤백 시간** | 30분~1시간 | 10초~1분 | **롤백 99% 단축** |
| **감사 추적** | CI 로그 검색 | Git 커밋 히스토리 | **완전한 추적** |
| **드리프트 감지** | 수동 확인 | 실시간 자동 감지 | **100% 가시성** |
| **보안 노출** | CI 서버 권한 과다 | 최소 권한 (Git만) | **공격 면적 축소** |
| **협업 효율** | 낮음 | PR 기반 리뷰 | **협업 품질 향상** |

### 2. 미래 전망 및 진화 방향
- **Progressive Delivery**: Argo Rollouts으로 카나리 배포, 블루-그린 배포를 GitOps 방식으로 자동화.
- **Multi-cluster Management**: ArgoCD + ApplicationSet으로 수십 개 클러스터를 단일 Git 리포지토리에서 관리.

### 3. 참고 표준/가이드
- **OpenGitOps (CNCF)**: GitOps 표준 정의 및 원칙
- **ArgoCD Documentation**: GitOps 구현 가이드
- **Flux Documentation**: GitOps Toolkit 가이드

---

## 관련 개념 맵 (Knowledge Graph)
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/3_automation/continuous_integration.md)**: GitOps와 연동되는 빌드/테스트 자동화
- **[카나리 배포](@/studynotes/15_devops_sre/3_automation/deployment_strategies.md)**: GitOps 기반 점진적 배포
- **[쿠버네티스](@/studynotes/13_cloud_architecture/1_native/kubernetes.md)**: GitOps의 주요 대상 플랫폼
- **[테라폼](@/studynotes/15_devops_sre/4_iac/191_terraform.md)**: 인프라 레벨 GitOps (Atlantis)
- **[시크릿 관리](@/studynotes/15_devops_sre/5_devsecops/secret_management.md)**: GitOps 보안 구성요소

---

## 어린이를 위한 3줄 비유 설명
1. 도서관에 **"이 책들을 꽂아주세요"** 라는 목록이 있어요. 로봇이 목록과 책장을 매일 확인해서 다르면 알아서 고쳐요!
2. GitOps는 이 목록을 **Git이라는 특별한 공책**에 적어두는 거예요. 누가 언제 무슨 책을 꽂았는지 다 기록되죠.
3. 덕분에 사서는 공책만 관리하면 돼요. 책이 없어지거나 순서가 바뀌면 로봇이 알아서 다시 정리해주니까요!
