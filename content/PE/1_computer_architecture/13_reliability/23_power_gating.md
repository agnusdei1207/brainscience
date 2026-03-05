+++
title = "471. 전력 게이팅 (Power Gating)"
description = "사용하지 않는 회로에 전원 차단으로 정적 전력 절감"
date = "2026-03-05"
[taxonomies]
tags = ["Power Gating", "전력게이팅", "Sleep Transistor", "Leakage", "C-state"]
categories = ["studynotes-1_computer_architecture"]
+++

# 471. 전력 게이팅 (Power Gating)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전력 게이팅은 사용하지 않는 회로 모듈에 전원(VDD) 자체를 차단하여 정적 전력(누설 전류)까지 0으로 만드는 가장 강력한 저전력 기술이다.
> 2. **가치**: 정적 전력의 90~99% 절감이 가능하며, 현대 CPU의 Deep C-state(C6, C7 등)에서 코어 단위 전력 게이팅을 적용하여 대기 전력을 거의 0으로 만든다.
> 3. **융합**: Sleep Transistor(Header/Footer Switch)로 구현되며, State Retention, Wake-up Latency, In-rush Current 등의 설계 고려사항이 있다.

---

### I. 개요

#### 개념 정의

**전력 게이팅(Power Gating)**은 회로 모듈의 전원을 물리적으로 차단하여 누설 전류를 완전히 없애는 기술이다. Clock Gating이 동적 전력만 차단한다면, Power Gating은 정적 전력까지 차단한다.

```
┌─────────────────────────────────────────────────────────────────┐
│                  전력 게이팅 구조                               │
└─────────────────────────────────────────────────────────────────┘

Header Switch 방식:
                    VDD (Power Rail)
                         │
                    ┌────┴────┐
                    │  Sleep  │ ◀── Sleep Signal
                    │   PMOS  │     (0 = ON, 1 = OFF)
                    └────┬────┘
                         │
                    Virtual VDD
                         │
                    ┌────┴────┐
                    │  Logic  │
                    │ Circuit │
                    └────┬────┘
                         │
                        GND

Sleep = 0: PMOS ON → 전원 공급 → 회로 동작
Sleep = 1: PMOS OFF → 전원 차단 → 누설 전류 ≈ 0
```

#### 비유

> **전력 게이팅은 "안 쓰는 방의 차단기(두꺼비집)를 내리는 것"과 같다.**
>
> 전등만 끄는 건 Clock Gating. 하지만 차단기를 내리면 그 방에는 완전히 전기가 안 들어간다. 냉장고, 텔레비전, 모든 게 꺼진다!

---

### II. 아키텍처 및 핵심 원리

#### Power Gating 구현 방식

```
1. Header Switch (VDD 차단):
   · PMOS를 VDD에 배치
   · 면적이 크지만 성능 손실 적음
   · 누설 감소 효과 우수

2. Footer Switch (GND 차단):
   · NMOS를 GND에 배치
   · 면적이 작지만 성능 손실 있음
   · Ground Bounce 위험

3. Power Switch Array:
   · 여러 개의 작은 스위치 병렬 연결
   · In-rush Current 제어
   · 점진적 Wake-up 가능
```

#### Power Gating 시퀀스

```
Power Down Sequence:
1. 인터럽트 비활성화
2. 상태 저장 (Retention Register / Memory)
3. Sleep 신호 Active
4. 전원 차단 (수 μs ~ 수 ms)
5. 정적 전력 = 0

Power Up Sequence:
1. Sleep 신호 Inactive
2. 전원 인가 (In-rush Current 제어)
3. 전압 안정화 대기
4. 상태 복원
5. 인터럽트 활성화
```

---

### III. 융합 비교 및 다각도 분석

#### Clock Gating vs Power Gating

| 항목 | Clock Gating | Power Gating |
|------|--------------|--------------|
| **차단 대상** | 클럭 | 전원 |
| **절감 전력** | 동적만 | 동적 + 정적 |
| **절감률** | 20~40% | 90~99% |
| **복구 시간** | ns | μs ~ ms |
| **상태 유지** | O | X (별도 저장) |

---

### IV. 실무 적용

#### 실무 시나리오: Intel CPU C-states

```
┌─────────────────────────────────────────────────────────────────┐
│              Intel CPU C-state (Power Gating 적용)              │
└─────────────────────────────────────────────────────────────────┘

C0: Active (전원 ON, 클럭 ON)
C1: Halt (클럭 Gated, 전원 ON)
C1E: Enhanced Halt (클럭 Gated, 전압 낮춤)
C3: Sleep (클럭 Gated, PLL Off)
C6: Deep Power Down (Power Gated) ← 코어 전원 차단
C7: Deeper Power Down (Power Gated + LLC Flush)
C8/C9/C10: Additional Power Gating

C6 상태:
· 코어 전원: OFF (Power Gated)
· 누설 전력: ~0
· Wake-up 시간: ~150μs
· 절감 효과: 정적 전력 90%+ 감소
```

---

### V. 기대효과 및 결론

전력 게이팅은 정적 전력을 거의 완전히 제거하는 가장 강력한 기술. Wake-up 지연이 단점.

---

### 관련 개념 맵 (Knowledge Graph)

- [468. 정적 전력](./20_static_power.md) - 전력 게이팅이 제거하는 대상
- [470. 클럭 게이팅](./22_clock_gating.md) - 더 가벼운 절감 기술
- [473. 서멀 스로틀링](./25_thermal_throttling.md) - 발열 관련 기술

---

### 어린이를 위한 3줄 비유 설명

**전력 게이팅은 "안 쓰는 방의 두꺼비집을 내리는 것"과 같아요!**

1. 전등만 끄면(Clock Gating) 방에 전기는 들어오지만 안 써요. 하지만 두꺼비집을 내리면(Power Gating) 방에 완전히 전기가 끊겨요!

2. 컴퓨터가 쉴 때 아예 전기를 끊어버리면, 전기가 새어 나가는 것(누설 전류)도 완전히 막을 수 있어요!

3. 다시 쓸 때는 두꺼비집을 올리면 돼요. 조금 시간이 걸리지만, 전기를 아주 많이 아낄 수 있어요!
