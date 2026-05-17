+++
weight = 11
title = "11. 데이터 마이닝"
date = "2026-05-17"
[extra]
categories = "gisulsa-bigdata"
+++

# 🎯 데이터 마이닝 & CRISP-DM

> **별점**: ★★★★★ | 기본 필수

## 1. 데이터 마이닝 기법

```
[분류 (Classification)]
레이블 있는 데이터 학습 → 새 데이터 분류
알고리즘: 의사결정트리, SVM, 랜덤포레스트, XGBoost
예) 이탈 고객 예측, 스팸 분류, 신용 평가

[군집 (Clustering)]
레이블 없이 유사 그룹 발견
알고리즘: K-Means, DBSCAN, 계층적 군집화
예) 고객 세그먼트, 이상 탐지

[연관 규칙 (Association Rules)]
함께 구매되는 아이템 발견
Apriori, FP-Growth
지표:
  지지도(Support) = P(A∩B)
  신뢰도(Confidence) = P(B|A)
  향상도(Lift) = Confidence / P(B)
예) 기저귀 → 맥주 (마트 유명 사례)

[회귀 (Regression)]
연속 값 예측
선형 회귀, 리지, 라쏘, XGBoost
예) 집값 예측, 수요 예측
```

## 2. CRISP-DM (데이터 마이닝 방법론)

```
[6단계 프로세스]
1. 비즈니스 이해 (Business Understanding):
   목표 정의, 성공 기준

2. 데이터 이해 (Data Understanding):
   데이터 수집, EDA (탐색적 분석)

3. 데이터 준비 (Data Preparation):
   정제, 변환, 피처 엔지니어링
   = 전체 작업의 60~80%

4. 모델링 (Modeling):
   알고리즘 선택, 학습, 튜닝

5. 평가 (Evaluation):
   비즈니스 목표 달성 여부
   정확도, F1, ROC-AUC

6. 배포 (Deployment):
   운영 환경 적용, 모니터링
```

## 3. 답안 포인트

**3단락**: ① 데이터 마이닝 4대 기법 → ② CRISP-DM 6단계 & 데이터 준비 중요성 → ③ 연관 규칙(지지도/신뢰도/향상도)

## 4. 관련 개념

`ML(10_ai)` → 데이터 마이닝의 ML 확장 | `분석 4단계(08번)` → 마이닝은 예측 분석에 해당 | `데이터 품질(05_db 14번)` → 마이닝 전 필수 준비
