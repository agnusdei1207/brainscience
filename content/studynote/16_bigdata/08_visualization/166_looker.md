+++
weight = 166
title = "166. Looker / Looker Studio — LookML 시맨틱 레이어 BI"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Looker / Looker Studio — LookML 시맨틱 레이어 BI은(는) 복잡한 대규모 데이터를 사람이 빠르게 해석하고 행동으로 옮기게 만드는 시각화 핵심 원리 또는 도구다.
> **비유**: 복잡한 계기판 수치를 한눈에 읽히는 조종석 화면으로 바꾸는 일과 같다.

📝 모범 답안

## 1. 개요 및 필요성

### 지표 불일치(Metric Sprawl) 문제

현대 기업에서 "전환율"이라는 단순한 지표도 팀마다 다르게 계산된다:
- 마케팅팀: 클릭 대비 가입 완료
- 영업팀: 상담 신청 대비 계약 체결
- 제품팀: 방문 대비 핵심 기능 사용
- 경영진: 방문 대비 유료 전환

데이터가 분산되고 각 팀이 자체 SQL을 작성하면 이 불일치가 심화된다. **Looker의 LookML 시맨틱 레이어**는 이 문제를 "비즈니스 정의를 코드로 관리"하여 해결한다.

---

## 2. 구성요소

### Looker 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Looker 아키텍처                           │
├──────────────────────────────────────────────────────────────┤
│  비즈니스 사용자                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Explore UI: 드래그앤드롭 (SQL 없이 분석)             │   │
│  │  Dashboard: 공유 대시보드                             │   │
│  │  Look: 저장된 분석 쿼리                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                   │
│  LookML 시맨틱 레이어                                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  models/: 데이터베이스 연결 + Explore 정의            │   │
│  │  views/: 테이블/뷰 + 비즈니스 로직 정의               │   │
│  │    - dimensions: 필터 가능한 속성                     │   │
│  │    - measures: 집계 지표 (매출, 사용자 수)            │   │
│  │    - derived_table: LookML 기반 계산 테이블           │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │ SQL 자동 생성                     │
│  데이터 소스 (항상 Live)                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  BigQuery / Snowflake / Redshift / PostgreSQL        │   │
│  │  (데이터 복사 없음 — 원본 직접 쿼리)                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### LookML 핵심 구조

```yaml

view: orders {
  sql_table_name: "public"."orders" ;;  # 원본 테이블 매핑

  # Dimension: 필터·그룹화 가능한 속성
  dimension: order_id {
    type: number
    sql: ${TABLE}.order_id ;;
    primary_key: yes
  }

  dimension: status {
    type: string
    sql: ${TABLE}.status ;;
  }

  # Measure: 집계 지표 (비즈니스 정의가 여기에)
  measure: total_revenue {
    type: sum
    sql: ${TABLE}.amount ;;
    value_format_name: usd
    description: "완료된 주문의 총 매출 (취소·환불 제외)"
    filters: [status: "completed"]  # 비즈니스 로직 내장
  }

  measure: average_order_value {
    type: average
    sql: ${TABLE}.amount ;;
  }
}
```

### Looker vs Looker Studio 비교

| 차원 | Looker | Looker Studio |
|:---|:---|:---|
| **가격** | 엔터프라이즈 (고가) | 무료 |
| **시맨틱 레이어** | LookML (강력한 거버넌스) | 없음 |
| **SQL 사용** | LookML이 자동 생성 | 사용자 정의 SQL 가능 |
| **데이터 소스** | 주요 데이터베이스 | 800+ 커넥터 |
| **주요 사용자** | 데이터 팀 + 비즈니스 | 비기술 사용자 |
| **복잡도** | 높음 (LookML 학습 필요) | 낮음 (드래그앤드롭) |

---

## 3. 구조 및 원리

**핵심 조건**: 표현 정확성, 인지 부하, 질의 성능, 상호작용성을 함께 균형시켜야 한다.

동작 순서:
### Looker Block: 사전 구축 LookML 템플릿

Looker Blocks는 일반적인 플랫폼 데이터를 위한 사전 제작된 LookML 솔루션:
- **Salesforce Block**: CRM 데이터 분석 템플릿
- **Google Analytics Block**: 웹 분석 템플릿
- **Stripe Block**: 결제 데이터 분석
- **Snowplow Block**: 이벤트 추적 데이터

이를 가져와 수정하면 처음부터 LookML을 작성하는 시간을 대폭 절약한다.

### Looker + BigQuery BI Engine

BigQuery BI Engine을 사용하면 BigQuery에 저장된 데이터를 인메모리 캐싱으로 서브세컨드 응답으로 Looker에서 조회할 수 있다. Google Cloud 생태계 내에서 Looker + BigQuery + BI Engine의 조합이 성능·거버넌스의 최적 패키지다.

---

## 4. 비교 및 연결

### LookML 거버넌스 모범 사례

```yaml

measure: active_users {
  type: count_distinct
  sql: ${TABLE}.user_id ;;
  filters: [
    last_login_date: "30 days"  # "활성"의 정의가 여기에
  ]
  description: "최근 30일 내 1회 이상 로그인한 사용자 수"
  group_label: "사용자 지표"
}
```

### API-First 설계와 임베디드 분석

Looker는 API-First 철학으로 설계되어, 자사 애플리케이션 내에 Looker 대시보드를 **임베딩(Embedded Analytics)**하는 것이 주요 활용 사례다:
- iFrame 임베딩: 가장 간단한 방식
- Signed Embed: JWT 기반 인증으로 사용자별 필터 적용
- Looker API: 프로그래밍 방식으로 데이터·시각화 접근

---

## 5. 실무 적용 및 판단

### Looker 도입 효과

| 영역 | 효과 |
|:---|:---|
| **지표 일관성** | 전사 모든 팀이 동일한 비즈니스 정의 사용 |
| **SQL 거버넌스** | LookML이 SQL 생성 → SQL 오류·불일치 제거 |
| **보안** | 원본 데이터 복사 없음 → 데이터 유출 위험 감소 |
| **확장성** | 새 팀·프로젝트 온보딩 시 기존 LookML 재사용 |

### 결론

Looker는 **BI 거버넌스의 미래 표준**이다. 데이터가 분산되고 팀이 늘어날수록 지표 불일치 문제가 심화되는데, LookML 시맨틱 레이어는 이를 코드 수준에서 해결한다. 다만 LookML 전문 인력 확보와 초기 모델링 투자가 필요하므로, 조직의 데이터 성숙도와 팀 역량을 고려하여 도입 시점을 결정해야 한다.

---

## 6. 기대효과 및 결론

Looker / Looker Studio — LookML 시맨틱 레이어 BI은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 시각화의 본질은 더 많은 그래프가 아니라 더 빠르고 정확한 판단을 가능하게 하는 정보 구조다.

---

## 7. 발전 흐름도

```text
[SQL (SQL)]
    │
    ▼
[LookML (LookML)]
    │
    ▼
[Looker (Looker)]
    │
    ▼
[셀프서비스 BI (Self-Service BI)]
```

이 흐름도는 SQL에서 LookML과 Looker를 거쳐 셀프서비스 BI로 발전하는 분석 흐름을 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| LookML | 핵심 기술 | 비즈니스 로직 코드화 시맨틱 레이어 |
| Dimension | LookML 구성 | 필터·그룹화 속성 정의 |
| Measure | LookML 구성 | 비즈니스 지표 집계 정의 (비즈니스 로직 내장) |
| Explore | LookML 구성 | 조인 관계 + 분석 진입점 정의 |
| Looker Studio | 관련 제품 | 무료, 비기술용 빠른 시각화 |
| Metric Sprawl | 해결 문제 | 팀별 다른 지표 정의로 인한 불일치 |
| BigQuery BI Engine | 성능 최적화 | Looker + BigQuery 인메모리 가속 |
