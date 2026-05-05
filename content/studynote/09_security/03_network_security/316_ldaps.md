+++
weight = 316
title = "316. LDAPS — SSL/TLS 적용 LDAP (LDAP over SSL/TLS)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: LDAPS (LDAP over SSL/TLS)는 평문 LDAP 트래픽을 SSL/TLS (Secure Sockets Layer/Transport Layer Security)로 암호화해 도청(Eavesdropping)과 중간자 공격(MITM, Man-in-the-Middle)을 방어하는 보안 강화 방식이다.
> 2. **가치**: 사용자 패스워드와 디렉터리 데이터가 네트워크 상에서 암호화되어 전송되므로, 공격자가 네트워크 패킷을 캡처해도 인증 정보를 탈취할 수 없다.
> 3. **판단 포인트**: LDAPS(포트 636)와 StartTLS(포트 389 + STARTTLS 업그레이드)의 차이, 인증서 검증(Certificate Validation) 적용 여부가 기술사 시험의 핵심 구분점이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

LDAP는 기본적으로 TCP 389번 포트를 사용하며, 모든 데이터를 평문(Plaintext)으로 전송한다. 이는 네트워크 내부에서 Wireshark 같은 패킷 캡처 도구만 있으면 사용자 ID, 패스워드, 조직 구조 전체가 그대로 노출된다는 의미다. 특히 관리자 계정(Bind DN)의 패스워드가 평문으로 흘러다니는 환경은 내부자 공격과 APT (Advanced Persistent Threat) 침투 경로가 된다.

이를 해결하기 위해 두 가지 방식이 존재한다. 하나는 LDAPS로, SSL/TLS 래퍼(Wrapper) 위에서 처음부터 암호화 채널을 통해 LDAP를 실행하는 방식이다(포트 636). 다른 하나는 StartTLS로, 평문 포트 389에서 연결을 시작한 뒤 `STARTTLS` 명령으로 암호화 채널로 업그레이드하는 방식이다. 두 방식 모두 TLS를 활용하지만 동작 흐름이 다르다.

보안 정책상 평문 LDAP 트래픽은 반드시 차단하고, 모든 디렉터리 서비스 통신을 LDAPS 또는 StartTLS로 강제해야 한다. ISMS-P, ISO 27001 등 각종 보안 인증에서도 전송 구간 암호화는 필수 요건으로 규정된다.

📢 **섹션 요약 비유**: 평문 LDAP는 엽서로 연애편지를 보내는 것이다. 우편배달부도, 이웃도 내용을 읽을 수 있다. LDAPS는 봉인 밀봉 봉투에 넣어 보내는 것으로, 수신자만 열어볼 수 있다.

---

## 2. 구성요소

### LDAPS vs StartTLS 동작 흐름 비교

```
LDAPS (포트 636):
클라이언트                           LDAP 서버
    │                                    │
    │──── TCP Connect → 포트 636 ────────►│
    │◄─── TLS Handshake (즉시 시작) ─────│
    │      (인증서 교환 / 세션키 협상)    │
    │◄─── 암호화 채널 수립 완료 ─────────│
    │──── LDAP Bind (암호화됨) ──────────►│
    └────────────────────────────────────┘

StartTLS (포트 389):
클라이언트                           LDAP 서버
    │                                    │
    │──── TCP Connect → 포트 389 ────────►│
    │──── LDAP 평문 연결 수립 ───────────►│
    │──── Extended Request: STARTTLS ────►│
    │◄─── Extended Response: Success ────│
    │◄─── TLS Handshake 시작 ────────────│
    │◄─── 암호화 채널 수립 완료 ─────────│
    │──── LDAP Bind (암호화됨) ──────────►│
    └────────────────────────────────────┘
```

### 핵심 비교 표

| 항목 | LDAPS | StartTLS |
|:---|:---|:---|
| 포트 | 636 | 389 |
| 암호화 시작 시점 | 연결 즉시 | STARTTLS 명령 후 |
| 초기 평문 노출 | 없음 | STARTTLS 이전 메타데이터 일부 노출 |
| RFC 표준 | 비공식(RFC 없음, 관행) | RFC 2830 공식 표준 |
| 방화벽 구성 | 단일 포트(636) 허용 | 389 포트 허용 필요 |
| 다운그레이드 공격 위험 | 없음 | STARTTLS 가로채기 가능성 존재 |
| 권고 사항 | 레거시 환경, 단순 구성 | 최신 표준, 유연한 암호화 |

### 인증서(Certificate) 설정 흐름

```
┌─────────────────────────────────────────────┐
│            LDAPS 인증서 체인                 │
│                                             │
│  CA (Certificate Authority) 루트 인증서     │
│       │                                     │
│       ▼                                     │
│  중간 CA (Intermediate CA) 인증서           │
│       │                                     │
│       ▼                                     │
│  LDAP 서버 인증서                           │
│  - Subject: CN=ldap.example.com             │
│  - SAN: ldap.example.com                   │
│  - Key Usage: serverAuth                   │
│                                             │
│  클라이언트 검증 단계:                      │
│  1. 인증서 체인 신뢰 확인                   │
│  2. 인증서 만료일 확인                      │
│  3. CRL/OCSP로 인증서 폐기 여부 확인        │
│  4. 호스트명 일치 확인 (CN/SAN)             │
└─────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: LDAPS는 "처음부터 은행 금고실 안에서 대화하는" 방식이고, StartTLS는 "일반 방에서 대화하다가 중간에 방음 부스로 이동하는" 방식이다. StartTLS는 이동 중에 도청되는 위험이 남아 있다.

---

## 3. 구조 및 동작 원리

### 인증서 검증 수준별 보안 차이

| 검증 수준 | 설정 예시 | 보안 강도 | 위험 |
|:---|:---|:---:|:---|
| 검증 없음 (TLS_REQCERT never) | OpenLDAP 클라이언트 설정 | 낮음 | MITM 공격에 완전 무방비 |
| 서버 인증서만 검증 | TLS_REQCERT demand | 중간 | 자체 서명 인증서 오류 주의 |
| 상호 인증 (mTLS) | TLS_REQCERT hard + 클라이언트 인증서 | 높음 | 인증서 관리 복잡도 증가 |

### 관련 프로토콜 및 표준 연결

| 항목 | 설명 |
|:---|:---|
| RFC 2830 | StartTLS for LDAPv3 표준 |
| RFC 4513 | LDAP 인증 메커니즘 및 보안 고려사항 |
| SASL (Simple Authentication and Security Layer) | GSSAPI/Kerberos 등 다양한 인증 메커니즘 적용 |
| CRL (Certificate Revocation List) | 폐기된 인증서 목록 |
| OCSP (Online Certificate Status Protocol) | 실시간 인증서 유효성 확인 |

📢 **섹션 요약 비유**: 인증서 검증을 끄는 것은 신분증 없이 출입을 허가하는 것과 같다. "나 직원이에요"라고 말만 하면 통과시키면 누구든 들어올 수 있다.

---

## 4. 비교 및 트레이드오프

### OpenLDAP LDAPS 설정 예시

```bash
# /etc/ldap/ldap.conf (클라이언트 설정)
URI     ldaps://ldap.example.com:636
BASE    dc=example,dc=com
TLS_CACERT  /etc/ssl/certs/ca-bundle.crt
TLS_REQCERT demand

# slapd.conf (서버 설정)
TLSCACertificateFile  /etc/ssl/certs/ca-bundle.crt
TLSCertificateFile    /etc/ssl/ldap/server.crt
TLSCertificateKeyFile /etc/ssl/ldap/server.key
TLSVerifyClient       demand
```

### 포트 차단 정책 적용

보안 정책 강화 시 방화벽에서 평문 포트 389를 완전 차단하고 636만 허용하는 방식을 권고한다. 그러나 레거시 애플리케이션이 389를 직접 사용하는 경우, StartTLS 강제화(ldap.conf: `TLS_REQCERT demand` + 서버에서 StartTLS 필수 설정)로 중간 단계 적용도 가능하다.

### 기술사 시험 판단 포인트

시험에서 "LDAP 보안 강화 방안"을 묻는 문제가 나올 때 핵심은 세 가지다: ① LDAPS/StartTLS로 전송 구간 암호화, ② 인증서 검증 강제(TLS_REQCERT demand), ③ 서비스 계정(Service Account) 최소 권한 적용. 인증서 검증을 `never`로 설정한 LDAPS는 암호화만 될 뿐 MITM 방어가 안 된다는 점을 반드시 언급해야 한다.

📢 **섹션 요약 비유**: TLS_REQCERT never는 봉투는 있지만 주소 확인을 안 하는 것이다. 내용은 숨겨지지만, 엉뚱한 사람한테 전달될 수 있다.

---

## 5. 실무 적용 및 최적화 기법

LDAPS 도입으로 조직은 디렉터리 서비스 전 구간의 기밀성(Confidentiality)과 무결성(Integrity)을 확보한다. 패킷 스니핑(Packet Sniffing)으로 관리자 패스워드를 탈취하는 가장 단순한 내부자 공격이 원천 차단된다. 또한 상호 인증(mTLS, mutual TLS) 적용 시 클라이언트 위·변조도 방어할 수 있다.

인증서 관리 비용(CA 운영, 인증서 갱신 자동화)이 추가되지만, 이는 Let's Encrypt나 내부 PKI (Public Key Infrastructure) 자동화로 충분히 감당 가능하다. 핵심은 "암호화했다"는 사실보다 "올바른 서버와 통신하고 있는지 검증한다"는 인증서 체인 신뢰가 보안의 실질적 가치임을 이해하는 것이다.

📢 **섹션 요약 비유**: LDAPS는 안전한 택배 시스템이다. 봉투를 봉인하고(암호화), 배달 주소를 확인하고(인증서 검증), 서명을 받는(무결성) 세 단계가 모두 있어야 진짜 안전하다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| LDAP | 기반 프로토콜 | 평문 디렉터리 접근, 포트 389 |
| SSL/TLS | 암호화 레이어 | LDAP 트래픽을 감싸는 보안 계층 |
| StartTLS | 대안 방식 | 평문 연결 후 암호화 업그레이드, RFC 2830 |
| PKI (Public Key Infrastructure) | 인증서 관리 | CA, 인증서, CRL/OCSP 전체 체계 |
| MITM (Man-in-the-Middle) | 방어 대상 위협 | 암호화 미적용 시 패스워드 도청 |
| mTLS (mutual TLS) | 강화 옵션 | 서버 + 클라이언트 양방향 인증서 검증 |
| SASL (Simple Authentication and Security Layer) | 인증 레이어 | Kerberos 등 강력한 인증 메커니즘 연동 |

### 👶 어린이를 위한 3줄 비유 설명

- 평문 LDAP는 엽서로 패스워드를 보내는 것처럼 누구나 볼 수 있어.
- LDAPS는 봉투에 넣어 봉인하는 것처럼, 내용은 수신자만 볼 수 있어.
- 근데 봉투에 수신자 주소를 확인(인증서 검증)하지 않으면, 엉뚱한 사람한테 가는 거야.
