+++
weight = 58
title = "Tungsten Engine"
date = "2024-03-23"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Tungsten Engine은(는) 인메모리 분산 실행과 쿼리 최적화를 통해 대화형 분석·배치·스트리밍을 빠르게 연결하는 스파크 핵심 개념이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

- **정의**: Spark의 데이터 처리 속도를 개선하기 위해 하드웨어 아키텍처(CPU, RAM)를 최대한 활용하도록 설계된 엔진 계층이다.
- **배경**: Spark의 병목 현상이 네트워크/디스크 I/O에서 CPU와 메모리로 이동함에 따라, Java 객체의 높은 메모리 사용량과 GC(Garbage Collection) 부하를 해결하기 위해 등장했다.

---

## 2. 구성요소

- **Memory Management & Binary Processing**: 데이터를 Java 객체로 변환하지 않고 바이너리 형태로 메모리에 직접 저장한다. Unsafe Row 형식을 사용하여 직렬화 비용을 최소화한다.
- **Cache-aware Computation**: CPU 캐시(L1/L2/L3)의 지역성(Locality)을 고려한 알고리즘을 사용하여 캐시 미스를 줄인다.

```text
[ Tungsten CPU & Memory Optimization ]

   [ Standard JVM Approach ]          [ Tungsten Approach ]
   +-----------------------+        +--------------------------+
   |   Java Object (Rich)  |        | Binary Data (Row format) |
   | (Metadata, Padding)   | <----   +-----------------------+        +--------------------------+
               |                                |
       High GC Pressure                 Direct Memory Access
      High Cache Misses                 Cache-aware Algorithms
```

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:
| 최적화 기법 | 주요 내용 | 기대 효과 |
| :--- | :--- | :--- |
| **Off-heap Memory** | JVM 힙 외부에서 메모리 직접 관리 | GC 부하 제거 및 대용량 메모리 효율성 |
| **Binary Row Format** | 데이터를 바이너리 직렬화 형태로 유지 | 메모리 사용량 감소 (객체 오버헤드 제거) |
| **Whole-stage CodeGen** | 여러 연산(Select, Filter 등)을 하나의 코드로 병합 | 가상 함수 호출 제거 및 루프 최적화 |
| **Vectorized Processing** | SIMD(Single Instruction Multiple Data) 활용 | CPU 연산 처리량(Throughput) 극대화 |

---

## 4. 비교 및 연결

- **메모리 설정**: `spark.memory.offHeap.enabled=true` 설정을 통해 Tungsten의 Off-heap 기능을 활성화하여 GC 이슈가 잦은 대규모 워크로드를 안정화할 수 있다.
- **데이터 구조 선택**: RDD보다는 Tungsten의 혜택을 100% 받을 수 있는 DataFrame/Dataset API 사용을 강력히 권고한다. RDD는 Java 객체 오버헤드를 그대로 가지기 때문이다.

---

## 5. 실무 적용 및 판단

- Tungsten은 Spark를 단순한 분산 프레임워크를 넘어 고성능 분석 엔진으로 진화시켰다. 최신 버전의 Spark에서는 벡터화된 실행(Vectorized Execution) 범위가 더욱 넓어지고 있으며, 이는 GPU 가속(RAPIDS) 및 차세대 하드웨어와의 융합으로 이어지는 토대가 되고 있다.

---

## 6. 기대효과 및 결론

Tungsten Engine은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[RDD]
    │
    ▼
[DataFrame]
    │
    ▼
[Tungsten 엔진]
    │
    ▼
[코드 생성 (Code Generation)]
    │
    ▼
[Photon 엔진]
```

Spark의 데이터 표현이 RDD에서 DataFrame으로 발전하고 Tungsten 최적화를 거쳐 하드웨어 가속 엔진으로 이어지는 흐름이다.

---

## 8. 관련 개념 맵

- **부모 개념**: Apache Spark
- **자식 개념**: Off-heap Memory, Whole-stage Code Generation
- **연관 개념**: Catalyst Optimizer, GC(Garbage Collection), SIMD
