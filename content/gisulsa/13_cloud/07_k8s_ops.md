+++
weight = 7
title = "07. K8s 클러스터 운영"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 🎯 K8s 클러스터 운영 & 네트워크

> **별점**: ★★★★★ | ★133회 기출

## 1. K8s 핵심 아키텍처

```
[K8s 컨트롤 플레인]
API Server: 모든 요청의 진입점 (REST API)
etcd: 클러스터 상태 저장 (분산 KV)
Controller Manager: 상태 루프 (ReplicaSet 유지)
Scheduler: 파드 배치 결정

[Worker Node]
kubelet: 파드 실행·모니터링 (노드 에이전트)
kube-proxy: 네트워크 규칙 (iptables/IPVS)
컨테이너 런타임: containerd, CRI-O

[K8s 오브젝트]
Pod: 최소 배포 단위 (1+컨테이너)
Deployment: 파드 롤링 업데이트 관리
Service: 파드 로드밸런싱 (ClusterIP/NodePort/LB)
Ingress: HTTP 라우팅, TLS 종료
ConfigMap/Secret: 설정 외부화
PVC: 영속 스토리지 요청
```

## 2. K8s 스케일링 & 자가 치유

```
[자동 스케일링]
HPA (Horizontal Pod Autoscaler):
  CPU/메모리 임계값 → 파드 수 자동 조절
  예) CPU 70% → 파드 2 → 4 → 8

VPA (Vertical Pod Autoscaler):
  파드 리소스 요청/제한 자동 조정

Cluster Autoscaler:
  노드 부족 → 클라우드 API로 노드 자동 추가

[자가 치유]
Liveness Probe: 파드 재시작 결정
Readiness Probe: 트래픽 전달 여부 결정
파드 재시작: CrashLoopBackOff → 자동 재시작
```

## 3. K8s 네트워크

```
[K8s 네트워크 원칙]
모든 파드는 NAT 없이 서로 통신 가능
파드 IP는 클러스터 내 고유

CNI 플러그인:
Calico: 네트워크 정책, BGP 라우팅
Cilium: eBPF 기반, 고성능, 관찰 가능성
Flannel: 단순 오버레이, 소규모

Service Mesh:
Istio, Linkerd → mTLS, 트래픽 관리, 분산 트레이싱
```

## 4. 답안 포인트

**3단락**: ① K8s 아키텍처(컨트롤플레인+노드) → ② 스케일링(HPA/VPA/CA) & 자가치유 → ③ 네트워크(CNI, 서비스 메시)

## 5. 관련 개념

`eBPF(★02_os 24번)` → Cilium CNI의 기반 | `GitOps(☆예측)` → ArgoCD로 K8s 배포 자동화 | `MSA(★133회)` → K8s는 MSA 오케스트레이션
