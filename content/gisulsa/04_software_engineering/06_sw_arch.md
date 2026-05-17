+++
weight = 6
title = "06. SW 아키텍처 패턴"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# 🎯 SW 아키텍처 패턴 (Layered / MSA / EDA / Hexagonal)

> **별점**: ★★★★★ | 매회 기본 | ★133·135회 MSA 기출

## 1. 핵심 정의

| 패턴 | 정의 | 특징 |
|------|------|------|
| **계층형** | Presentation→Business→Data 분리 | 단순, 모놀리식 |
| **MSA** | 독립 배포 가능 마이크로서비스 | 확장성, 복잡도↑ |
| **EDA** | 이벤트 기반 비동기 통신 | 느슨한 결합, Kafka |
| **헥사고날** | 포트&어댑터, 도메인 중심 | 테스트 용이 |
| **CQRS** | 읽기/쓰기 모델 분리 | 성능 최적화 |

## 2. MSA 전환 전략 (★★★)

```
모놀리식 → MSA 전환 전략 (Strangler Fig Pattern):
1. API 게이트웨이 앞단 배치
2. 신규 기능을 마이크로서비스로 구현
3. 점진적 기존 기능 이전 (사가 패턴으로 트랜잭션 처리)
4. 레거시 모놀리식 제거

MSA 주요 패턴:
- 사가(Saga): 분산 트랜잭션 (Choreography/Orchestration)
- API Gateway: 단일 진입점, 인증/라우팅
- Circuit Breaker: 장애 격리 (Hystrix, Resilience4j)
- Service Discovery: 동적 서비스 위치 탐색
```

## 3. 답안 포인트

**3단락 구조**: ① 모놀리식 한계 → ② MSA 아키텍처 & 패턴 → ③ 전환 전략 & 트레이드오프

**핵심 비교**: 모놀리식(단순/배포 느림) vs MSA(복잡/독립 배포) — 양쪽 장단점 모두 서술

**컴시응 포인트**: 서버 인프라 설계 관점 — 서비스별 독립 스케일링, 컨테이너 연계

## 4. 관련 개념

`K8s(★133회)` → MSA 오케스트레이션 | `EDA` → 이벤트 메시지 큐(Kafka) | `CQRS` → 읽기/쓰기 분리
