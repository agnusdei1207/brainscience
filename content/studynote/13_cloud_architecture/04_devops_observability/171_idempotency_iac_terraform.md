+++
weight = 171
title = "171. 멱등성 (Idempotency in IaC)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: 멱등성(Idempotency)은 동일한 IaC 코드를 1번 실행하든 100번 실행하든 최종 인프라 상태가 항상 동일하다는 성질이다.
> **비유**: 멱등성은 전등 스위치와 같다. 이미 켜진 전등의 스위치를 10번 더 켜도 전등은 여전히 하나만 켜져 있다. 결과는 항상 동일하다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

수학에서 멱등성은 `f(f(x)) = f(x)`, 즉 함수를 여러 번 적용해도 결과가 달라지지 않는 성질이다. IaC에서 멱등성은 "코드를 여러 번 실행해도 인프라 상태가 항상 동일하다"로 해석된다.

멱등성이 없는 스크립트의 위험성을 생각해보자. 예를 들어 `echo "export PATH=..." >> ~/.bashrc`를 10번 실행하면 동일한 줄이 10번 추가된다. 반면 Terraform은 같은 S3 버킷 생성 코드를 10번 실행해도 버킷이 이미 존재하면 건드리지 않는다.

CI/CD 자동화 환경에서 네트워크 오류, 타임아웃 등으로 파이프라인이 중간에 실패할 수 있다. 멱등성이 보장된 IaC라면 단순 재시도로 안전하게 완료 상태에 도달할 수 있다.

---

## 2. 구성요소

### Terraform의 멱등성 구현 원리

```
Desired State        Current State          Action
(코드 정의)          (tfstate 파일)         (Terraform이 결정)

VPC 존재 원함   vs   VPC 없음          →  CREATE
EC2 t3.micro    vs   EC2 t3.micro      →  NO ACTION (이미 원하는 상태)
RDS db.t3       vs   RDS db.t2         →  UPDATE
S3 버킷 원함    vs   S3 버킷 없음      →  CREATE
```

```
terraform apply 실행 흐름

.tf 코드 읽기
    ↓
terraform.tfstate 읽기 (현재 상태)
    ↓
차이 계산 (diff)
    ↓
차이가 있는 리소스만 변경 → 멱등성 보장
```

| 개념 | 설명 |
|:---|:---|
| Desired State | 코드에서 정의한 "원하는" 인프라 상태 |
| Current State | tfstate 파일에 기록된 "현재" 실제 상태 |
| Drift | Desired와 Current가 벌어진 상태 |
| Reconciliation | 차이를 계산하여 Desired에 맞게 조정 |

---

## 3. 구조 및 원리

**핵심 조건**: 변경 자동화와 운영 안정성은 별개가 아니라 하나의 루프이며, 빌드·검증·배포·관측·피드백이 끊기지 않아야 지속 개선이 가능하다.

동작 순서:
1. 변경 사항을 버전 관리 시스템에서 감지한다.
2. 빌드·테스트·보안 검증으로 변경의 품질을 빠르게 확인한다.
3. 승인된 산출물을 선언형 배포나 자동화 파이프라인으로 운영 환경에 반영한다.
4. 메트릭·로그·트레이스를 통해 실제 동작 결과를 관측한다.
5. 피드백을 다음 개선 주기에 연결해 반복적으로 신뢰성을 높인다.

### 멱등성 구현 방식 비교

| 도구 | 멱등성 구현 방법 | 주의 사항 |
|:---|:---|:---|
| Terraform | State 파일 비교 후 변경분만 적용 | State 파일 손상 시 멱등성 깨짐 |
| Ansible | 각 Task `changed`/`ok` 상태 체크 | 일부 모듈은 멱등성 미보장 |
| Shell Script | 기본적으로 멱등성 없음 | 조건문으로 직접 구현해야 함 |
| Kubernetes | Desired State 선언, Controller가 조정 | 쿠버네티스 자체가 멱등성 기반 |

**비멱등 스크립트 vs 멱등 IaC 비교:**

```bash
# 비멱등 (Shell)
aws ec2 create-security-group --group-name "web-sg"
# 이미 존재하면 오류 발생

# 멱등 (Terraform)
resource "aws_security_group" "web" {
  name = "web-sg"
}
# 이미 존재하면 그냥 통과
```

---

## 4. 비교 및 연결

**State 파일 관리 Best Practice:**
- Remote Backend(S3)에 tfstate 저장: 팀 공유 및 유실 방지
- DynamoDB 잠금: 동시 apply 충돌 방지
- tfstate 직접 편집 금지: `terraform state` 명령어만 사용
- tfstate 버전 관리: S3 버전 관리 활성화

**Ansible 멱등성 체크:**
- `apt` 모듈: 패키지 이미 설치면 `ok` (변경 없음)
- `copy` 모듈: 파일 내용 동일하면 `ok`
- `shell`/`command` 모듈: 멱등성 미보장, `creates` 파라미터로 보완

**실무 시나리오**: 파이프라인이 네트워크 오류로 `terraform apply` 도중 실패했다. 멱등성 덕분에 단순 재시도(re-run)로 안전하게 완료 상태에 도달한다. State 파일이 중간 상태를 기록하고 있어 이미 생성된 리소스는 건너뛴다.

---

## 5. 실무 적용 및 판단

멱등성은 IaC 자동화의 신뢰성을 뒷받침하는 핵심 속성이다. 이 속성이 없으면 "자동화"는 "실수 자동화"가 될 수 있다. 멱등성 덕분에 CI/CD 파이프라인에서 IaC를 두려움 없이 반복 실행할 수 있고, 부분 실패도 안전하게 복구된다.

더 나아가 멱등성은 쿠버네티스의 Desired State Reconciliation 루프와 동일한 철학이다. 쿠버네티스 컨트롤러는 끊임없이 현재 상태를 Desired State와 비교하고 차이를 좁힌다. 이 패턴은 자기 치유(Self-healing) 시스템의 기반이다.

---

## 6. 기대효과 및 결론

멱등성 (Idempotency in IaC)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 멱등성 (Idempotency in IaC)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
비멱등 명령: 실행할 때마다 결과가 달라짐
    │
    ▼
멱등성 보장: 동일 명령 N번 실행 = 동일 결과
    ├─► Terraform: Desired State ↔ Current State 비교
    └─► Ansible: changed/ok 상태 보고
    │
    ▼
선언적 IaC + GitOps = 드리프트 자동 감지 · 복구
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Terraform State | 멱등성 구현의 핵심 메커니즘 |
| Desired State | 코드가 정의하는 목표 인프라 상태 |
| Configuration Drift | State 불일치로 발생, 멱등 apply로 복구 |
| Kubernetes Reconciliation | 동일한 멱등성 철학의 구현 |
| CI/CD 안전성 | 멱등성이 자동 재시도를 안전하게 만듦 |
| Ansible | 모듈별 멱등성 지원 수준 확인 필요 |

---
