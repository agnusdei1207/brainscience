+++
weight = 7
title = "07. 실시간 스트림 처리"
date = "2026-05-17"
[extra]
categories = "gisulsa-bigdata"
+++

# 실시간 스트림 처리 — Kafka & Flink

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

     높은 처리량, 낮은 지연, 내구성
Producer → Broker(Kafka 클러스터) → Consumer
Topic: 메시지 카테고리 (큐 개념)

### Ⅱ. 핵심 구성요소

```
정의: 분산 이벤트 스트리밍 플랫폼
     높은 처리량, 낮은 지연, 내구성

[Kafka 구성]
Producer → Broker(Kafka 클러스터) → Consumer

Topic: 메시지 카테고리 (큐 개념)
Partition: Topic을 나눈 병렬 단위
  - 파티션 수 = 병렬도
  - 파티션 내 순서 보장
Offset: 파티션 내 메시지 위치 (0부터 순차)
Consumer Group: 파티션을 병렬 소비하는 그룹

[Kafka 보장]
At-most-once: 중복 없음, 손실 가능
At-least-once: 손실 없음, 중복 가능
Exactly-once: 손실+중복 없음 (Kafka Streams 지원)

[용도]
이벤트 스트리밍: 실시간 데이터 파이프라인
MSA 이벤트 버스: 서비스 간 비동기 통신
로그 집계: 서버 로그 중앙화
CDC: 데이터베이스 변경 캡처
```
```
정의: 진정한 스트림 처리 엔진 (스트림 퍼스트)
vs Spark: 마이크로배치 vs 진정한 스트림

[Flink 핵심]


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
