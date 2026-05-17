+++
weight = 42
title = "42. DPU & SmartNIC"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# DPU (Data Processing Unit) & SmartNIC

> 별점: ★★★★☆ | ☆ 예측

---

## 답안.

### Ⅰ. 개요

CPU: 범용 컴퓨팅 (응용 프로그램)
GPU: 병렬 데이터 처리 (AI, 그래픽)
DPU: 인프라 오프로딩 (네트워크, 스토리지, 보안)

### Ⅱ. 핵심 구성요소

```
CPU: 범용 컴퓨팅 (응용 프로그램)
GPU: 병렬 데이터 처리 (AI, 그래픽)
DPU: 인프라 오프로딩 (네트워크, 스토리지, 보안)

DPU = 데이터 센터의 '세 번째 칩'
      (CPU + GPU + DPU)

[DPU 담당 작업]
네트워크: 패킷 처리, 방화벽, 로드밸런서
스토리지: NVMe-oF, 스토리지 가상화
보안: 암호화/복호화, IPSec, TLS
가상화: OVS (Open vSwitch) 오프로딩
```
```
NIC(네트워크 인터페이스) + 프로그래밍 가능 프로세서

[SmartNIC 유형]
FPGA 기반: Microsoft Catapult, Azure SmartNIC
ARM 기반: NVIDIA BlueField DPU
ASIC 기반: 특화 처리

[DPDK & SR-IOV]
DPDK: 커널 우회 고성능 패킷 처리
SR-IOV: PCIe 가상화, VM에 직접 NIC 노출

[주요 제품]
NVIDIA BlueField-3: ARM + RDMA + 네트워크
Intel IPU (Infrastructure Processing Unit)
AWS Nitro: EC2 DPU (보안 격리)


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
