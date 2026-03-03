+++
title = "표본 추출 기법 (Sampling Techniques)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 표본 추출 기법 (Sampling Techniques)

## 핵심 인사이트 (3줄 요약)
> **모집단을 대표하는 부분집합을 과학적으로 선정**. 단순랜덤, 층화, 계통, 집락이 4대 확률추출. 대표성 확보와 비용절감의 균형이 핵심.

---

### Ⅰ. 개요

**개념**: 표본 추출(Sampling)은 **모집단 전체를 조사할 수 없을 때, 모집단의 특성을 잘 대변할 수 있는 부분 집합(표본)을 선정하는 과학적 방법**이다.

> 💡 **비유**: "국민 전체의 건강상태 파악" - 5천만 명을 다 검사할 수 없어요. 대신 5천 명만 검사해서 전체를 추정해요. 어떤 5천 명을 검사하느냐가 중요해요!

**등장 배경** (3가지 이상 기술):

1. **기존 문제점**: 전수조사는 비용, 시간, 인력 면에서 비현실적. 국세조사, 선거 등 특수한 경우만 가능
2. **기술적 필요성**: 통계적 추론을 위해 모집단을 대표하는 표본 필요. 표본오차를 정량화하여 신뢰도 확보
3. **산업적 요구**: 시장조사, 품질검사, 여론조사, 의료연구 등 다양한 분야에서 의사결정 근거 필요

**핵심 목적**: 제한된 자원으로 모집단의 특성을 정확하게 추정할 수 있는 대표성 있는 표본을 확보하는 것.

---

### Ⅱ. 구성 요소 및 핵심 원리

**구성 요소** (4개 이상):

| 구성 요소 | 영어 | 역할/기능 | 비유 |
|----------|------|----------|------|
| 모집단 | Population | 조사 대상 전체 | 대한민국 전체 국민 |
| 표본 | Sample | 실제 조사 대상 | 5천 명 조사 대상자 |
| 표본틀 | Sampling Frame | 표본 추출의 기준 목록 | 주민등록부, 전화번호부 |
| 표본크기 | Sample Size | 표본의 수 | n = 1,000 |
| 추출확률 | Selection Probability | 각 단위가 뽑힐 확률 | 1/50,000 |

**확률 추출 4대 기법**:

```
┌─────────────────────────────────────────────────────────────────┐
│                 확률 추출 4대 기법                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ 단순 무작위 추출 (Simple Random Sampling):                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 모든 단위가 동일한 추출 확률 (1/N)                      │ │
│  │  • 제비뽑기, 난수표, 컴퓨터 난수                           │ │
│  │  • 장점: 편향 없음, 통계이론 단순                          │ │
│  │  • 단점: 표본틀 필수, 분산 클 수 있음                      │ │
│  │  예: 100명 중 10명 추출 → 각각 10% 확률                   │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  2️⃣ 층화 추출 (Stratified Sampling):                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 모집단을 동질적 층(strata)으로 분할 후 각 층에서 추출   │ │
│  │  • 층 내 동질적, 층 간 이질적                              │ │
│  │  • 장점: ★ 대표성 높음, 오차 작음, 소집단 보장            │ │
│  │  • 단점: 층 분류 기준 설정 어려움                          │ │
│  │  예: 성별(남/여) 또는 연령대별로 나누어 비례 추출          │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  3️⃣ 계통 추출 (Systematic Sampling):                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 일정한 간격(k)으로 추출                                 │ │
│  │  • k = N/n (모집단 크기 / 표본 크기)                       │ │
│  │  • 장점: ★ 간편, 효율적, 균등 분포                         │ │
│  │  • 단점: 주기성 있으면 편향 발생                           │ │
│  │  예: 명부에서 매 10번째 사람 추출                          │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  4️⃣ 집락 추출 (Cluster Sampling):                              │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 모집단을 집락(cluster)으로 분할 후 일부 집락 전수 조사  │ │
│  │  • 집락 내 이질적, 집락 간 동질적                          │ │
│  │  • 장점: ★ 비용 절감, 지리적 효율성                        │ │
│  │  • 단점: 표본오차 가장 큼                                  │ │
│  │  예: 전국 학교 중 20개교 선정 → 각 학교 전체 학생 조사     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**층화 추출 vs 집락 추출 비교**:

```
┌─────────────────────────────────────────────────────────────────┐
│              층화 추출 vs 집락 추출 (핵심 차이)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  층화 추출 (Stratified):                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  [ 모집단 ]                                              │   │
│  │   /   |   \                                              │   │
│  │ [층1] [층2] [층3]  ← 층 내부: 동질적 (같은 학년)        │   │
│  │  ↓    ↓    ↓       ← 층 간: 이질적                      │   │
│  │  ●●   ●●   ●●     ← 모든 층에서 골고루 추출             │   │
│  │  ●●   ●●   ●●                                            │   │
│  │                                                          │   │
│  │  목적: 정확도 향상, 소집단 대표성 보장                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  집락 추출 (Cluster):                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  [ 모집단 ]                                              │   │
│  │   /   |   \                                              │   │
│  │ [C1] [C2] [C3]   ← 집락 내부: 이질적 (한 학교 전체)     │   │
│  │  ●●   ●●   ●●     ← 집락 간: 동질적                     │   │
│  │  ●●   ●●   ●●                                            │   │
│  │  ↓              ↓                                        │   │
│  │ [전수]         [전수]  ← 선택된 집락만 전수 조사         │   │
│  │                                                          │   │
│  │  목적: 비용 절감, 조사 편의성                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 구분 | 층화 추출 | 집락 추출 |
|-----|----------|----------|
| 집단 구성 원칙 | 층 내 동질, 층 간 이질 | 집락 내 이질, 집락 간 동질 |
| 추출 단위 | 개별 요소 | 집락 전체 |
| 조사 대상 | 모든 층에서 일부 | 일부 집락의 전체 |
| 목적 | 정확도 향상 | 비용 절감 |
| 표본오차 | 작음 | 큼 |
| 적용 예 | 연령대별 선호도 조사 | 전국 학교 일부 선정 |

**비확률 추출 기법**:

| 기법 | 특징 | 장점 | 단점 | 용도 |
|-----|------|------|------|------|
| 편의 추출 | 접근 용이한 대상 | 간편, 저렴 | 편향 심함 | 탐색적 조사 |
| 판단 추출 | 전문가 판단 | 전문성 활용 | 주관적 | 정성연구 |
| 할당 추출 | 층화 비슷, 비랜덤 | 구현 용이 | 편향 가능 | 시장조사 |
| 스노우볼 | 추천 연쇄 | 소수집단 접근 | 편향 큼 | 특수집단 |

**표본오차 vs 비표본오차**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    오차의 종류                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 표본 오차 (Sampling Error):                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 표본이 모집단을 완벽히 대표하지 못해 발생              │ │
│  │  • 표본 크기(n)가 커지면 감소                             │ │
│  │  • 정량화 가능: 표준오차 = σ/√n                          │ │
│  │  • 예: 1,000명 조사 → ±3.1% 오차                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ⚠️ 비표본 오차 (Non-sampling Error):                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • 표본 추출 외의 원인으로 발생                           │ │
│  │  • 표본 크기와 무관 (오히려 늘어날 수 있음!) ★            │ │
│  │  • 정량화 어려움                                          │ │
│  │  • 종류:                                                  │ │
│  │    - 커버리지 오차: 표본틀 불완전                         │ │
│  │    - 무응답 오차: 응답 거부                               │ │
│  │    - 측정 오차: 잘못된 질문, 기록 오류                    │ │
│  │    - 처리 오차: 데이터 입력 오류                          │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**동작 원리** (단계별 상세 설명):

```
① 모집단정의 → ② 표본틀구축 → ③ 추출방법선택 → ④ 표본크기결정 → ⑤ 표본추출
```

- **1단계**: 연구 목적에 맞는 모집단 명확히 정의 (대상, 시간, 공간)
- **2단계**: 모집단을 완전히 포함하는 표본틀(목록) 확보
- **3단계**: 비용, 정확도, 실현가능성 고려하여 추출 방법 선택
- **4단계**: 허용오차, 신뢰수준, 모집단 분산으로 표본크기 계산
- **5단계**: 선택된 방법으로 실제 표본 추출 수행

**코드 예시** (Python):

```python
from typing import List, Tuple, Dict, Any
import random
import math

class SamplingTechniques:
    """표본 추출 기법 구현"""

    @staticmethod
    def simple_random_sampling(population: List[Any], n: int, seed: int = None) -> List[Any]:
        """
        단순 무작위 추출 (Simple Random Sampling)
        모든 요소가 동일한 확률로 추출
        """
        if seed is not None:
            random.seed(seed)

        if n > len(population):
            raise ValueError("표본 크기가 모집단보다 클 수 없습니다")

        return random.sample(population, n)

    @staticmethod
    def systematic_sampling(population: List[Any], n: int, start: int = None) -> List[Any]:
        """
        계통 추출 (Systematic Sampling)
        일정한 간격(k)으로 추출
        """
        N = len(population)
        if n > N:
            raise ValueError("표본 크기가 모집단보다 클 수 없습니다")

        k = N // n  # 추출 간격
        if start is None:
            start = random.randint(0, k - 1)

        sample = []
        for i in range(n):
            index = (start + i * k) % N
            sample.append(population[index])

        return sample

    @staticmethod
    def stratified_sampling(population: List[Any], strata: List[int], n: int,
                           proportional: bool = True) -> Tuple[List[Any], List[int]]:
        """
        층화 추출 (Stratified Sampling)
        각 층에서 비례 또는 동일 크기로 추출

        population: 전체 데이터
        strata: 각 요소의 층 번호 (0, 1, 2, ...)
        n: 총 표본 크기
        proportional: 비례 추출 여부
        """
        if len(population) != len(strata):
            raise ValueError("모집단과 층 정보 길이가 일치해야 합니다")

        # 층별로 그룹화
        strata_groups: Dict[int, List[Any]] = {}
        for item, stratum in zip(population, strata):
            if stratum not in strata_groups:
                strata_groups[stratum] = []
            strata_groups[stratum].append(item)

        num_strata = len(strata_groups)
        sample = []
        sample_strata = []

        if proportional:
            # 비례 추출
            total = len(population)
            for stratum, group in strata_groups.items():
                stratum_n = round(n * len(group) / total)
                stratum_n = max(1, min(stratum_n, len(group)))  # 최소 1개, 최대 그룹 크기
                stratum_sample = random.sample(group, stratum_n)
                sample.extend(stratum_sample)
                sample_strata.extend([stratum] * stratum_n)
        else:
            # 동일 크기 추출
            stratum_n = n // num_strata
            for stratum, group in strata_groups.items():
                actual_n = min(stratum_n, len(group))
                stratum_sample = random.sample(group, actual_n)
                sample.extend(stratum_sample)
                sample_strata.extend([stratum] * actual_n)

        return sample, sample_strata

    @staticmethod
    def cluster_sampling(population: List[Any], clusters: List[int],
                        num_clusters: int) -> Tuple[List[Any], List[int]]:
        """
        집락 추출 (Cluster Sampling)
        일부 집락을 선택하고 선택된 집락의 모든 요소 조사

        population: 전체 데이터
        clusters: 각 요소의 집락 번호
        num_clusters: 선택할 집락 수
        """
        # 집락별로 그룹화
        cluster_groups: Dict[int, List[int]] = {}
        for idx, cluster in enumerate(clusters):
            if cluster not in cluster_groups:
                cluster_groups[cluster] = []
            cluster_groups[cluster].append(idx)

        # 집락 무작위 선택
        all_clusters = list(cluster_groups.keys())
        selected_clusters = random.sample(all_clusters, min(num_clusters, len(all_clusters)))

        # 선택된 집락의 모든 요소 추출
        sample = []
        sample_clusters = []
        for cluster in selected_clusters:
            for idx in cluster_groups[cluster]:
                sample.append(population[idx])
                sample_clusters.append(cluster)

        return sample, sample_clusters

    @staticmethod
    def multi_stage_sampling(population: List[Any], primary_units: List[int],
                            num_primary: int, secondary_ratio: float = 0.5) -> List[Any]:
        """
        다단계 추출 (Multi-stage Sampling)
        1단계: 1차 추출단위 선택
        2단계: 선택된 1차 단위에서 2차 추출
        """
        # 1단계: 1차 단위(집락) 선택
        _, selected_primary = SamplingTechniques.cluster_sampling(
            population, primary_units, num_primary
        )
        selected_primary_set = set(selected_primary)

        # 2단계: 선택된 1차 단위에서 2차 추출
        sample = []
        for item, unit in zip(population, primary_units):
            if unit in selected_primary_set:
                if random.random() < secondary_ratio:
                    sample.append(item)

        return sample


class SampleSizeCalculator:
    """표본 크기 계산기"""

    @staticmethod
    def for_proportion(p: float, margin_error: float = 0.05,
                       confidence_level: float = 0.95,
                       population_size: int = None) -> int:
        """
        비율 추정을 위한 표본 크기 계산
        n = Z² × p(1-p) / e²

        p: 예상 비율 (모르면 0.5)
        margin_error: 허용 오차 (예: 0.05 = ±5%)
        confidence_level: 신뢰수준 (0.90, 0.95, 0.99)
        population_size: 유한 모집단 보정 (선택)
        """
        # Z-값
        z_values = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_values.get(confidence_level, 1.96)

        # 기본 표본 크기
        n = (z ** 2 * p * (1 - p)) / (margin_error ** 2)

        # 유한 모집단 보정
        if population_size is not None and population_size > 0:
            n = n / (1 + (n - 1) / population_size)

        return math.ceil(n)

    @staticmethod
    def for_mean(std_dev: float, margin_error: float,
                 confidence_level: float = 0.95,
                 population_size: int = None) -> int:
        """
        평균 추정을 위한 표본 크기 계산
        n = Z² × σ² / e²
        """
        z_values = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_values.get(confidence_level, 1.96)

        n = (z ** 2 * std_dev ** 2) / (margin_error ** 2)

        if population_size is not None and population_size > 0:
            n = n / (1 + (n - 1) / population_size)

        return math.ceil(n)


class SamplingErrorEstimator:
    """표본오차 추정"""

    @staticmethod
    def standard_error_proportion(p: float, n: int) -> float:
        """비율의 표준오차: SE = √(p(1-p)/n)"""
        return math.sqrt(p * (1 - p) / n)

    @staticmethod
    def standard_error_mean(std_dev: float, n: int) -> float:
        """평균의 표준오차: SE = σ/√n"""
        return std_dev / math.sqrt(n)

    @staticmethod
    def confidence_interval_proportion(p: float, n: int,
                                       confidence: float = 0.95) -> Tuple[float, float]:
        """비율의 신뢰구간"""
        z_values = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_values.get(confidence, 1.96)
        se = SamplingErrorEstimator.standard_error_proportion(p, n)

        lower = max(0, p - z * se)
        upper = min(1, p + z * se)
        return lower, upper

    @staticmethod
    def margin_of_error(p: float, n: int, confidence: float = 0.95) -> float:
        """오차범위 계산"""
        z_values = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_values.get(confidence, 1.96)
        se = SamplingErrorEstimator.standard_error_proportion(p, n)
        return z * se


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("표본 추출 기법 예시")
    print("=" * 60)

    # 모집단 생성
    population = [f"학생{i+1}" for i in range(100)]
    # 층 정보 (학년: 1, 2, 3, 4)
    strata = [i // 25 for i in range(100)]
    # 집락 정보 (반: 1~10)
    clusters = [(i // 10) + 1 for i in range(100)]

    # 1. 단순 무작위 추출
    print("\n1. 단순 무작위 추출 (n=20)")
    sample = SamplingTechniques.simple_random_sampling(population, 20, seed=42)
    print(f"추출된 표본: {sample[:5]}... (총 {len(sample)}개)")

    # 2. 계통 추출
    print("\n2. 계통 추출 (n=20, k=5)")
    sample = SamplingTechniques.systematic_sampling(population, 20)
    print(f"추출된 표본: {sample[:5]}... (총 {len(sample)}개)")

    # 3. 층화 추출
    print("\n3. 층화 추출 (n=20, 비례)")
    sample, sample_strata = SamplingTechniques.stratified_sampling(
        population, strata, 20, proportional=True
    )
    stratum_counts = {}
    for s in sample_strata:
        stratum_counts[s] = stratum_counts.get(s, 0) + 1
    print(f"층별 표본 수: {dict(sorted(stratum_counts.items()))}")

    # 4. 집락 추출
    print("\n4. 집락 추출 (3개 반 선택)")
    sample, sample_clusters = SamplingTechniques.cluster_sampling(
        population, clusters, num_clusters=3
    )
    selected_classes = sorted(set(sample_clusters))
    print(f"선택된 반: {selected_classes}")
    print(f"총 표본 수: {len(sample)}")

    # 5. 표본 크기 계산
    print("\n5. 표본 크기 계산")
    n_95 = SampleSizeCalculator.for_proportion(
        p=0.5, margin_error=0.05, confidence_level=0.95
    )
    n_99 = SampleSizeCalculator.for_proportion(
        p=0.5, margin_error=0.05, confidence_level=0.99
    )
    print(f"95% 신뢰수준, ±5% 오차: n = {n_95}")
    print(f"99% 신뢰수준, ±5% 오차: n = {n_99}")

    # 유한 모집단 보정
    n_finite = SampleSizeCalculator.for_proportion(
        p=0.5, margin_error=0.05, confidence_level=0.95, population_size=1000
    )
    print(f"모집단 1,000명일 때: n = {n_finite}")

    # 6. 표본오차 계산
    print("\n6. 표본오차 예시")
    p, n = 0.45, 1000  # 지지율 45%, 표본 1000명
    se = SamplingErrorEstimator.standard_error_proportion(p, n)
    moe = SamplingErrorEstimator.margin_of_error(p, n, 0.95)
    ci = SamplingErrorEstimator.confidence_interval_proportion(p, n, 0.95)

    print(f"표준오차: ±{se:.3f} ({se*100:.1f}%)")
    print(f"오차범위 (95%): ±{moe:.3f} ({moe*100:.1f}%)")
    print(f"신뢰구간 (95%): [{ci[0]:.3f}, {ci[1]:.3f}]")
    print(f"→ 지지율 45% ± {moe*100:.1f}% = [{(p-moe)*100:.1f}%, {(p+moe)*100:.1f}%]")
