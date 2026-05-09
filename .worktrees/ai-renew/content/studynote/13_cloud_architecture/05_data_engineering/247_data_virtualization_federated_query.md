+++
weight = 247
title = "247. 데이터 가상화 (Data Virtualization) - 연방 쿼리"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터 가상화(Data Virtualization)는 물리적으로 분산된 여러 데이터 소스를 **복사·이동 없이 연방 쿼리(Federated Query) 엔진 하나로 실시간 JOIN·집계**하는 기술이다.
> 2. **가치**: ETL 파이프라인과 중복 데이터 저장 없이 **원본 소스에 직접 쿼리**하므로 데이터 이동 비용·지연·일관성 문제를 동시에 해결하며, 새 소스 연결이 ETL 개발 없이 즉시 가능하다.
> 3. **판단 포인트**: AWS Athena·Presto·Trino 기반의 연방 쿼리는 **분석 워크로드에는 강력**하지만, 복잡한 대규모 집계나 빈번한 조인은 원본 소스 부하를 유발하므로 **쿼리 유형과 소스 특성에 따른 선택적 적용**이 필요하다.

---

## Ⅰ. 개요 및 필요성

전통적으로 여러 소스의 데이터를 함께 분석하려면 ETL로 중앙에 복사해야 했다. 이 방식은:
- **지연**: 복사 완료까지 수시간~수일 소요
- **비용**: 대용량 데이터 이동 네트워크·스토리지 비용
- **일관성**: 복사 시점 이후 원본 변경 미반영
- **복잡성**: 소스별 ETL 파이프라인 설계·유지

데이터 가상화는 데이터를 원본 위치에 두고, 쿼리 실행 시점에 실시간으로 각 소스에 접근하는 방식으로 이 문제를 해결한다.

```
[데이터 가상화 개념]
분석가 SQL:
SELECT c.name, SUM(o.amount)
FROM crm.customers c          -- Salesforce에 있음
JOIN s3_lake.orders o          -- AWS S3에 있음
ON c.id = o.customer_id
WHERE c.country = 'KR'
GROUP BY c.name

연방 쿼리 엔진 처리:
① Salesforce → "SELECT id, name FROM customers WHERE country='KR'"
② AWS S3    → "SELECT customer_id, amount FROM orders"
③ 결과 병합 → JOIN + GROUP BY 실행
④ 분석가에게 통합 결과 반환

데이터 이동: 없음 (원본 그대로)
```

📢 **섹션 요약 비유**: 데이터 가상화는 마트 여러 곳의 가격을 비교하는 쇼핑 앱이다. 각 마트(데이터 소스)에 직접 방문(쿼리)해서 가격을 가져오고, 앱(연방 쿼리 엔진)이 비교표(결과)를 만들어준다. 가격을 앱 서버에 미리 복사하지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 연방 쿼리 엔진 아키텍처

```
┌────────────────────────────────────────────────────────────────┐
│                   연방 쿼리 엔진 (Presto/Trino)                 │
│                                                                │
│  SQL 입력                                                      │
│     │                                                          │
│     ▼                                                          │
│  ┌─────────────────────────────────────────────┐              │
│  │  쿼리 파서 → 논리 플랜 → 최적화기 → 물리 플랜│              │
│  │                                             │              │
│  │  Pushdown: 각 소스에 적합한 쿼리 변환        │              │
│  │   - S3 → Parquet 컬럼 프루닝, 파티션 필터   │              │
│  │   - MySQL → SQL WHERE 절                    │              │
│  │   - Elasticsearch → JSON 쿼리               │              │
│  └────────────────┬────────────────────────────┘              │
│                   │ 분산 실행                                   │
│    ┌──────────────┼──────────────┐                            │
│    ▼              ▼              ▼                            │
│  Worker 1       Worker 2       Worker 3                       │
│  (S3 스캔)      (MySQL 조회)   (중간 결과 집계)                │
└────────────────────────────────────────────────────────────────┘

커넥터 (Connector) 시스템:
  Hive Connector  → S3/HDFS Parquet/ORC
  MySQL Connector → MySQL, PostgreSQL
  Elasticsearch   → ES 인덱스
  Kafka Connector → Kafka 토픽
  Iceberg Connector → Apache Iceberg 테이블
```

### Predicate Pushdown (조건 푸시다운)

```
[최적화 핵심: Pushdown]
SQL: SELECT * FROM orders WHERE date = '2024-01-15' AND amount > 10000

Without Pushdown:
  S3에서 전체 orders 데이터 읽기 (수백GB)
  → 엔진 메모리에서 필터링

With Predicate Pushdown:
  S3에 "date=2024-01-15 파티션만 읽기" 요청
  → Parquet 통계로 amount > 10000 행만 읽기
  → 수십MB만 읽음 (수십 배 효율)

효과: I/O 90%+ 절감, 소스 시스템 부하 최소화
```

### AWS Athena 특성

```
[AWS Athena 아키텍처]
- 서버리스 연방 쿼리 엔진 (Presto 기반)
- S3 데이터를 SQL로 직접 쿼리
- Glue Data Catalog를 메타스토어로 사용
- 스캔된 데이터 1TB당 $5 과금
- 연방 쿼리: RDS, Redshift, DynamoDB, Elasticsearch도 쿼리

사용 사례:
  - S3의 로그 파일 임시 분석
  - 데이터 레이크의 탐색적 쿼리
  - 멀티소스 연방 분석 (파이프라인 없이)
```

📢 **섹션 요약 비유**: Predicate Pushdown은 도서관에서 책을 전부 가져오지 않고 "1월 서가의 소설만"이라고 요청하는 것이다. 전체 도서관(S3)을 다 가져오지 않고, 조건에 맞는 책(데이터)만 가져와서 비교한다.

---

## Ⅲ. 비교 및 연결

### 주요 연방 쿼리 엔진 비교

| 엔진 | 유형 | 특징 | 적합 사례 |
|:---|:---|:---|:---|
| **AWS Athena** | 서버리스 | 과금: 스캔 바이트, S3 특화 | AWS S3 레이크 분석 |
| **Trino** | 분산 클러스터 | 오픈소스, 멀티소스 연방 | 엔터프라이즈 멀티소스 |
| **Presto** | 분산 클러스터 | Facebook 원조, Meta 대규모 | 대용량 배치 분석 |
| **Dremio** | 레이크하우스 | Arrow 가속, Apache Iceberg | 자체 완결 레이크하우스 |
| **Starburst** | Trino 관리형 | 상용 Trino, 보안+거버넌스 | 엔터프라이즈 연방 |
| **Google BigQuery Omni** | 멀티클라우드 | AWS/Azure 데이터 직접 분석 | GCP 기반 멀티클라우드 |

### 데이터 가상화 vs ETL 비교

| 비교 항목 | 데이터 가상화 | ETL |
|:---|:---|:---|
| **데이터 이동** | 없음 | 있음 |
| **데이터 신선도** | 실시간 | 배치 주기 지연 |
| **복잡 집계 성능** | 소스 부하 의존 | DW에서 최적화 |
| **개발 속도** | 빠름 (SQL만) | 느림 (파이프라인 설계) |
| **거버넌스** | 원본 정책 유지 | 복사본 별도 정책 필요 |
| **적합 사례** | 탐색 분석, 임시 쿼리 | 정기 KPI, 고성능 대시보드 |

📢 **섹션 요약 비유**: 데이터 가상화 vs ETL은 배달 앱 vs 마트 입점 차이다. 배달 앱(가상화)은 각 식당(소스)에서 직접 가져와 신선하지만, 배달 시간 변수가 있다. 마트 입점(ETL)은 미리 진열해서 빠르지만, 오래된 재고(지연)가 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Athena 연방 쿼리 예시

```sql
-- AWS Athena 연방 쿼리: S3 + RDS 동시 조회
-- data_source_name은 Athena 커넥터로 사전 설정

SELECT 
    c.customer_name,
    c.email,
    s3_orders.total_orders,
    s3_orders.total_amount
FROM 
    -- RDS PostgreSQL의 고객 정보 (Lambda 데이터 소스)
    "rds_postgresql".ecommerce.customers c
    
JOIN (
    -- S3 레이크의 주문 집계
    SELECT customer_id, 
           COUNT(*) AS total_orders,
           SUM(amount) AS total_amount
    FROM s3_lake.orders  -- Glue 카탈로그 테이블
    WHERE year = '2024'
    GROUP BY customer_id
) s3_orders ON c.id = s3_orders.customer_id

WHERE c.tier = 'VIP'
ORDER BY s3_orders.total_amount DESC
LIMIT 100;
```

### 성능 최적화 가이드

```
[연방 쿼리 최적화 원칙]
□ 필터 조건을 최대한 소스에 Pushdown
□ 크로스 소스 JOIN은 작은 테이블 기준 (Broadcast Join)
□ 집계는 가능한 한 소스에서 미리 수행
□ 자주 사용되는 연방 쿼리 결과는 Materialized View 사용
□ 소스 시스템이 허용하는 최대 병렬도 설정

[주의: 과도한 사용 금지]
- 수억 행 크로스 JOIN → 소스 시스템 과부하
- 실시간 OLTP 소스에 집계 쿼리 → 운영 서비스 영향
- 복잡한 다단계 JOIN → 네트워크 전송량 폭발
```

📢 **섹션 요약 비유**: 연방 쿼리 최적화는 회의 준비와 같다. 전체 서류(데이터)를 다 가져오지 않고, 필요한 부분만 요약해서(Pushdown) 가져오면 회의실(엔진 메모리)이 넘치지 않는다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 효과 | 내용 |
|:---|:---|
| **즉각적 데이터 접근** | ETL 파이프라인 없이 새 소스 즉시 분석 |
| **비용 절감** | 중복 데이터 저장 비용 제거 |
| **데이터 신선도** | 원본 데이터에 실시간 접근 |
| **거버넌스 단순화** | 원본 시스템의 보안·접근 제어 그대로 상속 |

### 한계 및 주의점

| 한계 | 내용 |
|:---|:---|
| **성능 의존성** | 소스 시스템 성능에 쿼리 속도 종속 |
| **복잡 집계 한계** | 대규모 크로스 소스 조인은 느리거나 불가 |
| **소스 부하** | 빈번한 연방 쿼리가 운영 DB 부하 유발 |
| **일관성** | 여러 소스 쿼리 시 시점 불일치 가능 |

📢 **섹션 요약 비유**: 데이터 가상화는 강력하지만 선택적으로 써야 한다. 마치 직접 조리 대신 배달만 주문하는 것처럼, 메뉴 수가 적고 신선함이 중요할 때(탐색 분석)는 좋지만, 매일 대량으로 같은 메뉴(정기 KPI 집계)를 주문하려면 직접 조리(ETL→DW)가 더 효율적이다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| 데이터 패브릭 | 데이터 가상화를 핵심 기술로 활용하는 아키텍처 |
| AWS Athena | 서버리스 연방 쿼리 엔진 (S3 특화) |
| Presto/Trino | 오픈소스 분산 연방 SQL 엔진 |
| ETL | 데이터 가상화와 보완·대체 관계 |
| Predicate Pushdown | 연방 쿼리 최적화의 핵심 기법 |
| 데이터 메시 | 도메인별 데이터 상품을 연방 쿼리로 접근하는 패턴 |
| AWS Glue Data Catalog | Athena의 메타스토어, 연방 쿼리 스키마 정보 |

### 👶 어린이를 위한 3줄 비유 설명
1. 데이터 가상화는 마법 거울이다. 거울(연방 쿼리 엔진)을 들여다보면 집(S3), 학교(RDS), 회사(Salesforce) 정보가 모두 보이지만, 실제로는 각 곳에서 실시간으로 정보를 가져온다.
2. Presto/Trino는 여러 나라 요리를 동시에 서빙하는 요리사다. 한국 식재료(S3), 이탈리아 식재료(MySQL), 프랑스 식재료(Elasticsearch)를 각 나라에서 가져와 한 접시에 담아준다.
3. Predicate Pushdown은 심부름을 효율적으로 하는 방법이다. "마트에서 빨간 사과만 골라와"라고 하면, 사과 전체를 가져와서 집에서 고르는 것보다 훨씬 짐이 가볍다.
