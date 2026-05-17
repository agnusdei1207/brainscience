+++
weight = 17
title = "17. SBOM (Software Bill of Materials)"
date = "2026-05-17"
[extra]
categories = "gisulsa-security"
exam = "★ 134회 기출"
+++

# 🎯 핵심 키워드: SBOM, 소프트웨어 재료명세서, 공급망 보안, SPDX, CycloneDX

> **출제 빈도**: ★★★★★ | **기출**: ★134회 | **연계**: 보안, SW공학, DevOps

## 1. 정의

SBOM(Software Bill of Materials)은 소프트웨어를 구성하는 **모든 컴포넌트, 라이브러리, 의존성의 목록**을 체계적으로 문서화한 "SW 재료명세서"이다.

미국 대통령 행정명령 EO 14028(2021)으로 연방 정부 소프트웨어에 SBOM 의무화 → 글로벌 표준화 추세.

## 2. 출제 포인트

| 포인트 | 내용 | 채점 비중 |
|--------|------|----------|
| 정의 | SBOM 목적, 구성 요소 | 20% |
| 표준 | SPDX, CycloneDX, SWID | 25% |
| 활용 | 취약점 탐지, CVE 대응 | 30% |
| 국내 | 과기부 가이드라인, 공공 적용 | 25% |

## 3. 답안 목차 템플릿

**문제**: "SBOM(소프트웨어 재료명세서)의 개념과 필요성, SW 공급망 보안에서의 역할을 설명하시오."

```
I. SBOM 정의 및 배경
   - 오픈소스 의존성: 현대 SW의 70~90%가 오픈소스
   - Log4Shell(2021): Log4j 취약점 → SBOM 없이 영향받는 SW 파악 불가
   - SolarWinds 공격: 빌드 공급망 침해 → SBOM으로 추적 가능

II. SBOM 구성 요소 & 표준
   
   SBOM 필수 포함 정보 (NTIA 기준):
   - 공급자 이름, 컴포넌트 이름, 버전
   - 고유 식별자 (CPE, PURL)
   - 의존성 관계, 타임스탬프, 생성자
   
   SBOM 표준:
   | 표준       | 주관         | 형식          | 특징           |
   |-----------|-------------|--------------|----------------|
   | SPDX      | Linux Foundation | JSON/YAML/RDF | SBOM 공식표준 |
   | CycloneDX | OWASP        | JSON/XML      | 보안 특화      |
   | SWID      | ISO/IEC 19770 | XML          | 설치 소프트웨어 |

III. SBOM 활용: SW 공급망 보안
   
   [SBOM 기반 취약점 대응 흐름]
   SBOM 생성 (CI/CD 자동화)
      ↓
   CVE 데이터베이스 연동 (NVD, OSV)
      ↓
   취약 컴포넌트 자동 탐지
      ↓
   업데이트/패치 권고 자동화
      ↓
   영향받는 시스템 즉시 파악
   
   도구:
   - Syft: SBOM 자동 생성
   - Grype: SBOM 기반 취약점 스캐닝
   - Dependency-Track: SBOM 관리 플랫폼

IV. 국내 적용 현황
   - 과기부 '소프트웨어 공급망 보안 가이드라인' (2023)
   - 공공SW 사업: SBOM 제출 의무화 추진
   - 감리: SBOM 포함 여부 체크 예상
   - DevSecOps: CI/CD 파이프라인 내 SBOM 자동 생성/검증
```

## 4. 핵심 암기 포인트

- **Log4Shell = SBOM 의무화의 직접 계기**
- **SPDX**: Linux Foundation 표준, 공식 SBOM 표준
- **CycloneDX**: OWASP, 보안 특화 SBOM
- **연계**: SBOM → CVE 대조 → 취약 컴포넌트 자동 탐지

## 5. 관련 개념 연결

| 개념 | 연결 포인트 |
|------|------------|
| 공급망 보안 (★136회) | SBOM은 공급망 보안의 핵심 도구 |
| DevSecOps | CI/CD에서 SBOM 자동 생성 |
| 플랫폼 엔지니어링 (★134회) | IDP에서 SBOM 관리 |
| Zero Trust (★136회) | SBOM 기반 소프트웨어 신뢰 검증 |
| 정보시스템 감리 | SBOM 제출 감리 체크 |
