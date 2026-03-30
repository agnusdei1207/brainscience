+++
weight = 6
title = "SMTP (Simple Mail Transfer Protocol)"
description = "이메일 전송의 핵심 프로토콜 SMTP의 동작, POP3/IMAP과의 관계를 다룬다."
date = 2024-02-06

[extra]
categories = ["studynote-software-engineering"]
topics = ["application-layer", "smtp", "email", "pop3", "imap"]
study_section = ["section-9-application-layer-web-email"]

number = "906"
core_insight = "SMTP는 이메일 전송을 담당하는 프로토콜로, 발신 MDA에서 수신 MDA로 메일을 전달하며, 수신자는 POP3/IMAP으로 메일을 조회한다."
key_points = ["SMTP (Port 25/587)", "POP3 vs IMAP", "SMTP AUTH", "SPF, DKIM, DMARC"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SMTP는 이메일을 발신 MTA에서 수신 MTA로 전달하는 전송 프로토콜로, TCP 25번(서버 간) 또는 587번(클라이언트→서버) 포트에서 동작한다.
> 2. **가치**: 글로벌 이메일 시스템의 핵심으로, 도메인 간 메일 전송을 표준화된 방법으로 처리한다.
> 3. **융합**: SMTP 보안(SMTP AUTH, STARTTLS)과 함께 이메일 인증(SPF, DKIM, DMARC)으로 스팸/피싱 방어에 활용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

**개념**: SMTP(Simple Mail Transfer Protocol)는 RFC 821(원본), RFC 5321(현재)로 표준화된 이메일 전송 프로토콜이다. 발신자의 메일 클라이언트가 SMTP 서버(MTA: Mail Transfer Agent)에 메일을 제출하면, SMTP는 도메인 간 DNS MX 레코드를 통해 수신자의 SMTP 서버로 메일을 전달한다. 수신자는 POP3(사서함에서 메일 가져오기) 또는 IMAP(사서함과 동기화)로 메일을 조회한다.

**필요성**: 이메일은 인터넷의 핵심 서비스로, 일상/business communication에서 필수적이다. SMTP는 이러한 이메일 전송의 표준 프로토콜로서, 서로 다른 메일 시스템 간의 상호운용성을 보장한다.

**비유**: SMTP는 **우체국 간 소포 전달 시스템**과 같다. 발신자 우체국(발신 SMTP)이 수신자 우체국(수신 SMTP)에 소포(메일)를 전달하고, 수신자는 우체국에 가서( POP3/IMAP) 소포를 가져간다.

**등장 배경**: 1982년 RFC 821로 처음 정의되었으며, 이후 SMTP AUTH, STARTTLS, IPv6 지원 등의 확장이 추가되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### SMTP 전송 과정

```
┌───────────────────────────────────────────────────────────────────────┐
│                    SMTP 메일 전송 과정                                    │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  [발신자]  ── SMTP (587) ──▶ [발신 SMTP Server (MTA)]               │
│                                        │                              │
│                                    DNS MX Query                       │
│                                        │                              │
│                                        ▼                              │
│                              [수신 SMTP Server (MTA)]                  │
│                                        │                              │
│                                        ▼                              │
│                              [수신자 Mailbox (MDA)]                   │
│                                        │                              │
│                                        ▼                              │
│                              [수신자] ◀── POP3/IMAP                   │
│                                                                       │
│  SMTP 명령/응답 예시:                                                 │
│                                                                       │
│  S: 220 mail.example.com ESMTP Postfix                             │
│  C: EHLO client.example.com                                          │
│  S: 250-mail.example.com                                            │
│  S: 250-PIPELINING                                                  │
│  S: 250-SIZE 10240000                                               │
│  S: 250-STARTTLS                                                    │
│  S: 250 AUTH PLAIN                                                   │
│  C: AUTH LOGIN                                                       │
│  S: 334 VXNlcm5hbaU6                                                 │
│  C: dXNlckBleGFtcGxlLmNvbQ==                                        │
│  S: 334 UGFzc3dvcmQ6                                                 │
│  C: cGFzc3dvcmQ=                                                     │
│  S: 235 2.7.0 Authentication successful                             │
│  C: MAIL FROM:<user@example.com>                                    │
│  S: 250 2.1.0 Ok                                                     │
│  C: RCPT TO:<recipient@target.com>                                   │
│  S: 250 2.1.5 Ok                                                     │
│  C: DATA                                                             │
│  S: 354 End data with <CR><LF>.<CR><LF>                             │
│  C: From: user@example.com                                           │
│  C: To: recipient@target.com                                        │
│  C: Subject: Test                                                    │
│  C:                                                                  │
│  C: Hello, World!                                                    │
│  C: .                                                                │
│  S: 250 2.0.0 Ok: queued as 12345                                   │
│  C: QUIT                                                             │
│  S: 221 2.0.0 Bye                                                   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

### POP3 vs IMAP

| 항목 | POP3 | IMAP |
|:---|:---|:---|
| **포트** | 110 (평문), 995 (TLS) | 143 (평문), 993 (TLS) |
| **동작** | 서버에서 메일 다운로드, 일반적으로 삭제 | 서버의 메일함과 동기화 |
| **오프라인** | 다운로드 후 서버에서 삭제되면 접근 불가 | 서버에 메일이 남아있어 어디서나 접근 |
| **대역폭** | 매번 전체 다운로드 | 변경분만 동기화 |
| **적합한 용도** | 단일 디바이스에서 메일 |複数 디바이스에서 메일 |

---

## Ⅲ. 융합 비교 및 다각도 분석

### SMTP 보안

| 기술 | 목적 | 동작 |
|:---|:---|:---|
| **SMTP AUTH** | 발신자 인증 | 사용자 이름/비밀번호로 SMTP 서버 접속 허용 |
| **STARTTLS** | 전송 구간 암호화 | 평문 연결을 TLS로 업그레이드 |
| **SPF** | 발신자 도메인 인증 | 해당 도메인의 정당한 메일 서버 목록 정의 |
| **DKIM** | 메일 무결성 인증 | 발신 도메인에서 암호학적 서명 |
| **DMARC** | 스팸/피싱 방어 | SPF/DKIM 결과에 따른 처리 정책 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 1 — SMTP 서버 보안**: SMTP 서버에 SMTP AUTH와 STARTTLS를 필수로 적용하여, 평문 전송을 차단한다. Let's Encrypt 인증서를 활용하여 TLS를 적용하고, Submission 포트(587)는 반드시 인증을 요구한다.

### 도입 체크리스트

- **운영·보안적**: STARTTLS 필수, SMTP AUTH 적용, SPF/DKIM/DMARC 적용, 스팸 필터링

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

이메일은 여전히 핵심 비즈니스 도구이며, SMTP의 역할도 계속될 것이다. 동시에 스팸/피싱 방지를 위한 인증 기술(SPF, DKIM, DMARC)의 역할이 더욱 중요해지고 있다.

### 참고 표준

- RFC 5321 — Simple Mail Transfer Protocol
- RFC 1939 — Post Office Protocol - Version 3
- RFC 3501 — INTERNET MESSAGE ACCESS PROTOCOL

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **POP3** | 메일을 서버에서 가져오는 수신 프로토콜로, 기본적으로 다운로드 후 삭제한다. |
| **IMAP** | 서버의 메일함과 동기화하는 수신 프로토콜로,複数 디바이스에서 접근 가능하다. |
| **SPF/DKIM/DMARC** | 이메일 인증 기술로, 스팸과 피싱을 방어한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. SMTP는 **우체국 간에 소포(메일)를 전달하는 방식**과 같아요. 발신 우체국(SMTP)이 수신 우체국에 소포를 가져다주고, 수신자는 우체국에 가서 소포를 찾아간다.
2. POP3는 **우체국에서 소포를 가져와서 내 방에 둔다**는 것과 같아요. 다 보고 나면 우체국에 없어요.
3. IMAP은 **우체국에 있는 내 소포를 어디서든 볼 수 있게** 해주는 거예요. 여러 곳에서 같은 소포를 볼 수 있어서便利다!
