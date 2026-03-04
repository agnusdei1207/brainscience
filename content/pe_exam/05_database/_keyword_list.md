+++
title = "05. 데이터베이스 키워드 목록"
date = 2026-03-03
[extra]
categories = "pe_exam-db"
+++

# 데이터베이스 (Database) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 데이터베이스 전 영역 핵심 키워드

---

## 1. 데이터베이스 기초 / DBMS — 22개

1. 데이터베이스 (Database) 정의 — 공유, 통합, 저장, 운영 데이터
2. DBMS (Database Management System) 역할 — 데이터 정의/조작/제어
3. 데이터 독립성 — 논리적/물리적 독립성
4. 3단계 스키마 구조 — 외부/개념/내부 스키마
5. 데이터 모델 유형 — 계층형/네트워크형/관계형/객체형/NoSQL
6. 관계형 데이터베이스 (RDBMS) — 테이블/행/열/릴레이션
7. 엔티티 (Entity) / 속성 (Attribute) / 관계 (Relationship)
8. 카디널리티 (Cardinality) — 1:1 / 1:N / M:N
9. ERD (Entity-Relationship Diagram) — 개념 데이터 모델링
10. 관계 대수 (Relational Algebra) — 선택/투영/합집합/차집합/카티션/조인
11. 관계 해석 (Relational Calculus) — 튜플/도메인 해석
12. SQL (Structured Query Language) — DDL/DML/DCL/TCL
13. DDL — CREATE / ALTER / DROP / TRUNCATE
14. DML — SELECT / INSERT / UPDATE / DELETE
15. DCL — GRANT / REVOKE
16. TCL — COMMIT / ROLLBACK / SAVEPOINT
17. 뷰 (View) — 가상 테이블, 보안/단순화
18. 저장 프로시저 (Stored Procedure)
19. 트리거 (Trigger) — 이벤트 기반 자동 실행
20. 함수 (Function) — 사용자 정의 함수
21. 커서 (Cursor) — 레코드 단위 처리
22. 데이터 딕셔너리 (Data Dictionary) / 시스템 카탈로그

---

## 2. 정규화 (Normalization) — 18개

1. 정규화 목적 — 이상 현상 (Anomaly) 제거, 중복 최소화
2. 이상 현상 — 삽입/삭제/갱신 이상
3. 함수적 종속성 (FD, Functional Dependency)
4. 완전 함수 종속 vs 부분 함수 종속
5. 이행 함수 종속 (Transitive FD)
6. 제1정규형 (1NF) — 원자값, 반복 그룹 제거
7. 제2정규형 (2NF) — 부분 종속 제거
8. 제3정규형 (3NF) — 이행 종속 제거
9. BCNF (Boyce-Codd NF) — 결정자가 모두 후보키
10. 제4정규형 (4NF) — 다치 종속 제거
11. 제5정규형 (5NF) — 조인 종속 제거
12. 역정규화 (Denormalization) — 성능을 위한 의도적 중복
13. 역정규화 기법 — 테이블 합병, 컬럼 중복, 파생 컬럼
14. 후보키 (Candidate Key) / 기본키 (Primary Key) / 대리키 (Surrogate Key)
15. 슈퍼키 (Super Key) / 복합키 (Composite Key)
16. 대체키 (Alternate Key) / 외래키 (Foreign Key)
17. 참조 무결성 (Referential Integrity)
18. 정규화 vs 역정규화 트레이드오프

---

## 3. 트랜잭션 / 동시성 제어 — 24개

1. 트랜잭션 (Transaction) 정의 — 논리적 작업 단위
2. ACID 특성 — 원자성(Atomicity)/일관성(Consistency)/격리성(Isolation)/지속성(Durability)
3. 원자성 (Atomicity) — All or Nothing
4. 일관성 (Consistency) — 무결성 제약조건 유지
5. 격리성 (Isolation) — 트랜잭션 간 독립성
6. 지속성 (Durability) — 영구 반영
7. 트랜잭션 상태 — 활성/부분완료/완료/실패/철회
8. 동시성 제어 (Concurrency Control) 목적
9. 갱신 손실 (Lost Update)
10. 더티 리드 (Dirty Read)
11. 반복 불가능 읽기 (Non-Repeatable Read)
12. 팬텀 읽기 (Phantom Read)
13. 트랜잭션 격리 수준 — READ UNCOMMITTED / READ COMMITTED / REPEATABLE READ / SERIALIZABLE
14. 잠금 (Locking) — 공유(S)/배타(X) 잠금
15. 2PL (Two-Phase Locking) — 확장 단계/축소 단계
16. 엄격한 2PL (Strict 2PL) — 해제 시점 통제
17. 데드락 (Deadlock in DB) — Wait-For Graph, 예방/탐지/회복
18. 타임스탬프 기반 프로토콜 (Timestamp Ordering)
19. 낙관적 동시성 제어 (OCC, Optimistic CC) — 충돌 적을 때 유리
20. MVCC (Multi-Version Concurrency Control) — 읽기/쓰기 충돌 없음
21. PostgreSQL MVCC — 각 트랜잭션에 스냅샷 제공
22. 갭 잠금 (Gap Lock) — 팬텀 리드 방지, InnoDB
23. 넥스트-키 잠금 (Next-Key Lock) — InnoDB REPEATABLE READ
24. savepoint — 부분 롤백 지점

---

## 4. 회복 (Recovery) — 16개

1. 회복의 목적 — 장애 후 ACID의 A·D 보장
2. 장애 유형 — 트랜잭션/시스템/매체 장애
3. 로그 (Log) 기반 회복 — WAL (Write-Ahead Logging)
4. UNDO — 미완료 트랜잭션 취소
5. REDO — 완료 트랜잭션 재실행
6. 즉각 갱신 (Immediate Update) vs 지연 갱신 (Deferred Update)
7. 체크포인트 (Checkpoint) — 로그 스캔 범위 축소
8. ARIES 회복 알고리즘 — 분석/REDO/UNDO 단계
9. 섀도우 페이징 (Shadow Paging) — 현재/섀도우 페이지 테이블
10. 미러링 (Mirroring) — 실시간 복제
11. 백업 (Backup) — 전체/차등/증분
12. 포인트-인-타임 복구 (PITR, Point-In-Time Recovery)
13. 로그 기반 PITR — PostgreSQL WAL, MySQL binlog
14. RTO (Recovery Time Objective) / RPO (Recovery Point Objective)
15. 재해 복구 (DR, Disaster Recovery) — Hot/Warm/Cold Standby
16. CDC (Change Data Capture) — 변경 캡처, 데이터 동기화

---

## 5. 인덱스 / 물리적 설계 — 20개

1. 인덱스 (Index) — B+Tree, Hash, Bitmap, Full-Text
2. B-Tree 인덱스 — 균형 트리, 순서 기반 범위 검색
3. B+Tree 인덱스 — 리프 노드 연결, 순차 스캔 유리
4. 해시 인덱스 — 등치 검색 최적, 범위 검색 불가
5. 비트맵 인덱스 (Bitmap Index) — 낮은 카디널리티, DW
6. 함수 기반 인덱스 (Function-Based Index)
7. 부분 인덱스 (Partial Index) — PostgreSQL
8. 커버링 인덱스 (Covering Index) — Index Only Scan
9. 클러스터드 인덱스 (Clustered Index) vs 논클러스터드
10. 인덱스 선택성 (Selectivity) / 카디널리티
11. 실행 계획 (Execution Plan) — EXPLAIN, 쿼리 최적화
12. SQL 튜닝 — 인덱스 힌트, 조인 방법, 서브쿼리 최적화
13. 해시 조인 / 중첩 루프 조인 / 정렬-병합 조인
14. 파티셔닝 (Partitioning) — Range/List/Hash/Composite
15. 수평 파티셔닝 (Sharding)
16. 수직 파티셔닝 — 컬럼 분리
17. 테이블스페이스 (Tablespace) — 물리 파일 할당
18. 파일 구성 방법 — 힙/순차/해시/B+Tree 파일
19. 버퍼 관리 (Buffer Pool) — LRU, 더티 페이지
20. 통계 정보 (Statistics) — 행 수, 히스토그램, 쿼리 플래너

---

## 6. SQL 심화 — 18개

1. 조인 유형 — INNER / LEFT OUTER / RIGHT OUTER / FULL OUTER / CROSS / SELF
2. 윈도우 함수 (Window Function) — ROW_NUMBER / RANK / DENSE_RANK / LEAD / LAG / SUM OVER
3. CTE (Common Table Expression) — WITH 절, 재귀 CTE
4. 서브쿼리 — 스칼라/인라인 뷰/상관 서브쿼리 (Correlated)
5. EXISTS vs IN — 성능 차이
6. UNION / UNION ALL / INTERSECT / EXCEPT
7. GROUP BY / HAVING / ROLLUP / CUBE / GROUPING SETS
8. CASE WHEN — 조건부 값 변환
9. 집계 함수 — COUNT/SUM/AVG/MAX/MIN
10. NULL 처리 — IS NULL / COALESCE / NULLIF / NVL
11. 조건부 집계 — FILTER (WHERE) in PostgreSQL
12. 피벗 (PIVOT) / 언피벗 (UNPIVOT)
13. 전체 텍스트 검색 (Full-Text Search) — tsvector, ts_rank
14. JSON/JSONB 쿼리 — PostgreSQL, MySQL JSON 함수
15. upsert — INSERT … ON CONFLICT / MERGE
16. 실행 계획 분석 — EXPLAIN ANALYZE, 비용 모델
17. 파라미터화 쿼리 — Prepared Statement, SQL 인젝션 방어
18. 저장 프로시저 vs 함수 vs 트리거 차이

---

## 7. NoSQL — 22개

1. NoSQL 특징 — 비정형/반정형, 수평 확장, BASE 원칙
2. BASE 원칙 — 기본적 가용성(BA)/소프트 상태(S)/최종 일관성(E)
3. CAP 정리 (Brewer's Theorem) — CP / AP / CA 불가
4. PACELC — CAP 확장, 지연(Latency) 고려
5. 문서 DB (Document DB) — MongoDB, CouchDB, Firestore
6. 키-값 DB (Key-Value DB) — Redis, DynamoDB, Riak
7. 컬럼 패밀리 DB (Column-Family) — Apache Cassandra, HBase
8. 그래프 DB (Graph DB) — Neo4j, Amazon Neptune, ArangoDB
9. 시계열 DB (Time-Series DB) — InfluxDB, TimescaleDB, Prometheus
10. 검색 엔진 DB — Elasticsearch, OpenSearch, Solr
11. 공간 DB (Spatial DB) — PostGIS, SpatiaLite
12. MongoDB BSON 구조 — 컬렉션, 도큐먼트, 중첩
13. MongoDB 인덱스 — 복합/텍스트/지리공간/TTL
14. Redis 자료구조 — String/Hash/List/Set/Sorted Set/Stream
15. Redis 클러스터링 — 샤딩, 복제, Sentinel, Cluster 모드
16. Cassandra 아키텍처 — 링 토폴로지, 복제 전략, Consistent Hashing
17. Cassandra 일관성 수준 — ONE / QUORUM / ALL
18. HBase — Hadoop 기반, 희소 컬럼, 압축
19. 벡터 데이터베이스 (Vector DB) — Pinecone, Weaviate, Milvus, Chroma
20. 멀티모델 DB — ArangoDB, CosmosDB, FaunaDB
21. NewSQL — CockroachDB, Google Spanner, TiDB — ACID + 수평 확장
22. 그래프 DB 쿼리 — Cypher (Neo4j), Gremlin, SPARQL

---

## 8. 분산 데이터베이스 — 18개

1. 분산 데이터베이스 (Distributed DB) 개념 — 투명성
2. 분산 투명성 — 위치/복제/분할/장애/동시성 투명성
3. 데이터 분할 — 수평 분할 / 수직 분할 / 혼합 분할
4. 데이터 복제 (Replication) — 동기/비동기, 마스터/슬레이브
5. 2PC (Two-Phase Commit) — 준비/커밋 단계, 코디네이터
6. 3PC (Three-Phase Commit) — 블록킹 방지, 추가 단계
7. Saga 패턴 — 분산 트랜잭션, 보상 트랜잭션
8. Paxos — 분산 합의 알고리즘
9. Raft — Paxos 단순화, 리더 선출, Log 복제
10. 수평 샤딩 (Sharding) — 데이터 파티셔닝, 해시/범위 기반
11. 글로벌 트랜잭션 — XA 트랜잭션, 분산 잠금
12. 최종 일관성 (Eventual Consistency)
13. 강한 일관성 (Strong Consistency)
14. 읽기-쓰기 일관성 — 쓰기 후 읽기 (Read-Your-Writes)
15. 복제 지연 (Replication Lag) — 비동기 복제의 한계
16. CRDTs (Conflict-free Replicated Data Types) — 충돌 없는 병합
17. Google Spanner — TrueTime, 전역 일관성
18. Amazon DynamoDB — 도큐먼트+키값, 서버리스, 어댑티브 용량

---

## 9. 데이터 웨어하우스 / 빅데이터 분석 — 20개

1. 데이터 웨어하우스 (DW) — 주제 지향, 통합, 시간 변화, 비휘발
2. OLTP vs OLAP — 트랜잭션 vs 분석
3. 다차원 모델 (Multidimensional Model) — 큐브, 사실/차원 테이블
4. 스타 스키마 (Star Schema) — 사실 테이블 + 차원 테이블
5. 눈송이 스키마 (Snowflake Schema) — 차원 정규화
6. ETL (Extract, Transform, Load)
7. ELT (Extract, Load, Transform) — 클라우드 DW 트렌드
8. 데이터 마트 (Data Mart) — 부서별 DW 서브셋
9. OLAP 큐브 연산 — Drill-Down / Roll-Up / Slice / Dice / Pivot
10. MOLAP / ROLAP / HOLAP 비교
11. 데이터 레이크 (Data Lake) — 원시 데이터, S3/HDFS
12. 레이크하우스 (Lakehouse) — DW + 데이터레이크, Delta Lake, Apache Iceberg, Hudi
13. 데이터 메시 (Data Mesh) — 분산 소유권, 도메인 기반
14. 데이터 패브릭 (Data Fabric) — 연합 통합, 메타데이터
15. CDC (Change Data Capture) — 변경 캡처, Debezium
16. 데이터 카탈로그 (Data Catalog) — 메타데이터 관리
17. 마스터 데이터 관리 (MDM) — 황금 레코드
18. BI 도구 — Tableau / Power BI / Looker / Superset
19. 컬럼 지향 DB (Columnar) — ClickHouse, Redshift, BigQuery
20. 실시간 분석 — Apache Flink, Druid, Pinot, Kafka Streams

---

## 10. 데이터 거버넌스 / 최신 동향 — 14개

1. 데이터 거버넌스 (Data Governance) — 정책/프로세스/조직
2. 데이터 품질 관리 — 완전성/정확성/일관성/적시성
3. 데이터 보안 — 접근 제어, 암호화, 마스킹, 감사
4. 개인정보 보호 — GDPR, 개인정보보호법, DPO
5. 데이터 마스킹 (Data Masking) — 민감 데이터 보호
6. 컬럼 수준 암호화 — 투명 데이터 암호화 (TDE)
7. 행 수준 보안 (Row-Level Security, RLS)
8. 데이터 계보 (Data Lineage) — 데이터 흐름 추적
9. HTAP (Hybrid Transactional/Analytical Processing) — 실시간 분석+트랜잭션
10. 서버리스 DB — Aurora Serverless, Neon, PlanetScale
11. AI/ML 통합 DB — ML 모델 in-DB (PostgreSQL ML, BigQueryML)
12. 그래프 분석 — 사기 탐지, 추천, 네트워크 분석
13. 공간-시간 데이터 분석 — PostGIS, TimescaleDB
14. 양자 내성 암호화 (Post-Quantum Cryptography) — DB 암호 대비

---

**총 키워드 수: 192개**
