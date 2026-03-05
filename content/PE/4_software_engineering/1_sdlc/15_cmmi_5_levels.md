+++
title = "15. CMMI 5단계 (CMMI Maturity Levels)"
description = "소프트웨어 프로세스 성숙도의 5단계 평가 모델, 초기(Initial)부터 최적화(Optimizing)까지의 진화 경로"
date = "2026-03-05"
[taxonomies]
tags = ["cmmi", "maturity-level", "process-improvement", "sei", "capability"]
categories = ["studynotes-4_software_engineering"]
+++

# 15. CMMI 5단계 (CMMI Maturity Levels)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CMMI 5단계는 소프트웨어 개발 조직의 **프로세스 성숙도를 1단계(초기)부터 5단계(최적화)까지** 체계적으로 평가하고 개선하는 프레임워크로, **예측 가능한 품질과 일정**을 달성하기 위한 로드맵을 제공합니다.
> 2. **가치**: CMMI Level 3 이상 조직은 **결함률 62% 감소, 일정 준수율 46% 향상, 비용 절감 20~30%** 등 정량적 효과가 입증되어 있으며, 특히 대형 공공/방위/금융 프로젝트에서 필수적입니다.
> 3. **융합**: **ISO 15504(SPICE), ISO 9001, Six Sigma** 등과 연계되며, 최근에는 **Agile CMMI, DevOps CMMI** 등으로 진화하여 애자일 환경에서도 적용 가능합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**CMMI(Capability Maturity Model Integration)**는 미국 카네기멜런대학교(CMU)의 **SEI(Software Engineering Institute)**가 개발한 프로세스 성숙도 평가 및 개선 모델입니다. 조직이 **"현재 어디에 있는가"**를 진단하고 **"어떻게 더 나아질 수 있는가"**를 체계적으로 안내합니다.

**CMMI 5단계의 핵심 철학**:
```
"프로세스의 품질이 제품의 품질을 결정한다"
(The quality of a product is largely determined by the quality of the process used to develop it)
```

**성숙도(Maturity) vs 능력(Capability)**:
- **성숙도 레벨(Maturity Level)**: 단계형 표현(Staged Representation) - 조직 전체의 성숙도를 1~5단계로 평가
- **능력 레벨(Capability Level)**: 연속형 표현(Continuous Representation) - 각 프로세스 영역별로 0~5단계 평가

### 2. 5단계 개요표

| 레벨 | 명칭 | 핵심 특징 | 프로세스 특성 | 대표적 조직 유형 |
|:---:|:---|:---|:---|:---|
| **1** | 초기 (Initial) | 혼돈, 예측 불가 | 프로세스 없음, 히어로 의존 | 스타트업, 초기 벤처 |
| **2** | 관리 (Managed) | 기본 프로젝트 관리 | 요구, 계획, 모니터링 | 성장기 기업 |
| **3** | 정의 (Defined) | 조직 표준 프로세스 | 표준화, 테일러링 | 중견 SI 기업 |
| **4** | 정량적 관리 (Quantitatively Managed) | 통계적 프로세스 관리 | 메트릭 기반 통제 | 대형 금융, 통신 |
| **5** | 최적화 (Optimizing) | 지속적 프로세스 개선 | 혁신, 최적화 | 항공우주, 원자력, 방산 |

### 3. 비유: 학교 성적 등급과 비교

```
[CMMI 5단계 = 학업 성취 수준]

Level 1 (초기): "시험 기간에 밤샘 공부"
- 공부 방법이 없음, 그날 컨디션에 따라 성적이 들쑥날쑥
- 운이 좋으면 100점, 나쁘면 0점 가능

Level 2 (관리): "학습 계획 세우기"
- 기본적인 공부 계획 존재 (무엇을, 언제 공부할지)
- 성적이 어느 정도 예측 가능해짐

Level 3 (정의): "검증된 공부법 정착"
- 나만의 효과적인 공부 방법을 문서화
- 어떤 과목도 동일한 방법으로 접근

Level 4 (정량적 관리): "성적 분석 시스템"
- "수학은 85±3점, 영어는 90±2점"처럼 통계적 예측
- 오답 분석, 약점 보완이 체계화

Level 5 (최적화): "완벽한 학습 최적화"
- 공부법 자체를 지속적으로 개선
- 새로운 학습법 실험, AI 기반 맞춤 학습 도입
```

### 4. 등장 배경 및 발전 과정

**1) 1986년: CMM(Capability Maturity Model)의 탄생**
- 미국 공군(US Air Force)이 소프트웨어 계약업체 평가를 위해 SEI에 의뢰
- Watts Humphrey가 중심이 되어 개발
- 소프트웨어 분야에 국한된 초기 모델

**2) 1991년: CMM v1.0 공식 발표**
- 5단계 성숙도 모델 정식화
- 미국 국방부(DoD) 조달 평가에 의무화

**3) 2002년: CMMI v1.1 - 통합 모델**
- CMM(SW), SECM(시스템 공학), IPD-CMM(통합 제품 개발) 통합
- 단계형 + 연속형 표현 모두 지원

**4) 2006년: CMMI v1.2 / 2010년: CMMI v1.3**
- 서비스(CMMI-SVC), 획득(CMMI-ACQ) 영역 추가
- 애자일 방법론과의 통합 가이드 강화

**5) 2018년: CMMI V2.0 (현재 최신 버전)**
- **성능 중심(Performance-oriented)**으로 재설계
- 25개 Process Area를 Practice Area로 재구성
- 애자일, DevOps, 보안(Security) 통합

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 각 레벨별 상세 구성 요소

```
================================================================================
|                    CMMI MATURITY LEVELS - DETAILED STRUCTURE                  |
================================================================================

LEVEL 5: OPTIMIZING (최적화)
┌──────────────────────────────────────────────────────────────────────────────┐
│  Focus: 지속적 프로세스 개선 (Continuous Process Improvement)                │
│  ──────────────────────────────────────────────────────────────────────────  │
│  Process Areas:                                                              │
│  • OPM (Organizational Performance Management) - 조직 성과 관리              │
│  • CAR (Causal Analysis and Resolution) - 원인 분석 및 해결                 │
│  ──────────────────────────────────────────────────────────────────────────  │
│  특징:                                                                       │
│  • 프로세스 성능 목표(PPO) 지속적 최적화                                     │
│  • 통계적 방법으로 개선 기회 식별                                            │
│  • 혁신적 기술, 도구 적극 도입                                               │
│  • "얼마나 더 개선할 수 있는가?"에 집중                                      │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
LEVEL 4: QUANTITATIVELY MANAGED (정량적 관리)
┌──────────────────────────────────────────────────────────────────────────────┐
│  Focus: 통계적 프로세스 관리 (Statistical Process Control)                   │
│  ──────────────────────────────────────────────────────────────────────────  │
│  Process Areas:                                                              │
│  • OPP (Organizational Process Performance) - 조직 프로세스 성능             │
│  • QPM (Quantitative Project Management) - 정량적 프로젝트 관리              │
│  ──────────────────────────────────────────────────────────────────────────  │
│  특징:                                                                       │
│  • 프로세스 성능 기준선(PPL)과 모델(PPM) 확립                                │
│  • 정량적 목표 설정 및 통계적 관리 한계선(UCL/LCL) 적용                       │
│  • "결함률 0.5±0.1/KLOC" 같은 예측 가능성 확보                               │
│  • 6-Sigma, SPC 기법 적용                                                    │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
LEVEL 3: DEFINED (정의)
┌──────────────────────────────────────────────────────────────────────────────┐
│  Focus: 조직 표준 프로세스 (Organizational Standard Process)                 │
│  ──────────────────────────────────────────────────────────────────────────  │
│  Process Areas:                                                              │
│  • OPD (Organizational Process Definition) - 조직 프로세스 정의              │
│  • OT (Organizational Training) - 조직 교육                                  │
│  • IPM (Integrated Project Management) - 통합 프로젝트 관리                  │
│  • RSKM (Risk Management) - 위험 관리                                        │
│  • DAR (Decision Analysis and Resolution) - 의사결정 분석                    │
│  ──────────────────────────────────────────────────────────────────────────  │
│  특징:                                                                       │
│  • 표준 소프트웨어 프로세스(SSP) 문서화                                       │
│  • 프로젝트별 테일러링(Tailoring) 가이드                                      │
│  • 조직 차원의 프로세스 자산 라이브러리(PAL) 구축                             │
│  • "회사 표준대로 하면 일정/품질이 보장됨"                                    │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
LEVEL 2: MANAGED (관리)
┌──────────────────────────────────────────────────────────────────────────────┐
│  Focus: 프로젝트 단위 관리 (Project-Level Management)                        │
│  ──────────────────────────────────────────────────────────────────────────  │
│  Process Areas:                                                              │
│  • REQM (Requirements Management) - 요구사항 관리                            │
│  • PP (Project Planning) - 프로젝트 계획                                     │
│  • PMC (Project Monitoring and Control) - 프로젝트 모니터링                  │
│  • SAM (Supplier Agreement Management) - 공급자 계약 관리                    │
│  • MA (Measurement and Analysis) - 측정 및 분석                              │
│  • PPQA (Process and Product Quality Assurance) - 품질 보증                  │
│  • CM (Configuration Management) - 형상 관리                                 │
│  ──────────────────────────────────────────────────────────────────────────  │
│  특징:                                                                       │
│  • 프로젝트별로 계획 수립 및 실적 관리                                        │
│  • 이슈 발생 시 추적 및 조치 가능                                            │
│  • "이번 프로젝트는 무엇을, 언제까지, 누가" 정의                              │
│  • 과거 유사 프로젝트 경험 활용 시작                                          │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    v
LEVEL 1: INITIAL (초기)
┌──────────────────────────────────────────────────────────────────────────────┐
│  Focus: 개인 역량 의존 (Individual Heroics)                                  │
│  ──────────────────────────────────────────────────────────────────────────  │
│  특징:                                                                       │
│  • 공식 프로세스 없음                                                        │
│  • 성공은 개인 능력에 전적으로 의존                                          │
│  • 일정, 예산 초과가 일상적                                                  │
│  • "이번엔 운이 좋아서 성공했어"                                              │
│  • 동일한 실수 반복                                                          │
└──────────────────────────────────────────────────────────────────────────────┘

================================================================================
```

### 2. 정교한 ASCII 다이어그램: 레벨별 프로세스 영역 맵핑

```
================================================================================
|           CMMI-DEV Process Areas by Maturity Level (Staged)                   |
================================================================================

       Level 5                                          Level 4
   ┌──────────────────┐                         ┌──────────────────┐
   │  CAR ──────────┐ │                         │  OPP ──────────┐ │
   │  (원인분석)     │ │                         │  (프로세스성능) │ │
   │                 │ │                         │                 │ │
   │  OPM ───────────┤ │                         │  QPM ───────────┤ │
   │  (조직성과관리) │ │                         │  (정량적관리)   │ │
   └────────┬─────────┘                         └────────┬─────────┘
            │                                            │
            └────────────────────┬───────────────────────┘
                                 │
                          Level 3 (정의)
    ┌─────────────────────────────────────────────────────────────┐
    │  RD   REQM  TS   PI   VER  VAL  OPF  OPD  OT  IPM  RSKM DAR │
    │  │    │     │    │    │    │    │    │    │   │    │    │  │
    │  │    │     │    │    │    │    │    │    │   │    │    │  │
    │  요구 요구  기술 제품 검증 확인 조직 조직 조직 통합 위험 의사 │
    │  개발 관리  솔루션 통합                          관리 결정 │
    └─────────────────────────────────────────────────────────────┘
                                 │
                          Level 2 (관리)
    ┌─────────────────────────────────────────────────────────────┐
    │  REQM  PP   PMC  SAM  MA   PPQA  CM                         │
    │  │     │    │    │    │     │     │                         │
    │  │     │    │    │    │     │     │                         │
    │  요구  계획  모니 터링 공급 측정 품질 형상                   │
    │  관리       제어       관리 분석 보증 관리                   │
    └─────────────────────────────────────────────────────────────┘

  범례:
  ──>: 선행 관계 (Prerequisite)
  RD: Requirements Development    TS: Technical Solution
  PI: Product Integration        VER: Verification
  VAL: Validation               OPF: Organizational Process Focus
  OPD: Organizational Process Definition
================================================================================
```

### 3. 심층 동작 원리: 레벨 업 프로세스 (5단계)

```
Step 1: 현재 레벨 진단 (Appraisal)
        ┌────────────────────────────────────────┐
        │ SCAMPI (Standard CMMI Appraisal Method)│
        │ - Class A: 공식 인증 평가              │
        │ - Class B: 준공식 진단                 │
        │ - Class C: 초기 자가 진단              │
        │                                         │
        │ 결과: 현재 레벨 확인, Gap 분석          │
        └────────────────────────────────────────┘
                         │
                         v
Step 2: 개선 영역 식별 (Improvement Identification)
        ┌────────────────────────────────────────┐
        │ 현재 레벨 대비 부족한 Practice Areas    │
        │ 우선순위화 (비즈니스 영향도, 난이도)    │
        │ 개선 목표(Specific Goals) 설정         │
        └────────────────────────────────────────┘
                         │
                         v
Step 3: 액션 플랜 수립 (Action Planning)
        ┌────────────────────────────────────────┐
        │ 프로세스 정의/수정                     │
        │ 교육 계획                              │
        │ 도구 도입 계획                         │
        │ 파일럿 프로젝트 선정                   │
        └────────────────────────────────────────┘
                         │
                         v
Step 4: 파일럿 실행 및 검증 (Pilot & Validation)
        ┌────────────────────────────────────────┐
        │ 소규모 프로젝트에 새 프로세스 적용     │
        │ 메트릭 수집                            │
        │ 피드백 수집 및 프로세스 조정           │
        └────────────────────────────────────────┘
                         │
                         v
Step 5: 전사 확산 및 인증 (Deployment & Certification)
        ┌────────────────────────────────────────┐
        │ 조직 전체로 프로세스 확산              │
        │ 정식 SCAMPI Class A 평가 수행          │
        │ CMMI Institute로 레벨 인증 신청        │
        │                                        │
        │ ──────> 다음 레벨 도전                 │
        └────────────────────────────────────────┘
```

### 4. 핵심 코드 예시: CMMI 레벨 진단 시스템

```python
"""
CMMI Maturity Level Assessment System
조직 프로세스 성숙도 자가 진단 도구
"""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class MaturityLevel(Enum):
    INITIAL = 1
    MANAGED = 2
    DEFINED = 3
    QUANTITATIVELY_MANAGED = 4
    OPTIMIZING = 5

@dataclass
class PracticeArea:
    """CMMI V2.0 Practice Area"""
    name: str
    level_required: MaturityLevel
    specific_practices: List[str]
    satisfaction_score: float = 0.0  # 0-100

@dataclass
class ProcessAreaAssessment:
    """프로세스 영역별 평가 결과"""
    area_name: str
    goal_achievement: float  # 0-100
    practice_scores: Dict[str, float]  # practice name -> score
    evidence: List[str]
    gaps: List[str]

class CMMIAssessment:
    """CMMI 성숙도 평가 클래스"""

    def __init__(self, organization_name: str):
        self.organization_name = organization_name
        self.assessments: List[ProcessAreaAssessment] = []

    def assess_level2_areas(self) -> Dict[str, ProcessAreaAssessment]:
        """Level 2 (Managed) 프로세스 영역 평가"""
        level2_areas = {
            "REQM": "요구사항 관리",
            "PP": "프로젝트 계획",
            "PMC": "프로젝트 모니터링 및 제어",
            "SAM": "공급자 계약 관리",
            "MA": "측정 및 분석",
            "PPQA": "프로세스 및 제품 품질 보증",
            "CM": "형상 관리"
        }

        results = {}
        for code, name in level2_areas.items():
            # 실제로는 인터뷰, 문서 검토 등을 통해 점수 산출
            assessment = ProcessAreaAssessment(
                area_name=f"{code} - {name}",
                goal_achievement=0.0,  # 평가 후 입력
                practice_scores={},
                evidence=[],
                gaps=[]
            )
            results[code] = assessment

        return results

    def calculate_maturity_level(self) -> MaturityLevel:
        """종합 성숙도 레벨 계산"""

        # Level 2 달성 조건: 모든 Level 2 PA가 85% 이상 달성
        level2_results = self.assess_level2_areas()
        level2_satisfied = all(
            a.goal_achievement >= 85 for a in level2_results.values()
        )

        if not level2_satisfied:
            return MaturityLevel.INITIAL

        # Level 3 달성 조건: Level 2 + 모든 Level 3 PA 85% 이상
        # Level 4, 5 도 동일한 로직 적용
        # ... (실제 구현 시 전체 PA 평가 로직 추가)

        return MaturityLevel.MANAGED

    def generate_gap_report(self) -> str:
        """Gap 분석 보고서 생성"""
        report = [f"\n=== {self.organization_name} CMMI Gap 분석 보고서 ===\n"]

        current_level = self.calculate_maturity_level()
        report.append(f"현재 추정 레벨: {current_level.name}\n")

        target_level = MaturityLevel(current_level.value + 1)
        report.append(f"목표 레벨: {target_level.name}\n")
        report.append("\n개선 필요 영역:\n")

        for assessment in self.assessments:
            if assessment.goal_achievement < 85:
                report.append(f"\n[{assessment.area_name}]")
                report.append(f"  달성률: {assessment.goal_achievement:.1f}%")
                for gap in assessment.gaps:
                    report.append(f"  - {gap}")

        return "\n".join(report)

# 사용 예시
if __name__ == "__main__":
    assessment = CMMIAssessment("ABC소프트웨어")

    # 샘플 평가 데이터
    sample_assessment = ProcessAreaAssessment(
        area_name="REQM - 요구사항 관리",
        goal_achievement=78,
        practice_scores={
            "SP 1.1 요구사항 이해": 85,
            "SP 1.2 요구사항 획득": 70,
            "SP 1.3 요구사항 변경 관리": 80
        },
        evidence=["요구사항 추적 매트릭스 존재"],
        gaps=["변경 관리 프로세스 미흡", "이해관계자 리뷰 미실시"]
    )

    assessment.assessments.append(sample_assessment)
    print(assessment.generate_gap_report())
```

---

## III. 융합 비교 및 다각도 분석

### 1. 심층 기술 비교: CMMI vs 다른 품질 모델

| 비교 항목 | CMMI | ISO 9001 | SPICE (ISO 15504) | Six Sigma |
|:---|:---|:---|:---|:---|
| **영역** | 소프트웨어/시스템 공학 | 전 산업 품질 경영 | 소프트웨어 프로세스 | 전 산업 품질 개선 |
| **구조** | 5단계 성숙도 | 요구사항 체크리스트 | 6단계 능력 레벨 | DMAIC 방법론 |
| **인증** | CMMI Institute 인증 | ISO 인증 기관 | SPICE 평가 | 없음 (기법) |
| **비용** | 높음 (평가비+컨설팅) | 중간 | 중간 | 낮음~중간 |
| **소요 기간** | 2~3년 (레벨업당) | 1~2년 | 1~2년 | 지속적 |
| **강점** | 소프트웨어 특화, 심층적 | 범용성, 글로벌 인지도 | 유연성, 세분화 | 데이터 기반, 정량적 |
| **약점** | 높은 비용, 복잡성 | 소프트웨어 특성 반영 부족 | 인지도 낮음 | SW 특화 아님 |

### 2. 레벨별 비즈니스 임팩트 비교

| 지표 | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **일정 준수율** | ~40% | ~60% | ~80% | ~90% | ~95% |
| **예산 준수율** | ~35% | ~55% | ~75% | ~88% | ~93% |
| **결함률 (Defects/KLOC)** | 5.0+ | 2.5 | 1.0 | 0.5 | 0.2 |
| **재작업 비용 비율** | 40%+ | 25% | 15% | 8% | 3% |
| **고객 만족도** | 2.5/5 | 3.2/5 | 3.8/5 | 4.2/5 | 4.6/5 |
| **프로젝트 성공률** | 30% | 50% | 70% | 85% | 95% |

### 3. 과목 융합 관점 분석

**CMMI + 프로젝트 관리 (PMBOK)**
```
[융합 매핑]

CMMI Level 2 Process Areas    <--->    PMBOK Knowledge Areas
─────────────────────────────────────────────────────────────
REQM (요구사항 관리)          <--->    범위 관리, 이해관계자 관리
PP (프로젝트 계획)            <--->    통합 관리, 일정 관리, 비용 관리
PMC (모니터링 및 제어)        <--->    통합 관리, 위험 관리
MA (측정 및 분석)             <--->    품질 관리, 통합 관리
CM (형상 관리)                <--->    통합 관리, 범위 관리

[시너지]
- CMMI: "어떻게" 프로세스를 구축할지
- PMBOK: "무엇을" 관리할지
- 결합: 체계적이고 측정 가능한 프로젝트 관리
```

**CMMI + 애자일 (Agile)**
```
[오해] "CMMI와 애자일은 양립할 수 없다"
[현실] CMMI V2.0은 애자일을 명시적으로 지원

Level 2 (Managed):
- 스크럼의 스프린트 계획 = PP (Project Planning)
- 데일리 스탠드업 = PMC (Monitoring)
- 제품 백로그 = REQM

Level 3 (Defined):
- 조직 표준 스크럼 프로세스 = OPD
- 스크럼 마스터 교육 = OT

Level 5 (Optimizing):
- 스프린트 회고 = CAR (Causal Analysis)
- 지속적 개선 = OPM
```

---

## IV. 실무 적용 및 기술사적 판단

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오 1] 중견 SI 기업의 CMMI Level 3 달성**

*   **상황**:
    - 직원 200명, 연 매출 500억 원
    - 현재 상태: 체계적 프로세스 없음, 프로젝트마다 상이
    - 목표: 공공 시장 진출을 위해 CMMI Level 3 획득
    - 예산: 3억 원, 기간: 2년

*   **기술사적 판단**: **단계적 접근, 파일럿 중심**

*   **실행 로드맵**:
    ```
    Year 1 (Level 2 달성):
    Q1: 현재 상태 진단 (SCAMPI Class C)
    Q2: PP, PMC, REQM 프로세스 정의
    Q3: 파일럿 프로젝트 2개에 적용
    Q4: Level 2 프랙티스 정착, 내부 감사

    Year 2 (Level 3 달성):
    Q1: OPD, OT, IPM 프로세스 정의
    Q2: 조직 표준 프로세스(SOP) 문서화
    Q3: 전사 확산, 전 프로젝트 적용
    Q4: SCAMPI Class A 정식 평가, 인증
    ```

*   **핵심 성공 요인**:
    - 최고 경영진(Top Management)의 확실한 commitment
    - 전담 조직(EPG: Engineering Process Group) 구성
    - 실무자 참여형 프로세스 정의 (문서 위주 X)

**[시나리오 2] 스타트업의 Agile-CMMI 하이브리드**

*   **상황**:
    - 직원 30명, 핀테크 서비스 개발
    - 현재: 스크럼 도입 1년차, 빠른 성장 중
    - 요구: 투자자 신뢰 확보, 대형 금융사 협업

*   **기술사적 판단**: **Agile-CMMI 융합, 경량화 접근**

*   **실행 전략**:
    - CMMI 레벨 인증보다는 **핵심 프랙티스만 선택적 도입**
    - Level 2의 PP, PMC, REQM을 스크럼에 맞게 해석하여 적용
    - 문서보다 **자동화된 메트릭 수집**에 집중 (Jira, Confluence)
    - "우리는 CMMI Level 3 인증"보다 "우리는 CMMI 레벨 3 상당의 프로세스 운영"

### 2. 도입 시 고려사항 체크리스트

**조직적 고려사항**:
- [ ] **경영진 지원**: 충분한 예산, 인력 배정 약속
- [ ] **변화 관리**: 저항 세력 관리, 성공 사례 홍보
- [ ] **전담 조직**: EPG(Engineering Process Group) 구성
- [ ] **인센티브**: 프로세스 준수에 대한 보상 체계

**기술적 고려사항**:
- [ ] **도구 선정**: 프로세스 자동화 도구 (Jira, Azure DevOps 등)
- [ ] **메트릭 정의**: 수집할 핵심 메트릭 선정
- [ ] **문서 관리**: 프로세스 자산 라이브러리 구축

**비용/일정 고려사항**:
- [ ] **평가 비용**: SCAMPI Class A 약 1~2억 원 (컨설팅 별도)
- [ ] **컨설팅 비용**: 레벨당 1~3억 원
- [ ] **소요 기간**: 레벨업당 1~2년 현실적 고려

### 3. 주의사항 및 안티패턴

*   **문서를 위한 프로세스 (Process for Documentation)**:
    - 인증만 통과하면 된다는 식의 형식적 문서 작성
    - 실제 프로젝트에서는 전혀 활용되지 않는 "선반용" 프로세스

*   **레벨 숫자에 집착 (Level Obsession)**:
    - "무조건 Level 5까지만 올라가자"는 잘못된 목표
    - 비즈니스에 맞는 적정 레벨(보통 Level 3)이 최적

*   **일회성 인증 (One-time Certification)**:
    - 인증 후 프로세스 유지/개선 없음
    - 3년 후 재평가 시 탈락

*   **ROI 무시**:
    - CMMI 도입 비용 vs 품질 향상 효과 계산 없음
    - 소규모 조직에 과도한 프로세스 적용

---

## V. 기대효과 및 결론

### 1. 정량적/정성적 기대효과

| 구분 | 효과 내용 | 측정 가능 지표 |
|:---:|:---|:---|
| **품질** | 결함 감소, 재작업 축소 | 결함률 60% 감소 (L2→L4) |
| **생산성** | 프로세스 표준화로 효율 증대 | 생산성 30% 향상 |
| **예측성** | 일정/비용 예측 정확도 향상 | 일정 준수율 50% 향상 |
| **경쟁력** | 공공/방위 입찰 자격 확보 | 신규 수주 20% 증가 |
| **조직 역량** | 체계적 교육, 지식 축적 | 이직률 15% 감소 |

### 2. 미래 전망 및 진화 방향

1.  **CMMI V3.0 (예정)**:
    - AI/ML 기반 프로세스 자동화 가이드 강화
    - 보안(Security), 개인정보보호(Privacy) 영역 통합

2.  **DevOps/CMMI 융합**:
    - CI/CD 파이프라인을 CMMI 프랙티스로 해석
    - 자동화된 메트릭 수집 → Level 4/5 달성 용이

3.  **클라우드 네이티브**:
    - MSA, 컨테이너 환경에 맞는 프로세스 영역 추가

### 3. 참고 표준/가이드

*   **CMMI Institute**: https://cmmiinstitute.com/
*   **CMMI for Development (CMMI-DEV) V1.3/V2.0**
*   **SCAMPI Appraisal Method**
*   **ISO/IEC 15504 (SPICE)**: CMMI와 유사한 국제 표준

---

## 관련 개념 맵 (Knowledge Graph)

*   [소프트웨어 공학](@/studynotes/4_software_engineering/1_sdlc/1_software_engineering.md) : CMMI가 속한 상위 개념
*   [ISO 15504 SPICE](@/studynotes/4_software_engineering/1_sdlc/14_iso15504_spice.md) : CMMI와 유사한 국제 표준
*   [형상 관리](@/studynotes/4_software_engineering/1_sdlc/configuration_management.md) : Level 2 필수 프로세스 영역
*   [품질 보증](@/studynotes/4_software_engineering/2_quality/software_quality_standards.md) : Level 2 PPQA 프로세스
*   [프로젝트 관리](@/studynotes/4_software_engineering/3_project/_index.md) : CMMI PP, PMC와 직접 연관

---

## 어린이를 위한 3줄 비유 설명

1. **문제**: 어떤 친구는 숙제를 아무렇게나 하고, 어떤 친구는 계획을 세워서 해요. 아무렇게나 하면 실수도 많고 늦게 끝나죠!

2. **해결(CMMI)**: **공부 레벨**을 매겨봐요! 레벨 1은 "그냥 하는 것", 레벨 2는 "계획 세우기", 레벨 3은 "자기만의 공부법 만들기", 레벨 4는 "성적 분석하기", 레벨 5는 "완벽하게 최적화하기"예요.

3. **효과**: 레벨이 높아질수록 숙제도 빨리 끝나고, 성적도 좋아져요! 회사에서도 이 레벨이 높으면 "이 회사는 일을 잘하는 곳이구나!"라고 인정받아요.
