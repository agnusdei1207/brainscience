+++
weight = 9
title = "09. 데이터 품질 고도화"
date = "2026-05-17"
[extra]
categories = "gisulsa-data-engineering"
+++

# 🎯 데이터 품질 & 데이터 계약

> **별점**: ★★★★★ | 기본 필수

## 1. 데이터 품질 6대 차원

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

## 2. Great Expectations & 데이터 검증

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
```

## 3. 데이터 계약 (Data Contracts)

```
정의: 데이터 생산자와 소비자 간의 명시적 합의
     데이터의 형식, 의미, SLA를 정의

[데이터 계약 내용]
스키마: 컬럼명, 타입, 제약조건
SLA: 배송 지연 허용 시간, 가용성
의미: 컬럼 설명, 비즈니스 규칙
버전: 하위 호환성 정책

[데이터 계약 생명주기]
생산자 정의 → 소비자 검토 → 합의
→ 모니터링 (실제 데이터 vs 계약 검증)
→ 위반 시 알림

도구: OpenDataContract, Soda, Atlan
→ 데이터 메시의 핵심 운영 요소
```

## 4. 답안 포인트

**3단락**: ① 데이터 품질 6대 차원 & 측정 지표 → ② Great Expectations 검증 파이프라인 → ③ 데이터 계약 & 데이터 메시 연계

## 5. 관련 개념

`데이터 메시(08번)` → 데이터 계약 = 메시의 계약 | `데이터 거버넌스(16_bigdata)` → 품질 정책 | `Airflow(01번)` → 파이프라인에 GE 통합
