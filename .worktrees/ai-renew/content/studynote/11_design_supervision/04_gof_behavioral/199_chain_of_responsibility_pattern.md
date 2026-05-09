+++
weight = 199
title = "199. 책임 연쇄 패턴 (Chain of Responsibility Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 요청을 처리할 수 있는 핸들러(Handler)들이 사슬(Chain) 형태로 연결되어, 각 핸들러가 처리 가능 여부를 판단하고 처리하거나 다음 핸들러로 전달한다.
> 2. **가치**: 요청 발신자(Sender)와 수신자(Receiver)를 완전히 분리하여 결합도(Coupling)를 낮추고, 처리 규칙을 런타임(Runtime)에 동적으로 조립할 수 있다.
> 3. **판단 포인트**: "누가 처리할지 모르지만 순서대로 물어봐야 한다"는 구조가 필요할 때 적용한다.

---

## Ⅰ. 개요 및 필요성

### 1-1. 패턴 탄생 배경

기업 결재 라인을 생각해 보자. 10만 원 지출은 팀장이 승인하지만, 100만 원이면 부서장, 1,000만 원이면 임원이 필요하다. 이를 `if-else`로 구현하면:

```java
if (amount < 100_000) teamLeader.approve(amount);
else if (amount < 1_000_000) deptHead.approve(amount);
else executive.approve(amount);
```

결재 라인이 바뀌거나 새로운 단계가 추가될 때마다 이 코드를 수정해야 한다. Chain of Responsibility (책임 연쇄) 패턴은 각 결재자를 **독립 Handler 객체**로 만들고, 사슬로 연결하여 이 문제를 해결한다.

### 1-2. 현실 세계의 사례

| 사례 | 설명 |
|:---|:---|
| 결재 라인 | 팀장 → 부서장 → 임원 순서로 전달 |
| DOM Event Bubbling | 자식 요소 → 부모 → document → window |
| Java Servlet Filter Chain | Filter1 → Filter2 → Filter3 → Servlet |
| 로그 레벨 처리 | DEBUG → INFO → WARN → ERROR Handler |
| 고객 서비스 에스컬레이션 | 상담원 → 팀장 → 매니저 |

📢 **섹션 요약 비유**: 고객센터에 전화하면 상담원이 먼저 받고, 해결 못 하면 팀장, 팀장도 못 하면 매니저로 연결해 주는 것 — 그것이 책임 연쇄 패턴이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 구조 (UML 요약)

```
  Client
    │
    │ request
    ▼
┌─────────────┐   nextHandler   ┌─────────────┐   nextHandler   ┌─────────────┐
│  Handler    │────────────────►│  Handler    │────────────────►│  Handler    │
│  (Abstract) │                 │  (Abstract) │                 │  (Abstract) │
└──────┬──────┘                 └──────┬──────┘                 └──────┬──────┘
       │                               │                               │
       ▼                               ▼                               ▼
 ConcreteHandler A              ConcreteHandler B              ConcreteHandler C
 (처리 or 전달)                 (처리 or 전달)                 (처리 or 전달)
```

### 2-2. 결재 라인 예시 상세

```
  결재 요청 (amount)
        │
        ▼
  ┌─────────────────────────────────────────────────────────┐
  │ TeamLeaderHandler                                       │
  │  if (amount < 100,000) → 승인                          │
  │  else → deptHeadHandler.handle(amount)                  │
  └─────────────────────────────────────────────────────────┘
                              │
                              ▼ (amount ≥ 100,000)
  ┌─────────────────────────────────────────────────────────┐
  │ DeptHeadHandler                                         │
  │  if (amount < 1,000,000) → 승인                        │
  │  else → executiveHandler.handle(amount)                 │
  └─────────────────────────────────────────────────────────┘
                              │
                              ▼ (amount ≥ 1,000,000)
  ┌─────────────────────────────────────────────────────────┐
  │ ExecutiveHandler                                        │
  │  if (amount < 10,000,000) → 승인                       │
  │  else → 처리 불가 (null or throw)                       │
  └─────────────────────────────────────────────────────────┘
```

### 2-3. 핵심 코드 구조 (Java)

```java
abstract class Handler {
    protected Handler next;

    public void setNext(Handler next) { this.next = next; }

    public abstract void handle(int amount);

    protected void passToNext(int amount) {
        if (next != null) next.handle(amount);
        else System.out.println("처리 불가: " + amount);
    }
}

class TeamLeaderHandler extends Handler {
    @Override
    public void handle(int amount) {
        if (amount < 100_000) System.out.println("팀장 승인: " + amount);
        else passToNext(amount);
    }
}
```

📢 **섹션 요약 비유**: 택배 분류 컨베이어 벨트 — 각 구간에서 자기가 처리할 수 있는 택배만 가져가고, 나머지는 다음 구간으로 넘긴다.

---

## Ⅲ. 비교 및 연결

### 3-1. 관련 패턴 비교

| 패턴 | Chain of Responsibility | Command | Strategy |
|:---|:---|:---|:---|
| **요청 처리 주체** | 동적으로 결정 | 명령 객체가 결정 | 클라이언트가 결정 |
| **처리 여부** | 핸들러가 판단 | 항상 처리 | 항상 처리 |
| **다수 객체 관여** | ✅ (체인) | ❌ | ❌ |
| **순서 중요성** | ✅ | ❌ | ❌ |
| **미처리 가능성** | ✅ | ❌ | ❌ |

### 3-2. Servlet Filter Chain vs Chain of Responsibility

```
HTTP Request
     │
     ▼
┌──────────────────────────────────────────────────┐
│  AuthFilter.doFilter()                           │
│    → chain.doFilter() ──────────────────────────►│
│                          LogFilter.doFilter()     │
│                            → chain.doFilter() ──►│
│                                                  │
│                                CompressionFilter  │
│                                  → chain.doFilter│
│                                          │        │
│                                          ▼        │
│                                       Servlet     │
└──────────────────────────────────────────────────┘
```

Java Servlet의 `FilterChain.doFilter()`는 Chain of Responsibility 패턴의 완벽한 실제 구현이다.

📢 **섹션 요약 비유**: 공항 보안 검색대 — 여권 확인 → X-ray 검색 → 금속 탐지 → 탑승구. 각 단계가 독립적이고, 통과해야만 다음으로 넘어간다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 실무 패턴 조립 예시 (Builder로 체인 구성)

```java
Handler chain = new TeamLeaderHandler();
chain.setNext(new DeptHeadHandler())
     .setNext(new ExecutiveHandler());

// 런타임에 체인 재조립 가능
chain.handle(50_000);    // 팀장 처리
chain.handle(500_000);   // 부서장 처리
chain.handle(5_000_000); // 임원 처리
```

### 4-2. Node.js Express Middleware와의 관계

```javascript
// Express는 Chain of Responsibility 패턴의 실용적 구현
app.use(authMiddleware);    // Handler 1
app.use(logMiddleware);     // Handler 2
app.use(rateLimitMiddleware); // Handler 3
app.get('/api', handler);   // 최종 처리
```

`next()` 호출이 다음 핸들러로 요청을 전달하는 핵심 메커니즘이다.

### 4-3. 기술사 서술 포인트

- **OCP (Open-Closed Principle)**: 새로운 결재 단계 추가 시 기존 Handler 무수정
- **SRP (Single Responsibility Principle)**: 각 Handler는 자신의 처리 범위만 담당
- **동적 조립 가능**: 환경 설정(Configuration)에 따라 체인 구성 변경 가능

📢 **섹션 요약 비유**: 레스토랑 주방의 조리 라인 — 각 조리사는 자신 담당 작업만 하고 나머지는 다음 사람에게 넘긴다. 메뉴(요청)가 달라도 라인 자체를 바꿀 필요가 없다.

---

## Ⅴ. 기대효과 및 결론

### 5-1. 장점

| 장점 | 설명 |
|:---|:---|
| 결합도(Coupling) 감소 | 발신자가 최종 수신자를 알 필요 없음 |
| 유연한 체인 구성 | 런타임에 핸들러 삽입·제거·재배열 가능 |
| SRP 준수 | 각 핸들러는 단일 처리 책임 보유 |
| OCP 달성 | 새 핸들러 추가 시 기존 코드 수정 불필요 |

### 5-2. 단점 및 주의사항

| 단점 | 설명 | 개선 방법 |
|:---|:---|:---|
| 요청 유실 | 체인 끝까지 처리 못 하면 묵살 | 기본 핸들러(Fallback Handler) 필수 배치 |
| 디버깅 어려움 | 어느 핸들러가 처리했는지 추적 곤란 | MDC (Mapped Diagnostic Context) 로깅 |
| 성능 저하 | 긴 체인에서 모든 핸들러 순회 | 처리 가능성 높은 핸들러를 앞에 배치 |
| 순서 의존성 | 체인 순서가 결과에 영향 | 문서화·테스트로 명시적 관리 |

### 5-3. 결론

Chain of Responsibility (책임 연쇄)는 **규칙 기반 처리 파이프라인**을 구현하는 가장 우아한 방법이다. 특히 미들웨어(Middleware), 필터(Filter), 이벤트 전파(Event Propagation) 시스템에서 이미 광범위하게 사용된다.

📢 **섹션 요약 비유**: "다음 사람에게 물어봐" — 조직의 책임이 명확하게 분산되어 있고, 아무도 자신 권한 밖의 결정을 하지 않는 구조.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF Behavioral Pattern | 행동 패턴 그룹 |
| 하위 개념 | ConcreteHandler | 실제 처리 로직 구현체 |
| 연관 개념 | Servlet Filter Chain | Java EE의 실제 구현 |
| 연관 개념 | Express Middleware | Node.js의 실제 구현 |
| 연관 개념 | DOM Event Bubbling | 이벤트 전파의 CoR 응용 |
| 연관 개념 | SRP / OCP | 패턴이 달성하는 설계 원칙 |

### 👶 어린이를 위한 3줄 비유 설명

- 학교 건물 경비원이 있어요. 1층 경비원이 모르면 2층으로, 2층도 모르면 교장 선생님께 물어봐요.
- 각 경비원은 자기가 알 수 있는 것만 대답하고, 나머지는 윗사람에게 넘겨요.
- 책임 연쇄 패턴은 이렇게 "모르면 다음 사람에게 넘기는" 질문 사슬이에요!
