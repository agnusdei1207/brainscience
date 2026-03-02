+++
title = "DevSecOps - 보안 내재화 개발 방법론"
date = 2026-03-02

[extra]
categories = "pe_exam-software_engineering"
+++

# DevSecOps - 보안 내재화 개발 방법론

## 핵심 인사이트 (3줄 요약)
> **개발(Dev)·보안(Sec)·운영(Ops)을 통합**해 개발 초기부터 보안을 자동화하는 현대 SW 개발 패러다임. "Shift Left Security" - 보안 검사를 개발 초기(왼쪽)로 당긴다. 기술사 시험에서 DevOps와의 차이 및 파이프라인 구성이 핵심이다.

## 1. 개념 및 등장 배경

```
DevOps 진화:

개발(Dev) ─────┐              DevOps:
운영(Ops) ─────┤ → 속도↑      Dev + Ops 통합
               │              배포 주기: 수개월 → 수십 번/일

문제: 보안(Sec)이 뒤처짐
- 개발 막판에 보안 검토 → 취약점 늦게 발견
- 수정 비용 폭증 (요구사항 단계의 100배)
- 클라우드·컨테이너 시대 공격 표면 증가

해결: DevSecOps
Dev + Sec + Ops = 보안을 SDLC 전 단계에 자동화로 내재화
```

## 2. Shift Left Security (보안 좌이동)

```
기존 보안 검토:       Shift Left:
━━━━━━━━━━━━          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
계획 → 설계 → 개발 → 테스트 → 출시 → 운영
                               [보안]   ← 너무 늦음!

계획 → 설계 → 개발 → 테스트 → 출시 → 운영
[위협│  [SCA │[SAST][DAST][침투│[런타임
모델링│  설계 │ 코드  │ 동적│ 테스트│ 보안 모니터링
     │  검토]│분석]  │분석]│      │
     
↑                              ↑
일찍 발견 → 수정 비용 ↓        늦게 발견 → 수정 비용 폭증
```

## 3. DevSecOps 파이프라인 구성

```
┌──────────────────────────────────────────────────────────────────┐
│              DevSecOps CI/CD 파이프라인                           │
├──────┬────────┬───────┬──────────┬──────────┬────────────────────┤
│Plan  │ Code   │Build  │  Test    │ Release  │    Monitor         │
├──────┼────────┼───────┼──────────┼──────────┼────────────────────┤
│위협  │IDE 보안│SCA    │SAST      │DAST      │런타임 보안 모니터링  │
│모델링│플러그인│(공개  │(정적     │(동적     │SIEM·SOAR           │
│      │        │소스   │분석)     │분석)     │                    │
│      │시크릿  │취약점)│          │          │취약점 스캔          │
│보안  │스캔    │       │IaC 보안  │침투      │(Twistlock, Falco)  │
│요구  │(Gitleaks│컨테이  │검사      │테스트    │                    │
│사항  │)       │너 스캔 │(tfscan)  │          │인시던트 대응        │
│      │        │(Trivy) │          │          │                    │
└──────┴────────┴───────┴──────────┴──────────┴────────────────────┘

핵심 도구:
SAST (Static Analysis): SonarQube, Checkmarx, Fortify
SCA (Software Composition Analysis): Snyk, OWASP Dependency Check
DAST (Dynamic Analysis): OWASP ZAP, Burp Suite
Container Security: Trivy, Clair, Twistlock
Secret Scanning: Gitleaks, TruffleHog
IaC Security: Checkov, tfsec, KICS
```

## 4. DevOps vs DevSecOps 비교

| 항목 | DevOps | DevSecOps |
|------|--------|-----------|
| 포커스 | 속도·빈도 | 속도 + 보안 |
| 보안 시점 | 출시 전 | 개발 전 단계 |
| 보안 담당 | 보안팀 별도 | 모든 팀 공동 |
| 자동화 범위 | CI/CD | CI/CD + 보안 검사 |
| 피드백 속도 | 빠름 | 빠름 (자동화 시) |
| 도구 | Jenkins, GitHub Actions | + SAST, DAST, SCA |
| 문화 | 개발·운영 협력 | 개발·보안·운영 협력 |

## 5. SBOM (Software Bill of Materials)

```
SW 부품표 - 소프트웨어 구성 성분 목록

왜 필요한가?
- Log4Shell(2021): Log4j 취약점 → 전 세계 동시 타격
- 오픈소스 의존성 파악 부재 → 취약한 버전 사용 모름

SBOM 내용:
- 사용 오픈소스 목록 (이름, 버전, 라이선스)
- 의존성 트리 (어떤 라이브러리가 어떤 라이브러리 사용)
- 알려진 취약점 (CVE) 매핑

미국 행정명령(EO 14028, 2021): 연방정부 납품 SW SBOM 의무화
한국: 공공SW SBOM 도입 검토 중

형식: SPDX, CycloneDX
```

## 6. 공급망 보안 (Supply Chain Security)

```
SW 공급망 공격 (SolarWinds 2020 사례):
해커 → [SolarWinds 빌드 서버 침투]
      → 악성코드 주입 → 정상 업데이트에 포함
      → 18,000개 기업·기관이 업데이트 설치
      → NSA, 미 재무부 등 침투

대응: SLSA (Supply chain Levels for Software Artifacts)
Level 1: 빌드 스크립트 형식화
Level 2: 서명된 출처(Provenance) 생성
Level 3: 신뢰할 수 있는 빌드 플랫폼
Level 4: 두 명 검토, 밀봉된 빌드

Sigstore: 소프트웨어 서명 오픈소스 표준
```

## 7. 실무에서? (기술사적 판단)
- **금융권**: DevSecOps 파이프라인 + SIEM 통합 의무화 추세
- **공공 클라우드**: AWS Security Hub, Azure Defender 자동화
- **규제 대응**: PCI-DSS, ISMS-P, 망분리 요구 반영
- **기술사 포인트**: Shift Left, SAST·DAST·SCA 차이, SBOM, 공급망 보안

## 8. 관련 개념
- CI/CD (지속적 통합·배포)
- 보안 (OWASP Top 10)
- 소프트웨어 품질
- Zero Trust Architecture

---

---


## 📝 기술사 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"DevSecOps의 개념과 Shift Left Security 원칙을 설명하고, SAST·DAST·SCA·SBOM 등 핵심 도구를 비교하여 소프트웨어 공급망 보안 강화 방안을 논하시오."**

---

### Ⅰ. 개요

**DevSecOps**란 소프트웨어 개발(Dev)·보안(Sec)·운영(Ops)을 통합하여 개발 초기부터 보안을 내재화하는 방법론이다.

- **등장 배경**: 전통적 개발 주기에서 보안은 출시 직전 검토 → 취약점 발견 시 수정 비용 폭증 (IBM 보고서: 운영 시 발견 취약점은 설계 단계 대비 100배 비용)
- **Shift Left Security**: 보안 검증 시점을 개발 생명주기 왼쪽(초기 단계)으로 당기는 것
- **핵심 목적**: 보안 취약점의 조기 발견·수정으로 비용 절감, 빠른 배포 주기와 보안 수준 동시 확보

---

### Ⅱ. 구성 요소 및 핵심 원리

#### 1. DevSecOps 파이프라인 보안 게이트

| 파이프라인 단계 | 보안 활동 | 도구 예시 |
|-------------|---------|---------|
| **코드 작성** | IDE 내 실시간 취약점 탐지 | SonarLint, Snyk |
| **코드 커밋** | SAST (정적 분석) | SonarQube, Fortify |
| **빌드** | SCA (오픈소스 취약점) | OWASP Dependency-Check, Black Duck |
| **테스트** | DAST (동적 분석) | OWASP ZAP, Burp Suite |
| **배포** | SBOM 생성·검증 | CycloneDX, SPDX |
| **운영** | SIEM + SOAR 실시간 모니터링 | Splunk, IBM QRadar |

#### 2. 핵심 도구 원리

```
SAST (Static Application Security Testing):
  소스코드를 실행하지 않고 분석 → SQL Injection, XSS 패턴 탐지
  장점: 개발 초기 발견 가능  단점: 오탐(False Positive) 많음

DAST (Dynamic Application Security Testing):
  실행 중인 앱에 악성 입력 전송 → 실제 취약점 확인
  장점: 실제 공격 시뮬레이션  단점: 코드 커버리지 제한

SCA (Software Composition Analysis):
  오픈소스 라이브러리의 알려진 CVE 취약점 스캔
  장점: 공급망 취약점 탐지  단점: CVE 미등록 0-day 미탐지
```

---

### Ⅲ. 기술 비교 분석

| 항목 | DevOps | DevSecOps |
|-----|-------|---------|
| **보안 처리 시점** | 출시 전 별도 보안 점검 | ★ 전 개발 단계 통합 |
| **보안 담당자** | 별도 보안팀 (Gate Keeper) | ★ 전 팀원 보안 책임 (Shared Responsibility) |
| **취약점 발견 시점** | 스테이징/운영 단계 (비용 고) | ★ 코드 작성 단계 (비용 저, 100배 절감) |
| **배포 속도** | 빠름 | ★ 보안과 속도 동시 확보 |
| **컴플라이언스** | 사후 감사 | ★ 자동화된 지속적 컴플라이언스 검증 |

**SBOM (Software Bill of Materials):**
- 소프트웨어에 포함된 모든 오픈소스 성분표
- Log4Shell 사태(2021): Log4j 취약점 영향 범위를 SBOM 없이 파악 불가 → SBOM 의무화 트리거
- 미국 행정명령 EO 14028 (2021): 연방 정부 납품 소프트웨어 SBOM 제공 의무화

---

### Ⅳ. 실무 적용 방안

| 분야 | 적용 방법 | 기대 효과 |
|-----|---------|---------|
| **CI/CD 파이프라인** | SAST/SCA를 Quality Gate로 설정, 심각도 High 이상 빌드 차단 | 취약 코드 운영 환경 배포 차단 |
| **컨테이너 보안** | 컨테이너 이미지 취약점 스캔 (Trivy, Grype) | 알려진 CVE 포함 이미지 배포 방지 |
| **공급망 보안** | SBOM 자동 생성 + 취약점 DB와 자동 매핑 | 0-day 발생 시 영향 범위 수분 내 파악 |
| **비밀 정보 관리** | Git에서 비밀키 탐지 (GitGuardian), Vault 기반 비밀 관리 | 시크릿 노출 사고 예방 |

---

### Ⅴ. 기대 효과 및 결론

| 효과 | 내용 | 정량 목표 |
|-----|-----|---------|
| **보안 비용 절감** | 조기 취약점 탐지로 수정 비용 절감 | 개발 단계 발견 시 운영 대비 100배 절감 |
| **배포 빠른 속도** | 자동화된 보안 게이트로 수동 검토 제거 | 배포 주기 30~50% 단축 |
| **컴플라이언스** | 자동 감사 로그로 규정 준수 증명 | ISMS-P, ISO 27001 감사 대응 자동화 |

#### 결론
> DevSecOps는 소프트웨어 개발에서 보안을 비용이 아닌 **경쟁력**으로 변환하는 패러다임 전환이다. 특히 오픈소스 의존성이 90% 이상인 현대 소프트웨어에서 SCA와 SBOM은 공급망 보안의 필수 기반이 되었다. 향후 AI 기반 코드 생성 도구(GitHub Copilot 등)에도 보안 분석을 내재화하는 AI-Powered DevSecOps로 진화할 것이다.

> **※ 참고 표준**: OWASP Top 10, NIST SP 800-218 (SSDF), 미국 EO 14028, KISA 소프트웨어 개발 보안 가이드

---

## 어린이를 위한 종합 설명

**DevSecOps는 "집 짓는 중에 안전검사"야!**

```
기존 방식:
집 다 지음 → "화재 검사" → 문제 발견 → 이미 늦음 😱

DevSecOps (Shift Left):
기초 공사부터 → 벽 세울 때 → 지붕 올릴 때 → 계속 검사!
→ 문제 일찍 발견 = 비용 절감! 💰

SAST: 설계도 검토 (코드 분석)
DAST: 실제로 침입 테스트 (동적)
SCA: 쓴 자재들 성분 확인 (오픈소스)
```

**비밀**: Log4Shell 취약점 한 개로 전 세계 기업 수만 개가 해킹당했어요! 💥✨
