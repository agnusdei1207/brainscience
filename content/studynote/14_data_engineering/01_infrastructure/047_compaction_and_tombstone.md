+++
weight = 47
title = "47. 컴팩션과 툼스톤 — Compaction & Tombstone"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: 컴팩션(Compaction)은 LSM 트리 기반 DB에서 여러 SSTable을 합쳐 중복 제거와 공간 효율화를 수행하는 백그라운드 프로세스 — Cassandra·RocksDB·HBase에서 지속적으로 발생하며, 쓰기 증폭(Write Amplification)과 공간 효율 사이의 트레이드오프를 관리한다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

컴팩션과 툼스톤 — Compaction & Tombstone은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
컴팩션 필요성:

LSM 쓰기 특성:
  MemTable → 플러시 → SSTable 생성
  같은 키의 새 값 → 새 SSTable에 저장
  (기존 SSTable 수정 X, 불변)
  
  결과:
  키 K1의 버전 1: SSTable A에
  키 K1의 버전 2: SSTable B에
  키 K1의 버전 3: SSTable C에
  
  읽기 시: SSTable A, B, C 모두 확인 필요
  → 읽기 오버헤드 증가

컴팩션 역할:
  SSTable A + B + C → SSTable D (합병)
  키 K1: 버전 3만 남김 (버전 1, 2 제거)
  
  효과:
  1. 읽기 성능 향상 (확인할 파일 수 감소)
  2. 공간 효율화 (중복 제거)
  3. 툼스톤 실제 삭제

컴팩션 비용:
  CPU: 파일 병합, 정렬
  I/O: 대용량 파일 읽기 + 쓰기
  임시 공간: 원본 + 결과물 동시 보유
  
  → 컴팩션 집중 시 프로덕션 성능 영향
  → Rate Limiter로 속도 제한 필요

Write Amplification:
  논리적 쓰기 1MB → 실제 디스크 쓰기 10MB?
  WA = 실제 쓰기 / 논리 쓰기
  
  높은 WA: 컴팩션 오버헤드 큰 전략
  SSD 수명 영향: 쓰기 횟수 제한
```

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```
툼스톤 (Tombstone):

문제: LSM에서 즉각 삭제 불가
  SSTable은 불변(Immutable)
  → 기존 SSTable의 특정 키 삭제 불가

해결: 삭제 마커(Tombstone) 쓰기
  DELETE FROM users WHERE id = 1
  → MemTable에 Tombstone(id=1) 쓰기
  → SSTable로 플러시
  
  실제 삭제는 컴팩션 시:
  Tombstone과 원본 데이터 같이 있으면 → 제거
  
  읽기 시 Tombstone 처리:
  id=1 데이터 찾기
  SSTable에서 id=1 Tombstone 발견
  → "삭제됨"으로 처리, 반환 안 함

Tombstone 유형 (Cassandra):

Cell Tombstone: 단일 셀 삭제
Row Tombstone: 전체 행 삭제
Range Tombstone: 범위 삭제 (CLUSTERING 컬럼)
TTL Tombstone: TTL 만료 시 자동 생성

Tombstone 문제 (Tombstone Hell):

시나리오:
  DELETE 집중 워크로드
  또는 TTL 많은 데이터 (IoT, 로그)
  
  컴팩션 늦으면:
  Tombstone 수백만 개 축적
  
  읽기 시:
  데이터 1개 찾는데 Tombstone 100만개 확인
  
  카산드라 tomb_failure_threshold:
  기본 100,000개 → 초과 시 경고/오류

GC Grace Period:
  Tombstone이 실제 삭제되기까지 대기 시간
  Cassandra 기본: 10일 (864,000초)
  
  이유: 복제 노드가 Tombstone 전파 보장
  만약 3일 후 오프라인 노드 복귀:
  GC Grace 10일 이내 → Tombstone 전파 OK
  
  단, 10일 동안 Tombstone 축적됨
```

---

## 3. 구조 및 원리

**핵심 조건**: 컴팩션과 툼스톤 — Compaction & Tombstone은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```
Cassandra 컴팩션 전략:

1. STCS (Size-Tiered Compaction Strategy):
  기본 전략
  
  동작: 비슷한 크기의 SSTable N개 → 하나로 합침
  
  예:
  4개의 50MB SSTable → 200MB SSTable
  4개의 200MB SSTable → 800MB SSTable
  
  장점:
  쓰기 최적화 (Write-Heavy 적합)
  컴팩션 빈도 낮음
  
  단점:
  읽기 시 여러 파일 확인
  공간 사용 증가 (임시 공간 필요)
  Tombstone 오래 축적
  
  적합: 쓰기 집중, 데이터 변경 적음

2. LCS (Leveled Compaction Strategy):
  각 레벨에서 키 범위 비중첩 보장
  
  L0: 새 SSTable들
  L1: 최대 크기 제한 (예: 160MB)
  L2: L1 × 10 (1600MB)
  ...
  
  장점:
  읽기 최적화 (각 레벨 1개 파일만 확인)
  공간 효율적
  Tombstone 빠른 제거
  
  단점:
  쓰기 증폭 높음 (더 많은 컴팩션)
  쓰기 집중 워크로드에 I/O 과부하
  
  적합: 읽기 집중, 업데이트 많음

3. TWCS (Time Window Compaction Strategy):
  시계열 데이터 특화
  
  동작: 시간 윈도우(예: 1일)로 SSTable 분류
  같은 시간 윈도우 내 SSTable만 합침
  
  장점:
  오래된 데이터(변경 없음) = 컴팩션 안 함
  TTL 데이터 효율적 삭제
  
  단점:
  시계열 외 워크로드에 비효율
  
  적합: 시계열 IoT, 로그, 이벤트 데이터
```

---

## 4. 비교 및 연결

```
컴팩션 모니터링 핵심 지표:

Cassandra 주요 메트릭:

1. PendingCompactions:
  현재 대기 중인 컴팩션 수
  정상: < 100
  위험: > 1000 (컴팩션 쌓임 = 읽기 저하)

2. TotalDiskSpaceUsed:
  데이터 디스크 사용량 추적
  급격히 증가 = Tombstone 축적 또는 컴팩션 미실행

3. LiveSSTableCount:
  테이블당 SSTable 수
  STCS: < 20 정상
  많을수록 읽기 오버헤드

4. TombstoneScannedHistogram:
  읽기 당 스캔한 Tombstone 수
  높으면 Tombstone 문제

5. CompactionBytesWrittenPerSec:
  컴팩션 I/O
  너무 높으면 프로덕션 영향

Tombstone 문제 해결:

진단:
  nodetool compactionstats
  → 대기 컴팩션 확인
  
  nodetool tablestats <keyspace>.<table>
  → LiveSSTableCount, TombstoneScannedHistogram

해결:
  1. 강제 컴팩션:
  nodetool compact <keyspace> <table>
  → 즉시 컴팩션 실행 (IO 집중!)
  
  2. GC Grace 조정:
  ALTER TABLE ... WITH gc_grace_seconds = 86400;
  (10일 → 1일)
  데이터 손실 위험 검토 후 적용
  
  3. TWCS 전환:
  시계열 데이터 → TWCS로 전략 변경

RocksDB 모니터링:
  db.GetProperty("rocksdb.stats") → 전체 통계
  db.GetProperty("rocksdb.compaction-pending") → 대기 수
```

---

## 5. 실무 적용 및 판단

```
IoT 플랫폼 Cassandra 컴팩션 최적화:

현황:
  센서 10,000개, 데이터 보존 90일
  TTL 설정: 90일 (7,776,000초)
  기본 STCS 전략 사용
  
  문제:
  읽기 지연 급증: P99 5초 (목표 1초)
  디스크 사용량 계속 증가
  
  진단:
  nodetool tablestats → TombstoneScannedHistogram: 평균 500,000!
  LiveSSTableCount: 350개 (매우 많음)
  
  원인:
  TTL 만료 → Tombstone 대량 생성
  STCS: Tombstone 포함 SSTable이 쌓임
  컴팩션이 Tombstone 제거 못 따라감

최적화:

1. TWCS 전략 전환:
  ALTER TABLE sensor_data
  WITH compaction = {'class': 'TimeWindowCompactionStrategy',
    'compaction_window_unit': 'DAYS',
    'compaction_window_size': '1'};
  
  효과: 오래된(TTL 만료) 시간 윈도우 자동 정리
  Tombstone 축적 90% 감소

2. GC Grace 단축:
  단일 DC, 실시간 데이터:
  ALTER TABLE sensor_data WITH gc_grace_seconds = 86400; (1일)
  
  주의: 2개 이상 DC면 단축 위험 있음

3. 불필요 DELETE 제거:
  TTL로 자동 만료 → 명시적 DELETE 불필요
  비즈니스 로직 DELETE만 유지

결과:
  P99 읽기: 5초 → 0.8초
  TombstoneScannedHistogram: 500,000 → 2,000
  LiveSSTableCount: 350 → 12 (시간 윈도우 수)
  디스크: 정상 범위 유지

운영 교훈:
  IoT 시계열 + TTL 많으면 TWCS 필수
  STCS + TTL + Tombstone = 읽기 재앙
  초기 설계부터 컴팩션 전략 고려
```

---

## 6. 기대효과 및 결론

컴팩션과 툼스톤 — Compaction & Tombstone의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```
[LSM 트리 제안 (1996)]
Patrick O'Neil 등
컴팩션 개념 포함
      |
      v
[LevelDB (2011)]
Google 구현
Level Compaction
      |
      v
[Cassandra 컴팩션 발전 (2012~)]
STCS → LCS → TWCS
IoT/시계열 워크로드 최적화
      |
      v
[RocksDB 전략 다양화 (2013~)]
Universal, FIFO, Level
티어드 스토리지 통합
      |
      v
[현재: 자동 컴팩션 최적화]
머신러닝 기반 전략 선택
클라우드 관리형 서비스
```

---

## 8. 관련 개념 맵

```
컴팩션 & 툼스톤
+-- 컴팩션 전략 (Cassandra)
|   +-- STCS (쓰기 최적, 기본)
|   +-- LCS (읽기 최적)
|   +-- TWCS (시계열 최적)
+-- 툼스톤
|   +-- 삭제 마커
|   +-- GC Grace Period
|   +-- Tombstone 문제
+-- 관련 개념
|   +-- LSM 트리
|   +-- SSTable (불변 파일)
|   +-- Write Amplification
+-- 모니터링
    +-- PendingCompactions
    +-- TombstoneScannedHistogram
    +-- LiveSSTableCount
```
