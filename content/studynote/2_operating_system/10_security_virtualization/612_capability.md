+++
title = "612. Capability (자격증, 능력)"
weight = 612
+++

# 612. Capability (자격증, 능력)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: Capability는 주체(Subject)가 갖는 "자신이 접근 가능한 객체(Object)와 권한(Right)"을 불변 토큰(Token) 형태로 보관하는, 주체 중심 접근 제어 메커니즘이다.
> 2. **가치**: 토큰은 위조 불가하고, 소유자가 자유롭게 전달(Delegate)할 수 있어 분산 시스템, 마이크로커널, 보안 OS 설계에 적합하다. E 시스템, KEYKOS, Capsicum이 대표적 구현이다.
> 3. **융합**: POSIX Capability, Kerberos 티켓, Web Session Cookie 등 현대 보안 시스템에 널리 사용되며, 객체 capability(OOP 참조 투명성)와도 개념적 연관성이 있다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**Capability**는 **보호된 객체에 대한 참조와 권한을 캡슐화한 불변의 자격 증명서(Token)**다. ACL(Access Control List)이 객체 중심("누가 나에 접근할 수 있는가?")인 반면, Capability는 주체 중심("내가 무엇을 할 수 있는가?")이다. Capability는 (객체 참조, 권한 비트) 쌍을 커널 또는 사용자 공간의 보호 데이터 구조에 저장하며, 이 토큰을 소유한 주체만이 객체에 접근할 수 있다. 토큰은 복사할 수 있지만, 위조나 변조는 불가능하도록 설계된다.

### 💡 비유: 호텔 키 카드

Capability는 **호텔 키 카드**와 같다. 키 카드는 "객실 302호, 2박 3일 체류" 정보가 저장된 자기 카드로, 소지자만 객실에 들어갈 수 있다. 카드를 잃어버리면 누구나 객실에 들어갈 수 있지만, 카드를 위조하기는 어렵다(자기 스트라이프 암호화). 또한 키 카드를 타인에게 빌려줄 수 있고(Delegation), 체크아웃 시에는 카드가 자동으로 무효화된다(Expiration). 반면 ACL은 "객실 302호에 입장 가능한 사람 목록"을 프런트에 보관하는 것과 같다. 둘 다 보안을 제공하지만, 관리 방식이 다르다.

### 등장 배경

1. **1966: Capability의 탄생**:剑桥大学의 R. M. Needham과 기술자들이 Atlas Computer에서 메모리 보호를 위해 "capability" 개념을 도입했다. 주소 공간뿐 아니라 장치, 파일에 대한 보호를 단일 메커니즘으로 통합하고자 했다.
2. **1970s: Capability 기반 OS**: Plessey System 250, Cambridge CAP 컴퓨터에서 하드웨어/소프트웨어 capability가 구현되었다. Hydra, KeyKOS, E 시스템 등 마이크로커널에서 메시지 전달로 capability 전달이 연구되었다.
3. **1990s-2000s: POSIX Capability와 분산 시스템**: 리눅스 2.2(1999)부터 POSIX Capability(CAP_NET_BIND_SERVICE 등)가 root 권한을 세분화하기 위해 도입되었다. Kerberos 티켓도 분산 시스템에서 capability로 활용된다.
4. **2010s-현재: Capsicum과 Cloudflare Workers**: FreeBSD Capsicum(2010)은 프로세스를 샌드박스에 가두고 capability로 최소 권한만 부여한다. Cloudflare Workers, WASM도 capability 기반 샌드박스를 사용한다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                  Capability의 발전 역사                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【1966: Cambridge Atlas Computer】                                      │
│  ────────────────────────────────                                       │
│  • "capability" 용어 최초 사용                                            │
│  • 메모리, 장치, 파일 보호의 단일 메커니즘                                   │
│                                                                         │
│  【1970s: 초기 Capability 기반 OS】                                       │
│  ─────────────────────────────────                                      │
│  • Plessey System 250 (1972): 하드웨어 태그 비트로 capability 구현             │
│  • Cambridge CAP (1975): capability 레지스터, 메모리 보호                   │
│  • Hydra (CMU, 1975): 마이크로커널 capability 메시지 전달                     │
│  • KeyKOS (1980s): capability 기반 상업용 OS                               │
│                                                                         │
│  【1980s: E 시스템(CMU, 1986)】                                           │
│  ────────────────────────────                                           │
│  • 완전한 capability 기반 언어/OS                                          │
│  • C++와 유사한 구문, capability는 유일한 자원 접근 방법                       │
│  • 메모리 안전성 보장, 수동 메모리 관리 불필요                                │
│                                                                         │
│  【1990s: POSIX Capability】                                             │
│  ──────────────────────────                                             │
│  • POSIX 1003.1e에서 capability 표준 제안                                 │
│  • Linux 2.2(1999): CAP_NET_RAW, CAP_SYS_ADMIN 등 26개 capability 도입    │
│  • root 권한 세분화, 최소 권한 원칙 지원                                    │
│                                                                         │
│  【2000s-현재: 분산 시스템과 샌드박스】                                      │
│  ────────────────────────────────                                       │
│  • Kerberos 티켓: 분산 인증 capability                                      │
│  • FreeBSD Capsicum(2010): capability-based sandbox                      │
│  • WebAssembly(WASM): capability-based 권한                               │
│  • Cloudflare Workers, Deno: capability 기반 런타임                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 정의 | 예시 | 비유 |
|:---|:---|:---|:---|
| **Capability 토큰** | (객체 참조, 권한) 쌍의 불변 데이터 구조 | `cap = (file_ptr, {R, W})` | 호텔 키 카드 |
| **C-List (Capability List)** | 주체가 보유한 capability 집합 | 프로세스의 FD 테이블 | 지갑에 담긴 여러 키 |
| **Seal/Unseal** | capability를 사용자 공간에서 보호하기 위한 암호화 | 메모리 태그, 암호화 서명 | 키 카드 자기 스트라이프 |
| **Revocation** | capability 무효화 회수 | 시스템 콜, 중재자(Indirection) | 체크아웃 시 카드 반납 |

### Capability 구조

기본적인 Capability의 구조와 ACL과의 대비를 보자.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│              ACL vs Capability 구조 비교                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【ACL: 객체 중심】                                                       │
│  ────────────────────                                                   │
│                                                                         │
│    각 객체마다 "접근자-권한" 리스트 저장                                    │
│                                                                         │
│    File A: [(User1, RW), (User2, R), (User3, RWX)]                     │
│    File B: [(User2, RWX), (User3, R)]                                  │
│    Printer: [(User1, W), (User2, W)]                                   │
│                                                                         │
│  • 접근 확인: "User1이 File A에 접근 가능한가?" → File A의 ACL 검색 O(k)    │
│  • 권한 열거: "User1이 무엇을 할 수 있는가?" → 모든 객체의 ACL 검색 O(n)      │
│                                                                         │
│  【Capability: 주체 중심】                                                │
│  ────────────────────────                                               │
│                                                                         │
│    각 주체마다 "객체-권한" 리스트(C-List) 저장                              │
│                                                                         │
│    User1의 C-List: [(File A, RW), (Printer, W)]                        │
│    User2의 C-List: [(File A, R), (File B, RWX), (Printer, W)]           │
│    User3의 C-List: [(File A, RWX), (File B, R)]                        │
│                                                                         │
│  • 접근 확인: "User1이 File A에 접근 가능한가?" → User1의 C-List 검색 O(k)   │
│  • 권한 열거: "User1이 무엇을 할 수 있는가?" → User1의 C-List만 확인 O(1)    │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  비교 항목        │  ACL                 │  Capability            │ │
│  │  ─────────        │  ───                 │  ────────             │ │
│  │  저장 위치         │  객체 메타데이터        │  주체의 C-List        │ │
│  │  접근 확인 복잡도  │  O(k) (ACE 길이)     │  O(k) (C-List 길이)   │ │
│  │  권한 열거        │  O(n) (모든 객체 검색)  │  O(1) (C-List만)     │ │
│  │  권한 회수        │  쉬움 (ACL 수정)       │  어려움 (복사본 추적)   │ │
│  │  위임(Delegation) │  복잡 (권한 전파 필요)   │  쉬움 (토큰 전달)      │ │
│  │  대표적 구현      │  Unix, Windows        │  Kerberos, POSIX cap  │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** ACL은 객체가 "자신을 사용할 수 있는 사용자 목록"을 갖는 반면, Capability는 사용자가 "자신이 사용할 수 있는 객체 목록(C-List)"을 갖는다. 접근 확인 시간 복잡도는 둘 다 O(k)로 동일하지만, 권한 열거("User1이 무엇을 할 수 있는가?")는 Capability가 O(1)로 빠르다. 왜냐하면 User1의 C-List만 확인하면 되기 때문이다. 반면 ACL은 모든 객체의 ACL을 검색해야 한다. Capability의 가장 큰 단점은 회수(Revocation) 어려움이다. 한 번 발급된 토큰을 복사해서 여러 주체가 가질 수 있으므로, 토큰을 무효화하려면 모든 복사본을 찾아야 한다. 이를 해결하기 위해 중재자(Indirection) 패턴을 사용한다. 토큰은 직접 객체를 참조하는 대신, 중재자를 통해 간접 참조하게 하여, 중재자에서 회수를 수행한다.

### Capability 연산

Capability 기반 시스템에서 주체가 객체에 접근하는 의사코드는 다음과 같다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│               Capability 기반 접근 제어 알고리즘                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【데이터 구조】                                                           │
│  ────────────                                                           │
│                                                                         │
│  Capability = (ObjectPointer, Rights, Seal)                             │
│    - ObjectPointer: 객체를 참조하는 불변 포인터                              │
│    - Rights: {Read, Write, Execute, Delete} 등 권한 집합                     │
│    - Seal: 위조 방지 태그(하드웨어/암호화)                                   │
│                                                                         │
│  C-List[Subject]: Subject이 보유한 Capability 리스트                         │
│                                                                         │
│  【함수 access_with_capability(S, cap, r)】                                │
│  ──────────────────────────────────────────────                          │
│                                                                         │
│  입력: S = 주체(Subject)                                                   │
│       cap = Capability 토큰                                               │
│       r = 요청 연산(Requested Operation)                                   │
│                                                                         │
│  출력: 성공(Success) / 실패(Failure)                                       │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  1. Capability 유효성 검증                                             │ │
│  │     if cap이 S의 C-List에 없으면:                                     │ │
│  │       return Failure  // 훔친 토큰                                     │ │
│  │     if verify_seal(cap) == false then:                                │ │
│  │       return Failure  // 위조된 토큰                                   │ │
│  │                                                                      │ │
│  │  2. 권한 확인                                                          │ │
│  │     if r ∉ cap.Rights then:                                          │ │
│  │       return Failure  // 권한 부족                                    │ │
│  │                                                                      │ │
│  │  3. 객체 참조 확인                                                      │ │
│  │     if is_valid(cap.ObjectPointer) == false then:                     │ │
│  │       return Failure  // 객체가 이미 삭제됨                             │ │
│  │                                                                      │ │
│  │  4. 접근 허용                                                          │ │
│  │     return Success                                                  │ │
│  │                                                                      │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  【Capability 전달(Delegation)】                                           │
│  ──────────────────────────────────                                      │
│                                                                         │
│  # User1이 User2에게 File A 읽기 capability를 위임                             │
│  cap_file_A = lookup_capability(User1, "File A")                        │
│  cap_read_only = restrict_rights(cap_file_A, {Read})  # 쓰기 권한 제거    │
│  transfer_capability(User1, User2, cap_read_only)                        │
│  # User2의 C-List에 cap_read_only 추가                                     │
│                                                                         │
│  【중재자(Indirection) 패턴을 이용한 회수(Revocation)】                           │
│  ────────────────────────────────────────────────                        │
│                                                                         │
│  # Capability는 직접 객체를 참조하지 않고, 중재자(Indirector)를 참조           │
│  cap = (IndirectionID, Rights, Seal)                                     │
│                                                                         │
│  # 중재자 테이블: IndirectionID → 실제 ObjectPointer                       │
│  IndirectionTable:                                                       │
│    1 → File_A_Pointer                                                    │
│    2 → File_B_Pointer                                                    │
│    3 → Printer_Device                                                    │
│                                                                         │
│  # 회수: 중재자 테이블에서 항목만 삭제                                        │
│  revoke(IndirectionID = 1)  # File_A_Pointer를 NULL로 설정                  │
│  # ID 1을 참조하는 모든 capability가 무효화                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Capability 기반 접근은 (1) 토큰이 진짜인지(위조 여부), (2) 주체가 실제로 이 토큰을 가지고 있는지, (3) 토큰에 요청 권한이 있는지, (4) 객체가 여전히 존재하는지 확인한다. 위조 방지를 위해 하드웨어 태그 비트(MPU, 메모리 보호 유닛), 암호화 서명(HMAC), 또는 커널 공간에서만 접근 가능한 보호 영역에 capability를 저장한다. 중재자 패턴은 회수 문제를 해결하는 전형적 방법이다. 토큰이 객체를 직접 참조하는 대신, 중재자 ID를 참조하게 하면, 중재자 테이블에서 매핑만 삭제하면 해당 ID를 참조하는 모든 토큰이 한 번에 무효화된다. 단, 중재자 테이블 조회 오버헤드가 발생하고, 중재자가 단일 실패 지점(Single Point of Failure)이 될 수 있다.

### POSIX Capability

리눅스의 POSIX Capability는 전통적 root 권한을 세분화하여, 프로세스가 필요한 최소 권한만 갖도록 한다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│            리눅스 POSIX Capability                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【목적】                                                                │
│  ────────────                                                           │
│  • 전통적 root(UID 0) 권한을 세분화                                       │
│  • 프로세스가 필요한 최소 권한만 갖도록(least privilege)                        │
│  • setuid 바이너리 실행 파일의 보안 취약점 완화                               │
│                                                                         │
│  【주요 Capability 목록 (36개, Linux 5.x 기준)】                           │
│  ────────────────────────────────────────────────                        │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  Capability              │  설명                                   │ │
│  │  ──────────              │  ────                                   │ │
│  │  CAP_CHOWN              │  chown() 시 UID/GID 변경 가능             │ │
│  │  CAP_DAC_OVERRIDE       │  파일 접근 권한(DAC) 무시 가능               │ │
│  │  CAP_DAC_READ_SEARCH    │  읽기 권한 없는 파일/디렉터리 검색 가능        │ │
│  │  CAP_FOWNER              │  파일 소유자 권한 조작 가능                 │ │
│  │  CAP_FSETID              │  setuid/setgid 비트 설정 가능              │ │
│  │  CAP_KILL                │  시그널을 임의 프로세스에 전송 가능            │ │
│  │  CAP_SETGID              │  setgid(), GID 변경 가능                │ │
│  │  CAP_SETUID              │  setuid(), UID 변경 가능                │ │
│  │  CAP_SETPCAP             │  다른 프로세스의 capability 조작 가능       │ │
│  │  CAP_LINUX_IMMUTABLE    │  IMMUTABLE/APPEND 파일 속성 변경 가능      │ │
│  │  CAP_NET_BIND_SERVICE   │  1024 이하 포트 바인드 가능                │ │
│  │  CAP_NET_BROADCAST       │  소켓 브로드캐스트 가능                     │ │
│  │  CAP_NET_RAW             │  RAW 소켓, PACKET 소켓 생성 가능          │ │
│  │  CAP_SYS_MODULE          │  커널 모듈(ko) 로드/언로드 가능             │ │
│  │  CAP_SYS_ADMIN           │  모든 시스템 관리 작업 가능                │ │
│  │  CAP_SYS_PTRACE          │  ptrace()로 임의 프로세스 추적 가능         │ │
│  │  CAP_SYS_RAWIO           │  RAW I/O操作(디스크 직접 접근) 가능       │ │
│  │  CAP_SYS_TIME            │  시스템 클럭 변경 가능                     │ │
│  │  CAP_SYS_TTY_CONFIG      │  tty 장치 설정 가능                       │ │
│  │  CAP_SYS_NICE            │  nice(), setpriority()로 우선순위 변경    │ │
│  │  CAP_SYS_RESOURCE        │  리소스 한계(quota) 설정 가능              │ │
│  │  CAP_AUDIT_CONTROL       │  감사 시스템 제어 가능                     │ │
│  │  CAP_AUDIT_READ          │  감사 로그 읽기 가능                      │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  【관리 도구】                                                            │
│  ────────────                                                           │
│                                                                         │
│  # 현재 프로세스의 capability 확인                                          │
│  $ capsh --print                                                       │
│  Current: = cap_chown,cap_dac_override,...+ep                            │
│                                                                         │
│  # 파일의 capability 설정                                                  │
│  $ sudo setcap cap_net_bind_service=+ep /usr/bin/nginx                   │
│  # nginx는 root가 아니어도 80포트 바인드 가능                                 │
│                                                                         │
│  # capability 확인                                                        │
│  $ getcap /usr/bin/nginx                                               │
│  /usr/bin/nginx = cap_net_bind_service+ep                               │
│                                                                         │
│  # capability 제거                                                        │
│  $ sudo setcap -r /usr/bin/ping                                        │
│                                                                         │
│  【capability 비트 플래그】                                                │
│  ────────────────────────────                                            │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  플래그  │  설명                                   │ 예시              │ │
│  │  ────  │  ────                                   │ ────              │ │
│  │  e (Effective) │  실행 중 유효한 capability               │ cap_net_bind_service+e │
│  │  p (Permitted)  │  프로세스가 획득 가능한 capability       │ cap_net_raw+p     │
│  │  i (Inheritable)│  execve() 후 자식에게 상속될 capability │ cap_setuid+i      │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 전통적으로 `ping`은 ICMP RAW 소켓을 생성하려 root 권한이 필요했다. 하지만 POSIX Capability가 도입된 후, `ping` 바이너리에 `cap_net_raw+ep`를 설정하면 일반 사용자도 실행 가능하다. `+ep`의 `e`(Effective)는 실행 중 유효함을, `p`(Permitted)은 프로세스가 이 capability를 획득할 수 있음을 의미한다. `+pi`로 설정하면 `execve()` 후 자식 프로세스에 이 capability가 상속된다. 예를 들어, 웹 서버가 80포트(특권 포트)를 바인드하려면 `CAP_NET_BIND_SERVICE`가 필요하다. Apache/Nginx는 초기에 root로 실행하여 80포트를 바인드한 후, `setuid()`로 일반 사용자로 권한을 낮춘다. POSIX Capability를 사용하면 처음부터 일반 사용자로 실행하면서도 80포트를 바인드할 수 있어 보안이 강화된다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교 1: Capability 기반 시스템 비교

| 시스템 | 특징 | Capability 구현 | 사용 사례 |
|:---|:---|:---|:---|
| **E 시스템** | Capability 기반 언어 | 모든 자원 접근이 capability로만 | 연구용 OS |
| **KeyKOS** | 상업용 capability OS | 키 복사 불가, 회수 지원 | 금융 시스템 |
| **Capsicum** | FreeBSD 샌드박스 | capability mode 제한 | 샌드박스 앱 |
| **WASM** | 웹 샌드박스 | capability 기반 import | Cloudflare Workers |
| **POSIX cap** | 리눅스 root 세분화 | process capability set | 서비스 프로세스 |

### 비교 2: ACL vs Capability 선택 가이드

```text
┌─────────────────────────────────────────────────────────────────────────┐
│          ACL vs Capability 선택 가이드                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  상황                          │  추천 방식         │  이유            │ │
│  │  ────────────────────────────│  ────────         │  ────            │ │
│  │  파일 시스템 권한 관리         │  ACL              │  객체 중심,       │ │
│  │  (Unix, Windows)              │                   │  관리 직관적      │ │
│  │                                                         │             │
│  │  분산 시스템 인증/권한 위임     │  Capability        │  토큰 전달 용이,   │ │
│  │  (Kerberos, OAuth)            │                   │  중앙 서버 불필요  │ │
│  │                                                         │             │ │
│  │  마이크로커널 IPC             │  Capability        │  메시지로 토큰 전달 │ │
│  │  (Mach, seL4)                 │                   │  경량화           │ │
│  │                                                         │             │ │
│  │  샌드박스 앱                  │  Capability        │  최소 권한만 부여  │ │
│  │  (Capsicum, WASM)             │                   │  격리 강화         │ │
│  │                                                         │             │ │
│  │  웹 서버 특권 포트 바인드      │  POSIX Capability  │  root 권한 불필요 │ │
│  │  (80/443)                    │                   │                   │ │
│  │                                                         │             │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 과목 융합 관점

- **컴퓨터 구조**: 하드웨어 capability 시스템(예: Plessey System 250)은 메모리에 태그 비트를 추가하여, 포인터가 capability인지 일반 데이터인지 하드웨어로 구분한다. CHERI( Capability-Hardware Enhanced RISC Instructions)는 ARMv8-A/RISC-V에 capability를 하드웨어 수준에서 지원한다.
- **프로그래밍 언어**: Rust/Python의 객체 참조도 일종의 capability다. 소유자(Owner)만 객체에 접근할 수 있고, 참조가 드롭되면 자동으로 회수된다. 이를 **linear type**이라고 한다.
- **분산 시스템**: Kerberos 티켓, AWS IAM 임시 자격 증명(STS), OAuth 2.0 Access Token도 capability의 일종이다. JSON Web Token(JWT)은 self-contained capability로, 서버 상태 없이(stateless) 검증 가능하다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 웹 서버를 일반 사용자로 실행하면서 80포트 바인드**: Apache를 root가 아닌 `www-data` 사용자로 실행하되, 80포트(특권 포트)를 바인드해야 한다. 아키텍트는 (1) `setcap cap_net_bind_service=+ep /usr/bin/apache2`로 capability 부여, (2) systemd 서비스에서 `User=www-data` 지정, (3) Apache는 root 없이도 80포트 바인드 가능, (4) 공격자가 Apache를 장악해도 root 권한 탈취 불가, (5) `getcap`으로 확인 및 감사 로그 남긴다.

2. **시나리오 — 샌드박스 앱에서 최소 권한 원칙 구현**: Capsicum(FreeBSD)로 PDF 뷰어를 샌드박스에 가두고, 파일 시스템 접근을 제한한다. 아키텍트는 (1) `cap_enter()`로 capability mode 진입, (2) `cap_rights_limit()`으로 파일 디스크립터의 권한 제한(예: 읽기만), (3) `cap_ioctls_limit()`으로 허용된 ioctl 목록 제한, (4) 샌드박스 밖으로 탈출 시도 시 `ECAPMODE` 에러 반환, (5) `pledge`(OpenBSD)와 함께 사용하여 추가 보호 강화.

3. **시나리오 — Kubernetes Pod에서 최소 권한 구성**: 컨테이너에 불필요한 capability을 제거하여 공격 표면 최소화. 아키텍트는 (1) Pod 매니페스트에서 `spec.containers.securityContext.capabilities.drop: [ALL]`로 모든 capability 박탈, (2) 필요한 최소 capability만 추가(`add: [NET_BIND_SERVICE]`), (3) `readOnlyRootFilesystem: true`로 루트 읽기 전용, (4) `allowPrivilegeEscalation: false`로 권한 상승 금지, (5) Open Policy Agent(OPA) Gatekeeper로 정책 강제.

### 도입 체크리스트

- **기술적**: 모든 daemon 프로세스가 root로 실행되지 않는가? POSIX Capability로 최소 권한만 부여되는가? 불필요한 setuid 바이너리를 제거했는가?
- **운영·보안적**: capability 부여가 감사 로그에 기록되는가? 정기적 보안 audit로 과도한 capability 부여를 검사하는가?

### 안티패턴

- **setuid root 바이너리 남용**: `ping`, `sudo` 같은 setuid 바이너리는 버퍼 오버플로우 시 root 권한 탈취 경로가 된다. POSIX Capability로 대체해야 한다.
- **모든 capability 부여**: `cap_setpcap` 등 모든 capability를 부여하면 root와 다를 바 없다. 최소 권한 원칙을 따라야 한다.
- **capability 확인 누락**: `getcap`으로 정기적으로 확인하지 않으면, 보안 팀의 승인 없이 추가된 capability를 발견하지 못할 수 있다.
- **중재자 패턴 미사용**: 회수가 필요한 상황에서 직접 참조 capability를 사용하면, 회수가 불가능해진다. 중재자(Indirection) 패턴을 적용해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 최적화 전 | 최적화 후 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | daemon이 root로 실행, 보안 위험 | POSIX Capability로 최소 권한만 부여 | **권한 상승 취약점 75% 감소** |
| **정량** | setuid 바이너리 다수, 공격 표면 넓음 | capability로 대체, setuid 제거 | **SUID exploits 위험 90% 감소** |
| **정성** | 샌드박스 미구현, 프로세스 격리 미흡 | Capsicum/WASM 기반 샌드박스 | **격리 강화**, 공격 표면 최소화 |

### 미래 전망

- **CHERI (Capability-Hardware Enhanced RISC Instructions)**: ARMv8-A와 RISC-V에 capability를 하드웨어 명령어와 메모리 태그로 지원하여, C/C++ 메모리 안전성(버퍼 오버플로우, Use-After-Free)을 원천 차단한다.
- **Cloudflare Workers, V8 Isolates**: capability 기반 JavaScript 샌드박스로, 수백만 개의 worker를 안전하게 실행한다.
- **object-capability model in Rust**: 타입 시스템에 capability를 통합하여, 컴파일 타임에 메모리 안전성을 보장한다.

### 참고 표준

- **POSIX 1003.1e**: capability 표준 (취소되었으나 구현에 영향)
- **Draft POSIX.1e Capabilities**: 리눅스 `capabilities(7)` 매뉴얼
- **Capsicum: Practical Capabilities for UNIX**: FreeBSD capsicum(4)

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [접근 제어 행렬](./610_access_matrix.md) → Capability의 기반 모델
- [ACL](./611_acl.md) → 객체 중심 대안
- [RBAC](./613_rbac.md) → 역할 기반 확장
- [POSIX Capability](./612_posix_capability.md) → 리눅스 capability 상세
- [Capsicum](./622_capsicum.md) → FreeBSD 샌드박스
- [CHERI](./623_cheri.md) → 하드웨어 capability
- [Kerberos](./624_kerberos.md) → 분산 capability(티켓)

### 👶 어린이를 위한 3줄 비유 설명

**개념**: Capability는 **호텔 키 카드** 같아요! 내가 가진 키 카드에 내가 들어갈 수 있는 방(객체)과 할 수 있는 것(권한)이 다 적혀 있어요.

**원리**: 키 카드를 프런트에 제시하면 객실에 들어갈 수 있어요. 카드를 친구에게 빌려줄 수도 있고(Delegation), 체크아웃 시에는 반납해야 해요(Revocation).

**효과**: 키 카드를 분실했을 때 누가 카드를 가졌는지 확인하는 것보다, 카드만 있으면 방에 들어갈 수 있어서 빨라요! 내가 무엇을 할 수 있는지 카드만 보면 돼서 편리해요.
