+++
weight = 7
title = "07. K8s 클러스터 운영"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# K8s 클러스터 운영 & 네트워크

> 별점: ★★★★★ | ★133회 기출

---

## 답안.

### Ⅰ. 개요

API Server: 모든 요청의 진입점 (REST API)
etcd: 클러스터 상태 저장 (분산 KV)
Controller Manager: 상태 루프 (ReplicaSet 유지)

### Ⅱ. 핵심 구성요소

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
```
[자동 스케일링]
HPA (Horizontal Pod Autoscaler):
  CPU/메모리 임계값 → 파드 수 자동 조절
  예) CPU 70% → 파드 2 → 4 → 8

VPA (Vertical Pod Autoscaler):
  파드 리소스 요청/제한 자동 조정

Cluster Autoscaler:


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
