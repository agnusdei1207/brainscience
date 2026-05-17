+++
weight = 12
title = "12. IT 서비스 관리 (ITSM)"
date = "2026-05-17"
[extra]
categories = "gisulsa-it-mgmt"
+++

# 🎯 ITSM (IT 서비스 관리) & CMDB

> **별점**: ★★★★★ | 기본 필수

## 1. ITSM 핵심 프로세스

```
[인시던트 관리 (Incident Management)]
목적: 서비스 중단 → 최대한 빨리 복구
     (원인 해결 아님 → 임시 해결 포함)

[문제 관리 (Problem Management)]
목적: 인시던트의 근본 원인 제거
     재발 방지
Known Error: 근본 원인은 알지만 해결 전
사전적: 인시던트 발생 전 잠재 문제 탐지

[변경 관리 (Change Management)]
목적: 변경으로 인한 서비스 중단 최소화
RFC (Request For Change): 변경 요청
CAB (Change Advisory Board): 변경 승인 위원회
긴급 변경: 즉시 승인 절차 (ECAB)

[릴리즈 관리 (Release Management)]
소프트웨어/인프라 변경을 계획·빌드·테스트·배포

[서비스 데스크]
사용자 단일 접점 (Single Point Of Contact)
1차 해결 → 2차 에스컬레이션 → 3차 전문가
```

## 2. CMDB (Configuration Management DB)

```
정의: IT 인프라의 모든 구성 항목(CI)과 관계를 기록하는 DB

CI (Configuration Item):
  서버, 애플리케이션, 네트워크 장비, 관계
  
CMDB 활용:
  인시던트: "이 서버와 연결된 시스템은?" → 영향 분석
  변경: "이 서버 변경 시 어디에 영향?" → 위험 평가
  자산 관리: 라이선스, 유지보수 계약

도구: ServiceNow, BMC Helix, Jira Service Management
```

## 3. 현대 ITSM vs SRE

```
전통 ITSM (ITIL 기반):
  프로세스·절차 중심, 문서 많음
  변경 승인 오래 걸림

SRE (현대):
  코드·자동화 중심, 빠른 변경
  에러 버짓으로 변경 의사결정
  → SRE = ITIL의 엔지니어링화
```

## 4. 답안 포인트

**3단락**: ① 인시던트/문제/변경 관리 정의 & 차이 → ② CMDB 역할 & CI 관계 → ③ ITIL ITSM vs SRE 비교

## 5. 관련 개념

`ITIL v4(07번)` → ITSM의 프레임워크 | `SRE(06번)` → ITSM의 현대적 대안 | `플랫폼 엔지니어링(15_devops)` → 내부 ITSM 자동화
