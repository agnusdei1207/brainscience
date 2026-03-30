+++
weight = 142
title = "이벤트 루프 기반 비동기 처리"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

# 이벤트 루프 기반 비동기 처리 (Event Loop Based Asynchronous Processing)

## Ⅰ. 이벤트 루프 개념

### 1. 정의 및 특징

이벤트 루프(Event Loop)는 단일 스레드에서 이벤트 큐를 순회하며 콜백 함수를 디스패치하는 비동기 처리 아키텍처다. 멀티스레딩 없이 동시성을 달성하는 핵심 메커니즘이다.

> **비유:** 식당 주방장이 혼자서 주문서를 하나씩 확인하고, 조리가 오래 걸리는 음식은 오븐에 맡겨놓고 다음 주문을 처리하는 방식과 같다.

```
┌─────────────────────────────────────────────────┐
│                 Event Loop                       │
│                                                   │
│   ┌─────────┐    ┌──────────┐    ┌──────────┐   │
│   │  Event   │───>│ Dispatch  │───>│ Callback │   │
│   │  Queue   │    │  & Exec  │    │ Complete │   │
│   └─────────┘    └──────────┘    └──────────┘   │
│        ^                               │          │
│        └───────────────────────────────┘          │
└─────────────────────────────────────────────────┘
```

```
┌─────────────────── Single Thread Timeline ───────────────────┐
│                                                              │
│  [A]──request──>[B]──request──>[A]──callback──>[C]──...     │
│   non-blocking   non-blocking   result                       │
│                                                              │
│  Legend: [A],[B],[C] = async operations                      │
└──────────────────────────────────────────────────────────────┘
```

## Ⅱ. 동작 원리

### 1. 논블로킹 I/O (Non-blocking I/O)

I/O 연산이 완료될 때까지 스레드를 차단하지 않고 즉시 반환하며, 작업 완료 시 콜백을 큐에 등록한다.

### 2. 이벤트 루프의 5단계 (Node.js 기준)

| 단계 | 이름 | 설명 |
|------|------|------|
| 1 | **Timers** | `setTimeout`, `setInterval` 만료된 콜백 실행 |
| 2 | **Pending Callbacks** | 이전 루프에서 지연된 I/O 콜백 실행 |
| 3 | **Poll** | 새로운 I/O 이벤트 수집 및 실행 |
| 4 | **Check** | `setImmediate` 콜백 실행 |
| 5 | **Close** | `close` 이벤트 콜백 실행 |

```
┌──────────────────────────────────────────────────────────┐
│                   Event Loop Phases                      │
│                                                          │
│   ┌────────┐  ┌────────┐  ┌──────┐  ┌───────┐  ┌─────┐│
│   │ Timers │─>│Pending │─>│ Poll │─>│ Check │─>│Close││
│   └────────┘  │Callback│  └──────┘  └───────┘  └─────┘│
│      ^        └────────┘     │                         │
│      └───────────────────────┘  (다시 반복)              │
│                                                          │
│   [Microtask Queue: Promise.then, process.nextTick]     │
│   > 각 페이즈 사이마다 우선 실행                          │
└──────────────────────────────────────────────────────────┘
```

### 3. 구현체별 특징

| 플랫폼 | 엔진 | 특징 |
|--------|------|------|
| **Node.js** | libuv | C++ 기반, 파일 I/O + 네트워크 모두 비동기 |
| **Browser JS** | V8/SpiderMonkey | Web API 사용, UI 렌더링과 병행 |
| **Python asyncio** | async/await | 코루틴 기반, `asyncio.run()` 진입점 |
| **Go** | goroutine | M:N 스케줄링, runtime에 이벤트 루프 내장 |

> **비유:** 이벤트 루프의 페이즈는 우체부가 아침에 배달(Timers), 미처 못한 편지(Pending), 새 편지 수거(Poll), 등기 확인(Check), 마감(Close) 순으로 돌리는 일과와 같다.

## Ⅲ. 비동기 처리 흐름

### 1. 콜백 기반 vs 프로미스 기반

```
┌────────────────── Callback Style ──────────────────┐
│                                                     │
│  readFile("data.txt", function(err, data) {        │
│      if (err) throw err;    // 콜백 지옥 가능       │
│      console.log(data);                             │
│  });                                                │
│                                                     │
└─────────────────────────────────────────────────────┘

┌────────────────── Promise Style ───────────────────┐
│                                                     │
│  readFile("data.txt")                               │
│      .then(data => console.log(data))               │
│      .catch(err => console.error(err));             │
│                                                     │
│  // async/await 변환                                 │
│  const data = await readFile("data.txt");           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 2. 마이크로태스크와 매크로태스크

| 구분 | 예시 | 실행 시점 |
|------|------|-----------|
| **Microtask** | `Promise.then`, `queueMicrotask` | 현재 페이즈 종료 직후, 다음 페이즈 이전 |
| **Macrotask** | `setTimeout`, `setImmediate` | 다음 이벤트 루프 틱(tick) |

## Ⅳ. 장단점 및 한계

### 1. 장점

- 스레드 생성/컨텍스트 스위칭 오버헤드 없음
- 메모리 사용량 적음 (단일 스레드)
- 수만 개의 동시 연결 처리 가능 (C10K 문제 해결)
- 동기 코드와 비슷한 제어 흐름으로 작성 가능

### 2. 한계: CPU 연산 집약적 작업

```
┌──────── CPU-Bound Blocking ────────┐
│                                     │
│  [Event Loop]──[Task A]────────────>│ BLOCKED!
│                   │                 │ (다른 이벤트 전부 지연)
│                   │  CPU 100%      │
│                   │  10초 소요     │
│                   ▼                 │
│              [완료]                  │
│  [Task B, C, D... 지연됨]          │
│                                     │
└─────────────────────────────────────┘
```

해결책: **Worker Thread** 분리, **클러스터 모드** (멀티프로세스), **C++ Addon** 오프로딩

## Ⅴ. 지식 그래프

```
이벤트 루프 기반 비동기 처리
├── 핵심 개념
│   ├── 단일 스레드 이벤트 구동 아키텍처
│   ├── 논블로킹 I/O
│   └── 콜백 큐 순회 및 디스패치
├── 이벤트 루프 페이즈
│   ├── Timers (setTimeout/setInterval)
│   ├── Pending Callbacks (지연된 I/O)
│   ├── Poll (새 이벤트 수집)
│   ├── Check (setImmediate)
│   └── Close (닫기 콜백)
├── 구현체
│   ├── libuv (Node.js)
│   ├── Browser Web API
│   ├── Python asyncio
│   └── Go runtime scheduler
├── 비동기 패턴
│   ├── Callback (콜백 지옥)
│   ├── Promise (then/catch/finally)
│   └── Async/Await (코루틴)
├── 장점
│   ├── 스레드 오버헤드 제거
│   ├── 적은 메모리 사용
│   └── C10K 문제 해결
└── 한계 및 해결책
    ├── CPU-bound 작업 시 블로킹
    ├── Worker Thread 분리
    └── 클러스터 (멀티프로세스)
```

---

## 약어 정리

| 약어 | Full Name |
|------|-----------|
| **libuv** | Library for UV (Unified Virtualization) |
| **I/O** | Input/Output |
| **API** | Application Programming Interface |
| **C10K** | Client 10,000 Problem |

---

## 3줄 어린이 설명

컴퓨터가 한 사람처럼 일할 때, 기다리지 않고 여러 일을 번갈아 하는 방법입니다.
주문이 들어오면 오븐에 넣고 다른 주문을 받는 식당 주방장과 같아요.
단, 계산이 아주 많이 필요한 일은 다른 도우미에게 맡겨야 합니다.
