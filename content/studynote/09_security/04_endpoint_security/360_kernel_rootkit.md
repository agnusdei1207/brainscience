+++
weight = 360
title = "360. 커널 루트킷 (Kernel Rootkit)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: 커널 루트킷은 ring 0 커널 공간에 악성 코드를 삽입하여 시스템 콜 테이블, 인터럽트 디스크립터 테이블(IDT), VFS(Virtual File System) 후킹으로 OS의 눈을 완전히 속이는 가장 강력한 루트킷 유형이다.
> 2. **가치**: 커널 수준에서 동작하므로 사용자 공간의 모든 보안 도구(AV, EDR)가 커널 루트킷에 의해 조작된 API를 통해 정보를 받아 탐지가 본질적으로 어렵다.
> 3. **판단 포인트**: 방어는 DKMS(Dynamic Kernel Module Support) 서명 강제, Linux `lockdown` 모드, Windows HVCI(Hypervisor-Protected Code Integrity), PatchGuard로 커널 수정 자체를 차단하는 것이 핵심이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

커널 루트킷은 악성 커널 모듈(LKM: Loadable Kernel Module) 또는 Windows 드라이버(.sys)를 통해 커널 공간에 로드된다. 로드되면 커널 내부 자료구조를 직접 조작하여: ① 시스템 콜 테이블(sys_call_table)의 함수 포인터를 후킹 함수로 교체, ② DKOM(Direct Kernel Object Manipulation)으로 프로세스/모듈 목록의 이중 연결 리스트에서 자신의 항목 제거, ③ VFS 후킹으로 특정 파일·디렉터리를 파일 시스템 함수에서 숨김.

결과적으로 `ps`, `ls`, `netstat`, AV 소프트웨어 등 모든 도구가 커널을 통해 정보를 얻으므로, 루트킷이 후킹한 결과값을 받아 실제 악성 활동을 볼 수 없게 된다.

📢 **섹션 요약 비유**: 커널 루트킷은 건물의 CCTV 제어 시스템(커널)을 장악해 카메라 화면을 가짜로 바꾸는 것—경비원(보안 소프트웨어)이 가짜 화면을 진짜로 믿는다.

---

## 2. 구성요소

### 커널 루트킷 후킹 기법

| 기법 | 대상 | 은닉 효과 |
|:---|:---|:---|
| Syscall Table Hooking | sys_call_table 포인터 | getdents64, kill, socket 결과 조작 |
| DKOM | task_struct.list | ps/top에서 프로세스 숨김 |
| IDT Hooking | 인터럽트 핸들러 | 시스템 이벤트 인터셉트 |
| VFS Hooking | file_operations 포인터 | ls/find에서 파일 숨김 |
| Inline Hooking | 함수 첫 바이트 교체 | 특정 함수 전면 탈취 |

```
┌──────────────────────────────────────────────────────┐
│         커널 루트킷 시스템 콜 후킹 구조               │
├──────────────────────────────────────────────────────┤
│  사용자 공간: ps 명령 → getdents64() 호출            │
│                  ↓                                  │
│  커널 공간: sys_call_table[__NR_getdents64]          │
│            = 루트킷_후킹_함수  ← 교체됨              │
│                  ↓                                  │
│  루트킷: 원본 함수 호출 → 결과에서 악성 파일 제거    │
│         → 가공된 결과 반환                          │
└──────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: syscall 테이블 후킹은 회사의 전화 교환원(커널)을 매수해—모든 외부 전화를 교환원이 먼저 받고 원하는 내용으로 편집 후 전달하는 것이다.

---

## 3. 구조 및 동작 원리

| 루트킷 유형 | 동작 계층 | 탐지 난이도 | 방어 기법 |
|:---|:---|:---|:---|
| 사용자 모드 | ring 3 | 중간 | LD_PRELOAD 검사, libc 무결성 |
| 커널 루트킷 | ring 0 | 높음 | lockdown, PatchGuard, HVCI |
| 하이퍼바이저 | ring -1 | 매우 높음 | TPM, Measured Boot |

📢 **섹션 요약 비유**: 커널 루트킷은 경찰서(OS) 내부에 위장 요원을 심어두는 것—경찰이 요원을 잡으려 해도 내부 정보 시스템이 이미 조작되어 있다.

---

## 4. 비교 및 트레이드오프

Linux 커널 루트킷 방어: ① `CONFIG_MODULE_SIG_FORCE`로 서명된 모듈만 로드, ② `lockdown=integrity` 모드로 `/dev/mem`, `/proc/kcore` 등 커널 메모리 직접 접근 차단, ③ LKRG(Linux Kernel Runtime Guard)로 syscall 테이블·DKOM 실시간 감지. Windows: PatchGuard(KPP)로 커널 패치 탐지, HVCI로 서명 없는 드라이버 로드 차단.

메모리 포렌식으로 커널 루트킷 탐지: Volatility의 `check_syscall`, `linux_check_modules`, `psxview` 플러그인이 실시간 커널 자료구조와 포렌식 스캔 결과를 교차 비교한다.

📢 **섹션 요약 비유**: LKRG는 경찰서 내부에 CCTV를 독립적으로 설치해—교환원(커널)이 조작해도 별도 채널로 실제 상황을 기록한다.

---

## 5. 실무 적용 및 최적화 기법

HVCI와 Secure Boot의 보편화는 커널 루트킷 로드 자체를 어렵게 만들고 있다. 장기적으로 Rust for Linux를 통한 메모리 안전 커널 코드와, eBPF 검증기의 강화는 커널 루트킷이 악용하는 취약점의 수를 줄이는 근본 방향이다.

📢 **섹션 요약 비유**: 서명 없는 코드의 커널 진입을 막는 HVCI는 경찰서 출입에 신원 조회(디지털 서명)를 의무화하는 것—신원 불명자는 처음부터 들어올 수 없다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DKOM (Direct Kernel Object Manipulation) | 핵심 기법 | 커널 자료구조 직접 조작 |
| PatchGuard (KPP) | 방어 기술 | Windows 커널 패치 탐지 |
| HVCI | 방어 기술 | 하이퍼바이저 코드 무결성 보호 |
| LKRG | 탐지 도구 | Linux 커널 런타임 무결성 감시 |
| Volatility | 포렌식 도구 | 메모리 포렌식 루트킷 탐지 |

### 👶 어린이를 위한 3줄 비유 설명
- 커널 루트킷은 컴퓨터의 교환원(커널)을 매수해서 모든 정보 보고를 조작하는 거야.
- 보안 프로그램이 "악성코드 있어?"라고 물어봐도, 매수된 교환원이 "없어요!"라고 거짓말해.
- 막으려면 교환원 자리에 공식 신분증(서명된 모듈)이 있는 사람만 앉힐 수 있게(lockdown/HVCI) 해야 해!
