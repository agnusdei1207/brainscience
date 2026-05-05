+++
weight = 216
title = "216. 빅데이터 분산 처리 인프라"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++

## 0. 핵심 인사이트

> **핵심**: 빅데이터 분산 처리 인프라의 본질은 하둡 에코시스템 (HDFS, MapReduce 병목) -> 아파치 스파크 (Apache Spark 인메모리 고속 병렬 컴퓨팅)를 비즈니스 가치, 통제, 실행 관점에서 일관되게 연결하는 데 있다.
> **비유**: 대형 프로젝트의 건강 상태를 수치로 읽어 내는 계기판과 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

2000년대 인터넷 서비스 폭발로 구글은 하루 수십억 건의 웹 페이지를 크롤링·색인해야 했다. 단일 서버로는 이 규모를 처리할 수 없어, 구글은 2003년 GFS(Google File System) 논문과 2004년 MapReduce 논문을 발표했다. 이를 오픈소스로 구현한 것이 Doug Cutting이 만든 Apache Hadoop(2006)이다.

하둡은 "100대의 저렴한 PC로 1대의 슈퍼컴퓨터를 대체한다"는 철학으로, 범용 서버에 데이터를 분산 저장하고 데이터가 있는 곳에서 직접 처리(Data Locality)하는 패러다임을 구현했다.

| 구성 요소 | 역할 |
|:---|:---|
| **HDFS** | 분산 파일 시스템. 파일을 128MB 블록으로 분할, 3중 복제 저장 |
| **MapReduce** | 분산 연산 프레임워크. Map(병렬 변환) + Reduce(집계) |
| **YARN** (Yet Another Resource Negotiator) | 클러스터 자원 관리. CPU·메모리 할당 |
| **Hive** | SQL 형태 쿼리를 MapReduce로 변환 (HiveQL) |
| **HBase** | HDFS 위의 NoSQL 컬럼 패밀리 DB |
| **ZooKeeper** | 분산 코디네이션 서비스 |

---

## 2. 구성요소

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

Spark는 MapReduce의 단계 간 디스크 I/O 문제를 **인메모리 RDD**로 해결했다. 중간 결과를 RAM에 보관하여 반복 연산(ML 학습, 그래프 처리)에서 MapReduce 대비 10~100배 성능을 낸다.

| API 레벨 | 설명 | 최적화 |
|:---|:---|:---|
| **RDD** (Resilient Distributed Dataset) | 저수준 불변 분산 컬렉션 | 수동 최적화 필요 |
| **DataFrame** | 스키마 있는 분산 테이블 | Catalyst 옵티마이저 자동 최적화 |
| **Dataset** | 타입 안전 DataFrame (Scala/Java) | 컴파일 타임 타입 검사 |

| 모듈 | 기능 | 활용 |
|:---|:---|:---|
| **Spark Core** | RDD 분산 처리 기반 | 범용 배치 처리 |
| **Spark SQL** | SQL + DataFrame 분석 | 데이터 분석, ETL |
| **Spark Streaming** | DStream/Structured Streaming | 실시간 스트리밍 |
| **MLlib** | 분산 ML 알고리즘 라이브러리 | 대용량 ML 학습 |
| **GraphX** | 분산 그래프 처리 | 소셜 네트워크, 추천 |

---

## 3. 구조 및 원리

| 항목 | Hadoop MapReduce | Apache Spark |
|:---|:---|:---|
| **처리 속도** | 배치 중심, 디스크 I/O로 느림 | 인메모리로 10~100배 빠름 |
| **프로그래밍** | Java 중심, 복잡한 코드 | Python/Scala/R/Java, 간결한 API |
| **처리 유형** | 배치만 지원 | 배치+스트리밍+ML+그래프 통합 |
| **결함 허용** | HDFS 복제, 재시작 | RDD 리니지 기반 재계산 |
| **메모리 요구** | 낮음 | 높음 (인메모리 특성) |
| **활용** | 대용량 배치 ETL | ML, 스트리밍, 반복 연산 |

| 계층 | 역할 | 도구 |
|:---|:---|:---|
| **스토리지** | 분산 파일 시스템 | HDFS, S3, GCS |
| **컴퓨팅** | 분산 처리 엔진 | Spark, Flink, Hive |
| **자원 관리** | 클러스터 자원 조율 | YARN, Kubernetes |
| **오케스트레이션** | 작업 스케줄링·의존성 | Airflow, Oozie |
| **데이터 수집** | 스트리밍 수집 | Kafka, Flume, Sqoop |
| **쿼리** | SQL 인터페이스 | Hive, Presto, Spark SQL |

---

## 4. 비교 및 연결

```python

from pyspark.sql import SparkSession
from pyspark.sql.functions import window, count

spark = SparkSession.builder.appName("RealTimeOrders").getOrCreate()

orders = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .load()

agg = orders.withWatermark("timestamp", "2 minutes") \
    .groupBy(window("timestamp", "1 minute"), "product_id") \
    .agg(count("*").alias("order_count"))

query = agg.writeStream \
    .outputMode("update") \
    .format("snowflake") \
    .start()
```

| 기법 | 설명 | 효과 |
|:---|:---|:---|
| **파티셔닝 (Partitioning)** | 데이터를 균등 분할하여 병렬성 극대화 | CPU 활용률 향상 |
| **캐싱 (Caching)** | 반복 사용 RDD/DataFrame 메모리 캐싱 | 재계산 제거 |
| **브로드캐스트 조인** | 소형 테이블을 모든 노드에 복사 | Shuffle 비용 제거 |
| **Catalyst 옵티마이저** | 쿼리 실행 계획 자동 최적화 | 코드 없이 성능 향상 |
| **Tungsten** | 메모리 관리·코드 생성 JVM 최적화 | JVM GC 부담 감소 |

- **HDFS 3중 복제 원리**: NameNode 역할, DataNode 블록 복제, 장애 복구
- **MapReduce vs Spark 성능 차이 원인**: 디스크 I/O vs 인메모리
- **RDD → DataFrame → Dataset API 진화**: 각 레벨의 특징과 트레이드오프
- **Spark 통합 엔진 모듈**: Spark SQL, MLlib, Streaming, GraphX

---

## 5. 실무 적용 및 판단

| 효과 | 내용 |
|:---|:---|
| **처리 속도** | MapReduce 대비 배치 10배, 인메모리 반복 연산 100배 향상 |
| **통합 플랫폼** | 배치·스트리밍·ML·그래프를 단일 엔진으로 처리 |
| **개발 생산성** | Python/SQL API로 데이터 과학자 직접 활용 가능 |
| **클라우드 네이티브** | EMR, Databricks, GCP Dataproc으로 서버리스 운영 |
| **실시간 확장** | Structured Streaming으로 밀리초 단위 처리 |

Hadoop HDFS는 여전히 대용량 데이터 저장 인프라로 사용되지만, MapReduce는 Spark로 사실상 대체됐다. 클라우드 환경에서는 HDFS 대신 S3/GCS를 스토리지로, Spark를 컴퓨팅 엔진으로, Kubernetes를 자원 관리로 사용하는 클라우드 네이티브 빅데이터 스택이 표준이 되고 있다.

---

## 6. 기대효과 및 결론

빅데이터 분산 처리 인프라를 올바르게 적용하면 의사결정의 일관성, 운영의 재현성, 통제의 추적성이 동시에 향상된다. 즉 “누가 무엇을 왜 했는가”가 남기 때문에 조직이 커질수록 효과가 커진다.

다만 빅데이터 분산 처리 인프라는 문서만 잘 만들어도 성공하는 영역이 아니다. 정의와 실행이 분리되면 형식주의가 되고, 자동화만 앞서면 통제 목적이 사라진다. 따라서 표준화와 민첩성, 통제와 생산성 사이의 균형이 항상 필요하다.

향후에는 정책 코드화(Policy as Code), 실시간 관측성(Observability), AI 기반 이상 탐지와 의사결정 지원이 결합되면서 관리 체계가 더 자동화되고 증거 중심으로 진화할 가능성이 크다. 결론적으로 핵심은 도구가 아니라 기준선이며, 기준선이 명확할 때만 자동화와 확장이 의미를 가진다.

---

## 7. 발전 흐름도

```text
수작업 보고
    ↓
표준 지표 정의
    ↓
빅데이터 분산 처리 인프라 정착
    ↓
대시보드 기반 모니터링
    ↓
예측형 의사결정
```

---

## 8. 관련 개념 맵

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
