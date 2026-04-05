+++
weight = 882
title = "82. Kubelet (큐블렛)"
description = "Kubelet: 쿠버네티스 워커 노드에서 파드를 생성,관리,모니터링하는 노드별 에이전트"
date = 2026-03-26

[taxonomies]
tags = ["kubernetes", "k8s", "kubelet", "pod-lifecycle", "node-agent", "cri"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Kubelet은 쿠버네티스 워커 노드에 배치되는 에이전트로, 마스터 노드의 API Server로부터 파드 생성/관리 명령을 수신하고 Container Runtime을 통해 실제 컨테이너를 실행하며, 그 상태를 지속적으로 모니터링하여 마스터에 보고하는"현장 관리자"이다.
> 2. **가치**: Kubelet이 없으면 마스터의 명령이 워커 노드에 전달되지 못하고, 파드의 헬스체크나 자동 복구 메커니즘이 동작하지 않아 수동 운영이 불가피해진다.
> 3. **융합**: CRI(Container Runtime Interface)를 통해 containerd, CRI-O 등 다양한 런타임과 연동可能하며, cAdvisor를 통해 자원 사용량 메트릭을 수집하고, Pleaser를 통해 파드 레벨의 접근 권한을 관리한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

Kubelet은 쿠버네티스 클러스터에서"각 워커 노드에 상주하는 관리자"이다. 마스터 노드의 API Server가 클러스터 전체의"두뇌"라면, Kubelet은 각 노드에 파견된"현장 관리자"이다. Kubelet은 자신이 할당된 노드의 상태를常に監視し、 마스터가 명령한 파드가 제대로 실행되고 있는지를 확인하고, 문제가 있으면 스스로 복구하려고 시도하거나 마스터에 보고한다. 이는 서버 관점에서"각 서버에 설치되는 Agent"와 유사한 개념이다.

### 마스터-노드通信의 다리

쿠버네티스 아키텍처에서 마스터 노드와 워커 노드는 직접 통신하지 않는다. 모든 제어 명령은 API Server를 통해間接적으로 이루어진다. Kubelet은 API Server를 Watch하여 자신이 담당하는 노드에 할당된 파드 목록을 가져오고, 파드 스펙에 따라 Container Runtime에 컨테이너 생성을 요청하며, 실행 결과를 다시 API Server에 보고한다. 이 모든 과정이 마스터 노드에 Polling하지 않고, Kubelet이 능동적으로 API Server에 접근하여 수행된다.

### 비유

Kubelet을"호텔 각 층의 서비스 매니저"에 비유할 수 있다. 호텔 본부(마스터)가"404호에 손님이 도착한다"고 알려주면, 해당 층의 서비스 매니저(Kubelet)가 객실 준비 상태를 확인하고, housekeeping staff(Container Runtime)에게 침구 세팅을 지시하고, 작업이 완료되면 본부에"404호 준비 완료"를 보고한다. 서비스 매니저가 없으면 본부의 지시가 층에 도달하지 못하고, 각 층의 상황도 본부에報告되지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Kubelet의 주요 기능

Kubelet은 파드生命周期管理를 위해 다양한 기능을 수행한다. 첫째,"파드 스펙 수신"이다. API Server의特定の Namespace以下の Pod 리소스를 Watch하여, 자신에게 할당된 파드 목록을取得한다. 둘째,"컨테이너 생성/시작/중지"이다. 파드 스펙에 따라 Container Runtime에 CRI(Container Runtime Interface) 호출을 수행한다. 셋째,"헬스체크 실행"이다. Liveness Probe, Readiness Probe, Startup Probe를주기에 맞춰 실행하고, 실패 시 정略에 따른 조치를 취한다. 넷째,"상태 보고"이다. 파드의 현재 상태, 자원 사용량, 이벤트 등을 API Server에報告하여 etcd에 저장되도록 한다.

### Container Runtime Interface (CRI)

CRI는 Kubelet과 Container Runtime 사이의通信を標準化する 인터페이스이다. CRI 이전에는 Kubelet이 Docker Engine과直接 통신하여 Docker에 종속적이었다. CRI 도입으로 containerd, CRI-O, frakti 등 다양한 런타임을 선택적으로 사용할 수 있게 되었다. CRI의 주요 API는 "RuntimeService::ListContainers", "RuntimeService::CreateContainer", "RuntimeService::StartContainer", "RuntimeService::StopContainer", "RuntimeService::RemoveContainer"등이 있다.

```
[ Kubelet과 CRI의 관계 ]

┌─────────────────────────────────────────────────────────────────────────┐
│                        Kubelet (워커 노드)                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  파드 관리자 (Pod Manager)                                        │  │
│  │  • 파드 스펙 캐시 관리                                              │  │
│  │  • 파드 레벨 설정(shutdown deadline 등)                           │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  CRI.stub (gRPC Client)                                           │  │
│  │  • 컨테이너 생성/시작/중지/삭제 요청                                │  │
│  │  • 이미지 풀 요청                                                  │  │
│  │  • 컨테이너 상태 조회                                              │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
└──────────────────────────────│──────────────────────────────────────────┘
                               │ gRPC (Unix Socket or TCP)
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Container Runtime (containerd 등)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  CRI Service (gRPC Server)                                        │  │
│  │  RuntimeService + ImageService                                    │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  containerd (실제 컨테이너 실행)                                    │  │
│  │  • OCI 런타임 (runc) 호출                                          │  │
│  │  • 컨테이너生命周期的管理                                           │  │
│  │  • 네트워크 설정 (CNI 연동)                                         │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Kubelet 내부에서 파드 관리는 여러 서브 모듈로分工된다. Pod Manager가 파드 스펙을 캐시하고, CRI.stub이 gRPC를 통해 Container Runtime에 요청을 전달한다. Container Runtime은 OCI 런타임(runc)을 호출하여 실제 컨테이너를 생성하고, CNI(Container Network Interface)를 연동하여 네트워크를 설정한다. 이 분산 구조로 인해 각コンポーネントが独立して 발전할 수 있다.

### cAdvisor와 자원 모니터링

 Kubelet은 cAdvisor(Container Advisor)를 통해 컨테이너의 자원 사용량을 모니터링한다. cAdvisor는 각 노드에서 실행되는 시스템 데몬으로, CPU, Memory, Network, Disk I/O등의 메트릭을 수집한다. 이 메트릭은 Kubernetes 내부적으로 HPA(Horizontal Pod Autoscaler)의判断資料로 사용되며, Prometheus 같은 외부 모니터링 시스템도 Kubelet의_metrics_endpoint를 통해 데이터를 수집할 수 있다.

### 상태 보고와 Kubelet vs 노드 상태

 Kubelet이 보고하는 파드 상태는 "phase"로 표현된다. "Pending"은 파드가 아직 노드에 배치되지 않은 상태, "Running"은 적어도 한 개의 컨테이너가 실행 중이거나 재시작 중인 상태, "Succeeded"는 모든 컨테이너가 성공적으로 종료되고 재시작되지 않을 상태, "Failed"는 모든 컨테이너가 실패로 종료된 상태, "Unknown"은 Kubelet과 API Server 간 통신이 불가능한 상태이다.

### 섹션 비유

 Kubelet의 CRI를 통한 런타임 연동은"통역사를 통한 국제 회의"에 비유할 수 있다. 회의 진행자(Kubelet)는 한국어로 된 의제를 받지만, 직접 영어를話すことができず, 통역사(CRI)를 통해 영국인 참가자(containerd)에게 전달한다. 통역사가 없으면 회의 진행자는英国 참가자와 의사소통할 수 없고, 英国 참가자도 한국어 의제를 이해할 수 없다. CRI는 이러한"언어 장벽"을 해소하는 표준화된 통역 시스템이다.

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### Kubelet vs systemd vs Docker Swarm Agent

| 비교 항목 | Kubelet | systemd | Docker Swarm Agent |
|:---|:---|:---|:---|
| **관리 대상** | 파드 (컨테이너 그룹) | 시스템 서비스 | 서비스 (컨테이너) |
| **마스터 연동** | API Server Watch | 없음 (로컬) | Manager 노드 연동 |
| **자동 복구** | Liveness Probe 기반 | Restart=on-failure | 복제 기반 자동 복구 |
| **네트워킹** | CNI 연동 | 로컬 네트워크 | Overlay 네트워크 |
| **확장성** | 수천 노드 지원 | 단일 노드 | 수십 노드 |

### Kubelet과 마스터 연결 단절 시 동작

 Kubelet과 API Server 간의 연결이 끊어지면, Kubelet은 어떻게 동작할까? 결론부터 말하면,"현재 실행 중인 파드는 계속 실행"된다. Kubelet은 일시적인 API Server 연결 단절에 관계없이, 로컬에 캐시된 파드 스펙을 기반으로 컨테이너를 계속 관리한다. 그러나 새로운 파드 생성이나 기존 파드 삭제는 API Server 연결이 복원될 때까지 대기한다. 이러한設計により、マスターの負荷分散と耐障害性が確保された.

### Pleaser와 시큐어 쿠버네티스

 Kubelet은 Pleaser를 통해 파드의 보안 설정을 관리한다. Pod Security Policy(PSP, 쿠버네티스 1.21에서 deprecated)나 Pod Security Standards(PSS)를 통해 파드의 privileged 모드 실행, 호스트 네트워크 사용, 호스트 파드景德使用等の security context를强制할 수 있다. Kubelet은 이러한 정책에不合致하는 파드를 실행 거부한다.

### 섹션 비유

 Kubelet의 ローカル 캐시 동작은"오프라인에서도 운영 가능한 자급식 점포"에 비유할 수 있다. 본사와의通信線が切断되어도、각 점포는 이미 受領한 재고 정보(파드 스펙)를 기반으로 상품 판매(파드 실행)를 계속한다. 그러나 새로운 商品 주문(새 파드 생성)이나 商品 회수(파드 삭제)는通信恢复 후에만 가능하다. 이러한設計により、일시적 네트워크 장애에도 서비스가 계속될 수 있다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### Kubelet 설정 항목

 Kubelet을 프로덕션 환경에서 설정할 때 주의해야 할 주요 항목은 다음과 같다. **--container-runtime-endpoint**는 원격 containerd 소켓 경로를 지정하며, **--kubeconfig**는 마스터 연결용 kubeconfig 파일 경로를 지정한다. **--pod-infra-container-image**는 인프라 컨테이너(pause) 이미지를 지정하며, 기본값은 registry.k8s.io/pause:3.x이다. **--image-pull-progress-deadline**은 이미지 풀 최대 대기 시간을 설정한다. **--runtime-request-timeout**은 CRI 요청의 타임아웃을 설정한다.

### Kubelet 인증/인가

 Kubelet의 API Server 접근은 안전하게 인증/인가되어야 한다. Kubelet은"--kubeconfig"로 지정된 kubeconfig 파일의 인증 정보(클라이언트 인증서, 토큰 등)를 사용하여 API Server에 접근한다. 이 kubeconfig는 일반적으로 노드 프로비저닝 시 자동으로 생성되며, Kubelet의 역할(RBAC)은 "system:node:*"로 노드가 관리하는 자신의 파드만 접근 가능하도록 제한된다.

### Kubelet 메트릭 endpoint

 Kubelet은 **/metrics** 엔드포인트를 통해 Prometheus 형식의 메트릭을 제공한다. 주요 메트릭으로는 "kubelet_pod_worker_duration" (파드 작업 소요 시간), "kubelet_cgroup_status" (cgroup 상태), "container_memory_usage_bytes" (컨테이너 메모리 사용량), "container_cpu_usage_seconds_total" (컨테이너 CPU 사용량)등이 있다. 이 메트릭들을 Grafana로 시각화하면 Kubelet과 워커 노드의 성능을 실시간으로 모니터링할 수 있다.

### 섹션 비유

 Kubelet 메트릭 수집은"공장 안전 센서"에 비유할 수 있다. 각 작업장(노드)에는 온도, 먼지, 소음 등을 측정하는 센서(cAdvisor)가 설치되어 있고, 중앙 관제실(모니터링 시스템)이 실시간으로 데이터를 수집한다. 센서가 없으면 작업장 상태를 알 수 없고,異常 발생을 미리 파악할 수 없다. Kubelet 메트릭 endpoint는 이러한 센서 데이터를 수집하는 통로이다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 기대 효과

 Kubelet을 제대로 이해하고 설정하면, 파드 lifecycle 관리의 모든 측면을 세밀하게 제어할 수 있다. 적절한 Probe 설정으로 애플리케이션의 가용성을 높이고, 올바른 cgroup 설정으로 자원 사용을 최적화하며, 메트릭 수집을 통해 사전에 문제를 예방할 수 있다. Kubelet은 쿠버네티스 아키텍처에서"마스터와 워커 사이의 다리"로서, 이 다리가 탄탄해야 클러스터 전체가 안정적으로 운영된다.

### 핵심 정리

 Kubelet은 쿠버네티스 워커 노드의 핵심 에이전트로, 마스터의 명령을 받아 파드를 생성/관리하고, Container Runtime과 CRI를 통해 실제 컨테이너를 실행하며, 상태를 모니터링하여 마스터에 보고한다. CRI 덕분에 다양한 Container Runtime과 연동 가능하며, cAdvisor를 통해 메트릭을 수집하여 HPA 등의 자동 확장에 활용된다.

### 섹션 비유

 Kubelet은"각 사무실에 배치된 자원 관리 담당자"에 비유할 수 있다. 본사(마스터)에서 전체 인력 운용的计划(파드 스펙)을 세우면, 각 부서의 담당자(Kubelet)가 해당 부서에 배정된 인력(파드)을 파악하고, 근무 환경(Container Runtime)을 준비하며, 근태情况(헬스체크)을 모니터링하여 본사에報告한다. 담당자의 철저한 관리가 있어야全局の人員運用が効率的行われる.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **CRI (Container Runtime Interface)** | Kubelet과 Container Runtime 사이의 통신을 표준화하여 다양한 런타임 연동을 가능하게 한다. |
| **cAdvisor** | Kubelet 내장 컨테이너 메트릭 수집기로, 자원 사용량 데이터를 제공한다. |
| **Pod Infra Container (pause)** | 파드의 네트워크 네임스페이스를 제공하는 특수 컨테이너이다. |
| **Liveness/Readiness/Startup Probe** | Kubelet이 실행하는 헬스체크로, 파드의 상태를 판단한다. |
| **cgroups** | Kubelet이 Container Runtime과 함께 사용하여 컨테이너의 자원 사용량을 제한한다. |
| **CNI (Container Network Interface)** | Kubelet이 컨테이너 네트워크 설정을 위해 호출하는 플러그인 인터페이스이다. |
