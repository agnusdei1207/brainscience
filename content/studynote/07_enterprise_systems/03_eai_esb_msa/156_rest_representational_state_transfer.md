+++
title = "156. REST (Representational State Transfer) - Roy Fielding 제안 아키텍처 스타일, HTTP 메서드(GET, POST, PUT, DELETE)와 URI(자원)를 있는 그대로 활용 (SOAP 대체)"
weight = 156
+++
## 0. 핵심 인사이트

> **핵심 인사이트**: REST는 무거운 SOAP를 대체한 현대 웹 API의 표준 설계 철학이다. URI로 '어떤 자원(Resource)'인지를 명시하고, HTTP 메서드(GET, POST, PUT, DELETE)로 '무슨 행위(Action)'를 할지 직관적으로 표현한다.

> 📝 모범 답안

## 1. 개요 및 필요성
REST는 웹의 창시자 중 한 명인 로이 필딩(Roy Fielding)이 2000년 논문에서 제안한 소프트웨어 아키텍처 스타일입니다. 웹의 기존 기술과 HTTP 프로토콜을 그대로 활용하여, 자원(Resource)의 상태(State)를 주고받는 구조입니다. REST 원칙을 잘 지킨 시스템을 **RESTful** 하다고 부릅니다.

## 2. 구성요소
REST는 다음 3가지 요소로 구성됩니다.

1. **자원 (Resource)**: `URI` (예: `/users/123`) - 조작하고자 하는 대상
2. **행위 (Verb)**: `HTTP Method` - 자원에 대한 조작 (CRUD)
   - `GET` (조회), `POST` (생성), `PUT` (전체 수정), `PATCH` (부분 수정), `DELETE` (삭제)
3. **표현 (Representation)**: `JSON, XML` - 클라이언트와 서버가 데이터를 주고받는 형태

## 3. 구조 및 동작 원리

| 원칙 | 설명 |
|:---|:---|
| **Client-Server** | 클라이언트(UI)와 서버(데이터/로직)가 독립적으로 분리되어 발전할 수 있어야 합니다. |
| **Stateless (무상태성)** | 서버는 클라이언트의 상태(세션 등)를 보관하지 않습니다. 모든 요청은 처리에 필요한 모든 정보를 포함해야 합니다. |
| **Cacheable (캐시 처리 가능)** | HTTP의 캐싱 기능(ETag, Last-Modified 등)을 적용할 수 있어야 합니다. |
| **Uniform Interface** | URI 리소스 식별, 자기 서술적(Self-descriptive) 메시지 등 일관된 인터페이스를 제공해야 합니다. |

## 4. 비교 및 트레이드오프

```text
[ ❌ 안티 패턴 (행위가 URI에 포함됨) ]
GET /getUser?id=123
POST /deleteUser?id=123
POST /users/123/update

[ ✅ RESTful 방식 (자원과 행위 분리) ]
GET    /users/123   (123번 사용자 조회)
POST   /users       (새 사용자 생성)
PUT    /users/123   (123번 사용자 정보 전체 수정)
DELETE /users/123   (123번 사용자 삭제)
```

> 📢 **섹션 요약 비유**: 식당에서 주문할 때 "짜장면 하나요(POST /food/jjajang)", "주문한 거 취소할게요(DELETE /orders/1)"라고 명확하고 규칙적으로 말하는 표준 언어 체계입니다. 복잡한 서식(SOAP) 없이도 누구나 이해하고 요청할 수 있습니다.
