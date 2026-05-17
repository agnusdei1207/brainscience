+++
weight = 35
title = "35. 멀티코어 동기화"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 멀티코어 동기화 & 메모리 모델

> **별점**: ★★★★★ | 기본 필수

## 1. 하드웨어 동기화 지원

```
[원자적 연산 (Atomic Operations)]
HW가 분할 불가능하게 실행 보장

Test-and-Set: 읽기+쓰기 원자적 수행
Compare-and-Swap (CAS):
  CAS(addr, expected, new):
    if (*addr == expected): *addr = new, return true
    else: return false
  → 락프리 알고리즘의 기반

Fetch-and-Add: 원자적 증가
LL/SC (Load-Link/Store-Conditional): ARM 방식

[x86 명령어]
LOCK CMPXCHG: CAS 구현
XCHG: Test-and-Set 구현
```

## 2. 메모리 일관성 모델

```
[메모리 순서 보장 레벨]
Relaxed: 재정렬 마음대로 (성능 최대)
Release-Acquire: Acquire 이후/Release 이전만 보장
Sequential Consistency: 모든 순서 보장 (느림)

[실제 HW 메모리 모델]
x86: TSO (Total Store Order) = 거의 순차 일관성
ARM/RISC-V: 약한 모델, 재정렬 많음 → 배리어 필요

[프로그래밍 언어 원자 연산]
C++ std::atomic<int> x{0};
  x.fetch_add(1, std::memory_order_relaxed)
Java AtomicInteger: incrementAndGet()
Go sync/atomic: AddInt64()
```

## 3. 락 구현 & 성능

```
[Spinlock]
CAS 기반 바쁜 대기 (busy-wait)
적합: 짧은 임계 구역, 멀티코어
부적합: 단일 코어 (CPU 낭비), 긴 대기

[MCS Lock (Mellor-Crummey & Scott)]
공정한 스핀락, 지역 변수 스핀
NUMA 환경에서 캐시 효율적

[Ticket Lock]
선착순 보장 (공정성)
인터넷 번호표 방식

[적응형 락]
짧게 스핀 후 블록 전환
Linux futex (Fast Userspace Mutex)
```

## 4. 답안 포인트

**3단락**: ① CAS 원자 연산 & 락프리 기반 → ② 메모리 일관성 모델(TSO/Relaxed) & 배리어 → ③ Spinlock/MCS/Ticket 락 비교

## 5. 관련 개념

`캐시 일관성(14번)` → HW MESI + SW 동기화 | `OS 동기화(02_os)` → 커널 뮤텍스 구현 | `데드락(04번)` → 락 획득 실패 시
