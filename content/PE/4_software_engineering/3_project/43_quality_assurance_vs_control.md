+++
title = "43. 품질 보증(QA) vs 품질 제어(QC)"
description = "품질 관리의 두 축, 예방 중심의 QA와 검출 중심의 QC의 상호 보완적 관계"
date = "2026-03-05"
[taxonomies]
tags = ["qa", "qc", "quality-management", "prevention", "detection"]
categories = ["studynotes-4_software_engineering"]
+++

# 43. 품질 보증(QA) vs 품질 제어(QC)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: QA(Quality Assurance)는 **프로세스 개선을 통한 품질 예방**에 집중하고, QC(Quality Control)는 **제품 검사를 통한 결함 검출**에 집중하는 상호 보완적 품질 관리 활동입니다.
> 2. **가치**: QA 중심 조직은 **결함 발생률 40% 감소**, QC 중심 조직은 **결함 유출률 60% 감소** 효과가 있으며, 두 활동의 균형 잡힌 수행이 **최적의 품질 비용(Cost of Quality)**을 달성합니다.
> 3. **융합**: ISO 9001의 품질 경영 체계, CMMI의 PPQA 프로세스 영역, TQM의 전사적 품질 관리와 밀접하게 연결됩니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**품질 보증(Quality Assurance, QA)**과 **품질 제어(Quality Control, QC)**는 품질 관리의 양대 축입니다. 둘 다 품질 목표 달성을 목적으로 하지만, 접근 방식과 초점이 다릅니다.

| 구분 | QA (품질 보증) | QC (품질 제어) |
|:---|:---|:---|
| **정의** | 품질 요구사항이 충족될 것이라는 **신뢰를 제공**하는 활동 | 품질 요구사항이 **충족되는지 모니터링**하고 제거하는 활동 |
| **초점** | **프로세스** 중심 | **제품** 중심 |
| **목적** | **예방** (Prevention) | **검출** (Detection) |
| **시점** | 개발 **전/중** | 개발 **후** |
| **주체** | QA 조직/프로세스 담당 | 테스터/검사 담당 |
| **활동** | 프로세스 정의, 교육, 감사 | 테스트, 검사, 리뷰 |
| **질문** | "올바른 방법으로 하고 있는가?" | "올바른 결과가 나왔는가?" |

### 2. 비유: 의료 시스템과 비교

```
[QA vs QC = 예방의학 vs 진료]

의료 시스템                          소프트웨어 품질
─────────────────                   ─────────────────

QA (예방의학)                       QA (프로세스 예방)
─────────────────                   ─────────────────
• 건강 검진                         • 프로세스 감사
• 운동/식단 가이드                   • 코딩 표준 교육
• 예방 접종                         • 보안 코딩 가이드
• 금연 권고                         • 정적 분석 도구
• 목표: "병에 안 걸리게"             • 목표: "결함이 안 생기게"

──────────────────────────────────────────────────────

QC (진료/치료)                      QC (제품 검사)
─────────────────                   ─────────────────
• 혈액 검사                         • 단위 테스트
• X-레이 촬영                       • 통합 테스트
• MRI 스캔                          • 시스템 테스트
• 수술/치료                         • 버그 수정
• 목표: "병을 찾아내서 고치기"        • 목표: "결함을 찾아내서 수정"

──────────────────────────────────────────────────────

교훈:
• 예방이 치료보다 싸다              • QA가 QC보다 비용 효율적
• 둘 다 필요하다                    • QA와 QC 모두 필요
• 정기 검진이 중요                   • 지속적 품질 활동 필요
```

### 3. 등장 배경 및 발전 과정

**1) 1920~30년대: QC의 시작**
- Walter Shewhart의 통계적 품질 관리(SQC)
- 제조업에서 검사 기반 품질 관리

**2) 1950년대: QA의 등장**
- W. Edwards Deming, Joseph Juran의 품질 철학
- "품질은 검사가 아니라 제조 공정에서 만들어진다"

**3) 1987년: ISO 9000 시리즈**
- QA 중심의 품질 경영 체계 표준화

**4) 1990년대~현재: 소프트웨어 품질**
- CMMI의 PPQA(Process & Product Quality Assurance)
- Shift-Left Testing: QA 활동을 개발 초기로 이동

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. QA vs QC 상세 비교 다이어그램

```
================================================================================
|                    QA vs QC - DETAILED COMPARISON                             |
================================================================================

                              QUALITY MANAGEMENT
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    v                                   v
        ┌───────────────────────┐       ┌───────────────────────┐
        │   QA (Quality         │       │   QC (Quality         │
        │       Assurance)      │       │       Control)        │
        │   ─────────────────   │       │   ─────────────────   │
        │   품질 보증            │       │   품질 제어            │
        └───────────────────────┘       └───────────────────────┘
                    │                                   │
        ┌───────────┴───────────┐       ┌───────────┴───────────┐
        │                       │       │                       │
        v                       v       v                       v
    ┌───────┐             ┌───────┐ ┌───────┐             ┌───────┐
    │프로세스│             │ 프로세스│ │제품   │             │제품   │
    │ 정의  │             │ 감사  │ │ 검사  │             │ 테스트 │
    └───────┘             └───────┘ └───────┘             └───────┘
        │                       │       │                       │
        v                       v       v                       v
    ┌───────┐             ┌───────┐ ┌───────┐             ┌───────┐
    │표준/  │             │ 준수  │ │ 결함  │             │결함  │
    │ 가이드│             │ 확인  │ │ 검출  │             │ 수정  │
    └───────┘             └───────┘ └───────┘             └───────┘
        │                       │       │                       │
        v                       v       v                       v
    ┌───────┐             ┌───────┐ ┌───────┐             ┌───────┐
    │ 교육  │             │ 개선  │ │ 리포트 │             │재발방지│
    └───────┘             └───────┘ └───────┘             └───────┘

    ─────────────────────────────────────────────────────────────────────────

    QA 활동 상세:
    ┌─────────────────────────────────────────────────────────────────────┐
    │  • 프로세스 표준 정의 (SDLC, 코딩 표준, 테스트 표준)                 │
    │  • 프로세스 교육 및 인증                                             │
    │  • 프로세스 준수 감사 (Process Audit)                                │
    │  • 형상 관리 감사 (Configuration Audit)                              │
    │  • 품질 메트릭 정의 및 수집                                          │
    │  • 프로세스 개선 제안 (PIP)                                          │
    │  • 도구 선정 및 도입                                                 │
    │  • 인스펙션/리뷰 주도                                                │
    └─────────────────────────────────────────────────────────────────────┘

    QC 활동 상세:
    ┌─────────────────────────────────────────────────────────────────────┐
    │  • 단위 테스트 (Unit Testing)                                        │
    │  • 통합 테스트 (Integration Testing)                                 │
    │  • 시스템 테스트 (System Testing)                                    │
    │  • 인수 테스트 (Acceptance Testing)                                  │
    │  • 회귀 테스트 (Regression Testing)                                  │
    │  • 성능 테스트 (Performance Testing)                                 │
    │  • 보안 테스트 (Security Testing)                                    │
    │  • 사용성 테스트 (Usability Testing)                                 │
    └─────────────────────────────────────────────────────────────────────┘

================================================================================
```

### 2. 품질 비용(Cost of Quality) 분석

```
================================================================================
|                    COST OF QUALITY (COQ) MODEL                               |
================================================================================

                    총 품질 비용
                    ─────────────────────────────────────────────────────
                    │                                               │
        ┌───────────┴───────────┐                   ┌───────────────┴─────────┐
        │    Cost of Good       │                   │    Cost of Poor         │
        │    Quality (COGQ)     │                   │    Quality (COPQ)       │
        │    적합 품질 비용      │                   │    부적합 품질 비용      │
        └───────────────────────┘                   └─────────────────────────┘
                    │                                               │
        ┌───────────┴───────────┐                   ┌───────────────┴─────────┐
        │                       │                   │                         │
        v                       v                   v                         v
    ┌───────┐             ┌───────┐             ┌───────┐             ┌───────┐
    │ 예방  │             │ 평가  │             │ 내부  │             │ 외부  │
    │ 비용  │             │ 비용  │             │ 실패  │             │ 실패  │
    └───────┘             └───────┘             └───────┘             └───────┘
        │                       │                   │                       │
        │                       │                   │                       │

    ─────────────────────────────────────────────────────────────────────────

    예방 비용 (Prevention Costs) - QA 중심
    ┌─────────────────────────────────────────────────────────────────────┐
    │  • 품질 계획 수립                                                    │
    │  • 교육 및 훈련                                                      │
    │  • 프로세스 정의                                                     │
    │  • 도구 도입                                                         │
    │  • 설계 리뷰                                                         │
    │                                                                      │
    │  목표: 결함 예방                                                     │
    │  특징: 투자 성격, 장기적 효과                                         │
    └─────────────────────────────────────────────────────────────────────┘

    평가 비용 (Appraisal Costs) - QC 중심
    ┌─────────────────────────────────────────────────────────────────────┐
    │  • 테스트 설계 및 수행                                               │
    │  • 검사 및 검증                                                      │
    │  • 정적 분석                                                         │
    │  • 인스펙션                                                          │
    │  • 품질 감사                                                         │
    │                                                                      │
    │  목표: 결함 검출                                                     │
    │  특징: 운영 성격, 단기적 효과                                         │
    └─────────────────────────────────────────────────────────────────────┘

    내부 실패 비용 (Internal Failure Costs) - QC에서 검출된 결함
    ┌─────────────────────────────────────────────────────────────────────┐
    │  • 재작업 (Rework)                                                   │
    │  • 결함 수정                                                         │
    │  • 재테스트                                                          │
    │  • 일정 지연                                                         │
    │                                                                      │
    │  발생 시점: 출시 전                                                   │
    │  비용: 중간                                                          │
    └─────────────────────────────────────────────────────────────────────┘

    외부 실패 비용 (External Failure Costs) - QC에서 누락된 결함
    ┌─────────────────────────────────────────────────────────────────────┐
    │  • 고객 불만 처리                                                    │
    │  • 제품 리콜                                                         │
    │  • 소송 및 배상                                                      │
    │  • 브랜드 이미지 손상                                                 │
    │  • 기술 지원 비용                                                     │
    │                                                                      │
    │  발생 시점: 출시 후                                                   │
    │  비용: 최고 (내부 실패의 10~100배)                                    │
    └─────────────────────────────────────────────────────────────────────┘

    ─────────────────────────────────────────────────────────────────────────

    최적화 곡선:

    비용
      ^
      │                                      총 품질 비용
      │                                    ／
      │                                  ／
      │                ／－－－－－－－－／ 最적점
      │              ／   내부/외부     ／
      │            ／     실패 비용   ／
      │          ／                 ／  평가 비용
      │        ／                 ／
      │      ／                 ／
      │    ／  예방 비용       ／
      │  ／                 ／
      │／──────────────────────────────────────> QA/QC 투자 수준
      │
      │  적음        적정        과다

    교훈: 예방 비용 1달러 투자 = 실패 비용 10~100달러 절감

================================================================================
```

### 3. 심층 동작 원리: QA/QC 통합 프로세스

```
Step 1: 품질 계획 수립 (Quality Planning) - QA
        ┌────────────────────────────────────────┐
        │ • 품질 목표 정의                        │
        │ • 품질 메트릭 선정                      │
        │ • QA/QC 활동 계획                      │
        │ • 품질 기준선(Baseline) 설정            │
        └────────────────────────────────────────┘
                         │
                         v
Step 2: 프로세스 정의 및 교육 (Process Definition & Training) - QA
        ┌────────────────────────────────────────┐
        │ • 코딩 표준 정의                        │
        │ • 테스트 표준 정의                      │
        │ • 리뷰/인스펙션 절차 수립               │
        │ • 팀 교육 실시                         │
        └────────────────────────────────────────┘
                         │
                         v
Step 3: 개발 활동 모니터링 (Development Monitoring) - QA
        ┌────────────────────────────────────────┐
        │ • 프로세스 준수 감사                    │
        │ • 정적 분석 실행                        │
        │ • 코드 리뷰 지원                        │
        │ • 프로세스 편차 식별                    │
        └────────────────────────────────────────┘
                         │
                         v
Step 4: 제품 검증 (Product Verification) - QC
        ┌────────────────────────────────────────┐
        │ • 단위 테스트 수행                      │
        │ • 통합/시스템 테스트                   │
        │ • 결함 기록 및 추적                    │
        │ • 테스트 커버리지 측정                  │
        └────────────────────────────────────────┘
                         │
                         v
Step 5: 품질 분석 및 개선 (Analysis & Improvement) - QA+QC
        ┌────────────────────────────────────────┐
        │ • 결함 원인 분석 (RCA)                 │
        │ • 프로세스 개선 제안                    │
        │ • 품질 메트릭 리포트                   │
        │ • 교훈(Lessons Learned) 정리           │
        └────────────────────────────────────────┘
```

### 4. 핵심 코드: QA/QC 메트릭 시스템

```python
"""
QA/QC Metrics System
품질 보증 및 품질 제어 메트릭 관리 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
from enum import Enum

class MetricType(Enum):
    QA = "QA"
    QC = "QC"

@dataclass
class QualityMetric:
    """품질 메트릭"""
    name: str
    metric_type: MetricType
    target: float
    actual: float
    unit: str
    measurement_date: datetime

    @property
    def achievement_rate(self) -> float:
        """달성률"""
        if self.target == 0:
            return 0
        return (self.actual / self.target) * 100

    @property
    def status(self) -> str:
        """상태"""
        if self.achievement_rate >= 100:
            return "달성"
        elif self.achievement_rate >= 80:
            return "주의"
        else:
            return "미달"

@dataclass
class Defect:
    """결함"""
    defect_id: str
    severity: str  # Critical, Major, Minor
    phase_found: str  # 발견 단계
    phase_injected: str  # 주입 단계
    cost_to_fix: float  # 수정 비용 (인시)

@dataclass
class QualityReport:
    """품질 리포트"""
    project_name: str
    report_date: datetime
    qa_metrics: List[QualityMetric] = field(default_factory=list)
    qc_metrics: List[QualityMetric] = field(default_factory=list)
    defects: List[Defect] = field(default_factory=list)

    def calculate_defect_removal_efficiency(self) -> Dict[str, float]:
        """결함 제거 효율 (DRE) - QC 메트릭"""
        # DRE = (출시 전 발견 결함 / 전체 결함) × 100
        pre_release = sum(1 for d in self.defects
                         if d.phase_found != "운영")
        total = len(self.defects)

        if total == 0:
            return {"DRE": 0}

        return {"DRE": round((pre_release / total) * 100, 1)}

    def calculate_phase_containment_efficiency(self) -> float:
        """단계별 결함 포집 효율 (PCE) - QA 메트릭"""
        # PCE = (해당 단계에서 발견된 결함 / 해당 단계에서 주입된 결함) × 100
        # 간소화: 전체 평균
        total_injected = len(self.defects)
        same_phase_found = sum(1 for d in self.defects
                              if d.phase_found == d.phase_injected)

        if total_injected == 0:
            return 0

        return round((same_phase_found / total_injected) * 100, 1)

    def calculate_cost_of_quality(self) -> Dict:
        """품질 비용 분석"""
        # 예방 비용 (QA 활동)
        prevention_cost = sum(
            m.actual * 1000  # 예시: 시간당 1000원
            for m in self.qa_metrics
            if "교육" in m.name or "감사" in m.name
        )

        # 평가 비용 (QC 활동)
        appraisal_cost = sum(
            m.actual * 1000
            for m in self.qc_metrics
            if "테스트" in m.name
        )

        # 실패 비용 (결함 수정)
        failure_cost = sum(d.cost_to_fix * 50 for d in self.defects)  # 인시당 50원

        return {
            "prevention": prevention_cost,
            "appraisal": appraisal_cost,
            "internal_failure": failure_cost * 0.3,  # 내부 30%
            "external_failure": failure_cost * 0.7,  # 외부 70%
            "total": prevention_cost + appraisal_cost + failure_cost
        }

    def generate_summary(self) -> str:
        """요약 리포트"""
        dre = self.calculate_defect_removal_efficiency()
        pce = self.calculate_phase_containment_efficiency()
        coq = self.calculate_cost_of_quality()

        summary = [
            f"\n{'='*60}",
            f"품질 리포트 - {self.project_name}",
            f"{'='*60}",
            f"\n[QA 메트릭 (예방 중심)]",
            f"  단계별 결함 포집 효율: {pce}%",
        ]

        for m in self.qa_metrics:
            status_icon = "✓" if m.status == "달성" else "△" if m.status == "주의" else "✗"
            summary.append(f"  {status_icon} {m.name}: {m.actual}/{m.target} {m.unit}")

        summary.extend([
            f"\n[QC 메트릭 (검출 중심)]",
            f"  결함 제거 효율 (DRE): {dre['DRE']}%",
        ])

        for m in self.qc_metrics:
            status_icon = "✓" if m.status == "달성" else "△" if m.status == "주의" else "✗"
            summary.append(f"  {status_icon} {m.name}: {m.actual}/{m.target} {m.unit}")

        summary.extend([
            f"\n[품질 비용]",
            f"  예방 비용: {coq['prevention']:,.0f}원",
            f"  평가 비용: {coq['appraisal']:,.0f}원",
            f"  내부 실패: {coq['internal_failure']:,.0f}원",
            f"  외부 실패: {coq['external_failure']:,.0f}원",
            f"  총 품질 비용: {coq['total']:,.0f}원",
            f"{'='*60}",
        ])

        return "\n".join(summary)


# 사용 예시
if __name__ == "__main__":
    report = QualityReport(
        project_name="모바일 앱 개발",
        report_date=datetime.now()
    )

    # QA 메트릭
    report.qa_metrics = [
        QualityMetric("프로세스 준수율", MetricType.QA, 95, 92, "%"),
        QualityMetric("교육 이수율", MetricType.QA, 100, 100, "%"),
        QualityMetric("정적 분석 결함률", MetricType.QA, 5, 3, "건/KLOC"),
    ]

    # QC 메트릭
    report.qc_metrics = [
        QualityMetric("테스트 커버리지", MetricType.QC, 80, 85, "%"),
        QualityMetric("결함 밀도", MetricType.QC, 0.5, 0.3, "건/KLOC"),
        QualityMetric("인수 테스트 통과율", MetricType.QC, 100, 98, "%"),
    ]

    # 결함 데이터
    report.defects = [
        Defect("D001", "Major", "통합 테스트", "설계", 4),
        Defect("D002", "Minor", "단위 테스트", "구현", 1),
        Defect("D003", "Critical", "시스템 테스트", "요구사항", 8),
        Defect("D004", "Minor", "운영", "구현", 2),
    ]

    print(report.generate_summary())
```

---

## III. 융합 비교 및 다각도 분석

### 1. 심층 기술 비교: QA vs QC vs 테스트

| 비교 항목 | QA | QC | 테스트 |
|:---|:---|:---|:---|
| **초점** | 프로세스 | 제품 | 제품 |
| **목적** | 예방 | 검출 | 검증 |
| **활동** | 감사, 교육, 표준 | 검사, 테스트, 리뷰 | 실행 기반 검증 |
| **결과물** | 프로세스 개선 | 결함 리포트 | 테스트 리포트 |
| **담당** | QA 엔지니어 | QC 엔지니어 | 테스터 |
| **시점** | 전 과정 | 개발 후 | 개발 후 |

### 2. 과목 융합: QA/QC + CMMI

```
[CMMI PPQA 프로세스 영역]

PPQA (Process and Product Quality Assurance):
- CMMI Level 2 필수 프로세스 영역
- QA와 QC의 통합 활동

SG 1: 프로세스 준수 객관적 평가
- SP 1.1: 표준 프로세스 준수 평가
- SP 1.2: 산출물 준수 평가

SG 2: 비준수 사항 추적 및 통제
- SP 2.1: 비준수 사항 기록
- SP 2.2: 비준수 사항 해결

[융합 효과]
- QA: 프로세스 평가 (SG 1)
- QC: 산출물 평가 (SG 1.2)
- 통합: 비준수 관리 (SG 2)
```

---

## IV. 실무 적용 및 기술사적 판단

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오] 스타트업의 QA/QC 조직 구축**

*   **상황**:
    - 직원 20명, 개발팀 10명
    - 현재: 테스트 담당자 1명 (QC만 수행)
    - 문제: 출시 후 버그 다수, 고객 불만

*   **기술사적 판단**: **QA 중심으로 전환, Shift-Left**

*   **실행 전략**:
    ```
    1. QA 역할 강화:
       - 코딩 표준 정의
       - PR 리뷰 체크리스트
       - 자동화된 정적 분석

    2. QC 효율화:
       - 자동화된 테스트 도입
       - CI/CD 파이프라인 통합

    3. QA/QC 통합:
       - 개발자가 QA/QC 겸임
       - "품질은 모두의 책임"

    4. 메트릭 기반 관리:
       - 결함 밀도, 커버리지 추적
       - 월간 품질 리뷰
    ```

### 2. 도입 시 고려사항

**조직 구조**:
- [ ] 독립 QA 조직 vs 개발팀 내 QA
- [ ] QA/QC 역할 분리 vs 통합
- [ ] 아웃소싱 vs 내재화

**도구 선정**:
- [ ] 정적 분석: SonarQube, ESLint
- [ ] 테스트 자동화: Selenium, Cypress
- [ ] 메트릭 대시보드: Grafana, SonarQube

### 3. 주의사항

*   **QA 없이 QC만**:
    - 검사만 하고 예방 안 함
    - 해결: QA 활동 비중 늘리기

*   **QA/QC 분리**:
    - 서로 "너희 일이야"라며 책임 전가
    - 해결: 공동 목표, 통합 보고

---

## V. 기대효과 및 결론

### 1. 정량적/정성적 기대효과

| 구분 | QA 효과 | QC 효과 |
|:---:|:---|:---|
| **결함** | 발생률 40% 감소 | 유출률 60% 감소 |
| **비용** | 실패 비용 50% 감소 | 재작업 30% 감소 |
| **일정** | 지연 25% 감소 | 테스트 기간 예측 가능 |

### 2. 미래 전망

1.  **AI 기반 QA**: 자동 프로세스 감사
2.  **Shift-Left Extreme**: 개발 초기 QA 통합
3.  **DevQAOps**: QA가 DevOps에 내재화

### 3. 참고 표준

*   **ISO 9001**: 품질 경영 체계
*   **CMMI PPQA**: Process and Product QA
*   **IEEE 730**: Software Quality Assurance

---

## 관련 개념 맵 (Knowledge Graph)

*   [소프트웨어 품질](@/studynotes/4_software_engineering/2_quality/software_quality_standards.md) : QA/QC의 목표
*   [소프트웨어 테스팅](@/studynotes/4_software_engineering/2_quality/software_testing.md) : QC의 핵심 활동
*   [CMMI](@/studynotes/4_software_engineering/1_sdlc/cmmi.md) : PPQA 프로세스 영역

---

## 어린이를 위한 3줄 비유 설명

1. **문제**: 숙제를 하고 나서 틀린 게 많아요.

2. **해결(QA/QC)**: 두 가지로 나눠요!
   - QA: "숙제하는 방법을 미리 알려줘요" (예방)
   - QC: "숙제 다 하고 나서 채점해요" (검출)

3. **효과**: 방법을 잘 알면 틀리는 게 줄어들고, 채점도 하니까 틀린 걸 고칠 수 있어요. 둘 다 해야 완벽해져요!
