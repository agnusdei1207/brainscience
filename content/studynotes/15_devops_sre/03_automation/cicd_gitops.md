+++
title = "CI/CD Pipeline & GitOps (Jenkins, ArgoCD)"
description = "소프트웨어 배포 자동화의 핵심인 CI/CD 파이프라인과 선언적 인프라 관리를 실현하는 GitOps 아키텍처를 Jenkins와 ArgoCD 사례를 통해 심층 분석합니다."
date = 2024-03-24
[taxonomies]
tags = ["devops", "cicd", "gitops", "jenkins", "argocd", "automation", "kubernetes", "cloud_native"]
categories = ["studynotes-15_devops_sre"]
+++

# CI/CD 파이프라인 및 GitOps (Jenkins & ArgoCD)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소스 코드의 통합(CI)부터 실행 환경으로의 배포(CD)까지 전 과정을 자동화하고, 인프라의 최종 상태를 Git 리포지토리에 선언적으로 정의하여 관리하는 현대적 소프트웨어 공급망 체계입니다.
> 2. **가치**: 수동 배포에 따른 휴먼 에러를 원천 차단하고, 배포 속도(Velocity)와 안정성(Reliability)을 동시에 극대화하여 비즈니스 아이디어를 실시간으로 시장에 출시(Time-to-Market 단축)할 수 있게 합니다.
> 3. **융합**: 컨테이너 오케스트레이션(Kubernetes), 코드형 인프라(IaC), 그리고 보안 자동화(DevSecOps)가 결합된 클라우드 네이티브 운영의 핵심 정수입니다.

---

## Ⅰ. 개요 (Context & Background)

과거의 소프트웨어 배포는 개발자가 코드를 짜고, 빌드한 결과물을 서버에 직접 접속하여 업로드하고 서비스를 재시작하는 고통스럽고 위험한 수작업이었습니다. 이러한 방식은 규모가 커질수록 배포 주기가 길어지고 장애 발생 시 복구가 어렵다는 치명적 한계를 가집니다. CI/CD(지속적 통합/지속적 배포)는 이러한 과정을 기계가 수행하도록 자동화한 것이며, 한발 더 나아가 GitOps는 "Git에 있는 내용이 곧 서버의 상태여야 한다"는 원칙하에 인프라와 애플리케이션의 일관성을 유지하는 최신 패러다임입니다.

**💡 일상생활 비유: 밀키트 배달 서비스와 무인 편의점**
- **CI (지속적 통합)**: 요리사(개발자)가 레시피(코드)를 고칠 때마다, 주방 로봇이 즉시 재료를 다듬고(빌드) 맛이 이상하지 않은지 한 숟가락 먹어보는(테스트) 과정입니다.
- **CD (지속적 배포)**: 완성된 밀키트를 손님의 집 앞(운영 서버)까지 자동으로 배달하고 식탁에 차려주는 과정입니다.
- **GitOps (선언적 관리)**: 무인 편의점 진열대와 같습니다. 점주가 "진열대에 우유 10개가 있어야 해"라고 장부(Git)에 적어두면, 로봇(ArgoCD)이 실시간으로 확인하다가 우유가 8개로 줄어들면 즉시 2개를 채워 넣어서 항상 장부와 똑같은 상태를 유지하는 것입니다.

**등장 배경 및 발전 과정**
1. **Agile 방법론의 확산**: 더 자주, 더 작게 배포해야 하는 요구가 생기면서 자동화가 필수가 되었습니다.
2. **컨테이너 기술(Docker)의 도래**: 환경의 일관성이 확보되면서 "어디서나 똑같이 돌아가는" 배포 파이프라인 구축이 가능해졌습니다.
3. **Kubernetes와 GitOps**: 복잡한 분산 환경의 상태를 수동으로 맞추는 것이 불가능해지자, 선언적(Declarative) 구성 관리와 자동 동기화(Reconciliation)를 수행하는 GitOps 모델이 표준으로 자리 잡았습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. CI/CD 및 GitOps 핵심 구성 요소

| 요소명 | 상세 역할 | 핵심 메커니즘 | 관련 도구 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **CI Server** | 코드 통합, 빌드, 테스트 자동화 | Webhook 트리거, 파이프라인 스크립트 실행 | Jenkins, GitHub Actions | 주방 로봇 |
| **Artifact Registry** | 빌드된 결과물(이미지) 저장소 | 버전 관리, 취약점 스캐닝 | Docker Hub, ECR, Harbor | 밀키트 창고 |
| **Git Repository** | 소스 코드 및 '인프라 선언서' 보관 | 버전 제어(Git), PR 기반 코드 리뷰 | GitLab, Bitbucket | 요리 레시피 및 장부 |
| **GitOps Agent** | Git과 클러스터 상태를 동기화 | Pull 방식 모니터링, Diff 감지 및 적용 | ArgoCD, Flux | 편의점 재고 정리 로봇 |
| **Target Cluster** | 서비스가 실제로 구동되는 환경 | 컨테이너 오케스트레이션 | Kubernetes (K8s) | 식탁 및 매장 진열대 |

### 2. Modern CI/CD & GitOps 파이프라인 아키텍처

아래는 Jenkins를 이용한 CI와 ArgoCD를 이용한 CD가 결합된 전형적인 클라우드 네이티브 배포 구조입니다.

```text
 [Developer] --- (1. Push Code) ---> [Git: App Repo]
                                          |
                                (2. Webhook Trigger)
                                          V
 [CI: Jenkins] <----------------------------------------------------------+
 |  - Lint & Unit Test                                                    |
 |  - Build Docker Image                                                  |
 |  - Security Scan                                                       |
 |  - Push Image ----> [Container Registry]                               |
 |  - Update Manifest -> [Git: Config Repo] (3. Image Tag Update)         |
 +------------------------------------------------------------------------+
                                          |
                                          V
 [CD: ArgoCD] <--- (4. Pull & Compare) --- [Git: Config Repo]
 |   (Desired State)                      (YAML Manifests)
 |        |
 | (5. Sync / Reconciliation Loop)
 |        |
 V        V
 [Kubernetes Cluster] (Current State)
 (Pods, Services, Ingress...)
```

### 3. 심층 동작 원리

#### A. CI (Continuous Integration) 상세 단계
1. **Code Integration**: 개발자가 작성한 코드가 Shared Repository에 병합됩니다.
2. **Static Analysis**: SonarQube 등을 통해 코드 품질 및 보안 취약점을 정적으로 분석합니다.
3. **Automated Testing**: 단위 테스트(Unit Test), 통합 테스트를 수행하여 기능 결함을 조기 발견합니다.
4. **Build & Packaging**: 코드를 실행 가능한 바이너리나 컨테이너 이미지로 패키징합니다.

#### B. GitOps의 핵심: Push vs Pull 모델
- **Push 모델 (Jenkins 중심)**: CI 서버가 운영 환경에 직접 접속하여 `kubectl apply` 명령을 내립니다. CI 서버가 운영 서버의 접근 권한을 가져야 하므로 보안상 위험할 수 있습니다.
- **Pull 모델 (ArgoCD 중심)**: 운영 환경 내부에 설치된 에이전트(ArgoCD)가 외부 Git을 계속 바라보며 변경 사항을 가져옵니다. 클러스터 외부로 권한을 노출하지 않아 보안성이 뛰어나며, 누군가 수동으로 서버 설정을 바꿔도 Git 상태로 자동 복구(Self-healing)합니다.

#### C. ArgoCD의 Reconciliation Loop
ArgoCD는 `Desired State`(Git에 정의된 상태)와 `Actual State`(현재 K8s에 떠 있는 상태)를 무한 루프를 돌며 비교합니다.
- **OutOfSync**: 두 상태가 다를 때 발생.
- **Sync**: ArgoCD가 Git의 내용을 K8s에 적용하여 두 상태를 일치시킴.
- **Drift Detection**: 관리자가 실수로 K8s 설정을 바꿔버려도 ArgoCD가 감지하여 다시 Git 내용으로 덮어씀.

### 4. 실무 코드 및 설정 (Jenkins Pipeline & K8s Manifest)

#### Jenkinsfile (Declarative Pipeline)
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t my-app:${env.BUILD_NUMBER} .'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Push') {
            steps {
                sh 'docker push my-app:${env.BUILD_NUMBER}'
            }
        }
        stage('Update Manifest') {
            steps {
                // Config Git Repo의 YAML 파일 내 이미지 태그를 새 버전으로 수정
                sh "sed -i 's/image: my-app:.*/image: my-app:${env.BUILD_NUMBER}/g' deploy.yaml"
                sh "git commit -am 'update image to ${env.BUILD_NUMBER}' && git push"
            }
        }
    }
}
```

#### ArgoCD Application Manifest (YAML)
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-sync
spec:
  project: default
  source:
    repoURL: 'https://github.com/my-org/config-repo.git'
    targetRevision: HEAD
    path: 'overlays/prod'
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 배포 전략(Deployment Strategy) 심층 비교

시스템 중단 없는 배포를 위해 CD 파이프라인에서 선택하는 전략들입니다.

| 전략명 | 동작 방식 | 장점 | 단점 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Recreate** | 기존 버전 모두 종료 후 새 버전 기동 | 자원 소모 적음, 데이터 일관성 | 일시적 서비스 중단 (Downtime) | 가게 문 닫고 인테리어 교체 |
| **Rolling Update** | 하나씩 순차적으로 교체 | 무중단 배포 가능 | 배포 중 구버전/신버전 공존 (호환성 이슈) | 손님 받으면서 한 테이블씩 교체 |
| **Blue/Green** | 구버전(Blue)과 똑같은 신버전(Green) 전체 구성 후 스위칭 | 즉각적인 롤백 가능, 환경 격리 | 리소스 점유량 2배 (비용 증가) | 옆 건물에 새 가게 차리고 이사 |
| **Canary** | 일부 사용자(5%)에게만 먼저 배포 후 확대 | 리스크 최소화, 실시간 모니터링 가능 | 배포 로직 복잡 (Traffic Shifting) | 단골에게만 신메뉴 먼저 맛보게 하기 |

### 2. 과목 융합 관점 분석
- **네트워크**: Canary 배포나 Blue/Green 배포 시 트래픽을 정교하게 나누기 위해 L7 로드밸런서, Ingress Controller, 또는 Service Mesh(Istio)의 가상 서비스(Virtual Service) 제어 기술이 필수적입니다.
- **보안 (DevSecOps)**: 파이프라인 중간에 정적 분석(SAST), 동적 분석(DAST), 이미지 스캐닝을 삽입하여 보안 결함이 운영 환경에 도달하기 전에 차단하는 'Shift-Left Security'를 구현합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)
- **시나리오 A: 빈번한 장애가 발생하는 수동 배포 환경 개선**
  - **상황**: 매주 금요일 밤마다 개발자가 직접 서버에 접속해 배포하며, 가끔 설정 파일 실수를 저질러 주말 내내 장애가 지속됨.
  - **판단**: GitOps 모델 도입 제안. 모든 인프라와 앱 설정을 Git으로 관리(IaC)하고, 수동 접속 권한을 회수한 뒤 ArgoCD를 통한 자동 동기화 체계 구축. 변경 이력이 Git에 남으므로 장애 시 즉각적인 `git revert`로 1분 내 복구 가능.
- **시나리오 B: 대규모 마이크로서비스(MSA)의 배포 복잡도 증가**
  - **상황**: 서비스가 50개로 늘어나면서 각 서비스의 배포 순서와 버전 관리가 꼬이기 시작함.
  - **판단**: 서비스 간 의존성을 고려한 Helm Chart 기반의 패키징 전략 수립. 환경별(Dev, Staging, Prod) 설정을 분리하는 Kustomize 적용. 배포 전 단계에서 통합 테스트(E2E)를 자동화하여 서비스 간 연동 오류를 사전에 필터링하는 파이프라인 고도화.

### 2. 도입 시 고려사항 (체크리스트)
- **비밀값 관리 (Secret Management)**: DB 암호나 API 키를 Git에 평문으로 올리는 것은 치명적입니다. Sealed Secrets, HashiCorp Vault, 또는 AWS Secrets Manager와 연동하여 보안을 강화해야 합니다.
- **롤백 전략**: 배포 성공보다 중요한 것이 '실패 시 어떻게 되돌릴 것인가'입니다. ArgoCD의 자동 롤백 기능이나 수동 롤백 절차를 미리 정의하고 연습(Game Day)해야 합니다.
- **파이프라인 가시성**: 배포가 어디서 멈췄는지, 왜 실패했는지 개발자가 한눈에 알 수 있도록 알림(Slack 연동) 및 대시보드 구축이 필요합니다.

### 3. 주의사항 및 안티패턴 (Anti-patterns)
- **수동 수정(Manual Drift)**: 급하다고 서버에 직접 들어가서 설정을 바꾸는 행위. GitOps 에이전트가 이를 다시 Git 상태로 되돌려버리거나, Git과의 불일치로 인해 추후 마이그레이션 시 대형 사고가 발생할 수 있습니다.
- **거대한 단일 파이프라인**: 모든 서비스를 하나의 거대한 Jenkinsfile로 관리하면 빌드 속도가 느려지고 한 곳의 에러가 전체 배포를 막습니다. 서비스별로 파이프라인을 쪼개어 독립적인 배포가 가능하게 해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (Manual) | 도입 후 (CI/CD + GitOps) | 효과 수치 |
| :--- | :--- | :--- | :--- |
| **배포 빈도** | 월 1~2회 (대규모 배포) | 일 수십 회 이상 (수시 배포) | 배포 주기 20배 이상 단축 |
| **장애 복구 시간(MTTR)** | 수 시간 (원인 파악 및 수동 복구) | 수 분 이내 (Git Revert/Auto Rollback) | 복구 속도 90% 이상 향상 |
| **배포 성공률** | 휴먼 에러로 인한 잦은 실패 | 자동화된 검증으로 안정적 성공 | 배포 실패율 80% 감소 |

### 2. 미래 전망 및 진화 방향
- **Platform Engineering**: 개발자가 인프라를 몰라도 셀프 서비스로 파이프라인을 생성하고 배포할 수 있도록 돕는 내부 개발자 플랫폼(IDP)이 확산되고 있습니다.
- **AI-driven DevOps (AIOps)**: AI가 배포 후의 로그와 메트릭을 실시간 분석하여, 장애 징후가 보이면 사람보다 먼저 판단하여 배포를 중단하고 이전 버전으로 되돌리는 지능형 자동화로 진화 중입니다.

### 3. ※ 참고 표준/가이드
- **DORA Metrics**: Deployment Frequency, Lead Time for Changes, MTTR, Change Failure Rate.
- **GitOps Principles (OpenGitOps)**: Declarative, Versioned and Immutable, Pulled Automatically, Continuously Reconciled.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [`[MSA (Microservices Architecture)]`](@/studynotes/04_software_engineering/01_sdlc/msa.md) : CI/CD 자동화가 없으면 운영이 불가능한 아키텍처 스타일.
- [`[Kubernetes (K8s)]`](@/studynotes/13_cloud_architecture/01_native/_index.md) : GitOps가 가장 강력한 힘을 발휘하는 선언적 운영 플랫폼.
- [`[IaC (Infrastructure as Code)]`](@/studynotes/15_devops_sre/03_automation/_index.md) : 인프라를 코드로 관리하여 GitOps의 대상이 되게 하는 기술(Terraform, Ansible).
- [`[Observability]`](@/studynotes/15_devops_sre/02_observability/_index.md) : 배포 후 시스템 상태를 감시하여 자동 롤백 여부를 판단하는 근거.

---

## 👶 어린이를 위한 3줄 비유 설명
1. **CI/CD**: 우리가 만든 프로그램을 로봇이 대신 검사하고(CI), 안전하게 서버라는 목적지까지 배달해주는(CD) 똑똑한 자동 택배 시스템이에요.
2. **GitOps**: "서버야, 이 장부에 적힌 대로만 있어!"라고 명령서를 써두면, 로봇이 밤낮으로 감시하면서 장부와 실제 모습이 똑같게 유지해주는 거예요.
3. **결론**: 사람이 일일이 손으로 하는 것보다 로봇에게 맡기면 훨씬 빠르고 실수도 없어서, 우리가 만든 멋진 기능을 친구들에게 바로 보여줄 수 있게 됩니다.
