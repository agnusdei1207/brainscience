+++
weight = 19
title = "19. CXL (Compute Express Link)"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
exam = "☆ 2026~2027 출제 예측"
+++

# 🎯 핵심 키워드: CXL (Compute Express Link), 메모리 풀링, 캐시 일관성, PCIe 5.0

> **출제 빈도**: ★★★★★ | **난이도**: ★★★★☆ | **예측**: ☆2026 확실 예측 (HPC+AI 인프라 핵심)

## 1. 정의

CXL(Compute Express Link)은 Intel이 주도하고 AMD, ARM, 삼성 등이 참여한 **PCIe 기반 개방형 캐시 일관성 인터커넥트 표준**으로, CPU와 GPU/가속기/메모리를 낮은 지연으로 연결하고 메모리 풀링(Memory Pooling)을 가능하게 한다.

CXL 2.0부터 메모리 풀링, CXL 3.0부터 멀티 호스트 공유 메모리를 지원한다.

## 2. 출제 포인트

| 포인트 | 내용 | 채점 비중 |
|--------|------|----------|
| 정의 | CXL 표준, PCIe 기반, 캐시 일관성 | 20% |
| Type 분류 | Type 1(가속기), Type 2(메모리+가속기), Type 3(메모리) | 35% |
| 메모리 풀링 | 물리 메모리 분리, 유연한 할당 | 25% |
| AI 인프라 | LLM 서빙, GPU 메모리 확장 | 20% |

## 3. 답안 목차 템플릿

**문제**: "CXL(Compute Express Link)의 개념과 메모리 풀링 메커니즘, AI 인프라 적용을 설명하시오."

```
I. CXL 정의 및 등장 배경
   - 기존 PCIe: 단방향, 캐시 일관성 미지원
   - CXL: PCIe 5.0 물리 계층 기반, 3개 프로토콜 계층
     * CXL.io   : PCIe 호환 I/O
     * CXL.cache: 가속기가 호스트 메모리 캐시
     * CXL.mem  : 호스트가 가속기 메모리 접근

II. CXL 디바이스 Type 분류
   | Type   | 구성              | 예시                    |
   |--------|------------------|------------------------|
   | Type 1 | 가속기 (캐시만)   | SmartNIC, DPU          |
   | Type 2 | 가속기 + 메모리   | GPU, AI 가속기          |
   | Type 3 | 메모리 전용       | CXL DRAM, Persistent M |

III. 메모리 풀링 (CXL 2.0+)
   
   [기존]                    [CXL 메모리 풀링]
   서버1: 256GB RAM          ┌─────────────────┐
   서버2: 256GB RAM          │  메모리 풀 (2TB) │
   (사용률 낮아도 공유 불가) │  CXL Fabric     │
                             └────┬──────┬─────┘
                             서버1│      │서버2
                             (필요│시 동적│할당)
   
   효과: 메모리 이용률 향상, LLM 서빙 용량 확장

IV. AI 인프라에서 CXL 적용
   - LLM 추론: 수백GB 모델 가중치 → CXL 메모리 풀에서 동적 로드
   - GPU 메모리 확장: GPU VRAM(80GB) + CXL DRAM(수TB)
   - 멀티 GPU: CXL Fabric으로 GPU 간 메모리 공유
   - 향후: CXL 3.0 멀티 호스트 → AI 클러스터 메모리 통합
```

## 4. 핵심 암기 포인트

- **CXL = PCIe 5.0 위에 캐시 일관성 추가**
- **Type 3**: 순수 메모리 확장 → LLM 시대 핵심
- **메모리 풀링**: 물리 메모리를 서버 간 동적 공유

## 5. 관련 개념 연결

| 개념 | 연결 포인트 |
|------|------------|
| HBM | CXL로 연결되는 AI 가속기용 메모리 |
| PNM (★131회) | CXL 메모리에서의 근메모리 연산 |
| 칩렛 (★131회) | CXL 인터커넥트로 칩렛 간 연결 |
| NPU (★134회) | CXL Type 2로 CPU와 연결 |
| 메모리 계층 구조 | CXL이 추가하는 새로운 계층 |
