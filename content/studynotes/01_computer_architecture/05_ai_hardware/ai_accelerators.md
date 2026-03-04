+++
title = "AI Accelerators (GPGPU, NPU, TPU, Systolic Array)"
date = 2024-05-24
updated = 2024-05-20
description = "AI 연산 최적화를 위한 차세대 하드웨어 가속기 아키텍처 심층 분석: GPGPU에서 NPU까지"
[taxonomies]
tags = ["Computer Architecture", "AI Hardware", "Deep Learning", "Acceleration"]
categories = ["studynotes-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: AI 가속기는 심층 신경망(DNN)의 핵심 연산인 대규모 행렬 곱셈(Matrix Multiplication)과 벡터 연산을 병렬적으로 처리하기 위해 고안된 특수 목적 하드웨어로, 제어 로직을 최소화하고 산술 연산 장치(ALU)를 극대화한 아키텍처를 가집니다.
> 2. **가치**: 범용 CPU 대비 수백 배 이상의 연산 처리량(Throughput)과 수십 배 높은 전력 효율(Energy Efficiency)을 제공하여, LLM(Large Language Model) 학습 및 실시간 추론 서비스의 인프라적 한계를 극복합니다.
> 3. **융합**: 고성능 메모리(HBM), 고속 인터커넥트(NVLink), 소프트웨어 스택(CUDA, ONNX)과 결합하여 데이터 센터부터 온디바이스(On-device)까지 AI 생태계의 물리적 근간을 형성하며, 향후 PIM(Processor-In-Memory) 및 뉴로모픽 칩으로 진화하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)
AI 가속기는 인공지능 알고리즘, 특히 딥러닝 연산에 최적화된 하드웨어 시스템을 의미합니다. 전통적인 폰 노이만 구조(Von Neumann Architecture) 기반의 CPU가 복잡한 분기 예측(Branch Prediction)과 범용적인 제어 로직에 집중하는 반면, AI 가속기는 단순 반복적인 산술 연산을 동시에 처리하는 병렬성에 모든 자원을 투입합니다.

**💡 비유**: CPU가 복잡한 수학 문제부터 문학적 분석까지 모두 해내는 '한 명의 천재 교수'라면, AI 가속기는 오직 구구단만 엄청나게 빠른 속도로 계산해내는 '수천 명의 초등학생 부대'와 같습니다.

**등장 배경 및 발전 과정**:
1. **CPU의 한계 (Memory Wall & Power Wall)**: 딥러닝의 폭발적 성장에 따라 수십억 개의 파라미터를 처리해야 했으나, CPU는 메모리와 연산기 사이의 데이터 이동 병목(Memory Wall)과 높은 전력 소모(Power Wall)로 인해 기하급수적으로 늘어나는 연산량을 감당하지 못했습니다.
2. **GPGPU의 태동**: 초기에는 그래픽 처리를 위해 설계된 GPU를 연산에 활용하는 GPGPU(General Purpose GPU) 방식이 주를 이루었으나, 점차 AI만을 위해 설계된 전용 ASIC(NPU, TPU)으로 시장이 분화되었습니다.
3. **비즈니스적 요구**: ChatGPT와 같은 초거대 모델의 등장으로 인해 학습 비용 절감과 추론 지연 시간(Latency) 최소화가 기업의 핵심 경쟁력이 되면서 하드웨어 가속기 도입은 선택이 아닌 필수가 되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
AI 가속기의 성능은 얼마나 효율적으로 데이터를 연산 유닛에 공급하고, 공급된 데이터를 재사용(Data Reuse)하느냐에 달려 있습니다.

**구성 요소 (표)**:

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **PE (Processing Element)** | 최소 연산 단위 | 곱셈-누산(MAC) 연산을 수행하는 핵심 로직 | FP16/INT8 Arithmetic | 펜을 든 학생 |
| **Local Buffer (SRAM)** | 데이터 임시 저장 | PE 근처에 위치하여 메모리 접근 지연 시간 최소화 | Register File, Scratchpad | 책상 위 공책 |
| **Interconnect** | 데이터 전송로 | PE 간 또는 PE와 메모리 간의 고속 통신 통로 | Mesh/Ring Topology | 복도의 컨베이어 벨트 |
| **Control Unit** | 연산 흐름 제어 | 데이터의 흐름과 연산 순서를 스케줄링 | Microcode, ISA | 조장/감독관 |
| **HBM (High Bandwidth Memory)** | 고대역폭 주메모리 | 적층형 메모리를 통해 대규모 파라미터를 고속 공급 | TSV(Through Silicon Via) | 거대 도서관 |

**정교한 구조 다이어그램 (Systolic Array 기반 TPU 아키텍처)**:

```ascii
       [ Main Memory / HBM ]
                |
                v (High Bandwidth Interface)
        +-------+-------+-------------------------+
        |  Unified Buffer (SRAM) - Weights/Activations|
        +-------+-------+-------------------------+
                |           |           |
        +-------v-------+---v-----------v---------+
        |  Weight FIFO  |  Input / Activation FIFO |
        +-------+-------+-----------+-------------+
                |                   |
    [ Systolic Array (256x256 Matrix Multiply Unit) ]
    +-------+       +-------+       +-------+
    | PE    |<------| PE    |<------| PE    |<---- (Input Data)
    | [W|A] |       | [W|A] |       | [W|A] |
    +---+---+       +---+---+       +---+---+
        |               |               |
        v               v               v
    +---+---+       +---+---+       +---+---+
    | PE    |<------| PE    |<------| PE    |
    | [W|A] |       | [W|A] |       | [W|A] |
    +---+---+       +---+---+       +---+---+
        |               |               |
        v               v               v
    [ Accumulators / Activation Function (ReLU) ]
                |
                v
        [ Output Result Queue / DMA ]
```

**심층 동작 원리 - Systolic Array (시스톨릭 어레이)**:
1. **Data Pumping**: 데이터가 심장(Systole)처럼 일정한 박자에 맞춰 인접한 연산 유닛(PE)으로 흘러갑니다.
2. **Weight Stationary / Output Stationary**: 가중치(Weight)를 PE에 고정시켜 두거나, 결과값(Accumulation)을 고정하여 불필요한 메모리 접근을 줄입니다.
3. **Data Reuse Maximize**: 한 번 메모리에서 읽어온 데이터가 여러 PE를 거치며 수백 번 재사용되도록 설계되어, 메모리 대역폭의 한계를 극복합니다.
4. **Pipeline Processing**: 모든 PE가 동시에 다른 데이터를 처리하는 파이프라인 방식을 통해 병렬성을 극대화합니다.

**핵심 알고리즘: Matrix Multiplication (GEMM)**:
딥러닝의 90% 이상은 `C = A * B + C` 형태의 행렬 연산입니다. 이를 하드웨어에서 효율적으로 처리하기 위해 'Loop Unrolling'과 'Tiling' 기법을 사용합니다.

```python
# 실무 수준의 연산 최적화 의사코드 (Tiling 기법)
def tiled_matrix_multiply(A, B, tile_size):
    for i in range(0, N, tile_size):
        for j in range(0, M, tile_size):
            # Tile을 로컬 SRAM(Scratchpad Memory)으로 로드
            tile_A = load_to_sram(A[i:i+tile_size, :])
            tile_B = load_to_sram(B[:, j:j+tile_size])
            
            # SRAM 내에서의 고속 연산 (MAC 유닛 활용)
            for k in range(0, K, tile_size):
                compute_mac(tile_A, tile_B, C[i:i+tile_size, j:j+tile_size])
```

---

### Ⅲ. 융합 비교 및 다각도 분석
주요 AI 가속기 형태별 비교 분석입니다.

| 비교 항목 | GPGPU (NVIDIA) | NPU (Mobile/Edge) | TPU (Google) | FPGA / ASIC |
| :--- | :--- | :--- | :--- | :--- |
| **유연성 (Flexibility)** | 매우 높음 (CUDA) | 중간 (특정 모델 최적화) | 낮음 (TensorFlow/JAX) | 매우 낮음/극도로 높음 |
| **전력 효율 (W/Perf)** | 낮음 (범용 로직 오버헤드) | 매우 높음 | 높음 | 매우 높음 |
| **핵심 기술** | Tensor Core | Mobile Neural Engine | Systolic Array | Reconfigurable Logic |
| **지연 시간 (Latency)** | 중간 | 매우 낮음 | 낮음 | 매우 낮음 |
| **주요 용도** | 대규모 모델 학습 | 스마트폰 온디바이스 AI | 클라우드 서비스 추론 | 실시간 하드웨어 제어 |

---

### Ⅳ. 실무 적용 및 기술사적 판단
AI 가속기 도입 시의 전략적 고려사항입니다.

**기술사적 판단 (실무 시나리오)**:
*   **시나리오 1: LLM 서비스 상용화**: 수조 개의 파라미터를 가진 모델을 서빙할 때, 단일 GPU로는 메모리 부족(OOM)이 발생합니다. 이때 **HBM3 기반의 GPU 클러스터링**과 **Model Parallelism**을 지원하는 하드웨어-소프트웨어 통합 아키텍처를 선택해야 합니다.
*   **시나리오 2: 온디바이스 AI 비전 서비스**: 스마트 미러나 자율주행 드론과 같은 환경에서는 전력 소모와 열 발생이 치명적입니다. 이때는 **Low-precision (INT8/INT4) 양자화**를 하드웨어 수준에서 지원하는 NPU를 선정하여 전력 효율을 극대화해야 합니다.

**도입 시 고려사항**:
1. **Precision (정밀도)**: FP32(범용) -> FP16(학습) -> INT8(추론)로 갈수록 속도는 빨라지나 정확도는 낮아집니다. 서비스 특성에 맞는 정밀도 지원 여부를 확인해야 합니다.
2. **Software Stack (Ecosystem)**: 하드웨어가 아무리 좋아도 CUDA나 TVM, ONNX와 같은 소프트웨어 생태계가 받쳐주지 않으면 개발 생산성이 급격히 저하됩니다.
3. **Bandwidth (대역폭)**: 연산 속도(FLOPS)보다 데이터 공급 속도(Bandwidth)가 병목인 경우가 많으므로, PCIe 버전이나 NVLink 탑재 여부를 체크해야 합니다.

---

### Ⅴ. 기대효과 및 결론
AI 가속기는 더 이상 보조 프로세서가 아닌, 데이터 센터의 주인공으로 자리 잡았습니다.

**정량적 기대효과**:
- **학습 시간 단축**: CPU 기반 수주 걸리던 학습을 수 시간 내로 단축 (최대 100배 이상).
- **TCO (Total Cost of Ownership) 절감**: 동일 성능 대비 전력 소모를 1/10 수준으로 감소시켜 운영 비용 절감.

**미래 전망**:
1. **PIM (Processor-In-Memory)**: 메모리 내부에 연산기를 통합하여 데이터 이동을 완전히 제거하는 기술이 상용화될 것입니다.
2. **Neuromorphic Computing**: 인간의 뇌 구조를 모방하여 극저전력으로 상시 추론이 가능한 하드웨어가 IoT 분야를 혁신할 것입니다.

---

### 📌 관련 개념 맵
- [CPU Pipeline](@/studynotes/01_computer_architecture/01_cpu_architecture/cpu_pipeline.md): 병렬 처리를 위한 하드웨어의 기초 설계 방식.
- [Memory Hierarchy](@/studynotes/01_computer_architecture/02_memory_hierarchy/cache_memory.md): 가속기 성능의 핵심인 HBM과 SRAM의 계층 구조 이해.
- [Quantization (양자화)](@/studynotes/10_ai/01_deep_learning/_index.md): 가속기 효율을 극대화하기 위한 모델 압축 기술.
- [Distributed Computing](@/studynotes/16_bigdata/02_distributed_computing/_index.md): 수만 개의 가속기를 연결하기 위한 클러스터링 기술.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **무엇인가요?**: 엄청나게 많은 계산 문제를 한꺼번에 푸는 아주 빠른 '수학 전용 계산기'예요.
2. **어떻게 하나요?**: 수천 명의 아이들이 손을 잡고 옆 사람에게 연필과 종이를 넘기며 다 같이 한 번에 문제를 풀어요.
3. **왜 좋은가요?**: 사람이 100년 걸릴 어려운 인공지능 공부를 이 기계는 하루 만에 끝낼 수 있게 도와줘요.
