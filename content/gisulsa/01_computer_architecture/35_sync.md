+++
weight = 35
title = "35. 멀티코어 동기화"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 멀티코어 동기화 & 메모리 모델

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

Test-and-Set: 읽기+쓰기 원자적 수행
Compare-and-Swap (CAS):
  CAS(addr, expected, new):

### Ⅱ. 핵심 구성요소

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


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
