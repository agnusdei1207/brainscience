+++
title = "06. 프로토타입 모델 (Prototype Model)"
description = "요구사항 불확실성 해소를 위한 시제품 중심 개발 방법론, 사용자 피드백 기반 점진적 완성도 향상"
date = "2026-03-04"
[taxonomies]
tags = ["prototype", "sdlc", "requirements", "user-feedback", "iterative"]
categories = ["studynotes-4_software_engineering"]
+++

# 06. 프로토타입 모델 (Prototype Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로토타입 모델은 최종 제품의 **축소형 시제품(Prototype)**을 조기에 개발하여 사용자가 직접 체험하고 피드백을 제공함으로써, **요구사항의 불확실성을 최소화**하고 개발 리스크를 조기에 완화하는 반복적 개발 방법론입니다.
> 2. **가치**: 사용자 요구사항의 **30~50%가 프로토타입 체험 후 변경**되는 현실을 고려할 때, 초기 단계에서의 피드백 루프는 전체 프로젝트 실패율을 **40% 이상 감소**시키고 재작업 비용을 획기적으로 절감합니다.
> 3. **융합**: 현대 애자일 방법론의 **스프린트 리뷰, MVP(Minimum Viable Product), 사용자 스토리 검증**의 근간이 되었으며, UX/UI 설계, 제품 관리(Product Management) 분야에서 필수적인 검증 도구로 진화했습니다.

---

### I. 개요 (Context & Background) - [최소 500자]

#### 1. 개념 정의

프로토타입 모델(Prototype Model)은 소프트웨어 개발 초기 단계에서 **실행 가능한 시제품(Working Prototype)**을 신속하게 제작하여 사용자에게 시연하고, 이를 통해 수집된 피드백을 바탕으로 요구사항을 구체화하며 점진적으로 최종 제품을 완성해 나가는 소프트웨어 개발 생명주기(SDLC) 모델입니다.

이 모델의 핵심 철학은 **"보여주고, 써보게 하고, 고쳐라(Show, Let Use, Fix)"**입니다. 사용자는 추상적인 명세서보다 실제 동작하는 화면을 보며 훨씬 더 정확하게 자신의 요구를 표현할 수 있습니다. 이를 **"I'll know it when I see it(보면 알겠어)"** 현상이라고 부릅니다.

#### 2. 비유: 건축 모형(Mock-up)과 인테리어 시공

새집을 짓기 전에 건축주는 설계도면만으로는 공간 감을 느끼기 어렵습니다. 이때 건축가는 **1/50 스케일의 모형(Mock-up)**을 제작하거나, 실제 크기의 **체험 주택(Sample House)**을 지어 보여줍니다. 건축주는 이 모형을 보며 "주방이 너무 좁아요", "거실 창문 위치를 바꿔주세요"라고 구체적인 수정 요청을 합니다.

이 과정에서 중요한 점은 모형이 **실제로 거주할 수 있는 상태가 아니라는 것**입니다. 수도, 전기, 방수 등 실제 거주에 필요한 기능은 포함되지 않지만, **공간 배치와 동선 확인**이라는 목적에는 완벽하게 부합합니다. 프로토타입 모델도 마찬가지로, 모든 기능이 완벽한 것이 아니라 **핵심 기능과 사용자 경험 검증**에 집중합니다.

#### 3. 등장 배경 및 발전 과정

**1) 전통적 방법론의 한계: "사용자는 자신이 원하는 것을 모른다"**

폭포수 모델에서는 요구사항 분석 단계에서 사용자가 모든 요구를 명확히 밝혀야 했습니다. 그러나 현실에서는 다음과 같은 문제가 발생했습니다:

- **표현 능력의 한계**: 사용자는 자신의 업무를 추상적으로만 설명 가능
- **지식의 부재**: IT 전문 용어와 기술적 표현을 이해하지 못함
- **요구사항의 진화**: 시스템을 사용해 보면서 새로운 요구가 떠오름
- **암묵적 요구**: "당연히 있어야 하는 기능"이라 말로 표현하지 않음

**2) 1980년대 프로토타이핑의 등장**

1980년대 들어 그래픽 사용자 인터페이스(GUI)가 보편화되면서, 화면 중심의 소프트웨어가 증가했습니다. 텍스트 기반 명세서만으로는 사용자 경험(UX)을 전달하기 어려워졌고, 이를 해결하기 위해 **화면 목업(Mockup)**과 **클릭 가능한 프로토타입**이 도입되었습니다.

**3) 현대로의 진화: MVP와 린 스타트업**

2000년대 이후 린 스타트업(Lean Startup) 방법론의 **MVP(Minimum Viable Product)** 개념과 결합하여, 단순한 시제품을 넘어 **실제 시장 검증 도구**로 진화했습니다. 현대의 프로토타입은 투자자 유치(Pitching), A/B 테스트, 사용자 인터뷰 등 다양한 목적으로 활용됩니다.

---

### II. 아키텍처 및 핵심 원리 (Deep Dive) - [최소 1,000자]

#### 1. 프로토타입 모델의 유형

| 유형 | 특징 | 장점 | 단점 | 적용 시나리오 |
|:---:|:---|:---|:---|:---|
| **폐기형 (Throwaway)** | 요구사항 수집 후 프로토타입을 버리고 재개발 | 빠른 제작, 피드백 집중 | 이중 작업 비용 | 요구사항이 매우 불명확한 경우 |
| **진화형 (Evolutionary)** | 프로토타입을 지속적으로 개선하여 최종 제품으로 완성 | 작업 중복 방지, 실제 코드 활용 | 코드 품질 저하 가능성 | 요구사항이 점진적으로 명확해지는 경우 |
| **증분형 (Incremental)** | 기능을 모듈별로 나누어 순차적으로 완성 | 부분적 조기 가시화, 리스크 분산 | 통합 복잡도 증가 | 대규모 시스템, 모듈 간 독립성 높은 경우 |
| **스파이럴 (Spiral)** | 위험 분석 + 프로토타이핑 결합 | 위험 기반 의사결정 | 복잡한 관리 오버헤드 | 고위험 대형 프로젝트 |

#### 2. 정교한 ASCII 다이어그램: 프로토타입 모델 프로세스

```
================================================================================
|                    PROTOTYPE MODEL - ITERATIVE FEEDBACK LOOP                  |
================================================================================

    [ PHASE 1: REQUIREMENTS GATHERING ]
    |  - Initial User Interviews
    |  - Identify Basic Requirements
    |  - Define Core Functionality
    v
    [ PHASE 2: QUICK DESIGN ]
    |  - Lo-Fi Wireframe / Mockup
    |  - Key Screens Identification
    |  - User Flow Definition
    v
    [ PHASE 3: PROTOTYPE BUILD ]
    |  - Rapid Development (Days/Weeks, not Months)
    |  - Focus on UI/UX, Not Performance
    |  - Tools: Figma, InVision, Axure, HTML/CSS
    v
    [ PHASE 4: USER EVALUATION ]
    |  - User Testing Sessions
    |  - Observe User Behavior
    |  - Collect Feedback
    v
    [ PHASE 5: REFINE REQUIREMENTS ]
    |  - Analyze Feedback
    |  - Identify Missing/Incorrect Requirements
    |  - Update Requirements Document
    |
    +----> [ MEETS EXPECTATIONS? ]
           |                    |
           | NO                 | YES
           v                    v
    [ ITERATE BACK TO        [ FINAL DEVELOPMENT ]
      PHASE 2 ]              |  - Production-Quality Code
           |                 |  - Full Architecture
           |                 |  - Complete Testing
           |                 |  - Deployment
           v                 v
    [ MAX 3-5              [ DELIVERED PRODUCT ]
      ITERATIONS ]
           |
           v
    [ DISCARD PROTOTYPE
      (Throwaway) OR
      EVOLVE TO PRODUCT
      (Evolutionary) ]

================================================================================
|                           KEY METRICS                                         |
|  - Prototype Cycle Time: 1-4 weeks per iteration                             |
|  - User Feedback Per Iteration: 10-50+ comments/changes                      |
|  - Requirements Clarity Improvement: 30-50% per iteration                    |
|  - Cost Ratio: Prototype (10-20%) vs Final Development (80-90%)              |
================================================================================
```

#### 3. 심층 동작 원리: 프로토타입 개발 사이클 (5단계 이상)

**Step 1: 요구사항 1차 수집 (Initial Requirements Gathering)**
```
[사용자] --> (인터뷰/설문/워크샵) --> [1차 요구사항 목록]
                                          |
                                          v
                                    [요구사항 분류]
                                    - 핵심 기능 (Must-have)
                                    - 부가 기능 (Nice-to-have)
                                    - 불명확 요구 (Needs Clarification)
```

**Step 2: 빠른 설계 (Quick Design)**
```
[1차 요구사항] --> (와이어프레임 도구) --> [Lo-Fi 디자인]
                                              |
                                              v
                                        [화면 흐름도]
                                        - 진입점
                                        - 핵심 사용자 여정
                                        - 예외 상황 처리
```

**Step 3: 프로토타입 구축 (Prototype Building)**
```
[Lo-Fi 디자인] --> (프로토타이핑 도구) --> [실행 가능한 시제품]
                                              |
                                              v
                                        [수준 결정]
                                        - Low-Fidelity: 종이, 화면 스케치
                                        - Medium-Fidelity: 와이어프레임, 클릭 가능
                                        - High-Fidelity: 실제와 유사한 UI, 제한적 기능
```

**Step 4: 사용자 평가 및 피드백 수집 (User Evaluation)**
```
[프로토타입] --> (사용자 테스트 세션) --> [피드백 데이터]
                                              |
                                              v
                                        [피드백 분류]
                                        - UI/UX 개선사항
                                        - 누락된 기능
                                        - 불필요한 기능
                                        - 오해/혼란 포인트
```

**Step 5: 요구사항 정제 및 반복 (Refinement & Iteration)**
```
[피드백 분석] --> [요구사항 변경 요청] --> [업데이트된 요구사항]
                                              |
                                              v
                                    [재평가 필요?] --YES--> [Step 2로 복귀]
                                              |
                                              NO
                                              v
                                    [최종 요구사항 확정]
```

#### 4. 핵심 알고리즘/코드 예시: 프로토타입 피드백 관리 시스템

```python
"""
프로토타입 피드백 수집 및 분석 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum
from datetime import datetime

class FeedbackType(Enum):
    UI_IMPROVEMENT = "UI 개선"
    MISSING_FEATURE = "누락 기능"
    UNNECESSARY = "불필요 기능"
    CONFUSION = "혼란 포인트"
    BUG = "버그"
    ENHANCEMENT = "기능 향상"

class Priority(Enum):
    CRITICAL = 1  # 즉시 수정 필요
    HIGH = 2      # 다음 반영 전 필수
    MEDIUM = 3    # 고려 필요
    LOW = 4       # 선택적 반영

@dataclass
class UserFeedback:
    """사용자 피드백 데이터 클래스"""
    feedback_id: str
    user_id: str
    session_date: datetime
    feedback_type: FeedbackType
    priority: Priority
    screen_name: str
    description: str
    suggested_solution: str = ""
    status: str = "NEW"  # NEW, ANALYZED, IMPLEMENTED, DEFERRED, REJECTED

@dataclass
class PrototypeIteration:
    """프로토타입 반복 정보"""
    iteration_number: int
    start_date: datetime
    end_date: datetime
    prototype_type: str  # Lo-Fi, Mid-Fi, Hi-Fi
    feedbacks: List[UserFeedback] = field(default_factory=list)

    def calculate_clarity_score(self) -> float:
        """요구사항 명확도 점수 계산 (0-100)"""
        if not self.feedbacks:
            return 0.0

        critical_high_count = sum(
            1 for f in self.feedbacks
            if f.priority in [Priority.CRITICAL, Priority.HIGH]
        )
        total_count = len(self.feedbacks)

        # 피드백이 적을수록 명확도가 높다고 가정
        # 단, 피드백의 질도 고려해야 함
        clarity = max(0, 100 - (critical_high_count * 10) - (total_count * 2))
        return round(clarity, 1)

    def get_feedback_summary(self) -> Dict[str, int]:
        """유형별 피드백 요약"""
        summary = {}
        for feedback_type in FeedbackType:
            count = sum(1 for f in self.feedbacks if f.feedback_type == feedback_type)
            if count > 0:
                summary[feedback_type.value] = count
        return summary

class PrototypeManager:
    """프로토타입 관리 클래스"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.iterations: List[PrototypeIteration] = []
        self.max_iterations = 5  # 최대 반복 횟수 제한

    def add_iteration(self, iteration: PrototypeIteration):
        """새로운 반복 추가"""
        if len(self.iterations) >= self.max_iterations:
            raise ValueError(f"최대 반복 횟수({self.max_iterations}) 초과")
        self.iterations.append(iteration)

    def should_continue_iteration(self) -> bool:
        """
        반복 여부 결정 로직
        - 명확도 점수가 80 이상이면 중단
        - 최대 반복 횟수 미달 시 계속
        """
        if not self.iterations:
            return True

        latest_clarity = self.iterations[-1].calculate_clarity_score()

        if latest_clarity >= 80:
            print(f"요구사항 명확도 {latest_clarity}% 달성 - 반복 종료")
            return False

        if len(self.iterations) >= self.max_iterations:
            print(f"최대 반복 횟수 도달 - 강제 종료")
            return False

        return True

    def generate_progress_report(self) -> str:
        """진행 상황 보고서 생성"""
        report = [f"\n=== {self.project_name} 프로토타입 진행 보고서 ===\n"]

        for iteration in self.iterations:
            report.append(f"\n[반복 #{iteration.iteration_number}]")
            report.append(f"  기간: {iteration.start_date} ~ {iteration.end_date}")
            report.append(f"  프로토타입 유형: {iteration.prototype_type}")
            report.append(f"  수집된 피드백: {len(iteration.feedbacks)}건")
            report.append(f"  요구사항 명확도: {iteration.calculate_clarity_score()}%")
            report.append(f"  피드백 유형별:")
            for fb_type, count in iteration.get_feedback_summary().items():
                report.append(f"    - {fb_type}: {count}건")

        return "\n".join(report)

# 사용 예시
if __name__ == "__main__":
    manager = PrototypeManager("전자상거래 모바일 앱")

    # 첫 번째 반복
    iteration1 = PrototypeIteration(
        iteration_number=1,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 7),
        prototype_type="Lo-Fi Wireframe"
    )

    # 피드백 추가
    iteration1.feedbacks.extend([
        UserFeedback("FB001", "USER01", datetime(2024,1,5),
                     FeedbackType.CONFUSION, Priority.HIGH,
                     "상품 목록", "필터 위치가 눈에 띄지 않음", "상단으로 이동"),
        UserFeedback("FB002", "USER02", datetime(2024,1,5),
                     FeedbackType.MISSING_FEATURE, Priority.CRITICAL,
                     "장바구니", "수량 변경 기능 없음", "수량 +/- 버튼 추가"),
        UserFeedback("FB003", "USER03", datetime(2024,1,6),
                     FeedbackType.UI_IMPROVEMENT, Priority.MEDIUM,
                     "결제 화면", "버튼이 너무 작음", "버튼 크기 20% 증가"),
    ])

    manager.add_iteration(iteration1)
    print(manager.generate_progress_report())
    print(f"\n반복 계속 여부: {manager.should_continue_iteration()}")
```

---

### III. 융합 비교 및 다각도 분석 - [비교표 2개 이상]

#### 1. 심층 기술 비교표: 프로토타입 모델 vs 타 SDLC 모델

| 비교 항목 | 프로토타입 모델 | 폭포수 모델 | 애자일(스크럼) | 나선형 모델 |
|:---|:---|:---|:---|:---|
| **요구사항 명확성** | 불명확해도 시작 가능 | 명확해야만 시작 | 점진적 명확화 | 위험 분석 기반 |
| **사용자 참여** | 매 반복마다 필수 | 초기/말기에만 | 매 스프린트 | 주요 마일스톤마다 |
| **문서화 수준** | 중간 (프로토타입 산출물) | 매우 높음 | 낮음 (동작 코드 우선) | 높음 (위험 보고서) |
| **변경 비용** | 낮음 (초기 단계) | 매우 높음 | 중간 | 중간 |
| **프로젝트 규모** | 중소규모, UI 중심 | 대규모, 규제 산업 | 모든 규모 가능 | 초대형, 고위험 |
| **리스크 관리** | 요구사항 리스크 중심 | 일정/예산 중심 | 제품 리스크 중심 | 전 영역 리스크 |
| **프로토타입 활용** | 핵심 활동 | 선택적 | 스프린트 결과물이 프로토타입 | 위험 완화 도구 |
| **완료 정의** | 요구사항 명확화 | 단계별 문서 승인 | 잠재적 출시 가능 증분 | 위험 허용 수준 도달 |

#### 2. 프로토타입 충실도(Fidelity)별 비교 분석

| 구분 | Low-Fidelity | Medium-Fidelity | High-Fidelity |
|:---|:---|:---|:---|
| **형태** | 종이 스케치, 화이트보드 | 디지털 와이어프레임, 클릭 가능 | 실제와 유사한 UI, 제한적 동작 |
| **제작 시간** | 몇 시간 ~ 1일 | 1일 ~ 1주 | 1주 ~ 몇 주 |
| **비용** | 매우 낮음 | 낮음 | 중간 |
| **인터랙션** | 없음 또는 수동 시뮬레이션 | 기본 클릭, 화면 전환 | 복잡한 인터랙션, 애니메이션 |
| **목적** | 아이디어 구체화, 빠른 합의 | 사용자 흐름 검증, UI 구조 확인 | 실제 사용성 테스트, 투자자 데모 |
| **도구** | 종이, 펜, 포스트잇 | Figma, Sketch, Balsamiq | Figma, ProtoPie, HTML/CSS/JS |
| **피드백 품질** | 전반적 방향성 | 구조적 개선점 | 세부 UX 이슈 |
| **폐기 비용** | 없음 | 낮음 | 중간~높음 |

#### 3. 과목 융합 관점 분석

**프로토타입 + 요구공학 (Requirements Engineering)**
```
[전통적 요구공학]              [프로토타입 기반 요구공학]
      |                                |
  문서 중심 명세                 실행 가능한 명세
      |                                |
  사용자 상상에 의존              실제 체험 기반
      |                                |
  후반 단계에 오류 발견           초기 단계에 오류 발견
      |                                |
  수정 비용 높음                  수정 비용 낮음

[융합 효과]
- 요구사항 누락률 40% 감소
- 요구사항 모순 60% 조기 발견
- 사용자 만족도 35% 향상
```

**프로토타입 + UX/UI 설계**
```
[UX 설계 프로세스와의 통합]

1. Research        -->  사용자 조사 결과를 프로토타입에 반영
2. Define          -->  페르소나, 사용자 여정 기반 시나리오 설계
3. Ideate          -->  다수 프로토타입 변형(Version) 생성
4. Prototype       -->  핵심 활동 (본 섹션)
5. Test            -->  사용성 테스트, A/B 테스트
6. Implement       -->  최종 프로토타입을 개발팀에 인계
```

---

### IV. 실무 적용 및 기술사적 판단 - [최소 800자]

#### 1. 기술사적 판단 (실무 시나리오)

**[시나리오 1] 핀테크 모바일 앱 신규 개발**

*   **상황**:
    - 최초 핀테크 스타트업의 모바일 뱅킹 앱 개발
    - 타겟 사용자: 2030 밀레니얼 세대
    - 요구사항: "편한 앱", "직관적인 UI", "빠른 송금"
    - 초기 투자: 5억 원, 개발 기간: 6개월

*   **기술사적 판단**: **진화형 프로토타입 모델 + 애자일 하이브리드**

*   **실행 전략**:
    1. **Week 1-2**: Low-Fi 프로토타입 (종이 스케치)으로 핵심 사용자 여정 3가지 정의
    2. **Week 3-4**: Medium-Fi 프로토타입 (Figma)으로 10명 대상 사용자 테스트
    3. **Week 5-8**: High-Fi 프로토타입으로 핵심 기능(잔액 조회, 송금) 구현, 50명 대상 베타 테스트
    4. **Week 9-24**: 진화형 접근으로 프로토타입을 실제 제품으로 발전시키며 2주 단위 스프린트 운영

*   **핵심 의사결정 포인트**:
    - 프로토타입 단계에서 **실제 은행 API 연동은 Mock**으로 처리
    - 보안 기능(지문 인증, OTP)은 프로토타입에서 **UI만 구현**
    - 사용자 피드백 중 **"송금 버튼이 눈에 띄지 않는다"**는 의견이 70% → UI 구조 대폭 수정

**[시나리오 2] 공공 기관 통합 정보시스템 구축**

*   **상황**:
    - 기존 10년 된 레거시 시스템을 웹 기반으로 전면 개편
    - 사용자: 내부 직원 500명 + 외부 협력기관 2000명
    - 요구사항: "기존 기능 유지", "사용성 개선", "모바일 지원"
    - 예산: 30억 원, 기간: 18개월

*   **기술사적 판단**: **폐기형 프로토타입 + 폭포수 하이브리드**

*   **실행 전략**:
    1. **기존 시스템 분석**: 화면 캡처 500장, 사용자 인터뷰 30명
    2. **프로토타입 제작**: 핵심 업무 20개 화면에 대해 Hi-Fi 프로토타입 제작
    3. **사용자 워크샵**: 5개 부서별로 프로토타입 시연 및 피드백 수집
    4. **요구사항 확정**: 프로토타입 피드백을 바탕으로 SRS(요구사항 명세서) 최종 확정
    5. **폐기 및 재개발**: 프로토타입은 요구사항 검증 목적으로만 사용 후 폐기, 정식 개발 착수

*   **핵심 의사결정 포인트**:
    - 공공 사업의 특성상 **계약상 요구사항 명세서가 필수** → 프로토타입은 보조 수단
    - 기존 시스템 사용자의 **관성(Inertia)** 고려 → 급격한 UI 변경 지양

**[시나리오 3] AI 기반 챗봇 서비스 개발**

*   **상황**:
    - 고객 상담 자동화를 위한 AI 챗봇 개발
    - 자연어 처리(NLP) 엔진의 응답 품질이 불확실
    - 사용자: 일반 고객, 예상 문의 1만 건/월

*   **기술사적 판단**: **Wizard of Oz 프로토타입**

*   **실행 전략**:
    - AI 엔진 개발 전, **사람이 AI인 척 응답**하는 방식으로 서비스 시뮬레이션
    - 2주간 실제 고객 문의 500건 처리 (사람이 타이핑)
    - 수집된 질문-응답 셋을 AI 학습 데이터로 활용
    - AI 엔진 도입 전 **고객 만족도 베이스라인** 확보

#### 2. 도입 시 고려사항 체크리스트

**기술적 고려사항**:
- [ ] **프로토타이핑 도구 선정**: Figma, Sketch, Adobe XD, ProtoPie, Axure 등 팀 역량에 맞는 도구 선택
- [ ] **프로토타입-실제 개발 간극**: 프로토타입에서 가능했던 기능이 기술적으로 구현 불가능하지 않은지 검증
- [ ] **데이터 처리**: 실제 데이터 없이 어떻게 현실적인 UI를 보여줄 것인가 (Mock Data 전략)
- [ ] **성능 고려**: 프로토타입은 성능을 고려하지 않으므로, 실제 개발 시 성능 이슈 발생 가능

**운영/조직적 고려사항**:
- [ ] **사용자 참여 보장**: 실제 최종 사용자가 프로토타입 평가에 참여할 수 있는지
- [ ] **기대치 관리**: 프로토타입이 "거의 완성된 제품"처럼 보일 수 있음 → 일정 재설정 기대 방지
- [ ] **반복 횟수 제한**: 무한 반복 방지를 위한 명확한 종료 조건 정의
- [ ] **문서화 균형**: 프로토타입 산출물과 전통적 문서 간의 일관성 유지

**비즈니스적 고려사항**:
- [ ] **ROI 계산**: 프로토타입 제작 비용 vs 요구사항 변경 비용 절감 효과 비교
- [ ] **경쟁사 대응**: 프로토타입 단계에서 시장 선점 기회를 놓치지 않는지
- [ ] **투자자/이해관계자 커뮤니케이션**: 프로토타입을 투자 유치용으로 활용 가능한지

#### 3. 주의사항 및 안티패턴 (Anti-patterns)

*   **프로토타입을 제품으로 오인 (Prototype as Product)**:
    - "이미 화면은 다 나왔는데 왜 개발이 6개월이나 걸리나요?"
    - 프로토타입은 겉모습만 구현된 것이며, 내부 로직, 데이터 처리, 보안, 성능 최적화 등은 별도 개발이 필요함을 명확히 설명해야 합니다.

*   **무한 반복 (Infinite Loop)**:
    - "조금만 더 다듬어 봅시다" → 3개월 후에도 여전히 프로토타입 단계
    - **Definition of Done**을 명확히 정의하고, 최대 반복 횟수(3~5회)를 제한해야 합니다.

*   **고립된 프로토타이핑 (Isolated Prototyping)**:
    - UX 디자이너 혼자 프로토타입을 만들고, 개발자는 나중에야 확인
    - 개발팀의 기술적 타당성 검토가 병행되지 않으면 구현 불가능한 프로토타입이 됩니다.

*   **폐기를 두려워함 (Fear of Throwing Away)**:
    - "이 코드를 버리기 아까워요" → 진화형으로 가자니 코드 품질이 낮고, 폐기하자니 아까운 딜레마
    - **Throwaway**를 선택했다면 과감하게 폐기하고, **Evolutionary**를 선택했다면 처음부터 프로덕션 퀄리티로 작성해야 합니다.

---

### V. 기대효과 및 결론 - [최소 400자]

#### 1. 정량적/정성적 기대효과

| 구분 | 효과 내용 | 기대 수치 (Industry Benchmark) |
|:---:|:---|:---|
| **요구사항 품질** | 요구사항 누락 및 모순 감소 | 40~60% 감소 |
| **재작업 비용** | 후반 단계 변경에 따른 재작업 | 50~70% 절감 |
| **사용자 만족도** | 최종 제품에 대한 사용자 만족도 | 30~40% 향상 |
| **프로젝트 성공률** | 일정/예산 내 완료 확률 | 25~35% 향상 |
| **의사소통 효율** | 이해관계자 간 합의 도출 시간 | 40~50% 단축 |
| **시장 검증** | 출시 전 제품-시장 적합성(Product-Market Fit) 검증 | 조기 실패 가능성 60% 감소 |

#### 2. 미래 전망 및 진화 방향

1.  **AI 기반 프로토타입 자동 생성**:
    - LLM(대규모 언어 모델)과 생성형 AI를 활용하여 텍스트 설명만으로 자동으로 프로토타입을 생성하는 도구(Galileo AI, Uizard 등)가 보편화될 것입니다.
    - "로그인 화면 만들어줘" → 1분 내에 완성된 UI 프로토타입 생성

2.  **실시간 협업 프로토타이핑**:
    - Figma와 같은 클라우드 기반 도구의 발전으로, 디자이너, 개발자, 사용자가 동시에 같은 프로토타입을 보며 실시간 수정 및 피드백이 가능해질 것입니다.

3.  **VR/AR 프로토타이핑**:
    - 메타버스, 공간 컴퓨팅 시대에 맞춰 3D 공간, AR/UX 경험을 프로토타이핑하는 도구가 발전할 것입니다.

4.  **No-Code/Low-Code와의 융합**:
    - 프로토타입 단계를 넘어, 프로토타입 자체가 실제 배포 가능한 제품이 되는 No-Code 플랫폼과의 경계가 모호해질 것입니다.

#### 3. 참고 표준/가이드

*   **ISO/IEC 25010**: 소프트웨어 품질 모델 - 사용성(Usability) 평가에 프로토타입 활용
*   **ISO 9241-210**: 인간-시스템 상호작용의 인간공학적 설계 - 사용자 중심 설계(UCD) 프로세스
*   **IEEE 830**: 소프트웨어 요구사항 명세서 작성 가이드 - 프로토타입을 보조 명세로 활용
*   **Nielsen Norman Group**: 사용성 평가 및 프로토타이핑 가이드라인

---

### 관련 개념 맵 (Knowledge Graph)

*   [폭포수 모델](@/studynotes/4_software_engineering/1_sdlc/sdlc_waterfall_model.md) : 프로토타입 모델이 보완하고자 한 순차적 모델의 한계
*   [나선형 모델](@/studynotes/4_software_engineering/1_sdlc/spiral_model.md) : 위험 분석과 프로토타이핑을 결합한 모델
*   [애자일 방법론](@/studynotes/4_software_engineering/1_sdlc/agile_methodology.md) : 프로토타입의 반복적 개선 철학을 계승한 현대적 방법론
*   [요구공학](@/studynotes/4_software_engineering/4_requirements/requirements_engineering.md) : 프로토타입이 핵심 도구로 활용되는 요구사항 도출 기법
*   [MVP (Minimum Viable Product)](@/studynotes/4_software_engineering/1_sdlc/_index.md) : 프로토타입 개념을 시장 검증으로 확장한 린 스타트업 개념

---

### 어린이를 위한 3줄 비유 설명

1. **문제**: 새로운 장난감을 주문했는데, 다 만들고 나니 "이런 게 아니었는데!"라고 말하는 상황이에요.
2. **해결(프로토타입)**: 먼저 장난감의 **가짜 모형(시제품)**을 레고로 만들어 보여주고, "이게 맞아?"라고 먼저 물어봐요. 친구가 "다리가 더 길었으면 좋겠어"라고 하면, 레고를 고쳐서 다시 보여줘요.
3. **효과**: 진짜 장난감을 만들기 전에 친구가 원하는 모양을 정확히 알 수 있어서, 다 만들고 나서 "아, 이게 아니었어" 하고 다시 만드는 일이 없어져요!
