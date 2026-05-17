+++
weight = 19
title = "19. CXL (Compute Express Link)"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# CXL (Compute Express Link), 메모리 풀링, 캐시 일관성, PCIe 5.0

> 출제 빈도: ★★★★★ | 난이도: ★★★★☆ | 예측: ☆2026 확실 예측 (HPC+AI 인프라 핵심)

---

## 답안.

### Ⅰ. 개요

CXL(Compute Express Link)은 Intel이 주도하고 AMD, ARM, 삼성 등이 참여한 **PCIe 기반 개방형 캐시 일관성 인터커넥트 표준**으로, CPU와 GPU/가속기/메모리를 낮은 지연으로 연결하고 메모리 풀링(Memory Pooling)을 가능하게 한다.
CXL 2.0부터 메모리 풀링, CXL 3.0부터 멀티 호스트 공유 메모리를 지원한다.

### Ⅱ. 핵심 구성요소

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


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
