+++
title = "68. 스프린트 계획 (Sprint Planning)"
date = "2026-03-05"
[extra]
categories = "studynotes-se"
+++

# 스프린트 계획 (Sprint Planning)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스프린트 계획(Sprint Planning)은 새로운 스프린트를 시작할 때 수행할 작업을 계획하는 스크럼 이벤트로, '무엇(What)'을 할지와 '어떻게(How)' 할지를 협업하여 결정하고 스프린트 목표(Sprint Goal)를 수립하는 시간박스된(2주 스프린트 기준 최대 4시간) 활동이다.
> 2. **가치**: 효과적인 스프린트 계획은 스프린트 완료율을 85% 이상으로 유지하고, 팀의 예측 가능성을 30% 향상시키며, 불필요한 작업을 25% 감소시켜 전체 생산성을 극대화한다.
> 3. **융합**: 스프린트 계획은 용량 계획(Capacity Planning), 속도(Velocity) 분석, 의존성 매핑, 리스크 기반 우선순위화를 융합하여 실행 가능한 계획을 수립하고 CI/CD 파이프라인과 연계된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
스프린트 계획(Sprint Planning)은 스크럼 가이드에서 스프린트의 시작을 알리는 공식 이벤트로 정의된다. 이 회의에서는 다음 세 가지 질문에 답한다:
1. **이번 스프린트의 목표는 무엇인가?** (Sprint Goal)
2. **제품 백로그 항목 중 어떤 것을 이번 스프린트에 포함할 수 있는가?** (Sprint Backlog)
3. **선정된 항목을 어떻게 구현할 것인가?** (Work Plan)

스프린트 계획은 **전체 스크럼 팀**(PO, SM, 개발팀)이 참여하며, 타임박스(Time-box)를 준수한다. 1개월 스프린트는 최대 8시간, 2주 스프린트는 최대 4시간이 권장된다.

### 💡 비유
스프린트 계획은 **"여행 출발 전 가족 회의"**에 비유할 수 있다. 가족이 함께 앉아 "이번 여행에서 무엇을 보고 싶니?"(목표)를 정하고, "시간과 예산을 고려해 어디를 갈까?"(항목 선정)를 결정하며, "어떻게 이동하고 숙소는 어디서 잡을까?"(작업 계획)를 논의한다. 모두가 동의해야 출발할 수 있듯, 스프린트 계획도 팀의 합의가 필수적이다.

### 등장 배경 및 발전 과정

**1. 기존 계획 방식의 치명적 한계점**
- 프로젝트 착수 시 일괄 계획(Big Upfront Planning)의 높은 불확실성
- 관리자 주도 계획으로 인한 팀 주도권 상실
- 추정 정확도 저하 및 일정 지연의 악순환
- 계획과 실행의 괴리로 인한 "계획대로 안 되는" 문화

**2. 혁신적 패러다임 변화**
- 1995년 스크럼 프레임워크와 함께 스프린트 계획 개념 도입
- 2001년 애자일 선언문의 "주기적 간격으로 작업" 원칙 반영
- 2000년대 후반 플래닝 포커(Planning Poker)의 표준화
- 2010년대 데이터 기반 계획(Velocity, Cycle Time)의 도입

**3. 비즈니스적 요구사항**
- Time-to-Market 예측 가능성 향상
- 자원 활용 효율화
- 이해관계자 기대 관리

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 비유 |
|-----------|-----------|---------------------|----------------|------|
| **스프린트 목표** | 스프린트의 핵심 목적 | 비즈니스 가치 중심, 달성 가능성 | Product Goal | 여행 목적 |
| **백로그 선정** | 수행 항목 결정 | 용량 기반, 우선순위 준수 | Jira, Azure DevOps | 행선지 선정 |
| **용량 계산** | 팀 가용 시간 파악 | 휴가, 회의, 집중 계수 고려 | Capacity Planning | 예산 산정 |
| **작업 분해** | 기술적 세부 계획 | 태스크 단위 분할, 시간 추정 | Task Board | 일정 짜기 |
| **의존성 식별** | 외부/내부 의존 파악 | 블로커 사전 식별 | Dependency Matrix | 예약 필요 |
| **합의 형성** | 팀 커밋먼트 | 투표, 토론, 동의 | Fist of Five | 가족 합의 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      SPRINT PLANNING ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                   PRE-PLANNING INPUTS (사전 준비물)                       │   │
│  │                                                                          │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                │   │
│  │  │ Product       │  │ Team          │  │ Technical     │                │   │
│  │  │ Backlog       │  │ Velocity      │  │ Constraints   │                │   │
│  │  │ (정제된 상태)  │  │ (과거 데이터) │  │ (아키텍처)     │                │   │
│  │  │               │  │               │  │               │                │   │
│  │  │ □ Story A     │  │ Sprint 1: 30  │  │ API 연동 필요 │                │   │
│  │  │ □ Story B     │  │ Sprint 2: 35  │  │ DB 마이그레이션│                │   │
│  │  │ □ Story C     │  │ Sprint 3: 32  │  │ 인프라 제약   │                │   │
│  │  └───────────────┘  └───────────────┘  └───────────────┘                │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                     │                                          │
│                                     ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                   SPRINT PLANNING EVENT (계획 회의)                       │   │
│  │                                                                          │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │                    PART 1: WHAT (무엇을)                           │  │   │
│  │  │  Timebox: 1-2시간 | 주도: Product Owner                            │  │   │
│  │  │  ┌─────────────────────────────────────────────────────────────┐  │  │   │
│  │  │  │                                                             │  │  │   │
│  │  │  │  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │  │  │   │
│  │  │  │  │ Product │    │ Sprint  │    │ Backlog │                 │  │  │   │
│  │  │  │  │ Goal    │───→│ Goal    │───→│ Items   │                 │  │  │   │
│  │  │  │  │ Context │    │ Draft   │    │ Selection│                 │  │  │   │
│  │  │  │  └─────────┘    └─────────┘    └─────────┘                 │  │  │   │
│  │  │  │                                                             │  │  │   │
│  │  │  │  PO presents:                                               │  │  │   │
│  │  │  │  • Product Goal 진척 상황                                   │  │  │   │
│  │  │  │  • 우선순위가 높은 백로그 항목 발표                          │  │  │   │
│  │  │  │  • 비즈니스 맥락 설명                                       │  │  │   │
│  │  │  │                                                             │  │  │   │
│  │  │  │  Team discusses:                                            │  │  │   │
│  │  │  │  • 질문 및 명확화                                           │  │  │   │
│  │  │  │  • 각 항목의 가치 이해                                      │  │  │   │
│  │  │  │  • 스프린트 목표 초안 작성                                   │  │  │   │
│  │  │  │                                                             │  │  │   │
│  │  │  └─────────────────────────────────────────────────────────────┘  │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  │                                     │                                    │   │
│  │                                     ▼                                    │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │                    PART 2: HOW (어떻게)                            │  │   │
│  │  │  Timebox: 1-2시간 | 주도: Development Team                        │  │   │
│  │  │  ┌─────────────────────────────────────────────────────────────┐  │  │   │
│  │  │  │                                                             │  │  │   │
│  │  │  │  ┌─────────────┐                                           │  │  │   │
│  │  │  │  │  Capacity   │                                           │  │  │   │
│  │  │  │  │  Planning   │                                           │  │  │   │
│  │  │  │  │             │                                           │  │  │   │
│  │  │  │  │ Team: 5명   │                                           │  │  │   │
│  │  │  │  │ Days: 10일  │                                           │  │  │   │
│  │  │  │  │ PTO: 2일    │                                           │  │  │   │
│  │  │  │  │ Focus: 0.7  │                                           │  │  │   │
│  │  │  │  │ ───────────│                                           │  │  │   │
│  │  │  │  │ Eff: 196시간│                                           │  │  │   │
│  │  │  │  └──────┬──────┘                                           │  │  │   │
│  │  │  │         │                                                  │  │  │   │
│  │  │  │         ▼                                                  │  │  │   │
│  │  │  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │  │  │   │
│  │  │  │  │  Work       │    │  Dependency │    │  Final      │    │  │  │   │
│  │  │  │  │  Breakdown  │───→│  Check      │───→│  Commitment │    │  │  │   │
│  │  │  │  │             │    │             │    │             │    │  │  │   │
│  │  │  │  │ Story → Task│    │ Blockers?   │    │ Team agrees │    │  │  │   │
│  │  │  │  │ Estimates   │    │ External?   │    │ to goal     │    │  │  │   │
│  │  │  │  │ (hours)     │    │ Risks?      │    │             │    │  │  │   │
│  │  │  │  └─────────────┘    └─────────────┘    └─────────────┘    │  │  │   │
│  │  │  │                                                             │  │  │   │
│  │  │  └─────────────────────────────────────────────────────────────┘  │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                     │                                          │
│                                     ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                   PLANNING OUTPUTS (산출물)                               │   │
│  │                                                                          │   │
│  │  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐    │   │
│  │  │   Sprint Goal     │  │  Sprint Backlog   │  │   Team            │    │   │
│  │  │   (스프린트 목표) │  │  (스프린트 백로그)│  │   Commitment      │    │   │
│  │  │                   │  │                   │  │   (팀 약속)       │    │   │
│  │  │ "이번 스프린트    │  │ ■ Story A (5pt)   │  │                   │    │   │
│  │  │  목표는 사용자가  │  │ ■ Story B (3pt)   │  │ ✓ 우리는 이 목표  │    │   │
│  │  │  소셜 로그인을    │  │ ■ Story C (8pt)   │  │   를 달성하기     │    │   │
│  │  │  할 수 있게 하는  │  │ ■ Task 1 (4h)     │  │   위해 최선을     │    │   │
│  │  │  것이다"          │  │ ■ Task 2 (2h)     │  │   다하겠습니다"   │    │   │
│  │  └───────────────────┘  └───────────────────┘  └───────────────────┘    │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 플래닝 포커(Planning Poker)

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                     PLANNING POKER PROCESS                                     │
│                                                                                │
│   피보나치 수열 기반 스토리 포인트 추정                                         │
│   ┌─────────────────────────────────────────────────────────────┐             │
│   │  0.5 │ 1 │ 2 │ 3 │ 5 │ 8 │ 13 │ 21 │ 34 │ 55 │ 89 │ ∞     │             │
│   └─────────────────────────────────────────────────────────────┘             │
│                                                                                │
│   Process Flow:                                                                │
│                                                                                │
│   Step 1        Step 2        Step 3        Step 4        Step 5              │
│   ┌──────┐     ┌──────┐     ┌──────┐     ┌──────┐     ┌──────┐               │
│   │ Story│     │Discuss│    │ Vote  │     │Debate│     │Consensus│            │
│   │ Read │ ──→ │       │ ──→ │       │ ──→ │      │ ──→ │         │            │
│   └──────┘     └──────┘     └──────┘     └──────┘     └──────┘               │
│       │            │            │            │            │                   │
│       ▼            ▼            ▼            ▼            ▼                   │
│   PO가 스토리   팀이 질문    각자 카드   높은/낮은    합의 도출              │
│   설명          및 토론      선택        값 논의                              │
│                                                                                │
│   Example:                                                                     │
│   ┌───────────────────────────────────────────────────────────────────┐       │
│   │  Story: "사용자가 이메일로 로그인할 수 있다"                        │       │
│   │                                                                   │       │
│   │  Alice: 5    Bob: 8    Charlie: 5    Diana: 3    Eve: 5          │       │
│   │                                                                   │       │
│   │  ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐                │       │
│   │  │  5  │   │  8  │   │  5  │   │  3  │   │  5  │                │       │
│   │  └─────┘   └─────┘   └─────┘   └─────┘   └─────┘                │       │
│   │                                                                   │       │
│   │  Gap Analysis:                                                    │       │
│   │  Bob (8): "소셜 로그인도 포함?" → 아니요, 별도 스토리             │       │
│   │  Diana (3): "비밀번호 찾기도?" → 아니요, 별도 스토리              │       │
│   │                                                                   │       │
│   │  Re-vote: All → 5                                                │       │
│   │  Consensus: 5 Story Points                                       │       │
│   └───────────────────────────────────────────────────────────────────┘       │
│                                                                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 알고리즘: 스프린트 백로그 구성 최적화

```python
"""
스프린트 백로그 구성 최적화 알고리즘
- 용량, 우선순위, 의존성을 고려한 최적의 백로그 구성
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple
from enum import Enum

class Priority(Enum):
    MUST = 1
    SHOULD = 2
    COULD = 3

@dataclass
class BacklogItem:
    """백로그 항목"""
    id: str
    title: str
    story_points: int
    priority: Priority
    business_value: int
    dependencies: List[str] = field(default_factory=list)
    risk_level: int = 1  # 1-5

    def __hash__(self):
        return hash(self.id)

@dataclass
class SprintCapacity:
    """스프린트 용량"""
    team_size: int
    sprint_days: int
    velocity: float
    pto_days: int = 0
    focus_factor: float = 0.75

    @property
    def available_points(self) -> int:
        """가용 스토리 포인트"""
        effective_days = self.sprint_days - (self.pto_days / self.team_size)
        return int(self.velocity * (effective_days / self.sprint_days))

@dataclass
class SprintPlan:
    """스프린트 계획 결과"""
    selected_items: List[BacklogItem]
    total_points: int
    sprint_goal: str
    risks: List[str]
    dependencies_blocked: List[str]

class SprintPlanner:
    """스프린트 계획 최적화기"""

    def __init__(self, backlog: List[BacklogItem], capacity: SprintCapacity):
        self.backlog = backlog
        self.capacity = capacity
        self.selected: List[BacklogItem] = []
        self.blocked: Set[str] = set()

    def plan(self) -> SprintPlan:
        """
        최적의 스프린트 백로그 구성
        우선순위, 용량, 의존성을 종합 고려
        """
        # 1. 우선순위 정렬
        sorted_items = sorted(
            self.backlog,
            key=lambda x: (x.priority.value, -x.business_value)
        )

        # 2. 의존성 그래프 구축
        dependency_graph = self._build_dependency_graph()

        # 3. 그리디 선택 + 의존성 해결
        remaining_capacity = self.capacity.available_points

        for item in sorted_items:
            if remaining_capacity <= 0:
                break

            # 의존성 확인
            unmet_deps = self._check_dependencies(
                item, dependency_graph
            )

            if unmet_deps:
                # 의존성이 해결되지 않으면 스킵하거나 의존성도 포함
                can_include = self._try_include_dependencies(
                    item, unmet_deps, remaining_capacity, sorted_items
                )
                if can_include:
                    for dep_item in can_include:
                        self.selected.append(dep_item)
                        remaining_capacity -= dep_item.story_points
                else:
                    self.blocked.add(item.id)
                    continue
            else:
                # 용량 확인
                if item.story_points <= remaining_capacity:
                    self.selected.append(item)
                    remaining_capacity -= item.story_points

        # 4. 결과 생성
        total_points = sum(item.story_points for item in self.selected)
        sprint_goal = self._generate_sprint_goal()
        risks = self._identify_risks()
        blocked_items = list(self.blocked)

        return SprintPlan(
            selected_items=self.selected,
            total_points=total_points,
            sprint_goal=sprint_goal,
            risks=risks,
            dependencies_blocked=blocked_items
        )

    def _build_dependency_graph(self) -> Dict[str, Set[str]]:
        """의존성 그래프 구축"""
        graph = {}
        for item in self.backlog:
            graph[item.id] = set(item.dependencies)
        return graph

    def _check_dependencies(self, item: BacklogItem,
                            graph: Dict[str, Set[str]]) -> Set[str]:
        """미충족 의존성 확인"""
        selected_ids = {i.id for i in self.selected}
        unmet = set()
        for dep in item.dependencies:
            if dep not in selected_ids:
                unmet.add(dep)
        return unmet

    def _try_include_dependencies(self, item: BacklogItem,
                                   unmet_deps: Set[str],
                                   capacity: int,
                                   all_items: List[BacklogItem]) -> Optional[List[BacklogItem]]:
        """의존성 항목 포함 시도"""
        item_map = {i.id: i for i in all_items}
        to_include = []
        total_cost = 0

        # 위상 정렬로 의존성 순서 결정
        for dep_id in self._topological_sort(unmet_deps, item_map):
            if dep_id in item_map:
                dep_item = item_map[dep_id]
                to_include.append(dep_item)
                total_cost += dep_item.story_points

        total_cost += item.story_points

        if total_cost <= capacity:
            to_include.append(item)
            return to_include
        return None

    def _topological_sort(self, ids: Set[str],
                          item_map: Dict) -> List[str]:
        """간소화된 위상 정렬"""
        # 실제로는 더 복잡한 알고리즘 필요
        return list(ids)

    def _generate_sprint_goal(self) -> str:
        """스프린트 목표 자동 생성"""
        if not self.selected:
            return "스프린트 목표 미정"

        # 상위 항목들의 테마 파악
        must_items = [i for i in self.selected if i.priority == Priority.MUST]
        if must_items:
            return f"{must_items[0].title} 외 {len(self.selected)-1}개 항목 완료"

        return f"{self.selected[0].title} 외 {len(self.selected)-1}개 항목 완료"

    def _identify_risks(self) -> List[str]:
        """리스크 식별"""
        risks = []

        # 고위험 항목 확인
        high_risk = [i for i in self.selected if i.risk_level >= 4]
        if high_risk:
            risks.append(f"고위험 항목 {len(high_risk)}개 포함")

        # 용량 근접 확인
        total = sum(i.story_points for i in self.selected)
        if total > self.capacity.available_points * 0.95:
            risks.append("용량 근접: 버퍼 부족")

        # 의존성 차단 항목
        if self.blocked:
            risks.append(f"의존성으로 차단된 항목 {len(self.blocked)}개")

        return risks

    def suggest_alternatives(self) -> List[Dict]:
        """대안 조합 제안"""
        alternatives = []

        # Must 항목만 포함한 보수적 계획
        must_only = [i for i in self.backlog if i.priority == Priority.MUST]
        must_points = sum(i.story_points for i in must_only)

        alternatives.append({
            "name": "보수적 (Must Only)",
            "items": len(must_only),
            "points": must_points,
            "risk": "낮음"
        })

        # 현재 선택에 대한 정보
        alternatives.append({
            "name": "균형형 (현재 선택)",
            "items": len(self.selected),
            "points": sum(i.story_points for i in self.selected),
            "risk": "중간"
        })

        return alternatives


# 실무 예시
if __name__ == "__main__":
    # 백로그 항목
    backlog = [
        BacklogItem("S1", "로그인 기능", 5, Priority.MUST, 90, risk_level=2),
        BacklogItem("S2", "소셜 로그인", 8, Priority.SHOULD, 70,
                   dependencies=["S1"], risk_level=3),
        BacklogItem("S3", "비밀번호 찾기", 3, Priority.SHOULD, 50,
                   dependencies=["S1"], risk_level=2),
        BacklogItem("S4", "프로필 편집", 5, Priority.COULD, 40, risk_level=1),
        BacklogItem("S5", "알림 설정", 5, Priority.COULD, 30, risk_level=1),
        BacklogItem("S6", "다크 모드", 3, Priority.COULD, 20, risk_level=1),
    ]

    # 용량
    capacity = SprintCapacity(
        team_size=5,
        sprint_days=10,
        velocity=30,
        pto_days=2
    )

    # 계획 수립
    planner = SprintPlanner(backlog, capacity)
    plan = planner.plan()

    print("=== 스프린트 계획 결과 ===")
    print(f"스프린트 목표: {plan.sprint_goal}")
    print(f"총 포인트: {plan.total_points}/{capacity.available_points}")
    print(f"선정 항목: {len(plan.selected)}개")
    print("\n선정된 항목:")
    for item in plan.selected:
        print(f"  - {item.id}: {item.title} ({item.story_points}pt)")

    if plan.risks:
        print(f"\n리스크:")
        for risk in plan.risks:
            print(f"  ⚠️ {risk}")

    print(f"\n대안 조합:")
    for alt in planner.suggest_alternatives():
        print(f"  {alt['name']}: {alt['points']}pt, 리스크: {alt['risk']}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 추정 기법

| 비교 항목 | 플래닝 포커 | T셔츠 사이즈 | 볼륜 비교 | 완벽한 날 |
|-----------|------------|-------------|----------|----------|
| **정확도** | 높음 | 낮음 | 중간 | 높음 |
| **속도** | 느림 | 빠름 | 빠름 | 중간 |
| **참여도** | 높음 | 낮음 | 중간 | 높음 |
| **규모** | 중소형 | 대형 초기 | 대형 | 모든 규모 |
| **주요 용도** | 스토리 추정 | 에픽 추정 | 백로그 정제 | 용량 계획 |
| **도구** | 실물 카드/앱 | 화이트보드 | 스프레드시트 | 캘린더 |

### 과목 융합 관점 분석

#### 1. 프로젝트 관리 × 애자일 방법론 융합
스프린트 계획은 전통적 WBS(Work Breakdown Structure)의 애자일 버전이다. 차이점은 WBS가 프로젝트 착수 시 일괄 수립되는 반면, 스프린트 계획은 매 스프린트마다 수립된다. EVM(Earned Value Management)의 개념을 적용하면 스프린트 계획이 PV(Planned Value)가 된다.

#### 2. 요구공학 × 설계 융합
스프린트 계획에서 선정된 스토리는 즉시 설계 단계로 진입한다. 백로그 정제(Refinement)가 잘 되어 있을수록 스프린트 계획의 효율이 높아진다. 인수 기준(Acceptance Criteria)은 테스트 케이스 설계의 기반이 된다.

#### 3. 리스크 관리 × 품질 관리 융합
스프린트 계획에서 리스크가 높은 항목은 우선순위를 조정하거나 스파이크(Spike)로 선행 조사를 진행한다. 정의(Definition of Done)에 포함된 품질 기준이 용량 계산에 반영된다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단: 실무 시나리오 3가지

#### 시나리오 1: 용량 과다 계획 방지
**상황**: 팀이 매 스프린트마다 과도하게 계획하여 완료율 저하

**기술사적 의사결정 과정**:
1. **데이터 분석**: 최근 5스프린트 완료율 vs 계획 포인트 비교
2. **버퍼 적용**: 평균 속도의 85%만 계획에 반영
3. **Unknowns 고려**: 예상치 못한 작업을 위한 10% 예비
4. **점진적 증가**: 안정화 후 점진적으로 계획 증가

#### 시나리오 2: 외부 의존성 관리
**상황**: 타 팀 API가 필요한 스토리로 인해 스프린트 차질

**기술사적 의사결정 과정**:
1. **의존성 매트릭스 작성**: 스프린트 내 모든 외부 의존 식별
2. **선제적 커뮤니케이션**: 스프린트 시작 전 의존 팀에 일정 확인
3. **Mock/Stub 활용**: 외부 API를 Mock으로 대체하여 개발 진행
4. **대안 스토리**: 의존성 미해결 시 작업 가능한 대안 준비

#### 시나리오 3: 신규 팀원 온보딩
**상황**: 스프린트 중간에 신규 팀원 합류로 용량 변화

**기술사적 의사결정 과정**:
1. **러닝 커브 고려**: 신규 팀원은 첫 스프린트에 30-50% 생산성만 기대
2. **멘토링 비용**: 기존 팀원의 온보딩 시간을 용량에서 차감
3. **페어링 계획**: 신규 팀원과 경력 팀원의 페어 프로그래밍 일정 포함
4. **점진적 통합**: 첫 주는 관찰 및 학습, 둘째 주부터 작업 할당

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] 백로그 정제 수준 (Ready 상태 항목 충분성)
- [ ] 추정 데이터 (과거 속도 이력)
- [ ] CI/CD 파이프라인 준비도
- [ ] 의존성 매핑 도구

#### 운영/보안적 고려사항
- [ ] 스프린트 계획 회의 타임박스 준수
- [ ] 전체 스크럼 팀 참여 보장
- [ ] 스프린트 목표의 명확성
- [ ] 계획 변경 프로세스 정의

### 주의사항 및 안티패턴

1. **Big Upfront Design**: 스프린트 계획에서 과도한 설계 논의
2. **Manager Dictates**: 관리자가 범위를 일방적으로 결정
3. **No Buffer**: 예비 없이 꽉 찬 계획
4. **Ignore Dependencies**: 의존성 고려 없이 계획

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 개선 전 | 개선 후 | 개선율 |
|------|---------|---------|--------|
| 스프린트 완료율 | 60% | 85% | **42% 향상** |
| 계획 정확도 | 50% | 80% | **60% 향상** |
| 평균 계획 시간 | 6시간 | 3시간 | **50% 단축** |
| 팀 만족도 | 65% | 85% | **31% 향상** |

### 미래 전망 및 진화 방향

1. **AI 기반 추정**: 과거 데이터 기반 스토리 포인트 자동 추천
2. **실시간 용량 조정**: 팀 구성 변화에 따른 동적 재계획
3. **예측적 분석**: 몬테카를로 시뮬레이션 기반 완료 확률 예측
4. **자동화된 의존성 분석**: 코드베이스 분석을 통한 의존성 자동 식별

### ※ 참고 표준/가이드
- **Scrum Guide 2020**: 스프린트 계획의 공식 정의
- **Planning Poker**: James Grenning의 추정 기법
- **Mountain Goat Software**: Mike Cohn의 스토리 포인트 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)

1. [스프린트](./67_sprint.md) - 스프린트 계획이 시작하는 개발 주기
2. [제품 백로그](./66_product_backlog.md) - 스프린트 백로그의 원천
3. [스토리 포인트](./82_story_point.md) - 스프린트 계획에 사용되는 추정 단위
4. [플래닝 포커](./83_planning_poker.md) - 스프린트 계획의 추정 기법
5. [개발 팀](./65_development_team.md) - 스프린트 계획의 핵심 참여자
6. [번다운 차트](./72_burndown_chart.md) - 스프린트 계획 진척 추적 도구

---

## 👶 어린이를 위한 3줄 비유 설명

**비유: 가족 여행 계획 회의**

1. **어디 갈지 정해요**: "이번 주말에 놀이공원 가자!"라고 가족이 함께 목표를 정해요. 엄마 아빠가 가고 싶은 곳을 설명해요.

2. **시간을 계산해요**: "놀이공원이 3시간 걸리고, 점심 먹는 데 1시간이야. 그럼 저녁 전까지 집에 올 수 있을까?" 하고 계산해요.

3. **모두 동의해요**: 가족 모두가 "좋아! 그럼 가자!" 하고 약속해요. 한 사람이라도 반대하면 다시 이야기해요.
