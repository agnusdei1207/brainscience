+++
weight = 16
title = "16. 클라우드 스토리지"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 🎯 클라우드 스토리지 & 데이터 서비스

> **별점**: ★★★★☆ | 기본 필수

## 1. 클라우드 스토리지 유형

| 유형 | 설명 | 사용 사례 |
|------|------|---------|
| **오브젝트** | S3, GCS (키-값, 비정형) | 이미지, 동영상, 로그 |
| **블록** | EBS, SAN (블록 수준) | OS, DB (빠른 I/O) |
| **파일** | EFS, NFS (파일시스템) | 공유 스토리지, 홈디렉토리 |
| **인메모리** | Redis, ElastiCache | 캐시, 세션 (ms 이하) |
| **아카이브** | S3 Glacier (콜드) | 장기 보관, 저비용 |

## 2. 데이터 티어링 (Data Tiering)

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

## 3. 관리형 데이터베이스 서비스

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
```

## 4. 답안 포인트

**3단락**: ① 클라우드 스토리지 유형 비교 → ② 데이터 티어링 & 비용 최적화 → ③ 관리형 DB 서비스 (RDS/Aurora/NoSQL/분석)

## 5. 관련 개념

`레이크하우스(05_db 11번)` → S3 기반 | `FinOps(09번)` → 스토리지 비용 최적화 | `데이터 분류(14번)` → 엣지→클라우드 스토리지 연계
