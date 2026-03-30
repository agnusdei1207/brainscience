+++
weight = 155
title = "동적 링킹 프로세스"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

# 동적 링킹 프로세스 (Dynamic Linking Process)

## Ⅰ. 동적 링킹의 개념과 필요성

### 1. 정의

동적 링킹(Dynamic Linking)은 프로그램 실행 시점(Run-time)에 외부 공유 라이브러리(Shared Library)를 메모리에 적재하고 결합하는 과정이다. 정적 링킹(Static Linking)이 빌드 시점에 모든 코드를 복사하는 것과 달리, 동적 링킹은 라이브러리를 여러 프로세스가 공유하여 메모리를 절약한다.

> **비유**: 정적 링킹은 책에 부록을 직접 인쇄해 넣는 것이고, 동적 링킹은 도서관에서 필요할 때마다 공용 참고서를 빌려 읽는 것이다.

### 2. 동적 링커 (Dynamic Linker / Loader)

| 플랫폼 | 동적 링커 | 경로 |
|--------|-----------|------|
| Linux | **ld.so** (ld-linux.so) | `/lib/ld-linux.so` 또는 `/lib64/ld-linux-x86-64.so.2` |
| macOS | **dyld** (Dynamic Linker) | `/usr/lib/dyld` |

- **ld.so** (Linker and Loader Shared Object): ELF 바이너리의 `PT_INTERP` 세그먼트에 지정된 동적 링커로, 커널이 프로그램을 로드할 때 먼저 실행된다.
- **dyld** (Dynamic Linker eDitor): macOS의 동적 링커로 Mach-O 바이너리를 처리한다.

### 3. ELF에서의 동적 링킹 구조

```
ELF Executable Layout (동적 링킹 관련)
+--------------------------------------------------+
|  ELF Header                                      |
|    e_ident: "Magic Number"                       |
|    e_type:  ET_EXEC / ET_DYN                    |
|    e_phoff: Program Header Table offset          |
+--------------------------------------------------+
|  Program Header Table                            |
|    PT_INTERP  --> /lib64/ld-linux-x86-64.so.2  |
|    PT_LOAD    --> .text, .data 세그먼트          |
|    PT_DYNAMIC --> .dynamic 세그먼트              |
|    PT_NOTE    --> auxiliary info                 |
+--------------------------------------------------+
|  .text (Code Section)                            |
|  .plt  (Procedure Linkage Table)                |
|  .got  (Global Offset Table)                    |
|  .got.plt (PLT용 GOT)                           |
|  .data (Data Section)                            |
|  .dynamic (Linker Metadata)                      |
+--------------------------------------------------+
|  Section Header Table                            |
+--------------------------------------------------+
```

> **비유**: PLT는 "어떤 책이 어디 있는지 적어둔 도서관 안내판"이고, GOT는 "실제 책이 꽂힌 선반 번호표"다. 처음에는 안내판만 보고 찾아가고, 두 번째부터는 선반 번호표를 바로 이용한다.

---

## Ⅱ. PLT와 GOT의 동작 원리

### 1. PLT (Procedure Linkage Table)

PLT는 외부 함수(Shared Library 함수)를 호출하기 위한 점프 테이블이다. 각 외부 함수에 대해 하나의 PLT 엔트리가 존재하며, 첫 호출 시 동적 링커가 실제 주소를 해석한다.

```
PLT 엔트리 구조 (x86-64 어셈블리 개념도)
+-------------------------------------------+
| PLT[0]: Push GOT[1]; Jump to ld.so        |
|   (동적 링커 진입점)                       |
+-------------------------------------------+
| PLT[1] (printf):                          |
|   jmp *GOT[printf]  <-- 첫 호출: PLT 자신 |
|   push reloc_offset                        |
|   jmp PLT[0]          --> ld.so 해석      |
+-------------------------------------------+
| PLT[2] (malloc):                          |
|   jmp *GOT[malloc]                         |
|   push reloc_offset                        |
|   jmp PLT[0]                               |
+-------------------------------------------+
```

### 2. GOT (Global Offset Table)

GOT는 외부 심볼의 실제 메모리 주소를 저장하는 테이블이다.

```
PLT/GOT 연동 흐름 (Lazy Binding)

[1st Call] printf("hello")
    |
    v
PLT[printf]: jmp *GOT[printf]
    |
    v  (GOT에는 PLT 다음 명령어 주소)
    push reloc_index
    jmp PLT[0] --> ld.so
    |
    v
Dynamic Linker resolves printf in libc.so
    |
    v
GOT[printf] = &real_printf  (실제 주소 기록)
    |
    v
printf("hello") 실행

[2nd Call] printf("world")
    |
    v
PLT[printf]: jmp *GOT[printf]
    |
    v  (GOT에는 실제 printf 주소!)
    --> 직접 printf로 점프 (오버헤드 없음)
```

### 3. 지연 바인딩 (Lazy Binding) vs 즉시 바인딩 (Eager Binding)

| 특징 | Lazy Binding | Eager Binding |
|------|-------------|---------------|
| 해석 시점 | 함수가 처음 호출될 때 | 프로그램 시작 시 모든 함수 |
| 시작 시간 | 빠름 | 느림 |
| 실행 중 오버헤드 | 첫 호출에만 발생 | 없음 |
| 오류 감지 시점 | 실행 중 (늦음) | 시작 시 (빠름) |
| 설정 옵션 | 기본 동작 | `LD_BIND_NOW=1` 또는 컴파일 시 `-z now` |
| 보안 | 첫 호출 시 지연으로 인한 타이밍 공격 가능 | 더 안전 |

> **비유**: Lazy Binding은 "누가 물어볼 때까지 정답을 계산하지 않는 학생"이고, Eager Binding은 "시험 전에 모든 답을 미리 계산해 두는 학생"이다.

---

## Ⅲ. 라이브러리 검색 경로

### 1. 검색 우선순위

```
라이브러리 검색 우선순위 (Library Search Order)

1. RPATH (ELF 내부, compile-time)
   |
2. LD_LIBRARY_PATH (환경 변수, runtime)
   |
3. RUNPATH (ELF 내부, compile-time)
   |
4. /etc/ld.so.cache (ldconfig 결과)
   |
5. 기본 경로: /lib, /usr/lib
```

### 2. LD_LIBRARY_PATH

- **LD_LIBRARY_PATH** (Library Path): 동적 링커가 공유 라이브러리를 검색할 때 사용하는 콜론(`:`)으로 구분된 디렉토리 목록이다.
- 개발 중에는 편리하지만, 프로덕션 환경에서는 보안 및 예측성 문제로 사용을 지양한다.

```bash
# 예시
export LD_LIBRARY_PATH=/opt/mylib/lib:$LD_LIBRARY_PATH
```

### 3. RPATH와 RUNPATH

| 특징 | RPATH | RUNPATH |
|------|-------|---------|
| 저장 위치 | ELF `.dynamic` 섹션 | ELF `.dynamic` 섹션 |
| LD_LIBRARY_PATH보다 | 우선함 | 우선하지 않음 |
| 설정 옵션 | `-rpath` (기본) | `-rpath` + `-Wl,--enable-new-dtags` |
| `$ORIGIN` 지원 | 가능 | 가능 |
| 보안 | LD_LIBRARY_PATH 무시 가능 | LD_LIBRARY_PATH가 우선 |

```bash
# 컴파일 시 RPATH 설정
gcc -o myapp main.c -L./lib -lmylib -Wl,-rpath,'$ORIGIN/../lib'

# RUNPATH로 설정
gcc -o myapp main.c -L./lib -lmylib -Wl,-rpath,'$ORIGIN/../lib' -Wl,--enable-new-dtags
```

> **비유**: RPATH는 "집에 고정된 내선번호"이고, LD_LIBRARY_PATH는 "전화번호부에 임시로 적어둔 번호"다. RPATH가 항상 먼저 걸린다 (RUNPATH는 제외).

### 4. ldd 명령어

- **ldd** (List Dynamic Dependencies): 실행 파일이나 공유 라이브러리가 의존하는 동적 라이브러리 목록을 표시한다.

```bash
$ ldd /bin/ls
    linux-vdso.so.1 (0x00007ffc123fd000)
    libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1 (0x00007f8b0a3a0000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f8b0a1d8000)
    libpcre2-8.so.0 => /lib/x86_64-linux-gnu/libpcre2-8.so.0 (0x00007f8b0a142000)
    /lib64/ld-linux-x86-64.so.2 (0x00007f8b0a3f6000)
```

---

## Ⅳ. 재배치 (Relocation)

### 1. 재배치의 필요성

공유 라이브러리는 PIE (Position Independent Executable) 및 ASLR (Address Space Layout Randomization)로 인해 매번 다른 가상 주소에 로드된다. 따라서 절대 주소를 사용하는 코드는 런타임에 재배치(Relocation)가 필요하다.

```
재배치 전후 비교

[Before Relocation]          [After Relocation]
GOT[printf] = 0x00000000     GOT[printf] = 0x7f8b0a250680
GOT[malloc]  = 0x00000000    GOT[malloc]  = 0x7f8b0a1c4b90
PLT entries: unresolved       PLT entries: resolved

Library loaded at: ?         Library loaded at: 0x7f8b0a1a0000
                             (ASLR에 의해 매번 다른 주소)
```

### 2. 재배치 종류

| 재배치 유형 | 설명 | 대상 |
|-------------|------|------|
| R_X86_64_GLOB_DAT | GOT 엔트리에 절대 주소 기록 | 전역 변수, 함수 주소 |
| R_X86_64_JUMP_SLOT | PLT/GOT에 절대 주소 기록 (Lazy) | 외부 함수 |
| R_X86_64_RELATIVE | 베이스 주소 + 오프셋 | PIE 코드 내부 참조 |
| R_X86_64_COPY | 복사 재배치 (data 복사) | `__attribute__((visibility("default")))` 전역 변수 |

### 3. PIC와 PIE

- **PIC** (Position Independent Code): 공유 라이브러리가 어떤 주소에 로드되어도 동작하도록 컴파일된 코드
- **PIE** (Position Independent Executable): 실행 파일 자체도 위치 독립적으로 만드는 기법
- 컴파일 옵션: `-fPIC` (라이브러리), `-pie` (실행 파일)

> **비유**: PIC/PIE는 "어느 자리에 앉아도 수업을 들을 수 있는 이동식 강의실"이다. 고정된 좌석 배치(절대 주소)에 의존하지 않는다.

---

## Ⅴ. 요약 및 기술사 출제 포인트

### 핵심 정리

```
동적 링킹 프로세스 요약도

[프로그램 실행]
      |
      v
[커널이 ELF 로드]
      |
      v
[PT_INTERP 확인 --> ld.so 실행]
      |
      v
[ld.so가 필요한 공유 라이브러리 검색]
  RPATH -> LD_LIBRARY_PATH -> RUNPATH -> 캐시 -> 기본경로
      |
      v
[라이브러리를 메모리에 매핑]
      |
      v
[재배치 수행 (Relocation)]
  GOT 엔트리에 실제 주소 기록
      |
      v
[Lazy/Eager Binding 설정 적용]
      |
      v
[프로그램 main() 실행]
```

### 지식 그래프

```
동적 링킹 프로세스
├── 동적 링커
│   ├── ld.so (Linux ELF)
│   └── dyld (macOS Mach-O)
├── 핵심 데이터 구조
│   ├── PLT (Procedure Linkage Table)
│   ├── GOT (Global Offset Table)
│   └── .dynamic 세그먼트
├── 바인딩 전략
│   ├── Lazy Binding (지연 바인딩)
│   └── Eager Binding (즉시 바인딩)
├── 검색 경로
│   ├── RPATH
│   ├── LD_LIBRARY_PATH
│   ├── RUNPATH
│   ├── ld.so.cache
│   └── 기본 경로 (/lib, /usr/lib)
├── 재배치
│   ├── GLOB_DAT
│   ├── JUMP_SLOT
│   ├── RELATIVE
│   └── COPY
├── 관련 기법
│   ├── PIC (Position Independent Code)
│   ├── PIE (Position Independent Executable)
│   └── ASLR (Address Space Layout Randomization)
└── 진단 도구
    ├── ldd (의존성 확인)
    ├── readelf -d (RPATH/RUNPATH 확인)
    └── LD_DEBUG (링커 디버그)
```

### 세 줄 설명 (어린이용)

1. 동적 링킹은 프로그램이 켜질 때 필요한 도구(라이브러리)를 가져다 쓰는 방법이에요.
2. PLT와 GOT라는 표를 써서 처음 한 번만 도구를 찾고, 다음부터는 빠르게 쓸 수 있어요.
3. Lazy Binding은 필요할 때 찾고, Eager Binding은 미리 다 찾아두는 방식이에요.

### 약어 정리

| 약어 | Full Name |
|------|-----------|
| PLT | Procedure Linkage Table |
| GOT | Global Offset Table |
| PIC | Position Independent Code |
| PIE | Position Independent Executable |
| ASLR | Address Space Layout Randomization |
| ELF | Executable and Linkable Format |
| RPATH | Run-time search PATH |
| RUNPATH | Run-time search PATH (new DTAGs) |
| VDSO | Virtual Dynamic Shared Object |
