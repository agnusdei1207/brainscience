+++
weight = 213
title = "213. 맵리듀스 (MapReduce)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: MapReduce는 대용량 데이터를 Map(필터링·변환)과 Reduce(집계·합산) 두 단계로 분할하여 수천 노드에 병렬 처리하는 분산 연산 프레임워크로, 구글 논문(2004)을 기반으로 Hadoop이 구현했다.
> **비유**: MapReduce는 선거 개표 방식과 같다. 투표함(데이터)을 전국 개표소(Map 단계)에서 각자 집계하고, 그 결과를 중앙선거관리위원회(Reduce 단계)로 모아 최종 합산한다. 한 곳에서 다 세는 것보다 훨씬 빠르다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

구글은 2004년 발표한 논문 "MapReduce: Simplified Data Processing on Large Clusters"에서 수천 대 서버에서 페타바이트 데이터를 처리하는 방법을 제시했다. 핵심 아이디어는 단순하다: **데이터를 잘게 쪼개어 병렬로 처리하고, 결과를 한 곳에 모아 합산한다.**

MapReduce의 이름은 두 핵심 연산에서 왔다. **Map**은 입력 데이터를 처리하여 키-값(Key-Value) 쌍으로 변환하는 과정이고, **Reduce**는 같은 키를 가진 모든 값을 모아서 집계(합산, 카운트 등)하는 과정이다. 이 두 연산의 조합으로 필터링, 정렬, 집계, 조인 같은 대부분의 데이터 처리가 가능하다.

MapReduce는 함수형 프로그래밍의 map()과 reduce() 개념을 분산 시스템에 적용한 것이다. Python의 `map()`이 리스트의 각 원소에 함수를 적용하는 것처럼, 분산 Map은 수천 노드의 각 데이터 파티션에 함수를 적용한다.

---

## 2. 구성요소

### MapReduce 처리 단계

```
  입력 데이터 (HDFS 블록)
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │                   Map 단계                               │
  │                                                          │
  │  Split 1: [hello world] → (hello,1) (world,1)           │
  │  Split 2: [hello hadoop] → (hello,1) (hadoop,1)          │
  │  Split 3: [world hello] → (world,1) (hello,1)            │
  └────────────────────────────────────────────────────────┘
       │
       ▼ Shuffle & Sort (같은 키끼리 모으기)
  ┌─────────────────────────────────────────────────────────┐
  │                 Shuffle & Sort 단계                      │
  │                                                          │
  │  hadoop: [(hadoop,1)]                                    │
  │  hello:  [(hello,1), (hello,1), (hello,1)]              │
  │  world:  [(world,1), (world,1)]                         │
  └────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │                  Reduce 단계                             │
  │                                                          │
  │  hadoop: sum([1]) = 1                                    │
  │  hello:  sum([1,1,1]) = 3                               │
  │  world:  sum([1,1]) = 2                                 │
  └────────────────────────────────────────────────────────┘
       │
       ▼
  출력: hadoop=1, hello=3, world=2 (HDFS에 저장)
```

### MapReduce 처리 흐름

| 단계 | 역할 | 저장 위치 |
|:---:|:---|:---:|
| Input Split | 입력 데이터를 Map Task 단위로 분할 | HDFS |
| Map | 키-값 쌍으로 변환·필터링 | 로컬 디스크 |
| Combiner | 로컬 사전 집계 (Reduce 전 최적화) | 로컬 디스크 |
| Shuffle & Sort | 같은 키를 같은 Reducer로 전송 | 네트워크 + 디스크 |
| Reduce | 집계·합산 처리 | HDFS |
| Output | 최종 결과 저장 | HDFS |

### Java MapReduce 코드 예시 (단어 빈도 계산)

```java
// Mapper 클래스
public class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    private Text word = new Text();
    private IntWritable one = new IntWritable(1);
    
    @Override
    protected void map(LongWritable key, Text value, Context context) 
            throws IOException, InterruptedException {
        // 각 줄을 공백으로 분리하여 단어 추출
        StringTokenizer tokenizer = new StringTokenizer(value.toString());
        while (tokenizer.hasMoreTokens()) {
            word.set(tokenizer.nextToken());
            context.write(word, one);  // (단어, 1) 출력
        }
    }
}

// Reducer 클래스
public class WordCountReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context) 
            throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable val : values) {
            sum += val.get();  // 같은 단어의 1들을 모두 합산
        }
        context.write(key, new IntWritable(sum));  // (단어, 빈도) 출력
    }
}
```

---

## 3. 구조 및 원리

**핵심 조건**: 변경 자동화와 운영 안정성은 별개가 아니라 하나의 루프이며, 빌드·검증·배포·관측·피드백이 끊기지 않아야 지속 개선이 가능하다.

동작 순서:
1. 변경 사항을 버전 관리 시스템에서 감지한다.
2. 빌드·테스트·보안 검증으로 변경의 품질을 빠르게 확인한다.
3. 승인된 산출물을 선언형 배포나 자동화 파이프라인으로 운영 환경에 반영한다.
4. 메트릭·로그·트레이스를 통해 실제 동작 결과를 관측한다.
5. 피드백을 다음 개선 주기에 연결해 반복적으로 신뢰성을 높인다.

### MapReduce vs Apache Spark

| 항목 | MapReduce | Apache Spark |
|:---|:---|:---|
| 데이터 저장 | 매 단계 디스크(HDFS) 기록 | 메모리(RAM) 우선 |
| 속도 | 느림 (디스크 I/O 병목) | 10~100배 빠름 |
| 반복 처리 | 매 반복마다 디스크 쓰기/읽기 | 메모리에 데이터 유지 |
| ML 지원 | 제한적 (MLlib 없음) | SparkML 내장 |
| 언어 | Java (verbose) | Python/Scala/Java/R |
| 현재 트렌드 | 점차 대체 중 | 산업 표준 |

### MapReduce 적합/비적합 케이스

| 케이스 | 적합 여부 | 이유 |
|:---|:---:|:---|
| 수십 TB 로그 분석 (1회) | ✅ | 대규모 배치, 결과 재사용 없음 |
| 반복적 ML 모델 학습 | ❌ | 매 반복 디스크 I/O → 극도로 느림 |
| 실시간 스트림 처리 | ❌ | 배치 모델, 실시간 불가 |
| 단순 집계 쿼리 | ⚠️ | Hive/SparkSQL이 더 편리 |

---

## 4. 비교 및 연결

**MapReduce 실행 최적화**:
```
1. Combiner 활용:
   Reducer에 보내기 전 로컬에서 사전 집계
   예: Map 결과 (hello,1)(hello,1)(hello,1) → Combiner → (hello,3)
   → 네트워크 트래픽 대폭 감소

2. 적절한 Reducer 수 설정:
   - 너무 적으면: 일부 Reducer에 부하 집중 (Skew)
   - 너무 많으면: 작은 파일 다수 생성, NameNode 부하

3. 입력 포맷 최적화:
   - ORC, Parquet 같은 컬럼형 저장 포맷 사용
   - 압축 코덱 적용 (Snappy, LZO)
```

**AWS EMR에서 MapReduce 실행**:
```bash
aws emr add-steps \
  --cluster-id j-XXXXX \
  --steps Type=CUSTOM_JAR,\
          Name="WordCount",\
          ActionOnFailure=CONTINUE,\
          Jar=s3://mybucket/wordcount.jar,\
          Args=[s3://mybucket/input/,s3://mybucket/output/]
```

**기술사 판단 포인트**:
- MapReduce는 학습 목적과 레거시 시스템 이해를 위해 알아야 하지만, 신규 개발에는 Spark를 사용하는 것이 표준이다.
- Shuffle 단계가 MapReduce의 성능 병목이다. 데이터 스큐(Skew)가 있으면 일부 Reducer가 과부하되어 전체 Job이 지연된다.
- 구글은 MapReduce를 2014년 자체 시스템에서 Dremel(BigQuery의 전신)과 Millwheel로 대체했다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 설명 |
|:---|:---|
| 자동 병렬화 | 개발자가 병렬화 코드를 작성하지 않아도 됨 |
| 자동 장애 복구 | Task 실패 시 프레임워크가 자동 재실행 |
| 대규모 처리 | 수천 노드에서 페타바이트 데이터 처리 |
| 단순한 프로그래밍 모델 | Map + Reduce 두 함수만 작성 |

MapReduce는 빅데이터 처리의 첫 번째 민주화였다. 구글만 할 수 있었던 수천 노드 분산 처리를 누구나 가능하게 했다. 현재는 Spark에 자리를 내줬지만, Spark도 MapReduce의 개념을 계승·개선한 것이다. MapReduce를 이해해야 Spark의 가치를 제대로 평가할 수 있다.

---

## 6. 기대효과 및 결론

맵리듀스 (MapReduce)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 맵리듀스 (MapReduce)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
MapReduce 처리 흐름
    ├─► Map: 데이터 분할 → 키-값 쌍 추출
    ├─► Shuffle & Sort: 같은 키끼리 모으기
    └─► Reduce: 집계 · 요약
    │
    ▼
한계: 디스크 I/O 병목 → Spark (In-Memory) 대체
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| HDFS | MapReduce의 입력/출력 저장소 |
| YARN | MapReduce 작업의 CPU/메모리 자원을 배분하는 관리자 |
| Apache Spark | MapReduce의 디스크 I/O 한계를 극복한 후계자 |
| Shuffle & Sort | MapReduce 성능 병목의 핵심 단계 |
| Combiner | 로컬 사전 집계로 Shuffle 트래픽 감소 최적화 |
| 구글 MapReduce 논문 | HDFS, MapReduce 모두의 이론적 기원 |

---
