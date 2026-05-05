+++
weight = 44
title = "아파치 스톰 (Apache Storm) 및 실시간 분산 처리"
date = "2024-03-24"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 아파치 스톰 (Apache Storm) 및 실시간 분산 처리은(는) 분산 저장, 병렬 처리, 자원 관리를 결합해 대규모 데이터를 저비용으로 처리하게 하는 하둡 계열 핵심 기술이다.
> **비유**: 대형 물류창고에 재고를 나눠 보관하고 작업 지시서를 현장 직원에게 보내는 체계와 같다.

📝 모범 답안

## 1. 개요 및 필요성

빅데이터 초기, 하둡 맵리듀스는 디스크 기반 배치 처리에는 강력했으나 실시간 응답이 필요한 시스템에는 부적합했습니다. Apache Storm은 "실시간 하둡(Real-time Hadoop)"이라 불리며 등장하여, 데이터가 유입되는 즉시 수 밀리초(ms) 내에 연산을 수행할 수 있는 환경을 제공했습니다. 이는 금융 거래 사기 탐지, 실시간 대시보드 업데이트, IoT 센서 데이터 모니터링 분야의 혁신을 이끌었습니다.

---

## 2. 구성요소

Storm은 영구적으로 실행되는 토폴로지(Topology) 아키텍처를 기반으로 합니다.

```text
[ Apache Storm Topology: Spout & Bolt ]

   (Data Source)         (Processing Unit)        (Storage/Output)
   -------------        -------------------      ------------------
   [   Spout   ] ----   (Data Ingest)        (Filtering/Logic)        [ (Result Store) ]
       |                       |
       |                [     Bolt 2      ]
       +--------------> (Aggregation/Joins)

[ Core Components ]
1. Spout: 외부 소스(Kafka, Twitter 등)에서 데이터를 읽어 튜플 스트림 생성.
2. Bolt: 실제 비즈니스 로직(필터링, 조인, DB 저장 등)을 수행하는 연산 노드.
3. Tuple: 스톰에서 처리되는 데이터의 기본 단위 (List of Values).
4. Nimbus: 마스터 노드로 코드 배포 및 작업 할당 관리.
5. Supervisor: 실제 작업을 수행하는 워커 프로세스 관리 노드.
```

**핵심 원리:**
1. **스트림 그룹화(Stream Groupings):** 데이터(Tuple)를 어떤 Bolt로 보낼지 결정하는 전략(Shuffle, Fields, All grouping 등).
2. **신뢰성 전파(Ack/Fail):** 튜플 처리가 성공하면 Ack를 보내고, 실패 시 처음부터 재시도하여 최소 1회 처리(At-least-once) 보장.
3. **무한 루프 실행:** 배치와 달리 작업이 종료되지 않고 데이터가 들어올 때까지 대기하며 지속 실행.

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 배치 위치, 메타데이터 관리, 병렬 실행, 장애 복구가 함께 맞물려야 한다.

동작 순서:
| 비교 항목 | Hadoop MapReduce | Apache Storm | Apache Spark Streaming |
| :--- | :--- | :--- | :--- |
| **처리 모델** | 배치 (Batch) | 네이티브 스트림 (Stream) | 마이크로 배치 (Micro-batch) |
| **지연 시간 (Latency)** | 분~시간 (High) | 밀리초 (Very Low) | 초 단위 (Low) |
| **상태 관리** | 파일 기반 (HDFS) | 외부에 별도 관리 필요 | 인메모리 (Checkpointing) |
| **상태 보장** | Exactly-once | At-least-once (기본) | Exactly-once |
| **주요 용도** | 대규모 통계 분석 | 초저지연 알람, 실시간 처리 | 복잡한 분석 및 머신러닝 |

---

## 4. 비교 및 연결

- **실무 적용:** 웹 서비스의 실시간 로그 분석 시, Spout로 카프카 메시지를 읽고 Bolt에서 특정 에러 키워드를 필터링하여 이상 징후 발생 시 0.1초 내에 관리자에게 푸시 알림을 보내는 시스템에 적합합니다.
- **기술사적 판단:** Storm은 상태 관리(State Management) 기능이 약해 Flink나 Spark에 밀려나는 추세였으나, 단순하고 빠른 처리가 필요한 영역에서는 여전히 유효합니다. 기술사는 "복잡한 윈도우 연산이나 정확한 상태 유지가 필요하다면 Storm 보다는 Trident(Storm의 고차원 추상화)나 Flink를 선택해야 한다"는 설계 가이드라인을 제시해야 합니다.

---

## 5. 실무 적용 및 판단

Apache Storm은 실시간 분산 컴퓨팅의 원형을 정립한 도구입니다. 비록 최근에는 Apache Flink나 Spark Structured Streaming에 주류 자리를 넘겨주었지만, 데이터 흐름 지향(Dataflow) 프로그래밍 모델의 기초 지식으로서 가치가 높으며, 경량화된 실시간 파이프라인 구축 시 효율적인 대안으로 지속 활용될 것입니다.

---

## 6. 기대효과 및 결론

아파치 스톰 (Apache Storm) 및 실시간 분산 처리은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 하둡 계열 기술의 가치는 개별 컴포넌트보다 저장·자원·처리 계층이 얼마나 안정적으로 결합되는가에 달려 있다.

---

## 7. 발전 흐름도

```text
[Spout (데이터 소스 — Kafka · 파일 · API)]
    │
    ▼
[스트림 (Stream) — 무한 데이터 튜플 흐름]
    │
    ▼
[Bolt (처리·변환·집계 — 필터·조인·집계)]
    │
    ▼
[토폴로지 (Topology) — Spout + Bolt 유향 그래프]
    │
    ▼
[Apache Flink / Spark Structured Streaming — 후계 진화]
```
Spout가 수집한 스트림이 Bolt 체인을 거쳐 처리되는 토폴로지 모델로 실시간 분산 처리의 원형을 정립하고, Flink와 Spark Streaming으로 계승·발전된 흐름이다.

---

## 8. 관련 개념 맵

- **상위 개념:** Stream Processing, Distributed Computing
- **하위 개념:** Spout, Bolt, Topology, Stream Grouping
- **연관 기술:** Apache Kafka, Apache Flink, Spark Streaming, Apache Samza
