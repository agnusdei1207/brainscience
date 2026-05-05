+++
weight = 51
title = "29. Apache Oozie — Hadoop 워크플로 스케줄러"
date = "2026-04-29"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Apache Oozie는 Hadoop 에코시스템 기반 워크플로(Workflow)와 코디네이터(Coordinator) 잡을 관리하는 서버 기반 스케줄러다. MapReduce·Hive·Pig·Sqoop 등 Hadoop 잡을 DAG(방향성 비순환 그래프)로 구성하여 복잡한 ETL 파이프라인을 자동화한다.
> **비유**: 대형 물류창고에 재고를 나눠 보관하고 작업 지시서를 현장 직원에게 보내는 체계와 같다.

📝 모범 답안

## 1. 개요 및 필요성

```text
┌──────────────────────────────────────────────────────────┐
│          Oozie 워크플로 구조                               │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  워크플로 DAG:                                            │
│  [START] → [Sqoop 임포트] → [Hive ETL] → [Pig 집계]      │
│                                 │                         │
│                           성공/실패 분기                  │
│                         /              \                  │
│                    [이메일 알림]    [오류 처리 잡]          │
│                         \              /                  │
│                              [END]                        │
│                                                           │
│  코디네이터:                                              │
│  매일 02:00 → 전날 데이터 준비 확인 → 워크플로 자동 실행  │
└──────────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### Oozie 구성 요소

| 구성 요소 | 역할 |
|:---|:---|
| **워크플로** | 잡 실행 순서·분기·병렬 정의 (XML DAG) |
| **코디네이터** | 시간/데이터 기반 워크플로 자동 트리거 |
| **번들** | 여러 코디네이터 묶음 관리 |
| **액션 노드** | MapReduce/Hive/Pig/Sqoop 잡 실행 단위 |
| **컨트롤 노드** | start·end·fork·join·decision |

### Oozie vs Apache Airflow

```text
Oozie:
  - XML 기반 설정 (workflow.xml)
  - Hadoop 전용 (YARN/HDFS 의존)
  - 레거시 Hadoop 환경에 적합
  - 데이터 가용성 기반 트리거 강점

Airflow:
  - Python 기반 DAG (코드로 파이프라인)
  - 클라우드·다양한 시스템 통합
  - 모니터링 UI, 동적 DAG, 풍부한 플러그인
  - 현대 데이터 엔지니어링 표준
```

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 배치 위치, 메타데이터 관리, 병렬 실행, 장애 복구가 함께 맞물려야 한다.

동작 순서:
| 비교 | Oozie | Airflow | NiFi |
|:---|:---|:---|:---|
| 설정 방식 | XML | Python DAG | GUI |
| 생태계 | Hadoop 전용 | 범용 | 범용 |
| 모니터링 | 기본 | 강력 | 강력 |
| 현황 | 레거시 | 현재 표준 | 스트리밍 강점 |

---

## 4. 비교 및 연결

### Oozie 워크플로 예시 (XML 개요)

```xml
<!-- workflow.xml 구조 -->
<workflow-app name="daily-etl">
  <start to="sqoop-import"/>
  
  <action name="sqoop-import">
    <sqoop>...</sqoop>
    <ok to="hive-transform"/>
    <error to="fail"/>
  </action>
  
  <action name="hive-transform">
    <hive>...</hive>
    <ok to="end"/>
    <error to="fail"/>
  </action>
  
  <kill name="fail">
    <message>ETL 실패: ${wf:errorMessage(wf:lastErrorNode())}</message>
  </kill>
  <end name="end"/>
</workflow-app>
```

### 마이그레이션: Oozie → Airflow

```text
1. Oozie XML 워크플로를 Airflow Python DAG로 변환
2. YARN 직접 실행 → SparkSubmitOperator, HiveOperator
3. 코디네이터 스케줄 → Airflow cron expression
4. 데이터 가용성 트리거 → Airflow Sensor (HdfsFileSensor)
```

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:---|:---|
| **자동화** | 복잡한 Hadoop ETL 파이프라인 스케줄링 |
| **모니터링** | 잡 실행 이력·상태 중앙 관리 |
| **의존성 관리** | 데이터 가용성 기반 자동 트리거 |

온프레미스 Hadoop 환경에서는 Oozie가 여전히 현역이지만, 클라우드 레이크하우스로 이전하는 기업들은 Airflow·AWS MWAA·Google Cloud Composer로 파이프라인을 마이그레이션하고 있다.

---

## 6. 기대효과 및 결론

Apache Oozie — Hadoop 워크플로 스케줄러은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 하둡 계열 기술의 가치는 개별 컴포넌트보다 저장·자원·처리 계층이 얼마나 안정적으로 결합되는가에 달려 있다.

---

## 7. 발전 흐름도

```text
[Cron + 쉘 스크립트 — 기본 배치 스케줄링]
    │
    ▼
[Apache Oozie — Hadoop 전용 워크플로 스케줄러]
    │
    ▼
[Apache Airflow — Python DAG 기반 범용 오케스트레이터]
    │
    ▼
[클라우드 관리형 — AWS MWAA, GCP Composer]
    │
    ▼
[AI 파이프라인 — MLflow·Kubeflow·Vertex AI 워크플로]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Apache Airflow** | Oozie의 현대적 대안 |
| **DAG** | 워크플로 비순환 의존성 그래프 |
| **Hadoop YARN** | Oozie 잡 실행 환경 |
| **코디네이터** | 시간/데이터 기반 워크플로 트리거 |
| **NiFi** | GUI 기반 데이터 플로우 관리 |
