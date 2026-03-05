+++
title = "62. 스크럼 (Scrum) 프레임워크 - 역할, 이벤트, 산출물"
date = "2026-03-05"
[extra]
categories = "studynotes-se"
tags = ["스크럼", "Scrum", "애자일", "스프린트", "백로그"]
+++

# 스크럼 (Scrum) 프레임워크 - 역할, 이벤트, 산출물

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스크럼은 복잡한 제품 개발을 위한 경량级 프레임워크로, 3가지 역할, 5개 이벤트, 3가지 산출물을 통해 투명성, 검사, 적응의 empiricism(경험주의)을 실현한다.
> 2. **가치**: 스프린트(2~4주) 단위의 반복적 개발로 평균 30~40%의 생산성 향상과 25% 이상의 품질 개선효과를 달성하며, 시장 출시 시간을 50%까지 단축한다.
> 3. **융합**: DevOps, 마이크로서비스, SAFe 등 대규모 애자일 프레임워크의 기반이 되며, AI 기반 도구와 결합하여 스프린트 계획 및 회고 자동화가 가능하다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

스크럼(Scrum)은 1995년 Ken Schwaber와 Jeff Sutherland가 공식화한 애자일 소프트웨어 개발 프레임워크로, 복잡하고 예측 불가능한 문제를 해결하기 위한 경량级 방법론이다. 럭비 용어인 'Scrum'은 경기 재개를 위한 밀집 대형을 의미하며, 팀이 목표를 향해 함께 전진하는 협업 방식을 메타포로 삼았다.

스크럼의 핵심은 '경험적 프로세스 관리 이론(Empirical Process Control Theory)'에 기반하며, 세 가지 기둥인 투명성(Transparency), 검사(Inspection), 적응(Adaptation)을 통해 불확실성을 관리한다.

### 비유

스크럼은 마치 '카레이싱 팀'과 같다. 레이스(프로젝트)는 여러 바퀴(스프린트)로 구성되고, 각 바퀴마다 피트 스톱(스프린트 리뷰/회고)을 통해 타이어 교체, 연료 보충, 전략 수정을 수행한다. 팀 주장(스크럼 마스터)은 팀원들이 최고 성과를 낼 수 있도록 돕고, 감독(제품 책임자)은 우승(제품 목표)을 위한 전략을 수립한다.

### 등장 배경 및 발전 과정

1. **기존 방법론의 한계**: 1980~90대, 폭포수 모델은 '분석-설계-구현-테스트'의 선형적 흐름으로 인해 요구사항 변화에 둔감했다. 프로젝트 실패율이 70%에 달하는 상황에서, 더 유연한 접근법이 필요했다.

2. **패러다임 변화**: 1986년 Hirotaka Takeuchi와 Ikujiro Nonaka가 하버드 비즈니스 리뷰에 발표한 "The New New Product Development Game"에서 럭비의 스크럼을 비유로 한 혁신적 제품 개발 방식을 소개했다. 이후 1995년 Schwaber와 Sutherland가 이를 소프트웨어 개발에 적용한 스크럼 프레임워크를 발표했다.

3. **비즈니스적 요구사항**: 닷컴 버블 이후 빠른 시장 대응이 생존 조건이 되었고, 스타트업부터 대기업까지 스크럼을 도입하여 제품 출시 주기를 단축하고 고객 가치를 극대화하고자 했다.

### 스크럼 프레임워크 개요도

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         스크럼 프레임워크 개요                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      제품 백로그 (Product Backlog)               │   │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │   │
│  │  │ P1  │ │ P2  │ │ P3  │ │ P4  │ │ P5  │ │ P6  │ │ ... │      │   │
│  │  │로그인│ │검색 │ │결제 │ │장바 │ │알림 │ │설정 │ │     │      │   │
│  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘      │   │
│  │  ◀── 우선순위 높음 ──────────────────────────── 우선순위 낮음 ──▶│   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     스프린트 계획 회의                            │   │
│  │         Sprint Planning (최대 8시간 / 4주 스프린트)              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      스프린트 백로그 (Sprint Backlog)            │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐               │   │
│  │  │ 스토리1 │ │ 스토리2 │ │ 스토리3 │ │ 스토리4 │               │   │
│  │  │ 태스크  │ │ 태스크  │ │ 태스크  │ │ 태스크  │               │   │
│  │  │ 3개     │ │ 2개     │ │ 4개     │ │ 3개     │               │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│        ┌─────────────────────┼─────────────────────┐                   │
│        ▼                     ▼                     ▼                   │
│  ┌──────────┐         ┌──────────┐         ┌──────────┐              │
│  │  데일리  │ ──────▶ │   스프린트   │ ──────▶ │  스프린트  │              │
│  │ 스탠드업 │ 24시간   │    수행    │ 2~4주    │   리뷰    │              │
│  │15분/일  │         │            │         │  4시간    │              │
│  └──────────┘         └──────────┘         └──────────┘              │
│        │                                          │                    │
│        └──────────────────────────────────────────┘                    │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       스프린트 회고                              │   │
│  │            Sprint Retrospective (최대 3시간)                     │   │
│  │            "잘한 것, 문제점, 개선할 것" 논의                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      잠재적 출시 가능 제품                       │   │
│  │              Potentially Shippable Product Increment             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 3가지 역할 (Scrum Roles) 상세

| 역할 | 책임 | 상세 활동 | 권한 | 비유 |
|------|------|----------|------|------|
| **제품 책임자 (PO)** | 비즈니스 가치 극대화 | 백로그 관리, 우선순위 결정, 이해관계자 커뮤니케이션, 인수 기준 정의 | 백로그 우선순위 최종 결정 | 영화 감독 |
| **스크럼 마스터 (SM)** | 프로세스 촉진 및 장애 제거 | 스크럼 교육, 장애물 제거, 팀 보호, 회의 진행 | 프로세스 개선 권한 | 코치 |
| **개발 팀** | 제품 증분 인도 | 설계, 구현, 테스트, 통합, 문서화 | 업무 수행 방식 자율 결정 | 배우 |

### 5가지 이벤트 (Scrum Events) 상세

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    스크럼 이벤트 시간 박스 (Time-box)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  스프린트 길이: 1주 ~ 4주 (프로젝트에 따라 결정, 고정)                    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 1. 스프린트 (Sprint)                                             │   │
│  │    - 기간: 1~4주 (고정)                                          │   │
│  │    - 목적: "Done" 인증된 증분 인도                               │   │
│  │    - 특징: 기간 변경 금지, 품질 저하 금지                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│  ┌───────────────────────────┼───────────────────────────────────────┐ │
│  │ 2. 스프린트 계획 회의      │                                       │ │
│  │    - 최대 시간: 2주=4h, 4주=8h                                     │ │
│  │    - 질문: What(목표)? Who(인원)? How(작업)?                       │ │
│  │    - 산출물: 스프린트 목표, 스프린트 백로그                        │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                              │                                          │
│  ┌───────────────────────────┼───────────────────────────────────────┐ │
│  │ 3. 데일리 스크럼 (Daily Scrum)                                     │ │
│  │    - 시간: 15분 (엄격)                                             │ │
│  │    - 질문: 어제 한 일? 오늘 할 일? 장애물?                         │ │
│  │    - 목적: 동기화, 장애물 식별                                     │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                              │                                          │
│  ┌───────────────────────────┼───────────────────────────────────────┐ │
│  │ 4. 스프린트 리뷰 (Sprint Review)                                   │ │
│  │    - 최대 시간: 2주=2h, 4주=4h                                     │ │
│  │    - 참여: 팀 + 이해관계자                                         │ │
│  │    - 활동: 데모, 피드백 수집, 백로그 조정                          │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                              │                                          │
│  ┌───────────────────────────┼───────────────────────────────────────┐ │
│  │ 5. 스프린트 회고 (Sprint Retrospective)                            │ │
│  │    - 최대 시간: 2주=1.5h, 4주=3h                                   │ │
│  │    - 질문: 무엇이 좋았나? 문제는? 무엇을 개선할까?                  │ │
│  │    - 산출물: 개선 액션 아이템                                      │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3가지 산출물 (Scrum Artifacts) 상세

| 산출물 | 정의 | 책임자 | 구성 요소 | 특징 |
|--------|------|--------|----------|------|
| **제품 백로그** | 제품에 필요한 모든 작업의 우선순위 목록 | PO | 사용자 스토리, 버그, 기술 부채, 스파이크 | 동적, 지속적 정제 |
| **스프린트 백로그** | 해당 스프린트에서 수행할 작업 | 개발 팀 | 선택된 스토리 + 태스크 분해 | 스프린트 중 수정 가능 |
| **제품 증분** | "Done" 기준을 충족한 잠재적 출시 가능 제품 | 개발 팀 | 완료된 기능들의 통합 | 누적, 실행 가능 |

### 스크럼의 3가지 기둥 (Empiricism)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   경험적 프로세스 관리의 3가지 기둥                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│         ┌─────────────────────────────────────────────────────┐        │
│         │                                                     │        │
│         │     ┌─────────────────────────────────────┐        │        │
│         │     │         투명성 (Transparency)        │        │        │
│         │     │                                     │        │        │
│         │     │ • 의사결정에 필요한 정보 공개        │        │        │
│         │     │ • 공통 언어(Definition of Done)     │        │        │
│         │     │ • 가시적인 백로그, 번다운 차트       │        │        │
│         │     │                                     │        │        │
│         │     └──────────────┬──────────────────────┘        │        │
│         │                    │                                  │        │
│         │                    ▼                                  │        │
│         │     ┌─────────────────────────────────────┐        │        │
│         │     │         검사 (Inspection)           │        │        │
│         │     │                                     │        │        │
│         │     │ • 스프린트 리뷰, 회고에서 수행       │        │        │
│         │     │ • 데일리 스크럼에서 진척 확인       │        │        │
│         │     │ • 페어 프로그래밍, 코드 리뷰        │        │        │
│         │     │                                     │        │        │
│         │     └──────────────┬──────────────────────┘        │        │
│         │                    │                                  │        │
│         │                    ▼                                  │        │
│         │     ┌─────────────────────────────────────┐        │        │
│         │     │         적응 (Adaptation)           │        │        │
│         │     │                                     │        │        │
│         │     │ • 검사 결과에 따른 프로세스/제품 수정│        │        │
│         │     │ • 백로그 우선순위 조정              │        │        │
│         │     │ • 개선 액션 아이템 이행             │        │        │
│         │     │                                     │        │        │
│         │     └─────────────────────────────────────┘        │        │
│         │                                                     │        │
│         └─────────────────────────────────────────────────────┘        │
│                                                                         │
│         ※ 이 사이클이 스크럼의 모든 이벤트에서 반복됨                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드 예시: 스크럼 관리 시스템

```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum

class SprintStatus(Enum):
    PLANNED = "계획됨"
    ACTIVE = "진행중"
    COMPLETED = "완료"
    CANCELLED = "취소"

class TaskStatus(Enum):
    TODO = "할 일"
    IN_PROGRESS = "진행중"
    DONE = "완료"
    BLOCKED = "차단됨"

@dataclass
class User:
    name: str
    role: str  # PO, SM, Developer

@dataclass
class Task:
    id: str
    title: str
    assignee: Optional[User] = None
    status: TaskStatus = TaskStatus.TODO
    estimated_hours: float = 0.0
    actual_hours: float = 0.0

@dataclass
class UserStory:
    id: str
    title: str
    description: str  # As a <who>, I want <what>, so that <why>
    acceptance_criteria: List[str]
    story_points: int
    tasks: List[Task] = field(default_factory=list)
    priority: int = 0  # 낮을수록 높은 우선순위

    def is_done(self) -> bool:
        """모든 태스크가 완료되었는지 확인"""
        return all(t.status == TaskStatus.DONE for t in self.tasks)

    def calculate_progress(self) -> float:
        """스토리 완료율 계산"""
        if not self.tasks:
            return 0.0
        done_count = sum(1 for t in self.tasks if t.status == TaskStatus.DONE)
        return (done_count / len(self.tasks)) * 100

@dataclass
class Sprint:
    id: str
    name: str
    start_date: datetime
    end_date: datetime
    goal: str
    status: SprintStatus = SprintStatus.PLANNED
    sprint_backlog: List[UserStory] = field(default_factory=list)

    def calculate_velocity(self) -> int:
        """스프린트 속도(Velocity) 계산"""
        return sum(s.story_points for s in self.sprint_backlog if s.is_done())

    def calculate_burndown_data(self) -> List[dict]:
        """번다운 차트 데이터 생성"""
        total_points = sum(s.story_points for s in self.sprint_backlog)
        sprint_days = (self.end_date - self.start_date).days
        ideal_burndown = total_points / sprint_days

        burndown_data = []
        remaining = total_points

        for day in range(sprint_days + 1):
            # 이상적인 번다운
            ideal_remaining = total_points - (ideal_burndown * day)

            # 실제 번다운 (완료된 스토리 포인트 차감)
            # 실제 구현에서는 날짜별 완료 이력을 추적해야 함
            burndown_data.append({
                "day": day,
                "ideal": max(0, ideal_remaining),
                "actual": remaining  # 실제로는 일자별 업데이트
            })

        return burndown_data

    def get_daily_scrum_report(self) -> dict:
        """데일리 스크럼 리포트 생성"""
        blocked_tasks = []
        for story in self.sprint_backlog:
            for task in story.tasks:
                if task.status == TaskStatus.BLOCKED:
                    blocked_tasks.append({
                        "story_id": story.id,
                        "task": task
                    })

        return {
            "sprint": self.name,
            "days_remaining": (self.end_date - datetime.now()).days,
            "total_stories": len(self.sprint_backlog),
            "completed_stories": sum(1 for s in self.sprint_backlog if s.is_done()),
            "blocked_tasks": blocked_tasks,
            "sprint_goal": self.goal
        }

@dataclass
class ProductBacklog:
    items: List[UserStory] = field(default_factory=list)

    def add_item(self, story: UserStory):
        """백로그 항목 추가"""
        self.items.append(story)
        self._reorder_priorities()

    def _reorder_priorities(self):
        """우선순위 재정렬"""
        self.items.sort(key=lambda x: x.priority)

    def get_refined_items(self, max_points: int) -> List[UserStory]:
        """
        스프린트 계획을 위한 정제된 백로그 항목 반환
        스토리 포인트 합이 max_points를 초과하지 않도록
        """
        selected = []
        total_points = 0

        for story in self.items:
            if total_points + story.story_points <= max_points:
                selected.append(story)
                total_points += story.story_points

        return selected

class ScrumTeam:
    """스크럼 팀 관리"""

    def __init__(self, product_owner: User, scrum_master: User):
        self.product_owner = product_owner
        self.scrum_master = scrum_master
        self.developers: List[User] = []
        self.product_backlog = ProductBacklog()
        self.sprints: List[Sprint] = []

    def add_developer(self, developer: User):
        """개발자 추가"""
        if developer.role == "Developer":
            self.developers.append(developer)

    def plan_sprint(self, sprint_name: str, duration_weeks: int,
                    goal: str, avg_velocity: int) -> Sprint:
        """
        스프린트 계획 수립

        Args:
            sprint_name: 스프린트 이름
            duration_weeks: 기간 (주 단위)
            goal: 스프린트 목표
            avg_velocity: 이전 스프린트 평균 속도

        Returns:
            계획된 Sprint 객체
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(weeks=duration_weeks)

        sprint = Sprint(
            id=f"SP-{len(self.sprints) + 1}",
            name=sprint_name,
            start_date=start_date,
            end_date=end_date,
            goal=goal
        )

        # 평균 속도 기반으로 백로그 항목 선택
        sprint.sprint_backlog = self.product_backlog.get_refined_items(avg_velocity)
        sprint.status = SprintStatus.ACTIVE

        self.sprints.append(sprint)
        return sprint

    def calculate_average_velocity(self, last_n_sprints: int = 3) -> int:
        """최근 N개 스프린트 평균 속도 계산"""
        completed_sprints = [s for s in self.sprints
                           if s.status == SprintStatus.COMPLETED]

        if not completed_sprints:
            return 0

        recent_sprints = completed_sprints[-last_n_sprints:]
        total_velocity = sum(s.calculate_velocity() for s in recent_sprints)

        return total_velocity // len(recent_sprints)

    def conduct_retrospective(self, sprint: Sprint) -> dict:
        """스프린트 회고 수행"""
        # 실제로는 토의를 통해 도출됨
        return {
            "sprint": sprint.name,
            "what_went_well": [
                "데일리 스크럼이 효과적이었다",
                "페어 프로그래밍으로 버그가 감소했다"
            ],
            "what_could_improve": [
                "스토리 포인트 산정이 부정확했다",
                "외부 의존성으로 인한 지연 발생"
            ],
            "action_items": [
                "스토리 포인트 산정 가이드라인 도입",
                "외부 API 의존성 사전 식별 프로세스 추가"
            ]
        }
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 스크럼 vs 다른 애자일 방법론 비교

| 비교 차원 | 스크럼 | XP | 칸반 | SAFe |
|----------|-------|-----|------|------|
| **반복 주기** | 2~4주 고정 | 1~2주 | 연속적 | 8~12주 PI |
| **역할 정의** | 3개 (PO/SM/Dev) | 유연함 | 최소화 | 확장됨 |
| **변경 수용 시점** | 스프린트 간 | 언제든 | 실시간 | PI 간 |
| **주요 산출물** | 백로그, 증분 | 코드, 테스트 | 보드, WIP | 피처, 에픽 |
| **확장성** | LeSS/Nexus | 제한적 | 높음 | 대규모 |
| **기술 실천법** | 권장 | 강제(TDD 등) | 선택적 | 선택적 |

### 스크럼 이벤트별 효과 분석

| 이벤트 | 주요 효과 | 실패 시 위험 | 성공 지표 |
|--------|---------|-------------|----------|
| 스프린트 계획 | 목표 명확화, 몰입도 향상 | 범위 크리프, 우왕좌왕 | 계획 대비 달성률 85%+ |
| 데일리 스크럼 | 동기화, 장애물 조기 식별 | 정보 비대칭, 지연 누적 | 장애물 해결 시간 < 24h |
| 스프린트 리뷰 | 피드백 수집, 가시성 확보 | 요구사항 불일치 | 이해관계자 만족도 4.0+ |
| 스프린트 회고 | 지속적 개선, 팀 성장 | 반복적 실수, 사기 저하 | 개선 액션 이행률 70%+ |

### 과목 융합 관점 분석

1. **운영체제와의 융합**: 스크럼의 '타임 박스'는 OS의 선점형 스케줄링과 유사하다. 정해진 시간 내에 작업을 완료해야 하며, 초과 시 다음 슬롯으로 이연된다.

2. **데이터베이스와의 융합**: 제품 백로그는 DB의 인덱스와 유사하게 우선순위 기반 조회를 지원해야 한다. 스프린트 계획 시 인덱스 스캔 방식으로 상위 항목을 빠르게 조회한다.

3. **네트워크와의 융합**: 데일리 스크럼은 네트워크의 heartbeat 패킷과 유사하다. 정기적인 신호 교환으로 연결 상태(팀 동기화)를 확인하고, 장애(차단 태스크)를 조기에 탐지한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오 및 기술사적 판단

**시나리오 1: 분산 팀의 스크럼 도입**
- **상황**: 한국(개발) + 미국(PO) + 인도(QA)로 구성된 글로벌 팀
- **기술사적 판단**:
  - 시간대 겹치는 2시간을 '코어 타임'으로 설정
  - 데일리 스크럼은 비동기(슬랙 + 비디오)로 대체
  - 리뷰/회고는 번갈아가며 양쪽 시간대에 맞춤
- **전략**: 온라인 협업 도구(Miro, Notion) 적극 활용

**시나리오 2: 규제 산업(금융/의료)의 스크럼 적용**
- **상황**: 감사 추적성, 문서화 요구사항이 높은 환경
- **기술사적 판단**:
  - Definition of Done에 '감사 로그', '문서화' 추가
  - 스프린트 리뷰에 컴플라이언스 담당자 참여
  - 자동화된 문서 생성 도구 도입
- **전략**: 스크럼 + 문서화 자동화의 하이브리드

**시나리오 3: 스타트업의 하이퍼 그로스 대응**
- **상황**: 5명 팀에서 50명으로 6개월 내 확장
- **기술사적 판단**:
  - Spotify 모델(Squad/Chapter/Guild)로 확장
  - 공통 플랫폼 팀(Chapter)으로 기술 부채 관리
  - 스크럼 오브 스크럼(Scrum of Scrums) 도입
- **전략**: 역할 분담 명확화, 아키텍처 런웨이 구축

### 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] CI/CD 파이프라인 구축 상태
- [ ] 자동화된 테스트 커버리지
- [ ] 협업 도구 선정 (Jira, Azure DevOps 등)
- [ ] 원격 근무 지원 인프라

**운영/보안적 고려사항**
- [ ] 팀원 교육 계획 (PO/SM/Dev 별)
- [ ] 조직 변화 관리 준비
- [ ] 보안(DevSecOps)의 스프린트 통합
- [ ] 측정 지표(Metrics) 정의

### 안티패턴 (Anti-patterns)

1. **제품 책임자 부재**: PO가 없거나 위임만 하고 실제 결정을 하지 않음. 백로그 우선순위가 모호해지고 팀이 방황.

2. **스크럼 마스터가 팀장**: SM이 팀원에게 지시하고 통제. 자기 조직화 팀이 아니라 전통적 관리 체계로 퇴보.

3. **스프린트 연장**: 마감이 다가와 스프린트 기간을 연장. 이는 근본 원인을 숨기고 타임 박스의 의미를 훼손.

4. **장애물 방치**: 데일리 스크럼에서 식별된 장애물이 해결되지 않음. SM이 적극적으로 제거하지 않으면 팀 신뢰 저하.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | 도입 전 | 도입 후 | 개선율 |
|----------|--------|--------|-------|
| 생산성 (스토리 포인트/스프린트) | 15 | 22 | 47% 향상 |
| 품질 (결함/스프린트) | 8 | 3 | 63% 감소 |
| Time-to-Market | 6개월 | 2개월 | 67% 단축 |
| 팀 만족도 | 3.0/5 | 4.2/5 | 40% 향상 |
| 예측 가능성 (Velocity 표준편차) | ±40% | ±15% | 63% 개선 |

### 미래 전망 및 진화 방향

1. **AI 보조 스크럼**: AI가 번다운 차트 분석, 위험 예측, 회고 패턴 분석을 자동화. SM의 부담을 줄이고 데이터 기반 의사결정 지원.

2. **하이브리드 스크럼**: 스크럼 + 칸반(Scrumban) 등 유연한 혼합 모델 확산. 팀 상황에 맞는 맞춤형 프레임워크.

3. **비즈니스 애자일 확장**: IT를 넘어 마케팅, HR 등 전사 부서로 스크럼 확산. 비즈니스 애자일(Business Agility) 달성.

### 참고 표준/가이드

| 표준/가이드 | 내용 | 출처 |
|-----------|------|------|
| Scrum Guide | 공식 스크럼 가이드 | scrumguides.org |
| Professional Scrum | PSPO, PSM 인증 | Scrum.org |
| Certified Scrum | CSM, CSPO 인증 | Scrum Alliance |
| ISO 21508 | 애자일 프레임워크 표준 | ISO |

---

## 관련 개념 맵 (Knowledge Graph)

- [애자일 선언문](./61_agile_manifesto.md): 스크럼의 철학적 기반
- [XP(eXtreme Programming)](./73_xp.md): 기술적 실천법 중심의 애자일
- [칸반(Kanban)](./84_kanban.md): 흐름 기반 애자일 방법론
- [SAFe](./93_safe.md): 대규모 스크럼 확장 프레임워크
- [DevOps](./97_devops.md): 스크럼과 운영의 통합

---

## 어린이를 위한 3줄 비유 설명

1. **개념**: 스크럼은 학교에서 조별 과제를 할 때와 같아요. 우리 반(개발 팀)은 선생님(PO)이 내주신 숙제(제품 백로그) 중에서 중요한 것부터 골라서 2주 동안 열심히 해요.

2. **원리**: 매일 아침에 친구들과 모여서 "어제 뭐 했어?", "오늘 뭐 할 거야?", "어려운 거 있어?"라고 이야기해요. 그리고 2주가 끝나면 선생님께 보여드리고(리뷰), 우리가 더 잘할 수 있는 방법을 생각해요(회고).

3. **효과**: 이렇게 하면 2주마다 조금씩 완성된 숙제를 볼 수 있어서, 나중에 가서 "이게 아니잖아!" 하고 다시 할 일이 줄어들어요. 친구들과 함께하니까 더 재미있고 빨리 끝낼 수 있어요.
