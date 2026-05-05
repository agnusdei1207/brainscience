+++
title = "043. 보호와 보안 (Protection & Security)"
weight = 43
date = "2026-04-05"
[extra]
categories = "studynote-operating-system"
+++

## 0. 핵심 인사이트

> **핵심**: 보호와 보안 (Protection & Security)은(는) 운영체제가 자원을 추상화하고 통제하는 과정에서 성능, 보호, 응답성을 동시에 조율하기 위해 필요한 핵심 개념이다.
> **비유**: 보호와 보안 (Protection & Security)은(는) 복잡한 교통을 한 번에 통제해 전체 흐름을 맞추는 신호 체계와 같다.

---

📝 모범 답안

## 1. 개요 및 필요성

```
보호 (Protection):
  목적: 프로세스/사용자 간 리소스 격리 및 접근 제어
  대상: 내부 위협 (프로그램 오류, 권한 오남용)
  메커니즘: 하드웨어 + OS 커널 기능
  예: 프로세스 A가 프로세스 B의 메모리 접근 방지

보안 (Security):
  목적: 시스템 전체를 외부 위협으로부터 방어
  대상: 외부 위협 (해커, 악성코드, DoS)
  메커니즘: 인증, 암호화, 방화벽, 감사
  예: 네트워크 침입 탐지, 악성코드 차단

계층 관계:
  보안 (Security) ⊃ 보호 (Protection)

  외부 위협 방어 (보안)
        ↓
  내부 접근 제어 (보호)
        ↓
  하드웨어 격리 (링 구조, MMU)

OS 보안 요구사항 (CIA):
  C - Confidentiality (기밀성): 인가된 자만 읽기
  I - Integrity (무결성): 인가된 방식으로만 수정
  A - Availability (가용성): 서비스 지속 제공
```

> 📢 **섹션 요약 비유**: 보호 vs 보안은 건물 내부 잠금 vs 외벽 보안 — 보호는 내부 회의실 문 잠금(내부 격리), 보안은 외부 침입자 방어(외벽, CCTV).

---

## 2. 구성요소

```
보호 도메인 (Protection Domain):
  주체(Subject)가 가진 권한 집합

  도메인 D = { (객체, 권한) 쌍의 집합 }

  예:
  Domain 1 (root): { (file1, rw), (file2, rwx), (mem, rw) }
  Domain 2 (user): { (file1, r), (file3, rw) }

접근 행렬 (Access Matrix):
  행: 도메인 (주체)
  열: 객체 (파일, 포트, 메모리 세그먼트)
  셀: 허용 권한 집합

         | 파일A | 파일B | 프린터 | 세그먼트1
---------+-------+-------+--------+----------
도메인1  |  rw   |  rwx  |  print |   rw
도메인2  |   r   |       |        |    r
도메인3  |       |  rx   |  print |

구현 방법:

1. ACL (Access Control List) — 열 기준:
   파일A: { (도메인1, rw), (도메인2, r) }
   장점: 객체별 접근자 목록 관리 쉬움
   단점: 특정 주체의 모든 권한 확인 어려움

2. Capability List — 행 기준:
   도메인1: { (파일A, rw), (파일B, rwx), (프린터, print) }
   장점: 주체 관점에서 권한 관리
   단점: 권한 취소(revoke) 어려움
```

> 📢 **섹션 요약 비유**: 접근 행렬은 학교 열쇠 관리 장부 — ACL은 "이 강의실에 들어갈 수 있는 사람" 목록, Capability는 "이 사람이 열 수 있는 강의실" 목록.

---

## 3. 구조 및 원리

**핵심 조건**: 운영체제의 해당 메커니즘은 현재 상태 정보, 자원 제약, 정책 기준이 함께 정합성을 가질 때 안정적으로 동작한다.

동작 순서:
1. **요청 또는 이벤트 발생**: 사용자 요청, 인터럽트, 시스템 호출 등으로 커널이 해당 기능을 처리할 필요가 생긴다.
2. **현재 상태 확인**: 커널은 큐, 제어 블록, 메타데이터, 자원 가용량을 확인해 실행 가능 여부와 우선순위를 판단한다.
3. **정책 적용 및 자원 배정**: 해당 주제의 핵심 정책에 따라 상태 전이, 자원 할당, 보호 검사를 수행한다.
4. **결과 반영 및 후속 처리**: 처리 결과를 시스템 상태에 기록하고 다음 인터럽트·스케줄링·복구 단계로 연결한다.

```
x86 CPU 링 구조 (Privilege Levels):

Ring 0 — 커널 모드 (Kernel Mode):
  최고 권한
  모든 명령어 실행 가능
  하드웨어 직접 접근
  OS 커널, 디바이스 드라이버 핵심 부분

Ring 1, 2 — (현재 대부분 미사용):
  원래 OS 서비스, 드라이버용
  현대 OS: Ring 0/3 양분 구조

Ring 3 — 사용자 모드 (User Mode):
  최소 권한
  특권 명령어 실행 불가
  I/O 직접 접근 불가
  일반 응용 프로그램

권한 이동:
  Ring 3 → Ring 0:
    시스템 콜 (INT, SYSCALL 명령어)
    예외 처리 (Exception Handler)
    인터럽트 (Interrupt)

  Ring 0 → Ring 3:
    IRET, SYSRET 명령어
    스케줄러에 의한 사용자 프로세스 복귀

보호 메커니즘:
  특권 명령어: Ring 0에서만 실행
    (LGDT, LIDT, IN/OUT, HLT, MOV CR0 등)
  메모리: 페이지 테이블로 Ring 3 접근 격리
  I/O: IOPL(I/O Protection Level) 비트로 제어

가상화와 Ring:
  VMware/VirtualBox: Ring -1 (Hypervisor)
  Intel VT-x: VMX root/non-root 모드
```

> 📢 **섹션 요약 비유**: 링 구조는 군대 계급 — Ring 0은 사령관(모든 명령 가능), Ring 3은 일반 병사(기본 임무만). 계급 외 명령 실행 → 즉시 처벌(예외 발생).

---

## 4. 비교 및 연결

```
x86 CPU 링 구조 (Privilege Levels):

Ring 0 — 커널 모드 (Kernel Mode):
  최고 권한
  모든 명령어 실행 가능
  하드웨어 직접 접근
  OS 커널, 디바이스 드라이버 핵심 부분

Ring 1, 2 — (현재 대부분 미사용):
  원래 OS 서비스, 드라이버용
  현대 OS: Ring 0/3 양분 구조

Ring 3 — 사용자 모드 (User Mode):
  최소 권한
  특권 명령어 실행 불가
  I/O 직접 접근 불가
  일반 응용 프로그램

권한 이동:
  Ring 3 → Ring 0:
    시스템 콜 (INT, SYSCALL 명령어)
    예외 처리 (Exception Handler)
    인터럽트 (Interrupt)

  Ring 0 → Ring 3:
    IRET, SYSRET 명령어
    스케줄러에 의한 사용자 프로세스 복귀

보호 메커니즘:
  특권 명령어: Ring 0에서만 실행
    (LGDT, LIDT, IN/OUT, HLT, MOV CR0 등)
  메모리: 페이지 테이블로 Ring 3 접근 격리
  I/O: IOPL(I/O Protection Level) 비트로 제어

가상화와 Ring:
  VMware/VirtualBox: Ring -1 (Hypervisor)
  Intel VT-x: VMX root/non-root 모드
```

> 📢 **섹션 요약 비유**: 링 구조는 군대 계급 — Ring 0은 사령관(모든 명령 가능), Ring 3은 일반 병사(기본 임무만). 계급 외 명령 실행 → 즉시 처벌(예외 발생).

---

## 5. 실무 적용 및 판단

```
OS 보안 위협 분류:

악성코드 (Malware):
  바이러스: 다른 프로그램에 기생, 자기 복제
  웜: 독립 실행, 네트워크 전파
  트로이 목마: 정상 프로그램으로 위장
  랜섬웨어: 파일 암호화 후 몸값 요구

권한 상승 공격:
  버퍼 오버플로우: 스택 리턴 주소 덮어쓰기
  → 셸코드 실행 → Root 권한 탈취
  대응: ASLR(주소 공간 레이아웃 랜덤화), DEP(데이터 실행 방지), Stack Canary

레이스 컨디션 (Race Condition):
  TOCTOU(Time-Of-Check-To-Time-Of-Use)
  권한 확인과 실제 사용 사이의 시간차 악용
  대응: 원자적 연산, 잠금(Lock) 사용

사이드 채널 공격:
  Spectre, Meltdown (2018):
    CPU 투기적 실행 → 캐시 타이밍 측정 → 비밀 데이터 추출
  대응: OS 패치, KPTI(Kernel Page Table Isolation)

보안 메커니즘:
  인증 (Authentication): 비밀번호, 생체인식, 2FA
  인가 (Authorization): DAC/MAC/RBAC
  감사 (Auditing): 접근 로그, SIEM
  암호화: 파일 시스템 암호화 (BitLocker, LUKS)
```

> 📢 **섹션 요약 비유**: OS 보안 위협은 건물 침입 방법 — 정문 뚫기(인증 우회), 창문 깨기(버퍼 오버플로우), 청소부 위장(트로이 목마), 열쇠 복사(자격증명 도용).

---

## 6. 기대효과 및 결론

```
Linux 강제 접근 제어 (MAC) 구현:

DAC (Discretionary Access Control) 한계:
  파일 소유자가 권한 부여 결정
  root 계정 탈취 시 모든 파일 접근 가능
  → Linux 전통 rwx 권한의 한계

MAC (Mandatory Access Control):
  시스템 정책이 모든 접근 제어
  소유자도 정책 외 권한 부여 불가

SELinux (Security-Enhanced Linux):
  NSA 개발, Red Hat/CentOS/Fedora 기본 탑재
  레이블 기반: 모든 파일/프로세스에 보안 컨텍스트

  컨텍스트 형식: user:role:type:level
  예: system_u:system_r:httpd_t:s0

  정책 유형:
    Enforcing: 정책 위반 = 차단 + 로그
    Permissive: 차단 없음 + 로그만 (개발/디버깅)
    Disabled: 비활성화

AppArmor (Ubuntu/SUSE):
  경로 기반 프로파일
  더 간단, 관리 편이

  /etc/apparmor.d/usr.sbin.nginx 예시:
    /var/www/html/** r,
    /var/log/nginx/** w,
    network tcp,

실무 적용:
  웹서버(Apache/Nginx)에 SELinux 프로파일 적용
  → 웹 디렉토리 외 파일 접근 자동 차단
  → 명령 실행(system()) 차단
  → 취약점 악용 시 피해 최소화 (컨테인먼트)
```

> 📢 **섹션 요약 비유**: SELinux는 회사 보안 시스템 — 팀장(root)도 다른 팀 서버실에 못 들어가는 것처럼, 역할(Role)과 유형(Type)으로 최소 권한 강제.

---

## 7. 발전 흐름도

```
[초기 OS 보호 (1960s~)]
IBM System/360: 특권 모드 도입
멀틱스: 링 구조 최초 구현
      |
      v
[Unix 권한 모델 (1970s)]
DAC: rwx + 소유자/그룹/기타
      |
      v
[보안 확장 (1980s~90s)]
Orange Book (TCSEC): 보안 등급화
NSA: B3급 OS 연구 → SELinux 기반
      |
      v
[Linux 보안 (2000s)]
SELinux (2000, 2003 커널 통합)
AppArmor (2006, Ubuntu 통합)
      |
      v
[현재: 컨테이너 보안]
seccomp: 시스템 콜 필터링
cgroups + namespace: 컨테이너 격리
eBPF: 커널 내 보안 프로그램 실행
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 보호와 보안 (Protection & Security) | 운영체제 자원 관리와 보호 정책이 실제로 적용되는 핵심 주제 |
| 커널 (Kernel) | 정책 집행, 상태 전이, 시스템 호출 처리의 중심 |
| 프로세스/스레드 | CPU, 메모리, 동기화 자원과 직접 연결되는 실행 단위 |
| 메모리/I/O | 성능 병목과 보호 요구사항이 함께 드러나는 연계 영역 |
| 가상화/보안 | 격리, 제어, 관측 확장 관점에서 해당 주제가 연결되는 상위 개념 |
