+++
weight = 269
title = "269. 소형 파일 문제 (Small File Problem) - 레이크하우스 최적화"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 레이크에 수만~수백만 개의 소형 파일(1MB 이하)이 쌓이면 HDFS NameNode 메모리 고갈, Spark 태스크 오버헤드 폭증, S3 LIST API 요청 급증으로 쿼리 성능이 수십 배 저하된다.
> 2. **가치**: Delta Lake의 `OPTIMIZE` + `ZORDER BY`와 Apache Hudi의 Compaction을 통해 소형 파일을 128MB~1GB 크기의 적정 파일로 병합하면 쿼리 속도가 5~100배 향상되고 스토리지 비용도 절감된다.
> 3. **판단 포인트**: 소형 파일은 스트리밍 마이크로배치(초당 수백 파일)와 세밀한 파티션 분할(날짜·시간·지역 등 다중 파티션)에서 발생하므로, 파티션 전략 설계 단계부터 예방하는 것이 사후 병합보다 효과적이다.

---

## Ⅰ. 개요 및 필요성

실시간 로그 수집 파이프라인이 1분에 수십 개의 파일을 S3에 저장한다고 하자. 하루가 지나면 수만 개 파일, 1년이면 수백만 개 파일이 쌓인다. 이것이 **소형 파일 문제(Small File Problem)**다.

```
[소형 파일 문제의 영향]

HDFS 상황:
NameNode 메모리: 각 파일/블록당 약 150 bytes 메모리 사용
100만 파일 × 150 bytes = 143 MB (메모리 고갈 위험!)
(일반 NameNode 힙: 수 GB → 수십억 파일이면 한계)

Spark 상황:
소형 파일 100만 개 쿼리:
- 태스크 생성: 100만 개 (스케줄링 오버헤드 폭증)
- 각 태스크: 1KB 파일 처리에 수십 ms 오버헤드
- 실제 데이터 처리 < 메타데이터 오버헤드 → 성능 역전!

S3 상황:
LIST API 호출: $0.005/1000요청
100만 파일 조회: 1000번 LIST 호출 = $5 쿼리당
대규모 쿼리 시 비용 폭증
```

📢 **섹션 요약 비유**: 소형 파일 문제는 창고에 물건을 하나하나 개별 봉투에 포장한 것이다. 봉투 수가 너무 많아서 창고 목록(NameNode) 관리가 더 힘들어지고, 물건 찾는 시간(쿼리)보다 봉투 여는 시간(메타데이터 처리)이 더 걸린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 소형 파일 발생 원인

| 원인 | 발생 패턴 | 대응 방법 |
|:---|:---|:---|
| **스트리밍 마이크로배치** | Spark/Flink가 배치마다 파일 생성 | 배치 크기 조절, 트리거 간격 증가 |
| **과도한 파티셔닝** | 날짜+시간+지역 다중 파티션 | 파티션 카디널리티 줄이기 |
| **잦은 배치 실행** | 분 단위 ETL | 시간 단위로 배치 통합 |
| **파티션별 소량 데이터** | 롱테일 파티션 | 파티션 프루닝 + 병합 |

### Delta Lake OPTIMIZE + ZORDER BY

```sql
-- 소형 파일 병합 (OPTIMIZE)
-- Target File Size: 기본 1GB
OPTIMIZE delta.`/data/events`;

-- 특정 파티션만 최적화
OPTIMIZE delta.`/data/events`
WHERE date = '2024-01-15';

-- ZORDER BY: 클러스터링 (관련 데이터를 같은 파일에)
-- country와 user_id로 자주 필터링하는 경우:
OPTIMIZE delta.`/data/events`
ZORDER BY (country, user_id);

-- 결과:
-- 이전: 10,000개 × 1MB 파일
-- 이후: 10개 × 1GB 파일 (1000배 파일 수 감소)
```

### Hudi Compaction 아키텍처

```
[Hudi Copy-on-Write vs Merge-on-Read]

Copy-on-Write (COW):
INSERT/UPDATE/DELETE
    │
    ▼
항상 새 Parquet 파일 생성 (소형 파일 주의)
    │
    ▼
읽기: 바로 Parquet 읽기 (빠름)

Merge-on-Read (MOR):
INSERT/UPDATE/DELETE
    │
    ▼
Base Parquet + Delta Log (Avro) 병렬 저장
(소형 파일 = Delta Log = 빠른 쓰기)
    │
    ▼ Compaction (배치)
Base Parquet 파일로 Delta Log 병합
    │
    ▼
읽기: 병합된 Parquet 읽기 (빠름)

Hudi Compaction 스케줄:
inline: 매 커밋마다 (쓰기 느림)
async: 별도 Spark 작업으로 (권장)
```

📢 **섹션 요약 비유**: Delta Lake OPTIMIZE는 서랍 정리다. 흩어진 서류들(소형 파일)을 주제별 폴더(ZORDER 기준)에 묶어서 큰 바인더(1GB 파일)로 정리한다. 찾을 때는 폴더 하나만 열면 된다.

---

## Ⅲ. 비교 및 연결

### 소형 파일 해결 도구 비교

| 도구 | 방법 | 실행 시점 | 특징 |
|:---|:---|:---|:---|
| **Delta Lake OPTIMIZE** | Bin-packing 병합 | 수동/스케줄 | ZORDER 동시 적용 |
| **Hudi Compaction** | MOR → COW 병합 | 인라인/비동기 | 실시간 쓰기 최적화 |
| **Iceberg RewriteDataFiles** | 파일 병합 | 수동/스케줄 | 멀티 엔진 지원 |
| **Spark repartition** | 출력 파일 수 제어 | 쓰기 시점 | 사전 예방 |
| **HDFS NameNode Federation** | NameNode 분산 | 아키텍처 수준 | 대규모 HDFS 클러스터 |

### 적정 파일 크기 기준

| 시스템 | 권장 파일 크기 | 이유 |
|:---|:---|:---|
| **HDFS** | 128MB~1GB | 블록 크기(기본 128MB) 단위 |
| **S3 (Spark)** | 128MB~1GB | Spark 파티션 크기 최적화 |
| **BigQuery** | 자동 관리 | 내부 마이크로파티션 자동 최적화 |
| **Snowflake** | 자동 관리 | 마이크로파티션 자동 크기 조정 |

📢 **섹션 요약 비유**: 적정 파일 크기는 "좋은 책 두께"와 같다. 너무 얇으면(소형 파일) 책 1페이지를 찾으려 서랍을 수천 번 열어야 하고, 너무 두꺼우면(대형 단일 파일) 병렬 처리가 불가능하다. 128MB~1GB가 현대 분산 시스템의 골디락스 구간이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 스트리밍 파이프라인의 소형 파일 예방

```python
# Spark Streaming: 파일 크기 최적화
(df.writeStream
    .format("delta")
    .option("checkpointLocation", "/checkpoints/events")
    # 마이크로배치 트리거 간격 늘리기
    .trigger(processingTime="5 minutes")  # 1분 → 5분으로 조정
    # 출력 파일 수 제한
    .option("maxRecordsPerFile", 1000000)  # 파일당 최대 레코드 수
    .start("/delta/events"))
```

```python
# 파티션 수 최적화 (과도한 소형 파일 방지)
df_optimized = (
    df
    .repartition(20)  # 출력 파일 수 = 20개
    .write
    .mode("append")
    .partitionBy("date")  # 날짜 파티션만 (시간 단위 제거)
    .parquet("/data/events")
)
```

### Auto Optimize (Delta Lake on Databricks)

```sql
-- 테이블 수준에서 자동 최적화 활성화
ALTER TABLE events
SET TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',  -- 쓰기 시 자동 파일 크기 조정
    'delta.autoOptimize.autoCompact' = 'true'     -- 자동 컴팩션
);
```

### 기술사 시험 판단 포인트

- **OPTIMIZE vs ZORDER**: OPTIMIZE는 파일 크기 병합, ZORDER는 데이터 물리 정렬 (결합 사용 권장)
- **NameNode 메모리 계산**: 파일 수 × 150 bytes → NameNode 힙 크기 설계에 반영
- **예방이 사후 치료보다 효율적**: 파티션 전략 설계 단계에서 파일 수를 제한하는 것이 핵심

📢 **섹션 요약 비유**: ZORDER BY는 도서관의 장르별 정렬이다. 단순히 책을 합치는(OPTIMIZE) 것을 넘어, 같은 주제의 책들이 같은 선반(파일)에 모이도록 정렬한다. "한국 소설" 검색 시 그 선반만 열면 되는 것처럼, 같은 country+user_id 데이터가 같은 파일에 모여 스캔 효율이 극대화된다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 영역 | 효과 |
|:---|:---|
| **쿼리 성능** | 소형 파일 100만 개 → 병합 10개 시 10~100배 속도 향상 |
| **NameNode 안정성** | 파일 수 감소로 NameNode 메모리 사용량 절감 |
| **S3 API 비용** | LIST 요청 수 감소로 API 호출 비용 절감 |
| **Spark 효율성** | 태스크 수 감소로 스케줄링 오버헤드 제거 |

### 한계 및 주의사항

- **OPTIMIZE 실행 비용**: 대규모 OPTIMIZE는 많은 CPU·I/O 소비 → 트래픽 없는 시간에 실행
- **ZORDER 효과 저하**: 필터 카디널리티가 낮으면 ZORDER 효과 제한적
- **증분 OPTIMIZE**: 전체 테이블이 아닌 변경된 파티션만 최적화하여 비용 절감
- **파일 크기 vs 병렬성 트레이드오프**: 파일이 너무 크면(> 1GB) Spark 병렬 처리 단위 감소

📢 **섹션 요약 비유**: 소형 파일 문제의 근본 원인 제거가 최선이다. 스트리밍 마이크로배치 간격을 늘리고, 파티션 컬럼 수를 줄이는 것이 OPTIMIZE를 주기적으로 실행하는 것보다 효율적이다. 어지르지 않는 것이 청소하는 것보다 낫다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| HDFS NameNode | 파일 메타데이터 관리, 소형 파일에 취약 |
| Delta Lake OPTIMIZE | 소형 파일 병합 + ZORDER 클러스터링 |
| Hudi Compaction | MOR 방식에서 베이스 파일로 병합 |
| Z-Order Indexing | 다차원 데이터 클러스터링으로 쿼리 효율화 |
| Iceberg | 멀티 엔진 지원 레이크하우스, 파일 병합 기능 |
| Spark Repartition | 쓰기 시점에 출력 파일 수를 제어하는 예방 수단 |

### 👶 어린이를 위한 3줄 비유 설명
1. 소형 파일 문제는 클레이(점토)를 아주 작은 콩알 크기로 나눠놓는 것이야. 1000개 콩알을 찾는 것보다 10개 덩어리를 찾는 게 훨씬 빠르지?
2. Delta Lake OPTIMIZE는 콩알들을 다시 큰 덩어리로 합쳐주는 거야. ZORDER는 같은 색끼리 모아서 합치는 거고.
3. 처음부터 너무 잘게 나누지 않는 게 최선이야. 스트리밍할 때 5분마다 파일 하나씩 만들면, 1분마다 만드는 것보다 파일이 5배 적어!
