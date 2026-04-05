+++
title = "312. 데이터 패브릭 (Data Fabric)"
weight = 4312
+++

> **💡 핵심 인사이트**
> 데이터 패브릭(Data Fabric)은 **"AI/ML 기반의 자동화된 데이터 통합 및 관리 레이어를 통해, 다양한 소스의 데이터를物理적 이동 없이 논리적으로 연결하는 중앙 집중형 메타데이터 아키텍처"**입니다.
> Data Mesh가 "도메인에 데이터 소유권을 분산"한다면, Data Fabric은 **"중앙에서 AI가 데이터의 흐름, 변환, 품질을 자동 관리"**한다는 점에서根本적으로 다른 철학을 가집니다. Gartner가 2021~2022년 Top Strategic Technology Trend로 선정하며 주목받았습니다.

---

## Ⅰ. Data Fabric의 탄생 배경: 데이터 복잡성의 폭발

현대 기업 데이터 환경의 현실:

```
[기업 데이터環境の複雑性]

  - ERP (SAP, Oracle)        ─┐
  - CRM (Salesforce)          ├─► 수십 개의 데이터 소스
  - HR 시스템 (Workday)       │    + API, 파일, 로그, 센서 데이터
  - MES (제조 실행 시스템)     │    = 데이터 팀의 70%가
  - IoT 센서 (백만 개)        │      "데이터 통합"에만 소요
  - SNS, 웹 로그, ...        ─┘
                                   │
  [문제]                            ▼
  각 소스마다 다른 포맷, 다른 주기, 다른 의미
  → 데이터 통합에 엄청난 수작업 + 유지보수 비용
```

Data Fabric은 이 **"데이터 통합의 피로"**를 AI 기반 자동화로 해결하겠다는愿景입니다.

---

## Ⅱ. Data Fabric의 핵심 구성 요소

```
[Data Fabric 아키텍처]

┌─────────────────────────────────────────────────────────────┐
│                    Data Fabric Layer                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Knowledge Graph (지식 그래프)            │   │
│  │   - 데이터 자산 간 관계를 노드-엣지로 모델링           │   │
│  │   - "주문ID → 주문테이블 → 고객ID → 고객테이블"       │   │
│  │   - 데이터 기원(Lineage) 자동 추적                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Semantic │  │ Active   │  │ Data     │  │ AI-based │     │
│  │ Enreach-│  │ Metadata │  │ Integra- │  │Governance│     │
│  │ ment    │  │ Manager  │  │ tion     │  │ Engine   │     │
│  │ (의미   │  │ (메타    │  │ (연결    │  │ (자동    │     │
│  │ 网罗)   │  │ 管理)    │  │ 자동화)  │  │ 품질관리) │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────┘
           │               │               │
           ▼               ▼               ▼
    ┌───────────┐  ┌───────────┐  ┌───────────┐
    │ ERP (SAP) │  │ CRM (SF)  │  │ Cloud DW  │
    └───────────┘  └───────────┘  └───────────┘
```

### 지식 그래프 (Knowledge Graph): Data Fabric의 핵심

지식 그래프는 데이터 자산 간의 **의미론적 관계(Semantic Relationships)**를 그래프 구조로 표현합니다.

```json
// 지식 그래프 노드 예시
{
  "node": "orders_table",
  "type": "Table",
  "attributes": {
    "schema": "public",
    "database": "warehouse_db",
    "owner": "orders_team",
    "rowCount": 15000000,
    "lastUpdated": "2024-01-15"
  },
  "edges": [
    {"relationship": "joins_with", "target": "customers_table", "joinKey": "customer_id"},
    {"relationship": "source_of", "target": "order_facts_dw", "pipeline": "elt_order_sync"},
    {"relationship": "derived_from", "target": "raw_orders_api", "transformation": "ETL_v2.1"}
  ]
}
```

이 그래프를 통해 Data Fabric은 **"이 테이블을 바꾸면 어떤 파이프라인과下游 테이블에 영향이 가는가?"**를 자동으로 추적할 수 있습니다.

---

## Ⅲ. AI 기반 자동화의 실제 사례

### 사례 1: 자동 데이터 기지 추적 (Auto Lineage)

기존: 데이터 엔지니어가 파이프라인 코드에 주석으로 기원 정보手動 기록 → 실제와 불일치 발생

Data Fabric: AI가 SQL의 FROM/JOIN 구문을解析해서 자동으로 데이터 흐름 그래프를構築:

```
[AI 기반 Lineage 추적]

  raw_orders_api
         │
         │ ETL (order_id, customer_id, amount, date)
         ▼
  stg_orders_normalized
         │
         │ transformation ( филь터 active orders, anonymize PII)
         ▼
  orders_table ──► BI_reports (sales_dashboard)
         │                  ▲
         │                  │
         ▼                  │
  customers_table ─────────┘
         │
         ▼
  dw_order_facts
```

### 사례 2: 자동 품질 이상 탐지

AI가 데이터의 분포, null 비율, 패턴을 학습하여 **"평소와 다른 데이터 패턴"**을 탐지하면 알림 발송:

- 결제 테이블의 일일 평균 금액이前日比 40% 하락 → 알림
- 고객 나이 필드에忽然 음수 등장 → 알림

---

## Ⅳ. Data Fabric vs Data Mesh: 어떻게 다른가?

```
[비교: Data Fabric vs Data Mesh]

          Data Fabric                    Data Mesh
     ┌──────────────────┐          ┌──────────────────┐
     │  중앙집중형 (Centralized)   │  분산형 (Distributed) │
     │                        │                        │
     │   ┌──────────────┐   │   │  [Domain A] [Domain B] │
     │   │ AI/ML Engine │   │   │    ▼           ▼      │
     │   │ Knowledge    │   │   │  [Domain C] [Domain D] │
     │   │ Graph        │   │   │         │              │
     │   └──────────────┘   │   │         ▼              │
     │         ▲            │   │   [Interconnection     │
     │         │            │   │    Fabric]              │
     │  All Teams' Data     │   │                         │
     └──────────────────────┘   └─────────────────────────┘

     Philosophy: "중앙이全部알아서 해줄게"  "도메인이各自管理해"
```

| 구분 | Data Fabric | Data Mesh |
|------|------------|-----------|
| **관리 주체** | 중앙 데이터 플랫폼 팀 | 각 도메인 팀 |
| **자동화 수준** | AI/ML 기반高度自動化 | 사람 중심 (Domain Owner) |
| **변화 관리** | 기존 조직 구조에 적용 가능 | 문화/조직 변화 필요 |
| **적합한 상황** | 규제 산업 (금융, 의료) | MSA/민첩한 조직 |

---

## Ⅴ. 도입 시 고려사항과 📢 비유

**도입 전 확인 사항:**
1. **메타데이터 기반**: Data Fabric의 효과는 "메타데이터의 품질"에 좌우됩니다. 메타데이터가 부실하면 AI도 잘못된 결론
2. **AI Governance**: AI 기반 추천/자동화가 실수하면 영향이 全社적 → AI 판단에 대한 설명 가능성(Explainability) 확보 필요
3. **비용**:Commercial Data Fabric 도구(Alation, Collibra, Informatica Cloud)는 연간 수억~수십억 원 수준

**주요 Data Fabric 도구:**
- **Alation**: 자동화된 카탈로그 + AI 기반 추천
- **Collibra**: 데이터 거버넌스 + 워크플로우
- **Informatica**: 클라우드 데이터 관리 + AI (CLAIRE 엔진)
- **Azure Purview**: Microsoft의 Data Fabric 서비스

> 📢 **섹션 요약 비유:** Data Fabric은 **"항만监督管理局의 원격 통제 시스템"**과 같습니다. 항구에 수십 척의 선박(데이터 소스)이 들어오고 나가고, 각 선박의 화물 목록(메타데이터)을 중앙 시스템이 全量 파악하고 있습니다.哪儿에 병목이 생기고(품질 이상),哪儿 물량이 쌓이는지(이상치)를 AI가 분석해서 관리자에게 보고합니다. 선박들은 여전히各自 운항(데이터 소스는 그대로)하지만, 중앙 시스템이 **"모든 화물의 흐름을 실시간으로 연결하는 직물(Fabric)"** 역할을 합니다. **중앙 통제 + AI 자동화**가 핵심입니다.
