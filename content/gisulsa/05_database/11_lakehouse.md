+++
weight = 11
title = "11. 데이터 레이크하우스"
date = "2026-05-17"
[extra]
categories = "gisulsa-database"
+++

# 🎯 데이터 레이크하우스 (Lakehouse)

> **별점**: ★★★★★ | ☆ 2026 확실 예측

## 1. 진화 과정

```
데이터 웨어하우스(DW) → 데이터 레이크 → 레이크하우스

[데이터 웨어하우스 문제]
- 정형 데이터만, 고비용, 비정형 미지원

[데이터 레이크 문제]  
- 스키마 없음, 품질 보장 안됨, "데이터 늪"
- ACID 없음 → 동시 쓰기 시 데이터 불일치

[레이크하우스 해결]
데이터 레이크 위에 DW 기능(ACID, 스키마, 성능) 추가
= 레이크의 유연성 + DW의 신뢰성
```

## 2. 핵심 기술

| 기술 | 주관 | 특징 |
|------|------|------|
| **Delta Lake** | Databricks | ACID, 타임트래블, 스키마 진화 |
| **Apache Iceberg** | Netflix→ASF | 숨겨진 파티션, 스냅샷 격리 |
| **Apache Hudi** | Uber→ASF | 점진적 처리, CDC 지원 |

```
[Delta Lake 핵심 기능]
타임트래블: 과거 데이터 버전 조회 가능
  SELECT * FROM table TIMESTAMP AS OF '2024-01-01'

ACID 트랜잭션:
- 원자적 쓰기 (부분 실패 없음)
- 낙관적 동시성 제어
- 롤백 가능

스키마 강제(Schema Enforcement) + 진화(Evolution)
```

## 3. 아키텍처

```
[레이크하우스 계층]
저장: 클라우드 오브젝트 스토리지 (S3, ADLS)
메타데이터: Delta/Iceberg 트랜잭션 로그
처리: Apache Spark, Databricks, Flink
서빙: BI 도구 (Power BI, Tableau) + ML
```

## 4. 답안 포인트

**3단락**: ① 데이터 웨어하우스→레이크→레이크하우스 진화 → ② Delta Lake ACID·타임트래블 핵심 기능 → ③ Iceberg/Hudi 비교 & 클라우드 적용

## 5. 관련 개념

`데이터 패브릭(★135회)` → 레이크하우스 위의 거버넌스 계층 | `벡터DB(★135회)` → AI용 특화 저장소 | `Spark` → 레이크하우스 처리 엔진
