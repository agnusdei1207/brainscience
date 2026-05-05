+++
weight = 75
title = "24. Apache Spark 3.5 주요 개선 사항"
date = "2026-04-29"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Apache Spark 3.5는 2023년 릴리스되어 Python API (PySpark)의 기능 강화, Spark Connect (원격 클라이언트 연결), ANSI SQL 지원 확대, 구조화된 스트리밍(Structured Streaming) 고도화를 통해 데이터 엔지니어링·ML 워크플로우의 생산성과 이식성을 높인 메이저 버전이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

Apache Spark 3.5는 Spark 3.x 시리즈의 주요 기능 업데이트로, 사용 편의성·성능·SQL 표준 준수를 중점적으로 개선했다.

```text
┌──────────────────────────────────────────────────────────┐
│          Spark 3.5 핵심 개선 영역                          │
├──────────────────────────────────────────────────────────┤
│  1. Spark Connect — 경량 원격 클라이언트 연결               │
│  2. Python UDTF — 테이블 반환 Python 함수                  │
│  3. ANSI SQL 강화 — 표준 SQL 호환성 확대                   │
│  4. Structured Streaming — 상태 관리 고도화                │
│  5. PySpark + PyArrow — 데이터 교환 성능 향상              │
│  6. Spark SQL 함수 확장 — 300+ 신규 함수 추가              │
└──────────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### Spark Connect 아키텍처

```text
[로컬 Python/Notebook 클라이언트]
         │ gRPC 연결 (Protocol Buffers)
         ▼
[Spark Connect Server (클러스터)]
         │
         ▼
[Spark 드라이버 → 익스큐터]
```

Spark Connect 이전: 드라이버 JVM에 직접 연결 (언어 의존성, 버전 충돌).
Spark Connect 이후: 임의 언어 클라이언트에서 안정적 원격 접속.

### Python UDTF (User-Defined Table Function)

```python

from pyspark.sql.functions import udtf

@udtf(returnType="num: int, squared: int")
class SquaredNumbers:
    def eval(self, n: int):
        for i in range(n):
            yield i, i ** 2

spark.udtf.register("squared", SquaredNumbers)
spark.sql("SELECT * FROM squared(5)").show()
```

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:
| 버전 | 주요 특징 |
|:---|:---|
| **Spark 2.x** | DataFrame API, Spark SQL, ML lib |
| **Spark 3.0** | AQE(Adaptive Query Execution), 동적 파티션 프루닝 |
| **Spark 3.4** | Spark Connect 프리뷰, ANSI 강화 시작 |
| **Spark 3.5** | Spark Connect GA, Python UDTF, Streaming 고도화 |
| **Spark 4.0 (예정)** | Python-first API, 추가 통합 |

AQE (Adaptive Query Execution, 적응형 쿼리 실행)는 Spark 3.0에서 도입되어 런타임 통계 기반으로 실행 계획을 동적으로 재최적화하는 기능으로, 3.5에서 더욱 안정화되었다.

---

## 4. 비교 및 연결

### 실무 시나리오: Spark Connect 기반 노트북 개발 환경 구축
데이터 과학 팀의 Jupyter Notebook에서 원격 Spark 클러스터 직접 활용.

1. **기존**: 각 노트북 서버에 Spark 드라이버 설치, 버전 관리 복잡.
2. **Spark Connect 도입**: Databricks/EMR Spark Connect Server 활성화.
3. **클라이언트**: `pip install pyspark[connect]` 로컬 설치.
4. **연결**: `SparkSession.builder.remote("sc://spark-server:15002").getOrCreate()`.
5. **결과**: 로컬 Python 3.11 + 클러스터 Spark 3.5 독립적 버전 관리 가능.

### 안티패턴
- Spark 3.5로 업그레이드 시 ANSI 모드 변경으로 인한 기존 코드 동작 차이를 간과하는 안티패턴. 예를 들어 Spark 3.4 이전에서 `1/0`이 Infinity 반환 → 3.5 ANSI 모드에서 ArithmeticException 발생. 마이그레이션 전 전체 파이프라인 회귀 테스트가 필수다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:---|:---|
| **개발 편의성** | Spark Connect로 원격 클라이언트 지원 |
| **Python 호환성** | Python UDTF, PyArrow 통합 강화 |
| **SQL 표준화** | ANSI 준수 → 타 DB 이식성 향상 |

Spark 4.0은 Python-first 설계로 Scala API와 동등한 Python API를 목표로 하며, DataFrame API와 Dataset API의 Python 통합 강화가 예정되어 있다. Lakehouse 아키텍처(Delta Lake, Iceberg)와의 더 긴밀한 통합도 예고되어 있다.

---

## 6. 기대효과 및 결론

Apache Spark 3.5 주요 개선 사항은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[Spark 2.x — DataFrame API, SparkSQL 기반 확립]
    │
    ▼
[Spark 3.0 — AQE, 동적 파티션 프루닝 도입]
    │
    ▼
[Spark 3.4 — Spark Connect 프리뷰, ANSI 강화]
    │
    ▼
[Spark 3.5 — Spark Connect GA, Python UDTF, Streaming↑]
    │
    ▼
[Spark 4.0 — Python-first, Lakehouse 통합 강화]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Spark Connect** | 경량 원격 클라이언트 연결; 개발 편의성 핵심 |
| **AQE** | 런타임 적응형 쿼리 최적화; Spark 3.0+ |
| **Python UDTF** | 1행→다행 반환 Python 함수; 3.5 신규 |
| **ANSI SQL** | 표준 SQL 준수 강화; 호환성 이슈 주의 |
| **Spark 4.0** | Python-first API; 차세대 버전 방향 |
