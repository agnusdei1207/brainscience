+++
weight = 6
title = "06. LLM 파인튜닝 & PEFT"
date = "2026-05-17"
[extra]
categories = "gisulsa-ai"
+++

# 🎯 LLM 파인튜닝 & PEFT (효율적 학습)

> **별점**: ★★★★★ | ★136회 기출

## 1. LLM 파인튜닝 개요

```
[파인튜닝 필요성]
파운데이션 모델: 범용 지식 (GPT-4, Claude)
파인튜닝: 특정 태스크/도메인에 최적화

[파인튜닝 유형]
Full Fine-tuning:
  모든 가중치 업데이트 (비용 최고)
  GPU 메모리: 100B 모델 = 수백 GB

PEFT (Parameter Efficient Fine-Tuning):
  소수 파라미터만 업데이트
  전체 성능 유지, 비용 대폭 절감
```

## 2. PEFT 핵심 기법

```
[LoRA (Low-Rank Adaptation)]
가중치 행렬을 저랭크 분해로 근사
W' = W + ΔW = W + A×B
  A: (d × r) 행렬, r << d (랭크)
  B: (r × k) 행렬
업데이트할 파라미터: r × (d+k) << d × k

장점: 메모리 10배 절감, 원본 가중치 고정
     여러 LoRA를 전환하여 다중 태스크

QLoRA:
  4bit 양자화 + LoRA 결합
  70B 모델을 48GB GPU에서 학습 가능

[Prefix Tuning]
입력 앞에 학습 가능한 프리픽스 토큰 추가
모델 가중치 고정, 프리픽스만 학습

[Prompt Tuning]
프리픽스 최소화, 소프트 프롬프트 학습
```

## 3. 정렬 (Alignment) 기법

```
[RLHF (Reinforcement Learning from Human Feedback)]
사람 피드백으로 LLM 정렬
1. 지도 학습 파인튜닝 (SFT)
2. 보상 모델 학습 (인간 선호도 반영)
3. PPO 강화학습으로 최적화
→ ChatGPT 핵심 기법

[DPO (Direct Preference Optimization)]
RLHF 단순화: 보상 모델 없이 직접 최적화
선호/비선호 쌍으로 학습
더 안정적, 학습 효율적

[Constitutional AI (CAI, Anthropic)]
AI 스스로 원칙 적용 → 출력 비판·개선
```

## 4. 답안 포인트

**3단락**: ① LLM 파인튜닝 필요성 & Full vs PEFT → ② LoRA/QLoRA 저랭크 분해 원리 → ③ RLHF/DPO 정렬 기법 & ChatGPT 적용

## 5. 관련 개념

`LLM(★★02번)` → 파인튜닝의 대상 | `MLOps(04번)` → LoRA 모델 배포 관리 | `Agentic AI(★136회 11번)` → 정렬된 에이전트 설계
