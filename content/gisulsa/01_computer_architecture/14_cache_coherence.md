+++
weight = 14
title = "14. 캐시 일관성 (MESI)"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 캐시 일관성 — MESI 프로토콜

> **별점**: ★★★★★ | 기본 필수

## 1. 캐시 일관성 문제

```
멀티코어 환경:
  코어0 L1캐시 ─ 코어1 L1캐시 ─ 코어2 L1캐시
         ↓               ↓               ↓
              공유 LLC (Last Level Cache)

문제: 코어0이 X=1을 캐시에 쓰면
     코어1의 캐시에는 여전히 X=0
     → 일관성 위반!
```

## 2. MESI 프로토콜

```
각 캐시 라인이 4가지 상태 중 하나:

M (Modified):
  이 캐시만 최신 데이터 보유
  메모리 값과 다름 (dirty)
  → 교체 시 메모리에 쓰기 (Write-Back) 필요

E (Exclusive):
  이 캐시만 보유 (유일), 메모리와 동일 (clean)
  읽기 전용 상태

S (Shared):
  여러 캐시가 동시 보유 가능
  메모리와 동일 (clean)
  쓰기 시 다른 캐시에 무효화 메시지

I (Invalid):
  유효하지 않은 데이터
  캐시 미스 → 메모리/다른 캐시에서 가져옴

[상태 전이]
읽기:  I→S 또는 I→E (유일 보유 시)
쓰기:  I/S→M (다른 캐시에 Invalidate 신호)
스누핑: 다른 코어의 버스 트랜잭션 감시
```

## 3. MOESI 확장

```
O (Owned): S의 확장
  여러 캐시 공유 BUT 이 캐시가 메모리 업데이트 책임
  Write-Back 부담 분산

Directory 프로토콜:
  스누핑 방식은 버스 브로드캐스트 → 스케일 한계
  Directory: 각 라인의 공유 상태를 중앙에 기록
  → NUMA 멀티소켓 대규모 시스템
```

## 4. 메모리 배리어 (Fence)

```
컴파일러/CPU 명령어 재정렬 → 일관성 문제
메모리 배리어: 순서 보장 명령어

x86: MFENCE, SFENCE, LFENCE
ARM: DMB, DSB, ISB

Java volatile: 자동 메모리 배리어 삽입
C++ std::atomic: 원자적 연산 + 배리어
```

## 5. 답안 포인트

**3단락**: ① 멀티코어 캐시 일관성 문제 → ② MESI 4가지 상태 & 전이 → ③ 메모리 배리어 & Java/C++ 적용

## 6. 관련 개념

`멀티코어 동기화(35번)` → MESI + 뮤텍스/세마포어 | `NUMA(SMP)` → Directory 프로토콜 확장 | `스레드 프로그래밍` → volatile/atomic 필수
