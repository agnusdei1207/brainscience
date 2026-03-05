+++
title = "37. CPM (Critical Path Method)"
description = "프로젝트의 최단 완료 기간을 결정하는 핵심 경로 분석 기법, 일정 최적화의 필수 도구"
date = "2026-03-05"
[taxonomies]
tags = ["cpm", "critical-path", "scheduling", "project-management", "pert"]
categories = ["studynotes-4_software_engineering"]
+++

# 37. CPM (Critical Path Method)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CPM은 프로젝트를 구성하는 **모든 작업의 선후관계와 소요시간을 분석**하여, 프로젝트 완료에 **최장 시간이 소요되는 경로(Critical Path)**를 식별하고 일정을 최적화하는 네트워크 기반 일정 관리 기법입니다.
> 2. **가치**: Critical Path 상의 작업은 **1일 지연 시 프로젝트 전체가 1일 지연**되므로 집중 관리 대상이 되며, Float(여유시간) 분석을 통해 자원 재배분으로 **전체 공기를 10~30% 단축**할 수 있습니다.
> 3. **융합**: PERT, Gantt Chart, EVM과 결합하여 사용되며, 최신 프로젝트 관리 도구(MS Project, Jira Advanced Roadmaps)에서 자동 계산됩니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**CPM(Critical Path Method, 주공정법)**은 1957년 미국 듀폰(DuPont) 사와 레밍턴-유니박(Remington-Rand) 사가 공동 개발한 프로젝트 일정 관리 기법입니다. 프로젝트를 **노드(작업)**와 **간선(의존관계)**으로 구성된 네트워크로 표현하고, **최장 경로**를 찾아 프로젝트의 최단 완료 기간을 결정합니다.

**CPM의 핵심 개념**:

| 용어 | 정의 | 계산 공식 |
|:---|:---|:---|
| **Critical Path** | 프로젝트 완료까지 최장 시간이 걸리는 경로 | ES=LS, EF=LF인 작업들의 연결 |
| **ES (Earliest Start)** | 작업이 시작될 수 있는 가장 빠른 시점 | 선행 작업들의 EF 중 최대값 |
| **EF (Earliest Finish)** | 작업이 완료될 수 있는 가장 빠른 시점 | ES + Duration |
| **LF (Latest Finish)** | 후속 작업 지연 없이 완료해야 하는 최늦 시점 | 후속 작업들의 LS 중 최소값 |
| **LS (Latest Start)** | 후속 작업 지연 없이 시작해야 하는 최늦 시점 | LF - Duration |
| **Float (Slack)** | 작업이 지연될 수 있는 여유 시간 | LS - ES 또는 LF - EF |
| **Free Float** | 후속 작업에 영향 없이 지연 가능한 시간 | 후속 ES - 현재 EF |

### 2. 비유: 등산 코스와 최단 시간

```
[CPM = 등산 코스 찾기]

                ┌─── Task B (2시간) ────────────────┐
                │                                    │
    출발점 ──── Task A (3시간) ────┬─────────────> 합류점 ────> 정상
                │                 │                  │
                └─── Task C (5시간) ────────────────┘

분석:
- 경로 1: A → B → 정상 = 3 + 2 = 5시간
- 경로 2: A → C → 정상 = 3 + 5 = 8시간

Critical Path = 경로 2 (A → C)
- 이 코스가 1분 늦어지면 전체 등산이 1분 늦어짐
- Task B는 3시간 여유가 있음 (Float = 3시간)

전략:
- Task C에 인력 집중! 여기서 막히면 정상 도착 늦어짐
- Task B는 여유가 있으니 천천히 가도 됨
```

### 3. 등장 배경 및 발전 과정

**1) 1957년: 듀폰(DuPont)의 공장 보수 프로젝트**
- 화학 공장의 정기 보수 기간 단축 필요
- 수천 개의 작업 간 복잡한 선후관계 정리
- 결과: 보수 기간 37% 단축 (1,000시간 → 630시간)

**2) 1958년: 미 해군의 PERT 개발과 동시 발전**
- 폴라리스 미사일 개발 프로젝트
- PERT는 확률적 소요시간 적용 (낙관/기대/비관)
- CPM은 확정적 소요시간 적용

**3) 1960~70년대: 건설/엔지니어링 산업으로 확산**
- 대형 건설 프로젝트에 표준 도구로 정착

**4) 2000년대~현재: 소프트웨어 프로젝트 관리에 적용**
- MS Project, Primavera 등 도구에서 자동화
- 애자일에서도 스프린트 간 의존성 관리에 활용

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. CPM 네트워크 다이어그램

```
================================================================================
|                   CPM NETWORK DIAGRAM - EXAMPLE                               |
================================================================================

    프로젝트: 소프트웨어 개발 (총 15일 소요)

                          ┌─────────────────────────────────┐
                          │         LEGEND                  │
                          │  ES │ Dur │ EF                 │
                          │  LS │     │ LF                 │
                          │  [작업명]   Float = LS-ES       │
                          └─────────────────────────────────┘

         ┌──────────────────┐                         ┌──────────────────┐
         │   0  │ 3  │ 3   │                         │   3  │ 2  │ 5   │
         │   0  │    │ 3   │                         │   7  │    │ 9   │
         │ [A.요구분석]  0  │───────────────────────>│ [B.UI설계]   4   │
         └──────────────────┘                         └──────────────────┘
                  │                                              │
                  │                                              │
                  v                                              v
         ┌──────────────────┐                         ┌──────────────────┐
         │   3  │ 5  │ 8   │                         │   5  │ 4  │ 9   │
         │   3  │    │ 8   │                         │   5  │    │ 9   │
         │ [C.DB설계]    0  │───────────────────────>│ [D.개발]     0   │
         └──────────────────┘                         └──────────────────┘
                  │                                              │
                  │                                              │
                  v                                              v
         ┌──────────────────┐                         ┌──────────────────┐
         │   8  │ 2  │ 10  │                         │   9  │ 5  │ 14  │
         │  10  │    │ 12  │                         │   9  │    │ 14  │
         │ [E.API개발]   2  │                         │ [F.통합테스트] 0 │
         └──────────────────┘                         └──────────────────┘
                  │                                              │
                  └──────────────────┬───────────────────────────┘
                                     │
                                     v
                            ┌──────────────────┐
                            │  14  │ 1  │ 15  │
                            │  14  │    │ 15  │
                            │ [G.배포]      0  │
                            └──────────────────┘

    ─────────────────────────────────────────────────────────────────────────

    CRITICAL PATH (주공정): A → C → D → F → G (굵은 선)
    총 소요 기간: 15일

    비주공정 작업 (Float > 0):
    - B (UI설계): Float = 4일 → 4일까지 지연 가능
    - E (API개발): Float = 2일 → 2일까지 지연 가능

================================================================================
```

### 2. Forward Pass / Backward Pass 알고리즘

```
================================================================================
|                        CPM CALCULATION ALGORITHM                              |
================================================================================

FORWARD PASS (전진 계산) - ES, EF 계산
─────────────────────────────────────────────────────────────────────────────
Step 1: 시작 작업의 ES = 0
Step 2: EF = ES + Duration
Step 3: 후속 작업의 ES = 선행 작업들의 EF 중 최대값
Step 4: 모든 작업까지 반복

예시:
  A (Duration=3): ES=0, EF=0+3=3
  B (Duration=2): ES=3 (A의 EF), EF=3+2=5
  C (Duration=5): ES=3 (A의 EF), EF=3+5=8
  D (Duration=4): ES=max(5,8)=8 (B,C의 EF 중 최대), EF=8+4=12
  ...

─────────────────────────────────────────────────────────────────────────────

BACKWARD PASS (후진 계산) - LF, LS 계산
─────────────────────────────────────────────────────────────────────────────
Step 1: 마지막 작업의 LF = 프로젝트 완료일 (EF와 동일)
Step 2: LS = LF - Duration
Step 3: 선행 작업의 LF = 후속 작업들의 LS 중 최소값
Step 4: 시작 작업까지 역순으로 반복

예시:
  G (Duration=1): LF=15, LS=15-1=14
  F (Duration=5): LF=14 (G의 LS), LS=14-5=9
  D (Duration=4): LF=9 (F의 LS), LS=9-4=5
  C (Duration=5): LF=5 (D의 LS), LS=5-5=0... (잘못됨, 재계산)
  ...

─────────────────────────────────────────────────────────────────────────────

FLOAT 계산
─────────────────────────────────────────────────────────────────────────────
Total Float = LS - ES = LF - EF
Free Float  = min(후속 ES) - 현재 EF

Critical Path 판정: Float = 0인 작업들의 연결

================================================================================
```

### 3. 핵심 코드: CPM 계산 엔진

```python
"""
CPM (Critical Path Method) Calculator
주공정법 일정 분석 엔진
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

class TaskStatus(Enum):
    NOT_STARTED = "미시작"
    IN_PROGRESS = "진행중"
    COMPLETED = "완료"

@dataclass
class Task:
    """작업 정의"""
    task_id: str
    name: str
    duration: int  # 일 단위
    predecessors: List[str] = field(default_factory=list)
    successors: List[str] = field(default_factory=list)

    # CPM 계산 결과
    es: int = 0  # Earliest Start
    ef: int = 0  # Earliest Finish
    ls: int = 0  # Latest Start
    lf: int = 0  # Latest Finish
    float_days: int = 0  # Total Float
    is_critical: bool = False
    status: TaskStatus = TaskStatus.NOT_STARTED

class CPMCalculator:
    """CPM 계산기"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def add_task(self, task: Task):
        """작업 추가"""
        self.tasks[task.task_id] = task
        # 선행/후속 관계 설정
        for pred_id in task.predecessors:
            if pred_id in self.tasks:
                self.tasks[pred_id].successors.append(task.task_id)

    def forward_pass(self):
        """전진 계산 (ES, EF)"""
        processed = set()

        def calculate_es_ef(task_id: str):
            if task_id in processed:
                return

            task = self.tasks[task_id]

            if not task.predecessors:
                # 시작 작업
                task.es = 0
            else:
                # 선행 작업들의 EF 중 최대값
                max_ef = 0
                for pred_id in task.predecessors:
                    if pred_id not in processed:
                        calculate_es_ef(pred_id)
                    pred_ef = self.tasks[pred_id].ef
                    max_ef = max(max_ef, pred_ef)
                task.es = max_ef

            task.ef = task.es + task.duration
            processed.add(task_id)

        for task_id in self.tasks:
            calculate_es_ef(task_id)

    def backward_pass(self, project_end: Optional[int] = None):
        """후진 계산 (LF, LS)"""
        if not self.tasks:
            return

        # 프로젝트 종료일 = 마지막 작업들의 EF 중 최대값
        if project_end is None:
            project_end = max(t.ef for t in self.tasks.values())

        processed = set()

        def calculate_lf_ls(task_id: str):
            if task_id in processed:
                return

            task = self.tasks[task_id]

            if not task.successors:
                # 마지막 작업
                task.lf = project_end
            else:
                # 후속 작업들의 LS 중 최소값
                min_ls = float('inf')
                for succ_id in task.successors:
                    if succ_id not in processed:
                        calculate_lf_ls(succ_id)
                    succ_ls = self.tasks[succ_id].ls
                    min_ls = min(min_ls, succ_ls)
                task.lf = min_ls

            task.ls = task.lf - task.duration
            processed.add(task_id)

        # 후속이 없는 작업부터 역순으로 계산
        end_tasks = [t_id for t_id, t in self.tasks.items()
                     if not t.successors]
        for task_id in end_tasks:
            calculate_lf_ls(task_id)

        # 모든 작업이 처리되도록 전체 재실행
        for task_id in self.tasks:
            if task_id not in processed:
                calculate_lf_ls(task_id)

    def calculate_float(self):
        """Float 계산 및 Critical Path 식별"""
        for task in self.tasks.values():
            task.float_days = task.ls - task.es
            task.is_critical = (task.float_days == 0)

    def get_critical_path(self) -> List[str]:
        """Critical Path 반환"""
        critical_tasks = [t_id for t_id, t in self.tasks.items()
                         if t.is_critical]
        # 순서대로 정렬 (ES 기준)
        critical_tasks.sort(key=lambda x: self.tasks[x].es)
        return critical_tasks

    def get_project_duration(self) -> int:
        """프로젝트 총 소요 기간"""
        if not self.tasks:
            return 0
        return max(t.ef for t in self.tasks.values())

    def analyze(self) -> Dict:
        """전체 분석 수행"""
        self.forward_pass()
        self.backward_pass()
        self.calculate_float()

        return {
            "project_duration": self.get_project_duration(),
            "critical_path": self.get_critical_path(),
            "tasks_with_float": [
                (t_id, t.name, t.float_days)
                for t_id, t in self.tasks.items()
                if t.float_days > 0
            ],
            "critical_tasks": [
                (t_id, t.name, t.es, t.ef)
                for t_id, t in self.tasks.items()
                if t.is_critical
            ]
        }

    def print_schedule(self):
        """일정표 출력"""
        print("\n" + "="*80)
        print(f"{'Task':<20} {'Dur':>4} {'ES':>4} {'EF':>4} {'LS':>4} {'LF':>4} {'Float':>6} {'Critical':>8}")
        print("="*80)

        for task_id in sorted(self.tasks.keys(), key=lambda x: self.tasks[x].es):
            t = self.tasks[task_id]
            critical = "YES" if t.is_critical else ""
            print(f"{t.name:<20} {t.duration:>4} {t.es:>4} {t.ef:>4} {t.ls:>4} {t.lf:>4} {t.float_days:>6} {critical:>8}")

        print("="*80)
        print(f"Project Duration: {self.get_project_duration()} days")
        print(f"Critical Path: {' → '.join([self.tasks[t].name for t in self.get_critical_path()])}")
        print("="*80)

# 사용 예시
if __name__ == "__main__":
    cpm = CPMCalculator()

    # 소프트웨어 개발 프로젝트 작업 정의
    tasks = [
        Task("A", "요구사항 분석", 3, []),
        Task("B", "UI 설계", 2, ["A"]),
        Task("C", "DB 설계", 5, ["A"]),
        Task("D", "백엔드 개발", 8, ["C"]),
        Task("E", "프론트엔드 개발", 6, ["B"]),
        Task("F", "통합 테스트", 4, ["D", "E"]),
        Task("G", "배포", 2, ["F"]),
    ]

    for task in tasks:
        cpm.add_task(task)

    # 분석 실행
    result = cpm.analyze()

    print(f"\n프로젝트 총 소요 기간: {result['project_duration']}일")
    print(f"Critical Path: {' → '.join([cpm.tasks[t].name for t in result['critical_path']])}")

    cpm.print_schedule()
```

---

## III. 융합 비교 및 다각도 분석

### 1. 심층 기술 비교: CPM vs PERT vs Gantt

| 비교 항목 | CPM | PERT | Gantt Chart |
|:---|:---|:---|:---|
| **소요시간** | 확정적 (단일 값) | 확률적 (3점 추정) | 확정적 |
| **주용도** | 일정 최적화, Float 분석 | 불확실성 관리, 리스크 분석 | 시각화, 진척 관리 |
| **복잡도** | 중간 | 높음 (확률 계산) | 낮음 |
| **네트워크** | 필수 | 필수 | 선택적 |
| **강점** | Critical Path 식별 | 예측 정확도 | 직관적 시각화 |
| **약점** | 변동성 반영 못함 | 계산 복잡 | 의존관계 파악 어려움 |

### 2. CPM과 EVM 융합

```
[CPM + EVM 융합]

CPM 제공 정보                     EVM 활용
───────────────────────────────────────────────────
Critical Path 작업         →     SPI, CPI 우선 모니터링
Float (여유시간)           →     일정 영향도 분석
ES, EF (계획 일정)         →     PV (계획 가치) 계산 기준
실제 진행률                →     EV (획득 가치) 계산

[융합 시나리오]
Critical Path 상의 작업 F가 2일 지연
→ Float = 0이므로 프로젝트 전체 2일 지연
→ EVM: SPI < 1.0, SV < 0
→ 조치: Float이 있는 비주공정 작업에서 자원 재배분
```

### 3. 과목 융합: CPM + 소프트웨어 아키텍처

```
[MSA 구축 프로젝트에 CPM 적용]

작업                           의존관계           Duration
─────────────────────────────────────────────────────────
A. 마이크로서비스 식별          없음               5일
B. API 게이트웨이 설계          A                  3일
C. 서비스별 DB 설계             A                  4일
D. User 서비스 개발             B, C               8일
E. Order 서비스 개발            B, C               10일
F. Payment 서비스 개발          B, C               7일
G. 서비스 메시 구축             B                  5일
H. 통합 테스트                  D, E, F, G         6일
I. 배포 파이프라인              없음               3일 (병렬)
J. 최종 배포                    H, I               2일

Critical Path 분석:
- 경로 1: A → B → G → H → J = 5+3+5+6+2 = 21일
- 경로 2: A → C → E → H → J = 5+4+10+6+2 = 27일 ★

Critical Path: A → C → E → H → J
- Order 서비스(E)가 가장 오래 걸림 → 자원 집중
- Payment 서비스(F)는 Float = 3일 존재
- 배포 파이프라인(I)은 병렬 수행으로 Float = 22일
```

---

## IV. 실무 적용 및 기술사적 판단

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오] 대형 공공 SI 프로젝트 일정 관리**

*   **상황**:
    - 규모: 100억 원, 30인, 18개월
    - WBS 작업 수: 500개
    - 문제: 일정 지연 누적, 책임 소재 불분명

*   **기술사적 판단**: **CPM 기반 일정 통제 체계 구축**

*   **실행 전략**:
    ```
    1. WBS 4단계까지 분해 후 CPM 네트워크 구축
    2. Critical Path 상 20개 작업 식별
    3. 주공정 작업에 자원 집중 (경력자 배치, 투입 증원)
    4. Float 활용: 비주공정 작업에서 자원 차출
    5. 주간 CPM 리뷰: Critical Path 변화 모니터링

    개선 효과:
    - 일정 지연 조기 경보 (Critical Path 이탈 시)
    - 자원 최적화 (Float 활용)
    - 책임 소재 명확화
    ```

### 2. 도입 시 고려사항

**데이터 품질**:
- [ ] 작업 간 선후관계 정확성 검증
- [ ] Duration 추정의 신뢰성 (전문가 합의)
- [ ] 리스크 버퍼 포함 여부 결정

**도구 선정**:
- [ ] MS Project, Primavera P6, Jira Advanced Roadmaps
- [ ] 자동 CPM 계산, Critical Path 하이라이트 기능
- [ ] What-If 시뮬레이션 기능

### 3. 주의사항 및 안티패턴

*   **Critical Path 고집 (Critical Path Fixation)**:
    - 비주공정 작업 무시하다가 Float 소진 후 급격한 지연
    - 해결: Near-Critical Path (Float < 5일)도 모니터링

*   **과도한 세분화**:
    - 1시간 단위 작업까지 CPM 적용 → 관리 오버헤드 과다
    - 해결: 적정 수준(WBS 3~4단계)에서 적용

---

## V. 기대효과 및 결론

### 1. 정량적/정성적 기대효과

| 구분 | 효과 내용 | 기대 수치 |
|:---:|:---|:---|
| **일정 단축** | 자원 최적화로 공기 단축 | 10~20% |
| **리스크 관리** | Critical Path 집중 관리 | 지연 조기 감지 |
| **의사결정** | What-If 분석 지원 | 대안 비교 용이 |
| **커뮤니케이션** | 네트워크 다이어그램 시각화 | 이해관계자 합의 |

### 2. 미래 전망

1.  **AI 기반 일정 최적화**: 머신러닝으로 최적 자원 배분
2.  **실시간 CPM**: IoT 센서와 연동한 실시간 진척률 반영
3.  **몬테카를로 시뮬레이션**: 확률적 CPM으로 리스크 정량화

### 3. 참고 표준

*   **PMBOK Guide**: Schedule Management 지식 영역
*   **ISO 21500**: 프로젝트 관리 국제 표준

---

## 관련 개념 맵 (Knowledge Graph)

*   [WBS](@/studynotes/4_software_engineering/3_project/36_wbs.md) : CPM 적용 전 작업 분할 선행
*   [PERT](@/studynotes/4_software_engineering/1_sdlc/_index.md) : CPM과 유사한 확률적 일정 기법
*   [EVM](@/studynotes/4_software_engineering/3_project/project_management_evm.md) : CPM 일정과 성과 측정 융합

---

## 어린이를 위한 3줄 비유 설명

1. **문제**: 여행을 가는데 짐 싸기, 표 끊기, 숙소 예약 중 뭐부터 해야 할지 모르겠어요!

2. **해결(CPM)**: **가장 오래 걸리는 길**을 찾아요! 표 끊기가 3일 걸리고, 숙소 예약은 1일, 짐 싸기는 반나절이면, 표 끊기가 가장 중요해요. 이게 늦어지면 여행 전체가 늦어지니까요!

3. **효과**: 중요한 것부터 먼저 하고, 여유 있는 건 나중에 해도 된다는 걸 알게 돼요. 그래서 계획대로 여행을 갈 수 있어요!
