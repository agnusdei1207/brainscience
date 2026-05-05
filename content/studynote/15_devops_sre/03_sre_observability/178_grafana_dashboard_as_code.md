+++
weight = 178
title = "178. 그라파나 Dashboard as Code (Grafana Dashboard Provisioning)"
date = "2026-04-21"
[extra]
categories = "studynote-devops-sre"
+++

## 0. 핵심 인사이트

> **핵심**: Dashboard as Code는 Grafana 대시보드를 JSON/YAML로 선언하고 Git에 버전 관리함으로써 인프라 변경과 동기화된 관측성을 보장한다.
> **비유**: Dashboard as Code는 마치 건물 설계도(코드)를 Git에 보관하는 것 — 누가 벽을 옮겼는지, 언제 창문이 추가됐는지 모두 기록되며, 같은 설계도로 여러 건물(환경)을 동일하게 지을 수 있다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

Grafana 대시보드는 강력한 시각화 도구지만, UI 클릭으로 생성된 대시보드는 버전 관리가 되지 않아 "누가 언제 어떤 패널을 삭제했는지" 추적이 불가능하다. 장애 대응 중 실수로 대시보드를 망가뜨리거나, 개발·스테이징·운영 환경의 대시보드가 서로 다른 내용을 보여주는 혼란이 발생한다.

Dashboard as Code는 이 문제를 Git 워크플로우로 해결한다. 대시보드 JSON을 코드 리뷰(PR), CI 검증, 자동 배포 파이프라인으로 관리하면 인프라 변경과 관측 대시보드 변경이 동일한 배포 단위로 묶인다. 예를 들어 새 마이크로서비스를 배포할 때 서비스 코드와 Grafana 대시보드 JSON이 동일한 PR에 포함된다.

Grafana는 세 가지 공식 메커니즘으로 Dashboard as Code를 지원한다. 첫째 파일 기반 Provisioning(대시보드 JSON을 `/etc/grafana/provisioning/dashboards/`에 마운트), 둘째 Grafana API를 통한 배포 자동화, 셋째 Terraform Grafana Provider를 통한 IaC 통합이다.

더 나아가 Grafonnet 같은 Jsonnet 기반 라이브러리를 사용하면 대시보드를 프로그래밍 방식으로 생성할 수 있다. 동일 구조의 패널을 서비스별로 반복 생성하거나, 표준 대시보드 템플릿을 상속받아 서비스별 커스터마이징을 수행하는 DRY(Don't Repeat Yourself) 원칙을 적용할 수 있다.

---

## 2. 구성요소

### Dashboard as Code 배포 파이프라인

```
개발자
  │
  │ git push
  ▼
┌─────────────────────────┐
│    Git Repository        │
│  /dashboards/            │
│    ├── svc-payment.json  │
│    ├── svc-auth.json     │
│    └── infra-k8s.json    │
└──────────┬──────────────┘
           │ PR 생성
           ▼
┌─────────────────────────┐
│     CI 파이프라인         │
│  ① jsonlint 검증         │
│  ② grafana-dashboard-lint│
│  ③ 스키마 버전 호환 검사  │
└──────────┬──────────────┘
           │ 머지 후 자동 배포
           ▼
┌─────────────────────────┐
│   배포 방식 선택          │
├──────────┬──────────────┤
│ 파일 마운트│ Terraform    │
│ (K8s CM) │ grafana prov.│
│          │ /API Push    │
└──────────┴──────────────┘
           │
           ▼
┌─────────────────────────┐
│     Grafana 인스턴스     │
│  대시보드 자동 업데이트   │
└─────────────────────────┘
```

---

## 3. 구조 및 원리

**핵심 조건**: 측정 가능한 SLI, 합의된 SLO, 실행 가능한 경보·복구 절차가 하나의 폐쇄 루프를 이뤄야 한다.

동작 순서:
1. 사용자 경험을 대표하는 지표를 선택해 서비스 상태를 수치화한다.
2. 허용 가능한 목표치와 에러 버짓을 정해 변화 속도와 안정성의 기준선을 만든다.
3. 메트릭·로그·트레이스로 이상 징후를 탐지하고 원인을 빠르게 국소화한다.
4. 장애 이후 포스트모템과 자동화를 통해 토일을 줄이고 재발 방지책을 시스템에 반영한다.

```text
서비스 요청
   ↓
측정(SLI)
   ↓
목표(SLO)·예산
   ↓
알림·복구
   ↓
학습·자동화
```

---

## 4. 비교 및 연결

| 방식 | 도구 | 장점 | 단점 |
|:---|:---|:---|:---|
| 파일 Provisioning | JSON + ConfigMap | 단순, Grafana 기본 내장 | 동적 생성 어려움 |
| API 배포 | curl + CI/CD | 유연, 현재 상태 확인 가능 | 상태 관리 필요 |
| Terraform | grafana provider | IaC 통합, 상태 파일 관리 | TF 학습 곡선 |
| Grafonnet | Jsonnet 라이브러리 | 재사용·상속·DRY | 복잡한 빌드 체인 |

### Grafana Provisioning YAML 구성 예시

```yaml
apiVersion: 1
providers:
  - name: 'GitOps Dashboards'
    orgId: 1
    folder: 'SRE'
    type: file
    disableDeletion: true   # 코드 외 수동 삭제 방지
    updateIntervalSeconds: 30
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true
```

| 항목 | 수동 UI 생성 | Dashboard as Code |
|:---|:---|:---|
| 버전 관리 | 불가 (Grafana 내부 히스토리만) | Git 풀 히스토리 |
| 환경 간 일관성 | 수동 복사, 불일치 발생 | 동일 코드로 자동 배포 |
| 코드 리뷰 | 불가 | PR 기반 리뷰 가능 |
| 실수 복구 | Grafana 버전 복원 (제한적) | `git revert` 즉시 롤백 |
| 재사용성 | 복사-붙여넣기 | 템플릿·상속 (Grafonnet) |

| 도구 | 역할 | 특이사항 |
|:---|:---|:---|
| grafana/grafana-foundation-sdk | 공식 TypeScript/Python SDK | 타입 안전한 대시보드 생성 |
| Grafonnet | Jsonnet 라이브러리 | 커뮤니티 표준, 재사용성 최고 |
| grafana-dash-gen | Python 기반 생성기 | 구형, 점차 대체됨 |
| Terraform grafana provider | 상태 기반 관리 | 삭제·업데이트 완전 제어 |

### Dashboard as Code CI/CD 파이프라인 구성

```yaml
name: Deploy Grafana Dashboards
on:
  push:
    paths:
      - 'dashboards/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint dashboards
        run: |
          npx @grafana/dashboard-linter dashboards/**/*.json

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - name: Push to Grafana API
        run: |
          for f in dashboards/**/*.json; do
            curl -X POST \
              -H "Authorization: Bearer ${{ secrets.GRAFANA_TOKEN }}" \
              -H "Content-Type: application/json" \
              -d @"$f" \
              "$GRAFANA_URL/api/dashboards/db"
          done
```

---

## 5. 실무 적용 및 판단

| 시나리오 | 권장 방식 | 이유 |
|:---|:---|:---|
| 소규모 팀, 단일 Grafana | 파일 Provisioning | 설정 단순, 유지보수 용이 |
| 다수 서비스, 표준화 필요 | Grafonnet + CI/CD | 재사용성, DRY 원칙 |
| 멀티 Grafana 인스턴스 | Terraform | 상태 일관성, IaC 통합 |
| 엔터프라이즈 Grafana Cloud | Grafana Foundation SDK | 공식 지원, 타입 안전성 |

Dashboard as Code를 도입하면 대시보드 변경에 대한 책임 추적(Accountability)이 가능해지고, 장애 대응 중 실수로 인한 대시보드 손상을 즉시 복구할 수 있다. 새 서비스 출시 시 관련 대시보드가 자동으로 배포되어 관측성 공백(Observability Gap)을 예방한다.

운영 환경에서 SRE 팀이 직접 Grafana를 클릭하지 않아도 되므로 인적 오류가 감소하고, 신규 팀원이 대시보드 구조를 코드로 이해할 수 있어 온보딩이 빨라진다. 또한 대시보드가 서비스 코드와 함께 PR로 관리되므로 인프라 변경과 관측 변경의 동기화가 자연스럽게 이루어진다.

향후 방향으로는 Grafana Scenes(React 기반 동적 대시보드)와 결합하여 더 인터랙티브한 코드 기반 대시보드가 표준이 될 것이며, OpenTelemetry 메트릭·트레이스·로그 데이터 모델과 직접 연동하는 자동 대시보드 생성 도구도 등장할 것이다.

---

## 6. 기대효과 및 결론

그라파나 Dashboard as Code (Grafana Dashboard Provisioning)을(를) 도입하면 자동화와 표준화를 통해 속도·안정성·가시성의 균형을 높일 수 있다. 다만 효과를 얻으려면 측정 가능한 SLI, 합의된 SLO, 실행 가능한 경보·복구 절차가 하나의 폐쇄 루프를 이뤄야 한다는 전제가 충족되어야 하며, 도구만 도입하고 운영 원칙을 바꾸지 않으면 기대 효과가 빠르게 한계에 부딪힌다.

결론적으로 그라파나 Dashboard as Code (Grafana Dashboard Provisioning)은(는) 개별 기능이 아니라 운영 체계 전체의 품질을 재정렬하는 방식이며, 향후에는 플랫폼화·정책화·AI 기반 최적화와 결합해 더 높은 수준의 자동 운영으로 확장된다.

---

## 7. 발전 흐름도

```text
전통 운영 모니터링
    ↓
SRE 지표화
    ↓
옵저버빌리티 확장
    ↓
카오스·자동 복구
    ↓
AIOps·예측 운영
```

---

## 8. 관련 개념 맵

| 분류 | 관련 개념 |
|:---|:---|
| 상위 개념 | GitOps, 옵저버빌리티 (Observability), IaC (Infrastructure as Code) |
| 연관 기술 | Grafana Provisioning, Grafonnet, Terraform grafana provider, Grafana Foundation SDK |
| 비교 대상 | 수동 UI 생성 vs Dashboard as Code, Grafonnet vs Terraform |
