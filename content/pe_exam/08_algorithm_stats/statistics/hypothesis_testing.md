+++
title = "가설 검정 (Hypothesis Testing)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 가설 검정 (Hypothesis Testing)

## 핵심 인사이트 (3줄 요약)
> **표본 데이터로 모집단 가설을 통계적으로 검증**. 귀무가설 vs 대립가설. 유의수준과 p-value로 판단.

---

### Ⅰ. 개요

**개념**: 가설 검정(Hypothesis Testing)은 **표본 데이터를 바탕으로 모집단에 대한 주장(가설)이 참인지 거짓인지를 통계적으로 판단하는 추론 방법**이다.

> 💡 **비유**: "법정 판결 과정" - 피고는 무죄로 간주(귀무가설)되고, 증거(데이터)가 충분히 강력하면 유죄로 판결(귀무가설 기각)하는 것과 같아요.

**등장 배경** (3가지 이상 기술):

1. **기존 문제점**: 모집단 전수조사는 비용과 시간이 너무 많이 들어 현실적으로 불가능. 소수 표본으로 전체를 어떻게 판단할 것인가?
2. **기술적 필요성**: 약물 효과, 신제품 성능, 교육 프로그램 효과 등이 "통계적으로 유의미한가"를 객관적으로 판단하는 과학적 방법 필요
3. **산업적 요구**: A/B 테스트, 품질 관리, 의약품 임상시험 등에서 의사결정의 근거를 마련하는 표준화된 절차 필요

**핵심 목적**: 제한된 표본 데이터로 모집단에 대한 주장을 오류 가능성을 정량화하며 검증하는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (4개 이상):

| 구성 요소 | 영어 | 역할/기능 | 비유 |
|----------|------|----------|------|
| 귀무가설 H₀ | Null Hypothesis | 차이/효과 없음을 가정 | 무죄 추정 |
| 대립가설 H₁ | Alternative Hypothesis | 차이/효과 있음을 주장 | 유죄 주장 |
| 유의수준 α | Significance Level | 제1종 오류 허용 확률 | "증거 기준" |
| p-value | p-value | 귀무가설 하에서 극단적 결과 확률 | "증거의 강도" |
| 검정통계량 | Test Statistic | 표본 데이터로 계산한 값 | "재판 결과" |

**구조 다이어그램**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    가설 검정 절차                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │  1. 가설 설정 │ ──→ │ 2. 유의수준   │ ──→ │ 3. 검정통계량 │   │
│   │  H₀ vs H₁    │     │   α 설정      │     │   계산        │   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│                                                      │          │
│                      ┌───────────────────────────────┘          │
│                      ↓                                          │
│              ┌──────────────┐     ┌──────────────┐              │
│              │ 4. p-value   │ ──→ │ 5. 결론 도출  │              │
│              │   계산/비교   │     │  기각/채택    │              │
│              └──────────────┘     └──────────────┘              │
│                                                                 │
│   결정 규칙:                                                    │
│   ┌────────────────────────────────────────────────────────┐   │
│   │  p-value < α  →  H₀ 기각 (통계적으로 유의미)           │   │
│   │  p-value ≥ α  →  H₀ 채택 (유의미하지 않음)             │   │
│   └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**오류 유형 매트릭스**:

```
┌────────────────────────────────────────────────────────────┐
│                    판단 vs 실제                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│              실제 H₀ 참          실제 H₀ 거짓              │
│           (효과 없음)           (효과 있음)                │
│         ┌─────────────┬─────────────┐                      │
│   H₀ 기각│ 제1종 오류  │   정상      │                      │
│  (유의미)│   (α)       │  (정탐)     │                      │
│         ├─────────────┼─────────────┤                      │
│   H₀ 채택│   정상      │ 제2종 오류  │                      │
│ (무의미)│  (정상)      │   (β)       │                      │
│         └─────────────┴─────────────┘                      │
│                                                            │
│   • 제1종 오류 (Type I): 없는 효과가 있다고 판단 (거짓 양성)│
│   • 제2종 오류 (Type II): 있는 효과가 없다고 판단 (거짓 음성)│
│   • 검정력 (Power): 1 - β = 진짜 효과를 탐지할 확률        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**검정 방법 선택 기준**:

| 조건 | 모분산 | 표본크기 | 검정법 | 검정통계량 |
|-----|--------|---------|--------|-----------|
| 모평균 검정 | 앎 | n ≥ 30 | z-검정 | z = (x̄-μ)/(σ/√n) |
| 모평균 검정 | 모름 | n < 30 | t-검정 | t = (x̄-μ)/(s/√n) |
| 두 집단 평균 | - | - | 독립표본 t-검정 | t = (x̄₁-x̄₂)/SE |
| 대응표본 | - | - | 대응 t-검정 | t = d̄/(s_d/√n) |
| 모비율 검정 | - | np, n(1-p) ≥ 5 | z-검정 | z = (p̂-p)/√(p(1-p)/n) |
| 분산 검정 | - | - | χ²-검정 | χ² = (n-1)s²/σ² |
| 독립성 검정 | - | - | χ²-검정 | χ² = Σ(O-E)²/E |
| 분산분석 | - | - | F-검정 | F = MSB/MSW |

**동작 원리** (단계별 상세 설명):

```
① 가설수립 → ② 유의수준설정 → ③ 검정통계량계산 → ④ p-value산출 → ⑤ 결론도출
```

- **1단계**: 귀무가설(H₀)과 대립가설(H₁)을 명확히 정의. H₀은 보통 "차이 없음", H₁은 "차이 있음"
- **2단계**: 제1종 오류 허용 수준(α)을 설정. 일반적으로 0.05(5%) 또는 0.01(1%)
- **3단계**: 표본 데이터에서 검정통계량(z, t, χ², F 등)을 계산
- **4단계**: 검정통계량으로부터 p-value를 계산하거나 임계값과 비교
- **5단계**: p-value < α이면 H₀ 기각, 아니면 H₀ 채택 (채택은 "기각할 증거 부족"의 의미)

**코드 예시** (Python):

```python
from typing import Tuple, List
import math

class HypothesisTest:
    """가설 검정 구현체"""

    @staticmethod
    def z_test(sample_mean: float, pop_mean: float, pop_std: float,
               n: int, alpha: float = 0.05, two_tailed: bool = True) -> dict:
        """
        단일 표본 z-검정
        모분산을 아는 경우의 모평균 검정
        """
        # 검정통계량 계산
        se = pop_std / math.sqrt(n)
        z_stat = (sample_mean - pop_mean) / se

        # p-value 계산 (정규분포 CDF 근사)
        p_value = HypothesisTest._normal_pvalue(z_stat, two_tailed)

        # 임계값
        z_crit = HypothesisTest._z_critical(alpha, two_tailed)

        return {
            'test_statistic': z_stat,
            'p_value': p_value,
            'critical_value': z_crit,
            'reject_null': abs(z_stat) > z_crit,
            'alpha': alpha,
            'test_type': 'z-test'
        }

    @staticmethod
    def t_test(sample_mean: float, pop_mean: float, sample_std: float,
               n: int, alpha: float = 0.05, two_tailed: bool = True) -> dict:
        """
        단일 표본 t-검정
        모분산을 모르는 경우의 모평균 검정
        """
        # 검정통계량 계산
        se = sample_std / math.sqrt(n)
        t_stat = (sample_mean - pop_mean) / se
        df = n - 1  # 자유도

        # p-value 계산 (t-분포 근사)
        p_value = HypothesisTest._t_pvalue(t_stat, df, two_tailed)

        # 임계값
        t_crit = HypothesisTest._t_critical(alpha, df, two_tailed)

        return {
            'test_statistic': t_stat,
            'p_value': p_value,
            'critical_value': t_crit,
            'degrees_of_freedom': df,
            'reject_null': abs(t_stat) > t_crit,
            'alpha': alpha,
            'test_type': 't-test'
        }

    @staticmethod
    def two_sample_t_test(mean1: float, mean2: float, std1: float, std2: float,
                          n1: int, n2: int, alpha: float = 0.05,
                          equal_var: bool = False) -> dict:
        """
        독립 두 표본 t-검정
        두 집단 평균 차이 검정
        """
        if equal_var:
            # 등분산 가정: pooled variance
            pooled_var = ((n1-1)*std1**2 + (n2-1)*std2**2) / (n1 + n2 - 2)
            se = math.sqrt(pooled_var * (1/n1 + 1/n2))
            df = n1 + n2 - 2
        else:
            # 이분산 가정: Welch's t-test
            se = math.sqrt(std1**2/n1 + std2**2/n2)
            # Welch-Satterthwaite 자유도
            df = ((std1**2/n1 + std2**2/n2)**2 /
                  ((std1**2/n1)**2/(n1-1) + (std2**2/n2)**2/(n2-1)))

        t_stat = (mean1 - mean2) / se
        p_value = HypothesisTest._t_pvalue(t_stat, df, two_tailed=True)
        t_crit = HypothesisTest._t_critical(alpha, df, two_tailed=True)

        return {
            'test_statistic': t_stat,
            'p_value': p_value,
            'critical_value': t_crit,
            'degrees_of_freedom': df,
            'reject_null': abs(t_stat) > t_crit,
            'test_type': 'two-sample t-test (Welch)' if not equal_var else 'two-sample t-test (pooled)'
        }

    @staticmethod
    def paired_t_test(before: List[float], after: List[float],
                      alpha: float = 0.05) -> dict:
        """
        대응표본 t-검정 (쌍체 t-검정)
        전후 비교, 쌍으로 된 데이터
        """
        if len(before) != len(after):
            raise ValueError("두 리스트 길이가 같아야 합니다")

        # 차이 계산
        differences = [a - b for a, b in zip(after, before)]
        n = len(differences)
        mean_diff = sum(differences) / n

        # 차이의 표준편차
        var_diff = sum((d - mean_diff)**2 for d in differences) / (n - 1)
        std_diff = math.sqrt(var_diff)

        # t-검정
        se = std_diff / math.sqrt(n)
        t_stat = mean_diff / se
        df = n - 1
        p_value = HypothesisTest._t_pvalue(t_stat, df, two_tailed=True)
        t_crit = HypothesisTest._t_critical(alpha, df, two_tailed=True)

        return {
            'mean_difference': mean_diff,
            'test_statistic': t_stat,
            'p_value': p_value,
            'critical_value': t_crit,
            'degrees_of_freedom': df,
            'reject_null': abs(t_stat) > t_crit,
            'test_type': 'paired t-test'
        }

    @staticmethod
    def proportion_test(successes: int, n: int, hypothesized_p: float = 0.5,
                        alpha: float = 0.05) -> dict:
        """
        모비율 검정 (z-검정)
        """
        sample_p = successes / n
        se = math.sqrt(hypothesized_p * (1 - hypothesized_p) / n)
        z_stat = (sample_p - hypothesized_p) / se
        p_value = HypothesisTest._normal_pvalue(z_stat, two_tailed=True)
        z_crit = HypothesisTest._z_critical(alpha, two_tailed=True)

        return {
            'sample_proportion': sample_p,
            'test_statistic': z_stat,
            'p_value': p_value,
            'critical_value': z_crit,
            'reject_null': abs(z_stat) > z_crit,
            'test_type': 'proportion z-test'
        }

    @staticmethod
    def chi_square_goodness_of_fit(observed: List[int], expected: List[float],
                                   alpha: float = 0.05) -> dict:
        """
        적합도 검정 (카이제곱)
        관측값이 기대분포를 따르는지 검정
        """
        if len(observed) != len(expected):
            raise ValueError("관측값과 기대값 길이가 같아야 합니다")

        chi_stat = sum((o - e)**2 / e for o, e in zip(observed, expected))
        df = len(observed) - 1
        p_value = HypothesisTest._chi_square_pvalue(chi_stat, df)
        chi_crit = HypothesisTest._chi_square_critical(alpha, df)

        return {
            'test_statistic': chi_stat,
            'p_value': p_value,
            'critical_value': chi_crit,
            'degrees_of_freedom': df,
            'reject_null': chi_stat > chi_crit,
            'test_type': 'chi-square goodness of fit'
        }

    # === 근사 함수들 (실제로는 scipy 등 사용 권장) ===

    @staticmethod
    def _normal_pvalue(z: float, two_tailed: bool) -> float:
        """정규분포 p-value 근사 (Abramowitz & Stegun)"""
        # 표준정규분포 CDF 근사
        a1, a2, a3, a4, a5 = 0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429
        k = 1 / (1 + 0.2316419 * abs(z))
        cdf = 1 - (1/math.sqrt(2*math.pi)) * math.exp(-z**2/2) * (a1*k + a2*k**2 + a3*k**3 + a4*k**4 + a5*k**5)

        if two_tailed:
            return 2 * (1 - cdf) if z >= 0 else 2 * cdf
        return 1 - cdf if z >= 0 else cdf

    @staticmethod
    def _t_pvalue(t: float, df: int, two_tailed: bool) -> float:
        """t-분포 p-value 근사 (큰 df에서 정규 근사)"""
        if df >= 30:
            return HypothesisTest._normal_pvalue(t, two_tailed)
        # 작은 df에서는 정규 근사 + 보정
        correction = 1 + t**2 / (2 * df)
        z = t / math.sqrt(correction)
        return HypothesisTest._normal_pvalue(z, two_tailed)

    @staticmethod
    def _z_critical(alpha: float, two_tailed: bool) -> float:
        """z 임계값"""
        if two_tailed:
            alpha = alpha / 2
        # 일반적 임계값
        crit_values = {0.10: 1.28, 0.05: 1.645, 0.025: 1.96, 0.01: 2.33, 0.005: 2.576}
        return crit_values.get(alpha, 1.96)

    @staticmethod
    def _t_critical(alpha: float, df: int, two_tailed: bool) -> float:
        """t 임계값 (근사)"""
        if two_tailed:
            alpha = alpha / 2
        # df가 크면 z에 수렴
        if df >= 30:
            return HypothesisTest._z_critical(alpha * 2, False)
        # 작은 df 보정
        t_correction = {1: 6.31, 2: 2.92, 3: 2.35, 4: 2.13, 5: 2.02,
                        10: 1.81, 15: 1.75, 20: 1.72, 25: 1.71}
        return t_correction.get(df, 1.96)

    @staticmethod
    def _chi_square_pvalue(chi: float, df: int) -> float:
        """카이제곱 p-value 근사"""
        # Wilson-Hilferty 변환으로 정규 근사
        z = ((chi / df) ** (1/3) - (1 - 2/(9*df))) / math.sqrt(2/(9*df))
        return HypothesisTest._normal_pvalue(z, two_tailed=False)

    @staticmethod
    def _chi_square_critical(alpha: float, df: int) -> float:
        """카이제곱 임계값 (근사)"""
        # 근사 공식
        h = 1 - 2/(9*df)
        z = HypothesisTest._z_critical(alpha * 2, False)
        return df * (h + z * math.sqrt(2/(9*df)))**3


def interpret_result(result: dict) -> str:
    """검정 결과 해석"""
    if result['reject_null']:
        conclusion = (f"결론: 통계적으로 유의미함 (p={result['p_value']:.4f} < α={result['alpha']})\n"
                     f"→ 귀무가설을 기각합니다.")
    else:
        conclusion = (f"결론: 통계적으로 유의미하지 않음 (p={result['p_value']:.4f} ≥ α={result.get('alpha', 0.05)})\n"
                     f"→ 귀무가설을 기각할 증거가 부족합니다.")
    return conclusion


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("가설 검정 예시")
    print("=" * 60)

    # 1. 단일 표본 z-검정
    print("\n1. 단일 표본 z-검정")
    print("문제: 한 공장의 제품 무게가 평균 100g(표준편차 5g)이어야 한다.")
    print("      36개 표본의 평균이 102g일 때, 평균이 변했는가?")
    result = HypothesisTest.z_test(
        sample_mean=102, pop_mean=100, pop_std=5, n=36, alpha=0.05
    )
    print(f"H₀: μ = 100, H₁: μ ≠ 100")
    print(f"z-통계량: {result['test_statistic']:.3f}")
    print(f"p-value: {result['p_value']:.4f}")
    print(f"임계값: ±{result['critical_value']:.3f}")
    print(interpret_result(result))

    # 2. 단일 표본 t-검정
    print("\n2. 단일 표본 t-검정")
    print("문제: 새로운 학습법이 효과가 있는지 16명에게 적용.")
    print("      평균 점수 향상 5점, 표준편차 8점. 효과가 있는가?")
    result = HypothesisTest.t_test(
        sample_mean=5, pop_mean=0, sample_std=8, n=16, alpha=0.05
    )
    print(f"H₀: μ = 0 (효과 없음), H₁: μ ≠ 0 (효과 있음)")
    print(f"t-통계량: {result['test_statistic']:.3f}")
    print(f"p-value: {result['p_value']:.4f}")
    print(f"자유도: {result['degrees_of_freedom']}")
    print(interpret_result(result))

    # 3. 독립 두 표본 t-검정
    print("\n3. 독립 두 표본 t-검정 (Welch)")
    print("문제: 두 교육법의 효과 비교")
    print("      A그룹: n=25, 평균=78, 표준편차=10")
    print("      B그룹: n=30, 평균=85, 표준편차=12")
    result = HypothesisTest.two_sample_t_test(
        mean1=78, std1=10, n1=25,
        mean2=85, std2=12, n2=30,
        alpha=0.05, equal_var=False
    )
    print(f"H₀: μ₁ = μ₂, H₁: μ₁ ≠ μ₂")
    print(f"t-통계량: {result['test_statistic']:.3f}")
    print(f"p-value: {result['p_value']:.4f}")
    print(interpret_result(result))

    # 4. 대응표본 t-검정
    print("\n4. 대응표본 t-검정")
    print("문제: 다이어트 프로그램 전후 체중 변화")
    before = [70, 75, 80, 68, 72, 78, 85, 65]
    after = [68, 73, 77, 67, 70, 75, 82, 63]
    result = HypothesisTest.paired_t_test(before, after, alpha=0.05)
    print(f"평균 변화: {result['mean_difference']:.2f}kg")
    print(f"t-통계량: {result['test_statistic']:.3f}")
    print(f"p-value: {result['p_value']:.4f}")
    print(interpret_result(result))

    # 5. 모비율 검정
    print("\n5. 모비율 검정")
    print("문제: 동전 던지기 100회 중 앞면 60회. 공정한 동전인가?")
    result = HypothesisTest.proportion_test(
        successes=60, n=100, hypothesized_p=0.5, alpha=0.05
    )
    print(f"H₀: p = 0.5 (공정), H₁: p ≠ 0.5 (불공정)")
    print(f"표본 비율: {result['sample_proportion']:.2%}")
    print(f"z-통계량: {result['test_statistic']:.3f}")
    print(f"p-value: {result['p_value']:.4f}")
    print(interpret_result(result))
```

---

### Ⅲ. 기술 비교 분석

**장단점 분석**:

| 장점 | 단점 |
|-----|------|
| 객관적 의사결정 기준 제공 | p-value 오해/남용 가능성 |
| 과학적 근거로 인정받음 | 표본 크기에 민감 (클수록 유의) |
| 재현 가능한 결과 | 유의수준(α) 설정의 임의성 |
| 다양한 상황에 적용 가능 | 효과 크기(effect size) 무시 위험 |
| 오류 확률 정량화 | "유의미 ≠ 중요" 혼동 |

**검정 방법 비교**:

| 비교 항목 | z-검정 | t-검정 | χ²-검정 | F-검정 |
|---------|--------|--------|---------|--------|
| 핵심 용도 | 모평균 (모분산 已知) | 모평균 (모분산 未知) | 분산, 적합도, 독립성 | 분산비교, ANOVA |
| 분포 | 정규분포 | t-분포 | 카이제곱분포 | F-분포 |
| 표본크기 | ★ n ≥ 30 권장 | ★ 소표본 가능 | 빈도 데이터 | 여러 집단 |
| 전제조건 | 정규성, 모분산 已知 | 정규성 | 기대빈도 ≥ 5 | 정규성, 등분산 |

> **★ 선택 기준**:
> - 모분산을 알고 표본이 크면 → **z-검정**
> - 모분산을 모르거나 소표본이면 → **t-검정**
> - 범주형 데이터 빈도 분석 → **χ²-검정**
> - 세 집단 이상 평균 비교 → **F-검정 (ANOVA)**

**단측 vs 양측 검정**:

| 유형 | 대립가설 | 용도 | 특징 |
|-----|----------|------|------|
| 양측 | H₁: μ ≠ μ₀ | 차이 존재 (방향 무관) | 가장 보수적 |
| 우측 | H₁: μ > μ₀ | 증가, 향상 | α 전부를 우측에 |
| 좌측 | H₁: μ < μ₀ | 감소, 저하 | α 전부를 좌측에 |

---

### Ⅳ. 실무 적용 방안

**기술사적 판단** (3개 이상 시나리오):

| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| A/B 테스트 | 신규 UI vs 기존 UI 전환율 비교 (두 표본 비율 검정) | 유의미한 개선만 도입, 실패 리스크 80% 감소 |
| 품질 관리 | 제품 불량률이 기준 이하인지 검정 (모비율 검정) | 불량률 50% 감소, 고객 불만 30% 감소 |
| 의약품 임상시험 | 신약 vs 위약 효과 차이 검정 (대응 t-검정) | FDA 승인 가능성 근거 확보 |
| 교육 효과 평가 | 프로그램 전후 점수 변화 (대응 t-검정) | 효과적 프로그램 식별, ROI 40% 향상 |

**실제 도입 사례**:

- **사례 1: Google A/B 테스트** - 모든 UI 변경을 가설 검정으로 검증. 41가지 파란색 실험으로 수억 달러 수익 증대. 통계적 유의성 없으면 변경 불허
- **사례 2: Pfizer 코로나19 백신 임상시험** - 3상에서 위약군과 백신군의 감염률 차이를 가설 검정. 95% 유효성, p < 0.0001로 승인 획득
- **사례 3: Amazon 개인화 추천** - 새로운 추천 알고리즘의 클릭률 개선 효과를 통계적으로 검증. 매일 수천 개의 가설 검정 수행

**도입 시 고려사항** (4가지 관점):

1. **기술적**:
   - 표본 크기 결정 (검정력 분석)
   - 정규성 가정 검증 (Shapiro-Wilk 등)
   - 다중 검정 보정 (Bonferroni, FDR)

2. **운영적**:
   - 테스트 기간 설정 (최소 표본 확보)
   - 실시간 vs 배치 검정
   - 조기 중단 규칙 (Early stopping)

3. **보안적**:
   - 데이터 조작으로 결과 왜곡 가능성
   - p-hacking (p-value 맞추기) 방지
   - 결과 공개 전 검증 절차

4. **경제적**:
   - 테스트 비용 vs 의사결정 가치
   - 표본 크기와 비용 트레이드오프
   - 오류 비용 (제1종 vs 제2종)

**주의사항 / 흔한 실수**:

- ❌ **p-value 오해**: p-value는 H₀이 참일 확률이 아님! (H₀ 하에서 데이터 확률)
- ❌ **유의성 vs 중요성 혼동**: 통계적 유의미 ≠ 실제로 중요한 차이
- ❌ **다중 검정 무시**: 여러 번 검정하면 우연히 유의한 결과 나올 확률 증가
- ❌ **p-hacking**: 유의해질 때까지 분석 반복 (과학적 비윤리)

**관련 개념 / 확장 학습**:

```
📌 가설 검정 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│                   가설 검정 연관 개념                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [확률분포] ←──→ [가설검정] ←──→ [신뢰구간]                   │
│        ↓                ↓                ↓                       │
│   [표본분포]      [검정력분석]      [효과크기]                   │
│        ↓                ↓                ↓                       │
│   [중심극한정리]  [다중검정]      [베이지안검정]                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| 신뢰구간 | 보완 개념 | 모수의 추정 범위, 가설 검정과 이중성 | `[신뢰구간](./confidence_interval.md)` |
| 효과 크기 | 필수 보완 | 통계적 유의성과 별개로 실제 차이의 크기 | `[효과크기](./effect_size.md)` |
| 검정력 | 핵심 개념 | 진짜 효과를 탐지할 확률 (1-β) | `[검정력](./statistical_power.md)` |
| 베이즈 정리 | 대안 접근 | 빈도주의 vs 베이지안 검정 | `[베이즈정리](./bayes_theorem.md)` |
| 기술통계 | 선행 개념 | 가설 검정 전 데이터 요약 | `[기술통계](./descriptive.md)` |

---

### Ⅴ. 기대 효과 및 결론

**정량적 기대 효과**:

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 의사결정 품질 | 데이터 기반 객관적 판단 | 의사결정 오류 40% 감소 |
| 리스크 관리 | 오류 확률 정량화 | 잘못된 투자 60% 감소 |
| 과학적 신뢰성 | 재현 가능한 결과 | 연구 재현성 90% 이상 |
| 비용 최적화 | 불필요한 변경 방지 | 실패 프로젝트 50% 감소 |

**미래 전망** (3가지 관점):

1. **기술 발전 방향**: 베이지안 검정으로 전환 추세. p-value 의존도 낮추고 효과 크기, 신뢰구간 강조 (APA 권장)
2. **시장 트렌드**: A/B 테스트 자동화, 다중 팔 실험(Multi-armed Bandit)으로 진화. MLOps에서 모델 성능 비교 표준화
3. **후속 기술**: 순차적 검정(Sequential Testing), 적응적 설계(Adaptive Design), 메타분석(Meta-analysis)

> **결론**: 가설 검정은 데이터 기반 의사결정의 핵심 도구로, 특히 디지털 시대에 그 중요성이 더욱 커지고 있다. p-value 남용 문제에도 불구하고, 적절히 사용하면 불확실성을 정량화하고 과학적 근거를 마련하는 가장 효과적인 방법이다. 효과 크기와 신뢰구간을 함께 보고하는 것이 미래의 표준이 될 것이다.

> **※ 참고 표준**: ISO 3534 (Statistics), NIST Engineering Statistics Handbook, FDA Statistical Guidance, APA Publication Manual

---

## 어린이를 위한 종합 설명

**가설 검정**은 마치 **법정에서 판사가 판결을 내리는 과정**과 같아요.

첫 번째 문단: 피고는 처음에 "무죄"라고 가정해요(귀무가설). 그리고 증거(데이터)를 하나씩 살펴봐요. 만약 증거가 너무나 강력해서 "이건 우연이 아니야!"라고 판단되면, 무죄 가정을 뒤집고 유죄 판결을 내려요(귀무가설 기각). 이때 "얼마나 강력한 증거여야 할까?"가 유의수준(α)이에요.

두 번째 문단: p-value는 "이 정도 증거가 우연히 나올 확률"이에요. p-value가 0.05(5%)보다 작으면 "5% 확률로 우연인 건 말이 안 돼!"라고 판단해요. 예를 들어, 동전을 100번 던졌는데 95번 앞면이 나왔다면, p-value는 거의 0에 가까워요. "이 동전은 공정하지 않아!"라고 판단하겠죠?

세 번째 문단: 하지만 조심해야 해요! "통계적으로 유의미하다"고 해서 "실제로 중요하다"는 뜻은 아니에요. 100만 명을 조사하면 아주 작은 차이도 유의미하게 나올 수 있거든요. 그래서 효과 크기(얼마나 큰 차이인가?)도 함께 봐야 해요. 좋은 과학자는 p-value만 보지 않고, "이 차이가 실제로 의미 있나?"를 항상 고민해요!

---

## ✅ 작성 완료 체크리스트

- [x] 핵심 인사이트 3줄 요약
- [x] Ⅰ. 개요: 개념 + 비유 + 등장배경(3가지)
- [x] Ⅱ. 구성요소: 표(5개) + 다이어그램 + 단계별 동작 + Python 코드
- [x] Ⅲ. 비교: 장단점 표 + 대안 비교표 + 선택 기준
- [x] Ⅳ. 실무: 적용 시나리오(4개) + 실제 사례(3개) + 고려사항(4가지) + 주의사항(4개)
- [x] Ⅴ. 결론: 정량 효과 표 + 미래 전망(3가지) + 참고 표준
- [x] 관련 개념: 5개 나열 + 개념 맵 + 링크
- [x] 어린이를 위한 종합 설명 (3문단)
