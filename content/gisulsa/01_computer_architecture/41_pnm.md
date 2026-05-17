+++
weight = 41
title = "41. PNM — Processing Near Memory"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# PNM (Processing Near Memory), PIM (Processing In Memory), HBM-PIM

> 출제 빈도: ★★★★☆ | 난이도: ★★★★☆ | 기출: ★131회

---

## 답안.

### Ⅰ. 개요

PNM(Processing Near Memory)은 CPU/GPU에서 데이터를 가져오는 대신, **메모리 근처에서 연산을 수행**하여 메모리 대역폭 병목과 에너지 소비를 획기적으로 줄이는 차세대 컴퓨팅 패러다임이다.
- **PIM(Processing In Memory)**: 메모리 칩 내부에 연산 회로 내장
- **PNM**: 메모리 패키지 내(HBM 스택 베이스 다이 등)에 연산 유닛 배치

### Ⅱ. 핵심 구성요소

```
I. PNM 등장 배경 — 메모리 월(Memory Wall)
   
   기존 von Neumann 병목:
   [CPU] ←── 좁은 버스 ──→ [DRAM]
    연산      대역폭 병목     데이터
   
   - CPU 성능: 매년 50% 향상
   - DRAM 대역폭: 매년 10% 향상
   → '메모리 월': 데이터 이동이 연산보다 느리고 비쌈
   - AI 워크로드: 대규모 행렬 연산 = 데이터 이동 집약적

II. PNM/PIM 아키텍처
   
   [HBM-PIM 구조 (삼성)]
   ┌─────────────────────────┐
   │   Base Die (베이스 다이)  │
   │  ┌────┐ ┌────┐ ┌────┐  │
   │  │PIM │ │PIM │ │PIM │  │  ← AI 연산 유닛
   │  │Unit│ │Unit│ │Unit│  │
   │  └────┘ └────┘ └────┘  │
   ├─────────────────────────┤
   │  DRAM Die 1 (16GB)      │
   │  DRAM Die 2 (16GB)      │
   │  DRAM Die 3 (16GB)      │
   │  DRAM Die 4 (16GB)      │
   └─────────────────────────┘
   
   동작: 데이터 이동 최소화 → 메모리 내 MAC 연산 직접 수행


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
