+++
title = "형상 식별 (Configuration Identification)"
date = 2024-05-24
description = "소프트웨어 형상 항목을 정의, 명명, 문서화하여 형상 관리의 기반을 구축하는 핵심 활동"
weight = 20
+++

# 형상 식별 (Configuration Identification)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 형상 식별은 **소프트웨어 구성 요소 중 관리 대상이 되는 형상 항목(CI, Configuration Item)을 선정**하고, 각 항목에 **고유 식별자를 부여**하여 추적 가능하게 만드는 형상 관리(SCM)의 첫 번째 핵심 활동입니다.
> 2. **가치**: 체계적 형상 식별은 **변경 추적성 100% 보장, 버전 충돌 90% 감소, 감사 준비 시간 50% 단축** 효과를 제공하며, ISO 12207, CMMI의 필수 요구사항입니다.
> 3. **융합**: Git 기반 버전 관리, 컨테이너 이미지 태깅, SBOM(Software Bill of Materials) 생성과 연계되어 **DevOps 파이프라인의 식별 체계**로 진화했습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**형상 식별(Configuration Identification)**은 소프트웨어 형상 관리(SCM, Software Configuration Management)의 4대 핵심 활동(식별, 통제, 감사, 기록) 중 첫 번째로, **무엇을 관리할 것인가**를 정의하는 활동입니다. IEEE 828에 따르면 형상 식별은 다음을 포함합니다:

```
[형상 식별의 핵심 구성요소]

1. 형상 항목(CI) 선정
   - 어떤 산출물이 형상 관리 대상인가?
   - 소스코드, 문서, 빌드 스크립트, 테스트 케이스 등

2. 명명 규칙(Naming Convention) 수립
   - CI에 고유 식별자를 어떻게 부여할 것인가?
   - 버전 번호, 파일명 규칙, 브랜치명 규칙

3. 문서화(Documentation)
   - CI의 속성, 관계, 소유자를 어떻게 기록할 것인가?
   - 형상 관리 계획서(CMP), CI 목록

4. 기준선(Baseline) 정의
   - 언제 CI를 확정하고 변경 통제 대상으로 삼을 것인가?
   - 요구사항 기준선, 설계 기준선, 제품 기준선
```

**형상 항목(Configuration Item, CI)의 정의**:
> 형상 관리를 위해 명시적으로 지정된 소프트웨어 또는 하드웨어의 구성 요소로, **고유 식별자, 버전, 변경 이력**을 가지며 **형상 통제 위원회(CCB)의 승인 없이는 변경될 수 없는** 관리 대상입니다.

### 💡 일상생활 비유: 도서관의 책 관리 시스템

```
[형상 식별 = 도서관 책 등록 시스템]

도서관                         소프트웨어 형상 관리
======                        ====================
등록 대상 도서 선정             CI 선정
- 도서관 소장 결정              - 형상 관리 대상 결정

청구기호 부여                   명명 규칙 적용
- 001.23 = 분류 + 일련번호      - PROJ-MOD-001 = 프로젝트-모듈-번호

도서 정보 입력                  문서화
- 제목, 저자, 출판사, 위치       - 파일명, 작성자, 버전, 경로

대출/반납 기록 시작              기준선 설정
- 책이 확정되어 관리 시작        - CI가 확정되어 변경 통제 시작

예시:
도서: "클린 코드"              CI: "UserService.java"
청구기호: 005.1-CLE123         식별자: AUTH-SVC-001
버전: 2판                      버전: v2.3.1
위치: A열 3층                  경로: /src/services/auth/
```

### 2. 등장 배경 및 발전 과정

#### 1) 1960~70년대: 초기 형상 관리의 필요성
대규모 소프트웨어 프로젝트에서 **"어떤 버전의 코드가 배포되었는가?"**를 알 수 없는 혼란이 발생했습니다.

#### 2) 1970년대: SCCS, RCS 등 초기 도구
- **SCCS (Source Code Control System, 1972)**: 최초의 버전 관리 시스템
- **RCS (Revision Control System, 1982)**: 개별 파일 버전 관리

#### 3) 1980~90년대: 표준화
- **IEEE 828 (1983)**: 형상 관리 계획 표준
- **ISO 10007 (1995)**: 품질 관리 - 형상 관리 지침

#### 4) 2000년대~현재: 분산 버전 관리와 DevOps
- **Git (2005)**: 분산 버전 관리, 브랜치/태그 기반 식별
- **컨테이너/클라우드**: 이미지 태그, Helm Chart 버전
- **SBOM**: 소프트웨어 공급망 식별 체계

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 형상 식별 구성 요소

| 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 표준/도구 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **형상 항목(CI)** | 관리 대상 산출물 | 버전, 상태, 소유자 속성 | Git, SVN | 등록된 책 |
| **명명 규칙** | 고유 식별자 부여 | 프로젝트-유형-번호 체계 | 코딩 표준 | 청구기호 |
| **버전 번호** | 변경 이력 추적 | Semantic Versioning | Git Tags | 개정판 |
| **기준선(Baseline)** | 변경 통제 시작점 | 승인된 CI 집합 | CCB 승인 | 최초 등록 |
| **트레이서빌리티** | CI 간 관계 추적 | 요구-설계-코드-테스트 매핑 | RTM | 참고 문헌 |

### 2. 형상 항목(CI) 유형 및 선정 기준

```text
================================================================================
|                    CONFIGURATION ITEM HIERARCHY                              |
================================================================================

                        ┌─────────────────────────────────┐
                        │     SOFTWARE CONFIGURATION      │
                        │     (전체 형상 구성)              │
                        └────────────────┬────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        │                                │                                │
        v                                v                                v
┌───────────────┐              ┌───────────────┐              ┌───────────────┐
│  개발 산출물   │              │  관리 산출물   │              │  사용자 산출물 │
│ Development   │              │ Management    │              │ User          │
│ Deliverables  │              │ Documents     │              │ Documents     │
└───────┬───────┘              └───────┬───────┘              └───────┬───────┘
        │                              │                              │
   ┌────┴────┐                    ┌────┴────┐                    ┌────┴────┐
   │         │                    │         │                    │         │
   v         v                    v         v                    v         v
┌─────┐  ┌─────┐              ┌─────┐  ┌─────┐              ┌─────┐  ┌─────┐
│소스 │  │설계  │              │계획서│  │형상  │              │매뉴얼│  │교육  │
│코드 │  │문서  │              │     │  │계획서│              │     │  │자료  │
└─────┘  └─────┘              └─────┘  └─────┘              └─────┘  └─────┘
   │         │                    │         │                    │
   │    ┌────┴────┐               │         │                    │
   │    │         │               │         │                    │
   v    v         v               v         v                    v
┌─────┐┌─────┐┌─────┐         ┌─────┐┌─────┐               ┌─────┐
│Java ││UML  ││DB   │         │WBS  ││변경  │               │설치  │
│Files││Diag.││Schema│        │     ││요청서│               │가이드│
└─────┘└─────┘└─────┘         └─────┘└─────┘               └─────┘

[CI 선정 기준 체크리스트]
=========================================================
✅ 변경 가능성: 프로젝트 수행 중 변경될 가능성이 있는가?
✅ 추적 필요성: 요구사항/결함과의 추적이 필요한가?
✅ 재사용성: 다른 프로젝트에서 재사용할 가치가 있는가?
✅ 의존성: 다른 CI에 영향을 주거나 받는가?
✅ 계약적 중요성: 고객 인수 대상 산출물인가?
✅ 규제 준수: 감사/규제 검토 대상인가?
=========================================================
```

### 3. 명명 규칙(Naming Convention) 설계

```text
================================================================================
|                    CONFIGURATION ITEM NAMING CONVENTION                      |
================================================================================

[파일명 규칙]

형식: {프로젝트}_{유형}_{번호}_{버전}.{확장자}

예시:
┌──────────────────────────────────────────────────────────────────────┐
│ ECOM_REQ_001_v1.0.docx                                               │
│ │    │   │   │                                                       │
│ │    │   │   └── 버전 (v1.0)                                          │
│ │    │   └── 일련번호 (001)                                           │
│ │    └── 유형 (REQ=요구사항)                                          │
│ └── 프로젝트 (ECOM=이커머스)                                          │
└──────────────────────────────────────────────────────────────────────┘

유형 코드:
┌──────────┬─────────────────────┐
│ 코드      │ 설명                 │
├──────────┼─────────────────────┤
│ REQ      │ 요구사항 명세서       │
│ DES      │ 설계 문서            │
│ SRC      │ 소스 코드            │
│ TST      │ 테스트 케이스        │
│ MAN      │ 매뉴얼               │
│ PLN      │ 계획서               │
│ RPT      │ 보고서               │
└──────────┴─────────────────────┘


[브랜치명 규칙]

형식: {유형}/{이슈번호}-{간단한설명}

예시:
┌──────────────────────────────────────────────────────────────────────┐
│ feature/JIRA-123-add-user-auth                                       │
│ │       │   │                                                        │
│ │       │   └── 간단한 설명 (kebab-case)                              │
│ │       └── 이슈 추적 번호                                            │
│ └── 유형 (feature, bugfix, hotfix, release)                          │
└──────────────────────────────────────────────────────────────────────┘

브랜치 유형:
┌──────────────┬───────────────────────────────┐
│ 유형          │ 용도                           │
├──────────────┼───────────────────────────────┤
│ main/master  │ 프로덕션 배포용                │
│ develop      │ 개발 통합                      │
│ feature/*    │ 신규 기능 개발                 │
│ bugfix/*     │ 버그 수정                      │
│ hotfix/*     │ 긴급 수정                      │
│ release/*    │ 릴리스 준비                    │
└──────────────┴───────────────────────────────┘


[태그/버전 규칙 - Semantic Versioning]

형식: v{MAJOR}.{MINOR}.{PATCH}[-{PRERELEASE}][+{BUILD}]

예시:
┌──────────────────────────────────────────────────────────────────────┐
│ v2.3.1-rc.1+build.20240315                                          │
│ │ │ │ │     │                                                        │
│ │ │ │ │     └── 빌드 메타데이터                                       │
│ │ │ │ └── 사전 릴리스 (rc=Release Candidate)                          │
│ │ │ └── 패치 버전 (버그 수정 시 증가)                                  │
│ │ └── 마이너 버전 (기능 추가 시 증가)                                  │
│ └── 메이저 버전 (호환성 깨지는 변경 시 증가)                            │
└──────────────────────────────────────────────────────────────────────┘

버전 증가 규칙:
┌────────────┬─────────────────────────────────────┐
│ 증가 대상   │ 조건                                 │
├────────────┼─────────────────────────────────────┤
│ MAJOR      │ 호환되지 않는 API 변경               │
│ MINOR      │ 이전 버전 호환 기능 추가             │
│ PATCH      │ 이전 버전 호환 버그 수정             │
│ PRERELEASE │ alpha, beta, rc 등                   │
└────────────┴─────────────────────────────────────┘
```

### 4. 기준선(Baseline) 정의 및 관리

```text
================================================================================
|                    BASELINE DEFINITION & MANAGEMENT                          |
================================================================================

                        프로젝트 타임라인
                        =================

    시작        요구분석완료    설계완료        코딩완료       테스트완료    출시
      │              │             │              │             │          │
      │              │             │              │             │          │
      v              v             v              v             v          v
   ┌──────┐     ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐ ┌────────┐
   │ 계획 │     │ 요구사항│    │ 설계   │    │ 개발   │    │ 테스트 │ │ 제품   │
   │ 기준 │     │ 기준선 │    │ 기준선 │    │ 기준선 │    │ 기준선 │ │ 기준선 │
   │ 선   │     │ (FBL)  │    │ (DBL)  │    │ (CBL)  │    │ (TBL)  │ │ (PBL)  │
   └──────┘     └────────┘    └────────┘    └────────┘    └────────┘ └────────┘
      │              │             │              │             │          │
      │              │             │              │             │          │
   비공식         CCB승인       CCB승인        CCB승인       CCB승인     CCB승인
   관리          후 변경통제    후 변경통제    후 변경통제    후 변경통제  후 변경통제


[각 기준선 상세]

1. 기능적 기준선 (FBL - Functional Baseline)
   ┌────────────────────────────────────────────────────────────────────┐
   │ 정의: 요구사항 분석 완료 후 승인된 요구사항 명세서                    │
   │ 내용:                                                               │
   │   - SRS (Software Requirements Specification)                      │
   │   - 유스케이스 명세서                                                │
   │   - 비기능 요구사항 정의서                                           │
   │   - 인수 기준                                                       │
   │                                                                    │
   │ 관리: CCB 승인 후 변경 시 CR(Change Request) 필요                    │
   └────────────────────────────────────────────────────────────────────┘

2. 설계 기준선 (DBL - Design Baseline)
   ┌────────────────────────────────────────────────────────────────────┐
   │ 정의: 상세 설계 완료 후 승인된 설계 문서                              │
   │ 내용:                                                               │
   │   - 소프트웨어 아키텍처 문서                                         │
   │   - 상세 설계서 (클래스, 시퀀스 다이어그램)                          │
   │   - DB 설계서 (ERD, 스키마)                                         │
   │   - 인터페이스 정의서                                               │
   └────────────────────────────────────────────────────────────────────┘

3. 개발 기준선 (CBL - Code Baseline)
   ┌────────────────────────────────────────────────────────────────────┐
   │ 정의: 코딩 완료 후 버전 관리 시스템에 확정된 소스코드                   │
   │ 내용:                                                               │
   │   - 소스코드                                                        │
   │   - 단위 테스트 코드                                                │
   │   - 빌드 스크립트                                                   │
   │   - 정적 분석 결과                                                  │
   │                                                                    │
   │ Git 태그: v1.0.0-dev                                               │
   └────────────────────────────────────────────────────────────────────┘

4. 테스트 기준선 (TBL - Test Baseline)
   ┌────────────────────────────────────────────────────────────────────┐
   │ 정의: 시스템 테스트 완료 후 승인된 테스트 산출물                       │
   │ 내용:                                                               │
   │   - 테스트 계획서                                                   │
   │   - 테스트 케이스                                                   │
   │   - 테스트 결과 보고서                                              │
   │   - 결함 리포트                                                    │
   └────────────────────────────────────────────────────────────────────┘

5. 제품 기준선 (PBL - Product Baseline)
   ┌────────────────────────────────────────────────────────────────────┐
   │ 정의: 인수 테스트 완료 후 출시 준비가 된 최종 제품                     │
   │ 내용:                                                               │
   │   - 실행 가능한 소프트웨어                                          │
   │   - 사용자 매뉴얼                                                  │
   │   - 설치 가이드                                                    │
   │   - 릴리스 노트                                                    │
   │                                                                    │
   │ Git 태그: v1.0.0 (release)                                         │
   └────────────────────────────────────────────────────────────────────┘
```

### 5. 형상 식별 구현 코드 예시

```python
"""
형상 식별 시스템 구현
CI 관리, 명명 규칙 검증, 기준선 관리
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
import re

class CIType(Enum):
    """형상 항목 유형"""
    REQUIREMENT = "REQ"
    DESIGN = "DES"
    SOURCE = "SRC"
    TEST = "TST"
    DOCUMENT = "DOC"
    BUILD = "BLD"
    RELEASE = "REL"

class CIPStatus(Enum):
    """형상 항목 상태"""
    DRAFT = "draft"           # 작성 중
    REVIEWED = "reviewed"     # 검토 완료
    BASELINED = "baselined"   # 기준선 편입
    MODIFIED = "modified"     # 변경 중
    ARCHIVED = "archived"     # 보관

@dataclass
class Version:
    """버전 정보 (Semantic Versioning)"""
    major: int = 0
    minor: int = 0
    patch: int = 0
    prerelease: str = ""
    build: str = ""

    def __str__(self) -> str:
        version = f"v{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version

    def bump_major(self) -> 'Version':
        """메이저 버전 증가"""
        return Version(self.major + 1, 0, 0)

    def bump_minor(self) -> 'Version':
        """마이너 버전 증가"""
        return Version(self.major, self.minor + 1, 0)

    def bump_patch(self) -> 'Version':
        """패치 버전 증가"""
        return Version(self.major, self.minor, self.patch + 1)

@dataclass
class ConfigurationItem:
    """형상 항목"""
    id: str                           # 고유 식별자
    name: str                         # 항목명
    ci_type: CIType                   # 유형
    version: Version                  # 버전
    status: CIPStatus                 # 상태
    file_path: str                    # 파일 경로
    owner: str                        # 소유자
    created_date: datetime            # 생성 일시
    modified_date: datetime           # 수정 일시
    baseline: Optional[str] = None    # 소속 기준선
    dependencies: List[str] = field(default_factory=list)  # 의존 CI
    attributes: Dict = field(default_factory=dict)         # 추가 속성

    def get_identifier(self) -> str:
        """표준 식별자 생성"""
        return f"{self.ci_type.value}-{self.id}-{self.version}"

class NamingConvention:
    """명명 규칙 검증기"""

    # 파일명 패턴: PROJECT_TYPE_NUMBER_VERSION.EXT
    FILE_PATTERN = re.compile(
        r'^[A-Z]{2,6}_'           # 프로젝트 코드 (2~6자 대문자)
        r'[A-Z]{2,3}_'            # 유형 코드 (2~3자 대문자)
        r'\d{3}_'                 # 일련번호 (3자리 숫자)
        r'v\d+\.\d+\.\d+'         # 버전 (vX.Y.Z)
        r'\.[a-zA-Z0-9]+$'        # 확장자
    )

    # 브랜치명 패턴: type/ISSUE-description
    BRANCH_PATTERN = re.compile(
        r'^(feature|bugfix|hotfix|release)/'
        r'[A-Z]+-\d+-'
        r'[a-z0-9-]+$'
    )

    # 태그 패턴: vX.Y.Z[-prerelease][+build]
    TAG_PATTERN = re.compile(
        r'^v\d+\.\d+\.\d+'
        r'(?:-[a-zA-Z0-9.]+)?'
        r'(?:\+[a-zA-Z0-9.]+)?$'
    )

    @classmethod
    def validate_filename(cls, filename: str) -> tuple[bool, str]:
        """파일명 검증"""
        if cls.FILE_PATTERN.match(filename):
            return True, "Valid filename"
        return False, f"Invalid filename format: {filename}. Expected: PROJECT_TYPE_NUMBER_VERSION.EXT"

    @classmethod
    def validate_branch_name(cls, branch: str) -> tuple[bool, str]:
        """브랜치명 검증"""
        if cls.BRANCH_PATTERN.match(branch):
            return True, "Valid branch name"
        return False, f"Invalid branch name: {branch}. Expected: type/ISSUE-description"

    @classmethod
    def validate_tag(cls, tag: str) -> tuple[bool, str]:
        """태그 검증"""
        if cls.TAG_PATTERN.match(tag):
            return True, "Valid tag"
        return False, f"Invalid tag format: {tag}. Expected: vX.Y.Z[-prerelease][+build]"

@dataclass
class Baseline:
    """기준선"""
    id: str                           # 기준선 ID
    name: str                         # 기준선명 (FBL, DBL, PBL 등)
    version: str                      # 기준선 버전
    created_date: datetime            # 생성 일시
    created_by: str                   # 생성자
    cis: List[str] = field(default_factory=list)  # 포함된 CI 목록
    approved: bool = False            # CCB 승인 여부
    approval_date: Optional[datetime] = None

class ConfigurationManager:
    """형상 관리자"""

    def __init__(self, project_code: str):
        self.project_code = project_code
        self.configuration_items: Dict[str, ConfigurationItem] = {}
        self.baselines: Dict[str, Baseline] = {}
        self.ci_counter = 1

    def register_ci(self, name: str, ci_type: CIType,
                   file_path: str, owner: str) -> ConfigurationItem:
        """새로운 CI 등록"""
        ci_id = f"{ci_type.value}-{self.ci_counter:03d}"
        self.ci_counter += 1

        now = datetime.now()
        ci = ConfigurationItem(
            id=ci_id,
            name=name,
            ci_type=ci_type,
            version=Version(0, 1, 0),
            status=CIPStatus.DRAFT,
            file_path=file_path,
            owner=owner,
            created_date=now,
            modified_date=now
        )

        self.configuration_items[ci_id] = ci
        return ci

    def create_baseline(self, name: str, ci_ids: List[str],
                       created_by: str) -> Baseline:
        """기준선 생성"""
        baseline_id = f"BL-{name}-{len(self.baselines) + 1:03d}"

        baseline = Baseline(
            id=baseline_id,
            name=name,
            version="1.0",
            created_date=datetime.now(),
            created_by=created_by,
            cis=ci_ids
        )

        # CI 상태를 BASELINED로 변경
        for ci_id in ci_ids:
            if ci_id in self.configuration_items:
                self.configuration_items[ci_id].status = CIPStatus.BASELINED
                self.configuration_items[ci_id].baseline = baseline_id

        self.baselines[baseline_id] = baseline
        return baseline

    def approve_baseline(self, baseline_id: str) -> bool:
        """기준선 CCB 승인"""
        if baseline_id not in self.baselines:
            return False

        baseline = self.baselines[baseline_id]
        baseline.approved = True
        baseline.approval_date = datetime.now()
        return True

    def get_ci_report(self) -> Dict:
        """CI 현황 보고서 생성"""
        report = {
            "project": self.project_code,
            "total_cis": len(self.configuration_items),
            "by_type": {},
            "by_status": {},
            "baselines": len(self.baselines),
            "approved_baselines": sum(1 for b in self.baselines.values() if b.approved)
        }

        for ci in self.configuration_items.values():
            # 유형별 집계
            type_name = ci.ci_type.value
            report["by_type"][type_name] = report["by_type"].get(type_name, 0) + 1

            # 상태별 집계
            status_name = ci.status.value
            report["by_status"][status_name] = report["by_status"].get(status_name, 0) + 1

        return report

    def generate_sbom(self, baseline_id: str) -> Dict:
        """SBOM (Software Bill of Materials) 생성"""
        if baseline_id not in self.baselines:
            return {}

        baseline = self.baselines[baseline_id]
        sbom = {
            "sbom_version": "1.0",
            "baseline_id": baseline_id,
            "baseline_name": baseline.name,
            "creation_date": datetime.now().isoformat(),
            "components": []
        }

        for ci_id in baseline.cis:
            if ci_id in self.configuration_items:
                ci = self.configuration_items[ci_id]
                sbom["components"].append({
                    "id": ci.id,
                    "name": ci.name,
                    "version": str(ci.version),
                    "type": ci.ci_type.value,
                    "owner": ci.owner,
                    "path": ci.file_path
                })

        return sbom


# 사용 예시
if __name__ == "__main__":
    # 형상 관리자 생성
    cm = ConfigurationManager("ECOM")

    # CI 등록
    req_ci = cm.register_ci("요구사항 명세서", CIType.REQUIREMENT, "/docs/SRS.docx", "김기획")
    src_ci = cm.register_ci("UserService.java", CIType.SOURCE, "/src/UserService.java", "박개발")
    test_ci = cm.register_ci("로그인_테스트케이스", CIType.TEST, "/test/LoginTest.java", "이테스터")

    print("=== 등록된 CI ===")
    for ci_id, ci in cm.configuration_items.items():
        print(f"  {ci.get_identifier()} - {ci.name} [{ci.status.value}]")

    # 기준선 생성
    baseline = cm.create_baseline("FBL", [req_ci.id, src_ci.id, test_ci.id], "형상관리자")
    print(f"\n=== 기준선 생성 ===")
    print(f"  ID: {baseline.id}")
    print(f"  포함 CI: {len(baseline.cis)}개")

    # 명명 규칙 검증
    print("\n=== 명명 규칙 검증 ===")
    is_valid, msg = NamingConvention.validate_filename("ECOM_REQ_001_v1.0.0.docx")
    print(f"  파일명: {is_valid} - {msg}")

    is_valid, msg = NamingConvention.validate_branch_name("feature/JIRA-123-add-login")
    print(f"  브랜치명: {is_valid} - {msg}")

    is_valid, msg = NamingConvention.validate_tag("v1.2.3-rc.1+build.123")
    print(f"  태그: {is_valid} - {msg}")

    # 현황 보고서
    print("\n=== CI 현황 보고서 ===")
    report = cm.get_ci_report()
    for key, value in report.items():
        print(f"  {key}: {value}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 버전 관리 시스템별 식별 방식

| 비교 항목 | 중앙집중형(SVN) | 분산형(Git) | 클라우드(GitHub/GitLab) |
| :--- | :--- | :--- | :--- |
| **CI 식별** | 파일 경로 + 리비전 번호 | 파일 경로 + 커밋 해시 | + PR 번호 |
| **기준선 표시** | Tags, Branches | Tags, Branches | + Releases |
| **명명 규칙** | 서버 정책 | 로컬+원격 정책 | Organization 정책 |
| **추적성** | 리비전 간 diff | 커밋 그래프 | + Issue 연동 |
| **협업 식별** | Lock/Unlock | Branch per Feature | + Fork/PR |

### 2. 과목 융합 관점 분석

#### 형상 식별 + 요구사항 관리

```
[요구사항-형상 추적성]

요구사항 ID ──────────────> CI ID
    │                          │
    │ 1:N 매핑                 │
    │                          │
    v                          v
REQ-001 ─────────────────> SRC-UserService
    │                          │
    │ 검증                      │ 구현
    v                          v
TST-LoginTest ◄────────────┘

RTM(Requirements Traceability Matrix)와 CI 식별 연계:
┌────────────┬─────────────┬──────────────┐
│ 요구사항    │ 설계 CI      │ 소스 CI       │
├────────────┼─────────────┼──────────────┤
│ REQ-001    │ DES-Auth-01 │ SRC-Auth-001 │
│ REQ-002    │ DES-DB-01   │ SRC-DAO-001  │
└────────────┴─────────────┴──────────────┘
```

#### 형상 식별 + DevOps

```
[CI/CD 파이프라인에서의 식별]

Source Stage:
  Git Commit Hash → CI 식별자
  Branch Name → 환경 식별자
  Tag → Release 식별자

Build Stage:
  Build Number → 아티팩트 버전
  Docker Image Tag → 컨테이너 식별자

Deploy Stage:
  Helm Chart Version → 배포 식별자
  Environment Name → 환경 식별자

예시:
  commit: a1b2c3d → image: myapp:v1.2.3-a1b2c3d
  branch: release/1.2 → env: production
  tag: v1.2.3 → deployment: myapp-1.2.3
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오] 대형 공공 프로젝트의 형상 식별 체계 수립**

**상황**:
- 규모: 50인, 24개월, 500개 이상 산출물
- 요구: 감사 대상, 추적성 필수
- 환경: SVN + Jira + Jenkins

**기술사적 판단**:
```
형상 식별 체계 설계:

1. CI 선정 기준
   - 모든 인수 산출물 → 필수 CI
   - 내부 문서 → 선택적 CI
   - 임시 산출물 → 비CI

2. 명명 규칙
   파일명: {PJT}_{TYPE}_{NO}_{VER}.{EXT}
   예: G2B_REQ_001_v1.0.docx

   폴더구조:
   /G2B
   ├── 01_요구사항/{TYPE}_{NO}_{VER}
   ├── 02_설계/{TYPE}_{NO}_{VER}
   ├── 03_구현/{MODULE}/{TYPE}_{NO}_{VER}
   ├── 04_테스트/{TYPE}_{NO}_{VER}
   └── 05_배포/{TYPE}_{NO}_{VER}

3. 기준선 정의
   - FBL: 요구사항 검토회의 완료 시점
   - DBL: 설계 검토회의 완료 시점
   - PBL: 인수 테스트 완료 시점

4. 자동화
   - 커밋 메시지에 Jira 이슈 번호 필수
   - Jenkins 빌드 번호와 SVN 리비전 연동
   - 자동 CI 목록 생성

5. 감사 대응
   - 분기별 CI 목록 보고서 자동 생성
   - 기준선별 스냅샷 보관
   - 변경 이력 추적 보고서
```

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**:
- [ ] **버전 관리 도구 선정**: SVN vs Git (프로젝트 특성 고려)
- [ ] **명명 규칙 템플릿**: 프로젝트 코드, 유형 코드 정의
- [ ] **자동화 도구**: pre-commit hook, CI 연동
- [ ] **백업 전략**: CI 저장소 백업 및 복구

**운영적 고려사항**:
- [ ] **교육 계획**: 팀원 대상 명명 규칙 교육
- [ ] **감사 체계**: 정기 CI 감사 일정
- [ ] **변경 통제**: CCB 운영 절차
- [ ] **도구 관리자**: 형상 관리 도구 관리자 지정

### 3. 주의사항 및 안티패턴

| 안티패턴 | 증상 | 해결 방안 |
| :--- | :--- | :--- |
| **과도한 CI 선정** | 모든 파일을 CI로 지정 | 선정 기준 명확화 |
| **불일치한 명명** | 팀원마다 다른 규칙 사용 | pre-commit hook 강제 |
| **기준선 누락** | 변경 통제 없이 계속 수정 | CCB 프로세스 정착 |
| **식별자 중복** | 같은 ID의 다른 파일 | 중복 검사 자동화 |
| **버전 번호 혼란** | 임의 버전 번호 부여 | Semantic Versioning 채택 |

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | 적용 전 | 적용 후 | 개선 효과 |
| :--- | :--- | :--- | :--- | :--- |
| **추적성** | 요구-코드 매핑률 | 30% | 100% | +70%p |
| **감사 대응** | 준비 시간 | 5일 | 1일 | -80% |
| **버전 충돌** | 월간 충돌 건수 | 20건 | 2건 | -90% |
| **변경 관리** | 미승인 변경 | 10건/월 | 0건 | -100% |
| **생산성** | 산출물 검색 시간 | 30분 | 3분 | -90% |

### 2. 미래 전망 및 진화 방향

1. **AI 기반 식별 자동화**
   - 자동 CI 선정 추천
   - 명명 규칙 위반 자동 수정
   - 의존성 자동 분석

2. **SBOM 의무화 대응**
   - 소프트웨어 공급망 투명성
   - 오픈소스 라이선스 추적
   - 취약점 관리 연계

3. **클라우드 네이티브 식별**
   - 컨테이너 이미지 서명
   - IaC 상태 추적
   - 멀티클라우드 식별 체계

### ※ 참고 표준/가이드

- **IEEE 828**: Configuration Management Plans
- **ISO/IEC 12207**: Software Life Cycle Processes
- **ISO 10007**: Quality Management - Configuration Management
- **CMMI V2.0**: Configuration Management Process Area

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [형상 통제](@/studynotes/4_software_engineering/1_sdlc/21_configuration_control.md) : 식별된 CI의 변경 관리
- [형상 감사](@/studynotes/4_software_engineering/1_sdlc/23_configuration_audit.md) : CI 무결성 검증
- [버전 관리](@/studynotes/4_software_engineering/1_sdlc/configuration_management.md) : CI 버전 이력 관리
- [기준선 관리](@/studynotes/4_software_engineering/1_sdlc/baseline_management.md) : 확정된 CI 집합 관리
- [DevOps](@/studynotes/4_software_engineering/1_sdlc/devops.md) : CI/CD 파이프라인 식별

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 여러 친구가 함께 숙제를 하는데, 누가 어떤 부분을 했는지 모르면 엉망이 돼요. 마지막에 합칠 때도 어떤 게 최신인지 모르고요!

2. **해결(형상 식별)**: 모든 숙제 파일에 "누가, 언제, 무슨 버전인지" 이름표를 붙여요. 예를 들어 "철수_수학_1판_0315"처럼요. 그러면 어떤 게 최신인지 바로 알 수 있죠!

3. **효과**: 이름표가 있으면 실수로 옛날 파일을 쓰는 일이 없어요. 선생님이 "누가 이거 고쳤어?"라고 물어도 바로 찾을 수 있죠. 마치 도서관에서 책을 찾을 때 책 번호를 보는 것과 같아요!
