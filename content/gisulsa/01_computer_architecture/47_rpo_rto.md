+++
weight = 47
title = "47. RPO & RTO"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 RPO & RTO — 복구 목표

> **별점**: ★★★★★ | 기본 필수

## 1. 핵심 지표 정의

```
RTO (Recovery Time Objective):
  장애 발생 → 서비스 복구까지 최대 허용 시간
  = "얼마나 빨리 복구해야 하나?"
  예) RTO = 4시간 → 4시간 내 복구 의무

RPO (Recovery Point Objective):
  장애 발생 → 얼마 이전 시점까지 데이터 복구 허용
  = "어느 시점 데이터까지 잃을 수 있나?"
  예) RPO = 1시간 → 최대 1시간 전 백업까지 허용

[관계]
RTO = 0: 무중단 (Active-Active)
RPO = 0: 무손실 (동기 복제)
비용 ∝ (RTO 단축 + RPO 단축)
```

## 2. DR 사이트 유형

```
[Hot Site]
RTO: 수분 ~ 1시간
RPO: 수분 이내 (준 실시간 복제)
특징: 항상 운영 준비, 실시간 동기
비용: 최고 (자원 이중화 100%)
적합: 금융, 의료, 정부

[Warm Site]
RTO: 4~8시간
RPO: 4~24시간 (주기적 백업)
특징: 일부 자원 사전 준비
비용: 중간
적합: 중요 업무 시스템

[Cold Site]
RTO: 1~3일
RPO: 1일 이상
특징: 공간만 준비, 자원 없음
비용: 최저
적합: 비핵심 시스템, 아카이브

[클라우드 DR]
Pilot Light: 핵심 DB만 복제, 나머지 AMI
Warm Standby: 소규모 클라우드 환경 운영
Multi-Site (Active-Active): 완전 이중화
```

## 3. 백업 유형

```
전체(Full) 백업: 모든 데이터, 오래 걸림, 복구 빠름
증분(Incremental) 백업: 마지막 이후 변경분만
  → 빠른 백업, 복구 느림 (여러 세트 필요)
차등(Differential) 백업: 전체 이후 모든 변경분
  → 증분보다 빠른 복구, 백업 점점 커짐

[3-2-1 규칙]
3개 데이터 복사본
2가지 다른 미디어 타입
1개 오프사이트 보관 (또는 클라우드)
```

## 4. 답안 포인트

**3단락**: ① RPO/RTO 정의 & 차이 → ② Hot/Warm/Cold/클라우드 DR 사이트 비교 → ③ 백업 유형(전체/증분/차등) & 3-2-1 규칙

## 5. 관련 개념

`BCP(07_enterprise 09번)` → RPO/RTO를 BIA로 결정 | `HA(46번)` → HA + DR 조합 | `클라우드(13_cloud)` → 클라우드 DR 비용 최적화
