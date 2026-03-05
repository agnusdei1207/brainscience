+++
title = "38. PERT (Program Evaluation and Review Technique)"
description = "확률적 일정 추정 기법, 낙관치·기대치·비관치를 활용한 불확실성 관리"
date = "2026-03-05"
[taxonomies]
tags = ["pert", "schedule-estimation", "probability", "risk-management", "cmmi"]
categories = ["studynotes-4_software_engineering"]
+++

# 38. PERT (Program Evaluation and Review Technique)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: PERT는 각 작업의 소요시간을 **낙관치(Optimistic), 비관치(Pessimistic), 기대치(Most Likely)**의 3점으로 추정하고, 이를 **가중평균(β-분포)**하여 확률적 일정을 산출하는 프로젝트 일정 관리 기법입니다.
> 2. **가치**: 불확실성이 높은 프로젝트에서 **일정 완료 확률(예: 95% 확률로 90일 이내 완료)**을 제공하며, **표준편차 기반 리스크 구간**을 식별하여 의사결정을 지원합니다.
> 3. **융합**: CPM과 결합하여 **PERT/CPM**으로 통합 활용되며, 몬테카를로 시뮬레이션, EVM과 연계됩니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**PERT(Program Evaluation and Review Technique)**는 1958년 미 해군(US Navy)이 **폴라리스(Polaris) 미사일 개발 프로젝트**에서 불확실성이 높은 연구개발 일정을 관리하기 위해 개발한 기법입니다.

**PERT의 핵심 공식**:

| 공식 | 내용 | 설명 |
|:---|:---|:---|
| **기대 시간 (TE)** | TE = (O + 4M + P) / 6 | 가중평균 (β-분포 가정) |
| **표준편차 (σ)** | σ = (P - O) / 6 | 불확실성의 척도 |
| **분산 (V)** | V = σ² | 분산 |
| **프로젝트 분산** | Vp = Σ Vi (Critical Path) | 주공정 분산 합 |
| **Z-점수** | Z = (T - TE) / σp | 완료 확률 계산용 |

**용어 정의**:
- **O (Optimistic)**: 낙관적 추정 - 모든 것이 순조로울 때 소요시간
- **M (Most Likely)**: 최빈치/기대치 - 일반적인 상황에서 소요시간
- **P (Pessimistic)**: 비관적 추정 - 모든 것이 불리할 때 소요시간

### 2. 비유: 날씨 예보와 비교

```
[PERT = 날씨 예보의 강수 확률]

내일 야외 행사 일정:
─────────────────────────────────────────────────────────
전통적 추정: "내일 비가 올 것 같아요" (O/X)

PERT 추정:
- 낙관적 (O): "맑을 확률 20%" → 행사 진행 OK
- 기대치 (M): "흐릴 확률 50%" → 우비 준비
- 비관적 (P): "폭우 확률 30%" → 실내 대안

계산:
- 기대 강수확률 = (20 + 4×50 + 30) / 6 = 41.7%
- 표준편차 = (80 - 20) / 6 = 10%

의사결정:
- "70% 확률로 강수확률이 52% 이하"
- "95% 확률로 강수확률이 62% 이하"
→ 대안 준비 수준 결정
```

### 3. 등장 배경 및 발전 과정

**1) 1958년: 폴라리스 미사일 프로젝트**
- 미 해군의 핵미사일 잠수함 개발
- 250개 주요 계약업체, 9,000개 하청업체
- 기존 일정 관리로는 불가능한 복잡성
- 결과: 개발 기간 2년 단축 (예상 7년 → 5년)

**2) 1958~59년: CPM과 독립적 개발**
- 듀폰의 CPM과 거의 동시에 개발
- CPM: 확정적 소요시간 / PERT: 확률적 소요시간

**3) 1960~70년대: 우주/국방 산업 표준**
- 아폴로 계획, NASA 프로젝트에 적용
- 대형 R&D 프로젝트의 필수 도구

**4) 현대: PERT/CPM 통합, 몬테카를로 시뮬레이션**
- MS Project 등에서 PERT 분석 기능 제공
- 몬테카를로 시뮬레이션으로 정교화

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. PERT 네트워크 다이어그램

```
================================================================================
|                     PERT NETWORK WITH 3-POINT ESTIMATION                      |
================================================================================

    프로젝트: 소프트웨어 개발 (확률적 일정 분석)

    각 작업 표기법:
    ┌─────────────────────────────────────┐
    │  [작업명]                           │
    │  O = 낙관적, M = 기대, P = 비관적    │
    │  TE = (O+4M+P)/6, σ = (P-O)/6       │
    └─────────────────────────────────────┘

    ┌─────────────────────────────┐        ┌─────────────────────────────┐
    │  [A. 요구사항 분석]          │        │  [B. 아키텍처 설계]          │
    │  O=5, M=8, P=15             │───────>│  O=7, M=10, P=18            │
    │  TE=8.7, σ=1.67             │        │  TE=10.8, σ=1.83            │
    └─────────────────────────────┘        └─────────────────────────────┘
                 │                                    │
                 │                                    │
                 v                                    v
    ┌─────────────────────────────┐        ┌─────────────────────────────┐
    │  [C. UI/UX 설계]             │        │  [D. 백엔드 개발]            │
    │  O=8, M=12, P=20            │        │  O=15, M=25, P=45           │
    │  TE=13.5, σ=2.0             │        │  TE=26.7, σ=5.0             │
    └─────────────────────────────┘        └─────────────────────────────┘
                 │                                    │
                 └──────────────┬─────────────────────┘
                                │
                                v
                   ┌─────────────────────────────┐
                   │  [E. 통합 및 테스트]          │
                   │  O=10, M=15, P=25           │
                   │  TE=15.8, σ=2.5             │
                   └─────────────────────────────┘
                                │
                                v
                   ┌─────────────────────────────┐
                   │  [F. 배포]                   │
                   │  O=2, M=3, P=7              │
                   │  TE=3.5, σ=0.83             │
                   └─────────────────────────────┘

    ─────────────────────────────────────────────────────────────────────────

    CRITICAL PATH 분석:
    경로 1: A → B → D → E → F
    경로 2: A → C → E → F

    Critical Path: A → B → D → E → F (TE 합계 최대)

    프로젝트 기대 기간 (TE_total):
    = 8.7 + 10.8 + 26.7 + 15.8 + 3.5 = 65.5일

    프로젝트 표준편차 (σ_total):
    = √(1.67² + 1.83² + 5.0² + 2.5² + 0.83²)
    = √(2.79 + 3.35 + 25.0 + 6.25 + 0.69)
    = √38.08 = 6.17일

    완료 확률 계산:
    - 70일 내 완료: Z = (70-65.5)/6.17 = 0.73 → 76.7%
    - 75일 내 완료: Z = (75-65.5)/6.17 = 1.54 → 93.8%
    - 80일 내 완료: Z = (80-65.5)/6.17 = 2.35 → 99.1%

================================================================================
```

### 2. β-분포와 가중평균 원리

```
================================================================================
|                    BETA DISTRIBUTION FOR PERT                                 |
================================================================================

                    확률밀도
                       ^
                       │         ___
                       │      __/   \__
                       │    _/         \_
                       │  _/             \_
                       │_/                 \___
    ───────────────────┼────────────────────────────────────────> 시간
                       O        M              P

    O (Optimistic):   낙관적 추정 - 최단 소요시간
    M (Most Likely):  최빈치 - 가장 자주 발생하는 소요시간
    P (Pessimistic):  비관적 추정 - 최장 소요시간

    ─────────────────────────────────────────────────────────────────────────

    β-분포 가정 하의 가중평균 (PERT 공식):

    TE = (O + 4M + P) / 6

    가중치 설명:
    - O (낙관적): 가중치 1
    - M (최빈치): 가중치 4 ← "가장 확실한 정보"
    - P (비관적): 가중치 1

    예시: O=5, M=10, P=25
    TE = (5 + 4×10 + 25) / 6 = (5 + 40 + 25) / 6 = 70/6 ≈ 11.67일

    ─────────────────────────────────────────────────────────────────────────

    표준편차 (Standard Deviation):

    σ = (P - O) / 6

    근거: β-분포의 표준편차가 대략 (P-O)/6

    예시: O=5, P=25
    σ = (25 - 5) / 6 = 20/6 ≈ 3.33일

    ─────────────────────────────────────────────────────────────────────────

    정규분포 근사 (중심극한정리):

    프로젝트 전체 소요시간은 정규분포를 따른다고 가정

    신뢰구간:
    - 68.3% 신뢰구간: TE ± 1σ
    - 95.5% 신뢰구간: TE ± 2σ
    - 99.7% 신뢰구간: TE ± 3σ

    예시: TE=65.5일, σ=6.17일
    - 95.5% 확률로 53.2일 ~ 77.9일 사이 완료
    - 99.7% 확률로 47.0일 ~ 84.0일 사이 완료

================================================================================
```

### 3. 심층 동작 원리: 완료 확률 계산 (5단계)

```
Step 1: 각 작업의 3점 추정치 수집
        ┌────────────────────────────────────────┐
        │ 전문가 인터뷰, 델파이 기법              │
        │                                        │
        │ Task A: O=5, M=8, P=15                 │
        │ Task B: O=7, M=10, P=18                │
        │ ...                                    │
        └────────────────────────────────────────┘
                         │
                         v
Step 2: 기대 시간(TE)과 표준편차(σ) 계산
        ┌────────────────────────────────────────┐
        │ TE = (O + 4M + P) / 6                  │
        │ σ = (P - O) / 6                        │
        │                                        │
        │ Task A: TE=8.7, σ=1.67                 │
        │ Task B: TE=10.8, σ=1.83                │
        └────────────────────────────────────────┘
                         │
                         v
Step 3: Critical Path 식별 (CPM 적용)
        ┌────────────────────────────────────────┐
        │ TE 기준으로 CPM 수행                    │
        │                                        │
        │ Critical Path: A → B → D → E → F       │
        │ 프로젝트 TE = Σ(주공정 TE) = 65.5일     │
        └────────────────────────────────────────┘
                         │
                         v
Step 4: 프로젝트 표준편차 계산
        ┌────────────────────────────────────────┐
        │ σ_project = √(Σ(주공정 σ²))            │
        │                                        │
        │ σ²_total = 1.67² + 1.83² + 5.0² + ...  │
        │          = 38.08                       │
        │ σ_total = 6.17일                       │
        └────────────────────────────────────────┘
                         │
                         v
Step 5: 완료 확률 계산 (Z-점수 활용)
        ┌────────────────────────────────────────┐
        │ Z = (목표일 - TE_total) / σ_total      │
        │                                        │
        │ 목표 70일: Z = (70-65.5)/6.17 = 0.73   │
        │ → 정규분포표 조회: P(Z<0.73) = 0.767   │
        │ → 76.7% 확률로 70일 내 완료            │
        │                                        │
        │ 목표 75일: Z = 1.54 → 93.8%            │
        │ 목표 80일: Z = 2.35 → 99.1%            │
        └────────────────────────────────────────┘
```

### 4. 핵심 코드: PERT 분석 엔진

```python
"""
PERT (Program Evaluation and Review Technique) Calculator
확률적 일정 분석 엔진
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import math

@dataclass
class PERTTask:
    """PERT 작업 정의"""
    task_id: str
    name: str
    optimistic: float      # O: 낙관적 추정
    most_likely: float     # M: 최빈치/기대치
    pessimistic: float     # P: 비관적 추정
    predecessors: List[str]

    # 계산 결과
    expected_time: float = 0.0  # TE
    std_deviation: float = 0.0  # σ
    variance: float = 0.0       # V = σ²

    def calculate_pert(self):
        """PERT 공식 적용"""
        self.expected_time = (self.optimistic +
                              4 * self.most_likely +
                              self.pessimistic) / 6
        self.std_deviation = (self.pessimistic - self.optimistic) / 6
        self.variance = self.std_deviation ** 2


class PERTAnalyzer:
    """PERT 분석기"""

    def __init__(self):
        self.tasks: Dict[str, PERTTask] = {}
        self.critical_path: List[str] = []

    def add_task(self, task: PERTTask):
        """작업 추가"""
        task.calculate_pert()
        self.tasks[task.task_id] = task

    def find_critical_path(self) -> List[str]:
        """Critical Path 식별 (간단화된 구현)"""
        # 실제로는 CPM 알고리즘 적용
        # 여기서는 예시용 하드코딩
        self.critical_path = ["A", "B", "D", "E", "F"]
        return self.critical_path

    def calculate_project_duration(self) -> Tuple[float, float]:
        """프로젝트 기간 및 표준편차 계산"""
        if not self.critical_path:
            self.find_critical_path()

        total_te = sum(self.tasks[t_id].expected_time
                       for t_id in self.critical_path)

        total_variance = sum(self.tasks[t_id].variance
                            for t_id in self.critical_path)

        total_std = math.sqrt(total_variance)

        return total_te, total_std

    def calculate_completion_probability(self, target_days: float) -> float:
        """목표 기간 내 완료 확률 계산"""
        te, sigma = self.calculate_project_duration()

        if sigma == 0:
            return 100.0 if target_days >= te else 0.0

        z_score = (target_days - te) / sigma

        # 정규분포 누적확률 (근사 공식)
        probability = self._normal_cdf(z_score) * 100

        return probability

    def _normal_cdf(self, z: float) -> float:
        """표준정규분포 누적분포함수 (근사)"""
        # Abramowitz and Stegun 근사 공식
        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911

        sign = 1 if z >= 0 else -1
        z = abs(z) / math.sqrt(2)

        t = 1.0 / (1.0 + p * z)
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-z * z)

        return 0.5 * (1.0 + sign * y)

    def get_confidence_intervals(self) -> Dict[str, Tuple[float, float]]:
        """신뢰구간 계산"""
        te, sigma = self.calculate_project_duration()

        return {
            "68.3% (1σ)": (te - sigma, te + sigma),
            "95.5% (2σ)": (te - 2*sigma, te + 2*sigma),
            "99.7% (3σ)": (te - 3*sigma, te + 3*sigma),
        }

    def generate_report(self) -> str:
        """분석 보고서 생성"""
        te, sigma = self.calculate_project_duration()

        report = [
            "\n" + "="*70,
            "PERT ANALYSIS REPORT",
            "="*70,
            f"\n{'작업':<20} {'O':>6} {'M':>6} {'P':>6} {'TE':>8} {'σ':>8}",
            "-"*70,
        ]

        for task_id, task in self.tasks.items():
            critical = "★" if task_id in self.critical_path else " "
            report.append(
                f"{critical}{task.name:<19} {task.optimistic:>6.1f} "
                f"{task.most_likely:>6.1f} {task.pessimistic:>6.1f} "
                f"{task.expected_time:>8.2f} {task.std_deviation:>8.2f}"
            )

        report.extend([
            "-"*70,
            f"\nCritical Path: {' → '.join([self.tasks[t].name for t in self.critical_path])}",
            f"\n프로젝트 기대 기간 (TE): {te:.1f}일",
            f"프로젝트 표준편차 (σ): {sigma:.2f}일",
            f"\n완료 확률 분석:",
        ])

        for target in [te, te + sigma, te + 2*sigma, te + 3*sigma]:
            prob = self.calculate_completion_probability(target)
            report.append(f"  - {target:.1f}일 내 완료: {prob:.1f}%")

        report.extend([
            f"\n신뢰구간:",
        ])

        for level, (low, high) in self.get_confidence_intervals().items():
            report.append(f"  - {level}: {low:.1f}일 ~ {high:.1f}일")

        report.append("="*70)

        return "\n".join(report)


# 사용 예시
if __name__ == "__main__":
    analyzer = PERTAnalyzer()

    # 소프트웨어 개발 프로젝트 작업 정의 (3점 추정)
    tasks = [
        PERTTask("A", "요구사항 분석", 5, 8, 15, []),
        PERTTask("B", "아키텍처 설계", 7, 10, 18, ["A"]),
        PERTTask("C", "UI/UX 설계", 8, 12, 20, ["A"]),
        PERTTask("D", "백엔드 개발", 15, 25, 45, ["B"]),
        PERTTask("E", "프론트엔드 개발", 12, 18, 30, ["C"]),
        PERTTask("F", "통합 테스트", 10, 15, 25, ["D", "E"]),
        PERTTask("G", "배포", 2, 3, 7, ["F"]),
    ]

    for task in tasks:
        analyzer.add_task(task)

    print(analyzer.generate_report())

    # 특정 목표일에 대한 완료 확률
    target = 75
    prob = analyzer.calculate_completion_probability(target)
    print(f"\n{target}일 내 완료 확률: {prob:.1f}%")
```

---

## III. 융합 비교 및 다각도 분석

### 1. 심층 기술 비교: PERT vs CPM vs 몬테카를로

| 비교 항목 | PERT | CPM | 몬테카를로 시뮬레이션 |
|:---|:---|:---|:---|
| **소요시간** | 확률적 (3점) | 확정적 (단일값) | 확률적 (분포) |
| **분포 가정** | β-분포 | 없음 | 임의 분포 가능 |
| **계산 복잡도** | 중간 | 낮음 | 높음 (반복 수행) |
| **정확도** | 중간 | 낮음 (확정적) | 높음 |
| **완료 확률** | 제공 (정규근사) | 없음 | 제공 (정확) |
| **도구 지원** | MS Project | 모든 PM 도구 | @Risk, Crystal Ball |

### 2. PERT와 CPM의 통합 (PERT/CPM)

```
[PERT/CPM 통합 워크플로우]

Step 1: CPM 네트워크 구축
        - 작업 간 선후관계 정의
        - 간트차트/네트워크 다이어그램 작성

Step 2: PERT 3점 추정
        - 각 작업에 대해 O, M, P 추정
        - TE = (O + 4M + P) / 6 계산

Step 3: CPM 계산 (TE 활용)
        - Forward/Backward Pass
        - Critical Path 식별

Step 4: PERT 확률 분석
        - Critical Path 분산 합산
        - 완료 확률 계산

Step 5: 리스크 대응
        - 높은 σ 작업 식별 → 리스크 완화
        - 시나리오 분석 (What-If)
```

### 3. 과목 융합: PERT + 비용 산정 (COCOMO)

```
[PERT를 활용한 COCOMO 보정]

COCOMO 기본 공식:
E = a × (KLOC)^b × EAF

여기서 일정(T) 산정 시 PERT 활용:

전통적 COCOOMO:
T = c × E^d (단일값)

PERT 기반 일정:
1. COCOMO로 E (인월) 산정
2. E를 작업별로 분배
3. 각 작업에 PERT 3점 추정 적용
4. 전체 일정 확률 분포 산출

예시:
- COCOMO E = 24인월
- 작업 분해 후 PERT 분석
- 결과: "95% 확률로 8~12개월 내 완료"
```

---

## IV. 실무 적용 및 기술사적 판단

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오] R&D 프로젝트 일정 계약**

*   **상황**:
    - AI 기반 신규 서비스 개발
    - 기술적 불확실성 높음 (신기술 적용)
    - 고객: "정확히 언제 완료되나요?"

*   **기술사적 판단**: **PERT 기반 확률적 계약**

*   **실행 전략**:
    ```
    1. 3점 추정 수행 (전문가 델파이)
    2. PERT 분석 결과:
       - 기대 일정: 120일
       - 표준편차: 18일

    3. 계약안 제시:
       - "50% 확률로 120일 완료"
       - "85% 확률로 138일 완료"
       - "95% 확률로 150일 완료"

    4. 고객 합의: 140일 (85% 신뢰수준)
       - 조기 완료 시 인센티브
       - 지연 시 페널티 (단, 150일까지는 면책)
    ```

### 2. 도입 시 고려사항

**추정 품질**:
- [ ] 전문가 역량: O, M, P 추정의 신뢰성
- [ ] 과거 데이터: 유사 프로젝트 실적 활용
- [ ] 델파이 합의: 다수 전문가 합의 도출

**활용 수준**:
- [ ] 단순 PERT: 3점 추정 + 가중평균
- [ ] PERT/CPM: 네트워크 분석 통합
- [ ] 몬테카를로: 정밀 확률 분석

### 3. 주의사항 및 안티패턴

*   **허구적 정확도 (Illusion of Precision)**:
    - PERT 결과가 "정확한 것처럼" 착각
    - 해결: "확률적 추정"임을 명확히 커뮤니케이션

*   **낙관적 편향 (Optimism Bias)**:
    - O를 너무 낮게, P를 너무 높지 않게 추정
    - 해결: Reference Class Forecasting (과거 데이터 활용)

---

## V. 기대효과 및 결론

### 1. 정량적/정성적 기대효과

| 구분 | 효과 내용 | 기대 수치 |
|:---:|:---|:---|
| **일정 예측** | 완료 확률 제공 | 의사결정 품질 향상 |
| **리스크 관리** | 고위험 작업 식별 | σ 큰 작업 집중 관리 |
| **계약 협상** | 현실적 일정 합의 | 분쟁 감소 |
| **신뢰성** | 확률 기반 근거 | 이해관계자 신뢰 확보 |

### 2. 미래 전망

1.  **AI 기반 추정**: 과거 프로젝트 데이터로 O, M, P 자동 추천
2.  **실시간 PERT**: 진척률에 따른 확률 재계산
3.  **몬테카를로 통합**: PERT → 몬테카를로 자동 전환

### 3. 참고 표준

*   **PMBOK Guide**: Schedule Management - Three-Point Estimating
*   **PMI-SP**: Scheduling Professional 인증

---

## 관련 개념 맵 (Knowledge Graph)

*   [CPM](@/studynotes/4_software_engineering/1_sdlc/37_cpm.md) : PERT와 결합하여 PERT/CPM으로 통합
*   [WBS](@/studynotes/4_software_engineering/3_project/36_wbs.md) : PERT 적용 전 작업 분할
*   [델파이 기법](@/studynotes/4_software_engineering/1_sdlc/_index.md) : 3점 추정 시 전문가 합의 도출

---

## 어린이를 위한 3줄 비유 설명

1. **문제**: 여행 가는데 비행기 표가 언제 나올지 모르겠어요. 빨리 나올 수도 있고, 늦게 나올 수도 있어요.

2. **해결(PERT)**: **세 가지 경우**를 생각해요! "가장 빨리 3일, 보통 5일, 늦으면 10일" 이렇게요. 그리고 이걸 계산해서 "대부분 5~6일쯤 나올 거야"라고 말해요.

3. **효과**: "100% 확실히 5일이야"라고 거짓말하는 대신, "대부분 5일이지만 가끔 늦어질 수도 있어요"라고 솔직하게 말할 수 있어요!
