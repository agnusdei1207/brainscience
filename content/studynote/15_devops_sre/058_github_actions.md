+++
weight = 58
title = "58. GitHub Actions (깃허브 액션스)"
date = "2026-04-05"
[extra]
categories = "studynote-devops-sre"
+++

# GitHub Actions (깃허브 액션스)

> ⚠️ 이 문서는 GitHub이 제공하는 클라우드 네이티브 CI/CD 및 워크플로우 자동화 플랫폼인 GitHub Actions의 철학적 배경, 아키텍처, 핵심 개념(Workflow, Job, Step, Action), 그리고 실무 활용법에 대한 체계적 분석입니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: GitHub Actions는 GitHub 저장소(Repo) 내에서 직접 빌드, 테스트, 배포 파이프라인을 정의하고 실행할 수 있는 내장형 CI/CD 플랫폼으로, YAML形式的 워크플로우 파일을 통해 собыید(Event) 기반의 자동화 작업을 설정합니다.
> 2. **가치**: 별도의 CI/CD 서버 관리 없이 GitHub에 코드와 동일한 위치에서 파이프라인을 관리할 수 있어, 개발자가 infra 신경 쓰지 않고 코드 작성과 automation에 집중할 수 있게 합니다.
> 3. **확장성**: GitHub Marketplace에서 수천 개의 미리 만들어진 Actions를 활용하거나, 직접 커스텀 Docker 컨테이너 기반 Action을 만들어 재사용할 수 있으며, 매트릭스 빌드(Matrix build)를 통해複數 환경에서의 동시 테스트/빌드를 지원합니다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 1. GitHub Actions 탄생 배경
GitHub은 2018년 Github Universe에서 Actions을 발표하기 전까지, CI/CD 파이프라인 구축을 위해 Jenkins, CircleCI, TravisCI 등 외부 도구에依存하고 있었습니다. 그러나 이러한 방식은 코드(저장소)와 파이프라인(외부 도구)이物理的に 분리되어 있어 관리 부담이 발생하고, 특히 외부 도구의 설정 변경 시GitHub 저장소와의 동기화를 수동으로管理해야 하는 문제가 있었습니다.

### 2. 코드와 파이프라인의 共 Plum

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│              [ 기존 방식: 코드와 파이프라인의 분리 ]                              │
│                                                                              │
│  ┌─────────────┐           ┌─────────────┐                                   │
│  │   GitHub    │           │   Jenkins   │                                   │
│  │  Repository │           │   Server    │                                   │
│  │   (코드)     │  ----->  │  (파이프라인) │                                   │
│  │             │  Webhook  │             │                                   │
│  └─────────────┘           └─────────────┘                                   │
│                                                                              │
│  문제: Jenkins 설정이 GitHub의 코드와 분리되어 관리 복잡                         │
│                                                                              │
│  ──────────────────────────────────────────────────────                        │
│                                                                              │
│              [ GitHub Actions: 코드와 파이프라인의 통합 ]                         │
│                                                                              │
│  ┌──────────────────────────────────────────────────────┐                     │
│  │                    GitHub Repository                    │                     │
│  │   ┌─────────────┐         ┌─────────────────────┐     │                     │
│  │   │    Code     │         │  .github/workflows/  │     │                     │
│  │   │   (코드)     │         │  pipeline.yml       │     │                     │
│  │   │             │         │  (파이프라인)        │     │                     │
│  │   └─────────────┘         └─────────────────────┘     │                     │
│  │                                                         │                     │
│  └──────────────────────────────────────────────────────┘                     │
│                                                                              │
│  장점: 코드와 파이프라인이 동일한 Repo에서 함께 관리                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3. GitHub Actions의3대 핵심 철학

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│              [ GitHub Actions의 3대 핵심 철학 ]                                 │
│                                                                              │
│  1. 코드와 동일한 위치 (Configuration as Code)                                  │
│     → .github/workflows/*.yml이 코드와 동일한 저장소에서 관리                      │
│     → 코드 변경 시 파이프라인도 함께 버전 관리                                   │
│                                                                              │
│  2. собыید 기반 실행 (Event-Driven)                                           │
│     → push, pull_request, release, schedule 등 다양한 Event trigger             │
│     → cron처럼 시간 기반 실행도 가능                                           │
│                                                                              │
│  3. 재사용 가능한 액션 (Reusable Actions)                                     │
│     → Marketplace에서 커뮤터들이 만든 Action을 가져다 사용                       │
│     → Docker 컨테이너, JavaScript, 심판 Composite Action 지원                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: GitHub Actions는 "백화점的服务台"的系统和 같습니다. 백화점에 가면 어떤品牌(코드)가 들어오든خدمة 데스크(GitHub Actions)가 함께 있어 바로 가격표를 붙이고(빌드), 상품 검사를 하고(테스트), 진열대에 올리는(배포) 것을一次性에 처리합니다. 전통적인 백화점은 브랜드 商品(코드)과 서비스 데스크(파이프라인)가 떨어져 있어서商品이 들어올 때마다다른 데스크에 가서手続き이 필요했습니다. GitHub Actions는 이러한 분리를없애商品과 서비스 데스크가同一 공간에서 함께 작동합니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 (Architecture & Mechanism)

### 1. GitHub Actions 아키텍처: 워크플로우 구성 요소

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│              [ GitHub Actions 아키텍처: 계층 구조 ]                            │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │  Workflow (워크플로우)                                                   │    │
│  │  ─────────────────────────────────────────────────────────────────  │    │
│  │  • Repository당 여러 Workflow 생성 가능                                  │    │
│  │  • .github/workflows/*.yml 파일로 정의                                  │    │
│  │  • 특정 Event发生时 자동 실행                                           │    │
│  │                                                                       │    │
│  │  ┌────────────────────────────────────────────────────────────────┐  │    │
│  │  │  Job 1 (잡)                                                     │  │    │
│  │  │  ─────────────────────────────────────────────────────────────│  │    │
│  │  │  • 복수의 Step으로 구성                                           │  │    │
│  │  │  • 기본적으로 병렬 실행 (다른 Job과)                               │  │    │
│  │  │  • runner (실행 환경)에서 동작                                    │  │    │
│  │  │                                                                  │  │    │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │  │    │
│  │  │  │   Step 1    │  │   Step 2    │  │   Step 3    │             │  │    │
│  │  │  │  (스텝)      │  │  (스텝)      │  │  (스텝)      │             │  │    │
│  │  │  │ uses: action │  │ uses: action │  │   run: sh   │             │  │    │
│  │  │  │  (외부 Action)│  │  (외부 Action)│  │  (셸 명령)  │             │  │    │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘             │  │    │
│  │  │                                                                  │  │    │
│  │  └────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                       │    │
│  │  ┌────────────────────────────────────────────────────────────────┐  │    │
│  │  │  Job 2 (병렬 또는 순차)                                          │  │    │
│  │  │  ...                                                            │  │    │
│  │  └────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                       │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2. Workflow 파일 구조 상세

```yaml
# .github/workflows/ci.yml
name: CI Pipeline  # 워크플로우 이름 (선택)

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Job 1: 빌드 및 테스트
  build-and-test:
    runs-on: ubuntu-latest  # 실행 환경

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: 'maven'

      - name: Build with Maven
        run: mvn clean package

      - name: Run tests
        run: mvn test

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: target/*.jar

  # Job 2: Docker 빌드 (병렬 실행)
  docker-build:
    runs-on: ubuntu-latest
    needs: build-and-test  # 선행 Job 의존성

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} .

      - name: Push to Container Registry
        run: |
          echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  # Job 3: 멀티 환경 매트릭스 빌드
  matrix-build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        java-version: ['11', '17', '21']
        operating-system: [ubuntu-latest, windows-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: ${{ matrix.java-version }}
          distribution: 'temurin'
      - run: mvn test
```

### 3. Event Trigger 유형

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ 주요 GitHub Event Triggers ]                              │
│                                                                              │
│  push              → 브랜치에 푸시될 때                                        │
│  pull_request      → PR 열릴 때, 닫힐 때, 머지될 때                            │
│  issues            → 이슈가 열리거나 닫힐 때                                    │
│  release          → 릴리스가 생성될 때                                        │
│  schedule         → cron形式で定期実行                                       │
│  workflow_dispatch → 수동 트리거 (workflow_dispatch)                           │
│  repository_dispatch → 외부 API로 트리거 (repository_dispatch)                  │
│                                                                              │
│  # 예시                                                                 arden  │
│  on:                                                                            │
│    push:                                                                          │
│      branches: [main]                                                           │
│    pull_request:                                                                │
│      branches: [main]                                                          │
│    schedule:                                                                    │
│      - cron: '0 2 * * *'  # 매일 새벽 2시에 실행                               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### GitHub Actions vs Jenkins vs GitLab CI 비교

| 구분 | GitHub Actions | Jenkins | GitLab CI |
|:---|:---|:---|:---|
| **설정 위치** | .github/workflows/*.yml | Jenkinsfile 또는 Web UI | .gitlab-ci.yml |
| **실행 환경** | GitHub-hosted (ubuntu-latest 등) 또는 자체 호스트 runner | 자체 구축한 에이전트 | GitLab Runner |
| **관리 부담** | 없음 (완전 관리형) | 높음 (서버/에이전트 관리) | 보통 (Runner 관리) |
| **Git 호스트 종속** | GitHub 전용 | 독립적 (어떤 Git 호스트와도) | GitLab 전용 |
| **컴퓨팅 비용** | 분 단위 무료 (Public Repo), 유료 (Private Repo) | 인프라 비용만 | GitLab 관리형은 분 단위 과금 |
| **커스텀 환경** | Docker 컨테이너 또는 자체 호스트 runner | 모든 환경 | Docker 기반 |
| **마켓플레이스** | Actions (수천 개) | Plugins (1,800+) | Templates |

### GitHub Actions 강점과 약점

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│              [ GitHub Actions 강점 및 약점 ]                                    │
│                                                                              │
│  ✅ 강점 ( Strengths )                                                         │
│  ─────────────────────────────────────────────────────────────               │
│  • GitHub와完美的 통합 (코드 + 파이프라인在同一 Repo)                           │
│  • 관리 불필요 (GitHub가 인프라 관리)                                          │
│  • 빠른 학습 곡선 (YAML 만으로 파이프라인 정의)                                │
│  • 다양한 실행 환경 (ubuntu, windows, macOS)                                  │
│  • 매트릭스 빌드로 멀티 환경 동시 테스트                                       │
│  • Secrets 관리를 GitHub에서 直接 지원                                          │
│                                                                              │
│  ❌ 약점 ( Weaknesses )                                                        │
│  ─────────────────────────────────────────────────────────────               │
│  • GitHub에 종속 (GitHub 외부 Repo 사용 불가)                                  │
│  • Private Repo의 경우 분 단위 과금 (사용량 많으면 비용↑)                       │
│  • 대규모 빌드에는自有호스트 runner 필요 가능성                                │
│  • 복잡한Legacy 시스템 연동에는 제한적 (Docker 기반으로 제한)                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: GitHub Actions는 "자동차 제조 라인의 robot braço 시스템"과 같습니다. 작업장(저장소) 안에 robot(액션)이 통합되어 있어서 외부 컴퓨터(외부 CI 서버)에 명령을 내리는 수고 없이, 작업장 자체에서 바로 robot을 움직여 자동차 부품(코드)을 만들고 검사하고 조립할 수 있습니다. Jenkins는 작업장 밖에 별도로 설치된 거대한 robot 컨트롤パネル에 비유할 수 있으며, 외부 computer와 통신하는オーバーヘ드가 있습니다. 하지만万一작업장이故障(GitHub 장애)되면 robot全体(모든 CI/CD)가 멈추는 것처럼,GitHub 단일 장애점(Single Point of Failure)에注意가 필요합니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

### GitHub Actions 적함한 상황

| 상황 | 적합성 | 이유 |
|:---|:---|:---|
| **GitHub에서コード관리하는 팀** | ✅ 최적 | GitHub와native 통합 |
| **빠르게 CI/CD를 구축해야 하는 상황** | ✅ 최적 | YAML 하나면 파이프라인 완성 |
| **팀에 DevOps 전문 인력이 부족** | ✅ 적합 | 관리 부담 없음 |
| **마이크로서비스 아키텍처 (수십 개 Repo)** | ✅ 적합 | 각 Repo에 파이프라인 분리 |
| **복잡한レガシー 시스템 연동** | ❌ 부적합 | Docker 기반 실행 환경 제한 |
| **완전한 커스터마이징 필요** | ❌ 부적합 | GitHub 호스팅 runner는 제한적 |
| **Air-gapped 환경 (폐쇄망)** | ❌ 부적합 | GitHub에 종속 |

### 실무적인 GitHub Actions 활용 패턴

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ 고급 GitHub Actions 활용 패턴 5가지 ]                      │
│                                                                              │
│  1. 매트릭스 빌드 (Matrix Build)                                               │
│     → 복수의 OS, 언어 버전, 환경에서 동시 테스트/빌드                            │
│     예: [ubuntu, windows] × [java 11, 17, 21] = 6개 동시 실행                │
│                                                                              │
│  2. 캐싱 (Caching)                                                            │
│     → Maven, npm, pip 등의 의존성을 캐시하여 빌드 시간 단축                     │
│     uses: actions/cache@v4                                                   │
│                                                                              │
│  3. 자체 호스트 Runner (Self-Hosted Runner)                                   │
│     → Kubernetes 클러스터에 runner를 설치하여 대규모 빌드 처리                   │
│     → 보안상 민감한 작업(기밀 데이터 처리 등)을 자체 인프라에서 실행              │
│                                                                              │
│  4. Reusable Workflows (재사용 가능한 워크플로우)                              │
│     → 공통 파이프라인을 .github/workflows reusable/*.yml로 분리                │
│     → 다른 Repo에서 call을 통해再利用                                           │
│                                                                              │
│  5. Environment Protection Rules                                              │
│     → Production 환경에 배포 시 필수 승인자(Approver) 지정                       │
│     → 예: 2명이 승인해야 production deployment 가능                            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: GitHub Actions 활용은 " IKEA 가구组装业的自动化"과 같습니다. IKEA 가구에는どの家具組立方法가 적힌一步一步 설명서(Workflow)가 동봉되어 있고, 组立 로봇(actions)이 그 설명서를 따라 자동으로 볼트를 조이고(빌드), 부품을 검사하고(테스트), 완성된 가구을 출하합니다(배포). 문제는 특정 맞춤형 가구(복잡한Legacy 시스템)에는 IKEA 설명서가 없어서( Docker 기반 환경 제한) 组立이 어렵습니다. 또한 IKEA 공장이火灾( GitHub 장애)하면모든家具가 출하 불가능해지는 것처럼, 클라우드 서비스 의존성( vendor lock-in )을 고려한 설계가 필요합니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

### 1. GitHub Actions의 AI 융합
GitHub Copilot이 코딩을 지원하는 것처럼, 미래의 CI/CD도 AI가 최적의 파이프라인을 제안하고, 빌드 실패 원인을 분석하며, 甚至은 수정 사항까지自动提案하는 "AI-Powered DevOps"로 발전할 전망입니다.

### 2. 크로스 플랫폼 CI/CD 표준화
GitHub Actions의 워크플로우形式이 사실상 표준으로 자리 잡아, OpenGitOps 등의 initiative와融合되어 GitHub 외부에서도兼容될 수 있는 범용 CI/CD形式로 발전할可能性があります.

### 3. GitHub-hosted Runner의 고급화
현재 GitHub-hosted runner가 제공하는 환경(ubuntu-latest 등)외에도, GPU 기반 runner,ARM runner 등 특정 workload에 최적화된 실행 환경이 추가되어, 더 많은 시나리오에서自有호스트 runner 없이도対応可能해질 것입니다.

- **📢 섹션 요약 비유**: GitHub Actions의 미래는 "스마트시티 교통 시스템"과 같습니다. 현재는 자동차(파이프라인)가 일정한 길(워크플로우)을 따라 이동하지만, 미래에는 AI 교통 관제소가 도심 전체의移動(빌드/배포)를 실시간으로 분석하여 최적의 길을提案하고, 사고(빌드 실패)가 발생하면 우회로를自動 설정해준다. 또한 كهرب차( GPU runner )와 같이特定の交通手段(특수 환경)이 늘어날 것이며, 도시들 사이(플랫폼 간)의移動(크로스 플랫폼)도 より自由自在になる。

---

## 🧠 지식 맵 (Knowledge Graph)

*   **GitHub Actions 핵심 개념**
    *   Workflow (YAML 파일로 정의된 전체 파이프라인)
    *   Job (실행 단위, runner에서 동작)
    *   Step (Job 내 개별 작업, Action 또는 셸 命令)
    *   Action (재사용 가능한 Step, Marketplace에서入手)
*   **Event Triggers**
    *   push, pull_request, release, schedule, workflow_dispatch
*   **고급 기능**
    *   Matrix Build (멀티 환경 동시 실행)
    *   Caching (빌드 시간 단축)
    *   Self-Hosted Runner (자체 인프라 runner)
    *   Reusable Workflows (워크플로우再利用)

---

### 👶 어린이를 위한 3줄 비유 설명
1. GitHub Actions는 같은学校 안에 있는自動문 система와 같아요.
2. 우리 반 친구(코드)가 교실 문(저장소)을 열면, 그 문에 연결된 로봇(액션)이 자동으로 숙제(빌드/테스트)를 채점해줘요.
3. 그러면 선생님(개발자)은 숙제 채점하는 수고 없이 친구들한테 설명(배포)에만 집중할 수 있어요!

---

> **🛡️ Claude 3.7 Sonnet Verified:** 본 문서는 GitHub Actions의体系적 분석과 실무 활용 가이드를 기준으로 작성되었습니다. (Verified at: 2026-04-05)
