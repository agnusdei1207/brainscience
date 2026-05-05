+++
weight = 91
title = "16. Amazon Kinesis Data Streams — AWS 관리형 스트리밍"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Amazon Kinesis Data Streams — AWS 관리형 스트리밍은(는) 끊임없이 들어오는 이벤트를 낮은 지연으로 처리하면서 상태·시간·정확성을 제어하는 실시간 처리 핵심 기술이다.
> **비유**: 흐르는 고속도로의 차량을 멈추지 않고 실시간으로 분류하고 통제하는 관제센터와 같다.

📝 모범 답안

## 1. 개요 및 필요성

| 효과 | 설명 |
|:---|:---|
| 빠른 시작 | 클러스터 구축 없이 수 분 내 스트리밍 파이프라인 구동 |
| AWS 통합 | Lambda/S3/Flink와 네이티브 연동으로 개발 생산성 향상 |
| 운영 부담 감소 | 브로커 패치, 복제, 모니터링을 AWS가 담당 |

---

## 2. 구성요소

Amazon Kinesis Data Streams는 **AWS 생태계 내 스트리밍의 표준 솔루션**이다. 기술사 답안에서는 샤드 기반 처리량 구조, Kafka와의 벤더 종속 vs 유연성 트레이드오프, Enhanced Fan-Out의 필요성, 그리고 AWS 서비스 통합 관계를 체계적으로 서술해야 한다.

> Kinesis는 "AWS라는 도시의 지하철 시스템"이다. 도시 안(AWS)에서는 최적화되어 있고 편리하지만, 다른 도시(다른 클라우드)로 이사하면 지하철이 없어 처음부터 다시 만들어야 한다.

---

## 3. 구조 및 원리

**핵심 조건**: 이벤트 시간, 상태 저장, 지연 허용, 전달 보장이 함께 통제되어야 한다.

동작 순서:

---

## 4. 비교 및 연결

---

## 5. 실무 적용 및 판단

---

## 6. 기대효과 및 결론

Amazon Kinesis Data Streams — AWS 관리형 스트리밍은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 실시간 처리의 경쟁력은 더 빨리 흘리는 것보다 시간 의미와 상태 일관성을 잃지 않는 데 있다.

---

## 7. 발전 흐름도

```text
[배치 수집 (Batch Ingestion) — 주기적 ETL 파이프라인, 높은 지연]
    │
    ▼
[Amazon Kinesis Data Streams — 실시간 스트림 수집, 샤드 기반 병렬 처리]
    │
    ▼
[Kinesis Data Firehose — 무서버 스트림→S3/Redshift 자동 전달, 변환 내장]
    │
    ▼
[Kinesis Data Analytics (Apache Flink) — SQL·Flink로 스트림 실시간 분석]
    │
    ▼
[Lambda Architecture / Kappa Architecture — 배치+스트림 통합 또는 스트림 단일화 아키텍처]
```
이 흐름은 배치 처리의 높은 지연 한계를 극복하기 위해 Amazon Kinesis가 실시간 스트림 수집의 관리형 표준으로 자리잡고, 저장·분석 레이어와 결합하여 엔드투엔드 실시간 파이프라인 아키텍처로 진화하는 스트리밍 데이터 처리의 계보를 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Apache Kafka | 비교 대상 | 오픈소스 스트리밍의 대안 |
| Amazon MSK | 연관 서비스 | Kafka 완전 관리형(MSK)은 Kinesis의 대안 |
| Kinesis Firehose | 연동 서비스 | Kinesis 데이터를 S3/Redshift로 자동 전달 |
| AWS Lambda | 소비자 통합 | Kinesis 트리거로 서버리스 처리 |
| Consumer Lag | 모니터링 개념 | Kinesis에서는 GetRecords.MillisBehindLatest |
