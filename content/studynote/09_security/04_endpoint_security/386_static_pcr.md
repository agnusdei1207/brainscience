+++
weight = 386
title = "386. Static PCR — 부팅 무결성 측정"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Static PCR (Platform Configuration Register)은 컴퓨터 전원 투입 시점부터 OS 부팅 완료까지의 정적 부팅 과정을 측정한 값들을 TPM PCR 0-7에 저장하며, CRTM (Core Root of Trust for Measurement)에서 시작하는 신뢰 체인을 형성한다.
> 2. **가치**: "정적"이라 함은 시스템이 시작될 때 한 번 측정되고 이후 변경되지 않는 부팅 코드 영역을 의미하며, UEFI 펌웨어·Secure Boot 상태·부트로더의 무결성 기준값이 된다.
> 3. **판단 포인트**: PCR 0-7은 UEFI/BIOS가 측정하는 정적 영역이고 PCR 8-15는 OS/부트로더가 측정하는 동적 영역이며, BitLocker 봉인 시 어떤 PCR을 사용하는지 이해하는 것이 핵심이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

TCG (Trusted Computing Group) 플랫폼 사양에서 PCR (Platform Configuration Register)은 TPM 내부의 176비트(SHA-256 기준) 레지스터로, 부팅 과정 각 단계의 해시를 누적 기록한다. 전원 투입 시 PCR은 모두 0으로 초기화되고, CRTM (Core Root of Trust for Measurement)—일반적으로 UEFI 펌웨어—이 측정의 첫 번째 신뢰 앵커가 된다.

"정적(Static) PCR"은 S-CRTM (Static Core Root of Trust for Measurement) 기반 측정을 의미하며, 전통적인 시스템 부팅 시 UEFI 펌웨어가 주도하는 측정 과정이다. 이에 대비되는 개념이 "동적(Dynamic) PCR"으로, Intel TXT·AMD SKINIT 등이 제공하는 late launch 기반 동적 측정 메커니즘이다.

📢 **섹션 요약 비유**: Static PCR은 건물 입구에서 처음 찍는 출석부—처음부터 끝까지 순서대로 기록되며, 나중에 수정할 수 없다.

---

## 2. 구성요소

| PCR 번호 | 측정 주체 | 측정 내용 |
|:---|:---|:---|
| PCR 0 | UEFI 펌웨어 | UEFI 코어 펌웨어 코드 |
| PCR 1 | UEFI 펌웨어 | UEFI 펌웨어 설정 데이터 |
| PCR 2 | UEFI 펌웨어 | 옵션 ROM (확장 카드 펌웨어) |
| PCR 3 | UEFI 펌웨어 | 옵션 ROM 설정 데이터 |
| PCR 4 | UEFI 펌웨어 | MBR 또는 UEFI 부트 애플리케이션 |
| PCR 5 | UEFI 펌웨어 | GPT 파티션 테이블 |
| PCR 6 | UEFI 펌웨어 | 플랫폼 이벤트 |
| PCR 7 | UEFI 펌웨어 | Secure Boot 상태 (db, dbx, PK) |
| PCR 8-15 | OS/부트로더 | OS 정의 측정 (GRUB 커맨드라인, Linux IMA 등) |
| PCR 23 | 가상화 전용 | 하이퍼바이저 측정 |

```text
┌──────────────────────────────────────────────────────┐
│             Static PCR 측정 흐름                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  [전원 ON → PCR 0~23 모두 0 초기화]                  │
│                                                      │
│  S-CRTM (UEFI 펌웨어 시작)                           │
│  1. Hash(UEFI_core)  → PCR0.Extend                  │
│  2. Hash(UEFI_config) → PCR1.Extend                 │
│  3. Hash(Option_ROMs) → PCR2.Extend                 │
│  4. Hash(Boot_App)   → PCR4.Extend                  │
│  5. Hash(GPT)        → PCR5.Extend                  │
│  6. Hash(SecureBoot) → PCR7.Extend                  │
│                                                      │
│  [GRUB 부트로더 (OS 인계)]                           │
│  7. Hash(grub.cfg)   → PCR8.Extend  (OS 정의)       │
│  8. Hash(kernel)     → PCR9.Extend  (OS 정의)       │
│                                                      │
│  [최종 PCR 값 = 전체 부팅 경로의 암호학적 지문]      │
└──────────────────────────────────────────────────────┘
```

**PCR 7의 특별한 역할**: Secure Boot 상태(활성화 여부, db/dbx 내용)를 기록하므로, Secure Boot가 비활성화되면 PCR 7 값이 달라진다. BitLocker는 PCR 7을 봉인 조건에 포함시켜 Secure Boot 비활성화 시 드라이브 잠금이 걸리도록 한다.

📢 **섹션 요약 비유**: PCR 7은 경비원의 마지막 확인 도장—경비 시스템(Secure Boot)이 꺼진 채로 부팅하면 금고(BitLocker)가 열리지 않는다.

---

## 3. 구조 및 동작 원리

| 항목 | Static PCR (PCR 0-7) | Dynamic PCR (PCR 17-22) |
|:---|:---|:---|
| 측정 시작 | 전원 ON, S-CRTM | Late Launch (Intel TXT/SKINIT) |
| 신뢰 앵커 | UEFI 펌웨어 | DRTM (Dynamic RoT) |
| 부팅 단계 | 정적 부팅 경로 전체 | 특정 애플리케이션 런타임 |
| 취약점 | UEFI 펌웨어 자체 변조 | Late Launch 직전까지 실행된 악성 코드 |

📢 **섹션 요약 비유**: Static PCR은 아침에 집을 나설 때 찍는 사진, Dynamic PCR은 중요한 회의실 들어갈 때 다시 확인하는 출입증이다.

---

## 4. 비교 및 트레이드오프

**BitLocker PCR 봉인 프로파일**  
- 기본값(레거시): PCR 0, 2, 4, 11  
- 권장값(UEFI + Secure Boot): PCR 0, 2, 4, 7, 11  
- PCR 7 포함 시: Secure Boot 비활성화·db 변경 → BitLocker 복구 키 요구  

**PCR 값 조회 및 검증**  
```bash
# Linux
tpm2_pcrread sha256:0,1,2,4,7

# Windows PowerShell
Get-TpmSupportedFeature
Get-TpmEndorsementKeyInfo
```

**IMA (Integrity Measurement Architecture)**: Linux에서 PCR 10에 실행 파일·라이브러리·스크립트의 해시를 동적으로 기록—런타임 무결성 검증.

📢 **섹션 요약 비유**: PCR 봉인 프로파일 설정은 "이 조건들이 모두 맞아야만 열쇠가 작동한다"는 다중 조건 자물쇠—조건이 많을수록 보안이 강하지만 관리가 복잡해진다.

---

## 5. 실무 적용 및 최적화 기법

Static PCR은 부팅 무결성 검증의 기반 인프라로, BitLocker·원격 증명·제로트러스트 디바이스 컴플라이언스의 핵심 구성 요소다. PCR 값의 예측 가능성과 재현 가능성을 확보하는 것이 실무에서 중요하며, 하드웨어 교체·BIOS 업데이트·드라이버 변경 시 예상 PCR 변화를 미리 계획해야 한다.

📢 **섹션 요약 비유**: PCR은 시스템의 DNA 프로파일—같은 환경이면 항상 같은 DNA가 나와야 한다. 달라지면 뭔가 바뀐 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| TPM | PCR 저장소 | 변조 불가능한 하드웨어 보안 칩 |
| CRTM | 신뢰 앵커 | 측정의 첫 번째 신뢰 루트 |
| Measured Boot | 상위 개념 | Static PCR을 활용한 부팅 무결성 체계 |
| BitLocker 봉인 | 응용 사례 | PCR 값에 암호화 키 묶기 |
| PCR 7 | Secure Boot 연동 | Secure Boot 상태 반영 레지스터 |

### 👶 어린이를 위한 3줄 비유 설명
Static PCR은 컴퓨터가 켜질 때 각 단계마다 "무엇이 실행됐는지" 도장을 차례로 찍어 저장하는 거예요.  
도장이 하나라도 달라지면 컴퓨터가 "뭔가 바뀌었어!"라고 알고 파일 암호(BitLocker)를 잠가요.  
TPM이라는 특별한 칩이 이 도장들을 안전하게 보관해서 아무도 위조할 수 없어요.
