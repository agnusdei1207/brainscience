+++
title = "157. RESTful API 성숙도 모델 (Richardson Maturity Model)"
weight = 157
+++
## 0. 핵심 인사이트

> **핵심 인사이트**: 세상에는 무늬만 REST인 API가 많다. 레오나르드 리처드슨은 진정한 RESTful 아키텍처에 도달하기 위한 4단계(Level 0~3) 성숙도 모델을 제시했다. 자원 분리, HTTP 메서드 활용, 그리고 HATEOAS(하이퍼미디어)까지 완비해야 궁극의 REST에 도달한다.

> 📝 모범 답안

## 1. 개요 및 필요성
RESTful API 성숙도 모델(Richardson Maturity Model, RMM)은 웹 API가 얼마나 REST의 아키텍처 제약 조건을 잘 준수하고 있는지를 평가하는 4단계(Level 0 ~ Level 3) 분류 체계입니다.
이를 통해 개발자는 자신이 설계한 API가 진정한 RESTful인지 점검하고 개선 방향을 잡을 수 있습니다.

## 2. 구성요소

```text
[ 영광의 REST (The Glory of REST) ]
  ▲
  │  Level 3 : 하이퍼미디어 컨트롤 (HATEOAS)
  │  Level 2 : HTTP 메서드의 올바른 사용 (GET, POST, PUT, DELETE)
  │  Level 1 : 리소스(URI)의 분리 (개별 자원 식별)
  │  Level 0 : 단일 URI와 단일 메서드 (RPC 스타일의 늪)
  └──────────────────────────────────────────────────────────
```

### 1. Level 0: The Swamp of POX (Plain Old XML)
REST 개념이 전혀 없는 상태입니다. HTTP를 단순한 터널링(Transport) 용도로만 사용합니다.
- 단 하나의 끝점(Endpoint URI)만 존재하며, 오직 `POST` 메서드 하나만 사용하여 데이터(XML, JSON 등)를 통해 어떤 작업을 할지 서버에 지시합니다. (전통적인 SOAP 방식)
- 예: `POST /apiService` 바디에 `{ "action": "deleteUser", "id": 123 }` 전송

### 2. Level 1: Resources (자원의 분리)
모든 요청을 단일 엔드포인트로 보내는 대신, 개별적인 자원(Resource)마다 고유한 URI를 부여하기 시작하는 단계입니다.
- 단, 여전히 HTTP 메서드는 분리하지 않고 조회든 생성/삭제든 모두 `POST`나 `GET` 중 하나만 혼용해서 사용합니다.
- 예: 사용자 정보는 `POST /users/123`, 예약 정보는 `POST /reservations/456`

### 3. Level 2: HTTP Verbs (HTTP 메서드의 도입)
**현재 산업계에서 가장 대중적으로 RESTful하다고 부르는 단계**입니다. URI로 자원을 식별하고, 해당 자원에 대한 행위는 목적에 맞는 **표준 HTTP 메서드(GET, POST, PUT, DELETE)** 를 사용합니다.
- 조회 시 서버 상태를 변경하지 않음(안전성)을 보장하고, 상태 코드(200, 201, 404 등)를 명확하게 활용합니다.
- 예: `GET /users/123` (조회), `DELETE /users/123` (삭제)

### 4. Level 3: Hypermedia Controls (HATEOAS)
진정한(Glory) REST의 완성 단계입니다. HATEOAS(Hypermedia As The Engine Of Application State) 원칙이 적용됩니다.
- 클라이언트가 응답을 받았을 때, 다음 단계에 할 수 있는 **상태 전이 작업의 링크(Hyperlink)** 가 응답 메시지 안에 동적으로 포함되어 반환됩니다. 클라이언트는 API 문서를 하드코딩하지 않고 응답에 있는 링크만 따라가며 앱을 구동할 수 있습니다.
- 예: 사용자 조회 응답 JSON 내에 `"links": { "deposit": "/users/123/deposit", "delete": "/users/123" }` 포함

## 3. 구조 및 동작 원리
대부분의 실무 API는 **Level 2** 단계에 머물러 있습니다. Level 3의 HATEOAS는 프론트엔드 개발의 복잡도를 높일 수 있어, 엄격한 표준 준수보다 실용성을 중시하는 경향이 크기 때문입니다.

> 📢 **섹션 요약 비유**: Level 0은 접수처 창구 하나에 가서(단일 URI) "이거 취소해주세요"라고 말하는 것이고, Level 2는 '환불 창구'나 '접수 창구' 등 명확한 푯말(다양한 자원+메서드)을 찾아가는 것이며, Level 3는 일을 마쳤더니 직원이 "다음은 저쪽 3번 창구로 가시면 됩니다"라고 안내 지도(하이퍼링크)를 쥐여주는 완벽한 안내 시스템입니다.
