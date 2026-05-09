+++
weight = 200
title = "200. 책임 연쇄 패턴 장단점 (Chain of Responsibility Pros and Cons)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Chain of Responsibility (책임 연쇄)의 강점은 결합도 감소와 유연한 조립이지만, 요청 유실과 디버깅 어려움이라는 구조적 단점도 함께 가져온다.
> 2. **가치**: 단점을 알고 보완 패턴(Fallback Handler, 로깅, 처리 확인)을 함께 적용해야 프로덕션(Production) 품질의 구현이 된다.
> 3. **판단 포인트**: 체인 길이가 길어질수록 성능·추적성 비용이 증가하므로 처리 확률이 높은 핸들러를 앞에 배치하는 최적화가 필수다.

---

## Ⅰ. 개요 및 필요성

### 1-1. 왜 장단점을 별도로 다루는가

Chain of Responsibility (책임 연쇄)는 구조가 단순하고 직관적이어서 남용되기 쉽다. 잘못 설계된 체인은 다음과 같은 문제를 유발한다:

- 500만 원 결재 요청이 **묵살(silently dropped)**되어 처리됐는지 모름
- 10개의 필터를 거쳐야 하는 HTTP 요청의 **지연 증가**
- 어느 핸들러가 예외를 던졌는지 **추적 불가**

이 장에서는 장점을 구체적으로 수치화하고, 단점마다 실무 개선 방법을 제시한다.

### 1-2. 장점 전체 요약

```
  Chain of Responsibility 장점
  ┌────────────────────────────────────────────────────┐
  │  1. 결합도(Coupling) 감소                          │
  │     - Sender는 Receiver를 직접 참조하지 않음       │
  │                                                    │
  │  2. 단일 책임 원칙 (SRP) 준수                      │
  │     - 각 Handler = 하나의 처리 책임                │
  │                                                    │
  │  3. 개방-폐쇄 원칙 (OCP) 준수                      │
  │     - 새 Handler 추가 시 기존 코드 무수정           │
  │                                                    │
  │  4. 동적 체인 조립                                 │
  │     - 런타임에 핸들러 순서 변경·삽입·제거 가능     │
  └────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 책임 연쇄는 잘 쓰면 "전문가 팀 분업", 잘못 쓰면 "아무도 책임 안 지는 핑퐁 게임".

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 장점 상세: 결합도 감소

```
[ Before: 강결합 ]
  Client ──직접 참조──► TeamLeader
  Client ──직접 참조──► DeptHead
  Client ──직접 참조──► Executive
  (3개의 의존성, if-else 필요)

[ After: Chain of Responsibility ]
  Client ──참조──► Handler (추상)
                      │
                 체인이 내부적으로 전달
                 (1개의 의존성)
```

클라이언트는 체인의 **첫 번째 핸들러만 알면 된다**. 체인 구성이 바뀌어도 클라이언트 코드는 변경되지 않는다.

### 2-2. 단점 상세: 요청 유실 메커니즘

```
  Request(amount=5억)
        │
        ▼
  TeamLeader → 전달
        │
        ▼
  DeptHead → 전달
        │
        ▼
  Executive → 전달
        │
        ▼
  ┌─────────────────────────┐
  │  next == null           │
  │  → 아무 처리 없이 종료  │ ← 요청 유실!
  └─────────────────────────┘
```

**개선 방법**: 체인 끝에 **Fallback Handler (폴백 핸들러)**를 반드시 배치한다:

```java
class FallbackHandler extends Handler {
    @Override
    public void handle(int amount) {
        // 로그 기록, 예외 발생, 알림 발송 등
        log.error("처리되지 않은 요청: {}", amount);
        throw new UnhandledRequestException(amount);
    }
}
```

### 2-3. 단점 상세: 디버깅 어려움

```
  Request → H1 → H2 → H3 → H4 → 처리됨
  
  Question: 어느 핸들러가 처리했나?
  Answer:   로그 없으면 알 수 없음!
```

**개선 방법**: 각 핸들러에 MDC (Mapped Diagnostic Context) 기반 구조 로깅 추가:

```java
public void handle(Request req) {
    MDC.put("handler", this.getClass().getSimpleName());
    log.debug("Handler {} 처리 시도: {}", MDC.get("handler"), req);
    
    if (canHandle(req)) {
        log.info("Handler {} 처리 완료", MDC.get("handler"));
        doHandle(req);
    } else {
        passToNext(req);
    }
}
```

📢 **섹션 요약 비유**: 요청 유실은 "아무도 집 열쇠를 책임지지 않아서 잃어버린 것", 디버깅 어려움은 "어느 택배기사가 배달했는지 영수증이 없는 것".

---

## Ⅲ. 비교 및 연결

### 3-1. 장단점 전체 비교표

| 항목 | 장점 | 단점 | 개선 방법 |
|:---|:---|:---|:---|
| **결합도** | Sender-Receiver 분리 | 체인 전체 흐름 파악 어려움 | 체인 구성 문서화 |
| **확장성** | Handler 추가·제거 용이 | 체인 순서 오류 시 버그 | 통합 테스트 필수 |
| **책임 분리** | SRP 달성 | 책임 분산으로 흐름 파악 어려움 | 시퀀스 다이어그램 작성 |
| **요청 처리** | 동적 라우팅 가능 | 요청 유실 가능성 | Fallback Handler |
| **디버깅** | 각 Handler 독립 테스트 | 전체 흐름 추적 어려움 | MDC 로깅 |
| **성능** | 조건 분기 제거 | 긴 체인 = O(n) 순회 | 우선순위 정렬 |

### 3-2. 다른 패턴과 조합하여 단점 보완

| 조합 패턴 | 보완 효과 |
|:---|:---|
| **Decorator (데코레이터)** | 처리 전후 횡단 관심사(로깅, 타이밍) 추가 |
| **Observer (옵저버)** | 처리 이벤트를 구독자에게 알림 → 추적성 확보 |
| **Command (커맨드)** | 요청을 객체화하여 로그·재시도 가능 |
| **Composite (컴포지트)** | 핸들러 그룹을 단일 핸들러처럼 취급 |

📢 **섹션 요약 비유**: 칼은 편리하지만 잘못 쓰면 다친다. Chain of Responsibility도 Fallback + 로깅 + 테스트라는 안전 장치와 함께 써야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 성능 최적화: 핸들러 우선순위 정렬

```
  Before (비최적화):
  RareHandler(5%) → CommonHandler(80%) → VeryCommonHandler(15%)
  → 평균 1.9번 순회

  After (최적화):
  CommonHandler(80%) → VeryCommonHandler(15%) → RareHandler(5%)
  → 평균 1.25번 순회
  (34% 성능 향상)
```

처리 확률이 높은 핸들러를 체인 앞쪽에 배치한다.

### 4-2. 실무 체크리스트

```
  체인 설계 시 반드시 확인할 것
  ┌──────────────────────────────────────────────┐
  │  □ Fallback Handler가 체인 끝에 있는가?      │
  │  □ 각 Handler에 처리 여부 로그가 있는가?     │
  │  □ 처리 확률 기준으로 핸들러가 정렬되었나?  │
  │  □ 체인 무한 루프 방지 로직이 있는가?        │
  │  □ 단위 테스트: 각 Handler 독립 테스트 완료? │
  │  □ 통합 테스트: 전체 체인 흐름 테스트 완료? │
  └──────────────────────────────────────────────┘
```

### 4-3. 기술사 서술 포인트

- CoR (Chain of Responsibility)의 구조적 단점을 **인지하고 보완 패턴과 함께 제시**하는 것이 고수준 답안
- "단점: 요청 유실 가능 → 개선: Fallback Handler + 예외 발생 처리" 쌍으로 서술
- 실제 Java Servlet Filter Chain, Spring Security Filter Chain이 CoR의 산업 표준 적용 사례임을 명시

📢 **섹션 요약 비유**: 좋은 의사는 약의 부작용도 안다. 좋은 개발자는 패턴의 단점과 보완법을 함께 안다.

---

## Ⅴ. 기대효과 및 결론

### 5-1. 잘 설계된 Chain의 효과

- 새로운 처리 규칙 추가 시 **기존 운영 코드 무수정** → 배포 위험 최소화
- 핸들러별 독립 단위 테스트 → **테스트 커버리지 향상**
- 처리 이력 로그 확보 → **운영 장애 시 빠른 원인 분석**

### 5-2. 안티패턴 (Anti-Pattern) 경계

```
  ❌ 잘못된 사용:
  - 체인이 100개 이상의 핸들러로 구성 (성능 문제)
  - Fallback Handler 없이 배포 (요청 유실)
  - 핸들러가 자신 다음의 핸들러를 직접 생성 (강결합 재발)

  ✅ 올바른 사용:
  - 의미 있는 처리 단위별로 핸들러 분리 (최대 5~10개 권장)
  - 체인 구성은 외부(Factory, Configuration)에서 조립
  - 각 핸들러는 다음 핸들러의 존재를 모르는 것이 이상적
```

### 5-3. 결론

Chain of Responsibility (책임 연쇄)는 **처리 규칙의 유연성**과 **발신자-수신자 분리**라는 명확한 가치를 제공한다. 그러나 요청 유실, 디버깅 어려움, 성능 저하라는 단점을 함께 인식하고, Fallback Handler와 구조적 로깅으로 보완할 때 비로소 프로덕션 품질의 구현이 완성된다.

📢 **섹션 요약 비유**: 멋진 릴레이 경주팀은 빠를 뿐 아니라, 바통을 떨어뜨렸을 때의 대응 훈련도 한다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Chain of Responsibility Pattern | 본 패턴 |
| 연관 개념 | SRP (Single Responsibility Principle) | 각 Handler의 단일 책임 |
| 연관 개념 | OCP (Open-Closed Principle) | 새 Handler 추가 시 기존 코드 보호 |
| 연관 개념 | Fallback Handler | 요청 유실 방지 보완 패턴 |
| 연관 개념 | MDC (Mapped Diagnostic Context) | 분산 추적 로깅 기법 |
| 연관 개념 | Spring Security Filter Chain | 실제 산업 적용 사례 |

### 👶 어린이를 위한 3줄 비유 설명

- 책임 연쇄는 릴레이 경주처럼 바통을 다음 주자에게 넘기는 거예요.
- 근데 마지막 주자가 결승선을 무시하고 가버리면 바통을 잃어버리겠죠?
- 그래서 항상 "마지막 선수"(Fallback Handler)를 미리 정해두는 것이 중요해요!
