+++
weight = 273
title = "273. 피처 스토어 (Feature Store) - ML 변수 관리"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 피처 스토어(Feature Store)는 ML 모델 훈련(오프라인)과 실시간 서빙(온라인) 양쪽에서 동일한 Feature를 일관성 있게 제공하여 훈련-서빙 불일치(Training-Serving Skew)를 방지하는 ML 인프라 레이어다.
> 2. **가치**: 팀 A가 만든 "사용자 구매 빈도" Feature를 팀 B가 재사용하고, 실시간 추론 시 Feature를 매번 재계산하지 않고 사전 계산된 값을 수 ms 이내에 조회하여 추론 지연을 최소화한다.
> 3. **판단 포인트**: 온라인(저지연 조회, Redis/DynamoDB)과 오프라인(대용량 배치 훈련, S3/Hive) 스토어를 분리하여 운영하되, 두 스토어 간 Feature 값의 일관성 유지가 가장 중요한 설계 과제다.

---

## Ⅰ. 개요 및 필요성

추천 시스템 팀이 "사용자의 최근 30일 구매 횟수"를 Feature로 사용한다. 이 Feature는:
1. 모델 **훈련** 시: 6개월치 배치 데이터에서 계산
2. 모델 **서빙** 시: 실시간으로 DB에서 직접 계산

만약 훈련과 서빙에서 Feature 계산 방법이 조금이라도 다르면 모델 성능이 저하된다. 이것이 **Training-Serving Skew**다.

```
[피처 스토어 없는 경우 (문제)]

훈련: "30일 구매 횟수" = Spark SQL로 계산
               ↕ 코드 불일치!
서빙: "30일 구매 횟수" = Java/Python 코드로 재구현

→ 미묘한 차이 (타임존, 반올림 등)로 Feature 불일치
→ 프로덕션 모델 성능이 개발 환경보다 낮은 이유!

[피처 스토어 있는 경우 (해결)]

훈련: Feature Store에서 "user_purchase_30d" 조회
서빙: Feature Store에서 동일 "user_purchase_30d" 조회
→ 완전한 일관성 보장!
```

📢 **섹션 요약 비유**: 피처 스토어는 표준 재료 창고다. 모든 셰프(ML 팀)가 같은 창고에서 같은 규격의 재료(Feature)를 가져다 쓰므로, 레시피(모델)가 달라도 재료 품질은 동일하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 피처 스토어 이중 구조

```
[피처 스토어 아키텍처]

Feature 생성 파이프라인
┌─────────────────────────────────────────────────┐
│  원본 데이터 (DB, 이벤트 스트림)                   │
│         │                                       │
│  ┌──────▼──────────────────────────┐            │
│  │  Feature 계산 파이프라인         │            │
│  │  (Spark/Flink: 배치+스트리밍)    │            │
│  └──────────────────────────────┐  │            │
└─────────────────────────────────│──┘            │
                                  │                │
                   ┌──────────────┤                │
                   │              │                │
                   ▼              ▼                │
         ┌─────────────┐  ┌──────────────┐        │
         │ 오프라인 스토어│  │ 온라인 스토어│        │
         │ (S3/Hive)   │  │ (Redis/DDB) │        │
         │ 대용량 배치  │  │ 저지연 조회  │        │
         │ 훈련 데이터  │  │ ms 단위 응답│        │
         └─────────────┘  └──────────────┘        │
                │                  │               │
         ML 훈련 파이프라인    실시간 추론 서버       │
```

### Feature 레지스트리

```python
# Feast (오픈소스 피처 스토어) 예시

from feast import FeatureStore, Entity, Feature, FeatureView
from feast.types import Float64, Int64

# Feature 정의
user_stats_view = FeatureView(
    name="user_purchase_stats",
    entities=["user_id"],
    ttl=timedelta(days=30),
    features=[
        Feature(name="purchase_count_30d", dtype=Int64),
        Feature(name="total_amount_30d", dtype=Float64),
        Feature(name="avg_order_value", dtype=Float64),
    ],
    source=purchase_events_source
)

# 훈련 데이터 조회 (오프라인)
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=["user_purchase_stats:purchase_count_30d"]
).to_df()

# 실시간 서빙 (온라인)
online_features = store.get_online_features(
    features=["user_purchase_stats:purchase_count_30d"],
    entity_rows=[{"user_id": 12345}]
)
```

### Feature 카탈로그와 재사용

```
[Feature 재사용 패턴]

팀 A (추천 시스템): "user_purchase_30d" Feature 생성
                                │
                                ▼
                    Feature Store에 등록
                    (이름, 설명, 소유팀, 계산 방법, 품질 메트릭)
                                │
팀 B (사기 탐지):   ←────────────┘  재사용 (재계산 불필요)
팀 C (신용 평가):   ←────────────────┘  재사용
```

📢 **섹션 요약 비유**: Feature Store의 Feature 카탈로그는 요리 기본 재료 데이터베이스다. 누군가 "표준 밀가루 반죽" 만드는 법을 한번 정의해두면, 모든 베이커리 팀이 재정의 없이 그 레시피를 가져다 쓸 수 있다.

---

## Ⅲ. 비교 및 연결

### 피처 스토어 제품 비교

| 제품 | 유형 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| **Feast** | 오픈소스 | 경량, 클라우드 불가지론 | 소~중형 팀 |
| **Tecton** | 상용 | 엔터프라이즈급, 모니터링 강화 | 대형 기업 |
| **Databricks Feature Store** | 클라우드+상용 | Unity Catalog 통합 | Databricks 사용자 |
| **AWS SageMaker Feature Store** | 클라우드 | AWS 생태계 통합 | AWS 기반 MLOps |
| **Vertex AI Feature Store** | 클라우드 | GCP 통합, 서버리스 | GCP 기반 MLOps |
| **Hopsworks** | 오픈소스/상용 | 스트리밍 지원, Python-first | Flink 기반 파이프라인 |

### Training-Serving Skew 원인과 해결

| 원인 | 설명 | 피처 스토어 해결 |
|:---|:---|:---|
| 코드 중복 구현 | 훈련/서빙 다른 언어로 재구현 | 단일 Feature 정의 |
| 시간 기준 차이 | 훈련은 Event Time, 서빙은 Processing Time | Point-in-time Correct Join |
| 데이터 누락 | 서빙 시 Feature 값 없으면 NULL | 기본값 정책 표준화 |

📢 **섹션 요약 비유**: Training-Serving Skew는 레시피 번역 오류다. 한국어 레시피(훈련 코드)를 영어(서빙 코드)로 번역할 때 "1 컵"을 200ml로 번역하면 실제 결과가 달라진다. 피처 스토어는 번역 없이 모두가 동일한 원본 레시피를 쓰게 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Point-in-Time Correct Join

```python
# 타임트래블 조인: 특정 시점의 Feature 값 조회
# 훈련 데이터의 각 이벤트 시점에서의 Feature 값 사용

entity_df = pd.DataFrame({
    "user_id": [1001, 1002, 1003],
    "event_timestamp": ["2024-01-10", "2024-01-15", "2024-01-20"]
})

# Feature Store: 각 이벤트 시점의 user_purchase_30d 반환
# (미래 데이터 누출 방지: 2024-01-10 이전 30일만 계산)
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=["user_stats:purchase_count_30d"]
).to_df()
```

### MLOps 파이프라인에서의 역할

```
[피처 스토어 중심 MLOps 파이프라인]

데이터 → Feature Pipeline → Feature Store
                                  │
              ┌───────────────────┤
              │                   │
         훈련 파이프라인      실시간 서빙
         (오프라인 Feature)  (온라인 Feature)
              │
         모델 레지스트리
              │
         배포 → 모니터링 (Feature 드리프트 감지)
```

### 기술사 시험 판단 포인트

- **온라인/오프라인 분리 이유**: 훈련은 대용량 배치 처리, 서빙은 저지연 조회 — 전혀 다른 최적화 방향
- **Point-in-Time Correct Join**: 데이터 누출(Data Leakage) 방지 — 미래 시점 Feature가 훈련에 포함되지 않도록
- **Feature 드리프트**: 서빙 시 Feature 분포가 훈련 시와 달라지면 모델 성능 저하 → 모니터링 필수

📢 **섹션 요약 비유**: Point-in-time Join은 시험 공부 규칙이다. 2023년 문제를 풀 때 "2023년 이전까지만 알고 있던 내용"으로만 풀어야 한다. 2024년 지식으로 2023년 시험을 푸는 것은 치팅(데이터 누출)이다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 영역 | 효과 |
|:---|:---|
| **일관성** | 훈련-서빙 Feature 완전 일치 보장 |
| **재사용성** | 팀 간 Feature 공유로 중복 개발 제거 |
| **서빙 성능** | 사전 계산된 Feature 조회로 추론 지연 최소화 |
| **ML 생산성** | Feature 발견·재사용으로 모델 개발 속도 향상 |

### 한계 및 주의사항

- **운영 복잡성**: 온라인/오프라인 이중 스토어 유지, 동기화 파이프라인 관리
- **새로운 Feature 추가 비용**: Feature 정의·파이프라인·테스트·문서화 = 상당한 엔지니어링 비용
- **Feature 폭발 문제**: 수천 개의 Feature가 쌓이면 관리·발견이 어려워짐
- **실시간 Feature 지원 한계**: 초 단위 이하 실시간 Feature는 스트리밍 파이프라인 별도 구축 필요

📢 **섹션 요약 비유**: 피처 스토어 구축은 도서관 시스템 구축과 같다. 처음엔 책(Feature)이 몇 권 없어서 파일 폴더면 충분하다. 수백만 권이 생기면 도서관 시스템(Catalog + 검색 + 반납 시스템)이 필요하다. 단, 시스템 자체를 유지하는 사서(엔지니어)가 필요하다는 것이 비용이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Training-Serving Skew | 피처 스토어가 해결하는 핵심 문제 |
| MLOps | 피처 스토어는 MLOps 파이프라인의 데이터 레이어 |
| 데이터 리니지 | Feature의 원본 추적에 리니지 도구 활용 |
| 온라인 스토어 | Redis/DynamoDB: 저지연 실시간 Feature 조회 |
| 오프라인 스토어 | S3/Hive: 대용량 배치 훈련 데이터 제공 |
| Point-in-Time Join | 데이터 누출 방지를 위한 시간 기준 조인 |

### 👶 어린이를 위한 3줄 비유 설명
1. 피처 스토어는 학교 급식 재료창고야. 모든 선생님(ML 팀)이 같은 창고에서 재료(Feature)를 가져다 쓰니까 요리(모델) 재료가 항상 같아.
2. 급식실(온라인 스토어)에서는 바로바로 꺼낼 수 있고, 냉동창고(오프라인 스토어)에는 많은 양이 보관돼.
3. 어제 공부한 내용으로만 오늘 시험을 봐야 하듯이(Point-in-Time Join), AI도 미래 데이터를 보지 않고 훈련해야 제대로 작동해!
