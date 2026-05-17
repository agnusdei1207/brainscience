+++
weight = 15
title = "15. AI 윤리 & 책임AI"
date = "2026-05-17"
[extra]
categories = "gisulsa-bigdata"
+++

# 🎯 AI 윤리 & 책임 AI (Responsible AI)

> **별점**: ★★★★★ | ★133회, ★136회 기출

## 1. AI 윤리 원칙

```
[OECD AI 원칙 (2019)]
포용적 성장 & 지속가능 발전
인간 중심 가치 & 공정성
투명성 & 설명가능성
견고성, 보안, 안전
책임성 (Accountability)

[EU AI 윤리 4원칙 (HLEG)]
공정성 (Fairness)
투명성 (Transparency)
책임 (Accountability)
개인정보보호 (Privacy)
```

## 2. AI 편향 (Bias) & 공정성

```
[편향 유형]
데이터 편향:
  과소 대표성: 특정 그룹 데이터 부족
  역사적 편향: 과거 차별이 데이터에 반영
  측정 편향: 그룹별 다른 기준으로 측정

알고리즘 편향:
  모델이 편향된 상관관계 학습

[편향 측정]
인구통계학적 동등성:
  그룹별 양성 예측률 동일해야 함
등거리 교차:
  그룹 간 FPR/FNR 동일해야 함

공정성 딜레마:
  여러 공정성 기준 동시 만족 불가능
  → 어떤 공정성을 우선할지 사회적 합의 필요
```

## 3. XAI (설명 가능한 AI)

```
[XAI 기법]
SHAP (SHapley Additive exPlanations):
  게임 이론 기반, 특성별 기여도 계산
  정확하지만 계산 비용 큼
  
LIME (Local Interpretable Model-agnostic Explanation):
  예측 주변을 단순 모델로 근사
  
Grad-CAM:
  CNN에서 어떤 영역을 보고 결정했는지 시각화
  이미지 분류 설명

[필요성]
고위험 AI (의료, 금융, 채용): 설명 의무
EU AI법: 고위험 AI 투명성 요구
신뢰: "왜 대출이 거절됐나?" 설명 가능해야 함
```

## 4. 답안 포인트

**3단락**: ① AI 윤리 원칙(OECD/EU) → ② AI 편향 유형 & 공정성 지표 → ③ XAI(SHAP/LIME/GradCAM) & EU AI법 요구

## 5. 관련 개념

`AI 기본법(☆예측)` → 국내 AI 윤리 법제화 | `AI 감리(11_design 14번)` → 편향 검사 감리 | `Agentic AI(★136회)` → 에이전트 AI 윤리 이슈
