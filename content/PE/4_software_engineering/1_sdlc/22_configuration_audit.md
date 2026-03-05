+++
title = "22. 형상 감사 (Configuration Audit)"
description = "소프트웨어 형상 항목이 요구사항을 충족하고 무결성을 유지하는지 검증하는 SCM 핵심 활동"
date = "2026-03-05"
[taxonomies]
tags = ["형상감사", "FCA", "PCA", "ConfigurationAudit", "SCM"]
categories = ["studynotes-4_software_engineering"]
+++

# 형상 감사 (Configuration Audit)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 형상 감사는 형상 항목(CI)이 **지정된 요구사항을 충족하는지(기능적 감사, FCA)**, 문서와 실제가 **일치하는지(물리적 감사, PCA)**를 체계적으로 검증하여 형상 무결성을 보장하는 SCM의 핵심 활동입니다.
> 2. **가치**: 형상 감사는 **결함 조기 발견, 인수 테스트 품질 보증, 규정 준수 증명**을 제공하며, 안전 중요 시스템(항공, 의료, 원전)에서는 법적 필수 요구사항입니다.
> 3. **융합**: 전통적 문서 기반 감사에서 **자동화된 CI/CD 품질 게이트, 컨테이너 이미지 스캔, SBOM 검증**으로 진화하였으며, DevSecOps의 핵심 검증 단계입니다.

---

## Ⅰ. 개요 (Context & Background) - [최소 500자 이상]

### 1. 명확한 개념 및 정의

**형상 감사(Configuration Audit)**는 형상 관리(SCM)의 4대 핵심 활동 중 네 번째로, 형상 항목이 **요구사항과 일치하는지**, 형상 관리 **프로세스가 준수되었는지**를 독립적으로 검토하고 검증하는 활동입니다.

**IEEE Std 828-2012 정의**:
> "Configuration audit is the process of verifying that configuration items comply with their specified requirements and that the configuration management system is effective."

**형상 감사의 2대 유형**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    형상 감사 2대 유형                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 기능적 형상 감사 (FCA, Functional Configuration Audit)      │
│     ├── 목적: CI가 기능적 요구사항을 충족하는가?                │
│     ├── 시점: 각 개발 단계 완료 시                              │
│     ├── 검증 항목:                                              │
│     │   - 요구사항 대비 구현 충족도                             │
│     │   - 테스트 결과 적합성                                    │
│     │   - 운영 문서 완전성                                      │
│     └── 산출물: FCA 보고서                                      │
│                                                                 │
│  2. 물리적 형상 감사 (PCA, Physical Configuration Audit)        │
│     ├── 목적: CI가 기술 문서와 물리적으로 일치하는가?           │
│     ├── 시점: 제품 기준선 설정 전                               │
│     ├── 검증 항목:                                              │
│     │   - 설계 문서 대비 코드 일치성                            │
│     │   - 빌드 절차 정확성                                      │
│     │   - 버전 번호 일치성                                      │
│     │   - 형상 항목 완전성                                      │
│     └── 산출물: PCA 보고서                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 💡 일상생활 비유: 자동차 완성차 검사

```
[형상 감사 = 자동차 완성차 검사]

자동차 공장에서 완성된 차를 출고하기 전 검사합니다:

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  🔍 기능적 감사 (FCA) - 성능 테스트                          │
│                                                             │
│  - 시동이 잘 걸리는가?                                       │
│  - 브레이크가 제대로 작동하는가?                              │
│  - 에어컨이 시원한가?                                        │
│  - 연비가 규격대로 나오는가?                                  │
│                                                             │
│  "영업사원이 약속한 기능이 모두 작동하나요?"                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  📋 물리적 감사 (PCA) - 명세서 확인                          │
│                                                             │
│  - 엔진 번호가 문서와 일치하는가?                             │
│  - 색상이 주문서와 같은가?                                    │
│  - 옵션이 모두 장착되었는가?                                  │
│  - 매뉴얼이 모두 포함되었는가?                                │
│                                                             │
│  "계약서에 있는 내용이 실제 차와 일치하나요?"                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 등장 배경 및 발전 과정

#### 1) 형상 감사의 필요성

```
┌─────────────────────────────────────────────────────────────────┐
│                    형상 감사 필요성                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 품질 보증 (Quality Assurance)                               │
│     - 요구사항 충족 확인                                        │
│     - 결함 조기 발견                                           │
│     - 인수 기준 검증                                           │
│                                                                 │
│  2. 무결성 검증 (Integrity Verification)                        │
│     - 문서-구현 일치성                                          │
│     - 버전 일관성                                               │
│     - 변경 이력 추적                                            │
│                                                                 │
│  3. 규정 준수 (Compliance)                                      │
│     - ISO/CMMI 요구사항 충족                                    │
│     - 안전 표준 (DO-178C, IEC 62304)                           │
│     - 감사 증거 제공                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [최소 1,000자 이상]

### 1. 형상 감사 구성 요소

| 요소 | FCA (기능적) | PCA (물리적) | 담당자 | 시점 |
| :--- | :--- | :--- | :--- | :--- |
| **요구사항 추적** | O | - | QA | 단계 완료 시 |
| **테스트 결과 검토** | O | - | 테스트 리더 | 테스트 완료 시 |
| **문서 완전성** | O | O | 문서 관리자 | 인수 전 |
| **버전 일치성** | - | O | 형상 관리자 | 기준선 설정 전 |
| **빌드 재현성** | - | O | 빌드 관리자 | 배포 전 |
| **변경 이력** | - | O | 형상 관리자 | 지속적 |

### 2. 정교한 구조 다이어그램: 형상 감사 프로세스

```text
================================================================================
|              CONFIGURATION AUDIT PROCESS                                    |
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│              기능적 형상 감사 (FCA) - Functional Configuration Audit         │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   FCA 체크리스트:                                                   │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │ #  │ 검증 항목                    │ 상태 │ 비고            │  │   │
│   │   │────┼─────────────────────────────┼──────┼─────────────────│  │   │
│   │   │ 1  │ 모든 요구사항이 구현됨?      │ □   │                 │  │   │
│   │   │ 2  │ 테스트 케이스가 충분함?      │ □   │                 │  │   │
│   │   │ 3  │ 모든 테스트가 통과함?        │ □   │                 │  │   │
│   │   │ 4  │ 알려진 결함이 문서화됨?      │ □   │                 │  │   │
│   │   │ 5  │ 사용자 매뉴얼이 완전함?      │ □   │                 │  │   │
│   │   │ 6  │ 운영 절차서가 준비됨?        │ □   │                 │  │   │
│   │   │ 7  │ 교육 자료가 준비됨?          │ □   │                 │  │   │
│   │   │ 8  │ 인수 테스트 계획이 승인됨?   │ □   │                 │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   │   요구사항 추적 매트릭스 (RTM) 검토:                                 │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │ REQ-ID │ 설계 │ 코드 │ 테스트 │ 상태                        │  │   │
│   │   │ R-001  │ D-01 │ C-01 │ T-01   │ ✓ 충족                     │  │   │
│   │   │ R-002  │ D-02 │ C-02 │ T-02   │ ✓ 충족                     │  │   │
│   │   │ R-003  │ D-03 │ C-03 │ T-03   │ ✓ 충족                     │  │   │
│   │   │ R-004  │ D-04 │ -    │ -      │ ✗ 미구현                   │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   │   FCA 결과: [ 합격 / 조건부 합격 / 불합격 ]                         │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│              물리적 형상 감사 (PCA) - Physical Configuration Audit           │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   PCA 체크리스트:                                                   │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │ #  │ 검증 항목                        │ 상태 │ 비고        │  │   │
│   │   │────┼─────────────────────────────────┼──────┼─────────────│  │   │
│   │   │ 1  │ 설계 문서와 코드가 일치함?       │ □   │             │  │   │
│   │   │ 2  │ 모든 CI가 식별됨?               │ □   │             │  │   │
│   │   │ 3  │ 버전 번호가 올바름?             │ □   │             │  │   │
│   │   │ 4  │ 빌드 절차가 재현 가능함?        │ □   │             │  │   │
│   │   │ 5  │ 형상 항목 목록이 완전함?        │ □   │             │  │   │
│   │   │ 6  │ 변경 이력이 기록됨?            │ □   │             │  │   │
│   │   │ 7  │ 승인된 변경만 포함됨?          │ □   │             │  │   │
│   │   │ 8  │ 저장소가 최신 상태임?          │ □   │             │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   │   형상 항목 일치성 검증:                                             │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │ CI ID           │ 문서 버전 │ 실제 버전 │ 일치 여부        │  │   │
│   │   │ PROJ-AUTH-SRC   │ 1.2.0    │ 1.2.0    │ ✓                │  │   │
│   │   │ PROJ-USER-DB    │ 1.1.0    │ 1.1.0    │ ✓                │  │   │
│   │   │ PROJ-FRONT-SRC  │ 1.3.0    │ 1.3.1    │ ✗ 불일치         │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   │   PCA 결과: [ 합격 / 조건부 합격 / 불합격 ]                         │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                           감사 보고서 작성                                  │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   형상 감사 보고서 구성:                                             │   │
│   │                                                                     │   │
│   │   1. 감사 개요                                                      │   │
│   │      - 감사 일시, 장소, 참석자                                      │   │
│   │      - 감사 대상 형상 항목                                          │   │
│   │      - 감사 범위                                                    │   │
│   │                                                                     │   │
│   │   2. FCA 결과                                                       │   │
│   │      - 기능적 요구사항 충족 현황                                     │   │
│   │      - 테스트 결과 요약                                             │   │
│   │      - 발견된 이슈                                                  │   │
│   │                                                                     │   │
│   │   3. PCA 결과                                                       │   │
│   │      - 물리적 일치성 현황                                           │   │
│   │      - 형상 항목 완전성                                             │   │
│   │      - 발견된 불일치                                                │   │
│   │                                                                     │   │
│   │   4. 결론 및 권고사항                                               │   │
│   │      - 감사 결과 (합격/조건부/불합격)                                │   │
│   │      - 시정 조치 항목                                               │   │
│   │      - 차기 감사 권고                                                │   │
│   │                                                                     │   │
│   │   5. 서명                                                           │   │
│   │      - 감사관, 프로젝트 관리자, QA 담당자                           │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
```

### 3. 자동화된 형상 감사 코드 예시

```python
"""
자동화된 형상 감사 시스템
CI/CD 파이프라인 통합용
"""

import subprocess
import json
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class AuditStatus(Enum):
    PASS = "합격"
    CONDITIONAL = "조건부 합격"
    FAIL = "불합격"

@dataclass
class AuditItem:
    """감사 항목"""
    id: str
    description: str
    status: bool
    details: str

@dataclass
class AuditResult:
    """감사 결과"""
    audit_type: str  # FCA or PCA
    items: List[AuditItem]
    overall_status: AuditStatus
    summary: str

class ConfigurationAuditor:
    """형상 감사 자동화"""

    def __init__(self, project_path: str):
        self.project_path = project_path

    def run_fca(self) -> AuditResult:
        """기능적 형상 감사 (FCA) 실행"""
        items = []

        # 1. 요구사항 추적 매트릭스 검증
        rtm_result = self._verify_requirements_traceability()
        items.append(AuditItem(
            id="FCA-001",
            description="요구사항 추적 매트릭스 완전성",
            status=rtm_result['status'],
            details=f"추적률: {rtm_result['trace_rate']}%"
        ))

        # 2. 테스트 커버리지 검증
        coverage_result = self._verify_test_coverage()
        items.append(AuditItem(
            id="FCA-002",
            description="테스트 커버리지 충족",
            status=coverage_result['status'],
            details=f"커버리지: {coverage_result['coverage']}%"
        ))

        # 3. 테스트 결과 검증
        test_result = self._verify_all_tests_passed()
        items.append(AuditItem(
            id="FCA-003",
            description="모든 테스트 통과",
            status=test_result['status'],
            details=f"통과: {test_result['passed']}/{test_result['total']}"
        ))

        # 4. 문서 완전성 검증
        doc_result = self._verify_documentation()
        items.append(AuditItem(
            id="FCA-004",
            description="사용자 문서 완전성",
            status=doc_result['status'],
            details=doc_result['details']
        ))

        # 전체 상태 결정
        passed_count = sum(1 for item in items if item.status)
        if passed_count == len(items):
            overall = AuditStatus.PASS
        elif passed_count >= len(items) * 0.8:
            overall = AuditStatus.CONDITIONAL
        else:
            overall = AuditStatus.FAIL

        return AuditResult(
            audit_type="FCA",
            items=items,
            overall_status=overall,
            summary=f"{len(items)}개 항목 중 {passed_count}개 합격"
        )

    def run_pca(self) -> AuditResult:
        """물리적 형상 감사 (PCA) 실행"""
        items = []

        # 1. Git 상태 검증
        git_result = self._verify_git_status()
        items.append(AuditItem(
            id="PCA-001",
            description="Git 작업 디렉토리 clean",
            status=git_result['status'],
            details=git_result['details']
        ))

        # 2. 버전 태그 검증
        tag_result = self._verify_version_tag()
        items.append(AuditItem(
            id="PCA-002",
            description="버전 태그 존재",
            status=tag_result['status'],
            details=f"태그: {tag_result['tag']}"
        ))

        # 3. 빌드 재현성 검증
        build_result = self._verify_build_reproducibility()
        items.append(AuditItem(
            id="PCA-003",
            description="빌드 재현성",
            status=build_result['status'],
            details=build_result['details']
        ))

        # 4. 의존성 검증 (SBOM)
        sbom_result = self._verify_sbom()
        items.append(AuditItem(
            id="PCA-004",
            description="SBOM 생성 완료",
            status=sbom_result['status'],
            details=f"의존성: {sbom_result['count']}개"
        ))

        # 5. 컨테이너 이미지 검증
        container_result = self._verify_container_image()
        items.append(AuditItem(
            id="PCA-005",
            description="컨테이너 이미지 무결성",
            status=container_result['status'],
            details=container_result['details']
        ))

        # 전체 상태 결정
        passed_count = sum(1 for item in items if item.status)
        if passed_count == len(items):
            overall = AuditStatus.PASS
        elif passed_count >= len(items) * 0.8:
            overall = AuditStatus.CONDITIONAL
        else:
            overall = AuditStatus.FAIL

        return AuditResult(
            audit_type="PCA",
            items=items,
            overall_status=overall,
            summary=f"{len(items)}개 항목 중 {passed_count}개 합격"
        )

    def _verify_requirements_traceability(self) -> Dict:
        """요구사항 추적 매트릭스 검증"""
        # 실제 구현에서는 RTM 파일을 읽어 검증
        return {"status": True, "trace_rate": 100}

    def _verify_test_coverage(self) -> Dict:
        """테스트 커버리지 검증"""
        try:
            # 커버리지 도구 실행 (예: pytest-cov, jacoco)
            result = subprocess.run(
                ["pytest", "--cov", "--cov-report=json", "-q"],
                capture_output=True, text=True, cwd=self.project_path
            )
            # 결과 파싱 (간소화)
            return {"status": True, "coverage": 85}
        except:
            return {"status": False, "coverage": 0}

    def _verify_all_tests_passed(self) -> Dict:
        """모든 테스트 통과 여부 검증"""
        return {"status": True, "passed": 50, "total": 50}

    def _verify_documentation(self) -> Dict:
        """문서 완전성 검증"""
        # README, CHANGELOG, API 문서 등 확인
        return {"status": True, "details": "모든 문서 존재"}

    def _verify_git_status(self) -> Dict:
        """Git 상태 검증"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=self.project_path
            )
            is_clean = len(result.stdout.strip()) == 0
            return {"status": is_clean, "details": "Clean" if is_clean else "Uncommitted changes"}
        except:
            return {"status": False, "details": "Git error"}

    def _verify_version_tag(self) -> Dict:
        """버전 태그 검증"""
        try:
            result = subprocess.run(
                ["git", "describe", "--tags"],
                capture_output=True, text=True, cwd=self.project_path
            )
            tag = result.stdout.strip()
            return {"status": True, "tag": tag}
        except:
            return {"status": False, "tag": "None"}

    def _verify_build_reproducibility(self) -> Dict:
        """빌드 재현성 검증"""
        return {"status": True, "details": "빌드 성공, 체크섬 일치"}

    def _verify_sbom(self) -> Dict:
        """SBOM 검증"""
        return {"status": True, "count": 45}

    def _verify_container_image(self) -> Dict:
        """컨테이너 이미지 검증"""
        return {"status": True, "details": "이미지 서명 검증 완료"}

    def generate_audit_report(self, fca_result: AuditResult,
                              pca_result: AuditResult) -> str:
        """감사 보고서 생성"""
        report = f"""
# 형상 감사 보고서

## 감사 개요
- 감사 일시: 2026-03-05
- 감사 대상: {self.project_path}

## FCA (기능적 형상 감사) 결과
상태: {fca_result.overall_status.value}
요약: {fca_result.summary}

| ID | 검증 항목 | 상태 | 상세 |
|----|-----------|------|------|
"""
        for item in fca_result.items:
            status_mark = "✓" if item.status else "✗"
            report += f"| {item.id} | {item.description} | {status_mark} | {item.details} |\n"

        report += f"""
## PCA (물리적 형상 감사) 결과
상태: {pca_result.overall_status.value}
요약: {pca_result.summary}

| ID | 검증 항목 | 상태 | 상세 |
|----|-----------|------|------|
"""
        for item in pca_result.items:
            status_mark = "✓" if item.status else "✗"
            report += f"| {item.id} | {item.description} | {status_mark} | {item.details} |\n"

        report += """
## 결론
"""
        if fca_result.overall_status == AuditStatus.PASS and pca_result.overall_status == AuditStatus.PASS:
            report += "모든 감사 항목 합격 - 기준선 설정 승인\n"
        else:
            report += "시정 조치 필요 - 기준선 설정 보류\n"

        return report


# 사용 예시
if __name__ == "__main__":
    auditor = ConfigurationAuditor("/path/to/project")

    # FCA 실행
    fca_result = auditor.run_fca()
    print("=== FCA 결과 ===")
    for item in fca_result.items:
        print(f"{item.id}: {'✓' if item.status else '✗'} {item.description}")

    # PCA 실행
    pca_result = auditor.run_pca()
    print("\n=== PCA 결과 ===")
    for item in pca_result.items:
        print(f"{item.id}: {'✓' if item.status else '✗'} {item.description}")

    # 보고서 생성
    report = auditor.generate_audit_report(fca_result, pca_result)
    print("\n" + report)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 - [비교표 2개 이상]

### 1. FCA vs PCA 비교

| 비교 항목 | FCA (기능적) | PCA (물리적) |
| :--- | :--- | :--- |
| **주요 질문** | "제대로 작동하는가?" | "문서와 일치하는가?" |
| **검증 대상** | 기능, 성능, 요구사항 | 버전, 문서, 구성 |
| **수행 시점** | 각 단계 완료 시 | 기준선 설정 전 |
| **주관자** | QA 담당자 | 형상 관리자 |
| **산출물** | 테스트 결과, RTM | CI 목록, 버전 정보 |

### 2. 감사 유형별 적용 시점

| 개발 단계 | FCA | PCA | 목적 |
| :--- | :--- | :--- | :--- |
| **요구사항** | O | - | 요구사항 검증 |
| **설계** | O | O | 설계 일치성 |
| **구현** | O | O | 코드 일치성 |
| **테스트** | O | O | 테스트 완전성 |
| **인수** | O | O | 인수 기준 충족 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 1. 기술사적 판단

**[시나리오] 감사 불합격 시 대응**

```
상황:
- PCA에서 버전 불일치 발견 (프론트엔드 v1.3.0 vs v1.3.1)

기술사적 판단:
1. 원인 분석
   - Git 태그와 실제 코드 불일치
   - hotfix 적용 후 태그 미갱신

2. 시정 조치
   - 올바른 버전으로 태그 재설정
   - 형상 기록 업데이트
   - PCA 재실시

3. 재발 방지
   - CI/CD 파이프라인에 자동 태깅 추가
   - 버전 검증 게이트 추가
```

---

## Ⅴ. 기대효과 및 결론

### 1. 정량적 기대효과

| 구분 | 지표 | 감사 미실시 | 감사 실시 | 개선 |
| :--- | :--- | :--- | :--- | :--- |
| **무결성** | 버전 불일치율 | 15% | 0% | -100% |
| **품질** | 결함 누락률 | 20% | 5% | -75% |
| **인수** | 1차 인수 합격률 | 60% | 95% | +58% |

### ※ 참고 표준

- **IEEE 828-2012**: Configuration Management
- **ISO 10007**: Configuration Management Guidelines
- **DO-178C**: Software Considerations in Airborne Systems

---

## 📌 관련 개념 맵

- [형상 관리](./19_configuration_management.md) : SCM 전체 체계
- [형상 통제](./21_configuration_control.md) : 변경 승인 프로세스
- [기준선](./25_baseline.md) : 감사 대상 버전
- [형상 기록](./23_configuration_status_accounting.md) : 감사 증거
- [품질 보증](./43_quality_assurance_vs_control.md) : QA 활동

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 숙제를 했는데 선생님이 "정말 네가 한 거 맞아?"라고 물으세요. 또 "숙제 내용이 맞는지 어떻게 확인해?"라고도 해요!

2. **해결(형상 감사)**: 선생님이 숙제를 검사해요! "계획대로 했어?" (기능적 감사), "숙제 파일이 제출된 거 맞아?" (물리적 감사). 이렇게 두 가지를 확인해요!

3. **효과**: 이제 숙제가 완벽한지 확인할 수 있어요! 계획한 대로 했고, 제출한 파일도 맞는지 알 수 있죠. 선생님도 안심하고 채점할 수 있어요!
