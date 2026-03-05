+++
title = "67. 스프린트 (Sprint)"
date = "2026-03-05"
[extra]
categories = "studynotes-se"
+++

# 스프린트 (Sprint)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스프린트(Sprint)는 스크럼에서 1~4주(통상 2주)의 고정된 기간 동안 잠재적으로 출시 가능한 제품 증분(Potentially Releasable Increment)을 생성하는 핵심 컨테이너 이벤트로, 계획-실행-검토-회고의 사이클을 통해 적응형 개발을 실현한다.
> 2. **가치**: 스프린트 기반 개발은 평균 배포 주기를 3개월에서 2주로 단축하고(85% 감소), 요구사항 변경 비용을 70% 절감하며, 팀의 예측 가능성(Predictability)을 80% 이상으로 향상시킨다.
> 3. **융합**: 스프린트는 CI/CD 파이프라인, 테스트 자동화, 코드 리뷰, 피처 플래그와 결합하여 지속적 배포(Continuous Deployment)를 실현하고, SRE의 에러 예산(Error Budget)과 연계하여 안정성-속도 균형을 달성한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
스프린트(Sprint)는 스크럼 가이드(2020)에서 "스크럼의 심장부"로 정의되며, 스크럼의 다른 모든 이벤트가 이를 중심으로 진행된다. 스프린트는 **타임박스(Time-box)** 개념으로, 1개월 이하의 고정된 기간 동안 '완료(Done)'된, 사용 가능한 제품 증분을 생성한다. 스프린트가 진행되는 동안에는 다음과 같은 규칙이 적용된다:
- 품질 목표를 낮추는 변경은 허용되지 않음
- 범위는 제품 책임자와 개발팀 간 협의 하에 명확화 및 재협상 가능
- 스프린트는 취소될 수 있으나(PO 권한), 극히 드물어야 함

### 💡 비유
스프린트는 **"마라톤의 중간 계표"** 또는 **"요리 대회의 라운드"**에 비유할 수 있다. 요리 대회에서 각 라운드(스프린트)는 제한된 시간(타임박스) 내에 완성된 요리(증분)를 제출해야 한다. 심사위원(이해관계자)이 피드백을 주면 다음 라운드에서 반영한다. 한 라운드가 진행 중일 때는 레시피(범위)를 바꿀 수 없지만, 다음 라운드를 준비할 때는 새로운 전략을 세울 수 있다.

### 등장 배경 및 발전 과정

**1. 기존 개발 방식의 치명적 한계점**
- 폭포수 모델의 긴 피드백 루프 (6개월~1년)
- 중간 산출물의 "완료" 개념 모호
- 변경에 대한 높은 비용과 저항
- 진척률 파악의 어려움 (90% 완료의 90%...)

**2. 혁신적 패러다임 변화**
- 1993년 제프 서덜랜드가 Easel사에서 최초 스프린트 도입
- 1995년 OOPSLA 컨퍼런스에서 스크럼 공식 발표
- 2001년 애자일 선언문의 "정기적으로 작동하는 소프트웨어" 원칙 반영
- 2010년대 DevOps와 결합하여 CI/CD 파이프라인의 단위가 됨

**3. 비즈니스적 요구사항**
- Time-to-Market 단축 압박
- 시장 변화에 대한 민첩한 대응
- 투자 대비 빠른 가치 회수(ROI)

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 비유 |
|-----------|-----------|---------------------|----------------|------|
| **스프린트 계획** | 목표 설정 및 범위 합의 | 목표, 선정 항목, 작업 계획 | Planning Poker | 메뉴 선정 |
| **데일리 스크럼** | 진행 상황 동기화 | 어제/오늘/장애물 공유 | Standup Bot | 주방 미팅 |
| **개발 작업** | 증분 생성 | 코딩, 테스트, 통합 | CI/CD, Git | 요리 과정 |
| **스프린트 리뷰** | 결과물 검증 및 피드백 | 데모, 이해관계자 피드백 | Demo Tools | 시식 평가 |
| **스프린트 회고** | 프로세스 개선 | 성공/개선점/실험 도출 | Retromat | 평가 회의 |
| **증분(Increment)** | 완료된 기능 집합 | DoD 준수, 잠재적 출시 가능 | Artifact Repository | 완성 요리 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         SPRINT LIFECYCLE ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                   SPRINT TIMEBOX (1-4 weeks)                             │   │
│  │                                                                          │   │
│  │   Day 1                 Day 2~N-1                 Last Day              │   │
│  │   ┌─────────────┐      ┌─────────────────┐     ┌─────────────────┐     │   │
│  │   │   SPRINT    │      │   DEVELOPMENT   │     │     REVIEW &    │     │   │
│  │   │  PLANNING   │ ───→ │   & DAILY       │ ──→ │   RETROSPECTIVE │     │   │
│  │   │             │      │   SCRUM         │     │                 │     │   │
│  │   │ • 목표 설정 │      │ • 구현          │     │ • 데모          │     │   │
│  │   │ • 항목 선정 │      │ • 테스트        │     │ • 피드백        │     │   │
│  │   │ • 작업 분해 │      │ • 통합          │     │ • 개선 도출     │     │   │
│  │   │ • 용량 확인 │      │ • 장애물 해결   │     │ • 액션 아이템   │     │   │
│  │   └─────────────┘      └─────────────────┘     └─────────────────┘     │   │
│  │        │                       │                        │               │   │
│  │        ▼                       ▼                        ▼               │   │
│  │   Sprint Backlog        Daily Progress            Increment +          │   │
│  │   (스프린트 백로그)      (일일 진척)               Process Insights     │   │
│  │                                                  (프로세스 인사이트)    │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                 SPRINT BACKLOG EVOLUTION                                 │   │
│  │                                                                          │   │
│  │   Product Backlog         Sprint Backlog           Task Board           │   │
│  │   ┌───────────────┐      ┌───────────────┐      ┌───────────────┐      │   │
│  │   │ □ Story A     │      │ ■ Story A     │      │ TODO │ DOING │ DONE │      │   │
│  │   │ □ Story B     │ ───→ │ ■ Story C     │ ───→ │──────┼───────┼──────│      │   │
│  │   │ □ Story C     │      │ ■ Story E     │      │ Task1│ Task3 │ Task2│      │   │
│  │   │ □ Story D     │      │               │      │ Task4│       │ Task5│      │   │
│  │   │ □ Story E     │      └───────────────┘      │ Task6│       │      │      │   │
│  │   └───────────────┘                             └───────────────┘      │   │
│  │                                                                          │   │
│  │   PO가 우선순위화        팀이 수용량 내       일일 진척 추적            │   │
│  │                           선정                                           │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    SPRINT FLOW DIAGRAM                                   │   │
│  │                                                                          │   │
│  │   ┌───────────┐                        ┌───────────┐                    │   │
│  │   │  Product  │                        │  Sprint   │                    │   │
│  │   │  Backlog  │ ──────────────────────→│  Backlog  │                    │   │
│  │   └───────────┘   Sprint Planning      └─────┬─────┘                    │   │
│  │         ▲                                    │                          │   │
│  │         │                                    ▼                          │   │
│  │         │         ┌──────────────────────────────────────┐              │   │
│  │         │         │            DEVELOPMENT               │              │   │
│  │         │         │  ┌─────────────────────────────┐     │              │   │
│  │         │         │  │ Daily Scrum (15min/day)     │     │              │   │
│  │         │         │  │ ┌───┐ ┌───┐ ┌───┐ ┌───┐    │     │              │   │
│  │         │         │  │ │Mon│ │Tue│ │Wed│ │Thu│    │     │              │   │
│  │         │         │  │ └───┘ └───┘ └───┘ └───┘    │     │              │   │
│  │         │         │  └─────────────────────────────┘     │              │   │
│  │         │         │                │                      │              │   │
│  │         │         │                ▼                      │              │   │
│  │         │         │  ┌─────────────────────────────┐     │              │   │
│  │         │         │  │      Increment (증분)       │     │              │   │
│  │         │         │  │  • Potentially Releasable  │     │              │   │
│  │         │         │  │  • Meets Definition of Done│     │              │   │
│  │         │         │  └─────────────────────────────┘     │              │   │
│  │         │         └──────────────┬───────────────────────┘              │   │
│  │         │                        │                                      │   │
│  │         │         ┌──────────────┴───────────────┐                      │   │
│  │         │         ▼                              ▼                      │   │
│  │         │   ┌───────────┐                  ┌───────────┐                │   │
│  │         │   │  Review   │                  │Retrospect │                │   │
│  │         │   │  (데모)   │                  │  (회고)   │                │   │
│  │         │   └─────┬─────┘                  └─────┬─────┘                │   │
│  │         │         │                              │                      │   │
│  │         │         ▼                              ▼                      │   │
│  │         │   ┌───────────┐                  ┌───────────┐                │   │
│  │         │   │ Feedback  │                  │Improvement│                │   │
│  │         │   │ (피드백)  │                  │ (개선안)  │                │   │
│  │         │   └─────┬─────┘                  └─────┬─────┘                │   │
│  │         │         │                              │                      │   │
│  │         └─────────┴──────────────────────────────┘                      │   │
│  │                  다음 스프린트에 반영                                    │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: 스프린트 이벤트 상세

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                     SPRINT EVENTS BREAKDOWN                                    │
│                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  1. SPRINT PLANNING (스프린트 계획)                                      │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Timebox: 2주 스프린트 → 최대 4시간                                │  │  │
│  │  │                                                                   │  │  │
│  │  │  Part 1: WHAT (무엇을)                     Part 2: HOW (어떻게)   │  │  │
│  │  │  ┌─────────────────────┐                 ┌─────────────────────┐  │  │  │
│  │  │  │ • PO가 목표 제시    │                 │ • 팀이 작업 분해    │  │  │  │
│  │  │  │ • 백로그 항목 선정  │ ──────────────→ │ • 기술 접근법 논의  │  │  │  │
│  │  │  │ • 범위 합의         │                 │ • 의존성 식별       │  │  │  │
│  │  │  │ • 우선순위 확인     │                 │ • 용량 확인         │  │  │  │
│  │  │  └─────────────────────┘                 └─────────────────────┘  │  │  │
│  │  │                                                                   │  │  │
│  │  │  Output: Sprint Goal + Sprint Backlog                            │  │  │
│  │  └───────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  2. DAILY SCRUM (데일리 스크럼)                                          │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Timebox: 15분 / 매일 동일 시간                                    │  │  │
│  │  │                                                                   │  │  │
│  │  │  Three Questions (전통적)          Focus Areas (현대적)           │  │  │
│  │  │  ┌─────────────────────┐          ┌─────────────────────┐        │  │  │
│  │  │  │ 1. 어제 무엇을?     │          │ • Sprint Goal 진척  │        │  │  │
│  │  │  │ 2. 오늘 무엇을?     │    OR    │ • 백로그 항목 상태  │        │  │  │
│  │  │  │ 3. 장애물이 있는가? │          │ • 장애물 식별       │        │  │  │
│  │  │  └─────────────────────┘          └─────────────────────┘        │  │  │
│  │  │                                                                   │  │  │
│  │  │  Purpose: 동기화, 장애물 식별, 계획 조정                          │  │  │
│  │  │  NOT a Status Report to SM!                                       │  │  │
│  │  └───────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  3. SPRINT REVIEW (스프린트 리뷰)                                        │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Timebox: 2주 스프린트 → 최대 2시간                                │  │  │
│  │  │                                                                   │  │  │
│  │  │  Agenda:                                                          │  │  │
│  │  │  ┌─────────────────────────────────────────────────────────────┐  │  │  │
│  │  │  │ 1. PO: 참석자 환영, 스프린트 목표 상기 (5분)                  │  │  │  │
│  │  │  │ 2. Team: 완료된 항목 데모 (What we built)                    │  │  │  │
│  │  │  │ 3. Team: 미완료 항목 설명 (Why, what's next)                 │  │  │  │
│  │  │  │ 4. PO: 백로그 현황 및 예상 일정 (Current state)              │  │  │  │
│  │  │  │ 5. Collaborative: 다음 단계 논의 (What's next)               │  │  │  │
│  │  │  └─────────────────────────────────────────────────────────────┘  │  │  │
│  │  │                                                                   │  │  │
│  │  │  Output: Revised Product Backlog                                 │  │  │
│  │  └───────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  4. SPRINT RETROSPECTIVE (스프린트 회고)                                 │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Timebox: 2주 스프린트 → 최대 1.5시간                              │  │  │
│  │  │                                                                   │  │  │
│  │  │  Format:                                                          │  │  │
│  │  │  ┌─────────────────────────────────────────────────────────────┐  │  │  │
│  │  │  │                What?           So What?        Now What?   │  │  │  │
│  │  │  │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐     │  │  │  │
│  │  │  │  │  잘 한  │   │  효과   │   │  의미   │   │  액션   │     │  │  │  │
│  │  │  │  │  것     │ → │  분석   │ → │  도출   │ → │  계획   │     │  │  │  │
│  │  │  │  └─────────┘   └─────────┘   └─────────┘   └─────────┘     │  │  │  │
│  │  │  │                                                                │  │  │  │
│  │  │  │  Start / Stop / Continue                                       │  │  │  │
│  │  │  │  Glad / Sad / Mad                                              │  │  │  │
│  │  │  │  4Ls (Liked, Learned, Lacked, Longed for)                      │  │  │  │
│  │  │  └─────────────────────────────────────────────────────────────┘  │  │  │
│  │  │                                                                   │  │  │
│  │  │  Output: Improvement Actions (최대 1-2개에 집중)                  │  │  │
│  │  └───────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 알고리즘: 스프린트 용량 계산

```python
"""
스프린트 용량(Capacity) 계산 및 계획 시스템
"""

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime, timedelta
from enum import Enum

class DayType(Enum):
    WORKDAY = "workday"
    WEEKEND = "weekend"
    HOLIDAY = "holiday"

@dataclass
class TeamMember:
    """팀원 정보"""
    name: str
    daily_capacity_hours: float = 6.0  # 실제 업무 가능 시간
    pto_days: int = 0                  # 휴가 일수
    is_part_time: bool = False
    focus_factor: float = 0.7          # 집중 계수 (회의, 컨텍스트 스위칭 고려)

    @property
    def effective_daily_capacity(self) -> float:
        """유효 일일 용량"""
        return self.daily_capacity_hours * self.focus_factor

@dataclass
class SprintCapacity:
    """스프린트 용량 분석 결과"""
    total_hours: float
    effective_hours: float
    available_story_points: int
    team_members: int
    avg_velocity: float
    recommendation: str

class SprintPlanner:
    """스프린트 계획 도구"""

    def __init__(self, team: List[TeamMember], sprint_days: int,
                 holidays: List[datetime] = None):
        self.team = team
        self.sprint_days = sprint_days
        self.holidays = holidays or []
        self.velocity_history: List[int] = []

    def calculate_capacity(self, sprint_start: datetime) -> SprintCapacity:
        """
        스프린트 용량 계산

        고려 요소:
        - 팀원별 가용 시간
        - 휴가(PTO)
        - 공휴일
        - 집중 계수 (Focus Factor)
        - 스크럼 이벤트 시간
        """
        # 실제 근무일 계산
        workdays = self._count_workdays(sprint_start)

        # 스크럼 이벤트 시간 차감 (스프린트당)
        scrum_events_hours = self._calculate_scrum_events_time()

        # 팀 전체 용량 계산
        total_hours = 0
        effective_hours = 0

        for member in self.team:
            member_workdays = workdays - member.pto_days
            member_total = member_workdays * member.daily_capacity_hours
            member_effective = member_workdays * member.effective_daily_capacity

            total_hours += member_total
            effective_hours += member_effective

        # 스크럼 이벤트 시간 차감
        effective_hours -= scrum_events_hours

        # 스토리 포인트 변환 (평균 속도 기반)
        if self.velocity_history:
            avg_velocity = sum(self.velocity_history) / len(self.velocity_history)
        else:
            # 초기 스프린트: 팀 규모 기반 추정
            avg_velocity = len(self.team) * self.sprint_days * 0.5

        # 예측 가능한 범위 제안
        recommended_sp = int(avg_velocity * 0.9)  # 90% 수용

        recommendation = self._generate_recommendation(
            effective_hours, recommended_sp, avg_velocity
        )

        return SprintCapacity(
            total_hours=total_hours,
            effective_hours=max(0, effective_hours),
            available_story_points=recommended_sp,
            team_members=len(self.team),
            avg_velocity=round(avg_velocity, 1),
            recommendation=recommendation
        )

    def _count_workdays(self, start_date: datetime) -> int:
        """근무일 계산 (주말, 공휴일 제외)"""
        workdays = 0
        current = start_date

        for _ in range(self.sprint_days):
            # 주말 체크
            if current.weekday() < 5:  # Mon=0, Fri=4
                # 공휴일 체크
                if current not in self.holidays:
                    workdays += 1
            current += timedelta(days=1)

        return workdays

    def _calculate_scrum_events_time(self) -> float:
        """스크럼 이벤트 소요 시간 계산"""
        # 2주 스프린트 기준
        sprint_planning = 4.0  # 시간
        daily_scrum = 0.25 * self.sprint_days  # 15분 x 일수
        sprint_review = 2.0  # 시간
        sprint_retrospective = 1.5  # 시간

        return sprint_planning + daily_scrum + sprint_review + sprint_retrospective

    def _generate_recommendation(self, effective_hours: float,
                                  recommended_sp: int,
                                  avg_velocity: float) -> str:
        """계획 권장사항 생성"""
        if effective_hours < avg_velocity * 4:  # 부족
            return (f"⚠️ 용량 부족: {recommended_sp}SP 권장. "
                   f"휴가자가 많아 범위 축소를 고려하세요.")
        elif effective_hours > avg_velocity * 8:  # 여유
            return (f"✅ 여유 있음: {recommended_sp + 5}SP까지 도전 가능. "
                   f"기술 부채나 혁신 아이디어를 포함하세요.")
        else:
            return f"✓ 적정 범위: {recommended_sp}SP 권장."

    def add_velocity(self, completed_points: int):
        """속도 이력 추가"""
        self.velocity_history.append(completed_points)
        # 최근 5개 스프린트만 유지
        if len(self.velocity_history) > 5:
            self.velocity_history.pop(0)

    def predict_completion(self, committed_points: int) -> Dict:
        """완료 확률 예측"""
        if not self.velocity_history:
            return {"confidence": "N/A", "message": "이력 부족"}

        avg = sum(self.velocity_history) / len(self.velocity_history)
        std_dev = (sum((x - avg) ** 2 for x in self.velocity_history)
                   / len(self.velocity_history)) ** 0.5

        # 정규분포 기반 확률 추정
        if std_dev == 0:
            confidence = 100 if committed_points <= avg else 50
        else:
            # z-score 계산
            z = (committed_points - avg) / std_dev
            # 간소화된 확률 계산
            if z <= -1:
                confidence = 85
            elif z <= 0:
                confidence = 70
            elif z <= 1:
                confidence = 50
            else:
                confidence = 30

        return {
            "committed": committed_points,
            "average_velocity": round(avg, 1),
            "std_deviation": round(std_dev, 1),
            "confidence": f"{confidence}%",
            "message": self._get_confidence_message(confidence)
        }

    def _get_confidence_message(self, confidence: int) -> str:
        if confidence >= 70:
            return "높은 확신도"
        elif confidence >= 50:
            return "보통 확신도 - 버퍼 필요"
        else:
            return "낮은 확신도 - 범위 재검토 필요"


# 실무 예시
if __name__ == "__main__":
    # 팀 구성
    team = [
        TeamMember(name="Alice", daily_capacity_hours=6, focus_factor=0.75),
        TeamMember(name="Bob", daily_capacity_hours=6, pto_days=2),
        TeamMember(name="Charlie", daily_capacity_hours=6, focus_factor=0.8),
        TeamMember(name="Diana", daily_capacity_hours=5, is_part_time=True),
        TeamMember(name="Eve", daily_capacity_hours=6),
    ]

    # 스프린트 계획
    planner = SprintPlanner(team, sprint_days=10)  # 2주

    # 속도 이력 설정
    planner.velocity_history = [32, 35, 30, 38, 33]

    # 용량 계산
    capacity = planner.calculate_capacity(datetime(2026, 3, 3))

    print("=== 스프린트 용량 분석 ===")
    print(f"팀 규모: {capacity.team_members}명")
    print(f"총 가용 시간: {capacity.total_hours}시간")
    print(f"유효 작업 시간: {capacity.effective_hours}시간")
    print(f"권장 스토리 포인트: {capacity.available_story_points}SP")
    print(f"평균 속도: {capacity.avg_velocity}SP")
    print(f"권장사항: {capacity.recommendation}")
    print()

    # 완료 예측
    prediction = planner.predict_completion(committed_points=35)
    print("=== 완료 예측 ===")
    for key, value in prediction.items():
        print(f"{key}: {value}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 스프린트 기간별 특성

| 비교 항목 | 1주 스프린트 | 2주 스프린트 | 3주 스프린트 | 4주 스프린트 |
|-----------|-------------|-------------|-------------|-------------|
| **피드백 빈도** | 매우 빠름 | 빠름 | 보통 | 느림 |
| **계획 오버헤드** | 높음 (20%) | 중간 (15%) | 낮음 (10%) | 낮음 (8%) |
| **적합 규모** | 소규모 팀 | 중규모 팀 | 대규모 팀 | 매우 큰 팀 |
| **변경 대응** | 즉시 | 빠름 | 보통 | 느림 |
| **린업 비용** | 높음 | 중간 | 낮음 | 낮음 |
| **추천 상황** | 스타트업, 연구 | 일반적 | 레거시 시스템 | 안정적 제품 |
| **CI/CD 요구도** | 매우 높음 | 높음 | 보통 | 낮음 |

### 과목 융합 관점 분석

#### 1. 프로젝트 관리 × 애자일 방법론 융합
스프린트는 전통적 프로젝트 관리의 WBS(Work Breakdown Structure)와 달리, 시간 중심(Time-boxed) 접근을 취한다. EVM(Earned Value Management)의 개념을 스크럼에 적용하면, 스프린트 완료율이 EV(Earned Value)가 되고, 계획된 속도가 PV(Planned Value)가 된다.

#### 2. 품질 관리 × CI/CD 융합
스프린트의 "완료(Definition of Done)"에는 CI/CD 파이프라인 통과가 포함된다. 모든 스토리는 단위 테스트, 정적 분석, 보안 스캔을 통과해야 '완료'로 간주된다. 이는 시프트 레프트(Shift-Left) 테스팅을 실현한다.

#### 3. 데이터베이스 × DevOps 융합
스프린트 내에서 데이터베이스 스키마 변경은 마이그레이션 스크립트로 관리된다. Flyway, Liquibase 등을 통해 데이터베이스 변경사항도 코드처럼 버전 관리되며, 스프린트 증분에 포함된다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단: 실무 시나리오 3가지

#### 시나리오 1: 스프린트 중간 범위 변경 요청
**상황**: 스프린트 5일차에 경영진이 긴급 기능 추가 요청

**기술사적 의사결정 과정**:
1. **원칙 확인**: 스프린트 목표(Sprint Goal)가 변경되는지 평가
2. **트레이드오프 분석**: 추가 시 기존 항목 제외 필요성 명시
3. **팀 협의**: 개발팀이 수용 가능한지 확인 (강제 금지)
4. **문서화**: 변경 사유와 영향을 ADR 형태로 기록
5. **예방**: 다음 스프린트 계획에 "긴급 슬롯" 예비

#### 시나리오 2: 스프린트 완료율 저하
**상황**: 최근 3회 연속 스프린트 완료율 60% 미달

**기술사적 의사결정 과정**:
1. **근본 원인 분석**: 5-Why 기법으로 원인 파악
2. **데이터 검토**: 번다운 차트 패턴 분석
3. **용량 재산정**: 실제 가용 용량 대비 과다 계획 여부
4. **DoD 완화 검토**: 품질 기준이 과도한지 평가
5. **개선 액션**: 회고에서 구체적 개선안 도출

#### 시나리오 3: 분산 팀의 스프린트 동기화
**상황**: 서울-미국 팀이 하나의 스프린트 수행, 시차 문제

**기술사적 의사결정 과정**:
1. **오버랩 시간 확보**: 최소 2시간 공통 업무 시간 설정
2. **비동기 커뮤니케이션**: 스탠드업을 채팅+비디오 혼합
3. **핸드오프 프로세스**: 일일 인계 문서 템플릿 활용
4. **롤링 스프린트**: 팀별 1일 오프셋으로 자연스러운 인계

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] CI/CD 파이프라인 준비도 (자동화 수준)
- [ ] 테스트 자동화 커버리지 (70% 이상 권장)
- [ ] 피처 플래그(Feature Flag) 도구 준비
- [ ] 모니터링/알림 시스템 구축

#### 운영/보안적 고려사항
- [ ] 스프린트 길이 조직 표준화 (일관성)
- [ ] 스프린트 취소 기준 및 프로세스
- [ ] 보안 스캔을 DoD에 포함
- [ ] 장애 대응을 위한 온콜(On-call) 로테이션

### 주의사항 및 안티패턴

1. **Sprint Stuffing**: 과도한 항목 추가로 실패 예정된 스프린트
2. **Mini-Waterfall**: 스프린트 내에서 분석-설계-개발-테스트 순차 수행
3. **Sprint Interrupt**: 스프린트 중간 지속적 범위 변경
4. **Gold Plating**: 스프린트 목표 초과 작업으로 인한 범위 확장

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 도입 전 | 도입 후 | 개선율 |
|------|---------|---------|--------|
| 평균 배포 주기 | 6개월 | 2주 | **92% 단축** |
| 요구사항 변경 비용 | $100K/건 | $30K/건 | **70% 절감** |
| 스프린트 완료율 | N/A | 85%+ | 신규 도입 |
| 팀 예측 가능성 | 40% | 80% | **100% 향상** |
| 고객 만족도 | 65 | 85 | **31% 향상** |

### 미래 전망 및 진화 방향

1. **AI 기반 스프린트 계획**: 과거 데이터 기반 최적 범위 자동 추천
2. **컨티뉴어스 스프린트**: 스프린트 경계 없는 지속적 흐름(Flow)
3. **하이퍼 단축 스프린트**: 1일 단위의 초단기 피드백 루프
4. **예측적 완료**: 머신러닝 기반 스프린트 성공 확률 예측

### ※ 참고 표준/가이드
- **Scrum Guide 2020**: 스프린트의 공식 정의
- **Nexus Guide**: 대규모 스크럼의 스프린트 관리
- **SAFe Iteration**: SAFe의 스프린트 확장 모델
- **LeSS Sprint**: Large-Scale Scrum의 스프린트 구조

---

## 📌 관련 개념 맵 (Knowledge Graph)

1. [스크럼 프레임워크](./62_scrum_framework.md) - 스프린트가 속한 애자일 프레임워크
2. [제품 백로그](./66_product_backlog.md) - 스프린트 백로그의 원천
3. [스프린트 계획](./68_sprint_planning.md) - 스프린트 시작 이벤트
4. [데일리 스크럼](./69_daily_scrum.md) - 스프린트 내 일일 동기화 이벤트
5. [스프린트 리뷰](./70_sprint_review.md) - 스프린트 종료 검증 이벤트
6. [스프린트 회고](./71_sprint_retrospective.md) - 스프린트 프로세스 개선 이벤트

---

## 👶 어린이를 위한 3줄 비유 설명

**비유: 독서 클럽 모임**

1. **정해진 시간 동안 읽어요**: "이번 주에는 50쪽까지 읽어오자!"라고 정하고, 그 기간 동안 열심히 책을 읽어요. 중간에 다른 책으로 바꾸면 안 돼요.

2. **매일 조금씩 나눠서 읽어요**: 하루에 한 번 친구들과 "어디까지 읽었어?" 하고 이야기해요. 어려운 단어가 나오면 서로 도와줘요.

3. **다 읽으면 이야기해요**: 50쪽을 다 읽으면 친구들에게 어떤 내용이었는지 이야기해요. 재미있었는지, 어려웠는지 말하고, 다음엔 어떻게 읽을지 계획해요.
