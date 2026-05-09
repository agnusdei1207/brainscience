+++
weight = 395
title = "395. 하둡 맵리듀스 디스크 병목 분산 처리 (Hadoop MapReduce)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Hadoop MapReduce는 대용량 데이터를 Map(분할·처리)→Shuffle(정렬·그룹화)→Reduce(집계) 단계로 분산 처리하며, 각 단계 사이에 HDFS(Hadoop Distributed File System) 디스크 I/O가 발생하는 구조다.
> 2. **가치**: 수천 노드의 범용 서버로 페타바이트 데이터를 처리하는 수평 확장성을 제공하지만, 디스크 I/O 병목으로 반복적 ML 워크로드에는 부적합하다.
> 3. **판단 포인트**: 디스크 병목을 해소하기 위해 인메모리 처리(Apache Spark)가 등장했으며, MapReduce는 일회성 대용량 배치에만 적합하다.

## Ⅰ. 개요 및 필요성

Google의 MapReduce 논문(2004)과 GFS(Google File System) 논문에서 영감을 받아 Doug Cutting이 개발한 Hadoop은 빅데이터 처리의 표준이 됐다. MapReduce는 데이터를 여러 노드에 분산 저장(HDFS)하고, 연산을 데이터가 있는 노드에서 수행(Data Locality)하여 네트워크 전송 비용을 최소화하는 원리다.

**디스크 병목**: Map→Shuffle→Reduce 단계 사이마다 중간 결과를 디스크에 기록하여, 반복 처리(ML 학습의 Epoch)마다 디스크 읽기·쓰기가 발생한다. 이것이 Spark 대비 10~100배 느린 주된 원인이다.

📢 **섹션 요약 비유**: MapReduce는 팩스 기계 — 한 장씩(배치) 처리는 잘 하지만, 실시간 화상통화(반복 처리)는 못 한다.

## Ⅱ. 아키텍처 및 핵심 원리

```
Input Data (HDFS)
       │
       ▼
┌─────────────┐   Map 단계: 각 노드에서 로컬 처리
│  Map Task 1  │──> (key, value) pairs
│  Map Task 2  │──> (key, value) pairs    → 디스크 기록
│  Map Task N  │──> (key, value) pairs
└──────┬──────┘
       │ Shuffle & Sort (네트워크 전송 + 정렬)
       ▼
┌─────────────┐   Reduce 단계: 집계 처리
│ Reduce Task 1│──> 최종 결과 → HDFS 기록
│ Reduce Task 2│──> 최종 결과 → HDFS 기록
└─────────────┘
```

| 단계 | 동작 | I/O 유형 |
|:---|:---|:---|
| Map | 입력 분할·변환 | HDFS 읽기 |
| Shuffle | 키별 그룹화·정렬 | 디스크+네트워크 |
| Reduce | 집계·출력 | HDFS 쓰기 |

📢 **섹션 요약 비유**: Shuffle은 카드 섞기 — 전국의 카드(중간 결과)를 모아서 숫자별로 정렬하는 것이 가장 비싼 단계다.

## Ⅲ. 비교 및 연결

| 항목 | Hadoop MapReduce | Apache Spark |
|:---|:---|:---|
| 중간 결과 저장 | HDFS(디스크) | 메모리(RDD) |
| 반복 처리 성능 | 매우 낮음 | 높음(10~100x) |
| 실시간 처리 | 불가 | 가능(Structured Streaming) |
| 생태계 | HDFS, YARN, Hive | Spark SQL, MLlib, GraphX |

📢 **섹션 요약 비유**: MapReduce와 Spark의 차이는 USB 저장 vs RAM — USB(디스크)는 느리고, RAM(메모리)은 빠르다.

## Ⅳ. 실무 적용 및 기술사 판단

**의사결정 포인트**:
- 일회성 대용량 텍스트 처리(로그 집계): MapReduce 여전히 유효
- ML 반복 학습, 실시간 스트리밍: Spark 필수
- 클라우드 환경: EMR(AWS), Dataproc(GCP)로 관리형 하둡 활용
- HDFS 대체: S3/ADLS 기반 오브젝트 스토리지로 마이그레이션 권장

📢 **섹션 요약 비유**: Hadoop은 노련한 배달 트럭 — 무거운 짐(배치)엔 최고지만, 빠른 배달(실시간)엔 오토바이(Spark)가 낫다.

## Ⅴ. 기대효과 및 결론

Hadoop MapReduce는 빅데이터 분산 처리의 토대를 만들었으나, 디스크 I/O 병목으로 실시간·반복 처리 영역에서는 Spark에게 주도권을 넘겼다. 현재는 HDFS 기반 배치 처리와 Hive 쿼리 엔진의 백엔드로 활용되며, 클라우드 마이그레이션 시 오브젝트 스토리지 + Spark/Trino 조합으로 전환하는 것이 현대적 아키텍처 방향이다.

📢 **섹션 요약 비유**: MapReduce는 철도 — 대량 화물 운송엔 여전히 최적이지만, 고속도로(Spark)와 항공(스트리밍)이 생기면서 역할이 재정의됐다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| HDFS (Hadoop Distributed File System) | 저장 레이어 | 분산 파일 시스템 |
| YARN (Yet Another Resource Negotiator) | 리소스 관리 | 클러스터 자원 할당 |
| Apache Spark | 후계자 | 인메모리 처리로 MapReduce 대체 |
| Data Locality | 핵심 원리 | 연산을 데이터 위치로 이동 |
| Shuffle | 병목 단계 | 네트워크+디스크 I/O 집중 단계 |

### 👶 어린이를 위한 3줄 비유 설명

1. MapReduce는 큰 퍼즐을 여러 친구가 나눠서 맞추는 것 — 각자 맡은 조각을 맞추고(Map), 전부 모아서 최종 그림을 완성해(Reduce).
2. 중간에 결과를 모두 종이에 적어(디스크) 주고받아야 해서 시간이 걸려.
3. Spark는 종이 대신 머릿속(메모리)에 기억하면서 처리해서 훨씬 빨라!
