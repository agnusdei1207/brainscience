+++
weight = 117
title = "117. K8s Network Policy 마이크로 세그멘테이션 - Pod 간 트래픽 격리·제로 트러스트"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: K8s Network Policy는 **Pod 간 네트워크 트래픽을 라벨 기반으로 허용/거부**하는 선언적 방화벽 규칙이며, 마이크로 세그멘테이션(Micro-segmentation)을 통해 클러스터 내부 **East-West 트래픽을 제어**한다.
> **비유**: 복잡한 시스템을 작은 운영 규칙으로 정리해 안정적으로 굴러가게 만드는 교통 관제 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Network Policy 예시                                │
├───────────────────────────────────────────────────────┤
│  [기본: Flat Network — 모든 Pod 간 통신 허용]         │
│   frontend ←→ backend ←→ db ←→ 모든 Pod             │
│   → 1개 Pod 침투 시 전체 위험                        │
│                                                       │
│  [Network Policy 적용: 마이크로 세그멘테이션]         │
│   frontend → backend:8080 ✅                         │
│   backend → db:5432 ✅                               │
│   frontend → db:5432 ❌ (차단)                       │
│   외부 → frontend:443 ✅ (Ingress)                   │
│   → 최소 권한, 횡이동(Lateral Movement) 차단         │
└───────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### Network Policy 구성 요소

| 요소 | 설명 |
|:---|:---|
| **podSelector** | 정책이 적용될 대상 Pod (라벨) |
| **policyTypes** | Ingress(수신) / Egress(발신) |
| **ingress.from** | 트래픽을 허용할 소스 (Pod/Namespace/CIDR) |
| **egress.to** | 트래픽을 허용할 목적지 |
| **ports** | 허용할 포트/프로토콜 |

### CNI 플러그인별 지원

| CNI | L3/L4 Policy | L7 Policy | eBPF |
|:---|:---|:---|:---|
| **Flannel** | ✗ | ✗ | ✗ |
| **Calico** | ✅ | 일부 | 옵션 |
| **Cilium** | ✅ | **✅ (HTTP/gRPC)** | **✅** |

---

## 3. 구조 및 원리

**핵심 조건**: 쿠버네티스 기반 클라우드 네이티브 운영은 선언형 상태, 보안 통제, 자동 확장, 관측성, 정책 일관성이 함께 작동해야 효과가 난다.

동작 순서:
1. 워크로드나 정책을 선언형 객체로 정의한다.
2. 컨트롤 플레인이 스케줄링·보안·배치 정책을 해석한다.
3. 런타임과 플러그인이 실제 실행, 네트워킹, 스토리지를 구성한다.
4. 서비스 계층과 정책 엔진이 외부 노출, 통신 통제, 이미지 신뢰를 관리한다.
5. 모니터링과 오토스케일링이 상태를 보정하며 운영 품질을 유지한다.

| 비교 | 기본 (정책 없음) | L3/L4 Policy | L7 Policy |
|:---|:---|:---|:---|
| **제어 수준** | 없음 | IP·포트 | **HTTP 경로·메서드** |
| **횡이동** | 가능 | **차단** | **정밀 차단** |

---

## 4. 비교 및 연결

### 기본 정책: Default Deny
```yaml
# 모든 Ingress 차단 → 필요한 것만 허용 (화이트리스트)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

---

## 5. 실무 적용 및 판단

| 지표 | 정책 없음 | Network Policy | 개선 |
|:---|:---|:---|:---|
| 횡이동 위험 | 100% | **차단** | 제로 트러스트 |
| 공격 표면 | 전체 Pod | **최소 권한** | 90% 축소 |

Network Policy는 **K8s 제로 트러스트의 기초**이며, Cilium eBPF 기반 L7 정책으로 Service Mesh 수준의 보안을 달성하는 방향으로 진화하고 있다.

---

## 6. 기대효과 및 결론

K8s Network Policy 마이크로 세그멘테이션 - Pod 간 트래픽 격리·제로 트러스트를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 K8s Network Policy 마이크로 세그멘테이션 - Pod 간 트래픽 격리·제로 트러스트의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
[Flat Network (K8s 기본 — 모든 Pod 간 통신 허용)]
    │
    ▼
[K8s Network Policy (2017) — L3/L4 Pod 간 격리]
    │
    ▼
[Calico (2018~) — BGP 기반 L3/L4 정책]
    │
    ▼
[Cilium (2020~) — eBPF 기반 L7 정책]
    │
    ▼
[현재: Cilium Service Mesh — Network Policy + L7 관측성 통합]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **마이크로 세그멘테이션** | Network Policy가 구현하는 보안 원칙 |
| **Calico** | L3/L4 Network Policy CNI |
| **Cilium** | L7 (HTTP/gRPC) Policy, eBPF 기반 |
| **제로 트러스트** | Network Policy가 기여하는 보안 아키텍처 |
| **Service Mesh** | L7 트래픽 제어의 상위 개념 |

---
