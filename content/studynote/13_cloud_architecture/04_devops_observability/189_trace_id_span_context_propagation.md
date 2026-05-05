+++
weight = 189
title = "189. Trace ID / Span ID / Context Propagation"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: Trace ID는 단일 사용자 요청 전체 여정의 고유 식별자이고, Span ID는 그 여정 중 각 서비스가 처리한 개별 구간의 식별자이며, Context Propagation은 이 식별자들을 서비스 간에 HTTP 헤더로 전달하는 메커니즘이다.
> **비유**: Trace ID는 가족 여행의 예약 번호다. 항공권, 호텔, 렌터카 예약이 각각 다른 시스템에 있어도 예약 번호 하나로 전체 여행 정보를 묶어서 조회할 수 있다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

여러 서비스에서 각자 로그를 남겨도 "이 로그가 어느 사용자 요청에서 나온 것인가?"를 연결하지 못하면 의미가 없다. Trace ID와 Span ID는 이 연결 고리다.

예를 들어 `trace_id=abc123`으로 Elasticsearch를 검색하면 인증 서비스, 결제 서비스, 알림 서비스가 각각 기록한 로그가 하나의 뷰에 시간순으로 모인다. 어느 서비스에서 오류가 발생했고 그 이전에 어떤 일이 있었는지 완전한 컨텍스트가 보인다.

Context Propagation이 없으면 각 서비스의 로그는 고아(orphan)가 되어 연결할 방법이 없다. 2019년 W3C가 표준화한 **Trace Context** 스펙(RFC)이 `traceparent`와 `tracestate` HTTP 헤더를 정의하여 플랫폼·언어 간 호환성을 보장한다.

---

## 2. 구성요소

### Trace ID / Span ID 구조

```
사용자 요청: "주문하기"

Trace ID: trace-7f4a2b9c  (전체 요청 고유값)
│
├── Root Span (API Gateway)
│   span_id: span-001
│   parent_span_id: null
│   시작: 14:32:01.000
│   종료: 14:32:01.250
│
├── Child Span (Order Service)
│   span_id: span-002
│   parent_span_id: span-001
│   시작: 14:32:01.010
│   종료: 14:32:01.200
│
│   ├── Child Span (Inventory Service)
│   │   span_id: span-003
│   │   parent_span_id: span-002
│   │   시작: 14:32:01.020
│   │   종료: 14:32:01.080
│   │
│   └── Child Span (Payment Service)
│       span_id: span-004
│       parent_span_id: span-002
│       시작: 14:32:01.090
│       종료: 14:32:01.190
│
└── Child Span (Notification Service)
    span_id: span-005
    parent_span_id: span-001
    시작: 14:32:01.200
    종료: 14:32:01.220
```

| 개념 | 형식 | 범위 | 고유성 |
|:---|:---|:---|:---|
| Trace ID | 128bit (UUID) | 전체 요청 흐름 | 글로벌 고유 |
| Span ID | 64bit | 개별 서비스 구간 | Trace 내 고유 |
| Parent Span ID | 64bit | 호출한 Span 참조 | 계층 구조 형성 |

---

## 3. 구조 및 원리

**핵심 조건**: 변경 자동화와 운영 안정성은 별개가 아니라 하나의 루프이며, 빌드·검증·배포·관측·피드백이 끊기지 않아야 지속 개선이 가능하다.

동작 순서:
1. 변경 사항을 버전 관리 시스템에서 감지한다.
2. 빌드·테스트·보안 검증으로 변경의 품질을 빠르게 확인한다.
3. 승인된 산출물을 선언형 배포나 자동화 파이프라인으로 운영 환경에 반영한다.
4. 메트릭·로그·트레이스를 통해 실제 동작 결과를 관측한다.
5. 피드백을 다음 개선 주기에 연결해 반복적으로 신뢰성을 높인다.

### W3C Trace Context 헤더 형식

```
HTTP 요청 헤더 예시:
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             ↑  ↑────────────────────────────  ↑──────────────  ↑
             버전  Trace ID (128bit/32hex)      Span ID(64bit/16hex) 플래그

tracestate: vendor1=value1,vendor2=value2
           (벤더별 추가 메타데이터)
```

| 헤더 | 역할 | 형식 |
|:---|:---|:---|
| `traceparent` | 표준 추적 컨텍스트 전파 | `version-traceid-spanid-flags` |
| `tracestate` | 벤더별 확장 데이터 | `key=value,key=value` |
| `baggage` | 앱 수준 메타데이터 전파 | `key=value` (OpenTelemetry) |

**기존 비표준 헤더들:**
- `X-B3-TraceId`: Zipkin/Brave 형식 (구형)
- `X-Request-Id`: 일부 서비스 자체 구현 (비표준)
- W3C Trace Context: 2021년 표준화, 현재 표준

---

## 4. 비교 및 연결

**Context Propagation 끊김 방지:**

```
// 나쁜 예: 새 Thread에서 컨텍스트 유실
executor.submit(() -> {
    // Trace Context가 새 Thread에 전달되지 않음!
    callNextService();
});

// 좋은 예: OTel Context 명시 전파
Context ctx = Context.current();
executor.submit(() -> {
    try (Scope scope = ctx.makeCurrent()) {
        callNextService(); // Trace Context 유지
    }
});
```

**비동기/메시지 큐에서의 전파:**
- Kafka 메시지 헤더에 Trace Context 포함
- gRPC는 metadata에 Trace Context 포함
- 비동기 작업(스레드, 큐)은 Context를 명시적으로 전달 필수

**로그와 트레이스 연결:**
```java
// MDC에 Trace ID 자동 주입 (Logback + OTel)
// 로그 출력 예: 2026-04-21 14:32:01 [trace=4bf92f35,span=00f067aa] INFO
logger.info("결제 처리 시작");
```

---

## 5. 실무 적용 및 판단

Trace ID와 Span ID를 모든 서비스와 로그에 일관되게 적용하면 "사용자 요청 하나가 어떤 경로로 처리되었는가"를 완전히 재구성할 수 있다. 고객 불만 신고 시 해당 요청의 Trace ID 하나로 전체 처리 경위를 1분 내 파악하는 것이 가능해진다.

Context Propagation의 완전성은 분산 추적 품질의 핵심이다. 하나의 서비스에서라도 헤더 전달이 누락되면 트레이스가 단절된다. 특히 레거시 서비스 통합, 비동기 처리, 외부 서비스 호출 시 누락이 자주 발생하므로, 계측 자동화(OTel Java Agent 등)와 통합 테스트로 전파 완전성을 주기적으로 검증해야 한다.

---

## 6. 기대효과 및 결론

Trace ID / Span ID / Context Propagation를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 Trace ID / Span ID / Context Propagation의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
Trace ID: 요청 고유 식별자 (전 서비스 전파)
    │
    ▼
Span: 각 서비스 내 작업 단위 (parent-child 관계)
    │
    ▼
Context Propagation: W3C Trace Context · B3 헤더
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 분산 추적 | Trace/Span ID가 추적의 기본 단위 |
| W3C Trace Context | 표준화된 HTTP 헤더 전파 규격 |
| OpenTelemetry | Trace/Span 생성 및 전파의 표준 SDK |
| 로그 연결 | MDC에 Trace ID 주입으로 로그-트레이스 연결 |
| 비동기 처리 | Context 전달이 끊기기 쉬운 위험 지점 |
| Jaeger / Zipkin | Trace/Span 데이터 저장·시각화 |

---
