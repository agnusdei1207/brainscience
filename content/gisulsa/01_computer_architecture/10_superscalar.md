+++
weight = 10
title = "10. 슈퍼스칼라·비순차 실행"
date = "2026-05-18"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 슈퍼스칼라, 비순차 실행 (OoO)

> 출제 빈도: ★★★★☆ | 기본

---

## 답안.

### Ⅰ. 개요

슈퍼스칼라(Superscalar)란 한 클럭 사이클에 다수의 명령어를 동시에 발행(Issue)하여 IPC(Instructions Per Cycle)를 1 이상으로 높이는 프로세서 구조이다. 비순차 실행(Out-of-Order Execution, OoO)은 명령어 간 의존성이 없는 경우 프로그램 순서와 무관하게 실행하여 파이프라인 공백(Bubble)을 최소화하는 기법이다.

### Ⅱ. 슈퍼스칼라 구조

```
Fetch → Decode → Rename → Issue → Execute → Commit
  (다중)  (다중)   (RAT)   (RS)    (FU)     (ROB)

RAT: Register Alias Table (레지스터 재명명)
RS : Reservation Station (실행 대기)
FU : Functional Unit (ALU, FPU, Load/Store)
ROB: Reorder Buffer (순서 복원)
```

슈퍼스칼라 프로세서는 클럭당 4~8개 명령어를 디코드하고, 실행 유닛(ALU, FPU, 분기, 로드/스토어)에 분배한다. 비순차 실행을 위해 레지스터 재명명(Register Renaming)으로 WAW/WAR 해저드를 제거하고, ROB(Reorder Buffer)로 커밋 순서를 보장한다.

### Ⅲ. 투기적 실행

분기 예측기(Branch Predictor)를 통해 분기 결과를 미리 예측하고 해당 경로를 미리 실행한다. 예측이 맞으면 결과를 커밋하고, 틀리면 롤백(Flush)한다. 현대 CPU는 TAGE(Tagged Geometric) 등 정교한 예측기로 97%+ 적중률을 달성한다. Spectre/Meltdown은 이 투기적 실행의 부채널 취약점이다.

### Ⅳ. 성능 한계

ILP(Instruction-Level Parallelism)의 이론적 한계(보통 2~5 IPC)에 의해 슈퍼스칼라 확장에는 수확 체감이 존재한다. 이에 따라 SMT(Simultaneous Multi-Threading, 하이퍼스레딩)로 스레드 수준 병렬성을 추가 활용하는 전략이 병행된다.

---

**관련**: 파이프라인(01번) · 병렬/멀티코어(05번) · 폴락의 법칙(08번)
