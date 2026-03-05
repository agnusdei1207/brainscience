+++
title = "DataOps (데이터 운영)"
description = "데이터 파이프라인의 개발과 운영을 DevOps 원칙으로 자동화하여 데이터 품질, 신뢰성, 민첩성을 보장하는 협업 방법론"
date = 2024-05-15
[taxonomies]
tags = ["DataOps", "Data-Pipeline", "DevOps", "ETL", "Data-Quality", "Automation"]
+++

# DataOps (데이터 운영)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 엔지니어링, 데이터 사이언스, 데이터 분석의 **전체 수명 주기(수집-변환-품질 검증-배포-모니터링)에 DevOps 원칙(자동화, CI/CD, 버전 관리, 협업)**을 적용하여 데이터 파이프라인의 민첩성과 신뢰성을 극대화하는 방법론입니다.
> 2. **가치**: 데이터 품질 문제를 조기에 감지하고, 파이프라인 변경을 안전하게 배포하며, 데이터 소비자(분석가, AI 모델)에게 **"Always Fresh, Always Correct"** 데이터를 제공하여 데이터 기반 의사결정의 신뢰도를 높입니다.
> 3. **융합**: MLOps(ML 파이프라인), IaC(Terraform), 오케스트레이션(Airflow/Dagster), 데이터 품질(Great Expectations), 데이터 카탈로그와 결합하여 현대적 데이터 플랫폼을 구축합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**DataOps(Data Operations)**는 데이터 파이프라인의 **개발, 테스트, 배포, 운영에 DevOps 실천법을 적용**하는 협업 방법론입니다. 2014년 Lenny Liebmann이 처음 제안하고, 2018년 DataKitchen의 Christopher Bergh가 정립했습니다. 핵심 원칙:
- **자동화(Automation)**: ETL/ELT 파이프라인 CI/CD
- **품질 검증(Quality Gates)**: 데이터 품질 테스트 자동화
- **버전 관리(Version Control)**: SQL, 스키마, 설정의 Git 관리
- **모니터링(Observability)**: 파이프라인 상태 및 데이터 드리프트 감지
- **협업(Collaboration)**: 데이터 팀과 비즈니스 팀 간 커뮤니케이션

### 2. 구체적인 일상생활 비유
식당의 **주방 파이프라인**을 상상해 보세요. 재료 수령 -> 세척 -> 손질 -> 조리 -> 플레이팅 -> 서빙. 전통적 방식은 요리사가 각 단계를 수동으로 확인합니다. **DataOps**는 자동화된 주방입니다. 재료가 들어오면 자동으로 신선도 검사, 세척 기계, 조리 로봇, 플레이팅 머신, 서빙 컨베이어가 작동합니다. 문제가 생기면 즉시 알람이 울립니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (데이터 파이프라인의 취약성)**:
   데이터 파이프라인은 "깨지기 쉽습니다(Fragile)". 소스 시스템 스키마 변경, 데이터 형식 변화, 네트워크 장애 등으로 인해 매일 실패합니다. 그러나 데이터 엔지니어링은 DevOps 없는 "개발은 개발, 운영은 운영" 상태였습니다.

2. **혁신적 패러다임 변화의 시작**:
   2010년대 후반 Airflow, dbt, Spark가 대중화되면서 "데이터 파이프라인도 코드다"라는 인식이 확산. SQL, Python으로 작성된 파이프라인도 버전 관리하고 테스트하고 CI/CD로 배포해야 한다는 DataOps 철학이 정착되었습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   데이터 기반 의사결정, AI/ML 모델 훈련, 실시간 대시보드를 위해서는 **신뢰할 수 있는 데이터**가 필수입니다. "잘못된 데이터로 잘못된 결정"을 하는 것을 방지하기 위해 DataOps는 선택이 아닌 필수입니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 관련 도구/기술 |
| :--- | :--- | :--- | :--- |
| **Orchestrator** | 파이프라인 스케줄링 및 실행 | DAG(Directed Acyclic Graph) 기반 태스크 관리 | Airflow, Dagster, Prefect |
| **Transform Engine** | 데이터 변환(ETL/ELT) | SQL 실행, Spark Job 제출 | dbt, Spark, Flink |
| **Data Quality** | 데이터 품질 검증 | 스키마 검증, 통계적 테스트 | Great Expectations, dbt tests |
| **Version Control** | 코드 및 스키마 버전 관리 | Git, 마이그레이션 관리 | Git, Liquibase |
| **CI/CD Pipeline** | 파이프라인 변경 배포 | 테스트 -> 스테이징 -> 프로덕션 | GitHub Actions, Jenkins |
| **Observability** | 파이프라인 모니터링 | 메트릭, 로그, 알람 | Datadog, Monte Carlo |

### 2. 정교한 구조 다이어그램: DataOps 파이프라인

```text
=====================================================================================================
                      [ DataOps End-to-End Pipeline Architecture ]
=====================================================================================================

  [ Data Sources ]             [ DataOps Platform ]              [ Data Consumers ]
       |                            |                                   |
       v                            v                                   v

+------------------+       +----------------------------------+      +------------------+
| Source Systems   |       | 1. INGESTION LAYER               |      | Analytics        |
| - PostgreSQL DB  | ----> | +----------+ +----------+        |      | - Dashboards     |
| - API Endpoints  |       | | Airbyte  | | Fivetran |        |      | - Reports        |
| - S3/GCS Buckets |       | +----------+ +----------+        |      +--------+---------+
| - Kafka Streams  |       |         |                        |               |
+------------------+       |         v                        |               |
                           | +---------------------------+    |               |
                           | | Data Lake (Raw Zone)      |    |               |
                           | | - S3/GCS                  |    |               |
                           | | - Parquet/Delta Format    |    |               |
                           | +------------+--------------+    |               |
                           |              |                   |               |
                           |              v                   |               |
                           | +--------------------------------+ |               |
                           | | 2. TRANSFORMATION LAYER (dbt) | |               |
                           | | +----------+ +----------+     | |               |
                           | | | Staging  | | Mart     |     | |               |
                           | | | Models   | | Models   |     | |               |
                           | | +----------+ +----------+     | |               |
                           | |                              | |               |
                           | | 3. QUALITY GATES             | |               |
                           | | +--------------------------+ | |               |
                           | | | Great Expectations       | | |               |
                           | | | - Schema Validation      | | |               |
                           | | | - Freshness Check        | | |               |
                           | | | - Volume Anomaly         | | |               |
                           | | +--------------------------+ | |               |
                           | +-------------+----------------+ |               |
                           |               |                  |               |
                           |               v                  |               |
                           | +--------------------------------+ |               |
                           | | 4. DATA WAREHOUSE             | |               |
                           | | - Snowflake / BigQuery        | |               |
                           | | - dbt-generated tables        | |               |
                           | +----------------+---------------+ |               |
                           |                  |                 |               |
                           +------------------+-----------------+               |
                                              |                                 |
                                              v                                 v
                           +----------------------------------+      +------------------+
                           | 5. ORCHESTRATION (Airflow)       | ---> | ML Platform      |
                           | +-------------------------------+|      | - Feature Store  |
                           | | DAG: daily_etl_pipeline       ||      | - Model Training |
                           | |  - extract_source_data        ||      +------------------+
                           | |  - run_dbt_transformations    ||
                           | |  - run_data_quality_tests     ||
                           | |  - notify_on_failure          ||
                           | +-------------------------------+|
                           +----------------------------------+

=====================================================================================================

                      [ DataOps CI/CD Pipeline ]
=====================================================================================================

  Developer                    CI Server                     Production
  Workstation                                                Environment
       |                           |                               |
       | 1. git push               |                               |
       v                           v                               v

+----------------+        +------------------+         +------------------+
| Feature Branch | -----> | 2. CI Pipeline   |         | Prod Environment |
| - models/*.sql |        | +--------------+ |         | - Airflow DAGs   |
| - tests/*.sql  |        | | Lint SQL     | |         | - dbt Models     |
+----------------+        | | dbt compile  | |         | - Data Quality   |
                          | | dbt test     | |         +--------+---------+
                          | | Great        | |                  ^
                          | | Expectations | |                  |
                          | +------+-------+ |                  |
                          |        |         |                  |
                          |        v         |                  |
                          | +--------------+ |                  |
                          | | 3. Deploy to | |                  |
                          | | Staging      | |                  |
                          | +------+-------+ |                  |
                          |        |         |                  |
                          |        v         |                  |
                          | +--------------+ |                  |
                          | | 4. Run Full  | |                  |
                          | | E2E Tests    | |                  |
                          | +------+-------+ |                  |
                          |        |         |                  |
                          |        v         |                  |
                          | +--------------+ |                  |
                          | | 5. PR Review | |                  |
                          | | & Approval   | |                  |
                          | +------+-------+ |                  |
                          +--------|---------+                  |
                                   |                            |
                                   | 6. Merge to main           |
                                   +----------------------------+
                                           |
                                           v
                                   +------------------+
                                   | 7. CD Pipeline   |
                                   | - Deploy to Prod |
                                   +------------------+

=====================================================================================================
```

### 3. 핵심 알고리즘 및 실무 코드 예시

**dbt(Data Build Tool) 모델 및 테스트**

```sql
-- models/staging/stg_orders.sql
with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_status,
        -- Convert timestamp to date
        cast(order_timestamp as date) as order_date,
        -- Calculate order value in USD
        order_value / 100.0 as order_value_usd,
        -- Metadata
        {{ dbt_utils.generate_surrogate_key(['order_id']) }} as order_key,
        current_timestamp as loaded_at
    from source
    where order_timestamp >= '{{ var("start_date") }}'
)

select * from renamed
```

```yaml
# models/staging/schema.yml (Data Tests)
version: 2

models:
  - name: stg_orders
    description: "Cleansed and renamed orders data"
    columns:
      - name: order_id
        description: "Primary key"
        tests:
          - unique
          - not_null

      - name: customer_id
        description: "Foreign key to customers"
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id

      - name: order_status
        description: "Current status of the order"
        tests:
          - accepted_values:
              values: ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

      - name: order_value_usd
        description: "Order value in USD"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 100000  # Sanity check

# Custom data quality test
tests:
  - name: assert_order_freshness
    description: "Ensure orders are not older than 24 hours"
    query: |
      select count(*) as stale_orders
      from {{ ref('stg_orders') }}
      where order_date < current_date - interval '24 hours'
    assertions:
      - stale_orders == 0
```

**Airflow DAG (DataOps Orchestration)**

```python
# dags/daily_etl_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.dbt.operators.dbt import DbtRunOperator, DbtTestOperator
from airflow.providers.slack.operators.slack import SlackAPIOperator
from datetime import datetime, timedelta
import great_expectations as gx

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['data-team@company.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_etl_pipeline',
    default_args=default_args,
    description='DataOps daily ETL with quality gates',
    schedule_interval='0 6 * * *',  # 6 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['dataops', 'etl', 'production'],
) as dag:

    # Task 1: Run dbt transformations
    dbt_run = DbtRunOperator(
        task_id='dbt_run',
        dbt_project_path='/opt/airflow/dags/dbt_project',
        profiles_dir='/opt/airflow/dags/dbt_project',
    )

    # Task 2: Run dbt tests (data quality)
    dbt_test = DbtTestOperator(
        task_id='dbt_test',
        dbt_project_path='/opt/airflow/dags/dbt_project',
    )

    # Task 3: Great Expectations validation
    def run_great_expectations():
        context = gx.get_context()
        suite = context.get_expectation_suite("orders_suite")
        batch_request = {
            "datasource_name": "warehouse",
            "data_connector_name": "default",
            "data_asset_name": "orders",
        }
        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite=suite
        )
        results = validator.validate()
        if not results.success:
            raise Exception(f"Data quality check failed: {results.statistics}")

    ge_validation = PythonOperator(
        task_id='great_expectations_validation',
        python_callable=run_great_expectations,
    )

    # Task 4: Data freshness check
    def check_data_freshness():
        import snowflake.connector
        conn = snowflake.connector.connect(...)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MAX(loaded_at) as latest_load
            FROM analytics.fact_orders
        """)
        result = cursor.fetchone()
        freshness_hours = (datetime.now() - result[0]).total_seconds() / 3600
        if freshness_hours > 24:
            raise Exception(f"Data is stale: {freshness_hours} hours old")
        print(f"Data freshness: {freshness_hours} hours")

    freshness_check = PythonOperator(
        task_id='data_freshness_check',
        python_callable=check_data_freshness,
    )

    # Task 5: Notify on success
    notify_success = SlackAPIOperator(
        task_id='notify_success',
        slack_conn_id='slack_default',
        channel='#data-alerts',
        text='Daily ETL pipeline completed successfully!',
    )

    # Task dependencies
    dbt_run >> dbt_test >> ge_validation >> freshness_check >> notify_success
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 데이터 오케스트레이션 도구 비교

| 평가 지표 | Apache Airflow | Dagster | Prefect | Luigi |
| :--- | :--- | :--- | :--- | :--- |
| **프로그래밍** | Python | Python | Python | Python |
| **DAG 정의** | 코드 기반 | 코드 + 선언적 | 코드 + 데코레이터 | 코드 |
| **데이터 자산** | 수동 | 자동 추적 | 자동 | 수동 |
| **테스트** | 어려움 | 용이함 | 용이함 | 어려움 |
| **UI** | 강력함 | 현대적 | 현대적 | 기본적 |
| **학습 곡선** | 높음 | 중간 | 낮음 | 낮음 |
| **시장 점유율** | 1위 | 성장 중 | 성장 중 | 감소 중 |

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 데이터 파이프라인 장애 복구**
- **문제점**: 어제 밤 ETL 파이프라인이 실패해서 대시보드 데이터가 갱신되지 않았습니다.
- **기술사 판단 (전략)**: DataOps 모니터링으로 실패 지점 식별. Airflow UI에서 실패한 태스크 재실행. dbt incremental 모델로 전체 재실행 없이 복구.

**[상황 B] 데이터 스키마 변경 배포**
- **문제점**: 신규 컬럼 추가로 인해 기존 파이프라인이 깨질 수 있습니다.
- **기술사 판단 (전략)**: DataOps CI/CD로 staging 환경에서 테스트 후 배포. dbt 스키마 테스트로 호환성 검증. Blue-Green 배포로 무중단 전환.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 수동 데이터 운영 (AS-IS) | DataOps 적용 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **파이프라인 실패 감지** | 수 시간~수 일 | 실시간 | **감지 속도 99% 향상** |
| **데이터 품질 이슈** | 빈번 | 드묾 | **품질 80% 향상** |
| **변경 배포 시간** | 주 단위 | 시간 단위 | **배포 속도 10배** |
| **데이터 신뢰도** | 낮음 | 높음 | **의사결정 신뢰성 향상** |

### 2. 참고 표준/가이드
- **DataOps Manifesto**: DataOps 원칙 선언
- **Data Management Body of Knowledge (DMBOK)**: 데이터 관리 표준

---

## 관련 개념 맵 (Knowledge Graph)
- **[MLOps](@/studynotes/15_devops_sre/1_sre/48_mlops.md)**: DataOps가 데이터를 제공하는 ML 운영
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/3_automation/continuous_integration.md)**: DataOps의 자동화 기반
- **[Airflow](@/studynotes/15_devops_sre/1_sre/55_workflow_orchestrator.md)**: DataOps 오케스트레이션 도구
- **[데이터 품질](@/studynotes/8_database/1_rdbms/data_quality.md)**: DataOps의 핵심 목표
- **[ETL/ELT](@/studynotes/8_database/1_rdbms/etl_elt.md)**: 데이터 변환 프로세스

---

## 어린이를 위한 3줄 비유 설명
1. 요리사가 **매일 아침 식재료를 받아서 요리**해요. 근데 식재료가 상했는지, 양이 맞는지 확인하는 게 힘들죠.
2. DataOps는 **자동 검사 기계**예요. 식재료가 들어오면 신선도, 양, 품질을 자동으로 검사해요!
3. 덕분에 요리사는 요리만 하면 돼요. 나쁜 식재료는 기계가 걸러주니까 손님은 항상 맛있는 요리를 먹어요!
