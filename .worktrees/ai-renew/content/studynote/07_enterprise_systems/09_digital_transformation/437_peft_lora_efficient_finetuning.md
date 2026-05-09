+++
weight = 437
title = "437. PEFT LoRA 저차원 가중치 효율적 파인튜닝 (PEFT / LoRA)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PEFT(Parameter-Efficient Fine-Tuning)는 LLM의 전체 파라미터 대신 소수의 추가 파라미터만 학습하여 전체 파인튜닝 대비 메모리·연산 비용을 90%+ 절감하며, LoRA(Low-Rank Adaptation)는 가중치 행렬을 저차원 행렬 곱으로 근사하여 PEFT를 구현하는 가장 대표적 기법이다.
> 2. **가치**: 70B 파라미터 LLM을 전체 파인튜닝하려면 A100 80GB GPU 16개 이상이 필요하지만, LoRA/QLoRA로 단일 A100 또는 RTX 4090 소비자 GPU로도 가능하여 도메인 특화 LLM 개발의 접근성을 극적으로 높였다.
> 3. **판단 포인트**: LoRA rank(r) 값이 낮을수록 파라미터 수·메모리가 줄지만 모델 용량도 감소하므로, 작업 복잡도에 따른 r 값과 알파(α) 하이퍼파라미터 튜닝이 핵심이다.

## Ⅰ. 개요 및 필요성

GPT-4·LLaMA 같은 LLM을 도메인 전용으로 파인튜닝하면 최고 성능을 내지만, 수백억 파라미터를 모두 업데이트하는 Full Fine-tuning은 수백 GB GPU 메모리와 수일의 학습 시간이 필요하다. PEFT는 대부분의 파라미터는 동결(frozen)하고 소수만 학습하여 이 문제를 해결한다. Hu et al.(2021) 의 LoRA 논문은 PEFT 분야의 표준 기법이 됐다.

📢 **섹션 요약 비유**: LoRA는 원본 그림에 작은 덧칠 — 수백억 픽셀(파라미터) 전체를 다시 칠하는 대신, 핵심 부분(저차원 행렬)만 수정하여 새 그림을 완성한다.

## Ⅱ. 아키텍처 및 핵심 원리

```
LoRA 원리:
  기존 가중치 행렬: W₀ (d×k, 동결)
  LoRA 추가 행렬: ΔW = B·A  (B: d×r, A: r×k, r << d,k)
  실제 연산: h = W₀x + ΔWx = W₀x + BAx
  
  파라미터 절감: 원본 d×k → LoRA r×(d+k) (r=8 기준 수백 배 감소)

  예시: LLaMA-2 70B 파인튜닝
    Full Fine-tuning: ~560GB GPU 메모리 (A100×7)
    LoRA (r=16): ~40GB GPU 메모리 (A100×1)
    QLoRA (4bit 양자화 + LoRA): ~20GB (RTX 4090 가능!)

PEFT 기법 비교:
  LoRA  : 저차원 행렬 분해, 빠른 학습
  Prefix Tuning: 입력 앞에 학습 가능 토큰 추가
  Adapter : 레이어 사이 소형 모듈 삽입
  Prompt Tuning: 소프트 프롬프트 벡터 학습
```

| 기법 | 파라미터 비율 | GPU 요건 | 성능 |
|:---|:---|:---|:---|
| Full Fine-tuning | 100% | 매우 높음 | 최고 |
| LoRA | 0.1~1% | 낮음 | Full에 근접 |
| QLoRA | 0.1~1% + 4bit | 최저 | LoRA에 근접 |
| Prefix Tuning | 0.1% | 낮음 | 중간 |

📢 **섹션 요약 비유**: QLoRA는 4배 압축 + 스티커 학습 — 원본 책(LLM)을 4배로 압축(4-bit 양자화)하고, 스티커(LoRA 행렬)만 새로 붙여서 도메인 지식을 추가한다.

## Ⅲ. 비교 및 연결

Merge and Unload: LoRA 학습 후 ΔW를 원본 W₀에 병합하면 추론 시 추가 연산 없음 — 서빙 효율화. DoRA(Weight-Decomposed LoRA): 가중치를 크기와 방향으로 분해하여 LoRA보다 안정적 학습. RLHF(Reinforcement Learning from Human Feedback): 파인튜닝 후 인간 선호도 기반 강화학습으로 정렬(Alignment) 수행.

📢 **섹션 요약 비유**: LoRA Merge는 스티커 영구 부착 — 수정 스티커를 붙인 채로 두는 것보다 원본에 완전히 합치면 더 빠르고 깔끔하다.

## Ⅳ. 실무 적용 및 기술사 판단

**의사결정 포인트**:
- 소비자 GPU로 LLM 파인튜닝: QLoRA (4bit + LoRA) 선택
- 빠른 실험: LoRA rank=16, alpha=32, dropout=0.05 기본값
- 서빙 최적화: LoRA 가중치 병합 후 vLLM 배포
- 오픈소스 생태계: Hugging Face PEFT 라이브러리 (5줄 코드로 LoRA 적용)

📢 **섹션 요약 비유**: Hugging Face PEFT 라이브러리는 LoRA의 간편 도구 — 5줄 코드로 어떤 LLM에도 LoRA 파인튜닝을 적용할 수 있다.

## Ⅴ. 기대효과 및 결론

LoRA/QLoRA는 도메인 특화 LLM 개발의 진입 장벽을 혁신적으로 낮춰 의료·법률·금융 등 전문 도메인의 AI 적용을 가속화한다. 전체 파인튜닝 대비 성능 차이가 최소화되고 있어 PEFT가 엔터프라이즈 LLM의 표준 적응 기법으로 자리매김하고 있다. 장기적으로 PEFT+RAG+프롬프트 엔지니어링의 조합이 최고 비용 효율의 LLM 도메인 적용 방법론이다.

📢 **섹션 요약 비유**: LoRA는 LLM의 개인 맞춤 테일러링 — 기성복(범용 LLM)을 완전히 새로 만드는(Full Fine-tuning) 대신, 핵심 부분만 수선(LoRA)하여 딱 맞는 옷을 만든다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| PEFT | 방법론 카테고리 | 소수 파라미터만 학습하는 파인튜닝 |
| LoRA | 핵심 기법 | 저차원 행렬 분해로 가중치 근사 |
| QLoRA | 효율화 확장 | 4-bit 양자화 + LoRA 결합 |
| RLHF | 정렬 기법 | 인간 선호도 기반 강화학습 |
| Hugging Face PEFT | 구현 라이브러리 | 오픈소스 PEFT 표준 라이브러리 |

### 👶 어린이를 위한 3줄 비유 설명

1. LoRA는 LLM에 스티커 붙이기 — 책 전체를 다시 쓰는 대신, 필요한 페이지에만 수정 스티커(저차원 행렬)를 붙여.
2. QLoRA는 4배 압축 책 + 스티커 — 책을 얇게 압축해서 가방(GPU)에 넣고, 수정 스티커도 함께 달아.
3. r=16은 스티커 크기 설정 — 작은 스티커(r=1)는 빠르지만 정보가 적고, 큰 스티커(r=64)는 느리지만 더 많이 담아!
