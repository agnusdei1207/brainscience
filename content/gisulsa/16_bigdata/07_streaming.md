+++
weight = 7
title = "07. 실시간 스트림 처리"
date = "2026-05-17"
[extra]
categories = "gisulsa-bigdata"
+++

# 🎯 실시간 스트림 처리 — Kafka & Flink

> **별점**: ★★★★★ | 기본 필수

## 1. Apache Kafka

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

## 2. Apache Flink

```
정의: 진정한 스트림 처리 엔진 (스트림 퍼스트)
vs Spark: 마이크로배치 vs 진정한 스트림

[Flink 핵심]
이벤트 시간 (Event Time): 이벤트 발생 시각 기준 처리
  → 네트워크 지연으로 늦게 도착한 데이터 처리
워터마크: 지연 데이터 허용 기준 (5초 허용)
상태 관리: 로컬 상태 + 체크포인트로 정확한 1회 처리

[Flink vs Spark Streaming]
항목        Flink           Spark Streaming
처리 방식   진정한 스트림   마이크로배치
지연        밀리초         1~2초
상태 관리   강력           기본적
정확성      Exactly-once   At-least-once
```

## 3. 데이터 파이프라인 아키텍처

```
[Lambda 아키텍처]
데이터 → 배치 레이어(Spark, HDFS) + 속도 레이어(Flink, Kafka)
         → 서빙 레이어(결합 조회)
단점: 이중 관리 복잡성

[Kappa 아키텍처]
데이터 → Kafka → Flink(스트림) → 서빙
단점 해소: 단일 코드베이스
장점: 단순, 재처리 쉬움
```

## 4. 답안 포인트

**3단락**: ① Kafka 아키텍처 & 파티션 병렬성 → ② Flink 스트림 처리 & 이벤트 시간 → ③ Lambda vs Kappa 아키텍처

## 5. 관련 개념

`MSA(★133회)` → Kafka 이벤트 버스로 서비스 연결 | `Spark(06번)` → 배치 처리 파트너 | `CDC` → Kafka Connect로 DB 변경 스트리밍
