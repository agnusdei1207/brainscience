+++
weight = 42
title = "42. DPU & SmartNIC"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 DPU (Data Processing Unit) & SmartNIC

> **별점**: ★★★★☆ | ☆ 예측

## 1. DPU 정의

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

## 2. SmartNIC

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
```

## 3. 데이터센터 인프라 오프로딩

```
[기존 문제]
서버 CPU의 30~40%가 인프라 처리에 낭비
암호화, 가상 스위칭, 스토리지 → CPU 부담

[DPU 해결]
인프라 작업 → DPU로 이전 → CPU 해방
CPU 전부 → 애플리케이션에 집중

[eBPF + SmartNIC]
eBPF 프로그램을 SmartNIC에 오프로드
네트워크 가속 + 커널 프로그래밍 결합
```

## 4. 답안 포인트

**3단락**: ① DPU 정의 & CPU/GPU와 역할 구분 → ② SmartNIC 구현 & 인프라 오프로딩 → ③ AWS Nitro & 보안 격리 사례

## 5. 관련 개념

`eBPF(★02_os 24번)` → SmartNIC eBPF 오프로드 | `SDN(03_net)` → DPU 기반 소프트웨어 정의 인프라 | `가상화(43번)` → DPU로 가상화 오프로딩
