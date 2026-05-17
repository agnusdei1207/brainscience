+++
weight = 12
title = "12. ITIL & SLA"
date = "2026-05-17"
[extra]
categories = "gisulsa-enterprise"
+++

# 🎯 ITIL v4 & IT 서비스 관리 & SLA

> **별점**: ★★★★★ | 기본 필수

## 1. ITIL v4 개요

```
ITIL (IT Infrastructure Library): 전 세계 표준 IT 서비스 관리 프레임워크

[ITIL v4 서비스 가치 시스템 (SVS)]
핵심 구성:
- 서비스 가치 체인 (SVC): 계획→개선→참여→설계전환→획득구축→제공지원
- 관행 (Practices): 34개 관리 관행
- 거버넌스 원칙
- 지속적 개선

[4가지 차원]
조직 & 인력
정보 & 기술
파트너 & 공급자
가치 흐름 & 프로세스
```

## 2. ITIL 핵심 관행 (Practices)

```
[주요 관행 20개 이해]
서비스 데스크: 단일 접점 (SPOC)
인시던트 관리: 서비스 중단 빠른 복구
문제 관리: 근본 원인 분석, 재발 방지
변경 관리: 변경 위험 평가·승인·실행
CMDB: 구성 항목 정보 데이터베이스
가용성 관리: 가용성 목표 달성
용량 관리: 수요 예측, 리소스 계획
서비스 연속성 관리: BCP/DRS 연계
서비스 수준 관리: SLA 협의·모니터링
```

## 3. SLA & OLA

```
SLA (Service Level Agreement): 서비스 제공자-고객 간 약정
  - 가용성: 99.9% (연간 8.76시간 다운)
  - 응답 시간: 2초 이내
  - 처리량: 1000 TPS 이상
  - 지원 시간: 24×7 or 8×5

OLA (Operational Level Agreement): 내부 팀 간 약정
  - SLA 달성을 위한 내부 지원 조건

UC (Underpinning Contract): 외부 공급사와 계약

SLA 위반 대응:
  페널티, 보상 크레딧
  에스컬레이션 프로세스
```

## 4. 답안 포인트

**3단락**: ① ITIL v4 SVS 구조 → ② 주요 관행(인시던트/문제/변경/SLA 관리) → ③ SLA/OLA/UC 계층 구조

## 5. 관련 개념

`BCP(★133회)` → 서비스 연속성 관리 | `SRE` → SRE는 ITIL의 현대적 재해석 | `PMO(★132회)` → 변경관리·프로젝트 연계
