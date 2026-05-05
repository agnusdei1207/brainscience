+++
weight = 156
title = "156. 환경 변수 (Environment Variables) 상속"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

## 0. 핵심 인사이트

> **핵심**: 환경 변수 (Environment Variables) 상속은(는) 운영체제가 자원을 추상화하고 통제하는 과정에서 성능, 보호, 응답성을 동시에 조율하기 위해 필요한 핵심 개념이다.
> **비유**: 환경 변수는 "가족의 전통 레시피"다. 부모가 아이에게 전달하며, 아이는 그대로 사용하거나 자신만의 재료를 추가할 수 있다.

---

📝 모범 답안

## 1. 개요 및 필요성

### 1. 정의

환경 변수(Environment Variable)는 운영체제에서 프로세스가 실행될 때 참조할 수 있는 키-값(Key-Value) 쌍으로 이루어진 문자열이다. 프로세스는 부모 프로세스(Parent Process)로부터 환경 변수를 상속(Inherit)받으며, 이를 통해 실행 환경 설정을 자식 프로세스(Child Process)에 전달한다.

### 2. 프로세스 메모리에서의 환경 변수

```
프로세스 메모리 레이아웃 상 환경 변수의 위치

High Address
+---------------------------+
|         Stack             |
|   argv[0], argv[1], ...   |
|   envp[0], envp[1], ...  | <-- 환경 변수 포인터 배열
|   argc                     |
+---------------------------+
|          |                |  Stack grows downward
|          v                |
+---------------------------+
|        Heap               |  Heap grows upward
+---------------------------+
|       BSS                 |
|       Data                |
|       Text (Code)         |
+---------------------------+
Low Address

환경 변수 블록 (Environ Block):
+--------------------------------------+
| PATH=/usr/bin:/bin                   |
| HOME=/home/user                      |
| LANG=ko_KR.UTF-8                     |
| LD_LIBRARY_PATH=/opt/lib             |
| SHELL=/bin/bash                      |
| TERM=xterm-256color                  |
| NULL (terminator)                    |
+--------------------------------------+
```

> **비유**: 환경 변수는 프로세스라는 "가방" 주머니에 넣어둔 "메모 쪽지"들이다. 프로그램은 언제든 주머니에서 꺼내 읽을 수 있다.

---

## 2. 구성요소

### 1. 시스템 핵심 환경 변수

| 환경 변수 | 설명 | 예시 |
|-----------|------|------|
| **PATH** | 실행 파일 검색 경로 | `/usr/bin:/bin:/usr/local/bin` |
| **HOME** | 사용자 홈 디렉토리 | `/home/user` |
| **LANG** | 로케일 및 언어 설정 | `ko_KR.UTF-8` |
| **SHELL** | 로그인 셸 경로 | `/bin/bash` |
| **TERM** | 터미널 유형 | `xterm-256color` |
| **USER** | 현재 사용자 이름 | `ubuntu` |
| **PWD** | 현재 작업 디렉토리 | `/home/user/project` |
| **LD_LIBRARY_PATH** | 동적 라이브러리 검색 경로 | `/opt/oracle/lib` |
| **LD_PRELOAD** | 사전 로드할 라이브러리 | `/tmp/malloc_hook.so` |
| **TMPDIR** | 임시 파일 디렉토리 | `/tmp` |

### 2. PATH 환경 변수

- **PATH** (Path): 셸이 명령어를 입력받았을 때 실행 파일을 검색하는 디렉토리 목록이다. 콜론(`:`)으로 구분되며, 왼쪽부터 순서대로 검색한다.

```bash
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

$ export PATH=.:$PATH   # 위험: 현재 디렉토리의 악성 파일 실행 가능
```

### 3. 환경 변수 설정 방법

```bash
export MY_VAR="hello"

echo 'export MY_VAR="hello"' >> ~/.bashrc

MY_VAR="hello" /bin/child_program

unset MY_VAR
```

---

## 3. 구조 및 원리

**핵심 조건**: 운영체제의 해당 메커니즘은 현재 상태 정보, 자원 제약, 정책 기준이 함께 정합성을 가질 때 안정적으로 동작한다.

동작 순서:
1. **요청 또는 이벤트 발생**: 사용자 요청, 인터럽트, 시스템 호출 등으로 커널이 해당 기능을 처리할 필요가 생긴다.
2. **현재 상태 확인**: 커널은 큐, 제어 블록, 메타데이터, 자원 가용량을 확인해 실행 가능 여부와 우선순위를 판단한다.
3. **정책 적용 및 자원 배정**: 해당 주제의 핵심 정책에 따라 상태 전이, 자원 할당, 보호 검사를 수행한다.
4. **결과 반영 및 후속 처리**: 처리 결과를 시스템 상태에 기록하고 다음 인터럽트·스케줄링·복구 단계로 연결한다.

### 1. C 표준 라이브러리 함수

| 함수 | 원형 | 설명 |
|------|------|------|
| **getenv()** | `char *getenv(const char *name)` | 환경 변수 값 조회 |
| **setenv()** | `int setenv(const char *name, const char *value, int overwrite)` | 환경 변수 설정 (overwrite=1이면 덮어씀) |
| **putenv()** | `int putenv(char *string)` | "NAME=VALUE" 형식 문자열로 설정 (버퍼 소유권 이전) |
| **unsetenv()** | `int unsetenv(const char *name)` | 환경 변수 제거 |
| **environ** | `extern char **environ` | 전체 환경 변수 배열에 대한 전역 포인터 |

### 2. 사용 예제

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 환경 변수 조회
    char *path = getenv("PATH");
    if (path) {
        printf("PATH: %s\n", path);
    }

    // 환경 변수 설정 (기존 값 있으면 덮어씀)
    setenv("MY_APP_DIR", "/opt/myapp", 1);

    // putenv: 문자열 포인터를 직접 전달 (주의: 버퍼 수정 시 문제)
    putenv("MY_TEMP_VAR=temp_value");

    // 환경 변수 제거
    unsetenv("MY_TEMP_VAR");

    // 전체 환경 변수 순회
    extern char **environ;
    for (char **env = environ; *env != NULL; env++) {
        printf("%s\n", *env);
    }

    return 0;
}
```

```
환경 변수 API 동작 흐름

[getenv("PATH")]
    |
    v
environ 배열에서 "PATH="로 시작하는 항목 검색
    |
    v
"PATH=/usr/bin:/bin"에서 '=' 이후 문자열 반환
    |
    v
포인터 반환 (복사본 아님, 수정하면 안 됨)

[setenv("KEY", "VALUE", 1)]
    |
    v
environ 배열에서 "KEY=" 검색
    |
    +-- 있고 overwrite=1 --> 기존 항목 대체
    |
    +-- 없음 --> environ 배열 확장 후 새 항목 추가
```

> **비유**: getenv()는 "전화번호부에서 이름 찾기", setenv()는 "전화번호부에 새 번호 등록하기"와 같다. putenv()는 "직접 전화번호부 책갈피에 메모지 꽂기"라서 메모지를 분실하면 번호도 사라진다.

---

## 4. 비교 및 연결

### 1. C 표준 라이브러리 함수

| 함수 | 원형 | 설명 |
|------|------|------|
| **getenv()** | `char *getenv(const char *name)` | 환경 변수 값 조회 |
| **setenv()** | `int setenv(const char *name, const char *value, int overwrite)` | 환경 변수 설정 (overwrite=1이면 덮어씀) |
| **putenv()** | `int putenv(char *string)` | "NAME=VALUE" 형식 문자열로 설정 (버퍼 소유권 이전) |
| **unsetenv()** | `int unsetenv(const char *name)` | 환경 변수 제거 |
| **environ** | `extern char **environ` | 전체 환경 변수 배열에 대한 전역 포인터 |

### 2. 사용 예제

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 환경 변수 조회
    char *path = getenv("PATH");
    if (path) {
        printf("PATH: %s\n", path);
    }

    // 환경 변수 설정 (기존 값 있으면 덮어씀)
    setenv("MY_APP_DIR", "/opt/myapp", 1);

    // putenv: 문자열 포인터를 직접 전달 (주의: 버퍼 수정 시 문제)
    putenv("MY_TEMP_VAR=temp_value");

    // 환경 변수 제거
    unsetenv("MY_TEMP_VAR");

    // 전체 환경 변수 순회
    extern char **environ;
    for (char **env = environ; *env != NULL; env++) {
        printf("%s\n", *env);
    }

    return 0;
}
```

```
환경 변수 API 동작 흐름

[getenv("PATH")]
    |
    v
environ 배열에서 "PATH="로 시작하는 항목 검색
    |
    v
"PATH=/usr/bin:/bin"에서 '=' 이후 문자열 반환
    |
    v
포인터 반환 (복사본 아님, 수정하면 안 됨)

[setenv("KEY", "VALUE", 1)]
    |
    v
environ 배열에서 "KEY=" 검색
    |
    +-- 있고 overwrite=1 --> 기존 항목 대체
    |
    +-- 없음 --> environ 배열 확장 후 새 항목 추가
```

> **비유**: getenv()는 "전화번호부에서 이름 찾기", setenv()는 "전화번호부에 새 번호 등록하기"와 같다. putenv()는 "직접 전화번호부 책갈피에 메모지 꽂기"라서 메모지를 분실하면 번호도 사라진다.

---

## 5. 실무 적용 및 판단

### 1. fork() 시 환경 변수 복사

`fork()` 시스템 콜은 부모 프로세스의 환경 변수 블록(Environ Block)을 자식 프로세스로 **복사(Copy)**한다. 부모와 자식은 독립적인 복사본을 가지므로, 한쪽에서 `setenv()`를 호출해도 다른 쪽에 영향을 주지 않는다.

```
fork() 시 환경 변수 복사

[Parent Process]                    [Child Process]
environ:                            environ:
  PATH=/usr/bin                       PATH=/usr/bin       (복사본)
  HOME=/home/user                     HOME=/home/user     (복사본)
  MY_VAR=parent                       MY_VAR=parent       (복사본)
        |                                    |
        | fork()                             |
        v                                    v
  setenv("MY_VAR", "changed", 1)       // 영향 없음
  MY_VAR=changed                      MY_VAR=parent (그대로)
```

### 2. exec() 시 환경 변수 대체

`exec()` 계열 함수는 현재 프로세스의 이미지를 새 프로그램으로 **완전히 교체**한다. 이때 환경 변수 처리는 함수에 따라 다르다.

| 함수 | 환경 변수 동작 |
|------|---------------|
| `execl(path, arg...)` | 기존 환경 변수 유지 |
| `execv(path, argv)` | 기존 환경 변수 유지 |
| `execle(path, arg..., envp)` | **새 envp로 대체** |
| `execve(path, argv, envp)` | **새 envp로 대체** |
| `execlp(file, arg...)` | 기존 환경 변수 유지 + PATH 검색 |
| `execvp(file, argv)` | 기존 환경 변수 유지 + PATH 검색 |

```
exec() 계열의 환경 변수 처리

[execl("/bin/ls", "ls", NULL)]
    기존 environ 블록 그대로 유지
    --> ls가 부모와 동일한 환경 변수로 실행됨

[execle("/bin/ls", "ls", NULL, new_envp)]
    기존 environ 폐기
    --> new_envp 배열이 새 environ이 됨
    --> 부모의 환경 변수 완전히 사라짐

[execve("/bin/ls", argv, new_envp)]
    execle와 동일 (배열 형식)
```

> **비유**: fork()는 "부모의 레시피 노트를 복사해서 아이에게 주는 것"이고, execle()는 "아이가 자기만의 새 레시피 노트로 교체하는 것"이다.

---

## 6. 기대효과 및 결론

### 1. LD_PRELOAD의 동작 원리

- **LD_PRELOAD**: 동적 링커가 다른 모든 라이브러리보다 먼저 로드하는 라이브러리 경로를 지정하는 환경 변수이다. 이를 이용해 표준 라이브러리 함수를 가로채거나(Hooking) 대체할 수 있다.

### 2. 공격 시나리오

```c
// malicious.c - malloc을 가로채는 악성 라이브러리
#include <stdio.h>

void *malloc(size_t size) {
    printf("[ATTACK] malloc(%zu) intercepted!\n", size);
    // 원래 malloc 대신 임의 동작 수행
    return NULL;  // DoS 공격
}
```

```bash
gcc -shared -fPIC -o /tmp/malicious.so malicious.c -ldl

LD_PRELOAD=/tmp/malicious.so /usr/bin/victim_program
```

### 3. 방어 수단

```
LD_PRELOAD 공격 방어 레이어

+------------------------------------------+
| 1. SUID/SGID 바이너리                     |
|    -> LD_PRELOAD 무시 (보안 설정)          |
+------------------------------------------+
| 2. /etc/ld.so.preload (관리자 전용)       |
|    -> 시스템 수준 preloading만 허용        |
+------------------------------------------+
| 3. setenv("LD_PRELOAD", "", 1)           |
|    -> 프로그램 시작 시 명시적 초기화        |
+------------------------------------------+
| 4. Docker/Container 격리                  |
|    -> 호스트 환경 변수 격리                |
+------------------------------------------+
| 5. Capabilities / SELinux                 |
|    -> 라이브러리 로딩 권한 제한            |
+------------------------------------------+
```

> **비유**: LD_PRELOAD 공격은 "수업 전에 선생님의 교과서를 가짜 교과서로 몰래 바꿔치기하는 것"이다. SUID는 "출입증을 확인하는 교실 문지기" 역할을 한다.

---

## 7. 발전 흐름도

```text
기초 자원 관리 문제
    ↓
환경 변수 (Environment Variables) 상속
    ↓
성능·격리·공정성 최적화
    ↓
가상화·관측·자동화 통합
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 환경 변수 (Environment Variables) 상속 | 운영체제 자원 관리와 보호 정책이 실제로 적용되는 핵심 주제 |
| 커널 (Kernel) | 정책 집행, 상태 전이, 시스템 호출 처리의 중심 |
| 프로세스/스레드 | CPU, 메모리, 동기화 자원과 직접 연결되는 실행 단위 |
| 메모리/I/O | 성능 병목과 보호 요구사항이 함께 드러나는 연계 영역 |
| 가상화/보안 | 격리, 제어, 관측 확장 관점에서 해당 주제가 연결되는 상위 개념 |
