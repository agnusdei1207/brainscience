+++
title = "소프트웨어 생명주기 (SDLC)"
date = 2024-05-24
description = "소프트웨어 개발부터 폐기까지의 전 과정을 체계화한 프레임워크"
weight = 30
+++

# 소프트웨어 생명주기 (SDLC - Software Development Life Cycle)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SDLC(Software Development Life Cycle)는 소프트웨어가 **태어나고(계획), 성장하고(개발), 운영되다가(유지보수), 폐기되는(退役)** 전 과정을 **단계별로 체계화한 프레임워크**로, ISO/IEC 12207 표준의 핵심 개념입니다.
> 2. **가치**: 적절한 SDLC 적용 시 **요구사항 누락 60% 감소, 재작업 비용 40% 절감, 프로젝트 예측 가능성 50% 향상** 등 정량적 효과가 입증되며, 각 단계별 **산출물, 진입/진출 기준, 품질 게이트**를 정의합니다.
> 3. **융합**: 폭포수, V-Model, 나선형, 애자일 등 다양한 모델로 구체화되며, 최근 **DevOps, CI/CD, GitOps** 등과 결합하여 **지속적 배포 생명주기**로 진화하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**소프트웨어 생명주기(SDLC, Software Development Life Cycle)**는 소프트웨어 제품이 **계획 단계부터 최종 폐기까지** 거치는 전 과정을 단계별로 정의한 프레임워크입니다. 각 단계는 명확한 **입력(Input), 처리(Process), 출력(Output)**을 가지며, 품질 관리 활동이 통합됩니다.

**SDLC의 핵심 구성요소**:

| 구성요소 | 설명 | 예시 |
| :--- | :--- | :--- |
| **단계(Phases)** | 소프트웨어 개발의 논리적 구분 | 요구분석, 설계, 구현, 테스트, 운영 |
| **산출물(Deliverables)** | 각 단계의 결과물 | 요구사항 명세서, 설계서, 소스코드 |
| **활동(Activities)** | 단계 내 수행 작업 | 인터뷰, 모델링, 코딩, 테스트 수행 |
| **진입 기준(Entry Criteria)** | 단계 시작 조건 | 요구사항 확정, 승인된 계획서 |
| **진출 기준(Exit Criteria)** | 단계 완료 조건 | 검토 완료, 품질 게이트 통과 |
| **품질 게이트(Quality Gates)** | 단계 전환 승인점 | 기술 검토, 인스펙션, 테스트 통과 |

**SDLC vs SLC (Software Life Cycle)**:
```
SDLC (Software Development Life Cycle):
- 소프트웨어 '개발'에 초점
- 계획 → 분석 → 설계 → 구현 → 테스트 → 배포

SLC (Software Life Cycle):
- 소프트웨어 '전 수명'에 초점
- 개발 + 운영 + 유지보수 + 폐기
- ISO/IEC 12207의 더 포괄적 개념

실무에서는 SDLC와 SLC를 혼용하여 사용
```

### 💡 일상생활 비유: 인간의 생애 주기

```
[소프트웨어 생명주기 = 인간의 생애 주기]

인간 생애 주기              SDLC 단계
===============            ===========
임신/출산                   계획 (Planning)
  │                        - 태교(요구사항 분석)
  │                        - 출산 준비(환경 구축)
  v
유아기                     요구분석 (Analysis)
  │                        - 아이의 필요 파악
  │                        - 성장 계획 수립
  v
학생기                     설계 (Design)
  │                        - 교육 과정 설계
  │                        - 진로 계획
  v
성인/직장인                 구현 (Implementation)
  │                        - 실제 일 수행
  │                        - 역량 발휘
  v
건강검진/치료               테스트 (Testing)
  │                        - 문제 조기 발견
  │                        - 치료 및 개선
  v
직장 생활                   운영 (Operation)
  │                        - 지속적 업무 수행
  │                        - 성과 창출
  v
노후/은퇴                   유지보수 (Maintenance)
  │                        - 건강 관리
  │                        - 적응적 생활
  v
사망/장례                   폐기 (Retirement)
                           - 생애 마무리
                           - 기록 보관

핵심:
- 각 단계는 순차적이지만 되돌아갈 수도 있음
- 이전 단계가 다음 단계에 영향
- 모든 단계가 중요함 (어느 하나 소홀히 하면 문제 발생)
```

### 2. 등장 배경 및 발전 과정

#### 1) 1960~70년대: SDLC 개념의 탄생

**배경**:
- 소프트웨어 위기 인식
- 무계획적 개발로 인한 실패 반복
- 체계적 접근의 필요성 대두

**초기 SDLC (폭포수 모델)**:
```
1970년 Winston Royce가 제안한 순차적 모델

요구사항 → 설계 → 구현 → 테스트 → 운영

특징:
- 각 단계가 완료되어야 다음 단계 진행
- 문서 중심, 형식적 검토
- 변경에 취약
```

#### 2) 1980~90년대: 다양한 SDLC 모델 등장

| 모델 | 특징 | 적용 분야 |
| :--- | :--- | :--- |
| **V-Model** | 개발-테스트 단계 대응 | 안전 중요 시스템 |
| **나선형 모델** | 위험 분석 중심 | 대규모, 고위험 프로젝트 |
| **프로토타입 모델** | 시제품 중심 | 요구사항 불확실 |
| **RAD** | 신속 개발 | 비즈니스 앱 |

#### 3) 2000년대~현재: 애자일과 DevOps

```
전통적 SDLC → 애자일 SDLC → DevOps 생명주기

특징 변화:
- 문서 중심 → 동작 코드 중심
- 순차적 → 반복적/점진적
- 분리된 단계 → 통합된 파이프라인
- 수동 게이트 → 자동화된 품질 게이트
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. SDLC 기본 단계 구성

| 단계 | 영문명 | 핵심 활동 | 주요 산출물 | 품질 활동 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 계획** | Planning | 타당성 조사, 범위 정의, 자원 계획 | 프로젝트 계획서, WBS | 리스크 분석 |
| **2. 요구분석** | Analysis | 요구사항 도출, 분석, 명세 | SRS, 유스케이스 | 요구사항 검토 |
| **3. 설계** | Design | 아키텍처, 상세 설계 | 설계서, DB 스키마 | 설계 검토 |
| **4. 구현** | Implementation | 코딩, 단위 테스트 | 소스코드, 실행파일 | 코드 리뷰 |
| **5. 테스트** | Testing | 통합, 시스템, 인수 테스트 | 테스트 보고서 | 결함 관리 |
| **6. 배포/운영** | Deployment | 설치, 사용자 교육 | 운영 매뉴얼 | 전환 테스트 |
| **7. 유지보수** | Maintenance | 수정, 적응, 완전, 예방 유지보수 | 변경 요청, 패치 | 형상 관리 |
| **8. 폐기** | Retirement | 데이터 이관, 시스템 종료 | 폐기 보고서 | 데이터 보안 |

### 2. 정교한 구조 다이어그램: SDLC 전체 구조

```text
================================================================================
|              SOFTWARE DEVELOPMENT LIFE CYCLE (SDLC)                          |
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                            PHASE 1: 계획 (Planning)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  입력:          비즈니스 요구, 아이디어, RFP                                │
│  활동:          ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│                 │ 타당성 조사 │→ │ 범위 정의   │→ │ 자원 계획   │          │
│                 └─────────────┘  └─────────────┘  └─────────────┘          │
│  산출물:        프로젝트 계획서, WBS, 위험 등록부                           │
│  진출기준:      ✓ 계획서 승인  ✓ 예산 확보  ✓ 팀 구성                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      v
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 2: 요구분석 (Analysis)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  입력:          승인된 프로젝트 계획서                                      │
│  활동:          ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│                 │ 요구사항    │→ │ 요구사항    │→ │ 요구사항    │          │
│                 │ 도출        │  │ 분석        │  │ 명세        │          │
│                 └─────────────┘  └─────────────┘  └─────────────┘          │
│  산출물:        SRS, 유스케이스, 요구사항 추적 매트릭스(RTM)                │
│  진출기준:      ✓ SRS 검토 완료  ✓ 요구사항 기준선 확정                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      v
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PHASE 3: 설계 (Design)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  입력:          승인된 SRS                                                   │
│  활동:          ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│                 │ 아키텍처    │→ │ 상세 설계   │→ │ DB 설계     │          │
│                 │ 설계        │  │             │  │             │          │
│                 └─────────────┘  └─────────────┘  └─────────────┘          │
│  산출물:        아키텍처 문서, 상세 설계서, DB 스키마, UI 목업              │
│  진출기준:      ✓ 설계 검토 완료  ✓ 기술 검증 완료                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      v
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 4: 구현 (Implementation)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  입력:          승인된 설계서                                                │
│  활동:          ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│                 │ 코딩        │→ │ 단위 테스트 │→ │ 코드 리뷰   │          │
│                 └─────────────┘  └─────────────┘  └─────────────┘          │
│  산출물:        소스코드, 단위 테스트 케이스, 빌드 스크립트                 │
│  진출기준:      ✓ 코딩 표준 준수  ✓ 단위 테스트 통과  ✓ 정적 분석 통과     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      v
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PHASE 5: 테스트 (Testing)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  입력:          테스트 가능한 빌드                                           │
│  활동:          ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│                 │ 통합 테스트 │→ │ 시스템      │→ │ 인수 테스트 │          │
│                 │             │  │ 테스트      │  │ (UAT)       │          │
│                 └─────────────┘  └─────────────┘  └─────────────┘          │
│  산출물:        테스트 계획서, 테스트 케이스, 결함 보고서, 테스트 결과서    │
│  진출기준:      ✓ 모든 테스트 케이스 수행  ✓ 결함 수정 완료  ✓ UAT 승인    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      v
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PHASE 6: 배포/운영 (Deployment)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  입력:          테스트 완료된 시스템                                         │
│  활동:          ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│                 │ 환경 구성   │→ │ 설치/배포   │→ │ 사용자 교육 │          │
│                 └─────────────┘  └─────────────┘  └─────────────┘          │
│  산출물:        설치 가이드, 운영 매뉴얼, 사용자 교육 자료                  │
│  진출기준:      ✓ 설치 완료  ✓ 데이터 이관 완료  ✓ 교육 완료                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      v
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PHASE 7: 유지보수 (Maintenance)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  유형:                                                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ 수정형      │ │ 적응형      │ │ 완전형      │ │ 예방형      │          │
│  │ Corrective  │ │ Adaptive    │ │ Perfective  │ │ Preventive  │          │
│  │ 버그 수정   │ │ 환경 적응   │ │ 기능 개선   │ │ 사전 예방   │          │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘          │
│  산출물:        변경 요청서, 패치, 업데이트 버전                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      v
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 8: 폐기 (Retirement)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  활동:          데이터 백업 → 데이터 이관 → 시스템 종료 → 기록 보관        │
│  산출물:        폐기 보고서, 데이터 이관 확인서, 보안 폐기 인증서           │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
|                    SDLC QUALITY GATES                                       |
================================================================================

    계획 ──[G1]──> 요구분석 ──[G2]──> 설계 ──[G3]──> 구현 ──[G4]──> 테스트

    G1: 사업 타당성 검토, 승인
    G2: 요구사항 검토(인스펙션), 기준선 확정
    G3: 설계 검토, 기술 검증
    G4: 코드 리뷰, 정적 분석, 단위 테스트 통과
    G5: 테스트 완료, UAT 승인

================================================================================
```

### 3. 심층 동작 원리: V-Model 매핑

V-Model은 SDLC 단계를 테스트 단계와 대응시켜 **요구사항부터 테스트까지 추적성**을 보장합니다.

```
                        V-MODEL 구조
    ============================================================

    요구사항 명세 ─────────────────────────────────────> 인수 테스트
           │                                              ▲
           │                                              │
           v                                              │
    기본 설계 ─────────────────────────────────────> 시스템 테스트
           │                                              ▲
           │                                              │
           v                                              │
    상세 설계 ─────────────────────────────────────> 통합 테스트
           │                                              ▲
           │                                              │
           v                                              │
    코딩/단위테스트 ──────────────────────────────> 단위 테스트
           │                                              ▲
           │                                              │
           v                                              │
    ──────────────────────────────────────────────────────────
                            시간 →

    [매핑 원칙]
    ┌───────────────────┬───────────────────┐
    │   개발 단계        │   테스트 단계      │
    ├───────────────────┼───────────────────┤
    │ 요구사항 명세      │ 인수 테스트 (AT)   │
    │                   │ - 요구사항 충족?   │
    ├───────────────────┼───────────────────┤
    │ 기본 설계         │ 시스템 테스트 (ST)  │
    │ (아키텍처)        │ - 시스템 명세 준수? │
    ├───────────────────┼───────────────────┤
    │ 상세 설계         │ 통합 테스트 (IT)    │
    │ (모듈 인터페이스) │ - 인터페이스 검증  │
    ├───────────────────┼───────────────────┤
    │ 코딩             │ 단위 테스트 (UT)    │
    │                   │ - 모듈 기능 검증   │
    └───────────────────┴───────────────────┘
```

### 4. 핵심 알고리즘/공식 & 실무 코드 예시

#### SDLC 프로세스 추적 시스템

```python
"""
SDLC 단계별 추적 및 게이트 관리 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class Phase(Enum):
    """SDLC 단계 정의"""
    PLANNING = "계획"
    ANALYSIS = "요구분석"
    DESIGN = "설계"
    IMPLEMENTATION = "구현"
    TESTING = "테스트"
    DEPLOYMENT = "배포"
    MAINTENANCE = "유지보수"
    RETIREMENT = "폐기"

class GateStatus(Enum):
    """품질 게이트 상태"""
    PENDING = "대기"
    IN_REVIEW = "검토중"
    PASSED = "통과"
    FAILED = "실패"
    WAIVED = "면제"

@dataclass
class Deliverable:
    """산출물 정의"""
    name: str
    phase: Phase
    required: bool = True
    status: str = "미완료"
    review_result: Optional[str] = None

@dataclass
class QualityGate:
    """품질 게이트 정의"""
    name: str
    phase: Phase
    criteria: List[str]
    status: GateStatus = GateStatus.PENDING
    review_date: Optional[datetime] = None
    reviewer: Optional[str] = None
    comments: str = ""

@dataclass
class SDLCProject:
    """SDLC 프로젝트 관리"""
    name: str
    current_phase: Phase = Phase.PLANNING
    deliverables: List[Deliverable] = field(default_factory=list)
    quality_gates: List[QualityGate] = field(default_factory=list)
    phase_history: Dict[Phase, dict] = field(default_factory=dict)

    def add_deliverable(self, deliverable: Deliverable):
        """산출물 추가"""
        self.deliverables.append(deliverable)

    def add_quality_gate(self, gate: QualityGate):
        """품질 게이트 추가"""
        self.quality_gates.append(gate)

    def evaluate_gate(self, gate_name: str, passed: bool,
                      reviewer: str, comments: str = "") -> bool:
        """품질 게이트 평가"""
        gate = next((g for g in self.quality_gates
                     if g.name == gate_name), None)
        if not gate:
            return False

        gate.status = GateStatus.PASSED if passed else GateStatus.FAILED
        gate.review_date = datetime.now()
        gate.reviewer = reviewer
        gate.comments = comments

        return passed

    def can_advance_to_next_phase(self) -> tuple:
        """다음 단계 진입 가능 여부 확인"""
        current_gates = [g for g in self.quality_gates
                         if g.phase == self.current_phase]

        all_passed = all(g.status == GateStatus.PASSED or
                         g.status == GateStatus.WAIVED
                         for g in current_gates)

        current_deliverables = [d for d in self.deliverables
                                if d.phase == self.current_phase]
        all_delivered = all(d.status == "완료"
                            for d in current_deliverables if d.required)

        blocking_items = []
        for g in current_gates:
            if g.status not in [GateStatus.PASSED, GateStatus.WAIVED]:
                blocking_items.append(f"게이트 미통과: {g.name}")

        for d in current_deliverables:
            if d.required and d.status != "완료":
                blocking_items.append(f"산출물 미완료: {d.name}")

        return all_passed and all_delivered, blocking_items

    def advance_phase(self) -> bool:
        """다음 단계로 진행"""
        can_advance, blockers = self.can_advance_to_next_phase()

        if not can_advance:
            print(f"단계 진입 불가: {blockers}")
            return False

        # 현재 단계 기록
        self.phase_history[self.current_phase] = {
            "completed_at": datetime.now().isoformat(),
            "deliverables": [d.name for d in self.deliverables
                            if d.phase == self.current_phase],
            "gates_passed": [g.name for g in self.quality_gates
                            if g.phase == self.current_phase]
        }

        # 다음 단계로 이동
        phases = list(Phase)
        current_idx = phases.index(self.current_phase)
        if current_idx < len(phases) - 1:
            self.current_phase = phases[current_idx + 1]
            return True

        return False

    def get_phase_progress(self) -> Dict[str, any]:
        """단계별 진척도 조회"""
        progress = {}
        phases = list(Phase)

        for phase in phases:
            phase_deliverables = [d for d in self.deliverables
                                  if d.phase == phase]
            phase_gates = [g for g in self.quality_gates
                           if g.phase == phase]

            completed_deliverables = sum(1 for d in phase_deliverables
                                         if d.status == "완료")
            passed_gates = sum(1 for g in phase_gates
                               if g.status == GateStatus.PASSED)

            progress[phase.value] = {
                "deliverables": f"{completed_deliverables}/{len(phase_deliverables)}",
                "gates": f"{passed_gates}/{len(phase_gates)}",
                "current": phase == self.current_phase
            }

        return progress


# 사용 예시
if __name__ == "__main__":
    # 프로젝트 생성
    project = SDLCProject(name="ERP 시스템 개발")

    # 산출물 정의
    project.add_deliverable(Deliverable("프로젝트 계획서", Phase.PLANNING))
    project.add_deliverable(Deliverable("WBS", Phase.PLANNING))
    project.add_deliverable(Deliverable("요구사항 명세서(SRS)", Phase.ANALYSIS))
    project.add_deliverable(Deliverable("아키텍처 설계서", Phase.DESIGN))
    project.add_deliverable(Deliverable("소스코드", Phase.IMPLEMENTATION))

    # 품질 게이트 정의
    project.add_quality_gate(QualityGate(
        "G1: 계획 승인",
        Phase.PLANNING,
        ["사업 타당성 검토", "예산 승인", "팀 구성 완료"]
    ))
    project.add_quality_gate(QualityGate(
        "G2: 요구사항 검토",
        Phase.ANALYSIS,
        ["요구사항 검토 완료", "이해관계자 승인"]
    ))

    # 게이트 평가
    project.evaluate_gate("G1: 계획 승인", True, "PM 김철수", "승인됨")

    # 산출물 완료 처리
    project.deliverables[0].status = "완료"
    project.deliverables[1].status = "완료"

    # 단계 진행 시도
    can_advance, blockers = project.can_advance_to_next_phase()
    print(f"진입 가능: {can_advance}")
    if blockers:
        print(f"차단 항목: {blockers}")

    # 진척도 조회
    progress = project.get_phase_progress()
    print("\n=== 단계별 진척도 ===")
    for phase, info in progress.items():
        marker = ">>>" if info["current"] else "   "
        print(f"{marker} {phase}: 산출물 {info['deliverables']}, 게이트 {info['gates']}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: SDLC 모델 비교

| 비교 항목 | 폭포수 | V-Model | 나선형 | 애자일 | DevOps |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **구조** | 순차적 | V자형 | 나선형 | 반복적 | 순환형 |
| **단계 전환** | 단방향 | 단방향+역추적 | 반복 | 유연 | 연속 |
| **위험 관리** | 후반 발견 | 중간 | 초기 강화 | 지속 | 자동화 |
| **변경 수용** | 낮음 | 낮음 | 중간 | 높음 | 매우 높음 |
| **문서화** | 상세 | 상세 | 중간 | 최소 | 코드 중심 |
| **적합 분야** | 임베디드 | 안전 중요 | 대형/고위험 | 웹/앱 | 클라우드 |
| **고객 참여** | 시작/끝 | 시작/끝 | 주요 시점 | 지속적 | 지속적 |
| **품질 관리** | 단계별 | V 매핑 | 위험 기반 | TDD/BDD | 자동화 게이트 |

### 2. 과목 융합 관점 분석

#### SDLC + 프로젝트 관리 (PMBOK)

```
[SDLC와 PMBOK 프로세스 매핑]

SDLC 단계          PMBOK 프로세스 그룹
==========         ===================
계획               ┌─────────────────────┐
                   │ 착수 (Initiating)   │
                   │ - 프로젝트 헌장     │
                   │ - 이해관계자 식별   │
                   ├─────────────────────┤
                   │ 계획 (Planning)     │
                   │ - 범위, 일정, 비용  │
                   │ - 위험, 품질 계획   │
                   └─────────────────────┘

요구분석/설계      ┌─────────────────────┐
                   │ 실행 (Executing)    │
                   │ - 요구사항 수집     │
                   │ - 품질 관리         │
                   └─────────────────────┘

구현/테스트        ┌─────────────────────┐
                   │ 실행 + 감시통제     │
                   │ - 품질 통제         │
                   │ - 변경 요청 관리    │
                   └─────────────────────┘

유지보수           ┌─────────────────────┐
                   │ 감시통제 (M&C)      │
                   │ - 통합 변경 통제    │
                   │ - 품질 통제         │
                   └─────────────────────┘

폐기               ┌─────────────────────┐
                   │ 종료 (Closing)      │
                   │ - 인수인계          │
                   │ - 교훈 문서화       │
                   └─────────────────────┘
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오 1] 안전 중요 시스템(원자력 제어)의 SDLC 선택**

**상황**:
- 시스템: 원자력 발전소 제어 시스템
- 요구: 안전성 최우선, 규제 기관 승인 필요
- 특성: 요구사항 안정적, 문서화 필수

**기술사적 판단**:
```
선택: V-Model + IEC 61508 (기능 안전 표준)

근거:
1. 안전 무결성 수준(SIL) 달성 필요
2. 각 단계별 검증(Verification)과 확인(Validation) 명확히 구분
3. 추적성 매트릭스로 요구사항→테스트 매핑 필수
4. 규제 기관 감사 대응을 위한 완전한 문서화

추가 요구사항:
- 독립적 검증(IV&V) 조직 운영
- 형상 관리 엄격 적용
- 안전 케이스(Safety Case) 작성
```

**[시나리오 2] 스타트업의 SaaS 서비스 개발**

**상황**:
- 서비스: B2B SaaS 플랫폼
- 시장: 빠른 시장 진입 필요, 요구사항 불확실
- 팀: 8명, 애자일 경험 있음

**기술사적 판단**:
```
선택: 스크럼 + CI/CD (DevOps SDLC)

근거:
1. 2주 스프린트로 빠른 피드백
2. MVP 우선 개발, 점진적 기능 확장
3. 자동화된 품질 게이트 (테스트, 보안 스캔)
4. 일일 배포 가능한 파이프라인

단계별 적용:
- 스프린트 0: 제품 백로그, 아키텍처 기본
- 스프린트 1~N: 기능 개발, 지속적 배포
- 매 스프린트: 회고로 프로세스 개선
```

### 2. 도입 시 고려사항 (체크리스트)

**SDLC 모델 선택 체크리스트**:

| 고려 항목 | 폭포수/V-Model | 애자일 | DevOps |
| :--- | :--- | :--- | :--- |
| 요구사항 안정성 | 높음 | 낮음~중간 | 낮음~높음 |
| 규제/감사 요구 | 높음 | 낮음~중간 | 중간 |
| 팀 크기 | 대규모 | 소~중규모 | 모든 규모 |
| 변경 빈도 | 낮음 | 높음 | 매우 높음 |
| 안전 중요성 | 높음 | 낮음~중간 | 중간 |
| 자동화 역량 | 낮음 | 중간 | 높음 |

### 3. 주의사항 및 안티패턴

| 안티패턴 | 설명 | 해결 방안 |
| :--- | :--- | :--- |
| **단계 건너뛰기** | 설계 없이 바로 코딩 | 최소 설계 의무화 |
| **품질 게이트 무시** | 일정 압박으로 게이트 우회 | 게이트 강제 적용 |
| **문서 과잉/부족** | 필요 이상 문서 또는 문서 없음 | 테일러링으로 최적화 |
| **단계 완료 착각** | "90% 완료" 지속 | 정량적 진출 기준 설정 |

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | 비체계적 개발 | SDLC 적용 | 개선 효과 |
| :--- | :--- | :--- | :--- | :--- |
| **요구사항** | 누락률 | 35% | 10% | -25%p |
| **재작업** | 비용 비중 | 40% | 15% | -25%p |
| **일정 준수** | 준수율 | 45% | 75% | +30%p |
| **결함** | 후반 발견률 | 60% | 25% | -35%p |
| **유지보수** | TCO 비중 | 70% | 45% | -25%p |

### 2. 미래 전망 및 진화 방향

1. **AI 통합 SDLC**
   - LLM 기반 요구사항 분석, 코드 생성
   - 자동화된 품질 게이트, 예측적 분석

2. **지속적 모든 것 (Continuous Everything)**
   - Continuous Planning, Continuous Design
   - Continuous Testing, Continuous Security

3. **하이브리드 SDLC**
   - 조직 내 여러 모델 혼합 운영
   - 프로젝트 특성별 맞춤형 테일러링

### ※ 참고 표준/가이드

- **ISO/IEC 12207**: 소프트웨어 생명주기 프로세스
- **ISO/IEC 15288**: 시스템 생명주기 프로세스
- **IEEE 1074**: 소프트웨어 생명주기 프로세스 개발 표준
- **CMMI V2.0**: 프로세스 성숙도 모델
- **PMBOK 7th**: 프로젝트 관리 지식체계

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [폭포수 모델](@/studynotes/4_software_engineering/1_sdlc/_index.md) : 가장 전통적인 SDLC 모델
- [V-Model](@/studynotes/4_software_engineering/1_sdlc/_index.md) : 개발-테스트 대응 모델
- [애자일 방법론](@/studynotes/4_software_engineering/1_sdlc/agile_methodology.md) : 반복적 SDLC
- [DevOps](@/studynotes/4_software_engineering/1_sdlc/devops.md) : 개발-운영 통합 SDLC
- [형상 관리](@/studynotes/4_software_engineering/1_sdlc/configuration_management.md) : SDLC의 변경 관리
- [ISO 12207](@/studynotes/4_software_engineering/1_sdlc/iso12207.md) : SDLC 국제 표준

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 레고로 멋진 성을 짓고 싶은데 아무 계획 없이 시작했어요. 그랬더니 중간에 블록이 모자라거나, 만들다가 무너지거나, 완성했는데 엉망이 되었어요!

2. **해결(SDLC)**: 그래서 '만드는 순서'를 정했어요. 1단계: 무엇을 만들지 계획하기, 2단계: 설계도 그리기, 3단계: 필요한 블록 모으기, 4단계: 조립하기, 5단계: 흔들어서 튼튼한지 확인하기!

3. **효과**: 이 순서대로 하니까 실패하지 않고 멋진 성을 완성할 수 있었어요! 컴퓨터 프로그램도 이렇게 순서대로 만들면 성공적으로 완성할 수 있어요. 이것이 바로 SDLC랍니다!
