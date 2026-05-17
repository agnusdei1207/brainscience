+++
weight = 1
title = "15. DevOps/SRE — 키워드 마스터 리스트"
[extra]
categories = "gisulsa-devops"
+++

# 15. DevOps / SRE

> **출제기준**: 시스템 및 응용 소프트웨어
> ★ = 131~136회 기출 확인 / ☆ = 2026~2027 예측

---

## 키워드 마스터 리스트

### A. CI/CD & 자동화

| # | 파일 | 키워드 | 별점 | 출제비고 |
|---|------|--------|:---:|---------|
| 01 | [CI/CD 파이프라인](01_cicd.md) | 빌드→테스트→배포, Jenkins/GitHub Actions | ★★★★★ | ※매회 기본 |
| 02 | [배포 전략](06_deploy_strategy.md) | 블루그린, 카나리, 롤링 | ★★★★★ | ★132회 |
| 03 | [GitOps](07_gitops.md) | ArgoCD, 선언적, Git 단일소스 | ★★★★☆ | ☆예측 |
| 04 | [IaC (코드형 인프라)](03_iac.md) | Terraform, Ansible, 불변 인프라 | ★★★★★ | ※기본 |

### B. SRE & 운영

| # | 파일 | 키워드 | 별점 | 출제비고 |
|---|------|--------|:---:|---------|
| 05 | [SRE 개요](02_sre_observability.md) | SLI/SLO/SLA, 에러 버짓 | ★★★★★ | ※기본 |
| 06 | [옵저버빌리티](08_observability.md) | 로그/메트릭/트레이스, OpenTelemetry | ★★★★★ | ★133회 |
| 07 | [카오스 엔지니어링](09_chaos.md) | 장애주입, GameDay, Netflix Chaos Monkey | ★★★★☆ | ☆예측 |
| 08 | [인시던트 관리](10_incident.md) | 포스트모템, MTTR, 온콜 | ★★★★☆ | ※기본 |

### C. DevSecOps & 보안

| # | 파일 | 키워드 | 별점 | 출제비고 |
|---|------|--------|:---:|---------|
| 09 | [DevSecOps](04_devsecops.md) | Shift Left, SAST/DAST/IAST | ★★★★★ | ※기본 |
| 10 | [SBOM](11_sbom_devops.md) | 공급망 투명성, 취약점 관리 | ★★★★★ | ★134회 |
| 11 | [소프트웨어 공급망 보안](12_supply_chain.md) | SLSA, 빌드 무결성, Sigstore | ★★★★★ | ★136회 |

### D. 플랫폼 엔지니어링 & 최신

| # | 파일 | 키워드 | 별점 | 출제비고 |
|---|------|--------|:---:|---------|
| 12 | [플랫폼 엔지니어링](05_platform_engineering.md) | IDP, 개발자경험(DevEx), 셀프서비스 | ★★★★★ | ★134회 |
| 13 | [AI 기반 DevOps (AIOps)](13_aiops.md) | 이상탐지, 자동치유, 로그분석 | ★★★★★ | ☆2026 확실예측 |
| 14 | [FinOps](14_finops.md) | 클라우드 비용 문화, 태그 관리 | ★★★★☆ | ☆예측 |
| 15 | [그린 소프트웨어](15_green_sw.md) | SCI 지표, 탄소 절감, 에너지효율 | ★★★☆☆ | ☆예측 |

---

> [!NOTE]
> **★★★★★** 최우선: 플랫폼엔지니어링(★134), SBOM(★134), 공급망보안(★136), CI/CD(기본)
> **☆2026**: AIOps, GitOps, 카오스엔지니어링
