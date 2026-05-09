+++
weight = 270
title = "270. 데이터 품질 (Data Quality) - Great Expectations"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 품질은 정확성(Accuracy), 완전성(Completeness), 일관성(Consistency), 적시성(Timeliness), 유효성(Validity)의 5가지 차원으로 측정되며, 나쁜 데이터는 나쁜 의사결정과 직결되는 비즈니스 리스크다.
> 2. **가치**: Great Expectations 같은 오픈소스 프레임워크로 파이프라인 내에 데이터 테스트를 자동화하면, "garbage in, garbage out" 문제를 조기에 차단하여 DW·ML 모델에 나쁜 데이터가 유입되는 것을 방지한다.
> 3. **판단 포인트**: 데이터 계약(Data Contract)은 생산자-소비자 간 품질 기준을 코드로 명문화하는 패러다임 전환 — 단순 모니터링이 아닌 "계약 위반 시 파이프라인 자동 중단"으로 품질을 보장한다.

---

## Ⅰ. 개요 및 필요성

AI 회사에서 ML 모델이 고객 이탈 예측을 잘못하여 마케팅 캠페인에 수억 원을 낭비했다. 조사해보니 훈련 데이터의 20%가 NULL값이었고, 거래 금액이 음수인 레코드가 섞여 있었다. 모델의 문제가 아니라 **데이터 품질**의 문제였다.

"나쁜 데이터(Dirty Data)"는 비즈니스 리스크다. IBM 연구에 따르면 미국에서 데이터 품질 문제로 인한 비즈니스 손실이 연간 3.1조 달러에 달한다.

```
[데이터 품질 5가지 차원]

정확성(Accuracy):    실제 값과 일치하는가?
                     예: 나이=150, 음수 금액 → 오류

완전성(Completeness): 필수 필드가 채워져 있는가?
                     예: 고객 이름이 NULL → 불완전

일관성(Consistency): 시스템 간 동일 값이 일치하는가?
                    예: CRM과 DW의 고객 수가 다름 → 불일치

적시성(Timeliness): 제때 최신 데이터가 도착했는가?
                   예: 어제 배치가 아직 미완료 → 지연

유효성(Validity):   정의된 형식/범위를 따르는가?
                   예: 이메일 형식 오류, 날짜 범위 초과
```

📢 **섹션 요약 비유**: 데이터 품질은 요리 재료의 신선도다. 아무리 좋은 레시피(알고리즘)와 훌륭한 셰프(데이터 과학자)가 있어도, 상한 재료(나쁜 데이터)로 만든 요리는 맛이 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Great Expectations (GE) 핵심 개념

| 개념 | 설명 | 예시 |
|:---|:---|:---|
| **Expectation** | 개별 데이터 품질 규칙 | `expect_column_not_to_be_null` |
| **Expectation Suite** | Expectation 집합 | 테이블별 전체 품질 규칙 묶음 |
| **Checkpoint** | 검증 실행 단위 | ETL 파이프라인 각 단계 |
| **Validation Result** | 검증 통과/실패 결과 | JSON 형태 상세 보고서 |
| **Data Docs** | 품질 보고서 자동 생성 | HTML 형태 대시보드 |

### GE 코드 예시

```python
import great_expectations as gx

context = gx.get_context()

# Expectation Suite 생성
suite = context.add_expectation_suite("orders.basic")

# Validator 로드
validator = context.get_validator(
    datasource_name="my_postgres_db",
    data_asset_name="orders"
)

# 품질 규칙 정의
validator.expect_column_to_exist("order_id")
validator.expect_column_values_to_not_be_null("order_id")
validator.expect_column_values_to_be_unique("order_id")
validator.expect_column_values_to_be_between(
    "amount", min_value=0, max_value=10000000
)
validator.expect_column_values_to_match_regex(
    "email", r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
)
validator.expect_column_values_to_be_in_set(
    "status", ["pending", "completed", "cancelled"]
)

# Checkpoint 생성 및 실행
checkpoint = context.add_or_update_checkpoint(
    name="orders_checkpoint",
    validations=[{"expectation_suite_name": "orders.basic"}]
)

results = checkpoint.run()
if not results.success:
    raise DataQualityError("데이터 품질 검증 실패 → 파이프라인 중단")
```

### 데이터 계약(Data Contract) 개념

```yaml
# Data Contract: orders 테이블
# 파일: contracts/orders_v1.yaml
apiVersion: v1
name: "orders"
version: "1.0.0"

schema:
  fields:
    - name: order_id
      type: integer
      required: true
      unique: true
    - name: amount
      type: decimal
      required: true
      minimum: 0
    - name: status
      type: string
      enum: ["pending", "completed", "cancelled"]

quality:
  completeness: "> 99%"
  freshness: "< 1 hour"

sla:
  availability: "99.9%"
  latency: "< 30 minutes"

owners:
  - team: "orders-service"
    contact: "orders-team@company.com"
```

📢 **섹션 요약 비유**: 데이터 계약은 식재료 납품 계약서다. "닭고기를 1kg씩 신선도 A등급으로 매일 오전 6시까지 납품하라"는 계약처럼, 데이터 생산자와 소비자가 품질 기준을 코드로 약속한다.

---

## Ⅲ. 비교 및 연결

### 데이터 품질 도구 비교

| 도구 | 유형 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| **Great Expectations** | 오픈소스 | 코드 기반, 풍부한 Expectation | Python 파이프라인 |
| **dbt Tests** | 오픈소스 | SQL 기반, dbt 통합 | SQL 변환 파이프라인 |
| **Apache Griffin** | 오픈소스 | Spark 기반, 대규모 | Hadoop 에코시스템 |
| **Soda** | 상용/오픈소스 | SodaCL 언어, 알림 통합 | 다양한 데이터 소스 |
| **Monte Carlo** | 상용 | ML 기반 이상 탐지 | 엔터프라이즈 |

### 데이터 품질 검증 위치 (파이프라인 단계)

```
데이터 소스 → [검증 1] → 스테이징 → [검증 2] → DW → [검증 3] → 대시보드

검증 1 (소스 레이어):  스키마, null 체크, 범위 검증
검증 2 (변환 레이어):  비즈니스 규칙, 집계 일관성
검증 3 (서빙 레이어):  최종 데이터 완전성, 적시성

"Shift Left": 검증을 최대한 소스 가까이에서 실행
→ 나쁜 데이터가 파이프라인 깊이 침투하기 전에 차단
```

📢 **섹션 요약 비유**: 데이터 품질 검증의 "Shift Left"는 공장의 원재료 검수다. 완성품이 된 후에 불량을 발견하면 폐기 비용이 크지만, 원재료 입고 단계에서 불량을 거르면 비용이 훨씬 적다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### CI/CD 파이프라인에 데이터 품질 통합

```yaml
# GitHub Actions: 데이터 품질 게이트
name: Data Quality Gate

on:
  schedule:
    - cron: '0 6 * * *'  # 매일 오전 6시 실행

jobs:
  data-quality:
    steps:
      - name: Run Great Expectations
        run: |
          great_expectations checkpoint run orders_daily
          if [ $? -ne 0 ]; then
            echo "Data quality check FAILED"
            # 알림 전송
            curl -X POST $SLACK_WEBHOOK -d '{"text": "DQ 실패: orders_daily 파이프라인 중단"}'
            exit 1
          fi
```

### 데이터 품질 메트릭 모니터링

| 메트릭 | 측정 방법 | 알림 기준 |
|:---|:---|:---|
| Null 비율 | `COUNT(null) / COUNT(*)` | > 1% |
| 중복 비율 | `COUNT(*) - COUNT(DISTINCT PK)` | > 0% |
| 신선도 | `MAX(updated_at) - NOW()` | > 2시간 |
| 형식 오류 | 정규식 패턴 불일치 수 | > 0건 |
| 분포 이탈 | Z-score 또는 IQR 기반 | > 3σ |

### 기술사 시험 판단 포인트

- **데이터 품질 5차원**: 정확성·완전성·일관성·적시성·유효성을 각각 별도 측정
- **Data Contract**: 코드로 품질 기준을 계약화하여 생산자 책임 명확화
- **Shift Left 원칙**: 소스에 가까울수록 품질 이슈 탐지 비용이 저렴

📢 **섹션 요약 비유**: Great Expectations는 데이터의 의사 건강검진이다. 매일 정해진 시간에 혈압(null 비율)·혈당(범위 이탈)·체중(데이터 건수)을 자동 측정하고, 이상이 있으면 즉시 알림을 보낸다. 큰 병이 되기 전에 작은 이상을 잡는 것이 목적이다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 영역 | 효과 |
|:---|:---|
| **의사결정 신뢰성** | 검증된 데이터로 경영 보고서 신뢰도 향상 |
| **ML 모델 품질** | 깨끗한 훈련 데이터로 모델 정확도 향상 |
| **운영 효율** | 데이터 품질 이슈 사후 대응 → 사전 차단 |
| **책임 명확화** | Data Contract으로 생산자 책임 구조 확립 |

### 한계 및 주의사항

- **Expectation 관리 비용**: 수백 개의 Expectation을 유지·업데이트하는 것 자체가 작업
- **False Positive**: 지나치게 엄격한 규칙이 정상 데이터를 불합격 처리할 수 있음
- **실시간 검증 비용**: 스트리밍 파이프라인의 모든 레코드를 검증하면 지연 및 비용 급증
- **도구 의존성**: Great Expectations 버전 업그레이드 시 호환성 이슈 발생 가능

📢 **섹션 요약 비유**: 데이터 품질 관리의 가장 큰 함정은 "측정하면 개선될 것이라는 착각"이다. 건강검진 결과를 무시하는 것처럼, 데이터 품질 보고서를 보고 아무 조치도 안 하면 의미가 없다. 측정·알림·자동 차단·책임 있는 수정까지 사이클이 완성되어야 품질이 실제로 개선된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 데이터 계약 | 생산자-소비자 품질 기준 코드화 |
| Great Expectations | 파이프라인 내 데이터 품질 자동 검증 |
| dbt Tests | SQL 변환 단계의 품질 테스트 |
| 데이터 거버넌스 | 품질 기준 설정의 조직적 프레임워크 |
| 스키마 드리프트 | 품질 이슈의 주요 원인 (스키마 변경) |
| MLOps | ML 파이프라인에서 데이터 품질이 모델 품질의 전제 |

### 👶 어린이를 위한 3줄 비유 설명
1. 데이터 품질은 숙제 검사야. 숙제를 다 했는지(완전성), 맞는지(정확성), 제때 냈는지(적시성)를 선생님이 확인해.
2. Great Expectations는 자동 채점기야. 규칙을 미리 등록해두면 매번 선생님이 직접 보지 않아도 자동으로 맞고 틀림을 알려줘.
3. 데이터 계약은 숙제 약속이야. "매일 10문제, 오전 9시까지, 이름 반드시 쓰기"라고 미리 약속해두면 기준이 명확해!
