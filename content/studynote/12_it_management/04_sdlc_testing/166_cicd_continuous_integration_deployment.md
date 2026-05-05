+++
weight = 166
title = "166. CI/CD (Continuous Integration / Continuous Deployment) 빌드/테스트 파이프라인"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++

## 0. 핵심 인사이트

> **핵심**: CI/CD (Continuous Integration / Continuous Deployment) 빌드/테스트 파이프라인의 본질은 CI/CD (Continuous Integration / Continuous Deployment) 빌드/테스트 파이프라인의 목적·구성·운영 기준을 명확히 설명하는 주제를 비즈니스 가치, 통제, 실행 관점에서 일관되게 연결하는 데 있다.
> **비유**: 전략과 운영 사이의 간극을 메우는 조정 메커니즘과 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

CI/CD (Continuous Integration / Continuous Delivery & Deployment)는 DevOps 문화의 기술적 핵심이다. 전통적 SW 개발에서는 각 개발자가 오랫동안 독립적으로 작업 후 큰 단위로 통합했다—이른바 "지옥의 통합(Integration Hell)"이 발생했다. 코드 충돌, 예상치 못한 의존성 문제, 수주간의 통합 작업이 반복되었다.

CI는 이 문제를 "매일 또는 매 커밋마다 통합"으로 해결한다. 각 통합에서 자동 빌드와 테스트가 실행되어, 문제를 작게 나누어 조기에 발견하고 즉시 수정한다. CD는 이 통합을 넘어 검증된 코드를 자동으로 스테이징 또는 운영 환경에 배포한다.

실무에서 CI/CD의 비즈니스 가치는 명확하다. 아마존은 11.6초마다 배포를 하고, 넷플릭스는 하루에 수천 번 배포를 한다. 이러한 고속 배포는 CI/CD 파이프라인 없이는 불가능하다. 작은 변경을 자주 배포하면 문제 발생 시 원인 추적이 쉽고, 롤백 범위도 최소화된다.

---

## 2. 구성요소

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

| 도구 | 유형 | 특징 |
|:---|:---|:---|
| Jenkins | 오픈소스 셀프 호스팅 | 가장 넓은 플러그인 생태계 |
| GitHub Actions | 클라우드 네이티브 | GitHub 통합, YAML 기반 |
| GitLab CI/CD | 통합 DevOps 플랫폼 | 완전 통합 (.gitlab-ci.yml) |
| CircleCI | 클라우드 | 빠른 설정, Docker 네이티브 |
| ArgoCD | Kubernetes GitOps | K8s 선언적 배포 |
| Tekton | Kubernetes 네이티브 | Cloud Native CI/CD |

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

---

## 3. 구조 및 원리

| 전략 | 방식 | CI/CD 적합성 |
|:---|:---|:---|
| Git Flow | main/develop/feature/release/hotfix | Continuous Delivery 적합 |
| GitHub Flow | main + feature 브랜치, PR 병합 | 단순, Deployment 적합 |
| Trunk-Based Development | main에 직접 커밋 (기능 플래그 활용) | Continuous Deployment 최적 |
| GitLab Flow | 환경 브랜치 (staging, production) | Delivery 모델 |

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

---

## 4. 비교 및 연결

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

1. **Delivery vs Deployment**: 시험에서 자주 나오는 구분—Delivery는 "인간 승인 필요", Deployment는 "완전 자동".

2. **Shift Left**: 테스트를 개발 프로세스 앞쪽(왼쪽)으로 이동—CI 파이프라인에서 단위 테스트를 첫 단계로.

3. **파이프라인 실패 시**: "Fast Fail"—파이프라인 앞 단계에서 실패하면 뒷 단계를 실행하지 않음.

4. **블루-그린 배포**: CD에서 다운타임 없는 배포를 위해 두 환경을 교차 사용.

---

## 5. 실무 적용 및 판단

CI/CD를 체계적으로 도입하면:

1. **배포 빈도 향상**: 주/월 단위에서 일/시간 단위 배포로 전환—시장 반응 속도가 혁신된다.
2. **변경 실패율 감소**: 자동화된 테스트가 결함을 배포 전에 차단—운영 사고가 줄어든다.
3. **복구 시간 단축**: 문제 발생 시 이전 버전으로 자동 롤백—MTTR (Mean Time to Recovery) 단축.
4. **개발자 생산성**: 반복적인 빌드·배포 수작업에서 해방—가치 창출에 집중.

CI/CD 도입의 핵심은 **문화 변화**다. 도구를 설치했다고 CI/CD가 되지 않는다. "작은 변경을 자주 통합"하는 습관, 파이프라인 실패를 "긴급 사항"으로 인식하는 팀 문화, 자동화된 테스트에 대한 신뢰가 함께 필요하다.

---

## 6. 기대효과 및 결론

CI/CD (Continuous Integration / Continuous Deployment) 빌드/테스트 파이프라인를 올바르게 적용하면 의사결정의 일관성, 운영의 재현성, 통제의 추적성이 동시에 향상된다. 즉 “누가 무엇을 왜 했는가”가 남기 때문에 조직이 커질수록 효과가 커진다.

다만 CI/CD (Continuous Integration / Continuous Deployment) 빌드/테스트 파이프라인는 문서만 잘 만들어도 성공하는 영역이 아니다. 정의와 실행이 분리되면 형식주의가 되고, 자동화만 앞서면 통제 목적이 사라진다. 따라서 표준화와 민첩성, 통제와 생산성 사이의 균형이 항상 필요하다.

향후에는 정책 코드화(Policy as Code), 실시간 관측성(Observability), AI 기반 이상 탐지와 의사결정 지원이 결합되면서 관리 체계가 더 자동화되고 증거 중심으로 진화할 가능성이 크다. 결론적으로 핵심은 도구가 아니라 기준선이며, 기준선이 명확할 때만 자동화와 확장이 의미를 가진다.

---

## 7. 발전 흐름도

```text
개별 대응
    ↓
프로세스 표준화
    ↓
CI/CD (Continuous Integration / Continuous Deployment) 빌드/테스트 파이프라인 정착
    ↓
지표 기반 통제
    ↓
정책 코드화·AI 보조
```

---

## 8. 관련 개념 맵

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
