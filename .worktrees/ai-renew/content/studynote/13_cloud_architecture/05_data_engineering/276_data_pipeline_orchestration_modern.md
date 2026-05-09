+++
weight = 276
title = "276. 데이터 파이프라인 오케스트레이션 - Airflow, Prefect, Dagster"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 파이프라인 오케스트레이터는 복잡한 의존성을 가진 데이터 작업들의 실행 순서, 스케줄, 재시도, 모니터링을 코드 기반 DAG(방향성 비순환 그래프)로 정의하고 관리하는 워크플로우 관리 시스템이다.
> 2. **가치**: 수십~수백 개의 ETL 작업이 얽혀있는 파이프라인에서 "어떤 작업이 왜 실패했는가?", "어제 실패한 구간만 재실행(Backfill)하려면?"의 질문에 코드 기반으로 안전하게 답한다.
> 3. **판단 포인트**: Airflow(스케줄 기반, 성숙한 생태계) vs Prefect(Python 친화적, 동적 워크플로우) vs Dagster(에셋 중심, 데이터 인식 오케스트레이션) — 팀의 기술 수준과 파이프라인 복잡도에 따라 선택.

---

## Ⅰ. 개요 및 필요성

Cron 작업으로 데이터 파이프라인을 관리하면: 한 작업이 실패해도 다음 작업이 실행되어 오류가 전파되고, 실패 이유를 파악하려면 각 서버의 로그를 직접 조회해야 한다. 재실행은 수작업으로.

**파이프라인 오케스트레이터**는 이 문제를 해결한다:
- 의존성 기반 실행 순서 자동 결정
- 실패 시 자동 재시도 및 알림
- 중앙 집중식 로그 및 모니터링
- Backfill(과거 구간 재실행) 지원

```
[복잡한 파이프라인 의존성 DAG]

ingest_raw_data
      │
      ├──▶ validate_schema ──▶ transform_orders ──▶ load_dw
      │                                               │
      └──▶ validate_completeness                      ▼
                                            aggregate_daily_sales
                                                      │
                                                      ▼
                                             update_dashboard
```

📢 **섹션 요약 비유**: 오케스트레이터는 공사 현장 소장이다. "기초 공사 완료 후 벽을 세우고, 벽 완료 후 지붕을 올린다"는 순서를 관리하고, 각 공정을 누가 언제 했는지 기록하며, 문제 발생 시 해당 공정만 재시공한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Apache Airflow DAG 예시

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "data-team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["data-alerts@company.com"]
}

with DAG(
    "daily_etl_pipeline",
    schedule_interval="0 6 * * *",  # 매일 오전 6시
    start_date=datetime(2024, 1, 1),
    catchup=True,  # Backfill 허용
    default_args=default_args
) as dag:

    extract = PythonOperator(
        task_id="extract_from_source",
        python_callable=extract_data,
        op_kwargs={"date": "{{ ds }}"}  # 실행 날짜 템플릿
    )

    validate = PythonOperator(
        task_id="validate_schema",
        python_callable=validate_data
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data
    )

    load = BashOperator(
        task_id="load_to_dw",
        bash_command="dbt run --select orders --vars '{date: {{ ds }}}'"
    )

    # 의존성 정의
    extract >> validate >> transform >> load
```

### Airflow vs Prefect vs Dagster 비교

| 항목 | Airflow | Prefect | Dagster |
|:---|:---|:---|:---|
| **설계 철학** | DAG 스케줄러 | Python-first 워크플로우 | 에셋 중심 오케스트레이션 |
| **동적 워크플로우** | 제한적 | ✅ 런타임 동적 | ✅ 에셋 의존성 |
| **로컬 개발** | 어려움 | 쉬움 | 쉬움 |
| **에셋 추적** | 없음 | 제한적 | ✅ 핵심 기능 |
| **성숙도** | 높음 (2015~) | 중간 | 성장 중 |
| **관리형 서비스** | MWAA (AWS), Cloud Composer | Prefect Cloud | Dagster Cloud |

### 이벤트 기반 vs 스케줄 기반

```
스케줄 기반 (Airflow 기본):
  매일 오전 6시 실행 (고정 일정)
  → 데이터가 준비되지 않아도 실행될 수 있음
  → 간단하지만 데이터 준비 상태와 무관

이벤트 기반 (Prefect/Dagster):
  S3에 새 파일 도착 → 파이프라인 트리거
  Kafka 메시지 수신 → 처리 시작
  → 데이터 준비 시 즉시 처리 (더 반응적)
  → 더 복잡한 트리거 설정 필요
```

📢 **섹션 요약 비유**: 스케줄 기반은 알람 시계다. 몇 시든 울리도록 맞춰두면 무조건 일어나야 한다. 이벤트 기반은 문 열림 감지기다. 손님이 도착했을 때만 반응한다. 손님(데이터)이 언제 올지 모를 때는 감지기가 더 효율적이다.

---

## Ⅲ. 비교 및 연결

### Backfill 전략

```
[Backfill 시나리오]

상황: 2024-01-10~2024-01-15 파이프라인 실패
     2024-01-15 이후 정상 운영 중

Airflow Backfill:
airflow dags backfill \
    --start-date 2024-01-10 \
    --end-date 2024-01-15 \
    daily_etl_pipeline

→ 누락 구간을 자동으로 순서에 맞게 재실행
→ 이미 성공한 날짜는 건너뜀 (catchup=True 필요)
```

### 파이프라인 모니터링 지표

| 지표 | 설명 | 알림 기준 |
|:---|:---|:---|
| 실행 지연 시간 | 예상 완료 시간 초과 | SLA 기준 10% 초과 |
| 실패율 | 전체 태스크 중 실패 비율 | 5% 초과 |
| 재시도 횟수 | 성공까지 재시도 수 | 2회 이상 |
| 데이터 신선도 | 최신 데이터가 얼마나 오래됐는지 | 2시간 이상 |

📢 **섹션 요약 비유**: Backfill은 결석한 날의 수업을 따라잡는 것이다. 1월 10일~15일에 결석했다면, 그 기간의 수업 내용을 순서대로 따라잡아야 한다. 이미 들은 날짜는 다시 들을 필요 없다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Dagster 에셋 중심 오케스트레이션

```python
# Dagster: 데이터 에셋 정의
from dagster import asset, AssetIn

@asset
def raw_orders(context):
    """원본 주문 데이터 수집"""
    return extract_from_source()

@asset(ins={"raw_orders": AssetIn()})
def validated_orders(raw_orders):
    """스키마 검증된 주문 데이터"""
    assert raw_orders["amount"].notna().all()
    return raw_orders

@asset(ins={"validated_orders": AssetIn()})
def daily_revenue(validated_orders):
    """일별 매출 집계"""
    return validated_orders.groupby("date")["amount"].sum()
```

### 대규모 파이프라인 운영 아키텍처

```
[프로덕션 Airflow 아키텍처]

                [Web Server] (UI)
                      │
              [Scheduler] (DAG 스케줄링)
                      │
              [Message Broker] (Celery/Kafka)
               /      │      \
          [Worker1] [Worker2] [Worker3]  (태스크 실행)
               \      │      /
              [Metadata DB] (PostgreSQL)
              (실행 이력, 상태 저장)
```

### 기술사 시험 판단 포인트

- **DAG의 핵심**: 방향성 비순환 그래프 — 순환 참조 없이 단방향 의존성으로 실행 순서 결정
- **Idempotent(멱등성)**: 파이프라인 태스크는 여러 번 실행해도 동일한 결과를 보장해야 Backfill 안전
- **Airflow 선택 기준**: 수동 트리거보다 스케줄 기반, 복잡한 의존성, 성숙한 생태계 필요 시

📢 **섹션 요약 비유**: 멱등성 태스크는 복사기 같다. 같은 원본을 몇 번 복사해도 결과는 항상 동일한 복사본이다. 데이터 파이프라인도 마찬가지로, Backfill로 같은 날짜를 여러 번 재실행해도 항상 같은 결과가 나와야 한다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 영역 | 효과 |
|:---|:---|
| **가시성** | 파이프라인 실행 상태 중앙 집중 모니터링 |
| **신뢰성** | 자동 재시도, 알림으로 데이터 신선도 보장 |
| **생산성** | 코드 기반 파이프라인 정의로 재사용성 향상 |
| **운영성** | Backfill, 선택적 재실행으로 장애 복구 용이 |

### 한계 및 주의사항

- **Airflow 운영 복잡성**: Worker, Scheduler, WebServer, MetaDB 다중 컴포넌트 관리
- **동적 파이프라인 한계**: Airflow는 DAG 구조를 실행 전에 알아야 함 — 런타임 동적 생성 어려움
- **테스트 어려움**: 데이터 파이프라인 단위 테스트가 일반 소프트웨어보다 복잡
- **도구 교체 비용**: Airflow에서 Dagster/Prefect 마이그레이션은 상당한 리팩토링 필요

📢 **섹션 요약 비유**: Airflow는 회사의 레거시 ERP와 같다. 너무 많은 곳에 퍼져 있어서 교체가 어렵지만, 최신 도구들이 그 틈새를 파고들고 있다. 새로운 파이프라인을 만든다면 Prefect나 Dagster를 검토하고, 기존 Airflow가 있다면 점진적으로 마이그레이션하는 것이 현실적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| DAG | 오케스트레이터의 파이프라인 정의 구조 |
| Backfill | 과거 구간 재처리 - 오케스트레이터의 핵심 기능 |
| dbt | SQL 변환 도구, Airflow와 통합하여 변환 단계 관리 |
| 이벤트 기반 파이프라인 | Kafka/S3 이벤트로 파이프라인 트리거 |
| 데이터 품질 게이트 | 오케스트레이터 내에서 GE 검증 단계 통합 |
| MLOps 파이프라인 | ML 훈련 파이프라인도 Airflow/Kubeflow로 오케스트레이션 |

### 👶 어린이를 위한 3줄 비유 설명
1. 파이프라인 오케스트레이터는 도미노 쓰러뜨리기 설계자야. "이 조각이 쓰러진 다음에야 저 조각이 쓰러진다"는 순서를 미리 설계해둬.
2. 중간에 조각이 쓰러지지 않으면(실패) 자동으로 다시 세워서 시도하고(재시도), 안 되면 알림을 줘.
3. Backfill은 지난주에 도미노가 중간에 멈춰서 못 쓰러뜨린 조각들을, 오늘 다시 처음부터 순서대로 쓰러뜨리는 거야!
