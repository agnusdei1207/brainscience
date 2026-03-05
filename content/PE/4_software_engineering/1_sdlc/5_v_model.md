+++
title = "V-모델 (V-Model)"
date = 2024-05-24
description = "개발 단계와 테스트 단계를 대칭 구조로 매핑한 SDLC 모델"
weight = 50
+++

# V-모델 (V-Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: V-모델은 **폭포수 모델을 확장**하여 각 개발 단계에 대응하는 **테스트 단계를 V자형으로 매핑**한 SDLC 모델로, 요구사항→인수테스트, 설계→시스템테스트, 코딩→단위테스트의 **검증(Verification)과 확인(Validation)**을 체계화합니다.
> 2. **가치**: **안전 중요 시스템(항공, 원자력, 의료기기, 자동차)**에서 필수적으로 적용되며, 각 단계별 산출물에 대한 **추적성(Traceability)**을 보장하여 결함을 조기에 발견하고 **규제 인증(DO-178C, IEC 61508)**을 획득할 수 있습니다.
> 3. **융합**: 폭포수 모델의 순차적 특성을 유지하면서 **테스트 활동을 병렬로 계획**할 수 있어, 현대에는 **V-Model + 애자일(하이브리드)** 형태로도 적용됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**V-모델(V-Model)**은 소프트웨어 개발의 각 단계를 **V자 모양으로 배치**하고, 좌측(개발) 단계와 우측(테스트) 단계를 **수평으로 매핑**한 생명주기 모델입니다. 1990년대 독일에서 정부 프로젝트용으로 개발되었으며, 현재는 **안전 중요 시스템의 사실상 표준**으로 자리잡았습니다.

**V-모델의 핵심 개념**:

| 개념 | 설명 |
| :--- | :--- |
| **V자 구조** | 좌측 하향: 개발 단계, 우측 상향: 테스트 단계 |
| **수평 매핑** | 요구사항↔인수테스트, 설계↔시스템테스트 등 |
| **검증(Verification)** | "제품을 올바르게 만들고 있는가?" (과정 중심) |
| **확인(Validation)** | "올바른 제품을 만들었는가?" (결과 중심) |
| **추적성(Traceability)** | 요구사항→설계→코드→테스트 간의 연결 |

**V-모델의 단계 구성**:

```
                    V-모델 단계 구조
    ========================================================

    [좌측: 개발 단계]              [우측: 테스트 단계]

    요구사항 분석 ─────────────────────────────> 인수 테스트
           │                                        ▲
           │ 요구사항 명세서                        │ 인수 테스트 계획
           │ (SRS)                                 │ (ATP)
           │                                        │
           v                                        │
    시스템 설계 ─────────────────────────────> 시스템 테스트
           │                                        ▲
           │ 시스템 설계서                          │ 시스템 테스트 계획
           │ (SDD)                                 │ (STP)
           │                                        │
           v                                        │
    아키텍처 설계 ───────────────────────────> 통합 테스트
           │                                        ▲
           │ 아키텍처 문서                          │ 통합 테스트 계획
           │                                        │ (ITP)
           │                                        │
           v                                        │
    상세 설계 ───────────────────────────────> 단위 테스트
           │                                        ▲
           │ 상세 설계서                            │ 단위 테스트 계획
           │                                        │ (UTP)
           │                                        │
           v                                        │
    ═════════════════════════════════════════════════
                       코딩 (Coding)
    ═════════════════════════════════════════════════

    [핵심 원칙]
    1. 각 개발 단계에서 대응하는 테스트 계획을 작성
    2. 테스트 계획은 해당 단계의 산출물을 기준으로 작성
    3. 추적성 매트릭스로 요구사항-테스트 간 연결 유지
```

### 💡 일상생활 비유: 건축과 검수 과정

```
[V-모델 = 건축 설계와 검수 매핑]

건축 과정 (좌측)                 검수 과정 (우측)
============                     ===============
설계도 그리기 ───────────────────> 최종 입주 검수
    │                                   ▲
    │ "방 3개, 욕실 2개"                 │ "요청한 대로 되었나?"
    v                                   │
구조 설계 ─────────────────────────> 구조 안전 검사
    │                                   ▲
    │ 기둥, 보 설계                      │ "무너지지 않나?"
    v                                   │
전기/설비 설계 ─────────────────────> 전기/설비 검사
    │                                   ▲
    │ 콘센트, 파이프 배치                 │ "제대로 작동하나?"
    v                                   │
상세 시공도 ───────────────────────> 방별 마감 검사
    │                                   ▲
    │ 벽지, 바닥재                       │ "스크래치 없나?"
    v                                   │
════════════════════════════════════════════
              실제 시공 (코딩)
════════════════════════════════════════════

핵심:
- 설계할 때 이미 "어떻게 검사할지"도 함께 계획!
- "방 3개"라고 설계했으면, 검수 때 "방이 3개인가?" 확인
- 설계와 검수가 1:1로 대응
```

### 2. 등장 배경 및 발전 과정

#### 1) 1980년대: 폭포수 모델의 한계 인식

**폭포수 모델의 문제점**:
```
요구사항 → 설계 → 코딩 → 테스트
                           ↑
                      여기서 문제 발견!

문제:
1. 테스트 계획이 코딩 후에 수립됨
2. 요구사항 누락이 인수 테스트에서 발견됨
3. 재작업 비용이 막대함
```

#### 2) 1990년대: V-모델 등장

**독일 V-모델 (V-Model 97)**:
- 독일 연방정부 IT 프로젝트용으로 개발
- IABG(Informationstechnische Gesellschaft) 주도
- 공식 명칭: "Entwicklungsstandard für IT-Systeme des Bundes"

**핵심 혁신**:
- 각 개발 단계에서 **테스트 계획을 병행 작성**
- 개발과 테스트의 **추적성 확보**
- **조기 결함 발견** 가능

#### 3) 2000년대~현재: 안전 표준으로 정착

| 표준 | 적용 분야 | V-모델 요구사항 |
| :--- | :--- | :--- |
| **DO-178C** | 항공 소프트웨어 | 요구사항-테스트 추적성 필수 |
| **IEC 61508** | 기능 안전 | V-모델 기반 개발 프로세스 |
| **ISO 26262** | 자동차 기능 안전 | ASIL 등급별 V-모델 적용 |
| **IEC 62304** | 의료기기 소프트웨어 | 소프트웨어 생명주기 V-모델 |
| **EN 50128** | 철도 제어 소프트웨어 | 안전 등급별 V-모델 |

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. V-모델 단계별 상세 구조

| 단계 | 입력 | 활동 | 산출물 | 대응 테스트 |
| :--- | :--- | :--- | :--- | :--- |
| **요구사항 분석** | 사용자 요구 | 요구사항 도출, 분석 | SRS, 유스케이스 | 인수 테스트 계획 |
| **시스템 설계** | SRS | 시스템 구조, 인터페이스 | 시스템 설계서 | 시스템 테스트 계획 |
| **아키텍처 설계** | 시스템 설계서 | 모듈 분할, 아키텍처 | 아키텍처 문서 | 통합 테스트 계획 |
| **상세 설계** | 아키텍처 문서 | 모듈 상세, 알고리즘 | 상세 설계서 | 단위 테스트 계획 |
| **코딩** | 상세 설계서 | 프로그래밍 | 소스코드 | - |
| **단위 테스트** | 소스코드, UTP | 모듈 테스트 | 테스트 결과 | 상세 설계 검증 |
| **통합 테스트** | 단위 테스트 완료 | 모듈 통합 테스트 | 테스트 결과 | 아키텍처 검증 |
| **시스템 테스트** | 통합 테스트 완료 | 시스템 기능/비기능 | 테스트 결과 | 시스템 설계 검증 |
| **인수 테스트** | 시스템 테스트 완료 | 사용자 요구 검증 | 최종 승인 | 요구사항 검증 |

### 2. 정교한 구조 다이어그램: V-모델 전체 구조

```text
================================================================================
|                        V-MODEL COMPLETE ARCHITECTURE                         |
================================================================================

                         ┌─────────────────────────────────┐
                         │        요구사항 분석            │
                         │   (Requirements Analysis)       │
                         │                                 │
                         │   • 사용자 요구 도출            │
                         │   • 기능/비기능 요구사항        │
                         │   • 유스케이스 작성             │
                         │                                 │
                         │   산출물: SRS                   │
                         └───────────────┬─────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              │                          v                          │
              │            ┌─────────────────────────────────┐      │
              │            │         시스템 설계              │      │
              │            │    (System Design)              │      │
              │            │                                 │      │
              │            │   • 시스템 구조 정의            │      │
              │            │   • 하드웨어/소프트웨어 할당    │      │
              │            │   • 인터페이스 정의             │      │
              │            │                                 │      │
              │            │   산출물: SDD, 인터페이스 명세  │      │
              │            └───────────────┬─────────────────┘      │
              │                            │                        │
              │                            v                        │
              │              ┌─────────────────────────────────┐    │
              │              │       아키텍처 설계              │    │
              │              │    (Architecture Design)        │    │
              │              │                                 │    │
              │              │   • 소프트웨어 아키텍처         │    │
              │              │   • 모듈 분할                   │    │
              │              │   • 컴포넌트 정의               │    │
              │              │                                 │    │
              │              │   산출물: 아키텍처 문서         │    │
              │              └───────────────┬─────────────────┘    │
              │                              │                      │
              │                              v                      │
              │                ┌─────────────────────────────────┐  │
              │                │         상세 설계               │  │
              │                │    (Detailed Design)            │  │
              │                │                                 │  │
              │                │   • 모듈 상세 설계              │  │
              │                │   • 알고리즘 설계               │  │
              │                │   • 데이터 구조                 │  │
              │                │                                 │  │
              │                │   산출물: 상세 설계서           │  │
              │                └───────────────┬─────────────────┘  │
              │                                │                    │
              │                                v                    │
              │                  ┌───────────────────────────────┐  │
              │                  │           코딩                │  │
              │                  │        (Coding)               │  │
              │                  │                               │  │
              │                  │   • 프로그래밍                │  │
              │                  │   • 코드 리뷰                 │  │
              │                  │   • 정적 분석                 │  │
              │                  │                               │  │
              │                  │   산출물: 소스코드            │  │
              │                  └───────────────┬───────────────┘  │
              │                                  │                  │
              │                                  v                  │
              │                    ┌─────────────────────────────┐  │
              │                    │        단위 테스트          │  │
              │                    │     (Unit Testing)          │  │
              │                    │                             │  │
              │                    │   • 모듈 단위 검증          │  │
              │                    │   • 화이트박스 테스트       │  │
              │                    │   • 구문/분기 커버리지      │  │
              │                    │                             │  │
              │                    │   검증: 상세 설계           │  │
              │                    └───────────────┬─────────────┘  │
              │                                    │                │
              │                                    v                │
              │                      ┌───────────────────────────┐  │
              │                      │       통합 테스트         │  │
              │                      │   (Integration Testing)   │  │
              │                      │                           │  │
              │                      │   • 모듈 간 인터페이스    │  │
              │                      │   • 컴포넌트 통합         │  │
              │                      │   • 상향/하향 통합        │  │
              │                      │                           │  │
              │                      │   검증: 아키텍처 설계     │  │
              │                      └───────────────┬───────────┘  │
              │                                      │              │
              │                                      v              │
              │                        ┌─────────────────────────┐  │
              │                        │     시스템 테스트       │  │
              │                        │  (System Testing)       │  │
              │                        │                         │  │
              │                        │   • 기능 테스트         │  │
              │                        │   • 비기능 테스트       │  │
              │                        │   • 성능, 보안, 회귀    │  │
              │                        │                         │  │
              │                        │   검증: 시스템 설계     │  │
              │                        └───────────────┬─────────┘  │
              │                                        │            │
              │                                        v            │
              │                          ┌───────────────────────┐  │
              │                          │     인수 테스트       │  │
              │                          │  (Acceptance Testing) │  │
              │                          │                       │  │
              │                          │   • 사용자 요구 검증  │  │
              │                          │   • 비즈니스 시나리오 │  │
              │                          │   • UAT               │  │
              │                          │                       │  │
              │                          │   검증: 요구사항      │  │
              │                          └───────────────────────┘  │
              │                                                      │
              └──────────────────────────────────────────────────────┘

================================================================================
|                    HORIZONTAL MAPPING (수평 매핑)                           |
================================================================================

    요구사항 분석 ◄═══════════════════════════════════► 인수 테스트
         │                                                   ▲
         │ SRS                                               │ ATP
         │                                                   │
         └───────────────> 추적성 매트릭스 <─────────────────┘

    시스템 설계 ◄═════════════════════════════════════► 시스템 테스트
         │                                                   ▲
         │ SDD                                               │ STP
         │                                                   │
         └───────────────> 추적성 매트릭스 <─────────────────┘

    아키텍처 설계 ◄═══════════════════════════════════► 통합 테스트
         │                                                   ▲
         │ 아키텍처 문서                                      │ ITP
         │                                                   │
         └───────────────> 추적성 매트릭스 <─────────────────┘

    상세 설계 ◄═══════════════════════════════════════► 단위 테스트
         │                                                   ▲
         │ 상세 설계서                                        │ UTP
         │                                                   │
         └───────────────> 추적성 매트릭스 <─────────────────┘

================================================================================
|                    VERIFICATION vs VALIDATION                               |
================================================================================

    검증 (Verification)                    확인 (Validation)
    ==================                    ==================
    "제품을 올바르게                      "올바른 제품을
     만들고 있는가?"                       만들었는가?"

    • 과정 중심                           • 결과 중심
    • 요구사항 → 설계 일치                • 사용자 요구 충족
    • 설계 → 코드 일치                    • 비즈니스 목표 달성
    • 리뷰, 인스펙션                      • 인수 테스트
    • 정적 분석                           • 사용자 시연

    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │   V&V (Verification & Validation)                           │
    │   = "제품을 올바르게 만들고, 올바른 제품을 만들었는가?"      │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

================================================================================
```

### 3. 심층 동작 원리: 추적성 매트릭스

V-모델의 핵심은 **요구사항-설계-코드-테스트 간의 추적성**입니다.

```
[추적성 매트릭스 (Traceability Matrix)]

                 시스템                아키텍처              상세설계              코드               테스트
    요구사항      설계                  설계                 (모듈)              (TC)
    ══════════════════════════════════════════════════════════════════════════════════════════════
    RQ-001    │ SD-001           │ AD-001,002        │ DD-001..005      │ M1,M2,M3         │ TC-001..010
    RQ-002    │ SD-001,002       │ AD-003            │ DD-006..008      │ M4,M5            │ TC-011..015
    RQ-003    │ SD-003           │ AD-004,005        │ DD-009..012      │ M6,M7,M8         │ TC-016..025
    ...       │ ...              │ ...               │ ...              │ ...              │ ...

    [수직 추적성 (Vertical Traceability)]
    RQ-001 → SD-001 → AD-001 → DD-001 → M1 → TC-001

    [수평 추적성 (Horizontal Traceability)]
    RQ-001 ◄═══════════════════════════════════════════════► TC-001..010

    [활용 목적]
    1. 결함 분석: TC-005 실패 → RQ-001 문제?
    2. 변경 영향: RQ-001 변경 → SD, AD, DD, M, TC 모두 수정 필요?
    3. 커버리지: 모든 요구사항이 테스트되었는가?
    4. 감사 대응: 증거 자료 제시
```

### 4. 핵심 알고리즘/공식 & 실무 코드 예시

#### V-모델 추적성 매트릭스 관리 시스템

```python
"""
V-모델 추적성 매트릭스 관리 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from enum import Enum
from datetime import datetime

class ArtifactType(Enum):
    """산출물 유형"""
    REQUIREMENT = "요구사항"
    SYSTEM_DESIGN = "시스템설계"
    ARCHITECTURE_DESIGN = "아키텍처설계"
    DETAILED_DESIGN = "상세설계"
    CODE = "코드"
    TEST_CASE = "테스트케이스"

class TestPhase(Enum):
    """테스트 단계"""
    UNIT = "단위테스트"
    INTEGRATION = "통합테스트"
    SYSTEM = "시스템테스트"
    ACCEPTANCE = "인수테스트"

@dataclass
class Artifact:
    """산출물"""
    id: str
    type: ArtifactType
    name: str
    description: str
    version: str = "1.0"
    status: str = "작성중"
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class TestCase:
    """테스트 케이스"""
    id: str
    name: str
    phase: TestPhase
    description: str
    preconditions: List[str] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    expected_result: str = ""
    actual_result: str = ""
    status: str = "미실행"  # 미실행, 통과, 실패

@dataclass
class TraceLink:
    """추적 링크"""
    source_id: str
    source_type: ArtifactType
    target_id: str
    target_type: ArtifactType
    link_type: str  # "satisfies", "implements", "verifies"

class VModelTraceability:
    """V-모델 추적성 관리"""

    def __init__(self):
        self.artifacts: Dict[str, Artifact] = {}
        self.test_cases: Dict[str, TestCase] = {}
        self.trace_links: List[TraceLink] = []

    def add_artifact(self, artifact: Artifact):
        """산출물 추가"""
        self.artifacts[artifact.id] = artifact

    def add_test_case(self, test_case: TestCase):
        """테스트 케이스 추가"""
        self.test_cases[test_case.id] = test_case

    def create_trace_link(self, source_id: str, target_id: str, link_type: str):
        """추적 링크 생성"""
        source = self.artifacts.get(source_id) or self.test_cases.get(source_id)
        target = self.artifacts.get(target_id) or self.test_cases.get(target_id)

        if not source or not target:
            raise ValueError("소스 또는 타겟 산출물을 찾을 수 없습니다")

        source_type = source.type if isinstance(source, Artifact) else ArtifactType.TEST_CASE
        target_type = target.type if isinstance(target, Artifact) else ArtifactType.TEST_CASE

        self.trace_links.append(TraceLink(
            source_id=source_id,
            source_type=source_type,
            target_id=target_id,
            target_type=target_type,
            link_type=link_type
        ))

    def get_forward_trace(self, artifact_id: str) -> List[str]:
        """전방 추적: 요구사항 → 테스트"""
        traced = []
        for link in self.trace_links:
            if link.source_id == artifact_id:
                traced.append(link.target_id)
                # 재귀적 추적
                traced.extend(self.get_forward_trace(link.target_id))
        return list(set(traced))

    def get_backward_trace(self, artifact_id: str) -> List[str]:
        """후방 추적: 테스트 → 요구사항"""
        traced = []
        for link in self.trace_links:
            if link.target_id == artifact_id:
                traced.append(link.source_id)
                # 재귀적 추적
                traced.extend(self.get_backward_trace(link.source_id))
        return list(set(traced))

    def get_requirements_without_tests(self) -> List[str]:
        """테스트가 없는 요구사항 식별"""
        requirements = [a.id for a in self.artifacts.values()
                       if a.type == ArtifactType.REQUIREMENT]

        tested_requirements = set()
        for tc in self.test_cases.values():
            traced = self.get_backward_trace(tc.id)
            for req_id in traced:
                if req_id in requirements:
                    tested_requirements.add(req_id)

        return [r for r in requirements if r not in tested_requirements]

    def get_test_coverage(self) -> Dict:
        """테스트 커버리지 계산"""
        requirements = [a for a in self.artifacts.values()
                       if a.type == ArtifactType.REQUIREMENT]

        covered = 0
        coverage_detail = {}

        for req in requirements:
            traced_tests = [tc for tc in self.test_cases.values()
                          if req.id in self.get_forward_trace(req.id)]
            coverage_detail[req.id] = {
                "name": req.name,
                "test_count": len(traced_tests),
                "test_ids": [tc.id for tc in traced_tests],
                "covered": len(traced_tests) > 0
            }
            if traced_tests:
                covered += 1

        return {
            "total_requirements": len(requirements),
            "covered_requirements": covered,
            "coverage_percentage": (covered / len(requirements) * 100) if requirements else 0,
            "detail": coverage_detail
        }

    def impact_analysis(self, artifact_id: str) -> Dict:
        """변경 영향도 분석"""
        impacted = self.get_forward_trace(artifact_id)
        impacted_artifacts = []
        impacted_tests = []

        for id in impacted:
            if id in self.artifacts:
                impacted_artifacts.append({
                    "id": id,
                    "type": self.artifacts[id].type.value,
                    "name": self.artifacts[id].name
                })
            elif id in self.test_cases:
                impacted_tests.append({
                    "id": id,
                    "phase": self.test_cases[id].phase.value,
                    "name": self.test_cases[id].name
                })

        return {
            "changed_artifact": artifact_id,
            "impacted_artifacts": impacted_artifacts,
            "impacted_tests": impacted_tests,
            "total_impacted": len(impacted)
        }

    def generate_traceability_matrix(self) -> str:
        """추적성 매트릭스 생성 (마크다운)"""
        requirements = [a for a in self.artifacts.values()
                       if a.type == ArtifactType.REQUIREMENT]

        md = "# 추적성 매트릭스\n\n"
        md += "| 요구사항 ID | 요구사항 명 | 테스트 케이스 |\n"
        md += "|-------------|-------------|---------------|\n"

        for req in requirements:
            tests = [tc.id for tc in self.test_cases.values()
                    if req.id in self.get_forward_trace(req.id)]
            md += f"| {req.id} | {req.name} | {', '.join(tests) if tests else '없음'} |\n"

        return md


# 사용 예시
if __name__ == "__main__":
    vmodel = VModelTraceability()

    # 요구사항 추가
    vmodel.add_artifact(Artifact("RQ-001", ArtifactType.REQUIREMENT, "사용자 로그인", "사용자가 ID/PW로 로그인한다"))
    vmodel.add_artifact(Artifact("RQ-002", ArtifactType.REQUIREMENT, "상품 검색", "사용자가 상품을 검색한다"))

    # 설계 문서 추가
    vmodel.add_artifact(Artifact("SD-001", ArtifactType.SYSTEM_DESIGN, "인증 시스템 설계", ""))
    vmodel.add_artifact(Artifact("DD-001", ArtifactType.DETAILED_DESIGN, "로그인 모듈 설계", ""))

    # 코드 추가
    vmodel.add_artifact(Artifact("M-001", ArtifactType.CODE, "LoginModule", ""))

    # 테스트 케이스 추가
    vmodel.add_test_case(TestCase(
        "TC-001", "로그인 성공 테스트", TestPhase.ACCEPTANCE,
        "유효한 ID/PW로 로그인"
    ))
    vmodel.add_test_case(TestCase(
        "TC-002", "로그인 실패 테스트", TestPhase.ACCEPTANCE,
        "잘못된 PW로 로그인"
    ))

    # 추적 링크 생성
    vmodel.create_trace_link("RQ-001", "SD-001", "satisfies")
    vmodel.create_trace_link("SD-001", "DD-001", "refines")
    vmodel.create_trace_link("DD-001", "M-001", "implements")
    vmodel.create_trace_link("RQ-001", "TC-001", "verifies")
    vmodel.create_trace_link("RQ-001", "TC-002", "verifies")

    # 커버리지 확인
    coverage = vmodel.get_test_coverage()
    print(f"=== 테스트 커버리지 ===")
    print(f"전체 요구사항: {coverage['total_requirements']}")
    print(f"테스트된 요구사항: {coverage['covered_requirements']}")
    print(f"커버리지: {coverage['coverage_percentage']:.1f}%")

    # 테스트 없는 요구사항
    missing = vmodel.get_requirements_without_tests()
    print(f"\n테스트 없는 요구사항: {missing}")

    # 영향도 분석
    impact = vmodel.impact_analysis("RQ-001")
    print(f"\n=== RQ-001 변경 영향도 ===")
    print(f"영향받는 산출물: {len(impact['impacted_artifacts'])}")
    print(f"영향받는 테스트: {len(impact['impacted_tests'])}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: V-모델 vs 폭포수 vs 애자일

| 비교 항목 | 폭포수 | V-모델 | 애자일 |
| :--- | :--- | :--- | :--- |
| **테스트 계획** | 코딩 후 | 개발 단계와 병행 | 스프린트 내 |
| **추적성** | 암시적 | **명시적/필수** | 선택적 |
| **결함 발견** | 후반 | 단계별 | 지속적 |
| **문서화** | 상세 | **매우 상세** | 최소 |
| **규제 대응** | 가능 | **최적** | 어려움 |
| **안전 인증** | 가능 | **필수** | 부적합 |
| **변경 비용** | 높음 | 높음 | 낮음 |
| **적합 분야** | SI | 안전 중요 | 웹/스타트업 |

### 2. 과목 융합 관점 분석

#### V-모델 + DO-178C (항공 소프트웨어 표준)

```
[DO-178C와 V-모델 매핑]

DO-178C 목표                   V-모델 단계
============                   ===========
요구사항 기반 테스트            인수 테스트 ↔ 요구사항 분석
   ↓
설계 기반 테스트               시스템/통합 테스트 ↔ 설계
   ↓
코드 기반 테스트               단위 테스트 ↔ 상세 설계/코딩

[DO-178C 필수 산출물]
┌────────────────────────────────────────────┐
│ 요구사항 관련                               │
│ - 시스템 요구사항                           │
│ - 소프트웨어 요구사항 (SRS)                 │
│ - 요구사항 추적성                           │
├────────────────────────────────────────────┤
│ 설계 관련                                   │
│ - 소프트웨어 설계 설명서 (SDD)              │
│ - 설계 추적성                               │
├────────────────────────────────────────────┤
│ 코드 관련                                   │
│ - 소스코드                                  │
│ - 컴파일된 오브젝트 코드                    │
│ - 코드 추적성                               │
├────────────────────────────────────────────┤
│ 테스트 관련                                 │
│ - 테스트 케이스                             │
│ - 테스트 절차                               │
│ - 테스트 결과                               │
│ - 테스트 추적성                             │
└────────────────────────────────────────────┘

[안전 등급별 요구사항]
DAL A (재앙적): MC/DC 커버리지 100%
DAL B (위험한): 결정 커버리지 100%
DAL C (중대한): 구문 커버리지 100%
DAL D (경미한): 커버리지 권장
DAL E (효과 없음): 커버리지 요구 없음
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오 1] 항공 전자 시스템 개발**

**상황**:
- 시스템: 항공기 비행 제어 소프트웨어
- 등급: DAL B (위험한)
- 인증: DO-178C 필수

**기술사적 판단**:
```
선택: V-모델 + DO-178C

근거:
1. 법적 요구: 항공기 소프트웨어는 DO-178C 인증 필수
2. 추적성: 목표별로 산출물과 증거가 필요
3. 독립 검증: IV&V(Independent V&V) 수행
4. 커버리지: 결정 커버리지 100% 달성

단계별 적용:
- 요구사항: DO-178C Objective 기반
- 설계: 구조적 설계 방법
- 코딩: MISRA-C 표준
- 테스트: 자동화된 커버리지 측정
```

**[시나리오 2] 일반 웹 서비스 개발**

**상황**:
- 서비스: 전자상거래 플랫폼
- 시장: 빠른 출시 필요
- 인증: 요구 없음

**기술사적 판단**:
```
선택: 애자일 (V-모델 부적합)

V-모델이 부적합한 이유:
1. 오버헤드: 추적성 매트릭스 관리 비용
2. 유연성 부족: 변경에 취약
3. 출시 속도: 문서화 중심으로 인한 지연

대안: 스크럼 + 자동화된 테스트
- 요구사항: 사용자 스토리
- 테스트: 자동화된 E2E 테스트
- 추적성: 간소화된 형태
```

### 2. 도입 시 고려사항 (체크리스트)

**V-모델 적합성 체크리스트**:

| 항목 | 예 | 아니오 |
| :--- | :---: | :---: |
| 안전 인증이 필요한가? (DO-178C, IEC 61508 등) | □ | □ |
| 규제 기관 감사가 예상되는가? | □ | □ |
| 완전한 추적성이 요구되는가? | □ | □ |
| 결함의 비용이 매우 높은가? (인명, 재산 피해) | □ | □ |
| 요구사항이 안정적인가? | □ | □ |
| 문서화 투자가 가능한가? | □ | □ |

→ 4개 이상 '예'면 V-모델 권장

### 3. 주의사항 및 안티패턴

| 안티패턴 | 설명 | 해결 방안 |
| :--- | :--- | :--- |
| **추적성 누락** | 링크를 제대로 관리하지 않음 | 도구 활용, 정기 감사 |
| **문서만 작성** | 실제 테스트와 문서 불일치 | 검증 활동 의무화 |
| **후반 테스트** | 테스트 계획을 나중에 작성 | 개발 단계에서 병행 작성 |
| **커버리지 부족** | 요구사항이 테스트되지 않음 | 커버리지 분석 자동화 |

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | 일반 개발 | V-모델 적용 | 개선 효과 |
| :--- | :--- | :--- | :--- | :--- |
| **추적성** | 요구사항-테스트 매핑 | 50% | 100% | +50%p |
| **결함 발견** | 전 단계 발견률 | 40% | 85% | +45%p |
| **재작업** | 비용 비중 | 35% | 10% | -25%p |
| **인증** | 1회 통과율 | 30% | 80% | +50%p |
| **감사** | 준비 시간 | 4주 | 3일 | -90% |

### 2. 미래 전망 및 진화 방향

1. **자동화된 추적성 관리**
   - AI 기반 요구사항-코드 매핑
   - 자동 추적성 매트릭스 생성

2. **하이브리드 V-모델**
   - 안전 중요 부분: V-모델
   - 일반 부분: 애자일
   - "V-모델 + 스크럼" 결합

3. **모델 기반 개발 (MBD)**
   - Simulink 등 모델 기반
   - 자동 코드 생성
   - 모델 레벨 테스트

### ※ 참고 표준/가이드

- **DO-178C**: 항공 소프트웨어 개발 표준
- **IEC 61508**: 기능 안전 표준
- **ISO 26262**: 자동차 기능 안전
- **IEC 62304**: 의료기기 소프트웨어 생명주기
- **EN 50128**: 철도 제어 소프트웨어

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [SDLC](@/studynotes/4_software_engineering/1_sdlc/3_sdlc.md) : V-모델의 상위 개념
- [폭포수 모델](@/studynotes/4_software_engineering/1_sdlc/4_waterfall_model.md) : V-모델의 기반 모델
- [소프트웨어 테스팅](@/studynotes/4_software_engineering/5_testing/_index.md) : V-모델 우측 단계
- [요구사항 명세](@/studynotes/4_software_engineering/2_requirement/_index.md) : V-모델 시작점
- [형상 관리](@/studynotes/4_software_engineering/1_sdlc/configuration_management.md) : 추적성 관리 지원
- [CMMI](@/studynotes/4_software_engineering/1_sdlc/cmmi.md) : 프로세스 성숙도 모델

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 숙제를 하고 선생님께 검사받는데, 무엇을 검사해야 하는지 모르겠어요! "방학 숙제 다 했어?"라고 물어보면 뭐가 뭔지 모르겠죠?

2. **해결(V-모델)**: V-모델은 숙제 목록과 검사 목록을 짝지어놓은 거예요! "독서 감상문" 숙제가 있으면, 그에 맞는 "독서 감상문 검사"도 함께 계획하는 거죠. 숙제를 내면서 이미 어떻게 검사할지도 정해둬요!

3. **효과**: 이렇게 하면 숙제를 빠뜨리거나, 검사를 잘못하는 일이 없어요! 비행기나 자동차 같이 아주 중요한 것들을 만들 때 이 방법을 써요. 안전하니까요!
