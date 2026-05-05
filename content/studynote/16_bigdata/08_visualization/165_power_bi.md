+++
weight = 165
title = "165. Power BI — Microsoft 생태계 통합 DAX 비즈니스 인텔리전스"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Power BI — Microsoft 생태계 통합 DAX 비즈니스 인텔리전스은(는) 복잡한 대규모 데이터를 사람이 빠르게 해석하고 행동으로 옮기게 만드는 시각화 핵심 원리 또는 도구다.
> **비유**: 복잡한 계기판 수치를 한눈에 읽히는 조종석 화면으로 바꾸는 일과 같다.

📝 모범 답안

## 1. 개요 및 필요성

### Power BI의 위치와 성장

Power BI는 2015년 Microsoft가 출시한 클라우드 기반 BI 서비스다. 현재 Fortune 500 기업의 97% 이상이 사용하며, Gartner BI Magic Quadrant에서 Tableau와 함께 꾸준히 리더로 평가된다.

Power BI의 핵심 경쟁 우위:
- **비용**: Power BI Pro $10/사용자/월 vs Tableau Creator ~$70/월
- **Microsoft 통합**: Teams, SharePoint, Excel, Azure, OneDrive 네이티브 연동
- **AI 기능**: OpenAI 기반 Copilot (질의응답, 자동 인사이트, 요약)
- **학습 곡선**: Excel 사용자가 빠르게 전환 가능

---

## 2. 구성요소

### Power BI 3레이어 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                Power BI 3레이어 구조                         │
├──────────────────────────────────────────────────────────────┤
│  Layer 1: Power Query (데이터 수집·변환)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  M 언어 기반 ETL 엔진                                   │ │
│  │  - 300+ 데이터 커넥터 (DB, API, 파일, 클라우드)         │ │
│  │  - 변환: 피벗/언피벗, 조인, 텍스트 처리, 형변환         │ │
│  │  - 단계별 변환 이력 관리 (Applied Steps)                │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│  Layer 2: 데이터 모델 (관계·계산)                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  스타 스키마: 팩트 테이블 + 차원 테이블                  │ │
│  │  관계 정의: 1:N, N:M, 양방향                            │ │
│  │                                                        │ │
│  │  DAX 계산:                                             │ │
│  │  ① 계산 컬럼(Calculated Column): 행 단위 계산           │ │
│  │  ② 측정값(Measure): 동적 집계 (권장)                   │ │
│  │  ③ 계산 테이블(Calculated Table): 새 테이블 생성        │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│  Layer 3: 시각화 (보고서·대시보드)                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Power BI Desktop: 보고서 제작                          │ │
│  │  Power BI Service: 게시·공유·협업                       │ │
│  │  Power BI Mobile: 모바일 보고서                         │ │
│  │  Power BI Report Server: 온프렘 배포                    │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### DAX 핵심 패턴

#### CALCULATE: 필터 컨텍스트 조작

```dax
// 기본 패턴: CALCULATE(집계, 필터1, 필터2, ...)
서울 매출 = CALCULATE([총 매출], '지역'[지역] = "서울")

// 모든 필터 제거
전체 매출 = CALCULATE([총 매출], ALL('날짜'))

// 전년 동기 대비
전년 매출 = CALCULATE([총 매출], SAMEPERIODLASTYEAR('날짜'[Date]))

// YTD (Year-to-Date)
YTD 매출 = TOTALYTD([총 매출], '날짜'[Date])
```

#### 시간 인텔리전스 함수

| 함수 | 용도 |
|:---|:---|
| `SAMEPERIODLASTYEAR` | 전년 동기 |
| `TOTALYTD / TOTALQTD / TOTALMTD` | 누적(연/분기/월) |
| `DATEADD` | n 기간 이전/이후 |
| `DATESINPERIOD` | 특정 기간 범위 |
| `PARALLELPERIOD` | 병렬 기간 비교 |

---

## 3. 구조 및 원리

**핵심 조건**: 표현 정확성, 인지 부하, 질의 성능, 상호작용성을 함께 균형시켜야 한다.

동작 순서:
### 데이터 저장 모드 비교

| 모드 | 설명 | 장점 | 단점 | 적합 상황 |
|:---|:---|:---|:---|:---|
| **Import** | 데이터를 Power BI 모델로 복사 | 최고 성능 | 갱신 필요 | 대용량, 복잡 계산 |
| **DirectQuery** | 쿼리할 때마다 소스 DB 직접 조회 | 항상 최신 | 성능 제한 | 실시간 요구 |
| **Composite** | Import + DirectQuery 혼합 | 유연성 | 복잡한 관리 | 일부 실시간 필요 |
| **Dual** | Import·DirectQuery 동시 가능 | 유연성 최대 | 복잡도 최대 | 집계 테이블과 함께 |

### Microsoft Fabric: Power BI의 미래

```
Microsoft Fabric (2023) = 통합 분석 플랫폼

  One Lake (단일 데이터 저장소)
       │
  ┌────┴────────────────────────────────────┐
  │  Data Factory  │  Synapse   │  Power BI │
  │  (데이터 통합) │  (분석)    │  (시각화)  │
  └─────────────────────────────────────────┘
  
  특징:
  - 모든 데이터가 One Lake의 Delta Parquet 형식 저장
  - 복사 없이 각 서비스에서 직접 접근
  - 단일 과금 체계 (F-SKU)
  - 직물처럼 모든 서비스가 연결(Fabric 명칭 유래)
```

---

## 4. 비교 및 연결

### 행 수준 보안 (RLS: Row-Level Security)

RLS는 사용자 역할에 따라 볼 수 있는 데이터 행을 제한하는 보안 기능:

```dax
// RLS 규칙 정의 (영업 담당자는 자기 지역 데이터만 접근)
[담당자] = USERPRINCIPALNAME()

// 또는 동적 RLS
[지역] IN VALUES(RELATED('담당자 지역 매핑'[지역]))
```

### 고급 개발 도구

| 도구 | 용도 |
|:---|:---|
| **DAX Studio** | DAX 쿼리 성능 분석, 모델 문서화 |
| **Tabular Editor** | 모델 개발, CI/CD, 배포 파이프라인 |
| **ALM Toolkit** | 모델 비교·병합 (Git Flow 지원) |
| **Power BI Helper** | 모델 문서 자동 생성 |

---

## 5. 실무 적용 및 판단

### Power BI 도입 효과

| 영역 | 효과 |
|:---|:---|
| **비용 효율** | Tableau 대비 1/7 수준 비용으로 유사한 BI 능력 |
| **생태계 통합** | Microsoft 365 환경에서 Teams/SharePoint 내장 보고서 |
| **데이터 민주화** | Excel 사용자 → Power BI 전환 학습 곡선 최소화 |
| **거버넌스** | Premium 워크스페이스 배포 파이프라인, RLS |

### 결론

Power BI는 **비용 효율성·Microsoft 생태계 통합·AI 기능**의 3가지 강점으로 엔터프라이즈 BI 시장의 주류가 되었다. DAX는 Excel 함수와 유사한 구조지만, 필터 컨텍스트 이해가 핵심이다. Microsoft Fabric으로의 전환은 데이터 플랫폼의 패러다임 변화를 의미하며, 정보통신기술사는 이 통합 플랫폼 전략을 이해하고 클라우드 데이터 전략에 반영해야 한다.

---

## 6. 기대효과 및 결론

Power BI — Microsoft 생태계 통합 DAX 비즈니스 인텔리전스은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 시각화의 본질은 더 많은 그래프가 아니라 더 빠르고 정확한 판단을 가능하게 하는 정보 구조다.

---

## 7. 발전 흐름도

```text
[DAX (Data Analysis Expressions)]
    │
    ▼
[CALCULATE (필터 조작)]
    │
    ▼
[Power Query (M 언어)]
    │
    ▼
[Import 모드 vs DirectQuery]
    │
    ▼
[Microsoft Fabric (통합 플랫폼)]
```

이 흐름도는 DAX (Data Analysis Expressions)에서 출발해 Microsoft Fabric (통합 플랫폼)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DAX | 계산 언어 | Data Analysis Expressions — 측정값·계산 컬럼 |
| CALCULATE | 핵심 DAX 함수 | 필터 컨텍스트 조작의 핵심 |
| Power Query | 데이터 변환 | M 언어 기반 300+ 커넥터 ETL |
| Import 모드 | 데이터 모드 | 복사 저장, 최고 성능 |
| DirectQuery | 데이터 모드 | 소스 직접 쿼리, 항상 최신 |
| RLS | 보안 기능 | 역할별 행 수준 데이터 필터 |
| Microsoft Fabric | 통합 플랫폼 | Power BI + Data Factory + Synapse |
