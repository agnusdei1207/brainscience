+++
weight = 218
title = "218. 스파크 스트리밍 / Structured Streaming"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: Spark Structured Streaming은 실시간 스트림 데이터를 "무한히 쌓이는 테이블(Unbounded Table)"로 추상화하여 배치와 동일한 DataFrame API로 처리하는 실시간 처리 엔진이며, 마이크로 배치와 연속 처리 두 모드를 지원한다.
> **비유**: Structured Streaming은 뉴스 자막 기계와 같다. 자막 기계는 기자가 전송하는 뉴스(스트림)를 화면 아래에 계속 추가하는 테이블처럼 처리하여, 매초 새로운 자막을 자동으로 표시한다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

기업의 데이터 처리 요구가 "어젯밤 로그 분석(배치)" 수준을 넘어 "지금 이 순간 이상 감지·추천·알림"으로 진화하면서 실시간 스트림 처리가 필수가 됐다. 넷플릭스가 사용자가 영상을 보는 동안 실시간으로 스트리밍 품질을 조정하고, 우버가 실시간으로 근방 드라이버를 매칭하는 것이 대표적 사례다.

초기 Spark Streaming(Spark 1.x)은 DStream(Discretized Stream) API를 사용했다. 스트림 데이터를 고정 시간 간격(예: 1초)으로 RDD로 쪼개어 배치처럼 처리하는 방식이었다. 동작은 했지만 이벤트 시간 처리, 상태 관리, exactly-once 보장이 복잡했다.

Spark 2.0에서 등장한 **Structured Streaming**은 완전히 재설계됐다. 핵심 아이디어: **스트림을 끝없이 행이 추가되는 테이블**로 본다. 개발자는 이 테이블에 배치와 동일한 DataFrame/SQL 쿼리를 작성하고, Spark이 내부적으로 마이크로 배치로 쿼리를 반복 실행하여 결과를 점진적으로 업데이트한다.

---

## 2. 구성요소

### Structured Streaming 실행 모델

```
  ┌────────────────────────────────────────────────────────────┐
  │               Structured Streaming 처리 모델                │
  ├────────────────────────────────────────────────────────────┤
  │                                                             │
  │  소스 (Kafka/File/Socket)                                   │
  │       │ 새 데이터 계속 유입                                  │
  │       ▼                                                     │
  │  Input Table (무한히 쌓이는 테이블 추상화)                   │
  │  ┌──────────────────────────────────────────────────────┐  │
  │  │ T=0 │ event_1, event_2                               │  │
  │  │ T=1 │ event_3, event_4, event_5                      │  │
  │  │ T=2 │ event_6                                        │  │
  │  │ ... │ (계속 쌓임)                                     │  │
  │  └──────────────────────────────────────────────────────┘  │
  │       │ 동일한 DataFrame 쿼리 적용                           │
  │       ▼                                                     │
  │  Result Table (쿼리 결과 테이블)                             │
  │       │                                                     │
  │       ▼ 마이크로 배치마다 업데이트                            │
  │  Output (Console/File/Kafka/DB 등)                          │
  └────────────────────────────────────────────────────────────┘
```

### Kafka 소스 연동 코드

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count
from pyspark.sql.types import StructType, StringType, LongType

spark = SparkSession.builder \
    .appName("RealtimeOrderAnalysis") \
    .getOrCreate()

# Kafka 소스 읽기 (실시간 스트림)
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "latest") \
    .load()

# JSON 파싱
schema = StructType() \
    .add("order_id", LongType()) \
    .add("user_id", LongType()) \
    .add("amount", LongType()) \
    .add("timestamp", LongType())

orders = kafka_df \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# 이벤트 시간 기반 윈도우 집계 (5분 윈도우, 1분 슬라이딩)
windowed_counts = orders \
    .withWatermark("timestamp", "10 minutes") \  # 지연 데이터 10분까지 허용
    .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("user_id")
    ) \
    .agg(count("order_id").alias("order_count"),
         sum("amount").alias("total_amount"))

# 싱크: 콘솔 출력 (처음 N개만, 개발용)
query = windowed_counts.writeStream \
    .outputMode("update") \      # 변경된 행만 출력
    .format("console") \
    .option("truncate", False) \
    .trigger(processingTime="10 seconds") \  # 10초마다 마이크로 배치
    .start()

query.awaitTermination()
```

### 윈도우 연산 유형

| 윈도우 유형 | 설명 | 예시 |
|:---|:---|:---|
| **Tumbling Window** | 겹치지 않는 고정 크기 윈도우 | 1분마다 초기화 |
| **Sliding Window** | 슬라이딩 간격으로 이동하는 윈도우 | 5분 윈도우, 1분마다 이동 |
| **Session Window** | 비활성 기간으로 세션 구분 | 30초 이상 이벤트 없으면 세션 종료 |

---

## 3. 구조 및 원리

**핵심 조건**: 변경 자동화와 운영 안정성은 별개가 아니라 하나의 루프이며, 빌드·검증·배포·관측·피드백이 끊기지 않아야 지속 개선이 가능하다.

동작 순서:
1. 변경 사항을 버전 관리 시스템에서 감지한다.
2. 빌드·테스트·보안 검증으로 변경의 품질을 빠르게 확인한다.
3. 승인된 산출물을 선언형 배포나 자동화 파이프라인으로 운영 환경에 반영한다.
4. 메트릭·로그·트레이스를 통해 실제 동작 결과를 관측한다.
5. 피드백을 다음 개선 주기에 연결해 반복적으로 신뢰성을 높인다.

### 처리 모드 비교

| 모드 | 최소 지연 | 처리량 | 정확도 | 사용 시나리오 |
|:---|:---:|:---:|:---:|:---|
| 마이크로 배치 (기본) | ~100ms | 높음 | Exactly-once | 대부분의 실시간 처리 |
| 연속 처리 (Spark 2.3+) | ~1ms | 낮음 | At-least-once | 초저지연 필요 시 |
| 배치 처리 (비교용) | 분~시간 | 최고 | Exactly-once | 대규모 비실시간 |

### 출력 모드 (OutputMode)

| 모드 | 설명 | 적합 쿼리 |
|:---|:---|:---|
| **Append** | 새로 추가된 행만 출력 | 집계 없는 변환, 워터마크 적용 시 |
| **Complete** | 결과 테이블 전체를 매번 출력 | 소규모 집계 결과 |
| **Update** | 변경된 행만 출력 | 집계 + 실시간 대시보드 |

### Spark Streaming vs Apache Flink

| 항목 | Spark Structured Streaming | Apache Flink |
|:---|:---|:---|
| 처리 방식 | 마이크로 배치 (기본) | 진정한 스트림 처리 |
| 지연 시간 | 수백ms~수 초 | ~수ms |
| 처리량 | 높음 | 중간 |
| 배치 통합 | ✅ (배치와 동일 API) | 별도 DataSet API |
| 상태 관리 | 좋음 | 매우 강함 |
| 적합 시나리오 | 처리량 우선 | 초저지연 필요 |

---

## 4. 비교 및 연결

**워터마크(Watermark) 설정**:
```python
# 이벤트 시간 vs 처리 시간
# 이벤트: 15:00:00에 발생 → 네트워크 지연으로 15:00:30에 도착
# 워터마크 10분 설정: 15:10:00 이후에는 15:00:00 이벤트를 늦은 데이터로 처리

windowed = df \
    .withWatermark("event_time", "10 minutes") \  # 10분 지연 허용
    .groupBy(
        window("event_time", "5 minutes"),
        "user_id"
    ) \
    .count()

# 워터마크 없으면: 지연 데이터 기다리느라 메모리 무한 증가
# 워터마크 있으면: 허용 시간 초과한 지연 데이터는 버리고 상태 메모리 정리
```

**Kafka → Spark → S3 파이프라인**:
```python
# Delta Lake로 실시간 데이터 저장 (ACID 트랜잭션 지원)
orders.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "s3://checkpoints/orders/") \
    .option("path", "s3://data/orders/") \
    .trigger(processingTime="30 seconds") \
    .start()
```

**기술사 판단 포인트**:
- Checkpoint Location은 장애 복구의 핵심이다. Spark가 재시작될 때 checkpoint에서 마지막 처리 오프셋을 읽어 중복 처리 없이 이어서 실행한다.
- 상태 있는 집계(Stateful Aggregation)는 상태가 메모리에 축적되므로, 워터마크로 오래된 상태를 주기적으로 정리해야 메모리 문제를 방지한다.
- Structured Streaming과 Delta Lake의 조합이 현대 실시간 데이터 레이크하우스 아키텍처의 표준이 되고 있다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 설명 |
|:---|:---|
| 배치·스트리밍 통합 | 동일한 DataFrame API로 배치와 스트리밍 처리 |
| Exactly-once 보장 | 체크포인팅과 멱등 싱크로 정확히 한 번 처리 |
| 이벤트 시간 처리 | 네트워크 지연 데이터를 워터마크로 처리 |
| Kafka 완전 통합 | 오프셋 관리·체크포인팅 자동화 |

Spark Structured Streaming은 "빅데이터 배치 처리의 강점을 실시간 처리로 확장"한 결과물이다. 카프카와의 통합, Delta Lake와의 조합으로 현대 Lambda 아키텍처와 Kappa 아키텍처를 모두 Spark 단일 플랫폼으로 구현할 수 있게 됐다. 정보통신기술사 시험에서 스트리밍 처리 아키텍처와 Kafka·Spark의 연계는 빈출 주제다.

---

## 6. 기대효과 및 결론

스파크 스트리밍 / Structured Streaming를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 스파크 스트리밍 / Structured Streaming의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
배치 처리 (지연 ↑, 실시간성 ↓)
    │
    ▼
Spark Streaming: 마이크로배치 (준실시간)
    │
    ▼
Structured Streaming: DataFrame API + Event-Time + Watermark
    │
    ▼
Flink: True Streaming (이벤트별 처리) · 정확히 한 번 보장
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Apache Kafka | Structured Streaming의 가장 일반적인 소스 |
| 워터마크 (Watermark) | 지연 데이터 처리와 상태 메모리 관리의 핵심 |
| 마이크로 배치 | Structured Streaming의 기본 실행 모드 |
| Delta Lake | Structured Streaming 결과 저장의 현대 표준 |
| Apache Flink | 초저지연 스트리밍에서 Spark의 대안 도구 |
| Exactly-once | 체크포인팅으로 보장하는 스트리밍 처리 의미론 |

---
