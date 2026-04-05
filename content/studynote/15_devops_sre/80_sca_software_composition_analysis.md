+++
weight = 80
title = "80. 패키지 취약점 스캐닝 (SCA, Software Composition Analysis)"
description = "소스코드에 포함된 오픈소스 라이브러리의 알려진 취약점(CVE)과 라이선스 충돌 위험을 자동으로 검사하는 SCA 도구와 CI/CD 파이프라인 통합 방법"
date = "2026-04-05"

[taxonomies]
tags = ["DevOps", "SCA", "Security", "CVE", "Dependency Scanning", "DevSecOps"]
categories = ["studynote-devops-sre"]
+++

# 80. 패키지 취약점 스캐닝 (SCA, Software Composition Analysis)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: SCA(Software Composition Analysis)는 프로젝트가 사용하는 외부 오픈소스 라이브러리와 그 transitive dependencies(전이적 의존성) 전체를 탐색하여 알려진 보안 취약점(CVE)과 라이선스 위반을 자동으로 스캔하는 기법이다.
> 2. **가치**: 현대 애플리케이션의 80~90%는 오픈소스 코드(Dependencies)로 구성되므로, 이들의 취약점이 곧 애플리케이션의 취약점이 된다. SCA는 이 '전면 야외전'에서 조직을 보호하는 첫 번째 방어선이다.
> 3. **융합**: SCA는 CI/CD 파이프라인(Shift-Left)의 빌드 단계에 내장되어,脆弱한 라이브러리가 프로덕션에 배포되는 것을 자동으로 차단하며, SBOM(Software Bill of Materials) 생성으로 공급망 보안 규제 준수의 증거로 활용된다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

오픈소스 소프트웨어(OSS)는 현대 소프트웨어 개발의 근간이다. 개발자가 직접 작성하는 코드보다 npm, PyPI, Maven Central 등에서 내려받는 외부 라이브러리(Dependencies)로 구성되는 코드가 압도적으로 많다. 문제는 이 오픈소스 라이브러리가 항상 안전하다는 가정에 있다. 실제로 Log4j(CVE-2021-44228), OpenSSL Heartbleed, Spring4Shell(CVE-2022-22965) 같은 치명적 취약점이 오픈소스에서 비롯되었으며, 한 번 발견되면 전 세계 수천 개의 애플리케이션에 즉각적 영향을 미친다.

SCA는 이 현실을 인식하고, 프로젝트가 사용하는 모든 외부 구성 요소의 취약점을 식별하는 자동화된 보안 검사 도구이다. 핵심은 개발자가 "직접 의존하는 라이브러리"만 관리할 뿐, "그 라이브러리가 의존하는 또 다른 라이브러리"까지 추적하지 않는 전이적 의존성(Transitive Dependency) 문제를 해결한다는 점이다.

```text
[SCA가 탐지하는 의존성 그래프]

[자신의 프로젝트 코드]  ←  직접 작성한 코드
       │
       ├── package.json / requirements.txt
       │         │
       │    [직접 의존성 (Direct Dependencies)]
       │         │
       │    lodash@4.17.20  ← ✅ 개발자가 명시적으로 설치
       │         │
       │    lodash@4.17.20 → [전이적 의존성 (Transitive Dependencies)]
       │                      │
       │                 ├─ deep-equal@1.0.1  ← ❓ lodash가 묵시적으로 사용
       │                 └─ get-random-values@1.0.0  ← CVE-2023-XXXXX 취약!
       │
       ▼
[SCA 스캔 결과: 1개의 치명적 CVE 발견, 3개의 중대한 라이선스 위반 탐지]
```

SCA의 필요성은 단순히 보안 취약점 탐지를 넘어서 **라이선스 컴플라이언스** 영역까지 확장된다. GPL 라이선스의 오픈소스를 상업적 제품에 사용하면 저작권 위반 소송이 가능하며, LGPL 라이선스의 경우 동적 링크를 사용하면linking 예외가 적용되지만 정적 링크는 위반이 될 수 있다. SCA 도구는 이러한 라이선스 위험까지 포착하여 법무팀에警报한다.

**📢 섹션 요약 비유**: 친구에게 음식을 만들어 주려는데, 재료 표를 확인해보니 고추(직접 의존성)는 신선하지만, 그 고추를 키운 비료(전이적 의존성)에 유해한 물질이 들어있음을 알 수 없는 것과 같습니다. SCA는 비료까지 추적하여 안전한 음식(애플리케이션) 조리 여부를 판단하는 식품 위생 검사원입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

SCA 도구의 동작 원리는 크게 세 단계로 나뉜다. 의존성 탐지(Discovery), 취약점 매칭(Matching), 리포팅 및 통제(Reporting & Governance)이다.

**1단계: 의존성 탐지(Dependency Discovery)**
패키지 매니저(package.json, requirements.txt, pom.xml, go.mod 등)를 파싱하여 직접 의존성을 추출하고, 이를 기반으로 전이적 의존성 트리(Dependency Tree)를 구성한다.

```text
[의존성 트리 구성 및 스캔 흐름]

┌─ 의존성 트리 구성 ──────────────────────────────────────────┐
│                                                             │
│  [package.json]                                             │
│  "dependencies": {                                         │
│    "express": "^4.18.0"     ← 직접 의존성                  │
│  }                                                         │
│       │                                                    │
│  npm ls --all (의존성 트리 전체 출력)                       │
│       │                                                    │
│       ├── express@4.18.2     (direct)                      │
│       │     ├── accepts@1.3.8                                 │
│       │     ├── body-parser@1.20.0                           │
│       │     │     └── raw-body@2.4.3   ← CVE-2023-XXXXX   │
│       │     └── ...                                         │
│       └── qs@6.11.0          (transitive)                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**2단계: 취약점 데이터베이스 매칭(Matching)**
NVD(National Vulnerability Database), CVE 데이터베이스, 자사 보안 Intel 데이터베이스(GitHub Advisory Database, Snyk Intel, WhiteSource)를 참조하여, 의존성 버전과 CVE를 매칭한다.

```text
[SCA 취약점 매칭 아키텍처]

[스캔된 의존성 목록]          [취약점 DB (CVE, NVD)]
                                 │
express@4.18.2  ──────────────> ┌────────────────────────┐
                               │ CVE-2021-23337        │
                               │ 심각도: HIGH (8.1)     │
                               │影响的版本: <4.17.21   │
                               │ 설명: Lodash RCE 취약점 │
                               └────────────────────────┘
                                    │
                              매칭 결과: ⚠️ 발견
```

**3단계: 리포팅 및 게이트 통제**
스캔 결과를 HTML/XML/JSON 보고서로 출력하고, CI/CD 파이프라인에서 게이트를 설정하여 취약점이 발견되면 빌드를 실패시킨다.

| SCA 도구 | 개발사 | 특징 | 데이터베이스 |
|:---|:---|:---|:---|
| **OWASP Dependency-Check** | OWASP | 오픈소스, CLI 통합 용이 | NVD, OASIS |
| **Snyk** | Snyk | 실시간 취약점 DB, IDE 연동 강함 | 자체 Intel DB |
| **GitHub Dependabot** | GitHub | GitHub 내장, 자동 PR 생성 | GitHub Advisory DB |
| **WhiteSource** | Mend | 기업용, 라이선스 컴플라이언스 강함 | 자체 DB |
| **Trivy** | Aqua Security | 컨테이너 이미지 스캐닝 겸용, 가벼움 | NVD, GitHub Advisories |

SCA를 CI/CD 파이프라인에 통합하는 구조는 다음과 같다:

```text
[CI/CD 파이프라인 내 SCA 통합]

[Git Push / PR]
       │
       ▼
┌── CI Server (GitHub Actions) ─────────────────────────────┐
│                                                           │
│  1. [Build] 의존성 설치 (npm install / pip install)      │
│       │                                                  │
│  2. [SCA Scan - Build 단계]                              │
│     npx snyk test (또는 trivy fs --security-checks vuln) │
│       │                                                  │
│       ├─ 취약점 발견 ❌ ──> ❌ 빌드 실패, 자동 PR 생성 불가 │
│       │     (ex: log4j 2.17.0 미만 → 즉시 실패)            │
│       │                                                  │
│       └─ 통과 ✅ ──> 빌드 계속                              │
│                                                           │
│  3. [SBOM 생성]                                           │
│     syft . -o cyclonedx-json > sbom.json                  │
│       │ (SBOM을 artifact로 저장 - 향후 감사 증거)         │
│       │                                                  │
│  4. [Container Scan - Deploy 단계]                        │
│     trivy image --severity HIGH,CRITICAL myapp:1.0.0      │
│       │                                                  │
│       └─ 이미지 내 취약한 base layer 발견 시 배포 차단   │
└───────────────────────────────────────────────────────────┘
```

**📢 섹션 요약 비유**: SCA는 음식 재료의 원산지를 추적하는食品安全追溯系统입니다. 고춧가루(라이브러리)를 사왔는데, 그 고춧가루를 만든 사람(공급자)이 비료(전달 의존성)에 대해 허위 보고를 했는지까지 검증하여, 최종 요리(프로덕션)가 안전하게 고객에게 나갈 수 있도록 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

SCA는 단독으로 존재하지 않고, SAST(코드 정적 분석), 컨테이너 스캐닝, SBOM 생성과 결합하여 DevSecOps 보안 파이프라인을 완성한다.

| 보안 도구 | 분석 대상 | 분석 시점 | 주요 탐지 내용 |
|:---|:---|:---|:---|
| **SAST** | 직접 작성한 소스코드 | CI 빌드 (소스 코드) | SQL Injection, XSS 등 코드 결함 |
| **SCA** | 오픈소스 의존성 | CI 빌드 (의존성 설치 후) | CVE 취약점, 라이선스 위반 |
| **DAST** | 실행 중인 애플리케이션 | 배포 후 (스테이징) | 런타임 웹 취약점, API 보안 |
| **컨테이너 스캐닝** | 도커 이미지/OS 패키지 | 이미지 빌드/배포 시 | Base Image CVE, 설정 오류 |

SCA와 SAST의 가장 큰 차이는 **분석 대상**이다. SAST는 내가 작성한 코드에 Security 문제가 있는지를 분석하고, SCA는 내가 가져다 쓴第三方 코드에 Security 문제가 있는지를 분석한다. 따라서 보안 파이프라인에서 두 가지는 반드시 함께 동작해야 한다.

```text
[SCA + SAST + 컨테이너 스캐닝 통합 보안 파이프라인]

[Code]
  │
  ├── SAST (SonarQube, Checkmarx) ────> 내가 작성한 코드 결함 탐지
  │
  ├── SCA (Snyk, Dependabot) ────────> 외부 의존성 CVE 탐지
  │
  └── [Build Docker Image]
            │
            ├── 컨테이너 스캐닝 (Trivy, Clair) ────> Base Image CVE 탐지
            │
            └── [Scan Result]
                  │
                  ├─ ✅ 모든 보안 검사 통과 ──> 프로덕션 배포 승인
                  └─ ❌ 하나라도 실패 ──> 빌드/배포 차단
```

**📢 섹션 요약 비유**: 집을 지을 때 내 설계도(SAST)를 점검하고, 시공에 사용하는 모든 건설 자재(SCM)의 제조일자와 품질 인증서(SCA)를 확인하며, 완공된 건물 전체(컨테이너 스캐닝)의 안전성을 다시 한 번 검증하는 3단계 안전 진단 시스템과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

SCA를 실무에 도입할 때 흔히 겪는 딜레마와 기술적 판단 기준은 다음과 같다.

1. **취약점 심각도 기준 설정 (Severity Threshold)**
   - **상황**: SCA가 100개 이상의 취약점을 탐지했는데, 대부분이 낮은 심각도(LOW)이다. 개발팀이 "Critical만 고치면 된다"고 주장함.
   - **판단**: 단순히 심각도(CVSS Score)만으로 우선순위를 정하면 안 된다. **실제 공격 가능성(Exploitability)** 과 **애플리케이션 내 사용 여부(Usage)** 를 함께 고려해야 한다. 예를 들어, RCE(Remote Code Execution) 취약점이 있어도 해당 라이브러리의脆弱한 함수를 애플리케이션에서 사용하지 않으면 실제 위험은 낮다. Snyk, Sonatype Nexus Firewall 등의 **Exploitability Inteligence** 기능을 활용하여 실질적 위험을 평가해야 한다.

2. **전이적 의존성의 업데이트 어려움**
   - **상황**: 직접 사용하는 라이브러리(express@4.18.2)는 안전하지만, 그 내부에 포함된 전이적 의존성(body-parser@1.20.0)이 CVE에 노출되어 있음. 라이브러리 개발자가 패치를 기다려야 하는데更新时间 알 수 없음.
   - **판단**: 전이적 의존리의 취약점은 **번들링 또는 포팅(Bundling/Patching)** 으로 대응한다. 직접 의존성을 업그레이드하여 전이적 의존성도 자동 업데이트되게 하거나, 취약한 함수 사용을 코딩 레벨에서 회피(Workaround)하는 것이 현실적이다. 또한 **"최소 권한 의존성(Least Dependency)"** 원칙을 지켜, 불필요한 라이브러리는 설치 자체를 하지 않는 것이 예방이다.

3. **라이선스 컴플라이언스 vs 개발 속도 트레이드오프**
   - **상황**: 팀이 "이 오픈소스 라이브러리(AGPL 라이선스)를 쓰면 제품 전체가 GPL이 되어 소스 코드 공개 의무가 발생한다"고 주장. 법무팀에서 사용을 원천 거부함.
   - **판단**: AGPL은 네트워크 사용까지 소스 공개 의무를 확대한 라이선스로, SaaS 형태의 서비스에는 매우 위험하다. **선택적 라이선스 허용 정책(Allow-list vs Block-list)** 을 세워야 한다. Apache 2.0, MIT, BSD-3-Clause는 허용, AGPL, SSPL, BSL은 기본 차단하는 명확한 가이드라인을 문서화하고, SCA 도구에서 이를 자동 enforcement해야 한다.

```text
[라이선스 허용/차단 정책 설정 예시 (Snyk)]

Allowed Licenses (Allow-list):
  ├─ MIT, Apache-2.0, BSD-2/3-Clause, ISC
  └─ GNU GPL-2.0 / GPL-3.0 (상업적 내부 사용만 허용)

Blocked Licenses (Block-list):
  ├─ AGPL-3.0, SSPL-1.0, BSL-1.0
  └─ proprietary licensed components

Policy Enforcement:
  ├─ BLOCK: 빌드 실패 (Critical/Permissive 위반)
  ├─ WARN: 경고만 발생 (Weak Copyleft 등)
  └─ APPROVE: 수동 승인 후 사용 (Complex License)
```

**📢 섹션 요약 비유**: 음식을 만들 때 모든 재료에 원산지 증명서와 유통기한을 확인하는 것은 기본입니다. 하지만 "유통기한은 남아있지만 내 음식을 만든 조리사(라이브러리 개발자)가 누구냐"까지 추적하면 안전이 한 단계 더 올라갑니다. SCA는 이 모든 추적 과정을 자동화한食品安全 감독관입니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

SCA가 조직에 정착되면 다음과 같은 기대효과가 있다.

| 기대 효과 | 기존 (의존성 미검증) | SCA 도입 후 | 비즈니스 가치 |
|:---|:---|:---|:---|
| **취약점 발견 시점** | 프로덕션 배포 후 (침해 사고) | 빌드 단계 (조기 발견) | 사고 대응 비용 100분의 1 이하 |
| **공급망 보안** |第三方 라이브러리 알 수 없음 | 전체 의존성 트리可視化 | 제조물 책임 위험 최소화 |
| **라이선스 컴플라이언스** | 법무팀 수동 검토 (릴리스 병목) | 자동화된 라이선스 검증 | 제품 출시 시간 단축 |
| **규제 준수** | 증거 확보 어려움 | SBOM 자동 생성 | ISO 27001, SOC 2 감사 대응 |

향후 SCA는 **SBOM(Software Bill of Materials)** 표준과 결합하여 더욱 정교한 공급망 보안을 구현할 것이다. 미국 연방 정부에서는 Biden 행정명령(14028)으로 95조 이상의政府采购에 SBOM 의무화를 시행하고 있으며, 이는 전 세계 공공 部رشглашение 확대될 전망이다. SCA는 이 SBOM 생성의 핵심 기술이 된다.

**📢 섹션 요약 비유**: 식품의 원산지 표시제도가 소비자에게食品安全을 보장하듯이, 소프트웨어의 "구성 요소 표시제(SBOM)"가 궁극적으로는 소프트웨어 소비자에게 오픈소스 재료의 안전성을 보장하는 시대가 온 것입니다. SCA는 이 표시제를 자동으로 작성하고 검증하는 핵심 시스템입니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **SBOM (Software Bill of Materials)** (SCA가 생성하는 소프트웨어 구성 요소 명세서)
- **CVE (Common Vulnerabilities and Exposures)** (공개된 보안 취약점의 표준화된 식별자)
- **DevSecOps** (보안 검사 도구를 CI/CD 파이프라인에 내장하는 DevOps 확장 철학)
- **SAST (Static Application Security Testing)** (내가 작성한 코드 기반 보안 분석)
- **컨테이너 이미지 스캐닝 (Trivy, Clair)** (컨테이너 레이어의 OS/라이브러리 취약점 스캔)

### 👶 어린이를 위한 3줄 비유 설명
1. 빵을 만드는 데 밀가루(오픈소스 라이브러리)를 사왔는데, 그 밀가루를 만든 곳에서 썩은 곡물을 섞었는지 알 수 없잖아요.
2. SCA는 밀가루뿐 아니라 그 밀가루를 만든 농부와 비료(전이적 의존성)까지 전부 추적해주는 거예요.
3. 문제가 있는 밀가루면 아예 빵을 만들지 못하게 막아주니까 우리 아이들은 항상 안전한 빵을 먹을 수 있어요.