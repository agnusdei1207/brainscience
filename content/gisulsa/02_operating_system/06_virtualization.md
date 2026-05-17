+++
weight = 6
title = "06. OS 가상화 & 컨테이너"
date = "2026-05-17"
[extra]
categories = "gisulsa-os"
+++

# 🎯 가상화 심화 — 하이퍼바이저 & 컨테이너

> **별점**: ★★★★★ | 기본 필수

## 1. 하이퍼바이저 유형

```
[Type 1 (Bare Metal)]
HW → 하이퍼바이저 → VM
직접 HW 위에서 동작
성능 우수, 보안 강함
예) VMware ESXi, KVM, Hyper-V, Xen

[Type 2 (Hosted)]
HW → Host OS → 하이퍼바이저 → VM
Host OS 위에 동작
성능 낮음, 개발·테스트용
예) VirtualBox, VMware Workstation

[전가상화 vs 반가상화]
전가상화(Full Virtualization):
  Guest OS 수정 불필요
  HW 에뮬레이션 (느림) or Intel VT-x (빠름)

반가상화(Para-virtualization):
  Guest OS 수정 필요 (하이퍼콜 사용)
  오버헤드 적음, 성능 우수
  예) Xen 반가상화 드라이버
```

## 2. 컨테이너 vs VM

```
VM (Virtual Machine):
  OS 전체 가상화
  무겁고 느린 부팅 (수분)
  강한 격리 (커널 분리)

컨테이너 (Container):
  OS 커널 공유, 프로세스 격리
  가볍고 빠른 부팅 (수초~ms)
  낮은 격리 (커널 취약점 공유 위험)

[Linux 컨테이너 기반 기술]
Namespace: PID/네트워크/파일시스템/IPC 격리
cgroups: CPU/메모리/I/O 자원 제한
Union FS: 이미지 레이어 (overlay2)
seccomp: 시스템 콜 필터링 (보안)

Docker → OCI 표준화 → containerd/CRI-O
```

## 3. 가상화 보안

```
[VM 탈출 (VM Escape)]
VM에서 하이퍼바이저·Host 접근 취약점
예) VMware 취약점, 가상화 소프트웨어 버그

[컨테이너 탈출]
privileged 컨테이너 → host 마운트 접근
커널 취약점 악용

[보안 강화]
gVisor: 사용자 공간 커널 (Google)
Kata Containers: VM 기반 컨테이너 (강한 격리)
Confidential Containers: TEE + 컨테이너
```

## 4. 답안 포인트

**3단락**: ① 하이퍼바이저 Type1/2 & 전/반가상화 → ② VM vs 컨테이너(Namespace/cgroups) → ③ 가상화 보안 위협 & gVisor/Kata

## 5. 관련 개념

`K8s(13_cloud 07번)` → 컨테이너 오케스트레이션 | `Confidential Computing(53번)` → 가상화 + 기밀 컴퓨팅 | `DevSecOps(15번)` → 컨테이너 이미지 보안
