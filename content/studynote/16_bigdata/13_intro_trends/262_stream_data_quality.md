+++
title = "스트리밍 데이터 품질 관리 (Streaming Data Quality Management)"
date = 2025-01-01
description = "실시간 스트리밍 데이터의 품질 이슈, 스키마 레지스트리, Great Expectations 기반 인라인 검증, 이상 탐지를 다룬다."
categories = "studynote-bigdata"
tags = ["streaming data quality", "schema registry", "Great Expectations", "Kafka", "data validation", "anomaly detection", "data quality", "real-time"]
+++

## 0. 핵심 인사이트

> **핵심**: 스트리밍 데이터 품질 관리 (Streaming Data Quality Management)은(는) 빅데이터 전략과 거시적 변화 방향을 이해하기 위한 정책·시장·기술 트렌드 개념이다.
> **비유**: 멀리서 지형과 조류를 함께 보며 데이터 산업의 큰 흐름을 읽는 전망대와 같다.

📝 모범 답안

## 1. 개요 및 필요성

### 1.1 배치 vs 스트리밍 품질 관리 차이

| 항목          | 배치 품질 관리          | 스트리밍 품질 관리          |
|-------------|----------------------|--------------------------|
| 처리 시점     | 적재 후 일괄 검증       | 실시간 인라인 검증          |
| 오류 처리     | 재실행 가능             | 즉시 격리·알림 필요         |
| 지연 데이터   | 문제 없음               | 워터마크·윈도우 처리 필요   |
| 스키마 변화   | 배치 시 감지             | 실시간 스키마 호환성 검증   |

### 1.2 주요 품질 이슈

```
[데이터 소스] → Kafka → [소비자]
      ↓ 발생 가능한 품질 이슈:
  - 스키마 불일치: 필드 추가/제거/타입 변경
  - 누락값: 필수 필드 null
  - 범위 위반: 음수 금액, 미래 타임스탬프
  - 중복 이벤트: 네트워크 재전송으로 중복 메시지
  - 지연 도착: 이벤트 시간 vs 처리 시간 불일치
```

---

## 2. 구성요소

### 2.1 Confluent Schema Registry

```
생산자                    스키마 레지스트리        소비자
  │                            │                    │
  ├─[스키마 등록/확인]──────▶  │                    │
  │                            │                    │
  ├─[메시지 직렬화(Avro)]──▶ Kafka ──▶[스키마 확인]─▶│
                                                     │
                                               [역직렬화]
```

### 2.2 호환성 모드

| 모드                | 의미                                   |
|-------------------|----------------------------------------|
| BACKWARD (기본)    | 새 스키마로 이전 데이터 읽기 가능       |
| FORWARD           | 이전 스키마로 새 데이터 읽기 가능       |
| FULL              | 양방향 호환                            |
| NONE              | 호환성 검사 없음                       |

```json
{
  "type": "record", "name": "Order",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "ts", "type": "long"}
  ]
}
```

---

## 3. 구조 및 원리

**핵심 조건**: 정책, 거버넌스, 플랫폼 구조, 산업 활용 방향을 함께 읽어야 한다.

동작 순서:
### 3.1 Flink DataStream 내 검증

```python
def validate_event(event):
    errors = []
    if event['amount'] < 0:
        errors.append('negative_amount')
    if event['user_id'] is None:
        errors.append('null_user_id')
    if event['timestamp'] > time.time() + 60:
        errors.append('future_timestamp')
    return errors

stream.map(validate_event) \
      .filter(lambda e: len(e) > 0) \
      .sink_to(dead_letter_queue)
```

### 3.2 Great Expectations Streaming

```python
import great_expectations as gx

context = gx.get_context()
validator = context.get_validator(batch_request=streaming_batch)
validator.expect_column_values_to_not_be_null("user_id")
validator.expect_column_values_to_be_between("amount", 0, 1_000_000)
results = validator.validate()
```

---

## 4. 비교 및 연결

### 4.1 DLQ 아키텍처

```
메인 토픽 (orders)
      ↓
[소비자 + 검증]
      ├─ 유효 이벤트 → 처리 파이프라인 진행
      └─ 오류 이벤트 → DLQ (orders.dlq)
                            ↓
                     [알림/모니터링]
                            ↓
                     [수동 검토/재처리]
```

### 4.2 DLQ 메시지 구조

```json
{
  "original_topic": "orders",
  "original_partition": 3,
  "original_offset": 12345,
  "error_code": "SCHEMA_MISMATCH",
  "error_message": "Field 'amount' expected DOUBLE got STRING",
  "timestamp": "2024-01-15T10:30:00Z",
  "original_payload": "..."
}
```

---

## 5. 실무 적용 및 판단

### 5.1 통계 기반 이상 탐지

3σ 규칙: |값 - 평균| > 3 × 표준편차 → 이상값

```python
from collections import deque

window = deque(maxlen=100)

def detect_anomaly(value):
    if len(window) >= 30:
        mean = sum(window) / len(window)
        std = (sum((x-mean)**2 for x in window)/len(window))**0.5
        if abs(value - mean) > 3 * std:
            return True
    window.append(value)
    return False
```

### 5.2 ML 기반 이상 탐지

- **Isolation Forest**: 이상값은 적은 분기 수로 고립됨
- **LSTM Autoencoder**: 시계열 재구성 오류로 이상 탐지
- **Prophet + 신뢰구간**: 예측 범위 벗어나면 이상

---

## 6. 기대효과 및 결론

스트리밍 데이터 품질 관리 (Streaming Data Quality Management)은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 거시 트렌드는 개별 제품 비교보다 데이터 산업 구조가 어디로 이동하는지 판단하게 해 주는 기준점이다.

---

## 7. 발전 흐름도

```
배치 ETL 품질 관리 (SQL 검증, Great Expectations)
     │  스트리밍 데이터 증가
     ▼
Kafka + Schema Registry 도입 (2014~)
     │  실시간 검증 필요
     ▼
스트리밍 인라인 검증 (Flink/Spark + DLQ)
     │  ML 기반 이상 탐지
     ▼
지능형 스트리밍 DQ (Anomaly Detection + Auto-Remediation)
     │  DataOps + 스트리밍 통합
     ▼
실시간 데이터 옵저버빌리티 플랫폼 (현재~)
```

**핵심 키워드**: Schema Registry, Avro, DLQ, Great Expectations, 이상 탐지, 워터마크, 인라인 검증

## 👶 어린이를 위한 3줄 비유 설명

1. 스트리밍 데이터 품질 관리는 컨베이어 벨트 검사 — 물건이 흘러올 때마다 즉시 불량을 걸러내야 해.
2. 스키마 레지스트리는 계약서 확인 창구 — 보내는 사람과 받는 사람이 같은 양식을 쓰는지 중간에서 확인해줘.
3. DLQ는 불량품 보관함 — 이상한 데이터를 바로 버리지 않고 모아뒀다가 나중에 고쳐서 다시 쓸 수 있어.

---

## 8. 관련 개념 맵

```
스트리밍 데이터 품질
├── 1단: 스키마 검증
│   ├── Schema Registry (Avro/Protobuf)
│   └── 호환성 모드 (BACKWARD/FORWARD)
├── 2단: 인라인 검증
│   ├── Great Expectations Streaming
│   └── Flink/Spark 내 커스텀 검증
├── 3단: 이상 탐지
│   ├── 통계 기반 (3σ, Z-score)
│   └── ML 기반 (Isolation Forest, LSTM)
└── 오류 처리
    ├── 데드 레터 큐 (DLQ)
    └── 알림 + 재처리 흐름
```
