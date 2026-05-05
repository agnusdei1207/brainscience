+++
weight = 179
title = "179. 시계열 DB (Time-Series Database)"
date = "2026-04-21"
[extra]
categories = "studynote-devops-sre"
+++
## 0. 핵심 인사이트

> **핵심**: 시계열 DB(TSDB)는 타임스탬프가 키인 데이터의 특성(단조 증가, 고빈도 쓰기, 범위 쿼리)에 최적화된 특수 목적 데이터베이스다.
> 2. **가치**: InfluxDB와 Prometheus TSDB는 델타 인코딩(Delta Encoding), 고릴라 압축(Gorilla Compression), 다운샘플링(Downsampling)을 통해 일반 RDBMS 대비 10~100배 공간 효율을 달성한다.
> 3. **판단 포인트**: 메트릭 보존 기간, 카디널리티(Cardinality), 쿼리 패턴(최근 데이터 vs 장기 집계)에 따라 Prometheus TSDB, InfluxDB, Thanos/Cortex를 선택한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

시계열 데이터(Time-Series Data)는 동일한 메트릭이 일정 간격으로 반복 수집되는 특수한 구조를 가진다. CPU 사용률, 네트워크 트래픽, HTTP 요청 수는 초 단위로 수집되며, 서버 수천 대에서 발생하면 하루에 수십억 개의 데이터 포인트가 된다.

일반 RDBMS로 이 데이터를 저장하면 INSERT 성능 한계, 인덱스 폭발(Index Bloat), 오래된 데이터 삭제 복잡성이라는 세 가지 문제에 직면한다. TSDB는 이 문제를 처음부터 시계열 패턴에 맞게 설계된 스토리지 엔진으로 해결한다.

Prometheus TSDB는 로컬 블록 기반 스토리지로 15일 기본 보존을 제공하며, Thanos나 Cortex와 결합해 장기 보존과 글로벌 집계를 가능하게 한다. InfluxDB는 더 범용적인 TSDB로 SQL 유사 쿼리 언어(Flux), 연속 쿼리(Continuous Query), 보존 정책(Retention Policy)을 내장하여 IoT·금융·인프라 모니터링에 폭넓게 사용된다.

TSDB 선택은 단순한 데이터베이스 선택이 아니라 메트릭 생태계 전체(수집→압축→롤업→시각화)의 아키텍처 결정이다. 특히 카디널리티(Cardinality) 관리 실패는 TSDB 성능 붕괴의 가장 흔한 원인으로, 기술사 시험에서도 자주 다루어진다.

📢 **섹션 요약 비유**: TSDB는 마치 날씨 관측소의 전용 기록부 — 일반 일기장(RDBMS)이 아닌, 매 시간 온도만 빠르게 적고 오래된 기록은 월 평균으로 압축해서 보관하는 특화된 장부다.

---

## 2. 구성요소

### Prometheus TSDB 저장 구조

```
수집 (Scrape)
  15초 간격
      │
      ▼
┌────────────────────────────────┐
│     WAL (Write-Ahead Log)      │  ← 인메모리 Head Block 보호
│  (고장 시 데이터 복구용)        │
└──────────────┬─────────────────┘
               │ 2시간마다 블록 압축
               ▼
┌──────────────────────────────────────────────┐
│   로컬 블록 스토리지 (디스크)                  │
│                                              │
│  Block_0  Block_1  Block_2  ...  Block_N     │
│  (2h)     (2h)     (2h)          (2h)        │
│     └──────────────────────────┘            │
│            주기적 Compaction                  │
│            (겹치는 블록 병합 + 압축)           │
└──────────────────┬───────────────────────────┘
                   │ 15일 초과 또는 원격 전송
                   ▼
┌──────────────────────────────────────────────┐
│   장기 스토리지 (Thanos / Cortex)             │
│   S3 / GCS 오브젝트 스토리지                  │
│   다운샘플링: 5m, 1h 집계 블록 자동 생성       │
└──────────────────────────────────────────────┘
```

### TSDB 압축 기법

| 기법 | 원리 | 효과 |
|:---|:---|:---|
| 델타 인코딩 (Delta) | 타임스탬프 차이만 저장 | 타임스탬프 크기 80% 절감 |
| 이중 델타 (Delta-of-Delta) | 연속 타임스탬프 차이의 차이 | 일정 간격 수집 시 1~2비트 |
| 고릴라 압축 (Gorilla) | XOR + Huffman 부동소수점 | 값 공간 75% 절감 |
| 다운샘플링 (Downsampling) | 오래된 데이터 집계 (min/max/avg) | 1년치 데이터를 1/60로 축소 |

### Prometheus vs InfluxDB vs Thanos 비교

| 항목 | Prometheus TSDB | InfluxDB | Thanos |
|:---|:---|:---|:---|
| 아키텍처 | 로컬 단일 서버 | 단일/클러스터 | Prometheus 위 레이어 |
| 쿼리 언어 | PromQL | Flux / InfluxQL | PromQL (전역) |
| 보존 기간 | 기본 15일 | 정책 기반 무제한 | 오브젝트 스토리지 무제한 |
| 카디널리티 한계 | 수백만 시리즈 | 수천만 시리즈 | 분산 처리 |
| 사용 사례 | K8s 모니터링 | IoT, 금융, 범용 | 멀티 클러스터, 장기 보존 |

📢 **섹션 요약 비유**: TSDB 압축은 마치 건물 층간 소리 기록 — 매초 기록하지 않고 "이전보다 3dB 올랐다"만 기록하면 같은 정보를 10배 적은 공간에 담을 수 있다.

---

## 3. 구조 및 동작 원리

### 카디널리티(Cardinality) 문제

고카디널리티(High Cardinality)는 TSDB 성능 붕괴의 주된 원인이다. 예를 들어 HTTP 요청을 사용자 ID 레이블로 수집하면 사용자 수만큼 시리즈가 생성된다.

```
# 위험한 레이블 사용 (Cardinality 폭발)
http_requests_total{user_id="12345678", endpoint="/api/v1/..."}

# 올바른 레이블 사용 (낮은 카디널리티)
http_requests_total{endpoint="/api/v1/payment", status="200"}
```

| 레이블 값 종류 | 예시 | 카디널리티 수준 |
|:---|:---|:---|
| 안전 | status_code, method, region | 낮음 (<100) |
| 주의 | 서비스명, 버전 | 중간 (<10,000) |
| 위험 | user_id, 세션 ID, 요청 ID | 높음 (무제한) |

📢 **섹션 요약 비유**: TSDB 카디널리티는 마치 책 목차 — 카테고리(낮은 카디널리티)로 분류하면 목차가 간결하지만, 각 단어마다(높은 카디널리티) 목차를 만들면 목차가 본문보다 두꺼워진다.

---

## 4. 비교 및 트레이드오프

### 장기 보존 아키텍처 (Thanos)

```yaml
# thanos-store.yaml
type: S3
config:
  bucket: metrics-long-term
  endpoint: s3.amazonaws.com
  region: ap-northeast-2

# 다운샘플링 정책
downsampling:
  - resolution: 5m   # 원본 → 5분 집계: 40일 이후
  - resolution: 1h   # 5분 → 1시간 집계: 10개월 이후
```

### 기술사 판단 포인트

| 시나리오 | 권장 설계 | 근거 |
|:---|:---|:---|
| 단일 K8s 클러스터 모니터링 | Prometheus + Grafana | 단순, 충분한 15일 보존 |
| 멀티 클러스터 전역 조회 | Thanos / Cortex | 전역 PromQL, 단일 화면 |
| 규정 준수 1년 이상 보존 | InfluxDB + 장기 보존 정책 | 다운샘플링 내장 |
| 고카디널리티 요구 | InfluxDB / VictoriaMetrics | 높은 시리즈 처리 능력 |
| IoT 실시간 집계 | InfluxDB + Telegraf | 다양한 Input 플러그인 |

📢 **섹션 요약 비유**: TSDB 선택은 마치 냉장고 선택 — 한 집(단일 클러스터)엔 일반 냉장고(Prometheus), 대형 식당(멀티 클러스터)엔 산업용 냉동고(Thanos/Cortex)가 맞고, 오래 보관이 목적이면 냉동 창고(InfluxDB 장기 보존)를 선택한다.

---

## 5. 실무 적용 및 최적화 기법

TSDB 도입으로 인프라 메트릭 저장 비용을 일반 RDBMS 대비 10배 이상 절감하고, 수천 개 서버의 메트릭을 초 단위로 수집·쿼리하는 운영 관측성(Operational Observability)의 기반을 마련한다. 다운샘플링과 보존 정책을 통해 1년 치 이상의 트렌드 분석도 저렴하게 가능하다.

한계로는 TSDB가 시계열 데이터 외의 복잡한 관계형 쿼리에는 부적합하다는 점과, 카디널리티 관리에 실패하면 메모리 급증과 쿼리 성능 저하가 발생한다는 점이다. 따라서 TSDB 도입 시 레이블 설계 가이드라인과 카디널리티 모니터링이 반드시 병행되어야 한다.

향후에는 열 지향(Columnar) 스토리지와 TSDB의 융합(Apache Parquet + TSDB), 스트리밍 처리와의 통합, 그리고 ML 기반 이상 탐지와의 직접 연동이 TSDB 발전의 주요 방향이 될 것이다.

📢 **섹션 요약 비유**: TSDB는 마치 주식 차트 전용 장부 — 주가의 모든 순간을 다 기록하지 않고 최신 데이터는 세밀하게, 오래된 데이터는 일별 요약으로 관리하여 방대한 이력을 효율적으로 보존한다.

---

### 📌 관련 개념 맵
| 분류 | 관련 개념 |
|:---|:---|
| 상위 개념 | 옵저버빌리티 (Observability), 메트릭 (Metrics), 모니터링 (Monitoring) |
| 연관 기술 | Prometheus, InfluxDB, Thanos, Cortex, VictoriaMetrics, Grafana |
| 비교 대상 | RDBMS vs TSDB, Prometheus TSDB vs InfluxDB, Thanos vs Cortex |

### 👶 어린이를 위한 3줄 비유 설명
1. TSDB는 매일 체온을 재는 온도계 노트처럼, 같은 종류의 숫자가 시간 순서대로 가득한 특별한 데이터베이스야.
2. 고릴라 압축은 마치 "어제랑 똑같아"라고 쓰는 대신 체크 표시만 하는 것 — 저장 공간을 엄청나게 아낄 수 있어.
3. 오래된 데이터는 일별 평균으로 압축(다운샘플링)해서 1년치도 조그만 공간에 보관할 수 있어!
