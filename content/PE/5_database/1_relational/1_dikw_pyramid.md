+++
title = "DIKW 피라미드 (Data Information Knowledge Wisdom)"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
+++

# DIKW 피라미드 (Data Information Knowledge Wisdom)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DIKW 피라미드는 데이터(Data)가 정보(Information)를 거쳐 지식(Knowledge)으로, 최종적으로 지혜(Wisdom)로 변환되는 계층적 가치 창출 프로세스를 시각화한 프레임워크로, 데이터베이스 시스템의 근본적 목표를 정의합니다.
> 2. **가치**: 원시 데이터의 단순 축적을 넘어 맥락(Context)을 부여하고 패턴을 추출하며, 미래 예측과 의사결정을 지원함으로써 데이터의 비즈니스 가치를 기하급수적으로 증대시킵니다.
> 3. **융합**: AI/머신러닝은 Information→Knowledge 단계를 자동화하고, 데이터 웨어하우스는 데이터 통합과 정제를 담당하며, BI 도구는 Knowledge 시각화를 수행하는 등 현대 데이터 스택의 각 계층과 밀접하게 연결됩니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**DIKW 피라미드**는 1989년 Russell Ackoff가 체계화한 지식 계층 모델로, 데이터가 의미 있는 정보로, 정보가 조직화된 지식으로, 지식이 통찰력 있는 지혜로 발전하는 과정을 4단계 피라미드 구조로 표현합니다. 데이터베이스 시스템의 궁극적 목표는 단순한 데이터 저장이 아니라, 저장된 데이터를 통해 조직의 의사결정을 지원하는 지혜(Wisdom)를 생성하는 데 있습니다.

**4단계 계층 구조**:
- **Data (데이터)**: 관찰이나 측정을 통해 수집된 원시적 사실(Facts). 가공되지 않은 상태로, 단독으로는 의미가 없음.
- **Information (정보)**: 데이터에 맥락(Context), 구조(Structure), 의미(Meaning)를 부여한 것. "Who, What, Where, When"을 답변.
- **Knowledge (지식)**: 정보 간의 관계를 파악하고 패턴을 추출한 것. "How"를 답변하며, 경험과 학습이 결합됨.
- **Wisdom (지혜)**: 지식을 바탕으로 미래를 예측하고 최적의 의사결정을 내리는 능력. "Why"를 답변하며, 도덕적 판단과 통찰력 포함.

#### 2. 비유를 통한 이해
DIKW 피라미드는 **'요리 과정'**에 비유할 수 있습니다.
- **데이터**: 시장에서 사 온 생재료(당근, 양파, 고기) - 아직 요리가 아니므로 그 자체로는 식사가 될 수 없음
- **정보**: 재료를 손질하여 의미 있게 배치한 상태(다진 야채, 썬 고기) - 요리의 재료로 준비됨
- **지식**: 레시피에 따라 조리한 완성된 요리(카레라이사) - 먹을 수 있는 상태가 됨
- **지혜**: 이 요리가 어떤 상황에서 건강에 좋은지 알고 적절히 활용하는 것 - 영양사의 조언

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 초기 컴퓨터 시스템은 단순히 대량의 데이터를 저장하고 검색하는 데 그쳤습니다. 데이터가 쌓여도 이를 활용한 의사결정은 전적으로 인간의 직관에 의존했고, 데이터와 의사결정 간의 간극이 컸습니다.

2. **혁신적 패러다임의 도입**: 1989년 Russell Ackoff는 "From Data to Wisdom" 논문에서 데이터의 가치 변환 과정을 체계화했습니다. 이는 데이터베이스가 단순 저장소가 아니라 의사결정 지원 시스템의 핵심 인프라임을 정립한 이정표였습니다.

3. **비즈니스적 요구사항**: 현대 기업은 데이터 홍수(Data Deluge) 시대에 직면해 있습니다. 하루 생성되는 2.5엑사바이트의 데이터 중 의미 있는 정보로 전환되는 비율은 1% 미만입니다. DIKW 모델은 이러한 데이터 활용 격차를 해소하기 위한 전략적 프레임워크를 제공합니다.

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. DIKW 계층별 상세 구성 요소 (표)

| 계층 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/시스템 | 비유 |
|:---|:---|:---|:---|:---|
| **Data** | 원시 팩트 수집 | 센서, 로그, 트랜잭션 기록 | RDBMS, Data Lake, IoT | 밀가루, 계란 |
| **Information** | 맥락 부여 및 구조화 | 정제, 분류, 요약, 포맷팅 | ETL, Data Warehouse, SQL | 반죽 완성 |
| **Knowledge** | 패턴 추출 및 관계 파악 | 분석, 마이닝, 모델링, 시뮬레이션 | BI, ML/AI, OLAP | 케이크 굽기 |
| **Wisdom** | 미래 예측 및 의사결정 | 추론, 판단, 통찰, 전략 수립 | AI 의사결정, Expert System | 미식 평론가의 조언 |

#### 2. DIKW 피라미드 구조 및 데이터 변환 흐름 다이어그램

```text
================================================================================
                        [ DIKW Pyramid Architecture ]
================================================================================

                              /\
                             /  \
                            /    \
                           / WIS  \          ← 미래 예측, 의사결정 (Why?)
                          /  DOM   \
                         /==========\
                        /  KNOWLEDGE \       ← 패턴, 규칙, 모델 (How?)
                       /              \
                      /================\
                     /   INFORMATION    \     ← 맥락, 구조, 의미 (Who/What/Where/When?)
                    /                    \
                   /======================\
                  /        DATA            \   ← 원시 팩트, 기호 (Fact)
                 /                          \
                /============================\

================================================================================
                    [ Data Value Transformation Flow ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│  [ Raw Data Sources ]                                                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │ IoT Sensors  │ │ Transaction  │ │ Social Media │ │ Log Files    │       │
│  │  (Temp, GPS) │ │   (Sales)    │ │  (Tweets)    │ │  (Clicks)    │       │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘       │
│         │                │                │                │                │
│         v                v                v                v                │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    DATA LAYER (Collection)                           │   │
│  │  - Format: Binary, JSON, CSV, XML                                   │   │
│  │  - Characteristics: Volume, Velocity, Variety                       │   │
│  │  - Value: Low (Per byte)                                            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ [Processing: Clean, Validate, Integrate]
                                    v
┌─────────────────────────────────────────────────────────────────────────────┐
│  [ Information Layer ]                                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Context Generation:                                                 │   │
│  │  - "Sales in Seoul: 1M KRW (Jan 2024)"                              │   │
│  │  - "Customer A purchased Product X at 14:30"                        │   │
│  │                                                                       │   │
│  │  Transformation:                                                     │   │
│  │  - Aggregation (SUM, AVG, COUNT)                                    │   │
│  │  - Classification (Category, Region)                                │   │
│  │  - Formatting (Reports, Dashboards)                                 │   │
│  │                                                                       │   │
│  │  Systems: Data Warehouse (Snowflake, BigQuery), RDBMS               │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ [Processing: Analyze, Model, Learn]
                                    v
┌─────────────────────────────────────────────────────────────────────────────┐
│  [ Knowledge Layer ]                                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Pattern Recognition:                                                │   │
│  │  - "Sales increase 30% on rainy days"                               │   │
│  │  - "Customer churn probability: 85% if no purchase in 30 days"      │   │
│  │                                                                       │   │
│  │  Knowledge Representation:                                           │   │
│  │  - Rules: IF rain THEN stock += 30%                                 │   │
│  │  - Models: y = f(x1, x2, ..., xn)                                   │   │
│  │  - Ontologies: Entity-Relationship structures                        │   │
│  │                                                                       │   │
│  │  Systems: ML Platform, Business Intelligence, OLAP                  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ [Processing: Reason, Judge, Predict]
                                    v
┌─────────────────────────────────────────────────────────────────────────────┐
│  [ Wisdom Layer ]                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Decision Making:                                                    │   │
│  │  - "Launch umbrella promotion when rain forecast > 60%"             │   │
│  │  - "Implement retention campaign for at-risk customers"             │   │
│  │                                                                       │   │
│  │  Future Prediction:                                                  │   │
│  │  - "Expected Q3 revenue: 5M KRW (+15% YoY)"                         │   │
│  │  - "Market trend: Sustainable products will dominate"               │   │
│  │                                                                       │   │
│  │  Ethical Judgment:                                                   │   │
│  │  - "This data use complies with GDPR"                               │   │
│  │  - "AI recommendation should be explainable"                        │   │
│  │                                                                       │   │
│  │  Systems: Decision Support, AI Agents, Expert Systems               │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
```

#### 3. 심층 동작 원리: 계층 간 변환 프로세스

**① Data → Information 변환 (Contextualization)**
1. **수집(Collection)**: 원시 데이터를 소스 시스템에서 추출
2. **정제(Cleansing)**: 결측치, 이상치, 중복 데이터 처리
3. **통합(Integration)**: 여러 소스의 데이터를 일관된 형식으로 병합
4. **구조화(Structuring)**: 스키마 적용, 데이터 타입 변환
5. **맥락 부여(Contextualizing)**: 시간, 위치, 출처 등 메타데이터 추가

**② Information → Knowledge 변환 (Pattern Recognition)**
1. **탐색(Exploration)**: 시각화, 기술 통계로 데이터 특성 파악
2. **분석(Analysis)**: 상관관계, 인과관계, 트렌드 분석
3. **모델링(Modeling)**: 머신러닝/통계 모델로 패턴 학습
4. **검증(Validation)**: 교차 검증, A/B 테스트로 지식 검증
5. **문서화(Documentation)**: 지식을 규칙, 프로시저, 모델로 형식화

**③ Knowledge → Wisdom 변환 (Insight Generation)**
1. **이해(Understanding)**: 지식의 원인과 결과 파악
2. **추론(Inference)**: 새로운 상황에 지식 적용
3. **판단(Judgment)**: 여러 대안 중 최선의 선택 결정
4. **예측(Prediction)**: 미래 시나리오 시뮬레이션
5. **행동(Action)**: 의사결정을 실제 비즈니스 액션으로 전환

#### 4. 실무 수준의 데이터 파이프라인 구현 예시

```python
# ==============================================================================
# DIKW Pipeline Implementation (Python + SQL)
# ==============================================================================

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import sqlite3

# ==============================================================================
# Stage 1: DATA - Raw Collection
# ==============================================================================

# 원시 데이터 수집 (IoT 센서, 트랜잭션 로그 등)
raw_data = {
    'timestamp': ['2024-01-15 09:30:00', '2024-01-15 10:15:00', ...],
    'customer_id': ['C001', 'C002', ...],
    'product_id': ['P100', 'P205', ...],
    'quantity': [2, 1, ...],
    'price': [50000, 120000, ...],
    'weather': ['rain', 'sunny', ...]
}

df_raw = pd.DataFrame(raw_data)
print(f"[DATA] Raw records collected: {len(df_raw)}")

# ==============================================================================
# Stage 2: INFORMATION - Contextualization & Structuring
# ==============================================================================

# 데이터 정제 및 구조화
df_info = df_raw.copy()

# 1. 결측치 처리
df_info = df_info.dropna(subset=['customer_id', 'product_id'])

# 2. 데이터 타입 변환
df_info['timestamp'] = pd.to_datetime(df_info['timestamp'])
df_info['amount'] = df_info['quantity'] * df_info['price']

# 3. 맥락 정보 추가
df_info['date'] = df_info['timestamp'].dt.date
df_info['hour'] = df_info['timestamp'].dt.hour
df_info['day_of_week'] = df_info['timestamp'].dt.day_name()

# 4. 집계 및 요약
daily_sales = df_info.groupby(['date', 'weather']).agg({
    'amount': 'sum',
    'customer_id': 'nunique'
}).reset_index()

print(f"[INFO] Processed records: {len(df_info)}")
print(f"[INFO] Daily sales summary:\n{daily_sales.head()}")

# ==============================================================================
# Stage 3: KNOWLEDGE - Pattern Recognition & Modeling
# ==============================================================================

# 특성 엔지니어링
df_knowledge = df_info.copy()
df_knowledge['is_weekend'] = df_knowledge['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
df_knowledge['is_rain'] = (df_knowledge['weather'] == 'rain').astype(int)

# 고객별 구매 패턴 분석
customer_pattern = df_knowledge.groupby('customer_id').agg({
    'amount': ['sum', 'mean', 'count'],
    'is_rain': 'mean'  # 비 오는 날 구매 비율
}).reset_index()
customer_pattern.columns = ['customer_id', 'total_amount', 'avg_amount', 'purchase_count', 'rain_purchase_ratio']

# 머신러닝 모델: 이탈 예측
# (실제로는 더 많은 피처와 라벨이 필요)
features = ['avg_amount', 'purchase_count', 'rain_purchase_ratio']
X = customer_pattern[features]
y = (customer_pattern['purchase_count'] < 3).astype(int)  # 간단한 이탈 라벨

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(f"[KNOWLEDGE] Churn prediction accuracy: {model.score(X_test, y_test):.2%}")

# 추출된 지식 규칙
knowledge_rules = {
    "rain_effect": "Sales increase by 30% on rainy days for umbrellas",
    "churn_indicator": "Customers with < 3 purchases in 90 days have 85% churn probability",
    "peak_hours": "Peak sales occur between 14:00-16:00"
}

# ==============================================================================
# Stage 4: WISDOM - Decision Making & Action
# ==============================================================================

def make_business_decision(weather_forecast, customer_segment):
    """
    지혜: 지식을 활용한 의사결정 함수
    """
    decisions = []

    # 날씨 기반 의사결정
    if weather_forecast['rain_probability'] > 0.6:
        decisions.append({
            'action': 'PROMOTION',
            'target': 'umbrella_products',
            'discount': 0.15,
            'reason': 'Rain forecast triggers 30% sales increase opportunity'
        })

    # 고객 세그먼트 기반 의사결정
    if customer_segment['churn_risk'] == 'HIGH':
        decisions.append({
            'action': 'RETENTION_CAMPAIGN',
            'target': customer_segment['customer_id'],
            'incentive': '20% coupon',
            'reason': 'High churn risk based on purchase pattern'
        })

    # 윤리적 판단
    if 'sensitive_data' in customer_segment:
        decisions.append({
            'action': 'PRIVACY_CHECK',
            'requirement': 'GDPR consent verification required'
        })

    return decisions

# 의사결정 실행
weather_forecast = {'rain_probability': 0.75, 'temperature': 15}
customer_segment = {'churn_risk': 'HIGH', 'customer_id': 'C001'}

wisdom_decisions = make_business_decision(weather_forecast, customer_segment)
print(f"[WISDOM] Business decisions: {wisdom_decisions}")

# ==============================================================================
# SQL Implementation for Data Warehouse
# ==============================================================================

sql_queries = """
-- Stage 1-2: Data to Information (ETL)
CREATE TABLE fact_sales AS
SELECT
    t.transaction_id,
    t.timestamp,
    t.customer_id,
    t.product_id,
    t.quantity,
    t.unit_price,
    t.quantity * t.unit_price AS amount,
    w.weather_condition,
    DATE(t.timestamp) AS sale_date,
    EXTRACT(HOUR FROM t.timestamp) AS sale_hour
FROM raw_transactions t
LEFT JOIN weather_data w ON DATE(t.timestamp) = w.date
    AND EXTRACT(HOUR FROM t.timestamp) = w.hour;

-- Stage 3: Information to Knowledge (Analytics)
CREATE VIEW customer_knowledge AS
SELECT
    customer_id,
    SUM(amount) AS lifetime_value,
    COUNT(*) AS purchase_frequency,
    AVG(amount) AS avg_basket_size,
    -- Rainy day preference
    SUM(CASE WHEN weather_condition = 'rain' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
        AS rain_purchase_pct,
    -- Churn risk score
    CASE
        WHEN COUNT(*) < 3 THEN 'HIGH'
        WHEN COUNT(*) < 10 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS churn_risk
FROM fact_sales
GROUP BY customer_id;

-- Stage 4: Knowledge to Wisdom (Decision Support)
-- Actionable recommendation view
CREATE VIEW action_recommendations AS
SELECT
    customer_id,
    churn_risk,
    CASE
        WHEN churn_risk = 'HIGH' THEN 'Send 20% retention coupon'
        WHEN rain_purchase_pct > 50 THEN 'Target for weather-based promotions'
        ELSE 'Standard marketing campaign'
    END AS recommended_action,
    CASE
        WHEN churn_risk = 'HIGH' THEN 'Immediate'
        ELSE 'Normal'
    END AS priority
FROM customer_knowledge;
"""
```

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. DIKW 계층별 특성 비교

| 비교 항목 | Data | Information | Knowledge | Wisdom |
|:---|:---|:---|:---|:---|
| **정의** | 원시 팩트 | 맥락화된 데이터 | 조직화된 정보 | 통찰력 있는 지식 |
| **질문** | "무엇이?" | "언제, 어디서?" | "어떻게?" | "왜?" |
| **가치 밀도** | 낮음 (Low) | 중간 (Medium) | 높음 (High) | 최고 (Highest) |
| **처리 방식** | 수집, 저장 | 정제, 통합 | 분석, 모델링 | 추론, 판단 |
| **주요 기술** | DBMS, Data Lake | ETL, DW | ML/AI, BI | DSS, Expert System |
| **인간 개입** | 최소 | 중간 | 높음 | 최대 |
| **시간 지향** | 과거 (Past) | 과거-현재 | 현재 | 미래 (Future) |
| **형태** | 숫자, 텍스트 | 보고서, 그래프 | 규칙, 모델 | 전략, 정책 |

#### 2. 현대 데이터 스택과 DIKW 매핑

| DIKW 계층 | 데이터 스택 구성요소 | 대표 도구 |
|:---|:---|:---|
| **Data** | 데이터 수집, 저장 | Kafka, S3, HDFS, PostgreSQL |
| **Information** | ETL/ELT, 데이터 웨어하우스 | Snowflake, BigQuery, dbt |
| **Knowledge** | BI, ML/AI 플랫폼 | Tableau, Looker, SageMaker |
| **Wisdom** | 의사결정 지원, 자동화 | Salesforce Einstein, UiPath |

#### 3. 과목 융합 관점 분석

- **[데이터베이스 융합] 데이터 독립성**: DIKW 계층은 데이터베이스의 3단계 스키마와 유사하게 하위 계층의 변화가 상위 계층에 미치는 영향을 최소화하는 구조입니다. 원시 데이터 스키마가 변경되어도 정보 계층의 뷰는 독립적으로 유지될 수 있습니다.

- **[AI/ML 융합] 지식 자동화**: 머신러닝은 Information → Knowledge 변환을 자동화합니다. 딥러닝은 이미지, 텍스트 등 비정형 데이터에서 직접 패턴을 추출하여 Knowledge 계층을 효율화합니다.

- **[보안 융합] 데이터 거버넌스**: 각 계층에서 적절한 접근 제어가 필요합니다. 원시 데이터는 개인정보 포함 가능성이 높고, 지혜 계층의 의사결정은 윤리적 검토가 필요합니다.

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

- **시나리오 1: BI 도구 도입 실패 분석**
  - 상황: 회사가 고가의 BI 도구를 도입했지만 활용도가 저조함.
  - 판단: 문제는 도구가 아니라 Data → Information 변환 단계의 부실에 있을 가능성이 높습니다. 데이터 품질 문제, 메타데이터 부재, 표준화 미흡을 먼저 해결해야 합니다. "Garbage In, Garbage Out" 원칙을 상기해야 합니다.

- **시나리오 2: AI 프로젝트 실패 원인 진단**
  - 상황: 머신러닝 모델의 정확도가 낮음.
  - 판단: Knowledge 계층(모델링)만 집중하고 Information 계층(데이터 품질)을 간과했을 수 있습니다. 피처 엔지니어링과 데이터 전처리에 80%의 시간을 투자해야 한다는 업계 관행을 따라야 합니다.

- **시나리오 3: 데이터 조직 구조 설계**
  - 상황: 데이터 조직의 역할과 책임 정의 필요.
  - 판단: DIKW 계층별로 역할을 분담합니다. Data Engineering (Data→Info), Data Analytics (Info→Knowledge), Data Science (Knowledge→Wisdom)로 팀을 구성하고 협업 프로세스를 정의합니다.

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **데이터 품질 관리**: Data 계층의 품질이 Information 계층의 품질을 결정
- [ ] **메타데이터 관리**: 각 계층의 데이터에 대한 문서화와 계보(Lineage) 추적
- [ ] **피드백 루프**: Wisdom → Data로의 피드백으로 시스템 개선
- [ ] **조직 역량**: 각 계층별 전문 인력 확보와 교육
- [ ] **거버넌스**: 계층 간 이동 시 데이터 보안 및 컴플라이언스 준수

#### 3. 안티패턴 (Anti-patterns)

- **데이터 수집 중독**: Data 계층만 확장하고 Information/Knowledge 변환을 등한시하면 "데이터 묘지"가 됩니다.
- **분석 마비(Analysis Paralysis)**: Knowledge 계층에서 과도한 분석만 하고 Wisdom(행동)으로 전환하지 못하면 ROI가 발생하지 않습니다.
- **툴 중심 사고**: 계층별 목적보다 특정 도구에 집착하면 비즈니스 가치 창출에 실패합니다.

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 효과 영역 | 내용 | 개선 지표 |
|:---|:---|:---|
| **의사결정 품질** | 데이터 기반 객관적 판단 | 의사결정 오류 40% 감소 |
| **운영 효율성** | 자동화된 정보 처리 | 분석 리드타임 60% 단축 |
| **경쟁력** | 시장 인사이트 선점 | 대응 속도 3배 향상 |
| **위험 관리** | 패턴 기반 위험 예측 | 리스크 사전 감지 80% |

#### 2. 미래 전망

DIKW 모델은 **AI의 발전과 함께 재정의**되고 있습니다:

1. **AutoML의 부상**: Information → Knowledge 변환이 자동화되어, 도메인 전문가가 AI를 쉽게 활용
2. **인과추론(Causal Inference)****: 상관관계를 넘어 인과관계 파악으로 Knowledge 품질 향상
3. **Augmented Intelligence**: 인간의 Wisdom과 AI의 Knowledge 처리 속도가 결합
4. **실시간 지혜**: 스트림 처리 기술로 Data→Wisdom 변환의 지연 시간 최소화

#### 3. 참고 표준

- **ISO/IEC 20547**: Big Data Reference Architecture
- **DMBOK (Data Management Body of Knowledge)**: DAMA International
- **Russell Ackoff's Systems Thinking**: From Data to Wisdom (1989)

---

### 관련 개념 맵 (Knowledge Graph)

- **[데이터베이스 정의](@/studynotes/5_database/1_relational/2_database_definition.md)**: Data 계층의 저장 및 관리 시스템.
- **[데이터 웨어하우스](@/studynotes/5_database/4_dw_olap/data_warehouse_olap.md)**: Information 계층의 통합 저장소.
- **[OLAP](@/studynotes/5_database/4_dw_olap/data_warehouse_olap.md)**: Knowledge 계층의 다차원 분석.
- **[데이터 마이닝](@/studynotes/5_database/_keyword_list.md)**: Information → Knowledge 패턴 추출.
- **[비즈니스 인텔리전스](@/studynotes/5_database/_keyword_list.md)**: Knowledge 시각화 및 보고.

---

### 어린이를 위한 3줄 비유 설명

1. **재료 모으기**: 데이터는 장보기에서 사 온 야채와 고기예요. 아직 요리가 아니라 그냥 재료들이에요.
2. **요리 만들기**: 정보는 재료를 손질해서 요리한 것이고, 지식은 요리 레시피를 익히는 거예요.
3. **미식 평론가**: 지혜는 어떤 요리를 언제 먹으면 좋은지 아는 미식 평론가의 조언이에요!
