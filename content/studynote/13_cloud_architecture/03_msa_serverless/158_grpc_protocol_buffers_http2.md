+++
weight = 158
title = "158. gRPC와 프로토콜 버퍼 (gRPC / Protocol Buffers / HTTP2)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: gRPC (Google Remote Procedure Call)는 HTTP/2 위에서 Protocol Buffers (바이너리 직렬화)를 사용해 마이크로서비스 간 내부 동기 통신을 REST/JSON보다 최대 5~10배 빠르게 처리하는 고성능 RPC 프레임워크다.
> **비유**: gRPC는 서비스 간 전용 고속도로 — REST/JSON이 일반 도로라면, gRPC는 체증 없이 고속으로 달리는 전용 차선이다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

MSA 환경에서 수백 개의 마이크로서비스가 서로 빈번하게 호출할 때 HTTP/1.1 + JSON 방식의 REST API는 두 가지 성능 병목을 만든다. 첫째, JSON 직렬화·역직렬화 비용이 크다. 둘째, HTTP/1.1은 요청당 커넥션을 새로 맺거나 Keep-Alive에 의존해 헤더 오버헤드가 크다.

gRPC (Google Remote Procedure Call)는 이 문제를 HTTP/2 + Protocol Buffers (프로토콜 버퍼) 조합으로 해결한다. Protocol Buffers는 JSON 대비 3~10배 작은 바이너리 포맷으로 데이터를 직렬화하며, HTTP/2는 단일 TCP 연결 위에서 다중화(Multiplexing)·헤더 압축·서버 푸시를 지원한다.

원래 Google이 내부적으로 수십억 건의 API 호출을 처리하기 위해 개발했으며, 현재는 CNCF (Cloud Native Computing Foundation) 오픈소스 프로젝트로 공개되어 있다. Go, Java, Python, C++, Node.js 등 10개 이상의 언어를 지원한다.

---

## 2. 구성요소

| 항목 | REST/JSON | gRPC/Protobuf |
|:---|:---|:---|
| 전송 프로토콜 | HTTP/1.1 | HTTP/2 |
| 데이터 포맷 | JSON (텍스트) | Protocol Buffers (바이너리) |
| 메시지 크기 | 100% 기준 | 약 30~50% 수준 |
| 직렬화 속도 | 느림 | 약 5~10배 빠름 |
| 스키마 | 없음 (문서 의존) | `.proto` 강타입 스키마 |
| 스트리밍 | 단방향 (HTTP/2에서 가능) | 단방향·서버→클라·양방향 |
| 브라우저 지원 | 직접 | gRPC-Web 레이어 필요 |
| 코드 생성 | 없음 (OpenAPI 도구) | `.proto` → 다국어 자동 생성 |

```text
┌────────────────────────────────────────────────────────────────────┐
│                    gRPC 통신 구조                                  │
│                                                                    │
│  .proto 파일 정의:                                                 │
│  service OrderService {                                            │
│    rpc GetOrder (OrderRequest) returns (OrderResponse);            │
│    rpc StreamOrders (Empty) returns (stream OrderResponse);        │
│  }                                                                 │
│                                                                    │
│  ┌──────────────────┐          ┌──────────────────────────────┐   │
│  │   gRPC 클라이언트 │          │      gRPC 서버               │   │
│  │                  │          │                              │   │
│  │  Stub (자동생성) │─HTTP/2──►│  Handler                    │   │
│  │  GetOrder(req)   │◄─────────│  ProcessOrder(req, res)     │   │
│  │  [Protobuf 직렬화│ 바이너리  │  [Protobuf 역직렬화]        │   │
│  └──────────────────┘          └──────────────────────────────┘   │
│                                                                    │
│  HTTP/2 멀티플렉싱:                                                │
│  ┌───────────────────────────────────────────────────────────┐    │
│  │  단일 TCP 연결                                            │    │
│  │  Stream 1: 주문 조회 ──────────────────────────────►     │    │
│  │  Stream 2: 재고 확인 ───────────────────────────────►    │    │
│  │  Stream 3: 배송 조회 ────────────────────────────────►   │    │
│  └───────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 3. 구조 및 원리

**핵심 조건**: 분산 서비스 환경에서는 서비스 경계, 상태 관리, 호출 정책, 장애 격리, 데이터 일관성 전략이 명확해야 전체 시스템이 안정적으로 동작한다.

동작 순서:
1. 요청이 API 게이트웨이·이벤트 소스·메시지 브로커를 통해 유입된다.
2. 서비스 디스커버리와 라우팅 계층이 적절한 실행 주체를 결정한다.
3. 각 서비스나 함수가 독립적으로 로직을 수행하고 필요한 데이터를 조회·갱신한다.
4. 비동기 이벤트, 보상 트랜잭션, 캐시 전략으로 분산 일관성 문제를 완화한다.
5. 관측성·재시도·회로 차단·배포 전략으로 장애 전파를 제어한다.

| 구분 | Unary RPC | Server Streaming | Client Streaming | Bidirectional |
|:---|:---|:---|:---|:---|
| 방향 | 요청 1 → 응답 1 | 요청 1 → 응답 N개 스트림 | 요청 N개 → 응답 1 | 양방향 스트림 |
| 사용 예 | 일반 API 조회 | 실시간 로그/이벤트 구독 | 파일 업로드 청크 | 채팅, 실시간 게임 |
| HTTP/1.1 대응 | REST | SSE (Server-Sent Events) | FormData POST | WebSocket |

gRPC의 4가지 통신 패턴은 REST가 Unary에만 자연스럽게 맞는 것과 달리, 스트리밍 워크로드까지 네이티브로 지원한다.

---

## 4. 비교 및 연결

**내부/외부 통신 기술 선택 기준**
- 마이크로서비스 내부 동기 통신 → gRPC (성능·타입 안전성)
- 외부 공개 API (파트너·모바일) → REST 또는 GraphQL
- 실시간 스트리밍 (IoT, 실시간 대시보드) → gRPC Bidirectional Streaming
- 브라우저 직접 호출 → gRPC-Web 또는 REST

**gRPC 도입 시 고려사항**
1. `.proto` 파일 버전 관리 → 스키마 레지스트리 (Buf Schema Registry 등)
2. Load Balancer 호환성 → L7 HTTP/2 지원 여부 확인 (AWS ALB 지원)
3. 서비스 메시 (Istio, Linkerd) 연동 → 자동 mTLS + 트래픽 관리
4. 디버깅 도구 → gRPC 클라이언트(grpcurl), gRPC UI 활용

---

## 5. 실무 적용 및 판단

gRPC는 MSA 내부 통신의 성능 문제를 원천적으로 해결하는 강력한 도구다. 특히 수십~수백 개의 마이크로서비스가 초당 수만 건의 RPC를 주고받는 대규모 시스템에서 REST 대비 지연 감소·처리량 향상 효과가 명확하다.

한계로는 바이너리 포맷 특성상 Wireshark 등 네트워크 디버깅 도구로 직접 내용을 확인하기 어렵고, REST에 비해 학습 곡선이 가파르다. 그러나 `.proto` 기반 강타입 계약과 다국어 코드 자동 생성은 팀이 성장할수록 장기적으로 더 큰 생산성 이점을 제공한다.

---

## 6. 기대효과 및 결론

gRPC와 프로토콜 버퍼 (gRPC / Protocol Buffers / HTTP2)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 gRPC와 프로토콜 버퍼 (gRPC / Protocol Buffers / HTTP2)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
REST/JSON (텍스트 기반, 사람 친화)
    │
    ▼
gRPC: Protocol Buffers + HTTP/2
    ├─► 바이너리 직렬화: 10x 빠름, 70% 작은 페이로드
    ├─► 스트리밍: Unary · Server · Client · Bidirectional
    └─► IDL 기반 코드 생성: 타입 안전
    │
    ▼
내부 MSA 통신: gRPC | 외부 API: REST · GraphQL
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Protocol Buffers (Protobuf) | gRPC의 바이너리 직렬화 포맷 |
| HTTP/2 | gRPC의 전송 레이어, 다중화·헤더 압축 |
| 서비스 메시 (Service Mesh) | gRPC 트래픽을 mTLS·관찰로 관리 |
| gRPC-Web | 브라우저에서 gRPC 사용을 가능하게 하는 레이어 |
| REST (Representational State Transfer) | 외부 API에서 gRPC와 공존 |
| OpenAPI / Swagger | REST용 스키마 명세, gRPC의 `.proto`와 대응 |

---
