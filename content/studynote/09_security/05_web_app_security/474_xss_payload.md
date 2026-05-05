+++
weight = 474
title = "474. XSS 페이로드"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: XSS (Cross-Site Scripting) 방어는 입력 검증 → 출력 인코딩 → HTTP 보안 헤더(CSP, HTTPOnly, X-Content-Type-Options)로 이어지는 심층 방어(Defense in Depth) 전략이다.
> 2. **가치**: 단일 계층 방어는 새로운 우회 기법에 취약하므로, 여러 계층이 독립적으로 작동해야 실질적 보호가 가능하다.
> 3. **판단 포인트**: CSP (Content Security Policy) 정책이 지나치게 느슨하거나 `'unsafe-inline'`을 허용하면 방어 효과가 사실상 무력화된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

XSS 방어를 위한 HTTP (Hypertext Transfer Protocol) 보안 헤더 3종은 각각 독립적인 역할을 수행한다.
- **CSP**: 실행 가능한 스크립트 출처를 제한
- **HTTPOnly**: `document.cookie`로 쿠키 접근 차단
- **X-Content-Type-Options**: MIME 스니핑 방지로 콘텐츠 타입 위조 차단

이 세 헤더는 서로 다른 공격 벡터를 차단하므로 모두 설정해야 완전한 방어가 된다.

📢 **섹션 요약 비유**: 방화문(CSP) + 금고 자물쇠(HTTPOnly) + 위조 방지 봉인(X-Content-Type) 세 겹 보호막이다.

---

## 2. 구성요소

| 헤더 | 역할 | 예시 값 |
|:---|:---|:---|
| Content-Security-Policy | 스크립트 출처 제한 | `script-src 'self' 'nonce-abc'` |
| Set-Cookie HTTPOnly | JS 쿠키 접근 차단 | `session=x; HttpOnly; Secure` |
| X-Content-Type-Options | MIME 스니핑 방지 | `nosniff` |
| X-XSS-Protection | 레거시 브라우저 XSS 필터 | `1; mode=block` |

```
[XSS 방어 계층]

사용자 입력
  │
  ▼
┌─────────────────────────────┐
│  Layer 1: 입력 검증          │
│  allowlist 기반 필터링       │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Layer 2: 출력 인코딩        │
│  < → &lt;  " → &quot;       │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Layer 3: HTTP 보안 헤더     │
│  CSP / HTTPOnly / nosniff   │
└─────────────────────────────┘
```

📢 **섹션 요약 비유**: 공항의 수화물 검사(입력 검증) → X-ray(출력 인코딩) → 폭발물 감지기(보안 헤더) 순의 다중 검문이다.

---

## 3. 구조 및 동작 원리

| 방어 기법 | 차단하는 공격 | 한계 |
|:---|:---|:---|
| CSP strict-dynamic | 인라인 스크립트 | nonce 탈취 시 무력화 |
| HTTPOnly 쿠키 | 쿠키 탈취 XSS | XHR/Fetch 기반 공격 무방어 |
| X-Content-Type | MIME 기반 XSS | 최신 브라우저에는 기본 적용 |
| SameSite 쿠키 | CSRF 연계 | XSS와는 별개 방어 |

📢 **섹션 요약 비유**: 각 헤더는 다른 문을 잠그는 열쇠—하나가 없으면 그 문으로 침입 가능하다.

---

## 4. 비교 및 트레이드오프

**Nginx 설정 예시**:
```
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'nonce-$request_id'";
add_header X-Content-Type-Options "nosniff";
add_header X-Frame-Options "DENY";
```

**CSP 위반 리포트**: `report-uri /csp-report`로 공격 시도 수집 및 SIEM (Security Information and Event Management) 연동

📢 **섹션 요약 비유**: 서버 응답에 경호원 세 명(CSP·HTTPOnly·nosniff)을 붙여 보내는 것이다.

---

## 5. 실무 적용 및 최적화 기법

세 헤더를 모두 적용하면 알려진 XSS 페이로드의 대부분이 브라우저 수준에서 차단된다. CSP 리포트 기능은 제로데이 시도까지 포착하는 탐지 수단으로도 활용된다.

📢 **섹션 요약 비유**: 세 겹 방어막은 하나가 뚫려도 나머지가 막아주는 안전망이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CSP | 주요 방어 | 스크립트 출처 정책 |
| HTTPOnly | 쿠키 방어 | JS 쿠키 접근 차단 |
| nosniff | MIME 방어 | 콘텐츠 타입 위조 방지 |
| nonce | CSP 구성 | 요청별 고유 토큰 |

### 👶 어린이를 위한 3줄 비유 설명
CSP는 허락된 사람만 집 안에 들어올 수 있게 하는 경비원이에요.
HTTPOnly는 쿠키(열쇠)를 자바스크립트가 만지지 못하게 하는 자물쇠예요.
X-Content-Type-Options는 위조 신분증을 사용하지 못하게 막는 봉인이에요.
