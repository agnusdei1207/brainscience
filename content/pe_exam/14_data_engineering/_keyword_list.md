+++
title = "14. 데이터 엔지니어링 키워드 목록"
date = 2026-03-03
[extra]
categories = "pe_exam-data-engineering"
+++

# 데이터 엔지니어링 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 데이터 엔지니어링 전 영역 기술사 수준 키워드
> ⚡ 데이터 엔지니어링: 원시 데이터를 가치 있는 정보로 변환하는 **파이프라인 설계·운영·최적화** 전체 흐름

---

## 1. 데이터 수집 / 수집 파이프라인 — 20개

1. 데이터 수집 유형 — 배치(Batch) / 스트리밍(Streaming) / 마이크로배치
2. CDC (Change Data Capture) — 변경 사항만 캡처, Debezium / Maxwell
3. Debezium — Kafka Connect 기반 CDC, MySQL/PostgreSQL/Oracle Binlog
4. 웹 스크래핑 — Scrapy / Playwright / Puppeteer, robots.txt 준수
5. API 데이터 수집 — REST/GraphQL/gRPC, Pagination, Rate Limiting
6. Kafka (Apache Kafka) — 분산 메시지 브로커, 토픽/파티션/오프셋/Consumer Group
7. Kafka 아키텍처 — Broker / ZooKeeper(구) / KRaft(신) / Controller
8. Kafka Connect — 소스/싱크 커넥터, 외부 시스템 통합
9. Kafka Streams — 경량 스트리밍, Topology, KTable/KStream
10. Kafka 중요 설정 — Replication Factor / Retention / acks / exactly-once semantics
11. Apache Pulsar — Kafka 대안, 컴퓨트/스토리지 분리, 다중 테넌시
12. Amazon Kinesis — Data Streams / Firehose / Analytics, AWS 관리형
13. Apache Flink — 상태 기반 스트리밍, Event-Time / Processing-Time, Watermark
14. Flink Exactly-Once — 2PC 기반, 정확히 한 번 처리 보장
15. MQTT → Kafka — IoT 데이터 흐름 설계
16. Fluentd / FluentBit — 로그 수집 및 전달
17. Logstash — ELK Stack 수집, 필터링, 변환
18. Filebeat / Metricbeat — 경량 Elastic 에이전트
19. NiFi (Apache) — 시각적 데이터 흐름 관리, 백프레셔
20. Airbyte — ELT 플랫폼, 오픈소스, 300+ 커넥터

---

## 2. 데이터 저장소 / 포맷 — 22개

1. Parquet 포맷 — 컬럼 지향, 스키마 임베디드, 압축 효율, Pandas/Spark 기본
2. ORC (Optimized Row Columnar) — Hive 기본, 브라우저 풋프린트 최소화
3. Avro — 스키마 레지스트리, 메시지 직렬화 (Kafka 기본 포맷)
4. JSON / JSONL — 가독성↑, 크기↑, 비정형 적합
5. Delta Lake — ACID on Data Lake, 시간여행, 스키마 진화, Databricks
6. Apache Iceberg — 오픈 테이블 포맷, 히든 파티셔닝, 타임 트래블, Netflix
7. Apache Hudi — Upsert 지원 증분 처리, Uber 개발
8. Apache Arrow — 컬럼 지향 인메모리 포맷, 제로 카피, 크로스 언어
9. DuckDB — 임베디드 OLAP, SQL on Parquet/CSV/JSON, MotherDuck
10. HDFS (Hadoop Distributed File System) — 대용량 분산 파일 시스템, 블록 복제
11. 오브젝트 스토리지 — S3 / GCS / ADLS Gen2, 데이터 레이크 기반
12. 데이터 레이크 (Data Lake) — 원시 데이터 저장, Schema-on-Read
13. 레이크하우스 (Lakehouse) — Data Lake + DW, ACID + BI + ML 통합
14. LSM-Tree (Log-Structured Merge Tree) — RocksDB/LevelDB, 쓰기 최적화
15. B-Tree vs LSM-Tree — 읽기/쓰기 트레이드오프
16. RocksDB — 임베디드 KV, Compaction 전략, 카프카 스테이트 스토어
17. 시계열 데이터 — InfluxDB / TimescaleDB / QuestDB / OpenTSDB
18. 로그 데이터 — Elasticsearch / OpenSearch / Loki (Grafana)
19. 스키마 레지스트리 — Confluent Schema Registry, Avro/Protobuf/JSON Schema 관리
20. 데이터 압축 — Snappy / Zstd / LZ4 / Gzip / Brotli — 속도vs압축률
21. 파일 파티셔닝 전략 — 날짜/지역/카테고리 기반, Hive 파티셔닝
22. 데이터 최적화 — 소파일 문제 (Small File Problem), 압축 병합

---

## 3. 배치 처리 / 분산 컴퓨팅 — 18개

1. MapReduce — 분산 배치 패러다임, Map(분산)/Reduce(집계)
2. Apache Spark — 인메모리 분산 처리, RDD → DataFrame → Dataset
3. Spark 아키텍처 — Driver / Executor / SparkContext / DAG Scheduler
4. Spark 최적화 — Catalyst Optimizer / Tungsten / AQE (Adaptive Query Execution)
5. Spark 구조적 스트리밍 (Structured Streaming) — 마이크로배치 / Continuous
6. Spark + Delta Lake — ACID 트랜잭션, 업서트(Merge into)
7. Dask — Python 병렬 컴퓨팅, Pandas 호환 대규모 데이터
8. Ray — 분산 Python, RL·서빙·ML 훈련
9. Hadoop YARN — 자원 관리자, MR/Spark/Tez 실행
10. Hive — SQL on Hadoop, 메타스토어, Beeline
11. Presto / Trino — 분산 SQL 쿼리 엔진, 다중 카탈로그
12. Athena (AWS) — 서버리스 SQL, S3 직접 쿼리, Presto 기반
13. BigQuery — Google 서버리스 DW, 컬럼 지향, Dremel 기반
14. Redshift — AWS MPP DW, Redshift Spectrum, RA3 노드
15. Snowflake — 멀티클라우드 DW, VPS 가상 웨어하우스, Time Travel
16. Spark on Kubernetes — 동적 자원 할당, k8s 네이티브
17. 파티션 수 최적화 — 코어 수 × 2~4, 셔플 파티션 설정
18. Broadcast Join / Skew Join / Sort-Merge Join — Spark 조인 최적화

---

## 4. 스트리밍 처리 심화 — 16개

1. 스트리밍 처리 패러다임 — 이벤트 시간 vs 처리 시간 vs 수집 시간
2. Watermark — 지연 데이터 허용 임계시간, 윈도우 트리거
3. 윈도우 연산 — 텀블링(Tumbling) / 슬라이딩(Sliding) / 세션(Session) / 글로벌
4. 정확히 한 번 (Exactly-Once) — Idempotent Producer + Transactional Consumer
5. 최소 한 번 (At-Least-Once) / 최대 한 번 (At-Most-Once) 비교
6. 상태 기반 처리 (Stateful Processing) — 집계, 조인, 세션화
7. 체크포인팅 (Checkpointing) — 장애 복구, 상태 저장
8. 역압 (Backpressure) — 소비 속도 조절, 유입 제한
9. 스트리밍 SQL — ksqlDB / Flink SQL / Spark SQL Streaming
10. 복잡 이벤트 처리 (CEP) — 패턴 매칭, Flink CEP
11. 람다 아키텍처 — 배치 레이어 + 스피드 레이어 + 서빙 레이어
12. 카파 아키텍처 — 스트리밍만으로 단순화
13. 델타 아키텍처 (Delta Architecture) — Delta Lake 기반 통합
14. 실시간 OLAP — Apache Druid / Apache Pinot — 초저지연 분석
15. ClickHouse — 컬럼 지향 초고속 OLAP, 비정형 스키마
16. 스트리밍 데이터 품질 — 스키마 검증, 중복 제거, 지연 알람

---

## 5. 데이터 파이프라인 오케스트레이션 — 16개

1. Apache Airflow — DAG 기반 파이프라인, Python 정의, 스케줄러
2. Airflow 구성 — Scheduler / Worker / Webserver / Metadata DB / Executor
3. Airflow Executor — Sequential / Local / Celery / Kubernetes / DASK
4. Prefect — Pythonic 파이프라인, 동적 워크플로우, Prefect Cloud
5. Dagster — 데이터 자산 중심 파이프라인, 데이터 의존성 그래프
6. dbt (Data Build Tool) — SQL 변환 레이어, 테스트/문서화, ELT 핵심
7. dbt 모델 — Staging → Intermediate → Mart 계층, Ref/Source
8. dbt Tests — 스키마 테스트 / 커스텀 테스트, Great Expectations 연동
9. Apache NiFi — 시각적 흐름 관리, 역압, 클러스터
10. Mage (Mage AI) — 현대적 파이프라인, 블록 기반 개발
11. Temporal — 내결함성 워크플로우 엔진 (Uber → Temporal)
12. Luigi — 이탈리아어, Spotify, 의존성 기반 태스크
13. Glue (AWS) — 서버리스 ETL, 스파크 기반
14. Data Factory (Azure) — GUI 기반 ETL/ELT 파이프라인
15. Cloud Composer (GCP) — 관리형 Airflow
16. DataOps — 데이터 파이프라인의 DevOps, 자동화·협업·품질

---

## 6. 데이터 품질 / 거버넌스 — 18개

1. 데이터 품질 차원 — 완전성/정확성/일관성/적시성/유효성/유일성
2. Great Expectations — 파이썬 데이터 품질 프레임워크, Expectations
3. Deequ (AWS) — Spark 기반 데이터 품질, 통계 제약
4. Soda — SQL 기반 데이터 품질 검사
5. 데이터 카탈로그 — Apache Atlas / DataHub / OpenMetadata / Collibra / Alation
6. DataHub (LinkedIn) — 메타데이터 검색, 계보, 오픈소스
7. 데이터 계보 (Data Lineage) — 열 수준 계보, 영향 분석
8. 데이터 의미론적 레이어 — dbt Semantic Layer, MetricFlow
9. 마스터 데이터 관리 (MDM) — 황금 레코드, 통합 뷰
10. 참조 데이터 관리 (RDM)
11. 데이터 메시 (Data Mesh) — 도메인 소유, 제품으로서의 데이터, 연합 거버넌스
12. 데이터 계약 (Data Contract) — 생산자-소비자 스키마 합의
13. 데이터 관찰성 (Data Observability) — Monte Carlo, Bigeye, Acceldata
14. 데이터 신선도 / 지연 알람 — SLA 기반 모니터링
15. PII (Personally Identifiable Information) 관리 — 마스킹/토큰화/암호화
16. CCPA / GDPR 데이터 파이프라인 적용 — 목적 제한, 삭제 요청 전파
17. 데이터 분류 — 공개/내부/기밀/극비, 자동화 분류 (Macie/DLP)
18. 컬럼 수준 접근 제어 — 행 수준 보안 (RLS), 동적 데이터 마스킹

---

## 7. 분석 엔지니어링 / BI 통합 — 12개

1. Analytics Engineering — ELT + dbt, 비즈니스 로직을 SQL로
2. Semantic Layer — 지표 정의 중앙화, LookML / MetricFlow / Cube.dev
3. OLAP 큐브 현대화 — 가상 큐브 (Cube.js), 실시간 OLAP
4. 역 ETL (Reverse ETL) — DW → CRM/마케팅/운영 시스템 동기화, Census/Hightouch
5. BI 도구 통합 — Tableau / Looker (Google) / Power BI / Metabase / Superset
6. Headless BI — API 기반 지표 서비스, 임베디드 분석
7. 데이터 민주화 — 셀프서비스 분석, 데이터 리터러시
8. Notebooks — Jupyter / Databricks Notebooks / Hex / Observable
9. 데이터 앱 — Streamlit / Gradio / Panel — Python 기반 인터랙티브 앱
10. Operational Analytics — 실시간 운영 대시보드, 에지 케이스 모니터링
11. 예측 분석 파이프라인 — ML 모델 출력 → DW 저장 → BI 시각화
12. AI-Augmented Analytics — 자동 인사이트 생성 (ThoughtSpot, Ask Data)

---

**총 키워드 수: 122개**
