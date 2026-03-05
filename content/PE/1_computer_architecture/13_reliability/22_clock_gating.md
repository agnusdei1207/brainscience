+++
title = "470. 클럭 게이팅 (Clock Gating)"
description = "사용하지 않는 회로에 클럭 차단으로 동적 전력 절감"
date = "2026-03-05"
[taxonomies]
tags = ["Clock Gating", "클럭게이팅", "Dynamic Power", "Low Power", "Enable"]
categories = ["studynotes-1_computer_architecture"]
+++

# 470. 클럭 게이팅 (Clock Gating)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 클럭 게이팅은 사용하지 않는 회로 모듈에 클럭 신호를 차단하여 동적 전력(P ∝ f)을 0으로 만드는 저전력 설계 기법이다.
> 2. **가치**: Fine-grained 게이팅으로 20~40%, Coarse-grained 게이팅으로 40~60%의 동적 전력 절감이 가능하며, 현대 CPU의 필수 기술이다.
> 3. **융합**: 하드웨어(자동)와 소프트웨어(명시적) 클럭 게이팅이 있으며, DVFS, Power Gating과 함께 계층적 전력 관리를 구성한다.

---

### I. 개요

#### 개념 정의

**클럭 게이팅(Clock Gating)**은 디지털 회로에서 사용하지 않는 모듈에 클럭 신호를 차단하는 기술이다. 클럭이 없으면 플립플롭이 스위칭하지 않아 동적 전력이 0이 된다.

```
┌─────────────────────────────────────────────────────────────────┐
│                  클럭 게이팅 원리                               │
└─────────────────────────────────────────────────────────────────┘

Clock Gating 없음:
    CLK ──────────────────▶ [Module] ──▶ Power 소모

Clock Gating 적용:
                    ┌───────────┐
    CLK ───────────▶│    AND    │────▶ [Module] ──▶ No Power (Idle)
                    │   Gate    │
                    └─────┬─────┘
                          │
                    Enable│ (0 = Gated)

Module이 idle일 때 Enable = 0 → 클럭 차단 → 동적 전력 = 0
```

#### 비유

> **클럭 게이팅은 "사용하지 않는 방의 전등을 끄는 것"과 같다.**
>
> 집에 10개의 방이 있고, 현재 3개만 사용 중이라면 나머지 7개 방의 전등을 끈다. 전등이 꺼진 방은 전기를 안 쓴다!

---

### II. 아키텍처 및 핵심 원리

#### 클럭 게이팅 유형

```
1. Coarse-grained (거시적):
   · 모듈/블록 단위 게이팅
   · 예: FPU, L2 Cache, 전체 코어
   · 소프트웨어 제어
   · 게이팅 오버헤드: 낮음

2. Fine-grained (미시적):
   · 개별 플립플롭/레지스터 단위
   · 하드웨어 자동 제어
   · 게이팅 오버헤드: 있음 (면적 증가)

3. Sequential Clock Gating:
   · 데이터 경로 분석 후 게이팅
   · RTL 합성 시 자동 삽입
   · EDA 툴 최적화
```

---

### III. 융합 비교 및 다각도 분석

#### 전력 절감 효과

| 기법 | 절감률 | 지연 | 구현 복잡도 |
|------|--------|------|-------------|
| Coarse-grained | 40~60% | 낮음 | 낮음 |
| Fine-grained | 20~40% | 없음 | 높음 |
| Power Gating | 90%+ | 높음 | 높음 |

---

### IV. 실무 적용

#### 실무 시나리오: CPU Idle

```c
// Linux Kernel Clock Gating
// arch/arm/kernel/process.c

void arch_cpu_idle(void) {
    // 1. Clock Gating 진입
    clockevents_notify(CLOCK_EVT_NOTIFY_BROADCAST_ENTER, ...);

    // 2. WFI (Wait For Interrupt) - 클럭 정지
    cpu_do_idle();

    // 3. 인터럽트 시 깨어남
    clockevents_notify(CLOCK_EVT_NOTIFY_BROADCAST_EXIT, ...);
}
```

---

### V. 기대효과 및 결론

클럭 게이팅은 동적 전력 절감의 기본 기술. Fine/Coarse 조합으로 최적화.

---

### 관련 개념 맵 (Knowledge Graph)

- [467. 동적 전력](./19_dynamic_power.md) - 클럭 게이팅이 절감하는 대상
- [469. DVFS](./21_dvfs.md) - 주파수 조절 기술
- [471. 전력 게이팅](./23_power_gating.md) - 더 강력한 절감 기술

---

### 어린이를 위한 3줄 비유 설명

**클럭 게이팅은 "사용하지 않는 방의 전등을 끄는 것"과 같아요!**

1. 집에 10개 방이 있어도 지금 쓰는 건 3개뿐이에요. 나머지 7개 방의 전등을 켜두면 전기 낭비죠!

2. 컴퓨터도 마찬가지예요. 지금 쓰지 않는 부분에는 "일해라!"라는 신호(클럭)를 보내지 않아요. 그럼 전기를 안 써요!

3. 이렇게 안 쓰는 부분만 골라서 신호를 차단하는 게 클럭 게이팅이에요. 전기도 아끼고, 발열도 줄어들어요!
