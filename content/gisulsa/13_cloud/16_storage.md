+++
weight = 16
title = "16. 클라우드 스토리지"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 클라우드 스토리지 & 데이터 서비스

> 별점: ★★★★☆ | 기본 필수

---

## 답안.

### Ⅰ. 개요

데이터 온도에 따른 자동 스토리지 계층화
핫 (Hot): 자주 접근 → SSD 인스턴스 스토리지
웜 (Warm): 가끔 접근 → S3 Standard

### Ⅱ. 핵심 구성요소

```
데이터 온도에 따른 자동 스토리지 계층화

핫 (Hot): 자주 접근 → SSD 인스턴스 스토리지
웜 (Warm): 가끔 접근 → S3 Standard
쿨 (Cool): 드물게 접근 → S3 Standard-IA
콜드 (Cold): 거의 없음 → S3 Glacier
아카이브: 연간 → S3 Deep Archive

[자동 티어링]
S3 Intelligent-Tiering: 접근 패턴 자동 분석 → 계층 이동
→ 예측 불가 접근 패턴에 비용 최적화
```
```
[RDS (관계형)]
AWS RDS: MySQL, PostgreSQL, Oracle
자동 백업, 멀티-AZ, 읽기 복제본

Aurora: MySQL/PostgreSQL 호환, 5배 성능
  글로벌 데이터베이스: 여러 리전 복제

[NoSQL]
DynamoDB: Key-Value, 서버리스, 단일 자리 ms
DocumentDB: MongoDB 호환
Neptune: 그래프 DB

[분석]
Redshift: 페타바이트 규모 DW
BigQuery: GCP, 서버리스 OLAP
Athena: S3 데이터 바로 SQL (서버리스)


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
