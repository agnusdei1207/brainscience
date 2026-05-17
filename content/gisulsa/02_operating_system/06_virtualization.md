+++
weight = 6
title = "06. OS 가상화 & 컨테이너"
date = "2026-05-17"
[extra]
categories = "gisulsa-os"
+++

# 가상화 심화 — 하이퍼바이저 & 컨테이너

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

예) VMware ESXi, KVM, Hyper-V, Xen
HW → Host OS → 하이퍼바이저 → VM
예) VirtualBox, VMware Workstation

### Ⅱ. 핵심 구성요소

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
```
VM (Virtual Machine):
  OS 전체 가상화
  무겁고 느린 부팅 (수분)
  강한 격리 (커널 분리)

컨테이너 (Container):


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
