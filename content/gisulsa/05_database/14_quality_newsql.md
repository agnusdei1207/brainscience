+++
weight = 14
title = "14. 데이터 품질 관리"
date = "2026-05-17"
[extra]
categories = "gisulsa-database"
+++

# 🎯 데이터 품질 관리 & NewSQL

> **별점**: ★★★★☆ | 기본 필수

## 1. 데이터 품질 6대 차원

| 차원 | 정의 | 측정 예 |
|------|------|--------|
| **완전성** | 필수 값 누락 없음 | NULL 비율 |
| **정확성** | 실제 값과 일치 | 오류 레코드 비율 |
| **일관성** | 시스템 간 동일한 값 | 중복 모순 건수 |
| **적시성** | 최신 데이터 반영 | 데이터 지연 시간 |
| **유일성** | 중복 없음 | 중복 키 비율 |
| **유효성** | 정의된 형식·범위 준수 | 형식 오류 비율 |

## 2. 데이터 품질 관리 프로세스

```
[데이터 품질 관리 사이클]
① 프로파일링: 현황 파악 (NULL, 중복, 분포)
② 규칙 정의: 품질 기준 수립 (사업 규칙)
③ 측정: 지표 자동 측정 (DQ 대시보드)
④ 개선: 원인 분석 → 소스 시스템 수정
⑤ 모니터링: 지속적 품질 감시

도구: AWS Glue DataBrew, Great Expectations,
     Informatica DQ, Talend Data Quality
```

## 3. NewSQL

```
정의: ACID 보장 + 수평 확장의 결합
→ RDB의 일관성 + NoSQL의 확장성

특징:
- SQL 인터페이스 유지 (기존 앱 호환)
- 분산 트랜잭션 ACID 보장
- 자동 샤딩 + 복제

대표 제품:
- CockroachDB: PostgreSQL 호환, 자동 분산
- TiDB: MySQL 호환, HTAP (OLTP+OLAP)
- Google Spanner: 글로벌 분산, TrueTime
- YugabyteDB: PostgreSQL 호환, 오픈소스

적합 용도:
- 금융 결제 (전 세계 ACID)
- 글로벌 재고 관리
```

## 4. 답안 포인트

**3단락**: ① 데이터 품질 6차원 정의 → ② 품질 관리 프로세스(프로파일링→측정→개선) → ③ NewSQL(CockroachDB, TiDB) 등장 배경

## 5. 관련 개념

`CAP 정리(★134회)` → NewSQL은 CP 달성 시도 | `분산 트랜잭션(★132회)` → NewSQL 분산 ACID | `데이터 거버넌스` → 품질 관리 프레임워크
