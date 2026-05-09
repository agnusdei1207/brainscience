+++
weight = 364
title = "364. REST API HATEOAS 성숙도 모델 (REST API Richardson Maturity Model)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Richardson 성숙도 모델(Richardson Maturity Model)은 REST API를 Level 0~3으로 평가하며, Level 3은 HATEOAS(Hypermedia As The Engine Of Application State)로 클라이언트가 링크를 따라 API 네비게이션을 스스로 수행하는 최고 수준의 RESTful API다.
> 2. **가치**: RESTful API 설계는 HTTP 표준(메서드·상태코드·헤더)을 올바르게 활용하여 API의 자기 설명성(Self-descriptiveness)·진화 가능성(Evolvability)·클라이언트-서버 결합도를 최적화한다.
> 3. **판단 포인트**: Level 2(HTTP 메서드+상태코드 준수)가 현실적 목표이며, Level 3(HATEOAS)는 API 탐색성이 중요한 공개 API나 하이퍼미디어 중심 시스템에서 의미 있는 수준이다.

## Ⅰ. 개요 및 필요성

REST(Representational State Transfer)는 2000년 Roy Fielding의 박사 논문에서 제시된 웹 아키텍처 스타일로, HTTP 프로토콜의 본래 의도에 맞게 웹 자원(Resource)을 URI로 표현하고 HTTP 메서드로 조작하는 원칙이다. Richardson Maturity Model은 2008년 Leonard Richardson이 REST 성숙도를 4단계로 분류한 실용적 가이드라인이다.

REST API는 SOAP 기반 웹서비스 대비 ①가볍고 빠름(XML → JSON), ②학습 곡선 낮음, ③브라우저/모바일 친화적, ④캐싱 용이 등의 장점으로 현재 API의 사실상 표준(De facto Standard)이다.

| REST 6가지 제약 조건 | 설명 |
|:---|:---|
| 클라이언트-서버 분리 | UI와 데이터 저장 분리 |
| 상태 없음 (Stateless) | 각 요청은 완전한 정보 포함 |
| 캐시 가능 (Cacheable) | 응답 캐시 여부 명시 |
| 계층 시스템 (Layered) | 중간 계층 투명 |
| 코드 온 디맨드 (옵션) | 클라이언트에 코드 전송 가능 |
| 통일된 인터페이스 | 자원 식별, 표현, 자기 설명, HATEOAS |

📢 **섹션 요약 비유**: Richardson 성숙도 모델은 운전 면허처럼, 1종(Level 3)이 가장 높은 수준이지만 일반 도로(Level 2)에서 충분히 잘 달릴 수 있다.

## Ⅱ. 아키텍처 및 핵심 원리

### Richardson 성숙도 모델 4단계

```
Level 0: HTTP 터널 (The Swamp of POX)
  - 단일 URI + POST 메서드만 사용
  - XML-RPC, SOAP 방식과 유사
  예: POST /api → {"action": "getCustomer", "id": 1}

Level 1: 자원 (Resources)
  - URI로 자원 구분
  - 아직 HTTP 메서드는 POST/GET만 사용
  예: GET /customers/1, GET /orders/5

Level 2: HTTP 동사 (HTTP Verbs)
  - GET/POST/PUT/PATCH/DELETE 올바르게 사용
  - HTTP 상태 코드 의미론적 사용 (200/201/404/409...)
  예: GET /customers/1 → 200 OK
      DELETE /customers/1 → 204 No Content

Level 3: 하이퍼미디어 (HATEOAS)
  - 응답에 다음 가능한 액션의 링크 포함
  - 클라이언트가 API 문서 없이도 탐색 가능
```

### Level 2 설계 원칙

| HTTP 메서드 | 의미 | 멱등성 | 안전성 |
|:---|:---|:---|:---|
| GET | 자원 조회 | ✓ | ✓ |
| POST | 자원 생성 | ✗ | ✗ |
| PUT | 자원 전체 수정 | ✓ | ✗ |
| PATCH | 자원 부분 수정 | 조건부 | ✗ |
| DELETE | 자원 삭제 | ✓ | ✗ |

### HATEOAS Level 3 응답 예시

```json
{
  "orderId": "12345",
  "status": "PENDING",
  "_links": {
    "self": { "href": "/orders/12345" },
    "payment": { "href": "/orders/12345/payment" },
    "cancel": { "href": "/orders/12345/cancel" },
    "customer": { "href": "/customers/456" }
  }
}
```

📢 **섹션 요약 비유**: HATEOAS는 웹 페이지의 하이퍼링크처럼, 지금 이 페이지에서 다음에 무엇을 할 수 있는지(링크)를 응답에 포함시키는 자기 안내 API다.

## Ⅲ. 비교 및 연결

### REST vs GraphQL vs gRPC

| 구분 | REST | GraphQL | gRPC |
|:---|:---|:---|:---|
| 쿼리 방식 | URI + HTTP 메서드 | 쿼리 언어 | 프로시저 호출 |
| 응답 구조 | 고정 (서버 정의) | 유연 (클라이언트 정의) | 고정 (Protobuf 스키마) |
| Over-fetching | 있음 | 없음 | 없음 |
| 성능 | 보통 | 보통 | 높음 (바이너리) |
| 적합 사례 | 공개 API | 복잡한 데이터 조회 | 내부 MSA 통신 |
| 캐싱 | HTTP 캐시 용이 | 복잡 | 복잡 |

### HTTP 상태 코드 핵심 정리

```
2xx 성공:
  200 OK | 201 Created | 204 No Content
4xx 클라이언트 오류:
  400 Bad Request | 401 Unauthorized | 403 Forbidden
  404 Not Found | 409 Conflict | 422 Unprocessable Entity
5xx 서버 오류:
  500 Internal Server Error | 503 Service Unavailable
```

📢 **섹션 요약 비유**: HTTP 상태코드는 우편물 처리 결과처럼, 200(배달 성공)·404(주소 없음)·500(우체국 장애)처럼 표준화된 결과 코드다.

## Ⅳ. 실무 적용 및 기술사 판단

### RESTful API 설계 가이드라인

1. **URI 명사화**: `/getCustomer` → `/customers/{id}` (동사 금지)
2. **복수형 자원**: `/customer` → `/customers`
3. **계층 표현**: `/customers/{id}/orders/{orderId}`
4. **버전 관리**: `/v1/customers` 또는 Header `Accept: application/vnd.api+json; version=2`
5. **페이지네이션**: `GET /customers?page=2&size=20`
6. **HATEOAS**: 응답에 `_links` 객체 포함 (선택적)

### API 보안 설계

```
인증: Bearer Token (JWT), OAuth 2.0
인가: RBAC (Role-Based Access Control)
전송: HTTPS (TLS 1.2+)
속도 제한: Rate Limiting (429 Too Many Requests)
입력 검증: SQL Injection, XSS 방지
```

📢 **섹션 요약 비유**: URI 명사화는 "동사 금지"처럼, `/deleteUser` 대신 `DELETE /users/1`처럼 HTTP 메서드가 동사를 이미 담당하므로 URI엔 명사만 쓴다.

## Ⅴ. 기대효과 및 결론

Richardson Level 2 이상의 RESTful API를 설계하면 ①API 직관성 향상(학습 비용 절감), ②HTTP 캐싱 활용 가능(성능 향상), ③클라이언트-서버 독립 진화, ④표준 도구(Swagger/OpenAPI) 연동 용이 등의 효과를 얻는다. Level 3(HATEOAS)는 특히 공개 API나 복잡한 상태 전이가 있는 시스템(주문 상태 전이, 의료 워크플로)에서 클라이언트의 API 탐색 자율성을 높인다.

**한계**: HATEOAS는 구현 복잡도가 높아 대부분의 실무 API가 Level 2에 머문다. 또한 REST가 모든 상황에 최적은 아니며, 실시간 스트리밍(WebSocket), 고성능 내부 통신(gRPC), 복잡한 쿼리(GraphQL)에는 다른 선택이 더 적합할 수 있다.

📢 **섹션 요약 비유**: REST API 성숙도는 한식 등급처럼, 특상급(Level 3)이 목표이지만 상급(Level 2)으로도 충분히 맛있는 밥(좋은 API)을 제공할 수 있다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| HTTP | 기반 | REST의 전송 프로토콜 및 의미론 기반 |
| OpenAPI/Swagger | 도구 | REST API 명세·문서화·테스트 표준 도구 |
| API 게이트웨이 | 연계 | REST API의 외부 노출·보안·트래픽 관리 |
| gRPC | 비교 | 고성능 바이너리 RPC, MSA 내부 통신 대안 |
| GraphQL | 비교 | 클라이언트 정의 쿼리, REST의 Over-fetching 해결 |

### 👶 어린이를 위한 3줄 비유 설명

1. REST API는 음식 주문처럼, "피자 주문해줘(POST)"·"내 주문 보여줘(GET)"·"주문 취소해줘(DELETE)"처럼 HTTP 메서드가 행동을 정확히 말해줘요.
2. HATEOAS(Level 3)는 인터넷 뱅킹 화면처럼, "이체 후 가능한 다음 작업: [영수증 출력], [다른 이체]" 버튼이 응답에 포함되어 있는 똑똑한 API예요.
3. Level 2만 잘 지켜도 누구나 쉽게 이해하고 사용할 수 있는 좋은 API가 되어, 새로운 개발자가 API 문서를 읽는 시간이 크게 줄어들어요.
