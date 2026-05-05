+++
weight = 160
title = "160. Microsoft Fabric — One Lake 통합 분석 플랫폼"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Microsoft Fabric — One Lake 통합 분석 플랫폼은(는) 원시 데이터 저장의 유연성과 분석 거버넌스의 통제를 함께 확보하기 위한 현대 데이터 플랫폼 핵심 개념이다.
> **비유**: 자유롭게 물을 모으는 저수지에 수문·정수 설비를 함께 갖춘 복합 수자원 시설과 같다.

📝 모범 답안

## 1. 개요 및 필요성

Microsoft의 데이터 서비스는 Azure Synapse Analytics, Azure Data Factory, Power BI, Azure Databricks, Azure Data Lake Storage 등이 각각 독립적으로 운영되어, 조직이 여러 서비스를 개별 계약·관리해야 하는 복잡성이 있었다. 데이터 사일로(Data Silo) 문제도 심각하여, 부서마다 별도 스토리지에 동일한 데이터를 중복 보관하는 경우가 빈번했다.

Microsoft Fabric은 이 분산된 Azure 데이터 서비스를 단일 SaaS 플랫폼으로 통합하며, OneLake라는 단일 조직 데이터 저장소가 모든 서비스의 스토리지 레이어를 공유한다.

| 기존 Azure 데이터 스택 | Microsoft Fabric |
|:---|:---|
| Azure Synapse Analytics | Fabric Synapse Data Engineering |
| Azure Data Factory | Fabric Data Factory |
| Power BI Premium | Fabric Power BI |
| Azure Data Lake Storage | OneLake (Fabric 내장) |
| Azure Machine Learning | Fabric Data Science |
| 개별 서비스 라이선스 | 단일 Fabric SKU |

---

## 2. 구성요소

```
┌──────────────────────────────────────────────────────────────────┐
│               Microsoft Fabric 아키텍처                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                Fabric 경험(Experience) 레이어              │    │
│  │                                                          │    │
│  │  Data       Data       Data      Power   Real-Time      │    │
│  │  Engineering Factory   Science   BI      Analytics       │    │
│  │  (Spark)    (Pipeline) (ML)      (Report)(Eventstream)  │    │
│  └────────────────────┬────────────────────────────────────┘    │
│                       │                                         │
│  ┌────────────────────▼────────────────────────────────────┐    │
│  │                OneLake (통합 스토리지)                    │    │
│  │                                                          │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │  조직 전체 단일 ADLS Gen2 인스턴스                  │   │    │
│  │  │  workspace1/  workspace2/  workspace3/            │   │    │
│  │  │  (테넌트당 하나)                                   │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  │                                                          │    │
│  │  ┌───────────────┐   ┌─────────────────────────────┐   │    │
│  │  │  Shortcuts    │   │  Delta Parquet 형식 (기본)   │   │    │
│  │  │  (가상 링크)   │   │  Iceberg 지원 (2024~)       │   │    │
│  │  │  AWS S3       │   │                             │   │    │
│  │  │  GCS          │   │  OneCopy: 단일 물리 복사본   │   │    │
│  │  │  Azure Blob   │   │  로 모든 서비스가 공유 접근  │   │    │
│  │  └───────────────┘   └─────────────────────────────┘   │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Fabric Capacity (SKU: F4~F2048)                           │  │
│  │  - 단일 용량 단위로 모든 경험 레이어 컴퓨팅 공유            │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

**핵심 구성 요소 상세**

| 구성 요소 | 역할 | 핵심 특징 |
|:---|:---|:---|
| OneLake | 통합 스토리지 | 조직당 하나, ADLS Gen2 기반, Delta 포맷 |
| Shortcuts | 가상 데이터 참조 | 복사 없이 S3/GCS/Azure Blob 데이터 접근 |
| Lakehouse | 데이터 엔지니어링 | Delta 기반 Bronze/Silver/Gold 구현 |
| Data Warehouse | SQL 분석 | 완전 관리형 SQL 웨어하우스 |
| Eventstream | 실시간 스트리밍 | Kafka 호환, Real-Time Analytics 연동 |
| Fabric Capacity | 과금 단위 | 모든 경험 공유 컴퓨팅 자원 |

---

## 3. 구조 및 원리

**핵심 조건**: 저장 포맷, 메타데이터, 트랜잭션, 거버넌스 계층을 함께 설계해야 한다.

동작 순서:
**Fabric vs 경쟁 플랫폼 비교**

| 항목 | Microsoft Fabric | Databricks | Snowflake |
|:---|:---|:---|:---|
| 통합 범위 | BI + 데이터 엔지니어링 + ML + 스트리밍 | 데이터 엔지니어링 + ML | DW + 제한적 레이크 |
| BI 도구 | Power BI 내장 (최강) | Databricks SQL (제한적) | Tableau/Power BI 외부 연결 |
| ML/AI | Fabric Data Science | MLflow 최고 수준 | Snowpark ML |
| 스트리밍 | Eventstream (관리형) | Structured Streaming | Snowpipe |
| 과금 모델 | 단일 Capacity SKU | DBU 기반 | Credit 기반 |
| 멀티 클라우드 | Azure 중심 (AWS/GCS Shortcut) | 완전 멀티 클라우드 | 완전 멀티 클라우드 |

**OneLake와 Shortcuts 활용 패턴**

- **교차 워크스페이스 공유**: 다른 팀의 Lakehouse 테이블을 Shortcut으로 참조 (복사 없음)
- **레거시 연동**: Azure Blob이나 AWS S3의 기존 데이터를 Shortcut으로 즉시 연결
- **멀티 클라우드 패브릭**: GCS/S3 데이터를 OneLake에 Shortcut으로 포함, Fabric 경험 레이어로 분석

---

## 4. 비교 및 연결

**Fabric 도입 의사 결정 기준**

- **Microsoft 친화 조직**: Power BI + Azure 스택 이미 사용 중인 기업에서 최적 ROI
- **BI-데이터 통합 요구**: 데이터 엔지니어링 결과를 즉시 Power BI로 시각화해야 할 때
- **비용 단순화**: 여러 Azure 서비스 라이선스를 Fabric 단일 SKU로 통합할 때
- **레거시 현대화**: Azure Synapse/ADF를 Fabric으로 마이그레이션하는 로드맵

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| OneLake 핵심 원칙 | 조직당 단일 ADLS Gen2, OneCopy (단일 물리 복사본) |
| Shortcuts 동작 원리 | 가상 링크로 외부 스토리지를 OneLake 네임스페이스에 연결, 복사 없음 |
| Fabric SKU 특징 | F4~F2048, CU(컴퓨팅 단위) 공유로 모든 경험 레이어 동시 실행 |
| Fabric vs Azure Synapse | Fabric = 통합 SaaS 플랫폼, Synapse = 개별 서비스 (마이그레이션 대상) |

---

## 5. 실무 적용 및 판단

| 효과 | 내용 |
|:---|:---|
| 데이터 사일로 해소 | OneLake로 부서별 중복 스토리지 통합 |
| TCO 절감 | 개별 서비스 라이선스 → 단일 Fabric SKU |
| 분석 속도 향상 | 데이터 엔지니어링→BI를 같은 플랫폼에서 즉시 연결 |
| 거버넌스 일원화 | Microsoft Purview 통합으로 OneLake 전체 데이터 거버넌스 |

Microsoft Fabric은 2023년 GA(General Availability) 이후 Microsoft 최대 데이터 플랫폼 투자로 주목받고 있다. Power BI 기반 조직과 Azure 중심 기업에서 가장 빠른 도입 속도를 보이며, Databricks·Snowflake와의 3파전이 빅데이터 플랫폼 시장의 핵심 경쟁 구도를 형성한다. 기술사 시험에서는 **OneLake 원칙(조직당 단일 레이크)**, **Shortcuts 메커니즘**, **Fabric SKU 과금 모델**이 핵심 논점이다.

---

## 6. 기대효과 및 결론

Microsoft Fabric — One Lake 통합 분석 플랫폼은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 레이크하우스 계열 기술은 저장 유연성과 거버넌스 통제를 동시에 달성할 때 비로소 플랫폼 가치가 커진다.

---

## 7. 발전 흐름도

```text
[분산 데이터 웨어하우스 (Distributed DW) — 구조화 데이터, SQL 중심]
    │
    ▼
[데이터 레이크 (Data Lake) — 비정형·반정형 포함, 스키마 온 리드]
    │
    ▼
[Azure Synapse Analytics — DW + Lake 통합, SQL + Spark 혼용]
    │
    ▼
[Microsoft Fabric — OneLake 단일 저장소, 통합 SaaS 분석 플랫폼]
    │
    ▼
[Lakehouse 아키텍처 (Delta Lake / OneLake) — ACID + 분석 통합 표준화]
```
Microsoft Fabric은 OneLake라는 단일 저장소 위에 데이터 엔지니어링·과학·BI를 통합한 SaaS 분석 플랫폼으로, Lakehouse 아키텍처의 완성형이다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| OneLake | 핵심 스토리지 | 조직당 단일 ADLS Gen2, OneCopy |
| Shortcuts | 가상 참조 | 데이터 복사 없는 외부 스토리지 연결 |
| Fabric Capacity | 과금 단위 | F4~F2048 SKU, 모든 경험 공유 |
| Lakehouse (Fabric) | 데이터 엔지니어링 | Delta 기반, Notebooks, Spark |
| Eventstream | 실시간 처리 | Kafka 호환 스트리밍 |
| Microsoft Purview | 거버넌스 통합 | OneLake 전체 데이터 카탈로그·리니지 |
