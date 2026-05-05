+++
weight = 364
title = "364. UEFI 부트킷 (UEFI Bootkit)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: UEFI 부트킷은 UEFI(Unified Extensible Firmware Interface) 펌웨어에 악성 드라이버를 삽입하여 하드디스크 교체·OS 재설치 후에도 살아남는 "불멸의 지속성"을 달성하는 가장 고급 부트킷이다.
> 2. **가치**: LoJax(2018, APT28/Fancy Bear), CosmicStrand(2022, 중국 APT), BlackLotus(2023, CVE-2022-21894 악용)는 모두 실제 야생에서 발견된 UEFI 부트킷으로, 국가 수준 APT의 핵심 무기다.
> 3. **판단 포인트**: 방어는 UEFI Secure Boot + Intel Boot Guard(CPU에서 UEFI 서명 검증) + 정기 펌웨어 업데이트 + SPI 플래시 쓰기 방지가 4중 기준이며, Secure Boot 비활성화 또는 MOK 취약점이 있으면 우회 가능하다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

UEFI는 BIOS의 후속으로, 부팅 과정을 관리하는 펌웨어 표준이다. UEFI 코드는 SPI(Serial Peripheral Interface) 플래시 칩에 저장되며, 운영체제와 완전히 분리된 환경에서 실행된다. UEFI 부트킷은 이 플래시 칩에 악성 UEFI 애플리케이션/드라이버를 삽입하여 OS 로드 전 단계에서 영속적으로 실행된다.

BlackLotus(2023)는 특히 주목받는 사례로, Secure Boot가 활성화된 Windows 11 시스템에서도 CVE-2022-21894(BootHole 변형) 취약점을 이용해 Secure Boot를 우회하고 UEFI 레벨에서 커널 드라이버를 로드했다. 이는 Secure Boot 자체가 취약점 없이는 절대적 방어가 아님을 보여줬다.

📢 **섹션 요약 비유**: UEFI 부트킷은 집 기초 공사 때 벽 안에 감청 장치(악성 드라이버)를 심는 것—집(OS)을 부수고 다시 지어도 기초(펌웨어)는 그대로다.

---

## 2. 구성요소

### UEFI 부트킷 동작 구조

| 단계 | 동작 | 설명 |
|:---|:---|:---|
| 감염 | SPI 플래시 쓰기 | 악성 UEFI 드라이버를 플래시에 삽입 |
| 부팅 초기화 | DXE(Driver Execution Environment) 단계 | 악성 드라이버가 호출됨 |
| 커널 패치 | ExitBootServices() 전후 | 커널 로드 전/후 패치 삽입 |
| 지속 | 재부팅·재설치 후에도 | 플래시 칩은 디스크 포맷 무관 |

```
┌──────────────────────────────────────────────────────┐
│           UEFI 부트킷 감염 구조                       │
├──────────────────────────────────────────────────────┤
│  SPI 플래시 칩                                       │
│  ┌──────────────────────────────────────────┐        │
│  │  정상 UEFI 드라이버들...                │        │
│  │  [악성 UEFI 드라이버] ← 삽입됨          │        │
│  └──────────────────────────────────────────┘        │
│                                                     │
│  부팅 시:                                           │
│  UEFI POST → DXE → [악성 드라이버 실행]             │
│           → OS 커널 패치 → ExitBootServices        │
│           → Windows/Linux 부팅 (이미 감염)          │
└──────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: UEFI 플래시는 집 전기 배선도(DXE 드라이버 목록)—배선도에 몰래 추가 회로(악성 드라이버)를 삽입하면 집이 새로 지어져도 전기는 항상 악성 회로를 통과한다.

---

## 3. 구조 및 동작 원리

| 구분 | MBR 부트킷 | UEFI 부트킷 |
|:---|:---|:---|
| 저장 위치 | 디스크 MBR | SPI 플래시(마더보드) |
| OS 재설치 생존 | 아니오 | 예 |
| 하드디스크 교체 생존 | 아니오 | 예 |
| Secure Boot 우회 | Legacy BIOS에서만 | 취약점(CVE) 필요 |
| 제거 방법 | MBR 복구 | 펌웨어 업데이트/교체 |

📢 **섹션 요약 비유**: MBR 부트킷은 문(MBR)을 교체하면 해결되지만, UEFI 부트킷은 집 기초(플래시)를 뜯어고쳐야 해결된다.

---

## 4. 비교 및 트레이드오프

UEFI 부트킷 방어: ① Intel Boot Guard(CPU 내장 ACM이 UEFI 서명 검증, 펌웨어 수정 불가 모드), ② Secure Boot(부트로더·커널 서명 검증, 취약점 패치 필수), ③ UEFI 펌웨어 정기 업데이트(알려진 UEFI 취약점 패치), ④ CHIPSEC(UEFI 펌웨어 보안 점검 도구)로 정기 검사.

탐지: CHIPSEC `platform.py`, `uefi.py`로 UEFI 드라이버 목록 해시 검증. Kaspersky Firmware Scanner, VirusTotal의 UEFI 모듈 스캔.

📢 **섹션 요약 비유**: Intel Boot Guard는 공장(CPU 제조사)이 집 배선도를 봉인하는 것—봉인 없이는 배선도를 열어볼 수도, 수정할 수도 없다.

---

## 5. 실무 적용 및 최적화 기법

UEFI 부트킷 대응은 Secured-core PC(Windows 11 요구사항) 플랫폼처럼 하드웨어 수준에서 Boot Guard + Secure Boot + TPM을 결합하는 방향이 가장 효과적이다. Secure Boot 취약점(BlackLotus 등)에 대해서는 DBX(Secure Boot 폐기 목록) 업데이트가 신속히 이루어져야 한다.

📢 **섹션 요약 비유**: Secured-core PC는 집 기초공사부터 최종 열쇠까지 모든 단계에 공인된 계약자(서명된 코드)만 참여하게 하는 건축 인증 제도다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Secure Boot | 주요 방어 | UEFI 부트 체인 서명 검증 |
| Intel Boot Guard | 강화 방어 | CPU 수준 UEFI 서명 검증 |
| BlackLotus | 실제 사례 | 2023년 실제 UEFI 부트킷 |
| LoJax | 실제 사례 | 최초 발견 UEFI 부트킷(APT28) |
| CHIPSEC | 탐지 도구 | UEFI 펌웨어 보안 분석 도구 |

### 👶 어린이를 위한 3줄 비유 설명
- UEFI 부트킷은 집의 전기 시스템(UEFI 펌웨어) 안에 숨어 있어서, 이사를 가도(OS 재설치) 없어지지 않아.
- 아주 깊은 곳에 숨어 있어서 보안 프로그램으로는 찾기 매우 어려워.
- 막으려면 전기 시스템 설계도를 공장에서 봉인하고(Boot Guard), 변경 시 경보가 울리게(Secure Boot) 해야 해!
