+++
weight = 446
title = "446. 다중 클러스터 OOM 킬링 정책 스케줄 (Kubernetes OOM Killer & Multi-Cluster Scheduling)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kubernetes(K8s)의 OOM(Out of Memory) Killer는 노드의 물리 메모리가 고갈될 때 Linux 커널이 oom_score_adj 값 기반으로 희생할 프로세스(Pod)를 선택하여 강제 종료하는 마지막 방어선이다.
> 2. **가치**: Requests/Limits 정확 설정과 QoS(Quality of Service) 클래스 이해를 통해 OOM 종료를 예방하고, 다중 클러스터 환경에서 Cluster Autoscaler와 VPA(Vertical Pod Autoscaler)를 결합하면 메모리 위기를 사전에 방지할 수 있다.
> 3. **판단 포인트**: OOM 종료의 근본 원인은 Pod의 메모리 Limit 미설정 또는 과소 설정이며, 기술사는 메모리 튜닝보다 애플리케이션 메모리 누수(Memory Leak) 탐지와 Limit 최적화를 우선 처방해야 한다.

## Ⅰ. 개요 및 필요성

쿠버네티스 클러스터에서 OOM은 가장 흔하고 치명적인 운영 장애 원인 중 하나이다. "Pod가 갑자기 재시작된다"는 신고의 80% 이상이 OOM에 의한 것이다. 문제는 OOM 이벤트가 발생하면 서비스가 아무 예고 없이 중단되고, 운영팀은 로그에서 `OOMKilled` 상태를 발견하고서야 원인을 파악하게 된다는 점이다.

Linux 커널의 OOM Killer는 메모리 압박 시 *oom_score*가 높은 프로세스를 우선 종료한다. K8s는 이 메커니즘 위에 **QoS 클래스** 개념을 추가하여, 어느 Pod를 먼저 종료할지에 대한 정책을 제공한다.

다중 클러스터(Multi-Cluster) 환경에서는 단일 클러스터의 메모리 포화가 다른 클러스터의 스케줄링에도 영향을 미치므로, **Federation 수준의 메모리 거버넌스**가 필요하다.

📢 **섹션 요약 비유**: OOM 강제 종료는 불이 난 배에서 무게를 줄이기 위해 짐을 바다에 버리는 것처럼, 배(서버)가 가라앉지 않으려면 가장 값어치 없는 짐(BestEffort Pod)부터 버리는 응급 처치이다.

## Ⅱ. 아키텍처 및 핵심 원리

### K8s QoS 클래스 및 OOM 우선순위

| QoS 클래스 | 조건 | oom_score_adj | 종료 우선순위 |
|:---|:---|:---:|:---|
| **Guaranteed** | requests == limits (모든 컨테이너) | -997 | 가장 마지막 (보호) |
| **Burstable** | requests < limits (일부 설정) | 2~999 | 중간 |
| **BestEffort** | requests/limits 미설정 | 1000 | 가장 먼저 종료 |

### OOM 발생 흐름

```
┌─────────────────────────────────────────────────────────────┐
│               OOM 이벤트 발생 및 K8s 대응 흐름              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Pod 메모리 사용 증가                                     │
│       │                                                     │
│       ▼                                                     │
│  2. [컨테이너 Limit 초과?]                                   │
│       │ Yes                    │ No                        │
│       ▼                        ▼                           │
│  3. cgroups 메모리 제한 →  계속 할당 허용                    │
│     컨테이너 OOM 강제 종료                                   │
│       │                                                     │
│       ▼                                                     │
│  4. kubelet이 Pod 상태를 OOMKilled로 기록                   │
│       │                                                     │
│       ▼                                                     │
│  5. restartPolicy에 따라 Pod 재시작                         │
│     (Always: 재시작, OnFailure: 비정상 종료 시만 재시작)     │
│                                                             │
│  ※ 노드 전체 메모리 고갈 시:                                 │
│     Linux 커널 OOM Killer가 직접 oom_score 기준으로 선택    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### VPA(Vertical Pod Autoscaler) vs HPA(Horizontal Pod Autoscaler)

| 항목 | VPA | HPA |
|:---|:---|:---|
| 스케일 방향 | 수직 (개별 Pod의 requests/limits 조정) | 수평 (Pod 수 증가) |
| 적합 워크로드 | 단일 프로세스, 스테이트풀 앱 | 웹 서버, 상태 없는 마이크로서비스 |
| OOM 예방 | requests 자동 상향 조정 | Pod 추가로 메모리 부담 분산 |
| 단점 | 적용 시 Pod 재시작 필요 | 메모리 누수 워크로드에는 효과 없음 |

📢 **섹션 요약 비유**: QoS 클래스는 비행기 탑승권 등급과 같다. 퍼스트 클래스(Guaranteed) 승객은 마지막까지 탑승 유지되고, 이코노미 무임승차(BestEffort)는 비행기가 과적이면 첫 번째로 하기되는 정책이다.

## Ⅲ. 비교 및 연결

### 다중 클러스터 메모리 관리 전략

| 전략 | 도구 | 설명 |
|:---|:---|:---|
| 클러스터 오토스케일러 | Cluster Autoscaler | 노드 메모리 부족 시 VM 자동 추가 |
| 연합 스케줄링 | Karmada, Clusternet | 워크로드를 여러 클러스터에 분산 배치 |
| 메모리 과부하 감지 | Prometheus + AlertManager | MemoryUsage > 85% 시 사전 알림 |
| LimitRange | K8s 기본 기능 | 네임스페이스별 기본 메모리 Limit 강제 |

### 노드 압박 퇴거(Node Pressure Eviction)

메모리 부족 시 kubelet이 OOM Killer 발동 전에 Pod를 정상 종료(graceful eviction)하는 사전 방어 메커니즘:
- `--eviction-hard=memory.available<100Mi`: 가용 메모리 100Mi 이하 시 퇴거 시작
- `--eviction-soft=memory.available<200Mi`: 2분 유예 후 소프트 퇴거

📢 **섹션 요약 비유**: 노드 압박 퇴거는 홍수 대피령처럼, 물이 완전히 차기 전에 미리 주민을 다른 곳으로 이동시키는 사전 예방 조치이다. OOM 강제 종료는 이미 물이 차서 강제 탈출하는 상황이다.

## Ⅳ. 실무 적용 및 기술사 판단

### OOM 예방을 위한 기술사 체크리스트

1. **모든 Pod에 requests/limits 설정 의무화** (LimitRange로 네임스페이스 수준 강제)
2. **메모리 Limit = JVM 힙 + 네이티브 메모리 + 여유분(10~20%)** 공식으로 계산
3. **Prometheus 메모리 사용 모니터링** + `container_oom_events_total` 메트릭 알림 설정
4. **VPA Recommendation Mode 실행** 후 실제 사용량 데이터로 Limit 재조정
5. **메모리 누수 탐지**: Java의 경우 `-XX:+HeapDumpOnOutOfMemoryError` 옵션으로 힙 덤프 수집 자동화

```
┌──────────────────────────────────────────────────────────┐
│         OOM 예방 권장 메모리 설정 공식                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Java 컨테이너:                                          │
│  Limit = JVM 힙(-Xmx) + MetaSpace + 스레드 스택         │
│        + 기타 네이티브 + 버퍼 (15~20%)                  │
│                                                          │
│  예시: Xmx=1G, MetaSpace=256Mi, 버퍼=256Mi              │
│  → Limit = 1536Mi  Request = 1024Mi                     │
│                                                          │
│  주의: JVM은 Limit을 초과해도 GC로 버티려다              │
│        결국 OOMKilled 당하는 경우 빈번 → Limit 넉넉히!  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Pod 메모리 Limit 설정은 자동차 연료통 크기를 정하는 것과 같다. 너무 작으면 중간에 서고(OOM 종료), 너무 크면 다른 차(Pod)가 연료를 못 받는다.

## Ⅴ. 기대효과 및 결론

**기대효과**:
- OOM 종료 발생률 90% 이상 감소 (Limit 최적화 + VPA 적용 시)
- 클러스터 전체 메모리 효율 25% 향상 (BestEffort → Guaranteed 전환)
- 서비스 가용성(SLA 99.9%) 달성을 위한 OOM 관련 재시작 제거

**한계 및 전제조건**:
- VPA 적용은 Pod 재시작이 수반되어 스테이트풀 워크로드에 부작용 가능
- 메모리 누수(Memory Leak)가 있는 애플리케이션은 Limit을 아무리 올려도 재발
- 다중 클러스터 연합 스케줄링은 지연 증가 및 네트워크 비용 발생 트레이드오프

**미래**: eBPF 기반의 세밀한 메모리 추적과 AI 예측 모델을 결합한 **예측적 메모리 관리(Predictive Memory Management)**가 K8s 표준 기능으로 통합될 전망이다.

📢 **섹션 요약 비유**: OOM 관리의 진화는 마치 병원의 응급실 → 정기 건강검진 → 예방 의학으로의 전환처럼, 사후 처리(OOM 강제 종료)에서 사전 예방(VPA + 예측 모델)으로 성숙해가는 여정이다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| QoS 클래스 | 핵심 정책 | Guaranteed/Burstable/BestEffort 우선순위 결정 |
| VPA | 예방 도구 | Pod 메모리 requests/limits 자동 최적화 |
| LimitRange | 강제 정책 | 네임스페이스별 기본 Limit 설정 강제화 |
| cgroups | 구현 기반 | 컨테이너 메모리 제한의 Linux 커널 기반 |
| Cluster Autoscaler | 확장 전략 | 노드 메모리 고갈 시 VM 자동 추가 |
| Prometheus | 모니터링 | OOM 이벤트 메트릭 수집 및 알림 |

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안에 방(메모리)이 있는데, 프로그램들이 너무 많이 방을 쓰면 넘쳐요.
2. 그럼 컴퓨터가 "방이 부족해!" 하면서 가장 덜 중요한 프로그램(BestEffort Pod)을 강제로 끄는 게 OOM 종료예요.
3. 미리 각 프로그램에게 방 크기(Limit)를 정해주면 이런 싸움이 안 일어나요!
