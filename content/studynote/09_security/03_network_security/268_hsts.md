+++
weight = 268
title = "268. HSTS (HTTP Strict Transport Security)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: HSTS (HTTP Strict Transport Security)는 웹 서버가 브라우저에게 "이 도메인은 앞으로 HTTPS (HyperText Transfer Protocol Secure)로만 접속하라"고 지시하는 응답 헤더로, SSL (Secure Sockets Layer) 스트리핑 공격을 원천 차단한다.
> 2. **가치**: 첫 HTTP 요청을 HTTPS로 자동 업그레이드하던 기존 방식은 첫 연결 시점에 MitM (Man-in-the-Middle) 공격에 취약하지만, HSTS Preload를 통해 브라우저가 아예 HTTP 연결 시도를 하지 않도록 할 수 있다.
> 3. **판단 포인트**: `max-age`를 최소 1년(31,536,000초)으로 설정하고 `includeSubDomains`·`preload` 디렉티브를 포함해야 완전한 HSTS 보호가 달성된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

사용자가 브라우저 주소창에 `bank.com`을 입력하면 기본적으로 `http://bank.com`으로 먼저 연결된다. 서버가 301 리다이렉트로 `https://bank.com`으로 보내더라도, 첫 HTTP 요청과 응답이 평문으로 오가는 순간이 존재한다. 이 순간을 공격자가 가로채 HTTPS 업그레이드 응답을 제거하고 계속 HTTP로 통신하게 만드는 것이 SSL 스트리핑(SSL Stripping) 공격이다. 2009년 Moxie Marlinspike가 sslstrip 도구로 이 공격을 시연하면서 실질적 위협으로 부각됐다.

HSTS (RFC 6797)는 이 문제를 해결하기 위해 2012년 표준화됐다. 서버가 HTTPS 응답에 `Strict-Transport-Security` 헤더를 포함하면, 브라우저는 `max-age`에 지정된 기간 동안 해당 도메인에 대해 HTTP 연결 자체를 시도하지 않고 내부적으로 HTTPS로 전환한다. 사용자가 의도적으로 `http://`를 입력해도 브라우저가 자동으로 `https://`로 바꾼다.

그러나 HSTS 헤더는 최초 HTTPS 연결 성공 이후부터 유효하다. 사용자가 특정 사이트에 처음 접속할 때는 여전히 HTTP 첫 요청이 발생할 수 있어 초기 연결 취약점(TOFU, Trust On First Use)이 남는다. HSTS Preload는 이 초기 취약점도 제거한다.

📢 **섹션 요약 비유**: HSTS는 은행이 "우리 지점은 항상 보안 채널(HTTPS)로만 상담합니다"라고 고객 수첩에 기록해두는 것이다. 고객은 다음번에 HTTP 창구에 가지 않는다.

---

## 2. 구성요소

### HSTS 헤더 구조

| 디렉티브 | 설명 | 권장값 |
|:---|:---|:---|
| `max-age` | HSTS 정책 유지 기간 (초) | 최소 31,536,000 (1년), Preload는 63,072,000 (2년) |
| `includeSubDomains` | 모든 서브도메인에도 HSTS 적용 | 권장 포함 |
| `preload` | 브라우저 내장 Preload 리스트 등재 동의 | Preload 원하는 경우 필수 |

```
HTTP 응답 예시:
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

### HSTS 동작 흐름 및 SSL 스트리핑 방어

```
[HSTS 없는 환경 - SSL 스트리핑 취약]

  사용자                    공격자 (MitM)           서버
    │── http://bank.com ──▶│                         │
    │                       │── http://bank.com ────▶│
    │                       │◀── 301 → https:// ─────│
    │                       │(리다이렉트 제거!)       │
    │                       │── http://bank.com ────▶│
    │◀── http 평문 응답 ────│                         │
    ※ 사용자는 HTTPS인 줄 알지만 HTTP로 통신

[HSTS 적용 환경]

  사용자         브라우저 HSTS 캐시       서버
    │
    │ "bank.com 입력"
    │
    ▼
  HSTS 캐시 확인: bank.com 등록됨 (max-age 유효)
    │
    ▼
  브라우저가 내부적으로 https://bank.com으로 전환
    │
    └── TLS 핸드셰이크 ──────────────────────────▶│
    │◀─────────────────────────────────────────────│
  ※ HTTP 연결 시도 자체가 없음 → MitM 개입 불가

[HSTS Preload - 최초 접속도 보호]

  브라우저 설치 시부터 내장된 Preload 리스트에
  bank.com 포함 → 서버 응답 없이도 HTTPS 강제
```

### HSTS Preload 리스트

구글이 관리하는 `hstspreload.org`에 도메인을 등록하면, 크롬·파이어폭스·엣지·사파리 등 주요 브라우저의 소스코드에 해당 도메인이 "항상 HTTPS" 목록으로 포함된다. 첫 접속 시점부터 HTTP 연결 시도가 브라우저 레벨에서 차단된다.

Preload 등록 요건:
1. 유효한 HTTPS 인증서 보유
2. HTTP → HTTPS 리다이렉트 활성화
3. `max-age` ≥ 31,536,000초
4. `includeSubDomains` 포함
5. `preload` 디렉티브 포함

📢 **섹션 요약 비유**: HSTS Preload는 전화번호부가 인쇄될 때부터 "이 은행은 보안 회선만 사용"이라는 메모가 인쇄된 것이다. 누군가 스티커로 가려도 소용없다.

---

## 3. 구조 및 동작 원리

| 방어 기술 | 보호 범위 | TOFU 취약점 | 관리 복잡도 |
|:---|:---|:---|:---|
| HTTPS 리다이렉트만 | HTTP→HTTPS 유도 | 있음 (첫 HTTP 연결 노출) | 낮음 |
| HSTS (헤더만) | HTTPS 강제 (캐시 유효 기간) | 최초 방문 시 있음 | 낮음 |
| HSTS + Preload | 브라우저 수준 HTTPS 강제 | 없음 | 중간 (Preload 등록·해제 절차) |
| CAA (Certification Authority Authorization) | 인증서 발급 제한 | 없음 | 낮음 |
| HPKP (HTTP Public Key Pinning) | 인증서 피닝 | 없음 | 높음 (현재 deprecated) |

📢 **섹션 요약 비유**: HTTPS 리다이렉트는 문 앞 안내판, HSTS는 고객이 주소록에 "보안 채널만"이라고 기록한 것, Preload는 공장 출고 시부터 그 기록이 인쇄된 것이다.

---

## 4. 비교 및 트레이드오프

**서버 설정 예시**:

```nginx
# Nginx 설정
server {
    listen 443 ssl;
    server_name bank.com;
    add_header Strict-Transport-Security
        "max-age=63072000; includeSubDomains; preload" always;
}
server {
    listen 80;
    server_name bank.com;
    return 301 https://$host$request_uri;
}
```

```apache
# Apache 설정
<VirtualHost *:443>
    Header always set Strict-Transport-Security \
        "max-age=63072000; includeSubDomains; preload"
</VirtualHost>
```

**HSTS 해제 절차** (잘못 설정 시):
- Preload 등록된 도메인의 HSTS를 해제하려면 `max-age=0`을 응답하고, hstspreload.org에서 제거 신청 후 브라우저 배포 주기(수개월)를 기다려야 한다.
- 따라서 `includeSubDomains` 적용 전 모든 서브도메인이 HTTPS를 지원하는지 반드시 확인해야 한다. HTTPS 미지원 서브도메인이 있으면 접속 불가 장애 발생.

**HSTS Bypass 공격 가능성**:
- 브라우저 캐시 삭제 후 첫 방문 시 (Preload 없는 경우) 여전히 취약.
- 새 브라우저 프로파일·시크릿 모드에서 Preload 리스트가 적용되는지 확인 필요.
- 공격자가 `max-age` 만료 직후 SSL 스트리핑 시도 → `max-age` 갱신 정책 필요.

**기술사 시험 포인트**:
- HSTS의 동작 원리와 TOFU 문제, Preload로의 해결을 순서대로 설명해야 한다.
- `max-age`, `includeSubDomains`, `preload` 세 디렉티브의 의미를 각각 설명해야 한다.
- SSL 스트리핑과 HSTS의 관계를 묻는 문제가 자주 출제된다.

📢 **섹션 요약 비유**: HSTS max-age가 끝나는 날 문을 잠깐 열어 두면 강도가 들어올 수 있다. 그래서 만료 전에 고객이 다시 방문해 갱신되도록 사이트를 주기적으로 방문하게 해야 한다.

---

## 5. 실무 적용 및 최적화 기법

HSTS는 설정 한 줄로 SSL 스트리핑 공격을 완전히 차단할 수 있는 강력한 보안 헤더다. 구현 비용이 낮고 효과가 크기 때문에 OWASP (Open Web Application Security Project), NIST (National Institute of Standards and Technology), KISA 모두 HTTPS 필수 헤더로 권고한다.

Preload 등록까지 완료하면 처음 방문하는 사용자도 HTTP 연결 없이 항상 HTTPS로 보호된다. 다만 `includeSubDomains` 적용 전 서브도메인 HTTPS 지원 여부를 철저히 점검해 운영 장애를 방지해야 한다.

TLS 1.3 전면 채택, DoH/DoT 확산과 함께 HSTS Preload는 웹 보안의 기본 요건으로 자리잡고 있으며, 공공·금융·의료 서비스에서는 사실상 의무적 설정이 되어 가고 있다.

📢 **섹션 요약 비유**: HSTS는 집의 자동 잠금 장치다. 손님이 문을 열어두고 나가더라도 일정 시간 후 자동으로 잠긴다. Preload는 공장에서 이미 자동 잠금 장치가 기본 설치된 집을 받는 것이다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SSL Stripping | 방어 대상 | HTTP 다운그레이드 MitM 공격 |
| TLS (Transport Layer Security) | 기반 기술 | HTTPS의 암호화 프로토콜 |
| HSTS Preload | 강화 기법 | 브라우저 내장 HTTPS 강제 리스트 |
| TOFU (Trust On First Use) | 잔존 취약점 | 최초 방문 시 HTTP 노출 |
| HPKP (HTTP Public Key Pinning) | 연관 헤더 | 인증서 피닝 (현재 deprecated) |
| CAA (Certification Authority Authorization) | 보완 기술 | 허가된 CA만 인증서 발급 가능 |
| RFC 6797 | 표준 문서 | HSTS 정의 |

### 👶 어린이를 위한 3줄 비유 설명
- HSTS는 은행이 "우리 은행은 보안 유리창(HTTPS) 있는 창구만 운영해요"라고 고객 수첩에 적어주는 것이다.
- 다음번에 고객은 수첩을 보고 보안 창구로만 간다.
- Preload는 수첩이 아니라 아예 은행 지도에 인쇄되어 있는 것이라 처음 오는 사람도 보안 창구로 바로 간다.
