+++
title = "요구공학 (Requirements Engineering)"
date = 2024-05-24
description = "소프트웨어 요구사항을 체계적으로 도출, 분석, 명세, 검증 및 관리하는 공학적 활동, 성공적인 소프트웨어 개발을 위한 가장 중요한 단계"
weight = 30
categories = ["studynotes-se"]
+++

# 요구공학 (Requirements Engineering)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구공학은 소프트웨어가 **무엇을(What) 해야 하는지**를 정의하는 공학적 활동으로, 이해관계자의 요구를 **체계적으로 도출, 분석, 명세, 검증, 관리**하여 개발 착오를 예방하고 프로젝트 성공 확률을 높이는 핵심 프로세스입니다.
> 2. **가치**: 체계적 요구공학 적용 시 **재작업 비용 50~70% 감소**, 프로젝트 성공률 30% 향상 효과가 있으며, 요구사항 결함의 **60~80%가 요구공학 단계에서 발생**하므로 이 단계의 품질이 프로젝트 전체의 성패를 좌우합니다.
> 3. **융합**: 시스템 공학, 비즈니스 분석과 밀접하게 연관되며, **UML, 유스케이스, 사용자 스토리** 등의 기법과 **도메인 주도 설계(DDD)**의 입력이 되며, 애자일에서는 백로그 관리로 진화했습니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**요구공학(Requirements Engineering, RE)**은 소프트웨어 시스템이 달성해야 할 목표와 제약사항을 체계적으로 식별, 분석, 명세, 검증하고, 이를 지속적으로 관리하는 공학적 활동입니다.

**공식적 정의 (IEEE 830)**:
> "요구사항이란 시스템이 가져야 할 능력이나 특성에 대한 조건이나 능력으로, 문제를 해결하거나 목표를 달성하기 위해 사용자에 의해 필요로 되거나, 계약, 표준, 명세, 또는 다른 공식 문서에 의해 요구되는 것이다."

**요구공학의 5대 핵심 활동**:

| 활동 | 영문 | 설명 | 주요 산출물 |
|:---|:---|:---|:---|
| **도출** | Elicitation | 이해관계자로부터 요구사항 수집 | 인터뷰 기록, 워크숍 결과 |
| **분석** | Analysis | 수집된 요구사항의 모순 해결, 우선순위 결정 | 분석 모델, 우선순위 매트릭스 |
| **명세** | Specification | 요구사항의 공식적 문서화 | SRS, 유스케이스, 사용자 스토리 |
| **검증** | Validation | 요구사항의 정확성, 완전성 검토 | 검토 보고서, 인수 테스트 계획 |
| **관리** | Management | 요구사항 변경 통제, 추적성 관리 | RTM, 변경 요청서 |

### 2. 요구사항의 유형

```
[요구사항 분류 체계]

                    요구사항
                        |
        +---------------+---------------+
        |                               |
   기능적 요구사항                  비기능적 요구사항
   (Functional)                    (Non-Functional)
        |                               |
        +-- 시스템이 무엇을 해야 하는가    +-- 시스템이 어떻게 동작해야 하는가
        |                               |
        |-- 입력                        |-- 성능 (Performance)
        |-- 출력                        |-- 보안 (Security)
        |-- 저장                        |-- 가용성 (Availability)
        |-- 계산                        |-- 사용성 (Usability)
        |-- 제어                        |-- 신뢰성 (Reliability)
        |-- 통신                        |-- 유지보수성 (Maintainability)
                                        |-- 이식성 (Portability)

[비기능 요구사항의 FURPS+ 분류]

F - Functionality (기능성): 보안, 로깅 등
U - Usability (사용성): UI/UX, 접근성
R - Reliability (신뢰성): 가용성, 장애 복구
P - Performance (성능): 응답 시간, 처리량
S - Supportability (지원성): 유지보수, 확장성
+ - + Constraints (제약사항): 기술, 비용, 일정
+ - + Interfaces (인터페이스): 외부 시스템 연동
+ - + Operations (운영): 배포, 모니터링
+ - + Packaging (패키징): 설치, 라이선스
+ - + Legal (법적): 규제, 표준 준수
```

### 3. 비유: 집 설계

```
[집 설계로 보는 요구공학]

기능적 요구사항:
- "방이 3개 필요해요"
- "욕실이 2개 필요해요"
- "주차장이 있어야 해요"
- "부엌이 넓어야 해요"

비기능적 요구사항:
- "내진 설계가 필요해요" (신뢰성)
- "에너지 효율이 좋아야 해요" (성능)
- "노인도 사용하기 쉬워야 해요" (사용성)
- "보안 시스템이 필요해요" (보안)
- "5억 원 이내여야 해요" (비용 제약)

요구공학의 역할:
- 고객이 "좋은 집"이라고만 말할 때
- 구체적으로 무엇이 필요한지 질문하고 정리
- "좋은 집"의 의미를 명확히 문서화
- 이를 건축가에게 전달하여 설계
```

### 4. 등장 배경 및 발전 과정

#### 1) 요구사항 실패의 영향

**스탠디시 그룹(Standish Group)의 Chaos Report**:

| 실패 원인 | 비율 | 설명 |
|:---|:---:|:---|
| 불완전한 요구사항 | 13% | 요구사항이 충분히 수집되지 않음 |
| 사용자 참여 부족 | 12% | 이해관계자 참여 미흡 |
| 자원 부족 | 11% | 예산, 인력 부족 |
| 비현실적 기대 | 10% | 요구사항이 과도함 |
| 지원 부족 | 9% | 경영진 지원 미흡 |

**요구사항 결함의 파급 효과**:

```
[결함 발견 시점별 수정 비용]

요구공학 단계:     1x (기준)
설계 단계:         3~5x
구현 단계:         10x
테스트 단계:       20~50x
운영 단계:         100~1000x

예시:
요구공학에서 발견: 1시간 수정 = 1시간
운영에서 발견:     1시간 수정 = 100시간+ (장애, 고객 불만, 핫픽스 등)
```

#### 2) 역사적 발전

| 시기 | 발전 내용 | 표준/기여자 |
|:---|:---|:---|
| 1970년대 | 구조적 분석 (DFD) | DeMarco, Yourdon |
| 1980년대 | SRS 표준 | IEEE 830 (1984) |
| 1990년대 | 객체지향 분석 (UML) | Rumbaugh, Booch, Jacobson |
| 1990년대 | 요구공학 개념 정립 | IEEE, SEI |
| 2000년대 | 애자일 요구사항 | 사용자 스토리, 백로그 |
| 2010년대 | BDD, DDD 연계 | North, Evans |
| 현재 | AI 기반 요구사항 분석 | LLM, NLP |

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석

| 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 비유 |
|:---|:---|:---|:---|:---|
| **이해관계자** | 요구사항의 원천 | 사용자, 고객, 개발자, 관리자 | 이해관계자 맵 | 주문자 |
| **요구사항** | 시스템이 달성해야 할 목표 | 기능적, 비기능적, 제약사항 | SRS, 백로그 | 주문서 |
| **도출 기법** | 요구사항 수집 방법 | 인터뷰, 워크숍, 프로토타이핑 | Jira, Miro | 인터뷰 |
| **분석 모델** | 요구사항의 구조화 | 유스케이스, DFD, UML | UML 도구 | 설계도 |
| **명세서** | 요구사항의 공식 문서 | SRS, 사용자 스토리 | Word, Confluence | 계약서 |
| **추적 매트릭스** | 요구사항 추적성 | RTM (Requirements Traceability Matrix) | Excel, DOORS | 색인 |

### 2. 정교한 구조 다이어그램

```text
================================================================================
|                REQUIREMENTS ENGINEERING PROCESS MODEL                         |
================================================================================

                    +--------------------------+
                    |    Stakeholders          |
                    |  (이해관계자)             |
                    +------------+-------------+
                                 |
                                 v
+--------------------------------------------------------------------------+
|                    REQUIREMENTS ENGINEERING LIFECYCLE                     |
+--------------------------------------------------------------------------+
|                                                                          |
|  +-------------+      +-------------+      +-------------+               |
|  |  ELICITATION |----->|  ANALYSIS   |----->|SPECIFICATION|               |
|  |   (도출)     |      |   (분석)     |      |   (명세)     |               |
|  +------+------+      +------+------+      +------+------+               |
|         |                   |                    |                        |
|         v                   v                    v                        |
|  +-------------+      +-------------+      +-------------+               |
|  |- Interviews |      |- Conflict   |      |- SRS        |               |
|  |- Workshops  |      |  Resolution |      |- Use Cases  |               |
|  |- Prototypes |      |- Prioritize |      |- Stories    |               |
|  |- Observation|      |- Modeling    |      |- Diagrams   |               |
|  |- Documents  |      |- Validation  |      |- Mockups    |               |
|  +-------------+      +-------------+      +-------------+               |
|                                                                          |
|         |                   ^                    ^                        |
|         |                   |                    |                        |
|         v                   |                    |                        |
|  +-------------+      +------+------+             |                        |
|  | VALIDATION  |<-----| MANAGEMENT |<------------+                        |
|  |  (검증)     |      |   (관리)    |                                      |
|  +------+------+      +-------------+                                      |
|         |                   ^                                             |
|         v                   |                                             |
|  +-------------+            |                                             |
|  |- Reviews    |            |                                             |
|  |- Prototypes |            |                                             |
|  |- Test Cases |            |                                             |
|  |- Acceptance |            |                                             |
|  +-------------+            |                                             |
|                             |                                             |
+-----------------------------|---------------------------------------------+
                              |
                              v
                    +--------------------------+
                    |    DEVELOPMENT TEAM      |
                    |    (개발 팀)              |
                    +--------------------------+


REQUIREMENTS TRACEABILITY
=========================

    Business    System    Software    Test    Code
      Needs    Requirements  Specs    Cases   Modules
        |          |           |        |       |
        v          v           v        v       v
    +-------+  +-------+   +-------+ +-------+ +---+
    | BN-01 |->| SR-01 |-->| SS-01 | | TC-01 | | C1|
    +-------+  +-------+   +-------+ +-------+ +---+
        |          |           |        |       |
        v          v           v        v       v
    +-------+  +-------+   +-------+ +-------+ +---+
    | BN-02 |->| SR-02 |-->| SS-02 | | TC-02 | | C2|
    +-------+  +-------+   +-------+ +-------+ +---+

    Forward Traceability:  Business -> Code
    Backward Traceability:  Code -> Business
    Bidirectional Traceability: Both directions

================================================================================
```

### 3. 심층 동작 원리: 요구사항 도출 기법

```
[요구사항 도출 기법 비교]

1. 인터뷰 (Interviews)
   +------------------------------------------+
   | 개별/그룹 인터뷰, 구조화/비구조화          |
   | 장점: 깊이 있는 정보, 명확화 질문 가능      |
   | 단점: 시간 소요, 인터뷰어 역량 의존         |
   +------------------------------------------+

2. 워크숍 (Workshops/JAD)
   +------------------------------------------+
   | 이해관계자 모두 참여, 합의 도출            |
   | 장점: 빠른 합의, 이해관계자 참여           |
   | 단점: 일정 조율 어려움, 중재자 필요        |
   +------------------------------------------+

3. 관찰 (Observation/Shadowing)
   +------------------------------------------+
   | 실제 업무 현장 관찰                        |
   | 장점: 숨겨진 요구사항 발견                 |
   | 단점: 시간 소요, 사용자 거부감 가능        |
   +------------------------------------------+

4. 프로토타이핑 (Prototyping)
   +------------------------------------------+
   | 실행 가능한 모형으로 요구사항 명확화        |
   | 장점: 사용자 피드백 즉시 확보              |
   | 단점: 오버엔지니어링 위험, 시간 소요        |
   +------------------------------------------+

5. 설문조사 (Questionnaires)
   +------------------------------------------+
   | 구조화된 질문지로 대규모 데이터 수집        |
   | 장점: 대규모 대상, 정량적 분석              |
   | 단점: 깊이 부족, 응답률 문제               |
   +------------------------------------------+

6. 문서 분석 (Document Analysis)
   +------------------------------------------+
   | 기존 문서, 매뉴얼, 규정 분석               |
   | 장점: 객관적 정보, 빠른 수집               |
   | 단점: 최신성 문제, 맥락 부족               |
   +------------------------------------------+

7. 브레인스토밍 (Brainstorming)
   +------------------------------------------+
   | 자유로운 아이디어 생성                      |
   | 장점: 창의적 요구사항 발견                  |
   | 단점: 정리 필요, 발산 위험                 |
   +------------------------------------------+
```

### 4. 요구사항 명세서(SRS) 품질 특성 (IEEE 830)

| 품질 특성 | 설명 | 체크리스트 예시 |
|:---|:---|:---|
| **정확성** | 요구사항이 올바르게 기술됨 | "사용자가 의도한 대로 기술되었는가?" |
| **명확성** | 모호하지 않고 해석 가능 | "~등", "~정도" 등 모호어 배제 |
| **완전성** | 모든 요구사항이 포함됨 | "예외 상황도 기술되었는가?" |
| **일관성** | 요구사항 간 모순 없음 | "상충되는 요구사항이 없는가?" |
| **중요도** | 우선순위가 부여됨 | "Must/Should/Could 구분?" |
| **검증 가능성** | 테스트로 확인 가능 | "측정 가능한 기준인가?" |
| **수정 용이성** | 변경이 용이함 | "구조화되어 있는가?" |
| **추적 가능성** | 출처와 영향 파악 가능 | "요구사항 ID가 있는가?" |

### 5. 실무 코드 예시: 요구사항 관리 시스템

```python
"""
요구사항 관리 시스템
Requirements Management System
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
from datetime import datetime

class RequirementType(Enum):
    FUNCTIONAL = "기능적"
    PERFORMANCE = "성능"
    SECURITY = "보안"
    USABILITY = "사용성"
    RELIABILITY = "신뢰성"
    INTERFACE = "인터페이스"
    CONSTRAINT = "제약사항"

class RequirementPriority(Enum):
    MUST = "Must"        # 필수
    SHOULD = "Should"    # 권장
    COULD = "Could"      # 선택
    WONT = "Won't"       # 이번 제외

class RequirementStatus(Enum):
    PROPOSED = "제안됨"
    APPROVED = "승인됨"
    IMPLEMENTED = "구현됨"
    VERIFIED = "검증됨"
    REJECTED = "거부됨"
    DEFERRED = "연기됨"

@dataclass
class Stakeholder:
    """이해관계자"""
    name: str
    role: str
    email: str
    influence: int        # 1~5 (영향도)
    interest: int         # 1~5 (관심도)

@dataclass
class Requirement:
    """요구사항"""
    req_id: str
    title: str
    description: str
    req_type: RequirementType
    priority: RequirementPriority
    status: RequirementStatus = RequirementStatus.PROPOSED
    source: Optional[str] = None           # 출처 (이해관계자)
    rationale: Optional[str] = None        # 근거
    acceptance_criteria: List[str] = field(default_factory=list)
    parent_ids: List[str] = field(default_factory=list)      # 상위 요구사항
    child_ids: List[str] = field(default_factory=list)       # 하위 요구사항
    related_ids: List[str] = field(default_factory=list)     # 관련 요구사항
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: int = 1

    def add_child(self, child_id: str) -> None:
        """하위 요구사항 추가"""
        if child_id not in self.child_ids:
            self.child_ids.append(child_id)
            self.updated_at = datetime.now()

    def set_parent(self, parent_id: str) -> None:
        """상위 요구사항 설정"""
        if parent_id not in self.parent_ids:
            self.parent_ids.append(parent_id)
            self.updated_at = datetime.now()


class RequirementsManager:
    """
    요구사항 관리자
    요구사항 도출, 분석, 명세, 검증, 관리 기능 제공
    """

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.requirements: Dict[str, Requirement] = {}
        self.stakeholders: Dict[str, Stakeholder] = {}
        self.traceability_matrix: Dict[str, Set[str]] = {}

    def register_stakeholder(
        self,
        name: str,
        role: str,
        email: str,
        influence: int,
        interest: int
    ) -> Stakeholder:
        """이해관계자 등록"""
        stakeholder = Stakeholder(
            name=name,
            role=role,
            email=email,
            influence=influence,
            interest=interest
        )
        self.stakeholders[name] = stakeholder
        return stakeholder

    def add_requirement(
        self,
        req_id: str,
        title: str,
        description: str,
        req_type: RequirementType,
        priority: RequirementPriority,
        source: str = None,
        rationale: str = None,
        acceptance_criteria: List[str] = None
    ) -> Requirement:
        """요구사항 추가"""
        req = Requirement(
            req_id=req_id,
            title=title,
            description=description,
            req_type=req_type,
            priority=priority,
            source=source,
            rationale=rationale,
            acceptance_criteria=acceptance_criteria or []
        )
        self.requirements[req_id] = req
        self.traceability_matrix[req_id] = set()
        return req

    def link_requirements(
        self,
        parent_id: str,
        child_id: str
    ) -> None:
        """요구사항 간 추적성 연결"""
        if parent_id not in self.requirements:
            raise ValueError(f"요구사항 {parent_id}가 존재하지 않습니다")
        if child_id not in self.requirements:
            raise ValueError(f"요구사항 {child_id}가 존재하지 않습니다")

        self.requirements[parent_id].add_child(child_id)
        self.requirements[child_id].set_parent(parent_id)
        self.traceability_matrix[parent_id].add(child_id)

    def analyze_conflicts(self) -> List[Dict]:
        """요구사항 충돌 분석"""
        conflicts = []
        req_list = list(self.requirements.values())

        for i, req1 in enumerate(req_list):
            for req2 in req_list[i+1:]:
                # 간단한 키워드 기반 충돌 감지
                # 실제로는 더 정교한 분석 필요
                conflict = self._check_conflict(req1, req2)
                if conflict:
                    conflicts.append({
                        "req1": req1.req_id,
                        "req2": req2.req_id,
                        "reason": conflict
                    })
        return conflicts

    def _check_conflict(
        self,
        req1: Requirement,
        req2: Requirement
    ) -> Optional[str]:
        """두 요구사항 간 충돌 확인"""
        # 성능 vs 보안 충돌 예시
        if req1.req_type == RequirementType.PERFORMANCE:
            if req2.req_type == RequirementType.SECURITY:
                return "성능과 보안 요구사항 간 상충 가능성"

        return None

    def prioritize_requirements(self) -> List[Requirement]:
        """요구사항 우선순위 정렬"""
        priority_order = {
            RequirementPriority.MUST: 1,
            RequirementPriority.SHOULD: 2,
            RequirementPriority.COULD: 3,
            RequirementPriority.WONT: 4
        }

        return sorted(
            self.requirements.values(),
            key=lambda r: priority_order.get(r.priority, 5)
        )

    def generate_rtm(self) -> Dict:
        """요구사항 추적 매트릭스(RTM) 생성"""
        rtm = {
            "project": self.project_name,
            "generated_at": datetime.now().isoformat(),
            "requirements": [],
            "traceability": {}
        }

        for req_id, req in self.requirements.items():
            rtm["requirements"].append({
                "id": req_id,
                "title": req.title,
                "type": req.req_type.value,
                "priority": req.priority.value,
                "status": req.status.value,
                "children": req.child_ids,
                "parents": req.parent_ids
            })

        rtm["traceability"] = {
            k: list(v) for k, v in self.traceability_matrix.items()
        }

        return rtm

    def get_statistics(self) -> Dict:
        """요구사항 통계"""
        if not self.requirements:
            return {"message": "등록된 요구사항이 없습니다"}

        by_type = {}
        by_priority = {}
        by_status = {}

        for req in self.requirements.values():
            # 유형별
            t = req.req_type.value
            by_type[t] = by_type.get(t, 0) + 1

            # 우선순위별
            p = req.priority.value
            by_priority[p] = by_priority.get(p, 0) + 1

            # 상태별
            s = req.status.value
            by_status[s] = by_status.get(s, 0) + 1

        return {
            "project_name": self.project_name,
            "total_requirements": len(self.requirements),
            "total_stakeholders": len(self.stakeholders),
            "by_type": by_type,
            "by_priority": by_priority,
            "by_status": by_status,
            "traceability_links": sum(
                len(v) for v in self.traceability_matrix.values()
            )
        }

    def validate_requirement(self, req_id: str) -> Dict:
        """요구사항 품질 검증 (IEEE 830 기준)"""
        if req_id not in self.requirements:
            return {"error": f"요구사항 {req_id}가 존재하지 않습니다"}

        req = self.requirements[req_id]
        issues = []

        # 명확성 검사
        ambiguous_words = ["등", "정도", "약간", "매우", "빠르게"]
        for word in ambiguous_words:
            if word in req.description:
                issues.append(f"모호한 표현: '{word}'")

        # 완전성 검사
        if not req.acceptance_criteria:
            issues.append("인수 기준이 정의되지 않음")

        # 검증 가능성 검사
        if not any(c.isdigit() for c in req.description):
            issues.append("정량적 기준 부족 (숫자 없음)")

        # 추적 가능성 검사
        if not req.source:
            issues.append("출처(이해관계자) 미지정")

        return {
            "req_id": req_id,
            "title": req.title,
            "is_valid": len(issues) == 0,
            "issues": issues,
            "quality_score": max(0, 100 - len(issues) * 20)
        }


# ===== 실제 사용 예시 =====
if __name__ == "__main__":
    # 요구사항 관리자 생성
    rm = RequirementsManager("이커머스 플랫폼")

    # 이해관계자 등록
    rm.register_stakeholder("김사용", "고객", "user@example.com", 5, 5)
    rm.register_stakeholder("박기획", "기획자", "pm@example.com", 4, 4)
    rm.register_stakeholder("이개발", "개발자", "dev@example.com", 3, 3)

    # 요구사항 추가
    rm.add_requirement(
        "FR-001",
        "상품 검색",
        "사용자가 키워드로 상품을 검색할 수 있다. 검색 결과는 1초 이내에 표시되어야 한다.",
        RequirementType.FUNCTIONAL,
        RequirementPriority.MUST,
        source="김사용",
        rationale="핵심 사용자 기능",
        acceptance_criteria=[
            "키워드 입력 후 1초 이내 결과 표시",
            "100만 건 상품에서 검색 가능",
            "검색 결과는 관련도순 정렬"
        ]
    )

    rm.add_requirement(
        "NFR-001",
        "검색 응답 시간",
        "모든 검색 요청에 대해 평균 500ms 이내 응답",
        RequirementType.PERFORMANCE,
        RequirementPriority.MUST,
        source="박기획",
        acceptance_criteria=[
            "95% 요청 500ms 이내",
            "최대 2초까지 허용"
        ]
    )

    # 추적성 연결
    rm.link_requirements("FR-001", "NFR-001")

    # 통계
    stats = rm.get_statistics()
    print("=== 요구사항 통계 ===")
    print(f"총 요구사항: {stats['total_requirements']}")
    print(f"유형별: {stats['by_type']}")
    print(f"우선순위별: {stats['by_priority']}")

    # 품질 검증
    validation = rm.validate_requirement("FR-001")
    print(f"\n=== 요구사항 검증 ({validation['req_id']}) ===")
    print(f"유효성: {validation['is_valid']}")
    print(f"품질 점수: {validation['quality_score']}점")
    if validation['issues']:
        print(f"이슈: {validation['issues']}")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 요구사항 명세 기법 비교

| 비교 항목 | 전통적 SRS | 유스케이스 | 사용자 스토리 |
|:---|:---|:---|:---|
| **형식** | 문서 중심 | 다이어그램+텍스트 | 짧은 문장 |
| **상세도** | 매우 상세 | 중간 | 간결 |
| **고객 가독성** | 낮음 | 중간 | 높음 |
| **변경 용이성** | 낮음 | 중간 | 높음 |
| **추적성** | 높음 | 중간 | 낮음~중간 |
| **적합 방법론** | 폭포수 | RUP | 애자일 |
| **검증 방법** | 검토, 인스펙션 | 시나리오 리뷰 | 인수 테스트 |

### 2. 과목 융합 관점 분석

#### 요구공학 + UML 모델링

```
[요구사항 -> UML 매핑]

기능적 요구사항:
- 유스케이스 다이어그램 (Use Case Diagram)
- 액티비티 다이어그램 (Activity Diagram)
- 시퀀스 다이어그램 (Sequence Diagram)

비기능적 요구사항:
- 배치 다이어그램 (Deployment Diagram) - 성능, 가용성
- 컴포넌트 다이어그램 (Component Diagram) - 확장성

데이터 요구사항:
- 클래스 다이어그램 (Class Diagram)
- ER 다이어그램
```

#### 요구공학 + 테스팅

| 요구공학 산출물 | 테스팅 연계 |
|:---|:---|
| 인수 기준 | 인수 테스트 케이스 |
| 유스케이스 | 시나리오 테스트 |
| 성능 요구사항 | 부하 테스트 |
| 보안 요구사항 | 침투 테스트 |

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

#### [시나리오 1] 대형 공공 SI 프로젝트

**상황**:
- 프로젝트: 관공서 전자결재 시스템
- 규모: 100억 원, 30인, 18개월
- 특성: 요구사항 명확, 감사 대상

**기술사적 판단**:

```
선택: 전통적 요구공학 (SRS 기반)

근거:
1. 문서화 요구: 감사 및 인수인계를 위한 완전한 문서
2. 안정적 요구사항: 정부 사업은 요구사항 변동 적음
3. 계약 준거: SRS가 계약의 일부

수행 전략:
- IEEE 830 표준 SRS 작성
- 유스케이스 + DFD 병행
- RTM으로 추적성 확보
- 정기 검토회의(인스펙션) 실시
```

#### [시나리오 2] 스타트업 애자일 프로젝트

**상황**:
- 프로젝트: AI 챗봇 서비스
- 규모: 5인, 3개월 MVP
- 특성: 요구사항 불확실, 빠른 변화

**기술사적 판단**:

```
선택: 애자일 요구공학 (사용자 스토리)

근거:
1. 요구사항 진화: 사용자 피드백으로 계속 변화
2. 속도 중요: 상세 문서보다 빠른 개발
3. 고객 참여: 매 스프린트 피드백

수행 전략:
- 사용자 스토리 + 인수 기준
- 스토리 맵으로 우선순위 관리
- 스프린트마다 백로그 리파인먼트
- BDD 시나리오로 검증
```

### 2. 도입 시 고려사항 (체크리스트)

**조직적 고려사항**:
- [ ] **이해관계자 참여**: 모든 이해관계자가 참여 가능한가?
- [ ] **도구 지원**: 요구사항 관리 도구가 있는가?
- [ ] **역량**: 요구공학 수행 역량이 있는가?
- [ ] **시간**: 충분한 요구공학 수행 시간이 확보되었는가?

**프로세스적 고려사항**:
- [ ] **표준**: 조직 표준 요구공학 프로세스가 있는가?
- [ ] **템플릿**: SRS/유스케이스 템플릿이 준비되었는가?
- [ ] **검증**: 요구사항 검증 프로세스가 있는가?
- [ ] **변경 관리**: 요구사항 변경 통제 프로세스가 있는가?

### 3. 주의사항 및 안티패턴

| 안티패턴 | 증상 | 원인 | 해결 방안 |
|:---|:---|:---|:---|
| **골드 플래팅** | 요구사항에 없는 기능 추가 | 오버엔지니어링 | 범위 엄격 관리 |
| **분석 마비** | 요구사항 분석만 계속 | 완벽주의 | 타임박스 설정 |
| **사용자 배제** | 개발자가 임의로 결정 | 사용자 접근 어려움 | 사용자 챔피언 확보 |
| **문서 방치** | SRS 작성 후 업데이트 안 함 | 관리 부재 | 지속적 업데이트 |
| **모호성 수용** | "~정도", "~등" 허용 | 검증 부재 | 정량적 기준 요구 |

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | 적용 전 | 적용 후 | 개선 효과 |
|:---|:---|:---:|:---:|:---:|
| **재작업 비용** | 전체 비용 대비 | 40% | 15% | -62.5% |
| **프로젝트 성공률** | 성공적 완료율 | 35% | 65% | +30%p |
| **요구사항 결함** | 전체 결함 중 비율 | 50% | 20% | -30%p |
| **일정 준수** | 일정 준수율 | 45% | 70% | +25%p |
| **고객 만족** | 최종 만족도 | 60% | 85% | +25%p |

### 2. 미래 전망 및 진화 방향

1. **AI 기반 요구사항 분석**:
   - NLP로 자연어 요구사항 분석
   - 자동 모순 감지, 완전성 검증

2. **시각화 도구 발전**:
   - 요구사항 시각화 자동화
   - 실시간 협업 도구

3. **지속적 요구공학**:
   - DevOps와 통합된 요구사항 관리
   - 운영 데이터 기반 요구사항 진화

### 3. 참고 표준/가이드

| 표준/가이드 | 내용 | 적용 분야 |
|:---|:---|:---|
| **IEEE 830** | SRS 작성 가이드 | 명세서 작성 |
| **IEEE 29148** | 요구공학 프로세스 | 프로세스 |
| **ISO/IEC 25010** | 품질 요구사항 모델 | 비기능 요구사항 |
| **IIBA BABOK** | 비즈니스 분석 지식체계 | 비즈니스 분석 |
| **PMBOK** | 요구사항 수집 프로세스 | 프로젝트 관리 |

---

## 관련 개념 맵 (Knowledge Graph)

- [소프트웨어 공학](@/studynotes/4_software_engineering/1_sdlc/1_software_engineering.md) : 요구공학의 상위 학문
- [UML](@/studynotes/4_software_engineering/1_sdlc/uml.md) : 요구사항 모델링 언어
- [유스케이스](@/studynotes/4_software_engineering/4_requirements/requirements_analysis_dfdd.md) : 요구사항 명세 기법
- [사용자 스토리](@/studynotes/4_software_engineering/1_sdlc/scrum_framework.md) : 애자일 요구사항
- [테스팅](@/studynotes/4_software_engineering/6_testing/_index.md) : 요구사항 검증
- [형상 관리](@/studynotes/4_software_engineering/1_sdlc/configuration_management.md) : 요구사항 버전 관리

---

## 어린이를 위한 3줄 비유 설명

1. **문제**: 친구한테 선물을 사주려고 하는데, 그 친구가 뭘 좋아하는지 몰라요. 그냥 내가 좋은 걸 사주면 될까요?

2. **해결(요구공학)**: 먼저 친구한테 물어봐요! "어떤 색을 좋아해?", "어떤 걸 갖고 싶어?" 이렇게 질문하고, 친구의 대답을 정리해요. 그리고 나서 선물을 사요.

3. **효과**: 친구가 진짜 좋아하는 선물을 줄 수 있어요! "이거 딱 원하던 거야!"라며 좋아할 거예요. 요구공학은 이렇게 사용자가 진짜 원하는 것을 찾아내는 방법이에요.
