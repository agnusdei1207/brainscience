+++
weight = 6
title = "06. Hadoop & Spark"
date = "2026-05-17"
[extra]
categories = "gisulsa-bigdata"
+++

# 🎯 Hadoop & Apache Spark

> **별점**: ★★★★★ | 기본 필수

## 1. Hadoop 생태계

```
[Hadoop 핵심 구성]
HDFS (분산 파일시스템):
  블록 단위 분산 저장 (기본 128MB)
  복제 계수 3 → 고가용성
  NameNode (메타데이터) + DataNode (실제 데이터)

YARN (Yet Another Resource Negotiator):
  클러스터 자원 관리
  ResourceManager + NodeManager

MapReduce:
  Map(분산 처리) → Shuffle(정렬) → Reduce(집계)
  배치 처리 특화, 실시간 부적합

[Hadoop 생태계]
Hive: SQL on Hadoop (배치)
HBase: Hadoop 위의 NoSQL (실시간 조회)
Pig: 데이터 흐름 스크립트
Zookeeper: 분산 코디네이션
```

## 2. Apache Spark

```
[Spark vs Hadoop MapReduce]
MapReduce: 디스크 기반 → 느림 (I/O 반복)
Spark: 인메모리 처리 → 100배 빠름

[Spark 핵심 개념]
RDD (Resilient Distributed Dataset):
  불변 분산 데이터셋, 결함 허용
  Transformation (lazy) + Action (실행)

DataFrame & Dataset:
  스키마 있는 분산 데이터
  Catalyst 옵티마이저로 자동 최적화

[Spark 처리 유형]
Spark SQL: 구조적 데이터 SQL 분석
Spark Streaming: 실시간 스트림 (마이크로배치)
Structured Streaming: 진정한 실시간
MLlib: 분산 머신러닝
GraphX: 그래프 처리

[배포 모드]
Standalone, YARN, Kubernetes
```

## 3. 답안 포인트

**3단락**: ① Hadoop 생태계 (HDFS+YARN+MapReduce) → ② Spark 인메모리 처리 & RDD/DataFrame → ③ Spark vs Hadoop 사용 시나리오

## 4. 관련 개념

`레이크하우스(05_db 11번)` → Spark가 핵심 처리 엔진 | `실시간 처리(07번)` → Spark Streaming | `데이터 파이프라인(14_data_eng)` → Spark 기반 ETL
