+++
weight = 385
title = "385. Measured Boot — TPM 이용 부팅 측정"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Measured Boot는 부팅 과정의 각 단계(UEFI 펌웨어→부트로더→OS 커널→드라이버)의 해시를 TPM (Trusted Platform Module)의 PCR (Platform Configuration Register)에 순차적으로 누적 기록해 부팅 무결성을 측정·증명하는 기술이다.
> 2. **가치**: Secure Boot가 "차단"이라면 Measured Boot는 "기록"—Secure Boot로 막지 못한 변조를 원격 증명(Remote Attestation)으로 사후 탐지할 수 있으며, 변조된 환경에서 암호화 키 해제를 차단하는 BitLocker/TPM 시일링(sealing)의 기반이 된다.
> 3. **판단 포인트**: PCR 체인은 순차적 확장(extend) 방식으로 설계돼 이전 값을 변경할 수 없으며, 최종 PCR 값은 전체 부팅 과정의 지문(fingerprint)이 된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

Measured Boot (측정된 부팅)는 UEFI 플랫폼에서 TPM과 연동해 부팅 무결성을 수학적으로 증명하는 기술이다. TCG (Trusted Computing Group) 표준에 정의되어 있으며, Intel TXT (Trusted Execution Technology)·Microsoft Windows Measured Boot·Android Verified Boot 등에 구현됐다.

Secure Boot가 미허가 코드의 실행을 "차단"하는 예방 메커니즘이라면, Measured Boot는 실행된 코드의 해시를 "기록"하는 탐지 메커니즘이다. 두 기술은 상호 보완적이다.

핵심 활용 시나리오는 두 가지다. ①BitLocker·LUKS의 볼륨 암호화 키를 TPM PCR 값에 묶어두어, 부팅 환경이 변조되면 키를 자동으로 차단한다. ②원격 증명(Remote Attestation)으로 네트워크에 연결하는 디바이스가 신뢰할 수 있는 부팅 상태인지 검증한다.

📢 **섹션 요약 비유**: Measured Boot는 체인 계약서—각 서명(측정값)이 이전 것과 연결되어, 하나라도 위조하면 전체 계약이 무효가 된다.

---

## 2. 구성요소

**PCR 확장 연산**  
```
PCR_new = SHA256(PCR_old || measurement)
```
각 부팅 단계의 해시를 이전 PCR 값과 연결(concatenate)해 새로운 PCR 값을 계산한다. 이 단방향 해시 체인은 과거 측정값을 변경하면 이후 모든 PCR 값이 달라지므로 위변조가 불가능하다.

| PCR 번호 | 측정 내용 |
|:---|:---|
| PCR 0 | UEFI 펌웨어 코드 |
| PCR 1 | UEFI 펌웨어 설정 |
| PCR 2-3 | 옵션 ROM, 기타 플랫폼 코드 |
| PCR 4 | MBR/UEFI 부트 애플리케이션 |
| PCR 5-6 | 파티션 테이블 등 |
| PCR 7 | Secure Boot 상태 |
| PCR 8-15 | OS 정의 (GRUB, Windows Boot Manager 등) |

```text
┌──────────────────────────────────────────────────────┐
│           Measured Boot PCR 체인 형성               │
├──────────────────────────────────────────────────────┤
│                                                      │
│  [UEFI 펌웨어]                                       │
│  Hash(UEFI) → Extend(PCR0)                          │
│                │                                     │
│                ▼                                     │
│  [부트로더]                                          │
│  Hash(Bootloader) → Extend(PCR4)                    │
│  PCR4_new = SHA256(PCR4_old || Hash(Bootloader))    │
│                │                                     │
│                ▼                                     │
│  [OS 커널]                                          │
│  Hash(Kernel) → Extend(PCR8)                        │
│                │                                     │
│                ▼                                     │
│  [드라이버·설정]                                    │
│  Hash(Drivers) → Extend(PCR9)                       │
│                │                                     │
│                ▼                                     │
│  [최종 PCR 값] = 전체 부팅 과정의 지문              │
│  BitLocker/LUKS가 이 PCR 값에 키를 봉인(seal)       │
└──────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: PCR 체인은 도미노—하나가 바뀌면 이후 모든 도미노가 달라져서 최종 결과가 완전히 달라진다.

---

## 3. 구조 및 동작 원리

| 항목 | Measured Boot | Secure Boot |
|:---|:---|:---|
| 주요 기능 | 부팅 상태 측정·기록 | 미서명 코드 실행 차단 |
| TPM 필요 여부 | 필수 | 불필요 (UEFI db만으로 가능) |
| 변조 대응 | 사후 탐지 + 키 봉인 해제 차단 | 실행 전 차단 |
| 원격 증명 | 가능 | 불가 |
| 클라우드 활용 | Confidential VM 증명 | 플랫폼 부팅 보안 |

📢 **섹션 요약 비유**: Secure Boot는 입구 경비원, Measured Boot는 CCTV 녹화—경비원이 못 막은 것을 녹화로 나중에 잡을 수 있다.

---

## 4. 비교 및 트레이드오프

**BitLocker + TPM 시일링**  
BitLocker는 볼륨 암호화 키를 TPM의 PCR 0·2·4·7·11·12·13에 봉인한다. 부팅 환경이 변조되면 PCR 값이 달라져 TPM이 키 해제를 거부—부트킷·UEFI 루트킷 설치 후 재부팅 시 BitLocker가 복구 키를 요구하게 된다.

**원격 증명 활용**  
- Microsoft Azure Attestation: VM의 PCR 값을 원격 검증 후 비밀 데이터 제공  
- Google Confidential VMs: AMD SEV + TPM 측정값으로 VM 무결성 증명  
- 제로트러스트 NAC: 접속 전 Measured Boot 상태 검증 후 네트워크 접근 허용  

📢 **섹션 요약 비유**: BitLocker + TPM 시일링은 금고 비밀번호를 집 구조 자체에 연동—집 구조가 바뀌면(부팅 환경 변조) 비밀번호도 작동 안 한다.

---

## 5. 실무 적용 및 최적화 기법

Measured Boot는 제로트러스트 아키텍처에서 "디바이스 신뢰 검증"의 핵심 기술이다. 엔드포인트가 신뢰할 수 있는 상태로 부팅됐음을 수학적으로 증명하지 않으면 기업 리소스 접근을 허용하지 않는 정책에서, Measured Boot + 원격 증명이 디바이스 컴플라이언스 검증의 기반이 된다.

📢 **섹션 요약 비유**: Measured Boot는 "내가 건강하다"는 의료 진단서—접속 전에 시스템 건강 상태를 수학적으로 증명한다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| TPM PCR | 측정 저장소 | 부팅 측정값 누적 해시 저장 |
| BitLocker 시일링 | 활용 사례 | PCR 값에 암호화 키 봉인 |
| 원격 증명 | 원격 검증 | 외부 검증자가 PCR 값 확인 |
| Intel TXT | 연관 기술 | 동적 Measured Boot 지원 |
| Secure Boot | 보완 기술 | 차단(예방) + 측정(탐지) 이중 방어 |

### 👶 어린이를 위한 3줄 비유 설명
Measured Boot는 컴퓨터가 켜지는 각 단계마다 "지금 뭐가 실행됐는지" 도장을 찍어 기록하는 기능이에요.  
이 도장이 하나라도 다르면(변조 감지) 중요한 파일의 암호(BitLocker)가 열리지 않아요.  
마치 학교에서 출석 도장을 매일 찍어서, 빠진 날이 있으면 시험을 못 보게 하는 것과 비슷해요.
