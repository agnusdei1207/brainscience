+++
weight = 178
title = "178. 모던 데이터 스택 (MDS, Modern Data Stack) — Fivetran+Snowflake+dbt+Tableau"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)

- MDS (Modern Data Stack)는 클라우드 네이티브 구성 요소를 결합한 데이터 인프라로, Fivetran/Airbyte(ELT 수집) + Snowflake/BigQuery(클라우드 DW) + dbt(SQL 변환) + Tableau/Looker(BI)의 조합이 사실상 표준으로 자리잡았다.
- ETL (Extract-Transform-Load)에서 ELT (Extract-Load-Transform)로의 전환이 MDS의 핵심으로, 클라우드 DW의 강력한 SQL 처리 능력을 변환 계층으로 활용한다.
- MDS의 한계는 실시간 처리 지원 부족, 대용량 시 높은 클라우드 비용, 벤더 종속이며, 이를 보완하기 위해 Streaming MDS (Kafka + Materialize/RisingWave)가 부상 중이다.

---

## Ⅰ. 개요 및 필요성

### 1-1. MDS의 등장 배경

2016년 이후 클라우드 DW (Snowflake, BigQuery)의 성숙, Fivetran의 간편한 커넥터 서비스, dbt의 Git 기반 SQL 버전 관리가 결합되면서 스타트업도 수주 내에 엔터프라이즈급 데이터 인프라를 구축할 수 있게 됐다.

### 1-2. MDS vs 전통 데이터 스택

| 항목 | 전통 스택 | 모던 데이터 스택 |
|:---|:---|:---|
| 수집 방식 | ETL (Informatica, SSIS) | ELT (Fivetran, Airbyte) |
| 변환 위치 | 수집 전 (ETL 서버) | 수집 후 (DW 내부, dbt) |
| 저장소 | 온프레미스 DW | 클라우드 DW |
| 구축 기간 | 수개월 | 수주 |
| 비용 모델 | CapEx 중심 | OpEx (SaaS 구독) |

> 📢 **섹션 요약 비유**: MDS는 요리사(팀)가 재료 손질(ETL 서버)을 직접 하지 않고, 손질된 재료(ELT)를 받아 자신의 주방(DW)에서 원하는 대로 요리(dbt 변환)하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. MDS 핵심 파이프라인

```
┌─────────────────────────────────────────────────────────────┐
│                    데이터 소스                               │
│  Salesforce  │  MySQL  │  Google Ads  │  Stripe  │  ...     │
└────────────────────────┬────────────────────────────────────┘
                         │ EL (Extract-Load, 원본 그대로)
                         ▼
            ┌─────────────────────────┐
            │   Fivetran / Airbyte    │
            │   (300+ 커넥터, 자동    │
            │    스키마 적응, CDC)     │
            └────────────┬────────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │  Cloud Data Warehouse   │
            │  Snowflake / BigQuery   │
            │  Redshift / Databricks  │
            │  ┌─────────────────┐    │
            │  │  Raw Layer      │    │
            │  │  Staging Layer  │    │ ← dbt 변환
            │  │  Mart Layer     │    │
            │  └─────────────────┘    │
            └────────────┬────────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │  BI / 시각화            │
            │  Tableau / Looker       │
            │  Metabase / PowerBI     │
            └─────────────────────────┘
```

### 2-2. dbt (data build tool) 핵심 개념

| 개념 | 설명 |
|:---|:---|
| Model | SELECT 문으로 정의된 변환 단위 (`.sql` 파일) |
| Ref | 모델 간 의존성 선언 (`{{ ref('stg_orders') }}`) |
| Test | 데이터 품질 자동 검증 (Not Null, Unique, FK) |
| Lineage | 자동 생성되는 시각적 의존성 그래프 |
| Macro | Jinja2 템플릿 기반 재사용 가능 SQL 함수 |

### 2-3. ELT vs ETL

- **ETL**: 수집 단계에서 변환 → 변환 로직 변경 시 재파이프라인 필요
- **ELT**: 원본 그대로 적재 후 DW 안에서 변환 → 유연성·재처리 용이

> 📢 **섹션 요약 비유**: dbt는 데이터 팀의 Git이다. SQL을 코드처럼 버전 관리하고, 테스트를 자동화하며, 팀 간 협업을 가능하게 한다.

---

## Ⅲ. 비교 및 연결

### MDS 핵심 도구 비교

| 카테고리 | 도구 | 차별점 |
|:---|:---|:---|
| 수집 | Fivetran | 완전 관리형, 높은 비용 |
| 수집 | Airbyte | 오픈소스, 커스텀 커넥터 가능 |
| DW | Snowflake | 멀티클라우드, 데이터 공유 |
| DW | BigQuery | 서버리스, ML 통합 (BQML) |
| 변환 | dbt Core | 오픈소스 CLI |
| 변환 | dbt Cloud | 관리형 서비스, IDE, 스케줄러 |
| BI | Looker | LookML 시맨틱 레이어 |
| BI | Metabase | 오픈소스, 빠른 셀프서비스 |

### Semantic Layer (시맨틱 레이어)

비즈니스 메트릭 정의를 BI 도구와 분리하는 계층. dbt Semantic Layer (MetricFlow), Looker의 LookML, Cube.js가 대표적. "Revenue" 메트릭이 팀마다 다르게 정의되는 문제(Metric Sprawl)를 해결.

> 📢 **섹션 요약 비유**: Semantic Layer는 회사의 공식 용어사전이다. "매출"이 팀마다 다른 계산식을 쓰는 혼란을 방지하고, 모든 팀이 같은 정의를 쓰게 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. MDS 도입 단계

1. **Phase 1**: Fivetran으로 주요 SaaS 소스 자동 수집, BigQuery 적재
2. **Phase 2**: dbt로 Staging → Mart 변환, Git 기반 버전 관리
3. **Phase 3**: Looker/Tableau 연결, 전사 대시보드 구축
4. **Phase 4**: Semantic Layer 도입, 메트릭 표준화

### 4-2. MDS의 한계와 보완

- **실시간 부족**: Kafka + Materialize/RisingWave로 스트리밍 레이어 추가
- **비용 급증**: 쿼리 최적화(파티셔닝, 클러스터링), dbt 증분(Incremental) 모델
- **벤더 종속**: Apache Iceberg 오픈 포맷 채택, 오픈소스 대안(Trino, dbt Core) 병행

### 4-3. 기술사 시험 포인트

- MDS의 핵심 패러다임 전환: ETL → ELT, CapEx → SaaS OpEx
- dbt의 위치: 처리 레이어의 현대화, DataOps 구현
- Reverse ETL: DW 분석 결과 → CRM/마케팅 도구로 역수출 (Census, Hightouch)

> 📢 **섹션 요약 비유**: Reverse ETL은 데이터 웨어하우스에서 CRM으로 분석 결과를 역수출하는 것이다. 마치 연구소에서 만든 신제품 정보를 영업팀에 전달하는 것처럼.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 구축 속도 | 수개월 → 수주로 데이터 인프라 구축 기간 단축 |
| 데이터 민주화 | SQL 아는 분석가라면 누구나 데이터 변환·분석 가능 |
| 품질 자동화 | dbt 테스트로 파이프라인 품질 자동 검증 |

MDS는 소규모 스타트업부터 중견 기업까지 빠르게 데이터 인프라를 구축하는 검증된 방법론이다. 기술사 관점에서 MDS 도입 제안 시, SaaS 비용 구조의 장기 시뮬레이션과 벤더 종속 완화 전략을 함께 제시해야 한다.

> 📢 **섹션 요약 비유**: MDS는 인테리어 패키지 서비스처럼, 각 영역의 전문가(Fivetran, dbt, Snowflake)가 모여 빠르게 완성된 집을 만들어준다. 직접 자재 구매부터 시공까지 할 필요가 없다.

---

### 📌 관련 개념 맵

| 개념 | 관련 기술 | 연결 포인트 |
|:---|:---|:---|
| ELT | ETL 진화, dbt | 클라우드 DW 활용 변환 |
| Semantic Layer | LookML, MetricFlow | 메트릭 표준화 |
| Reverse ETL | Census, Hightouch | DW → 운영 시스템 역수출 |
| DataOps | CI/CD, dbt | 데이터 파이프라인 DevOps |
| Metric Sprawl | 거버넌스 | 메트릭 분산 정의 문제 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[:---]
    │
    ▼
[ELT]
    │
    ▼
[Semantic Layer]
    │
    ▼
[Reverse ETL]
    │
    ▼
[DataOps]
    │
    ▼
[Metric Sprawl]
```

이 흐름도는 :---에서 출발해 Metric Sprawl까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. MDS는 레고 블록처럼 각 전문 도구들을 조립해서 데이터 인프라를 빠르게 만드는 방법이에요.
2. dbt는 데이터 팀의 요리 레시피북처럼, SQL 변환 방법을 기록하고 공유해서 모두가 같은 방식으로 요리하게 해요.
3. Semantic Layer는 회사 공식 단어장처럼, "매출"이 뭔지 모든 팀이 같은 의미로 쓰게 통일해줘요.
