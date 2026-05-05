+++
weight = 110
title = "110. OOM Killed (Out of Memory) - K8s 파드 메모리 초과 강제 종료와 QoS 생존 전략"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: OOM Killed는 파드가 `resources.limits.memory`로 선언한 메모리 상한을 초과하는 순간, 리눅스 커널의 **OOM Killer가 SIGKILL(9번 시그널)로 프로세스를 즉시 사살**하는 cgroups 기반 자원 통제 메커니즘이다.
> **비유**: 복잡한 시스템을 작은 운영 규칙으로 정리해 안정적으로 굴러가게 만드는 교통 관제 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

CPU를 초과하면 K8s는 파드를 죽이지 않고 **속도를 늦춘다(Throttling)**. 하지만 메모리(RAM)는 "빌린 뒤 반환 불가능한" 자원이므로, 한도를 넘는 순간 리눅스 커널이 프로세스를 **즉시 사살(OOM Killed)**하여 다른 파드를 보호한다.

```text
┌───────────────────────────────────────────────────────┐
│      CPU 초과 vs 메모리 초과: 비대칭 대응               │
├───────────────────────────────────────────────────────┤
│  [CPU 초과]                                           │
│   limits.cpu: 500m 초과 → Throttling (감속)           │
│   파드는 살아있음, 응답만 느려짐                       │
│                                                       │
│  [Memory 초과]                                        │
│   limits.memory: 512Mi 초과 → OOM Killed (즉사)       │
│   SIGKILL → CrashLoopBackOff 무한 루프                │
│                                                       │
│  왜 즉사? → 메모리는 "빌린 뒤 반환 불가"              │
│  방치 시 → 노드 전체 RAM 소진 → 동반 질식사           │
└───────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### QoS 클래스별 사살 우선순위

| QoS 클래스 | 조건 | 사살 순위 | 비유 |
|:---|:---|:---|:---|
| **BestEffort** | requests·limits 미지정 | **1순위 (최우선 사살)** | 무임승차 승객 |
| **Burstable** | requests < limits | **2순위** | 얌체 고무줄 승객 |
| **Guaranteed** | requests == limits | **최후 생존** | 1등석 정가 승객 |

### Java JVM OOM 90% 원인

Java 컨테이너가 OOM의 주범인 이유: JVM은 자신이 컨테이너 안에 갇힌 줄 모르고 **노드 전체 RAM(32GB)**을 자기 것으로 착각하여 Heap을 무한 확장한다. 컨테이너 limits(512MB)를 넘는 순간 OOM Killed.

**해결**: `-XX:MaxRAMPercentage=75.0` 옵션으로 JVM Heap을 컨테이너 limits의 75%로 제한한다.

---

## 3. 구조 및 원리

**핵심 조건**: 컨테이너/쿠버네티스 환경에서는 선언형 상태, 스케줄링 정책, 네트워크·스토리지 연동, 복구 자동화가 일관되게 맞물려야 운영 안정성이 확보된다.

동작 순서:
1. 사용자가 원하는 최종 상태를 선언형으로 정의한다.
2. 컨트롤 플레인이 스케줄링과 리소스 배치를 결정한다.
3. 런타임이 컨테이너를 기동하고 네트워크·스토리지를 연계한다.
4. 서비스 계층이 외부 트래픽과 내부 통신을 안정적으로 중계한다.
5. 프로브·오토스케일링·정책 엔진이 복구와 최적화를 반복한다.

| 비교 | CPU Throttling | OOM Killed |
|:---|:---|:---|
| **대상 자원** | CPU (시간 분할 가능) | Memory (분할 불가) |
| **초과 시 대응** | 감속 (느려짐) | **즉사 (SIGKILL)** |
| **파드 상태** | Running (느림) | **CrashLoopBackOff** |
| **사용자 영향** | 응답 지연 | **서비스 중단** |
| **복구 방법** | 자동 (부하 감소 시) | **재시작 + 원인 수정** |

---

## 4. 비교 및 연결

### 대처 체크리스트
1. **즉시**: `kubectl describe pod` → `Reason: OOMKilled` 확인.
2. **임시**: `limits.memory` 상향 (진통제, 근본 해결 아님).
3. **근본**: Java → `-XX:MaxRAMPercentage=75.0`, Node.js → `--max-old-space-size`.
4. **예방**: Prometheus + Grafana로 메모리 사용률 80% 알림 설정.

### 안티패턴
- **limits 미지정 (BestEffort)**: DB 파드에 limits를 안 걸어두면 노드 OOM 시 1순위 사살 대상.
- **limits 무조건 상향**: 메모리 누수 버그를 방치하고 limits만 올리면 시한폭탄.

---

## 5. 실무 적용 및 판단

| 전략 | 효과 |
|:---|:---|
| Guaranteed QoS (DB) | 노드 OOM에서도 **최후까지 생존** |
| JVM Heap 제한 | OOM 발생률 **90% 감소** |
| limits 적정 설정 | 리소스 낭비 없이 **안정 운영** |
| 모니터링 알림 | OOM 전 **사전 대응** 가능 |

OOM Killed는 클라우드 네이티브 환경에서 가장 빈번한 장애 원인이며, cgroups v2와 K8s Memory QoS(KEP-2570)가 결합하여 더 세밀한 메모리 관리가 가능해지고 있다.

---

## 6. 기대효과 및 결론

OOM Killed (Out of Memory) - K8s 파드 메모리 초과 강제 종료와 QoS 생존 전략를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 OOM Killed (Out of Memory) - K8s 파드 메모리 초과 강제 종료와 QoS 생존 전략의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
[cgroups v1 (2007) — 프로세스별 메모리 제한 도입]
    │
    ▼
[Docker (2013) — 컨테이너별 메모리 limits 적용]
    │
    ▼
[K8s QoS Class (2015~) — Guaranteed·Burstable·BestEffort 분류]
    │
    ▼
[cgroups v2 + Memory QoS (2022~) — 세밀한 메모리 보호]
    │
    ▼
[현재: VPA + KEP-2570 — 자동 limits 튜닝 + 메모리 QoS]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **cgroups** | OOM Killer의 기반 기술, 리눅스 자원 격리 |
| **K8s QoS Class** | Guaranteed·Burstable·BestEffort 사살 우선순위 |
| **JVM Heap** | Java 컨테이너 OOM의 90% 원인 |
| **CrashLoopBackOff** | OOM Killed 후 재시작 반복 상태 |
| **Vertical Pod Autoscaler** | OOM 방지를 위한 자동 limits 조정 도구 |

---
