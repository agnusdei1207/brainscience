+++
weight = 27
title = "05. Apache Oozie와 Airflow - 워크플로우 오케스트레이션의 진화"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Apache Oozie와 Airflow - 워크플로우 오케스트레이션의 진화은(는) 분산 저장, 병렬 처리, 자원 관리를 결합해 대규모 데이터를 저비용으로 처리하게 하는 하둡 계열 핵심 기술이다.
> **비유**: 대형 물류창고에 재고를 나눠 보관하고 작업 지시서를 현장 직원에게 보내는 체계와 같다.

📝 모범 답안

## 1. 개요 및 필요성

Oozie의 Workflow는 XML로 정의되며, HDFS에 배포되어 YARN에서 실행됩니다.

```xml
<!-- Oozie Workflow XML 예시 -->
<workflow-app name="etl-workflow" xmlns="uri:oozie:workflow:0.5">
  <start to="ingest-data"/>
  <action name="ingest-data">
    <hive xmlns="uri:oozie:hive-action:0.5">
      <script>/scripts/ingest.hql</script>
    </hive>
    <ok to="transform-data"/>
    <error to="send-alert"/>
  </action>
  <action name="transform-data">
    <spark xmlns="uri:oozie:spark-action:0.2">
      <master>yarn-cluster</master>
      <script>/scripts/transform.py</script>
    </spark>
    <ok to="end"/>
    <error to="send-alert"/>
  </action>
  <kill name="send-alert">
    <message>Workflow failed, error message[${wf:errorMessage(wf:lastErrorNode())}]</message>
  </kill>
  <end name="end"/>
</workflow-app>
```

---

## 2. 구성요소

Airflow의 DAG는 Python 코드로 정의됩니다.

```python

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

default_args = {
    'owner': 'data_engineer',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='etl_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 2 * * *',  # 매일 새벽 2시
    default_args=default_args,
    catchup=False,
) as dag:

    ingest_task = SnowflakeOperator(
        task_id='ingest_data',
        sql="CALL my_procedure('INSERT');",
        snowflake_conn_id='snowflake_conn',
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_function,
        op_kwargs={'input_key': 'data'},
    )

    check_quality = PythonOperator(
        task_id='check_data_quality',
        python_callable=data_quality_check,
    )

    # 의존성 정의
    ingest_task >> transform_task >> check_quality
    # 또는: ingest_task.set_downstream(transform_task)
```

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 배치 위치, 메타데이터 관리, 병렬 실행, 장애 복구가 함께 맞물려야 한다.

동작 순서:
| 비교 항목 | Apache Oozie | Apache Airflow |
|:---|:---|:---|
| **학습 곡선** | 상대적으로 완만한 (XML熟悉必要) | Python熟悉的 엔지니어에게 친숙 |
| **生态계統合** | Hadoop生态系と紧密结合 | 400+ 외부 시스템Integration (Provider) |
| **모니터링** | 기본적 | 매우 풍부 (Gantt, Tree, Slack 연동) |
| **에러 복구** | 기본 (재시도, 알림) | 세밀함 (Trigger Rules, Depends on Past, Backfill) |
| **멀티 테넌시** | 제한적 | Celery + K8s로良好的 |
| **Python 활용** | 불가 (별도 Python 태스크 필요) | 네이티브 Python 활용 |
| **현재 유지보수** | 크게 활발하지 않음 | 매우 활발 (Apache Airflow + Astronomer, AWS MWAA 등) |

- **Airflow가 주목받는 이유**: Airflow는"코드로서의 데이터 파이프라인"이라는 철학을 통해, 데이터 엔지니어링 팀의 생산성을 크게 향상시켰습니다. Python으로 DAG를 작성하면 Git으로 버전 관리, Pull Request로 코드 리뷰, CI/CD로 자동 테스트가 가능해져"엔지니어링 품질 관리"를 파이프라인에 적용할 수 있습니다. 또한 Rich한 UI,Slack/이메일 알림,실행 이력 추적,Backfill(과거 데이터 재처리) 기능 등이 뛰어나"운영 관점"에서도 우월합니다.

---

## 4. 비교 및 연결

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **기존 인프라** | 기존 Hadoop/HDFS 환경 → Oozie 自然스럽게 Integration | 신규 / Cloud 환경 → Airflow |
| **팀 기술 스택** | Java 중심 → Oozie XML (Java 태스크) | Python 중심 → Airflow (네이티브) |
| **통합 필요성** | Hadoop生態圈中心 → Oozie | Snowflake, BigQuery, Kafka 등 400+ → Airflow |
| **모니터링 요구** |基本监控足够 → Oozie | 상세 모니터링 + 알람 → Airflow |

*(추가 실무 적용 가이드 - Airflow 도입 Decision Tree)*
- **Airflow가 적합한 경우**: Python 기반 데이터 팀, Snowflake/BigQuery/Databricks 등 모던 데이터 플랫폼 활용, 상세 모니터링 필요, GitOps/CD/CD 요구
- **Oozie가 적합한 경우**: 기존 Hadoop/HDFS 환경에서 간단한 태스크 의존성 관리만 필요, 제한된 수의 태스크 (10개 이내), 이미 Oozie가 구축되어 있는 레거시 환경
- **대안 고려**: Prefect, Dagster, Temporal 등 모던 오케스트레이션 도구도 평가해볼 가치가 있습니다. 특히 Dagster는"데이터 파이프라인의 테스트와 문서화를 중요시하는团队"에 적합합니다.

---

## 5. 실무 적용 및 판단

1. **Airflow의 완전히 관리되는 서비스 확산**
   AWS MWAA (Managed Workflows for Apache Airflow), Astronomer Cloud, Google Cloud Composer 등 fully managed Airflow 서비스가 확산됨에 따라,"스케줄러/웹서버/Worker 관리"의 운영 부담이 크게 줄어들고 있습니다. 이는"Serverless Airflow"라는 개념으로 진화하며, 데이터 엔지니어가"오케스트레이션의 logic 설계"에만 집중할 수 있는 환경을 제공합니다.

2. **Dagster의 台頭: "엔지니어링 우선" 오케스트레이션**
   Prefect와 Dagster는 Airflow의"단점"(예: 테스트 어려움, 파이프라인과 외부 시스템의耦合,세밀한 리소스 격리 어려움)을 개선한"차세대" 오케스트레이션 도구로 떠오르고 있습니다. 특히 Dagster는"소스 코드 수준의 파이프라인 테스트", "타ипа卡片 기반 파이프라인 모니터링", "파이프라인과 스케줄러의 완벽한 분리"를 통해"엔지니어링 품질"을 한 단계 끌어올립니다.

3. **Temporal의崛起: 마이크로서비스 스타일의 워크플로우**
   Temporal은" طول 수명Workflow( Long-Running Workflow)"와"분산 트랜잭션"을 네이티브하게 지원하는新規念な 오케스트레이션 플랫폼으로,金融거래나 주문 처리처럼"여러 마이크로서비스가 참여하는 장기간の Workflow"에 적합합니다. 이는"단순한 데이터 ETL"을 넘어"비즈니스 프로세스 오케스트레이션"으로의 확장을 보여줍니다.

## 🧠 지식 맵 (Knowledge Graph)

*   **Apache Oozie核心组件**
    *   **Workflow**: DAG 기반 작업 순서 (XML 정의)
    *   **Coordinator**: 시간/데이터 기반 Workflow 트리거
    *   **Bundle**: 복수의 Coordinator 그룹化管理
    *   **Action**: 실제 실행할 태스크 (MapReduce, Spark, Hive, Shell等)
*   **Apache Airflow核心组件**
    *   **DAG**: Python으로 정의된 방향성 비순환 그래프
    *   **Operator**: 태스크 실행 단위 (Python, Bash, Snowflake, etc.)
    *   **Task**: Operator 실행 인스턴스
    *   **Executor**: 태스크 실행 방식 (Local, Celery, K8s)
    *   **XCom**: 태스크 간 데이터 공유 메커니즘
    *   **Connection**: 외부 시스템 연결 정보 관리
*   **Airflow vs alternatives**
    *   **Prefect**: Prefect Cloud + Orion 엔진, Python-첫
    *   **Dagster**: 테스트/문서화 특화, 파이프라인-스케줄러 분리
    *   **Temporal**: Long-running Workflow + 분산 트랜잭션

---

## 6. 기대효과 및 결론

Apache Oozie와 Airflow - 워크플로우 오케스트레이션의 진화은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 하둡 계열 기술의 가치는 개별 컴포넌트보다 저장·자원·처리 계층이 얼마나 안정적으로 결합되는가에 달려 있다.

---

## 7. 발전 흐름도

```text
[Apache Oozie]
    │
    ▼
[Apache Airflow]
    │
    ▼
[DAG (Directed Acyclic Graph)]
    │
    ▼
[Celery/Kubernetes Executor]
    │
    ▼
[Dagster / Prefect]
```

이 흐름도는 Apache Oozie에서 출발해 Dagster / Prefect까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| HDFS | 분산 저장 계층 |
| MapReduce·Spark | 분산 처리 엔진 연결점 |
| YARN | 클러스터 자원 관리 축 |
| Hive·HBase·Kafka | 하둡 생태계 확장 요소 |
