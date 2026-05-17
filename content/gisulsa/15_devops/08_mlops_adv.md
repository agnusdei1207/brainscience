+++
weight = 8
title = "08. 피처 스토어 & MLOps 고도화"
date = "2026-05-17"
[extra]
categories = "gisulsa-devops"
+++

# 🎯 피처 스토어 & MLOps 고도화

> **별점**: ★★★★★ | ★136회 연계

## 1. 피처 스토어 (Feature Store)

```
정의: ML 모델에 사용되는 피처(특성)를 저장·관리·
     재사용하는 중앙 저장소

[문제 해결]
Training-Serving Skew:
  학습: 과거 데이터로 피처 계산
  서빙: 실시간 피처 계산
  → 로직 차이로 성능 저하

피처 중복:
  각 팀이 같은 피처를 다르게 계산

[피처 스토어 구성]
오프라인 스토어: Parquet, S3 (학습용 배치)
온라인 스토어: Redis, DynamoDB (추론용 실시간)
피처 레지스트리: 메타데이터, 버전, 소유자

[도구]
Feast (오픈소스), Tecton, Hopsworks
AWS SageMaker Feature Store
Databricks Feature Store
```

## 2. 모델 모니터링 & 드리프트

```
[드리프트 유형]
데이터 드리프트 (Data Drift):
  입력 데이터 분포 변화
  예) 코로나 → 사용자 행동 패턴 급변

개념 드리프트 (Concept Drift):
  입력-출력 관계 변화 (더 심각)
  예) 경제 변화 → 신용 점수 모델 부정확

[모니터링 방법]
분포 비교: PSI (Population Stability Index)
          KL 발산, Wasserstein 거리
성능 모니터링: 정확도, F1 추적
슈도 레이블: 예측값 vs 실제값 지연 수집

[자동 재학습]
드리프트 탐지 → 자동 파이프라인 트리거
CI/CD for ML = CML (Continuous ML)
```

## 3. LLMOps

```
[LLMOps = MLOps + LLM 특화]
프롬프트 관리: 버전 관리, A/B 테스트
평가 파이프라인:
  LLM-as-Judge: GPT-4로 출력 평가
  RAGAS: RAG 시스템 평가 프레임워크
파인튜닝 파이프라인: LoRA → 평가 → 배포
비용 모니터링: 토큰 사용량 추적

[LLMOps 도구]
LangSmith (LangChain), Weights & Biases
Phoenix (Arize), Helicone
```

## 4. 답안 포인트

**3단락**: ① 피처 스토어 필요성 & 오프라인/온라인 구성 → ② 데이터/개념 드리프트 & PSI 탐지 → ③ LLMOps & 프롬프트/평가 관리

## 5. 관련 개념

`MLOps(10_ai 04번)` → MLOps 기반 개념 | `LLM(10_ai 02번)` → LLMOps 대상 | `데이터 파이프라인(14_de)` → 피처 생성 파이프라인
