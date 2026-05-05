+++
weight = 483
title = "483. CORS Preflight (교차 출처 리소스 공유 사전 요청)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: CORS (Cross-Origin Resource Sharing) Preflight는 브라우저가 실제 요청 전에 `OPTIONS` 메서드로 서버에 허용 여부를 사전 확인하는 메커니즘으로, SOP (Same-Origin Policy) 완화를 안전하게 수행하기 위한 장치이다.
> 2. **가치**: 서버가 명시적으로 허용한 출처·메서드·헤더만 크로스 오리진 요청이 가능하므로, 무분별한 크로스 오리진 요청으로 인한 CSRF (Cross-Site Request Forgery) 유사 공격을 방지한다.
> 3. **판단 포인트**: `Access-Control-Allow-Origin: *`와 `Access-Control-Allow-Credentials: true`를 동시에 설정하면 보안 취약점이 발생하며 브라우저도 이를 거부한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

SOP는 기본적으로 다른 출처로의 요청을 차단하지만, 현대 웹(API 서버, CDN, 마이크로서비스)은 크로스 오리진 요청이 필수적이다. CORS는 W3C (World Wide Web Consortium) 표준으로 이를 안전하게 허용한다.

Preflight 요청은 다음 조건 중 하나가 해당될 때 발생한다.
- HTTP 메서드가 GET·POST·HEAD가 아닌 경우(PUT, DELETE, PATCH 등)
- Content-Type이 `text/plain`, `multipart/form-data`, `application/x-www-form-urlencoded` 이외인 경우
- 커스텀 요청 헤더가 포함된 경우

📢 **섹션 요약 비유**: 파티장(서버)에 들어가기 전에 문지기(Preflight)에게 먼저 초대받았는지 물어보는 절차이다.

---

## 2. 구성요소

| 응답 헤더 | 역할 | 예시 |
|:---|:---|:---|
| Access-Control-Allow-Origin | 허용 출처 | `https://app.example.com` |
| Access-Control-Allow-Methods | 허용 메서드 | `GET, POST, PUT` |
| Access-Control-Allow-Headers | 허용 헤더 | `Content-Type, Authorization` |
| Access-Control-Max-Age | Preflight 캐시 | `3600` (초) |
| Access-Control-Allow-Credentials | 쿠키 포함 허용 | `true` |

```
브라우저 (origin: app.example.com)
  │
  │ OPTIONS /api/data HTTP/1.1
  │ Origin: https://app.example.com
  │ Access-Control-Request-Method: PUT
  ▼
API 서버
  │ HTTP/1.1 204 No Content
  │ Access-Control-Allow-Origin: https://app.example.com
  │ Access-Control-Allow-Methods: GET, PUT
  ▼
브라우저 판단: 허용됨
  │
  │ PUT /api/data HTTP/1.1  ← 실제 요청
  ▼
API 서버 처리
```

📢 **섹션 요약 비유**: 식당(API)에 예약 전화(Preflight)를 먼저 하고 실제 방문(본 요청)하는 것이다.

---

## 3. 구조 및 동작 원리

| 요청 유형 | Preflight 발생 여부 | 이유 |
|:---|:---|:---|
| GET + 단순 헤더 | 없음 | Simple Request |
| POST + JSON body | 있음 | Content-Type 비표준 |
| DELETE | 있음 | 비표준 메서드 |
| Authorization 헤더 | 있음 | 커스텀 헤더 |

Simple Request(단순 요청)는 Preflight 없이 바로 전송되므로 CSRF와 유사한 위험이 있다. 이 때문에 서버 사이드 CSRF 방어는 여전히 필요하다.

📢 **섹션 요약 비유**: 간단한 심부름(Simple Request)은 예약 없이 바로 가지만, 복잡한 업무(비표준 메서드)는 반드시 사전 예약이 필요하다.

---

## 4. 비교 및 트레이드오프

**잘못된 설정(취약)**:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true  ← 브라우저 오류 발생
```

**올바른 설정**:
```
Access-Control-Allow-Origin: https://trusted.app.com  # 특정 출처만
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT
```

**기술사 논점**: "CORS 설정 오류(와일드카드 + Credentials)는 세션 하이재킹 경로를 열어주므로, 허용 출처는 반드시 명시적으로 지정해야 한다."

📢 **섹션 요약 비유**: 파티에 아무나 초대(wildcard)하면서 와인(쿠키)도 마음대로 마시게 하는 것은 파티 난장판의 시작이다.

---

## 5. 실무 적용 및 최적화 기법

Preflight 메커니즘과 명시적 CORS 설정을 통해 신뢰된 출처만 API에 접근하도록 제한하면 크로스 오리진 공격 표면이 최소화된다. `Access-Control-Max-Age` 설정으로 Preflight 캐시를 활용하면 성능과 보안을 동시에 달성한다.

📢 **섹션 요약 비유**: 사전 예약 시스템(Preflight)이 있으면 불청객 없이 초대받은 손님만 파티장에 입장할 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SOP | 기반 | 크로스 오리진 기본 차단 정책 |
| Simple Request | 관련 | Preflight 없이 전송되는 요청 |
| OPTIONS 메서드 | 메커니즘 | Preflight HTTP 메서드 |
| Credentials | 위험 요소 | wildcard와 동시 사용 금지 |

### 👶 어린이를 위한 3줄 비유 설명
CORS Preflight는 낯선 집에 방문하기 전에 전화로 "방문해도 되나요?"라고 먼저 묻는 예의예요.
집 주인(서버)이 "네, 오세요"(허용 헤더)라고 해야만 방문할 수 있어요.
아무 집이나 들어가도 된다고 하면(wildcard + credentials) 도둑이 들 수 있어요.
