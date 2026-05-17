+++
weight = 1
title = "01. CI/CD 파이프라인"
date = "2026-05-18"
[extra]
categories = "gisulsa-devops"
+++

# CI/CD 파이프라인

> 출제 빈도: ★★★★★ | 매회 기본

---

## 답안.

### Ⅰ. 개요

CI/CD(Continuous Integration / Continuous Delivery·Deployment)는 소프트웨어의 빌드·테스트·배포를 자동화하여 릴리스 주기를 단축하고 품질을 보장하는 DevOps의 핵심 실천이다. CI는 코드 통합 시 자동 빌드·테스트를, CD는 검증된 코드의 자동 배포를 수행한다.

### Ⅱ. 파이프라인 구조

```
개발자 코드 커밋
    ↓
┌──────────────────────────────────────────┐
│ CI (지속적 통합)                          │
│  Source → Build → Unit Test → SAST       │
│                                          │
│ CD (지속적 배포)                          │
│  → Integration Test → Stage → Approval   │
│  → Production Deploy                     │
└──────────────────────────────────────────┘
    ↓
모니터링 & 피드백 (SRE)
```

### Ⅲ. 핵심 구성요소

| 구성요소 | 역할 | 대표 도구 |
|---------|------|----------|
| 소스 관리 | 버전 관리, 브랜치 전략 | Git, GitHub |
| 빌드 자동화 | 컴파일, 패키징 | Maven, Gradle, Docker |
| 테스트 자동화 | 단위·통합·E2E 테스트 | JUnit, Selenium, Jest |
| 보안 스캔 | SAST/DAST/SCA | SonarQube, Trivy |
| 배포 전략 | 무중단 배포 | ArgoCD, Spinnaker |
| 모니터링 | 성능·에러 추적 | Prometheus, Grafana |

### Ⅳ. 배포 전략 비교

| 전략 | 방법 | 장점 | 단점 |
|------|------|------|------|
| 롤링 | 인스턴스 순차 교체 | 자원 효율 | 버전 혼재 |
| 블루/그린 | 두 환경 전환 | 즉시 롤백 | 2배 인프라 |
| 카나리 | 소수에 먼저 배포 | 리스크 최소화 | 관측성 필요 |
| A/B 테스트 | 사용자 그룹별 분배 | 데이터 기반 검증 | 복잡한 설정 |

### Ⅴ. GitOps와의 연계

GitOps는 Git 저장소를 단일 진실의 원천(SSOT)으로 삼아 선언적 인프라와 애플리케이션 상태를 관리하는 운영 모델이다. ArgoCD가 Git과 클러스터 상태를 지속 동기화하여 드리프트를 자동 교정한다.

---

**관련**: IaC(03번) · DevSecOps(04번) · GitOps(09번) · SRE(02번)
