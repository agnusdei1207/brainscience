+++
weight = 10
title = "10. 네트워크 인프라 설계"
date = "2026-05-17"
[extra]
categories = "gisulsa-network"
+++

# 데이터센터 네트워크 & Spine-Leaf

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

코어 계층 (Core): 초고속 L3 라우팅
집선 계층 (Aggregation/Distribution): VLAN, QoS
액세스 계층 (Access): 서버 연결

### Ⅱ. 핵심 구성요소

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
```
[VXLAN (Virtual eXtensible LAN)]
L2 프레임을 UDP(4789)로 캡슐화
VLAN 4096개 한계 → VNI 16M개
데이터센터 간 L2 확장 가능

[오버레이 vs 언더레이]
언더레이: 물리 네트워크 (BGP, IP)
오버레이: 논리 네트워크 (VXLAN, Geneve)
K8s CNI: VXLAN 오버레이로 Pod 네트워크 구성


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
