+++
title = "폭포수 모델 (Waterfall Model)"
date = 2024-05-24
description = "소프트웨어 개발 단계를 순차적으로 진행하는 전통적 생명주기 모델"
weight = 40
+++

# 폭포수 모델 (Waterfall Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 폭포수 모델은 **1970년 Winston Royce**가 제안한 SDLC 모델로, 요구분석→설계→구현→테스트→운영의 **단계가 폭포처럼 일방향으로 흐르는 순차적 개발 방식**입니다. 각 단계는 명확한 **진입/진출 기준**을 가지며, 이전 단계가 완료되어야 다음 단계로 진행합니다.
> 2. **가치**: 요구사항이 안정적이고 문서화가 중요한 **임베디드, 국방, 항공우주, 원자력** 등 안전 중요 시스템에서 **예측 가능한 일정과 품질**을 보장하며, 계약 및 감사 대응에 유리합니다.
> 3. **융합**: 변경에 취약하다는 한계를 보완하기 위해 **V-Model, 나선형, 반복적 폭포수** 등으로 진화했으며, 현대에는 **애자일과 하이브리드** 형태로 결합되어 사용됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**폭포수 모델(Waterfall Model)**은 소프트웨어 개발 과정을 **계단식으로 순차적으로 진행**하는 가장 전통적인 생명주기 모델입니다. 물이 폭포에서 떨어지면 다시 올라갈 수 없듯이, 한 단계가 완료되면 **되돌아갈 수 없다는 원칙**을 기본으로 합니다(실제로는 제한적 피드백 허용).

**폭포수 모델의 6단계 구조**:

| 단계 | 영문명 | 핵심 활동 | 주요 산출물 | 완료 기준 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 요구사항** | Requirements | 요구사항 수집, 분석, 명세 | SRS (Software Requirements Spec) | 요구사항 검토 승인 |
| **2. 분석** | Analysis | 시스템 분석, 논리 설계 | 시스템 명세서, 논리 모델 | 분석 검토 승인 |
| **3. 설계** | Design | 아키텍처, 상세 설계 | 설계 문서, DB 스키마 | 설계 검토 승인 |
| **4. 코딩** | Coding | 프로그래밍, 단위 테스트 | 소스코드, 실행 모듈 | 코딩 표준 준수 |
| **5. 테스트** | Testing | 통합, 시스템, 인수 테스트 | 테스트 보고서 | 테스트 완료, 결함 해결 |
| **6. 운영** | Operations | 설치, 유지보수 | 운영 매뉴얼 | 안정적 운영 |

**폭포수 모델의 핵심 원칙**:

```
1. 순차성 (Sequentiality)
   - 단계는 정해진 순서대로만 진행
   - 이전 단계 완료 = 다음 단계 진입 조건

2. 단계별 완결성 (Phase Completeness)
   - 각 단계는 명확한 시작과 끝이 있음
   - "완료"의 정의가 명확해야 함

3. 문서 중심 (Documentation-Driven)
   - 모든 단계의 결과는 문서화
   - 문서가 다음 단계의 입력

4. 검증 중심 (Verification-Oriented)
   - 각 단계 종료 시 공식 검토(Review)
   - 품질 게이트(Quality Gate) 통과 필요

5. 변경 통제 (Change Control)
   - 일단 완료된 단계로의 피드백은 제한적
   - 변경은 공식 절차를 통해서만 가능
```

### 💡 일상생활 비유: 건축 과정

```
[폭포수 모델 = 건축 과정]

건축 단계                    폭포수 모델 단계
==========                   ================
1. 설계도 그리기              1. 요구사항 분석
   │                           │
   │ "거실 20평, 침실 3개"      │ "기능 A, 성능 B"
   │ 건축가와 협의              │ 사용자 인터뷰
   v                           v
2. 건축 허가                  2. 시스템 분석
   │                           │
   │ 구조 계산, 안전 검토       │ 타당성 분석
   v                           v
3. 기초 공사                  3. 설계
   │                           │
   │ 콘크리트 타설              │ 아키텍처 설계
   │ (이후 변경 불가!)          │ (기본 구조 확정)
   v                           v
4. 골조 공사                  4. 코딩
   │                           │
   │ 기둥, 보, 지붕             │ 모듈 구현
   v                           v
5. 마감 공사                  5. 테스트
   │                           │
   │ 도장, 설비 설치            │ 통합/시스템 테스트
   │ 하자 점검                  │ 결함 수정
   v                           v
6. 입주/거주                  6. 운영/유지보수
   │                           │
   │ 수리, 리모델링             │ 유지보수
   v                           v

핵심 유사점:
- 기초 공사 후에 "방 하나 더 늘려주세요"라면?
  → 건축: 엄청난 비용 발생 (기초 다시)
  → 폭포수: 요구사항 단계로 복귀 필요 (재작업 비용 큼)
- 그래서 설계도를 꼼꼼히 확인하는 것이 중요!
```

### 2. 등장 배경 및 발전 과정

#### 1) 1950~60년대: 코딩 중심 시대

**배경**:
- 소프트웨어 규모가 작고 단순
- 하드웨어 비용이 지배적
- "그냥 짜면 됨" 시대

**문제점**:
- 소프트웨어 규모 증가 → 혼란
- 유지보수 곤란
- 품질 저하

#### 2) 1970년: Winston Royce의 제안

**Winston W. Royce (1970)**:
> "Managing the Development of Large Software Systems"
> IEEE Proceedings, 1970

```
원래 논문의 의도:
- 실제로는 "순수 폭포수는 위험하다"고 경고
- 반복과 피드백이 필요하다고 주장
- 하지만 논문의 그림만 인용되어 "폭포수 모델"로 알려짐

Royce가 제안한 실제 모델:
요구사항 → 설계 → 구현 → 테스트
    ↑_________________________|
         (피드백 루프)
```

#### 3) 1980~90년대: 표준화와 보완

| 발전 | 내용 |
| :--- | :--- |
| **DOD-STD-2167A** | 미 국방부 표준, 폭포수 기반 |
| **IEEE 1016** | 설계 문서 표준 |
| **ISO 12207** | 생명주기 프로세스 표준 |
| **수정 폭포수** | 제한적 피드백 허용 |
| **V-Model** | 테스트 단계 매핑 추가 |

#### 4) 2000년대~현재: 애자일과 공존

```
폭포수 vs 애자일 논쟁 → 하이브리드 접근

현대적 관점:
- 폭포수: 문서 중심, 예측 가능, 규제 대응
- 애자일: 변화 수용, 빠른 피드백, 고객 중심

상황에 따른 선택:
┌───────────────────┬───────────────────┐
│ 폭포수 적합       │ 애자일 적합        │
├───────────────────┼───────────────────┤
│ 안전 중요 시스템  │ 스타트업          │
│ 규제/감사 대상    │ 웹/모바일 앱      │
│ 요구사항 안정     │ 요구사항 불확실   │
│ 대형 SI 프로젝트  │ SaaS 서비스       │
└───────────────────┴───────────────────┘
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 폭포수 모델 단계별 상세 구조

| 단계 | 입력 | 핵심 활동 | 산출물 | 검증 방법 | 진출 기준 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **요구사항** | RFP, 사용자 요구 | 인터뷰, 설문, 프로토타입 | SRS, 유스케이스 | 요구사항 검토 | 승인된 SRS |
| **시스템 분석** | SRS | DFD, ERD, 상태 다이어그램 | 분석 명세서 | 기술 검토 | 분석서 승인 |
| **설계** | 분석 명세서 | 아키텍처, 모듈, DB 설계 | 설계 문서 | 설계 검토 | 설계서 승인 |
| **코딩** | 설계 문서 | 프로그래밍, 단위 테스트 | 소스코드 | 코드 리뷰 | 코딩 완료 |
| **테스트** | 소스코드, 테스트 계획 | 통합/시스템/인수 테스트 | 테스트 보고서 | 테스트 수행 | 모든 TC 통과 |
| **운영** | 테스트 완료 시스템 | 설치, 교육, 유지보수 | 운영 매뉴얼 | 운영 전환 | 안정 운영 |

### 2. 정교한 구조 다이어그램: 폭포수 모델 전체 구조

```text
================================================================================
|                    WATERFALL MODEL ARCHITECTURE                             |
================================================================================

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                         PHASE 1: REQUIREMENTS                            │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                         │
    │   입력: RFP, 비즈니스 요구, 사용자 인터뷰                               │
    │                                                                         │
    │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
    │   │   요구사항   │───>│   요구사항   │───>│   요구사항   │            │
    │   │   수집       │    │   분석       │    │   명세       │            │
    │   └──────────────┘    └──────────────┘    └──────────────┘            │
    │          │                   │                   │                     │
    │          v                   v                   v                     │
    │   - 인터뷰            - 우선순위          - SRS 작성                   │
    │   - 설문조사          - 충돌 해결         - 유스케이스                 │
    │   - 관찰              - 범위 확정         - 인수 기준                  │
    │                                                                         │
    │   산출물: SRS (Software Requirements Specification)                     │
    │   검증: 요구사항 검토 회의 (Requirements Review)                        │
    │   진출기준: ✓ SRS 승인  ✓ 요구사항 기준선 확정                         │
    │                                                                         │
    │   ┌─────────────────────────────────────────────────────────┐          │
    │   │              📋 QUALITY GATE 1: Requirements Review      │          │
    │   │  - 완전성: 모든 요구사항이 포함되었는가?                 │          │
    │   │  - 일관성: 요구사항 간 모순이 없는가?                    │          │
    │   │  - 명확성: 모호하지 않고 해석이 분명한가?                │          │
    │   │  - 검증가능성: 테스트로 확인 가능한가?                   │          │
    │   └─────────────────────────────────────────────────────────┘          │
    └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 승인
                                      v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                         PHASE 2: SYSTEM ANALYSIS                         │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                         │
    │   입력: 승인된 SRS                                                      │
    │                                                                         │
    │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
    │   │   구조적      │───>│   데이터     │───>│   프로세스   │            │
    │   │   분석        │    │   모델링     │    │   모델링     │            │
    │   └──────────────┘    └──────────────┘    └──────────────┘            │
    │          │                   │                   │                     │
    │          v                   v                   v                     │
    │   - DFD 작성          - ERD 작성          - 상태 다이어그램           │
    │   - 자료 사전         - 정규화            - 프로세스 정의              │
    │   - 미니 스펙         - DB 설계           - 업무 규칙                  │
    │                                                                         │
    │   산출물: 시스템 분석 명세서, DFD, ERD, 자료 사전                      │
    │   검증: 기술 검토 (Technical Review)                                    │
    │   진출기준: ✓ 분석 문서 승인  ✓ 논리 모델 확정                         │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 승인
                                      v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                         PHASE 3: DESIGN                                  │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                         │
    │   입력: 분석 명세서                                                     │
    │                                                                         │
    │   ┌─────────────────────────────────────────────────────────┐          │
    │   │                     설계 단계 세분화                     │          │
    │   ├─────────────────────────────────────────────────────────┤          │
    │   │                                                         │          │
    │   │  기본 설계 (Preliminary Design)                         │          │
    │   │  ├── 아키텍처 설계                                      │          │
    │   │  ├── 시스템 구조                                        │          │
    │   │  └── 인터페이스 정의                                    │          │
    │   │           │                                             │          │
    │   │           v                                             │          │
    │   │  상세 설계 (Detailed Design)                            │          │
    │   │  ├── 모듈 설계                                          │          │
    │   │  ├── 알고리즘 설계                                      │          │
    │   │  ├── DB 물리 설계                                      │          │
    │   │  └── UI 설계                                           │          │
    │   │                                                         │          │
    │   └─────────────────────────────────────────────────────────┘          │
    │                                                                         │
    │   산출물: 설계 문서, 아키텍처 다이어그램, DB 스키마, UI 목업            │
    │   검증: 설계 검토 (Design Review / PDR / CDR)                           │
    │   진출기준: ✓ 설계 문서 승인  ✓ 기술 검증 완료                         │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 승인
                                      v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                         PHASE 4: CODING                                  │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                         │
    │   입력: 승인된 설계 문서                                                │
    │                                                                         │
    │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
    │   │   코딩       │───>│   단위 테스트 │───>│   코드 리뷰  │            │
    │   └──────────────┘    └──────────────┘    └──────────────┘            │
    │          │                   │                   │                     │
    │          v                   v                   v                     │
    │   - 코딩 표준 준수    - 화이트박스        - 동료 검토                   │
    │   - 모듈 구현        - 커버리지 80%+     - 정적 분석                   │
    │   - 인터페이스 구현   - mock/stub 활용    - 복잡도 측정                │
    │                                                                         │
    │   산출물: 소스코드, 단위 테스트 케이스, 빌드 스크립트                  │
    │   검증: 코드 리뷰, 정적 분석                                            │
    │   진출기준: ✓ 코딩 완료  ✓ 단위 테스트 통과  ✓ 코드 리뷰 완료          │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 승인
                                      v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                         PHASE 5: TESTING                                 │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                         │
    │   입력: 테스트 가능한 빌드, 테스트 계획서                               │
    │                                                                         │
    │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
    │   │  통합 테스트  │───>│ 시스템 테스트 │───>│  인수 테스트  │            │
    │   │    (IT)      │    │    (ST)      │    │    (AT)      │            │
    │   └──────────────┘    └──────────────┘    └──────────────┘            │
    │          │                   │                   │                     │
    │          v                   v                   v                     │
    │   - 모듈 간 인터페이스 - 기능/비기능       - 사용자 참여                │
    │   - 빅뱅/상향/하향     - 성능/보안        - 비즈니스 시나리오           │
    │   - 결함 발견/수정     - 회귀 테스트      - 최종 승인                   │
    │                                                                         │
    │   산출물: 테스트 계획서, 테스트 케이스, 결함 보고서, 테스트 결과서      │
    │   검증: 테스트 수행, 결함 추적                                          │
    │   진출기준: ✓ 모든 TC 수행  ✓ 결함 수정  ✓ UAT 승인                    │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ 승인
                                      v
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                      PHASE 6: OPERATIONS                                 │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                         │
    │   입력: 테스트 완료 시스템                                               │
    │                                                                         │
    │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
    │   │   배포       │───>│   교육       │───>│  유지보수    │            │
    │   └──────────────┘    └──────────────┘    └──────────────┘            │
    │                                                                         │
    │   산출물: 운영 매뉴얼, 사용자 교육 자료, 변경 요청 처리 결과            │
    │   검증: 운영 전환 테스트, 사용자 교육 평가                              │
    │   진출기준: ✓ 안정적 운영  ✓ 사용자 교육 완료                          │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
|                    FEEDBACK (제한적)                                        |
================================================================================

    실제로는 제한된 피드백이 허용됨:

    요구사항 <─────────────────────────────────────┐
        │                                          │
        v                                          │
    분석 <───────────────────────────────┐         │
        │                                 │         │
        v                                 │         │
    설계 <──────────────────────┐        │         │
        │                        │        │         │
        v                        │        │         │
    코딩 <───────────────┐      │        │         │
        │                 │      │        │         │
        v                 │      │        │         │
    테스트 ───────────────┘      │        │         │
        │                        │        │         │
        v                        │        │         │
    운영 ────────────────────────┘────────┘─────────┘

    (수정된 폭포수 모델: 단계 간 피드백 허용)

================================================================================
```

### 3. 심층 동작 원리: 단계별 검증 프로세스

```
폭포수 모델의 핵심: 각 단계별 공식 검증

┌─────────────────────────────────────────────────────────────────┐
│                   VERIFICATION & VALIDATION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  검증 (Verification)                                            │
│  "제품을 올바르게 만들고 있는가?"                                │
│  - 요구사항 → 설계 일치 검증                                    │
│  - 설계 → 코드 일치 검증                                        │
│  - 단계별 산출물 검토                                           │
│                                                                 │
│  확인 (Validation)                                              │
│  "올바른 제품을 만들었는가?"                                     │
│  - 최종 산출물이 사용자 요구 충족                                │
│  - 인수 테스트                                                  │
│  - 사용자 승인                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

[단계별 검토 유형]

1. 요구사항 검토 (Requirements Review)
   - 대상: SRS
   - 참여자: 사용자, 분석가, 프로젝트 관리자
   - 체크리스트:
     □ 완전성: 누락된 요구사항 없는가?
     □ 일관성: 모순되는 요구사항 없는가?
     □ 명확성: 모호한 표현 없는가?
     □ 검증가능성: 테스트 가능한가?
     □ 추적가능성: 출처 파악 가능한가?

2. 설계 검토 (Design Review)
   - PDR (Preliminary Design Review): 기본 설계 검토
   - CDR (Critical Design Review): 상세 설계 검토
   - 체크리스트:
     □ 아키텍처 적절성
     □ 인터페이스 일관성
     □ 성능 달성 가능성
     □ 확장성

3. 코드 리뷰 (Code Review)
   - 방식: 인스펙션, 워크쓰루, 페어 프로그래밍
   - 체크리스트:
     □ 코딩 표준 준수
     □ 논리적 정확성
     □ 예외 처리
     □ 성능 고려

4. 테스트 검토 (Test Review)
   - 테스트 계획서 검토
   - 테스트 케이스 리뷰
   - 테스트 결과 분석
```

### 4. 핵심 알고리즘/공식 & 실무 코드 예시

#### 폭포수 모델 프로젝트 관리자

```python
"""
폭포수 모델 단계 관리 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timedelta

class Phase(Enum):
    """폭포수 모델 단계"""
    REQUIREMENTS = "요구사항"
    ANALYSIS = "분석"
    DESIGN = "설계"
    CODING = "구현"
    TESTING = "테스트"
    OPERATIONS = "운영"

class PhaseStatus(Enum):
    """단계 상태"""
    NOT_STARTED = "미시작"
    IN_PROGRESS = "진행중"
    COMPLETED = "완료"
    BLOCKED = "차단됨"

@dataclass
class Deliverable:
    """산출물"""
    name: str
    required: bool = True
    status: str = "미완료"
    approved: bool = False
    approver: Optional[str] = None

@dataclass
class QualityGate:
    """품질 게이트"""
    name: str
    criteria: List[str]
    passed: bool = False
    review_date: Optional[datetime] = None
    reviewer: Optional[str] = None
    defects_found: int = 0
    defects_fixed: int = 0

@dataclass
class WaterfallPhase:
    """폭포수 모델 단계"""
    phase: Phase
    status: PhaseStatus = PhaseStatus.NOT_STARTED
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    planned_duration: int = 0  # 일
    deliverables: List[Deliverable] = field(default_factory=list)
    quality_gates: List[QualityGate] = field(default_factory=list)
    dependencies: List[Phase] = field(default_factory=list)

    def can_start(self, completed_phases: List[Phase]) -> tuple:
        """시작 가능 여부 확인"""
        blocking = []
        for dep in self.dependencies:
            if dep not in completed_phases:
                blocking.append(dep.value)
        return len(blocking) == 0, blocking

    def can_complete(self) -> tuple:
        """완료 가능 여부 확인"""
        blockers = []

        # 산출물 검사
        for d in self.deliverables:
            if d.required and not d.approved:
                blockers.append(f"산출물 미승인: {d.name}")

        # 품질 게이트 검사
        for g in self.quality_gates:
            if not g.passed:
                blockers.append(f"게이트 미통과: {g.name}")

        return len(blockers) == 0, blockers

@dataclass
class WaterfallProject:
    """폭포수 모델 프로젝트"""
    name: str
    phases: Dict[Phase, WaterfallPhase] = field(default_factory=dict)
    completed_phases: List[Phase] = field(default_factory=list)

    def setup_standard_phases(self):
        """표준 폭포수 단계 설정"""
        phase_order = [
            (Phase.REQUIREMENTS, ["요구사항 명세서(SRS)", "유스케이스 명세서"]),
            (Phase.ANALYSIS, ["시스템 분석서", "DFD", "ERD"]),
            (Phase.DESIGN, ["설계 문서", "DB 설계서", "UI 설계서"]),
            (Phase.CODING, ["소스코드", "단위 테스트 결과"]),
            (Phase.TESTING, ["테스트 계획서", "테스트 결과서", "결함 보고서"]),
            (Phase.OPERATIONS, ["운영 매뉴얼", "사용자 교육 자료"]),
        ]

        prev_phase = None
        for phase, deliverable_names in phase_order:
            deliverables = [Deliverable(name) for name in deliverable_names]

            dependencies = []
            if prev_phase:
                dependencies.append(prev_phase)

            self.phases[phase] = WaterfallPhase(
                phase=phase,
                deliverables=deliverables,
                dependencies=dependencies
            )

            # 품질 게이트 추가
            self.phases[phase].quality_gates.append(
                QualityGate(
                    name=f"{phase.value} 검토",
                    criteria=["완전성", "일관성", "정확성"]
                )
            )

            prev_phase = phase

    def start_phase(self, phase: Phase) -> bool:
        """단계 시작"""
        wf_phase = self.phases.get(phase)
        if not wf_phase:
            return False

        can_start, blockers = wf_phase.can_start(self.completed_phases)
        if not can_start:
            print(f"시작 불가: {blockers}")
            return False

        wf_phase.status = PhaseStatus.IN_PROGRESS
        wf_phase.start_date = datetime.now()
        return True

    def complete_phase(self, phase: Phase) -> bool:
        """단계 완료"""
        wf_phase = self.phases.get(phase)
        if not wf_phase:
            return False

        can_complete, blockers = wf_phase.can_complete()
        if not can_complete:
            print(f"완료 불가: {blockers}")
            return False

        wf_phase.status = PhaseStatus.COMPLETED
        wf_phase.end_date = datetime.now()
        self.completed_phases.append(phase)
        return True

    def approve_deliverable(self, phase: Phase, deliverable_name: str,
                           approver: str) -> bool:
        """산출물 승인"""
        wf_phase = self.phases.get(phase)
        if not wf_phase:
            return False

        for d in wf_phase.deliverables:
            if d.name == deliverable_name:
                d.approved = True
                d.approver = approver
                d.status = "완료"
                return True
        return False

    def pass_quality_gate(self, phase: Phase, gate_name: str,
                         reviewer: str, defects: int = 0) -> bool:
        """품질 게이트 통과"""
        wf_phase = self.phases.get(phase)
        if not wf_phase:
            return False

        for g in wf_phase.quality_gates:
            if g.name == gate_name:
                g.passed = True
                g.review_date = datetime.now()
                g.reviewer = reviewer
                g.defects_found = defects
                g.defects_fixed = defects  # 모두 수정됨
                return True
        return False

    def get_progress(self) -> Dict:
        """진척도 조회"""
        total = len(self.phases)
        completed = len(self.completed_phases)
        in_progress = sum(1 for p in self.phases.values()
                         if p.status == PhaseStatus.IN_PROGRESS)

        return {
            "total_phases": total,
            "completed": completed,
            "in_progress": in_progress,
            "percentage": (completed / total * 100) if total > 0 else 0,
            "current_phase": next(
                (p.value for p in self.phases.values()
                 if p.status == PhaseStatus.IN_PROGRESS),
                "없음"
            )
        }

    def get_gantt_chart_data(self) -> List[Dict]:
        """간트 차트 데이터"""
        data = []
        base_date = datetime.now()

        for i, (phase, wf_phase) in enumerate(self.phases.items()):
            start = base_date + timedelta(days=sum(
                self.phases[p].planned_duration or 20
                for p in list(self.phases.keys())[:i]
            ))
            end = start + timedelta(days=wf_phase.planned_duration or 20)

            data.append({
                "phase": phase.value,
                "start": start.strftime("%Y-%m-%d"),
                "end": end.strftime("%Y-%m-%d"),
                "status": wf_phase.status.value
            })

        return data


# 사용 예시
if __name__ == "__main__":
    project = WaterfallProject(name="은행 시스템 구축")
    project.setup_standard_phases()

    # 요구사항 단계 시작
    project.start_phase(Phase.REQUIREMENTS)

    # 산출물 승인
    project.approve_deliverable(Phase.REQUIREMENTS, "요구사항 명세서(SRS)", "PM 김철수")
    project.approve_deliverable(Phase.REQUIREMENTS, "유스케이스 명세서", "PM 김철수")

    # 품질 게이트 통과
    project.pass_quality_gate(Phase.REQUIREMENTS, "요구사항 검토", "QA 박영희", 2)

    # 단계 완료
    project.complete_phase(Phase.REQUIREMENTS)

    # 진척도 확인
    progress = project.get_progress()
    print(f"=== 프로젝트 진척도 ===")
    print(f"완료: {progress['completed']}/{progress['total_phases']}")
    print(f"진행률: {progress['percentage']:.1f}%")
    print(f"현재 단계: {progress['current_phase']}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 폭포수 vs 다른 모델

| 비교 항목 | 폭포수 | V-Model | 나선형 | 애자일 |
| :--- | :--- | :--- | :--- | :--- |
| **구조** | 선형 순차 | V자형 | 나선형 반복 | 반복적 |
| **단계 전환** | 단방향 | 단방향+역추적 | 반복 | 유연 |
| **변경 비용** | 매우 높음 | 높음 | 중간 | 낮음 |
| **위험 식별** | 후반 | 중반 | 초기 | 지속 |
| **고객 참여** | 시작/끝 | 시작/끝 | 주요 시점 | 지속 |
| **문서화** | 상세 | 상세 | 중간 | 최소 |
| **예측 가능성** | 높음 | 높음 | 중간 | 낮음 |
| **적합 분야** | 임베디드, 국방 | 안전 중요 | 대형/고위험 | 웹/앱 |

### 2. 과목 융합 관점 분석

#### 폭포수 모델 + 형상 관리

```
[폭포수 모델에서의 형상 관리]

1. 단계별 기준선(Baseline) 관리
   ┌────────────────────────────────────────────┐
   │ 요구사항 기준선                            │
   │ - 승인된 SRS                               │
   │ - 변경은 CCB(변경통제위원회) 승인 필요     │
   ├────────────────────────────────────────────┤
   │ 설계 기준선                                │
   │ - 승인된 설계 문서                         │
   │ - 요구사항과의 추적성 유지                 │
   ├────────────────────────────────────────────┤
   │ 제품 기준선                                │
   │ - 테스트 완료된 제품                       │
   │ - 출시 버전 관리                           │
   └────────────────────────────────────────────┘

2. 변경 통제 프로세스
   변경 요청 → 영향 분석 → CCB 심의 → 승인/반려 → 변경 수행 → 검증

3. 형상 감사
   - 기능적 감사: 요구사항 충족 여부
   - 물리적 감사: 산출물 일치 여부
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오 1] 국방 SI 프로젝트**

**상황**:
- 규모: 500억, 100인, 36개월
- 특성: 요구사항 안정, 규제 준수, 감사 대상
- 고객: 국방기술품질원

**기술사적 판단**:
```
선택: 폭포수 모델 + MIL-STD-498

근거:
1. 국방 표준 준수: MIL-STD-498은 폭포수 기반
2. 문서화 요구: 완전한 SRS, SDD, IDD 등 필수
3. 감사 대응: 각 단계별 산출물로 객관적 증거 확보
4. 계약 관리: 단계별 승인으로 진척 관리

단계별 강조점:
- 요구사항: 철저한 분석, CCB 운영
- 설계: PDR/CDR 공식 검토
- 테스트: 독립적 검증(IV&V)
```

**[시나리오 2] 요구사항이 불확실한 웹 서비스**

**상황**:
- 서비스: 신규 SaaS 플랫폼
- 시장: 빠른 변화, 경쟁 심화
- 요구사항: "사용자 반응 보면서 수정"

**기술사적 판단**:
```
선택: 폭포수 모델 부적합 → 애자일 권장

폭포수가 부적합한 이유:
1. 요구사항 불확실: 초기에 모든 요구사항 정의 불가
2. 변경 빈번: 시장 반응에 따른 잦은 변경
3. 출시 속도: 6개월 후 출시면 이미 늦음
4. 고객 참여: 지속적 피드백 필요

대안: 스크럼 + CI/CD
- 2주 스프린트
- MVP 우선 출시
- 지속적 배포
```

### 2. 도입 시 고려사항 (체크리스트)

**폭포수 모델 적합성 체크리스트**:

| 항목 | 예 | 아니오 |
| :--- | :---: | :---: |
| 요구사항이 초기에 확정 가능한가? | □ | □ |
| 프로젝트 기간 동안 요구사항 변경이 10% 미만인가? | □ | □ |
| 규제/감사로 인한 문서화 요구가 있는가? | □ | □ |
| 안전/보안이 중요한 시스템인가? | □ | □ |
| 고객이 단계별 승인 방식에 동의하는가? | □ | □ |
| 팀이 충분한 경험과 역량을 가졌는가? | □ | □ |

→ 4개 이상 '예'면 폭포수 모델 고려

### 3. 주의사항 및 안티패턴

| 안티패턴 | 설명 | 해결 방안 |
| :--- | :--- | :--- |
| **분석 마비** | 요구사항 단계에서 과도한 시간 소요 | 타임박스 설정, 80% 원칙 |
| **90% 완료 착각** | "90% 완료"가 반복됨 | 정량적 진출 기준 설정 |
| **문서 과잉** | 필요 이상의 문서 작성 | 테일러링으로 문서 최적화 |
| **변경 거부** | 정당한 변경 요청도 거부 | 유연한 변경 관리 프로세스 |

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | 비체계적 개발 | 폭포수 적용 | 개선 효과 |
| :--- | :--- | :--- | :--- | :--- |
| **일정 예측** | 일정 오차율 | ±50% | ±15% | +35%p |
| **요구사항** | 추적 가능성 | 30% | 95% | +65%p |
| **문서화** | 완전성 | 40% | 90% | +50%p |
| **감사 대응** | 준비 시간 | 4주 | 1주 | -75% |
| **유지보수** | 인수인계 시간 | 2주 | 2일 | -85% |

### 2. 미래 전망 및 진화 방향

1. **하이브리드 접근**
   - 초기 요구사항: 폭포수 방식
   - 개발/테스트: 애자일 방식
   - "Water-Scrum-Fall" 모델

2. **자동화된 문서화**
   - 코드에서 문서 자동 생성
   - 추적성 매트릭스 자동 관리

3. **규제 대응 강화**
   - GDPR, AI Act 등 새로운 규제
   - 컴플라이언스 문서화 요구 증가

### ※ 참고 표준/가이드

- **IEEE 830**: 소프트웨어 요구사항 명세서 가이드
- **IEEE 1016**: 소프트웨어 설계 설명서 표준
- **MIL-STD-498**: 국방 소프트웨어 개발 표준
- **ISO/IEC 12207**: 소프트웨어 생명주기 프로세스
- **DOD-STD-2167A**: 미 국방부 소프트웨어 개발 표준

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [SDLC](@/studynotes/4_software_engineering/1_sdlc/3_sdlc.md) : 폭포수 모델의 상위 개념
- [V-Model](@/studynotes/4_software_engineering/1_sdlc/_index.md) : 폭포수 + 테스트 매핑
- [나선형 모델](@/studynotes/4_software_engineering/1_sdlc/_index.md) : 위험 분석 추가 모델
- [애자일 방법론](@/studynotes/4_software_engineering/1_sdlc/agile_methodology.md) : 폭포수의 대안
- [형상 관리](@/studynotes/4_software_engineering/1_sdlc/configuration_management.md) : 폭포수의 필수 지원 활동
- [요구사항 명세](@/studynotes/4_software_engineering/2_requirement/_index.md) : 폭포수 첫 단계

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 숙제를 하는데 아무 계획 없이 시작했어요. 읽기 과제를 하다가 갑자기 글쓰기가 하고 싶어지고, 또 다시 읽기로 돌아가고... 이러다가는 영원히 끝나지 않겠죠?

2. **해결(폭포수 모델)**: 그래서 순서를 정했어요! 1단계: 읽기, 2단계: 요약하기, 3단계: 글쓰기, 4단계: 검토하기. 한 단계가 끝나면 다음 단계로만 가요. 다시 돌아갈 수 없어요!

3. **효과**: 이렇게 하니까 숙제가 빨리 끝났어요! 물론 중간에 "아, 이거 읽어야 했는데!" 할 수도 있지만, 그래도 순서대로 하면 혼란스럽지 않아요. 컴퓨터 프로그램도 이렇게 순서대로 만들면 성공적으로 완성된답니다!
