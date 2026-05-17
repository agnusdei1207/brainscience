+++
weight = 3
title = "03. 명령어 집합 CISC vs RISC"
date = "2026-05-18"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 명령어 집합 구조 (ISA), CISC vs RISC

> 출제 빈도: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

명령어 집합 구조(ISA, Instruction Set Architecture)란 소프트웨어가 하드웨어에 접근하기 위한 인터페이스 규약으로, 명령어 형식·주소 지정 방식·레지스터 구조·데이터 타입을 정의한다. ISA 설계 철학에 따라 CISC(Complex Instruction Set Computer)와 RISC(Reduced Instruction Set Computer)로 대별된다.

### Ⅱ. CISC vs RISC 비교

| 구분 | CISC | RISC |
|------|------|------|
| 철학 | 복잡한 명령 하나로 여러 동작 | 단순 명령을 빠르게 반복 |
| 명령어 길이 | 가변 (1~15byte) | 고정 (4byte) |
| 클럭/명령 | 다수 클럭 | 단일 클럭 목표 |
| 레지스터 | 소수 범용 | 다수 범용 (32~64개) |
| 파이프라인 | 비정형 → 복잡 | 정형 → 고효율 |
| 대표 | x86(Intel/AMD) | ARM, RISC-V, MIPS |

### Ⅲ. 주소 지정 방식

```
즉시(Immediate):  ADD R1, #5       ← 오퍼랜드가 명령어에 포함
직접(Direct):     LOAD R1, [1000]  ← 메모리 주소 직접 지정
간접(Indirect):   LOAD R1, @R2     ← 레지스터가 가리키는 주소
인덱스(Indexed):  LOAD R1, 100(R2) ← 베이스+오프셋
레지스터(Register): ADD R1, R2     ← 레지스터 간 연산
```

### Ⅳ. RISC-V와 최신 동향

RISC-V는 오픈소스 ISA로 라이선스 비용 없이 커스텀 프로세서 설계가 가능하다. 모듈식 확장(M:정수곱셈, F/D:부동소수점, V:벡터)을 통해 IoT부터 서버까지 스케일링이 가능하며, 중국·EU의 반도체 주권 전략에서 핵심 역할을 한다. ARM은 빅.LITTLE 이종 코어 구조로 모바일·서버(AWS Graviton) 시장을 지배하고 있다.

### Ⅴ. 답안 포인트

기술사 답안에서는 ① CISC/RISC 비교표 ② 파이프라인 효율성과의 연관 ③ RISC-V 오픈소스 ISA의 산업적 의미를 반드시 서술한다.

---

**관련**: 파이프라인(01번) · 슈퍼스칼라(10번) · 병렬/멀티코어(05번)
