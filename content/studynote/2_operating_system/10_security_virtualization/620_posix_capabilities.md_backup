+++
title = "620. POSIX Capabilities (포식스 캐파빌리티)"
weight = 620
+++

# POSIX Capabilities

## 핵심 인사이트

**POSIX Capabilities는 루트의 모든 권한을 개별 기능 단위로 분리하여, 프로세스에 필요한 최소한의 권한만 부여하는 리눅스 커널 메커니즘이다.** 전통적으로 **setuid root 프로그램**은 모든 루트 권한을 가졌지만, Capabilities를 사용하면 `CAP_NET_RAW`(ICMP 소켓), `CAP_NET_BIND_SERVICE`(1024 이하 포트 바인드) 등 세분화된 권한만 부여할 수 있어 **보안을 크게 향상**시킨다.

---

## Ⅰ. 개요 및 필요성

### 1. 루트 권한의 문제점

```
┌─────────────────────────────────────────────────────────────┐
│              setuid root의 보안 문제                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  전통적 setuid root 프로그램:                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ping (setuid root)                                 │   │
│  │  ├── CAP_NET_RAW  ✓ (필요)                          │   │
│  │  ├── CAP_NET_BIND_SERVICE  ? (불필요)               │   │
│  │  ├── CAP_DAC_OVERRIDE  ? (불필요)                   │   │
│  │  ├── CAP_SYS_ADMIN  ? (위험!)                       │   │
│  │  └── ... (모든 루트 권한)                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  문제: ping 프로그램이 해킹당하면                            │
│        → 공격자는 **모든 루트 권한** 획득!                  │
│                                                             │
│  해결: Capabilities로 **필요한 권한만** 부여                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ping (CAP_NET_RAW만 부여)                           │   │
│  │  ├── CAP_NET_RAW  ✓ (필요)                          │   │
│  │  └── 그 외 ✗ (차단)                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 정의

| 개념 | 설명 |
|:---|:---|
| **Capability** | 루트 권한을 개별 기능으로 분리한 것 |
| **목적** | **최소 권한의 원칙**(Principle of Least Privilege) 실현 |
| **LSM과의 관계** | AppArmor/SELinux와 함께 MAC 계층 형성 |

---

## Ⅱ. 주요 Capabilities

### 1. Capability 목록 (부분)

```
┌─────────────────────────────────────────────────────────────┐
│                주요 POSIX Capabilities                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Capability              │ 값 │ 설명                 │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ CAP_CHOWN              │ 0  │ 파일 소유자 변경       │  │
│  │ CAP_DAC_OVERRIDE        │ 1  │ 파일 접근 권한 무시   │  │
│  │ CAP_DAC_READ_SEARCH     │ 2  │ 읽기/검색 권한 무시   │  │
│  │ CAP_FOWNER              │ 3  │ 소유자 아닌 파일 조작  │  │
│  │ CAP_FSETID              │ 4  │ setuid/setgid 비트 설정│  │
│  │ CAP_KILL                │ 5  │ 모든 프로세스 시그널   │  │
│  │ CAP_SETGID              │ 6  │ GID 변경               │  │
│  │ CAP_SETUID              │ 7  │ UID 변경               │  │
│  │ CAP_SETPCAP             │ 8  │Capability 조작 권한    │  │
│  │ CAP_LINUX_IMMUTABLE     │ 9  │ immutable 파일 속성    │  │
│  │ CAP_NET_BIND_SERVICE    │ 10 │ 1024 이하 포트 바인드  │  │
│  │ CAP_NET_BROADCAST       │ 11 │ 브로드캐스트 소켓      │  │
│  │ CAP_NET_ADMIN           │ 12 │ 네트워크 관리          │  │
│  │ CAP_NET_RAW             │ 13 │ RAW 소켓 생성          │  │
│  │ CAP_IPC_LOCK            │ 14 │ 메모리 잠금(mlock)     │  │
│  │ CAP_IPC_OWNER           │ 15 │ IPC 객체 조작          │  │
│  │ CAP_SYS_MODULE          │ 16 │ 커널 모듈 로드         │  │
│  │ CAP_SYS_RAWIO           │ 17 │ raw I/O 접근           │  │
│  │ CAP_SYS_CHROOT          │ 18 │ chroot 실행            │  │
│  │ CAP_SYS_PTRACE          │ 19 │ 모든 프로세스 디버깅   │  │
│  │ CAP_SYS_PACCT           │ 20 │ 프로세스 회계          │  │
│  │ CAP_SYS_ADMIN           │ 21 │ **가장 강력한** 권한   │  │
│  │ CAP_SYS_BOOT            │ 22 │ 시스템 재부팅          │  │
│  │ CAP_SYS_NICE            │ 23 │ 우선순위/스케줄링 조정  │  │
│  │ CAP_SYS_RESOURCE        │ 24 │ 자원 제한 설정         │  │
│  │ CAP_SYS_TIME            │ 25 │ 시스템 시간 설정       │  │
│  │ CAP_SYS_TTY_CONFIG      │ 26 │ 터미널 장치 설정       │  │
│  │ CAP_MKNOD               │ 27 │ 특수 파일 생성         │  │
│  │ CAP_LEASE               │ 28 │ 파일 임대 설정         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 자주 사용되는 Capabilities

| Capability | 사용처 | 예시 |
|:---|:---|:---|
| `CAP_NET_RAW` | RAW 소켓 | ping, traceroute |
| `CAP_NET_BIND_SERVICE` | 잘 알려진 포트(<1024) | 웹 서버(80), DNS(53) |
| `CAP_SETUID`/`CAP_SETGID` | ID 변경 | sudo, passwd |
| `CAP_CHOWN` | 파일 소유자 변경 | chown 명령 |
| `CAP_DAC_OVERRIDE` | 파일 권한 무시 | 백업 도구 |
| `CAP_SYS_ADMIN` | **시스템 관리** | mount, iptables (주의 필요!) |

---

## Ⅲ. Capability 집합 (Sets)

### 1. 5가지 Capability 집합

```
┌─────────────────────────────────────────────────────────────┐
│            프로세스의 5가지 Capability 집합                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1) Permitted (P)       : 가질 수 있는 최대 Capability    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Effective ⊆ Permitted ⊆ Bounding                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  2) Inheritable (I)      : execve 후 자식에게 상속       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 자식 프로세스가 물려받을 Capability (거의 사용 안 함) │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  3) Effective (E)        : ★실제 권한 검사에 사용★      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 커널이 권한을 확인할 때 참조하는 집합                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  4) Bounding (B)         : execve 후 유지 가능 최대치    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ drop 불가, 제거되면 영구적                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  5) Ambient (A)          : 2017 추가, execve 후 유지    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Inheritable과 유사하지만 더 유연함                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 집합 간 관계

```
┌─────────────────────────────────────────────────────────────┐
│           Capability 집합의 관계와 변환                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   P (Permitted)                                            │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                                                     │  │
│   │   E (Effective)    I (Inheritable)  A (Ambient)    │  │
│   │   ┌───────┐        ┌───────┐        ┌───────┐      │  │
│   │   │ CAP_  │        │ CAP_  │        │ CAP_  │      │  │
│   │   │ NET_  │        │ SET_  │        │ NET_  │      │  │
│   │   │ RAW   │        │ UID   │        │ RAW   │      │  │
│   │   └───────┘        └───────┘        └───────┘      │  │
│   │      │                │                │           │  │
│   │      └────────────────┴────────────────┘           │  │
│   │                      │                             │  │
│   │                      ▼                             │  │
│   │              B (Bounding)                          │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   execve() 전후 변환:                                       │
│   ┌───────────────────────┐     ┌───────────────────────┐ │
│   │   execve() 전        │ ─▶  │   execve() 후        │ │
│   ├───────────────────────┤     ├───────────────────────┤ │
│   │ P' = P ∩ file.P      │     │ P'' = P'             │ │
│   │ I' = I ∩ file.I      │     │ I'' = file.I         │ │
│   │ E' = file.E 비트?P'  │     │ E'' = file.E?P''     │ │
│   │ B' = B ∩ file.B      │     │ B'' = file.B         │ │
│   │ A' = A ∩ file.A      │     │ A'' = A' ∪ file.A    │ │
│   └───────────────────────┘     └───────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. Capabilities 사용

### 1. 파일에 Capability 부여

```bash
# ping의 setuid root 제거하고 CAP_NET_RAW만 부여
$ sudo setcap cap_net_raw+ep /bin/ping

# 확인
$ getcap /bin/ping
/bin/ping = cap_net_raw+ep

# +ep 설명
# +e: Effective 집합에 추가 (실제 권한)
# +p: Permitted 집합에 추가 (가질 수 있음)
# +i: Inheritable 집합에 추가 (상속)
# +a: Ambient 집합에 추가

# setuid root 제거
$ sudo chmod u-s /bin/ping

# 이제 ping은 루트 권한 없이 CAP_NET_RAW만 사용
```

### 2. 프로세스 Capabilities 확인

```bash
# 현재 쉘의 capabilities
$ capsh --print
Current: = cap_chown,cap_dac_override,...
        (1) 0x0000000000000000 (bounding)
        (1) 0x0000000000000000 (ambient)
...

# 특정 프로세스 확인
$ sudo cat /proc/1234/status | grep Cap
CapInh: 0000000000000000
CapPrm: 0000000000000000
CapEff: 0000000000000000
CapBnd: 0000003fffffffff
CapAmb: 0000000000000000

# 16진수를 Capability 이름으로 변환
$ capsh --decode=0000003fffffffff
0x0000003fffffffff=cap_chown,cap_dac_override,...
```

### 3. 프로그래밍에서의 Capabilities

```c
#include <sys/capability.h>
#include <unistd.h>

// 현재 프로세스의 CAP_NET_RAW 제거
void drop_unneeded_caps() {
    cap_t caps = cap_get_proc();
    cap_value_t cap_list[] = { CAP_NET_RAW };

    // Permitted 집합에서 제거
    cap_set_flag(caps, CAP_PERMITTED, 1, cap_list, CAP_CLEAR);

    // Effective 집합에서 제거
    cap_set_flag(caps, CAP_EFFECTIVE, 1, cap_list, CAP_CLEAR);

    cap_set_proc(caps);
    cap_free(caps);
}

// 루트 권한 완전 포기
void drop_root() {
    if (setuid(getuid()) == -1)
        perror("setuid");
    if (setgid(getgid()) == -1)
        perror("setgid");
}

// Capabilities 확인
void check_caps() {
    cap_t caps = cap_get_proc();
    char *caps_text = cap_to_text(caps, NULL);
    printf("Capabilities: %s\n", caps_text);
    cap_free(caps_text);
    cap_free(caps);
}
```

### 4. Docker 컨테이너에서의 Capabilities

```bash
# 컨테이너의 기본 Capabilities 확인
$ docker run --rm alpine capsh --print
Current: = cap_chown,cap_dac_override,...  (많은 권한)

# 모든 Capabilities 제거 (안전한 컨테이너)
$ docker run --rm --cap-drop=all alpine capsh --print
Current: = (없음)

# 특정 Capability만 추가
$ docker run --rm \
    --cap-drop=all \
    --cap-add=CAP_NET_BIND_SERVICE \
    nginx

# 권장 제거 Capabilities (보안)
$ docker run --rm \
    --cap-drop=CAP_SYS_ADMIN \
    --cap-drop=CAP_NET_RAW \
    --cap-drop=CAP_SYS_PTRACE \
    myapp
```

---

## Ⅴ. 모범 사례 및 보안

### 1. Capability 관리 원칙

| 원칙 | 설명 |
|:---|:---|
| **최소 권한** | 필요한 Capability만 부여 |
| **Capability Drop** | 시작 후 불필요한 것 즉시 제거 |
| **Bounding Set 제한** | 자식 프로세스가 상속받을 최대치 제한 |
| **Effective 비트** | Permitted만 있고 Effective가 없으면 권한 없음 |

### 2. setuid root → Capabilities 마이그레이션

```bash
# 이전 (위험)
$ ls -l /usr/bin/traceroute
-rwsr-xr-x 1 root root ... /usr/bin/traceroute

# 이후 (안전)
$ sudo chmod u-s /usr/bin/traceroute
$ sudo setcap cap_net_raw+ep /usr/bin/traceroute
$ ls -l /usr/bin/traceroute
-rwxr-xr-x 1 root root ... /usr/bin/traceroute
$ getcap /usr/bin/traceroute
/usr/bin/traceroute = cap_net_raw+ep
```

### 3. 보안 강화 팁

```bash
# 1) 일반 사용자는 Capabilities 없음 확인
$ capsh --print | grep Current
Current: = (없어야 함)

# 2) Bounding Set 축소 (부팅 스크립트)
# /etc/sysctl.conf
kernel.capability-boundset=0x7fffffffff  # 필요한 것만

# 3) CAP_SYS_ADMIN 절대 부여 금지 (대안 확인)
# CAP_SYS_ADMIN은 너무 강력함
# 대신 CAP_NET_ADMIN, CAP_SYS_MODULE 등 구체적 권한 사용

# 4) 파일 시스템별 제한
# /etc/fstab
/home ext4 defaults,nosuid  # setuid 방지
/tmp  ext4 defaults,nodev,noexec  # 장치 파일 실행 방지
```

---

## Ⅵ. Capabilities vs 루트

### 1. 권한 검사 비교

```
┌─────────────────────────────────────────────────────────────┐
│             커널 권한 검사 흐름                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  int capable(int cap)  // kernel/capability.c              │
│  {                                                         │
│      if (uid == 0)                 // 전통적 검사         │
│          return 1;  // 루트는 무조건 허용                   │
│                                                           │
│      if (cap_valid(cap) && cap_raised(current->cap_e, cap))│
│          return 1;  // ★ Capability에 있으면 허용         │
│                                                           │
│      return 0;  // 거부                                    │
│  }                                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 개념 맵

```
                     ┌───────────────────────┐
                     │   POSIX Capabilities  │
                     │   (분할된 루트 권한)   │
                     └───────────┬───────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   ┌────▼────┐           ┌───────▼───────┐         ┌─────▼─────┐
   │  문제    │           │  5가지 집합    │         │   사용법   │
   │  setuid  │           ├───────────────┤         ├───────────┤
   │  root    │           │ Permitted (P) │         │ setcap     │
   │          │           │ Inheritable(I)│         │ getcap     │
   │ 모든     │           │ Effective (E) │         │ capsh      │
   │ 권한 부여│           │ Bounding (B)  │         │            │
   │ 위험!    │           │ Ambient (A)   │         │ Docker     │
   └─────────┘           └───────────────┘         │ --cap-add  │
        │                        │                └───────────┘
        └────────────────────────┴────────────────────────┘
                                    │
                       ┌────────────┴────────────┐
                       ▼                         ▼
                 ┌─────────────┐          ┌─────────────┐
                 │ 최소 권한   │          │  보안 강화  │
                 │ 원칙 실현   │          │             │
                 └─────────────┘          │ Bounding    │
                                         │ 축소        │
                                         │ CAP_SYS_    │
                                         │ ADMIN 제거  │
                                         └─────────────┘
```

---

## 어린이를 위한 비유

**Capabilities는 "면허증"**과 같습니다.

옛날에는 **면허증 하나**(루트 권한)만 있으면:
- 운전도 하고 ✓
- 비행기도 조종하고 ✓
- 의사도 되고 ✓
- 변호사도 되고 ✓ (위험!)

지금은 각각의 **면허증**이 따로 있습니다:
- **CAP_NET_RAW**: "네트워크 핑 면허" (ping만 가능)
- **CAP_NET_BIND_SERVICE**: "80번 포트 사용 면허" (웹 서버만)
- **CAP_SYS_ADMIN**: "시스템 관리자 면허" (정말 위험한 것들)

ping 프로그램이 **CAP_NET_RAW 면허**만 가지고 있다면:
- 핑은 보낼 수 있어 ✓
- 비밀번호 파일은 못 열어 ✗
- 시스템은 못 고쳐 ✗

이제 ping이 해커에게 잡혀도 **다른 나쁜 짓**을 할 수 없습니다!

**Bounding Set**은 "내가 줄 수 있는 면허의 한계"고, **Effective**는 "지금 유효한 면허"입니다.
