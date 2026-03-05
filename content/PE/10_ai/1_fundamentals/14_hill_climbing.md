+++
title = "언덕 오르기 탐색 (Hill Climbing)"
date = "2026-03-05"
[extra]
categories = "studynotes-ai"
+++

# 언덕 오르기 탐색 (Hill Climbing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 언덕 오르기(Hill Climbing)는 현재 상태의 이웃 상태들 중 더 좋은 상태로만 이동하는 탐욕적(Greedy) 국소 탐색 알고리즘으로, 구현이 간단하고 메모리 효율적이지만 지역 최적해(Local Optimum)에 갇히는 문제가 있다.
> 2. **가치**: 최적화 문제에서 빠른 근사 해를 찾는 데 유용하며, TSP(외판원 문제), 스케줄링, 기계 학습의 파라미터 최적화 등에서 활용된다. 변종으로 Stochastic, First-Choice, Random-Restart 등이 있다.
> 3. **융합**: 시뮬레이티드 어닐링(Simulated Annealing), 유전 알고리즘, 타부 서치(Tabu Search) 등의 메타휴리스틱 기법의 기반이 되며, 신경망 학습의 경사 하강법과도 개념적으로 연결된다.

---

## I. 개요 (Context & Background)

### 개념 정의

언덕 오르기 탐색(Hill Climbing)은 **현재 상태에서 시작하여, 이웃 상태들 중 더 좋은(더 높은 가치를 가진) 상태로만 계속 이동하며 최적해를 찾아가는 국소 탐색(Local Search) 알고리즘**이다. 등산가가 안개 낀 산에서 정상을 찾을 때 "가장 높은 곳으로 계속 이동"하는 전략과 유사하다.

**핵심 특징**:
- **탐욕적(Greedy)**: 항상 가장 좋아 보이는 이웃 선택
- **국소적(Local)**: 현재 상태의 이웃만 고려, 전역 시야 없음
- **메모리 효율**: 현재 상태만 유지, 경로 저장 안 함
- **비완전성**: 지역 최적해에 갇힐 수 있음

### 💡 비유: "안개 낀 산에서 정상 찾기"

언덕 오르기를 **"완전히 안개 낀 산에서 눈을 가리고 정상 찾기"**에 비유할 수 있다.

**상황**: 당신은 산의 어딘가에 서 있고, 정상(최적해)에 도달하고 싶다. 하지만 안개가 너무 짙어서 멀리는 전혀 보이지 않는다. 오직 발밑의 경사만 느낄 수 있다.

**언덕 오르기 전략**: "가장 가파르게 올라가는 방향으로 한 발짝 이동하자." 발밑에서 가장 높게 느껴지는 방향으로 계속 이동한다.

**문제점**:
1. **지역 정상(Local Maximum)**: 작은 봉우리에 도달하면, 그게 진짜 정상이 아니더라도 더 이상 갈 곳이 없다. 모든 방향이 아래로 내려가기 때문이다.
2. **평원(Plateau)**: 평지에 서면 어느 쪽도 더 높지 않아서 멈춘다.
3. **능선(Ridge)**: 능선에서는 양쪽이 모두 아래로 보여 진행을 멈출 수 있다.

### 등장 배경 및 발전 과정

#### 1. 전역 탐색의 비효율성

완전한 탐색(BFS, DFS, A*)은 상태 공간이 클 때 비실용적이다:
- **메모리 한계**: 상태 공간이 너무 커서 모든 상태 저장 불가
- **시간 한계**: 현실적인 시간 내에 탐색 완료 불가
- **실시간 요구**: 빠른 근사 해가 필요한 상황

#### 2. 국소 탐색의 등장

"완벽한 해보다 빠른 좋은 해" 철학:
- 현재 상태만 유지 → 메모리 O(1)
- 이웃만 평가 → 시간 효율적
- 실시간 적용 가능

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|----------|------|
| **상태** | 현재 해 | 문제에 따른 표현 | 비트, 숫자, 배열 | 산의 위치 |
| **이웃 함수** | 주변 해 생성 | 상태 변환 규칙 | 비트 플립, 교환 | 이동 가능 방향 |
| **평가 함수** | 해의 품질 | 목적 함수 f(x) | 점수, 비용 | 고도 |
| **선택 전략** | 다음 이동 결정 | 최선, 확률적, 첫 선택 | Greedy, Random | 이동 결정 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          언덕 오르기 탐색 프로세스                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [초기 상태 선택] ─────▶ [현재 상태 = 초기 상태]
                                  │
                                  ▼
                         ┌───────────────────┐
                         │    이웃 생성       │
                         │  Neighbor(current) │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   이웃 평가        │
                         │  각 n에 대해 f(n) │
                         └─────────┬─────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────────┐
                    │     더 나은 이웃이 있는가?        │
                    └──────────────┬───────────────────┘
                           Yes     │     No
                    ┌──────────────┴───────────────┐
                    │                              ▼
                    ▼                    ┌───────────────────┐
           ┌────────────────┐            │     종료          │
           │  최선 이웃 선택 │            │  현재 = 지역 최적  │
           │  (또는 확률적)  │            └───────────────────┘
           └───────┬────────┘
                   │
                   ▼
           ┌────────────────┐
           │  현재 = 최선   │
           │     이웃       │
           └───────┬────────┘
                   │
                   └──────────────▶ [이웃 생성] (반복)

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          언덕 오르기의 문제점                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [1차원 목적 함수] - 지역 최적해 예시

    값 ↑
       │              ★ 전역 최적 (Global Maximum)
       │             /\
       │            /  \
       │           /    \
       │    ◀── 지역 최적 (Local Maximum)
       │      /\  /      \
       │     /  \/        \
       │    /              \
       │───/────────────────\───▶ 상태
       │
       │   언덕 오르기는 A에서 시작하면
       │   지역 최적에 도달하여 멈춤
       │   전역 최적을 놓침!

    [능선(Ridge) 문제]

       3D 지형에서:
          /\
         /  \  ← 능선
        /    \
       ▼      ▼
      양쪽이 모두 아래로 보여
      능선 방향으로 진행하지 못함
```

### 심층 동작 원리

**① 기본 언덕 오르기 (Steepest Ascent)**

```python
def hill_climbing(initial_state, get_neighbors, evaluate):
    """
    기본 언덕 오르기 (Steepest Ascent Hill Climbing)

    Args:
        initial_state: 초기 상태
        get_neighbors: 상태 -> 이웃 리스트 반환 함수
        evaluate: 상태 -> 가치(점수) 반환 함수

    Returns:
        지역 최적 상태
    """
    current = initial_state

    while True:
        # 모든 이웃 생성 및 평가
        neighbors = get_neighbors(current)
        neighbor_values = [(n, evaluate(n)) for n in neighbors]

        # 최선의 이웃 찾기
        best_neighbor, best_value = max(neighbor_values, key=lambda x: x[1])

        # 더 나은 이웃이 없으면 종료
        if best_value <= evaluate(current):
            return current  # 지역 최적

        # 최선 이웃으로 이동
        current = best_neighbor
```

**② 확률적 언덕 오르기 (Stochastic Hill Climbing)**

```python
import random

def stochastic_hill_climbing(initial_state, get_neighbors, evaluate, max_iter=10000):
    """
    확률적 언덕 오르기

    더 나은 이웃 중 하나를 확률적으로 선택
    - uphill move를 확률적으로 수락
    """

    def uphill_probability(current_val, neighbor_val, temperature=1.0):
        """상향 이동 확률 계산"""
        if neighbor_val > current_val:
            # 더 좋으면 높은 확률로 선택
            diff = neighbor_val - current_val
            return 1 / (1 + math.exp(-diff / temperature))
        return 0

    current = initial_state

    for _ in range(max_iter):
        neighbors = get_neighbors(current)
        current_val = evaluate(current)

        # 상향 이동 가능한 이웃들
        uphill_neighbors = []
        for n in neighbors:
            n_val = evaluate(n)
            prob = uphill_probability(current_val, n_val)
            if prob > 0 and random.random() < prob:
                uphill_neighbors.append(n)

        if not uphill_neighbors:
            return current

        # 무작위 선택
        current = random.choice(uphill_neighbors)

    return current
```

**③ First-Choice 언덕 오르기**

```python
def first_choice_hill_climbing(initial_state, get_random_neighbor, evaluate, max_attempts=1000):
    """
    First-Choice Hill Climbing

    모든 이웃을 생성하는 대신, 하나씩 생성하며
    처음으로 더 좋은 이웃을 찾으면 즉시 이동
    (이웃 생성이 비용이 클 때 유용)
    """
    current = initial_state

    while True:
        current_val = evaluate(current)

        for _ in range(max_attempts):
            neighbor = get_random_neighbor(current)
            neighbor_val = evaluate(neighbor)

            if neighbor_val > current_val:
                current = neighbor
                break
        else:
            # max_attempts 내에 더 좋은 이웃 못 찾음
            return current
```

**④ Random-Restart 언덕 오르기**

```python
def random_restart_hill_climbing(
    generate_random_state,
    get_neighbors,
    evaluate,
    num_restarts=100,
    max_steps=1000
):
    """
    Random-Restart Hill Climbing

    여러 번 무작위 시작점에서 언덕 오르기 수행
    전역 최적에 도달할 확률 증가
    """
    best_state = None
    best_value = float('-inf')

    for _ in range(num_restarts):
        # 무작위 시작점
        current = generate_random_state()

        # 언덕 오르기
        for _ in range(max_steps):
            neighbors = get_neighbors(current)
            neighbor_values = [(n, evaluate(n)) for n in neighbors]
            best_neighbor, best_neighbor_val = max(neighbor_values, key=lambda x: x[1])

            if best_neighbor_val <= evaluate(current):
                break

            current = best_neighbor

        # 최선 갱신
        current_val = evaluate(current)
        if current_val > best_value:
            best_state = current
            best_value = current_val

    return best_state
```

**⑤ TSP 문제에 적용**

```python
import random
from typing import List, Tuple

def tsp_hill_climbing(cities: List[Tuple[float, float]], max_iter=10000):
    """
    TSP(외판원 문제)를 언덕 오르기로 해결

    상태: 도시 방문 순서 (순열)
    이웃: 두 도시 위치 교환 (2-opt)
    평가: 총 거리 (최소화)
    """

    def total_distance(tour):
        dist = 0
        for i in range(len(tour)):
            c1, c2 = cities[tour[i]], cities[tour[(i+1) % len(tour)]]
            dist += ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)**0.5
        return dist

    def get_neighbors(tour):
        """2-opt 이웃 생성"""
        neighbors = []
        n = len(tour)
        for i in range(n-1):
            for j in range(i+2, n):
                # i-j 구간 역순
                new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
                neighbors.append(new_tour)
        return neighbors

    def get_random_neighbor(tour):
        """무작위 2-opt 이웃"""
        n = len(tour)
        i = random.randint(0, n-2)
        j = random.randint(i+1, n-1)
        return tour[:i] + tour[i:j+1][::-1] + tour[j+1:]

    # 초기 해 (무작위 순열)
    current = list(range(len(cities)))
    random.shuffle(current)
    current_dist = total_distance(current)

    for iteration in range(max_iter):
        # First-Choice 방식
        improved = False
        for _ in range(len(cities) * 2):
            neighbor = get_random_neighbor(current)
            neighbor_dist = total_distance(neighbor)

            if neighbor_dist < current_dist:
                current = neighbor
                current_dist = neighbor_dist
                improved = True
                break

        if not improved:
            break

    return current, current_dist
```

---

## III. 융합 비교 및 다각도 분석

### 언덕 오르기 변종 비교

| 변종 | 특징 | 장점 | 단점 |
|------|------|------|------|
| **Steepest Ascent** | 최선 이웃 선택 | 수렴 빠름 | 계산 비용 높음 |
| **Stochastic** | 확률적 선택 | 능선 회피 가능 | 느린 수렴 |
| **First-Choice** | 첫 개선 선택 | 계산 효율 | 놓칠 수 있음 |
| **Random-Restart** | 다중 시작 | 전역 최적 가능 | 비용 증가 |
| **Adaptive** | 적응적 이웃 생성 | 효율적 | 구현 복잡 |

### 문제점 및 해결책

| 문제 | 설명 | 해결책 |
|------|------|--------|
| **지역 최적** | 전역 최적이 아닌 봉우리에 갇힘 | Random-Restart, Simulated Annealing |
| **평원** | 모든 이웃이 동일한 가치 | 큰 점프, noise 추가 |
| **능선** | 일련의 지역 최적들 | 확률적 이동, momentum |

### 과목 융합 관점

#### 언덕 오르기 × 머신러닝

- **경사 하강법**: 연속 공간에서의 언덕 오르기
- **Hyperparameter 튜닝**: Grid Search 대신 Hill Climbing
- **Neural Architecture Search**: 구조 탐색에 활용

#### 언덕 오르기 × 최적화

- **Simulated Annealing**: 확률적 하향 이동 허용
- **Tabu Search**: 이전 상태 방문 방지
- **유전 알고리즘**: 집단 기반 탐색

---

## IV. 실무 적용 및 기술사적 판단

### 실무 시나리오

#### 시나리오 1: 작업 스케줄링

**문제**: 작업 순서 최적화 (총 소요 시간 최소화)

**전략**:
1. **상태**: 작업 순서 (순열)
2. **이웃**: 인접 작업 교환
3. **Random-Restart**: 여러 시작점
4. **결과**: 1000개 작업에서 15% 개선

#### 시나리오 2: 네트워크 배치

**문제**: 노드 배치 최적화

**전략**:
1. **상태**: 노드 좌표
2. **이웃**: 좌표 미세 이동
3. **Simulated Annealing** 결합
4. **결과**: 배선 길이 20% 감소

### 안티패턴

1. **이웃 정의 오류**: 너무 좁거나 넓은 이웃
2. **평가 함수 설계**: 지역 최적이 많은 함수
3. **과도한 재시작**: 비효율적인 탐색

---

## V. 기대효과 및 결론

### 장단점 요약

| 장점 | 단점 |
|------|------|
| 구현 간단 | 지역 최적 |
| 메모리 효율 | 완전성 없음 |
| 빠른 근사 | 평원 문제 |
| 실시간 적용 | 이웃 정의 중요 |

### 미래 전망

1. **Hybrid 방식**: 언덕 오르기 + 메타휴리스틱
2. **딥러닝 결합**: 이웃 생성/선택 학습
3. **병렬화**: 다중 시작점 병렬 탐색

---

## 👶 어린이를 위한 3줄 비유

**1. 언덕 오르기는 눈 가리고 산 정상 찾기예요.** 발밑의 경사만 느낄 수 있어서, "이쪽이 더 높아!" 하며 계속 올라가요.

**2. 문제는 작은 봉우리를 정상이라고 착각할 수 있어요.** 진짜 정상은 저기 먼 곳에 있는데, 지금 서 있는 작은 언덕 꼭대기에서는 모든 방향이 아래로 보이거든요.

**3. 그래서 여러 번 다른 곳에서 시작해 보기도 해요.** 이번엔 산 남쪽에서, 저번엔 북쪽에서 시작해서, 가장 높았던 곳을 진짜 정상으로 정해요!
