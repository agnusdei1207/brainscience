+++
weight = 115
title = "115. Atlantis Terraform CI"
date = "2026-04-19"
[extra]
categories = "studynote-devops-sre"
+++

## 0. 핵심 인사이트

> **핵심**: Atlantis는 Terraform/OpenTofu의 **PR(Pull Request) 기반 자동 Plan/Apply 워크플로**를 제공하는 OSS 도구로, PR을 열면 자동으로 `terraform plan` 결과를 코멘트로 달고, 승인 후 `atlantis apply`로 적용한다.
> **비유**: Atlantis는 인프라 변경의 **4-eyes 원칙(이중 확인)**을 자동화한 것이다. 혼자 몰래 서버를 바꿀 수 없고, 반드시 PR 리뷰를 거쳐야 한다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Atlantis PR 기반 워크플로                           │
├───────────────────────────────────────────────────────┤
│  1. 개발자: main.tf 수정 → PR 생성                   │
│  2. Atlantis Bot: 자동 terraform plan 실행            │
│     → PR 코멘트에 Plan 결과 표시                      │
│     "1 to add, 0 to change, 0 to destroy"            │
│  3. 리뷰어: Plan 결과 확인 → Approve                 │
│  4. 개발자: "atlantis apply" 코멘트                   │
│  5. Atlantis Bot: terraform apply 실행                │
│     → 성공 결과 코멘트 + PR 머지                      │
└───────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### Atlantis 핵심 기능

| 기능 | 설명 |
|:---|:---|
| **Auto Plan** | PR 생성 시 자동 plan 실행 |
| **PR Comment** | Plan 결과를 PR 코멘트로 표시 |
| **Locking** | 동일 디렉터리 동시 변경 방지 |
| **Apply Require** | PR Approve 후에만 apply 허용 |
| **Custom Workflow** | pre-plan/post-apply 훅 지원 |

### Atlantis vs Terraform Cloud

| 비교 | Atlantis | Terraform Cloud |
|:---|:---|:---|
| **호스팅** | 자체 (Docker) | **SaaS** |
| **비용** | 무료 | 유료 |
| **제어** | **완전** | HashiCorp 의존 |
| **State** | 별도 관리 (S3) | 내장 |
| **Sentinel** | ✗ | ✅ (정책) |

---

## 3. 구조 및 원리

**핵심 조건**: 모든 변경이 버전 관리되고, 자동 검증을 통과하며, 배포 상태와 롤백 경로가 추적 가능해야 한다.

동작 순서:
1. 코드와 배포 정의를 저장소에 커밋해 변경 이력을 단일 진실 공급원으로 만든다.
2. 빌드·테스트·보안 검사를 자동 수행해 배포 가능 아티팩트를 만든다.
3. 환경별 설정을 분리하면서도 동일한 파이프라인으로 일관성을 유지한다.
4. 배포 후 메트릭과 로그를 확인하고 이상 시 즉시 롤백하거나 다음 단계 승인을 중단한다.

```text
소스 변경
   ↓
CI 검증
   ↓
아티팩트 저장
   ↓
CD/GitOps 동기화
   ↓
운영 반영·롤백
```

| 비교 | 로컬 apply | Atlantis | Terraform Cloud |
|:---|:---|:---|:---|
| **리뷰** | 없음 | **PR 필수** | PR 필수 |
| **감사** | 불가 | **Git 이력** | 내장 |
| **State 충돌** | 빈번 | **Lock으로 방지** | 내장 |

---

## 4. 비교 및 연결

### 배포 체크리스트
1. Atlantis 서버를 K8s/Docker에 배포.
2. GitHub/GitLab Webhook 연결.
3. `atlantis.yaml`에 프로젝트 디렉터리·워크플로 정의.
4. PR Approve → `atlantis apply` 코멘트로 적용.

---

## 5. 실무 적용 및 판단

| 지표 | 로컬 apply | Atlantis | 개선 |
|:---|:---|:---|:---|
| 인프라 변경 감사 | 불가 | **PR 이력** | 100% |
| State 충돌 | 빈번 | **Lock** | 0건 |
| 비용 | - | **무료** | SaaS 대비 절감 |

Atlantis는 GitOps + Terraform의 가장 실용적인 조합이며, PR 리뷰 문화가 정착된 팀에서 인프라 거버넌스를 비용 없이 확보할 수 있는 최적의 도구다.

---

## 6. 기대효과 및 결론

Atlantis Terraform CI을(를) 도입하면 자동화와 표준화를 통해 속도·안정성·가시성의 균형을 높일 수 있다. 다만 효과를 얻으려면 모든 변경이 버전 관리되고, 자동 검증을 통과하며, 배포 상태와 롤백 경로가 추적 가능해야 한다는 전제가 충족되어야 하며, 도구만 도입하고 운영 원칙을 바꾸지 않으면 기대 효과가 빠르게 한계에 부딪힌다.

결론적으로 Atlantis Terraform CI은(는) 개별 기능이 아니라 운영 체계 전체의 품질을 재정렬하는 방식이며, 향후에는 플랫폼화·정책화·AI 기반 최적화와 결합해 더 높은 수준의 자동 운영으로 확장된다.

---

## 7. 발전 흐름도

```text
[로컬 terraform apply (2014~) — 개인 실행, 감사 불가]
    │
    ▼
[Atlantis (2017, Hootsuite) — PR 기반 자동 Plan/Apply]
    │
    ▼
[Terraform Cloud (2019~) — HashiCorp SaaS]
    │
    ▼
[Spacelift / env0 (2020~) — IaC CI SaaS 경쟁]
    │
    ▼
[현재: Atlantis + OPA/Conftest — 정책 검증 통합]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Terraform** | Atlantis가 자동화하는 IaC 도구 |
| **GitOps** | PR 기반 인프라 관리 = IaC GitOps |
| **Terraform Cloud** | SaaS 경쟁 도구 |
| **Spacelift** | 또 다른 Terraform CI SaaS 대안 |
| **PR Review** | Atlantis가 강제하는 변경 리뷰 프로세스 |
