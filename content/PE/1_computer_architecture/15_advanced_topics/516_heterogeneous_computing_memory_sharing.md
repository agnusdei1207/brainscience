+++
title = "516. 이종 컴퓨팅 메모리 공유"
date = "2026-03-05"
[extra]
categories = "studynotes-computer-architecture"
+++

# 이종 컴퓨팅 메모리 공유 (Heterogeneous Computing Memory Sharing)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CPU, GPU, NPU 등 서로 다른 아키텍처를 가진 프로세서들이 단일 주소 공간을 공유하거나 물리적 메모리를 효율적으로 공동 활용하는 기술로, 데이터 복사 오버헤드 제거가 핵심이다.
> 2. **가치**: 불필요한 PCIe 데이터 전송(Copy-and-Sync)을 제거하여 지연 시간을 50-80% 단축하고, 프로그래밍 모델을 단순화하여 개발 생산성을 비약적으로 향상시킨다.
> 3. **융합**: 고대역폭 메모리(HBM), CXL(Compute Express Link), 가상 메모리 관리(SVM), 캐시 일관성 프로토콜과 밀접하게 연합된다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
이종 컴퓨팅 메모리 공유는 시스템 내의 이종 가속기(GPU, FPGA, NPU 등)가 호스트 CPU의 메인 메모리에 직접 접근하거나, CPU와 가속기가 동일한 가상 주소 공간을 공유하여 데이터를 주고받는 아키텍처 기술이다. 과거의 분리된 메모리 구조(Discrete Memory)에서 발생하는 데이터 복사 병목을 해결하기 위한 필수 기술이다.

### 💡 비유
이종 컴퓨팅 메모리 공유는 "주방(CPU)과 홀(GPU) 사이의 벽을 허문 오픈 키친"과 같다. 예전에는 요리사가 음식을 만들어 창구(PCIe)를 통해 전달하고 서빙 직원이 이를 다시 받아가야 했지만(Data Copy), 오픈 키친에서는 요리사와 서빙 직원이 동일한 조리대(공유 메모리)를 함께 사용하여 훨씬 빠르고 효율적으로 협업할 수 있다.

### 등장 배경 및 발전 과정

#### 1. 기존 기술의 치명적 한계점
- **PCIe 데이터 전송 병목**: CPU와 가속기 간 데이터 복사(Host-to-Device)가 연산 자체보다 더 오래 걸리는 현상.
- **프로그래밍 복잡성**: 프로그래머가 명시적으로 `cudaMemcpy` 등을 호출하여 메모리 상태를 관리해야 함.
- **메모리 단편화**: CPU와 GPU가 각자 전용 메모리를 가져 시스템 전체 자원 활용도가 떨어짐.

#### 2. 패러다임 변화의 역사
- **Discrete Phase**: CPU 메모리와 GPU 메모리가 물리적/논리적으로 완전히 분리됨.
- **UVA (Unified Virtual Addressing) Phase**: 주소 공간만 논리적으로 통합, 데이터 복사는 여전히 존재.
- **HSA (Heterogeneous System Architecture) Phase**: 하드웨어 수준의 캐시 일관성과 공유 가상 메모리(SVM) 지원.
- **CXL/HBM Phase**: 고대역폭 인터커넥트(CXL)를 통한 메모리 풀링 및 확장성 확보.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|--------|----------|-------------------|-----------|------|
| **SVM (Shared Virtual Memory)** | CPU/가속기 간 주소 공간 통합 | 동일한 포인터로 양쪽에서 데이터 접근 | CUDA Unified Memory | 한글 성함 |
| **IOMMU (I/O MMU)** | 가속기의 가상 주소를 물리 주소로 변환 | 페이지 테이블 공유 및 주소 번역 수행 | VT-d, SMMU | 통번역사 |
| **ATS (Address Translation Services)** | 가속기가 직접 주소 번역을 요청 | 가속기 내부에 TLB(Address Cache) 구현 | PCIe ATS | 지름길 |
| **HMM (Heterogeneous Memory Management)** | OS 커널 수준의 메모리 통합 관리 | CPU 페이지 테이블과 가속기 페이지 테이블 동기화 | Linux HMM | 총괄 지배인 |
| **Cache Coherency Link** | 장치 간 캐시 데이터 일관성 유지 | 스누핑 또는 디렉터리 기반 프로토콜 연동 | CXL.cache, NVLink | 정보 공유방 |

### 정교한 구조 다이어그램 (ASCII Art)

```
        ┌─────────────────────────────────────────────────────────────┐
        │                 통합 가상 주소 공간 (Unified Virtual Address Space)      │
        └──────────────────────────────┬──────────────────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                │             가상 메모리 관리 (SVM / HMM)             │
                └──────┬───────────────────────────────┬──────┘
                       │                               │
        ┌──────────────▼──────────────┐        ┌───────▼─────────────────────┐
        │        Host CPU (CISC)      │        │      Accelerator (SIMT)     │
        │  ┌───────┐   ┌───────────┐  │        │  ┌──────────┐   ┌─────────┐ │
        │  │  L1   │   │ Page Table│  │        │  │ GPU Cache│   │ ATS/PRI │ │
        │  └───────┘   └─────┬─────┘  │        │  └──────────┘   └────┬────┘ │
        └──────┬─────────────┼────────┘        └────────┬─────────────┼──────┘
               │             │                          │             │
  ═════════════╪═════════════╪══════════════════════════╪═════════════╪══════════════
               │             │  Interconnect (CXL/NVLink)  │             │
  ═════════════╪═════════════╪══════════════════════════╪═════════════╪══════════════
               │             │                          │             │
        ┌──────▼─────────────▼──────────────────────────▼─────────────▼──────┐
        │                    공유 물리 메모리 (System RAM / HBM)               │
        │  ┌───────────────────────────────────────────────────────────────┐  │
        │  │ [ Shared Buffer A ]  [ Shared Buffer B ]  [ OS Protected Area ] │  │
        │  └───────────────────────────────────────────────────────────────┘  │
        └────────────────────────────────────────────────────────────────────┘

 [동작 시나리오: Zero-Copy Data Access]
 1. CPU가 Shared Buffer A에 데이터 작성 (가상 주소 0x1000)
 2. GPU에 "데이터 준비됨(0x1000)" 신호 전송 (데이터 복사 없음)
 3. GPU가 0x1000 접근 시 ATS를 통해 물리 주소 획득
 4. GPU가 시스템 RAM에서 직접 데이터 읽어 연산 수행
```

### 심층 동작 원리 (Step-by-Step)

#### ① 주소 공간의 통합 (Unified Addressing)
프로그래머는 `malloc` 또는 전용 `Unified Memory Allocator`를 사용하여 메모리를 할당받는다. 이 주소는 CPU와 가속기 양쪽에서 동일하게 유효하다. 이를 위해 하드웨어는 가상 주소 공간의 일부를 가속기가 직접 제어할 수 있도록 예약하거나, IOMMU를 통해 페이지 테이블을 공유한다.

#### ② 온디맨드 페이지 폴팅 (On-demand Page Faulting)
가속기가 아직 물리 메모리에 로드되지 않은 가상 주소에 접근하면, 가속기 내부의 `PRI (Page Request Interface)`가 CPU에 페이지 폴트를 알린다. 호스트 OS는 페이지를 메모리에 로드하고 가속기의 페이지 테이블을 갱신한 후 연산을 재개시킨다. 이는 `Zero-copy` 전송의 핵심이다.

#### ③ 데이터 마이그레이션 전략 (Hardware Managed)
하드웨어(예: NVIDIA Pascal 아키텍처 이후)는 접근 빈도에 따라 데이터를 CPU 메모리와 GPU 메모리(HBM) 사이에서 자동으로 이동시킨다. 자주 쓰이는 데이터는 고대역폭의 가속기 메모리로 옮기고, 드물게 쓰이는 데이터는 호스트 메모리에 둔다.

### 핵심 알고리즘 & 실무 코드 예시

#### CUDA Unified Memory (C++)
```cpp
#include <iostream>
#include <cuda_runtime.h>

// GPU 연산 커널
__global__ void add(int n, float *x, float *y) {
  int index = blockIdx.x * blockDim.x + threadIdx.x;
  int stride = blockDim.x * gridDim.x;
  for (int i = index; i < n; i += stride)
      y[i] = x[i] + y[i];
}

int main(void) {
  int N = 1<<20;
  float *x, *y;

  // [핵심] Unified Memory 할당 - CPU/GPU 모두에서 접근 가능
  cudaMallocManaged(&x, N*sizeof(float));
  cudaMallocManaged(&y, N*sizeof(float));

  // CPU에서 초기화 (별도의 Memcpy 필요 없음)
  for (int i = 0; i < N; i++) {
    x[i] = 1.0f;
    y[i] = 2.0f;
  }

  // GPU에서 실행
  int blockSize = 256;
  int numBlocks = (N + blockSize - 1) / blockSize;
  add<<<numBlocks, blockSize>>>(N, x, y);

  // CPU에서 결과 대기 및 확인 (동기화)
  cudaDeviceSynchronize();

  float maxError = 0.0f;
  for (int i = 0; i < N; i++)
    maxError = fmax(maxError, fabs(y[i]-3.0f));
  std::cout << "Max error: " << maxError << std::endl;

  // 메모리 해제
  cudaFree(x);
  cudaFree(y);
  
  return 0;
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 기술 아키텍처 비교

| 비교 항목 | Discrete (기존) | Unified (UVA) | Shared (HSA/CXL) |
|-----------|-----------------|---------------|-------------------|
| **데이터 전송** | 명시적 복사 (PCIe) | 논리적 통합, 물리적 복사 | 하드웨어 자동 마이그레이션 |
| **일관성 관리** | 프로그래머 책임 | 프로그래머 책임 | 하드웨어 캐시 일관성 |
| **지연 시간** | 높음 (PCIe Latency) | 중간 | 매우 낮음 |
| **복잡도** | 매우 높음 | 중간 | 낮음 (자동화) |
| **대표 기술** | CUDA (Early) | CUDA Managed Memory | AMD hUMA, CXL 2.0/3.0 |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**상황**: 초거대 AI 모델(LLM) 추론 시스템을 구축 중이나, 모델 가중치가 GPU 메모리(80GB)를 초과하는 150GB 규모임.
**판단**:
1. **단기적**: `Managed Memory`와 `OOM (Out of Memory)` 방지 기능을 활성화하여 호스트 메모리를 스왑 공간으로 활용.
2. **중장기적**: `CXL 1.1/2.0` 기반의 메모리 확장 카드를 도입하여 CPU와 가속기가 공유하는 메모리 풀(Pool)을 구성. 이를 통해 PCIe 병목을 최소화하면서 대규모 모델을 로드함.

### 주의사항 및 안티패턴 (Anti-patterns)
- **Thrashing**: CPU와 GPU가 동일한 페이지를 빈번하게 번갈아 쓰면 데이터가 버스를 타고 왕복(Ping-pong)하느라 성능이 급락함.
- **Granularity 문제**: OS 페이지 단위(4KB~2MB)로 이동하기 때문에 아주 작은 데이터 하나 때문에 큰 페이지를 옮기는 오버헤드가 발생할 수 있음.

---

## Ⅴ. 기대효과 및 결론

### 정량적/정성적 기대효과
- **성능**: 데이터 이동 병목 제거로 복잡한 알고리즘에서 최대 2-3배 성능 향상.
- **생산성**: 복잡한 메모리 관리 코드 약 30-50% 감소.
- **유연성**: 가속기 메모리 용량 한계를 초과하는 대규모 데이터 처리 가능.

### 미래 전망 및 진화 방향
향후 **CXL 3.0**이 보편화되면 개별 서버 단위를 넘어 데이터센터 규모의 **메모리 패브릭(Memory Fabric)**이 형성될 것이며, 이종 컴퓨팅 장치들은 어디에 있는 메모리든 자신의 로컬 메모리처럼 자유롭게 공유하며 연산하는 "Composable Infrastructure"로 진화할 것이다.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [HBM (High Bandwidth Memory)](./495_hbm.md) - 공유 메모리의 성능을 뒷받침하는 기술
- [IOMMU / SMMU](../7_virtual_memory/3_memory_management_unit.md) - 주소 번역의 핵심
- [CXL (Compute Express Link)](./25_compute_express_link.md) - 차세대 공유 인터커넥트
- [Cache Coherency](../11_synchronization/402_cache_coherence.md) - 데이터 일관성 보장 원리

---

## 👶 어린이를 위한 3줄 비유 설명
1. **이종 컴퓨팅 메모리 공유란?**: 요리사(CPU)와 보조 요리사(GPU)가 각자 자기 냉장고를 쓰는 게 아니라, 커다란 공용 냉장고를 같이 쓰는 거예요.
2. **어떻게 도와주나요?**: 보조 요리사가 재료를 가지러 멀리 있는 요리사 냉장고까지 달려갈 필요 없이, 바로 옆 공용 냉장고에서 꺼내 쓰면 되니까 요리가 빨라져요.
3. **왜 좋은가요?**: 요리 시간이 짧아지고, 주방이 훨씬 덜 복잡해져서 맛있는 음식을 더 많이 만들 수 있어요!
