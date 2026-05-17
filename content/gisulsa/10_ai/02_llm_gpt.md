+++
weight = 2
title = "02. LLM·GPT·트랜스포머"
date = "2026-05-18"
[extra]
categories = "gisulsa-ai"
+++

# LLM, GPT, 트랜스포머

> 출제 빈도: ★★★★★ | ★132,135회 기출

---

## 답안.

### Ⅰ. 개요

대규모 언어 모델(LLM, Large Language Model)은 수십억~수조 개의 파라미터를 가진 트랜스포머(Transformer) 기반 신경망으로, 대규모 텍스트 코퍼스에서 사전학습(Pre-training)하여 자연어 이해·생성·추론 능력을 획득한 AI 모델이다. GPT(Generative Pre-trained Transformer)는 OpenAI가 개발한 대표적 LLM이다.

### Ⅱ. 트랜스포머 구조

```
입력 토큰 → [임베딩 + 위치 인코딩]
                    ↓
         ┌──────────────────┐
         │  Multi-Head       │ ← Q, K, V 행렬 연산
         │  Self-Attention   │   Attention(Q,K,V)
         ├──────────────────┤   = softmax(QK^T/√d)V
         │  Feed-Forward     │
         │  Network          │
         └────────┬─────────┘
                  │ × N layers (GPT-4: ~120층)
                  ↓
         [출력 확률 분포] → 다음 토큰 예측
```

셀프 어텐션(Self-Attention)은 입력 시퀀스 내 모든 토큰 간 관계를 병렬로 계산하여, RNN의 순차 처리 한계를 극복했다. 이것이 LLM 성능 혁신의 핵심이다.

### Ⅲ. 사전학습과 미세조정

| 단계 | 방법 | 데이터 | 목적 |
|------|------|--------|------|
| 사전학습 | 다음 토큰 예측 (CLM) | 인터넷 텍스트 수 TB | 일반 언어 능력 |
| SFT | 지도 미세조정 | 고품질 Q&A 데이터 | 지시 따르기 |
| RLHF | 인간 피드백 강화학습 | 선호도 라벨링 | 안전성·유용성 정렬 |
| LoRA/QLoRA | 파라미터 효율 미세조정 | 도메인 데이터 | 적은 자원으로 특화 |

### Ⅳ. 스케일링 법칙

Chinchilla 스케일링 법칙에 의하면 모델 파라미터 수와 학습 데이터 토큰 수를 균형 있게 늘려야 최적 성능을 달성한다. 파라미터만 키우면 학습 부족(Under-training), 데이터만 늘리면 모델 용량 부족이 된다.

### Ⅴ. 한계와 전망

환각(Hallucination), 최신 정보 부족, 추론 비용 문제가 존재하며, RAG(검색증강생성), MoE(Mixture of Experts), 소형화(SLM) 등으로 보완하고 있다. Agentic AI와 결합하여 자율적 작업 수행이 가능한 방향으로 진화 중이다.

---

**관련**: RAG(03번) · 파인튜닝(06번) · 멀티모달(08번) · Agentic AI(11번)
