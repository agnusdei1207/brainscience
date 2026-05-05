+++
weight = 30
title = "30. UEFI vs BIOS — 현대 펌웨어 부팅 표준"
date = "2026-04-29"
[extra]
categories = "studynote-operating-system"
+++

## 0. 핵심 인사이트

> **핵심**: BIOS(Basic Input/Output System)는 16비트 리얼 모드로 실행되는 레거시 펌웨어로 1MB 이하 주소 공간·MBR 디스크 구조에 묶인다. UEFI(Unified Extensible Firmware Interface)는 32/64비트 보호 모드에서 실행되며 GPT 디스크·2.2TB 이상 용량·Secure Boot를 지원한다.
> **비유**: UEFI vs BIOS — 현대 펌웨어 부팅 표준은(는) 복잡한 교통을 한 번에 통제해 전체 흐름을 맞추는 신호 체계와 같다.

---

📝 모범 답안

## 1. 개요 및 필요성

```text
BIOS 부팅 흐름:
  전원 → POST → MBR(512B) → 부트로더 → OS 커널

  한계:
  - 16비트 실모드: 1MB 메모리만 접근
  - MBR: 최대 2.2TB 디스크
  - 파티션: 최대 4개 기본 파티션
  - 텍스트 기반 설정 화면

UEFI 부팅 흐름:
  전원 → SEC → PEI → DXE → BDS → 부트매니저 → OS

  장점:
  - 64비트 보호 모드
  - GPT: 최대 9.4ZB 디스크, 128개 파티션
  - GUI 설정 화면, 네트워크 스택, GPU 드라이버
  - Secure Boot: 서명된 부트로더만 실행
```

---

## 2. 구성요소

### UEFI 부팅 단계 (PI Specification)

| 단계 | 영문 | 역할 |
|:---|:---|:---|
| **SEC** | Security | CPU 초기화, 임시 RAM 설정 |
| **PEI** | Pre-EFI Init | 메모리 초기화 |
| **DXE** | Driver Execution | 드라이버 로드, 서비스 초기화 |
| **BDS** | Boot Device Select | 부팅 디바이스 결정 |
| **RT** | Runtime | OS 실행 중 UEFI 런타임 서비스 |
| **AL** | After Life | S3 절전 복귀 등 |

### Secure Boot 흐름

```text
UEFI 펌웨어 → db(허용 서명 목록) 확인
부트로더 서명 검증 → 성공: 로드
                    → 실패: 부팅 중단

Microsoft → Windows 서명 키 포함
Linux    → shim(MOK) 통해 GRUB 서명 검증
커스텀  → 자체 키 등록 (MOK - Machine Owner Key)
```

---

## 3. 구조 및 원리

**핵심 조건**: 운영체제의 해당 메커니즘은 현재 상태 정보, 자원 제약, 정책 기준이 함께 정합성을 가질 때 안정적으로 동작한다.

동작 순서:
1. **요청 또는 이벤트 발생**: 사용자 요청, 인터럽트, 시스템 호출 등으로 커널이 해당 기능을 처리할 필요가 생긴다.
2. **현재 상태 확인**: 커널은 큐, 제어 블록, 메타데이터, 자원 가용량을 확인해 실행 가능 여부와 우선순위를 판단한다.
3. **정책 적용 및 자원 배정**: 해당 주제의 핵심 정책에 따라 상태 전이, 자원 할당, 보호 검사를 수행한다.
4. **결과 반영 및 후속 처리**: 처리 결과를 시스템 상태에 기록하고 다음 인터럽트·스케줄링·복구 단계로 연결한다.

| 비교 | BIOS | UEFI |
|:---|:---|:---|
| 실행 모드 | 16비트 실모드 | 32/64비트 보호 모드 |
| 디스크 | MBR (최대 2.2TB) | GPT (최대 9.4ZB) |
| 파티션 수 | 4개 | 128개 |
| Secure Boot | ❌ | ✅ |
| GUI 설정 | ❌ (텍스트) | ✅ |
| 부팅 속도 | 느림 | 빠름 (Fast Boot) |

---

## 4. 비교 및 연결

| 비교 | BIOS | UEFI |
|:---|:---|:---|
| 실행 모드 | 16비트 실모드 | 32/64비트 보호 모드 |
| 디스크 | MBR (최대 2.2TB) | GPT (최대 9.4ZB) |
| 파티션 수 | 4개 | 128개 |
| Secure Boot | ❌ | ✅ |
| GUI 설정 | ❌ (텍스트) | ✅ |
| 부팅 속도 | 느림 | 빠름 (Fast Boot) |

---

## 5. 실무 적용 및 판단

### 디스크 구조: MBR vs GPT

```text
MBR (Master Boot Record):
  └─ 512바이트 섹터 0
      ├─ 부트 코드 (446B)
      ├─ 파티션 테이블 (64B, 4엔트리)
      └─ 시그니처 (2B: 0x55AA)

GPT (GUID Partition Table):
  └─ 섹터 0: 보호 MBR
  └─ 섹터 1: GPT 헤더 (CRC32 체크섬)
  └─ 섹터 2-33: 128개 파티션 엔트리
  └─ 마지막 섹터: 백업 GPT 헤더
```

### 서버 환경 UEFI 고려사항

```text
- Secure Boot: 서버 OS 서명 키 등록 필요
- iSCSI/PXE 부팅: UEFI 네트워크 스택 활용
- TPM 2.0: UEFI Secure Boot + TPM = 측정 부팅 (Measured Boot)
- 가상화: VM에서 UEFI 부팅 (OVMF 오픈소스 UEFI)
```

---

## 6. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **보안 강화** | Secure Boot로 부트킷 차단 |
| **대용량 디스크** | GPT로 2.2TB 한계 초과 |
| **빠른 부팅** | Fast Boot, POST 간소화 |

ARM 기반 서버(AWS Graviton, Ampere Altra)와 임베디드 시스템에서는 U-Boot 같은 경량 부트로더가 UEFI 역할을 하며, UEFI의 복잡성 없이 빠른 부팅을 제공한다.

---

## 7. 발전 흐름도

```text
[BIOS — 16비트 레거시 펌웨어, MBR]
    │
    ▼
[UEFI — 64비트 현대 펌웨어, GPT, Secure Boot]
    │
    ▼
[Secure Boot + TPM — 측정 부팅, 무결성 보장]
    │
    ▼
[Confidential Computing — AMD SEV, Intel TDX]
    │
    ▼
[ARM/RISC-V 부팅 — U-Boot, EDK2, 오픈 펌웨어 표준화]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **GRUB** | UEFI 부트로더 표준 (Linux) |
| **TPM 2.0** | UEFI Secure Boot와 연계 |
| **GPT** | UEFI 디스크 파티션 표준 |
| **Secure Boot** | 부트킷·루트킷 방어 |
| **U-Boot** | ARM 임베디드 경량 부트로더 |
