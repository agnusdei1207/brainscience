+++
weight = 131
title = "131. 관측 가능성 Three Pillars"
date = "2026-04-19"
[extra]
categories = "studynote-devops-sre"
+++

## 0. 핵심 인사이트

> **핵심**: Metrics(수치 시계열)·Logs(텍스트 이벤트)·Traces(분산 요청 추적)는 관측 가능성의 **3대 필러(Three Pillars)**이며, 세 가지를 **상관 분석(Correlation)**해야 장애 근본 원인을 파악할 수 있다.
> **비유**: Metrics는 체온계(숫자), Logs는 의사 진료 기록(텍스트), Traces는 혈류 추적(경로). 셋 다 봐야 정확한 진단.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
Metrics: "무엇이" — 에러율 5%↑
Logs:    "왜" — NullPointerException at OrderService
Traces:  "어디서" — Order→Payment→DB 3번째 구간에서 지연
  → TraceID로 3가지를 연결 → 완전한 진단
```

---

## 2. 구성요소

| Pillar | 형태 | 도구 |
|:---|:---|:---|
| **Metrics** | 수치 시계열 | Prometheus, Mimir |
| **Logs** | 텍스트 이벤트 | Loki, ELK |
| **Traces** | 분산 요청 추적 | Tempo, Jaeger |

---

## 3. 구조 및 원리

**핵심 조건**: 측정 가능한 SLI, 합의된 SLO, 실행 가능한 경보·복구 절차가 하나의 폐쇄 루프를 이뤄야 한다.

동작 순서:
1. 사용자 경험을 대표하는 지표를 선택해 서비스 상태를 수치화한다.
2. 허용 가능한 목표치와 에러 버짓을 정해 변화 속도와 안정성의 기준선을 만든다.
3. 메트릭·로그·트레이스로 이상 징후를 탐지하고 원인을 빠르게 국소화한다.
4. 장애 이후 포스트모템과 자동화를 통해 토일을 줄이고 재발 방지책을 시스템에 반영한다.

```text
서비스 요청
   ↓
측정(SLI)
   ↓
목표(SLO)·예산
   ↓
알림·복구
   ↓
학습·자동화
```

---

## 4. 비교 및 연결

관측 가능성 Three Pillars은(는) 유사한 도구나 방법론과 겹쳐 보일 수 있지만, 핵심 차이는 변경을 통제하는 방식과 피드백을 수집하는 위치에 있다. 따라서 비교 시에는 단순 기능 목록보다 적용 시점, 위험 통제 수준, 조직 변화 요구도를 함께 봐야 한다.

---

## 5. 실무 적용 및 판단

실무에서는 관측 가능성 Three Pillars을(를) 단독 도구로 취급하기보다 표준 운영 절차와 함께 도입해야 한다. 채택 전에는 현재 병목, 자동화 범위, 실패 시 롤백 경로, 필요한 관측 데이터가 준비되었는지 점검해야 하며, 특히 기존 프로세스와 충돌하는 승인 체계를 미리 조정해야 한다.

---

## 6. 기대효과 및 결론

Three Pillars의 **상관 분석(Correlation)**이 관측 가능성의 진정한 가치이며, OpenTelemetry+Grafana Stack이 이를 실현한다.

---

## 7. 발전 흐름도

```text
[메트릭만 (Nagios, 2000s)] → [로그 추가 (ELK, 2012~)]
    → [트레이스 추가 (Jaeger, 2016~)]
    → [3 Pillars 통합 (Grafana LGTM, 2020~)]
    → [현재: Profiles (4th Pillar) — 코드 수준 성능 분석]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Metrics** | 수치 지표 (Prometheus) |
| **Logs** | 텍스트 이벤트 (Loki) |
| **Traces** | 분산 추적 (Tempo) |
| **Correlation** | 3 Pillars 연결 (TraceID) |
| **LGTM Stack** | Grafana 관측 표준 |
