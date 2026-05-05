+++
weight = 388
title = "388. Intel TXT (Trusted Execution Technology)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Intel TXT (Trusted Execution Technology)는 CPU·칩셋·TPM 하드웨어를 결합해 DRTM (Dynamic Root of Trust for Measurement) 기반의 신뢰 실행 환경을 구축하는 Intel의 하드웨어 보안 기술로, 신뢰할 수 없는 소프트웨어 스택 위에서도 안전한 코드 실행을 보장한다.
> 2. **가치**: 클라우드·가상화 환경에서 하이퍼바이저 무결성을 검증하고, 고위험 데이터 처리 환경에서 소프트웨어 공격에 강건한 격리 실행 영역을 제공한다.
> 3. **판단 포인트**: Intel TXT는 SGX(프로세스 수준 격리)와 달리 하이퍼바이저·OS 수준의 신뢰 부팅을 제공하며, SINIT ACM의 서명 검증이 신뢰의 핵심이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

Intel TXT (Trusted Execution Technology)는 2007년 처음 도입된 Intel의 하드웨어 보안 기술이다. Safer Computing Initiative의 일환으로, DRTM을 통해 특정 실행 환경(MLE: Measured Launch Environment)의 무결성을 CPU 수준에서 보장한다.

TXT가 필요한 이유는 기존 소프트웨어 신뢰 체인의 한계다. UEFI→부트로더→OS→하이퍼바이저의 연쇄 신뢰 구조에서 어느 한 링크가 오염되면 전체가 무너진다. TXT는 CPU 하드웨어를 직접 신뢰 앵커로 사용해 이 체인을 새로 시작할 수 있다.

주요 활용 분야는 클라우드 컨피덴셜 컴퓨팅(Confidential Computing), 신뢰 하이퍼바이저 부팅, 그리고 원격 증명(Remote Attestation)이다. VMware vSphere의 vTPM과 GETSEC[SENTER]를 결합한 신뢰 부팅이 대표적 사례다.

📢 **섹션 요약 비유**: Intel TXT는 오염된 수사 현장에서 "증거 봉투를 다시 봉인"하는 CPU—어떤 소프트웨어도 믿지 않고 하드웨어 자체가 공정성을 보장한다.

---

## 2. 구성요소

| 구성 요소 | 역할 | 설명 |
|:---|:---|:---|
| CPU TXT 지원 | 하드웨어 실행 | GETSEC 명령어 집합 제공 |
| 칩셋 TXT 지원 | DMA 보호 | VT-d IOMMU로 DMA 공격 차단 |
| TPM | PCR 저장소 | Dynamic PCR 17-22 기록 |
| SINIT ACM | 신뢰 앵커 | Intel 서명된 인증 코드 모듈 |
| MLE | 실행 환경 | 하이퍼바이저/신뢰 OS |

```text
┌──────────────────────────────────────────────────────┐
│              Intel TXT 실행 흐름                     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. GETSEC[SENTER] 실행                              │
│     → 모든 AP (Application Processor) 중단           │
│     → SMI 차단, 인터럽트 비활성화                    │
│                                                      │
│  2. SINIT ACM 로드                                   │
│     → CPU: Intel CA로 서명 검증                      │
│     → 검증 실패 시 리셋                              │
│                                                      │
│  3. SINIT 실행                                       │
│     → 하드웨어 상태 검증 (DMA 보호 확인 등)          │
│     → PCR17 = Hash(SINIT_ACM)                        │
│     → PCR18 = Hash(MLE_header)                       │
│                                                      │
│  4. MLE 진입                                         │
│     → 신뢰할 수 있는 하이퍼바이저/OS 실행            │
│     → PCR 19-22에 추가 측정값 기록                   │
│                                                      │
│  5. 원격 증명                                        │
│     → TPM Quote (PCR + AIK 서명)                    │
│     → 원격 검증자에게 무결성 증명                    │
└──────────────────────────────────────────────────────┘
```

**DMA 보호 (VT-d IOMMU)**: TXT 실행 중 DMA (Direct Memory Access) 공격을 차단하기 위해 VT-d (Virtualization Technology for Directed I/O) IOMMU가 활성화된다. 악성 PCI 장치가 MLE 메모리를 직접 읽거나 수정하는 것을 막는다.

**GETSEC 명령어 집합**  
- GETSEC[CAPABILITIES]: TXT 지원 기능 조회  
- GETSEC[ENTER ACX]: ACM 실행  
- GETSEC[SENTER]: Late Launch 시작  
- GETSEC[SEXIT]: Measured Environment 종료  

📢 **섹션 요약 비유**: SINIT ACM은 법원 공증인—인텔이 서명한 중립적 검사관으로, 부팅 환경을 공정하게 검증한다.

---

## 3. 구조 및 동작 원리

| 항목 | Intel TXT | Intel SGX |
|:---|:---|:---|
| 보호 수준 | 하이퍼바이저/OS 수준 | 프로세스/애플리케이션 수준 |
| 격리 방식 | DRTM + PCR | 엔클레이브 메모리 암호화 |
| 공격자 모델 | 오염된 부팅 스택 | 악성 OS/하이퍼바이저 |
| 원격 증명 | TPM-based Quote | EPID/DCAP 기반 증명 |
| 가용 여부 | 현재 deprecated 추세 | 여전히 활발 |

📢 **섹션 요약 비유**: TXT는 건물 전체(OS/하이퍼바이저)를 검증, SGX는 특정 방(프로세스)만 보호—목적과 범위가 다르다.

---

## 4. 비교 및 트레이드오프

**tboot (Trusted Boot) 활용**  
- Xen·KVM 하이퍼바이저 앞에 배치되는 TXT 기반 신뢰 부트로더  
- 오픈소스 프로젝트, Intel·Citrix·Red Hat 지원  
- PCR 17-18에 tboot 측정값 기록 후 하이퍼바이저로 제어 이전  

**클라우드 활용**  
- 물리 호스트의 TXT 활성화로 하이퍼바이저 무결성 원격 증명  
- 임차인(테넌트)이 자신의 VM이 신뢰할 수 있는 호스트에서 실행됨을 검증  

**최신 동향**  
Intel은 TXT의 일부 기능을 SGX·Trust Domain Extensions (TDX)로 통합·진화시키는 추세다. TDX는 VM 수준 신뢰 실행 환경을 제공한다.

📢 **섹션 요약 비유**: Intel TXT는 클라우드 호텔이 "우리 방은 도청 안 됩니다"라고 증명하는 기술—투숙객(테넌트)이 직접 확인할 수 있다.

---

## 5. 실무 적용 및 최적화 기법

Intel TXT는 신뢰할 수 없는 인프라 위에서 신뢰 실행 환경을 구축하는 핵심 기술로, Confidential Computing의 이론적 기반을 제공했다. 현재는 SGX·TDX로 진화하고 있지만, TXT의 DRTM 개념과 SINIT ACM 신뢰 체인은 여전히 현대 하드웨어 보안의 기본 원리로 남아있다. 기술사 답안에서는 "하드웨어 신뢰 루트 → DRTM → PCR 측정 → 원격 증명"의 흐름으로 서술하면 완성도가 높다.

📢 **섹션 요약 비유**: Intel TXT는 신뢰의 뿌리(Root of Trust)를 하드웨어에 고정시키는 것—뿌리가 튼튼해야 나무(소프트웨어 스택) 전체가 안전하다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DRTM | 핵심 기능 | 동적 신뢰 루트 측정 확립 |
| SINIT ACM | 신뢰 앵커 | Intel 서명 인증 코드 모듈 |
| tboot | 구현체 | TXT 기반 신뢰 부트로더 |
| Intel SGX | 진화 방향 | 프로세스 수준 신뢰 실행 |
| Intel TDX | 최신 기술 | VM 수준 신뢰 도메인 확장 |

### 👶 어린이를 위한 3줄 비유 설명
Intel TXT는 컴퓨터가 켜진 상태에서도 "지금부터 완전히 새로운 안전 구역을 만들겠다"고 선언하는 CPU 기능이에요.  
나쁜 프로그램들이 이미 실행 중이더라도, 이 안전 구역(MLE) 안에서는 안전하게 일할 수 있어요.  
클라우드 서버에서 내 데이터가 정말로 안전한지 수학적으로 증명할 수 있게 해줘요.
