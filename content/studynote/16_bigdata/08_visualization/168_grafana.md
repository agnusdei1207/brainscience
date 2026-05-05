+++
weight = 168
title = "168. Grafana — 메트릭/로그/추적 통합 관측성 시각화"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Grafana — 메트릭/로그/추적 통합 관측성 시각화은(는) 복잡한 대규모 데이터를 사람이 빠르게 해석하고 행동으로 옮기게 만드는 시각화 핵심 원리 또는 도구다.
> **비유**: 복잡한 계기판 수치를 한눈에 읽히는 조종석 화면으로 바꾸는 일과 같다.

📝 모범 답안

## 1. 개요 및 필요성

### 관측성(Observability)의 3대 기둥

마이크로서비스, 쿠버네티스, 분산 시스템에서 "왜 서비스가 느린가?"를 파악하려면 3가지 신호가 필요하다:

```
관측성 3대 기둥:
┌──────────────────────────────────────────────────────┐
│  1. 메트릭 (Metrics)                                 │
│     - CPU, 메모리, 요청 수, 응답 시간, 오류율         │
│     - 시계열 데이터 (시간 + 숫자값)                   │
│     - "무슨 일이 일어나고 있나?" → 양적 측정           │
│                                                      │
│  2. 로그 (Logs)                                      │
│     - 애플리케이션 이벤트 기록 (ERROR, INFO, WARN)    │
│     - 비정형 텍스트 + 타임스탬프                      │
│     - "왜 이런 일이 일어났나?" → 상세 이유             │
│                                                      │
│  3. 추적 (Traces)                                    │
│     - 분산 서비스 간 요청 흐름 추적                   │
│     - Span 연결 (A서비스 → B서비스 → DB 순서)         │
│     - "어디서 느렸나?" → 병목 위치 식별               │
└──────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### LGTM 스택 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│                     LGTM 스택 구조                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  데이터 수집                                                 │
│  ┌────────────┬──────────────┬─────────────────────────────┐ │
│  │Prometheus  │ Promtail/    │ OpenTelemetry / Jaeger /    │ │
│  │(메트릭 수집)│ Fluentbit   │ Zipkin                      │ │
│  │Pull 기반   │ (로그 수집)  │ (추적 데이터 수집)           │ │
│  └─────┬──────┴──────┬───────┴──────────────┬──────────────┘ │
│        │             │                       │               │
│  저장  ▼             ▼                       ▼               │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────┐   │
│  │  Mimir   │  │  Loki    │  │         Tempo            │   │
│  │(메트릭   │  │(로그     │  │(추적 데이터 저장)          │   │
│  │ 장기저장)│  │ 집계·저장)│  │TraceQL 쿼리 지원          │   │
│  └──────────┘  └──────────┘  └──────────────────────────┘   │
│        │             │                       │               │
│  시각화 ▼             ▼                       ▼               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    Grafana UI                          │  │
│  │  PromQL / LogQL / TraceQL 통합 쿼리                    │  │
│  │  Explore, Dashboard, Alerting                         │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### 핵심 쿼리 언어 비교

| 언어 | 데이터 소스 | 주요 용도 |
|:---|:---|:---|
| **PromQL** | Prometheus, Mimir | 메트릭 쿼리·집계·알림 |
| **LogQL** | Loki | 로그 필터링·패턴 추출 |
| **TraceQL** | Tempo | 추적 검색·필터링 |

```
PromQL 예시:
  # 5분 평균 CPU 사용률 (전체 서비스)
  avg(rate(cpu_usage_seconds_total[5m])) by (service)

  # 오류율   sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m])) > 0.05

LogQL 예시:
  # 에러 로그만 필터
  {app="api-server"} |= "ERROR"
  
  # 분당 오류 발생 건수
  count_over_time({app="api-server"} |= "ERROR" [1m])
```

---

## 3. 구조 및 원리

**핵심 조건**: 표현 정확성, 인지 부하, 질의 성능, 상호작용성을 함께 균형시켜야 한다.

동작 순서:
### Grafana vs Kibana 비교

| 차원 | Grafana | Kibana |
|:---|:---|:---|
| **주 용도** | 다중 소스 메트릭·관측성 | Elasticsearch 로그 분석 |
| **데이터 소스** | 다수 (Prometheus, Loki, InfluxDB, 등) | Elasticsearch 전용 |
| **강점** | 멀티소스 통합, 메트릭 시각화 | 전문 로그 검색, SIEM |
| **ML 기능** | 기본 이상 감지 | Elastic ML (고급) |
| **무료 수준** | 오픈소스 전체 | 기본 기능 (고급은 유료) |

### Grafana k6: 부하 테스트 통합

Grafana k6는 JavaScript 기반 부하 테스트 도구로, 테스트 결과를 Grafana 대시보드로 실시간 시각화한다:

```javascript
// k6 테스트 스크립트
import http from 'k6/http';
export const options = { vus: 100, duration: '30s' };
export default function() {
  const res = http.get('https://api.example.com/products');
  check(res, { 'status was 200': (r) => r.status == 200 });
}
```

---

## 4. 비교 및 연결

### 쿠버네티스 모니터링 스택

```
쿠버네티스 표준 모니터링 스택:
  kube-state-metrics: K8s 오브젝트 상태 노출
  node-exporter: 노드 수준 메트릭 (CPU, 메모리, 디스크)
  Prometheus: 메트릭 수집 + 저장 (Pull 방식)
  Grafana: 시각화

  주요 대시보드:
  - Cluster Overview: 전체 클러스터 리소스 현황
  - Node Exporter Full: 노드별 상세 메트릭
  - Pod/Deployment: 워크로드별 CPU/메모리
  - Kubernetes Events: 이벤트 로그 연동
  
  커뮤니티 대시보드: grafana.com/grafana/dashboards/
  (ID 번호로 바로 가져오기 가능)
```

### Grafana Alerting

```yaml

- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    / sum(rate(http_requests_total[5m])) > 0.05
  for: 5m  # 5분 이상 지속 시 발화
  annotations:
    summary: "서비스 오류율 5% 초과"
    description: "{{ $labels.service }} 오류율: {{ $value | humanizePercentage }}"
  labels:
    severity: critical
```

알림 채널: Slack, PagerDuty, OpsGenie, 이메일, Webhook

---

## 5. 실무 적용 및 판단

### Grafana 도입 효과

| 영역 | 효과 |
|:---|:---|
| **MTTR 단축** | Mean Time To Recover — 장애 원인 파악 시간 대폭 단축 |
| **관측성** | 메트릭·로그·추적 통합으로 전체 시스템 상태 파악 |
| **비용** | 오픈소스 + 클라우드 관리형 Grafana Cloud 선택 가능 |
| **표준화** | 전사 모니터링 플랫폼 단일화 |

### 결론

Grafana는 **클라우드 네이티브 시대의 표준 관측성 플랫폼**이다. 마이크로서비스와 쿠버네티스 환경에서 시스템의 "건강 상태"를 지속적으로 모니터링하고, 이상 감지 시 즉각 대응할 수 있는 가시성을 제공한다. 정보통신기술사는 LGTM 스택의 각 컴포넌트 역할과 PromQL 기반 알림 설계를 이해하고 클라우드 인프라 모니터링 아키텍처 설계에 적용할 수 있어야 한다.

---

## 6. 기대효과 및 결론

Grafana — 메트릭/로그/추적 통합 관측성 시각화은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 시각화의 본질은 더 많은 그래프가 아니라 더 빠르고 정확한 판단을 가능하게 하는 정보 구조다.

---

## 7. 발전 흐름도

```text
[메트릭 수집 (Metrics) — Prometheus Pull 방식]
    │
    ▼
[로그 집계 (Log Aggregation) — Loki]
    │
    ▼
[분산 추적 (Distributed Tracing) — Tempo]
    │
    ▼
[Grafana 대시보드 — 통합 관측성 (Unified Observability)]
    │
    ▼
[LGTM 스택 (Loki + Grafana + Tempo + Mimir)]
```

관측성 기술이 개별 메트릭·로그·추적을 통합하여 Grafana 중심의 단일 가시성 플랫폼으로 수렴한 흐름이다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Prometheus | 메트릭 데이터 소스 | Pull 방식 시계열 메트릭 수집·저장 |
| Loki | 로그 데이터 소스 | 수평 확장 로그 집계, LogQL 쿼리 |
| Tempo | 추적 데이터 소스 | 분산 추적 백엔드, TraceQL |
| Mimir | Prometheus 확장 | 멀티테넌트 고가용성 Prometheus |
| LGTM 스택 | 통합 관측성 | Loki+Grafana+Tempo+Mimir |
| PromQL | 쿼리 언어 | Prometheus 메트릭 쿼리 언어 |
| Grafana k6 | 부하 테스트 | JavaScript 기반 부하 테스트 + Grafana 통합 |
| Kibana | 비교 도구 | Elasticsearch 특화 로그 분석 시각화 |
