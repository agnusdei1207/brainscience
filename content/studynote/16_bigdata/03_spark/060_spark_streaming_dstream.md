+++
weight = 60
title = "Spark Streaming (DStream) 아키텍처"
date = "2024-03-24"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Spark Streaming (DStream) 아키텍처은(는) 인메모리 분산 실행과 쿼리 최적화를 통해 대화형 분석·배치·스트리밍을 빠르게 연결하는 스파크 핵심 개념이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

아파치 스파크의 첫 번째 스트리밍 라이브러리인 Spark Streaming은 "모든 스트림 처리는 아주 작은 배치의 연속"이라는 철학에서 시작되었습니다. 이는 플링크(Flink) 같은 '이벤트 단위' 처리 모델과 대비되는 특징으로, 하둡 에코시스템과의 강력한 통합과 고도의 결함 허용(Fault Tolerance) 기능을 제공하며 실시간 분석 시장을 선도했습니다.

---

## 2. 구성요소

Spark Streaming은 입력을 짧은 주기의 RDD로 변환하여 스파크 코어 엔진으로 전달합니다.

```text
[ Spark Streaming Micro-batch Architecture ]

   (Input Stream)        (Spark Streaming)        (Spark Core)
   Kafka/Flume/S3           Receiver               Engine
   ~~~~~~~~~~~~~~       +---------------+       +-----------+
   Data Flow (t)  ---   ~~~~~~~~~~~~~~       | (1 second)    |       +-----------+
                        +---------------+       +-----------+
                        | Micro-batch 2 | ----> | RDD (t+1) |
                        | (1 second)    |       +-----------+
                        +---------------+

[ DStream Definition ]
DStream = Sequence of RDDs (t, t+1, t+2, ...)
* Operation: DStream.map() internally calls RDD.map() for each batch.
```

**핵심 원리:**
1. **Receiver:** 워커 노드에서 실행되며 외부 소스로부터 데이터를 수집해 메모리에 저장하고 복제하여 안정성 확보.
2. **배치 간격 (Batch Interval):** 스트림을 쪼개는 최소 시간 단위. 시스템의 지연 시간(Latency)을 결정함.
3. **윈도우 연산 (Window Operations):** 현재 배치뿐 아니라 과거 여러 배치를 묶어서 집계(예: 최근 10분간의 평균) 수행.
4. **체크포인팅 (Checkpointing):** 장애 시 상태 복구를 위해 메타데이터와 RDD 데이터를 안정적인 스토리지(HDFS)에 저장.

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:
| 비교 항목 | Spark Streaming (DStream) | Structured Streaming |
| :--- | :--- | :--- |
| **API 모델** | RDD 기반 (Low-level) | DataFrame/Dataset 기반 (High-level) |
| **처리 방식** | 시간 기반 마이크로 배치 | 무한히 성장하는 테이블 (Append-only) |
| **최적화** | 수동 RDD 튜닝 필요 | Catalyst/Tungsten 자동 최적화 |
| **이벤트 시간** | 처리 시간 기준 중심 (복잡) | 원어민 수준의 Event Time/Watermark 지원 |

---

## 4. 비교 및 연결

- **실무 적용:** 기존에 작성된 대규모 스파크 배치 코드를 실시간으로 전환해야 할 때, DStream 모델을 사용하면 비즈니스 로직 수정 없이 배포할 수 있어 마이그레이션 비용이 저렴합니다.
- **기술사적 판단:** DStream은 '초당 수십만 건'의 대량 처리에 유리하지만, '밀리초' 단위의 반응 속도가 중요한 증권 거래 등에는 부적합할 수 있습니다. 기술사는 비즈니스 요구사항(지연 시간 vs 처리량)을 분석하여 Spark Streaming과 Flink 중 적합한 엔진을 권고해야 합니다. 또한 최신 프로젝트라면 성능과 편의성이 개선된 'Structured Streaming'으로의 전환을 우선 고려해야 합니다.

---

## 5. 실무 적용 및 판단

Spark Streaming은 빅데이터 배치 처리와 실시간 처리를 단일 코드 베이스로 통합한 혁신적인 사례입니다. 비록 현재는 구조화된 스트리밍(Structured Streaming)에 주류 자리를 내주고 있으나, 마이크로 배치 사상은 클라우드 비용 최적화(서버리스 가동 시간 제어) 관점에서 여전히 유효한 아키텍처 표준입니다.

---

## 6. 기대효과 및 결론

Spark Streaming (DStream) 아키텍처은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[배치 처리(Spark Core)]
    │
    ▼
[마이크로 배치]
    │
    ▼
[Spark Streaming(DStream)]
    │
    ▼
[Structured Streaming]
    │
    ▼
[실시간 분석 파이프라인]
```

Spark Streaming은 배치 중심 Spark에서 마이크로 배치와 DStream, Structured Streaming으로 진화했다.

---

## 8. 관련 개념 맵

- **상위 개념:** Real-time Data Processing, Apache Spark
- **하위 개념:** Micro-batch, DStream, Receiver, Batch Interval
- **연관 기술:** Apache Flink (Native Stream), Kafka, Structured Streaming
