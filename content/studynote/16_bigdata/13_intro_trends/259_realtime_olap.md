+++
title = "047. 실시간 OLAP — ClickHouse·Druid·Pinot·StarRocks"
weight = 259
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 실시간 OLAP — ClickHouse·Druid·Pinot·StarRocks은(는) 빅데이터 전략과 거시적 변화 방향을 이해하기 위한 정책·시장·기술 트렌드 개념이다.
> **비유**: 멀리서 지형과 조류를 함께 보며 데이터 산업의 큰 흐름을 읽는 전망대와 같다.

📝 모범 답안

## 1. 개요 및 필요성

```
전통 분석 아키텍처의 한계:

ETL 배치 파이프라인:
  이벤트 발생 → Kafka → Spark Batch(1시간) → Hive → 리포트
  
  지연: 1~24시간
  문제: "오늘 캠페인 효과를 내일 봄"

Lambda 아키텍처:
  배치 레이어 + 속도 레이어 병행
  복잡도 증가, 두 레이어 데이터 불일치 문제

실시간 OLAP 필요성:
  이벤트 발생 → [실시간 OLAP 엔진] → 쿼리 결과
  지연: < 1초

대표 사용 사례:
  광고 기술: 실시간 CTR(클릭률), 노출 집계
  게임: 실시간 DAU, 아이템 구매 현황
  금융: 실시간 거래 모니터링 대시보드
  IoT: 수천 센서 실시간 집계
  전자상거래: 실시간 재고 + 판매 추적

실시간 OLAP 엔진:
  ClickHouse (Yandex, 2016)
  Apache Druid (MetaMarkets, 2012)
  Apache Pinot (LinkedIn, 2013)
  StarRocks (구 DorisDB, 2021)
```

---

## 2. 구성요소

```
ClickHouse (클릭하우스):
  개발: Yandex (러시아 구글)
  목적: Yandex.Metrica 웹 분석
  특징: 컬럼형 DBMS, 고성능 집계

핵심 기술:

1. 컬럼형 저장 (Columnar Storage):
  행: [사용자, 이벤트, 시간, 가격]×10억
  컬럼: 가격 컬럼만 읽어 SUM 계산
  → 불필요한 컬럼 I/O 없음
  
  압축률: 일반 대비 10~100배
  LZ4 / ZSTD 알고리즘 적용

2. 벡터화 실행 (Vectorized Execution):
  CPU SIMD 명령어 활용
  256비트 AVX: 한 번에 32개 값 처리
  
  SUM(price) 10억 행:
  일반: 10억 번 덧셈
  SIMD: 약 3,125만 번 (32배 빠름)

3. 파트 기반 쓰기 (MergeTree):
  쓰기: 작은 파트(Part)로 저장
  백그라운드 머지: 파트 주기적 병합
  (LSM과 유사하지만 OLAP 최적화)
  
  파티셔닝: 날짜별 파티션
  정렬 키: 자주 필터링하는 컬럼

벤치마크:
  쿼리: 100억 행 GROUP BY
  ClickHouse: ~5초
  Hive: ~300초 (60배 빠름)
  Spark: ~30초 (6배 빠름)

단점:
  UPDATE/DELETE: 비효율 (LSM 구조 특성)
  ACID: 부분적 지원
  JOIN: 큰 테이블 JOIN은 느림
  
적합 워크로드: 시계열, 로그 분석, 이벤트 스트림
```

---

## 3. 구조 및 원리

**핵심 조건**: 정책, 거버넌스, 플랫폼 구조, 산업 활용 방향을 함께 읽어야 한다.

동작 순서:
```
Apache Druid:
  아키텍처: 마이크로서비스 + Kafka 통합
  
  핵심 특징:
  1. 사전 집계 (Rollup):
    원본: 초당 100만 이벤트
    집계: 분당 사용자별 이벤트 수로 압축
    저장량: 100배 감소, 쿼리 100배 빠름
  
  2. 컬럼 사전 처리:
    인덱스: 비트맵 인덱스 자동 생성
    압축: 컬럼별 최적 압축
  
  3. 실시간 인제스트:
    Kafka → Druid 실시간 (스트리밍)
    Druid → S3/HDFS (배치 보완)
  
  노드 유형:
    Historical: 과거 데이터 쿼리
    MiddleManager: 실시간 인제스트
    Broker: 쿼리 라우팅
    Coordinator: 데이터 분배
  
  사용사례: Lyft, Netflix, Alibaba

Apache Pinot:
  개발: LinkedIn
  
  핵심 특징:
  1. 최저 지연 쿼리 (< 10ms):
    스타 트리 인덱스 (Star-Tree Index)
    자주 쓰는 집계를 미리 계산해 트리 형태로 저장
    
  2. Upsert 지원:
    실시간 업데이트 가능 (Druid는 어려움)
    사용자 프로필 실시간 업데이트 + 집계
  
  3. 멀티 스테이지 쿼리 엔진:
    복잡한 JOIN, 서브쿼리 지원
  
  사용사례: LinkedIn, Uber, Stripe

비교:
  Druid: 대용량 스트리밍, 집계 최적화
  Pinot: 초저지연, Upsert, LinkedIn 타입 집계
  ClickHouse: 복잡 SQL, 대용량 배치+스트리밍 혼합
```

---

## 4. 비교 및 연결

```
StarRocks (스타록스):
  구 DorisDB → StarRocks
  개발: 중국 빅테크, 2021 오픈소스
  
  포지셔닝: "통합 분석 플랫폼"
  OLAP + ETL 대체 (Spark 없애기)

핵심 특징:

1. MPP (Massively Parallel Processing):
  쿼리 자동 분산 실행
  각 노드 병렬 처리 후 집계
  
2. 벡터화 쿼리 엔진:
  ClickHouse와 유사 SIMD 최적화

3. CBO (Cost-Based Optimizer):
  쿼리 플랜 자동 최적화
  JOIN 순서, 인덱스 선택 자동화

4. 스토리지 유형:
  
  Primary Key 모델:
  Upsert 지원, 실시간 업데이트
  → 전자상거래 재고 실시간 업데이트
  
  Aggregate 모델:
  SUM/MAX/MIN 사전 집계
  → 광고 지표 집계
  
  Duplicate 모델:
  원본 데이터 그대로 저장
  → 로그 분석

5. 데이터 레이크 통합:
  S3/HDFS/Iceberg/Delta Lake 직접 쿼리
  (데이터 이동 없이)
  External Catalog 기능

6. 실시간 + 배치:
  Kafka Stream 실시간 인제스트
  S3 배치 로딩 동시 지원

사용사례:
  JD.com, 이마트24, Meituan
  
성능:
  TPC-H 벤치마크: Spark 대비 5~10배 빠름
  실시간 인제스트 + 즉시 쿼리 가능
```

---

## 5. 실무 적용 및 판단

```
광고 플랫폼 실시간 OLAP 아키텍처:

요구사항:
  일 이벤트: 500억 (노출+클릭+전환)
  쿼리: "광고주 X의 캠페인별 실시간 CTR"
  지연 목표: < 2초
  데이터 보존: 90일

문제:
  배치(Spark+Hive): 1시간 지연 → 광고주 불만
  
기존 아키텍처:
  AdServer → Kafka → Spark(1시간) → Hive → BI

신규 아키텍처:
  AdServer → Kafka → [Druid 실시간] → 대시보드
                  ↘ [S3 원본 저장] ← Spark 배치
  
  Druid 설정:
  Rollup: 초→분 집계 (광고주/캠페인/디바이스별)
  보존: 실시간 14일 (핫), S3 76일 (콜드)
  쿼리 패턴: GROUP BY 광고주, 캠페인, 날짜

결과:
  리포트 지연: 1시간 → 1분 이내
  쿼리 응답: < 2초 (P99)
  스토리지: Rollup으로 원본 대비 95% 감소
  (500억 이벤트/일 → 2.5억 집계 행/일)

광고주 피드백:
  "실시간 캠페인 최적화 가능해짐"
  "예산 소진 전 저성능 광고 즉시 중단"

비용 절감:
  Spark 클러스터 비용 40% 감소
  (배치 처리 감소)
```

---

## 6. 기대효과 및 결론

실시간 OLAP — ClickHouse·Druid·Pinot·StarRocks은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 거시 트렌드는 개별 제품 비교보다 데이터 산업 구조가 어디로 이동하는지 판단하게 해 주는 기준점이다.

---

## 7. 발전 흐름도

```
[Dremel (Google, 2010)]
컬럼형 쿼리 엔진
실시간 OLAP 선구자
      |
      v
[Apache Druid (2012)]
실시간 이벤트 집계
비트맵 인덱스
      |
      v
[ClickHouse (2016)]
벡터화 실행 엔진
초고속 SQL OLAP
      |
      v
[Apache Pinot (2018 오픈소스)]
초저지연 OLAP
Star-Tree 인덱스
      |
      v
[StarRocks, DuckDB (2021~)]
레이크하우스 통합 OLAP
임베디드/클라우드 실시간 분석
      |
      v
[현재: AI 통합 OLAP]
벡터 임베딩 통합
AI 자연어 쿼리
```

## 👶 어린이를 위한 3줄 비유 설명

1. 실시간 OLAP = 즉석 성적표 — 시험 끝나고 다음 날 성적 대신 즉시 결과! 광고, 게임, 금융에서 "지금 바로" 100억 개 계산!
2. ClickHouse = 초고속 집계기 — 가격 컬럼만 뽑아(컬럼형) CPU 32개씩 더하기(SIMD). 100억 행도 5초!
3. Druid Rollup = 미리 손질된 재료 — 500억 이벤트를 인제스트 시 2.5억 집계로 압축. 쿼리 시 가볍게 바로 답변!

---

## 8. 관련 개념 맵

```
실시간 OLAP
+-- 엔진
|   +-- ClickHouse (벡터화, 복잡 SQL)
|   +-- Apache Druid (스트리밍, Rollup)
|   +-- Apache Pinot (초저지연, Upsert)
|   +-- StarRocks (통합, 레이크하우스)
+-- 핵심 기술
|   +-- 컬럼형 저장소
|   +-- 벡터화 실행 (SIMD)
|   +-- 사전 집계 (Rollup)
|   +-- 비트맵 인덱스
+-- 비교 기준
    +-- 지연 시간
    +-- UPDATE 지원
    +-- 스트리밍 통합
```
