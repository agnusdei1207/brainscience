+++
weight = 43
title = "43. 하이퍼바이저 & 가상화"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 하이퍼바이저 심화 & KVM

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

KVM (Kernel-based Virtual Machine):
  리눅스 커널 내장 하이퍼바이저 (Type 1 성능)
  인텔 VT-x, AMD-V 하드웨어 가속 활용

### Ⅱ. 핵심 구성요소

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
```
VM 안에서 또 다른 VM 실행
  물리 HW → L0 하이퍼바이저 → L1 VM(하이퍼바이저) → L2 VM

용도:
  클라우드에서 K8s + VMware 테스트
  공개 클라우드에서 사설 클라우드 에뮬레이션

성능: 2계층 에뮬레이션 → 성능 저하 있음
지원: Intel VT-x VMCS 하드웨어 지원
```
```
[기존 VM 문제]
완전한 VM = 부팅 수십 초, 수백MB 메모리


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
