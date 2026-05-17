+++
weight = 6
title = "06. SW 아키텍처 패턴"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# SW 아키텍처 패턴 (Layered / MSA / EDA / Hexagonal)

> 별점: ★★★★★ | 매회 기본 | ★133·135회 MSA 기출

---

## 답안.

### Ⅰ. 개요

모놀리식 → MSA 전환 전략 (Strangler Fig Pattern):
2. 신규 기능을 마이크로서비스로 구현
3. 점진적 기존 기능 이전 (사가 패턴으로 트랜잭션 처리)

### Ⅱ. 핵심 구성요소

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


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
