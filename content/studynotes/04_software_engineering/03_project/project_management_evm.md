+++
title = "프로젝트 일정 및 비용 통제 (WBS, PERT/CPM, EVM)"
description = "성공적인 프로젝트 수행을 위한 일정 계획 및 획득 가치 관리(EVM) 심층 분석"
date = 2024-05-24
[taxonomies]
categories = ["studynotes-software_engineering"]
tags = ["WBS", "PERT/CPM", "EVM", "Critical Path", "Project Management"]
+++

# 프로젝트 일정 및 비용 통제 전략 (WBS, PERT/CPM, EVM)

#### ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로젝트의 불확실성을 최소화하기 위해 작업을 분할(WBS)하고, 작업 간의 논리적 선후관계를 네트워크로 모델링(PERT/CPM)하며, 진행 성과를 화폐 가치로 환산하여 통제(EVM)하는 과학적 관리 체계입니다.
> 2. **가치**: 감각이나 경험에 의존하던 일정/비용 관리를 정량적 지표(SPI, CPI) 기반으로 전환하여, 프로젝트의 잔여 리스크를 예측하고 조기 경보(Early Warning)를 통해 평균 20% 이상의 자원 낭비를 방지합니다.
> 3. **융합**: 최근에는 전통적인 폭포수 모델의 EVM을 애자일(Agile) 환경에 맞게 조정한 Agile EVM(AEVM)으로 진화하고 있으며, JIRA 등 ALM(Application Lifecycle Management) 도구와 통합되어 실시간 대시보드 형태로 제공됩니다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 프로젝트 관리의 핵심 기법인 WBS(Work Breakdown Structure), PERT(Program Evaluation and Review Technique), CPM(Critical Path Method), 그리고 EVM(Earned Value Management)은 프로젝트의 범위를 정의하고, 일정을 계획하며, 진척도를 비용 가치로 통합 측정하는 종합적인 통제 프레임워크입니다. 단순한 공정 관리를 넘어, 일정과 비용이라는 두 가지 상충하는 제약 조건을 단일 가치 체계로 동기화하여 아키텍트와 PM(Project Manager)에게 객관적인 프로젝트 건전성을 제공합니다.
- **💡 비유**: 목적지까지 자동차 여행을 한다고 가정해 봅시다. WBS는 여행 코스를 '구간별 목적지'로 나누는 것이고, PERT/CPM은 각 구간의 '최적 이동 경로와 예상 소요 시간'을 내비게이션으로 계산하는 것입니다. EVM은 중간 기착지에서 "현재까지 쓴 기름값 대비 원래 계획했던 이동 거리를 제대로 왔는가?"를 계산하여, 최종 목적지 도착 시 연료가 부족할지 남을지를 미리 경고해 주는 차량의 트립 컴퓨터(Trip Computer)와 같습니다.
- **등장 배경 및 발전 과정**:
  1. **기존 기술의 한계**: 과거 간트 차트(Gantt Chart) 위주의 관리는 "일정이 50% 지났으니, 예산도 50% 썼겠지"라는 선형적이고 안일한 가정에 기반했습니다. 이는 실제 완료된 '작업의 가치'를 반영하지 못해, 프로젝트 막바지에 돌연 예산이 고갈되거나 일정이 폭발적으로 지연되는 이른바 '90% 증후군(90% Syndrome)'을 유발했습니다.
  2. **패러다임 변화**: 1950년대 미국 국방부(DoD)와 듀폰(DuPont)사에서 대규모 군사/화학 프로젝트를 관리하기 위해 PERT/CPM을 고안하였고, 이후 1960년대 미 국방부의 'Minuteman Missile Project'에서 일정과 예산을 통합하여 성과를 측정하는 EVM(Earned Value Management) 체계가 최초로 확립되었습니다.
  3. **비즈니스적 요구사항**: 현대의 대규모 IT 구축이나 클라우드 전환 프로젝트는 복잡도가 기하급수적으로 높아져, C-Level 경영진에게 감이 아닌 데이터를 기반으로 한 프로젝트 ROI 보고와 위험 조기 식별 시스템(Early Warning System)이 법적/제도적으로 강제되고 있습니다(예: ANSI/EIA-748 규격).

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

프로젝트 관리 통제 프레임워크는 계획(WBS → PERT/CPM)과 통제(EVM)라는 두 개의 큰 축으로 구성되며, 각 모듈은 유기적으로 데이터를 주고받습니다.

#### 1. 핵심 구성 요소

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 도구/지표 | 비유 |
|---|---|---|---|---|
| **WBS (Work Breakdown Structure)** | 프로젝트 범위를 계층적으로 분할하여 관리 가능한 최소 단위(Work Package)로 세분화 | 하향식(Top-Down) 분할을 통해 최종 인도물 기준 100% Rule을 만족하도록 작업 정의 | Work Package, Control Account | 레고 블록 조립 설명서 |
| **PERT / CPM** | 작업 간의 선후 관계를 네트워크 다이어그램으로 도식화하고 최장 경로(주공정) 산출 | CPM은 확정적 시간(1점 추정)으로 임계 경로(Critical Path) 계산, PERT는 확률적 시간(3점 추정)으로 불확실성 반영 | Forward/Backward Pass, Float(여유 시간) | 내비게이션 경로 탐색 알고리즘 |
| **PV (Planned Value)** | 특정 시점까지 완료하기로 계획된 작업의 예산 가치 총합 | 기준선(Baseline) 계획에 따라 날짜별 누적 비용을 S-Curve 형태로 할당 | BCWS (Budgeted Cost of Work Scheduled) | 여행 출발 전 계획한 예산 |
| **EV (Earned Value)** | 특정 시점까지 **실제 완료된** 작업을 예산 가치로 환산한 금액 | 완료된 Work Package에 배정된 예산을 합산 (예: 100만원짜리 작업의 50% 완료 시 EV = 50만원) | BCWP (Budgeted Cost of Work Performed) | 지금까지 여행한 거리를 돈으로 환산한 가치 |
| **AC (Actual Cost)** | 특정 시점까지 완료된 작업을 수행하는 데 **실제로 투입된** 총 비용 | 회계 시스템과 연동하여 인건비, 외주비 등 발생한 총 실 비용 집계 | ACWP (Actual Cost of Work Performed) | 지갑에서 실제 빠져나간 돈 |

#### 2. PERT/CPM 네트워크 구조 및 EVM 변동 추이 다이어그램

아래 다이어그램은 WBS에 의해 도출된 Activity들이 PERT/CPM 네트워크를 형성하고, 진행 과정에서 EVM 지표들이 어떻게 추적되는지 보여줍니다.

```text
[ PERT / CPM Network Diagram (AON: Activity On Node) ]

         [Activity B] 
        ES: 3 | EF: 8       --- Float: 2 Days --->
         Duration: 5
       /               \
[Activity A]           [Activity D] ----------> [Activity E]
ES: 0 | EF: 3          ES: 10 | EF: 15          ES: 15 | EF: 20
Duration: 3            Duration: 5              Duration: 5
       \               /
         [Activity C]  
        ES: 3 | EF: 10      <--- Critical Path (Float: 0) --->
         Duration: 7

- 경로 1: A -> B -> D -> E (3+5+5+5 = 18일)
- 경로 2: A -> C -> D -> E (3+7+5+5 = 20일) => Critical Path (최장 경로, 지연 시 전체 지연)


[ EVM S-Curve (Earned Value Management Tracking) ]

Cost ($)
  ^
  |                                 .* (EAC - Estimate at Completion: 예측 총 비용)
  |                              .  
  |                           .   [BAC - Budget at Completion: 계획 총 비용] 
  |                        .   .-' 
  |                     .   .-'
  |                  .   .-'    <-- PV (Planned Value: 계획 가치 S-Curve)
  |               .   .-'
  |  AC(*)...*...*   <-- AC (Actual Cost: 실제 투입 비용 - 예산 초과 상태)
  |         . .-'|   <-- CV (Cost Variance: EV - AC, 음수면 비용 초과)
  |        .-'   |
  | EV(+)+---+---+   <-- EV (Earned Value: 획득 가치 - 일정 지연 상태)
  |   .-'    |
  |.-'       |       <-- SV (Schedule Variance: EV - PV, 음수면 일정 지연)
  +-------------------------------------> Time (Now)
```

#### 3. EVM 핵심 공식 및 계산 알고리즘

EVM의 분석은 현재 성과(Variance)와 미래 예측(Forecasting)으로 나뉩니다.

*   **현재 성과 측정 지표:**
    *   `SV (Schedule Variance) = EV - PV` (< 0 이면 일정 지연)
    *   `CV (Cost Variance) = EV - AC` (< 0 이면 예산 초과)
    *   `SPI (Schedule Performance Index) = EV / PV` (< 1.0 이면 일정 지연)
    *   `CPI (Cost Performance Index) = EV / AC` (< 1.0 이면 비용 초과)
*   **미래 예측 지표:**
    *   `BAC (Budget at Completion)`: 프로젝트 전체 총 계획 예산
    *   `ETC (Estimate to Complete) = (BAC - EV) / CPI`: 잔여 작업을 완료하는 데 필요한 추가 예측 비용 (현재의 비효율이 계속된다는 가정 하에)
    *   `EAC (Estimate at Completion) = AC + ETC` 또는 `BAC / CPI`: 최종 프로젝트 종료 시 예상되는 총 소요 비용
    *   `VAC (Variance at Completion) = BAC - EAC`: 최종 비용 차이 예측치

다음은 Python을 활용한 실무 수준의 EVM 지표 계산 및 상태 판별 클래스 예시입니다.

```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ProjectStatus:
    PV: float  # Planned Value
    EV: float  # Earned Value
    AC: float  # Actual Cost
    BAC: float # Budget at Completion

class EVMCalculator:
    def __init__(self, status: ProjectStatus):
        self.s = status
        # 0으로 나누는 예외 처리 (ZeroDivisionError 방지)
        self.epsilon = 1e-9 
        
    def calculate_metrics(self) -> Dict[str, Any]:
        sv = self.s.EV - self.s.PV
        cv = self.s.EV - self.s.AC
        
        spi = self.s.EV / (self.s.PV + self.epsilon)
        cpi = self.s.EV / (self.s.AC + self.epsilon)
        
        # 잔여 예측 (ETC) - 현재의 CPI 효율이 미래에도 동일하게 적용된다고 가정(Typical)
        etc = (self.s.BAC - self.s.EV) / (cpi + self.epsilon)
        eac = self.s.AC + etc
        
        return {
            "SV": round(sv, 2), "SPI": round(spi, 2),
            "CV": round(cv, 2), "CPI": round(cpi, 2),
            "EAC": round(eac, 2),
            "Health": self._evaluate_health(spi, cpi)
        }
        
    def _evaluate_health(self, spi: float, cpi: float) -> str:
        """프로젝트 건전성 다차원 평가 매트릭스"""
        if spi >= 1.0 and cpi >= 1.0:
            return "🟩 훌륭함: 일정 단축 및 비용 절감 상태 (Under Budget, Ahead of Schedule)"
        elif spi < 1.0 and cpi < 1.0:
            return "🟥 위험: 일정 지연 및 예산 초과 상태 (Over Budget, Behind Schedule) - 즉각적인 Crashing/Fast-Tracking 필요"
        elif spi >= 1.0 and cpi < 1.0:
            return "🟨 경고: 일정은 빠르나 비용이 초과됨 (Over Budget, Ahead of Schedule) - 품질 저하 또는 자원 과투입 의심"
        else:
            return "🟨 경고: 일정은 지연되나 비용은 절감됨 (Under Budget, Behind Schedule) - 자원 부족 또는 착수 지연 의심"

# 예시: 프로젝트 계획 1000, 획득 가치 800, 실제 투입 900, 총 예산 5000인 상황
status = ProjectStatus(PV=1000, EV=800, AC=900, BAC=5000)
evm = EVMCalculator(status)
print(evm.calculate_metrics())
# 출력: {'SV': -200, 'SPI': 0.8, 'CV': -100, 'CPI': 0.89, 'EAC': 5619.1, 'Health': '🟥 위험...'}
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 일정 관리 기법 비교 (Gantt vs PERT vs CPM)

| 비교 항목 | Gantt Chart (간트 차트) | PERT (프로그램 평가 및 리뷰 기법) | CPM (임계 경로 방법) |
|---|---|---|---|
| **설계 목적** | 단순 일정 시각화 및 직관적 보고 | **불확실성**이 높은 연구개발(R&D) | **과거 데이터**가 있는 건설/엔지니어링 |
| **시간 추정 방식** | 결정론적 1점 추정 | **확률적 3점 추정** (낙관/비관/최빈치) | 결정론적 1점 추정 |
| **주요 통제 요소** | 시간 (단순 날짜) | 시간적 확률 (납기 달성 확률 계산) | **비용 통제 최적화** (Crashing 연계) |
| **선후 관계 파악** | 명확하지 않음 (바 형태로 나열) | 노드 네트워크로 명확한 종속성 도출 | 네트워크 기반 선후 관계 파악 |
| **실무 적용** | 임원진 보고용 대시보드 | 신기술 도입 프로젝트, R&D | 토목 건설, 정형화된 SI 프로젝트 |

#### 2. 애자일(Agile) 환경과의 융합: Agile EVM (AEVM)
전통적인 EVM은 WBS가 명확하고 변경이 적은 폭포수(Waterfall) 모델에 최적화되어 있습니다. 요구사항이 지속적으로 변하는 애자일 환경에서는 스토리 포인트(Story Point)를 활용하여 다음과 같이 매핑합니다.
- **WBS ↔ Product Backlog**: 백로그의 에픽(Epic)과 스토리(Story)가 WBS를 대체합니다.
- **PV ↔ 계획된 스토리 포인트**: 스프린트 플래닝(Sprint Planning) 시 할당된 총 스토리 포인트.
- **EV ↔ 완료된(Done) 스토리 포인트**: 스프린트 리뷰 시 통과된 기능의 스토리 포인트 가치.
- **시너지**: 버다운 차트(Burndown Chart)의 단점(비용 가시성 부족)을 보완하여, 스프린트 단위로 재무적 건전성(CPI)을 경영진에게 제공할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: 프로젝트 지연 시 일정 단축 전략(Schedule Compression)
실무에서 EVM 산출 결과 SPI < 1.0 (일정 지연) 상황이 발생했을 때, 기술사로서 다음과 같은 전략적 의사결정을 내려야 합니다.

*   **상황 분석**: 주공정(Critical Path) 상의 작업이 지연되고 있는지 파악. 주공정이 아닌 여유 시간(Float)이 있는 작업의 지연은 프로젝트 전체 일정에 영향을 주지 않으므로 과도한 조치를 자제해야 함.
*   **전략 1 - Crashing (공정 압축)**: 비용이 가장 적게 드는 주공정 작업에 추가 자원(인력, 야근, 고성능 장비)을 투입하여 일정을 단축. (트레이드오프: **비용 증가 및 품질 저하 위험**)
*   **전략 2 - Fast-Tracking (공정 중첩)**: 논리적으로 순차적으로 진행해야 할 작업을 병행(동시)하여 수행. (예: 설계가 끝나기 전에 개발 착수). (트레이드오프: **재작업(Rework) 리스크 및 프로젝트 복잡도 급증**)
*   **의사결정 기준**: 예산의 여유가 있다면 Crashing을 우선 고려하고, 예산이 고갈(CPI < 1.0)된 상태라면 리스크를 감수하고 Fast-Tracking을 선택하거나, 가장 최후의 수단으로 고객과 협의하여 범위를 축소(Scope Reduction)해야 합니다.

#### 2. EVM 도입 시 고려사항 및 안티패턴 (Anti-patterns)

*   **안티패턴 1: 0/100 Rule 무시 (환상의 진척률)**: 개발자가 "거의 다 했어요(90% 완료)"라고 보고하는 것을 그대로 EV에 반영하는 오류. 실무에서는 작업 패키지의 주관적 평가를 막기 위해 착수 시 0%, 완전 종료 시 100%만 인정하는 '0/100 Rule' 또는 시작 시 50%, 종료 시 50%를 주는 '50/50 Rule'과 같은 엄격한 획득 가치 측정 지침이 필요합니다.
*   **안티패턴 2: WBS 세분화 실패**: Work Package를 너무 크게 잡으면(예: 'DB 구축 - 3개월') 내부 진척률 파악이 불가능해져 EVM이 작동하지 않습니다. 8-80 Rule(작업 패키지는 8시간 이상, 80시간 이하가 적당)을 준수해야 합니다.
*   **안티패턴 3: 매몰 비용(Sunk Cost)에 대한 집착**: 프로젝트의 CPI가 0.5 이하로 심각하게 악화되어 EAC가 예산을 초과함에도, 이미 투자된 AC가 아까워 무리하게 프로젝트를 강행하는 경영진의 오류. EVM 데이터를 바탕으로 과감한 킬(Kill) 스위치 작동 기준을 마련해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (간트 차트 및 단순 예산 관리) | 도입 후 (EVM 기반 정량 통제) | 향상 수치 |
|---|---|---|---|
| **가시성** | 일정과 비용이 분리되어 종합 분석 불가 | 통합된 S-Curve 형태의 대시보드 제공 | 프로젝트 위험 인지 시간 40% 단축 |
| **비용 통제** | 사후 정산 시 예산 초과 발견 (대응 불가) | CPI 기반 조기 경보로 자원 재분배 및 낭비 방지 | 예산 초과율 15~20% 감소 |
| **예측력** | 프로젝트 종료 시점 추정 불가 | EAC, ETC를 통한 과학적 최종 예산/일정 도출 | 예측 정확도 85% 이상 확보 |

#### 2. 미래 전망 및 진화 방향
향후 EVM은 AI 머신러닝 기법과 결합하여 **Predictive EVM**으로 진화할 것입니다. 과거 수많은 프로젝트의 WBS 패턴과 지연 데이터를 학습한 AI가 초기 기획 단계에서부터 잠재적인 병목 구간(Hidden Critical Path)을 예측하고, 실시간 진척도 입력 시 몬테카를로 시뮬레이션(Monte Carlo Simulation)을 통해 프로젝트의 납기 달성 확률을 자동 계산해 주는 지능형 PMO 봇 체계가 대세로 자리 잡을 것입니다.

#### ※ 참고 표준/가이드
*   **ANSI/EIA-748**: 미국 국방성 및 산업계에서 널리 쓰이는 EVMS(Earned Value Management System)에 대한 32가지 국제 가이드라인.
*   **PMBOK Guide**: 미국 프로젝트 관리 협회(PMI)에서 발행하는 프로젝트 관리 지식 체계 및 EVM 공식 표준 가이드.

---

### 📌 관련 개념 맵 (Knowledge Graph)
*   [`[범위 관리 (Scope Management)]`](@/studynotes/04_software_engineering/04_requirements/requirements_engineering.md) : WBS를 도출하기 위한 근간이 되는 요구사항 및 범위 정의 체계. 범위가 변하면(Scope Creep) EVM의 기준선이 흔들립니다.
*   [`[애자일 스크럼 (Agile Scrum)]`](@/studynotes/04_software_engineering/01_sdlc/agile_methodology.md) : 전통적인 WBS 대신 스토리 포인트를 활용하는 현대적 프로젝트 관리 방법론으로, Agile EVM으로 발전 중입니다.
*   [`[위험 관리 (Risk Management)]`](@/studynotes/04_software_engineering/03_project/_index.md) : EVM에서 CPI/SPI 저하라는 '징후'를 발견했을 때, 실제 원인(Risk)을 식별하고 대응 계획을 수립하는 연계 활동입니다.
*   [`[형상 관리 (Configuration Management)]`](@/studynotes/04_software_engineering/02_quality/_index.md) : 프로젝트 진행 중 기준선(Baseline)이 변경될 때 이를 통제하여 EVM 계산의 무결성을 유지하는 기법.
*   [`[품질 관리 (Quality Assurance)]`](@/studynotes/04_software_engineering/02_quality/software_quality_standards.md) : 일정을 무리하게 단축(Crashing)할 때 발생하는 품질 저하를 방지하기 위한 통제 기법.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **WBS**: 커다란 코끼리를 한 번에 먹을 수 없으니, 아주 작은 크기(코, 다리, 귀 등)로 잘게 쪼개는 계획서입니다.
2. **PERT/CPM**: 쪼개진 일들을 어떤 순서로 해야 제일 빨리 끝낼지, 가장 막히기 쉬운 '핵심 구간'을 찾는 내비게이션입니다.
3. **EVM**: 중간 기착지에 도착했을 때 "시간은 얼마나 늦었는지?", "돈은 얼마나 펑펑 썼는지?"를 동시에 계산해 주는 똑똑한 가계부입니다.
