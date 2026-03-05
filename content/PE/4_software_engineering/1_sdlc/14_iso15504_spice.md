+++
title = "14. ISO/IEC 15504 (SPICE) - 소프트웨어 프로세스 평가 표준"
date = "2026-03-05"
[extra]
categories = "studynotes-se"
tags = ["ISO15504", "SPICE", "프로세스평가", "프로세스성숙도", "소프트웨어공학"]
+++

# ISO/IEC 15504 (SPICE) - 소프트웨어 프로세스 평가 표준

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ISO/IEC 15504(SPICE)는 소프트웨어 개발 조직의 프로세스 역량을 체계적으로 평가하고 개선하기 위한 국제 표준 프레임워크로, 프로세스 수행 능력을 0~5단계로 측정한다.
> 2. **가치**: 조직의 프로세스 성숙도를 객관적으로 진단하여 프로세스 개선 로드맵을 수립할 수 있게 하며, 국제적인 소프트웨어 품질 인증 획득의 근거를 제공한다.
> 3. **융합**: CMMI와 상호 보완적 관계에 있으며, ISO 12207과 연계되어 SDLC 전반의 프로세스 품질 관리 체계를 완성한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

ISO/IEC 15504(SPICE, Software Process Improvement and Capability dEtermination)는 소프트웨어 프로세스의 평가와 개선을 위한 국제 표준으로, 조직이 자신의 소프트웨어 개발 프로세스를 객관적으로 평가하고 지속적으로 개선할 수 있도록 체계화된 프레임워크를 제공한다. 이 표준은 프로세스의 '무엇(What)'을 수행해야 하는가뿐만 아니라 '얼마나 잘(How well)' 수행하는가를 측정하는 이차원적 평가 모델을 특징으로 한다.

### 비유

SPICE는 마치 요리사의 실력을 평가하는 '미쉐린 가이드'와 같다. 요리(프로세스)의 종류는 다양하지만, 각 요리가 제대로 만들어졌는지, 위생은 청결한지, 맛은 일정한지 등을 기준으로 평가하여 0~5개의 별(역량 수준)을 부여한다. 이를 통해 요리사(조직)는 자신의 약점을 파악하고 더 나은 요리를 만들기 위한 개선 활동을 수행할 수 있다.

### 등장 배경 및 발전 과정

1. **기존 평가 방식의 한계**: 1990년대 초반, 소프트웨어 조직의 역량 평가는 주로 CMM(Capability Maturity Model)에 의존했으나, 이는 단계적(Staged) 모델로서 모든 프로세스가 동일한 성숙도를 가져야 한다는 제약이 있었다. 또한 특정 프로세스만 선택적으로 개선하려는 조직의 요구를 충족시키기 어려웠다.

2. **ISO 표준화 요구**: 유럽 연합을 중심으로 소프트웨어 품질에 대한 국제적 표준의 필요성이 대두되면서, 1991년부터 SPICE 프로젝트가 시작되었다. 이는 다양한 프로세스 평가 모델을 통합하고 국제 표준화하기 위한 노력이었다.

3. **비즈니스적 요구사항**: 글로벌 소프트웨어 아웃소싱 시장의 확대와 함께, 공급업체의 프로세스 역량을 객관적으로 평가할 수 있는 국제 공인 기준에 대한 수요가 급증했다. ISO 15504는 이러한 공급자 평가 및 선정의 객관적 근거를 제공한다.

### SPICE 모델의 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                    SPICE 2차원 평가 모델                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────┐  ┌─────────────────────────────────────────┐    │
│   │  프로세스 │  │         역량 수준 (Capability Level)      │    │
│   │  차원     │  │  ┌───┬───┬───┬───┬───┬───┐           │    │
│   │  (What)   │  │  │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │           │    │
│   │           │  │  │불완│수행│관리│확립│예측│최적│           │    │
│   ├─────────┤  │  └───┴───┴───┴───┴───┴───┘           │    │
│   │ CUS      │  │       ▲                             │    │
│   │ (고객)   │  │       │                             │    │
│   ├─────────┤  │       │                             │    │
│   │ ENG      │  └───────┴─────────────────────────────┘    │
│   │ (공학)   │              역량 차원 (How well)             │
│   ├─────────┤                                                │
│   │ SUP      │         각 프로세스별로 0~5 수준 평가          │
│   │ (지원)   │                                                │
│   ├─────────┤                                                │
│   │ MAN      │                                                │
│   │ (관리)   │                                                │
│   └─────────┘                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 프로세스 카테고리 구성 (5개)

| 카테고리 | 코드 | 상세 역할 | 주요 프로세스 | 내부 동작 메커니즘 |
|---------|------|----------|-------------|-------------------|
| 고객-공급자 | CUS | 고객 요구 파악 및 서비스 제공 | 요구사항 도출, 공급, 운영 | 고객 인터페이스 관리, SLA 모니터링 |
| 공학 | ENG | 소프트웨어 개발 핵심 활동 | 분석, 설계, 구현, 통합, 유지보수 | 기술적 작업 수행, 산출물 생성 |
| 지원 | SUP | 프로세스 수행 보조 활동 | 문서화, 형상관리, 품질보증, 검증 | 다른 프로세스 지원, 품질 게이트 |
| 관리 | MAN | 프로세스/프로젝트 관리 활동 | 프로젝트 관리, 위험 관리, 측정 | 계획, 모니터링, 조정 활동 |
| 조직 | ORG | 조직 수준의 인프라 구축 | 프로세스 정의, 인력 개선, 자산 관리 | 전사적 표준 수립, 교육 체계 |

### 역량 수준 (Capability Levels) 상세

```
┌────────────────────────────────────────────────────────────────────┐
│                      역량 수준 구조도                               │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Level 5: 최적화 (Optimizing)                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ • 지속적인 프로세스 개선                                       │ │
│  │ • 혁신 및 최적화 목표 설정                                     │ │
│  │ • 정량적 개선 효과 분석                                        │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              ▲                                     │
│  Level 4: 예측 가능 (Predictable)                                 │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ • 정량적 목표 설정 및 관리                                     │ │
│  │ • 프로세스 성능 예측                                          │ │
│  │ • 통계적 공정 관리 (SPC)                                       │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              ▲                                     │
│  Level 3: 확립 (Established)                                      │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ • 표준 프로세스 정의 및 배포                                   │ │
│  │ • 조직 차원의 프로세스 자산 활용                               │ │
│  │ • 테일러링 가이드라인 적용                                     │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              ▲                                     │
│  Level 2: 관리됨 (Managed)                                        │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ • 작업 산출물 관리                                             │ │
│  │ • 일정 및 자원 계획/모니터링                                   │ │
│  │ • 이해관계자 참여 관리                                         │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              ▲                                     │
│  Level 1: 수행됨 (Performed)                                      │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ • 프로세스 목표 달성                                           │ │
│  │ • 작업 산출물 식별                                             │ │
│  │ • 기본적인 수행 증거 확보                                      │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              ▲                                     │
│  Level 0: 불완전 (Incomplete)                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ • 프로세스가 구현되지 않거나 목표 미달성                        │ │
│  │ • 작업 산출물 없음                                             │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 프로세스 속성 (Process Attributes)

각 역량 수준은 프로세스 속성으로 구성되며, 각 속성은 0~100% 척도로 평가된다:

| 수준 | 속성 | 평가 기준 | 달성 등급 |
|------|------|----------|----------|
| 1 | PA 1.1 프로세스 수행 | 프로세스가 목표를 달성하는가? | N(0-15%), P(15-50%), L(50-85%), F(85-100%) |
| 2 | PA 2.1 수행 관리 | 작업이 계획되고 모니터링되는가? | N/P/L/F |
| 2 | PA 2.2 작업 산출물 관리 | 산출물이 적절히 관리되는가? | N/P/L/F |
| 3 | PA 3.1 프로세스 정의 | 표준 프로세스가 정의되었는가? | N/P/L/F |
| 3 | PA 3.2 프로세스 배포 | 표준이 실제로 적용되는가? | N/P/L/F |
| 4 | PA 4.1 정량적 분석 | 프로세스가 정량적으로 분석되는가? | N/P/L/F |
| 4 | PA 4.2 정량적 관리 | 정량적 목표가 관리되는가? | N/P/L/F |
| 5 | PA 5.1 프로세스 개선 | 개선 기회가 식별되는가? | N/P/L/F |
| 5 | PA 5.2 프로세스 최적화 | 개선이 효과적으로 구현되는가? | N/P/L/F |

### 평가 프로세스 상세 동작 원리

```
┌─────────────────────────────────────────────────────────────────────┐
│                      SPICE 평가 프로세스 흐름                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│  │ 1.평가   │───▶│ 2.평가   │───▶│ 3.데이터 │───▶│ 4.평가   │     │
│  │   입력   │    │   계획   │    │   수집   │    │   수행   │     │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘     │
│       │               │               │               │            │
│       ▼               ▼               ▼               ▼            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│  │•평가목적 │    │•범위설정 │    │•인터뷰   │    │•속성별   │     │
│  │•평가제약 │    │•일정수립 │    │•문서검토 │    │  점수산정│     │
│  │•조직문맥 │    │•팀구성   │    │•관찰     │    │•강점/약점│     │
│  │•평가기준 │    │•도구선정 │    │•설문조사 │    │  식별   │     │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘     │
│                                                        │            │
│                                                        ▼            │
│  ┌──────────┐    ┌──────────┐                   ┌──────────┐       │
│  │ 6.평가   │◀───│ 5.평가   │◀──────────────────│ 결과검증 │       │
│  │   보고   │    │   결과   │                   │ 및확인   │       │
│  └──────────┘    └──────────┘                   └──────────┘       │
│       │               │                                             │
│       ▼               ▼                                             │
│  ┌──────────┐    ┌──────────┐                                      │
│  │•평가보고서    │•역량수준 │                                      │
│  │•개선권고안    │  프로파일│                                      │
│  │•행동계획 │    │•프로세스 │                                      │
│  │          │    │  등급   │                                      │
│  └──────────┘    └──────────┘                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드 예시: 프로세스 역량 평가 시스템

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional

class CapabilityLevel(Enum):
    """역량 수준 정의"""
    INCOMPLETE = 0
    PERFORMED = 1
    MANAGED = 2
    ESTABLISHED = 3
    PREDICTABLE = 4
    OPTIMIZING = 5

class AttributeRating(Enum):
    """속성 평가 등급 (N/P/L/F)"""
    NOT_ACHIEVED = "N"    # 0-15%
    PARTIALLY = "P"       # 15-50%
    LARGELY = "L"         # 50-85%
    FULLY = "F"           # 85-100%

@dataclass
class ProcessAttribute:
    """프로세스 속성 정의"""
    attribute_id: str
    name: str
    description: str
    level: int
    rating: Optional[AttributeRating] = None
    score: float = 0.0

@dataclass
class ProcessInstance:
    """프로세스 인스턴스 평가"""
    process_id: str
    process_name: str
    category: str  # CUS, ENG, SUP, MAN, ORG
    attributes: Dict[str, ProcessAttribute]

    def calculate_capability_level(self) -> CapabilityLevel:
        """
        프로세스 역량 수준 계산
        규칙: 상위 레벨 달성을 위해 하위 레벨의 모든 속성이
        'Largely' 이상 달성되어야 함
        """
        level_achieved = CapabilityLevel.INCOMPLETE

        # Level 1 체크: PA 1.1
        if self._is_level_1_achieved():
            level_achieved = CapabilityLevel.PERFORMED
        else:
            return level_achieved

        # Level 2 체크: PA 2.1, PA 2.2
        if self._is_level_2_achieved():
            level_achieved = CapabilityLevel.MANAGED
        else:
            return level_achieved

        # Level 3 체크: PA 3.1, PA 3.2
        if self._is_level_3_achieved():
            level_achieved = CapabilityLevel.ESTABLISHED
        else:
            return level_achieved

        # Level 4 체크: PA 4.1, PA 4.2
        if self._is_level_4_achieved():
            level_achieved = CapabilityLevel.PREDICTABLE
        else:
            return level_achieved

        # Level 5 체크: PA 5.1, PA 5.2
        if self._is_level_5_achieved():
            level_achieved = CapabilityLevel.OPTIMIZING

        return level_achieved

    def _check_attributes_achieved(self, attr_ids: List[str]) -> bool:
        """지정된 속성들이 모두 Largely 이상 달성되었는지 확인"""
        for attr_id in attr_ids:
            attr = self.attributes.get(attr_id)
            if not attr or attr.rating in [None, AttributeRating.NOT_ACHIEVED]:
                return False
            if attr.rating == AttributeRating.PARTIALLY:
                return False
        return True

    def _is_level_1_achieved(self) -> bool:
        return self._check_attributes_achieved(['PA1.1'])

    def _is_level_2_achieved(self) -> bool:
        return self._check_attributes_achieved(['PA1.1', 'PA2.1', 'PA2.2'])

    def _is_level_3_achieved(self) -> bool:
        return self._check_attributes_achieved(
            ['PA1.1', 'PA2.1', 'PA2.2', 'PA3.1', 'PA3.2'])

    def _is_level_4_achieved(self) -> bool:
        return self._check_attributes_achieved(
            ['PA1.1', 'PA2.1', 'PA2.2', 'PA3.1', 'PA3.2', 'PA4.1', 'PA4.2'])

    def _is_level_5_achieved(self) -> bool:
        return self._check_attributes_achieved(
            ['PA1.1', 'PA2.1', 'PA2.2', 'PA3.1', 'PA3.2',
             'PA4.1', 'PA4.2', 'PA5.1', 'PA5.2'])

class SpiceAssessment:
    """SPICE 평가 수행 클래스"""

    def __init__(self, organization_name: str):
        self.organization_name = organization_name
        self.processes: Dict[str, ProcessInstance] = {}
        self.evidence_records: List[Dict] = []

    def add_evidence(self, process_id: str, evidence_type: str,
                     description: str, assessor: str):
        """평가 증거 추가"""
        self.evidence_records.append({
            'process_id': process_id,
            'type': evidence_type,  # interview, document, observation
            'description': description,
            'assessor': assessor,
            'timestamp': datetime.now()
        })

    def generate_capability_profile(self) -> Dict[str, int]:
        """
        조직의 역량 프로파일 생성
        각 프로세스별 역량 수준을 매핑
        """
        profile = {}
        for process_id, process in self.processes.items():
            level = process.calculate_capability_level()
            profile[process_id] = level.value
        return profile

    def identify_improvement_areas(self) -> List[Dict]:
        """개선 영역 식별"""
        improvements = []

        for process_id, process in self.processes.items():
            for attr_id, attr in process.attributes.items():
                if attr.rating in [None, AttributeRating.NOT_ACHIEVED,
                                   AttributeRating.PARTIALLY]:
                    improvements.append({
                        'process': process.process_name,
                        'attribute': attr.name,
                        'current_level': attr.rating.value if attr.rating else 'N/A',
                        'target_level': 'L',
                        'priority': self._calculate_priority(attr)
                    })

        return sorted(improvements, key=lambda x: x['priority'], reverse=True)

    def _calculate_priority(self, attribute: ProcessAttribute) -> int:
        """개선 우선순위 계산"""
        # 핵심 프로세스일수록, 낮은 레벨일수록 높은 우선순위
        priority = 100 - (attribute.level * 10)
        if attribute.rating == AttributeRating.NOT_ACHIEVED:
            priority += 50
        return priority
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### SPICE vs CMMI 심층 비교

| 평가 차원 | ISO 15504 (SPICE) | CMMI |
|----------|-------------------|------|
| **모델 구조** | 연속형(Continuous) 중심, 2차원 모델 | 단계형(Staged) + 연속형 선택 가능 |
| **평가 단위** | 개별 프로세스별 역량 수준 | 조직 전체 성숙도 레벨 |
| **성숙도/역량 수준** | 0~5 (불완전~최적화) | 1~5 (초기~최적화) |
| **프로세스 영역** | 5개 카테고리 (CUS/ENG/SUP/MAN/ORG) | 4개 영역 (관리/공학/지원/프로세스관리) |
| **평가 결과** | 프로세스별 개별 등급 (프로파일) | 전사 단일 등급 또는 선택적 등급 |
| **국제 표준** | ISO 국제 표준 | SEI 개발, 산업 표준 |
| **적용 유연성** | 높음 (프로세스 선택적 평가 가능) | 상대적으로 낮음 (단계형은 순차적) |
| **주요 적용 분야** | 유럽, 자동차(Automotive SPICE) | 미국, 방산/IT |

### SPICE와 타 표준 간 융합 관계

| 표준 | 관계 유형 | 융합 포인트 | 시너지 효과 |
|------|----------|------------|------------|
| **ISO 12207** | 상호 보완 | SPICE가 12207 프로세스 평가 기준 제공 | SDLC 프로세스 정의 + 평가 체계 완성 |
| **ISO 9001** | 통합 가능 | 품질 경영시스템과 프로세스 평가 연계 | 품질 인증 획득 가속화 |
| **Automotive SPICE** | 산업 특화 | 자동차 산업용 SPICE 파생 모델 | 안전 필수 시스템 개발 역량 보증 |
| **Six Sigma** | 방법론 통합 | DMAIC와 SPICE 평가 연계 | 정량적 프로세스 개선 체계 구축 |

### 과목 융합 관점 분석

1. **OS(운영체제)와의 융합**: SPICE의 수준 4(예측 가능)에서 요구하는 정량적 프로세스 관리는 OS의 자원 스케줄링 알고리즘과 유사한 원리를 적용한다. 프로세스 수행 시간, 자원 사용량을 측정하고 통계적 공정 관리(SPC) 기법을 통해 이상 징후를 조기에 탐지한다.

2. **데이터베이스와의 융합**: 평가 증거 데이터의 축적 및 분석을 위해 데이터 웨어하우스 구축이 필요하다. 프로세스 수행 이력, 결함 밀도, 생산성 지표를 저장하고 OLAP을 통한 다차원 분석을 수행하여 개선 기회를 도출한다.

3. **보안과의 융합**: SPICE Level 2의 '작업 산출물 관리' 속성은 보안 관점에서 접근 통제, 무결성 검증과 밀접하게 연관된다. 형상 관리 프로세스의 보안성 평가는 SBOM(Software Bill of Materials) 관리로 확장된다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오 및 기술사적 판단

**시나리오 1: 자동차 부품 소프트웨어 공급업체 평가**
- **상황**: 완성차 업체가 10개 SW 공급업체의 역량을 평가하여 선정해야 함
- **기술사적 판단**: Automotive SPICE(ASPICE) 기준으로 공급업체별 역량 프로파일 작성. 핵심 공정(ENG.4 소프트웨어 상세 설계, ENG.5 소프트웨어 구현)은 최소 Level 2, 안전 관련(SUP.8 형상 관리)은 Level 3 이상 요구
- **전략**: 가중 평가 모델 적용, 위험도가 높은 공정에 가중치 부여

**시나리오 2: 금융 IT 조직의 프로세스 개선 로드맵 수립**
- **상황**: 현재 Level 1 수준의 조직을 3년 내 Level 3로 도달해야 하는 규제 요건
- **기술사적 판단**: 단계적 개선 전략 수립
  - 1년차: 핵심 공정(요구사항 분석, 설계, 구현) Level 2 달성
  - 2년차: 품질 관리, 형상 관리 프로세스 Level 3 달성
  - 3년차: 전사 프로세스 표준화 및 Level 3 종합 인증
- **전략**: 내부 평가자 양성, 프로세스 자산 구축 우선

**시나리오 3: 글로벌 아웃소싱 공급업체 모니터링**
- **상황**: 인도/베트남 개발팀의 지속적 역량 모니터링 필요
- **기술사적 판단**: 분기별 SPICE 경평가(Lite Assessment) 수행, 주요 지표 대시보드 구축
- **전략**: 자동화된 메트릭 수집, 이상 징후 알림 시스템 구축

### 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] 평가 도구 선정 (SPSS, SPICE 1-2-1 등)
- [ ] 증거 데이터 관리 시스템 구축
- [ ] 프로세스 자산 라이브러리 설계
- [ ] 메트릭 수집 자동화 인프라

**운영/보안적 고려사항**
- [ ] 평가자 자격 인증 (Certified SPICE Assessor)
- [ ] 평가 결과의 기밀 관리 체계
- [ ] 제3자 인증 기관 선정
- [ ] 지속적 개선 거버넌스 수립

### 안티패턴 (Anti-patterns)

1. **문서화 오버헤드**: 평가 통과에만 집중하여 과도한 문서를 양산하고 실제 개발 효율은 저하되는 현상. 이는 '형식적 SPICE'로 불리며 권장되지 않는다.

2. **선택적 최적화**: 일부 프로세스만 고평가 받고 나머지는 방치되는 불균형. 조직 전체의 역량이 아닌 쇼케이스용 역량만 키우는 결과 초래.

3. **평가 주기 과다**: 매 분기마다 정식 평가를 수행하여 조직에 과도한 부담. 경평가와 정식 평가의 적절한 혼용 필요.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 구분 | 도입 전 | 도입 후 | 개선율 |
|----------|--------|--------|-------|
| 결함 밀도 (개/KLOC) | 15.2 | 8.3 | 45% 감소 |
| 프로젝트 일정 준수율 | 62% | 85% | 37% 향상 |
| 고객 만족도 (5점 척도) | 3.2 | 4.1 | 28% 향상 |
| 프로세스 표준화율 | 35% | 78% | 123% 향상 |
| 기술 부채 해소율 | - | 60%/년 | 신규 지표 |

### 미래 전망 및 진화 방향

1. **AI 기반 평가 자동화**: 머신러닝을 활용한 프로세스 수행 패턴 분석, 이상 탐지 자동화. 자연어 처리를 통한 문서 품질 평가 자동화.

2. **DevOps와의 융합**: CI/CD 파이프라인에 SPICE 메트릭 수집 통합, 실시간 역량 모니터링 체계 구축.

3. **클라우드 네이티브 확장**: MSA 환경에서의 서비스별 프로세스 역량 평가 모델 개발.

4. **양자 컴퓨팅 대비**: 양자 소프트웨어 개발 프로세스에 대한 새로운 SPICE 확장 모델 연구.

### 참고 표준/가이드

| 표준 | 내용 | 적용 범위 |
|------|------|----------|
| ISO/IEC 15504-1~10 | SPICE 전체 규격 | 평가 모델, 지침, 프로세스 |
| ISO/IEC 33000 시리즈 | SPICE 개정판 (ISO 15504 대체) | 최신 표준 |
| Automotive SPICE PAM | 자동차 산업 특화 | 안전 필수 시스템 |
| SPICE 1-2-1 | 평가 도구 표준 | 도구 호환성 |
| ISO/IEC 20000-1 | IT 서비스 관리와 통합 | ITSM 영역 |

---

## 관련 개념 맵 (Knowledge Graph)

- [CMMI](./15_cmmi.md): 프로세스 성숙도 모델로 SPICE와 상호 보완적 관계
- [ISO 12207](./13_iso12207.md): 소프트웨어 생명주기 프로세스 표준, SPICE 평가 대상
- [프로세스 개선](./19_software_reengineering.md): SPICE 평가 결과 기반 개선 활동
- [품질 보증](../2_quality/software_quality_standards.md): 프로세스 품질과 제품 품질의 연관성
- [형상 관리](./20_configuration_management.md): SPICE SUP.8 프로세스 영역

---

## 어린이를 위한 3줄 비유 설명

1. **개념**: SPICE는 학교에서 선생님이 수업을 얼마나 잘 가르치시는지 점수로 매기는 것과 같아요. 0점부터 5점까지 있어서, 5점을 받은 선생님은 정말 훌륭하게 가르치시는 거예요.

2. **원리**: 선생님(소프트웨어 회사)이 수업 계획을 잘 세웠는지, 학생들이 이해했는지, 매년 더 좋아지는지를 꼼꼼하게 검사해요. 그래서 어떤 부분이 부족한지 알려주는 거예요.

3. **효과**: 이 검사를 통과한 학원(회사)은 어디서든 인정받을 수 있어요. 또한, 점수가 낮은 부분을 열심히 연습해서 다음에는 더 높은 점수를 받을 수 있도록 도와줘요.
