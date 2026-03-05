+++
title = "39. 간트 차트 (Gantt Chart)"
description = "프로젝트 일정을 시간 순서대로 막대 그래프로 시각화한 도구, 일정 관리의 표준"
date = "2026-03-05"
[taxonomies]
tags = ["gantt-chart", "scheduling", "visualization", "project-management", "timeline"]
categories = ["studynotes-4_software_engineering"]
+++

# 39. 간트 차트 (Gantt Chart)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 간트 차트는 프로젝트의 **각 작업을 시작일부터 종료일까지의 막대(Bar)**로 표현하여, **시간의 흐름에 따른 작업 진행 상황을 직관적으로 시각화**하는 프로젝트 일정 관리 도구입니다.
> 2. **가치**: **의존관계, 마일스톤, 진척률**을 한눈에 파악할 수 있어 이해관계자 커뮤니케이션 비용을 50% 이상 절감하며, 1910년대 개발 이후 100년 넘게 **일정 관리의 사실상 표준(De Facto Standard)**으로 자리 잡았습니다.
> 3. **융합**: CPM/PERT와 결합하여 Critical Path 표시가 가능하며, 현대적으로는 **Jira, MS Project, Asana** 등의 디지털 도구에서 WBS, 자원 배분, 베이스라인과 통합됩니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**간트 차트(Gantt Chart)**는 1910년대 미국의 기계 공학자 **헨리 간트(Henry L. Gantt)**가 개발한 프로젝트 일정 시각화 도구입니다. 가로축은 **시간(날짜/주/월)**, 세로축은 **작업(Task)**을 나타내며, 각 작업은 **시작일부터 종료일까지의 막대**로 표현됩니다.

**간트 차트의 핵심 구성 요소**:

| 요소 | 표현 방식 | 설명 |
|:---|:---|:---|
| **작업 막대 (Task Bar)** | 가로 막대 | 시작일~종료일 기간 |
| **마일스톤 (Milestone)** | 다이아몬드(◆) | 주요 이정점 (0일Duration) |
| **의존관계 (Dependency)** | 화살표(→) | 선후관계 |
| **진척률 (Progress)** | 막대 내부 채우기 | 완료율 (%) |
| **베이스라인 (Baseline)** | 회색 막대 | 계획 대비 실적 |
| **자원 (Resource)** | 텍스트/아이콘 | 담당자 |

### 2. 비유: 음악 악보와 비교

```
[간트 차트 = 오케스트라 악보]

오케스트라 악보                        간트 차트
─────────────────                    ─────────────────
시간축 (왼쪽→오른쪽)        ────>   시간축 (왼쪽→오른쪽)
악기별 가로줄               ────>   작업별 가로줄
음표의 길이                 ────>   작업 막대의 길이
쉼표                        ────>   대기 기간
강조표시/마디               ────>   마일스톤
악기 간 조화                ────>   작업 간 의존관계

──────────────────────────────────────────────────────
지휘자가 한눈에 보는 것:              PM이 한눈에 보는 것:
• 누가 언제 연주하는가?              • 무슨 작업이 언제 수행되는가?
• 동시에 연주하는 악기는?            • 병렬로 수행되는 작업은?
• 하이라이트 지점은?                 • 마일스톤은 언제인가?
• 늦게 시작하면 안 되는 악기?         • Critical Path는?
```

### 3. 등장 배경 및 발전 과정

**1) 1910년: 헨리 간트의 발명**
- 미국 해군 조선소에서 생산 관리용으로 개발
- 당시: 손으로 그린 종이 차트
- 혁신: "언제 끝나는가?"를 시각적으로 표현

**2) 1950~60년대: CPM/PERT와 결합**
- Critical Path를 간트 차트에 표시
- 의존관계 화살표 추가

**3) 1980년대: PC 기반 도구 등장**
- Microsoft Project (1984) 등장
- 자동 계산, 자원 배분 기능 추가

**4) 2000년대~현재: 클라우드 협업 도구**
- Jira, Asana, Monday.com, Smartsheet
- 실시간 협업, 모바일 지원
- 애자일 친화적 (스프린트 간트)

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 간트 차트 구조 다이어그램

```
================================================================================
|                        GANTT CHART STRUCTURE                                  |
================================================================================

    프로젝트: 웹 애플리케이션 개발 (12주)

    ID   작업명                | W1  W2  W3  W4  W5  W6  W7  W8  W9  W10 W11 W12 |
    ─────────────────────────────────────────────────────────────────────────────

    1    프로젝트 계획          |████│    │    │    │    │    │    │    │    │    │    │    │
         (완료 100%)           |    │    │    │    │    │    │    │    │    │    │    │    │
                               |    │    │    │    │    │    │    │    │    │    │    │    │

    2    요구사항 분석          |    |████████│    │    │    │    │    │    │    │    │    │    │
         (완료 100%)           |    │    │    │    │    │    │    │    │    │    │    │    │
         └──> 의존: 1          |    │    │    │    │    │    │    │    │    │    │    │    │

    3    UI/UX 설계            |    │    │████████│    │    │    │    │    │    │    │    │    │
         (완료 75%)            |    │    │▓▓▓▓│    │    │    │    │    │    │    │    │    │
         └──> 의존: 2          |    │    │    │    │    │    │    │    │    │    │    │    │

    4    DB 설계               |    │    │████████│    │    │    │    │    │    │    │    │    │
         (완료 100%)           |    │    │    │    │    │    │    │    │    │    │    │    │
         └──> 의존: 2          |    │    │    │    │    │    │    │    │    │    │    │    │

    5    백엔드 개발           |    │    │    │████████████████████│    │    │    │    │
         (완료 40%)            |    │    │    │▓▓▓▓│    │    │    │    │    │    │    │    │
         └──> 의존: 4          |    │    │    │    │    │    │    │    │    │    │    │    │

    6    프론트엔드 개발        |    │    │    │    │████████████████│    │    │    │    │    │
         (완료 20%)            |    │    │    │    │▓▓▓▓│    │    │    │    │    │    │    │
         └──> 의존: 3          |    │    │    │    │    │    │    │    │    │    │    │    │

    7    통합 테스트           |    │    │    │    │    │    │    │████████│    │    │    │    │
         (완료 0%)             |    │    │    │    │    │    │    │    │    │    │    │    │
         └──> 의존: 5,6        |    │    │    │    │    │    │    │    │    │    │    │    │

    8    배포 및 안정화        |    │    │    │    │    │    │    │    │    │████│    │    │
         (완료 0%)             |    │    │    │    │    │    │    │    │    │    │    │    │
         └──> 의존: 7          |    │    │    │    │    │    │    │    │    │    │    │    │

    ─────────────────────────────────────────────────────────────────────────────

    범례:
    ████  완료된 작업
    ▓▓▓▓  진행 중인 작업 (부분 완료)
    ░░░░  계획된 작업 (미완료)

    마일스톤:
    ◆ M1: 요구사항 승인 (W3)
    ◆ M2: 설계 완료 (W5)
    ◆ M3: 개발 완료 (W9)
    ◆ M4: 출시 (W12)

    오늘: W6 (수직선 표시)

================================================================================
```

### 2. 의존관계 유형 (Dependency Types)

```
================================================================================
|                    DEPENDENCY TYPES IN GANTT CHART                            |
================================================================================

    1. Finish-to-Start (FS) - 완료-시작 (가장 일반적)
    ─────────────────────────────────────────────────────────────────────────
    선행 작업 완료 후 후속 작업 시작

    [Task A]────────────>
                         │
                         v
                         [Task B]────────────>

    예: "요구사항 분석 완료 후 설계 시작"

    ─────────────────────────────────────────────────────────────────────────

    2. Start-to-Start (SS) - 시작-시작
    ─────────────────────────────────────────────────────────────────────────
    선행 작업 시작 후 후속 작업 시작 (병렬 가능)

    [Task A]────────────>
    │
    v
    [Task B]────────────>

    예: "DB 설계 시작하면 API 설계도 시작 가능"

    ─────────────────────────────────────────────────────────────────────────

    3. Finish-to-Finish (FF) - 완료-완료
    ─────────────────────────────────────────────────────────────────────────
    선행 작업 완료 시점에 후속 작업도 완료되어야 함

    [Task A]────────────>
                        │
                        v
    [Task B]────────────>

    예: "테스트 완료 시점에 버그 수정도 완료"

    ─────────────────────────────────────────────────────────────────────────

    4. Start-to-Finish (SF) - 시작-완료 (드묾)
    ─────────────────────────────────────────────────────────────────────────
    선행 작업 시작 시 후속 작업 완료되어야 함

    [Task A]────────────>
    │
    └────────────────────>[Task B]────> (완료)

    예: "새 시스템 시작하면 구 시스템 종료"

    ─────────────────────────────────────────────────────────────────────────

    LAG (지연 시간) & LEAD (선행 시간)
    ─────────────────────────────────────────────────────────────────────────

    FS + 2일 Lag:
    [Task A]────>  (2일 대기)  [Task B]────>

    FS - 2일 Lead:
    [Task A]────────>
              │
              v (-2일)
              [Task B]────────>

================================================================================
```

### 3. 핵심 코드: 간트 차트 데이터 모델

```python
"""
Gantt Chart Data Model
간트 차트 렌더링을 위한 데이터 구조
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from enum import Enum

class DependencyType(Enum):
    FINISH_TO_START = "FS"
    START_TO_START = "SS"
    FINISH_TO_FINISH = "FF"
    START_TO_FINISH = "SF"

class TaskStatus(Enum):
    NOT_STARTED = "미시작"
    IN_PROGRESS = "진행중"
    COMPLETED = "완료"
    DELAYED = "지연"

@dataclass
class Dependency:
    """의존관계"""
    predecessor_id: str  # 선행 작업 ID
    type: DependencyType
    lag_days: int = 0  # 양수=Lag, 음수=Lead

@dataclass
class Task:
    """간트 차트 작업"""
    task_id: str
    name: str
    start_date: datetime
    end_date: datetime
    progress: float = 0.0  # 0~100
    dependencies: List[Dependency] = field(default_factory=list)
    assignee: str = ""
    status: TaskStatus = TaskStatus.NOT_STARTED
    is_milestone: bool = False
    baseline_start: Optional[datetime] = None
    baseline_end: Optional[datetime] = None
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)

    @property
    def duration(self) -> int:
        """소요 기간 (일)"""
        return (self.end_date - self.start_date).days + 1

    @property
    def is_critical(self) -> bool:
        """Critical Path 여부 (별도 계산 필요)"""
        return False

    def get_delay(self) -> int:
        """지연 일수 (베이스라인 대비)"""
        if self.baseline_end:
            return (self.end_date - self.baseline_end).days
        return 0

    def to_gantt_dict(self) -> Dict:
        """간트 차트 렌더링용 딕셔너리"""
        return {
            "id": self.task_id,
            "name": self.name,
            "start": self.start_date.isoformat(),
            "end": self.end_date.isoformat(),
            "progress": self.progress,
            "dependencies": [
                f"{d.predecessor_id}{d.type.value}"
                for d in self.dependencies
            ],
            "assignee": self.assignee,
            "status": self.status.value,
            "is_milestone": self.is_milestone,
            "delay": self.get_delay()
        }

@dataclass
class Milestone:
    """마일스톤"""
    milestone_id: str
    name: str
    date: datetime
    description: str = ""

@dataclass
class GanttChart:
    """간트 차트"""
    project_name: str
    tasks: Dict[str, Task] = field(default_factory=dict)
    milestones: List[Milestone] = field(default_factory=list)
    project_start: Optional[datetime] = None
    project_end: Optional[datetime] = None

    def add_task(self, task: Task):
        """작업 추가"""
        self.tasks[task.task_id] = task

        # 프로젝트 시작/종료일 업데이트
        if self.project_start is None or task.start_date < self.project_start:
            self.project_start = task.start_date
        if self.project_end is None or task.end_date > self.project_end:
            self.project_end = task.end_date

    def add_milestone(self, milestone: Milestone):
        """마일스톤 추가"""
        self.milestones.append(milestone)

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """ID로 작업 조회"""
        return self.tasks.get(task_id)

    def get_critical_path(self) -> List[str]:
        """Critical Path 계산 (간소화)"""
        # 실제로는 CPM 알고리즘 적용
        # 여기서는 예시용
        critical = []
        for task_id, task in self.tasks.items():
            if task.get_delay() < 0 and task.progress < 100:
                critical.append(task_id)
        return critical

    def get_progress_summary(self) -> Dict:
        """진척률 요약"""
        total_tasks = len(self.tasks)
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        in_progress = sum(1 for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS)
        delayed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.DELAYED)

        avg_progress = sum(t.progress for t in self.tasks.values()) / total_tasks if total_tasks > 0 else 0

        return {
            "total_tasks": total_tasks,
            "completed": completed,
            "in_progress": in_progress,
            "delayed": delayed,
            "average_progress": round(avg_progress, 1),
            "project_duration_days": (self.project_end - self.project_start).days + 1 if self.project_end and self.project_start else 0
        }

    def export_to_json(self) -> Dict:
        """JSON으로 내보내기"""
        return {
            "project": {
                "name": self.project_name,
                "start": self.project_start.isoformat() if self.project_start else None,
                "end": self.project_end.isoformat() if self.project_end else None
            },
            "tasks": [t.to_gantt_dict() for t in self.tasks.values()],
            "milestones": [
                {
                    "id": m.milestone_id,
                    "name": m.name,
                    "date": m.date.isoformat()
                }
                for m in self.milestones
            ],
            "summary": self.get_progress_summary()
        }

    def print_ascii_gantt(self):
        """ASCII 간트 차트 출력"""
        print(f"\n{'='*80}")
        print(f"PROJECT: {self.project_name}")
        print(f"{'='*80}")

        for task in sorted(self.tasks.values(), key=lambda x: x.start_date):
            bar = "█" * int(task.progress / 10) + "░" * (10 - int(task.progress / 10))
            status_icon = "✓" if task.status == TaskStatus.COMPLETED else "►" if task.status == TaskStatus.IN_PROGRESS else "○"
            delay_str = f" (+{task.get_delay()}일)" if task.get_delay() > 0 else ""

            print(f"{status_icon} {task.name:<25} [{bar}] {task.progress:>5.1f}%{delay_str}")

        print(f"{'='*80}")
        summary = self.get_progress_summary()
        print(f"Total: {summary['total_tasks']} tasks | Completed: {summary['completed']} | In Progress: {summary['in_progress']} | Delayed: {summary['delayed']}")
        print(f"Average Progress: {summary['average_progress']}%")
        print(f"{'='*80}\n")


# 사용 예시
if __name__ == "__main__":
    gantt = GanttChart("웹 애플리케이션 개발")

    # 작업 추가
    tasks = [
        Task("T1", "요구사항 분석", datetime(2024, 1, 1), datetime(2024, 1, 14), 100),
        Task("T2", "UI/UX 설계", datetime(2024, 1, 8), datetime(2024, 1, 21), 80,
             dependencies=[Dependency("T1", DependencyType.FINISH_TO_START)]),
        Task("T3", "DB 설계", datetime(2024, 1, 8), datetime(2024, 1, 21), 100,
             dependencies=[Dependency("T1", DependencyType.FINISH_TO_START)]),
        Task("T4", "백엔드 개발", datetime(2024, 1, 15), datetime(2024, 2, 11), 45,
             dependencies=[Dependency("T3", DependencyType.FINISH_TO_START)]),
        Task("T5", "프론트엔드 개발", datetime(2024, 1, 22), datetime(2024, 2, 18), 20,
             dependencies=[Dependency("T2", DependencyType.FINISH_TO_START)]),
        Task("T6", "통합 테스트", datetime(2024, 2, 12), datetime(2024, 2, 25), 0,
             dependencies=[Dependency("T4", DependencyType.FINISH_TO_START),
                          Dependency("T5", DependencyType.FINISH_TO_START)]),
    ]

    for task in tasks:
        if task.progress == 100:
            task.status = TaskStatus.COMPLETED
        elif task.progress > 0:
            task.status = TaskStatus.IN_PROGRESS
        gantt.add_task(task)

    # 마일스톤 추가
    gantt.add_milestone(Milestone("M1", "설계 완료", datetime(2024, 1, 21)))
    gantt.add_milestone(Milestone("M2", "개발 완료", datetime(2024, 2, 18)))
    gantt.add_milestone(Milestone("M3", "출시", datetime(2024, 2, 25)))

    # ASCII 간트 차트 출력
    gantt.print_ascii_gantt()

    # JSON 내보내기
    import json
    print(json.dumps(gantt.export_to_json(), indent=2, ensure_ascii=False))
```

---

## III. 융합 비교 및 다각도 분석

### 1. 심층 기술 비교: 간트 차트 vs 칸반 vs CPM 네트워크

| 비교 항목 | 간트 차트 | 칸반 보드 | CPM 네트워크 |
|:---|:---|:---|:---|
| **주용도** | 일정 시각화 | 작업 흐름 관리 | Critical Path 분석 |
| **시간 표현** | 명시적 (날짜) | 암시적 (스wimlane) | 상대적 (ES, LF) |
| **의존관계** | 화살표로 표시 | 없음 | 핵심 정보 |
| **병목 식별** | 어려움 | 용이 (WIP) | 용이 (CP) |
| **애자일 적합** | 낮음~중간 | 높음 | 낮음 |
| **워터폴 적합** | 높음 | 낮음 | 높음 |
| **학습 곡선** | 낮음 | 낮음 | 높음 |

### 2. 과목 융합: 간트 차트 + EVM

```
[간트 차트와 EVM 융합]

간트 차트 제공 정보          EVM 계산 활용
───────────────────────────────────────────────────
계획 시작/종료일         →   PV (계획 가치) 기간 분배
진척률 (Progress %)      →   EV (획득 가치) = BAC × %
실제 종료일 예상         →   EAC (완료 시 추정)

[융합 시각화]
간트 차트 위에 EVM 곡선 오버레이:
- S-Curve (PV, EV, AC)
- 각 시점의 SPI, CPI 표시
- 색상으로 상태 표시 (녹색: 정상, 황색: 주의, 적색: 위험)
```

---

## IV. 실무 적용 및 기술사적 판단

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오] 공공 SI 프로젝트 진척 관리**

*   **상황**:
    - 규모: 50억 원, 20인, 24개월
    - 고객: 월간 진척 보고 의무
    - 요구: "시각적으로 보여줘라"

*   **기술사적 판단**: **간트 차트 + EVM 통합 대시보드**

*   **실행 전략**:
    ```
    1. WBS 4단계까지 간트 차트 구축
    2. 마일스톤 10개 설정 (월 1회)
    3. 매주 진척률 업데이트
    4. 베이스라인과 실적 비교
    5. EVM 지표(SPI, CPI) 오버레이
    6. 지연 작업 빨간색 표시

    고객 보고:
    - 월간 PDF 간트 차트 배포
    - Critical Path 붉은 막대
    - 마일스톤 달성 여부 ◆/◇
    ```

### 2. 도입 시 고려사항

**도구 선정**:
- [ ] Microsoft Project: 전통적, 기능 풍부
- [ ] Jira + BigPicture: 애자일 통합
- [ ] Asana, Monday.com: 협업 중심
- [ ] Smartsheet: 스프레드시트 친화적

**데이터 품질**:
- [ ] 작업 분해 수준 (너무 세분화 X)
- [ ] 의존관계 정확성
- [ ] 진척률 업데이트 주기

### 3. 주의사항 및 안티패턴

*   **막대 지나친 세분화**:
    - 1시간 단위 작업까지 표시 → 가독성 저하
    - 해결: WBS 3~4단계 수준 유지

*   **정적 간트 차트**:
    - 초기 계획만 있고 업데이트 안 함
    - 해결: 주간 업데이트 의무화

---

## V. 기대효과 및 결론

### 1. 정량적/정성적 기대효과

| 구분 | 효과 내용 | 기대 수치 |
|:---:|:---|:---|
| **커뮤니케이션** | 일정 이해 시간 | 70% 단축 |
| **가시성** | 진척 파악 | 실시간 |
| **의사결정** | 일정 영향 분석 | What-If 가능 |
| **보고** | 보고서 작성 시간 | 50% 단축 |

### 2. 미래 전망

1.  **AI 일정 최적화**: 과거 데이터 기반 자동 스케줄링
2.  **실시간 협업**: 동시 편집, 자동 동기화
3.  **AR/VR**: 3D 공간에서 일정 시각화

### 3. 참고 표준

*   **PMBOK Guide**: Schedule Management
*   **ISO 21500**: Project Management

---

## 관련 개념 맵 (Knowledge Graph)

*   [WBS](@/studynotes/4_software_engineering/3_project/36_wbs.md) : 간트 차트의 데이터 소스
*   [CPM](@/studynotes/4_software_engineering/1_sdlc/37_cpm.md) : Critical Path 계산
*   [EVM](@/studynotes/4_software_engineering/3_project/project_management_evm.md) : 성과 측정 통합

---

## 어린이를 위한 3줄 비유 설명

1. **문제**: 숙제가 많은데 뭘 언제까지 해야 할지 모르겠어요.

2. **해결(간트 차트)**: **시간표 같은 그림**을 그려요! 가로는 시간, 세로는 숙제 이름이고, 각 숙제가 언제부터 언제까지인지 **막대**로 보여줘요.

3. **효과**: 한눈에 보고 "아, 이건 오늘까지!", "이건 아직 여유 있네!"를 알 수 있어요. 선생님께 보여주기도 쉬워요!
