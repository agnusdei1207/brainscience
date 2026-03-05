+++
title = "DevSecOps (데브섹옵스)"
description = "보안을 소프트웨어 개발 수명 주기(SDLC)의 모든 단계에 내재화하여 배포 속도를 희생하지 않으면서 보안을 보장하는 데브옵스의 보안 확장 패러다임"
date = 2024-05-15
[taxonomies]
tags = ["DevSecOps", "Security", "Shift-Left", "SAST", "DAST", "SCA", "CI/CD"]
+++

# DevSecOps (데브섹옵스)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 보안(Security)을 개발(Dev)과 운영(Ops)의 협업 문화인 DevOps에 내재화(Embed)하여, 보안이 개발 속도를 늦추는 장애물이 아니라 CI/CD 파이프라인의 자동화된 품질 게이트(Quality Gate)가 되게 하는 '보안의 모든 단계 통합' 접근법입니다.
> 2. **가치**: 전통적인 '배포 직전 보안 감사' 병목 현상을 제거하고, SAST/SCA/DAST 자동화 스캔을 통해 보안 취약점을 조기 발견하여 프로덕션 보안 사고를 80% 이상 감소시킵니다.
> 3. **융합**: 시프트 레프트(Shift-Left), SBOM(소프트웨어 자재 명세서), 컨테이너 이미지 스캐닝, IaC 보안 검증과 결합하여 '보안은 모두의 책임(Security is Everyone's Responsibility)' 문화를 실현합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**DevSecOps(데브섹옵스)**는 Development(개발), Security(보안), Operations(운영)의 합성어로, 보안을 소프트웨어 개발 수명 주기(SDLC)의 **모든 단계**에 통합하는 실천법, 문화, 자동화 도구의 집합입니다. 전통적으로 보안은 개발 완료 후 별도의 '보안 감사' 단계에서 수행되어 배포를 지연시키는 병목(Bottleneck)이었으나, DevSecOps는 보안 검증을 **CI/CD 파이프라인 내에 자동화된 단계**로 만들어 개발 속도를 유지하면서도 보안을 보장합니다. 핵심 원칙은:
- **Security as Code**: 보안 정책과 규칙을 코드로 정의하여 버전 관리
- **Shift-Left Security**: 보안 검증을 개발 초기 단계로 이동
- **Automated Security Testing**: SAST, SCA, DAST 등 자동화된 보안 스캔
- **Continuous Security**: 지속적 통합/배포의 일부로 지속적 보안 검증

### 💡 2. 구체적인 일상생활 비유
자동차 조립 공장을 상상해 보세요. 전통적 방식은 완성된 자동차를 마지막에 '안전 검사소'로 보내서 충돌 테스트, 브레이크 테스트를 합니다. 문제가 발견되면 공장 라인을 멈추고 수정해야 합니다. **DevSecOps**는 조립 라인의 모든 단계에서 자동으로 안전 검사를 수행하는 것입니다. 엔진을 장착할 때 자동으로 배기가스 센서가 검사하고, 브레이크를 설치할 때 압력 테스트가 자동 수행됩니다. 문제는 발생 즉시 발견되어 라인을 멈추지 않고도 안전한 자동차가 완성됩니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (보안 감사 병목과 보안 부채)**:
   폭포수 모델에서는 개발이 90% 완료된 시점에 보안 팀이 개입했습니다. 수백 개의 취약점이 발견되어 개발 일정이 수개월 지연되거나, 일정 압박으로 취약점이 방치되어 '보안 부채(Security Debt)'가 쌓였습니다. 개발자는 보안 팀을 "배포를 막는 적"으로 인식했습니다.

2. **혁신적 패러다임 변화의 시작**:
   2012년 Gartner의 Neil MacDonald가 "DevOps는 보안을 포함해야 한다"고 주장하면서 DevSecOps라는 용어가 등장했습니다. 2010년대 중반 AWS, Netflix, Google 등이 "보안을 개발자 도구에 통합"하는 실천법을 공유하며 산업 표준으로 자리잡았습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   SolarWinds(2020), Log4j(2021) 등 대규모 공급망 공격이 발생하면서 소프트웨어 보안의 중요성이 극대화되었습니다. 미국 행정명령 14028(SBOM 의무화), EU 사이버 복원력 법안(CRA) 등 규정 준수 요구사항이 강화되어 DevSecOps는 선택이 아닌 필수가 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 관련 도구/기술 | SDLC 단계 |
| :--- | :--- | :--- | :--- | :--- |
| **SAST (Static App Sec Testing)** | 소스코드 정적 보안 분석 | 제어 흐름, 데이터 흥름 분석으로 SQLi, XSS 탐지 | SonarQube, Checkmarx, Semgrep | 코딩/빌드 |
| **SCA (Software Comp Analysis)** | 오픈소스 의존성 취약점 스캔 | CVE DB와 비교하여 알려진 취약점 탐지 | Snyk, OWASP Dep-Check, Trivy | 빌드 |
| **DAST (Dynamic App Sec Testing)** | 실행 중인 앱의 동적 보안 테스트 | 웹 스파이더, 퍼징 공격으로 런타임 취약점 탐지 | OWASP ZAP, Burp Suite | 스테이징 |
| **IaC Security Scanning** | 인프라 코드 보안 검증 | Terraform/K8s YAML의 잘못된 설정 탐지 | tfsec, Checkov, Kics | 커밋/빌드 |
| **Container Image Scanning** | 컨테이너 이미지 취약점 스캔 | 베이스 이미지 OS 패키지, 앱 라이브러리 검사 | Trivy, Clair, Snyk Container | 빌드 |
| **Secrets Scanning** | 코드 내 하드코딩된 시크릿 탐지 | 정규식, ML 기반 API 키/패스워드 탐지 | GitLeaks, TruffleHog | 커밋 |
| **SBOM Generation** | 소프트웨어 구성 요소 명세서 생성 | SPDX/CycloneDX 형식으로 의존성 목록화 | Syft, sbom-tool | 빌드 |

### 2. 정교한 구조 다이어그램: DevSecOps 파이프라인

```text
=====================================================================================================
                      [ DevSecOps Pipeline - Security at Every Stage ]
=====================================================================================================

  [ DEVELOP ]         [ BUILD ]           [ TEST ]            [ RELEASE ]         [ DEPLOY ]
       │                  │                   │                    │                   │
       ▼                  ▼                   ▼                    ▼                   ▼

┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ IDE Plugins │   │ CI Server   │   │ Test Env    │   │ Stage Env   │   │ Production  │
│             │   │             │   │             │   │             │   │             │
│ [1] Pre-    │   │ [3] SAST    │   │ [6] DAST    │   │ [8] Pen     │   │ [10] RASP   │
│     commit  │   │     Scan    │   │     Scan    │   │     Test    │   │     (Runtime│
│     Secrets │   │ [4] SCA     │   │ [7] API     │   │ [9] Compliance│  │     Protect)│
│     Scan    │   │     Scan    │   │     Security│   │     Scan    │   │ [11] CSPM   │
│ [2] IDE-    │   │ [5] Image   │   │     Test    │   │             │   │     (Cloud  │
│     Security│   │     Scan    │   │             │   │             │   │     Posture)│
│     Linting │   │             │   │             │   │             │   │             │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │                 │                 │
       │                 │                 │                 │                 │
       ▼                 ▼                 ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           [ Security Quality Gates ]                                    │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐ │
│  │ Gate 1 (Commit):    No secrets in code ✓                                          │ │
│  │ Gate 2 (Build):     SAST: 0 Critical, 0 High ✓                                    │ │
│  │                    SCA:  No Critical CVEs ✓                                        │ │
│  │                    Image: No Critical vulnerabilities ✓                            │ │
│  │ Gate 3 (Test):      DAST: 0 High severity issues ✓                                │ │
│  │ Gate 4 (Release):   Compliance: All checks passed ✓                               │ │
│  │ Gate 5 (Runtime):   RASP active, CSPM monitoring ✓                                │ │
│  └───────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  Any gate FAIL → Pipeline BLOCKED → Fix required before proceeding                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
       │                 │                 │                 │                 │
       ▼                 ▼                 ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           [ Security Observability ]                                    │
│                                                                                         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                  │
│  │ Vulnerability│   │ Security    │   │ Compliance  │   │ Threat      │                  │
│  │ Dashboard    │   │ Metrics     │   │ Reports     │   │ Intelligence│                  │
│  │ (DefectDojo) │   │ (Prometheus)│   │ (SonarQube) │   │ (SIEM)      │                  │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

=====================================================================================================
```

### 3. 심층 동작 원리 (보안 게이트 메커니즘)

**① 커밋 단계 보안 (Pre-commit Security)**
개발자가 `git commit`을 실행하면 pre-commit hook이 자동으로 실행됩니다:
- **Secrets Scanning**: API 키, 비밀번호, 토큰이 포함되어 있는지 정규식으로 검사
- **SAST Lite**: 간단한 정적 분석 (빠른 피드백을 위해 전체 분석은 CI에서 수행)
- **IaC Linting**: Terraform/K8s YAML의 기본 문법 및 보안 규칙 검사

발견된 문제는 커밋을 차단(Block)하고 개발자에게 즉시 피드백을 제공합니다.

**② 빌드 단계 보안 (CI Security Gates)**
PR이 생성되면 CI 파이프라인이 실행됩니다:
- **SAST (Static Application Security Testing)**: 소스코드를 컴파일하지 않고 분석. SQL Injection, XSS, 경로 traversal 등의 패턴 탐지. 제어 흐름 분석(Control Flow Analysis)으로 데이터가 검증 없이 사용자 입력에서 위험 함수로 전달되는지 추적.
- **SCA (Software Composition Analysis)**: `package.json`, `pom.xml`에 선언된 모든 의존성을 NVD(National Vulnerability Database)의 CVE와 교차 검색. Known vulnerabilities가 있으면 Critical/High는 차단, Medium/Low는 경고.
- **Container Image Scanning**: Docker 이미지의 각 레이어를 스캔. 베이스 이미지(alpine, ubuntu)의 OS 패키지와 앱 라이브러리의 취약점 탐지.

**③ 테스트/스테이징 단계 보안 (DAST & Pen Testing)**
애플리케이션이 스테이징 환경에 배포되면:
- **DAST (Dynamic Application Security Testing)**: 실행 중인 앱에 실제 HTTP 요청을 보내 취약점 탐지. 인증 우회, 세션 관리 취약점, CSRF 토큰 누락 등 런타임에서만 발견되는 문제 식별.
- **API Security Testing**: OpenAPI(Swagger) 스펙 기반으로 자동으로 API 엔드포인트 테스트. 잘못된 입력 검증, Rate Limiting 미작동 등 탐지.

**④ 런타임 보안 (Production Security)**
프로덕션 배포 후에도 보안은 지속됩니다:
- **RASP (Runtime Application Self-Protection)**: 애플리케이션 내부에서 실행되는 에이전트가 실시간 공격 탐지 및 차단. SQL Injection 시도가 들어오면 앱 수준에서 차단.
- **CSPM (Cloud Security Posture Management)**: 클라우드 인프라 설정을 지속 감시. S3 버킷 퍼블릭 오픈, Security Group 과도한 개방 등 탐지.

### 4. 핵심 알고리즘 및 실무 코드 예시

**DevSecOps CI/CD 파이프라인 (GitHub Actions)**

```yaml
# .github/workflows/devsecops.yml
name: DevSecOps Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # ==================== SECURITY GATE 1: Secrets Scan ====================
  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for secret detection

      - name: Detect Secrets (Gitleaks)
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}

  # ==================== SECURITY GATE 2: SAST ====================
  sast-scan:
    runs-on: ubuntu-latest
    needs: secrets-scan
    steps:
      - uses: actions/checkout@v4

      - name: SonarCloud Scan (SAST)
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        with:
          args: >
            -Dsonar.qualitygate.wait=true
            -Dsonar.security.hotspots.review.status=reviewed

      - name: Semgrep Scan (Lightweight SAST)
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten

  # ==================== SECURITY GATE 3: SCA ====================
  sca-scan:
    runs-on: ubuntu-latest
    needs: secrets-scan
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Run Snyk SCA
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: test
          args: >
            --severity-threshold=high
            --fail-on=all
            --sarif-file-output=snyk.sarif

      - name: Upload Snyk Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: snyk.sarif

  # ==================== SECURITY GATE 4: Container Scan ====================
  container-scan:
    runs-on: ubuntu-latest
    needs: [sast-scan, sca-scan]
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker Image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Run Trivy Image Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fail on vulnerabilities

      - name: Upload Trivy Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  # ==================== SECURITY GATE 5: IaC Scan ====================
  iac-scan:
    runs-on: ubuntu-latest
    needs: secrets-scan
    steps:
      - uses: actions/checkout@v4

      - name: Run Checkov IaC Scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: ./terraform
          framework: terraform
          output_format: sarif
          output_file_path: results.sarif
          soft_fail: false  # Fail on policy violations

  # ==================== SECURITY GATE 6: DAST ====================
  dast-scan:
    runs-on: ubuntu-latest
    needs: [container-scan]
    steps:
      - name: Deploy to Staging
        run: kubectl apply -f k8s/staging.yaml

      - name: Run OWASP ZAP DAST Scan
        uses: zaproxy/action-full-scan@v0.7.0
        with:
          target: 'https://staging.myapp.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'  # Include all alerts
          fail_action: true

  # ==================== SBOM Generation ====================
  sbom:
    runs-on: ubuntu-latest
    needs: [sast-scan, sca-scan, container-scan]
    steps:
      - uses: actions/checkout@v4

      - name: Generate SBOM (Syft)
        uses: anchore/sbom-action@v0
        with:
          image: myapp:${{ github.sha }}
          format: spdx-json
          output-file: sbom.spdx.json

      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.spdx.json
```

**IaC 보안 정책 (Checkov/OPA)**

```python
# checkov/custom_checks/s3_bucket_encryption.py
from checkov.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck

class S3BucketEncryption(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure S3 bucket has encryption enabled"
        id = "CKV_CUSTOM_001"
        supported_resources = ['aws_s3_bucket']
        categories = ['encryption']
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        # Check if server_side_encryption_configuration exists
        if 'server_side_encryption_configuration' in conf:
            return CheckResult.PASSED
        return CheckResult.FAILED

check = S3BucketEncryption()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 보안 접근법 비교

| 평가 지표 | 전통적 보안 감사 | DevSecOps | 차이점 |
| :--- | :--- | :--- | :--- |
| **개입 시점** | 개발 완료 후 (SDLC 후반) | 개발 전 과정 (SDLC 초기부터) | Shift-Left |
| **수행 주체** | 별도 보안 팀 | 모든 개발자 (자동화 도구 지원) | 책임 분산 |
| **검증 빈도** | 연 1~2회 정기 감사 | 모든 커밋/PR마다 자동 검증 | 지속적 검증 |
| **피드백 속도** | 주~월 단위 | 분 단위 | 빠른 피드백 |
| **배포 영향** | 병목 발생 (수주 지연) | 병목 없음 (자동화된 게이트) | 속도 유지 |
| **취약점 발견율** | 낮음 (샘플링 검사) | 높음 (100% 코드 커버) | 완전 검증 |

### 2. 과목 융합 관점 분석

**DevSecOps + 컨테이너 보안 (Container Security)**
- 컨테이너 이미지는 빌드 시점에 스캔되고, 런타임에는 Seccomp/AppArmor 프로파일로 권한 제한, 네트워크는 Network Policy로 격리됩니다. 전체 컨테이너 수명 주기에 보안이 통합됩니다.

**DevSecOps + 클라우드 보안 (Cloud Security)**
- IaC(Infrastructure as Code) 스캔으로 인프라 설정 오류를 사전 탐지하고, CSPM으로 런타임 클라우드 설정을 지속 감시합니다. CSPM과 CI/CD가 연동하여 drift 발생 시 자동 수정합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 신규 프로젝트에 DevSecOps 도입**
- **문제점**: 스타트업에서 신규 서비스를 개발하는데 보안 팀이 없습니다. 어떤 도구를 먼저 도입해야 할까요?
- **기술사 판단 (전략)**: ① Secrets Scanning (GitLeaks) - 가장 빠른 승인 효과 ② SCA (Snyk/Dependabot) - 공급망 공격 방어 ③ SAST (Semgrep) - 경량화된 도구로 시작. 순차적 도입으로 개발자 저항 최소화.

**[상황 B] 레거시 시스템의 보안 부채 해결**
- **문제점**: 기존 시스템에 수백 개의 취약점이 있는데, DevSecOps를 도입하면 모든 배포가 차단됩니다.
- **기술사 판단 (전략)**: 'Grandfathering' 전략 적용. 기존 코드는 예외 처리하고, 신규 코드부터 게이트 적용. 취약점은 심각도별로 우선순위를 매겨 순차 수정. 'Security Quality Gate'를 점진적으로 강화 (처음엔 Critical만 차단 → High 추가 → Medium 추가).

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] 파이프라인 실행 시간: 보안 스캔이 개발 속도를 저하하지 않도록 병렬 실행 및 캐싱 활용
- [ ] 오탐지(False Positive) 관리: SAST 도구는 오탐지가 많을 수 있음, 튜닝 필수
- [ ] 취약점 관리 프로세스: 발견된 취약점을 추적하고 수정하는 Jira 연동 워크플로우

**문화적 고려사항**
- [ ] 개발자 교육: "보안은 보안 팀의 책임" → "보안은 모두의 책임" 인식 변화
- [ ] 보안 챔피언(Security Champion): 각 개발 팀에 보안 전문성을 가진 멤버 지정
- [ ] 책임 없는 문화(Blameless Culture): 취약점 발견 시 비난하지 않고 시스템 개선에 집중

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: 보안 팀 없이 DevSecOps 도구만 도입**
- 도구는 자동화를 돕지만, 보안 정책 수립, 오탐지 분석, 취약점 대응 전략은 보안 전문가가 필요합니다. 최소한 Security Champion 또는 파트타임 보안 담당자가 있어야 합니다.

**안티패턴 2: 너무 엄격한 게이트로 개발 마비**
- "Critical 취약점 0개" 요구사항은 현실적으로 불가능할 수 있습니다. 위험 기반(Risk-based) 접근으로 "Critical + Exploitable + Internet-facing"만 차단하는 식으로 현실적 기준 설정이 필요합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 전통적 보안 (AS-IS) | DevSecOps (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **취약점 발견 시점** | 프로덕션 배포 후 | 코딩 단계 | **조기 발견 90%** |
| **보안 수정 비용** | 100x (프로덕션) | 1x (코딩 단계) | **비용 99% 절감** |
| **배포 속도** | 보안 감사로 지연 | 자동화로 속도 유지 | **병목 제거** |
| **보안 사고율** | 15% (연간) | 3% (연간) | **사고 80% 감소** |
| **규정 준수** | 수동 증빙 | 자동화된 증빙 | **감사 비용 절감** |

### 2. 미래 전망 및 진화 방향
- **AI 기반 보안 분석**: 머신러닝이 코드 패턴을 학습하여 0-day 취약점을 예측하고, 자동으로 수정 코드를 제안하는 "AI Security Copilot"이 등장할 것입니다.
- **공급망 보안 강화**: SBOM 의무화, SLSA(Supply-chain Levels for Software Artifacts) 프레임워크 도입으로 소프트웨어 공급망의 투명성과 무결성이 강화될 것입니다.

### 3. 참고 표준/가이드
- **NIST SP 800-218 (SSDF)**: Secure Software Development Framework
- **OWASP DevSecOps Guideline**: DevSecOps 구현 가이드
- **SLSA (Supply-chain Levels for Software Artifacts)**: Google의 공급망 보안 프레임워크
- **US Executive Order 14028**: 연방정부 소프트웨어 공급망 보안 강화 (SBOM 의무화)

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[시프트 레프트](@/studynotes/15_devops_sre/1_sre/45_shift_left.md)**: DevSecOps의 핵심 철학
- **[SAST/DAST](@/studynotes/15_devops_sre/5_devsecops/sast_dast.md)**: 정적/동적 보안 분석 도구
- **[SBOM](@/studynotes/15_devops_sre/5_devsecops/sbom.md)**: 소프트웨어 자재 명세서
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/3_automation/continuous_integration.md)**: DevSecOps 자동화 인프라
- **[컨테이너 보안](@/studynotes/15_devops_sre/5_devsecops/container_security.md)**: 이미지 스캔 및 런타임 보호

---

## 👶 어린이를 위한 3줄 비유 설명
1. 집을 지을 때 **나중에 한 번에 검사하면 문제가 크지만**, 매일매일 조금씩 검사하면 문제가 생겨도 바로 고칠 수 있어요!
2. DevSecOps는 건축가가 벽돌을 쌓을 때마다 "이 벽돌 튼튼해?", "이 문 잠겨 있어?" 하고 자동으로 물어보는 로봇 같아요.
3. 덕분에 나쁜 사람이 들어올 틈을 미리미리 막을 수 있어서, 집이 다 지어지고 나서 "앗! 문이 없네?" 하고 놀라는 일이 없답니다!
