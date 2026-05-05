+++
weight = 114
title = "114. Argo CD (ArgoCD GitOps CD) - K8s 선언적 지속 배포·Git 단일 진실 원천"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: Argo CD는 **Git 레포지토리를 단일 진실 원천(Single Source of Truth)**으로 삼아, Git의 매니페스트와 K8s 클러스터 상태를 **실시간 비교(Diff)하고 자동 동기화(Sync)**하는 CNCF 졸업 GitOps CD 도구다.
> **비유**: 복잡한 시스템을 작은 운영 규칙으로 정리해 안정적으로 굴러가게 만드는 교통 관제 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Push 기반 CD vs Pull 기반 GitOps (Argo CD)         │
├───────────────────────────────────────────────────────┤
│  [Push: Jenkins]                                      │
│   개발자 → Git Push → Jenkins → kubectl apply → K8s  │
│   Jenkins에 클러스터 kubeconfig 필요 (보안 위험)      │
│                                                       │
│  [Pull: Argo CD]                                      │
│   개발자 → Git Push → (끝)                            │
│   Argo CD (클러스터 내부) → Git 감시 → 자동 Sync     │
│   Jenkins에 클러스터 권한 불필요 (보안 강화)          │
└───────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### Argo CD 핵심 개념

| 개념 | 설명 |
|:---|:---|
| **Application** | Git 레포 경로 + 타겟 클러스터/네임스페이스 매핑 |
| **Sync** | Git 상태 → K8s 클러스터 적용 |
| **Diff** | Git vs 클러스터 상태 차이 감지 |
| **Health** | Pod/Deployment 건강 상태 모니터링 |
| **Prune** | Git에서 삭제된 리소스를 클러스터에서도 삭제 |

### 지원 매니페스트 형식
- **Plain YAML**, **Helm Chart**, **Kustomize**, **Jsonnet**

---

## 3. 구조 및 원리

**핵심 조건**: 쿠버네티스 기반 클라우드 네이티브 운영은 선언형 상태, 보안 통제, 자동 확장, 관측성, 정책 일관성이 함께 작동해야 효과가 난다.

동작 순서:
1. 워크로드나 정책을 선언형 객체로 정의한다.
2. 컨트롤 플레인이 스케줄링·보안·배치 정책을 해석한다.
3. 런타임과 플러그인이 실제 실행, 네트워킹, 스토리지를 구성한다.
4. 서비스 계층과 정책 엔진이 외부 노출, 통신 통제, 이미지 신뢰를 관리한다.
5. 모니터링과 오토스케일링이 상태를 보정하며 운영 품질을 유지한다.

| 비교 | Jenkins CD | Argo CD | Flux |
|:---|:---|:---|:---|
| **방식** | Push | **Pull (GitOps)** | Pull (GitOps) |
| **보안** | CI에 클러스터 권한 | **클러스터 내부** | 클러스터 내부 |
| **UI** | Jenkins 대시보드 | **리소스 트리 시각화** | CLI 중심 |
| **CNCF** | - | **Graduated** | Graduated |

---

## 4. 비교 및 연결

### 도입 체크리스트
1. **Git 레포 분리**: 앱 코드 레포 + 매니페스트 레포 분리 (Config Repo 패턴).
2. **RBAC**: Argo CD 프로젝트별 접근 제어.
3. **Argo Rollouts**: 카나리·블루/그린 배포 선언적 관리.

### 안티패턴
- **kubectl apply 수동 실행 병행**: Git과 클러스터 상태 불일치 → GitOps 원칙 파괴.

---

## 5. 실무 적용 및 판단

| 지표 | Jenkins CD | Argo CD | 개선 |
|:---|:---|:---|:---|
| 클러스터 권한 노출 | CI에 kubeconfig | **클러스터 내부만** | 보안 강화 |
| 상태 드리프트 감지 | 불가 | **실시간 Diff** | 즉시 감지 |
| 롤백 | 파이프라인 재실행 | **Git Revert → 자동 Sync** | 30초 |

Argo CD는 멀티클러스터 GitOps·Argo Workflows(CI) 통합으로 **CI/CD 전체를 GitOps 패러다임**으로 통합하는 방향으로 진화하고 있다.

---

## 6. 기대효과 및 결론

Argo CD (ArgoCD GitOps CD) - K8s 선언적 지속 배포·Git 단일 진실 원천를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 Argo CD (ArgoCD GitOps CD) - K8s 선언적 지속 배포·Git 단일 진실 원천의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
[Jenkins CD (2010s) — Push 기반 파이프라인 배포]
    │
    ▼
[GitOps 개념 (2017, Weaveworks) — Git = 단일 진실 원천]
    │
    ▼
[Argo CD v1 (2018) — K8s Pull 기반 CD]
    │
    ▼
[CNCF Graduated (2022) — 생태계 표준화]
    │
    ▼
[현재: Argo CD + Argo Workflows — CI/CD 전체 GitOps 통합]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **GitOps** | Argo CD가 구현하는 배포 패러다임 |
| **Argo Rollouts** | 카나리·블루/그린 배포 확장 |
| **Flux** | 경쟁 GitOps CD 도구 (CNCF) |
| **Helm / Kustomize** | Argo CD가 지원하는 매니페스트 형식 |
| **Config Repo 패턴** | 앱 코드와 매니페스트 레포 분리 |

---
