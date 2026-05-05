+++
weight = 868
title = "868. HTTP Response Splitting (HTTP 응답 분할)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: HTTP Response Splitting (HTTP 응답 분할)은 HTTP 응답 헤더에 개행 문자(`

> 📝 모범 답안

`, `
`)를 삽입해 응답을 임의로 분리하고, 완전히 새로운 HTTP 응답을 주입하는 헤더 인젝션 공격이다.
> 2. **가치**: 공격에 성공하면 XSS, 웹 캐시 포이즈닝, 쿠키 인젝션, 피싱 등 다양한 2차 공격이 가능하며, 특히 캐시 서버가 있는 환경에서 캐시 포이즈닝 피해가 크다.
> 3. **판단 포인트**: 헤더 값에 사용자 입력을 포함할 때 개행 문자(`CR`, `LF`)를 반드시 제거하거나 인코딩해야 하며, 현대 웹 프레임워크는 대부분 이를 자동 처리한다.

---

## 1. 개요 및 필요성

HTTP/1.1 헤더는 `
`(CRLF, Carriage Return Line Feed)으로 구분된다. 서버가 사용자 입력을 헤더 값에 그대로 포함할 때, 공격자가 `
` 문자를 입력에 삽입하면 헤더가 중간에 끊기고 새로운 헤더나 완전히 새로운 HTTP 응답이 시작된다.

이를 CRLF Injection 또는 HTTP Header Injection이라고도 부른다. 단순한 헤더 주입부터 전체 응답 분할까지 다양한 변형이 존재한다.

```text
┌──────────────────────────────────────────────────────────────┐
│              HTTP Response Splitting 공격                    │
├──────────────────────────────────────────────────────────────┤
│  취약한 코드:                                                 │
│  response.setHeader("Location", request.getParam("url"))     │
│                                                              │
│  악성 입력:                                                   │
│  url = "/safe
Content-Length: 0

HTTP/1.1 200 OK
│
│  Content-Type: text/html

<script>attack()</script>"   │
│                                                              │
│  생성된 응답:                                                 │
│  HTTP/1.1 302 Found                                          │
│  Location: /safe                                             │
│  Content-Length: 0                                           │
│                                                              │
│  HTTP/1.1 200 OK                  ← 두 번째 응답 주입!       │
│  Content-Type: text/html                                     │
│                                                              │
│  <script>attack()</script>                                   │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: HTTP Response Splitting은 편지 중간에 "편지 끝" 도장을 위조해서 다음 내용을 완전히 다른 편지로 만들어 끼워 넣는 것이다.

---

## 2. 구성요소

### 공격 시나리오와 방어

| 공격 변형 | 삽입 대상 | 피해 |
|:---|:---|:---|
| CRLF 인젝션 | 모든 응답 헤더 | 임의 헤더 추가 |
| 쿠키 인젝션 | Set-Cookie 헤더 | 세션 쿠키 조작 |
| 캐시 포이즈닝 | Location 헤더 | 악성 응답 캐시 |
| 응답 분할 XSS | 응답 본문 주입 | 스크립트 실행 |

```text
┌──────────────────────────────────────────────────────────────┐
│               방어 구현 (Python 예시)                         │
├──────────────────────────────────────────────────────────────┤
│  # 취약한 코드                                               │
│  redirect_url = request.args.get('url')                      │
│  response.headers['Location'] = redirect_url  # 위험!        │
│                                                              │
│  # 안전한 코드: CR, LF 문자 제거                             │
│  def sanitize_header(value):                                 │
│      return value.replace('
', '').replace('
', '')        │
│  safe_url = sanitize_header(redirect_url)                    │
│                                                              │
│  # 현대 프레임워크: 자동 처리                                │
│  # Flask, Django, Spring: 헤더에 CRLF 자동 거부              │
└──────────────────────────────────────────────────────────────┘
```

현대 웹 프레임워크(Flask, Django, Spring, Express.js)는 응답 헤더 설정 시 CRLF 문자를 자동으로 거부하거나 인코딩한다. 그러나 저수준 HTTP 라이브러리를 직접 사용하거나 레거시 시스템에서는 여전히 취약점이 존재할 수 있다.

📢 **섹션 요약 비유**: CRLF 제거는 편지에 "편지 끝" 도장 위조를 막기 위해 편지 내용에서 인장 문자를 모두 지우는 검열이다.

---

## 3. 구조 및 동작 원리

| 항목 | HTTP Response Splitting | HTTP Request Smuggling |
|:---|:---|:---|
| 조작 대상 | 서버 응답 헤더 | 서버 요청 처리 |
| 공격 위치 | 응답 헤더 파라미터 | Content-Length vs Transfer-Encoding |
| 주요 피해 | 캐시 포이즈닝, XSS | 요청 처리 혼란, 보안 통제 우회 |
| 방어 핵심 | CRLF 필터링 | 헤더 일관성 검증 |

HTTP Request Smuggling은 유사하지만 다른 공격으로, 프론트엔드와 백엔드 서버 간의 HTTP 요청 경계 해석 차이를 이용한다.

📢 **섹션 요약 비유**: HTTP Response Splitting과 HTTP Request Smuggling은 같은 우체국(HTTP)에서 다른 방법으로 편지를 위조하는 두 가지 공격이다.

---

## 4. 비교 및 트레이드오프

**취약한 패턴 탐지**:
1. `response.setHeader()`, `header()` 함수에 사용자 입력 직접 전달 여부 확인
2. URL 파라미터 값이 `Location`, `Set-Cookie` 헤더에 포함되는지 확인
3. `%0d%0a` (CRLF URL 인코딩)를 파라미터로 주입해 응답 헤더 확인

**보안 테스트**:
- 도구: Burp Suite Intruder에 CRLF 페이로드 삽입
- 페이로드: `%0d%0a%0d%0a<script>alert(1)</script>`

📢 **섹션 요약 비유**: HTTP Response Splitting 테스트는 편지봉투에 숨겨진 위조 도장을 찾기 위해 UV 램프로 조사하는 것과 같다.

---

## 5. 실무 적용 및 최적화 기법

HTTP Response Splitting 방어를 통해 웹 캐시 포이즈닝, XSS, 쿠키 인젝션 등 연쇄 공격을 차단할 수 있다. 현대 프레임워크는 자동으로 방어하지만, 레거시 코드와 저수준 HTTP 처리 코드에 대한 정기 감사가 필요하다.

최신 HTTP/2, HTTP/3 환경에서는 헤더 구분 방식이 변경되어 전통적인 CRLF 인젝션의 적용 범위가 줄었지만, HTTP/1.1을 지원하는 레거시 시스템과 프록시에서는 여전히 유효한 공격이다.

📢 **섹션 요약 비유**: HTTP Response Splitting 완전 방어는 편지 배달 시스템 자체를 현대화해서 도장 위조가 물리적으로 불가능한 디지털 서명 체계(HTTP/2 헤더)로 바꾸는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CRLF Injection | 동의어 | HTTP Response Splitting의 다른 이름 |
| 웹 캐시 포이즈닝 | 결합 공격 | 오염된 응답이 캐시에 저장 |
| HTTP Request Smuggling | 유사 공격 | 요청 경계 해석 차이 악용 |
| Set-Cookie 인젝션 | 변형 공격 | 쿠키 값 조작 |
| HTTP/2 | 완화 요소 | CRLF 헤더 분리 미사용 |

### 👶 어린이를 위한 3줄 비유 설명
- HTTP Response Splitting은 편지 중간에 "여기서 끝"이라고 써서 그 뒤에 다른 편지를 끼워 넣는 거예요.
- 받는 사람(브라우저)은 두 번째 편지도 진짜 편지라고 생각해요.
- 편지에 "여기서 끝" 표시를 쓸 수 없도록 규칙을 만들면(CRLF 필터링) 막을 수 있어요!
