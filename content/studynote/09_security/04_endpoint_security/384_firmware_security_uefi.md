+++
weight = 384
title = "384. 펌웨어 보안 UEFI Secure Boot"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: UEFI Secure Boot는 부트 프로세스에서 로드되는 모든 실행 코드(UEFI 드라이버, 부트로더, OS 로더)의 디지털 서명을 검증해 서명되지 않거나 신뢰하지 않는 코드의 실행을 차단하는 펌웨어 수준 무결성 보호 메커니즘이다.
> 2. **가치**: 부트킷·UEFI 루트킷·오염된 OS 로더를 초기 부팅 단계에서 차단해 OS 보안 소프트웨어가 시작되기 전의 공격을 막는 최초 방어선 역할을 한다.
> 3. **판단 포인트**: Secure Boot의 한계는 UEFI 펌웨어 자체가 변조됐거나 유효한 서명 인증서가 탈취된 경우—TPM Measured Boot와 함께 적용해야 더 강력한 부팅 무결성을 보장한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

UEFI (Unified Extensible Firmware Interface) Secure Boot는 UEFI 2.3.1 Errata C 사양에 정의된 표준으로, 2012년 Windows 8 출시와 함께 상용 PC에 광범위하게 도입됐다. 기존 BIOS/MBR 환경에서는 부트 코드 서명 검증이 없어 부트킷(Bootkit)이 OS 로더를 교체하는 것이 가능했다.

Secure Boot의 핵심 아이디어는 "신뢰 체인(Chain of Trust)"이다. UEFI 펌웨어가 루트 신뢰(Root of Trust)가 되어 부트로더를 검증하고, 부트로더는 OS 커널을 검증하고, OS 커널은 드라이버를 검증하는 계층적 신뢰 구조를 형성한다.

📢 **섹션 요약 비유**: Secure Boot는 공항 보안 검색대—탑승 전에 모든 짐(부트 코드)을 X-ray로 검사하고, 신원(서명) 확인된 승객만 비행기(OS)에 탑승시킨다.

---

## 2. 구성요소

**Secure Boot 키 데이터베이스**  

| 키/DB | 역할 | 내용 |
|:---|:---|:---|
| PK (Platform Key) | 최상위 신뢰 키 | OEM/소유자의 루트 서명 키 |
| KEK (Key Exchange Key) | PK 서명으로 보호 | db/dbx 업데이트 권한 |
| db (Signature Database) | 허용 목록 | 신뢰하는 서명·해시 |
| dbx (Forbidden Signatures) | 거부 목록 | 취소된 서명·해시 |

```text
┌──────────────────────────────────────────────────────┐
│           UEFI Secure Boot 신뢰 체인                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  [전원 ON]                                           │
│       │                                              │
│       ▼                                              │
│  [UEFI 펌웨어] ← PK로 보호된 신뢰 루트              │
│  db에 있는 서명만 허용                               │
│       │                                              │
│       ▼                                              │
│  [Boot Manager] ← 서명 검증 (db 대조, dbx 거부)     │
│       │                                              │
│       ▼                                              │
│  [OS 부트로더]  ← Microsoft/Linux CA 서명 필요       │
│  (bootmgfw.efi, grub.efi 등)                         │
│       │                                              │
│       ▼                                              │
│  [OS 커널] ← 커널 코드 서명 검증                    │
│       │                                              │
│       ▼                                              │
│  [시스템 시작 완료]                                   │
└──────────────────────────────────────────────────────┘
```

**UEFI dbx (거부 목록) 관리**: 취약한 부트로더(예: BlackLotus에서 악용된 취약한 shim 버전)가 발견되면 dbx에 해당 해시를 추가해 차단한다. Microsoft는 정기적으로 dbx 업데이트를 배포한다.

**Secure Boot와 Linux**: 대부분의 Linux 배포판은 Microsoft 제3자 CA가 서명한 shim 부트로더를 사용해 Secure Boot 환경에서 부팅한다.

📢 **섹션 요약 비유**: db는 입장 허용 명단, dbx는 블랙리스트—둘 다 최신 상태로 유지해야 보안이 유지된다.

---

## 3. 구조 및 동작 원리

| 항목 | Secure Boot | Measured Boot (TPM) |
|:---|:---|:---|
| 목적 | 부팅 코드 실행 차단 | 부팅 상태 측정·기록 |
| 동작 방식 | 서명 검증 (허용/차단) | PCR에 해시 누적 저장 |
| 변조 대응 | 실행 자체 차단 | 원격 증명으로 사후 탐지 |
| 취약점 | 서명 키 탈취, 펌웨어 자체 변조 | TPM 물리 공격 |

📢 **섹션 요약 비유**: Secure Boot는 출입 통제, Measured Boot는 출입 기록—전자는 나쁜 사람을 막고, 후자는 들어온 사람의 발자국을 기록한다.

---

## 4. 비교 및 트레이드오프

**Secure Boot 관리**  
1. PK·KEK는 하드웨어 보안 모듈(HSM)에서 관리—키 탈취 방지  
2. dbx 업데이트 정기 적용 (Windows Update 자동 포함, Linux는 fwupd)  
3. 사용자 지정 Secure Boot: 기업 환경에서 자체 CA로 db 등록 (MOK: Machine Owner Key)  
4. Secure Boot 상태 검증: `mokutil --sb-state` (Linux), UEFI 설정 화면 확인  
5. 취약한 부트로더 해시를 dbx에 추가 관리  

**BlackLotus 교훈 (2023)**: CVE-2022-21894를 악용해 패치된 시스템에서도 Secure Boot를 우회—dbx 업데이트의 중요성을 재확인.

📢 **섹션 요약 비유**: dbx 업데이트를 안 하는 것은 블랙리스트를 갱신하지 않는 것—이미 알려진 위험인물도 통과시킬 수 있다.

---

## 5. 실무 적용 및 최적화 기법

UEFI Secure Boot는 현대 엔드포인트 보안의 기반이며, Windows 11이 TPM 2.0과 함께 Secure Boot를 필수 요건으로 지정한 것은 이 중요성을 반영한다. Secure Boot + TPM Measured Boot의 조합은 부팅 무결성 보증을 강화하며, 하드웨어 신뢰 루트(HW RoT)에서 OS까지 이어지는 완전한 신뢰 체인 구축이 가능하다.

📢 **섹션 요약 비유**: Secure Boot는 컴퓨터가 켜질 때부터 "이 코드는 믿을 수 있는가?"를 묻는 것—신뢰는 처음부터 시작해야 진짜 신뢰다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| TPM Measured Boot | 보완 기술 | PCR 기반 부팅 상태 측정·원격 증명 |
| dbx | 핵심 구성 | 취소된 부트로더 차단 목록 |
| MOK | 사용자 확장 | 기업 자체 CA 등록 메커니즘 |
| BlackLotus | 취약점 사례 | Secure Boot 우회 UEFI 부트킷 |
| shim | Linux 연동 | Microsoft CA 서명 경유 Linux 부팅 |

### 👶 어린이를 위한 3줄 비유 설명
Secure Boot는 컴퓨터가 켜질 때 "이 프로그램이 안전한 사람(공인된 회사)이 만든 것인지" 서명을 확인하는 기능이에요.  
서명이 없거나 가짜 서명이면 실행 자체를 차단해 바이러스가 켜지기 전에 막아요.  
이 기능은 Windows 11에서는 반드시 켜져 있어야 하는 기본 보안 요건이에요.
