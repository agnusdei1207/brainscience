+++
weight = 426
title = "426. 약한 TLS 버전"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: 약한 TLS (Transport Layer Security) 버전이나 암호화 스위트(Cipher Suite) 사용은 POODLE, BEAST, DROWN 같은 프로토콜 수준 공격에 취약하게 하고, 공격자가 전송 데이터를 복호화하거나 변조할 수 있게 한다.
> 2. **가치**: TLS 1.0/1.1은 2021년 RFC 8996으로 공식 폐기되었고, PCI DSS 3.2+는 TLS 1.2 이상 의무화, TLS 1.3은 현재 표준으로 모든 신규 서비스에 적용되어야 한다.
> 3. **판단 포인트**: TLS 버전뿐 아니라 암호화 스위트(RC4, NULL 암호화, 수출용 암호화), 인증서 강도(키 길이), HSTS (HTTP Strict Transport Security) 적용 여부를 종합 점검해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

TLS는 인터넷 통신의 기밀성·무결성·인증을 제공하는 핵심 프로토콜이다. 하지만 오래된 버전과 취약한 암호화 스위트는 20년간 발견된 수많은 공격에 노출되어 있다.

주요 TLS 취약점 공격:
- **POODLE (Padding Oracle On Downgraded Legacy Encryption)**: SSL 3.0 패딩 오라클 공격
- **BEAST (Browser Exploit Against SSL/TLS)**: TLS 1.0 CBC 블록 암호 공격
- **DROWN (Decrypting RSA with Obsolete and Weakened eNcryption)**: SSLv2 약점으로 TLS 세션 복호화
- **FREAK (Factoring RSA Export Keys)**: 수출용 512비트 RSA 강제 협상
- **Logjam**: 512비트 DH (Diffie-Hellman) 파라미터 다운그레이드

이런 공격들은 오래된 TLS 버전이 "지원만 하고 있어도" 공격자가 핸드셰이크 과정에서 다운그레이드를 강제할 수 있어 위험하다.

📢 **섹션 요약 비유**: 집에 새 잠금장치를 달면서 옛날 마스터키 구멍을 막지 않으면, 공격자는 옛날 구멍으로 들어온다.

---

## 2. 구성요소

TLS 버전별 현황과 권장 수준:

| TLS 버전 | 상태 | 출시 | 권고 |
|:---:|:---|:---:|:---|
| SSL 3.0 | 완전 폐기 | 1996 | 즉시 비활성화 |
| TLS 1.0 | 공식 폐기 (RFC 8996) | 1999 | 즉시 비활성화 |
| TLS 1.1 | 공식 폐기 (RFC 8996) | 2006 | 즉시 비활성화 |
| TLS 1.2 | 허용 (설정 주의 필요) | 2008 | 강력한 스위트만 허용 |
| TLS 1.3 | 권장 현재 표준 | 2018 | 모든 신규 서비스 적용 |

```
┌──────────────────────────────────────────────────────────┐
│           TLS 1.3 개선 포인트                            │
├──────────────────────────────────────────────────────────┤
│  1-RTT 핸드셰이크 (TLS 1.2 대비 레이턴시 감소)          │
│  0-RTT 재연결 (이전 세션 재개)                           │
│  취약 암호화 스위트 전면 제거 (RC4, DES, NULL 등)        │
│  PFS (Perfect Forward Secrecy) 기본 강제               │
│  RSA 키 교환 제거 → ECDHE/DHE만 허용                    │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: TLS 1.3는 낡은 자물쇠 구멍을 모두 용접해버리고, 최신 생체 인식만 남긴 것과 같다.

---

## 3. 구조 및 동작 원리

| 구분 | TLS 1.2 | TLS 1.3 |
|:---|:---|:---|
| 핸드셰이크 | 2-RTT | 1-RTT (0-RTT 재연결) |
| PFS | 선택적 | 기본 강제 |
| 취약 암호 제거 | 불완전 | RC4, DES, 수출암호 전면 제거 |
| 속도 | 느림 | 빠름 |
| 브라우저 지원 | 전체 | 최신 브라우저 (99%+) |

📢 **섹션 요약 비유**: TLS 1.2는 구형 자동차(안전벨트 있음), TLS 1.3은 에어백·충돌방지·자동제동까지 갖춘 최신 자동차다.

---

## 4. 비교 및 트레이드오프

**Nginx TLS 설정 예시**:
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers on;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
```

**정기 점검 도구**:
- **SSL Labs Server Test**: ssllabs.com/ssltest — A+ 등급 목표
- **testssl.sh**: 명령줄 TLS 취약점 스캔 도구
- **Qualys SSL Pulse**: 대규모 TLS 설정 모니터링

📢 **섹션 요약 비유**: SSL Labs A+ 등급은 자동차 충돌 안전 테스트 최고 등급과 같다. 설정 후 반드시 외부 검증을 받아야 한다.

---

## 5. 실무 적용 및 최적화 기법

TLS 1.3 전용 설정과 HSTS preload 등록을 완료하면 전송 계층 보안을 현재 최고 수준으로 높일 수 있다. HSTS preload는 브라우저 출하 시점부터 HTTPS를 강제해 SSLStrip 공격도 방어한다.

기술사 관점에서 TLS 설정은 인프라 수준의 보안 요소로, IaC (Infrastructure as Code) 템플릿에 강제 설정을 포함시키고 CSPM (Cloud Security Posture Management) 도구로 준수 여부를 지속 모니터링해야 한다.

📢 **섹션 요약 비유**: TLS 버전 관리는 소프트웨어 패치처럼 지속적 유지보수가 필요하다. 한 번 설정하고 잊으면 새로운 공격에 무방비 상태가 된다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| POODLE | 공격 예시 | SSL 3.0 패딩 오라클 |
| PFS | 보안 속성 | 세션 키 노출 최소화 |
| HSTS | 보완 통제 | HTTP→HTTPS 강제 전환 |
| Certificate Pinning | 추가 방어 | 인증서 위변조 방지 |
| Cipher Suite | 설정 요소 | 암호화 알고리즘 조합 |

### 👶 어린이를 위한 3줄 비유 설명
- TLS는 인터넷에서 편지를 안전하게 보내는 봉투인데, 낡은 봉투는 쉽게 뜯을 수 있어.
- TLS 1.3은 봉투 위에 특수 잠금장치까지 달린 가장 최신 봉투야.
- 낡은 봉투(SSL 3.0, TLS 1.0)는 쓰지 말고, 항상 최신 봉투를 써야 안전해!
