+++
weight = 31
title = "31. Oozie vs Airflow — 워크플로 스케줄러 비교"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: Apache Oozie는 Hadoop 생태계 전용 XML 기반 워크플로 스케줄러이고, Apache Airflow는 Python DAG 기반 범용 오케스트레이터다. 현대 데이터 엔지니어링에서는 Airflow가 사실상 표준(de facto)이 됐다.
> **비유**: 여러 공정이 연결된 생산 라인처럼, 앞단의 입력 품질과 중간 단계의 흐름 제어가 최종 결과를 좌우하는 구조와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

Oozie vs Airflow — 워크플로 스케줄러 비교은 데이터 엔지니어링에서 입력 데이터의 특성, 처리 방식, 운영 제어를 함께 다루는 주제다. 이 개념이 필요한 이유는 시스템이 커질수록 데이터 규모와 변화 속도, 품질 요구가 동시에 증가하기 때문이다. 따라서 이 주제를 이해할 때는 정의만 암기할 것이 아니라, 어떤 한계를 해결하려고 등장했고 어떤 조건에서 효과가 나는지까지 함께 봐야 한다.

```text
워크플로 스케줄러 비교:

  Oozie:                    Airflow:
  workflow.xml              from airflow import DAG
  <workflow-app>            from airflow.operators import *
    <action name="hive">    
      <hive>...</hive>      with DAG('etl', ...) as dag:
      <ok to="next"/>         t1 = HiveOperator(...)
      <error to="fail"/>      t2 = SparkSubmitOperator(...)
    </action>                 t1 >> t2
  </workflow-app>
  
  XML 설정 → Python 코드
  복잡하고 장황 → 직관적
```

---

## 2. 구성요소

| 컴포넌트 | 역할 |
|:---|:---|
| **Scheduler** | DAG 파싱·실행 스케줄링 |
| **Executor** | 태스크 실행 (Local/Celery/K8s) |
| **Worker** | 실제 태스크 수행 |
| **Metadata DB** | DAG·태스크 상태 저장 (PostgreSQL) |
| **Webserver** | 모니터링 UI |
| **DAG Bag** | DAG 파일 디렉토리 |

---

## 3. 구조 및 원리

**핵심 조건**: Oozie vs Airflow — 워크플로 스케줄러 비교은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 비교 | Oozie | Airflow | Prefect | Dagster |
|:---|:---|:---|:---|:---|
| 설정 방식 | XML | Python | Python | Python |
| Hadoop 통합 | ✅ 최적 | ✅ Operator | ❌ | ❌ |
| 클라우드 | △ 제한 | ✅ 풍부 | ✅ | ✅ |
| UI | 기본 | 강력 | 강력 | 강력 |
| 데이터 인식 | ❌ | △ | ✅ | ✅ |

동작 순서:
1. **입력 정의**: 해당 주제가 다루는 데이터·요청·상태를 명확히 식별한다. 입력 경계가 불분명하면 품질 검증과 책임 분리가 무너진다.
2. **처리 규칙 적용**: 저장 구조, 연산 로직, 분산 처리, 학습 규칙 중 핵심 메커니즘을 실행한다. 이 단계가 성능·확장성·정확도를 결정한다.
3. **결과 검증**: 정합성, 지연, 비용, 품질 지표를 확인해 운영 가능한 상태인지 판단한다. 이 검증이 없으면 실험은 가능해도 서비스화는 어렵다.
4. **운영 피드백 반영**: 드리프트, 부하 변화, 장애, 스키마 변화에 대응해 구조를 다시 조정한다. 실무에서는 이 폐쇄 루프가 기술의 지속성을 만든다.

```text
[입력/이벤트]
      ↓
[저장·정제·변환]
      ↓
[핵심 연산/학습/질의]
      ↓
[검증·배포·활용]
      ↓
[모니터링·재조정]
```

---

## 4. 비교 및 연결

```python
from airflow import DAG
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

with DAG(
    dag_id='daily_etl',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:
    
    extract = HiveOperator(
        task_id='extract',
        hql='INSERT INTO staging SELECT * FROM raw WHERE date = "{{ ds }}"'
    )
    
    transform = SparkSubmitOperator(
        task_id='transform',
        application='/jobs/transform.py',
        application_args=['--date', '{{ ds }}']
    )
    
    extract >> transform  # 의존성 정의
```

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:Episcopal: 내용 |
|:---|:---|
| **가시성** | DAG UI로 파이프라인 전체 상태 확인 |
| **유연성** | Python으로 복잡한 의존성 표현 |
| **통합성** | 200+ Operator로 모든 서비스 연결 |

LLM 기반 DAG 자동 생성이 등장하고 있다. "매일 새벽 2시에 S3에서 데이터 읽어서 BigQuery에 적재하고 실패 시 Slack 알림"을 자연어로 입력하면 Airflow DAG 코드를 자동 생성하는 도구가 실용화 단계에 있다. 데이터 엔지니어의 역할이 DAG 작성에서 요구사항 정의로 이동하고 있다.

```text
1단계: Oozie XML 분석
  - workflow.xml → 태스크 그래프 추출
  - coordinator.xml → 스케줄 패턴 추출

2단계: Airflow DAG 변환
  - Oozie Action → Airflow Operator 매핑
  - Oozie OK/Error → Airflow trigger_rule
  - Oozie 변수 → Airflow Jinja 템플릿

3단계: 병행 운영
  - 동일 파이프라인 양쪽 실행 비교
  - 결과 일치 확인

4단계: Oozie 종료
```

```text
AWS MWAA (Managed Workflows for Apache Airflow):
  - Airflow 클러스터 관리 자동화
  - VPC 통합, IAM 권한 관리
  - 자동 스케일링

GCP Cloud Composer:
  - GKE 기반 관리형 Airflow
  - BigQuery·GCS 네이티브 통합

Azure Data Factory:
  - 비주얼 파이프라인 (GUI 방식)
  - Airflow 아닌 독자 오케스트레이터
```

---

## 6. 기대효과 및 결론

LLM 기반 DAG 자동 생성이 등장하고 있다.

Oozie vs Airflow — 워크플로 스케줄러 비교의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
[Cron + 쉘 스크립트 — 기초 배치 스케줄링]
    │
    ▼
[Apache Oozie — Hadoop 전용 XML 스케줄러]
    │
    ▼
[Apache Airflow — Python DAG 범용 오케스트레이터]
    │
    ▼
[관리형 Airflow — AWS MWAA, GCP Composer]
    │
    ▼
[LLM DAG 생성 — 자연어 → 파이프라인 자동 생성]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **DAG** | Airflow 워크플로 표현 단위 |
| **Operator** | Airflow 태스크 실행 단위 |
| **Celery Executor** | 분산 태스크 실행 엔진 |
| **AWS MWAA** | 관리형 Airflow 클라우드 서비스 |
| **Prefect/Dagster** | 차세대 데이터 오케스트레이터 |
