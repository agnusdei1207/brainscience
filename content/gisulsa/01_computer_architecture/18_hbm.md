+++
weight = 18
title = "18. HBM (High Bandwidth Memory)"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# HBM & 차세대 메모리 기술

> 별점: ★★★★★ | ☆ 2026 예측

---

## 답안.

### Ⅰ. 개요

정의: 3D 적층 기술을 사용한 고대역폭 DRAM
     기존 GDDR 대비 대역폭 5~10배 ↑
여러 개의 DRAM 다이를 TSV(관통 실리콘 비아)로 수직 연결

### Ⅱ. 핵심 구성요소

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
```
기존 문제: Memory Wall (CPU-메모리 대역폭 병목)
PIM 해결: 메모리 내에서 직접 연산

HBM-PIM (PNM):
  각 HBM 스택 내에 AI 연산 유닛 내장
  메모리↔연산 간 데이터 이동 최소화
  삼성: AXDIMM, SK하이닉스: AiM

적용: AI 행렬 연산, 데이터 집약 작업
```


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
