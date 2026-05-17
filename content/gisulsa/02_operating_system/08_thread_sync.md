+++
weight = 8
title = "08. 멀티스레드 & 동기화"
date = "2026-05-17"
[extra]
categories = "gisulsa-os"
+++

# 🎯 멀티스레드 & 동기화 심화

> **별점**: ★★★★★ | 기본 필수

## 1. 스레드 모델

```
[사용자 수준 vs 커널 수준]
사용자 수준 스레드 (Green Thread):
  라이브러리 관리, 커널 미인식
  빠르지만 블로킹 시스템 콜 = 프로세스 전체 블록

커널 수준 스레드:
  커널이 직접 관리 (TCB)
  진정한 병렬 실행 가능
  컨텍스트 전환 비용 있음

[N:M 하이브리드 (Go 고루틴)]
M개 사용자 스레드 → N개 커널 스레드
적은 커널 스레드로 많은 작업 처리
Go: goroutine + GMP 스케줄러
```

## 2. 동기화 원시 (Primitives)

```
[뮤텍스 (Mutex)]
상호 배제: 임계 구역에 한 번에 하나만
소유 개념: 잠근 스레드만 해제 가능
우선순위 역전 문제 → 우선순위 상속으로 해결

[세마포어 (Semaphore)]
계수 세마포어: N개 자원 제어
이진 세마포어: 뮤텍스와 유사 (소유 없음)
wait(P)/signal(V) 연산

[모니터 (Monitor)]
Java synchronized / C# lock
상호 배제 + 조건 변수 통합
condition.wait() / condition.notify()

[Spinlock]
CAS (Compare-And-Swap) 기반 바쁜 대기
짧은 임계 구역에 효율적
멀티코어 환경에 적합
```

## 3. 락프리 & 비동기

```
[락프리 알고리즘]
CAS (Compare And Swap):
  원자적 읽기-비교-교환
  락 없이 공유 자원 접근

[비동기 프로그래밍]
콜백 → Promise → async/await
코루틴: 실행 일시 중단 가능한 함수
  Go goroutine, Python asyncio, Kotlin coroutine
이벤트 루프: Node.js, 단일 스레드 비동기
```

## 4. 답안 포인트

**3단락**: ① 사용자/커널 스레드 & Go 고루틴 → ② 뮤텍스/세마포어/모니터 동기화 → ③ 락프리 CAS & async/await 비동기

## 5. 관련 개념

`데드락(★04번)` → 동기화 실패 결과 | `캐시 일관성(01 14번)` → 메모리 배리어 + 원자적 연산 | `RTOS(01 56번)` → 실시간 뮤텍스/세마포어
