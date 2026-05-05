+++
weight = 216
title = "216. 빅데이터 분산처리 - 하둡/스파크 (Hadoop & Spark)"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++
## 0. 핵심 인사이트

> **핵심**: Hadoop은 HDFS(Hadoop Distributed File System, 하둡 분산 파일 시스템)와 MapReduce로 수천 대 범용 서버에 페타바이트 데이터를 분산 저장·처리하는 빅데이터 기반 프레임워크이며, Apache Spark는 인메모리(In-memory) 분산 컴퓨팅으로 MapReduce 대비 최대 100배 빠른 처리를 실현한다.
> 2. **가치**: RDD(Resilient Distributed Dataset, 탄력적 분산 데이터셋)→DataFrame→Dataset API의 진화는 사용 편의성과 최적화를 동시에 달성했으며, Spark의 통합 엔진(배치·스트리밍·ML·그래프)은 단일 플랫폼에서 모든 빅데이터 워크로드를 처리한다.
> 3. **판단 포인트**: MapReduce는 디스크 I/O 기반으로 반복 연산에 부적합하므로, ML·그래프·스트리밍 처리는 Spark를 사용하고, Hadoop 생태계(HDFS, YARN, Hive)는 Spark의 인프라로 활용하는 것이 현대 빅데이터 아키텍처의 표준이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 1.1 빅데이터 처리의 도전
2000년대 인터넷 서비스 폭발로 구글은 하루 수십억 건의 웹 페이지를 크롤링·색인해야 했다. 단일 서버로는 이 규모를 처리할 수 없어, 구글은 2003년 GFS(Google File System) 논문과 2004년 MapReduce 논문을 발표했다. 이를 오픈소스로 구현한 것이 Doug Cutting이 만든 Apache Hadoop(2006)이다.

하둡은 "100대의 저렴한 PC로 1대의 슈퍼컴퓨터를 대체한다"는 철학으로, 범용 서버에 데이터를 분산 저장하고 데이터가 있는 곳에서 직접 처리(Data Locality)하는 패러다임을 구현했다.

### 1.2 Hadoop 핵심 구성 요소

| 구성 요소 | 역할 |
|:---|:---|
| **HDFS** | 분산 파일 시스템. 파일을 128MB 블록으로 분할, 3중 복제 저장 |
| **MapReduce** | 분산 연산 프레임워크. Map(병렬 변환) + Reduce(집계) |
| **YARN** (Yet Another Resource Negotiator) | 클러스터 자원 관리. CPU·메모리 할당 |
| **Hive** | SQL 형태 쿼리를 MapReduce로 변환 (HiveQL) |
| **HBase** | HDFS 위의 NoSQL 컬럼 패밀리 DB |
| **ZooKeeper** | 분산 코디네이션 서비스 |

📢 **섹션 요약 비유**: Hadoop 클러스터는 거대한 개미 군집이다. 여왕개미(NameNode)가 먹이(데이터) 위치를 기억하고, 수백만 일개미(DataNode)가 각자 맡은 구역에서 동시에 먹이를 수집·운반한다. 한 마리 개미가 죽어도(노드 장애) 군집은 멈추지 않는다.

---

## 2. 구성요소

### 2.1 HDFS와 MapReduce 처리 흐름

```
┌─────────────────────────────────────────────────────────────┐
│           Hadoop HDFS + MapReduce Architecture              │
│                                                             │
│  HDFS 저장 구조:                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  NameNode (메타데이터 관리)                           │  │
│  │  - 파일명, 블록 위치, 복제 정보 관리                  │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                         │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │ DataNode-1  │ DataNode-2  │ DataNode-3  │ DataNode-4 │  │
│  │ [Block A-1] │ [Block A-2] │ [Block A-1] │ [Block B-1]│  │
│  │ [Block B-2] │ [Block A-3] │ [Block B-3] │ [Block A-2]│  │
│  └──────────────────────────────────────────────────────┘  │
│                   복제 계수: 3 (기본값)                      │
│                                                             │
│  MapReduce 처리 흐름:                                       │
│  ┌─────────┐  Map  ┌──────────┐ Shuffle ┌──────────────┐  │
│  │ Input   │──────►│ Mapper   │────────►│ Reducer      │  │
│  │ Splits  │       │ (병렬)   │ Sort    │ (집계)       │  │
│  │(HDFS블록)│       │ K,V 출력 │         │ 최종 결과    │  │
│  └─────────┘       └──────────┘         └──────────────┘  │
│                                                             │
│  ※ 각 Map/Reduce 단계 사이에 디스크 I/O 발생 → 속도 한계  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Apache Spark 인메모리 처리 원리

Spark는 MapReduce의 단계 간 디스크 I/O 문제를 **인메모리 RDD**로 해결했다. 중간 결과를 RAM에 보관하여 반복 연산(ML 학습, 그래프 처리)에서 MapReduce 대비 10~100배 성능을 낸다.

| API 레벨 | 설명 | 최적화 |
|:---|:---|:---|
| **RDD** (Resilient Distributed Dataset) | 저수준 불변 분산 컬렉션 | 수동 최적화 필요 |
| **DataFrame** | 스키마 있는 분산 테이블 | Catalyst 옵티마이저 자동 최적화 |
| **Dataset** | 타입 안전 DataFrame (Scala/Java) | 컴파일 타임 타입 검사 |

### 2.3 Spark 통합 엔진 아키텍처

| 모듈 | 기능 | 활용 |
|:---|:---|:---|
| **Spark Core** | RDD 분산 처리 기반 | 범용 배치 처리 |
| **Spark SQL** | SQL + DataFrame 분석 | 데이터 분석, ETL |
| **Spark Streaming** | DStream/Structured Streaming | 실시간 스트리밍 |
| **MLlib** | 분산 ML 알고리즘 라이브러리 | 대용량 ML 학습 |
| **GraphX** | 분산 그래프 처리 | 소셜 네트워크, 추천 |

📢 **섹션 요약 비유**: MapReduce는 도서관에서 책을 찾을 때마다 서고에서 꺼내 책상에 놓고 읽은 뒤 다시 서고에 반납하는 방식(디스크 I/O)이고, Spark는 자주 보는 책들을 모두 책상 위에 펼쳐두고(인메모리) 빠르게 오가며 읽는 방식이다.

---

## 3. 구조 및 동작 원리

### 3.1 Hadoop MapReduce vs Apache Spark

| 항목 | Hadoop MapReduce | Apache Spark |
|:---|:---|:---|
| **처리 속도** | 배치 중심, 디스크 I/O로 느림 | 인메모리로 10~100배 빠름 |
| **프로그래밍** | Java 중심, 복잡한 코드 | Python/Scala/R/Java, 간결한 API |
| **처리 유형** | 배치만 지원 | 배치+스트리밍+ML+그래프 통합 |
| **결함 허용** | HDFS 복제, 재시작 | RDD 리니지 기반 재계산 |
| **메모리 요구** | 낮음 | 높음 (인메모리 특성) |
| **활용** | 대용량 배치 ETL | ML, 스트리밍, 반복 연산 |

### 3.2 현대 빅데이터 아키텍처 스택

| 계층 | 역할 | 도구 |
|:---|:---|:---|
| **스토리지** | 분산 파일 시스템 | HDFS, S3, GCS |
| **컴퓨팅** | 분산 처리 엔진 | Spark, Flink, Hive |
| **자원 관리** | 클러스터 자원 조율 | YARN, Kubernetes |
| **오케스트레이션** | 작업 스케줄링·의존성 | Airflow, Oozie |
| **데이터 수집** | 스트리밍 수집 | Kafka, Flume, Sqoop |
| **쿼리** | SQL 인터페이스 | Hive, Presto, Spark SQL |

📢 **섹션 요약 비유**: Hadoop 생태계는 거대한 도시 인프라와 같다. HDFS는 도로망, MapReduce/Spark는 대중교통 시스템, YARN은 교통 관제 센터, Kafka는 물류 허브, Hive는 GPS 네비게이션이다. 각 구성 요소가 역할을 분담하며 페타바이트 도시를 운영한다.

---

## 4. 비교 및 트레이드오프

### 4.1 Spark Structured Streaming 예시

```python
# Kafka → Spark Streaming → 실시간 집계
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, count

spark = SparkSession.builder.appName("RealTimeOrders").getOrCreate()

# Kafka에서 실시간 주문 스트림 읽기
orders = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .load()

# 1분 윈도우별 주문 수 집계
agg = orders.withWatermark("timestamp", "2 minutes") \
    .groupBy(window("timestamp", "1 minute"), "product_id") \
    .agg(count("*").alias("order_count"))

# 결과 Snowflake에 저장
query = agg.writeStream \
    .outputMode("update") \
    .format("snowflake") \
    .start()
```

### 4.2 성능 최적화 핵심 기법

| 기법 | 설명 | 효과 |
|:---|:---|:---|
| **파티셔닝 (Partitioning)** | 데이터를 균등 분할하여 병렬성 극대화 | CPU 활용률 향상 |
| **캐싱 (Caching)** | 반복 사용 RDD/DataFrame 메모리 캐싱 | 재계산 제거 |
| **브로드캐스트 조인** | 소형 테이블을 모든 노드에 복사 | Shuffle 비용 제거 |
| **Catalyst 옵티마이저** | 쿼리 실행 계획 자동 최적화 | 코드 없이 성능 향상 |
| **Tungsten** | 메모리 관리·코드 생성 JVM 최적화 | JVM GC 부담 감소 |

### 4.3 기술사 핵심 출제 포인트
- **HDFS 3중 복제 원리**: NameNode 역할, DataNode 블록 복제, 장애 복구
- **MapReduce vs Spark 성능 차이 원인**: 디스크 I/O vs 인메모리
- **RDD → DataFrame → Dataset API 진화**: 각 레벨의 특징과 트레이드오프
- **Spark 통합 엔진 모듈**: Spark SQL, MLlib, Streaming, GraphX

📢 **섹션 요약 비유**: Spark Catalyst 옵티마이저는 내비게이션 AI와 같다. 목적지(결과)가 같더라도 "현재 교통 상황과 도로 구조를 분석해 가장 빠른 경로"를 자동으로 계산한다. 개발자가 최적 경로를 일일이 지정하지 않아도, AI가 항상 최단 경로를 찾는다.

---

## 5. 실무 적용 및 최적화 기법

### 5.1 Spark 도입 효과

| 효과 | 내용 |
|:---|:---|
| **처리 속도** | MapReduce 대비 배치 10배, 인메모리 반복 연산 100배 향상 |
| **통합 플랫폼** | 배치·스트리밍·ML·그래프를 단일 엔진으로 처리 |
| **개발 생산성** | Python/SQL API로 데이터 과학자 직접 활용 가능 |
| **클라우드 네이티브** | EMR, Databricks, GCP Dataproc으로 서버리스 운영 |
| **실시간 확장** | Structured Streaming으로 밀리초 단위 처리 |

### 5.2 Hadoop vs Spark 공존 현황
Hadoop HDFS는 여전히 대용량 데이터 저장 인프라로 사용되지만, MapReduce는 Spark로 사실상 대체됐다. 클라우드 환경에서는 HDFS 대신 S3/GCS를 스토리지로, Spark를 컴퓨팅 엔진으로, Kubernetes를 자원 관리로 사용하는 클라우드 네이티브 빅데이터 스택이 표준이 되고 있다.

📢 **섹션 요약 비유**: Hadoop은 도시의 기반 인프라(도로·수도·전기)고, Spark는 그 위를 달리는 전기차다. 전기차(Spark)가 압도적으로 빠르고 효율적이지만, 도로 인프라(HDFS)가 있어야 달릴 수 있다. 클라우드 시대에는 도로도 임대(S3/GCS)하고, 전기차(Spark)만 직접 운영하는 방식이 대세다.

---

### 📌 관련 개념 맵

| 개념 | 설명 | 연관 키워드 |
|:---|:---|:---|
| HDFS | 하둡 분산 파일 시스템, 블록 복제 저장 | NameNode, DataNode, 3중 복제 |
| MapReduce | Map(병렬 변환) + Reduce(집계) 분산 연산 | 디스크 I/O, 배치 처리 |
| Apache Spark | 인메모리 분산 처리 엔진 | RDD, DataFrame, MLlib |
| RDD (Resilient Distributed Dataset) | Spark 핵심 분산 데이터 추상화 | 불변성, 리니지, 재계산 |
| Catalyst Optimizer | Spark SQL 쿼리 자동 최적화 엔진 | 실행 계획, 코드 생성 |
| YARN (Yet Another Resource Negotiator) | 하둡 클러스터 자원 관리 | 컨테이너, AM, NM |
| Databricks | Spark 기반 통합 분석 플랫폼 | Delta Lake, MLflow |
| Data Locality | 데이터 있는 곳에서 연산 수행 원칙 | 네트워크 I/O 최소화 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. HDFS는 커다란 책을 여러 조각으로 나눠 여러 친구 집에 보관하는 방식이야. 한 집에 불이 나도(노드 장애) 다른 집에 같은 조각이 있어서(3중 복제) 책을 잃어버리지 않아.
2. MapReduce는 운동회 줄넘기 기록을 반 별로 세고(Map), 마지막에 전체 합산하는(Reduce) 방식이야. 그런데 매 단계마다 칠판에 쓰고 지우는(디스크 I/O) 시간이 걸려서 느려.
3. Spark는 칠판 대신 각 팀이 기억(메모리)으로 중간 결과를 가지고 있어서, 마지막에 딱 한 번만 칠판에 적는(디스크 저장) 방식이라 훨씬 빠르고 ML 같은 반복 연산에 강해.
