+++
weight = 1
title = "01. 캐시·파이프라인·해저드"
date = "2026-05-18"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 캐시 메모리, 파이프라인, 해저드

> 출제 빈도: ★★★★★ | 컴퓨터구조 기본 필수

---

## 답안.

### Ⅰ. 개요

캐시 메모리(Cache Memory)란 CPU와 주기억장치 사이의 속도 격차를 해소하기 위해 시간적·공간적 지역성(Locality)을 활용하는 고속 SRAM 버퍼이다. 파이프라인(Pipeline)은 명령어 실행 단계(IF→ID→EX→MEM→WB)를 중첩 실행하여 CPI(Cycles Per Instruction)를 이상적으로 1에 수렴시키는 CPU 성능 향상 기법이다. 해저드(Hazard)는 이러한 파이프라인 흐름을 방해하는 요소로, 정확한 제어 없이는 오히려 성능 저하를 초래한다.

### Ⅱ. 캐시 메모리 구조와 동작

캐시는 L1(접근 ~1ns)→L2(~5ns)→L3(~20ns) 다계층 구조로 설계되며, 적중률(Hit Ratio)이 전체 성능을 좌우한다. 평균 메모리 접근 시간은 아래와 같이 산출된다.

```
AMAT = Hit Time + Miss Rate × Miss Penalty

예) Hit Time=1ns, Miss Rate=5%, Miss Penalty=100ns
    AMAT = 1 + 0.05 × 100 = 6ns
```

캐시 매핑 방식은 직접(Direct), 연관(Fully Associative), 집합연관(Set-Associative)으로 분류되며, 교체 정책에는 LRU, LFU, FIFO가 적용된다. 쓰기 정책은 Write-Through(즉시 반영)와 Write-Back(지연 반영) 두 가지이며, 멀티코어 환경에서는 MESI 프로토콜로 캐시 일관성(Cache Coherence)을 유지한다.

### Ⅲ. 파이프라인 단계와 해저드

5단 파이프라인은 다음과 같이 명령어를 중첩 처리한다.

```
시간축 →  T1   T2   T3   T4   T5   T6   T7
명령 1:  [IF] [ID] [EX] [MEM][WB]
명령 2:       [IF] [ID] [EX] [MEM][WB]
명령 3:            [IF] [ID] [EX] [MEM][WB]
```

해저드는 세 가지 유형으로 분류된다.

| 유형 | 원인 | 해결 기법 |
|------|------|-----------|
| 데이터 해저드 | RAW 의존성 | 포워딩(Forwarding), 파이프라인 인터락 |
| 제어 해저드 | 분기 명령 | 분기 예측(Branch Prediction), 지연 분기 |
| 구조 해저드 | 자원 충돌 | 하버드 구조(I/D 캐시 분리), 다중 포트 |

### Ⅳ. 캐시 vs 파이프라인 비교

| 구분 | 캐시 메모리 | 파이프라인 |
|------|-------------|-----------|
| 목적 | 메모리 접근 지연 감소 | 명령어 처리량(Throughput) 향상 |
| 핵심 원리 | 지역성(Locality) | 단계 중첩(Stage Overlap) |
| 성능 지표 | 적중률, AMAT | IPC, CPI |
| 위험 요소 | 미스 패널티, 일관성 | 해저드, 플러시 패널티 |

### Ⅴ. 적용 사례 및 전망

현대 고성능 CPU(Apple M시리즈, AMD Zen)는 12~20단 파이프라인에 비순차 실행(OoO)과 투기적 실행(Speculative Execution)을 결합하며, L1 캐시 64KB~192KB에 Way Prediction을 적용하여 적중률 95% 이상을 달성한다. 엣지 AI SoC 분야에서는 전력 제약 하에 2~3단 짧은 파이프라인과 스크래치패드 메모리를 사용하여 결정론적 지연을 보장한다. 향후 CXL 기반 메모리 풀링과 결합하여 캐시 계층이 확장될 전망이다.

---

**관련**: 메모리 계층(02번) · 캐시 매핑(12번) · 캐시 일관성 MESI(14번) · CXL(19번)
