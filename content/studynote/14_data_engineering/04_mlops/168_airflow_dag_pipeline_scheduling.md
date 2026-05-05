+++
weight = 168
title = "168. 데이터 파이프라인 워크플로우 DAG 제어 (Apache Airflow) 자동화"
date = "2026-05-05"
[extra]
categories = "studynote-data-engineering"
+++

## 0. 핵심 인사이트

> **핵심**: Apache Airflow는 파이썬 코드로 워크플로우를 DAG (Directed Acyclic Graph, 방향성 비순환 그래프)로 정의하고, 스케줄러가 이를 자동 실행·모니터링하는 오픈소스 오케스트레이션 플랫폼이다.
> **비유**: 여러 공정이 연결된 생산 라인처럼, 앞단의 입력 품질과 중간 단계의 흐름 제어가 최종 결과를 좌우하는 구조와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

**Apache Airflow**는 Airbnb가 2014년에 개발하고 2019년 Apache Top Level Project가 된 파이썬 기반 워크플로우 오케스트레이션 플랫폼이다. 데이터 파이프라인의 작업 의존성을 DAG (Directed Acyclic Graph, 방향성 비순환 그래프)로 표현하고 스케줄에 따라 자동 실행한다.

```
Airflow 없는 세상 (문제 상황)
┌────────────────────────────────────────────────────────┐
│  스크립트 A (00:00 실행)                                │
│  스크립트 B (01:00 실행)  ← A 완료 확인을 어떻게?      │
│  스크립트 C (02:00 실행)  ← B 실패 시 C는?             │
│  → 크론탭(crontab)으로 시간 기반 실행                  │
│  → 의존성 관리 없음, 실패 재시도 없음                  │
│  → 파이프라인 현황 가시성 없음                          │
└────────────────────────────────────────────────────────┘

Airflow 도입 후
┌────────────────────────────────────────────────────────┐
│  DAG: etl_pipeline                                     │
│  extract_task → transform_task → load_task             │
│                    ↓ (실패 시)                          │
│                 자동 재시도 3회                         │
│                 → 알람 발송                            │
│  Web UI로 실시간 현황 모니터링                          │
└────────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

| 요소 | 역할 | 핵심 포인트 |
|:---|:---|:---|
| 핵심 대상 | 해당 주제가 직접 다루는 데이터·모델·인프라의 중심 객체 | 무엇을 저장·처리·최적화하는지가 기술의 경계를 결정한다 |
| 제어 메커니즘 | 처리 순서, 규칙, 알고리즘, 오케스트레이션 | 성능·정합성·확장성은 제어 방식에 따라 달라진다 |
| 운영 레이어 | 모니터링, 품질 검증, 거버넌스, 비용 관리 | 실무에서는 기능보다 운영 가능성이 채택 여부를 좌우한다 |

```
DAG = 방향성(Directed) + 비순환(Acyclic) + 그래프(Graph)

방향성: 작업 A → 작업 B (A가 끝나야 B 시작)
비순환: A → B → C → A 같은 순환 불가 (무한 루프 방지)

예시 DAG:
extract_data
     │
     ├──→ validate_data ──→ load_to_staging
     │                              │
     └──→ profile_data             │
                                   ▼
                           run_dbt_models
                                   │
                           ┌───────┴────────┐
                           ▼               ▼
                    build_marts      send_report
```

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 파이프라인 워크플로우 DAG 제어 (Apache Airflow) 자동화은 입력 데이터의 품질, 처리 단계의 일관성, 결과 활용 단계의 운영 제어가 동시에 맞아야 기대 효과를 낸다.

| 항목 | Airflow | Luigi | Prefect | Dagster |
|:---|:---|:---|:---|:---|
| **개발사** | Apache/Airbnb | Spotify | Prefect Technologies | Elementl |
| **정의 방식** | Python DAG | Python Task | Python Flow | Python Asset/Job |
| **동적 DAG** | 제한적 | 없음 | 완전 지원 | 완전 지원 |
| **관찰성** | 기본 UI | 기본 UI | 강력한 UI | 매우 강력한 UI |
| **데이터 자산** | 없음 | 없음 | 제한적 | 핵심 개념 |
| **클라우드 서비스** | MWAA, Composer | 없음 | Prefect Cloud | Dagster Cloud |
| **활성 커뮤니티** | 매우 높음 | 낮음 | 높음 | 높음 |
| **러닝 커브** | 중간 | 쉬움 | 쉬움 | 중간 |

| 한계 | 설명 | 대안 |
|:---|:---|:---|
| **실시간 스트리밍 불가** | 배치 지향 설계 | Apache Flink, Kafka Streams |
| **동적 태스크 제한** | DAG 구조 런타임 변경 어려움 | Prefect, Dagster |
| **스케줄러 단일 장애점** | 스케줄러 다운 시 전체 중단 | Airflow 2.x HA 스케줄러 |
| **무거운 설치** | Celery + Redis 설정 복잡 | MWAA, Cloud Composer 관리형 |
| **의존성 표현 한계** | 크로스-DAG 의존성 어려움 | 외부 센서 + 이벤트 |

| 서비스 | 제공사 | 특징 |
|:---|:---|:---|
| **Amazon MWAA** | AWS | EKS 기반, IAM 통합 |
| **Cloud Composer** | GCP | GKE 기반, GCP 서비스 완전 통합 |
| **Astronomer** | Astronomer | 전문 Airflow 관리형 SaaS |

---

## 4. 비교 및 연결

```
┌──────────────────────────────────────────────────────────────┐
│                  Airflow 모범 사례 (Best Practices)          │
├──────────────────────────────────────────────────────────────┤
│  DAG 설계                                                    │
│  □ 한 DAG당 하나의 논리적 워크플로우만                       │
│  □ 태스크를 원자적(Atomic)으로 설계 (재시도 안전)            │
│  □ 비즈니스 로직은 DAG 외부 (Python 모듈)에 위치             │
│  □ XCom은 소량 데이터만 (대용량은 S3/GCS 경유)              │
├──────────────────────────────────────────────────────────────┤
│  성능                                                        │
│  □ schedule_interval 최소 5분 이상 (너무 잦은 실행 금지)     │
│  □ max_active_runs로 동시 실행 제한                          │
│  □ 연결 풀링 (Connections Pool) 활용                         │
├──────────────────────────────────────────────────────────────┤
│  운영                                                        │
│  □ Variables/Connections에 민감 정보 저장 (하드코딩 금지)    │
│  □ SLA (Service Level Agreement) 설정으로 지연 알람          │
│  □ 로그 외부화 (S3/GCS)로 장기 보관                         │
└──────────────────────────────────────────────────────────────┘
```

**Q. Apache Airflow와 Luigi, Prefect를 비교하고 각각의 적합 사용 사례를 설명하시오.**

- **Airflow**: 복잡한 의존성의 대규모 배치 파이프라인, 풍부한 Operator 생태계, 안정성이 검증된 운영 환경에 적합
- **Luigi**: 간단한 파이프라인, 소규모 팀에서 빠른 도입이 필요할 때 적합
- **Prefect**: 동적 워크플로우(런타임 DAG 변경), 마이크로서비스 아키텍처, 데이터 품질 검증에 적합
- **Dagster**: 데이터 자산(Asset) 중심 파이프라인, 데이터 품질 가시성, ML 파이프라인에 적합

**Q. Airflow KubernetesExecutor의 동작 원리와 장단점을 설명하시오.**

KubernetesExecutor는 각 Airflow Task를 독립된 쿠버네티스 Pod로 실행한다. Scheduler가 Task를 대기 큐에서 꺼내면, K8s API를 통해 Pod를 생성하고 Task를 실행한다. Task 완료 후 Pod는 자동 삭제된다.
- **장점**: 완전한 자원 격리, 동적 스케일링, Task별 다른 Docker 이미지 사용 가능
- **단점**: Pod 생성 오버헤드(수십 초), 단발성 Task가 많으면 오버헤드 누적, K8s 운영 지식 필요

```
┌──────────────────────────────────────────────────────────────┐
│              엔터프라이즈 Airflow 배포 구조                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Git (DAG 코드 관리)                                         │
│       │ CI/CD                                                │
│       ▼                                                      │
│  DAG 파일 서버 (NFS/S3)                                      │
│       │ 마운트                                               │
│       ▼                                                      │
│  Airflow Web Server ←── 운영자 모니터링                      │
│  Airflow Scheduler                                           │
│       │ 태스크 할당                                          │
│       ▼                                                      │
│  ┌─────────────────────────────────────────┐               │
│  │  Celery Workers (Auto Scaling Group)    │               │
│  │  Worker 1  Worker 2  ...  Worker N      │               │
│  └─────────────────────────────────────────┘               │
│       │                                                      │
│       ▼                                                      │
│  외부 시스템: BigQuery, Spark, S3, Redis, ML 서버            │
│                                                              │
│  메타데이터: Aurora PostgreSQL (Multi-AZ)                    │
│  브로커: Redis ElastiCache                                   │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. 실무 적용 및 판단

| 항목 | 크론탭 기반 | Airflow 기반 | 개선 |
|:---|:---|:---|:---|
| **의존성 관리** | 없음 (시간 기반만) | DAG로 명확한 관계 표현 | 파이프라인 신뢰성 향상 |
| **실패 처리** | 수동 확인 후 재실행 | 자동 재시도 + 알람 | 운영 공수 80% 감소 |
| **가시성** | 없음 | Web UI 실시간 모니터링 | 이슈 감지 속도 향상 |
| **코드 관리** | 분산된 쉘 스크립트 | Git 기반 버전 관리 | 코드 품질 향상 |
| **확장성** | 서버 증설 | CeleryExecutor 워커 추가 | 수평 확장 가능 |

Apache Airflow는 데이터 엔지니어링과 MLOps 분야에서 사실상 표준(De Facto Standard) 워크플로우 오케스트레이션 도구다. DAG 기반 의존성 관리, 풍부한 Operator 생태계, 시각적 모니터링은 복잡한 데이터 파이프라인 운영을 코드로 관리할 수 있게 한다. 실시간 스트리밍이 아닌 배치 파이프라인에서 검증된 선택이다.

```
┌──────────────────────────────────────────────────────────────────┐
│                     Apache Airflow 아키텍처                      │
├────────────────┬─────────────────────────────────────────────────┤
│  Web Server    │  Django 기반 Web UI                              │
│  (Flask)       │  DAG 시각화, 실행 현황, 로그 확인                │
├────────────────┼─────────────────────────────────────────────────┤
│  Scheduler     │  DAG 파일 파싱, 트리거 결정                      │
│                │  스케줄 기반 또는 외부 트리거로 DagRun 생성      │
├────────────────┼─────────────────────────────────────────────────┤
│  Executor      │  실제 작업 실행 담당                              │
│                │  Sequential/Local/Celery/Kubernetes              │
├────────────────┼─────────────────────────────────────────────────┤
│  Workers       │  Executor에서 할당받은 Task 실행                  │
│                │  Celery: Celery Worker                          │
│                │  K8s: Pod로 Task 실행                           │
├────────────────┼─────────────────────────────────────────────────┤
│  Metadata DB   │  DAG 메타데이터, 실행 이력                       │
│  (PostgreSQL)  │  변수(Variables), 연결(Connections)              │
├────────────────┼─────────────────────────────────────────────────┤
│  DAG 파일      │  Python 파일로 정의된 워크플로우                  │
│  (File System) │  Scheduler가 주기적으로 파싱                     │
└────────────────┴─────────────────────────────────────────────────┘
```

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta

# DAG 기본 설정
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['alert@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,                           # 실패 시 3회 재시도
    'retry_delay': timedelta(minutes=5),    # 재시도 간격 5분
}

with DAG(
    dag_id='ml_training_pipeline',
    default_args=default_args,
    description='ML 학습 파이프라인',
    schedule_interval='0 2 * * *',  # 매일 새벽 2시 실행 (cron 표현식)
    start_date=datetime(2024, 1, 1),
    catchup=False,  # 과거 실행 누락 복구 안 함
    tags=['ml', 'training'],
) as dag:

    # 단계 1: 데이터 추출
    extract_task = BashOperator(
        task_id='extract_data',
        bash_command='python /opt/scripts/extract.py --date {{ ds }}',
    )

    # 단계 2: 데이터 검증
    def validate_data(**context):
        execution_date = context['ds']
        # 검증 로직...
        print(f"{execution_date} 데이터 검증 완료")

    validate_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
    )

    # 단계 3: BigQuery 변환
    transform_task = BigQueryInsertJobOperator(
        task_id='transform_data',
        configuration={
            "query": {
                "query": "{% raw %}{% include 'sql/transform.sql' %}{% endraw %}",
                "useLegacySql": False,
            }
        },
    )

    # 단계 4: 모델 학습
    train_task = BashOperator(
        task_id='train_model',
        bash_command='python /opt/scripts/train.py --date {{ ds }}',
    )

    # 의존성 설정 (오른쪽 화살표 = 실행 순서)
    extract_task >> validate_task >> transform_task >> train_task
```

| Operator | 설명 | 사용 예시 |
|:---|:---|:---|
| **BashOperator** | 셸 명령어 실행 | 스크립트 실행, 파일 이동 |
| **PythonOperator** | Python 함수 실행 | 데이터 처리, API 호출 |
| **SparkSubmitOperator** | Spark 잡 제출 | 대용량 배치 처리 |
| **BigQueryOperator** | BigQuery SQL 실행 | 데이터 변환, 집계 |
| **S3ToRedshiftOperator** | S3 → Redshift 복사 | 데이터 로딩 |
| **KubernetesPodOperator** | K8s Pod 실행 | 컨테이너 기반 작업 |
| **DummyOperator** | 빈 작업 (분기 포인트) | DAG 구조화 |
| **BranchPythonOperator** | 조건부 분기 | A/B 실행 경로 선택 |

```
┌───────────────────────────────────────────────────────────────┐
│                     Executor 비교                              │
├──────────────────┬──────────────┬────────────────────────────┤
│ SequentialExecutor│ 단일 프로세스│ 개발/테스트용, 병렬 불가  │
├──────────────────┼──────────────┼────────────────────────────┤
│ LocalExecutor     │ 로컬 멀티프로│ 소규모 운영, 단일 서버    │
│                   │ 세스 (fork) │ (수십 개 태스크 동시)     │
├──────────────────┼──────────────┼────────────────────────────┤
│ CeleryExecutor    │ 분산 워커    │ 중~대규모, 고가용성       │
│                   │ (RabbitMQ/  │ 워커 수평 확장 가능       │
│                   │  Redis)     │ 복잡한 설정 필요          │
├──────────────────┼──────────────┼────────────────────────────┤
│ KubernetesExecutor│ 태스크별    │ 클라우드 네이티브         │
│                   │ K8s Pod 생성│ 자원 격리, 동적 스케일링  │
│                   │             │ 태스크 시작 오버헤드 있음 │
└──────────────────┴──────────────┴────────────────────────────┘
```

---

## 6. 기대효과 및 결론

Apache Airflow는 데이터 엔지니어링과 MLOps 분야에서 사실상 표준(De Facto Standard) 워크플로우 오케스트레이션 도구다.

데이터 파이프라인 워크플로우 DAG 제어 (Apache Airflow) 자동화의 효과는 성능 향상 자체보다도 예측 가능성과 운영 일관성을 확보하는 데 있다. 반대로 데이터 품질, 거버넌스, 모니터링 없이 도입하면 복잡도만 늘고 실질 가치는 줄어든다. 따라서 이 주제는 기능 도입이 아니라 구조적 운영 역량과 함께 판단해야 하며, 향후에는 자동화·실시간성·설명 가능성·비용 최적화와 결합된 방향으로 발전한다.

---

## 7. 발전 흐름도

```text
cron + 쉘 스크립트 (원시적 스케줄링)
    │
    ▼
Apache Airflow: Python DAG 기반 워크플로우
    ├─► Scheduler: DAG 실행 스케줄링
    ├─► Executor: Sequential · Celery · Kubernetes
    └─► Web UI: 실행 현황 · 로그 · 재시도 관리
    │
    ▼
Airflow + Kubernetes Executor → 동적 Pod 스케일링
    │
    ▼
차세대 오케스트레이터
    ├─► Dagster: 자산 기반 (Asset-centric)
    ├─► Prefect: Pythonic, 클라우드 네이티브
    └─► Mage AI: 통합 데이터 파이프라인
```

---

## 8. 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 핵심 개념 | DAG (Directed Acyclic Graph) | 작업 의존성 표현 그래프 |
| 핵심 구성 | Scheduler | DAG 파싱 및 실행 트리거 |
| 핵심 구성 | Executor | 태스크 실행 방식 결정 |
| 핵심 구성 | Operator | 개별 태스크 실행 단위 |
| 비교 도구 | Luigi (Spotify) | 범용 파이프라인 (경쟁) |
| 비교 도구 | Prefect | 동적 워크플로우 (경쟁) |
| 비교 도구 | Dagster | 데이터 자산 중심 (경쟁) |
| 연관 | Kubeflow Pipelines | ML 특화 파이프라인 (협력/경쟁) |
| 상위 개념 | MLOps | Airflow는 CT 파이프라인 스케줄링에 활용 |
| 클라우드 | Amazon MWAA | AWS 관리형 Airflow |
| 클라우드 | Cloud Composer | GCP 관리형 Airflow |
