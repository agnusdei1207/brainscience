+++
weight = 271
title = "271. 세션 하이재킹 (Session Hijacking)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: 세션 하이재킹(Session Hijacking)은 인증 후 발급된 세션 식별자(Session ID)를 탈취해 합법적 사용자로 위장하는 공격으로, 인증 과정 자체를 우회한다는 점에서 암호 탈취보다 더 은밀하다.
> 2. **가치**: 방어의 핵심은 세션 ID를 예측 불가하게(256-bit random), 전송 중 암호화(HTTPS), 그리고 HTTPOnly·Secure 쿠키 플래그로 JavaScript 접근을 원천 차단하는 것이다.
> 3. **판단 포인트**: TCP (Transmission Control Protocol) 시퀀스 넘버 예측 공격과 쿠키 도용(Cookie Theft) 방식의 차이, 그리고 각 방어 기법의 대응 관계를 정확히 구별해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

HTTP는 본질적으로 무상태(Stateless) 프로토콜이다. 로그인 상태를 유지하기 위해 서버는 세션 ID를 발급하고 클라이언트는 이를 쿠키나 URL 파라미터로 전송한다. 세션 하이재킹은 이 세션 ID를 공격자가 획득해 피해자 대신 서버와 통신하는 공격이다.

세션 하이재킹이 위험한 이유는 **인증 단계를 건너뛰기** 때문이다. 공격자는 비밀번호를 모르더라도 이미 인증된 세션 토큰만 있으면 피해자의 계정에 완전히 접근할 수 있다. 이메일, 금융 거래, 관리자 패널 등 모든 권한이 세션에 묶여 있으므로 피해 범위가 매우 넓다.

공격 시나리오는 크게 두 축으로 나뉜다. 네트워크 레벨에서 TCP 시퀀스 넘버를 예측해 패킷을 가로채는 **능동적 하이재킹(Active Hijacking)**과, XSS (Cross-Site Scripting) 또는 패킷 스니핑으로 세션 쿠키를 훔치는 **수동적 하이재킹(Passive Hijacking)**이 그것이다.

📢 **섹션 요약 비유**: 세션 하이재킹은 누군가 공항 탑승권을 복사해 당신 대신 비행기에 타는 것과 같다. 여권(비밀번호)이 없어도 탑승권(세션 ID)만 있으면 된다.

---

## 2. 구성요소

### 공격 유형별 메커니즘

```
[TCP 시퀀스 예측 (IP Spoofing + Sequence Prediction)]

클라이언트 (A)      공격자 (C)        서버 (S)
    │                  │                │
    │── SYN (seq=100)──┼───────────────►│
    │◄─ SYN-ACK ───────┼────────────────│
    │                  │ 패킷 스니핑     │
    │                  │ seq=300 예측   │
    │                  │── ACK(seq=301)►│ ← A로 위장
    │                  │   세션 탈취!   │

[쿠키 도용 (XSS 기반)]

피해자 (V)           악성 스크립트    공격자 서버
    │                     │              │
    │ 악성 페이지 방문     │              │
    │──────────────────►  │              │
    │  <script>           │              │
    │  document.cookie    │              │
    │  → 공격자 서버 전송 │─────────────►│
    │  </script>          │  세션 쿠키 수신
```

### 세션 하이재킹 유형 및 방어

| 공격 유형 | 원리 | 핵심 방어 |
|:---|:---|:---|
| TCP 세션 하이재킹 | ISN(Initial Sequence Number) 예측 | 암호학적 난수 ISN, IPsec |
| 쿠키 스니핑 | 평문 HTTP에서 쿠키 캡처 | HTTPS 강제, Secure 플래그 |
| XSS 쿠키 도용 | JavaScript로 document.cookie 탈취 | HTTPOnly 플래그 |
| 세션 고정(Fixation) | 공격자가 세션 ID 주입 | 로그인 후 세션 ID 재발급 |
| 세션 사이드재킹 | 무선랜에서 쿠키 캡처 | 전체 세션 HTTPS |
| 크로스사이트 요청 위조(CSRF) | 세션 쿠키를 이용한 요청 위조 | CSRF 토큰, SameSite 쿠키 |

📢 **섹션 요약 비유**: TCP 하이재킹은 편지봉투를 중간에 바꿔치기하는 것이고, 쿠키 도용은 열쇠를 몰래 복사하는 것이다. 방어 방법이 다를 수밖에 없다.

---

## 3. 구조 및 동작 원리

### 쿠키 보안 플래그 비교

| 플래그 | 기능 | 방어하는 공격 |
|:---|:---|:---|
| `Secure` | HTTPS 연결에서만 쿠키 전송 | 스니핑, 평문 탈취 |
| `HttpOnly` | JavaScript document.cookie 접근 차단 | XSS 기반 쿠키 도용 |
| `SameSite=Strict` | 크로스사이트 요청 시 쿠키 미전송 | CSRF 공격 |
| `SameSite=Lax` | GET 크로스사이트는 허용, POST는 차단 | CSRF 부분 방어 |
| `SameSite=None; Secure` | 크로스사이트 전송 허용 (HTTPS 필수) | 서드파티 쿠키 허용 시 |

추가 방어 계층:

- **세션 바인딩**: IP 주소, User-Agent, 지리적 위치를 세션에 묶어 이상 감지
- **짧은 세션 만료**: 유휴 타임아웃 15~30분 적용
- **재인증(Step-Up Auth)**: 민감한 작업(이체, 비밀번호 변경) 전 재확인
- **토큰 순환(Token Rotation)**: 요청마다 세션 토큰을 갱신하는 방식

📢 **섹션 요약 비유**: Secure 플래그는 탑승권을 봉투에 넣어 보내는 것, HttpOnly는 봉투를 투명 테이프로 봉인해 중간에 열어볼 수 없게 하는 것이다.

---

## 4. 비교 및 트레이드오프

**안전한 세션 관리 구현 체크리스트**

```
1. 세션 ID 생성
   ├─ 최소 128비트 (권장 256비트) 암호학적 난수 사용
   ├─ CSPRNG (Cryptographically Secure Pseudo-Random Number Generator)
   └─ URL에 세션 ID 노출 금지 (Referer 헤더 유출 위험)

2. 전송 보안
   ├─ 전체 사이트 HTTPS + HSTS (HTTP Strict Transport Security)
   ├─ Secure 쿠키 플래그 필수
   └─ 쿠키 경로(Path)와 도메인(Domain) 최소 범위로 설정

3. 생명주기 관리
   ├─ 로그인 성공 시 즉시 세션 ID 재발급 (Session Regeneration)
   ├─ 로그아웃 시 서버 측 세션 즉시 삭제
   ├─ 유휴 타임아웃 (Idle Timeout) + 절대 타임아웃 (Absolute Timeout)
   └─ 동시 세션 제한 (한 계정 = 한 활성 세션)
```

**실무 시나리오**: 금융 앱에서 이체 화면 접근 시 세션 나이(Session Age)가 10분 이상이면 OTP (One-Time Password) 재인증을 요구하고, 새 세션 ID를 발급하는 패턴이 표준이다. 이 방식은 탈취된 오래된 세션 토큰을 무력화한다.

**OWASP (Open Web Application Security Project) Session Management Cheat Sheet** 핵심:
- 세션 ID는 서버 측 저장소에서만 유효성 검증
- JWT (JSON Web Token) 사용 시 `exp` 클레임 필수, 블랙리스트 관리 병행

📢 **섹션 요약 비유**: 금고 열쇠를 빌려준 후 돌려받더라도 복사본이 있을 수 있다. 중요한 작업 전에는 자물쇠 자체를 교체(세션 재발급)하는 것이 가장 확실한 방어다.

---

## 5. 실무 적용 및 최적화 기법

세션 관리는 웹 보안의 근간이다. 강력한 인증 메커니즘을 갖추더라도 세션 관리가 허술하면 인증이 무의미해진다. HttpOnly + Secure + SameSite 쿠키 플래그 조합, HTTPS 강제, 로그인 후 세션 ID 재발급 이 세 가지는 최소 필수 조치다.

JWT 기반 토큰 인증이 증가하는 현대 아키텍처에서도 핵심 원칙은 동일하다. 토큰의 서명 키 관리, 만료 시간 설정, Refresh Token 순환 정책이 기존 세션 관리의 원칙을 그대로 계승한다.

📢 **섹션 요약 비유**: 세션 관리는 "문을 잠그는 것"이 아니라 "문을 주기적으로 교체하고, 여분 열쇠를 통제하며, 누가 언제 들어왔는지 기록하는" 종합 보안 체계다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| XSS (Cross-Site Scripting) | 공격 벡터 | HttpOnly 플래그로 쿠키 도용 차단 |
| CSRF (Cross-Site Request Forgery) | 연관 공격 | SameSite 쿠키로 방어 |
| 세션 고정 (Session Fixation) | 연관 공격 | 로그인 후 세션 ID 재발급으로 방어 |
| HTTPS / TLS | 방어 기제 | 전송 중 쿠키 암호화 |
| JWT (JSON Web Token) | 대안 기술 | 세션리스(Stateless) 토큰 인증 |
| OWASP Top 10 | 분류 체계 | A07: Identification and Authentication Failures |

### 👶 어린이를 위한 3줄 비유 설명
로그인하면 학교가 "출입증 번호"를 주는데, 나쁜 사람이 그 번호를 몰래 훔쳐서 학교에 나 대신 들어가는 거예요.
그래서 출입증은 암호로 잠그고(HTTPS), 화면에 보이지 않게 숨기고(HttpOnly), 오래되면 새 번호로 바꿔요.
중요한 일을 할 때는 선생님이 다시 한번 얼굴을 확인해요(재인증).
