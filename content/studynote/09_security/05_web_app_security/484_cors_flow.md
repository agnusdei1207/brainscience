+++
weight = 484
title = "484. CORS 요청 흐름 (Cross-Origin Resource Sharing Flow)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: CORS (Cross-Origin Resource Sharing) 요청 흐름은 브라우저가 다른 출처(origin)의 리소스를 요청할 때 SOP (Same-Origin Policy)를 안전하게 완화하기 위해 거치는 헤더 교환 과정이다.
> 2. **가치**: CORS 흐름을 정확히 이해해야 API 접근 오류를 빠르게 진단하고, 보안 설정(허용 출처, 메서드, 헤더)이 올바른지 검증할 수 있다.
> 3. **판단 포인트**: 응답의 `Access-Control-Allow-Origin`이 요청의 `Origin` 헤더와 일치해야 하며, 와일드카드(`*`)는 Credentials 요청에서 사용 불가이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

브라우저는 크로스 오리진 요청 시 자동으로 `Origin` 헤더를 추가한다. 서버 응답에 `Access-Control-Allow-Origin`이 없거나 `Origin` 값과 불일치하면 브라우저는 응답을 차단하고 JavaScript에서 오류를 발생시킨다.

중요: CORS는 **서버가 응답을 보내지 않는 것이 아니라**, 브라우저가 응답을 JavaScript에 노출하지 않는 것이다. 따라서 CORS는 클라이언트 사이드 보호 메커니즘이다.

📢 **섹션 요약 비유**: 편지(요청)는 배달되지만, 우체부(브라우저)가 발신자(서버) 허가 없이 수신자(JS)에게 내용물을 보여주지 않는 것이다.

---

## 2. 구성요소

| 단계 | 요청/응답 | 주요 헤더 |
|:---|:---|:---|
| 1. Simple 요청 | GET/POST + 단순 헤더 | `Origin: https://app.com` |
| 2. 서버 응답 | CORS 허용 시 | `Access-Control-Allow-Origin: https://app.com` |
| 3. Preflight | 비단순 요청 전 | `OPTIONS + ACRM + ACRH` |
| 4. 서버 Preflight 응답 | 허용 여부 | `Access-Control-Allow-Methods` |
| 5. 실제 요청 | Preflight 통과 후 | 본 요청 전송 |

```
[CORS Simple Request 흐름]

브라우저
  origin: https://app.com
  │ GET /api/data
  │ Origin: https://app.com
  ▼
서버 (api.backend.com)
  │ 200 OK
  │ Access-Control-Allow-Origin: https://app.com
  ▼
브라우저 검증
  ├─ ACAO == Origin? → YES → JS에 응답 노출
  └─ ACAO 없음/불일치? → CORS 오류, 응답 차단

[CORS 오류 메시지]
"Access to fetch at 'https://api.backend.com/data'
 from origin 'https://app.com' has been blocked by
 CORS policy: No 'Access-Control-Allow-Origin' header"
```

📢 **섹션 요약 비유**: 도서관(서버)이 책(응답)을 주긴 하지만, 사서(브라우저)가 대출증(ACAO 헤더) 없으면 책을 독자(JS)에게 넘기지 않는다.

---

## 3. 구조 및 동작 원리

| 흐름 유형 | 조건 | Preflight |
|:---|:---|:---|
| Simple Request | GET/POST + 단순 헤더 | 없음 |
| Preflighted Request | PUT/DELETE/커스텀 헤더 | 있음 |
| Credentialed Request | withCredentials=true | 있음 + ACAC 필요 |

CORS 오류는 서버 문제가 아닌 브라우저 정책이므로, `curl`로 직접 요청하면 CORS 오류 없이 응답이 온다. 이 점이 보안 테스트 시 혼동을 야기한다.

📢 **섹션 요약 비유**: 사서(브라우저) 규칙은 일반인(JS)에게만 적용되고, 직원(curl)은 그냥 책을 가져갈 수 있다.

---

## 4. 비교 및 트레이드오프

**CORS 설정 보안 체크리스트**:
1. `Access-Control-Allow-Origin`을 특정 출처로 제한
2. `Access-Control-Allow-Origin: *` + Credentials 동시 사용 금지
3. `Access-Control-Allow-Methods`에 최소 필요 메서드만 나열
4. `Access-Control-Max-Age` 설정으로 Preflight 캐시 활용(성능)

**Spring CORS 설정 예시**:
```java
@CrossOrigin(origins = "https://app.example.com",
             methods = {RequestMethod.GET, RequestMethod.POST})
```

📢 **섹션 요약 비유**: 허용 목록(ACAO)이 정확할수록 올바른 독자만 책을 받아볼 수 있다.

---

## 5. 실무 적용 및 최적화 기법

정확한 CORS 흐름 이해를 바탕으로 올바른 설정을 적용하면, 크로스 오리진 API 접근을 안전하게 허용하면서도 무단 접근을 차단할 수 있다. 특히 Credentials 요청에서 명시적 출처 지정은 세션 탈취 방어의 핵심이다.

📢 **섹션 요약 비유**: 사서 규칙(CORS)이 정확하면 진짜 독자에게는 책을, 불청객에게는 책을 숨긴다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SOP | 기반 | 크로스 오리진 기본 차단 |
| Preflight | 메커니즘 | 비단순 요청 사전 허가 |
| ACAO | 핵심 헤더 | 허용 출처 선언 |
| Credentials | 위험 설정 | wildcard 동시 사용 금지 |

### 👶 어린이를 위한 3줄 비유 설명
CORS는 도서관(서버)이 책(응답)을 낯선 동네(다른 출처) 독자에게 줄 수 있는지 사서(브라우저)가 확인하는 규칙이에요.
도서관이 "이 동네(출처) 독자는 괜찮아요"라고 말해야(ACAO 헤더) 사서가 책을 전달해요.
아무한테나 다 준다고 하면(wildcard + credentials) 사서가 거부해요.
