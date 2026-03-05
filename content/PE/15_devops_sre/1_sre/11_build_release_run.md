+++
title = "빌드, 릴리스, 실행 (Build, Release, Run) 단계의 엄격한 분리"
description = "12-Factor App의 5번째 원칙으로 소프트웨어交付 lifecycle에서 빌드, 릴리스, 실행의 3단계를 엄격히 분리하여 재현성과 추적성을 보장하는 DevOps 핵심实践"
date = 2024-05-15
[taxonomies]
tags = ["12-Factor-App", "CI/CD", "Build", "Release", "DevOps", "Pipeline"]
+++

# 빌드, 릴리스, 실행 (Build, Release, Run)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 전달 파이프라인에서 코드를 실행 가능한 아티팩트로 변환하는 '빌드', 환경별 설정을 주입하는 '릴리스', 실제 프로세스를 구동하는 '실행'의 세 단계를 명확히 분리하여 각 단계의 책임과 출력물을 독립적으로 관리하는 12-Factor App 핵심 원칙입니다.
> 2. **가치**: 이 분리를 통해 '어떤 코드가', '어떤 설정으로', '언제' 배포되었는지 100% 추적 가능(Traceability)해지며, 프로덕션 장애 발생 시 정확한 릴리스 버전으로 즉시 롤백할 수 있는 안전망을 확보합니다.
> 3. **융합**: 컨테이너(Docker)와 CI/CD 파이프라인(Jenkins, GitHub Actions)의 핵심 설계 철학으로, GitOps(ArgoCD)의 선언적 배포 모델과 결합하여 인프라까지 포함한 전체 시스템의 불변성(Immutability)을 실현합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**빌드-릴리스-실행(Build-Release-Run)** 분리 원칙은 12-Factor App 방법론의 다섯 번째 원칙으로, 소프트웨어 전달 수명 주기(SDLC)를 세 개의 엄격하게 구분된 단계로 나누는 것을 말합니다. **빌드(Build)** 단계는 소스 코드를 컴파일하고 의존성을 해결하여 실행 가능한 아티팩트(JAR, Docker Image, Binary)를 생성하는 과정이며, 개발자가 주도하고 코드베이스의 특정 커밋(Immutable Snapshot)에서 시작됩니다. **릴리스(Release)** 단계는 빌드된 아티팩트와 환경별 설정(Config)을 결합하여 특정 배포 환경(Staging, Production)에서 실행될 수 있는 형태로 패키징하는 과정입니다. **실행(Run)** 단계는 릴리스된 패키지를 실제 프로덕션 환경에서 프로세스로 구동하고 운영하는 단계입니다. 이 세 단계는 각각 독립된 입력과 출력을 가지며, 한 단계의 출력이 다음 단계의 입력이 되는 단방향 파이프라인을 형성합니다.

### 💡 2. 구체적인 일상생활 비유
자동차 제조 공장을 상상해 보세요. **빌드 단계**는 차량의 기본 골격과 엔진을 조립하여 '운반이 가능한 완성 차량'을 만드는 과정입니다. 이 차량은 아직 어떤 나라에서 운행될지 결정되지 않았습니다. **릴리스 단계**는 이 차량에 한국용/미국용 계기판, 좌/우핸들, 내비게이션 언어 팩 등 '운행 국가에 맞는 설정'을 주입하여 '특정 시장용 출고 차량'으로 완성하는 과정입니다. **실행 단계**는 완성된 차량이 실제 도로에서 운전자에 의해 운행되는 단계입니다. 빌드된 차량(아티팩트)은 수정할 수 없고, 릴리스된 차량은 추적 가능한 고유 VIN 번호(Release ID)를 가지며, 운행 중인 차량은 실시간 모니터링됩니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (설정의 혼재와 재현 불가능성)**:
   전통적인 소프트웨어 배포에서는 빌드, 설정 주입, 실행이 불분명하게 섞여 있었습니다. 개발자가 로컬에서 "build.bat"를 실행하면 컴파일과 함께 설정 파일이 하드코딩되어, 같은 코드라도 누가, 언제 빌드했느냐에 따라 다른 결과물이 나왔습니다. 프로덕션 장애 시 "개발 환경에서는 잘 되는데..."라는 변명이 통용되는 근본 원인은 빌드 산출물의 불일치(Non-reproducibility)였습니다.

2. **혁신적 패러다임 변화의 시작**:
   2011년 Heroku의 Adam Wiggins가 제안한 12-Factor App 방법론은 클라우드 네이티브 애플리케이션 설계의 핵심 원칙들을 정립했습니다. 그중 5번째 원칙인 Build-Release-Run 분리는 "코드는 한 번만 빌드되고, 설정은 릴리스 시점에 주입되며, 실행은 단순한 프로세스 시작이어야 한다"는 선언적 접근을 제시했습니다. 이는 Docker 컨테이너 이미지의 'Build Once, Run Anywhere' 철학과 완벽하게 일치합니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   마이크로서비스 아키텍처(MSA) 환경에서는 수백 개의 서비스가 매일 수십 번씩 배포됩니다. 각 배포마다 '어떤 코드+어떤 설정'이 조합되었는지 추적하지 못하면, 장애 발생 시 원인 분석이 불가능합니다. 또한 SOC 2, ISO 27001 등의 규정 준수(Compliance) 요구사항은 모든 프로덕션 변경 사항에 대한 감사 추적(Audit Trail)을 의무화하고 있어, Build-Release-Run 분리는 선택이 아닌 필수입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Stage) | 상세 역할 | 내부 동작 메커니즘 | 관련 도구/기술 | 산출물 (Output) |
| :--- | :--- | :--- | :--- | :--- |
| **Build (빌드)** | 소스 코드를 실행 가능한 불변 아티팩트로 변환 | ① 의존성 해결 (Dependency Resolution) ② 컴파일 (Java/Kotlin/Go) ③ 번들링 (Webpack/Vite) ④ 이미지 빌드 (Docker Build) | Maven, Gradle, npm, Docker, Kaniko | 불변 아티팩트 (JAR, Docker Image with SHA) |
| **Release (릴리스)** | 아티팩트 + 환경 설정 결합 → 배포 가능한 릴리스 생성 | ① 환경 변수(Config Maps) 주입 ② 시크릿(Secrets) 마운트 ③ 버전 태그 부여 ④ 변경 불가능한 릴리스 ID 생성 | Helm, Kustomize, ArgoCD, Spinnaker | Release ID (e.g., `v2.3.1-prod-20240515`) |
| **Run (실행)** | 릴리스된 패키지를 프로세스로 구동 및 관리 | ① 컨테이너 스케줄링 (Pod Creation) ② 헬스 체크 (Health Probe) ③ 트래픽 라우팅 (Service/Ingress) ④ 로그 수집 | Kubernetes, systemd, PM2, supervisord | 실행 중인 프로세스 (PID, Container ID) |
| **Release Store** | 모든 릴리스 버전을 보관하여 롤백 지원 | 시맨틱 버저닝 기반 스토리지, 불변 태그 정책, 아티팩트 서명(Cosign) | AWS ECR, JFrog Artifactory, Harbor | 버전별 릴리스 히스토리 |
| **Config Injector** | 런타임에 설정을 코드에서 분리하여 주입 | 환경 변수(Env Vars), 볼트(Vault) 동적 시크릿, ConfigMap 마운트 | HashiCorp Vault, AWS Secrets Manager | 런타임 설정 데이터 |

### 2. 정교한 구조 다이어그램: Build-Release-Run 파이프라인 아키텍처

```text
=====================================================================================================
                    [ Build-Release-Run Strict Separation Architecture ]
=====================================================================================================

  [ Developer Workstation ]              [ CI/CD Infrastructure ]                  [ Production ]
         │                                      │                                      │
         │ 1. git push                          │                                      │
         ▼                                      ▼                                      │
+------------------+                  +------------------------+                        │
|  Git Repository  |                  |   BUILD STAGE          |                        │
| (Source Code +   | ───────────────> | ┌──────────────────┐   |                        │
|  lock files)     |  Checkout Code   | │ 1. Dependency     │   |                        │
|                  |                  │ │    Resolution     │   |                        │
| commit: a1b2c3d  |                  | │ 2. Compile/Bundle │   |                        │
+------------------+                  | │ 3. Unit Test      │   |                        │
                                      | │ 4. Docker Build   │   |                        │
                                      | └────────┬─────────┘   |                        │
                                      |          │             |                        │
                                      |          ▼             |                        │
                                      | ┌────────────────────┐ |                        │
                                      | │ BUILD ARTIFACT     │ |                        │
                                      | │ myapp:a1b2c3d      │ | (Immutable Image)      │
                                      | │ SHA256:7f8e9a...   │ |                        │
                                      | └────────┬─────────┘ |                        │
                                      +──────────┼───────────+                        │
                                                 │                                    │
                                                 │ Artifact Push                      │
                                                 ▼                                    │
+------------------+                  +------------------------+                        │
| Config Repo      |                  |   RELEASE STAGE        |                        │
| (GitOps Config)  |                  | ┌──────────────────┐   |                        │
| - values-dev.yaml| ───────────────> │ │ 1. Load Config   │   |                        │
| - values-prod.yaml                  │ │    per Env       │   |                        │
| - secrets/       |   Config Values  │ │ 2. Inject Secrets│   |                        │
+------------------+                  │ │ 3. Generate      │   |                        │
                                      │ │    Manifests     │   |                        │
                                      │ │ 4. Tag Release   │   |                        │
                                      │ └────────┬─────────┘   |                        │
                                      |          │             |                        │
                                      |          ▼             |                        │
                                      | ┌────────────────────┐ |                        │
                                      | │ RELEASE CANDIDATE  │ |                        │
                                      | │ v2.3.1-prod-2024   │ | (Deployable Unit)      │
                                      | │ + Config Hash      │ |                        │
                                      | └────────┬─────────┘ |                        │
                                      +──────────┼───────────+                        │
                                                 │                                    │
                                                 │ Deploy                             │
                                                 └────────────────────────────────────>│
                                                                                      ▼
                                                                         +------------------------+
                                                                         |   RUN STAGE            |
                                                                         | ┌──────────────────┐   |
                                                                         | │ K8s Deployment   │   |
                                                                         | │ Pod: myapp-xyz   │   |
                                                                         | │ Image: SHA256... │   |
                                                                         | │ Env: PROD        │   |
                                                                         | │ Status: Running  │   |
                                                                         | └──────────────────┘   |
                                                                         +------------------------+
                                                                                    │
                                         +------------------------------------------+
                                         │
                                         ▼
+------------------+                  +------------------------+
|  Rollback        | <─────────────── |  Release History       |
|  If Failure      |  Previous Ver   |  v2.3.0-prod (stable)  |
+------------------+                  |  v2.3.1-prod (current) |
                                      +------------------------+

=====================================================================================================
```

### 3. 심층 동작 원리 (3단계 상세 메커니즘)

**① 빌드 단계 (Build Stage) - 불변 아티팩트 생성**
빌드 단계는 코드베이스의 특정 커밋(snapshot)을 입력으로 받아, 실행 환경에 독립적인 불변(Immutable) 아티팩트를 생성합니다. 핵심 원칙은:
- **의존성 고정 (Vendoring)**: package-lock.json, pom.xml의 해시값을 기준으로 정확한 버전의 라이브러리를 다운로드합니다. 이는 "내 컴퓨터에서는 되는데" 문제를 근절합니다.
- **결정론적 빌드 (Reproducible Build)**: 같은 커밋에서 빌드하면 항상 동일한 SHA256 해시를 가진 이미지가 생성되어야 합니다. 타임스탬프 등 비결정적 요소를 제거합니다.
- **빌드 캐싱 (Build Cache)**: Docker 레이어 캐시, Maven .m2 리포지토리를 활용하여 증분 빌드 속도를 최적화합니다.

**② 릴리스 단계 (Release Stage) - 환경 특화 설정 주입**
릴리스 단계는 빌드된 불변 아티팩트와 환경별 설정(Config)을 결합하여 배포 가능한 단위를 만듭니다. 이때 핵심은:
- **설정의 외부화 (Externalized Configuration)**: DB 연결 문자열, API 키 등은 코드에 하드코딩되지 않고, 릴리스 시점에 환경 변수 또는 볼트(Vault)에서 주입됩니다.
- **불변 릴리스 ID 생성**: "myapp:v2.3.1-prod-20240515-a1b2c3d"와 같이 버전+환경+타임스탬프+커밋해시를 조합한 고유 ID를 부여합니다. 이 ID로 언제든 동일한 릴리스를 재현할 수 있습니다.
- **시크릿 주입 (Secret Injection)**: DB 패스워드, API Secret은 릴리스 시점에 HashiCorp Vault 등에서 동적으로 조회하여 아티팩트에 포함시키지 않고 런타임에만 메모리에 로드합니다.

**③ 실행 단계 (Run Stage) - 프로세스 구동 및 관찰**
실행 단계는 릴리스된 패키지를 실제 프로세스로 시작합니다. 이 단계에서는:
- **무상태 실행 (Stateless Execution)**: 실행 중인 프로세스는 언제든 종료되고 새 프로세스로 교체될 수 있어야 합니다. 상태는 외부 DB/캐시에 저장됩니다.
- **우아한 종료 (Graceful Shutdown)**: SIGTERM 신호 수신 시 진행 중인 요청을 완료하고 정리 작업을 수행한 후 종료합니다.
- **건강 확인 (Health Checks)**: Liveness Probe(프로세스 생존 여부), Readiness Probe(트래픽 수용 준비 여부)를 통해 오케스트레이터가 프로세스 상태를 모니터링합니다.

### 4. 핵심 알고리즘 및 실무 코드 예시

**GitOps 기반 Build-Release-Run 자동화 (GitHub Actions 예시)**

```yaml
# .github/workflows/build-release-run.yml
name: Build-Release-Run Pipeline

on:
  push:
    branches: [main]

jobs:
  # ============== BUILD STAGE ==============
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.build.outputs.tag }}
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for versioning

      - name: Setup Build Cache
        uses: actions/cache@v3
        with:
          path: |
            ~/.m2/repository
            ~/.npm
          key: ${{ runner.os }}-deps-${{ hashFiles('**/pom.xml', '**/package-lock.json') }}

      - name: Build Docker Image (Immutable Artifact)
        id: build
        run: |
          # Generate deterministic tag from commit SHA
          COMMIT_SHA=$(git rev-parse --short HEAD)
          IMAGE_TAG="myapp:${COMMIT_SHA}"

          # Build with --no-cache for reproducibility in prod
          docker build -t $IMAGE_TAG .
          echo "tag=$IMAGE_TAG" >> $GITHUB_OUTPUT

      - name: Push to Registry
        run: |
          docker push ${{ steps.build.outputs.tag }}

  # ============== RELEASE STAGE ==============
  release:
    needs: build
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval gate
    steps:
      - name: Checkout Config Repo (GitOps)
        uses: actions/checkout@v4
        with:
          repository: org/k8s-configs
          token: ${{ secrets.CONFIG_REPO_TOKEN }}

      - name: Generate Release Manifest
        run: |
          RELEASE_ID="v$(date +%Y%m%d)-${{ github.sha }}"

          # Inject immutable image tag into Helm values
          cat > values-prod.yaml << EOF
          image:
            tag: ${{ needs.build.outputs.tag }}
          releaseId: $RELEASE_ID
          configHash: $(echo -n "${{ secrets.PROD_CONFIG }}" | sha256sum | cut -d' ' -f1)
          EOF

          # Commit release version to GitOps repo
          git add values-prod.yaml
          git commit -m "release: $RELEASE_ID"
          git push

          echo "Release $RELEASE_ID created and pushed to GitOps"

  # ============== RUN STAGE (ArgoCD Sync) ==============
  # ArgoCD automatically detects GitOps repo change and syncs to cluster
```

**Kubernetes Deployment Manifest (Run Stage)**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app.kubernetes.io/version: "v2.3.1-prod-20240515"  # Release ID
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:a1b2c3d  # Immutable Build Artifact
        env:
        - name: RELEASE_ID
          valueFrom:
            fieldRef:
              fieldPath: metadata.labels['app.kubernetes.io/version']
        # Config injected at runtime via ConfigMap/Secret
        envFrom:
        - configMapRef:
            name: myapp-config-prod
        - secretRef:
            name: myapp-secrets-prod
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]  # Graceful shutdown
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 전통적 배포 vs Build-Release-Run 분리

| 평가 지표 | 전통적 배포 (Monolithic Pipeline) | Build-Release-Run 분리 | GitOps + Build-Release-Run |
| :--- | :--- | :--- | :--- |
| **아티팩트 불변성** | 환경마다 재빌드 (Non-reproducible) | 빌드 1회, 환경별 릴리스 (Immutable) | 동일 + Git 기반 추적 |
| **설정 관리** | 코드에 하드코딩 또는 빌드 시 포함 | 릴리스 시점 주입 (Late Binding) | GitOps Config Repo에서 선언적 관리 |
| **롤백 복잡도** | 코드+설정+빌드 모두 재실행 필요 | 이전 릴리스 ID로 즉시 전환 | `git revert` 한 줄로 전체 환경 롤백 |
| **감사 추적 (Audit)** | 로그에서 수동 검색 필요 | 각 릴리스마다 고유 ID 부여 | Git 커밋 히스토리 = 감사 로그 |
| **환경 일관성** | Dev/Staging/Prod 빌드 결과 불일치 | 동일 아티팩트, 설정만 상이 | 환경별 values.yaml로 파라미터화 |
| **장애 재현** | "그때 어떤 설정이었는지 모름" | Release ID로 정확한 스냅샷 복원 | GitOps 커밋으로 100% 재현 가능 |

### 2. 과목 융합 관점 분석

**Build-Release-Run + 컨테이너 보안 (DevSecOps)**
- 빌드 단계에서 SAST(정적 분석), 컨테이너 이미지 스캐닝(Trivy)을 수행하여 취약점이 있는 아티팩트가 릴리스되지 않도록 게이트(Quality Gate)를 설치합니다.
- 릴리스 단계에서 이미지 서명(Cosign, Notary)을 통해 빌드된 아티팩트의 무결성을 검증하고, 서명되지 않은 이미지는 프로덕션 실행 단계에서 차단합니다(Admission Controller).

**Build-Release-Run + 옵저버빌리티 (SRE)**
- 실행 단계의 모든 로그와 메트릭에 `release_id` 레이블을 포함시켜, 장애 발생 시 어떤 릴리스에서 문제가 발생했는지 즉시 식별합니다.
- 릴리스 간의 메트릭 비교(Regression Analysis)를 통해 신규 릴리스가 성능 저하를 일으키는지 자동 감지합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 프로덕션 장애 발생 시 즉각적 롤백 요구**
- **문제점**: 프로덕션 환경에서 신규 배포 후 5xx 에러율이 급증했습니다. 전통적 방식에서는 이전 코드를 체크아웃하여 재빌드하고 설정을 다시 적용해야 하므로 롤백에 30분 이상 소요됩니다.
- **기술사 판단 (전략)**: Build-Release-Run 분리 환경에서는 ArgoCD UI 또는 `argocd app rollback` 명령 한 번으로 이전 릴리스 ID를 가리키도록 변경합니다. 빌드된 아티팩트는 이미 존재하므로, 설정만 이전 버전으로 되돌리면 되어 롤백이 10초 이내에 완료됩니다.

**[상황 B] 다중 환경(Dev/Staging/Prod) 배포 자동화**
- **문제점**: 각 환경마다 DB 엔드포인트, 로깅 레벨, 기능 토글이 다릅니다. 코드를 환경마다 수정하여 빌드하는 것은 비효율적입니다.
- **기술사 판단 (전략)**: 단일 빌드 아티팩트(`myapp:abc123`)를 생성한 후, 릴리스 단계에서 `values-dev.yaml`, `values-staging.yaml`, `values-prod.yaml`을 각각 주입하여 세 개의 릴리스를 생성합니다. 이를 통해 "Build Once, Deploy Anywhere"를 실현합니다.

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] 아티팩트 리포지토리(ECR, Artifactory) 용량 관리: 불변 이미지가 무한히 쌓이지 않도록 Retention Policy(예: 90일 이전 이미지 삭제) 설정
- [ ] 빌드 캐시 무효화 전략: 의존성 업데이트 시 캐시된 레이어가 문제를 일으키지 않도록 주기적인 캐시 클리어
- [ ] 시크릿 로테이션(Secret Rotation): 릴리스 시점에 주입된 시크릿이 만료되지 않도록 Vault 동적 시크릿 사용

**운영/보안적 고려사항**
- [ ] SBOM(Software Bill of Materials) 생성: 각 빌드 산출물에 포함된 오픈소스 구성 요소 명세를 생성하여 공급망 보안 강화
- [ ] 이미지 서명 검증: 실행 단계(K8s Admission Controller)에서 서명되지 않은 이미지 배포 차단

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: 릴리스 단계에서 코드 수정**
- 릴리스 단계에서 sed/awk로 소스 코드를 치환하거나 설정 파일을 수정하는 것은 Build-Release-Run 분리를 깨는 행위입니다. 모든 수정은 빌드 단계 이전(코드 커밋)에서 이루어져야 합니다.

**안티패턴 2: 실행 단계에서 설정 파일 수정**
- 실행 중인 컨테이너에 `kubectl exec`로 접속하여 설정을 수정하는 것은 불변 인프라 원칙 위반입니다. 모든 설정 변경은 새 릴리스를 통해 이루어져야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 레거시 환경 (AS-IS) | Build-Release-Run 적용 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **평균 롤백 시간** | 30분~2시간 (재빌드 필요) | 10초~1분 (릴리스 전환만) | **롤백 시간 99% 단축** |
| **장애 재현률** | 60% (설정 누락/불일치) | 100% (Release ID로 정확한 복원) | **재현 불가 문제 제로화** |
| **감사 대응 시간** | 수 시간 (로그 검색) | 즉시 (Git 커밋 히스토리) | **컴플라이언스 비용 절감** |
| **배포 실패율** | 15% (환경 불일치) | 3% (동일 아티팩트 사용) | **배포 안정성 5배 향상** |

### 2. 미래 전망 및 진화 방향
- **AI 기반 릴리스 최적화**: 머신러닝이 이전 릴리스들의 성능 데이터를 학습하여, 새 릴리스가 성능 저하를 일으킬 확률을 예측하고 자동으로 배포 승인/거부를 판단하는 "AI Release Manager"로 진화할 것입니다.
- **WASM(WebAssembly) 기반 Build-Run 통합**: 컨테이너 이미지 대신 WASM 모듈로 빌드 산출물을 패키징하면, 빌드-실행 간격이 밀리초 단위로 축소되어 서버리스 수준의 빠른 배포가 가능해질 것입니다.

### 3. 참고 표준/가이드
- **12-Factor App (12factor.net)**: Build-Release-Run 분리의 원천 방법론
- **NIST SP 800-53 (CM-3)**: 변경 관리를 위한 구성 제어 표준
- **SOC 2 Type II**: 변경 사항 추적 및 승인 프로세스 요구사항

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[12-Factor App](@/studynotes/15_devops_sre/1_sre/twelve_factor_app.md)**: Build-Release-Run 분리를 포함한 클라우드 네이티브 앱 설계 12원칙
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/3_automation/continuous_integration.md)**: Build-Release-Run을 자동화하는 지속적 통합/배포 인프라
- **[GitOps](@/studynotes/15_devops_sre/3_automation/cicd_gitops.md)**: 릴리스 단계를 Git 커밋 기반으로 관리하는 선언적 배포 패러다임
- **[컨테이너 이미지](@/studynotes/13_cloud_architecture/1_native/docker.md)**: 빌드 단계의 핵심 산출물인 불변 실행 환경
- **[구성 관리](@/studynotes/15_devops_sre/1_sre/config_management.md)**: 릴리스 단계에서 주입되는 설정의 외부화 원칙

---

## 👶 어린이를 위한 3줄 비유 설명
1. 레고로 멋진 로봇을 만들 때, **'설계도대로 조립하기(빌드)'**, **'색깔 입히기(릴리스)'**, **'가지고 놀기(실행)'**는 각각 다른 단계예요!
2. 한 번 만든 로봇은 다시 뜯어고치지 않고, 색깔만 바꿔서 여러 친구들한테 줄 수 있어요. 그래서 어떤 로봇이 문제가 생겨도 "이건 빨간 로봇이었지!" 하고 금방 찾을 수 있답니다.
3. 덕분에 로봇을 만드는 시간은 줄어들고, 고장 나도 금방 이전 로봇으로 바꿀 수 있어서 모두가 행복해요!
