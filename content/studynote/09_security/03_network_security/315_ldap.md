+++
weight = 315
title = "315. LDAP — 디렉터리 서비스 접근 프로토콜 (Lightweight Directory Access Protocol)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: LDAP (Lightweight Directory Access Protocol)는 DAP (Directory Access Protocol)를 경량화한 RFC 4511 프로토콜로, 조직의 사용자·장치·정책 정보를 계층 트리 구조로 저장하고 조회하는 표준 디렉터리 서비스다.
> 2. **가치**: SSO (Single Sign-On), 이메일 주소록, 네트워크 장비 인증 등 중앙화된 신원 관리(Identity Management)의 백본(Backbone)으로, 수천 대 서버의 계정을 한 곳에서 제어할 수 있게 한다.
> 3. **판단 포인트**: DIT (Directory Information Tree) 구조와 DN (Distinguished Name) 표기법을 정확히 이해해야 LDAP 인젝션, LDAPS, Active Directory 연계 문제를 모두 풀 수 있다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

1980년대 X.500 표준이 정의한 DAP (Directory Access Protocol)는 강력했지만, OSI 7계층 전체를 구현해야 했기에 무겁고 복잡했다. 1993년 미시간 대학교에서 TCP/IP 위에서 동작하는 경량화 버전인 LDAP v2를 개발했고, 현재는 RFC 4511로 표준화된 LDAPv3가 사실상 표준이다.

LDAP의 존재 이유는 단순하다. 1,000명의 직원이 있는 기업에서 이메일 서버, VPN, ERP, 출입 시스템이 각각 독립된 계정 DB를 가지면 계정 동기화 문제, 퇴직자 계정 잔존, 패스워드 불일치가 필연적으로 발생한다. LDAP는 이 모든 시스템이 단일 디렉터리를 조회하게 해 IAM (Identity and Access Management)의 중앙화를 실현한다.

대표적인 구현체로는 Microsoft의 AD (Active Directory), 오픈소스인 OpenLDAP, Red Hat의 389 Directory Server가 있다. TCP 389번 포트(평문), TCP 636번 포트(LDAPS)를 사용한다.

📢 **섹션 요약 비유**: LDAP은 회사 전화번호부다. 영업팀, 개발팀, 임원 정보가 모두 한 책에 있고, 누구나 이름으로 검색하면 부서·번호·이메일을 찾을 수 있다. 다만 이 책에는 "누가 어디에 접근할 수 있는지"도 함께 적혀 있다.

---

## 2. 구성요소

### DIT (Directory Information Tree) 구조

LDAP는 데이터를 역방향 DNS처럼 트리(Tree) 형태로 구성한다.

```
DIT (Directory Information Tree)
│
└── dc=example,dc=com         (도메인 컴포넌트, Domain Component)
    │
    ├── ou=Users               (조직 단위, Organizational Unit)
    │   ├── cn=Alice           (공통 이름, Common Name)
    │   └── cn=Bob
    │
    ├── ou=Groups
    │   ├── cn=admins
    │   └── cn=developers
    │
    └── ou=Computers
        ├── cn=web-server-01
        └── cn=db-server-01
```

- **DC (Domain Component)**: `dc=example,dc=com` — 최상위 도메인 분리
- **OU (Organizational Unit)**: `ou=Users` — 논리적 그룹 단위
- **CN (Common Name)**: `cn=Alice` — 개별 객체 식별자
- **DN (Distinguished Name)**: 트리 루트까지의 전체 경로. 예: `cn=Alice,ou=Users,dc=example,dc=com`
- **RDN (Relative Distinguished Name)**: 부모 기준 상대 경로. 예: `cn=Alice`

### LDAP 기본 연산 요약

| 연산 | 설명 | 예시 |
|:---|:---|:---|
| Bind | 서버에 인증 (연결 수립) | 관리자 DN + 패스워드 제시 |
| Search | 필터(Filter) 기반 항목 조회 | `(uid=alice)` 검색 |
| Add | 새 항목 추가 | 신입 직원 계정 생성 |
| Modify | 기존 항목 수정 | 전화번호, 소속 변경 |
| Delete | 항목 삭제 | 퇴직자 계정 삭제 |
| Compare | 속성 값 비교 | 패스워드 검증 |
| Unbind | 연결 종료 | 세션 닫기 |

### LDAP 검색 필터 문법

```
기본 필터:     (속성=값)
AND:          (&(uid=alice)(ou=Users))
OR:           (|(uid=alice)(uid=bob))
NOT:          (!(uid=guest))
와일드카드:    (cn=A*)
복합 필터:    (&(objectClass=inetOrgPerson)(uid=alice))
```

📢 **섹션 요약 비유**: DIT는 회사 조직도다. DN은 "서울 본사 > 개발팀 > 이앨리스"처럼 위치를 전부 표기한 이름이고, RDN은 그냥 "이앨리스"라고 부르는 것이다.

---

## 3. 구조 및 동작 원리

### LDAP vs 관계형 DB (Relational Database)

| 비교 항목 | LDAP | 관계형 DB (RDBMS) |
|:---|:---|:---|
| 데이터 구조 | 계층 트리 | 테이블/행/열 |
| 최적 용도 | 읽기 집중(Read-Heavy) 조회 | 읽기/쓰기 균형 트랜잭션 |
| 스키마 유연성 | 객체 클래스 기반 확장 가능 | 엄격한 스키마 |
| 표준 쿼리 언어 | LDAP 필터(Filter) | SQL |
| 복제(Replication) | 다중 마스터 복제 지원 | 마스터-슬레이브 등 다양 |
| 인증 통합 | Kerberos, SASL 기본 지원 | 별도 구현 필요 |

### 주요 구현체 비교

| 구현체 | 제공사 | 특징 |
|:---|:---|:---|
| AD (Active Directory) | Microsoft | Kerberos + LDAP 통합, Windows 환경 표준 |
| OpenLDAP | 오픈소스 | 경량, Linux 환경 표준, 설정 복잡 |
| 389 Directory Server | Red Hat | RHEL/CentOS 기본 제공, 고가용성 지원 |
| Oracle Internet Directory | Oracle | Oracle DB 연동 최적화 |

📢 **섹션 요약 비유**: LDAP vs RDBMS는 전화번호부(빠른 이름 찾기) vs 회계 장부(복잡한 계산)의 차이다. 전화번호부는 이름 검색에 최적화되어 있고, 회계 장부는 숫자 계산에 특화되어 있다.

---

## 4. 비교 및 트레이드오프

### Linux 서버 LDAP 인증 통합 흐름

```
리눅스 서버 로그인 시도
    │
    ├── PAM (Pluggable Authentication Module)
    │   └── pam_ldap.so 호출
    │         │
    │         ▼
    │   LDAP 서버 (389/636 포트)
    │         │
    │         ├── Bind: 서비스 계정으로 서버 연결
    │         ├── Search: uid=사용자 검색
    │         └── Compare: 입력 패스워드 검증
    │
    └── NSS (Name Service Switch): uid/gid 매핑
```

### Active Directory 연계 고려사항

AD는 LDAP를 기반으로 구축되어 있어 LDAP 클라이언트로 AD에 쿼리할 수 있다. 그러나 기본 포트 389는 평문 전송이므로, 운영 환경에서는 반드시 LDAPS 636 또는 StartTLS를 사용해야 한다. 또한 AD는 글로벌 카탈로그(Global Catalog, GC)를 3268/3269 포트로 제공하며, 전체 포리스트(Forest) 대상 검색 시 이를 활용한다.

### 기술사 시험 판단 포인트

LDAP 관련 기술사 문제의 핵심은 두 가지다. 첫째, "중앙화된 인증 아키텍처"를 DIT 구조와 연결해 설명할 수 있는가. 둘째, LDAP 보안 취약점(LDAP 인젝션, 평문 전송)과 대응책(LDAPS, 입력 검증)을 짝지어 논술할 수 있는가.

📢 **섹션 요약 비유**: LDAP 통합 인증은 회사 출입증 시스템이다. 한 장의 카드로 사무실, 서버실, 식당을 모두 통과하지만, 권한은 카드에 등록된 직급에 따라 다르다.

---

## 5. 실무 적용 및 최적화 기법

LDAP 기반 중앙 디렉터리 서비스 도입으로 기업은 계정 관리 효율화, 보안 강화, 컴플라이언스(Compliance) 준수라는 세 가지 핵심 가치를 얻는다. 퇴직자 계정 즉시 비활성화, 권한 변경의 실시간 전파, 접근 로그 중앙 수집이 모두 단일 LDAP 디렉터리 수정으로 실현된다.

그러나 LDAP 서버 자체가 단일 실패점(SPOF, Single Point of Failure)이 되지 않도록 다중 마스터 복제(Multi-Master Replication)나 HA (High Availability) 구성이 필수다. 또한 LDAP는 평문 프로토콜이므로 반드시 LDAPS 또는 StartTLS와 함께 사용해야 한다.

디렉터리 서비스는 현대 기업 IT 인프라의 심장부다. 이것이 침해되면 모든 시스템 접근권이 동시에 노출되므로, LDAP 보안은 인프라 보안의 최우선 과제다.

📢 **섹션 요약 비유**: LDAP는 회사의 마스터 열쇠 보관함이다. 모든 문의 열쇠가 여기에 있으니, 보관함 자체의 보안이 가장 중요하고, 복사본(복제)도 안전하게 관리해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DAP (Directory Access Protocol) | LDAP의 원형 | OSI 기반 무거운 프로토콜, LDAP가 경량화 |
| DIT (Directory Information Tree) | LDAP 데이터 구조 | 계층 트리 형태의 디렉터리 구성 |
| DN (Distinguished Name) | 항목 식별자 | 트리 루트까지 전체 경로 표기 |
| RDN (Relative Distinguished Name) | 상대 식별자 | 부모 기준 상대 경로 |
| AD (Active Directory) | LDAP 구현체 | Kerberos + LDAP 통합 Microsoft 솔루션 |
| LDAPS | 보안 강화 | LDAP over SSL/TLS, 포트 636 |
| PAM (Pluggable Authentication Module) | Linux 인증 연동 | pam_ldap.so로 LDAP 인증 통합 |
| SSO (Single Sign-On) | 활용 사례 | LDAP 기반 중앙 인증으로 SSO 구현 |

### 👶 어린이를 위한 3줄 비유 설명

- LDAP는 학교 학생부야. 이름, 반, 번호, 동아리 가입 여부가 모두 한 장부에 있어.
- 선생님이 급식실, 도서관, 체육관 입장을 확인할 때 모두 이 학생부를 참고하는 거야.
- 학생이 전학 가면 학생부에서 지우면 모든 곳의 출입이 동시에 막혀. 정말 편리하지?
