+++
title = "스프린트 회고 (Sprint Retrospective)"
date = 2024-05-24
description = "팀의 프로세스, 관계, 도구를 검토하고 개선하여 다음 스프린트의 효율성을 높이는 스크럼 이벤트"
weight = 71
+++

# 스프린트 회고 (Sprint Retrospective)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스프린트 회고는 **팀이 지난 스프린트 동안의 협업 방식, 프로세스, 도구를 검사(Inspection)**하고, **구체적인 개선 액션을 도출**하여 다음 스프린트에 적용하는 스크럼의 적응(Adaptation) 이벤트입니다.
> 2. **가치**: 정기적 회고는 **팀 생산성 25% 향상, 결함률 30% 감소, 팀 만족도 35% 증가** 효과가 있으며, "지속적 개선(Kaizen)"을 실천하는 핵심 메커니즘입니다.
> 3. **융합**: 데브옵스의 블릿포스트(Post-mortem), 사이트 신뢰성 엔지니어링(SRE)의 장애 회고와 결합하여 **조직 학습 조직(Learning Organization)** 구축에 기여합니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**스프린트 회고(Sprint Retrospective)**는 스크럼 가이드(2020)에 따르면 "스프린트 동안 **어떤 것이 잘 되었고, 어떤 문제가 발생했으며, 그 문제가 어떻게 해결되었는지(또는 해결되지 않았는지)** 검사하는 기회"입니다. 이는 제품이 아닌 **프로세스와 팀 역학에 초점**을 맞춥니다.

```
[스프린트 회고의 3가지 핵심 질문]

1. 잘 한 것 (What Went Well)
   - 이번 스프린트에서 성공한 것은?
   - 계속 유지해야 할 것은?

2. 개선할 것 (What Could Be Improved)
   - 어떤 문제가 있었나?
   - 무엇이 방해가 되었나?

3. 다음에 할 것 (What Will We Commit To)
   - 다음 스프린트에서 무엇을 바꿀 것인가?
   - 구체적인 액션 아이템은?

[Scrum Guide 2020의 목적]
스프린트 회고는 다음 스프린트에서 더 효과적일 수 있도록
품질과 효율성을 검사하고 적응할 기회를 제공합니다.
```

**스프린트 리뷰 vs 스프린트 회고**:

| 구분 | 스프린트 리뷰 | 스프린트 회고 |
| :--- | :--- | :--- |
| **초점** | 제품(Product) | 프로세스(Process) |
| **참석자** | 팀 + 이해관계자 | 스크럼 팀만 (안전한 공간) |
| **질문** | "무엇을 만들었나?" | "어떻게 일했나?" |
| **산출물** | 갱신된 제품 백로그 | 개선 액션 아이템 |
| **비공개성** | 공개 | 비공개 |

### 💡 일상생활 비유: 스포츠 팀의 경기 후 분석

```
[스프린트 회고 = 스포츠 팀의 경기 분석]

축구 팀                        스크럼 팀
========                      =========
경기                          스프린트
선수                          팀원
감독                          스크럼 마스터
경기 결과                      제품 증분

시나리오:
1. 경기 종료                  1. 스프린트 종료
2. 관중(이해관계자)과 하이파이브  2. 이해관계자와 리뷰
3. 락커룸으로 이동 (비공개)      3. 회고 장소로 이동
4. 경기 분석                   4. 스프린트 회고
   "전반전에 수비가 약했어"        "코드 리뷰가 늦었어"
   "패스 성공률이 좋았어"          "페어 프로그래밍이 효과적이었어"
5. 다음 경기 전략 수립         5. 다음 스프린트 개선안
   "수비 조직 강화하자"           "리뷰 SLA를 정하자"

핵심: 팬(이해관계자) 앞에서는 하지 않는,
      팀만의 솔직한 대화가 필요하다!
```

### 2. 등장 배경 및 발전 과정

#### 1) 1980년대: 사후 검토(Post-Mortem)
전통적 프로젝트 관리에서는 프로젝트 종료 후 **"교훈 보고서(Lessons Learned)"**를 작성했습니다. 그러나 이는 **너무 늦은 피드백**이었습니다.

#### 2) 1995년: 스크럼의 등장
Jeff Sutherland와 Ken Schwaber가 스크럼을 정립하면서 **매 스프린트마다 회고**하는 것을 표준화했습니다.

#### 3) 2001년: 애자일 원칙
> "일정한 주기로 팀은 어떻게 더 효과적이 될지 숙고하고, 그에 따라 행동을 조정한다." - 애자일 12원칙 중 제12원칙

#### 4) 현대적 발전
- **다양한 회고 기법**: Keep/Drop/Start, 4Ls, Sailboat 등
- **원격 회고**: 온라인 협업 도구(Miro, Retrium)
- **데이터 기반 회고**: 메트릭 활용

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 스프린트 회고 구성 요소

| 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기법 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **참석자** | 회고 수행 주체 | 스크럼 팀만 (심리적 안전) | 팀 빌딩 | 락커룸 대화 |
| **시간 상자** | 시간 제한 | 스프린트 2주면 최대 3시간 | 타임박싱 | 경기 분석 시간 |
| **진행자** | 회고 촉진 | 스크럼 마스터 또는 외부 | 파실리테이션 | 감독 |
| **아이템 수집** | 의견 수렴 | 포스트잇, 온라인 보드 | 브레인스토밍 | 전술 보드 |
| **액션 아이템** | 개선 과제 | SMART 기준, 담당자 지정 | Task Board | 훈련 계획 |

### 2. 회고 진행 프로세스 (5단계 프레임워크)

```text
================================================================================
|                    SPRINT RETROSPECTIVE 5-PHASE FRAMEWORK                    |
================================================================================

                    Esther Derby & Diana Larsen (Agile Retrospectives)

Phase 1: 개회 (Opening)
┌─────────────────────────────────────────────────────────────────────────┐
│ 목적: 안전한 분위기 조성, 목표 설정                                        │
│ 활동:                                                                    │
│   • 참석자 체크인 (Check-in)                                             │
│   • 회고 규칙 리뷰                                                        │
│   • "지금 우리는 어떤 기분인가?"                                          │
│ 시간: 5~10분                                                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
Phase 2: 데이터 수집 (Gather Data)
┌─────────────────────────────────────────────────────────────────────────┐
│ 목적: 객관적/주관적 사실 수집                                              │
│ 활동:                                                                    │
│   • 타임라인 작성 (주요 이벤트)                                           │
│   • "감정 그래프" (기분 변화)                                             │
│   • 메트릭 검토 (벨로시티, 버그 수)                                        │
│ 시간: 20~30분                                                             │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────┐     │
│   │  스프린트 타임라인                                             │     │
│   │  ============                                                 │     │
│   │  Day1    Day3    Day5    Day7    Day9                         │     │
│   │  시작    결함    기능    데모    완료                          │     │
│   │   😊      😟      😊      😐      🎉                          │     │
│   └──────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
Phase 3: 통찰 생성 (Generate Insights)
┌─────────────────────────────────────────────────────────────────────────┐
│ 목적: "왜" 그런 일이 일어났는지 분석                                        │
│ 활동:                                                                    │
│   • 5 Whys (근본 원인 분석)                                               │
│   • 패턴 찾기 (공통점 식별)                                               │
│   • 그룹핑 (유사 항목 묶기)                                               │
│ 시간: 30~45분                                                             │
│                                                                          │
│   예시: 5 Whys                                                           │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ 문제: 기능이 스프린트에 완료되지 않음                           │   │
│   │ Why 1: 개발 시간이 부족했다                                     │   │
│   │ Why 2: 예상보다 복잡했다                                        │   │
│   │ Why 3: 기술 부채가 많았다                                       │   │
│   │ Why 4: 코드 리뷰가 늦었다                                       │   │
│   │ Why 5: 리뷰어가 부족하다 (근본 원인)                            │   │
│   └────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
Phase 4: 결정 도출 (Decide What To Do)
┌─────────────────────────────────────────────────────────────────────────┐
│ 목적: 실행 가능한 개선 아이템 선정                                         │
│ 활동:                                                                    │
│   • 우선순위 투표 (Dot Voting)                                           │
│   • SMART 목표 설정                                                       │
│   • 담당자 지정                                                           │
│ 시간: 30~45분                                                             │
│                                                                          │
│   액션 아이템 예시:                                                       │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ 액션: 매일 오전 10시 코드 리뷰 세션 진행                        │   │
│   │ 담당: 김철수                                                    │   │
│   │ 기한: 다음 스프린트 Day 1부터                                    │   │
│   │ 성공 기준: 리뷰 대기 시간 < 4시간                                │   │
│   └────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
Phase 5: 폐회 (Closing)
┌─────────────────────────────────────────────────────────────────────────┐
│ 목적: 회고 마무리, 다음 단계 확인                                          │
│ 활동:                                                                    │
│   • 액션 아이템 요약                                                      │
│   • ROT(Return On Time) 평가                                             │
│   • 체크아웃 (감정 마무리)                                                │
│ 시간: 5~10분                                                              │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3. 다양한 회고 기법

```text
================================================================================
|                    RETROSPECTIVE TECHNIQUES                                  |
================================================================================

1. Keep / Drop / Start (가장 기본)
   ┌─────────────────────────────────────────────────────────────────────┐
   │ KEEP (유지)        │ DROP (중단)        │ START (시작)              │
   │ 계속할 것          │ 그만할 것          │ 새로 시작할 것            │
   │ ──────────────     │ ──────────────     │ ──────────────            │
   │ • 데일리 스탠드업   │ • 긴 회의          │ • 페어 프로그래밍         │
   │ • 자동화 테스트    │ • 수동 배포        │ • 기술 세션               │
   └─────────────────────────────────────────────────────────────────────┘

2. 4Ls (Liked, Learned, Lacked, Longed For)
   ┌─────────────────────────────────────────────────────────────────────┐
   │ LIKED (좋았던 것)  │ LEARNED (배운 것)  │ LACKED (부족한 것)        │
   │ 좋았던 점          │ 새로 알게 된 것    │ 없어서 아쉬운 것          │
   │ ──────────────     │ ──────────────     │ ──────────────            │
   │ • 협업이 원활      │ • 새로운 프레임워크│ • 문서화                  │
   │                   │                   │                           │
   │ LONGED FOR (바라는 것)                                              │
   │ 더 있었으면 하는 것                                                  │
   │ ──────────────                                                      │
   │ • 더 많은 테스트 시간                                                │
   └─────────────────────────────────────────────────────────────────────┘

3. Sailboat (범선 기법)
   ┌─────────────────────────────────────────────────────────────────────┐
   │                                                                     │
   │                        🌬️ 바람 (가속 요소)                           │
   │                     우리를 앞으로 밀어주는 것                         │
   │                                                                     │
   │                           ⛵ 범선 (팀)                               │
   │                                                                     │
   │                         🪨 암초 (위험)                               │
   │                      조심해야 할 장애물                              │
   │                                                                     │
   │                        ⚓ 닻 (방해 요소)                              │
   │                      우리를 늦추는 것                               │
   │                                                                     │
   │                         🏝️ 섬 (목표)                                 │
   │                       향하고 있는 곳                                 │
   └─────────────────────────────────────────────────────────────────────┘

4. Starfish (해서 별)
   ┌─────────────────────────────────────────────────────────────────────┐
   │                                                                     │
   │              KEEP (계속)                                             │
   │                 │                                                    │
   │                 │                                                    │
   │    LESS --------┼-------- MORE                                       │
   │   (줄이기)       │       (늘리기)                                    │
   │                 │                                                    │
   │                 │                                                    │
   │              START (시작)                                            │
   │                                                                     │
   │              STOP (중단)                                             │
   └─────────────────────────────────────────────────────────────────────┘

5. Mad / Sad / Glad (감정 중심)
   ┌─────────────────────────────────────────────────────────────────────┐
   │ 😡 MAD (화남)      │ 😢 SAD (슬픔)     │ 😊 GLAD (기쁨)            │
   │ 불만스러운 것      │ 아쉬운 것         │ 만족스러운 것              │
   │ ──────────────     │ ──────────────     │ ──────────────            │
   │ • 잦은 요구사항 변경│ • 기능 취소       │ • 팀워크                   │
   │ • 늦은 피드백      │ • 일정 지연       │ • 성공적 출시              │
   └─────────────────────────────────────────────────────────────────────┘
```

### 4. 회고 관리 시스템 구현

```python
"""
스프린트 회고 관리 시스템
회고 아이템 수집, 분석, 액션 아이템 추적
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timedelta

class ItemType(Enum):
    """회고 아이템 유형"""
    WENT_WELL = "well"           # 잘 된 것
    NEEDS_IMPROVEMENT = "improve" # 개선 필요
    ACTION_ITEM = "action"        # 액션 아이템
    QUESTION = "question"         # 질문

class ActionStatus(Enum):
    """액션 아이템 상태"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

@dataclass
class RetroItem:
    """회고 아이템"""
    id: str
    sprint_number: int
    item_type: ItemType
    content: str
    author: str
    votes: int = 0
    category: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class ActionItem:
    """액션 아이템 (개선 과제)"""
    id: str
    sprint_number: int          # 생성된 스프린트
    description: str            # SMART 형식
    owner: str                  # 담당자
    due_date: datetime          # 기한
    status: ActionStatus = ActionStatus.TODO
    success_criteria: str = ""  # 성공 기준
    related_retro_item: Optional[str] = None
    completed_at: Optional[datetime] = None

@dataclass
class Retrospective:
    """스프린트 회고"""
    sprint_number: int
    date: datetime
    participants: List[str]
    items: List[RetroItem] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)
    duration_minutes: int = 90
    facilitator: str = ""
    notes: str = ""

class RetrospectiveManager:
    """회고 관리자"""

    def __init__(self):
        self.retrospectives: Dict[int, Retrospective] = {}
        self.action_items: Dict[str, ActionItem] = {}
        self.item_counter = 1
        self.action_counter = 1

    def create_retrospective(self, sprint_number: int,
                            participants: List[str],
                            facilitator: str) -> Retrospective:
        """회고 생성"""
        retro = Retrospective(
            sprint_number=sprint_number,
            date=datetime.now(),
            participants=participants,
            facilitator=facilitator
        )
        self.retrospectives[sprint_number] = retro
        return retro

    def add_item(self, sprint_number: int, item_type: ItemType,
                content: str, author: str) -> RetroItem:
        """회고 아이템 추가"""
        item_id = f"RI-{self.item_counter:04d}"
        self.item_counter += 1

        item = RetroItem(
            id=item_id,
            sprint_number=sprint_number,
            item_type=item_type,
            content=content,
            author=author
        )

        if sprint_number in self.retrospectives:
            self.retrospectives[sprint_number].items.append(item)

        return item

    def vote_item(self, item_id: str) -> int:
        """아이템 투표"""
        for retro in self.retrospectives.values():
            for item in retro.items:
                if item.id == item_id:
                    item.votes += 1
                    return item.votes
        return -1

    def create_action_item(self, sprint_number: int, description: str,
                          owner: str, due_date: datetime,
                          success_criteria: str = "",
                          related_item: str = "") -> ActionItem:
        """액션 아이템 생성"""
        action_id = f"ACT-{self.action_counter:04d}"
        self.action_counter += 1

        action = ActionItem(
            id=action_id,
            sprint_number=sprint_number,
            description=description,
            owner=owner,
            due_date=due_date,
            success_criteria=success_criteria,
            related_retro_item=related_item
        )

        self.action_items[action_id] = action
        if sprint_number in self.retrospectives:
            self.retrospectives[sprint_number].action_items.append(action)

        return action

    def update_action_status(self, action_id: str,
                            status: ActionStatus) -> bool:
        """액션 아이템 상태 업데이트"""
        if action_id in self.action_items:
            self.action_items[action_id].status = status
            if status == ActionStatus.DONE:
                self.action_items[action_id].completed_at = datetime.now()
            return True
        return False

    def get_action_completion_rate(self, sprint_number: int) -> float:
        """액션 아이템 완료율"""
        actions = [a for a in self.action_items.values()
                  if a.sprint_number == sprint_number]
        if not actions:
            return 0
        completed = sum(1 for a in actions if a.status == ActionStatus.DONE)
        return (completed / len(actions)) * 100

    def get_overdue_actions(self) -> List[ActionItem]:
        """기한 초과 액션 아이템"""
        now = datetime.now()
        return [a for a in self.action_items.values()
                if a.due_date < now and a.status not in
                [ActionStatus.DONE, ActionStatus.CANCELLED]]

    def analyze_trends(self) -> Dict:
        """트렌드 분석 (반복되는 문제 식별)"""
        all_items = []
        for retro in self.retrospectives.values():
            all_items.extend(retro.items)

        # 카테고리별 빈도
        category_counts = {}
        for item in all_items:
            if item.category:
                category_counts[item.category] = \
                    category_counts.get(item.category, 0) + 1

        # 가장 많이 언급된 문제
        improvement_items = [i for i in all_items
                           if i.item_type == ItemType.NEEDS_IMPROVEMENT]
        top_issues = sorted(improvement_items, key=lambda x: x.votes,
                          reverse=True)[:5]

        return {
            "total_retrospectives": len(self.retrospectives),
            "total_items": len(all_items),
            "category_distribution": category_counts,
            "top_issues": [{"content": i.content, "votes": i.votes}
                          for i in top_issues],
            "action_completion_rate": self._calculate_overall_completion()
        }

    def _calculate_overall_completion(self) -> float:
        """전체 액션 완료율"""
        if not self.action_items:
            return 0
        completed = sum(1 for a in self.action_items.values()
                       if a.status == ActionStatus.DONE)
        return (completed / len(self.action_items)) * 100

    def generate_retro_report(self, sprint_number: int) -> str:
        """회고 보고서 생성"""
        retro = self.retrospectives.get(sprint_number)
        if not retro:
            return "회고 데이터가 없습니다."

        report = f"""
================================================================================
                    SPRINT {sprint_number} RETROSPECTIVE REPORT
================================================================================

[기본 정보]
- 일시: {retro.date.strftime('%Y-%m-%d %H:%M')}
- 참석자: {', '.join(retro.participants)} ({len(retro.participants)}명)
- 진행자: {retro.facilitator}
- 소요 시간: {retro.duration_minutes}분

[아이템 현황]
- 잘 된 것: {sum(1 for i in retro.items if i.item_type == ItemType.WENT_WELL)}개
- 개선 필요: {sum(1 for i in retro.items if i.item_type == ItemType.NEEDS_IMPROVEMENT)}개
- 액션 아이템: {len(retro.action_items)}개

[투표 상위 항목]
"""
        top_voted = sorted([i for i in retro.items
                          if i.item_type == ItemType.NEEDS_IMPROVEMENT],
                         key=lambda x: x.votes, reverse=True)[:3]
        for item in top_voted:
            report += f"  • {item.content} ({item.votes}표)\n"

        report += "\n[액션 아이템]\n"
        for action in retro.action_items:
            status_emoji = "✅" if action.status == ActionStatus.DONE else "⏳"
            report += f"  {status_emoji} {action.description}\n"
            report += f"     담당: {action.owner} | 기한: {action.due_date.strftime('%m/%d')}\n"

        return report


# 사용 예시
if __name__ == "__main__":
    manager = RetrospectiveManager()

    # 회고 생성
    retro = manager.create_retrospective(
        sprint_number=5,
        participants=["김철수", "이영희", "박개발"],
        facilitator="스크럼마스터"
    )

    # 아이템 추가
    manager.add_item(5, ItemType.WENT_WELL,
                    "페어 프로그래밍으로 결함 감소", "김철수")
    manager.add_item(5, ItemType.NEEDS_IMPROVEMENT,
                    "코드 리뷰 대기 시간이 김", "이영희")

    # 액션 아이템 생성
    manager.create_action_item(
        sprint_number=5,
        description="매일 오전 10시 리뷰 세션 진행",
        owner="박개발",
        due_date=datetime.now() + timedelta(days=14),
        success_criteria="리뷰 대기 시간 < 4시간"
    )

    # 보고서 생성
    print(manager.generate_retro_report(5))
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 개선 활동 비교

| 비교 항목 | 스프린트 회고 | 포스트모템 | 5 Whys | Kaizen |
| :--- | :--- | :--- | :--- | :--- |
| **주기** | 매 스프린트 | 장애/사고 후 | 문제 발생 시 | 지속적 |
| **초점** | 프로세스 전반 | 특정 사건 | 근본 원인 | 작은 개선 |
| **참여자** | 팀 전체 | 관계자 전체 | 분석가+관계자 | 전사 |
| **분위기** | 건설적 | 분석적 | 분석적 | 개선적 |
| **산출물** | 액션 아이템 | 보고서 | 원인 분석 | 개선 제안 |

### 2. 과목 융합 관점 분석

#### 스프린트 회고 + 품질 관리

```
[회고 기반 품질 개선 루프]

PDCA 사이클과 회고 연계:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Plan ──────> Do ──────> Check ──────> Act                │
│     │           │           │            │                  │
│     │           │           │            │                  │
│   스프린트     스프린트     회고       액션                  │
│   계획        수행        분석       실행                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

품질 메트릭과 회고 연계:
- 결함 밀도 추세 → 회고에서 원인 분석
- 벨로시티 변동 → 프로세스 문제 식별
- 팀 만족도 → 팀 역학 개선
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단

**[시나리오] 회고에서 나온 액션 아이템이 지속되지 않는 문제**

**기술사적 판단**:
```
근본 원인:
1. 액션 아이템이 너무 많음 (과용)
2. 담당자 불명확
3. 추적 메커니즘 부재
4. 경영진 관심 부족

해결 전략:

1. 액션 아이템 수 제한
   - 스프린트당 최대 3개
   - "Less is More" 원칙

2. 다음 스프린트 백로그에 포함
   - 액션 아이템을 사용자 스토리로 변환
   - 우선순위 부여

3. 가시화
   - 팀 보드에 액션 아이템 섹션
   - 매일 데일리 스탠드업에서 진행 확인

4. 스크럼 마스터 역할 강화
   - 액션 아이템 추적 책임
   - 완료 시 팀에 공유

5. 성공 축하
   - 완료된 액션 아이템 축하
   - 개선 효과 정량화
```

### 2. 주의사항 및 안티패턴

| 안티패턴 | 증상 | 해결 방안 |
| :--- | :--- | :--- |
| **비난 대회** | 특정 인물 비난 | "나" 메시지, 사실 중심 |
| **액션 과용** | 수십 개 액션 | 최대 3개 제한 |
| **반복 문제** | 같은 이슈 반등 | 근본 원인 분석 |
| **침묵** | 일부만 발언 | 라운드 로빈, 익명 투표 |
| **형식적 진행** | 시간 때우기 | 다양한 기법 사용 |

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | 적용 전 | 적용 후 | 개선 효과 |
| :--- | :--- | :--- | :--- | :--- |
| **생산성** | 벨로시티 | 30 SP | 38 SP | +27% |
| **품질** | 결함 수 | 15개/스프린트 | 10개 | -33% |
| **팀 만족** | 만족도 | 3.2/5 | 4.3/5 | +34% |
| **액션 완료** | 완료율 | 20% | 85% | +65%p |

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [스프린트 리뷰](@/studynotes/4_software_engineering/2_agile/70_sprint_review.md) : 제품 검사
- [스크럼 마스터](@/studynotes/4_software_engineering/2_agile/64_scrum_master.md) : 회고 진행자
- [팀 토폴로지](@/studynotes/4_software_engineering/9_cloud_native/531_cloud_native.md) : 팀 역학
- [지속적 개선](@/studynotes/4_software_engineering/1_sdlc/cmmi.md) : Kaizen
- [데브옵스](@/studynotes/4_software_engineering/2_agile/97_devops.md) : 블릿포스트

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 친구들과 함께 숙제를 했는데, 다음에도 똑같이 어려움을 겪으면 힘들어요!

2. **해결(회고)**: 숙제가 끝나고 친구들과 모여서 이야기해요. "이번에 뭐가 어려웠어?", "다음엔 어떻게 하면 더 잘할 수 있을까?" 그리고 다음에 시도해 볼 것을 정해요.

3. **효과**: 매번 조금씩 더 잘하게 돼요! "지난번에 정하기로 한 대로 역할을 나눠서 하니까 훨씬 빨랐어!"라며 발전하는 걸 느껴요. 마치 운동선수가 경기 후 비디오를 보며 분석하는 것과 같아요!
