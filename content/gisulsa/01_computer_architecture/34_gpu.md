+++
weight = 34
title = "34. GPU 컴퓨팅"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# GPU 컴퓨팅 & CUDA

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

CPU: 코어 수십 개, 복잡한 제어 로직, 직렬 최적화
GPU: 코어 수천~만 개, 단순 ALU, 병렬 처리 최적화
SM (Streaming Multiprocessor):

### Ⅱ. 핵심 구성요소

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


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
