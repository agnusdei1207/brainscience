+++
weight = 48
title = "48. 컴플라이언스 애즈 코드 (Compliance as Code)"
date = "2026-04-05"
[extra]
categories = "studynote-it-management"
+++

## 0. 핵심 인사이트

> **핵심**: 컴플라이언스 애즈 코드 (Compliance as Code)의 본질은 수동 감사가 아닌 인프라 코드에 규제 검사 룰셋 자동 융합를 비즈니스 가치, 통제, 실행 관점에서 일관되게 연결하는 데 있다.
> **비유**: 전략과 운영 사이의 간극을 메우는 조정 메커니즘과 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```
전통 컴플라이언스 vs Compliance as Code:

전통 방식:
  1. 정책 문서 작성 (Word/PDF)
  2. IT 팀에 이메일로 전달
  3. 구성 변경 후 수동 검토
  4. 분기/연간 감사

  문제:
  감사 준비 = 2~4주 수작업
  감사 주기 사이 위반 지속
  인적 오류 (체크리스트 누락)
  클라우드 변경 속도를 따라가지 못함

Compliance as Code:
  정책 → 코드화 → CI/CD 파이프라인 통합
  인프라 변경 → 자동 정책 검사 → 위반 즉시 차단/알림

  도구:
  OPA (Open Policy Agent): 범용 정책 엔진
  AWS Config Rules: AWS 자원 규정 준수
  Azure Policy: Azure 자원 정책
  Terraform Sentinel: IaC 정책 게이트
  Chef InSpec: 인프라 규정 준수 테스트

핵심 원칙:
  Policy as Code:
  정책 → Git 저장소 관리 (버전 관리, 변경 추적)
  검토/승인 → PR 프로세스

  Continuous Compliance:
  매 커밋/배포 시 정책 자동 검사
  "컴플라이언스 = 코드 빌드 테스트와 동일 레벨"
```

---

## 2. 구성요소

```
OPA (Open Policy Agent):
  CNCF 프로젝트 (Cloud Native Computing Foundation)
  범용 정책 엔진

  언어: Rego (OPA 전용 정책 언어)
  용도: Kubernetes, API, IaC 정책

Rego 정책 예시:

1. Kubernetes Pod 보안 정책:
  package kubernetes.admission

  deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.privileged == true
    msg := sprintf("특권 컨테이너 허용 안 됨: %v", [container.name])
  }

  → 특권 컨테이너 배포 시 자동 거부

2. Terraform IaC 정책 (S3 퍼블릭 차단):
  package terraform

  deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    resource.change.after.acl == "public-read"
    msg := "S3 버킷 공개 읽기 허용 금지"
  }

  → terraform plan 시 정책 검사 → 위반 차단

3. API 접근 정책:
  package authz

  allow {
    input.method == "GET"
    input.user.role == "admin"
  }
  allow {
    input.method == "GET"
    input.path == ["public", "api"]
  }

  → API 게이트웨이에서 OPA로 권한 검사

OPA 통합 포인트:
  Kubernetes: OPA Gatekeeper (Admission Controller)
  CI/CD: Conftest (Terraform/YAML 정책 검사)
  API 게이트웨이: Envoy + OPA
```

---

## 3. 구조 및 원리

```
AWS Config:
  AWS 자원 구성 변경 추적 + 정책 준수 검사

  동작:
  1. 자원 변경 발생 (EC2, S3, IAM...)
  2. AWS Config가 변경 기록 (Configuration Item)
  3. Config Rules 자동 평가
  4. 위반 → AWS Security Hub로 전달

AWS Config Rules 예시:

  s3-bucket-public-read-prohibited:
  S3 버킷 퍼블릭 읽기 → NON_COMPLIANT

  ec2-instance-no-public-ip:
  EC2에 퍼블릭 IP → NON_COMPLIANT

  iam-password-policy:
  IAM 비밀번호 정책 최소 길이 14자 미만 → NON_COMPLIANT

  root-account-mfa-enabled:
  루트 계정 MFA 비활성화 → NON_COMPLIANT

AWS Security Hub:
  여러 AWS 서비스 보안 결과 통합
  표준 준수 점수 자동 계산:

  CIS AWS Foundations Benchmark
  AWS Foundational Security Best Practices
  PCI DSS v3.2.1

  점수 예:
  CIS Level 1: 67% 준수
  → 무엇을 고쳐야 100%?
  → 우선순위별 수정 가이드

자동 교정 (Auto Remediation):
  Config Rule 위반 → Lambda 자동 실행 → 수정

  예:
  S3 퍼블릭 → Lambda가 ACL을 private으로 변경
  IAM 비밀번호 정책 위반 → 자동 정책 업데이트
```

---

## 4. 비교 및 연결

```
Terraform Sentinel:
  HashiCorp의 Policy as Code 프레임워크
  IaC 배포 전 정책 검사 (Shift-Left!)

정책 적용 단계:
  terraform plan → Sentinel 정책 검사 → terraform apply

  정책 위반 시: apply 차단 (Advisory / Soft-Mandatory / Mandatory)

Sentinel 정책 예시:

1. 태그 필수 정책:
  import "tfplan/v2" as tfplan

  required_tags = ["environment", "owner", "cost-center"]

  resources = tfplan.find_resources("aws_instance")

  check_tags = rule {
    all resources as _, rc {
      all required_tags as tag {
        rc.change.after.tags contains tag
      }
    }
  }

  main = rule { check_tags }

  → 태그 없는 EC2 배포 차단

2. 인스턴스 유형 제한:
  allowed_types = ["t3.micro", "t3.small", "t3.medium"]

  check_type = rule {
    all resources as _, rc {
      rc.change.after.instance_type in allowed_types
    }
  }

  → 프로덕션 제외 환경에서 큰 인스턴스 배포 차단

정책 단계:
  Advisory: 경고만 (배포는 진행)
  Soft-Mandatory: 강제 + 권한자 override 가능
  Mandatory: 절대 차단

Conftest (오픈소스 대안):
  Terraform, Kubernetes YAML, Helm에 OPA Rego 정책 적용
  Terraform Cloud 없이도 사용 가능
```

---

## 5. 실무 적용 및 판단

```
핀테크 스타트업 → 금융감독원 규제 준수 CaC:

배경:
  AWS 기반 서비스
  규제: 전자금융감독규정, 클라우드 이용 기준

  감사 준비: 분기마다 2주 수작업
  개발팀 위반 반복: S3 퍼블릭, IAM 과잉 권한

CaC 구축:

1. 정책 코드화 (OPA + AWS Config):
  전자금융감독규정 주요 항목 → Rego + Config Rules

  정책 목록 (50개):
  - S3 암호화 필수 (AES-256)
  - RDS 암호화 필수
  - 퍼블릭 S3 버킷 금지
  - EC2 공개 접근 금지 (특수 경우 제외)
  - 로그 보존 1년 이상
  - MFA 전 IAM 사용자 적용
  - ...

2. CI/CD 통합:
  Terraform 변경 → Sentinel 정책 자동 검사
  Kubernetes 배포 → OPA Gatekeeper 검사

  PR 단계에서 정책 위반 즉시 피드백:
  "🚫 S3 버킷에 암호화 누락 (규정 제28조)"
  "✅ 8개 정책 통과"

3. 실시간 대시보드:
  AWS Security Hub → Grafana 대시보드
  준수율 실시간 표시 (목표: 98%+)
  위반 항목 드릴다운 가능

결과 (3개월):
  감사 준비 시간: 2주 → 1일 (대시보드 리포트 출력)
  반복 위반: 월 25건 → 2건 (자동 차단)
  개발팀 체감: "배포할 때 미리 알려줘서 좋음"

  규제 감사 결과:
  "컴플라이언스 자동화 우수 사례" 인정
  지적 사항: 3건 → 0건
```

---

## 6. 기대효과 및 결론

컴플라이언스 애즈 코드 (Compliance as Code)를 올바르게 적용하면 의사결정의 일관성, 운영의 재현성, 통제의 추적성이 동시에 향상된다. 즉 “누가 무엇을 왜 했는가”가 남기 때문에 조직이 커질수록 효과가 커진다.

다만 컴플라이언스 애즈 코드 (Compliance as Code)는 문서만 잘 만들어도 성공하는 영역이 아니다. 정의와 실행이 분리되면 형식주의가 되고, 자동화만 앞서면 통제 목적이 사라진다. 따라서 표준화와 민첩성, 통제와 생산성 사이의 균형이 항상 필요하다.

향후에는 정책 코드화(Policy as Code), 실시간 관측성(Observability), AI 기반 이상 탐지와 의사결정 지원이 결합되면서 관리 체계가 더 자동화되고 증거 중심으로 진화할 가능성이 크다. 결론적으로 핵심은 도구가 아니라 기준선이며, 기준선이 명확할 때만 자동화와 확장이 의미를 가진다.

---

## 7. 발전 흐름도

```
[전통 수동 감사 (2000s)]
체크리스트 기반
연간/분기 점검
      |
      v
[IaC 등장 (Terraform, 2014)]
인프라 코드화
정책 코드화 가능성
      |
      v
[OPA 오픈소스 (2016)]
범용 정책 엔진
Kubernetes Gatekeeper
      |
      v
[DevSecOps (2018~)]
보안+컴플라이언스를 CI/CD로
Shift-Left 보안
      |
      v
[현재: AI 컴플라이언스]
LLM 기반 정책 생성
자동 규제 해석
```

---

## 8. 관련 개념 맵

```
Compliance as Code
+-- 핵심 도구
|   +-- OPA (Rego 정책)
|   +-- AWS Config Rules
|   +-- Terraform Sentinel
|   +-- Conftest
+-- 통합 포인트
|   +-- CI/CD 파이프라인
|   +-- Kubernetes Admission
|   +-- IaC (Terraform)
+-- 표준 프레임워크
|   +-- CIS Benchmark
|   +-- PCI DSS
|   +-- 전자금융감독규정
+-- 원칙
    +-- Policy as Code
    +-- Shift-Left Compliance
    +-- Continuous Compliance
```
