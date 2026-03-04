+++
title = "Hadoop 에코시스템 심층 분석 (HDFS, YARN, MapReduce)"
date = 2024-05-20
description = "분산 컴퓨팅의 초석인 하둡(Hadoop) 아키텍처, 데이터 저장(HDFS), 자원 관리(YARN), 분산 처리(MapReduce)의 내부 동작 원리와 최신 데이터 레이크 전략"
weight = 10
[taxonomies]
categories = ["studynotes-bigdata"]
tags = ["Hadoop", "HDFS", "YARN", "MapReduce", "BigData", "Distributed-Computing"]
+++

# Hadoop 에코시스템 심층 분석 (HDFS, YARN, MapReduce)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 저가형 서버(Commodity Hardware)를 클러스터로 구성하여 페타바이트급 데이터를 신뢰성 있게 저장(HDFS)하고, 병렬로 처리(MapReduce)하며, 클러스터 자원을 효율적으로 관리(YARN)하는 분산 플랫폼입니다.
> 2. **가치**: 데이터 이동 대신 연산 이동(Moving Computation to Data) 패러다임을 통해 네트워크 병목을 최소화하고, 단일 서버의 한계를 넘어선 무한한 수평적 확장성(Scale-out)을 제공합니다.
> 3. **융합**: 현대 데이터 플랫폼에서 Hadoop은 독자적 실행을 넘어 Spark, Kafka, Presto 등과 결합된 하이브리드 데이터 레이크(Data Lake)의 견고한 스토리지 계층으로서 핵심 역할을 지속하고 있습니다.

---

## Ⅰ. 개요 (Context & Background)

Hadoop은 2000년대 초반 구글이 발표한 GFS(Google File System)와 MapReduce 논문을 오픈소스로 구현한 프로젝트로, '빅데이터' 시대의 개막을 알린 상징적 기술입니다. 대용량 데이터를 처리하기 위해 슈퍼컴퓨터를 도입하는 대신, 수천 대의 일반 PC를 연결하여 하나의 거대한 가상 컴퓨터처럼 활용하는 접근 방식을 제안했습니다. Hadoop의 핵심 철학은 **"실패를 상수로 가정하는 것"**입니다. 개별 서버의 장애가 전체 시스템의 정지로 이어지지 않도록 데이터 복제(Replication)와 작업 재시도(Retry) 메커니즘을 내장하고 있습니다.

**💡 비유**: 한 명의 천재 요리사가 10,000인분의 요리를 하는 것이 아니라, 1,000명의 일반 요리사에게 재료를 나누어 주고 각자 자기 주방(Data Node)에서 요리한 뒤 마지막에 결과만 합치는 방식입니다. 만약 요리사 한 명이 아파서 결근하더라도, 다른 요리사가 그 주방의 백업 재료를 가져와 요리를 대신 완성할 수 있는 시스템입니다.

**등장 배경 및 발전 과정**:
1. **Vertical Scale-up의 한계**: 전통적인 데이터베이스와 스토리지 장비는 성능 확장에 천문학적인 비용이 소모되었으며, 비정형 데이터(로그, 이미지 등) 처리에 취약했습니다.
2. **Hadoop 1.0 (JobTracker 기반)**: HDFS와 MapReduce가 강력하게 결합된 초기 버전입니다. 하지만 JobTracker에 자원 관리와 작업 스케줄링 부하가 집중되어 단일 장애점(SPOF)과 확장성 병목 현상이 발생했습니다.
3. **Hadoop 2.0/3.0 (YARN의 도입)**: 자원 관리(Resource Manager)와 애플리케이션 라이프사이클 관리(Application Master)를 분리한 YARN(Yet Another Resource Negotiator) 아키텍처로 진화했습니다. 이를 통해 Spark, Flink 등 MapReduce 이외의 다양한 연산 프레임워크가 Hadoop 클러스터를 공유할 수 있게 되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Hadoop 핵심 3대 구성 요소 및 상세 역할

| 구성 요소 | 명칭 | 상세 역할 및 내부 동작 매커니즘 | 기술적 특징 | 비유 |
|---|---|---|---|---|
| **HDFS** | 분산 파일 시스템 | 블록 단위(128MB/256MB) 저장, 3중 복제본 생성으로 가용성 확보 | Write-once, Read-many | 거대한 창고와 보관원 |
| **YARN** | 클러스터 자원 관리 | CPU, Memory 자원 할당 및 클러스터 전체 스케줄링 수행 | Multi-tenancy 지원 | 클러스터 지배인 |
| **MapReduce** | 분산 처리 엔진 | Map(데이터 분산 처리) -> Shuffle(데이터 정렬) -> Reduce(결합) | 배치 기반 대용량 처리 | 분산 요리 공정 |
| **NameNode** | HDFS 메타데이터 관리 | 파일 이름, 권한, 블록 위치 정보를 메모리에서 관리 | HA(High Availability) 필수 | 도서관 대출 목록 |
| **DataNode** | 실제 데이터 저장 | 블록을 로컬 디스크에 저장하고 NameNode에 주기적 보고(Heartbeat) | 데이터 지역성(Locality) | 도서관 서가 |

### 정교한 구조 다이어그램: Hadoop 2.x/3.x YARN 기반 아키텍처

```ascii
[ Hadoop Cluster Management & Data Flow ]

    +---------------------------------------+
    |           Client Application          |
    +---------------------------------------+
                    | (Submit Job)
                    v
    +---------------------------------------+      +-----------------------+
    |        YARN Resource Manager          | <--> |  HDFS NameNode        |
    |  (Global Scheduler, Node Health)      |      |  (Metadata, Namespace)|
    +---------------------------------------+      +-----------------------+
           /                |               \                |
 (Allocate Container) (Monitor) (Allocate Container)         | (Block Locations)
         /                  |                 \              |
+----------------+  +----------------+  +----------------+   |
| Node Manager 1 |  | Node Manager 2 |  | Node Manager N |   |
| +------------+ |  | +------------+ |  | +------------+ | <---+
| | Container  | |  | | Container  | |  | | Container  | |
| | (App Master)| |  | | (Map Task) | |  | |(Reduce Task)| |
| +------------+ |  | +------------+ |  | +------------+ |
| [ DataNode 1 ] |  | [ DataNode 2 ] |  | [ DataNode N ] |
+----------------+  +----------------+  +----------------+
      (Local Disk)        (Local Disk)        (Local Disk)

[ Data Locality Principle ]
"Move computation to data, not data to computation."
-> Reduce Network I/O by executing tasks on the same node where data resides.
```

### 심층 동작 원리: MapReduce 실행 5단계 (Shuffling Deep Dive)

1. **Input Splitting**: HDFS 블록 단위로 데이터를 쪼개어 Map 태스크에 할당합니다.
2. **Map Phase**: 사용자 정의 로직에 따라 (Key, Value) 쌍으로 데이터를 가공합니다.
3. **Shuffling & Sorting (Critical Path)**:
   - **Partitioning**: Reduce 태스크 수에 맞춰 데이터를 나눕니다.
   - **Sorting**: 같은 Key를 가진 데이터를 모으고 정렬합니다. 
   - 이 과정에서 대규모 네트워크 I/O와 디스크 I/O가 발생하며, Hadoop 성능의 핵심 병목 지점이 됩니다.
4. **Reduce Phase**: 같은 Key로 그룹화된 데이터를 합산하거나 요약합니다.
5. **Output Writing**: 최종 결과를 HDFS에 기록합니다.

### 핵심 코드: MapReduce WordCount 예시 (Java 기반)

```java
public class WordCount {
    // Mapper: 문장을 단어로 쪼개어 (단어, 1)로 출력
    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }

    // Reducer: 같은 단어의 1들을 모두 더함
    public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }
}
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Hadoop MapReduce vs Apache Spark

| 비교 관점 | Hadoop MapReduce | Apache Spark | 기술적 인사이트 |
|---|---|---|---|
| **처리 방식** | 디스크 기반 배치 처리 | 인메모리(RAM) 기반 처리 | Spark는 중간 결과를 RAM에 유지하여 10~100배 빠름. |
| **지연 시간** | 높음 (High Latency) | 낮음 (Low Latency) | 실시간성 처리가 필요하면 Spark, 초고용량 배치는 Hadoop. |
| **장애 복구** | 작업 단계별 디스크 기록(강력) | 리니지(Lineage) 재계산 방식 | Hadoop은 매우 안정적이나 I/O 비용이 큼. |
| **학습 곡선** | 높음 (Java 기반 API 복잡) | 낮음 (SQL, Python 등 지원) | Spark는 생산성이 월등히 높음. |
| **비용 모델** | 저렴한 디스크 자원 중심 | 비싼 RAM 자원 중심 | 비용 효율성은 여전히 Hadoop이 우위에 있음. |

### 과목 융합 관점 분석 (운영체제 및 네트워크 연계)
- **운영체제(OS)와의 융합**: HDFS DataNode는 OS의 **Zero-copy(sendfile)** 기술을 활용하여 디스크의 데이터를 커널 영역에서 네트워크 카드로 직접 전송함으로써 CPU 오버헤드를 최소화합니다. 또한 YARN은 **Linux Container(Cgroups)**를 통해 각 태스크 간의 CPU 및 메모리 간섭을 격리합니다.
- **네트워크(Network)와의 융합**: Hadoop 클러스터는 **Rack-awareness** 알고리즘을 사용합니다. 데이터 복제본 3개를 구성할 때 [로컬 1개, 같은 랙 1개, 다른 랙 1개]에 배치하여, 스위치 장애에 대비하면서도 랙 간 트래픽(East-West Traffic)을 최적화합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 기존 RDBMS 기반 데이터 웨어하우스의 한계 극복
**문제 상황**: 국내 대형 금융사의 로그 데이터가 매일 10TB씩 쌓이면서 기존 Oracle DW 시스템의 용량이 한계에 도달하고, 쿼리 수행 시간이 24시간을 넘기 시작했습니다.

**기술사의 전략적 의사결정**:
1. **Hadoop 기반 데이터 레이크(Data Lake) 구축**: 정형 데이터뿐만 아니라 비정형 로그를 원형 그대로 저장하기 위해 HDFS를 도입합니다. 이는 데이터 저장 비용을 기존 대비 1/10 이하로 절감합니다.
2. **Off-loading 전략**: 고비용 RDBMS에서는 복잡한 연산을 제거하고, Hadoop에서 MapReduce/Spark로 전처리(ETL)한 결과물만 RDBMS로 로드하여 분석 리포트를 생성합니다.
3. **압축 알고리즘 적용**: 디스크 I/O를 줄이기 위해 Snappy나 Parquet(Colunmar Format) 저장 형식을 채택하여 저장 공간 효율성과 검색 성능을 동시에 확보합니다.

### 도입 시 고려사항 및 안티패턴 (Anti-patterns)
- **안티패턴 - 작은 파일 문제 (Small Files Problem)**: HDFS에 수 KB 단위의 작은 파일 수백만 개를 저장하면 NameNode의 메모리가 고갈되어 전체 클러스터가 마비됩니다. 이를 방지하기 위해 파일 병합(Compaction)이나 Hadoop Archive(HAR)를 활용해야 합니다.
- **체크리스트**: 
  - NameNode HA(Active-Standby) 및 Quorum Journal Node 구성 여부.
  - 데이터 거버넌스 및 보안(Kerberos, Ranger) 적용 방안.
  - 워크로드에 최적화된 블록 사이즈(최근엔 256MB 이상 권장) 설정.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과
- **TCO 절감**: 고가의 외산 스토리지 장비를 범용 x86 서버 클러스터로 대체하여 데이터 저장 및 처리 비용을 획적으로 낮춥니다.
- **데이터 분석 민주화**: 전사 데이터를 중앙 집중화하여 데이터 사이언티스트들이 자유롭게 대규모 데이터를 탐색할 수 있는 환경을 제공합니다.

### 미래 전망 및 진화 방향
- **Cloud-Native Hadoop**: 온프레미스 클러스터에서 벗어나 AWS S3나 Azure Blob Storage를 스토리지로 활용하고, 연산(Compute)만 탄력적으로 확장하는 **Separation of Storage and Compute** 아키텍처로 진화 중입니다.
- **AI/ML 연계**: Hadoop 상의 거대 데이터를 활용하여 LLM(대규모 언어 모델) 학습을 위한 파이프라인으로 재조명받고 있습니다.

### ※ 참고 표준/가이드
- **Apache Software Foundation**: 하둡 오픈소스 표준 프로젝트 관리 기관.
- **Cloud Era/Hortonworks Reference Architecture**: 엔터프라이즈 하둡 구축 표준 가이드라인.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [Apache Spark](@studynotes/16_bigdata/01_bigdata_processing/apache_spark.md) : Hadoop의 한계를 극복한 인메모리 분산 처리 엔진.
- [Kafka](@/studynotes/16_bigdata/01_bigdata_processing/_index.md) : Hadoop으로 실시간 데이터를 수집하기 위한 메시징 시스템.
- [Hive](@/studynotes/16_bigdata/01_bigdata_processing/_index.md) : Hadoop 데이터를 SQL로 조회할 수 있게 해주는 데이터 웨어하우스 소프트웨어.
- [Zookeeper](@/studynotes/16_bigdata/01_bigdata_processing/_index.md) : Hadoop 에코시스템의 분산 코디네이션 및 HA 관리 도구.
- [Data Lakehouse](@studynotes/14_data_engineering/01_data_architecture/data_lakehouse.md) : 데이터 레이크와 데이터 웨어하우스의 장점을 결합한 차세대 아키텍처.

---

### 👶 어린이를 위한 3줄 비유 설명
1. 하둡은 **거대한 정보를 나누어서 보관하고 처리하는 '슈퍼 로봇 팀'**과 같아요.
2. 한 명의 로봇이 다 하는 게 아니라, 수천 명의 로봇이 각자 데이터를 맡아서 보관하고 숙제를 나눠서 하기 때문에 엄청나게 어려운 문제도 빨리 풀 수 있어요.
3. 로봇 한두 명이 고장 나도 다른 로봇들이 그 일을 대신해 주기 때문에 절대 데이터가 사라지거나 멈추지 않는답니다!
