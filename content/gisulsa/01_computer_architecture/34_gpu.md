+++
weight = 34
title = "34. GPU 컴퓨팅"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 GPU 컴퓨팅 & CUDA

> **별점**: ★★★★★ | 기본 필수

## 1. GPU 구조

```
[CPU vs GPU]
CPU: 코어 수십 개, 복잡한 제어 로직, 직렬 최적화
GPU: 코어 수천~만 개, 단순 ALU, 병렬 처리 최적화

[GPU 계층 구조 (NVIDIA)]
SM (Streaming Multiprocessor):
  여러 CUDA 코어 묶음 (warp 단위 실행)
  공유 메모리 (L1 캐시 역할)

Warp:
  32개 스레드 묶음 = SIMD 실행 단위
  같은 명령어를 32개 스레드가 동시 실행

VRAM (HBM3e/GDDR6X):
  GPU 전용 고대역폭 메모리
  A100: 80GB HBM2e / H100: 80GB HBM3
```

## 2. CUDA 프로그래밍 모델

```
[CUDA 스레드 계층]
Grid → Block → Thread
Grid: 전체 문제 공간
Block: 공유 메모리 공유 단위 (max 1024 스레드)
Thread: 최소 실행 단위

[CUDA 메모리 계층]
전역 메모리(Global): 느림, GPU 전체 공유
공유 메모리(Shared): 빠름, Block 내 공유
레지스터: 최빠름, Thread 전용
상수 메모리(Constant): 읽기 전용, 캐시됨

[CUDA 코드 예시 개념]
kernel<<<numBlocks, threadsPerBlock>>>(...)
CPU → GPU 메모리 복사 → 커널 실행 → 결과 복사
```

## 3. GPGPU & AI 가속

```
GPGPU: GPU를 범용 병렬 컴퓨팅에 활용

[AI 학습 병목 해결]
행렬 곱 (GeMM): 딥러닝 핵심 연산
  A×B = C: 병렬화 완벽 적합
Tensor Core: NVIDIA, 행렬 연산 전용 유닛
  FP8/INT8 지원 → AI 추론 최적화

[CUDA 에코시스템]
cuDNN: 딥러닝 연산 라이브러리
cuBLAS: 선형대수 라이브러리
NCCL: 멀티GPU 통신
NVIDID NVLink: GPU 간 고속 인터커넥트
```

## 4. 답안 포인트

**3단락**: ① CPU vs GPU 구조 차이 & Warp → ② CUDA 스레드 계층 & 메모리 모델 → ③ Tensor Core & AI 학습 가속

## 5. 관련 개념

`NPU(★134회, 37번)` → GPU와 보완 관계 | `HBM(18번)` → GPU용 고대역폭 메모리 | `암달의 법칙(07번)` → GPU 병렬화 한계
