+++
weight = 319
title = "319. 데이터 파이프라인 오케스트레이터 Airflow DAG (Airflow DAG Pipeline)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Airflow DAG (Directed Acyclic Graph)는 데이터 파이프라인을 코드로 정의하고, 의존성을 방향성 비순환 그래프로 표현해 스케줄·모니터링·재실행을 자동화한다.
> 2. **가치**: CeleryExecutor나 KubernetesExecutor로 수천 개의 태스크를 병렬 실행하고, SLA Miss 알람과 Backfill로 데이터 신뢰성을 운영 수준에서 보장한다.
> 3. **판단 포인트**: Airflow는 스케줄 기반 배치 오케스트레이션에 강하지만, 실시간 스트리밍 파이프라인은 Kafka/Flink가 적합하며 두 도구는 상호 보완 관계다.

## Ⅰ. 개요 및 필요성

데이터 파이프라인은 수십~수백 개의 태스크(ETL, 데이터 품질 검사, ML 학습, 리포트 생성)가 특정 순서와 조건으로 실행되어야 한다.
수작업 스크립트로 관리하면 의존성 파악 불가, 실패 시 재실행 어려움, 스케줄 충돌 등의 문제가 발생한다.

Airflow (Apache Airflow, Airbnb 개발)는 Python으로 DAG를 정의해:
- 태스크 간 의존성을 `>>` 연산자로 선언
- 스케줄을 cron 표현식으로 정의 (`0 2 * * *` = 매일 새벽 2시)
- Web UI에서 실행 현황·로그·재실행을 시각적으로 관리

주요 개념:
- **DAG**: Directed Acyclic Graph, 파이프라인 전체 정의
- **Task**: 개별 작업 단위 (Operator로 구현)
- **Operator**: PythonOperator, BashOperator, SparkSubmitOperator 등
- **Sensor**: 외부 조건 대기 (S3FileSensor, ExternalTaskSensor)

📢 **섹션 요약 비유**: Airflow DAG는 복잡한 공사 공정표다. 어떤 공정이 먼저 끝나야 다음 공정을 시작할 수 있는지, 언제 시작할지를 모두 코드로 관리한다.

## Ⅱ. 아키텍처 및 핵심 원리

### Executor 유형 비교

| Executor | 특징 | 병렬성 | 사용 환경 |
|:---|:---|:---|:---|
| LocalExecutor | 단일 서버 프로세스 병렬 | 수십 태스크 | 개발, 소규모 |
| CeleryExecutor | Redis/RabbitMQ 큐 기반 분산 | 수백 태스크 | 중형 프로덕션 |
| KubernetesExecutor | 태스크당 Pod 생성 | 수천 태스크 | 클라우드 네이티브 |

### XCom (Cross-Communication)

태스크 간 데이터 전달:
```python
# 업스트림 태스크가 값 push
def extract_data(**context):
    result = {"row_count": 1000}
    context['task_instance'].xcom_push(key='result', value=result)

# 다운스트림 태스크가 값 pull
def validate_data(**context):
    result = context['task_instance'].xcom_pull(
        task_ids='extract_task', key='result'
    )
    assert result['row_count'] > 0
```

주의: XCom은 소규모 메타데이터용 (대용량 데이터는 S3에 저장 후 경로 전달)

### ASCII 다이어그램: DAG 태스크 의존성 그래프

```
  DAG: daily_etl_pipeline  (cron: 0 2 * * *)
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  [extract_raw_data]                                         │
  │         │                                                   │
  │         ▼                                                   │
  │  [validate_schema] ──── [check_row_count]                   │
  │         │                       │                           │
  │         └───────────┬───────────┘                           │
  │                     ▼                                       │
  │           [transform_to_staging]                            │
  │                     │                                       │
  │          ┌──────────┼──────────┐                            │
  │          ▼          ▼          ▼                            │
  │    [load_dim_A] [load_dim_B] [load_dim_C]                   │
  │          │          │          │                            │
  │          └──────────┼──────────┘                            │
  │                     ▼                                       │
  │              [build_fact_table]                             │
  │                     │                                       │
  │                     ▼                                       │
  │              [refresh_BI_cache]                             │
  │                     │                                       │
  │                     ▼                                       │
  │              [send_completion_alert]                        │
  └─────────────────────────────────────────────────────────────┘
```

### Backfill과 Catchup

```bash
# 과거 날짜 데이터 소급 실행
airflow dags backfill -s 2024-01-01 -e 2024-01-31 my_dag

# Catchup: DAG 비활성화 기간 동안의 실행을 재처리 (기본 True)
# 프로덕션에서는 catchup=False 권장 (의도치 않은 대량 실행 방지)
```

📢 **섹션 요약 비유**: DAG 의존성은 도미노 게임이다. 앞 도미노(태스크)가 넘어져야 다음 도미노가 넘어지고, 어느 하나가 넘어지지 않으면 뒤도 멈춘다.

## Ⅲ. 비교 및 연결

### 오케스트레이터 비교

| 항목 | Airflow | Prefect | Dagster | Luigi |
|:---|:---|:---|:---|:---|
| 스케줄링 | 강력 (cron, sensor) | 강력 | 강력 | 제한적 |
| UI | 성숙 | 현대적 | 현대적 | 기본 |
| 코드 방식 | Python DAG (선언적) | Python Flow | Python Job | Python Task |
| 데이터 관측성 | 제한 (로그 중심) | 강함 | 매우 강함 | 없음 |
| 클라우드 관리형 | Astronomer, MWAA | Prefect Cloud | Dagster Cloud | - |

📢 **섹션 요약 비유**: Airflow는 믿을 수 있는 베테랑 공정 관리자다. Dagster와 Prefect는 현대적 UI와 관측성을 강조하는 신입이다.

## Ⅳ. 실무 적용 및 기술사 판단

### Airflow 운영 체크리스트

- [ ] DAG 파일 Git 버전 관리 (DAG 변경 이력 추적)
- [ ] SLA Miss 알람 설정: `sla=timedelta(hours=2)` 태스크 단위
- [ ] KubernetesExecutor 사용 시 태스크별 리소스 제한 (CPU, 메모리)
- [ ] catchup=False 설정 (재활성화 시 대량 소급 실행 방지)
- [ ] DB 연결 풀 관리: Worker 수 × 평균 병렬 태스크 × 커넥션 = 커넥션 풀 크기

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| DAG 내 무거운 Python 코드 직접 실행 | Scheduler 스레드 블로킹 | SparkSubmitOperator 또는 K8s Pod 위임 |
| XCom으로 대용량 데이터 전달 | Metadata DB 용량 폭발 | S3 경로만 XCom으로 전달 |
| 모든 태스크에 동일 retry=3 | 지연 3배 증가 | 태스크별 retry 전략 다르게 |
| MAX_ACTIVE_RUNS 무제한 | DAG 중복 실행, DB 과부하 | max_active_runs=1~3 제한 |

📢 **섹션 요약 비유**: DAG 내 무거운 작업 직접 실행은 지휘자(Scheduler)가 직접 악기를 연주하는 것이다. 지휘자는 지휘만 해야 한다.

## Ⅴ. 기대효과 및 결론

| 항목 | 수작업 스크립트 | Airflow DAG |
|:---|:---|:---|
| 파이프라인 가시성 | 없음 (로그만) | Web UI 전체 상태 시각화 |
| 실패 시 재실행 | 수동 (어떤 태스크부터?) | 실패 태스크부터 자동 재실행 |
| SLA 모니터링 | 없음 | SLA Miss 자동 알람 |
| 백필 (소급 실행) | 스크립트 수동 수정 | `airflow dags backfill` 한 줄 |

📢 **섹션 요약 비유**: Airflow는 공항 관제탑이다. 모든 항공편(태스크)의 출발·도착을 실시간으로 모니터링하고, 지연이 생기면 즉시 알려준다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DAG | 핵심 구조 | 방향성 비순환 그래프 파이프라인 |
| Operator | 태스크 구현체 | Python/Bash/Spark/S3 등 |
| Sensor | 대기 태스크 | 외부 조건 충족까지 폴링 |
| XCom | 데이터 전달 | 태스크 간 소규모 데이터 공유 |
| Executor | 실행 엔진 | Local/Celery/Kubernetes |
| Backfill | 소급 실행 | 과거 날짜 데이터 재처리 |

### 👶 어린이를 위한 3줄 비유 설명

1. Airflow DAG는 청소 순서표예요. "방 청소가 끝나야 욕실 청소를 시작할 수 있어요"처럼 순서가 정해져 있어요.
2. Operator는 각 청소 도구예요. 진공청소기(PythonOperator), 걸레(BashOperator), 소독약(SparkOperator) 등이 있어요.
3. SLA Miss 알람은 "약속한 시간까지 청소를 못 끝냈어요!"라고 알려주는 타이머예요.
