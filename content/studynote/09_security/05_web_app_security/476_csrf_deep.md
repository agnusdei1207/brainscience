+++
weight = 476
title = "476. CSRF 심화 (Cross-Site Request Forgery Deep Dive)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: CSRF (Cross-Site Request Forgery)는 피해자가 인증된 상태에서 공격자가 유도한 요청이 서버에 자동으로 쿠키와 함께 전송되어 피해자 의도 없이 서버 상태를 변경하는 공격이다.
> 2. **가치**: XSS와 달리 서버 코드 취약점이 아닌 브라우저의 쿠키 자동 전송 메커니즘을 악용하므로, 방어가 개발 단계에서 명시적으로 구현되어야 한다.
> 3. **판단 포인트**: SameSite 쿠키 속성과 CSRF 토큰 중 어느 계층이 없는지 확인하는 것이 취약점 분석의 핵심이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

CSRF 공격은 브라우저가 동일 도메인 쿠키를 자동으로 요청에 포함하는 특성(Cookie 자동 전송)을 악용한다. 피해자가 이미 `bank.com`에 로그인된 상태에서 공격자 사이트를 방문하면, 공격자 사이트의 `<img src="https://bank.com/transfer?to=attacker&amount=1000">` 같은 태그가 피해자 쿠키와 함께 은행에 요청을 보낸다.

2000년대 초반 대규모 피해를 야기했으며, OWASP Top 10에 2003년부터 2017년까지 꾸준히 포함되었다. 2021 버전에서 A01 접근 제어 실패에 합병되었다.

📢 **섹션 요약 비유**: 피해자의 공인인증서(쿠키)를 빼앗지 않고, 피해자 손을 잡고 서명란(요청)에 도장을 찍게 하는 공격이다.

---

## 2. 구성요소

| 방어 기법 | 원리 | 한계 |
|:---|:---|:---|
| CSRF 토큰 | 요청마다 랜덤 토큰 검증 | 토큰 누출 시 무력화 |
| SameSite=Strict | 크로스 사이트 쿠키 전송 차단 | 일부 레거시 브라우저 미지원 |
| SameSite=Lax | GET 제외 크로스 사이트 차단 | GET 기반 변경 요청 취약 |
| Double Submit Cookie | 쿠키값=파라미터값 검증 | MITM 환경 취약 |
| Origin/Referer 검증 | 요청 출처 확인 | Proxy 환경 누락 가능 |

```
[CSRF 공격 흐름]

피해자 브라우저
  (bank.com 세션 쿠키 보유)
  │
  │ 공격자 사이트 방문
  ▼
evil.com 페이지
  <form action="https://bank.com/transfer" method="POST">
    <input name="to" value="attacker">
    <input name="amount" value="1000">
  </form>
  <script>document.forms[0].submit()</script>
  │
  │ 자동 제출 (쿠키 자동 포함)
  ▼
bank.com 서버
  유효한 쿠키 → 요청 처리 → 송금 완료
```

📢 **섹션 요약 비유**: 자는 동안 손을 잡아 도장을 찍게 하는 것처럼, 피해자 모르게 인증된 요청을 보낸다.

---

## 3. 구조 및 동작 원리

| 항목 | CSRF | XSS |
|:---|:---|:---|
| 악용 대상 | 브라우저 쿠키 자동 전송 | DOM 실행 컨텍스트 |
| 서버 취약점 | 없음(정상 동작 악용) | 있음(출력 미검증) |
| 피해 내용 | 상태 변경(송금·삭제) | 정보 탈취·실행 |
| 방어 수단 | CSRF 토큰, SameSite | 인코딩, CSP |

XSS 취약점이 존재하면 CSRF 토큰을 탈취할 수 있으므로 XSS 방어가 선행되어야 한다.

📢 **섹션 요약 비유**: XSS는 집에 침입, CSRF는 집 열쇠(쿠키) 없이 복사본(자동 전송)으로 들어오는 것이다.

---

## 4. 비교 및 트레이드오프

**최신 권고 방어 조합**:
1. `SameSite=Lax` 기본 + 민감 작업은 `SameSite=Strict`
2. Synchronizer Token Pattern(동기화 토큰 패턴): 서버가 세션당 토큰 발급 → 요청 시 검증
3. `Origin` 헤더 검증 (Referer 대신 Origin 우선)

**프레임워크 내장**: Django CSRF middleware, Spring Security CSRF protection이 기본 활성화됨.

📢 **섹션 요약 비유**: SameSite는 열쇠 복사를 막고, CSRF 토큰은 도장을 찍을 때 추가 비밀번호를 요구하는 이중 자물쇠다.

---

## 5. 실무 적용 및 최적화 기법

SameSite 쿠키와 CSRF 토큰을 함께 적용하면 현실적인 CSRF 공격의 거의 모든 경로가 차단된다. 특히 SameSite=Lax가 2020년 이후 Chrome의 기본값이 되면서 CSRF의 위협은 크게 감소했지만, 레거시 브라우저·서브도메인 공유 환경에서는 여전히 토큰 방어가 필요하다.

📢 **섹션 요약 비유**: 이중 자물쇠(SameSite + CSRF 토큰)가 있으면 남의 손을 잡아 도장 찍기가 불가능해진다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SameSite 쿠키 | 방어 | 크로스 사이트 쿠키 전송 제한 |
| CSRF 토큰 | 방어 | 요청 진위 검증 토큰 |
| XSS | 연계 위협 | CSRF 토큰 탈취 가능 |
| Double Submit | 대안 방어 | 쿠키값-파라미터 일치 검증 |

### 👶 어린이를 위한 3줄 비유 설명
CSRF는 잠든 사람의 손을 잡아 도장을 찍게 하는 것처럼, 피해자 모르게 서류에 서명을 받는 공격이에요.
브라우저가 자동으로 쿠키(도장)를 가져가기 때문에 일어나는 일이에요.
SameSite와 CSRF 토큰이라는 두 자물쇠를 채우면 이런 도장 찍기를 막을 수 있어요.
