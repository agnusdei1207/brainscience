+++
weight = 177
title = "177. 시크릿 관리 (Secrets Management - Vault, Kubernetes Secret)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시크릿 관리(Secrets Management)는 DB 비밀번호, API 키, TLS 인증서 같은 민감 자격 증명을 소스 코드·환경 변수가 아닌 전용 키 저장소(HashiCorp Vault 등)에서 런타임에 동적으로 주입하는 방식이다.
> 2. **가치**: 자격 증명이 Git 히스토리에 한 번 포함되면 삭제 후에도 영구적으로 위험하므로, 코드에서 완전히 분리하고 중앙에서 접근 제어·감사·자동 갱신하는 것이 필수다.
> 3. **판단 포인트**: Kubernetes Secret은 Base64 인코딩에 불과해 보안 수준이 낮으므로, Vault Agent Injector나 External Secrets Operator를 통해 진정한 시크릿 관리를 구현해야 한다.

---

## Ⅰ. 개요 및 필요성

2022년 GitGuardian 보고서에 따르면 GitHub에서 공개 저장소의 코드 100만 건당 6,000개 이상의 시크릿이 발견된다. `AWS_SECRET_KEY=xxx`가 코드에 한 줄 들어가는 순간 봇이 수분 내로 스캔하여 악용한다.

하드코딩된 자격 증명 문제의 핵심은 불가역성이다. Git 히스토리에서 커밋을 지워도 이미 클론한 복사본이 전 세계에 존재한다. 근본 해결책은 코드에 자격 증명을 넣지 않는 것이다.

시크릿 관리의 올바른 방법은 세 단계로 요약된다: **저장(Store)** — 시크릿을 전용 저장소(Vault)에 저장, **주입(Inject)** — 앱 시작 시 런타임에 동적으로 전달, **감사(Audit)** — 누가 언제 어떤 시크릿에 접근했는지 로그 기록.

📢 **섹션 요약 비유**: 시크릿 관리는 회사 금고(Vault)와 같다. 직원이 필요할 때 금고에서 열쇠를 빌리고, 언제 누가 빌렸는지 금고 일지에 기록된다. 열쇠를 서랍에 아무렇게나 두는 것(하드코딩)과는 완전히 다르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### HashiCorp Vault 동작 구조

```
[Vault 기반 시크릿 주입 흐름]

개발자 → vault kv put secret/db password=xxx (1회 저장)
                       ↓
                 Vault Server
              (암호화 저장, 접근 정책)
                       ↓
           K8s Pod 시작 시 Vault Agent Injector
                       ↓
    Init Container: Vault 인증 → 시크릿 가져오기
                       ↓
    App Container: /vault/secrets/db 파일에서 읽기
                  (메모리 파일시스템, Pod 종료 시 삭제)

[코드에는 자격 증명 없음 — 파이프라인/Git에도 없음]
```

| 항목 | Kubernetes Secret | HashiCorp Vault |
|:---|:---|:---|
| 저장 방식 | Base64 인코딩 (암호화 아님) | AES-256 암호화 |
| 접근 제어 | K8s RBAC | 정밀한 정책 기반 |
| 감사 로그 | 제한적 | 상세 감사 추적 |
| 동적 시크릿 | 불지원 | DB 비밀번호 자동 생성/만료 |
| 자동 갱신 | 불지원 | TTL 기반 자동 갱신 |
| 운영 복잡도 | 낮음 | 높음 |

📢 **섹션 요약 비유**: K8s Secret은 종이에 비밀번호를 써서 숨겨두는 것(Base64)이고, Vault는 지문 인식이 필요한 철제 금고에 잠가두는 것이다.

---

## Ⅲ. 비교 및 연결

### 시크릿 주입 방법 비교

| 방법 | 동작 방식 | 보안 수준 | 운영 복잡도 |
|:---|:---|:---|:---|
| 환경 변수 하드코딩 | 코드에 직접 | 매우 낮음 | 없음 |
| K8s Secret (기본) | etcd에 Base64 저장 | 낮음~중간 | 낮음 |
| Vault Agent Injector | Pod 사이드카가 주입 | 높음 | 중간 |
| External Secrets Operator | K8s에 Vault를 K8s Secret으로 동기화 | 높음 | 낮음 |
| CSI Secret Store Driver | Volume 마운트로 주입 | 높음 | 중간 |
| 클라우드 네이티브 (AWS SSM, GCP Secret) | 클라우드 IAM 기반 | 높음 | 낮음 |

**Git 히스토리 시크릿 제거 도구:**
- `git-filter-repo`: Git 히스토리에서 특정 파일/문자열 완전 삭제
- BFG Repo-Cleaner: 빠른 히스토리 정리
- **주의**: 히스토리 삭제 후에도 자격 증명 즉시 무효화(rotate)가 필수

📢 **섹션 요약 비유**: Git 히스토리에서 시크릿을 지우는 것은 쓰레기통 비우기와 같다. 쓰레기통(히스토리)에서 삭제해도 이미 사진 찍은 사람(클론)이 있을 수 있어서, 즉시 자물쇠(비밀번호)를 바꿔야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**시크릿 탐지 자동화:**
- **Gitleaks**: Git 커밋에서 AWS 키, GitHub 토큰 등 패턴 탐지
- **git-secrets**: AWS 공식 도구, pre-commit 훅으로 커밋 차단
- **TruffleHog**: 엔트로피(무작위성) 분석으로 시크릿 패턴 감지

**Vault Dynamic Secrets (동적 시크릿):**
```
앱이 DB 연결 필요 → Vault에 요청
Vault → AWS RDS에 임시 사용자 생성 (TTL: 1시간)
Vault → 앱에 임시 사용자명/비밀번호 반환
1시간 후 → 임시 사용자 자동 삭제
```
동적 시크릿은 자격 증명 수명을 최소화하여 유출되어도 피해를 제한한다.

**AWS 환경 Best Practice:**
- EC2/ECS: IAM Instance Profile(인스턴스 메타데이터 서비스)로 자격 증명 없이 AWS API 접근
- Lambda: IAM Execution Role로 S3, DynamoDB 접근
- EKS: IRSA(IAM Roles for Service Accounts)로 Pod별 세밀한 권한 부여

📢 **섹션 요약 비유**: IAM Instance Profile은 사원증과 같다. 직원이 회사 복사기를 쓸 때 사원증을 대면 개인 비밀번호 없이도 쓸 수 있는 것처럼, EC2는 AWS API를 비밀번호 없이 사용한다.

---

## Ⅴ. 기대효과 및 결론

시크릿 관리 체계를 구축하면 자격 증명 유출로 인한 데이터 침해 위험이 근본적으로 감소한다. 동적 시크릿으로 자격 증명 수명이 최소화되고, 감사 로그로 모든 접근이 추적된다. SOC2, PCI-DSS, ISO 27001 같은 보안 규정 준수에도 필수적으로 요구되는 영역이다.

초기 구축 비용이 있지만, 자격 증명 유출로 인한 데이터 침해 사고 대응 비용(평균 수백억 원)에 비하면 투자 대비 효과가 압도적이다. 쿠버네티스 환경에서는 External Secrets Operator가 낮은 복잡도로 Vault 통합을 지원하여 진입 장벽이 낮아졌다.

📢 **섹션 요약 비유**: 시크릿 관리는 회사의 자동 잠금 금고 시스템이다. 매일 아침 코드가 새 열쇠를 받고 저녁에 반납한다. 어제 열쇠가 유출되어도 오늘은 이미 새 열쇠를 쓰고 있어서 안전하다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| HashiCorp Vault | 중앙 시크릿 저장소 및 동적 발급 |
| K8s Secret | 기본 제공이지만 보안 취약, 보완 필요 |
| DevSecOps | 시크릿 탐지(Gitleaks)가 파이프라인에 통합 |
| IAM Role | 클라우드 네이티브 인증 방식, 시크릿 불필요 |
| IRSA | EKS Pod별 IAM 권한, 세밀한 접근 제어 |
| SBOM / 감사 | 시크릿 접근 로그로 규정 준수 증명 |

### 👶 어린이를 위한 3줄 비유 설명
1. 비밀번호를 코드에 적어두는 건 일기장에 은행 PIN을 써두는 것만큼 위험해요.

### 📈 관련 키워드 및 발전 흐름도

```text
하드코딩된 시크릿 (코드 · 환경변수 평문)
    │
    ▼
시크릿 관리: Vault · AWS Secrets Manager · K8s Secrets
    ├─► 동적 시크릿: 사용 후 자동 회전
    └─► 암호화: Sealed Secrets · SOPS · KMS
    │
    ▼
Zero Trust: 최소 권한 + 감사 로그 + RBAC
```
2. Vault는 튼튼한 금고예요. 필요할 때만 잠깐 꺼내 쓰고, 언제 꺼냈는지 기록해요.
3. 동적 시크릿은 매일 새로운 열쇠를 주는 시스템이라서, 열쇠를 잃어버려도 금방 바꿀 수 있어요!
