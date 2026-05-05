+++
weight = 43
title = "43. 람다 아키텍처 — 배치 & 스피드 레이어"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: 람다 아키텍처(Lambda Architecture)는 Nathan Marz가 제안한 데이터 처리 아키텍처로 — 배치 레이어(정확성), 스피드 레이어(실시간성), 서빙 레이어(통합 조회)의 3계층으로 "정확하고 빠른" 데이터 처리를 달성하지만, 동일 로직을 두 번 구현해야 하는 "코드 중복" 문제가 근본 한계이다.
> **비유**: 단일 기능의 기술이 아니라, 흐름과 기준과 운영 판단이 함께 맞물릴 때 의미가 생기는 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

람다 아키텍처 — 배치 & 스피드 레이어은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```
람다 아키텍처 (Lambda Architecture):
  Nathan Marz (Twitter) 제안, 2012
  
  데이터 소스
      │
      ├── 배치 레이어 (Batch Layer) ──────────┐
      │   - 전체 히스토리 데이터 처리         │
      │   - 높은 정확성, 느린 처리(시간~일)   │
      │   - Hadoop MapReduce, Spark Batch     │
      │   - Batch View (하루치 집계 등)       │
      │                                      │
      ├── 스피드 레이어 (Speed Layer) ─────────┤
      │   - 최근 데이터만 처리 (배치 지연 보완)│
      │   - 낮은 지연(수초 이내), 근사치 허용 │
      │   - Storm, Flink, Spark Streaming    │
      │   - Realtime View (최신 수분 데이터)  │
      │                                      │
      └──────────────────────────────────────┤
                                             ↓
                               서빙 레이어 (Serving Layer)
                               - Batch View + Realtime View 병합
                               - 쿼리 응답 (HBase, Cassandra)
                               - 쿼리: Batch + Speed 조합 결과

핵심 원칙:
  1. 불변성 (Immutability): 원본 데이터 수정 없음
  2. 재계산 (Recomputation): 배치 레이어는 전체 재계산 가능
  3. 정확성 (Accuracy): 배치 레이어가 최종 정확한 답 제공
```

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```
배치 레이어 (Batch Layer):

특징:
  전체 데이터셋(역사적 데이터 포함)을 처리
  정확성 최우선
  지연 허용 (시간 ~ 일 단위)
  
데이터 스토어:
  HDFS, Amazon S3, Azure ADLS
  포맷: Parquet, ORC (컬럼 지향, 압축 효율)

처리 엔진:
  Apache Hadoop MapReduce (초기)
  Apache Spark (현재 표준)
    - 인메모리 처리 → 10~100배 빠름
    - Spark SQL, DataFrame API

배치 뷰 (Batch View):
  집계/변환 결과를 미리 계산해서 저장
  예: 일별 판매 합계, 월별 사용자 활동 통계

배치 처리 주기:
  일간 배치: 매일 새벽 2시 (D-1 데이터)
  주간 배치: 월요일 새벽 (주간 통계)
  임시 전체 재처리: 스키마 변경 시

배치 레이어 한계:
  지연: 방금 발생한 이벤트는 내일 집계에 포함
  → 사용자가 "오늘 내 구매 합계"를 보려면?
  → 스피드 레이어 필요

Apache Spark 배치 예시:
  spark.read.parquet("s3://data/events/2026-04-05/")
    .groupBy("user_id", "date")
    .agg(sum("amount").alias("daily_total"))
    .write.parquet("s3://batch-views/daily_user_total/")
```

---

## 3. 구조 및 원리

**핵심 조건**: 람다 아키텍처 — 배치 & 스피드 레이어은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

```
스피드 레이어 (Speed Layer):

특징:
  최근 데이터만 처리 (배치 지연 구간 보완)
  낮은 지연 최우선 (수초~수분)
  근사치 허용 (정확성 < 속도)
  처리 완료 시 데이터 삭제 (배치가 최종 권위)

처리 엔진:
  Apache Storm: 지연 최소화 (수ms)
  Apache Spark Streaming: 마이크로 배치 (수초)
  Apache Flink: 진정한 스트리밍 + 이벤트 타임
  Kafka Streams: 경량, 라이브러리 형태

리얼타임 뷰 (Realtime View):
  배치 뷰의 최신화 역할
  예: "오늘 현재까지" 집계 (배치 뷰 없는 부분)

스피드 레이어 한계:
  지연 보상 로직: 배치와 동일 비즈니스 로직 재구현 필요
  → 코드 중복 = 람다의 핵심 문제

쿼리 시 조합:
  총 판매액 쿼리:
    결과 = Batch View (어제까지) + Realtime View (오늘 현재)
    
  코드:
    batch_result = query_hbase("batch_view", user_id, date_range)
    speed_result = query_cassandra("speed_view", user_id, today)
    total = batch_result + speed_result

Flink 스트리밍 예시:
  DataStream<Event> stream = env.addSource(kafkaConsumer);
  stream
    .keyBy(event -> event.getUserId())
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .sum("amount")
    .addSink(cassandraSink);
```

---

## 4. 비교 및 연결

```
람다의 문제:
  동일 비즈니스 로직을 두 번 구현
    배치: Spark SQL로 집계 로직
    스피드: Flink로 동일 집계 로직
  → 코드 불일치 위험
  → 유지보수 비용 2배

카파 아키텍처 (Kappa Architecture):
  Jay Kreps (LinkedIn) 제안, 2014
  
  핵심: 스트리밍 레이어 하나로 통합
  
  데이터 소스 → Kafka (로그 저장) → 스트리밍 처리 → 서빙

  배치 재처리가 필요하면:
    Kafka에 전체 로그 보관 (Kafka Log Compaction)
    스트리밍 처리를 처음부터 재실행 (재처리 = 스트리밍)

람다 vs 카파 비교:

항목            | 람다                  | 카파
----------------+-----------------------+---------------------------
코드 복잡도     | 높음 (로직 2회 구현)  | 낮음 (스트리밍만)
재처리          | 배치 재실행 (빠름)    | 스트리밍 재처리 (느리고 비용)
정확성          | 높음 (배치 최종 권위) | 높음 (이벤트 타임 Flink)
인프라 복잡도   | 높음 (2레이어)        | 낮음 (1레이어)
대규모 재처리   | 유리                  | 불리 (자원 많이 소요)

현대 트렌드:
  Databricks Delta Live Tables:
    배치 + 스트리밍을 동일 코드로 처리
    람다의 이점 + 카파의 단순성
    
  Apache Flink + Apache Iceberg:
    스트리밍 처리 + 배치 쿼리 통합
    = Kappa + 대규모 재처리 개선
```

---

## 5. 실무 적용 및 판단

```
이커머스 판매 대시보드 람다 아키텍처:

요구사항:
  "현재 판매 현황" 대시보드 (수초 지연 허용)
  "월간 매출 통계" 보고서 (일 1회 배치)

람다 아키텍처 구현:

  데이터 소스:
    주문 서비스 → Kafka 토픽 (orders)

  배치 레이어:
    Spark on EMR, 매일 새벽 3시 실행
    S3 Parquet (원본) → 일별/월별 집계 → HBase (batch view)
    
  스피드 레이어:
    Kafka → Flink → Cassandra (speed view)
    Tumbling Window: 1분 단위 집계
    
  서빙 레이어:
    대시보드 API:
      GET /dashboard/sales?date=today
      
      Response:
        historical (배치 뷰, HBase): 어제까지 합계
        realtime (스피드 뷰, Cassandra): 오늘 지금까지
        total = historical + realtime

성능:
  배치 정확성: D-1 기준 정확
  스피드 지연: ~30초
  쿼리 응답: 100ms 이내

카파로 전환 검토:
  문제: 동일 집계 로직 Spark + Flink 중복
  해결: Flink로 통합 + Kafka 24시간 로그 보관
  
  전환 후:
    코드 50% 감소
    인프라 40% 단순화
    재처리: Kafka lag으로 처음부터 재실행 (수시간 소요)
```

---

## 6. 기대효과 및 결론

람다 아키텍처 — 배치 & 스피드 레이어의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```
[분산 배치 처리 (2004)]
Google MapReduce, Hadoop
      |
      v
[람다 아키텍처 제안 (2012)]
Nathan Marz: 배치 + 스피드 통합
"Big Data" 책 출판
      |
      v
[카파 아키텍처 제안 (2014)]
Jay Kreps (LinkedIn): 스트리밍으로 통합
Kafka 기반 단일 파이프라인
      |
      v
[실시간 처리 고도화 (2015~)]
Apache Flink: 이벤트 타임, 정확한 스트리밍
Spark Structured Streaming
      |
      v
[현재: 통합 데이터 플랫폼]
Delta Live Tables (Databricks)
배치+스트리밍 동일 코드
Apache Iceberg + Flink
```

---

## 8. 관련 개념 맵

```
람다 아키텍처
+-- 3계층
|   +-- 배치 레이어 (Spark, Hadoop)
|   +-- 스피드 레이어 (Flink, Storm)
|   +-- 서빙 레이어 (HBase, Cassandra)
+-- 장단점
|   +-- 장점: 정확성 + 실시간성 동시
|   +-- 단점: 코드 중복
+-- 대안
|   +-- 카파 아키텍처 (스트리밍 통합)
|   +-- Delta Live Tables (Databricks)
+-- 관련 기술
|   +-- Apache Kafka, Flink, Spark
|   +-- Apache Iceberg
```
