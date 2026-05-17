+++
weight = 43
title = "43. 하이퍼바이저 & 가상화"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 하이퍼바이저 심화 & KVM

> **별점**: ★★★★★ | 기본 필수

## 1. KVM & QEMU

```
KVM (Kernel-based Virtual Machine):
  리눅스 커널 내장 하이퍼바이저 (Type 1 성능)
  인텔 VT-x, AMD-V 하드웨어 가속 활용
  → 게스트 OS가 직접 하드웨어 명령어 실행 가능

QEMU:
  CPU 에뮬레이터, KVM과 결합하여 사용
  KVM 없이 = 순수 소프트웨어 에뮬레이션 (느림)
  KVM + QEMU = 하드웨어 가속 VM (빠름)

[VirtIO]
반가상화 드라이버: 게스트-하이퍼바이저 효율적 I/O
  virtio-net, virtio-blk, virtio-gpu
```

## 2. 중첩 가상화 (Nested Virtualization)

```
VM 안에서 또 다른 VM 실행
  물리 HW → L0 하이퍼바이저 → L1 VM(하이퍼바이저) → L2 VM

용도:
  클라우드에서 K8s + VMware 테스트
  공개 클라우드에서 사설 클라우드 에뮬레이션

성능: 2계층 에뮬레이션 → 성능 저하 있음
지원: Intel VT-x VMCS 하드웨어 지원
```

## 3. 마이크로VM & Firecracker

```
[기존 VM 문제]
완전한 VM = 부팅 수십 초, 수백MB 메모리

[마이크로VM]
최소 보안 격리 유지 + 컨테이너 수준 가벼움
Firecracker (AWS Lambda 기반):
  KVM 기반 경량 VMM
  125ms 부팅, 5MB 메모리
  → Lambda, Fargate의 보안 격리 기반

gVisor (Google):
  사용자 공간 커널 → 시스템 콜 인터셉트
  완전한 VM보다 가볍고 컨테이너보다 격리 강함
```

## 4. 답안 포인트

**3단락**: ① KVM+QEMU 구조 & VirtIO 반가상화 → ② 중첩 가상화 활용 사례 → ③ 마이크로VM(Firecracker) & 서버리스 연계

## 5. 관련 개념

`컨테이너(02_os)` → VM vs 컨테이너 비교 | `서버리스(13_cloud)` → Firecracker가 Lambda 기반 | `K8s` → VMs on K8s (Virtual Kubelet)
