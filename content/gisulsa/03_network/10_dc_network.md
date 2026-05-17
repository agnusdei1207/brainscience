+++
weight = 10
title = "10. 네트워크 인프라 설계"
date = "2026-05-17"
[extra]
categories = "gisulsa-network"
+++

# 🎯 데이터센터 네트워크 & Spine-Leaf

> **별점**: ★★★★★ | 기본 필수

## 1. 데이터센터 네트워크 아키텍처

```
[3계층 전통 아키텍처]
코어 계층 (Core): 초고속 L3 라우팅
집선 계층 (Aggregation/Distribution): VLAN, QoS
액세스 계층 (Access): 서버 연결

문제: 스패닝 트리(STP) 트래픽 차단 → 대역폭 낭비
     북-남 트래픽에 최적, 동-서 트래픽 취약

[Spine-Leaf 아키텍처]
Spine: 코어 스위치 (Leaf끼리 연결, ECMP)
Leaf: 서버/스토리지 연결 (ToR 스위치)
모든 Leaf는 모든 Spine에 연결 (Full-Mesh)

장점:
  동-서 트래픽 효율: 서버 간 통신 (MSA, 컨테이너)
  수평 확장: Spine/Leaf 추가만으로 확장
  예측 가능 지연: 최대 2홉 (Leaf→Spine→Leaf)
  ECMP: 모든 경로 사용 (최대 대역폭)
```

## 2. VXLAN & 오버레이 네트워크

```
[VXLAN (Virtual eXtensible LAN)]
L2 프레임을 UDP(4789)로 캡슐화
VLAN 4096개 한계 → VNI 16M개
데이터센터 간 L2 확장 가능

[오버레이 vs 언더레이]
언더레이: 물리 네트워크 (BGP, IP)
오버레이: 논리 네트워크 (VXLAN, Geneve)
K8s CNI: VXLAN 오버레이로 Pod 네트워크 구성

BGP EVPN (Ethernet VPN):
  VXLAN 제어 플레인 표준
  MAC/IP 정보를 BGP로 배포
  대규모 데이터센터 표준
```

## 3. 고속 인터커넥트

```
[InfiniBand]
HPC, AI 학습 클러스터 고속 연결
400Gb/s, 마이크로초 지연
RDMA: CPU 우회 직접 메모리 접근
NVIDIA NVLink + InfiniBand = DGX 슈퍼클러스터

[RoCE (RDMA over Converged Ethernet)]
이더넷 위의 RDMA
이더넷 인프라 재사용 + InfiniBand 성능
스토리지: NVMe-oF(TCP/RoCE) 활용
```

## 4. 답안 포인트

**3단락**: ① 3계층 vs Spine-Leaf 비교 & 동-서 트래픽 → ② VXLAN 오버레이 & BGP EVPN → ③ InfiniBand/RoCE AI 클러스터 인터커넥트

## 5. 관련 개념

`K8s(13_cloud)` → Pod 네트워크 = VXLAN 오버레이 | `GPU(01_ca 34번)` → NVLink + InfiniBand 학습 클러스터 | `SDN(05번)` → Spine-Leaf SDN 제어
