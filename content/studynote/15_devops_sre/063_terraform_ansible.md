+++
weight = 63
title = "63. Terraform/Ansible (테라폼/앤서블)"
date = "2026-04-05"
[extra]
categories = "studynote-devops-sre"
+++

# Terraform/Ansible (테라폼/앤서블)

> ⚠️ 이 문서는 IaC(Infrastructure as Code) 분야의 대표적인 두 도구인 Terraform과 Ansible의 철학적 배경, 아키텍처 차이, 각각의 강점과 한계, 그리고 실무에서 선택과 활용에 대한 체계적 비교 분석입니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Terraform은 인프라 자원의 생성/삭제를 담당하는 선언형 프로비저닝 도구이며, Ansible은 이미 생성된 자원의 설정을 관리하는 명령형 구성 관리 도구입니다. 둘 다 IaC의实现이며, 실무에서는互补적으로 함께 사용되는 경우가 많습니다.
> 2. **가치**: Terraform은 "어떤 인프라를 만들어야 하는지"를 코드로 선언하여 멀티 클라우드 환경을统一的に管理할 수 있게 하며, Ansible은 "이미 있는 서버에 어떻게 설정을 적용할지"를 태스크 나열로 관리하여 기존의 레거시 서버도代码化할 수 있게 합니다.
> 3. **선택 기준**: 인프라의 생성/삭제/변경이 빈번하면 Terraform을, 기존 서버의 설정 관리/애플리케이션 배포가 주요 업무이면 Ansible을 선택하는 것이 일반적이며, 많은 조직에서 두 도구를 모두 활용합니다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 1. Terraform과 Ansible의誕生 배경제이

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│              [ Terraform과 Ansible의 탄생 배경 비교 ]                            │
│                                                                              │
│  Terraform (2014, HashiCorp)                                                  │
│  ──────────────────────────────────────────────                            │
│  • 문제: AWS, GCP, Azure 등 각 클라우드의 API가 다르다                         │
│         →同一スクリプトで複数のクラウドを管理することは困難                           │
│  • 해결: 各クラウドのAPI를 추상화한 Provider(plugin) 구조                      │
│         → 하나의 HCL 언어로 1,000+ 클라우드/서비스 관리 가능                  │
│                                                                              │
│  Ansible (2012, Red Hat)                                                      │
│  ──────────────────────────────────────────────                            │
│  • 문제: 수백 대의 서버에同一个 설정을 적용하려면? (SSH 수동 접속...)          │
│  • 해결: SSH 기반으로 설정 작업을 자동화 → 에이전트 불필요                       │
│         → YAML 기반으로 누구나 쉽게 작성 가능                                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2. Terraform vs Ansible: 다른 문제를 풀고 있다

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│              [ Terraform과 Ansible의 관점 차이 ]                                │
│                                                                              │
│  Terraform视角: "인프라를 Architecture도"                                       │
│  ────────────────────────────────────────                                    │
│                                                                              │
│      코드 (HCL)                                                               │
│         │                                                                     │
│         ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐          │
│  │ VPC 생성 ──▶ Subnet 생성 ──▶ EC2 생성 ──▶ RDS 생성 ──▶ 应用 배포 │          │
│  │                                                              │          │
│  │ [선언형: "이렇게 된インフラストラクチャがほしい"]                              │          │
│  └─────────────────────────────────────────────────────────────────┘          │
│                                                                              │
│  Ansible视角: "서버 안에 기능을 부여한다"                                       │
│  ────────────────────────────────────────                                    │
│                                                                              │
│      코드 (YAML)                                                              │
│         │                                                                     │
│         ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐          │
│  │ 패키지 설치 ──▶ 설정 파일 복사 ──▶ 서비스 시작 ──▶ 방화벽 설정 ──▶ 배포  │          │
│  │                                                              │          │
│  │ [명령형: "이 서버에서 이 단계들을 순서대로 실행하라"]                     │          │
│  └─────────────────────────────────────────────────────────────────┘          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3. 함께 사용할 때의 효과

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│              [ Terraform + Ansible: 보완적 활용 ]                               │
│                                                                              │
│  Terraform (인프라 생성)                                                       │
│  ────────────────────                                                         │
│  • VPC, Subnet, Route Table                                                  │
│  • EC2 Instance, Auto Scaling Group                                          │
│  • RDS, ElastiCache, S3                                                      │
│  • IAM Role, Security Group                                                 │
│                                                                              │
│          ↓                                                                   │
│                                                                              │
│  Ansible (서버 설정)                                                          │
│  ────────────────────                                                         │
│  • Nginx, Apache 설치 및 설정                                                │
│  • Java, Node.js, Python 런타임 설치                                         │
│  • 애플리케이션 코드 배포 (war, jar, zip)                                     │
│  •Monitoring Agent 설치 (Prometheus, DataDog)                                │
│  • 로그 роутирование 설정 (Fluentd, Filebeat)                                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Terraform과 Ansible의 관계는 "建筑业的现场负责人과 功能공의 관계"와 같습니다. Terraform은 "기초를打人하고( VPC, 서버 생성 ), 배관을 설치하고( 네트워크, 스토리지 ), 전선을 깔고( 로드밸런서, 캐시 ), 전체 건물의 골조( 인프라 )를construction"하는 현장 감독의 역할입니다. Ansible은 "각 방에 전구를 연결하고( 패키지 설치 ), 보일러를 설정하고( 설정 파일 ), 문 잠금장치를 점검하는( 보안 설정 ), 입주자에게 키를 넘기는( 애플리케이션 배포 ) 기능공"의 역할입니다. 건물만 짓고 입주시공( 애플리케이션 실행 )이 안 되면 의미가 없듯이, Terraform으로 인프라를 만들고 Ansible으로 상세 설정을 적용하는 것이 효과적입니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 (Architecture & Mechanism)

### 1. Terraform 아키텍처 상세

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Terraform 아키텍처 ]                                       │
│                                                                              │
│                      ┌─────────────────────┐                                  │
│                      │   .tf files (HCL)   │                                  │
│                      │   (IaC 코드)         │                                  │
│                      └──────────┬──────────┘                                  │
│                                 │                                             │
│                                 ▼                                             │
│                      ┌─────────────────────┐                                  │
│                      │   terraform init    │                                  │
│                      │  (Provider 다운로드) │                                  │
│                      └──────────┬──────────┘                                  │
│                                 │                                             │
│                                 ▼                                             │
│                      ┌─────────────────────┐                                  │
│                      │   terraform plan    │                                  │
│                      │  (실행 계획 생성)    │                                  │
│                      │  - 현재 상태 vs     │                                  │
│                      │    목표 상태 비교    │                                  │
│                      │  - 변경 사항Preview │                                  │
│                      └──────────┬──────────┘                                  │
│                                 │                                             │
│                                 ▼                                             │
│                      ┌─────────────────────┐                                  │
│                      │   terraform apply   │                                  │
│                      │  (실제 리소스 변경)   │                                  │
│                      │  1. 실행 plan 실행  │                                  │
│                      │  2. State 파일更新   │                                  │
│                      │  3. 실제 인프라 반영 │                                  │
│                      └──────────┬──────────┘                                  │
│                                 │                                             │
│                                 ▼                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                       Backend (State 저장소)                            │   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐               │   │
│  │   │   S3    │  │ DynamoDB│  │   GCS   │  │  Azure  │               │   │
│  │   │  (AWS)  │  │  (AWS)  │  │  (GCP)  │  │  Blob   │               │   │
│  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘               │   │
│  │                                                                       │   │
│  │   State 파일: 실제 인프라 상태의 "녹음"                                 │   │
│  │   Locking: 동시 apply 방지                                            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2. Ansible 아키텍처 상세

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Ansible 아키텍처 ]                                         │
│                                                                              │
│                      ┌─────────────────────┐                                  │
│                      │  Ansible Playbook    │                                  │
│                      │   (YAML, 태스크 목록) │                                  │
│                      └──────────┬──────────┘                                  │
│                                 │                                             │
│                                 ▼                                             │
│                      ┌─────────────────────┐                                  │
│                      │    Ansible Engine    │                                  │
│                      │  (실행 엔진)         │                                  │
│                      │  - 모듈 로더        │                                  │
│                      │  - 태스크 실행기     │                                  │
│                      │  -.inventory 파서   │                                  │
│                      └──────────┬──────────┘                                  │
│                                 │                                             │
│                                 ▼                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    SSH (Control Node → Managed Node)                   │   │
│  │                                                                       │   │
│  │   Control Node (Ansible 설치됨)                                       │   │
│  │   └── Ansible Engine                                                  │   │
│  │           │                                                          │   │
│  │           │ SSH (密码 or 키 인증)                                      │   │
│  │           │                                                          │   │
│  │           ▼                                                          │   │
│  │   Managed Node 1 ──▶ 실행: nginx 설치 + 설정 + 시작                    │   │
│  │   Managed Node 2 ──▶ 실행: nginx 설치 + 설정 + 시작                    │   │
│  │   Managed Node N ──▶ 실행: nginx 설치 + 설정 + 시작                    │   │
│  │                                                                       │   │
│  │   ※ 에이전트 불필요: SSH만으로 원격 실행 가능                           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3. Terraform 코드 예시

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "ap-northeast-2"
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = "ap-northeast-2"
}

# VPC 생성
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "prod-vpc"
    Environment = "production"
  }
}

# 서브넷 생성
resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "prod-private-subnet-${count.index + 1}"
  }
}

# EC2 인스턴스 생성
resource "aws_instance" "web" {
  count                  = 3
  ami                    = "ami-1234567890abcdef0"
  instance_type          = "t3.medium"
  subnet_id              = aws_subnet.private[count.index].id
  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = <<-EOF
              #!/bin/bash
              yum install -y nginx
              systemctl start nginx
              EOF

  tags = {
    Name = "web-server-${count.index + 1}"
  }
}

# Security Group
resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 4. Ansible Playbook 예시

```yaml
# playbook.yml
---
- name: Web Server Configuration
  hosts: webservers
  become: yes
  vars:
    nginx_version: "1.24.0"
    app_deploy_path: "/var/www/app"

  tasks:
    - name: Update package cache
      ansible.builtin.apt:
        update_cache: yes
      when: ansible_os_family == "Debian"

    - name: Install Nginx
      ansible.builtin.apt:
        name: nginx
        state: present

    - name: Copy Nginx configuration
      ansible.builtin.template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        mode: '0644'
      notify: Restart Nginx

    - name: Deploy application
      ansible.builtin.copy:
        src: "{{ item.src }}"
        dest: "{{ app_deploy_path }}/{{ item.dest }}"
        mode: '0644'
      loop:
        - { src: 'app.war', dest: 'app.war' }
        - { src: 'config.yml', dest: 'config.yml' }
      notify: Restart Application

    - name: Ensure Nginx is running
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: Restart Nginx
      ansible.builtin.service:
        name: nginx
        state: restarted

    - name: Restart Application
      ansible.builtin.systemd:
        name: myapp
        state: restarted
```

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### Terraform vs Ansible 기능 비교

| 구분 | Terraform | Ansible |
|:---|:---|:---|
| **IaC 유형** | 선언형 (Desired State) | 명령형 (Procedural) |
| **주요 기능** | 인프라 생성/삭제/변경 | 설정 관리, 애플리케이션 배포 |
| **대상** | Cloud API, 네트워크, 스토리지, VM 등 | OS 설정, 패키지, 서비스, 파일 |
| **실행 방식** | Plan → Apply (2단계) | 직접 실행 |
| **State 관리** | State 파일로 현재 상태 추적 | Stateless (현재 상태를 그때그때 파악) |
| **멀티 클라우드** | 1,000+ Provider 내장 | Cloud modules 있지만 Terraform 대비 제한적 |
| ** idempotency** | 자동 보장 (Provider가 처리) | 태스크 설계 시 주의 필요 |
| **에이전트** | 불필요 | 불필요 (SSH만 사용) |
| **강점** | 프로비저닝, 상태 관리 | 유연성, 기존 서버 관리 |
| **한계** | State 관리 복잡성 | 대규모 환경에서 속도 저하 가능성 |

### 언제 무엇을 사용할 것인가?

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ Terraform / Ansible 선택 가이드 ]                         │
│                                                                              │
│  Terraform을 선택해야 하는 경우 ✅                                              │
│  ──────────────────────────────────────────                                  │
│  • 새 인프라를 처음부터 생성해야 하는 경우                                       │
│  • 멀티 클라우드/멀티 환경 인프라를统一的に管理하는 경우                          │
│  • 인프라 상태의 정확한 추적과 버전 관리가 중요한 경우                            │
│  •基础设施를 코드로Audit해야 하는 규제 산업                                    │
│                                                                              │
│  Ansible을 선택해야 하는 경우 ✅                                                │
│  ──────────────────────────────────────────                                  │
│  • 이미 프로비저닝된 서버의 설정을 변경하는 경우                                  │
│  • 레거시 서버(Physical, VM)을 관리해야 하는 경우                               │
│  • 애플리케이션 코드/컨테이너를 배포하는 경우                                     │
│  • 설정 변경이 빈번하고 유연한 스크립트가 필요한 경우                             │
│                                                                              │
│  둘 다 함께 사용해야 하는 경우 ✅                                              │
│  ──────────────────────────────────────────                                  │
│  • Terraform으로 인프라 생성 → Ansible로 상세 설정 + 앱 배포                     │
│  • Ansible으로 생성된 자원의Terraform import                                    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Terraform과 Ansible의 선택은 "목적지에 도착하는交通수단"과 같습니다. Terraform은 "氵歶单机으로 목적지까지 직행하는" 것에 비유할 수 있습니다. 출발지(현재 인프라)에서目的地(완성된 인프라)까지의 경로(변경 사항)를 자동으로 계산하고, 가장 효율적인ルート로 이동합니다. Ansible은 "각 역에서 내리는旅客를降りて 다른交通수단을 찾는" 것에 비유할 수 있습니다. 각 서버(역)에서 내리고(현재 상태 확인), 다른交通수단(설정)을 타고( 패키지 설치), 다시 올라타는( 서비스 시작 ) 과정을 순차적으로 실행합니다. 결국 목적지가 인프라 생성(직행)인지, 서버 내 설정 변경(각 역에서 내림)인지에 따라交通수단을 선택해야 합니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

### Terraform + Ansible 통합 아키텍처

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│              [ Terraform + Ansible 통합 CI/CD 파이프라인 ]                        │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     CI/CD Pipeline                                     │   │
│  │                                                                       │   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │   │
│  │  │  Git     │───▶│Terraform │───▶│ Ansible  │───▶│  Verify  │      │   │
│  │  │  Commit  │    │  Plan    │    │  Apply   │    │          │      │   │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘      │   │
│  │       │              │               │               │                  │   │
│  │       │         (Approval)       (SSH to         (Smoke Test)          │   │
│  │       │          Gate)          Servers)                             │   │
│  │       │              │               │               │                  │   │
│  │       │              ▼               ▼               ▼                  │   │
│  │       │       ┌──────────┐    ┌──────────┐    ┌──────────┐          │   │
│  │       │       │ Human   │    │  Apply   │    │ Monitoring│          │   │
│  │       │       │ Review  │    │ complete │    │ dashboard │          │   │
│  │       │       └──────────┘    └──────────┘    └──────────┘          │   │
│  │       │                                                              │   │
│  └───────┼──────────────────────────────────────────────────────────────┘   │
│          │                                                                     │
│          ▼                                                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  순서: Git Push → Terraform Plan → (승인) → Ansible Playbook 실행      │   │
│  │                                                                       │   │
│  │  Terraform: VPC, Subnet, EC2, RDS 등 인프라 프로비저닝                   │   │
│  │  Ansible: nginx 설치, 애플리케이션 배포, 모니터링 설정                   │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Terraform Module vs Ansible Role 구조화

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    [ 모듈/롤 구조화 Best Practices ]                            │
│                                                                              │
│  Terraform 모듈 (재사용 가능한 인프라组件)                                        │
│  ──────────────────────────────────────────                                  │
│  modules/                                                                    │
│  ├── networking/                                                            │
│  │   ├── vpc.tf                                                            │
│  │   ├── subnet.tf                                                         │
│  │   └── outputs.tf                                                        │
│  ├── compute/                                                               │
│  │   ├── ec2.tf                                                            │
│  │   ├── asg.tf                                                            │
│  │   └── outputs.tf                                                        │
│  └── database/                                                              │
│      ├── rds.tf                                                            │
│      └── outputs.tf                                                        │
│                                                                              │
│  Ansible 롤 (재사용 가능한 설정 태스크)                                          │
│  ──────────────────────────────────────────                                  │
│  roles/                                                                     │
│  ├── nginx/                                                                 │
│  │   ├── tasks/main.yml                                                   │
│  │   ├── handlers/main.yml                                                 │
│  │   ├── templates/nginx.conf.j2                                          │
│  │   └── vars/main.yml                                                    │
│  ├── java/                                                                  │
│  │   ├── tasks/main.yml                                                   │
│  │   └── vars/main.yml                                                    │
│  └── myapp/                                                                 │
│      ├── tasks/main.yml                                                    │
│      ├── templates/app.conf.j2                                            │
│      └── defaults/main.yml                                                 │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Terraform 모듈과 Ansible 롤의 구조화는 "leman 공장의 부품 표준화"와 같습니다. Tesla 공장에서 모든 차종에通用的인 부품을 사용하듯이, Terraform 모듈과 Ansible 롤도 동일한 구조로再利用 가능합니다. 네트워크용 모듈( VPC, Subnet )과 계산용 모듈( EC2, ASG ), 데이터베이스용 모듈( RDS )을組み合わせることで 새로운 모델( 인프라 )을 빠르게 구축할 수 있습니다. 또한 역할을標準화하면 숙련되지 않은 엔지니어도 공장 설명서(roles/)만 읽으면 올바른方法来설정할 수 있습니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

### 1. Terraform CDK와 Pulumi의崛起
HashiCorp의 Terraform CDK(Cloud Development Kit)뿐 아니라 Pulumi가 일반 프로그래밍 언어로 인프라를 정의할 수 있게 함으로써, 인프라 엔지니어와 애플리케이션 개발자 사이의 경계가 모호해지고 있습니다.

### 2. Ansible의 플랫폼化
Ansible은 단순한 구성 관리 도구를 넘어, Ansible Automation Platform으로 진화하여 네트워크 장비, 클라우드, 컨테이너, 그리고 비즈니스 응용 프로그램까지 자동화하는 통합 플랫폼으로 확장되고 있습니다.

### 3. IaC 도구의 합류
Terraform과 Ansible 모두 Kubernetes, GitOps, Policy as Code 등 현대적인 인프라 관리 방식과 긴밀히 통합되어, IaC 도구 자체가 DevOps 도구들의 hub로 기능하는 방향으로 발전하고 있습니다.

- **📢 섹션 요약 비유**: Terraform과 Ansible의 미래는 "스마트시티 통합 교통 시스템"과 같습니다. 현재에는 지하철( Terraform )과 버스( Ansible )가 별개로 운영되지만, 미래에는 두 시스템이 하나의 통합 카드( 통합 플랫폼 )로 연결되어, 여행자( 개발자 )가目的地를 말하면 시스템이 자동으로 최적의 경로( 인프라 + 설정 )를 계산하고, 도보( 설정 )와 전동 킥보드( 프로비저닝 )를 알아서 조합하여Navigation합니다. 어느 한交通工具(도구)에过分依赖하지 않고, 여행자의 필요에 맞게自由に組み合わせる万能な交通体系が姿を现し始めています.

---

## 🧠 지식 맵 (Knowledge Graph)

*   **Terraform 핵심 개념**
    *   Provider (AWS, GCP, Azure 등)
    *   Resource ( 인프라 객체)
    *   State (현재 인프라 상태)
    *   Plan (변경 사항 미리보기)
    *   Module (재사용 가능한IaC 코드)
*   **Ansible 핵심 개념**
    *   Playbook (태스크 목록 YAML)
    *   Role (태스크 분리/캡슐화)
    *   Handler (이벤트トリガー 태스크)
    *   Inventory (대상 서버 목록)
    *   Module (실제 작업 수행 단위)
*   **보완적 활용**
    *   Terraform: 인프라 생성
    *   Ansible: 상세 설정 + 앱 배포

---

### 👶 어린이를 위한 3줄 비유 설명
1. Terraform은 "레고 기본 키트"와 같아요. 블록( 인프라 )을 처음부터 조립해서 멋진 작품( 서버, 네트워크 )을 만들어요.
2. Ansible은 "레고 작품에 색칠과萧성을 입히는" 것과 같아요. 기본 모양은 Terraform이 만들고, 상세한设定은 Ansible이 해요.
3. 둘 다レゴ説明書の代わりに 코드( .tf, .yml )를 사용해서, 누구나 같은 작품을 만들 수 있어요!

---

> **🛡️ Claude 3.7 Sonnet Verified:** 본 문서는 Terraform과 Ansible의体系적 비교와 실무 통합 가이드를 기준으로 작성되었습니다. (Verified at: 2026-04-05)
