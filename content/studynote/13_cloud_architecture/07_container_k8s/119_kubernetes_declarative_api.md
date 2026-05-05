+++
weight = 119
title = "119. K8s 선언적 API (Declarative API) - Desired State·Reconciliation Loop"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: K8s 선언적 API는 **"무엇을 원하는가(Desired State)"를 YAML로 선언**하면, K8s 컨트롤러가 현재 상태를 Desired State에 **자동으로 수렴시키는(Reconciliation)** 운영 모델이다.
> **비유**: 복잡한 시스템을 작은 운영 규칙으로 정리해 안정적으로 굴러가게 만드는 교통 관제 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    명령형 vs 선언적                                   │
├───────────────────────────────────────────────────────┤
│  [명령형 (Imperative)]                                │
│   kubectl run nginx --image=nginx                     │
│   kubectl scale --replicas=3 deploy/nginx             │
│   → "어떻게(How)"를 지시, 상태 보장 없음             │
│                                                       │
│  [선언적 (Declarative)]                               │
│   apiVersion: apps/v1                                 │
│   kind: Deployment                                    │
│   spec:                                               │
│     replicas: 3                                       │
│   → "무엇(What)"을 선언, K8s가 자동 유지             │
│   Pod 1개 죽으면 → 자동으로 1개 재생성               │
└───────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### Reconciliation Loop

| 단계 | 설명 |
|:---|:---|
| **Observe** | 현재 상태 확인 (Pod 2개) |
| **Diff** | Desired(3개) vs Current(2개) = 1개 부족 |
| **Act** | Pod 1개 생성 → 3개 달성 |
| **반복** | 무한 루프로 상태 유지 |

### Operator Pattern
- **Custom Resource (CR)**: 사용자 정의 리소스 (e.g., `PostgreSQL`).
- **Custom Controller**: CR의 Desired State를 Reconcile하는 로직.
- 결과: `kubectl apply -f postgres.yaml`로 **DB 클러스터 자동 프로비저닝**.

---

## 3. 구조 및 원리

**핵심 조건**: 쿠버네티스 기반 클라우드 네이티브 운영은 선언형 상태, 보안 통제, 자동 확장, 관측성, 정책 일관성이 함께 작동해야 효과가 난다.

동작 순서:
1. 워크로드나 정책을 선언형 객체로 정의한다.
2. 컨트롤 플레인이 스케줄링·보안·배치 정책을 해석한다.
3. 런타임과 플러그인이 실제 실행, 네트워킹, 스토리지를 구성한다.
4. 서비스 계층과 정책 엔진이 외부 노출, 통신 통제, 이미지 신뢰를 관리한다.
5. 모니터링과 오토스케일링이 상태를 보정하며 운영 품질을 유지한다.

| 비교 | 명령형 | 선언적 |
|:---|:---|:---|
| **표현** | How (방법) | **What (목표)** |
| **상태 보장** | 없음 | **자동 복원** |
| **GitOps** | 불가 | **자연스러운 결합** |
| **롤백** | 수동 | **git revert → 자동** |

---

## 4. 비교 및 연결

### 선언적 관리 Best Practice
1. 모든 리소스를 YAML로 정의 → Git 관리.
2. `kubectl apply -f` (선언적) 사용, `kubectl create/run` (명령형) 지양.
3. Kustomize/Helm으로 환경별 분기.

---

## 5. 실무 적용 및 판단

선언적 API는 K8s의 **철학적 핵심**이며, 이 원칙 덕분에 GitOps·Operator·Self-healing이 자연스럽게 구현된다. 모든 클라우드 네이티브 도구가 이 패러다임을 따른다.

---

## 6. 기대효과 및 결론

K8s 선언적 API (Declarative API) - Desired State·Reconciliation Loop를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 K8s 선언적 API (Declarative API) - Desired State·Reconciliation Loop의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
[명령형 인프라 관리 (스크립트, 2000s)]
    │
    ▼
[K8s 선언적 API (2014~) — Desired State + Reconciliation]
    │
    ▼
[Custom Resource + Operator (2016~) — 선언적 확장]
    │
    ▼
[GitOps (2017~) — Git + 선언적 API 결합]
    │
    ▼
[현재: Crossplane — 클라우드 리소스까지 선언적 관리]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Desired State** | YAML로 선언한 목표 상태 |
| **Reconciliation Loop** | 현재→목표 자동 수렴 |
| **Operator Pattern** | CR + Controller로 선언적 확장 |
| **GitOps** | 선언적 API 위에 Git 기반 운영 |
| **Self-healing** | Reconciliation의 자동 복구 효과 |

---
