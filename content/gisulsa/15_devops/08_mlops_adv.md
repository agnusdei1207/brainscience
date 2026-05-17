+++
weight = 8
title = "08. 피처 스토어 & MLOps 고도화"
date = "2026-05-17"
[extra]
categories = "gisulsa-devops"
+++

# 피처 스토어 & MLOps 고도화

> 별점: ★★★★★ | ★136회 연계

---

## 답안.

### Ⅰ. 개요

정의: ML 모델에 사용되는 피처(특성)를 저장·관리·
Training-Serving Skew:
오프라인 스토어: Parquet, S3 (학습용 배치)

### Ⅱ. 핵심 구성요소

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
```
[드리프트 유형]
데이터 드리프트 (Data Drift):
  입력 데이터 분포 변화
  예) 코로나 → 사용자 행동 패턴 급변

개념 드리프트 (Concept Drift):


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
