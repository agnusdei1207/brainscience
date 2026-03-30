+++
weight = 20
title = "GCP 주요 서비스 (IaaS/PaaS)"
description = "Google Cloud Platform의 IaaS/PaaS 대표 서비스와 활용"
date = 2026-03-26

[taxonomies]
tags = ["cloud", "gcp", "compute-engine", "cloud-storage", "bigquery", "gke"]
+++
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Google Cloud Platform (GCP)은 Google의 全 earth 規模 네트워크 인프라와データ分析/AI/ML领域的기술력을�은 클라우드 플랫폼으로, BigQuery, TensorFlow, Kubernetes (GKE), Spanner 등이 主役 제품이다.
> 2. **가치**: Google 自社開発環境 (Search, YouTube, Gmail) 에서 검증된 기술을 제공하므로, 성능,확장성,신뢰성에서最高水準을 자랑한다.
> 3. **융합**: GCP의 가장 큰 강점은 데이터 분석 (BigQuery), AI/ML (Vertex AI, TensorFlow), container (GKE)领域에서 나타나며, 이러한 workload를 운영하는 조직에게 가장 적합한 선택이다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### GCP 개요

GCP는 Google의 내부 인프라를外部に提供する 형태로诞성했으며, 현재 40개 지역 121개 가용 영역에서 서비스를 제공하고 있다. GCP의 기술력은 Google 自社의 대규모 서비스를 운영하는中で培われたもので、MapReduce, BigTable, TensorFlow, Kubernetes 等の技术在 GCP에서サービスとして提供されている。

### 비유

GCP의 기술력は/are Honda의 엔진 기술과 같습니다. Honda는机车用 engines를自言自语하며培ってきた技術力を自動車, 除草機, 甚至는  робот as等多种 产品에 적용하듯이, Google도 自社サービス (Search, YouTube, Gmail)运维で 쌓은技術力を GCP 통해 외부에 提供합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### GCP IaaS 핵심 서비스

#### Google Compute Engine

Compute Engine은 GCP의 IaaS 핵심 서비스로,预定義 머신 유형 (E2, N1, N2, C2, M2) 과 커스텀 머신 유형을 지원한다. Live Migration 기능이 강점으로, 호스트 유지보수 시 VM을シャットダウンせずに 다른 물리적 서버로 자동迁移한다.这点은 AWS/EC2나 Azure VM보다 우수한 점이다.

#### Google Cloud Storage (GCS)

Cloud Storage는 GCP의 객체 스토리지로,AWS S3와Direct 경쟁한다. 스토리지 클래스는 Standard, Nearline, Coldline, Archive이며, ARN(地理的冗長存储)를 통해 全球 어디서나 低レイテン시로 접근 가능하다.

#### Google VPC Network

GCP VPC는 全球 1개의 software-defined 네트워크로, 리전 간 네트워크Latency이 AWS/ Azure보다 낮은 경향이 있다. Firewall Rules, Cloud NAT, VPC Peering, Shared VPC, Cloud Router 등의 기능을 제공한다.

### GCP PaaS 핵심 서비스

#### BigQuery

BigQuery는 完全Serverless 데이터 웨어하우스로, 페타바이트 규모의 데이터 분석을 SQL로 수행할 수 있다. 저장과 컴퓨팅이 분리되어 있어, 데이터 양에 관계없이 인프라 관리 없이 SQL 만으로 分析이 가능하다. ML integrate도 지원하여 BigQuery ML로 SQL 만으로 머신러닝 模型 훈련과 추론이 가능하다.

#### Cloud SQL

Cloud SQL은 MySQL, PostgreSQL, SQL Server를 지원하는管理型 관계형 DB 서비스다. HA 구성, Automated Backup, Point-in-time Recovery, Read Replica 등을 지원한다.

#### Google Kubernetes Engine (GKE)

GKE는 Gartner에서 最推荐으로 선정된 管理型 Kubernetes 서비스다. Autopilot 모드는 ノード管理を完全に Google に委任し、ユーザーは支払い，而不是預約したリソースに対して 而是 실제 사용량에 따라 지불한다. Anthos를 통해 온프레미스 GKE와의 통합 관리도 가능하다.

#### Cloud Functions / Cloud Run

Cloud Functions는 AWS Lambda와 유사한 FaaS이고, Cloud Run은 Knative 기반의 서버리스 컨테이너 플랫폼이다. Cloud Run은任意の 컨테이너 이미지를 실행할 수 있어, Lambda보다 더 큰 유연성을 제공한다.

### GCP 핵심 서비스 비교 (AWS/Azure 대비)

GCP의 핵심 서비스들이 AWS/Azure의 어떤 서비스에 대응하는지 비교하면,，GCP의 강점이 어디에 있는지 파악할 수 있다.

```text
  ┌────────────────────────────────────────────────────────────────────┐
  │               GCP 핵심 서비스 매핑 (AWS/Azure 대비)                        │
  ├────────────────────────────────────────────────────────────────────┤
  │
  │  ┌────────────────┬────────────────┬────────────────┐              │
  │  │    GCP         │      AWS       │     Azure      │              │
  │  ├────────────────┼────────────────┼────────────────┤              │
  │  │ Compute Engine │     EC2        │ Azure VM       │  ← IaaS    │
  │  ├────────────────┼────────────────┼────────────────┤              │
  │  │ Cloud Storage  │      S3        │  Blob Storage  │  ← 스토리지 │
  │  ├────────────────┼────────────────┼────────────────┤              │
  │  │   Cloud SQL    │      RDS       │ Azure SQL DB   │  ← RDB    │
  │  ├────────────────┼────────────────┼────────────────┤              │
  │  │   BigQuery     │   Redshift     │  Synapse Analytics│ ← 分析   │
  │  ├────────────────┼────────────────┼────────────────┤              │
  │  │      GKE       │      EKS       │     AKS        │  ← K8s    │
  │  ├────────────────┼────────────────┼────────────────┤              │
  │  │ Cloud Functions│    Lambda      │ Azure Functions│  ← FaaS   │
  │  ├────────────────┼────────────────┼────────────────┤              │
  │  │   Vertex AI    │  SageMaker     │ Azure ML       │  ← AI/ML  │
  │  ├────────────────┼────────────────┼────────────────┤              │
  │  │   Cloud CDN    │ CloudFront     │   Azure CDN    │  ← CDN    │
  │  ├────────────────┼────────────────┼────────────────┤              │
  │  │    Cloud DNS   │  Route 53      │   Azure DNS    │  ← DNS    │
  │  └────────────────┴────────────────┴────────────────┘              │
  │                                                                      │
  │  GCP 특화 강점:                                                  │
  │  - BigQuery: 페타바이트規模 Serverless 분석 (Redshift보다 운영 편의)   │
  │  - GKE: Google의 15년 K8s 운영 노하우 + Autopilot                 │
  │  - Live Migration: 호스트 장애 시 VM 자동 이전 (AWS/Az보다優れる)      │
  │  - Global VPC: 리전 간Latency 매우 낮음                             │
  └──────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** GCP의 상대적 강점은 데이터 분석과 container 오케스트레이션에 있다. BigQuery는 저장이랑 컴퓨팅이 분리된 serverless架构로, 데이터 분석을 위한 infra管理 부담이 AWS Redshift보다 현저히 낮다. GKE는 Google이 Borg (K8s의前身) を15년 운영하며 쌓은 경험을注ぎ込んでおり, Autopilot 모드는 노드 관리에서 完全放手して Google이 최적의 노드를 자동 Provisioning한다. Live Migration도 강점으로, 호스트에 장애가 발생해도 VM이 자동 이전되어 서비스 중단이 거의 없다.

### 섹션 요약 비유

GCP의 Live Migration機能は/are 新幹線の運行 시스템と 같습니다。線路inspection（호스트 장애 예방メンテナンス）が必要になっても、乘客（VM 运行상태）を降ろすことなく（シャットダウン 없이）別の編成（다른 물리적 서버）に自動連結されて、遅延なく運行이 계속되는 구조입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### GCP의 상대적 강점과 약점

| 영역 | 강점 | 약점 |
|:---|:---|:---|
| **데이터 분석** | BigQuery의 serverless 아키텍처, 저렴한 저장소 | Redshift 대비 ML 통합은劣势 |
| **AI/ML** | TensorFlow native 지원, Vertex AI의 포괄적 기능 | Azure ML의 엔터프라이즈 통합은劣势 |
| **Kubernetes** | GKE Autopilot,/Borg 경험, 무료 운영 panels | EKS/AKS의 MS 도구統合は劣势 |
| **컴퓨팅** | Live Migration, 가성비 | Windowsワーク로드対応は劣势 |
| **시장 점유율** | ~10% (3위) | AWS/Azure 대비 낮은 점유율 |

### 과목 융합 관점

- **데이터 분석 (Data Analytics)**: BigQuery는 全地球 規模 분석에 최적화되어 있으며, Google Cloud Storage와 긴밀히統合되어、データレイクからBigQueryまで の連携が容易이다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — BigQuery 기반 실시간 분석 파이프라인**:、수십 테라바이트의 클릭스트림 데이터를 Cloud Storage에 저장하고, BigQuery로 일별/주별 분석을 수행하여 마케팅 인사이트를 도출하는 파이프라인을 구축했다. 별도의 DW 인프라도运维人员도 없이, SQL 만으로 페타바이트 분석이 가능하여 기존 하둡 클러스터 대비 60% 비용 절감과 동시에分析 속도가 10배 향상되었다.

### 도입 체크리스트

- **기술적**: BigQuery로 분석할 데이터의スキーマ設計를事前准备了乎? GKE Autopilot利用時의 비용 모델 (실제 사용량 결제) 을 이해했는가?
- **운영·보안적**: GCP IAM의 자원 계층 구조 (Organization → Folder → Project → Resource) 를 통해Least Privilege를 적용했는가?

### 섹션 요약 비유

BigQueryのServerless性がもたらす価値は/are 自前面的 식당과 같습니다. 料理道具（인프라）를 모두 갖추고、常時 配置시켜두는 것이 아니라、손님（쿼리）が来ないと 检查어 놓다가（アイドル資源なし）、注文하면（クエリ実行）同時に料理道具（컴퓨팅 자원）도出現하여料理하는（処理）構造です.

---

## Ⅴ. 기대효과 및 결론

GCP는 데이터分析과 AI/ML领域에서最高의 기술력을持有하고 있으며, Kubernetes 운영 역량에서도 경쟁力を 갖추고 있다. 그러나 전반적인 생태계는 AWS/Azure 대비 협소하여, 서비스 선택 시 충분한 검토가 필요하다.

### 섹션 요약 비유

GCPの全体的な価値は/are Rolex와 Swatch의 관계에 비유할 수 있습니다. Rolex（GCP）는高端 기술（分析/AI/ML）에서 절대적이 강점이 있지만, Swatch（AWS/Azure）는 다양한 취급 가격대와 제품 라인으로 全消費者的商品覆盖를 하고 있습니다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Compute Engine** | GCP의 IaaS로, Live Migration과 커스텀 머신 유형을 지원한다. |
| **BigQuery** | 完全Serverless 데이터 웨어하우스로, 페타바이트 규모 SQL 분석을 지원한다. |
| **Cloud Storage** | GCP의 객체 스토리지로, AWS S3/Azure Blob과 동일한 역할을 담당한다. |
| **GKE (Google Kubernetes Engine)** | 管理型 Kubernetes로, Autopilot 모드와 Borg 기반 운영 경험을 제공한다. |
| **Cloud Functions / Cloud Run** | GCP의 FaaS (Cloud Functions) 와 서버리스 컨테이너 (Cloud Run) 서비스다. |
| **Vertex AI** | GCP의統合 AI/ML 플랫폼으로, TensorFlow native 지원과 AutoML 기능을 제공한다. |
| **VPC Network** | GCP의 software-defined 네트워크로, 全球 단일 네트워크라는 특징이 있다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. GCP의 BigQueryは/高級寿司店のretéと 같습니다。板前さん（인공지능)가 お在手（データ）を見て、那一刻最佳的（お岁时에 가장 맛있는）寿司（分析結果）를 만들어 내듯이, 데이터量에関係없이 그때그때 가장 맛있는 分析結果를 만들어 냅니다.
2. GKE Autopilot模式は/完全托管のBus Tourと 같습니다。乘客（컨테이너）은停留所（ノード）到着을 기다릴 필요も 없고、 Bus公司（Google）가最適なBus（노드）를 自动 prepared하여乗客을运送하는 역할을 합니다.
3. Compute Engine의 Live Migration功能은/are漫画의主人公がダメージ를 입어도 自动으로回復する力と 같습니다。宿主のalli（호스트障害）が发生しても、 VM（캐릭터）는-Shutdown 없이別の 장소（다른 물리적 서버）로이동하여서비스를 계속 제공하는结构입니다.
