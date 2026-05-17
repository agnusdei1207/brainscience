+++
weight = 6
title = "06. ITIL v4 상세"
date = "2026-05-17"
[extra]
categories = "gisulsa-it-mgmt"
+++

# 🎯 IT 서비스 관리 심화 (ITIL v4 & SRE)

> **별점**: ★★★★★ | 기본 필수

## 1. SRE (Site Reliability Engineering)

```
정의: 구글이 제안한 IT 운영 방법론.
     SW 엔지니어링 원칙으로 운영 문제를 해결.
     "시스템 신뢰성을 공학적으로 보장"

[SRE vs ITIL]
ITIL: 프로세스·절차 중심, 규정 준수
SRE:  코드·자동화·측정 중심, 에러 버짓

[SRE 핵심 개념]
SLI (Service Level Indicator): 실제 측정 지표
  예) 요청 성공률, p95 지연시간

SLA (Service Level Agreement): 외부 약정
  예) 99.9% 가용성 보장

SLO (Service Level Objective): 내부 목표
  예) SLI 99.95% 목표 (SLA보다 높게)

에러 버짓 (Error Budget):
  100% - SLO 목표 = 허용 가능한 장애 시간
  예) 99.9% SLO = 8.76시간/년 에러 버짓
  에러 버짓 소진 시: 기능 릴리즈 중단, 신뢰성 집중

토일 (Toil): 자동화 가능한 수동 반복 작업
  SRE 엔지니어: Toil < 50% 목표
```

## 2. 관찰 가능성 (Observability)

```
[세 가지 기둥]
메트릭 (Metrics): 숫자 기반 시계열 (CPU, 응답시간)
로그 (Logs): 이벤트 기록 (에러, 트랜잭션)
트레이스 (Traces): 요청의 분산 시스템 흐름 추적

도구:
Prometheus + Grafana: 메트릭 수집·시각화
ELK Stack: 로그 분석
Jaeger, Zipkin: 분산 추적
OpenTelemetry: 통합 계측 표준

[황금 신호 (4 Golden Signals, Google SRE)]
지연 (Latency): 응답시간
트래픽 (Traffic): 처리량
오류 (Errors): 오류율
포화 (Saturation): 리소스 사용률
```

## 3. 답안 포인트

**3단락**: ① SRE 정의 & SLI/SLO/SLA/에러버짓 개념 → ② 관찰가능성 3기둥 & 황금신호 → ③ ITIL vs SRE 비교 & 현대 조직 적용

## 4. 관련 개념

`ITIL v4(★★07 enterprise)` → SRE와 상호보완 | `K8s(★133회)` → SRE 운영 플랫폼 | `AIOps(☆예측)` → SRE 자동화 + AI
