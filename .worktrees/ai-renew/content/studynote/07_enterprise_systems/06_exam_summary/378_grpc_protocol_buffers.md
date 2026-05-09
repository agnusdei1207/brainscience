+++
weight = 378
title = "378. gRPC 프로토콜 버퍼 직렬화 통신 (gRPC Protocol Buffers)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: gRPC(Google Remote Procedure Call)는 HTTP/2 기반 고성능 RPC 프레임워크로, Protocol Buffers(Protobuf)라는 이진 직렬화 스키마를 사용하여 REST/JSON 대비 3~10배 빠른 성능과 강타입(Strongly-typed) 계약을 제공한다.
> 2. **가치**: 양방향 스트리밍·멀티플렉싱(HTTP/2)·코드 자동 생성으로 마이크로서비스 간 내부 통신, IoT 디바이스 연결, 실시간 스트리밍 API에서 REST를 압도하는 효율을 달성한다.
> 3. **판단 포인트**: gRPC는 브라우저 직접 호출이 어렵고(gRPC-Web 필요) Protobuf의 사람이 읽기 어려운 바이너리 포맷이 디버깅을 불편하게 하므로, 외부 공개 API보다 내부 MSA 통신에 적합하다.

## Ⅰ. 개요 및 필요성

REST/JSON은 인간 친화적이고 범용적이지만, MSA 내부 서비스 간 통신에서는 ①JSON 직렬화/역직렬화 CPU 비용, ②HTTP/1.1의 헤드오브라인 블로킹, ③동적 타입으로 인한 런타임 오류 등이 성능·안정성 문제를 야기한다.

gRPC는 2015년 Google이 내부 Stubby RPC를 오픈소스화한 것으로, CNCF Incubating 프로젝트다. Protocol Buffers(Protobuf)는 1/10 크기의 바이너리 직렬화로 JSON 대비 압도적 성능을 제공한다. 언어 지원: C++, Java, Python, Go, Kotlin, Swift, Ruby, PHP 등 10개 이상.

| 비교 항목 | REST/JSON | gRPC/Protobuf |
|:---|:---|:---|
| 직렬화 | 텍스트 JSON | 바이너리 Protobuf |
| 페이로드 크기 | 100% | 10~30% (3~7배 작음) |
| 처리 속도 | 기준 | 5~10배 빠름 |
| 타입 안전성 | 느슨 (런타임 검증) | 강함 (컴파일 타임) |
| 스트리밍 | 제한적 (SSE, WebSocket) | 네이티브 양방향 스트리밍 |
| 브라우저 지원 | 직접 지원 | gRPC-Web 필요 |

📢 **섹션 요약 비유**: gRPC와 REST의 차이는 모스 부호(바이너리 Protobuf)와 일반 편지(JSON)처럼, 같은 정보도 압축된 부호가 훨씬 빠르게 전달된다.

## Ⅱ. 아키텍처 및 핵심 원리

### Protobuf 스키마 (.proto 파일)

```protobuf
syntax = "proto3";

message Order {
  string order_id     = 1;
  string customer_id  = 2;
  repeated OrderItem items = 3;
  OrderStatus status  = 4;
}

message OrderItem {
  string product_id = 1;
  int32  quantity   = 2;
  double price      = 3;
}

enum OrderStatus {
  PENDING    = 0;
  CONFIRMED  = 1;
  SHIPPED    = 2;
}

service OrderService {
  rpc CreateOrder(CreateOrderRequest) returns (Order);
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc StreamOrders(StreamOrdersRequest) returns (stream Order);
}
```

### gRPC 4가지 스트리밍 패턴

| 패턴 | 설명 | 사용 사례 |
|:---|:---|:---|
| Unary | 단일 요청 → 단일 응답 | 일반 API 호출 |
| Server Streaming | 단일 요청 → 스트림 응답 | 실시간 데이터 피드 |
| Client Streaming | 스트림 요청 → 단일 응답 | 파일 업로드, 배치 처리 |
| Bidirectional Streaming | 스트림 요청 ↔ 스트림 응답 | 채팅, IoT 실시간 제어 |

### gRPC 아키텍처

```
클라이언트 (Java/Go/Python)
  ├── .proto 파일 → protoc 컴파일 → 클라이언트 Stub 자동 생성
  └── Stub 호출 (로컬 함수처럼)

HTTP/2 멀티플렉싱 채널
  └── 다중 RPC 동시 처리 (헤드오브라인 블로킹 없음)

서버 (Java/Go/Python)
  ├── .proto 파일 → protoc 컴파일 → 서버 인터페이스 자동 생성
  └── 서비스 구현 → 등록
```

📢 **섹션 요약 비유**: Protobuf 코드 자동 생성은 설계도(proto 파일)에서 자동으로 부품(Stub/스켈레톤 코드)이 생산되는 공장처럼, 개발자가 직접 직렬화 코드를 쓸 필요가 없다.

## Ⅲ. 비교 및 연결

### REST vs GraphQL vs gRPC 선택 가이드

```
공개 외부 API (개발자 친화):
  → REST API (표준 문서화, 브라우저 친화)

복잡한 데이터 조회 (클라이언트 정의 쿼리):
  → GraphQL (Over-fetching 방지)

내부 MSA 서비스 간 고성능 통신:
  → gRPC (성능 + 타입 안전성)

실시간 양방향 스트리밍:
  → gRPC Bidirectional Streaming 또는 WebSocket
```

### gRPC-Gateway (REST ↔ gRPC 브리지)

```
외부 클라이언트 (REST JSON)
        ↓
gRPC-Gateway (Reverse Proxy)
REST → gRPC 변환
        ↓
내부 gRPC 서비스
```

📢 **섹션 요약 비유**: gRPC-Gateway는 외국어 통역처럼, 외부에서 오는 REST 요청을 내부 gRPC 언어로 자동 변환하여 최고 성능을 유지하면서 외부 호환성도 확보한다.

## Ⅳ. 실무 적용 및 기술사 판단

### gRPC 적용 판단 기준

1. **내부 MSA 통신**: 서비스 간 초당 수천 RPC → gRPC 우선 검토
2. **IoT/Edge**: 제한된 대역폭·배터리 → Protobuf 바이너리 효율적
3. **다국어 팀**: proto 스키마로 언어 무관 계약 정의 → 타입 불일치 런타임 오류 제거
4. **공개 API**: 개발자 경험 중요 → REST 유지, gRPC-Gateway로 내부 변환

### Protobuf 스키마 버전 관리

```
하위 호환 변경 (허용):
  ├── 새 필드 추가 (옵션 필드)
  ├── 새 enum 값 추가
  └── 서비스에 새 메서드 추가

비호환 변경 (금지):
  ├── 기존 필드 번호 변경
  ├── 필드 타입 변경
  └── 기존 enum 값 번호 변경
```

📢 **섹션 요약 비유**: Protobuf 필드 번호는 주민등록번호처럼, 한 번 할당되면 절대 바꾸면 안 되지만 새 번호(필드)는 언제든 추가할 수 있다.

## Ⅴ. 기대효과 및 결론

gRPC 도입 시 ①REST 대비 CPU 사용량 60~70% 감소, ②네트워크 대역폭 70~80% 절감(바이너리 직렬화), ③컴파일 타임 타입 검증으로 런타임 오류 감소, ④HTTP/2 멀티플렉싱으로 연결 효율 향상 등의 효과를 기대할 수 있다. Google, Netflix, Square, Lyft 등이 내부 MSA 통신에 gRPC를 표준으로 채택하고 있다.

**한계**: Protobuf의 바이너리 포맷은 사람이 직접 읽기 어려워 디버깅·로깅이 불편하다. 또한 브라우저의 직접 gRPC 호출이 불가(HTTP/2 트레일러 제한)하여 gRPC-Web 또는 gRPC-Gateway가 필요하다.

📢 **섹션 요약 비유**: gRPC는 암호 전보처럼, 전문가(서버-서버)끼리 빠르고 효율적으로 통신하지만 일반인(브라우저)이 직접 읽기엔 번역기(gRPC-Web)가 필요하다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| REST API | 비교 | 외부 공개 API의 표준, gRPC와 용도 구분 |
| HTTP/2 | 기반 | gRPC의 전송 프로토콜, 멀티플렉싱 지원 |
| MSA | 활용 맥락 | 내부 서비스 간 고성능 통신에 최적 |
| 서비스 메시 | 연계 | Envoy가 gRPC 트래픽 제어 지원 |
| GraphQL | 비교 | 클라이언트 정의 쿼리, REST/gRPC와 다른 용도 |

### 👶 어린이를 위한 3줄 비유 설명

1. gRPC는 모스 부호처럼, 같은 내용을 훨씬 적은 신호(바이너리)로 전달해서 일반 편지(JSON REST)보다 수십 배 빠르게 통신해요.
2. proto 파일은 LEGO 설명서처럼, 한 번 작성해두면 Java, Python, Go 등 어떤 언어로도 자동으로 조립 코드(Stub)가 만들어져요.
3. 단, 모스 부호는 훈련받지 않은 사람(브라우저)이 읽기 어려우므로, 외부에 공개하는 API는 여전히 일반 편지(REST) 형태가 더 편리해요.
