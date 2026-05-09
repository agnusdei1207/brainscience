+++
weight = 1
title = "1. Hadoop·Spark·MapReduce (Hadoop Spark MapReduce)"
date = "2026-05-09"
[extra]
categories = "gisulsa-bigdata"
+++
# 🎯 핵심 키워드: Hadoop, Spark, MapReduce

> **출제 빈도**: ★★★★★ | **난이도**: ★★★☆☆

## 1. 정의 (Definition)

Hadoop은 HDFS와 YARN을 기반으로 대규모 분산 저장·처리를 지원하는 빅데이터 생태계다.  
MapReduce는 데이터를 분산 처리하기 위한 배치 계산 모델로, Map 단계와 Reduce 단계를 통해 대량 데이터를 병렬 처리한다.  
Spark는 메모리 기반 분산 처리 엔진으로 MapReduce 대비 반복 연산과 대화형 분석에 유리하다.

## 2. 출제 포인트 (Exam Key Points)

| 포인트 | 내용 | 채점 비중 |
|--------|------|----------|
| 정의 | Hadoop은 HDFS와 YARN을 기반으로 대규모 분산 저장·처리를 지원하는 빅데이터 생태계다.와 Spark는 메모리 기반 분산 처리 엔진으로 MapReduce 대비 반복 연산과 대화형 분석에 유리하다.의 인과관계를 한 문장 구조로 묶어 서술한다. | 20% |
| 구성요소 | 분산 파일시스템과 리소스 관리, 배치 처리와 DAG 실행, 메모리 처리와 반복 연산를 구조-동작-효과 순으로 정리한다. | 30% |
| 비교/차이 | Hadoop MapReduce vs Spark의 선택 기준과 트레이드오프를 비교표로 제시한다. | 30% |
| 적용사례 | 대규모 로그 분석과 데이터 처리 플랫폼 구축 관점에서 기대효과와 실패 포인트를 함께 적는다. | 20% |

## 3. 답안 목차 템플릿 (Answer Outline Template)

문제: "Hadoop과 Spark, MapReduce의 개념과 차이를 설명하시오."

```text
Ⅰ. 개요
   1. 정의
   2. 대용량 데이터 처리 요구 증가

Ⅱ. 핵심 구성요소
   1. 분산 처리 플랫폼 구조
   2. 배치 엔진별 특징과 선택

Ⅲ. 특징 및 장단점
   1. 대규모 데이터 병렬 처리 가능
   2. 운영 복잡도와 자원 관리 부담

Ⅳ. 유사 기술과의 비교
   - Hadoop MapReduce vs Spark 비교표

Ⅴ. 적용사례 및 향후전망
   1. 대규모 로그 분석과 데이터 처리 플랫폼 구축
   2. Lakehouse와 통합 처리 엔진 확장
```

## 4. 핵심 비교표 (Key Comparison Table)

| 구분 | Hadoop MapReduce | Spark |
| --- | --- | --- |
| 처리 방식 | 디스크 기반 배치 처리 | 메모리 기반 DAG 처리 |
| 장점 | 안정적 대량 처리 | 반복 연산과 실시간성 우수 |
| 단점 | 지연 시간이 큼 | 메모리 자원 요구 큼 |
| 적합 사례 | 대규모 배치 ETL | 인터랙티브 분석, ML |
| 시험 포인트 | Batch job | In-memory compute |

## 5. 인출 훈련 문제 (Output Drills)

### 단답형 (30초)
1. Hadoop의 정의를 한 문장으로 쓰시오.
2. Hadoop·Spark·MapReduce 답안에서 반드시 써야 할 핵심 구성요소 3가지를 나열하시오.
3. Hadoop MapReduce와 Spark의 가장 큰 차이점을 설명하시오.
4. "저장(HDFS)-자원(YARN)-처리 엔진 차이를 연결해 설명하는 연습"를 답안 키워드 3개로 압축하시오.
5. 대규모 로그 분석과 데이터 처리 플랫폼 구축 중 하나를 들고 기대효과 2가지를 말하시오.

### 서술형 (5분)
6. "Hadoop과 Spark, MapReduce의 개념과 차이를 설명하시오."의 핵심 구성요소와 기대효과를 5분 답안으로 정리하시오.
7. "Hadoop MapReduce vs Spark"의 선택 기준과 실패 시 발생하는 운영 리스크를 서술하시오.

### 답안 작성 (25분)
8. "Hadoop과 Spark, MapReduce의 개념과 차이를 설명하시오." (개념, 구조, 비교, 적용사례, 향후전망 포함)

## 6. 면접 예상 질문 (Mock Interview)

Q1: "MapReduce와 Spark의 차이는 무엇입니까?"  
Q2: "Spark가 반복 연산에 유리한 이유는 무엇입니까?"  
Q3: "배치 중심 환경에서는 어떤 엔진을 우선 선택하시겠습니까?"
