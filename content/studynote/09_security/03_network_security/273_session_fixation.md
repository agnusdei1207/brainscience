+++
weight = 273
title = "273. 세션 고정 공격 (Session Fixation Attack)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: 세션 고정(Session Fixation)은 공격자가 **피해자에게 미리 알고 있는 세션 ID를 사용하게 만든** 뒤, 피해자 로그인 후 그 세션을 탈취하는 공격으로, 세션 하이재킹의 능동적 변형이다.
> 2. **가치**: 방어의 핵심은 **로그인 성공 직후 반드시 새 세션 ID를 발급(Session Regeneration)**하는 것으로, 공격자가 주입한 세션 ID는 인증 전의 것이기 때문에 재발급으로 무력화된다.
> 3. **판단 포인트**: OWASP (Open Web Application Security Project) Top 10의 A07(Identification and Authentication Failures)에 해당하며, 세션 하이재킹과의 차이(수동 vs 능동)를 정확히 구별해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

세션 하이재킹(Session Hijacking)이 **이미 인증된** 세션 ID를 훔치는 것이라면, 세션 고정은 한 발 앞서 **공격자가 세션 ID를 먼저 생성하고 피해자에게 심어두는** 방식이다. 피해자가 로그인하면 서버가 동일 세션 ID를 인증된 상태로 격상시키고, 공격자는 이미 알고 있는 그 세션 ID로 접근한다.

이 공격이 가능한 근본 원인은 서버가 로그인 전에 발급한 세션 ID를 **로그인 후에도 그대로 유지**하기 때문이다. 많은 레거시 프레임워크가 세션 재발급을 기본값으로 구현하지 않았고, PHP 초기 버전의 `session_start()` 함수가 대표적 취약점으로 지적된 바 있다.

공격자는 피해자에게 세션 ID를 주입하기 위해 URL 파라미터(`?SID=attacker_value`), 메타 태그, JavaScript 등 다양한 벡터를 활용한다. 서버가 URL 기반 세션 추적을 허용할 경우 이메일 링크 하나로 공격이 완성된다.

📢 **섹션 요약 비유**: 세션 고정은 주차 대리인(공격자)이 차 열쇠를 미리 복사해두고, 나중에 차 주인(피해자)이 그 열쇠로 문을 열어줄 때를 기다리는 것과 같다.

---

## 2. 구성요소

### 세션 고정 공격 시나리오

```
공격자 (Attacker)          피해자 (Victim)           서버 (Server)
      │                         │                        │
      │─── 세션 요청 ──────────────────────────────────►│
      │◄── SID=KNOWN_VALUE ─────────────────────────────│
      │                         │                        │
      │  악성 URL 이메일 전송   │                        │
      │──────────────────────►  │                        │
      │                         │                        │
      │             피해자 링크 클릭                     │
      │         ?sessionid=KNOWN_VALUE ────────────────►│
      │                         │  서버: 세션 재사용     │
      │                         │◄─ 로그인 페이지 ──────│
      │                         │                        │
      │                피해자 로그인 (ID/PW 입력)        │
      │                         │──────────────────────►│
      │                         │  SID=KNOWN_VALUE로 인증│
      │                         │◄─ 로그인 성공 ────────│
      │                         │                        │
      │─── SID=KNOWN_VALUE로 접근 ─────────────────────►│
      │◄── 피해자 계정 접근 성공 ───────────────────────│
      │     [세션 하이재킹 완료!]                        │
```

### 세션 고정 허용 조건 및 방어

| 취약 조건 | 설명 | 방어 조치 |
|:---|:---|:---|
| URL 세션 파라미터 허용 | `?PHPSESSID=xxx` 패턴 | URL 세션 추적 비활성화 |
| 세션 ID 재사용 | 로그인 후 동일 SID 유지 | 로그인 성공 시 session_regenerate_id() |
| 세션 ID 외부 주입 수용 | 클라이언트 제공 SID 그대로 사용 | 서버 생성 SID만 허용 |
| 장수명 세션 | 긴 세션 유효 기간 | 유휴 타임아웃 설정 |

📢 **섹션 요약 비유**: 호텔이 "방 번호를 직접 골라도 된다"고 하면 나쁜 사람이 비어있는 방 번호를 알아두고 당신이 체크인할 때를 기다릴 수 있다. 항상 프런트(서버)가 방 번호를 정해야 한다.

---

## 3. 구조 및 동작 원리

### 세션 공격 3종 비교

| 구분 | 세션 고정 (Fixation) | 세션 하이재킹 (Hijacking) | CSRF (Cross-Site Request Forgery) |
|:---|:---|:---|:---|
| **시점** | 로그인 전 세션 ID 주입 | 로그인 후 세션 ID 탈취 | 인증된 세션을 이용한 요청 위조 |
| **공격자 역할** | 능동적 (사전 준비) | 수동적 또는 능동적 | 수동적 (피해자 행동 유도) |
| **세션 ID 지식** | 공격자가 미리 알고 있음 | 공격 후 획득 | 필요 없음 |
| **핵심 방어** | 로그인 후 세션 재발급 | HTTPOnly, Secure, TLS | CSRF 토큰, SameSite 쿠키 |
| **OWASP 분류** | A07 인증 실패 | A07 인증 실패 | A01 접근제어 실패 |

**세션 재발급(Session Regeneration) 구현 예시**

```php
// PHP 취약 코드 (로그인 후 동일 세션 ID 유지)
session_start();
if (authenticate($user, $pass)) {
    $_SESSION['user'] = $user;  // ← SID 변경 없음! 취약!
}

// PHP 안전한 코드 (세션 재발급)
session_start();
if (authenticate($user, $pass)) {
    session_regenerate_id(true); // ← 새 SID 발급 + 기존 파일 삭제
    $_SESSION['user'] = $user;   // ← 안전
}
```

```java
// Java Servlet 예시
HttpSession oldSession = request.getSession(false);
if (oldSession != null) {
    oldSession.invalidate(); // 기존 세션 무효화
}
HttpSession newSession = request.getSession(true); // 새 세션 발급
newSession.setAttribute("user", user);
```

📢 **섹션 요약 비유**: 로그인 성공 후 세션 ID 재발급은 "호텔 체크인 후 새 카드키로 교체"하는 것이다. 이전 카드키(주입된 세션 ID)는 즉시 무효가 된다.

---

## 4. 비교 및 트레이드오프

**프레임워크별 세션 재발급 기본값**

| 프레임워크 | 기본 동작 | 권장 설정 |
|:---|:---|:---|
| Spring Security | 로그인 시 자동 재발급 (기본값) | `sessionManagement().sessionFixation().newSession()` |
| Django | 자동 재발급 지원 | `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_HTTPONLY=True` |
| Express.js | 수동 구현 필요 | `express-session`의 `regenerate()` 호출 |
| PHP (raw) | 수동 구현 필요 | `session_regenerate_id(true)` 필수 |
| Rails | 자동 재발급 (기본값) | `config.session_store :cookie_store, expire_after: 30.minutes` |

**추가 강화 방안**:
1. **세션 바인딩**: 세션에 클라이언트 IP, User-Agent 해시를 저장하고 불일치 시 세션 무효화
2. **이중 쿠키 패턴**: 별도의 짧은 수명 인증 쿠키와 세션 쿠키를 분리
3. **토큰 기반 인증(JWT)**: 서버 측 세션을 최소화해 고정 공격 표면 감소

**기술사 답안 핵심**: "로그인 전후 세션 ID의 연속성"이 문제의 본질임을 명확히 하고, 세션 재발급이 왜 유일한 근본 해결책인지 설명해야 한다.

📢 **섹션 요약 비유**: 보안 게이트 통과 후 새 배지를 발급하는 것이 원칙이다. 입장 전에 받은 임시 번호를 그대로 사용하면 미리 번호를 아는 사람이 함께 들어올 수 있다.

---

## 5. 실무 적용 및 최적화 기법

세션 고정 공격은 간단한 방어 코드 한 줄(`session_regenerate_id()`)로 99% 방어 가능하다. 그럼에도 레거시 시스템에서 빈번히 발견되는 이유는 개발자 교육 부재와 프레임워크 기본값 미확인에 있다.

현대 인증 프레임워크(Spring Security, Django, Rails)는 대부분 로그인 시 세션 재발급을 기본으로 구현한다. 새로운 시스템 개발 시 검증된 프레임워크를 사용하고, 레거시 시스템은 보안 감사를 통해 세션 관리 코드를 점검해야 한다.

OWASP 권고에 따라 세션 ID는 최소 128비트, 암호학적 난수로 생성하고, 모든 세션 전환(로그인, 권한 상승, 로그아웃) 시 ID를 재발급하는 것이 표준이다.

📢 **섹션 요약 비유**: 세션 고정 방어는 "처음부터 잘 만든 자물쇠 하나"로 해결된다. 복잡한 탐지 시스템보다 올바른 세션 재발급 코드 한 줄이 더 강력하다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| 세션 하이재킹 (Hijacking) | 상위 개념 | 세션 고정은 하이재킹의 능동적 변형 |
| CSRF (Cross-Site Request Forgery) | 연관 공격 | 인증된 세션 악용 (SameSite 쿠키 방어) |
| XSS (Cross-Site Scripting) | 공격 벡터 | 세션 ID 주입 수단으로 활용 가능 |
| session_regenerate_id() | 핵심 방어 | 로그인 후 새 세션 ID 발급 |
| OWASP Top 10 A07 | 분류 체계 | Identification and Authentication Failures |
| HTTPOnly / Secure 쿠키 | 보완 방어 | 세션 ID 탈취 경로 차단 |

### 👶 어린이를 위한 3줄 비유 설명
나쁜 사람이 놀이공원 입장권 번호를 미리 알아두고, 내가 그 번호로 들어가면 같이 들어오는 거예요.
해결책은 매표소에서 내가 표를 사는 순간 새 번호로 바꿔주는 거예요.
로그인 후 새 세션 번호를 받는 것(Session Regeneration)이 바로 그 방법이에요!
