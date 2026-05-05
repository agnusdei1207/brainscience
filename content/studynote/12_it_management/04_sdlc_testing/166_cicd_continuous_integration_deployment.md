+++
weight = 166
title = "166. CI/CD (Continuous Integration/Continuous Deployment, 지속적 통합/배포)"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++
## 0. 핵심 인사이트

> **핵심**: CI/CD는 코드 변경(커밋)부터 운영 배포까지 자동화된 파이프라인을 통해 소프트웨어를 빠르고 안정적으로 제공하는 DevOps 핵심 실천법으로—CI (Continuous Integration, 지속적 통합)는 코드 통합·검증, CD (Continuous Deployment/Delivery)는 배포 자동화를 담당한다.
> 2. **가치**: CI/CD는 "작은 변경을 자주 통합"하는 방식으로 대형 통합(Big Bang Integration)의 위험을 제거한다—빌드·테스트·배포 사이클을 수분~수시간으로 단축해 시장 출시 시간(Time to Market)을 혁신한다.
> 3. **판단 포인트**: Continuous Delivery와 Continuous Deployment의 차이—Delivery는 운영 배포 전 인간 승인이 있고, Deployment는 완전 자동화로 인간 개입 없이 운영까지 자동 배포된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

CI/CD (Continuous Integration / Continuous Delivery & Deployment)는 DevOps 문화의 기술적 핵심이다. 전통적 SW 개발에서는 각 개발자가 오랫동안 독립적으로 작업 후 큰 단위로 통합했다—이른바 "지옥의 통합(Integration Hell)"이 발생했다. 코드 충돌, 예상치 못한 의존성 문제, 수주간의 통합 작업이 반복되었다.

CI는 이 문제를 "매일 또는 매 커밋마다 통합"으로 해결한다. 각 통합에서 자동 빌드와 테스트가 실행되어, 문제를 작게 나누어 조기에 발견하고 즉시 수정한다. CD는 이 통합을 넘어 검증된 코드를 자동으로 스테이징 또는 운영 환경에 배포한다.

실무에서 CI/CD의 비즈니스 가치는 명확하다. 아마존은 11.6초마다 배포를 하고, 넷플릭스는 하루에 수천 번 배포를 한다. 이러한 고속 배포는 CI/CD 파이프라인 없이는 불가능하다. 작은 변경을 자주 배포하면 문제 발생 시 원인 추적이 쉽고, 롤백 범위도 최소화된다.

📢 **섹션 요약 비유**: CI/CD는 컨베이어 벨트 공장 라인과 같다. 원자재(코드 커밋)가 들어오면 자동으로 조립(빌드), 품질 검사(테스트), 포장(배포 준비), 출하(배포)되어 나온다—사람이 일일이 확인하지 않아도 기준에 맞는 제품이 자동으로 배송된다.

---

## 2. 구성요소

### CI/CD 파이프라인 단계

```text
┌──────────────────────────────────────────────────────────────────┐
│                CI/CD 파이프라인                                   │
├──────────┬──────────┬──────────┬──────────┬─────────────────────┤
│ Source   │ Build    │ Test     │ Stage    │ Deploy              │
│ (소스)   │ (빌드)   │ (테스트) │ (스테이지)│ (배포)              │
├──────────┼──────────┼──────────┼──────────┼─────────────────────┤
│ Git 커밋 │ 컴파일   │ 단위     │ 스테이징 │ 운영 배포           │
│ PR 병합  │ 패키징   │ 통합     │ 환경 배포│ (Delivery: 승인 후) │
│ 코드     │ Docker   │ E2E      │ 성능/    │ (Deployment: 자동)  │
│ 리뷰     │ 이미지   │ 테스트   │ 보안 테스│                     │
│          │ 빌드     │ 정적 분석│ 트       │                     │
└──────────┴──────────┴──────────┴──────────┴─────────────────────┘
        │         │         │          │             │
      즉시      2-5분    5-20분     30-60분        결정
      트리거    완료      완료        완료          (승인 or 자동)
```

### CI vs CD 구분

```text
┌──────────────────────────────────────────────────────────────┐
│  CI (Continuous Integration, 지속적 통합)                    │
│    코드 커밋 → 빌드 → 단위 테스트 → 통합 테스트             │
│    목표: 코드 통합 문제를 즉시 발견                          │
│    주기: 매 커밋마다 (수분 이내)                             │
├──────────────────────────────────────────────────────────────┤
│  CD (Continuous Delivery, 지속적 제공)                       │
│    CI 통과 → 스테이징 자동 배포 → 수동 승인 → 운영 배포     │
│    목표: 언제든 운영 배포 가능한 상태 유지                   │
│    인간 개입: 최종 운영 배포 전 승인                         │
├──────────────────────────────────────────────────────────────┤
│  CD (Continuous Deployment, 지속적 배포)                     │
│    CI 통과 → 모든 검증 통과 → 자동 운영 배포                │
│    목표: 사람 없이 코드가 운영까지 자동 배포                 │
│    인간 개입: 없음 (실패 시 자동 롤백)                       │
└──────────────────────────────────────────────────────────────┘
```

### CI/CD 도구 생태계

| 도구 | 유형 | 특징 |
|:---|:---|:---|
| Jenkins | 오픈소스 셀프 호스팅 | 가장 넓은 플러그인 생태계 |
| GitHub Actions | 클라우드 네이티브 | GitHub 통합, YAML 기반 |
| GitLab CI/CD | 통합 DevOps 플랫폼 | 완전 통합 (.gitlab-ci.yml) |
| CircleCI | 클라우드 | 빠른 설정, Docker 네이티브 |
| ArgoCD | Kubernetes GitOps | K8s 선언적 배포 |
| Tekton | Kubernetes 네이티브 | Cloud Native CI/CD |

### Shift Left Testing

```text
전통적:
  개발 → → → → → → 테스트 → 배포
  (테스트가 늦게 실행, 결함 발견 지연)

Shift Left (CI/CD):
  커밋→단위테스트→통합테스트→E2E→스테이징→배포
  (테스트를 파이프라인 앞쪽으로 이동)
  
  효과:
  - 결함을 개발 단계에서 즉시 발견
  - 수정 비용 최소화 (결함 발견이 빠를수록 저렴)
  - 배포 품질 보장
```

📢 **섹션 요약 비유**: Shift Left Testing은 건강 검진을 1년에 한 번에서 매달 하는 것과 같다. 작은 이상을 조기에 발견하면 치료(수정)가 훨씬 쉽고 저렴하다—CI/CD는 매 커밋마다 건강 검진을 자동으로 한다.

---

## 3. 구조 및 동작 원리

### 브랜치 전략 비교

| 전략 | 방식 | CI/CD 적합성 |
|:---|:---|:---|
| Git Flow | main/develop/feature/release/hotfix | Continuous Delivery 적합 |
| GitHub Flow | main + feature 브랜치, PR 병합 | 단순, Deployment 적합 |
| Trunk-Based Development | main에 직접 커밋 (기능 플래그 활용) | Continuous Deployment 최적 |
| GitLab Flow | 환경 브랜치 (staging, production) | Delivery 모델 |

### CI/CD 성숙도 모델

```text
레벨 1: 수동 빌드·배포
  → 개발자가 수동으로 빌드 및 배포

레벨 2: 자동화된 빌드 (CI 시작)
  → 커밋 시 자동 빌드, 수동 테스트

레벨 3: 자동화된 테스트 (CI 완성)
  → 커밋 시 빌드+테스트 자동화

레벨 4: 자동화된 스테이징 배포 (CD - Delivery)
  → 테스트 통과 시 스테이징 자동 배포

레벨 5: 완전 자동화 운영 배포 (CD - Deployment)
  → 모든 검증 통과 시 운영 자동 배포, 자동 롤백
```

📢 **섹션 요약 비유**: Trunk-Based Development는 모든 요리사가 같은 요리책(main)을 동시에 사용하는 것이다. 기능 플래그(Feature Flag)는 "아직 완성되지 않은 요리는 손님에게 내지 않는" 가림막이다.

---

## 4. 비교 및 트레이드오프

### GitHub Actions 예시

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: mvn package
      - name: Test
        run: mvn test
      - name: Code Coverage
        run: mvn jacoco:report

  deploy-staging:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Staging
        run: ./deploy.sh staging

  deploy-production:
    needs: deploy-staging
    environment: production  # 수동 승인 필요 (Delivery)
    steps:
      - name: Deploy to Production
        run: ./deploy.sh production
```

### 기술사 시험 판단 포인트

1. **Delivery vs Deployment**: 시험에서 자주 나오는 구분—Delivery는 "인간 승인 필요", Deployment는 "완전 자동".

2. **Shift Left**: 테스트를 개발 프로세스 앞쪽(왼쪽)으로 이동—CI 파이프라인에서 단위 테스트를 첫 단계로.

3. **파이프라인 실패 시**: "Fast Fail"—파이프라인 앞 단계에서 실패하면 뒷 단계를 실행하지 않음.

4. **블루-그린 배포**: CD에서 다운타임 없는 배포를 위해 두 환경을 교차 사용.

📢 **섹션 요약 비유**: Continuous Delivery와 Continuous Deployment의 차이는 비행기 자동 착륙과 수동 착륙의 차이다. Delivery는 "자동 비행 후 파일럿이 착륙 버튼을 누름", Deployment는 "이륙부터 착륙까지 완전 자동"이다.

---

## 5. 실무 적용 및 최적화 기법

CI/CD를 체계적으로 도입하면:

1. **배포 빈도 향상**: 주/월 단위에서 일/시간 단위 배포로 전환—시장 반응 속도가 혁신된다.
2. **변경 실패율 감소**: 자동화된 테스트가 결함을 배포 전에 차단—운영 사고가 줄어든다.
3. **복구 시간 단축**: 문제 발생 시 이전 버전으로 자동 롤백—MTTR (Mean Time to Recovery) 단축.
4. **개발자 생산성**: 반복적인 빌드·배포 수작업에서 해방—가치 창출에 집중.

CI/CD 도입의 핵심은 **문화 변화**다. 도구를 설치했다고 CI/CD가 되지 않는다. "작은 변경을 자주 통합"하는 습관, 파이프라인 실패를 "긴급 사항"으로 인식하는 팀 문화, 자동화된 테스트에 대한 신뢰가 함께 필요하다.

📢 **섹션 요약 비유**: CI/CD 없는 소프트웨어 배포는 택배 없는 인터넷 쇼핑과 같다. 좋은 상품(코드)이 있어도 고객(사용자)에게 전달되는 과정이 느리고 불안정하면 가치가 없다—CI/CD는 초고속 자동 택배 시스템이다.

---

### 📌 관련 개념 맵

| 개념 | 설명 | 연관 키워드 |
|:---|:---|:---|
| CI (Continuous Integration) | 코드 커밋→빌드→테스트 자동화 | Jenkins, GitHub Actions |
| CD (Continuous Delivery) | 스테이징 자동 배포+수동 승인 | 운영 준비 상태 유지 |
| CD (Continuous Deployment) | 완전 자동 운영 배포 | 고성숙 팀 |
| 파이프라인 (Pipeline) | Source→Build→Test→Stage→Deploy | 자동화 흐름 |
| Shift Left Testing | 테스트를 파이프라인 앞쪽으로 | 조기 결함 발견 |
| 트렁크 기반 개발 | main에 자주 커밋, 기능 플래그 활용 | Continuous Deployment |
| Feature Flag | 미완성 기능을 배포하되 비활성화 | 위험 분리 |
| Blue-Green Deployment | 두 환경 교차로 무중단 배포 | 롤백 전략 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. CI는 매일 숙제를 내면 선생님이 바로 채점해주는 것이에요 — 틀린 부분을 즉시 알 수 있어서 나중에 크게 틀리는 일이 없어요.
2. CD (Delivery)는 숙제 검사 후 부모님이 "잘 됐다" 하면 학교에 제출하는 것이고, CD (Deployment)는 자동으로 학교에 제출되는 것이에요.
3. CI/CD가 있으면 "내가 고친 코드가 다른 부분을 망가뜨리지 않았나?" 걱정 없이 마음 놓고 개발할 수 있어요.
