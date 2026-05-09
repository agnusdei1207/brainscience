+++
weight = 382
title = "382. ELT 클라우드 내부 변환 아키텍처 (ELT: Extract-Load-Transform)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ELT(Extract-Load-Transform)는 원시 데이터를 클라우드 DW에 먼저 적재한 뒤, DW 내부 MPP(Massively Parallel Processing) 엔진으로 변환을 수행하는 현대적 패러다임이다.
> 2. **가치**: 별도 변환 서버가 불필요하고 DW 스케일아웃으로 변환 성능을 탄력적으로 확장할 수 있어, 클라우드 환경에서 ETL 대비 TCO(Total Cost of Ownership)가 낮다.
> 3. **판단 포인트**: 원시 데이터 보존(Schema-on-Read), 변환 재실행 가능성, dbt 기반 SQL 변환 관리가 ELT 도입의 핵심 판단 기준이다.

## Ⅰ. 개요 및 필요성

ELT(Extract-Load-Transform)는 데이터를 추출(E)→ 대상 스토리지에 적재(L)→ 그 안에서 변환(T)하는 순서로 동작한다. Snowflake·Google BigQuery·Amazon Redshift 등 클라우드 DW가 보유한 MPP 엔진이 수백 노드에서 SQL을 병렬 실행함으로써, 외부 ETL 서버보다 DW 내부 변환이 더 경제적이고 빠른 경우가 많아졌다.

원시 데이터를 Raw Layer에 보존하면 재처리(Reprocessing)가 언제든 가능하고, 요구사항 변화에 유연하게 대응할 수 있다는 것이 ELT의 철학적 장점이다.

📢 **섹션 요약 비유**: ELT는 원재료를 창고(DW)에 넣어두고 창고 안 대형 기계로 그 자리에서 가공하는 것 — 외부 공장(ETL 서버)이 필요 없다.

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────┐  Extract     ┌─────────────────────────────────────────────────┐
│  Source      │─────────────>│           Cloud Data Warehouse                  │
│  (SaaS/DB)   │ (Fivetran,   │  ┌──────────────┐  Transform   ┌─────────────┐  │
│              │  Airbyte)    │  │  Raw Layer   │──(dbt/SQL)──>│  Mart Layer │  │
└──────────────┘              │  │  (Immutable) │              │  (Curated)  │  │
                              │  └──────────────┘              └─────────────┘  │
                              │         MPP Engine (Snowflake / BigQuery)        │
                              └─────────────────────────────────────────────────┘
```

| 레이어 | 역할 | 도구 예시 |
|:---|:---|:---|
| Raw Layer | 원시 데이터 불변 보존 | S3, GCS, DW Raw Schema |
| Staging Layer | 타입 캐스팅·중복 제거 | dbt staging models |
| Mart Layer | 비즈니스 로직·집계 | dbt mart models |
| Serving Layer | BI 도구 연결 | Looker, Tableau |

📢 **섹션 요약 비유**: dbt는 DW 내부의 요리사 — 식재료(Raw)를 받아 레시피(SQL)대로 완성 요리(Mart)를 만든다.

## Ⅲ. 비교 및 연결

| 항목 | ETL | ELT |
|:---|:---|:---|
| 변환 시점 | 적재 전 | 적재 후 |
| 인프라 | 전용 변환 서버 필요 | DW 엔진 재활용 |
| 원시 데이터 보존 | 옵션 | 기본 |
| 재처리 용이성 | 낮음 | 높음 |
| 비용 구조 | 서버 고정비 | DW 쿼리 종량제 |

📢 **섹션 요약 비유**: ETL은 인쇄 전 편집, ELT는 인쇄 후 편집 — 편집을 나중에 하면 원본을 항상 다시 활용할 수 있다.

## Ⅳ. 실무 적용 및 기술사 판단

**의사결정 포인트**:
- 클라우드 DW 보유 + SQL 역량 있음: ELT + dbt 채택
- 복잡한 비SQL 로직(ML 전처리, 바이너리 변환): ETL 혼용 필요
- 데이터 거버넌스 강화: Raw Layer 보존으로 감사(Audit) 추적 용이
- 비용 주의: BigQuery On-demand는 대규모 변환 시 비용 급증 → Slots 예약 고려

📢 **섹션 요약 비유**: ELT 비용은 택시 미터기 — 움직일수록(쿼리할수록) 요금이 오르므로 예약제(Slots)가 대량 사용 시 유리하다.

## Ⅴ. 기대효과 및 결론

ELT는 클라우드 DW의 탄력적 확장성을 활용하여 변환 인프라 관리 부담을 제거하고, 원시 데이터 보존을 통한 재처리 유연성을 제공한다. dbt와 결합하면 SQL 기반 변환 코드의 버전 관리·테스트·문서화가 가능하여 데이터 신뢰성이 높아진다. 단, 클라우드 DW 종속성과 쿼리 비용 증가가 한계이므로 쿼리 최적화와 파티셔닝 전략이 필수 전제 조건이다.

📢 **섹션 요약 비유**: ELT는 강력한 DW 엔진을 빌려 타는 것 — 내 차(ETL 서버)를 살 필요 없지만, 렌트비(쿼리 비용)는 꼼꼼히 관리해야 한다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| dbt (data build tool) | ELT 변환 레이어 | SQL 기반 모듈화 변환 관리 |
| Fivetran / Airbyte | EL 자동화 | SaaS 소스 커넥터 기반 적재 자동화 |
| MPP (Massively Parallel Processing) | 변환 엔진 | 수백 노드 병렬 SQL 실행 |
| Raw Layer | 원시 보존 레이어 | 재처리·감사 기반 불변 원본 |
| Schema-on-Read | ELT 철학 | 읽을 때 스키마 해석으로 유연성 극대화 |

### 👶 어린이를 위한 3줄 비유 설명

1. ELT는 사진을 먼저 앨범에 넣어두고(적재), 나중에 포토샵으로 편집(변환)하는 것 — 원본이 항상 남아 있어.
2. dbt는 앨범 안에 있는 편집 앱 — 밖에 있는 컴퓨터(ETL 서버)가 필요 없어.
3. 클라우드 DW는 초고성능 인화소 — 버튼 하나로 10만 장을 동시에 처리할 수 있어!
