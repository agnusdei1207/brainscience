+++
weight = 365
title = "365. 시큐어 부트 우회 (Secure Boot Bypass)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Secure Boot 우회는 UEFI Secure Boot 메커니즘의 구현 취약점(서명 검증 로직 버그, MOK 데이터베이스 조작, 폐기 목록 미적용)을 이용하여 서명되지 않은 부트코드를 실행하는 공격이다.
> 2. **가치**: BlackLotus(2023)는 CVE-2022-21894를 이용해 완전히 업데이트된 Windows 11에서도 Secure Boot를 우회, Secure Boot가 "완벽한 방어"가 아님을 증명했다.
> 3. **판단 포인트**: 방어는 DBX(UEFI 폐기 목록) 지속적 업데이트, UEFI 펌웨어 패치, Boot Guard로 2중 검증, shim 서명 체인 감사가 핵심이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

Secure Boot는 부팅 체인의 각 단계(UEFI → 부트로더 → 커널)에서 코드 서명을 검증하여 인가되지 않은 코드 실행을 방지한다. 그러나 이 메커니즘 자체에 구현 취약점이 있거나, 폐기된 취약한 부트로더가 여전히 서명 데이터베이스(DB)에 존재하면 우회가 가능하다.

주요 우회 기법: ① DBX(Forbidden Signature Database) 미갱신—취약한 부트로더의 해시가 폐기 목록에 없으면 여전히 부팅 허용, ② BootHole(CVE-2020-10713)—GRUB2의 설정 파일 파싱 버그로 임의 코드 실행, ③ BlackLotus(CVE-2022-21894)—Secure Boot 정책 처리 취약점으로 롤백 공격, ④ MOK(Machine Owner Key) 데이터베이스 조작—루트 권한으로 MOK에 공격자 인증서 추가.

📢 **섹션 요약 비유**: Secure Boot 우회는 출입 카드 리더기(Secure Boot) 자체의 버그를 이용해—"폐기된 카드인데 리더기가 아직 업데이트를 못 받았다"는 점을 악용하는 것이다.

---

## 2. 구성요소

### Secure Boot 서명 데이터베이스

| 데이터베이스 | 내용 | 역할 |
|:---|:---|:---|
| DB (Authorized Signature Database) | 허용된 인증서·해시 | 이것에 해당하면 부팅 허용 |
| DBX (Forbidden Signature Database) | 폐기된 인증서·해시 | 이것에 해당하면 부팅 차단 |
| KEK (Key Exchange Key) | DB/DBX 갱신 서명 키 | DB·DBX 수정 권한 |
| PK (Platform Key) | 최상위 플랫폼 키 | KEK 서명 검증 |

```
┌──────────────────────────────────────────────────────┐
│           Secure Boot 검증 흐름                       │
├──────────────────────────────────────────────────────┤
│  UEFI 펌웨어: 부트로더 서명 추출                     │
│      ↓                                              │
│  DB에 있는가? → YES → DBX에 있는가?                  │
│      │                    ↓                         │
│      NO                  YES → 부팅 차단             │
│      ↓                    ↓                         │
│   차단                   NO → 부팅 허용               │
│                                                     │
│  우회: DBX 미갱신 시 폐기된 서명도 NO로 판단→허용!    │
└──────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: DBX 미갱신은 경찰관이 범죄자 명단(폐기 목록)을 업데이트하지 않아—이미 신원 조회에서 범죄자인 사람이 통과하는 것이다.

---

## 3. 구조 및 동작 원리

| 우회 기법 | CVE | 메커니즘 | 영향 |
|:---|:---|:---|:---|
| BootHole | CVE-2020-10713 | GRUB2 파싱 버그 | Linux Secure Boot 우회 |
| BlackLotus | CVE-2022-21894 | Windows Boot Manager 롤백 | Windows Secure Boot 우회 |
| MOK 조작 | N/A(루트 필요) | mokutil로 공격자 키 등록 | Linux shim 우회 |

📢 **섹션 요약 비유**: DBX 업데이트를 누락하는 것은 보안 검색대를 통과한 후 새 폭발물 탐지 목록을 받지 않는 것—이미 알려진 위협을 탐지 못한다.

---

## 4. 비교 및 트레이드오프

Secure Boot 강화: ① DBX를 정기적으로 업데이트(UEFI 펌웨어 업데이트 포함), ② Boot Guard로 UEFI 서명 검증 추가 계층 확보, ③ MOK 데이터베이스 접근을 제한(MOK 변경 시 물리적 재부팅+PIN 입력 요구), ④ Measured Boot + Remote Attestation으로 부팅 체인 이상 감지.

기술사 답안: Secure Boot를 "필요하지만 충분하지 않은" 방어로 정의하고, Boot Guard + DBX 갱신 + Measured Boot + Remote Attestation의 4중 방어를 제시.

📢 **섹션 요약 비유**: Secure Boot 단독은 문에 잠금장치—Boot Guard+DBX 갱신+Measured Boot는 잠금+CCTV+감시원의 3중 보안이다.

---

## 5. 실무 적용 및 최적화 기법

BlackLotus 이후 Microsoft는 Windows UEFI CA 갱신 정책을 가속화하고 DBX 업데이트를 Windows Update에 포함시켰다. 장기적으로 Secure Boot 취약점 방어의 핵심은 "인증 체인 전체를 지속적으로 감사하고 갱신하는 것"이며, 단순 활성화만으로는 충분하지 않다.

📢 **섹션 요약 비유**: 자물쇠(Secure Boot)를 달았다고 끝이 아니라—자물쇠 취약점 패치(DBX 갱신)와 잠금 상태 확인(Measured Boot)을 지속해야 진짜 보안이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DBX | 핵심 요소 | 폐기된 서명 목록 |
| BlackLotus | 실제 우회 사례 | 2023년 Secure Boot 우회 UEFI 부트킷 |
| Boot Guard | 보완 방어 | CPU 수준 추가 검증 |
| Measured Boot | 보완 방어 | TPM 기반 부팅 측정 |
| MOK | 취약 요소 | Machine Owner Key 데이터베이스 |

### 👶 어린이를 위한 3줄 비유 설명
- Secure Boot는 컴퓨터가 켜질 때 공식 허가증(서명)이 있는 코드만 실행하게 하는 검사소야.
- 그런데 검사소의 블랙리스트(DBX)를 업데이트하지 않으면, 이미 나쁜 것으로 밝혀진 허가증도 통과시켜 버려.
- 막으려면 블랙리스트를 항상 최신으로 유지하고(DBX 업데이트), 검사소 자체에도 추가 경비원(Boot Guard)을 두어야 해!
