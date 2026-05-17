+++
weight = 25
title = "25. CMMI & SPICE"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# 🎯 SBOM & 공급망 보안 (SW공학 관점)

> **별점**: ★★★★★ | ★134회, ★136회 기출

## 1. SBOM (SW 재료명세서)

```
정의: SW를 구성하는 모든 컴포넌트·라이브러리·의존성 목록
= 식품의 성분표 (SW 버전)

[왜 중요한가]
현대 SW의 70~90%: 오픈소스 라이브러리
Log4Shell(2021): Log4j 취약점 → 수천만 시스템 영향
SBOM 없이: 어떤 시스템이 영향받는지 파악 불가 (수일 소요)
SBOM 있으면: 즉시 영향 범위 파악 → 수시간 내 패치

[표준]
SPDX (Linux Foundation): ISO/IEC 5962:2021 공식 표준
CycloneDX (OWASP): 보안 특화, JSON/XML
```

## 2. SLSA (소프트웨어 공급망 레벨)

```
SLSA (Supply chain Levels for Software Artifacts):
구글 제안, 빌드 공급망 무결성 보장 프레임워크

[SLSA 레벨]
L0: 보장 없음
L1: 빌드 스크립트 존재 (수동 빌드)
L2: 빌드 서비스 사용 (GitHub Actions 등)
L3: 독립 감사 가능 빌드 서비스
L4: 두 관계자 검토, 헤르메틱 빌드

SolarWinds 공격: 빌드 파이프라인 침해
→ SLSA 빌드 무결성으로 대응
```

## 3. DevSecOps 연계

```
[CI/CD에서 SBOM 자동화]
소스코드 commit
    ↓
SBOM 자동 생성 (Syft, SBOM-tool)
    ↓
취약점 스캐닝 (CVE DB 대조, Grype)
    ↓
SLSA 서명 (Sigstore Cosign)
    ↓
컨테이너 이미지 + SBOM 함께 레지스트리 저장
    ↓
배포 시 SBOM 검증
```

## 4. 답안 포인트

**3단락**: ① SBOM 정의 & 필요성(Log4Shell 사례) → ② SPDX/CycloneDX 표준 & SLSA 레벨 → ③ CI/CD 파이프라인 통합 & 국내 의무화 동향

## 5. 관련 개념

`DevSecOps` → SBOM 파이프라인 핵심 | `Zero Trust(★136회)` → SW 신뢰 검증 | `감리(★134회)` → SBOM 체크리스트 포함
