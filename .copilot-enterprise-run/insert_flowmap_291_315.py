import os

BASE = "/home/ubuntu/workspace/brainscience/content/studynote/07_enterprise_systems/05_data_bi"
MARKER = "### 👶 어린이를 위한 3줄 비유 설명"

FLOWS = {
    "291_data_lineage_flow_transformation_tracking.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
소스 시스템 데이터 생성 (DB, API, 파일)
    │
    ▼
ETL/ELT 파이프라인 (수집·변환·적재)
    │
    ▼
테이블 수준 리니지 → 컬럼 수준 리니지 진화
    │
    ▼
OpenLineage 표준 + dbt·Airflow 자동 수집
    │
    ▼
Data Catalog 통합 → 규제 감사·품질 근본 원인 분석
```

> **키워드**: Data Lineage, Column-level Lineage, OpenLineage, Data Catalog, DAG, Data Provenance
""",
    "292_cloud_native_dw_snowflake_bigquery_redshift.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
온프레미스 MPP DW (Teradata, Netezza)
    │
    ▼
Hadoop 기반 분산 처리 (HDFS + Hive)
    │
    ▼
클라우드 DW 1세대 (Redshift - 컬럼 스토어)
    │
    ▼
스토리지·컴퓨팅 분리 DW (Snowflake, BigQuery)
    │
    ▼
서버리스·멀티클러스터·Zero-Copy Clone 진화
```

> **키워드**: Cloud Native DW, Snowflake, BigQuery, Redshift, MPP, Storage-Compute Separation, Serverless
""",
    "293_storage_compute_separation.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
온프레미스 공유 스토리지 (SAN/NAS) 병목
    │
    ▼
Hadoop HDFS - 데이터 로컬리티 강제 결합
    │
    ▼
S3/GCS/ADLS 오브젝트 스토리지 분리 등장
    │
    ▼
Snowflake/BigQuery 스토리지·컴퓨팅 독립 확장
    │
    ▼
Data Lakehouse (Delta Lake, Iceberg) - 통합 계층
```

> **키워드**: Storage-Compute Separation, Object Storage, S3, Data Lakehouse, Snowflake, Elasticity
""",
    "294_zero_copy_cloning.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
전통 DW 데이터 복사 - 시간·비용 비효율
    │
    ▼
백업/스냅샷 방식 (물리적 복사 오버헤드)
    │
    ▼
Copy-on-Write 메타데이터 포인터 기법 등장
    │
    ▼
Snowflake Zero-Copy Clone - 즉각·비용 제로
    │
    ▼
개발/테스트/프로덕션 격리 환경 즉시 생성
```

> **키워드**: Zero-Copy Cloning, Copy-on-Write, Snowflake, Metadata Pointer, Data Isolation, Time Travel
""",
    "295_data_mesh.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
중앙 집중형 데이터 레이크 - 병목·소유권 혼란
    │
    ▼
데이터 플랫폼 팀 단독 관리 → 확장성 한계
    │
    ▼
Data Mesh 패러다임 - 도메인 소유권 분산
    │
    ▼
Data Product + 셀프서브 플랫폼 + 연합 거버넌스
    │
    ▼
Federated Computational Governance 표준화
```

> **키워드**: Data Mesh, Domain Ownership, Data Product, Self-Serve Platform, Federated Governance, Zhamak Dehghani
""",
    "296_data_fabric.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
사일로화된 이기종 데이터 소스 난립
    │
    ▼
데이터 통합 미들웨어 (ETL 허브) 한계
    │
    ▼
Active Metadata + AI 기반 데이터 패브릭 등장
    │
    ▼
Knowledge Graph + 자동 발견·추천·거버넌스
    │
    ▼
하이브리드/멀티클라우드 통합 지능형 데이터 계층
```

> **키워드**: Data Fabric, Active Metadata, Knowledge Graph, AI-Driven Integration, Hybrid Cloud, Data Virtualization
""",
    "297_data_virtualization.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
물리적 ETL 복사 - 지연·중복 스토리지 문제
    │
    ▼
연합 쿼리 (Federated Query) 초기 방식
    │
    ▼
데이터 가상화 레이어 - 논리적 단일 뷰 제공
    │
    ▼
Denodo/Dremio - 실시간 쿼리 푸시다운 최적화
    │
    ▼
Data Fabric 구성 요소로 편입·진화
```

> **키워드**: Data Virtualization, Logical Data Warehouse, Federated Query, Denodo, Dremio, Query Pushdown
""",
    "298_distributed_processing_framework_mapreduce_spark.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
단일 서버 배치 처리 한계 (TB급 데이터)
    │
    ▼
Google MapReduce 논문 (2004) - 분산 처리 패러다임
    │
    ▼
Hadoop MapReduce 오픈소스 구현 (디스크 I/O 병목)
    │
    ▼
Apache Spark - 인메모리 DAG 실행 엔진 (100x 빠름)
    │
    ▼
Spark Structured Streaming + Delta Lake 통합
```

> **키워드**: MapReduce, Apache Spark, DAG, In-Memory Processing, HDFS, RDD, DataFrame, Hadoop
""",
    "299_spark_rdd_resilient_distributed_dataset.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
Hadoop MapReduce - 디스크 기반 중간 결과 저장
    │
    ▼
Spark RDD - 인메모리 분산 데이터셋 추상화
    │
    ▼
Transformation (지연 평가) + Action (실행 트리거)
    │
    ▼
DataFrame/Dataset API - 스키마 기반 최적화
    │
    ▼
Catalyst Optimizer + Tungsten 메모리 관리
```

> **키워드**: RDD, Resilient Distributed Dataset, Spark, Lazy Evaluation, Lineage, DataFrame, Catalyst
""",
    "300_realtime_data_streaming_kafka_cdc.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
배치 ETL - 야간 처리, T+1 데이터 지연
    │
    ▼
메시지 큐 (RabbitMQ) - 실시간 이벤트 전달
    │
    ▼
Apache Kafka - 분산 로그 스트리밍 플랫폼
    │
    ▼
CDC (Change Data Capture) - DB 변경 이벤트 캡처
    │
    ▼
Kafka + Debezium + Flink 실시간 스트리밍 파이프라인
```

> **키워드**: Kafka, CDC, Change Data Capture, Debezium, Stream Processing, Real-Time ETL, Flink
""",
    "301_kafka_topic_partition_consumer_group.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
단일 큐 메시지 브로커 - 처리량 병목
    │
    ▼
Kafka Topic - 논리적 데이터 채널 추상화
    │
    ▼
Partition - 물리적 분산·병렬 처리 단위
    │
    ▼
Consumer Group - 파티션별 독립 소비자 배정
    │
    ▼
Replication Factor + ISR = 고가용성 보장
```

> **키워드**: Kafka Topic, Partition, Consumer Group, Offset, Replication Factor, ISR, Producer, Broker
""",
    "302_dataops_cicd_dbt.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
수작업 SQL 쿼리 관리 - 버전관리 부재
    │
    ▼
ETL 도구 GUI 기반 파이프라인 (Informatica 등)
    │
    ▼
dbt - SQL 변환 코드화 + Git 버전관리
    │
    ▼
DataOps - CI/CD + 테스트 + 모니터링 통합
    │
    ▼
DataOps 플랫폼 (데이터 파이프라인 자동화 표준화)
```

> **키워드**: DataOps, dbt, CI/CD, Data Pipeline, Data Testing, Git-based Workflow, Data Quality
""",
    "303_mlops_feature_store.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
실험실 ML 모델 - 프로덕션 배포 단절 문제
    │
    ▼
수작업 피처 엔지니어링 반복 - 일관성 부재
    │
    ▼
Feature Store 등장 - 피처 재사용·공유 플랫폼
    │
    ▼
온라인(Redis)/오프라인(Hive) 이중 저장 구조
    │
    ▼
MLOps 통합 - 피처→모델→서빙 자동화 파이프라인
```

> **키워드**: Feature Store, MLOps, Feature Engineering, Online Store, Offline Store, Feast, Training-Serving Skew
""",
    "304_realtime_cdp_architecture.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
채널별 고객 데이터 사일로 (CRM·웹·앱 분리)
    │
    ▼
DMP (Data Management Platform) - 쿠키 기반 익명
    │
    ▼
CDP (Customer Data Platform) - ID 통합 실명 프로파일
    │
    ▼
실시간 CDP - 스트리밍 이벤트 즉각 프로파일 갱신
    │
    ▼
Real-Time Personalization + 동의 관리 통합
```

> **키워드**: CDP, Customer Data Platform, Real-Time CDP, Identity Resolution, DMP, 360° Profile, Consent Management
""",
    "305_data_clean_room.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
쿠키 기반 광고 타겟팅 (서드파티 데이터)
    │
    ▼
개인정보 규제 강화 (GDPR, 쿠키리스 시대)
    │
    ▼
Data Clean Room - 원시 데이터 비공개 협업 분석
    │
    ▼
MPC/차분 프라이버시/동형암호 프라이버시 기술 통합
    │
    ▼
Snowflake/Google Ads DCR 플랫폼 상용화
```

> **키워드**: Data Clean Room, Privacy-Preserving Analytics, MPC, Differential Privacy, Cookieless, First-Party Data
""",
    "306_data_governance_3_elements.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
데이터 품질 문제 인식 - 임시방편 대응
    │
    ▼
데이터 관리 정책 수립 (조직·프로세스·IT 3요소)
    │
    ▼
Data Catalog + Data Steward 체계화
    │
    ▼
DAMA-DMBOK 기반 거버넌스 성숙도 모델 적용
    │
    ▼
능동적 거버넌스 (Active Metadata + AI 자동화)
```

> **키워드**: Data Governance, Data Steward, Data Catalog, CDO, DAMA-DMBOK, MDM, Data Quality, Active Metadata
""",
    "307_molap_rolap_holap.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
평면 2D 리포트 한계 - 다차원 분석 필요성
    │
    ▼
MOLAP - 전용 큐브 스토리지 (빠른 쿼리, 공간 비용)
    │
    ▼
ROLAP - RDB 기반 스타 스키마 (확장성, 느린 쿼리)
    │
    ▼
HOLAP - MOLAP+ROLAP 하이브리드 계층화
    │
    ▼
현대 OLAP (Druid, ClickHouse) - 실시간 집계 진화
```

> **키워드**: MOLAP, ROLAP, HOLAP, OLAP Cube, Star Schema, Snowflake Schema, Drill-Down, ClickHouse
""",
    "308_ai_bi_augmented_analytics.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
전통 BI - 수작업 SQL 쿼리 + 정적 대시보드
    │
    ▼
셀프서비스 BI (Power BI, Tableau) - 드래그앤드롭
    │
    ▼
Augmented Analytics - AI/ML 자동 인사이트 발굴
    │
    ▼
NLQ (자연어 쿼리) + Auto-Narrative 리포트
    │
    ▼
GenAI BI - LLM 기반 대화형 데이터 분석
```

> **키워드**: Augmented Analytics, NLQ, AutoML BI, Self-Service BI, Power BI, Tableau, GenAI BI, Smart Insight
""",
    "309_influxdb_downsampling.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
RDB 시계열 저장 - 쓰기 병목·스토리지 폭증
    │
    ▼
시계열 DB 전용 (InfluxDB, Prometheus) 등장
    │
    ▼
고해상도 실시간 데이터 → 시간 경과 후 용량 문제
    │
    ▼
Downsampling - 집계 함수로 해상도 단계적 축소
    │
    ▼
Retention Policy + CQ (Continuous Query) 자동화
```

> **키워드**: InfluxDB, Time Series DB, Downsampling, Retention Policy, Continuous Query, Prometheus, Telegraf, Flux
""",
    "310_neo4j_fraud_detection.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
RDB 조인 기반 사기 탐지 - 복잡한 관계에서 성능 한계
    │
    ▼
그래프 DB (Neo4j) - 노드·엣지 네이티브 저장
    │
    ▼
실시간 그래프 트래버설 - 연결 관계 패턴 탐지
    │
    ▼
GDS (Graph Data Science) - PageRank·커뮤니티 탐지
    │
    ▼
GNN + Neo4j 하이브리드 - AI 기반 사기 예측
```

> **키워드**: Neo4j, Graph Database, Cypher Query, Fraud Detection, GDS, Graph Traversal, Community Detection, GNN
""",
    "311_parquet_orc_rle_compression.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
행 기반 저장 (CSV, JSON) - 분석 쿼리 불필요 I/O
    │
    ▼
컬럼 기반 저장 (Parquet, ORC) - 컬럼 선택 I/O 최소화
    │
    ▼
RLE (Run-Length Encoding) + Dictionary 압축
    │
    ▼
Predicate Pushdown + Column Pruning 쿼리 최적화
    │
    ▼
Delta Lake/Iceberg - 오픈 테이블 포맷으로 진화
```

> **키워드**: Parquet, ORC, RLE, Columnar Storage, Predicate Pushdown, Snappy, Zstandard, Data Lakehouse
""",
    "312_hash_sharding_directory_sharding.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
단일 DB 서버 한계 - 수평 분할(Sharding) 필요
    │
    ▼
Range Sharding - 핫스팟 문제 발생
    │
    ▼
Hash Sharding - 균등 분산, 범위 조회 불리
    │
    ▼
Directory Sharding - 룩업 테이블 기반 유연한 재분배
    │
    ▼
Consistent Hashing + Virtual Node - 확장성 극대화
```

> **키워드**: Sharding, Hash Sharding, Directory Sharding, Consistent Hashing, Virtual Node, Horizontal Scaling, Hotspot
""",
    "313_htap_in_memory_architecture.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
OLTP/OLAP 완전 분리 - ETL 지연 (T+1 분석)
    │
    ▼
인메모리 DB (SAP HANA) - 단일 엔진 HTAP 시도
    │
    ▼
행·열 혼합 스토리지 + 분리된 워크로드 격리
    │
    ▼
TiDB/SingleStore - 분산 HTAP 클라우드 네이티브
    │
    ▼
실시간 OLAP 분석 (Freshness < 1s) 달성
```

> **키워드**: HTAP, In-Memory Database, SAP HANA, TiDB, Row Store, Column Store, Real-Time Analytics
""",
    "314_telemetry_bigdata_parsing.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
O-RAN 네트워크 장비 지표 수동 수집 한계
    │
    ▼
스트리밍 텔레메트리 (gRPC/gNMI) - 실시간 전송
    │
    ▼
Kafka + Flink - 대용량 텔레메트리 스트리밍 파싱
    │
    ▼
시계열 DB (InfluxDB, OpenTSDB) 저장·분석
    │
    ▼
ML 기반 네트워크 이상 탐지 자동화
```

> **키워드**: Telemetry, O-RAN, gNMI, gRPC, Kafka, Flink, Time Series, Network Analytics, Streaming Parsing
""",
    "315_nosql_base_cap_theorem.md": """\
### 📈 관련 키워드 및 발전 흐름도

```
RDB ACID 트랜잭션 - 분산 환경 확장 한계
    │
    ▼
CAP 정리 - 일관성·가용성·분할내성 동시 불가
    │
    ▼
NoSQL BASE - 결과적 일관성으로 가용성 극대화
    │
    ▼
CP 계열 (HBase, ZooKeeper) vs AP 계열 (Cassandra)
    │
    ▼
NewSQL (CockroachDB, Spanner) - ACID + 수평 확장
```

> **키워드**: CAP Theorem, BASE, ACID, NoSQL, Eventual Consistency, Partition Tolerance, NewSQL, CockroachDB
""",
}

for filename, section_content in FLOWS.items():
    path = os.path.join(BASE, filename)
    if not os.path.exists(path):
        print(f"MISSING: {filename}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if '관련 키워드 및 발전 흐름도' in content:
        print(f"SKIP (already has): {filename}")
        continue
    if MARKER not in content:
        print(f"WARNING: No marker found in {filename}")
        continue
    new_content = content.replace(MARKER, section_content + "\n" + MARKER)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated: {filename}")

print("Done.")
