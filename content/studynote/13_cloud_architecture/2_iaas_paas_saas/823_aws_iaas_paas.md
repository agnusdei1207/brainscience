+++
weight = 18
title = "AWS 주요 서비스 (IaaS/PaaS)"
description = "AWS의 IaaS/PaaS 대표 서비스와 활용"
date = 2026-03-26

[taxonomies]
tags = ["cloud", "aws", "ec2", "lambda", "s3", "rds", "eks"]
+++
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: AWS는 2006년 출시 이후 200개 이상의 서비스를 제공하는 클라우드 플랫폼으로, IaaS (EC2, S3, VPC), PaaS (Lambda, RDS, Elastic Beanstalk), SaaS (QuickSight, Chime) 全層을 cover하며, 시장 점유율 30% 이상으로 업계 리더다.
> 2. **가치**: Amazon의 e-Commerce 운영에서 도출된 대규모 분산 시스템의 운영 경험과テクノロジーが注入되어 있어,信頼性と拡張性에서業界最高水準을 자랑한다.
> 3. **융합**: AWS는 단순한 IaaS/PaaS를 넘어 AI/ML (SageMaker), IoT (IoT Core), Media Services, Security (Macie, GuardDuty) 등 매우 폭넓은领域을 services로 제공한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### AWS 개요

Amazon Web Services (AWS)는 2006년亚马逊가 온라인Commerce의多余한 IT 인프라를 외부에 서비스로 제공하기 시작하면서诞obal 클라우드 시장 Leader가됐다. AWS는全세계 31개 지역 99개 가용 영역 (AZ) 을 운영하며, 200개 이상의 서비스를 통해 全산업의 IT 요구를 대응하고 있다.

### 비유

AWSの全体像は/are巨大な商業施設のテナントモールと 같습니다。 EC2（S3などの基礎サービス）から SageMaker（AI/ML）まで、从小卖部（基本インフラ）から 百貨店（先進技術）까지多种多样的業種の店が入り、各業種が自分の必要に最も近い店を選んで買い物ができる構造です。

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### AWS IaaS 핵심 서비스

#### Amazon EC2 (Elastic Compute Cloud)

EC2는 AWS의 핵심 IaaS 서비스로, 안전하고 크기 조정이 가능한 컴퓨팅 용량을 제공한다. 인스턴스 유형은 목적에 따라 구분된다: T 시리즈 (T3, T4 - Balances), M 시리즈 (M5, M6 - General Purpose), C 시리즈 (C5, C6 - Compute Optimized), R 시리즈 (R5, R6 - Memory Optimized), X 시리즈 (X2gd - Memory Optimized) 등 다양한 옵션이 있다. EC2의 핵심 기능으로는 Auto Scaling, Placement Groups, Enhanced Networking (ENA), Nitro System 등이 있다.

#### Amazon S3 (Simple Storage Service)

S3는 객체 스토리지 서비스로, 11-nine (99.999999999%) 의 내구성을 자랑한다. 스토리지 클래스는 Standard, Intelligent-Tiering, Standard-IA, Glacier, Glacier Deep Archive 등으로 구분되며, 데이터의 접근 빈도에 따라自動的に階級化된다. S3는 정적 웹사이트 호스팅, 데이터 레이크, 백업/아카이빙, 빅데이터 분석 등 매우 넓은領域で活用される。

#### Amazon VPC (Virtual Private Cloud)

VPC는 AWS 클라우드 내의 논리적으로 격리된 가상 네트워크로, 온프레미스 네트워크 환경과 유사한 네트워크 구성 제공한다. 서브넷 (Public/Private), 라우팅 테이블, 인터넷 게이트웨이, NAT Gateway, VPN, Direct Connect, Security Group, NACL, VPC Peering, Transit Gateway 등을 활용하여高度の 네트워크 아키텍처를構築할 수 있다.

AWS IaaS 핵심 서비스들의 관계를 시각화하면, EC2, S3, VPC가 어떻게 함께 작동하여 완전한 인프라를 구성하는지 파악할 수 있다.

```text
  ┌────────────────────────────────────────────────────────────────────┐
  │                    AWS IaaS 핵심 서비스 관계도                          │
  ├────────────────────────────────────────────────────────────────────┤
  │
  │  ┌──────────────────────────────────────────────────────────────┐  │
  │  │                         Amazon VPC                           │  │
  │  │  (논리적으로 격리된 가상 네트워크)                               │  │
  │  │                                                              │  │
  │  │  ┌──────────────────────────┐  ┌──────────────────────────┐  │  │
  │  │  │    Public Subnet        │  │    Private Subnet        │  │  │
  │  │  │                         │  │                         │  │  │
  │  │  │  ┌──────────────────┐  │  │  ┌──────────────────┐  │  │  │
  │  │  │  │   EC2 Instance   │  │  │  │   EC2 Instance   │  │  │  │
  │  │  │  │  (Web Server)    │  │  │  │  (App Server)    │  │  │  │
  │  │  │  │  Port: 80, 443  │  │  │  │  Port: 8080     │  │  │  │
  │  │  │  └────────┬─────────┘  │  │  └────────┬─────────┘  │  │  │
  │  │  │           │            │  │           │            │  │  │
  │  │  │  Security Group       │  │  │  Security Group      │  │  │
  │  │  │  Allow: 80,443       │  │  │  Allow: 8080 (from  │  │  │
  │  │  │  Deny: all           │  │  │  SG-Web)           │  │  │
  │  │  └────────┬─────────┘  │  │  └────────┬─────────┘  │  │  │
  │  │           │            │  │           │            │  │  │
  │  │           └────────────┼─────────────┘            │  │  │
  │  │                        │                          │  │  │
  │  └────────────────────────┼───────────────────────────┘  │  │
  │                           │                               │  │
  │  ┌────────────────────────┴───────────────────────────┐  │
  │  │                    Internet Gateway                 │  │
  │  │                    (공용 인터넷 연결)                 │  │
  │  └────────────────────────────────────────────────────┘  │
  │                                                              │
  │  ┌────────────────────────────────────────────────────┐  │
  │  │                   Amazon S3                         │  │
  │  │              (Object Storage)                        │  │
  │  │   버킷: static-assets, app-data-backup              │  │
  │  │   가용성: 99.99%, 내구성: 11-nine                  │  │
  │  └────────────────────────────────────────────────────┘  │
  │                                                              │
  │  Public Subnet: 외부 접근 가능 (ELB, NAT Gateway 배치)       │
  │  Private Subnet: 외부 직접 접근 불가 (DB, App Server 배치)    │
  └────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 아키텍처는 웹 애플리케이션의 전형적인 3계층 구조를 보여준다. Public Subnet에는 외부에서 접근 가능한 웹 서버 (EC2)가 위치하고, Private Subnet에는 외부에서 직접 접근할 수 없는 애플리케이션 서버와 데이터베이스가 위치한다. Security Group은 Stateful防火墙로, inbound 규칙에 따라 허용된トラフィック만 인입되고, outbound는 자동 허용된다. 이렇게 하면 외부 공격자로부터 보호해야 할 애플리케이션 서버와 DB는直接 노座을 차단하고, Public Subnet의 웹 서버를 경유해서만 접근할 수 있는 다중 방어 체계가 된다.

### AWS PaaS 핵심 서비스

#### AWS Lambda

Lambda는 서버리스 함수 실행 서비스로, 함수를 실행한 시간 (밀리초 단위) 만큼만 비용이 부과된다. Cold Start, Warm Pool, Provisioned Concurrency, SnapStart (Java) 등의 개념이 있으며, S3 트리거, API Gateway, SQS, CloudWatch Events 등 다양한 이벤트 소스와 연계된다.

#### Amazon RDS (Relational Database Service)

RDS는 MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora를 지원하는 관리형 관계형 DB 서비스다. Multi-AZ 배치, Read Replica, Automated Backup, Performance Insights, Enhanced Monitoring 등의 기능을 제공한다. 그러나 RDS는 SSH 접근이 불가능하고, 직접 OS에ログイン하여いじることもできない 因此に 管理簡易성과引き換えに 일부 유연성을 상실한다.

#### Amazon EKS (Elastic Kubernetes Service)

EKS는 완전 관리형 Kubernetes 서비스로, Kubernetes 控制プレーン (API Server, etcd, Scheduler, Controller Manager) 의 가용성과更新을 AWS가 관리한다. Fargate (サーバーレスクラスタ) 와의統合により、ユーザーはノード管理から開放される。 Karpenterとの統合により、ワークロードに最も适合したノードを自動的にプロビジョニングできる。

### 섹션 요약 비유

AWS 서비스들의関係は/are大都市の地下鉄路線図と 같습니다。 EC2（S3などの基礎サービス）から SageMaker（AI/ML）까지、基本路線（コアサービス）から 高급 노선（先进サービス）까지系统的に整然と結びつけられており、一而易に乗り換え（サービス間連携）江湖ができます。

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교: AWS vs Azure vs GCP

| 서비스 카테고리 | AWS | Azure | GCP |
|:---|:---|:---|:---|
| **IaaS (컴퓨팅)** | EC2 | Azure Virtual Machines | Compute Engine |
| **IaaS (스토리지)** | S3 | Blob Storage | Cloud Storage |
| **PaaS (DB)** | RDS, Aurora | Azure SQL, Cosmos DB | Cloud SQL, Cloud Spanner |
| **PaaS (컨테이너)** | EKS | AKS | GKE |
| **FaaS (서버리스)** | Lambda | Azure Functions | Cloud Functions |
| **AI/ML** | SageMaker | Azure ML | Vertex AI |
| **시장 점유율 (2024)** | ~31% | ~25% | ~10% |

### 과목 융합 관점

- **네트워크 (Network)**: AWS의 VPC, Direct Connect, Route 53, CloudFront는 네트워크 관점에서 全方位的인 서비스를 提供하여、온프레미스-클라우드 통합 네트워크 아키텍처 구축이 가능하다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 3계층 웹 애플리케이션 아키텍처**: AWS에서3계층 (Web-App-DB) 아키텍처를 구축했다. Public Subnet에 ALB (Application Load Balancer) 와 웹 서버 (EC2 Auto Scaling Group) 를 배치하고, Private Subnet에 애플리케이션 서버와 RDS (Multi-AZ) 를 배치하여, 외부 공격으로부터 DB를 격리하고 高가용성을 달성했다.

### 도입 체크리스트

- **기술적**: VPC 설계 시 IP 주소 대역이 온프레미스와 중복되지 않는가? 다중 AZ 구성을 통해 단일 장애점을 제거했는가?
- **운영·보안적**: IAM 역할과 Security Group을 Least Privilege 원칙으로 설정했는가? CloudTrail로 API 활동 로깅을 활성화했는가?

### 섹션 요약 비유

AWS 리전/AZ 아키텍처は/are Tokyo의Tokyo Metroと 같습니다。 主要駅（AZ）가互いに離れており、 하나의駅が營小女孩（AZ障害）でも他の駅（他のAZ）を通じて都市（Mリージョン）全体が机能し続けます.

---

## Ⅴ. 기대효과 및 결론

AWS는业界最大規模のサービスポートフォリオを持ち、IaaS/PaaS/SaaS 全層をカバーする。그러나 서비스 수가 많다는 것은それ自体がComplexityを意味し、服務選定と架構設計에 충분한 전문성이 필요하다.

### 섹션 요약 비유

AWSの全体的な価値は/are食べログ夢を彷彿とさせます。 多种多様なレストラン（サービス）から自分の머니散と嗜場合に最も近い餐厅（ワーク로드에 적합한 서비스）を選んで可以利用し、それだけで一生の美食体験（IT 要求）をすべて賄うことができる構造です.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **EC2 (Elastic Compute Cloud)** | AWS의 대표 IaaS 서비스로, 다양한 인스턴스 유형과 오토 스케일링 기능을 제공한다. |
| **S3 (Simple Storage Service)** | AWS의 객체 스토리지로, 11-nine의 내구성과 다양한 스토리지 클래스를 제공한다. |
| **VPC (Virtual Private Cloud)** | AWS 내 논리적으로 격리된 가상 네트워크로, 온프레미스 네트워크와 유사한 구성 가능 |
| **Lambda** | AWS의 서버리스 함수 실행 서비스로, 밀리초 단위의 실행 시간만 과금된다. |
| **RDS (Relational Database Service)** | AWS의 관리형 관계형 DB 서비스로, 다중 AZ, 읽기 복제본, 자동 백업을 지원한다. |
| **EKS (Elastic Kubernetes Service)** | AWS의 관리형 Kubernetes로, 완전한 Kubernetes API 호환성과 Fargate 통합을 제공한다. |
| **IAM (Identity and Access Management)** | AWS의 접근 제어 서비스로, 역할, 정책, 임시 자격 증명을 통한 세밀한 권한 관리를 제공한다. |

---

## 👶 어린이를 위한 3줄 비유 설명
1. AWSは/are巨大的な游園地のテーマパークと 같습니다。乘坐できるアイテム（サービス）が200種以上もあり、从小型的旋转木马（EC2）から巨大的なコースター（AI/ML）まで揃っています.
2. VPCは/街区设计与 같습니다。テーマパーク场内（VPC）には回遊者（トラフィック）专用の道（サブネット）が設計されており、危険なアトラクション（DBサーバ）は裏口（プライベートサブネット）에만 배치되어 있습니다.
3. Lambdaは/自动販売機のafricと 같습니다。想要の饮料（関数）を押すと（トリガー）その場で饮料 나와（実行）되고, 何も购买하지 않으면（未使用） 비용이 들지 않는 구조입니다.
