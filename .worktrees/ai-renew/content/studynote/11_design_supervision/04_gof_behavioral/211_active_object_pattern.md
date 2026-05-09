+++
weight = 211
title = "211. 액티브 오브젝트 패턴 (Active Object Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Active Object (액티브 오브젝트) 패턴은 메서드 호출(호출 스레드)과 메서드 실행(실행 스레드)을 분리하여, 비동기 호출자가 즉시 Future를 받고 실제 실행은 별도 스케줄러 스레드에서 처리되도록 한다.
> 2. **가치**: 호출자와 실행자 사이의 완전한 분리로 높은 응답성(Responsiveness)을 달성하며, 요청 큐(ActivationQueue)로 실행 순서를 제어한다.
> 3. **판단 포인트**: Java의 `CompletableFuture`, `ExecutorService.submit()` 모두 Active Object 패턴의 현대적 구현이다.

---

## Ⅰ. 개요 및 필요성

### 1-1. 동기 호출의 문제

```
  동기 호출:
  Client → method() → [실행, 대기, 대기, 대기...] → 결과 반환
                       (Client는 실행이 완료될 때까지 블록됨)

  예: HTTP 요청 처리 중 DB 조회 10초 → UI 10초 동안 멈춤
```

### 1-2. Active Object의 해결

```
  Active Object 호출:
  Client → method() → Future 즉시 반환
                          │
                          ▼ (별도 스레드에서 비동기 실행)
                       Scheduler → 실행 완료 → Future에 결과 저장
  Client는 나중에 future.get() 또는 콜백으로 결과 수신
```

### 1-3. 6요소 구조

| 요소 | 역할 |
|:---|:---|
| **Proxy** | 클라이언트가 보는 인터페이스, 호출을 MethodRequest로 변환 |
| **MethodRequest** | 메서드 호출 정보(메서드명, 인자)를 캡슐화한 객체 |
| **ActivationQueue** | MethodRequest를 순서대로 보관하는 큐 |
| **Scheduler** | ActivationQueue에서 꺼내 적절한 시점에 Servant에게 전달 |
| **Servant** | 실제 메서드를 실행하는 객체 |
| **Future** | 비동기 실행 결과를 나중에 받을 수 있는 핸들 |

📢 **섹션 요약 비유**: 식당 주문 시스템 — 손님(Client)이 주문서(MethodRequest)를 제출하고 주문 번호표(Future)를 받는다. 주방(Servant)은 주문 큐(ActivationQueue) 순서대로 조리한다. 손님은 음식을 기다리지 않고 앉아서 다른 일을 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 전체 구조 흐름

```
  Client Thread                    Active Object Thread
  ─────────────                    ─────────────────────
       │                                    │
       │ proxy.doWork(args)                 │
       ▼                                    │
  ┌─────────────┐                           │
  │   Proxy     │  enqueue(MethodRequest)   │
  │  (대리자)   │──────────────────────────►│
  └──────┬──────┘                     ┌────┴──────────────┐
         │                            │  ActivationQueue  │
         │ Future 즉시 반환            │  [Req1, Req2, ...] │
         ▼                            └────┬──────────────┘
  ┌──────────────┐                         │ dequeue()
  │  Future<T>   │                    ┌────▼──────────────┐
  │  (결과 수신  │                    │    Scheduler      │
  │   핸들)      │                    │  (실행 타이밍     │
  └──────┬───────┘                    │   제어)           │
         │                            └────┬──────────────┘
         │ future.get() [나중에]           │ execute()
         │                            ┌────▼──────────────┐
         └◄───────────────────────────│    Servant        │
            result                   │  (실제 실행)       │
                                      └───────────────────┘
```

### 2-2. Java CompletableFuture와 비교

```java
// Active Object 패턴 직접 구현 (단순화)
class ActiveWorker {
    private final BlockingQueue<Runnable> queue = new LinkedBlockingQueue<>();
    private final Thread schedulerThread;

    public ActiveWorker() {
        schedulerThread = new Thread(() -> {
            while (!Thread.interrupted()) {
                try {
                    Runnable task = queue.take();  // ActivationQueue에서 꺼냄
                    task.run();                     // Servant 실행
                } catch (InterruptedException e) { break; }
            }
        });
        schedulerThread.start();
    }

    public Future<String> processAsync(String input) {
        CompletableFuture<String> future = new CompletableFuture<>();
        queue.offer(() -> {
            String result = expensiveOperation(input);  // Servant
            future.complete(result);
        });
        return future;  // 즉시 반환
    }
}

// 사용 (Java의 현대적 구현)
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> expensiveOperation(input));  // Active Object 내장

String result = future
    .thenApply(s -> transform(s))
    .get();  // 필요할 때 결과 수신
```

### 2-3. Scheduler의 역할: 우선순위 제어

```
  ActivationQueue with Priority:

  High Priority:  [AuthRequest]
  Normal Priority: [DataRequest1, DataRequest2]
  Low Priority:   [LogRequest]

  Scheduler가 Priority Queue를 사용하면
  중요한 요청(Auth)을 먼저 처리 가능

  Java: PriorityBlockingQueue 활용
```

📢 **섹션 요약 비유**: 택배 회사의 드라이브 스루 — 고객(Client)은 창구(Proxy)에 택배를 맡기고 영수증(Future)만 받아 떠난다. 배달기사(Servant)는 창고(ActivationQueue)에서 순서대로 꺼내 배달한다.

---

## Ⅲ. 비교 및 연결

### 3-1. 비동기 패턴 비교

| 패턴 | 호출 방식 | 결과 수신 | 스레드 제어 |
|:---|:---|:---|:---|
| **Active Object** | 비동기 + Future | 폴링 or 콜백 | Scheduler가 제어 |
| **CompletableFuture** | 비동기 체인 | thenApply/get | ForkJoinPool |
| **Reactor** | 이벤트 기반 | 핸들러 콜백 | Event Loop |
| **async/await** | 문법 기반 비동기 | await 키워드 | 런타임 제어 |
| **Thread Pool** | Runnable 제출 | Future.get() | Thread Pool |

### 3-2. 연관 패턴

| 패턴 | 관계 |
|:---|:---|
| Command (커맨드) | MethodRequest가 Command 패턴으로 구현 |
| Proxy (프록시) | Active Object의 Proxy가 실제 객체처럼 보임 |
| Strategy (전략) | Scheduler의 스케줄링 전략 교체 가능 |
| Observer (옵저버) | Future 완료 시 Observer에게 알림 |

📢 **섹션 요약 비유**: Active Object는 "뛰어난 비서" — 상사(Scheduler)에게 할 일 목록(ActivationQueue)을 전달하고, 상사는 우선순위에 따라 실무자(Servant)에게 지시한다. 지시를 내린 사람(Client)은 결과를 기다리지 않고 다른 일을 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. Android UI Thread 패턴 (Active Object 응용)

```
  Android 아키텍처:
  UI Thread (Main Thread)          Worker Thread
       │                                │
       │ viewModel.loadData()           │
       │ → 즉시 반환 (LiveData Future)  │
       │                                │
       │ [다른 UI 업데이트 계속]        │ 데이터 로딩 중...
       │                                │
       │◄──────────────────────────────│ liveData.postValue(result)
       │ UI 자동 업데이트 (Observer)    │
```

### 4-2. Spring @Async 어노테이션

```java
// Spring의 @Async = Active Object 패턴의 선언적 구현
@Service
public class ReportService {
    @Async  // 별도 스레드에서 비동기 실행
    public CompletableFuture<Report> generateReport(Long id) {
        // 무거운 처리 (Servant 역할)
        Report report = buildReport(id);
        return CompletableFuture.completedFuture(report);
    }
}

// 호출자
CompletableFuture<Report> future = reportService.generateReport(123L);
// 호출 즉시 반환 → 다른 작업 처리 가능
```

### 4-3. 기술사 서술 포인트

- Active Object의 **6요소**: Proxy, MethodRequest, ActivationQueue, Scheduler, Servant, Future
- 호출 스레드와 실행 스레드의 **완전한 분리** 강조
- Java `CompletableFuture`, Spring `@Async`가 패턴의 실용적 구현임 언급

📢 **섹션 요약 비유**: Active Object는 "비동기 은행 업무 시스템" — 창구 직원(Proxy)이 신청서(MethodRequest)를 받아 대기열(ActivationQueue)에 넣고, 처리 번호표(Future)를 준다. 처리 직원(Servant)이 순서대로 처리하고 알림 문자(결과)를 보낸다.

---

## Ⅴ. 기대효과 및 결론

### 5-1. 기대 효과

| 효과 | 설명 |
|:---|:---|
| 응답성 향상 | 호출자가 즉시 반환 → UI 블록 없음 |
| 처리량 증가 | 요청과 처리를 분리 → 병렬 처리 가능 |
| 실행 순서 제어 | ActivationQueue로 우선순위 관리 |
| 부하 분산 | Scheduler가 적절한 시점에 실행 조율 |

### 5-2. 한계 및 주의사항

- **복잡성 증가**: 6요소 구현으로 코드 복잡도 상승 (실무에서는 CompletableFuture 활용 권장)
- **디버깅 어려움**: 비동기 스택 트레이스 추적이 어려움
- **메모리**: ActivationQueue 과부하 시 OOM (Out of Memory) 위험 → 큐 크기 제한 필요

### 5-3. 결론

Active Object (액티브 오브젝트) 패턴은 비동기 처리의 이론적 기반이다. Java의 `ExecutorService`, `CompletableFuture`, Spring의 `@Async` 모두 이 패턴의 현대적 구현이다. 6요소의 역할을 이해하면 비동기 시스템의 설계와 디버깅 능력이 크게 향상된다.

📢 **섹션 요약 비유**: Active Object는 "현대 전자정부 민원 시스템" — 민원 접수(Proxy), 접수증(Future), 처리 대기열(ActivationQueue), 담당 공무원 배정(Scheduler), 실제 처리(Servant), 결과 통지(Future 완료).

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 동시성 패턴 (Concurrency Pattern) | 병렬 처리 설계 패턴 그룹 |
| 하위 개념 | 6요소 (Proxy/MethodRequest/Queue/Scheduler/Servant/Future) | 패턴 구성 요소 |
| 연관 개념 | CompletableFuture | Java의 Active Object 현대 구현 |
| 연관 개념 | Command Pattern | MethodRequest의 구현 방식 |
| 연관 개념 | Spring @Async | 선언적 Active Object |
| 연관 개념 | Reactor Pattern | 이벤트 기반 비동기의 대안 |

### 👶 어린이를 위한 3줄 비유 설명

- 레스토랑에서 주문하면 번호표(Future)를 주고, 음식이 준비되면 불러줘요.
- 손님(Client)은 번호표 받고 자리에서 대화를 나눌 수 있어요 — 기다리는 동안 멈추지 않아요!
- 주방(Servant)은 주문 목록(ActivationQueue)에서 순서대로 요리해요.
