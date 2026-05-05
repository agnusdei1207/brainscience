+++
weight = 115
title = "115. Terraform 인프라 프로비저닝 - IaC 선언적 다중 클라우드 관리"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: Terraform은 HashiCorp가 개발한 **선언적 IaC(Infrastructure as Code)** 도구로, HCL(HashiCorp Configuration Language)로 인프라를 정의하면 `terraform apply`로 AWS·Azure·GCP 등 **다중 클라우드에 자동 프로비저닝**한다.
> **비유**: 복잡한 시스템을 작은 운영 규칙으로 정리해 안정적으로 굴러가게 만드는 교통 관제 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Terraform 워크플로                                  │
├───────────────────────────────────────────────────────┤
│  1. Write: main.tf에 인프라 선언                      │
│     resource "aws_instance" "web" {                   │
│       ami           = "ami-xxx"                       │
│       instance_type = "t3.micro"                      │
│     }                                                 │
│  2. Plan: terraform plan → 변경 사항 미리 확인        │
│     + aws_instance.web will be created                │
│  3. Apply: terraform apply → 실제 생성                │
│  4. State: terraform.tfstate에 현재 상태 기록         │
└───────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### 핵심 개념

| 개념 | 설명 |
|:---|:---|
| **Provider** | AWS/Azure/GCP 등 클라우드 API 연결 플러그인 |
| **Resource** | 생성할 인프라 단위 (EC2, VPC, RDS 등) |
| **Module** | 재사용 가능한 리소스 묶음 |
| **State** | 현재 인프라 상태 기록 파일 |
| **Plan/Apply** | 변경 미리보기 → 실제 적용 2단계 |

### State 관리 Best Practice

| 방식 | 적합 | 위험 |
|:---|:---|:---|
| 로컬 파일 | 개인 프로젝트 | 팀 충돌, 유실 |
| **S3 + DynamoDB Lock** | **프로덕션** | 없음 (표준) |
| Terraform Cloud | SaaS 선호 팀 | 비용 |

---

## 3. 구조 및 원리

**핵심 조건**: 쿠버네티스 기반 클라우드 네이티브 운영은 선언형 상태, 보안 통제, 자동 확장, 관측성, 정책 일관성이 함께 작동해야 효과가 난다.

동작 순서:
1. 워크로드나 정책을 선언형 객체로 정의한다.
2. 컨트롤 플레인이 스케줄링·보안·배치 정책을 해석한다.
3. 런타임과 플러그인이 실제 실행, 네트워킹, 스토리지를 구성한다.
4. 서비스 계층과 정책 엔진이 외부 노출, 통신 통제, 이미지 신뢰를 관리한다.
5. 모니터링과 오토스케일링이 상태를 보정하며 운영 품질을 유지한다.

| 비교 | Terraform | CloudFormation | Pulumi |
|:---|:---|:---|:---|
| **클라우드** | **멀티** | AWS 전용 | 멀티 |
| **언어** | HCL | YAML/JSON | TypeScript/Python |
| **State** | 파일 기반 | AWS 관리 | 파일/SaaS |
| **라이선스** | BSL (1.6+) | 무료 | Apache 2.0 |

---

## 4. 비교 및 연결

### 모듈 구조 예시
```
infra/
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── rds/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
```

### 안티패턴
- **State 로컬 보관 + 팀 작업**: 동시 수정 시 State 충돌 → S3 원격 백엔드 필수.

---

## 5. 실무 적용 및 판단

| 지표 | 콘솔 수동 | Terraform | 개선 |
|:---|:---|:---|:---|
| 인프라 재현성 | 불가 | **100%** | 코드로 보장 |
| 변경 추적 | 불가 | **Git 이력** | 감사 가능 |
| 프로비저닝 | 시간 단위 | **분 단위** | 자동화 |

Terraform은 OpenTofu(OSS Fork)와의 생태계 분화가 진행 중이며, Terraform CDK(TypeScript/Python으로 HCL 생성)로 프로그래밍 언어 생태계와 통합되고 있다.

---

## 6. 기대효과 및 결론

Terraform 인프라 프로비저닝 - IaC 선언적 다중 클라우드 관리를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 Terraform 인프라 프로비저닝 - IaC 선언적 다중 클라우드 관리의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
[수동 콘솔 인프라 관리 (2010s)]
    │
    ▼
[Terraform 0.x (2014, HashiCorp) — 멀티클라우드 IaC]
    │
    ▼
[Terraform Module Registry (2017~) — 재사용 모듈 생태계]
    │
    ▼
[BSL 라이선스 전환 (2023) → OpenTofu Fork]
    │
    ▼
[현재: Terraform CDK + AI 인프라 자동 생성]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **IaC** | Terraform이 구현하는 인프라 코드화 패러다임 |
| **HCL** | Terraform의 선언적 설정 언어 |
| **State** | 현재 인프라 상태 추적 파일 |
| **Provider** | 클라우드 API 플러그인 생태계 |
| **OpenTofu** | Terraform의 OSS Fork (라이선스 분화) |

---
