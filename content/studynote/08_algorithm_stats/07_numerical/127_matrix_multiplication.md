+++
title = "행렬 곱셈 최적화 (Matrix Multiplication Optimization)"
date = 2025-01-01
description = "나이브 O(N³) 행렬 곱셈, Strassen O(N^2.81) 알고리즘, 캐시 친화적 블록 행렬 곱셈, 딥러닝 가속을 다룬다."
categories = "studynote-algorithm"
tags = ["matrix multiplication", "Strassen", "O(N^2.81)", "cache optimization", "block matrix", "GEMM", "cuBLAS", "deep learning"]
+++

## 0. 핵심 인사이트

> **핵심**: 나이브 행렬 곱셈 O(N³)은 Strassen(1969)의 분할정복으로 O(N^2.807)으로 개선됐으나, 실무에서는 캐시 효율을 극대화한 블록 행렬 곱셈(GEMM)이 더 중요하다.
> **비유**: 행렬 곱셈 최적화 (Matrix Multiplication Optimization)은(는) 정확한 값을 직접 구하기 어려울 때 반복 계산으로 점점 정답에 가까워지는 측정 기구와 같다.
> **핵심 인사이트 3줄**
> 2. 딥러닝의 핵심 연산인 행렬 곱셈(matmul)은 GPU의 SIMD 병렬 처리와 Tensor Core(FP16/INT8)를 통해 수천 배 가속된다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```
메모리 접근 패턴:
A[i][k]: 행 방향 접근 → 캐시 친화적 ✓
B[k][j]: 열 방향 접근 → 캐시 미스 빈번 ✗
```

B 행렬을 전치(transpose)하면 j 방향 접근이 행 방향으로 바뀌어 캐시 효율 개선.

📢 **섹션 요약 비유**: 행렬 곱셈에서 B를 열방향으로 읽는 건 책을 한 쪽 건너뛰며 읽는 것 — 캐시가 미리 준비를 못 해 느리다.

---

## 2. 구성요소

- 수치 불안정성 (부동소수점 오류 누적)
- 작은 N에서는 오버헤드로 나이브보다 느림
- 현재 이론적 최선: Williams et al. (2024) O(N^2.371552)

📢 **섹션 요약 비유**: Strassen은 8번 곱할 것을 7번으로 줄인 영리한 요령 — 하지만 중간 계산(덧셈)이 늘어 실제로는 항상 빠르지 않다.

---

## 3. 구조 및 원리

**핵심 조건**: 행렬 곱셈 최적화 (Matrix Multiplication Optimization)은(는) 수렴성, 반올림 오차, 초기값, 반복 횟수, 안정성이 성능보다 먼저 검증되어야 한다.

동작 순서:
1. 해를 직접 구할지 근사로 구할지 결정한다.
2. 반복식이나 분할 기준을 세우고 초기값을 정한다.
3. 오차와 수렴 조건을 확인하며 계산을 진행한다.
4. 허용 오차 이내가 되면 결과를 확정하고 안정성을 검증한다.

```
초기값·오차 기준 설정
        ↓
반복 계산 또는 분할 정복
        ↓
수렴 여부 확인
        ↓
근사해 확정 (행렬 곱셈 최적화 (Matrix Multiplication Optimization))
```

```
L1 캐시: ~32KB, ~4 사이클
L2 캐시: ~256KB, ~12 사이클
L3 캐시: ~8MB, ~40 사이클
메모리:  수 GB, ~100+ 사이클
```

블록 크기 B를 L1/L2 캐시에 맞게 설정:

```python
def matmul_blocked(A, B, block_size=64):
    N = len(A)
    C = [[0]*N for _ in range(N)]
    for ii in range(0, N, block_size):
        for jj in range(0, N, block_size):
            for kk in range(0, N, block_size):
                # 블록 단위 계산 (L1 캐시 내에서)
                for i in range(ii, min(ii+block_size, N)):
                    for j in range(jj, min(jj+block_size, N)):
                        for k in range(kk, min(kk+block_size, N)):
                            C[i][j] += A[i][k] * B[k][j]
    return C
```

📢 **섹션 요약 비유**: 블록 분할은 큰 교재를 챕터(블록)로 나눠 공부하는 것 — 챕터 내용을 한 번에 머릿속(캐시)에 넣어 효율을 높인다.

---

## 4. 비교 및 연결

```python
import numpy as np  # BLAS (OpenBLAS/MKL) 자동 활용
C = np.dot(A, B)  # 또는 A @ B

import torch
C = torch.mm(A_gpu, B_gpu)  # cuBLAS 자동 활용
```

📢 **섹션 요약 비유**: GPU는 수천 명의 계산원 — 큰 행렬의 모든 원소를 동시에 계산해 CPU 한 명이 순서대로 하는 것보다 압도적으로 빠르다.

---

## 5. 실무 적용 및 판단

| 알고리즘          | 복잡도            | 비고                      |
|----------------|-----------------|--------------------------|
| 나이브           | O(N³)           | 기본                     |
| Strassen        | O(N^2.807)      | 실용성 제한              |
| Williams(2024)  | O(N^2.371552)   | 이론적 최선              |
| GPU BLAS        | O(N³/P)         | P개 코어 병렬             |

📢 **섹션 요약 비유**: BLAS GEMM은 수학 계산기 중 최고 성능 — 직접 3중 루프 짜는 것보다 항상 라이브러리를 써라.

---

## 6. 기대효과 및 결론

행렬 곱셈 최적화 (Matrix Multiplication Optimization)은(는) 정확한 닫힌형 해가 어려운 문제를 계산 가능한 근사 문제로 바꾸어 공학 계산을 가능하게 한다. 다만 수렴성, 반올림 오차, 초기값 민감도가 크면 계산 결과가 쉽게 왜곡되므로, 알고리즘의 속도보다 안정성 관리가 우선이다. 앞으로는 병렬 수치해석, 확률적 근사, 자동 미분 기반 최적화와 함께 더 넓게 활용된다.

---

## 7. 발전 흐름도

```
나이브 행렬 곱셈 O(N³)
     │  이론적 개선
     ▼
Strassen O(N^2.807) (1969)
     │  캐시 효율 최적화
     ▼
블록 GEMM + BLAS (1970s~80s)
     │  GPU 병렬화
     ▼
cuBLAS / cuDNN (2007~)
     │  딥러닝 전용 하드웨어
     ▼
Tensor Core FP16/INT8 (2017~)
     │  이론 한계 접근
     ▼
Williams et al. O(N^2.37) (2024)
```

**핵심 키워드**: Strassen, GEMM, BLAS, 블록 행렬, Tensor Core, cuBLAS, AMP, 캐시 최적화

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 수렴성 | 행렬 곱셈 최적화 (Matrix Multiplication Optimization)가 실제 계산에서 유효한지 판단하는 기준 |
| 오차 분석 | 반올림·절단 오차와의 관계 |
| 초기값/조건 | 반복법 성공 여부에 직접 영향 |
| 복잡도 | 정확도 향상 비용과 계산량의 균형 |
| 병렬화 | 대규모 과학 계산에서 성능 확장성 확보 |
