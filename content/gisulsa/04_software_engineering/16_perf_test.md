+++
weight = 16
title = "16. 성능 테스트"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# 성능 테스트 (Performance Testing)

> 별점: ★★★★☆ | 기본 필수

---

## 답안.

### Ⅰ. 개요

응답 시간 (Response Time): 요청→응답 소요 시간
- 목표: P95 < 2초, P99 < 5초 (업종별 상이)
처리량 (Throughput): 단위시간당 처리 트랜잭션 수

### Ⅱ. 핵심 구성요소

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
```
JMeter: 오픈소스, GUI+CLI, HTTP/DB/메시지
Gatling: 스칼라 기반, 코드형, 상세 리포트
k6: JavaScript, 클라우드 친화, CI/CD 통합
Locust: Python, 분산 테스트, 코드 가독성
```


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
