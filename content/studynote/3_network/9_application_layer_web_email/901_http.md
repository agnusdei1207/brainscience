+++
weight = 1
title = "HTTP (Hypertext Transfer Protocol)"
description = "웹의 기반 프로토콜 HTTP의 버전별 발전, 요청/응답 구조, 상태 관리 메커니즘을 다룬다."
date = 2024-01-28

[extra]
categories = ["studynote-software-engineering"]
topics = ["application-layer", "http", "https", "rest"]
study_section = ["section-9-application-layer-web-email"]

number = "901"
core_insight = "HTTP는 웹의 기반 애플리케이션 프로토콜로, 요청-응답 모델로 동작하며, stateless 특성으로 확장성 있게 설계되었다. HTTP/1.1에서 Keep-Alive, HTTP/2에서 멀티플렉싱, HTTP/3에서 QUIC 기반으로 진화하고 있다."
key_points = ["요청-응답 모델 (Request-Response)", "Stateless 프로토콜", "HTTP/1.1 vs HTTP/2 vs HTTP/3 차이", "Cookie 기반 세션 관리"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: HTTP는 하이퍼텍스트(HTML) 문서를传输하는 애플리케이션 프로토콜로, 요청-응답 모델과 stateless 특성을 가진다.
> 2. **가치**: 웹 브라우징의 기반이며, REST API를 통해 대규모 분산 시스템의 통신 규격으로 활용된다.
> 3. **융합**: HTTP/2의 멀티플렉싱, HTTP/3의 QUIC 기반传输으로 웹 성능이 지속적으로 개선되고 있다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

**개념**: HTTP(Hypertext Transfer Protocol)는 RFC 1945(HTTP/1.0), RFC 2616(HTTP/1.1), RFC 7540(HTTP/2), RFC 9114(HTTP/3)로 발전해온 애플리케이션 계층 프로토콜이다. 클라이언트가 요청(Request)을 보내고, 서버가 응답(Response)을 반환하는 요청-응답 모델로 동작한다. HTTP는 stateless 프로토콜로, 각 요청은독립적으로 처리되어 이전 요청의 상태를保存하지 않는다. 그러나 Cookie와 Session을 통해 상태를管理할 수 있다.

**필요성**: 월드와이드웹(WWW)의爆発적 성장과 함께, 웹 페이지와 웹 애플리케이션의 복잡도가 증가했다. 초기 HTTP는 단순한 문서传输에 설계되었으나, 현재는 동적 콘텐츠, 실시간 통신, REST API 등 매우 다양한用途에 사용된다. 성능 최적화를 위해 HTTP/2의 헤더 압축과 멀티플렉싱, HTTP/3의 QUIC 기반.zero-RTT 연결 설정 등이 도입되었다.

**비유**: HTTP는 **호텔 리셉션 시스템**과 같다. 손님이 요청하면(요청), 리셉션이 방을 찾아서 안내하고(응답), 다음 손님이 오면 이전 손님을모르며 또다시 안내한다(stateless). 하지만 리셉션이 멤버십 카드(쿠키)를 주면, 다음 방문 때도 그 손님을 안다(상태 관리).

**등장 배경**: 1989년 CERN의 Tim Berners-Lee가 HTTP를 고안했고, 1996년 HTTP/1.0이 표준화되었다. 이후 HTTP/1.1이200개 이상의 확장을 포함하여2007년까지 주류 버전이었다. 2015년 HTTP/2, 2022년 HTTP/3이 등장하며 현재까지 발전하고 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### HTTP 요청-응답 구조

HTTP 메시지는 시작 줄, 헤더, 본문(선택)으로 구성된다. 요청 메시지는 메서드, URI, HTTP 버전으로 시작하며, 응답 메시지는 HTTP 버전, 상태 코드, 상태 메시지로 시작한다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    HTTP 요청-응답 메시지 구조                           │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【HTTP 요청 메시지】                                                     │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  GET /index.html HTTP/1.1                              ← 시작줄   │   │
│  │  Host: www.example.com                                 ← 헤더     │   │
│  │  User-Agent: Mozilla/5.0                                       │   │
│  │  Accept: text/html, application/xhtml+xml                     │   │
│  │  Accept-Language: ko-KR, ko;q=0.9, en;q=0.8                   │   │
│  │  Accept-Encoding: gzip, deflate, br                           │   │
│  │  Connection: keep-alive                                       │   │
│  │                                                         ← 빈 줄     │   │
│  │  (본문 없음 - GET 요청)                                         │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  【HTTP 응답 메시지】                                                     │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  HTTP/1.1 200 OK                                      ← 시작줄   │   │
│  │  Date: Mon, 27 Jan 2024 00:00:00 GMT                   ← 헤더     │   │
│  │  Server: Apache/2.4.52                                         │   │
│  │  Content-Type: text/html; charset=UTF-8                       │   │
│  │  Content-Length: 1256                                         │   │
│  │  Last-Modified: Sun, 26 Jan 2024 12:00:00 GMT                 │   │
│  │  Cache-Control: max-age=3600                                    │   │
│  │  Connection: keep-alive                                         │   │
│  │                                                         ← 빈 줄     │   │
│  │  <!DOCTYPE html>                                        ← 본문     │   │
│  │  <html>                                                         │   │
│  │  ...                                                            │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  주요 HTTP 메서드:                                                      │
│  • GET: 리소스 요청 (반환)                                             │
│  • POST: 데이터 제출 (처리 요청)                                         │
│  • PUT: 리소스 생성/수정                                               │
│  • DELETE: 리소스 삭제                                                 │
│  • PATCH: 부분 수정                                                    │
│  • HEAD: 헤더만 요청 (본문 없음)                                        │
│  • OPTIONS: 지원 메서드 질의                                            │
│                                                                       │
│  주요 상태 코드:                                                        │
│  • 2xx: 성공 (200 OK, 201 Created, 204 No Content)                   │
│  • 3xx: 리다이렉션 (301 Moved Permanently, 304 Not Modified)        │
│  • 4xx: 클라이언트 오류 (400 Bad Request, 401 Unauthorized,          │
│           403 Forbidden, 404 Not Found)                               │
│  • 5xx: 서버 오류 (500 Internal Server Error, 502 Bad Gateway,       │
│           503 Service Unavailable)                                    │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** HTTP 메시지의 구조는 매우 규칙적이다. 시작 줄에는 요청의 경우 메서드와 URI가, 응답의 경우 버전과 상태 코드가 있다. 헤더는冒頭にColon(:)으로 구분되는 키-값 쌍으로, 요청/응답에 대한附加情報를 제공한다. 빈 줄 다음이 본문으로, GET 요청에는 없고 POST/PUT 요청에는 데이터가 포함된다. HTTP/1.1에서는 한 TCP 연결에서 여러 요청/응답을 순차적으로 처리하므로( keep-alive), 요청 #1의 응답이 완전히 돌아올 때까지 요청 #2를 보낼 수 없다(Head-of-Line Blocking).

### HTTP/1.1 vs HTTP/2 vs HTTP/3

| 항목 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|:---|:---|:---|:---|
| **전송** | TCP 위에서 plaintext | TCP 위에서 binary framing | **UDP 위에서 QUIC** |
| **멀티플렉싱** | 없음 (HOL Blocking) | **있음** (스트림 독립) | **있음** (개선됨) |
| **헤더 압축** | 없음 (평문 반복) | **HPACK** | **QPACK** |
| **서버 푸시** | 없음 | **있음** | **있음** |
| **연결 수립** | 3-way TCP + TLS | 3-way TCP + TLS | **1-RTT 또는 0-RTT** |
| **Head-of-Line Blocking** | 있음 | **TCP 레벨에서 발생** | **없음** |
| **현재 점유율** | ~30% | ~35% | ~35% |

```
┌───────────────────────────────────────────────────────────────────────┐
│                    HTTP/2 멀티플렉싱 vs HTTP/1.1 HOL Blocking          │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【HTTP/1.1: 순차 요청-응답 (HOL Blocking)】                           │
│                                                                       │
│  Client ──▶ GET /a.jpg ──▶ Server                                     │
│  Client ◀── 200 OK ◀── Server                                         │
│                      (이미지 로딩 완료까지 대기)                           │
│            Client ──▶ GET /b.jpg ──▶ Server                           │
│            Client ◀── 200 OK ◀── Server                              │
│                                                                       │
│  → 요청 #2는 응답 #1이 끝나야 시작 가능 → 불필요한 대기                 │
│                                                                       │
│  【HTTP/2: 병렬 스트림 (멀티플렉싱)】                                   │
│                                                                       │
│  Client ──▶ [Stream 1: GET /a.jpg] ──▶ Server                        │
│  Client ──▶ [Stream 2: GET /b.jpg] ──▶ Server                        │
│  Client ──▶ [Stream 3: GET /c.jpg] ──▶ Server                        │
│  Client ◀── [Stream 1: 200 OK] ◀── Server                            │
│  Client ◀── [Stream 3: 200 OK] ◀── Server                            │
│  Client ◀── [Stream 2: 200 OK] ◀── Server                            │
│                                                                       │
│  → 모든 요청이 동시에 전송/수신 → HOL Blocking 해결                     │
│  → 스트림별로 독립적으로 처리                                             │
│                                                                       │
│  【HTTP/3: QUIC 기반】                                                 │
│                                                                       │
│  • UDP 위에서 동작 → TCP의 HOL Blocking 없음                           │
│  • 연결 수립 지연 감소 (0-RTT, 1-RTT)                                 │
│  • 스트림이 QUIC 내에서 독립 → 하나의 스트림 지연이 다른 스트림에 영향 X  │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** HTTP/1.1의 가장 큰 문제점은 Head-of-Line(HOL) Blocking이다. TCP 연결에서 요청 #1의 응답이 완전히 돌아와야 다음 요청을 보낼 수 있으므로, 앞선 요청의 응답이 느리면 뒤의 모든 요청이 대기한다. HTTP/2는 바이너리 프레이밍을 통해 여러 스트림을 동시에 multiplex하여 이 문제를 해결한다. 그러나 HTTP/2는 여전히 TCP 위에서 동작하므로, TCP 레벨의 HOL Blocking이 발생할 수 있다. HTTP/3는 QUIC(UDP 기반)을 사용하여 TCP의 HOL Blocking을 원천 제거했다. 하나의 스트림에서 패킷 유실이 발생해도, 다른 스트림에는 영향을 주지 않는다.

### Cookie와 Session

HTTP는 stateless이므로, 상태 관리(Session)를 위해 Cookie를 사용한다. 서버가 Set-Cookie 헤더로 클라이언트에 쿠키를 전달하면, 클라이언트는 이후 요청 시 Cookie 헤더에 해당 쿠키를 포함하여 보낸다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    HTTP Cookie 동작 과정                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ① 처음 방문:                                                          │
│  Client ──▶ GET /login HTTP/1.1 ──▶ Server                           │
│             (쿠키 없음)                                                │
│  Server ◀── HTTP/1.1 200 OK ◀── Server                               │
│             Set-Cookie: session_id=abc123; Path=/; HttpOnly         │
│  Client 쿠키 저장: session_id=abc123                                  │
│                                                                       │
│  ② 이후 요청:                                                          │
│  Client ──▶ GET /dashboard HTTP/1.1 ──▶ Server                        │
│             Cookie: session_id=abc123                                 │
│  Server 세션 저장소에서 session_id=abc123 조회 → 사용자 확인           │
│  Server ◀── HTTP/1.1 200 OK ◀── Server                               │
│                                                                       │
│  쿠키 속성:                                                            │
│  • HttpOnly: JavaScript에서 접근 불가 (XSS 방지)                       │
│  • Secure: HTTPS에서만 전송                                            │
│  • SameSite: CSRF 방지 (Strict/Lax/None)                              │
│  • Expires/Max-Age: 쿠키 만료 시간                                     │
│  • Path: 쿠키가 전송될 URL 경로                                        │
│                                                                       │
│  세션 저장 위치:                                                        │
│  • Client-side Session: 쿠키에 전체 세션 데이터 저장 (Base64 인코딩)   │
│  • Server-side Session: 쿠키에 세션 ID만 저장, 서버에 데이터 저장       │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### HTTP 상태 관리 기법 비교

| 기법 | 동작 | 장점 | 단점 |
|:---|:---|:---|:---|
| **Cookie** | 서버→클라이언트 쿠키 전달 | 간단, 널리 지원 | 크기 제한, 보안 주의 |
| **Session** | 서버에 세션 저장, ID만 쿠키로 | 대량 데이터 저장 가능 | 서버 리소스 사용 |
| **JWT** | Self-contained 토큰 (Base64) | Stateless, 서버 부담 적음 | 토큰 크기, 만료 주의 |
| **Authorization Header** | 매 요청마다 자격 증명 전송 | 단순 | 보안 위험 (매번 인증) |

### REST API 설계 원칙

| 원칙 | 설명 |
|:---|:---|
| **Client-Server** | 클라이언트와 서버가 독립적으로 분리 |
| **Stateless** | 각 요청이 필요한 모든 정보를 포함 |
| **Cacheable** | 응답 캐시 가능 여부 명시 |
| **Uniform Interface** | 일관된 인터페이스 (URI, HTTP 메서드) |
| **Layered System** | 계층 구조 가능 (LB, Gateway) |
| **Code on Demand** | 서버가 코드 전송 가능 (선택적) |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 1 — HTTP/2에서 HTTP/3 전환**: HTTP/3은 QUIC 기반으로, 패킷 유실 시 다른 스트림에 영향이 없다. 특히 모바일 환경(네트워크 전환 빈번), 고대역폭 환경에서 효과적이다. 전환 방법: 서버가 Alt-Svc 헤더로 HTTP/3 사용 가능한ことを 알리거나, DNS에서 _https._tcp CNAME 레코드로 advertisement한다.

**시나리오 2 — REST API 설계**: RESTful API를 설계할 때, 리소스는 URI로Identification하고, HTTP 메서드로 작업을 표현한다. 예: GET /users (사용자 목록), POST /users (생성), GET /users/123 (상세), PUT /users/123 (수정), DELETE /users/123 (삭제). 상태 코드를 정확히 사용하고(201 Created, 404 Not Found 등), versioning을URI에 포함(/v1/users)하거나 Accept 헤더로 처리한다.

### 도입 체크리스트

- **기술적**: HTTP 버전 선택 (가능하면 HTTP/2 이상), TLS 필수(HTTPS), 압축 활성화
- **운영·보안적**: 쿠키 보안 属性(HttpOnly, Secure, SameSite) 설정, 불필요한 헤더 제거

### 안티패턴

- **HTTP/1.1의 HOL Blocking 미해결**: 이미지 CDN 사용으로 domains 분산(요청 병렬화)하여HTTP/1.1의 한계를规避하는 것은 과거 방법.
- **쿠키에 민감 정보 저장**: 세션 ID만 저장하고, 실제 데이터는 서버 세션 저장소에 보관해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

HTTP/3의 점유율이 빠르게 증가하고 있으며, 2026년까지 과반수를 넘을 것으로 예측된다. QUIC의 이점으로 웹 성능이 지속적으로 개선될 것이다. 또한 WebSocket, Server-Sent Events, gRPC 등 HTTP 기반의 양방향 통신 기술도 함께 발전하고 있다.

### 참고 표준

- RFC 9110 — HTTP Semantics
- RFC 9111 — HTTP/1.1
- RFC 7540 — HTTP/2
- RFC 9114 — HTTP/3

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **HTTPS** | HTTP over TLS로, HTTP의 암호화된 버전이다. |
| **HTTP/2** | 멀티플렉싱, 헤더 압축, 서버 푸시를 지원하는 HTTP의 두 번째 메이저 버전이다. |
| **HTTP/3** | QUIC 기반의 HTTP의 세 번째 버전으로, TCP HOL Blocking을 해결했다. |
| **REST API** | HTTP 메서드를 활용한 웹 서비스 설계 스타일이다. |
| **WebSocket** | HTTP 업그레이드를 통한 양방향 통신 프로토콜이다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. HTTP는 **호텔服务员에게 손님이 물어보는 것**과 같아요. "방 있어?"(요청), "있어요!"(응답), "wififi 비밀번호 뭐예요?"(또 요청), "1234"(또 응답).服务员는 매번 처음부터 생각해요 (stateless).
2. 但し服务员が常連客を知っている (쿠키), だから「いつも와이파이 꺼」라고 알아서 도와줘요.
3. HTTP/2は 여러 질문를 동시에 (멀티플렉싱) 받을 수 있어서, HTTP/1.1보다hotel服务员が 더 빠르게 대답해 줄 수 있어요!
