+++
weight = 159
title = "프로세스 그룹"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

# 프로세스 그룹 (Process Group)

## Ⅰ. 프로세스 그룹의 개념

### 1. 정의

프로세스 그룹(Process Group)은 하나 이상의 프로세스를 논리적으로 묶는 커널의 grouping 메커니즘이다. 프로세스 그룹 내의 모든 프로세스는 동일한 PGID (Process Group ID)를 공유하며, 시그널(Signal)을 그룹 단위로 전송할 수 있다. 셸(Shell)은 파이프라인(Pipeline) 명령어를 실행할 때 연관된 프로세스들을 하나의 프로세스 그룹으로 묶는다.

> **비유**: 프로세스 그룹은 "한 팀의 운동선수들"이다. 감독(셸)은 팀 전체에 동시에 지시(시그널)를 내릴 수 있고, 각 선수(프로세스)는 자신의 팀 번호(PGID)를 안다.

### 2. PGID (Process Group ID)

- **PGID** (Process Group ID): 프로세스 그룹을 식별하는 정수값이다. 프로세스 그룹 리더(Leader)의 PID와 동일하다.
- 프로세스 그룹 리더: PGID와 PID가 동일한 프로세스. 리더가 종료되어도 그룹은 유지된다.

```
프로세스 그룹 구조

+----------------------------------------------------------+
|  Session (SID = 1000)                                    |
|                                                           |
|  +----------------------------------------------------+  |
|  | Process Group (PGID = 1000, Leader: bash PID=1000) |  |
|  |                                                    |  |
|  |  [bash]    PID=1000  PGID=1000  SID=1000  (Leader)|  |
|  |  [grep]    PID=2001  PGID=2001  SID=1000           |  |
|  +----------------------------------------------------+  |
|                                                           |
|  +----------------------------------------------------+  |
|  | Process Group (PGID = 2001, Leader: cat PID=2001) |  |
|  | (파이프라인: cat file | grep pattern)               |  |
|  |                                                    |  |
|  |  [cat]     PID=2001  PGID=2001  SID=1000  (Leader)|  |
|  |  [grep]    PID=2002  PGID=2001  SID=1000           |  |
|  +----------------------------------------------------+  |
|                                                           |
|  +----------------------------------------------------+  |
|  | Process Group (PGID = 3001, Leader: gcc PID=3001) |  |
|  |                                                    |  |
|  |  [gcc]     PID=3001  PGID=3001  SID=1000  (Leader)|  |
|  |  [cc1]     PID=3002  PGID=3001  SID=1000           |  |
|  |  [as]      PID=3003  PGID=3001  SID=1000           |  |
|  |  [collect2] PID=3004 PGID=3001  SID=1000           |  |
|  +----------------------------------------------------+  |
+----------------------------------------------------------+
```

> **비유**: 각 프로세스 그룹은 "프로젝트 팀"이고, PGID는 "팀 번호"다. 팀장(PGID=PID)이 퇴사해도 팀은 계속 존재한다.

---

## Ⅱ. 프로세스 그룹 관리 API

### 1. 시스템 콜 및 함수

| 함수 | 원형 | 설명 |
|------|------|------|
| **getpgrp()** | `pid_t getpgrp(void)` | 호출 프로세스의 PGID 반환 (POSIX) |
| **getpgid()** | `pid_t getpgid(pid_t pid)` | 지정 PID의 PGID 반환 |
| **setpgid()** | `int setpgid(pid_t pid, pid_t pgid)` | 프로세스의 PGID 설정 |
| **setpgrp()** | `int setpgrp(void)` | `setpgid(0, 0)`과 동일 (자신을 리더로 새 그룹 생성) |

### 2. setpgid()의 동작 규칙

```
setpgid(pid, pgid) 동작 규칙

+--------------------------------------------------------------+
|  setpgid(pid, pgid) 호출 시 검증 규칙                         |
|                                                              |
|  1. pid가 0이면 호출자 자신의 PID 사용                         |
|  2. pgid가 0이면 pid을 PGID로 사용 (새 그룹 생성)              |
|  3. pid는 호출자의 자식이거나 호출자 자신이어야 함              |
|  4. pid가 자식이면, fork() 직후 exec() 전에만 설정 가능         |
|     (그렇지 않으면 EACCES 에러)                                |
|  5. pgid는 호출자의 세션 내에 존재하는 프로세스 그룹이어야 함    |
+--------------------------------------------------------------+

예시:
  setpgid(0, 0)       // 자신을 리더로 새 프로세스 그룹 생성
  setpgid(child, 0)   // child를 리더로 새 프로세스 그룹 생성
  setpgid(child, pgid) // child를 기존 pgid 그룹에 추가
```

### 3. 사용 예제

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    pid_t pid = fork();
    
    if (pid == 0) {
        // 자식 프로세스
        // 새 프로세스 그룹에 자신을 리더로 배치
        setpgid(0, 0);
        
        printf("Child PID=%d, PGID=%d\n", getpid(), getpgid(0));
        // PID == PGID (그룹 리더)
    } else {
        // 부모 프로세스
        printf("Parent PID=%d, PGID=%d\n", getpid(), getpgid(0));
        
        // 자식을 새 그룹으로 이동 (fork 직후에 호출해야 함)
        setpgid(pid, pid);
        
        printf("Child PGID after setpgid: %d\n", getpgid(pid));
    }
    
    return 0;
}
```

---

## Ⅲ. 프로세스 그룹 시그널링

### 1. 그룹 시그널 전송

`kill()` 시스템 콜에 **음수 PID**를 전달하면, 해당 PGID를 가진 모든 프로세스에 시그널을 전송한다.

```
그룹 시그널 전송 메커니즘

kill(pid, sig)
  |
  +-- pid > 0  --> PID와 일치하는 단일 프로세스에 sig 전송
  |
  +-- pid == 0 --> 호출자와 동일 PGID의 모든 프로세스에 sig 전송
  |
  +-- pid < 0  --> |pid|와 일치하는 PGID의 모든 프로세스에 sig 전송
  |
  +-- pid == -1 --> 권한이 있는 모든 프로세스에 sig 전송 (SIGKILL 제한)

예시:
  kill(-2001, SIGTERM)
    --> PGID=2001인 모든 프로세스(cat, grep)에 SIGTERM 전송
    --> 파이프라인 전체가 종료됨
```

### 2. 실제 동작 예시

```
파이프라인 실행: $ cat file.txt | grep "error" | wc -l

+------------------------------------------------------+
|  PGID = 5001                                         |
|                                                      |
|  [cat]   PID=5001  PGID=5001  <--- 그룹 리더          |
|  [grep]  PID=5002  PGID=5001                         |
|  [wc]    PID=5003  PGID=5001                         |
+------------------------------------------------------+

Ctrl+C (SIGINT) 입력:
  --> 터미널이 포그라운드 프로세스 그룹(PGID=5001)에
      SIGINT 전송
  --> cat, grep, wc 모두 종료됨

또는:
  kill -TERM -5001
  --> PGID=5001인 모든 프로세스에 SIGTERM 전송
```

> **비유**: 그룹 시그널링은 "방송 시스템"이다. "300번 팀 전원, 즉시 철수하시오!"라고 하면 300번 팀에 속한 모든 선수가 동시에 철수한다.

---

## Ⅳ. 작업 제어 (Job Control)

### 1. 셸의 작업 제어

셸(Shell)은 프로세스 그룹을 활용하여 작업 제어(Job Control)를 구현한다. 포그라운드(Foreground)와 백그라운드(Background) 작업을 관리한다.

```
셸 작업 제어 구조

+----------------------------------------------------------+
|  Shell (bash)                                            |
|  PID=1000  PGID=1000  SID=1000                          |
|  Controlling Terminal: /dev/pts/0                        |
|                                                           |
|  포그라운드 그룹 (Foreground Process Group)               |
|  +----------------------------------------------------+  |
|  | PGID=5001 (현재 포그라운드)                           |  |
|  | [vim] PID=5001 PGID=5001                           |  |
|  +----------------------------------------------------+  |
|                                                           |
|  백그라운드 그룹 1 (Background Process Group)             |
|  +----------------------------------------------------+  |
|  | PGID=3001 (백그라운드)                               |  |
|  | [find] PID=3001 PGID=3001                           |  |
|  | [sort] PID=3002 PGID=3001                           |  |
|  +----------------------------------------------------+  |
|                                                           |
|  백그라운드 그룹 2 (Stopped)                              |
|  +----------------------------------------------------+  |
|  | PGID=4001 (정지 상태)                                |  |
|  | [python] PID=4001 PGID=4001  (SIGTSTP로 정지됨)      |  |
|  +----------------------------------------------------+  |
+----------------------------------------------------------+
```

### 2. 작업 제어 명령어

| 명령어 | 동작 | 프로세스 그룹 영향 |
|--------|------|-------------------|
| `command &` | 백그라운드 실행 | 새 PGID 할당, 백그라운드 그룹으로 이동 |
| `Ctrl+Z` (SIGTSTP) | 포그라운드 정지 | 포그라운드 그룹 전체에 SIGTSTP 전송 |
| `bg %1` | 정지된 작업을 백그라운드에서 재개 | 해당 그룹에 SIGCONT 전송 |
| `fg %1` | 백그라운드 작업을 포그라운드로 | 해당 그룹을 포그라운드로 전환 |
| `jobs` | 작업 목록 표시 | 각 작업의 PGID와 상태 표시 |
| `kill %1` | 작업에 시그널 전송 | 해당 PGID의 모든 프로세스에 전송 |

### 3. 파이프와 프로세스 그룹 생성

```
파이프라인에서의 프로세스 그룹 생성 과정

$ ls -la | grep "\.txt" | sort -k5 -n | head -5

[Step 1: 셸이 파이프라인 파싱]
  명령어: ls, grep, sort, head (4개 프로세스)

[Step 2: pipe()로 파이프 생성]
  pipe1: ls --> grep
  pipe2: grep --> sort
  pipe3: sort --> head

[Step 3: fork()로 각 프로세스 생성]
  fork(ls)  --> PID=6001
  fork(grep) --> PID=6002
  fork(sort) --> PID=6003
  fork(head) --> PID=6004

[Step 4: 모든 자식을 동일 PGID로 설정]
  setpgid(6001, 6001)  // ls가 리더
  setpgid(6002, 6001)  // grep을 ls의 그룹에
  setpgid(6003, 6001)  // sort를 ls의 그룹에
  setpgid(6004, 6001)  // head를 ls의 그룹에

[Step 5: 포그라운드 그룹으로 설정]
  tcsetpgrp(terminal_fd, 6001)
  --> 터미널 입출력이 PGID=6001 그룹에 연결
```

> **비유**: 파이프라인은 "조립 라인"이다. 컨베이어 벨트(파이프)로 연결된 작업자(프로세스)들은 모두 같은 조(프로세스 그룹)에 속한다. 감독(셸)이 "조 전원 휴식!"이라고 하면 조 전원이 함께 쉰다.

---

## Ⅴ. 요약 및 기술사 출제 포인트

### 핵심 정리

```
프로세스 그룹 요약도

[프로세스 그룹의 목적]
  1. 파이프라인의 프로세스들을 논리적으로 묶기
  2. 시그널을 그룹 단위로 전송
  3. 셸의 작업 제어(Foreground/Background) 구현
  4. 터미널 입출력 관리

[핵심 데이터]
  PGID: 프로세스 그룹 식별자
  그룹 리더: PID == PGID인 프로세스
  세션: 여러 프로세스 그룹의 상위 집합

[주요 API]
  getpgid()   : PGID 조회
  setpgid()   : PGID 설정
  kill(-pgid) : 그룹 시그널 전송
```

### 지식 그래프

```
프로세스 그룹
├── 기본 개념
│   ├── PGID (Process Group ID)
│   ├── 프로세스 그룹 리더 (PID == PGID)
│   └── 세션(Session)의 하위 개념
├── 관리 API
│   ├── getpgrp() (자신의 PGID 반환)
│   ├── getpgid(pid) (지정 PID의 PGID 반환)
│   ├── setpgid(pid, pgid) (PGID 설정)
│   └── setpgrp() (setpgid(0,0)과 동일)
├── 시그널링
│   ├── kill(-PGID, SIGTERM) (그룹 전체 전송)
│   ├── kill(0, SIGTERM) (동일 그룹 전체)
│   └── 터미널 시그널 (SIGINT, SIGTSTP)
├── 작업 제어 (Job Control)
│   ├── 포그라운드 프로세스 그룹
│   ├── 백그라운드 프로세스 그룹
│   ├── bg/fg 명령어
│   └── tcsetpgrp() (포그라운드 그룹 전환)
├── 파이프라인
│   ├── pipe()로 프로세스 간 연결
│   ├── 파이프라인 전체가 하나의 PGID
│   └── 첫 번째 프로세스가 그룹 리더
└── 관련 개념
    ├── 세션 (Session, SID)
    ├── 제어 터미널 (Controlling Terminal)
    └── 데몬 (Daemon, setsid()로 분리)
```

### 세 줄 설명 (어린이용)

1. 프로세스 그룹은 여러 프로그램을 하나의 팀으로 묶어서, 한 번에 명령을 내릴 수 있게 만드는 것이에요.
2. 엔터키를 눌러 `cat | grep` 같은 명령을 실행하면, 컴퓨터가 알아서 같은 팀(PGID)으로 묶어줘요.
3. Ctrl+C를 누르면 같은 팀에 속한 모든 프로그램이 동시에 멈추게 돼요.

### 약어 정리

| 약어 | Full Name |
|------|-----------|
| PGID | Process Group ID |
| SID | Session ID |
| PID | Process Identifier |
| API | Application Programming Interface |
