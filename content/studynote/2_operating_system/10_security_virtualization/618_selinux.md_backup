+++
title = "618. SELinux (Security-Enhanced Linux)"
weight = 618
+++

# SELinux

## 핵심 인사이트

**SELinux(Security-Enhanced Linux)는 NSA(미국 국가안보국)가 개발한 강제적 접근 제어(MAC) 구현체로, 전통적인 DAC(Discretionary Access Control)를 보완하는 커널 레벨 보안 계층이다.** 모든 프로세스와 객체(Object)에 **보안 컨텍스트(Security Context, 라벨)**를 부여하고, 이를 기반으로 **정책(Policy)**에 따른 강제적 접근 통제를 수행한다. 루트 권한을 가졌더라도 SELinux 정책을 위반하면 접근이 거부된다.

---

## Ⅰ. 개요 및 아키텍처

### 1. 정의 및 목적

| 요소 | 설명 |
|:---|:---|
| **SELinux** | 리눅스 커널에 통합된 MAC(Mandatory Access Control) 시스템 |
| **개발자** | NSA(미 국가안보국) + Red Hat 협력 |
| **목적** | 루트 계정 탈취 시에도 시스템 피해 최소화 |
| **핵심** | Type Enforcement(TE), RBAC, MLS(Multi-Level Security) |

### 2. DAC vs SELinux(MAC)

```
┌─────────────────────────────────────────────────────────────┐
│                   DAC vs SELinux 비교                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DAC (기존 리눅스)         SELinux (MAC)                    │
│  ┌─────────────────┐      ┌─────────────────┐             │
│  │ Subject → Object│      │ Subject → Object│             │
│  │                 │      │                 │             │
│  │ 소유자가 판단   │      │ 정책에 따름     │             │
│  │                 │      │                 │             │
│  │ root = ALL PASS │      │ root도 제한     │             │
│  └─────────────────┘      └─────────────────┘             │
│                                                             │
│  예: root가               예: Apache가                     │
│  /etc/shadow를           /root/에                           │
│  자유롭게 접근            접근 거부                         │
│  가능                     (정책 위반)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 보안 컨텍스트 (Security Context)

### 1. 컨텍스트 구조

```
┌─────────────────────────────────────────────────────────────┐
│          SELinux 보안 컨텍스트 구조                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  user:role:type:level[:range]                              │
│                                                             │
│  예: system_u:system_r:httpd_t:s0-s0:c0.c1023              │
│      │     │      │      │                                 │
│      │     │      │      └─ MLS 레벨 (선택)               │
│      │     │      └───────── Type (★핵심)                 │
│      │     └───────────────── Role (역할)                  │
│      └─────────────────────── User (사용자 ID)             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 컴포넌트별 설명

| 컴포넌트 | 예시 | 설명 |
|:---|:---|:---|
| **User** | system_u, unconfined_u, user_u | SELinux 사용자 식별자 (리눅스 사용자와 별개) |
| **Role** | system_r, object_r, staff_r | 역할 기반 접근 제어(RBAC) |
| **Type** | httpd_t, etc_t, shadow_t | **Type Enforcement의 핵심**, 도메인/타입 |
| **Level** | s0, s0-s1, s0:c0.c1023 | MLS(Multi-Level Security) 레벨 |

### 3. 실제 예시

```bash
$ ls -Z /etc/shadow
system_u:object_r:shadow_t:s0    /etc/shadow

$ ps -Z | grep httpd
system_u:system_r:httpd_t:s0     1234 ? 00:00:00 httpd

$ ls -Z /var/www/html/index.html
system_u:object_r:httpd_sys_content_t:s0 /var/www/html/index.html

# 의미
# httpd_t 도메인의 프로세스는
# httpd_sys_content_t 타입의 파일만 읽을 수 있다!
```

---

## Ⅲ. Type Enforcement (TE)

### 1. 도메인과 타입

```
┌─────────────────────────────────────────────────────────────┐
│                Type Enforcement 동작 원리                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Subject (프로세스)              Object (파일/디렉터리)      │
│   ┌───────────────┐              ┌───────────────┐         │
│   │   httpd_t     │              │ httpd_sys_    │         │
│   │   (도메인)    │ ──읽기──▶   │  content_t    │         │
│   │               │              │   (타입)      │  허용    │
│   └───────────────┘              └───────────────┘         │
│         │                                                     │
│         │ 쓰기                                               │
│         ▼                                                    │
│   ┌───────────────┐                                         │
│   │  etc_t        │                                         │
│   │               │  거부                                   │
│   └───────────────┘                                         │
│                                                             │
│   ★ 정책(Policy)에 정의된 Type 간 허용 관계만 접근 가능   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 정책 언어 예시

```policy
# /etc/selinux/targeted/policy/policy.x (컴파일된 바이너리)
# 소스: httpd.te (Type Enforcement)

# httpd_t 도메인 정의
type httpd_t;
domain_type(httpd_t)

# 파일 타입 정의
type httpd_sys_content_t;
files_type(httpd_sys_content_t)

# 허용 규칙 (allow)
# allow 도메인 타입:클래스 {권한들};
allow httpd_t httpd_sys_content_t:file { read getattr open ioctl };
allow httpd_t httpd_log_t:file { write append create ioctl };

# 거부 예시 (명시적 규칙 없으면 자동 거부)
# httpd_t는 etc_t 파일에 쓰기 권한 없음
# → httpd가 /etc/passwd 수정 시도 시 거부!
```

### 3. 주요 도메인/타입

| 도메인/타입 | 용도 |
|:---|:---|
| `httpd_t` | Apache 웹 서버 프로세스 |
| `httpd_sys_content_t` | 웹 콘텐츠 파일 |
| `httpd_log_t` | 웹 서버 로그 |
| `sshd_t` | SSH 서버 |
| `user_t` | 일반 사용자 도메인 |
| `unconfined_t` | **SELinux 제한 없음** (위험!) |

---

## Ⅳ. SELinux 모드 및 관리

### 1. 동작 모드

```
┌─────────────────────────────────────────────────────────────┐
│                  SELinux 동작 모드                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐│
│  │  Enforcing  │      │ Permissive  │      │  Disabled   ││
│  │   (강제)    │      │  (관찰)     │      │  (비활성)   ││
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘│
│         │                    │                    │        │
│         ▼                    ▼                    ▼        │
│  정책 위반 시        정책 위반 시        완전 비활성화      │
│  접근 거부 (실제동작)  로그만 기록      (재부팅 필요)      │
│  (AVC Deny)         (AVC Allow)                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 모드 확인 및 변경

```bash
# 현재 모드 확인
$ getenforce
Enforcing

# 일시적 모드 변경
$ sudo setenforce 0    # Permissive로 변경
$ sudo setenforce 1    # Enforcing로 변경

# 영구적 모드 변경 (/etc/selinux/config)
$ sudo vi /etc/selinux/config
SELINUX=enforcing      # enforcing | permissive | disabled
SELINUXTYPE=targeted   # targeted | mls | minimum

# 부팅 시 일시적 비활성 (grub)
selinux=0
```

### 3. 부울(Boolean) 옵션

```bash
# 부울 목록 확인
$ getsebool -a
httpd_enable_cgi --> on
httpd_enable_homedirs --> off
httpd_read_user_content --> off

# 부울 변경 (일시적)
$ setsebool httpd_enable_cgi on

# 부울 변경 (영구적)
$ setsebool -P httpd_enable_cgi on
```

---

## Ⅴ. 문제 해결 및 디버깅

### 1. AVC(Access Vector Cache) 메시지

```
┌─────────────────────────────────────────────────────────────┐
│               AVC Deny 메시지 분석                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  $ sudo ausearch -m avc -ts recent                          │
│                                                             │
│  type=AVC msg=audit(1699000000.000:123): avc: denied { }  │
│     for pid=1234 comm="httpd" path="/var/www/html/data" │
│     scontext=system_u:system_r:httpd_t:s0                  │
│     tcontext=system_u:object_r:httpd_sys_content_t:s0      │
│     tclass=dir                                             │
│     │    │         │                                        │
│     │    │         └─ 무엇을                                      │
│     │    └───────────── 누가                                     │
│     └────────────────── 어떤 권한이 거부되었는지            │
│                                                             │
│  해석: httpd_t 프로세스가                                   │
│       httpd_sys_content_t 디렉터리에                       │
│       { } (권한 없음)                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. audit2allow 도구

```bash
# AVC 로그로부터 SELinux 정책 생성
$ sudo ausearch -c 'httpd' --raw | audit2allow -M my_httpd

# 생성된 정책 확인
$ cat my_httpd.te

module my_httpd 1.0;

require {
    type httpd_t;
    type httpd_sys_content_t;
    class dir { write add_name remove_name };
}

#============= httpd_t ==============
allow httpd_t httpd_sys_content_t:dir { write add_name remove_name };

# 정책 적용
$ sudo semodule -i my_httpd.pp
```

### 3. 컨텍스트 복원

```bash
# 잘못된 컨텍스트 수정
$ ls -Z /var/www/html/newfile
unconfined_u:object_r:user_home_t:s0 newfile

# 정상 컨텍스트로 복원
$ restorecon -v /var/www/html/newfile
restorecon reset /var/www/html/newfile context
unconfined_u:object_r:httpd_sys_content_t:s0

# 재귀적 복원
$ restorecon -R -v /var/www/html/
```

---

## Ⅵ. 활용 사례

### 1. 웹 서버 격리

```
┌─────────────────────────────────────────────────────────────┐
│              SELinux로 웹 서버 보호                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Apache (httpd_t)                                           │
│       │                                                     │
│       ├─▶ /var/www/html (httpd_sys_content_t)  ✓ 읽기 가능 │
│       │                                                     │
│       ├─▶ /var/log/httpd (httpd_log_t)          ✓ 쓰기 가능 │
│       │                                                     │
│       ├─▶ /etc/shadow (shadow_t)                ✗ 거부      │
│       │                                                     │
│       ├─▶ /root (admin_home_t)                   ✗ 거부      │
│       │                                                     │
│       └─▶ 네트워크 연결                          ✓ 허용      │
│                                                             │
│   → Apache가 해킹당하더라도                                 │
│     시스템 전체로 확산되는 것 방지!                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. MLS(Multi-Level Security)

```bash
# MLS 활성화 시
# SELINUXTYPE=mls

# 레벨 확인
$ ls -Z /secret/doc
system_u:object_r:secret_t:s2  /secret/doc

# s0 < s1 < s2 < s3 (기밀 등급)
# s0:c0.c1023 (카테고리 기반 분류)

# 낮은 레벨 프로세스는 높은 레벨 객체 읽기 불가 (No Read Up)
# 높은 레벨 프로세스는 낮은 레벨 객체 쓰기 불가 (No Write Down)
```

---

## 개념 맵

```
                     ┌───────────────────────┐
                     │       SELinux         │
                     │   (MAC in Kernel)     │
                     └───────────┬───────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   ┌────▼────┐           ┌───────▼───────┐         ┌─────▼─────┐
   │   DAC   │           │ Security     │         │   Policy  │
   │ 보완    │           │ Context      │         │           │
   │         │           ├───────────────┤         ├───────────┤
   │ root도  │           │ user:role:   │         │ Type      │
   │ 제한    │           │   type:level │         │ Enforcement│
   │         │           │               │         │           │
   │         │           │ httpd_t      │         │ TE + RBAC │
   │         │           │ etc_t        │         │ + MLS     │
   └─────────┘           └───────────────┘         └───────────┘
        │                        │                        │
        └────────────────────────┴────────────────────────┘
                                    │
                       ┌────────────┴────────────┐
                       ▼                         ▼
                 ┌─────────────┐          ┌─────────────┐
                 │  Enforcing  │          │ Permissive  │
                 │  (실제거부) │          │ (로그만)    │
                 └─────────────┘          └─────────────┘
```

---

## 어린이를 위한 비유

**SELinux는 "학교의 엄격한 규칙"**과 같습니다.

일반 리눅스(DAC)는 **선생님(루트)이 모든 것을 허용**하지만, SELinux는 **학교 규칙집**이 따로 있습니다:

- **보안 컨텍스트**: "너는 **1학년 학생**(httpd_t)이고, 이건 **1학년 교실**(httpd_sys_content_t)이야"
- **Type Enforcement**: "1학년은 **2학년 교실**에는 들어갈 수 없어"
- **Enforcing 모드**: "규칙을 어기면 **바로 제지**"
- **Permissive 모드**: "규칙을 어겨도 **기록만 하고**, 실제로는 지켜봐"

해커가 웹 서버를 장악해도:
1. 웹 서버는 **httpd_t라는 껍대기**에 갇혀 있다
2. **shadow_t(비밀번호 파일)** 같은 중요한 건 건드리지 못한다
3. 마치 **운동장에만 있어야 하는** 학생이 **교무실**에 못 들어가는 것처럼요!
