+++
weight = 16
title = "16. 성능 테스트"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# 🎯 성능 테스트 (Performance Testing)

> **별점**: ★★★★☆ | 기본 필수

## 1. 성능 테스트 유형

| 유형 | 목적 | 특징 |
|------|------|------|
| **부하(Load)** | 예상 부하에서 성능 측정 | 정상 운영 조건 |
| **스트레스(Stress)** | 임계점 초과 시 동작 | 장애 상황 재현 |
| **스파이크(Spike)** | 갑작스러운 부하 급증 | 트래픽 폭증 대응 |
| **내구성(Soak/Endurance)** | 장기간 성능 유지 | 메모리 누수 탐지 |
| **용량(Volume)** | 대용량 데이터 처리 | 데이터 증가 대응 |

## 2. 핵심 성능 지표

```
[컴시응 핵심 메트릭]
응답 시간 (Response Time): 요청→응답 소요 시간
- 목표: P95 < 2초, P99 < 5초 (업종별 상이)

처리량 (Throughput): 단위시간당 처리 트랜잭션 수
- TPS (Transactions Per Second): 초당 트랜잭션
- RPS (Requests Per Second)

동시 사용자 (Concurrent Users): 동시 처리 사용자 수

오류율 (Error Rate): 전체 요청 중 오류 비율
- 목표: < 0.1%

가용성 (Availability): 99.9% (8.76시간/년 다운)
                      99.99% (52.6분/년)
                      99.999% (5.26분/년, 파이브나인)
```

## 3. 성능 테스트 도구

```
JMeter: 오픈소스, GUI+CLI, HTTP/DB/메시지
Gatling: 스칼라 기반, 코드형, 상세 리포트
k6: JavaScript, 클라우드 친화, CI/CD 통합
Locust: Python, 분산 테스트, 코드 가독성
```

## 4. 답안 포인트

**3단락**: ① 성능 테스트 유형 정의 → ② TPS/응답시간/동시접속자 지표 → ③ 성능 개선(캐싱/DB최적화/스케일) 전략

## 5. 관련 개념

`HW 사이징(★135회)` → tpmC 기반 성능 기준 | `SRE SLI/SLO` → 성능 목표 정의 | `K8s HPA` → 자동 스케일링 연계
