+++
weight = 9
title = "09. 데이터 품질 고도화"
date = "2026-05-17"
[extra]
categories = "gisulsa-data-engineering"
+++

# 데이터 품질 & 데이터 계약

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

완전성 (Completeness): 누락 없음 (결측치 없음)
정확성 (Accuracy): 실제 값과 일치
일관성 (Consistency): 여러 시스템 간 동일

### Ⅱ. 핵심 구성요소

```
[ISO 8000 / DAMA DMBOK 기준]
완전성 (Completeness): 누락 없음 (결측치 없음)
정확성 (Accuracy): 실제 값과 일치
일관성 (Consistency): 여러 시스템 간 동일
적시성 (Timeliness): 적절한 시간에 사용 가능
유일성 (Uniqueness): 중복 없음
유효성 (Validity): 형식/범위 준수

[데이터 품질 지표]
결측률 = NULL 수 / 전체 행 수
중복률 = 중복 행 / 전체 행
정확도 = 유효 값 수 / 전체 행 수
```
```
[Great Expectations]
데이터 파이프라인 내 데이터 검증 프레임워크
파이썬 기반 오픈소스

기대값 (Expectation) 예시:
  expect_column_values_to_not_be_null("email")
  expect_column_values_to_be_between("age", 0, 150)
  expect_column_values_to_match_regex("phone", r"010-\d{4}-\d{4}")

[데이터 품질 파이프라인]
데이터 수집 → 검증 (GE) → 실패 시 경보
  → 격리 (Quarantine) → 보고서 (Data Docs)

Soda Core: GE 대안, SQL 기반 테스트
dbt tests: dbt 모델 내 품질 테스트


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
