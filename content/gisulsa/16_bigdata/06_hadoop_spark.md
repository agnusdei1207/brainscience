+++
weight = 6
title = "06. Hadoop & Spark"
date = "2026-05-17"
[extra]
categories = "gisulsa-bigdata"
+++

# Hadoop & Apache Spark

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

  블록 단위 분산 저장 (기본 128MB)
  NameNode (메타데이터) + DataNode (실제 데이터)
YARN (Yet Another Resource Negotiator):

### Ⅱ. 핵심 구성요소

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
```
[Spark vs Hadoop MapReduce]
MapReduce: 디스크 기반 → 느림 (I/O 반복)
Spark: 인메모리 처리 → 100배 빠름

[Spark 핵심 개념]
RDD (Resilient Distributed Dataset):
  불변 분산 데이터셋, 결함 허용
  Transformation (lazy) + Action (실행)


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
