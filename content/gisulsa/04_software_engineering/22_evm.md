+++
weight = 22
title = "22. EVM (Earned Value Management)"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# 🎯 EVM (획득가치관리)

> **별점**: ★★★★☆ | 기본 필수

## 1. 핵심 지표

| 지표 | 의미 | 계산 |
|------|------|------|
| **PV** (계획가치) | 이시점 완료 예정 작업 비용 | 계획 기반 |
| **EV** (획득가치) | 실제 완료된 작업의 계획 비용 | 완료율×BAC |
| **AC** (실제비용) | 실제 지출 비용 | 실제 지출 |
| **BAC** | 전체 예산 | 총 계획 비용 |

## 2. 성과 지표

```
[진척도 지표]
SV (일정 차이) = EV - PV
SPI (일정 성과 지수) = EV / PV
→ SPI < 1: 일정 지연

[비용 지표]
CV (비용 차이) = EV - AC
CPI (비용 성과 지수) = EV / AC
→ CPI < 1: 예산 초과

[완료 예측]
EAC (완료 예상 비용) = BAC / CPI
ETC (잔여 예상 비용) = EAC - AC
VAC (완료 분산) = BAC - EAC

예시:
BAC=100, PV=50, EV=40, AC=55
SPI = 40/50 = 0.8 (20% 지연)
CPI = 40/55 = 0.73 (27% 예산 초과)
EAC = 100/0.73 = 137 (최종 예상 비용)
```

## 3. S-Curve

```
EVM S-Curve 그래프:
y축: 누적 비용
x축: 시간

PV 곡선: 계획 완료 경로
EV 곡선: 실제 완료 경로 (PV 대비 위/아래)
AC 곡선: 실제 지출 경로

SV = EV - PV (PV와 EV의 수직 거리)
CV = EV - AC (EV와 AC의 수직 거리)
```

## 4. 답안 포인트

**3단락**: ① PV/EV/AC 정의 → ② SPI/CPI/EAC 계산 & 해석 → ③ S-Curve 시각화 & 프로젝트 의사결정 연계

## 5. 관련 개념

`CPM/PERT` → 일정 계획(PV 기반) | `PMO(★132회)` → EVM 성과 보고 | `프로젝트 위험관리` → CPI 저하 시 선제 대응
