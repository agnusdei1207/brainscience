+++
weight = 18
title = "18. HBM (High Bandwidth Memory)"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 HBM & 차세대 메모리 기술

> **별점**: ★★★★★ | ☆ 2026 예측

## 1. HBM (High Bandwidth Memory)

```
정의: 3D 적층 기술을 사용한 고대역폭 DRAM
     기존 GDDR 대비 대역폭 5~10배 ↑

[HBM 구조]
여러 개의 DRAM 다이를 TSV(관통 실리콘 비아)로 수직 연결
→ 짧은 배선 = 저전력 + 고속

HBM1: 128GB/s
HBM2/2E: 256~460GB/s
HBM3: 819GB/s (SK하이닉스, 2022)
HBM3e: 1.2TB/s (NVIDIA H200 사용)

[인터포저 기반 2.5D 패키징]
HBM + GPU → 실리콘 인터포저 위에 배치
= CoWoS (TSMC), InFO-MSI, SoIC
→ 메모리↔GPU 물리적 거리 최소화
```

## 2. PIM (Processing In Memory)

```
기존 문제: Memory Wall (CPU-메모리 대역폭 병목)
PIM 해결: 메모리 내에서 직접 연산

HBM-PIM (PNM):
  각 HBM 스택 내에 AI 연산 유닛 내장
  메모리↔연산 간 데이터 이동 최소화
  삼성: AXDIMM, SK하이닉스: AiM

적용: AI 행렬 연산, 데이터 집약 작업
```

## 3. LPDDR vs GDDR vs HBM

| 메모리 | 용도 | 대역폭 | 특징 |
|--------|------|--------|------|
| LPDDR5 | 스마트폰/온디바이스 | ~68GB/s | 저전력 |
| GDDR6X | GPU 그래픽 | ~1000GB/s | 고대역폭 |
| HBM3e | AI HPC | ~1.2TB/s | 최고 대역폭 |
| CXL | 메모리 풀링 | 가변 | 확장성 |

## 4. 답안 포인트

**3단락**: ① HBM 정의 & TSV 3D 적층 구조 → ② PIM/HBM-PIM 메모리 내 연산 → ③ LPDDR/GDDR/HBM 비교 & AI 가속기 적용

## 5. 관련 개념

`PNM(★131회, 41번)` → HBM 내 연산 | `NPU(★134회, 37번)` → HBM3e + NPU 조합 | `CXL(☆예측, 19번)` → HBM 메모리 풀링
