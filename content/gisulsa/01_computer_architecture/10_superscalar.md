+++
weight = 10
title = "10. 슈퍼스칼라 & 비순차 실행"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 슈퍼스칼라 & 비순차 실행 (OoO)

> **별점**: ★★★★☆ | 기본 필수

## 1. 슈퍼스칼라 (Superscalar)

```
정의: 한 사이클에 여러 명령어를 동시에 발행(Issue)·실행

vs 단순 파이프라인: 1사이클 = 1명령어 진행
슈퍼스칼라: 1사이클 = N명령어 동시 (IPC > 1)

[구성 요소]
다중 이슈 큐: 여러 명령어를 동시 디코드
실행 유닛 다중화:
  정수 ALU × 2~4개
  부동소수점 FPU
  로드/스토어 유닛
  분기 예측기
```

## 2. 비순차 실행 (OoO, Out-of-Order)

```
정의: 준비된 명령어를 프로그램 순서와 관계없이 실행

[OoO 파이프라인]
Fetch → Decode → 명령어 재정렬 버퍼(ROB)
  → 예약 스테이션 (RS) → 실행 유닛 → 완료(Commit)

[핵심 구성]
ROB (ReOrder Buffer):
  완료 순서를 프로그램 순서로 정렬 (보장)
  예외·분기 오예측 시 롤백

Tomasulo 알고리즘:
  레지스터 이름 바꾸기 (RAW/WAW/WAR 해저드 해결)

[해저드 해결]
RAW (Read After Write): 데이터 해저드 → 포워딩
WAR (Write After Read): 이름 바꾸기로 해결
WAW (Write After Write): 이름 바꾸기로 해결
```

## 3. 분기 예측 (Branch Prediction)

```
동적 분기 예측:
  2-bit 예측기: 4가지 상태 (강/약 taken/not-taken)
  BTB (Branch Target Buffer): 분기 목적지 캐시
  
분기 오예측 페널티:
  최신 CPU: 15~20사이클 낭비
  → 중요한 성능 요소
  
스펙터 취약점:
  분기 예측을 이용한 투기적 실행 → 정보 누출
```

## 4. 답안 포인트

**3단락**: ① 슈퍼스칼라 정의 & 다중 이슈 구조 → ② OoO 실행 & ROB/Tomasulo → ③ 분기 예측 & 스펙터 취약점

## 5. 관련 개념

`파이프라이닝(09번)` → 슈퍼스칼라의 기반 | `캐시 일관성(14번)` → OoO + 멀티코어 동시성 | `스펙터/멜트다운(54번)` → 투기적 실행 취약점
