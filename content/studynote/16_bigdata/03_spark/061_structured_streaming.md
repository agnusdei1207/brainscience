+++
weight = 61
title = "스파크 구조적 스트리밍 (Spark Structured Streaming)"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 스파크 구조적 스트리밍 (Spark Structured Streaming)은(는) 인메모리 분산 실행과 쿼리 최적화를 통해 대화형 분석·배치·스트리밍을 빠르게 연결하는 스파크 핵심 개념이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

- **정의**: 정적 데이터에 대한 배치 쿼리를 실행하듯이 스트리밍 데이터를 처리할 수 있게 해주는 고수준 API 기반의 실시간 처리 프레임워크이다.
- **배경**: 기존 DStream(마이크로 배치)의 복잡한 RDD 조작과 이벤트 시간 처리의 한계를 극복하고, 배치와 스트리밍 코드의 통합(Unified)을 실현하기 위해 등장했다.
- **주요 활용**: 실시간 ETL 파이프라인, 실시간 대시보드 업데이트, IoT 센서 데이터의 이상 탐지, 실시간 개인화 추천 시스템 등에서 표준으로 사용된다.

---

## 2. 구성요소

#### 1. 무한 테이블 (Unbounded Table) 모델
```text
[ Data Stream ] (Incoming events)
      |
      V
[ Input Table ] (Unbounded / Append-only)
+-------+-------+-------+
| Col 1 | Col 2 | Col 3 |  <-- New data appended every trigger
+-------+-------+-------+
      |
      V [ Incremental Query ] (Spark SQL Engine)
      |
[ Result Table ] (Updated state)
      |
      V [ Output Sink ] (External Storage)
```

#### 2. 핵심 처리 메커니즘
- **Trigger**: 데이터를 처리할 주기를 결정한다 (예: 1초마다, 혹은 데이터가 들어오는 즉시 처리하는 연속 모드).
- **Watermarking**: 늦게 도착한 데이터(Late Data)를 얼마나 기다릴지 정의하여 상태 정보의 메모리 무한 증식을 방지한다.
- **State Store**: 윈도우 합계나 조인 처리를 위해 필요한 중간 상태값을 인메모리 혹은 HDFS/S3에 안전하게 보관한다.
- **Fault Tolerance**: Checkpointing을 통해 장애 발생 시 마지막 처리 지점부터 중단 없이 재시작할 수 있다.

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:
| 비교 항목 | Spark Streaming (DStream) | Structured Streaming |
| :--- | :--- | :--- |
| **기반 추상화** | RDD (Low-level) | DataFrame / Dataset (High-level) |
| **처리 모델** | 마이크로 배치 전용 | 마이크로 배치 + 연속 처리(Continuous) |
| **이벤트 시간 처리** | 지원 미흡 (Processing Time 위주) | 워터마크 기반 완벽 지원 |
| **코드 통합** | 배치 코드와 별도 작성 필요 | 배치 쿼리와 90% 이상 동일 코드 사용 |
| **보증 수준** | At-least-once (일부 상황) | Exactly-once (엔드 투 엔드 보장) |

---

## 4. 비교 및 연결

- **배치-스트림 통합 아키텍처**: 동일한 로직을 배치 데이터와 실시간 데이터에 모두 적용할 수 있어 유지보수 비용을 획기적으로 낮춘다 (Lambda/Kappa 아키텍처 구현 용이).
- **Sink 선택 전략**: Kafka, HDFS, Console 외에도 Delta Lake와 결합하여 실시간 데이터 레이크하우스를 구축하는 것이 최신 기술 트렌드이다.
- **성능 최적화**: 셔플링을 유도하는 윈도우 연산 시 파티션 개수(`spark.sql.shuffle.partitions`)를 데이터 규모에 맞게 조정하고, 로컬 상태 저장소의 성능(RocksDB 등)을 튜닝해야 한다.

---

## 5. 실무 적용 및 판단

- **기대효과**: 데이터 엔지니어가 실시간 처리를 위해 특별한 기술을 새로 배울 필요 없이 기존 SQL/DataFrame 지식만으로 고성능 실시간 시스템을 구축할 수 있게 한다.
- **결론**: 구조적 스트리밍은 '배치와 스트리밍의 경계'를 허문 혁신적인 도구이다. 향후 Apache Flink와의 경쟁 속에서도 Spark 생태계의 강력한 통합 이점을 바탕으로 실시간 데이터 처리의 중추 역할을 지속할 것으로 전망된다.

---

## 6. 기대효과 및 결론

스파크 구조적 스트리밍 (Spark Structured Streaming)은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[배치 처리 (Batch Processing) — 정해진 주기 대규모 데이터 처리]
    │
    ▼
[스트리밍 처리 (Streaming) — 실시간 연속 데이터 처리]
    │
    ▼
[Spark Streaming (DStream) — RDD 기반 마이크로 배치]
    │
    ▼
[Structured Streaming — DataFrame API 기반 연속 처리]
    │
    ▼
[워터마크 (Watermark) — 지연 데이터 처리 기준 시간 설정]
    │
    ▼
[Delta Live Tables — 선언형 스트리밍 파이프라인 자동화]
```
Structured Streaming은 DStream의 복잡성을 DataFrame API로 추상화하여, 배치와 스트리밍을 통합하는 현대 실시간 파이프라인의 표준이 되었다.

---

## 8. 관련 개념 맵

1. **Micro-batching**: 데이터를 아주 작은 단위로 묶어 처리하는 방식
2. **Exactly-once Semantics**: 데이터 손실이나 중복 없이 정확히 한 번 처리됨을 보장
3. **Event Time**: 데이터가 시스템에 입력된 시간이 아닌, 실제 발생한 시간
