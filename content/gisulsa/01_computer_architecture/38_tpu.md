+++
weight = 38
title = "38. TPU (Tensor Processing Unit)"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 TPU & AI 전용 가속기 비교

> **별점**: ★★★★☆ | 기본 필수

## 1. TPU 아키텍처

```
[구글 TPU]
목적: 구글의 AI 추론·학습 전용 칩
핵심: 시스톨릭 배열 (Systolic Array)

[시스톨릭 배열]
PE(Processing Element)가 행렬 방식으로 배치
데이터가 배열을 통해 흐르면서 연산
행렬 곱셈 = GeMM에 최적화

예) 256×256 PE 배열:
  한 사이클에 65,536번 곱셈-덧셈
  → 행렬 곱 = 딥러닝 핵심 연산

[TPU 세대]
TPU v1 (2016): 추론 전용, INT8
TPU v2 (2017): 학습 지원, BF16
TPU v3 (2018): 물 냉각, 더 강력
TPU v4 (2021): 최신, 대규모 포드 구성
TPU v5e/p (2023): 가격/성능 최적화
```

## 2. AI 가속기 비교

```
[GPU vs NPU vs TPU 비교]
항목       GPU           NPU            TPU
제조사     NVIDIA/AMD    Qualcomm/Apple  Google
범용성     높음          중간            낮음(구글)
프로그래밍  CUDA          제조사 SDK     JAX/XLA
에너지     보통          효율            효율
용도       학습+추론     모바일 추론     구글 학습+추론
```

## 3. 양자 컴퓨팅 (미래 가속기)

```
양자 비트 (Qubit): 0과 1 중첩
  → 특정 문제에서 지수적 병렬성

[양자 우위 (Quantum Advantage)]
대규모 최적화 문제
소인수분해 (Shor 알고리즘)
양자 화학 시뮬레이션

[현재 한계]
양자 디코히어런스: 오류율 높음
큐비트 수 제한
극저온 환경 필요 (15 밀리켈빈)

보안 영향: RSA 위협 → PQC (양자내성암호) 필요
```

## 4. 답안 포인트

**3단락**: ① TPU 시스톨릭 배열 구조 → ② GPU/NPU/TPU 비교 & 사용 시나리오 → ③ 양자 컴퓨팅 전망 & PQC 보안 연계

## 5. 관련 개념

`NPU(★134회, 37번)` → 모바일/엣지 AI | `GPU(34번)` → 범용 병렬 연산 | `PQC(★09_security 09번)` → 양자 컴퓨터 위협 대응
