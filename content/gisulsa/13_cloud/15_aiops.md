+++
weight = 15
title = "15. AIOps & 관찰 가능성"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 🎯 AIOps & 관찰 가능성 플랫폼

> **별점**: ★★★★★ | ☆ 2026 예측

## 1. AIOps (AI + IT Operations)

```
정의: AI/ML을 IT 운영(모니터링, 사고 대응, 자동화)에
     적용하여 운영 효율성을 높이는 기술

[AIOps 기능]
이상 탐지: ML로 정상 패턴 학습 → 이상 자동 감지
근본 원인 분석 (RCA): 여러 경보 중 실제 원인 추적
인시던트 예측: 장애 발생 전 예방적 조치
자동 치유 (Auto-remediation): 이상 탐지 → 자동 수정
용량 예측: 트래픽 예측 기반 미리 스케일

[AIOps 플랫폼]
Dynatrace: AI 기반 전체 스택 모니터링
Splunk ITSI: IT 서비스 인텔리전스
New Relic AI: 이상 탐지, 연관분석
Datadog: 클라우드 전 영역 관찰가능성
```

## 2. OpenTelemetry (OTel)

```
정의: 분산 시스템의 관찰 가능성 데이터(메트릭·로그·트레이스)를
     수집하기 위한 CNCF 오픈 표준

[OTel 구성]
API & SDK: 애플리케이션 계측 (코드 삽입)
Collector: 데이터 수집·처리·내보내기
Protocol: OTLP (OpenTelemetry Protocol)

[장점]
벤더 중립: Datadog, Jaeger, Prometheus 어디든 전송
표준화: 한 번 계측 → 여러 백엔드 지원
자동 계측: 코드 수정 없이 자동 계측 (Java Agent 등)

[현대 Observability 스택]
계측: OTel SDK
수집: OTel Collector
저장: Prometheus(메트릭), Loki(로그), Tempo(트레이스)
시각화: Grafana
```

## 3. 답안 포인트

**3단락**: ① AIOps 정의 & 이상탐지/RCA/자동치유 → ② OpenTelemetry 구조 & 벤더 중립성 → ③ 현대 관찰가능성 스택 (Prometheus/Loki/Grafana)

## 4. 관련 개념

`SRE(12_it 06번)` → SLI 측정에 OTel 활용 | `K8s(07번)` → K8s 클러스터 OTel 계측 | `MSA(★133회)` → 분산 추적 필수
