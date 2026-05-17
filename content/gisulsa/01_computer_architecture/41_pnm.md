+++
weight = 41
title = "41. PNM — Processing Near Memory"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
exam = "★ 131회 기출"
+++

# 🎯 핵심 키워드: PNM (Processing Near Memory), PIM (Processing In Memory), HBM-PIM

> **출제 빈도**: ★★★★☆ | **난이도**: ★★★★☆ | **기출**: ★131회

## 1. 정의

PNM(Processing Near Memory)은 CPU/GPU에서 데이터를 가져오는 대신, **메모리 근처에서 연산을 수행**하여 메모리 대역폭 병목과 에너지 소비를 획기적으로 줄이는 차세대 컴퓨팅 패러다임이다.

- **PIM(Processing In Memory)**: 메모리 칩 내부에 연산 회로 내장
- **PNM**: 메모리 패키지 내(HBM 스택 베이스 다이 등)에 연산 유닛 배치

## 2. 출제 포인트

| 포인트 | 내용 | 채점 비중 |
|--------|------|----------|
| 정의 | PNM/PIM 구분, 등장 배경(메모리 월) | 20% |
| 구성요소 | HBM-PIM 구조, 연산 유닛 | 35% |
| 비교 | 기존 von Neumann vs PNM | 25% |
| 트렌드 | AI 워크로드, 삼성 HBM-PIM | 20% |

## 3. 답안 목차 템플릿

**문제**: "PNM(Processing Near Memory)의 개념과 AI 가속에서의 활용을 설명하시오."

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

III. 기존 방식 vs PNM 비교
   | 항목         | 기존 (CPU/GPU)     | PNM             |
   |-------------|-------------------|-----------------|
   | 데이터 이동  | CPU ↔ DRAM 왕복   | 메모리 내 처리   |
   | 에너지 효율  | 낮음               | 수십 배 향상     |
   | 대역폭 활용  | 버스 병목          | 내부 대역폭 활용 |
   | 프로그래밍  | 일반 모델           | 별도 API 필요   |

IV. AI 시대 PNM 적용
   - LLM 추론: 대용량 가중치(수십GB) → PNM으로 메모리 내 연산
   - 삼성 HBM-PIM: GDDR6-AiM → AI 가속기에 탑재
   - UPMEM: DDR4 기반 PIM DIMM → 서버 DB 가속
```

## 4. 핵심 암기 포인트

- **메모리 월**: CPU는 빠른데 메모리 대역폭이 병목
- **PIM vs PNM**: PIM=칩 내부, PNM=패키지 내 근처
- **HBM-PIM**: 삼성 실제 제품. AI 가속기의 미래

## 5. 관련 개념 연결

| 개념 | 연결 포인트 |
|------|------------|
| HBM (High Bandwidth Memory) | PIM이 내장되는 메모리 |
| NPU (★134회) | PNM과 협력하는 AI 가속기 |
| 칩렛 (★131회) | PIM이 메모리 칩렛으로 통합 |
| CXL (☆예측) | PNM 확장된 메모리 풀링 |
| 폴락의 법칙 (★132회) | 단순 연산 유닛 분산 배치 |
