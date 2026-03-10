+++
title = "619. AppArmor (Application Armor)"
weight = 619
+++

# AppArmor

## 핵심 인사이트

**AppArmor는 리눅스 커널의 MAC(Mandatory Access Control) 시스템으로, SELinux와 달리 **경로(Path) 기반**으로 접근을 제어한다.** 프로그램별로 **프로필(Profile)**을 작성하여 파일 접근, 네트워크 사용, 능력(Capability) 등을 제한하며, 프로필 작성이 상대적으로 쉽고 학습 곡선이 낮아 데비안, 우분투, SUSE 계열에서 기본으로 사용된다.

---

## Ⅰ. 개요 및 특징

### 1. SELinux vs AppArmor

| 특징 | SELinux | AppArmor |
|:---|:---|:---|
| **라벨링 방식** | **라벨 기반** (파일시스템 확장 속성) | **경로 기반** |
| **구성** | 복잡한 TE 언어, 정책 컴파일 필요 | 간단한 프로필 스크립트 |
| **학습 곡선** | 높음 | 낮음 |
| **주요 배포판** | RHEL, CentOS, Fedora | Debian, Ubuntu, openSUSE |
| **동적 로딩** | 어려움 (정책 재컴파일) | 쉬움 (프로필 리로드) |
| **파일시스템** | XFS, Ext4 등 지원 | 모든 파일시스템 |

### 2. 동작 원리

```
┌─────────────────────────────────────────────────────────────┐
│              AppArmor 경로 기반 접근 제어                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SELinux:                     AppArmor:                     │
│  ┌─────────────┐              ┌─────────────┐              │
│  │ Label       │              │ Path        │              │
│  │ shadow_t    │              │ /etc/shadow │              │
│  └─────────────┘              └─────────────┘              │
│       │                             │                      │
│       ▼                             ▼                      │
│  파일시스템 xattr로       실제 파일 경로로                   │
│  라벨 부여 필요          직접 접근 제어                     │
│  (복잡함)              (간단함)                            │
│                                                             │
│  예: 파일 이동 시            예: 파일 이동 시                │
│      라벨 유지/복원               경로만 확인                │
│      필요 없음                   (자동 추적)                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 프로필 구조

### 1. 프로필 기본 형식

```
┌─────────────────────────────────────────────────────────────┐
│              AppArmor 프로필 구조                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  #include <tunables/global>                                 │
│                                                             │
│  profile executable_path flags {                           │
│      # capability                                          │
│      capability dac_override,                              │
│                                                             │
│      # network access                                      │
│      network inet stream,                                  │
│                                                             │
│      # file access                                         │
│      /path/to/file rw,                                     │
│      /path/to/dir/** r,                                    │
│      /etc/** r,                                            │
│                                                             │
│      # deny rules (우선순위 높음)                          │
│      deny /secret/** w,                                    │
│                                                             │
│      # owner match (파일 소유자 일치 시)                    │
│      owner /home/** rw,                                    │
│  }                                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 실제 프로필 예시

```apparmor
# /etc/apparmor.d/usr.sbin.nginx

#include <tunables/global>

profile nginx /usr/sbinnginx {
  # 네트워크 권한
  network inet stream,
  network inet6 stream,

  # 파일 접근
  /etc/nginx/** r,
  /var/log/nginx/* w,
  /var/www/html/** r,
  /run/nginx.pid w,
  /var/lib/nginx/** rw,

  # 캐파빌리티
  capability setuid,
  capability setgid,
  capability net_bind_service,

  # 거부 규칙
  deny /root/** w,
  deny /etc/shadow rw,

  # 소켓
  unix stream listen,
}
```

### 3. 권한 표기법

| 표기 | 의미 | 설명 |
|:---|:---|:---|
| `r` | read | 읽기 |
| `w` | write | 쓰기 (삭제 포함) |
| `a` | append | 추가 (삭제 불가) |
| `k` | lock | 파일 잠금 |
| `rw` | read+write | 읽기+쓰기 |
| `/**` | 와일드카드 | 하위 모든 경로 |
| `owner` | 소유자 매칭 | 파일 소유자가 프로세스 소유자와 같을 때만 |

---

## Ⅲ. AppArmor 모드 및 관리

### 1. 프로필 모드

```
┌─────────────────────────────────────────────────────────────┐
│                AppArmor 프로필 모드                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐│
│  │  Enforce    │      │  Complain   │      │ Unconfined  ││
│  │  (강제)     │      │  (관찰)     │      │  (제한없음) ││
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘│
│         │                    │                    │        │
│         ▼                    ▼                    ▼        │
│  프로필 위반 시      프로필 위반 시      AppArmor 제어      │
│  접근 거부 (실제동작)  로그만 기록      받지 않음           │
│  (기본값)          (학습 모드)                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 주요 명령어

```bash
# AppArmor 상태 확인
$ sudo aa-status
apparmor module is loaded.
25 profiles are loaded.
13 profiles are in enforce mode.
   /usr/bin/ping
   /usr/sbin/nginx
12 profiles are in complain mode.
   /usr/bin/man
0 profiles are in kill mode.
0 processes are unconfined but have a profile defined.

# 프로필 모드 변경
$ sudo aa-complain /usr/sbin/nginx   # Complain 모드
$ sudo aa-enforce /usr/sbin/nginx    # Enforce 모드
$ sudo aa-disable /usr/sbin/nginx    # 비활성화

# 프로필 리로드
$ sudo apparmor_parser -r /etc/apparmor.d/usr.sbin.nginx

# 프로필 문법 검증
$ sudo apparmor_parser -Q /etc/apparmor.d/usr.sbin.nginx
```

### 3. 로그 확인

```bash
# syslog 확인
$ sudo grep apparmor /var/log/syslog
audit: type=1400 audit(1699000000.000): apparmor="DENIED" \
  operation="open" profile="/usr/sbin/nginx" name="/etc/shadow" \
  pid=1234 comm="nginx" requested_mask="r" denied_mask="r" \
  fsuid=33 ouid=0

# 해석: nginx 프로필이 /etc/shadow 읽기를 거부함
```

---

## Ⅳ. 프로필 생성 워크플로우

### 1. 자동 프로필 생성 (aa-genprof)

```
┌─────────────────────────────────────────────────────────────┐
│           aa-genprof으로 프로필 자동 생성                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1) Complain 모드로 시작                                    │
│     $ sudo aa-genprof /usr/bin/myapp                       │
│                                                             │
│  2) 애플리케이션 사용                                       │
│     $ myapp --do-something                                 │
│                                                             │
│  3) aa-genprof이 로그 스캔                                 │
│                                                             │
│     Profile:  /usr/bin/myapp                               │
│     Path:     /etc/myapp/config                            │
│     Mode:     [1] complain  [2] enforce                   │
│     Severity: [3] read     [4] write                       │
│               □  [5] other                                 │
│               > 1  ← 사용자 선택                           │
│                                                             │
│  4) 프로필 자동 생성                                        │
│     $ sudo aa-logprof                                      │
│                                                             │
│  5) Enforce 모드로 전환                                    │
│     $ sudo aa-enforce /usr/bin/myapp                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 수동 프로필 작성

```apparmor
# /etc/apparmor.d/opt.myapp

profile myapp /opt/myapp/bin/myapp {
  # 표준 라이브러리 포함
  #include <abstractions/base>
  #include <abstractions/perl>

  # 실행 파일
  /opt/myapp/bin/myapp mr,

  # 설정 파일
  /opt/myapp/etc/** r,

  # 로그
  /var/log/myapp/* w,

  # 데이터 디렉터리
  /var/lib/myapp/** rw,

  # 네트워크 (옵션)
  #include <abstractions/nameservice>
  #include <abstractions/openssl>
  network inet stream,

  # 금지된 경로
  deny /root/** rw,
  deny /home/*/.ssh/** rw,
}
```

---

## Ⅴ. 비교 및 선택

### 1. SELinux vs AppArmor 선택 기준

| 상황 | 추천 | 이유 |
|:---|:---|:---|
| RHEL/CentOS 환경 | SELinux | 배포판 기본 통합 |
| Ubuntu/Debian 환경 | AppArmor | 배포판 기본 통합 |
| 복잡한 MLS 요구 | SELinux | 다단계 보안 지원 |
| 빠른 프로필 개발 | AppArmor | 학습 곡선 낮음 |
| NFS/CIFS 사용 | SELinux | 경로 기반 약점 없음 |

### 2. 공존 가능성

```
┌─────────────────────────────────────────────────────────────┐
│            SELinux + AppArmor 공존                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  가능하지만 권장하지 않음:                                  │
│  • 두 시스템이 동일한 LSM 훅 사용                           │
│  • 상호 작용 예측 어려움                                   │
│  • 성능 저하 가능                                          │
│  • 둘 중 하나 선택 권장                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 개념 맵

```
                     ┌───────────────────────┐
                     │      AppArmor         │
                     │   (Path-based MAC)    │
                     └───────────┬───────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   ┌────▼────┐           ┌───────▼───────┐         ┌─────▼─────┐
   │  경로    │           │   Profile     │         │    모드    │
   │  기반    │           ├───────────────┤         ├───────────┤
   │  라벨링  │           │ - file path   │         │ Enforce   │
   │          │           │ - capability  │         │ Complain  │
   │  xattr   │           │ - network    │         │ Unconfined│
   │  불필요  │           │ - deny rules │         │           │
   └─────────┘           └───────────────┘         └───────────┘
        │                        │
        └────────────────────────┴────────────────────────┘
                                    │
                       ┌────────────┴────────────┐
                       ▼                         ▼
                 ┌─────────────┐          ┌─────────────┐
                 │ aa-genprof  │          │ aa-logprof  │
                 │ 자동 생성   │          │ 자동 학습   │
                 └─────────────┘          └─────────────┘
```

---

## 어린이를 위한 비유

**AppArmor는 "사용 설명서"**와 같습니다.

각 프로그램마다 **설명서(프로필)**가 붙어 있습니다:

- **nginx**: "나는 `/etc/nginx` 설정만 읽고, `/var/www/html` 웹파일만 서비스해. `/etc/shadow` 건드리지 마!"
- **ping**: "나는 네트워크로 핑만 보낼 수 있어. 파일은 못 읽어!"

이 설명서는 **파일의 위치(경로)**로 적힙니다:
- SELinux: "이 파일은 `secret_t` 라벨이야" (파일에 스티커 붙이기)
- AppArmor: "`/etc/secret` 경로는 금지야" (주소로 규제)

**Enforce 모드**는 "설명서대로만 행동해" (엄격한 선생님)
**Complain 모드**는 "설명서 어겨도 기록만 해둘게" (관대한 선생님)

프로그램이 바이러스에 감염되더라도, **프로필이라는 갇옷** 때문에 다른 파일을 건드리지 못합니다!
