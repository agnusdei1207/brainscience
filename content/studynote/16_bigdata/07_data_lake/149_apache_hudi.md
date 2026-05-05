+++
weight = 149
title = "149. Apache Hudi (Hadoop Upserts Deletes Incrementals) — CDC 지원 레이크"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Apache Hudi (Hadoop Upserts Deletes Incrementals) — CDC 지원 레이크은(는) 원시 데이터 저장의 유연성과 분석 거버넌스의 통제를 함께 확보하기 위한 현대 데이터 플랫폼 핵심 개념이다.
> **비유**: 자유롭게 물을 모으는 저수지에 수문·정수 설비를 함께 갖춘 복합 수자원 시설과 같다.

📝 모범 답안

## 1. 개요 및 필요성

Uber는 수천 개의 MySQL 테이블을 Hadoop 데이터 레이크에 동기화해야 했다. 전통적인 배치 ETL은 전체 테이블을 매일 덮어쓰는 방식으로, 테이블 크기가 증가할수록 비용이 급증하는 문제가 있었다. 또한 라이더/드라이버 데이터 삭제(개인정보 보호법) 요청에 대응하기 위한 레코드 단위 삭제 기능도 필요했다.

Uber는 2016년 Hudi를 개발하여 레이크에서 CDC 기반 실시간 upsert를 가능하게 했고, 2019년 Apache 재단에 기증했다.

| 문제 (기존 레이크) | Hudi 해결책 |
|:---|:---|
| CDC 반영 = 전체 재작성 | Upsert API로 변경 레코드만 처리 |
| 레코드 삭제 불가 | Hard Delete (물리) / Soft Delete (논리) |
| 변경분 재처리 | Incremental Query로 타임라인 구간 조회 |
| 읽기/쓰기 성능 선택 | COW(읽기 최적) vs MOR(쓰기 최적) |

---

## 2. 구성요소

```
┌─────────────────────────────────────────────────────────────────┐
│                  Apache Hudi 내부 구조                           │
├─────────────────────────────────────────────────────────────────┤
│  .hoodie/  (Timeline)                                           │
│  ├── 20260421120000.commit    (완료된 커밋)                      │
│  ├── 20260421120000.clean     (클리너 실행 이력)                 │
│  └── 20260421120000.compaction (컴팩션 이력)                     │
│                                                                 │
│  COW (Copy-on-Write) 테이블:                                    │
│  ┌───────────┐  Write    ┌─────────────────┐                   │
│  │ 변경 레코드│ ────────▶ │ 파일 전체 재작성 │ (base Parquet)    │
│  └───────────┘           └─────────────────┘                   │
│                                                                 │
│  MOR (Merge-on-Read) 테이블:                                    │
│  ┌───────────┐  Write    ┌────────────────┐                    │
│  │ 변경 레코드│ ────────▶ │ Delta Log 파일  │ (.log, Avro)      │
│  └───────────┘           └───────┬────────┘                    │
│                                  │ 읽기 시 병합                  │
│                         ┌────────▼────────┐                    │
│                         │ Base Parquet +  │                     │
│                         │ Delta Log 병합  │                     │
│                         └─────────────────┘                    │
│                          (주기적 Compaction으로 병합 고정)        │
└─────────────────────────────────────────────────────────────────┘
```

**COW vs MOR 비교**

| 항목 | COW (Copy-on-Write) | MOR (Merge-on-Read) |
|:---|:---|:---|
| 쓰기 방식 | 변경 행 포함 파일 전체 재작성 | Delta Log 파일에 추가만 |
| 읽기 방식 | Parquet 직접 읽기 (빠름) | Base + Delta 병합 (느림) |
| 쓰기 지연 | 높음 (파일 재작성 비용) | 낮음 (로그 추가만) |
| 읽기 지연 | 낮음 | Compaction 전까지 높음 |
| 적합 워크로드 | 읽기 집중, 배치 CDC | 쓰기 집중, 실시간 CDC |
| Compaction 필요 | 없음 | 필요 (주기적 로그 정리) |

---

## 3. 구조 및 원리

**핵심 조건**: 저장 포맷, 메타데이터, 트랜잭션, 거버넌스 계층을 함께 설계해야 한다.

동작 순서:
**Hudi 쿼리 타입 (3가지)**

| 쿼리 타입 | 설명 | 사용 목적 |
|:---|:---|:---|
| Snapshot Query | 최신 스냅샷 전체 조회 | 일반 조회, BI |
| Incremental Query | 특정 시간 구간의 변경분만 조회 | CDC 파이프라인, 증분 처리 |
| Read-Optimized Query | Base 파일만 읽기 (MOR에서 Delta 무시) | 높은 읽기 성능 필요 시 |

**Hudi vs Delta Lake vs Iceberg**

| 항목 | Hudi | Delta Lake | Iceberg |
|:---|:---|:---|:---|
| 주요 강점 | CDC/upsert 특화, 증분 처리 | Spark 생태계 성숙도 | 멀티엔진 표준, 히든 파티셔닝 |
| 쓰기 방식 선택 | COW / MOR 선택 가능 | COW 방식 | COW 방식 (행 삭제 파일 별도) |
| 증분 처리 API | Incremental Query 공식 지원 | 체인지 데이터 피드(CDF) | 증분 스캔 API |
| 주요 채택 | Cloudera, AWS EMR | Databricks | AWS Athena, Snowflake |

---

## 4. 비교 및 연결

**주요 활용 시나리오**

- **GDPR 삭제**: Hard Delete API로 특정 사용자의 모든 레코드를 레이크에서 물리 삭제
- **실시간 CDC**: Debezium → Kafka → Spark Structured Streaming → Hudi MOR 테이블 upsert
- **증분 배치**: 매시간 Incremental Query로 변경분만 읽어 하위 집계 테이블 갱신
- **대용량 upsert**: 수억 건의 MySQL 테이블을 Hudi로 매일 delta 동기화

**핵심 운영 태스크**

| 태스크 | 설명 | Hudi API |
|:---|:---|:---|
| Compaction | MOR 로그 파일을 Parquet로 병합 | `HoodieCompactionJob` |
| Cleaning | 만료 파일 버전 정리 | `HoodieCleanJob` |
| Clustering | 데이터 파일 정렬·통합 | `HoodieClusteringJob` |
| Index 관리 | 레코드 키 → 파일 위치 매핑 | Bloom/Bucket/Record Level |

---

## 5. 실무 적용 및 판단

| 효과 | 내용 |
|:---|:---|
| CDC 실시간화 | 배치 전체 재작성 → 변경분만 upsert로 지연 수 시간 → 수 분 단축 |
| 스토리지 효율 | 전체 테이블 복사 제거로 스토리지 사용량 30~60% 절감 |
| 규정 준수 | GDPR·CCPA 삭제 요구를 레이크 단계에서 직접 처리 |
| 증분 파이프라인 | Incremental Query로 하위 파이프라인 컴퓨팅 비용 대폭 감소 |

Apache Hudi는 CDC와 upsert가 핵심 요건인 데이터 레이크 환경에서 독보적인 강점을 가진다. Cloudera CDP, AWS EMR, Google Dataproc에서 기본 지원하며, GDPR 대응과 실시간 CDC가 요건인 프로젝트에서 Delta Lake, Iceberg와 함께 1순위 후보다. 기술사 시험에서는 **COW vs MOR 트레이드오프**, **Timeline 구조**, **Incremental Query 활용**이 핵심 논점이다.

---

## 6. 기대효과 및 결론

Apache Hudi (Hadoop Upserts Deletes Incrementals) — CDC 지원 레이크은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 레이크하우스 계열 기술은 저장 유연성과 거버넌스 통제를 동시에 달성할 때 비로소 플랫폼 가치가 커진다.

---

## 7. 발전 흐름도

```text
[HDFS]
    │
    ▼
[Delta Lake]
    │
    ▼
[Apache Hudi]
    │
    ▼
[Copy-on-Write]
    │
    ▼
[Merge-on-Read]
    │
    ▼
[Data Lakehouse]
```

HDFS 기반 데이터 레이크에서 ACID와 증분 처리 요구가 더해지며 Hudi와 레이크하우스 아키텍처로 발전하는 흐름이다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| COW 테이블 | 핵심 설계 | 쓰기 시 전체 파일 재작성, 읽기 최적 |
| MOR 테이블 | 핵심 설계 | 델타 로그 추가 방식, 쓰기 최적 |
| Timeline | 메타데이터 구조 | `.hoodie/` 내 커밋·클린·컴팩션 이력 |
| Incremental Query | 쿼리 타입 | 특정 구간 변경분만 조회 |
| Compaction | 운영 태스크 | MOR 로그 파일 → Parquet 병합 |
| GDPR 삭제 | 활용 사례 | Hard Delete API로 레코드 물리 삭제 |
