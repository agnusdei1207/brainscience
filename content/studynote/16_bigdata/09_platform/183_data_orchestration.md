+++
weight = 183
title = "183. 데이터 오케스트레이션 (Data Orchestration) — Apache Airflow/Dagster/Prefect"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: 데이터 오케스트레이션 (Data Orchestration) — Apache Airflow/Dagster/Prefect은(는) 수집·저장·처리·분석·운영을 하나의 아키텍처로 연결하기 위한 빅데이터 플랫폼 설계 요소다.
> **비유**: 도시 전체의 도로, 창고, 관제, 배송 체계를 한 번에 설계하는 종합 교통망과 같다.

📝 모범 답안

## 1. 개요 및 필요성

### 1-1. 오케스트레이션이 필요한 이유

수동으로 관리하는 데이터 파이프라인의 문제:
- 실패 시 재시도 없음 → 데이터 손실
- 의존성 파악 어려움 → 순서 오류
- 실행 이력 추적 불가 → 장애 원인 파악 지연
- 단순 cron → 복잡한 조건 분기·동적 파이프라인 처리 불가

### 1-2. 주요 도구 비교

| 항목 | Apache Airflow | Dagster | Prefect |
|:---|:---|:---|:---|
| 패러다임 | 태스크 중심 DAG | 자산 중심 | 플로우 중심 |
| Python API | 데코레이터 기반 | 타입 시스템 | 간결한 데코레이터 |
| 테스트 용이성 | 낮음 | 높음 | 중간 |
| 클라우드 관리형 | MWAA, Cloud Composer | Dagster Cloud | Prefect Cloud |
| 생태계 규모 | 매우 큼 | 성장 중 | 성장 중 |

---

## 2. 구성요소

### 2-1. Apache Airflow DAG 구조

```
┌──────────────────────────────────────────────────────────┐
│                  Airflow DAG 예시                        │
│                                                          │
│  extract_data                                            │
│       │                                                  │
│       ▼                                                  │
│  ┌────────────┐   ┌────────────┐                        │
│  │ transform_A│   │ transform_B│  (병렬 실행)           │
│  └─────┬──────┘   └────┬───────┘                        │
│        └──────┬─────────┘                               │
│               ▼                                         │
│          load_to_dw                                     │
│               │                                         │
│               ▼                                         │
│          send_notification                              │
└──────────────────────────────────────────────────────────┘
```

### 2-2. Airflow 핵심 컴포넌트

| 컴포넌트 | 역할 |
|:---|:---|
| DAG | 태스크 의존성 그래프 정의 |
| Operator | 태스크 유형 (PythonOperator, BashOperator, SparkSubmitOperator) |
| Sensor | 외부 조건 대기 (FileSensor, HttpSensor) |
| XCom | 태스크 간 소량 데이터 교환 |
| Executor | 태스크 실행 방식 (LocalExecutor, CeleryExecutor, KubernetesExecutor) |
| Scheduler | DAG 스캔·트리거 담당 |

### 2-3. Dagster 자산 중심 패러다임

```python

@asset
def raw_orders(context) -> pd.DataFrame:
    return fetch_from_db("orders")

@asset
def cleaned_orders(raw_orders: pd.DataFrame) -> pd.DataFrame:
    return raw_orders.dropna()

@asset
def order_metrics(cleaned_orders: pd.DataFrame) -> dict:
    return {"total": len(cleaned_orders)}
```

자산(Asset) 의존성이 코드에서 명시적으로 선언되어 계보가 자동 생성된다.

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 흐름, 운영 자동화, 비용 구조, 확장 전략을 함께 결정해야 한다.

동작 순서:
### 실행 환경별 Airflow Executor

- **LocalExecutor**: 단일 노드, 개발·소규모
- **CeleryExecutor**: Redis/RabbitMQ 큐, 다중 워커
- **KubernetesExecutor**: 태스크당 Pod 생성, 격리·탄력적 확장
- **CeleryKubernetesExecutor**: 하이브리드 (간단 태스크 → Celery, 무거운 태스크 → K8s)

### 오케스트레이션 vs 스케줄링

- **cron**: 시간 기반 단순 스케줄링 (의존성 관리 없음)
- **오케스트레이션**: 의존성·재시도·모니터링·데이터 품질 통합

---

## 4. 비교 및 연결

### 4-1. Airflow 운영 모범 사례

- **동적 DAG 생성**: Factory 패턴으로 반복 파이프라인 DRY
- **태스크 멱등성**: 재실행 시 같은 결과 보장 (파티션 덮어쓰기 설계)
- **SLA 알림**: `sla` 파라미터로 예상 완료 시간 초과 시 알림
- **태그·소유자**: 팀별 DAG 분류, 책임 명확화

### 4-2. 기술사 시험 포인트

- Airflow vs Dagster 선택 기준: 기존 Airflow 팀 많음 → Airflow, 신규 + 테스트 중시 → Dagster
- KubernetesExecutor 장점: 태스크 격리로 의존성 충돌 방지, 자원 탄력적 사용
- dbt와 Airflow 연동: dbt 모델 실행을 Airflow 태스크로 오케스트레이션 (cosmos 라이브러리)

---

## 5. 실무 적용 및 판단

| 효과 | 내용 |
|:---|:---|
| 안정성 향상 | 자동 재시도·알림으로 장애 인지 및 복구 시간 단축 |
| 가시성 | UI 기반 실행 이력·계보로 파이프라인 투명성 확보 |
| 협업 효율 | Git 기반 DAG 코드 협업, PR 리뷰 가능 |

데이터 오케스트레이션은 데이터 파이프라인의 신뢰성과 관리 가능성을 결정한다. 기술사 관점에서 Airflow 도입 시 KubernetesExecutor 기반 확장 전략, SLA 기반 알림 체계, 멱등성 설계 원칙을 아키텍처에 반드시 포함해야 한다.

---

## 6. 기대효과 및 결론

데이터 오케스트레이션 (Data Orchestration) — Apache Airflow/Dagster/Prefect은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 플랫폼 설계의 승패는 기능 나열보다 운영 가능성과 비용 지속 가능성을 확보하느냐에 달려 있다.

---

## 7. 발전 흐름도

```text
[수동 ETL 파이프라인]
    │
    ▼
[워크플로우 자동화]
    │
    ▼
[Airflow(DAG 기반 오케스트레이션)]
    │
    ▼
[데이터 메시]
    │
    ▼
[실시간 데이터 오케스트레이션]
```

데이터 오케스트레이션은 수동 ETL을 넘어 DAG, 데이터 메시, 실시간 파이프라인으로 진화한다.

---

## 8. 관련 개념 맵

| 개념 | 관련 기술 | 연결 포인트 |
|:---|:---|:---|
| DAG | 위상 정렬, 그래프 이론 | 의존성 순환 방지 |
| KubernetesExecutor | K8s Pod | 태스크 격리 실행 |
| XCom | Airflow 태스크 통신 | 태스크 간 소량 데이터 |
| dbt + Airflow | cosmos 라이브러리 | SQL 변환 오케스트레이션 |
| SLA | 데이터 신선도 | 파이프라인 완료 시간 보장 |
