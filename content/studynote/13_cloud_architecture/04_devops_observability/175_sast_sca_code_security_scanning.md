+++
weight = 175
title = "175. 코드 정적 스캐닝 (SAST, SCA - Software Composition Analysis)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++
## 0. 핵심 인사이트

> **핵심**: SAST(Static Application Security Testing, 정적 애플리케이션 보안 테스팅)는 소스 코드를 실행하지 않고 취약점 패턴을 탐지하고, SCA(Software Composition Analysis, 소프트웨어 구성 분석)는 의존 오픈소스 라이브러리의 알려진 CVE를 스캔한다.
> 2. **가치**: 코드 리뷰 단계에서 SQL Injection, XSS 패턴을 자동 탐지하고, `log4j` 같은 오픈소스 취약점을 사용 여부와 함께 즉시 파악하여 배포 전 위험 제거가 가능하다.
> 3. **판단 포인트**: SAST는 자체 코드 취약점을, SCA는 의존성 취약점을 각각 담당하므로 두 도구를 모두 파이프라인에 통합해야 완전한 코드 보안 커버리지가 확보된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

현대 애플리케이션은 80~90%가 오픈소스 라이브러리로 구성된다는 연구 결과가 있다. 따라서 보안 취약점의 경로도 자체 작성 코드와 외부 의존성(Dependencies) 두 가지로 나뉜다.

SAST는 첫 번째 경로를 다룬다. 코드를 실행하지 않고 AST(Abstract Syntax Tree, 추상 구문 트리) 분석이나 패턴 매칭으로 SQL Injection, 하드코딩된 비밀번호, 입력 검증 누락 등 코딩 취약점을 찾는다. SonarQube, Semgrep이 대표 도구다.

SCA는 두 번째 경로를 다룬다. `package.json`, `pom.xml`, `requirements.txt` 같은 의존성 목록 파일을 분석하고, CVE(Common Vulnerabilities and Exposures, 공통 취약점 및 노출) 데이터베이스와 대조하여 위험한 버전의 라이브러리를 식별한다. 2021년 Log4Shell(Log4j 취약점, CVE-2021-44228)은 SCA의 필요성을 전 세계에 각인시켰다.

📢 **섹션 요약 비유**: SAST는 직접 만든 음식의 레시피를 검사해 유해 성분을 찾는 것이고, SCA는 식재료(오픈소스)의 원산지 성분표를 보고 알레르기 유발 물질을 확인하는 것이다.

---

## 2. 구성요소

### SAST와 SCA의 분석 위치

```
소스 코드
├─ app/
│   ├─ UserController.java   ← SAST 분석 대상
│   └─ DatabaseService.java  ← SAST 분석 대상
└─ pom.xml / package.json    ← SCA 분석 대상
    └─ log4j:2.14.1          → CVE-2021-44228 (Critical) ← SCA 탐지

[SAST 분석 과정]
소스 코드 → 파서(AST 생성) → 규칙 엔진(패턴 매칭) → 취약점 보고

[SCA 분석 과정]
의존성 파일 → 라이브러리 목록 추출 → CVE DB 조회 → 위험 등급 보고
```

| 항목 | SAST | SCA |
|:---|:---|:---|
| 분석 대상 | 자체 작성 소스 코드 | 오픈소스 라이브러리 의존성 |
| 데이터 소스 | 코딩 패턴 규칙셋 | CVE, NVD, OSS Advisory DB |
| 대표 취약점 | SQL Injection, XSS, 하드코딩 키 | Log4Shell, Spring4Shell |
| 도구 예시 | SonarQube, Semgrep, Checkmarx | Snyk, OWASP Dep-Check, Trivy |
| OWASP 관련 | Top 10 항목 대부분 커버 | A06:Vulnerable Components |

📢 **섹션 요약 비유**: SAST는 건물 설계 도면(소스 코드)에서 비상구가 제대로 있는지 확인하고, SCA는 건축 자재(라이브러리)에 불량품이 섞이지 않았는지 확인하는 검사다.

---

## 3. 구조 및 동작 원리

### SAST vs DAST vs SCA 비교

| 항목 | SAST | DAST | SCA |
|:---|:---|:---|:---|
| 분석 시점 | 빌드 전 (코드) | 배포 후 (실행) | 빌드 중 (의존성) |
| 앱 실행 필요 | 불필요 | 필요 | 불필요 |
| 발견 취약점 | 코드 버그 | 런타임 취약점 | 알려진 CVE |
| 오탐률 | 높음 | 낮음 | 낮음 |
| 속도 | 분 단위 | 시간 단위 | 빠름 |

**OWASP Top 10과 SAST 커버리지:**
- **A01**: Broken Access Control → SAST 부분 탐지
- **A02**: Cryptographic Failures → SAST 하드코딩 키 탐지
- **A03**: Injection (SQL, Command) → SAST 강력 탐지
- **A06**: Vulnerable Components → SCA 전담 영역

📢 **섹션 요약 비유**: SAST는 의사가 환자 X-ray(코드)를 보는 것이고, DAST는 환자를 뛰게 해보며 실제 증상을 확인하는 것이고, SCA는 가족력(라이브러리 이력)을 확인하는 것이다.

---

## 4. 비교 및 트레이드오프

**SonarQube 운영 방식:**
- Quality Gate: 임계값(Critical 0건, Coverage 80% 이상)을 통과해야 PR 머지 허용
- SonarLint: 개발자 IDE 플러그인으로 코드 작성 중 실시간 피드백
- SonarCloud: SaaS 형태, GitHub Actions와 즉시 통합

**Snyk(SCA) CI/CD 통합:**
```yaml
# GitHub Actions 예시
- name: Snyk 취약점 스캔
  uses: snyk/actions/node@master
  with:
    command: test
    args: --severity-threshold=high
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
# High 이상 CVE 발견 시 빌드 실패
```

**실무 우선순위**: Critical → High → Medium → Low 순으로 임계값 설정. 초기 도입 시 Critical만 빌드 차단하고, 안정화 후 High로 확대.

📢 **섹션 요약 비유**: Quality Gate는 식당의 위생 검사 기준이다. "바퀴벌레 0마리(Critical 취약점 0건)"를 충족해야 영업(배포)이 가능하다.

---

## 5. 실무 적용 및 최적화 기법

SAST + SCA 통합으로 코드 레벨과 의존성 레벨의 보안 취약점을 개발 초기에 체계적으로 차단할 수 있다. 특히 오픈소스 의존성 취약점(SCA)은 매년 수천 건의 새 CVE가 공개되므로 자동화된 모니터링 없이는 인력으로 추적이 불가능하다.

SBOM(Software Bill of Materials, 소프트웨어 자재 명세서)과 연계하면 배포된 모든 소프트웨어의 구성 요소를 목록화하여, 새 CVE가 공개될 때 즉시 영향 범위를 파악할 수 있다. 미국 정부 행정명령(EO 14028)과 같은 규제도 SBOM 제출을 요구하는 방향으로 발전하고 있다.

📢 **섹션 요약 비유**: SBOM은 식품의 영양 성분표다. 새로운 "유해 성분 발견" 뉴스가 나오면 해당 성분이 내 제품에 들어 있는지 성분표로 즉시 확인할 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| DevSecOps | SAST/SCA는 파이프라인 보안의 핵심 |
| OWASP Top 10 | SAST/SCA의 취약점 분류 기준 |
| CVE / NVD | SCA가 참조하는 취약점 데이터베이스 |
| SBOM | SCA 결과의 공식 문서화 형태 |
| Quality Gate | 보안 기준 미달 시 빌드 차단 메커니즘 |
| 이미지 취약점 스캐닝 | SCA의 컨테이너 이미지 확장 |

### 👶 어린이를 위한 3줄 비유 설명
1. SAST는 내가 직접 만든 작품에서 위험한 부분을 찾는 검사예요.

### 📈 관련 키워드 및 발전 흐름도

```text
SAST: 소스 코드 정적 분석 (SonarQube · Semgrep)
SCA: 오픈소스 의존성 취약점 스캔 (Snyk · Dependabot)
    │
    ▼
CI 통합: PR 단계에서 자동 차단 · 보고
    │
    ▼
SBOM 생성 → 소프트웨어 공급망 보안
```
2. SCA는 내가 가져다 쓴 레고 블록(라이브러리)에 불량품이 있는지 확인하는 거예요.
3. 두 검사를 모두 자동으로 해주니까, 위험한 코드가 사용자에게 전달되기 전에 잡을 수 있어요!
