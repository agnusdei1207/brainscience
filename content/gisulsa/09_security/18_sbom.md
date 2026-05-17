+++
weight = 18
title = "17. SBOM (Software Bill of Materials)"
date = "2026-05-17"
[extra]
categories = "gisulsa-security"
+++

# SBOM, 소프트웨어 재료명세서, 공급망 보안, SPDX, CycloneDX

> 출제 빈도: ★★★★★ | 기출: ★134회 | 연계: 보안, SW공학, DevOps

---

## 답안.

### Ⅰ. 개요

SBOM(Software Bill of Materials)은 소프트웨어를 구성하는 **모든 컴포넌트, 라이브러리, 의존성의 목록**을 체계적으로 문서화한 "SW 재료명세서"이다.
미국 대통령 행정명령 EO 14028(2021)으로 연방 정부 소프트웨어에 SBOM 의무화 → 글로벌 표준화 추세.

### Ⅱ. 핵심 구성요소

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


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
