+++
weight = 7
title = "07. 암달의 법칙 & 구스타프손"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 암달의 법칙 & 구스타프손의 법칙

> **별점**: ★★★★★ | 기본 필수

## 1. 암달의 법칙 (Amdahl's Law)

```
정의: 병렬화로 얻을 수 있는 성능 향상의 이론적 한계

[공식]
Speedup = 1 / (S + (1-S)/N)

S: 직렬화 비율 (병렬화 불가 부분)
(1-S): 병렬화 가능 비율
N: 프로세서 수

[예시]
병렬화 가능 비율 = 90% (S = 0.1)
N = 10: Speedup = 1/(0.1+0.9/10) = 5.26배
N = 100: Speedup = 1/(0.1+0.9/100) = 9.17배
N = ∞: Speedup 최대 = 1/S = 10배

→ 결론: 직렬 부분 10%만 있어도 최대 10배 한계
```

## 2. 구스타프손의 법칙 (Gustafson's Law)

```
암달의 법칙 비판: 문제 크기를 고정으로 가정

구스타프손: 프로세서 증가 → 문제 크기도 증가

Speedup = N - S(N-1)

예: S=0.1, N=100
  Speedup = 100 - 0.1×99 = 100 - 9.9 = 90.1배

현실적 관점:
  더 큰 데이터셋을 처리 = 실용적 스케일업
  빅데이터, HPC, AI 학습에 적합
```

## 3. 성능 측정 지표

```
[FLOPS]
Floating Point Operations Per Second
TFLOPS (10^12), PETAFLOPS (10^15)
AI 학습: H100 = 2000 TFLOPS (FP8)

[tpmC (Transaction per Minute)]
국내 HW 규모 산정 기준 (조달청)
1회 기출: ★135회
벤치마크: TPC-C 기준 트랜잭션/분

[IPC vs 클록속도]
IPC (Instruction Per Cycle) × 클록 = 성능
현대 CPU: 클록 증가보다 IPC·코어 수 증가 전략
```

## 4. 답안 포인트

**3단락**: ① 암달의 법칙 공식 & 한계점 → ② 구스타프손의 법칙과 차이 → ③ FLOPS/tpmC 성능 지표 & AI 가속기 적용

## 5. 관련 개념

`폴락의 법칙(★132회)` → 성능 ∝ √복잡도 | `GPU(34번)` → FLOPS 극대화 | `HW 규모산정(★135회)` → tpmC 기반 서버 산정
