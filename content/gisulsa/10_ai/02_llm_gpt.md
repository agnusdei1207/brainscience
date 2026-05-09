+++
weight = 2
title = "2. LLM·GPT·트랜스포머 (LLM GPT Transformer)"
date = "2026-05-09"
[extra]
categories = "gisulsa-ai"
+++
# 🎯 핵심 키워드: LLM (Large Language Model), GPT (Generative Pre-trained Transformer), 트랜스포머 (Transformer)

> **출제 빈도**: ★★★★★ | **난이도**: ★★★★☆

## 1. 정의 (Definition)

LLM은 방대한 텍스트를 사전학습하여 언어 이해와 생성 능력을 갖춘 대규모 파라미터 모델이다.  
GPT는 Transformer의 decoder 구조를 활용해 다음 토큰 예측 기반으로 자연스러운 텍스트를 생성하는 대표적인 생성형 모델 계열이다.  
Transformer는 Self-Attention을 통해 장거리 의존성을 병렬 처리하며 현대 자연어처리와 멀티모달 AI의 기반이 되었다.

## 2. 출제 포인트 (Exam Key Points)

| 포인트 | 내용 | 채점 비중 |
|--------|------|----------|
| 정의 | LLM은 방대한 텍스트를 사전학습하여 언어 이해와 생성 능력을 갖춘 대규모 파라미터 모델이다.와 Transformer는 Self-Attention을 통해 장거리 의존성을 병렬 처리하며 현대 자연어처리와 멀티모달 AI의 기반이 되었다.의 인과관계를 한 문장 구조로 묶어 서술한다. | 20% |
| 구성요소 | 사전학습과 파인튜닝, Attention과 Context Window, 환각·비용·정렬(Alignment) 문제를 구조-동작-효과 순으로 정리한다. | 30% |
| 비교/차이 | GPT vs BERT의 선택 기준과 트레이드오프를 비교표로 제시한다. | 30% |
| 적용사례 | 사내 지식 챗봇과 생성형 AI 서비스 구축 관점에서 기대효과와 실패 포인트를 함께 적는다. | 20% |

## 3. 답안 목차 템플릿 (Answer Outline Template)

문제: "LLM과 GPT, Transformer의 개념 및 특징을 설명하시오."

```text
Ⅰ. 개요
   1. 정의
   2. 생성형 AI 수요 폭증

Ⅱ. 핵심 구성요소
   1. 대규모 언어모델 구조
   2. 생성형 모델의 특징과 한계

Ⅲ. 특징 및 장단점
   1. 자연어 인터페이스 혁신과 생산성 향상
   2. 환각, 비용, 데이터 거버넌스 리스크

Ⅳ. 유사 기술과의 비교
   - GPT vs BERT 비교표

Ⅴ. 적용사례 및 향후전망
   1. 사내 지식 챗봇과 생성형 AI 서비스 구축
   2. 소형 언어모델과 멀티모달 모델 경쟁 심화
```

## 4. 핵심 비교표 (Key Comparison Table)

| 구분 | GPT | BERT |
| --- | --- | --- |
| 모델 구조 | Decoder 중심 | Encoder 중심 |
| 주요 목적 | 텍스트 생성 | 이해·분류·표현 학습 |
| 학습 방식 | Auto-regressive | Masked Language Modeling |
| 장점 | 자연스러운 생성 | 문맥 이해와 분류 성능 우수 |
| 시험 포인트 | Generation | Understanding |

## 5. 인출 훈련 문제 (Output Drills)

### 단답형 (30초)
1. LLM (Large Language Model)의 정의를 한 문장으로 쓰시오.
2. LLM·GPT·트랜스포머 답안에서 반드시 써야 할 핵심 구성요소 3가지를 나열하시오.
3. GPT와 BERT의 가장 큰 차이점을 설명하시오.
4. "사전학습, 추론 비용, 환각 리스크를 함께 말하는 연습"를 답안 키워드 3개로 압축하시오.
5. 사내 지식 챗봇과 생성형 AI 서비스 구축 중 하나를 들고 기대효과 2가지를 말하시오.

### 서술형 (5분)
6. "LLM과 GPT, Transformer의 개념 및 특징을 설명하시오."의 핵심 구성요소와 기대효과를 5분 답안으로 정리하시오.
7. "GPT vs BERT"의 선택 기준과 실패 시 발생하는 운영 리스크를 서술하시오.

### 답안 작성 (25분)
8. "LLM과 GPT, Transformer의 개념 및 특징을 설명하시오." (개념, 구조, 비교, 적용사례, 향후전망 포함)

## 6. 면접 예상 질문 (Mock Interview)

Q1: "Transformer의 핵심 혁신은 무엇입니까?"  
Q2: "GPT와 BERT의 차이를 설명해보세요."  
Q3: "기업 환경에서 LLM 도입 시 가장 큰 리스크는 무엇입니까?"
