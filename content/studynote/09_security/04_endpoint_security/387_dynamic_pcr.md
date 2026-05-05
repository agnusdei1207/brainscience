+++
weight = 387
title = "387. Dynamic PCR — Late Launch 동적 측정"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Dynamic PCR은 Intel TXT (Trusted Execution Technology)나 AMD SKINIT 명령어를 이용해 시스템 부팅 완료 후 특정 시점(late launch)에 DRTM (Dynamic Root of Trust for Measurement)을 확립하고, 이미 실행 중인 환경과 무관하게 신뢰할 수 있는 측정 기준점을 새로 설정하는 기술이다.
> 2. **가치**: Static PCR이 UEFI 펌웨어 신뢰에 의존하는 것과 달리, Dynamic PCR은 OS가 실행 중인 상태에서도 하이퍼바이저·보안 OS를 신뢰할 수 있는 환경에서 시작할 수 있어 펌웨어 취약점 위협을 우회한다.
> 3. **판단 포인트**: Dynamic PCR은 PCR 17-22를 사용하며, Intel TXT의 SINIT ACM (Authenticated Code Module)이 측정의 루트가 되어 MLE (Measured Launch Environment) 진입 전 시스템 상태를 검증한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

Static PCR (S-CRTM)의 근본적 한계는 UEFI 펌웨어 자체를 신뢰해야 한다는 점이다. 펌웨어 루트킷이나 UEFI 변조가 있을 경우 Static 측정 전체가 오염될 수 있다. Dynamic PCR은 이 문제를 해결하기 위해 시스템이 이미 실행 중인 상태에서 별도의 하드웨어 메커니즘으로 신뢰 기준점을 새로 확립한다.

Intel TXT의 GETSEC[SENTER] 명령어 또는 AMD SKINIT 명령어가 실행되면, CPU는 현재 실행 중인 모든 소프트웨어를 일시 중단하고, SMI (System Management Interrupt)·인터럽트를 차단한 후, SINIT ACM (Intel 디지털 서명된 인증 코드 모듈)을 실행해 시스템 상태를 검증한다. 이후 MLE (Measured Launch Environment)—주로 하이퍼바이저나 보안 부팅 코드—가 PCR 17부터 시작하는 Dynamic PCR에 측정값을 기록한다.

📢 **섹션 요약 비유**: Dynamic PCR은 수사관이 현장에 도착해서 "지금부터 내가 직접 증거를 수집한다"고 선언하는 것—이전에 조작됐을 가능성을 배제하고 새로 시작한다.

---

## 2. 구성요소

| PCR 번호 | 사용 기술 | 측정 내용 |
|:---|:---|:---|
| PCR 17 | Intel TXT | SINIT ACM 측정 |
| PCR 18 | Intel TXT | MLE (tboot/Hypervisor) 측정 |
| PCR 19-22 | Intel TXT | MLE 정의 측정 |
| PCR 17 | AMD SKINIT | SKL (Secure Kernel Loader) 측정 |

```text
┌──────────────────────────────────────────────────────┐
│          Intel TXT Late Launch 흐름                  │
├──────────────────────────────────────────────────────┤
│                                                      │
│  [시스템 정상 부팅 완료]                             │
│  (Static PCR 0-7 이미 기록됨)                        │
│                                                      │
│  GETSEC[SENTER] 실행 (Late Launch 시작)              │
│       │                                              │
│       ▼                                              │
│  CPU: 모든 다른 프로세서 중단                        │
│  CPU: SMI/인터럽트 차단                              │
│       │                                              │
│       ▼                                              │
│  SINIT ACM 로드 및 실행 (Intel 서명 검증)            │
│  ┌────────────────────────────────────────┐          │
│  │ SINIT이 하드웨어 상태 검증             │          │
│  │ PCR17 = SHA256(SINIT_ACM)              │          │
│  │ PCR18 = SHA256(MLE_header)             │          │
│  └────────────────────────────────────────┘          │
│       │                                              │
│       ▼                                              │
│  [MLE 진입] → 신뢰할 수 있는 환경에서 실행          │
│  (tboot 하이퍼바이저, Xen, KVM 등)                  │
│                                                      │
│  Dynamic PCR 17-22: Late Launch 측정값               │
│  이전 Static PCR과 독립적                            │
└──────────────────────────────────────────────────────┘
```

**DRTM의 핵심 특성**: 이전에 실행 중이던 소프트웨어가 어떤 상태였는지에 관계없이 새로운 신뢰 체인을 시작할 수 있다. 오염된 OS 위에서도 신뢰할 수 있는 측정 환경을 확립할 수 있다는 것이 Static PCR 대비 핵심 차별점이다.

📢 **섹션 요약 비유**: DRTM은 기존 건물을 철거하지 않고 그 위에 독립적인 방폭 컨테이너를 새로 설치하는 것—컨테이너 내부는 외부 오염과 격리된다.

---

## 3. 구조 및 동작 원리

| 항목 | Static PCR (S-CRTM) | Dynamic PCR (D-CRTM) |
|:---|:---|:---|
| 측정 시작 시점 | 전원 투입 즉시 | OS 부팅 후 (Late Launch) |
| 신뢰 앵커 | UEFI 펌웨어 | CPU 하드웨어 (SINIT ACM) |
| 펌웨어 변조 시 | 신뢰 체인 오염 | 독립적 새 체인 수립 |
| PCR 범위 | PCR 0-15 | PCR 17-22 |
| 구현 기술 | UEFI 표준 | Intel TXT, AMD SKINIT |

📢 **섹션 요약 비유**: Static은 처음부터 믿고 시작하는 것, Dynamic은 중간에 신분증을 다시 확인하는 것—두 번째 확인이 더 철저하다.

---

## 4. 비교 및 트레이드오프

**Intel TXT 기반 tboot**  
- Xen·KVM 하이퍼바이저의 신뢰 부팅에 활용  
- PCR 17-18에 하이퍼바이저 측정값 기록  
- 원격 증명으로 클라우드 VM의 하이퍼바이저 무결성 검증  

**AMD SEV (Secure Encrypted Virtualization) 연동**  
- AMD SKINIT + SEV-SNP (Secure Nested Paging)로 VM 측정 및 암호화 결합  
- PCR 값과 SEV 증명 리포트를 결합한 완전한 VM 무결성 증명  

**활용 시나리오**  
1. 클라우드 컨피덴셜 컴퓨팅: VM 시작 시 Dynamic PCR로 무결성 증명  
2. TPM봉인 + DRTM: 특정 하이퍼바이저 환경에서만 키 해제  
3. SIEM 연동: PCR 값 변화 탐지 시 보안 알림  

📢 **섹션 요약 비유**: Intel TXT는 "이미 켜진 가스레인지 불꽃을 끄지 않고 새로운 안전밸브를 설치하는" 기술—기존 환경을 건드리지 않고 신뢰 구역을 만든다.

---

## 5. 실무 적용 및 최적화 기법

Dynamic PCR과 DRTM은 펌웨어 취약점이 난무하는 환경에서 하이퍼바이저와 보안 OS의 무결성을 보장하는 고급 기술이다. 클라우드 컨피덴셜 컴퓨팅(Confidential Computing)의 핵심 구성 요소로 부상하고 있으며, Intel SGX·AMD SEV-SNP와 결합해 "신뢰할 수 없는 클라우드 인프라에서의 기밀 컴퓨팅"을 가능하게 한다.

📢 **섹션 요약 비유**: Dynamic PCR은 의심스러운 호텔 방(클라우드 서버)에서 자신만의 잠금 장치(DRTM)를 설치해 안전하게 작업하는 기술이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Intel TXT | 구현 기술 | SINIT ACM 기반 DRTM |
| AMD SKINIT | 구현 기술 | AMD CPU의 DRTM 명령 |
| SINIT ACM | 신뢰 앵커 | Intel 서명 인증 코드 모듈 |
| tboot | 활용 사례 | Intel TXT 기반 신뢰 부팅 |
| Confidential Computing | 응용 분야 | 클라우드에서 DRTM 활용 |

### 👶 어린이를 위한 3줄 비유 설명
Dynamic PCR은 컴퓨터가 이미 켜진 상태에서 "잠깐, 지금부터 내가 직접 확인할게"라며 새로 검사를 시작하는 거예요.  
이전에 뭔가 나쁜 프로그램이 있었더라도, 이 검사는 독립적으로 진행돼서 더 믿을 수 있어요.  
클라우드 서버처럼 믿기 어려운 환경에서도 내 프로그램이 안전하게 실행됐는지 증명할 수 있어요.
