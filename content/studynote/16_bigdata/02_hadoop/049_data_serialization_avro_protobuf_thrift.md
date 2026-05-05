+++
weight = 49
title = "27. 데이터 직렬화: Avro / Protobuf / Thrift"
date = "2026-04-29"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Avro, Protocol Buffers(Protobuf), Apache Thrift는 구조화된 데이터를 언어·플랫폼 독립적인 바이너리 형식으로 직렬화(Serialization)하는 프레임워크로, JSON/XML 대비 크기·속도에서 탁월한 효율을 제공한다.
> **비유**: 대형 물류창고에 재고를 나눠 보관하고 작업 지시서를 현장 직원에게 보내는 체계와 같다.

📝 모범 답안

## 1. 개요 및 필요성

```text
┌────────────────────────────────────────────────────────┐
│     JSON vs. Avro vs. Protobuf 비교                    │
├─────────────────┬──────────────────────────────────────┤
│ 형식            │ 특징                                  │
├─────────────────┼──────────────────────────────────────┤
│ JSON            │ 사람이 읽기 쉬움, 크기 큼, 파싱 느림 │
│ Avro            │ 바이너리, 스키마 분리, Hadoop 친화    │
│ Protobuf        │ 바이너리, 스키마 필드 번호 기반, gRPC │
│ Thrift          │ 바이너리, RPC 통합, Meta 오리지널     │
└─────────────────┴──────────────────────────────────────┘
```

---

## 2. 구성요소

### 각 형식의 직렬화 방식

```text
Avro:
  - 스키마를 .avsc 파일(JSON)로 별도 정의
  - 데이터에 스키마 없음 → Schema Registry에서 참조
  - 스키마 진화: 필드 추가/제거 + default값으로 backward/forward 호환

Protobuf:
  - .proto 파일에 스키마 정의
  - 각 필드에 고유 번호 (field=1, field=2...)
  - 번호 기반 인코딩 → 필드명 변경해도 호환 유지

Thrift:
  - .thrift 파일에 데이터 + 서비스(RPC) 정의
  - 직렬화 + RPC 프레임워크 통합
  - Meta(Facebook) 오리지널
```

### Avro 스키마 예시

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 배치 위치, 메타데이터 관리, 병렬 실행, 장애 복구가 함께 맞물려야 한다.

동작 순서:
| 비교 | Avro | Protobuf | Thrift |
|:---|:---|:---|:---|
| 스키마 언어 | JSON (.avsc) | IDL (.proto) | IDL (.thrift) |
| 스키마 진화 | Excellent | Good | Good |
| 바이트 효율 | Good | Better | Good |
| Kafka 통합 | Excellent | Good | Fair |
| gRPC 지원 | 없음 | Native | 없음 |
| 언어 지원 | 10+ | 13+ | 28+ |

---

## 4. 비교 및 연결

### Kafka + Confluent Schema Registry + Avro

```text
Producer → [Avro 직렬화] → Kafka 토픽
              ↑ 스키마 등록/조회
           Schema Registry
              ↓ 스키마 조회/역직렬화
Consumer ← [Avro 역직렬화] ← Kafka 토픽
```

### gRPC + Protobuf
- 마이크로서비스 간 고속 통신: HTTP/2 + Protobuf 바이너리.
- .proto → 각 언어 클라이언트 자동 생성.
- 스트리밍 지원: 단방향·양방향 스트리밍.

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:---|:---|
| **네트워크 효율** | JSON 대비 50~80% 데이터 크기 감소 |
| **처리 속도** | 바이너리 파싱으로 역직렬화 10배+ 향상 |
| **스키마 관리** | Schema Registry로 스키마 버전 중앙 관리 |

AI/ML 파이프라인에서 대규모 Feature Store와 모델 서빙에 Protobuf·Avro가 표준 직렬화로 자리잡고 있으며, Apache Arrow의 컬럼형 인메모리 포맷이 분석 워크로드에서 새로운 직렬화 표준으로 부상하고 있다.

---

## 6. 기대효과 및 결론

데이터 직렬화: Avro / Protobuf / Thrift은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 하둡 계열 기술의 가치는 개별 컴포넌트보다 저장·자원·처리 계층이 얼마나 안정적으로 결합되는가에 달려 있다.

---

## 7. 발전 흐름도

```text
[JSON/XML — 텍스트 직렬화, 사람 가독성, 크기 비효율]
    │
    ▼
[Avro/Protobuf/Thrift — 바이너리 직렬화, 효율성]
    │
    ▼
[Schema Registry — 스키마 버전 중앙 관리]
    │
    ▼
[gRPC + Protobuf — 마이크로서비스 표준 RPC]
    │
    ▼
[Apache Arrow — 컬럼형 인메모리 분석 직렬화]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Schema Registry** | Avro 스키마 중앙 저장·버전 관리 |
| **gRPC** | Protobuf 기반 고성능 RPC 프레임워크 |
| **Kafka** | Avro/Protobuf 직렬화의 주요 활용 시스템 |
| **Apache Arrow** | 컬럼형 인메모리 직렬화 차세대 표준 |
| **스키마 진화** | 데이터 구조 변경 시 하위 호환성 유지 |
