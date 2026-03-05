+++
title = "131. 요구공학 (Requirements Engineering) 정의 및 필요성"
date = "2026-03-05"
[extra]
categories = "studynotes-se"
tags = ["요구공학", "RequirementsEngineering", "요구사항", "소프트웨어공학"]
+++

# 요구공학 (Requirements Engineering) 정의 및 필요성

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 요구공학은 소프트웨어 개발의 성패를 좌우하는 요구사항을 체계적으로 도출, 분석, 명세, 검증, 관리하는 학문 분야이자 엔지니어링 활동이다.
> 2. **가치**: 요구공학 실패는 프로젝트 실패의 60% 이상을 차지하며, 반면 체계적 요구공학 적용 시 재작업 비용을 40~50% 절감하고 프로젝트 성공률을 30% 이상 향상시킨다.
> 3. **융합**: AI 기반 요구사항 자동 분석, 자연어 처리를 통한 모순 탐지, 블록체인 기반 추적성 관리 등 4차 산업혁명 기술과 결합하여 진화하고 있다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

요구공학(Requirements Engineering, RE)은 소프트웨어 시스템이 충족해야 할 요구사항을 체계적으로 다루는 소프트웨어 공학의 핵심 분야다. 구체적으로, 이해관계자의 요구를 식별하고(Elicitation), 분석하여(Analysis), 명확하게 명세하며(Specification), 이를 검증(Validation)하고 지속적으로 관리(Management)하는 일련의 활동을 포괄한다.

IEEE 610.12 표준에 따르면, 요구사항(Requirement)은 다음 중 하나를 의미한다:
1. 문제를 해결하거나 목표를 달성하기 위해 시스템이 갖추어야 할 조건이나 능력
2. 계약, 표준, 명세서 등이 요구하는 조건이나 능력
3. 위 1번이나 2번의 조건이나 능력을 만족시키는 문서화된 표현

### 비유

요구공학은 마치 '건축 설계'와 같다. 집을 짓기 전에 "방 몇 개가 필요한가?", "화장실은 어디에?", "예산은 얼마?" 등을 명확히 해야 한다. 이 과정에서 건축주(고객)와의 대화, 설계도 검토, 법규 확인 등이 이루어진다. 요구사항이 불명확하면 완공 후 "이게 아니었는데!"라며 재시공해야 하는 상황이 발생한다.

### 등장 배경 및 발전 과정

1. **기존 접근법의 치명적 한계**: Standish Group의 CHAOS Report(2020)에 따르면, IT 프로젝트 실패 원인의 약 70%가 요구사항 관련 문제(불완전한 요구사항 37%, 사용자 참여 부족 13%, 자원 부족 11%, 불현실적 기대 10% 등)였다. 요구사항 오류는 개발 후반부로 갈수록 수정 비용이 기하급수적으로 증가한다(Boehm의 비용 곡선).

2. **패러다임 변화**: 1970년대까지 요구사항은 단순한 '명세서'로 취급되었으나, 1990년대부터 이를 엔지니어링 활동으로 체계화하려는 노력이 시작되었다. 1997년 IEEE 830 표준(SRS 작성 가이드) 발표, 2000년대에는 애자일 방법론의 등장으로 요구사항의 점진적 발견이 강조되었다.

3. **비즈니스적 요구사항**: 디지털 전환(Digital Transformation) 시대에 소프트웨어는 비즈니스의 핵심 경쟁력이다. 빠르게 변화하는 시장 요구에 대응하기 위해, 요구사항을 지속적으로 발견하고 적응하는 능력이 필수적이 되었다.

### 요구공학 프로세스 개요도

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      요구공학 5단계 프로세스                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                        ┌─────────────────┐                             │
│                        │  이해관계자      │                             │
│                        │  (Stakeholders)  │                             │
│                        └────────┬────────┘                             │
│                                 │                                       │
│                                 ▼                                       │
│   ┌───────────────────────────────────────────────────────────────┐   │
│   │                     1. 요구사항 도출 (Elicitation)             │   │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │   │
│   │  │인터뷰   │ │워크숍   │ │관찰     │ │프로토타입│ │설문조사 │ │   │
│   │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │   │
│   └───────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│   ┌───────────────────────────────────────────────────────────────┐   │
│   │                     2. 요구사항 분석 (Analysis)                │   │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │   │
│   │  │우선순위 결정 │ │모순 해결     │ │범위 확정     │             │   │
│   │  └─────────────┘ └─────────────┘ └─────────────┘             │   │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │   │
│   │  │구조적 분석   │ │객체지향 분석 │ │분류/그룹화   │             │   │
│   │  └─────────────┘ └─────────────┘ └─────────────┘             │   │
│   └───────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│   ┌───────────────────────────────────────────────────────────────┐   │
│   │                   3. 요구사항 명세 (Specification)             │   │
│   │  ┌───────────────────────┐ ┌───────────────────────┐         │   │
│   │  │   비정형 명세           │ │   정형 명세             │         │   │
│   │  │   (자연어, 유스케이스)   │ │   (Z, VDM, B 메서드)    │         │   │
│   │  └───────────────────────┘ └───────────────────────┘         │   │
│   │                        ↓                                       │   │
│   │              ┌─────────────────────┐                          │   │
│   │              │ SRS (Software       │                          │   │
│   │              │ Requirements Spec)  │                          │   │
│   │              └─────────────────────┘                          │   │
│   └───────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│   ┌───────────────────────────────────────────────────────────────┐   │
│   │                   4. 요구사항 검증 (Validation)                │   │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │   │
│   │  │인스펙션     │ │워크쓰루     │ │프로토타이핑 │             │   │
│   │  └─────────────┘ └─────────────┘ └─────────────┘             │   │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │   │
│   │  │테스트 케이스│ │모델 검증    │ │시뮬레이션   │             │   │
│   │  └─────────────┘ └─────────────┘ └─────────────┘             │   │
│   └───────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│   ┌───────────────────────────────────────────────────────────────┐   │
│   │                   5. 요구사항 관리 (Management)                │   │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │   │
│   │  │변경 관리     │ │버전 관리     │ │추적성 관리   │             │   │
│   │  └─────────────┘ └─────────────┘ └─────────────┘             │   │
│   │  ┌─────────────┐ ┌─────────────┐                             │   │
│   │  │베이스라인   │ │형상 관리     │                             │   │
│   │  └─────────────┘ └─────────────┘                             │   │
│   └───────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│                                 ▼                                       │
│                        ┌─────────────────┐                             │
│                        │   검증된 요구사항 │                             │
│                        │   (Validated    │                             │
│                        │   Requirements)  │                             │
│                        └─────────────────┘                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 요구사항의 유형 분류

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       요구사항 분류 체계                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐ │
│   │                    기능적 요구사항                               │ │
│   │              (Functional Requirements)                          │ │
│   │  ┌─────────────────────────────────────────────────────────┐   │ │
│   │  │ • 시스템이 수행해야 할 기능/서비스                         │   │ │
│   │  │ • 입력 → 처리 → 출력의 명세                               │   │ │
│   │  │ • 예: "사용자는 상품을 검색할 수 있다"                     │   │ │
│   │  │ • 예: "시스템은 결제 완료 시 이메일을 발송한다"            │   │ │
│   │  └─────────────────────────────────────────────────────────┘   │ │
│   └─────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐ │
│   │                  비기능적 요구사항                               │ │
│   │            (Non-Functional Requirements / Quality Attributes)   │ │
│   │  ┌─────────────────────────────────────────────────────────┐   │ │
│   │  │                    ISO 25010 기반                         │   │ │
│   │  ├─────────────────────────────────────────────────────────┤   │ │
│   │  │ 성능      │ "응답 시간 3초 이내"                          │   │ │
│   │  │ 보안성    │ "개인정보는 AES-256 암호화"                    │   │ │
│   │  │ 가용성    │ "99.9% 가동률 보장"                            │   │ │
│   │  │ 사용성    │ "신규 사용자 학습 시간 30분 이내"              │   │ │
│   │  │ 유지보수성│ "신규 기능 추가 2주 이내"                       │   │ │
│   │  │ 이식성    │ "Windows/Linux/Mac 지원"                       │   │ │
│   │  │ 신뢰성    │ "MTBF 1000시간 이상"                           │   │ │
│   │  │ 호환성    │ "IE/Chrome/Edge 브라우저 지원"                  │   │ │
│   │  └─────────────────────────────────────────────────────────┘   │ │
│   └─────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐ │
│   │                    제약사항 (Constraints)                        │ │
│   │  ┌─────────────────────────────────────────────────────────┐   │ │
│   │  │ • 기술적 제약: 특정 DBMS, 프레임워크 사용 필수            │   │ │
│   │  │ • 비즈니스 제약: 예산, 일정, 인력 제한                    │   │ │
│   │  │ • 법적/규제 제약: GDPR, 개인정보보호법 준수               │   │ │
│   │  │ • 환경적 제약: 하드웨어, 네트워크 제약                    │   │ │
│   │  └─────────────────────────────────────────────────────────┘   │ │
│   └─────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 요구사항 도출 기법 비교

| 기법 | 장점 | 단점 | 적합 상황 | 비용 |
|------|------|------|----------|------|
| **인터뷰** | 심층 정보 획득, 유연함 | 시간 소요, 주관적 | 소수 핵심 이해관계자 | 중 |
| **설문조사** | 대량 데이터, 통계적 분석 | 깊이 부족, 회수율 | 다수 사용자, 정량적 정보 | 저 |
| **워크숍/JAD** | 합의 도출, 창의적 아이디어 | 조직 어려움, 시간 많이 소요 | 복잡한 요구사항, 이견 조정 | 고 |
| **관찰(Shadowing)** | 실제 업무 파악 | 시간 소요, 관찰자 효과 | 업무 프로세스 이해 | 중 |
| **프로토타이핑** | 구체적 피드백, 오해 감소 | 범위 크리프 위험 | UI 중심, 불확실한 요구사항 | 중~고 |
| **문서 분석** | 기존 지식 활용, 객관적 | 구버전 정보, 맥락 부족 | 레거시 시스템 분석 | 저 |
| **페르소나** | 사용자 공감, 설계 방향 | 가상 인물, 편향 위험 | UX 설계, 사용자 중심 개발 | 저~중 |

### 요구사항 명세서(SRS) 품질 특성

| 특성 | 정의 | 검증 방법 |
|------|------|----------|
| **정확성(Correctness)** | 실제 요구를 정확히 반영 | 이해관계자 리뷰 |
| **명확성(Unambiguity)** | 하나의 해석만 가능 | 용어 정의, 모호어 제거 |
| **완전성(Completeness)** | 모든 요구가 포함됨 | 체크리스트, 시나리오 검토 |
| **일관성(Consistency)** | 모순이 없음 | 자동화된 모순 탐지 도구 |
| **수정 용이성(Modifiability)** | 변경이 용이함 | 모듈화, 버전 관리 |
| **추적 가능성(Traceability)** | 출처와 영향 추적 가능 | RTM(Requirements Traceability Matrix) |
| **검증 가능성(Verifiability)** | 테스트/검사 가능 | 인수 기준 명시 |

### 핵심 코드 예시: 요구사항 관리 시스템

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
from datetime import datetime
import re

class RequirementType(Enum):
    FUNCTIONAL = "기능적"
    NON_FUNCTIONAL = "비기능적"
    CONSTRAINT = "제약사항"
    BUSINESS = "비즈니스"
    USER = "사용자"
    SYSTEM = "시스템"

class RequirementPriority(Enum):
    MUST = "반드시 필요"     # MoSCoW: Must
    SHOULD = "필요함"        # MoSCoW: Should
    COULD = "있으면 좋음"    # MoSCoW: Could
    WONT = "이번엔 제외"     # MoSCoW: Won't

class RequirementStatus(Enum):
    DRAFT = "초안"
    ELICITED = "도출됨"
    ANALYZED = "분석됨"
    SPECIFIED = "명세됨"
    VALIDATED = "검증됨"
    BASELINED = "베이스라인"
    CHANGED = "변경됨"

@dataclass
class Stakeholder:
    name: str
    role: str
    contact: str
    influence_level: int  # 1-5

@dataclass
class Requirement:
    id: str
    title: str
    description: str
    type: RequirementType
    priority: RequirementPriority
    status: RequirementStatus
    source: Stakeholder
    acceptance_criteria: List[str]
    created_date: datetime = field(default_factory=datetime.now)
    modified_date: datetime = field(default_factory=datetime.now)
    version: int = 1
    parent_id: Optional[str] = None
    child_ids: List[str] = field(default_factory=list)
    related_ids: List[str] = field(default_factory=list)

    def validate_quality(self) -> Dict[str, bool]:
        """
        요구사항 품질 검증
        Returns: 각 품질 특성별 검증 결과
        """
        results = {}

        # 1. 명확성 검증 - 모호한 단어 탐지
        ambiguous_words = ['적절히', '신속히', '효율적으로', '사용자 친화적',
                          '충분히', '약간', '대체로', '필요시']
        has_ambiguous = any(word in self.description for word in ambiguous_words)
        results['clarity'] = not has_ambiguous

        # 2. 완전성 검증 - 필수 항목 확인
        results['completeness'] = (
            bool(self.title) and
            bool(self.description) and
            len(self.acceptance_criteria) > 0
        )

        # 3. 검증 가능성 - 인수 기준의 측정 가능성
        measurable_patterns = [
            r'\d+.*이내',      # "3초 이내"
            r'\d+%.*이상',     # "99% 이상"
            r'최대 \d+',       # "최대 100명"
            r'최소 \d+',       # "최소 5개"
        ]
        has_measurable = any(
            any(re.search(pattern, criterion)
                for pattern in measurable_patterns)
            for criterion in self.acceptance_criteria
        )
        results['verifiability'] = has_measurable

        # 4. 일관성 - 자기 모순 검사 (간단한 버전)
        # 실제로는 NLP 기반 분석 필요
        contradictory_pairs = [
            ('필수', '선택'), ('항상', '절대 안 함'), ('모든', '없음')
        ]
        has_contradiction = any(
            pair[0] in self.description and pair[1] in self.description
            for pair in contradictory_pairs
        )
        results['consistency'] = not has_contradiction

        return results

    def is_testable(self) -> bool:
        """테스트 가능성 평가"""
        return len(self.acceptance_criteria) > 0 and all(
            len(criterion) > 5 for criterion in self.acceptance_criteria
        )

@dataclass
class RequirementsTraceabilityMatrix:
    """요구사항 추적성 매트릭스 (RTM)"""

    requirements: Dict[str, Requirement] = field(default_factory=dict)

    # 추적성 링크
    source_to_requirement: Dict[str, Set[str]] = field(default_factory=dict)
    requirement_to_design: Dict[str, Set[str]] = field(default_factory=dict)
    requirement_to_code: Dict[str, Set[str]] = field(default_factory=dict)
    requirement_to_test: Dict[str, Set[str]] = field(default_factory=dict)

    def add_requirement(self, req: Requirement):
        """요구사항 추가"""
        self.requirements[req.id] = req

    def link_source(self, source_id: str, req_id: str):
        """출처와 요구사항 연결"""
        if source_id not in self.source_to_requirement:
            self.source_to_requirement[source_id] = set()
        self.source_to_requirement[source_id].add(req_id)

    def link_design(self, req_id: str, design_id: str):
        """요구사항과 설계 요소 연결"""
        if req_id not in self.requirement_to_design:
            self.requirement_to_design[req_id] = set()
        self.requirement_to_design[req_id].add(design_id)

    def link_test(self, req_id: str, test_id: str):
        """요구사항과 테스트 케이스 연결"""
        if req_id not in self.requirement_to_test:
            self.requirement_to_test[req_id] = set()
        self.requirement_to_test[req_id].add(test_id)

    def get_forward_trace(self, req_id: str) -> Dict[str, List[str]]:
        """
        전방 추적 (Forward Trace)
        요구사항 → 설계 → 코드 → 테스트
        """
        return {
            'design': list(self.requirement_to_design.get(req_id, set())),
            'code': list(self.requirement_to_code.get(req_id, set())),
            'test': list(self.requirement_to_test.get(req_id, set()))
        }

    def get_backward_trace(self, req_id: str) -> Dict[str, List[str]]:
        """
        후방 추적 (Backward Trace)
        요구사항 → 출처
        """
        sources = []
        for source_id, req_ids in self.source_to_requirement.items():
            if req_id in req_ids:
                sources.append(source_id)
        return {'source': sources}

    def find_orphan_requirements(self) -> List[str]:
        """추적성이 끊어진 요구사항 식별"""
        orphans = []
        for req_id, req in self.requirements.items():
            # 설계나 테스트와 연결되지 않은 경우
            has_design = req_id in self.requirement_to_design
            has_test = req_id in self.requirement_to_test
            if not has_design and not has_test:
                orphans.append(req_id)
        return orphans

    def generate_coverage_report(self) -> Dict:
        """요구사항 커버리지 리포트 생성"""
        total = len(self.requirements)
        with_design = len(self.requirement_to_design)
        with_test = len(self.requirement_to_test)

        return {
            'total_requirements': total,
            'design_coverage': (with_design / total * 100) if total > 0 else 0,
            'test_coverage': (with_test / total * 100) if total > 0 else 0,
            'orphan_requirements': self.find_orphan_requirements()
        }

class RequirementsEngineeringProcess:
    """요구공학 프로세스 관리"""

    def __init__(self):
        self.rtm = RequirementsTraceabilityMatrix()
        self.elicitation_records: List[Dict] = []
        self.change_requests: List[Dict] = []

    def elicit_requirement(self, technique: str, stakeholder: Stakeholder,
                          raw_content: str) -> Requirement:
        """
        요구사항 도출
        """
        # 도출 기록 저장
        self.elicitation_records.append({
            'technique': technique,
            'stakeholder': stakeholder.name,
            'date': datetime.now(),
            'raw_content': raw_content
        })

        # 요구사항 ID 생성 (자동)
        req_id = f"REQ-{len(self.rtm.requirements) + 1:04d}"

        # 초기 요구사항 생성
        req = Requirement(
            id=req_id,
            title=self._extract_title(raw_content),
            description=raw_content,
            type=RequirementType.FUNCTIONAL,  # 기본값
            priority=RequirementPriority.SHOULD,  # 기본값
            status=RequirementStatus.ELICITED,
            source=stakeholder,
            acceptance_criteria=[]
        )

        self.rtm.add_requirement(req)
        self.rtm.link_source(stakeholder.name, req_id)

        return req

    def _extract_title(self, content: str) -> str:
        """내용에서 제목 추출 (간단한 버전)"""
        # 첫 문장 또는 50자 이내
        first_sentence = content.split('.')[0]
        return first_sentence[:50] + ('...' if len(first_sentence) > 50 else '')

    def analyze_requirement(self, req_id: str) -> Dict:
        """
        요구사항 분석
        - 우선순위 조정
        - 모순 탐지
        - 분류
        """
        req = self.rtm.requirements.get(req_id)
        if not req:
            return {'error': '요구사항을 찾을 수 없습니다'}

        # 품질 검증
        quality = req.validate_quality()

        # 유사 요구사항 탐지 (간단한 버전)
        similar = []
        for other_id, other_req in self.rtm.requirements.items():
            if other_id != req_id:
                # 단어 중복률 기반 유사도 (실제로는 NLP 사용)
                words1 = set(req.description.split())
                words2 = set(other_req.description.split())
                similarity = len(words1 & words2) / len(words1 | words2)
                if similarity > 0.5:
                    similar.append({'id': other_id, 'similarity': similarity})

        req.status = RequirementStatus.ANALYZED

        return {
            'requirement_id': req_id,
            'quality_check': quality,
            'similar_requirements': similar,
            'recommendations': self._generate_recommendations(quality)
        }

    def _generate_recommendations(self, quality: Dict) -> List[str]:
        """품질 개선 권고사항 생성"""
        recommendations = []

        if not quality.get('clarity', True):
            recommendations.append("모호한 표현을 구체적인 수치로 대체하세요")

        if not quality.get('completeness', True):
            recommendations.append("인수 기준을 추가하세요")

        if not quality.get('verifiability', True):
            recommendations.append("측정 가능한 기준을 명시하세요")

        return recommendations

    def request_change(self, req_id: str, change_description: str,
                      requester: str) -> Dict:
        """
        요구사항 변경 요청
        """
        req = self.rtm.requirements.get(req_id)
        if not req:
            return {'error': '요구사항을 찾을 수 없습니다'}

        change_id = f"CR-{len(self.change_requests) + 1:04d}"

        # 영향도 분석
        impact = {
            'forward_trace': self.rtm.get_forward_trace(req_id),
            'related_requirements': req.related_ids
        }

        change_request = {
            'id': change_id,
            'requirement_id': req_id,
            'description': change_description,
            'requester': requester,
            'date': datetime.now(),
            'status': '요청됨',
            'impact_analysis': impact
        }

        self.change_requests.append(change_request)

        return {
            'change_id': change_id,
            'impact_analysis': impact,
            'message': '변경 요청이 등록되었습니다'
        }
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 요구공학 접근법 비교

| 접근법 | 철학 | 프로세스 | 강점 | 약점 |
|--------|------|----------|------|------|
| **전통적(폭포수)** | 선형, 문서 중심 | 완전한 명세 후 개발 | 추적성 용이, 계약 명확 | 변경 비용高, 유연성 낮음 |
| **애자일** | 점진적, 대화 중심 | 백로그로 지속 발전 | 변경 수용, 빠른 피드백 | 문서화 부족, 범위 크리프 위험 |
| **하이브리드** | 균형 | 핵심 명세 + 점진적 상세 | 장점 결합 | 복잡성 증가 |

### 요구사항 도구 비교

| 도구 | 유형 | 주요 기능 | 적합 규모 | 비용 |
|------|------|----------|----------|------|
| **Jira** | 애자일 중심 | 백로그, 스토리, 추적 | 중소~대 | 유료 |
| **IBM DOORS** | 정통 중심 | 추적성, 명세서 관리 | 대형/규제 | 고가 |
| **Polarion** | 하이브리드 | ALM 통합, 추적성 | 중대형 | 유료 |
| **Confluence** | 협업 | 문서화, 협업 | 모든 규모 | 유료(무료 버전) |
| **Excel/Google Sheets** | 간단 | 목록 관리 | 소규모 | 무료 |

### 과목 융합 관점 분석

1. **데이터베이스와의 융합**: 요구사항 추적성 매트릭스(RTM)는 관계형 DB로 모델링할 수 있다. 요구사항, 설계, 코드, 테스트 간의 N:M 관계를 관리하며, 영향도 분석을 위한 그래프 순회 알고리즘을 적용한다.

2. **네트워크와의 융합**: 분산 팀의 요구사항 도출을 위해 화상 회의, 실시간 협업 도구가 필수적이다. WebSocket 기반의 동시 편집, CRDT(Conflict-free Replicated Data Types)를 통한 데이터 일관성 관리가 필요하다.

3. **AI/머신러닝과의 융합**: 자연어 처리(NLP)를 통한 요구사항 자동 분석, 모순 탐지, 중복 식별이 가능하다. GPT 기반 도구로 요구사항에서 테스트 케이스를 자동 생성할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오 및 기술사적 판단

**시나리오 1: 대규모 공공 SI 프로젝트**
- **상황**: 100억 원 규모, 30명 팀, 2년 개발 기간
- **기술사적 판단**:
  - 정식 SRS 문서 필수 (국가 IT 사업 표준)
  - DOORS와 같은 전문 도구 도입
  - CCB(Change Control Board) 운영으로 변경 통제
  - RTM을 통한 완전한 추적성 확보
- **전략**: 문서 중심 + 애자일 실천법(정기 리뷰) 하이브리드

**시나리오 2: 스타트업 MVP 개발**
- **상황**: 5인 팀, 3개월 개발, 불확실성 높음
- **기술사적 판단**:
  - 사용자 스토리 + 인수 기준 중심
  - 과도한 문서화 지양
  - 프로토타이핑을 통한 요구사항 발견
  - 지속적 고객 인터뷰
- **전략**: 애자일/린 접근법, 최소 문서화

**시나리오 3: 안전 필수 시스템(의료기기)**
- **상황**: IEC 62304 준수, FDA 승인 필요
- **기술사적 판단**:
  - 완전한 추적성: 요구사항 → 설계 → 코드 → 테스트
  - 형식적 명세(Formal Specification) 고려
  - 위험 분석(Hazard Analysis)과 요구사항 연계
  - 모든 변경에 대한 감사 추적(Audit Trail)
- **전략**: 엄격한 요구공학 + 안전 분석 통합

### 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] 요구사항 관리 도구 선정
- [ ] 추적성 매트릭스 자동화
- [ ] 버전 관리 시스템 연동
- [ ] 자동화된 품질 검사 도구

**운영/보안적 고려사항**
- [ ] 이해관계자 식별 및 참여 계획
- [ ] 변경 관리 프로세스 정의
- [ ] 접근 통제 및 승인 체계
- [ ] 감사 추적(Audit Trail) 확보

### 안티패턴 (Anti-patterns)

1. **골드 플래팅(Gold Plating)**: 요구사항에 없는 기능을 개발자가 임의로 추가. "이렇게 하면 더 좋을 것 같아서"라는 생각은 위험.

2. **범위 크리프(Scope Creep)**: 통제 없는 요구사항 확장. 변경 관리 프로세스 없이 요구사항이 계속 추가되어 일정/예산 초과.

3. **분석 마비(Analysis Paralysis)**: 완벽한 요구사항을 위해 분석 단계에서 너무 많은 시간을 소비. "완벽한 명세서"는 존재하지 않는다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | 미적용 시 | 적용 시 | 개선율 |
|----------|----------|--------|-------|
| 요구사항 결함 발견률 (개발 전) | 20% | 70% | 250% 향상 |
| 재작업 비용 비율 | 40% | 15% | 63% 감소 |
| 프로젝트 성공률 | 35% | 65% | 86% 향상 |
| 고객 만족도 | 3.0/5 | 4.2/5 | 40% 향상 |
| 요구사항 추적성 | 30% | 95% | 217% 향상 |

### 미래 전망 및 진화 방향

1. **AI 기반 요구공학**: GPT-4, Claude 등 LLM을 활용한 요구사항 자동 분석, 모순 탐지, 테스트 케이스 생성. 자연어 요구사항에서 UML 다이어그램 자동 생성.

2. **지속적 요구공학(Continuous RE)**: DevOps와 통합되어 요구사항이 지속적으로 발견되고 진화하는 모델. 피처 플래그를 통한 요구사항 실험.

3. **블록체인 기반 추적성**: 요구사항 변경 이력의 위변조 방지, 스마트 컨트랙트를 통한 자동화된 승인 프로세스.

### 참고 표준/가이드

| 표준 | 내용 | 출처 |
|------|------|------|
| IEEE 830 | SRS 작성 가이드 | IEEE |
| IEEE 29148 | 요구공학 표준 | IEEE |
| ISO/IEC/IEEE 29148 | 요구공학 프로세스 | ISO |
| IIBA BABOK | 비즈니스 분석 지식 체계 | IIBA |

---

## 관련 개념 맵 (Knowledge Graph)

- [요구사항 유형](./132_requirement_types.md): 기능적/비기능적 요구사항 분류
- [요구사항 도출 기법](./135_elicitation_techniques.md): 인터뷰, 워크숍, 관찰 등
- [요구사항 추적성](./156_traceability.md): RTM과 전/후방 추적
- [유스케이스](./147_usecase_diagram.md): 요구사항의 시나리오 기반 명세
- [SRS 작성](./149_srs.md): 요구사항 명세서 표준

---

## 어린이를 위한 3줄 비유 설명

1. **개념**: 요구공학은 집을 짓기 전에 "어떤 집을 지을지" 꼼꼼하게 적어두는 것과 같아요. "방이 3개 필요해", "화장실은 2개가 좋겠어", "예산은 3억 원까지" 같은 것들을 하나씩 확인하면서 적어요.

2. **원리**: 건축주(고객)님과 이야기해서(도출), "이거랑 저거가 같이 있으면 이상한데?"(분석), "이렇게 적어놓을게요"(명세), "맞나요?"(검증), 그리고 나중에 "화장실 하나 더 추가해요" 하면 기록해두는(관리) 일을 해요.

3. **효과**: 이렇게 미리 잘 적어두면, 집을 다 지어놓고 나서 "아, 화장실이 없네?" 하고 다시 짓는 일이 없어져요. 돈도 아끼고 시간도 아낄 수 있어요.
