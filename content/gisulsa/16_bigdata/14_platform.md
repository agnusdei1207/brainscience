+++
weight = 14
title = "14. 빅데이터 플랫폼"
date = "2026-05-17"
[extra]
categories = "gisulsa-bigdata"
+++

# 🎯 빅데이터 플랫폼 & 클라우드 빅데이터

> **별점**: ★★★★★ | 기본 필수

## 1. 클라우드 빅데이터 서비스

```
[AWS]
S3: 데이터 레이크 (무한 저장)
Glue: 서버리스 ETL, 데이터 카탈로그
EMR: 관리형 Hadoop/Spark 클러스터
Kinesis: 실시간 스트리밍
Redshift: 클라우드 DW
Athena: S3 SQL 분석 (서버리스)
SageMaker: ML 플랫폼

[Azure]
Data Lake Storage: 레이크
Synapse Analytics: DW + Spark 통합
Azure Databricks: 레이크하우스
Event Hubs: 실시간 스트리밍
Azure ML: ML 플랫폼

[GCP]
BigQuery: 서버리스 DW (페타바이트)
Dataflow: 배치+스트림 통합
Pub/Sub: 메시지 스트리밍
Vertex AI: ML 플랫폼
```

## 2. 데이터 플랫폼 아키텍처

```
[현대 데이터 플랫폼 (Modern Data Stack)]
수집: Airbyte, Fivetran, Kafka
저장: S3/ADLS (데이터 레이크)
변환: dbt (SQL 기반 ELT)
카탈로그: DataHub, Amundsen
서빙: Redshift, BigQuery
BI: Looker, Tableau
ML: MLflow, SageMaker

[선택 기준]
배치 vs 실시간 요구 → 아키텍처 결정
데이터 볼륨 → 처리 엔진 결정
팀 역량 → 도구 복잡도 결정
비용 → 서버리스 vs 클러스터
```

## 3. 데이터 엔지니어링 핵심

```
dbt (data build tool):
  SQL로 데이터 변환 정의
  테스트, 문서화 자동화
  ELT의 T(변환)를 코드로 관리
  
Airflow (Apache):
  워크플로우 오케스트레이션
  DAG (비순환 방향 그래프)로 파이프라인 정의
  스케줄링, 의존성 관리
```

## 4. 답안 포인트

**3단락**: ① AWS/Azure/GCP 빅데이터 서비스 비교 → ② 현대 데이터 스택(dbt+Airflow+레이크하우스) → ③ 실시간 vs 배치 선택 기준

## 5. 관련 개념

`레이크하우스(05_db 11번)` → 현대 데이터 플랫폼 핵심 | `데이터 메시(★135회)` → 도메인별 플랫폼 분산 | `MLOps(10_ai)` → 데이터 플랫폼 + ML 결합
