+++
weight = 173
title = "173. 텐서 코어 (Tensor Core) HBM GPU 최적화 - 혼합 정밀도 학습 FP16/FP32"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++
## 0. 핵심 인사이트

> **핵심**: Tensor Core는 NVIDIA GPU의 행렬 곱셈 전용 하드웨어로, FP16/BF16 연산을 FP32 대비 최대 16배 빠르게 수행하여 딥러닝 학습의 병목을 해소한다.
> 2. **가치**: 혼합 정밀도 학습(Mixed Precision Training)은 FP16의 속도 이점을 취하면서 FP32 마스터 가중치로 수치 안정성을 보장하여, 메모리 절반·속도 2~4배를 달성한다.
> 3. **판단 포인트**: H100 vs A100 선택 시 Tensor Core TFlops와 HBM (High Bandwidth Memory) 대역폭을 함께 평가해야 하며, 트랜스포머 학습에는 BF16이 FP16보다 수치 안정성이 높아 선호된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 1.1 딥러닝 연산의 특성

딥러닝의 핵심 연산은 거대한 행렬 곱셈(GEMM, General Matrix Multiply)이다.

```
트랜스포머 Self-Attention 핵심 연산:
  Q, K, V = X × W_Q, X × W_K, X × W_V    (행렬 곱)
  Attention = softmax(QK^T / √d_k) × V    (행렬 곱)
  
  [seq=2048, d=4096] × [d=4096, d=4096]
  = 약 34.4 GFLOP (단일 레이어, 단일 배치)
  
  GPT-3 (96 레이어):  약 3.1 TFLOP/토큰
  → FP32: 수일, FP16: 수시간 (Tensor Core 활용 시)
```

### 1.2 GPU 컴퓨팅 아키텍처 진화

| 세대 | GPU | Tensor Core 세대 | FP16 TFlops | 메모리 |
|:---|:---|:---|:---|:---|
| Volta | V100 | 1세대 | 112 TFlops | HBM2 32GB |
| Turing | T4 | 2세대 | 65 TFlops | GDDR6 16GB |
| Ampere | A100 | 3세대 | 312 TFlops | HBM2e 80GB |
| Hopper | H100 | 4세대 | 989 TFlops | HBM3 80GB |
| Blackwell | B200 | 5세대 | 4,500 TFlops | HBM3e 192GB |

📢 **섹션 요약 비유**: Tensor Core는 일반 계산기가 아닌 행렬 계산 전용 슈퍼 계산기다. 일반 연산은 일반 직원이 처리하고, 행렬 곱셈은 전용 팀(Tensor Core)이 훨씬 빠르게 처리한다.

---

## 2. 구성요소

### 2.1 Tensor Core 구조

```
┌─────────────────────────────────────────────────────────┐
│           NVIDIA A100 Tensor Core (3세대)                │
│                                                          │
│  단일 클럭 사이클에 4×4 행렬 곱 누산 수행:               │
│  D = A × B + C                                          │
│                                                          │
│  A[4×4] × B[4×4] + C[4×4] = D[4×4]                    │
│  (FP16 입력)       (FP32 누산)                           │
│                                                          │
│  1 클럭 = 64 FMA (Fused Multiply-Add) 연산              │
│  CUDA Core 1개: 1 FMA/클럭                               │
│  Tensor Core 1개: 64 FMA/클럭 → 64배 효율               │
│                                                          │
│  A100 SM(Streaming Multiprocessor) 1개:                  │
│  ┌─────────────────────────────────────┐                │
│  │  CUDA Core × 128                    │                │
│  │  Tensor Core × 4 (3세대)            │                │
│  │  L1 캐시 / 공유 메모리: 192KB        │                │
│  └─────────────────────────────────────┘                │
│  A100 전체: SM × 108 = Tensor Core 432개                │
└─────────────────────────────────────────────────────────┘
```

### 2.2 HBM (High Bandwidth Memory) 아키텍처

HBM (High Bandwidth Memory, 고대역폭 메모리)은 GPU 다이 옆에 3D 적층 방식으로 배치된 전용 메모리이다.

```
┌─────────────────────────────────────────────────────────┐
│              HBM3 vs GDDR6 비교                          │
│                                                          │
│  HBM3 (H100):                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ DRAM Die │  │ DRAM Die │  │ DRAM Die │ (8-high 적층)│
│  │ DRAM Die │  │ DRAM Die │  │ DRAM Die │              │
│  │ DRAM Die │  │ DRAM Die │  │ DRAM Die │              │
│  │ DRAM Die │  │ DRAM Die │  │ DRAM Die │              │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘              │
│        └─────────────┴─────────────┘                    │
│                  GPU Die                                 │
│  인터포저(Interposer): 1024-bit 버스                      │
│                                                          │
│  H100 HBM3:   3.35 TB/s 대역폭                          │
│  A100 HBM2e:  2.0 TB/s 대역폭                           │
│  GDDR6X:      ~1.0 TB/s (RTX 4090 기준)                 │
└─────────────────────────────────────────────────────────┘
```

### 2.3 혼합 정밀도 학습 (Mixed Precision Training)

```
┌─────────────────────────────────────────────────────────────┐
│         혼합 정밀도 학습 (Mixed Precision Training)           │
│                                                              │
│  FP32 마스터 가중치: W_fp32                                   │
│       │                                                      │
│       ▼ 다운캐스트                                            │
│  FP16 가중치: W_fp16     FP16 활성화: A_fp16                  │
│       │                          │                           │
│       └──────────┬───────────────┘                          │
│                  ▼                                           │
│       Tensor Core로 FP16 순전파 / 역전파                      │
│                  │                                           │
│                  ▼                                           │
│       FP16 그라디언트: ΔW_fp16                               │
│                  │                                           │
│                  ▼ 손실 역스케일링 (Loss Unscaling)           │
│       FP32 그라디언트: ΔW_fp32                               │
│                  │                                           │
│                  ▼                                           │
│       FP32 가중치 업데이트: W_fp32 ← W_fp32 - η·ΔW_fp32     │
└─────────────────────────────────────────────────────────────┘
```

#### 왜 FP32 마스터 가중치가 필요한가?

```
FP16 숫자 범위:
  최소 정규 수: 6.1×10⁻⁵
  최대 수: 65,504
  정밀도: 약 3.3 십진 자리

FP32 숫자 범위:
  최소 정규 수: 1.18×10⁻³⁸
  최대 수: 3.4×10³⁸
  정밀도: 약 7.2 십진 자리

문제: FP16으로 가중치 업데이트 시
  W = 1.0 (FP16),  ΔW = 0.0001 (FP16 표현 한계 이하)
  → 업데이트 손실! 학습 발산 위험
  
해결: FP32 마스터 가중치로 업데이트 후 FP16으로 복사
```

### 2.4 손실 스케일링 (Loss Scaling)

```
FP16 그라디언트 언더플로우 문제 해결:

  1. 순전파 전: Loss × Scale Factor (예: ×1024)
  2. 역전파 수행 (FP16 그라디언트, 스케일된 상태)
  3. 역전파 후: ΔW_fp16 / Scale Factor (역스케일링)
  4. 이상 값(Inf, NaN) 감지 → Scale 자동 조정

  동적 손실 스케일링 (Dynamic Loss Scaling):
  - 연속 N 스텝 정상 → Scale × 2 (증가)
  - Inf/NaN 발생 → Scale / 2 (감소), 스텝 스킵
```

### 2.5 BF16 (Brain Float 16) vs FP16 비교

```
┌──────────────────────────────────────────────────────┐
│         부동소수점 형식 비교                           │
│                                                      │
│  FP32:  [1 부호][8 지수][23 가수] = 32 bit           │
│  FP16:  [1 부호][5 지수][10 가수] = 16 bit           │
│  BF16:  [1 부호][8 지수][7 가수]  = 16 bit           │
│                                                      │
│  BF16의 장점:                                        │
│  - FP32와 동일한 지수 범위 → 오버플로우 없음          │
│  - 가수 정밀도 낮음 → 노이즈 도입 (정규화 효과)       │
│  - 변환: FP32 → BF16 (상위 16비트 절사, 단순)        │
│                                                      │
│  FP16의 단점:                                        │
│  - 좁은 지수 범위 → 대형 모델 학습 시 오버플로우 위험 │
│  - 손실 스케일링 필수                                 │
│                                                      │
│  결론: 트랜스포머 대형 모델 → BF16 선호              │
│       추론 최적화 → FP16/INT8/FP8 적극 활용          │
└──────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 혼합 정밀도 학습은 연필(FP16)로 빠르게 계산 초안을 잡고, 최종 기록은 잉크(FP32)로 정확하게 남기는 것과 같다. 속도와 정확성을 동시에 잡는 영리한 전략이다.

---

## 3. 구조 및 동작 원리

### 3.1 H100 vs A100 비교

| 항목 | A100 (Ampere) | H100 (Hopper) | 개선률 |
|:---|:---|:---|:---|
| **Tensor Core 세대** | 3세대 | 4세대 | — |
| **FP16 TFlops** | 312 | 989 (w/Sparsity: 1,979) | 3.2× |
| **BF16 TFlops** | 312 | 989 | 3.2× |
| **FP8 TFlops** | 미지원 | 3,958 | 신규 |
| **HBM 종류** | HBM2e | HBM3 | — |
| **메모리 대역폭** | 2.0 TB/s | 3.35 TB/s | 1.67× |
| **NVLink 대역폭** | 600 GB/s | 900 GB/s | 1.5× |
| **TDP (전력)** | 400W | 700W | 1.75× |
| **Transformer Engine** | ✗ | ✓ (FP8 자동) | 신규 |

### 3.2 정밀도별 성능/메모리 트레이드오프

```
┌─────────────────────────────────────────────────────┐
│         정밀도별 학습/추론 전략                       │
│                                                     │
│  INT4 ──→ INT8 ──→ FP8 ──→ FP16 ──→ BF16 ──→ FP32│
│  └─────────────────────┘  └──────────────────────┘ │
│       추론 양자화 영역            학습 가능 영역       │
│                                                     │
│  FP32: 최고 정밀도, 메모리 2×, 속도 기준            │
│  BF16: FP32 수준 범위, 속도 2×, 메모리 0.5×         │
│  FP16: 속도 2-4×, 손실 스케일링 필요               │
│  FP8:  H100 신규, 속도 4×, QAT 필요                │
│  INT8: 추론 전용, 속도 4-8×, PTQ/QAT 필요          │
│  INT4: 추론 전용, 속도 8-16×, 품질 저하 주의        │
└─────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 정밀도 선택은 사진 해상도와 같다. 원본(FP32)은 최고 화질이지만 용량이 크고, 압축(FP16/BF16)은 눈에 띄는 차이 없이 절반 크기, 썸네일(INT8/INT4)은 빠르지만 세부 정보 손실이 있다.

---

## 4. 비교 및 트레이드오프

### 4.1 PyTorch 혼합 정밀도 학습 구현

```python
import torch
from torch.cuda.amp import autocast, GradScaler

model = MyTransformer().cuda()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
scaler = GradScaler()  # 동적 손실 스케일링

for batch in dataloader:
    optimizer.zero_grad()
    
    # FP16 자동 캐스팅 (Tensor Core 활용)
    with autocast(dtype=torch.float16):
        output = model(batch['input'])
        loss = criterion(output, batch['label'])
    
    # 손실 스케일링 역전파
    scaler.scale(loss).backward()
    
    # 그라디언트 언스케일링 + 클리핑
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    
    # FP32 마스터 가중치 업데이트
    scaler.step(optimizer)
    scaler.update()

# BF16 사용 (H100/A100 권장)
with autocast(dtype=torch.bfloat16):
    output = model(batch['input'])
```

### 4.2 Transformer Engine (H100)

H100의 Transformer Engine은 레이어별로 FP8 정밀도를 자동으로 적용한다.

```
Transformer Engine 동작:
  ┌────────────────────────────────────────────┐
  │  레이어별 히스토그램 모니터링                 │
  │       │                                    │
  │       ▼                                    │
  │  동적 스케일 팩터 결정                       │
  │  (값 분포에 따라 FP8 E4M3 or E5M2 선택)    │
  │       │                                    │
  │       ▼                                    │
  │  Tensor Core에 FP8 입력 자동 공급           │
  │  → 이론상 BF16 대비 2배 처리량             │
  └────────────────────────────────────────────┘
```

### 4.3 메모리 최적화 기법

| 기법 | 설명 | 메모리 절감 |
|:---|:---|:---|
| **그라디언트 체크포인팅** | 활성화 값 재계산으로 메모리 절감 | 최대 10× (속도 33% 감소) |
| **FlashAttention** | IO 효율 어텐션 커널, HBM ↔ SRAM 최소화 | 메모리 O(N) |
| **혼합 정밀도 (BF16)** | FP32 대비 메모리 절반 | 2× 절감 |
| **ZeRO Stage 3** | 파라미터 분산 | GPU 수 비례 절감 |
| **Paged Attention** | KV 캐시 페이징 | 추론 중 메모리 급증 방지 |

📢 **섹션 요약 비유**: GPU 메모리 최적화는 작은 책상에서 작업하는 것과 같다. 필요한 책(활성화)만 꺼내고(그라디언트 체크포인팅), 같은 내용을 두 번 안 쓰고(FlashAttention), 작은 글씨로 메모하되(BF16) 중요한 것은 정자로 남긴다(FP32 마스터).

---

## 5. 실무 적용 및 최적화 기법

### 5.1 혼합 정밀도 학습 효과

| 항목 | FP32 기준 | BF16 혼합 정밀도 |
|:---|:---|:---|
| **메모리 사용** | 100% | ~50% |
| **학습 속도** | 1× | 2~4× |
| **수렴 품질** | 기준 | 동등 (대형 모델) |
| **손실 스케일링 필요** | ✗ | BF16: ✗, FP16: ✓ |

### 5.2 기술사 답안 핵심 논점

1. **Tensor Core 활용 조건**: 행렬 크기가 8(FP16)·16(FP8)의 배수일 때 최대 효율 (Alignment 규칙)
2. **BF16 vs FP16 선택**: 대형 트랜스포머 학습 → BF16 (지수 범위 넓음), 엣지 추론 → FP16/INT8
3. **HBM 병목 이해**: 연산 속도보다 메모리 대역폭이 병목(Bandwidth-bound)인 경우 FlashAttention으로 해결
4. **H100 Transformer Engine**: FP8 자동 관리로 개발자 개입 없이 최대 4× 속도 향상

📢 **섹션 요약 비유**: 혼합 정밀도 GPU 최적화는 F1 레이싱의 타이어 전략과 같다. 소프트 타이어(FP16)로 빠른 랩타임을 내고, 핵심 계산(가중치 업데이트)은 하드 타이어(FP32)로 내구성을 확보한다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 하드웨어 | Tensor Core | NVIDIA 행렬 곱 전용 하드웨어 유닛 |
| 메모리 | HBM3 | GPU 전용 3D 적층 고대역폭 메모리 |
| 학습 기법 | Mixed Precision | FP16/BF16 + FP32 마스터 가중치 |
| 안정화 | Loss Scaling | FP16 언더플로우 방지 스케일링 |
| 수치 형식 | BF16 | 구글 Brain Float, FP32 호환 지수부 |
| 커널 최적화 | FlashAttention | IO 효율 어텐션, HBM 접근 최소화 |
| 하드웨어 비교 | H100 vs A100 | Hopper vs Ampere 세대 비교 |
| 상호연결 | NVLink/NVSwitch | GPU 간 고속 통신 인터커넥트 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. Tensor Core는 곱셈 전용 계산기야 — 일반 계산기는 한 번에 하나씩 계산하지만, Tensor Core는 4×4 표 전체를 한 번에 처리해!

### 📈 관련 키워드 및 발전 흐름도

```text
FP32 학습 (기본, 높은 정밀도)
    │
    ▼
혼합 정밀도 학습 (Mixed Precision): FP16 연산 + FP32 마스터 가중치
    ├─► Loss Scaling: 언더플로 방지
    └─► Tensor Core 활용: 4×4 행렬 fused multiply-add
    │
    ▼
GPU 메모리 최적화
    ├─► HBM (High Bandwidth Memory): 대역폭 극대화
    ├─► Gradient Checkpointing: 메모리↔연산 트레이드오프
    └─► Flash Attention: IO-aware 어텐션
    │
    ▼
BF16 (Brain Float 16) → FP8 (H100+) → 차세대 정밀도
```
2. 혼합 정밀도 학습은 계산할 때 연필(FP16)로 빠르게 쓰고, 최종 답은 잉크(FP32)로 정확하게 남기는 거야.
3. HBM은 GPU 안에 있는 초고속 메모리야 — 일반 RAM이 버스라면, HBM은 특급 열차처럼 빠르게 데이터를 전달해줘!
