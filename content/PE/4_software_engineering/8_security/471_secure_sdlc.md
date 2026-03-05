+++
title = "471. 소프트웨어 개발 보안 (Secure SDLC) - 기획, 설계, 구현, 테스트 전 단계 보안 활동"
date = "2026-03-05"
[extra]
categories = "studynotes-se"
tags = ["SecureSDLC", "보안", "DevSecOps", "시큐어코딩", "소프트웨어공학"]
+++

# 소프트웨어 개발 보안 (Secure SDLC) - 전 단계 보안 활동

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Secure SDLC는 소프트웨어 개발 생명주기의 모든 단계(기획→설계→구현→테스트→배포→운영)에 보안 활동을 내장하여, 출시 후 발견되는 보안 결함의 수정 비용을 100배까지 절감하는 선제적 보안 접근법이다.
> 2. **가치**: NIST 연구에 따르면 설계 단계에서 보안 취약점을 발견하면 운영 단계 대비 1/30~1/100의 비용으로 수정 가능하며, Secure SDLC 도입 시 보안 사고 감소 50%, 컴플라이언스 비용 절감 40% 효과가 입증된다.
> 3. **융합**: DevSecOps, Shift-Left Security, SBOM, IaC 보안 스캐닝 등 클라우드 네이티브 및 AI 기반 개발 환경에서 필수적인 보안 프랙티스로 진화하고 있다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

소프트웨어 개발 보안(Secure SDLC, Security Development Lifecycle)은 소프트웨어 개발의 전 과정에 보안 활동을 통합하여, 안전한 소프트웨어를 개발하기 위한 체계적인 접근법이다. 기존의 '개발 후 보안 점검(Bolt-on Security)' 방식에서 '개발 과정 내 보안 내장(Build-in Security)' 방식으로의 패러다임 전환을 의미한다.

Microsoft SDL, OWASP CLASP, BSIMM 등 다양한 프레임워크가 존재하며, 공통적으로 보안 요구사항 정의, 위협 모델링, 보안 설계, 시큐어 코딩, 보안 테스트, 보안 배포의 활동을 포괄한다.

### 비유

Secure SDLC는 마치 '건축 설계에 내장된 안전 시스템'과 같다. 집을 다 지어놓고 나서 "화재 감지기 어디에 달까?"라고 생각하면 이미 전선 공사가 끝난 후라 비용이 많이 든다. 반면, 설계 단계에서부터 화재 감지기, 비상구, 소화기 위치를 계획하면 추가 비용 없이 완벽한 안전 시스템을 갖출 수 있다.

### 등장 배경 및 발전 과정

1. **기존 접근법의 치명적 한계**: 전통적으로 보안은 개발 완료 후 침투 테스트, 취약점 스캐닝 등으로 점검했다. 그러나 이 방식은:
   - 이미 코드가 작성된 후라 수정 비용이 막대함 (Boehm의 비용 곡선: 설계 단계 대비 운영 단계 수정 비용은 100배)
   - 근본적 설계 결함은 수정 불가능한 경우가 많음
   - 보안 사고 발생 후 대응적 조치에 그침

2. **패러다임 변화**: 2002년 Microsoft의 Trustworthy Computing Initiative로 SDL(Security Development Lifecycle)이 탄생했다. 2004년 OWASP가 CLASP(Comprehensive, Lightweight Application Security Process)를 발표했고, 2008년에는 BSIMM(Building Security In Maturity Model)이 등장했다.

3. **비즈니스적 요구사항**: GDPR, CCPA 등 데이터 보호 법규 위반 시 최대 매출의 4% 벌금이 부과된다. 또한 보안 사고는 브랜드 신뢰도 하락, 매출 손실로 이어진다. Secure SDLC는 이러한 리스크를 선제적으로 관리하는 수단이다.

### Secure SDLC 전체 프레임워크

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   Secure SDLC 전체 프레임워크                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    1. 요구사항 단계 (Requirements)                │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 보안 요구사항 도출 (ABAC, RBAC, 암호화 요구 등)          │    │   │
│  │  │ • 규제 준수 요구사항 식별 (GDPR, ISMS, HIPAA)             │    │   │
│  │  │ • 보안 목표 정의 (CIA Triad)                              │    │   │
│  │  │ • 프라이버시 영향 평가 (PIA)                              │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      2. 설계 단계 (Design)                        │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 위협 모델링 (Threat Modeling - STRIDE/DREAD)           │    │   │
│  │  │ • 보안 아키텍처 설계 (Security Architecture)             │    │   │
│  │  │ • 보안 설계 원칙 적용 (Least Privilege, Defense in Depth)│    │   │
│  │  │ • 암호화 설계 (전송 구간, 저장 구간, 사용 구간)            │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      3. 구현 단계 (Implementation)                │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 시큐어 코딩 가이드라인 준수 (OWASP, KISA 47개 약점)      │    │   │
│  │  │ • 정적 분석 (SAST) - SonarQube, Checkmarx, Fortify       │    │   │
│  │  │ • 코드 리뷰에서 보안 체크리스트 적용                       │    │   │
│  │  │ • 시크릿 관리 (Hardcoded Secrets 탐지 및 제거)            │    │   │
│  │  │ • 의존성 취약점 스캔 (SCA) - OWASP Dependency-Check       │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      4. 테스트 단계 (Testing)                     │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 동적 분석 (DAST) - OWASP ZAP, Burp Suite               │    │   │
│  │  │ • 보안 테스트 케이스 수행 (인증, 인가, 세션, 입력 검증)    │    │   │
│  │  │ • 침투 테스트 (Penetration Testing)                     │    │   │
│  │  │ • 퍼즈 테스팅 (Fuzz Testing)                             │    │   │
│  │  │ • IAST (Interactive Application Security Testing)        │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      5. 배포 단계 (Deployment)                    │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 컨테이너 이미지 스캐닝 (Trivy, Clair)                   │    │   │
│  │  │ • IaC 보안 스캔 (Terraform Sentinel, Checkov)            │    │   │
│  │  │ • 시크릿 스캐닝 (Git-secrets, TruffleHog)                │    │   │
│  │  │ • 보안 설정 검증 (CSPM)                                  │    │   │
│  │  │ • SBOM 생성 및 검증 (SPDX, CycloneDX)                    │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      6. 운영 단계 (Operations)                    │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 런타임 보안 (RASP)                                     │    │   │
│  │  │ • 보안 모니터링 (SIEM, SOAR)                             │    │   │
│  │  │ • 취약점 관리 프로세스 (CVE 추적, 패치 관리)               │    │   │
│  │  │ • 침해 사고 대응 (Incident Response)                     │    │   │
│  │  │ • 보안 로그 감사 (Audit Trail)                           │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    ⊙ 전 단계 공통 활동                           │   │
│  │  • 보안 교육 및 인증    • 보안 메트릭 수집    • 컴플라이언스 유지  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 주요 Secure SDLC 프레임워크 비교

| 프레임워크 | 개발사 | 특징 | 주요 활동 | 적합 대상 |
|-----------|--------|------|----------|----------|
| **Microsoft SDL** | Microsoft | 7단계 프로세스, 실무적 | 위협 모델링, SAST/DAST, 보안 리뷰 | 대기업, 윈도우 환경 |
| **OWASP CLASP** | OWASP | 경량级, 애자일 친화적 | 보안 활동 통합, 역할 정의 | 중소규모, 웹 앱 |
| **BSIMM** | Cigital | 성숙도 모델, 벤치마킹 | 110+ 보안 활동, 측정 기반 | 성숙도 평가 |
| **NIST SSDF** | NIST | 미 연방 표준, 포괄적 | 준비, 구현, 테스트, 배포 | 규제 산업 |
| **ISO 27034** | ISO | 국제 표준, 인증 가능 | 보안 제어, 프로세스 관리 | 글로벌 기업 |

### Microsoft SDL 7단계 상세

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Microsoft SDL 7단계 프로세스                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 1: 교육 (Training)                                        │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 보안 기초 교육 (연 1회 필수)                            │    │   │
│  │  │ • 역할별 전문 교육 (개발자, 테스터, 아키텍트)               │    │   │
│  │  │ • 최신 위협 동향 공유                                     │    │   │
│  │  │ • 교육 이수 인증 체계                                     │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 2: 요구사항 (Requirements)                                │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 보안 요구사항 식별                                      │    │   │
│  │  │ • 품질 게이트/버그 바 정의                                │    │   │
│  │  │ • 보안 및 프라이버시 위험 평가                            │    │   │
│  │  │ • 최소 보안 요구사항(MSR) 체크리스트                       │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 3: 설계 (Design)                                          │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 위협 모델링 (STRIDE 모델 활용)                          │    │   │
│  │  │ • 공격 표면 분석 (Attack Surface Analysis)               │    │   │
│  │  │ • 보안 설계 리뷰                                         │    │   │
│  │  │ • 암호화 표준 준수 설계                                   │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 4: 구현 (Implementation)                                  │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 승인된 도구 사용 (컴파일러, 링커 보안 옵션)              │    │   │
│  │  │ • 정적 분석 (SAST) 자동화                                 │    │   │
│  │  │ • 코드 리뷰에 보안 체크리스트 포함                         │    │   │
│  │  │ • 안전하지 않은 함수 사용 금지 (strcpy, sprintf 등)        │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 5: 검증 (Verification)                                    │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 동적 분석 (DAST) / 퍼징 테스트                          │    │   │
│  │  │ • 위협 모델링 검증                                       │    │   │
│  │  │ • 코드 리뷰 및 보안 테스트                                │    │   │
│  │  │ • 침투 테스트 (외부 전문업체)                             │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 6: 릴리즈 (Release)                                       │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 최종 보안 리뷰 (FSR - Final Security Review)            │    │   │
│  │  │ • 보안 응급 대응 계획 수립                                │    │   │
│  │  │ • 취약점 대응 계획 (Vulnerability Response Plan)          │    │   │
│  │  │ • 릴리즈 서명 (Sign-off)                                 │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Phase 7: 대응 (Response)                                        │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ • 보안 응급 대응 계획 실행 (Incident Response Plan)       │    │   │
│  │  │ • 취약점 보고서 처리 (CERT-KR 등)                        │    │   │
│  │  │ • 보안 업데이트 배포 프로세스                             │    │   │
│  │  │ • 사후 분석 및 SDL 개선                                   │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 보안 테스트 도구 체계

| 단계 | 도구 유형 | 대표 도구 | 탐지 대상 |
|------|----------|----------|----------|
| 구현 | SAST | SonarQube, Checkmarx, Fortify | 소스코드 취약점 |
| 구현 | SCA | OWASP Dep-Check, Snyk, Black Duck | 오픈소스 취약점 |
| 구현 | Secrets Scan | Git-secrets, TruffleHog, Gitleaks | 하드코딩된 시크릿 |
| 테스트 | DAST | OWASP ZAP, Burp Suite, Nikto | 런타임 취약점 |
| 테스트 | IAST | Contrast Security, Hdiv Security | 하이브리드 분석 |
| 배포 | Container Scan | Trivy, Clair, Anchore | 컨테이너 이미지 취약점 |
| 배포 | IaC Scan | Checkov, Tfsec, Terrascan | 인프라 코드 취약점 |
| 운영 | RASP | Contrast, Imperva, Signal Sciences | 런타임 공격 방어 |

### 핵심 코드 예시: Secure SDLC 파이프라인

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class Severity(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"

class VulnerabilityType(Enum):
    SQL_INJECTION = "SQL Injection"
    XSS = "Cross-Site Scripting"
    CSRF = "Cross-Site Request Forgery"
    AUTH_BYPASS = "Authentication Bypass"
    INSECURE_DESERIALIZATION = "Insecure Deserialization"
    HARDCODED_SECRET = "Hardcoded Secret"
    OUTDATED_DEPENDENCY = "Outdated Dependency"
    MISCONFIGURATION = "Security Misconfiguration"

@dataclass
class Vulnerability:
    id: str
    type: VulnerabilityType
    severity: Severity
    title: str
    description: str
    location: str  # 파일:라인
    cwe_id: Optional[str] = None
    cve_id: Optional[str] = None
    cvss_score: Optional[float] = None
    remediation: Optional[str] = None
    detected_date: datetime = None
    status: str = "Open"

    def __post_init__(self):
        if self.detected_date is None:
            self.detected_date = datetime.now()

@dataclass
class SecurityGateResult:
    """보안 게이트 결과"""
    passed: bool
    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    blocked_reasons: List[str]

class SecureSDLC Pipeline:
    """
    Secure SDLC 파이프라인 관리

    CI/CD 파이프라인에 통합되어 보안 검사 자동화
    """

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.security_gate_policy = {
            'critical': 0,  # Critical 0개 허용
            'high': 0,      # High 0개 허용
            'medium': 5,    # Medium 5개까지 허용
            'low': 20       # Low 20개까지 허용
        }
        self.vulnerabilities: List[Vulnerability] = []

    def run_sast_scan(self, source_path: str) -> List[Vulnerability]:
        """
        정적 분석 (SAST) 실행

        실제로는 SonarQube, Checkmarx 등의 도구 API 호출
        """
        # 시뮬레이션: SAST 도구 실행 결과
        detected = [
            Vulnerability(
                id="SAST-001",
                type=VulnerabilityType.SQL_INJECTION,
                severity=Severity.CRITICAL,
                title="SQL Injection in UserDAO",
                description="사용자 입력이 SQL 쿼리에 직접 포함됨",
                location="src/dao/UserDAO.java:45",
                cwe_id="CWE-89",
                cvss_score=9.8,
                remediation="PreparedStatement 사용"
            ),
            Vulnerability(
                id="SAST-002",
                type=VulnerabilityType.HARDCODED_SECRET,
                severity=Severity.HIGH,
                title="Hardcoded Database Password",
                description="DB 비밀번호가 소스코드에 하드코딩됨",
                location="src/config/DatabaseConfig.java:12",
                cwe_id="CWE-798",
                remediation="환경 변수 또는 시크릿 매니저 사용"
            )
        ]

        self.vulnerabilities.extend(detected)
        return detected

    def run_sca_scan(self, dependency_file: str) -> List[Vulnerability]:
        """
        소프트웨어 구성 분석 (SCA) 실행

        오픈소스 의존성 취약점 스캔
        """
        detected = [
            Vulnerability(
                id="SCA-001",
                type=VulnerabilityType.OUTDATED_DEPENDENCY,
                severity=Severity.HIGH,
                title="Log4j Remote Code Execution",
                description="Apache Log4j 2.14.1 취약점 (Log4Shell)",
                location="pom.xml:45",
                cve_id="CVE-2021-44228",
                cvss_score=10.0,
                remediation="Log4j 2.17.0 이상으로 업그레이드"
            )
        ]

        self.vulnerabilities.extend(detected)
        return detected

    def run_secrets_scan(self, git_repo_path: str) -> List[Vulnerability]:
        """
        시크릿 스캔 실행

        Git 이력에서 하드코딩된 시크릿 탐지
        """
        detected = [
            Vulnerability(
                id="SECRET-001",
                type=VulnerabilityType.HARDCODED_SECRET,
                severity=Severity.CRITICAL,
                title="AWS Access Key in Commit",
                description="AWS 액세스 키가 커밋에 포함됨",
                location="commit:abc123 config/deploy.sh",
                remediation="시크릿 로테이션 후 Vault로 이관"
            )
        ]

        self.vulnerabilities.extend(detected)
        return detected

    def check_security_gate(self) -> SecurityGateResult:
        """
        보안 게이트 통과 여부 확인

        정책에 따른 취약점 허용 기준 검사
        """
        counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }

        blocked_reasons = []

        for vuln in self.vulnerabilities:
            if vuln.status == "Open":
                severity = vuln.severity.value.lower()
                if severity in counts:
                    counts[severity] += 1

        # 정책 검사
        if counts['critical'] > self.security_gate_policy['critical']:
            blocked_reasons.append(
                f"Critical 취약점 {counts['critical']}개 (허용: {self.security_gate_policy['critical']})"
            )

        if counts['high'] > self.security_gate_policy['high']:
            blocked_reasons.append(
                f"High 취약점 {counts['high']}개 (허용: {self.security_gate_policy['high']})"
            )

        if counts['medium'] > self.security_gate_policy['medium']:
            blocked_reasons.append(
                f"Medium 취약점 {counts['medium']}개 (허용: {self.security_gate_policy['medium']})"
            )

        passed = len(blocked_reasons) == 0

        return SecurityGateResult(
            passed=passed,
            total_vulnerabilities=sum(counts.values()),
            critical_count=counts['critical'],
            high_count=counts['high'],
            medium_count=counts['medium'],
            low_count=counts['low'],
            blocked_reasons=blocked_reasons
        )

    def generate_sbom(self, format: str = "CycloneDX") -> Dict:
        """
        SBOM (Software Bill of Materials) 생성

        소프트웨어 구성 요소 명세서
        """
        return {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "serialNumber": f"urn:uuid:{self.project_name}",
            "version": 1,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "component": {
                    "type": "application",
                    "name": self.project_name,
                    "version": "1.0.0"
                }
            },
            "components": [
                {
                    "type": "library",
                    "name": "spring-boot-starter-web",
                    "version": "2.7.0",
                    "purl": "pkg:maven/org.springframework.boot/spring-boot-starter-web@2.7.0"
                },
                {
                    "type": "library",
                    "name": "log4j-core",
                    "version": "2.17.0",
                    "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.17.0"
                }
            ],
            "vulnerabilities": [
                {
                    "id": vuln.cve_id,
                    "source": {"name": "NVD"},
                    "ratings": [{"severity": vuln.severity.value}],
                    "description": vuln.description
                }
                for vuln in self.vulnerabilities
                if vuln.cve_id
            ]
        }

class ThreatModelingEngine:
    """
    위협 모델링 엔진 (STRIDE 기반)
    """

    def analyze_threats(self, architecture_diagram: Dict) -> List[Dict]:
        """
        아키텍처 다이어그램에서 위협 식별
        """
        stride_mapping = {
            'S': 'Spoofing (스푸핑)',
            'T': 'Tampering (변조)',
            'R': 'Repudiation (부인)',
            'I': 'Information Disclosure (정보 유출)',
            'D': 'Denial of Service (서비스 거부)',
            'E': 'Elevation of Privilege (권한 상승)'
        }

        threats = []

        # 각 컴포넌트 분석
        for component in architecture_diagram.get('components', []):
            component_type = component.get('type')

            if component_type == 'web_server':
                threats.append({
                    'component': component['name'],
                    'stride_category': 'S',
                    'threat': '자격 증명 무차별 대입 공격',
                    'mitigation': '계정 잠금 정책, MFA 적용'
                })
                threats.append({
                    'component': component['name'],
                    'stride_category': 'I',
                    'threat': 'XSS를 통한 세션 탈취',
                    'mitigation': '입출력 인코딩, CSP 헤더'
                })

            elif component_type == 'database':
                threats.append({
                    'component': component['name'],
                    'stride_category': 'T',
                    'threat': 'SQL Injection',
                    'mitigation': 'PreparedStatement, ORM 사용'
                })
                threats.append({
                    'component': component['name'],
                    'stride_category': 'I',
                    'threat': '데이터베이스 덤프 유출',
                    'mitigation': '저장 데이터 암호화, 접근 제어'
                })

        return threats

    def calculate_risk(self, threat: Dict) -> Dict:
        """
        DREAD 모델로 위험도 계산

        D: Damage (피해 규모)
        R: Reproducibility (재현 가능성)
        E: Exploitability (악용 가능성)
        A: Affected Users (영향 사용자)
        D: Discoverability (발견 가능성)

        각 항목 1-10 점수, 평균으로 위험도 산출
        """
        # 예시 점수 (실제로는 전문가 평가)
        dread_scores = {
            'damage': 8,
            'reproducibility': 7,
            'exploitability': 9,
            'affected_users': 8,
            'discoverability': 6
        }

        risk_score = sum(dread_scores.values()) / len(dread_scores)

        if risk_score >= 8:
            risk_level = "Critical"
        elif risk_score >= 6:
            risk_level = "High"
        elif risk_score >= 4:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return {
            'threat': threat,
            'dread_scores': dread_scores,
            'risk_score': risk_score,
            'risk_level': risk_level
        }
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### Secure SDLC vs 전통적 보안 접근법

| 비교 차원 | 전통적 (Bolt-on) | Secure SDLC (Build-in) |
|----------|-----------------|----------------------|
| 보안 적용 시점 | 개발 후 (테스트/운영) | 개발 전 과정 |
| 취약점 발견 비용 | 높음 (운영 단계) | 낮음 (설계/구현 단계) |
| 수정 용이성 | 어려움 | 쉬움 |
| 보안 의식 | 보안팀만 | 전 구성원 |
| 자동화 수준 | 낮음 | 높음 (CI/CD 통합) |
| 규제 준수 | 사후 대응 | 선제적 준비 |

### 과목 융합 관점 분석

1. **소프트웨어 공학과의 융합**: Secure SDLC는 기존 SDLC에 보안 활동을 추가한 것. 요구사항 분석, 설계, 구현, 테스트 각 단계에 보안 체크포인트를 내장한다.

2. **데이터베이스와의 융합**: 저장 데이터 암호화, 접근 제어, 감사 로깅 등 DB 보안 기능과 연계. SQL Injection 방어를 위한 PreparedStatement, ORM 사용.

3. **네트워크와의 융합**: 전송 구간 암호화(TLS), 방화벽, WAF, 침입 탐지 시스템과 연계. 네트워크 분할, DMZ 구성 등.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오 및 기술사적 판단

**시나리오 1: 금융권 코어뱅킹 시스템**
- **상황**: 개인정보 1000만 건 처리, ISMS 인증 필수
- **기술사적 판단**:
  - Microsoft SDL 전체 단계 적용
  - 위협 모델링 필수, 외부 침투 테스트 연 2회
  - SAST/DAST/SCA 모든 파이프라인 통합
  - SBOM 생성 및 공급망 보안 관리
- **전략**: 보안 게이트 0-tolerance 정책

**시나리오 2: 스타트업 SaaS 서비스**
- **상황**: 빠른 출시 필요, 리소스 제약
- **기술사적 판단**:
  - OWASP CLASP 경량 모델 적용
  - CI/CD에 SAST/SCA만 통합
  - OWASP Top 10 중심 방어
  - 클라우드 보안 서비스 활용 (AWS Security Hub)
- **전략**: 핵심 취약점 우선 방어, 점진적 강화

### 안티패턴 (Anti-patterns)

1. **보안 병목**: 모든 코드를 보안팀이 리뷰해야 배포 가능. 개발 속도 저하.

2. **도구 과신**: 도구 도입만으로 해결되지 않음. 교육, 프로세스 변화가 선행되어야.

3. **1회성 스캔**: 배포 전 1회만 스캔하고 말음. 지속적 스캔이 필요.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | 미적용 시 | 적용 시 | 개선율 |
|----------|----------|--------|-------|
| 보안 결함 발견 비용 | 운영 단계 $7,600/개 | 설계 단계 $80/개 | 99% 절감 |
| 보안 사고 발생률 | 100% | 45% | 55% 감소 |
| 컴플라이언스 비용 | 높음 | 중간 | 40% 절감 |
| 취약점 수정 시간 | 30일 | 7일 | 77% 단축 |

### 참고 표준/가이드

| 표준 | 내용 | 출처 |
|------|------|------|
| Microsoft SDL | 7단계 보안 개발 프로세스 | Microsoft |
| OWASP CLASP | 경량级 보안 개발 프로세스 | OWASP |
| BSIMM | 보안 성숙도 모델 | Cigital |
| NIST SSDF | 안전한 소프트웨어 개발 프레임워크 | NIST |
| KISA 가이드 | 소프트웨어 개발 보안 가이드 (47개 약점) | KISA |

---

## 관련 개념 맵 (Knowledge Graph)

- [위협 모델링](./474_threat_modeling.md): STRIDE, DREAD 모델
- [OWASP Top 10](./477_owasp_top10.md): 주요 웹 보안 취약점
- [SAST/DAST](./491_492_sast_dast.md): 정적/동적 분석 도구
- [DevSecOps](./105_devsecops.md): Secure SDLC의 DevOps 확장
- [SBOM](./496_sbom.md): 소프트웨어 자재 명세서

---

## 어린이를 위한 3줄 비유 설명

1. **개념**: Secure SDLC는 집을 지을 때 처음부터 도둑이 못 들어오게 설계하는 것과 같아요. 나중에 "앗, 문이 없네?" 하고 달지 않고, 설계부터 튼튼한 문과 창문 잠금장치를 계획하는 거예요.

2. **원리**: 건축가(설계자)가 "이 창문은 1층이라 위험해"(위협 모델링)라고 말하고, 목수(개발자)는 "튼튼한 자물쇠를 달았어"(시큐어 코딩), 감독관(테스터)은 "따봉!"(보안 테스트) 하고 확인해요.

3. **효과**: 이렇게 하면 집이 완성된 후에 "도둑이 들어왔어!" 하고 비싼 보안 시스템을 설치할 필요가 없어요. 처음부터 안전한 집이니까 돈도 아끼고 마음도 편해요.
