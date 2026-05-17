+++
weight = 26
title = "26. 기능 안전 (SW 관점)"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# 🎯 기능 안전 SW — ISO 26262 SW편 & IEC 61508

> **별점**: ★★★★☆ | ★134회 연계

## 1. 기능 안전 SW 개요

```
기능 안전(Functional Safety): HW/SW 시스템에서 안전 기능이
오동작하여 위험 발생 시 안전 상태로 전환 보장

ISO 26262 Part 6 (SW 개발):
자동차 SW의 ASIL 등급에 따른 개발 요구사항

IEC 61508: 산업 안전 SW 국제 표준 (SIL 기반)
SIL (Safety Integrity Level): SIL 1~4
```

## 2. SW 안전 요구사항 (ASIL에 따라)

```
ASIL D SW 개발 요구:

설계 단계:
- 방어적 프로그래밍 (오류 처리 완전)
- 정형 명세 방법
- 구조적 설계 커버리지 100%

구현 단계:
- 안전 관련 코딩 가이드라인 준수 (MISRA C)
- 정적 분석 도구 (필수 적용)
- MC/DC 커버리지 (100% 요구)

검증 단계:
- 구조적 커버리지: 구문/분기/MC/DC
- 결함 주입 테스트
- 소프트웨어 통합 테스트
```

## 3. MISRA C & MC/DC

```
MISRA C: 자동차 SW를 위한 C 코딩 표준
- 동적 메모리 할당 금지
- 재귀 함수 제한
- 암묵적 형변환 금지

MC/DC (Modified Condition/Decision Coverage):
- 각 조건이 독립적으로 결과에 영향 미침을 증명
- ASIL D: 100% MC/DC 달성 필수
- 항공: DO-178C Level A에서도 필수
```

## 4. 답안 포인트

**3단락**: ① 기능 안전 SW 정의 & ASIL 등급 → ② ASIL D 개발 요구사항(MISRA C, MC/DC) → ③ IEC 61508 SIL 비교

## 5. 관련 개념

`ISO 26262 전체(★134회)` → ASIL 분류·자율주행 연계 | `뮤테이션테스팅(★133회)` → 안전 SW 테스트 보완 | `정형 검증` → 고 ASIL 시스템 수학적 증명
