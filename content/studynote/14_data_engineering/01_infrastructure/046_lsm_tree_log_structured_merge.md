+++
weight = 46
title = "46. LSM 트리 — Log-Structured Merge-Tree"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: LSM(Log-Structured Merge-Tree) 트리는 쓰기 집약적 워크로드에 최적화된 데이터 구조 — 임의 쓰기(Random Write)를 순차 쓰기(Sequential Write)로 변환해 HDD/SSD에서 극적인 쓰기 성능을 달성하며, RocksDB·Cassandra·HBase·LevelDB의 스토리지 엔진으로 사용된다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

LSM 트리 — Log-Structured Merge-Tree은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
쓰기 문제와 LSM 솔루션:

B-Tree (전통 RDBMS):
  임의 쓰기 (Random Write):
  데이터 → 페이지 탐색 → 디스크 랜덤 위치 쓰기
  
  HDD 랜덤 쓰기: ~150 IOPS (매우 느림)
  SSD 랜덤 쓰기: ~10,000 IOPS
  
LSM 아이디어:
  임의 쓰기 → 순차 쓰기로 변환
  
  "모든 쓰기를 메모리에 먼저 모은 후
   순차적으로 디스크에 한번에 기록"
  
  HDD 순차 쓰기: ~200 MB/s (랜덤 대비 1,000×)
  SSD 순차 쓰기: ~3,000 MB/s

LSM 활용 사례:
  RocksDB: Facebook 개발, 광범위 사용
  LevelDB: Google 개발 (RocksDB 원조)
  Cassandra: SSTable + LSM
  HBase: HDFS 기반 LSM
  InfluxDB: 시계열 DB LSM
  TiKV: TiDB 스토리지 엔진

LSM 장점:
  높은 쓰기 처리량
  순차 쓰기 → HDD/SSD 친화적
  Write Amplification 낮음 (B-Tree 대비)

LSM 단점:
  읽기 성능 낮음 (여러 레벨 검색)
  Compaction 오버헤드
  Read Amplification
  Space Amplification
```

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```
LSM 트리 구성:

MemTable (메모리):
  인메모리 정렬된 자료구조
  보통 Red-Black Tree 또는 Skip List
  
  모든 쓰기가 먼저 MemTable에 삽입
  크기 임계값 (예: 64MB) 도달 시 플러시
  
  WAL (Write-Ahead Log):
  장애 복구를 위해 디스크에도 순차 로그
  MemTable 소실 시 WAL로 복구

SSTable (Sorted String Table):
  MemTable이 플러시될 때 생성
  불변(Immutable): 한번 쓰면 수정 불가
  정렬된 키-값 파일
  
  Level 0 (L0):
  MemTable → L0 SSTable (최신 데이터)
  L0 파일 수 임계값 → L1으로 Compaction
  
  Level 1 (L1):
  키 범위가 겹치지 않도록 정렬
  
  Level N (Ln):
  각 레벨: 이전 레벨 × 10배 크기
  L0: 수MB
  L1: 10MB
  L2: 100MB
  L3: 1GB
  ...

쓰기 과정:
  1. WAL에 순차 쓰기 (내구성)
  2. MemTable에 삽입
  3. MemTable 가득 차면 L0에 플러시
  4. L0 가득 차면 L1으로 Compaction

읽기 과정:
  1. MemTable 검색 (최신)
  2. L0 SSTable 검색 (최신순)
  3. L1 → L2 → ... 검색
  → 최악: 모든 레벨 검색 (느림)
  → Bloom Filter로 불필요한 탐색 건너뜀
```

---

## 3. 구조 및 원리

**핵심 조건**: LSM 트리 — Log-Structured Merge-Tree은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```
Compaction (컴팩션):

역할: LSM의 핵심 백그라운드 프로세스
     여러 SSTable을 합쳐 정렬된 파일 생성

왜 필요한가:
  LSM 쓰기: 항상 새 SSTable 추가
  같은 키가 여러 파일에 존재 가능
  → 읽기 시 여러 파일 검색
  → 오래된 데이터(tombstone) 공간 낭비

Compaction 유형:

Size-Tiered Compaction (크기 기반):
  비슷한 크기의 SSTable 여러 개 → 하나로 합침
  
  장점: Compaction 적게 발생
  단점: 임시 공간 많이 필요 (1.5~2× 데이터)
  사용: Cassandra 기본

Level Compaction (레벨 기반):
  LevelDB/RocksDB 방식
  L0 → L1으로, L1 → L2로 단계적 합침
  
  각 레벨은 겹치지 않는 키 범위
  읽기: 각 레벨에서 1개 SSTable만 확인
  
  장점: 읽기 성능 좋음, 공간 효율적
  단점: Compaction 자주 발생 (쓰기 증폭)

Bloom Filter (블룸 필터):
  "이 키가 이 SSTable에 없을 가능성 99.9%"를 O(1)에 판단
  
  확률적 자료구조 (False Positive 있지만 False Negative 없음)
  
  읽기 최적화:
  블룸 필터: "이 SSTable에 없음" → 건너뜀
  불필요한 디스크 I/O 90%+ 절감

Write Amplification:
  실제 쓰기 / 논리적 쓰기
  LSM Level Compaction: ~10×
  B-Tree: ~3~5× (낮음)
  → Compaction으로 인한 추가 쓰기
```

---

## 4. 비교 및 연결

```
B-Tree vs LSM 비교:

B-Tree:
  구조: 균형 트리, 인플레이스 업데이트
  쓰기: 임의 쓰기 (페이지 탐색 후 수정)
  읽기: 빠름 (트리 경로 = O(log n))
  공간: 페이지 낭비 있음 (~30%)
  
  Write Amp: 낮음 (데이터 한번에 쓰기)
  Read Amp: 낮음
  Space Amp: 중간
  
  최적: 읽기 많은 OLTP

LSM:
  구조: 순차 쓰기, 계층적 파일
  쓰기: 순차 쓰기 (10~1,000× 빠름)
  읽기: 느림 (여러 파일 검색)
  공간: 임시 Compaction 공간 필요
  
  Write Amp: 높음 (Compaction 추가 쓰기)
  Read Amp: 높음 (여러 레벨 검색)
  Space Amp: 높음 (중복 데이터)
  
  최적: 쓰기 집약적 워크로드

RUM Conjecture:
  Read / Update / Memory 트레이드오프
  
  R(읽기 오버헤드) × U(쓰기 오버헤드) × M(공간 오버헤드)
  → 셋 중 둘을 최소화하면 하나는 증가

선택 가이드:
  IoT 센서 데이터 수집: LSM (쓰기 우선)
  온라인 쇼핑 주문: B-Tree (읽기 빠름)
  시계열 DB (InfluxDB, Prometheus): LSM
  관계형 OLTP (MySQL): B-Tree
  로그 저장 (Kafka→Cassandra): LSM
```

---

## 5. 실무 적용 및 판단

```
스마트 공장 IoT 데이터 저장 (RocksDB + LSM):

요구사항:
  센서: 10,000개
  측정 주기: 1초
  데이터: 초당 10,000 쓰기
  보존 기간: 2년
  조회: 특정 센서의 최근 1시간 데이터

RocksDB 설정:
  MemTable 크기: 128MB
  L0 파일 수 트리거: 4
  L1 최대 크기: 256MB
  레벨 배율: 10×
  
  Bloom Filter: 활성화 (False Positive = 1%)
  Compaction: Level Compaction
  
  블록 캐시: 1GB (자주 조회 데이터)

성능 결과:
  쓰기 처리량: 초당 200,000 이상
  (10,000 IoT 포인트 × 20 여유)
  
  P99 쓰기 지연: < 1ms
  P99 읽기 지연: < 5ms (Bloom Filter 덕분)
  
  비교: MySQL InnoDB (B-Tree)
  동일 쓰기 워크로드:
  → 쓰기 처리량: 초당 30,000
  → P99 쓰기 지연: 10~50ms
  → 디스크 IOPS 포화 현상

Compaction 관리:
  TTL Compaction: 2년 지난 데이터 자동 삭제
  
  Compaction 백그라운드:
  쓰기 집중 시간 회피 (일과 후 집중)
  Rate Limiter: 초당 100MB 제한
  (프로덕션 영향 최소화)

확장:
  Kafka → Flink → RocksDB 파이프라인
  RocksDB Replication: Leader-Follower
  스냅샷 백업: S3로 주기적 백업
  
  2년 데이터: 약 2TB
  S3 Glacier 아카이브: 연 20만원
```

---

## 6. 기대효과 및 결론

LSM 트리 — Log-Structured Merge-Tree의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```
[B-Tree 한계 인식 (1990s)]
HDD 랜덤 I/O 병목
로그 파일 개념 등장
      |
      v
[LSM 제안 (1996)]
Patrick O'Neil 등
Log-Structured Merge-Tree 논문
      |
      v
[LevelDB (2011)]
Google Jeff Dean 팀
오픈소스 LSM 구현체
      |
      v
[RocksDB (2012)]
Facebook이 LevelDB 포크
멀티 스레드 Compaction
      |
      v
[NoSQL 표준 스토리지 (2015~)]
Cassandra, TiKV 등 채택
모바일(SQLite 대안), 임베디드 DB
```

---

## 8. 관련 개념 맵

```
LSM 트리 (Log-Structured Merge-Tree)
+-- 구성 요소
|   +-- MemTable (인메모리)
|   +-- SSTable (불변 파일)
|   +-- WAL (장애 복구)
+-- 핵심 프로세스
|   +-- Flush (MemTable → SSTable)
|   +-- Compaction (SSTable 합병)
+-- 최적화
|   +-- Bloom Filter (읽기 최적화)
|   +-- Block Cache
+-- 대표 구현체
    +-- RocksDB (Facebook)
    +-- LevelDB (Google)
    +-- Cassandra (SSTable)
    +-- HBase
```
