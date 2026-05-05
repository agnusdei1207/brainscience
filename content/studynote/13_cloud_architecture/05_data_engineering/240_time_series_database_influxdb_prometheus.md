+++
weight = 240
title = "240. 시계열 데이터베이스 (TSDB) - InfluxDB / Prometheus"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++
## 0. 핵심 인사이트

> **핵심**: 시계열 데이터베이스(TSDB, Time Series Database)는 **타임스탬프가 기본 인덱스**인 데이터(IoT 센서·모니터링 메트릭·금융 호가)를 초당 수백만 건 쓰기와 **다운샘플링·보존 정책** 자동화에 특화된 저장소다.
> 2. **가치**: 시간 순서대로 압축·저장하고 범위 쿼리를 최적화하여, RDBMS 대비 **저장 공간 10배 절감**과 **10~100배 빠른 시계열 쿼리**를 제공하며 오래된 데이터 자동 압축·삭제로 운영을 단순화한다.
> 3. **판단 포인트**: InfluxDB는 독립형 시계열 저장·쿼리 완결 플랫폼, Prometheus는 쿠버네티스·MSA **메트릭 수집·알람**에 최적화된 Pull 방식 모니터링 시스템으로 역할이 다르다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

서버 모니터링 시스템이 1,000대 서버에서 CPU·메모리·네트워크 메트릭을 10초마다 수집한다면, 하루에 1,000×3×86,400/10 = **2,592만 건**의 데이터가 쌓인다. 이를 RDBMS로 저장하면:
- 1개월 = 7.8억 건 → 인덱스 유지 비용 폭발
- 범위 쿼리(`WHERE time > '어제' AND time < '오늘'`)가 느림
- 오래된 데이터 주기적 삭제 로직 직접 구현 필요

TSDB는 이 패턴을 위해 설계되었다.

```
[시계열 데이터 특성]
time                  server_id  cpu_pct  mem_pct
2024-01-15 09:00:00  server-01   23.5     60.2
2024-01-15 09:00:10  server-01   24.1     60.5
2024-01-15 09:00:20  server-01   22.8     60.1
...

특성:
- 시간 순서로 삽입 (append-only 패턴)
- 같은 시리즈(server-01)는 값이 비슷함 → 높은 압축률
- 최근 데이터 자주 쿼리, 오래된 데이터 다운샘플링
- 개별 행 UPDATE 거의 없음
```

📢 **섹션 요약 비유**: TSDB는 날씨 관측 일지다. 매 10분마다 온도·습도를 기록하고, 한 달이 지나면 일별 평균으로 요약(다운샘플링)하고, 5년이 지난 데이터는 자동 삭제(보존 정책)한다. 관측 일지를 위한 특화 시스템이다.

---

## 2. 구성요소

### InfluxDB 아키텍처

```
[InfluxDB 핵심 개념]
Measurement (테이블 유사): "cpu_usage"
  Tags (인덱스 메타데이터): host="server-01", region="us-east"
  Fields (실제 측정값): cpu=23.5, mem=60.2
  Timestamp: 2024-01-15T09:00:00Z

저장 구조:
  같은 태그 조합 = 하나의 시리즈(Series)
  시리즈 내 값을 시간 순서대로 압축 저장 (delta 인코딩)

[InfluxQL 쿼리]
SELECT mean("cpu")
FROM "cpu_usage"
WHERE time > now() - 1h
  AND host = 'server-01'
GROUP BY time(5m), host

[Flux 쿼리 (InfluxDB 2.0+)]
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu_usage")
  |> filter(fn: (r) => r.host == "server-01")
  |> aggregateWindow(every: 5m, fn: mean)
```

### Prometheus 아키텍처

```
┌────────────────────────────────────────────────────────────┐
│                   Prometheus 아키텍처                       │
│                                                            │
│  타겟 서버들                   Prometheus Server             │
│  ┌───────────┐    Pull        ┌──────────────────────┐    │
│  │ App:8080  │ ◀─────────── │  Scrape (15초마다)    │    │
│  │ /metrics  │               │  TSDB (로컬 저장)     │    │
│  └───────────┘               │  Rule Engine          │    │
│  ┌───────────┐               │  Alert Manager 연동   │    │
│  │ Node:9100 │ ◀─────────── └──────────┬───────────┘    │
│  │ /metrics  │                         │                  │
│  └───────────┘                         ▼                  │
│  ┌───────────┐               ┌──────────────────────┐    │
│  │ K8s:443   │ ◀─────────── │   Grafana             │    │
│  │ /metrics  │               │   (대시보드 시각화)    │    │
│  └───────────┘               └──────────────────────┘    │
└────────────────────────────────────────────────────────────┘
```

### PromQL 쿼리 예시

```promql
# CPU 사용률 1분 평균
rate(cpu_usage_total[1m])

# 메모리 사용률 80% 초과 알람 조건
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 20

# HTTP 요청 에러율 (5xx / 전체)
sum(rate(http_requests_total{status=~"5.."}[5m])) /
sum(rate(http_requests_total[5m]))

# p99 레이턴시
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

### 보존 정책 (Retention Policy) 및 다운샘플링

```
[데이터 수명 주기 관리]
원시 데이터 (10초 간격) → 7일 보관
1분 집계 (mean, max, min) → 30일 보관
1시간 집계              → 1년 보관
1일 집계               → 무기한 보관

InfluxDB Continuous Query 예시:
CREATE CONTINUOUS QUERY cq_hourly ON metrics
BEGIN
  SELECT mean(cpu) AS mean_cpu, max(cpu) AS max_cpu
  INTO metrics.one_hour.cpu_usage
  FROM metrics.raw.cpu_usage
  GROUP BY time(1h), host
END
```

📢 **섹션 요약 비유**: 보존 정책과 다운샘플링은 사진 보관 방식과 같다. 최근 1주일 사진은 원본(고화질, 많은 용량), 1달 지난 사진은 중간 해상도 압축, 1년 지난 사진은 썸네일만 보관. 디스크 공간을 관리하면서 역사적 추이는 유지한다.

---

## 3. 구조 및 동작 원리

### InfluxDB vs Prometheus 비교

| 비교 항목 | InfluxDB | Prometheus |
|:---|:---|:---|
| **수집 방식** | Push + Pull | Pull (스크레이핑) |
| **저장 범위** | 대용량 장기 저장 | 기본 15일 (짧은 로컬 저장) |
| **쿼리 언어** | InfluxQL / Flux | PromQL |
| **클러스터링** | 엔터프라이즈 기능 | 외부 솔루션 필요 (Thanos/Cortex) |
| **알람** | Tasks / Checks | Alert Manager |
| **K8s 통합** | 보통 | 탁월 (쿠버네티스 사실상 표준) |
| **장기 보관** | 직접 지원 | Thanos/Cortex 연동 필요 |
| **적합 사례** | IoT, 산업 모니터링 | MSA/K8s 모니터링 |

### TSDB 생태계 비교

| DB | 특징 | 적합 사례 |
|:---|:---|:---|
| **InfluxDB** | 범용 TSDB, 자체 완결 | IoT, 산업 센서 |
| **Prometheus** | K8s 메트릭 표준 | MSA, DevOps |
| **TimescaleDB** | PostgreSQL 확장 TSDB | SQL 친숙팀, 복잡 쿼리 |
| **QuestDB** | 초고속 쿼리 | 금융 호가, 고빈도 거래 |
| **AWS Timestream** | 완전 관리형 | AWS 에코시스템 |

📢 **섹션 요약 비유**: Prometheus Pull 방식은 교사가 학생을 호명해서 점수를 수집하는 방식이다(학생이 자발적으로 내지 않음). InfluxDB Push 방식은 학생이 자발적으로 점수를 제출하는 방식이다. K8s 환경에서는 Prometheus Pull이 더 안정적이다.

---

## 4. 비교 및 트레이드오프

### Prometheus 알람 규칙 설계

```yaml
# alerting_rules.yml
groups:
  - name: infrastructure
    rules:
      # CPU 85% 초과 5분 지속
      - alert: HighCPUUsage
        expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU on {{ $labels.instance }}"
          description: "CPU usage is {{ $value }}%"

      # 파드 재시작 횟수 급증
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: critical
```

### 실무 모니터링 스택 (K8s)

```
[표준 K8s 모니터링 스택]
Prometheus Operator (메트릭 수집)
  + Grafana (대시보드 - 골든 시그널: 레이턴시, 트래픽, 에러, 포화도)
  + Alert Manager (알람 → Slack/PagerDuty)
  + Thanos (장기 저장, 글로벌 쿼리)

골든 시그널 (SRE 4가지 핵심 메트릭):
  1. 레이턴시 (Latency): p50/p99 응답 시간
  2. 트래픽 (Traffic): 초당 요청 수 (RPS)
  3. 에러 (Errors): HTTP 5xx 비율
  4. 포화도 (Saturation): CPU/Memory/Disk 사용률
```

📢 **섹션 요약 비유**: SRE 골든 시그널은 자동차 계기판이다. 속도계(트래픽), 연료게이지(포화도), 온도계(에러율), 반응 속도(레이턴시) 4가지만 잘 보면 차(시스템) 상태를 실시간 파악할 수 있다.

---

## 5. 실무 적용 및 최적화 기법

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **저장 효율** | 시계열 압축으로 RDBMS 대비 10배 이상 공간 절감 |
| **쿼리 속도** | 시간 범위 쿼리 RDBMS 대비 10~100배 빠름 |
| **운영 자동화** | 보존 정책·다운샘플링 자동 처리 |
| **실시간 알람** | 임계값 기반 자동 알람으로 장애 선제 대응 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **단순 액세스 패턴** | 시간 범위 + 시리즈 기반 외 복잡한 쿼리 약함 |
| **카디널리티 폭발** | 고카디널리티 태그(요청 ID 등) 사용 시 성능 급락 |
| **JOIN 불가** | 여러 메트릭 조인은 외부 쿼리 레이어 필요 |
| **Prometheus 단기 저장** | 기본 15일, 장기 저장은 Thanos/Cortex 필요 |

📢 **섹션 요약 비유**: TSDB의 카디널리티 폭발은 날씨 일지에 매 관측마다 날씨 측정 도구 일련번호를 태그로 붙이는 것과 같다. 도구 수만큼 인덱스가 생겨 관리 비용이 폭발한다. 태그는 LOW 카디널리티(지역, 서버 타입 등)만 사용해야 한다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| Prometheus + Grafana | TSDB 기반 표준 모니터링·대시보드 스택 |
| SRE 골든 시그널 | TSDB 메트릭 수집의 핵심 관찰 지표 |
| Thanos / Cortex | Prometheus 장기 저장 및 고가용성 확장 |
| IoT 스트리밍 | TSDB에 초고속 시계열 데이터 적재 패턴 |
| InfluxDB | 범용 Push/Pull TSDB, IoT 특화 |
| TimescaleDB | PostgreSQL TSDB 확장, SQL 호환 |
| Apache Kafka | 대규모 메트릭/이벤트 → TSDB로 전달하는 버퍼 |

### 👶 어린이를 위한 3줄 비유 설명
1. TSDB는 체온계 기록지다. 환자 이름(시리즈)과 시간마다 체온(값)을 기록하고, 지난 달 기록은 일별 평균(다운샘플링)으로 요약해서 보관한다.
2. Prometheus는 학교 선생님이 매 시간 학생들 출석을 확인하는 것처럼(Pull), 정기적으로 서버에 접속해서 상태를 수집한다.
3. InfluxDB 다운샘플링은 동영상 해상도를 낮추는 것과 같다. 최근 영상은 HD로, 오래된 영상은 SD로 압축해서 저장하면 용량을 아끼면서도 과거 추이를 볼 수 있다.
