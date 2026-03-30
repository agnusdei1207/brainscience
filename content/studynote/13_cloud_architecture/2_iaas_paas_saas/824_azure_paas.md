+++
weight = 19
title = "Azure 주요 서비스 (IaaS/PaaS)"
description = "Microsoft Azure의 IaaS/PaaS 대표 서비스와 활용"
date = 2026-03-26

[taxonomies]
tags = ["cloud", "azure", "virtual-machines", "azure-sql", "aks", "functions"]
+++
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Microsoft Azure는 200개 이상의 서비스를 제공하는 클라우드 플랫폼으로, Windows Server, SQL Server, .NET, Active Directory 등 Microsoft ecossystemとの深い統合이最大 강점이며, 엔터프라이즈 환경에서 가장 빠르게 성장하고 있다.
> 2. **가치**: Azure AD (Active Directory) 와의 SSO 연동, Microsoft 365生态계との統合、 Windows/Linux 全対応으로、Microsoft 기반 기업에게 가장 자연스러운 클라우드 전환 경로를 제공한다.
> 3. **융합**: Azure Arc, Azure Defender for IoT, Azure Sphere 등 Hybrid Cloud와 Edge 시나리오에 특화된 서비스로, 온프레미스-클라우드 통합 관리에 강한 포커스를 두고 있다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### Azure 개요

Microsoft Azure는 2010년 정식 출시되어 현재 全세계 60개 이상 지역에서 서비스를 제공하고 있다. Azure의 가장 큰 차별화 요소는 Microsoft製品群との深い統合이다. 이미 Microsoft 환경에서 운영하는 기업이라면, Azure는 既知のツールと 프로세스를 최대한 활용하면서 클라우드로 전환할 수 있는 자연스러운 경로를 제공한다.

### 비유

Azure의Microsoft統合은/are 같은 회사의 系列社との合作社과 같습니다.系列社（Microsoft製品群）들 간에는 sudah tercipta 신뢰와 시스템 통합이 되어 있어서, 系列사간협력（オンプレミス↔클라우드）이 마치内部 협업처럼 자연스럽게 이루어집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Azure IaaS 핵심 서비스

#### Azure Virtual Machines

Azure VM은 AWS EC2와 유사한 IaaS 서비스로, Windows와 Linux 全対応한다. VM 크기는 B (Burstable), D (General), E (Memory Optimized), F (Compute Optimized), H (High Performance Computing), L (Storage Optimized), N (GPU) 시리즈로 구분된다.可用성 집합 (Availability Set), 가용성 영역 (Availability Zone), Virtual Machine Scale Sets (VMSS) 등을 통해 고가용성과 오토 스케일링을 지원한다.

#### Azure Virtual Network (VNet)

VNet은 AWS VPC와 유사한 Azure의 논리적으로 격리된 가상 네트워크다. 서브넷, NSG (Network Security Group), Application Security Group, Azure Firewall, Virtual Network Peering, VPN Gateway, ExpressRoute 등을 제공한다.

#### Azure Storage

Azure Storage는 Blob (객체), Table (NoSQL), Queue (메시지), Files (파일 공유), Disk (블록 스토리지) 의 5가지 저장소 서비스를 unified 하나의 계정에서 제공한다. redundancy 옵션으로 LRS (Local), ZRS (Zone), GRS (Geo), GZRS (Geo-Zone)를 제공한다.

### Azure PaaS 핵심 서비스

#### Azure App Service

App Service는 웹 앱, RESTful API, 백엔드服务的托管プラットフォームだ。 .NET, .NET Core, Java, Node.js, Python, PHP, Ruby 등 다양한 런타임을 지원하며, Deployment Slot을 통해 무중단 배포를 지원한다.

#### Azure SQL Database

Azure SQL Database는 완전히 관리된的关系형 DB 서비스로, SQL Server 엔진 기반이다. 따라서 기존 SQL Server 애플리케이션의コード変更 거의 없이 마이그레이션이 가능하다. Intelligent Performance (쿼리 처리 자동 최적화), Dynamic Data Masking, Always Encrypted 등의 고급 기능을 제공한다.

#### Azure Kubernetes Service (AKS)

AKS는Azure의管理型 Kubernetes 서비스로, Windows 컨테이너 노드 지원, Azure AD 통합, Azure Monitor 통합 등의Azure 특화 기능을 제공한다.

#### Azure Functions

Azure Functions는 AWS Lambda와 유사한 서버리스 함수 실행 서비스로, Durable Functions (상태 유지 함수), Azure Durable Entities (분산 상태 관리) 등 Lambda에 없는 고급 기능을 제공한다.

### Azure IaaS/PaaS 서비스 관계

Azure에서 VMs, VNet, Storage, App Service가 어떻게 관계하는지 시각화하면,Microsoft製品群との統合-based 설계思想을 파악할 수 있다.

```text
  ┌────────────────────────────────────────────────────────────────────┐
  │               Azure IaaS/PaaS 서비스 관계도                              │
  ├────────────────────────────────────────────────────────────────────┤
  │
  │  ┌──────────────────────────────────────────────────────────────┐  │
  │  │                   Azure Virtual Network (VNet)                 │  │
  │  │                                                              │  │
  │  │   ┌────────────────────┐   ┌────────────────────┐             │  │
  │  │   │   Public Subnet   │   │   Private Subnet   │             │  │
  │  │   │                   │   │                    │             │  │
  │  │   │  ┌────────────┐  │   │  ┌────────────┐    │             │  │
  │  │   │  │Azure VMs   │  │   │  │Azure VMs   │    │             │  │
  │  │   │  │Web Server  │  │   │  │App Server  │    │             │  │
  │  │   │  └────────────┘  │   │  └────────────┘    │             │  │
  │  │   │                   │   │                    │             │  │
  │  │   │  NSG: Allow 80,443│   │  NSG: Allow 8080 │             │  │
  │  │   └────────────────────┘   └────────────────────┘             │  │
  │  │                                                              │  │
  │  └──────────────────────────────────────────────────────────────┘  │
  │                              │                                      │
  │  ┌────────────────────────────┴────────────────────────────┐  │
  │  │                   Azure Storage Account                    │  │
  │  │   ├─ Blob Storage (객체 스토리지, S3 대항)                 │  │
  │  │   ├─ Table Storage (NoSQL, DynamoDB 대항)                  │  │
  │  │   ├─ Queue Storage (메시지 큐, SQS 대항)                   │  │
  │  │   └─ Files (파일 공유, EFS/FSx 대항)                      │  │
  │  └────────────────────────────────────────────────────────────┘  │
  │                                                                      │
  │  ┌────────────────────────────────────────────────────────────┐  │
  │  │                  Azure PaaS Layer                           │  │
  │  │   ├─ App Service (PaaS 웹 앱)                             │  │
  │  │   ├─ Azure SQL (PaaS DB)                                  │  │
  │  │   ├─ AKS (Kubernetes)                                     │  │
  │  │   └─ Functions (Serverless)                               │  │
  │  └────────────────────────────────────────────────────────────┘  │
  │                                                                      │
  │  핵심: VNet과 통합되어 PaaS 서비스도 Virtual Network에 配置 가능        │
  └──────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Azure의 아키텍처 설계思想은 "Microsoft 환경과의 통합"이다. Azure VM과 PaaS 서비스 양쪽 모두 VNet에 연결되어同一ネットワーク内で通信 가능하다. Azure AD와統合된認証/인가 시스템, Microsoft 365/Teamsとの原生集成등이Azure의 가장 큰 강점이다. 엔터프라이즈 환경에서 기존에 Windows Server, SQL Server, Active Directory 등을使用してきた企业には、Azureへの移行が最も自然な選擇となる。

### 섹션 요약 비유

Azure의 Microsoft統合는/are 같은 브랜드의 무선 이어폰과 스마트폰의 연결과 같습니다. 같은 브랜드 (Microsoft) 产品이라면、箱から取り出す 순간（プロ비ジョニング）부터즉시 연결（統合）되어、追加設定（追加 구성）없이도 손쉽게 활용할 수 있는 사용성를 提供합니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: Azure vs AWS 핵심 서비스 매핑

| 카테고리 | AWS | Azure |
|:---|:---|:---|
| **컴퓨팅** | EC2 | Azure Virtual Machines |
| **오토 스케일링** | Auto Scaling Groups | Virtual Machine Scale Sets |
| **객체 스토리지** | S3 | Blob Storage |
| **관계형 DB** | RDS | Azure SQL Database |
| **키-값 스토리지** | DynamoDB | Cosmos DB (Table API) |
| **컨테이너** | EKS | AKS |
| **서버리스** | Lambda | Azure Functions |
| **CDN** | CloudFront | Azure CDN |
| **DNS** | Route 53 | Azure DNS |
| **IAM** | IAM | Azure AD (Entra ID) |

### 과목 융합 관점

- **보안 (Security)**: Azure AD (현재 Microsoft Entra ID) 는 Azure의 IAM 핵심으로, 온프레미스 Active Directory와Federation되어 SSO를 提供한다. Conditional Access, MFA (Multi-Factor Authentication) 등을 통해_zero trust модель을 구현할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — .NET 기반 업무 시스템의 Azure 이전**:、기존 ASP.NET MVC 기반 업무 시스템을 Azure App Service로 마이그레이션했다. 기존 코드의 95% 변경 없이 이전되었고, Azure AD 통합으로 SSO도 즉座実装되었다. IIS에서 Azure App Service로의 이전으로、 デプロイ時間은 30분에서 5분으로 단축되었다.

### 도입 체크리스트

- **기술적**: 온프레미스 Active Directory와 Azure AD 간 federation을 수립했는가? IaC 도구 (Terraform, ARM Templates, Bicep) 활용을 준비했는가?
- **운영·보안적**: Azure Security Center를 통해 보안态势를統一 모니터링했는가? 역할 기반 접근 제어 (RBAC)를 통해Least Privilege 원칙을 적용했는가?

### 섹션 요약 비유

Azure ADの統合価値は/are 같은 계열사間のbizCardと 같습니다。系列사間では既に信頼関係（フェデレーション）が構築되어 있어、到着하자마자（ログイン）即座に社内外の各部门（Azure ресурсов）にアクセスできる構造です.

---

## Ⅴ. 기대효과 및 결론

Azure는 Microsoft環境での运营に強みを持ち、.NET, SQL Server, Active Directory 기반의 엔터프라이즈企业에 가장 적합한 선택이다. 그러나 Windows/Linux 全対応故、特定プラットフォーム에拘泥しない灵活性도 갖추고 있다.

### 섹션 요약 비유

Azureの全体的な価値は/are IKEAのシステムキッチンと 같습니다。 IKEA产品들（Microsoft製品群）之间には設計の統一性（統合）が 이미 되어 있어서, 올려놓는 것（배포만 하면）으로 Kitchen（IT 시스템）が 바로 利用可能状态가 됩니다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Azure Virtual Machines** | Azure의 대표 IaaS로, Windows/Linux 全対応한 가상 머신 서비스다. |
| **Azure Virtual Network (VNet)** | Azure 내 논리적으로 격리된 가상 네트워크로, AWS VPC와 유사한 기능 제공 |
| **Azure App Service** | Azure의 PaaS 웹 애플리케이션 호스팅 서비스로, .NET, Java, Node.js 등을 지원한다. |
| **Azure SQL Database** | 完全管理형 SQL Server 기반 DBaaS로, 기존 SQL Server 마이그레이션에最適이다. |
| **AKS (Azure Kubernetes Service)** | Azure의管理型 Kubernetes로, Azure AD 및 모니터링 도구와原生統合されている。 |
| **Azure AD (Microsoft Entra ID)** | Azure의 IAM 서비스로, 온프레미스 AD와Federation되어 SSO를 제공한다. |
| **Azure Functions** | Azure의 서버리스 함수 서비스로, Durable Functions를 통해 상태 유지 함수를 지원한다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. Azure는/are三星電子製品との統合に似た thingです。 삼성스마트폰과 삼성 스마트 TV, 삼성 전자레인지が 모두同一个 앱（Microsoft生态系）で繋がっている 것처럼, Azure도 Microsoft製品군（.NET, SQL Server, Teams 등）と紧密하게 연결되어 있습니다.
2. Azure AD（Microsoft Entra ID）는/are 같은 회사원의 출입카드와 같습니다. 한 번 카드를 치면（一次 인증）社内 모든 시설（Azure 자원）에 출입이 가능해서,额外的 인증 없이도 모든 것에 접근할 수 있어요.
3. Azure Functions는/aredynamically部署される简易宿舎のようなものです。旅行者に宿舎（関数运行环境）をその場で提供し、旅行終わり（関数終了）と同時に宿舎も消える（資源解放）する仕組みです.
