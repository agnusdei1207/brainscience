+++
title = "나선형 모델 (Spiral Model)"
date = 2024-05-24
description = "위험 분석을 통해 프로젝트 실패를 조기에 예방하는 반복적 개발 모델"
weight = 70
+++

# 나선형 모델 (Spiral Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 나선형 모델은 **1988년 Barry Boehm**이 제안한 SDLC 모델로, **폭포수의 체계성과 프로토타입의 반복성을 결합**하되, 각 반복마다 **위험 분석(Risk Analysis)**을 선행하여 프로젝트 실패를 조기에 예방하는 접근법입니다.
> 2. **가치**: 고위험 대형 프로젝트에서 **실패율을 40% 이상 감소**시키며, 특히 **신기술 도입, 요구사항 불확실, 대규모 통합** 프로젝트에서 위험을 체계적으로 관리할 수 있습니다.
> 3. **융합**: 현대 애자일의 **스파이크(Spike), 인크리먼트(Increment), 위험 기반 백로그 우선순위**의 이론적 기반이 되었으며, 대규모 애자일 프레임워크(SAFe)에도 위험 관리 개념이 통합되었습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**나선형 모델(Spiral Model)**은 소프트웨어 개발 과정을 **나선형으로 반복**하면서 각 주기(Spiral Cycle)마다 **목표 설정 → 위험 분석 → 개발 및 검증 → 계획 수립**의 4단계를 거치는 생명주기 모델입니다. 각 반복에서 위험을 분석하고 완화함으로써 프로젝트 실패를 사전에 예방하는 것이 핵심입니다.

**나선형 모델의 4가지 사분면(Quadrant)**:

| 사분면 | 명칭 | 핵심 활동 | 산출물 |
| :--- | :--- | :--- | :--- |
| **1** | 목표 설정 | 요구사항 정의, 제약조건 식별, 대안 도출 | 요구사항 목록, 대안 분석 |
| **2** | 위험 분석 | 위험 식별, 평가, 완화 전략 수립, 프로토타입 | 위험 분석 보고서, 프로토타입 |
| **3** | 개발 및 검증 | 설계, 코딩, 테스트, 통합 | 소프트웨어 증분 |
| **4** | 계획 수립 | 다음 반복 계획, 일정/자원 재조정 | 다음 반복 계획서 |

**핵심 개념: 위험(Risk) vs 불확실성(Uncertainty)**:
```
위험(Risk):
- 발생 가능성과 영향도를 추정할 수 있음
- 예: "핵심 개발자 이직 확률 30%, 2주 지연 영향"

불확실성(Uncertainty):
- 발생 가능성이나 영향도를 알 수 없음
- 예: "신기술이 6개월 내에 안정화될지 알 수 없음"

나선형 모델의 목표:
→ 불확실성을 위험으로 전환 (분석, 프로토타이핑)
→ 위험을 수용 가능한 수준으로 완화
```

### 💡 일상생활 비유: 탐험 여행

```
[나선형 모델 = 정글 탐험]

전통적 방식 (폭포수):
  "출발!" → 무작정 앞으로 이동 → 낭떠러지 발견 → "망했어요"

나선형 방식:
  루프 1:
    목표: "기지에서 1km 지점까지"
    위험분석: "지도를 보니 늪지대가 있어요" → 우회로 탐색
    실행: 우회로 이동, 표지판 설치
    계획: "다음은 2km 지점까지"

  루프 2:
    목표: "2km 지점까지"
    위험분석: "야생동물 흔적 발견" → 무기 준비
    실행: 안전하게 2km 도달
    계획: "다음은 3km 지점까지"

  ... 반복 ...

핵심:
- 위험을 먼저 파악하고 대비
- 작은 목표부터 점진적 달성
- 문제 시 이전 단계로 안전하게 복귀
- 각 단계에서 학습하고 개선
```

### 2. 등장 배경 및 발전 과정

#### 1) 1980년대: 기존 모델의 한계

**폭포수 모델의 문제**:
- 후반 단계에서 위험 발견 → 재작업 비용 막대
- 요구사항 변경에 취약
- 대형 프로젝트에서 실패 빈번

**프로토타입 모델의 문제**:
- 위험 관리 체계 없음
- 무한 반복 가능성
- 품질 관리 어려움

#### 2) 1988년: Barry Boehm의 제안

**Barry W. Boehm**의 논문:
> "A Spiral Model of Software Development and Enhancement"
> IEEE Computer, 1988

핵심 통찰:
```
"프로젝트 실패의 주요 원인은 요구사항이나 기술이 아니라
 위험(Risk)을 체계적으로 관리하지 않기 때문이다."

기여:
1. 위험 분석을 개발 프로세스에 통합
2. 각 반복마다 위험을 평가하고 완화
3. 프로토타이핑을 위험 완화 도구로 활용
4. 점진적 확장(Incremental Development) 개념 도입
```

#### 3) 1990년대~현재: 진화와 적용

| 연도 | 발전 | 내용 |
| :--- | :--- | :--- |
| **1990s** | WINWIN Spiral | 이해관계자 승리 조건(Win-Win) 추가 |
| **2000s** | 애자일 영향 | 스파이크, 위험 기반 백로그 |
| **2010s** | SAFe 통합 | 대규모 애자일에 위험 관리 통합 |
| **현재** | 하이브리드 | 나선형 + 애자일 결합 운영 |

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 나선형 모델 4사분면 상세 구조

| 사분면 | 활동 | 세부 작업 | 기법/도구 |
| :--- | :--- | :--- | :--- |
| **Q1: 목표 설정** | 요구사항 정의 | 이해관계자 식별, 요구사항 수집, 제약조건 명시 | 인터뷰, 설문, 분석 |
| **Q2: 위험 분석** | 위험 관리 | 위험 식별, 평가, 우선순위, 완화 전략, 프로토타이핑 | FMEA, FTA, 시뮬레이션 |
| **Q3: 개발 검증** | 구현 | 설계, 코딩, 테스트, 통합 | 표준 개발 방법론 |
| **Q4: 계획 수립** | 다음 단계 계획 | 성과 검토, 다음 반복 계획, 자원 재조정 | PM 도구, 검토 회의 |

### 2. 정교한 구조 다이어그램: 나선형 모델 전체 구조

```text
================================================================================
|                    SPIRAL MODEL ARCHITECTURE                                |
================================================================================

                    방사형 축: 누적 비용 (Cumulative Cost)
                              ↑
                              │
    ══════════════════════════╪══════════════════════════════════════════
    │                         │                                         │
    │    ┌─────────────────┐  │  ┌─────────────────┐                    │
    │    │   Q1: 목표설정   │  │  │   Q2: 위험분석   │                    │
    │    │                 │  │  │                 │                    │
    │    │ • 요구사항 정의 │  │  │ • 위험 식별     │                    │
    │    │ • 제약조건 식별 │──┼──│ • 위험 평가     │                    │
    │    │ • 대안 도출     │  │  │ • 완화 전략     │                    │
    │    └─────────────────┘  │  │ • 프로토타이핑 │                    │
    │            │            │  └────────┬────────┘                    │
    │            │            │           │                             │
    │            │    Cycle 1 │           │        (0° → 90°)           │
    │            │            │           │                             │
    │            │            │           v                             │
    │    ┌───────┴────────┐   │  ┌─────────────────┐                    │
    │    │   Q4: 계획수립   │   │  │   Q3: 개발검증   │                    │
    │    │                 │   │  │                 │                    │
    │    │ • 다음 계획     │   │  │ • 설계          │                    │
    │    │ • 자원 재조정   │←──┼──│ • 구현          │                    │
    │    │ • 기준선 설정   │   │  │ • 테스트        │                    │
    │    └─────────────────┘   │  └─────────────────┘                    │
    │                          │                                         │
    ═══════════════════════════╪══════════════════════════════════════════
                               │
    ───────────────────────────┼──────────────────────────────────────────
                               │
    ═══════════════════════════╪══════════════════════════════════════════
    │                          │                                         │
    │    ┌─────────────────┐   │  ┌─────────────────┐                    │
    │    │   Q1: 목표설정   │   │  │   Q2: 위험분석   │                    │
    │    │                 │   │  │                 │                    │
    │    │ • 요구사항 확장 │   │  │ • 새로운 위험   │                    │
    │    │ • 기능 추가     │───┼─│ • 기술 검증     │                    │
    │    └─────────────────┘   │  └────────┬────────┘                    │
    │            │             │           │                             │
    │            │    Cycle 2  │           │        (360° → 450°)        │
    │            │             │           v                             │
    │    ┌───────┴────────┐    │  ┌─────────────────┐                    │
    │    │   Q4: 계획수립   │    │  │   Q3: 개발검증   │                    │
    │    │                 │    │  │                 │                    │
    │    │ • 다음 계획     │    │  │ • 기능 확장     │                    │
    │    │                 │←───┼──│ • 통합 테스트   │                    │
    │    └─────────────────┘    │  └─────────────────┘                    │
    │                           │                                         │
    ════════════════════════════╪═════════════════════════════════════════
                                │
                    ────────────┴────────────
                              각도축: 진행 단계 (Phase)

================================================================================
|                    RISK ANALYSIS PROCESS (Q2 상세)                          |
================================================================================

    ┌─────────────────────────────────────────────────────────────────────┐
    │                     위험 분석 4단계 프로세스                         │
    ├─────────────────────────────────────────────────────────────────────┤
    │                                                                     │
    │   Step 1: 위험 식별 (Risk Identification)                          │
    │   ========================================                          │
    │   • 기술적 위험: "이 기술이 우리 요구를 충족할까?"                  │
    │   • 인적 위험: "핵심 인력이 이직하면?"                              │
    │   • 일정 위험: "일정이 현실적인가?"                                 │
    │   • 비용 위험: "예산이 충분한가?"                                   │
    │   • 외부 위험: "공급업체가 도산하면?"                               │
    │                                                                     │
    │   Step 2: 위험 평가 (Risk Assessment)                              │
    │   ========================================                          │
    │   위험 점수 = 발생확률(P) × 영향도(I)                               │
    │                                                                     │
    │   ┌─────────────┬─────────────┬─────────────┐                       │
    │   │  영향도\확률 │    낮음     │    높음     │                       │
    │   ├─────────────┼─────────────┼─────────────┤                       │
    │   │   높음      │   중간      │   매우높음  │                       │
    │   │   낮음      │   낮음      │   중간      │                       │
    │   └─────────────┴─────────────┴─────────────┘                       │
    │                                                                     │
    │   Step 3: 위험 완화 전략 (Risk Mitigation)                         │
    │   ========================================                          │
    │   • 회피(Avoid): 위험 원천 제거                                    │
    │   • 전가(Transfer): 보험, 아웃소싱                                 │
    │   • 완화(Mitigate): 확률/영향도 감소                               │
    │   • 수용(Accept): 비상 계획(Contingency Plan)                       │
    │                                                                     │
    │   Step 4: 프로토타이핑 (Prototyping for Risk Resolution)           │
    │   =======================================================           │
    │   • 기술 검증: 기술적 위험 해소                                    │
    │   • 사용자 검증: 요구사항 위험 해소                                │
    │   • 성능 검증: 성능 위험 해소                                      │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

================================================================================
```

### 3. 심층 동작 원리: 위험 기반 의사결정

```
[각 사이클의 의사결정 포인트]

Cycle 시작
    │
    v
┌─────────────────┐
│ 목표 설정 (Q1)  │
└────────┬────────┘
         │
         v
┌─────────────────┐     위험 없음      ┌─────────────────┐
│ 위험 분석 (Q2)  │──────────────────→ │ 개발 진행 (Q3)  │
└────────┬────────┘                    └─────────────────┘
         │
         │ 위험 존재
         v
┌─────────────────────────────────────────────────────────────┐
│                    위험 해결 여부 판단                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   위험 해결 가능?                                            │
│        │                                                    │
│   YES  │  NO                                                │
│        │  ┌─────────────────────────────────┐               │
│        │  │                                 │               │
│        │  │  프로젝트 계속 가능?             │               │
│        │  │       │                         │               │
│        │  │  YES  │  NO                     │               │
│        │  │       │   ┌──────────────┐      │               │
│        │  │       │   │  프로젝트    │      │               │
│        │  │       └──→│  종료/변경   │      │               │
│        │  │           │  (Abort)     │      │               │
│        v  v           └──────────────┘      │               │
│   ┌─────────────────┐                        │               │
│   │ 프로토타입/스파이크│                        │               │
│   │ (위험 해소)      │                        │               │
│   └────────┬────────┘                        │               │
│            │                                 │               │
│            v                                 │               │
│   ┌─────────────────┐                        │               │
│   │ 위험 재평가      │←───────────────────────┘               │
│   └────────┬────────┘                                        │
│            │                                                 │
└────────────┼────────────────────────────────────────────────┘
             │
             v
    ┌─────────────────┐
    │ 개발 및 검증 (Q3) │
    └────────┬────────┘
             │
             v
    ┌─────────────────┐
    │ 계획 수립 (Q4)   │
    └────────┬────────┘
             │
             v
    ┌─────────────────┐
    │ 다음 Cycle?      │
    │ YES → 처음으로   │
    │ NO  │            │
    │     v            │
    │   프로젝트 완료   │
    └─────────────────┘

[핵심 원칙]
1. 각 사이클은 위험 해소에 집중
2. 해결되지 않은 위험은 개발 진행 불가
3. 위험이 너무 크면 과감하게 프로젝트 중단/변경
4. 프로토타입은 위험 해소 도구
```

### 4. 핵심 알고리즘/공식 & 실무 코드 예시

#### 나선형 모델 위험 관리 시스템

```python
"""
나선형 모델 위험 관리 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime
import math

class RiskCategory(Enum):
    """위험 카테고리"""
    TECHNICAL = "기술적"
    PERSONNEL = "인적"
    SCHEDULE = "일정"
    BUDGET = "예산"
    EXTERNAL = "외부"
    REQUIREMENTS = "요구사항"

class RiskLevel(Enum):
    """위험 수준"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class MitigationStrategy(Enum):
    """완화 전략"""
    AVOID = "회피"
    TRANSFER = "전가"
    MITIGATE = "완화"
    ACCEPT = "수용"

@dataclass
class Risk:
    """위험 항목"""
    id: str
    name: str
    category: RiskCategory
    description: str
    probability: float  # 0.0 ~ 1.0
    impact: int  # 1 ~ 5
    mitigation_strategy: MitigationStrategy
    mitigation_actions: List[str] = field(default_factory=list)
    status: str = "OPEN"  # OPEN, MITIGATING, RESOLVED, ACCEPTED
    owner: Optional[str] = None

    @property
    def risk_score(self) -> float:
        """위험 점수 = 확률 × 영향도"""
        return self.probability * self.impact

    @property
    def risk_level(self) -> RiskLevel:
        """위험 수준 산정"""
        score = self.risk_score
        if score >= 4.0:
            return RiskLevel.CRITICAL
        elif score >= 2.5:
            return RiskLevel.HIGH
        elif score >= 1.0:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

@dataclass
class SpiralCycle:
    """나선형 사이클"""
    cycle_number: int
    start_date: datetime
    end_date: Optional[datetime] = None
    objectives: List[str] = field(default_factory=list)
    risks_identified: List[Risk] = field(default_factory=list)
    prototype_delivered: bool = False
    increment_delivered: bool = False
    status: str = "PLANNING"  # PLANNING, RISK_ANALYSIS, DEVELOPMENT, COMPLETED

    def add_risk(self, risk: Risk):
        """위험 추가"""
        self.risks_identified.append(risk)

    def get_high_risks(self) -> List[Risk]:
        """고위험 항목 조회"""
        return [r for r in self.risks_identified
                if r.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]

    def can_proceed(self) -> Tuple[bool, List[str]]:
        """개발 진행 가능 여부"""
        blockers = []
        for risk in self.risks_identified:
            if risk.status == "OPEN" and risk.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                blockers.append(f"미해결 {risk.risk_level.value} 위험: {risk.name}")

        return len(blockers) == 0, blockers

class SpiralModelProject:
    """나선형 모델 프로젝트"""

    def __init__(self, name: str):
        self.name = name
        self.cycles: List[SpiralCycle] = []
        self.current_cycle: Optional[SpiralCycle] = None
        self.risk_register: Dict[str, Risk] = {}

    def start_new_cycle(self, objectives: List[str]) -> SpiralCycle:
        """새 사이클 시작"""
        cycle_num = len(self.cycles) + 1
        cycle = SpiralCycle(
            cycle_number=cycle_num,
            start_date=datetime.now(),
            objectives=objectives
        )
        self.cycles.append(cycle)
        self.current_cycle = cycle
        return cycle

    def identify_risk(self, name: str, category: RiskCategory,
                     probability: float, impact: int,
                     strategy: MitigationStrategy) -> Risk:
        """위험 식별 및 등록"""
        risk_id = f"R-{len(self.risk_register)+1:03d}"
        risk = Risk(
            id=risk_id,
            name=name,
            category=category,
            description="",
            probability=probability,
            impact=impact,
            mitigation_strategy=strategy
        )
        self.risk_register[risk_id] = risk
        if self.current_cycle:
            self.current_cycle.add_risk(risk)
        return risk

    def perform_risk_analysis(self) -> Dict:
        """위험 분석 수행"""
        if not self.current_cycle:
            return {"error": "활성 사이클 없음"}

        risks = self.current_cycle.risks_identified
        analysis = {
            "total_risks": len(risks),
            "by_level": {},
            "by_category": {},
            "total_risk_exposure": 0,
            "recommendation": ""
        }

        # 수준별 분류
        for level in RiskLevel:
            count = sum(1 for r in risks if r.risk_level == level)
            analysis["by_level"][level.name] = count

        # 카테고리별 분류
        for cat in RiskCategory:
            count = sum(1 for r in risks if r.category == cat)
            if count > 0:
                analysis["by_category"][cat.value] = count

        # 총 위험 노출 계산
        analysis["total_risk_exposure"] = sum(r.risk_score for r in risks)

        # 권장사항
        critical_count = analysis["by_level"].get("CRITICAL", 0)
        high_count = analysis["by_level"].get("HIGH", 0)

        if critical_count > 0:
            analysis["recommendation"] = f"치명적 위험 {critical_count}개 해결 전까지 개발 불가"
        elif high_count > 2:
            analysis["recommendation"] = f"고위험 {high_count}개 완화 후 개발 권장"
        else:
            analysis["recommendation"] = "개발 진행 가능"

        return analysis

    def resolve_risk(self, risk_id: str, resolution: str) -> bool:
        """위험 해결"""
        risk = self.risk_register.get(risk_id)
        if not risk:
            return False

        risk.status = "RESOLVED"
        risk.mitigation_actions.append(f"해결: {resolution}")
        return True

    def complete_cycle(self, deliverables: List[str]) -> bool:
        """사이클 완료"""
        if not self.current_cycle:
            return False

        can_proceed, blockers = self.current_cycle.can_proceed()
        if not can_proceed:
            print(f"사이클 완료 불가: {blockers}")
            return False

        self.current_cycle.end_date = datetime.now()
        self.current_cycle.status = "COMPLETED"
        self.current_cycle.increment_delivered = True
        return True

    def generate_risk_report(self) -> str:
        """위험 보고서 생성"""
        report = f"""
# 나선형 모델 위험 분석 보고서

## 프로젝트: {self.name}
## 현재 사이클: {self.current_cycle.cycle_number if self.current_cycle else 'N/A'}

### 위험 요약
"""
        total = len(self.risk_register)
        open_risks = sum(1 for r in self.risk_register.values() if r.status == "OPEN")
        resolved = total - open_risks

        report += f"""
- 총 위험 항목: {total}
- 미해결: {open_risks}
- 해결됨: {resolved}

### 위험 상세 목록
"""
        for risk in sorted(self.risk_register.values(),
                          key=lambda r: r.risk_score, reverse=True):
            report += f"""
#### {risk.id}: {risk.name}
- 카테고리: {risk.category.value}
- 확률: {risk.probability:.0%}
- 영향도: {risk.impact}/5
- 위험 점수: {risk.risk_score:.2f}
- 수준: {risk.risk_level.name}
- 완화 전략: {risk.mitigation_strategy.value}
- 상태: {risk.status}
"""

        return report


# 사용 예시
if __name__ == "__main__":
    project = SpiralModelProject("대규모 전자상거래 시스템")

    # Cycle 1 시작
    cycle1 = project.start_new_cycle([
        "핵심 아키텍처 설계",
        "기술 스택 검증",
        "프로토타입 개발"
    ])

    # 위험 식별
    r1 = project.identify_risk(
        "신규 프레임워크 학습 곡선",
        RiskCategory.TECHNICAL,
        0.7, 3,
        MitigationStrategy.MITIGATE
    )
    r1.mitigation_actions = ["프레임워크 교육", "기술 스파이크 수행"]

    r2 = project.identify_risk(
        "핵심 개발자 이직",
        RiskCategory.PERSONNEL,
        0.3, 5,
        MitigationStrategy.MITIGATE
    )
    r2.mitigation_actions = ["지식 공유", "문서화 강화"]

    r3 = project.identify_risk(
        "요구사항 변경 빈번",
        RiskCategory.REQUIREMENTS,
        0.8, 4,
        MitigationStrategy.ACCEPT
    )
    r3.mitigation_actions = ["변경 관리 프로세스", "애자일 방식 도입"]

    # 위험 분석
    analysis = project.perform_risk_analysis()
    print("=== 위험 분석 결과 ===")
    print(f"총 위험: {analysis['total_risks']}")
    print(f"위험 노출: {analysis['total_risk_exposure']:.2f}")
    print(f"권장사항: {analysis['recommendation']}")

    # 위험 해결 시뮬레이션
    project.resolve_risk("R-001", "스파이크 프로젝트로 기술 검증 완료")

    # 사이클 완료
    if project.complete_cycle(["아키텍처 문서", "프로토타입"]):
        print("\nCycle 1 완료!")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 나선형 vs 다른 모델

| 비교 항목 | 나선형 | 폭포수 | 프로토타입 | 애자일 |
| :--- | :--- | :--- | :--- | :--- |
| **위험 관리** | **핵심 활동** | 사후 대응 | 암시적 | 백로그 기반 |
| **반복성** | 있음 | 없음 | 있음 | **핵심** |
| **문서화** | 높음 | 매우 높음 | 중간 | 낮음 |
| **프로토타이핑** | 위험 해소용 | 선택적 | 핵심 활동 | 스파이크 |
| **복잡도** | 높음 | 낮음 | 중간 | 중간 |
| **비용 예측** | 중간 | 높음 | 낮음 | 낮음 |
| **적합 규모** | 대형 | 대형 | 중소형 | 모든 규모 |
| **고객 참여** | 주요 시점 | 시작/끝 | 지속적 | **지속적** |

### 2. 과목 융합 관점 분석

#### 나선형 모델 + 프로젝트 관리 (PMBOK)

```
[나선형 모델과 PMBOK 위험 관리 통합]

PMBOK 위험 관리 프로세스:
1. 위험 관리 계획
2. 위험 식별
3. 정성적 위험 분석
4. 정량적 위험 분석
5. 위험 대응 계획
6. 위험 통제

나선형 모델 매핑:
┌──────────────────────────────────────────────────────┐
│ Q2: 위험 분석 사분면                                  │
│ ├── 위험 식별 (PMBOK 11.2)                           │
│ ├── 정성/정량 분석 (PMBOK 11.3, 11.4)                │
│ ├── 대응 전략 수립 (PMBOK 11.5)                      │
│ └── 프로토타이핑으로 검증                            │
└──────────────────────────────────────────────────────┘

통합 효과:
- 위험 기반 사이클 계획
- 각 사이클 후 위험 재평가
- 위험 예비비(Contingency) 체계적 관리
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오 1] 신기술 도입 대형 프로젝트**

**상황**:
- 프로젝트: AI 기반 추천 시스템 구축
- 규모: 50억 원, 20인, 18개월
- 위험: AI 기술 불확실성, 데이터 품질, 성능 요구사항

**기술사적 판단**:
```
선택: 나선형 모델 + 하이브리드 애자일

근거:
1. AI 기술의 불확실성이 높음
2. 실패 시 비용이 막대함
3. 점진적 검증 필요

사이클 구성:
Cycle 1 (2개월): 기술 검증
  - 위험: "AI 모델이 정확도 90% 달성 가능?"
  - 프로토타입: 소규모 데이터로 검증
  - 결과: 85% 달성 → 추가 개선 필요

Cycle 2 (3개월): 아키텍처 검증
  - 위험: "실시간 추천 100ms 이내 가능?"
  - 프로토타입: 성능 벤치마크
  - 결과: 120ms → 캐싱 전략 추가

Cycle 3-5 (13개월): 기능 구현
  - 나선형 구조 유지하면서 스크럼 운영
  - 위험 중심 우선순위
```

### 2. 도입 시 고려사항 (체크리스트)

**나선형 모델 적합성 체크리스트**:

| 항목 | 예 | 아니오 |
| :--- | :---: | :---: |
| 대규모/고비용 프로젝트인가? | □ | □ |
| 신기술 도입으로 불확실성이 높은가? | □ | □ |
| 실패 시 비용이 매우 큰가? | □ | □ |
| 위험 분석 전문 역량이 있는가? | □ | □ |
| 점진적 개발/인도가 가능한가? | □ | □ |
| 이해관계자가 위험 관리에 동의하는가? | □ | □ |

→ 4개 이상 '예'면 나선형 모델 권장

### 3. 주의사항 및 안티패턴

| 안티패턴 | 설명 | 해결 방안 |
| :--- | :--- | :--- |
| **위험 분석 과잉** | 분석만 하다가 개발 못함 | 분석 시간 제한, 타임박스 |
| **나선 무한 순환** | 사이클만 반복하다 종료 못함 | 최대 사이클 수 제한 |
| **프로토타입 오용** | 프로토타입을 제품으로 | 폐기 원칙 명확화 |
| **전문가 의존** | 위험 분석가 1인 의존 | 팀 기반 위험 분석 |

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | 일반 프로젝트 | 나선형 적용 | 개선 효과 |
| :--- | :--- | :--- | :--- | :--- |
| **프로젝트 실패** | 실패율 | 25% | 10% | -15%p |
| **위험 발견** | 조기 발견률 | 30% | 80% | +50%p |
| **재작업** | 비용 비중 | 40% | 15% | -25%p |
| **예측성** | 일정 준수율 | 50% | 75% | +25%p |

### 2. 미래 전망 및 진화 방향

1. **AI 기반 위험 예측**
   - 머신러닝으로 위험 자동 식별
   - 프로젝트 데이터 기반 위험 예측

2. **애자일과의 하이브리드**
   - SAFe, LeSS에 위험 관리 통합
   - 스파이크를 위험 해소 도구로 활용

3. **실시간 위험 대시보드**
   - 지속적 위험 모니터링
   - 자동 알림 및 대응 추천

### ※ 참고 표준/가이드

- **IEEE 12207**: 소프트웨어 생명주기 프로세스
- **PMBOK 7th**: 위험 관리 지식 영역
- **ISO 31000**: 위험 관리 원칙 및 가이드라인
- **SEI CMMI**: 위험 관리 프로세스 영역

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [SDLC](@/studynotes/4_software_engineering/1_sdlc/3_sdlc.md) : 나선형 모델의 상위 개념
- [폭포수 모델](@/studynotes/4_software_engineering/1_sdlc/4_waterfall_model.md) : 나선형의 기반 구조
- [프로토타입 모델](@/studynotes/4_software_engineering/1_sdlc/6_prototype_model.md) : 위험 해소 도구
- [애자일](@/studynotes/4_software_engineering/1_sdlc/agile_methodology.md) : 현대적 적응
- [위험 관리](@/studynotes/4_software_engineering/8_project/_index.md) : 나선형의 핵심 활동
- [프로젝트 관리](@/studynotes/4_software_engineering/8_project/_index.md) : 위험 관리 영역

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 정글을 탐험하러 가는데, 무작정 들어갔다가 낭떠러지를 만나면 큰일이에요! 미리 알았으면 다른 길로 갔을 텐데 말이죠.

2. **해결(나선형 모델)**: 먼저 지도를 보고 "여기 낭떠러지가 있을 수 있어!"라고 위험을 찾아요. 그리고 조금만 가서 확인해요. 정말 위험하면 다른 길로, 괜찮으면 조금 더 가요. 이렇게 한 바퀴 돌고, 또 돌고 하면서 목표까지 가는 거예요!

3. **효과**: 이렇게 하면 갑자기 큰 위험을 만나서 "망했어요!" 하는 일이 없어요. 컴퓨터 프로그램을 만들 때도 먼저 "이게 잘 될까?"를 확인하고, 조금씩 만들어가면 실패하지 않아요!
