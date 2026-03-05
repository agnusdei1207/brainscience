+++
title = "테라폼 (Terraform)"
description = "HashiCorp가 개발한 오픈소스 IaC(Infrastructure as Code) 도구로 선언적 구성 언어(HCL)를 사용하여 멀티 클라우드 인프라를 프로비저닝하고 관리"
date = 2024-05-15
[taxonomies]
tags = ["Terraform", "IaC", "Infrastructure-as-Code", "DevOps", "Cloud", "HCL"]
+++

# 테라폼 (Terraform)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인프라를 코드(Infrastructure as Code)로 정의하여, AWS, Azure, GCP 등 멀티 클라우드 리소스를 선언적(Declarative) 구성 언어(HCL)로 프로비저닝하고, 상태 파일(tfstate)로 실제 인프라와 동기화하며 버전 관리하는 오픈소스 도구입니다.
> 2. **가치**: 'ClickOps'(수동 콘솔 클릭) 방식의 재현 불가능성, 설정 드리프트(Drift), 감사 추적 불가 문제를 해결하여 인프라 변경을 Git 기반으로 관리하고, 롤백을 코드 되돌리기만 하면 되는 수준으로 단순화합니다.
> 3. **융합**: GitOps(ArgoCD와 연동), CI/CD 파이프라인, 정책 애즈 코드(OPA/Checkov), 시크릿 관리(Vault)와 결합하여 엔터프라이즈급 IaC 플랫폼을 구축합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**테라폼(Terraform)**은 HashiCorp가 개발한 오픈소스 **IaC(Infrastructure as Code)** 도구로, 인프라 리소스(서버, 네트워크, 스토리지, DNS, SaaS 서비스 등)를 **선언적(Declarative) 코드**로 정의하고 관리합니다. 핵심 개념:
- **HCL(HashiCorp Configuration Language)**: 테라폼 전용 선언적 언어 (JSON 호환)
- **Provider**: AWS, Azure, GCP, Kubernetes 등 클라우드/서비스 API와 통신하는 플러그인
- **Resource**: 생성할 인프라 객체 (EC2 인스턴스, S3 버킷, VPC 등)
- **State(tfstate)**: 실제 인프라와 코드 간의 매핑을 저장하는 상태 파일
- **Plan**: 실행 전 변경 사항 미리보기 (Dry-run)
- **Apply**: 실제 인프라에 변경 사항 적용

테라폼은 "어떻게 만들지(How)"가 아니라 "무엇을 만들지(What)"를 선언하면, Provider가 API를 호출하여 자동으로 생성합니다.

### 2. 구체적인 일상생활 비유
레고 조립 설명서를 상상해 보세요. 테라폼 코드는 **"이 블록들을 이 순서대로 조립하라"**는 설명서입니다. 테라폼을 실행하면 로봇 팔이 설명서대로 블록을 조립합니다. 설명서를 수정하면(코드 변경), 로봇은 추가된 블록을 붙이고, 삭제된 블록을 떼어냅니다. 설명서를 Git에 저장해두면, 언제든 이전 버전으로 되돌려 똑같은 레고를 다시 조립할 수 있습니다. 수동으로 블록을 붙였다 떼는 것이 아니라, 설명서(코드)만 관리하면 됩니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (ClickOps와 Snowflake Server)**:
   클라우드 초기에는 관리자가 AWS 콘솔에 로그인하여 마우스로 EC2, S3, VPC를 생성했습니다. 이 방식의 문제점: 1) 재현 불가능 (어떤 순서로 클릭했는지 기억 안 남) 2) Snowflake Server (모든 서버가 조금씩 다름) 3) 감사 추적 불가 (누가 언제 무엇을 변경했는지 모름) 4) 롤백 불가능 (이전 상태로 되돌릴 방법 없음).

2. **혁신적 패러다임 변화의 시작**:
   2014년 HashiCorp가 테라폼을 발표하며 "인프라도 코드처럼 버전 관리하고, 리뷰하고, 테스트하자"는 IaC 패러다임을 대중화했습니다. AWS CloudFormation(2011)은 AWS 전용이었으나, 테라폼은 멀티 클라우드(AWS, Azure, GCP, K8s, Datadog 등)를 단일 도구로 관리 가능하게 했습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   멀티 클라우드 전략, 하이브리드 클라우드, 규정 준수(SOC 2, ISO 27001) 요구사항으로 인해 IaC는 선택이 아닌 필수가 되었습니다. 미국 연방정부, 금융권, 대기업 모두 테라폼을 표준 IaC 도구로 채택하고 있습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **HCL Configuration** | 인프라 선언적 정의 | 리소스, 변수, 출력, 지역 변수 블록 | .tf 파일 | 레고 설명서 |
| **Provider** | 클라우드 API 통신 | SDK 사용하여 REST/gRPC API 호출 | AWS, Azure, GCP, K8s | 레고 조립 로봇 |
| **Resource** | 인프라 객체 정의 | 생성, 수정, 삭제 로직 자동 판단 | aws_instance, azurerm_vm | 레고 블록 |
| **State (tfstate)** | 코드와 실제 인프라 매핑 | JSON 형식으로 리소스 ID, 속성 저장 | S3, Terraform Cloud | 조립 완료 사진 |
| **Plan Graph** | 변경 사항 DAG 생성 | 의존성 분석 후 실행 순서 결정 | terraform graph | 조립 순서도 |
| **Backend** | State 파일 저장소 | 잠금(Lock)으로 동시 수정 방지 | S3+DynamoDB, Consul | 설명서 보관함 |

### 2. 정교한 구조 다이어그램: 테라폼 실행 사이클

```text
=====================================================================================================
                      [ Terraform Execution Cycle & Architecture ]
=====================================================================================================

  [ Developer ]                 [ Terraform Core ]                 [ Cloud Providers ]
       |                              |                                    |
       | 1. Write .tf files           |                                    |
       v                              |                                    |
+-------------+                       |                                    |
| main.tf     |                       |                                    |
| variables.tf|                       |                                    |
| outputs.tf  |                       |                                    |
+------+------+                       |                                    |
       |                              |                                    |
       | 2. terraform init            |                                    |
       +----------------------------> |                                    |
       |                              | 3. Download Providers              |
       |                              |    +-------------+                 |
       |                              |    | AWS Provider|                 |
       |                              |    | Azure Prov. |                 |
       |                              |    +------+------+                 |
       |                              |           |                        |
       | 4. terraform plan            |           |                        |
       +----------------------------> |           |                        |
       |                              | 5. Read State                       |
       |                              |    +-------------+                 |
       |                              |    | tfstate     |                 |
       |                              |    | (S3 Backend)|                 |
       |                              |    +------+------+                 |
       |                              |           |                        |
       |                              | 6. Refresh (API Calls)              |
       |                              |           |                        |
       |                              |           +----------------------> |
       |                              |           |   GET /instances      |
       |                              |           <---------------------- |
       |                              |           |   Actual Resources    |
       |                              |           |                        |
       |                              | 7. Compare: Code vs State vs Real  |
       |                              |    +----------------------------+ |
       |                              |    | Plan Output:               | |
       |                              |    | + aws_instance.web (new)   | |
       |                              |    | ~ aws_s3_bucket.data (mod) | |
       |                              |    | - aws_lb.old (destroy)     | |
       |                              |    +----------------------------+ |
       |                              |                                    |
       | 8. terraform apply           |                                    |
       +----------------------------> |                                    |
       |                              | 9. Execute DAG (Dependency Order) |
       |                              |    +----------------------------+ |
       |                              |    | Execution Order:            | |
       |                              |    | 1. VPC                      | |
       |                              |    | 2. Subnet                   | |
       |                              |    | 3. Security Group           | |
       |                              |    | 4. EC2 Instance             | |
       |                              |    +----------------------------+ |
       |                              |           |                        |
       |                              | 10. API Calls                       |
       |                              |           +----------------------> |
       |                              |           |   POST /instances     |
       |                              |           <---------------------- |
       |                              |           |   Resource Created    |
       |                              |                                    |
       |                              | 11. Update State                    |
       |                              |    +-------------+                 |
       |                              |    | tfstate     |                 |
       |                              |    | (Updated)   |                 |
       |                              |    +-------------+                 |
       |                              |                                    |
       | 12. Outputs                   |                                    |
       <---------------------------- |                                    |
       |  instance_ip = "1.2.3.4"     |                                    |
       v                              v                                    v

=====================================================================================================
```

### 3. 심층 동작 원리 (핵심 메커니즘)

**1. 선언적 구성 (Declarative Configuration)**
테라폼은 "이 EC2 인스턴스가 있어야 한다"고 선언합니다. "인스턴스를 생성하는 명령"을 내리는 것이 아닙니다. 테라폼이 알아서:
- 인스턴스가 없으면 생성
- 속성이 다르면 수정
- 코드에서 삭제되었으면 실제 리소스도 삭제

이를 통해 멱등성(Idempotency)을 보장합니다. 같은 코드를 100번 실행해도 결과는 동일합니다.

**2. 상태 관리 (State Management)**
tfstate 파일은 코드와 실제 인프라 간의 매핑을 저장합니다:
```json
{
  "resources": [
    {
      "type": "aws_instance",
      "name": "web",
      "instances": [{
        "attributes": {
          "id": "i-1234567890abcdef0",
          "ami": "ami-0c55b159cbfafe1f0",
          "instance_type": "t3.micro"
        }
      }]
    }
  ]
}
```
State가 없으면 테라폼은 매번 모든 리소스를 새로 생성하려 합니다. State를 통해 이미 존재하는 리소스를 식별합니다.

**3. 의존성 그래프 (Dependency Graph)**
테라폼은 리소스 간 의존성을 자동으로 분석하여 DAG(Directed Acyclic Graph)를 생성합니다:
```hcl
resource "aws_vpc" "main" { ... }          # 1번째 실행
resource "aws_subnet" "public" {           # VPC 생성 후 실행
  vpc_id = aws_vpc.main.id
}
resource "aws_instance" "web" {            # Subnet 생성 후 실행
  subnet_id = aws_subnet.public.id
}
```
명시적 의존성(depends_on)과 암시적 의존성(참조) 모두 처리합니다.

### 4. 핵심 알고리즘 및 실무 코드 예시

**테라폼 모듈 구조 (프로덕션급)**

```hcl
# main.tf - Root module
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote backend for state management
  backend "s3" {
    bucket         = "myorg-terraform-state"
    key            = "prod/infrastructure/terraform.tfstate"
    region         = "ap-northeast-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"  # State locking
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      ManagedBy   = "Terraform"
      Environment = var.environment
      Project     = "myapp"
    }
  }
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# VPC Module
module "vpc" {
  source  = "./modules/vpc"
  version = "1.0.0"

  vpc_cidr           = var.vpc_cidr
  availability_zones = ["ap-northeast-2a", "ap-northeast-2c"]
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets    = ["10.0.10.0/24", "10.0.11.0/24"]

  tags = {
    Environment = var.environment
  }
}

# EC2 Instance
resource "aws_instance" "web" {
  count = var.instance_count

  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  subnet_id              = module.vpc.public_subnet_ids[count.index % length(module.vpc.public_subnet_ids)]
  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    environment = var.environment
  }))

  tags = {
    Name = "web-${var.environment}-${count.index + 1}"
  }

  lifecycle {
    create_before_destroy = true  # Zero-downtime updates
    ignore_changes        = [ami] # Ignore AMI changes after creation
  }
}

# Security Group
resource "aws_security_group" "web" {
  name        = "web-sg-${var.environment}"
  description = "Security group for web servers"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "HTTP from ALB"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  ingress {
    description = "SSH from Bastion"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Outputs
output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "instance_ids" {
  description = "IDs of EC2 instances"
  value       = aws_instance.web[*].id
}

output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}
```

**CI/CD 파이프라인 통합 (GitHub Actions)**

```yaml
# .github/workflows/terraform.yml
name: Terraform CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.5.7

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ap-northeast-2

      - name: Terraform Init
        run: terraform init

      - name: Terraform Format Check
        run: terraform fmt -check

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        id: plan
        run: terraform plan -no-color -out=tfplan
        continue-on-error: true

      - name: Post Plan to PR
        uses: actions/github-script@v7
        with:
          script: |
            const output = `#### Terraform Plan
            \`\`\`
            ${{ steps.plan.outputs.stdout }}
            \`\`\``;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });

      - name: Terraform Apply (main branch only)
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve tfplan
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: IaC 도구 비교

| 평가 지표 | Terraform | AWS CloudFormation | Pulumi | Ansible |
| :--- | :--- | :--- | :--- | :--- |
| **언어** | HCL (선언형) | YAML/JSON | Python/TS/Go | YAML |
| **멀티 클라우드** | 지원 (100+ Provider) | AWS 전용 | 지원 | 지원 |
| **상태 관리** | tfstate (필수) | AWS 관리 | Pulumi Cloud | 없음 |
| **프로비저닝** | 지원 | 지원 | 지원 | 제한적 |
| **구성 관리** | 미지원 | 미지원 | 미지원 | 핵심 기능 |
| **학습 곡선** | 중간 | 낮음 | 높음 (코딩 필요) | 낮음 |
| **롤백** | 코드로 되돌리기 | 자동 롤백 | 코드로 되돌리기 | 수동 |

### 2. 과목 융합 관점 분석

**Terraform + GitOps**
- 테라폼 코드를 Git에 커밈하면 자동으로 terraform plan/apply를 실행하는 GitOps 워크플로우 구축 (Atlantis, Terraform Cloud, Spacelift).

**Terraform + 보안 (Policy as Code)**
- OPA(Open Policy Agent), Checkov, tfsec으로 테라폼 코드를 정적 분석하여 보안 위반(S3 퍼블릭 오픈, 암호화 미사용)을 CI 단계에서 차단.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 멀티 리전 DR 환경 구축**
- **문제점**: 서울(ap-northeast-2) 리전 장애 시 Tokyo(ap-northeast-1) 리전으로 페일오버해야 합니다.
- **기술사 판단 (전략)**: 테라폼 모듈로 리전 독립적인 인프라 정의. variables.tf로 region 변수화. `terraform workspace` 또는 별도 디렉토리로 각 리전 관리. Route53 헬스 체크와 페일오버 라우팅 정책을 테라폼으로 관리.

**[상황 B] State 파일 충돌 (동시 수정)**
- **문제점**: 두 명의 엔지니어가 동시에 terraform apply를 실행하여 State가 손상되었습니다.
- **기술사 판단 (전략)**: S3 Backend + DynamoDB Lock 테이블 구성. State 잠금이 자동으로 획득되어 동시 실행 방지. Terraform Cloud로 마이그레이션하면 팀 협업 기능(Run Triggers, Policy as Code) 추가 활용.

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] State 저장소: S3 + DynamoDB, Terraform Cloud, 또는 Consul?
- [ ] 모듈 전략: Private Module Registry 구축?
- [ ] Secret 관리: tfvars에 하드코딩 금지, Vault 또는 AWS Secrets Manager 사용

**운영적 고려사항**
- [ ] State 잠금: DynamoDB 등으로 동시 수정 방지
- [ ] 권한 관리: IAM Role로 최소 권한 원칙 적용
- [ ] 변경 관리: PR 기반 리뷰 프로세스 수립

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: tfstate를 Git에 커밋**
- State 파일에는 민감 정보(password, token)가 평문으로 포함될 수 있습니다. 반드시 암호화된 원격 백엔드(S3 + KMS)를 사용해야 합니다.

**안티패턴 2: 수동 수정(ClickOps)과 테라폼 혼용**
- 테라폼으로 생성한 리소스를 AWS 콘솔에서 수동으로 수정하면 State와 실제 리소스가 불일치(Drift)합니다. 모든 변경은 테라폼 코드를 통해서만 수행해야 합니다.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 수동 관리 (AS-IS) | 테라폼 적용 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **인프라 프로비저닝 시간** | 수 시간~수 일 | 수 분~수 십 분 | **90% 단축** |
| **환경 재현성** | 불가능 (Snowflake) | 100% (동일 코드) | **재현성 보장** |
| **감사 추적** | 없음 | Git 커밋 히스토리 | **완전한 추적** |
| **구성 드리프트** | 빈번함 | 자동 탐지 및 수정 | **드리프트 제로** |
| **롤백 시간** | 수 시간 | `git revert` 후 apply | **롤백 99% 단축** |

### 2. 미래 전망 및 진화 방향
- **Terraform Cloud/Enterprise**: 협업 기능, Policy as Code, Private Module Registry, Run Triggers 등 엔터프라이즈 기능 강화.
- **CDK for Terraform (CDKTF)**: TypeScript, Python, Go 등 프로그래밍 언어로 테라폼 구성 작성 가능.

### 3. 참고 표준/가이드
- **HashiCorp Terraform Best Practices**: 공식 모범 사례 가이드
- **AWS Well-Architected Framework**: IaC 기반 인프라 설계 원칙
- **CIS Benchmarks**: 테라폼 보안 구성 가이드

---

## 관련 개념 맵 (Knowledge Graph)
- **[IaC 개념](@/studynotes/15_devops_sre/4_iac/iac_fundamentals.md)**: Infrastructure as Code 기본 원칙
- **[불변 인프라](@/studynotes/15_devops_sre/4_iac/immutable_infrastructure.md)**: 테라폼이 구현하는 인프라 패러다임
- **[Ansible](@/studynotes/15_devops_sre/4_iac/ansible.md)**: 구성 관리(Configuration Management) 도구
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/3_automation/continuous_integration.md)**: 테라폼 자동화 인프라
- **[DevSecOps](@/studynotes/15_devops_sre/5_devsecops/devsecops_principles.md)**: IaC 보안 스캔

---

## 어린이를 위한 3줄 비유 설명
1. 레고를 조립할 때 **설명서만 있으면** 누구나 똑같은 모양을 만들 수 있어요!
2. 테라폼은 이 설명서를 **컴퓨터가 읽을 수 있는 코드**로 만들어서, 버튼만 누르면 로봇이 알아서 조립해줘요.
3. 덕분에 설명서를 친구에게 보내주면, 멀리 있는 친구도 똑같은 레고를 만들 수 있답니다!
