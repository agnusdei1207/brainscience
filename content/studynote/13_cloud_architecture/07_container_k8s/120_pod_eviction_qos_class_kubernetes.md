+++
weight = 120
title = "120. Pod Eviction과 QoS Class (K8s 리소스 관리) - Guaranteed·Burstable·BestEffort"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: K8s QoS Class는 Pod의 리소스 요청(requests)·제한(limits) 설정에 따라 **Guaranteed·Burstable·BestEffort** 3등급으로 자동 분류되며, 노드 리소스 부족 시 **QoS 등급이 낮은 Pod부터 Eviction(퇴거)**된다.
> **비유**: 복잡한 시스템을 작은 운영 규칙으로 정리해 안정적으로 굴러가게 만드는 교통 관제 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    QoS Class 결정 규칙                                │
├───────────────────────────────────────────────────────┤
│  [Guaranteed] requests == limits (CPU + Memory 모두)  │
│   → 최우선 보호, Eviction 가장 마지막               │
│                                                       │
│  [Burstable] requests < limits (일부만 설정도 포함)   │
│   → 중간 우선순위                                     │
│                                                       │
│  [BestEffort] requests·limits 없음                    │
│   → 최저 우선순위, Eviction 1순위                    │
│                                                       │
│  Eviction 순서: BestEffort → Burstable → Guaranteed  │
└───────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### Eviction 순서

| 순서 | QoS | 조건 | 보호 수준 |
|:---|:---|:---|:---|
| **1순위** | BestEffort | requests 없음 | 최저 |
| **2순위** | Burstable | requests 초과 사용 중 | 중간 |
| **3순위** | Guaranteed | requests == limits | **최고** |

### 설정 예시
```yaml
# Guaranteed: requests == limits
resources:
  requests:
    cpu: 500m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 256Mi
```

---

## 3. 구조 및 원리

**핵심 조건**: 쿠버네티스 기반 클라우드 네이티브 운영은 선언형 상태, 보안 통제, 자동 확장, 관측성, 정책 일관성이 함께 작동해야 효과가 난다.

동작 순서:
1. 워크로드나 정책을 선언형 객체로 정의한다.
2. 컨트롤 플레인이 스케줄링·보안·배치 정책을 해석한다.
3. 런타임과 플러그인이 실제 실행, 네트워킹, 스토리지를 구성한다.
4. 서비스 계층과 정책 엔진이 외부 노출, 통신 통제, 이미지 신뢰를 관리한다.
5. 모니터링과 오토스케일링이 상태를 보정하며 운영 품질을 유지한다.

| 비교 | BestEffort | Burstable | Guaranteed |
|:---|:---|:---|:---|
| **requests** | 없음 | 있음 | **== limits** |
| **Eviction** | 1순위 | 2순위 | **마지막** |
| **적합** | 배치·테스트 | 일반 워크로드 | **프로덕션 핵심** |

---

## 4. 비교 및 연결

### Best Practice
1. **프로덕션**: Guaranteed (requests == limits).
2. **개발/테스트**: Burstable (requests < limits).
3. **BestEffort**: 절대 프로덕션 금지.
4. LimitRange·ResourceQuota로 네임스페이스 전체 관리.

---

## 5. 실무 적용 및 판단

| 지표 | QoS 미설정 | QoS 설정 | 개선 |
|:---|:---|:---|:---|
| OOMKilled 대상 | 무작위 | **등급순** | 핵심 보호 |
| 리소스 예측 | 불가 | **requests 기반** | 스케줄링 최적화 |

QoS Class는 K8s 리소스 관리의 기본이며, VPA(Vertical Pod Autoscaler)가 requests/limits를 자동 조정하는 방향으로 진화하고 있다.

---

## 6. 기대효과 및 결론

Pod Eviction과 QoS Class (K8s 리소스 관리) - Guaranteed·Burstable·BestEffort를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 Pod Eviction과 QoS Class (K8s 리소스 관리) - Guaranteed·Burstable·BestEffort의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
[K8s 초기 (리소스 미설정, OOMKill 빈발)]
    │
    ▼
[QoS Class 도입 (2016~) — 3등급 Eviction 우선순위]
    │
    ▼
[LimitRange/ResourceQuota (네임스페이스 관리)]
    │
    ▼
[VPA (2019~) — requests/limits 자동 조정]
    │
    ▼
[현재: Karpenter — 노드 자체를 자동 스케일링]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Guaranteed** | requests == limits, 최고 보호 |
| **Eviction** | 리소스 부족 시 Pod 강제 종료 |
| **OOMKilled** | 메모리 초과 시 커널이 프로세스 종료 |
| **LimitRange** | 네임스페이스 기본 requests/limits 설정 |
| **VPA** | requests/limits 자동 조정 도구 |

---
