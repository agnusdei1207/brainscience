+++
weight = 211
title = "211. 하둡 에코시스템 (Hadoop Ecosystem)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: 하둡(Hadoop)은 단일 서버 한계를 넘기 위해 수천 대의 범용 서버에 데이터를 분산 저장(HDFS)하고 분산 처리(MapReduce)하는 오픈소스 프레임워크로, Apache Software Foundation(ASF)의 핵심 프로젝트다.
> **비유**: 하둡은 대형 마트의 물류 시스템과 같다. 상품(데이터)을 하나의 거대한 창고(단일 서버)에 모두 넣는 대신, 수천 개의 작은 창고(분산 서버)에 나눠서 보관하고, 창고 목록(HDFS NameNode)을 중앙에서 관리한다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

하둡은 2006년 Doug Cutting과 Mike Cafarella가 구글의 두 논문(GFS: Google File System, 2003; MapReduce, 2004)을 영감받아 개발했다. 이름의 유래는 Cutting의 아들이 노란 코끼리 장난감에 붙인 이름이다.

하둡의 탄생 배경은 2000년대 웹 크롤러 데이터 문제였다. Yahoo!, Amazon 같은 회사들이 수십~수백 TB의 웹 데이터를 처리해야 했지만, 당시 단일 서버로는 불가능했다. 수천 대의 범용(Commodity) 서버를 네트워크로 연결하여 분산 처리하면 된다는 아이디어가 하둡이었다.

핵심 철학: **하드웨어는 반드시 고장 난다(Hardware Failure is the Norm).** 수천 대 서버 중 일부가 항상 고장 상태이므로, 데이터를 여러 노드에 복제(기본 3벌)하여 하드웨어 고장을 소프트웨어로 투명하게 처리한다.

---

## 2. 구성요소

### 하둡 에코시스템 구조도

```
  ┌────────────────────────────────────────────────────────────┐
  │                  하둡 에코시스템                              │
  ├────────────────────────────────────────────────────────────┤
  │  쿼리/SQL     │  Hive   │  Pig   │  Spark SQL │  Presto   │
  ├────────────────────────────────────────────────────────────┤
  │  처리 엔진    │  MapReduce    │  Apache Spark    │  Flink   │
  ├────────────────────────────────────────────────────────────┤
  │  리소스 관리  │              YARN                           │
  ├────────────────────────────────────────────────────────────┤
  │  분산 저장    │              HDFS                           │
  ├────────────────────────────────────────────────────────────┤
  │  NoSQL DB     │  HBase   │  Cassandra                      │
  ├────────────────────────────────────────────────────────────┤
  │  스트리밍     │  Kafka   │  Flume   │  Spark Streaming     │
  ├────────────────────────────────────────────────────────────┤
  │  데이터 수집  │  Sqoop (RDB ↔ HDFS)  │  Flume (로그)       │
  ├────────────────────────────────────────────────────────────┤
  │  조율/관리    │  ZooKeeper │  Oozie (워크플로우)             │
  └────────────────────────────────────────────────────────────┘
```

### 핵심 컴포넌트 역할

| 컴포넌트 | 역할 |
|:---|:---|
| **HDFS** | Hadoop Distributed File System — 분산 파일 저장 |
| **MapReduce** | 분산 병렬 연산 프레임워크 |
| **YARN** | Yet Another Resource Negotiator — 클러스터 자원 관리 |
| **Hive** | HDFS 데이터에 SQL 쿼리 제공 (SQL-on-Hadoop) |
| **Pig** | 데이터 변환·분석 스크립트 언어 (Pig Latin) |
| **HBase** | 하둡 위의 NoSQL 칼럼 기반 분산 DB (Bigtable 영감) |
| **Spark** | 메모리 기반 고속 처리 엔진 (MapReduce 대체) |
| **ZooKeeper** | 분산 시스템 코디네이션 (설정 공유, 리더 선출) |
| **Sqoop** | RDBMS ↔ HDFS 양방향 데이터 전송 |
| **Oozie** | Hadoop 워크플로우 스케줄러 |

---

## 3. 구조 및 원리

**핵심 조건**: 변경 자동화와 운영 안정성은 별개가 아니라 하나의 루프이며, 빌드·검증·배포·관측·피드백이 끊기지 않아야 지속 개선이 가능하다.

동작 순서:
1. 변경 사항을 버전 관리 시스템에서 감지한다.
2. 빌드·테스트·보안 검증으로 변경의 품질을 빠르게 확인한다.
3. 승인된 산출물을 선언형 배포나 자동화 파이프라인으로 운영 환경에 반영한다.
4. 메트릭·로그·트레이스를 통해 실제 동작 결과를 관측한다.
5. 피드백을 다음 개선 주기에 연결해 반복적으로 신뢰성을 높인다.

### 하둡 vs 기존 RDBMS

| 항목 | RDBMS | 하둡 |
|:---|:---|:---|
| 스케일 | 수직 확장 (Scale-Up) | 수평 확장 (Scale-Out) |
| 데이터 유형 | 정형 (Structured) | 정형 + 반정형 + 비정형 |
| 스키마 | 사전 정의 (Schema-on-Write) | 사후 정의 (Schema-on-Read) |
| 비용 | 고가 서버 | 저가 범용 서버 |
| 처리 속도 | 빠른 트랜잭션 | 대규모 배치 (느린 응답) |
| ACID | ✅ 완전 지원 | ❌ 제한적 |

### 하둡 버전 진화

| 버전 | 특징 |
|:---:|:---|
| Hadoop 1.x | JobTracker + TaskTracker (단일 장애 지점 존재) |
| Hadoop 2.x | YARN 도입 (리소스 분리), HDFS HA 추가 |
| Hadoop 3.x | Erasure Coding(저장 효율↑), 서비스 성숙 |

---

## 4. 비교 및 연결

**클라우드에서의 하둡 사용 (AWS EMR)**:
```
# AWS EMR 클러스터 생성 (최소 구성)
aws emr create-cluster \
  --name "MyHadoopCluster" \
  --release-label emr-6.10.0 \
  --applications Name=Hadoop Name=Spark Name=Hive \
  --instance-type m5.xlarge \
  --instance-count 3 \
  --use-default-roles

# 스팟 인스턴스로 비용 절약
# 핵심 마스터 노드: On-Demand, 워커 노드: Spot
```

**Hive SQL 예시**:
```sql
-- HDFS의 CSV 파일에 SQL 쿼리
CREATE EXTERNAL TABLE sales (
  date STRING,
  product_id INT,
  amount DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 's3://mybucket/sales/';

SELECT product_id, SUM(amount) as total
FROM sales
WHERE date >= '2026-01-01'
GROUP BY product_id
ORDER BY total DESC;
```

**기술사 판단 포인트**:
- 현대 클라우드 환경에서 하둡 직접 운영보다 EMR/Dataproc 관리형 서비스 사용이 TCO(총소유비용) 관점에서 유리하다.
- HDFS vs S3 + Spark 아키텍처: 클라우드에서는 HDFS를 S3로 대체하고 Spark를 독립 실행하는 "S3 중심 아키텍처"가 운영 효율이 높다.
- HBase의 경우 AWS DynamoDB, GCP Bigtable 같은 클라우드 관리형 서비스로 대체되는 추세다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 설명 |
|:---|:---|
| 수평 확장 | 서버 추가만으로 처리 용량 선형 확장 |
| 저비용 인프라 | 고가 전용 서버 없이 범용 서버로 구성 |
| 유연한 데이터 | 정형·비정형 모든 데이터 처리 가능 |
| 내결함성 | 3벌 복제로 하드웨어 고장을 투명하게 처리 |

하둡 에코시스템은 빅데이터 시대를 연 기반 기술이다. 직접 운영은 줄었지만, 클라우드 관리형 서비스(EMR, Dataproc)와 Apache Spark가 하둡의 핵심 아이디어를 계승하여 현재도 대규모 데이터 처리의 표준이다.

---

## 6. 기대효과 및 결론

하둡 에코시스템 (Hadoop Ecosystem)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 하둡 에코시스템 (Hadoop Ecosystem)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
Hadoop 1.0: HDFS + MapReduce (일체형)
    │
    ▼
Hadoop 2.0: YARN 분리 → 다양한 처리 엔진 지원
    │
    ▼
Hadoop 3.0: Erasure Coding + GPU 지원 → 클라우드 최적화
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| HDFS | 하둡 분산 파일 시스템, 빅데이터 저장의 토대 |
| MapReduce | 하둡 1세대 분산 처리 엔진, 스파크로 대체 중 |
| YARN | 하둡 2.x의 범용 리소스 관리자 |
| Apache Spark | 하둡 MapReduce의 후계자, 메모리 기반 고속 처리 |
| AWS EMR | 클라우드 관리형 하둡/스파크 서비스 |
| 구글 GFS/BigTable | 하둡/HBase의 영감이 된 구글 논문 |

---
