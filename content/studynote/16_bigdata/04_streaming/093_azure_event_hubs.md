+++
weight = 93
title = "18. Azure Event Hubs — Kafka 호환 이벤트 스트리밍"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Azure Event Hubs — Kafka 호환 이벤트 스트리밍은(는) 끊임없이 들어오는 이벤트를 낮은 지연으로 처리하면서 상태·시간·정확성을 제어하는 실시간 처리 핵심 기술이다.
> **비유**: 흐르는 고속도로의 차량을 멈추지 않고 실시간으로 분류하고 통제하는 관제센터와 같다.

📝 모범 답안

## 1. 개요 및 필요성

| 효과 | 설명 |
|:---|:---|
| Kafka 마이그레이션 용이 | 코드 변경 없이 Azure로 전환 |
| Azure 통합 | Databricks/Stream Analytics/Functions 네이티브 연동 |
| Geo-DR | 자동 지역 페일오버로 비즈니스 연속성 보장 |
| Capture | 원본 이벤트 자동 보관으로 감사 및 재처리 지원 |

---

## 2. 구성요소

Azure Event Hubs는 **Kafka 호환성을 통한 점진적 마이그레이션**과 Azure 생태계 최적화를 동시에 달성하는 엔터프라이즈 스트리밍 플랫폼이다. 기술사 답안에서는 Kafka 드롭인 교체의 의미, 티어별 특성, Capture를 통한 레이크하우스 연계, Geo-DR 구성을 중심으로 서술하면 된다.

> Event Hubs는 "Microsoft의 스트리밍 다리"다. Azure라는 섬으로 Kafka라는 대륙에서 건너올 수 있는 다리를 놓아서, 기존 Kafka 여행자들이 배(완전한 이식)가 아닌 차(Kafka 호환 API)로 바로 건너올 수 있게 했다.

---

## 3. 구조 및 원리

**핵심 조건**: 이벤트 시간, 상태 저장, 지연 허용, 전달 보장이 함께 통제되어야 한다.

동작 순서:
- [ ] 처리량 요구사항 기반 티어 선택 (Standard → Premium → Dedicated)
- [ ] Kafka 마이그레이션: 연결 문자열만 변경하여 테스트
- [ ] Capture 설정: 원본 이벤트 보존 정책 수립
- [ ] Geo-DR 설정: 페어링 네임스페이스로 DR 구성
- [ ] Consumer Group 격리: 서비스별 독립적 오프셋 관리

> Event Hubs Standard → Dedicated는 "공용 수영장 → 개인 수영장 임대"와 같다. 공용(Standard)은 저렴하지만 피크 시간에 혼잡하고, 개인(Dedicated)은 비싸지만 항상 전용 레인을 보장한다.

---

## 4. 비교 및 연결

---

## 5. 실무 적용 및 판단

---

## 6. 기대효과 및 결론

Azure Event Hubs — Kafka 호환 이벤트 스트리밍은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 실시간 처리의 경쟁력은 더 빨리 흘리는 것보다 시간 의미와 상태 일관성을 잃지 않는 데 있다.

---

## 7. 발전 흐름도

```text
[이벤트 소스 (Event Sources) — IoT·앱·클릭스트림, 초당 수백만 이벤트]
    │
    ▼
[아파치 카프카 (Apache Kafka) — 오픈소스 고처리량 메시지 스트리밍]
    │
    ▼
[Azure Event Hubs — Kafka 호환, 완전 관리형 이벤트 스트리밍 서비스]
    │
    ▼
[Azure Stream Analytics — 실시간 SQL 쿼리 처리, 창 집계(Window)]
    │
    ▼
[Azure Synapse Analytics / Power BI — 배치 분석 및 시각화 대시보드]
```
Azure Event Hubs는 Apache Kafka 호환 API를 제공하며, 완전 관리형 서비스로 대규모 이벤트를 수집하여 Azure 분석 파이프라인의 진입점 역할을 한다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Apache Kafka | 호환 대상 | Kafka 프로토콜 드롭인 교체 |
| Amazon Kinesis | 경쟁 서비스 | AWS 동등 포지션 |
| Azure Databricks | 통합 처리 | Spark Structured Streaming과 연동 |
| Azure Data Lake Gen2 | 저장 대상 | Capture 기능으로 자동 보관 |
| Kafka MirrorMaker 2 | 마이그레이션 도구 | 온프레미스 → Event Hubs 마이그레이션 |
