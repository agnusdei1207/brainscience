+++
weight = 56
title = "56. RTOS & 실시간 시스템"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 RTOS (실시간 운영체제)

> **별점**: ★★★★★ | 컴시응 특화

## 1. 실시간 시스템 분류

```
경성 실시간 (Hard Real-Time):
  데드라인 절대 준수
  초과 시 치명적 결과
  예) 항공기 비행 제어, 의료 장비, 원자로

연성 실시간 (Soft Real-Time):
  데드라인 초과 허용, 성능 저하
  예) 영상 스트리밍, 게임, 화상통화
  
확정적 실시간 (Firm Real-Time):
  경성+연성 사이: 초과 시 무효 처리
  예) 금융 거래, 화폐 결제
```

## 2. RTOS 스케줄링

```
[선점 스케줄링 (Preemptive)]
높은 우선순위 태스크가 낮은 태스크를 선점
RTOS 필수: 언제든 높은 우선순위 즉시 실행

[RM (Rate Monotonic) 스케줄링]
주기가 짧을수록 높은 우선순위
이론적 이용률 상한: n(2^(1/n) - 1) → 69.3% (n→∞)
최적 고정 우선순위 알고리즘

[EDF (Earliest Deadline First)]
마감시간 가장 가까운 태스크 우선
동적 우선순위, CPU 이용률 100% 가능
이론적으로 최적, 구현 복잡

[우선순위 역전 문제]
낮은 우선순위 태스크가 자원 점유
→ 높은 우선순위 태스크 대기

해결: 우선순위 상속 (Priority Inheritance)
      우선순위 상한 (Priority Ceiling Protocol)

화성 탐사선(패스파인더) 실제 사고 사례
```

## 3. 주요 RTOS

```
FreeRTOS: 오픈소스, 소규모 MCU
  AWS FreeRTOS: IoT 연결 확장
VxWorks: 항공/방어 산업 표준
QNX: 자동차 IVI, 높은 신뢰성
Zephyr: Linux Foundation, IoT
AUTOSAR OS: 차량 전장 표준

[RTOS vs GPOS (범용 OS)]
항목         RTOS          GPOS (Linux)
지연보장      O (경성)       X (최선)
인터럽트 처리  초저지연       최선
선점          모든 상황       커널 섹션 예외
용도          임베디드        서버/PC
```

## 4. 답안 포인트

**3단락**: ① 경성/연성/확정적 실시간 분류 → ② RM/EDF 스케줄링 & 우선순위 역전 → ③ FreeRTOS/VxWorks/QNX/AUTOSAR

## 5. 관련 개념

`ISO 26262(★134회, 57번)` → RTOS = 기능안전 요소 | `임베디드(58번)` → RTOS 기반 임베디드 설계 | `IIoT(06_ict)` → RTOS + 스마트팩토리
