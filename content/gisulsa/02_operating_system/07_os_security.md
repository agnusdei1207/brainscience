+++
weight = 7
title = "07. OS 보안 & 리눅스 권한"
date = "2026-05-17"
[extra]
categories = "gisulsa-os"
+++

# 🎯 OS 보안 — 리눅스 권한 & SELinux

> **별점**: ★★★★★ | 기본 필수

## 1. 리눅스 파일 권한

```
[DAC (임의적 접근 제어)]
소유자가 권한 설정: rwxrwxrwx (소유자/그룹/기타)

r (4): 읽기, w (2): 쓰기, x (1): 실행

예) -rwxr-xr--
  소유자: rwx (7) = 읽기+쓰기+실행
  그룹: r-x (5) = 읽기+실행
  기타: r-- (4) = 읽기만

[특수 비트]
SetUID (4xxx): 실행 시 소유자 권한으로
SetGID (2xxx): 실행 시 그룹 권한으로
Sticky Bit (1xxx): 공유 디렉토리에서 자신 파일만 삭제

sudo:
  특정 명령어를 root 권한으로 실행
  /etc/sudoers에 권한 설정
```

## 2. MAC & SELinux

```
[MAC (강제적 접근 제어)]
관리자가 정의한 정책으로 접근 통제
소유자도 임의 변경 불가

[SELinux (Security-Enhanced Linux)]
NSA 개발, 리눅스 커널 내장
Type Enforcement: 도메인(프로세스)-타입(파일) 규칙
  예) httpd_t 도메인은 httpd_sys_content_t 타입만 접근

모드:
  Enforcing: 정책 강제 (차단 + 로그)
  Permissive: 로그만 (개발/디버그)
  Disabled: SELinux 비활성

컨텍스트: ls -Z (파일), ps -Z (프로세스)
  시스템_u:object_r:httpd_sys_content_t:s0
```

## 3. 네임스페이스 & cgroups (컨테이너 격리)

```
[Linux Namespaces]
PID: 프로세스 ID 격리 (컨테이너 내 PID 1)
Net: 네트워크 인터페이스 격리
Mount: 파일시스템 격리
User: UID/GID 격리
IPC: 프로세스 간 통신 격리

[cgroups v2]
자원 그룹화 & 제한
CPU: 코어 할당, 스로틀링
Memory: 메모리 한도, OOM 킬러
I/O: 블록 I/O 대역폭 제한
```

## 4. 답안 포인트

**3단락**: ① 리눅스 DAC 권한 체계 & 특수 비트 → ② SELinux MAC & Type Enforcement → ③ Namespace/cgroups 컨테이너 격리

## 5. 관련 개념

`컨테이너(06번)` → Namespace+cgroups 기반 | `Zero Trust(09_security)` → MAC 접근 제어와 연계 | `DevSecOps` → 최소 권한 원칙
