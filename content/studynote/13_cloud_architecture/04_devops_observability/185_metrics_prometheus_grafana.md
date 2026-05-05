+++
weight = 185
title = "185. 메트릭 (Metrics - Prometheus, Grafana)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: 메트릭(Metrics)은 시스템과 애플리케이션의 상태를 시간의 흐름에 따라 수집한 숫자 기반 시계열 데이터로, 가장 경량이며 집계·알람에 최적화된 옵저버빌리티의 첫 번째 기둥이다.
> **비유**: 메트릭은 자동차 계기판이다. 속도계, 연료계, 온도계처럼 중요한 수치를 실시간으로 보여주고, 위험 수준에 도달하면 경고등(알람)을 켠다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

메트릭은 "지금 CPU가 몇 %인가?", "지난 1분간 HTTP 요청이 몇 건인가?"처럼 숫자로 표현되는 측정값이다. 텍스트 로그와 달리 집계·시각화·알람이 용이하고 저장 공간이 효율적이어서 실시간 모니터링의 핵심 데이터다.

Prometheus(프로메테우스)는 2012년 SoundCloud에서 시작된 오픈소스 모니터링 시스템으로, 현재 CNCF(Cloud Native Computing Foundation, 클라우드 네이티브 컴퓨팅 재단) 졸업 프로젝트다. Pull 방식의 스크레이핑(Scraping), 강력한 레이블 기반 데이터 모델, PromQL(Prometheus Query Language) 쿼리 언어로 쿠버네티스 생태계의 표준 모니터링 도구가 되었다.

Grafana(그라파나)는 메트릭, 로그, 트레이스 등 다양한 데이터 소스를 하나의 대시보드로 시각화하는 오픈소스 도구다. Prometheus와의 조합("kube-prometheus-stack")은 쿠버네티스 모니터링의 디 팩토 스택이다.

---

## 2. 구성요소

### Prometheus Pull 방식 아키텍처

```
[Prometheus 스크레이핑 흐름]

애플리케이션           Prometheus 서버
(metrics 엔드포인트)       (수집·저장)
    │                         │
    ←─── HTTP GET /metrics ───┤  (15초마다 Pull)
    │                         │
    ─── 메트릭 데이터 반환 ───→  TSDB(시계열 DB)
                               │
                               ↓
                          PromQL 쿼리
                               │
                    ┌──────────┼──────────┐
                    ↓          ↓          ↓
                Grafana    AlertManager   API
              (시각화)      (알람 발송)
```

| 메트릭 유형 | 설명 | 예시 |
|:---|:---|:---|
| Counter | 단조 증가 값 | 전체 요청 수, 오류 수 |
| Gauge | 증감 가능 현재 값 | CPU 사용률, 메모리 |
| Histogram | 분포 측정, 백분위 계산 가능 | 응답 지연 시간 |
| Summary | 슬라이딩 윈도우 백분위 | 클라이언트 사이드 레이턴시 |

---

## 3. 구조 및 원리

**핵심 조건**: 변경 자동화와 운영 안정성은 별개가 아니라 하나의 루프이며, 빌드·검증·배포·관측·피드백이 끊기지 않아야 지속 개선이 가능하다.

동작 순서:
1. 변경 사항을 버전 관리 시스템에서 감지한다.
2. 빌드·테스트·보안 검증으로 변경의 품질을 빠르게 확인한다.
3. 승인된 산출물을 선언형 배포나 자동화 파이프라인으로 운영 환경에 반영한다.
4. 메트릭·로그·트레이스를 통해 실제 동작 결과를 관측한다.
5. 피드백을 다음 개선 주기에 연결해 반복적으로 신뢰성을 높인다.

### Prometheus vs 대안 도구

| 도구 | 특징 | 장점 | 단점 |
|:---|:---|:---|:---|
| Prometheus | Pull 방식, OSS | 쿠버네티스 네이티브 | 단일 노드, 장기 보존 어려움 |
| Thanos/Cortex | Prometheus 확장 | 멀티 클러스터, 장기 보존 | 운영 복잡도 증가 |
| Datadog | SaaS, 통합 | 로그·트레이스 통합 | 비용 높음 |
| New Relic | SaaS, APM 강점 | 애플리케이션 성능 분석 | 비용 높음 |
| VictoriaMetrics | 고성능 OSS TSDB | 메모리 효율, 빠름 | 생태계 작음 |

**PromQL 핵심 쿼리 예시:**
```promql
# 5분간 HTTP 요청 비율 (RPS)
rate(http_requests_total[5m])

# HTTP 오류율 (%)
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m])) * 100

# p99 응답 지연
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket[5m]))
```

---

## 4. 비교 및 연결

**Alertmanager 알람 설계 원칙:**
- **신호 기반 알람**: 증상(서비스 느림)에 알람, 원인(CPU 높음)이 아님
- **실행 가능 알람**: 알람 발생 시 즉각 대응 행동이 정의된 것만 알람
- **알람 그룹화**: 같은 원인의 알람을 그룹화하여 알람 폭풍(Alert Storm) 방지
- **페이지 임계값**: On-call을 깨울 알람과 단순 슬랙 알림을 구분

**카디널리티(Cardinality) 폭발 방지:**
```
# 나쁜 예 (높은 카디널리티 레이블)
http_requests_total{user_id="12345"} ← 사용자마다 다른 시계열 생성

# 좋은 예 (낮은 카디널리티 레이블)
http_requests_total{endpoint="/api/users", status="200"}
```

**실무 kube-prometheus-stack 구성:**
- Prometheus Operator + Prometheus + Grafana + Alertmanager
- ServiceMonitor CRD로 쿠버네티스 서비스 자동 스크레이핑
- Grafana 내장 쿠버네티스 대시보드

---

## 5. 실무 적용 및 판단

Prometheus + Grafana 스택 도입으로 쿠버네티스 클러스터와 애플리케이션의 실시간 상태가 대시보드 하나로 가시화된다. SLI/SLO 메트릭을 이 스택에서 수집·계산하여 Error Budget을 실시간으로 추적할 수 있다.

장기 메트릭 보존이 필요한 엔터프라이즈 환경에서는 Thanos 또는 VictoriaMetrics로 Prometheus를 확장하거나, Datadog 같은 SaaS를 선택하는 것을 검토한다. 핵심은 메트릭 데이터를 모으는 것이 목적이 아니라, 모은 데이터로 빠른 의사결정을 내릴 수 있는 대시보드와 알람 체계를 구축하는 것이다.

---

## 6. 기대효과 및 결론

메트릭 (Metrics - Prometheus, Grafana)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 메트릭 (Metrics - Prometheus, Grafana)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
메트릭 수집: Prometheus (Pull) · Datadog (Push)
    │
    ▼
저장: TSDB (시계열 DB) → PromQL 쿼리
    │
    ▼
시각화: Grafana 대시보드 · 알림: AlertManager
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 옵저버빌리티 | 메트릭은 3대 기둥 중 하나 |
| SLI / SLO | Prometheus 메트릭으로 SLI 계산 |
| PromQL | 메트릭 집계·SLI 계산 쿼리 언어 |
| AlertManager | 메트릭 임계값 기반 알람 발송 |
| Thanos / VictoriaMetrics | Prometheus 장기 보존 확장 |
| OpenTelemetry | 메트릭 수집 표준 SDK |

---
