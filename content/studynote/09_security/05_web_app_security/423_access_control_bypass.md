+++
weight = 423
title = "423. 접근 제어 회피 CORS Misconfiguration"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: CORS (Cross-Origin Resource Sharing) Misconfiguration은 웹 서버가 교차 출처 요청의 `Origin` 헤더를 무분별하게 신뢰해, 악의적인 외부 도메인이 인증된 사용자의 자격으로 민감한 API에 접근할 수 있게 하는 취약점이다.
> 2. **가치**: CORS 오설정은 사용자가 악성 사이트를 방문하는 것만으로도 자신의 인증 토큰·쿠키를 통한 API 호출이 공격자에게 가능하게 하므로, 데이터 유출·계정 탈취로 직결된다.
> 3. **판단 포인트**: `Access-Control-Allow-Origin: *`과 `withCredentials: true`의 조합은 브라우저가 차단하지만, Origin을 동적으로 반사하거나 `null` Origin을 허용하는 설정이 실제 공격 벡터가 된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

브라우저의 SOP (Same-Origin Policy) 는 다른 출처(Origin)의 리소스 접근을 기본적으로 차단한다. CORS는 서버가 특정 출처를 명시적으로 허용해 이 제한을 완화하는 메커니즘이다. 하지만 CORS 설정이 잘못되면 원래 막아야 할 교차 출처 접근을 오히려 허용하게 된다.

가장 흔한 오설정 패턴:
1. **Origin 동적 반사**: 모든 요청의 Origin 헤더를 그대로 `Access-Control-Allow-Origin`에 반영
2. **null Origin 허용**: `Access-Control-Allow-Origin: null` — file:// 프로토콜이나 샌드박스 iframe에서 악용 가능
3. **와일드카드 + 자격증명**: `Allow-Origin: *` + `Allow-Credentials: true` — 브라우저 차단이지만 잘못 이해한 개발자가 우회 시도
4. **부분 매칭**: `attacker.victim.com` 형태의 서브도메인 허용

📢 **섹션 요약 비유**: CORS 오설정은 클럽 입구에서 "아무 손님이나 VIP라고 하면 들여보내는" 규칙과 같다. 원래 VIP만 들어가야 하는데 아무나 VIP 흉내를 낼 수 있다.

---

## 2. 구성요소

CORS Misconfiguration 공격 흐름:

| 단계 | 설명 |
|:---|:---|
| 1 | 피해자가 `https://victim-bank.com`에 로그인 (세션 쿠키 보유) |
| 2 | 피해자가 공격자의 `https://evil.com` 방문 |
| 3 | evil.com 페이지가 victim-bank.com API 호출 (XHR/Fetch) |
| 4 | victim-bank.com이 evil.com Origin을 허용 (오설정) |
| 5 | 브라우저가 피해자 쿠키와 함께 요청 전송 |
| 6 | 계좌 정보·거래 내역 탈취 |

```
┌──────────────────────────────────────────────────────────────┐
│            CORS Misconfiguration 공격 흐름                   │
├──────────────────────────────────────────────────────────────┤
│  [evil.com]                                                  │
│     │ fetch("https://api.bank.com/balance", {credentials:    │
│     │        "include"})                                     │
│     ▼                                                        │
│  [api.bank.com] ← Origin: https://evil.com 확인             │
│     │  잘못된 설정: ACAO: https://evil.com + ACAC: true     │
│     ▼                                                        │
│  [브라우저] 피해자 쿠키 포함 응답 → evil.com에 전달           │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 은행 창구가 "내가 해당 계좌 주인이에요"라는 메모만 보여주면 잔액을 알려주는 것과 같다. 실제로 누가 메모를 쓰든 상관없이.

---

## 3. 구조 및 동작 원리

CORS Misconfiguration과 CSRF (Cross-Site Request Forgery)의 차이를 명확히 해야 한다.

| 구분 | CORS Misconfiguration | CSRF |
|:---|:---|:---|
| 피해 방식 | 응답 데이터 읽기 가능 | 피해자 권한으로 액션 수행 |
| SameSite 쿠키로 방어 | 부분적 | 효과적 |
| 공격자 요구 | Origin 허용된 도메인 통제 | 피해자가 링크/페이지 방문 |
| 위험 | 데이터 읽기·탈취 | 의도치 않은 상태 변경 |

📢 **섹션 요약 비유**: CORS 오설정은 남의 은행 잔액을 몰래 볼 수 있는 것이고, CSRF는 남의 계좌에서 돈을 이체하게 만드는 것이다.

---

## 4. 비교 및 트레이드오프

**안전한 CORS 설정 원칙**:
1. **엄격한 화이트리스트**: 허용 Origin을 정적 목록으로 관리, 요청 Origin과 비교
2. **null Origin 비허용**: `ACAO: null` 사용 금지
3. **불필요한 ACAC 제거**: `Access-Control-Allow-Credentials: true` 최소화
4. **Vary: Origin 헤더**: 캐시가 Origin별로 다른 응답을 구분하도록 설정
5. **Preflight 검증**: OPTIONS 요청의 Method·Headers도 엄격히 검증
6. **SameSite 쿠키**: `SameSite=Strict` 또는 `SameSite=Lax`로 CSRF 동시 방어

```nginx
# 올바른 예시 (Nginx)
if ($http_origin ~* "^https://(trusted-app.com|api.trusted.com)$") {
    add_header 'Access-Control-Allow-Origin' "$http_origin";
}
```

�� **섹션 요약 비유**: 초대 손님 목록을 미리 작성해두고, 그 목록에 있는 이름만 입장시키는 것이 올바른 CORS 설정이다.

---

## 5. 실무 적용 및 최적화 기법

엄격한 CORS 정책과 SameSite 쿠키를 조합하면 교차 출처 데이터 탈취와 CSRF를 동시에 방어할 수 있다. 특히 API Gateway 수준에서 통합 CORS 정책을 관리하면 개별 서비스별 오설정 위험을 줄일 수 있다.

기술사 관점에서 CORS 오설정은 A01 Broken Access Control의 한 형태다. 클라이언트 측 SOP 메커니즘에 의존하는 것이 아니라, 서버 측에서 명시적으로 신뢰 도메인을 정의하고 관리하는 아키텍처가 필요하다.

📢 **섹션 요약 비유**: CORS 보안은 문을 잠그는 것만큼 중요하다. "누구나 들어올 수 있지만 아무것도 가져갈 수 없다"는 착각이 가장 위험한 오설정이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SOP (Same-Origin Policy) | 기반 정책 | 기본 교차 출처 차단 |
| CSRF | 연관 공격 | 교차 출처 상태 변경 |
| SameSite 쿠키 | 보완 방어 | 쿠키 교차 사이트 전송 제한 |
| Preflight | CORS 메커니즘 | 본 요청 전 권한 확인 |
| Access-Control-Allow-Credentials | 핵심 설정 | 자격증명 포함 여부 |

### 👶 어린이를 위한 3줄 비유 설명
- CORS는 웹사이트가 "이 손님은 우리 친구야"라고 인정하는 규칙인데, 잘못 설정하면 나쁜 사람도 "친구예요"라고 속일 수 있어.
- 그러면 나쁜 웹사이트가 내 은행 계좌 정보를 몰래 볼 수 있게 돼.
- 그래서 초대받은 사이트 목록을 미리 정확하게 정해 놓는 게 중요해!
