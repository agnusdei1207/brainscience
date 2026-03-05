+++
title = "진화적 프로세스 모델 (Evolutionary Process Model)"
date = 2024-05-24
description = "소프트웨어를 점진적으로 진화시키며 개발하는 방법론, 프로토타입을 통해 요구사항을 명확화하고 지속적으로 개선해 나가는 적응적 개발 체계"
weight = 19
categories = ["studynotes-se"]
+++

# 진화적 프로세스 모델 (Evolutionary Process Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 진화적 프로세스 모델은 소프트웨어를 **생물의 진화처럼 점진적으로 발전**시키는 방법론으로, 초기 버전을 기반으로 사용자 피드백을 수집하고 **지속적으로 개선 및 확장**해 나가며 최종 시스템을 완성해 갑니다.
> 2. **가치**: 요구사항이 불확실한 프로젝트에서 **프로토타입을 통한 요구사항 명확화**가 가능하며, 사용자 피드백 기반 개선으로 **최종 사용자 만족도 40% 향상**, 재작업 비용 35% 절감 효과가 있습니다.
> 3. **융합**: 프로토타입 모델의 개념을 확장하여 애자일 방법론의 이론적 기반이 되었으며, 현대의 **MVP(Minimum Viable Product) 개발, 린 스타트업 방식**과 직접적으로 연결됩니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**진화적 프로세스 모델(Evolutionary Process Model)**은 소프트웨어 개발을 생물의 진화 과정처럼 접근하는 방법론입니다. 초기에 기본적인 버전을 개발하고, 이를 사용자에게 제공하여 피드백을 수집한 후, 이 피드백을 반영하여 소프트웨어를 지속적으로 진화(evolve)시켜 나갑니다.

**핵심 철학**:
- "완벽한 계획보다 **빠른 실행과 피드백**이 중요하다"
- "요구사항은 **개발 과정에서 명확해진다**"
- "소프트웨어는 **살아있는 유기체**처럼 성장한다"

**진화적 모델의 핵심 특성**:

| 특성 | 설명 | 기존 모델과의 차이 |
|:---|:---|:---|
| **점진적 명세** | 요구사항이 개발 중에 점차 명확해짐 | 폭포수: 초기에 모든 요구사항 정의 |
| **프로토타입 중심** | 실행 가능한 버전을 빠르게 개발 | 폭포수: 문서 중심 |
| **사용자 참여** | 개발 과정 전반에 걸친 사용자 참여 | 폭포수: 시작과 끝에만 참여 |
| **적응적 계획** | 피드백에 따라 계획 수정 | 폭포수: 고정된 계획 |
| **지속적 전달** | 정기적으로 작동하는 버전 전달 | 폭포수: 최종 1회 전달 |

### 2. 진화적 모델의 유형

```
[진화적 프로세스 모델의 유형]

1. 프로토타입 모델 (Prototype Model)
   ┌───────────────────────────────────────────┐
   │ 요구수집 -> 프로토타입 개발 -> 고객평가    │
   │      ^__________________________|          │
   │         (요구사항 명확해질 때까지)          │
   └───────────────────────────────────────────┘

2. 점진적 모델 (Incremental Model)
   ┌───────────────────────────────────────────┐
   │ [Core] -> [+Module1] -> [+Module2] -> ... │
   │   v1.0      v2.0         v3.0             │
   └───────────────────────────────────────────┘

3. 나선형 모델 (Spiral Model)
   ┌───────────────────────────────────────────┐
   │    위험분석 + 프로토타이핑 + 반복개발       │
   └───────────────────────────────────────────┘

4. 동시적 공학 (Concurrent Engineering)
   ┌───────────────────────────────────────────┐
   │    여러 활동을 병렬로 수행                  │
   └───────────────────────────────────────────┘
```

### 3. 비유: 정원 가꾸기

```
[정원 가꾸기로 보는 진화적 모델]

처음:
- 씨앗을 심고 (초기 버전)
- 물을 주고 가꿈 (개발)
- 어떤 꽃이 피는지 지켜봄 (사용자 피드백)

중간:
- 예쁜 꽃은 더 키우고 (기능 강화)
- 안 피는 꽃은 다른 곳에 심음 (요구사항 변경)
- 새로운 씨앗을 추가 (기능 추가)

나중:
- 아름다운 정원 완성! (최종 제품)

특징:
- 처음에 완벽한 설계가 불가능
- 중간중간 상황에 맞게 조정
- 결과물이 계속 변화하고 성장
```

### 4. 등장 배경 및 발전 과정

#### 1) 기존 모델의 치명적 한계

**폭포수 모델의 문제**:
- 초기 요구사항이 불완전해도 수정 불가
- 사용자가 무엇을 원하는지 모르는 경우 대응 불가
- "나는 내가 원하는 것을 요청했지만, 그건 내가 원하는 게 아니었다"

**현실적 문제**:
```
[요구사항의 불확실성]

고객의 초기 요구: "편리한 쇼핑몰이 필요해요"
        |
        v
개발자의 해석: 검색, 장바구니, 결제 기능
        |
        v
최종 결과물: 복잡하고 사용하기 어려운 쇼핑몰
        |
        v
고객의 반응: "이게 아니에요!"

문제: 고객도 자신이 무엇을 원하는지 정확히 모름
해결: 직접 써보면서 요구사항을 명확히 함 (진화적 모델)
```

#### 2) 진화적 접근의 필요성

| 상황 | 폭포수 | 진화적 |
|:---|:---|:---|
| 요구사항이 명확할 때 | 적합 | 과도한 오버헤드 |
| 요구사항이 불확실할 때 | **실패 가능성 높음** | **적합** |
| 사용자가 무엇을 원하는지 모를 때 | **실패** | **적합** |
| 기술적 위험이 높을 때 | 위험 | 나선형으로 변형 |

#### 3) 역사적 발전

| 시기 | 발전 내용 | 제안자/출처 |
|:---|:---|:---|
| 1970년대 | 프로토타이핑 개념 도입 | Brooks, "Mythical Man-Month" |
| 1980년대 | 진화적 개발 모델 정립 | Gilb, "Evolutionary Delivery" |
| 1988년 | 나선형 모델 | Boehm |
| 1990년대 | RUP(진화적 접근 포함) | Rational |
| 2001년 | 애자일 선언문 | 애자일 연합 |
| 2010년대 | 린 스타트업, MVP | Eric Ries |

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석

| 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 비유 |
|:---|:---|:---|:---|:---|
| **초기 명세** | 기본 요구사항 정의 | 핵심 기능 식별, 사용자 스토리 | 유스케이스, 스토리 맵 | 씨앗 |
| **프로토타입** | 실행 가능한 초기 버전 | 신속 개발, 핵심 기능 구현 | 목업 도구, Rapid Dev | 새싹 |
| **사용자 평가** | 피드백 수집 | 데모, 사용성 테스트, 인터뷰 | 피드백 도구, 설문 | 가지치기 |
| **명세 개선** | 요구사항 업데이트 | 변경 사항 반영, 우선순위 조정 | Jira, Confluence | 비료 |
| **진화 사이클** | 반복적 개선 주기 | 개발-평가-수정-재평가 | CI/CD, 스프린트 | 성장 |
| **최종 버전** | 완성된 제품 | 모든 기능 통합, 품질 검증 | 테스트 도구 | 열매 |

### 2. 정교한 구조 다이어그램

```text
================================================================================
|              EVOLUTIONARY PROCESS MODEL ARCHITECTURE                          |
================================================================================

                        INITIAL REQUIREMENTS
                               |
                               v
    +----------------------------------------------------------+
    |              EVOLUTIONARY DEVELOPMENT CYCLE               |
    +----------------------------------------------------------+
    |                                                          |
    |   +------------------+                                   |
    |   |   1. DEFINE      |                                   |
    |   |   Initial Spec   |                                   |
    |   +--------+---------+                                   |
    |            |                                             |
    |            v                                             |
    |   +------------------+                                   |
    |   |   2. DEVELOP     |                                   |
    |   |   Prototype/     |                                   |
    |   |   Increment      |                                   |
    |   +--------+---------+                                   |
    |            |                                             |
    |            v                                             |
    |   +------------------+                                   |
    |   |   3. DELIVER     |                                   |
    |   |   to Users       |                                   |
    |   +--------+---------+                                   |
    |            |                                             |
    |            v                                             |
    |   +------------------+                                   |
    |   |   4. EVALUATE    |                                   |
    |   |   User Feedback  |                                   |
    |   +--------+---------+                                   |
    |            |                                             |
    |            v                                             |
    |   +------------------+                                   |
    |   |   5. REFINE      |                                   |
    |   |   Requirements   |                                   |
    |   +--------+---------+                                   |
    |            |                                             |
    |            |  +----------------------------------+       |
    |            +->| More Evolution Needed?           |       |
    |               +----------------+-----------------+       |
    |                                |                        |
    |                     Yes        |        No              |
    |                  +-------------+-------------+          |
    |                  |                           |          |
    |                  v                           v          |
    |          [Next Cycle]              [FINAL PRODUCT]      |
    |                                                          |
    +----------------------------------------------------------+


EVOLUTION TIMELINE EXAMPLE
==========================

    Week 1-2         Week 3-4         Week 5-6         Week 7-8
       |                |                |                |
       v                v                v                v
  +-----------+    +-----------+    +-----------+    +-----------+
  | Version   |    | Version   |    | Version   |    | Version   |
  |   0.1     |    |   0.3     |    |   0.6     |    |   1.0     |
  | [Search]  | -> | [Search]  | -> | [Search]  | -> | [Complete |
  |           |    | [Cart]    |    | [Cart]    |    |  System]  |
  |           |    |           |    | [Payment] |    |           |
  +-----------+    +-----------+    +-----------+    +-----------+
       |                |                |                |
       v                v                v                v
   [Feedback]      [Feedback]      [Feedback]      [Launch!]
   "Add filters"   "Add wishlist"  "Fix UX"        "Success!"


EVOLUTION VS REVOLUTION COMPARISON
==================================

    Evolutionary (진화적)              Revolutionary (혁명적/폭포수)
    ===================              =============================

    v0.1 ----> v0.3 ----> v0.6 ----> v1.0    vs    [============] v1.0
      ^          ^          ^                         (완성 후에야)
   사용자      사용자      사용자                     사용자 반응
   반응       반응        반응

    장점: 조기 피드백, 위험 완화            장점: 일관성, 문서화
    단점: 범위 크리프 가능성               단점: 후반 실패 위험

================================================================================
```

### 3. 심층 동작 원리: 진화 사이클

```
[진화 사이클 상세 프로세스]

PHASE 1: 명세 정의 (Specification)
├── 현재 알려진 요구사항 정리
├── 핵심 기능(Must-have) 식별
├── 사용자 스토리 작성
├── 우선순위 부여 (MoSCoW)
└── 개발 범위 설정

PHASE 2: 개발 (Development)
├── 프로토타입/증분 개발
├── 신속한 구현 (Speed over Perfection)
├── 핵심 기능에 집중
├── 기술 부채 감수 (나중에 개선)
└── 내부 테스트

PHASE 3: 전달 (Delivery)
├── 사용자에게 버전 전달
├── 데모/시연 수행
├── 설치 및 사용 지원
├── 초기 사용자 교육
└── 피드백 수집 채널 오픈

PHASE 4: 평가 (Evaluation)
├── 사용자 피드백 수집
│   ├── 정식 피드백 세션
│   ├── 사용성 테스트
│   ├── 버그 리포트 분석
│   └── 사용 패턴 분석
├── 요구사항 변경 사항 식별
├── 새로운 요구사항 발견
└── 우선순위 재조정

PHASE 5: 개선 (Refinement)
├── 명세서 업데이트
├── 변경 사항 영향도 분석
├── 다음 진화 계획 수립
├── 리팩토링 (필요시)
└── 다음 사이클 시작

[진화 종료 조건]
- 모든 Must-have 기능 완료
- 사용자 만족도 기준 달성
- 비즈니스 목표 충족
- 또는 예산/일정 소진
```

### 4. 핵심 알고리즘 & 실무 코드 예시

```python
"""
진화적 프로세스 관리 시스템
Evolutionary Process Management System
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime

class EvolutionPhase(Enum):
    SPECIFICATION = "명세정의"
    DEVELOPMENT = "개발"
    DELIVERY = "전달"
    EVALUATION = "평가"
    REFINEMENT = "개선"
    COMPLETED = "완료"

class FeatureStatus(Enum):
    PROPOSED = "제안됨"
    APPROVED = "승인됨"
    IMPLEMENTED = "구현됨"
    VALIDATED = "검증됨"
    EVOLVED = "진화됨"  # 피드백으로 변경됨

@dataclass
class UserFeedback:
    """사용자 피드백 데이터"""
    feedback_id: str
    version: str
    user_id: str
    category: str           # Bug, Enhancement, New Feature, UX
    description: str
    priority: int           # 1(Critical) ~ 5(Low)
    created_at: datetime = field(default_factory=datetime.now)
    addressed: bool = False

@dataclass
class Feature:
    """기능 단위"""
    feature_id: str
    name: str
    description: str
    priority: str           # Must, Should, Could, Won't (MoSCoW)
    status: FeatureStatus = FeatureStatus.PROPOSED
    version_introduced: str = "0.0"
    feedback_count: int = 0
    evolution_history: List[str] = field(default_factory=list)

    def evolve(self, new_description: str, reason: str) -> None:
        """기능 진화 (피드백 반영)"""
        self.evolution_history.append(
            f"{self.description} -> {new_description}: {reason}"
        )
        self.description = new_description
        self.status = FeatureStatus.EVOLVED


@dataclass
class EvolutionaryVersion:
    """진화 버전"""
    version: str
    release_date: datetime
    features: List[Feature] = field(default_factory=list)
    feedbacks_received: List[UserFeedback] = field(default_factory=list)
    user_satisfaction: Optional[float] = None  # 1.0 ~ 5.0

    @property
    def feature_count(self) -> int:
        return len(self.features)

    def add_feedback(self, feedback: UserFeedback) -> None:
        self.feedbacks_received.append(feedback)

    def calculate_satisfaction(self) -> float:
        """만족도 계산"""
        if not self.feedbacks_received:
            return 0.0
        # 간단히: 높은 우선순위 피드백이 적을수록 만족도 높음
        avg_priority = sum(
            f.priority for f in self.feedbacks_received
        ) / len(self.feedbacks_received)
        # 5점 만점으로 변환
        return max(0, 6 - avg_priority)


class EvolutionaryProject:
    """
    진화적 프로젝트 관리자
    버전별 진화 과정을 관리하고 피드백을 추적
    """

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.versions: Dict[str, EvolutionaryVersion] = {}
        self.features: Dict[str, Feature] = {}
        self.all_feedbacks: List[UserFeedback] = []
        self.current_phase: EvolutionPhase = EvolutionPhase.SPECIFICATION
        self.current_version: str = "0.0"
        self.evolution_cycles: int = 0

    def start_evolution_cycle(self) -> None:
        """새 진화 사이클 시작"""
        self.evolution_cycles += 1
        self.current_phase = EvolutionPhase.SPECIFICATION

    def create_initial_specification(
        self,
        features: List[Tuple[str, str, str, str]]
    ) -> None:
        """
        초기 명세 생성
        features: [(id, name, description, priority), ...]
        """
        for fid, name, desc, priority in features:
            feature = Feature(
                feature_id=fid,
                name=name,
                description=desc,
                priority=priority,
                version_introduced=self.current_version
            )
            self.features[fid] = feature

        self.current_phase = EvolutionPhase.DEVELOPMENT

    def release_version(
        self,
        version: str,
        feature_ids: List[str]
    ) -> EvolutionaryVersion:
        """버전 릴리즈"""
        new_version = EvolutionaryVersion(
            version=version,
            release_date=datetime.now()
        )

        for fid in feature_ids:
            if fid in self.features:
                self.features[fid].status = FeatureStatus.IMPLEMENTED
                self.features[fid].version_introduced = version
                new_version.features.append(self.features[fid])

        self.versions[version] = new_version
        self.current_version = version
        self.current_phase = EvolutionPhase.DELIVERY

        return new_version

    def collect_feedback(
        self,
        version: str,
        feedbacks: List[UserFeedback]
    ) -> Dict:
        """피드백 수집 및 분석"""
        if version not in self.versions:
            raise ValueError(f"버전 {version}이 존재하지 않습니다")

        version_obj = self.versions[version]

        for fb in feedbacks:
            version_obj.add_feedback(fb)
            self.all_feedbacks.append(fb)

        self.current_phase = EvolutionPhase.EVALUATION

        # 피드백 분석
        analysis = self._analyze_feedbacks(feedbacks)
        return analysis

    def _analyze_feedbacks(
        self,
        feedbacks: List[UserFeedback]
    ) -> Dict:
        """피드백 분석"""
        by_category = {}
        by_priority = {}

        for fb in feedbacks:
            # 카테고리별 집계
            if fb.category not in by_category:
                by_category[fb.category] = 0
            by_category[fb.category] += 1

            # 우선순위별 집계
            if fb.priority not in by_priority:
                by_priority[fb.priority] = 0
            by_priority[fb.priority] += 1

        # 다음 진화에서 처리할 항목 식별
        critical_items = [
            fb for fb in feedbacks
            if fb.priority <= 2
        ]

        return {
            "total_feedbacks": len(feedbacks),
            "by_category": by_category,
            "by_priority": by_priority,
            "critical_items": [
                {"id": fb.feedback_id, "desc": fb.description}
                for fb in critical_items
            ],
            "recommendation": self._generate_recommendation(feedbacks)
        }

    def _generate_recommendation(
        self,
        feedbacks: List[UserFeedback]
    ) -> str:
        """다음 진화 방향 추천"""
        if not feedbacks:
            return "피드백이 없습니다. 사용자 평가를 진행하세요."

        bug_count = sum(1 for fb in feedbacks if fb.category == "Bug")
        enhancement_count = sum(
            1 for fb in feedbacks if fb.category == "Enhancement"
        )

        if bug_count > len(feedbacks) * 0.5:
            return "버그가 많습니다. 품질 안정화에 집중하세요."
        elif enhancement_count > len(feedbacks) * 0.5:
            return "기능 개선 요청이 많습니다. UX 개선에 집중하세요."
        else:
            return "균형잡힌 피드백입니다. 우선순위에 따라 진화하세요."

    def evolve_requirements(
        self,
        feature_id: str,
        new_description: str,
        reason: str
    ) -> None:
        """요구사항 진화"""
        if feature_id not in self.features:
            raise ValueError(f"기능 {feature_id}가 존재하지 않습니다")

        self.features[feature_id].evolve(new_description, reason)
        self.current_phase = EvolutionPhase.REFINEMENT

    def is_evolution_complete(self) -> Tuple[bool, str]:
        """진화 완료 여부 확인"""
        # 모든 Must 기능이 검증되었는지 확인
        must_features = [
            f for f in self.features.values()
            if f.priority == "Must"
        ]

        if not must_features:
            return (False, "Must 기능이 정의되지 않았습니다")

        all_validated = all(
            f.status == FeatureStatus.VALIDATED
            for f in must_features
        )

        if all_validated:
            self.current_phase = EvolutionPhase.COMPLETED
            return (True, "모든 핵심 기능이 검증되었습니다")
        else:
            return (False, "아직 검증되지 않은 Must 기능이 있습니다")

    def get_evolution_report(self) -> Dict:
        """진화 보고서 생성"""
        return {
            "project_name": self.project_name,
            "evolution_cycles": self.evolution_cycles,
            "current_version": self.current_version,
            "current_phase": self.current_phase.value,
            "total_versions": len(self.versions),
            "total_features": len(self.features),
            "total_feedbacks": len(self.all_feedbacks),
            "feature_evolution": {
                fid: {
                    "name": f.name,
                    "status": f.status.value,
                    "evolution_count": len(f.evolution_history),
                    "history": f.evolution_history
                }
                for fid, f in self.features.items()
            },
            "version_history": {
                ver: {
                    "feature_count": v.feature_count,
                    "feedback_count": len(v.feedbacks_received),
                    "satisfaction": v.user_satisfaction
                }
                for ver, v in self.versions.items()
            }
        }


# ===== 실제 사용 예시 =====
if __name__ == "__main__":
    # 프로젝트 초기화
    project = EvolutionaryProject("이커머스 플랫폼")

    # 진화 사이클 1 시작
    project.start_evolution_cycle()

    # 초기 명세 정의
    initial_features = [
        ("F-001", "상품 검색", "키워드로 상품 검색", "Must"),
        ("F-002", "장바구니", "상품을 장바구니에 담기", "Must"),
        ("F-003", "결제", "신용카드 결제", "Should"),
        ("F-004", "위시리스트", "상품을 위시리스트에 추가", "Could"),
    ]
    project.create_initial_specification(initial_features)

    # 버전 0.1 릴리즈 (최소 기능)
    v01 = project.release_version("0.1", ["F-001"])

    # 사용자 피드백 수집
    feedbacks_v01 = [
        UserFeedback("FB-001", "0.1", "user1", "Enhancement",
                     "필터링 기능이 필요해요", 2),
        UserFeedback("FB-002", "0.1", "user2", "Enhancement",
                     "검색 결과 정렬이 필요해요", 3),
        UserFeedback("FB-003", "0.1", "user3", "Bug",
                     "특수문자 검색 시 오류", 1),
    ]

    analysis = project.collect_feedback("0.1", feedbacks_v01)
    print("=== 버전 0.1 피드백 분석 ===")
    print(f"총 피드백: {analysis['total_feedbacks']}")
    print(f"카테고리별: {analysis['by_category']}")
    print(f"추천: {analysis['recommendation']}")

    # 요구사항 진화
    project.evolve_requirements(
        "F-001",
        "키워드로 상품 검색 + 필터링 + 정렬",
        "사용자 피드백 FB-001, FB-002 반영"
    )

    # 진화 사이클 2 시작
    project.start_evolution_cycle()

    # 버전 0.2 릴리즈
    v02 = project.release_version("0.2", ["F-001", "F-002"])

    # 진화 보고서
    report = project.get_evolution_report()
    print("\n=== 진화 보고서 ===")
    print(f"진화 사이클 수: {report['evolution_cycles']}")
    print(f"현재 버전: {report['current_version']}")
    print(f"총 피드백 수: {report['total_feedbacks']}")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 프로세스 모델 비교

| 비교 항목 | 폭포수 | 진화적 | 반복적 점진적 | 애자일 |
|:---|:---|:---|:---|:---|
| **요구사항** | 초기 완전 정의 | **점진적 명확화** | 증분별 정의 | 지속적 발견 |
| **계획** | 고정 | **적응적** | 증분별 계획 | 스프린트별 |
| **프로토타입** | 없음 | **핵심** | 선택적 | 스파이크 |
| **사용자 참여** | 시작/끝 | **지속적** | 증분마다 | 매일 |
| **위험 관리** | 후반 | **조기 발견** | 분산 | 지속 |
| **문서화** | 높음 | **중간** | 중간~높음 | 낮음 |
| **변경 비용** | 높음 | **낮음** | 중간 | 낮음 |
| **적합 상황** | 요구 확정 | **요구 불확실** | 대형 프로젝트 | 빠른 변화 |

### 2. 진화적 모델의 변형들

```
[진화적 모델의 주요 변형]

1. 프로토타입 모델 (Prototype Model)
   - 단일 프로토타입을 반복 개선
   - 주로 요구사항 명확화 목적

2. 점진적 모델 (Incremental Model)
   - 기능별 증분을 순차적 추가
   - 각 증분은 완전한 기능 제공

3. 진화적 전달 (Evolutionary Delivery)
   - Gilb 제안
   - 핵심 기능 먼저 전달, 점진적 확장

4. 나선형 모델 (Spiral Model)
   - 위험 분석 + 진화적 개발
   - 대형/고위험 프로젝트용

5. 동시적 공학 (Concurrent Engineering)
   - 여러 활동 병렬 수행
   - 개발 주기 단축
```

### 3. 과목 융합 관점 분석

#### 진화적 모델 + 요구공학

```
[요구공학과의 융합]

전통적 요구공학:
1. 요구사항 도출 (초기 1회)
2. 요구사항 분석
3. 요구사항 명세
4. 요구사항 검증

진화적 요구공학:
1. 초기 요구사항 도출
2. 프로토타입 개발
3. 사용자 평가
4. 요구사항 발견 (새로운 요구)
5. 요구사항 명세 업데이트
6. 다음 프로토타입 개발
7. ... 반복 ...

장점:
- 사용자가 직접 써보면서 진짜 요구 발견
- 숨겨진 요구사항 발견
- 요구사항 우선순위 검증
```

#### 진화적 모델 + 프로젝트 관리

| PMBOK 영역 | 진화적 모델 적용 |
|:---|:---|
| **범위 관리** | 범위가 점진적으로 확정됨, 롤링 웨이브 |
| **일정 관리** | 진화 사이클별 일정, 유연한 마일스톤 |
| **비용 관리** | 진화별 예산 배분, 단계적 투자 |
| **위험 관리** | 프로토타입으로 위험 조기 식별 |
| **품질 관리** | 각 진화마다 품질 검증 |

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

#### [시나리오 1] 혁신적 신규 서비스 개발

**상황**:
- 프로젝트: AI 기반 개인화 추천 서비스
- 규모: 10인, 12개월
- 특성: 요구사항 매우 불확실, 신기술 적용

**기술사적 판단**:

```
선택: 진화적 프로세스 모델 (MVP 방식)

근거:
1. 요구사항 불확실성: 사용자도 무엇을 원하는지 모름
2. 기술적 위험: AI 모델 성능이 비즈니스 모델에 영향
3. 시장 검증: 빠른 MVP로 시장 반응 확인 필요

진화 계획:
┌─────────────────────────────────────────────────────┐
│ Evolution 1 (MVP, 8주)                              │
│ - 기본 추천 알고리즘 (룰 기반)                       │
│ - 사용자 행동 데이터 수집                            │
│ - A/B 테스트 프레임워크                              │
│ -> 목적: 시장 수요 검증                              │
├─────────────────────────────────────────────────────┤
│ Evolution 2 (16주)                                  │
│ - ML 기반 추천 모델 도입                             │
│ - 개인화 기능                                       │
│ - 피드백 루프 구축                                  │
│ -> 목적: 핵심 가치 검증                              │
├─────────────────────────────────────────────────────┤
│ Evolution 3 (12주)                                  │
│ - 딥러닝 모델 업그레이드                             │
│ - 실시간 추천                                       │
│ - 확장성 확보                                       │
│ -> 목적: 경쟁력 강화                                │
├─────────────────────────────────────────────────────┤
│ Evolution 4 (8주)                                   │
│ - 안정화 및 최적화                                   │
│ - 운영 이관                                        │
│ -> 목적: 프로덕션 준비                              │
└─────────────────────────────────────────────────────┘

각 진화마다:
- 명확한 가설 설정
- 성공 지표 정의
- 사용자 피드백 수집
- 다음 진화 방향 결정
```

#### [시나리오 2] 레거시 시스템 현대화

**상황**:
- 프로젝트: 20년 된 ERP 시스템 현대화
- 규모: 30인, 24개월
- 특성: 비즈니스 연속성 필수, 기존 기능 유지

**기술사적 판단**:

```
선택: 진화적 접근 + 스트랭글러 패턴

근거:
1. 비즈니스 연속성: 한 번에 전환 불가
2. 기능 검증: 기존 기능과 신규 기능 병행 운영
3. 위험 분산: 점진적 마이그레이션

진화 전략:
1. 새 아키텍처 기반 구축
2. 저위험 기능부터 진화적 전환
3. 고위험 기능은 충분히 검증 후 전환
4. 마지막에 레거시 폐기

각 진화 단계:
- 양쪽 시스템 병행 운영
- 데이터 동기화
- 사용자 그룹별 순차 전환
```

### 2. 도입 시 고려사항 (체크리스트)

**요구사항 관련**:
- [ ] 요구사항이 불확실한가? (진화적 모델 적합)
- [ ] 사용자가 자신의 요구를 명확히 표현할 수 있는가?
- [ ] 요구사항 변경이 예상되는가?

**프로젝트 관련**:
- [ ] 프로토타입 개발 역량이 있는가?
- [ ] 사용자 참여가 가능한 구조인가?
- [ ] 유연한 계약 구조인가? (Time & Material)

**위험 관련**:
- [ ] 기술적 위험이 높은가?
- [ ] 시장 검증이 필요한가?
- [ ] 실패 시 조기 철수가 가능한가?

**조직 관련**:
- [ ] 변화를 수용하는 조직 문화인가?
- [ ] 신속한 의사결정이 가능한가?
- [ ] 피드백 수집 프로세스가 있는가?

### 3. 주의사항 및 안티패턴

| 안티패턴 | 증상 | 원인 | 해결 방안 |
|:---|:---|:---|:---|
| **범위 크리프** | 요구사항이 계속 늘어남 | 명확한 완료 기준 없음 | MoSCoW 우선순위, 종료 조건 설정 |
| **영원한 프로토타입** | 프로토타입이 제품이 됨 | 품질 관리 부재 | 프로토타입은 버리거나 리팩토링 |
| **피드백 과부하** | 피드백이 너무 많아 처리 불가 | 피드백 필터링 없음 | 우선순위 기반 피드백 관리 |
| **사용자 참여 부족** | 피드백이 없음 | 사용자 참여 미보장 | 정기 데모, 사용자 챔피언 |
| **아키텍처 부재** | 진화할수록 구조 악화 | 초기 아키텍처 무시 | 아키텍처 런웨이 확보 |

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | 적용 전 | 적용 후 | 개선 효과 |
|:---|:---|:---:|:---:|:---:|
| **요구사항 적중률** | 사용자 요구 충족도 | 60% | 90% | +30%p |
| **재작업 비용** | 후반 재작업 비용 | 40% | 15% | -62.5% |
| **사용자 만족도** | 최종 만족도 (5점) | 3.0 | 4.2 | +40% |
| **위험 완화** | 조기 위험 발견률 | 20% | 75% | +55%p |
| **시장 적기성** | 출시 시간 | 100% | 60% | -40% |
| **투자 효율** | 무효 기능 개발률 | 30% | 10% | -67% |

### 2. 미래 전망 및 진화 방향

1. **린 스타트업과의 융합**:
   - Build-Measure-Learn 사이클
   - MVP에서 MLP(Minimum Lovable Product)로

2. **AI 기반 진화**:
   - 사용자 행동 분석으로 자동 개선 추천
   - A/B 테스트 자동화

3. **지속적 전달 (CD)**:
   - 진화 주기 단축 (주 → 일 → 시간)
   - Feature Flag로 점진적 출시

4. **데이터 기반 진화**:
   - 사용 데이터 분석 기능 우선순위 결정
   - 가설 검증 자동화

### 3. 참고 표준/가이드

| 표준/가이드 | 내용 | 적용 분야 |
|:---|:---|:---|
| **ISO/IEC 12207** | 진화적 프로세스 포함 | 범용 |
| **IEEE 830** | 요구사항 명세 (반복적 개선 허용) | 요구공학 |
| **PMBOK** | 롤링 웨이브 계획 | 프로젝트 관리 |
| **Lean Startup** | MVP, 피벗 | 스타트업 |
| **Design Thinking** | 프로토타이핑, 사용자 중심 | 혁신 |

---

## 관련 개념 맵 (Knowledge Graph)

- [소프트웨어 공학](@/studynotes/4_software_engineering/1_sdlc/1_software_engineering.md) : 진화적 모델의 이론적 기반
- [프로토타입 모델](@/studynotes/4_software_engineering/1_sdlc/6_prototype_model.md) : 진화적 모델의 구현 방식
- [반복적 점진적 모델](@/studynotes/4_software_engineering/1_sdlc/8_iterative_incremental_model.md) : 구조화된 진화 접근
- [애자일 방법론](@/studynotes/4_software_engineering/1_sdlc/agile_methodology.md) : 진화적 사고의 구체화
- [요구공학](@/studynotes/4_software_engineering/4_requirements/requirements_engineering.md) : 요구사항 진화 관리
- [위험 관리](@/studynotes/4_software_engineering/3_project/_index.md) : 조기 위험 식별

---

## 어린이를 위한 3줄 비유 설명

1. **문제**: 새로운 요리를 만들어야 하는데, 손님이 어떤 맛을 좋아하는지 몰라요. 그냥 만들었다가 "이게 아니야!"라고 하면 큰일이죠!

2. **해결(진화적 모델)**: 먼저 간단한 맛보기 요리를 내드려요. 손님이 "좀 더 짜게 해주세요" 하면 짜게 만들고, "이건 빼고 저건 넣어주세요" 하면 그렇게 해요. 이렇게 계속 고쳐나가는 거예요.

3. **효과**: 손님이 진짜 좋아하는 맛을 찾을 수 있어요! 중간에 "이건 정말 맛있어요!" 하는 걸 듣는 것도 기분 좋고, 나중에는 완벽한 요리가 완성되죠!
