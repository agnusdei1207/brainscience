+++
weight = 14
title = "14. 빅데이터 플랫폼"
date = "2026-05-17"
[extra]
categories = "gisulsa-bigdata"
+++

# 빅데이터 플랫폼 & 클라우드 빅데이터

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

Glue: 서버리스 ETL, 데이터 카탈로그
EMR: 관리형 Hadoop/Spark 클러스터
Athena: S3 SQL 분석 (서버리스)

### Ⅱ. 핵심 구성요소

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
```
[현대 데이터 플랫폼 (Modern Data Stack)]
수집: Airbyte, Fivetran, Kafka
저장: S3/ADLS (데이터 레이크)
변환: dbt (SQL 기반 ELT)
카탈로그: DataHub, Amundsen
서빙: Redshift, BigQuery


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
