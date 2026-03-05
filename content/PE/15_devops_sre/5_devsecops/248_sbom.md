+++
title = "SBOM (소프트웨어 자재 명세서)"
description = "소프트웨어를 구성하는 모든 오픈소스 컴포넌트, 라이브러리, 버전 정보를 명세한 자재 명세서로 공급망 보안의 핵심"
date = 2024-05-15
[taxonomies]
tags = ["SBOM", "Software-Bill-of-Materials", "Supply-Chain-Security", "DevSecOps", "CVE", "Compliance"]
+++

# SBOM (소프트웨어 자재 명세서)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 소프트웨어 제품에 포함된 **모든 서드파티 컴포넌트(오픈소스 라이브러리, 버전, 라이선스, 출처)를 상세히 나열한 명세서**로, 식품의 원재료 표시와 같이 소프트웨어 공급망의 투명성을 보장하는 메타데이터 문서입니다.
> 2. **가치**: Log4j, SolarWinds 같은 공급망 공격 발생 시, 어떤 제품이 취약한 컴포넌트를 포함하는지 신속히 식별하고, 규정 준수(SBOM 의무화) 및 라이선스 충돌 방지를 가능하게 합니다.
> 3. **융합**: CI/CD 파이프라인에서 자동 생성되어 취약점 스캐너(SCA), 컴플라이언스 도구, SBOM 관리 플랫폼과 연동되어 DevSecOps의 핵심 구성요소가 됩니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**SBOM(Software Bill of Materials, 소프트웨어 자재 명세서)**는 소프트웨어 제품을 구성하는 **모든 구성 요소(Component)의 명세 목록**입니다. 각 컴포넌트에 대한 정보:
- **이름(Name)**: 컴포넌트 이름 (예: log4j-core)
- **버전(Version)**: 2.14.1
- **공급자(Supplier)**: Apache Software Foundation
- **식별자(Identifier)**: PURL(pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1), CPE, SWID
- **라이선스(License)**: Apache-2.0
- **의존성(Dependencies)**: 이 컴포넌트가 의존하는 다른 컴포넌트
- **해시(Hash)**: SHA-256 등 무결성 검증용

SBOM은 **직접 의존성(Direct Dependencies)**과 **간접 의존성(Transitive Dependencies)** 모두를 포함합니다.

### 2. 구체적인 일상생활 비유
식품 포장지의 **원재료 명세서**를 상상해 보세요. "밀가루, 설탕, 계란, 우유..."가 적혀 있습니다. 알레르기가 있는 사람은 "계란 포함"을 보고 피할 수 있습니다. **SBOM**은 소프트웨어의 원재료 명세서입니다. "Log4j 2.14.1 포함"을 보고, "아, 이건 보안 취약점이 있으니 업데이트해야겠다"라고 판단할 수 있습니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (공급망 보안의 블랙박스)**:
   기업들은 자신이 개발한 코드는 관리하지만, 그 코드가 사용하는 수천 개의 오픈소스 라이브러리가 **무엇인지, 어디서 왔는지, 어떤 라이선스인지** 모르는 경우가 많았습니다. Log4j 취약점(CVE-2021-44228) 발생 시, "우리 제품이 Log4j를 쓰나?"부터 확인해야 했습니다.

2. **혁신적 패러다임 변화의 시작**:
   2021년 미국 행정명령 14028(EO 14028)이 연방정부에 판매되는 모든 소프트웨어에 SBOM 제출을 의무화했습니다. 이는 민간 기업에도 파급효과를 주었습니다. SPDX(Software Package Data Exchange)와 CycloneDX가 주요 SBOM 표준 포맷으로 자리잡았습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   사이버 보안 보험, 공급망 보안 규정, 기업 간 계약에서 SBOM 제출을 요구하는 사례가 급증하고 있습니다. "SBOM 없으면 계약 없다"가 현실이 되고 있습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Field) | 상세 역할 | 필수 여부 | 예시 |
| :--- | :--- | :--- | :--- |
| **Component Name** | 컴포넌트 이름 | 필수 | log4j-core |
| **Version** | 버전 번호 | 필수 | 2.14.1 |
| **Supplier** | 제공자/개발자 | 권장 | Apache Software Foundation |
| **PURL (Package URL)** | 패키지 식별자 | 권장 | pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1 |
| **CPE** | 공통 플랫폼 열거 | 선택 | cpe:2.3:a:apache:log4j:2.14.1 |
| **License** | 라이선스 정보 | 권장 | Apache-2.0 |
| **Hash** | 무결성 해시 | 권장 | SHA-256:abc123... |
| **Dependency** | 의존 관계 | 권장 | Depends on: jackson-core |

### 2. 정교한 구조 다이어그램: SBOM 생성 및 활용 파이프라인

```text
=====================================================================================================
                      [ SBOM Generation & Usage Pipeline ]
=====================================================================================================

  [ Development ]              [ CI/CD Pipeline ]               [ Security/Compliance ]
       |                            |                                  |
       v                            v                                  v

+------------------+        +------------------+           +------------------+
| Source Code      |        | Build Stage      |           | SBOM Management  |
| + package.json   |  --->  | + Compile        |  --->     | Platform         |
| + pom.xml        |        | + SBOM Generate  |           | (Dependency-Track)|
| + go.mod         |        | + SBOM Sign      |           +--------+---------+
+------------------+        +--------+---------+                    |
                                     |                              |
                                     v                              v
                            +------------------+           +------------------+
                            | SBOM Artifact    |           | Vulnerability    |
                            | (SPDX/CycloneDX) |  ------>  | Scanner (SCA)    |
                            |                  |           | - Known CVEs     |
                            +--------+---------+           | - License Check  |
                                     |                     +--------+---------+
                                     |                              |
                                     v                              v
                            +------------------+           +------------------+
                            | Artifact Repo    |           | Risk Dashboard   |
                            | (Nexus/Artifactory)|          | - Critical: 2    |
                            +------------------+           | - High: 5        |
                                     |                     | - License Issues: 1|
                                     v                     +------------------+
                            +------------------+
                            | Software Release |
                            | + Binary         |
                            | + SBOM           |
                            | + Signature      |
                            +------------------+

=====================================================================================================

                      [ SBOM Format Comparison: SPDX vs CycloneDX ]
=====================================================================================================

  SPDX (Software Package Data Exchange)       CycloneDX (OWASP)
  ════════════════════════════════════════    ═════════════════════════════════

  {                                           {
    "spdxVersion": "SPDX-2.3",                "bomFormat": "CycloneDX",
    "dataLicense": "CC0-1.0",                 "specVersion": "1.4",
    "name": "myapp",                          "serialNumber": "urn:uuid:...",
    "packages": [                             "components": [
      {                                         {
        "name": "log4j-core",                    "type": "library",
        "version": "2.14.1",                     "name": "log4j-core",
        "licenseConcluded": "Apache-2.0",        "version": "2.14.1",
        "externalRefs": [{                       "licenses": [{
          "referenceCategory": "PACKAGE-MANAGER",   "license": {"id": "Apache-2.0"}
          "referenceLocator":                     }]
            "pkg:maven/..."                     "purl": "pkg:maven/...",
        }]                                      "hashes": [{"alg": "SHA-256", ...}]
      }                                       }
    ],                                        ],
    "relationships": [...]                    "dependencies": [...]
  }                                           }

  Linux Foundation 표준                      OWASP 경량화 표준
  라이선스 정보 풍부                          보안 중심, 의존성 그래프 강화

=====================================================================================================
```

### 3. 심층 동작 원리 (SBOM 생성 및 활용 메커니즘)

**1. SBOM 생성 방식**
- **빌드 시 생성(Build-time)**: 패키지 매니저(maven, npm, pip)의 lock 파일을 분석하여 생성
- **런타임 생성(Runtime)**: 실행 중인 컨테이너/시스템에서 실제 로드된 라이브러리 스캔
- **소스 분석(Source Analysis)**: 소스 코드의 import/require 문 분석

**2. 의존성 트리(Dependency Tree)**
SBOM은 직접 의존성뿐 아니라, 간접 의존성(의존성의 의존성)까지 모두 포함합니다:
```
myapp
  |-- express@4.18.0 (direct)
  |     |-- body-parser@1.20.0 (transitive)
  |     |     |-- bytes@3.1.2 (transitive)
  |     |-- debug@2.6.9 (transitive)
  |-- lodash@4.17.21 (direct)
```

**3. VEX(Vulnerability Exploitability eXchange)**
SBOM과 함께 VEX 문서를 제공하면, "이 취약점은 우리 환경에서 악용 불가능함"을 선언할 수 있습니다. False Positive 감소.

### 4. 핵심 알고리즘 및 실무 코드 예시

**CycloneDX SBOM 생성 (Syft)**

```bash
# Generate SBOM from container image
syft myapp:v1.2.3 -o cyclonedx-json > sbom.json

# Generate SBOM from directory
syft dir:/path/to/source -o cyclonedx-json > sbom.json

# Generate SPDX format
syft myapp:v1.2.3 -o spdx-json > sbom-spdx.json
```

**생성된 SBOM 예시 (CycloneDX JSON)**

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "serialNumber": "urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79",
  "version": 1,
  "metadata": {
    "timestamp": "2024-05-15T10:30:00Z",
    "component": {
      "type": "application",
      "name": "myapp",
      "version": "1.2.3"
    },
    "tools": [
      {
        "vendor": "Anchore",
        "name": "Syft",
        "version": "0.100.0"
      }
    ]
  },
  "components": [
    {
      "type": "library",
      "bom-ref": "pkg:npm/express@4.18.2",
      "name": "express",
      "version": "4.18.2",
      "purl": "pkg:npm/express@4.18.2",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "abc123def456..."
        }
      ]
    },
    {
      "type": "library",
      "bom-ref": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1",
      "name": "log4j-core",
      "version": "2.14.1",
      "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1",
      "licenses": [
        {
          "license": {
            "id": "Apache-2.0"
          }
        }
      ],
      "supplier": {
        "name": "Apache Software Foundation"
      }
    }
  ],
  "dependencies": [
    {
      "ref": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1",
      "dependsOn": [
        "pkg:maven/org.apache.logging.log4j/log4j-api@2.14.1"
      ]
    }
  ]
}
```

**CI/CD 파이프라인 통합 (GitHub Actions)**

```yaml
# .github/workflows/sbom.yml
name: Generate and Upload SBOM

on:
  push:
    branches: [main]

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Application
        run: |
          npm ci
          npm run build

      - name: Generate SBOM with Syft
        uses: anchore/sbom-action@v0
        with:
          image: myapp:${{ github.sha }}
          format: cyclonedx-json
          output-file: sbom.json

      - name: Upload SBOM to Dependency-Track
        run: |
          curl -X POST \
            -H "X-API-Key: ${{ secrets.DTRACK_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d @sbom.json \
            "${{ secrets.DTRACK_URL }}/api/v1/bom"

      - name: Scan SBOM for vulnerabilities
        uses: anchore/scan-action@v3
        with:
          sbom: sbom.json
          fail-build: true
          severity-cutoff: high

      - name: Upload SBOM artifact
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.json
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: SBOM 표준 비교

| 평가 지표 | SPDX | CycloneDX | SWID Tag |
| :--- | :--- | :--- | :--- |
| **개발 주체** | Linux Foundation | OWASP | ISO/IEC 19770-2 |
| **주요 용도** | 라이선스 컴플라이언스 | 보안 취약점 스캔 | 소프트웨어 자산 관리 |
| **포맷** | JSON, RDF, Tag-Value | JSON, XML | XML |
| **의존성 그래프** | 제한적 | 강력함 | 없음 |
| **VEX 지원** | 제한적 | 완전 지원 | 없음 |
| **채택률** | 높음 (리눅스/오픈소스) | 증가 중 (보안 중심) | 낮음 (엔터프라이즈) |

### 2. 과목 융합 관점 분석

**SBOM + SCA(Software Composition Analysis)**
- SBOM은 컴포넌트 목록, SCA는 그 컴포넌트의 취약점(CVE)을 탐지합니다. SBOM이 SCA의 입력이 됩니다.

**SBOM + 컨테이너 레지스트리**
- 컨테이너 이미지와 함께 SBOM을 레지스트리(Harbor, ECR)에 저장하면, 이미지를 배포할 때마다 SBOM도 함께 전달됩니다.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] Log4j 취약점 발생 시 대응**
- **문제점**: Log4j 취약점(CVE-2021-44228)이 발표되었습니다. 어떤 제품이 영향받는지 파악해야 합니다.
- **기술사 판단 (전략)**: 모든 제품의 SBOM을 쿼리하여 "log4j-core" 버전이 2.14.x 이하인 제품 식별. 5분 내에 영향받는 제품 목록 확보.

**[상황 B] 고객사 SBOM 제출 요구**
- **문제점**: 고객사가 "제품의 SBOM을 제출하라"고 요청했습니다.
- **기술사 판단 (전략)**: CI/CD 파이프라인에서 자동 생성된 SBOM을 CycloneDX 포맷으로 제출. 민감 정보(내부 라이브러리 이름 등)는 마스킹.

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] SBOM 포맷 선택: SPDX(라이선스 중심) vs CycloneDX(보안 중심)
- [ ] 생성 시점: 빌드 시 vs 릴리스 시
- [ ] 저장소: 아티팩트 리포지토리, Dependency-Track, 전용 SBOM 플랫폼

**운영적 고려사항**
- [ ] SBOM 버전 관리: 소프트웨어 버전과 SBOM 버전 매핑
- [ ] 공개 범위: 전체 공개 vs 부분 공개 vs 내부용
- [ ] 업데이트 주기: 릴리스 시마다 갱신

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: SBOM 생성만 하고 활용 안 함**
- SBOM을 생성하여 파일만 저장해두고, 취약점 스캔이나 컴플라이언스 체크에 활용하지 않으면 무용지물입니다. 자동화된 파이프라인 필수.

**안티패턴 2: 수동으로 SBOM 작성**
- 엑셀이나 문서로 수동 작성한 SBOM은 불완전하고 오래되면 부정확해집니다. 반드시 도구로 자동 생성해야 합니다.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | SBOM 없음 (AS-IS) | SBOM 적용 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **취약점 영향 파악** | 수일~수주 | 수분 | **대응 속도 99% 향상** |
| **규정 준수** | 수동 증빙 | 자동화된 증빙 | **감사 비용 절감** |
| **라이선스 위반** | 발견 시 법적 문제 | 사전 탐지 | **법적 리스크 제거** |
| **공급망 투명성** | 블랙박스 | 완전 투명 | **신뢰성 향상** |

### 2. 미래 전망 및 진화 방향
- **SBOM签署(SBOM Signing)**: SBOM 자체를 Cosign으로 서명하여 위변조 방지.
- **VEX(Vulnerability Exploitability eXchange)**: 취약점의 악용 가능성을 선언하는 VEX와 결합하여 False Positive 감소.

### 3. 참고 표준/가이드
- **NTIA Minimum Elements for SBOM**: SBOM 필수 항목 정의
- **US Executive Order 14028**: 연방정부 SBOM 의무화
- **SPDX ISO/IEC 5962:2021**: SPDX 국제 표준
- **CycloneDX Specification**: OWASP CycloneDX 사양

---

## 관련 개념 맵 (Knowledge Graph)
- **[SCA](@/studynotes/15_devops_sre/5_devsecops/246_sca.md)**: SBOM 기반 취약점 스캔
- **[DevSecOps](@/studynotes/15_devops_sre/5_devsecops/241_devsecops_principles.md)**: SBOM 생성 자동화
- **[공급망 보안](@/studynotes/15_devops_sre/5_devsecops/249_supply_chain_attack.md)**: SBOM이 방어하는 공격 유형
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/3_automation/continuous_integration.md)**: SBOM 생성 단계
- **[컨테이너 이미지 스캔](@/studynotes/15_devops_sre/5_devsecops/247_container_scanning.md)**: SBOM 기반 이미지 분석

---

## 어린이를 위한 3줄 비유 설명
1. 과자 봉지 뒤에는 **"이 과자에 뭐가 들었는지"** 적혀 있어요. 밀가루, 설탕, 우유... 알레르기 있는 친구는 피할 수 있죠!
2. SBOM은 소프트웨어의 **원재료 표시**예요. "이 프로그램에 Log4j가 들었어요" 하고 알려주죠.
3. 덕분에 "Log4j가 아프대요!" 하면, "내 과자에 Log4j 있나?" 하고 바로 확인할 수 있어요!
