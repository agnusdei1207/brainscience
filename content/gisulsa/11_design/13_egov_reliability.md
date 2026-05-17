+++
weight = 13
title = "13. 전자정부 표준프레임워크"
date = "2026-05-17"
[extra]
categories = "gisulsa-design"
+++

# 🎯 전자정부 표준프레임워크 & SW 신뢰성

> **별점**: ★★★★★ | 기본 필수

## 1. 전자정부 표준프레임워크

```
행안부 주도, Spring Framework 기반 공공 표준 플랫폼

[구성 요소]
실행 환경:
  프레젠테이션: Spring MVC, Tiles
  비즈니스: Spring IoC, AOP, TX
  데이터: MyBatis, Spring Data JPA
  연계: WSDL, REST

개발 환경:
  이클립스 기반 IDE, 코드 생성, 빌드 자동화

운영 환경:
  모니터링, 배포, 서버 환경

공통 컴포넌트:
  로그인, 게시판, 파일 관리 등 공공 공통 기능 (200+ 개)
  
[버전]
4.x (현재): Spring Boot 기반, MSA 지원
```

## 2. SW 신뢰성

```
신뢰성 (Reliability): 주어진 시간·환경에서 요구 기능을
                      수행할 확률

[신뢰성 지표]
MTTF (Mean Time To Failure): 고장까지 평균 시간
MTTR (Mean Time To Repair): 복구까지 평균 시간
MTBF (Mean Time Between Failure): 고장 간격 평균
MTBF = MTTF + MTTR

가용성 = MTTF / MTBF = MTTF / (MTTF + MTTR)

결함 밀도 (Defect Density):
  결함 수 / 코드 크기 (결함/KLOC)
  배포 전: < 0.5결함/KLOC 목표

[신뢰성 모델]
지수 분포 모델: λ (고장률)이 일정
와이블 분포: 초기 고장→우발 고장→마모 고장 (욕조 곡선)
```

## 3. SW 신뢰성 향상 기법

```
결함 내성 (Fault Tolerance):
  - N-버전 프로그래밍: 독립 팀이 N가지 버전 개발
  - 복구 블록: 체크포인트 기반 롤백
  
방어적 프로그래밍:
  - 입력 검증, 오류 처리, 단언문(Assert)
  - MISRA C, CERT C (안전 코딩 표준)
```

## 4. 답안 포인트

**3단락**: ① 전자정부 표준프레임워크 구성 → ② SW 신뢰성 지표(MTTF/MTTR/가용성) → ③ 결함 내성·방어적 프로그래밍

## 5. 관련 개념

`전자정부법(11번)` → 표준프레임워크 법적 근거 | `SRE(12번)` → MTTF/MTTR을 현대적으로 SLI/SLO로 | `ASIL D(04_sw 26번)` → 고신뢰 SW 개발
