+++
title = "41. 위험 관리 (Risk Management) 4단계"
description = "프로젝트 리스크를 식별, 분석, 대응, 모니터링하는 체계적 프로세스, 프로젝트 성공의 핵심 보험"
date = "2026-03-05"
[taxonomies]
tags = ["risk-management", "identification", "analysis", "response", "monitoring"]
categories = ["studynotes-4_software_engineering"]
+++

# 41. 위험 관리 (Risk Management) 4단계

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 위험 관리는 프로젝트 수행 중 발생 가능한 **불확실성을 체계적으로 식별, 분석, 대응, 모니터링**하여 프로젝트 목표 달성을 위협하는 요소를 **사전에 예방하거나 영향을 최소화**하는 관리 프로세스입니다.
> 2. **가치**: 체계적 위험 관리 적용 시 **프로젝트 성공률 30% 향상, 예기치 못한 이슈 50% 감소, 위기 대응 시간 60% 단축** 효과가 있으며, 특히 대형/고위험 프로젝트에서는 필수적입니다.
> 3. **융합**: PMBOK 10대 지식 영역 중 하나이며, **SWOT 분석, FMEA, Monte Carlo 시뮬레이션, 카오스 엔지니어링** 등 다양한 기법과 결합됩니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**위험(Risk)**이란 프로젝트 목표에 **부정적 영향을 미칠 수 있는 불확실한 사건**으로, **발생 확률(Probability)**과 **영향도(Impact)**의 함수입니다. **위험 관리(Risk Management)**는 이러한 위험을 체계적으로 관리하는 프로세스입니다.

**위험 관리 4단계 (PMBOK 기준)**:

| 단계 | 명칭 | 핵심 활동 | 산출물 |
|:---:|:---|:---|:---|
| **1** | **식별 (Identify)** | 어떤 위험이 있는가? | 위험 등록부 (Risk Register) |
| **2** | **분석 (Analyze)** | 얼마나 위험한가? | 위험 우선순위 |
| **3** | **대응 (Response)** | 어떻게 대처할 것인가? | 위험 대응 계획 |
| **4** | **모니터링 (Monitor)** | 잘 관리되고 있는가? | 위험 상태 보고서 |

**위험 vs 이슈**:

| 구분 | 위험 (Risk) | 이슈 (Issue) |
|:---|:---|:---|
| **시제** | 미래 (아직 안 일어남) | 현재 (이미 발생) |
| **확률** | 0~100% | 100% |
| **대응** | 예방, 완화 | 해결, 수용 |
| **비용** | 낮음 (사전 대응) | 높음 (사후 대응) |

### 2. 비유: 자동차 보험과 안전 운전

```
[위험 관리 = 자동차 안전 시스템]

위험 관리 4단계                     자동차 안전
─────────────────                 ─────────────────

1. 식별 (Identify)                 미리 알아보기
"사고 날 수 있는 상황?"      →    "빙판길, 졸음운전, 고속도로"
                                  (위험 요소 파악)

2. 분석 (Analyze)                  확률과 영향 계산
"얼마나 위험해?"              →    "겨울철 빙판길: 30%, 사고 시 치명적"
                                  (위험도 평가)

3. 대응 (Response)                 대비하기
"어떻게 막을까?"              →    • 회피: "오늘 운전 안 할래"
                                  • 완화: "스노우 타이어 끼자"
                                  • 전가: "보험 들자"
                                  • 수용: "조심해서 운전하자"

4. 모니터링 (Monitor)              지속 확인
"잘 되고 있어?"               →    • 주행 중 도로 상황 체크
                                  • 정기 점검
                                  • 보험 갱신

──────────────────────────────────────────────────────
교훈:
• 사고 나고 나서 "보험 들걸" 후회 X
• 프로젝트도 위험 발생 전에 미리 대비
• 위험 관리 = 프로젝트 보험
```

### 3. 등장 배경 및 발전 과정

**1) 1950~60년대: 방위/우주 산업에서 시작**
- 미 국방성, NASA의 대형 프로젝트
- 실패 비용이 막대 → 사전 위험 관리 필요

**2) 1987년: PMBOK 초판**
- 위험 관리를 별도 지식 영역으로 정식 편입

**3) 1990년대: 소프트웨어 위험 관리**
- SEI(Software Engineering Institute)의 위험 관리 모델
- "Risk Management is Project Management for Adults" (Tom DeMarco)

**4) 2000년대~현재: 애자일과 통합**
- 스크럼: 스프린트 리뷰에서 위험 식별
- 린: "실패 빨리 배우기" (Fail Fast)
- 카오스 엔지니어링: 의도적 위험 유발

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 위험 관리 프로세스 다이어그램

```
================================================================================
|                    RISK MANAGEMENT PROCESS (4 STEPS)                          |
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                        STEP 1: IDENTIFY RISKS                            │
    │                           (위험 식별)                                    │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  기법:                                                          │   │
    │  │  • 브레인스토밍 (Brainstorming)                                   │   │
    │  │  • 체크리스트 (Checklist)                                        │   │
    │  │  • 인터뷰 (Expert Interviews)                                    │   │
    │  │  • SWOT 분석                                                    │   │
    │  │  • 가정 분석 (Assumption Analysis)                               │   │
    │  │  • 과거 프로젝트 교훈 (Lessons Learned)                           │   │
    │  │                                                                  │   │
    │  │  질문:                                                           │   │
    │  │  • 무엇이 잘못될 수 있는가?                                       │   │
    │  │  • 어떤 가정이 틀릴 수 있는가?                                    │   │
    │  │  • 외부 환경에서 어떤 변화가 올 수 있는가?                         │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                              │                                         │
    │                              v                                         │
    │  산출물: 위험 등록부 (Risk Register)                                   │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  ID | 위험명 | 카테고리 | 발생 확률 | 영향도 | 점수 | 대응전략    │   │
    │  │  R1 | 일정지연 | 일정 | 중간 | 높음 | 12 | 완화                  │   │
    │  │  R2 | 핵심인력이직 | 자원 | 낮음 | 매우높음 | 10 | 전가          │   │
    │  │  R3 | 요구사항변경 | 범위 | 높음 | 중간 | 12 | 수용              │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────────┘
                                       │
                                       v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                        STEP 2: ANALYZE RISKS                             │
    │                           (위험 분석)                                    │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  정성적 분석 (Qualitative):                                      │   │
    │  │  • 확률 × 영향도 매트릭스 (Probability-Impact Matrix)             │   │
    │  │  • 등급: 높음/중간/낮음 (High/Medium/Low)                         │   │
    │  │  • 위험 점수 = 확률 × 영향도                                      │   │
    │  │                                                                  │   │
    │  │  정량적 분석 (Quantitative):                                     │   │
    │  │  • 몬테카를로 시뮬레이션                                         │   │
    │  │  • 의사결정 트리 (Decision Tree)                                 │   │
    │  │  • 민감도 분석 (Sensitivity Analysis)                            │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                              │                                         │
    │                              v                                         │
    │  산출물: 우선순위 위험 목록 (Prioritized Risk List)                    │
    └─────────────────────────────────────────────────────────────────────────┘
                                       │
                                       v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                       STEP 3: RESPONSE TO RISKS                          │
    │                          (위험 대응)                                     │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  4가지 대응 전략:                                                │   │
    │  │                                                                  │   │
    │  │  1. 회피 (Avoid)     - 위험 제거                                 │   │
    │  │     "그 기능을 아예 빼자"                                         │   │
    │  │                                                                  │   │
    │  │  2. 전가 (Transfer)  - 제3자에게 책임 이전                        │   │
    │  │     "외주 주자 / 보험 들자"                                       │   │
    │  │                                                                  │   │
    │  │  3. 완화 (Mitigate)  - 확률 또는 영향 감소                        │   │
    │  │     "프로토타입으로 미리 검증하자"                                 │   │
    │  │                                                                  │   │
    │  │  4. 수용 (Accept)    - 감수                                      │   │
    │  │     "발생하면 그때 대처하자" (비상계획 Contingency)               │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                              │                                         │
    │                              v                                         │
    │  산출물: 위험 대응 계획 (Risk Response Plan)                           │
    └─────────────────────────────────────────────────────────────────────────┘
                                       │
                                       v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                     STEP 4: MONITOR & CONTROL                            │
    │                        (모니터링 및 통제)                                 │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │  활동:                                                          │   │
    │  │  • 위험 재평가 (Risk Reassessment)                               │   │
    │  │  • 위험 감사 (Risk Audit)                                        │   │
    │  │  • 위험 대응 효과성 검토                                          │   │
    │  │  • 신규 위험 식별                                                 │   │
    │  │  • 위험 보고서 작성                                               │   │
    │  │                                                                  │   │
    │  │  도구:                                                           │   │
    │  │  • 위험 대시보드 (Risk Dashboard)                                 │   │
    │  │  • 위험 벌레(Burndown) 차트                                       │   │
    │  │  • KRI (Key Risk Indicators)                                     │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
```

### 2. 확률-영향도 매트릭스 (Probability-Impact Matrix)

```
================================================================================
|                PROBABILITY-IMPACT MATRIX (위험 우선순위 매트릭스)              |
================================================================================

                        영 향 도 (Impact)
              ┌────────────────────────────────────────────┐
              │  1    2    3    4    5                    │
              │ 낮음      보통       높음                 │
         ┌────┼────────────────────────────────────────────┤
         │ 5  │  5   10   15   20   25  ████████████ 높음  │
    확   │    │                                          │
    률   │ 4  │  4    8   12   16   20  ████████████ 높음  │
         │    │                                          │
   (P)   │ 3  │  3    6    9   12   15  ██████ 중간       │
         │    │                                          │
         │ 2  │  2    4    6    8   10  ████ 중간         │
         │    │                                          │
         │ 1  │  1    2    3    4    5  ██ 낮음           │
         └────┴────────────────────────────────────────────┘

    점수 = 확률 × 영향도

    등급 기준 (예시):
    ┌─────────────────────────────────────────┐
    │  15~25: 높음 (High)     - 즉시 대응     │
    │   9~14: 중간 (Medium)   - 계획적 대응   │
    │    1~8: 낮음 (Low)      - 수용/모니터링 │
    └─────────────────────────────────────────┘

    ─────────────────────────────────────────────────────────────────────────

    예시 적용:

    R1: 핵심 개발자 이직
        확률: 4 (높음 - 채용 시장 어려움)
        영향도: 5 (매우 높음 - 핵심 기술 보유)
        점수: 4 × 5 = 20 → 높음 ★

    R2: 새로운 기술 스택 도입 실패
        확률: 3 (보통)
        영향도: 4 (높음)
        점수: 3 × 4 = 12 → 중간

    R3: 사소한 UI 버그
        확률: 4 (높음)
        영향도: 1 (낮음)
        점수: 4 × 1 = 4 → 낮음

================================================================================
```

### 3. 4가지 대응 전략 상세

```
================================================================================
|                    4 RISK RESPONSE STRATEGIES                                 |
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  1. 회피 (AVOID) - 위험 원천 제거                                        │
    │  ─────────────────────────────────────────────────────────────────────  │
    │  전략: 위험을 완전히 없앰                                                │
    │  방법:                                                                  │
    │  • 프로젝트 범위 변경                                                   │
    │  • 일정 조정                                                            │
    │  • 기술 변경                                                            │
    │  • 자원 추가                                                            │
    │                                                                         │
    │  예시:                                                                  │
    │  위험: "새로운 AI 기술 적용 실패 가능성"                                 │
    │  회피: "AI 기능을 다음 버전으로 미루고, 기존 기술 사용"                  │
    │                                                                         │
    │  비용: 높음 (범위 축소, 일정 지연)                                       │
    │  효과: 100% (위험 제거)                                                 │
    └─────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  2. 전가 (TRANSFER) - 제3자에게 위험 이전                                │
    │  ─────────────────────────────────────────────────────────────────────  │
    │  전략: 위험의 소유권과 책임을 제3자에게 이전                             │
    │  방법:                                                                  │
    │  • 보험 가입                                                            │
    │  • 외주 (Outsourcing)                                                   │
    │  • 계약상 면책 조항                                                      │
    │  • SLA (서비스 수준 협약)                                                │
    │                                                                         │
    │  예시:                                                                  │
    │  위험: "서버 장애로 인한 서비스 중단"                                    │
    │  전가: "AWS에 호스팅하고 SLA 99.9% 보장받음"                            │
    │                                                                         │
    │  비용: 중간 (보험료, 외주비)                                            │
    │  효과: 높음 (책임 이전)                                                 │
    └─────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  3. 완화 (MITIGATE) - 확률 또는 영향 감소                                │
    │  ─────────────────────────────────────────────────────────────────────  │
    │  전략: 위험 발생 확률 또는 영향도를 낮춤                                 │
    │  방법:                                                                  │
    │  • 프로토타이핑                                                          │
    │  • 파일럿 프로젝트                                                       │
    │  • 교육 및 역량 강화                                                     │
    │  • 중복 설계 (Redundancy)                                                │
    │  • 단계적 론칭                                                           │
    │                                                                         │
    │  예시:                                                                  │
    │  위험: "성능 목표 미달"                                                  │
    │  완화: "초기부터 성능 테스트, 카나리 배포로 점진적 확대"                 │
    │                                                                         │
    │  비용: 중간                                                              │
    │  효과: 높음 (확률/영향 감소)                                            │
    └─────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  4. 수용 (ACCEPT) - 위험 감수                                            │
    │  ─────────────────────────────────────────────────────────────────────  │
    │  전략: 위험을 감수하고 발생 시 대응                                      │
    │  방법:                                                                  │
    │  • 능동적 수용: 비상 계획(Contingency Plan) 수립                         │
    │  • 수동적 수용: 별도 대응 없이 발생 시 대처                              │
    │  • 예비금(Reserve) 확보                                                 │
    │                                                                         │
    │  예시:                                                                  │
    │  위험: "사소한 UI 버그 다수 발생"                                        │
    │  수용: "버그가 발생하면 우선순위에 따라 수정 (예비 인원 1명 할당)"       │
    │                                                                         │
    │  비용: 낮음 (발생 전) → 높음 (발생 후)                                  │
    │  효과: 낮음 (위험 그대로 존재)                                          │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
```

### 4. 핵심 코드: 위험 관리 시스템

```python
"""
Risk Management System
위험 관리 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class RiskCategory(Enum):
    TECHNICAL = "기술"
    SCHEDULE = "일정"
    COST = "비용"
    SCOPE = "범위"
    RESOURCE = "자원"
    EXTERNAL = "외부"
    ORGANIZATIONAL = "조직"

class RiskLevel(Enum):
    LOW = "낮음"
    MEDIUM = "중간"
    HIGH = "높음"

class ResponseStrategy(Enum):
    AVOID = "회피"
    TRANSFER = "전가"
    MITIGATE = "완화"
    ACCEPT = "수용"

@dataclass
class Risk:
    """위험 정의"""
    risk_id: str
    name: str
    description: str
    category: RiskCategory
    probability: int  # 1-5
    impact: int  # 1-5
    response_strategy: ResponseStrategy
    response_plan: str
    owner: str
    status: str = "Open"  # Open, Closed, Occurred
    contingency_plan: str = ""
    trigger: str = ""  # 위험 발생 조건
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)

    @property
    def score(self) -> int:
        """위험 점수"""
        return self.probability * self.impact

    @property
    def level(self) -> RiskLevel:
        """위험 등급"""
        score = self.score
        if score >= 15:
            return RiskLevel.HIGH
        elif score >= 9:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

@dataclass
class RiskRegister:
    """위험 등록부"""
    project_name: str
    risks: Dict[str, Risk] = field(default_factory=dict)

    def add_risk(self, risk: Risk):
        """위험 추가"""
        self.risks[risk.risk_id] = risk

    def get_prioritized_risks(self) -> List[Risk]:
        """우선순위 정렬된 위험 목록"""
        return sorted(self.risks.values(), key=lambda r: r.score, reverse=True)

    def get_risks_by_level(self, level: RiskLevel) -> List[Risk]:
        """등급별 위험 목록"""
        return [r for r in self.risks.values() if r.level == level]

    def get_risks_by_category(self, category: RiskCategory) -> List[Risk]:
        """카테고리별 위험 목록"""
        return [r for r in self.risks.values() if r.category == category]

    def get_risk_statistics(self) -> Dict:
        """위험 통계"""
        total = len(self.risks)
        if total == 0:
            return {"total": 0}

        high = len(self.get_risks_by_level(RiskLevel.HIGH))
        medium = len(self.get_risks_by_level(RiskLevel.MEDIUM))
        low = len(self.get_risks_by_level(RiskLevel.LOW))

        return {
            "total": total,
            "high": high,
            "medium": medium,
            "low": low,
            "high_percentage": round(high / total * 100, 1),
            "avg_score": round(sum(r.score for r in self.risks.values()) / total, 1),
            "by_category": {
                cat.value: len(self.get_risks_by_category(cat))
                for cat in RiskCategory
            }
        }

    def generate_report(self) -> str:
        """위험 보고서 생성"""
        stats = self.get_risk_statistics()

        report = [
            f"\n{'='*80}",
            f"위험 관리 보고서 - {self.project_name}",
            f"{'='*80}",
            f"\n[요약]",
            f"  총 위험 수: {stats['total']}개",
            f"  높음: {stats['high']}개 ({stats['high_percentage']}%)",
            f"  중간: {stats['medium']}개",
            f"  낮음: {stats['low']}개",
            f"  평균 점수: {stats['avg_score']}",
            f"\n[카테고리별]",
        ]

        for cat, count in stats['by_category'].items():
            if count > 0:
                report.append(f"  • {cat}: {count}개")

        report.extend([
            f"\n[우선순위 TOP 5]",
            f"{'ID':<8} {'위험명':<30} {'점수':>6} {'등급':>6} {'대응':>8}",
            "-"*80,
        ])

        for risk in self.get_prioritized_risks()[:5]:
            report.append(
                f"{risk.risk_id:<8} {risk.name:<30} {risk.score:>6} "
                f"{risk.level.value:>6} {risk.response_strategy.value:>8}"
            )

        report.append("="*80)

        return "\n".join(report)


# 사용 예시
if __name__ == "__main__":
    register = RiskRegister("웹 애플리케이션 개발 프로젝트")

    # 위험 등록
    risks = [
        Risk(
            risk_id="R001",
            name="핵심 개발자 이직",
            description="프로젝트 핵심 개발자가 이직하여 지식 유실",
            category=RiskCategory.RESOURCE,
            probability=4,
            impact=5,
            response_strategy=ResponseStrategy.MITIGATE,
            response_plan="지식 공유 세션, 문서화, 백업 인력 양성",
            owner="PM",
            trigger="개발자 휴가/이직 징후"
        ),
        Risk(
            risk_id="R002",
            name="요구사항 잦은 변경",
            description="고객의 요구사항이 지속적으로 변경됨",
            category=RiskCategory.SCOPE,
            probability=5,
            impact=4,
            response_strategy=ResponseStrategy.ACCEPT,
            response_plan="변경 관리 프로세스 적용, 일정 버퍼 확보",
            owner="PO",
            contingency_plan="요구사항 변경 10%까지 수용"
        ),
        Risk(
            risk_id="R003",
            name="신규 기술 도입 실패",
            description="새로운 프레임워크 도입 시 기술적 난관",
            category=RiskCategory.TECHNICAL,
            probability=3,
            impact=4,
            response_strategy=ResponseStrategy.MITIGATE,
            response_plan="프로토타입 검증, 기술 스파이크 수행",
            owner="아키텍트",
            trigger="기술 검토 결과 부적합"
        ),
        Risk(
            risk_id="R004",
            name="서버 장애",
            description="운영 서버 다운으로 서비스 중단",
            category=RiskCategory.TECHNICAL,
            probability=2,
            impact=5,
            response_strategy=ResponseStrategy.TRANSFER,
            response_plan="AWS 클라우드 이관, SLA 99.9% 계약",
            owner="운영팀"
        ),
        Risk(
            risk_id="R005",
            name="일정 지연",
            description="개발 일정이 계획보다 지연됨",
            category=RiskCategory.SCHEDULE,
            probability=4,
            impact=3,
            response_strategy=ResponseStrategy.MITIGATE,
            response_plan="주간 진척 점검, 위험 작업 조기 식별",
            owner="PM"
        ),
    ]

    for risk in risks:
        register.add_risk(risk)

    print(register.generate_report())
```

---

## III. 융합 비교 및 다각도 분석

### 1. 심층 기술 비교: 위험 분석 기법

| 기법 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| **P-I 매트릭스** | 확률×영향도 | 간단, 직관 | 주관적 |
| **FMEA** | 고장 모드 분석 | 체계적 | 시간 소요 |
| **SWOT** | 강약기위 분석 | 전략적 | 정성적 |
| **Monte Carlo** | 확률 시뮬레이션 | 정량적 | 복잡 |
| **Decision Tree** | 의사결정 경로 | 시각적 | 단순화 |

### 2. 과목 융합: 위험 관리 + 애자일

```
[애자일에서의 위험 관리]

스크럼 이벤트와 위험 관리 연계:
────────────────────────────────────────────────────────────────────
스프린트 계획    →    위험 식별 (새 스프린트 위험)
데일리 스탠드업  →    위험 모니터링 (장애물 = 위험)
스프린트 리뷰    →    위험 재평가 (데모 중 발견)
스프린트 회고    →    위험 교훈 (Lessons Learned)

애자일 특화 위험:
────────────────────────────────────────────────────────────────────
• 사용자 참여 부족
• 백로그 관리 실패
• 스프린트 범위 크리프
• 기술 부채 누적
• 팀 번아웃

대응:
────────────────────────────────────────────────────────────────────
• "Fail Fast" - 빨리 실패하고 빨리 배운다
• "Inspect & Adapt" - 지속적 검사와 적응
• Spike - 불확실성 해소를 위한 짧은 탐색
```

---

## IV. 실무 적용 및 기술사적 판단

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오] 금융 시스템 고위험 프로젝트**

*   **상황**:
    - 핵심 뱅킹 시스템 교체
    - 규제: 금융감독원 감사 대상
    - 위험도: 매우 높음

*   **기술사적 판단**: **적극적 위험 관리 (Proactive Risk Management)**

*   **실행 전략**:
    ```
    1. 위험 식별 (프로젝트 착수 전):
       - 외부 컨설턴트 참여
       - 과거 유사 프로젝트 교훈 수집
       - 체크리스트 100+ 항목

    2. 정량적 분석:
       - Monte Carlo 시뮬레이션
       - "95% 확률로 18~24개월 소요"

    3. 다층 대응:
       - 높음 위험: 회피/완화 + 예비금 20%
       - 중간 위험: 완화 + 비상계획
       - 낮음 위험: 수용

    4. 지속 모니터링:
       - 주간 위험 위원회
       - 월간 이사회 보고
    ```

### 2. 도입 시 고려사항

**조직적 고려**:
- [ ] 위험 관리 문화 (Risk-Aware Culture)
- [ ] 경영진 지원 (Management Commitment)
- [ ] 전담 조직 (Risk Management Office)

**기술적 고려**:
- [ ] 위험 등록부 도구 (Jira, Excel, 전용 도구)
- [ ] 분석 도구 (Monte Carlo 소프트웨어)
- [ ] 대시보드 (실시간 모니터링)

### 3. 주의사항

*   **분석 마비 (Analysis Paralysis)**:
    - 너무 많은 위험 식별 → 관리 불가
    - 해결: 상위 10개 위험에 집중

*   **형식적 관리 (Paper-Based)**:
    - 위험 등록부만 있고 대응 없음
    - 해결: 위험 대응을 작업 항목으로 전환

---

## V. 기대효과 및 결론

### 1. 정량적/정성적 기대효과

| 구분 | 효과 내용 | 기대 수치 |
|:---:|:---|:---|
| **성공률** | 프로젝트 성공 확률 | 30% 향상 |
| **대응 속도** | 위기 대응 시간 | 60% 단축 |
| **비용** | 예기치 못한 비용 | 40% 감소 |
| **신뢰** | 이해관계자 신뢰 | 향상 |

### 2. 미래 전망

1.  **AI 기반 위험 예측**: 머신러닝으로 위험 조기 경보
2.  **실시간 위험 대시보드**: IoT 센서와 연동
3.  **카오스 엔지니어링**: 의도적 위험 유발로 검증

### 3. 참고 표준

*   **PMBOK Guide**: Risk Management Knowledge Area
*   **ISO 31000**: Risk Management 표준
*   **IEEE 1540**: Software Life Cycle Processes - Risk Management

---

## 관련 개념 맵 (Knowledge Graph)

*   [PMBOK](@/studynotes/4_software_engineering/3_project/_index.md) : 위험 관리 지식 영역
*   [프로젝트 관리](@/studynotes/4_software_engineering/3_project/_index.md) : 전체 프로젝트 관리 체계
*   [EVM](@/studynotes/4_software_engineering/3_project/project_management_evm.md) : 성과 측정과 위험 연계

---

## 어린이를 위한 3줄 비유 설명

1. **문제**: 소풍 가는데 비가 올까 봐 걱정돼요.

2. **해결(위험 관리)**: **미리 준비해요!**
   - 식별: "비가 올 수도 있어"
   - 분석: "날씨 앱 보니 30% 확률이야"
   - 대응: "우산 챙기자!" (완화)
   - 모니터링: "아침에 날씨 다시 확인하자"

3. **효과**: 비가 와도 우산이 있어서 소풍을 즐길 수 있어요! 준비 안 한 친구들은 다 젖었는데 말이죠.
