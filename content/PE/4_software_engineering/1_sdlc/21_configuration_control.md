+++
title = "21. 형상 통제 (Configuration Control)"
description = "형상 항목의 변경을 체계적으로 관리하고 승인하는 SCM 핵심 활동"
date = "2026-03-05"
[taxonomies]
tags = ["형상통제", "CCB", "ChangeControl", "변경관리", "SCM"]
categories = ["studynotes-4_software_engineering"]
+++

# 형상 통제 (Configuration Control)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 형상 통제는 **기준선(Baseline)이 설정된 형상 항목(CI)에 대한 변경 요청을 체계적으로 심사, 승인, 구현, 검증**하는 과정으로, **변경 통제 위원회(CCB)**가 핵심 의사결정 기구입니다.
> 2. **가치**: 효과적인 형상 통제는 **무결성 100% 보장, 범위 크리프 80% 방지, 변경 관련 결함 70% 감소**를 달성하며, 특히 안전 중요 시스템에서 법적 필수 요구사항입니다.
> 3. **융합**: 전통적 CCB에서 **Git Pull Request/Merge Request, 코드 리뷰, 자동화된 품질 게이트**로 진화하였으며, DevOps의 변경 승인 프로세스와 통합됩니다.

---

## Ⅰ. 개요 (Context & Background) - [최소 500자 이상]

### 1. 명확한 개념 및 정의

**형상 통제(Configuration Control)**는 형상 관리(SCM)의 4대 핵심 활동 중 두 번째로, **기준선(Baseline)으로 설정된 형상 항목(CI)에 대한 변경을 체계적으로 관리**하는 활동입니다. 형상 식별이 "무엇을 관리할 것인가"라면, 형상 통제는 "변경을 어떻게 관리할 것인가"를 담당합니다.

**IEEE Std 828-2012 정의**:
> "Configuration control is the process for controlling changes to configuration items, including the evaluation, coordination, approval or disapproval, and implementation of changes."

**형상 통제의 핵심 목표**:
```
┌─────────────────────────────────────────────────────────────────┐
│                    형상 통제 4대 목표                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 무결성 보장 (Integrity)                                    │
│     - 승인되지 않은 변경 방지                                   │
│     - 변경의 추적 가능성 확보                                   │
│     - 버전 일관성 유지                                          │
│                                                                 │
│  2. 가시성 확보 (Visibility)                                   │
│     - 변경 사항의 투명한 공개                                   │
│     - 이해관계자 통지                                           │
│     - 변경 이력 관리                                            │
│                                                                 │
│  3. 추적성 확보 (Traceability)                                 │
│     - 요구사항 ↔ 변경 ↔ 구현 연결                               │
│     - 영향도 분석 지원                                          │
│     - 감사 증거 제공                                            │
│                                                                 │
│  4. 책임성 확보 (Accountability)                                │
│     - 변경 승인자 명확화                                        │
│     - 변경 구현자 식별                                          │
│     - 의사결정 근거 기록                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 💡 일상생활 비유: 건축 변경 승인 시스템

```
[형상 통제 = 건축 변경 승인 절차]

아파트 단지를 짓는다고 상상해 보세요:

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  📋 문제 상황 (형상 통제 없이)                               │
│                                                             │
│  시공사: "내일부터 벽을 하나 없애야겠어"                      │
│  전기팀: "어? 우리 이미 배선했는데!"                          │
│  설비팀: "파이프가 지나가야 하는데..."                        │
│  고객: "이게 원래 계약한 거 맞아요?"                          │
│                                                             │
│  혼란 → 재작업 → 비용 증가 → 분쟁                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ✅ 해결책 (형상 통제 적용)                                  │
│                                                             │
│  1. 변경 요청서 작성: 왜 벽을 없애야 하는가?                  │
│  2. 영향도 분석: 전기, 설비, 구조에 미치는 영향               │
│  3. CCB 심의: 건축주, 시공사, 설계사가 모여 승인              │
│  4. 승인/반려: 승인 시 변경 진행, 반려 시 사유 통지           │
│  5. 구현 및 검증: 변경 후 검사                               │
│                                                             │
│  체계 → 협업 → 품질 → 성공                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 등장 배경 및 발전 과정

#### 1) 형상 통제의 필요성

```
┌─────────────────────────────────────────────────────────────────┐
│                    형상 통제 필요성                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 변경의 불가피성                                             │
│     - 요구사항 변경은 필연적                                    │
│     - 비즈니스 환경 변화                                        │
│     - 기술적 개선 필요                                          │
│                                                                 │
│  2. 무통제 변경의 위험                                          │
│     - 기능 회귀 (Regression)                                    │
│     - 일관성 상실                                               │
│     - 추적 불가능                                               │
│     - 품질 저하                                                 │
│                                                                 │
│  3. 이해관계자 보호                                              │
│     - 고객: 계약 범위 보호                                      │
│     - 개발사: 범위 크리프 방지                                  │
│     - 감사: 규정 준수 증명                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [최소 1,000자 이상]

### 1. CCB(변경 통제 위원회) 구조

| 역할 | 책임 | 권한 | 참여 시점 |
| :--- | :--- | :--- | :--- |
| **CCB 의장** | 회의 주관, 최종 승인 | 의결권 | 모든 CCB |
| **프로젝트 관리자** | 일정/비용 영향 분석 | 의결권 | 모든 CCB |
| **기술 리더** | 기술적 영향 분석 | 의결권 | 기술적 변경 |
| **QA 담당자** | 품질 영향 분석 | 의결권 | 품질 관련 |
| **고객 대표** | 비즈니스 우선순위 | 의결권 | 주요 변경 |
| **형상 관리자** | 진행 관리, 기록 | 발언권 | 모든 CCB |

### 2. 정교한 구조 다이어그램: 형상 통제 프로세스

```text
================================================================================
|              CONFIGURATION CONTROL PROCESS FLOW                             |
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                      STEP 1: 변경 요청 접수                                 │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   변경 요청자 ──> 변경 요청서(CR) 작성 ──> 형상 관리자 접수          │   │
│   │                                                                     │   │
│   │   변경 요청서(CR) 구성요소:                                         │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │ CR-ID: CR-2026-001                                          │  │   │
│   │   │ 요청자: 홍길동                                               │  │   │
│   │   │ 요청일: 2026-03-05                                           │  │   │
│   │   │ 변경 대상: PROJ-AUTH-SRC-001 (인증 모듈)                     │  │   │
│   │   │ 변경 유형: 기능 추가 / 수정 / 삭제 / 결함 수정               │  │   │
│   │   │ 우선순위: 긴급 / 높음 / 보통 / 낮음                          │  │   │
│   │   │ 변경 내용: OAuth2.0 로그인 기능 추가                         │  │   │
│   │   │ 변경 사유: 고객 요청 - 소셜 로그인 필요                      │  │   │
│   │   │ 영향 범위: 인증 모듈, 사용자 DB, 프론트엔드                   │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                      STEP 2: 변경 분석                                      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐  │   │
│   │   │  기술적 분석    │   │  일정 분석      │   │  비용 분석      │  │   │
│   │   │  - 영향 CI 식별 │   │  - 소요 기간    │   │  - 인력 비용    │  │   │
│   │   │  - 복잡도 평가  │   │  - 마일스톤 영향│   │  - 자원 비용    │  │   │
│   │   │  - 리스크 평가  │   │  - 의존성 분석  │   │  - 기회비용     │  │   │
│   │   └─────────────────┘   └─────────────────┘   └─────────────────┘  │   │
│   │                                                                     │   │
│   │   영향도 분석 매트릭스:                                             │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │ CI ID           │ 영향 유형 │ 영향도 │ 조치 필요           │  │   │
│   │   │ PROJ-AUTH-SRC   │ 수정     │ 높음   │ OAuth 로직 추가     │  │   │
│   │   │ PROJ-USER-DB    │ 수정     │ 중간   │ 소셜 ID 컬럼 추가   │  │   │
│   │   │ PROJ-FRONT-SRC  │ 수정     │ 높음   │ 소셜 로그인 버튼    │  │   │
│   │   │ PROJ-AUTH-TEST  │ 추가     │ 높음   │ OAuth 테스트 케이스 │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                      STEP 3: CCB 심의                                       │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │              변경 통제 위원회 (CCB)                                 │   │
│   │                                                                     │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │                    CCB 회의 진행                            │  │   │
│   │   │                                                             │  │   │
│   │   │  1. 변경 요청서 검토                                        │  │   │
│   │   │  2. 분석 결과 발표                                          │  │   │
│   │   │  3. 이해관계자 의견 수렴                                    │  │   │
│   │   │  4. 토의 및 질의응답                                        │  │   │
│   │   │  5. 투표 (승인 / 조건부 승인 / 반려 / 보류)                 │  │   │
│   │   │                                                             │  │   │
│   │   │  의결 기준:                                                 │  │   │
│   │   │  - 비즈니스 가치 > 비용                                     │  │   │
│   │   │  - 기술적 실현 가능성                                       │  │   │
│   │   │  - 일정 내 완료 가능성                                      │  │   │
│   │   │  - 품질 영향 수용 가능성                                    │  │   │
│   │   │                                                             │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   │   CCB 의결 결과:                                                   │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │ □ 승인 (Approved)     : 변경 즉시 진행                      │  │   │
│   │   │ □ 조건부 승인 (Conditional): 조건 충족 시 진행              │  │   │
│   │   │ □ 반려 (Rejected)     : 변경 불가, 사유 기록                │  │   │
│   │   │ □ 보류 (Deferred)     : 차기 CCB에서 재심의                 │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                      STEP 4: 변경 구현                                      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   승인된 CR 구현 절차:                                              │   │
│   │                                                                     │   │
│   │   1. 작업 할당 ──> 2. 변경 구현 ──> 3. 단위 테스트                 │   │
│   │                                                                     │   │
│   │   구현 체크리스트:                                                  │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │ □ 영향 받는 모든 CI 식별 및 수정 완료                       │  │   │
│   │   │ □ 새로운 버전 번호 할당                                     │  │   │
│   │   │ □ 변경 사항 문서화                                          │  │   │
│   │   │ □ 단위 테스트 통과                                          │  │   │
│   │   │ □ 코드 리뷰 완료                                            │  │   │
│   │   │ ■ 통합 테스트 준비                                          │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        v
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                      STEP 5: 변경 검증                                      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                                                                     │   │
│   │   검증 활동:                                                        │   │
│   │   ┌─────────────────────────────────────────────────────────────┐  │   │
│   │   │ 1. 기능 검증: 변경 요청 내용이 정확히 구현되었는가?          │  │   │
│   │   │ 2. 회귀 테스트: 기존 기능에 영향이 없는가?                   │  │   │
│   │   │ 3. 성능 검증: 성능 저하가 발생하지 않았는가?                 │  │   │
│   │   │ 4. 보안 검증: 새로운 취약점이 없는가?                        │  │   │
│   │   │ 5. 문서 검증: 관련 문서가 업데이트되었는가?                  │  │   │
│   │   └─────────────────────────────────────────────────────────────┘  │   │
│   │                                                                     │   │
│   │   검증 완료 후:                                                      │   │
│   │   - 새로운 기준선 설정                                              │   │
│   │   - 형상 상태 기록 업데이트                                          │   │
│   │   - 이해관계자 통지                                                  │   │
│   │   - CR 종료                                                         │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
```

### 3. 핵심 코드 예시: 변경 요청 워크플로우

```python
"""
변경 요청 관리 시스템
형상 통제 프로세스 자동화
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class ChangeType(Enum):
    FEATURE = "기능 추가"
    MODIFICATION = "기능 수정"
    DELETION = "기능 삭제"
    DEFECT = "결함 수정"
    ENHANCEMENT = "개선"

class Priority(Enum):
    CRITICAL = "긴급"
    HIGH = "높음"
    MEDIUM = "보통"
    LOW = "낮음"

class CRStatus(Enum):
    SUBMITTED = "접수됨"
    ANALYZING = "분석중"
    CCB_REVIEW = "CCB 심의중"
    APPROVED = "승인됨"
    CONDITIONAL = "조건부 승인"
    REJECTED = "반려됨"
    DEFERRED = "보류됨"
    IMPLEMENTING = "구현중"
    VERIFYING = "검증중"
    CLOSED = "종료됨"

@dataclass
class ConfigItem:
    """형상 항목"""
    ci_id: str
    name: str
    version: str
    baseline: str
    owner: str

@dataclass
class ImpactAnalysis:
    """영향도 분석 결과"""
    ci: ConfigItem
    impact_type: str  # 수정, 추가, 삭제
    impact_level: str  # 높음, 중간, 낮음
    effort_hours: float
    description: str

@dataclass
class ChangeRequest:
    """변경 요청서"""
    cr_id: str
    requester: str
    request_date: datetime
    change_type: ChangeType
    priority: Priority
    status: CRStatus
    title: str
    description: str
    justification: str
    impacted_cis: List[ImpactAnalysis] = field(default_factory=list)
    estimated_effort: float = 0.0
    estimated_cost: float = 0.0
    schedule_impact: int = 0  # 일수
    ccb_decision: Optional[str] = None
    ccb_decision_date: Optional[datetime] = None
    ccb_comments: Optional[str] = None
    approval_conditions: List[str] = field(default_factory=list)

class ConfigurationManager:
    """형상 관리자"""

    def __init__(self):
        self.change_requests: List[ChangeRequest] = []
        self.cr_counter = 0

    def submit_change_request(self, requester: str, change_type: ChangeType,
                              priority: Priority, title: str,
                              description: str, justification: str) -> ChangeRequest:
        """변경 요청 접수"""
        self.cr_counter += 1
        cr_id = f"CR-{datetime.now().year}-{self.cr_counter:04d}"

        cr = ChangeRequest(
            cr_id=cr_id,
            requester=requester,
            request_date=datetime.now(),
            change_type=change_type,
            priority=priority,
            status=CRStatus.SUBMITTED,
            title=title,
            description=description,
            justification=justification
        )

        self.change_requests.append(cr)
        print(f"변경 요청 접수: {cr_id}")
        return cr

    def add_impact_analysis(self, cr: ChangeRequest, impact: ImpactAnalysis):
        """영향도 분석 추가"""
        cr.impacted_cis.append(impact)
        cr.estimated_effort += impact.effort_hours
        cr.status = CRStatus.ANALYZING

    def analyze_change_request(self, cr: ChangeRequest) -> dict:
        """변경 요청 분석"""
        analysis = {
            "cr_id": cr.cr_id,
            "total_impacted_cis": len(cr.impacted_cis),
            "total_effort_hours": cr.estimated_effort,
            "estimated_cost": cr.estimated_cost,
            "schedule_impact_days": cr.schedule_impact,
            "risk_level": self._calculate_risk_level(cr),
            "recommendation": self._generate_recommendation(cr)
        }
        return analysis

    def _calculate_risk_level(self, cr: ChangeRequest) -> str:
        """리스크 수준 계산"""
        score = 0

        # 우선순위 가중치
        if cr.priority == Priority.CRITICAL:
            score += 30
        elif cr.priority == Priority.HIGH:
            score += 20
        else:
            score += 10

        # 영향도 가중치
        for impact in cr.impacted_cis:
            if impact.impact_level == "높음":
                score += 15
            elif impact.impact_level == "중간":
                score += 10
            else:
                score += 5

        # 영향 CI 수 가중치
        score += len(cr.impacted_cis) * 5

        # 일정 영향 가중치
        score += cr.schedule_impact

        if score >= 80:
            return "높음"
        elif score >= 50:
            return "중간"
        else:
            return "낮음"

    def _generate_recommendation(self, cr: ChangeRequest) -> str:
        """승인 권고안 생성"""
        risk = self._calculate_risk_level(cr)

        if cr.priority == Priority.CRITICAL and risk == "높음":
            return "긴급 변경으로 즉시 승인 권장"
        elif cr.priority == Priority.LOW and risk == "높음":
            return "리스크 대비 우선순위 낮음 - 반려 또는 보류 권장"
        elif risk == "낮음":
            return "낮은 리스크 - 승인 권장"
        else:
            return "CCB 심의 필요"

    def ccb_review(self, cr: ChangeRequest, decision: str,
                   comments: str, conditions: List[str] = None):
        """CCB 심의 결과 기록"""
        cr.ccb_decision = decision
        cr.ccb_decision_date = datetime.now()
        cr.ccb_comments = comments

        if conditions:
            cr.approval_conditions = conditions

        if decision == "승인":
            cr.status = CRStatus.APPROVED
        elif decision == "조건부 승인":
            cr.status = CRStatus.CONDITIONAL
        elif decision == "반려":
            cr.status = CRStatus.REJECTED
        else:
            cr.status = CRStatus.DEFERRED

        print(f"CCB 결정: {cr.cr_id} - {decision}")

    def implement_change(self, cr: ChangeRequest):
        """변경 구현 시작"""
        if cr.status in [CRStatus.APPROVED, CRStatus.CONDITIONAL]:
            cr.status = CRStatus.IMPLEMENTING
            print(f"변경 구현 시작: {cr.cr_id}")
        else:
            print(f"오류: 승인되지 않은 변경 요청: {cr.cr_id}")

    def verify_and_close(self, cr: ChangeRequest, verification_result: bool):
        """변경 검증 및 종료"""
        if verification_result:
            cr.status = CRStatus.CLOSED
            print(f"변경 요청 종료: {cr.cr_id}")
        else:
            cr.status = CRStatus.IMPLEMENTING
            print(f"검증 실패 - 재작업 필요: {cr.cr_id}")


# 사용 예시
if __name__ == "__main__":
    cm = ConfigurationManager()

    # 1. 변경 요청 접수
    cr = cm.submit_change_request(
        requester="홍길동",
        change_type=ChangeType.FEATURE,
        priority=Priority.HIGH,
        title="OAuth 2.0 소셜 로그인 기능 추가",
        description="Google, Facebook 로그인 기능 추가",
        justification="고객 요청 - 사용자 편의성 향상"
    )

    # 2. 영향도 분석 추가
    auth_ci = ConfigItem("PROJ-AUTH-SRC-001", "인증 모듈", "1.2.0", "BL-DEV-003", "김개발")
    cm.add_impact_analysis(cr, ImpactAnalysis(auth_ci, "수정", "높음", 16.0, "OAuth 로직 추가"))

    user_ci = ConfigItem("PROJ-USER-DB-001", "사용자 DB", "1.1.0", "BL-DEV-003", "이DBA")
    cm.add_impact_analysis(cr, ImpactAnalysis(user_ci, "수정", "중간", 8.0, "소셜 ID 컬럼 추가"))

    # 3. 분석 수행
    analysis = cm.analyze_change_request(cr)
    print("\n=== 변경 분석 결과 ===")
    for key, value in analysis.items():
        print(f"{key}: {value}")

    # 4. CCB 심의
    cm.ccb_review(cr, "승인", "비즈니스 가치가 높음", ["보안 검토 필수"])

    # 5. 구현 및 종료
    cm.implement_change(cr)
    cm.verify_and_close(cr, True)

    print(f"\n최종 상태: {cr.status.value}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy) - [비교표 2개 이상]

### 1. CCB 유형 비교

| CCB 유형 | 구성 | 권한 | 빈도 | 적용 |
| :--- | :--- | :--- | :--- | :--- |
| **프로젝트 CCB** | PM, 기술리더, QA | 프로젝트 범위 변경 | 주간 | 일반 프로젝트 |
| **기술 CCB** | 아키텍트, 기술리더 | 기술적 변경 | 수시 | 기술 의사결정 |
| **긴급 CCB** | PM, 기술리더 | 긴급 변경 | 즉시 | 핫픽스 |
| **경영 CCB** | 경영진, PM, 고객 | 범위/계약 변경 | 월간 | 대형 변경 |

### 2. 형상 통제 vs Git 워크플로우

| 전통적 형상 통제 | Git 워크플로우 | 대응 관계 |
| :--- | :--- | :--- |
| CR 작성 | Issue/Ticket 생성 | 변경 요청 |
| 영향도 분석 | PR Preview | 분석 |
| CCB 심의 | PR 리뷰 | 승인 |
| 승인 문서 | Merge 승인 | 승인 |
| 변경 구현 | Commit/Push | 구현 |
| 검증 | CI/CD 테스트 | 검증 |
| 기준선 갱신 | Tag/Release | 버전화 |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단

**[시나리오] 긴급 vs 정규 변경 통제**

```
상황:
- 프로덕션 결함 발견, 즉시 수정 필요
- 정규 CCB는 매주 화요일

기술사적 판단:
1. 긴급 CCB 소집 조건 검토
   - 비즈니스 영향: 고객 서비스 중단
   - 보안 영향: 없음
   - 대안: 없음

2. 긴급 변경 프로세스
   - 즉시 긴급 CCB 소집 (PM + 기술리더)
   - 최소 분석 후 승인
   - 구현 후 정규 CCB에서 사후 승인

3. 품질 게이트
   - 단위 테스트 필수
   - 스테이징 검증 필수
   - 롤백 계획 필수
```

### 2. 주의사항

| 주의사항 | 설명 | 해결 방안 |
| :--- | :--- | :--- |
| **CCB 병목** | 승인 대기 시간 길어짐 | 위임 권한, 자동화 |
| **형식적 심의** | 확인 없이 승인 | 체크리스트 강제 |
| **우회 변경** | CCB 없이 직접 변경 | 감사, 페널티 |

---

## Ⅴ. 기대효과 및 결론

### 1. 정량적 기대효과

| 구분 | 지표 | 미적용 | 적용 | 개선 |
| :--- | :--- | :--- | :--- | :--- |
| **무결성** | 미승인 변경률 | 30% | 0% | -100% |
| **범위 관리** | 범위 크리프 | 40% | 10% | -75% |
| **추적성** | 변경 추적률 | 50% | 100% | +100% |

### ※ 참고 표준

- **IEEE 828-2012**: Configuration Management
- **ISO 10007**: Quality Management - Configuration Management
- **CMMI**: Configuration Management Process Area

---

## 📌 관련 개념 맵

- [형상 관리](./19_configuration_management.md) : SCM 전체 체계
- [형상 식별](./20_configuration_identification.md) : CI 선정 및 관리
- [기준선](./25_baseline.md) : 변경 통제 시작점
- [형상 감사](./22_configuration_audit.md) : 무결성 검증
- [변경 관리](./27_change_management.md) : 일반적 변경 프로세스

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 레고 성을 만드는데 친구가 맘대로 탑을 바꿨어요! "왜 바꿨어?" 물어보니까 "그냥요"라고만 해요. 이제 성이 이상해졌는데 누가 뭘 바꿨는지 모르겠어요!

2. **해결(형상 통제)**: 그래서 '변경 승인 규칙'을 만들었어요! 무얼 바꾸고 싶으면 먼저 "변경 요청서"를 써야 해요. 그리고 우리 팀 친구들이 모여서 "이 변경 괜찮아?"라고 투표를 해요!

3. **효과**: 이제 아무나 맘대로 레고를 바꿀 수 없어요! 모든 변경이 기록되고, 왜 바꿨는지도 알 수 있어요. 우리 성이 더 튼튼해졌죠!
